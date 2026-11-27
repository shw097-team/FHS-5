#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D2: Bridge OFF. A native reader consumes the pack/oracle directly while
w1_bridge_reference is import-blocked; compare facts with Bridge ON."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.ROOT / "04_DEV_OPS"
PROFILE = OUT / "off_bridge_profile"
TRACE = lib.TMP / "off_bridge_trace.jsonl"

SITECUSTOMIZE = '''import os, sys, json
class _B:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] == "w1_bridge_reference":
            try:
                with open(os.environ["FHS5_TRACE"], "a", encoding="utf-8") as f:
                    f.write(json.dumps({"blocked": fullname}) + "\\n")
            except Exception:
                pass
            raise ImportError("FHS5_BRIDGE_BLOCKED:" + fullname)
        return None
sys.meta_path.insert(0, _B())
'''


def native_facts() -> dict:
    man = lib.load_json(lib.PACK / "05_W0_SOURCE_MANIFEST.json")
    oracle = lib.load_json(lib.TQAEP / "oracle.json")
    return {
        "pack_manifest_sha256": lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json"),
        "identity": {k: man.get(k) for k in ("project_id", "wave_id", "batch_id", "pack_version")},
        "files": {e["path"]: lib.sha_file(lib.PACK / e["path"]) for e in man["pack_files"]},
        "cases": sorted(oracle["cases"].keys()),
        "fixtures": {k: v for k, v in oracle["fixtures"].items()},
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROFILE.mkdir(exist_ok=True)
    (PROFILE / "sitecustomize.py").write_text(SITECUSTOMIZE, encoding="utf-8")
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    TRACE.write_text("", encoding="utf-8")
    raw = OUT / "raw"

    # direct read under blocked Bridge
    code = ("import sys,json; sys.path.insert(0,r'%s'); import off_bridge; "
            "print(json.dumps(off_bridge.native_facts(),ensure_ascii=False,sort_keys=True))"
            % str(lib.ROOT / "tools"))
    env = {"PYTHONPATH": os.pathsep.join([str(PROFILE), str(lib.ROOT / "tools")]),
           "FHS5_TRACE": str(TRACE), "PYTHONDONTWRITEBYTECODE": "1"}
    direct = lib.run([sys.executable, "-c", code], lib.ROOT, env_extra=env, raw_dir=raw,
                     tag="off_bridge_direct")
    blocked = []
    if TRACE.is_file():
        blocked = [json.loads(x) for x in TRACE.read_text(encoding="utf-8").splitlines() if x.strip()]

    # positive control: direct import of bridge is blocked
    TRACE.write_text("", encoding="utf-8")
    ctrl = lib.run([sys.executable, "-c", "import w1_bridge_reference; print('BRIDGE_IMPORTED')"],
                   lib.ROOT, env_extra=env, raw_dir=raw, tag="off_bridge_control")

    # Bridge ON facts
    bridge = lib.ROOT / "tools" / "w1_bridge_reference.py"
    pkg = lib.PARTIES / "bridge" / "package"
    on = lib.run([sys.executable, str(bridge), "explain", "--pack-root", str(pkg), "--view", "all"],
                 lib.ROOT, env_extra={"PYTHONPATH": str(lib.ROOT / "tools")},
                 raw_dir=raw, tag="off_bridge_on")
    expl = json.loads(on["stdout"]) if on["exit"] == 0 else {}

    direct_facts = json.loads(direct["stdout"]) if direct["exit"] == 0 else {}
    bridge_cases = sorted({c["case_id"] for c in expl.get("clause_refs") or []})
    bridge_fixtures = {c["case_id"]: c["source"]["sha256"] for c in expl.get("clause_refs") or []}
    # bridge fixture hashes are in verification_refs; use case ids + pack sha instead
    same = (direct_facts.get("pack_manifest_sha256") ==
            lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json")
            and set(bridge_cases) == {f"SAMPLE-{k}" for k in direct_facts.get("cases", [])})
    parity = {
        "pack_sha_equal": direct_facts.get("pack_manifest_sha256") ==
                          lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json"),
        "bridge_case_count": len(bridge_cases),
        "native_case_count": len(direct_facts.get("cases", [])),
        "same_case_set": set(bridge_cases) == {f"SAMPLE-{k}" for k in direct_facts.get("cases", [])},
    }
    verdict = "PASS" if (direct["exit"] == 0 and not blocked and ctrl["exit"] != 0
                         and "FHS5_BRIDGE_BLOCKED" in ctrl["stderr"] and same
                         and parity["same_case_set"]) else "FAIL"
    out = {
        "schema": "FHS5.W0NF.OffBridge@1",
        "direct_exit": direct["exit"], "direct_facts": direct_facts,
        "bridge_exit": on["exit"], "bridge_cases": bridge_cases,
        "bridge_imports_blocked": blocked,
        "control": {"exit": ctrl["exit"], "blocked": "FHS5_BRIDGE_BLOCKED" in ctrl["stderr"]},
        "parity": parity,
        "verdict": verdict,
        "not_covered": ["Bridge 38+28 full denominator", "Host install/register/invoke"],
    }
    lib.write_json(OUT / "off_bridge.json", out)
    print(json.dumps({"verdict": verdict, "direct_exit": direct["exit"],
                      "parity": parity, "blocked": blocked}, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
