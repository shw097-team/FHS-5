#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Frozen probe: authority-injection via unlisted entry / reparse alias.

Frozen before the repair.  Same inputs, same oracle, run twice:
  pre-patch  expects accepted=True  (this is the RED observation)
  post-patch expects refused with UNLISTED_ENTRY / PATH_ESCAPE (GREEN)

Usage:  python probe_authority_injection.py <candidate_tree> <scratch_dir>
Prints one JSON object with per-probe result and the module digest actually
loaded, so the raw output can be sealed without re-deriving anything.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def make_delivery(root: Path, entries, extra: dict, pack_pin: str, schema: tuple):
    root.mkdir(parents=True, exist_ok=True)
    for rel, data in extra.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    manifest = {"schema": schema[0], "pack_manifest_sha256": pack_pin,
                "files": list(entries)}
    raw = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    (root / "EVIDENCE_MANIFEST.json").write_bytes(raw)
    seal = {"schema": schema[1], "evidence_manifest_sha256": sha_bytes(raw),
            "pack_manifest_sha256": pack_pin}
    seal_raw = json.dumps(seal, ensure_ascii=False).encode("utf-8")
    (root / "DELIVERY_SEAL.json").write_bytes(seal_raw)
    return {"evidence_manifest_sha256": sha_bytes(raw),
            "delivery_seal_sha256": sha_bytes(seal_raw),
            "pack_manifest_sha256": pack_pin}


def make_junction(link: Path, target: Path):
    try:
        os.symlink(target, link, target_is_directory=True)
        return "symlink"
    except OSError:
        pass
    res = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("no reparse capability: " + res.stderr.strip())
    return "junction"


def main():
    tree = Path(sys.argv[1]).resolve()
    scratch = Path(sys.argv[2]).resolve()
    sys.path.insert(0, str(tree / "W1" / "check"))
    import w2_receiver as R

    schema = (R.SCHEMA_MANIFEST, R.SCHEMA_SEAL)
    out = {
        "schema": "FHS5.PLP.W2S3.Probe@1",
        "receiver_sha256": hashlib.sha256(
            Path(R.__file__).read_bytes()).hexdigest(),
        "oracle": {
            "unlisted_entry": "refuse:UNLISTED_ENTRY",
            "reparse_alias": "refuse:PATH_ESCAPE",
        },
        "probes": {},
    }

    base = Path(tempfile.mkdtemp(prefix="probe_", dir=str(scratch)))
    data = b"same bytes\n"

    # P1: an unlisted file inside an otherwise self-consistent delivery.
    r1 = base / "unlisted"
    pins1 = make_delivery(
        r1,
        [{"path": "evidence/ok.json", "sha256": sha_bytes(b"{}\n"), "bytes": 3}],
        {"evidence/ok.json": b"{}\n",
         "evidence/w2/material/injected.json": b"authority-injection\n"},
        R.PACK_PIN, schema)
    v1 = R.verify_delivery(r1, pins1)
    out["probes"]["unlisted_entry"] = {
        "accepted": bool(v1["ok"]), "first_fail": v1["first_fail"],
        "checks_failed": [c["name"] for c in v1["checks"] if not c["ok"]],
    }

    # P2: a junction inside the root aliasing a listed path (stays inside root).
    r2 = base / "reparse"
    (r2 / "store").mkdir(parents=True, exist_ok=True)
    (r2 / "store" / "ok.txt").write_bytes(data)
    kind = make_junction(r2 / "data", r2 / "store")
    pins2 = make_delivery(
        r2, [{"path": "data/ok.txt", "sha256": sha_bytes(data), "bytes": len(data)}],
        {}, R.PACK_PIN, schema)
    v2 = R.verify_delivery(r2, pins2)
    out["probes"]["reparse_alias"] = {
        "link_kind": kind, "accepted": bool(v2["ok"]),
        "first_fail": v2["first_fail"],
        "checks_failed": [c["name"] for c in v2["checks"] if not c["ok"]],
    }

    out["verdict"] = ("GREEN"
                      if (not out["probes"]["unlisted_entry"]["accepted"]
                          and not out["probes"]["reparse_alias"]["accepted"])
                      else "RED_ACCEPTED")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["verdict"] == "GREEN" else 3


if __name__ == "__main__":
    sys.exit(main())
