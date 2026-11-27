#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent OPS consumer: re-reads the receipt/material and verifies them."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    t = Path(a.target)
    receipt = json.loads((t / "w2_binding_receipt.json").read_text(encoding="utf-8"))
    material = json.loads((t / "w2_effect_material" / "material.json").read_text(encoding="utf-8"))
    checks = {
        "schema": receipt.get("schema") == "FHS5.PLP.W2.BindingReceipt@1",
        "subject": receipt.get("subject") == "FHS-5_PLP/W2/CONTROL_PACK",
        "scope": receipt.get("scope") == "W2-NF-01",
        "cases": (receipt.get("parsed") or {}).get("cases") == 12,
        "pins": all((receipt.get("pins") or {}).get(k) for k in
                    ("manifest_sha256", "tree_sha256", "case_set_sha256")),
        "material_cases": len(material.get("cases") or []) == 12,
        "readback": (receipt.get("readback") or {}).get("fixture_case") is not None,
    }
    out = {"consumer_id": "g3-w2-ops-consumer-20261127",
           "checks": checks, "all_ok": all(checks.values()),
           "receipt_sha256": sha(t / "w2_binding_receipt.json"),
           "material_sha256": sha(t / "w2_effect_material" / "material.json"),
           "subject": receipt.get("subject"), "scope": receipt.get("scope"),
           "action": "parse+use+field-compare+readback"}
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"all_ok": out["all_ok"]}))
    return 0 if out["all_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
