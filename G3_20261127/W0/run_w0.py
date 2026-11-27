#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W0 G3 execution: ten SAMPLE cases, the 44-receipt reuse ledger, a cold OFF
run with a positive control, and the W0 summary.

Every observation is produced by a real subprocess.  The runner never edits the
pack, the fixtures or the oracle.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
sys.path.insert(0, str(G3 / "lib"))
import g3pack  # noqa: E402

PY = sys.executable
FORBIDDEN = ("hgk", "fabric", "sbl", "fhs", "pipd", "hermes", "far", "bridge", "guide")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha(p.read_bytes())


def run(argv, cwd, env=None, timeout=60):
    t0 = time.time()
    p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                       errors="replace", timeout=timeout, env=env)
    return {"argv": argv, "cwd": str(cwd), "exit": p.returncode,
            "stdout": p.stdout, "stderr": p.stderr,
            "stdout_sha256": sha(p.stdout.encode("utf-8")),
            "stderr_sha256": sha(p.stderr.encode("utf-8")),
            "elapsed_ms": int((time.time() - t0) * 1000)}


def parse_stdout(rec):
    for line in reversed((rec.get("stdout") or "").strip().splitlines()):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8", newline="\n")


def build_cli(pack: g3pack.Pack, run_root: Path) -> Path:
    src = Path(r"C:\Users\user\Downloads\FHS-5\FHS-5_PLP_W0-W4_執行控制小包"
               r"\FHS-5_PLP_W0-W2_執行控制包_FINAL\03_TOOLS\briefcheck_min.py")
    if not src.is_file():
        raise SystemExit("briefcheck_min.py not found at " + str(src))
    dst = run_root / "cli" / "briefcheck.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def stage_root(pack: g3pack.Pack, run_root: Path) -> Path:
    root = run_root / "world" / "root"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for name in ("case_ok.md", "case_missing.md", "case_dup.md",
                 "case_bad_path.md", "case_bad_utf8.md", "case_ambiguous.md",
                 "case_malformed.md"):
        shutil.copy2(pack.root / "assets" / "fixtures" / name, root / name)
    return root


def case_record(pack, oracle, cid, cli, root, extra=None):
    spec = next(c for c in oracle["cases"] if c["case_id"] == cid)
    argv = [PY, str(cli), *spec["argv"]]
    before = {p.name: sha_file(p) for p in root.iterdir() if p.is_file()}
    rec = run(argv, root)
    after = {p.name: sha_file(p) for p in root.iterdir() if p.is_file()}
    out = parse_stdout(rec)
    exp = spec["expect"]
    observed = {"exit": rec["exit"], "status": (out or {}).get("status")}
    if out and "missing" in out:
        observed["missing"] = out["missing"]
    verdict, first = "FAIL", None
    if rec["exit"] != exp["exit"]:
        first = f"EXIT:{rec['exit']}!={exp['exit']}"
    elif observed["status"] != exp["status"]:
        first = f"STATUS:{observed['status']}!={exp['status']}"
    else:
        verdict = "PASS"
    if cid == "SAMPLE-R9":
        again = run([PY, str(cli), "--root", str(root), "--input", "case_ok.md"], root)
        if again["stdout"] != rec["stdout"] or again["exit"] != 0:
            verdict, first = "FAIL", "UNSTABLE"
        rec["second_invocation"] = {"argv": again["argv"], "exit": again["exit"],
                                    "stdout": again["stdout"],
                                    "stdout_sha256": again["stdout_sha256"]}
    if cid == "SAMPLE-R1" and out and sorted(out.get("provided") or []) != ["A", "B"]:
        verdict, first = "FAIL", "PROVIDED"
    if cid == "SAMPLE-R2" and out and (out.get("missing") or []) != ["B"]:
        verdict, first = "FAIL", "MISSING_CHILD"
    if cid == "SAMPLE-R4":
        leak = "OUTSIDE_CANARY_DO_NOT_READ" in rec["stdout"] + rec["stderr"]
        if leak:
            verdict, first = "FAIL", "CANARY_READ"
    rec.update({"run_id": f"W0-{cid}-{time.strftime('%Y%m%dT%H%M%S')}",
                "case_id": cid, "kind": spec["kind"],
                "candidate": pack.candidate, "source_manifest_sha256": pack.sha256,
                "fixture": spec["fixture"], "oracle": "assets/oracles/W0_SAMPLE_ORACLE.json",
                "expected": exp, "observed": observed, "verdict": verdict,
                "first_fail": first, "pre_sha": before, "post_sha": after,
                "source_unchanged": before == after, "parsed": out})
    if extra:
        rec.update(extra)
    return rec


