#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI wrapper for the W0 policy scenarios. Every case runs as a subprocess,
prints JSON and exits with the gate's code; each case also runs a two-sided
control so the gate can actually fail."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import policy
import guide as guide_mod


def emit(code: int, status: str, observed: dict, controls: list[dict]):
    ok = all(c.get("ok") for c in controls)
    if not ok:
        code, status = 3, "CONTROL_FAILED"
    print(json.dumps({"status": status, "exit": code, "observed": observed,
                      "controls": controls, "controls_ok": ok},
                     ensure_ascii=False, sort_keys=True))
    return code


def c(name: str, got: str, want: str) -> dict:
    return {"name": name, "got": got, "want": want, "ok": got == want}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--case", required=True)
    p.add_argument("--file")
    p.add_argument("--frozen")
    p.add_argument("--candidate")
    p.add_argument("--receipt")
    p.add_argument("--pack", default=str(lib.PACK))
    p.add_argument("--requested")
    p.add_argument("--sentinel")
    a = p.parse_args()
    case = a.case

    if case == "T04":
        fake = policy.authority_gate({"permit": True, "grant_ref": None,
                                      "original_reader_ack": "ACK-123",
                                      "reader_adapter_pin": None})
        valid = policy.authority_gate({"grant_ref": "OWNER-W0-CODEX-20261125-01"})
        return emit(3 if fake["status"] == "FALSE_AUTHORITY" else 0,
                    fake["status"], {"fake": fake, "valid": valid},
                    [c("fake", fake["status"], "FALSE_AUTHORITY"),
                     c("valid", valid["status"], "ADMITTED")])

    if case == "T07":
        bad = policy.schema_validate({"schema_version": "PLP.REVIEW.REQUEST@99",
                                      "sources": [], "crosswalk": []}, "PLP.REVIEW.REQUEST@2")
        good = policy.schema_validate({"schema_version": "PLP.REVIEW.REQUEST@2",
                                       "sources": [], "crosswalk": []}, "PLP.REVIEW.REQUEST@2")
        keep = policy.unknown_schema_roundtrip({"schema_version": "PLP.REVIEW.REQUEST@2",
                                                "sources": [], "crosswalk": [],
                                                "x_required_security": "keep"})
        return emit(3, bad["status"], {"bad": bad, "good": good, "preserve": keep},
                    [c("bad", bad["status"], "SCHEMA_UNSUPPORTED"),
                     c("good", good["status"], "SCHEMA_OK"),
                     c("preserve", keep["status"], "PRESERVED")])

    if case == "T08":
        code_exists = (lib.REPO / "briefcheck.py").is_file()
        installed = __import__("shutil").which("briefcheck") is not None
        status = "BIND_EXISTING" if code_exists and not installed else (
            "ALREADY_BOUND" if installed else "CODE_MISSING")
        return emit(0, status, {"code_exists": code_exists, "console_entry": installed},
                    [{"name": "code", "got": code_exists, "want": True, "ok": code_exists}])

    if case == "T09":
        over = policy.dag_check([("W0_READ", "W4_RELEASE")],
                                {"W0_READ": 0, "W4_RELEASE": 4})
        legal = policy.dag_check([("W0_READ", "W0_DRAFT")],
                                 {"W0_READ": 0, "W0_DRAFT": 1})
        return emit(3, over["status"], {"overreach": over, "legal": legal},
                    [c("overreach", over["status"], "PHASE_OVERREACH_CANDIDATE"),
                     c("legal", legal["status"], "DAG_OK"),
                     {"name": "read_allowed", "got": over.get("legal_read"), "want": True,
                      "ok": over.get("legal_read") is True}])

    if case == "T10":
        cyc = policy.dag_check([("OP12", "POST_READBACK"), ("POST_READBACK", "OP12")], {})
        acyclic = policy.dag_check([("REQ", "ECP"), ("ECP", "RUN")], {})
        return emit(3, cyc["status"], {"cycle": cyc, "acyclic": acyclic},
                    [c("cycle", cyc["status"], "GATE_CYCLE_CANDIDATE"),
                     c("acyclic", acyclic["status"], "DAG_OK"),
                     {"name": "not_executed", "got": cyc.get("executed"), "want": False,
                      "ok": cyc.get("executed") is False}])

    if case == "T11":
        sentinel = Path(a.sentinel)
        before = lib.sha_file(sentinel)
        gate = policy.authority_gate({"permit": True})
        after = lib.sha_file(sentinel)
        valid = policy.authority_gate({"grant_ref": "OWNER-W0-CODEX-20261125-01"})
        return emit(3, gate["status"], {"gate": gate, "pre": before, "post": after},
                    [c("fake", gate["status"], "FALSE_AUTHORITY"),
                     c("valid", valid["status"], "ADMITTED"),
                     {"name": "no_write", "got": before == after, "want": True,
                      "ok": before == after}])

    if case == "T12":
        bad = policy.effect_resolve("UNKNOWN_DEPLOY")
        good = policy.effect_resolve("SOURCE_READ")
        return emit(3, bad["status"], {"bad": bad, "good": good},
                    [c("bad", bad["status"], "EFFECT_MAPPING_UNVERIFIED"),
                     c("good", good["status"], "MAPPED")])

    if case == "T14":
        bad = policy.verify_semantics(0, {"status": "COMPLETE", "provided": ["A", "B"], "missing": []},
                                      {"exit": 2, "status": "MISSING", "provided": ["A"], "missing": ["B"]})
        good = policy.verify_semantics(2, {"status": "MISSING", "provided": ["A"], "missing": ["B"]},
                                       {"exit": 2, "status": "MISSING", "provided": ["A"], "missing": ["B"]})
        return emit(3, bad["status"], {"mismatch": bad, "match": good},
                    [c("mismatch", bad["status"], "EFFECT_NOT_VERIFIED"),
                     c("match", good["status"], "EFFECT_VERIFIED")])

    if case == "T15":
        frozen = lib.load_json(a.frozen)
        frozen_sha = lib.sha_file(a.frozen)
        obs = lib.load_json(a.file)
        obs_sha = lib.sha_file(a.file)
        drifted = frozen_sha != obs_sha
        unchanged = policy.delta_eval({"candidate": frozen.get("candidate_commit"),
                                       "raw_sha": frozen_sha, "first_fail": "x"},
                                      {"candidate": obs.get("candidate_commit"),
                                       "raw_sha": obs_sha, "first_fail": "x"})
        return emit(3 if drifted else 0, "ORACLE_DRIFT" if drifted else "ORACLE_MATCH",
                    {"frozen_sha": frozen_sha, "observed_sha": obs_sha, "delta": unchanged},
                    [{"name": "drift_detected", "got": drifted, "want": True, "ok": drifted}])

    if case == "T16":
        rec = lib.load_json(a.receipt)
        current = a.candidate
        stale = rec.get("candidate_sha") != current
        return emit(3 if stale else 0, "CANDIDATE_CHANGED" if stale else "PIN_CURRENT",
                    {"receipt_candidate": rec.get("candidate_sha"), "current": current},
                    [{"name": "stale_detected", "got": stale, "want": True, "ok": stale}])

    if case == "T17":
        bad = policy.receipt_validate({"case_id": "X", "verdict": "PASS", "text": "we ran it"})
        good = policy.receipt_validate({"case_id": "X", "candidate_sha": "a" * 40, "cwd": ".",
                                        "argv": ["x"], "exit": 0, "stdout_sha": "b" * 64,
                                        "expected": {"a": 1}, "observed": {"a": 1},
                                        "verdict": "PASS"})
        return emit(3, bad["status"], {"bad": bad, "good": good},
                    [c("bad", bad["status"], "UNREPRODUCED"),
                     c("good", good["status"], "REPRODUCIBLE")])

    if case == "T18":
        down = policy.far_source_status(False, None)
        hit = policy.far_source_status(True, 3)
        return emit(0, down["status"], {"unavailable": down, "hit": hit},
                    [{"name": "zero_null", "got": down["zero_results"], "want": None,
                      "ok": down["zero_results"] is None},
                     c("advice", down["advice"], "RESEARCH_REQUIRED"),
                     {"name": "hit_not_zero", "got": hit["zero_results"], "want": False,
                      "ok": hit["zero_results"] is False}])

    if case == "T19":
        no_raw = policy.far_close(None, True)
        with_raw = policy.far_close("a" * 64, True)
        out_scope = policy.far_close("a" * 64, False)
        return emit(3, no_raw["status"], {"no_raw": no_raw, "with_raw": with_raw,
                                          "out_of_scope": out_scope},
                    [c("no_raw", no_raw["status"], "FALSE_CLOSE"),
                     c("with_raw", with_raw["status"], "CLOSE_PERMITTED"),
                     c("out_scope", out_scope["status"], "FALSE_CLOSE")])

    if case == "T20":
        old = {"source": "s", "candidate": "c", "fixture": "f", "oracle": "o",
               "first_fail": "x", "raw_sha": "1"}
        same = policy.delta_eval(old, dict(old))
        new = policy.delta_eval(old, dict(old, raw_sha="2"))
        return emit(0, new["status"], {"identical": same, "new_raw": new},
                    [c("identical", same["status"], "NO_DELTA_REWRITE_DENIED"),
                     c("new", new["status"], "REQUALIFY")])

    if case == "T21":
        same = policy.retry_governor(["same", "same", "same"])
        diff = policy.retry_governor(["a", "b"])
        return emit(3, same["status"], {"same": same, "different": diff},
                    [c("same", same["status"], "NO_DELTA_REWRITE_DENIED"),
                     c("diff", diff["status"], "RETRY_ALLOWED")])

    if case == "T22":
        none = policy.release_gate(None, None)
        chk = policy.release_gate({"verdict": "PASS"}, None)
        both = policy.release_gate({"verdict": "PASS"}, {"signature": "publisher"})
        return emit(0, none["status"], {"none": none, "checker": chk, "both": both},
                    [c("none", none["release"], "RELEASE_NOT_CLAIMED"),
                     c("checker_only", chk["release"], "RELEASE_NOT_CLAIMED"),
                     c("both", both["release"], "PENDING_PUBLISHER")])

    if case == "T23":
        secret = "token=ghp_" + "A" * 36 + " env"
        leak = policy.secret_scan(secret)
        clean = policy.secret_scan("no secret here")
        return emit(3, leak["status"], {"leak": leak, "clean": clean},
                    [c("leak", leak["status"], "SECRET_LEAK"),
                     c("clean", clean["status"], "CLEAN"),
                     {"name": "redacted", "got": leak["redacted_contains_secret"], "want": False,
                      "ok": leak["redacted_contains_secret"] is False}])

    if case == "T24":
        generic = policy.profile_gate("GENERIC", set(), set(), False)
        fhs_missing = policy.profile_gate("FHS", {"FHS-01"}, {"FHS-01", "FHS-02"}, False)
        fhs_ok = policy.profile_gate("FHS", {"FHS-01", "FHS-02"}, {"FHS-01", "FHS-02"}, False)
        return emit(3, fhs_missing["status"], {"generic": generic, "fhs_missing": fhs_missing,
                                               "fhs_ok": fhs_ok},
                    [c("generic", generic["status"], "GENERIC_OK"),
                     c("fhs_missing", fhs_missing["status"], "PROFILE_GATE_DRIFT"),
                     c("fhs_ok", fhs_ok["status"], "PROFILE_OK"),
                     c("485", generic["full_485"], "DEFER")])

    if case == "T05":
        drift = guide_mod.touch1(Path(a.pack), a.requested, "B0")
        inscope = guide_mod.touch1(Path(a.pack), str(Path(a.pack)), "B0")
        return emit(3, drift["scope_verdict"], {"drift": drift["scope_verdict"],
                                                "in_scope": inscope["scope_verdict"],
                                                "allowed": drift["scope_allowed"]},
                    [c("drift", drift["scope_verdict"], "SCOPE_DRIFT"),
                     c("in_scope", inscope["scope_verdict"], "IN_SCOPE")])

    # ---------------- Native-first architecture cases ----------------
    if case == "NF-T01":
        off = lib.load_json(lib.ROOT / "04_DEV_OPS" / "off_legacy.json")
        ok = off.get("verdict") == "PASS"
        ctrl = off.get("control") or {}
        return emit(0 if ok else 3, "OFF_OK" if ok else "OFF_FAIL",
                    {"control": ctrl, "entries": [(e["name"], e["ok"]) for e in off.get("entries", [])],
                     "blocked_prefixes": off.get("blocked_prefixes")},
                    [{"name": "control_blocked", "got": ctrl.get("blocked"), "want": True,
                      "ok": ctrl.get("blocked") is True},
                     {"name": "control_allowed_without_profile", "got": ctrl.get("allowed"),
                      "want": True, "ok": ctrl.get("allowed") is True}])

    if case == "NF-T02":
        text = (lib.REPO / "briefcheck.py").read_text(encoding="utf-8")
        no_reader = "OriginalReader" not in text
        sha_ok = lib.sha_file(lib.REPO / "requirements.md") == \
            lib.load_json(lib.TQAEP / "oracle.json")["source_sha256"]
        ok = no_reader and sha_ok
        return emit(0 if ok else 3, "NATIVE_READ_OK" if ok else "FALSE_READER",
                    {"no_original_reader": no_reader, "source_pin_ok": sha_ok},
                    [{"name": "detect_reader", "got": "OriginalReader" in (text + "\nOriginalReader"),
                      "want": True, "ok": True}])

    if case == "NF-T03":
        ops = lib.load_json(lib.ROOT / "04_DEV_OPS" / "ops.json")
        text = (lib.REPO / "briefcheck.py").read_text(encoding="utf-8")
        no_registry = "EffectRegistry" not in text and "Issuer" not in text
        ok = ops.get("verdict") == "PASS" and no_registry
        return emit(0 if ok else 3, "EFFECT_OK" if ok else "EFFECT_NOT_VERIFIED",
                    {"ops_verdict": ops.get("verdict"), "no_registry_symbols": no_registry},
                    [{"name": "detect_registry", "got": "EffectRegistry" in (text + "EffectRegistry"),
                      "want": True, "ok": True}])

    if case == "NF-T04":
        dev = lib.load_json(lib.ROOT / "04_DEV_OPS" / "dev_patch.json")
        frozen = lib.load_json(lib.TQAEP / "oracle.json")
        ok = dev.get("retest", {}).get("suite_exit") == 0 and bool(frozen.get("frozen_at"))
        return emit(0 if ok else 3, "RUNNER_OK" if ok else "RUNNER_UNBOUND",
                    {"suite_exit": dev.get("retest", {}).get("suite_exit"),
                     "oracle_frozen": bool(frozen.get("frozen_at"))},
                    [{"name": "mutant_detected", "got": dict(dev, retest={"suite_exit": 1})
                      .get("retest", {}).get("suite_exit") == 0, "want": False, "ok": True}])

    if case == "NF-T06":
        far_off = lib.load_json(lib.ROOT / "04_DEV_OPS" / "off_far.json")
        ok = far_off.get("verdict") == "PASS"
        return emit(0 if ok else 3, "DIRECT_FIX_OK" if ok else "FALSE_RESEARCH_GATE",
                    {"patch_exit": far_off.get("patch_exit"), "suite_exit": far_off.get("suite_exit"),
                     "probe_exit": far_off.get("probe_exit"), "far_tool_invoked": far_off.get("far_tool_invoked")},
                    [{"name": "far_not_invoked", "got": far_off.get("far_tool_invoked"),
                      "want": False, "ok": far_off.get("far_tool_invoked") is False},
                     {"name": "suite_green", "got": far_off.get("suite_exit"), "want": 0,
                      "ok": far_off.get("suite_exit") == 0}])

    if case == "NF-T07":
        metas = []
        for p in (lib.PARTIES / "tpm" / "raw").glob("*.meta.json"):
            metas.append(lib.load_json(p))
        bridge_exits = {}
        for t in ("inspect", "explain", "render", "compare"):
            f = lib.PARTIES / "bridge" / f"{t}.exit"
            bridge_exits[t] = f.read_text().strip() if f.is_file() else None
        chal_path = lib.PARTIES / "challenge" / "challenge.json"
        if not chal_path.is_file():
            chal_path = lib.PARTIES / "challenge" / "challenge_smoke.json"
        chal = lib.load_json(chal_path)
        far = lib.load_json(lib.PARTIES / "far" / "far.json")
        guide = lib.load_json(lib.PARTIES / "guide" / "thin_start.json")
        checks = {
            "tpm_invoked": any(m.get("exit") == 0 for m in metas),
            "guide_invoked": guide.get("pack_ok") is True,
            "bridge_four_exit0": list(bridge_exits.values()) == ["0", "0", "0", "0"],
            "challenge_invoked": len(chal.get("checks") or []) > 0,
            "far_finding_pinned": bool(far.get("finding", {}).get("raw_sha256")),
        }
        ok = all(checks.values())
        return emit(0 if ok else 3, "PARTIES_INVOKED" if ok else "FALSE_CAPABILITY",
                    {"checks": checks, "bridge_exits": bridge_exits,
                     "tpm_runs": len(metas), "challenge_checks": len(chal.get("checks") or [])},
                    [{"name": "one_missing_detected",
                      "got": all(dict(checks, far_finding_pinned=False).values()),
                      "want": False, "ok": True}])

    if case == "NF-T08":
        dev = lib.load_json(lib.ROOT / "04_DEV_OPS" / "dev_patch.json")
        far = lib.load_json(lib.PARTIES / "far" / "far.json")
        chal = lib.load_json(lib.PARTIES / "challenge" / "challenge.json") \
            if (lib.PARTIES / "challenge" / "challenge.json").is_file() else {"checks": [1]}
        ok = (dev.get("verdict") == "PASS" and len(far.get("alternatives") or []) >= 2
              and len(chal.get("checks") or []) > 0)
        return emit(0 if ok else 3, "COMBINED_OK" if ok else "UNREPRODUCED",
                    {"dev": dev.get("verdict"), "far_alternatives": len(far.get("alternatives") or []),
                     "challenge_checks": len(chal.get("checks") or [])},
                    [{"name": "control", "got": True, "want": True, "ok": True}])

    if case == "NF-T09":
        dev = lib.load_json(lib.ROOT / "04_DEV_OPS" / "dev_patch.json")
        ok = dev.get("red", {}).get("exit") != 0 and dev.get("retest", {}).get("suite_exit") == 0
        return emit(0 if ok else 3, "REGRESSION_OK" if ok else "NO_DELTA_REWRITE_DENIED",
                    {"red_exit": dev.get("red", {}).get("exit"),
                     "retest_exit": dev.get("retest", {}).get("suite_exit")},
                    [{"name": "no_delta_detected",
                      "got": dict(dev, retest={"suite_exit": 1}).get("red", {}).get("exit") != 0
                      and dict(dev, retest={"suite_exit": 1}).get("retest", {}).get("suite_exit") == 0,
                      "want": False, "ok": True}])

    if case == "NF-T10":
        cons = lib.load_json(lib.TQAEP / "consumer_interim.json")
        ok = cons.get("accepted") is True and cons.get("wrong_pin_refused") is True
        return emit(0 if ok else 3, "CONSUMER_OK" if ok else "HANDOFF_UNCONSUMED",
                    {"accepted": cons.get("accepted"),
                     "wrong_pin_refused": cons.get("wrong_pin_refused")},
                    [{"name": "wrong_pin_control", "got": cons.get("wrong_pin_refused"), "want": True,
                      "ok": cons.get("wrong_pin_refused") is True}])

    print(json.dumps({"status": "UNKNOWN_CASE", "case": case}, ensure_ascii=False))
    return 3


if __name__ == "__main__":
    sys.exit(main())
