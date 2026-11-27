#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Frozen pre-patch Challenge: reproduce the v2 invalid-root defect in an
isolated clone and emit an eight-field Finding that FAR can consume."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import tqaep_spec

OUT = lib.PARTIES / "challenge"
WT = lib.TMP / "prepatch_v2"
PRE = "5eab43de2d3f67d6afbb1c5f6bc390e2c391da36"


def probe(repo: Path, tag: str):
    missing = WT.parent / "does_not_exist_root"
    return lib.run([sys.executable, "-m", "briefcheck", "--root", str(missing),
                    "--input", "case_ok.md", "--sha256", "0" * 64], repo,
                   env_extra={"PYTHONPATH": str(repo)}, raw_dir=OUT / "prepatch_raw", tag=tag)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if WT.exists():
        shutil.rmtree(WT, ignore_errors=True)
    clone = lib.run(["git", "clone", "--no-hardlinks", "--quiet", str(lib.REPO), str(WT)], lib.ROOT,
                    raw_dir=OUT / "prepatch_raw", tag="prepatch_clone")
    co = lib.run(["git", "-C", str(WT), "checkout", "--quiet", PRE], lib.ROOT,
                 raw_dir=OUT / "prepatch_raw", tag="prepatch_checkout")
    v2 = lib.run([sys.executable, "-m", "briefcheck", "--root", str(WT / "no_root"),
                  "--input", "case_ok.md", "--sha256", "0" * 64], WT,
                 env_extra={"PYTHONPATH": str(WT)}, raw_dir=OUT / "prepatch_raw", tag="prepatch_probe")
    v3 = lib.run([sys.executable, "-m", "briefcheck", "--root", str(lib.REPO / "no_root"),
                  "--input", "case_ok.md", "--sha256", "0" * 64], lib.REPO,
                 env_extra={"PYTHONPATH": str(lib.REPO)}, raw_dir=OUT / "prepatch_raw", tag="postpatch_probe")
    err = (OUT / "prepatch_raw" / "prepatch_probe.stderr.txt").read_bytes()
    finding = {
        "id": "CH-F-W0NF-001",
        "severity": "MAJOR",
        "class": "fail_open_invalid_root",
        "subject_sha": PRE,
        "command": ("python -m briefcheck --root <missing> --input case_ok.md "
                    "--sha256 " + "0" * 64),
        "exit": v2["exit"],
        "raw_sha256": lib.sha_bytes(err),
        "reproduction": ("Clone candidate at 5eab43d and run briefcheck with a missing --root; "
                         "it raises FileNotFoundError and exits 1 instead of INVALID_PATH/3."),
    }
    confirmed = (v2["exit"] == 1 and b"FileNotFoundError" in err and v3["exit"] == 3)
    out = {
        "schema": "FHS5.W0NF.ChallengePrepatch@1",
        "claim_ceiling": "CHECKER_ROLE_SEPARATED_SAME_PRINCIPAL",
        "clone_exit": clone["exit"], "checkout_exit": co["exit"], "checkout": PRE,
        "finding": finding,
        "v2_exit": v2["exit"], "v2_stderr_sha": lib.sha_bytes(err),
        "v3_exit": v3["exit"], "v3_stdout_sha": v3["stdout_sha256"],
        "raw": {"stderr": "03_PARTIES/challenge/prepatch_raw/prepatch_probe.stderr.txt"},
        "verdict": "FINDING_CONFIRMED" if confirmed else "FINDING_UNCONFIRMED",
    }
    lib.write_json(OUT / "challenge_prepatch.json", out)
    print(json.dumps({"confirmed": confirmed, "v2_exit": v2["exit"], "v3_exit": v3["exit"],
                      "finding": finding["id"], "raw_sha": finding["raw_sha256"]},
                     ensure_ascii=False, indent=2))
    return 0 if confirmed else 3


if __name__ == "__main__":
    sys.exit(main())
