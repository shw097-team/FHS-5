#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D1: real legacy-provider OFF. A sitecustomize import blocker makes
HGK/FABRIC/SBL/FHS/PIPD/HERMES unimportable in the subprocess, then B0
representative entries must still work. Positive and negative controls."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import tqaep_spec

OUT = lib.ROOT / "04_DEV_OPS"
PROFILE = OUT / "off_profile"
LEGACY = OUT / "off_legacy_src"
TRACE = lib.TMP / "off_trace.jsonl"

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

    def entry(name, argv_on, argv_off, cwd, expect, semantics):
        TRACE.write_text("", encoding="utf-8")
        on = lib.run(argv_on, cwd, env_extra=env(False), raw_dir=raw, tag=f"off_{name}_on")
        TRACE.write_text("", encoding="utf-8")
        off = lib.run(argv_off, cwd, env_extra=env(True), raw_dir=raw, tag=f"off_{name}_off")
        blocked = blocked_lines()
        onj, offj = payload(on), payload(off)
        on_ok = expect(on["exit"], onj)
        off_ok = expect(off["exit"], offj)
        same = semantics(onj) == semantics(offj)
        ok = on_ok and off_ok and same and not blocked
        entries.append({
            "name": name, "on_exit": on["exit"], "off_exit": off["exit"],
            "on_expected": on_ok, "off_expected": off_ok, "same_semantics": same,
            "blocked_attempts": blocked, "ok": ok,
        })

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

    reviewer = Path(r"C:\Users\user\.codex\plugins\cache\created-by-me-remote\plp-tpm-review\1.0.1\scripts\review_core.py")
    req = lib.PARTIES / "tpm" / "review-request.json"
    inp = lib.PARTIES / "tpm" / "input"
    if reviewer.is_file() and req.is_file():
        on_out = lib.TMP / "off_review_on"
        off_out = lib.TMP / "off_review_off"
        on_out.mkdir(parents=True, exist_ok=True)
        off_out.mkdir(parents=True, exist_ok=True)
        entry("reviewer",
              [sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
               "--outroot", str(on_out)],
              [sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
               "--outroot", str(off_out)],
              lib.ROOT,
              lambda e, j: e == 0 and j.get("state") == "REVIEW_SOURCE_LOCATED_ONLY"
              and j.get("defects") == 0,
              lambda j: (j.get("state"), j.get("defects"), j.get("authority_state"),
                         j.get("original_acceptance")))
        bad_out = lib.TMP / "off_review_missing" / "absent"
        neg = lib.run([sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
                       "--outroot", str(bad_out)], lib.ROOT, env_extra=env(True),
                      raw_dir=raw, tag="off_reviewer_double_fail")
        neg_parity = (neg["exit"] == 0 and payload(neg).get("state") == "REVIEW_SOURCE_LOCATED_ONLY")
        entries.append({
            "name": "reviewer_double_fail_negative",
            "on_exit": neg["exit"], "off_exit": neg["exit"],
            "on_expected": False, "off_expected": False, "same_semantics": True,
            "blocked_attempts": [], "ok": True,
            "false_parity_rejected": neg_parity is False,
            "observed": payload(neg).get("error", "")[:120],
        })

    guide_argv = [sys.executable, str(lib.ROOT / "tools" / "guide.py"),
                  "--out", str(lib.TMP / "off_guide.json")]
    entry("guide", guide_argv, guide_argv, lib.ROOT,
          lambda e, j: e == 0 and j.get("mode") == "PACKAGE_FIRST" and j.get("pack_ok") is True,
          lambda j: (j.get("mode"), j.get("pack_ok"), (j.get("delta") or {}).get("candidate_sha")))

    bridge = lib.ROOT / "tools" / "w1_bridge_reference.py"
    pkg = lib.PARTIES / "bridge" / "package"
    if pkg.is_dir():
        insp = [sys.executable, str(bridge), "inspect", "--root", str(pkg),
                "--manifest", "PACKAGE_FILE_MANIFEST.json"]
        entry("bridge_inspect", insp, insp, lib.ROOT,
              lambda e, j: e == 0 and (j.get("counts") or {}).get("mismatched") == 0,
              lambda j: ((j.get("counts") or {}).get("mismatched"),
                         (j.get("counts") or {}).get("declared")))
        expl = [sys.executable, str(bridge), "explain", "--pack-root", str(pkg), "--view", "all"]
        entry("bridge_explain", expl, expl, lib.ROOT,
              lambda e, j: e == 0 and len(j.get("clause_refs") or []) == len(tqaep_spec.SAMPLE),
              lambda j: tuple(sorted(c.get("case_id") for c in (j.get("clause_refs") or []))))

    false_parity_ok = any(e.get("false_parity_rejected") for e in entries)
    verdict = ("PASS" if control_ok and entries and false_parity_ok
               and all(e["ok"] for e in entries) else "FAIL")
    out = {
        "schema": "FHS5.W0NF.OffLegacy@1",
        "profile": str(PROFILE),
        "blocked_prefixes": ["hgk", "fabric", "sbl", "fhs", "pipd", "hermes"],
        "control": {"blocked": ctrl_blocked["exit"] != 0, "allowed": ctrl_allowed["exit"] == 0,
                    "blocked_stderr": ctrl_blocked["stderr"][-300:]},
        "entries": entries,
        "verdict": verdict,
        "not_covered": ["Fabric/Legacy full provider set", "other hosts"],
    }
    lib.write_json(OUT / "off_legacy.json", out)
    print(json.dumps({"verdict": verdict, "control_ok": control_ok,
                      "entries": [(e["name"], e["ok"]) for e in entries]},
                     ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
