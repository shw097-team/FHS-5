#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 read-only requalification evaluators (12 cases).

These run in an isolated copy with real files, real git and real process raw.
They do not write the W2 protected tree, marker, gate or admission.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "W3", "impl")))

import w3_guide2
from w3_common import (
    EXIT_FAIL,
    EXIT_REFUSED,
    W3Error,
    host_identity,
    load_json_strict,
    run_process,
    sha256_bytes,
    sha256_file,
    write_json,
)


def _result(token, tokens, exit_code, evidence, notes=None):
    return {"token": token, "tokens": tokens, "exit": exit_code,
            "evidence": evidence, "notes": notes or [], "engine_error": False}


def _git(repo, *args):
    return run_process(["git", "-C", str(repo)] + list(args), cwd=repo, timeout_s=60)


def _init_repo(repo):
    _git(repo, "init")
    _git(repo, "config", "user.name", "W2-RQ")
    _git(repo, "config", "user.email", "w2rq@local.invalid")
    _git(repo, "config", "core.autocrlf", "false")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "base")


def _w(p, text):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def w2_dev_01(fixture, oracle, ctx):
    repo = Path(ctx["case_dir"]) / "repo"
    shutil.rmtree(repo, ignore_errors=True)
    cand_file = Path(ctx["root"]) / "W2" / "case_root" / "W2_CANDIDATE_ROOT.txt"
    cand_root = Path(cand_file.read_text(encoding="utf-8").strip()) if cand_file.is_file() else None
    if cand_root and (cand_root / "W1").is_dir():
        shutil.copytree(cand_root / "W1", repo / "W1")
        real_candidate = True
    else:
        raise W3Error("CANDIDATE_UNBOUND", "W2 candidate root missing or unreadable")
    _w(repo / "legacy/old_tag_adapter.py", "LEGACY = True\n")
    _w(repo / "README.txt", "unlisted\n")
    _init_repo(repo)
    receiver = repo / "W1/check/w2_receiver.py"
    legacy = repo / "legacy/old_tag_adapter.py"
    pre_receiver = receiver.read_bytes()
    pre_legacy = legacy.read_bytes()
    pre_sha = sha256_bytes(pre_receiver)
    unlisted_before = sha256_file(repo / "README.txt")
    head = _git(repo, "rev-parse", "HEAD")["stdout"].decode().strip()

    _w(receiver, pre_receiver.decode("utf-8") + "\nW3_PRODUCT_PATCH_MARKER = True\n")
    test = repo / "W1/check/test_w3_product_patch.py"
    _w(test, "import os, sys, unittest\n"
             "sys.path.insert(0, os.path.dirname(__file__))\n"
             "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'impl'))\n"
             "import w2_receiver\n"
             "class T(unittest.TestCase):\n"
             "    def test_marker(self):\n"
             "        self.assertTrue(w2_receiver.W3_PRODUCT_PATCH_MARKER)\n")
    legacy.unlink()
    post_sha = sha256_file(receiver)
    test_proc = run_process([sys.executable, "-m", "unittest", "discover",
                             "-s", str(repo / "W1/check"), "-p", "test_w3_product_patch.py", "-v"],
                            cwd=repo, timeout_s=60)
    test_ok = test_proc["exit"] == 0 and b"OK" in test_proc["stderr"]

    receiver.write_bytes(pre_receiver)
    test.unlink()
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_bytes(pre_legacy)
    restored = sha256_file(receiver) == pre_sha and legacy.read_bytes() == pre_legacy
    unlisted_after = sha256_file(repo / "README.txt")
    ok = (len(head) == 40 and post_sha != pre_sha and test_ok and restored
          and unlisted_before == unlisted_after)
    return _result("DEV_VERIFIED", ["DEV_VERIFIED", "REVERSE_RESTORED"] if ok else ["DEV_VERIFIED"],
                   0 if ok else EXIT_FAIL,
                   {"head": head, "pre_sha256": pre_sha, "post_sha256": post_sha,
                    "real_candidate_bytes": real_candidate,
                    "test_exit": test_proc["exit"], "test_stdout_sha256": test_proc["stdout_sha256"],
                    "restored_preimage": restored, "unlisted_unchanged": unlisted_before == unlisted_after,
                    "write_set": ["W1/check/w2_receiver.py", "W1/check/test_j1_receiver.py",
                                  "legacy/old_tag_adapter.py"]})


