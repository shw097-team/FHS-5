#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-checker finalization: bind NF-T10 to the real consumer receipt and
negative suite, then update the summary without touching checker-pinned cases."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib


def main():
    cons_path = lib.ROOT / "07_CONSUMER" / "runs"
    negatives = lib.load_json(lib.ROOT / "07_CONSUMER" / "negatives.json")
    pos_run = negatives["positive"]["run_id"]
    receipt_path = lib.ROOT / "07_CONSUMER" / "runs" / pos_run / "receipt.json"
    receipt = lib.load_json(receipt_path)
    ok = (negatives.get("verdict") == "NEGATIVES_REJECTED"
          and receipt.get("consumed") is True
          and receipt.get("validation_ok") is True)
    rec = lib.load_json(lib.TQAEP / "receipts" / "NF-T10.json")
    rec["expected"] = {"consumer": "consumed", "negatives": "NEGATIVES_REJECTED"}
    rec["observed"] = {
        "consumer_run_id": receipt.get("run_id"),
        "consumer_receipt_sha256": lib.sha_file(receipt_path),
        "checks": len(receipt.get("checks") or []),
        "negatives": negatives.get("verdict"),
        "negative_count": len(negatives.get("negative_cases") or []),
        "cli_executed": (receipt.get("cli") or {}).get("executed"),
    }
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = "" if ok else "HANDOFF_UNCONSUMED"
    rec["recovery_ref"] = str(receipt_path)
    rec["not_covered"] = ["HERMES/GPT host execution"]
    lib.write_json(lib.TQAEP / "receipts" / "NF-T10.json", rec)

    summary = lib.load_json(lib.TQAEP / "summary.json")
    for c in summary["cases"]:
        if c["case_id"] == "NF-T10":
            c["verdict"] = rec["verdict"]
            c["first_fail"] = rec["first_fail"]
    summary["counts"]["pass"] = sum(1 for c in summary["cases"] if c["verdict"] == "PASS")
    summary["counts"]["fail"] = sum(1 for c in summary["cases"] if c["verdict"] != "PASS")
    summary["counts"]["pending"] = sum(1 for c in summary["cases"]
                                       if c["verdict"] == "PENDING_CONSUMER")
    summary["receipts_index_sha"] = lib.canonical_sha(
        {p.name: lib.sha_file(p) for p in sorted((lib.TQAEP / "receipts").glob("*.json"))
         if p.name != "NF-T10.json"})
    summary["finalized_t10"] = {"consumer_run_id": receipt.get("run_id")}
    lib.write_json(lib.TQAEP / "summary.json", summary)
    print(json.dumps({"t10": rec["verdict"], "counts": summary["counts"],
                      "consumer": receipt.get("run_id")}, ensure_ascii=False, indent=2))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
