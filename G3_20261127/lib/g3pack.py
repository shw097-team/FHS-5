#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Strict reader for the adopted G3 (PCNF-r2) W0/W1/W2 control packs.

The reader is deliberately narrow: it verifies identity, the five markdown
files, the assets, the case set and the seven-key work orders against the
manifest that ships with the pack.  It never writes to the pack and never
issues a grant.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PACK_RE = re.compile(r"^FHS-5_PLP_(W[012])_NATIVE_FIRST$")
MD = ["00_{w}_PI_PD.md", "01_{w}_DEV_ECP.md", "02_{w}_OPS_ECP.md",
      "03_{w}_TQAEP.md", "04_{w}_START_THIN_PROMPT.md"]
KEYS = ("project_id", "subject_id", "scope", "profile", "wave", "operation_id", "case_id")
ADOPT = ("PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION", "CONSTRUCTION_READY")


class PackError(Exception):
    def __init__(self, token, detail=""):
        self.token = token
        self.detail = detail
        super().__init__(f"{token}: {detail}")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _pairs(ps):
    out = {}
    for k, v in ps:
        if k in out:
            raise PackError("DUPLICATE_KEY", k)
        out[k] = v
    return out


def strict_json(raw: bytes, label="<json>") -> dict:
    def bad(x):
        raise PackError("NONFINITE", f"{label}:{x}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PackError("INVALID_UTF8", label) from exc
    try:
        obj = json.loads(text, object_pairs_hook=_pairs, parse_constant=bad)
    except json.JSONDecodeError as exc:
        raise PackError("INVALID_JSON", f"{label}:{exc}") from exc
    if not isinstance(obj, dict):
        raise PackError("NOT_OBJECT", label)
    return obj


class Pack:
    def __init__(self, root: Path, man: dict, raw: bytes):
        self.root = root
        self.man = man
        self.raw = raw
        self.sha256 = sha256_bytes(raw)
        self.wave = man.get("wave_id")
        self.texts = {}
        self.files = []
        self.assets = []
        self.cases = list(man.get("cases") or [])

    # -- identity -------------------------------------------------------
    @property
    def candidate(self):
        return self.man.get("candidate")

    @property
    def identity(self):
        return {k: self.man.get(k) for k in
                ("project_id", "subject_id", "scope", "wave_id", "batch_id", "profile")}

    def text(self, name: str) -> str:
        return self.texts[name]

    def file_sha(self, name: str) -> str:
        return next(f["sha256"] for f in self.files if f["path"] == name)

    def asset(self, rel: str) -> dict:
        return next((a for a in self.assets if a["path"] == rel), None)

    def case(self, cid: str) -> dict:
        for c in self.cases:
            if c.get("case_id") == cid:
                return c
        raise PackError("CASE_UNKNOWN", cid)

    def fixture(self, cid: str) -> dict:
        c = self.case(cid)
        return strict_json((self.root / c["fixture"]).read_bytes(), c["fixture"])

    def oracle(self, cid: str) -> dict:
        c = self.case(cid)
        return strict_json((self.root / c["oracle"]).read_bytes(), c["oracle"])

    # -- digests --------------------------------------------------------
    def tree_sha256(self) -> str:
        rows = [f"{f['path']}|{f['bytes']}|{f['sha256']}" for f in self.files]
        rows += [f"{a['path']}|{a['bytes']}|{a['sha256']}" for a in self.assets]
        return sha256_bytes("\n".join(sorted(rows)).encode("utf-8"))

    def case_set_sha256(self) -> str:
        rows = sorted(f"{c['case_id']}|{c.get('kind')}|{c.get('fixture')}|{c.get('oracle')}"
                      for c in self.cases)
        return sha256_bytes("\n".join(rows).encode("utf-8"))


def load_pack(pack) -> Pack:
    root = Path(pack).resolve()
    m = PACK_RE.match(root.name)
    if not m:
        raise PackError("DIR_IDENTITY", root.name)
    cands = sorted(root.glob("05_*_SOURCE_MANIFEST.json"))
    if len(cands) != 1:
        raise PackError("MANIFEST_COUNT", str(len(cands)))
    raw = cands[0].read_bytes()
    man = strict_json(raw, cands[0].name)
    p = Pack(root, man, raw)
    if p.wave != m.group(1):
        raise PackError("WAVE_MISMATCH", f"{p.wave}!={m.group(1)}")
    return p


def verify_pack(pack, expect_manifest_sha: str | None = None) -> dict:
    p = load_pack(pack)
    errs = []
    man = p.man

    if not str(man.get("schema", "")).endswith("@2"):
        errs.append(f"SCHEMA:{man.get('schema')}")
    if man.get("pack_version") != man.get("candidate"):
        errs.append("VERSION_MISMATCH")
    if man.get("manifest_self_hash") != "EXTERNAL_RECORD_ONLY":
        errs.append("SELF_HASH")
    for k in ("project_id", "subject_id", "scope", "wave_id", "batch_id", "profile",
              "adoption_state", "claim_ceiling", "authority", "denominators"):
        if not man.get(k):
            errs.append(f"MISSING:{k}")
    if man.get("adoption_state") not in ADOPT:
        errs.append(f"ADOPTION:{man.get('adoption_state')}")
    if (man.get("authority") or {}).get("decision_id") != "PCNF-W0W2-ADOPT-20261127-01":
        errs.append("DECISION_ID")

    names = [n.format(w=p.wave) for n in MD]
    listed = {f.get("path"): f for f in (man.get("pack_files") or [])}
    if [f.get("path") for f in (man.get("pack_files") or [])] != names:
        errs.append("PACK_FILES_ORDER")
    for name in names:
        fp = p.root / name
        if not fp.is_file():
            errs.append(f"MISSING_FILE:{name}")
            continue
        data = fp.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            errs.append(f"UTF8:{name}")
            continue
        info = {"path": name, "bytes": len(data), "sha256": sha256_bytes(data),
                "lines": len(text.splitlines())}
        e = listed.get(name)
        if e is None:
            errs.append(f"UNLISTED:{name}")
        else:
            for k in ("bytes", "sha256", "lines"):
                if e.get(k) != info[k]:
                    errs.append(f"{k.upper()}:{name}")
        if b"\r\n" in data:
            errs.append(f"CRLF:{name}")
        p.texts[name] = text
        p.files.append(info)

    listed_assets = {a.get("path"): a for a in (man.get("assets") or [])}
    actual = set()
    ad = p.root / "assets"
    if ad.exists():
        for fp in ad.rglob("*"):
            if fp.is_file():
                actual.add(fp.relative_to(p.root).as_posix())
    if set(listed_assets) != actual:
        errs.append(f"ASSET_SET:{len(listed_assets)}/{len(actual)}")
    for rel, a in listed_assets.items():
        fp = p.root / rel
        if not fp.is_file():
            errs.append(f"ASSET_MISSING:{rel}")
            continue
        info = {"path": rel, "bytes": fp.stat().st_size, "sha256": sha256_file(fp),
                "role": a.get("role")}
        if info["bytes"] != a.get("bytes") or info["sha256"] != a.get("sha256"):
            errs.append(f"ASSET_DIGEST:{rel}")
        p.assets.append(info)
    p.assets.sort(key=lambda x: x["path"])

    ids = [c.get("case_id") for c in p.cases]
    if len(ids) != len(set(ids)):
        errs.append("CASE_DUP")
    if man.get("case_count") != len(ids):
        errs.append("CASE_COUNT")
    for c in p.cases:
        for key in ("fixture", "oracle"):
            if not c.get(key):
                continue
            rel = c.get(key)
            if not (p.root / rel).is_file():
                errs.append(f"CASE_{key.upper()}_MISSING:{c.get('case_id')}")
            elif rel not in listed_assets:
                errs.append(f"CASE_{key.upper()}_UNLISTED:{c.get('case_id')}")
        fx = p.root / c.get("fixture", "")
        orc = p.root / c.get("oracle", "")
        if fx.suffix == ".json" and orc.suffix == ".json" and fx.is_file() and orc.is_file():
            try:
                f = strict_json(fx.read_bytes(), c["fixture"])
                o = strict_json(orc.read_bytes(), c["oracle"])
            except PackError as exc:
                errs.append(f"CASE_JSON:{c.get('case_id')}:{exc.token}")
                continue
            if f.get("case_id") != c["case_id"] or o.get("case_id") != c["case_id"]:
                errs.append(f"CASE_ID_MISMATCH:{c['case_id']}")

    wos = man.get("work_orders") or []
    seen = set()
    for wo in wos:
        if any(k not in wo for k in KEYS):
            errs.append("WO_KEY_MISSING")
            continue
        key = tuple(str(wo[k]) for k in KEYS)
        if key in seen:
            errs.append("WO_DUP")
        seen.add(key)
        if wo["case_id"] not in ids:
            errs.append(f"WO_CASE:{wo['case_id']}")
    if len(wos) != len(ids):
        errs.append(f"WO_COUNT:{len(wos)}/{len(ids)}")

    seal = p.root.parent.parent / "02_EVIDENCE" / "EXTERNAL_SEAL.json"
    seal_ref = man.get("external_seal")
    if seal_ref:
        cand = (p.root / seal_ref).resolve()
        if not cand.is_file():
            errs.append("SEAL_MISSING")
        else:
            try:
                s = strict_json(cand.read_bytes(), "EXTERNAL_SEAL.json")
                row = (s.get("packs") or {}).get(p.wave) or {}
                if row.get("manifest_sha256") != p.sha256:
                    errs.append("SEAL_MANIFEST_SHA")
                if row.get("candidate") != p.candidate:
                    errs.append("SEAL_CANDIDATE")
            except PackError as exc:
                errs.append(f"SEAL_JSON:{exc.token}")
    if expect_manifest_sha and p.sha256 != expect_manifest_sha:
        errs.append("EXPECTED_MANIFEST_SHA")

    return {"ok": not errs, "errors": errs, "pack": p,
            "manifest_sha256": p.sha256, "tree_sha256": p.tree_sha256(),
            "case_set_sha256": p.case_set_sha256(),
            "counts": {"files": len(p.files), "assets": len(p.assets),
                       "cases": len(p.cases), "work_orders": len(wos)}}


def select_work_order(p: Pack, **q) -> dict:
    hits = [w for w in (p.man.get("work_orders") or [])
            if all(str(w.get(k)) == str(q.get(k)) for k in KEYS)]
    if len(hits) != 1:
        raise PackError("UNBOUND" if not hits else "AMBIGUOUS", str(q))
    return hits[0]

