#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2/S3 DEV gate (generation 2) — check / apply_patch / reverse.

Same contract shape as w2_dev_gate.py, with these differences:

  H1  The admission module and its trust config are resolved from *this file's
      directory* — never from the caller, an environment variable, or the repo
      being written.  The write root is a different tree.
  H2  Refusal is total: no git write, no file write, `wrote == []`,
      `product_calls == 0`, and the world digest is re-read to prove it.
  H3  apply_patch re-checks, applies, then re-reads every touched file and
      returns pre/post digests plus the world digest.
  H4  reverse works on a copy and proves restored == preimage; it never calls
      git reset / checkout / clean.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

KNOWN_EFFECTS = {"REPOSITORY_WRITE", "REPOSITORY_READ"}
FORBIDDEN_RECOVERY = {"GIT_REVERT", "GIT_RESET", "GIT_CLEAN", "WHOLE_REPO_ROLLBACK"}


class GateError(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _admission():
    import importlib
    import sys
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    mod = sys.modules.get("admission")
    if mod is None:
        mod = importlib.import_module("admission")
    if Path(mod.__file__).resolve().parent != Path(here).resolve():
        raise GateError("ADMISSION_INTEGRITY", "module loaded from a foreign path")
    return mod


def _git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def world_digest(root: Path) -> str:
    rows = []
    for p in sorted(root.rglob("*")):
        if "__pycache__" in p.parts or ".pytest_cache" in p.parts:
            continue
        if p.is_file() and ".git" not in p.parts:
            rows.append(f"{p.relative_to(root).as_posix()}|{sha256_file(p)}")
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def check(asserted, repo_root, write_set, request=None):
    repo = Path(repo_root).resolve()
    checks, first = [], {"v": None}

    def fail(name, tok, detail=""):
        checks.append({"check": name, "ok": False, "detail": str(detail)[:300]})
        if first["v"] is None:
            first["v"] = tok
        return False

    def ok(name, detail=""):
        checks.append({"check": name, "ok": True, "detail": str(detail)[:300]})
        return True

    effect = asserted.get("effect")
    if effect not in KNOWN_EFFECTS:
        fail("effect_token", "EFFECT_UNBOUND", effect)
        return _decision(checks, first["v"], repo)
    if effect == "REPOSITORY_READ":
        rc, head, _ = _git(repo, "rev-parse", "HEAD")
        return {"ok": rc == 0, "first_fail": None if rc == 0 else "REPO_UNBOUND",
                "mode": "READ_ONLY", "writes_allowed": False, "repo": str(repo),
                "checks": checks, "wrote": [], "product_calls": 0,
                "head": head}
    ok("effect_token", effect)

    try:
        adm = _admission()
        fresh = adm.require(asserted.get("admission"), "DEV",
                            asserted.get("scope"), repo, write_set, request)
        ok("admission", fresh["verified_from"]["trust_sha256"])
    except Exception as exc:  # noqa: BLE001
        fail("admission", getattr(exc, "token", "FALSE_AUTHORITY"), str(exc)[:200])
        return _decision(checks, first["v"], repo)

    if asserted.get("scope") != fresh["scope"]:
        fail("scope", "SCOPE_MISMATCH", asserted.get("scope"))
    else:
        ok("scope", fresh["scope"])

    rc, head, err = _git(repo, "rev-parse", "HEAD")
    if rc != 0:
        fail("repo_head", "REPO_UNBOUND", err)
        return _decision(checks, first["v"], repo)
    if asserted.get("head") != head:
        fail("repo_head", "REPO_HEAD_MISMATCH",
             {"asserted": asserted.get("head"), "live": head})
        return _decision(checks, first["v"], repo)
    ok("repo_head", head)

    if not write_set:
        fail("write_set", "WRITE_SET_UNBOUND", "empty")
        return _decision(checks, first["v"], repo)

    for e in write_set:
        p = repo / e["path"]
        op = e.get("operation")
        if op == "ADD":
            if p.exists():
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", "expected absent")
            else:
                ok("preimage:" + e["path"], "absent")
        elif op in ("MODIFY", "DELETE"):
            if not p.is_file():
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", "missing")
                continue
            live = sha256_file(p)
            if not e.get("preimage_sha256"):
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", "declared preimage required")
            elif e["preimage_sha256"] != live:
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND",
                     {"declared": e["preimage_sha256"], "live": live})
            else:
                ok("preimage:" + e["path"], live)
        else:
            fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", f"bad operation {op}")

    rc, porcelain, _ = _git(repo, "status", "--porcelain=v2", "--untracked-files=all")
    if rc == 0:
        dirty = {ln.split()[-1] for ln in porcelain.splitlines() if ln.strip()}
        foreign = sorted(dirty - {e["path"] for e in write_set})
        if foreign:
            fail("dirty_preservation", "REPO_UNBOUND", foreign[:5])
        else:
            ok("dirty_preservation", f"{len(dirty)} dirty in write set")

    rec = asserted.get("recovery") or {}
    if str(rec.get("kind", "")).upper() in FORBIDDEN_RECOVERY:
        fail("recovery_kind", "RECOVERY_KIND_MISMATCH", rec.get("kind"))
    else:
        ok("recovery_kind", rec.get("kind"))

    return _decision(checks, first["v"], repo)


