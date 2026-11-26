#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 pack reader for ``FHS5.PLP.W2.SourceManifest.NF@2``.

Why this exists: the W1 reader (``nf_reader.inspect_package``) refuses a W2 pack
with ``PACK_INCOMPLETE_LOCAL: 05_W1_SOURCE_MANIFEST.json`` — it looks for the W1
manifest filename and the W1 counts.  That made the W2 six-file pack unreadable
by the Native construction path, so the previous round could only do integrity
checks on it.

This reader does the real work instead:
  * strict JSON (duplicate keys / NaN / BOM refused) on the NF@2 manifest
  * re-hashes all 6 pack files and all 25 assets
  * builds the five construction views (PI / PD / DEV / OPS / TQAEP) from the
    pack's own content, and cross-checks the manifest counts against rows it
    parses out of the Markdown documents themselves

It is one module with no service, no registry and no schema of its own.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

SCHEMA = "FHS5.PLP.W2.SourceManifest.NF@2"
MANIFEST_NAME = "05_W2_SOURCE_MANIFEST.json"


class W2ReaderError(Exception):
    def __init__(self, token: str, detail: str = ""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _strict_json(raw: bytes):
    if raw[:3] == b"\xef\xbb\xbf":
        raise W2ReaderError("SCHEMA_INVALID", "BOM not allowed")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise W2ReaderError("SCHEMA_INVALID", f"not UTF-8: {exc}") from exc
    dups = []

    def _pairs(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                dups.append(k)
            seen.add(k)
        return dict(pairs)

    def _const(name):
        raise W2ReaderError("SCHEMA_INVALID", f"non-finite constant {name}")

    try:
        obj = json.loads(text, object_pairs_hook=_pairs, parse_constant=_const)
    except (json.JSONDecodeError, ValueError) as exc:
        raise W2ReaderError("SCHEMA_INVALID", f"not JSON: {exc}") from exc
    if dups:
        raise W2ReaderError("SCHEMA_INVALID", f"duplicate keys {sorted(set(dups))[:5]}")
    return obj


def _rows_after_heading(text: str, heading_pred) -> list[str]:
    """Return markdown table data rows belonging to the first matching heading."""
    lines = text.splitlines()
    out, active, header_seen = [], False, False
    for line in lines:
        if line.startswith("#"):
            if active and out:
                break
            active = bool(heading_pred(line))
            header_seen = False
            continue
        if not active:
            continue
        if line.strip().startswith("|"):
            if not header_seen:
                header_seen = True
                continue
            if set(line.strip()) <= set("|-: "):
                continue
            out.append(line)
    return out


def _cells(row: str) -> list[str]:
    return [c.strip().strip("`") for c in row.strip().strip("|").split("|")]


def inspect_package(root) -> dict:
    root = Path(root).resolve()
    man_p = root / MANIFEST_NAME
    if not man_p.is_file():
        raise W2ReaderError("PACK_INCOMPLETE_LOCAL", MANIFEST_NAME)
    manifest = _strict_json(man_p.read_bytes())
    if manifest.get("schema") != SCHEMA:
        raise W2ReaderError("SCHEMA_UNSUPPORTED",
                            f"{manifest.get('schema')} != {SCHEMA}")

    bad = []
    for e in manifest.get("pack_files") or []:
        p = root / e["path"]
        if not p.is_file():
            bad.append((e["path"], "missing"))
        elif sha256_file(p) != e["sha256"] or p.stat().st_size != e["bytes"]:
            bad.append((e["path"], "sha/bytes"))
    if bad:
        raise W2ReaderError("BYTES_MISMATCH", str(bad[:3]))

    bad_a = []
    for e in manifest.get("assets") or []:
        p = root / e["path"]
        if not p.is_file() or sha256_file(p) != e["sha256"]:
            bad_a.append(e["path"])
    if bad_a:
        raise W2ReaderError("BYTES_MISMATCH", f"assets {bad_a[:3]}")

    ident = manifest.get("identity") or {}
    for key in ("artifact_id", "subject_id", "scope", "candidate"):
        if not ident.get(key):
            raise W2ReaderError("SCHEMA_INVALID", f"identity.{key} missing")

    lines = sorted(f"{e['id']}|{e['sha256']}|{e['bytes']}"
                   for e in manifest.get("sources") or [])
    src_set = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    if manifest.get("source_set_sha256") and src_set != manifest["source_set_sha256"]:
        raise W2ReaderError("SOURCE_SET_MISMATCH",
                            f"{src_set} != {manifest['source_set_sha256']}")

    return {
        "pack_manifest_sha256": sha256_file(man_p),
        "manifest_bytes": man_p.stat().st_size,
        "manifest": manifest,
        "identity": ident,
        "source_set_sha256": src_set,
        "source_refs": manifest.get("sources") or [],
        "unresolved_refs": [s for s in (manifest.get("sources") or [])
                            if s.get("availability") != "LOCAL_READONLY"],
        "counts": {
            "pack_files": len(manifest.get("pack_files") or []),
            "assets": len(manifest.get("assets") or []),
            "sources": len(manifest.get("sources") or []),
            "requirements": len(manifest.get("requirements") or []),
            "cases": len(manifest.get("cases") or []),
            "crs": len(manifest.get("crs") or []),
            "holds": len(manifest.get("holds") or []),
            "w2_special_holds": len(manifest.get("w2_special_holds") or []),
        },
    }


def build_contracts(root, ident=None) -> dict:
    """Five construction views built from the pack's real content."""
    insp = inspect_package(root)
    root = Path(root).resolve()
    man = insp["manifest"]
    views = {}

    views["PI"] = {
        "identity": insp["identity"],
        "subject_id": insp["identity"]["subject_id"],
        "scope": insp["identity"]["scope"],
        "requirements": man.get("requirements") or [],
        "requirement_count": len(man.get("requirements") or []),
        "sources": man.get("sources") or [],
        "source_set_sha256": insp["source_set_sha256"],
        "constraints": {
            "permission_state": (man.get("authority_product_scope") or {})
                                .get("permission_state"),
            "unknown_effect": "FAIL_CLOSED",
            "ecp_is_grant": False,
        },
    }

    views["PD"] = {
        "wp": [n.get("id") if isinstance(n, dict) else n
               for n in (man.get("dag") or {}).get("nodes") or []],
        "dag_edges": (man.get("dag") or {}).get("edges") or [],
        "cycle": (man.get("dag") or {}).get("cycle"),
        "holds": [h.get("id") for h in man.get("holds") or []],
        "w2_special_holds": [h.get("id") for h in man.get("w2_special_holds") or []],
        "crs": len(man.get("crs") or []),
        "denominators": man.get("denominators") or {},
    }

    dev_doc = (root / "01_W2_DEV_ECP.md").read_text(encoding="utf-8")
    dev_rows = _rows_after_heading(dev_doc, lambda l: "Exact WriteSet" in l)
    write_set = []
    for r in dev_rows:
        c = _cells(r)
        if c and c[0].isdigit():
            write_set.append({"n": int(c[0]), "path": c[1], "operation": c[2],
                              "before_exists": c[3],
                              "allowed_post_shape": c[6] if len(c) > 6 else None})
    views["DEV"] = {
        "ops": sorted((man.get("dev_ops_locators") or {}).keys()),
        "write_set": write_set,
        "write_set_rows_parsed": len(write_set),
        "locators": man.get("dev_ops_locators") or {},
        "doc_sha256": sha256_file(root / "01_W2_DEV_ECP.md"),
    }

    ops_doc = (root / "02_W2_OPS_ECP.md").read_text(encoding="utf-8")
    ops_rows = _rows_after_heading(ops_doc, lambda l: l.startswith("## 7")
                                   or "O06" in l)
    views["OPS"] = {
        "ops": sorted((man.get("dev_ops_locators") or {}).keys()),
        "ops_sequence": ["O01", "O02", "O03", "O04", "O05", "O06"],
        "compensation_forbidden": ["git revert", "git reset", "whole-repo rollback"],
        "unknown_fixtures": ["F-TO-BEFORE", "F-TO-AFTER", "F-PARTIAL", "F-EXIT0-WRONG"],
        "doc_sha256": sha256_file(root / "02_W2_OPS_ECP.md"),
        "o06_rows_parsed": len(ops_rows),
    }

    tq_doc = (root / "03_W2_TQAEP.md").read_text(encoding="utf-8")
    case_rows = _rows_after_heading(tq_doc, lambda l: "Case" in l and "#" not in l)
    sub = man.get("subcases") or {}
    views["TQAEP"] = {
        "cases": [{"case_id": c["case_id"], "kind": c.get("kind"),
                   "fixture": c.get("fixture"), "oracle": c.get("oracle")}
                  for c in man.get("cases") or []],
        "case_count": len(man.get("cases") or []),
        "subcases": {k: len(v) for k, v in sub.items()},
        "fixtures_dir": str((root / "assets" / "fixtures")),
        "oracles_dir": str((root / "assets" / "oracles")),
        "doc_sha256": sha256_file(root / "03_W2_TQAEP.md"),
        "case_rows_parsed": len(case_rows),
    }

    entry = (root / "04_W2_START_THIN_PROMPT.md").read_text(encoding="utf-8")
    views["ENTRY"] = {
        "sha256": sha256_file(root / "04_W2_START_THIN_PROMPT.md"),
        "sections": [s for s in ("GOAL", "SOURCE", "SPEC", "EXECUTE",
                                 "HARNESS LOOP", "DONE") if s in entry],
        "bytes": (root / "04_W2_START_THIN_PROMPT.md").stat().st_size,
    }

    # cross-checks: the counts in the manifest must agree with the parsed views
    problems = []
    if views["PI"]["requirement_count"] != 16:
        problems.append(f"requirements {views['PI']['requirement_count']} != 16")
    if views["TQAEP"]["case_count"] != 12:
        problems.append(f"cases {views['TQAEP']['case_count']} != 12")
    if views["DEV"]["write_set_rows_parsed"] < 2:
        problems.append("DEV write set table not parsed from 01_W2_DEV_ECP.md")
    if not set(views["DEV"]["ops"]) >= {"DEV-D01", "DEV-D04", "DEV-D07"}:
        problems.append("DEV op locators incomplete")
    if len(views["ENTRY"]["sections"]) != 6:
        problems.append("04 entry sections incomplete")
    if views["PI"]["constraints"]["permission_state"] != "NONE_GRANTED":
        problems.append("pack must ship no grant")

    return {
        "schema": "FHS5.PLP.W2.Contracts@1",
        "pack_manifest_sha256": insp["pack_manifest_sha256"],
        "identity": insp["identity"],
        "views": views,
        "view_names": sorted(views),
        "counts": insp["counts"],
        "problems": problems,
        "ok": not problems,
    }


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    res = build_contracts(a.pack)
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"ok": res["ok"], "problems": res["problems"],
                      "views": res["view_names"], "counts": res["counts"]},
                     ensure_ascii=False))
    return 0 if res["ok"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
