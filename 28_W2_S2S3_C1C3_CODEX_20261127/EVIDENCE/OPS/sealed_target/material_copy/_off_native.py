
import json, sys
from pathlib import Path
forbidden = ("tpm_contracts_nf", "guide_nf", "bridge_nf", "w2_inbound")
leaked = [m for m in forbidden if m in sys.modules]
if leaked:
    print(json.dumps({"ok": False, "leaked": leaked})); raise SystemExit(3)
sys.path.insert(0, sys.argv[1])
import body_resolver as br
text = br.decode_utf8(Path(sys.argv[2]).read_bytes(), "w2m")
start = text.find("## 03.1")
end = text.find("**", start)
block = text[start:end]
rows = []
for line in block.splitlines():
    line = line.strip()
    if not line.startswith("|") or line.startswith("| #") or line.startswith("|---"):
        continue
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) < 7 or not cells[0].isdigit():
        continue
    rows.append([int(cells[0]), cells[1], cells[4], cells[6]])
print(json.dumps({"ok": True, "rows": rows, "modules": sorted(
    m for m in sys.modules if m in ("tpm_contracts_nf", "guide_nf", "bridge_nf", "w2_inbound"))},
    ensure_ascii=False))
