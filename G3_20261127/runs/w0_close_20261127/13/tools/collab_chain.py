#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NF-T08: verify the real five-party collaboration chain by consuming each
producer's actual pins, and reject representative broken-link mutations."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import tqaep_spec

OUT = lib.PARTIES / "collab"
PRE = "5eab43de2d3f67d6afbb1c5f6bc390e2c391da36"


def blob_sha(rev_path: str) -> str:
    p = subprocess.run(["git", "-C", str(lib.REPO), "show", rev_path],
                       capture_output=True)
    return hashlib.sha256(p.stdout).hexdigest()


def load_dataset() -> dict:
    pack_sha = lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json")
    man = lib.load_json(lib.PACK / "05_W0_SOURCE_MANIFEST.json")
    dev = lib.load_json(lib.ROOT / "04_DEV_OPS" / "dev_patch.json")
    tpm = lib.load_json(lib.PARTIES / "tpm" / "tpm_gate.json")
    guide_start = lib.load_json(lib.PARTIES / "guide" / "thin_start.json")
    guide_resume = lib.load_json(lib.PARTIES / "guide" / "thin_resume.json")
    bridge = lib.load_json(lib.PARTIES / "bridge" / "bridge_summary.json")
    native_ctx = lib.load_json(lib.PARTIES / "collab" / "native_context.json")
    chall = lib.load_json(lib.PARTIES / "challenge" / "challenge_prepatch.json")
    far = lib.load_json(lib.PARTIES / "far" / "far.json")
    oracle = lib.load_json(lib.TQAEP / "oracle.json")
    head = lib.git("rev-parse", "HEAD")
    red_raw = lib.ROOT / "03_PARTIES" / "challenge" / "prepatch_raw" / "prepatch_probe.stderr.txt"
    return {
        "pack": {"sha": pack_sha, "manifest": man,
                 "files_ok": all(lib.sha_file(lib.PACK / e["path"]) == e["sha256"]
                                 for e in man["pack_files"])},
        "tpm": tpm,
        "guide_start": guide_start,
        "guide_resume": guide_resume,
        "bridge": bridge,
        "native_ctx": native_ctx,
        "dev": dev,
        "chall": chall,
        "far": far,
        "oracle": oracle,
        "head": head,
        "red_raw_sha": lib.sha_file(red_raw) if red_raw.is_file() else None,
        "v2_blob": blob_sha(PRE + ":briefcheck.py"),
        "v3_file": lib.sha_file(lib.REPO / "briefcheck.py"),
        "patch_text": (lib.ROOT / "04_DEV_OPS" / "patch_12prime.diff").read_text(encoding="utf-8"),
    }


