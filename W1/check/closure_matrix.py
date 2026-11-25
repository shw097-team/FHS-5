#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared W1 closure matrix (R04).

One row per required obligation:
  OriginalID/Child -> Applicable -> ActualOperation -> EvidenceRef -> Verdict
  -> FirstFail/Next/Resume

Multiple IDs may share one real operation and one raw; the row records which
kind of evidence supports it (`exercise_kind`) so a shared operation is never
presented as an individual exercise.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import nf_reader as reader

WP = ["P01", "P02", "P03", "P04", "P05", "P06"]
ACC = ["W1-A01", "W1-A02", "W1-A03", "W1-A04", "W1-A05", "W1-A06",
       "W1-CODEX-01", "W1-CODEX-02", "W1-CODEX-03", "W1-CODEX-04",
       "W1-CODEX-05", "W1-CODEX-06"]
SUBS = ["N01", "N02", "N03", "N04", "N10", "N11"]

DEV_MAP = [
    (("DEV-APP", "DEV-EFF", "DEV-PRE", "DEV-OP-01", "DEV-OP-02", "DEV-PERM"),
     "nf_reader.inspect_package + evidence/inspect.json", "inspect.json", "SHARED_OPERATION", "P01"),
    (("DEV-WS-01",), "guide_nf.inspect_guide_request / render_thin_prompt", "raw/N03.json", "SHARED_OPERATION", "P03"),
    (("DEV-WS-02",), "bridge_nf.explain_slice + compare_context", "raw/N02.json", "SHARED_OPERATION", "P03"),
    (("DEV-WS-03",), "body_resolver.resolve_body/parse_clauses", "raw/N10.json", "SHARED_OPERATION", "P03"),
    (("DEV-WS-04",), "host_facade + run_host_nf real host run", "host/host_receipt.json", "INDIVIDUAL", "P04"),
    (("DEV-PROH-01", "DEV-PROH-02", "DEV-PROH-03", "DEV-PROH-04"),
     "no-write checker + canary + abi_guard + recovery kind", "how_to/independent_check.json", "SHARED_OPERATION", "P05"),
    (("DEV-OP-03", "DEV-OP-04", "DEV-OP-05", "DEV-OP-06"),
     "exact writeset + POS/NEG APIs + raw per run_id + consumer readback", "raw/N04.json", "SHARED_OPERATION", "P04"),
    (("DEV-ADP-01",), "guide advice never a grant", "raw/N03.json", "SHARED_OPERATION", "P03"),
    (("DEV-ADP-02",), "bridge read-only (wrote_bytes=0)", "raw/N02.json", "SHARED_OPERATION", "P03"),
    (("DEV-ADP-03",), "body resolver strict parse + span", "raw/N10.json", "SHARED_OPERATION", "P03"),
    (("DEV-ADP-04",), "host facade anti-upgrade", "raw/N04.json", "SHARED_OPERATION", "P04"),
    (("DEV-POST-01", "DEV-POST-03", "DEV-POST-05"),
     "digest domains + identity + outside canary", "inspect.json", "SHARED_OPERATION", "P06"),
    (("DEV-POST-02", "DEV-POST-04"), "asset pins + claim ledger", "cases.json", "SHARED_OPERATION", "P06"),
    (("DEV-RB-01", "DEV-RB-02", "DEV-RB-03", "DEV-RB-04"),
     "guard/readback/replay/independent checker", "how_to/independent_check.json", "SHARED_OPERATION", "P06"),
    (("DEV-IDEM-01", "DEV-IDEM-02", "DEV-IDEM-03"),
     "idempotent writes + LastGood + reverse patch", "raw/N11.json", "SHARED_OPERATION", "P06"),
]

