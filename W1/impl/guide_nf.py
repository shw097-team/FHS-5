#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 NF-r2 Guide (four original functions + four NF adapters).

Original names are preserved and crosswalked to NF names in function form:

  inspect_guide_request(req, root)                 <-> receive_package(pack_ref, root)
  select_bounded_advice(ctx, req)                  <-> select_advice(view, mode, evidence)
  render_thin_prompt(ctx, advice)                  <-> render_thin(prompt_view)
  reconcile_guide_delta(before, after, verifier)   <-> compare_material(before, after)

Two modes: PACKAGE_FIRST (enough real body -> thin prompt directly) and
CONTEXT_AUGMENTED (only fill missing context; never widen scope).

Nine-key dual-period verdict:
  DELTA_UNVERIFIED | NEW_SUBJECT_REVIEW_REQUIRED | NEW_MATERIAL_EVIDENCE |
  PARK_NO_DELTA

Every nine-key value must be produced by a registered producer that reads a
real artefact (file / receipt / git output).  A caller boolean, a single
evidence_sha or an absent period is never accepted.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import body_resolver as br
import bridge_nf as bridge
import tpm_contracts_nf as tpm
import w1_nf_reader as base

NFError = base.NFError

NINE_KEYS = ["subject", "scope", "source_sha", "repo_head", "host_id",
             "policy_epoch", "oracle_sha", "world_raw_sha", "first_fail"]

MODES = ("PACKAGE_FIRST", "CONTEXT_AUGMENTED")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


# ------------------------------------------------------------------ producers
def _p_subject(ctx: dict) -> str | None:
    return (ctx.get("identity") or {}).get("subject_id")


def _p_scope(ctx: dict) -> str | None:
    return (ctx.get("identity") or {}).get("scope")


def _p_source_sha(ctx: dict) -> str | None:
    return ctx.get("pack_manifest_sha256")


def _p_repo_head(ctx: dict) -> str | None:
    ref = ctx.get("repo_head_file")
    if ref and Path(ref).is_file():
        return Path(ref).read_text(encoding="utf-8").strip() or None
    root = ctx.get("repo_root")
    if root and Path(root, ".git").exists():
        try:
            out = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                                 capture_output=True, text=True, timeout=30)
        except Exception:
            return None
        return out.stdout.strip() if out.returncode == 0 else None
    return None


def _p_host_id(ctx: dict) -> str | None:
    ref = ctx.get("host_id_file")
    if ref and Path(ref).is_file():
        try:
            obj = json.loads(Path(ref).read_text(encoding="utf-8"))
        except Exception:
            return None
        return obj.get("host_id") or obj.get("host")
    return None


def _p_policy_epoch(ctx: dict) -> str | None:
    ref = ctx.get("policy_file")
    if ref and Path(ref).is_file():
        try:
            obj = json.loads(Path(ref).read_text(encoding="utf-8"))
        except Exception:
            return None
        return obj.get("policy_epoch")
    return None


def _p_oracle_sha(ctx: dict) -> str | None:
    ref = ctx.get("oracle_file")
    if ref and Path(ref).is_file():
        return sha256_file(Path(ref))
    return None


def _p_world_raw_sha(ctx: dict) -> str | None:
    ref = ctx.get("world_raw_file")
    if ref and Path(ref).is_file():
        return sha256_file(Path(ref))
    return None


def _p_first_fail(ctx: dict) -> str | None:
    if "first_fail" not in ctx:
        return None
    v = ctx.get("first_fail")
    if v is None:
        return "NONE"
    return v if isinstance(v, str) else None


PRODUCERS = {
    "subject": _p_subject,
    "scope": _p_scope,
    "source_sha": _p_source_sha,
    "repo_head": _p_repo_head,
    "host_id": _p_host_id,
    "policy_epoch": _p_policy_epoch,
    "oracle_sha": _p_oracle_sha,
    "world_raw_sha": _p_world_raw_sha,
    "first_fail": _p_first_fail,
}


def produce_nine_keys(ctx: dict) -> dict:
    out = {}
    for k in NINE_KEYS:
        try:
            out[k] = PRODUCERS[k](ctx)
        except Exception:
            out[k] = None
    return out


