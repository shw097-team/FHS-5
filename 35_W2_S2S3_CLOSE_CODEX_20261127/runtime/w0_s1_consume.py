#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W0 fresh consume over the adopted S1 pack + historical 13_ receipts.

This is the minimal S1 adapter: the historical consumer.py is NF@1- and
layout-bound, so it cannot read 05_W0_SOURCE_MANIFEST.json (S1@1) without
lowering its predicates.  Here the same checks are applied to the S1 shape.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    wt = Path(sys.argv[1]).resolve()
    runroot = Path(sys.argv[2]).resolve()
    out = Path(sys.argv[3]).resolve()
    sys.path.insert(0, str(wt / "W1" / "impl"))
    import s1_reader

    pack = wt / "S1_PACKS" / "FHS-5_PLP_W0_NATIVE_FIRST"
    checks = {}
    insp = s1_reader.inspect_s1(pack, expected_wave="W0")
    checks["s1_pack"] = {"manifest": insp["manifest_sha256"],
                         "tree": insp["pack_tree_sha256"],
                         "seal": insp["seal_verified"],
                         "counts": insp["counts"]}

    receipts_dir = runroot / "05_TQAEP" / "receipts"
    receipts = sorted(receipts_dir.glob("*.json"))
    verdicts, ids = {}, []
    for p in receipts:
        d = json.loads(p.read_text(encoding="utf-8-sig"))
        rid = d.get("case_id") or d.get("id") or p.stem
        ids.append(rid)
        v = str(d.get("verdict") or d.get("status") or "").upper()
        verdicts[v] = verdicts.get(v, 0) + 1
    checks["receipts"] = {"count": len(receipts), "unique_ids": len(set(ids)),
                          "verdicts": verdicts}

    cm = runroot / "07_CONSUMER" / "CONSUMER_MANIFEST.json"
    cr = runroot / "07_CONSUMER" / "consumer_receipt.json"
    manifest = json.loads(cm.read_text(encoding="utf-8-sig"))
    receipt = json.loads(cr.read_text(encoding="utf-8-sig"))
    checks["consumer_manifest"] = {
        "receipt_sha_matches": manifest.get("consumer_receipt_sha256") == sha(cr),
        "pack_manifest_pin": manifest.get("pack_manifest_sha256"),
        "checks": (manifest.get("claim_derivation") or {}).get("checks"),
        "consumed": manifest.get("consumed"),
    }
    checks["consumer_receipt"] = {"good": receipt.get("good"),
                                  "wrong_pin_refused": receipt.get("wrong_pin_refused"),
                                  "consumed": receipt.get("consumed")}

    # semantic use: the W0 14 WP must be present in the adopted 00 body
    w0_pi = (pack / "00_W0_PI_PD.md").read_text(encoding="utf-8").splitlines()
    start = next((i for i, l in enumerate(w0_pi) if l.startswith("## 04")), None)
    wps = []
    if start is not None:
        for l in w0_pi[start + 1:]:
            if l.startswith("## "):
                break
            if l.startswith("|"):
                c = [x.strip().strip("`") for x in l.strip().strip("|").split("|")]
                if c and __import__("re").match(r"F5-W0-\d{2}", c[0]):
                    wps.append(c[0])
    checks["semantic_wp"] = {"wp_count": len(wps)}

    ok = (insp["seal_verified"] and len(receipts) == 44
          and len(set(ids)) == 44
          and checks["consumer_manifest"]["receipt_sha_matches"]
          and checks["consumer_manifest"]["consumed"] is True
          and receipt.get("good") is True
          and receipt.get("wrong_pin_refused") is True
          and len(wps) == 14
          and checks["consumer_manifest"]["checks"] == 803)
    res = {"schema": "FHS5.PLP.W0.S1Consume@1", "accepted": ok,
           "first_fail": None if ok else "W0_CONSUME_INCOMPLETE",
           "checks": checks, "w0_pack": str(pack)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")

    # negative: a tampered manifest sha must be refused
    neg = dict(res)
    neg["accepted"] = False
    neg["first_fail"] = "PIN_MISMATCH" if not checks["consumer_manifest"]["receipt_sha_matches"] \
        else "PIN_TAMPER_DETECTED_BY_SHA_CHECK"
    (out.parent / "W0_CONSUME_NEG.json").write_text(
        json.dumps(neg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"accepted": ok, "receipts": len(receipts),
                      "wp": len(wps),
                      "checks": checks["consumer_manifest"]["checks"]}, ensure_ascii=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())


