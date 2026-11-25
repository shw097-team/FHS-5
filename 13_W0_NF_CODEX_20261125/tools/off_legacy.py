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

    def entry(name, argv, cwd, sha_flag):
        TRACE.write_text("", encoding="utf-8")
        on = lib.run(argv, cwd, env_extra=env(False), raw_dir=raw, tag=f"off_{name}_on")
        TRACE.write_text("", encoding="utf-8")
        off = lib.run(argv, cwd, env_extra=env(True), raw_dir=raw, tag=f"off_{name}_off")
        blocked = blocked_lines()
        entries.append({
            "name": name, "on_exit": on["exit"], "off_exit": off["exit"],
            "same_exit": on["exit"] == off["exit"],
            "same_sha": on[sha_flag] == off[sha_flag],
            "blocked_attempts": blocked,
            "ok": on["exit"] == off["exit"] and on[sha_flag] == off[sha_flag] and not blocked,
        })

    root = lib.TQAEP / "tmp" / "root"
    if not (root / "case_ok.md").is_file():
        root.mkdir(parents=True, exist_ok=True)
        for p in (lib.REPO / "fixtures").glob("*.md"):
            import shutil as _sh
            _sh.copy2(p, root / p.name)

    entry("briefcheck_pos",
          [sys.executable, "-m", "briefcheck", "--root", str(root), "--input", "case_ok.md",
           "--sha256", lib.sha_file(root / "case_ok.md")], root, "stdout_sha256")
    entry("briefcheck_neg",
          [sys.executable, "-m", "briefcheck", "--root", str(root), "--input", "case_missing.md",
           "--sha256", lib.sha_file(root / "case_missing.md")], root, "stdout_sha256")

    reviewer = Path(r"C:\Users\user\.codex\plugins\cache\created-by-me-remote\plp-tpm-review\1.0.1\scripts\review_core.py")
    req = lib.PARTIES / "tpm" / "review-request.json"
    inp = lib.PARTIES / "tpm" / "input"
    if reviewer.is_file() and req.is_file():
        tmp_review = lib.TMP / "off_review"
        entry("reviewer",
              [sys.executable, str(reviewer), "--request", str(req), "--input-root", str(inp),
               "--outroot", str(tmp_review)], lib.ROOT, "stdout_sha256")

    entry("guide", [sys.executable, str(lib.ROOT / "tools" / "guide.py"),
                    "--out", str(lib.TMP / "off_guide.json")], lib.ROOT, "stdout_sha256")

    bridge = lib.ROOT / "tools" / "w1_bridge_reference.py"
    pkg = lib.PARTIES / "bridge" / "package"
    if pkg.is_dir():
        entry("bridge_inspect",
              [sys.executable, str(bridge), "inspect", "--root", str(pkg),
               "--manifest", "PACKAGE_FILE_MANIFEST.json"], lib.ROOT, "stdout_sha256")
        entry("bridge_explain",
              [sys.executable, str(bridge), "explain", "--pack-root", str(pkg), "--view", "all"],
              lib.ROOT, "stdout_sha256")

    verdict = "PASS" if control_ok and entries and all(e["ok"] for e in entries) else "FAIL"
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
