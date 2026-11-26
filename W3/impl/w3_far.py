#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAR typed retrieval (RQ0-RQ4), five states, EvidenceGraph and RCA (RQ5-RQ8).

Providers are real local reads or declared unavailable roots. An unreachable
provider is never reported as zero. FAR never writes a subject/host and never
emits a WorkOrder/Grant/Release.
"""
from __future__ import annotations

import os
import re
import time
from pathlib import Path

from w3_common import (
    FAR_STATES,
    HYPOTHESES,
    W3Error,
    is_within,
    sha256_file,
)


def query_dir(provider_id, root, pattern, allowed_roots, scope="W3-NF-01", limit=50):
    start = time.time()
    rec = {
        "provider_id": provider_id,
        "query": pattern,
        "root": str(root),
        "scope": scope,
        "attempted": True,
        "reachable": None,
        "denominator": None,
        "rows": None,
        "zero_results": None,
        "state": None,
        "freshness": "FRESH_LOCAL_ENUMERATION",
        "independence": "LOCAL_PROCESS_NOT_FABRIC",
        "start": round(start, 3),
    }
    if root is None or not os.path.exists(root):
        rec.update(state="UNAVAILABLE", reachable=False, rows=None, zero_results=None,
                   reason="root_absent")
        rec["end"] = round(time.time(), 3)
        return rec
    if allowed_roots and not any(is_within(a, root) for a in allowed_roots):
        rec.update(state="BLOCKED_BY_AUTHORITY", reachable=True, rows=None, zero_results=None,
                   reason="outside_allowed_roots")
        rec["end"] = round(time.time(), 3)
        return rec
    try:
        rx = re.compile(pattern)
    except re.error as exc:
        rec.update(state="ERROR", reachable=True, rows=None, zero_results=None,
                   reason="bad_query:" + type(exc).__name__)
        rec["end"] = round(time.time(), 3)
        return rec
    try:
        hits = []
        denominator = 0
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in (".git", "__pycache__"))
            for name in sorted(filenames):
                denominator += 1
                if rx.search(name):
                    if len(hits) < limit:
                        hits.append(os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/"))
        rec.update(state="HIT" if hits else "ZERO_RELEVANT_HIT", reachable=True,
                   denominator=denominator, rows=len(hits) if hits else 0,
                   zero_results=None if hits else 0, sample=hits)
    except Exception as exc:
        rec.update(state="ERROR", reachable=True, rows=None, zero_results=None,
                   reason=type(exc).__name__)
    rec["end"] = round(time.time(), 3)
    return rec


def validate_injected_claim(claim):
    """An injected HIT with zero_results=0 is not evidence."""
    state = (claim or {}).get("state")
    zero = (claim or {}).get("zero_results")
    if state == "HIT" and zero == 0:
        return {
            "accepted": False,
            "token": "RESEARCH_REQUIRED",
            "reason": "a zero-result claim cannot be labelled HIT",
            "normalized_state": "ZERO_RELEVANT_HIT",
        }
    if state in FAR_STATES:
        return {"accepted": True, "token": "CLAIM_STATE_TYPED", "normalized_state": state}
    return {"accepted": False, "token": "CLAIM_UNBOUND", "normalized_state": None}


def evidence_graph(findings, providers, decision_question):
    nodes = []
    edges = []
    for f in findings:
        nodes.append({"id": f["id"], "kind": "Finding", "raw_sha256": f.get("raw_sha256")})
        edges.append({"from": f["id"], "to": f["case_id"], "type": "OBSERVED_IN"})
        edges.append({"from": f["id"], "to": f.get("requirement_refs", ["TRACE_UNBOUND"])[0], "type": "REQUIREMENT"})
    for p in providers:
        nodes.append({"id": "PROVIDER:" + p["provider_id"], "kind": "Provider",
                      "state": p["state"], "denominator": p.get("denominator")})
        edges.append({"from": decision_question["id"], "to": "PROVIDER:" + p["provider_id"], "type": "RETRIEVES"})
    rq = []
    rq.append({"rq": "RQ0", "question": "identity/scope/source join", "answer": "BOUND",
               "evidence": ["05_W3_SOURCE_MANIFEST.json", "EXTERNAL_SEAL.json"]})
    rq.append({"rq": "RQ1", "question": "what failed, with raw", "answer": "BOUND",
               "evidence": [f["id"] for f in findings]})
    rq.append({"rq": "RQ2", "question": "is the code path present", "answer": "BOUND",
               "evidence": [p["provider_id"] for p in providers if p["state"] == "HIT"]})
    rq.append({"rq": "RQ3", "question": "is the binding/host actually served", "answer": "UNBOUND",
               "evidence": [p["provider_id"] for p in providers if p["state"] == "UNAVAILABLE"]})
    rq.append({"rq": "RQ4", "question": "denominator and coverage", "answer": "BOUND",
               "evidence": [f"{p['provider_id']}:{p.get('denominator')}" for p in providers]})
    return {
        "schema": "FHS5.PLP.W3.FARRetrievalGraph@1",
        "decision_question": decision_question,
        "rq0_4": rq,
        "nodes": nodes,
        "edges": edges,
        "providers": providers,
        "states_seen": sorted({p["state"] for p in providers}),
        "state_enum": FAR_STATES,
        "claim": "TYPED_RETRIEVAL_ONLY",
    }


def rca(finding, providers, alternatives):
    """RQ5-RQ8: hypothesis, counterevidence, alternatives, advice."""
    hit = [p for p in providers if p["state"] == "HIT"]
    unavailable = [p for p in providers if p["state"] == "UNAVAILABLE"]
    hypothesis = "H-CODE-EXISTS-BINDING-MISSING" if hit else "H-RESEARCH_SOURCE_UNAVAILABLE"
    if finding.get("class") == "SECURITY_AUTHORIZATION":
        hypothesis = "H-AUTHORITY_UNBOUND"
    return {
        "rq5": {"hypothesis": hypothesis, "support": [p["provider_id"] for p in hit],
                "counterevidence": [p["provider_id"] for p in unavailable],
                "nofit": [h for h in HYPOTHESES if h != hypothesis][:4]},
        "rq6": {"root_cause_state": "CANDIDATE_NOT_CONFIRMED",
                "change_cone": finding.get("change_cone", []),
                "confirmed_by": finding.get("raw_sha256")},
        "rq7": {"alternatives": alternatives,
                "substantive_count": len(alternatives),
                "fit_nofit_present": all(a.get("fit") and a.get("nofit") for a in alternatives)},
        "rq8": {"advice_is_grant": False,
                "work_order_emitted": False,
                "release_emitted": False},
    }
