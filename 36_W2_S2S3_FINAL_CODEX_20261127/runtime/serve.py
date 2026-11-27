
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
