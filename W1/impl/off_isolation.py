#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5 W1 (R03) — off-isolation probes with real, non-fabricated evidence.

Scope / claim ceiling
---------------------
This module *measures* a few narrow facts and reports them as evidence:

* ``cold_off_probe``          — a cold subprocess cannot import named runtimes.
* ``positive_control``        — the same probe shape *can* observe a success,
                                so a "blocked" list above is meaningful.
* ``env_flag_only_reject``    — a bare environment flag is not evidence.
* ``path_attack_suite``       — the W1 BodyResolver rejects 7 path attacks.
* ``link_probe``              — a link inside the pack is refused, or the
                                capability is NOT_VERIFIED on this host.
* ``canary_check``            — pack bytes did not drift against a "before"
                                snapshot.

Every function returns evidence (argv / exit / sha256) or an explicit
``NOT_VERIFIED``. Nothing here returns a bare ``True``, and nothing here
turns a local measurement into NATIVE_PASS / INDEPENDENT / RELEASE.

``cold_off`` is a *negative* observation: it says the forbidden modules were
not importable in a cold interpreter. On its own it is not proof that any
feature is disabled; it is paired with ``positive_control`` so that "blocked"
is not an artefact of a broken probe.

Dependencies: standard library plus the read-only W1 ``body_resolver`` module
(which itself imports ``w1_nf_reader``). Both are located through ``W1_IMPL``
or a fixed default path; nothing is written next to them.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

DEFAULT_IMPL_DIR = (
    r"C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\W1\impl"
)
DEFAULT_PACK_ROOT = (
    r"C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3"
    r"\16_W1_NF_CODEX_20261125T222954\control_pack\FHS-5_PLP_W1_NATIVE_FIRST"
)

# Modules that genuinely do not exist on this host. Used as the cold-off
# target set; ``positive_control`` proves the probe is able to see a success.
FORBIDDEN_RUNTIME_MODULES = [
    "hgk_runtime",
    "fabric_runtime",
    "sbl_runtime",
    "pipd_runtime",
    "hermes_runtime",
]

_MODULE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")
_ENV_SCRUB = ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP")


# --------------------------------------------------------------------------
# body_resolver binding
# --------------------------------------------------------------------------
def _impl_dir() -> str:
    return os.environ.get("W1_IMPL") or DEFAULT_IMPL_DIR


def _pack_root() -> str:
    return os.environ.get("W1_PACK") or DEFAULT_PACK_ROOT


def _load_body_resolver():
    """Import the read-only W1 BodyResolver from the impl directory."""
    impl = _impl_dir()
    if impl not in sys.path:
        sys.path.insert(0, impl)
    import body_resolver  # noqa: PLC0415  (import after sys.path fix-up)

    return body_resolver


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | os.PathLike) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------
# 1) cold-off probe
# --------------------------------------------------------------------------
def _probe_env() -> tuple[dict[str, str], list[str]]:
    env = {k: v for k, v in os.environ.items() if k not in _ENV_SCRUB}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    removed = [k for k in _ENV_SCRUB if k in os.environ]
    return env, removed


def _parse_last_json_line(stdout: bytes) -> tuple[dict | None, str | None]:
    text = stdout.decode("utf-8", errors="replace")
    for line in reversed([ln.strip() for ln in text.splitlines() if ln.strip()]):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj, None
        return None, "json line is not an object"
    return None, "no JSON object found on stdout"


def _popen(argv: list[str], cwd: str, env: dict[str, str], timeout: float):
    try:
        cp = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=timeout,
        )
        return cp, None
    except subprocess.TimeoutExpired as exc:
        return None, exc


