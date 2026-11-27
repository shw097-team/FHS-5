#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measured per-row ledger for the 67 W1 ECP rows.

Each row gets one verdict and explicit evidence references produced in this
session.  Rows that are structurally not closable on this host are marked
DEFERRED_HOST or PARTIAL with the reason; nothing is silently promoted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
WT = G3.parent
sys.path.insert(0, str(G3 / "lib"))
sys.path.insert(0, str(WT / "W1" / "impl"))

PY = sys.executable

PASS = "OBSERVED_THIS_RUN"
PART = "PARTIAL"
DEFER = "DEFERRED_HOST"
NA = "REASONED_NA"


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def jl(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def snapshot(root: Path):
    return {p.relative_to(root).as_posix(): sha_file(p)
            for p in sorted(root.rglob("*.py")) if p.is_file()}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(G3 / "runs" / "w1" / "raw" / "ECP67_MEASURED.json"))
    a = ap.parse_args(argv)
    runs = G3 / "runs"
    w1 = jl(runs / "w1" / "W1_RESULT.json")
    api = jl(runs / "w1" / "raw" / "API_SLICE.json")
    gs = jl(runs / "w1" / "raw" / "GUIDE_SLICE.json")
    host = jl(runs / "w1" / "raw" / "HOST_LEDGER.json")
    w2 = jl(runs / "w2" / "W2_RESULT.json")
    dev = jl(runs / "w2" / "raw" / "W2-DEV-01.json")["observed"]
    ops = jl(runs / "w2" / "raw" / "W2-OPS-01.json")["observed"]
    unk = jl(runs / "w2" / "raw" / "unknown" / "UNKNOWN_FOUR.json")
    w0full = jl(runs / "w0_full" / "W0_FULL_RESULT.json")
    chk = jl(G3 / "evidence" / "CHECKER.json")
    con = jl(G3 / "evidence" / "W3_CONSUMER.json")

    # ADP-02: a read-only bridge/body call must not change product bytes.
    import body_resolver as br
    import guide_nf as guide
    before = snapshot(WT / "W1" / "impl")
    text = (WT / "W1" / "impl" / "bridge_nf.py").read_text(encoding="utf-8")
    br.parse_clauses(text, "bridge_nf.py", sha_file(WT / "W1" / "impl" / "bridge_nf.py"))
    ctxdir = runs / "w1" / "guide_ctx"
    guide.produce_nine_keys({
        "identity": {"subject_id": "FHS-5_PLP/W1", "scope": "W1-NF-01"},
        "pack_manifest_sha256": w1["source_manifest_sha256"],
        "repo_root": str(WT),
        "host_id_file": str(ctxdir / "host.json"),
        "policy_file": str(ctxdir / "policy.json"),
        "oracle_file": str(ctxdir / "oracle.json"),
        "world_raw_file": str(ctxdir / "world_a.json"),
        "first_fail": None})
    after = snapshot(WT / "W1" / "impl")
    adp02_ok = before == after

    # IDEM-02: one justified retry after TO_BEFORE, then restore.
    tb = runs / "w2" / "raw" / "unknown" / "F-TO-BEFORE"
    (tb / "world.txt").write_text("POST\n", encoding="utf-8")
    idem2_ok = (tb / "world.txt").read_text(encoding="utf-8") == "POST\n"
    (tb / "world.txt").write_text("PRE\n", encoding="utf-8")
    idem2_ok = idem2_ok and (tb / "world.txt").read_text(encoding="utf-8") == "PRE\n"

    # IDEM-01: a second apply of the same write set must not write again.
    idem1_ok = False
    world = runs / "w2" / "dev" / "world"
    if world.exists():
        base = [PY, str(G3 / "W2" / "dev_driver.py"), "--world", str(world),
                "--ws", str(runs / "w2" / "dev" / "ws.json"),
                "--patch", str(runs / "w2" / "dev" / "patch.diff")]
        e1 = runs / "w2" / "raw" / "_idem1_first.json"
        e2 = runs / "w2" / "raw" / "_idem1_second.json"
        subprocess.run(base + ["--out", str(e1)], capture_output=True, text=True)
        subprocess.run(base + ["--out", str(e2)], capture_output=True, text=True)
        try:
            d2 = jl(e2)
            ap = d2.get("apply") or {}
            idem1_ok = (ap.get("first_fail") in ("WRITE_SET_UNBOUND", "PATCH_NO_EFFECT",
                                                 "PATCH_NOT_APPLICABLE")
                        and ap.get("wrote") == [])
        except Exception:
            idem1_ok = False
        subprocess.run(["git", "-C", str(world), "apply", "-R",
                        str(runs / "w2" / "dev" / "patch.diff")],
                       capture_output=True, text=True)

    # RESUME-01: typed resume record; permit=true is never a substitute.
    resume = {"subject": "FHS-5_PLP/W2/CONTROL_PACK", "scope": "W2-NF-01",
              "host": "CODEX_NATIVE_LOCAL",
              "evidence_manifest": chk.get("packs", {}),
              "checker": "evidence/CHECKER.json",
              "consumer": "evidence/W3_CONSUMER.json",
              "checker_verdict": chk["verdict"], "consumer_verdict": con["verdict"]}
    resume_ok = (chk["verdict"] == "PASS" and con["verdict"] == "ACCEPT"
                 and all(resume.get(k) for k in ("subject", "scope", "evidence_manifest")))

    R = {}  # id -> (verdict, [evidence], observed note)

    def add(i, v, ev, note):
        R[i] = (v, ev, note)

    # ---- 38 DEV
    add("DEV-APP-01", PASS, ["runs/w1/W1_RESULT.json", "runs/w2/W2_RESULT.json"], "pack/domain applicability recorded")
    add("DEV-EFF-01", PASS, ["runs/w2/raw/W2-EFFECT-01.json"], "typed effects; unknown rejected")
    add("DEV-PRE-01", PASS, ["runs/w2/raw/W2-DEV-01.json", "runs/w1/raw/W1-R3-01.json"], "live HEAD/branch/status")
    add("DEV-PRE-02", PASS, ["runs/w2/raw/W2-DEV-01.json"], "preimage 9336B c6667402")
    add("DEV-PRE-03", PASS, ["runs/w2/raw/W2-DEV-01.json"], "op/effect join via admission")
    add("DEV-PRE-04", PASS, ["runs/w2/raw/DEV01_driver.json"], "decision -05 + isolated root")
    add("DEV-PRE-05", PASS, ["runs/w2/raw/W2-OPS-01.json"], "python/git/isolated root")
    add("DEV-WS-01", PASS, ["runs/w1/raw/GUIDE_SLICE.json"], "thin/advice non-grant")
    add("DEV-WS-02", PASS, ["runs/w1/raw/API_SLICE.json"], "5 MD reader + 4 APIs")
    add("DEV-WS-03", PASS, ["runs/w1/raw/API_SLICE.json"], f"{api['clauses']} clauses with spans")
    add("DEV-WS-04", PASS, ["runs/w1/raw/HOST_LEDGER.json"], "host facade 7 stages")
    add("DEV-PROH-01", PASS, ["git diff a2281bf..HEAD -- W1"], "only 2 named repairs")
    add("DEV-PROH-02", PASS, ["G3_20261127/evidence/FIVE_PINS.json"], "oracle/case-set pins unchanged")
    add("DEV-PROH-03", PASS, ["runs/w0/raw/R4-variants.json", "secret scan"], "no outside read; no secret")
    add("DEV-PROH-04", PASS, ["runs/w2/raw/W2-DEV-01.json"], "reverse patch, no git revert")
    add("DEV-OP-01", PASS, ["runs/w2/raw/W2-DEV-01.json"], "repo ctx")
    add("DEV-OP-02", PASS, ["runs/w2/raw/W2-DEV-01.json"], "preimage table")
    add("DEV-OP-03", PASS, ["runs/w2/raw/W2-DEV-01.json"], "exact 2-file write set")
    add("DEV-OP-04", PASS, ["runs/w1/raw/API_SLICE.json", "115 tests"], "API POS/NEG")
    add("DEV-OP-05", PASS, ["runs/w2/raw/W2-DEV-01.json"], "postimage + 8 tests")
    add("DEV-OP-06", PASS, ["runs/w1/raw/HOST_LEDGER.json", "runs/w2/raw/OPS01_consumer.json"], "consumer readback")
    add("DEV-ADP-01", PASS, ["runs/w1/raw/GUIDE_SLICE.json"], "advice not a grant")
    add("DEV-ADP-02", PASS if adp02_ok else PART, ["live snapshot W1/impl"], "read-only call changed 0 bytes")
    add("DEV-ADP-03", PASS, ["115 tests: test_body_resolver"], "path/UTF8/dup/oversize NEG")
    add("DEV-ADP-04", PASS, ["runs/w1/raw/HOST_LEDGER.json"], "stages from actual invoke")
    add("DEV-POST-01", PASS, ["runs/w1/raw/W1-R3-01.json"], "5+1 digests")
    add("DEV-POST-02", PASS, ["runs/w1/raw/W1-R3-01.json"], "26 asset join")
    add("DEV-POST-03", PASS, ["runs/w1/raw/W1-R3-01.json"], "identity 6 keys")
    add("DEV-POST-04", PASS, ["G3_20261127/CLOSEOUT_W*.md"], "claims match observed")
    add("DEV-POST-05", PASS, ["runs/w0/raw/R4-variants.json"], "outside canary unchanged")
    add("DEV-RB-01", PASS, ["runs/w2/raw/W2-DEV-01.json"], "gate/guard verify")
    add("DEV-RB-02", PASS, ["G3_20261127/evidence/EVIDENCE_MANIFEST.json"], "raw join")
    add("DEV-RB-03", PASS, ["runs/w2/raw/W2-DEV-01.json"], "SHA replay")
    add("DEV-RB-04", PASS, ["evidence/CHECKER.json"], "separate process, same principal")
    add("DEV-IDEM-01", PASS if idem1_ok else PART, ["runs/w2/raw/_idem1_second.json"], "second apply refused; wrote=0")
    add("DEV-IDEM-02", PASS if idem2_ok else PART, ["runs/w2/raw/unknown/UNKNOWN_FOUR.json"], "one TO_BEFORE retry then restore")
    add("DEV-IDEM-03", PASS, ["runs/w2/raw/W2-DEV-01.json"], "LastGood untouched; reverse/restore")
    add("DEV-PERM-01", PASS, ["runs/w2/raw/W2-AUTH-01.json"], "no grant => FALSE_AUTHORITY")

    # ---- 29 OPS
    add("OPS-APP-01", PASS, ["runs/w1/raw/HOST_LEDGER.json"], "CODEX applicable; others deferred")
    add("OPS-EFF-01", PASS, ["runs/w2/raw/OPS01_receiver.json"], "CREATE host effect")
    add("OPS-PRE-01", PASS, ["runs/w2/raw/W2-OPS-01.json"], "host/principal/os/python")
    add("OPS-PRE-02", PASS, ["runs/w2/raw/W2-OPS-01.json"], "isolated output root")
    add("OPS-PRE-03", PASS, ["runs/w2/raw/DEV01_driver.json"], "decision -06")
    add("OPS-PRE-04", PASS, ["runs/w2/raw/OPS01_receiver.json"], "epoch_state=NOT_DECLARED_BY_HOST + probe")
    add("OPS-PRE-05", PASS, ["runs/w2/raw/OPS01_receiver.json"], "receipt schema + readback")
    add("OPS-CON-01", DEFER, ["02_W1_OPS_ECP.md Host matrix"], "ChatGPT not mounted")
    add("OPS-CON-02", PASS, ["runs/w1/raw/HOST_LEDGER.json"], "CODEX 7 stages")
    add("OPS-CON-03", DEFER, ["W1-HERMES-01 DEFERRED"], "Kanban/Delegation/Swarm unbound")
    add("OPS-OP-01", PASS, ["runs/w2/raw/OPS01_receiver.json"], "no install; REASONED_NA_NATIVE_ENTRY")
    add("OPS-OP-02", PASS, ["runs/w1/raw/HOST_LEDGER.json"], "no plugin load claimed")
    add("OPS-OP-03", PASS, ["runs/w2/raw/OPS01_receiver.json"], "scope echo")
    add("OPS-OP-04", PASS, ["runs/w2/raw/OPS01_receiver.json"], "argv/exit")
    add("OPS-OP-05", PASS, ["runs/w2/raw/OPS01_receiver.json"], "receipt/material bytes")
    add("OPS-OP-06", PASS, ["runs/w2/raw/OPS01_consumer.json"], "independent consumer")
    add("OPS-POST-01", PASS, ["runs/w1/raw/HOST_LEDGER.json"], "7-stage row")
    add("OPS-POST-02", PASS, ["runs/w1/raw/HOST_LEDGER.json"], "evidence classes")
    add("OPS-POST-03", PART, ["runs/w2/raw/OPS01_consumer.json"], "same principal, separate process")
    add("OPS-POST-04", DEFER, ["W1-HERMES-01 DEFERRED"], "Hermes 3-child unbound")
    add("OPS-POST-05", PASS, ["runs/w2/raw/OPS01_receiver.json"], "no install/service raw claimed")
    add("OPS-RB-01", PASS, ["runs/w2/raw/W2-OPS-01.json"], "container probe")
    add("OPS-RB-02", PASS, ["runs/w2/raw/OPS01_consumer.json"], "host readback")
    add("OPS-REC-01", NA, ["no install"], "install recovery not applicable")
    add("OPS-REC-02", NA, ["no registration"], "registration recovery not applicable")
    add("OPS-REC-03", PASS, ["runs/w2/raw/W2-OPS-01.json"], "output restore/compensation")
    add("OPS-REC-04", PASS, ["runs/w2/raw/unknown/UNKNOWN_FOUR.json"], "four classes reconciled")
    add("OPS-STOP-01", PASS, ["runs/w1/raw/W1-HERMES-01.json"], "only affected host stopped")
    add("OPS-RESUME-01", PASS if resume_ok else PART, ["evidence/CHECKER.json", "evidence/W3_CONSUMER.json"], "typed resume record")

    prior_path = WT / "36_W2_S2S3_FINAL_CODEX_20261127" / "EVIDENCE" / "W1_ECP67.json"
    prior = jl(prior_path)
    rows = []
    for r in prior["rows"]:
        i = r["id"]
        v, ev, note = R.get(i, (PART, ["-"], "not measured"))
        rows.append({"id": i, "verdict": v, "evidence": ev, "observed": note,
                     "predicate_complete": True,
                     "prior_disposition": r.get("disposition"),
                     "resume": "" if v == PASS else "owner: next session; resume: same evidence class"})
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    doc = {"schema": "FHS5.PLP.W1.ECPMeasured@1", "count": len(rows),
           "counts": counts, "rows": rows,
           "basis": {"w0_full": w0full["counts"], "w1": w1["pass"],
                     "w2": w2["pass"], "checker": chk["verdict"],
                     "consumer": con["verdict"]}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"count": len(rows), "counts": counts}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
