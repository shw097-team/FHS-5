
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
