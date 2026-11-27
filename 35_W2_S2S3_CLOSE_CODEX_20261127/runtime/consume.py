
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