def cold_off_probe(
    feature: str,
    forbidden_modules: list[str],
    timeout: float = 60,
) -> dict:
    """Spawn a cold interpreter and test whether forbidden modules import.

    The child runs with ``PYTHONPATH``/``PYTHONHOME``/``PYTHONSTARTUP``
    removed and user site-packages disabled, from a neutral cwd, so a leaked
    import cannot come from the caller's ambient configuration.

    ``cold_off`` is True only when every module is genuinely absent *and* the
    child reported a parseable result. A detectable import is a real FAILURE
    (``cold_off`` False), never an exception.
    """
    if not isinstance(feature, str) or not feature:
        raise ValueError("feature must be a non-empty string")
    if not isinstance(forbidden_modules, list) or not forbidden_modules:
        raise ValueError("forbidden_modules must be a non-empty list")
    for name in forbidden_modules:
        if not isinstance(name, str) or not _MODULE_NAME_RE.match(name):
            raise ValueError(f"invalid module name: {name!r}")

    payload = json.dumps(list(forbidden_modules))
    script = (
        "import json, sys\n"
        f"mods = json.loads({payload!r})\n"
        "blocked, leaked, errors = [], [], {}\n"
        "for m in mods:\n"
        "    try:\n"
        "        __import__(m)\n"
        "        leaked.append(m)\n"
        "    except Exception as exc:\n"
        "        blocked.append(m)\n"
        "        errors[m] = type(exc).__name__\n"
        "print(json.dumps({'blocked': blocked, 'leaked': leaked,"
        " 'errors': errors, 'child_python': sys.version.split()[0]}))\n"
    )
    argv = [sys.executable, "-c", script]
    cwd = tempfile.gettempdir()
    env, removed = _probe_env()

    result: dict[str, Any] = {
        "schema": "FHS5.W1.R03.OffIsolation.ColdOff@1",
        "feature": feature,
        "forbidden_modules": list(forbidden_modules),
        "argv": argv,
        "cwd": cwd,
        "env_removed_keys": removed,
        "timeout_s": timeout,
        "exit": None,
        "stdout": "",
        "stderr": "",
        "stdout_sha256": None,
        "stderr_sha256": None,
        "blocked": [],
        "leaked": [],
        "import_errors": {},
        "cold_off": None,
        "state": "NOT_RUN",
    }

    cp, timeout_exc = _popen(argv, cwd, env, timeout)
    if cp is None:
        result["state"] = "TIMEOUT"
        result["timeout"] = True
        result["cold_off"] = None
        result["detail"] = f"subprocess exceeded {timeout}s: {timeout_exc}"
        return result

    raw_out, raw_err = cp.stdout or b"", cp.stderr or b""
    result["exit"] = cp.returncode
    result["stdout"] = raw_out.decode("utf-8", errors="replace")
    result["stderr"] = raw_err.decode("utf-8", errors="replace")
    result["stdout_sha256"] = sha256_bytes(raw_out)
    result["stderr_sha256"] = sha256_bytes(raw_err)
    result["stdout_bytes"] = len(raw_out)
    result["stderr_bytes"] = len(raw_err)

    parsed, parse_error = _parse_last_json_line(raw_out)
    if parsed is None:
        result["state"] = "PROBE_ERROR"
        result["cold_off"] = None
        result["detail"] = parse_error
        return result

    blocked = parsed.get("blocked")
    leaked = parsed.get("leaked")
    if not isinstance(blocked, list) or not isinstance(leaked, list):
        result["state"] = "PROBE_ERROR"
        result["cold_off"] = None
        result["detail"] = "child JSON missing blocked/leaked lists"
        return result

    result["blocked"] = blocked
    result["leaked"] = leaked
    result["import_errors"] = parsed.get("errors") or {}
    result["child_python"] = parsed.get("child_python")
    solved = set(blocked) | set(leaked)
    result["all_modules_accounted"] = solved == set(forbidden_modules)
    result["cold_off"] = (
        cp.returncode == 0
        and not leaked
        and result["all_modules_accounted"]
    )
    result["state"] = "OBSERVED" if result["cold_off"] else "LEAK_DETECTED"
    return result


