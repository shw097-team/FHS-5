#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-checker finalization: bind NF-T10 to the *current* consumer receipt.

Never reads a stale `negatives.positive.run_id` by default. The receipt is
chosen explicitly (`--consumer-receipt` / `--consumer-run`) or from
`07_CONSUMER/LATEST.json`, then freshness is proven against this tree:
receipt handoff/evidence/pack pins, consumed/validation flags, the negative
suite's positive run id, and `consumer.py --verify-receipt` when an expected
receipt SHA is available. Stale input is rejected with no writes.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

EXPECTED = {"consumer": "consumed", "negatives": "NEGATIVES_REJECTED"}


class Reject(Exception):
    def __init__(self, code: str, detail=None):
        super().__init__(code)
        self.code = code
        self.detail = detail


def verify_receipt_via_consumer(receipt: Path, expected_sha: str) -> dict:
    gate = Path(__file__).with_name("consumer.py")
    proc = subprocess.run(
        [sys.executable, "-B", str(gate), "--verify-receipt", str(receipt),
         "--expected-receipt-sha", expected_sha],
        capture_output=True, text=True, timeout=60)
    try:
        payload = json.loads(proc.stdout)
    except Exception:
        payload = {"status": "UNPARSEABLE_GATE_OUTPUT",
                   "stdout": proc.stdout[:400], "stderr": proc.stderr[:400]}
    return {"exit": proc.returncode, "payload": payload}


def resolve_receipt(args, consumer_root: Path) -> tuple[Path, str, str | None]:
    consumer_root = consumer_root.resolve()
    def confined(p: Path) -> Path:
        rp = p.resolve()
        if not rp.is_relative_to(consumer_root):
            raise Reject("RECEIPT_LOCATOR_OUTSIDE",
                         {"receipt": str(rp), "consumer_root": str(consumer_root)})
        return rp
    if args.consumer_receipt:
        return confined(Path(args.consumer_receipt)), "explicit", None
    if args.consumer_run:
        return confined(consumer_root / "runs" / args.consumer_run / "receipt.json"), \
            "explicit-run", None
    latest_path = consumer_root / "LATEST.json"
    if not latest_path.is_file():
        raise Reject("CONSUMER_RECEIPT_REQUIRED", "no --consumer-receipt/--consumer-run "
                     "and no 07_CONSUMER/LATEST.json")
    latest = lib.load_json(latest_path)
    run_id = latest.get("run_id")
    candidates = []
    if latest.get("receipt"):
        candidates.append(Path(latest["receipt"]))
    if run_id:
        candidates.append(consumer_root / "runs" / str(run_id) / "receipt.json")
    for cand in candidates:
        cand = cand if cand.is_absolute() else (consumer_root / cand)
        rp = confined(cand)
        if rp.is_file():
            return rp, "latest", latest.get("receipt_sha256")
    raise Reject("RECEIPT_MISSING", {"latest": latest})


