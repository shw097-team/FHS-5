#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute the author-declared case predicates on fixtures. Read-only on the pack.
Emits AUTHOR_LOCAL_RULE_ONLY; never a native/original verdict. POS cases without an
original executor stay NOT_RUN and are never proven by a NEG refusal.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

def d(b): return hashlib.sha256(b).hexdigest()

def rule(pred, req):
    if pred == "reject_cross_host_substitution":
        if req["host"] != req["target_host"] and req["stage"] in ("Loaded","Invoked") and req["target_stage"] in ("Served","Consumed"):
            return "HOST_ABI_DRIFT"
        return None
    if pred in ("reject_skill_read_as_invoked","reject_skill_bytes_as_loaded"):
        if req.get("evidence") in ("SKILL.md","skill_bytes") and req.get("claimed_stage") in ("Loaded","Installed","Invoked"):
            return "HOST_PENDING"
        return None
    if pred == "reject_same_suffix_direct":
        a=req["source_namespace"].split("@")[0]; b=req["target_namespace"].split("@")[0]
        if a!=b and not req.get("crosswalk"):
            return "EXPLICIT_REVIEW_REQUIRED"
        return None
    if pred == "reject_unnormalized_upgrade":
        if req["from"]!=req["to"] and not req.get("crosswalk"):
            return "LOSSY_MIGRATION"
        return None
    if pred == "mark_injected_instruction":
        if re.search(r"ignore\s+permission|grant\s+release|忽略.*權限|授權.*發布", req.get("context_text",""), re.I):
            return "UNTRUSTED_SOURCE_DATA"
        return None
    if pred == "reject_missing_effect_resume":
        if set(req["required_fields"]) - set(req["present_fields"]):
            return "ABI_LOSSY_CROSSWALK"
        return None
    if pred == "bound_workspace_drift":
        if req["workspace_entries"] != req["primary_entries"] and not req["primary_hash_changed"]:
            return "WORKSPACE_DRIFT_BOUNDED"
        return None
    if pred == "reject_identity_only_restore":
        if "identity" in req.get("evidence","") and req.get("claimed")=="bytes_restored":
            return "EVIDENCE_LAUNDERING"
        return None
    return "UNKNOWN_PREDICATE"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pack-root", required=True)
    ap.add_argument("--out", default=None)
    a=ap.parse_args()
    pack=Path(a.pack_root).resolve(strict=True)
    wave=json.loads((pack/"00_WAVE_RUN_MANIFEST.json").read_text(encoding="utf-8-sig"))
    outdir=Path(a.out) if a.out else pack.parent/"evidence"/"raw"
    outdir.mkdir(parents=True, exist_ok=True)
    results=[]; failed=[]
    for c in wave["cases"]:
        cid=c["case_id"]
        fp=pack/c["fixture_path"]; op=pack/c["oracle_path"]
        if d(fp.read_bytes())!=c["fixture_sha256"]: failed.append(cid+":FIXTURE_PIN"); continue
        if d(op.read_bytes())!=c["oracle_sha256"]: failed.append(cid+":ORACLE_PIN"); continue
        f=json.loads(fp.read_text(encoding="utf-8")); o=json.loads(op.read_text(encoding="utf-8"))
        rec={"case_id":cid,"kind":c["kind"],"executable":bool(f.get("executable")),
             "predicate":f.get("predicate"),"expected":f.get("expect_error")}
        if not f.get("executable"):
            rec.update({"status":"NOT_RUN","observed":None,
                        "reason":f.get("not_run_reason","no original executor")})
        else:
            if o.get("first_fail")!=f.get("expect_error"):
                rec.update({"status":"FAIL","observed":"ORACLE_FIXTURE_FIRSTFAIL_MISMATCH",
                            "oracle_first_fail":o.get("first_fail")}); failed.append(cid+":FIRSTFAIL")
            else:
                obs=rule(f.get("predicate"), f.get("request") or {})
                ok = obs == f.get("expect_error")
                rec.update({"status":"PASS" if ok else "FAIL","observed":obs})
                if not ok: failed.append(cid+":RULE")
        results.append(rec)
    raw={"schema":"FHS5.PLP.W1.CaseRuleRun@local-1","claim_ceiling":"AUTHOR_LOCAL_RULE_ONLY",
         "subject_id":wave["subject_id"],"pack":str(pack),
         "summary":{"total":len(results),"executed":sum(1 for r in results if r["executable"]),
                    "passed":sum(1 for r in results if r["status"]=="PASS"),
                    "not_run":sum(1 for r in results if r["status"]=="NOT_RUN"),
                    "failed":len([r for r in results if r["status"]=="FAIL"])},
         "results":results}
    outp=outdir/"case_rule_results.json"
    outp.write_text(json.dumps(raw,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":"CASE_RULES_PASS" if not failed else "CASE_RULES_FAIL",
                      "summary":raw["summary"],"failed":failed,"raw_sha256":d(outp.read_bytes()),
                      "claim_ceiling":"AUTHOR_LOCAL_RULE_ONLY"},ensure_ascii=False,sort_keys=True))
    return 0 if not failed else 2

if __name__=="__main__":
    sys.exit(main())
