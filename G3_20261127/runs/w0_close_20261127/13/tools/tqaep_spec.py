#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Frozen SAMPLE oracle + the W0 TQAEP case table (24 original + 10 NF)."""
from __future__ import annotations

import json
from pathlib import Path

import lib

FIX = lib.REPO / "fixtures"

SAMPLE = {
    "R1": {"fixture": "case_ok.md", "exit": 0, "status": "COMPLETE", "provided": ["A", "B"], "missing": []},
    "R2": {"fixture": "case_missing.md", "exit": 2, "status": "MISSING", "provided": ["A"], "missing": ["B"]},
    "R3": {"fixture": "case_dup.md", "exit": 3, "status": "INVALID_DUP"},
    "R5": {"fixture": "case_bad_utf8.md", "exit": 3, "status": "INVALID_ENCODING"},
    "R6": {"fixture": "case_ok.md", "bad_sha": True, "exit": 3, "status": "SHA_MISMATCH"},
    "R7": {"fixture": "case_ambiguous.md", "exit": 3, "status": "INVALID_FORMAT"},
    "R8": {"fixture": "case_malformed.md", "exit": 3, "status": "INVALID_FORMAT"},
    "R9": {"fixture": "case_ok.md", "twice": True, "exit": 0, "status": "COMPLETE"},
    "R10": {"fixture": "case_ok.md", "output": True, "exit": 0, "status": "COMPLETE"},
}


def oracle() -> dict:
    return {
        "schema": "FHS5.W0NF.BriefcheckOracle@2",
        "pack_manifest_sha256": lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json"),
        "candidate_commit": lib.git("rev-parse", "HEAD"),
        "source_sha256": lib.sha_file(lib.REPO / "requirements.md"),
        "fixtures": {p.name: lib.sha_file(p) for p in sorted(FIX.glob("*.md"))},
        "cases": SAMPLE,
        "path_expected": {"exit": 3, "status": "INVALID_PATH", "canary": "OUTSIDE_CANARY_DO_NOT_READ"},
        "json_schema_keys": ["source_sha256", "provided", "missing", "status"],
        "status_enum": ["COMPLETE", "MISSING", "INVALID_DUP", "INVALID_PATH", "INVALID_ENCODING",
                        "SHA_MISMATCH", "INVALID_FORMAT"],
    }


