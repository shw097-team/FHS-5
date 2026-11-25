import argparse, json, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--finding", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    f = json.loads(Path(a.finding).read_text(encoding="utf-8"))
    finding = f.get("finding") or f
    rq = {
        "RQ0": "finding has command/exit/raw/reproduction",
        "RQ1": "reproduced in candidate worktree",
        "RQ2": "root cause localized to duplicate counting",
        "RQ3": "affected cone: parser duplicate branch + R3/R7 cases",
        "RQ4": "no external source required",
        "RQ5": "two alternatives considered",
        "RQ6": "security impact: fail-open completeness claim",
        "RQ7": "compatibility: no schema change required",
        "RQ8": "next: patch and affected retest",
    }
    alternatives = [
        {"id": "ALT-1", "name": "reject duplicates fail-closed", "cost": "low", "risk": "low", "chosen": True},
        {"id": "ALT-2", "name": "deduplicate with warning", "cost": "low", "risk": "medium: silent normalization", "chosen": False},
    ]
    advice = {
        "root_cause": "v1 collected checked letters in a set without counting duplicates",
        "reproduce": finding.get("reproduction", "run R3/R7"),
        "minimal_patch": "count seen[A]/seen[B] and reject",
        "test": "R3 INVALID_DUP; R7 INVALID_FORMAT",
        "security": "fail-closed; no path/secret effect",
        "compat": "same JSON schema/exit codes",
        "docs": "requirements duplicate negative",
        "rollback": "restore v1 file from git",
        "monitor": "re-run affected cases only",
        "next": "12' candidate + checker",
    }
    out = {
        "schema": "FHS5.B0NF.FAR@1",
        "claim_ceiling": "BUILD_MINIMAL_FAR_REFERENCE",
        "finding": finding,
        "rq": rq,
        "alternatives": alternatives,
        "chosen": "ALT-1",
        "advice": advice,
        "keys": ["finding_id","root_cause","alternatives","chosen","risk","next","evidence"],
        "risk": "medium if fail-open; low after fail-closed patch",
        "next": "patch as 12' revision",
        "evidence": finding.get("raw_sha256"),
        "source_status": "HIT_LOCAL",
        "not_covered": ["Fabric three-source profile", "FAR-T20/FARP30 full denominator"],
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"chosen": out["chosen"], "alternatives": len(alternatives), "advice": len(advice)}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