def finalize(args) -> dict:
    root = Path(args.root).resolve()
    consumer_root = Path(args.consumer_root).resolve() \
        if args.consumer_root else root / "07_CONSUMER"
    receipt_path, source, latest_sha = resolve_receipt(args, consumer_root)
    if not receipt_path.is_file():
        raise Reject("RECEIPT_MISSING", str(receipt_path))

    expected_sha = (args.expected_receipt_sha or "").strip().lower() or None
    sha_source = "argument"
    if not expected_sha and source == "latest" and latest_sha:
        expected_sha = latest_sha
        sha_source = "latest"
    if not expected_sha:
        cm_path = consumer_root / "CONSUMER_MANIFEST.json"
        if cm_path.is_file():
            cm = lib.load_json(cm_path)
            cm_receipt = Path(cm.get("consumer_receipt") or "")
            if not cm_receipt.is_absolute():
                cm_receipt = consumer_root / cm_receipt
            if cm_receipt.resolve() == receipt_path and cm.get("consumer_receipt_sha256"):
                expected_sha = cm["consumer_receipt_sha256"]
                sha_source = "consumer_manifest"
    gate = None
    if expected_sha:
        gate = verify_receipt_via_consumer(receipt_path, expected_sha)
        if gate["exit"] != 0 or gate["payload"].get("status") != "RECEIPT_SHA_OK":
            raise Reject("STALE_CONSUMER_RECEIPT",
                         {"stage": "receipt_sha", "gate": gate})
    else:
        sha_source = "computed_self"

    receipt = lib.load_json(receipt_path)
    if receipt.get("consumed") is not True or receipt.get("validation_ok") is not True:
        raise Reject("RECEIPT_NOT_CONSUMED",
                     {"consumed": receipt.get("consumed"),
                      "validation_ok": receipt.get("validation_ok"),
                      "failure_code": receipt.get("failure_code")})

    handoff_path = root / "09_DELIVERY" / "W0_HANDOFF.md"
    if not handoff_path.is_file():
        raise Reject("HANDOFF_MISSING", str(handoff_path))
    handoff_sha = lib.sha_file(handoff_path)
    if receipt.get("handoff_sha256") != handoff_sha:
        raise Reject("STALE_CONSUMER_RECEIPT",
                     {"stage": "handoff", "receipt": receipt.get("handoff_sha256"),
                      "current": handoff_sha})
    evidence_path = root / "10_EVIDENCE" / "EVIDENCE_MANIFEST.json"
    if not evidence_path.is_file():
        raise Reject("EVIDENCE_MISSING", str(evidence_path))
    evidence_sha = lib.sha_file(evidence_path)
    if receipt.get("evidence_manifest_sha256") != evidence_sha:
        raise Reject("STALE_CONSUMER_RECEIPT",
                     {"stage": "evidence", "receipt":
                      receipt.get("evidence_manifest_sha256"),
                      "current": evidence_sha})

    text = handoff_path.read_text(encoding="utf-8")
    m = re.search(r"pack_manifest_sha256\*\*：`([0-9a-f]{64})`", text)
    pack_pin = m.group(1) if m else None
    pack_dir = Path(receipt.get("pack") or "").resolve()
    pack_manifest = pack_dir / "05_W0_SOURCE_MANIFEST.json"
    if not pack_pin or not pack_manifest.is_file() \
            or lib.sha_file(pack_manifest) != pack_pin:
        raise Reject("STALE_CONSUMER_RECEIPT", {"stage": "pack",
                     "pack": str(pack_manifest), "handoff_pin": pack_pin})
    pack_in_root = pack_dir.is_relative_to(root)

    negatives_path = Path(args.negatives).resolve() if args.negatives \
        else consumer_root / "negatives.json"
    if not negatives_path.is_file():
        raise Reject("NEGATIVES_MISSING", str(negatives_path))
    negatives = lib.load_json(negatives_path)
    pos = negatives.get("positive") or {}
    if negatives.get("verdict") != EXPECTED["negatives"] \
            or negatives.get("all_rejected") is False:
        raise Reject("NEGATIVES_NOT_REJECTED", negatives.get("verdict"))
    if pos.get("run_id") != receipt.get("run_id"):
        raise Reject("STALE_NEGATIVES_POSITIVE",
                     {"negatives_positive": pos.get("run_id"),
                      "receipt_run_id": receipt.get("run_id")})
    if pos.get("consumed") is not True:
        raise Reject("NEGATIVES_POSITIVE_NOT_CONSUMED", pos.get("consumed"))

    rec_path = root / "05_TQAEP" / "receipts" / "NF-T10.json"
    rec = lib.load_json(rec_path)
    frozen = rec.get("expected")
    if frozen is not None and frozen != EXPECTED:
        raise Reject("EXPECTED_FROZEN_MISMATCH", frozen)
    summary_path = root / "05_TQAEP" / "summary.json"
    summary = lib.load_json(summary_path)

    receipt_sha = lib.sha_file(receipt_path)
    observed = {
        "consumer_run_id": receipt.get("run_id"),
        "consumer_receipt": str(receipt_path),
        "consumer_receipt_sha256": receipt_sha,
        "checks": len(receipt.get("checks") or []),
        "negatives": negatives.get("verdict"),
        "negatives_positive_run_id": pos.get("run_id"),
        "negatives_sha256": lib.sha_file(negatives_path),
        "negative_count": len(negatives.get("negative_cases") or []),
        "cli_executed": (receipt.get("cli") or {}).get("executed"),
        "selection": source,
        "receipt_sha_source": sha_source,
        "receipt_sha_verified_via": ("consumer.py --verify-receipt"
                                     if gate else None),
        "handoff_sha256": handoff_sha,
        "evidence_manifest_sha256": evidence_sha,
        "pack_manifest_sha256": pack_pin,
        "receipt_pack_path_in_root": pack_in_root,
    }
    plan = {"status": "FINALIZE_T10_PASS", "observed": observed,
            "dry_run": bool(args.dry_run)}
    if args.dry_run:
        return plan

    rec["expected"] = EXPECTED
    rec["observed"] = observed
    rec["verdict"] = "PASS"
    rec["first_fail"] = ""
    rec["recovery_ref"] = str(receipt_path)
    rec["not_covered"] = ["HERMES/GPT host execution"]
    lib.write_json(rec_path, rec)

    for c in summary["cases"]:
        if c["case_id"] == "NF-T10":
            c["verdict"] = rec["verdict"]
            c["first_fail"] = rec["first_fail"]
    summary["counts"]["pass"] = sum(1 for c in summary["cases"]
                                    if c["verdict"] == "PASS")
    summary["counts"]["fail"] = sum(1 for c in summary["cases"]
                                    if c["verdict"] not in ("PASS",
                                                            "PENDING_CONSUMER"))
    summary["counts"]["pending"] = sum(1 for c in summary["cases"]
                                       if c["verdict"] == "PENDING_CONSUMER")
    summary["receipts_index_sha"] = lib.canonical_sha(
        {p.name: lib.sha_file(p)
         for p in sorted((root / "05_TQAEP" / "receipts").glob("*.json"))
         if p.name != "NF-T10.json"})
    summary["finalized_t10"] = {
        "consumer_run_id": receipt.get("run_id"),
        "consumer_receipt_sha256": receipt_sha,
        "negatives_sha256": lib.sha_file(negatives_path),
        "selection": source,
    }
    lib.write_json(summary_path, summary)
    plan["counts"] = summary["counts"]
    return plan


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(lib.ROOT))
    ap.add_argument("--consumer-root")
    ap.add_argument("--consumer-receipt")
    ap.add_argument("--consumer-run")
    ap.add_argument("--expected-receipt-sha")
    ap.add_argument("--negatives")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        plan = finalize(a)
    except Reject as exc:
        print(json.dumps({"status": "REJECTED", "code": exc.code,
                          "detail": exc.detail, "writes": False},
                         ensure_ascii=False))
        return 3
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
