
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
