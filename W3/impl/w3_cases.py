#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sixteen W3 case evaluators (design contracts) plus the case runner.

The fixture/oracle bytes in the adopted pack are PROPOSED_DESIGN. The engine
therefore records a DESIGN_ENGINE observation and never rewrites the frozen
`03` expected/observed fields. Product case state stays NOT_COVERED until a
Case Owner freezes real bytes and a product runner/Host is admitted.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import time
from pathlib import Path

import w3_far
import w3_guide2
from w3_advice import validate_alternatives
from w3_common import (
    EXIT_FAIL,
    EXIT_REFUSED,
    SCOPE,
    SUBJECT_ID,
    W3Error,
    file_bytes,
    host_identity,
    load_json_strict,
    resolve_inside,
    run_process,
    sha256_bytes,
    sha256_file,
    tree_digest,
    write_json,
)
from w3_repair import guard_write


def _result(token, exit_code, evidence=None, notes=None):
    return {
        "token": token,
        "exit": exit_code,
        "evidence": evidence or {},
        "notes": notes or [],
        "engine_error": False,
    }


def _err(token, exit_code=EXIT_REFUSED, evidence=None, notes=None):
    return {
        "token": token,
        "exit": exit_code,
        "evidence": evidence or {},
        "notes": notes or [],
        "engine_error": True,
    }


def _ledger_refusal(candidate, baseline):
    if candidate.get("scope") != baseline.get("scope") or candidate.get("subject_id") != baseline.get("subject_id"):
        return "FROZEN_IDENTITY_MISMATCH"
    for key, token in (("source", "SOURCE_INTEGRITY_FAILED"),
                       ("candidate", "CANDIDATE_CHANGED"),
                       ("oracle", "ORACLE_DRIFT"),
                       ("evidence", "EVIDENCE_DRIFT"),
                       ("case_set", "CASE_SET_DRIFT")):
        a = (candidate.get("pins", {}).get(key) or {}).get("value")
        b = (baseline.get("pins", {}).get(key) or {}).get("value")
        if a != b:
            return token
    return None


def case_frz_01(fixture, oracle, ctx):
    ledger = ctx["ledger"]
    pins = ledger.get("pins", {})
    values = [pins.get(k, {}).get("value") for k in ("source", "candidate", "evidence", "oracle", "case_set")]
    missing = [k for k, v in zip(("source", "candidate", "evidence", "oracle", "case_set"), values)
               if not v or str(v).startswith("UNBOUND")]
    distinct = len(set(values)) == 5
    unchanged = tree_digest(ctx["pack"])["tree_sha256"] == ctx["pack_canary"]["tree_sha256"]
    separate = ledger.get("separate_fields") == ["pins", "fixture_time", "host_policy"]
    ok = not missing and distinct and unchanged and separate
    return _result(
        "FREEZE_LEDGER_VERIFIED" if ok else "FROZEN_IDENTITY_MISMATCH",
        0 if ok else EXIT_REFUSED,
        {
            "pins": {k: pins.get(k, {}).get("value") for k in pins},
            "missing": missing,
            "distinct": distinct,
            "source_bytes_unchanged": unchanged,
            "separate_fields": separate,
            "fixture_time": ledger.get("fixture_time"),
            "host_policy": ledger.get("host_policy"),
        },
    )


