#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OPS receiver: verifies the adopted pack, parses/uses it, and atomically
creates a binding receipt plus material under an authorised output root.

It performs no DEV write and no git operation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--lib", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--runid", required=True)
    ap.add_argument("--result", required=True)
    ap.add_argument("--admission")
    a = ap.parse_args(argv)
    sys.path.insert(0, a.lib)
    import g3pack  # noqa: E402

    t0 = time.time()
    out = Path(a.out).resolve()
    adm = None
    if a.admission and Path(a.admission).is_file():
        try:
            adm = json.loads(Path(a.admission).read_text(encoding="utf-8"))
        except Exception:
            adm = None
    if not adm or str(adm.get("grant_state") or "") != "ISSUED":
        result = {"argv": sys.argv, "cwd": str(Path.cwd()), "run_id": a.runid,
                  "exit": 2, "error": "NOT_ADMITTED: no ISSUED external admission"}
        Path(a.result).write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n",
                                  encoding="utf-8", newline="\n")
        print(json.dumps({"exit": 2, "error": "NOT_ADMITTED"}))
        return 2
    result = {"argv": sys.argv, "cwd": str(Path.cwd()), "run_id": a.runid,
              "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    try:
        v = g3pack.verify_pack(a.pack)
        if not v["ok"]:
            raise RuntimeError("PACK_REJECTED:" + ",".join(v["errors"][:3]))
        p = v["pack"]
        cases = [{"case_id": c["case_id"], "kind": c.get("kind"),
                  "fixture": c.get("fixture"), "oracle": c.get("oracle")}
                 for c in p.cases]
        first = p.cases[0]["case_id"]
        fx = p.fixture(first)
        receipt = {
            "schema": "FHS5.PLP.W2.BindingReceipt@1",
            "run_id": a.runid,
            "subject": "FHS-5_PLP/W2/CONTROL_PACK",
            "source_subject": p.identity["subject_id"],
            "scope": p.identity["scope"],
            "candidate": p.candidate,
            "pins": {"manifest_sha256": v["manifest_sha256"],
                     "tree_sha256": v["tree_sha256"],
                     "case_set_sha256": v["case_set_sha256"]},
            "parsed": {"files": v["counts"]["files"], "assets": v["counts"]["assets"],
                       "cases": v["counts"]["cases"],
                       "first_case": first, "first_fixture_sha256":
                       sha((p.root / p.cases[0]["fixture"]).read_bytes())},
            "readback": {"fixture_case": fx.get("case_id"), "fixture_kind": fx.get("kind")},
            "host": {"host_id": hashlib.sha256(os.environ.get("COMPUTERNAME", "UNKNOWN").encode()).hexdigest()[:12],
                     "principal": "principal-" + hashlib.sha256(os.environ.get("USERNAME", "UNKNOWN").encode()).hexdigest()[:16],
                     "os": sys.platform,
                     "python": sys.version.split()[0],
                     "policy_epoch": None,
                     "epoch_state": "NOT_DECLARED_BY_HOST",
                     "epoch_probe": "no host policy service; recorded as not declared"},
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
        material = {"schema": "FHS5.PLP.W2.EffectMaterial@1",
                    "cases": cases,
                    "files": p.files,
                    "assets": p.assets}
        target = out / "OPS-A"
        if target.exists():
            raise RuntimeError("TARGET_ALREADY_EXISTS")
        out.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix=".tmp-", dir=str(out)))
        (tmp / "w2_binding_receipt.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8", newline="\n")
        (tmp / "w2_effect_material").mkdir()
        (tmp / "w2_effect_material" / "material.json").write_text(
            json.dumps(material, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8", newline="\n")
        os.replace(tmp, target)
        result.update({"exit": 0, "receipt": receipt, "material_sha256":
                       sha((target / "w2_effect_material" / "material.json").read_bytes()),
                       "receipt_sha256": sha((target / "w2_binding_receipt.json").read_bytes()),
                       "elapsed_ms": int((time.time() - t0) * 1000)})
    except Exception as exc:  # noqa: BLE001
        result.update({"exit": 2, "error": f"{type(exc).__name__}: {exc}"[:400]})
    Path(a.result).write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8", newline="\n")
    print(json.dumps({"exit": result.get("exit"),
                      "receipt_sha256": result.get("receipt_sha256")}))
    return result.get("exit", 2)


if __name__ == "__main__":
    sys.exit(main())
