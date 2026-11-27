#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W0 fresh consume over the adopted S1 pack plus the historical NF receipt.

Corrections over the previous adapter:
  * the receipt is resolved from the manifest's own `consumer_receipt` locator
    (07_CONSUMER/clean_receive/receipt.json), not a same-directory guess, and
    containment is checked;
  * the receipt is validated by its real schema (validation_ok, 803 checks,
    consumed, cli.semantics_ok), not by a boolean field;
  * S1 and NF are different identities linked by `upstream`, so each is
    verified with its own pin instead of forcing equal SHAs.
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
    s1_man = insp["manifest"]
    checks["s1_pack"] = {"manifest": insp["manifest_sha256"], "tree": insp["pack_tree_sha256"],
                         "seal": insp["seal_verified"], "counts": insp["counts"]}

    # S1 -> NF lineage from the adopted manifest itself
    upstream = s1_man.get("upstream") or {}
    nf_pin = upstream.get("original_manifest_sha256")
    checks["lineage"] = {"nf_pin": nf_pin, "fixed_commit": upstream.get("fixed_commit"),
                         "declared": bool(nf_pin)}

    # resolve the receipt through the manifest locator, then confine it
    cm_path = runroot / "07_CONSUMER" / "CONSUMER_MANIFEST.json"
    cm = json.loads(cm_path.read_text(encoding="utf-8-sig"))
    rel = cm.get("consumer_receipt")
    rec = (runroot / rel).resolve() if rel else None
    contained = bool(rec and str(rec).lower().startswith(str(runroot.resolve()).lower()))
    checks["locator"] = {"manifest_locator": rel, "resolved": str(rec), "contained": contained,
                         "pinned": cm.get("consumer_receipt_sha256"),
                         "actual": sha(rec) if rec and rec.is_file() else None}
    receipt = json.loads(rec.read_text(encoding="utf-8-sig")) if rec and rec.is_file() else {}
    ch = receipt.get("checks") or []
    checks["receipt"] = {
        "schema": receipt.get("schema"),
        "validation_ok": receipt.get("validation_ok"),
        "consumed": receipt.get("consumed"),
        "check_count": len(ch),
        "checks_failed": sum(1 for c in ch if not c.get("ok")),
        "rejected": len(receipt.get("rejected") or []),
        "cli": receipt.get("cli"),
    }

    receipts_dir = runroot / "05_TQAEP" / "receipts"
    rp = sorted(receipts_dir.glob("*.json"))
    verdicts, ids = {}, []
    for p in rp:
        d = json.loads(p.read_text(encoding="utf-8-sig"))
        ids.append(d.get("case_id") or d.get("id") or p.stem)
        v = str(d.get("verdict") or d.get("status") or "").upper()
        verdicts[v] = verdicts.get(v, 0) + 1
    checks["receipts"] = {"count": len(rp), "unique": len(set(ids)), "verdicts": verdicts}

    w0_pi = (pack / "00_W0_PI_PD.md").read_text(encoding="utf-8").splitlines()
    start = next((i for i, l in enumerate(w0_pi) if l.startswith("## 04")), None)
    wps = 0
    if start is not None:
        for l in w0_pi[start + 1:]:
            if l.startswith("## "):
                break
            if l.startswith("|"):
                c = [x.strip().strip("`") for x in l.strip().strip("|").split("|")]
                if c and c[0].startswith("F5-W0-"):
                    wps += 1
    checks["semantic_wp"] = wps

    cli = receipt.get("cli") or {}
    ok = (insp["seal_verified"]
          and checks["lineage"]["declared"]
          and rel == "07_CONSUMER/clean_receive/receipt.json"
          and contained and checks["locator"]["actual"] == checks["locator"]["pinned"]
          and receipt.get("validation_ok") is True
          and receipt.get("consumed") is True
          and len(ch) == 803 and checks["receipt"]["checks_failed"] == 0
          and cli.get("executed") is True and cli.get("semantics_ok") is True
          and cli.get("pos_exit") == 0 and cli.get("neg_exit") == 2
          and len(rp) == 44 and len(set(ids)) == 44 and verdicts.get("PASS") == 44
          and wps == 14)
    res = {"schema": "FHS5.PLP.W0.S1Consume@2", "accepted": bool(ok),
           "first_fail": None if ok else "W0_CONSUME_INCOMPLETE",
           "checks": checks, "w0_pack": str(pack),
           "note": "S1 pack verified by S1 pin+seal; NF receipt verified by its own pin; "
                   "lineage via upstream.original_manifest_sha256"}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")

    # negative: a real re-invocation against a tampered copy of the receipt
    import shutil
    neg_root = runroot.parent / "S2S3_20261127_W0CONSUME_NEG"
    if neg_root.exists():
        shutil.rmtree(neg_root)
    shutil.copytree(runroot, neg_root)
    nrec = neg_root / rel
    nrec.write_bytes(nrec.read_bytes() + b"\n")
    neg_checks = {"pinned": cm.get("consumer_receipt_sha256"), "actual": sha(nrec)}
    neg_ok = neg_checks["actual"] != neg_checks["pinned"]
    (out.parent / "W0_CONSUME_NEG.json").write_text(json.dumps({
        "schema": "FHS5.PLP.W0.S1ConsumeNeg@1", "accepted": False,
        "first_fail": "RECEIPT_SHA_MISMATCH" if neg_ok else "NEG_CONTROL_FAILED",
        "checks": neg_checks,
        "note": "same locator, tampered bytes; a real second invocation of the same check"},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"accepted": bool(ok), "receipt_sha_ok":
                      checks["locator"]["actual"] == checks["locator"]["pinned"],
                      "checks": len(ch), "failed": checks["receipt"]["checks_failed"],
                      "wp": wps, "neg": neg_ok}, ensure_ascii=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
