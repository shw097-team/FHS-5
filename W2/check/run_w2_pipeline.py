#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 read-only requalification: freeze 12 cases, run, matrix, seal."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "W3", "impl")))

from w3_common import (digest_obj, load_json_strict, run_process, sha256_bytes,
                       sha256_file, tree_digest, write_json)

CASES = [
    "W2-DEV-01", "W2-DEV-02", "W2-OPS-01", "W2-OPS-02",
    "W2-EFFECT-01", "W2-AUTH-01", "W2-RUNNER-01", "W2-DELTA-01",
    "W2-R3-01", "W2-R3-02", "W2-R3-03", "W2-R3-04",
]


def build_case_root(pack, root, run_id, w2_repo_root=None):
    case_root = Path(root) / "W2" / "case_root"
    if case_root.exists():
        shutil.rmtree(case_root)
    (case_root / "fixtures").mkdir(parents=True)
    (case_root / "oracles").mkdir(parents=True)
    refs = []
    for cid in CASES:
        fx_src = Path(pack) / "assets" / "fixtures" / (cid + ".json")
        or_src = Path(pack) / "assets" / "oracles" / (cid + ".json")
        fx = load_json_strict(fx_src)
        oracle = load_json_strict(or_src)
        fx_dst = case_root / "fixtures" / (cid + ".json")
        or_dst = case_root / "oracles" / (cid + ".json")
        fobj = dict(fx)
        fobj["product_freeze"] = {
            "state": "W2_PRODUCT_REQUAL_FROZEN",
            "case_owner": "CODEX delegated Case Owner (W2 upstream requalification)",
            "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "revision": "W2-RQ-20261126-r1",
            "source": "19_W2_NF_CODEX_20261126/assets/fixtures/" + cid + ".json",
        }
        oobj = dict(oracle)
        oobj["product_freeze"] = {
            "state": "W2_PRODUCT_REQUAL_ORACLE_FROZEN",
            "case_owner": "CODEX delegated Case Owner (W2 upstream requalification)",
            "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "revision": "W2-RQ-20261126-r1",
            "expected_before_observed": True,
            "source": "19_W2_NF_CODEX_20261126/assets/oracles/" + cid + ".json",
        }
        write_json(fx_dst, fobj)
        write_json(or_dst, oobj)
        refs.append({
            "case_id": cid, "kind": oracle.get("kind"),
            "requirement_refs": fx.get("requirement_refs"),
            "fixture": {"path": "fixtures/" + cid + ".json",
                        "sha256": sha256_file(fx_dst), "bytes": os.path.getsize(fx_dst)},
            "oracle": {"path": "oracles/" + cid + ".json",
                       "sha256": sha256_file(or_dst), "bytes": os.path.getsize(or_dst)},
        })
    man = {
        "schema": "FHS5.PLP.W2.ProductCaseManifest@1",
        "subject_id": "FHS-5_PLP/W2/CONTROL_PACK",
        "scope": "W2-NF-01",
        "revision": "W2-RQ-20261126-r1",
        "case_owner": "CODEX delegated Case Owner (W2 upstream requalification)",
        "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "case_refs": refs,
        "case_count": len(refs),
    }
    write_json(case_root / "05_W2_PRODUCT_CASE_MANIFEST.json", man)
    (case_root / "W2_CANDIDATE_ROOT.txt").write_text(str(w2_repo_root or ""), encoding="utf-8")
    return case_root, man


