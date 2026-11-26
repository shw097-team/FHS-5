#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 admission (generation 2) — the product entry, not a second runtime.

Replaces the generation-1 verifier that copied a prose expiry and a
local-marker revocation.  The changes that matter:

  A1  Revocation is by decision_id, so a fresh clone with no local marker still
      refuses the terminated decision.  The marker only corroborates.
  A2  Expiry is an absolute instant parsed from the decision, not a regex over
      its prose.
  A3  A caller cannot supply a root, scope, issuer, expiry or trust path that
      changes the decision: those keys are refused, not ignored.  A decision
      path may be supplied only to *locate* the pinned bytes.
  A4  The write set is the decision's exact op set.  A subset is not "fine".
  A5  Lexical checks and resolved checks are separate; every component from the
      root down is checked for a reparse point (junction or symlink).

Out of scope, stated: whoever can rewrite this module owns the process.  The
gate pins this file's digest, and this module refuses a decision whose bytes do
not match the pin.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
from pathlib import Path

SCHEMA = "FHS5.PLP.W2.OwnerDecision@local-2"
DECISION_ID = "W2-S2S3-OWNER-20261126-02"
DECISION_SHA256 = "abde6b84d92d15ed6806ad6c9c81c999019d75948ba0d9f03e8d4309a920f5e1"
NOT_AFTER = "2026-11-27T23:59:59+08:00"
DOMAIN = "DEV"
SCOPE = "W2-NF-01"
SUBJECT_ID = "FHS-5_PLP/W2/CONTROL_PACK"
WRITE_ROOT = (
    "C:/Projects/Agent_Workspace/FHS-5_Workspace/W2_NATIVE_RUNS/"
    "S2S3_20261126T225929/20_WORLD"
)
ALLOWED_OPS = (
    ("W1/check/w2_receiver.py", "MODIFY"),
    ("W1/check/test_j1_receiver.py", "MODIFY"),
)
REVOKED = {
    "W2-NF-PRIMARY-20261126-01": "ADMISSION_TERMINATED_BY_SECURITY_FINDING",
}
FINDING_MARKERS = ("W2_NATIVE_RUNS/W2_SECURITY_FINDING.json",)
DECISION_CANDIDATES = (
    "W2_NATIVE_RUNS/S2S3_20261126T225929/10_DECISION/W2_OWNER_DECISION_S2S3.json",
)

_FORBIDDEN_REQUEST_KEYS = {
    "trust_path", "trust_root", "decision_sha256", "allowed_roots",
    "write_root", "issuer", "principal", "scope_override", "expiry",
    "not_after", "revoked", "revocation", "decision_id",
}
FILE_ATTRIBUTE_REPARSE_POINT = 0x400


