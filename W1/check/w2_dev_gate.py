#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 DEV gate (generation 2) — the only writer.

Fixes over generation 1:

  G1  READ_ONLY decisions can never reach the writer.  A `check()` result with
      writes_allowed=False (or mode=READ_ONLY) is refused by apply_patch with
      WRITE_NOT_AUTHORISED, before any byte is touched.  Generation 1 returned
      ok=True for a READ check and then applied the patch.
  G2  The patch is parsed structurally: every file section needs exactly one
      `--- a/P` and one `+++ b/P` with P equal on both sides, the section must
      match the declared operation, and renames/copies/mode-only/null targets
      are refused.  Generation 1 only looked at `+++ b/` lines.
  G3  recovery is mandatory and must be a known DEV kind; missing or unknown
      kinds are refused.  Generation 1 accepted an absent recovery block.
  G4  Post-state is re-read and compared; a patch that leaves the declared
      target unchanged is PATCH_NO_EFFECT, not a success.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

KNOWN_EFFECTS = {"REPOSITORY_WRITE", "REPOSITORY_READ"}
KNOWN_RECOVERY = {"REVERSE_PATCH_ON_COPY", "HOST_COMPENSATION"}
FORBIDDEN_RECOVERY = {"GIT_REVERT", "GIT_RESET", "GIT_CLEAN", "WHOLE_REPO_ROLLBACK"}

ADMISSION_SOURCE_PIN = "e961b8d1dd46d7725392ac05e92d3e473c855b1b0473fab97dd084afccb47695"


