#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge→Native consumption: the Native executor parses the rendered context,
binds every case to the frozen oracle, and runs the two representative cases."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.PARTIES / "collab"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    render = lib.load_json(lib.PARTIES / "bridge" / "render.json")
    explain = lib.load_json(lib.PARTIES / "bridge" / "explain.json")
    resume = lib.load_json(lib.PARTIES / "guide" / "thin_resume.json")
    oracle = lib.load_json(lib.TQAEP / "oracle.json")
    context = render.get("context_utf8") or ""
    cases = sorted(set(re.findall(r"^##\s+(SAMPLE-R\d+)\b", context, re.M)))
    expected = sorted(f"SAMPLE-{k}" for k in oracle["cases"])
    locators = render.get("source_locators") or []
    source_ok = all(l.get("source_sha256") == oracle["source_sha256"] for l in locators)
    clause_ok = all(l.get("clause_sha256") for l in locators)
    ctx_sha_ok = render.get("context_sha256") == lib.sha_bytes(context.encode("utf-8"))
    root = lib.TQAEP / "tmp" / "root"
    if not (root / "case_ok.md").is_file():
        root.mkdir(parents=True, exist_ok=True)
        for p in (lib.REPO / "fixtures").glob("*.md"):
            import shutil
            shutil.copy2(p, root / p.name)
    pos = lib.cli(["--root", str(root), "--input", "case_ok.md",
                   "--sha256", lib.sha_file(root / "case_ok.md")], root,
                  raw_dir=OUT / "raw", tag="native_context_pos")
    neg = lib.cli(["--root", str(root), "--input", "case_missing.md",
                   "--sha256", lib.sha_file(root / "case_missing.md")], root,
                  raw_dir=OUT / "raw", tag="native_context_neg")
    pos_ok = pos["exit"] == 0 and json.loads(pos["stdout"]).get("status") == "COMPLETE"
    neg_ok = neg["exit"] == 2 and json.loads(neg["stdout"]).get("missing") == ["B"]
    resume_finding = ((resume.get("delta") or {}).get("findings") or [None])[0]
    ok = (ctx_sha_ok and cases == expected and source_ok and clause_ok
          and resume.get("state") == "RESUME" and bool(resume_finding)
          and pos_ok and neg_ok and len(explain.get("clause_refs") or []) == len(expected))
    out = {
        "schema": "FHS5.W0NF.NativeContext@1",
        "context_sha256": render.get("context_sha256"),
        "context_sha_match": ctx_sha_ok,
        "cases_in_context": cases,
        "cases_expected": expected,
        "case_set_match": cases == expected,
        "source_locators_ok": source_ok,
        "clause_hashes_present": clause_ok,
        "resume_state": resume.get("state"),
        "resume_finding": resume_finding,
        "native_runs": {"pos_exit": pos["exit"], "neg_exit": neg["exit"],
                        "pos_ok": pos_ok, "neg_ok": neg_ok},
        "verdict": "CONTEXT_CONSUMED" if ok else "CONTEXT_NOT_CONSUMED",
    }
    lib.write_json(OUT / "native_context.json", out)
    print(json.dumps({"verdict": out["verdict"], "cases": len(cases),
                      "pos": pos_ok, "neg": neg_ok,
                      "finding": resume_finding}, ensure_ascii=False, indent=2))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