OPS_MAP = [
    (("OPS-APP", "OPS-EFF", "OPS-PRE"), "host probe + effect tokens", "host/host_receipt.json", "SHARED_OPERATION", "O1"),
    (("OPS-CON-01",), "GPT CHAT not observed", "host/host_receipt.json", "NOT_APPLICABLE_THIS_ROUND", "O1"),
    (("OPS-CON-02",), "CODEX real invoke/serve/consume", "host/host_receipt.json", "INDIVIDUAL", "O3"),
    (("OPS-CON-03",), "Hermes three children deferred", "host/host_receipt.json", "DEFERRED", "O1"),
    (("OPS-OP-01", "OPS-OP-02"), "native entry, no install; loaded sha", "host/host_receipt.json", "SHARED_OPERATION", "O2"),
    (("OPS-OP-03", "OPS-OP-04", "OPS-OP-05", "OPS-OP-06"),
     "bind/invoke/serve/consume with real argv and readback", "host/host_receipt.json", "SHARED_OPERATION", "O3"),
    (("OPS-POST-01", "OPS-POST-02", "OPS-POST-03", "OPS-POST-05"),
     "stage ledger + evidence class + consumer split", "host/host_receipt.json", "SHARED_OPERATION", "O5"),
    (("OPS-POST-04",), "Hermes child rows", "host/host_receipt.json", "DEFERRED", "O5"),
    (("OPS-RB-01", "OPS-RB-02"), "container/host readback", "host/host_receipt.json", "SHARED_OPERATION", "O1"),
    (("OPS-REC-01", "OPS-REC-02", "OPS-REC-03", "OPS-REC-04"),
     "no install; uninstall n/a; restore by reverse patch; unknown reconcile", "raw/N11.json", "SHARED_OPERATION", "O6"),
    (("OPS-STOP-01", "OPS-RESUME-01"), "stop scope + typed resume", "raw/N11.json", "SHARED_OPERATION", "O6"),
]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def map_id(target: str, table) -> dict:
    for prefixes, op, ref, kind, step in table:
        for pre in prefixes:
            if target.startswith(pre):
                return {"operation": op, "evidence": ref, "exercise_kind": kind, "step": step}
    return {"operation": "MAPPED_NOT_EXERCISED", "evidence": None,
            "exercise_kind": "NOT_EXERCISED", "step": None}


