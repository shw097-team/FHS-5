#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S1 SourceManifest@1 reader (formal entry, generation 2).

Fixes over the first wiring:
  * external_seal is a string in the adopted manifests; resolve it without
    assuming a dict, and fall back to the sibling SEALS/ directory.
  * W0 has its own denominator contract (nf/sample/historical_receipts/wp).
  * returns the fields build_contracts needs: manifest, source_set_sha256,
    source_refs and requirements (identifiers only, with an explicit flag).
  * honours expected_identity like the NF@1 path.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import body_resolver as br

SCHEMA_RE = r"^FHS5\.PLP\.(W[0-9])\.SourceManifest\.S1@1$"
REQUIRED = (
    "schema", "candidate", "pack_version", "artifact_id", "project_id",
    "subject_id", "scope", "wave_id", "sources", "pack_files", "assets",
    "cases", "case_count", "denominators", "holds", "digest_contract",
    "manifest_self_hash", "external_seal", "adoption",
)
DIGEST_KEYS = ("file_sha256", "pack_manifest_sha256", "pack_tree_sha256",
               "source_set_algorithm", "manifest_self_hash")
NEED_DEN = {
    "W0": ("nf", "sample", "historical_receipts", "wp"),
    "W1": ("dev", "ops", "wp", "acc", "fuo"),
    "W2": ("wp", "fuo", "acc", "requirements", "n_cases"),
}
REQ_ID = re.compile(r"\bU-\d{3}[a-z]?\b")


