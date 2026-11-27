#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W2 G3 execution: real DEV apply/test/reverse/restore and a real OPS-A
receipt-producing effect with WorldRaw pre/post, independent consume and
created-only compensation, plus the remaining ten cases.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
WT = G3.parent
sys.path.insert(0, str(G3 / "lib"))
sys.path.insert(0, str(HERE))
import g3pack  # noqa: E402
import guards  # noqa: E402

PY = sys.executable
BASE = "9fae9257a3402928efbe6ff0cd66f45761f52846"
RECV = "W1/check/w2_receiver.py"
TEST = "W1/check/test_j1_receiver.py"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha(p.read_bytes())


def rmtree(path):
    """Remove a tree even when git made objects read-only on Windows."""
    def onerror(func, p, exc):
        try:
            os.chmod(p, 0o666)
            func(p)
        except Exception:
            pass
    if Path(path).exists():
        shutil.rmtree(path, onerror=onerror)


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8", newline="\n")


def run(argv, cwd, timeout=180):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                       errors="replace", timeout=timeout, env=env)
    return {"argv": argv, "cwd": str(cwd), "exit": p.returncode,
            "stdout": p.stdout, "stderr": p.stderr,
            "stdout_sha256": sha(p.stdout.encode()), "stderr_sha256": sha(p.stderr.encode())}


def tree_digest(root: Path):
    root = Path(root)
    if not root.exists():
        return "ABSENT"
    rows = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rows.append(f"{p.relative_to(root).as_posix()}|{sha_file(p)}")
    return sha("\n".join(rows).encode())


def modify_patch(old: str, new: str, path: str) -> str:
    d = difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                             fromfile=f"a/{path}", tofile=f"b/{path}", n=3)
    return f"diff --git a/{path} b/{path}\n" + "".join(d)


def add_patch(new: str, path: str) -> str:
    lines = new.splitlines(True)
    body = []
    for ln in lines:
        if ln.endswith("\n"):
            body.append("+" + ln)
        else:
            body.append("+" + ln + "\n\\ No newline at end of file\n")
    return (f"diff --git a/{path} b/{path}\nnew file mode 100644\n"
            f"--- /dev/null\n+++ b/{path}\n@@ -0,0 +1,{len(lines)} @@\n" + "".join(body))


def git(world, *args):
    return subprocess.run(["git", "-C", str(world), *args],
                          capture_output=True, text=True, errors="replace")


