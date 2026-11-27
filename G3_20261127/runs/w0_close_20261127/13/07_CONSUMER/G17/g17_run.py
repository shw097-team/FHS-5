#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical G17: same consumer entry, valid receipt POS, one-byte NEG."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = Path(__file__).resolve().parent
CONSUMER = ROOT / "tools" / "consumer.py"
LATEST = json.loads((ROOT / "07_CONSUMER" / "LATEST.json").read_text(encoding="utf-8"))
RECEIPT = Path(LATEST["receipt"])
EXPECTED = LATEST["receipt_sha256"]
ISO = G / "isolated_root"

def run_gate(receipt: Path, marker: Path):
    p = subprocess.run([sys.executable, "-B", str(CONSUMER), "--verify-receipt", str(receipt),
                        "--expected-receipt-sha", EXPECTED, "--downstream-marker", str(marker),
                        "--root", str(ISO)], capture_output=True, text=True, timeout=60)
    try:
        payload = json.loads(p.stdout)
    except Exception:
        payload = {"raw": p.stdout[-1000:]}
    return {"exit": p.returncode, "payload": payload, "stdout": p.stdout, "stderr": p.stderr}

def audit(receipt: Path, marker: Path | None):
    cmd = [sys.executable, "-B", str(G / "audit_scope.py"), "--target", str(CONSUMER),
           "--root", str(ROOT), "--receipt", str(receipt), "--expected-receipt-sha", EXPECTED]
    if marker:
        cmd += ["--downstream-marker", str(marker)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    try:
        return {"exit": p.returncode, "payload": json.loads(p.stdout)}
    except Exception:
        return {"exit": p.returncode, "payload": {"raw": p.stdout[-1000:]}, "stderr": p.stderr}

def main():
    marker_root = ROOT.parent / "g17_markers"
    marker_root.mkdir(parents=True, exist_ok=True)
    pos_marker = marker_root / "pos_downstream_marker.json"
    neg_marker = marker_root / "neg_downstream_marker.json"
    for p in (pos_marker, neg_marker):
        if p.exists():
            p.unlink()
    pos = run_gate(RECEIPT, pos_marker)
    pos_ok = (pos["exit"] == 0 and pos["payload"].get("status") == "RECEIPT_SHA_OK"
              and pos_marker.is_file())
    pos_out = {"schema": "FHS5.W0NF.G17.POS@2", "receipt": str(RECEIPT),
               "receipt_sha256": EXPECTED, "gate": pos,
               "marker": str(pos_marker), "marker_exists": pos_marker.is_file(),
               "marker_sha256": hashlib.sha256(pos_marker.read_bytes()).hexdigest() if pos_marker.is_file() else None,
               "verdict": "PASS" if pos_ok else "FAIL"}
    (G / "g17_pos.json").write_text(json.dumps(pos_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    raw = RECEIPT.read_bytes()
    mut = bytearray(raw)
    off = len(mut) // 2
    mut[off] ^= 1
    mutated = G / "neg" / "receipt.mutated.json"
    mutated.write_bytes(bytes(mut))
    neg = run_gate(mutated, neg_marker)
    neg_ok = (neg["exit"] == 3 and neg["payload"].get("status") == "RECEIPT_SHA_MISMATCH"
              and neg["payload"].get("receipt_parsed") is False
              and not neg_marker.exists())
    neg_out = {"schema": "FHS5.W0NF.G17.NEG@2", "original_receipt": str(RECEIPT),
               "original_sha256": EXPECTED, "mutated_receipt": str(mutated),
               "mutated_sha256": hashlib.sha256(mutated.read_bytes()).hexdigest(),
               "mutation": {"offset": off, "xor": "0x01", "single_byte": True,
                            "size_unchanged": len(mutated.read_bytes()) == len(raw)},
               "gate": neg, "marker": str(neg_marker), "marker_exists": neg_marker.exists(),
               "verdict": "PASS" if neg_ok else "FAIL"}
    (G / "g17_neg.json").write_text(json.dumps(neg_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    apos = audit(RECEIPT, pos_marker)
    aneg = audit(mutated, neg_marker)
    audit_ok = (apos["payload"].get("zero_outside_read") is True
                and not apos["payload"].get("unexpected_root_opens")
                and not apos["payload"].get("process_or_network_events")
                and aneg["payload"].get("zero_outside_read") is True
                and not aneg["payload"].get("unexpected_root_opens")
                and not aneg["payload"].get("process_or_network_events"))
    (G / "g17_audit.json").write_text(json.dumps({"pos": apos, "neg": aneg,
                                                  "verdict": "PASS" if audit_ok else "FAIL"},
                                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    overall = pos_ok and neg_ok and audit_ok
    print(json.dumps({"pos": pos_ok, "neg": neg_ok, "audit": audit_ok,
                      "verdict": "PASS" if overall else "FAIL",
                      "receipt_sha256": EXPECTED}, ensure_ascii=False, indent=2))
    return 0 if overall else 3

if __name__ == "__main__":
    sys.exit(main())