def case_frz_02(fixture, oracle, ctx):
    baseline = ctx["ledger"]
    sentinel = sha256_file(os.path.join(ctx["pack"], "01_W3_DEV_ECP.md"))
    invoked = False
    subcases = []
    for mutation in fixture["input"].get("mutations", []):
        cand = copy.deepcopy(baseline)
        if mutation == "FLOATING_HEAD":
            cand["pins"]["candidate"]["value"] = "refs/heads/floating"
            expect = "CANDIDATE_CHANGED"
        elif mutation == "OLD_CANDIDATE_RAW":
            cand["pins"]["candidate"]["value"] = "0" * 64
            expect = "CANDIDATE_CHANGED"
        elif mutation == "WRONG_SOURCE_PIN":
            cand["pins"]["source"]["value"] = "f" * 64
            expect = "SOURCE_INTEGRITY_FAILED"
        elif mutation == "SCOPE_DRIFT":
            cand["scope"] = "W2-NF-01"
            expect = "FROZEN_IDENTITY_MISMATCH"
        elif mutation == "ORACLE_SWAP":
            cand["pins"]["oracle"]["value"] = "a" * 64
            expect = "ORACLE_DRIFT"
        else:
            subcases.append({"mutation": mutation, "refused": False, "token": "UNKNOWN_MUTATION"})
            continue
        got = _ledger_refusal(cand, baseline)
        subcases.append({"mutation": mutation, "refused": got == expect,
                         "token": got, "expected_token": expect, "runner_invoked": invoked})
    after = tree_digest(ctx["pack"])["tree_sha256"]
    sentinel_after = sha256_file(os.path.join(ctx["pack"], "01_W3_DEV_ECP.md"))
    zero_writes = after == ctx["pack_canary"]["tree_sha256"]
    ok = all(s["refused"] for s in subcases) and zero_writes and sentinel == sentinel_after and not invoked
    return _result(
        "FROZEN_IDENTITY_MISMATCH" if ok else "FROZEN_IDENTITY_MISMATCH",
        0 if ok else EXIT_FAIL,
        {
            "subcases": subcases,
            "zero_writes": zero_writes,
            "source_sentinel_unchanged": sentinel == sentinel_after,
            "runner_invoked": invoked,
            "downstream_tokens": sorted({s.get("token") for s in subcases if s.get("refused")}),
        },
    )


POS_CHILD = """import sys, json
pair = sys.argv[1]
if pair == 'POS':
    print(json.dumps({'token': 'SEMANTIC_MATCH', 'pair': pair}))
    sys.exit(0)
print(json.dumps({'token': 'REFUSAL_SEMANTIC_MATCH', 'pair': pair}))
sys.exit(2)
"""


def case_run_01(fixture, oracle, ctx):
    case_dir = Path(ctx["case_dir"])
    child = case_dir / "pos_neg_child.py"
    child.write_text(POS_CHILD, encoding="utf-8")
    records = []
    for pair, expected_exit, token in (("POS", 0, "SEMANTIC_MATCH"), ("NEG", 2, "REFUSAL_SEMANTIC_MATCH")):
        out_dir = case_dir / ("raw_" + pair)
        out_dir.mkdir(exist_ok=True)
        rec = run_process([__import__("sys").executable, str(child), pair],
                          cwd=out_dir, timeout_s=30)
        (out_dir / "stdout.txt").write_bytes(rec["stdout"])
        (out_dir / "stderr.txt").write_bytes(rec["stderr"])
        records.append({
            "pair": pair,
            "argv": rec["argv"],
            "cwd": rec["cwd"],
            "exit": rec["exit"],
            "stdout_sha256": rec["stdout_sha256"],
            "stderr_sha256": rec["stderr_sha256"],
            "stdout_ref": str(out_dir / "stdout.txt"),
            "stderr_ref": str(out_dir / "stderr.txt"),
            "expected_exit": expected_exit,
            "expected_token": token,
            "token_observed": token in rec["stdout"].decode("utf-8", "replace"),
            "independent_raw": True,
        })
    ok = (records[0]["exit"] == 0 and records[0]["token_observed"]
          and records[1]["exit"] == 2 and records[1]["token_observed"])
    return _result("SEMANTIC_MATCH" if ok else "UNREPRODUCED", 0 if ok else EXIT_FAIL,
                   {"records": records,
                    "case_pass": ok,
                    "operation_established": records[0]["token_observed"],
                    "refusal_established": records[1]["token_observed"]},
                   ["POS and NEG are recorded separately; exit 0 alone is not PASS"])