# ------------------------------------------------------- package / thin prompt
def inspect_guide_request(req: dict, root: str) -> dict:
    """CG-R2-REQ-01: receive real package bytes / sha / subject / scope."""
    declared = req.get("expected_manifest_sha256")
    r0 = Path(root)
    cands = sorted(p.name for p in r0.glob("*SOURCE_MANIFEST*.json"))
    if not cands:
        raise NFError("PACK_INCOMPLETE_LOCAL", "no manifest")
    insp = bridge.inspect_package(str(r0 / cands[0]), root, expected_sha256=declared)
    if req.get("subject_id") and req["subject_id"] != insp["subject_id"]:
        raise NFError("SOURCE_IDENTITY_HOLD", "request subject != package subject")
    if req.get("scope") and req["scope"] != insp["scope"]:
        raise NFError("CONTEXT_SCOPE_MISMATCH", "request scope != package scope")
    if req.get("claim_over_package") is True and req.get("claim_kind") != "read":
        raise NFError("FALSE_AUTHORITY", "request claim tries to upgrade package")
    r = br.canonical_root(root)
    man_name = sorted(p.name for p in r.glob("*SOURCE_MANIFEST*.json"))[0]
    man, _ = br.load_json_strict(br.resolve_inside(r, man_name), man_name)
    wi = {"project_id": man["project_id"], "subject_id": man["subject_id"],
          "scope": man["scope"], "wave_id": man["wave_id"],
          "batch_id": man["batch_id"], "work_id": "GUIDE-RECEIVE"}
    contracts = tpm.build_contracts(str(r), wi)
    pi = contracts["views"]["PI"]
    thin = _thin_nav(r)
    return {
        "schema": "FHS5.PLP.W1.GuideReceive@1",
        "package_state": "RECEIVED_ACTUAL",
        "subject_id": insp["subject_id"],
        "scope": insp["scope"],
        "manifest_sha256": insp["manifest_sha256"],
        "manifest_bytes": insp["manifest_bytes"],
        "source_refs_count": len(insp["source_refs"]),
        "goal": pi["goal"],
        "fuo": pi["fuo"],
        "done": pi["done"],
        "effect": contracts["views"]["PD"]["effect_class"],
        "owner": pi.get("owner") or contracts["views"]["PD"].get("owner"),
        "next": thin.get("next"),
        "stop": thin.get("stop"),
        "resume": thin.get("resume"),
        "contract_profile": contracts["profile"],
        "permission_state": "NONE_GRANTED",
    }


def _thin_nav(root: Path) -> dict:
    """Derive next/stop/resume from the frozen thin-start section, not constants."""
    out = {}
    candidates = sorted(root.glob("04_*.md"))
    if not candidates:
        return out
    text = br.decode_utf8(br.read_bounded(candidates[0], candidates[0].name),
                          candidates[0].name)
    for key, marker in (("next", "## NEXT"), ("stop", "## STOP"),
                        ("resume", "## RESUME")):
        on = False
        for line in text.splitlines():
            if line.strip().startswith(marker):
                on = True
                continue
            if on and line.strip():
                out[key] = line.strip().lstrip("- ").strip()[:400]
                break
    return out


def select_bounded_advice(ctx: dict, req: dict) -> dict:
    """CG-R2-REQ-07/08/12: advice never becomes a grant or a work order."""
    if req.get("requested_effect") not in (None, "READ", "DRAFT"):
        raise NFError("EFFECT_UNBOUND", str(req.get("requested_effect")))
    evidence = ctx.get("evidence") or {}
    mode = ctx.get("mode")
    if mode not in MODES:
        raise NFError("MODE_UNKNOWN", str(mode))
    if not evidence:
        raise NFError("DELTA_UNVERIFIED", "no evidence")
    unknown = [k for k in ("policy_epoch", "oracle_sha") if not evidence.get(k)]
    if unknown and mode == "PACKAGE_FIRST":
        advice_state = "ADVICE_WITH_DECLARED_GAPS"
    else:
        advice_state = "ADVICE_BOUND"
    return {
        "schema": "FHS5.PLP.W1.GuideAdvice@1",
        "mode": mode,
        "advice_state": advice_state,
        "advice": ["read the frozen pack", "run the four APIs", "record raw per case"],
        "declared_gaps": unknown,
        "permission_state": "NONE_GRANTED",
        "advice_is_grant": False,
        "scope_echo": ctx.get("identity", {}).get("scope"),
    }


