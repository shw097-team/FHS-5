#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W1 G3 guards that are not already product code in W1/impl."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

INJECTION = re.compile(
    r"(ignore\s+(all\s+)?(previous\s+)?(permission|instruction)|grant\s+release|"
    r"system\s*:|<\s*script|rm\s+-rf|exfiltrat)", re.I)


class GuardError(Exception):
    def __init__(self, token, detail=""):
        self.token = token
        self.detail = detail
        super().__init__(f"{token}: {detail}")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def classify_untrusted(text: str) -> dict:
    """Mark an embedded instruction as source data; never execute or elevate."""
    hits = INJECTION.findall(text or "")
    if not hits:
        return {"token": "CLEAN", "marked": False, "executed": False,
                "elevated": False, "hits": []}
    return {"token": "UNTRUSTED_SOURCE_DATA", "marked": True, "executed": False,
            "elevated": False, "hits": [h[0] if isinstance(h, tuple) else h for h in hits],
            "text_sha256": sha256_bytes((text or "").encode("utf-8"))}


def hermes_three_children(children: dict) -> dict:
    """Kanban / Delegation / Swarm need three separate real observations."""
    need = ("kanban", "delegation", "swarm")
    have = {k: (children or {}).get(k) for k in need}
    missing = [k for k, v in have.items() if not v or not (v.get("raw") if isinstance(v, dict) else v)]
    merged = (children or {}).get("merged")
    if merged or missing:
        raise GuardError("REQUIRED_CHILD_MISSING", missing or ["merged"])
    return {"ok": True, "children": {k: have[k] for k in need}}


def workspace_drift(workspace_count: int, primary_count: int,
                    primary_hash_before: str, primary_hash_after: str) -> dict:
    if primary_hash_before != primary_hash_after:
        raise GuardError("PRIMARY_DRIFT", "primary changed")
    if workspace_count == primary_count:
        raise GuardError("WORKSPACE_DRIFT_BOUNDED", "counts equal; nothing bounded")
    return {"ok": True, "token": "WORKSPACE_DRIFT_BOUNDED",
            "workspace_count": workspace_count, "primary_count": primary_count,
            "primary_hash_stable": True}


def count_files(root: Path) -> int:
    return sum(1 for p in Path(root).rglob("*") if p.is_file())


def guide_two_periods(guide, period_a: dict, period_b: dict) -> dict:
    """Real nine-key reconciliation through the product verifier."""
    res = guide.reconcile_guide_delta(period_a, period_b,
                                      original_verifier=lambda a, b: a == b)
    return res
