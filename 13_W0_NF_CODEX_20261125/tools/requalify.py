#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Requalify only NF-T01 and NF-T08 after the M2/M3 tool changes; do not
re-run the other 42 cases."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

REC = lib.TQAEP / "receipts"
RAW = lib.ROOT / "05_TQAEP" / "raw"
CAND = lib.git("rev-parse", "HEAD")


def add(case_id, expected, observed, argv, r, kind, artifact, not_covered=None):
    rec = lib.receipt(
        case_id,
        expected=expected,
        observed=observed,
        verdict="PASS" if observed.get("ok") else "FAIL",
        first_fail="" if observed.get("ok") else expected.get("failure", "UNREPRODUCED"),
        candidate_ref="02_CANDIDATE/repo",
        candidate_sha=CAND,
        source_refs=[
            {"path": "01_PACK/FHS-5_PLP_W0_NATIVE_FIRST/05_W0_SOURCE_MANIFEST.json",
             "sha256": lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json")},
            {"path": "02_CANDIDATE/repo/requirements.md",
             "sha256": lib.sha_file(lib.REPO / "requirements.md")},
        ],
        oracle_sha=lib.sha_file(lib.TQAEP / "oracle.json"),
        cwd=str(lib.ROOT),
        argv=argv,
        runtime=f"Python {sys.version.split()[0]}",
        exit=r["exit"],
        stdout_sha=r["stdout_sha256"],
        stderr_sha=r["stderr_sha256"],
        execution_kind=kind,
        artifact=artifact,
        not_covered=not_covered or [],
    )
    lib.write_json(REC / f"{case_id}.json", rec)
    return rec


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    off = lib.run([sys.executable, str(lib.ROOT / "tools" / "off_legacy.py")], lib.ROOT,
                  raw_dir=RAW, tag="requal_NF-T01")
    offj = lib.load_json(lib.ROOT / "04_DEV_OPS" / "off_legacy.json")
    r01 = add("NF-T01", {"verdict": "PASS", "failure": "OFF_FAIL"},
              {"ok": off["exit"] == 0 and offj.get("verdict") == "PASS",
               "verdict": offj.get("verdict"),
               "entries": [(e["name"], e["ok"], e.get("on_expected"), e.get("off_expected"),
                            e.get("same_semantics"), e.get("false_parity_rejected"))
                           for e in offj.get("entries", [])],
               "control": offj.get("control")},
              off["argv"], off, "subprocess-step", "04_DEV_OPS/off_legacy.json")
    chain = lib.run([sys.executable, str(lib.ROOT / "tools" / "collab_chain.py"), "--mode", "full"],
                    lib.ROOT, raw_dir=RAW, tag="requal_NF-T08-chain")
    negs = lib.run([sys.executable, str(lib.ROOT / "tools" / "collab_chain.py"), "--mode", "negatives"],
                   lib.ROOT, raw_dir=RAW, tag="requal_NF-T08-neg")
    cj = lib.load_json(lib.PARTIES / "collab" / "chain.json")
    nj = lib.load_json(lib.PARTIES / "collab" / "chain_negatives.json")
    r08 = add("NF-T08", {"chain": "COMBINED_OK", "negatives": "NEGATIVES_REJECTED",
                         "failure": "UNREPRODUCED"},
              {"ok": chain["exit"] == 0 and negs["exit"] == 0
                     and cj.get("verdict") == "COMBINED_OK"
                     and nj.get("verdict") == "NEGATIVES_REJECTED",
               "chain_verdict": cj.get("verdict"), "checks": len(cj.get("checks") or []),
               "segments": cj.get("segments"),
               "negatives": [(n.get("name"), n.get("rejected")) for n in nj.get("negatives", [])]},
              chain["argv"], chain, "composite-collab-chain", "03_PARTIES/collab/chain.json")
    summary = lib.load_json(lib.TQAEP / "summary.json")
    for c in summary["cases"]:
        for rec in (r01, r08):
            if c["case_id"] == rec["case_id"]:
                c["verdict"] = rec["verdict"]
                c["first_fail"] = rec["first_fail"]
    summary["counts"]["pass"] = sum(1 for c in summary["cases"] if c["verdict"] == "PASS")
    summary["counts"]["fail"] = sum(1 for c in summary["cases"]
                                    if c["verdict"] not in ("PASS", "PENDING_CONSUMER"))
    summary["counts"]["pending"] = sum(1 for c in summary["cases"]
                                       if c["verdict"] == "PENDING_CONSUMER")
    summary["receipts_index_sha"] = lib.canonical_sha(
        {p.name: lib.sha_file(p) for p in sorted(REC.glob("*.json")) if p.name != "NF-T10.json"})
    lib.write_json(lib.TQAEP / "summary.json", summary)
    print(f"NF-T01={r01['verdict']} NF-T08={r08['verdict']} counts={summary['counts']}")
    return 0 if r01["verdict"] == "PASS" and r08["verdict"] == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