class AdmissionError(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _digest(fields) -> str:
    return _sha(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def _is_reparse(p: Path) -> bool:
    try:
        st = p.lstat()
    except OSError:
        return False
    if p.is_symlink():
        return True
    return bool(getattr(st, "st_file_attributes", 0) & FILE_ATTRIBUTE_REPARSE_POINT)


def _chain_has_reparse(root: Path, target: Path) -> bool:
    try:
        rel = target.relative_to(root)
    except ValueError:
        return True
    cur = root
    if _is_reparse(cur):
        return True
    for part in rel.parts:
        cur = cur / part
        if _is_reparse(cur):
            return True
    return False


def _lexical_problem(path) -> str | None:
    if not isinstance(path, str) or not path:
        return "empty"
    if path.startswith("/") or path.startswith("\\"):
        return "absolute"
    if "\\" in path:
        return "backslash"
    if ":" in path.split("/")[0]:
        return "drive"
    if "*" in path or "?" in path:
        return "glob"
    for seg in path.split("/"):
        if seg in ("", ".", ".."):
            return "segment"
        if seg.endswith(" ") or seg.endswith("."):
            return "truncatable segment"
    return None


def _locate_decision(explicit_path):
    cands = []
    if explicit_path:
        cands.append(Path(explicit_path))
    env = os.environ.get("W2_DECISION_PATH")
    if env:
        cands.append(Path(env))
    repo = Path(__file__).resolve().parents[2]
    cands += [repo / c for c in DECISION_CANDIDATES]
    for c in cands:
        try:
            if c.is_file() and _sha(c.read_bytes()) == DECISION_SHA256:
                return c
        except OSError:
            continue
    raise AdmissionError("FALSE_AUTHORITY",
                         "no decision matching " + DECISION_SHA256[:16])


def _load_decision(explicit_path):
    p = _locate_decision(explicit_path)
    raw = p.read_bytes()
    got = _sha(raw)
    if got != DECISION_SHA256:
        raise AdmissionError("FALSE_AUTHORITY", "decision drifted mid-read")
    doc = json.loads(raw.decode("utf-8"))
    if doc.get("schema") != SCHEMA:
        raise AdmissionError("FALSE_AUTHORITY", "schema " + str(doc.get("schema")))
    if doc.get("decision_id") != DECISION_ID:
        raise AdmissionError("FALSE_AUTHORITY", "decision_id " + str(doc.get("decision_id")))
    return doc, got, p


def _evaluate_state(doc, repo_root, now=None):
    did = doc.get("decision_id")
    if did in REVOKED:
        raise AdmissionError(REVOKED[did], did)
    try:
        end = _dt.datetime.fromisoformat(str(doc.get("expiry") or NOT_AFTER))
    except ValueError as exc:
        raise AdmissionError("ADMISSION_EXPIRY_UNPARSABLE", str(doc.get("expiry"))) from exc
    if end.tzinfo is None:
        raise AdmissionError("ADMISSION_EXPIRY_UNPARSABLE", "no offset")
    clock = now or _dt.datetime.now(end.tzinfo)
    if clock >= end:
        raise AdmissionError("ADMISSION_EXPIRED", f"{clock.isoformat()} >= {end.isoformat()}")
    for rel in FINDING_MARKERS:
        if (Path(repo_root) / rel).exists() and did in REVOKED:
            raise AdmissionError("ADMISSION_TERMINATED_BY_SECURITY_FINDING", rel)


def derive(domain, scope, repo_root, targets, ops=None, decision_path=None,
           request=None):
    if request is not None:
        if not isinstance(request, dict):
            raise AdmissionError("REQUEST_INVALID", "not an object")
        bad = sorted(set(request) & _FORBIDDEN_REQUEST_KEYS)
        if bad:
            raise AdmissionError("TRUST_OVERRIDE_REJECTED", bad)

    doc, dec_sha, dec_path = _load_decision(decision_path)
    _evaluate_state(doc, repo_root)

    if str(domain).upper() != DOMAIN:
        raise AdmissionError("PRINCIPAL_DOMAIN_MISMATCH", str(domain))
    if scope != SCOPE:
        raise AdmissionError("SCOPE_MISMATCH", {"want": SCOPE, "got": scope})
    if (doc.get("scope") or {}).get("subject_id") != SUBJECT_ID:
        raise AdmissionError("SCOPE_MISMATCH", "decision subject")

    root = Path(repo_root).resolve()
    if str(root).lower() != str(Path(WRITE_ROOT).resolve()).lower():
        raise AdmissionError("ROOT_NOT_AUTHORISED", str(root))
    if _is_reparse(root):
        raise AdmissionError("REPARSE_POINT_REFUSED", str(root))

    allowed = set(ALLOWED_OPS)
    got = set()
    resolved = []
    for t in targets or []:
        path = t.get("path")
        op = str(t.get("operation", "")).upper()
        problem = _lexical_problem(path)
        if problem is not None:
            raise AdmissionError("WRITE_SET_UNBOUND", f"{path!r}: {problem}")
        tp = (root / path).resolve(strict=False)
        try:
            tp.relative_to(root)
        except ValueError:
            raise AdmissionError("TARGET_OUTSIDE_ROOT", str(tp)) from None
        if _chain_has_reparse(root, tp):
            raise AdmissionError("REPARSE_POINT_REFUSED", str(tp))
        got.add((path, op))
        resolved.append({"path": path, "operation": op, "absolute": str(tp)})
    if got != allowed:
        raise AdmissionError("WRITE_SET_UNBOUND",
                             {"want": sorted(allowed), "got": sorted(got)})

    for extra in ops or []:
        if (extra.get("path"), str(extra.get("operation", "")).upper()) not in allowed:
            raise AdmissionError("WRITE_SET_UNBOUND", "op outside decision: " + str(extra))

    fields = {
        "decision_id": doc.get("decision_id"),
        "subject_id": SUBJECT_ID,
        "scope": SCOPE,
        "domain": DOMAIN,
        "write_root": str(root),
        "targets": sorted(f"{p}:{o}" for p, o in allowed),
        "decision_sha256": dec_sha,
        "expiry": (doc.get("expiry") or NOT_AFTER),
        "generation": 2,
    }
    return {
        "ok": True,
        "decision_id": fields["decision_id"],
        "subject_id": SUBJECT_ID,
        "scope": SCOPE,
        "domain": DOMAIN,
        "targets": resolved,
        "verified_from": {"decision": str(dec_path), "sha256": dec_sha},
        "fields": fields,
        "subject_sha256": _digest(fields),
    }


def require(receipt, domain, scope, repo_root, targets, ops=None,
            decision_path=None, request=None):
    if not isinstance(receipt, dict) or receipt.get("ok") is not True:
        raise AdmissionError("FALSE_AUTHORITY", "no receipt")
    fields = receipt.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise AdmissionError("FALSE_AUTHORITY", "receipt carries no field set")
    if _digest(fields) != receipt.get("subject_sha256"):
        raise AdmissionError("FALSE_AUTHORITY", "receipt digest does not re-derive")
    if fields.get("decision_sha256") != DECISION_SHA256:
        raise AdmissionError("FALSE_AUTHORITY", "receipt pins another decision")
    fresh = derive(domain, scope, repo_root, targets, ops=ops,
                   decision_path=decision_path, request=request)
    for k in ("decision_id", "subject_id", "scope", "domain", "write_root",
              "targets", "decision_sha256"):
        if fields.get(k) != fresh["fields"][k]:
            raise AdmissionError("FALSE_AUTHORITY", "receipt field drifted: " + k)
    return {"ok": True, "decision_id": fresh["decision_id"], "domain": DOMAIN,
            "scope": fresh["scope"], "subject_id": fresh["subject_id"],
            "verified_from": fresh["verified_from"], "reverified": True,
            "fields": fresh["fields"], "subject_sha256": fresh["subject_sha256"]}


def verify_receipt(receipt, domain="DEV", scope=SCOPE, repo_root=WRITE_ROOT,
                   targets=None, decision_path=None):
    try:
        require(receipt, domain, scope, repo_root,
                targets or [{"path": p, "operation": o} for p, o in ALLOWED_OPS],
                decision_path=decision_path)
        return True
    except AdmissionError:
        return False
