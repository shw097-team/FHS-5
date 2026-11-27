#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D1: real legacy-provider OFF. A sitecustomize import blocker makes
HGK/FABRIC/SBL/FHS/PIPD/HERMES unimportable in the subprocess, then B0
representative entries must still work. Positive and negative controls."""
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
    """Resolve the installed PLP reviewer script; never install or upgrade.

    Prefers the pinned 1.0.1 cache entry, otherwise the newest version that is
    actually present on this host. FHS5_REVIEWER_CACHE only narrows the search
    root (used by fail-closed negative controls); it can never add a reviewer.
    """
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

SITECUSTOMIZE = '''import os, sys, json
_BLOCK = ("hgk", "fabric", "sbl", "fhs", "pipd", "hermes")
class _Blocker:
    def find_spec(self, fullname, path=None, target=None):
        top = fullname.split(".")[0].lower()
        if any(top.startswith(b) for b in _BLOCK):
            try:
                with open(os.environ["FHS5_TRACE"], "a", encoding="utf-8") as f:
                    f.write(json.dumps({"blocked": fullname}) + "\\n")
            except Exception:
                pass
            raise ImportError("FHS5_LEGACY_BLOCKED:" + fullname)
        return None
sys.meta_path.insert(0, _Blocker())
'''


def env(profile: bool, trace: bool = True) -> dict:
    parts = ([str(PROFILE)] if profile else []) + [str(lib.REPO), str(lib.ROOT / "tools")]
    e = {"PYTHONPATH": os.pathsep.join(parts), "PYTHONDONTWRITEBYTECODE": "1",
         "PYTHONIOENCODING": "utf-8"}
    if trace:
        e["FHS5_TRACE"] = str(TRACE)
    return e


def blocked_lines() -> list[dict]:
    if not TRACE.is_file():
        return []
    return [json.loads(x) for x in TRACE.read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROFILE.mkdir(exist_ok=True)
    LEGACY.mkdir(exist_ok=True)
    (PROFILE / "sitecustomize.py").write_text(SITECUSTOMIZE, encoding="utf-8")
    (LEGACY / "hgk_core.py").write_text("VALUE = 1\n", encoding="utf-8")
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    TRACE.write_text("", encoding="utf-8")
    raw = OUT / "raw"

    # negative control: import must be blocked under the profile
    ctrl_blocked = lib.run([sys.executable, "-c", "import hgk_core; print('IMPORTED')"], lib.ROOT,
                           env_extra=dict(env(True), FHS5_TRACE=str(TRACE),
                                          PYTHONPATH=os.pathsep.join([str(PROFILE), str(LEGACY)])),
                           raw_dir=raw, tag="off_control_blocked")
    # positive control without profile: import must succeed
    ctrl_allowed = lib.run([sys.executable, "-c", "import hgk_core; print('IMPORTED')"], lib.ROOT,
                           env_extra={"PYTHONPATH": str(LEGACY),
                                      "PYTHONDONTWRITEBYTECODE": "1"},
                           raw_dir=raw, tag="off_control_allowed")
    control_ok = (ctrl_blocked["exit"] != 0 and "FHS5_LEGACY_BLOCKED" in ctrl_blocked["stderr"]
                  and ctrl_allowed["exit"] == 0 and "IMPORTED" in ctrl_allowed["stdout"])

    entries = []

    def payload(r):
        try:
            return json.loads(r["stdout"])
        except Exception:
            return {}

    def entry(name, argv_on, argv_off, cwd, expect, semantics, **extra):
        TRACE.write_text("", encoding="utf-8")
        on = lib.run(argv_on, cwd, env_extra=env(False), raw_dir=raw, tag=f"off_{name}_on")
        TRACE.write_text("", encoding="utf-8")
        off = lib.run(argv_off, cwd, env_extra=env(True), raw_dir=raw, tag=f"off_{name}_off")
        blocked = blocked_lines()
        onj, offj = payload(on), payload(off)
        on_ok = bool(expect(on["exit"], onj))
        off_ok = bool(expect(off["exit"], offj))
        same = semantics(onj) == semantics(offj)
        # Structural invariant: if either side misses its expectation this entry
        # can never be ok. A double-fail is a defect, not parity.
        ok = on_ok and off_ok and same and not blocked
        rec = {
            "name": name, "on_exit": on["exit"], "off_exit": off["exit"],
            "on_expected": on_ok, "off_expected": off_ok, "same_semantics": same,
            "blocked_attempts": blocked, "ok": ok,
            "on_semantics": semantics(onj), "off_semantics": semantics(offj),
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
    entry("briefcheck_pos", pos_argv, pos_argv, root,
          lambda e, j: e == 0 and j.get("status") == "COMPLETE"
          and j.get("provided") == ["A", "B"] and j.get("missing") == [],
          lambda j: (j.get("status"), tuple(j.get("provided") or []), tuple(j.get("missing") or [])))
    entry("briefcheck_neg", neg_argv, neg_argv, root,
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
        on_out = lib.TMP / "off_review_on"
        off_out = lib.TMP / "off_review_off"
        on_out.mkdir(parents=True, exist_ok=True)
        off_out.mkdir(parents=True, exist_ok=True)
        pos = entry("reviewer",
                    [sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
                     "--outroot", str(on_out)],
                    [sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
                     "--outroot", str(off_out)],
                    lib.ROOT,
                    lambda e, j: e == 0 and j.get("state") == "REVIEW_SOURCE_LOCATED_ONLY"
                    and j.get("defects") == 0,
                    lambda j: (j.get("state"), j.get("defects"), j.get("authority_state"),
                               j.get("original_acceptance"), j.get("unbound")),
                    kind="positive_parity")
        reviewer_positive_ok = pos["ok"]

        # Mandatory negative control: the reviewer must fail closed on a
        # non-existent output root with a typed error under BOTH ON and OFF.
        # Both sides failing is never accepted as parity.
        bad_out = lib.TMP / "off_review_missing" / "absent"
        neg = entry("reviewer_negative_control",
                    [sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
                     "--outroot", str(bad_out)],
                    [sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
                     "--outroot", str(bad_out)],
                    lib.ROOT,
                    lambda e, j: e != 0 and (j.get("state") == "REVIEW_FAIL_CLOSED"
                                             or bool(j.get("error"))),
                    lambda j: (j.get("state"), j.get("error")),
                    kind="negative_control", false_parity_rejected=True,
                    requires_reviewer_positive=True)
        neg["ok"] = bool(neg["ok"] and reviewer_positive_ok)
        reviewer_negative_ok = bool(neg["ok"])

    guide_argv = [sys.executable, str(lib.ROOT / "tools" / "guide.py"),
                  "--out", str(lib.TMP / "off_guide.json")]
    entry("guide", guide_argv, guide_argv, lib.ROOT,
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
        entry("bridge_inspect", insp, insp, lib.ROOT,
              lambda e, j: e == 0 and (j.get("counts") or {}).get("mismatched") == 0,
              lambda j: ((j.get("counts") or {}).get("mismatched"),
                         (j.get("counts") or {}).get("declared")),
              kind="positive_parity")
        expl = [sys.executable, str(bridge), "explain", "--pack-root", str(pkg), "--view", "all"]
        entry("bridge_explain", expl, expl, lib.ROOT,
              lambda e, j: e == 0 and len(j.get("clause_refs") or []) == len(tqaep_spec.SAMPLE),
              lambda j: tuple(sorted(c.get("case_id") for c in (j.get("clause_refs") or []))),
              kind="positive_parity")

    # Final structural guard: unmet expectations may never coexist with ok.
    for e in entries:
        if not (e.get("on_expected") is True and e.get("off_expected") is True
                and e.get("same_semantics") is True):
            e["ok"] = False

    false_parity_ok = any(e.get("false_parity_rejected") for e in entries)
    unbound = sorted({u for e in entries for u in (e.get("unbound") or [])})
    reviewer_gate = reviewer_positive_ok and reviewer_negative_ok
    all_ok = bool(entries) and all(e["ok"] for e in entries)
    verdict = ("PASS" if control_ok and reviewer_gate and false_parity_ok
               and all_ok and not unbound else "FAIL")
    out = {
        "schema": "FHS5.W0NF.OffLegacy@1",
        "harness_revision": "t01-nf01-r1",
        "tool_sha256": lib.sha_file(Path(__file__)),
        "profile": str(PROFILE),
        "blocked_prefixes": ["hgk", "fabric", "sbl", "fhs", "pipd", "hermes"],
        "control": {"blocked": ctrl_blocked["exit"] != 0, "allowed": ctrl_allowed["exit"] == 0,
                    "blocked_stderr": ctrl_blocked["stderr"][-300:]},
        "reviewer": reviewer_meta,
        "gates": {
            "import_control_ok": control_ok,
            "reviewer_positive_ok": reviewer_positive_ok,
            "reviewer_negative_ok": reviewer_negative_ok,
            "reviewer_gate": reviewer_gate,
            "false_parity_rejected": false_parity_ok,
            "all_entries_ok": all_ok,
            "unbound": unbound,
        },
        "entries": entries,
        "verdict": verdict,
        "not_covered": [
            "Fabric/Legacy full provider set",
            "other hosts",
            "OS-level process/mount isolation: only a PYTHONPATH sitecustomize "
            "import blocker is used",
            "network egress: python-level import observation only, no syscall/network tracing",
            "grandchild processes that scrub PYTHONPATH are not observed",
        ],
    }
    lib.write_json(OUT / "off_legacy.json", out)
    print(json.dumps({"verdict": verdict, "control_ok": control_ok,
                      "gates": out["gates"],
                      "entries": [(e["name"], e["ok"]) for e in entries]},
                     ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
