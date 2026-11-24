#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replay source, case, projection and manifest hashes without executing any case."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def d(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    pack = Path(a.root).resolve(strict=True)
    sm = json.loads((pack / "SOURCE_MANIFEST.json").read_text(encoding="utf-8-sig"))
    wave = json.loads((pack / "00_WAVE_RUN_MANIFEST.json").read_text(encoding="utf-8-sig"))
    tq = json.loads((pack / "05_PLANNED_TQAEP.json").read_text(encoding="utf-8-sig"))
    fm = json.loads((pack / "PACKAGE_FILE_MANIFEST.json").read_text(encoding="utf-8-sig"))
    bad = []
    for s in sm["sources"]:
        if d(pack / s["path"]) != s["sha256"]:
            bad.append("source:" + s["source_id"])
    for c in wave["cases"]:
        for stem in ("oracle", "fixture"):
            if d(pack / c[f"{stem}_path"]) != c[f"{stem}_sha256"]:
                bad.append(f"{stem}:{c['case_id']}")
    if tq["projection_of_sha256"] != d(pack / "05_PLANNED_TQAEP.md"):
        bad.append("projection")
    for e in fm["files"]:
        if d(pack / e["path"]) != e["sha256"]:
            bad.append("file:" + e["path"])
    out = {
        "status": "REPLAY_OK" if not bad else "REPLAY_MISMATCH",
        "sources": len(sm["sources"]), "cases": len(wave["cases"]),
        "files": len(fm["files"]), "mismatches": bad,
        "source_manifest_sha256": d(pack / "SOURCE_MANIFEST.json"),
        "package_file_manifest_sha256": d(pack / "PACKAGE_FILE_MANIFEST.json"),
        "tqaep_md_sha256": d(pack / "05_PLANNED_TQAEP.md"),
        "claim_ceiling": "AUTHOR_DESIGN_ONLY",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if not bad else 2


if __name__ == "__main__":
    sys.exit(main())
