#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2/S3 admission — generation 2, run-scoped, separated trust config.

Design differences from w2_admission.py (the W2 generation-1 verifier):

  G1  The trusted configuration is a file *outside the write root*
      (40_TRUST/TRUST.json next to this module).  A caller cannot select it,
      pass a path to it, or override its fields; anything that looks like an
      override is refused, not ignored.
  G2  Revocation and the security-finding termination are *portable*: they are
      named by decision_id inside TRUST.json, so a fresh clone without the
      local marker file still refuses the terminated decision.
  G3  Validity is an absolute instant (not_after, ISO-8601 with offset), not a
      regex over prose.
  G4  The exact write set is fixed by the trusted config.  A request that names
      any other path or operation is refused; there is no "subset is fine".
  G5  Every target and every parent between the write root and the target is
      checked for reparse points (junction / symlink) before any effect.

Stated out of scope, not hidden: whoever can rewrite this module or TRUST.json
owns the process.  Both live outside the write root, and the gate re-hashes
TRUST.json at every check so a mid-run swap is a typed refusal.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import stat
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRUST_PATH = HERE / "TRUST.json"

_FORBIDDEN_REQUEST_KEYS = {
    "trust_path", "trust_root", "decision_sha256", "decision_path",
    "allowed_roots", "write_root", "issuer", "principal", "scope_override",
    "not_after", "expiry", "revoked", "revocation",
}

FILE_ATTRIBUTE_REPARSE_POINT = 0x400


