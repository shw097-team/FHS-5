
import json, sys, hashlib
from pathlib import Path
art = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
pack_sha = sys.argv[2]
out = Path(sys.argv[3])
checks = {}
checks["has_identity"] = bool(art.get("subject") or art.get("scope"))
checks["scope_present"] = bool(art.get("scope"))
checks["artifact_not_empty"] = len(json.dumps(art)) > 40
req = [k for k in sys.argv[5].split(",") if k]
checks["required_keys_present"] = all(k in art for k in req)
checks["case_row_present"] = (art.get("case_id") == "W1-API-01") if "case_id" in req else True
payload = json.dumps({"subject": art.get("subject"), "scope": art.get("scope"),
                      "keys": sorted(art.keys())}, ensure_ascii=False, sort_keys=True)
out.write_text(payload + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"checks": checks, "payload_sha256": hashlib.sha256(payload.encode()).hexdigest(),
                  "consumed_sha256": hashlib.sha256(payload.encode()).hexdigest(),
                  "pack_sha256": pack_sha, "action": "parse_and_use_host_artifact",
                  "readback": str(out)}, ensure_ascii=False))
