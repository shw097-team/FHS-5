#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal W2 technical receiver (R05).

Consumes the frozen W1 delivery (not the maker's memory) from a clean root and
returns a receipt with accept/reject, next legal operation, stop and resume.

It refuses wrong candidate, pack, oracle, evidence, handoff, scope or ABI, and
it never issues a grant or performs a W2 protected effect.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import nf_reader as reader
import w1_nf_reader as base

NFError = base.NFError
PACK_PIN = "61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def receive(delivery: Path, w2_identity: dict) -> dict:
    d = delivery.resolve()
    checks, rejected, reasons = [], [], []

    def chk(name, ok, detail):
        checks.append({"check": name, "ok": bool(ok), "detail": str(detail)[:200]})
        if not ok:
            rejected.append(name)
            reasons.append(f"{name}: {detail}")
        return ok

    man_p = d / "EVIDENCE_MANIFEST.json"
    seal_p = d / "DELIVERY_SEAL.json"
    hand_p = d / "FHS-5_PLP_W1_HANDOFF.md"
    close_p = d / "FHS-5_PLP_W1_CLOSEOUT.md"
    pack = d / "control_pack" / "FHS-5_PLP_W1_NATIVE_FIRST"

    if not chk("delivery_files_present",
               all(p.is_file() for p in (man_p, seal_p, hand_p, close_p)), "manifest/seal/handoff/closeout"):
        return _receipt(w2_identity, rejected, reasons, checks, None, None)
    man = json.loads(man_p.read_text(encoding="utf-8"))
    seal = json.loads(seal_p.read_text(encoding="utf-8"))

    mism = []
    for f in man.get("files") or []:
        p = d / f["path"]
        if not p.is_file():
            mism.append((f["path"], "missing"))
        elif sha256_file(p) != f["sha256"]:
            mism.append((f["path"], "sha"))
    chk("evidence_manifest_recompute", not mism, mism[:5])
    seal_at_receive = sha256_file(man_p)
    chk("seal_manifest_binding", seal.get("evidence_manifest_sha256") == seal_at_receive,
        {"seal": seal.get("evidence_manifest_sha256"), "recomputed": seal_at_receive})
    chk("pack_pin", man.get("pack_manifest_sha256") == PACK_PIN, man.get("pack_manifest_sha256"))

    insp = None
    try:
        insp = reader.inspect_package(pack)
        chk("pack_inspect", insp["pack_manifest_sha256"] == PACK_PIN, insp["pack_manifest_sha256"])
        chk("pack_counts", insp["counts"] == {"pack_files": 5, "dev": 38, "ops": 29,
                                              "cases": 13, "assets": 26, "sources": 42,
                                              "holds": 14}, insp["counts"])
    except NFError as exc:
        chk("pack_inspect", False, f"{exc.token}:{exc.detail}")
        return _receipt(w2_identity, rejected, reasons, checks, None, None)

    text = hand_p.read_text(encoding="utf-8")
    for token in ("subject_id", "scope", "pack_manifest_sha256", "entry", "bridge",
                  "guide", "tpm", "consumer", "runner", "next", "stop", "resume"):
        chk("handoff_field:" + token, token in text, token)
    chk("handoff_scope", w2_identity.get("scope", "W1-NF-01") in text,
        w2_identity.get("scope"))

    cases = json.loads((d / "evidence" / "cases.json").read_text(encoding="utf-8"))
    verdicts = {c["case_id"]: c["verdict"] for c in cases["cases"]}
    chk("cases_present", len(verdicts) >= 20, len(verdicts))
    chk("host_consumed", verdicts.get("W1-HOST-01") == "PASS", verdicts.get("W1-HOST-01"))

    # negative handling: caller-controlled grant must never be honoured
    if w2_identity.get("permission_state") not in (None, "NONE_GRANTED"):
        chk("no_fake_grant", False, w2_identity.get("permission_state"))
    else:
        chk("no_fake_grant", True, "NONE_GRANTED")
    if w2_identity.get("expected_pack_sha256") and w2_identity["expected_pack_sha256"] != PACK_PIN:
        chk("caller_pack_pin", False, w2_identity["expected_pack_sha256"])
    else:
        chk("caller_pack_pin", True, PACK_PIN)

    next_op = ("W2-READ: consume W1 SourceRefs/EffectConstraints/HostCapabilityLedger, "
               "choose one READ/DRAFT task inside W2 scope")
    receipt = _receipt(w2_identity, rejected, reasons, checks, insp, cases)
    receipt["manifest_sha256_at_receive"] = seal_at_receive
    receipt["seal_evidence_manifest_sha256_at_receive"] = seal.get("evidence_manifest_sha256")
    receipt["receipt_excluded_from_manifest"] = True
    receipt["next_operation"] = next_op if not rejected else None
    receipt["stop"] = "wrong candidate/pack/oracle/evidence/handoff/scope, or any fake grant"
    receipt["resume"] = "same subject+scope+pack pin typed receipt; re-verify ACL/principal"
    receipt["consumed"] = {
        "source_refs": len(insp["source_refs"]),
        "effect_constraints": {"permission_state": "NONE_GRANTED",
                               "unknown_effect": "FAIL_CLOSED"},
        "host_capability_ledger": "evidence/host/host_receipt.json",
        "context_sha256_source": "bridge_nf.render_agent_context",
        "change_cone": json.loads((d / "W1_CLOSURE_MATRIX.json").read_text(encoding="utf-8")
                                  ).get("verdict_counts", {})
        if (d / "W1_CLOSURE_MATRIX.json").is_file() else {},
        "unresolved_refs": len(insp["unresolved_refs"]),
        "nine_keys": "guide_nf.produce_nine_keys",
    }
    receipt["w2_task"] = {"kind": "READ", "action": "verify W1 candidate and select next op",
                          "readback": "all checks above",
                          "accepted": not rejected}
    return receipt


def _receipt(ident, rejected, reasons, checks, insp, cases):
    return {
        "schema": "FHS5.PLP.W2.ReceiveReceipt@1",
        "receiver": "w2_receiver (independent)",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "w2_identity": ident,
        "accepted": not rejected,
        "rejected_checks": rejected,
        "reasons": reasons,
        "checks": checks,
        "check_count": len(checks),
        "permission_boundary": "W2 receives evidence only; no grant issued, no protected effect",
        "pack_manifest_sha256": (insp or {}).get("pack_manifest_sha256"),
        "w1_claim_seen": "W1_PARTIAL_VALIDATED" if any(
            "W1_PARTIAL_VALIDATED" in str(r) for r in reasons) else "see CLOSEOUT",
    }


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--delivery", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scope", default="W1-NF-01")
    ap.add_argument("--expect-pack-sha", default=None)
    args = ap.parse_args(argv)
    ident = {"subject_id": "FHS-5_PLP/W1/CONTROL_PACK", "scope": args.scope,
             "permission_state": "NONE_GRANTED",
             "expected_pack_sha256": args.expect_pack_sha}
    r = receive(Path(args.delivery), ident)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"accepted": r["accepted"], "checks": r["check_count"],
                      "rejected": r["rejected_checks"][:5],
                      "next": r.get("next_operation")}, ensure_ascii=False))
    return 0 if r["accepted"] else 5


if __name__ == "__main__":
    raise SystemExit(main())
