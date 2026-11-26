#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bounded repair routing: protected-target refusal, exact patch, retest, freeze.

An advice or NextOperation is not an authority. Every write binds a real
preimage, an in-root target and a reverse patch.
"""
from __future__ import annotations

import os
import re

from w3_common import W3Error, resolve_inside, sha256_bytes, sha256_file, tree_digest

PROTECTED_EXACT = {
    "W1/check/test_j1_strict.py",
    "W2_CURRENT.json",
    "oracle.json",
    "threshold.json",
}
PROTECTED_PREFIXES = (
    "assets/oracles/",
    "assets/fixtures/",
    "subject/",
    "24_",
    "25_",
)


def is_protected(rel: str) -> bool:
    s = str(rel).replace("\\", "/")
    if s in PROTECTED_EXACT:
        return True
    return any(s.startswith(p) for p in PROTECTED_PREFIXES)


def guard_write(rel, allowed_root, in_root=None):
    if is_protected(rel):
        raise W3Error("WRITE_SCOPE_VIOLATION", rel)
    target = resolve_inside(allowed_root, rel)
    if in_root and not os.path.realpath(target).startswith(os.path.realpath(in_root)):
        raise W3Error("WRITE_SCOPE_VIOLATION", "outside run root")
    return target


def apply_exact_patch(rel, allowed_root, old, new, preimage_sha256):
    target = guard_write(rel, allowed_root)
    if not os.path.isfile(target):
        raise W3Error("PREIMAGE_MISSING", rel)
    raw = open(target, "rb").read()
    if sha256_bytes(raw) != preimage_sha256:
        raise W3Error("PREIMAGE_MISMATCH", rel)
    text = raw.decode("utf-8")
    if text.count(old) != 1:
        raise W3Error("PATCH_AMBIGUOUS", rel)
    patched = text.replace(old, new, 1)
    open(target, "wb").write(patched.encode("utf-8"))
    return {
        "path": rel,
        "preimage_sha256": preimage_sha256,
        "post_sha256": sha256_file(target),
        "bytes": os.path.getsize(target),
        "reverse_patch": {"old": new, "new": old},
    }


def restore_exact(rel, allowed_root, preimage_bytes: bytes):
    target = guard_write(rel, allowed_root)
    open(target, "wb").write(preimage_bytes)
    return {"path": rel, "restored_sha256": sha256_file(target), "bytes": os.path.getsize(target)}


def change_cone(changed_paths):
    cases = []
    modules = []
    for p in changed_paths:
        s = p.replace("\\", "/")
        m = re.match(r"W3/(impl|check)/([A-Za-z0-9_]+)\.py$", s)
        if m:
            modules.append(m.group(2))
        cases.append(s)
    affected_cases = []
    if "w3_repair" in modules or "w3_common" in modules:
        affected_cases += ["W3-FR16-01", "W3-FR17-01"]
    if "w3_far" in modules:
        affected_cases += ["W3-FAR-01", "W3-FAR-02"]
    if "w3_guide2" in modules:
        affected_cases += ["W3-G2-01", "W3-R3-02"]
    return {
        "changed_paths": changed_paths,
        "modules": sorted(set(modules)),
        "affected_cases": sorted(set(affected_cases)) or ["W3-RUN-01"],
        "scope_limited": True,
    }


def new_freeze(root):
    return tree_digest(root)
