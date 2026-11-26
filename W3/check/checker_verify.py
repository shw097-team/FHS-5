#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Distinct read-only Checker over a frozen W3 run directory.

Its own file hash is recorded by the caller before execution. It loads no
verifier from a maker-writable path: it uses only stdlib reads and the frozen
records under the run's evidence directory.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

from w3_common import load_json_strict, sha256_file, tree_digest
from w3_intake import verify_pack


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--ext-root", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    ev = os.path.join(a.root, "evidence", a.run_id)
    errors = []
    verified = verify_pack(a.pack, os.path.join(a.ext_root, "EXTERNAL_SEAL.json"),
                           os.path.join(a.ext_root, "W3_OWNER_ADOPTION.json"),
                           os.path.join(a.ext_root, "W3_CURRENT.json"))
    if not verified["ok"]:
        errors.append("pack_verify_failed")
    pre = tree_digest(a.pack)["tree_sha256"]
    records = []
    for cid in sorted(os.listdir(os.path.join(ev, "cases"))):
        p = os.path.join(ev, "cases", cid, "record.json")
        if not os.path.isfile(p):
            errors.append("missing_record:" + cid)
            continue
        rec = load_json_strict(p)
        records.append(rec)
        if rec["case_id"] != cid:
            errors.append("case_id_mismatch:" + cid)
        if sha256_file(os.path.join(a.pack, rec["fixture_ref"].replace("/", os.sep))) != rec["fixture_sha256"]:
            errors.append("fixture_sha:" + cid)
        if sha256_file(os.path.join(a.pack, rec["oracle_ref"].replace("/", os.sep))) != rec["oracle_sha256"]:
            errors.append("oracle_sha:" + cid)
        if rec["observed"]["token"] != rec["expected"]["token"]:
            errors.append("token_mismatch:" + cid)
        if rec["design_verdict"] != "PASS":
            errors.append("design_verdict:" + cid)
        if rec["product_case_state"] != "NOT_COVERED":
            errors.append("overclaim_product:" + cid)
    if len(records) != 16:
        errors.append("record_count:%d" % len(records))

    fs = load_json_strict(os.path.join(ev, "FINDINGS", "FINDING_SET.json"))
    for f in fs["findings"]:
        for key in ("id", "severity", "class", "subject_sha", "command", "exit",
                    "raw_sha256", "reproduction"):
            if key not in f:
                errors.append("finding_field:%s" % key)
        if not os.path.isfile(f["raw_ref"]) or sha256_file(f["raw_ref"]) != f["raw_sha256"]:
            errors.append("finding_raw:" + f["id"])
    graph = load_json_strict(os.path.join(ev, "far", "FAR_GRAPH.json"))
    if len(set(graph["states_seen"])) != 5:
        errors.append("far_states")
    advice = load_json_strict(os.path.join(ev, "ADVICE", "DECISION_ADVICE.json"))
    if advice["advice_names_defined"] != 10:
        errors.append("advice_enum")
    if min(len(d["alternatives"]) for d in advice["decisions"]) < 2:
        errors.append("advice_alternatives")
    delta = load_json_strict(os.path.join(ev, "delta", "W3_DELTA.json"))
    if delta["p1_p2"]["state"] != "PARK_NO_DELTA":
        errors.append("delta_no_delta")
    if delta["p1_p3"]["state"] != "NEW_MATERIAL_EVIDENCE":
        errors.append("delta_new")
    repair = load_json_strict(os.path.join(ev, "repair", "REPAIR_RECEIPT.json"))
    if repair["verdict"] != "RED_TO_GREEN_WITH_RESTORE":
        errors.append("repair")

    post = tree_digest(a.pack)["tree_sha256"]
    if pre != post:
        errors.append("pack_changed_during_check")
    out = {
        "schema": "FHS5.PLP.W3.CheckerReceipt@1",
        "checker_role": "DISTINCT_READ_ONLY_CHECKER",
        "checker_script_sha256": sha256_file(os.path.abspath(__file__)),
        "argv": [sys.executable, os.path.abspath(__file__)] + (argv or []),
        "cwd": os.getcwd(),
        "run_id": a.run_id,
        "pack_manifest_sha256": verified["manifest_sha256"],
        "pack_package_tree_sha256": verified["package_tree_sha256"],
        "pack_directory_sha256": post,
        "pack_manifest_self_excluded": True,
        "candidate_tree_sha256": tree_digest(os.path.join(a.root, "W3"))["tree_sha256"],
        "cases_checked": len(records),
        "errors": errors,
        "verdict": "PASS" if not errors else "FAIL",
        "strength": "DISTINCT_LOCAL_PROCESS_READONLY; NOT_ORIGINAL_DOMAIN_PRINCIPAL",
        "independent_of_maker_process": True,
        "signature_state": "LOCAL_UNSIGNED_HASH_BOUND",
        "limitations": [
            "same OS principal as the maker",
            "design fixtures/oracles, not Case Owner product freeze",
            "does not replace an original-domain Checker",
        ],
    }
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"verdict": out["verdict"], "errors": errors,
                      "checker_sha256": out["checker_script_sha256"]}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
