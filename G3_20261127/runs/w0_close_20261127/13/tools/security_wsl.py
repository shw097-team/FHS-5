#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drive the POSIX symlink security suite through WSL Ubuntu (existing host)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.PARTIES / "security"


def wsl_path(p: Path) -> str:
    s = str(p.resolve())
    if len(s) > 2 and s[1] == ":":
        return "/mnt/" + s[0].lower() + s[2:].replace("\\", "/")
    return s.replace("\\", "/")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    distro = subprocess.run(["wsl.exe", "-l", "-q"], capture_output=True, text=True)
    names = [x.strip().replace("\x00", "") for x in distro.stdout.splitlines() if x.strip()]
    if not names:
        lib.write_json(OUT / "security_wsl.json", {
            "schema": "FHS5.W0NF.SecurityWsl@1", "verdict": "NOT_VERIFIED",
            "reason": "WSL_UNAVAILABLE", "symlink_supported": False,
        })
        print("NOT_VERIFIED: WSL unavailable")
        return 3
    out_path = OUT / "security_wsl.json"
    raw_dir = OUT / "raw"
    raw_dir.mkdir(exist_ok=True)
    cmd = ["wsl.exe", "-e", "python3", wsl_path(lib.ROOT / "tools" / "security_linux.py"),
           "--repo", wsl_path(lib.REPO), "--out", wsl_path(out_path)]
    r = lib.run(cmd, lib.ROOT, timeout=180, raw_dir=raw_dir, tag="security_wsl")
    result = {}
    if out_path.is_file():
        result = json.loads(out_path.read_text(encoding="utf-8"))
    else:
        lib.write_json(out_path, {
            "schema": "FHS5.W0NF.SecurityWsl@1", "verdict": "NOT_VERIFIED",
            "reason": "POSIX_RUNNER_FAILED", "exit": r["exit"],
            "stderr": r["stderr"][-800:], "symlink_supported": False,
        })
        result = json.loads(out_path.read_text(encoding="utf-8"))
    print(json.dumps({"wsl": names, "exit": r["exit"], "verdict": result.get("verdict")},
                     ensure_ascii=False))
    return 0 if result.get("verdict") == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
