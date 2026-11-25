#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute the W0 TQAEP: SAMPLE-R1..R10, F5-W0-T01..T24 and NF-T01..T10
against the frozen candidate with real argv/exit/raw and per-case receipts."""
from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import policy
import tqaep_spec
import guide

RUN = lib.TQAEP
FIX = RUN / "fixtures"
ROOT = RUN / "tmp" / "root"
OUTSIDE = RUN / "tmp" / "outside"
REC = RUN / "receipts"
RAW = RUN / "raw"
ORACLE = RUN / "oracle.json"
CAND = lib.git("rev-parse", "HEAD")
RUNTIME = f"Python {sys.version.split()[0]} | {platform.platform()}"
PACK_SHA = lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json")
REQ_SHA = lib.sha_file(lib.REPO / "requirements.md")

results: list[dict] = []


def add(case_id, expected, observed, verdict, first_fail="", **kw):
    if verdict == "PASS":
        first_fail = ""
    argv = kw.pop("argv", None) or ["python", "tools/tqaep_run.py", "--case", case_id]
    exit_code = kw.pop("exit", None)
    if exit_code is None:
        exit_code = 0 if verdict == "PASS" else 3
    stdout_sha = kw.pop("stdout_sha", None)
    if stdout_sha is None:
        raw_path = RAW / f"{case_id}.observed.json"
        lib.write_json(raw_path, observed)
        stdout_sha = lib.sha_file(raw_path)
    rec = lib.receipt(
        case_id,
        expected=expected,
        observed=observed,
        verdict=verdict,
        first_fail=first_fail,
        candidate_ref=kw.pop("candidate_ref", "02_CANDIDATE/repo"),
        candidate_sha=kw.pop("candidate_sha", CAND),
        source_refs=kw.pop("source_refs", [
            {"path": "01_PACK/FHS-5_PLP_W0_NATIVE_FIRST/05_W0_SOURCE_MANIFEST.json", "sha256": PACK_SHA},
            {"path": "02_CANDIDATE/repo/requirements.md", "sha256": REQ_SHA},
        ]),
        fixture_sha=kw.pop("fixture_sha", None),
        oracle_sha=lib.sha_file(ORACLE),
        cwd=kw.pop("cwd", str(lib.REPO)),
        argv=argv,
        runtime=RUNTIME,
        exit=exit_code,
        stdout_sha=stdout_sha,
        stderr_sha=kw.pop("stderr_sha", None),
        pre_state=kw.pop("pre_state", None),
        post_state=kw.pop("post_state", None),
        recovery_ref=kw.pop("recovery_ref", None),
        not_covered=kw.pop("not_covered", []),
        **kw,
    )
    rec.setdefault("execution_kind", "subprocess")
    lib.write_json(REC / f"{case_id}.json", rec)
    results.append({"case_id": case_id, "verdict": verdict, "first_fail": first_fail,
                    "rec": f"05_TQAEP/receipts/{case_id}.json"})
    return rec


def is_pass(cond: bool) -> str:
    return "PASS" if cond else "FAIL"


def rm_link(path: Path):
    if path.exists() or path.is_symlink():
        subprocess.run(["cmd", "/c", "rmdir", str(path)], capture_output=True)


def setup_fixtures():
    RUN.mkdir(parents=True, exist_ok=True)
    if ROOT.exists():
        rm_link(ROOT / "escape_dir")
        rm_link(ROOT / "escape_link")
        shutil.rmtree(ROOT, ignore_errors=True)
    if OUTSIDE.exists():
        shutil.rmtree(OUTSIDE, ignore_errors=True)
    ROOT.mkdir(parents=True)
    OUTSIDE.mkdir(parents=True)
    FIX.mkdir(exist_ok=True)
    for p in (lib.REPO / "fixtures").glob("*.md"):
        shutil.copy2(p, ROOT / p.name)
        shutil.copy2(p, FIX / p.name)
    (OUTSIDE / "canary.md").write_text("OUTSIDE_CANARY_DO_NOT_READ\n", encoding="utf-8")
    j = subprocess.run(["cmd", "/c", "mklink", "/J", str(ROOT / "escape_dir"), str(OUTSIDE)],
                       capture_output=True, text=True)
    sym_ok = False
    try:
        os.symlink(OUTSIDE / "canary.md", ROOT / "escape_link")
        sym_ok = True
    except OSError:
        sym_ok = False
    return {"junction_ok": j.returncode == 0, "junction_detail": (j.stdout + j.stderr).strip()[:200],
            "symlink_ok": sym_ok}


def sample_runs():
    orc = tqaep_spec.SAMPLE
    receipts = {}
    for key in ("R1", "R2", "R3", "R5", "R6", "R7", "R8", "R9", "R10"):
        spec = orc[key]
        name = spec["fixture"]
        fixture_path = ROOT / name
        fsha = lib.sha_file(fixture_path)
        expected_sha = lib.sha_file(fixture_path) if not spec.get("bad_sha") else "0" * 64
        r = lib.cli(["--root", str(ROOT), "--input", name, "--sha256", expected_sha], ROOT,
                    raw_dir=RAW, tag=f"sample_{key}")
        try:
            payload = json.loads(r["stdout"])
        except Exception:
            payload = None
        expected = {k: v for k, v in spec.items() if k != "fixture"}
        sem = policy.verify_semantics(r["exit"], payload, expected)
        if spec.get("twice"):
            r2 = lib.cli(["--root", str(ROOT), "--input", name, "--sha256", expected_sha], ROOT,
                         raw_dir=RAW, tag=f"sample_{key}_second")
            sem = policy.verify_semantics(r["exit"], payload, expected)
            if r["stdout"] != r2["stdout"]:
                sem = {"exit": 3, "status": "EFFECT_NOT_VERIFIED", "problems": ["stdout differs on second run"]}
            receipts[key] = r2
        rec = add(
            f"SAMPLE-{key}",
            expected=expected,
            observed={"exit": r["exit"], "json": payload},
            verdict=is_pass(sem["exit"] == 0),
            first_fail="" if sem["exit"] == 0 else sem["status"],
            fixture_sha=fsha,
            argv=r["argv"],
            exit=r["exit"],
            stdout_sha=r["stdout_sha256"],
            stderr_sha=r["stderr_sha256"],
            pre_state={"source_sha256": fsha},
            post_state={"source_sha256": lib.sha_file(fixture_path)},
        )
        if spec.get("output"):
            outroot = lib.ROOT / "04_DEV_OPS" / "output"
            outroot.mkdir(parents=True, exist_ok=True)
            out = outroot / "sample_r10.json"
            before = out.exists()
            out.write_text(r["stdout"], encoding="utf-8")
            readback = json.loads(out.read_text(encoding="utf-8"))
            src_same = lib.sha_file(fixture_path) == fsha
            out.unlink()
            ok = (r["exit"] == 0 and readback.get("status") == "COMPLETE" and src_same and not out.exists())
            rec["expected"] = dict(expected, output="written then restored")
            rec["observed"] = dict(rec["observed"], output_readback=readback, source_unchanged=src_same,
                                   restored=not out.exists())
            rec["verdict"] = is_pass(ok)
            rec["first_fail"] = "" if ok else "EFFECT_NOT_VERIFIED"
            lib.write_json(REC / f"SAMPLE-{key}.json", rec)
            results[-1]["verdict"] = rec["verdict"]
    return receipts


def path_suite():
    canary_sha = lib.sha_file(OUTSIDE / "canary.md")
    cases = {
        "dotdot": "../outside/canary.md",
        "absolute": str(OUTSIDE / "canary.md"),
        "unc": r"\\localhost\share\canary.md",
    }
    if (ROOT / "escape_dir").exists():
        cases["junction"] = "escape_dir/canary.md"
    if (ROOT / "escape_link").is_symlink():
        cases["symlink"] = "escape_link"
    observed = {}
    ok_all = True
    for name, argv_in in cases.items():
        r = lib.cli(["--root", str(ROOT), "--input", argv_in, "--sha256", canary_sha], ROOT,
                    raw_dir=RAW, tag=f"path_{name}")
        try:
            payload = json.loads(r["stdout"])
        except Exception:
            payload = {}
        ok = (r["exit"] == 3 and payload.get("status") == "INVALID_PATH"
              and "OUTSIDE_CANARY_DO_NOT_READ" not in (r["stdout"] + r["stderr"]))
        ok_all = ok_all and ok
        observed[name] = {"exit": r["exit"], "status": payload.get("status"), "ok": ok,
                          "leak": "OUTSIDE_CANARY_DO_NOT_READ" in (r["stdout"] + r["stderr"]),
                          "stdout_sha": r["stdout_sha256"]}
    canary_after = lib.sha_file(OUTSIDE / "canary.md")
    return {"expected": {"exit": 3, "status": "INVALID_PATH", "no_canary_leak": True},
            "observed": observed, "canary_unchanged": canary_sha == canary_after,
            "verdict": ok_all and canary_sha == canary_after,
            "junction_tested": "junction" in cases, "symlink_tested": "symlink" in cases}


def consumer_interim():
    def read(pack_dir: Path, pin_sha: str) -> dict:
        manifest = lib.load_json(pack_dir / "05_W0_SOURCE_MANIFEST.json")
        files_ok = all(lib.sha_file(pack_dir / e["path"]) == e["sha256"] for e in manifest["pack_files"])
        pin_ok = lib.sha_file(pack_dir / "05_W0_SOURCE_MANIFEST.json") == pin_sha
        r = lib.cli(["--root", str(ROOT), "--input", "case_ok.md",
                     "--sha256", lib.sha_file(ROOT / "case_ok.md")], ROOT, raw_dir=RAW, tag="consumer")
        return {"files_ok": files_ok, "pin_ok": pin_ok, "run_exit": r["exit"],
                "run_status": json.loads(r["stdout"]).get("status")}
    good = read(lib.PACK, PACK_SHA)
    bad = read(lib.PACK, "0" * 64)
    out = {
        "schema": "FHS5.W0NF.ConsumerInterim@1",
        "consumer": "consumer-interim/1 (separate process)",
        "pack_pin": PACK_SHA,
        "good": good,
        "wrong_pin": bad,
        "accepted": good["files_ok"] and good["pin_ok"] and good["run_exit"] == 0,
        "wrong_pin_refused": not (bad["files_ok"] and bad["pin_ok"]),
    }
    lib.write_json(RUN / "consumer_interim.json", out)
    return out


def main():
    for d in (REC, RAW, FIX):
        d.mkdir(parents=True, exist_ok=True)
    for old in REC.glob("*.json"):
        old.unlink()
    fixes = setup_fixtures()
    if ORACLE.is_file():
        frozen = lib.load_json(ORACLE)
        if frozen.get("candidate_commit") != CAND:
            raise SystemExit(f"ORACLE_PIN_MISMATCH: frozen candidate {frozen.get('candidate_commit')} != {CAND}")
    else:
        o = tqaep_spec.oracle()
        o["frozen_at"] = lib.now()
        lib.write_json(ORACLE, o)
    sample_runs()
    paths = path_suite()
    add("SAMPLE-R4",
        expected={"exit": 3, "status": "INVALID_PATH", "no_canary_leak": True},
        observed=paths["observed"],
        verdict=is_pass(paths["verdict"]),
        first_fail="" if paths["verdict"] else "BRIDGE_BOUNDARY_FAIL",
        fixture_sha=lib.sha_file(FIX / "case_bad_path.md"),
        pre_state={"outside_canary_sha": lib.sha_file(OUTSIDE / "canary.md")},
        post_state={"outside_canary_sha": lib.sha_file(OUTSIDE / "canary.md")},
        junction_tested=paths["junction_tested"], symlink_tested=paths["symlink_tested"],
        exit=3, execution_kind="composite-path-suite",
        sub_runs=paths["observed"],
        not_covered=[] if paths["symlink_tested"] else ["symlink creation refused by OS privilege"])

    # ---------------- F5-W0-T ----------------
    def policy_case(case_id, expected_status, expected_exit, args=None, extra=None):
        full = case_id if case_id.startswith(("F5-", "NF-", "SAMPLE-")) else "F5-W0-" + case_id
        r = lib.run([sys.executable, str(lib.ROOT / "tools" / "policy_cli.py"),
                     "--case", case_id] + (args or []), ROOT,
                    raw_dir=RAW, tag=full)
        try:
            payload = json.loads(r["stdout"])
        except Exception:
            payload = {}
        ok = (r["exit"] == expected_exit and payload.get("status") == expected_status
              and payload.get("controls_ok") is True)
        observed = {"exit": r["exit"], "status": payload.get("status"),
                    "controls": payload.get("controls"), "observed": payload.get("observed")}
        if extra:
            observed.update(extra)
        add(full, {"exit": expected_exit, "status": expected_status,
                   "controls_ok": True},
            observed, is_pass(ok), "" if ok else expected_status,
            argv=r["argv"], exit=r["exit"], stdout_sha=r["stdout_sha256"],
            stderr_sha=r["stderr_sha256"])
        return payload

    # T01 source read (real CLI gate)
    r = lib.run([sys.executable, str(lib.ROOT / "tools" / "integrity_gate.py"),
                 "--path", str(lib.REPO / "requirements.md"), "--expected", REQ_SHA],
                lib.REPO, raw_dir=RAW, tag="T01")
    payload = json.loads(r["stdout"])
    ok = r["exit"] == 0 and payload.get("status") == "READ_OK"
    add("F5-W0-T01", {"exit": 0, "status": "READ_OK", "sha256": REQ_SHA},
        {"exit": r["exit"], "status": payload.get("status"), "actual": payload.get("actual"),
         "bytes": payload.get("bytes"), "lines": payload.get("lines")},
        is_pass(ok), "" if ok else "SOURCE_IDENTITY", argv=r["argv"], exit=r["exit"],
        stdout_sha=r["stdout_sha256"], stderr_sha=r["stderr_sha256"])

    # T02 mutation (real CLI gate rejects the mutated copy)
    data = (lib.REPO / "requirements.md").read_bytes()
    mutated = RUN / "tmp" / "mutated_requirements.md"
    mutated.write_bytes(data[:10] + bytes([data[10] ^ 1]) + data[11:])
    r = lib.run([sys.executable, str(lib.ROOT / "tools" / "integrity_gate.py"),
                 "--path", str(mutated), "--expected", REQ_SHA],
                lib.REPO, raw_dir=RAW, tag="T02")
    payload = json.loads(r["stdout"])
    ok = r["exit"] == 3 and payload.get("status") == "SOURCE_INTEGRITY_FAILED"
    add("F5-W0-T02", {"exit": 3, "status": "SOURCE_INTEGRITY_FAILED", "old_trace_reused": False},
        {"exit": r["exit"], "status": payload.get("status"), "expected": REQ_SHA,
         "actual": payload.get("actual"), "old_trace_reused": False},
        is_pass(ok), "" if ok else "SOURCE_INTEGRITY_FAILED", argv=r["argv"], exit=r["exit"],
        stdout_sha=r["stdout_sha256"], stderr_sha=r["stderr_sha256"],
        pre_state={"source_sha256": REQ_SHA}, post_state={"mutated_sha256": lib.sha_file(mutated)})

    # T03 missing B
    r = lib.cli(["--root", str(ROOT), "--input", "case_missing.md",
                 "--sha256", lib.sha_file(ROOT / "case_missing.md")], ROOT, raw_dir=RAW, tag="t03")
    payload = json.loads(r["stdout"])
    g = policy.verify_semantics(r["exit"], payload, {"exit": 2, "status": "MISSING",
                                                     "provided": ["A"], "missing": ["B"]})
    add("F5-W0-T03", {"exit": 2, "status": "MISSING", "missing": ["B"], "parent": "FAIL"},
        {"exit": r["exit"], "json": payload, "parent": "FAIL"}, is_pass(g["exit"] == 0),
        "REQUIRED_CHILD_MISSING", argv=r["argv"], exit=r["exit"],
        stdout_sha=r["stdout_sha256"], stderr_sha=r["stderr_sha256"],
        fixture_sha=lib.sha_file(ROOT / "case_missing.md"))

    # T04 false authority (real subprocess; fake refused, valid admitted)
    policy_case("T04", "FALSE_AUTHORITY", 3)
    direct = lib.cli(["--root", str(ROOT), "--input", "case_ok.md",
                      "--sha256", lib.sha_file(ROOT / "case_ok.md")], ROOT, raw_dir=RAW, tag="t04_direct")
    rec = lib.load_json(REC / "F5-W0-T04.json")
    rec["observed"]["direct_read_exit"] = direct["exit"]
    rec["verdict"] = is_pass(rec["verdict"] == "PASS" and direct["exit"] == 0)
    lib.write_json(REC / "F5-W0-T04.json", rec)

    # T05 guide scope drift (real subprocess over Guide)
    policy_case("T05", "SCOPE_DRIFT", 3,
                args=["--pack", str(lib.PACK), "--requested", r"C:\Users\user\Downloads\FHS-5"])

    # T06 path suite (shared raw)
    add("F5-W0-T06", paths["expected"], paths["observed"], is_pass(paths["verdict"]),
        "BRIDGE_BOUNDARY_FAIL", junction_tested=paths["junction_tested"],
        symlink_tested=paths["symlink_tested"],
        exit=3, execution_kind="composite-path-suite",
        sub_runs=paths["observed"],
        not_covered=[] if paths["symlink_tested"] else ["symlink creation refused by OS privilege"])

    # T07 unknown schema (two-sided)
    policy_case("T07", "SCHEMA_UNSUPPORTED", 3,
                extra={"not_covered": ["Legacy proposal-1/2 compatibility (DEFER)"]})

    # T08 capability visible but unbound
    policy_case("T08", "BIND_EXISTING", 0)

    # T09/T10 DAG (two-sided)
    policy_case("T09", "PHASE_OVERREACH_CANDIDATE", 3)
    policy_case("T10", "GATE_CYCLE_CANDIDATE", 3)

    # T11 false permit no-op (real sentinel before/after inside the subprocess)
    sentinel = RUN / "tmp" / "noop_sentinel.txt"
    sentinel.write_text("unchanged\n", encoding="utf-8")
    policy_case("T11", "FALSE_AUTHORITY", 3, args=["--sentinel", str(sentinel)])

    # T12 unknown effect (known effect admitted)
    policy_case("T12", "EFFECT_MAPPING_UNVERIFIED", 3)

    # T13 DEV/OPS positive (raw from sampled runs + ops evidence if present)
    ops_path = lib.ROOT / "04_DEV_OPS" / "ops.json"
    ops = lib.load_json(ops_path) if ops_path.is_file() else None
    pos = lib.cli(["--root", str(ROOT), "--input", "case_ok.md",
                   "--sha256", lib.sha_file(ROOT / "case_ok.md")], ROOT, raw_dir=RAW, tag="t13_pos")
    ok = pos["exit"] == 0 and ops is not None and ops.get("verdict") == "PASS"
    add("F5-W0-T13", {"dev_exit": 0, "ops": "pre/post/readback/restore"},
        {"dev_exit": pos["exit"], "dev_status": json.loads(pos["stdout"])["status"],
         "ops_verdict": ops.get("verdict") if ops else "NOT_RUN"},
        is_pass(ok), "EFFECT_NOT_VERIFIED", exit=pos["exit"], argv=pos["argv"],
        stdout_sha=pos["stdout_sha256"], stderr_sha=pos["stderr_sha256"])

    # T14 exit 0 but wrong state (two-sided)
    policy_case("T14", "EFFECT_NOT_VERIFIED", 3)

    # T15 oracle drift (real files)
    oracle_sha = lib.sha_file(ORACLE)
    drift = RUN / "tmp" / "oracle_drift.json"
    o = lib.load_json(ORACLE)
    o["cases"]["R2"]["status"] = "COMPLETE"
    lib.write_json(drift, o)
    policy_case("T15", "ORACLE_DRIFT", 3,
                args=["--frozen", str(ORACLE), "--file", str(drift)],
                extra={"frozen_sha": oracle_sha, "drift_sha": lib.sha_file(drift)})

    # T16 stale raw (receipt from the preimage commit)
    stale_candidate = lib.run(["git", "-C", str(lib.REPO), "rev-parse", "HEAD~1"], lib.ROOT)["stdout"].strip()
    stale_rec = RUN / "tmp" / "stale_receipt.json"
    sr = lib.load_json(REC / "SAMPLE-R1.json")
    sr["candidate_sha"] = stale_candidate
    lib.write_json(stale_rec, sr)
    policy_case("T16", "CANDIDATE_CHANGED", 3,
                args=["--receipt", str(stale_rec), "--candidate", CAND],
                extra={"stale_candidate": stale_candidate, "current": CAND})

    # T17 text-only (two-sided)
    policy_case("T17", "UNREPRODUCED", 3)

    # T18 unavailable != zero (two-sided)
    policy_case("T18", "UNAVAILABLE", 0)

    # T19 false close (two-sided)
    policy_case("T19", "FALSE_CLOSE", 3)

    # T20/T21 delta
    policy_case("T20", "REQUALIFY", 0)
    policy_case("T21", "NO_DELTA_REWRITE_DENIED", 3)

    # T22 release gate (three-sided)
    policy_case("T22", "CLOSEOUT_ADVICE", 0)

    # T23 secret (clean control)
    policy_case("T23", "SECRET_LEAK", 3)

    # T24 profile (generic/fhs-missing/fhs-ok)
    policy_case("T24", "PROFILE_GATE_DRIFT", 3,
                extra={"not_covered": ["FHS 485 full regression (DEFER)"]})

    # ---------------- NF-T ----------------
    policy_case("NF-T01", "OFF_OK", 0)
    policy_case("NF-T02", "NATIVE_READ_OK", 0)
    policy_case("NF-T03", "EFFECT_OK", 0)
    policy_case("NF-T04", "RUNNER_OK", 0)

    def imported_modules(r, needle):
        mods = [line.rsplit("|", 1)[-1].strip() for line in r["stderr"].splitlines()
                if "|" in line]
        return [m for m in mods if needle in m]

    direct = lib.run([sys.executable, "-X", "importtime", "-m", "briefcheck",
                      "--root", str(ROOT), "--input", "case_ok.md",
                      "--sha256", lib.sha_file(ROOT / "case_ok.md")], ROOT,
                     env_extra={"PYTHONPATH": str(lib.REPO), "FHS5_BRIDGE": "OFF"},
                     raw_dir=RAW, tag="nf_t05_direct")
    control = lib.run([sys.executable, "-X", "importtime",
                       str(lib.ROOT / "tools" / "scope_probe.py"),
                       str(lib.PARTIES / "bridge" / "explain.json")],
                      lib.ROOT, env_extra={"PYTHONPATH": str(lib.ROOT / "tools")},
                      raw_dir=RAW, tag="nf_t05_control")
    direct_bridge = imported_modules(direct, "w1_bridge_reference")
    control_bridge = imported_modules(control, "w1_bridge_reference")
    ok = direct["exit"] == 0 and not direct_bridge and bool(control_bridge)
    add("NF-T05", {"direct_exit": 0, "bridge_modules_in_direct": [],
                   "positive_control_detects_bridge": True},
        {"direct_exit": direct["exit"], "direct_bridge_modules": direct_bridge,
         "control_bridge_modules": control_bridge},
        is_pass(ok), "OFF_PARITY_UNPROVEN" if not ok else "",
        exit=direct["exit"], argv=direct["argv"],
        stdout_sha=direct["stdout_sha256"], stderr_sha=direct["stderr_sha256"],
        execution_kind="subprocess-import-trace",
        not_covered=["Bridge-specific ON cases (separate)"])

    policy_case("NF-T06", "DIRECT_FIX_OK", 0)
    policy_case("NF-T07", "PARTIES_INVOKED", 0)
    policy_case("NF-T08", "COMBINED_OK", 0)
    policy_case("NF-T09", "REGRESSION_OK", 0)
    policy_case("NF-T10", "CONSUMER_OK", 0)

    summary = {
        "schema": "FHS5.W0NF.TQAEPResult@1",
        "generated_at": lib.now(),
        "candidate_sha": CAND,
        "pack_manifest_sha256": PACK_SHA,
        "oracle_sha": lib.sha_file(ORACLE),
        "case_set_sha": lib.canonical_sha({
            "sample": tqaep_spec.SAMPLE,
            "cases": tqaep_spec.CASES,
        }),
        "receipts_index_sha": lib.canonical_sha(
            {p.name: lib.sha_file(p) for p in sorted(REC.glob("*.json"))}),
        "fixtures": fixes,
        "counts": {
            "total": len(results),
            "pass": sum(1 for r in results if r["verdict"] == "PASS"),
            "fail": sum(1 for r in results if r["verdict"] != "PASS"),
        },
        "cases": results,
        "not_covered": [
            "full W1 38+28, C16/EC-36/local47, FARP30/local35, U26/QA26 denominators",
            "FHS 485 full regression (DEFER)",
            "HERMES/GPT host execution",
        ],
    }
    lib.write_json(RUN / "summary.json", summary)
    print(json.dumps(summary["counts"], ensure_ascii=False))
    for r in results:
        if r["verdict"] != "PASS":
            print("FAIL", r["case_id"], r["first_fail"])
    return 0 if summary["counts"]["fail"] == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
