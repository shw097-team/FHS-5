#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 TPM contracts, profile-driven (NF-r4 / R01).

One work identity -> five separation-of-concerns views (PI, PD, DEV, OPS,
TQAEP).  Nothing in the generic path hardcodes the W1 denominators: a profile
manifest declares its own expectations and its own required sections.  The W1
profile keeps the real 38 DEV / 29 OPS / 13 case denominators.

The reviewer is read-only, emits the eight-column Finding contract and derives
each Finding from a real observation payload (never from the subject sha).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import body_resolver as br
import w1_nf_reader as base

NFError = base.NFError

ROW_RE = re.compile(r"^\|\s*`((?:DEV|OPS)-[A-Z]+-\d{2})`\s*\|(.+)\|\s*$")
CASE_ROW_RE = re.compile(r"^\|\s*`(W1-[A-Z0-9]+-\d{2})`\s*\|(.+)\|\s*$")
FIELD_RE = re.compile(r"\*\*([A-Za-z_ ]+)\*\*\s*[：:]\s*(.+)$")
JOB_RE = re.compile(r"Job to be done\**\s*[：:]\s*(.+)$")

# Profile registry -----------------------------------------------------------
PROFILES = {
    "W1": {
        "schema": "FHS5.PLP.W1.SourceManifest.NF@1",
        "expect": {"dev": 38, "ops": 29, "cases": 13, "pack_files": 5, "assets": 26},
        "dev_file": "01_W1_DEV_ECP.md",
        "ops_file": "02_W1_OPS_ECP.md",
        "case_file": "03_W1_TQAEP.md",
        "pi_file": "00_W1_PI_PD.md",
        "start_file": "04_W1_START_THIN_PROMPT.md",
        "sections": ("GOAL", "SOURCE", "SPEC", "EXECUTE", "HARNESS LOOP",
                     "DONE", "STOP", "RESUME"),
    },
    "GENERIC": {
        "schema": None,   # decided from the manifest at runtime
        "expect": {},
        "sections": (),
    },
}

REQUIRED_VIEW_FIELDS_W1 = {
    "PI": ("subject_id", "scope", "goal", "fuo", "done", "non_goals", "acc", "constraints"),
    "PD": ("repo_context", "effect_class", "typed_dag", "capability", "owner"),
    "DEV": ("ids", "rows"),
    "OPS": ("ids", "rows"),
    "TQAEP": ("cases", "runner", "subcases"),
}

REQUIRED_VIEW_FIELDS_GENERIC = {
    "PI": ("subject_id", "scope", "goal", "constraints"),
    "PD": ("repo_context", "effect_class", "typed_dag"),
    "DEV": ("rows",),
    "OPS": ("rows",),
    "TQAEP": ("runner",),
}


def required_fields(profile: str) -> dict:
    return REQUIRED_VIEW_FIELDS_W1 if profile == "W1" else REQUIRED_VIEW_FIELDS_GENERIC


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _canon_sha(obj) -> str:
    return sha256_bytes(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":")).encode("utf-8"))


def _read(root: Path, name: str) -> str:
    p = br.resolve_inside(root, name)
    return br.decode_utf8(br.read_bounded(p, name), name)


def _table_rows(text: str, pattern=ROW_RE) -> list:
    rows = []
    for line in text.splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        rows.append({"id": m.group(1), "cells": [c.strip() for c in m.group(2).split("|")]})
    return rows


def _field(text: str, label: str) -> str | None:
    for line in text.splitlines():
        m = FIELD_RE.search(line)
        if m and m.group(1).strip().lower() == label.lower():
            return m.group(2).strip()
    return None


def _bullets(text: str, start_marker: str, limit: int = 12) -> list:
    out, on = [], False
    for line in text.splitlines():
        if start_marker in line:
            on = True
            continue
        if on:
            s = line.strip()
            if s.startswith("- "):
                out.append(s[2:].strip())
            elif s.startswith("#") or (s and not s.startswith("-") and out):
                break
            if len(out) >= limit:
                break
    return out


