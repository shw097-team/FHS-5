#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 NF-r2 production reader (D2/D3, execution-scope revision r3).

Superset of w1_nf_reader (kept unchanged as the historical entry).

Revision r3 amendments (explicit, recorded in W1_UPSTREAM_CHANGESET.md):
  A1  A source recorded LOCAL_VERIFIED but absent at probe time is recorded as
      LOCAL_MISSING_RECORDED with its recorded sha preserved; it is NOT a hard
      gate and its digest is never fabricated.  A present file whose bytes
      differ from the recorded sha remains a hard SOURCE_DIGEST_MISMATCH.
  A2  Adds a field-level legacy-15 to NF ABI crosswalk plus LossLedger.
  A3  Adds explicit digest domains (file / pack_manifest / source_set /
      context / package_tree / legacy).
  A4  Adds a clause index with Parent/Child/NEG/Exception.
  A5  Routes every body read through body_resolver (TOCTOU, size, link).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import body_resolver as br
import w1_nf_reader as base

NFError = base.NFError
PathDenied = base.PathDenied

LEGACY_CROSSWALK = [
    ("00_WAVE_RUN_MANIFEST.md", "00_W1_PI_PD.md + 05", "identity, goal, done, effect, claim, holds, host ledger"),
    ("00_WAVE_RUN_MANIFEST.json", "05_W1_SOURCE_MANIFEST.json", "identity, dag, assets, holds, checks"),
    ("01_SOURCE_SCOPE_AND_CONSTRUCTION.md", "00 + 01 + 02", "source, scope, P01-P06, four APIs, seven seams"),
    ("02_ORIGINAL_CONTRACT_REFS.json", "05 + 00", "original PI/PD/ECP/TQAEP refs"),
    ("03_DEV_ECP.md", "01_W1_DEV_ECP.md", "38 DEV ids, pre/post, writeset, readback, restore"),
    ("04_OPS_ECP.md", "02_W1_OPS_ECP.md", "29 OPS ids, host, acl, receiver, activation, recovery"),
    ("05_PLANNED_TQAEP.md", "03_W1_TQAEP.md", "13 case ids, denominators, fixtures, oracles, expected raw"),
    ("05_PLANNED_TQAEP.json", "03 + assets", "case ids, fixture/oracle sha, observation schema"),
    ("06_PERMISSION_STOP_RESUME.md", "00 + 01 + 02 + 04", "issuer, scoped grant, stop/resume, unknown reconcile"),
    ("07_EVIDENCE_AND_CHECKER.md", "03 + evidence appendix", "five pins, not-covered, checker/consumer split"),
    ("08_AS_BUILT_AND_HANDOFF.md", "00 as-built + closeout/handoff", "lastgood, changecone, receive fields"),
    ("09_README_RUN_ORDER.md", "00 DAG + 04", "next legal operation, dependency direction"),
    ("W1_START_THIN_PROMPT.md", "04_W1_START_THIN_PROMPT.md", "goal/source/spec/execute/loop/done"),
    ("SOURCE_MANIFEST.json", "05_W1_SOURCE_MANIFEST.json", "source bytes/sha/span/rights/selection"),
    ("PACKAGE_FILE_MANIFEST.json", "05 + external seal", "sha, bytes, path, duplicate rules"),
]

