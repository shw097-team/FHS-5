#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for the FHS-5 W0 NF CODEX execution harness."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "01_PACK" / "FHS-5_PLP_W0_NATIVE_FIRST"
REPO = ROOT / "02_CANDIDATE" / "repo"
PARTIES = ROOT / "03_PARTIES"
EVID = ROOT / "10_EVIDENCE"
TQAEP = ROOT / "05_TQAEP"
TMP = TQAEP / "tmp"

for _p in (EVID, TMP / "root", TMP / "outside"):
    _p.mkdir(parents=True, exist_ok=True)

SECRET_RE = re.compile(
    r"(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path | str) -> str:
    return sha_bytes(Path(path).read_bytes())


def canonical_sha(obj) -> str:
    return sha_bytes(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def redact(text: str) -> tuple[str, bool]:
    hit = bool(SECRET_RE.search(text))
    return SECRET_RE.sub("[REDACTED]", text), hit


def base_env(extra: dict | None = None) -> dict:
    env = dict(os.environ)
    env["TEMP"] = str(TMP)
    env["TMP"] = str(TMP)
    env["TMPDIR"] = str(TMP)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if extra:
        env.update(extra)
    return env


def run(
    argv: list[str],
    cwd: Path | str,
    timeout: int = 60,
    env_extra: dict | None = None,
    raw_dir: Path | None = None,
    tag: str | None = None,
) -> dict:
    started = time.time()
    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        env=base_env(env_extra),
        capture_output=True,
        timeout=timeout,
    )
    elapsed = round(time.time() - started, 3)
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace")
    out_red, hit_out = redact(out)
    err_red, hit_err = redact(err)
    result = {
        "argv": argv,
        "cwd": str(Path(cwd).resolve()),
        "exit": proc.returncode,
        "stdout": out_red,
        "stderr": err_red,
        "stdout_sha256": sha_bytes(proc.stdout),
        "stderr_sha256": sha_bytes(proc.stderr),
        "elapsed_s": elapsed,
        "timestamp": now(),
        "secret_hit": hit_out or hit_err,
    }
    if raw_dir is not None:
        raw_dir = Path(raw_dir)
        raw_dir.mkdir(parents=True, exist_ok=True)
        name = tag or ("cmd_%d" % int(started * 1000))
        (raw_dir / f"{name}.stdout.txt").write_bytes(proc.stdout)
        (raw_dir / f"{name}.stderr.txt").write_bytes(proc.stderr)
        (raw_dir / f"{name}.meta.json").write_text(
            json.dumps(
                {k: result[k] for k in ("argv", "cwd", "exit", "stdout_sha256", "stderr_sha256", "timestamp")},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        def _rel(p: Path) -> str:
            try:
                return str(p.relative_to(ROOT))
            except ValueError:
                return str(p)

        result["raw_refs"] = {
            "stdout": _rel(raw_dir / f"{name}.stdout.txt"),
            "stderr": _rel(raw_dir / f"{name}.stderr.txt"),
            "meta": _rel(raw_dir / f"{name}.meta.json"),
        }
    return result


def cli(argv: list[str], cwd: Path, timeout: int = 30, raw_dir: Path | None = None,
        tag: str | None = None, env_extra: dict | None = None) -> dict:
    env = {"PYTHONPATH": str(REPO)}
    if env_extra:
        env.update(env_extra)
    return run([sys.executable, "-m", "briefcheck", *argv], cwd, timeout, env, raw_dir, tag)


def write_json(path: Path, obj) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True).stdout.strip()


def all_files(base: Path, skip_git: bool = True):
    for p in sorted(Path(base).rglob("*")):
        if not p.is_file():
            continue
        if skip_git and ".git" in p.parts:
            continue
        if "__pycache__" in p.parts:
            continue
        yield p


def snapshot(base: Path) -> dict[str, str]:
    return {p.relative_to(base).as_posix(): sha_file(p) for p in all_files(base)}


def receipt(case_id: str, *, expected, observed, verdict: str, first_fail: str = "", **kw) -> dict:
    r = {
        "run_id": f"{case_id}-{datetime.now().strftime('%Y%m%dT%H%M%S')}",
        "case_id": case_id,
        "candidate_ref": kw.pop("candidate_ref", None),
        "candidate_sha": kw.pop("candidate_sha", None),
        "source_refs": kw.pop("source_refs", []),
        "fixture_sha": kw.pop("fixture_sha", None),
        "oracle_sha": kw.pop("oracle_sha", None),
        "cwd": kw.pop("cwd", None),
        "argv": kw.pop("argv", []),
        "runtime": kw.pop("runtime", None),
        "exit": kw.pop("exit", None),
        "stdout_sha": kw.pop("stdout_sha", None),
        "stderr_sha": kw.pop("stderr_sha", None),
        "pre_state": kw.pop("pre_state", None),
        "post_state": kw.pop("post_state", None),
        "recovery_ref": kw.pop("recovery_ref", None),
        "expected": expected,
        "observed": observed,
        "verdict": verdict,
        "first_fail": first_fail,
        "checker_identity": kw.pop("checker_identity", "maker-run; independent check in 06_CHECKER"),
        "consumer_ref": kw.pop("consumer_ref", None),
        "not_covered": kw.pop("not_covered", []),
    }
    r.update(kw)
    return r


def copy_tree_clean(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return dst