def _decision(checks, first_fail, repo):
    return {"ok": first_fail is None, "first_fail": first_fail, "repo": str(repo),
            "checks": checks, "wrote": [], "product_calls": 0,
            "world_before": world_digest(repo) if repo.is_dir() else None}


def apply_patch(asserted, repo_root, write_set, patch_text, request=None):
    repo = Path(repo_root).resolve()
    d = check(asserted, repo_root, write_set, request)
    if not d["ok"]:
        d["world_after"] = world_digest(repo)
        d["world_unchanged"] = d["world_after"] == d.get("world_before")
        return d

    before = {e["path"]: sha256_file(repo / e["path"]) for e in write_set}
    p = subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(repo),
                        "apply", "--check", "-"],
                       input=patch_text.encode("utf-8"), capture_output=True)
    if p.returncode != 0:
        d.update(ok=False, first_fail="PATCH_NOT_APPLICABLE",
                 world_after=world_digest(repo), world_unchanged=True)
        d["checks"].append({"check": "patch_apply_check", "ok": False,
                            "detail": (p.stderr or b"")[:200].decode("utf-8", "replace")})
        return d

    touched = {ln[6:] for ln in patch_text.splitlines() if ln.startswith("+++ b/")}
    outside = sorted(touched - {e["path"] for e in write_set})
    if outside:
        d.update(ok=False, first_fail="WRITE_SET_UNBOUND",
                 world_after=world_digest(repo), world_unchanged=True)
        d["checks"].append({"check": "patch_scope", "ok": False, "detail": outside})
        return d

    p = subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(repo),
                        "apply", "-"],
                       input=patch_text.encode("utf-8"), capture_output=True)
    if p.returncode != 0:
        d.update(ok=False, first_fail="PATCH_APPLY_FAILED",
                 world_after=world_digest(repo))
        d["checks"].append({"check": "patch_apply", "ok": False,
                            "detail": (p.stderr or b"")[:200].decode("utf-8", "replace")})
        return d

    post = {e["path"]: sha256_file(repo / e["path"]) for e in write_set}
    unchanged = [k for k in before if post[k] == before[k]]
    d["checks"].append({"check": "patch_apply", "ok": True, "detail": sorted(touched)})
    d["checks"].append({"check": "post_readback", "ok": not unchanged,
                        "detail": {"changed": sorted(set(post) - set(unchanged))}})
    d.update(ok=not unchanged,
             first_fail=None if not unchanged else "PATCH_NO_EFFECT",
             wrote=sorted(touched), preimage_sha256=before,
             postimage_sha256=post, world_after=world_digest(repo))
    d["world_unchanged"] = d["world_after"] == d.get("world_before")
    return d


def reverse(patch_text, repo_root, write_set, expected_preimage):
    repo = Path(repo_root).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="rev_", dir=str(repo.parent)))
    d = {"ok": False, "first_fail": None, "checks": []}
    try:
        for e in write_set:
            src = repo / e["path"]
            dst = tmp / e["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        subprocess.run(["git", "init", "-q", str(tmp)], capture_output=True)
        p = subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(tmp),
                            "apply", "-R", "-"],
                           input=patch_text.encode("utf-8"), capture_output=True)
        out = ((p.stdout or b"") + (p.stderr or b"")).decode("utf-8", "replace")
        d["checks"].append({"check": "reverse_apply", "ok": p.returncode == 0,
                            "detail": out[:300]})
        if p.returncode != 0:
            d["first_fail"] = "REVERSE_APPLY_FAILED"
            return d
        restored = {}
        for e in write_set:
            f = tmp / e["path"]
            restored[e["path"]] = sha256_file(f) if f.is_file() else None
        match = all(restored.get(k) == v for k, v in (expected_preimage or {}).items())
        d["checks"].append({"check": "restored_matches_preimage", "ok": match,
                            "detail": restored})
        d.update(ok=match, first_fail=None if match else "REVERSE_PREIMAGE_MISMATCH",
                 restored=restored)
        return d
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