CASES = [
    # id, group, requirement, kind, scenario
    ("F5-W0-T01", "T", "NF-R01", "POS", "source read + SHA/span"),
    ("F5-W0-T02", "T", "NF-R01", "NEG", "one-byte source mutation rejected"),
    ("F5-W0-T03", "T", "NF-R02", "NEG", "missing child B"),
    ("F5-W0-T04", "T", "NF-R05", "NEG", "self-made ID/ACK has no authority"),
    ("F5-W0-T05", "T", "NF-R02", "NEG", "Guide scope drift"),
    ("F5-W0-T06", "T", "NF-R03", "SEC", "path escape set"),
    ("F5-W0-T07", "T", "NF-R09", "EDGE", "unknown schema version rejected"),
    ("F5-W0-T08", "T", "NF-R09", "NEG", "capability visible but unbound"),
    ("F5-W0-T09", "T", "NF-R04", "NEG", "phase overreach detected"),
    ("F5-W0-T10", "T", "NF-R04", "NEG", "gate cycle detected"),
    ("F5-W0-T11", "T", "NF-R04", "NEG", "false permit no-op"),
    ("F5-W0-T12", "T", "NF-R04", "NEG", "unknown effect alias"),
    ("F5-W0-T13", "T", "NF-R04", "POS", "authorized DEV+OPS with readback"),
    ("F5-W0-T14", "T", "NF-R04", "NEG", "exit 0 but wrong state"),
    ("F5-W0-T15", "T", "NF-R05", "NEG", "challenger modifies oracle"),
    ("F5-W0-T16", "T", "NF-R05", "EDGE", "stale raw after candidate change"),
    ("F5-W0-T17", "T", "NF-R05", "NEG", "text-only claim is unreproduced"),
    ("F5-W0-T18", "T", "NF-R06", "NEG", "unavailable != zero"),
    ("F5-W0-T19", "T", "NF-R06", "NEG", "FAR false close refused"),
    ("F5-W0-T20", "T", "NF-R07", "EDGE", "new raw requalifies same first-fail"),
    ("F5-W0-T21", "T", "NF-R07", "NEG", "homogeneous redispatch stopped"),
    ("F5-W0-T22", "T", "NF-R09", "NEG", "closeout without checker != release"),
    ("F5-W0-T23", "T", "NF-R10", "SEC", "secret sentinel redacted"),
    ("F5-W0-T24", "T", "NF-R08", "POS", "Generic OFF read; FHS profile scoped"),
    ("NF-T01", "NF", "NF-R08", "POS", "no legacy providers imported"),
    ("NF-T02", "NF", "NF-R01/NF-R03", "POS", "no OriginalReader; real file pins"),
    ("NF-T03", "NF", "NF-R04/NF-R10", "POS", "no registry/issuer; real sandbox effect"),
    ("NF-T04", "NF", "NF-R05", "POS", "no case registry; stdlib runner"),
    ("NF-T05", "NF", "NF-R03/NF-R08", "POS", "Bridge OFF direct read parity"),
    ("NF-T06", "NF", "NF-R06/NF-R07", "POS", "FAR OFF direct fix allowed"),
    ("NF-T07", "NF", "NF-R01..R06", "POS", "five parties individual"),
    ("NF-T08", "NF", "NF-R01..R07", "POS", "combined loop end-to-end"),
    ("NF-T09", "NF", "NF-R07", "POS", "red -> patch -> affected retest"),
    ("NF-T10", "NF", "NF-R09", "POS", "consumer reads handoff; wrong pin refused"),
]


def bridge_tqaep(pack_root: Path, identity: dict | None = None) -> dict:
    cases = []
    for key, spec in SAMPLE.items():
        name = spec["fixture"]
        fx = pack_root / "cases" / name
        orc = pack_root / "cases" / ("oracle_" + key + ".json")
        clause = next(
            (ln for ln in (lib.REPO / "requirements.md").read_text(encoding="utf-8").splitlines()
             if f"SAMPLE-{key}" in ln),
            "SAMPLE-" + key,
        )
        cases.append({
            "case_id": f"SAMPLE-{key}",
            "kind": "POS" if spec["exit"] == 0 else "NEG",
            "requirement_ref": f"SAMPLE-{key}",
            "fixture_path": str(fx.relative_to(pack_root)).replace("\\", "/"),
            "oracle_path": str(orc.relative_to(pack_root)).replace("\\", "/"),
            "fixture_sha256": lib.sha_file(fx),
            "oracle_sha256": lib.sha_file(orc),
            "clause_text": clause,
            "clause_start_line": 1,
            "clause_end_line": 1,
            "requirement_source_sha256": lib.sha_file(lib.REPO / "requirements.md"),
        })
    if identity is None:
        identity = {
            "project_id": "FHS-5_PLP",
            "subject_id": "FHS-5_PLP/W0",
            "scope": "FHS-5/W0/B0-NF",
            "wave_id": "FHS-5_PLP/W0",
            "batch_id": "FHS-5/W0/B0-NF",
            "source_manifest_sha256": lib.sha_file(pack_root / "SOURCE_MANIFEST.json")
            if (pack_root / "SOURCE_MANIFEST.json").is_file() else lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json"),
        }
    return {
        "schema": "FHS5.W0NF.PlannedTQAEP@1",
        "identity": identity,
        "cases": cases,
        "not_covered": ["full W1 38+28", "C16/EC-36/local47", "FARP30/local35"],
    }
