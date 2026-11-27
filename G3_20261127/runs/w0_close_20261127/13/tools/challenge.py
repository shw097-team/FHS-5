#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent Challenge/Checker over the frozen candidate, oracle, receipts
and pack. Runs in its own worktree/process; never edits subject or oracle."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import policy
import tqaep_spec

REQUIRED_RECEIPT = ["case_id", "candidate_sha", "cwd", "argv", "exit", "stdout_sha",
                    "expected", "observed", "verdict"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workroot", required=True)
    ap.add_argument("--mode", choices=["smoke", "full"], default="full")
    a = ap.parse_args()
    cand = Path(a.candidate).resolve()
    oracle_path = Path(a.oracle).resolve()
    receipt_dir = Path(a.receipts).resolve()
    pack = Path(a.pack).resolve()
    summary = json.loads(Path(a.summary).read_text(encoding="utf-8")) if Path(a.summary).is_file() else {}
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    work = Path(a.workroot).resolve()
    work.mkdir(parents=True, exist_ok=True)

    checks, findings, not_verified = [], [], []
    subject_before = lib.snapshot(cand)
    g = cand / ".git"

    def git_meta():
        items = {}
        for rel in ("HEAD", "index"):
            p = g / rel
            items[rel] = lib.sha_file(p) if p.is_file() else None
        wt = g / "worktrees"
        items["worktrees"] = sorted(p.name for p in wt.glob("*")) if wt.is_dir() else []
        return items

    subject_git_before = git_meta()

    def check(cid, ok, observed, severity="MAJOR", cls="checker_mismatch"):
        checks.append({"id": cid, "ok": bool(ok), "observed": observed})
        if not ok:
            findings.append({
                "id": "CH-" + cid, "severity": severity, "class": cls,
                "subject_sha": oracle.get("candidate_commit", ""),
                "command": " ".join([sys.executable, "tools/challenge.py"]),
                "exit": 3,
                "raw_sha256": lib.canonical_sha(observed),
                "reproduction": f"python tools/challenge.py --candidate {cand} --oracle {oracle_path}",
            })

    # pins
    pack_manifest = pack / "05_W0_SOURCE_MANIFEST.json"
    pack_ok = all(lib.sha_file(pack / e["path"]) == e["sha256"] for e in
                  lib.load_json(pack_manifest)["pack_files"])
    check("PACK-PINS", pack_ok and (a.mode == "smoke" or lib.sha_file(pack_manifest) == summary.get("pack_manifest_sha256")),
          {"pack_ok": pack_ok})

    head = subprocess.run(["git", "-C", str(cand), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    check("CANDIDATE-PIN", head == oracle["candidate_commit"] and (a.mode == "smoke" or head == summary.get("candidate_sha")),
          {"head": head, "summary": summary.get("candidate_sha")}, cls="candidate_changed")
    check("ORACLE-PIN", a.mode == "smoke" or (
              lib.sha_file(oracle_path) == summary.get("oracle_sha")
              and bool(oracle.get("frozen_at"))
              and oracle.get("candidate_commit") == head),
          {"oracle_sha": lib.sha_file(oracle_path)}, cls="oracle_drift")
    for name, expected in oracle["fixtures"].items():
        p = cand / "fixtures" / name
        check("FIX-" + name, p.is_file() and lib.sha_file(p) == expected,
              {"file": name, "sha": lib.sha_file(p) if p.is_file() else None})

    # receipts complete and consistent
    rec_files = sorted(receipt_dir.glob("*.json")) if a.mode == "full" else []
    if a.mode == "full":
        check("RECEIPT-COUNT", len(rec_files) == 44, {"count": len(rec_files)})
    bad = []
    for p in rec_files:
        rec = json.loads(p.read_text(encoding="utf-8"))
        missing = [k for k in REQUIRED_RECEIPT if rec.get(k) in (None, "", [], {})]
        if missing or rec.get("expected") == rec.get("observed"):
            bad.append({"file": p.name, "missing": missing, "same": rec.get("expected") == rec.get("observed")})
    if a.mode == "full":
        check("RECEIPT-FIELDS", not bad, {"bad": bad[:5], "total": len(rec_files)})
    failing = []
    for p in rec_files:
        r = json.loads(p.read_text(encoding="utf-8"))
        if r.get("case_id") == "NF-T10" and r.get("verdict") in ("PASS", "PENDING_CONSUMER"):
            continue
        if r.get("verdict") != "PASS":
            failing.append(r.get("case_id"))
    if a.mode == "full":
        check("RECEIPT-VERDICTS", not failing, {"failing": failing})
        rec_index = lib.canonical_sha({p.name: lib.sha_file(p) for p in rec_files
                                       if p.name != "NF-T10.json"})
        case_set = lib.canonical_sha({"sample": tqaep_spec.SAMPLE, "cases": tqaep_spec.CASES})
        check("PIN-RECOMPUTE",
              rec_index == summary.get("receipts_index_sha") and case_set == summary.get("case_set_sha"),
              {"receipts_index": rec_index, "case_set": case_set})

    # independent re-execution in a separate worktree
    wt = work / "checker-wt"
    if wt.exists():
        shutil.rmtree(wt, ignore_errors=True)
    shutil.copytree(cand, wt, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    suite = lib.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], wt,
                    env_extra={"PYTHONPATH": str(wt)}, raw_dir=work / "raw", tag="challenge_suite")
    check("SUITE", suite["exit"] == 0, {"exit": suite["exit"], "sha": suite["stdout_sha256"]})

    # mutation self-test: a deliberately broken candidate must be caught
    mut = work / "mutant"
    if mut.exists():
        shutil.rmtree(mut)
    shutil.copytree(wt, mut)
    (mut / "briefcheck.py").write_text(
        "import json,sys\n"
        "print(json.dumps({'source_sha256':'0'*64,'provided':['A','B'],'missing':[],"
        "'status':'COMPLETE'}))\nsys.exit(0)\n",
        encoding="utf-8",
    )
    mroot = work / "mut_root"
    if mroot.exists():
        shutil.rmtree(mroot)
    mroot.mkdir(parents=True)
    for p in (wt / "fixtures").glob("*.md"):
        shutil.copy2(p, mroot / p.name)
    mr = lib.run([sys.executable, "-m", "briefcheck", "--root", str(mroot),
                  "--input", "case_dup.md", "--sha256", lib.sha_file(mroot / "case_dup.md")],
                 mroot, 30, {"PYTHONPATH": str(mut)}, work / "raw", "challenge_mutant")
    mutant_status = (json.loads(mr["stdout"]).get("status") if mr["stdout"].strip() else None)
    check("MUTANT-DETECTABLE", mr["exit"] != 3 and mutant_status != "INVALID_DUP",
          {"mutant_exit": mr["exit"], "expected_for_good_candidate": 3,
           "note": "a fail-open mutant must not match the oracle"})

    root = work / "root"
    outside = work / "outside"
    for d in (root, outside):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    for p in (wt / "fixtures").glob("*.md"):
        shutil.copy2(p, root / p.name)
    (outside / "canary.md").write_text("OUTSIDE_CANARY_DO_NOT_READ\n", encoding="utf-8")
    subprocess.run(["cmd", "/c", "mklink", "/J", str(root / "escape_dir"), str(outside)],
                   capture_output=True)

    def run(args, tag):
        env = {"PYTHONPATH": str(wt)}
        return lib.run([sys.executable, "-m", "briefcheck", *args], root, 30, env,
                       work / "raw", tag)

    expect = {"case_ok.md": (0, "COMPLETE"), "case_missing.md": (2, "MISSING"),
              "case_dup.md": (3, "INVALID_DUP"), "case_ambiguous.md": (3, "INVALID_FORMAT"),
              "case_malformed.md": (3, "INVALID_FORMAT"), "case_bad_utf8.md": (3, "INVALID_ENCODING")}
    for name, (code, status) in expect.items():
        r = run(["--root", str(root), "--input", name,
                 "--sha256", lib.sha_file(root / name)], "ch_" + name)
        payload = json.loads(r["stdout"]) if r["stdout"].strip() else {}
        check("CASE-" + name, r["exit"] == code and payload.get("status") == status,
              {"exit": r["exit"], "status": payload.get("status")})
    bad_sha = run(["--root", str(root), "--input", "case_ok.md", "--sha256", "0" * 64], "ch_sha")
    check("SHA-MISMATCH", bad_sha["exit"] == 3 and json.loads(bad_sha["stdout"])["status"] == "SHA_MISMATCH",
          {"exit": bad_sha["exit"]})

    for tag, rel in (("dd", "../outside/canary.md"), ("abs", str(outside / "canary.md")),
                     ("unc", r"\\localhost\share\canary.md"), ("jct", "escape_dir/canary.md")):
        r = run(["--root", str(root), "--input", rel, "--sha256", lib.sha_file(outside / "canary.md")], "ch_path_" + tag)
        payload = json.loads(r["stdout"]) if r["stdout"].strip() else {}
        check("PATH-" + tag, r["exit"] == 3 and payload.get("status") == "INVALID_PATH"
              and "OUTSIDE_CANARY" not in (r["stdout"] + r["stderr"]), {"exit": r["exit"]})
    sym_ok = False
    try:
        os.symlink(outside / "canary.md", root / "escape_link")
        sym_ok = True
        r = run(["--root", str(root), "--input", "escape_link", "--sha256", lib.sha_file(outside / "canary.md")],
                "ch_path_sym")
        check("PATH-symlink", r["exit"] == 3 and json.loads(r["stdout"])["status"] == "INVALID_PATH",
              {"exit": r["exit"]})
    except OSError:
        not_verified.append({"id": "PATH-symlink", "reason": "symlink privilege"})

    # no-write to subject/oracle (snapshot taken before the first check)
    oracle_before = lib.sha_file(oracle_path)
    after = lib.snapshot(cand)
    check("NO-WRITE", subject_before == after and oracle_before == lib.sha_file(oracle_path),
          {"candidate_changed": subject_before != after,
           "oracle_changed": oracle_before != lib.sha_file(oracle_path)})
    check("NO-GIT-WRITE", subject_git_before == git_meta(),
          {"before": subject_git_before, "after": git_meta()})

    # negative policy re-checks
    if a.mode == "full":
        stale = policy.delta_eval(
            {"source": "s", "candidate": "c1", "fixture": "f", "oracle": "o", "first_fail": "x", "raw_sha": "1"},
            {"source": "s", "candidate": "c2", "fixture": "f", "oracle": "o", "first_fail": "x", "raw_sha": "1"})
        check("STALE-RAW", stale["status"] == "REQUALIFY", stale)
        rel = policy.release_gate(None, None)
        check("RELEASE-GATE", rel["release"] == "RELEASE_NOT_CLAIMED", rel)
        secrets = []
        for p in rec_files:
            text = p.read_text(encoding="utf-8")
            if policy.secret_scan(text)["status"] == "SECRET_LEAK":
                secrets.append(p.name)
        check("SECRET-SCAN", not secrets, {"files": secrets})

    pins = {
        "source": oracle["source_sha256"],
        "candidate": head,
        "evidence": lib.canonical_sha({p.name: lib.sha_file(p) for p in rec_files
                                       if p.name != "NF-T10.json"}) if a.mode == "full" else None,
        "oracle": lib.sha_file(oracle_path),
        "case_set": lib.canonical_sha({"sample": tqaep_spec.SAMPLE, "cases": tqaep_spec.CASES}),
    }
    verdict = "PASS" if all(c["ok"] for c in checks) and not findings else "FAIL"
    result = {
        "schema": "FHS5.W0NF.Challenge@2" if a.mode == "full" else "FHS5.W0NF.ChallengeSmoke@1",
        "mode": a.mode,
        "claim_ceiling": "CHECKER_ROLE_SEPARATED_SAME_PRINCIPAL",
        "checker_identity": ("tools/challenge.py in a separate process over an isolated copy; "
                             "subject files and git metadata checked (NO-WRITE / NO-GIT-WRITE); "
                             "same OS principal"),
        "candidate": str(cand),
        "worktree": str(wt),
        "pins": pins,
        "checks": checks,
        "findings": findings,
        "not_verified": not_verified,
        "verdict": verdict,
        "symlink_tested": sym_ok,
        "not_covered": ["full C16/EC-36/local47", "different-principal independence",
                        "HERMES/GPT host execution", "release"]
                       + ([] if sym_ok else ["symlink creation (OS privilege); junction tested"]),
    }
    lib.write_json(Path(a.out), result)
    print(json.dumps({"verdict": verdict, "checks": len(checks), "findings": len(findings),
                      "failed": [c["id"] for c in checks if not c["ok"]], "pins": pins},
                     ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
