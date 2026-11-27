#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Redact, freeze five pins, build the evidence manifest and the outer seal."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
WT = G3.parent
sys.path.insert(0, str(G3 / "lib"))
import g3pack  # noqa: E402
import redact  # noqa: E402

PACK_BASE = Path(r"C:\Projects\Agent_Workspace\FHS-5_Workspace"
                 r"\FHS-5_PLP_W0-W2_第三代Native-first_執行控制包_FINAL\01_BODY")
EXCLUDE_PARTS = {".git", "__pycache__", "_scratch", "world", "off", "cli"}
KEEP_PARTS = {"raw", "dev", "ops"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha(Path(p).read_bytes())


def collect(root: Path, skip_world=True):
    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if set(rel.parts) & EXCLUDE_PARTS:
            continue
        if p.suffix in (".pyc", ".pyo"):
            continue
        if skip_world and "world" in rel.parts:
            continue
        out.append(rel.as_posix())
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(G3 / "evidence"))
    a = ap.parse_args(argv)
    out = Path(a.out)

    # 1. redact any local identifier in the run evidence
    changed = 0
    for p in (G3 / "runs").rglob("*.json"):
        if "world" in p.parts or "_scratch" in p.parts:
            continue
        if redact.file_json(p):
            changed += 1

    # 2. five pins
    packs = {w: g3pack.verify_pack(PACK_BASE / f"FHS-5_PLP_{w}_NATIVE_FIRST")
             for w in ("W0", "W1", "W2")}
    code_rows = []
    for base in (WT / "W1" / "impl", WT / "W1" / "check", G3 / "lib", G3 / "W0",
                 G3 / "W1", G3 / "W2", G3 / "check"):
        for p in sorted(base.glob("*.py")):
            if p.name.startswith("_patch") or p.name.startswith("_probe"):
                continue
            code_rows.append(f"{p.relative_to(WT).as_posix()}|{sha_file(p)}")
    candidate_agg = sha("\n".join(sorted(code_rows)).encode())
    pins = {
        "schema": "FHS5.PLP.G3.FivePins@1",
        "source": {w: packs[w]["manifest_sha256"] for w in packs},
        "candidate": {
            "members": [{"path": r.split("|")[0], "sha256": r.split("|")[1]}
                        for r in sorted(code_rows)],
            "count": len(code_rows),
            "aggregate": candidate_agg,
            "modified_product": ["W1/check/w2_dev_gate.py", "W1/impl/host_facade.py"],
        },
        "oracle": {}, "case_set": {},
        "pack_tree": {w: packs[w]["tree_sha256"] for w in packs},
        "evidence": {},
    }

    for w, v in packs.items():
        pk = v["pack"]
        orows, crows = [], []
        for c in pk.cases:
            orel = c.get("oracle")
            if orel:
                a = pk.asset(orel)
                osha = a["sha256"] if a else sha_file(pk.root / orel)
                orows.append(f"{c['case_id']}|{osha}")
            crows.append(f"{c['case_id']}|{c.get('fixture')}|{c.get('oracle')}")
        pins["oracle"][w] = {"count": len(orows),
                             "aggregate": sha("\n".join(sorted(orows)).encode())}
        pins["case_set"][w] = {"count": len(crows),
                               "aggregate": sha("\n".join(sorted(crows)).encode())}
    pins["dependencies"] = {w: {"manifest_sha256": packs[w]["manifest_sha256"],
                                "tree_sha256": packs[w]["tree_sha256"]} for w in packs}
    pins["runtime"] = {"python": sys.version.split()[0]}

    # 3. evidence manifest (manifest and seal are self-excluded)
    # The manifest binds evidence/raw and the checker verdict only.  Narrative
    # documents are bound by the git commit, so updating a closeout never
    # invalidates the evidence seal.
    files = [r for r in collect(G3)
             if (r.startswith("runs/") or r == "evidence/CHECKER.json")
             and not r.startswith("runs/w0_full/13/")]
    rows = []
    for rel in files:
        p = G3 / rel
        rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha_file(p)})
    manifest = {"schema": "FHS5.PLP.G3.EvidenceManifest@1",
                "candidate": candidate_agg,
                "pins": pins,
                "files": rows,
                "count": len(rows),
                "self_excluded": ["evidence/EVIDENCE_MANIFEST.json",
                                  "evidence/SEAL.json",
                                  "evidence/FIVE_PINS.json",
                                  "evidence/W3_CONSUMER.json"]}
    out.mkdir(parents=True, exist_ok=True)
    mpath = out / "EVIDENCE_MANIFEST.json"
    mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8", newline="\n")
    msha = sha_file(mpath)
    seal = {"schema": "FHS5.PLP.G3.OuterSeal@1",
            "manifest_sha256": msha,
            "candidate": candidate_agg,
            "packs": {w: {"manifest_sha256": packs[w]["manifest_sha256"],
                          "tree_sha256": packs[w]["tree_sha256"]} for w in packs},
            "files": len(rows),
            "redacted_jsons": changed,
            "note": "outer seal; the manifest does not embed this file"}
    (out / "SEAL.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8", newline="\n")
    pins["evidence"] = {"manifest_sha256": msha,
                        "seal_sha256": sha_file(out / "SEAL.json")}
    (out / "FIVE_PINS.json").write_text(json.dumps(pins, ensure_ascii=False, indent=1) + "\n",
                                        encoding="utf-8", newline="\n")
    print(json.dumps({"files": len(rows), "manifest": msha[:12],
                      "seal": pins["evidence"]["seal_sha256"][:12],
                      "candidate": candidate_agg[:12], "redacted": changed}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
