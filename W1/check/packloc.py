#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single place that resolves the W1 control pack.

Generation-1 tests each hard-coded a historical absolute path under
Downloads, which is why 44 test items failed on a clean host.  Resolution is
now: W1_PACK env, then repo-relative candidates, then an explicit error.
"""
from __future__ import annotations

import os
from pathlib import Path

TOKEN = "PACK_NOT_LOCATABLE"


def candidates(root: Path | None = None):
    here = (root or Path(__file__).resolve().parents[2])
    return [
        here / "18_W1_NF_CODEX_20261126T000627" / "control_pack" / "FHS-5_PLP_W1_NATIVE_FIRST",
        *sorted(here.glob("18_W1_NF_*/control_pack/FHS-5_PLP_W1_NATIVE_FIRST")),
        *sorted(here.glob("17_W1_NF_*/control_pack/FHS-5_PLP_W1_NATIVE_FIRST")),
        here / "16_W1_NF_CODEX_20261125T222954" / "control_pack" / "FHS-5_PLP_W1_NATIVE_FIRST",
    ]


def resolve_pack(root: Path | None = None) -> Path:
    env = os.environ.get("W1_PACK")
    if env:
        p = Path(env)
        if (p / "05_W1_SOURCE_MANIFEST.json").is_file():
            return p
        raise RuntimeError(f"{TOKEN}: W1_PACK={env} has no 05 manifest")
    for cand in candidates(root):
        if (cand / "05_W1_SOURCE_MANIFEST.json").is_file():
            return cand
    raise RuntimeError(f"{TOKEN}: no repo-relative W1 pack; set W1_PACK")


def resolve_s1_pack(wave: str, root: Path | None = None) -> Path:
    """Adopted S1 pack for a wave; never falls back to an NF pack."""
    here = (root or Path(__file__).resolve().parents[2])
    p = here / "S1_PACKS" / f"FHS-5_PLP_{wave}_NATIVE_FIRST"
    if not (p / f"05_{wave}_SOURCE_MANIFEST.json").is_file():
        raise RuntimeError(f"S1_PACK_NOT_LOCATABLE: {wave}")
    return p
