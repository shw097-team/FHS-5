#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derive the W1 technical claim from the consumed receipt, negative suite and
the evidence manifest's own derived B0/W0 claims. No self-hash cycle."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib


def main():
    root = lib.ROOT / "07_CONSUMER"
    cm_path = root / "CONSUMER_MANIFEST.json"
    cm = lib.load_json(cm_path)
    receipt = lib.load_json(Path(cm["consumer_receipt"]))
    negatives = lib.load_json(root / "negatives.json")
    evidence = lib.load_json(lib.ROOT / "10_EVIDENCE" / "EVIDENCE_MANIFEST.json")
    derived = {
        "receipt_consumed": receipt.get("consumed") is True,
        "receipt_validated": receipt.get("validation_ok") is True,
        "checks": len(receipt.get("checks") or []),
        "negatives_rejected": negatives.get("verdict") == "NEGATIVES_REJECTED",
        "evidence_B0": evidence.get("claims", {}).get("B0") == "B0_NF_VALIDATED",
        "evidence_W0": evidence.get("claims", {}).get("W0") == "W0_NF_VALIDATED",
        "evidence_sha_match": cm.get("evidence_manifest_sha256")
        == lib.sha_file(lib.ROOT / "10_EVIDENCE" / "EVIDENCE_MANIFEST.json"),
    }
    ok = all(v for k, v in derived.items() if k != "checks") and derived["checks"] >= 700
    cm["claims"] = {
        "W1_technical": "W1_TECHNICALLY_READY" if ok else "W1_NOT_READY",
        "W1_execution": "NOT_CLAIMED",
        "release": "NOT_CLAIMED",
        "different_principal_independence": "NOT_CLAIMED",
        "other_hosts": "NOT_CLAIMED",
    }
    cm["claim_derivation"] = derived
    lib.write_json(cm_path, cm)
    lib.write_json(root / "CONSUMER_MANIFEST.sha256",
                   {"sha256": lib.sha_file(cm_path)})
    print(json.dumps({"claims": cm["claims"], "derivation": derived,
                      "manifest": lib.sha_file(cm_path)}, ensure_ascii=False, indent=2))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