def path_variants(pack, cli, run_root, root):
    outside = run_root / "world" / "outside"
    outside.mkdir(parents=True, exist_ok=True)
    canary = outside / "canary.md"
    canary.write_text("OUTSIDE_CANARY_DO_NOT_READ\n", encoding="utf-8")
    junction = root / "escape_dir"
    if junction.exists():
        junction.unlink()
    made = []
    try:
        subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(outside)],
                       capture_output=True, check=True)
        made.append("junction")
    except Exception:
        pass
    variants = [
        ("dotdot", ["../outside/canary.md"]),
        ("absolute", [str(canary)]),
        ("unc", [r"\\localhost\share\canary.md"]),
    ]
    if "junction" in made:
        variants.append(("junction", ["escape_dir/canary.md"]))
    rows = []
    canary_pre = sha_file(canary)
    for name, inputs in variants:
        for rel in inputs:
            rec = run([PY, str(cli), "--root", str(root), "--input", rel], root)
            out = parse_stdout(rec) or {}
            leak = "OUTSIDE_CANARY_DO_NOT_READ" in rec["stdout"] + rec["stderr"]
            ok = rec["exit"] == 3 and out.get("status") == "INVALID_PATH" and not leak
            rows.append({"variant": name, "input": rel, "exit": rec["exit"],
                         "status": out.get("status"), "canary_leak": leak,
                         "verdict": "PASS" if ok else "FAIL",
                         "argv": rec["argv"], "stdout": rec["stdout"],
                         "stderr": rec["stderr"]})
    canary_post = sha_file(canary)
    if junction.exists():
        subprocess.run(["cmd", "/c", "rmdir", str(junction)], capture_output=True)
    return {"variants": rows, "canary_sha_before": canary_pre,
            "canary_sha_after": canary_post,
            "junction_created": "junction" in made,
            "verdict": "PASS" if all(r["verdict"] == "PASS" for r in rows)
                       and canary_pre == canary_post else "FAIL"}


def output_wrapper(pack, cli, root):
    out_rel = "out/result.json"
    out = root / out_rel
    if out.exists():
        out.unlink()
    src = root / "case_ok.md"
    pre = sha_file(src)
    rec = run([PY, str(cli), "--root", str(root), "--input", "case_ok.md",
               "--output", out_rel], root)
    exists = out.is_file()
    body = out.read_text(encoding="utf-8") if exists else None
    post = sha_file(src)
    parsed = json.loads(body) if body else None
    ok = (rec["exit"] == 0 and exists and parsed and parsed.get("status") == "COMPLETE"
          and pre == post)
    del_ok = False
    if exists:
        out.unlink()
        del_ok = not out.exists()
    return {"argv": rec["argv"], "exit": rec["exit"], "output": out_rel,
            "output_created": exists, "output_sha256": sha(body.encode()) if body else None,
            "source_sha_before": pre, "source_sha_after": post,
            "deleted_to_absent": del_ok, "parsed": parsed,
            "verdict": "PASS" if ok and del_ok else "FAIL"}


def receipts_ledger():
    base = G3.parent / "13_W0_NF_CODEX_20261125" / "05_TQAEP" / "receipts"
    rows = []
    for p in sorted(base.glob("*.json")):
        raw = p.read_bytes()
        try:
            doc = json.loads(raw.decode("utf-8"))
            keys = ("run_id", "case_id", "exit", "verdict", "expected", "observed")
            missing = [k for k in keys if k not in doc]
        except Exception as exc:  # noqa: BLE001
            doc, missing = None, [str(exc)]
        rows.append({"file": p.name, "bytes": len(raw), "sha256": sha(raw),
                     "case_id": (doc or {}).get("case_id"),
                     "verdict": (doc or {}).get("verdict"),
                     "missing_keys": missing,
                     "state": "REUSE_VERIFIED" if not missing else "REJECTED"})
    cohorts = {"original": 0, "NF": 0, "SAMPLE": 0}
    for r in rows:
        cid = r.get("case_id") or ""
        if cid.startswith("F5-W0-T"):
            cohorts["original"] += 1
        elif cid.startswith("NF-T"):
            cohorts["NF"] += 1
        else:
            cohorts["SAMPLE"] += 1
    return {"root": str(base), "count": len(rows), "cohorts": cohorts,
            "all_verified": all(r["state"] == "REUSE_VERIFIED" for r in rows),
            "rows": rows}