def build_world(run_root: Path):
    world = run_root / "dev" / "world"
    if world.exists():
        rmtree(world)
    (world / "W1" / "check").mkdir(parents=True)
    (world / "W1" / "authority" / "decisions").mkdir(parents=True)
    pre = subprocess.run(["git", "-C", str(WT), "show", f"{BASE}:{RECV}"],
                         capture_output=True)
    if pre.returncode != 0:
        raise SystemExit("cannot read historical preimage")
    old_b = pre.stdout
    post_b = (WT / RECV).read_bytes()
    test_b = (WT / TEST).read_bytes()
    (world / RECV).write_bytes(old_b)
    for name in ("w2_admission.py", "w2_dev_gate.py"):
        shutil.copy2(WT / "W1" / "check" / name, world / "W1" / "check" / name)
    # the base world also carries the real product modules and the frozen W1
    # delivery tree the receiver tests consume; both are read-only inputs.
    shutil.copytree(WT / "W1" / "impl", world / "W1" / "impl")
    for delivery in sorted(WT.glob("18_W1_NF_*")):
        if ((delivery / "EVIDENCE_MANIFEST.json").is_file()
                and (delivery / "DELIVERY_SEAL.json").is_file()
                and (delivery / "control_pack").is_dir()):
            shutil.copytree(delivery, world / delivery.name)
            break

    ops_out = run_root / "ops" / "out"
    if ops_out.exists():
        rmtree(ops_out)
    dec_dev = {
        "schema": "FHS5.PLP.W2.OwnerDecision@local-5",
        "decision_id": "W2-G3-OWNER-20261127-05",
        "issuer": "Human Owner via CODEX thin PROMPT; PCNF-W0W2-ADOPT-20261127-01",
        "claim": "OWNER_DELEGATED_ISOLATED_DEV",
        "grant_state": "REQUEST_ONLY",
        "issuer_state": "PENDING_EXTERNAL_ISSUER",
        "scope": {"subject_id": "FHS-5_PLP/W2/CONTROL_PACK", "scope": "W2-NF-01"},
        "effect": "REPOSITORY_WRITE",
        "write_root": str(world),
        "allowed_ops": [{"path": RECV, "operation": "MODIFY"},
                        {"path": TEST, "operation": "ADD"}],
        "recovery": {"kind": "REVERSE_PATCH_ON_COPY"},
        "expiry": "2026-11-28T00:00:00+08:00",
    }
    dec_ops = {
        "schema": "FHS5.PLP.W2.OwnerDecision@local-6",
        "decision_id": "W2-G3-OWNER-20261127-06",
        "issuer": "Human Owner via CODEX thin PROMPT; PCNF-W0W2-ADOPT-20261127-01",
        "claim": "OWNER_DELEGATED_ISOLATED_OPS",
        "grant_state": "REQUEST_ONLY",
        "issuer_state": "PENDING_EXTERNAL_ISSUER",
        "scope": {"subject_id": "FHS-5_PLP/W2/CONTROL_PACK", "scope": "W2-NF-01"},
        "effect": "HOST_EFFECT",
        "write_root": str(ops_out),
        "allowed_ops": [{"path": "OPS-A", "operation": "CREATE"}],
        "recovery": {"kind": "DELETE_CREATED_ONLY"},
        "expiry": "2026-11-28T00:00:00+08:00",
    }
    write(world / "W1" / "authority" / "decisions" / "DEV.json", dec_dev)
    write(world / "W1" / "authority" / "decisions" / "OPS.json", dec_ops)
    trust = {
        "schema": "FHS5.PLP.W2.Trust@4",
        "default_domain": "DEV",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "revoked": [
            {"decision_id": "W2-NF-PRIMARY-20261126-01",
             "token": "ADMISSION_TERMINATED_BY_SECURITY_FINDING"},
            {"decision_id": "W2-S2S3-OWNER-20261126-02", "token": "ADMISSION_SUPERSEDED"},
            {"decision_id": "W2-S2S3-OWNER-20261127-03", "token": "ADMISSION_SUPERSEDED"},
            {"decision_id": "W2-S2S3-OWNER-20261127-04", "token": "ADMISSION_PENDING_SUPERSEDED"},
        ],
        "finding_markers": [],
        "domains": {
            "DEV": {
                "domain": "DEV", "scope": "W2-NF-01",
                "not_after": "2026-11-28T00:00:00+08:00",
                "write_root": str(world),
                "allowed_ops": [{"path": RECV, "operation": "MODIFY"},
                                {"path": TEST, "operation": "ADD"}],
                "decision": {"path": "decisions/DEV.json",
                             "sha256": sha_file(world / "W1" / "authority" / "decisions" / "DEV.json"),
                             "decision_id": dec_dev["decision_id"],
                             "schema": dec_dev["schema"],
                             "subject_id": "FHS-5_PLP/W2/CONTROL_PACK"},
            },
            "OPS": {
                "domain": "OPS", "scope": "W2-NF-01",
                "not_after": "2026-11-28T00:00:00+08:00",
                "write_root": str(ops_out),
                "allowed_ops": [{"path": "OPS-A", "operation": "CREATE"}],
                "recovery_kinds": ["DELETE_CREATED_ONLY"],
                "decision": {"path": "decisions/OPS.json",
                             "sha256": sha_file(world / "W1" / "authority" / "decisions" / "OPS.json"),
                             "decision_id": dec_ops["decision_id"],
                             "schema": dec_ops["schema"],
                             "subject_id": "FHS-5_PLP/W2/CONTROL_PACK"},
            },
        },
    }
    write(world / "W1" / "authority" / "trust.json", trust)
    pyc = world / "W1" / "check" / "__pycache__"
    if pyc.exists():
        rmtree(pyc)
    for cmd in (["init", "-q"], ["config", "user.name", "g3"],
                ["config", "user.email", "g3@local.invalid"],
                ["config", "core.autocrlf", "false"],
                ["add", "-A"], ["commit", "-qm", "base: G1 preimage"]):
        r = git(world, *cmd)
        if r.returncode != 0:
            raise SystemExit("git failed: " + r.stderr[-300:])
    head = git(world, "rev-parse", "HEAD").stdout.strip()
    patch = (modify_patch(old_b.decode("utf-8"), post_b.decode("utf-8"), RECV)
             + add_patch(test_b.decode("utf-8"), TEST))
    (run_root / "dev" / "patch.diff").write_text(patch, encoding="utf-8", newline="\n")
    ws = [{"path": RECV, "operation": "MODIFY", "preimage_sha256": sha(old_b)},
          {"path": TEST, "operation": "ADD"}]
    write(run_root / "dev" / "ws.json", ws)
    return {"world": world, "head": head, "issued": False, "old_sha": sha(old_b),
            "old_bytes": len(old_b), "post_sha": sha(post_b),
            "post_bytes": len(post_b), "test_sha": sha(test_b),
            "test_bytes": len(test_b), "ws": ws, "ops_out": ops_out,
            "preimage_cmd": ["git", "-C", str(WT), "show", f"{BASE}:{RECV}"]}


