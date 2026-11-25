import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run(args, cwd, env=None):
    e = os.environ.copy()
    if env: e.update(env)
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=e, timeout=60)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    ev = {"schema": "FHS5.B0NF.OPS@1", "host": {}, "steps": []}

    for cmd in (["codex", "--version"], ["python", "--version"], ["git", "--version"]):
        r = run(cmd, repo)
        ev["host"][cmd[0]] = {"exit": r.returncode, "stdout": (r.stdout+r.stderr).strip()[:300]}

    root = out/"root"; root.mkdir(exist_ok=True)
    import shutil
    for f in (repo/"fixtures").glob("*.md"):
        shutil.copy2(f, root/f.name)
    env = {"PYTHONPATH": str(repo), "PYTHONIOENCODING": "utf-8"}

    src = root/"case_ok.md"; src_before = sha(src)
    o2 = run([sys.executable, "-m", "briefcheck", "--root", str(root), "--input", "case_ok.md", "--sha256", sha(src)], repo, env)
    ev["steps"].append({"id":"O2-POS","exit":o2.returncode,"stdout":o2.stdout.strip(),"stderr":o2.stderr.strip()[:200]})
    o2n = run([sys.executable, "-m", "briefcheck", "--root", str(root), "--input", "case_missing.md", "--sha256", sha(root/"case_missing.md")], repo, env)
    ev["steps"].append({"id":"O2-NEG","exit":o2n.returncode,"stdout":o2n.stdout.strip(),"stderr":o2n.stderr.strip()[:200]})

    outfile = out/"result.json"
    before_absent = not outfile.exists()
    outfile.write_text(o2.stdout, encoding="utf-8")
    after_sha = sha(outfile)
    ev["steps"].append({"id":"O3-OUTPUT","before_absent":before_absent,"after_sha":after_sha,"source_unchanged":sha(src)==src_before,"json_parse":json.loads(outfile.read_text(encoding="utf-8")).get("status")})

    outfile.unlink()
    ev["steps"].append({"id":"O4-RESTORE","absent":not outfile.exists(),"source_unchanged":sha(src)==src_before})

    code = "import sys;sys.path.insert(0,%r);import briefcheck;bad=[m for m in sys.modules if m.split('.')[0].lower() in {'hgk','fabric','sbl','fhs','pipd'}];print(','.join(bad) or 'NONE')" % str(repo)
    off = run([sys.executable, "-c", code], repo)
    ev["steps"].append({"id":"O5-PROVIDER-OFF","exit":off.returncode,"imported_providers":off.stdout.strip()})

    # O6 is run separately by consumer_readback.py; record the handoff pointer.
    ev["steps"].append({"id":"O6-CONSUMER","pointer":"evidence/consumer/consumer_receipt.json","state":"READY_AFTER_EVIDENCE"})
    (out/"ops.json").write_text(json.dumps(ev, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    ok = all(s.get("exit",0) in (0,2,3) for s in ev["steps"]) and ev["steps"][2]["json_parse"] == "COMPLETE"
    print(json.dumps({"ok": ok, "steps": len(ev["steps"]), "out": str(out/"ops.json")}, ensure_ascii=False))
    return 0 if ok else 3

if __name__ == "__main__":
    sys.exit(main())