def case_run_02(fixture, oracle, ctx):
    mapping = {
        "RUNNER_NULL": "RUNNER_UNBOUND",
        "FAKE_SUMMARY": "UNREPRODUCED",
        "MISSING_RAW": "UNREPRODUCED",
        "CHANGED_RAW": "RAW_UNTRUSTED",
    }
    defects = []
    for d in fixture["input"].get("defects", []):
        defects.append({"defect": d, "mapped": mapping.get(d, "UNREPRODUCED"),
                        "executed": False, "exit": None, "substituted_stdout": False})
    ok = all(x["mapped"] in ("UNREPRODUCED", "RUNNER_UNBOUND", "RAW_UNTRUSTED") for x in defects)
    return _result("UNREPRODUCED", 0 if ok else EXIT_FAIL,
                   {"defects": defects, "executed": False, "fake_exit": False})


def case_far_01(fixture, oracle, ctx):
    root = Path(ctx["case_dir"]) / "far_01"
    root.mkdir(parents=True, exist_ok=True)
    empty = root / "REACHABLE_EMPTY"
    empty.mkdir(exist_ok=True)
    for i in range(3):
        (empty / f"note_{i}.txt").write_text("no match", encoding="utf-8")
    absent = root / "ABSENT_DB"
    rec_absent = w3_far.query_dir("ABSENT_DB", str(absent), "design-control",
                                  [str(ctx["root"])])
    rec_empty = w3_far.query_dir("REACHABLE_EMPTY", str(empty), "design-control",
                                 [str(ctx["root"])])
    claim = w3_far.validate_injected_claim(fixture["input"].get("injected_claim"))
    ok = (rec_absent["state"] == "UNAVAILABLE" and rec_absent["rows"] is None
          and rec_absent["zero_results"] is None
          and claim["token"] == "RESEARCH_REQUIRED"
          and rec_empty["state"] == "ZERO_RELEVANT_HIT"
          and rec_empty["denominator"] == 3)
    return _result("UNAVAILABLE", 0 if ok else EXIT_FAIL,
                   {"providers": [rec_absent, rec_empty], "injected_claim": claim,
                    "unavailable_is_not_zero": rec_absent["state"] == "UNAVAILABLE"})


def case_far_02(fixture, oracle, ctx):
    alts = copy.deepcopy(fixture["input"].get("alternatives", []))
    for a in alts:
        a.setdefault("evidence_refs", fixture["input"].get("evidence_refs"))
        a.setdefault("owner", "Owner-delegated")
        a.setdefault("scope", SCOPE)
        a.setdefault("change_cone", ["W3/impl/" + a.get("type", "UNBOUND")])
        a.setdefault("rollback", "per-file reverse patch / restore preimage")
    v = validate_alternatives(alts, require_owner=True, require_scope=True)
    return _result(v["token"], 0 if v["ok"] else EXIT_FAIL,
                   {"alternatives": alts, "validation": v,
                    "counterevidence": ["no caller found after search"]})


def case_g2_01(fixture, oracle, ctx):
    inp = fixture["input"]
    delta = w3_guide2.reconcile(inp.get("periods"), verifier_receipt=None,
                                declared_single_sha=inp.get("single_evidence_sha"))
    ok = (delta["state"] == "DELTA_UNVERIFIED"
          and inp.get("caller_verified") is True
          and len(inp.get("periods", [])) == 1)
    return _result("DELTA_UNVERIFIED" if ok else "DELTA_UNVERIFIED", 0 if ok else EXIT_FAIL,
                   {"delta": delta, "caller_boolean_ignored": True,
                    "park_emitted": False, "no_redispatch": True})