def _table_block(text: str, marker: str, limit: int = 15) -> list:
    """Return the data rows of the first Markdown table after ``marker``."""
    rows, on = [], False
    for line in text.splitlines():
        if marker in line:
            on = True
            continue
        if not on:
            continue
        s = line.strip()
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells) or cells[0].startswith("層"):
            continue
        rows.append(cells)
        if len(rows) >= limit:
            break
    return rows


def _paragraph(text: str, marker: str) -> str:
    for line in text.splitlines():
        if marker in line:
            tail = line.split(marker, 1)[1]
            return tail.lstrip("：: ").strip()
    return ""


def resolve_profile(man: dict) -> tuple[str, dict]:
    schema = man.get("schema")
    for name, prof in PROFILES.items():
        if prof["schema"] and prof["schema"] == schema:
            return name, prof
    if isinstance(schema, str) and ".SourceManifest.NF@" in schema:
        return "GENERIC", PROFILES["GENERIC"]
    raise NFError("SCHEMA_UNSUPPORTED", str(schema))


def build_contracts(pack_root: str, work_identity: dict) -> dict:
    root = br.canonical_root(pack_root)
    cands = sorted(p.name for p in root.glob("*SOURCE_MANIFEST*.json"))
    if not cands:
        raise NFError("PACK_INCOMPLETE_LOCAL", "no manifest")
    man_name = cands[0]
    man, mraw = br.load_json_strict(br.resolve_inside(root, man_name), man_name)
    profile_name, prof = resolve_profile(man)
    ident = {k: work_identity.get(k) for k in
             ("project_id", "subject_id", "scope", "wave_id", "batch_id", "work_id")}
    missing = [k for k, v in ident.items() if not v]
    if missing:
        raise NFError("WORK_IDENTITY_INCOMPLETE", ",".join(missing))
    for k in ("project_id", "scope", "wave_id", "batch_id"):
        if man.get(k) and man.get(k) != ident[k]:
            raise NFError("IDENTITY_MISMATCH", k)

    expect = prof.get("expect") or {}
    files = man.get("pack_files") or []
    if expect.get("pack_files") and len(files) != expect["pack_files"]:
        raise NFError("PACK_INCOMPLETE_LOCAL", f"pack_files {len(files)}")

    texts = {}
    for f in files:
        rel = f["path"]
        texts[rel] = _read(root, rel)

    pi_text = texts.get(prof.get("pi_file", ""), "")
    goal = None
    for line in pi_text.splitlines():
        m = JOB_RE.search(line)
        if m:
            goal = m.group(1).strip()
            break
    if not goal:
        goal = (man.get("scope") or "")[:200]
    done = [" | ".join(r) for r in _table_block(pi_text, "**Done 分層**", 6)]
    if not done:
        done = _bullets(pi_text, "**Done 分層**", 6)
    ng_para = _paragraph(pi_text, "**Non-goals**")
    non_goals = [x.strip() for x in re.split(r"[；;]", ng_para) if x.strip()][:8]
    acc = sorted(set(re.findall(r"`(W1-(?:A|CODEX)-0\d)`", pi_text)))
    fuo = sorted(set(re.findall(r"`(P0\d)`", pi_text)))

    pi = {
        "view": "PI", "work_id": ident["work_id"], "subject_id": ident["subject_id"],
        "scope": ident["scope"], "profile": profile_name,
        "goal": goal, "fuo": fuo, "done": done, "non_goals": non_goals,
        "acc": acc,
        "constraints": {"permission_state": "NONE_GRANTED",
                        "unknown_effect": "FAIL_CLOSED",
                        "ecp_is_grant": False, "advice_is_grant": False},
        "sources": [{"path": f["path"], "sha256": f["sha256"]} for f in files],
    }

    repo = man.get("repository") or {}
    head = None
    if (root / ".git").exists():
        try:
            r = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                               capture_output=True, text=True, timeout=30)
            head = r.stdout.strip() if r.returncode == 0 else None
        except Exception:
            head = None
    pd = {
        "view": "PD", "work_id": ident["work_id"], "profile": profile_name,
        "repo_context": {"root": str(root), "head": head or repo.get("commit"),
                         "branch": repo.get("branch")},
        "effect_class": "DEV_AND_MINIMAL_OPS_LOCAL_REVERSIBLE",
        "typed_dag": man.get("dag") or {"nodes": [], "edges": []},
        "capability": sorted(set((man.get("implementation") or {}).get("api") or [])),
        "owner": (man.get("authority") or {}).get("owner_decisions", [{}])[0].get("id"),
    }

    def _rows(name: str, kind: str) -> dict:
        rows = _table_rows(texts.get(name, ""))
        rows = [r for r in rows if r["id"].startswith(kind)]
        want = expect.get("dev" if kind == "DEV-" else "ops")
        if want and len(rows) != want:
            raise NFError("ECP_NOT_GRANT", f"{kind} rows {len(rows)} != {want}")
        out = []
        for r in rows:
            c = r["cells"] + [""] * (5 - len(r["cells"]))
            out.append({"id": r["id"], "operation": c[0], "pre": c[1],
                        "post": c[2], "recovery": c[3], "step": c[4],
                        "cells": len(r["cells"])})
        return {"view": kind[:-1], "work_id": ident["work_id"], "profile": profile_name,
                "count": len(out), "ids": [o["id"] for o in out], "rows": out,
                "writeset_targets": sorted({o["step"] for o in out if o["step"]})}

    dev = _rows(prof.get("dev_file", ""), "DEV-")
    ops = _rows(prof.get("ops_file", ""), "OPS-")

    cases = []
    asset_map = {}
    for a in man.get("assets") or []:
        asset_map.setdefault(a.get("case_id"), {})[a.get("kind")] = a
    case_text = texts.get(prof.get("case_file", ""), "")
    for cr in _table_rows(case_text, CASE_ROW_RE):
        cid = cr["id"]
        cells = cr["cells"] + [""] * (7 - len(cr["cells"]))
        ent = asset_map.get(cid) or {}
        if ent.get("oracle"):
            p = br.resolve_inside(root, ent["oracle"]["path"])
            if sha256_bytes(br.read_bounded(p, ent["oracle"]["path"])) != ent["oracle"]["sha256"]:
                raise NFError("ORACLE_DRIFT", cid)
        cases.append({"case_id": cid, "kind": cells[0], "requirement": cells[1],
                      "pos": cells[2], "neg": cells[3],
                      "fixture_sha256": (ent.get("fixture") or {}).get("sha256"),
                      "oracle_sha256": (ent.get("oracle") or {}).get("sha256")})
    want_cases = expect.get("cases")
    if want_cases and len(cases) != want_cases:
        raise NFError("CASE_SET_INCOMPLETE", f"{len(cases)} != {want_cases}")
    subcases = [s for s in ("N01", "N02", "N03", "N04", "N10", "N11") if s in case_text]
    tqaep = {"view": "TQAEP", "work_id": ident["work_id"], "profile": profile_name,
             "count": len(cases), "cases": cases, "subcases": subcases,
             "runner": "check/run_cases_nf.py",
             "frozen": bool(cases) and all(c["oracle_sha256"] for c in cases)}

    contracts = {"schema": "FHS5.PLP.W1.TPMContracts@2",
                 "profile": profile_name,
                 "work_identity": ident, "identity_count": 1,
                 "views": {"PI": pi, "PD": pd, "DEV": dev, "OPS": ops, "TQAEP": tqaep},
                 "identity_shared": True,
                 "permission_state": "NONE_GRANTED",
                 "manifest_path": man_name,
                 "manifest_sha256": sha256_bytes(mraw)}
    for view, fields in required_fields(profile_name).items():
        missing_fields = [f for f in fields if not contracts["views"][view].get(f)]
        if missing_fields:
            raise NFError("CONTRACT_FIELD_MISSING", f"{view}:{','.join(missing_fields)}")
    return contracts


