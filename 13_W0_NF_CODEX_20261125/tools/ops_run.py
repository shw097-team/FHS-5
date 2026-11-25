#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local CODEX Native OPS O1-O6: probe, POS/NEG CLI, reversible output,
readback/restore, provider-OFF import trace and parity."""
from __future__ import annotations

import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import policy

OUT = lib.ROOT / "04_DEV_OPS"
OUTPUT_ROOT = OUT / "output"
RAW = OUT / "raw"
ROOT = lib.TQAEP / "tmp" / "root"
TMP = lib.TMP
ORACLE = lib.TQAEP / "oracle.json"

LEGACY_PREFIXES = ("hgk", "fabric", "sbl", "fhs", "pipd", "hermes", "plp")


def is_legacy(mod: str) -> bool:
    top = mod.split(".")[0].lower()
    return any(top.startswith(p) for p in LEGACY_PREFIXES)


def probe():
    def ver(argv):
        r = lib.run(argv, lib.ROOT, timeout=60, raw_dir=RAW, tag="probe_" + argv[0].split("\\")[-1])
        return {"argv": argv, "exit": r["exit"], "stdout": r["stdout"].strip()[:200],
                "stderr": r["stderr"].strip()[:200]}
    comp = os.environ.get("COMPUTERNAME", "unknown")
    who = f"{os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}"
    return {
        "os": platform.platform(),
        "python": sys.version.split()[0],
        "git": ver(["git", "--version"]),
        "codex": ver(["codex", "--version"]),
        "host_ref": "CODEX-LOCAL-" + lib.sha_bytes(comp.encode())[:12],
        "principal_ref": "principal-" + lib.sha_bytes(who.encode())[:16],
        "policy": "FHS5-CODEX-FIRST-2026-11-25",
        "sandbox_roots": [str(lib.ROOT)],
        "hermes": "HOST_SERVING_UNVERIFIED (compatibility only; not a W0 gate)",
    }


def import_trace(tag: str) -> dict:
    args = ["--root", str(ROOT), "--input", "case_ok.md", "--sha256", lib.sha_file(ROOT / "case_ok.md")]
    r = lib.run([sys.executable, "-X", "importtime", "-m", "briefcheck", *args], ROOT,
                env_extra={"PYTHONPATH": str(lib.REPO), "FHS5_BRIDGE": "OFF"},
                raw_dir=RAW, tag=tag)
    mods = []
    for line in r["stderr"].splitlines():
        m = re.search(r"\|\s*([A-Za-z0-9_.]+)\s*$", line)
        if m:
            mods.append(m.group(1))
    legacy = sorted({m for m in mods if is_legacy(m)})
    return {"exit": r["exit"], "stdout": r["stdout"].strip(), "modules": sorted(set(mods)),
            "legacy_imports": legacy, "raw": r.get("raw_refs")}


def module_list() -> dict:
    code = (
        "import sys, json; import briefcheck; "
        "print(json.dumps(sorted(m for m in sys.modules if not m.startswith('_'))))"
    )
    r = lib.run([sys.executable, "-c", code], lib.REPO,
                env_extra={"PYTHONPATH": str(lib.REPO)}, raw_dir=RAW, tag="module_list")
    mods = json.loads(r["stdout"]) if r["exit"] == 0 else []
    legacy = sorted({m for m in mods if is_legacy(m)})
    return {"modules": mods, "legacy_modules": legacy, "exit": r["exit"]}


def main():
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    if not (ROOT / "case_ok.md").is_file():
        ROOT.mkdir(parents=True, exist_ok=True)
        for p in (lib.REPO / "fixtures").glob("*.md"):
            shutil.copy2(p, ROOT / p.name)
    orc = lib.load_json(ORACLE)
    steps = {}
    steps["O1_probe"] = probe()

    # O2 POS/NEG
    pos = lib.cli(["--root", str(ROOT), "--input", "case_ok.md",
                   "--sha256", lib.sha_file(ROOT / "case_ok.md")], ROOT, raw_dir=RAW, tag="o2_pos")
    neg = lib.cli(["--root", str(ROOT), "--input", "case_missing.md",
                   "--sha256", lib.sha_file(ROOT / "case_missing.md")], ROOT, raw_dir=RAW, tag="o2_neg")
    pos_ok = policy.verify_semantics(pos["exit"], json.loads(pos["stdout"]),
                                     {"exit": 0, "status": "COMPLETE", "provided": ["A", "B"], "missing": []})
    neg_ok = policy.verify_semantics(neg["exit"], json.loads(neg["stdout"]),
                                     {"exit": 2, "status": "MISSING", "provided": ["A"], "missing": ["B"]})
    steps["O2_cli"] = {"pos": {"exit": pos["exit"], "stdout_sha": pos["stdout_sha256"],
                               "verdict": pos_ok["status"]},
                       "neg": {"exit": neg["exit"], "stdout_sha": neg["stdout_sha256"],
                               "verdict": neg_ok["status"]}}

    # O3 reversible output
    out = OUTPUT_ROOT / "result.json"
    source_before = lib.sha_file(ROOT / "case_ok.md")
    before = out.exists()
    out.write_text(pos["stdout"], encoding="utf-8")
    after_bytes = out.read_bytes()
    readback = json.loads(after_bytes.decode("utf-8"))
    o3_ok = (not before and readback.get("status") == "COMPLETE"
             and lib.sha_file(ROOT / "case_ok.md") == source_before)
    steps["O3_output"] = {"before_absent": not before, "after_sha": lib.sha_bytes(after_bytes),
                          "after_bytes": len(after_bytes), "source_unchanged":
                          lib.sha_file(ROOT / "case_ok.md") == source_before,
                          "readback": readback, "verdict": "PASS" if o3_ok else "FAIL"}

    # O4 restore
    out.unlink()
    restored = not out.exists()
    steps["O4_restore"] = {"restored_absent": restored, "source_sha": lib.sha_file(ROOT / "case_ok.md"),
                           "verdict": "PASS" if restored and lib.sha_file(ROOT / "case_ok.md") == source_before else "FAIL"}

    # O5 OFF
    clean = import_trace("o5_clean")
    marked = lib.run([sys.executable, "-m", "briefcheck", "--root", str(ROOT), "--input", "case_ok.md",
                      "--sha256", lib.sha_file(ROOT / "case_ok.md")], ROOT,
                     env_extra={"PYTHONPATH": str(lib.REPO),
                                "FHS5_PROVIDERS": "HGK,FABRIC,SBL,PIPD,HERMES"}, raw_dir=RAW, tag="o5_marked")
    ml = module_list()
    parity = clean["stdout"].strip() == marked["stdout"].strip() and clean["exit"] == marked["exit"] == 0
    ctrl_dir = TMP / "detector_control"
    ctrl_dir.mkdir(parents=True, exist_ok=True)
    (ctrl_dir / "hgk_core.py").write_text("VALUE = 1\n", encoding="utf-8")
    (ctrl_dir / "ctrl_probe.py").write_text("import hgk_core\nprint(hgk_core.VALUE)\n", encoding="utf-8")
    ctrl = lib.run([sys.executable, "-X", "importtime", str(ctrl_dir / "ctrl_probe.py")], ctrl_dir,
                   env_extra={"PYTHONPATH": str(ctrl_dir)}, raw_dir=RAW, tag="o5_detector_control")
    ctrl_mods = []
    for line in ctrl["stderr"].splitlines():
        m = re.search(r"\|\s*([A-Za-z0-9_.]+)\s*$", line)
        if m:
            ctrl_mods.append(m.group(1))
    detector_control = any(is_legacy(m) for m in ctrl_mods)
    steps["O5_off"] = {"import_trace": clean, "module_list": ml, "marked_run_exit": marked["exit"],
                       "parity": parity,
                       "detector_control": detector_control,
                       "detector_control_modules": [m for m in ctrl_mods if is_legacy(m)],
                       "legacy_modules": ml["legacy_modules"],
                       "verdict": "PASS" if (not ml["legacy_modules"] and not clean["legacy_imports"]
                                             and detector_control) else "FAIL"}

    steps["O6_consumer"] = {"state": "PENDING_FINAL_HANDOFF",
                            "note": "final consumer readback runs after CLOSEOUT/HANDOFF"}

    verdict = "PASS"
    for key in ("O2_cli", "O3_output", "O4_restore", "O5_off"):
        if key == "O2_cli":
            if steps[key]["pos"]["verdict"] != "EFFECT_VERIFIED" or steps[key]["neg"]["verdict"] != "EFFECT_VERIFIED":
                verdict = "FAIL"
        elif steps[key].get("verdict") != "PASS":
            verdict = "FAIL"
    ops = {
        "schema": "FHS5.W0NF.Ops@1",
        "generated_at": lib.now(),
        "candidate_sha": lib.git("rev-parse", "HEAD"),
        "host": steps["O1_probe"],
        "steps": steps,
        "legacy_imports": steps["O5_off"]["import_trace"]["legacy_imports"],
        "impure_modules": steps["O5_off"]["module_list"]["legacy_modules"],
        "parity": steps["O5_off"]["parity"],
        "parity_meaning": "environment-marker invariance; NOT an ON/OFF code branch",
        "detector_control": detector_control,
        "verdict": verdict,
        "not_claimed": ["EXTERNAL_GRANT", "OS_ADMIN", "PUBLISHER_RELEASE", "HERMES_COMPATIBILITY_PASS"],
    }
    lib.write_json(OUT / "ops.json", ops)
    lib.write_json(OUT / "off.json", {
        "schema": "FHS5.W0NF.OffTrace@1",
        "legacy_imports": ops["legacy_imports"],
        "impure_modules": ops["impure_modules"],
        "parity": ops["parity"],
        "parity_meaning": ops["parity_meaning"],
        "detector_control": ops["detector_control"],
        "ops_verdict": verdict,
        "trace": steps["O5_off"]["import_trace"],
        "modules": steps["O5_off"]["module_list"]["modules"],
    })
    print(json.dumps({"verdict": verdict, "O2": steps["O2_cli"], "O3": steps["O3_output"]["verdict"],
                      "O4": steps["O4_restore"]["verdict"], "O5": steps["O5_off"]["verdict"],
                      "legacy": ops["legacy_imports"]}, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
