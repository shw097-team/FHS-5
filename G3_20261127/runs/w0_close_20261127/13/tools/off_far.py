#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3: FAR OFF. Apply the real 12' diff to an isolated v2 clone and run the
affected probe + full suite without invoking any FAR tool."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.ROOT / "04_DEV_OPS"
WT = lib.TMP / "off_far_v2"
PATCH = OUT / "patch_12prime.diff"


def main():
    raw = OUT / "raw"
    if WT.exists():
        shutil.rmtree(WT, ignore_errors=True)
    clone = lib.run(["git", "clone", "--no-hardlinks", "--quiet", str(lib.REPO), str(WT)], lib.ROOT,
                    raw_dir=raw, tag="off_far_clone")
    co = lib.run(["git", "-C", str(WT), "checkout", "--quiet", "5eab43d"], lib.ROOT,
                 raw_dir=raw, tag="off_far_checkout")
    pre = lib.sha_file(WT / "briefcheck.py")
    normalized = WT.parent / "patch_12prime_lf.diff"
    raw_text = PATCH.read_text(encoding="utf-8")
    normalized.write_text(raw_text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    patch = lib.run(["git", "-C", str(WT), "apply", "--whitespace=nowarn", str(normalized)], lib.ROOT,
                    raw_dir=raw, tag="off_far_apply")
    post = lib.sha_file(WT / "briefcheck.py")
    v3 = lib.sha_file(lib.REPO / "briefcheck.py")
    suite = lib.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], WT,
                    env_extra={"PYTHONPATH": str(WT)}, raw_dir=raw, tag="off_far_suite")
    probe = lib.run([sys.executable, "-c",
                     "import subprocess,sys,json,os;"
                     "p=subprocess.run([sys.executable,'-m','briefcheck','--root',"
                     "os.path.join(os.environ['TMP_OFF'],'nope'),'--input','case_ok.md',"
                     "'--sha256','0'*64],capture_output=True,text=True,"
                     "env=dict(os.environ,PYTHONPATH=os.getcwd()));"
                     "print(json.dumps({'exit':p.returncode,'out':p.stdout.strip()}));"
                     "sys.exit(0 if p.returncode==3 else 1)"],
                    WT, env_extra={"PYTHONPATH": str(WT), "TMP_OFF": str(WT)},
                    raw_dir=raw, tag="off_far_probe")
    verdict = ("PASS" if (clone["exit"] == 0 and co["exit"] == 0 and patch["exit"] == 0
                          and post == v3 and suite["exit"] == 0 and probe["exit"] == 0) else "FAIL")
    out = {
        "schema": "FHS5.W0NF.OffFar@1",
        "clone_exit": clone["exit"], "checkout_exit": co["exit"],
        "pre_sha": pre, "post_sha": post, "v3_sha": v3,
        "patch_exit": patch["exit"], "suite_exit": suite["exit"], "probe_exit": probe["exit"],
        "patch_source_sha": lib.sha_file(PATCH),
        "patch_applied_sha": lib.sha_file(normalized),
        "patch_normalization": "CRLF->LF only; content unchanged",
        "far_tool_invoked": False,
        "verdict": verdict,
        "not_covered": ["Fabric three-source profile", "FARP30/local35"],
    }
    lib.write_json(OUT / "off_far.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
