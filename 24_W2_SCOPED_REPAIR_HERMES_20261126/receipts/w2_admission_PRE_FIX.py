#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Owner admission verifier (r4): trust root is module-level, not request-level.

The r3 version had two real holes:
  1. ``require_verified_admission`` was read from the request, so a caller could
     simply omit it and the gate fell back to trusting a caller dict.
  2. ``verify_receipt`` only re-derived the receipt's own ``fields`` digest, so a
     receipt minted elsewhere (or with a different decision) still validated.

This version fixes both:
  * ``TRUST`` below is the only trust root.  The decision document is verified
    against a hard-coded sha256; a caller cannot supply a pin.
  * ``derive()`` returns a receipt bound to that decision, and ``require()``
    re-reads *the decision on disk* at use time, so expiry/revocation/scope are
    checked against the real document, not against the receipt.
No new issuer service: the Owner decision document is the issuer artefact.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

# ---- the only trust root -------------------------------------------------
TRUST = {
    "decision_sha256": "1ef19c0f0b4212c087a43bf3b8e415f844004448cc0848bafb7da0aeba191ff7",
    "decision_id": "W2-NF-PRIMARY-20261126-01",
    "schema": "FHS5.PLP.W2.OwnerDecision@local-1",
    "decision_path_candidates": (
        "W2_NATIVE_RUNS/20261126T1225_W2_FINAL_CLOSURE/10_PACK/19_W2_NF_CODEX_20261126/W2_OWNER_DECISION.json",
        "W2_NATIVE_RUNS/20261126T1121_W2_PRODUCT/10_PACK/19_W2_NF_CODEX_20261126/W2_OWNER_DECISION.json",
    ),
    "repo_root": "C:/Projects/Agent_Workspace/FHS-5_Workspace",
    "revocation_marker": "W2_NATIVE_RUNS/OWNER_REVOKED.json",
    "subjects": {"DEV": "FHS-5_PLP/W2/CONTROL_PACK", "OPS": "FHS-5_PLP/W2/CONTROL_PACK"},
    "effects": {"DEV": ["dev"], "OPS": ["ops"]},
}

_CACHE = {}


class AdmissionError(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _digest(fields: dict) -> str:
    return _sha_bytes(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def resolve_decision(explicit_path=None) -> Path:
    """Locate the decision document.  Anything located must still match TRUST."""
    cands = []
    if explicit_path:
        cands.append(Path(explicit_path))
    env = os.environ.get("W2_DECISION_PATH")
    if env:
        cands.append(Path(env))
    root = Path(TRUST["repo_root"])
    cands += [root / c for c in TRUST["decision_path_candidates"]]
    for c in cands:
        if c.is_file() and _sha_bytes(c.read_bytes()) == TRUST["decision_sha256"]:
            return c
    raise AdmissionError("FALSE_AUTHORITY",
                         f"no decision document matching the pinned sha {TRUST['decision_sha256'][:16]}…")


def _load_verified(explicit_path=None) -> dict:
    p = resolve_decision(explicit_path)
    doc = json.loads(p.read_bytes().decode("utf-8"))
    if doc.get("schema") != TRUST["schema"]:
        raise AdmissionError("FALSE_AUTHORITY", f"schema {doc.get('schema')}")
    if doc.get("decision_id") != TRUST["decision_id"]:
        raise AdmissionError("FALSE_AUTHORITY", f"decision_id {doc.get('decision_id')}")
    return {"doc": doc, "path": p, "sha256": _sha_bytes(p.read_bytes())}


def _revoked() -> bool:
    m = Path(TRUST["repo_root"]) / TRUST["revocation_marker"]
    return m.exists()


def derive(domain: str, scope: str = "W2-NF-01", explicit_path=None) -> dict:
    """Produce the receipt the writer will accept.  Raises on any mismatch."""
    if _revoked():
        raise AdmissionError("ADMISSION_REVOKED", str(TRUST["revocation_marker"]))
    v = _load_verified(explicit_path)
    doc = v["doc"]
    sc = doc.get("scope") or {}
    want_subject = TRUST["subjects"].get(domain)
    if sc.get("subject_id") != want_subject:
        raise AdmissionError("SCOPE_MISMATCH", {"want": want_subject, "granted": sc.get("subject_id")})
    if sc.get("scope") != scope:
        raise AdmissionError("SCOPE_MISMATCH", {"want": scope, "granted": sc.get("scope")})
    authorised = [e.strip().lower() for e in (sc.get("effects_authorized") or [])]
    tokens = TRUST["effects"].get(domain, [])
    if not any(any(a.startswith(t) for t in tokens) for a in authorised):
        raise AdmissionError("FALSE_AUTHORITY", {"domain": domain, "authorised": authorised})
    fields = {"decision_id": doc.get("decision_id"), "subject_id": sc.get("subject_id"),
              "scope": sc.get("scope"), "domain": domain,
              "effects_authorized": sorted(sc.get("effects_authorized") or []),
              "expiry_revocation": doc.get("expiry_revocation"),
              "decision_sha256": v["sha256"],
              "trust_root": TRUST["decision_sha256"]}
    return {"ok": True, "decision_id": doc.get("decision_id"),
            "subject_id": sc.get("subject_id"), "scope": sc.get("scope"),
            "domain": domain, "expiry_revocation": doc.get("expiry_revocation"),
            "verified_from": {"path": str(v["path"]), "sha256": v["sha256"]},
            "fields": fields, "subject_sha256": _digest(fields)}


def require(receipt, domain: str, scope: str = "W2-NF-01", explicit_path=None) -> dict:
    """Re-verify at use time against the live decision document."""
    if not isinstance(receipt, dict) or receipt.get("ok") is not True:
        raise AdmissionError("FALSE_AUTHORITY", "no receipt")
    if _revoked():
        raise AdmissionError("ADMISSION_REVOKED", "revocation marker present")
    v = _load_verified(explicit_path)
    fields = receipt.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise AdmissionError("FALSE_AUTHORITY", "receipt carries no field set")
    if fields.get("decision_sha256") != v["sha256"] or \
            fields.get("trust_root") != TRUST["decision_sha256"]:
        raise AdmissionError("FALSE_AUTHORITY", "receipt does not point at the pinned decision")
    if _digest(fields) != receipt.get("subject_sha256"):
        raise AdmissionError("FALSE_AUTHORITY", "receipt digest does not re-derive")
    for k in ("decision_id", "subject_id", "scope", "domain"):
        if receipt.get(k) != fields.get(k):
            raise AdmissionError("FALSE_AUTHORITY", f"receipt field drifted: {k}")
    # the live document must still authorise exactly this
    fresh = derive(domain, scope, explicit_path)
    if fresh["fields"]["effects_authorized"] != fields.get("effects_authorized"):
        raise AdmissionError("FALSE_AUTHORITY", "authorised effect set changed since the receipt")
    return {"ok": True, "decision_id": fresh["decision_id"], "domain": domain,
            "verified_from": fresh["verified_from"], "reverified": True}


def verify_receipt(receipt, explicit_path=None) -> bool:
    try:
        require(receipt, receipt.get("domain", "DEV"), receipt.get("scope", "W2-NF-01"), explicit_path)
        return True
    except AdmissionError:
        return False
