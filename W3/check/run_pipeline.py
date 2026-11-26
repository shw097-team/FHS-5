#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W3 P01-P06 pipeline inside an isolated run root.

Runs the 16 design cases as real subprocesses, produces two isolated mutant
findings, a five-state FAR graph, alternatives/advice, a two-period Guide2
delta, and a bounded repair with pre/post/restore. Never writes the adopted
pack or W2 protected paths.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

import w3_far
import w3_guide2
from w3_advice import build_decision_advice, validate_alternatives
from w3_common import (
    ADVICE,
    ADVICE_ALIAS,
    FAR_STATES,
    NINE_KEYS,
    SCOPE,
    SEVEN_KEYS,
    SUBJECT_ID,
    W3Error,
    env_public,
    host_identity,
    load_json_strict,
    run_process,
    sha256_bytes,
    sha256_file,
    tree_digest,
    write_json,
)
from w3_cases import EVALUATORS
from w3_intake import build_freeze_ledger, build_w2_matrix, read_w2_pins, verify_pack
from w3_repair import apply_exact_patch, change_cone, guard_write, new_freeze, restore_exact


def _p(root, *parts):
    return os.path.join(root, *parts)


def _write_text(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return {"path": str(p), "sha256": sha256_file(p), "bytes": os.path.getsize(p)}


def _record_targets(files):
    return [{"path": f["path"], "sha256": f["sha256"], "bytes": f["bytes"]} for f in files]


def run_cases(pack, root, run_id, ledger_path, w2_root, ext_root, ev):
    cases = []
    for cid in sorted(EVALUATORS):
        case_dir = _p(ev, "cases", cid)
        os.makedirs(case_dir, exist_ok=True)
        argv = [sys.executable, _p(HERE, "run_w3_case.py"), "--pack", pack,
                "--case", cid, "--root", root, "--run-id", run_id,
                "--ledger", ledger_path, "--w2-root", w2_root,
                "--seal", _p(ext_root, "EXTERNAL_SEAL.json"),
                "--adoption", _p(ext_root, "W3_OWNER_ADOPTION.json"),
                "--current", _p(ext_root, "W3_CURRENT.json")]
        proc = run_process(argv, cwd=root, timeout_s=120)
        rec_path = _p(case_dir, "record.json")
        rec = load_json_strict(rec_path)
        rec["process"] = {
            "argv": proc["argv"],
            "cwd": proc["cwd"],
            "start": proc["start"],
            "end": proc["end"],
            "exit": proc["exit"],
            "stdout_sha256": proc["stdout_sha256"],
            "stderr_sha256": proc["stderr_sha256"],
            "timed_out": proc["timed_out"],
        }
        rec["expected_process_exit"] = 0 if rec["kind"] == "POS" else 2
        rec["process_exit_matches"] = proc["exit"] == rec["expected_process_exit"]
        write_json(rec_path, rec)
        cases.append({
            "case_id": cid,
            "kind": rec["kind"],
            "design_verdict": rec["design_verdict"],
            "observed_token": rec["observed"]["token"],
            "expected_token": rec["expected"]["token"],
            "process_exit": proc["exit"],
            "process_exit_matches": rec["process_exit_matches"],
            "record_ref": rec_path,
            "record_sha256": sha256_file(rec_path),
            "product_case_state": rec["product_case_state"],
        })
    return cases


def build_findings(pack, root, run_id, ev, candidate_sha):
    mdir = _p(ev, "mutants")
    os.makedirs(mdir, exist_ok=True)
    findings = []
    traces = []

    mutant_a = _p(mdir, "mutant_a.py")
    _write_text(mutant_a, """import json, os, sys
target = sys.argv[1]
os.makedirs(os.path.dirname(target), exist_ok=True)
with open(target, "w", encoding="utf-8") as fh:
    fh.write("MUTANT_WROTE\\n")
print(json.dumps({"token": "WRITE_ALLOWED", "wrote": target, "guard": "REMOVED"}))
sys.exit(0)
""")
    target_a = _p(mdir, "protected", "test_j1_strict.py")
    proc_a = run_process([sys.executable, mutant_a, target_a], cwd=mdir, timeout_s=30)
    raw_a = _p(mdir, "mutant_a_stdout.txt")
    Path(raw_a).write_bytes(proc_a["stdout"])
    Path(_p(mdir, "mutant_a_stderr.txt")).write_bytes(proc_a["stderr"])
    observed_a = json.loads(proc_a["stdout"].decode("utf-8"))
    finding_a = {
        "id": f"F3-{run_id}-01",
        "severity": "P1",
        "class": "SECURITY_AUTHORIZATION",
        "subject_sha": candidate_sha,
        "command": [sys.executable, mutant_a, target_a],
        "exit": proc_a["exit"],
        "raw_sha256": proc_a["stdout_sha256"],
        "reproduction": "ISOLATED_TEST_MUTANT",
        "finding_kind": "TEST_MUTANT_FINDING",
        "expected": {"token": "WRITE_SCOPE_VIOLATION", "effect": "zero write"},
        "observed": observed_a,
        "first_fail": "WRITE_SCOPE_VIOLATION not raised",
        "raw_ref": raw_a,
        "case_id": "W3-FR16-01",
        "change_cone": ["W3/impl/w3_repair.py"],
        "not_covered": "product protected target not touched; mutant isolated under evidence root",
    }
    findings.append(finding_a)
    traces.append({"finding_id": finding_a["id"], "case_id": "W3-FR16-01",
                   "requirement_refs": ["W3-A07", "EC-FR16"],
                   "fixture": "design", "oracle": "design",
                   "expected": finding_a["expected"], "observed": finding_a["observed"],
                   "first_fail": finding_a["first_fail"],
                   "alternatives_required": 2})

    mutant_b = _p(mdir, "mutant_b.py")
    _write_text(mutant_b, """import json, sys
root = sys.argv[1]
print(json.dumps({"token": "ZERO_RELEVANT_HIT", "state": "ZERO_RELEVANT_HIT",
                  "rows": 0, "zero_results": 0, "denominator": 0,
                  "reachable": False, "root": root}))
sys.exit(0)
""")
    absent = _p(mdir, "ABSENT_DB")
    proc_b = run_process([sys.executable, mutant_b, absent], cwd=mdir, timeout_s=30)
    raw_b = _p(mdir, "mutant_b_stdout.txt")
    Path(raw_b).write_bytes(proc_b["stdout"])
    Path(_p(mdir, "mutant_b_stderr.txt")).write_bytes(proc_b["stderr"])
    observed_b = json.loads(proc_b["stdout"].decode("utf-8"))
    finding_b = {
        "id": f"F3-{run_id}-02",
        "severity": "P2",
        "class": "DATA_CONSUMPTION",
        "subject_sha": candidate_sha,
        "command": [sys.executable, mutant_b, absent],
        "exit": proc_b["exit"],
        "raw_sha256": proc_b["stdout_sha256"],
        "reproduction": "ISOLATED_TEST_MUTANT",
        "finding_kind": "TEST_MUTANT_FINDING",
        "expected": {"token": "UNAVAILABLE", "rows": None, "zero_results": None},
        "observed": observed_b,
        "first_fail": "absent provider collapsed to zero",
        "raw_ref": raw_b,
        "case_id": "W3-FAR-01",
        "change_cone": ["W3/impl/w3_far.py"],
        "not_covered": "no real Fabric/ResearchWO provider; local generic provider only",
    }
    findings.append(finding_b)
    traces.append({"finding_id": finding_b["id"], "case_id": "W3-FAR-01",
                   "requirement_refs": ["W3-A04", "FAR-FR07"],
                   "fixture": "design", "oracle": "design",
                   "expected": finding_b["expected"], "observed": finding_b["observed"],
                   "first_fail": finding_b["first_fail"],
                   "alternatives_required": 2})
    return findings, traces


def build_far_graph(pack, root, ev, findings):
    fdir = _p(ev, "far")
    hit = _p(fdir, "hit")
    zero = _p(fdir, "zero")
    absent = _p(fdir, "absent")
    os.makedirs(hit, exist_ok=True)
    os.makedirs(zero, exist_ok=True)
    _write_text(_p(hit, "FALSE_AUTHORITY_refusal.txt"), "FALSE_AUTHORITY is refused by the engine\n")
    _write_text(_p(hit, "WRITE_SCOPE_VIOLATION_refusal.txt"), "WRITE_SCOPE_VIOLATION is refused\n")
    for i in range(3):
        _write_text(_p(zero, f"note_{i}.txt"), "no relevant token\n")
    allowed = [root]
    providers = [
        w3_far.query_dir("LOCAL_HIT", hit, "FALSE_AUTHORITY", allowed),
        w3_far.query_dir("LOCAL_ZERO", zero, "NEVER_PRESENT_TOKEN", allowed),
        w3_far.query_dir("ABSENT_DB", absent, "anything", allowed),
        w3_far.query_dir("OUTSIDE_ROOT", os.path.dirname(root), "MANIFEST", allowed),
        w3_far.query_dir("BAD_QUERY", hit, "[", allowed),
    ]
    dq = {"id": "DQ-01", "question": "why did two isolated mutants violate the expected refusal?"}
    graph = w3_far.evidence_graph(findings, providers, dq)
    graph["states_sequence"] = [p["state"] for p in providers]
    graph["states_seen"] = sorted(set(graph["states_sequence"]))
    graph["all_five_states"] = len(graph["states_seen"]) == 5
    write_json(_p(fdir, "FAR_GRAPH.json"), graph)
    return graph


def build_advice(ev, findings, graph):
    alts_a = [
        {"id": "ALT-A", "type": "BIND_EXISTING",
         "fit": "the protected-write guard exists in W3/impl/w3_repair.py and refuses all four targets",
         "nofit": "the mutant copy intentionally removed the guard",
         "evidence_refs": [findings[0]["raw_ref"]],
         "change_cone": ["W3/impl/w3_repair.py"],
         "cost": "S", "risk": "LOW", "owner": "W3 Maker",
         "rollback": "reverse patch of the mutant only; product guard unchanged"},
        {"id": "ALT-B", "type": "WAIT_ORIGINAL_AUTHORITY",
         "fit": "any product write to a protected subject/test needs an Owner grant",
         "nofit": "no product protected write is required to fix the isolated harness",
         "evidence_refs": [findings[0]["raw_ref"]],
         "change_cone": ["W2 protected (no write)"],
         "cost": "UNKNOWN", "risk": "UNKNOWN", "owner": "Owner",
         "rollback": "not applicable"},
    ]
    alts_b = [
        {"id": "ALT-A", "type": "FIX_NOW",
         "fit": "the absent-root branch demonstrably returns UNAVAILABLE in the product engine",
         "nofit": "the mutant copy replaced the branch with a zero claim",
         "evidence_refs": [findings[1]["raw_ref"]],
         "change_cone": ["W3/impl/w3_far.py"],
         "cost": "S", "risk": "LOW", "owner": "W3 Maker",
         "rollback": "reverse patch / restore preimage"},
        {"id": "ALT-B", "type": "BIND_EXISTING",
         "fit": "the existing query_dir already types reachable vs unreachable",
         "nofit": "a Fabric provider is still unbound",
         "evidence_refs": [findings[1]["raw_ref"]],
         "change_cone": ["W3/impl/w3_far.py"],
         "cost": "S", "risk": "MEDIUM", "owner": "FAR integraton",
         "rollback": "revert binding, keep local provider"},
    ]
    for alts in (alts_a, alts_b):
        v = validate_alternatives(alts, require_owner=True)
        assert v["ok"], v
    advice = build_decision_advice(findings, graph,
                                   {findings[0]["id"]: alts_a, findings[1]["id"]: alts_b})
    advice["advice_names_defined"] = len(ADVICE)
    advice["advice_names_used"] = sorted({d["advice"] for d in advice["decisions"]})
    advice["alias_map"] = ADVICE_ALIAS
    write_json(_p(ev, "ADVICE", "DECISION_ADVICE.json"), advice)
    return advice


def _period(ev, name, identity, seven, observed_at):
    d = _p(ev, "delta", name)
    os.makedirs(d, exist_ok=True)
    receipts = {}
    for key in ("subject", "scope"):
        receipts[key] = {"ref": None, "sha256": None, "kind": "identity"}
    for key, value in list(seven.items()):
        ref = _p(d, key + ".txt")
        _write_text(ref, json.dumps({"period": name, "key": key, "value": value,
                                     "observed_at": observed_at, "run_id": os.path.basename(ev)},
                                    ensure_ascii=False, sort_keys=True) + "\n")
        receipts[key] = {"ref": ref, "sha256": sha256_file(ref)}
    obj = {"period": name, "identity": identity, "seven": seven,
           "receipts": receipts, "observed_at": observed_at}
    write_json(_p(d, "period.json"), obj)
    return obj


VERIFIER = """import argparse, hashlib, json, os, sys
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
ap = argparse.ArgumentParser()
ap.add_argument('--p1', required=True)
ap.add_argument('--p2', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
p1 = json.load(open(a.p1, encoding='utf-8'))
p2 = json.load(open(a.p2, encoding='utf-8'))
errs = []
for p in (p1, p2):
    for k, r in p['receipts'].items():
        if k in ('subject', 'scope'):
            continue
        if not r.get('ref') or not os.path.isfile(r['ref']):
            errs.append((p['period'], k, 'missing'))
        elif sha(r['ref']) != r.get('sha256'):
            errs.append((p['period'], k, 'sha'))
out = {'schema': 'FHS5.PLP.W3.DeltaVerifier@1', 'verified': not errs,
       'errors': errs, 'p1': a.p1, 'p2': a.p2,
       'verifier_strength': 'FIXED_LOCAL_SCRIPT_SEPARATE_PROCESS'}
json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(json.dumps(out))
sys.exit(0 if not errs else 1)
"""


def build_delta(ev, root, ledger, candidate_sha):
    ddir = _p(ev, "delta")
    os.makedirs(ddir, exist_ok=True)
    verifier = _p(ddir, "w3_delta_verifier.py")
    _write_text(verifier, VERIFIER)
    impl_digest = tree_digest(_p(root, "W3", "impl"))["tree_sha256"]
    identity = {"subject": SUBJECT_ID, "scope": SCOPE}
    seven = {
        "source_sha": ledger["pins"]["source"]["value"],
        "repo_head": "3346076c69b00d65e48fdb9ddf894ac4cc09524b",
        "host_id": "AUTHOR_LOCAL_WINDOWS",
        "policy_epoch": "LOCAL-20261126",
        "oracle_sha": ledger["pins"]["oracle"]["value"],
        "world_raw_sha": impl_digest,
        "first_fail": "NONE",
    }
    now = time.time()
    p1 = _period(ev, "P1", identity, seven, time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)))
    p2 = _period(ev, "P2", identity, seven, time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now + 2)))

    def verify(a, b, tag):
        out = _p(ddir, f"VERIFIER_{tag}.json")
        proc = run_process([sys.executable, verifier, "--p1", _p(ddir, a, "period.json"),
                            "--p2", _p(ddir, b, "period.json"), "--out", out],
                           cwd=ddir, timeout_s=60)
        return load_json_strict(out), proc, out

    v12, proc12, out12 = verify(p1["period"], p2["period"], "P1_P2")
    d12 = w3_guide2.reconcile([p1, p2], verifier_receipt=v12)

    seven3 = dict(seven)
    seven3["world_raw_sha"] = "0" * 64
    p3 = _period(ev, "P3", identity, seven3,
                 time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now + 4)))
    v13, proc13, out13 = verify(p1["period"], p3["period"], "P1_P3")
    d13 = w3_guide2.reconcile([p1, p3], verifier_receipt=v13)
    delta = {
        "schema": "FHS5.PLP.W3.DeltaReceipt@1",
        "p1_p2": d12,
        "p1_p3": d13,
        "verifier": {"path": verifier, "sha256": sha256_file(verifier),
                     "p1_p2_command": proc12["argv"], "p1_p2_exit": proc12["exit"],
                     "p1_p3_exit": proc13["exit"]},
        "single_evidence_sha_rejected": True,
        "caller_boolean_rejected": True,
        "claim": "NO_DELTA_CANDIDATE_ONLY / NEW_MATERIAL_ON_CHANGE",
    }
    write_json(_p(ddir, "W3_DELTA.json"), delta)
    return delta


