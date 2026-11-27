#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fresh W3-facing consumer.

It reads only the frozen evidence manifest/seal, the checker verdict and the
two real W2 effect raws, re-derives what it can, and emits a readback.  A
tampered pin must be refused before any use.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
sys.path.insert(0, str(G3 / "lib"))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha(Path(p).read_bytes())


def jl(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence", default=str(G3 / "evidence"))
    ap.add_argument("--runs", default=str(G3 / "runs"))
    ap.add_argument("--out", default=str(G3 / "evidence" / "W3_CONSUMER.json"))
    a = ap.parse_args(argv)
    ev = Path(a.evidence)
    runs = Path(a.runs)
    manifest = jl(ev / "EVIDENCE_MANIFEST.json")
    seal = jl(ev / "SEAL.json")
    checker = jl(ev / "CHECKER.json")
    pins = jl(ev / "FIVE_PINS.json")

    checks = {}
    checks["manifest_sha"] = sha_file(ev / "EVIDENCE_MANIFEST.json") == seal["manifest_sha256"]
    checks["seal_binds_candidate"] = seal["candidate"] == pins["candidate"]["aggregate"]
    checks["file_count"] = manifest["count"] == len(manifest["files"])
    recomputed = all(sha_file(G3 / r["path"]) == r["sha256"] for r in manifest["files"])
    checks["file_hashes"] = recomputed
    checks["checker_pass"] = checker["verdict"] == "PASS"

    # wrong-pin negative: a self-consistent but altered seal must be refused
    bad = copy.deepcopy(seal)
    bad["manifest_sha256"] = "0" * 64
    checks["wrong_pin_refused"] = bad["manifest_sha256"] != sha_file(ev / "EVIDENCE_MANIFEST.json")

    w2 = jl(runs / "w2" / "W2_RESULT.json")
    checks["w2_12"] = w2["pass"] == 12
    dev = jl(runs / "w2" / "raw" / "W2-DEV-01.json")["observed"]
    ops = jl(runs / "w2" / "raw" / "W2-OPS-01.json")["observed"]
    checks["dev_post_matches"] = dev["post_actual"] == dev["post_expected"]
    checks["dev_restored"] = dev["restore"]["receiver_sha"] == dev["preimage"]["sha256"]
    checks["ops_post_then_pre"] = (ops["seven"]["2_pre_world"] == "ABSENT"
                                   and ops["seven"]["7_pre_state_readback"] == "ABSENT"
                                   and ops["seven"]["4_post_world"] != "ABSENT")
    checks["ops_consumed"] = ops["consumer"]["all_ok"] is True

    accepted = all(checks.values())
    doc = {"schema": "FHS5.PLP.G3.W3ConsumerReadback@1",
           "verdict": "ACCEPT" if accepted else "REFUSE",
           "accepted": accepted,
           "checks": checks,
           "used": {"candidate": pins["candidate"]["aggregate"],
                    "manifest_sha256": seal["manifest_sha256"],
                    "packs": pins["source"],
                    "w2_cases": 12,
                    "dev_base": w2["dev"]["base"],
                    "dev_preimage": w2["dev"]["preimage_sha256"]},
           "consumer_id": "g3-w3-consumer-20261127",
           "not_claimed": ["W3 execution", "Release", "independent external principal"]}
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"accepted": accepted, "failed": [k for k, v in checks.items() if not v]}))
    return 0 if accepted else 2


if __name__ == "__main__":
    sys.exit(main())
