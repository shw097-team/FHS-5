#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""N04 native-direct host ledger with per-case runner binding and a
fail-closed consumer.  Each stage is a real artifact or subprocess."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

SERVE = r'''
import json, sys
from pathlib import Path
loaded, out = Path(sys.argv[1]), Path(sys.argv[2])
c = json.loads(loaded.read_text(encoding="utf-8"))
v = c["views"]
dag = v["PD"].get("typed_dag") or []
nodes = (dag.get("nodes") if isinstance(dag, dict) else dag) or []
edges = (dag.get("edges") if isinstance(dag, dict) else []) or []
cases = []
for x in (v["TQAEP"].get("cases") or []):
    cid = x.get("case_id")
    cases.append({
        "id": cid, "kind": x.get("kind"),
        "fixture": "assets/fixtures/" + str(cid) + ".json",
        "oracle": "assets/oracles/" + str(cid) + ".json",
        "fixture_sha": x.get("fixture_sha256"), "oracle_sha": x.get("oracle_sha256"),
        "runner": x.get("runner"), "runner_status": x.get("runner_status"),
    })
bundle = {
  "identity": {"subject_id": v["PI"]["subject_id"], "scope": v["PI"]["scope"]},
  "pack_manifest_sha256": c["manifest_sha256"],
  "wp": [n.get("id") if isinstance(n, dict) else n for n in nodes],
  "edges": len(edges),
  "cases": cases,
  "ops": list(v["OPS"].get("ids") or []),
  "requirements": [r.get("id") for r in (v["PI"].get("requirements") or [])],
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n",
               encoding="utf-8", newline="\n")
print(json.dumps({"served": True, "cases": len(cases)}))
'''

CONSUME = r'''
import hashlib, json, sys
from pathlib import Path

served, pack, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
b = json.loads(served.read_text(encoding="utf-8"))

def refuse(first_fail, detail):
    res = {"accepted": False, "first_fail": first_fail, "detail": detail,
           "next_legal_action": "STOP_SCOPED:" + first_fail,
           "scope_bound_operation": None}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"consumed": False, "first_fail": first_fail}))
    raise SystemExit(2)

if b.get("identity", {}).get("subject_id") != "FHS-5_PLP/W2/CONTROL_PACK":
    refuse("SUBJECT_MISMATCH", b.get("identity"))
cases = b.get("cases") or []
if len(cases) != 12:
    refuse("CASE_SET_INCOMPLETE", len(cases))

pick = next((c for c in cases if c["kind"] == "POS"), cases[0])
if not pick.get("runner"):
    refuse("RUNNER_UNBOUND", pick.get("id"))
if str(pick.get("runner_status") or "").upper() not in ("BUILD_MINIMAL", "PREFLIGHT_ONLY"):
    refuse("RUNNER_STATUS_UNKNOWN", pick.get("runner_status"))

fx = pack / pick["fixture"] if pick.get("fixture") else None
orc = pack / pick["oracle"] if pick.get("oracle") else None
if fx is None or not fx.is_file():
    refuse("FIXTURE_MISSING", str(fx))
if orc is None or not orc.is_file():
    refuse("ORACLE_MISSING", str(orc))
fx_sha, or_sha = sha(fx), sha(orc)
if fx_sha != pick.get("fixture_sha"):
    refuse("FIXTURE_SHA_MISMATCH", {"want": pick.get("fixture_sha"), "got": fx_sha})
if or_sha != pick.get("oracle_sha"):
    refuse("ORACLE_SHA_MISMATCH", {"want": pick.get("oracle_sha"), "got": or_sha})

res = {
  "accepted": True, "first_fail": None,
  "scope_bound_operation": {
      "case": pick["id"], "kind": pick["kind"],
      "runner": pick["runner"], "runner_status": pick["runner_status"],
      "fixture": pick["fixture"], "fixture_sha256": fx_sha,
      "oracle": pick["oracle"], "oracle_sha256": or_sha,
      "subject_id": b["identity"]["subject_id"], "scope": b["identity"]["scope"],
  },
  "next_legal_action": ("RUN " + pick["id"] + " via " + pick["runner"]
                        + " (" + pick["runner_status"] + ")"),
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
               encoding="utf-8", newline="\n")
print(json.dumps({"consumed": True, "case": pick["id"], "runner": pick["runner"]}))
'''


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_stage(argv):
    return subprocess.run(argv, capture_output=True, text=True, errors="replace")