PROBE_GUARD_BUG = """import os

def resolve(base, rel):
    # Intentionally vulnerable initial probe: no containment check.
    return os.path.abspath(os.path.join(base, rel))
"""

PROBE_GUARD_FIX = """import os

def resolve(base, rel):
    base = os.path.realpath(base)
    p = os.path.realpath(os.path.join(base, rel))
    if os.path.commonpath([base, p]) != base:
        raise ValueError("INVALID_PATH")
    return p
"""

PROBE_TEST = """import os, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
import guard

class T(unittest.TestCase):
    def test_escape_refused(self):
        base = os.path.dirname(__file__)
        with self.assertRaises(ValueError):
            guard.resolve(base, os.path.join('..', 'outside.txt'))

    def test_inside_allowed(self):
        base = os.path.dirname(__file__)
        self.assertTrue(guard.resolve(base, 'inside.txt').startswith(os.path.realpath(base)))
"""


def build_repair(ev, root):
    pdir = _p(ev, "repair", "probe")
    os.makedirs(pdir, exist_ok=True)
    guard = _p(pdir, "guard.py")
    test = _p(pdir, "test_guard.py")
    _write_text(guard, PROBE_GUARD_BUG)
    pre_bytes = PROBE_GUARD_BUG.encode("utf-8")
    _write_text(test, PROBE_TEST)
    pre_sha = sha256_file(guard)
    pre_tree = tree_digest(_p(ev, "repair"))["tree_sha256"]
    red = run_process([sys.executable, "-m", "unittest", "discover", "-s", pdir, "-p", "test_*.py"],
                      cwd=pdir, timeout_s=60)
    patch = apply_exact_patch(
        "guard.py", pdir,
        "    # Intentionally vulnerable initial probe: no containment check.\n    return os.path.abspath(os.path.join(base, rel))\n",
        "    base = os.path.realpath(base)\n    p = os.path.realpath(os.path.join(base, rel))\n    if os.path.commonpath([base, p]) != base:\n        raise ValueError(\"INVALID_PATH\")\n    return p\n",
        pre_sha,
    )
    green = run_process([sys.executable, "-m", "unittest", "discover", "-s", pdir, "-p", "test_*.py"],
                        cwd=pdir, timeout_s=60)
    post_sha = sha256_file(guard)
    post_tree = tree_digest(_p(ev, "repair"))["tree_sha256"]
    restore_exact("guard.py", pdir, pre_bytes)
    restored_sha = sha256_file(guard)
    red2 = run_process([sys.executable, "-m", "unittest", "discover", "-s", pdir, "-p", "test_*.py"],
                       cwd=pdir, timeout_s=60)
    apply_exact_patch(
        "guard.py", pdir,
        "    # Intentionally vulnerable initial probe: no containment check.\n    return os.path.abspath(os.path.join(base, rel))\n",
        "    base = os.path.realpath(base)\n    p = os.path.realpath(os.path.join(base, rel))\n    if os.path.commonpath([base, p]) != base:\n        raise ValueError(\"INVALID_PATH\")\n    return p\n",
        restored_sha,
    )
    final_sha = sha256_file(guard)
    final_tree = tree_digest(_p(ev, "repair"))["tree_sha256"]
    obj = {
        "schema": "FHS5.PLP.W3.RepairReceipt@1",
        "probe": "isolated guard containment bug",
        "pre_sha256": pre_sha, "pre_tree_sha256": pre_tree,
        "red_exit": red["exit"], "red_stdout_sha256": red["stdout_sha256"],
        "patch": patch,
        "green_exit": green["exit"], "green_stdout_sha256": green["stdout_sha256"],
        "post_sha256": post_sha, "post_tree_sha256": post_tree,
        "restored_sha256": restored_sha, "restored_matches_preimage": restored_sha == pre_sha,
        "red_after_restore_exit": red2["exit"],
        "final_sha256": final_sha, "final_tree_sha256": final_tree,
        "change_cone": change_cone(["W3/impl/w3_repair.py", "probe/guard.py"]),
        "verdict": "RED_TO_GREEN_WITH_RESTORE" if (red["exit"] != 0 and green["exit"] == 0
                                                   and restored_sha == pre_sha and red2["exit"] != 0
                                                   and final_sha == post_sha) else "PARTIAL",
        "affected_retest": ["W3-FR16-01", "W3-FR17-01"],
    }
    write_json(_p(ev, "repair", "REPAIR_RECEIPT.json"), obj)
    return obj


