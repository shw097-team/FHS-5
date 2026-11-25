#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W0 TPM: generate the four construction contracts from real bytes and run
the missing-B / no-source gates plus the real plp-tpm-review Reviewer."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.PARTIES / "tpm"
OUT.mkdir(parents=True, exist_ok=True)

PLUGIN = Path(r"C:\Users\user\.codex\plugins\cache\created-by-me-remote\plp-tpm-review\1.0.1")
REVIEW_CORE = PLUGIN / "scripts" / "review_core.py"


def host_refs() -> dict:
    comp = os.environ.get("COMPUTERNAME", "unknown")
    who = f"{os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}"
    return {
        "host_ref": "CODEX-LOCAL-" + lib.sha_bytes(comp.encode())[:12],
        "principal_ref": "principal-" + lib.sha_bytes(who.encode())[:16],
        "computer_name_recorded": False,
        "user_name_recorded": False,
    }


def pack_verify() -> dict:
    manifest = lib.load_json(lib.PACK / "05_W0_SOURCE_MANIFEST.json")
    files = []
    for entry in manifest["pack_files"]:
        p = lib.PACK / entry["path"]
        h = lib.sha_file(p)
        files.append(
            {
                "path": entry["path"],
                "sha256": h,
                "bytes": len(p.read_bytes()),
                "declared_sha256": entry["sha256"],
                "declared_bytes": entry["bytes"],
                "ok": h == entry["sha256"] and len(p.read_bytes()) == entry["bytes"],
            }
        )
    return {
        "manifest_sha256": lib.sha_file(lib.PACK / "05_W0_SOURCE_MANIFEST.json"),
        "pack_version": manifest["pack_version"],
        "files": files,
        "all_ok": all(f["ok"] for f in files),
        "s33_sha256": lib.sha_file(next((lib.ROOT / "01_PACK" / "W0M_CODEX_FIRST").glob("*CODEX-FIRST-r4.md"))),
    }


def repo_context() -> dict:
    st = lib.run(["git", "-C", str(lib.REPO), "status", "--porcelain=v1", "--untracked-files=all"], lib.ROOT).__getitem__("stdout")
    return {
        "repo_root": lib.run(["git", "-C", str(lib.REPO), "rev-parse", "--show-toplevel"], lib.ROOT)["stdout"].strip(),
        "head": lib.run(["git", "-C", str(lib.REPO), "rev-parse", "HEAD"], lib.ROOT)["stdout"].strip(),
        "branch": lib.run(["git", "-C", str(lib.REPO), "branch", "--show-current"], lib.ROOT)["stdout"].strip(),
        "dirty_entries": [x for x in st.splitlines() if x],
        "clean": not st.strip(),
    }


def source_gate(contract: dict) -> dict:
    """Fail closed when a required source pin is absent or not 64 hex."""
    pins = contract.get("source_refs") or []
    if not pins:
        return {"gate": "G-NO-SOURCE", "exit": 3, "status": "SOURCE_UNBOUND", "admitted": False}
    for pin in pins:
        s = (pin or {}).get("sha256") or ""
        if len(s) != 64 or any(c not in "0123456789abcdef" for c in s.lower()):
            return {"gate": "G-NO-SOURCE", "exit": 3, "status": "SOURCE_UNBOUND", "admitted": False, "pin": pin}
    return {"gate": "G-NO-SOURCE", "exit": 0, "status": "SOURCE_BOUND", "admitted": True}


def missing_b_gate(required: list[str], observed: list[str]) -> dict:
    missing = [c for c in required if c not in observed]
    if missing:
        return {
            "gate": "G-MISSING-B",
            "exit": 2,
            "status": "REQUIRED_CHILD_MISSING",
            "missing": missing,
            "parent_verdict": "FAIL",
        }
    return {"gate": "G-MISSING-B", "exit": 0, "status": "COMPLETE", "missing": []}


