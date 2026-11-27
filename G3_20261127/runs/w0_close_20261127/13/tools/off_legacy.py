#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D1: real legacy-provider OFF, with CPython-audit observation (r2).

r1 established the semantics: reviewer resolved dynamically, a double-fail is
never parity, and missing pieces fail closed.  r2 adds the observation the
original NF-T01 intent still required: loader / call / child / network are
recorded inside every product subprocess by a ``sitecustomize`` that installs
``sys.addaudithook``, with an independent positive-control probe and a
negative control proving that an absent observer cannot silently pass.

The audit layer is observation only.  It is not presented as an OS sandbox.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import tqaep_spec

OUT = lib.ROOT / "04_DEV_OPS"
PROFILE = OUT / "off_profile"
LEGACY = OUT / "off_legacy_src"
TRACE = lib.TMP / "off_trace.jsonl"
AUDIT_DIR = OUT / "raw" / "audit"
SITE = lib.ROOT / "tools" / "off_audit_site" / "sitecustomize.py"
PROBE = lib.ROOT / "tools" / "off_audit_probe.py"

FORBIDDEN = ("hgk", "fabric", "sbl", "fhs", "pipd", "hermes")
CHILD_EVENTS = ("subprocess.Popen", "_winapi.CreateProcess", "os.system",
                "os.spawn", "os.posix_spawn")

REVIEWER_CACHE_ROOT = Path(os.environ.get(
    "FHS5_REVIEWER_CACHE",
    r"C:\Users\user\.codex\plugins\cache\created-by-me-remote\plp-tpm-review",
))
REVIEWER_PREFERRED_VERSION = "1.0.1"


def _version_key(name: str):
    key = []
    for chunk in re.split(r"[.\-+_]", name):
        key.append((0, int(chunk), "") if chunk.isdigit() else (1, 0, chunk))
    return key


def resolve_reviewer():
    """Resolve the installed PLP reviewer script; never install or upgrade."""
    root = REVIEWER_CACHE_ROOT
    if not root.is_dir():
        return None, "REVIEWER_CACHE_MISSING:" + str(root)
    preferred = root / REVIEWER_PREFERRED_VERSION / "scripts" / "review_core.py"
    if preferred.is_file():
        return preferred, "PREFERRED_VERSION:" + REVIEWER_PREFERRED_VERSION
    found = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        script = child / "scripts" / "review_core.py"
        if script.is_file():
            found.append((_version_key(child.name), child.name, script))
    if not found:
        return None, "REVIEWER_SCRIPT_MISSING:" + str(root)
    found.sort()
    _key, version, script = found[-1]
    return script, "FALLBACK_VERSION:" + version


def _rel(path: Path) -> str:
    try:
        return str(Path(path).relative_to(lib.ROOT))
    except ValueError:
        return str(path)


def audit_path(tag: str) -> Path:
    return AUDIT_DIR / f"{tag}.jsonl"


def env(mode: str, tag: str | None = None) -> dict:
    """Build the subprocess environment for on / audit / off.

    ``on``    - product path only, no profile, no observer.
    ``audit`` - same observable profile, blocker disabled (transparency run).
    ``off``   - profile + legacy import blocker + observer.
    """
    assert mode in ("on", "audit", "off"), mode
    parts = ([str(PROFILE)] if mode in ("audit", "off") else []) + [
        str(lib.REPO), str(lib.ROOT / "tools")]
    e = {
        "PYTHONPATH": os.pathsep.join(parts),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "FHS5_AUDIT": "",
        "FHS5_OFF_PROFILE": "",
        "FHS5_TRACE": "",
    }
    if mode in ("audit", "off") and tag:
        e["FHS5_AUDIT"] = str(audit_path(tag))
    if mode == "off":
        e["FHS5_OFF_PROFILE"] = "1"
        e["FHS5_TRACE"] = str(TRACE)
    return e


