#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W3 common primitives (stdlib only).

Strict JSON, raw receipts, path containment and a fixed process runner.
This module is part of the W3 isolated product slice; it never writes the
adopted pack or any W2 protected path.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_REFUSED = 2
EXIT_BLOCKED = 3
EXIT_UNBOUND = 4
EXIT_UNREPRODUCED = 5

SUBJECT_ID = "FHS-5_PLP/W3/CONTROL_PACK"
SCOPE = "W3-NF-01"
PROJECT_ID = "FHS-5_PLP"
WAVE_ID = "W3"

ADVICE = [
    "FIX_NOW",
    "BIND_EXISTING",
    "ACTIVATE_HOST",
    "RUN_AFFECTED_TEST",
    "FIX_PD",
    "PI_CHANGE_REQUEST",
    "WAIT_ORIGINAL_AUTHORITY",
    "DEFER_TO_PHASE",
    "RECOMMEND_CLOSE",
    "PARK_UNTIL_DELTA",
]

ADVICE_ALIAS = {
    "FIX_NOW": "CODE_FIX",
    "BIND_EXISTING": "BIND_REPAIR",
    "ACTIVATE_HOST": "ACTIVATE_HOST",
    "RUN_AFFECTED_TEST": "CASE_TEST",
    "FIX_PD": "PD_CHANGE",
    "PI_CHANGE_REQUEST": "PI_CHANGE",
    "WAIT_ORIGINAL_AUTHORITY": "AUTHORITY_REQUEST",
    "DEFER_TO_PHASE": "DEFER_TO_WAVE",
    "RECOMMEND_CLOSE": "CLOSE_AFTER_ORIGINAL_ACK",
    "PARK_UNTIL_DELTA": "PARK_NO_DELTA",
}

HYPOTHESES = [
    "H-CODE-MISSING",
    "H-CODE-EXISTS-BINDING-MISSING",
    "H-HOST-NOT-ACTUAL_SERVED",
    "H-CASE_ORACLE_RUN_MISSING",
    "H-PD_DRIFT",
    "H-PI_SOURCE_GAP",
    "H-AUTHORITY_UNBOUND",
    "H-PHASE_NONAPPLICABLE",
    "H-RESEARCH_SOURCE_UNAVAILABLE",
    "H-ALREADY_COMPLETE_SCOPE",
]

FAR_STATES = [
    "HIT",
    "ZERO_RELEVANT_HIT",
    "UNAVAILABLE",
    "BLOCKED_BY_AUTHORITY",
    "ERROR",
]

REFUSAL_TOKENS = {
    "UNAVAILABLE", "FROZEN_IDENTITY_MISMATCH", "UNREPRODUCED",
    "DELTA_UNVERIFIED", "FALSE_AUTHORITY", "FALSE_INDEPENDENT",
    "ORIGINAL_READER_UNBOUND", "WRITE_SCOPE_VIOLATION",
    "ALTERNATIVE_INSUFFICIENT", "BLOCKED_BY_AUTHORITY", "RUNNER_UNBOUND",
    "RAW_UNTRUSTED", "CANDIDATE_CHANGED",
}

NINE_KEYS = [
    "subject",
    "scope",
    "source_sha",
    "repo_head",
    "host_id",
    "policy_epoch",
    "oracle_sha",
    "world_raw_sha",
    "first_fail",
]

SEVEN_KEYS = [
    "source_sha",
    "repo_head",
    "host_id",
    "policy_epoch",
    "oracle_sha",
    "world_raw_sha",
    "first_fail",
]

SEVEN_TO_NINE = {
    "source_sha": "source_sha",
    "repo_head": "repo_head",
    "host_id": "host_id",
    "policy_epoch": "policy_epoch",
    "oracle_sha": "oracle_sha",
    "world_raw_sha": "world_raw_sha",
    "first_fail": "first_fail",
    "subject": "subject",
    "scope": "scope",
}


class W3Error(Exception):
    def __init__(self, token: str, detail: str = "", exit_code: int = EXIT_REFUSED):
        super().__init__(token + (": " + detail if detail else ""))
        self.token = token
        self.detail = detail
        self.exit_code = exit_code


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def file_bytes(path) -> int:
    return os.path.getsize(path)


def line_count(path) -> int:
    return len(Path(path).read_bytes().decode("utf-8").splitlines())


def _no_dup(pairs):
    seen = set()
    out = {}
    for k, v in pairs:
        if k in seen:
            raise W3Error("DUPLICATE_KEY", k)
        seen.add(k)
        out[k] = v
    return out


