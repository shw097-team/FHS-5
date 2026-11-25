#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the W0 evidence manifest (hash index + claims) and its .sha256."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

INCLUDE = ["01_PACK", "02_CANDIDATE", "03_PARTIES", "04_DEV_OPS", "05_TQAEP",
           "06_CHECKER", "openspec", "tools"]
EXCLUDE_PARTS = {".git", "__pycache__", "tmp"}
EXCLUDE_PREFIXES = (
    "02_CANDIDATE/repo/",
    "06_CHECKER/full/checker-wt/",
    "06_CHECKER/full/mutant/",
    "06_CHECKER/full/mut_root/",
    "06_CHECKER/full/root/",
    "06_CHECKER/full/outside/",
    "06_CHECKER/smoke/checker-wt/",
    "06_CHECKER/smoke/mutant/",
    "06_CHECKER/smoke/mut_root/",
    "06_CHECKER/smoke/root/",
    "06_CHECKER/smoke/outside/",
)


def index() -> list[dict]:
    rows = []
    for top in INCLUDE:
        base = lib.ROOT / top
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(lib.ROOT).as_posix()
            if any(part in EXCLUDE_PARTS for part in p.parts):
                continue
            if rel.startswith(EXCLUDE_PREFIXES):
                continue
            rows.append({"path": rel, "bytes": len(p.read_bytes()), "sha256": lib.sha_file(p)})
    return rows


def main():
    files = index()
    recs = sorted((lib.ROOT / "05_TQAEP" / "receipts").glob("*.json"))
    summary = lib.load_json(lib.ROOT / "05_TQAEP" / "summary.json")
    challenge = lib.load_json(lib.PARTIES / "challenge" / "challenge.json")
    tpm = lib.load_json(lib.PARTIES / "tpm" / "tpm_gate.json")
    bridge = lib.load_json(lib.PARTIES / "bridge" / "bridge_summary.json")
    ops = lib.load_json(lib.ROOT / "04_DEV_OPS" / "ops.json")
    dev = lib.load_json(lib.ROOT / "04_DEV_OPS" / "dev_patch.json")
    far = lib.load_json(lib.PARTIES / "far" / "far.json")
    manifest = {
        "schema": "FHS5.W0NF.EvidenceManifest@1",
        "generated_at": lib.now(),
        "root": str(lib.ROOT),
        "pack_manifest_sha256": lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json"),
        "candidate": {
            "head": lib.git("rev-parse", "HEAD"),
            "tree": lib.git("rev-parse", "HEAD^{tree}"),
            "preimage": dev["preimage"]["head"],
            "fixtures": lib.load_json(lib.TQAEP / "oracle.json")["fixtures"],
        },
        "oracle_sha256": lib.sha_file(lib.TQAEP / "oracle.json"),
        "summary_sha256": lib.sha_file(lib.TQAEP / "summary.json"),
        "counts": summary["counts"],
        "receipts": {p.name: lib.sha_file(p) for p in recs},
        "parties": {
            "tpm": {"exit": tpm["reviewer"]["exit"],
                    "state": tpm["reviewer"]["stdout"].get("state"),
                    "defects": tpm["reviewer"]["stdout"].get("defects"),
                    "unbound": tpm["reviewer"]["stdout"].get("unbound"),
                    "missing_b": tpm["gates"]["missing_b"]["status"],
                    "source_negative": tpm["gates"]["source_negative"]["status"]},
            "guide": {"mode": "PACKAGE_FIRST", "delta_keys": 9},
            "bridge": {"impl_sha256": bridge["bridge_sha256"],
                       "inspect_counts": bridge["results"]["inspect_counts"],
                       "security": bridge["security"]},
            "challenge": {"verdict": challenge["verdict"], "checks": len(challenge["checks"]),
                          "findings": len(challenge["findings"]), "pins": challenge["pins"],
                          "symlink_tested": challenge.get("symlink_tested")},
            "far": {"finding": far["finding"]["id"], "alternatives": len(far["alternatives"]),
                    "keys": far["keys"], "close_no_raw": far["close_policy"]["no_raw"]["status"]},
        },
        "native": {"dev_verdict": dev["verdict"], "red_exit": dev["red"]["exit"],
                   "retest_suite_exit": dev["retest"]["suite_exit"],
                   "ops_verdict": ops["verdict"], "legacy_imports": ops["legacy_imports"],
                   "parity": ops["parity"]},
        "claims": {
            "B0": "B0_NF_VALIDATED",
            "W0": "W0_NF_VALIDATED",
            "W1_technical": "W1_TECHNICALLY_READY",
            "W1_execution": "NOT_CLAIMED",
            "release": "NOT_CLAIMED",
            "different_principal_independence": "NOT_CLAIMED",
            "other_hosts": "NOT_CLAIMED",
        },
        "superseded_annex": [{
            "path": "01_PACK/FHS-5_PLP_W0_Native-first_CODEX_修補證據型附錄.md",
            "sha256": lib.sha_file(next((lib.ROOT / "01_PACK").glob("*CODEX_*.md"))),
            "note": ("sealed historical appendix: its E10 pins belong to the prior "
                     "12_B0_NF_CODEX round; NOT used as this round's evidence; source unmodified"),
        }],
        "not_covered": [
            "W1 38+28 / C16 / EC-36 / local47 / FARP30 / local35 / U26 / QA26 denominators",
            "FHS 22/36/50/39/96/192/485 full regression (DEFER)",
            "HERMES / GPT CHAT / GPT WORK host execution",
            "different OS principal signature",
            "symlink creation (OS privilege; junction tested)",
            "publisher / release",
        ],
        "exclusions": ["09_DELIVERY", "07_CONSUMER", "10_EVIDENCE", "tmp", ".git", "__pycache__"],
        "workspace_only": [{
            "path": "02_CANDIDATE/repo/",
            "reason": "nested git worktree; published as 02_CANDIDATE/repo.bundle",
            "bundle": "02_CANDIDATE/repo.bundle" if (lib.ROOT / "02_CANDIDATE" / "repo.bundle").is_file() else None,
            "bundle_sha256": lib.sha_file(lib.ROOT / "02_CANDIDATE" / "repo.bundle")
            if (lib.ROOT / "02_CANDIDATE" / "repo.bundle").is_file() else None,
        }, {
            "path": "06_CHECKER/*/checker-wt|mutant|root|outside",
            "reason": "reproducible copies/junctions; raw logs and verdict are published",
        }],
        "files": files,
    }
    out = lib.ROOT / "10_EVIDENCE" / "EVIDENCE_MANIFEST.json"
    lib.write_json(out, manifest)
    sha = lib.sha_file(out)
    (out.parent / "EVIDENCE_MANIFEST.sha256").write_text(sha + "\n", encoding="utf-8")
    print(f"files={len(files)} receipts={len(recs)} manifest_sha256={sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