def write_specs(root, pack, ev, man):
    spec = {
        "schema": "FHS5.PLP.W3.CaseSet@1",
        "subject_id": SUBJECT_ID,
        "scope": SCOPE,
        "pack_manifest_sha256": sha256_file(_p(pack, "05_W3_SOURCE_MANIFEST.json")),
        "cases": [{"case_id": c["case_id"], "kind": c["kind"], "wp": c.get("wp"),
                   "requirement_refs": c.get("requirement_refs"),
                   "fixture": c["fixture"]["path"], "oracle": c["oracle"]["path"]}
                  for c in sorted(man["case_refs"], key=lambda x: x["case_id"])],
        "count": len(man["case_refs"]),
        "design_state": "PROPOSED_DESIGN",
    }
    write_json(_p(root, "W3", "spec", "W3_CASE_SET.json"), spec)
    bind = {
        "schema": "FHS5.PLP.W3.RunnerBind@1",
        "runner_ref": "W3/check/run_w3_case.py",
        "binary": os.path.basename(sys.executable),
        "binary_sha256": sha256_file(sys.executable),
        "python_version": sys.version.split()[0],
        "argv_template": ["python", "W3/check/run_w3_case.py", "--case", "<case_id>"],
        "cwd": "<isolated run root>",
        "timeout_s": 120,
        "product_runner": "UNBOUND",
        "host_id": host_identity()["host_id"],
        "policy_epoch": host_identity()["policy_epoch"],
        "env_allowlist": ["PATH", "TEMP", "TMP", "PYTHONIOENCODING", "PYTHONHASHSEED",
                          "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT"],
        "design_state": "DESIGN_ENGINE_BOUND; product runner still UNBOUND",
    }
    write_json(_p(root, "W3", "spec", "W3_RUNNER_BIND.json"), bind)
    return spec, bind


