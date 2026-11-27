#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical W1 minimal consume: fresh clone/process POS and typed NEGs."""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W = Path(__file__).resolve().parent
BASE = ROOT.parent
TOOL = ROOT / "tools" / "w1_min_consume.py"
HANDOFF = ROOT / "09_DELIVERY" / "W0_HANDOFF.md"
REPO = W / "w1_candidate"

def run(handoff: Path, out_root: Path, scope="W0", repo=None):
    if out_root.exists():
        shutil.rmtree(out_root)
    p = subprocess.run([sys.executable, "-B", str(TOOL), "--handoff", str(handoff),
                        "--root", str(ROOT), "--repo", str(repo or REPO),
                        "--out-root", str(out_root), "--scope", scope],
                       capture_output=True, text=True, timeout=180)
    try:
        payload = json.loads(p.stdout)
    except Exception:
        payload = {"raw": p.stdout[-2000:]}
    return {"exit": p.returncode, "payload": payload, "stderr": p.stderr[-1000:]}

def main():
    if not REPO.is_dir():
        p = subprocess.run(["git", "-c", "core.fscache=false", "clone", "--quiet",
                            str(ROOT / "02_CANDIDATE" / "repo.bundle"), str(REPO)],
                           capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            raise SystemExit("clone failed: " + p.stderr)
        p = subprocess.run(["git", "-c", "core.fscache=false", "-C", str(REPO),
                            "checkout", "--quiet", "bb66a276aae8c5d6aef549832c523587fc47d247"],
                           capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            raise SystemExit("checkout failed: " + p.stderr)
    pos = run(HANDOFF, BASE / "w1_out_pos")
    cj = BASE / "w1_out_pos" / "w1_checklist.json"
    items = 0
    readback = False
    if cj.is_file():
        cl = json.loads(cj.read_text(encoding="utf-8"))
        items = len(cl.get("items") or [])
        readback = bool(cl.get("readback_ok") or (cl.get("readback") or {}).get("ok"))
    pos_ok = (pos["exit"] == 0 and pos["payload"].get("status") == "W1_CHECKLIST_READY"
              and pos["payload"].get("readback_ok") is True and items == 44 and cj.is_file())
    (W / "w1_pos.json").write_text(json.dumps({**pos, "items": items,
                                               "checklist": str(cj),
                                               "verdict": "PASS" if pos_ok else "FAIL"},
                                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # wrong pin
    hp = W / "handoff_wrong_pin.md"
    t = HANDOFF.read_text(encoding="utf-8").replace(
        "112f2902656f1122720ef275ac954e3422f896267f144f27d321fa138be382c6", "0" * 64)
    hp.write_text(t, encoding="utf-8", newline="\n")
    pin = run(hp, BASE / "w1_out_neg_pin")
    pin_ok = pin["exit"] == 3 and pin["payload"].get("code") == "PIN_MISMATCH_ORACLE"
    (W / "w1_neg_pin.json").write_text(json.dumps({**pin, "verdict": "PASS" if pin_ok else "FAIL"},
                                                  ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # wrong scope
    scope = run(HANDOFF, BASE / "w1_out_neg_scope", scope="W1")
    scope_ok = scope["exit"] == 3 and scope["payload"].get("code") == "SCOPE_MISMATCH"
    (W / "w1_neg_scope.json").write_text(json.dumps({**scope, "verdict": "PASS" if scope_ok else "FAIL"},
                                                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # partial handoff: remove a required section
    hp2 = W / "handoff_partial.md"
    lines = HANDOFF.read_text(encoding="utf-8").splitlines()
    out = []
    skip = False
    for line in lines:
        if line.startswith("## not_covered"):
            skip = True
            continue
        if skip and line.startswith("## "):
            skip = False
        if not skip:
            out.append(line)
    hp2.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    partial = run(hp2, BASE / "w1_out_neg_partial")
    partial_ok = partial["exit"] == 3 and partial["payload"].get("code") == "HANDOFF_INCOMPLETE"
    (W / "w1_neg_partial.json").write_text(json.dumps({**partial, "verdict": "PASS" if partial_ok else "FAIL"},
                                                      ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    overall = pos_ok and pin_ok and scope_ok and partial_ok
    summary = {"schema": "FHS5.W1.MinimalConsumeSuite@1",
               "pos": pos_ok, "wrong_pin": pin_ok, "wrong_scope": scope_ok,
               "partial_handoff": partial_ok, "items": items,
               "checklist": str(cj), "verdict": "PASS" if overall else "FAIL"}
    (W / "w1_suite.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if overall else 3

if __name__ == "__main__":
    sys.exit(main())