def validate(ds: dict) -> tuple[bool, str | None, dict]:
    checks = []
    failure = None

    def ck(cid, ok, code):
        nonlocal failure
        checks.append({"id": cid, "ok": bool(ok)})
        if not ok and failure is None:
            failure = code

    if ds.get("chall") is None:
        return False, "CHALLENGE_UNBOUND", {"segments": []}
    pack = ds["pack"]
    ck("SOURCE-PINS", pack["files_ok"] and pack["sha"] == ds["guide_start"].get("pack_digest"),
       "SOURCE_IDENTITY")
    # TPM contracts consumed by Guide
    contracts = ds["tpm"].get("contracts") or {}
    ck("TPM-CONTRACTS", len(contracts) == 4 and all(len(v) == 64 for v in contracts.values()),
       "TPM_CONTRACT_MISSING")
    ck("TPM-REVIEWER", ds["tpm"]["reviewer"]["exit"] == 0
       and ds["tpm"]["reviewer"]["stdout"].get("defects") == 0, "REVIEWER_FAIL")
    ck("TPM-SOURCE-LINK", any(p.get("sha256") == pack["sha"]
                              for p in lib.load_json(lib.PARTIES / "tpm" / "pi.json")["source_refs"]),
       "TPM_SOURCE_MISMATCH")
    cc = ds["guide_start"].get("contract_context")
    contract_pins = {k: lib.sha_file(lib.PARTIES / "tpm" / f"{k}.json")
                     for k in ("pi", "pd", "dev_ecp", "ops_ecp")}
    ck("TPM-CONTRACTS-FROZEN", contracts == contract_pins, "TPM_CONTRACT_DRIFT")
    ck("TPM-GUIDE-CONTRACT-CONSUMED",
       bool(cc) and cc.get("pins") == contract_pins
       and cc.get("source_manifest_match") is True
       and len(cc.get("requirement_ids") or []) >= 4,
       "CONTRACT_CONTEXT_MISSING")
    nc = ds["native_ctx"]
    ck("BRIDGE-NATIVE-CONTEXT-CONSUMED",
       nc.get("verdict") == "CONTEXT_CONSUMED" and nc.get("case_set_match") is True
       and nc.get("context_sha_match") is True and nc.get("source_locators_ok") is True
       and (nc.get("native_runs") or {}).get("pos_ok") is True
       and (nc.get("native_runs") or {}).get("neg_ok") is True,
       "CONTEXT_NOT_CONSUMED")
    # Guide start -> Bridge -> native run
    gs = ds["guide_start"]
    ck("GUIDE-START", gs.get("pack_ok") is True and gs.get("mode") == "PACKAGE_FIRST"
       and (gs.get("delta") or {}).get("candidate_sha") == ds["head"], "GUIDE_START_MISMATCH")
    br = ds["bridge"]
    ck("BRIDGE-READ", br["results"]["inspect_counts"]["mismatched"] == 0
       and br["results"]["explain_cases"] == len(tqaep_spec.SAMPLE)
       and all(br["security"].values()), "BRIDGE_BOUNDARY_FAIL")
    dev = ds["dev"]
    ck("DEV-PREIMAGE", dev["preimage"]["head"] == PRE
       and dev["preimage"]["briefcheck.py"] == ds["v2_blob"], "PREIMAGE_MISMATCH")
    ck("DEV-RED", dev["red"]["exit"] != 0, "RED_MISSING")
    ck("PATCH-DELTA", "briefcheck.py" in ds["patch_text"] and
       dev["patch"]["sha256"] == lib.sha_file(lib.ROOT / "04_DEV_OPS" / "patch_12prime.diff")
       and dev["preimage"]["briefcheck.py"] != ds["v3_file"], "NO_MATERIAL_DELTA")
    ck("RETEST", dev["retest"]["suite_exit"] == 0 and dev["retest"]["probe_exit"] == 0
       and ds["head"] != PRE and ds["v3_file"] != ds["v2_blob"], "RETEST_FAIL")
    # Frozen pre-patch Challenge -> FAR
    ch = ds["chall"]
    ck("CHALLENGE-FROZEN", ch.get("verdict") == "FINDING_CONFIRMED"
       and ch["finding"]["subject_sha"] == PRE, "CHALLENGE_UNBOUND")
    ck("CHALLENGE-RAW", ch["finding"]["raw_sha256"] == ds["red_raw_sha"]
       and ch["finding"]["raw_sha256"] == ds["far"]["finding"].get("raw_sha256"), "RAW_MISMATCH")
    far = ds["far"]
    ck("FAR-CONSUMES", far["finding"]["id"] == ch["finding"]["id"], "FINDING_MISMATCH")
    alts = far.get("alternatives") or []
    ck("FAR-ALTERNATIVES", len(alts) >= 2 and len({a.get("name") for a in alts}) >= 2
       and far.get("chosen") in {a.get("id") for a in alts}, "FAR_ALTERNATIVES")
    # Guide Touch2 consumes the MaterialDelta
    gr = ds["guide_resume"]
    ck("GUIDE-RESUME", gr.get("state") == "RESUME"
       and ch["finding"]["id"] in (gr.get("delta") or {}).get("findings", [])
       and (gr.get("delta") or {}).get("candidate_sha") == ds["head"], "GUIDE_RESUME_MISMATCH")
    ck("GUIDE-EVIDENCE", (gr.get("delta") or {}).get("evidence_sha") == far.get("evidence"),
       "GUIDE_EVIDENCE_MISMATCH")
    ck("SUBJECT", (gr.get("delta") or {}).get("subject_id") == ds["pack"]["manifest"].get("wave_id"),
       "SUBJECT_MISMATCH")
    # Retest bound to the frozen oracle and the actual new candidate
    oracle = ds["oracle"]
    osha = lib.sha_file(lib.TQAEP / "oracle.json")
    ck("ORACLE", bool(oracle.get("frozen_at")) and oracle.get("candidate_commit") == ds["head"]
       and osha == (ds["guide_resume"].get("delta") or {}).get("oracle_sha"),
       "RETEST_ORACLE_DRIFT")
    ck("ORACLE-SOURCE", oracle.get("source_sha256") == lib.sha_file(lib.REPO / "requirements.md"),
       "ORACLE_SOURCE_MISMATCH")
    ck("RETEST-CANDIDATE", (dev.get("commit") or {}).get("head") == ds["head"], "RETEST_CANDIDATE")
    segments = [
        {"from": "SOURCE", "to": "TPM", "pin": pack["sha"]},
        {"from": "TPM", "to": "GUIDE", "pin": lib.canonical_sha(contract_pins)},
        {"from": "GUIDE", "to": "BRIDGE", "pin": gs.get("pack_digest")},
        {"from": "BRIDGE", "to": "NATIVE", "pin": nc.get("context_sha256")},
        {"from": "NATIVE", "to": "CHALLENGE", "pin": ch["finding"]["raw_sha256"]},
        {"from": "CHALLENGE", "to": "FAR", "pin": far["finding"]["id"]},
        {"from": "FAR", "to": "GUIDE-RESUME", "pin": far.get("chosen")},
        {"from": "GUIDE-RESUME", "to": "RETEST", "pin": ds["v3_file"]},
    ]
    return (failure is None, failure, {"checks": checks, "segments": segments})


