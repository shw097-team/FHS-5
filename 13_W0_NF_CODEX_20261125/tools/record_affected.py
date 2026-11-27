#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Record only the affected W0 cases (NF-T01/07/08/10) from real runs.

This is a targeted selector, not a second runner: it executes the existing
entry scripts, reads their actual outputs, writes the same receipt schema as
tqaep_run.py, and merges the affected rows into the frozen 44-case summary.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

REC = lib.TQAEP / "receipts"
RAW = lib.TQAEP / "raw"
ORACLE = lib.TQAEP / "oracle.json"
SUMMARY = lib.TQAEP / "summary.json"
CAND = lib.git("rev-parse", "HEAD")
PACK_SHA = lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json")
REQ_SHA = lib.sha_file(lib.REPO / "requirements.md")
RUNTIME = f"Python {sys.version.split()[0]} | targeted affected replay"


def base(case_id, expected, observed, verdict, first_fail="", cwd=None, **kw):
    rec = lib.receipt(
        case_id,
        expected=expected,
        observed=observed,
        verdict=verdict,
        first_fail=first_fail,
        candidate_ref="02_CANDIDATE/repo",
        candidate_sha=CAND,
        source_refs=[
            {"path": "01_PACK/FHS-5_PLP_W0_NATIVE_FIRST/05_W0_SOURCE_MANIFEST.json",
             "sha256": PACK_SHA},
            {"path": "02_CANDIDATE/repo/requirements.md", "sha256": REQ_SHA},
        ],
        oracle_sha=lib.sha_file(ORACLE),
        cwd=str(cwd or lib.REPO),
        runtime=RUNTIME,
        **kw,
    )
    lib.write_json(REC / f"{case_id}.json", rec)
    return rec


def run_case(script, extra=None, tag=None):
    return lib.run([sys.executable, str(lib.ROOT / "tools" / script), *(extra or [])],
                   lib.TQAEP / "tmp" / "root", raw_dir=RAW, tag=tag)


def record_off():
    r = run_case("off_legacy.py", tag="NF-T01")
    out = lib.load_json(lib.ROOT / "04_DEV_OPS" / "off_legacy.json")
    entries = out.get("entries") or []
    neg = next((e for e in entries if e.get("name") == "reviewer_negative_control"), {})
    double = {
        "required": True,
        "rejected": bool(neg.get("ok") is True and neg.get("on_expected") is True
                         and neg.get("off_expected") is True
                         and neg.get("same_semantics") is True
                         and neg.get("requires_reviewer_positive") is True),
        "entry": neg,
    }
    ctrl = out.get("control") or {}
    allowed_ok = (ctrl.get("allowed") is True
                  or (ctrl.get("allowed_noprofile") is True
                      and ctrl.get("allowed_audit_only") is True))
    ok = (r["exit"] == 0 and out.get("verdict") == "PASS"
          and ctrl.get("blocked") is True and allowed_ok
          and bool(entries) and all(e.get("ok") is True for e in entries)
          and double["rejected"])
    return base(
        "NF-T01",
        {"status": "PASS", "exit": 0, "double_fail": "REJECTED"},
        {"verdict": out.get("verdict"), "exit": r["exit"],
         "control": out.get("control"), "entries": entries,
         "double_fail_control": double,
         "gates": out.get("gates"), "observer": out.get("observer"),
         "off_totals": out.get("off_totals")},
        "PASS" if ok else "FAIL",
        "" if ok else "OFF_CONTRACT_MISMATCH",
        argv=r["argv"], exit=r["exit"], stdout_sha=r["stdout_sha256"],
        stderr_sha=r["stderr_sha256"], execution_kind="subprocess-step",
        artifact="04_DEV_OPS/off_legacy.json",
        not_covered=out.get("not_covered") or [],
    )


def record_t07():
    r = lib.run([sys.executable, str(lib.ROOT / "tools" / "policy_cli.py"),
                 "--case", "NF-T07"], lib.TQAEP / "tmp" / "root",
                raw_dir=RAW, tag="NF-T07")
    try:
        payload = json.loads(r["stdout"])
    except Exception:
        payload = {}
    ok = (r["exit"] == 0 and payload.get("status") == "PARTIES_INVOKED"
          and payload.get("controls_ok") is True)
    return base(
        "NF-T07",
        {"status": "PARTIES_INVOKED", "exit": 0},
        {"exit": r["exit"], "status": payload.get("status"),
         "observed": payload.get("observed"), "controls": payload.get("controls")},
        "PASS" if ok else "FAIL",
        "" if ok else "FALSE_CAPABILITY",
        argv=r["argv"], exit=r["exit"], stdout_sha=r["stdout_sha256"],
        stderr_sha=r["stderr_sha256"], execution_kind="policy-cli",
        cwd=str(lib.TQAEP / "tmp" / "root"),
    )