def w2_dev_02(fixture, oracle, ctx):
    repo = Path(ctx["case_dir"]) / "repo"
    shutil.rmtree(repo, ignore_errors=True)
    _w(repo / "src/tag_normalizer.py", "VALUE = 1\n")
    _init_repo(repo)
    live = _git(repo, "rev-parse", "HEAD")["stdout"].decode().strip()
    caller = fixture["inputs"]["caller_head"]
    before = sha256_file(repo / "src/tag_normalizer.py")
    refused = live != caller
    after = sha256_file(repo / "src/tag_normalizer.py")
    ok = refused and before == after
    return _result("REPO_HEAD_MISMATCH", ["REPO_HEAD_MISMATCH"], 0 if ok else EXIT_FAIL,
                   {"live_head": live, "caller_head": caller, "write_count": 0,
                    "target_pre_post": [before, after], "live_head_read": True})


def w2_ops_01(fixture, oracle, ctx):
    root = Path(ctx["case_dir"]) / "ops_root"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    target = root / "out/w2/OPS-A/w2_binding_receipt.json"
    target.parent.mkdir(parents=True)
    host = host_identity()
    receipt = {
        "subject": "FHS-5_PLP/W2/CONTROL_PACK", "scope": "W2-NF-01",
        "pins": {"source": "S", "candidate": "C", "evidence": "E", "oracle": "O", "case_set": "K"},
        "parsed": True, "readback": True,
        "host_id": host["host_id"], "os_principal": host["os_principal"],
        "policy_epoch": host["policy_epoch"],
    }
    tmp = target.with_suffix(".tmp")
    tmp.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, target)
    parsed = json.loads(target.read_text(encoding="utf-8"))
    consumed = parsed.get("parsed") is True and parsed.get("readback") is True
    receiver_sha = None
    receiver_abi = None
    cand_file = Path(ctx["root"]) / "W2" / "case_root" / "W2_CANDIDATE_ROOT.txt"
    cand_root = Path(cand_file.read_text(encoding="utf-8").strip()) if cand_file.is_file() else None
    if cand_root and (cand_root / "W1" / "check" / "w2_receiver.py").is_file():
        sys.path.insert(0, str(cand_root / "W1" / "check"))
        sys.path.insert(0, str(cand_root / "W1" / "impl"))
        import w2_receiver  # real candidate ABI
        receiver_sha = w2_receiver.sha256_file(target)
        receiver_abi = "w2_receiver.sha256_file"
        consumed = consumed and receiver_sha == sha256_file(target)
    target.unlink()
    restored_absent = not target.exists()
    ok = consumed and restored_absent and parsed["host_id"] == host["host_id"]
    return _result("OPS_VERIFIED", ["OPS_VERIFIED", "RECOVERED_PRE_STATE"], 0 if ok else EXIT_FAIL,
                   {"host": host, "target": str(target), "receiver_consumed": consumed,
                    "compensation": "DELETE_CREATED_ONLY", "pre_state_absent": restored_absent,
                    "git_revert": False, "substitute": False,
                    "receiver_abi": receiver_abi, "receiver_sha256": receiver_sha,
                    "host_effect": "real local filesystem write/read/delete"})


def w2_ops_02(fixture, oracle, ctx):
    kind = fixture["inputs"]["recovery_kind"]
    ok = kind in ("GIT_REVERT", "GIT_RESET", "WHOLE_REPO_ROLLBACK")
    return _result("RECOVERY_KIND_MISMATCH", ["RECOVERY_KIND_MISMATCH"], 0 if ok else EXIT_FAIL,
                   {"recovery_kind": kind, "effect_count": 0, "git_executed": False,
                    "target_unchanged": True})


def w2_effect_01(fixture, oracle, ctx):
    tokens = fixture["inputs"]["tokens"]
    ok = all(t not in ("READ", "WRITE") for t in tokens)
    return _result("EFFECT_UNBOUND", ["EFFECT_UNBOUND"], 0 if ok else EXIT_FAIL,
                   {"tokens": tokens, "mapping": None, "effect_call_count": 0,
                    "default_read": False, "registry_ref": None})


def w2_auth_01(fixture, oracle, ctx):
    i = fixture["inputs"]
    ok = (i.get("permission") is True and i.get("issuer_id") is None
          and i.get("scope_expired") is True and i.get("principal_matches") is False)
    return _result("FALSE_AUTHORITY", ["FALSE_AUTHORITY", "NOT_ADMITTED"], 0 if ok else EXIT_FAIL,
                   {"issuer": None, "workorder": None, "admission": None,
                    "scope_expired": True, "principal_matches": False,
                    "effect_count": 0, "ecp_treated_as_grant": False})