ENTITY_PROBES = {
    "PI": {
        "subject_id": ("00_W1_PI_PD.md", "**subject_id**"),
        "scope": ("00_W1_PI_PD.md", "**scope**"),
        "claim_ceiling": ("00_W1_PI_PD.md", "Claim ceiling"),
        "job_to_be_done_or_goal": ("00_W1_PI_PD.md", "Job to be done"),
    },
    "PD": {
        "scope": ("00_W1_PI_PD.md", "**scope**"),
        "repo_context": ("01_W1_DEV_ECP.md", "RepoContext"),
        "effect_class": ("00_W1_PI_PD.md", "Effect"),
        "typed_dag": ("00_W1_PI_PD.md", "typed DAG"),
    },
    "DEV_ECP": {k: ("01_W1_DEV_ECP.md", v) for k, v in {
        "id": "DEV-", "operation": "Native 承接", "precondition": "Pre（真前件）",
        "postcondition": "Post／Readback", "writeset": "WriteSet",
        "recovery": "Recovery"}.items()},
    "OPS_ECP": {k: ("02_W1_OPS_ECP.md", v) for k, v in {
        "id": "OPS-", "host": "Host", "effect": "effect", "receiver": "Receiver",
        "post_readback": "Post／Readback", "recovery": "Recovery"}.items()},
    "TQAEP": {k: ("03_W1_TQAEP.md", v) for k, v in {
        "case_id": "W1-HOST-01", "kind": "Kind", "requirement_ref": "Requirement",
        "fixture_sha256": "Fixture SHA", "oracle_sha256": "Oracle SHA",
        "runner": "Runner"}.items()},
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _verify_sources(man: dict) -> list:
    """Lenient-but-honest source verification (amendment A1)."""
    out = []
    for s in man.get("sources") or []:
        sid = s.get("id")
        av = s.get("availability")
        if av == "LOCAL_VERIFIED":
            sr = Path(s["source_root"])
            rel = str(s["path"]).replace("\\", "/")
            try:
                p = Path(sr).joinpath(*br._split_rel(rel))
            except PathDenied as exc:
                raise NFError("SOURCE_PATH_DENIED", f"{sid}:{exc.detail}") from exc
            if not p.is_file():
                out.append({"id": sid, "role": s.get("role"), "path": str(p),
                            "availability": "LOCAL_MISSING_RECORDED",
                            "recorded_sha256": s.get("sha256"),
                            "recorded_bytes": s.get("bytes"),
                            "recorded_lines": s.get("lines"),
                            "local_missing": True,
                            "reason": "recorded LOCAL_VERIFIED but absent at probe time",
                            "read_level": s.get("read_level")})
                continue
            info = base.file_info(p)
            if (info["bytes"], info["sha256"], info["lines"]) != (
                    s.get("bytes"), s.get("sha256"), s.get("lines")):
                raise NFError("SOURCE_DIGEST_MISMATCH", sid)
            out.append({"id": sid, "role": s.get("role"), "path": str(p),
                        "bytes": info["bytes"], "sha256": info["sha256"],
                        "lines": info["lines"], "availability": av,
                        "local_missing": False, "read_level": s.get("read_level")})
        elif av == "REMOTE_ONLY_UNBOUND":
            if s.get("sha256") is not None or s.get("bytes") is not None:
                raise NFError("SOURCE_FAKE_DIGEST", sid)
            if not s.get("reason") or not base._hex(s.get("git_blob_sha1"), 40):
                raise NFError("SOURCE_REASON_MISSING", sid)
            out.append({"id": sid, "role": s.get("role"),
                        "git_blob_sha1": s.get("git_blob_sha1"),
                        "availability": av, "reason": s.get("reason"),
                        "local_missing": True})
        else:
            raise NFError("SOURCE_AVAILABILITY_UNKNOWN", f"{sid}={av}")
    return out


def _crosswalk(root: Path, texts: dict) -> dict:
    rows, ledger = [], []
    legacy_dir = root.parent / "primary"
    for legacy, target, fields in LEGACY_CROSSWALK:
        present = (legacy_dir / legacy).is_file()
        rows.append({"legacy_path": legacy, "target": target, "preserved": fields,
                     "classification": "PROJECTION", "legacy_present_local": present,
                     "loss": "NONE" if present else "PROJECTION_ONLY_NO_LOCAL_LEGACY"})
        for f in [x.strip() for x in fields.split(",")]:
            ledger.append({"entity": "LEGACY_15", "field": f, "source": legacy,
                           "target": target, "type": "text", "required": True,
                           "transform": "explicit_projection", "loss": "NONE",
                           "readback": "target_section_present"})
    fields_out = []
    for entity, fields in ENTITY_PROBES.items():
        for name, (path, needle) in fields.items():
            ok = needle in texts.get(path, "")
            fields_out.append({"entity": entity, "field": name, "source_path": path,
                               "target": "NF@1 canonical", "type": "text",
                               "required": True, "transform": "direct",
                               "loss": "NONE" if ok else "EXPLICIT_REVIEW",
                               "readback": "PRESENT" if ok else "ABSENT",
                               "unknown_preserved": True})
    missing = [f for f in fields_out if f["loss"] != "NONE"]
    return {"schema": "FHS5.PLP.W1.ABICrosswalk@1", "legacy_rows": rows,
            "legacy_row_count": len(rows), "entity_fields": fields_out,
            "loss_ledger": ledger + fields_out, "missing_fields": missing,
            "unknown_drop": 0,
            "state": "COMPLETE" if not missing else "EXPLICIT_REVIEW"}


def _digest_domains(insp: dict) -> dict:
    lines = [f"{f['path']}|{f['bytes']}|{f['sha256']}\n" for f in insp["file_refs"]]
    lines += [f"{a['path']}|{a['bytes']}|{a['sha256']}\n" for a in insp["asset_refs"]]
    return {"file_sha256": {f["path"]: f["sha256"] for f in insp["file_refs"]},
            "pack_manifest_sha256": insp["pack_manifest_sha256"],
            "source_set_sha256": insp["source_set_sha256"],
            "context_sha256": None,
            "package_tree_sha256": sha256_bytes("".join(sorted(lines)).encode("utf-8")),
            "legacy_package_sha256": "EXPLICIT_REVIEW_NOT_MAPPED",
            "note": "context_sha256 is produced by bridge render, never by the manifest"}


def _clauses(root: Path) -> dict:
    out, total, neg = {}, 0, 0
    for name in base.PACK_FILES:
        p = br.resolve_inside(root, name)
        data = br.read_bounded(p, name)
        cs = br.parse_clauses(br.decode_utf8(data, name), name, sha256_bytes(data))
        out[name] = cs
        total += len(cs)
        neg += sum(len(c["negatives"]) for c in cs)
    return {"files": out, "clause_count": total, "negative_markers": neg}


def inspect_package(pack_root, manifest_path=None, seal_path=None,
                    expected_identity=None) -> dict:
    root = br.canonical_root(pack_root)
    man, mraw = br.load_json_strict(br.resolve_inside(root, base.MANIFEST), base.MANIFEST)
    if man.get("schema") != base.SCHEMA:
        raise NFError("SCHEMA_UNSUPPORTED", str(man.get("schema")))
    if man.get("pack_version") != base.PACK_VERSION:
        raise NFError("VERSION_MISMATCH", str(man.get("pack_version")))
    for k, v in base.IDENT.items():
        if man.get(k) != v:
            raise NFError("IDENTITY_MISMATCH", f"{k}={man.get(k)!r}")
    ident = {k: man[k] for k in base.IDENT}
    ident["source_manifest_sha256"] = sha256_bytes(mraw)
    if expected_identity is not None and {k: expected_identity.get(k) for k in base.IDENT} != base.IDENT:
        raise NFError("IDENTITY_MISMATCH", "expected identity")

    texts, file_refs = {}, []
    pfs = man.get("pack_files") or []
    if [p.get("path") for p in pfs] != base.PACK_FILES:
        raise NFError("PACK_INCOMPLETE_LOCAL", "pack_files")
    for p in pfs:
        rel = p["path"]
        data = br.read_bounded(br.resolve_inside(root, rel), rel)
        info = {"bytes": len(data), "sha256": sha256_bytes(data),
                "lines": len(br.decode_utf8(data, rel).splitlines())}
        if (p.get("bytes"), p.get("sha256"), p.get("lines")) != (
                info["bytes"], info["sha256"], info["lines"]):
            raise NFError("DIGEST_MISMATCH", rel)
        if b"\r\n" in data:
            raise NFError("EOL_NON_CANONICAL", rel)
        text = br.decode_utf8(data, rel)
        if ident["source_manifest_sha256"] in text:
            raise NFError("MANIFEST_SELF_EMBED", rel)
        for k, token in base.EXACT_HEADERS.items():
            if token not in text:
                raise NFError("IDENTITY_MISMATCH", f"{rel} {k}")
        if base.PACK_VERSION not in text or "source_manifest_ref" not in text:
            raise NFError("VERSION_MISMATCH", rel)
        texts[rel] = text
        file_refs.append({"path": rel, **info, "role": p.get("role")})

    if man.get("manifest_self_hash") != "EXTERNAL_RECORD_ONLY":
        raise NFError("MANIFEST_SELF_HASH", str(man.get("manifest_self_hash")))
    if "pack_manifest_sha256" in man:
        raise NFError("MANIFEST_SELF_EMBED", "pack_manifest_sha256")
    dc = man.get("digest_contract") or {}
    for k in ("file_sha256", "pack_manifest_sha256", "source_set_sha256",
              "context_sha256", "package_tree_sha256", "legacy_package_sha256"):
        if k not in dc:
            raise NFError("DIGEST_DOMAIN_MISSING", k)

    dev = base._ids(texts["01_W1_DEV_ECP.md"], "DEV")
    ops = base._ids(texts["02_W1_OPS_ECP.md"], "OPS")
    if len(dev) != 38 or len(ops) != 29:
        raise NFError("ID_SET_INCOMPLETE", f"DEV={len(dev)} OPS={len(ops)}")
    t3, t0 = texts["03_W1_TQAEP.md"], texts["00_W1_PI_PD.md"]
    miss = [c for c in base.CASES if c not in t3]
    if miss:
        raise NFError("CASE_SET_INCOMPLETE", str(miss))
    for sub in ("N01", "N02", "N03", "N04", "N10", "N11"):
        if sub not in t3:
            raise NFError("SUBCASE_MISSING", sub)
    for i in range(1, 7):
        if f"P0{i}" not in t0:
            raise NFError("WP_MISSING", f"P0{i}")
    for i in range(1, 10):
        if f"D0{i}" not in t0:
            raise NFError("DELTA_MISSING", f"D0{i}")
    for i in range(1, 11):
        if f"NF{i:02d}" not in t0:
            raise NFError("NF_MISSING", f"NF{i:02d}")
    for i in range(1, 8):
        if f"SM{i:02d}" not in t0:
            raise NFError("SEAM_MISSING", f"SM{i:02d}")
    for i in range(1, 7):
        if f"W1-CODEX-0{i}" not in t0 or f"W1-A0{i}" not in t0:
            raise NFError("ACC_MISSING", str(i))
    for h in base.HOLDS:
        if h not in t0:
            raise NFError("HOLD_MISSING", h)
    if not all(sec in texts["04_W1_START_THIN_PROMPT.md"] for sec in
               ("GOAL", "SOURCE", "SPEC", "EXECUTE", "HARNESS LOOP", "DONE", "STOP", "RESUME")):
        raise NFError("THIN_PROMPT_INCOMPLETE")

    dag = man.get("dag") or {}
    order = base._topo(dag.get("nodes") or [], dag.get("edges") or [])

    assets = man.get("assets") or []
    if len(assets) != 26:
        raise NFError("ASSET_SET_INCOMPLETE", str(len(assets)))
    asset_refs, seen = [], set()
    for a in assets:
        key = (a.get("case_id"), a.get("kind"))
        if key in seen:
            raise NFError("ASSET_DUPLICATE", str(key))
        seen.add(key)
        rel = a.get("path")
        data = br.read_bounded(br.resolve_inside(root, rel), rel)
        if (len(data), sha256_bytes(data)) != (a.get("bytes"), a.get("sha256")):
            raise NFError("ASSET_DIGEST_MISMATCH", rel)
        asset_refs.append({"case_id": a["case_id"], "kind": a["kind"], "path": rel,
                           "bytes": len(data), "sha256": a["sha256"]})
    for c in base.CASES:
        for kind in ("fixture", "oracle"):
            if (c, kind) not in seen:
                raise NFError("ASSET_SET_INCOMPLETE", f"{c}/{kind}")

    sources = man.get("sources") or []
    source_refs = _verify_sources(man)
    sset = sha256_bytes("".join(
        f"{s['id']}|{s['sha256']}|{s['bytes']}\n"
        for s in sorted([x for x in sources if x.get("sha256")], key=lambda x: x["id"])
    ).encode("utf-8"))
    if dc.get("source_set_sha256_value") != sset:
        raise NFError("SOURCE_SET_DIGEST_MISMATCH", sset)

    uh = man.get("upstream_handoff") or {}
    for k in ("w0_handoff_id", "pack_sha256", "w0m_sha256", "candidate_commit",
              "oracle_sha256", "evidence_manifest_sha256", "consumer_manifest_sha256"):
        if not uh.get(k):
            raise NFError("UPSTREAM_PIN_MISSING", k)
    smap = {s["id"]: s for s in sources if s.get("sha256")}
    for pin, sid in {"pack_sha256": "W0-05", "w0m_sha256": "W0M", "handoff_sha256": "H0",
                     "closeout_sha256": "C0", "w1m_sha256": "W1M", "plan_sha256": "PLAN",
                     "workctrl_sha256": "WORKCTRL", "codexctrl_sha256": "CODEXCTRL"}.items():
        if sid not in smap or uh.get(pin) != smap[sid]["sha256"]:
            raise NFError("UPSTREAM_PIN_MISMATCH", f"{pin}!={sid}")

    sp = Path(seal_path) if seal_path else root.parent / "evidence" / "SEAL.json"
    seal, _ = br.load_json_strict(sp) if sp.is_file() else (None, b"")
    if seal is None:
        raise NFError("SEAL_MISSING", str(sp))
    if seal.get("pack_manifest_sha256") != ident["source_manifest_sha256"]:
        raise NFError("SEAL_MISMATCH", "pack_manifest_sha256")
    sfiles = {x.get("path"): (x.get("sha256"), x.get("bytes"), x.get("lines"))
              for x in seal.get("pack_files") or []}
    for f in file_refs:
        if sfiles.get(f["path"]) != (f["sha256"], f["bytes"], f["lines"]):
            raise NFError("SEAL_MISMATCH", f["path"])
    asset_tree = sha256_bytes("".join(
        sorted(f"{a['path']}|{a['sha256']}|{a['bytes']}\n" for a in asset_refs)).encode("utf-8"))
    if seal.get("assets_tree_sha256") != asset_tree or seal.get("asset_count") != 26:
        raise NFError("SEAL_MISMATCH", "assets")

    scan = br.scan_pack(root)
    insp = {
        "schema": "FHS5.PLP.W1.NFInspect@3",
        "claim_ceiling": man.get("claim_ceiling"),
        "root": str(root),
        "manifest_path": base.MANIFEST,
        "pack_manifest_sha256": ident["source_manifest_sha256"],
        "pack_manifest_bytes": len(mraw),
        "identity": ident,
        "pack_version": man.get("pack_version"),
        "counts": {"pack_files": len(file_refs), "dev": len(dev), "ops": len(ops),
                   "cases": len(base.CASES), "assets": len(asset_refs),
                   "sources": len(source_refs), "holds": len(base.HOLDS)},
        "file_refs": file_refs,
        "asset_refs": asset_refs,
        "source_refs": source_refs,
        "source_local_missing": [s["id"] for s in source_refs if s.get("local_missing")],
        "dag": {"nodes": dag.get("nodes"), "edges": dag.get("edges"),
                "topological_order": order},
        "ids": {"dev": dev, "ops": ops, "cases": base.CASES, "holds": base.HOLDS},
        "source_set_sha256": sset,
        "assets_tree_sha256": asset_tree,
        "readiness": man.get("readiness"),
        "permission_state": "NONE_GRANTED",
        "host_effect": "NOT_ADMITTED",
        "original_reader_state": "UNBOUND",
        "claims": {"pack_primary": True,
                   "w1_execution_ready": (man.get("readiness") or {}).get("w1_execution_ready"),
                   "w1_nf_validated": (man.get("readiness") or {}).get("w1_nf_validated"),
                   "independent": (man.get("readiness") or {}).get("independent"),
                   "release": (man.get("readiness") or {}).get("release")},
        "unresolved_refs": man.get("unresolved_refs") or [],
        "semantic_state": "NF_PACK_READ_ACTUAL",
        "product_actual": "NOT_RUN",
        "scan": scan,
    }
    idx = _clauses(root)
    insp["abi_crosswalk"] = _crosswalk(root, texts)
    insp["digest_domains"] = _digest_domains(insp)
    insp["clause_index"] = {"clause_count": idx["clause_count"],
                            "negative_markers": idx["negative_markers"],
                            "files": {k: len(v) for k, v in idx["files"].items()}}
    return insp


W0_SCHEMA = "FHS5.PLP.W0.SourceManifest.NF@1"


def _verify_sources_w0(man: dict) -> list:
    """W0 profile sources are absolute paths without an availability field."""
    out = []
    for s in man.get("sources") or []:
        sid = s.get("id")
        p = Path(str(s.get("path")))
        if not p.is_file():
            out.append({"id": sid, "role": s.get("role"), "path": str(p),
                        "availability": "LOCAL_MISSING_RECORDED",
                        "recorded_sha256": s.get("sha256"), "local_missing": True,
                        "reason": "recorded absolute path absent at probe time"})
            continue
        info = base.file_info(p)
        want = (s.get("bytes"), s.get("sha256"))
        got = (info["bytes"], info["sha256"])
        if "lines" in s and s.get("lines") is not None:
            want = want + (s.get("lines"),)
            got = got + (info["lines"],)
        if want != got:
            raise NFError("SOURCE_DIGEST_MISMATCH", sid)
        out.append({"id": sid, "role": s.get("role"), "path": str(p),
                    "bytes": info["bytes"], "sha256": info["sha256"],
                    "lines": info["lines"], "availability": "LOCAL_VERIFIED",
                    "local_missing": False})
    return out


def inspect_generic(pack_root, expected_identity=None) -> dict:
    """Second-package dispatch: same reader ABI, explicit profile capabilities.

    The W1 profile keeps every semantic check.  The W0 profile is a real,
    different package (different subject/scope/schema, no assets/dag) and is
    read for identity, file digests, sources and seal only; capabilities that
    do not exist for that profile are reported as False rather than faked.
    """
    root = br.canonical_root(pack_root)
    cands = sorted(p.name for p in root.glob("*SOURCE_MANIFEST*.json"))
    if not cands:
        raise NFError("PACK_INCOMPLETE_LOCAL", "no source manifest")
    man_name = cands[0]
    man, mraw = br.load_json_strict(br.resolve_inside(root, man_name), man_name)
    schema = man.get("schema")
    if schema == base.SCHEMA:
        insp = inspect_package(root)
        insp["profile"] = "W1"
        insp["profile_capabilities"] = {"explain": True, "assets": True,
                                        "dag": True, "cases": True}
        return insp
    m_prof = re.match(r"^FHS5\.PLP\.([A-Z0-9]+)\.SourceManifest\.NF@1$", str(schema))
    if schema != W0_SCHEMA and not m_prof:
        raise NFError("SCHEMA_UNSUPPORTED", str(schema))
    if expected_identity:
        for k, v in expected_identity.items():
            if man.get(k) != v:
                raise NFError("IDENTITY_MISMATCH", k)
    sha = sha256_bytes(mraw)
    refs = []
    for f in man.get("pack_files") or []:
        rel = f.get("path")
        data = br.read_bounded(br.resolve_inside(root, rel), rel)
        refs.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data),
                     "matches_manifest": (len(data), sha256_bytes(data)) ==
                                         (f.get("bytes"), f.get("sha256"))})
    if [r for r in refs if not r["matches_manifest"]]:
        raise NFError("DIGEST_MISMATCH", "w0 pack_files")
    sources = _verify_sources_w0(man)
    seal_path = root.parent / "evidence" / "SEAL.json"
    seal_state = "ABSENT"
    if seal_path.is_file():
        seal, _ = br.load_json_strict(seal_path)
        seal_state = "MATCH" if seal.get("pack_manifest_sha256") == sha else "MISMATCH"
        if seal_state == "MISMATCH":
            raise NFError("SEAL_MISMATCH", "w0")
    return {
        "schema": "FHS5.PLP.W1.NFInspectGeneric@1",
        "profile": (m_prof.group(1) if m_prof else "W0"),
        "manifest_path": man_name,
        "profile_capabilities": {"explain": False, "assets": False,
                                 "dag": False, "cases": False},
        "root": str(root),
        "pack_manifest_sha256": sha,
        "pack_manifest_bytes": len(mraw),
        "identity": {k: man.get(k) for k in
                     ("project_id", "subject_id", "scope", "wave_id", "batch_id")},
        "pack_version": man.get("pack_version"),
        "claim_ceiling": man.get("claim_ceiling"),
        "counts": {"pack_files": len(refs), "sources": len(sources),
                   "dev": 0, "ops": 0, "cases": 0, "assets": 0, "holds": 0},
        "file_refs": refs,
        "source_refs": sources,
        "source_local_missing": [s["id"] for s in sources if s.get("local_missing")],
        "asset_refs": [],
        "dag": {"nodes": [], "edges": [], "topological_order": []},
        "ids": {"dev": [], "ops": [], "cases": [], "holds": []},
        "seal_state": seal_state,
        "permission_state": "NONE_GRANTED",
        "semantic_state": "GENERIC_PROFILE_READ",
    }


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    ins = sub.add_parser("inspect")
    ins.add_argument("--pack", required=True)
    ins.add_argument("--seal")
    ins.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        out = inspect_package(args.pack, seal_path=args.seal)
    except NFError as exc:
        sys.stdout.write(json.dumps({"result": "REJECT", "token": exc.token,
                                     "detail": exc.detail}, ensure_ascii=False, indent=2) + "\n")
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
