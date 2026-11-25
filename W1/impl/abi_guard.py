#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 NF-r2 ABI guards (product code exercised by the case runner).

These guards are the product implementation of the ABI NEG cases; keeping them
here (instead of inside the runner) means a failing guard fails the product,
not just a local helper.
"""
from __future__ import annotations

import w1_nf_reader as base

NFError = base.NFError

REQUIRED_FIELDS = ("id", "goal", "effect", "resume")


def crosswalk_version_guard(src: str, dst: str, explicit_crosswalk: bool = False) -> dict:
    """W1-ABI-01: same version suffix alone never proves compatibility."""
    if "@" not in src or "@" not in dst:
        raise NFError("EXPLICIT_REVIEW_REQUIRED", f"{src}->{dst}")
    if src.rsplit("@", 1)[-1] == dst.rsplit("@", 1)[-1] and not explicit_crosswalk:
        raise NFError("EXPLICIT_REVIEW_REQUIRED", f"{src}->{dst}")
    return {"ok": True, "src": src, "dst": dst, "explicit_crosswalk": explicit_crosswalk}


def abi_completeness(obj: dict, required=REQUIRED_FIELDS) -> dict:
    """W1-ABI-02: a rename without a field crosswalk is lossy."""
    have = set((obj or {}).get("fields") or {})
    missing = [f for f in required if f not in have]
    if missing:
        raise NFError("LOSSY_MIGRATION", "missing " + ",".join(missing))
    if (obj or {}).get("unknown_fields"):
        raise NFError("LOSSY_MIGRATION", "unknown fields dropped")
    return {"ok": True, "fields": sorted(have)}


def require_effect_resume(obj: dict) -> dict:
    """W1-R3-03: an object without effect/dag/resume can not be 'complete'."""
    for key in ("dag", "effect", "resume"):
        if key not in (obj or {}):
            raise NFError("ABI_LOSSY_CROSSWALK", f"{key} missing")
    return {"ok": True}


def restore_claim_check(claim: dict) -> dict:
    """W1-R3-05: identity-only evidence can never restore content bytes."""
    if (claim or {}).get("identity_only") and not (claim or {}).get("content_bytes_available"):
        raise NFError("EVIDENCE_LAUNDERING", "identity-only cannot restore bytes")
    if not (claim or {}).get("content_bytes_available"):
        raise NFError("EVIDENCE_LAUNDERING", "no content bytes")
    return {"ok": True}
