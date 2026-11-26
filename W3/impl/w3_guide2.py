#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guide2: seven FAR keys + identity -> nine Guide keys, lossless, two periods.

Sources of truth:
  * W1 guide_nf.NINE_KEYS (read-only crosswalk check when importable)
  * 00_W3_PI_PD.md section 05.5
"""
from __future__ import annotations

import os

from w3_common import (
    NINE_KEYS,
    SEVEN_KEYS,
    SEVEN_TO_NINE,
    W3Error,
    canon,
    sha256_file,
)


def optional_w1_nine_keys():
    """Prove the crosswalk against W1's constant when its tree is available."""
    base = os.environ.get("W3_W1_REPO")
    if not base:
        return {"available": False, "match": None}
    path = os.path.join(base, "W1", "impl", "guide_nf.py")
    if not os.path.isfile(path):
        return {"available": False, "match": None}
    text = open(path, "r", encoding="utf-8").read()
    ok = all(('"' + k + '"') in text for k in NINE_KEYS)
    return {"available": True, "match": ok, "path": path, "sha256": sha256_file(path)}


def to_nine(identity, seven):
    missing = [k for k in ("subject", "scope") if not identity.get(k)]
    missing += [k for k in SEVEN_KEYS if seven.get(k) in (None, "")]
    if missing:
        raise W3Error("DELTA_UNVERIFIED", "missing keys: " + ",".join(missing))
    nine = {"subject": identity["subject"], "scope": identity["scope"]}
    for k in SEVEN_KEYS:
        nine[SEVEN_TO_NINE[k]] = seven[k]
    if set(nine) != set(NINE_KEYS):
        raise W3Error("HANDOFF_LOSS", "nine-key set mismatch")
    return nine


def _verify_receipts(period):
    receipts = period.get("receipts") or {}
    out = {}
    for key in NINE_KEYS:
        r = receipts.get(key)
        if key in ("subject", "scope"):
            out[key] = {"verified": True, "kind": "identity"}
            continue
        if not r or not r.get("ref"):
            out[key] = {"verified": False, "reason": "receipt_missing"}
            continue
        ref = r["ref"]
        if not os.path.isfile(ref):
            out[key] = {"verified": False, "reason": "receipt_file_missing"}
            continue
        got = sha256_file(ref)
        out[key] = {"verified": got == r.get("sha256"), "ref": ref, "sha256": got}
    return out


def reconcile(periods, verifier_receipt=None, declared_single_sha=None):
    if declared_single_sha:
        return {"state": "DELTA_UNVERIFIED", "reason": "single_evidence_sha is not a delta"}
    if not periods or len(periods) < 2:
        return {"state": "DELTA_UNVERIFIED", "reason": "fewer than two periods"}
    if any(p.get("caller_verified") for p in periods):
        return {"state": "DELTA_UNVERIFIED", "reason": "caller boolean is not verification"}
    if not verifier_receipt or verifier_receipt.get("verified") is not True:
        return {"state": "DELTA_UNVERIFIED", "reason": "trusted verifier receipt missing"}
    keys = []
    checks = []
    for p in periods[:2]:
        try:
            k = to_nine(p.get("identity") or {}, p.get("seven") or {})
        except W3Error as exc:
            return {"state": "DELTA_UNVERIFIED", "reason": str(exc)}
        checks.append(_verify_receipts(p))
        keys.append(k)
    bad = [(i, key) for i, chk in enumerate(checks) for key, v in chk.items() if not v.get("verified")]
    if bad:
        return {"state": "DELTA_UNVERIFIED", "reason": "unverified key receipts",
                "bad": [f"p{i}:{k}" for i, k in bad]}
    copied = []
    for key in NINE_KEYS:
        if key in ("subject", "scope"):
            continue
        s1 = (checks[0].get(key) or {}).get("sha256")
        s2 = (checks[1].get(key) or {}).get("sha256")
        if s1 and s1 == s2:
            copied.append(key)
    if copied:
        return {"state": "DELTA_UNVERIFIED", "reason": "copied receipt", "keys": copied}
    t1 = periods[0].get("observed_at")
    t2 = periods[1].get("observed_at")
    if not t1 or not t2 or t1 == t2:
        return {"state": "DELTA_UNVERIFIED", "reason": "two independent observations need distinct times"}
    a, b = keys
    if a["subject"] != b["subject"] or a["scope"] != b["scope"]:
        return {"state": "NEW_SUBJECT_REVIEW_REQUIRED", "before": a, "after": b,
                "changed_keys": []}
    changed = [k for k in NINE_KEYS if a[k] != b[k]]
    if changed:
        return {"state": "NEW_MATERIAL_EVIDENCE", "before": a, "after": b,
                "changed_keys": changed, "receipts": checks}
    return {"state": "PARK_NO_DELTA", "candidate": True, "before": a, "after": b,
            "changed_keys": [], "receipts": checks,
            "note": "PARK is a candidate, not an automatic close"}


def thin_resume(advice, delta_state, owner, pack_ref, claim_ceiling):
    return {
        "schema": "FHS5.PLP.W3.GuideThinResume@1",
        "mode": "FAR_ADVICE_TO_TOUCHPOINT_2",
        "pack_ref": pack_ref,
        "advice": advice.get("advice"),
        "advice_alias": advice.get("guide2_alias"),
        "material_delta": delta_state,
        "owner": owner,
        "next_operation": advice.get("next_operation"),
        "stop_scope": advice.get("stop_scope"),
        "resume_predicate": advice.get("resume_predicate"),
        "claim_ceiling": claim_ceiling,
        "advice_is_grant": False,
        "permission_state": "NONE_GRANTED",
    }


def nine_digest(nine):
    return canon(nine)
