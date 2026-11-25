#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 inbound DRAFT material + five-seam wiring (F1).

Builds a *draft*, explicitly non-authoritative W2 inbound work material from the
real W2M section 03.1 table (thirteen UNBOUND predecessors) and wires the five
W1 producer seams into it with per-field readback:

  SourceRefs / EffectConstraints / ContextBundle / HostCapabilityLedger /
  ChangeCone

No W2 grant is issued and no protected effect is performed.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import body_resolver as br
import bridge_nf as bridge
import nf_reader as reader
import tpm_contracts_nf as tpm

SCHEMA_DRAFT = "FHS5.PLP.W2.SourceManifest.NF@1"
DRAFT_ID = "FHS5-PLP/W2/INBOUND_DRAFT/2026-11-25-r1"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _read(p: Path) -> str:
    return br.decode_utf8(p.read_bytes(), p.name)


def extract_predecessors(w2m: Path) -> list:
    text = _read(w2m)
    start = text.find("## 03.1")
    end = text.find("**註記**", start)
    block = text[start:end if end > 0 else start + 6000]
    rows = []
    for line in block.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|(.+)\|\s*$", line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) < 6:
            continue
        rows.append({"n": int(m.group(1)), "predecessor": cells[0], "fields": cells[1],
                     "type": cells[2], "owner": cells[3], "w0_evidence": cells[4],
                     "resume_min": cells[5]})
    return rows