class GateError(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def _admission():
    import importlib
    import sys
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    mod = sys.modules.get("w2_admission")
    if mod is None:
        mod = importlib.import_module("w2_admission")
    f = Path(getattr(mod, "__file__", "") or "")
    if not f.is_file() or f.resolve().parent != here:
        raise GateError("ADMISSION_INTEGRITY", "foreign or missing module")
    got = hashlib.sha256(f.read_bytes()).hexdigest()
    if got != ADMISSION_SOURCE_PIN:
        raise GateError("ADMISSION_INTEGRITY", got[:16] + " != pin")
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


def _decision(checks, first_fail, repo, **extra):
    d = {"ok": first_fail is None, "first_fail": first_fail, "repo": str(repo),
         "checks": checks, "wrote": [], "product_calls": 0,
         "mode": "WRITE", "writes_allowed": True}
    d.update(extra)
    return d



def _structural_precheck(repo, write_set, recovery):
    """Pure structural predicates; no admission needed and no writes."""
    if not write_set:
        return ("write_set", "WRITE_SET_UNBOUND", "empty")
    for e in write_set:
        path = e.get("path") or ""
        if (not path or path.startswith("/") or "\\" in path
                or ".." in Path(path).parts or "*" in path):
            return ("write_set_shape", "WRITE_SET_UNBOUND", path)
        p = repo / path
        op = e.get("operation")
        if op == "ADD":
            if p.exists():
                return ("preimage:" + path, "WRITE_SET_UNBOUND", "expected absent")
        elif op in ("MODIFY", "DELETE"):
            if not p.is_file():
                return ("preimage:" + path, "WRITE_SET_UNBOUND", "missing")
            if not e.get("preimage_sha256"):
                return ("preimage:" + path, "WRITE_SET_UNBOUND", "preimage required")
            if e["preimage_sha256"] != sha256_file(p):
                return ("preimage:" + path, "WRITE_SET_UNBOUND", "drift")
        else:
            return ("preimage:" + path, "WRITE_SET_UNBOUND", f"bad operation {op}")
    kind = str(((recovery or {}).get("kind")) or "").upper()
    if not kind:
        return ("recovery_kind", "RECOVERY_KIND_MISMATCH", "missing")
    if kind in FORBIDDEN_RECOVERY:
        return ("recovery_kind", "RECOVERY_KIND_MISMATCH", kind)
    if kind not in KNOWN_RECOVERY:
        return ("recovery_kind", "RECOVERY_KIND_MISMATCH", "unknown " + kind)
    return None

def check(asserted, repo_root, write_set, request=None):
    repo = Path(repo_root).resolve()
    checks, first = [], {"v": None}

    def fail(name, tok, detail=""):
        checks.append({"check": name, "ok": False, "detail": str(detail)[:300]})
        if first["v"] is None:
            first["v"] = tok

    def ok(name, detail=""):
        checks.append({"check": name, "ok": True, "detail": str(detail)[:300]})

    effect = asserted.get("effect")
    if effect not in KNOWN_EFFECTS:
        fail("effect_token", "EFFECT_UNBOUND", effect)
        return _decision(checks, first["v"], repo)
    if effect == "REPOSITORY_READ":
        rc, head, err = _git(repo, "rev-parse", "HEAD")
        checks.append({"check": "effect_token", "ok": True, "detail": effect})
        return {"ok": rc == 0, "first_fail": None if rc == 0 else "REPO_UNBOUND",
                "repo": str(repo), "checks": checks, "wrote": [],
                "product_calls": 0, "mode": "READ_ONLY",
                "writes_allowed": False, "head": head}
    ok("effect_token", effect)

    pre = _structural_precheck(repo, write_set, asserted.get("recovery"))
    if pre is not None:
        fail(*pre)
        return _decision(checks, first["v"], repo)

    try:
        adm = _admission()
        fresh = adm.require(asserted.get("admission"), "DEV",
                            asserted.get("scope"), repo, write_set,
                            ops=[dict(e) for e in write_set],
                            request=request)
        ok("admission", fresh["verified_from"]["sha256"])
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
            declared = e.get("preimage_sha256")
            if not declared:
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND", "preimage required")
            elif declared != live:
                fail("preimage:" + e["path"], "WRITE_SET_UNBOUND",
                     {"declared": declared, "live": live})
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

    rec = asserted.get("recovery")
    kind = str((rec or {}).get("kind", "")).upper()
    if not kind:
        fail("recovery_kind", "RECOVERY_KIND_MISMATCH", "missing")
    elif kind in FORBIDDEN_RECOVERY:
        fail("recovery_kind", "RECOVERY_KIND_MISMATCH", kind)
    elif kind not in KNOWN_RECOVERY:
        fail("recovery_kind", "RECOVERY_KIND_MISMATCH", "unknown " + kind)
    else:
        ok("recovery_kind", kind)

    return _decision(checks, first["v"], repo)


def check_readonly(asserted, repo_root):
    return check(dict(asserted, effect="REPOSITORY_READ"), repo_root, [])


_FILE_HDR = re.compile(r"^(---|\+\+\+) ([ab])/(.+)$")
_META = re.compile(r"^(rename from|rename to|copy from|copy to|old mode|"
                   r"new mode|new file mode|deleted file mode|similarity index|"
                   r"dissimilarity index)\b")


def parse_patch(patch_text):
    """Return {path: {"operation": ADD|MODIFY|DELETE, "a": [..], "b": [..]}}."""
    out = {}
    cur = None
    new_file = False
    deleted = False
    for ln in patch_text.splitlines():
        if ln.startswith("diff --git "):
            cur = None
            new_file = False
            deleted = False
            continue
        m = _META.match(ln)
        if m:
            if m.group(1) in ("rename from", "rename to", "copy from", "copy to",
                              "old mode", "new mode"):
                raise GateError("PATCH_OP_UNSUPPORTED", ln)
            if m.group(1) == "new file mode":
                new_file = True
            if m.group(1) == "deleted file mode":
                deleted = True
            continue
        if ln.startswith("--- /dev/null") or ln.startswith("+++ /dev/null"):
            if ln.startswith("--- /dev/null") and new_file:
                cur = {"path": None, "a": ["/dev/null"], "b": []}
                continue
            raise GateError("PATCH_OP_UNSUPPORTED", "null target")
        h = _FILE_HDR.match(ln)
        if h:
            side, path = h.group(2), h.group(3)
            if path == "/dev/null":
                # A new file is the only legal null side, and only on a/.
                if side == "a" and new_file:
                    cur = {"path": None, "a": ["/dev/null"], "b": []}
                    continue
                raise GateError("PATCH_OP_UNSUPPORTED", "null target")
            if path.startswith("/") or "\\" in path or ".." in path.split("/"):
                raise GateError("PATCH_PATH_INVALID", path)
            if side == "a":
                if new_file:
                    cur = {"path": None, "a": ["/dev/null"], "b": []}
                    continue
                cur = {"path": path, "a": [path], "b": []}
            else:
                if cur is None:
                    raise GateError("PATCH_PATH_MISMATCH",
                                    f"b/{path} without matching a/")
                if cur["path"] is None:
                    if not new_file:
                        raise GateError("PATCH_PATH_MISMATCH",
                                        f"b/{path} without a/")
                    cur["path"] = path
                    cur["b"].append(path)
                    cur["operation"] = "ADD"
                    out[path] = cur
                    cur = None
                    continue
                if cur["path"] != path:
                    raise GateError("PATCH_PATH_MISMATCH",
                                    f"b/{path} without matching a/")
                cur["b"].append(path)
                cur["operation"] = "DELETE" if deleted else "MODIFY"
                out[path] = cur
                cur = None
    return out


def apply_patch(asserted, repo_root, write_set, patch_text, request=None):
    repo = Path(repo_root).resolve()
    d = check(asserted, repo_root, write_set, request)

    # G1: a READ_ONLY / non-writable decision can never reach the writer.
    if d.get("mode") == "READ_ONLY" or d.get("writes_allowed") is False:
        return {"ok": False, "first_fail": "WRITE_NOT_AUTHORISED",
                "checks": d["checks"], "wrote": [], "product_calls": 0,
                "repo": str(repo), "mode": d.get("mode"),
                "writes_allowed": False}
    if not d["ok"]:
        d["wrote"] = []
        return d

    try:
        sections = parse_patch(patch_text)
    except GateError as exc:
        return {"ok": False, "first_fail": exc.token, "detail": exc.detail,
                "checks": d["checks"], "wrote": [], "product_calls": 0,
                "repo": str(repo)}
    want = {e["path"]: e["operation"] for e in write_set}
    if set(sections) != set(want):
        return {"ok": False, "first_fail": "WRITE_SET_UNBOUND",
                "detail": {"patch": sorted(sections), "declared": sorted(want)},
                "checks": d["checks"], "wrote": [], "product_calls": 0,
                "repo": str(repo)}
    for path, sec in sections.items():
        if sec["operation"] != want[path]:
            return {"ok": False, "first_fail": "WRITE_SET_UNBOUND",
                    "detail": {"path": path, "patch": sec["operation"],
                               "declared": want[path]},
                    "checks": d["checks"], "wrote": [], "product_calls": 0,
                    "repo": str(repo)}

    before = {e["path"]: sha256_file(repo / e["path"]) for e in write_set
              if (repo / e["path"]).is_file()}
    chk = subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(repo),
                          "apply", "--check", "-"],
                         input=patch_text.encode("utf-8"), capture_output=True)
    if chk.returncode != 0:
        return {"ok": False, "first_fail": "PATCH_NOT_APPLICABLE",
                "checks": d["checks"], "wrote": [], "product_calls": 0,
                "repo": str(repo),
                "detail": (chk.stderr or b"")[:200].decode("utf-8", "replace")}
    app = subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(repo),
                          "apply", "-"],
                         input=patch_text.encode("utf-8"), capture_output=True)
    if app.returncode != 0:
        return {"ok": False, "first_fail": "PATCH_APPLY_FAILED",
                "checks": d["checks"], "wrote": [], "product_calls": 0,
                "repo": str(repo),
                "detail": (app.stderr or b"")[:200].decode("utf-8", "replace")}

    d["checks"].append({"check": "patch_structure", "ok": True,
                        "detail": sorted(sections)})
    post, unchanged = {}, []
    for e in write_set:
        p = repo / e["path"]
        post[e["path"]] = sha256_file(p) if p.is_file() else None
        if before.get(e["path"]) == post[e["path"]]:
            unchanged.append(e["path"])
    rc, porcelain, _ = _git(repo, "status", "--porcelain=v2", "--untracked-files=all")
    dirty = {ln.split()[-1] for ln in porcelain.splitlines() if ln.strip()}
    foreign = sorted(dirty - set(want))
    d["checks"].append({"check": "post_readback", "ok": not unchanged,
                        "detail": {"unchanged": unchanged}})
    if foreign:
        d["checks"].append({"check": "write_set_respected", "ok": False,
                            "detail": foreign})
        return {"ok": False, "first_fail": "WRITE_SET_UNBOUND", "checks": d["checks"],
                "wrote": sorted(sections), "product_calls": 0, "repo": str(repo),
                "postimage_sha256": post, "unexpected": foreign}
    if unchanged:
        return {"ok": False, "first_fail": "PATCH_NO_EFFECT", "checks": d["checks"],
                "wrote": sorted(sections), "product_calls": 0, "repo": str(repo),
                "postimage_sha256": post}
    d.update(ok=True, first_fail=None, wrote=sorted(sections),
             preimage_sha256=before, postimage_sha256=post,
             recovery_kind=(asserted.get("recovery") or {}).get("kind"))
    return d


def reverse(patch_text, repo_root, write_set, expected_preimage):
    repo = Path(repo_root).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="rev_", dir=str(repo.parent)))
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
        if p.returncode != 0:
            return {"ok": False, "first_fail": "REVERSE_APPLY_FAILED",
                    "checks": [{"check": "reverse_apply", "ok": False,
                                "detail": out[:300]}]}
        restored = {e["path"]: (sha256_file(tmp / e["path"])
                                if (tmp / e["path"]).is_file() else None)
                    for e in write_set}
        match = all(restored.get(k) == v for k, v in (expected_preimage or {}).items())
        return {"ok": match,
                "first_fail": None if match else "REVERSE_PREIMAGE_MISMATCH",
                "checks": [{"check": "reverse_apply", "ok": True, "detail": ""},
                           {"check": "restored_matches_preimage", "ok": match,
                            "detail": restored}],
                "restored": restored}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
