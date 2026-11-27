#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""N09: one causal chain over the already-produced real artifacts.

contracts -> seven-key work order -> admission -> DEV effect -> OPS effect ->
readback -> recovery -> checker -> consumer.  Every stage must point at a real
file and its SHA; a missing stage fails the chain.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
sys.path.insert(0, str(G3 / "lib"))
import g3pack  # noqa: E402

PACK_BASE = Path(r"C:\Projects\Agent_Workspace\FHS-5_Workspace"
                 r"\FHS-5_PLP_W0-W2_第三代Native-first_執行控制包_FINAL\01_BODY")


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jl(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(G3 / "runs" / "w2" / "raw" / "N09_CHAIN.json"))
    a = ap.parse_args(argv)
    runs = G3 / "runs"
    stages = {}

    def stage(name, refs, ok, detail=None):
        rows = []
        for r in refs:
            p = G3 / r if not Path(r).is_absolute() else Path(r)
            rows.append({"ref": r, "exists": p.is_file(),
                         "sha256": sha_file(p) if p.is_file() else None})
        stages[name] = {"ok": bool(ok) and all(x["exists"] for x in rows),
                        "refs": rows, "detail": detail}

    second = jl(runs / "w1" / "raw" / "SECOND_PACK.json")
    stage("contracts", ["runs/w1/raw/SECOND_PACK.json"],
          second["verdict"] == "PASS" and len(second["packages"]) == 2,
          {"views": second["packages"][1]["views"], "cases": second["packages"][1]["case_count"]})

    pack = g3pack.verify_pack(PACK_BASE / "FHS-5_PLP_W2_NATIVE_FIRST")
    wo_dev = g3pack.select_work_order(pack["pack"], project_id="FHS-5_PLP",
                                      subject_id="FHS-5_PLP/W2", scope="W2-NF-01",
                                      profile="GENERIC_CODEX_NATIVE_FIRST", wave="W2",
                                      operation_id="RUN-DEV-01", case_id="W2-DEV-01")
    wo_ops = g3pack.select_work_order(pack["pack"], project_id="FHS-5_PLP",
                                      subject_id="FHS-5_PLP/W2", scope="W2-NF-01",
                                      profile="GENERIC_CODEX_NATIVE_FIRST", wave="W2",
                                      operation_id="RUN-OPS-01", case_id="W2-OPS-01")
    stage("work_order", ["runs/w2/dev/ws.json"], True,
          {"dev": wo_dev, "ops": wo_ops})

    drv = jl(runs / "w2" / "raw" / "DEV01_driver.json")
    stage("admission", ["runs/w2/raw/DEV01_driver.json"],
          drv["admission"]["ok"] and drv["admission"]["decision_id"] == "W2-G3-OWNER-20261127-05",
          {"decision": drv["admission"]["decision_id"]})

    dev = jl(runs / "w2" / "raw" / "W2-DEV-01.json")["observed"]
    stage("dev_effect", ["runs/w2/raw/W2-DEV-01.json"],
          dev["apply"]["ok"] and dev["post_actual"] == dev["post_expected"],
          {"post": dev["post_actual"]})

    ops = jl(runs / "w2" / "raw" / "W2-OPS-01.json")["observed"]
    stage("ops_effect", ["runs/w2/raw/W2-OPS-01.json", "runs/w2/raw/OPS01_receiver.json"],
          ops["checks"]["exit0"] and ops["seven"]["4_post_world"] != ops["seven"]["2_pre_world"],
          {"pre": ops["seven"]["2_pre_world"], "post": ops["seven"]["4_post_world"]})

    stage("readback", ["runs/w2/raw/OPS01_consumer.json"],
          ops["consumer"]["all_ok"] and dev["checks"]["tests_ok"],
          {"tests": "Ran 8 tests", "consumer": ops["consumer"]["consumer_id"]})

    stage("recovery", ["runs/w2/raw/W2-DEV-01.json"],
          dev["checks"]["reverse_ok"] and dev["restore"]["test_absent"]
          and ops["seven"]["7_pre_state_readback"] == "ABSENT",
          {"dev_restore": dev["restore"]["receiver_sha"],
           "ops_readback": ops["seven"]["7_pre_state_readback"]})

    chk = jl(G3 / "evidence" / "CHECKER.json")
    con = jl(G3 / "evidence" / "W3_CONSUMER.json")
    stage("checker", ["evidence/CHECKER.json"], chk["verdict"] == "PASS",
          {"count": chk["count"]})
    stage("consumer", ["evidence/W3_CONSUMER.json"], con["verdict"] == "ACCEPT",
          {"checks": con["checks"]})

    order = ["contracts", "work_order", "admission", "dev_effect", "ops_effect",
             "readback", "recovery", "checker", "consumer"]
    verdict = "PASS" if all(stages[s]["ok"] for s in order) else "FAIL"
    doc = {"schema": "FHS5.PLP.W2.N09Chain@1", "order": order,
           "stages": stages, "verdict": verdict,
           "first_fail": next((s for s in order if not stages[s]["ok"]), None),
           "note": "orchestration receipt over real artifacts; no new effect"}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": verdict, "first_fail": doc["first_fail"]}))
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
