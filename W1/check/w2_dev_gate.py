#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEV admission gate: refuse before any write.

01 §1 requires, for every DEV op, a same-snapshot repo probe plus an exact write
set with per-file preimage.  The previous round enforced this only by procedure;
this module makes it executable and gives each refusal a typed FirstFail.

Contract:
    check(asserted, repo_root, write_set) -> dict decision
      asserted  : what the caller *claims* (head, effect, admission, scope)
      repo_root : the live repository
      write_set : [{"path", "operation": "MODIFY"|"ADD"|"DELETE", "preimage_sha256"?}]

It never writes.  apply_patch() is the only writer and it re-runs check() first.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

KNOWN_EFFECTS = {"REPOSITORY_WRITE", "REPOSITORY_READ"}
FORBIDDEN_RECOVERY = {"GIT_REVERT", "GIT_RESET", "GIT_CLEAN", "WHOLE_REPO_ROLLBACK"}


class GateError(Exception):
    def __init__(self, token: str, detail: str = ""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _git(repo, *args) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, errors="replace")
    return p.returncode, (p.stdout or "").strip()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check(asserted: dict, repo_root, write_set: list) -> dict:
    repo = Path(repo_root).resolve()
    checks, token = [], {"v": None}

    def fail(name, tok, detail=""):
        checks.append({"check": name, "ok": False, "detail": str(detail)[:300]})
        if token["v"] is None:
            token["v"] = tok
        return False

    def ok(name, detail=""):
        checks.append({"check": name, "ok": True, "detail": str(detail)[:300]})
        return True

    # 1 effect must be a known token — unknown never defaults to READ
    effect = asserted.get("effect")
    if effect not in KNOWN_EFFECTS:
        fail("effect_token", "EFFECT_UNBOUND", effect)
        return _decision(checks, token["v"], repo, None)
    ok("effect_token", effect)

    # 2 admission: a caller dict is not a grant. Under strict mode the gate
    #    requires a receipt that re-derives from the hash-pinned Owner decision.
    adm = asserted.get("admission") or {}
    strict = bool(asserted.get("require_verified_admission"))
    if strict:
        try:
            import w2_admission as ADM
            pin = asserted.get("admission_pin")
            ADM.require(adm, pin)
            ok("admission", f"receipt verified against pinned decision {pin[:12]}")
        except Exception as exc:  # noqa: BLE001
            fail("admission", "FALSE_AUTHORITY", str(exc)[:200])
    elif not adm.get("decision_id") or adm.get("expired") is True:
        fail("admission", "FALSE_AUTHORITY", adm)
    else:
        ok("admission", adm.get("decision_id"))

    # 3 scope must match exactly
    want_scope = asserted.get("scope")
    have_scope = adm.get("scope")
    if not want_scope or want_scope != have_scope:
        fail("scope", "SCOPE_MISMATCH", {"want": want_scope, "granted": have_scope})
    else:
        ok("scope", want_scope)

    # 4 principal domain: DEV must not ride an OPS grant
    if adm.get("domain") and adm.get("domain") != "DEV":
        fail("principal_domain", "PRINCIPAL_DOMAIN_MISMATCH", adm.get("domain"))
    else:
        ok("principal_domain", adm.get("domain"))

    # 5 live repo probe, same snapshot
    rc, live_head = _git(repo, "rev-parse", "HEAD")
    if rc != 0:
        fail("repo_head", "REPO_UNBOUND", live_head)
        return _decision(checks, token["v"], repo, None)
    if asserted.get("head") != live_head:
        fail("repo_head", "REPO_HEAD_MISMATCH",
             {"asserted": asserted.get("head"), "live": live_head})
    else:
        ok("repo_head", live_head)

    # 6 write set must be exact, non-empty and free of globs
    if not write_set:
        fail("write_set", "WRITE_SET_UNBOUND", "empty")
    for e in write_set:
        p = e.get("path", "")
        if not p or "*" in p or p.startswith("/") or ".." in Path(p).parts:
            fail("write_set_shape", "WRITE_SET_UNBOUND", p)
            break
    else:
        ok("write_set_shape", f"{len(write_set)} entries")

    # 7 per-file preimage / absence, measured now
    preimages = {}
    for e in write_set:
        p = repo / e["path"]
        op = e.get("operation")
        if op == "ADD":
            if p.exists():
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", "expected absent")
                continue
            preimages[e["path"]] = None
        elif op in ("MODIFY", "DELETE"):
            if not p.is_file():
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", "missing")
                continue
            live_sha = sha256_file(p)
            preimages[e["path"]] = live_sha
            if e.get("preimage_sha256") and e["preimage_sha256"] != live_sha:
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND",
                     {"declared": e["preimage_sha256"], "live": live_sha})
        else:
            fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", f"bad operation {op}")

    # 8 dirty state: only our own write set may be dirty
    rc, porcelain = _git(repo, "status", "--porcelain=v2", "--untracked-files=all")
    if rc == 0:
        dirty = {ln.split()[-1] for ln in porcelain.splitlines() if ln.strip()}
        allowed = {e["path"] for e in write_set}
        foreign = sorted(d for d in dirty if d not in allowed)
        if foreign:
            fail("dirty_preservation", "REPO_UNBOUND", foreign[:5])
        else:
            ok("dirty_preservation", f"{len(dirty)} dirty, all in write set")

    # 9 recovery kind must be a DEV kind
    rec = asserted.get("recovery") or {}
    if str(rec.get("kind", "")).upper() in FORBIDDEN_RECOVERY:
        fail("recovery_kind", "RECOVERY_KIND_MISMATCH", rec.get("kind"))
    else:
        ok("recovery_kind", rec.get("kind"))

    return _decision(checks, token["v"], repo, preimages)


