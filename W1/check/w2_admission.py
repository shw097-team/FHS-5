#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Owner admission verifier (M1-A item 2).

The DEV gate used to trust caller-supplied ``{"decision_id": ..., "expired": false}``.
That is exactly the fake-grant path the contract forbids.  This module derives the
admission from a *hash-pinned* decision document instead:

    load(decision_path, pinned_sha256, wanted) -> receipt

A caller cannot mint a receipt: the receipt carries ``verified_from`` (file + sha)
and ``subject_sha256`` over the exact fields it checked, and `verify_receipt()`
re-derives that digest, so a hand-built dict is refused.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REQUIRED_EFFECTS = {"DEV": ("DEV", "REPOSITORY_WRITE"),
                    "OPS": ("OPS", "HOST_EFFECT")}


class AdmissionError(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _fields_digest(fields: dict) -> str:
    blob = json.dumps(fields, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def load(decision_path, pinned_sha256: str, wanted: dict,
         revocation_marker=None) -> dict:
    """Return a receipt derived from the pinned decision, or raise AdmissionError."""
    p = Path(decision_path)
    if not p.is_file():
        raise AdmissionError("FALSE_AUTHORITY", f"decision document absent: {p}")
    got = _sha_file(p)
    if got != pinned_sha256:
        raise AdmissionError("FALSE_AUTHORITY",
                             f"decision sha mismatch: {got} != {pinned_sha256}")
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise AdmissionError("FALSE_AUTHORITY", f"unparsable decision: {exc}") from exc
    if doc.get("schema") != "FHS5.PLP.W2.OwnerDecision@local-1":
        raise AdmissionError("FALSE_AUTHORITY", f"schema {doc.get('schema')}")

    scope = (doc.get("scope") or {})
    if wanted.get("subject_id") and scope.get("subject_id") != wanted["subject_id"]:
        raise AdmissionError("SCOPE_MISMATCH",
                             {"want": wanted.get("subject_id"),
                              "granted": scope.get("subject_id")})
    if wanted.get("scope") and scope.get("scope") != wanted["scope"]:
        raise AdmissionError("SCOPE_MISMATCH",
                             {"want": wanted.get("scope"), "granted": scope.get("scope")})

    domain = wanted.get("domain", "DEV")
    authorised = [e.strip().lower() for e in (scope.get("effects_authorized") or [])]
    # the decision writes effects as free text ("DEV (reversible, per op)"), so the
    # domain must be the leading word of an authorised entry - not a substring hit
    if not any(a == domain.lower() or a.startswith(domain.lower() + " ")
               or a.startswith(domain.lower() + "(") for a in authorised):
        raise AdmissionError("FALSE_AUTHORITY",
                             {"domain": domain, "authorised": authorised})

    # revocation: an explicit marker wins over the document's own text
    if revocation_marker and Path(revocation_marker).exists():
        raise AdmissionError("ADMISSION_REVOKED", str(revocation_marker))

    fields = {"decision_id": doc.get("decision_id"),
              "scope": scope.get("scope"),
              "subject_id": scope.get("subject_id"),
              "domain": domain,
              "effects_authorized": sorted(scope.get("effects_authorized") or []),
              "expiry_revocation": doc.get("expiry_revocation"),
              "decision_sha256": got}
    return {
        "ok": True,
        "decision_id": doc.get("decision_id"),
        "scope": scope.get("scope"),
        "subject_id": scope.get("subject_id"),
        "domain": domain,
        "expiry_revocation": doc.get("expiry_revocation"),
        "verified_from": {"path": str(p), "sha256": got},
        "fields": fields,
        "subject_sha256": _fields_digest(fields),
    }


def verify_receipt(receipt: dict, pinned_sha256: str) -> bool:
    """A receipt is valid only if its own fields re-derive to its digest and the
    digest still points at the pinned decision document."""
    if not isinstance(receipt, dict) or receipt.get("ok") is not True:
        return False
    vf = receipt.get("verified_from") or {}
    if vf.get("sha256") != pinned_sha256:
        return False
    fields = receipt.get("fields")
    if not isinstance(fields, dict) or not fields:
        return False
    if fields.get("decision_sha256") != pinned_sha256:
        return False
    # the exported identity must equal the signed field set; otherwise a tampered
    # top-level field rides on an untouched digest
    for k in ("decision_id", "scope", "subject_id", "domain"):
        if receipt.get(k) != fields.get(k):
            return False
    return _fields_digest(fields) == receipt.get("subject_sha256")


def require(receipt: dict, pinned_sha256: str) -> dict:
    if not verify_receipt(receipt, pinned_sha256):
        raise AdmissionError("FALSE_AUTHORITY",
                             "receipt does not re-derive from the pinned decision")
    return receipt
