#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Distinct read-only checker for the W2 12-case read-only requalification."""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "W3", "impl")))

from w3_common import load_json_strict, sha256_file


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    ev = os.path.join(a.root, "evidence", a.run_id)
    matrix = load_json_strict(os.path.join(ev, "W2_REQUALIFICATION_MATRIX.json"))
    errors = []
    for row in matrix["rows"]:
        p = os.path.join(ev, "cases", row["case_id"], "record.json")
        if not os.path.isfile(p):
            errors.append("missing:" + row["case_id"])
            continue
        rec = load_json_strict(p)
        if rec["verdict"] != "PASS":
            errors.append("verdict:" + row["case_id"])
        if rec["raw_sha256"] != row["raw_sha256"]:
            errors.append("raw:" + row["case_id"])
        expected = rec["expected_tokens"]
        if rec["kind"] == "POS":
            if not all(t in rec["observed_tokens"] for t in expected):
                errors.append("tokens:" + row["case_id"])
        else:
            if not set(rec["observed_tokens"]) & set(expected):
                errors.append("tokens:" + row["case_id"])
    if matrix["row_count"] != 12:
        errors.append("row_count")
    out = {
        "schema": "FHS5.PLP.W2.RequalCheckerReceipt@1",
        "checker_role": "DISTINCT_READ_ONLY_CHECKER",
        "checker_script_sha256": sha256_file(os.path.abspath(__file__)),
        "argv": [sys.executable, os.path.abspath(__file__)] + (argv or []),
        "cwd": os.getcwd(),
        "run_id": a.run_id,
        "rows_checked": matrix["row_count"],
        "errors": errors,
        "verdict": "PASS" if not errors else "FAIL",
        "strength": "DISTINCT_LOCAL_PROCESS_READONLY; NOT_ORIGINAL_DOMAIN_PRINCIPAL",
        "limitations": [
            "same OS principal as the executor",
            "W2 protected writer/gate/marker untouched and still blocked",
            "read-only requalification of the published 12 cases, not a W2 product write",
        ],
    }
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": out["verdict"], "errors": errors}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
