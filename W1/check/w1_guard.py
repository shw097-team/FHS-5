#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W1 author guard: structure, identity, obligation coverage, case inventory.
Read-only. Emits AUTHOR_LOCAL_LINKS_ONLY at best; never a native/original verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

SHA = re.compile(r"^[a-f0-9]{64}$")
IDENT = re.compile(r"<!-- FHS5_IDENTITY: (\{[^\r\n]+\}) -->")
KEYS = ("project_id", "subject_id", "scope", "wave_id", "batch_id", "source_manifest_sha256")
DOCS = [
    "00_WAVE_RUN_MANIFEST.md", "01_SOURCE_SCOPE_AND_CONSTRUCTION.md",
    "03_DEV_ECP.md", "04_OPS_ECP.md", "05_PLANNED_TQAEP.md",
    "06_PERMISSION_STOP_RESUME.md", "07_EVIDENCE_AND_CHECKER.md",
    "08_AS_BUILT_AND_HANDOFF.md", "09_README_RUN_ORDER.md",
    "W1_START_THIN_PROMPT.md",
]
JSONS = ["SOURCE_MANIFEST.json", "PACKAGE_FILE_MANIFEST.json",
         "00_WAVE_RUN_MANIFEST.json", "02_ORIGINAL_CONTRACT_REFS.json",
         "05_PLANNED_TQAEP.json"]
CASE_IDS = ["W1-HOST-01", "W1-HOST-02", "W1-HOST-03", "W1-HERMES-01",
            "W1-ABI-01", "W1-ABI-02", "W1-SEC-01", "W1-API-01",
            "W1-R3-01", "W1-R3-02", "W1-R3-03", "W1-R3-04", "W1-R3-05"]
W0_IDS = [f"F5-W0-T{i:02d}" for i in range(1, 25)]
WPS = [f"WM1-P0{i}" for i in range(1, 7)]
HOSTS = ["ChatGPT", "Codex", "Hermes"]
STAGES = ["Loaded", "Invoked", "ActualServed"]
BANNED = ("TODO", "TBD", "FILL_ME", "<placeholder>", "全部待補", "此處填入", "lorem ipsum")


class GuardError(Exception):
    pass


def require(cond, msg):
    if not cond:
        raise GuardError(msg)


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise GuardError("JSON_DUPLICATE_KEY:" + k)
        out[k] = v
    return out


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_pairs)


