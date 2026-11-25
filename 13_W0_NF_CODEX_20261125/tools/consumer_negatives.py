#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the consumer positive plus representative pin/raw/path negatives.
Every negative must fail closed before the product CLI executes."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.ROOT / "07_CONSUMER"


def run_consumer(args: list[str], tag: str) -> dict:
    r = lib.run([sys.executable, str(lib.ROOT / "tools" / "consumer.py"), *args], lib.ROOT,
                timeout=180, raw_dir=OUT / "neg_raw", tag=tag)
    receipt = None
    # the consumer prints its run_id; find that run receipt
    try:
        meta = json.loads(r["stdout"])
        rp = OUT / "runs" / meta["run_id"] / "receipt.json"
        if rp.is_file():
            receipt = json.loads(rp.read_text(encoding="utf-8"))
    except Exception:
        meta = {}
    return {"exit": r["exit"], "meta": meta, "receipt": receipt}


def copy_handoff(src: Path, dst: Path, key: str, value: str):
    text = src.read_text(encoding="utf-8")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if key in line and line.lstrip().startswith("-"):
            lines[i] = f"- **{key}**：`{value}`"
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handoff", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--out", default=str(OUT / "negatives.json"))
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / "neg_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    shadow = work / "root"
    shutil.copytree(lib.ROOT, shadow,
                    ignore=shutil.ignore_patterns(".git", "tmp", "__pycache__", "runs", "neg_work"))
    handoff, evidence = Path(a.handoff).resolve(), Path(a.evidence).resolve()
    evd = json.loads(evidence.read_text(encoding="utf-8"))
    cases = []

    def record(name, expected, r):
        rec = r["receipt"] or {}
        got = rec.get("failure_code")
        cli = (rec.get("cli") or {}).get("executed")
        cases.append({"name": name, "expected": expected, "got": got,
                      "rejected": r["exit"] == 0 and rec.get("consumed") is False
                                  and cli is False and got == expected,
                      "cli_executed": cli, "run_id": (rec.get("run_id"))})

    base = ["--handoff", str(handoff), "--evidence-manifest", str(evidence),
            "--evidence-root", str(lib.ROOT), "--allow-pending-t10", "--expect-reject"]

    # positive (allow pending T10 at this stage)
    pos = run_consumer(["--handoff", str(handoff), "--evidence-manifest", str(evidence),
                        "--evidence-root", str(lib.ROOT), "--allow-pending-t10"], "consumer_positive")

    def neg(name, expected, h_path, e_path, root, extra=None):
        args = ["--handoff", str(h_path), "--evidence-manifest", str(e_path),
                "--evidence-root", str(root), "--allow-pending-t10", "--expect-reject"]
        if extra:
            args += extra
        r = run_consumer(args, "neg_" + name)
        record(name, expected, r)

    # handoff pin negatives
    for name, key, expected in (("wrong_pack", "pack_manifest_sha256", "PIN_MISMATCH_PACK"),
                                ("wrong_candidate", "candidate_commit", "PIN_MISMATCH_CANDIDATE"),
                                ("wrong_oracle", "oracle_sha256", "PIN_MISMATCH_ORACLE"),
                                ("wrong_evidence", "evidence_manifest_sha256", "PIN_MISMATCH_EVIDENCE")):
        hp = work / f"{name}.md"
        copy_handoff(handoff, hp, key, "0" * 64)
        neg(name, expected, hp, evidence, lib.ROOT)

    # mutated indexed raw
    target = None
    for e in evd.get("files") or []:
        if e["path"].startswith("04_DEV_OPS/raw/") and (shadow / e["path"]).is_file():
            target = shadow / e["path"]
            break
    orig = target.read_bytes()
    target.write_bytes(orig + b"X")
    neg("mutated_raw", "EVIDENCE_HASH_MISMATCH", handoff, evidence, shadow)
    target.write_bytes(orig)

    # missing indexed file
    target.unlink()
    neg("missing_file", "MISSING_FILE", handoff, evidence, shadow)
    target.write_bytes(orig)

    # evidence-content negatives with a rebound handoff pin
    def mutated_evidence(name, mutate, expected):
        e = json.loads(json.dumps(evd))
        mutate(e)
        ep = work / f"{name}.json"
        ep.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        hp = work / f"{name}.md"
        copy_handoff(handoff, hp, "evidence_manifest_sha256", lib.sha_file(ep))
        neg(name, expected, hp, ep, lib.ROOT)

    mutated_evidence("bad_schema", lambda e: e.__setitem__("schema", "X"), "EVIDENCE_SCHEMA")
    mutated_evidence("duplicate_pin",
                     lambda e: e["files"].append(dict(e["files"][0])), "DUPLICATE_PIN")
    mutated_evidence("cross_subject",
                     lambda e: e["candidate"].__setitem__("head", "0" * 40),
                     "EVIDENCE_CANDIDATE_MISMATCH")
    mutated_evidence("path_escape",
                     lambda e: e["files"].append({"path": "../escape.txt", "bytes": 0,
                                                  "sha256": "0" * 64}), "PATH_DOTDOT")

    all_ok = all(c["rejected"] for c in cases) and pos["receipt"] and pos["receipt"].get("consumed")
    out = {
        "schema": "FHS5.W0NF.ConsumerNegatives@1",
        "positive": {"exit": pos["exit"], "run_id": (pos["receipt"] or {}).get("run_id"),
                     "consumed": (pos["receipt"] or {}).get("consumed"),
                     "checks": len((pos["receipt"] or {}).get("checks") or [])},
        "negative_cases": cases,
        "all_rejected": all(c["rejected"] for c in cases),
        "verdict": "NEGATIVES_REJECTED" if all_ok else "NEGATIVE_LEAK",
    }
    lib.write_json(Path(a.out), out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if all_ok else 3


if __name__ == "__main__":
    sys.exit(main())
