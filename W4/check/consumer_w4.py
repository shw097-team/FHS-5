#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fresh W4 inbound consumer: parse W4_INBOUND.json and choose next action."""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "W3", "impl")))

from w3_common import load_json_strict, sha256_file

REQUIRED = [
    "from_stage", "to_stage", "handoff_id", "project_id", "work_id",
    "pack_ref", "pack_manifest_sha256", "candidate_commit", "candidate_preimage",
    "oracle_sha256", "case_set_sha256", "evidence_ref", "evidence_manifest_sha256",
    "checker_ref", "consumer_ref", "actual_readback", "next_legal_action",
    "dependencies", "resume_predicate", "not_covered", "readiness", "publication_state",
]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbound", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    d = load_json_strict(a.inbound)
    errors = [k for k in REQUIRED if k not in d]
    if d.get("from_stage") != "W3" or d.get("to_stage") != "W4":
        errors.append("stage")
    if not d.get("not_covered"):
        errors.append("not_covered_empty")
    if d.get("readiness", {}).get("W4_TECHNICALLY_READY") is not False:
        errors.append("overclaim")
    if d.get("readiness", {}).get("W4_EXECUTION_READY") is not False:
        errors.append("overclaim_exec")
    next_action = "READ_ONLY_W4_PREP"
    if "CASE_OWNER_FREEZE_MISSING" in json.dumps(d, ensure_ascii=False):
        next_action = "CASE_OWNER_FREEZE"
    out = {
        "schema": "FHS5.PLP.W4.InboundConsumerReceipt@1",
        "consumer_role": "FRESH_W4_CONSUMER",
        "consumer_script_sha256": sha256_file(os.path.abspath(__file__)),
        "argv": [sys.executable, os.path.abspath(__file__)] + (argv or []),
        "cwd": os.getcwd(),
        "inbound": {"path": a.inbound, "sha256": sha256_file(a.inbound)},
        "cli_executed": True,
        "input_writes": 0,
        "missing_fields": errors,
        "next_action": next_action,
        "verdict": "PASS" if not errors else "FAIL",
        "strength": "FRESH_LOCAL_PROCESS_PARSE_AND_USE; NOT_ORIGINAL_DOMAIN_CONSUMER",
        "limitations": ["same OS principal as the producer",
                        "W4 named execution authority not present"],
    }
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": out["verdict"], "next_action": next_action,
                      "errors": errors}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
