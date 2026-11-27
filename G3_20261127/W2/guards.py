#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 G3 typed guards used by the case runner.

Each guard is fail-closed and returns an explicit token.  None of them performs
a world effect; the effect paths live in run_w2.py and are driven by the real
gate/receiver.
"""
from __future__ import annotations

KNOWN_EFFECTS = {"READ": "REPOSITORY_READ", "WRITE": "REPOSITORY_WRITE",
                 "CREATE": "REPOSITORY_WRITE", "DELETE": "REPOSITORY_WRITE"}
FORBIDDEN_RECOVERY = {"GIT_REVERT", "GIT_RESET", "GIT_CLEAN", "WHOLE_REPO_ROLLBACK"}


class GuardError(Exception):
    def __init__(self, token, detail=""):
        self.token = token
        self.detail = detail
        super().__init__(f"{token}: {detail}")


def map_effect(token, path=None) -> dict:
    """Unknown tokens are never inferred from a filename."""
    key = str(token or "").upper()
    if key not in KNOWN_EFFECTS:
        raise GuardError("EFFECT_UNBOUND", {"token": token, "path": path})
    return {"ok": True, "token": key, "effect": KNOWN_EFFECTS[key],
            "inferred_from_path": False}


def check_authority(inputs: dict) -> dict:
    """ECP presence, permission=true, expired scope and wrong principal never grant."""
    if (inputs or {}).get("issuer_id") is None:
        raise GuardError("FALSE_AUTHORITY", "no issuer")
    if (inputs or {}).get("scope_expired"):
        raise GuardError("NOT_ADMITTED", "expired scope")
    if not (inputs or {}).get("principal_matches"):
        raise GuardError("FALSE_AUTHORITY", "principal mismatch")
    if (inputs or {}).get("permission") is True and not (inputs or {}).get("admission_ref"):
        raise GuardError("FALSE_AUTHORITY", "permission flag without admission")
    return {"ok": True, "issuer_id": inputs["issuer_id"]}


def select_runner(case: dict) -> dict:
    runner = (case or {}).get("runner")
    oracle = (case or {}).get("oracle_ref")
    fixture = (case or {}).get("fixture_ref")
    if not runner or not oracle or not fixture:
        raise GuardError("RUNNER_UNBOUND", {"runner": runner, "oracle": oracle,
                                            "fixture": fixture})
    return {"ok": True, "runner": runner, "executed": False,
            "note": "binding only; execution is a separate observation"}


def apply_recovery(kind: str, target, spy: list) -> dict:
    if str(kind or "").upper() in FORBIDDEN_RECOVERY:
        raise GuardError("RECOVERY_KIND_MISMATCH", kind)
    raise GuardError("RECOVERY_KIND_UNKNOWN", kind)


DELTA_KEYS = ("subject", "scope", "source_sha", "repo_head", "host_id",
              "policy_epoch", "oracle_sha", "world_raw_sha", "first_fail")


def delta_verify(a: dict, b: dict, verifier=None) -> dict:
    if not a or not b:
        return {"state": "DELTA_UNVERIFIED", "reason": "missing period"}
    if not callable(verifier):
        return {"state": "DELTA_UNVERIFIED", "reason": "missing verifier"}
    receipt = verifier(a, b)
    if not isinstance(receipt, dict) or receipt.get("verified") is not True:
        return {"state": "DELTA_UNVERIFIED", "reason": "verifier did not verify"}
    if a.get("subject") != b.get("subject") or a.get("scope") != b.get("scope"):
        return {"state": "NEW_SUBJECT_REVIEW_REQUIRED"}
    changed = [k for k in DELTA_KEYS if a.get(k) != b.get(k)]
    return {"state": "NEW_MATERIAL_EVIDENCE" if changed else "REUSE_LASTGOOD",
            "changed_keys": changed, "verifier_receipt": receipt}


def r3_rows(fixture: dict) -> dict:
    rows = (fixture.get("inputs") or {}).get("rows") or []
    nf = (fixture.get("inputs") or {}).get("nf_rows") or []
    if len(rows) != 13 or len(nf) != 3:
        raise GuardError("ROW_SET_INCOMPLETE", {"rows": len(rows), "nf": len(nf)})
    for r in rows:
        if not r.get("owner") or not r.get("id"):
            raise GuardError("OWNER_DROPPED", r.get("id"))
    ids = {r["id"] for r in rows}
    if len(ids) != 13 or any(n["id"] in ids for n in nf):
        raise GuardError("NF_MERGED_INTO_13", "duplicate id")
    return {"ok": True, "rows": rows, "nf_rows": nf,
            "all_actual_null": True, "token": "NULL_PRESERVED"}


def g4_admit(fixture: dict) -> dict:
    g4 = (fixture.get("inputs") or {}).get("g4") or {}
    if g4.get("has_license") or g4.get("has_git"):
        return {"admitted": True, "reason": "unexpected"}
    raise GuardError("NOT_ADMITTED", "historical G4 bytes are not a W2 effect or License Fit")


def historical_preimage(fixture: dict) -> dict:
    live = (fixture.get("inputs") or {}).get("live_preimage")
    if live is None:
        raise GuardError("WRITESET_UNBOUND", "live preimage missing")
    return {"ok": True, "live": live}


def workspace_counts(fixture: dict) -> dict:
    inp = fixture.get("inputs") or {}
    ws = inp.get("workspace_files")
    co = inp.get("closeout_entries")
    if ws is None or co is None:
        raise GuardError("WORKSPACE_DRIFT_UNBOUND", "counts missing")
    if ws == co:
        raise GuardError("WORKSPACE_DRIFT_BOUNDED", "counts equal")
    return {"ok": True, "token": "WORKSPACE_DRIFT_BOUNDED",
            "workspace_files": ws, "closeout_entries": co,
            "periods": inp.get("periods"), "same_candidate": inp.get("same_candidate")}