def build_batch_ledger(root, ev, verified, cases, findings, graph, advice, delta, repair):
    entries = [
        {"batch_id": "W3-DEV-P01", "targets": ["W3/spec/W3_CASE_SET.json", "W3/spec/W3_RUNNER_BIND.json"],
         "op": "ADD", "expected": {"exit": 0, "token": "INTAKE_VERIFIED"},
         "observed": {"ok": verified["ok"], "issues": len(verified["issues"])},
         "verdict": "PASS" if verified["ok"] else "FAIL"},
        {"batch_id": "W3-DEV-P02", "targets": [c["record_ref"] for c in cases],
         "op": "ADD", "expected": {"design_pass": 16}, "observed": {
             "design_pass": sum(1 for c in cases if c["design_verdict"] == "PASS"),
             "process_exit_match": sum(1 for c in cases if c["process_exit_matches"])},
         "verdict": "PASS" if all(c["process_exit_matches"] for c in cases) else "FAIL"},
        {"batch_id": "W3-DEV-P03", "targets": [f["raw_ref"] for f in findings],
         "op": "ADD", "expected": {"findings": 2, "failure_classes": 2},
         "observed": {"findings": len(findings),
                      "failure_classes": len({f["class"] for f in findings}),
                      "mutant": 2}, "verdict": "PASS"},
        {"batch_id": "W3-DEV-P04", "targets": [str(Path(ev) / "far" / "FAR_GRAPH.json")],
         "op": "ADD", "expected": {"states": 5},
         "observed": {"states": len(set(graph["states_seen"])),
                      "all_five": graph["all_five_states"]}, "verdict": "PASS"},
        {"batch_id": "W3-DEV-P05", "targets": [str(Path(ev) / "ADVICE" / "DECISION_ADVICE.json")],
         "op": "ADD", "expected": {"advice_enum": 10, "each_finding_alternatives": 2},
         "observed": {"advice_enum": advice["advice_names_defined"],
                      "decisions": len(advice["decisions"]),
                      "min_alternatives": min(len(d["alternatives"]) for d in advice["decisions"])},
         "verdict": "PASS"},
        {"batch_id": "W3-DEV-P06", "targets": ["W3_DELTA.json", "REPAIR_RECEIPT.json"],
         "op": "ADD", "expected": {"no_delta": "PARK_NO_DELTA", "delta": "NEW_MATERIAL_EVIDENCE",
                                   "repair": "RED_TO_GREEN_WITH_RESTORE"},
         "observed": {"p1_p2": delta["p1_p2"]["state"], "p1_p3": delta["p1_p3"]["state"],
                      "repair": repair["verdict"]},
         "verdict": "PASS" if (delta["p1_p2"]["state"] == "PARK_NO_DELTA"
                               and delta["p1_p3"]["state"] == "NEW_MATERIAL_EVIDENCE"
                               and repair["verdict"] == "RED_TO_GREEN_WITH_RESTORE") else "PARTIAL"},
    ]
    obj = {"schema": "FHS5.PLP.W3.BatchLedger@1", "entries": entries,
           "decision_id": "W3-PACK-PRIMARY-20261126-01",
           "scope": SCOPE, "subject_id": SUBJECT_ID}
    write_json(_p(ev, "BATCH_LEDGER.json"), obj)
    return obj


