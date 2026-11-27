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

    def verify_seal(manifest_path: Path, seal_obj: dict) -> bool:
        return sha_file(manifest_path) == seal_obj.get("manifest_sha256")

    bad = copy.deepcopy(seal)
    bad["manifest_sha256"] = "0" * 64
    checks["wrong_pin_refused"] = not verify_seal(ev / "EVIDENCE_MANIFEST.json", bad)

    w2 = jl(runs / "w2" / "W2_RESULT.json")
    dev = jl(runs / "w2" / "raw" / "W2-DEV-01.json")
    ops = jl(runs / "w2" / "raw" / "W2-OPS-01.json")
    ecp = jl(runs / "w1" / "raw" / "ECP67_MEASURED.json")
    w0f = jl(G3 / "runs" / "w0_full" / "W0_FULL_RESULT.json")
    checks["w0_partial_state"] = (w0f["counts"]["pass"] == 41
                                  and w0f["counts"]["fail"] == 2
                                  and w0f["verdict"] == "PARTIAL")
    checks["w2_not_admitted"] = w2["verdict"] == "NOT_ADMITTED" and w2.get("not_admitted") == 3
    checks["dev_fail_closed"] = (dev["verdict"] == "NOT_ADMITTED"
                                 and dev["observed"]["post_actual"] == {})
    checks["ops_fail_closed"] = (ops["verdict"] == "NOT_ADMITTED"
                                 and ops["observed"]["checks"].get("exit0") is False)
    checks["ecp_measured"] = (ecp["count"] == 67
                              and ecp["counts"].get("OBSERVED_THIS_RUN", 0) >= 50)

    evidence_accepted = all(checks.values())
    admitted = w2["verdict"] != "NOT_ADMITTED"
    w0_closed = w0f["verdict"] == "DONE"
    accepted = evidence_accepted and admitted and w0_closed
    doc = {"schema": "FHS5.PLP.G3.W3ConsumerReadback@2",
           "verdict": ("ACCEPT" if accepted else
                       ("BLOCKED_NOT_ADMITTED" if evidence_accepted and not admitted
                        else "REFUSE_NOT_CLOSED")),
           "accepted": accepted,
           "evidence_accepted": evidence_accepted,
           "admitted": admitted,
           "checks": checks,
           "used": {"candidate": pins["candidate"]["aggregate"],
                    "manifest_sha256": seal["manifest_sha256"],
                    "packs": pins["source"],
                    "w2_cases": 12,
                    "w2_not_admitted": w2.get("not_admitted"),
                    "ecp": ecp["counts"]},
           "consumer_id": "g3-w3-consumer-20261127",
           "not_claimed": ["W3 execution", "Release", "independent external principal"]}
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"accepted": accepted, "failed": [k for k, v in checks.items() if not v]}))
    return 0 if accepted else 2


if __name__ == "__main__":
    sys.exit(main())