def build():
    pv = pack_verify()
    rc = repo_context()
    hr = host_refs()
    req_sha = lib.sha_file(lib.REPO / "requirements.md")
    head = rc["head"]

    pi = {
        "contract": "PI",
        "contract_id": "FHS5-W0NF-PI-20261125-01",
        "project_id": "FHS-5_PLP",
        "subject_id": "FHS-5_PLP/W0",
        "batch_id": "FHS-5/W0/B0-NF",
        "source_refs": [
            {"path": "01_PACK/FHS-5_PLP_W0_NATIVE_FIRST/05_W0_SOURCE_MANIFEST.json",
             "sha256": pv["manifest_sha256"]},
            {"path": "02_CANDIDATE/repo/requirements.md", "sha256": req_sha},
        ],
        "parent": {"id": "SAMPLE", "statement": "briefcheck produces a fail-closed A/B completeness verdict"},
        "children": [
            {"id": "SAMPLE-R1", "statement": "UTF-8 Markdown in an approved root; relative input; SHA-256 verified"},
            {"id": "SAMPLE-R2", "statement": "A and B are independent required children; parent passes iff both present, checked and unique"},
            {"id": "SAMPLE-R3", "statement": "stable UTF-8 JSON; no source write; exit 0/2/3"},
            {"id": "SAMPLE-R4", "statement": "idempotent twice; one reversible output write with readback"},
        ],
        "negative_cases": ["absolute", "dotdot", "UNC", "symlink/junction/reparse", "invalid UTF-8",
                           "SHA mismatch", "duplicate", "ambiguous", "malformed"],
        "acceptance": "every child and negative case has fixture+argv+expected exit+oracle",
    }
    pd = {
        "contract": "PD",
        "contract_id": "FHS5-W0NF-PD-20261125-01",
        "pi_ref": pi["contract_id"],
        "repo_context": rc,
        "capability": {
            "python": sys.version.split()[0],
            "git": lib.run(["git", "--version"], lib.ROOT)["stdout"].strip(),
            "sandbox": "CODEX workspace sandbox; writes confined to authorized engineering root",
        },
        "write_set": [
            {"path": "briefcheck.py", "change": "modified", "preimage": lib.sha_file(lib.REPO / "briefcheck.py")},
            {"path": "tests/test_briefcheck.py", "change": "modified",
             "preimage": lib.sha_file(lib.REPO / "tests" / "test_briefcheck.py")},
        ],
        "baseline": {"head": head, "branch": rc["branch"], "clean": rc["clean"]},
        "claim_ceiling": "LOCAL_CODEX_SCOPED_CONSTRUCTION",
    }
    dev = {
        "contract": "DEV_ECP",
        "contract_id": "FHS5-W0NF-DEV-20261125-01",
        "pd_ref": pd["contract_id"],
        "sample": "briefcheck",
        "argv": ["python", "-m", "briefcheck", "--root", "<root>", "--input", "<rel>", "--sha256", "<sha>"],
        "cwd": str(lib.REPO),
        "env": {"PYTHONIOENCODING": "utf-8", "PYTHONPATH": "<candidate repo>"},
        "timeout_s": 30,
        "expected": {"0": "COMPLETE", "2": "MISSING", "3": "INVALID_* / SHA_MISMATCH"},
        "write_set": [w["path"] for w in pd["write_set"]],
        "rollback": "git checkout -- <write-set paths> to the frozen preimage commit; no source overwrite",
        "source_refs": [{"path": "02_CANDIDATE/repo/requirements.md", "sha256": req_sha}],
    }
    ops = {
        "contract": "OPS_ECP",
        "contract_id": "FHS5-W0NF-OPS-20261125-01",
        "dev_ref": dev["contract_id"],
        "host": hr["host_ref"],
        "principal": hr["principal_ref"],
        "policy": "FHS5-CODEX-FIRST-2026-11-25",
        "effect_scope": ["SOURCE_READ", "DEV_WRITE_IN_REPO", "LOCAL_CLI_RUN",
                         "REVERSIBLE_OUTPUT_WRITE", "OUTPUT_RESTORE"],
        "output_root": str(lib.ROOT / "04_DEV_OPS" / "output"),
        "recovery": "delete only this run's output file; preimage restore for modified repo files",
        "excluded": ["external deploy", "ACL/registry change", "publisher release", "user data"],
        "source_refs": [{"path": "01_PACK/FHS-5_PLP_W0_NATIVE_FIRST/02_W0_OPS_ECP.md",
                         "sha256": lib.sha_file(lib.PACK / "02_W0_OPS_ECP.md")}],
    }
    for name, obj in (("pi", pi), ("pd", pd), ("dev_ecp", dev), ("ops_ecp", ops)):
        lib.write_json(OUT / f"{name}.json", obj)

    # Gates
    missing_fixture = (lib.REPO / "fixtures" / "case_missing.md").read_text(encoding="utf-8")
    observed_children = [c for c in ("A", "B") if f"- [x] {c}" in missing_fixture]
    gate_missing = missing_b_gate(["A", "B"], observed_children)
    gate_source = source_gate(pi)
    bad_pi = dict(pi)
    bad_pi["source_refs"] = []
    gate_source_neg = source_gate(bad_pi)

    # Real reviewer
    inp = OUT / "input"
    inp.mkdir(parents=True, exist_ok=True)
    (inp / "requirements.md").write_bytes((lib.REPO / "requirements.md").read_bytes())
    contracts_md = inp / "contracts.md"
    contracts_md.write_text(
        "# W0 NF contracts (generated from real bytes)\n\n"
        f"- PI: `{pi['contract_id']}`\n"
        f"- PD: `{pd['contract_id']}` head `{head}`\n"
        f"- DEV ECP: `{dev['contract_id']}`\n"
        f"- OPS ECP: `{ops['contract_id']}`\n\n"
        "NF-R01 requires frozen source pins before construction. "
        "SAMPLE-R2 requires the independent child B. "
        "The OPS contract is local CODEX native and excludes external effects.\n",
        encoding="utf-8",
    )
    request = {
        "scope": {"wp": "B0-NF", "effect": "SOURCE_READ", "wave": "W0"},
        "mode": "review_only",
        "review_subject": "FHS-5/W0/B0-NF/briefcheck",
        "crosswalk": [
            {
                "original_requirement_id": "SAMPLE-R2", "polarity": "POS", "consumer_ref": "OWNER-B0",
                "child_units": ["A", "B"], "phase": "W0", "unit_id": "B0-R2", "case_ref": "F5-W0-T03",
                "must_contain": "A和B各有", "pd_ref": pd["contract_id"], "pi_ref": pi["contract_id"],
                "source": "REQ", "effect": "SOURCE_READ", "line": 5,
            },
            {
                "original_requirement_id": "NF-R01", "polarity": "POS", "consumer_ref": "OWNER-B0",
                "child_units": ["CTR"], "phase": "W0", "unit_id": "B0-NFR01", "case_ref": "F5-W0-T01",
                "must_contain": "frozen source pins", "pd_ref": pd["contract_id"], "pi_ref": pi["contract_id"],
                "source": "CTR", "effect": "SOURCE_READ", "line": 8,
            },
        ],
        "sources": [
            {"path": "requirements.md", "label": "REQ", "expected_sha256": req_sha},
            {"path": "contracts.md", "label": "CTR", "expected_sha256": lib.sha_file(contracts_md)},
        ],
        "profile": "QUICK",
        "schema_version": "PLP.REVIEW.REQUEST@2",
    }
    lib.write_json(OUT / "review-request.json", request)
    review_out = OUT / "review"
    review_out.mkdir(exist_ok=True)
    r = lib.run(
        [sys.executable, str(REVIEW_CORE), "--request", str(OUT / "review-request.json"),
         "--input-root", str(inp), "--outroot", str(review_out)],
        lib.ROOT,
        timeout=120,
        raw_dir=OUT / "raw",
        tag="reviewer",
    )
    (OUT / "reviewer.exit").write_text(str(r["exit"]), encoding="utf-8")
    try:
        review_stdout = json.loads(r["stdout"])
    except Exception:
        review_stdout = {"parse_error": r["stdout"][:400]}
    gate = {
        "schema": "FHS5.W0NF.TPMGate@1",
        "generated_at": lib.now(),
        "pack": pv,
        "repo": rc,
        "contracts": {"pi": lib.sha_file(OUT / "pi.json"), "pd": lib.sha_file(OUT / "pd.json"),
                      "dev_ecp": lib.sha_file(OUT / "dev_ecp.json"), "ops_ecp": lib.sha_file(OUT / "ops_ecp.json")},
        "gates": {"missing_b": gate_missing, "source_positive": gate_source, "source_negative": gate_source_neg},
        "reviewer": {"exit": r["exit"], "stdout": review_stdout, "stderr_sha": r["stderr_sha256"],
                     "claim_ceiling": "AUTHOR_DESIGN_ONLY"},
    }
    lib.write_json(OUT / "tpm_gate.json", gate)
    print(json.dumps({
        "pack_ok": pv["all_ok"],
        "contracts": gate["contracts"],
        "missing_b": gate_missing,
        "source_pos": gate_source["status"],
        "source_neg": gate_source_neg["status"],
        "reviewer_exit": r["exit"],
        "reviewer_state": review_stdout.get("state"),
        "defects": review_stdout.get("defects"),
        "unbound": review_stdout.get("unbound"),
    }, ensure_ascii=False, indent=2))
    return gate


if __name__ == "__main__":
    build()