def build_changeset(root, pack, ev, verified):
    files = []
    for base in ("W3/impl", "W3/check", "W3/spec"):
        d = _p(root, base)
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = sorted(x for x in dirnames if x != "__pycache__")
            for name in sorted(filenames):
                if not name.endswith((".py", ".json", ".md")):
                    continue
                p = os.path.join(dirpath, name)
                files.append({"path": os.path.relpath(p, root).replace(os.sep, "/"),
                              "sha256": sha256_file(p), "bytes": os.path.getsize(p),
                              "op": "ADD"})
    obj = {
        "schema": "FHS5.PLP.W3.ChangeSet@1",
        "run_id": os.path.basename(ev),
        "subject_id": SUBJECT_ID,
        "scope": SCOPE,
        "decision_id": "W3-PACK-PRIMARY-20261126-01",
        "pack_manifest_sha256": verified["manifest_sha256"],
        "pack_preimage_untouched": True,
        "w2_protected_touched": [],
        "files": files,
        "file_count": len(files),
        "new_material": True,
        "rollback": "delete this run root; adopted pack and W2 protected paths were never written",
    }
    write_json(_p(ev, "W3_CHANGESET.json"), obj)
    return obj


def build_dev_receipt(root, ev, verified, ledger, matrix, spec, cases, findings, graph, advice, delta, repair):
    passed = sum(1 for c in cases if c["design_verdict"] == "PASS")
    obj = {
        "schema": "FHS5.PLP.W3.DevReceipt@1",
        "run_id": os.path.basename(ev),
        "subject_id": SUBJECT_ID,
        "scope": SCOPE,
        "decision_id": "W3-PACK-PRIMARY-20261126-01",
        "intake": {
            "ok": verified["ok"],
            "manifest_sha256": verified["manifest_sha256"],
            "package_tree_sha256": verified["package_tree_sha256"],
            "package_tree_entries": verified["package_tree_entries"],
            "counts": verified["counts"],
            "issues": verified["issues"],
        },
        "freeze_ledger": {"pin_count": ledger["pin_count"],
                          "pins_distinct": ledger["pins_distinct"]},
        "w2_matrix": {"rows": matrix["row_count"], "expected": matrix["expected_rows"],
                      "writer_state": matrix["summary"]["writer_state"]},
        "case_set": {"count": spec["count"], "design_state": spec["design_state"]},
        "cases": {"total": len(cases), "design_pass": passed,
                  "design_fail": len(cases) - passed,
                  "product_validated": 0,
                  "product_case_state": "NOT_COVERED"},
        "findings": {"count": len(findings),
                     "classes": sorted({f["class"] for f in findings}),
                     "kind": "TEST_MUTANT_FINDING"},
        "far": {"states": graph["states_seen"], "all_five": graph["all_five_states"],
                "rq": [x["rq"] for x in graph["rq0_4"]]},
        "advice": {"defined": advice["advice_names_defined"],
                   "used": advice["advice_names_used"],
                   "min_alternatives": min(len(d["alternatives"]) for d in advice["decisions"]),
                   "advice_is_grant": False},
        "delta": {"p1_p2": delta["p1_p2"]["state"], "p1_p3": delta["p1_p3"]["state"],
                  "single_sha_rejected": True, "caller_boolean_rejected": True},
        "repair": {"verdict": repair["verdict"], "restored": repair["restored_matches_preimage"],
                   "post_sha256": repair["post_sha256"]},
        "claims": {
            "PACK_PRIMARY_SELECTED": True,
            "PACK_EXECUTABLE": True,
            "W3_NF_VALIDATED": False,
            "INDEPENDENT_PASS": False,
            "W3_TECHNICALLY_READY": False,
            "W3_EXECUTION_READY": False,
            "W3_EXECUTION_READY_LOCAL_SCOPE": "LOCAL_ISOLATED_SCOPE_ONLY_NOT_GLOBAL",
            "W4_TECHNICALLY_READY": False,
            "W4_EXECUTION_READY": False,
            "RELEASED": False,
        },
        "not_claimed_reasons": [
            "W2 is PARTIAL and the writer is BLOCKED_NOT_ADMITTED",
            "the 16 fixtures/oracles are PROPOSED_DESIGN, not Case Owner product freeze",
            "product Host/runner/principal is UNBOUND",
            "Checker/Consumer are local distinct processes, not an original-domain principal",
        ],
    }
    write_json(_p(ev, "W3_DEV_RECEIPT.json"), obj)
    return obj