def freeze(case_root, man, w2_repo, pack):
    oracle_rows = [{"case_id": c["case_id"], "sha256": c["oracle"]["sha256"]} for c in man["case_refs"]]
    man05 = load_json_strict(Path(pack) / "05_W2_SOURCE_MANIFEST.json")
    source_set = man05.get("source_set_sha256") or "NA"
    head = run_process(["git", "-C", str(w2_repo), "rev-parse", "HEAD"], cwd=w2_repo, timeout_s=30)
    tree = run_process(["git", "-C", str(w2_repo), "rev-parse", "HEAD^{tree}"], cwd=w2_repo, timeout_s=30)
    if head["exit"] != 0 or tree["exit"] != 0:
        raise SystemExit("GIT_PROBE_FAILED: no hard-coded candidate fallback")
    delivery = head["stdout"].decode().strip()
    delivery_tree = tree["stdout"].decode().strip()
    pins = {
        "source": source_set,
        "candidate": delivery_tree,
        "evidence": sha256_file(Path(pack) / "05_W2_SOURCE_MANIFEST.json"),
        "oracle": digest_obj(oracle_rows),
        "case_set": sha256_file(case_root / "05_W2_PRODUCT_CASE_MANIFEST.json"),
    }
    return {
        "schema": "FHS5.PLP.W2.RequalFreezeLedger@1",
        "subject_id": "FHS-5_PLP/W2/CONTROL_PACK",
        "scope": "W2-NF-01",
        "pins": pins,
        "pins_distinct": len(set(pins.values())) == 5,
        "candidate_commit": delivery,
        "candidate_tree": delivery_tree,
        "candidate_aggregate_digest": "8b4b4068313ae4d3ab066d6951add31d225d360ac053771d7d611621101ed8d7",
        "aggregate_algorithm": "UNDECLARED_OLD_VALUE_PRESERVED",
        "aggregate_reproducible": False,
        "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "case_owner": "CODEX delegated Case Owner",
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--w2-repo", required=True)
    a = ap.parse_args(argv)
    ev = Path(a.root) / "evidence" / a.run_id
    ev.mkdir(parents=True, exist_ok=True)
    case_root, man = build_case_root(a.pack, a.root, a.run_id, a.w2_repo)
    ledger = freeze(case_root, man, a.w2_repo, a.pack)
    write_json(ev / "W2_FREEZE.json", ledger)
    records = []
    for cid in CASES:
        argv = [sys.executable, os.path.join(HERE, "run_w2_case.py"),
                "--case-root", str(case_root), "--case", cid,
                "--root", a.root, "--run-id", a.run_id]
        proc = run_process(argv, cwd=a.root, timeout_s=120)
        rec = load_json_strict(ev / "cases" / cid / "record.json")
        rec["process"] = {"argv": proc["argv"], "cwd": proc["cwd"], "exit": proc["exit"],
                          "stdout_sha256": proc["stdout_sha256"],
                          "stderr_sha256": proc["stderr_sha256"],
                          "start": proc["start"], "end": proc["end"]}
        write_json(ev / "cases" / cid / "record.json", rec)
        records.append(rec)
    matrix = {
        "schema": "FHS5.PLP.W2.RequalificationMatrix@2",
        "subject_id": "FHS-5_PLP/W2/CONTROL_PACK",
        "scope": "W2-NF-01",
        "rows": [{"case_id": r["case_id"], "kind": r["kind"], "verdict": r["verdict"],
                  "observed_tokens": r["observed_tokens"], "raw_sha256": r["raw_sha256"],
                  "record_ref": str(ev / "cases" / r["case_id"] / "record.json"),
                  "product_case_state": r["product_case_state"]} for r in records],
        "row_count": len(records),
        "pass_count": sum(1 for r in records if r["verdict"] == "PASS"),
        "freeze": ledger,
        "verdict": "W2_UPSTREAM_REQUALIFIED_READONLY"
        if all(r["verdict"] == "PASS" for r in records) else "W2_REQUAL_PARTIAL",
        "W2_NF_VALIDATED": False,
        "substitute_cases": [],
        "real_candidate_cases": sum(1 for r in records if r["verdict"] == "PASS"),
        "w2_nf_reason": "W2 protected writer/gate/marker remains BLOCKED_NOT_ADMITTED; no original-domain W2 signer",
        "not_covered": ["R4 protected writer", "W2 original-domain signature", "W2 gate/marker change"],
    }
    write_json(ev / "W2_REQUALIFICATION_MATRIX.json", matrix)
    raw_rows = []
    for r in records:
        for p in (ev / "cases" / r["case_id"]).glob("*"):
            if p.is_file():
                raw_rows.append({"path": str(p.relative_to(a.root)).replace(os.sep, "/"),
                                 "sha256": sha256_file(p), "bytes": os.path.getsize(p)})
    raw_rows.sort(key=lambda x: x["path"])
    write_json(ev / "W2_RAW_MANIFEST.json", {
        "schema": "FHS5.PLP.W2.RequalRawManifest@1",
        "run_id": a.run_id, "files": raw_rows, "file_count": len(raw_rows),
        "self_excluded": True,
    })
    seal = {
        "schema": "FHS5.PLP.W2.RequalSeal@1",
        "run_id": a.run_id,
        "matrix_sha256": sha256_file(ev / "W2_REQUALIFICATION_MATRIX.json"),
        "raw_manifest_sha256": sha256_file(ev / "W2_RAW_MANIFEST.json"),
        "freeze_sha256": sha256_file(ev / "W2_FREEZE.json"),
        "case_root_tree_sha256": tree_digest(case_root)["tree_sha256"],
        "verdict": matrix["verdict"],
    }
    write_json(ev / "W2_REQUAL_SEAL.json", seal)
    summary = {"rows": matrix["row_count"], "pass": matrix["pass_count"],
               "verdict": matrix["verdict"], "W2_NF_VALIDATED": False,
               "pins_distinct": ledger["pins_distinct"]}
    write_json(ev / "W2_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
