#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guide Touch2 with a real MaterialDelta produced by Challenge/FAR/patch."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib


def main():
    start = lib.load_json(lib.PARTIES / "guide" / "thin_start.json")
    far = lib.load_json(lib.PARTIES / "far" / "far.json")
    chall = lib.load_json(lib.PARTIES / "challenge" / "challenge_prepatch.json")
    dev = lib.load_json(lib.ROOT / "04_DEV_OPS" / "dev_patch.json")
    summary = lib.load_json(lib.TQAEP / "summary.json") if (lib.TQAEP / "summary.json").is_file() else {}
    evidence = far.get("evidence")
    delta = dict(start.get("delta") or {})
    delta.update({
        "subject_id": "FHS-5_PLP/W0",
        "source_sha": lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json"),
        "candidate_sha": lib.git("rev-parse", "HEAD"),
        "evidence_sha": evidence,
        "oracle_sha": lib.sha_file(lib.TQAEP / "oracle.json"),
        "requirement_ids": ["SAMPLE-R1", "SAMPLE-R2", "NF-R04", "NF-R07"],
        "case_ids": ["F5-W0-T14", "NF-T09", "NF-T08"],
        "findings": [chall["finding"]["id"]],
        "next_action": "re-run affected cone on candidate v3 with the frozen oracle",
        "retest_evidence_sha": summary.get("receipts_index_sha"),
        "not_covered": ["W1-W4 denominators", "other hosts"],
    })
    out = {
        "schema": "FHS5.W0NF.GuideThinResume@2",
        "state": "RESUME",
        "mode": start.get("mode", "PACKAGE_FIRST"),
        "delta": delta,
        "material_delta": {
            "finding_id": chall["finding"]["id"],
            "far_chosen": far.get("chosen"),
            "candidate_from": dev["preimage"]["head"],
            "candidate_to": lib.git("rev-parse", "HEAD"),
            "patch_sha256": dev["patch"]["sha256"],
            "retest_ref": "04_DEV_OPS/raw/green_v3.stderr.txt",
        },
        "resume_prompt": ("Continue W0/N-T08 from the frozen pack and the MaterialDelta: "
                          "FAR finding -> 12' patch -> affected retest. Do not widen scope."),
        "next_action": "affected retest + independent challenge",
    }
    lib.write_json(lib.PARTIES / "guide" / "thin_resume.json", out)
    print(json.dumps({"state": out["state"], "finding": delta["findings"],
                      "evidence": evidence, "candidate": delta["candidate_sha"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
