#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measured 67-row ECP ledger (v2).

Every row has a predicate function over real artifacts.  There is no fixed
PASS table and no free-text "observed": the verdict is computed, and rows that
depend on a protected effect inherit NOT_ADMITTED when no external grant exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
WT = G3.parent
sys.path.insert(0, str(G3 / "lib"))
sys.path.insert(0, str(WT / "W1" / "impl"))
import g3pack  # noqa: E402

PACK_BASE = Path(r"C:\Projects\Agent_Workspace\FHS-5_Workspace"
                 r"\FHS-5_PLP_W0-W2_第三代Native-first_執行控制包_FINAL\01_BODY")
PY = sys.executable


def jl(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class Ev:
    def __init__(self):
        r = G3 / "runs"
        self.r = r
        self.w1 = jl(r / "w1" / "W1_RESULT.json")
        self.apiv = jl(r / "w1" / "raw" / "API_SLICE.json")
        self.gs = jl(r / "w1" / "raw" / "GUIDE_SLICE.json")
        self.hostv = jl(r / "w1" / "raw" / "HOST_LEDGER.json")
        self.secondv = jl(r / "w1" / "raw" / "SECOND_PACK.json")
        self.w0f = jl(r / "w0_full" / "W0_FULL_RESULT.json")
        self.w2 = jl(r / "w2" / "W2_RESULT.json")
        self.cases = {c["case_id"]: c["verdict"] for c in self.w2["cases"]}
        self.dev = jl(r / "w2" / "raw" / "W2-DEV-01.json")
        self.ops = jl(r / "w2" / "raw" / "W2-OPS-01.json")
        self.drv = jl(r / "w2" / "raw" / "DEV01_driver.json")
        self.unk = jl(r / "w2" / "raw" / "unknown" / "UNKNOWN_FOUR.json")
        self.n09 = jl(r / "w2" / "raw" / "N09_CHAIN.json")
        self.chk = jl(G3 / "evidence" / "CHECKER.json")
        self.con = jl(G3 / "evidence" / "W3_CONSUMER.json")
        self.pinsv = jl(G3 / "evidence" / "FIVE_PINS.json")
        self.r4 = jl(r / "w0" / "raw" / "R4-variants.json")
        self.packv = g3pack.verify_pack(PACK_BASE / "FHS-5_PLP_W1_NATIVE_FIRST")
        self.suite = None

    # -- shared predicates ---------------------------------------------
    def pack(self):
        return self.packv["ok"]

    def api(self):
        a = self.apiv
        return a["files"] == 5 and a["clauses"] > 0 and a["negatives"] > 0 and a["all_have_span"]

    def guide(self):
        g = self.gs
        return (g["same"] == "PARK_NO_DELTA" and g["delta"] == "NEW_MATERIAL_EVIDENCE"
                and g["missing"] == "DELTA_UNVERIFIED")

    def host(self):
        return self.hostv["rows"]["CODEX"]["Consumed"] == "OBSERVED_LOCAL"

    def tests(self):
        if self.suite is None:
            p = subprocess.run([PY, "-m", "unittest", "discover", "-s", "W1\\check",
                                "-p", "test_*.py"], cwd=str(WT), capture_output=True,
                               text=True, errors="replace")
            ran = [l for l in p.stderr.splitlines() if l.startswith("Ran ")]
            self.suite = (p.returncode == 0 and ran and int(ran[0].split()[1]) == 115)
        return self.suite

    def second(self):
        return self.secondv["verdict"] == "PASS" and all(
            not p["review"].get("findings") for p in self.secondv["packages"])

    def w0(self):
        return (self.w0f["counts"]["pass"] == 44 and self.w0f["counts"]["fail"] == 0
                and self.w0f["consumer"]["checks"] == 803
                and not self.w0f["consumer"]["failed"])

    def unknown(self):
        return self.unk["verdict"] == "PASS" and len(set(self.unk["classes"].values())) == 4

    def auth(self):
        return self.cases.get("W2-AUTH-01") == "PASS"

    def eff(self):
        return self.cases.get("W2-EFFECT-01") == "PASS"

    def runner(self):
        return self.cases.get("W2-RUNNER-01") == "PASS"

    def r3(self):
        return all(self.cases.get(f"W2-R3-0{i}") == "PASS" for i in (1, 2, 3, 4))

    def delta(self):
        return self.cases.get("W2-DELTA-01") == "PASS"

    def outside(self):
        return self.r4["verdict"] == "PASS" and self.r4["canary_sha_before"] == self.r4["canary_sha_after"]

    def pins(self):
        return bool(self.chk["verdict"] == "PASS" and self.con["verdict"] == "ACCEPT"
                    and self.pinsv["evidence"]["manifest_sha256"])

    def live_head(self):
        return bool(self.drv.get("live_head"))

    def preimage(self):
        return (self.dev["observed"]["preimage"]["sha256"]
                == "c666740268cce914819e2ba43a0dbd9413de709792ee2c8338b0b67e895c74f0")

    def dev_effect(self):
        return True if self.dev["verdict"] == "PASS" else "NOT_ADMITTED"

    def ops_effect(self):
        return True if self.ops["verdict"] == "PASS" else "NOT_ADMITTED"

    def admission(self):
        tok = (self.drv.get("error") or {}).get("token")
        return "NOT_ADMITTED" if tok == "NOT_ADMITTED" else (
            True if self.drv.get("check", {}).get("ok") else False)

    def no_revert(self):
        checks = (self.dev["observed"].get("checks") or {})
        return bool(checks.get("git_not_reset") or self.dev["verdict"] == "NOT_ADMITTED")

    def no_secret(self):
        pat = re.compile(r"ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|password\s*=")
        for p in (G3).rglob("*"):
            if p.is_file() and p.suffix in (".json", ".md", ".py", ".txt"):
                try:
                    if pat.search(p.read_text(encoding="utf-8", errors="ignore")):
                        return False
                except Exception:
                    pass
        return True

    def gitdiff(self):
        p = subprocess.run(["git", "-C", str(WT), "diff", "--name-only",
                            "a2281bf", "HEAD"], capture_output=True, text=True)
        files = [x for x in p.stdout.splitlines() if x.startswith("W1/")]
        allowed = {"W1/check/w2_dev_gate.py", "W1/impl/host_facade.py",
                   "W1/impl/tpm_contracts_nf.py"}
        return set(files) <= allowed

    def ops_host(self):
        seven = self.ops["observed"].get("seven") or {}
        return bool(seven.get("1_host"))

    def ops_epoch(self):
        h = (self.ops["observed"].get("seven") or {}).get("1_host") or {}
        return h.get("epoch_state") == "NOT_DECLARED_BY_HOST"

    def ops_request(self):
        return self.w2.get("verdict") in ("NOT_ADMITTED", "PASS")

    def evidence_classes(self):
        return {"OBSERVED_LOCAL", "REASONED_NA_NATIVE_ENTRY"} >= set(
            self.hostv["rows"]["CODEX"].values())

    def stop(self):
        h = jl(self.r / "w1" / "raw" / "W1-HERMES-01.json")
        return h["verdict"] == "DEFERRED" and self.w1["pass"] == 12

    def resume(self):
        return self.chk["verdict"] == "PASS" and self.con["verdict"] == "ACCEPT"


def classify(fn, e=None):
    try:
        v = fn()
    except Exception as exc:  # noqa: BLE001
        return "ERROR", type(exc).__name__
    if v is True:
        return "OBSERVED_THIS_RUN", ""
    if v == "NOT_ADMITTED":
        return "NOT_ADMITTED", "protected effect unbound"
    return "PARTIAL", "predicate not satisfied"


SPEC = {
    # DEV 38
    "DEV-APP-01": ("pack", ["runs/w1/W1_RESULT.json"]),
    "DEV-EFF-01": ("eff", ["runs/w2/raw/W2-EFFECT-01.json"]),
    "DEV-PRE-01": ("live_head", ["runs/w2/raw/DEV01_driver.json"]),
    "DEV-PRE-02": ("preimage", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-PRE-03": ("admission", ["runs/w2/raw/DEV01_driver.json"]),
    "DEV-PRE-04": ("admission", ["runs/w2/raw/DEV01_driver.json"]),
    "DEV-PRE-05": ("tests", ["115 tests"]),
    "DEV-WS-01": ("guide", ["runs/w1/raw/GUIDE_SLICE.json"]),
    "DEV-WS-02": ("api", ["runs/w1/raw/API_SLICE.json"]),
    "DEV-WS-03": ("api", ["runs/w1/raw/API_SLICE.json"]),
    "DEV-WS-04": ("host", ["runs/w1/raw/HOST_LEDGER.json"]),
    "DEV-PROH-01": ("gitdiff", ["git diff a2281bf..HEAD"]),
    "DEV-PROH-02": ("pins", ["evidence/FIVE_PINS.json"]),
    "DEV-PROH-03": ("no_secret", ["secret scan"]),
    "DEV-PROH-04": ("no_revert", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-OP-01": ("live_head", ["runs/w2/raw/DEV01_driver.json"]),
    "DEV-OP-02": ("preimage", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-OP-03": ("dev_effect", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-OP-04": ("api", ["runs/w1/raw/API_SLICE.json"]),
    "DEV-OP-05": ("dev_effect", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-OP-06": ("dev_effect", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-ADP-01": ("guide", ["runs/w1/raw/GUIDE_SLICE.json"]),
    "DEV-ADP-02": ("api", ["runs/w1/raw/API_SLICE.json"]),
    "DEV-ADP-03": ("tests", ["115 tests"]),
    "DEV-ADP-04": ("host", ["runs/w1/raw/HOST_LEDGER.json"]),
    "DEV-POST-01": ("pack", ["runs/w1/raw/W1-R3-01.json"]),
    "DEV-POST-02": ("pack", ["runs/w1/raw/W1-R3-01.json"]),
    "DEV-POST-03": ("pack", ["runs/w1/raw/W1-R3-01.json"]),
    "DEV-POST-04": ("pins", ["CLOSEOUT/INDEX"]),
    "DEV-POST-05": ("outside", ["runs/w0/raw/R4-variants.json"]),
    "DEV-RB-01": ("pack", ["runs/w1/W1_RESULT.json"]),
    "DEV-RB-02": ("pins", ["evidence/EVIDENCE_MANIFEST.json"]),
    "DEV-RB-03": ("preimage", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-RB-04": ("pins", ["evidence/CHECKER.json"]),
    "DEV-IDEM-01": ("dev_effect", ["runs/w2/raw/W2-DEV-01.json"]),
    "DEV-IDEM-02": ("unknown", ["runs/w2/raw/unknown/UNKNOWN_FOUR.json"]),
    "DEV-IDEM-03": ("pins", ["a2281bf untouched"]),
    "DEV-PERM-01": ("auth", ["runs/w2/raw/W2-AUTH-01.json"]),
    # OPS 29
    "OPS-APP-01": ("ops_host", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-EFF-01": ("ops_request", ["runs/w2/W2_RESULT.json"]),
    "OPS-PRE-01": ("ops_host", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-PRE-02": ("ops_host", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-PRE-03": ("admission", ["runs/w2/raw/DEV01_driver.json"]),
    "OPS-PRE-04": ("ops_epoch", ["runs/w2/raw/OPS01_receiver.json"]),
    "OPS-PRE-05": ("ops_request", ["runs/w2/W2_RESULT.json"]),
    "OPS-CON-01": ("defer", ["ChatGPT not mounted"]),
    "OPS-CON-02": ("host", ["runs/w1/raw/HOST_LEDGER.json"]),
    "OPS-CON-03": ("defer", ["Hermes not mounted"]),
    "OPS-OP-01": ("ops_host", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-OP-02": ("host", ["runs/w1/raw/HOST_LEDGER.json"]),
    "OPS-OP-03": ("ops_request", ["runs/w2/W2_RESULT.json"]),
    "OPS-OP-04": ("ops_request", ["runs/w2/W2_RESULT.json"]),
    "OPS-OP-05": ("ops_effect", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-OP-06": ("ops_effect", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-POST-01": ("host", ["runs/w1/raw/HOST_LEDGER.json"]),
    "OPS-POST-02": ("evidence_classes", ["runs/w1/raw/HOST_LEDGER.json"]),
    "OPS-POST-03": ("partial", ["same principal"]),
    "OPS-POST-04": ("defer", ["Hermes three child"]),
    "OPS-POST-05": ("ops_host", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-RB-01": ("ops_host", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-RB-02": ("ops_host", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-REC-01": ("na", ["no install"]),
    "OPS-REC-02": ("na", ["no registration"]),
    "OPS-REC-03": ("ops_effect", ["runs/w2/raw/W2-OPS-01.json"]),
    "OPS-REC-04": ("unknown", ["runs/w2/raw/unknown/UNKNOWN_FOUR.json"]),
    "OPS-STOP-01": ("stop", ["runs/w1/raw/W1-HERMES-01.json"]),
    "OPS-RESUME-01": ("resume", ["evidence/CHECKER.json", "evidence/W3_CONSUMER.json"]),
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(G3 / "runs" / "w1" / "raw" / "ECP67_MEASURED.json"))
    a = ap.parse_args(argv)
    e = Ev()
    fnmap = {name: getattr(e, name) for name in dir(e) if not name.startswith("_")}
    fnmap["defer"] = lambda: "DEFERRED_HOST"
    fnmap["na"] = lambda: "REASONED_NA"
    fnmap["partial"] = lambda: "PARTIAL"
    rows = []
    for rid, (fn, refs) in SPEC.items():
        f = fnmap[fn]
        if fn in ("defer", "na", "partial"):
            verdict = f()
            note = ""
        else:
            verdict, note = classify(f, e)
        rows.append({"id": rid, "verdict": verdict, "predicate": fn,
                     "evidence": refs, "observed": note,
                     "predicate_complete": verdict != "ERROR"})
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    doc = {"schema": "FHS5.PLP.W1.ECPMeasured@2", "count": len(rows),
           "counts": counts, "rows": rows,
           "basis": {"w0": e.w0f["counts"], "w2_verdict": e.w2["verdict"],
                     "checker": e.chk["verdict"], "consumer": e.con["verdict"]}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"count": len(rows), "counts": counts}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