# ------------------------------------------------------------------- reviewer
def _finding(fid, severity, cls, command, subject_path, observed, expected,
             change_cone) -> dict:
    raw = {"observed": observed, "expected": expected, "subject_path": subject_path}
    return {"id": fid, "severity": severity, "class": cls,
            "subject_sha": _canon_sha(observed),
            "command": command, "exit": 1 if severity != "info" else 0,
            "raw_sha256": _canon_sha(raw), "reproduction": command,
            "subject_path": subject_path, "expected": expected,
            "observed": observed, "change_cone": change_cone,
            "raw": raw}


def review(contracts: dict, pack_root: str, expected_subject_sha: dict | None = None) -> dict:
    root = br.canonical_root(pack_root)
    man_name = contracts.get("manifest_path") or base.MANIFEST
    man, mraw = br.load_json_strict(br.resolve_inside(root, man_name), man_name)
    findings, checks = [], 0

    def add(*a, **k):
        findings.append(_finding(*a, **k))

    # 1 contract completeness (the 'B' child and required columns)
    for view in ("PI", "PD", "DEV", "OPS", "TQAEP"):
        checks += 1
        v = (contracts.get("views") or {}).get(view) or {}
        req = required_fields(contracts.get("profile", "W1"))
        missing = [f for f in req[view] if not v.get(f)]
        if missing:
            add("R-001", "high", "contract_missing_field", "review:contract", view,
                {"view": view, "missing": missing}, {"missing": []},
                ["W1/impl/tpm_contracts_nf.py"])
    for kind in ("DEV", "OPS"):
        for row in ((contracts.get("views") or {}).get(kind) or {}).get("rows") or []:
            checks += 1
            empties = [k for k in ("operation", "pre", "post", "recovery") if not row.get(k)]
            if empties or row.get("cells", 5) < 5:
                add("R-002", "high", "missing_child_b", "review:rows", row["id"],
                    {"id": row["id"], "empty": empties, "cells": row.get("cells")},
                    {"all_five_columns": True}, ["W1/impl/tpm_contracts_nf.py"])

    # 2 mandatory without a real source
    for f in man.get("pack_files") or []:
        checks += 1
        if not f.get("sha256") or not f.get("bytes"):
            add("R-003", "high", "mandatory_without_source", "review:pack_files",
                f.get("path"), {"path": f.get("path"), "sha256": f.get("sha256")},
                {"sha256": "64 hex"}, ["control_pack/" + str(f.get("path"))])
    for s in (contracts.get("views", {}).get("PI", {}) or {}).get("sources") or []:
        checks += 1
        if not s.get("sha256"):
            add("R-004", "medium", "mandatory_without_source", "review:pi_sources",
                s.get("path"), s, {"sha256": "64 hex"}, ["W1/impl/tpm_contracts_nf.py"])

    # 3 wrong bytes / 4 wrong span
    for f in man.get("pack_files") or []:
        checks += 1
        p = br.resolve_inside(root, f["path"])
        now = sha256_bytes(br.read_bounded(p, f["path"]))
        if now != f.get("sha256"):
            add("R-005", "critical", "bytes_wrong", "review:bytes", f["path"],
                {"sha256": now}, {"sha256": f.get("sha256")}, ["control_pack/" + f["path"]])
        text = br.decode_utf8(br.read_bounded(p, f["path"]), f["path"])
        for c in br.parse_clauses(text, f["path"], now):
            checks += 1
            body_sha = sha256_bytes(c["text"].encode("utf-8"))
            bad_span = c["line_end"] < c["line_start"]
            bad_body = body_sha != c["text_sha256"]
            in_range = 1 <= c["line_start"] <= len(text.splitlines())
            if bad_span or bad_body or not in_range:
                add("R-006", "high", "span_wrong", "review:span", c["clause_id"],
                    {"line_start": c["line_start"], "line_end": c["line_end"],
                     "body_sha_matches": not bad_body, "in_range": in_range},
                    {"line_end>=line_start": True, "body_sha_matches": True},
                    [f["path"]])

    # 5 fake authority anywhere in the contract tree
    checks += 1
    blob = json.dumps(contracts, ensure_ascii=False)
    for bad in ("permission_state\": \"GRANT", "advice_is_grant\": true", "ecp_is_grant\": true"):
        if bad in blob:
            add("R-007", "critical", "false_authority", "review:authority", "contracts",
                {"token": bad}, {"permission_state": "NONE_GRANTED"},
                ["W1/impl/tpm_contracts_nf.py", "W1/impl/guide_nf.py"])

    # 6 declared NEG markers that yield no negative row
    for f in man.get("pack_files") or []:
        p = br.resolve_inside(root, f["path"])
        text = br.decode_utf8(br.read_bounded(p, f["path"]), f["path"])
        for c in br.parse_clauses(text, f["path"], f.get("sha256") or ""):
            checks += 1
            if "拒" in c["heading"] and not c["negatives"]:
                add("R-008", "medium", "neg_missing", "review:neg", c["clause_id"],
                    {"heading": c["heading"], "negatives": []},
                    {"negatives": [">=1 token"]}, [f["path"]])

    # 7 subject mutation vs frozen expectation
    if expected_subject_sha:
        checks += 1
        for path, want in expected_subject_sha.items():
            p = br.resolve_inside(root, path)
            got = sha256_bytes(br.read_bounded(p, path))
            if got != want:
                add("R-009", "critical", "subject_mutation_denied", "review:frozen",
                    path, {"sha256": got}, {"sha256": want}, [path])

    first = findings[0]["id"] if findings else None
    cone = sorted({c for f in findings for c in f["change_cone"]})
    return {
        "schema": "FHS5.PLP.W1.TPMReview@2",
        "reviewer": "independent-readonly",
        "wrote_bytes": 0,
        "checks": checks,
        "findings": findings,
        "finding_count": len(findings),
        "first_fail": first,
        "change_cone": cone,
        "scope_note": "0 defects only means 0 within this scope",
        "manifest_sha256": sha256_bytes(mraw),
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
            man_name = sorted(p.name for p in br.canonical_root(args.pack)
                              .glob("*SOURCE_MANIFEST*.json"))[0]
            man, _ = br.load_json_strict(br.resolve_inside(br.canonical_root(args.pack),
                                                           man_name), man_name)
            wi = {"project_id": man["project_id"], "subject_id": man["subject_id"],
                  "scope": man["scope"], "wave_id": man["wave_id"],
                  "batch_id": man["batch_id"], "work_id": args.work_id}
            out = build_contracts(args.pack, wi)
        else:
            man_name = sorted(p.name for p in br.canonical_root(args.pack)
                              .glob("*SOURCE_MANIFEST*.json"))[0]
            man, _ = br.load_json_strict(br.resolve_inside(br.canonical_root(args.pack),
                                                           man_name), man_name)
            wi = {"project_id": man["project_id"], "subject_id": man["subject_id"],
                  "scope": man["scope"], "wave_id": man["wave_id"],
                  "batch_id": man["batch_id"], "work_id": "REVIEW"}
            out = review(build_contracts(args.pack, wi), args.pack)
    except NFError as exc:
        sys.stdout.write(json.dumps({"result": "REJECT", "token": exc.token,
                                     "detail": exc.detail}, ensure_ascii=False,
                                    indent=2) + "\n")
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if getattr(args, "out", None):
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
