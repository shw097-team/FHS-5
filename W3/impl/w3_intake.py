#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W3 P01 intake: pack verification + FreezeLedger + W2 requalification matrix.

Read-only with respect to the adopted pack and W2 protected paths. Writes only
inside the caller-provided isolated W3 root.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from w3_common import (
    PROJECT_ID,
    SCOPE,
    SUBJECT_ID,
    W3Error,
    canon,
    digest_obj,
    file_bytes,
    host_identity,
    line_count,
    load_json_strict,
    sha256_file,
    sha256_bytes,
    tree_digest,
)

EXPECTED_ARTIFACT = "FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY"
EXPECTED_SCHEMA = "FHS5.PLP.W3.SourceManifest.NF@2"


def _issue(issues, token, detail="", hard=True):
    issues.append({"token": token, "detail": str(detail), "hard": bool(hard)})


def verify_pack(pack_root, seal_path=None, adoption_path=None, current_path=None) -> dict:
    pack = Path(pack_root)
    issues = []
    man_path = pack / "05_W3_SOURCE_MANIFEST.json"
    try:
        man = load_json_strict(man_path)
    except W3Error as exc:
        return {"ok": False, "issues": [{"token": exc.token, "detail": exc.detail, "hard": True}]}
    ident = man.get("identity", {})
    if man.get("schema") != EXPECTED_SCHEMA:
        _issue(issues, "SCHEMA_UNSUPPORTED", man.get("schema"))
    if ident.get("project_id") != PROJECT_ID:
        _issue(issues, "IDENTITY_MISMATCH", "project_id")
    if ident.get("wave_id") != "W3":
        _issue(issues, "IDENTITY_MISMATCH", "wave_id")
    if ident.get("subject_id") != SUBJECT_ID:
        _issue(issues, "IDENTITY_MISMATCH", "subject_id")
    if ident.get("scope") != SCOPE:
        _issue(issues, "IDENTITY_MISMATCH", "scope")
    if ident.get("artifact_id") != EXPECTED_ARTIFACT:
        _issue(issues, "ARTIFACT_ID_MISMATCH", ident.get("artifact_id"))
    if man.get("selection_state") != "PACK_PRIMARY_SELECTED":
        _issue(issues, "SELECTION_STATE", man.get("selection_state"))

    file_rows = []
    for item in man.get("files", []):
        rel = item.get("path")
        p = pack / rel.replace("/", os.sep)
        ok = p.is_file()
        if ok:
            got_sha = sha256_file(p)
            got_bytes = file_bytes(p)
            got_lines = line_count(p)
            ok = (got_sha == item.get("sha256") and got_bytes == item.get("bytes")
                  and got_lines == item.get("lines"))
            if not ok:
                _issue(issues, "FILE_PIN_MISMATCH", rel)
            file_rows.append({"path": rel, "sha256": got_sha, "bytes": got_bytes, "lines": got_lines})
        else:
            _issue(issues, "FILE_MISSING", rel)
    if len(man.get("files", [])) != 5:
        _issue(issues, "FILE_COUNT", len(man.get("files", [])))

    asset_rows = []
    asset_paths = set()
    for item in man.get("assets", []):
        rel = item.get("path")
        asset_paths.add(rel)
        p = pack / rel.replace("/", os.sep)
        if not p.is_file():
            _issue(issues, "ASSET_MISSING", rel)
            continue
        got_sha = sha256_file(p)
        got_bytes = file_bytes(p)
        got_lines = line_count(p)
        if got_sha != item.get("sha256") or got_bytes != item.get("bytes") or got_lines != item.get("lines"):
            _issue(issues, "ASSET_PIN_MISMATCH", rel)
        asset_rows.append({"path": rel, "sha256": got_sha, "bytes": got_bytes, "lines": got_lines})
    if len(man.get("assets", [])) < 36:
        _issue(issues, "ASSET_COUNT", len(man.get("assets", [])))

    cases = man.get("case_refs", [])
    if len(cases) != 16 or len({c.get("case_id") for c in cases}) != 16:
        _issue(issues, "CASE_REF_COUNT", len(cases))
    for case in cases:
        cid = case.get("case_id")
        if case.get("observed") is not None or case.get("verdict") != "NOT_RUN":
            _issue(issues, "FALSE_OBSERVED", cid)
        for key in ("fixture", "oracle"):
            item = case.get(key) or {}
            rel = item.get("path")
            if rel not in asset_paths:
                _issue(issues, "CASE_ASSET_UNBOUND", f"{cid}:{key}")
                continue
            p = pack / rel.replace("/", os.sep)
            if not p.is_file() or sha256_file(p) != item.get("sha256"):
                _issue(issues, "CASE_ASSET_MISMATCH", f"{cid}:{key}")

    sources = man.get("sources", [])
    if len(sources) != 28:
        _issue(issues, "SOURCE_COUNT", len(sources))
    for src in sources:
        loc = src.get("locator", "")
        if not (loc.startswith("S:") or loc.startswith("R:")):
            _issue(issues, "SOURCE_LOGICAL_LOCATOR", src.get("id"))
        if not src.get("disposition"):
            _issue(issues, "SOURCE_DISPOSITION", src.get("id"))
        for span in src.get("spans", []):
            lo, hi = span.get("lines", [0, 0])
            if not (1 <= lo <= hi <= int(src.get("lines", 0))):
                _issue(issues, "SPAN_OOB", f"{src.get('id')}:{span.get('section')}")

    source_blob = "".join(
        sorted(x.get("id", "") + "\t" + x.get("sha256", "") + "\t" + str(x.get("bytes", ""))
               + "\t" + x.get("locator", "") + "\n" for x in sources)
    ).encode("utf-8")
    source_set = sha256_bytes(source_blob)
    if source_set != man.get("digest_contract", {}).get("source_set_sha256"):
        _issue(issues, "SOURCE_SET_MISMATCH", source_set)

    tree_blob = "".join(
        sorted(x["path"] + "\t" + str(x["bytes"]) + "\t" + x["sha256"] + "\n"
               for x in file_rows + asset_rows)
    ).encode("utf-8")
    tree_sha = sha256_bytes(tree_blob)
    if tree_sha != man.get("digest_contract", {}).get("package_tree_sha256"):
        _issue(issues, "PACKAGE_TREE_MISMATCH", tree_sha)

    raw_05 = sha256_file(man_path)
    text = man_path.read_bytes().decode("utf-8")
    if re.search(r"[A-Za-z]:\\\\", text):
        _issue(issues, "ABSOLUTE_PATH_IN_MANIFEST", "")
    if raw_05 in text:
        _issue(issues, "SELF_HASH", "")

    ext = {}
    for key, path in (("seal", seal_path), ("adoption", adoption_path), ("current", current_path)):
        if not path:
            continue
        p = Path(path)
        if not p.is_file():
            _issue(issues, f"{key.upper()}_MISSING", path)
            continue
        try:
            ext[key] = load_json_strict(p)
            ext[key + "_sha256"] = sha256_file(p)
        except W3Error as exc:
            _issue(issues, f"{key.upper()}_SCHEMA", exc.detail)
    if "seal" in ext:
        if ext["seal"].get("manifest_sha256") != raw_05:
            _issue(issues, "SEAL_MISMATCH", "manifest_sha256")
        if ext["seal"].get("package_tree_sha256") != tree_sha:
            _issue(issues, "SEAL_TREE_MISMATCH", "package_tree_sha256")
        if ext["seal"].get("identity", {}).get("artifact_id") != ident.get("artifact_id"):
            _issue(issues, "SEAL_IDENTITY", "artifact_id")
    if "adoption" in ext:
        if ext["adoption"].get("manifest_sha256") != raw_05:
            _issue(issues, "ADOPTION_MANIFEST", "manifest_sha256")
        if ext["adoption"].get("decision_id") != man.get("adoption", {}).get("decision_id"):
            _issue(issues, "ADOPTION_DECISION", "decision_id")
    if "current" in ext:
        if ext["current"].get("manifest_sha256") != raw_05:
            _issue(issues, "CURRENT_MANIFEST", "manifest_sha256")
        if ext["current"].get("adoption_sha256") != ext.get("adoption_sha256"):
            _issue(issues, "CURRENT_ADOPTION_SHA", "adoption_sha256")
        if ext["current"].get("external_seal_sha256") != ext.get("seal_sha256"):
            _issue(issues, "CURRENT_SEAL_SHA", "external_seal_sha256")

    hard = [x for x in issues if x["hard"]]
    return {
        "ok": not hard,
        "issues": issues,
        "identity": ident,
        "manifest_sha256": raw_05,
        "manifest_bytes": file_bytes(man_path),
        "package_tree_sha256": tree_sha,
        "package_tree_entries": len(file_rows) + len(asset_rows),
        "source_set_sha256": source_set,
        "counts": {
            "files": len(file_rows),
            "assets": len(asset_rows),
            "cases": len(cases),
            "sources": len(sources),
        },
        "file_rows": file_rows,
        "asset_rows": asset_rows,
        "cases": cases,
        "sources": sources,
        "external": {k: v for k, v in ext.items() if not k.endswith("_sha256")},
        "external_sha256": {k: v for k, v in ext.items() if k.endswith("_sha256")},
    }


