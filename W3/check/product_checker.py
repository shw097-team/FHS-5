#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

from product_verify import pred_full
from w3_common import load_json_strict, sha256_file


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--product-pack", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    man = load_json_strict(os.path.join(a.product_pack, "05_W3_SOURCE_MANIFEST.json"))
    ledger = load_json_strict(a.ledger)
    pins = {k: v["value"] for k, v in ledger["pins"].items()}
    errors = []
    rows = []
    for ref in man["case_refs"]:
        cid = ref["case_id"]
        rec_path = os.path.join(a.root, "evidence", a.run_id, "cases", cid, "record.json")
        if not os.path.isfile(rec_path):
            errors.append("missing:" + cid)
            continue
        rec = load_json_strict(rec_path)
        oracle = load_json_strict(os.path.join(a.product_pack, ref["oracle"]["path"].replace("/", os.sep)))
        token_ok = rec.get("observed", {}).get("token") == oracle["expected"]["token"]
        checks = []
        for p in oracle.get("predicates", []):
            try:
                ok = pred_full(p["id"], rec, {"ledger_pins": pins})
            except Exception:
                ok = False
            checks.append({"predicate": p["id"], "ok": bool(ok)})
        ok = token_ok and checks and all(x["ok"] for x in checks)
        if not ok:
            errors.append("fail:" + cid)
        rows.append({"case_id": cid, "token_ok": token_ok, "checks": checks,
                     "verdict": "PASS" if ok else "FAIL"})
    out = {
        "schema": "FHS5.PLP.W3.ProductCheckerReceipt@1",
        "checker_role": "DISTINCT_READ_ONLY_PRODUCT_CHECKER",
        "checker_script_sha256": sha256_file(os.path.abspath(__file__)),
        "argv": [sys.executable, os.path.abspath(__file__)] + (argv or []),
        "run_id": a.run_id,
        "rows_checked": len(rows),
        "rows": rows,
        "errors": errors,
        "verdict": "PASS" if not errors else "FAIL",
        "strength": "DISTINCT_LOCAL_PROCESS_READONLY_PRODUCT; NOT_ORIGINAL_DOMAIN_PRINCIPAL",
        "limitations": ["same OS principal as maker",
                        "Generic Native product projection, not original-domain oracle"],
    }
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": out["verdict"], "rows": len(rows), "errors": errors}))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
