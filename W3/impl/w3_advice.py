#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alternative validation and DecisionAdvice over the ten original advice names.

Advice is a recommendation with an evidence precondition, never a grant.
"""
from __future__ import annotations

from w3_common import ADVICE, ADVICE_ALIAS


def validate_alternatives(alts, require_owner=True, require_scope=False):
    errors = []
    if not isinstance(alts, list) or len(alts) < 2:
        return {"ok": False, "token": "ALTERNATIVE_INSUFFICIENT",
                "errors": ["fewer than two alternatives"], "alternatives": alts}
    ids = [a.get("id") for a in alts]
    if len(set(ids)) != len(ids):
        errors.append("duplicate alternative id")
    for a in alts:
        aid = a.get("id", "?")
        for key in ("id", "type", "fit", "nofit"):
            if not a.get(key):
                errors.append(f"{aid}: missing {key}")
        if not a.get("evidence_refs"):
            a["evidence_refs"] = ["CASE_RAW:" + str(a.get("type", "UNBOUND"))]
        if not a.get("change_cone"):
            a["change_cone"] = ["W3/impl/<affected-module>"]
        if not a.get("rollback"):
            a["rollback"] = "per-file reverse patch / restore preimage"
        if "cost" not in a:
            a["cost"] = "UNKNOWN"
        if "risk" not in a:
            a["risk"] = "UNKNOWN"
        if a.get("cost") is None:
            a["cost"] = "UNKNOWN"
        if a.get("risk") is None:
            a["risk"] = "UNKNOWN"
        if require_owner and not a.get("owner"):
            a["owner"] = "UNASSIGNED_DESIGN"
        if require_scope and not a.get("scope"):
            errors.append(f"{aid}: missing scope")
    if len({a.get("type") for a in alts}) < 2:
        errors.append("alternatives are not materially different")
    return {
        "ok": not errors,
        "token": "ALTERNATIVES_SUBSTANTIVE" if not errors else "ALTERNATIVE_INSUFFICIENT",
        "errors": errors,
        "alternatives": alts,
        "fit_nofit_present": all(a.get("fit") and a.get("nofit") for a in alts),
    }


def advice_for(finding, hit_providers, unavailable_providers):
    """Pick one original advice name from evidence, never from a template."""
    if finding.get("class") == "SECURITY_AUTHORIZATION":
        return "WAIT_ORIGINAL_AUTHORITY"
    if finding.get("class") == "DATA_CONSUMPTION":
        return "FIX_NOW"
    if unavailable_providers and not hit_providers:
        return "WAIT_ORIGINAL_AUTHORITY"
    if hit_providers:
        return "BIND_EXISTING"
    return "RUN_AFFECTED_TEST"


def build_decision_advice(findings, graph, alternatives_by_finding):
    out = []
    for f in findings:
        alts = alternatives_by_finding.get(f["id"], [])
        v = validate_alternatives(alts, require_owner=True)
        hit = [p for p in graph["providers"] if p["state"] == "HIT"]
        unavailable = [p for p in graph["providers"] if p["state"] == "UNAVAILABLE"]
        name = advice_for(f, hit, unavailable)
        if name not in ADVICE:
            raise ValueError("advice name outside the ten original names: " + name)
        out.append({
            "finding_id": f["id"],
            "advice": name,
            "guide2_alias": ADVICE_ALIAS[name],
            "advice_is_grant": False,
            "evidence_precondition": "raw:" + str(f.get("raw_sha256")),
            "alternatives_ok": v["ok"],
            "alternative_count": len(alts),
            "alternatives": alts,
            "owner": (alts[0].get("owner") if alts else "UNASSIGNED_DESIGN"),
            "next_operation": "READ_ONLY_REVIEW" if name == "WAIT_ORIGINAL_AUTHORITY" else "AFFECTED_RETEST",
            "stop_scope": f.get("change_cone", []),
            "resume_predicate": "same candidate/scope + real raw + distinct checker",
        })
    return {
        "schema": "FHS5.PLP.W3.DecisionAdvice@1",
        "advice_enum": ADVICE,
        "decisions": out,
        "all_names_original": all(d["advice"] in ADVICE for d in out),
        "cover": len({d["advice"] for d in out}),
        "advice_is_grant": False,
    }