def blocked_lines() -> list[dict]:
    if not TRACE.is_file():
        return []
    out = []
    for line in TRACE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def summarize(tag: str) -> dict:
    """Aggregate one subprocess audit stream into observation categories."""
    path = audit_path(tag)
    rec = {
        "tag": tag, "file": _rel(path), "sha256": None, "exists": path.is_file(),
        "events": 0, "pids": [], "by_event": {}, "import_events": 0,
        "imports": [], "legacy_import_attempts": [], "legacy_import_observed": [],
        "child_events": 0, "child_by_event": {}, "child_commands": [],
        "network_events": 0, "network_by_event": {},
        "native_events": 0, "native_by_event": {},
        "opens": 0, "truncated": False, "malformed_lines": 0,
    }
    if not rec["exists"]:
        return rec
    imports, attempts, pids, cmds = set(), set(), set(), []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception:
            rec["malformed_lines"] += 1
            continue
        event = item.get("event")
        args = item.get("args") or []
        rec["events"] += 1
        pids.add(item.get("pid"))
        rec["by_event"][event] = rec["by_event"].get(event, 0) + 1
        if event == "import":
            rec["import_events"] += 1
            name = args[0] if args else ""
            imports.add(name)
            top = str(name).split(".")[0].lower()
            if any(top.startswith(prefix) for prefix in FORBIDDEN):
                attempts.add(name)
        elif event == "open":
            rec["opens"] += 1
        elif event in CHILD_EVENTS:
            rec["child_events"] += 1
            rec["child_by_event"][event] = rec["child_by_event"].get(event, 0) + 1
            if event == "subprocess.Popen" and len(args) >= 2:
                cmds.append({"exe": args[0], "argv": args[1]})
        elif str(event).startswith("socket."):
            rec["network_events"] += 1
            rec["network_by_event"][event] = rec["network_by_event"].get(event, 0) + 1
        elif str(event).startswith("ctypes."):
            rec["native_events"] += 1
            rec["native_by_event"][event] = rec["native_by_event"].get(event, 0) + 1
    rec["pids"] = sorted(p for p in pids if p is not None)
    rec["child_commands"] = cmds
    rec["imports"] = sorted(imports)
    rec["legacy_import_attempts"] = sorted(attempts)
    rec["truncated"] = "_truncated" in rec["by_event"]
    rec["sha256"] = lib.sha_file(path)
    return rec


def run_probe(tag: str, with_audit: bool) -> tuple[dict, dict, list]:
    work = OUT / "probe"
    work.mkdir(parents=True, exist_ok=True)
    path = audit_path(tag)
    if path.exists():
        path.unlink()
    result_file = work / f"{tag}.result.json"
    if result_file.exists():
        result_file.unlink()
    TRACE.write_text("", encoding="utf-8")
    e = env("off", tag if with_audit else None)
    if not with_audit:
        e["FHS5_AUDIT"] = ""
    e["PYTHONPATH"] = os.pathsep.join(
        [str(PROFILE), str(LEGACY), str(lib.REPO), str(lib.ROOT / "tools")])
    res = lib.run([sys.executable, str(PROBE), "--out", str(result_file),
                   "--workdir", str(work), "--expect", "blocked"],
                  lib.ROOT, env_extra=e, raw_dir=OUT / "raw", tag=tag)
    payload = {}
    if result_file.is_file():
        payload = json.loads(result_file.read_text(encoding="utf-8"))
    return res, payload, blocked_lines()


