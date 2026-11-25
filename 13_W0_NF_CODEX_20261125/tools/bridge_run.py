#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercise the reused W1 Bridge reference over a real W0 package view:
inspect_package / explain_slice / render_agent_context / compare_context,
plus path, scope and cross-subject negatives."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import tqaep_spec

OUT = lib.PARTIES / "bridge"
PKG = OUT / "package"
BRIDGE = lib.ROOT / "tools" / "w1_bridge_reference.py"


def build_package():
    if PKG.exists():
        shutil.rmtree(PKG)
    (PKG / "cases").mkdir(parents=True)
    for name in ("00_W0_PI_PD.md", "01_W0_DEV_ECP.md", "02_W0_OPS_ECP.md",
                 "03_W0_TQAEP.md", "04_W0_START_THIN_PROMPT.md", "05_W0_SOURCE_MANIFEST.json"):
        shutil.copy2(lib.PACK / name, PKG / name)
    for p in sorted((lib.REPO / "fixtures").glob("*.md")):
        shutil.copy2(p, PKG / "cases" / p.name)
    for key, spec in tqaep_spec.SAMPLE.items():
        lib.write_json(PKG / "cases" / f"oracle_{key}.json", {
            "case": f"SAMPLE-{key}", "fixture": spec["fixture"],
            "expected": {k: v for k, v in spec.items() if k != "fixture"},
        })
    sources = []
    for name in ("00_W0_PI_PD.md", "01_W0_DEV_ECP.md", "02_W0_OPS_ECP.md",
                 "03_W0_TQAEP.md", "04_W0_START_THIN_PROMPT.md", "05_W0_SOURCE_MANIFEST.json"):
        data = (PKG / name).read_bytes()
        sources.append({
            "source_id": name.split("_")[0], "path": name,
            "role": "W0_PACK", "version": "W0-NF-r3-CODEX-PRIMARY",
            "sha256": lib.sha_bytes(data), "bytes": len(data),
            "lines": len(data.decode("utf-8-sig").splitlines()),
        })
    lib.write_json(PKG / "SOURCE_MANIFEST.json", {"schema": "FHS5.W0NF.BridgeSourceManifest@1", "sources": sources})
    identity = {
        "project_id": "FHS-5_PLP", "subject_id": "FHS-5_PLP/W0", "scope": "FHS-5/W0/B0-NF",
        "wave_id": "FHS-5_PLP/W0", "batch_id": "FHS-5/W0/B0-NF",
        "source_manifest_sha256": lib.sha_file(PKG / "SOURCE_MANIFEST.json"),
    }
    lib.write_json(PKG / "05_PLANNED_TQAEP.json", tqaep_spec.bridge_tqaep(PKG, identity))
    write_file_manifest(identity)


def write_file_manifest(identity: dict):
    files = []
    for p in lib.all_files(PKG):
        rel = p.relative_to(PKG).as_posix()
        if rel == "PACKAGE_FILE_MANIFEST.json":
            continue
        files.append({"path": rel, "bytes": len(p.read_bytes()), "sha256": lib.sha_file(p)})
    lib.write_json(PKG / "PACKAGE_FILE_MANIFEST.json", {
        "schema": "FHS5.PLP.FileManifest@proposal-2",
        "identity": identity,
        "files": sorted(files, key=lambda x: x["path"]),
    })