def render_thin_prompt(ctx: dict, advice: dict) -> dict:
    """CG-R2-REQ-06: a single plain-text thin START; no secrets, no scope growth."""
    ident = ctx.get("identity") or {}
    scope = advice.get("scope_echo")
    if scope and scope != ident.get("scope"):
        raise NFError("CONTEXT_SCOPE_MISMATCH", "advice scope != context scope")
    lines = [
        "# W1 thin start (generated)",
        "",
        "- subject: " + str(ident.get("subject_id")),
        "- scope: " + str(ident.get("scope")),
        "- mode: " + str(advice.get("mode")),
        "- permission_state: NONE_GRANTED",
        "- advice_is_grant: false",
        "",
        "## next bounded steps",
    ]
    for a in advice.get("advice") or []:
        lines.append("- " + a)
    text = "\n".join(lines) + "\n"
    if re.search(r"(?i)api[_-]?key\s*[:=]|ghp_[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY", text):
        raise NFError("SECRET_OR_ESCAPE", "thin prompt would embed a secret")
    return {
        "schema": "FHS5.PLP.W1.GuideThin@1",
        "thin_prompt_utf8": text,
        "thin_prompt_sha256": sha256_bytes(text.encode("utf-8")),
        "permission_state": "NONE_GRANTED",
        "scope_echo": ident.get("scope"),
    }


# --------------------------------------------------------------- delta compare
def reconcile_guide_delta(before: dict, after: dict, original_verifier=None) -> dict:
    """Nine-key dual-period reconcile; caller bool / single SHA never suffice."""
    if not before or not after:
        return _delta_unverified("missing period")
    verifier_receipt = None
    if original_verifier is not None:
        if not callable(original_verifier):
            return _delta_unverified("verifier not callable")
        try:
            verifier_receipt = original_verifier(before, after)
        except Exception as exc:
            return _delta_unverified(f"verifier raised: {type(exc).__name__}")
        if not isinstance(verifier_receipt, dict) or verifier_receipt.get("verified") is not True:
            return _delta_unverified("verifier did not verify")
    if before.get("caller_verified") or after.get("caller_verified"):
        return _delta_unverified("caller boolean is not verification")
    kb = produce_nine_keys(before)
    ka = produce_nine_keys(after)
    missing = [k for k in NINE_KEYS if kb.get(k) is None or ka.get(k) is None]
    if missing:
        return _delta_unverified("missing keys: " + ",".join(missing))
    if kb["subject"] != ka["subject"] or kb["scope"] != ka["scope"]:
        return {
            "schema": "FHS5.PLP.W1.GuideDelta@1",
            "state": "NEW_SUBJECT_REVIEW_REQUIRED",
            "before": kb, "after": ka,
            "changed_keys": [], "single_evidence_sha": False,
            "verifier_receipt": verifier_receipt,
        }
    changed = [k for k in NINE_KEYS if kb[k] != ka[k]]
    if not changed:
        return {
            "schema": "FHS5.PLP.W1.GuideDelta@1",
            "state": "PARK_NO_DELTA",
            "candidate": True,
            "note": "nine keys identical; PARK is a candidate, not an automatic close",
            "before": kb, "after": ka, "changed_keys": [],
            "verifier_receipt": verifier_receipt,
        }
    return {
        "schema": "FHS5.PLP.W1.GuideDelta@1",
        "state": "NEW_MATERIAL_EVIDENCE",
        "before": kb, "after": ka,
        "changed_keys": changed,
        "changed_detail": {k: {"before": kb[k], "after": ka[k]} for k in changed},
        "verifier_receipt": verifier_receipt,
    }


def _delta_unverified(reason: str) -> dict:
    return {"schema": "FHS5.PLP.W1.GuideDelta@1", "state": "DELTA_UNVERIFIED",
            "reason": reason, "changed_keys": []}


def compare_material(before: dict, after: dict) -> dict:
    return reconcile_guide_delta(before, after)


# ------------------------------------------------------------------- CLI glue
def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("keys")
    a.add_argument("--ctx", required=True)
    a.add_argument("--out")
    b = sub.add_parser("delta")
    b.add_argument("--before", required=True)
    b.add_argument("--after", required=True)
    b.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "keys":
            ctx, _ = br.load_json_strict(Path(args.ctx))
            out = {"nine_keys": produce_nine_keys(ctx), "keys": NINE_KEYS}
        else:
            before, _ = br.load_json_strict(Path(args.before))
            after, _ = br.load_json_strict(Path(args.after))
            out = reconcile_guide_delta(before, after)
    except NFError as exc:
        sys.stdout.write(json.dumps({"result": "REJECT", "token": exc.token,
                                     "detail": exc.detail}, ensure_ascii=False, indent=2) + "\n")
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if getattr(args, "out", None):
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