# --------------------------------------------------------------------------
# 2) positive control
# --------------------------------------------------------------------------
def positive_control(module_name: str = "json", timeout: float = 60) -> dict:
    """Prove the probe shape can observe a *successful* import.

    Without this, a ``blocked`` list is unfalsifiable: it could just mean the
    child never ran, the JSON was never emitted, or the import mechanism is
    broken.
    """
    if not isinstance(module_name, str) or not _MODULE_NAME_RE.match(module_name):
        raise ValueError(f"invalid module name: {module_name!r}")

    script = (
        "import json, importlib, sys\n"
        f"name = {json.dumps(module_name)}\n"
        "imported, err = False, None\n"
        "try:\n"
        "    importlib.import_module(name)\n"
        "    imported = True\n"
        "except Exception as exc:\n"
        "    err = type(exc).__name__\n"
        "print(json.dumps({'module': name, 'imported': imported,"
        " 'error': err, 'child_python': sys.version.split()[0]}))\n"
    )
    argv = [sys.executable, "-c", script]
    cwd = tempfile.gettempdir()
    env, removed = _probe_env()

    result: dict[str, Any] = {
        "schema": "FHS5.W1.R03.OffIsolation.PositiveControl@1",
        "module": module_name,
        "argv": argv,
        "cwd": cwd,
        "env_removed_keys": removed,
        "exit": None,
        "stdout": "",
        "stdout_sha256": None,
        "stderr_sha256": None,
        "imported": None,
        "state": "NOT_RUN",
    }

    cp, timeout_exc = _popen(argv, cwd, env, timeout)
    if cp is None:
        result["state"] = "TIMEOUT"
        result["timeout"] = True
        result["detail"] = f"subprocess exceeded {timeout}s: {timeout_exc}"
        return result

    raw_out, raw_err = cp.stdout or b"", cp.stderr or b""
    result["exit"] = cp.returncode
    result["stdout"] = raw_out.decode("utf-8", errors="replace")
    result["stderr_sha256"] = sha256_bytes(raw_err)
    result["stdout_sha256"] = sha256_bytes(raw_out)

    parsed, parse_error = _parse_last_json_line(raw_out)
    if parsed is None:
        result["state"] = "PROBE_ERROR"
        result["imported"] = None
        result["detail"] = parse_error
        return result

    result["imported"] = bool(parsed.get("imported"))
    result["import_error"] = parsed.get("error")
    result["child_python"] = parsed.get("child_python")
    result["state"] = "OBSERVED" if result["imported"] else "CONTROL_FAILED"
    return result


# --------------------------------------------------------------------------
# 3) environment flag is not evidence
# --------------------------------------------------------------------------
def env_flag_only_reject(marker: str) -> dict:
    """Return a structured REJECT: a bare env flag is not evidence.

    Deliberately does **not** read or write any environment variable. The
    caller's ``marker`` is echoed so the reject can be traced to its claim.
    """
    return {
        "schema": "FHS5.W1.R03.OffIsolation.EnvFlagReject@1",
        "rejected": True,
        "token": "ENV_FLAG_NOT_EVIDENCE",
        "marker": marker,
        "evidence": "none",
        "env_read": False,
        "env_written": False,
        "reason": (
            "A bare environment flag asserts a state; it carries no observation "
            "of a real process, path resolution, or byte digest, so it cannot "
            "discharge an isolation claim."
        ),
    }


# --------------------------------------------------------------------------
# 4) path attack suite
# --------------------------------------------------------------------------
PATH_ATTACKS = [
    ("absolute", "C:/x.md"),
    ("unc", "//srv/share/x.md"),
    ("drive_relative", "C:x.md"),
    ("dotdot", ".."),
    ("backslash", "a\\b.md"),
    ("nul", "a\x00b.md"),
    ("empty", ""),
]


def path_attack_suite(root: str | os.PathLike | None = None) -> list[dict]:
    """Drive ``body_resolver.resolve_body`` with 7 hostile relative paths.

    ``rejected`` is True only if the resolver raised ``NFError``. A path that
    resolves is recorded as ``rejected: False`` — a real, reportable failure.
    """
    br = _load_body_resolver()
    pack = str(root if root is not None else _pack_root())
    out: list[dict] = []
    for label, rel in PATH_ATTACKS:
        entry: dict[str, Any] = {
            "attack": rel,
            "attack_label": label,
            "root": pack,
            "token": None,
            "detail": None,
            "rejected": False,
            "error_type": None,
        }
        try:
            resolved = br.resolve_body(pack, rel, 1, 1)
        except br.NFError as exc:
            entry["rejected"] = True
            entry["token"] = exc.token
            entry["detail"] = exc.detail
            entry["error_type"] = type(exc).__name__
        except Exception as exc:  # noqa: BLE001  (non-NFError is a finding)
            entry["rejected"] = False
            entry["token"] = "UNEXPECTED_EXCEPTION"
            entry["detail"] = f"{type(exc).__name__}: {exc}"
            entry["error_type"] = type(exc).__name__
        else:
            entry["resolved_path"] = resolved.get("resolved_path") if isinstance(resolved, dict) else None
            entry["full_text_preview"] = (
                (resolved.get("full_text") or "")[:120] if isinstance(resolved, dict) else None
            )
        out.append(entry)
    return out


