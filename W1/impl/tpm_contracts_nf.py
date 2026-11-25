#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 NF-r2 TPM contracts (five views, one work identity).

One work identity produces five separation-of-concerns views:

  PI     semantic intent, ACC, constraints
  PD     bound capability + typed DAG + repo context
  DEV    build effect (38 DEV ECP ids)
  OPS    host effect (29 OPS ECP ids)
  TQAEP  frozen oracle/case set (13 cases, 26 assets)

PI and PD do not swallow each other; DEV and OPS effects are not
interchangeable.  The reviewer is read-only and emits eight-column
findings; it may never modify the subject or the oracle.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

import body_resolver as br
import w1_nf_reader as base

NFError = base.NFError

WORK_IDENTITY_KEYS = ["project_id", "subject_id", "scope", "wave_id", "batch_id", "work_id"]

ROW_RE = re.compile(r"^\|\s*`((?:DEV|OPS)-[A-Z]+-\d{2})`\s*\|(.+)\|\s*$")
CASE_ROW_RE = re.compile(r"^\|\s*`(W1-[A-Z0-9]+-\d{2})`\s*\|(.+)\|\s*$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read(root: Path, name: str) -> str:
    p = br.resolve_inside(root, name)
    return br.decode_utf8(br.read_bounded(p, name), name)


def _table_rows(text: str, pattern) -> list:
    rows = []
    for line in text.splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        rows.append({"id": m.group(1), "cells": cells})
    return rows


def build_contracts(pack_root: str, work_identity: dict) -> dict:
    root = br.canonical_root(pack_root)
    ident = {k: work_identity.get(k) for k in WORK_IDENTITY_KEYS}
    missing_wid = [k for k, v in ident.items() if not v]
    if missing_wid:
        raise NFError("WORK_IDENTITY_INCOMPLETE", ",".join(missing_wid))
    man, mraw = br.load_json_strict(br.resolve_inside(root, base.MANIFEST), base.MANIFEST)
    for k in ("project_id", "subject_id", "scope", "wave_id", "batch_id"):
        if man.get(k) != ident[k]:
            raise NFError("IDENTITY_MISMATCH", k)
    t0 = _read(root, "00_W1_PI_PD.md")
    t1 = _read(root, "01_W1_DEV_ECP.md")
    t2 = _read(root, "02_W1_OPS_ECP.md")
    t3 = _read(root, "03_W1_TQAEP.md")

    pi = {
        "view": "PI",
        "work_id": ident["work_id"],
        "subject_id": ident["subject_id"],
        "scope": ident["scope"],
        "goal": "W1 NF-r2 product entry built and verified",
        "fuo": [r["id"] for r in _table_rows(t0, re.compile(r"^\|\s*`(P0\d)`\s*\|(.+)\|\s*$"))],
        "done": ["P01-P06", "D1-D7", "O1-O6", "13 cases", "12 ACC"],
        "non_goals": ["W2-W4 product", "seven-volume adoption", "public release"],
        "acc": sorted(set(re.findall(r"`(W1-(?:A|CODEX)-0\d)`", t0))),
        "constraints": {"permission_state": "NONE_GRANTED", "unknown_effect": "FAIL_CLOSED"},
    }
    required_pi = ["goal", "fuo", "done", "non_goals", "acc", "constraints"]
    pi_missing = [k for k in required_pi if not pi.get(k)]
    if pi_missing:
        raise NFError("PI_REQUIREMENT_MISSING", ",".join(pi_missing))

    dag = man.get("dag") or {}
    pd = {
        "view": "PD",
        "work_id": ident["work_id"],
        "repo_context": {"root": str(root), "head": (man.get("repository") or {}).get("commit"),
                         "branch": (man.get("repository") or {}).get("branch")},
        "effect_class": "DEV_AND_MINIMAL_OPS_LOCAL_REVERSIBLE",
        "typed_dag": dag,
        "capability": sorted(set((man.get("implementation") or {}).get("api") or [])),
    }
    if not pd["repo_context"]["head"] or not pd["typed_dag"].get("edges") or not pd["capability"]:
        raise NFError("PD_BINDING_MISSING", "repo/dag/capability")

    dev_rows = _table_rows(t1, ROW_RE)
    dev_rows = [r for r in dev_rows if r["id"].startswith("DEV-")]
    if len(dev_rows) != 38:
        raise NFError("ECP_NOT_GRANT", f"DEV rows {len(dev_rows)} != 38")
    ops_rows = _table_rows(t2, ROW_RE)
    ops_rows = [r for r in ops_rows if r["id"].startswith("OPS-")]
    if len(ops_rows) != 29:
        raise NFError("ECP_NOT_GRANT", f"OPS rows {len(ops_rows)} != 29")

    dev = {
        "view": "DEV", "work_id": ident["work_id"], "count": len(dev_rows),
        "ids": [r["id"] for r in dev_rows],
        "rows_missing_cells": [r["id"] for r in dev_rows if len(r["cells"]) < 5],
        "effect": "local build / patch / test",
    }
    ops = {
        "view": "OPS", "work_id": ident["work_id"], "count": len(ops_rows),
        "ids": [r["id"] for r in ops_rows],
        "rows_missing_cells": [r["id"] for r in ops_rows if len(r["cells"]) < 5],
        "effect": "local invoke / reversible activation / restore",
    }

    assets = man.get("assets") or []
    asset_map = {}
    for a in assets:
        if a.get("kind") == "oracle":
            asset_map.setdefault(a.get("case_id"), {})["oracle_sha256"] = a.get("sha256")
            asset_map[a.get("case_id")]["oracle_path"] = a.get("path")
        elif a.get("kind") == "fixture":
            asset_map.setdefault(a.get("case_id"), {})["fixture_sha256"] = a.get("sha256")
            asset_map[a.get("case_id")]["fixture_path"] = a.get("path")
    cases = []
    for cid in base.CASES:
        ent = asset_map.get(cid) or {}
        if not ent.get("oracle_sha256") or not ent.get("fixture_sha256"):
            raise NFError("TQAEP_ORACLE_MISSING", cid)
        for key in ("oracle_path", "fixture_path"):
            p = br.resolve_inside(root, ent[key])
            if sha256_bytes(br.read_bounded(p, ent[key])) != ent[
                    "oracle_sha256" if key == "oracle_path" else "fixture_sha256"]:
                raise NFError("ORACLE_DRIFT", cid)
        cases.append({"case_id": cid, "kind": "CASE",
                      "fixture_sha256": ent["fixture_sha256"],
                      "oracle_sha256": ent["oracle_sha256"]})
    tqaep = {"view": "TQAEP", "work_id": ident["work_id"], "count": len(cases),
             "cases": cases, "subcases": ["N01", "N02", "N03", "N04", "N10", "N11"],
             "runner": "check/run_cases_nf.py"}

    return {
        "schema": "FHS5.PLP.W1.TPMContracts@1",
        "work_identity": ident,
        "identity_count": 1,
        "views": {"PI": pi, "PD": pd, "DEV": dev, "OPS": ops, "TQAEP": tqaep},
        "identity_shared": True,
        "permission_state": "NONE_GRANTED",
        "manifest_sha256": sha256_bytes(mraw),
    }


# ------------------------------------------------------------------- reviewer
def _finding(fid, severity, cls, subject_sha, command, exit_code, raw_sha, repro) -> dict:
    return {"id": fid, "severity": severity, "class": cls, "subject_sha": subject_sha,
            "command": command, "exit": exit_code, "raw_sha256": raw_sha,
            "reproduction": repro}


def review(contracts: dict, pack_root: str, expected_subject_sha: dict | None = None) -> dict:
    """Read-only eight-column review.  Never writes to the subject."""
    root = br.canonical_root(pack_root)
    man, mraw = br.load_json_strict(br.resolve_inside(root, base.MANIFEST), base.MANIFEST)
    subject_sha = sha256_bytes(mraw)
    findings = []
    checks = 0

    # 1. missing binding (B) -> PD
    checks += 1
    if not contracts.get("views", {}).get("PD", {}).get("typed_dag"):
        findings.append(_finding("R-001", "high", "missing_binding", subject_sha,
                                 "review:pd", 1, subject_sha, "build_contracts"))
    # 2. no-source mandatory
    for f in (man.get("pack_files") or []):
        checks += 1
        if not f.get("sha256"):
            findings.append(_finding("R-002", "high", "mandatory_without_source",
                                     subject_sha, "review:pack_files", 1, subject_sha, f.get("path")))
    # 3. bytes wrong
    for f in (man.get("pack_files") or []):
        checks += 1
        p = br.resolve_inside(root, f["path"])
        now = sha256_bytes(br.read_bounded(p, f["path"]))
        if now != f.get("sha256"):
            findings.append(_finding("R-003", "critical", "bytes_wrong", subject_sha,
                                     "review:bytes", 1, now, f["path"]))
    # 4. fake authority
    checks += 1
    for view in contracts.get("views", {}).values():
        if view.get("permission_state") not in (None, "NONE_GRANTED"):
            findings.append(_finding("R-004", "critical", "false_authority", subject_sha,
                                     "review:authority", 1, subject_sha, view.get("view")))
    # 5. subject mutation vs frozen expectation
    if expected_subject_sha:
        checks += 1
        for path, want in expected_subject_sha.items():
            p = br.resolve_inside(root, path)
            if sha256_bytes(br.read_bounded(p, path)) != want:
                findings.append(_finding("R-005", "critical", "subject_mutation_denied",
                                         subject_sha, "review:frozen", 1, subject_sha, path))
    return {
        "schema": "FHS5.PLP.W1.TPMReview@1",
        "reviewer": "independent-readonly",
        "wrote_bytes": 0,
        "checks": checks,
        "findings": findings,
        "finding_count": len(findings),
        "scope_note": "0 defects only means 0 within this scope, never a whole-product pass",
        "subject_sha256": subject_sha,
    }


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("contracts")
    a.add_argument("--pack", required=True)
    a.add_argument("--work-id", required=True)
    a.add_argument("--out")
    b = sub.add_parser("review")
    b.add_argument("--pack", required=True)
    b.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "contracts":
            wi = {"project_id": "FHS-5_PLP", "subject_id": "FHS-5_PLP/W1/CONTROL_PACK",
                  "scope": "W1-NF-01", "wave_id": "W1", "batch_id": "W1-NF-01",
                  "work_id": args.work_id}
            out = build_contracts(args.pack, wi)
        else:
            man, _ = br.load_json_strict(br.resolve_inside(br.canonical_root(args.pack),
                                                          base.MANIFEST), base.MANIFEST)
            wi = {"project_id": man["project_id"], "subject_id": man["subject_id"],
                  "scope": man["scope"], "wave_id": man["wave_id"],
                  "batch_id": man["batch_id"], "work_id": "W1-REVIEW"}
            out = review(build_contracts(args.pack, wi), args.pack)
    except NFError as exc:
        sys.stdout.write(json.dumps({"result": "REJECT", "token": exc.token,
                                     "detail": exc.detail}, ensure_ascii=False, indent=2) + "\n")
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if getattr(args, "out", None):
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