class AdmissionError(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _digest(fields):
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
    """True if target or any component below root is a reparse point."""
    try:
        rel = target.resolve(strict=False).relative_to(root.resolve())
    except ValueError:
        return True
    cur = root.resolve()
    if _is_reparse(cur):
        return True
    for part in rel.parts:
        cur = cur / part
        if _is_reparse(cur):
            return True
    return False


def load_trust():
    try:
        raw = TRUST_PATH.read_bytes()
    except OSError as exc:
        raise AdmissionError("TRUST_UNREADABLE", str(exc)) from exc
    sha = _sha(raw)
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise AdmissionError("TRUST_UNREADABLE", str(exc)) from exc
    if not isinstance(doc, dict):
        raise AdmissionError("TRUST_UNREADABLE", "not an object")
    return doc, sha


def _decision_doc(trust):
    d = trust.get("decision") or {}
    p = Path(d.get("path") or "")
    if not p.is_file():
        raise AdmissionError("FALSE_AUTHORITY", "decision document absent")
    raw = p.read_bytes()
    got = _sha(raw)
    if got != str(d.get("sha256", "")).lower():
        raise AdmissionError("FALSE_AUTHORITY", "decision sha drifted")
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise AdmissionError("FALSE_AUTHORITY", f"decision unreadable: {exc}") from exc
    if doc.get("schema") != d.get("schema"):
        raise AdmissionError("FALSE_AUTHORITY", "schema " + str(doc.get("schema")))
    if doc.get("decision_id") != d.get("decision_id"):
        raise AdmissionError("FALSE_AUTHORITY",
                             "decision_id " + str(doc.get("decision_id")))
    return doc, got


def _evaluate_state(trust, doc):
    did = doc.get("decision_id")
    for rev in trust.get("revoked") or []:
        if rev.get("decision_id") == did:
            raise AdmissionError(rev.get("token") or "ADMISSION_REVOKED",
                                 str(rev.get("reason", ""))[:200])
    ends = trust.get("not_after")
    try:
        end = _dt.datetime.fromisoformat(str(ends))
    except ValueError as exc:
        raise AdmissionError("TRUST_UNREADABLE", f"not_after: {ends}") from exc
    if end.tzinfo is None:
        raise AdmissionError("TRUST_UNREADABLE", "not_after has no offset")
    now = _dt.datetime.now(end.tzinfo)
    if now >= end:
        raise AdmissionError("ADMISSION_EXPIRED", f"{now.isoformat()} >= {ends}")
    for rel in trust.get("termination_markers") or []:
        repo = Path(trust["repo_root"])
        if (repo / rel).exists():
            for did_term in trust.get("terminated_decision_ids") or []:
                if did_term == did:
                    raise AdmissionError("ADMISSION_TERMINATED_BY_SECURITY_FINDING",
                                         str(repo / rel))


def _check_targets(trust, targets):
    root = Path(trust["write_root"]).resolve()
    allowed = {(e["path"], e["operation"].upper())
               for e in trust.get("allowed_ops") or []}
    got = set()
    resolved = []
    for t in targets or []:
        path = t.get("path")
        op = str(t.get("operation", "")).upper()
        if not isinstance(path, str) or not path:
            raise AdmissionError("WRITE_SET_UNBOUND", "empty path")
        if path.startswith("/") or "\\" in path or ".." in Path(path).parts:
            raise AdmissionError("WRITE_SET_UNBOUND", path)
        if "*" in path:
            raise AdmissionError("WRITE_SET_UNBOUND", "glob " + path)
        tp = (root / path).resolve(strict=False)
        try:
            tp.relative_to(root)
        except ValueError:
            raise AdmissionError("TARGET_OUTSIDE_ROOT", str(tp))
        if _chain_has_reparse(root, tp):
            raise AdmissionError("REPARSE_POINT_REFUSED", str(tp))
        got.add((path, op))
        resolved.append({"path": path, "operation": op, "absolute": str(tp)})
    if got != allowed:
        raise AdmissionError(
            "WRITE_SET_UNBOUND",
            str({"want": sorted(allowed), "got": sorted(got)}))
    return resolved


def derive(domain, scope, repo_root, targets, request=None):
    if request is not None:
        if not isinstance(request, dict):
            raise AdmissionError("REQUEST_INVALID", "not an object")
        bad = sorted(set(request) & _FORBIDDEN_REQUEST_KEYS)
        if bad:
            raise AdmissionError("TRUST_OVERRIDE_REJECTED", bad)
    trust, trust_sha = load_trust()
    doc, decision_sha = _decision_doc(trust)
    _evaluate_state(trust, doc)
    if str(domain).upper() != str(trust.get("domain", "")).upper():
        raise AdmissionError("PRINCIPAL_DOMAIN_MISMATCH", str(domain))
    if scope != trust.get("scope"):
        raise AdmissionError("SCOPE_MISMATCH",
                             str({"want": trust.get("scope"), "got": scope}))
    if str(Path(repo_root).resolve()) != str(Path(trust["write_root"]).resolve()):
        raise AdmissionError("ROOT_NOT_AUTHORISED", str(repo_root))
    resolved = _check_targets(trust, targets)
    fields = {
        "decision_id": doc.get("decision_id"),
        "subject_id": doc.get("scope", {}).get("subject_id"),
        "scope": trust.get("scope"),
        "domain": trust.get("domain"),
        "write_root": str(Path(trust["write_root"]).resolve()),
        "targets": sorted(f"{r['path']}:{r['operation']}" for r in resolved),
        "decision_sha256": decision_sha,
        "trust_sha256": trust_sha,
        "not_after": trust.get("not_after"),
    }
    return {
        "ok": True,
        "decision_id": fields["decision_id"],
        "subject_id": fields["subject_id"],
        "scope": fields["scope"],
        "domain": fields["domain"],
        "targets": resolved,
        "verified_from": {"trust": str(TRUST_PATH), "trust_sha256": trust_sha,
                          "decision": str(trust["decision"]["path"]),
                          "decision_sha256": decision_sha},
        "fields": fields,
        "receipt_sha256": _digest(fields),
    }


def require(receipt, domain, scope, repo_root, targets, request=None):
    if not isinstance(receipt, dict) or receipt.get("ok") is not True:
        raise AdmissionError("FALSE_AUTHORITY", "no receipt")
    fresh = derive(domain, scope, repo_root, targets, request)
    if _digest(receipt.get("fields")) != receipt.get("receipt_sha256"):
        raise AdmissionError("FALSE_AUTHORITY", "receipt digest does not re-derive")
    for k in ("decision_id", "subject_id", "scope", "domain", "write_root",
              "targets", "decision_sha256", "trust_sha256"):
        if (receipt.get("fields") or {}).get(k) != fresh["fields"][k]:
            raise AdmissionError("FALSE_AUTHORITY", "receipt field drifted: " + k)
    return fresh
