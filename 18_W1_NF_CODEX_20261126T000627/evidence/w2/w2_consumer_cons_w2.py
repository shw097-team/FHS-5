
import json, sys, hashlib
from pathlib import Path
art = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
rows = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
out = Path(sys.argv[3])
checks = {}
arows = art.get("rows") or []
checks["thirteen_rows"] = len(arows) == 13
by_n = {r.get("n"): r for r in arows if isinstance(r, dict)}
checks["row_numbers_complete"] = sorted(by_n) == list(range(1, 14))
null_numbers = {6, 7, 8, 11, 12}
must_w2 = [n for n in null_numbers if by_n.get(n, {}).get("blocker") == "W2_INPUT"]
checks["null_rows_need_w2_input"] = len(must_w2) == len(null_numbers)
checks["resume_present"] = all(by_n.get(n, {}).get("resume_min") for n in range(1, 14))
checks["no_grant_claim"] = not any(str(v).lower() == "granted" for v in
                                   (art.get("permission_state"), art.get("grant")))
checks["scope_exact"] = art.get("scope") == "W2-READ-01"
checks["subject_exact"] = art.get("subject") == "FHS-5_PLP/W2/INBOUND_DRAFT"
checks["permission_none_granted"] = art.get("permission_state") == "NONE_GRANTED"
payload = json.dumps({"subject": art.get("subject"), "scope": art.get("scope"),
                      "rows": [{"n": n, "blocker": by_n.get(n, {}).get("blocker")}
                               for n in range(1, 14)]}, ensure_ascii=False, sort_keys=True)
out.write_text(payload + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"checks": checks, "all": all(checks.values()),
                  "consumed_sha256": hashlib.sha256(payload.encode()).hexdigest(),
                  "readback": str(out)}, ensure_ascii=False))
