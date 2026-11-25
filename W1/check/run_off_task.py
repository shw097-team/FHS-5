#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Same-task ON vs OFF comparison (F2).

ON  : TPM contracts + Guide thin start + Bridge context produce the projection.
OFF : a cold-off Native path that imports no TPM/Guide/Bridge module and reads
      the frozen source directly, producing the same projection.
The two projections are compared on stable semantics only.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import body_resolver as br
import guide_nf as guide
import off_isolation as off
import tpm_contracts_nf as tpm
import w2_inbound as w2i


def on_path(material: Path, w1_pack: Path) -> dict:
    ident = {"project_id": "FHS-5_PLP", "subject_id": "FHS-5_PLP/W2/INBOUND_DRAFT",
             "scope": "W2-READ-01", "wave_id": "W2", "batch_id": "W2-IN-DRAFT-01",
             "work_id": "W2-ON"}
    contracts = tpm.build_contracts(str(material), ident)
    thin = guide.inspect_guide_request({}, str(material))
    rows = contracts["views"]["TQAEP"]["requirements"]
    proj = sorted((r["n"], r["predecessor"], r["owner"], r["resume_min"]) for r in rows)
    return {"path": "ON", "modules": ["tpm", "guide", "bridge"],
            "rows": len(rows), "projection": proj,
            "thin_next": thin.get("next"), "contract_profile": contracts["profile"]}


OFF_SCRIPT = r'''
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
'''


def off_path(material: Path, w2m: Path, impl: Path) -> dict:
    script = material / "_off_native.py"
    script.write_text(OFF_SCRIPT, encoding="utf-8", newline="\n")
    r = subprocess.run([sys.executable, "-B", str(script), str(impl), str(w2m)],
                       capture_output=True, text=True, timeout=120,
                       encoding="utf-8", errors="replace")
    try:
        out = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        out = {"ok": False, "stderr": r.stderr[-300:]}
    proj = sorted((int(x[0]), x[1], x[2], x[3]) for x in out.get("rows") or [])
    return {"path": "OFF", "exit": r.returncode, "imported_forbidden": out.get("modules"),
            "rows": len(proj), "projection": proj}


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--material", required=True)
    ap.add_argument("--w2m", required=True)
    ap.add_argument("--w1-pack", required=True)
    ap.add_argument("--impl", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    on = on_path(Path(args.material), Path(args.w1_pack))
    offd = off_path(Path(args.material), Path(args.w2m), Path(args.impl))
    cold = off.cold_off_probe("legacy_runtime",
                              ["hgk_runtime", "fabric_runtime", "sbl_runtime",
                               "pipd_runtime", "hermes_runtime"])
    ctl = off.positive_control("json")
    flag = off.env_flag_only_reject("W1_NATIVE_OFF")
    same = on["projection"] == offd["projection"]
    receipt = {
        "schema": "FHS5.PLP.W1.OffTaskReceipt@1",
        "run_id": time.strftime("%Y%m%dT%H%M%S"),
        "task": "W2 inbound draft 13-row projection",
        "inputs": {
            "w2m_path": str(Path(args.w2m).resolve()),
            "w2m_sha256": __import__("hashlib").sha256(Path(args.w2m).read_bytes()).hexdigest(),
            "material_manifest": str(Path(args.material) / "05_W2_SOURCE_MANIFEST.json"),
            "material_manifest_sha256": __import__("hashlib").sha256(
                (Path(args.material) / "05_W2_SOURCE_MANIFEST.json").read_bytes()).hexdigest(),
        },
        "on": {k: on[k] for k in ("rows", "thin_next", "contract_profile", "modules")},
        "off": {k: offd[k] for k in ("rows", "exit", "imported_forbidden")},
        "projection_equal": same,
        "on_rows": on["rows"], "off_rows": offd["rows"],
        "semantics": {"on_success": on["rows"] == 13, "off_success": offd["rows"] == 13,
                      "on_only_success": on["rows"] == 13 and offd["rows"] != 13,
                      "parity_double_failure": on["rows"] != 13 and offd["rows"] != 13},
        "cold_off": {k: cold.get(k) for k in ("cold_off", "blocked", "leaked", "exit")},
        "positive_control": ctl,
        "env_flag_only": flag,
        "state": ("ON_OFF_BOTH_SEMANTIC_SUCCESS" if (same and on["rows"] == 13 and
                                                     offd["rows"] == 13)
                  else "OFF_PARITY_NOT_ESTABLISHED"),
    }
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"state": receipt["state"], "on": on["rows"], "off": offd["rows"],
                      "cold_off": receipt["cold_off"]["cold_off"],
                      "control": ctl.get("imported")}, ensure_ascii=False))
    return 0 if receipt["state"] == "ON_OFF_BOTH_SEMANTIC_SUCCESS" else 4


if __name__ == "__main__":
    raise SystemExit(main())
