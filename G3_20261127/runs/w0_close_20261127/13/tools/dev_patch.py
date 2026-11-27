#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real red -> patch -> retest on the briefcheck candidate (v2 -> v3).

Red: an invalid/missing --root produces a traceback (exit 1) instead of the
contract's INVALID_PATH (exit 3). The probe is frozen before the patch.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.ROOT / "04_DEV_OPS"
PROBE = OUT / "probe"

PROBE_SRC = '''import hashlib, json, os, subprocess, sys, unittest
from pathlib import Path

REPO = Path(os.environ["BRIEFCHECK_REPO"])

def run(root, inp="case_ok.md"):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run([sys.executable, "-m", "briefcheck", "--root", root,
                           "--input", inp, "--sha256", "0"*64],
                          cwd=str(REPO), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env, timeout=30)

class InvalidRoot(unittest.TestCase):
    def test_missing_root_is_invalid_path(self):
        p = run(str(REPO.parent / "does_not_exist_root"))
        self.assertEqual(p.returncode, 3, p.stderr[-500:])
        self.assertEqual(json.loads(p.stdout)["status"], "INVALID_PATH")

    def test_root_file_is_invalid_path(self):
        p = run(str(REPO / "requirements.md"))
        self.assertEqual(p.returncode, 3, p.stderr[-500:])
        self.assertEqual(json.loads(p.stdout)["status"], "INVALID_PATH")

if __name__ == "__main__":
    unittest.main()
'''

PATCH = r'''#!/usr/bin/env python3
"""briefcheck B0 candidate v3: fail closed on invalid roots; stable JSON."""
import argparse, hashlib, json, os, sys
from pathlib import Path

def emit(code, status, sha256=None, provided=None, missing=None):
    print(json.dumps({"source_sha256": sha256, "provided": provided or [], "missing": missing or [], "status": status},
                     ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return code

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--sha256", required=True)
    a = p.parse_args(argv)
    try:
        root = Path(a.root).resolve(strict=True)
    except OSError:
        return emit(3, "INVALID_PATH")
    if not root.is_dir():
        return emit(3, "INVALID_PATH")
    rel = a.input
    if not rel or os.path.isabs(rel) or rel.startswith("\\\\") or ":" in rel:
        return emit(3, "INVALID_PATH")
    if any(part == ".." for part in Path(rel).parts):
        return emit(3, "INVALID_PATH")
    try:
        target = (root / rel).resolve(strict=True)
    except OSError:
        return emit(3, "INVALID_PATH")
    try:
        if os.path.normcase(os.path.commonpath([str(root), str(target)])) != os.path.normcase(str(root)):
            return emit(3, "INVALID_PATH")
    except ValueError:
        return emit(3, "INVALID_PATH")
    if not target.is_file():
        return emit(3, "INVALID_PATH")
    data = target.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != a.sha256.lower():
        return emit(3, "SHA_MISMATCH", actual)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return emit(3, "INVALID_ENCODING", actual)
    checked = set(); seen = {"A": 0, "B": 0}; malformed = False
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if not s.startswith("- ["):
            continue
        if len(s) == 7 and s[0:3] == "- [" and s[3] in " xX" and s[4] == "]" and s[5] == " " and s[6] in "AB":
            seen[s[6]] += 1
            if s[3].lower() == "x":
                checked.add(s[6])
        else:
            malformed = True
    if malformed:
        return emit(3, "INVALID_FORMAT", actual, sorted(checked))
    if seen["A"] > 1:
        return emit(3, "INVALID_DUP", actual, sorted(checked))
    if seen["B"] > 1:
        return emit(3, "INVALID_FORMAT", actual, sorted(checked))
    missing = [x for x in ("A", "B") if x not in checked]
    if missing:
        return emit(2, "MISSING", actual, sorted(checked), missing)
    return emit(0, "COMPLETE", actual, sorted(checked), [])

if __name__ == "__main__":
    sys.exit(main())
'''

