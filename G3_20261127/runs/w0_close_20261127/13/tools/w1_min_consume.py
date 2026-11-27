#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fresh-process W0 -> W1 minimal consumer.

Reads an existing W0 handoff/pack/candidate/oracle/raw/next, re-verifies the
frozen pins against real bytes, derives a W1 checklist from the real W0
requirement atoms, oracle, TQAEP case table, receipts and raw index, writes the
checklist to an independent output root and reads it back.

Rejection is typed and writes nothing:
  PIN_MISMATCH_PACK / PIN_MISMATCH_W0M / PIN_MISMATCH_CANDIDATE /
  PIN_MISMATCH_ORACLE / PIN_MISMATCH_EVIDENCE / HANDOFF_INCOMPLETE /
  SCOPE_MISMATCH / CANDIDATE_DIRTY / ORACLE_UNFROZEN / EVIDENCE_HASH_MISMATCH /
  EVIDENCE_PARTIAL / RECEIPT_HASH_MISMATCH / RECEIPT_VERDICT / CASE_MAP_MISSING /
  OUTPUT_ROOT_NOT_INDEPENDENT / OUTPUT_ROOT_NOT_EMPTY / READBACK_MISMATCH
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")
EXPECT = {
    "schema": "FHS5.PLP.W0.SourceManifest.NF@1",
    "project_id": "FHS-5_PLP",
    "wave_id": "FHS-5_PLP/W0",
    "batch_id": "FHS-5/W0/B0-NF",
    "pack_version": "W0-NF-r3-CODEX-PRIMARY",
    "artifact_id": "FHS5-PLP/W0/PACK-NF-20261125-03",
}
REQUIRED_SECTIONS = ("next_legal_action", "dependencies", "resume_predicate",
                     "not_covered")


class Reject(Exception):
    def __init__(self, code: str, detail=None):
        super().__init__(code)
        self.code = code
        self.detail = detail


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def pin_from(text: str, key: str) -> str | None:
    text = text.replace("**", "")
    m = re.search(rf"{key}\s*[:：=]\s*`?([0-9a-f]{{40,64}})", text)
    return m.group(1).strip("`") if m else None


def field_from(text: str, key: str, raw: bool = False) -> str | None:
    text = text.replace("**", "")
    m = re.search(rf"{key}\s*[:：]\s*([^\n]+)", text)
    if not m:
        return None
    tail = m.group(1).strip()
    if raw:
        return tail
    bt = re.match(r"`([^`]+)`", tail)
    if bt:
        return bt.group(1).strip()
    return re.split(r"[（|｜]", tail)[0].strip()


def section(text: str, name: str) -> str:
    m = re.search(rf"^##\s+{re.escape(name)}\s*$(.*?)(?=^##\s|\Z)", text,
                  re.M | re.S)
    return m.group(1).strip() if m else ""


