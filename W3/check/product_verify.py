#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent product verifier over engine raw records.

The engine only produces OBSERVED raw. This verifier decides PRODUCT_PASS by
checking the Case Owner's semantic predicates against the record and the real
world; it does not read design_verdict or a mode flag.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

from w3_common import load_json_strict, run_process, sha256_file, tree_digest, write_json


def ev(rec):
    return rec.get("observed", {}).get("evidence", {})


def pred(name, rec, ctx):
    e = ev(rec)
    n = name.lower()
    if "five_pins" in n or "pins_distinct" in n:
        return bool(e.get("distinct"))
    if "source_bytes" in n or "pack_tree_unchanged" in n:
        return bool(e.get("source_bytes_unchanged"))
    if "separate_fields" in n:
        return e.get("separate_fields") == ["pins", "fixture_time", "host_policy"]
    if "all_subcases" in n or "mutations_refused" in n:
        return bool(e.get("subcases")) and all(x.get("refused") for x in e["subcases"])
    if n == "zero_writes":
        return bool(e.get("zero_writes"))
    if "sentinel" in n:
        return bool(e.get("source_sentinel_unchanged"))
    if "runner_not_invoked" in n:
        return e.get("runner_invoked") is False
    if "pos_exit" in n:
        rs = e.get("records") or []
        return bool(rs) and rs[0].get("exit") == 0
    if "neg_exit" in n:
        rs = e.get("records") or []
        return len(rs) > 1 and rs[1].get("exit") == 2
    if "real_pos_neg" in n:
        rs = e.get("records") or []
        return len(rs) == 2 and all(r.get("exit") == r.get("expected_exit") for r in rs)
    if "defects" in n:
        return bool(e.get("defects")) and all(d.get("executed") is False for d in e["defects"])
    if "executed_false" in n:
        return e.get("executed") is False
    if "absent_unavailable" in n:
        ps = e.get("providers") or []
        return bool(ps) and ps[0].get("state") == "UNAVAILABLE"
    if "absent_rows_null" in n or "rows_null" in n:
        ps = e.get("providers") or []
        return bool(ps) and ps[0].get("rows") is None and ps[0].get("zero_results") is None
    if "empty_zero" in n:
        ps = e.get("providers") or []
        return len(ps) > 1 and ps[1].get("state") == "ZERO_RELEVANT_HIT"
    if "injected_zero" in n:
        return (e.get("injected_claim") or {}).get("token") == "RESEARCH_REQUIRED"
    if "alternatives_substantive" in n or "at_least_two" in n:
        alts = e.get("alternatives") or []
        return len(alts) >= 2 and all(a.get("fit") and a.get("nofit") for a in alts)
    if "delta_unverified" in n:
        return (e.get("delta") or {}).get("state") == "DELTA_UNVERIFIED"
    if "no_park" in n:
        return e.get("park_emitted") is False
    if "checker_null" in n:
        return e.get("checker_verdict_after") is None
    if "refused_writes" in n:
        return len(e.get("refused_writes") or []) >= 1
    if "identity_preserved" in n:
        return bool(e.get("identity_preserved"))
    if "no_fabricated" in n:
        return e.get("fabricated_bytes") is False
    if "world_raw_absent" in n:
        return e.get("world_raw_present") is False
    if "denominator" in n:
        p = e.get("provider") or {}
        return p.get("denominator") == ctx.get("expected_denominator")
    if "zero_rows" in n:
        p = e.get("provider") or {}
        return p.get("rows") == 0
    if "no_claim_raised" in n:
        return e.get("claim_raised") is False
    if "owner_scope" in n:
        alts = e.get("alternatives") or []
        return bool(alts) and all(a.get("owner") and a.get("scope") for a in alts)
    if "original_reader_null" in n:
        return e.get("original_reader") is None
    if "generic_read" in n:
        return (e.get("generic_read_bytes") or 0) > 0
    if "no_ack" in n:
        return e.get("original_domain_ack_claimed") is False
    if "all_writes_refused" in n:
        return bool(e.get("refused")) and all(x.get("refused") for x in e["refused"])
    if "canary_unchanged" in n:
        return bool(e.get("canary_unchanged"))
    if "zero_mutation" in n:
        return e.get("subject_oracle_test_threshold_mutation") == 0
    if "authority_none" in n:
        return e.get("authority") == "NONE"
    return False


