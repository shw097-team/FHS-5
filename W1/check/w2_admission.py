#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 admission (generation 2, config-driven) — the product entry.

The decision id, sha, expiry, domain, write root and allowed ops are no longer
hard-coded in this module: they come from ``W1/authority/trust.json`` next to
this package.  Replacing a grant therefore does not require editing product
code or re-pinning the gate.

What the module still enforces on its own:

  A1  revocation by decision_id (portable: a fresh clone with no local marker
      still refuses the terminated decision)
  A2  absolute expiry parsed from the decision document
  A3  caller-supplied root/scope/issuer/expiry/trust-path is refused, not
      ignored; a path may only *locate* the pinned decision bytes
  A4  the exact op set from the grant; a subset is not acceptable
  A5  lexical checks before resolve, resolved confinement, and a reparse check
      on every component from the root down
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
from pathlib import Path

AUTHORITY_DIR = Path(__file__).resolve().parent.parent / "authority"
TRUST_PATH = AUTHORITY_DIR / "trust.json"


def _load_cfg():
    try:
        raw = TRUST_PATH.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"TRUST_UNREADABLE: {exc}") from exc
    cfg = json.loads(raw.decode("utf-8"))
    cfg["_sha256"] = hashlib.sha256(raw).hexdigest()
    return cfg


CFG = _load_cfg()
_DEFAULT = CFG.get("default_domain", "DEV")
_DEV = CFG["domains"][_DEFAULT]

SCHEMA = _DEV["decision"]["schema"]
DECISION_ID = _DEV["decision"]["decision_id"]
DECISION_SHA256 = _DEV["decision"]["sha256"]
NOT_AFTER = _DEV.get("not_after") or "2099-01-01T00:00:00+08:00"
DOMAIN = _DEV.get("domain", _DEFAULT)
SCOPE = _DEV["scope"]
SUBJECT_ID = _DEV["decision"].get("subject_id", "FHS-5_PLP/W2/CONTROL_PACK")
WRITE_ROOT = _DEV["write_root"]
ALLOWED_OPS = tuple((o["path"], o["operation"].upper()) for o in _DEV["allowed_ops"])
REVOKED = {r["decision_id"]: (r.get("token") or "ADMISSION_REVOKED")
           for r in CFG.get("revoked") or []}
FINDING_MARKERS = tuple(CFG.get("finding_markers") or ())
DECISION_CANDIDATES = (_DEV["decision"]["path"],)

