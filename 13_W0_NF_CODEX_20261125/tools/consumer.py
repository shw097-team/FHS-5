#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Named W1 consumer readback: verifies pack, handoff pins, evidence and
candidate by re-running a POS/NEG pair; refuses a wrong pin."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.ROOT / "07_CONSUMER"


def pin_from(text: str, key: str) -> str | None:
    text = text.replace("**", "")
    m = re.search(rf"{key}\s*[:：=]\s*`?([0-9a-f]{{64}}|`?[0-9a-f]{{40}})", text)
    return m.group(1).strip("`") if m else None


def verify(pack: Path, repo: Path, handoff: Path | None, evidence_manifest: Path | None) -> dict:
    repo = Path(repo).resolve()
    manifest = lib.load_json(pack / "05_W0_SOURCE_MANIFEST.json")
    files_ok = all(lib.sha_file(pack / e["path"]) == e["sha256"] for e in manifest["pack_files"])
    pack_sha = lib.sha_file(pack / "05_W0_SOURCE_MANIFEST.json")
    cand = lib.run(["git", "-C", str(repo), "rev-parse", "HEAD"], lib.ROOT)["stdout"].strip()
    h = {"handoff_present": bool(handoff and handoff.is_file())}
    if h["handoff_present"]:
        text = handoff.read_text(encoding="utf-8")
        h["pack_manifest_sha256"] = pin_from(text, "pack_manifest_sha256")
        h["candidate"] = pin_from(text, "candidate_commit") or pin_from(text, "candidate_ref")
        h["evidence"] = pin_from(text, "evidence_manifest_sha256") or pin_from(text, "evidence_ref")
        h["pins_ok"] = (h["pack_manifest_sha256"] == pack_sha
                        and h["candidate"] == cand
                        and (h["evidence"] or "") == (lib.sha_file(evidence_manifest) if evidence_manifest else ""))
    root = OUT / "tmp" / "root"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for p in (repo / "fixtures").glob("*.md"):
        shutil.copy2(p, root / p.name)
    pos = lib.cli(["--root", str(root), "--input", "case_ok.md",
                   "--sha256", lib.sha_file(root / "case_ok.md")], root,
                  env_extra={"PYTHONPATH": str(repo)}, raw_dir=OUT / "raw", tag="consumer_pos")
    neg = lib.cli(["--root", str(root), "--input", "case_missing.md",
                   "--sha256", lib.sha_file(root / "case_missing.md")], root,
                  env_extra={"PYTHONPATH": str(repo)}, raw_dir=OUT / "raw", tag="consumer_neg")
    runs_ok = (pos["exit"] == 0 and json.loads(pos["stdout"])["status"] == "COMPLETE"
               and neg["exit"] == 2 and json.loads(neg["stdout"])["status"] == "MISSING")
    return {"files_ok": files_ok, "pack_manifest_sha256": pack_sha, "candidate": cand,
            "handoff": h, "pos_neg_ok": runs_ok,
            "accepted": files_ok and runs_ok and h.get("pins_ok", False)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=str(lib.PACK))
    ap.add_argument("--repo", default=str(lib.REPO))
    ap.add_argument("--handoff")
    ap.add_argument("--evidence-manifest", default=str(lib.ROOT / "10_EVIDENCE" / "EVIDENCE_MANIFEST.json"))
    ap.add_argument("--out", default=str(OUT / "consumer_receipt.json"))
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    handoff = Path(a.handoff) if a.handoff else None
    ev = Path(a.evidence_manifest) if Path(a.evidence_manifest).is_file() else None
    good = verify(Path(a.pack), Path(a.repo), handoff, ev)
    bad_handoff = OUT / "tmp" / "handoff_wrong_pin.md"
    bad_handoff.parent.mkdir(parents=True, exist_ok=True)
    if handoff and handoff.is_file():
        bad_handoff.write_text(handoff.read_text(encoding="utf-8").replace(
            good["pack_manifest_sha256"], "0" * 64), encoding="utf-8")
        bad = verify(Path(a.pack), Path(a.repo), bad_handoff, ev)
        wrong_refused = not bad["accepted"]
    else:
        wrong_refused = None
    receipt = {
        "schema": "FHS5.W0NF.ConsumerReceipt@2",
        "consumer_id": "W1-consumer/CODEX-Native-1 (separate process)",
        "pack": str(Path(a.pack)),
        "handoff": str(handoff) if handoff else None,
        "evidence_manifest": str(ev) if ev else None,
        "good": good,
        "wrong_pin_refused": wrong_refused,
        "consumed": bool(good["accepted"] and (wrong_refused is not False)),
        "actual_action": "re-read pack manifest+files, handoff pins, evidence manifest; re-ran POS/NEG",
        "not_claimed": ["HERMES/GPT host execution", "W1 product execution", "release"],
    }
    lib.write_json(Path(a.out), receipt)
    raw_files = {}
    raw_dir = OUT / "raw"
    if raw_dir.is_dir():
        raw_files = {p.name: lib.sha_file(p) for p in sorted(raw_dir.glob("*")) if p.is_file()}
    consumer_manifest = {
        "schema": "FHS5.W0NF.ConsumerManifest@1",
        "consumer_receipt": str(Path(a.out).resolve()),
        "consumer_receipt_sha256": lib.sha_file(Path(a.out)),
        "evidence_manifest": str(ev) if ev else None,
        "evidence_manifest_sha256": lib.sha_file(ev) if ev else None,
        "pack_manifest_sha256": good["pack_manifest_sha256"],
        "candidate": good["candidate"],
        "consumed": receipt["consumed"],
        "wrong_pin_refused": wrong_refused,
        "raw": raw_files,
    }
    cm_path = OUT / "CONSUMER_MANIFEST.json"
    lib.write_json(cm_path, consumer_manifest)
    lib.write_json(OUT / "CONSUMER_MANIFEST.sha256", {"sha256": lib.sha_file(cm_path)})
    print(json.dumps({"consumed": receipt["consumed"], "pins_ok": good["handoff"].get("pins_ok"),
                      "files_ok": good["files_ok"], "pos_neg_ok": good["pos_neg_ok"],
                      "wrong_pin_refused": wrong_refused,
                      "consumer_manifest_sha256": lib.sha_file(cm_path)},
                     ensure_ascii=False, indent=2))
    return 0 if receipt["consumed"] else 3


if __name__ == "__main__":
    sys.exit(main())
