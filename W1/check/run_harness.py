#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W1 convergence harness: positive guards + eight mutant families (H1-H8).
Every mutant runs on an isolated copy; the delivered pack is never modified.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
PACK = OUT / "primary" if (OUT / "primary").is_dir() else OUT / "FHS-5_PLP_W1_PRIMARY"
RAW = OUT / "evidence" / "raw"
W1 = HERE / "w1_guard.py"
M22 = HERE / "m22_guard_ref.py"


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(script: Path, args: list[str]) -> tuple[int, dict]:
    cp = subprocess.run([sys.executable, str(script), *args],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        obj = json.loads(cp.stdout.strip().splitlines()[-1])
    except Exception:
        obj = {"status": "UNPARSEABLE", "stdout": cp.stdout[-800:], "stderr": cp.stderr[-800:]}
    return cp.returncode, obj


def reseal(pack: Path) -> None:
    wave = json.loads((pack / "00_WAVE_RUN_MANIFEST.json").read_text(encoding="utf-8-sig"))
    files = []
    for p in sorted(pack.rglob("*"), key=lambda x: x.relative_to(pack).as_posix()):
        if not p.is_file():
            continue
        rel = p.relative_to(pack).as_posix()
        if rel == "PACKAGE_FILE_MANIFEST.json":
            continue
        files.append({"path": rel, "bytes": p.stat().st_size, "sha256": digest(p)})
    fm = {
        "schema": "FHS5.PLP.FileManifest@proposal-2",
        "identity": wave["identity"],
        "generated_at": "2026-11-24",
        "self_hash_policy": "Mutant copy; resealed only to expose semantic checks.",
        "files": files,
    }
    (pack / "PACKAGE_FILE_MANIFEST.json").write_text(
        json.dumps(fm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def edit_text(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"mutation anchor not found in {path.name}: {old[:60]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def mutate(mid: str, pack: Path) -> str:
    if mid == "H1_source_byte":
        p = pack / "sources" / "M.md"
        b = bytearray(p.read_bytes())
        b[-2] = b[-2] ^ 0x01
        p.write_bytes(bytes(b))
        return "flip one byte in sources/M.md"
    if mid == "H2_missing_normative":
        (pack / "08_AS_BUILT_AND_HANDOFF.md").unlink()
        return "delete 08_AS_BUILT_AND_HANDOFF.md"
    if mid == "H2b_placeholder":
        p = pack / "07_EVIDENCE_AND_CHECKER.md"
        p.write_text(p.read_text(encoding="utf-8") + "\nTODO\n", encoding="utf-8", newline="\n")
        return "append TODO to 07_EVIDENCE_AND_CHECKER.md"
    if mid == "H3_child_missing":
        edit_text(pack / "01_SOURCE_SCOPE_AND_CONSTRUCTION.md",
                  "`U-028/Hermes/Swarm`", "`U-028/Hermes/REMOVED`")
        return "rename U-028/Hermes/Swarm child row"
    if mid == "H4_projection_drift":
        wp = pack / "00_WAVE_RUN_MANIFEST.json"
        w = json.loads(wp.read_text(encoding="utf-8"))
        w["cases"][0]["clause_text"] = w["cases"][0]["clause_text"] + " DRIFT"
        wp.write_text(json.dumps(w, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return "change one case clause_text in WaveControl only"
    if mid == "H5_path_traversal":
        for name in ("00_WAVE_RUN_MANIFEST.json", "05_PLANNED_TQAEP.json"):
            wp = pack / name
            w = json.loads(wp.read_text(encoding="utf-8"))
            w["cases"][0]["fixture_path"] = "../outside.json"
            wp.write_text(json.dumps(w, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return "set case fixture_path to ../outside.json"
    if mid == "H6_fake_claims":
        wp = pack / "00_WAVE_RUN_MANIFEST.json"
        w = json.loads(wp.read_text(encoding="utf-8"))
        w["claims"] = {"local_observed": True, "native_observed": True,
                       "independent_accepted": True, "released": True}
        wp.write_text(json.dumps(w, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return "set all four claims true"
    if mid == "H6b_fake_receipt":
        wp = pack / "00_WAVE_RUN_MANIFEST.json"
        w = json.loads(wp.read_text(encoding="utf-8"))
        w["execution_admission_receipt"] = {"granted": True, "issuer": "self"}
        wp.write_text(json.dumps(w, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return "insert success-shaped execution_admission_receipt"
    if mid == "H7_scope_drift":
        edit_text(pack / "03_DEV_ECP.md", '"batch_id":"W1-PACK-01"', '"batch_id":"W1-PACK-02"')
        return "change batch_id inside 03_DEV_ECP.md identity header"
    if mid == "H9_cg_req_row":
        p = pack / "01_SOURCE_SCOPE_AND_CONSTRUCTION.md"
        lines = [l for l in p.read_text(encoding="utf-8").splitlines() if "| `CG-R2-REQ-11` |" not in l]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        return "delete the CG-R2-REQ-11 row"
    if mid == "H9_pcb_fr_row":
        p = pack / "01_SOURCE_SCOPE_AND_CONSTRUCTION.md"
        lines = [l for l in p.read_text(encoding="utf-8").splitlines() if "| `PCB-FR17` |" not in l]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        return "delete the PCB-FR17 row"
    if mid == "H9_clause_truncate":
        for name in ("00_WAVE_RUN_MANIFEST.json", "05_PLANNED_TQAEP.json"):
            q = pack / name
            o = json.loads(q.read_text(encoding="utf-8"))
            o["cases"][0]["clause_text"] = o["cases"][0]["clause_text"][:20]
            q.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return "truncate cases[0].clause_text in both projections"
    if mid == "H9_kind_flip":
        for name in ("00_WAVE_RUN_MANIFEST.json", "05_PLANNED_TQAEP.json"):
            q = pack / name
            o = json.loads(q.read_text(encoding="utf-8"))
            for c in o["cases"]:
                if c["case_id"] == "W1-HOST-02":
                    c["kind"] = "POS"
            q.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return "flip W1-HOST-02 kind to POS"
    if mid == "H9_firstfail_drift":
        for name in ("00_WAVE_RUN_MANIFEST.json", "05_PLANNED_TQAEP.json"):
            q = pack / name
            o = json.loads(q.read_text(encoding="utf-8"))
            o["cases"][4]["expected_raw"]["first_fail"] = "OK"
            q.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return "drift cases[4].expected_raw.first_fail"
    if mid == "H9_source_count_text":
        p = pack / "00_WAVE_RUN_MANIFEST.md"
        edit_text(p, "本包釘選 16 個實際可回取來源", "本包釘選 17 個實際可回取來源")
        return "change source count text 16 to 17"
    if mid == "H9_extra_file":
        (pack / "fixtures" / "EXTRA.json").write_text("{}", encoding="utf-8")
        return "add an unlisted fixture"
    if mid == "H8_duplicate_key":
        p = pack / "02_ORIGINAL_CONTRACT_REFS.json"
        text = p.read_text(encoding="utf-8")
        text = text.replace('{\n  "schema"', '{\n  "schema": "dup",\n  "schema"', 1)
        p.write_text(text, encoding="utf-8", newline="\n")
        return "duplicate schema key in 02_ORIGINAL_CONTRACT_REFS.json"
    raise SystemExit(f"unknown mutation {mid}")


MUTANTS = [
    ("H1_source_byte", "H1 Source/W0", "SOURCE_SHA_MISMATCH"),
    ("H2_missing_normative", "H2 Pack", "REQUIRED_FILE_MISSING"),
    ("H2b_placeholder", "H2 Pack", "PLACEHOLDER_BODY"),
    ("H3_child_missing", "H3 Trace/coverage", "u028_child"),
    ("H4_projection_drift", "H2 Pack", "TQAEP_CASE_MISMATCH"),
    ("H5_path_traversal", "H5 Security", "PATH_TRAVERSAL"),
    ("H6_fake_claims", "H6 Effect/Host/claim", "ORIGINAL_OR_LOCAL_SUCCESS_CLAIM_UNVERIFIED"),
    ("H6b_fake_receipt", "H6 Effect/Host/claim", "ORIGINAL_RECEIPT_UNVERIFIABLE"),
    ("H7_scope_drift", "H2 Pack", "CONTRACT_SCOPE_MISMATCH"),
    ("H8_duplicate_key", "H5 Security", "JSON_DUPLICATE_KEY"),
    ("H9_cg_req_row", "H3 Trace/coverage", "cg_req_row"),
    ("H9_pcb_fr_row", "H3 Trace/coverage", "pcb_fr_row"),
    ("H9_clause_truncate", "H3 Trace/coverage", "CASE_SOURCE_CLAUSE_MISMATCH"),
    ("H9_kind_flip", "H3 Trace/coverage", "case_kind_map"),
    ("H9_firstfail_drift", "H3 Trace/coverage", "case_oracle_firstfail"),
    ("H9_source_count_text", "H2 Pack", "source_count_text"),
    ("H9_extra_file", "H2 Pack", "fm_covers_all"),
]


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    result = {"run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
              "pack": str(PACK), "positive": {}, "negatives": []}

    rc1, o1 = run(M22, ["check-pack", "--pack-root", str(PACK)])
    rc2, o2 = run(W1, ["--pack-root", str(PACK), "--delivery-root", str(OUT)])
    result["positive"] = {"m22": {"rc": rc1, "out": o1}, "w1": {"rc": rc2, "out": o2}}
    positive_ok = (rc1 == 0 and o1.get("status") == "AUTHOR_LOCAL_LINKS_ONLY"
                   and rc2 == 0 and o2.get("status") == "W1_AUTHOR_LOCAL_LINKS_ONLY")

    tmp = Path(tempfile.mkdtemp(prefix="w1-mut-", dir=str(HERE)))
    try:
        for mid, group, expect in MUTANTS:
            dest = tmp / mid
            shutil.copytree(PACK, dest)
            note = mutate(mid, dest)
            if mid != "H9_extra_file":
                reseal(dest)
            rcm, om = run(M22, ["check-pack", "--pack-root", str(dest)])
            rcw, ow = run(W1, ["--pack-root", str(dest), "--delivery-root", str(OUT)])
            combined = json.dumps([om, ow], ensure_ascii=False)
            rejected = (rcm != 0 or rcw != 0) and (expect in combined)
            which = "m22" if expect in json.dumps(om, ensure_ascii=False) else "w1"
            result["negatives"].append({
                "id": mid, "group": group, "mutation": note, "expect_token": expect,
                "guard": which, "m22_rc": rcm, "m22_first_fail": om.get("first_fail"),
                "w1_rc": rcw, "w1_first_fail": ow.get("first_fail"),
                "rejected": rejected,
            })
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    all_neg = all(x["rejected"] for x in result["negatives"])
    result["summary"] = {
        "positive_pass": positive_ok,
        "negatives_pass": all_neg,
        "negatives": f"{sum(1 for x in result['negatives'] if x['rejected'])}/{len(result['negatives'])}",
        "verdict": "SELF_CHECK_PASS_WITH_NAMED_HOLDS" if positive_ok and all_neg
        else "SELF_CHECK_PARTIAL_WITH_NAMED_HOLDS",
    }
    (RAW / "harness_results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (RAW / "harness_summary.txt").write_text(
        json.dumps(result["summary"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0 if positive_ok and all_neg else 2


if __name__ == "__main__":
    sys.exit(main())