def evaluate_probe(payload: dict, obs: dict, blocked: list) -> dict:
    loop = payload.get("loopback") or {}
    native = payload.get("ctypes_load") or {}
    payload_blocked = payload.get("blocked_import") or {}
    return {
        "loader_blocked_import": bool(payload_blocked.get("ok"))
        and bool(obs.get("legacy_import_attempts"))
        and any(str(b.get("blocked", "")).startswith("hgk") for b in blocked),
        "loader_events": obs.get("import_events", 0) > 0,
        "open_observed": obs.get("opens", 0) > 0
        and bool((payload.get("open_marker") or {}).get("ok")),
        "child_spawn_observed": obs.get("child_by_event", {}).get("subprocess.Popen", 0) >= 1
        and obs.get("child_by_event", {}).get("_winapi.CreateProcess", 0) >= 1
        and bool((payload.get("child") or {}).get("ok")),
        "grandchild_pid_observed": len(obs.get("pids") or []) >= 2,
        "call_os_system_observed": obs.get("child_by_event", {}).get("os.system", 0) >= 1
        and bool((payload.get("os_system") or {}).get("ok")),
        "loopback_roundtrip_observed": obs.get("network_by_event", {}).get("socket.connect", 0) >= 1
        and obs.get("network_by_event", {}).get("socket.bind", 0) >= 1
        and loop.get("received") == "PONG"
        and loop.get("server_received") == ["PING"],
        "native_dlopen_observed": obs.get("native_by_event", {}).get("ctypes.dlopen", 0) >= 1
        and bool(native.get("ok")),
    }


GIT_LOCAL = {"rev-parse", "status", "diff", "log", "show", "ls-files",
             "for-each-ref", "symbolic-ref", "cat-file"}
GIT_NET = {"push", "fetch", "pull", "clone", "remote", "submodule"}


