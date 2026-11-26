#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

from w3_cases import run_case
from w3_common import sha256_bytes, write_json


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--product-pack", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--ledger", required=True)
    a = ap.parse_args(argv)
    ledger = json.load(open(a.ledger, encoding="utf-8"))
    rec = run_case(a.product_pack, a.case, a.root, ledger, a.run_id, mode="engine")
    case_dir = os.path.join(a.root, "evidence", a.run_id, "cases", a.case)
    code = rec.get("engine_exit", 0)
    rec["process_exit"] = code
    payload = json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    open(os.path.join(case_dir, "stdout.txt"), "w", encoding="utf-8", newline="\n").write(payload)
    rec["stdout_ref"] = os.path.join(case_dir, "stdout.txt")
    rec["stdout_sha256"] = sha256_bytes(payload.encode("utf-8"))
    write_json(os.path.join(case_dir, "record.json"), rec)
    sys.stdout.write(json.dumps(rec, ensure_ascii=False, indent=2) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