NEW_TESTS = '''
    def test_r11_missing_root(self):
        p = run_cli(["--root", str(Path(self.tmp) / "nope"), "--input", "case_ok.md", "--sha256", "0"*64], self.root)
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(jout(p)["status"], "INVALID_PATH")

    def test_r12_root_is_file(self):
        p = run_cli(["--root", str(REPO / "requirements.md"), "--input", "case_ok.md", "--sha256", "0"*64], self.root)
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(jout(p)["status"], "INVALID_PATH")
'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROBE.mkdir(parents=True, exist_ok=True)
    (PROBE / "test_invalid_root.py").write_text(PROBE_SRC, encoding="utf-8")
    head = lib.git("rev-parse", "HEAD")
    pre = {
        "head": head,
        "briefcheck.py": lib.sha_file(lib.REPO / "briefcheck.py"),
        "tests/test_briefcheck.py": lib.sha_file(lib.REPO / "tests" / "test_briefcheck.py"),
    }
    # 1. frozen red on the unpatched candidate
    red = lib.run([sys.executable, "-m", "unittest", "discover", "-s", str(PROBE), "-v"],
                  lib.REPO, env_extra={"BRIEFCHECK_REPO": str(lib.REPO), "PYTHONPATH": str(lib.REPO)},
                  raw_dir=OUT / "raw", tag="red_v2")
    (OUT / "red_v2.txt").write_text(red["stdout"] + "\n--- stderr ---\n" + red["stderr"], encoding="utf-8")
    # 2. patch
    (lib.REPO / "briefcheck.py").write_text(PATCH, encoding="utf-8", newline="\n")
    tests = (lib.REPO / "tests" / "test_briefcheck.py").read_text(encoding="utf-8")
    if "test_r11_missing_root" not in tests:
        marker = 'if __name__ == "__main__":'
        tests = tests.replace(marker, NEW_TESTS + "\n" + marker)
        (lib.REPO / "tests" / "test_briefcheck.py").write_text(tests, encoding="utf-8", newline="\n")
    diff = lib.run(["git", "-C", str(lib.REPO), "diff", "--", "briefcheck.py", "tests/test_briefcheck.py"],
                   lib.ROOT)["stdout"]
    (OUT / "patch_12prime.diff").write_text(diff, encoding="utf-8")
    # 3. retest: probe + full suite
    green_probe = lib.run([sys.executable, "-m", "unittest", "discover", "-s", str(PROBE), "-v"],
                          lib.REPO, env_extra={"BRIEFCHECK_REPO": str(lib.REPO), "PYTHONPATH": str(lib.REPO)},
                          raw_dir=OUT / "raw", tag="green_v3_probe")
    green = lib.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                    lib.REPO, env_extra={"PYTHONPATH": str(lib.REPO)},
                    raw_dir=OUT / "raw", tag="green_v3")
    (OUT / "green_v3.txt").write_text(green["stdout"] + "\n--- stderr ---\n" + green["stderr"], encoding="utf-8")
    # 4. commit v3
    lib.run(["git", "-C", str(lib.REPO), "add", "briefcheck.py", "tests/test_briefcheck.py"], lib.ROOT)
    commit = lib.run(["git", "-C", str(lib.REPO), "-c", "user.name=CODEX W0", "-c", "user.email=codex-w0@local",
                      "commit", "-m", "candidate v3 (12'): invalid root fails closed as INVALID_PATH"], lib.ROOT)
    lib.run(["git", "-C", str(lib.REPO), "tag", "-f", "w0-candidate-v3"], lib.ROOT)
    post_head = lib.git("rev-parse", "HEAD")
    evidence = {
        "schema": "FHS5.W0NF.DevPatch@1",
        "preimage": pre,
        "red": {"exit": red["exit"], "stdout_sha": red["stdout_sha256"], "first_fail": "INVALID_ROOT_TRACEBACK",
                "raw": "04_DEV_OPS/raw/red_v2.*"},
        "patch": {"path": "04_DEV_OPS/patch_12prime.diff", "sha256": lib.sha_file(OUT / "patch_12prime.diff")},
        "retest": {"probe_exit": green_probe["exit"], "suite_exit": green["exit"],
                   "suite_stdout_sha": green["stdout_sha256"]},
        "commit": {"exit": commit["exit"], "head": post_head,
                   "subject": "candidate v3 (12'): invalid root fails closed as INVALID_PATH"},
        "write_set": ["briefcheck.py", "tests/test_briefcheck.py"],
        "verdict": "PASS" if red["exit"] != 0 and green_probe["exit"] == 0 and green["exit"] == 0 else "FAIL",
    }
    lib.write_json(OUT / "dev_patch.json", evidence)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if evidence["verdict"] == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