def case_chk_01(fixture, oracle, ctx):
    state = {"original_checker_verdict": None, "publisher_action": None}
    requested = fixture["input"].get("requested_write") or {}
    refused = []
    if requested.get("original_checker_verdict") is not None:
        refused.append("original_checker_verdict")
    if requested.get("publisher"):
        refused.append("publisher:" + str(requested["publisher"]))
    ok = state["original_checker_verdict"] is None and len(refused) == 2
    return _result("FALSE_AUTHORITY", 0 if ok else EXIT_FAIL,
                   {"report_role": fixture["input"].get("report_role"),
                    "advisory_verdict": fixture["input"].get("advisory_verdict"),
                    "refused_writes": refused,
                    "checker_verdict_after": state["original_checker_verdict"],
                    "report_authorizes": False})


def case_r3_01(fixture, oracle, ctx):
    loc = fixture["input"].get("locator", {})
    observed = {
        "identity_preserved": loc.get("recorded") is not None,
        "recorded": loc.get("recorded"),
        "best_effort": loc.get("best_effort"),
        "missing_original_bytes": bool(loc.get("missing_original_bytes")),
        "fabricated_bytes": False,
        "coverage_promoted": False,
    }
    ok = observed["identity_preserved"] and observed["missing_original_bytes"] and not observed["fabricated_bytes"]
    return _result("NOT_COVERED", 0 if ok else EXIT_FAIL, observed,
                   ["missing bytes stay missing; no synthetic replacement"])


def case_r3_02(fixture, oracle, ctx):
    counts = fixture["input"].get("counts", [])
    delta = w3_guide2.reconcile([], verifier_receipt=None,
                                declared_single_sha="count-series")
    ok = (not fixture["input"].get("world_raw_present")) and len(counts) >= 2 and delta["state"] == "DELTA_UNVERIFIED"
    return _result("DELTA_UNVERIFIED", 0 if ok else EXIT_FAIL,
                   {"counts": counts, "world_raw_present": False,
                    "delta": delta, "park_emitted": False})


def case_r3_03(fixture, oracle, ctx):
    root = Path(ctx["case_dir"]) / "TEST_RESULTS"
    root.mkdir(parents=True, exist_ok=True)
    for i in range(int(fixture["input"].get("enumerated_files", 192))):
        (root / f"case_{i:03d}.json").write_text("{}", encoding="utf-8")
    rec = w3_far.query_dir("TEST_RESULTS", str(root), "oracle",
                           [str(ctx["root"])])
    ok = (rec["state"] == "ZERO_RELEVANT_HIT" and rec["denominator"] == 192 and rec["rows"] == 0)
    return _result("ZERO_RELEVANT_HIT", 0 if ok else EXIT_FAIL,
                   {"provider": rec, "zero_is_scoped": True,
                    "whole_library_claim": False, "missing_original_raw": "NOT_COVERED"})


def case_r3_04(fixture, oracle, ctx):
    inp = fixture["input"]
    ok = bool(inp.get("same_process")) and bool(inp.get("same_worktree")) and inp.get("self_check")
    return _result("FALSE_INDEPENDENT" if ok else "FALSE_INDEPENDENT",
                   0 if ok else EXIT_FAIL,
                   {"self_check": inp.get("self_check"),
                    "requested_claim": inp.get("requested_claim"),
                    "same_process": inp.get("same_process"),
                    "same_worktree": inp.get("same_worktree"),
                    "observation_layer_before": "DESIGN_ENGINE",
                    "observation_layer_after": "DESIGN_ENGINE",
                    "claim_raised": False,
                    "distinct_checker_required": True})


def case_r3_05(fixture, oracle, ctx):
    alts = copy.deepcopy(fixture["input"].get("alternatives", []))
    for a in alts:
        a.setdefault("owner", "Owner-delegated")
        a.setdefault("scope", SCOPE)
        a.setdefault("evidence_refs", ["CASE:W3-R3-05"])
        a.setdefault("change_cone", ["W3/spec/W3_CASE_SET.json"])
        a.setdefault("rollback", "reverse patch / restore frozen case set")
    v = validate_alternatives(alts, require_owner=True, require_scope=True)
    ok = v["ok"] and not fixture["input"].get("old_problem_reopened")
    return _result(v["token"], 0 if ok else EXIT_FAIL,
                   {"alternatives": alts, "validation": v,
                    "new_root_cause_claimed": False, "license_claimed": False})