class S1Error(Exception):
    def __init__(self, token, detail=""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def is_s1(schema) -> bool:
    return bool(re.match(SCHEMA_RE, str(schema or "")))


def _tree_sha(rows) -> str:
    text = "\n".join(sorted(f"{r['path']}|{r['bytes']}|{r['sha256']}" for r in rows))
    return sha_bytes(text.encode("utf-8"))


def _source_set_sha(sources) -> str:
    text = "\n".join(sorted(f"{s['id']}|{s['sha256']}|{s['bytes']}" for s in sources))
    return sha_bytes(text.encode("utf-8"))


def _seal_candidates(root: Path, wave: str, seal_ref):
    out = []
    if isinstance(seal_ref, dict) and seal_ref.get("path"):
        out.append(seal_ref["path"])
    elif isinstance(seal_ref, str) and seal_ref:
        out.append(seal_ref)
    out.append(str(root.parent / "SEALS" / f"{wave}_PACK_SEAL.json"))
    cands = []
    for raw in out:
        p = Path(raw)
        if p.is_file():
            cands.append(p)
            continue
        if not p.is_absolute():
            for base in (root.parent, root.parent.parent, root.parent.parent.parent):
                q = base / raw
                if q.is_file():
                    cands.append(q)
                    break
    return cands


def inspect_s1(root, seal_path=None, expected_wave=None, expected_identity=None) -> dict:
    root = br.canonical_root(root)
    man_path = root / "05_W1_SOURCE_MANIFEST.json"
    if not man_path.is_file():
        cands = sorted(root.glob("05_*_SOURCE_MANIFEST.json"))
        if len(cands) != 1:
            raise S1Error("ENTRY_MISSING", "05 manifest")
        man_path = cands[0]
    raw = man_path.read_bytes()
    man = json.loads(raw.decode("utf-8"))
    schema = man.get("schema")
    if not is_s1(schema):
        raise S1Error("SCHEMA_UNSUPPORTED", str(schema))
    wave = schema.split(".")[2]
    if expected_wave and wave != expected_wave:
        raise S1Error("IDENTITY_MISMATCH", f"wave {wave} != {expected_wave}")
    missing = [k for k in REQUIRED if k not in man]
    if missing:
        raise S1Error("SCHEMA_INCOMPLETE", missing)
    if man.get("manifest_self_hash") != "EXTERNAL_RECORD_ONLY":
        raise S1Error("MANIFEST_SELF_HASH", man.get("manifest_self_hash"))
    if "pack_manifest_sha256" in man or "pack_tree_sha256" in man:
        raise S1Error("MANIFEST_SELF_EMBED", "pin inside 05")
    dc = man.get("digest_contract") or {}
    miss_dc = [k for k in DIGEST_KEYS if k not in dc]
    if miss_dc:
        raise S1Error("DIGEST_DOMAIN_MISSING", miss_dc)

    if expected_identity is not None:
        for k, v in expected_identity.items():
            if man.get(k) != v:
                raise S1Error("IDENTITY_MISMATCH", f"{k}={man.get(k)!r}")

    man_sha = sha_bytes(raw)
    pfs = man["pack_files"]
    if len(pfs) != 5:
        raise S1Error("PACK_INCOMPLETE_LOCAL", len(pfs))
    texts, rows = {}, []
    for p in pfs:
        rel = p["path"]
        data = br.read_bounded(br.resolve_inside(root, rel), rel)
        if (len(data), sha_bytes(data)) != (p.get("bytes"), p.get("sha256")):
            raise S1Error("DIGEST_MISMATCH", rel)
        if b"\r\n" in data:
            raise S1Error("EOL_NON_CANONICAL", rel)
        text = br.decode_utf8(data, rel)
        if man_sha in text:
            raise S1Error("MANIFEST_SELF_EMBED", rel)
        if p.get("lines") is not None and p["lines"] != len(text.splitlines()):
            raise S1Error("DIGEST_MISMATCH", f"{rel} lines")
        texts[rel] = text
        rows.append({"path": rel, "bytes": len(data), "sha256": sha_bytes(data)})
    tree = _tree_sha(rows)

    for a in man["assets"]:
        data = br.read_bounded(br.resolve_inside(root, a["path"]), a["path"])
        if (len(data), sha_bytes(data)) != (a.get("bytes"), a.get("sha256")):
            raise S1Error("DIGEST_MISMATCH", a["path"])

    cases = man["cases"]
    if man.get("case_count") != len(cases):
        raise S1Error("CASE_SET_INCOMPLETE", "case_count")
    t3 = next((t for k, t in texts.items() if "TQAEP" in k), "")
    missing_cases = [c["case_id"] for c in cases if c["case_id"] not in t3]
    if missing_cases:
        raise S1Error("CASE_SET_INCOMPLETE", missing_cases)

    den = man["denominators"]
    for key in NEED_DEN.get(wave, ()):
        if not isinstance(den.get(key), int) or den[key] < 0:
            raise S1Error("DENOMINATOR_MISSING", key)

    body = "\n".join(texts.values())
    req_ids = sorted(set(REQ_ID.findall(body)))
    declared = den.get("requirements")
    req_state = ("MATCH" if declared is not None and declared == len(req_ids)
                 else ("IDENTIFIER_ONLY" if req_ids else "ABSENT_IN_PACK"))

    seal = None
    cands = [Path(seal_path)] if seal_path else _seal_candidates(
        root, wave, man.get("external_seal"))
    if not cands:
        raise S1Error("SEAL_MISSING", str(man.get("external_seal")))
    sp = next((c for c in cands if Path(c).is_file()), None)
    if sp is None:
        raise S1Error("SEAL_MISSING", str(cands[0]))
    seal = json.loads(Path(sp).read_text(encoding="utf-8"))
    if seal.get("schema") != "FHS5.PLP.S1.PackSeal@1":
        raise S1Error("SEAL_SCHEMA", seal.get("schema"))
    if seal["manifest"]["sha256"] != man_sha:
        raise S1Error("SEAL_BINDING", "manifest sha")
    if seal.get("pack_tree_sha256") != tree:
        raise S1Error("PACK_TREE_MISMATCH",
                      {"seal": seal.get("pack_tree_sha256"), "computed": tree})
    want = (man.get("adoption") or {}).get("decision_id")
    got = (seal.get("adoption") or {}).get("decision_id")
    if want and got and want != got:
        raise S1Error("ADOPTION_MISMATCH", got)

    man_out = dict(man)
    man_out["requirements"] = [{"id": i} for i in req_ids]
    man_out["requirements_declared"] = declared
    man_out["requirement_material"] = req_state
    identity = {k: man.get(k) for k in
                ("project_id", "subject_id", "scope", "wave_id",
                 "artifact_id", "candidate")}
    return {
        "schema": "FHS5.PLP.W1.S1Inspect@2",
        "abi": "SourceManifest.S1@1",
        "wave": wave,
        "identity": identity,
        "manifest": man_out,
        "manifest_sha256": man_sha,
        "pack_manifest_sha256": man_sha,
        "pack_tree_sha256": tree,
        "source_set_sha256": _source_set_sha(man["sources"]),
        "source_refs": [{"id": s["id"], "path": s.get("path"),
                         "bytes": s.get("bytes"), "sha256": s.get("sha256")}
                        for s in man["sources"]],
        "requirements": req_ids,
        "requirements_declared": declared,
        "requirement_material": req_state,
        "seal_verified": seal is not None,
        "seal_path": str(sp),
        "counts": {
            "pack_files": len(pfs),
            "dev": den.get("dev"), "ops": den.get("ops"),
            "cases": len(cases),
            "assets": len(man["assets"]),
            "sources": len(man["sources"]),
            "holds": len(man["holds"]),
        },
        "denominators": den,
        "case_ids": [c["case_id"] for c in cases],
        "readiness": man.get("readiness"),
        "file_refs": rows,
    }