def build_freeze_ledger(pack_root, verified: dict, w2_root=None, fixture_time=None) -> dict:
    pack = Path(pack_root)
    man = load_json_strict(pack / "05_W3_SOURCE_MANIFEST.json")
    cases = verified["cases"]
    oracle_rows = []
    case_rows = []
    for case in sorted(cases, key=lambda c: c["case_id"]):
        for key, bucket in (("fixture", case_rows), ("oracle", oracle_rows)):
            item = case[key]
            bucket.append({
                "case_id": case["case_id"],
                "path": item["path"],
                "sha256": item["sha256"],
                "bytes": item["bytes"],
            })
    oracle_digest = digest_obj(oracle_rows)
    case_set_digest = digest_obj({"plan": sha256_file(pack / "assets" / "schema" / "W3_PLAN_INDEX.json"),
                                  "cases": [c["case_id"] for c in sorted(cases, key=lambda c: c["case_id"])]})

    w2 = {}
    if w2_root:
        w2 = read_w2_pins(w2_root)
    candidate_digest = (w2.get("five_pins", {}).get("candidate", {}) or {}).get("aggregate_digest")
    if not candidate_digest:
        candidate_digest = "W2_CANDIDATE_UNBOUND"

    pins = {
        "source": {
            "value": verified["source_set_sha256"],
            "kind": "W3 source_set over 28 sources",
            "locator": "05_W3_SOURCE_MANIFEST.json#digest_contract.source_set_sha256",
        },
        "candidate": {
            "value": candidate_digest,
            "kind": "W2 five-member verified product set (upstream frozen input)",
            "locator": w2.get("five_pins_path", "UNBOUND"),
            "candidate_state": "W2_PARTIAL_UPSTREAM",
        },
        "evidence": {
            "value": verified["external_sha256"].get("seal_sha256", "UNBOUND"),
            "kind": "W3 pack external seal over manifest+tree",
            "locator": "EXTERNAL_SEAL.json",
        },
        "oracle": {
            "value": oracle_digest,
            "kind": "digest over 16 design oracle rows (not product-frozen)",
            "locator": "assets/oracles/*.json",
            "design_state": "PROPOSED_DESIGN_ORACLE",
        },
        "case_set": {
            "value": case_set_digest,
            "kind": "digest over plan index + 16 case ids",
            "locator": "assets/schema/W3_PLAN_INDEX.json",
            "design_state": "PROPOSED_DESIGN_FIXTURE",
        },
    }
    vals = [v["value"] for v in pins.values()]
    return {
        "schema": "FHS5.PLP.W3.FreezeLedger.NF@1",
        "subject_id": SUBJECT_ID,
        "scope": SCOPE,
        "pack_manifest_sha256": verified["manifest_sha256"],
        "package_tree_sha256": verified["package_tree_sha256"],
        "pins": pins,
        "pins_distinct": len(set(vals)) == len(vals),
        "pin_count": len(pins),
        "fixture_time": fixture_time or man.get("generated_at"),
        "host_policy": {
            "host_id": host_identity()["host_id"],
            "policy_epoch": host_identity()["policy_epoch"],
            "product_host": "UNBOUND",
        },
        "separate_fields": ["pins", "fixture_time", "host_policy"],
        "w2_upstream": {
            "product_commit": w2.get("product_commit"),
            "delivery_commit": w2.get("delivery_commit"),
            "status": w2.get("status"),
            "writer_state": w2.get("writer_state"),
            "oracle_status": w2.get("oracle_status"),
            "case_set_status": w2.get("case_set_status"),
            "evidence_status": w2.get("evidence_status"),
        },
        "claim": "FROZEN_IDENTITY_STRUCTURE_ONLY",
        "not_claimed": ["W2_NF_VALIDATED", "W3_TECHNICALLY_READY", "W3_NF_VALIDATED"],
    }


