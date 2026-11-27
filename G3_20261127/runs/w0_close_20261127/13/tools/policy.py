#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed policy functions used by the W0 TQAEP scenarios.

Each function returns a JSON-able dict with an explicit exit code and status.
They are intentionally small: the W0 point is demonstrable refusal behaviour,
not a new service or registry.
"""
from __future__ import annotations

import json
import re

KNOWN_EFFECTS = {
    "SOURCE_READ": "admitted",
    "DEV_WRITE": "admitted_with_writeset",
    "LOCAL_CLI_RUN": "admitted",
    "REVERSIBLE_OUTPUT_WRITE": "admitted_with_output_root",
    "OUTPUT_RESTORE": "admitted",
}


def authority_gate(receipt: dict) -> dict:
    """A self-declared permit/ID is not authority."""
    if receipt.get("permit") is True and not receipt.get("grant_ref"):
        return {"exit": 3, "status": "FALSE_AUTHORITY", "admitted": False, "noop": True}
    if receipt.get("original_reader_ack") and not receipt.get("reader_adapter_pin"):
        return {"exit": 3, "status": "FALSE_AUTHORITY", "admitted": False, "noop": True}
    if not receipt.get("grant_ref"):
        return {"exit": 3, "status": "NOT_ADMITTED", "admitted": False, "noop": True}
    return {"exit": 0, "status": "ADMITTED", "admitted": True, "noop": False}


def effect_resolve(alias: str) -> dict:
    if alias in KNOWN_EFFECTS:
        return {"exit": 0, "status": "MAPPED", "effect": alias, "disposition": KNOWN_EFFECTS[alias]}
    return {"exit": 3, "status": "EFFECT_MAPPING_UNVERIFIED", "effect": alias, "executed": False}


def dag_check(edges: list[tuple[str, str]], phases: dict[str, int]) -> dict:
    """Reject phase overreach (later phase required by an earlier one) and cycles."""
    for a, b in edges:
        if phases.get(a, 0) < phases.get(b, 0) and a.startswith(("W0", "W1")) and b.startswith("W4"):
            return {"exit": 3, "status": "PHASE_OVERREACH_CANDIDATE", "edge": [a, b], "legal_read": True}
    graph: dict[str, list[str]] = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
    color: dict[str, int] = {}

    def dfs(n: str) -> list[str] | None:
        color[n] = 1
        for m in graph.get(n, []):
            if color.get(m) == 1:
                return [n, m]
            if color.get(m, 0) == 0:
                got = dfs(m)
                if got:
                    return got
        color[n] = 2
        return None

    for n in list(graph):
        if color.get(n, 0) == 0:
            cyc = dfs(n)
            if cyc:
                return {"exit": 3, "status": "GATE_CYCLE_CANDIDATE", "cycle_edge": cyc,
                        "executed": False}
    return {"exit": 0, "status": "DAG_OK", "edges": len(edges)}


def schema_validate(obj: dict, schema_version: str) -> dict:
    if obj.get("schema_version") != schema_version:
        return {"exit": 3, "status": "SCHEMA_UNSUPPORTED",
                "observed": obj.get("schema_version"), "supported": schema_version}
    required = {"schema_version", "sources", "crosswalk"}
    missing = sorted(required - set(obj))
    if missing:
        return {"exit": 3, "status": "SCHEMA_UNSUPPORTED", "missing": missing}
    return {"exit": 0, "status": "SCHEMA_OK"}


def verify_semantics(exit_code: int, payload: dict | None, expected: dict) -> dict:
    if payload is None:
        return {"exit": 3, "status": "EFFECT_NOT_VERIFIED", "reason": "unparseable stdout"}
    problems = []
    if exit_code != expected["exit"]:
        problems.append(f"exit {exit_code} != {expected['exit']}")
    if payload.get("status") != expected["status"]:
        problems.append(f"status {payload.get('status')} != {expected['status']}")
    for key in ("provided", "missing"):
        if key in expected and payload.get(key) != expected[key]:
            problems.append(f"{key} {payload.get(key)} != {expected[key]}")
    if problems:
        return {"exit": 3, "status": "EFFECT_NOT_VERIFIED", "problems": problems}
    return {"exit": 0, "status": "EFFECT_VERIFIED"}


def receipt_validate(rec: dict) -> dict:
    need = ["case_id", "candidate_sha", "cwd", "argv", "exit", "stdout_sha",
            "expected", "observed", "verdict"]
    missing = [k for k in need if rec.get(k) in (None, "", [], {})]
    if missing:
        return {"exit": 3, "status": "UNREPRODUCED", "missing": missing}
    return {"exit": 0, "status": "REPRODUCIBLE"}


def far_source_status(available: bool, query_hits: int | None) -> dict:
    if not available:
        return {"status": "UNAVAILABLE", "zero_results": None, "advice": "RESEARCH_REQUIRED"}
    if query_hits is None:
        return {"status": "UNKNOWN", "zero_results": None, "advice": "ABSTAIN"}
    return {"status": "HIT_LOCAL", "zero_results": query_hits == 0, "advice": "CONTINUE"}


def far_close(raw_sha: str | None, scope_ok: bool) -> dict:
    if not raw_sha:
        return {"exit": 3, "status": "FALSE_CLOSE", "reason": "no raw evidence"}
    if not scope_ok:
        return {"exit": 3, "status": "FALSE_CLOSE", "reason": "outside owner scope"}
    return {"exit": 0, "status": "CLOSE_PERMITTED"}


def delta_eval(old: dict, new: dict) -> dict:
    same = all(old.get(k) == new.get(k) for k in ("source", "candidate", "fixture", "oracle", "first_fail"))
    if same and old.get("raw_sha") == new.get("raw_sha"):
        return {"exit": 3, "status": "NO_DELTA_REWRITE_DENIED", "action": "HOLD"}
    return {"exit": 0, "status": "REQUALIFY", "action": "re-assess affected cone only"}


def retry_governor(attempts: list[str]) -> dict:
    if len(attempts) > 1 and len(set(attempts)) == 1:
        return {"exit": 3, "status": "NO_DELTA_REWRITE_DENIED",
                "allowed_attempts": 1, "held": True}
    return {"exit": 0, "status": "RETRY_ALLOWED"}


def release_gate(checker: dict | None, publisher: dict | None) -> dict:
    if not checker:
        return {"exit": 0, "status": "CLOSEOUT_ADVICE", "release": "RELEASE_NOT_CLAIMED",
                "reason": "no independent checker receipt"}
    if not publisher:
        return {"exit": 0, "status": "CLOSEOUT_ADVICE", "release": "RELEASE_NOT_CLAIMED",
                "reason": "no publisher signature"}
    return {"exit": 0, "status": "RELEASE_CANDIDATE", "release": "PENDING_PUBLISHER"}


def profile_gate(profile: str, ids_present: set[str], required: set[str], full_485: bool) -> dict:
    if profile == "GENERIC":
        return {"exit": 0, "status": "GENERIC_OK", "full_485": "DEFER"}
    missing = sorted(required - ids_present)
    if missing:
        return {"exit": 3, "status": "PROFILE_GATE_DRIFT", "missing_ids": missing[:5],
                "full_485": "DEFER"}
    return {"exit": 0, "status": "PROFILE_OK", "full_485": "DEFER" if not full_485 else "RUN"}


SECRET = re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{16,}")


def secret_scan(text: str) -> dict:
    hits = bool(SECRET.search(text))
    redacted = SECRET.sub("[REDACTED]", text)
    return {
        "exit": 3 if hits else 0,
        "status": "SECRET_LEAK" if hits else "CLEAN",
        "redacted_contains_secret": bool(SECRET.search(redacted)),
        "raw_public_sha_allowed": not hits,
    }


def unknown_schema_roundtrip(obj: dict) -> dict:
    """Unknown required field must be preserved, not silently dropped."""
    dumped = json.loads(json.dumps(obj))
    unknown = sorted(set(dumped) - {"schema_version", "sources", "crosswalk", "profile"})
    return {"exit": 0 if unknown else 3, "status": "PRESERVED" if unknown else "SCHEMA_UNSUPPORTED",
            "unknown_fields": unknown}
