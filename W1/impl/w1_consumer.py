#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 NF-r2 independent consumer (D4 / O5).

Consumes real served bytes, performs one bounded observable task and returns
an action + readback.  A hash match alone is not consumption; exit 0 is not
served; served is not consumed.

Bounded tasks
  case-checklist : extract a frozen case row (requirement, POS, NEG, fixture
                   and oracle digests) into a scope-bound checklist
  clause-map     : extract one clause's ids, negatives and exceptions
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import body_resolver as br
import nf_reader as reader
import w1_nf_reader as base

NFError = base.NFError

CASE_LINE_RE = re.compile(r"^\|\s*`(W1-[A-Z0-9]+-\d{2})`\s*\|(.+)\|\s*$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _case_row(text: str, case_id: str) -> dict:
    for line in text.splitlines():
        m = CASE_LINE_RE.match(line.strip())
        if not m or m.group(1) != case_id:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) < 7:
            raise NFError("BODY_RESOLVER_UNBOUND", f"{case_id} row truncated")
        return {
            "case_id": case_id,
            "kind": cells[0],
            "requirement": cells[1],
            "pos": cells[2],
            "neg": cells[3],
            "fixture_sha256": cells[4].strip("`"),
            "oracle_sha256": cells[5].strip("`"),
        }
    raise NFError("CLAUSE_NOT_FOUND", case_id)


def consume(pack_root: str, task: str, target: str, expected_manifest_sha: str,
            out_dir: str, consumer_id: str = "w1-consumer-local",
            generic: bool = False) -> dict:
    root = br.canonical_root(pack_root)
    insp = reader.inspect_generic(root) if generic else reader.inspect_package(root)
    if expected_manifest_sha != insp["pack_manifest_sha256"]:
        raise NFError("SOURCE_INTEGRITY_FAILED", "manifest pin mismatch")
    ident = insp["identity"]
    if task == "case-checklist":
        text = br.decode_utf8(br.read_bounded(br.resolve_inside(root, "03_W1_TQAEP.md"),
                                              "03_W1_TQAEP.md"), "03_W1_TQAEP.md")
        row = _case_row(text, target)
        asset = {(a["case_id"], a["kind"]): a for a in insp["asset_refs"]}
        for kind in ("fixture", "oracle"):
            if asset[(target, kind)]["sha256"] != row[kind + "_sha256"]:
                raise NFError("ORACLE_DRIFT", f"{target}/{kind}")
        body = [
            "# bounded checklist: " + target,
            "",
            "- subject: " + ident["subject_id"],
            "- scope: " + ident["scope"],
            "- kind: " + row["kind"],
            "- requirement: " + row["requirement"],
            "",
            "## positive expectation",
            row["pos"],
            "",
            "## negative / first fail",
            row["neg"],
            "",
            "- fixture_sha256: " + row["fixture_sha256"],
            "- oracle_sha256: " + row["oracle_sha256"],
        ]
        action = "extract_case_checklist"
    elif task == "clause-map":
        exp = __import__("bridge_nf").explain_slice(str(root), "cases")
        hit = [s for s in exp["sections"] if target in s["heading"]]
        if not hit:
            raise NFError("CLAUSE_NOT_FOUND", target)
        s = hit[0]
        body = ["# clause map: " + s["heading"], "",
                "- path: " + s["path"],
                "- lines: " + str(s["line_start"]) + "-" + str(s["line_end"]),
                "- ids: " + ", ".join(s["ids"]),
                "- negatives: " + ", ".join(n["token"] for n in s["negatives"])]
        action = "extract_clause_map"
    elif task == "pack-summary":
        body = ["# pack summary: " + str(ident.get("scope")), "",
                "- profile: " + str(insp.get("profile")),
                "- pack_version: " + str(insp.get("pack_version")),
                "- pack_manifest_sha256: " + str(insp.get("pack_manifest_sha256")),
                "- pack_files: " + str(len(insp.get("file_refs") or [])),
                "- sources: " + str(len(insp.get("source_refs") or [])),
                "- capabilities: " + json.dumps(insp.get("profile_capabilities"), sort_keys=True)]
        action = "summarise_second_package"
    else:
        raise NFError("VIEW_UNKNOWN", task)
    out_text = "\n".join(body) + "\n"
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    target_file = out_path / ("consumed_" + re.sub(r"[^A-Za-z0-9_.-]", "_", target) + ".md")
    target_file.write_text(out_text, encoding="utf-8", newline="\n")
    back = target_file.read_text(encoding="utf-8")
    if back != out_text:
        raise NFError("CONSUMER_UNVERIFIED", "readback mismatch")
    return {
        "schema": "FHS5.PLP.W1.Consumed@1",
        "consumer_id": consumer_id,
        "consumer_kind": "independent-local-consumer",
        "subject": ident["subject_id"],
        "scope": ident["scope"],
        "scope_echo": ident["scope"],
        "action": action,
        "target": target,
        "served_sha256": insp["pack_manifest_sha256"],
        "consumed_sha256": sha256_bytes(out_text.encode("utf-8")),
        "consumed_bytes": len(out_text.encode("utf-8")),
        "readback_path": str(target_file),
        "readback_verified": True,
        "parsed_not_hashed_only": True,
        "permission_state": "NONE_GRANTED",
    }


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--task", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--expected-manifest-sha256", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--consumer-id", default="w1-consumer-local")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        res = consume(args.pack, args.task, args.target,
                      args.expected_manifest_sha256, args.out_dir, args.consumer_id)
    except NFError as exc:
        sys.stdout.write(json.dumps({"result": "REJECT", "token": exc.token,
                                     "detail": exc.detail}, ensure_ascii=False, indent=2) + "\n")
        return 2
    text = json.dumps(res, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
