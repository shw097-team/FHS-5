#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Four controlled UNKNOWN scenarios with real processes, real state and a
WorldRaw classification.  Every scenario runs in its own isolated directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PY = sys.executable


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tree(root: Path):
    if not root.exists():
        return "ABSENT"
    rows = [f"{p.relative_to(root).as_posix()}|{sha(p.read_bytes())}"
            for p in sorted(root.rglob("*")) if p.is_file()]
    return sha("\n".join(rows).encode())


WORKER = r'''
import sys, time
from pathlib import Path
kind = sys.argv[1]
root = Path(sys.argv[2])
if kind == "to_before":
    time.sleep(5)
elif kind == "to_after":
    (root / "world.txt").write_text("POST\n", encoding="utf-8")
    time.sleep(5)
elif kind == "partial":
    (root / "a.txt").write_text("POST-A\n", encoding="utf-8")
    time.sleep(5)
elif kind == "exit0_wrong":
    (root / "world.txt").write_text("WRONG\n", encoding="utf-8")
    sys.exit(0)
'''


def scenario(base: Path, name: str, kind: str) -> dict:
    d = base / name
    if d.exists():
        shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    (d / "world.txt").write_text("PRE\n", encoding="utf-8")
    if kind == "partial":
        (d / "b.txt").write_text("PRE-B\n", encoding="utf-8")
    worker = base / "worker.py"
    worker.write_text(WORKER, encoding="utf-8", newline="\n")
    pre_files = {p.name: p.read_bytes() for p in d.glob("*") if p.is_file()}
    pre = tree(d)
    argv = [PY, str(worker), kind, str(d)]
    timed_out = False
    stdout = stderr = ""
    exit_code = None
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=1,
                           errors="replace")
        exit_code = p.returncode
        stdout, stderr = p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
    post = tree(d)
    files = {p.name: p.read_text(encoding="utf-8").strip()
             for p in d.glob("*.txt")}
    # Classification is derived from observed state only, never from `kind`.
    if post == pre:
        cls = "TO_BEFORE" if timed_out else "MIXED"
    elif files.get("world.txt") == "POST":
        cls = "TO_AFTER"
    elif files.get("a.txt") == "POST-A" and files.get("b.txt") == "PRE-B":
        cls = "PARTIAL"
    elif exit_code == 0 and files.get("world.txt") not in (None, "POST"):
        cls = "EXIT0_WRONG"
    else:
        cls = "UNKNOWN"
    decision = {"TO_BEFORE": "RETRY_ALLOWED_ONCE",
                "TO_AFTER": "RECONCILE_VERIFIED_NO_RETRY",
                "PARTIAL": "COMPENSATE_OR_STOP",
                "EXIT0_WRONG": "EFFECT_NOT_VERIFIED"}.get(cls, "STOP_SCOPED")
    # compensation: restore the saved preimage, delete files that did not exist
    for name, data in pre_files.items():
        (d / name).write_bytes(data)
    for p in list(d.glob("*")):
        if p.is_file() and p.name not in pre_files:
            p.unlink()
    comp = tree(d)
    restored = comp == pre
    return {"scenario": kind, "argv": argv, "exit": exit_code,
            "timed_out": timed_out,
            "stdout_sha256": sha(stdout.encode()),
            "stderr_sha256": sha(stderr.encode()),
            "pre_world": pre, "post_world": post, "files": files,
            "class": cls, "decision": decision,
            "compensation": {"kind": "RESTORE_PREIMAGE_OR_DELETE_CREATED",
                             "ok": restored, "digest": comp},
            "verdict": "PASS" if cls != "UNKNOWN" and restored else "FAIL"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    base = Path(a.out).resolve()
    if base.exists():
        shutil.rmtree(base, ignore_errors=True)
    base.mkdir(parents=True)
    rows = [scenario(base, "F-TO-BEFORE", "to_before"),
            scenario(base, "F-TO-AFTER", "to_after"),
            scenario(base, "F-PARTIAL", "partial"),
            scenario(base, "F-EXIT0-WRONG", "exit0_wrong")]
    doc = {"schema": "FHS5.PLP.W2.UnknownFour@1",
           "rows": rows,
           "classes": {r["scenario"]: r["class"] for r in rows},
           "verdict": "PASS" if all(r["verdict"] == "PASS" for r in rows) else "FAIL",
           "note": "real subprocess timeouts/partial/exit0; WorldRaw pre/post; compensation readback"}
    (base / "UNKNOWN_FOUR.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": doc["verdict"], "classes": doc["classes"]}))
    return 0 if doc["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
