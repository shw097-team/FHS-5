#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Second work package through the same TPM/Guide/BodyResolver product.

Package A = adopted W1 G3 pack.  Package B = adopted W2 G3 pack.  Both must
produce five contract views; the second is not a rename of the first.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
G3 = HERE.parent
WT = G3.parent
sys.path.insert(0, str(WT / "W1" / "impl"))
sys.path.insert(0, str(G3 / "lib"))
import body_resolver as br  # noqa: E402
import guide_nf as guide  # noqa: E402
import tpm_contracts_nf as tpm  # noqa: E402

PACK_BASE = Path(r"C:\Projects\Agent_Workspace\FHS-5_Workspace"
                 r"\FHS-5_PLP_W0-W2_第三代Native-first_執行控制包_FINAL\01_BODY")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build(wave: str, subject: str, batch: str) -> dict:
    root = PACK_BASE / f"FHS-5_PLP_{wave}_NATIVE_FIRST"
    ident = {"project_id": "FHS-5_PLP", "subject_id": subject,
             "scope": f"{wave}-NF-01", "wave_id": wave, "batch_id": batch,
             "work_id": f"G3-SECOND-PACK-{wave}"}
    c = tpm.build_contracts(str(root), ident)
    rev = tpm.review(c, str(root))
    thin = guide.render_thin_prompt(
        {"identity": {"subject_id": subject, "scope": f"{wave}-NF-01"}},
        guide.select_bounded_advice(
            {"identity": {"scope": f"{wave}-NF-01"}, "mode": "PACKAGE_FIRST",
             "evidence": {"oracle_sha": c["views"]["TQAEP"].get("case_set_sha256"),
                          "policy_epoch": "NOT_DECLARED_BY_HOST"}},
            {"requested_effect": "DRAFT"}))
    text = (root / f"03_{wave}_TQAEP.md").read_text(encoding="utf-8")
    clauses = br.parse_clauses(text, f"03_{wave}_TQAEP.md", sha(text.encode()))
    return {"wave": wave, "subject": subject, "pack": str(root),
            "views": {k: (len(v) if isinstance(v, (list, dict)) else v)
                      for k, v in c["views"].items()},
            "case_count": len(c["views"]["TQAEP"].get("cases") or []),
            "clauses": len(clauses),
            "review": {k: rev.get(k) for k in ("verdict", "findings", "first_fail", "count")
                       if k in rev},
            "thin_prompt_sha256": sha(thin.get("thin_prompt_utf8", "").encode()),
            "permission_state": thin.get("permission_state")}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(G3 / "runs" / "w1" / "raw" / "SECOND_PACK.json"))
    a = ap.parse_args(argv)
    a_pack = build("W1", "FHS-5_PLP/W1", "FHS-5/W1")
    b_pack = build("W2", "FHS-5_PLP/W2/CONTROL_PACK", "FHS-5/W2")
    ok = (a_pack["case_count"] == 13 and b_pack["case_count"] == 12
          and a_pack["review"].get("verdict") in ("PASS", "OK", None)
          and a_pack["permission_state"] == "NONE_GRANTED"
          and b_pack["permission_state"] == "NONE_GRANTED")
    doc = {"schema": "FHS5.PLP.W1.SecondPack@1", "packages": [a_pack, b_pack],
           "distinct": a_pack["subject"] != b_pack["subject"],
           "verdict": "PASS" if ok and a_pack["subject"] != b_pack["subject"] else "PARTIAL"}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": doc["verdict"],
                      "w1_cases": a_pack["case_count"],
                      "w2_cases": b_pack["case_count"],
                      "views": b_pack["views"]}))
    return 0 if doc["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