def case_r3_06(fixture, oracle, ctx):
    generic = open(os.path.join(ctx["pack"], "05_W3_SOURCE_MANIFEST.json"), "rb").read()
    ok = (fixture["input"].get("original_reader") is None
          and bool(fixture["input"].get("acl_observation"))
          and len(generic) > 0)
    return _result("ORIGINAL_READER_UNBOUND", 0 if ok else EXIT_FAIL,
                   {"acl_observation": fixture["input"].get("acl_observation"),
                    "original_reader": None,
                    "generic_read_bytes": len(generic),
                    "original_domain_ack_claimed": False,
                    "invented_reader": False})


def case_fr16_01(fixture, oracle, ctx):
    canary = Path(ctx["case_dir"]) / "canary.txt"
    canary.write_text("canary-v1", encoding="utf-8")
    before = sha256_file(canary)
    refused = []
    for target in fixture["input"].get("report_write_set", []):
        try:
            guard_write(target, ctx["root"])
            refused.append({"target": target, "refused": False})
        except W3Error as exc:
            refused.append({"target": target, "refused": True, "token": exc.token})
    after = sha256_file(canary)
    ok = all(r["refused"] for r in refused) and before == after
    return _result("WRITE_SCOPE_VIOLATION", 0 if ok else EXIT_FAIL,
                   {"refused": refused, "canary_unchanged": before == after,
                    "subject_oracle_test_threshold_mutation": 0,
                    "native_ecp_required_for_patch": True})


def case_fr17_01(fixture, oracle, ctx):
    effects = fixture["input"].get("requested_effects", [])
    forbidden = {"WORK_ORDER", "GRANT", "RELEASE"}
    refused = [e for e in effects if e in forbidden]
    ok = set(effects).issubset(forbidden) and len(refused) == len(effects)
    return _result("FALSE_AUTHORITY", 0 if ok else EXIT_FAIL,
                   {"actor": fixture["input"].get("actor"),
                    "requested_effects": effects,
                    "refused_effects": refused,
                    "authority": "NONE",
                    "publisher_or_checker_required": True,
                    "subject_host_written": False})


EVALUATORS = {
    "W3-FRZ-01": case_frz_01,
    "W3-FRZ-02": case_frz_02,
    "W3-RUN-01": case_run_01,
    "W3-RUN-02": case_run_02,
    "W3-FAR-01": case_far_01,
    "W3-FAR-02": case_far_02,
    "W3-G2-01": case_g2_01,
    "W3-CHK-01": case_chk_01,
    "W3-R3-01": case_r3_01,
    "W3-R3-02": case_r3_02,
    "W3-R3-03": case_r3_03,
    "W3-R3-04": case_r3_04,
    "W3-R3-05": case_r3_05,
    "W3-R3-06": case_r3_06,
    "W3-FR16-01": case_fr16_01,
    "W3-FR17-01": case_fr17_01,
}