NEGATIVES = [
    ("missing_raw", lambda d: d["far"]["finding"].__setitem__("raw_sha256", "0" * 64), "RAW_MISMATCH"),
    ("wrong_candidate", lambda d: d["guide_resume"]["delta"].__setitem__("candidate_sha", PRE),
     "GUIDE_RESUME_MISMATCH"),
    ("wrong_oracle", lambda d: d["oracle"].__setitem__("candidate_commit", "0" * 40),
     "RETEST_ORACLE_DRIFT"),
    ("no_challenge", lambda d: d.__setitem__("chall", None), "CHALLENGE_UNBOUND"),
    ("wrong_finding", lambda d: d["far"]["finding"].__setitem__("id", "X"), "FINDING_MISMATCH"),
    ("no_patch_delta", lambda d: d["dev"]["preimage"].__setitem__("briefcheck.py", d["v3_file"]),
     "PREIMAGE_MISMATCH"),
    ("cross_subject", lambda d: d["guide_resume"]["delta"].__setitem__("subject_id", "FHS-5_PLP/W2"),
     "SUBJECT_MISMATCH"),
    ("contracts_not_consumed", lambda d: d["guide_start"].__setitem__("contract_context", None),
     "CONTRACT_CONTEXT_MISSING"),
    ("context_not_consumed",
     lambda d: d["native_ctx"].__setitem__("verdict", "CONTEXT_NOT_CONSUMED"),
     "CONTEXT_NOT_CONSUMED"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["full", "negatives"], default="full")
    ap.add_argument("--out", default=str(OUT / "chain.json"))
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ds = load_dataset()
    ok, code, detail = validate(ds)
    negatives = []
    if a.mode == "negatives":
        for name, mutate, expected in NEGATIVES:
            copy = json.loads(json.dumps(ds))
            mutate(copy)
            nok, ncode, _ = validate(copy)
            negatives.append({"name": name, "expected": expected, "got": ncode,
                              "rejected": not nok and ncode == expected})
        all_rej = all(n["rejected"] for n in negatives)
        out = {"schema": "FHS5.W0NF.CollabNegatives@1", "negatives": negatives,
               "verdict": "NEGATIVES_REJECTED" if all_rej else "NEGATIVE_LEAK",
               "count": len(negatives)}
        lib.write_json(OUT / "chain_negatives.json", out)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if all_rej else 3
    out = {
        "schema": "FHS5.W0NF.CollabChain@1",
        "candidate": ds["head"],
        "pack_sha256": ds["pack"]["sha"],
        "finding": ds["chall"]["finding"]["id"],
        "segments": detail["segments"],
        "checks": detail["checks"],
        "failure_code": None if ok else code,
        "verdict": "COMBINED_OK" if ok else "UNREPRODUCED",
        "not_covered": ["W1-W4 denominators", "other hosts", "different principal"],
    }
    lib.write_json(Path(a.out), out)
    print(json.dumps({"verdict": out["verdict"], "failure": out["failure_code"],
                      "checks": len(detail["checks"]),
                      "failed": [c["id"] for c in detail["checks"] if not c["ok"]]},
                     ensure_ascii=False, indent=2))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