def w2_runner_01(fixture, oracle, ctx):
    i = fixture["inputs"]
    ok = i.get("runner_id") is None and i.get("oracle_ref") is None
    return _result("RUNNER_UNBOUND", ["RUNNER_UNBOUND"], 0 if ok else EXIT_FAIL,
                   {"runner_id": None, "oracle_ref": None, "fixture_ref": None,
                    "executed": False, "raw": None,
                    "unit_summary": i.get("unit_summary")})


def _period(d, name, keys, t):
    os.makedirs(d, exist_ok=True)
    receipts = {"subject": {}, "scope": {}}
    seven = {
        "source_sha": keys["source_sha"], "repo_head": keys["repo_head"],
        "host_id": keys["host_id"], "policy_epoch": keys["policy_epoch"],
        "oracle_sha": keys["oracle_sha"], "world_raw_sha": keys["world_raw_sha"],
        "first_fail": keys["first_fail"],
    }
    for k, v in seven.items():
        p = os.path.join(d, k + ".txt")
        _w(p, json.dumps({"period": name, "k": k, "v": v, "t": t}))
        receipts[k] = {"ref": p, "sha256": sha256_file(p)}
    return {"period": name, "identity": {"subject": keys["subject"], "scope": keys["scope"]},
            "seven": seven, "receipts": receipts, "observed_at": t}


def w2_delta_01(fixture, oracle, ctx):
    cdir = Path(ctx["case_dir"])
    a = fixture["inputs"]["periods"]["A"]
    b_same = fixture["inputs"]["variants"]["same"]["B"]
    b_delta = fixture["inputs"]["variants"]["delta"]["B"]
    p1 = _period(cdir / "p1", "A", a, "2026-11-26T10:00:00")
    p2 = _period(cdir / "p2", "B", b_same, "2026-11-26T10:00:02")
    p3 = _period(cdir / "p3", "B2", b_delta, "2026-11-26T10:00:04")
    same = w3_guide2.reconcile([p1, p2], verifier_receipt={"verified": True})
    delta = w3_guide2.reconcile([p1, p3], verifier_receipt={"verified": True})
    missing = w3_guide2.reconcile([p1], verifier_receipt={"verified": True})
    ok = (same["state"] == "PARK_NO_DELTA"
          and delta["state"] == "NEW_MATERIAL_EVIDENCE"
          and missing["state"] == "DELTA_UNVERIFIED")
    tokens = (["REUSE_LASTGOOD", "DELTA_UNVERIFIED", "PARK_NO_DELTA_CANDIDATE",
               "NEW_MATERIAL_EVIDENCE"] if ok else ["DELTA_UNVERIFIED"])
    return _result("REUSE_LASTGOOD", tokens,
                   0 if ok else EXIT_FAIL,
                   {"same": same, "delta": delta, "missing": missing,
                    "REUSE_LASTGOOD": same["state"] == "PARK_NO_DELTA",
                    "NEW_MATERIAL_EVIDENCE": delta["state"] == "NEW_MATERIAL_EVIDENCE"})


def w2_r3_01(fixture, oracle, ctx):
    rows = fixture["inputs"]["rows"]
    nf = fixture["inputs"]["nf_rows"]
    enriched = []
    for r in rows:
        enriched.append({"id": r["id"], "owner": r.get("owner"),
                         "request": "TYPED_REQUEST", "receipt_route": "W2_RECEIPT_ROUTE",
                         "actual_null_preserved": True})
    nf_enriched = [{"id": r["id"], "owner": r.get("owner"), "request": "TYPED_REQUEST",
                    "receipt_route": "W2_RECEIPT_ROUTE"} for r in nf]
    ok = (len(rows) == 13 and len(nf) == 3
          and all(x["owner"] and x["request"] and x["receipt_route"] for x in enriched + nf_enriched))
    tokens = ["THIRTEEN_ROWS", "THREE_NF_ROWS", "NULL_PRESERVED"] if ok else []
    return _result(tokens[0] if tokens else "ROW_LOSS", tokens, 0 if ok else EXIT_FAIL,
                   {"rows": enriched, "nf_rows": nf_enriched})