def bridge(args: list[str], tag: str, cwd=None) -> dict:
    raw = OUT / "raw"
    res = lib.run([sys.executable, str(BRIDGE), *args], cwd or lib.ROOT, timeout=60, raw_dir=raw, tag=tag)
    (OUT / f"{tag}.exit").write_text(str(res["exit"]), encoding="utf-8")
    return res


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build_package()
    results = {}

    r = bridge(["inspect", "--root", str(PKG), "--manifest", "PACKAGE_FILE_MANIFEST.json",
                "--out", str(OUT / "inspect.json")], "inspect")
    results["inspect"] = {"exit": r["exit"], "stdout_sha": r["stdout_sha256"]}
    insp = lib.load_json(OUT / "inspect.json")
    results["inspect_counts"] = insp.get("counts")

    r = bridge(["explain", "--pack-root", str(PKG), "--view", "all",
                "--out", str(OUT / "explain.json")], "explain")
    results["explain"] = {"exit": r["exit"], "stdout_sha": r["stdout_sha256"]}
    expl = lib.load_json(OUT / "explain.json")
    results["explain_missing"] = expl.get("missing")
    results["explain_cases"] = len(expl.get("clause_refs") or [])

    r = bridge(["render", "--explanation", str(OUT / "explain.json"),
                "--target-host", "Codex", "--out", str(OUT / "render.json")], "render")
    results["render"] = {"exit": r["exit"], "stdout_sha": r["stdout_sha256"]}
    rend = lib.load_json(OUT / "render.json")
    results["render_context_sha"] = rend.get("context_sha256")

    # compare: controlled mutation in an isolated copy (never the source pack)
    after = lib.ROOT / "05_TQAEP" / "tmp" / "bridge_after"
    lib.copy_tree_clean(PKG, after)
    target = after / "cases" / "case_ok.md"
    target.write_bytes(target.read_bytes().replace(b"A", b"C", 1))
    identity = lib.load_json(OUT / "inspect.json")["identity"]
    files = []
    for p in lib.all_files(after):
        rel = p.relative_to(after).as_posix()
        if rel == "PACKAGE_FILE_MANIFEST.json":
            continue
        files.append({"path": rel, "bytes": len(p.read_bytes()), "sha256": lib.sha_file(p)})
    lib.write_json(after / "PACKAGE_FILE_MANIFEST.json", {
        "schema": "FHS5.PLP.FileManifest@proposal-2", "identity": identity,
        "files": sorted(files, key=lambda x: x["path"])})
    r = bridge(["inspect", "--root", str(after), "--manifest", "PACKAGE_FILE_MANIFEST.json",
                "--out", str(OUT / "inspect_after.json")], "inspect_after")
    r = bridge(["compare", "--before", str(OUT / "inspect.json"), "--after", str(OUT / "inspect_after.json"),
                "--out", str(OUT / "compare.json")], "compare")
    results["compare"] = {"exit": r["exit"], "stdout_sha": r["stdout_sha256"]}
    cmp = lib.load_json(OUT / "compare.json")
    results["compare_changed"] = [c.get("path") for c in cmp.get("changed") or []]

    # negatives: path escape, widened scope, cross-subject compare
    esc = lib.ROOT / "05_TQAEP" / "tmp" / "bridge_escape"
    lib.copy_tree_clean(PKG, esc)
    m = lib.load_json(esc / "PACKAGE_FILE_MANIFEST.json")
    m["files"].append({"path": "../escape.md", "bytes": 0, "sha256": "0" * 64})
    lib.write_json(esc / "PACKAGE_FILE_MANIFEST.json", m)
    r = bridge(["inspect", "--root", str(esc), "--manifest", "PACKAGE_FILE_MANIFEST.json"],
               "inspect_escape")
    try:
        esc_json = json.loads(r["stdout"])
    except Exception:
        esc_json = {}
    esc_codes = [u.get("code") for u in esc_json.get("unresolved_refs") or []]
    results["path_escape"] = {"exit": r["exit"], "codes": esc_codes,
                              "mismatched": (esc_json.get("counts") or {}).get("mismatched"),
                              "refused": "PATH_OUTSIDE_ROOT" in esc_codes}

    r = lib.run([sys.executable, str(lib.ROOT / "tools" / "scope_probe.py"),
                 str(OUT / "explain.json")], lib.ROOT, 30,
                raw_dir=OUT / "raw", tag="render_scope_drift")
    results["scope_drift"] = {"exit": r["exit"], "stdout": r["stdout"].strip()[:100],
                              "refused": r["exit"] == 0 and "SCOPE_DENIED" in r["stdout"]}

    cross = lib.load_json(OUT / "inspect_after.json")
    cross["identity"]["subject_id"] = "FHS-5_PLP/W2"
    lib.write_json(OUT / "inspect_cross.json", cross)
    r = bridge(["compare", "--before", str(OUT / "inspect.json"), "--after", str(OUT / "inspect_cross.json")],
               "compare_cross")
    results["cross_subject"] = {"exit": r["exit"], "stderr": r["stderr"].strip()[:200]}

    summary = {
        "schema": "FHS5.W0NF.BridgeRun@1",
        "impl": "REUSE 11_W1_EXECUTION_20261124/impl/w1_bridge_reference.py (copied)",
        "bridge_sha256": lib.sha_file(BRIDGE),
        "package": str(PKG),
        "package_manifest_sha256": lib.sha_file(PKG / "PACKAGE_FILE_MANIFEST.json"),
        "results": results,
        "reconciliation_notes": [
            "declared excludes PACKAGE_FILE_MANIFEST.json itself; actual includes it, so actual = declared + 1.",
            "primary_manifest is null because this W0 view has no W1 primary manifest; "
            "primary_manifest_entries=0 is expected, not a silent pass.",
        ],
        "security": {
            "path_escape_refused": bool(results["path_escape"]["refused"]),
            "scope_drift_refused": bool(results["scope_drift"]["refused"]),
            "cross_subject_refused": results["cross_subject"]["exit"] == 2,
        },
        "claim_ceiling": "AUTHOR_REFERENCE_IMPL_REUSED; NOT W1 38+28 DENOMINATOR",
        "not_covered": ["Bridge 38+28 full denominator", "Host install/register/invoke"],
    }
    lib.write_json(OUT / "bridge_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    ok = (results["inspect"]["exit"] == 0 and results["explain"]["exit"] == 0
          and results["render"]["exit"] == 0 and results["compare"]["exit"] == 0
          and all(summary["security"].values())
          and results["inspect_counts"]["mismatched"] == 0
          and results["inspect_counts"]["undeclared"] == 0)
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