def _decision(checks, first_fail, repo, preimages):
    return {
        "ok": first_fail is None,
        "first_fail": first_fail,
        "repo": str(repo),
        "checks": checks,
        "preimages": preimages or {},
        "wrote": [],
        "product_calls": 0,
    }


def apply_patch(asserted, repo_root, write_set, patch_text: str) -> dict:
    """The only writer.  Re-runs check(); applies the patch; re-reads."""
    d = check(asserted, repo_root, write_set)
    if not d["ok"]:
        return d
    repo = Path(repo_root).resolve()
    allowed = {e["path"] for e in write_set}
    p = subprocess.run(["git", "-C", str(repo), "apply", "--check", "-"],
                       input=patch_text.encode("utf-8"), capture_output=True)
    if p.returncode != 0:
        d["ok"] = False
        d["first_fail"] = "PATCH_NOT_APPLICABLE"
        d["checks"].append({"check": "patch_apply_check", "ok": False,
                            "detail": (p.stderr or b"")[:300].decode("utf-8", "replace")})
        return d
    touched = {ln[6:] for ln in patch_text.splitlines() if ln.startswith("+++ b/")}
    outside = sorted(touched - allowed)
    if outside:
        d["ok"] = False
        d["first_fail"] = "WRITE_SET_UNBOUND"
        d["checks"].append({"check": "patch_scope", "ok": False, "detail": outside})
        return d
    p = subprocess.run(["git", "-C", str(repo), "apply", "-"],
                       input=patch_text.encode("utf-8"), capture_output=True)
    d["checks"].append({"check": "patch_apply", "ok": p.returncode == 0,
                        "detail": (p.stderr or b"")[:300].decode("utf-8", "replace")})
    d["ok"] = p.returncode == 0
    d["first_fail"] = None if d["ok"] else "PATCH_APPLY_FAILED"
    d["wrote"] = sorted(touched) if d["ok"] else []
    return d


def reverse(patch_text: str, repo_root, write_set) -> dict:
    """DEV recovery: reverse patch on a copy, never git reset/clean/revert."""
    repo = Path(repo_root).resolve()
    d = {"ok": False, "first_fail": None, "checks": []}
    tmp = Path(tempfile.mkdtemp(prefix="rev_"))
    try:
        for e in write_set:
            src = repo / e["path"]
            dst = tmp / e["path"]
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        p = subprocess.run(["patch", "-R", "-p1", "--batch", "--binary", "-i", "-"],
                           input=patch_text.encode("utf-8"), capture_output=True,
                           cwd=str(tmp))
        out = ((p.stdout or b"") + (p.stderr or b"")).decode("utf-8", "replace")
        d["checks"].append({"check": "reverse_apply", "ok": p.returncode == 0,
                            "detail": out[:300]})
        d["ok"] = p.returncode == 0
        if d["ok"]:
            restored = {}
            for e in write_set:
                f = tmp / e["path"]
                restored[e["path"]] = sha256_file(f) if f.is_file() else None
            d["restored"] = restored
            want = {e["path"]: e.get("preimage_sha256") for e in write_set
                    if e.get("preimage_sha256")}
            d["restored_matches_preimage"] = all(
                restored.get(k) == v for k, v in want.items())
        return d
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