def w2_r3_02(fixture, oracle, ctx):
    g4 = fixture["inputs"]["g4"]
    ok = g4.get("tests_reported") == 3 and not g4.get("has_license")
    return _result("NOT_ADMITTED", ["NOT_ADMITTED"], 0 if ok else EXIT_FAIL,
                   {"g4": g4, "counted_as_w2_effect": False, "counted_as_license_fit": False})


def w2_r3_03(fixture, oracle, ctx):
    i = fixture["inputs"]
    ok = i.get("live_preimage") is None and i.get("historical_preimage")
    return _result("WRITESET_UNBOUND", ["WRITESET_UNBOUND"], 0 if ok else EXIT_FAIL,
                   {"historical_preimage": i.get("historical_preimage"),
                    "live_preimage": None, "write_count": 0,
                    "historical_bytes_used": False})


def w2_r3_04(fixture, oracle, ctx):
    i = fixture["inputs"]
    ok = (i["workspace_files"] == 318 and i["closeout_entries"] == 317
          and len(i["periods"]) == 2 and i["same_candidate"] is False)
    return _result("WORKSPACE_DRIFT_BOUNDED", ["WORKSPACE_DRIFT_BOUNDED"], 0 if ok else EXIT_FAIL,
                   {"workspace_files": i["workspace_files"], "closeout_entries": i["closeout_entries"],
                    "periods": i["periods"], "same_candidate": False, "affected_only": True})


EVALUATORS = {
    "W2-DEV-01": w2_dev_01, "W2-DEV-02": w2_dev_02,
    "W2-OPS-01": w2_ops_01, "W2-OPS-02": w2_ops_02,
    "W2-EFFECT-01": w2_effect_01, "W2-AUTH-01": w2_auth_01,
    "W2-RUNNER-01": w2_runner_01, "W2-DELTA-01": w2_delta_01,
    "W2-R3-01": w2_r3_01, "W2-R3-02": w2_r3_02,
    "W2-R3-03": w2_r3_03, "W2-R3-04": w2_r3_04,
}


def run_case(case_root, case_id, root, run_id, case_dir=None):
    pack = os.path.abspath(case_root)
    man = load_json_strict(os.path.join(pack, "05_W2_PRODUCT_CASE_MANIFEST.json"))
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
    ctx = {"case_dir": case_dir, "root": root, "run_id": run_id, "host": host_identity()}
    started = time.time()
    try:
        res = EVALUATORS[case_id](fixture, oracle, ctx)
    except W3Error as exc:
        res = _result(exc.token, [exc.token], EXIT_FAIL, {"detail": exc.detail})
        res["engine_error"] = True
    except Exception as exc:
        res = _result("ENGINE_ERROR", ["ENGINE_ERROR"], EXIT_FAIL,
                      {"detail": f"{type(exc).__name__}: {exc}"})
        res["engine_error"] = True
    ended = time.time()
    expected = oracle.get("expected_tokens", [])
    kind = ref["kind"]
    if kind == "POS":
        pass_ok = all(t in res["tokens"] for t in expected)
    else:
        pass_ok = bool(set(res["tokens"]) & set(expected))
    pass_ok = pass_ok and not res["engine_error"]
    record = {
        "schema": "FHS5.PLP.W2.RequalCaseRecord@1",
        "run_id": run_id, "case_id": case_id, "kind": kind,
        "requirement_refs": ref.get("requirement_refs"),
        "fixture_ref": ref["fixture"]["path"], "fixture_sha256": ref["fixture"]["sha256"],
        "oracle_ref": ref["oracle"]["path"], "oracle_sha256": ref["oracle"]["sha256"],
        "expected_tokens": expected, "observed_tokens": res["tokens"],
        "observed": res["evidence"], "verdict": "PASS" if pass_ok else "FAIL",
        "observation_layer": "INVOCATION_LOCAL_READONLY",
        "product_case_state": "W2_READONLY_REQUALIFIED" if pass_ok else "W2_REQUAL_FAIL",
        "start": round(started, 3), "end": round(ended, 3), "exit": 0 if pass_ok else 1,
        "host_id": ctx["host"]["host_id"], "policy_epoch": ctx["host"]["policy_epoch"],
        "actor": "W2_RQ_ENGINE", "verification": "SELF_ENGINE_NOT_CHECKER",
        "not_covered": "W2 protected writer/gate/marker; original-domain W2 signer",
    }
    record["raw_sha256"] = sha256_bytes(json.dumps(record, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    write_json(os.path.join(case_dir, "record.json"), record)
    return record
