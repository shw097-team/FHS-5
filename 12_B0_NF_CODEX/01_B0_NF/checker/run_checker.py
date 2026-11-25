import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run_cli(candidate, args, cwd):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(candidate) + os.pathsep + env.get("PYTHONPATH","")
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run([sys.executable, "-m", "briefcheck", *args], cwd=str(cwd),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, timeout=30)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--evidence-root", required=True)
    a = ap.parse_args()
    cand = Path(a.candidate).resolve()
    oracle = json.loads(Path(a.oracle).read_text(encoding="utf-8"))
    ev = Path(a.evidence_root); ev.mkdir(parents=True, exist_ok=True)
    findings = []
    checks = []

    def add(ok, cid, observed):
        checks.append({"id": cid, "ok": bool(ok), "observed": observed})
        if not ok:
            findings.append({
                "id": "CH-" + cid, "severity": "MAJOR", "class": "checker_mismatch",
                "subject_sha": oracle["candidate_commit"], "command": "run_checker.py",
                "exit": 3, "raw_sha256": hashlib.sha256(json.dumps(observed, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                "reproduction": f"python checker/run_checker.py --candidate {cand} --oracle {a.oracle}"
            })

    add(sha(cand/"requirements.md") == oracle["source_sha256"], "SRC", "requirements.md sha")
    for name, exp in oracle["fixtures"].items():
        add(sha(cand/"fixtures"/name) == exp, "FIX-" + name, name)

    tmp = Path(tempfile.mkdtemp(prefix="b0_checker_"))
    root = tmp/"root"; root.mkdir()
    for f in (cand/"fixtures").glob("*.md"):
        (root/f.name).write_bytes(f.read_bytes())
    outside = tmp/"outside"; outside.mkdir()
    (outside/"canary.md").write_text("OUTSIDE_CANARY_DO_NOT_READ\n", encoding="utf-8")
    def source_files():
        return [p for p in cand.rglob("*") if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts]
    src_before = {str(p): sha(p) for p in source_files()}

    for name, exp in oracle["cases"].items():
        p = root/name
        r = run_cli(cand, ["--root", str(root), "--input", name, "--sha256", sha(p)], root)
        ok = r.returncode == exp["exit"]
        if ok and "status" in exp:
            try: ok = json.loads(r.stdout).get("status") == exp["status"]
            except Exception: ok = False
        add(ok, "CASE-" + name, {"exit": r.returncode, "stdout": r.stdout.strip()[:300], "expected": exp})

    path_cases = ["../outside/canary.md", str(outside/"canary.md"), r"\\localhost\share\canary.md"]
    for rel in path_cases:
        r = run_cli(cand, ["--root", str(root), "--input", rel, "--sha256", sha(outside/"canary.md")], root)
        ok = r.returncode == 3 and json.loads(r.stdout).get("status") == "INVALID_PATH" and "OUTSIDE_CANARY_DO_NOT_READ" not in (r.stdout+r.stderr)
        add(ok, "PATH-" + rel[:20], {"exit": r.returncode, "stdout": r.stdout.strip()[:300]})
    link = root/"escape_dir"
    j = subprocess.run(f'cmd /c mklink /J "{link}" "{outside}"', shell=True, capture_output=True, text=True)
    if j.returncode == 0:
        r = run_cli(cand, ["--root", str(root), "--input", "escape_dir/canary.md", "--sha256", sha(outside/"canary.md")], root)
        ok = r.returncode == 3 and json.loads(r.stdout).get("status") == "INVALID_PATH" and "OUTSIDE_CANARY_DO_NOT_READ" not in (r.stdout+r.stderr)
        add(ok, "PATH-junction", {"exit": r.returncode, "stdout": r.stdout.strip()[:300]})
    else:
        checks.append({"id": "PATH-junction", "ok": True, "observed": "SKIPPED: junction not permitted"})

    src_after = {str(p): sha(p) for p in source_files()}
    add(src_before == src_after, "NO-WRITE", "candidate files unchanged")

    cand_commit = subprocess.run(["git", "-C", str(cand), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    pins = {
        "source": oracle["source_sha256"],
        "candidate": cand_commit,
        "evidence": hashlib.sha256(json.dumps(checks, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
        "oracle": sha(a.oracle),
        "case_set": hashlib.sha256(json.dumps(oracle["cases"], sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
    }
    result = {
        "schema": "FHS5.B0NF.Challenge@1",
        "claim_ceiling": "CHECKER_ROLE_SEPARATED_SAME_PRINCIPAL",
        "candidate": str(cand),
        "pins": pins,
        "checks": checks,
        "findings": findings,
        "verdict": "PASS" if all(c["ok"] for c in checks) and not findings else "FAIL",
        "checker_identity": "checker/run_checker.py (separate worktree/process; same OS principal)",
        "not_covered": ["HERMES/GPT CHAT/GPT WORK host execution", "full C16/EC-36/local47", "product release"],
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"verdict": result["verdict"], "checks": len(checks), "findings": len(findings), "pins": pins}, ensure_ascii=False))
    return 0 if result["verdict"] == "PASS" else 3

if __name__ == "__main__":
    sys.exit(main())