def classify_child(command: dict) -> dict:
    """Classify an observed child. Only local read-only git helpers are allowed."""
    exe = str(command.get("exe") or "").strip('"')
    argv = str(command.get("argv") or "")
    tokens = [token.strip('"') for token in argv.split()]
    if exe and exe != "None":
        name = Path(exe).name.lower()
    else:
        name = Path(tokens[0]).name.lower() if tokens else ""
    ok = (name in ("git", "git.exe")
          and any(token in GIT_LOCAL for token in tokens)
          and not any(token in GIT_NET for token in tokens))
    return {"exe": exe, "argv": argv[:400], "name": name, "ok": ok}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROFILE.mkdir(exist_ok=True)
    LEGACY.mkdir(exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    if not SITE.is_file():
        raise SystemExit("OBSERVATION_SITE_MISSING:" + str(SITE))
    if not PROBE.is_file():
        raise SystemExit("OBSERVATION_PROBE_MISSING:" + str(PROBE))
    (PROFILE / "sitecustomize.py").write_text(SITE.read_text(encoding="utf-8"), encoding="utf-8")
    (LEGACY / "hgk_core.py").write_text("VALUE = 1\n", encoding="utf-8")
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    TRACE.write_text("", encoding="utf-8")
    raw = OUT / "raw"

    # (1) blocker controls: must block under the flag, must allow without it.
    TRACE.write_text("", encoding="utf-8")
    ctrl_blocked = lib.run(
        [sys.executable, "-c", "import hgk_core; print('IMPORTED')"], lib.ROOT,
        env_extra=dict(env("off"), FHS5_AUDIT="",
                       PYTHONPATH=os.pathsep.join([str(PROFILE), str(LEGACY)])),
        raw_dir=raw, tag="off_control_blocked")
    blocked_ctrl = blocked_lines()
    TRACE.write_text("", encoding="utf-8")
    ctrl_allowed = lib.run(
        [sys.executable, "-c", "import hgk_core; print('IMPORTED')"], lib.ROOT,
        env_extra={"PYTHONPATH": str(LEGACY), "PYTHONDONTWRITEBYTECODE": "1"},
        raw_dir=raw, tag="off_control_allowed")
    TRACE.write_text("", encoding="utf-8")
    audit_ctrl_tag = "off_control_audit_only"
    audit_ctrl_path = audit_path(audit_ctrl_tag)
    if audit_ctrl_path.exists():
        audit_ctrl_path.unlink()
    ctrl_audit_only = lib.run(
        [sys.executable, "-c", "import hgk_core; print('IMPORTED')"], lib.ROOT,
        env_extra=dict(env("audit", audit_ctrl_tag),
                       PYTHONPATH=os.pathsep.join([str(PROFILE), str(LEGACY)])),
        raw_dir=raw, tag=audit_ctrl_tag)
    audit_ctrl_obs = summarize(audit_ctrl_tag)
    control_blocked_ok = (ctrl_blocked["exit"] != 0
                          and "FHS5_LEGACY_BLOCKED" in ctrl_blocked["stderr"]
                          and any(str(b.get("blocked", "")).startswith("hgk")
                                  for b in blocked_ctrl))
    control_allowed_ok = (ctrl_allowed["exit"] == 0
                          and "IMPORTED" in ctrl_allowed["stdout"])
    control_audit_only_ok = (ctrl_audit_only["exit"] == 0
                             and "IMPORTED" in ctrl_audit_only["stdout"]
                             and "hgk_core" in audit_ctrl_obs["imports"])
    control_ok = control_blocked_ok and control_allowed_ok and control_audit_only_ok

    # (2) independent observation positive control + absent-observer control.
    probe_res, probe_payload, probe_blocked = run_probe("off_audit_probe", True)
    probe_obs = summarize("off_audit_probe")
    probe_checks = evaluate_probe(probe_payload, probe_obs, probe_blocked)

    absent_res, absent_payload, absent_blocked = run_probe("off_audit_probe_absent", False)
    absent_obs = summarize("off_audit_probe_absent")
    absent_checks = evaluate_probe(absent_payload, absent_obs, absent_blocked)
    absent_rejected = (not absent_obs["exists"]) and not any(absent_checks.values())

    probe_ok = bool(probe_payload.get("all_ok")) and all(probe_checks.values())

    entries = []

    def payload(r):
        try:
            return json.loads(r["stdout"])
        except Exception:
            return {}

    def entry(name, make_argv, cwd, expect, semantics, **extra):
        TRACE.write_text("", encoding="utf-8")
        runs = {}
        for mode in ("on", "audit", "off"):
            tag = f"off_{name}_{mode}"
            path = audit_path(tag)
            if path.exists():
                path.unlink()
            runs[mode] = lib.run(make_argv(mode), cwd, env_extra=env(mode, tag),
                                 raw_dir=raw, tag=tag)
        blocked = blocked_lines()
        onj, aj, offj = (payload(runs[m]) for m in ("on", "audit", "off"))
        on_ok = bool(expect(runs["on"]["exit"], onj))
        audit_ok = bool(expect(runs["audit"]["exit"], aj))
        off_ok = bool(expect(runs["off"]["exit"], offj))
        same = semantics(onj) == semantics(offj)
        same_observed = semantics(onj) == semantics(aj)
        observation = {m: summarize(f"off_{name}_{m}") for m in ("on", "audit", "off")}
        ok = (on_ok and audit_ok and off_ok and same and same_observed
              and not blocked)
        rec = {
            "name": name, "on_exit": runs["on"]["exit"],
            "on_audit_exit": runs["audit"]["exit"],
            "off_exit": runs["off"]["exit"],
            "on_expected": on_ok, "on_audit_expected": audit_ok,
            "off_expected": off_ok, "same_semantics": same,
            "same_semantics_observed": same_observed,
            "blocked_attempts": blocked, "ok": ok,
            "on_semantics": semantics(onj), "off_semantics": semantics(offj),
            "observation": observation,
            "off_effect": {
                "legacy_import_attempts": observation["off"]["legacy_import_attempts"],
                "child_events": observation["off"]["child_events"],
                "network_events": observation["off"]["network_events"],
                "native_events": observation["off"]["native_events"],
            },
        }
        rec.update(extra)
        entries.append(rec)
        return rec

    root = lib.TQAEP / "tmp" / "root"
    if not (root / "case_ok.md").is_file():
        root.mkdir(parents=True, exist_ok=True)
        for p in (lib.REPO / "fixtures").glob("*.md"):
            import shutil as _sh
            _sh.copy2(p, root / p.name)

    pos_argv = [sys.executable, "-m", "briefcheck", "--root", str(root), "--input", "case_ok.md",
                "--sha256", lib.sha_file(root / "case_ok.md")]
    neg_argv = [sys.executable, "-m", "briefcheck", "--root", str(root), "--input", "case_missing.md",
                "--sha256", lib.sha_file(root / "case_missing.md")]
    entry("briefcheck_pos", lambda m: list(pos_argv), root,
          lambda e, j: e == 0 and j.get("status") == "COMPLETE"
          and j.get("provided") == ["A", "B"] and j.get("missing") == [],
          lambda j: (j.get("status"), tuple(j.get("provided") or []), tuple(j.get("missing") or [])))
    entry("briefcheck_neg", lambda m: list(neg_argv), root,
          lambda e, j: e == 2 and j.get("status") == "MISSING"
          and j.get("missing") == ["B"],
          lambda j: (j.get("status"), tuple(j.get("provided") or []), tuple(j.get("missing") or [])))

    reviewer, reviewer_resolution = resolve_reviewer()
    req = lib.PARTIES / "tpm" / "review-request.json"
    inp = lib.PARTIES / "tpm" / "input"
    reviewer_meta = {
        "resolved": None if reviewer is None else str(reviewer),
        "resolution": reviewer_resolution,
        "cache_root": str(REVIEWER_CACHE_ROOT),
        "request": str(req),
        "input_root": str(inp),
    }
    if reviewer is not None:
        reviewer_meta["plugin_version"] = reviewer.parent.parent.name
        reviewer_meta["script_sha256"] = lib.sha_file(reviewer)
    reviewer_unbound = []
    if reviewer is None:
        reviewer_unbound.append(reviewer_resolution)
    if not req.is_file():
        reviewer_unbound.append("REVIEW_REQUEST_MISSING:" + str(req))
    if not inp.is_dir():
        reviewer_unbound.append("REVIEW_INPUT_MISSING:" + str(inp))
    reviewer_positive_ok = False
    reviewer_negative_ok = False
    if reviewer_unbound:
        reviewer_meta["unbound"] = reviewer_unbound
        entries.append({
            "name": "reviewer", "kind": "positive_parity", "bound": False,
            "unbound": reviewer_unbound, "on_exit": None, "off_exit": None,
            "on_expected": False, "off_expected": False, "same_semantics": False,
            "blocked_attempts": [], "ok": False,
        })
        entries.append({
            "name": "reviewer_negative_control", "kind": "negative_control",
            "bound": False, "unbound": reviewer_unbound, "on_exit": None,
            "off_exit": None, "on_expected": False, "off_expected": False,
            "same_semantics": False, "blocked_attempts": [], "ok": False,
            "false_parity_rejected": True, "requires_reviewer_positive": True,
        })
    else:
        def review_argv(mode):
            out = lib.TMP / f"off_review_{mode}"
            out.mkdir(parents=True, exist_ok=True)
            return [sys.executable, str(reviewer), "--request", str(req),
                    "--input-root", str(inp), "--outroot", str(out)]

        pos = entry("reviewer", review_argv, lib.ROOT,
                    lambda e, j: e == 0 and j.get("state") == "REVIEW_SOURCE_LOCATED_ONLY"
                    and j.get("defects") == 0,
                    lambda j: (j.get("state"), j.get("defects"), j.get("authority_state"),
                               j.get("original_acceptance"), j.get("unbound")),
                    kind="positive_parity")
        reviewer_positive_ok = pos["ok"]

        bad_out = lib.TMP / "off_review_missing" / "absent"

        def review_neg_argv(mode):
            return [sys.executable, str(reviewer), "--request", str(req),
                    "--input-root", str(inp), "--outroot", str(bad_out)]

        neg = entry("reviewer_negative_control", review_neg_argv, lib.ROOT,
                    lambda e, j: e != 0 and (j.get("state") == "REVIEW_FAIL_CLOSED"
                                             or bool(j.get("error"))),
                    lambda j: (j.get("state"), j.get("error")),
                    kind="negative_control", false_parity_rejected=True,
                    requires_reviewer_positive=True)
        neg["ok"] = bool(neg["ok"] and reviewer_positive_ok)
        reviewer_negative_ok = bool(neg["ok"])

    def guide_argv(mode):
        return [sys.executable, str(lib.ROOT / "tools" / "guide.py"),
                "--out", str(lib.TMP / f"off_guide_{mode}.json")]

    entry("guide", guide_argv, lib.ROOT,
          lambda e, j: e == 0 and j.get("mode") == "PACKAGE_FIRST" and j.get("pack_ok") is True,
          lambda j: (j.get("mode"), j.get("pack_ok"), (j.get("delta") or {}).get("candidate_sha")))

    bridge = lib.ROOT / "tools" / "w1_bridge_reference.py"
    pkg = lib.PARTIES / "bridge" / "package"
    bridge_unbound = []
    if not bridge.is_file():
        bridge_unbound.append("BRIDGE_SCRIPT_MISSING:" + str(bridge))
    if not (pkg / "PACKAGE_FILE_MANIFEST.json").is_file():
        bridge_unbound.append("BRIDGE_PACKAGE_MANIFEST_MISSING:"
                              + str(pkg / "PACKAGE_FILE_MANIFEST.json"))
    if bridge_unbound:
        for nm in ("bridge_inspect", "bridge_explain"):
            entries.append({
                "name": nm, "kind": "positive_parity", "bound": False,
                "unbound": bridge_unbound, "on_exit": None, "off_exit": None,
                "on_expected": False, "off_expected": False, "same_semantics": False,
                "blocked_attempts": [], "ok": False,
            })
    else:
        insp = [sys.executable, str(bridge), "inspect", "--root", str(pkg),
                "--manifest", "PACKAGE_FILE_MANIFEST.json"]
        entry("bridge_inspect", lambda m: list(insp), lib.ROOT,
              lambda e, j: e == 0 and (j.get("counts") or {}).get("mismatched") == 0,
              lambda j: ((j.get("counts") or {}).get("mismatched"),
                         (j.get("counts") or {}).get("declared")),
              kind="positive_parity")
        expl = [sys.executable, str(bridge), "explain", "--pack-root", str(pkg), "--view", "all"]
        entry("bridge_explain", lambda m: list(expl), lib.ROOT,
              lambda e, j: e == 0 and len(j.get("clause_refs") or []) == len(tqaep_spec.SAMPLE),
              lambda j: tuple(sorted(c.get("case_id") for c in (j.get("clause_refs") or []))),
              kind="positive_parity")

    # Final structural guard: unmet expectations may never coexist with ok.
    for e in entries:
        if not (e.get("on_expected") is True and e.get("off_expected") is True
                and e.get("same_semantics") is True):
            e["ok"] = False

    observed = [e for e in entries if e.get("observation")]
    observer_live_all = bool(observed) and all(
        e["observation"][m]["events"] > 0 and e["observation"][m]["import_events"] > 0
        for e in observed for m in ("audit", "off"))

    off_legacy_attempts = sorted({m for e in observed
                                  for m in e["off_effect"]["legacy_import_attempts"]})
    off_child_total = sum(e["off_effect"]["child_events"] for e in observed)
    off_network_total = sum(e["off_effect"]["network_events"] for e in observed)
    off_native_total = sum(e["off_effect"]["native_events"] for e in observed)
    off_no_forbidden_import = (not off_legacy_attempts
                               and all(not e["blocked_attempts"] for e in observed))
    off_child_commands = [classify_child(c) for e in observed
                          for c in e["observation"]["off"].get("child_commands", [])]
    off_child_allowed = all(c["ok"] for c in off_child_commands)
    off_no_forbidden_effect = (off_child_allowed and off_network_total == 0
                               and off_native_total == 0)
    observer_transparent = all(e.get("same_semantics_observed") for e in observed)

    false_parity_ok = any(e.get("false_parity_rejected") for e in entries)
    unbound = sorted({u for e in entries for u in (e.get("unbound") or [])})
    reviewer_gate = reviewer_positive_ok and reviewer_negative_ok
    all_ok = bool(entries) and all(e["ok"] for e in entries)

    gates = {
        "import_control_ok": control_ok,
        "blocker_blocks_with_flag": control_blocked_ok,
        "blocker_allows_without_flag": control_audit_only_ok,
        "observer_probe_ok": probe_ok,
        "observer_absent_rejected": absent_rejected,
        "observer_live_all_runs": observer_live_all,
        "observer_transparent": observer_transparent,
        "off_no_forbidden_import": off_no_forbidden_import,
        "off_child_commands_allowed": off_child_allowed,
        "off_no_forbidden_effect": off_no_forbidden_effect,
        "reviewer_positive_ok": reviewer_positive_ok,
        "reviewer_negative_ok": reviewer_negative_ok,
        "reviewer_gate": reviewer_gate,
        "false_parity_rejected": false_parity_ok,
        "all_entries_ok": all_ok,
        "unbound": unbound,
    }
    verdict = ("PASS" if all(v for k, v in gates.items() if k != "unbound")
               and not unbound else "FAIL")

    out = {
        "schema": "FHS5.W0NF.OffLegacy@2",
        "harness_revision": "t02-nf01-audit-r1",
        "tool_sha256": lib.sha_file(Path(__file__)),
        "observation_site_sha256": lib.sha_file(SITE),
        "observation_probe_sha256": lib.sha_file(PROBE),
        "profile": str(PROFILE),
        "blocked_prefixes": list(FORBIDDEN),
        "mode_env": {m: {k: v for k, v in env(m, "TAG").items() if k.startswith("FHS5")}
                     for m in ("on", "audit", "off")},
        "control": {
            "blocked": control_blocked_ok,
            "allowed_noprofile": control_allowed_ok,
            "allowed_audit_only": control_audit_only_ok,
            "blocked_stderr": ctrl_blocked["stderr"][-300:],
            "audit_only_imports": audit_ctrl_obs["imports"],
        },
        "observer": {
            "probe_exit": probe_res["exit"],
            "probe_checks": probe_checks,
            "probe_all_ok": probe_payload.get("all_ok"),
            "probe_payload": probe_payload,
            "probe_observation": probe_obs,
            "probe_blocked_trace": probe_blocked,
            "absent_control": {
                "probe_exit": absent_res["exit"],
                "audit_exists": absent_obs["exists"],
                "checks": absent_checks,
                "rejected": absent_rejected,
            },
        },
        "reviewer": reviewer_meta,
        "gates": gates,
        "entries": entries,
        "off_totals": {
            "legacy_import_attempts": off_legacy_attempts,
            "child_events": off_child_total,
            "network_events": off_network_total,
            "native_events": off_native_total,
            "observed_pids": sorted({p for e in observed for p in e["observation"]["off"]["pids"]}),
            "opened_files": sum(e["observation"]["off"]["opens"] for e in observed),
            "child_commands": off_child_commands,
            "child_commands_allowed": off_child_allowed,
        },
        "verdict": verdict,
        "not_covered": [
            "OS-level sandboxing: the blocker is a CPython meta_path hook and the "
            "observer is a CPython audit hook; neither confines a native process",
            "native (non-Python) grandchildren and daemons are not observed",
            "Python children launched with -S/-E/-I or a scrubbed environment skip "
            "sitecustomize and are not observed",
            "kernel-level egress performed inside a native library after dlopen is "
            "not observed; only the dlopen/dlsym/call_function entry points are",
            "audit hooks observe but do not prevent; only legacy imports are blocked",
            "embedding / second interpreter with its own sys.audit state",
            "the observed native child (guide.py -> git rev-parse) is not audited "
            "internally; its argv is allowlisted as a local read-only helper",
            "different principals; Fabric/Legacy full provider set; other hosts",
        ],
    }
    lib.write_json(OUT / "off_legacy.json", out)
    print(json.dumps({
        "verdict": verdict,
        "control_ok": control_ok,
        "observer": {"probe_ok": probe_ok, "absent_rejected": absent_rejected,
                     "live_all": observer_live_all, "transparent": observer_transparent},
        "off_totals": out["off_totals"],
        "gates": {k: v for k, v in gates.items() if k not in ("unbound",)},
        "entries": [(e["name"], e["ok"]) for e in entries],
    }, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())