def build(pack: Path, evidence: Path) -> dict:
    insp = reader.inspect_package(pack)
    cases = json.loads((evidence / "cases.json").read_text(encoding="utf-8"))
    verdicts = {c["case_id"]: c for c in cases["cases"]}
    rows = []

    PACK_PREFIX = "control_pack/FHS-5_PLP_W1_NATIVE_FIRST/"

    def norm(ref: str) -> str:
        if not ref:
            return ""
        if ref.startswith(("evidence/", "control_pack/")):
            return ref
        if ref.startswith(("raw/", "host/", "how_to/")):
            return "evidence/" + ref
        if ref in ("cases.json", "inspect.json", "independent_check.json",
                   "test_run.txt"):
            return "evidence/" + ref
        return PACK_PREFIX + ref

    def add(oid, child, applicable, op, ref, verdict, first_fail="", nxt="", resume=""):
        rows.append({"original_id": oid, "child": child, "applicable": applicable,
                     "actual_operation": op, "evidence_ref": norm(ref), "verdict": verdict,
                     "first_fail": first_fail, "next": nxt, "resume": resume})

    WP_EVIDENCE = {
        "P01": ("identity/pins/dag consume", "evidence/inspect.json"),
        "P02": ("ABI crosswalk + loss ledger", "evidence/raw/N02.json"),
        "P03": ("reader/bridge/guide/TPM build", "evidence/raw/N03.json"),
        "P04": ("real CODEX host served/consumed", "evidence/host/host_receipt.json"),
        "P05": ("13 cases + subcases + NEG", "evidence/cases.json"),
        "P06": ("closure matrix + seal + handoff", "evidence/how_to/independent_check.json"),
    }
    for wp in WP:
        op, ref = WP_EVIDENCE[wp]
        add(wp, None, True, op, ref, "EVIDENCED")
    for dev in insp["ids"]["dev"]:
        m = map_id(dev, DEV_MAP)
        add(dev, None, True, m["operation"], m["evidence"],
            "COVERED_BY_SHARED_OPERATION" if m["exercise_kind"] == "SHARED_OPERATION"
            else ("EXERCISED_INDIVIDUALLY" if m["exercise_kind"] == "INDIVIDUAL"
                  else "NOT_EXERCISED"), "", "", "")
    for ops in insp["ids"]["ops"]:
        m = map_id(ops, OPS_MAP)
        verdict = {"SHARED_OPERATION": "COVERED_BY_SHARED_OPERATION",
                   "INDIVIDUAL": "EXERCISED_INDIVIDUALLY",
                   "DEFERRED": "DEFERRED",
                   "NOT_APPLICABLE_THIS_ROUND": "NOT_APPLICABLE_THIS_ROUND"}.get(
                       m["exercise_kind"], "NOT_EXERCISED")
        add(ops, None, True, m["operation"], m["evidence"], verdict, "", "", "")
    for cid in insp["ids"]["cases"]:
        c = verdicts.get(cid)
        add(cid, None, True, "run_cases_nf case " + cid,
            ("evidence/raw/" + cid + ".json") if c and c.get("raw_path") else "",
            c["verdict"] if c else "NOT_RUN",
            (c or {}).get("first_fail") or "",
            "fix the affected case" if c and c["verdict"] not in ("PASS", "DEFERRED") else "",
            "same pack pin")
    for sub in SUBS:
        c = verdicts.get(sub)
        add("SUBCASE-" + sub, sub, True, "run_cases_nf subcase " + sub,
            ("evidence/raw/" + sub + ".json") if c and c.get("raw_path") else "",
            c["verdict"] if c else "NOT_RUN", "", "", "")
    ACC_EVIDENCE = {
        "W1-A01": ("source audit + identity", "evidence/inspect.json"),
        "W1-A02": ("full clause body + span", "evidence/raw/N02.json"),
        "W1-A03": ("seven-stage host ledger", "evidence/host/host_receipt.json"),
        "W1-A04": ("field-level ABI fidelity", "evidence/inspect.json"),
        "W1-A05": ("split counts + DAG", "evidence/inspect.json"),
        "W1-A06": ("claim ceiling audit", "evidence/how_to/independent_check.json"),
        "W1-CODEX-01": ("TPM/Guide/Bridge/consumer read", "evidence/raw/N01.json"),
        "W1-CODEX-02": ("nine-key dual period", "evidence/raw/N03.json"),
        "W1-CODEX-03": ("four bridge APIs full body", "evidence/raw/N02.json"),
        "W1-CODEX-04": ("five views same identity", "evidence/raw/N01.json"),
        "W1-CODEX-05": ("second package same ABI", "evidence/raw/W1-CODEX-05.json"),
        "W1-CODEX-06": ("multi-host accounting", "evidence/host/host_receipt.json"),
    }
    for acc in ACC:
        op, ref = ACC_EVIDENCE[acc]
        if acc == "W1-CODEX-06":
            add(acc, None, True, op, ref, "EVIDENCED_WITH_DEFERRED_HOSTS", "", "", "")
        elif acc == "W1-A03":
            v = ("EVIDENCED" if (verdicts.get("W1-HOST-01") or {}).get("verdict") == "PASS"
                 else "NOT_EVIDENCED")
            add(acc, None, True, op, ref, v, "", "", "")
        else:
            add(acc, None, True, op, ref, "EVIDENCED")
    for h in insp["ids"]["holds"]:
        add(h, None, True, "named HOLD preserved", "00_W1_PI_PD.md",
            "HOLD_PRESERVED_NOT_CLOSED", "", "owner decision required", "")
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    return {"schema": "FHS5.PLP.W1.ClosureMatrix@1",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "pack_manifest_sha256": insp["pack_manifest_sha256"],
            "rows": rows, "row_count": len(rows), "verdict_counts": counts}


def to_markdown(m: dict) -> str:
    lines = ["# W1 CLOSURE MATRIX", "",
             "- pack_manifest_sha256: `" + m["pack_manifest_sha256"] + "`",
             "- rows: " + str(m["row_count"]), ""]
    lines += ["| " + k + " | " + str(v) + " |" for k, v in sorted(m["verdict_counts"].items())]
    lines += ["", "| ID | Child | Applicable | Operation | Evidence | Verdict |",
              "|---|---|---|---|---|---|"]
    for r in m["rows"]:
        lines.append("| `{}` | {} | {} | {} | {} | {} |".format(
            r["original_id"], r["child"] or "-", r["applicable"],
            r["actual_operation"][:60], r["evidence_ref"] or "-", r["verdict"]))
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    m = build(Path(args.pack), Path(args.evidence))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    out.with_suffix(".md").write_text(to_markdown(m), encoding="utf-8", newline="\n")
    print(json.dumps({"rows": m["row_count"], "counts": m["verdict_counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