def main():
    wt = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "tools").mkdir(exist_ok=True)
    (root / "tools" / "serve.py").write_text(SERVE, encoding="utf-8", newline="\n")
    (root / "tools" / "consume.py").write_text(CONSUME, encoding="utf-8", newline="\n")
    sys.path.insert(0, str(wt / "W1" / "impl"))
    import s1_reader

    pack = wt / "S1_PACKS" / "FHS-5_PLP_W2_NATIVE_FIRST"
    wo = "WO-W2-N04-N09-20261127"
    stages = {}
    insp = s1_reader.inspect_s1(pack)
    (root / "selected.json").write_text(json.dumps({
        "work_order": wo, "pack": str(pack), "manifest_sha256": insp["manifest_sha256"],
        "pack_tree_sha256": insp["pack_tree_sha256"], "identity": insp["identity"],
        "requirements": len(insp["requirement_rows"])}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8", newline="\n")
    stages["Selected"] = {"artifact": "selected.json", "sha256": sha(root / "selected.json")}

    loaded = root / "loaded_contracts.json"
    child = ("import json,sys;sys.path.insert(0,%r);import tpm_contracts_nf as T;"
             "c=T.build_contracts(sys.argv[1],json.loads(sys.argv[2]));"
             "open(sys.argv[3],'w',encoding='utf-8').write(json.dumps(c,ensure_ascii=False))"
             % str(wt / "W1" / "impl"))
    p = run_stage([sys.executable, "-c", child, str(pack), json.dumps({
        "project_id": "FHS-5_PLP", "subject_id": "FHS-5_PLP/W2/CONTROL_PACK",
        "scope": "W2-NF-01", "wave_id": "W2", "batch_id": "W2-NF-01",
        "work_id": wo}), str(loaded)])
    stages["Loaded"] = {"argv_exit": p.returncode, "stderr": p.stderr[-200:],
                        "artifact": "loaded_contracts.json",
                        "sha256": sha(loaded) if loaded.is_file() else None}
    stages["Installed"] = {"status": "REASONED_NA_NATIVE_ENTRY"}
    stages["Bound"] = {"work_order": wo}

    served = root / "served_bundle.json"
    inv = run_stage([sys.executable, str(root / "tools" / "serve.py"),
                     str(loaded), str(served)])
    stages["Invoked"] = {"argv": [sys.executable, "tools/serve.py"],
                         "exit": inv.returncode, "stdout": inv.stdout.strip()[:200],
                         "stderr": inv.stderr[-200:]}
    stages["ActualServed"] = {"artifact": "served_bundle.json",
                              "sha256": sha(served) if served.is_file() else None}

    decision = root / "consumed_decision.json"
    con = run_stage([sys.executable, str(root / "tools" / "consume.py"),
                     str(served), str(pack), str(decision)])
    dec = json.loads(decision.read_text(encoding="utf-8")) if decision.is_file() else None
    stages["Consumed"] = {"argv": [sys.executable, "tools/consume.py"],
                          "exit": con.returncode, "stdout": con.stdout.strip()[:200],
                          "stderr": con.stderr[-200:],
                          "artifact": "consumed_decision.json",
                          "sha256": sha(decision) if decision.is_file() else None,
                          "decision": dec}

    # fail-closed negative: a copy without the oracle must be refused
    import shutil
    neg_pack = root / "_neg_pack"
    if neg_pack.exists():
        shutil.rmtree(neg_pack)
    shutil.copytree(pack, neg_pack)
    (neg_pack / "assets" / "oracles" / "W2-DEV-01.json").unlink(missing_ok=True)
    neg_out = root / "consumed_negative.json"
    neg = run_stage([sys.executable, str(root / "tools" / "consume.py"),
                     str(served), str(neg_pack), str(neg_out)])
    negd = json.loads(neg_out.read_text(encoding="utf-8")) if neg_out.is_file() else {}

    ok = (stages["Loaded"]["argv_exit"] == 0 and inv.returncode == 0
          and con.returncode == 0 and dec and dec.get("accepted") is True
          and dec.get("scope_bound_operation", {}).get("runner") == "RUN-DEV-01"
          and neg.returncode == 2 and negd.get("first_fail") == "ORACLE_MISSING"
          and negd.get("next_legal_action", "").startswith("STOP_SCOPED"))
    rep = {"schema": "FHS5.PLP.W2.N04HostLedger@2", "work_order": wo,
           "stages": stages, "negative": {"exit": neg.returncode,
                                          "first_fail": negd.get("first_fail"),
                                          "next": negd.get("next_legal_action")},
           "verdict": "PASS" if ok else "FAIL"}
    (root / "N04_LEDGER.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": rep["verdict"],
                      "runner": ((dec or {}).get("scope_bound_operation") or {}).get("runner"),
                      "neg": rep["negative"]}, ensure_ascii=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