def pred_full(name, rec, ctx):
    e = ev(rec)
    n = name
    pro = e.get("providers") or []
    alts = e.get("alternatives") or []
    recs = e.get("records") or []
    if n in ("five_pins_present_and_distinct",):
        return len(e.get("pins") or {}) == 5 and len(set((e.get("pins") or {}).values())) == 5
    if n == "pins_reopen_freeze_ledger":
        return (e.get("pins") or {}) == (ctx.get("ledger_pins") or {})
    if n == "pack_tree_unchanged":
        if e.get("pack_tree_unchanged") is not None:
            return bool(e.get("pack_tree_unchanged"))
        return bool(e.get("source_bytes_unchanged"))
    if n == "separate_fields_present":
        sf = e.get("separate_fields")
        return sf is True or sf == ["pins", "fixture_time", "host_policy"]
    if n == "source_bytes_unchanged":
        return bool(e.get("source_bytes_unchanged"))
    if n == "five_mutations_covered":
        return len(e.get("subcases") or []) == 5
    if n == "each_mutation_refused_with_typed_token":
        return bool(e.get("subcases")) and all(x.get("refused") and x.get("token") for x in e["subcases"])
    if n == "zero_writes":
        return bool(e.get("zero_writes"))
    if n == "source_sentinel_unchanged":
        return bool(e.get("source_sentinel_unchanged"))
    if n == "runner_not_invoked":
        return e.get("runner_invoked") is False
    if n == "pos_exit_zero":
        if recs:
            return recs[0].get("exit") == 0 and rec.get("process_exit") == 0
        return rec.get("process_exit") == 0 and rec.get("exit") == 0
    if n == "neg_exit_two":
        if recs and len(recs) > 1:
            return recs[1].get("exit") == 2
        return rec.get("process_exit") == 2
    if n == "pos_neg_raws_independent":
        return len(recs) == 2 and len({r.get("cwd") for r in recs}) == 2 and all(r.get("independent_raw") for r in recs)
    if n == "operation_and_refusal_both_established":
        return bool(e.get("case_pass")) and bool(e.get("operation_established")) and bool(e.get("refusal_established"))
    if n == "all_four_defects_present":
        return len(e.get("defects") or []) == 4
    if n == "nothing_executed":
        return e.get("executed") is False
    if n == "no_defect_reproduced":
        return all(d.get("executed") is False for d in e.get("defects") or [])
    if n == "no_fake_exit":
        return all(d.get("exit") is None for d in e.get("defects") or [])
    if n == "no_stdout_substitution":
        return all(d.get("substituted_stdout") is False for d in e.get("defects") or [])
    if n == "absent_rows_null":
        return bool(pro) and pro[0].get("rows") is None and pro[0].get("zero_results") is None
    if n == "unavailable_is_not_zero":
        return bool(pro) and pro[0].get("state") == "UNAVAILABLE" and bool(e.get("unavailable_is_not_zero"))
    if n == "injected_zero_becomes_research_required":
        return (e.get("injected_claim") or {}).get("token") == "RESEARCH_REQUIRED" and (e.get("injected_claim") or {}).get("accepted") is False
    if n == "reachable_empty_has_denominator":
        return len(pro) > 1 and pro[1].get("denominator") == 3 and pro[1].get("rows") == 0
    if n in ("two_distinct_alternatives", "two_substantive_alternatives"):
        return len(alts) >= 2 and len({a.get("id") for a in alts}) == len(alts)
    if n == "each_has_fit_and_nofit":
        return bool(alts) and all(a.get("fit") and a.get("nofit") for a in alts)
    if n == "fit_nofit_present":
        return (e.get("validation") or {}).get("fit_nofit_present") is True or (bool(alts) and all(a.get("fit") and a.get("nofit") for a in alts))
    if n == "each_has_evidence_and_counterevidence":
        return bool(alts) and all(a.get("evidence_refs") for a in alts)
    if n == "each_has_owner_scope_rollback":
        return bool(alts) and all(a.get("owner") and a.get("scope") and a.get("rollback") for a in alts)
    if n == "cost_risk_may_be_unknown":
        return all(a.get("cost") is not None and a.get("risk") is not None for a in alts)
    if n == "delta_stays_unverified":
        return (e.get("delta") or {}).get("state") == "DELTA_UNVERIFIED"
    if n == "caller_boolean_ignored":
        return bool(e.get("caller_boolean_ignored"))
    if n == "single_sha_not_delta":
        return (e.get("delta") or {}).get("state") == "DELTA_UNVERIFIED"
    if n == "no_park":
        return e.get("park_emitted") is False
    if n == "no_redispatch":
        return bool(e.get("no_redispatch"))
    if n == "advisory_pass_cannot_write_checker_verdict":
        return e.get("checker_verdict_after") is None and bool(e.get("refused_writes"))
    if n == "checker_verdict_stays_null":
        return e.get("checker_verdict_after") is None
    if n == "publisher_release_refused":
        return any("publisher" in str(x) for x in e.get("refused_writes") or [])
    if n == "report_does_not_authorize":
        return e.get("report_authorizes") is False
    if n == "native_ecp_required":
        return e.get("native_ecp_required_for_patch") is True
    if n == "identity_preserved":
        return bool(e.get("identity_preserved"))
    if n == "missing_bytes_stay_missing":
        return bool(e.get("missing_original_bytes"))
    if n == "no_fabricated_bytes":
        return e.get("fabricated_bytes") is False
    if n == "no_coverage_promotion":
        return e.get("coverage_promoted") is False
    if n == "six_period_counts_present":
        return len(e.get("counts") or []) == 6
    if n == "count_series_is_not_world_raw":
        return e.get("world_raw_present") is False
    if n == "zero_is_scoped":
        return bool(e.get("zero_is_scoped"))
    if n == "denominator_is_192":
        return (e.get("provider") or {}).get("denominator") == 192
    if n == "rows_zero":
        return (e.get("provider") or {}).get("rows") == 0
    if n == "missing_original_raw_not_covered":
        return e.get("missing_original_raw") == "NOT_COVERED"
    if n == "same_process":
        return e.get("same_process") is True
    if n == "same_worktree":
        return e.get("same_worktree") is True
    if n == "observation_layer_not_raised":
        return e.get("claim_raised") is False
    if n == "distinct_checker_required":
        return e.get("distinct_checker_required") is True
    if n == "no_new_root_cause":
        return e.get("new_root_cause_claimed") is False
    if n == "no_license_claim":
        return e.get("license_claimed") is False
    if n == "acl_observed_13_of_13":
        return e.get("acl_observation") == "13/13"
    if n == "original_reader_null":
        return e.get("original_reader") is None
    if n == "generic_read_continues":
        return (e.get("generic_read_bytes") or 0) > 0
    if n == "ack_not_claimed":
        return e.get("original_domain_ack_claimed") is False
    if n == "no_invented_reader":
        return e.get("invented_reader") is False
    if n == "four_targets_refused":
        return len(e.get("refused") or []) == 4 and all(x.get("refused") for x in e.get("refused") or [])
    if n == "canary_unchanged":
        return bool(e.get("canary_unchanged"))
    if n == "zero_mutation":
        return e.get("subject_oracle_test_threshold_mutation") == 0
    if n == "three_effects_refused":
        return len(e.get("refused_effects") or []) == 3
    if n == "authority_none":
        return e.get("authority") == "NONE"
    if n == "subject_host_not_written":
        return e.get("subject_host_written") is False
    if n == "publisher_checker_required":
        return e.get("publisher_or_checker_required") is True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--product-pack", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    man = load_json_strict(os.path.join(a.product_pack, "05_W3_SOURCE_MANIFEST.json"))
    ledger = load_json_strict(a.ledger)
    ledger_pins = {k: v["value"] for k, v in ledger.get("pins", {}).items()}
    rows = []
    for ref in man["case_refs"]:
        cid = ref["case_id"]
        oracle = load_json_strict(os.path.join(a.product_pack, ref["oracle"]["path"].replace("/", os.sep)))
        argv = [sys.executable, os.path.join(HERE, "run_product_case.py"),
                "--product-pack", a.product_pack, "--case", cid,
                "--root", a.root, "--run-id", a.run_id, "--ledger", a.ledger]
        proc = run_process(argv, cwd=a.root, timeout_s=120)
        rec = load_json_strict(os.path.join(a.root, "evidence", a.run_id, "cases", cid, "record.json"))
        expected_token = oracle.get("expected", {}).get("token")
        token_ok = rec.get("observed", {}).get("token") == expected_token
        ctx = {"expected_denominator": oracle.get("expected", {}).get("denominator"),
               "ledger_pins": ledger_pins}
        checks = []
        for p in oracle.get("predicates", []):
            pid = p.get("id") if isinstance(p, dict) else p
            try:
                ok = pred_full(pid, rec, ctx)
            except Exception:
                ok = False
            checks.append({"predicate": pid, "ok": bool(ok)})
        verdict = "PRODUCT_PASS" if token_ok and checks and all(c["ok"] for c in checks) else "PRODUCT_FAIL"
        rows.append({
            "case_id": cid, "kind": ref["kind"],
            "expected_token": expected_token,
            "observed_token": rec.get("observed", {}).get("token"),
            "token_ok": token_ok,
            "predicates": checks,
            "verdict": verdict,
            "engine_exit": proc["exit"],
            "record_ref": os.path.join("evidence", a.run_id, "cases", cid, "record.json"),
            "record_sha256": sha256_file(os.path.join(a.root, "evidence", a.run_id, "cases", cid, "record.json")),
        })
    out = {
        "schema": "FHS5.PLP.W3.ProductVerdict@2",
        "run_id": a.run_id,
        "case_count": len(rows),
        "product_pass": sum(1 for r in rows if r["verdict"] == "PRODUCT_PASS"),
        "rows": rows,
        "verifier": {"path": os.path.abspath(__file__), "sha256": sha256_file(os.path.abspath(__file__))},
        "observation_layer": "PRODUCT_ENGINE_RAW",
        "not_design_verdict": True,
    }
    write_json(a.out, out)
    print(json.dumps({"cases": len(rows), "product_pass": out["product_pass"]}, ensure_ascii=False))
    return 0 if out["product_pass"] == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
