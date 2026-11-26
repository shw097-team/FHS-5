#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import shutil


def load(p):
    return json.load(open(p, encoding="utf-8-sig"))


def dump(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = a.out
    for sub in ("fixtures", "oracles"):
        dst = os.path.join(out, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a.owner, sub), dst)
    refs = []
    for name in sorted(os.listdir(os.path.join(out, "fixtures"))):
        if not name.endswith(".json"):
            continue
        cid = name[:-5]
        fx = load(os.path.join(out, "fixtures", name))
        orc = load(os.path.join(out, "oracles", name))
        refs.append({
            "case_id": cid, "kind": fx.get("kind"), "wp": fx.get("wp"),
            "fixture": {"path": "fixtures/" + name,
                        "sha256": __import__("hashlib").sha256(open(os.path.join(out, "fixtures", name), "rb").read()).hexdigest(),
                        "bytes": os.path.getsize(os.path.join(out, "fixtures", name))},
            "oracle": {"path": "oracles/" + name,
                       "sha256": __import__("hashlib").sha256(open(os.path.join(out, "oracles", name), "rb").read()).hexdigest(),
                       "bytes": os.path.getsize(os.path.join(out, "oracles", name))},
            "contract_ref": fx.get("contract_ref"),
        })
    man = {
        "schema": "FHS5.PLP.W3.SourceManifest.NF@2",
        "identity": {"project_id": "FHS-5_PLP", "wave_id": "W3",
                     "subject_id": "FHS-5_PLP/W3/PRODUCT", "scope": "W3-NF-01",
                     "artifact_id": "FHS5-PLP/W3/PRODUCT-REAL-20261126", "version": "real-r1"},
        "selection_state": "PRODUCT_CASE_SET_CASE_OWNER_FROZEN",
        "profile": "GENERIC_NATIVE_FIRST",
        "case_refs": refs,
        "case_count": len(refs),
        "case_owner": "separate Case Owner session",
        "domain_scope": "GENERIC_NATIVE_PROJECTION_NOT_ORIGINAL_DOMAIN",
    }
    dump(os.path.join(out, "05_W3_SOURCE_MANIFEST.json"), man)
    shutil.copy2(os.path.join(a.owner, "CASE_OWNER_FREEZE.json"),
                 os.path.join(out, "CASE_OWNER_FREEZE.json"))
    print(json.dumps({"cases": len(refs)}))


if __name__ == "__main__":
    main()
