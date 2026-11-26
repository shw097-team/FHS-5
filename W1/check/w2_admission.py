#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Owner admission verifier (r4b) — closes the findings the verifier raised.

F1  a valid receipt could write anywhere (decision allowed_roots is PENDING):
    derive()/require() now take repo_root + targets and refuse unless the root is
    an explicitly authorised one and every target stays inside it.
F2  expiry/revocation was copied as a string and never evaluated:
    _evaluate_expiry() parses the clause and refuses EXPIRED_<date> / REVOKED.
F3  the file was read three times (hash vs parse TOCTOU) and require() compared
    only the effect list against the fresh document:
    single read, and subject/scope/effects/root are all compared.

Out of scope, stated not hidden: anyone who can rewrite this module or the gate
owns the process.  The gate pins this file's digest, which removes the
shadow/poison path that only needed write access to the repo tree.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
from pathlib import Path

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
    "finding_marker": "W2_NATIVE_RUNS/W2_SECURITY_FINDING.json",
    "subjects": {"DEV": "FHS-5_PLP/W2/CONTROL_PACK", "OPS": "FHS-5_PLP/W2/CONTROL_PACK"},
    "effects": {"DEV": ["dev"], "OPS": ["ops"]},
    "authorised_roots": (
        "C:/Projects/Agent_Workspace/FHS-5_Workspace/W2_NATIVE_RUNS/",
    ),
}


