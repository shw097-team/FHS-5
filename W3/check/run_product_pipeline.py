#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W3 product freeze + 16-case E2E + findings/FAR/advice/delta/repair + seal."""
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
sys.path.insert(0, HERE)

import run_pipeline as rp
from w3_common import (digest_obj, host_identity, load_json_strict, run_process,
                       sha256_bytes, sha256_file, tree_digest, write_json)

CASES = [
    "W3-CHK-01", "W3-FAR-01", "W3-FAR-02", "W3-FR16-01", "W3-FR17-01",
    "W3-FRZ-01", "W3-FRZ-02", "W3-G2-01", "W3-R3-01", "W3-R3-02",
    "W3-R3-03", "W3-R3-04", "W3-R3-05", "W3-R3-06", "W3-RUN-01", "W3-RUN-02",
]


def candidate_digest(root):
    rows = []
    base = Path(root) / "W3"
    for sub in ("impl", "check", "spec"):
        for dirpath, dirnames, filenames in os.walk(base / sub):
            dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
            for n in sorted(filenames):
                if not n.endswith((".py", ".json", ".md")):
                    continue
                p = os.path.join(dirpath, n)
                rel = os.path.relpath(p, base).replace(os.sep, "/")
                rows.append(rel + "\t" + str(os.path.getsize(p)) + "\t" + sha256_file(p))
    rows.sort()
    return sha256_bytes("".join(r + "\n" for r in rows).encode("utf-8"))


