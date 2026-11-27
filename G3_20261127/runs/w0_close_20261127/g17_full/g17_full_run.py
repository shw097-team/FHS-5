#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G17 full-entry driver: real W1 Consumer POS, one-byte NEG, outside locator."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

BASE = Path(r"C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\g3-20261127\G3_20261127\runs\w0_close_20261127")
ROOT = BASE / "13"
G = BASE / "g17_full"
TOOL = ROOT / "tools" / "w1_min_consume.py"
HANDOFF = ROOT / "09_DELIVERY" / "W0_HANDOFF.md"
LATEST = json.loads((ROOT / "07_CONSUMER" / "LATEST.json").read_text(encoding="utf-8"))
RECEIPT = Path(LATEST["receipt"])
EXPECTED = LATEST["receipt_sha256"]
REPO = G / "candidate"
POS_OUT = BASE / "w1_out_pos"

def run(args):
    p = subprocess.run([sys.executable, "-B", str(TOOL), *args],
                       capture_output=True, text=True, timeout=300)
    try:
        payload = json.loads(p.stdout)
    except Exception:
        payload = {"raw": p.stdout[-2000:]}
    return {"exit": p.returncode, "stdout": payload,
            "stderr": p.stderr[-2000:]}

def common(out_root, receipt):
    return ["--handoff", str(HANDOFF), "--root", str(ROOT), "--repo", str(REPO),
            "--out-root", str(out_root), "--scope", "W0",
            "--receipt", str(receipt), "--expected-receipt-sha", EXPECTED]

def clean(p: Path):
    if p.exists():
        shutil.rmtree(p)

def main():
    if not REPO.is_dir():
        p = subprocess.run(["git", "-c", "core.fscache=false", "clone", "--quiet",
                            str(ROOT / "02_CANDIDATE" / "repo.bundle"), str(REPO)],
                           capture_output=True, text=True, timeout=180)
        if p.returncode != 0:
            raise SystemExit("clone failed: " + p.stderr)
        p = subprocess.run(["git", "-c", "core.fscache=false", "-C", str(REPO),
                            "checkout", "--quiet",
                            "bb66a276aae8c5d6aef549832c523587fc47d247"],
                           capture_output=True, text=True, timeout=180)
        if p.returncode != 0:
            raise SystemExit("checkout failed: " + p.stderr)

    clean(POS_OUT)
    pos = run(common(POS_OUT, RECEIPT))
    pos_receipt = POS_OUT / "consume_receipt.json"
    pos_payload = json.loads(pos_receipt.read_text(encoding="utf-8")) if pos_receipt.is_file() else {}
    pos_ok = (pos["exit"] == 0 and pos["stdout"].get("status") == "W1_CHECKLIST_READY"
              and pos["stdout"].get("items") == 44 and pos["stdout"].get("readback_ok") is True
              and (pos["stdout"].get("receipt_gate") or {}).get("receipt_parsed") is True
              and (pos["stdout"].get("receipt_gate") or {}).get("observed_receipt_sha256") == EXPECTED)
    pos_out = {"schema": "FHS5.W0.G17.FullPOS@1", "receipt": str(RECEIPT),
               "expected_receipt_sha256": EXPECTED, "run": pos,
               "consume_receipt": str(pos_receipt),
               "consume_receipt_sha256": hashlib.sha256(pos_receipt.read_bytes()).hexdigest() if pos_receipt.is_file() else None,
               "checklist": str(POS_OUT / "w1_checklist.json"),
               "checklist_sha256": hashlib.sha256((POS_OUT / "w1_checklist.json").read_bytes()).hexdigest() if (POS_OUT / "w1_checklist.json").is_file() else None,
               "items": pos["stdout"].get("items"), "readback_ok": pos["stdout"].get("readback_ok"),
               "verdict": "PASS" if pos_ok else "FAIL"}
    (G / "g17_pos.json").write_text(json.dumps(pos_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    negdir = ROOT / "07_CONSUMER" / "runs" / "g17_neg_20261128"
    negdir.mkdir(parents=True, exist_ok=True)
    mut = negdir / "receipt.json"
    raw = RECEIPT.read_bytes()
    b = bytearray(raw); off = len(b)//2; b[off] ^= 1
    mut.write_bytes(bytes(b))
    neg_out_dir = G / "neg_byte" / "out"; clean(neg_out_dir)
    neg = run(common(neg_out_dir, mut))
    neg_ok = (neg["exit"] == 3 and neg["stdout"].get("status") == "REJECTED"
              and neg["stdout"].get("code") == "RECEIPT_SHA_MISMATCH"
              and not (neg_out_dir / "w1_checklist.json").exists())
    neg_out = {"schema": "FHS5.W0.G17.FullNEG@1", "receipt": str(mut),
               "expected_receipt_sha256": EXPECTED,
               "mutation": {"offset": off, "xor": "0x01", "single_byte": True,
                            "size_unchanged": len(b) == len(raw)},
               "run": neg, "output_written": (neg_out_dir / "w1_checklist.json").exists(),
               "verdict": "PASS" if neg_ok else "FAIL"}
    (G / "g17_neg_byte.json").write_text(json.dumps(neg_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    outside = G / "outside" / "receipt.json"
    outside.write_text(json.dumps({"status": "OUTSIDE_CANARY_DO_NOT_READ",
                                   "expected_receipt_sha256": EXPECTED}) + "\n", encoding="utf-8")
    loc_out_dir = G / "neg_locator" / "out"; clean(loc_out_dir)
    loc = run(common(loc_out_dir, outside))
    loc_ok = (loc["exit"] == 3 and loc["stdout"].get("status") == "REJECTED"
              and loc["stdout"].get("code") == "RECEIPT_LOCATOR_OUTSIDE"
              and not (loc_out_dir / "w1_checklist.json").exists())
    audit_out_dir = G / "neg_locator" / "audit_out"; clean(audit_out_dir)
    audit = subprocess.run([sys.executable, "-B", str(G / "audit_locator.py"),
                            str(TOOL), str(HANDOFF), str(ROOT), str(REPO),
                            str(audit_out_dir), str(outside), EXPECTED],
                           capture_output=True, text=True, timeout=300)
    try:
        audit_payload = json.loads(audit.stdout)
    except Exception:
        audit_payload = {"raw": audit.stdout[-1000:]}
    audit_ok = audit_payload.get("outside_opened") is False and audit_payload.get("exit") == 3
    loc_out = {"schema": "FHS5.W0.G17.FullLocatorNEG@1", "receipt": str(outside),
               "run": loc, "audit": audit_payload,
               "audit_zero_outside_read": audit_ok,
               "output_written": (loc_out_dir / "w1_checklist.json").exists(),
               "verdict": "PASS" if (loc_ok and audit_ok) else "FAIL"}
    (G / "g17_neg_locator.json").write_text(json.dumps(loc_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    overall = pos_ok and neg_ok and loc_ok and audit_ok
    summary = {"schema": "FHS5.W0.G17.FullSuite@1", "pos": pos_ok, "neg_byte": neg_ok,
               "neg_locator": loc_ok, "audit_zero_outside_read": audit_ok,
               "receipt_sha256": EXPECTED, "items": pos["stdout"].get("items"),
               "checklist_sha256": pos_out["checklist_sha256"],
               "verdict": "PASS" if overall else "FAIL"}
    (G / "G17_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if overall else 3

if __name__ == "__main__":
    sys.exit(main())