class AdmissionError(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _digest(fields):
    return _sha(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def resolve_decision(explicit_path=None):
    cands = []
    if explicit_path:
        cands.append(Path(explicit_path))
    env = os.environ.get("W2_DECISION_PATH")
    if env:
        cands.append(Path(env))
    root = Path(TRUST["repo_root"])
    cands += [root / c for c in TRUST["decision_path_candidates"]]
    for c in cands:
        if c.is_file() and _sha(c.read_bytes()) == TRUST["decision_sha256"]:
            return c
    raise AdmissionError("FALSE_AUTHORITY",
                         "no decision document matching the pinned sha "
                         + TRUST["decision_sha256"][:16])


def _load_verified(explicit_path=None):
    p = resolve_decision(explicit_path)
    raw = p.read_bytes()
    got = _sha(raw)
    if got != TRUST["decision_sha256"]:
        raise AdmissionError("FALSE_AUTHORITY", "decision sha drifted mid-read")
    doc = json.loads(raw.decode("utf-8"))
    if doc.get("schema") != TRUST["schema"]:
        raise AdmissionError("FALSE_AUTHORITY", "schema " + str(doc.get("schema")))
    if doc.get("decision_id") != TRUST["decision_id"]:
        raise AdmissionError("FALSE_AUTHORITY", "decision_id " + str(doc.get("decision_id")))
    return {"doc": doc, "path": p, "sha256": got}


def _revoked():
    return (Path(TRUST["repo_root"]) / TRUST["revocation_marker"]).exists()


def _terminated_by_finding():
    """The decision's own clause: validity ends when a security Finding appears."""
    return (Path(TRUST["repo_root"]) / TRUST["finding_marker"]).exists()


def _evaluate_events():
    if _revoked():
        raise AdmissionError("ADMISSION_REVOKED", str(TRUST["revocation_marker"]))
    if _terminated_by_finding():
        raise AdmissionError("ADMISSION_TERMINATED_BY_SECURITY_FINDING",
                             str(TRUST["finding_marker"]))


def _evaluate_expiry(doc):
    text = str(doc.get("expiry_revocation") or "")
    up = text.upper()
    if "REVOK" in up and "NOT_REVOKED" not in up:
        raise AdmissionError("ADMISSION_REVOKED", text[:120])
    for m in re.finditer(r"(EXPIRED?|VALID[_ ]UNTIL)[^0-9]{0,12}(\d{4}-\d{2}-\d{2})", up):
        try:
            day = _dt.date.fromisoformat(m.group(2))
        except ValueError:
            raise AdmissionError("ADMISSION_EXPIRY_UNPARSABLE", text[:120])
        if day <= _dt.date.today():
            raise AdmissionError("ADMISSION_EXPIRED", str(day))
    for m in re.finditer(r"(\d{4}-\d{2}-\d{2})\s*(?:至|to|~|-)\s*(\d{4}-\d{2}-\d{2})", text):
        try:
            end = _dt.date.fromisoformat(m.group(2))
        except ValueError:
            continue
        if end <= _dt.date.today():
            raise AdmissionError("ADMISSION_EXPIRED", str(end))


def _within(child, parent):
    """Path-component containment, not a string prefix."""
    try:
        Path(child).relative_to(Path(parent))
        return True
    except ValueError:
        return False


def _check_root(repo_root, targets):
    repo = Path(repo_root).resolve()
    roots = [Path(r).resolve() for r in TRUST["authorised_roots"]]
    if not any(_within(repo, r) for r in roots):
        raise AdmissionError("ROOT_NOT_AUTHORISED", str(repo))
    out = []
    for t in targets or []:
        tp = Path(t).resolve() if Path(t).is_absolute() else (repo / t).resolve()
        if not _within(tp, repo):
            raise AdmissionError("TARGET_OUTSIDE_ROOT", str(tp))
        out.append(str(tp))
    return out


def _check_ops(repo_root, ops):
    """ADD requires a real parent directory; MODIFY/DELETE require a real file."""
    repo = Path(repo_root).resolve()
    for o in ops or []:
        p = (repo / o["path"]).resolve()
        op = str(o.get("operation", "")).upper()
        if op == "ADD":
            if p.exists():
                raise AdmissionError("WRITE_SET_UNBOUND", "ADD target already exists: " + str(p))
            if not p.parent.is_dir():
                raise AdmissionError("PARENT_ABSENT", str(p.parent))
        elif op in ("MODIFY", "DELETE"):
            if not p.is_file():
                raise AdmissionError("WRITE_SET_UNBOUND", "target missing: " + str(p))
        else:
            raise AdmissionError("WRITE_SET_UNBOUND", "unknown operation: " + op)


def derive(domain, scope="W2-NF-01", repo_root=None, targets=None,
           ops=None, explicit_path=None):
    _evaluate_events()
    v = _load_verified(explicit_path)
    doc = v["doc"]
    _evaluate_expiry(doc)
    sc = doc.get("scope") or {}
    want = TRUST["subjects"].get(domain)
    if sc.get("subject_id") != want:
        raise AdmissionError("SCOPE_MISMATCH",
                             str({"want": want, "granted": sc.get("subject_id")}))
    if sc.get("scope") != scope:
        raise AdmissionError("SCOPE_MISMATCH",
                             str({"want": scope, "granted": sc.get("scope")}))
    authorised = [e.strip().lower() for e in (sc.get("effects_authorized") or [])]
    tokens = TRUST["effects"].get(domain, [])
    if not any(any(a.startswith(t) for t in tokens) for a in authorised):
        raise AdmissionError("FALSE_AUTHORITY",
                             str({"domain": domain, "authorised": authorised}))
    if str(sc.get("allowed_roots") or "").upper().startswith("PENDING") and repo_root is None:
        raise AdmissionError("ROOT_NOT_AUTHORISED",
                             "decision allowed_roots is PENDING; supply and check a root")
    resolved = _check_root(repo_root, targets) if repo_root is not None else []
    if ops:
        _check_ops(repo_root, ops)
    fields = {"decision_id": doc.get("decision_id"), "subject_id": sc.get("subject_id"),
              "scope": sc.get("scope"), "domain": domain,
              "effects_authorized": sorted(sc.get("effects_authorized") or []),
              "expiry_revocation": doc.get("expiry_revocation"),
              "decision_sha256": v["sha256"],
              "trust_root": TRUST["decision_sha256"],
              "root": str(Path(repo_root).resolve()) if repo_root else None,
              "targets": sorted(resolved)}
    return {"ok": True, "decision_id": doc.get("decision_id"),
            "subject_id": sc.get("subject_id"), "scope": sc.get("scope"),
            "domain": domain, "expiry_revocation": doc.get("expiry_revocation"),
            "verified_from": {"path": str(v["path"]), "sha256": v["sha256"]},
            "fields": fields, "subject_sha256": _digest(fields)}


def require(receipt, domain, scope="W2-NF-01", explicit_path=None,
            repo_root=None, targets=None, ops=None):
    if not isinstance(receipt, dict) or receipt.get("ok") is not True:
        raise AdmissionError("FALSE_AUTHORITY", "no receipt")
    _evaluate_events()
    v = _load_verified(explicit_path)
    _evaluate_expiry(v["doc"])
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
            raise AdmissionError("FALSE_AUTHORITY", "receipt field drifted: " + k)
    fresh = derive(domain, scope, repo_root=repo_root, targets=targets,
                   ops=ops, explicit_path=explicit_path)
    if targets and sorted(fresh["fields"]["targets"]) != sorted(fields.get("targets") or []):
        raise AdmissionError("TARGET_SET_MISMATCH",
                             "receipt was issued for a different target set")
    for k in ("subject_id", "scope", "effects_authorized"):
        if fresh["fields"][k] != fields.get(k):
            raise AdmissionError("FALSE_AUTHORITY",
                                 "decision changed since the receipt: " + k)
    if repo_root is not None and fresh["fields"]["root"] != fields.get("root"):
        raise AdmissionError("ROOT_NOT_AUTHORISED",
                             "receipt was issued for a different root")
    return {"ok": True, "decision_id": fresh["decision_id"], "domain": domain,
            "verified_from": fresh["verified_from"], "reverified": True}


def verify_receipt(receipt, explicit_path=None):
    try:
        require(receipt, receipt.get("domain", "DEV"),
                receipt.get("scope", "W2-NF-01"), explicit_path)
        return True
    except AdmissionError:
        return False