def read_w2_pins(w2_root) -> dict:
    root = Path(w2_root)
    cur_path = root / "W2_CURRENT.json"
    out = {"w2_root": str(root)}
    if not cur_path.is_file():
        out["error"] = "W2_CURRENT_UNBOUND"
        return out
    cur = load_json_strict(cur_path)
    five_rel = (cur.get("current_delivery") or {}).get("five_pins")
    five_path = root / five_rel if five_rel else None
    if not five_path or not five_path.is_file():
        out["error"] = "W2_FIVE_PINS_UNBOUND"
        return out
    five = load_json_strict(five_path)
    import subprocess
    head = None
    try:
        pr = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                            capture_output=True, text=True, timeout=20)
        if pr.returncode == 0:
            head = pr.stdout.strip()
    except Exception:
        head = None
    out.update({
        "current": cur,
        "current_sha256": sha256_file(cur_path),
        "five_pins": five,
        "five_pins_path": str(five_path),
        "five_pins_sha256": sha256_file(five_path),
        "product_commit": "dada2354b7c25c8f4a316d9fae93827cef0d194e",
        "delivery_commit": head or "3346076c69b00d65e48fdb9ddf894ac4cc09524b",
        "working_branch": (cur.get("git") or {}).get("working_branch"),
        "candidate_aggregate_digest": (cur.get("current_delivery") or {}).get("candidate_aggregate_digest"),
        "aggregate_algorithm": "UNDECLARED",
        "aggregate_reproducible": False,
        "status": "PARTIAL",
        "writer_state": (cur.get("writer_state") or {}).get("state"),
        "oracle_status": (five.get("oracle") or {}).get("status"),
        "case_set_status": (five.get("case_set") or {}).get("status"),
        "evidence_status": (five.get("evidence") or {}).get("status"),
        "w2_next_owner": cur.get("next_owner"),
    })
    return out


