#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the briefcheck path-security suite on a POSIX host with real symlinks.
Copies the candidate to a private temp dir; never touches the source."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    src = Path(a.repo)
    tmp = Path(tempfile.mkdtemp(prefix="w0nf_symlink_"))
    repo = tmp / "repo"
    shutil.copytree(src, repo, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    root = tmp / "root"
    outside = tmp / "outside"
    root.mkdir()
    outside.mkdir()
    for p in (repo / "fixtures").glob("*.md"):
        shutil.copy2(p, root / p.name)
    canary = outside / "canary.md"
    canary.write_text("OUTSIDE_CANARY_DO_NOT_READ\n", encoding="utf-8")
    canary_sha = sha(canary)

    (root / "escape_file").symlink_to(canary)
    (root / "escape_dir").symlink_to(outside, target_is_directory=True)
    (root / "rel_link").symlink_to("../outside/canary.md")
    (root / "inside_link").symlink_to(root / "case_ok.md")

    def run(inp: str, expected_sha: str):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(repo)
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        p = subprocess.run([sys.executable, "-m", "briefcheck", "--root", str(root),
                            "--input", inp, "--sha256", expected_sha],
                           cwd=str(root), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=30)
        try:
            payload = json.loads(p.stdout)
        except Exception:
            payload = {}
        return {"input": inp, "exit": p.returncode, "status": payload.get("status"),
                "stdout_sha": hashlib.sha256(p.stdout.encode()).hexdigest(),
                "stderr_sha": hashlib.sha256(p.stderr.encode()).hexdigest(),
                "leak": "OUTSIDE_CANARY_DO_NOT_READ" in (p.stdout + p.stderr)}

    ok_sha = sha(root / "case_ok.md")
    results = []
    results.append(run("case_ok.md", ok_sha))
    results.append(run("inside_link", ok_sha))
    for inp in ("../outside/canary.md", str(canary), r"\\localhost\share\canary.md",
                "escape_file", "escape_dir/canary.md", "rel_link"):
        results.append(run(inp, canary_sha))

    canary_after = sha(canary)
    source_after = sha(root / "case_ok.md")
    shell = "shell" not in platform.python_implementation().lower()
    verdict = (
        results[0]["exit"] == 0 and results[0]["status"] == "COMPLETE"
        and results[1]["exit"] == 0 and results[1]["status"] == "COMPLETE"
        and all(r["exit"] == 3 and r["status"] == "INVALID_PATH" and not r["leak"]
                for r in results[2:])
        and canary_after == canary_sha and source_after == ok_sha
    )
    out = {
        "schema": "FHS5.W0NF.SecurityPosix@1",
        "host": {
            "system": platform.system(), "release": platform.release(),
            "python": platform.python_version(), "uid": os.getuid(),
            "cwd_fs": os.stat(tmp).st_dev,
            "note": "WSL2 ext4 temp root; real POSIX symlinks; no privilege change",
        },
        "symlink_supported": True,
        "cases": results,
        "canary_sha_before": canary_sha,
        "canary_sha_after": canary_after,
        "source_sha_before": ok_sha,
        "source_sha_after": source_after,
        "positive_control_inside_link": results[1]["exit"] == 0,
        "verdict": "PASS" if verdict else "FAIL",
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps({"verdict": out["verdict"], "cases": len(results),
                      "host": out["host"]}, ensure_ascii=False))
    return 0 if verdict else 3


if __name__ == "__main__":
    sys.exit(main())