def build_material(w2m: Path, w0b: Path | None, out: Path) -> dict:
    rows = extract_predecessors(w2m)
    if len(rows) != 13:
        raise RuntimeError(f"expected 13 predecessors, got {len(rows)}")
    out.mkdir(parents=True, exist_ok=True)
    w2m_sha = sha256_bytes(w2m.read_bytes())
    w2m_text = _read(w2m)
    i0 = w2m_text.find("## 01.1")
    jtbd = w2m_text[i0:i0 + 400].splitlines()[2].strip() if i0 >= 0 else ""
    pi = f"""# W2 INBOUND DRAFT — PI/PD（非正式主用）

**status**：`DRAFT`｜**artifact**：`{DRAFT_ID}`
**project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W2/INBOUND_DRAFT`
**scope**：`W2-READ-01`｜**wave_id**：`W2`｜**batch_id**：`W2-IN-DRAFT-01`
**source**：W2M §03.1（sha256 `{w2m_sha}`）

Job to be done：將 W0-B 13 個 UNBOUND 前件整理成 W2 DRAFT BindingRequest 清單（READ／DRAFT，不發 Grant、不執行 protected effect）。

**Non-goals**：不發 Grant；不執行 W2 protected DEV／OPS；不建立正式 W2 主用包；不改 W0 歷史。

## ACC（DRAFT）

- 13/13 每列具備 required fields、Owner、Resume 最小證據、W0 證據狀態。
- 全部列 `UNBOUND`，不得自行改為 true。
- 任何 output 僅為 DRAFT，`permission_state=NONE_GRANTED`。
"""
    (out / "00_W2_DRAFT_PI_PD.md").write_text(pi, encoding="utf-8", newline="\n")

    lines = ["# W2 INBOUND DRAFT — TQAEP（13 binding requests）", "",
             "| ID | Predecessor | Fields | Type | Owner | W0 evidence | Resume minimum |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| `W2-B{n:02d}` | {p} | {f} | {t} | {o} | {w} | {m} |".format(
            n=r["n"], p=r["predecessor"], f=r["fields"], t=r["type"], o=r["owner"],
            w=r["w0_evidence"], m=r["resume_min"]))
    (out / "03_W2_DRAFT_TQAEP.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    thin = """# W2 DRAFT thin start

## NEXT
W2-READ: produce the 13-row DRAFT binding-request plan inside W2-READ-01; no Grant, no protected effect.

## STOP
missing source, wrong scope, any request to issue a grant or perform a protected effect.

## RESUME
same subject+scope with a real W2 authority receipt or the Owner's W2 admission.
"""
    (out / "04_W2_DRAFT_THIN.md").write_text(thin, encoding="utf-8", newline="\n")

    files = []
    for name in ("00_W2_DRAFT_PI_PD.md", "03_W2_DRAFT_TQAEP.md", "04_W2_DRAFT_THIN.md"):
        p = out / name
        files.append({"path": name, "bytes": p.stat().st_size,
                      "sha256": sha256_bytes(p.read_bytes())})
    sources = [{"id": "W2M", "path": str(w2m), "sha256": w2m_sha,
                "bytes": w2m.stat().st_size, "role": "W2 primary spec"}]
    if w0b and Path(w0b).is_file():
        sources.append({"id": "W0B_DECISION", "path": str(w0b),
                        "sha256": sha256_bytes(Path(w0b).read_bytes()),
                        "bytes": Path(w0b).stat().st_size, "role": "W0-B decision"})
    man = {
        "schema": SCHEMA_DRAFT, "pack_version": "W2-INBOUND-DRAFT-r1",
        "artifact_id": DRAFT_ID, "project_id": "FHS-5_PLP",
        "subject_id": "FHS-5_PLP/W2/INBOUND_DRAFT", "scope": "W2-READ-01",
        "wave_id": "W2", "batch_id": "W2-IN-DRAFT-01",
        "draft": True, "claim_ceiling": "W2_INBOUND_DRAFT_NOT_ADMITTED",
        "pack_files": files, "sources": sources,
        "requirements": rows,
        "permission_state": "NONE_GRANTED",
        "note": "draft material only; not a W2 primary pack and not a grant",
    }
    (out / "05_W2_SOURCE_MANIFEST.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"material_root": str(out), "manifest": "05_W2_SOURCE_MANIFEST.json",
            "manifest_sha256": sha256_bytes((out / "05_W2_SOURCE_MANIFEST.json").read_bytes()),
            "rows": len(rows), "draft": True}


def seam_wiring(w1_pack: Path, w2_material: Path, delivery: Path) -> dict:
    """Five producer seams wired into the W2 draft with real readback."""
    insp = reader.inspect_package(w1_pack)
    inst = bridge.inspect_package(str(w1_pack / "05_W1_SOURCE_MANIFEST.json"), str(w1_pack))
    ctx = bridge.render_agent_context(bridge.explain_slice(str(w1_pack), "spec"), "Codex")
    host_p = delivery / "evidence" / "host" / "host_receipt.json"
    host = json.loads(host_p.read_text(encoding="utf-8")) if host_p.is_file() else {}
    cm_p = delivery / "W1_CLOSURE_MATRIX.json"
    cm = json.loads(cm_p.read_text(encoding="utf-8")) if cm_p.is_file() else {"rows": []}
    contracts = tpm.build_contracts(str(w2_material), {
        "project_id": "FHS-5_PLP", "subject_id": "FHS-5_PLP/W2/INBOUND_DRAFT",
        "scope": "W2-READ-01", "wave_id": "W2", "batch_id": "W2-IN-DRAFT-01",
        "work_id": "W2-IN-WIRING"})
    rows = []

    def add(seam, src, tgt, transform, ok, missing=None, loss="NONE", readback=""):
        rows.append({"seam": seam, "source_value": str(src)[:160],
                     "source_sha256": sha256_bytes(json.dumps(src, ensure_ascii=False,
                                                               sort_keys=True, default=str).encode("utf-8")),
                     "target_value": str(tgt)[:160],
                     "target_sha256": sha256_bytes(json.dumps(tgt, ensure_ascii=False,
                                                               sort_keys=True, default=str).encode("utf-8")),
                     "transform": transform, "matched": bool(ok),
                     "missing": missing or [], "loss": loss if ok else "EXPLICIT_REVIEW",
                     "consumer_readback": readback})
        return ok

    # 1 SourceRefs
    src_ids = {s["id"]: s.get("sha256") for s in insp["source_refs"]}
    local_sha = [k for k, v in src_ids.items() if v]
    w2_sources = contracts["views"]["PI"].get("sources") or []
    w2_sha = [s for s in w2_sources if s.get("sha256")]
    unresolved = [s for s in insp["source_refs"] if s.get("availability") == "LOCAL_MISSING_RECORDED"]
    ok1 = bool(local_sha) and bool(w2_sha) and len(w2_sha) == len(w2_sources)
    add("SourceRefs", {"w1_refs": len(src_ids), "with_sha": len(local_sha),
                       "unresolved": len(unresolved)},
        {"w2_sources": len(w2_sources), "with_sha": len(w2_sha)},
        "id+sha table -> W2 draft sources", ok1,
        [] if ok1 else ["source sha missing"],
        "PROJECTION",
        "%d W1 refs (%d with sha, %d unresolved) referenced by %d W2 draft sources"
        % (len(src_ids), len(local_sha), len(unresolved), len(w2_sources)))
    # 2 EffectConstraints
    ec = inst["effect_constraints"]
    cons = contracts["views"]["PI"]["constraints"]
    ok2 = (ec["permission_state"] == cons["permission_state"] == "NONE_GRANTED"
           and ec["unknown_effect"] == cons["unknown_effect"] == "FAIL_CLOSED"
           and not cons.get("ecp_is_grant"))
    add("EffectConstraints", ec, cons, "identity", ok2, [] if ok2 else ["permission/unknown"])
    # 3 ContextBundle
    ctx_file = w2_material / "context_bundle.md"
    ctx_file.write_text(ctx["context_utf8"], encoding="utf-8", newline="\n")
    back_sha = sha256_bytes(ctx_file.read_bytes())
    ok3 = ctx["context_sha256"] == back_sha
    add("ContextBundle", {"context_sha256": ctx["context_sha256"],
                          "bytes": len(ctx["context_utf8"].encode("utf-8"))},
        {"context_file": "context_bundle.md", "sha256": back_sha},
        "serve-then-readback", ok3, [] if ok3 else ["context sha mismatch"])
    # 4 HostCapabilityLedger
    stages = (host.get("stage_ledger") or {})
    ok4 = bool(stages) and stages.get("Consumed") == "OBSERVED_LOCAL" and bool(host.get("host_consumed"))
    add("HostCapabilityLedger", stages, {"consumed": ok4},
        "stage-row -> W2 host capability", ok4, [] if ok4 else ["stages missing"])
    # 5 ChangeCone
    cone = sorted({(r["verdict"], r["evidence_ref"]) for r in cm.get("rows", [])
                   if r.get("evidence_ref")})
    from_pack = Path(delivery / "W1_UPSTREAM_CHANGESET.md")
    ok5 = len(cone) > 0
    add("ChangeCone", {"rows": len(cm.get("rows", [])), "pairs": len(cone)},
        {"changeset_present": from_pack.is_file(), "distinct_pairs": len(cone)},
        "exact kind+path", ok5, [] if ok5 else ["changeset/cone missing"])
    return {"schema": "FHS5.PLP.W1.SeamWiring@1", "rows": rows,
            "matched": sum(1 for r in rows if r["matched"]), "total": len(rows),
            "state": "COMPLETE" if all(r["matched"] for r in rows) else "EXPLICIT_REVIEW"}


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--w2m", required=True)
    ap.add_argument("--w0b")
    ap.add_argument("--out", required=True)
    ap.add_argument("--w1-pack")
    ap.add_argument("--delivery")
    ap.add_argument("--wiring-out")
    args = ap.parse_args(argv)
    res = build_material(Path(args.w2m), Path(args.w0b) if args.w0b else None,
                         Path(args.out))
    if args.w1_pack and args.delivery:
        w = seam_wiring(Path(args.w1_pack), Path(args.out), Path(args.delivery))
        (Path(args.wiring_out) if args.wiring_out else Path(args.out) / "seam_wiring.json")
        target = Path(args.wiring_out) if args.wiring_out else Path(args.out) / "seam_wiring.json"
        target.write_text(json.dumps(w, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8", newline="\n")
        res["seam_wiring"] = {"matched": w["matched"], "total": w["total"], "state": w["state"]}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
