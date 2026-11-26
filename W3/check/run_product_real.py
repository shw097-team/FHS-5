#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Orchestrate the real product projection: pack, pre-freeze, verify, checker, seal."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

from w3_common import digest_obj, load_json_strict, run_process, sha256_bytes, sha256_file, tree_digest, write_json


def candidate_digest(root):
    rows = []
    base = os.path.join(root, "W3")
    for sub in ("impl", "check", "spec"):
        for dp, dn, fn in os.walk(os.path.join(base, sub)):
            dn[:] = sorted(d for d in dn if d != "__pycache__")
            for n in sorted(fn):
                if not n.endswith((".py", ".json", ".md")):
                    continue
                p = os.path.join(dp, n)
                rel = os.path.relpath(p, base).replace(os.sep, "/")
                rows.append(rel + "\t" + str(os.path.getsize(p)) + "\t" + sha256_file(p))
    rows.sort()
    return sha256_bytes("".join(r + "\n" for r in rows).encode("utf-8"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--owner", required=True)
    ap.add_argument("--run-id", required=True)
    a = ap.parse_args(argv)
    root = a.root
    ev = os.path.join(root, "evidence", a.run_id)
    os.makedirs(ev, exist_ok=True)
    pack = os.path.join(root, "W3", "product_real", "pack")
    proc = run_process([sys.executable, os.path.join(HERE, "build_product_pack.py"),
                        "--owner", a.owner, "--out", pack], cwd=root, timeout_s=60)
    if proc["exit"] != 0:
        raise SystemExit("build_product_pack failed: " + proc["stderr"].decode("utf-8", "replace"))
    man = load_json_strict(os.path.join(pack, "05_W3_SOURCE_MANIFEST.json"))
    candidate = candidate_digest(root)
    oracle_rows = [{"case_id": c["case_id"], "sha256": c["oracle"]["sha256"]} for c in man["case_refs"]]
    case_set = sha256_file(os.path.join(pack, "05_W3_SOURCE_MANIFEST.json"))
    source = "fb3d2eada010506c8d491c88df9536fa52c5b553c6eef5d589a30edfc3a59102"
    pre = {
        "schema": "FHS5.PLP.W3.ProductFreezePre@2",
        "subject_id": "FHS-5_PLP/W3/PRODUCT",
        "scope": "W3-NF-01",
        "pins": {
            "source": {"value": source},
            "candidate": {"value": candidate},
            "evidence": {"value": "POST_EXECUTION_SEAL"},
            "oracle": {"value": digest_obj(oracle_rows)},
            "case_set": {"value": case_set},
        },
        "pins_distinct": len({source, candidate, digest_obj(oracle_rows), case_set}) == 4,
        "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "case_owner": "separate Case Owner session",
        "case_owner_freeze_sha256": sha256_file(os.path.join(pack, "CASE_OWNER_FREEZE.json")),
        "immutable": True,
    }
    write_json(os.path.join(ev, "FREEZE_PRE.json"), pre)
    ledger = {"pins": pre["pins"], "source_pack": os.path.join(root, "pack"),
              "fixture_time": pre["frozen_at"],
              "host_policy": {"host_id": "AUTHOR_LOCAL_WINDOWS",
                              "policy_epoch": "LOCAL-20261126",
                              "product_host": "UNBOUND"},
              "separate_fields": ["pins", "fixture_time", "host_policy"]}
    ledger_path = os.path.join(ev, "LEDGER_FOR_RUN.json")
    write_json(ledger_path, ledger)

    verdict_path = os.path.join(ev, "PRODUCT_VERDICT.json")
    v = run_process([sys.executable, os.path.join(HERE, "product_verify.py"),
                     "--product-pack", pack, "--root", root, "--run-id", a.run_id,
                     "--ledger", ledger_path, "--out", verdict_path], cwd=root, timeout_s=600)
    verdict = load_json_strict(verdict_path)
    checker_path = os.path.join(ev, "PRODUCT_CHECKER.json")
    c = run_process([sys.executable, os.path.join(HERE, "product_checker.py"),
                     "--product-pack", pack, "--root", root, "--run-id", a.run_id,
                     "--ledger", ledger_path, "--out", checker_path], cwd=root, timeout_s=300)
    checker = load_json_strict(checker_path)

    raw_rows = []
    for dp, dn, fn in os.walk(ev):
        dn[:] = sorted(d for d in dn if d != "__pycache__")
        for n in sorted(fn):
            p = os.path.join(dp, n)
            raw_rows.append({"path": os.path.relpath(p, ev).replace(os.sep, "/"),
                             "sha256": sha256_file(p), "bytes": os.path.getsize(p)})
    raw_rows.sort(key=lambda x: x["path"])
    raw_manifest = os.path.join(ev, "PRODUCT_RAW_MANIFEST.json")
    write_json(raw_manifest, {"schema": "FHS5.PLP.W3.ProductRawManifest@2",
                              "run_id": a.run_id, "self_excluded": True,
                              "files": raw_rows, "file_count": len(raw_rows)})
    seal = {
        "schema": "FHS5.PLP.W3.ProductSeal@2",
        "run_id": a.run_id,
        "candidate": candidate,
        "case_set": case_set,
        "oracle": digest_obj(oracle_rows),
        "raw_manifest_sha256": sha256_file(raw_manifest),
        "verdict_sha256": sha256_file(verdict_path),
        "checker_sha256": sha256_file(checker_path),
        "product_pass": verdict["product_pass"],
        "checker_verdict": checker["verdict"],
        "sealed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    write_json(os.path.join(ev, "PRODUCT_SEAL.json"), seal)
    receipt = {
        "schema": "FHS5.PLP.W3.ProductRealReceipt@1",
        "run_id": a.run_id,
        "candidate": candidate,
        "pins": {k: v["value"] for k, v in pre["pins"].items()},
        "pins_distinct": len({v["value"] for v in pre["pins"].values()}) == 5,
        "cases": {"total": verdict["case_count"], "product_pass": verdict["product_pass"]},
        "verdict": verdict,
        "checker": checker,
        "seal": seal,
        "product_engine_exit": v["exit"],
        "checker_exit": c["exit"],
    }
    write_json(os.path.join(ev, "PRODUCT_RECEIPT.json"), receipt)
    print(json.dumps({"cases": verdict["case_count"], "product_pass": verdict["product_pass"],
                      "checker": checker["verdict"], "verdict_exit": v["exit"]}, ensure_ascii=False))
    return 0 if checker["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
