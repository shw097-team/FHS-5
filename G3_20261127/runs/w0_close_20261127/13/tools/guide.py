#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal-but-real Guide reference: PACKAGE_FIRST ThinStart (Touch1) and
ThinResume (Touch2) with the nine-key delta and scope-drift refusal."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

NINE = [
    "source_sha", "candidate_sha", "evidence_sha", "requirement_ids", "case_ids",
    "findings", "next_action", "stop_conditions", "not_covered",
]
STOP = ["pack digest mismatch", "no write-set/preimage", "path escape/secret", "false permit"]


def pack_check(pack: Path) -> dict:
    manifest = lib.load_json(pack / "05_W0_SOURCE_MANIFEST.json")
    files = []
    for e in manifest["pack_files"]:
        p = pack / e["path"]
        h = lib.sha_file(p) if p.is_file() else None
        files.append({"path": e["path"], "ok": h == e["sha256"], "sha256": h})
    return {"manifest": manifest, "files": files, "ok": all(f["ok"] for f in files) and len(files) == 5}


def body_sufficient(pack: Path) -> tuple[bool, list[str]]:
    need = {"00_W0_PI_PD.md": ["00.1 Wave Goal", "00.2 FUO", "00.3 Done"],
            "03_W0_TQAEP.md": ["NF-T01", "F5-W0-T01"],
            "04_W0_START_THIN_PROMPT.md": ["B0 Done"]}
    missing = []
    for name, anchors in need.items():
        text = (pack / name).read_text(encoding="utf-8-sig")
        for a in anchors:
            if a not in text:
                missing.append(f"{name}:{a}")
    return (not missing, missing)


def touch1(pack: Path, requested_scope: str, goal: str, contracts: Path | None = None) -> dict:
    pc = pack_check(pack)
    suff, missing = body_sufficient(pack)
    mode = "PACKAGE_FIRST" if suff else "CONTEXT_AUGMENTED"
    allowed = str(pack.resolve())
    scope_ok = Path(requested_scope).resolve().is_relative_to(Path(allowed))
    contract_context = None
    if contracts is not None and contracts.is_dir():
        pins = {}
        reqs = None
        for name in ("pi", "pd", "dev_ecp", "ops_ecp"):
            p = contracts / f"{name}.json"
            if p.is_file():
                pins[name] = lib.sha_file(p)
        pi_path = contracts / "pi.json"
        if pi_path.is_file():
            pi = lib.load_json(pi_path)
            reqs = [c.get("id") for c in pi.get("children") or []]
            source_ok = any(s.get("sha256") == lib.sha_file(pack / "05_W0_SOURCE_MANIFEST.json")
                            for s in pi.get("source_refs") or [])
        else:
            source_ok = False
        contract_context = {
            "pins": pins,
            "requirement_ids": reqs or [],
            "source_manifest_match": bool(source_ok),
            "contract_count": len(pins),
        }
    delta = {
        "source_sha": lib.sha_file(pack / "05_W0_SOURCE_MANIFEST.json"),
        "candidate_sha": lib.git("rev-parse", "HEAD"),
        "evidence_sha": None,
        "requirement_ids": (contract_context or {}).get("requirement_ids")
        or ["SAMPLE-R1", "SAMPLE-R2", "SAMPLE-R3", "SAMPLE-R4", "NF-R01"],
        "case_ids": ["F5-W0-T01", "F5-W0-T03", "F5-W0-T06", "F5-W0-T13", "NF-T01"],
        "findings": [],
        "next_action": "execute B0 current READY slice",
        "stop_conditions": STOP,
        "not_covered": ["HERMES/GPT host execution", "full U26/QA26/38+28/C16 denominators", "release"],
    }
    return {
        "schema": "FHS5.W0NF.GuideThinStart@1",
        "mode": mode,
        "goal": goal,
        "pack": str(pack),
        "pack_digest": lib.sha_file(pack / "05_W0_SOURCE_MANIFEST.json"),
        "files": pc["files"],
        "pack_ok": pc["ok"],
        "body_missing": missing,
        "scope_requested": requested_scope,
        "scope_allowed": allowed,
        "scope_verdict": "IN_SCOPE" if scope_ok else "SCOPE_DRIFT",
        "scope_exit": 0 if scope_ok else 3,
        "done": ["five-party individual+combined", "DEV/OPS readback", "Challenge/FAR",
                 "OFF", "consumer"],
        "limits": ["local CODEX scope", "no external admin/release", "no HERMES/GPT host claim"],
        "delta_keys": NINE,
        "delta": delta,
        "contract_context": contract_context,
    }


def touch2(prev: dict, new_evidence_sha: str) -> dict:
    delta = dict(prev.get("delta") or {})
    no_delta = new_evidence_sha == delta.get("evidence_sha") or (not new_evidence_sha and not delta.get("evidence_sha"))
    if no_delta:
        return {
            "schema": "FHS5.W0NF.GuideThinResume@1",
            "state": "HOLD_NO_DELTA",
            "exit": 0,
            "message": "same source/candidate/evidence/FirstFail; no homogeneous redispatch",
            "delta": delta,
        }
    delta["evidence_sha"] = new_evidence_sha
    return {
        "schema": "FHS5.W0NF.GuideThinResume@1",
        "state": "RESUME",
        "exit": 0,
        "delta_keys": NINE,
        "delta": delta,
        "next_action": "re-run only the affected ChangeCone",
        "resume_prompt": (
            "Continue FHS-5/W0 B0-NF from the frozen pack/pins. "
            "Use the nine-key delta; do not widen scope; stop on stop_conditions."
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=str(lib.PACK))
    ap.add_argument("--goal", default="Complete W0 B0-NF five-party loop")
    ap.add_argument("--requested-scope", default=str(lib.PACK))
    ap.add_argument("--out", default=str(lib.PARTIES / "guide" / "thin_start.json"))
    ap.add_argument("--resume-evidence", default="")
    ap.add_argument("--contracts", default="")
    a = ap.parse_args()
    start = touch1(Path(a.pack), a.requested_scope, a.goal,
                   Path(a.contracts) if a.contracts else None)
    lib.write_json(Path(a.out), start)
    resumed = touch2(start, a.resume_evidence)
    resume_path = Path(a.out).with_name("thin_resume.json")
    lib.write_json(resume_path, resumed)
    print(json.dumps({"mode": start["mode"], "pack_ok": start["pack_ok"],
                      "scope": start["scope_verdict"], "resume": resumed["state"]}, ensure_ascii=False))
    return 0 if start["pack_ok"] and start["scope_exit"] == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