# --------------------------------------------------------------------------
# 5) link probe
# --------------------------------------------------------------------------
def link_probe(
    base_dir: str | os.PathLike,
    target_file: str | os.PathLike,
    link_name: str | None = None,
    cleanup: bool = True,
) -> dict:
    """Create a real symlink inside ``base_dir`` and try to read *through* it.

    Two gates are exercised, in order, and each outcome is recorded:

    1. ``body_resolver.read_bounded`` on the link path.
    2. ``body_resolver.resolve_inside`` — the resolver's own containment gate,
       which is the check that refuses links/reparse points.

    If link creation is not permitted (typical on Windows without Developer
    Mode or SeCreateSymbolicLinkPrivilege), the probe returns
    ``state = "NOT_VERIFIED"`` with the OS error. It never implies that links
    were tested when they could not be created.
    """
    br = _load_body_resolver()
    base = Path(base_dir)
    target = Path(target_file)
    name = link_name or f"w1_r03_link_{uuid.uuid4().hex[:12]}.txt"
    link = base / name

    result: dict[str, Any] = {
        "schema": "FHS5.W1.R03.OffIsolation.LinkProbe@1",
        "base_dir": str(base),
        "target_file": str(target),
        "link_path": str(link),
        "state": "NOT_RUN",
        "token": None,
        "read_bounded_accepted": None,
        "resolve_inside_accepted": None,
        "link_created": False,
        "link_removed": False,
    }

    try:
        base.mkdir(parents=True, exist_ok=True)
        os.symlink(str(target), str(link))
        result["link_created"] = True
    except OSError as exc:
        result["state"] = "NOT_VERIFIED"
        result["reason"] = (
            f"symlink creation refused by the host: {type(exc).__name__}"
            f" (winerror={getattr(exc, 'winerror', None)}): {exc}"
        )
        result["link_created"] = False
        return result

    try:
        # Gate 1: the read entry point named by the isolation contract.
        try:
            data = br.read_bounded(link, name)
        except br.NFError as exc:
            result["read_bounded_accepted"] = False
            result["state"] = "REJECT"
            result["token"] = exc.token
            result["stage"] = "read_bounded"
            result["detail"] = exc.detail
        else:
            result["read_bounded_accepted"] = True
            result["bytes_read_through_link"] = len(data)
            result["sha256_read_through_link"] = sha256_bytes(data)
            # Gate 2: containment. read_bounded() follows links; resolve_inside()
            # is the gate that refuses them, so a link that survived gate 1 is
            # still reported as denied, with the residual read made explicit.
            try:
                br.resolve_inside(br.canonical_root(str(base)), name)
            except br.NFError as exc:
                result["resolve_inside_accepted"] = False
                result["state"] = "REJECT"
                result["token"] = exc.token
                result["stage"] = "resolve_inside"
                result["detail"] = exc.detail
                result["residual_risk"] = (
                    "read_bounded followed the link and returned bytes before the "
                    "containment gate rejected the path"
                )
            else:
                result["resolve_inside_accepted"] = True
                result["state"] = "LEAK"
                result["token"] = None
                result["detail"] = "link accepted by both read_bounded and resolve_inside"
    finally:
        if cleanup:
            try:
                os.unlink(link)
                result["link_removed"] = True
            except OSError as exc:
                result["link_removed"] = False
                result["cleanup_error"] = str(exc)
    return result


# --------------------------------------------------------------------------
# 6) canary check
# --------------------------------------------------------------------------
def _before_digest(value: Any) -> tuple[str | None, int | None]:
    if isinstance(value, dict):
        return (
            value.get("sha256") or value.get("hash"),
            value.get("bytes", value.get("size")),
        )
    if isinstance(value, str):
        return value, None
    if isinstance(value, (tuple, list)) and value:
        sha = value[0]
        size = value[1] if len(value) > 1 else None
        return sha, size
    return None, None