def load_json_strict(path):
    raw = Path(path).read_bytes().decode("utf-8")
    if raw.startswith("\ufeff"):
        raw = raw[1:]
    try:
        return json.loads(raw, object_pairs_hook=_no_dup)
    except W3Error:
        raise
    except Exception as exc:
        raise W3Error("SCHEMA_UNSUPPORTED", f"{path}: {type(exc).__name__}")


def canon(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_obj(obj) -> str:
    return sha256_bytes(canon(obj).encode("utf-8"))


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": str(p), "sha256": sha256_file(p), "bytes": file_bytes(p)}


def write_bytes(path, data: bytes):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return {"path": str(p), "sha256": sha256_bytes(data), "bytes": len(data)}


def is_within(root, target) -> bool:
    try:
        r = os.path.normcase(os.path.realpath(root))
        t = os.path.normcase(os.path.realpath(target))
    except Exception:
        return False
    try:
        return os.path.commonpath([r, t]) == r
    except Exception:
        return False


def resolve_inside(root, rel, must_exist=False):
    if rel is None:
        raise W3Error("INVALID_PATH", "null")
    s = str(rel)
    if "\x00" in s or s.startswith("\\\\") or s.startswith("//"):
        raise W3Error("INVALID_PATH", s)
    if os.path.isabs(s) or re.match(r"^[A-Za-z]:", s):
        raise W3Error("INVALID_PATH", s)
    norm = os.path.normpath(s)
    if norm == ".." or norm.startswith(".." + os.sep):
        raise W3Error("INVALID_PATH", s)
    p = os.path.abspath(os.path.join(root, norm))
    if not is_within(root, p):
        raise W3Error("INVALID_PATH", s)
    if os.path.exists(p) and hasattr(os.path, "islink") and os.path.islink(p):
        raise W3Error("INVALID_PATH", "symlink:" + s)
    if must_exist and not os.path.exists(p):
        raise W3Error("INVALID_PATH", "missing:" + s)
    return p


def tree_digest(root, skip_names=(".git", "__pycache__")) -> dict:
    root = os.path.abspath(root)
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in skip_names)
        for name in sorted(filenames):
            if name in skip_names:
                continue
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            rows.append(rel + "\t" + str(os.path.getsize(p)) + "\t" + sha256_file(p))
    rows.sort()
    blob = "".join(r + "\n" for r in rows).encode("utf-8")
    return {"entries": len(rows), "tree_sha256": sha256_bytes(blob), "rows": rows}


def run_process(argv, cwd, timeout_s=120, env_allow=None, merge_env=True):
    base = {k: v for k, v in os.environ.items() if k.upper() in {
        "PATH", "TEMP", "TMP", "PYTHONIOENCODING", "PYTHONHASHSEED",
        "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "USERPROFILE",
        "LOCALAPPDATA", "APPDATA", "PROGRAMDATA", "NUMBER_OF_PROCESSORS",
        "PROCESSOR_ARCHITECTURE", "OS",
    }}
    if env_allow:
        base.update({str(k): str(v) for k, v in env_allow.items()})
    start = time.time()
    try:
        proc = subprocess.run(
            [str(a) for a in argv],
            cwd=str(cwd),
            capture_output=True,
            timeout=timeout_s,
            env=base,
        )
        out, err, code = proc.stdout, proc.stderr, proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or b""
        err = exc.stderr or b""
        code = None
        timed_out = True
    end = time.time()
    return {
        "argv": [str(a) for a in argv],
        "cwd": str(cwd),
        "timeout_s": timeout_s,
        "start": round(start, 3),
        "end": round(end, 3),
        "exit": code,
        "timed_out": timed_out,
        "stdout": out,
        "stderr": err,
        "stdout_sha256": sha256_bytes(out),
        "stderr_sha256": sha256_bytes(err),
    }


def strip_binary(proc_record: dict) -> dict:
    return {k: v for k, v in proc_record.items() if k not in ("stdout", "stderr")}


def env_public() -> dict:
    return {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED", "0"),
        "HOST_ID": "AUTHOR_LOCAL_WINDOWS",
        "POLICY_EPOCH": "LOCAL-20261126",
    }


def evidence_root(root, run_id) -> Path:
    p = Path(root) / "evidence" / run_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def host_identity() -> dict:
    return {
        "host_id": "AUTHOR_LOCAL_WINDOWS",
        "os_principal": os.environ.get("USERNAME", "local-user"),
        "policy_epoch": "LOCAL-20261126",
        "product_host": "UNBOUND",
        "repo_principal": "UNBOUND",
    }


def json_safe(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8", "replace")
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    return obj


def emit(obj, code=EXIT_PASS):
    sys.stdout.write(json.dumps(json_safe(obj), ensure_ascii=False, indent=2) + "\n")
    sys.stdout.flush()
    return code