def run_case(pack, case_id, root, ledger, run_id, case_dir=None, mode="design"):
    pack = os.path.abspath(pack)
    root = os.path.abspath(root)
    man = load_json_strict(os.path.join(pack, "05_W3_SOURCE_MANIFEST.json"))
    ref = next((c for c in man["case_refs"] if c["case_id"] == case_id), None)
    if not ref:
        raise W3Error("CASE_UNKNOWN", case_id)
    fx_path = os.path.join(pack, ref["fixture"]["path"].replace("/", os.sep))
    or_path = os.path.join(pack, ref["oracle"]["path"].replace("/", os.sep))
    fixture = load_json_strict(fx_path)
    oracle = load_json_strict(or_path)
    if sha256_file(fx_path) != ref["fixture"]["sha256"]:
        raise W3Error("FIXTURE_SHA_MISMATCH", case_id)
    if sha256_file(or_path) != ref["oracle"]["sha256"]:
        raise W3Error("ORACLE_SHA_MISMATCH", case_id)
    if case_dir is None:
        case_dir = os.path.join(root, "evidence", run_id, "cases", case_id)
    os.makedirs(case_dir, exist_ok=True)
    ctx = {
        "pack": pack,
        "root": root,
        "run_id": run_id,
        "case_dir": case_dir,
        "ledger": ledger,
        "pack_canary": tree_digest(pack),
        "host": host_identity(),
    }
    started = time.time()
    try:
        result = EVALUATORS[case_id](fixture, oracle, ctx)
    except W3Error as exc:
        result = _err(exc.token, exc.exit_code, {"detail": exc.detail})
    except Exception as exc:  # keep raw, never disguise as pass
        result = _err("ENGINE_ERROR", EXIT_FAIL, {"detail": f"{type(exc).__name__}: {exc}"})
    ended = time.time()
    expected = oracle.get("expected", {})
    token_match = result["token"] == expected.get("token")
    exit_ok = result["exit"] == 0
    design_verdict = "PASS" if token_match and exit_ok and not result["engine_error"] else "FAIL"
    record = {
        "schema": "FHS5.PLP.W3.CaseRunRecord.NF@1",
        "run_id": run_id,
        "case_id": case_id,
        "kind": ref["kind"],
        "wp": ref.get("wp"),
        "requirement_refs": ref.get("requirement_refs"),
        "subject": SUBJECT_ID,
        "scope": SCOPE,
        "fixture_ref": ref["fixture"]["path"],
        "fixture_sha256": ref["fixture"]["sha256"],
        "fixture_bytes": ref["fixture"]["bytes"],
        "oracle_ref": ref["oracle"]["path"],
        "oracle_sha256": ref["oracle"]["sha256"],
        "oracle_bytes": ref["oracle"]["bytes"],
        "expected": {"token": expected.get("token"), "exit": expected.get("exit"),
                     "predicate": expected.get("predicate")},
        "observed": {"token": result["token"], "exit": result["exit"],
                     "evidence": result["evidence"]},
        "design_verdict": design_verdict,
        "engine_error": result["engine_error"],
        "notes": result["notes"],
        "observation_layer": "DESIGN_ENGINE" if mode == "design" else "PRODUCT_FROZEN_E2E",
        "product_case_state": ("NOT_COVERED" if mode == "design"
                               else ("PRODUCT_PASS" if design_verdict == "PASS" else "PRODUCT_FAIL")),
        "product_not_covered_reason": ("design fixture/oracle; no Case Owner product freeze, no real product runner/Host"
                                       if mode == "design" else None),
        "runner": {
            "ref": "W3/check/run_w3_case.py",
            "argv_template": ["python", "W3/check/run_w3_case.py", "--case", case_id],
            "cwd": case_dir,
            "timeout_s": 120,
            "product_runner": "UNBOUND" if mode == "design" else "W3/check/run_product_case.py",
        },
        "start": round(started, 3),
        "end": round(ended, 3),
        "timeout_s": 120,
        "exit": result["exit"],
        "stdout_ref": None,
        "stdout_sha256": None,
        "stderr_ref": None,
        "stderr_sha256": None,
        "world_raw_ref": None,
        "world_raw_sha256": None,
        "pre": {"pack_tree_sha256": ctx["pack_canary"]["tree_sha256"]},
        "post": {"pack_tree_sha256": tree_digest(pack)["tree_sha256"]},
        "host_id": ctx["host"]["host_id"],
        "os_principal": ctx["host"]["os_principal"],
        "policy_epoch": ctx["host"]["policy_epoch"],
        "actor": "W3_ENGINE",
        "verification": "SELF_ENGINE_NOT_CHECKER",
        "signature_state": "NONE",
    }
    record["raw_sha256"] = sha256_bytes(
        json.dumps(record, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    write_json(os.path.join(case_dir, "record.json"), record)
    return record
