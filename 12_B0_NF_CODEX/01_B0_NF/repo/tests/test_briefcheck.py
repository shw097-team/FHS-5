import os, sys, json, hashlib, subprocess, tempfile, unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIX = REPO / "fixtures"

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run_cli(args, cwd, timeout=30):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO) + os.pathsep + env.get("PYTHONPATH","")
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run([sys.executable, "-m", "briefcheck", *args],
                          cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env, timeout=timeout)

def jout(p):
    return json.loads(p.stdout)

class BriefcheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="briefcheck_test_")
        cls.root = Path(cls.tmp) / "root"
        cls.root.mkdir()
        for f in FIX.glob("*.md"):
            (cls.root / f.name).write_bytes(f.read_bytes())
        cls.outside = Path(cls.tmp) / "outside"
        cls.outside.mkdir()
        (cls.outside / "canary.md").write_text("OUTSIDE_CANARY_DO_NOT_READ\n", encoding="utf-8")

    def cli(self, name, sha_override=None):
        p = self.root / name
        exp = sha_override if sha_override is not None else sha(p)
        return run_cli(["--root", str(self.root), "--input", name, "--sha256", exp], self.root)

    def test_r1_ok(self):
        p = self.cli("case_ok.md")
        self.assertEqual(p.returncode, 0, p.stderr)
        d = jout(p)
        self.assertEqual(d["status"], "COMPLETE")
        self.assertEqual(d["provided"], ["A", "B"])
        self.assertEqual(d["missing"], [])

    def test_r2_missing_b(self):
        p = self.cli("case_missing.md")
        self.assertEqual(p.returncode, 2, p.stderr)
        d = jout(p)
        self.assertEqual(d["status"], "MISSING")
        self.assertEqual(d["missing"], ["B"])

    def test_r3_duplicate_a(self):
        p = self.cli("case_dup.md")
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(jout(p)["status"], "INVALID_DUP")

    def test_r4_path_escape(self):
        cases = [
            "../outside/canary.md",
            str(self.outside / "canary.md"),
            r"\\localhost\share\canary.md",
        ]
        for rel in cases:
            p = run_cli(["--root", str(self.root), "--input", rel, "--sha256", sha(self.outside/"canary.md")], self.root)
            self.assertEqual(p.returncode, 3, (rel, p.stdout, p.stderr))
            self.assertEqual(jout(p)["status"], "INVALID_PATH", (rel, p.stdout))
            self.assertNotIn("OUTSIDE_CANARY_DO_NOT_READ", p.stdout + p.stderr)
        link = self.root / "escape_dir"
        if not link.exists():
            r = subprocess.run(f'cmd /c mklink /J "{link}" "{self.outside}"', shell=True, capture_output=True, text=True)
            if r.returncode != 0:
                self.skipTest("junction creation not permitted: " + r.stderr)
        p = run_cli(["--root", str(self.root), "--input", "escape_dir/canary.md", "--sha256", sha(self.outside/"canary.md")], self.root)
        self.assertEqual(p.returncode, 3, (p.stdout, p.stderr))
        self.assertEqual(jout(p)["status"], "INVALID_PATH")
        self.assertNotIn("OUTSIDE_CANARY_DO_NOT_READ", p.stdout + p.stderr)

    def test_r5_bad_utf8(self):
        p = self.cli("case_bad_utf8.md")
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(jout(p)["status"], "INVALID_ENCODING")

    def test_r6_hash_mismatch(self):
        p = self.cli("case_ok.md", sha_override="0"*64)
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(jout(p)["status"], "SHA_MISMATCH")

    def test_r7_ambiguous(self):
        p = self.cli("case_ambiguous.md")
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(jout(p)["status"], "INVALID_FORMAT")

    def test_r8_malformed(self):
        p = self.cli("case_malformed.md")
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(jout(p)["status"], "INVALID_FORMAT")

    def test_r9_stable(self):
        a = self.cli("case_ok.md"); b = self.cli("case_ok.md")
        self.assertEqual(a.returncode, 0); self.assertEqual(b.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)

    def test_r10_reversible_output(self):
        src = self.root / "case_ok.md"
        before = sha(src)
        out = Path(self.tmp) / "result.json"
        p = self.cli("case_ok.md")
        self.assertEqual(p.returncode, 0)
        out.write_text(p.stdout, encoding="utf-8")
        self.assertTrue(out.exists())
        self.assertEqual(sha(src), before)
        out.unlink()
        self.assertFalse(out.exists())

if __name__ == "__main__":
    unittest.main()