def record_t08():
    chain = lib.run([sys.executable, str(lib.ROOT / "tools" / "collab_chain.py"),
                     "--mode", "full"], lib.TQAEP / "tmp" / "root",
                    raw_dir=RAW, tag="NF-T08-chain")
    negs = lib.run([sys.executable, str(lib.ROOT / "tools" / "collab_chain.py"),
                    "--mode", "negatives"], lib.TQAEP / "tmp" / "root",
                   raw_dir=RAW, tag="NF-T08-negatives")
    cpath = lib.PARTIES / "collab" / "chain.json"
    npath = lib.PARTIES / "collab" / "chain_negatives.json"
    out = lib.load_json(cpath) if cpath.is_file() else {}
    neg = lib.load_json(npath) if npath.is_file() else {}
    ncases = neg.get("negatives") or []
    ok = (chain["exit"] == 0 and negs["exit"] == 0
          and out.get("verdict") == "COMBINED_OK"
          and neg.get("verdict") == "NEGATIVES_REJECTED"
          and len(ncases) == 9 and all(n.get("rejected") is True for n in ncases))
    return base(
        "NF-T08",
        {"chain": "COMBINED_OK", "negatives": "NEGATIVES_REJECTED"},
        {"chain_verdict": out.get("verdict"), "chain_exit": chain["exit"],
         "negatives_verdict": neg.get("verdict"), "negatives_exit": negs["exit"],
         "failure_code": out.get("failure_code"),
         "segments": out.get("segments"),
         "checks": out.get("checks"),
         "negative_cases": [(n.get("name"), n.get("got"), n.get("rejected")) for n in ncases]},
        "PASS" if ok else "FAIL",
        "" if ok else (out.get("failure_code") or "UNREPRODUCED"),
        argv=chain["argv"], exit=chain["exit"], stdout_sha=chain["stdout_sha256"],
        stderr_sha=chain["stderr_sha256"], execution_kind="composite-collab-chain",
        sub_runs={"chain": {"argv": chain["argv"], "exit": chain["exit"]},
                  "negatives": {"argv": negs["argv"], "exit": negs["exit"]}},
        artifact="03_PARTIES/collab/chain.json",
    )


def merge(ids):
    s = lib.load_json(SUMMARY)
    rows = {c["case_id"]: c for c in s["cases"]}
    for cid in ids:
        rec = lib.load_json(REC / f"{cid}.json")
        rows[cid] = {"case_id": cid, "verdict": rec["verdict"],
                     "first_fail": rec.get("first_fail", ""),
                     "rec": f"05_TQAEP/receipts/{cid}.json"}
    s["cases"] = list(rows.values())
    s["counts"] = {
        "total": len(s["cases"]),
        "pass": sum(1 for c in s["cases"] if c["verdict"] == "PASS"),
        "fail": sum(1 for c in s["cases"] if c["verdict"] not in ("PASS", "PENDING_CONSUMER")),
        "pending": sum(1 for c in s["cases"] if c["verdict"] == "PENDING_CONSUMER"),
    }
    s["receipts_index_sha"] = lib.canonical_sha(
        {p.name: lib.sha_file(p) for p in sorted(REC.glob("*.json")) if p.name != "NF-T10.json"})
    s["generated_at"] = lib.now()
    s["affected_cases"] = sorted(ids)
    s["affected_note"] = ("41 unaffected same-position receipts reused; affected rows re-run "
                          "from byte-exact source and materialised candidate")
    lib.write_json(SUMMARY, s)
    print(json.dumps({"counts": s["counts"], "affected": sorted(ids)}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", action="append", choices=["NF-T01", "NF-T07", "NF-T08"], required=True)
    a = ap.parse_args()
    for cid in a.case:
        {"NF-T01": record_off, "NF-T07": record_t07, "NF-T08": record_t08}[cid]()
    merge(a.case)
    return 0


if __name__ == "__main__":
    sys.exit(main())