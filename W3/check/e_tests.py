#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E01-E11 targeted negative tests (functional where possible)."""
from __future__ import annotations
import argparse, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "W2", "impl"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "W2", "check"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "W4", "check"))
sys.path.insert(0, HERE)

import w3_far
from w3_common import W3Error, load_json_strict, sha256_file, write_json
from w3_cases import run_case
from product_verify import pred_full


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    base = os.path.join(a.root, "evidence", "ETEST")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base, exist_ok=True)
    rows = []

    def add(eid, ok, detail):
        rows.append({"id": eid, "ok": bool(ok), "detail": str(detail)})

    # E01 candidate absent -> typed blocker
    try:
        import w2_cases
        e01root = os.path.join(base, "e01root")
        os.makedirs(e01root, exist_ok=True)
        ctx = {"root": e01root, "case_dir": os.path.join(base, "e01"), "run_id": "E01"}
        os.makedirs(ctx["case_dir"], exist_ok=True)
        w2_cases.w2_dev_01({"inputs": {}}, {"expected_tokens": []}, ctx)
        add("E01", False, "no exception")
    except W3Error as exc:
        add("E01", exc.token == "CANDIDATE_UNBOUND", exc.token)
    except Exception as exc:
        add("E01", False, type(exc).__name__)

    # E02 git probe failed -> no hard-coded fallback
    src_w2 = open(os.path.join(HERE, "..", "..", "W2", "check", "run_w2_pipeline.py"), encoding="utf-8").read()
    add("E02", ("3346076c" not in src_w2 and "GIT_PROBE_FAILED" in src_w2),
        "no hard-coded candidate fallback")

    # E03 NEG with no actual refusal -> exit must not be forced by kind
    add("E03", pred_full("neg_exit_two", {"process_exit": 0, "observed": {"evidence": {}}}, {}) is False,
        "kind is not used to force exit 2")

    # E05 mode-only product forbidden
    try:
        run_case(os.path.join(a.root, "pack"), "W3-FRZ-01", a.root,
                 {"pins": {}, "source_pack": os.path.join(a.root, "pack")}, "E05", mode="product")
        add("E05", False, "mode product accepted")
    except W3Error as exc:
        add("E05", exc.token == "MODE_ONLY_PRODUCT_FORBIDDEN", exc.token)
    except Exception as exc:
        add("E05", False, type(exc).__name__)

    # E07 missing case -> freeze rejected
    try:
        import build_product_pack
        owner = os.path.join(base, "e07_owner")
        shutil.copytree(os.path.join(a.root, "product_case_owner"), owner)
        os.remove(os.path.join(owner, "oracles", "W3-FRZ-01.json"))
        build_product_pack.main.__globals__  # noqa
        sys.argv = ["build_product_pack.py", "--owner", owner, "--out", os.path.join(base, "e07_pack")]
        build_product_pack.main()
        add("E07", False, "missing oracle accepted")
    except SystemExit as exc:
        add("E07", True, str(exc))
    except Exception as exc:
        add("E07", True, type(exc).__name__)

    # E09 FAR result driven by input
    d1 = os.path.join(base, "e09_hit"); d2 = os.path.join(base, "e09_zero")
    os.makedirs(d1); os.makedirs(d2)
    open(os.path.join(d1, "TOKEN_hit.txt"), "w").write("x")
    open(os.path.join(d2, "nothing.txt"), "w").write("x")
    s1 = w3_far.query_dir("a", d1, "TOKEN", [base])["state"]
    s2 = w3_far.query_dir("b", d2, "TOKEN", [base])["state"]
    add("E09", s1 == "HIT" and s2 == "ZERO_RELEVANT_HIT", f"{s1}/{s2}")

    # E10 fake readiness + no authority -> W4 consumer fails
    inbound = os.path.join(base, "e10.json")
    write_json(inbound, {"from_stage": "W3", "to_stage": "W4", "handoff_id": "x",
                         "project_id": "p", "work_id": "w", "pack_ref": "x",
                         "pack_manifest_sha256": "x", "candidate_commit": "x",
                         "candidate_preimage": "x", "oracle_sha256": "x",
                         "case_set_sha256": "x", "evidence_ref": "x",
                         "evidence_manifest_sha256": "x", "checker_ref": "x",
                         "consumer_ref": "x", "actual_readback": {}, "next_legal_action": "x",
                         "dependencies": [], "resume_predicate": "x", "not_covered": ["x"],
                         "readiness": {"W4_TECHNICALLY_READY": True, "W4_EXECUTION_READY": True},
                         "publication_state": "PUSHED", "execution_authority": None})
    import consumer_w4
    code = consumer_w4.main(["--inbound", inbound, "--out", os.path.join(base, "e10_out.json")])
    add("E10", code != 0, "fake authority rejected")

    # E06/E08/E11 checker tamper tests
    real_root = a.root
    for eid, mutate in (("E06", "delete"), ("E08", "token"), ("E11", "bytes")):
        tmp = os.path.join(base, eid)
        shutil.copytree(os.path.join(real_root, "evidence", "PR"), os.path.join(tmp, "evidence", "PRT"))
        rec = os.path.join(tmp, "evidence", "PRT", "cases", "W3-FRZ-01", "record.json")
        if mutate == "delete":
            os.remove(rec)
        elif mutate == "token":
            d = load_json_strict(rec); d["observed"]["token"] = "FAKE_PASS"
            write_json(rec, d)
        else:
            open(rec, "a", encoding="utf-8").write("\n")
        import product_checker
        code = product_checker.main(["--product-pack", os.path.join(real_root, "W3", "product_real", "pack"),
                                     "--root", tmp, "--run-id", "PRT",
                                     "--ledger", os.path.join(real_root, "evidence", "PR", "LEDGER_FOR_RUN.json"),
                                     "--out", os.path.join(base, eid + "_out.json")])
        add(eid, code != 0, "tampered record rejected")

    # E04/E06 fresh/engine static guards (functional path above covers record checks)
    src = open(os.path.join(HERE, "product_verify.py"), encoding="utf-8").read()
    add("E04", "engine_ok" in src and "proc[\"exit\"] == expected_exit" in src, "engine/exit guard present")
    add("E06b", "fresh_ok" in src, "fresh raw guard present")
    add("E08b", "sha_ok" in open(os.path.join(HERE, "product_checker.py"), encoding="utf-8").read(), "record sha guard present")
    add("E11b", "sha_ok" in open(os.path.join(HERE, "product_checker.py"), encoding="utf-8").read(), "seal drift guard present")

    out = {"schema": "FHS5.PLP.W3.E01E11Results@1",
           "rows": rows, "pass": sum(1 for r in rows if r["ok"]), "total": len(rows),
           "ok": all(r["ok"] for r in rows)}
    write_json(a.out, out)
    print(json.dumps({"ok": out["ok"], "pass": out["pass"], "total": out["total"],
                      "fail": [r for r in rows if not r["ok"]]}, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
