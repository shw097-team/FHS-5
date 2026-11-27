#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent checker for the G3 W0/W1/W2 run.

It reads the frozen packs, the runner raws and the result files, then re-derives
the predicates it can check without trusting a runner boolean.  It writes
CHECKER.json and never edits a raw or a pack.
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
import g3pack  # noqa: E402

PY = sys.executable
PACK_BASE = Path(r"C:\Projects\Agent_Workspace\FHS-5_Workspace"
                 r"\FHS-5_PLP_W0-W2_第三代Native-first_執行控制包_FINAL\01_BODY")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha(Path(p).read_bytes())


def jl(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def check(name, ok, detail=""):
    return {"check": name, "ok": bool(ok), "detail": str(detail)[:400]}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=str(G3 / "runs"))
    ap.add_argument("--out", default=str(G3 / "evidence" / "CHECKER.json"))
    a = ap.parse_args(argv)
    runs = Path(a.runs)
    checks = []

    packs = {}
    for w in ("W0", "W1", "W2"):
        v = g3pack.verify_pack(PACK_BASE / f"FHS-5_PLP_{w}_NATIVE_FIRST")
        packs[w] = v
        checks.append(check(f"pack_{w}_verify", v["ok"], v["errors"][:3]))
        checks.append(check(f"pack_{w}_cases", v["counts"]["cases"] in
                            ({"W0": 44, "W1": 13, "W2": 12}[w],),
                            v["counts"]))
        checks.append(check(f"pack_{w}_manifest_sha", v["manifest_sha256"] in {
            "W0": "baa516b5675589c1a329cd5f65970d8d6c12b7892dd7c079115e1251c9e6e96d",
            "W1": "f00b4ee93611e738e409d40758aa320b0bfec3ef0a01fea04dbf5bcb9f1566dc",
            "W2": "7bdc4a0acb497944450d89a2c347d26ca4ac8593f6ee47ac229215a80ff227e0",
        }[w], v["manifest_sha256"][:12]))

    # ---- W0
    w0 = jl(runs / "w0" / "W0_RESULT.json")
    checks.append(check("w0_10_of_10", w0["samples"]["pass"] == 10, w0["samples"]["pass"]))
    oracle = g3pack.strict_json((packs["W0"]["pack"].root / "assets" / "oracles" /
                                 "W0_SAMPLE_ORACLE.json").read_bytes(), "oracle")
    exp = {c["case_id"]: c["expect"] for c in oracle["cases"]}
    for row in w0["samples"]["rows"]:
        raw = jl(runs / "w0" / row["raw"].replace("/", "\\"))
        e = exp[row["case_id"]]
        ok = (raw["exit"] == e["exit"]
              and (raw.get("parsed") or {}).get("status") == e["status"])
        checks.append(check(f"w0_{row['case_id']}", ok and raw["verdict"] == "PASS",
                            {"exit": raw["exit"], "status": (raw.get("parsed") or {}).get("status")}))
    r4 = jl(runs / "w0" / "raw" / "R4-variants.json")
    checks.append(check("w0_r4_variants", r4["verdict"] == "PASS" and r4["canary_sha_before"] == r4["canary_sha_after"],
                        {"junction": r4.get("junction_created"), "n": len(r4["variants"])}))
    r10 = jl(runs / "w0" / "raw" / "R10-output.json")
    checks.append(check("w0_r10_output", r10["verdict"] == "PASS" and r10["source_sha_before"] == r10["source_sha_after"],
                        r10.get("output")))
    led = jl(runs / "w0" / "raw" / "receipts-44.json")
    checks.append(check("w0_receipts_44", led["count"] == 44 and led["all_verified"],
                        led["cohorts"]))
    off = jl(runs / "w0" / "raw" / "OFF.json")
    checks.append(check("w0_off_positive_control", off["verdict"] == "PASS"
                        and off["positive_control"]["exit"] != 0
                        and off["off_run"]["exit"] == 0, off.get("blocked_imports")))

    # ---- W1
    w1 = jl(runs / "w1" / "W1_RESULT.json")
    checks.append(check("w1_12_pass_1_deferred", w1["pass"] == 12 and w1["deferred"] == 1,
                        {"pass": w1["pass"], "deferred": w1["deferred"]}))
    api = jl(runs / "w1" / "raw" / "API_SLICE.json")
    checks.append(check("w1_api_full_body", api["files"] == 5 and api["clauses"] > 0
                        and api["negatives"] > 0 and api["all_have_span"],
                        {"clauses": api["clauses"], "negatives": api["negatives"],
                         "exceptions": api["exceptions"]}))
    gs = jl(runs / "w1" / "raw" / "GUIDE_SLICE.json")
    checks.append(check("w1_guide_two_periods", gs["pass"] and gs["same"] == "PARK_NO_DELTA"
                        and gs["delta"] == "NEW_MATERIAL_EVIDENCE"
                        and gs["missing"] == "DELTA_UNVERIFIED", gs))
    host = jl(runs / "w1" / "raw" / "HOST_LEDGER.json")
    checks.append(check("w1_host_consumed", host["rows"]["CODEX"]["Consumed"] == "OBSERVED_LOCAL",
                        host["rows"]["CODEX"]))
    suite = subprocess.run([PY, "-m", "unittest", "discover", "-s", "W1\\check",
                            "-p", "test_*.py"], cwd=str(WT), capture_output=True,
                           text=True, errors="replace")
    ran = [ln for ln in suite.stderr.splitlines() if ln.startswith("Ran ")]
    n = int(ran[0].split()[1]) if ran else 0
    checks.append(check("w1_suite_115", suite.returncode == 0 and n == 115, ran[-1:] or ""))


    # ---- W2 (protected effects are NOT_ADMITTED; fail-closed is the predicate)
    w2 = jl(runs / "w2" / "W2_RESULT.json")
    checks.append(check("w2_9_pass_3_not_admitted",
                        w2["pass"] == 9 and w2.get("not_admitted") == 3
                        and w2["verdict"] == "NOT_ADMITTED",
                        {"pass": w2["pass"], "not_admitted": w2.get("not_admitted")}))
    dev = jl(runs / "w2" / "raw" / "W2-DEV-01.json")
    ob = dev["observed"]
    drv = jl(runs / "w2" / "raw" / "DEV01_driver.json")
    checks.append(check("w2_dev_fail_closed",
                        dev["verdict"] == "NOT_ADMITTED"
                        and (drv.get("error") or {}).get("token") == "NOT_ADMITTED"
                        and ob["post_actual"] == {}
                        and ob["restore"]["receiver_sha"] == ob["preimage"]["sha256"],
                        {"error": (drv.get("error") or {}).get("token"),
                         "post": ob["post_actual"]}))
    ops = jl(runs / "w2" / "raw" / "W2-OPS-01.json")
    ob2 = ops["observed"]
    checks.append(check("w2_ops_fail_closed",
                        ops["verdict"] == "NOT_ADMITTED"
                        and ob2["checks"].get("exit0") is False
                        and ob2["seven"]["4_post_world"] == ob2["seven"]["2_pre_world"],
                        {"exit0": ob2["checks"].get("exit0"),
                         "pre": ob2["seven"]["2_pre_world"],
                         "post": ob2["seven"]["4_post_world"]}))
    world = runs / "w2" / "dev" / "world"
    dec = world / "W1" / "authority" / "decisions" / "DEV.json"
    if dec.is_file():
        d = jl(dec)
        checks.append(check("w2_no_self_issued_grant",
                            d.get("grant_state") == "REQUEST_ONLY"
                            and d.get("issuer_state") == "PENDING_EXTERNAL_ISSUER",
                            {"grant_state": d.get("grant_state")}))
    checks.append(check("w2_non_effect_cases",
                        all(c["verdict"] == "PASS" for c in w2["cases"]
                            if c["case_id"] not in ("W2-DEV-01", "W2-DEV-02", "W2-OPS-01"))))

    # ---- full W0 44, measured ECP, second pack, UNKNOWN, N09
    w0full = jl(runs / "w0_full" / "W0_FULL_RESULT.json")
    checks.append(check("w0_full_state", w0full["counts"]["total"] == 44
                        and w0full["counts"]["pass"] == 41
                        and w0full["counts"]["fail"] == 2
                        and w0full["counts"]["pending"] == 1
                        and {f["case"] for f in w0full["failures"]} == {"NF-T01", "NF-T08"}
                        and w0full["verdict"] == "PARTIAL", w0full["counts"]))
    checks.append(check("w0_full_consumer", w0full["consumer"]["consumed"] is False
                        and w0full["consumer"]["failure_code"] == "RECEIPT_VERDICT"
                        and "RECEIPT-NF-T01" in w0full["consumer"]["failed"],
                        w0full["consumer"]))
    checks.append(check("w0_lineage", w0full["lineage"]["sealed_pack_manifest"]
                        == w0full["lineage"]["actual_pack_manifest"]
                        == "e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8"
                        and w0full["lineage"]["g3_control_manifest"] !=
                        w0full["lineage"]["sealed_pack_manifest"],
                        w0full["lineage"]))
    ecp = jl(runs / "w1" / "raw" / "ECP67_MEASURED.json")
    checks.append(check("w1_ecp67_measured", ecp["count"] == 67
                        and sum(ecp["counts"].values()) == 67
                        and ecp["counts"].get("OBSERVED_THIS_RUN", 0) >= 50
                        and ecp["counts"].get("NOT_ADMITTED", 0) >= 10,
                        ecp["counts"]))
    second = jl(runs / "w1" / "raw" / "SECOND_PACK.json")
    checks.append(check("w1_second_pack", second["verdict"] == "PASS"
                        and second["distinct"]
                        and second["packages"][1]["case_count"] == 12,
                        second["packages"][1]["views"]))
    unk = jl(runs / "w2" / "raw" / "unknown" / "UNKNOWN_FOUR.json")
    checks.append(check("w2_unknown_four", unk["verdict"] == "PASS"
                        and len(set(unk["classes"].values())) == 4, unk["classes"]))
    n09 = jl(runs / "w2" / "raw" / "N09_CHAIN.json")
    checks.append(check("w2_n09_chain", n09["verdict"] == "NOT_ADMITTED"
                        and n09["first_fail"] == "NOT_ADMITTED",
                        n09["first_fail"]))

    # no PASS with a first_fail, no FAIL counted as PASS
    for w in ("w0", "w1", "w2"):
        for res in runs.joinpath(w).glob("*_RESULT.json"):
            d = jl(res)
            rows = d.get("cases") or (d.get("samples") or {}).get("rows") or []
            bad = [r for r in rows if r.get("verdict") == "PASS" and r.get("first_fail")]
            checks.append(check(f"{w}_pass_with_first_fail", not bad, bad[:2]))

    failed = [c["check"] for c in checks if not c["ok"]]
    verdict = "PASS" if not failed else "FAIL"
    doc = {"schema": "FHS5.PLP.G3.Checker@1",
           "verdict": verdict,
           "checks": checks,
           "failed": failed,
           "count": len(checks),
           "packs": {w: {"manifest_sha256": packs[w]["manifest_sha256"],
                         "tree_sha256": packs[w]["tree_sha256"],
                         "case_set_sha256": packs[w]["case_set_sha256"]}
                     for w in packs},
           "checker_id": "g3-checker-separate-process-20261127",
           "principal_scope": "SEPARATE_PROCESS_SAME_PRINCIPAL",
           "note": ("checker re-derives predicates from packs/raws and does not trust runner verdicts; "
                    "it is a separate process but the same OS principal, so this is NOT INDEPENDENT_PASS")}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": verdict, "count": len(checks), "failed": failed[:5]}))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
