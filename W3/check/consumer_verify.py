#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fresh Consumer: parse/use the W3 closeout and handoff, choose next action.

Writes only its own receipt. A digest exchange is not consumption.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

from w3_common import load_json_strict, sha256_file


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    cl = os.path.join(a.root, "FHS-5_PLP_W3_CLOSEOUT.md")
    hd = os.path.join(a.root, "FHS-5_PLP_W3_HANDOFF.md")
    cur = os.path.join(a.root, "W3_PRODUCT_CURRENT.json")
    errors = []
    for p in (cl, hd, cur):
        if not os.path.isfile(p):
            errors.append("missing:" + os.path.basename(p))
    text_cl = open(cl, encoding="utf-8").read() if os.path.isfile(cl) else ""
    text_hd = open(hd, encoding="utf-8").read() if os.path.isfile(hd) else ""
    required_cl = ["W3_NF_VALIDATED", "NOT_COVERED", "下一合法動作", "TEST_MUTANT_FINDING"]
    required_hd = ["from_stage", "to_stage", "pack_manifest_sha256", "W4_TECHNICALLY_READY",
                   "NotCovered", "next legal action"]
    for token in required_cl:
        if token not in text_cl:
            errors.append("closeout_token:" + token)
    for token in required_hd:
        if token not in text_hd:
            errors.append("handoff_token:" + token)
    product = load_json_strict(cur) if os.path.isfile(cur) else {}
    if product.get("claims", {}).get("W3_NF_VALIDATED") is not False:
        errors.append("product_current_overclaims_validation")
    next_action = None
    if "CASE_OWNER_FREEZE_MISSING" in text_hd:
        next_action = "CASE_OWNER_FREEZE"
    elif "W2_WRITER_BLOCKED" in text_hd:
        next_action = "W2_OWNER_DECISION"
    else:
        next_action = "READ_ONLY_REVIEW"
    out = {
        "schema": "FHS5.PLP.W3.ConsumerReceipt@1",
        "consumer_role": "FRESH_CONSUMER",
        "consumer_script_sha256": sha256_file(os.path.abspath(__file__)),
        "argv": [sys.executable, os.path.abspath(__file__)] + (argv or []),
        "cwd": os.getcwd(),
        "run_id": a.run_id,
        "cli_executed": True,
        "input_writes": 0,
        "consumed": {
            "closeout": {"path": cl, "sha256": sha256_file(cl) if os.path.isfile(cl) else None},
            "handoff": {"path": hd, "sha256": sha256_file(hd) if os.path.isfile(hd) else None},
            "product_current": {"path": cur, "sha256": sha256_file(cur) if os.path.isfile(cur) else None},
        },
        "parsed_sections": {"closeout_tokens": required_cl, "handoff_tokens": required_hd},
        "next_action": next_action,
        "verdict": "PASS" if not errors else "FAIL",
        "errors": errors,
        "strength": "FRESH_LOCAL_PROCESS_PARSE_AND_USE; NOT_ORIGINAL_DOMAIN_CONSUMER",
        "limitations": ["same OS principal as the maker",
                        "consumes design-layer closeout, not product-validated evidence"],
    }
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"verdict": out["verdict"], "next_action": next_action,
                      "errors": errors, "consumer_sha256": out["consumer_script_sha256"]},
                     ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
