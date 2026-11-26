#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""N04: native-direct Host ledger over the real S1 W2 pack.

Selected -> Loaded -> Installed(REASONED_NA_NATIVE_ENTRY) -> Bound ->
Invoked -> ActualServed -> Consumed, each stage a real subprocess or a real
artifact with its own digest.  No host runtime is created.
"""
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
bundle = {
  "identity": {"subject_id": c["views"]["PI"]["subject_id"], "scope": c["views"]["PI"]["scope"]},
  "pack_manifest_sha256": c["manifest_sha256"],
  "wp": [n.get("id") if isinstance(n, dict) else n
         for n in ((v["PD"].get("typed_dag") or {}).get("nodes")
                   if isinstance(v["PD"].get("typed_dag"), dict) else (v["PD"].get("typed_dag") or []))],
  "edges": len(((v["PD"].get("typed_dag") or {}).get("edges")
                 if isinstance(v["PD"].get("typed_dag"), dict) else ()) or []),
  "cases": [{"id": x.get("case_id"), "kind": x.get("kind"),
             "fixture": "assets/fixtures/" + str(x.get("case_id")) + ".json",
             "oracle": "assets/oracles/" + str(x.get("case_id")) + ".json",
             "fixture_sha": x.get("fixture_sha256"), "oracle_sha": x.get("oracle_sha256"),
             "runner": v["TQAEP"].get("runner")}
            for x in (v["TQAEP"].get("cases") or [])],
  "ops": list(v["OPS"].get("ids") or []),
  "requirements": [r.get("id") for r in (v["PI"].get("requirements") or [])],
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n",
               encoding="utf-8", newline="\n")
print(json.dumps({"served": True, "cases": len(bundle["cases"])}))
'''

CONSUME = r'''
import hashlib, json, sys
from pathlib import Path
served, pack, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
b = json.loads(served.read_text(encoding="utf-8"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pick = next((c for c in b["cases"] if c["kind"] == "POS"), b["cases"][0])
fx = pack / pick["fixture"] if pick.get("fixture") else None
orc = pack / pick["oracle"] if pick.get("oracle") else None
fx_sha = sha(fx) if fx and fx.is_file() else None
or_sha = sha(orc) if orc and orc.is_file() else None
decision = {
  "selected_case": pick["id"], "kind": pick["kind"], "runner": pick.get("runner"),
  "fixture_present": bool(fx and fx.is_file()),
  "oracle_present": bool(orc and orc.is_file()),
  "fixture_sha256": fx_sha, "oracle_sha256": or_sha,
  "fixture_sha_match": fx_sha is not None and fx_sha == pick.get("fixture_sha"),
  "oracle_sha_match": or_sha is not None and or_sha == pick.get("oracle_sha"),
  "next_legal_action": ("RUN " + pick["id"] + " via " + str(pick.get("runner"))
                        if fx and orc else "STOP_SCOPED: fixture/oracle missing"),
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(decision, ensure_ascii=False, indent=1) + "\n",
               encoding="utf-8", newline="\n")
print(json.dumps({"consumed": True, "case": decision["selected_case"]}))
'''


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    wt = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "tools").mkdir(exist_ok=True)
    (root / "tools" / "serve.py").write_text(SERVE, encoding="utf-8", newline="\n")
    (root / "tools" / "consume.py").write_text(CONSUME, encoding="utf-8", newline="\n")
    sys.path.insert(0, str(wt / "W1" / "impl"))
    import s1_reader
    import tpm_contracts_nf as T

    pack = wt / "S1_PACKS" / "FHS-5_PLP_W2_NATIVE_FIRST"
    wo = "WO-W2-N04-N09-20261127"
    stages = {}

    # Selected
    insp = s1_reader.inspect_s1(pack)
    (root / "selected.json").write_text(json.dumps({
        "work_order": wo, "pack": str(pack),
        "manifest_sha256": insp["manifest_sha256"],
        "pack_tree_sha256": insp["pack_tree_sha256"],
        "identity": insp["identity"],
        "requirements": len(insp["requirement_rows"]),
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    stages["Selected"] = {"artifact": "selected.json", "sha256": sha(root / "selected.json")}

    # Loaded (TPM in a child process)
    loaded = root / "loaded_contracts.json"
    p = subprocess.run([sys.executable, "-c",
                        "import json,sys;sys.path.insert(0,%r);import tpm_contracts_nf as T;"
                        "c=T.build_contracts(sys.argv[1],json.loads(sys.argv[2]));"
                        "open(sys.argv[3],'w',encoding='utf-8').write(json.dumps(c,ensure_ascii=False))"
                        % str(wt / "W1" / "impl"),
                        str(pack),
                        json.dumps({"project_id": "FHS-5_PLP",
                                    "subject_id": "FHS-5_PLP/W2/CONTROL_PACK",
                                    "scope": "W2-NF-01", "wave_id": "W2",
                                    "batch_id": "W2-NF-01", "work_id": wo}),
                        str(loaded)],
                       capture_output=True, text=True, errors="replace")
    stages["Loaded"] = {"argv_exit": p.returncode, "stderr": p.stderr[-200:],
                        "artifact": "loaded_contracts.json",
                        "sha256": sha(loaded) if loaded.is_file() else None}
    stages["Installed"] = {"status": "REASONED_NA_NATIVE_ENTRY",
                           "reason": "native direct entry; no plugin install stage"}
    stages["Bound"] = {"work_order": wo,
                       "bound_identity": {"subject_id": json.loads(loaded.read_text(encoding="utf-8"))["views"]["PI"]["subject_id"], "scope": json.loads(loaded.read_text(encoding="utf-8"))["views"]["PI"]["scope"]}
                       if loaded.is_file() else None}

    # Invoked -> ActualServed (child writes served bundle)
    served = root / "served_bundle.json"
    inv = subprocess.run([sys.executable, str(root / "tools" / "serve.py"),
                          str(loaded), str(served)],
                         capture_output=True, text=True, errors="replace")
    stages["Invoked"] = {"argv": [sys.executable, "tools/serve.py", "loaded_contracts.json",
                                  "served_bundle.json"],
                         "exit": inv.returncode, "stdout": inv.stdout.strip()[:200],
                         "stderr": inv.stderr[-200:]}
    stages["ActualServed"] = {"artifact": "served_bundle.json",
                              "sha256": sha(served) if served.is_file() else None}

    # Consumed (separate process uses the served material)
    decision = root / "consumed_decision.json"
    con = subprocess.run([sys.executable, str(root / "tools" / "consume.py"),
                          str(served), str(pack), str(decision)],
                         capture_output=True, text=True, errors="replace")
    stages["Consumed"] = {"argv": [sys.executable, "tools/consume.py", "served_bundle.json",
                                   "pack", "consumed_decision.json"],
                          "exit": con.returncode, "stdout": con.stdout.strip()[:200],
                          "stderr": con.stderr[-200:],
                          "artifact": "consumed_decision.json",
                          "sha256": sha(decision) if decision.is_file() else None,
                          "decision": json.loads(decision.read_text(encoding="utf-8"))
                          if decision.is_file() else None}

    ok = (stages["Loaded"]["argv_exit"] == 0 and inv.returncode == 0
          and con.returncode == 0
          and stages["Consumed"]["decision"] is not None
          and stages["Consumed"]["decision"].get("fixture_present")
          and stages["Consumed"]["decision"].get("oracle_present")
          and stages["Consumed"]["decision"].get("fixture_sha_match")
          and stages["Consumed"]["decision"].get("oracle_sha_match"))
    rep = {"schema": "FHS5.PLP.W2.N04HostLedger@1", "work_order": wo,
           "stages": stages, "verdict": "PASS" if ok else "FAIL",
           "note": "native direct; Installed is REASONED_NA, not observed"}
    out = root / "N04_LEDGER.json"
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": rep["verdict"],
                      "stages": [k for k in stages],
                      "case": (stages["Consumed"]["decision"] or {}).get("selected_case"),
                      "next": (stages["Consumed"]["decision"] or {}).get("next_legal_action")},
                     ensure_ascii=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
