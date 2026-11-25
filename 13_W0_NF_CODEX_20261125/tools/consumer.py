#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W1 consumer v3: fail-closed verification of identity, pack, seal, W0M,
candidate, oracle, handoff, evidence-manifest contents and path confinement
BEFORE any product CLI runs. One unique run directory per invocation."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

CONSUMER_ROOT = lib.ROOT / "07_CONSUMER"
EXPECT = {
    "schema": "FHS5.PLP.W0.SourceManifest.NF@1",
    "project_id": "FHS-5_PLP",
    "wave_id": "FHS-5_PLP/W0",
    "batch_id": "FHS-5/W0/B0-NF",
    "pack_version": "W0-NF-r3-CODEX-PRIMARY",
    "artifact_id": "FHS5-PLP/W0/PACK-NF-20261125-03",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def pin_from(text: str, key: str) -> str | None:
    text = text.replace("**", "")
    m = re.search(rf"{key}\s*[:：=]\s*`?([0-9a-f]{{64}}|`?[0-9a-f]{{40}})", text)
    return m.group(1).strip("`") if m else None


def section(text: str, name: str) -> str:
    m = re.search(rf"^##\s+{re.escape(name)}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


class Verify:
    def __init__(self):
        self.checks: list[dict] = []
        self.failure = None

    def add(self, cid: str, ok: bool, detail=None, code: str | None = None):
        self.checks.append({"id": cid, "ok": bool(ok), "detail": detail})
        if not ok and self.failure is None:
            self.failure = code or cid
        return ok

    def done(self) -> bool:
        return self.failure is None and all(c["ok"] for c in self.checks)


def confined(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel:
        raise ValueError("PATH_EMPTY")
    if rel.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", rel):
        raise ValueError("PATH_ABSOLUTE")
    if any(p == ".." for p in Path(rel).parts):
        raise ValueError("PATH_DOTDOT")
    target = (root / rel).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("PATH_OUTSIDE")
    return target


def run_validation(pack: Path, repo: Path, handoff: Path, evidence: Path,
                   evidence_root: Path, allow_pending_t10: bool):
    v = Verify()
    info: dict = {}

    man = load(pack / "05_W0_SOURCE_MANIFEST.json")
    v.add("IDENTITY", all(man.get(k) == val for k, val in EXPECT.items()),
          {k: man.get(k) for k in EXPECT}, "IDENTITY_MISMATCH")
    files = man.get("pack_files") or []
    v.add("PACK-FILE-COUNT", len(files) == 5, len(files), "PACK_FILE_COUNT")
    for e in files:
        p = pack / e["path"]
        ok = p.is_file() and lib.sha_file(p) == e["sha256"] and len(p.read_bytes()) == e["bytes"]
        v.add("PACK-" + e["path"], ok, {"sha": lib.sha_file(p) if p.is_file() else None},
              "PACK_PIN_MISMATCH")
    pack_sha = lib.sha_file(pack / "05_W0_SOURCE_MANIFEST.json")
    info["pack_manifest_sha256"] = pack_sha

    seal_path = pack.parent / "EXTERNAL_SEAL.json"
    if v.add("SEAL-PRESENT", seal_path.is_file(), str(seal_path), "SEAL_MISSING"):
        seal = load(seal_path)
        seal_ok = all(seal.get("pack_files", {}).get(e["path"], {}).get("sha256") == e["sha256"]
                      for e in files)
        v.add("SEAL-PACK-PINS", seal_ok, None, "SEAL_MISMATCH")
        v.add("SEAL-MANIFEST-SELF",
              seal.get("manifest_self_hash") == "EXTERNAL_RECORD_ONLY"
              and seal.get("pack_files", {}).get("05_W0_SOURCE_MANIFEST.json", {}).get("sha256") == pack_sha,
              None, "SEAL_SELF_MISMATCH")
        app = seal.get("evidence_appendix") or {}
        ap = pack.parent / app.get("path", "")
        v.add("SEAL-APPENDIX", ap.is_file() and lib.sha_file(ap) == app.get("sha256")
              and len(ap.read_bytes()) == app.get("bytes"), None, "SEAL_APPENDIX_MISMATCH")

    text = handoff.read_text(encoding="utf-8")
    h = {
        "pack_manifest_sha256": pin_from(text, "pack_manifest_sha256"),
        "w0m_amendment_sha256": pin_from(text, "w0m_amendment_sha256"),
        "candidate_commit": pin_from(text, "candidate_commit"),
        "oracle_sha256": pin_from(text, "oracle_sha256"),
        "evidence_manifest_sha256": pin_from(text, "evidence_manifest_sha256"),
        "consumer_manifest_sha256": pin_from(text, "consumer_manifest_sha256"),
    }
    info["handoff"] = h
    v.add("HANDOFF-PACK-PIN", h["pack_manifest_sha256"] == pack_sha,
          h["pack_manifest_sha256"], "PIN_MISMATCH_PACK")

    w0m = next((pack.parent / "W0M_CODEX_FIRST").glob("*CODEX-FIRST-r4.md"), None)
    v.add("W0M-PRESENT", bool(w0m), None, "W0M_MISSING")
    if w0m:
        v.add("W0M-PIN", lib.sha_file(w0m) == h["w0m_amendment_sha256"], lib.sha_file(w0m),
              "PIN_MISMATCH_W0M")

    head = lib.run(["git", "-C", str(repo), "rev-parse", "HEAD"], lib.ROOT)["stdout"].strip()
    tree = lib.run(["git", "-C", str(repo), "rev-parse", "HEAD^{tree}"], lib.ROOT)["stdout"].strip()
    status = lib.run(["git", "-C", str(repo), "status", "--porcelain=v1", "--untracked-files=no"],
                     lib.ROOT)["stdout"].strip()
    info["candidate"] = {"head": head, "tree": tree}
    v.add("CANDIDATE-PIN", head == h["candidate_commit"], {"head": head}, "PIN_MISMATCH_CANDIDATE")
    v.add("CANDIDATE-CLEAN", status == "", status, "CANDIDATE_DIRTY")

    oracle_path = pack.parent.parent / "05_TQAEP" / "oracle.json"
    oracle = load(oracle_path)
    osha = lib.sha_file(oracle_path)
    info["oracle_sha256"] = osha
    v.add("ORACLE-PIN", osha == h["oracle_sha256"], {"sha": osha}, "PIN_MISMATCH_ORACLE")
    v.add("ORACLE-CANDIDATE", oracle.get("candidate_commit") == head,
          oracle.get("candidate_commit"), "ORACLE_CANDIDATE_MISMATCH")
    v.add("ORACLE-FROZEN", bool(oracle.get("frozen_at")), oracle.get("frozen_at"), "ORACLE_UNFROZEN")
    req_sha = lib.sha_file(repo / "requirements.md")
    v.add("ORACLE-SOURCE", oracle.get("source_sha256") == req_sha, req_sha, "ORACLE_SOURCE_MISMATCH")
    for name, exp in (oracle.get("fixtures") or {}).items():
        p = repo / "fixtures" / name
        v.add("ORACLE-FIX-" + name, p.is_file() and lib.sha_file(p) == exp, name, "FIXTURE_MISMATCH")

    esha = lib.sha_file(evidence)
    info["evidence_manifest_sha256"] = esha
    v.add("EVIDENCE-PIN", esha == h["evidence_manifest_sha256"], {"sha": esha},
          "PIN_MISMATCH_EVIDENCE")
    evd = load(evidence)
    v.add("EVIDENCE-SCHEMA", evd.get("schema") == "FHS5.W0NF.EvidenceManifest@1",
          evd.get("schema"), "EVIDENCE_SCHEMA")
    v.add("EVIDENCE-PACK", evd.get("pack_manifest_sha256") == pack_sha, None, "EVIDENCE_PACK_MISMATCH")
    v.add("EVIDENCE-CANDIDATE", (evd.get("candidate") or {}).get("head") == head, None,
          "EVIDENCE_CANDIDATE_MISMATCH")
    v.add("EVIDENCE-ORACLE", evd.get("oracle_sha256") == osha, None, "EVIDENCE_ORACLE_MISMATCH")

    root = evidence_root.resolve()
    indexed = evd.get("files") or []
    v.add("EVIDENCE-FILE-COUNT", len(indexed) >= 400, len(indexed), "EVIDENCE_FILE_COUNT")
    seen = set()
    for entry in indexed:
        rel = entry.get("path")
        if rel in seen:
            v.add("EVIDENCE-DUP-" + str(rel), False, rel, "DUPLICATE_PIN")
            continue
        seen.add(rel)
        try:
            p = confined(root, rel)
        except ValueError as exc:
            v.add("EVIDENCE-PATH-" + str(rel)[:60], False, str(exc), str(exc))
            continue
        if not p.is_file():
            v.add("EVIDENCE-MISSING-" + str(rel)[:60], False, rel, "MISSING_FILE")
            continue
        ok = lib.sha_file(p) == entry.get("sha256") and len(p.read_bytes()) == entry.get("bytes")
        v.add("EVIDENCE-FILE-" + str(rel)[:60], ok, rel, "EVIDENCE_HASH_MISMATCH")

    def require(rel: str, cid: str):
        try:
            p = confined(root, rel)
        except ValueError:
            return v.add(cid, False, rel, "PATH_ESCAPE")
        return v.add(cid, p.is_file(), rel, "MISSING_" + cid)

    for rel, cid in (
        ("05_TQAEP/oracle.json", "REQ-ORACLE"),
        ("05_TQAEP/summary.json", "REQ-SUMMARY"),
        ("03_PARTIES/challenge/challenge.json", "REQ-CHALLENGE"),
        ("03_PARTIES/far/far.json", "REQ-FAR"),
        ("04_DEV_OPS/ops.json", "REQ-OPS"),
        ("04_DEV_OPS/dev_patch.json", "REQ-DEV"),
        ("03_PARTIES/security/security_wsl.json", "REQ-SECURITY"),
        ("04_DEV_OPS/off_legacy.json", "REQ-OFF-LEGACY"),
        ("04_DEV_OPS/off_bridge.json", "REQ-OFF-BRIDGE"),
        ("04_DEV_OPS/off_far.json", "REQ-OFF-FAR"),
        ("03_PARTIES/collab/chain.json", "REQ-COLLAB"),
    ):
        require(rel, cid)

    summary = load(root / "05_TQAEP/summary.json")
    v.add("SUMMARY-COUNTS", summary.get("counts", {}).get("total") == 44,
          summary.get("counts"), "SUMMARY_COUNT")
    v.add("SUMMARY-ORACLE", (summary.get("oracle_sha256") or summary.get("oracle_sha")) == osha,
          None, "SUMMARY_ORACLE_MISMATCH")
    v.add("SUMMARY-CANDIDATE", summary.get("candidate_sha") == head, None, "SUMMARY_CANDIDATE_MISMATCH")

    receipts = summary.get("receipts") or evd.get("receipts") or {}
    v.add("RECEIPT-COUNT", len(receipts) == 44, len(receipts), "RECEIPT_COUNT")
    for name, sha in receipts.items():
        p = root / "05_TQAEP" / "receipts" / name
        if not p.is_file():
            v.add("RECEIPT-MISSING-" + name, False, name, "MISSING_RECEIPT")
            continue
        if lib.sha_file(p) != sha:
            v.add("RECEIPT-HASH-" + name, False, name, "RECEIPT_HASH_MISMATCH")
            continue
        rec = load(p)
        cid = rec.get("case_id")
        verdict = rec.get("verdict")
        allowed = verdict == "PASS" or (allow_pending_t10 and cid == "NF-T10"
                                        and verdict == "PENDING_CONSUMER")
        v.add("RECEIPT-" + str(cid), allowed and rec.get("candidate_sha") == head
              and rec.get("oracle_sha") == osha, {"verdict": verdict}, "RECEIPT_VERDICT")

    chal = load(root / "03_PARTIES/challenge/challenge.json")
    v.add("CHALLENGE-VERDICT", chal.get("verdict") == "PASS", chal.get("verdict"), "CHALLENGE_FAIL")
    v.add("CHALLENGE-CANDIDATE", (chal.get("pins") or {}).get("candidate") == head, None,
          "CHALLENGE_CANDIDATE_MISMATCH")
    v.add("CHALLENGE-ORACLE", (chal.get("pins") or {}).get("oracle") == osha, None,
          "CHALLENGE_ORACLE_MISMATCH")
    far = load(root / "03_PARTIES/far/far.json")
    v.add("FAR-ALTERNATIVES", len(far.get("alternatives") or []) >= 2, None, "FAR_ALTERNATIVES")
    v.add("FAR-RAW", bool(re.fullmatch(r"[0-9a-f]{64}", (far.get("finding") or {}).get("raw_sha256") or "")),
          None, "FAR_RAW")
    ops = load(root / "04_DEV_OPS/ops.json")
    v.add("OPS-VERDICT", ops.get("verdict") == "PASS", ops.get("verdict"), "OPS_FAIL")
    dev = load(root / "04_DEV_OPS/dev_patch.json")
    v.add("DEV-VERDICT", dev.get("verdict") == "PASS", dev.get("verdict"), "DEV_FAIL")
    collab = load(root / "03_PARTIES/collab/chain.json")
    v.add("COLLAB-VERDICT", collab.get("verdict") == "COMBINED_OK", collab.get("verdict"), "COLLAB_FAIL")
    sec = load(root / "03_PARTIES/security/security_wsl.json")
    v.add("SECURITY-VERDICT", sec.get("verdict") == "PASS", sec.get("verdict"), "SECURITY_FAIL")
    for name in ("off_legacy", "off_bridge", "off_far"):
        o = load(root / "04_DEV_OPS" / f"{name}.json")
        v.add("OFF-" + name, o.get("verdict") == "PASS", o.get("verdict"), "OFF_FAIL")

    for key in ("next_legal_action", "dependencies", "resume_predicate", "not_covered"):
        body = section(text, key)
        v.add("HANDOFF-" + key.upper(), bool(body), len(body), "HANDOFF_INCOMPLETE")
    v.add("HANDOFF-TARGET", "W1" in (pin_from(text, "target_consumer") or text),
          None, "HANDOFF_TARGET")
    return v, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(lib.ROOT))
    ap.add_argument("--pack")
    ap.add_argument("--repo")
    ap.add_argument("--handoff")
    ap.add_argument("--evidence-manifest")
    ap.add_argument("--evidence-root")
    ap.add_argument("--out-root")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--allow-pending-t10", action="store_true")
    ap.add_argument("--expect-reject", action="store_true")
    ap.add_argument("--publish-manifest", action="store_true")
    a = ap.parse_args()

    delivery_root = Path(a.root).resolve()
    pack = Path(a.pack).resolve() if a.pack else delivery_root / "01_PACK" / "FHS-5_PLP_W0_NATIVE_FIRST"
    handoff = Path(a.handoff).resolve() if a.handoff else delivery_root / "09_DELIVERY" / "W0_HANDOFF.md"
    evidence = (Path(a.evidence_manifest).resolve() if a.evidence_manifest
                else delivery_root / "10_EVIDENCE" / "EVIDENCE_MANIFEST.json")
    evidence_root = Path(a.evidence_root).resolve() if a.evidence_root else delivery_root
    out_root = Path(a.out_root).resolve() if a.out_root else delivery_root / "07_CONSUMER"
    out_root.mkdir(parents=True, exist_ok=True)
    run_id = a.run_id or (datetime.now().strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8])
    run_dir = out_root / "runs" / run_id
    if run_dir.exists():
        raise SystemExit("RUN_ID_EXISTS")
    run_dir.mkdir(parents=True)
    if a.repo:
        repo = Path(a.repo).resolve()
    else:
        bundle = delivery_root / "02_CANDIDATE" / "repo.bundle"
        repo = run_dir / "candidate"
        cl = lib.run(["git", "clone", "--quiet", str(bundle), str(repo)], run_dir,
                     raw_dir=run_dir / "raw", tag="materialize_clone")
        commit = pin_from(handoff.read_text(encoding="utf-8"), "candidate_commit")
        co = lib.run(["git", "-C", str(repo), "checkout", "--quiet", commit], run_dir,
                     raw_dir=run_dir / "raw", tag="materialize_checkout")
        if cl["exit"] != 0 or co["exit"] != 0:
            raise SystemExit("CANDIDATE_MATERIALIZE_FAILED")

    v, info = run_validation(pack, repo, handoff, evidence, evidence_root, a.allow_pending_t10)
    validation_ok = v.done()
    cli = {"executed": False}

    if validation_ok:
        root = run_dir / "root"
        root.mkdir()
        for p in (repo / "fixtures").glob("*.md"):
            shutil.copy2(p, root / p.name)
        pos = lib.cli(["--root", str(root), "--input", "case_ok.md",
                       "--sha256", lib.sha_file(root / "case_ok.md")], root,
                      env_extra={"PYTHONPATH": str(repo)}, raw_dir=run_dir / "raw", tag="pos")
        neg = lib.cli(["--root", str(root), "--input", "case_missing.md",
                       "--sha256", lib.sha_file(root / "case_missing.md")], root,
                      env_extra={"PYTHONPATH": str(repo)}, raw_dir=run_dir / "raw", tag="neg")
        try:
            pos_json, neg_json = json.loads(pos["stdout"]), json.loads(neg["stdout"])
        except Exception:
            pos_json, neg_json = {}, {}
        runs_ok = (pos["exit"] == 0 and pos_json.get("status") == "COMPLETE"
                   and pos_json.get("provided") == ["A", "B"]
                   and neg["exit"] == 2 and neg_json.get("status") == "MISSING"
                   and neg_json.get("missing") == ["B"])
        cli = {"executed": True, "pos_exit": pos["exit"], "neg_exit": neg["exit"],
               "pos_stdout_sha": pos["stdout_sha256"], "neg_stdout_sha": neg["stdout_sha256"],
               "semantics_ok": runs_ok}
        if not runs_ok:
            validation_ok = False
            v.failure = v.failure or "EFFECT_NOT_VERIFIED"
    else:
        cli = {"executed": False, "reason": "FAIL_CLOSED_BEFORE_CLI"}

    consumed = bool(validation_ok and cli.get("semantics_ok"))
    receipt = {
        "schema": "FHS5.W0NF.ConsumerReceipt@3",
        "run_id": run_id,
        "created_at": now(),
        "consumer_id": "W1-consumer/CODEX-Native-1 (separate process)",
        "pack": str(pack),
        "repo": str(repo),
        "handoff": str(handoff),
        "handoff_sha256": lib.sha_file(handoff),
        "evidence_manifest": str(evidence),
        "evidence_manifest_sha256": lib.sha_file(evidence),
        "validation_ok": validation_ok,
        "failure_code": None if validation_ok else v.failure,
        "checks": v.checks,
        "cli": cli,
        "consumed": consumed,
        "rejected": not consumed,
        "not_claimed": ["HERMES/GPT host execution", "W1 product execution", "release"],
    }
    receipt_path = run_dir / "receipt.json"
    lib.write_json(receipt_path, receipt)
    if consumed:
        lib.write_json(out_root / "LATEST.json",
                       {"run_id": run_id, "receipt": str(receipt_path)})

    if a.publish_manifest and consumed:
        raw = {p.name: lib.sha_file(p) for p in sorted((run_dir / "raw").glob("*")) if p.is_file()}
        cm = {
            "schema": "FHS5.W0NF.ConsumerManifest@2",
            "run_id": run_id,
            "consumer_receipt": str(receipt_path),
            "consumer_receipt_sha256": lib.sha_file(receipt_path),
            "evidence_manifest_sha256": receipt["evidence_manifest_sha256"],
            "handoff_sha256": receipt["handoff_sha256"],
            "pack_manifest_sha256": info.get("pack_manifest_sha256"),
            "candidate": info.get("candidate"),
            "oracle_sha256": info.get("oracle_sha256"),
            "consumed": True,
            "raw": raw,
            "not_claimed": receipt["not_claimed"],
        }
        lib.write_json(out_root / "CONSUMER_MANIFEST.json", cm)
        lib.write_json(out_root / "CONSUMER_MANIFEST.sha256",
                       {"sha256": lib.sha_file(out_root / "CONSUMER_MANIFEST.json")})

    print(json.dumps({"run_id": run_id, "consumed": consumed, "validation_ok": validation_ok,
                      "failure_code": receipt["failure_code"], "cli_executed": cli.get("executed"),
                      "checks": len(v.checks),
                      "failed": [c["id"] for c in v.checks if not c["ok"]][:6]},
                     ensure_ascii=False, indent=2))
    if a.expect_reject:
        return 0 if not consumed else 3
    return 0 if consumed else 3


if __name__ == "__main__":
    sys.exit(main())
