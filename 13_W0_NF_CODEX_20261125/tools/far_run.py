#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAR reference: real Finding from the red run, RQ0-RQ8, >=2 alternatives,
ten advice fields, seven keys, and fail-closed close behavior."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import policy

OUT = lib.PARTIES / "far"
RAW = OUT / "raw"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    dp = lib.load_json(lib.ROOT / "04_DEV_OPS" / "dev_patch.json")
    prepatch_path = lib.PARTIES / "challenge" / "challenge_prepatch.json"
    prepatch = lib.load_json(prepatch_path) if prepatch_path.is_file() else None
    raw_dir = lib.ROOT / "04_DEV_OPS" / "raw"
    raw_stdout = lib.sha_file(raw_dir / "red_v2.stdout.txt")
    raw_stderr = lib.sha_file(raw_dir / "red_v2.stderr.txt")
    raw_sha = raw_stderr
    dev_finding = {
        "id": "F-W0NF-001",
        "severity": "MAJOR",
        "class": "fail_open_invalid_root",
        "subject_sha": dp["preimage"]["head"],
        "command": "python -m unittest discover -s 04_DEV_OPS/probe -v",
        "exit": dp["red"]["exit"],
        "raw_sha256": raw_sha,
        "raw_streams": {"stdout_sha256": raw_stdout, "stderr_sha256": raw_stderr,
                        "stderr": "04_DEV_OPS/raw/red_v2.stderr.txt"},
        "reproduction": ("BRIEFCHECK_REPO=<candidate> python -m unittest discover -s 04_DEV_OPS/probe -v; "
                         "briefcheck --root <missing dir> raises FileNotFoundError and exits 1 instead of "
                         "INVALID_PATH/3"),
    }
    if prepatch and prepatch.get("verdict") == "FINDING_CONFIRMED":
        finding = dict(prepatch["finding"])
        finding["source"] = "CHALLENGE_PREPATCH"
        finding["dev_finding_id"] = dev_finding["id"]
        finding["raw_sha256"] = prepatch["finding"]["raw_sha256"]
    else:
        finding = dict(dev_finding)
        finding["source"] = "DEV_RED"
    alternatives = [
        {"id": "ALT-1", "name": "wrap root resolve in try/except OSError and require is_dir",
         "cost": "low", "risk": "low", "chosen": True,
         "reason": "minimal, local, keeps exit contract, no new dependency"},
        {"id": "ALT-2", "name": "pre-validate with os.path.isdir before resolve",
         "cost": "low", "risk": "medium",
         "reason": "TOCTOU window and still needs exception handling for races"},
        {"id": "ALT-3", "name": "catch all exceptions at top level and emit INVALID_FORMAT",
         "cost": "low", "risk": "high", "chosen": False,
         "reason": "masks programming errors and mislabels invalid paths"},
    ]
    rq = {
        "RQ0": {"question": "raw command/exit/reproduction?", "answer": "yes", "evidence": raw_sha},
        "RQ1": {"question": "reproduced on frozen candidate?", "answer": "yes", "candidate": dp["preimage"]["head"]},
        "RQ2": {"question": "root cause localized?", "answer": "uncaught Path.resolve(strict=True)"},
        "RQ3": {"question": "affected cone?",
                "answer": ["briefcheck.py:main", "R11 missing-root test"],
                "note": "R12 (root is a file) already returned INVALID_PATH pre-patch; not affected"},
        "RQ4": {"question": "external source needed?", "answer": "no"},
        "RQ5": {"question": "at least two alternatives?", "answer": 3},
        "RQ6": {"question": "security impact?", "answer": "traceback discloses absolute paths; fail-open exit code"},
        "RQ7": {"question": "compatibility?", "answer": "no schema change; existing statuses preserved"},
        "RQ8": {"question": "next?", "answer": "12' patch + affected retest"},
    }
    advice = {
        "root_cause": "Path(a.root).resolve(strict=True) is called before any guard; missing root raises OSError",
        "reproduce": finding["reproduction"],
        "minimal_patch": "try/except OSError around resolve; require root.is_dir()",
        "test": "R11 missing root; R12 root is a file; full suite",
        "security": "fail closed with INVALID_PATH; no path disclosure in stdout/stderr",
        "compat": "unchanged JSON schema and exit codes",
        "docs": "requirements NEG already lists absolute/dotdot; add invalid-root note in candidate README",
        "rollback": f"git -C 02_CANDIDATE/repo reset --hard {dp['preimage']['head']} (DEV only)",
        "monitor": "affected cone only: R11/R12 + full suite",
        "next": "12' candidate v3; challenge re-runs POS/NEG/security",
    }
    evidence_sha = finding["raw_sha256"] if finding.get("source") == "CHALLENGE_PREPATCH" else raw_sha
    far = {
        "schema": "FHS5.W0NF.FAR@2",
        "claim_ceiling": "BUILD_MINIMAL_FAR_REFERENCE",
        "finding": finding,
        "challenge_ref": "03_PARTIES/challenge/challenge_prepatch.json"
        if prepatch and prepatch.get("verdict") == "FINDING_CONFIRMED" else None,
        "rq": rq,
        "alternatives": alternatives,
        "chosen": "ALT-1",
        "advice": advice,
        "keys": ["finding_id", "root_cause", "alternatives", "chosen", "risk", "next", "evidence"],
        "risk": "medium before patch (wrong exit + path leak); low after fail-closed patch",
        "next": "12' patch (candidate v3) + affected retest",
        "evidence": evidence_sha,
        "source_status": {"status": "HIT_LOCAL", "zero_results": False,
                          "unavailable_behavior": policy.far_source_status(False, None)},
        "close_policy": {
            "no_raw": policy.far_close(None, True),
            "with_raw_in_scope": policy.far_close(raw_sha, True),
            "out_of_scope": policy.far_close(raw_sha, False),
        },
        "not_covered": ["Fabric three-source profile", "FAR-T20/FARP30/local35 denominators"],
    }
    lib.write_json(OUT / "finding.json", finding)
    lib.write_json(OUT / "far.json", far)
    lib.write_json(OUT / "raw" / "far_negative_probes.json", far["close_policy"])
    print(json.dumps({"finding": finding["id"], "raw_sha": raw_sha, "alternatives": len(alternatives),
                      "chosen": far["chosen"], "close_no_raw": far["close_policy"]["no_raw"]["status"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