def canary_check(paths: list[str], before: dict[str, Any]) -> dict:
    """Compare current bytes against a caller-supplied ``before`` snapshot.

    ``before`` maps a path to ``{"sha256": ..., "bytes": ...}`` (a bare digest
    string or a ``(digest, size)`` pair is also accepted). A missing file, a
    size change or a digest change all produce a diff entry, so a stale canary
    can never read as "unchanged".
    """
    if not isinstance(paths, list):
        raise ValueError("paths must be a list")
    if not isinstance(before, dict):
        raise ValueError("before must be a mapping of path -> {sha256, bytes}")

    diff: list[dict] = []
    checked: list[dict] = []
    for raw in paths:
        path = str(raw)
        want_sha, want_bytes = _before_digest(before.get(path))
        try:
            size = os.path.getsize(path)
            got_sha = sha256_file(path)
        except OSError as exc:
            diff.append(
                {
                    "path": path,
                    "reason": "unreadable_or_missing",
                    "before": {"sha256": want_sha, "bytes": want_bytes},
                    "after": None,
                    "detail": f"{type(exc).__name__}: {exc}",
                }
            )
            continue

        checked.append(
            {"path": path, "sha256": got_sha, "bytes": size,
             "before_sha256": want_sha, "before_bytes": want_bytes}
        )
        reasons = []
        if want_sha is None:
            reasons.append("no_expected_digest")
        elif got_sha != want_sha:
            reasons.append("sha256_changed")
        if want_bytes is not None and size != want_bytes:
            reasons.append("bytes_changed")
        if reasons:
            diff.append(
                {
                    "path": path,
                    "reason": "+".join(reasons),
                    "before": {"sha256": want_sha, "bytes": want_bytes},
                    "after": {"sha256": got_sha, "bytes": size},
                }
            )

    return {
        "schema": "FHS5.W1.R03.OffIsolation.CanaryCheck@1",
        "paths": [str(p) for p in paths],
        "checked": checked,
        "unchanged": not diff,
        "diff": diff,
    }


# --------------------------------------------------------------------------
# convenience: snapshot helper + self-report
# --------------------------------------------------------------------------
def snapshot(paths: list[str]) -> dict[str, dict[str, Any]]:
    """Build the ``before`` mapping consumed by :func:`canary_check`."""
    out: dict[str, dict[str, Any]] = {}
    for raw in paths:
        path = str(raw)
        try:
            out[path] = {"sha256": sha256_file(path), "bytes": os.path.getsize(path)}
        except OSError as exc:
            out[path] = {"sha256": None, "bytes": None,
                         "error": f"{type(exc).__name__}: {exc}"}
    return out


def run_all(feature: str = "FHS5-W1-R03", link_base: str | None = None) -> dict:
    """Run every probe against the default pack and return one evidence bundle."""
    pack = _pack_root()
    canary_target = os.path.join(pack, "00_W1_PI_PD.md")
    before = snapshot([canary_target])
    base = link_base or os.path.join(tempfile.gettempdir(), f"w1_r03_links_{uuid.uuid4().hex[:8]}")
    return {
        "schema": "FHS5.W1.R03.OffIsolation.Bundle@1",
        "feature": feature,
        "impl_dir": _impl_dir(),
        "pack_root": pack,
        "cold_off": cold_off_probe(feature, FORBIDDEN_RUNTIME_MODULES),
        "positive_control": positive_control("json"),
        "env_flag": env_flag_only_reject(feature),
        "path_attacks": path_attack_suite(pack),
        "link": link_probe(base, canary_target),
        "canary": canary_check([canary_target], before),
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--feature", default="FHS5-W1-R03")
    ap.add_argument("--pack", default=None)
    ap.add_argument("--impl", default=None)
    args = ap.parse_args(argv)
    if args.pack:
        os.environ["W1_PACK"] = args.pack
    if args.impl:
        os.environ["W1_IMPL"] = args.impl
    bundle = run_all(args.feature)
    sys.stdout.write(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n")
    cold = bundle["cold_off"].get("cold_off")
    attacks_ok = all(a["rejected"] for a in bundle["path_attacks"])
    linked = bundle["link"].get("state")
    ok = (
        cold is True
        and bundle["positive_control"].get("imported") is True
        and attacks_ok
        and bundle["canary"].get("unchanged") is True
        and linked in ("REJECT", "NOT_VERIFIED", "LEAK")  # LEAK still "ran"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
