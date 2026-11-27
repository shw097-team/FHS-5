import hashlib, json, os, subprocess, sys, unittest
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
