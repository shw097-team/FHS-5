#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single-case CLI for the W3 engine.

Exit 0 = design predicate PASS (POS), 2 = design predicate PASS (NEG refusal),
1 = FAIL/engine error. The record JSON is the evidence; exit alone is not PASS.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

from w3_cases import run_case
from w3_common import sha256_bytes, write_json
from w3_intake import build_freeze_ledger, verify_pack


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--w2-root", default=None)
    ap.add_argument("--seal", default=None)
    ap.add_argument("--adoption", default=None)
    ap.add_argument("--current", default=None)
    a = ap.parse_args(argv)

    if a.ledger and os.path.isfile(a.ledger):
        ledger = json.load(open(a.ledger, "r", encoding="utf-8"))
    else:
        verified = verify_pack(a.pack, a.seal, a.adoption, a.current)
        update = {v["path"]: v for v in []}
        ledger = build_freeze_ledger(a.pack, verified, a.w2_root)

    record = run_case(a.pack, a.case, a.root, ledger, a.run_id)
    case_dir = os.path.join(a.root, "evidence", a.run_id, "cases", a.case)
    if record["design_verdict"] == "PASS":
        code = 2 if record["kind"] == "NEG" else 0
    else:
        code = 1
    record["process_exit"] = code
    payload = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out_path = os.path.join(case_dir, "stdout.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    record["stdout_ref"] = out_path
    record["stdout_sha256"] = sha256_bytes(payload.encode("utf-8"))
    record["stderr_ref"] = os.path.join(case_dir, "stderr.txt")
    record["stderr_sha256"] = sha256_bytes(b"")
    open(record["stderr_ref"], "wb").close()
    write_json(os.path.join(case_dir, "record.json"), record)
    sys.stdout.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