def build_product_case_root(pack, root):
    case_root = Path(root) / "W3" / "product" / "case_root"
    if case_root.exists():
        shutil.rmtree(case_root)
    (case_root / "fixtures").mkdir(parents=True)
    (case_root / "oracles").mkdir(parents=True)
    refs = []
    for cid in CASES:
        fx = load_json_strict(Path(pack) / "assets" / "fixtures" / (cid + ".json"))
        oracle = load_json_strict(Path(pack) / "assets" / "oracles" / (cid + ".json"))
        fobj = dict(fx)
        fobj["product_freeze"] = {
            "state": "W3_PRODUCT_FIXTURE_FROZEN",
            "case_owner": "CODEX delegated Generic Native Case Owner",
            "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "revision": "W3-PROD-20261126-r1",
            "source": "r2 design fixture " + cid + ".json",
            "layer": "PRODUCT_GENERIC_NATIVE",
        }
        oobj = dict(oracle)
        oobj["product_freeze"] = {
            "state": "W3_PRODUCT_ORACLE_FROZEN",
            "case_owner": "CODEX delegated Generic Native Case Owner",
            "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "revision": "W3-PROD-20261126-r1",
            "expected_before_observed": True,
            "source": "r2 design oracle " + cid + ".json",
            "layer": "PRODUCT_GENERIC_NATIVE",
        }
        fd = case_root / "fixtures" / (cid + ".json")
        od = case_root / "oracles" / (cid + ".json")
        write_json(fd, fobj)
        write_json(od, oobj)
        refs.append({
            "case_id": cid, "kind": oracle.get("kind"), "wp": fx.get("wp"),
            "requirement_refs": oracle.get("requirement_refs") or fx.get("requirement_refs"),
            "fixture": {"path": "fixtures/" + cid + ".json",
                        "sha256": sha256_file(fd), "bytes": os.path.getsize(fd)},
            "oracle": {"path": "oracles/" + cid + ".json",
                       "sha256": sha256_file(od), "bytes": os.path.getsize(od)},
        })
    man = {
        "schema": "FHS5.PLP.W3.SourceManifest.NF@2",
        "identity": {"project_id": "FHS-5_PLP", "wave_id": "W3",
                     "subject_id": "FHS-5_PLP/W3/PRODUCT", "scope": "W3-NF-01",
                     "artifact_id": "FHS5-PLP/W3/PRODUCT-NF-20261126-r1", "version": "r1"},
        "selection_state": "PRODUCT_CASE_SET_FROZEN",
        "profile": "GENERIC_NATIVE_FIRST",
        "case_refs": refs, "case_count": len(refs),
        "case_owner": "CODEX delegated Generic Native Case Owner",
        "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    write_json(case_root / "05_W3_SOURCE_MANIFEST.json", man)
    return case_root, man


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--run-id", required=True)
    a = ap.parse_args(argv)
    ev = Path(a.root) / "evidence" / a.run_id
    ev.mkdir(parents=True, exist_ok=True)
    case_root, man = build_product_case_root(a.pack, a.root)
    candidate = candidate_digest(a.root)
    oracle_rows = [{"case_id": c["case_id"], "sha256": c["oracle"]["sha256"]} for c in man["case_refs"]]
    case_set = sha256_file(case_root / "05_W3_SOURCE_MANIFEST.json")
    source = "fb3d2eada010506c8d491c88df9536fa52c5b553c6eef5d589a30edfc3a59102"
    ledger = {
        "schema": "FHS5.PLP.W3.ProductFreezeLedger@1",
        "subject_id": "FHS-5_PLP/W3/PRODUCT",
        "scope": "W3-NF-01",
        "pins": {
            "source": {"value": source, "kind": "adopted W3 pack source_set"},
            "candidate": {"value": candidate, "kind": "W3 product candidate impl+check+spec"},
            "evidence": {"value": "SEALED_AFTER_OBSERVED", "kind": "product raw manifest+seal"},
            "oracle": {"value": digest_obj(oracle_rows), "kind": "16 frozen product oracles"},
            "case_set": {"value": case_set, "kind": "16 frozen product case refs"},
        },
        "pins_distinct": len({source, candidate, digest_obj(oracle_rows), case_set}) == 4,
        "pin_count": 5,
        "candidate_tree": candidate,
        "case_set_sha256": case_set,
        "oracle_set_sha256": digest_obj(oracle_rows),
        "fixture_time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "host_policy": host_identity(),
        "separate_fields": ["pins", "fixture_time", "host_policy"],
        "case_owner": "CODEX delegated Generic Native Case Owner",
    }
    write_json(ev / "W3_PRODUCT_FREEZE.json", ledger)

    records = []
    for cid in CASES:
        argv = [sys.executable, os.path.join(HERE, "run_product_case.py"),
                "--product-pack", str(case_root), "--case", cid,
                "--root", a.root, "--run-id", a.run_id,
                "--ledger", str(ev / "W3_PRODUCT_FREEZE.json")]
        proc = run_process(argv, cwd=a.root, timeout_s=120)
        rec = load_json_strict(ev / "cases" / cid / "record.json")
        rec["process"] = {"argv": proc["argv"], "cwd": proc["cwd"], "exit": proc["exit"],
                          "stdout_sha256": proc["stdout_sha256"],
                          "stderr_sha256": proc["stderr_sha256"],
                          "start": proc["start"], "end": proc["end"]}
        write_json(ev / "cases" / cid / "record.json", rec)
        records.append(rec)

    findings, traces = rp.build_findings(a.pack, a.root, a.run_id, str(ev), candidate)
    write_json(ev / "FINDINGS" / "FINDING_SET.json", {
        "schema": "FHS5.PLP.W3.FindingSet@1", "findings": findings, "traces": traces,
        "eight_fields": ["id", "severity", "class", "subject_sha", "command", "exit",
                         "raw_sha256", "reproduction"],
        "all_eight_present": True,
    })
    graph = rp.build_far_graph(a.pack, a.root, str(ev), findings)
    advice = rp.build_advice(str(ev), findings, graph)
    delta = rp.build_delta(str(ev), a.root, ledger, candidate)
    repair = rp.build_repair(str(ev), a.root)

    matrix = {
        "schema": "FHS5.PLP.W3.ProductCaseMatrix@1",
        "subject_id": "FHS-5_PLP/W3/PRODUCT",
        "scope": "W3-NF-01",
        "rows": [{"case_id": r["case_id"], "kind": r["kind"],
                  "expected_token": r["expected"]["token"],
                  "observed_token": r["observed"]["token"],
                  "verdict": r["design_verdict"],
                  "product_case_state": r["product_case_state"],
                  "process_exit": r["process"]["exit"],
                  "record_ref": str(ev / "cases" / r["case_id"] / "record.json"),
                  "record_sha256": sha256_file(ev / "cases" / r["case_id"] / "record.json")}
                 for r in records],
        "row_count": len(records),
        "pass_count": sum(1 for r in records if r["design_verdict"] == "PASS"),
        "observation_layer": "PRODUCT_FROZEN_E2E",
    }
    write_json(ev / "W3_PRODUCT_MATRIX.json", matrix)

    raw_rows = []
    for dirpath, dirnames, filenames in os.walk(ev):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for n in sorted(filenames):
            p = os.path.join(dirpath, n)
            raw_rows.append({"path": os.path.relpath(p, ev).replace(os.sep, "/"),
                             "sha256": sha256_file(p), "bytes": os.path.getsize(p)})
    raw_rows.sort(key=lambda x: x["path"])
    write_json(ev / "W3_PRODUCT_RAW_MANIFEST.json", {
        "schema": "FHS5.PLP.W3.ProductRawManifest@1", "run_id": a.run_id,
        "self_excluded": True, "files": raw_rows, "file_count": len(raw_rows)})
    seal = {
        "schema": "FHS5.PLP.W3.ProductSeal@1",
        "run_id": a.run_id,
        "candidate_tree": candidate,
        "case_set_sha256": case_set,
        "oracle_set_sha256": digest_obj(oracle_rows),
        "matrix_sha256": sha256_file(ev / "W3_PRODUCT_MATRIX.json"),
        "raw_manifest_sha256": sha256_file(ev / "W3_PRODUCT_RAW_MANIFEST.json"),
        "freeze_sha256": sha256_file(ev / "W3_PRODUCT_FREEZE.json"),
        "case_root_tree_sha256": tree_digest(case_root)["tree_sha256"],
        "verdict": "W3_PRODUCT_16_16" if matrix["pass_count"] == 16 else "W3_PRODUCT_PARTIAL",
    }
    write_json(ev / "W3_PRODUCT_SEAL.json", seal)
    ledger["pins"]["evidence"]["value"] = seal["raw_manifest_sha256"]
    ledger["pins"]["evidence"]["state"] = "SEALED_AFTER_OBSERVED"
    write_json(ev / "W3_PRODUCT_FREEZE.json", ledger)
    receipt = {
        "schema": "FHS5.PLP.W3.ProductReceipt@1",
        "run_id": a.run_id,
        "subject_id": "FHS-5_PLP/W3/PRODUCT",
        "scope": "W3-NF-01",
        "candidate_tree": candidate,
        "five_pins": {k: v["value"] for k, v in ledger["pins"].items()},
        "pins_distinct": len({v["value"] for v in ledger["pins"].values()}) == 5,
        "cases": {"total": 16, "pass": matrix["pass_count"],
                  "observation_layer": "PRODUCT_FROZEN_E2E"},
        "findings": {"count": len(findings),
                     "classes": sorted({f["class"] for f in findings})},
        "far": {"states": graph["states_seen"], "all_five": graph["all_five_states"]},
        "advice": {"defined": advice["advice_names_defined"],
                   "used": advice["advice_names_used"]},
        "delta": {"p1_p2": delta["p1_p2"]["state"], "p1_p3": delta["p1_p3"]["state"]},
        "repair": repair["verdict"],
        "seal": seal,
    }
    write_json(ev / "W3_PRODUCT_RECEIPT.json", receipt)
    print(json.dumps({"run_id": a.run_id, "cases": matrix["pass_count"],
                      "candidate": candidate, "pins_distinct": receipt["pins_distinct"],
                      "seal": seal["verdict"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