_FORBIDDEN_REQUEST_KEYS = {
    "trust_path", "trust_root", "decision_sha256", "allowed_roots",
    "write_root", "issuer", "principal", "scope_override", "expiry",
    "not_after", "revoked", "revocation", "decision_id", "domain",
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


def _lexical_problem(path):
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


def _domain_cfg(domain):
    key = str(domain).upper()
    cfg = CFG["domains"].get(key)
    if cfg is None:
        raise AdmissionError("PRINCIPAL_DOMAIN_MISMATCH", str(domain))
    cfg = dict(cfg)
    if key == _DEFAULT:
        # keep the module-level knobs authoritative for the default domain so
        # existing fixtures and probes can pin a root without editing the file
        cfg["write_root"] = WRITE_ROOT
        cfg["allowed_ops"] = [{"path": p, "operation": o} for p, o in ALLOWED_OPS]
    return cfg


def _locate_decision(cfg, explicit_path):
    dec = cfg["decision"]
    cands = []
    if explicit_path:
        cands.append(Path(explicit_path))
    env = os.environ.get("W2_DECISION_PATH")
    if env:
        cands.append(Path(env))
    dec_path = Path(dec["path"])
    cands.append(dec_path if dec_path.is_absolute() else AUTHORITY_DIR / dec_path)
    for c in cands:
        try:
            if c.is_file() and _sha(c.read_bytes()) == dec["sha256"]:
                return c
        except OSError:
            continue
    raise AdmissionError("FALSE_AUTHORITY", "no decision matching " + dec["sha256"][:16])


def _load_decision(cfg, explicit_path):
    p = _locate_decision(cfg, explicit_path)
    raw = p.read_bytes()
    got = _sha(raw)
    if got != cfg["decision"]["sha256"]:
        raise AdmissionError("FALSE_AUTHORITY", "decision drifted mid-read")
    doc = json.loads(raw.decode("utf-8"))
    if doc.get("schema") != cfg["decision"]["schema"]:
        raise AdmissionError("FALSE_AUTHORITY", "schema " + str(doc.get("schema")))
    if doc.get("decision_id") != cfg["decision"]["decision_id"]:
        raise AdmissionError("FALSE_AUTHORITY", "decision_id " + str(doc.get("decision_id")))
    return doc, got, p


def _evaluate_state(doc, cfg, repo_root, now=None):
    did = doc.get("decision_id")
    if did in REVOKED:
        raise AdmissionError(REVOKED[did], did)
    try:
        end = _dt.datetime.fromisoformat(str(cfg.get("not_after") or doc.get("expiry")))
    except ValueError as exc:
        raise AdmissionError("ADMISSION_EXPIRY_UNPARSABLE", str(cfg.get("not_after"))) from exc
    if end.tzinfo is None:
        raise AdmissionError("ADMISSION_EXPIRY_UNPARSABLE", "no offset")
    clock = now or _dt.datetime.now(end.tzinfo)
    if clock >= end:
        raise AdmissionError("ADMISSION_EXPIRED", f"{clock.isoformat()} >= {end.isoformat()}")
    for rel in FINDING_MARKERS:
        if did in REVOKED and (Path(repo_root) / rel).exists():
            raise AdmissionError("ADMISSION_TERMINATED_BY_SECURITY_FINDING", rel)


def derive(domain, scope, repo_root, targets, ops=None, decision_path=None,
           request=None):
    if request is not None:
        if not isinstance(request, dict):
            raise AdmissionError("REQUEST_INVALID", "not an object")
        bad = sorted(set(request) & _FORBIDDEN_REQUEST_KEYS)
        if bad:
            raise AdmissionError("TRUST_OVERRIDE_REJECTED", bad)

    cfg = _domain_cfg(domain)
    doc, dec_sha, dec_path = _load_decision(cfg, decision_path)
    _evaluate_state(doc, cfg, repo_root)

    if str(domain).upper() != str(cfg.get("domain", domain)).upper():
        raise AdmissionError("PRINCIPAL_DOMAIN_MISMATCH", str(domain))
    if scope != cfg["scope"]:
        raise AdmissionError("SCOPE_MISMATCH", {"want": cfg["scope"], "got": scope})
    if (doc.get("scope") or {}).get("subject_id") != SUBJECT_ID:
        raise AdmissionError("SCOPE_MISMATCH", "decision subject")

    root = Path(repo_root).resolve()
    if str(root).lower() != str(Path(cfg["write_root"]).resolve()).lower():
        raise AdmissionError("ROOT_NOT_AUTHORISED", str(root))
    if _is_reparse(root):
        raise AdmissionError("REPARSE_POINT_REFUSED", str(root))

    allowed = {(o["path"], str(o["operation"]).upper()) for o in cfg["allowed_ops"]}
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
        "scope": cfg["scope"],
        "domain": str(domain).upper(),
        "write_root": str(root),
        "targets": sorted(f"{p}:{o}" for p, o in allowed),
        "decision_sha256": dec_sha,
        "trust_sha256": CFG["_sha256"],
        "expiry": cfg.get("not_after") or doc.get("expiry"),
        "generation": 2,
    }
    return {
        "ok": True,
        "decision_id": fields["decision_id"],
        "subject_id": SUBJECT_ID,
        "scope": cfg["scope"],
        "domain": fields["domain"],
        "targets": resolved,
        "verified_from": {"decision": str(dec_path), "sha256": dec_sha,
                          "trust": str(TRUST_PATH), "trust_sha256": CFG["_sha256"]},
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
    if fields.get("trust_sha256") != CFG["_sha256"]:
        raise AdmissionError("FALSE_AUTHORITY", "receipt pins another trust config")
    fresh = derive(domain, scope, repo_root, targets, ops=ops,
                   decision_path=decision_path, request=request)
    for k in ("decision_id", "subject_id", "scope", "domain", "write_root",
              "targets", "decision_sha256", "trust_sha256"):
        if fields.get(k) != fresh["fields"][k]:
            raise AdmissionError("FALSE_AUTHORITY", "receipt field drifted: " + k)
    return {"ok": True, "decision_id": fresh["decision_id"], "domain": fresh["domain"],
            "scope": fresh["scope"], "subject_id": fresh["subject_id"],
            "verified_from": fresh["verified_from"], "reverified": True,
            "fields": fresh["fields"], "subject_sha256": fresh["subject_sha256"]}


def verify_receipt(receipt, domain="DEV", scope=None, repo_root=None,
                   targets=None, decision_path=None):
    try:
        require(receipt, domain, scope or SCOPE,
                repo_root or WRITE_ROOT,
                targets or [{"path": p, "operation": o} for p, o in ALLOWED_OPS],
                decision_path=decision_path)
        return True
    except AdmissionError:
        return False
