#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real DEV driver: imports the world's gate/admission and performs one op."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", required=True)
    ap.add_argument("--ws", required=True)
    ap.add_argument("--patch")
    ap.add_argument("--out", required=True)
    ap.add_argument("--caller-head", default=None)
    ap.add_argument("--stale-preimage", action="store_true")
    a = ap.parse_args(argv)
    world = Path(a.world).resolve()
    sys.path.insert(0, str(world / "W1" / "check"))
    import w2_admission as A  # noqa: E402
    import w2_dev_gate as G  # noqa: E402

    ws = json.loads(Path(a.ws).read_text(encoding="utf-8"))
    if a.stale_preimage:
        ws = [dict(e) for e in ws]
        ws[0]["preimage_sha256"] = "0" * 64
    A.WRITE_ROOT = str(world)
    A.ALLOWED_OPS = tuple((e["path"], e["operation"].upper()) for e in ws)
    head = subprocess.run(["git", "-C", str(world), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    out = {"argv": sys.argv, "cwd": str(Path.cwd()), "live_head": head,
           "write_set": ws}
    try:
        rec = A.derive("DEV", "W2-NF-01", world, ws)
        out["admission"] = {"ok": True, "decision_id": rec["decision_id"],
                            "subject_sha256": rec["subject_sha256"],
                            "verified_from": rec["verified_from"]}
        asserted = {"effect": "REPOSITORY_WRITE", "scope": "W2-NF-01",
                    "head": a.caller_head or head, "admission": rec,
                    "recovery": {"kind": "REVERSE_PATCH_ON_COPY"}}
        chk = G.check(asserted, world, ws)
        out["check"] = chk
        if a.patch:
            patch = Path(a.patch).read_text(encoding="utf-8")
            app = G.apply_patch(asserted, world, ws, patch)
            out["apply"] = app
            out["post"] = {e["path"]: (sha(world / e["path"])
                                       if (world / e["path"]).is_file() else None)
                           for e in ws}
            st = subprocess.run(["git", "-C", str(world), "status", "--porcelain=v2",
                                 "--untracked-files=all"], capture_output=True, text=True)
            out["status_porcelain"] = st.stdout
            df = subprocess.run(["git", "-C", str(world), "diff", "--stat"],
                                capture_output=True, text=True)
            out["diff_stat"] = df.stdout
        out["exit"] = 0
    except Exception as exc:  # noqa: BLE001
        out["error"] = {"type": type(exc).__name__,
                        "token": getattr(exc, "token", None),
                        "detail": str(exc)[:400]}
        out["exit"] = 2
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"exit": out["exit"],
                      "check": (out.get("check") or {}).get("ok"),
                      "first_fail": (out.get("check") or {}).get("first_fail")
                      or (out.get("apply") or {}).get("first_fail")}))
    return out["exit"]


if __name__ == "__main__":
    sys.exit(main())