def off_run(pack, cli, run_root):
    iso = run_root / "off"
    iso.mkdir(parents=True, exist_ok=True)
    log = iso / "blocked.log"
    wrapper = iso / "off_wrapper.py"
    wrapper.write_text(
        "import sys, runpy, importlib.abc, importlib.machinery, os\n"
        f"FORBIDDEN = {FORBIDDEN!r}\n"
        "LOG = os.environ['OFF_LOG']\n"
        "class Blocker(importlib.abc.MetaPathFinder):\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        top = name.split('.')[0]\n"
        "        if top in FORBIDDEN:\n"
        "            open(LOG, 'a', encoding='utf-8').write(name + '\\n')\n"
        "            raise ImportError('BLOCKED_IMPORT:' + name)\n"
        "        return None\n"
        "sys.meta_path.insert(0, Blocker())\n"
        "target = sys.argv[1]\n"
        "if target == '-c':\n"
        "    exec(compile(sys.argv[2], '<off-control>', 'exec'), {'__name__': '__main__'})\n"
        "else:\n"
        "    sys.argv = sys.argv[1:]\n"
        "    runpy.run_path(target, run_name='__main__')\n",
        encoding="utf-8", newline="\n")
    env = dict(os.environ, OFF_LOG=str(log), PYTHONIOENCODING="utf-8")
    if log.exists():
        log.unlink()
    (iso / "case_ok.md").write_text("- [x] A\n- [x] B\n", encoding="utf-8")
    pos = run([PY, str(wrapper), "-c",
               "import importlib; importlib.import_module('fabric')"], iso, env)
    control_blocked = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
    if log.exists():
        log.unlink()
    neg2 = run([PY, str(wrapper), str(cli), "--root", str(iso), "--input", "case_ok.md"], iso, env)
    blocked = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
    ok = (pos["exit"] != 0 and "BLOCKED_IMPORT" in pos["stderr"]
          and neg2["exit"] == 0 and "BLOCKED_IMPORT" not in neg2["stderr"])
    return {"positive_control": {"exit": pos["exit"], "stderr": pos["stderr"],
                                 "verdict": "PASS" if pos["exit"] != 0 else "FAIL"},
            "off_run": {"exit": neg2["exit"], "stdout": neg2["stdout"],
                        "verdict": "PASS" if neg2["exit"] == 0 else "FAIL"},
            "blocked_imports": blocked,
            "positive_control_blocked": control_blocked,
            "forbidden_imports_zero": len(blocked) == 0,
            "verdict": "PASS" if ok and not blocked else "FAIL",
            "note": "cold subprocess; provider modules blocked by meta_path; positive control proves the blocker fires"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    run_root = Path(a.out).resolve()
    if run_root.exists():
        shutil.rmtree(run_root)
    run_root.mkdir(parents=True)
    v = g3pack.verify_pack(a.pack)
    if not v["ok"]:
        print(json.dumps({"ok": False, "errors": v["errors"]}, ensure_ascii=False))
        return 1
    pack = v["pack"]
    cli = build_cli(pack, run_root)
    root = stage_root(pack, run_root)
    oracle = g3pack.strict_json((pack.root / "assets" / "oracles" /
                                 "W0_SAMPLE_ORACLE.json").read_bytes(), "oracle")
    rows = []
    for cid in [f"SAMPLE-R{i}" for i in range(1, 11)]:
        rec = case_record(pack, oracle, cid, cli, root)
        write(run_root / "raw" / f"{cid}.json", rec)
        rows.append({"case_id": cid, "verdict": rec["verdict"],
                     "exit": rec["exit"], "status": (rec.get("parsed") or {}).get("status"),
                     "first_fail": rec["first_fail"],
                     "raw": f"raw/{cid}.json"})
    variants = path_variants(pack, cli, run_root, root)
    write(run_root / "raw" / "R4-variants.json", variants)
    wrapper = output_wrapper(pack, cli, root)
    write(run_root / "raw" / "R10-output.json", wrapper)
    ledger = receipts_ledger()
    write(run_root / "raw" / "receipts-44.json", ledger)
    off = off_run(pack, cli, run_root)
    write(run_root / "raw" / "OFF.json", off)
    samples_pass = sum(1 for r in rows if r["verdict"] == "PASS")
    result = {
        "schema": "FHS5.PLP.G3.W0.Run@1",
        "run_id": f"W0-G3-{time.strftime('%Y%m%dT%H%M%S')}",
        "candidate": pack.candidate,
        "source_manifest_sha256": pack.sha256,
        "pack_tree_sha256": v["tree_sha256"],
        "case_set_sha256": v["case_set_sha256"],
        "samples": {"pass": samples_pass, "total": 10, "rows": rows},
        "r4_variants": variants["verdict"],
        "r10_output": wrapper["verdict"],
        "receipts_44": {"count": ledger["count"], "cohorts": ledger["cohorts"],
                        "all_verified": ledger["all_verified"]},
        "off": off["verdict"],
        "verdict": "PASS" if (samples_pass == 10 and variants["verdict"] == "PASS"
                              and wrapper["verdict"] == "PASS"
                              and ledger["all_verified"] and off["verdict"] == "PASS")
                   else "FAIL",
        "not_claimed": ["F5-W0-T01..T24 product rerun", "NF-T01..T10 product rerun",
                        "B0 product validation", "independent checker"],
    }
    write(run_root / "W0_RESULT.json", result)
    print(json.dumps({"ok": result["verdict"] == "PASS", "samples": f"{samples_pass}/10",
                      "r4": variants["verdict"], "r10": wrapper["verdict"],
                      "receipts": ledger["count"], "off": off["verdict"]}))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