def build_w2_matrix(w2_pins: dict) -> dict:
    five = w2_pins.get("five_pins", {})
    cases = (five.get("case_set") or {}).get("cases", [])
    details = {
        "W2-DEV-01": (True, False, False, "r3 PASS, raw:null; re-run BLOCKED"),
        "W2-DEV-02": (True, False, False, "r3 PASS, raw:null; re-run BLOCKED"),
        "W2-OPS-01": (False, True, False, "no r3 case row; O04/O05 proxy on older receiver"),
        "W2-OPS-02": (True, False, False, "r3 PASS, raw:null; re-run BLOCKED"),
        "W2-EFFECT-01": (True, False, False, "r3 PASS, raw:null; re-run BLOCKED"),
        "W2-AUTH-01": (True, False, False, "r3 PASS, raw:null; would pass for the wrong reason"),
        "W2-RUNNER-01": (True, False, True, "r3 PASS, raw:null; static re-run allowed"),
        "W2-DELTA-01": (False, True, True, "no r3 case row; delta disclosure is not a PASS"),
        "W2-R3-01": (True, False, True, "r3 PASS, raw:null; static re-run allowed"),
        "W2-R3-02": (True, False, False, "r3 PASS, raw:null; re-run BLOCKED"),
        "W2-R3-03": (True, False, False, "r3 PASS, raw:null; re-run BLOCKED"),
        "W2-R3-04": (True, False, True, "r3 PASS, raw:null; static re-run allowed"),
    }
    rows = []
    for cid in cases:
        present, proxy, static_ok, note = details.get(cid, (False, False, False, "UNKNOWN"))
        rows.append({
            "case_id": cid,
            "w3_action": "READ_ONLY_CARRY",
            "state": "NOT_REQUALIFIED",
            "ledger_row_present": present,
            "proxy_only": proxy,
            "static_rerun_allowed": static_ok,
            "verdict_reusable": False,
            "reason": note,
            "owner": "W2 Case Owner (UNBOUND)",
            "resume": "W2-scope named re-authorisation + frozen oracle/case_set bytes",
        })
    return {
        "schema": "FHS5.PLP.W3.W2RequalificationMatrix@1",
        "w2_subject": "FHS-5_PLP/W2/CONTROL_PACK",
        "w2_scope": "W2-NF-01",
        "rows": rows,
        "row_count": len(rows),
        "expected_rows": 12,
        "summary": {
            "product_commit": (five.get("candidate") or {}).get("aggregate_digest"),
            "product_commit_id": "dada2354b7c25c8f4a316d9fae93827cef0d194e",
            "delivery_commit": w2_pins.get("delivery_commit"),
            "aggregate_digest": (five.get("candidate") or {}).get("aggregate_digest"),
            "aggregate_algorithm": "UNDECLARED",
            "aggregate_reproducible": False,
            "r3_ledger_rows": 10,
            "rows_without_case_row": ["W2-OPS-01", "W2-DELTA-01"],
            "raw_attached_rows": 0,
            "verdict_reuse": False,
            "writer_state": (five.get("writer_state") or {}).get("state", "BLOCKED_NOT_ADMITTED"),
            "oracle": (five.get("oracle") or {}).get("status"),
            "case_set": (five.get("case_set") or {}).get("status"),
            "evidence": (five.get("evidence") or {}).get("status"),
            "required_actions": ["R2 freeze", "R3 raw seal", "R4 W2-named writer grant", "R5 retest", "R6 distinct checker", "R7 W2 owner verdict"],
            "blocked": "W2_WRITER_BLOCKED",
            "w3_effect": "W3_TECHNICALLY_READY cannot be claimed; W3 READ/DRAFT/isolated work continues",
        },
        "audit_evidence": {
            "ref": "subagent_w2_audit.md",
            "strength": "READ_ONLY_SUBAGENT_RECOMPUTED_BYTES",
            "findings": [
                "r3 ledger has 10 rows, not 12; all raw:null",
                "W2-OPS-01/W2-DELTA-01 have no case row",
                "r3 verdicts were produced on different gate/admission code",
                "one pinned oracle locator is missing (30_VERIFY/raw/CHECKER_J1_ORACLE.json)",
                "expected_pins.json pins the W1 receiver c6667402, not candidate 768d6318",
                "the 8b4b aggregate digest is not reproducible; algorithm undeclared",
            ],
        },
        "claim": "NO_W2_VERDICT_SIGNED",
    }


def pack_canary(pack_root) -> dict:
    return tree_digest(pack_root, skip_names=("__pycache__",))