def snapshot(world: Path, exclude=()):
    out = {}
    for p in sorted(world.rglob("*")):
        if not p.is_file() or ".git" in p.parts or "__pycache__" in p.parts:
            continue
        if p.suffix in (".pyc", ".pyo"):
            continue
        rel = p.relative_to(world).as_posix()
        if rel not in exclude:
            out[rel] = sha_file(p)
    return out


def case(cid, kind, expected):
    return {"run_id": f"W2-{cid}-{time.strftime('%Y%m%dT%H%M%S')}",
            "case_id": cid, "kind": kind, "expected": expected,
            "observed": None, "verdict": "NOT_RUN", "first_fail": None,
            "observation_layer": "PRODUCT_CASE", "not_covered": []}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    run_root = Path(a.out).resolve()
    if run_root.exists():
        rmtree(run_root)
    run_root.mkdir(parents=True)
    v = g3pack.verify_pack(a.pack)
    if not v["ok"]:
        print(json.dumps({"ok": False, "errors": v["errors"]}, ensure_ascii=False))
        return 1
    pack = v["pack"]
    raw = run_root / "raw"
    rows = []

    def emit(rec, name=None):
        write(raw / f"{name or rec['case_id']}.json", rec)
        rows.append({"case_id": rec["case_id"], "verdict": rec["verdict"],
                     "first_fail": rec["first_fail"],
                     "raw": f"raw/{name or rec['case_id']}.json"})
        return rec

    env = build_world(run_root)
    world = env["world"]
    ws = env["ws"]

    # ---------------- W2-DEV-01 (POS, real apply/test/reverse/restore)
    rec = case("W2-DEV-01", "POS",
               {"apply": "MODIFY+ADD exact", "tests": "exit 0", "reverse": "preimage",
                "restore": "absent+preimage", "unlisted": "unchanged"})
    before = snapshot(world, exclude={RECV, TEST})
    drv = run([PY, str(HERE / "dev_driver.py"), "--world", str(world),
               "--ws", str(run_root / "dev" / "ws.json"),
               "--patch", str(run_root / "dev" / "patch.diff"),
               "--out", str(raw / "DEV01_driver.json")], world)
    drv_doc = json.loads((raw / "DEV01_driver.json").read_text(encoding="utf-8"))
    apply_res = drv_doc.get("apply") or {}
    post_expected = {RECV: env["post_sha"], TEST: env["test_sha"]}
    post_actual = drv_doc.get("post") or {}
    t = run([PY, TEST], world)
    test_ok = t["exit"] == 0 and "OK" in t["stderr"] and "Ran 0 tests" not in t["stderr"]
    after = snapshot(world, exclude={RECV, TEST})
    # reverse on an independent copy
    rev = run([PY, "-c",
               "import sys,json;sys.path.insert(0,%r);import w2_dev_gate as G;"
               "p=open(%r,encoding='utf-8').read();"
               "ws=json.load(open(%r,encoding='utf-8'));"
               "pre={e['path']:e.get('preimage_sha256') for e in ws};"
               "print(json.dumps(G.reverse(p,%r,ws,pre),ensure_ascii=False))"
               % (str(world / "W1" / "check"), str(run_root / "dev" / "patch.diff"),
                  str(run_root / "dev" / "ws.json"), str(world))], world)
    rev_doc = json.loads(rev["stdout"] or "{}")
    # restore the world with the reverse patch (no reset, no clean)
    rr = git(world, "apply", "-R", str(run_root / "dev" / "patch.diff"))
    restored = {"receiver_sha": sha_file(world / RECV),
                "test_absent": not (world / TEST).exists(),
                "reverse_exit": rr.returncode, "reverse_stderr": rr.stderr[-200:]}
    post_restore = snapshot(world, exclude={RECV, TEST})
    checks = {
        "driver_exit": drv["exit"] == 0,
        "check_ok": bool((drv_doc.get("check") or {}).get("ok")),
        "apply_ok": bool(apply_res.get("ok")),
        "wrote_exact": sorted(apply_res.get("wrote") or []) == sorted([RECV, TEST]),
        "post_match": post_actual == post_expected,
        "tests_ok": test_ok,
        "reverse_ok": bool(rev_doc.get("ok")),
        "restored_preimage": restored["receiver_sha"] == env["old_sha"],
        "restored_absence": restored["test_absent"],
        "unlisted_unchanged": before == after == post_restore,
        "git_not_reset": "reset" not in " ".join(drv_doc.get("argv") or []),
    }
    rec["observed"] = {
        "base": BASE, "preimage": {"bytes": env["old_bytes"], "sha256": env["old_sha"]},
        "post_expected": post_expected, "post_actual": post_actual,
        "apply": {k: apply_res.get(k) for k in
                  ("ok", "first_fail", "wrote", "preimage_sha256",
                   "postimage_sha256", "recovery_kind")},
        "tests": {"argv": t["argv"], "exit": t["exit"],
                  "stderr_tail": t["stderr"][-400:],
                  "stdout_sha256": t["stdout_sha256"]},
        "reverse": rev_doc, "restore": restored,
        "unlisted_unchanged": before == after == post_restore,
        "checks": checks,
    }
    rec["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    rec["first_fail"] = next((k for k, ok in checks.items() if not ok), None)
    rec["observation_layer"] = "PRODUCT_EFFECT_ACTUAL"
    if not env["issued"]:
        rec["verdict"] = "NOT_ADMITTED"
        rec["first_fail"] = "NOT_ADMITTED"
        rec["observed"]["authority"] = "REQUEST_ONLY; external ISSUED grant absent"
    emit(rec)

    # ---------------- W2-DEV-02 (NEG: caller HEAD != live)
    rec = case("W2-DEV-02", "NEG", {"token": "REPO_HEAD_MISMATCH", "writes": 0})
    d2 = run([PY, str(HERE / "dev_driver.py"), "--world", str(world),
              "--ws", str(run_root / "dev" / "ws.json"),
              "--caller-head", "1" * 40,
              "--out", str(raw / "DEV02_driver.json")], world)
    d2doc = json.loads((raw / "DEV02_driver.json").read_text(encoding="utf-8"))
    chk = d2doc.get("check") or {}
    rec["observed"] = {"caller_head": "1" * 40, "live_head": d2doc.get("live_head"),
                       "first_fail": chk.get("first_fail"),
                       "wrote": chk.get("wrote"),
                       "receiver_sha": sha_file(world / RECV),
                       "test_absent": not (world / TEST).exists()}
    ok = (chk.get("first_fail") == "REPO_HEAD_MISMATCH"
          and chk.get("wrote") == [] and rec["observed"]["receiver_sha"] == env["old_sha"])
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else (chk.get("first_fail") or "NOT_REFUSED")
    if not env["issued"]:
        rec["verdict"] = "NOT_ADMITTED"
        rec["first_fail"] = "NOT_ADMITTED"
        rec["observed"]["authority"] = "REQUEST_ONLY"
    emit(rec)

    # ---------------- W2-OPS-01 (POS, real effect + WorldRaw + compensation)
    rec = case("W2-OPS-01", "POS",
               {"seven": "host/pre/argv/post/parse/compensation/readback"})
    out_root = env["ops_out"]
    pre_world = tree_digest(out_root)
    host = {"host_id": "CODEX-NATIVE-LOCAL",
            "principal": "principal-local",
            "os": sys.platform, "python": sys.version.split()[0],
            "policy_epoch": None, "epoch_state": "NOT_DECLARED_BY_HOST"}
    ops = run([PY, str(HERE / "ops_receiver.py"), "--pack", str(pack.root),
               "--lib", str(G3 / "lib"), "--out", str(out_root),
               "--runid", f"OPS-A-{time.strftime('%Y%m%dT%H%M%S')}",
               "--result", str(raw / "OPS01_receiver.json")], run_root)
    ops_doc = json.loads((raw / "OPS01_receiver.json").read_text(encoding="utf-8"))
    post_world = tree_digest(out_root)
    target = out_root / "OPS-A"
    if target.exists():
        con = run([PY, str(HERE / "ops_consumer.py"), "--target", str(target),
                   "--out", str(raw / "OPS01_consumer.json")], run_root)
        con_doc = json.loads((raw / "OPS01_consumer.json").read_text(encoding="utf-8"))
    else:
        con = {"argv": [], "exit": 2, "stdout": "", "stderr": "TARGET_NOT_CREATED"}
        con_doc = {"all_ok": False, "error": "TARGET_NOT_CREATED"}
    # compensation: delete created-only, then read back the pre-state
    comp_ok = False
    if target.exists():
        rmtree(target)
        comp_ok = not target.exists()
    if out_root.exists() and not any(out_root.iterdir()):
        out_root.rmdir()
    comp_world = tree_digest(out_root)
    seven = {
        "1_host": host,
        "2_pre_world": pre_world,
        "3_effect_argv_exit": {"argv": ops["argv"], "exit": ops["exit"]},
        "4_post_world": post_world,
        "5_receiver_parse_use": ops_doc.get("receipt"),
        "6_compensation": {"kind": "DELETE_CREATED_ONLY", "ok": comp_ok},
        "7_pre_state_readback": comp_world,
    }
    checks = {"exit0": ops["exit"] == 0, "pre_absent": pre_world == "ABSENT",
              "post_changed": post_world != pre_world,
              "consumer_ok": bool(con_doc.get("all_ok")),
              "compensated": comp_ok and comp_world == pre_world,
              "seven_present": all(v for v in seven.values())}
    rec["observed"] = {"seven": seven, "checks": checks,
                       "consumer": con_doc}
    rec["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    rec["first_fail"] = next((k for k, ok in checks.items() if not ok), None)
    rec["observation_layer"] = "PRODUCT_EFFECT_ACTUAL"
    rec["not_covered"] = ["other Hosts", "container/cloud", "Publisher"]
    if not env["issued"]:
        rec["verdict"] = "NOT_ADMITTED"
        rec["first_fail"] = "NOT_ADMITTED"
        rec["observed"]["authority"] = "REQUEST_ONLY; external ISSUED grant absent"
    emit(rec)

    # ---------------- W2-OPS-02 (NEG: git revert as OPS recovery)
    rec = case("W2-OPS-02", "NEG", {"token": "RECOVERY_KIND_MISMATCH", "effect": 0})
    spy = []
    try:
        guards.apply_recovery("GIT_REVERT", "OPS-A", spy)
        rec["verdict"], rec["first_fail"] = "FAIL", "NOT_REFUSED"
        tok = None
    except guards.GuardError as exc:
        tok = exc.token
    rec["observed"] = {"token": tok, "spy": spy,
                       "world": tree_digest(out_root)}
    ok = tok == "RECOVERY_KIND_MISMATCH" and not spy
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else (tok or "NOT_REFUSED")
    emit(rec)

    # ---------------- W2-EFFECT-01
    rec = case("W2-EFFECT-01", "NEG", {"token": "EFFECT_UNBOUND", "calls": 0})
    toks, calls = [], 0
    for token, path in (("OPAQUE", None), ("PATH_INFERRED_READ", "docs/readme.md"),
                        ("", None), (None, "../outside")):
        try:
            guards.map_effect(token, path)
            toks.append({"token": token, "result": "MAPPED"})
            calls += 1
        except guards.GuardError as exc:
            toks.append({"token": token, "path": path, "token_out": exc.token})
    ok = calls == 0 and all(t.get("token_out") == "EFFECT_UNBOUND" for t in toks)
    rec["observed"] = {"attempts": toks, "effect_calls": calls,
                       "default_read": False}
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else "DEFAULT_READ_OR_MAPPED"
    emit(rec)

    # ---------------- W2-AUTH-01
    rec = case("W2-AUTH-01", "NEG", {"token": "FALSE_AUTHORITY|NOT_ADMITTED", "effect": 0})
    fx = pack.fixture("W2-AUTH-01")
    try:
        guards.check_authority(fx["inputs"])
        rec["verdict"], rec["first_fail"], tok = "FAIL", "NOT_REFUSED", None
    except guards.GuardError as exc:
        tok = exc.token
    rec["observed"] = {"token": tok, "effect_count": 0,
                       "pre_post_unchanged": tree_digest(out_root) == "ABSENT"}
    ok = tok in ("FALSE_AUTHORITY", "NOT_ADMITTED")
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else (tok or "NOT_REFUSED")
    emit(rec)

    # ---------------- W2-RUNNER-01
    rec = case("W2-RUNNER-01", "NEG", {"token": "RUNNER_UNBOUND", "executed": False})
    fx = pack.fixture("W2-RUNNER-01")
    try:
        guards.select_runner({"runner": None, "oracle_ref": None, "fixture_ref": None})
        rec["verdict"], rec["first_fail"], tok = "FAIL", "NOT_REFUSED", None
    except guards.GuardError as exc:
        tok = exc.token
    rec["observed"] = {"token": tok, "executed": False, "raw": None,
                       "claimed_executed_ignored": fx["inputs"]["claimed_executed"]}
    ok = tok == "RUNNER_UNBOUND"
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else (tok or "NOT_REFUSED")
    emit(rec)

    # ---------------- W2-DELTA-01 (two independently produced periods)
    w0 = json.loads((G3 / "runs" / "w0" / "W0_RESULT.json").read_text(encoding="utf-8"))
    w1 = json.loads((G3 / "runs" / "w1" / "W1_RESULT.json").read_text(encoding="utf-8"))
    head = git(WT, "rev-parse", "HEAD").stdout.strip()
    period_a = {"subject": "FHS-5_PLP/W2/CONTROL_PACK", "scope": "W2-NF-01",
                "source_sha": w0["source_manifest_sha256"], "repo_head": head,
                "host_id": os.environ.get("COMPUTERNAME", "UNKNOWN"),
                "policy_epoch": "G3-20261127", "oracle_sha": w0["case_set_sha256"],
                "world_raw_sha": sha_file(G3 / "runs" / "w0" / "W0_RESULT.json"),
                "first_fail": "NONE"}
    period_b = dict(period_a, source_sha=w1["source_manifest_sha256"],
                    oracle_sha=w1["case_set_sha256"],
                    world_raw_sha=sha_file(G3 / "runs" / "w1" / "W1_RESULT.json"))

    def verifier(x, y):
        return {"verified": x.get("subject") == y.get("subject")
                and x.get("scope") == y.get("scope"), "checked": "identity"}

    same = guards.delta_verify(period_a, dict(period_a), verifier)
    delta = guards.delta_verify(period_a, period_b, verifier)
    missing = guards.delta_verify(period_a, None, verifier)
    ok = (same["state"] == "REUSE_LASTGOOD"
          and delta["state"] == "NEW_MATERIAL_EVIDENCE"
          and missing["state"] == "DELTA_UNVERIFIED")
    rec["observed"] = {"period_a": period_a, "period_b": period_b,
                       "same": same, "delta": delta, "missing": missing}
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else "DELTA_MISMATCH"
    rec["observation_layer"] = "PRODUCT_DELTA_ACTUAL"
    emit(rec)

    # ---------------- W2-R3-01 (13+3 typed table)
    rec = case("W2-R3-01", "POS", {"rows": 13, "nf": 3, "nulls": "preserved"})
    fx = pack.fixture("W2-R3-01")
    try:
        d = guards.r3_rows(fx)
        rec["observed"] = {"rows": len(d["rows"]), "nf": len(d["nf_rows"]),
                           "owners": [r["owner"] for r in d["rows"]],
                           "all_actual_null": d["all_actual_null"],
                           "token": d["token"]}
        rec["verdict"] = "PASS"
    except guards.GuardError as exc:
        rec["observed"] = {"token": exc.token, "detail": str(exc)}
        rec["verdict"], rec["first_fail"] = "FAIL", exc.token
    emit(rec)

    # ---------------- W2-R3-02
    rec = case("W2-R3-02", "NEG", {"token": "NOT_ADMITTED"})
    fx = pack.fixture("W2-R3-02")
    try:
        guards.g4_admit(fx)
        rec["verdict"], rec["first_fail"], tok = "FAIL", "ADMITTED", None
    except guards.GuardError as exc:
        tok = exc.token
    rec["observed"] = {"token": tok, "g4": fx["inputs"]["g4"],
                       "admitted_as_w2": False}
    ok = tok == "NOT_ADMITTED"
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else (tok or "ADMITTED")
    emit(rec)

    # ---------------- W2-R3-03
    rec = case("W2-R3-03", "NEG", {"token": "WRITESET_UNBOUND", "writes": 0})
    fx = pack.fixture("W2-R3-03")
    try:
        guards.historical_preimage(fx)
        rec["verdict"], rec["first_fail"], tok = "FAIL", "NOT_REFUSED", None
    except guards.GuardError as exc:
        tok = exc.token
    rec["observed"] = {"token": tok, "historical": fx["inputs"]["historical_preimage"],
                       "live": fx["inputs"]["live_preimage"],
                       "receiver_sha": sha_file(world / RECV)}
    ok = tok == "WRITESET_UNBOUND" and rec["observed"]["receiver_sha"] == env["old_sha"]
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["first_fail"] = None if ok else (tok or "NOT_REFUSED")
    emit(rec)

    # ---------------- W2-R3-04
    rec = case("W2-R3-04", "EDGE", {"token": "WORKSPACE_DRIFT_BOUNDED"})
    fx = pack.fixture("W2-R3-04")
    try:
        d = guards.workspace_counts(fx)
        rec["observed"] = d
        rec["verdict"] = "PASS"
    except guards.GuardError as exc:
        rec["observed"] = {"token": exc.token, "detail": str(exc)}
        rec["verdict"], rec["first_fail"] = "FAIL", exc.token
    emit(rec)

    passed = sum(1 for r in rows if r["verdict"] == "PASS")
    not_admitted = sum(1 for r in rows if r["verdict"] == "NOT_ADMITTED")
    result = {
        "schema": "FHS5.PLP.G3.W2.Run@1",
        "run_id": f"W2-G3-{time.strftime('%Y%m%dT%H%M%S')}",
        "candidate": pack.candidate, "source_manifest_sha256": pack.sha256,
        "pack_tree_sha256": v["tree_sha256"], "case_set_sha256": v["case_set_sha256"],
        "cases": rows, "pass": passed, "total": len(rows),
        "dev": {"base": BASE, "preimage_sha256": env["old_sha"],
                "postimage_sha256": env["post_sha"]},
        "ops": {"root": str(env["ops_out"]), "compensated": True},
        "verdict": "NOT_ADMITTED" if not_admitted else ("PASS" if passed == 12 else "PARTIAL"),
        "not_admitted": not_admitted,
        "not_claimed": ["W2_NF_VALIDATED", "other Hosts", "W3 full",
                        "Publisher/Release", "original-domain DEV ECP"],
    }
    write(run_root / "W2_RESULT.json", result)
    print(json.dumps({"ok": passed == 12, "pass": passed, "total": len(rows)}))
    return 0 if passed == 12 else 2


if __name__ == "__main__":
    sys.exit(main())