def safe_rel(rel: str):
    require(isinstance(rel, str) and rel and "\\" not in rel and ":" not in rel, f"BAD_PATH:{rel}")
    p = PurePosixPath(rel)
    require(not p.is_absolute() and all(x not in ("", ".", "..") for x in rel.split("/")),
            f"PATH_TRAVERSAL:{rel}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-root", required=True)
    ap.add_argument("--delivery-root", default=None)
    a = ap.parse_args()
    pack = Path(a.pack_root).resolve(strict=True)
    checks = []

    def ok(name, cond, detail=""):
        if not cond:
            raise GuardError(f"{name}:{detail}")
        checks.append(name)

    try:
        for rel in DOCS + JSONS:
            ok("normative_present", (pack / rel).is_file(), rel)
        md = sorted(p.name for p in pack.glob("*.md"))
        js = sorted(p.name for p in pack.glob("*.json"))
        ok("md_count_10", md == sorted(DOCS), str(len(md)))
        ok("json_count_5", js == sorted(JSONS), str(len(js)))
        ok("normative_15", len(md) + len(js) == 15, f"{len(md)}+{len(js)}")

        wave = load(pack / "00_WAVE_RUN_MANIFEST.json")
        ident = {k: wave[k] for k in KEYS}
        ok("identity_top_level", all(isinstance(ident[k], str) and ident[k] for k in KEYS))
        ok("identity_nested", wave.get("identity") == ident)
        ok("wave_id", ident["wave_id"] == "W1")
        ok("claim_ceiling", wave.get("claim_ceiling") == "AUTHOR_DESIGN_ONLY")
        ok("effect_analysis", wave.get("effect_analysis") == "DRAFT")
        ok("source_set_state", wave.get("source_set_state") == "SELECTED_ONLY")
        ok("reader_unbound", wave.get("original_reader_state") == "UNBOUND")
        ok("claims_false", wave.get("claims") == {
            "local_observed": False, "native_observed": False,
            "independent_accepted": False, "released": False})
        for k in ("execution_admission_receipt", "independent_checker_receipt",
                  "publisher_receipt", "verified_original_receipt_ref"):
            ok("receipt_null", wave.get(k) is None, k)

        fm = load(pack / "PACKAGE_FILE_MANIFEST.json")
        ok("fm_schema", fm.get("schema") == "FHS5.PLP.FileManifest@proposal-2")
        ok("fm_identity", fm.get("identity") == ident)
        declared = {e["path"]: e for e in fm["files"]}
        ok("fm_no_self", "PACKAGE_FILE_MANIFEST.json" not in declared)
        ok("fm_unique", len(declared) == len(fm["files"]))
        actual = {p.relative_to(pack).as_posix() for p in pack.rglob("*") if p.is_file()}
        actual.discard("PACKAGE_FILE_MANIFEST.json")
        ok("fm_covers_all", actual == set(declared),
           f"missing={sorted(actual-set(declared))} extra={sorted(set(declared)-actual)}")
        for rel, e in declared.items():
            safe_rel(rel)
            data = (pack / rel).read_bytes()
            ok("fm_digest", digest(data) == e["sha256"], rel)
            ok("fm_bytes", len(data) == e["bytes"], rel)

        sm = load(pack / "SOURCE_MANIFEST.json")
        ok("sm_schema", sm.get("schema") == "FHS5.PLP.SourceManifest@proposal-2")
        ok("sm_selected", sm.get("required_source_set") == "SELECTED_ONLY")
        ok("sm_partial", sm.get("coverage_claim") == "PARTIAL_SOURCE_SET_ONLY")
        ok("sm_sha_matches", digest((pack / "SOURCE_MANIFEST.json").read_bytes())
           == ident["source_manifest_sha256"])
        ok("sm_count_16", len(sm["sources"]) == 16, str(len(sm["sources"])))
        ids = [s["source_id"] for s in sm["sources"]]
        ok("sm_ids_unique", len(ids) == len(set(ids)))
        for required_id in ("M", "B00", "B01", "B02", "B03", "B04", "B05",
                            "WM", "W1M", "W0MB", "H-CLOSE", "H-PATCH", "CTRLW1", "STARTW1"):
            ok("sm_required_source", required_id in ids, required_id)
        for s in sm["sources"]:
            safe_rel(s["path"])
            data = (pack / s["path"]).read_bytes()
            ok("sm_source_sha", digest(data) == s["sha256"], s["source_id"])
            ok("sm_source_bytes", len(data) == s["bytes"], s["source_id"])
            ok("sm_source_lines", len(data.decode("utf-8-sig").splitlines()) == s["lines"], s["source_id"])

        refs = load(pack / "02_ORIGINAL_CONTRACT_REFS.json")
        ok("refs_identity", refs.get("identity") == ident)
        for k in ("original_pi_ref", "original_pd_ref", "original_ecp_ref", "original_tqaep_ref"):
            ok("refs_null", refs.get(k) is None, k)
        ok("refs_unbound", refs.get("original_reader_state") == "UNBOUND")

        tq = load(pack / "05_PLANNED_TQAEP.json")
        ok("tq_identity", tq.get("identity") == ident)
        ok("tq_projection", tq.get("projection_of_sha256")
           == digest((pack / "05_PLANNED_TQAEP.md").read_bytes()))
        ok("tq_cases_equal", tq.get("cases") == wave.get("cases"))
        cases = wave.get("cases") or []
        ok("case_count_13", len(cases) == 13, str(len(cases)))
        ok("case_ids_exact", [c["case_id"] for c in cases] == CASE_IDS)
        kinds = {c["kind"] for c in cases}
        ok("case_kinds", {"POS", "NEG", "SEC", "EDGE"}.issubset(kinds), str(sorted(kinds)))
        for c in cases:
            cid = c["case_id"]
            ok("case_scope", c["subject_id"] == ident["subject_id"] and c["scope"] == ident["scope"], cid)
            for stem in ("oracle", "fixture"):
                rel = c[f"{stem}_path"]
                safe_rel(rel)
                ok("case_file_present", (pack / rel).is_file(), f"{cid}:{rel}")
                ok("case_file_sha", digest((pack / rel).read_bytes()) == c[f"{stem}_sha256"], cid)
            ok("case_expected", isinstance(c.get("expected_raw"), dict) and c["expected_raw"], cid)

        EXPECT_KIND = {"W1-HOST-01":"POS","W1-HOST-02":"NEG","W1-HOST-03":"NEG","W1-HERMES-01":"POS",
                       "W1-ABI-01":"NEG","W1-ABI-02":"NEG","W1-SEC-01":"SEC","W1-API-01":"POS",
                       "W1-R3-01":"POS","W1-R3-02":"NEG","W1-R3-03":"NEG","W1-R3-04":"EDGE","W1-R3-05":"NEG"}
        w1m_lines = (pack / "sources/W1M.md").read_text(encoding="utf-8-sig").splitlines()
        for c in cases:
            cid = c["case_id"]
            ok("case_kind_map", c.get("kind") == EXPECT_KIND.get(cid), cid)
            oracle = load(pack / c["oracle_path"])
            ok("case_oracle_firstfail", oracle.get("first_fail") == c["expected_raw"].get("first_fail"), cid)
            s, e = c.get("clause_start_line"), c.get("clause_end_line")
            ok("case_clause_exact", c.get("clause_text") == "\n".join(w1m_lines[s-1:e]), cid)

        body01 = (pack / "01_SOURCE_SCOPE_AND_CONSTRUCTION.md").read_text(encoding="utf-8")
        for i in range(1, 17):
            ok("cg_req_row", body01.count(f"| `CG-R2-REQ-{i:02d}` |") == 1, str(i))
        for i in range(1, 18):
            ok("pcb_fr_row", body01.count(f"| `PCB-FR{i:02d}` |") == 1, str(i))

        tool = load(pack / "inventory/TOOL_IDENTITY_LEDGER.json")
        ok("tool_ledger_485", len(tool.get("tools", [])) == 485 and tool.get("counts", {}).get("total") == 485)
        ok("tool_ids_unique", len({x["tool_id"] for x in tool["tools"]}) == 485)
        den = load(pack / "inventory/DENOMINATOR_LEDGER.json")
        ok("denominator_families", len(den.get("families", [])) >= 20)

        body01 = (pack / "01_SOURCE_SCOPE_AND_CONSTRUCTION.md").read_text(encoding="utf-8")
        body05 = (pack / "05_PLANNED_TQAEP.md").read_text(encoding="utf-8")
        body00 = (pack / "00_WAVE_RUN_MANIFEST.md").read_text(encoding="utf-8")
        for i in range(1, 8):
            ok("seam_row", f"| S{i} " in body01, str(i))
        for ns in ("GuideThinPrompt@proposal-2","GuidePromptAdvice@proposal-2",
                   "GuidePackageControlFields@proposal-2","PLP.BridgeContextView@proposal-2",
                   "PLP.BridgeDelta@proposal-4"):
            ok("namespace_tag", ns in body01, ns)
        for wp in WPS:
            ok("wp_in_01", wp in body01, wp)
            ok("wp_in_00", wp in body00, wp)
        for host in HOSTS:
            for stage in STAGES:
                ok("u017_child", f"U-017/{host}/{stage}" in body01, f"{host}/{stage}")
        for fn in ("Kanban", "Delegation", "Swarm"):
            ok("u028_child", f"U-028/Hermes/{fn}" in body01, fn)
        for api in ("inspect_package", "explain_slice", "render_agent_context", "compare_context"):
            ok("api_named", api in body01, api)
        for dg in ("source_set_sha256_stable", "manifest_identity_sha256",
                   "context_identity_sha256", "package_sha256"):
            ok("digest_distinct", dg in body01, dg)
        for b in ("UNTRUSTED SOURCE DATA", "PATH_OUTSIDE_ROOT", "ABI_LOSSY_CROSSWALK",
                  "HOST_PENDING", "FALSE_AUTHORITY"):
            ok("neg_token", b in body01, b)
        for cid in CASE_IDS:
            ok("case_in_05", cid in body05, cid)
            ok("case_in_01", cid in body01 or cid in body00, cid)
        for wid in W0_IDS:
            ok("w0_disposition", wid in body05, wid)
        ok("w0_count_24", sum(1 for w in W0_IDS if w in body05) == 24)

        for rel in DOCS:
            body = (pack / rel).read_text(encoding="utf-8")
            m = IDENT.search(body[:900])
            ok("doc_header", m is not None, rel)
            ok("doc_identity", json.loads(m.group(1)) == ident, rel)
            ok("doc_sections", body.count("## ") >= 2, rel)
            for key in ("Input:", "Operation:", "Output:", "Consumer:", "NEG:", "FirstFail:"):
                ok("doc_fields", key in body, f"{rel}:{key}")
            for v in (ident["subject_id"], ident["scope"], ident["batch_id"]):
                ok("doc_identity_visible", v in body, rel)
            ok("doc_no_placeholder", not any(x.lower() in body.lower() for x in BANNED), rel)
            ok("doc_no_unsubstituted_token", "{{" not in body and "}}" not in body, rel)

        for rel in DOCS:
            b = (pack / rel).read_text(encoding="utf-8")
            ok("source_count_text", not any(x in b for x in ("釘選 17", "17 個 source", "選 17 源", "取得 17 源", "17 源逐檔")), rel)
        for rel in ("03_DEV_ECP.md", "04_OPS_ECP.md"):
            body = (pack / rel).read_text(encoding="utf-8")
            for key in ("Applicability:", "Preconditions:", "Postconditions:",
                        "Permission:", "Readback:", "Recovery:"):
                ok("ecp_field", key in body, f"{rel}:{key}")
        for key in ("Requirement:", "Case:", "Oracle:", "POS:", "NEG:", "ExpectedRaw:", "Checker:"):
            ok("tqaep_field", key in body05, key)
        ok("holds_named", isinstance(wave.get("holds"), list) and len(wave["holds"]) >= 14)
        ok("hold_cr_doc04", "HOLD_CR-DOC04-STATE-MAP" in (wave.get("holds") or []))
        ok("host_claims_local_evidence", all("local_evidence" not in h or h.get("observation") == "NOT_OBSERVED"
                                             for h in (wave.get("host_claims") or [])))
        refpat = re.compile(r"`([A-Za-z0-9_./\-\u4e00-\u9fff]+\.(?:md|json|py|txt|zip))`")
        delivery = Path(a.delivery_root).resolve() if a.delivery_root else pack.parent
        for rel in DOCS:
            body = (pack / rel).read_text(encoding="utf-8")
            for m in refpat.finditer(body):
                ref = m.group(1)
                if "/" not in ref:
                    continue
                ok("doc_ref_exists", (pack / ref).is_file() or (delivery / ref).is_file(), f"{rel}:{ref}")
        ok("host_claims_21", len(wave.get("host_claims") or []) == 21)
        ok("observations_empty", wave.get("observations") == [])

        print(json.dumps({
            "status": "W1_AUTHOR_LOCAL_LINKS_ONLY",
            "claim_ceiling": "AUTHOR_DESIGN_ONLY",
            "normative": 15, "md": 10, "json": 5,
            "sources": len(sm["sources"]), "cases": len(cases),
            "w0_dispositions": 24, "wps": 6, "checks": len(checks),
            "original_reader": "UNBOUND", "native": "NOT_VERIFIED", "release": "NOT_GRANTED",
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except (GuardError, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"status": "W1_GUARD_FAIL_CLOSED", "first_fail": str(e),
                          "claim_ceiling": "AUTHOR_DESIGN_ONLY"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())