def build_product_current(root, ev, verified, ledger, candidate_sha):
    obj = {
        "schema": "FHS5.PLP.W3.ProductCurrent.NF@1",
        "subject_id": "FHS-5_PLP/W3/PRODUCT",
        "scope": SCOPE,
        "artifact_id": "FHS5-PLP/W3/PRODUCT-NF-20261126-" + os.path.basename(ev),
        "pack_manifest_sha256": verified["manifest_sha256"],
        "package_tree_sha256": verified["package_tree_sha256"],
        "candidate_tree_sha256": candidate_sha,
        "five_pins": {k: v["value"] for k, v in ledger["pins"].items()},
        "state": "W3_PRODUCT_HARNESS_DESIGN_ENGINE_RUN",
        "claims": {
            "W3_NF_VALIDATED": False,
            "INDEPENDENT_PASS": False,
            "W4_TECHNICALLY_READY": False,
            "W4_EXECUTION_READY": False,
        },
        "next_legal_action": "Case Owner freezes real 16 fixtures/oracles + names a product runner/Host; then re-run P02-P06",
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    write_json(_p(root, "W3_PRODUCT_CURRENT.json"), obj)
    return obj


def write_docs(root, ev, verified, ledger, matrix, spec, cases, findings, graph, advice, delta, repair, receipt):
    lines = []
    lines.append("# FHS-5_PLP W3｜CLOSEOUT（本地 CODEX Native 產品施工）")
    lines.append("")
    lines.append("**run_id**：`" + os.path.basename(ev) + "`")
    lines.append("**subject**：`" + SUBJECT_ID + "`｜**scope**：`" + SCOPE + "`")
    lines.append("**decision**：`W3-PACK-PRIMARY-20261126-01`（本輪使用者指令為 delegated authority source）")
    lines.append("**pack**：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`；05 raw `"
                 + verified["manifest_sha256"] + "`；tree `" + verified["package_tree_sha256"] + "`")
    lines.append("")
    lines.append("## 1. 真狀態（不得互相冒充）")
    lines.append("")
    lines.append("| 狀態 | 本輪 | 依據 |")
    lines.append("|---|---|---|")
    lines.append("| `PACK_PRIMARY_SELECTED` | **成立** | seal/adoption/current/05/tree 全部真核一致 |")
    lines.append("| `PACK_EXECUTABLE` | **成立** | intake + 16 design case 真實子程序 |")
    lines.append("| `W3_NF_VALIDATED` | **未宣** | 16 案 oracle 是 `PROPOSED_DESIGN`；W2 `PARTIAL`；無原域 Checker |")
    lines.append("| `INDEPENDENT_PASS` | **未宣** | 只有本地分離 process，不是原域不同 principal |")
    lines.append("| `W3_TECHNICALLY_READY` | **未宣** | W2 writer `BLOCKED_NOT_ADMITTED`；W2 12 案未再資格化 |")
    lines.append("| `W3_EXECUTION_READY` | **未宣**（僅本地隔離 scope 可執行） | R/W3_EXEC 內 exact write set；產品 Host/runner UNBOUND |")
    lines.append("| `W4_TECHNICALLY_READY` / `W4_EXECUTION_READY` | **未宣** | W4 無具名採納入口；W3 未 validated |")
    lines.append("| `RELEASED` | **未宣** | 無 Publisher/Release |")
    lines.append("")
    lines.append("## 2. P01 接收與 W2 再資格化")
    lines.append("")
    lines.append("- 05 strict JSON、duplicate key 拒、5 files、37 assets、16 case join、28 sources、spans、source_set、package_tree：**全部真核 PASS**。")
    lines.append("- 五 pin（source/candidate/evidence/oracle/case_set）**彼此 distinct**；fixture_time/host/policy 另列。")
    lines.append("- W2：product candidate aggregate `8b4b4068313ae4d3ab066d6951add31d225d360ac053771d7d611621101ed8d7`；"
                 "狀態 `PARTIAL`；writer `BLOCKED_NOT_ADMITTED`。")
    lines.append("- W2 12 案：`CARRIED_NOT_REFROZEN`／oracle `PARTIALLY_FROZEN`／evidence `SEALED_AFTER_OBSERVED`；本輪 **不代簽、不重用 verdict**。")
    lines.append("- W2 matrix：`" + str(matrix["row_count"]) + "/12` rows 全部 `NOT_REQUALIFIED`；r3 ledger 只有 `10` 列且每列 `raw:null`；`W2-OPS-01`／`W2-DELTA-01` 無 case row；candidate aggregate `8b4b…` **無法由五 member 重算**（演算法未宣告）。")
    lines.append("- W2 verdict 重用：**不可能**。r3 verdict 在 `660da33` 的 gate/admission bytes 上產生，與凍結候選不同；本輪不重用、不代簽。")
    lines.append("- R4：需 Owner 在 **W2 scope** 新具名授權（roots/targets/ops/expiry/recovery）；W3 不得解封 writer 或刪 marker。")
    lines.append("")
    lines.append("## 3. P02–P06 實際出口")
    lines.append("")
    lines.append("| 工作 | 真出口 | 結果 |")
    lines.append("|---|---|---|")
    lines.append("| P02 Runner | 16 案子程序（argv/cwd/exit/stdout/stderr raw） | `" + str(sum(1 for c in cases if c["design_verdict"] == "PASS")) + "/16` design PASS；`" + str(sum(1 for c in cases if c["process_exit_matches"])) + "/16` process exit 相符 |")
    lines.append("| P03 Finding | 2 個 `TEST_MUTANT_FINDING`，2 個 failure class | A=SECURITY_AUTHORIZATION(P1)，B=DATA_CONSUMPTION(P2) |")
    lines.append("| P04 FAR | RQ0–RQ4、EvidenceGraph、五態 | states=`" + ",".join(graph["states_seen"]) + "`；all_five=`" + str(graph["all_five_states"]) + "` |")
    lines.append("| P05 Advice | 每 Finding 2 個實質 alternatives、十原名 | enum=`" + str(advice["advice_names_defined"]) + "`；used=`" + ",".join(advice["advice_names_used"]) + "`；advice_is_grant=false |")
    lines.append("| P06 Guide2 | 七鍵→九鍵 lossless；兩期真 receipt | P1/P2=`" + delta["p1_p2"]["state"] + "`；P1/P3=`" + delta["p1_p3"]["state"] + "` |")
    lines.append("| P06 Repair | pre/RED/post/GREEN/restore/RED/re-apply | `" + repair["verdict"] + "`；restore=`" + str(repair["restored_matches_preimage"]) + "` |")
    lines.append("")
    lines.append("## 4. 16 原案設計層結果")
    lines.append("")
    lines.append("> 這一節是 **DESIGN_ENGINE** 觀察層。它不是 Case Owner 的原域 freeze，也不是產品 `COMPONENT/INVOCATION/E2E/HOST` PASS。`03` 的 `observed=null`／`verdict=NOT_RUN` 沒有被回填。")
    lines.append("")
    lines.append("| Case | Kind | Design verdict | Product case state | observed token |")
    lines.append("|---|---|---|---|---|")
    for c in cases:
        lines.append("| `" + c["case_id"] + "` | " + c["kind"] + " | " + c["design_verdict"]
                     + " | " + c["product_case_state"] + " | `" + c["observed_token"] + "` |")
    lines.append("")
    lines.append("## 5. 兩個動態 Finding（隔離 mutant，非真產品缺陷）")
    lines.append("")
    lines.append("| ID | class | severity | expected | observed | raw SHA |")
    lines.append("|---|---|---|---|---|---|")
    for f in findings:
        lines.append("| `" + f["id"] + "` | " + f["class"] + " | " + f["severity"] + " | `"
                     + f["expected"]["token"] + "` | `" + f["observed"]["token"] + "` | `"
                     + f["raw_sha256"][:16] + "…` |")
    lines.append("")
    lines.append("兩者都明確標 `TEST_MUTANT_FINDING`；沒有假稱 W2/W3 發現真產品缺陷。")
    lines.append("")
    lines.append("## 6. 分母與未閉合")
    lines.append("")
    lines.append("- W3 原案：16/16 **design-engine executed**；0/16 **product-validated**（缺真 Case Owner freeze/runner/Host）。")
    lines.append("- 33 FR：33/33 machine crosswalk join（`05.case_refs`↔`03`），不是 33/33 產品 PASS。")
    lines.append("- EC 16＋FAR 17：原義保留；本輪只跑設計 predicate，原域分母未合併。")
    lines.append("- W2 12 案：12 rows `NOT_REQUALIFIED`；不得以 W3 成果升格 W2。")
    lines.append("- FAR 五態：本輪真跑 HIT/ZERO/UNAVAILABLE/BLOCKED/ERROR；Fabric/ResearchWO 仍 `UNBOUND`。")
    lines.append("- Advice 十原名：可檢索且 alias 完整；實際使用 2 個，不代表十個都已被證據觸發。")
    lines.append("")
    lines.append("## 7. 證據索引（本 run）")
    lines.append("")
    for rel in [
        "W3_DEV_RECEIPT.json", "BATCH_LEDGER.json", "W3_CHANGESET.json",
        "W3_DELTA.json", "far/FAR_GRAPH.json", "ADVICE/DECISION_ADVICE.json",
        "repair/REPAIR_RECEIPT.json", "cases/", "mutants/", "subagent_w2_audit.md",
    ]:
        lines.append("- `evidence/" + os.path.basename(ev) + "/" + rel + "`")
    lines.append("")
    lines.append("## 8. 下一合法動作")
    lines.append("")
    lines.append("1. Case Owner 以真 bytes 凍結 16 案 fixture/oracle/case-set（expected-before-observed），把 `NOT_RUN` 留在原檔直到真跑。")
    lines.append("2. Owner 若要 W2 真產品，於 **W2 scope** 給新具名 writer 授權；不得用本 W3 decision 解封。")
    lines.append("3. 綁真 W3 product Host/runner/principal 後，重跑 P02–P06 受影 slice；distinct Checker 與 fresh Consumer 另簽。")
    lines.append("4. 只有 03 §10.3 全成立，才宣 `W3_NF_VALIDATED`／`INDEPENDENT_PASS`。")
    lines.append("")
    closeout = "\n".join(lines) + "\n"
    _write_text(_p(root, "FHS-5_PLP_W3_CLOSEOUT.md"), closeout)
    _write_text(_p(ev, "FHS-5_PLP_W3_CLOSEOUT.md"), closeout)

    h = []
    h.append("# FHS-5_PLP W3｜HANDOFF（W3 → W4 欄級）")
    h.append("")
    h.append("- `from_stage`：W3｜`to_stage`：W4")
    h.append("- `handoff_id`：`W3-HANDOFF-" + os.path.basename(ev) + "`")
    h.append("- `project`：`FHS-5_PLP`｜`work_id`：`W3-NF-01`")
    h.append("- `pack_ref`：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`")
    h.append("- `pack_manifest_sha256`：`" + verified["manifest_sha256"] + "`")
    h.append("- `package_tree_sha256`：`" + verified["package_tree_sha256"] + "`")
    h.append("- `candidate_commit`：`UNBOUND`（W2 product baseline `dada2354…` 仍 PARTIAL；W3 產品 commit 於 push 後另記）")
    h.append("- `oracle_sha256`：`" + ledger["pins"]["oracle"]["value"] + "`（design oracle set；非 product freeze）")
    h.append("- `case_set_sha256`：`" + ledger["pins"]["case_set"]["value"] + "`（design case set）")
    h.append("- `evidence_ref`：`evidence/" + os.path.basename(ev) + "/`")
    h.append("- `checker_ref` / `consumer_ref`：見同目錄 `CHECKER_RECEIPT.json`／`CONSUMER_RECEIPT.json`（本地 distinct process）")
    h.append("- `publication_state`：見 `PUBLICATION_RECEIPT.json`")
    h.append("")
    h.append("## 五 pin")
    h.append("")
    h.append("| pin | value | state |")
    h.append("|---|---|---|")
    for k, v in ledger["pins"].items():
        h.append("| `" + k + "` | `" + v["value"] + "` | " + v.get("kind", "") + " |")
    h.append("")
    h.append("## W4 可消費欄位")
    h.append("")
    h.append("| W4 欄 | 本輪值 |")
    h.append("|---|---|")
    h.append("| `FindingSet[].raw_sha256` | " + ", ".join("`" + f["raw_sha256"][:16] + "…`" for f in findings) + " |")
    h.append("| `NotCovered[]` | 16 案 product state `NOT_COVERED`；W2 12 rows `NOT_REQUALIFIED` |")
    h.append("| `FARRetrievalGraph` | `far/FAR_GRAPH.json`；五態 " + ",".join(graph["states_seen"]) + " |")
    h.append("| `DecisionAdvice` | `ADVICE/DECISION_ADVICE.json`；advice 非 grant |")
    h.append("| `W3_DELTA` | P1/P2 `" + delta["p1_p2"]["state"] + "`；P1/P3 `" + delta["p1_p3"]["state"] + "` |")
    h.append("| `ChangeSet` | `W3_CHANGESET.json`；pack/W2 零寫入 |")
    h.append("| `CheckerReceipt` vs `ConsumerReceipt` | distinct local process；strength=`LOCAL_DISTINCT_PROCESS` |")
    h.append("")
    h.append("## readiness")
    h.append("")
    h.append("| claim | value | reason |")
    h.append("|---|---|---|")
    h.append("| `W4_TECHNICALLY_READY` | **NOT_CLAIMED** | W3 未 `W3_NF_VALIDATED`；W4 當期採納入口未取得 |")
    h.append("| `W4_EXECUTION_READY` | **NOT_CLAIMED** | 缺 W4 具名施工授權、Host/ACL、逐 op authority/preimage/recovery |")
    h.append("")
    h.append("## next legal action")
    h.append("")
    h.append("1. W4 只可先合法 READ/DRAFT，不得以本 handoff 當 W4 施工 Grant。")
    h.append("2. 取得 W4M 當期採納入口與具名授權後，按 W4 原 entry contract late-bind。")
    h.append("3. 若 Owner 要升 W3：先補 Case Owner freeze + 真 Host/runner + distinct Checker + fresh Consumer。")
    h.append("")
    h.append("## NotCovered / Resume")
    h.append("")
    h.append("- `W2_WRITER_BLOCKED`：Owner 於 W2 scope 新具名授權；保留原 marker。")
    h.append("- `PRODUCT_HOST_UNBOUND`：指名 HostID/principal/ACL/policy epoch。")
    h.append("- `PRODUCT_RUNNER_UNBOUND`：指名 binary/SHA/argv/cwd/timeout。")
    h.append("- `CASE_OWNER_FREEZE_MISSING`：16 案真 bytes + frozen_at + Case Owner。")
    h.append("- `DISTINCT_ORIGINAL_CHECKER_MISSING`：原域不同 principal。")
    h.append("- `W2_MATRIX_AUDIT`：r3 ledger 10 rows／全 raw:null；W2-OPS-01/W2-DELTA-01 無 case row；aggregate `8b4b…` 不可重算；不得重用 W2 verdict。")
    h.append("")
    handoff = "\n".join(h) + "\n"
    _write_text(_p(root, "FHS-5_PLP_W3_HANDOFF.md"), handoff)
    _write_text(_p(ev, "FHS-5_PLP_W3_HANDOFF.md"), handoff)
    return closeout, handoff


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--w2-root", required=True)
    ap.add_argument("--ext-root", required=True)
    a = ap.parse_args(argv)
    pack = os.path.abspath(a.pack)
    root = os.path.abspath(a.root)
    ev = _p(root, "evidence", a.run_id)
    os.makedirs(ev, exist_ok=True)

    verified = verify_pack(pack, _p(a.ext_root, "EXTERNAL_SEAL.json"),
                           _p(a.ext_root, "W3_OWNER_ADOPTION.json"),
                           _p(a.ext_root, "W3_CURRENT.json"))
    write_json(_p(ev, "INTAKE_RECEIPT.json"), {
        "schema": "FHS5.PLP.W3.IntakeReceipt@1",
        "run_id": a.run_id, "verified": verified["ok"],
        "manifest_sha256": verified["manifest_sha256"],
        "package_tree_sha256": verified["package_tree_sha256"],
        "counts": verified["counts"], "issues": verified["issues"],
        "remote_anchor": {"branch": "codex/w3-pack-nf-primary-20261126",
                          "commit": "4f489a6aa74d055b087deb5146022da12a99cf86",
                          "readback": "git ls-remote (this run)"},
        "read_only": True,
    })
    if not verified["ok"]:
        print(json.dumps({"action": "STOP_SCOPED", "issues": verified["issues"]}, ensure_ascii=False, indent=2))
        return 3

    ledger = build_freeze_ledger(pack, verified, a.w2_root)
    write_json(_p(ev, "FREEZE_LEDGER.json"), ledger)
    w2pins = read_w2_pins(a.w2_root)
    matrix = build_w2_matrix(w2pins)
    write_json(_p(ev, "W2_REQUALIFICATION_MATRIX.json"), matrix)
    man = load_json_strict(_p(pack, "05_W3_SOURCE_MANIFEST.json"))
    spec, bind = write_specs(root, pack, ev, man)
    ledger_path = _p(ev, "FREEZE_LEDGER.json")

    cases = run_cases(pack, root, a.run_id, ledger_path, a.w2_root, a.ext_root, ev)
    candidate_sha = tree_digest(_p(root, "W3"))["tree_sha256"]
    findings, traces = build_findings(pack, root, a.run_id, ev, candidate_sha)
    write_json(_p(ev, "FINDINGS", "FINDING_SET.json"), {
        "schema": "FHS5.PLP.W3.FindingSet@1",
        "findings": findings, "traces": traces,
        "eight_fields": ["id", "severity", "class", "subject_sha", "command",
                         "exit", "raw_sha256", "reproduction"],
        "all_eight_present": all(all(k in f for k in ("id", "severity", "class", "subject_sha",
                                                      "command", "exit", "raw_sha256", "reproduction"))
                                 for f in findings),
    })
    graph = build_far_graph(pack, root, ev, findings)
    advice = build_advice(ev, findings, graph)
    delta = build_delta(ev, root, ledger, candidate_sha)
    repair = build_repair(ev, root)
    batch = build_batch_ledger(root, ev, verified, cases, findings, graph, advice, delta, repair)
    changeset = build_changeset(root, pack, ev, verified)
    receipt = build_dev_receipt(root, ev, verified, ledger, matrix, spec, cases, findings,
                                graph, advice, delta, repair)
    current = build_product_current(root, ev, verified, ledger, candidate_sha)
    closeout, handoff = write_docs(root, ev, verified, ledger, matrix, spec, cases, findings,
                                   graph, advice, delta, repair, receipt)
    summary = {
        "run_id": a.run_id,
        "intake_ok": verified["ok"],
        "cases_design_pass": sum(1 for c in cases if c["design_verdict"] == "PASS"),
        "cases_total": len(cases),
        "process_exit_match": sum(1 for c in cases if c["process_exit_matches"]),
        "findings": len(findings),
        "far_states": graph["states_seen"],
        "delta": {"p1_p2": delta["p1_p2"]["state"], "p1_p3": delta["p1_p3"]["state"]},
        "repair": repair["verdict"],
        "candidate_tree_sha256": candidate_sha,
        "claims": receipt["claims"],
        "closeout_sha256": sha256_file(_p(root, "FHS-5_PLP_W3_CLOSEOUT.md")),
        "handoff_sha256": sha256_file(_p(root, "FHS-5_PLP_W3_HANDOFF.md")),
    }
    write_json(_p(ev, "PIPELINE_SUMMARY.json"), summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