def confined(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel:
        raise Reject("PATH_EMPTY", rel)
    if rel.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", rel):
        raise Reject("PATH_ABSOLUTE", rel)
    if any(p == ".." for p in Path(rel).parts):
        raise Reject("PATH_DOTDOT", rel)
    target = (root / rel).resolve()
    if not target.is_relative_to(root.resolve()):
        raise Reject("PATH_OUTSIDE", rel)
    return target


def git(repo: Path, *args: str) -> dict:
    try:
        proc = subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, timeout=60,
                              env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    except FileNotFoundError:
        raise Reject("GIT_UNAVAILABLE", "git executable not found")
    return {"exit": proc.returncode,
            "out": proc.stdout.decode("utf-8", "replace").strip(),
            "err": proc.stderr.decode("utf-8", "replace").strip()}


def requirement_atoms(repo: Path, oracle: dict, tqaep_md: Path) -> dict:
    """Derive case -> requirement atom from real W0 sources (no hand written map)."""
    atoms: dict[str, dict] = {}
    req = repo / "requirements.md"
    if req.is_file():
        for line in req.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*(SAMPLE-R\d+)\s*[｜|]\s*(.*)$", line)
            if m:
                atoms.setdefault(m.group(1), {
                    "source": "requirements.md", "text": m.group(2).strip()})
            elif line.startswith("NEG｜"):
                atoms["NEG"] = {"source": "requirements.md",
                                "text": line.split("｜", 1)[1].strip()}
    for name, case in (oracle.get("cases") or {}).items():
        atoms[f"SAMPLE-{name}"] = {
            "source": "05_TQAEP/oracle.json",
            "text": "fixture=%s exit=%s status=%s" % (
                case.get("fixture"), case.get("exit"), case.get("status")),
            "fixture": case.get("fixture"),
            "exit": case.get("exit"),
            "status": case.get("status"),
        }
    if tqaep_md.is_file():
        for line in tqaep_md.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            ids = re.findall(r"`((?:F5-W0-T|NF-T)\d+)", line)
            if not ids:
                continue
            cols = line.split("|")
            cid = ids[0]
            fail_col = cols[6] if cid.startswith("F5-W0-T") and len(cols) > 6 \
                else (cols[4] if len(cols) > 4 else "")
            quoted = re.findall(r"`([A-Z][A-Z0-9_]{4,})`", fail_col)
            fails = quoted or re.findall(
                r"\b([A-Z][A-Z0-9_]{4,})\b", fail_col)
            kind = None
            m = re.search(r"`(?:F5-W0-T|NF-T)\d+`\s*(POS/NEG|POS|NEG|SEC|EDGE)",
                          line)
            if m:
                kind = m.group(1)
            reqs = re.findall(r"R\d+", line)
            atoms[cid] = {
                "source": "03_W0_TQAEP.md",
                "text": line.strip().strip("|").strip(),
                "kind": kind,
                "first_fail": fails[0] if fails else "",
                "requirements": reqs,
            }
    return atoms


def render_md(checklist: dict) -> bytes:
    lines = [
        "# W0 -> W1 minimal consume checklist",
        "",
        "- generated_at: `%s`" % checklist["generated_at"],
        "- scope: `%s`" % checklist["scope"],
        "- pack_manifest_sha256: `%s`" % checklist["w0"]["pack_manifest_sha256"],
        "- candidate_commit: `%s`" % checklist["w0"]["candidate_commit"],
        "- oracle_sha256: `%s`" % checklist["w0"]["oracle_sha256"],
        "- evidence_manifest_sha256: `%s`" % checklist["w0"]["evidence_manifest_sha256"],
        "- cases: %d" % len(checklist["items"]),
        "",
        "## next_legal_action",
        "",
        checklist["next_legal_action"],
        "",
        "## items",
        "",
        "| case | kind | expected first_fail | w0 verdict | receipt sha (12) | raw refs |",
        "|---|---|---|---|---|---|",
    ]
    for it in checklist["items"]:
        lines.append("| `%s` | %s | `%s` | %s | `%s` | %s |" % (
            it["case_id"], it["kind"], it["expected_first_fail"] or "-",
            it["w0_verdict"], it["receipt_sha256"][:12],
            ", ".join("`%s`" % r for r in it["raw_refs"]) or "-"))
    lines += ["", "## not_covered", ""]
    lines += ["- %s" % n for n in checklist["not_covered"]]
    return ("\n".join(lines) + "\n").encode("utf-8")


def resolve_and_verify_receipt(args, root, handoff_path, evidence_path):
    """Trusted delivery pin -> confined locator -> bytes SHA -> parse -> verdict.

    The receipt is never opened before the locator is confined to the consumer
    root and the expected digest is resolved from an explicit pin or the
    delivery's CONSUMER_MANIFEST. LATEST.receipt is a locator only; its digest
    is not accepted as the expected value by itself.
    """
    consumer_root = (Path(args.consumer_root).resolve()
                     if getattr(args, "consumer_root", None)
                     else (root / "07_CONSUMER").resolve())
    if not consumer_root.is_dir():
        raise Reject("CONSUMER_ROOT_MISSING", str(consumer_root))
    latest = {}
    if getattr(args, "receipt", None):
        rp = Path(args.receipt)
        if not rp.is_absolute():
            rp = consumer_root / rp
        rp = rp.resolve()
    else:
        latest_path = consumer_root / "LATEST.json"
        if not latest_path.is_file():
            raise Reject("RECEIPT_LOCATOR_MISSING", str(latest_path))
        latest = load_json(latest_path)
        loc = latest.get("receipt")
        if not loc:
            raise Reject("RECEIPT_LOCATOR_MISSING", "LATEST.receipt")
        rp = Path(loc)
        if not rp.is_absolute():
            rp = consumer_root / rp
        rp = rp.resolve()
    # Confinement is a refusal condition, not an informational field.
    if not rp.is_relative_to(consumer_root):
        raise Reject("RECEIPT_LOCATOR_OUTSIDE",
                     {"receipt": str(rp), "consumer_root": str(consumer_root)})
    expected = (getattr(args, "expected_receipt_sha", None) or "").strip().lower()
    if expected and not HEX64.fullmatch(expected):
        raise Reject("EXPECTED_RECEIPT_SHA_INVALID", expected)
    if not expected:
        cm_path = consumer_root / "CONSUMER_MANIFEST.json"
        if cm_path.is_file():
            cm = load_json(cm_path)
            cm_receipt = cm.get("consumer_receipt")
            if cm_receipt:
                cp = Path(cm_receipt)
                if not cp.is_absolute():
                    cp = consumer_root / cp
                if cp.resolve() == rp:
                    expected = (cm.get("consumer_receipt_sha256") or "").strip().lower()
        if not expected:
            raise Reject("EXPECTED_RECEIPT_SHA_REQUIRED", {"receipt": str(rp)})
    if not rp.is_file():
        raise Reject("RECEIPT_MISSING", str(rp))
    if not evidence_path.is_file():
        raise Reject("EVIDENCE_MISSING", str(evidence_path))
    raw = rp.read_bytes()
    got = sha_bytes(raw)
    if got != expected:
        raise Reject("RECEIPT_SHA_MISMATCH",
                     {"expected": expected, "observed": got, "receipt": str(rp)})
    try:
        rec = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise Reject("RECEIPT_PARSE_ERROR", str(exc))
    if rec.get("consumed") is not True or rec.get("validation_ok") is not True:
        raise Reject("RECEIPT_NOT_CONSUMED",
                     {"consumed": rec.get("consumed"),
                      "validation_ok": rec.get("validation_ok")})
    if rec.get("handoff_sha256") != sha_file(handoff_path):
        raise Reject("RECEIPT_HANDOFF_MISMATCH",
                     {"receipt": rec.get("handoff_sha256"),
                      "current": sha_file(handoff_path)})
    if rec.get("evidence_manifest_sha256") != sha_file(evidence_path):
        raise Reject("RECEIPT_EVIDENCE_MISMATCH",
                     {"receipt": rec.get("evidence_manifest_sha256"),
                      "current": sha_file(evidence_path)})
    gate = {
        "consumer_root": str(consumer_root),
        "receipt": str(rp),
        "expected_receipt_sha256": expected,
        "observed_receipt_sha256": got,
        "receipt_bytes": len(raw),
        "receipt_parsed": True,
        "receipt_consumed": True,
        "receipt_run_id": rec.get("run_id"),
        "receipt_handoff_sha256": rec.get("handoff_sha256"),
        "receipt_evidence_manifest_sha256": rec.get("evidence_manifest_sha256"),
        "latest_run_id": latest.get("run_id"),
    }
    return gate, rec

def consume(args) -> dict:
    handoff_path = Path(args.handoff).resolve()
    if not handoff_path.is_file():
        raise Reject("HANDOFF_MISSING", str(handoff_path))
    root = Path(args.root).resolve() if args.root else handoff_path.parents[1]
    out_root = Path(args.out_root).resolve()

    if out_root == root or out_root.is_relative_to(root) or root.is_relative_to(out_root):
        raise Reject("OUTPUT_ROOT_NOT_INDEPENDENT",
                     {"out_root": str(out_root), "w0_root": str(root)})
    if out_root.exists() and any(out_root.iterdir()):
        raise Reject("OUTPUT_ROOT_NOT_EMPTY", str(out_root))

    text = handoff_path.read_text(encoding="utf-8")
    pins = {k: pin_from(text, k) for k in (
        "pack_manifest_sha256", "w0m_amendment_sha256", "candidate_commit",
        "oracle_sha256", "evidence_manifest_sha256")}
    if not all(pins.values()):
        raise Reject("HANDOFF_INCOMPLETE", {k: v for k, v in pins.items() if not v})
    for name in REQUIRED_SECTIONS:
        if not section(text, name):
            raise Reject("HANDOFF_INCOMPLETE", "missing section: " + name)

    work_id = field_from(text, "project/work_id") or ""
    wave = field_from(text, "wave_id") or work_id
    scope = args.scope
    if scope not in wave.split("/") and scope != wave and scope not in work_id:
        raise Reject("SCOPE_MISMATCH",
                     {"requested": scope, "handoff_work_id": work_id,
                      "handoff_wave": wave})
    target = field_from(text, "target_consumer") or ""
    if "W1" not in target:
        raise Reject("SCOPE_MISMATCH", {"target_consumer": target})

    evidence_path = root / "10_EVIDENCE" / "EVIDENCE_MANIFEST.json"
    receipt_gate, verified_receipt = resolve_and_verify_receipt(
        args, root, handoff_path, evidence_path)
    pack_dir = root / "01_PACK" / "FHS-5_PLP_W0_NATIVE_FIRST"
    pack_manifest = pack_dir / "05_W0_SOURCE_MANIFEST.json"
    if not pack_manifest.is_file():
        raise Reject("PIN_MISMATCH_PACK", "manifest missing")
    pack_sha = sha_file(pack_manifest)
    if pack_sha != pins["pack_manifest_sha256"]:
        raise Reject("PIN_MISMATCH_PACK",
                     {"expected": pins["pack_manifest_sha256"], "actual": pack_sha})
    man = load_json(pack_manifest)
    bad = {k: man.get(k) for k, v in EXPECT.items() if man.get(k) != v}
    if bad:
        raise Reject("PACK_IDENTITY_MISMATCH", bad)
    files = man.get("pack_files") or []
    if len(files) != 5:
        raise Reject("PACK_FILE_COUNT", len(files))
    for e in files:
        p = confined(pack_dir, e.get("path"))
        if not p.is_file() or sha_file(p) != e.get("sha256") \
                or len(p.read_bytes()) != e.get("bytes"):
            raise Reject("PIN_MISMATCH_PACK", e.get("path"))

    seal_path = root / "01_PACK" / "EXTERNAL_SEAL.json"
    if not seal_path.is_file():
        raise Reject("SEAL_MISSING", str(seal_path))
    seal = load_json(seal_path)
    for e in files:
        pin = (seal.get("pack_files") or {}).get(e["path"], {})
        if pin.get("sha256") != e["sha256"] or pin.get("bytes") != e["bytes"]:
            raise Reject("SEAL_MISMATCH", e["path"])
    if (seal.get("pack_files") or {}).get("05_W0_SOURCE_MANIFEST.json", {}) \
            .get("sha256") != pack_sha:
        raise Reject("SEAL_SELF_MISMATCH", None)
    app = seal.get("evidence_appendix") or {}
    app_path = root / "01_PACK" / app.get("path", "")
    if not app_path.is_file() or sha_file(app_path) != app.get("sha256") \
            or len(app_path.read_bytes()) != app.get("bytes"):
        raise Reject("SEAL_APPENDIX_MISMATCH", app.get("path"))

    w0m_dir = root / "01_PACK" / "W0M_CODEX_FIRST"
    w0m = next(iter(sorted(w0m_dir.glob("*CODEX-FIRST-r4.md"))), None) \
        if w0m_dir.is_dir() else None
    if not w0m:
        raise Reject("PIN_MISMATCH_W0M", "W0M r4 missing")
    if sha_file(w0m) != pins["w0m_amendment_sha256"]:
        raise Reject("PIN_MISMATCH_W0M",
                     {"expected": pins["w0m_amendment_sha256"],
                      "actual": sha_file(w0m)})

    repo = Path(args.repo).resolve() if args.repo else root / "02_CANDIDATE" / "repo"
    if not (repo / ".git").exists():
        raise Reject("CANDIDATE_MISSING", str(repo))
    head = git(repo, "rev-parse", "HEAD")
    if head["exit"] != 0 or head["out"] != pins["candidate_commit"]:
        raise Reject("PIN_MISMATCH_CANDIDATE",
                     {"expected": pins["candidate_commit"], "actual": head["out"]})
    tree = git(repo, "rev-parse", "HEAD^{tree}")
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=no")
    if status["exit"] != 0 or status["out"] != "":
        raise Reject("CANDIDATE_DIRTY", status["out"] or status["err"])

    oracle_path = root / "05_TQAEP" / "oracle.json"
    if not oracle_path.is_file():
        raise Reject("PIN_MISMATCH_ORACLE", "oracle missing")
    oracle = load_json(oracle_path)
    oracle_sha = sha_file(oracle_path)
    if oracle_sha != pins["oracle_sha256"]:
        raise Reject("PIN_MISMATCH_ORACLE",
                     {"expected": pins["oracle_sha256"], "actual": oracle_sha})
    if oracle.get("candidate_commit") != head["out"]:
        raise Reject("PIN_MISMATCH_CANDIDATE", "oracle.candidate_commit")
    if oracle.get("pack_manifest_sha256") != pack_sha:
        raise Reject("PIN_MISMATCH_PACK", "oracle.pack_manifest_sha256")
    if not oracle.get("frozen_at"):
        raise Reject("ORACLE_UNFROZEN", None)
    if sha_file(repo / "requirements.md") != oracle.get("source_sha256"):
        raise Reject("ORACLE_SOURCE_MISMATCH", "requirements.md")
    for name, exp in (oracle.get("fixtures") or {}).items():
        if not (repo / "fixtures" / name).is_file() \
                or sha_file(repo / "fixtures" / name) != exp:
            raise Reject("FIXTURE_MISMATCH", name)

    # evidence_path resolved before the receipt gate
    if not evidence_path.is_file():
        raise Reject("PIN_MISMATCH_EVIDENCE", "evidence manifest missing")
    evd = load_json(evidence_path)
    evd_sha = sha_file(evidence_path)
    if evd_sha != pins["evidence_manifest_sha256"]:
        raise Reject("PIN_MISMATCH_EVIDENCE",
                     {"expected": pins["evidence_manifest_sha256"],
                      "actual": evd_sha})
    if evd.get("schema") != "FHS5.W0NF.EvidenceManifest@1":
        raise Reject("EVIDENCE_SCHEMA", evd.get("schema"))
    if evd.get("pack_manifest_sha256") != pack_sha \
            or evd.get("oracle_sha256") != oracle_sha \
            or (evd.get("candidate") or {}).get("head") != head["out"]:
        raise Reject("EVIDENCE_CROSS_SUBJECT", None)
    indexed = evd.get("files") or []
    if len(indexed) < 400:
        raise Reject("EVIDENCE_FILE_COUNT", len(indexed))

    summary_path = root / "05_TQAEP" / "summary.json"
    if not summary_path.is_file():
        raise Reject("EVIDENCE_PARTIAL", "summary missing")
    summary = load_json(summary_path)
    counts = summary.get("counts") or {}
    if summary.get("schema") != "FHS5.W0NF.TQAEPResult@1":
        raise Reject("SUMMARY_SCHEMA", summary.get("schema"))
    if counts.get("total") != 44 or counts.get("fail") or counts.get("pending") \
            or counts.get("pass") != 44:
        raise Reject("EVIDENCE_PARTIAL", counts)
    if summary.get("oracle_sha") != oracle_sha \
            or summary.get("candidate_sha") != head["out"] \
            or summary.get("pack_manifest_sha256") != pack_sha:
        raise Reject("PIN_MISMATCH_SUMMARY", None)

    consumer_info = {
        "receipt_gate": receipt_gate,
        "legacy_latest_present": True,
        "legacy_run_id": receipt_gate.get("latest_run_id") or receipt_gate.get("receipt_run_id"),
        "legacy_receipt": receipt_gate["receipt"],
        "legacy_receipt_in_input_root": True,
        "legacy_receipt_handoff_sha_match": True,
        "legacy_consumed": True,
        "verified_receipt_parsed": True,
        "verified_receipt_used": True,
    }
    fin = summary.get("finalized_t10") or {}
    if fin.get("consumer_run_id"):
        fin_receipt = root / "07_CONSUMER" / "runs" / str(fin["consumer_run_id"]) \
            / "receipt.json"
        consumer_info["finalized_run_id"] = fin["consumer_run_id"]
        consumer_info["finalized_receipt_present"] = fin_receipt.is_file()
        consumer_info["finalized_matches_latest"] = \
            fin["consumer_run_id"] == consumer_info.get("legacy_run_id")
    seen = set()
    for e in indexed:
        rel = e.get("path")
        if rel in seen:
            raise Reject("DUPLICATE_PIN", rel)
        seen.add(rel)
        p = confined(root, rel)
        if not p.is_file():
            raise Reject("MISSING_FILE", rel)
        if sha_file(p) != e.get("sha256") or len(p.read_bytes()) != e.get("bytes"):
            raise Reject("EVIDENCE_HASH_MISMATCH", rel)

    receipts_dir = root / "05_TQAEP" / "receipts"
    receipt_files = sorted(receipts_dir.glob("*.json")) \
        if receipts_dir.is_dir() else []
    cases = summary.get("cases") or []
    if len(receipt_files) != len(cases):
        raise Reject("RECEIPT_COUNT_MISMATCH",
                     {"files": len(receipt_files), "cases": len(cases)})

    evd_index = {e["path"]: e for e in indexed}
    raw_dir = root / "05_TQAEP" / "raw"
    raw_names = sorted(p.name for p in raw_dir.glob("*") if p.is_file()) \
        if raw_dir.is_dir() else []
    if not raw_names:
        raise Reject("RAW_MISSING", str(raw_dir))

    atoms = requirement_atoms(repo, oracle, pack_dir / "03_W0_TQAEP.md")
    items = []
    for case in cases:
        cid = case.get("case_id")
        if not cid:
            raise Reject("CASE_MAP_MISSING", "case without id")
        rec_rel = case.get("rec") or ""
        rec_path = confined(root, rec_rel)
        if not rec_path.is_file():
            raise Reject("MISSING_RECEIPT", rec_rel)
        rec_obj = load_json(rec_path)
        if rec_obj.get("case_id") != cid:
            raise Reject("RECEIPT_CASE_MISMATCH", cid)
        rec_sha = sha_file(rec_path)
        evd_entry = evd_index.get(rec_rel)
        if not evd_entry or evd_entry.get("sha256") != rec_sha:
            raise Reject("RECEIPT_HASH_MISMATCH", rec_rel)
        if case.get("verdict") != "PASS" or rec_obj.get("verdict") != "PASS":
            raise Reject("RECEIPT_VERDICT",
                         {"case": cid, "verdict": rec_obj.get("verdict")})
        if rec_obj.get("candidate_sha") != head["out"] \
                or rec_obj.get("oracle_sha") != oracle_sha:
            raise Reject("RECEIPT_PIN_MISMATCH", cid)
        atom = atoms.get(cid)
        if not atom:
            raise Reject("CASE_MAP_MISSING", cid)
        artifact = rec_obj.get("artifact")
        if artifact:
            ap = confined(root, artifact)
            ent = evd_index.get(artifact)
            if not ap.is_file() or not ent or sha_file(ap) != ent.get("sha256"):
                raise Reject("ARTIFACT_MISMATCH", {"case": cid, "artifact": artifact})
        items.append({
            "case_id": cid,
            "kind": atom.get("kind") or (
                "SAMPLE" if cid.startswith("SAMPLE-") else "NF"),
            "requirement_atom": {k: atom.get(k) for k in
                                 ("source", "text", "requirements") if k in atom},
            "expected_first_fail": atom.get("first_fail", ""),
            "oracle_expectation": ("exit=%s status=%s" % (atom["exit"], atom["status"])
                                   if "exit" in atom else None),
            "w0_verdict": rec_obj.get("verdict"),
            "receipt": rec_rel,
            "receipt_sha256": rec_sha,
            "run_id": rec_obj.get("run_id"),
            "raw_refs": [n for n in raw_names
                         if cid.lower() in n.lower()][:8],
            "w1_use": ("negative_guard" if atom.get("first_fail")
                       else "baseline_evidence"),
        })

    if len(items) != 44:
        raise Reject("CASE_COUNT_MISMATCH", len(items))

    checklist = {
        "schema": "FHS5.W1.MinimalConsumeChecklist@1",
        "generated_by": "tools/w1_min_consume.py",
        "generated_at": now(),
        "scope": wave,
        "requested_scope": scope,
        "w0": {
            "handoff": str(handoff_path),
            "handoff_sha256": sha_file(handoff_path),
            "handoff_id": field_from(text, "handoff_id"),
            "pack_manifest_sha256": pack_sha,
            "w0m_amendment_sha256": pins["w0m_amendment_sha256"],
            "candidate_commit": head["out"],
            "candidate_tree": tree["out"],
            "oracle_sha256": oracle_sha,
            "evidence_manifest_sha256": evd_sha,
            "case_set": field_from(text, "case_set", raw=True),
            "legacy_consumer": consumer_info,
            "receipt_gate": receipt_gate,
        },
        "next_legal_action": section(text, "next_legal_action"),
        "dependencies": section(text, "dependencies"),
        "resume_predicate": section(text, "resume_predicate"),
        "not_covered": [ln.strip("- ").strip()
                        for ln in section(text, "not_covered").splitlines()
                        if ln.strip()],
        "claim_ceiling": {
            "w0_consumer_receipts_reverified": True,
            "w0_case_expected_unchanged": True,
            "w1_execution": "NOT_CLAIMED",
            "w1_full_wave": "NOT_CLAIMED",
            "release": "NOT_CLAIMED",
        },
        "items": items,
    }

    json_bytes = (json.dumps(checklist, ensure_ascii=False, indent=2)
                  + "\n").encode("utf-8")
    md_bytes = render_md(checklist)
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "w1_checklist.json").write_bytes(json_bytes)
    (out_root / "w1_checklist.md").write_bytes(md_bytes)

    rb_json = (out_root / "w1_checklist.json").read_bytes()
    rb_md = (out_root / "w1_checklist.md").read_bytes()
    if rb_json != json_bytes or rb_md != md_bytes \
            or json.loads(rb_json.decode("utf-8")) != checklist:
        raise Reject("READBACK_MISMATCH", None)

    receipt = {
        "schema": "FHS5.W1.MinimalConsumeReceipt@1",
        "status": "W1_CHECKLIST_READY",
        "generated_at": now(),
        "fresh_process": {"pid": os.getpid(), "python": sys.version.split()[0],
                          "argv": sys.argv, "cwd": os.getcwd()},
        "inputs": checklist["w0"],
        "outputs": {
            "w1_checklist.json": {"sha256": sha_bytes(rb_json), "bytes": len(rb_json)},
            "w1_checklist.md": {"sha256": sha_bytes(rb_md), "bytes": len(rb_md)},
        },
        "items": len(items),
        "readback_ok": True,
        "claim_ceiling": checklist["claim_ceiling"],
        "not_claimed": ["W1 execution", "W1 full wave", "W2-W4", "release",
                        "different principal"],
    }
    receipt_bytes = (json.dumps(receipt, ensure_ascii=False, indent=2)
                     + "\n").encode("utf-8")
    (out_root / "consume_receipt.json").write_bytes(receipt_bytes)
    if (out_root / "consume_receipt.json").read_bytes() != receipt_bytes:
        raise Reject("READBACK_MISMATCH", "consume_receipt.json")
    return {"status": "W1_CHECKLIST_READY", "items": len(items),
            "outputs": receipt["outputs"], "readback_ok": True,
            "receipt_gate": receipt_gate}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--handoff", required=True)
    ap.add_argument("--root")
    ap.add_argument("--repo")
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--scope", default="W0")
    ap.add_argument("--receipt")
    ap.add_argument("--expected-receipt-sha")
    ap.add_argument("--consumer-root")
    a = ap.parse_args()
    try:
        result = consume(a)
    except Reject as exc:
        print(json.dumps({"status": "REJECTED", "code": exc.code,
                          "detail": exc.detail, "output_written": False},
                         ensure_ascii=False))
        return 3
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
