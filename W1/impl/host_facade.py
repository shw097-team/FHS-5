#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 NF-r2 host facade (7-stage ledger, anti-upgrade).

Stages: Selected -> Loaded -> Installed -> Bound -> Invoked -> ActualServed
-> Consumed.  Each stage needs its own class of evidence.  The facade refuses
to promote weaker evidence:

  skill bytes            -> never Loaded
  exit 0                 -> never ActualServed
  sha equal              -> never Consumed
  local probe            -> never Installed (use REASONED_NA_NATIVE_ENTRY)

It never installs, never serves and never claims a host the caller did not
actually observe.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import w1_nf_reader as base

NFError = base.NFError


class StageDenied(NFError):
    def __init__(self, token: str, detail: str = ""):
        super().__init__(token, detail)


STAGES = ["Selected", "Loaded", "Installed", "Bound", "Invoked", "ActualServed", "Consumed"]
HOSTS = ["CODEX", "GPT_CHAT", "GPT_WORK", "HERMES"]

REQUIRED_EVIDENCE = {
    "Selected": {"host_id", "version"},
    "Loaded": {"slots", "loaded_sha256"},
    "Installed": {"installer_ref", "version"},
    "Bound": {"binding_ref", "scope"},
    "Invoked": {"argv", "exit", "stdout_sha256", "stderr_sha256"},
    "ActualServed": {"served_bytes_sha256", "scope_echo", "served_at"},
    "Consumed": {"consumer_id", "consumed_sha256", "action", "readback_at"},
}

DENY_HINTS = {
    "Loaded": ("skill", "skill_bytes", "readme"),
    "Installed": ("probe", "local_probe", "container", "skill"),
    "Invoked": ("skill", "skill_bytes", "readme"),
    "ActualServed": ("exit0", "exit_zero", "hash"),
    "Consumed": ("hash_only", "sha_only", "manifest_hash"),
}


def ledger() -> dict:
    return {"schema": "FHS5.PLP.W1.HostLedger@1",
            "rows": {h: {s: "NOT_OBSERVED" for s in STAGES} for h in HOSTS},
            "evidence": {h: {} for h in HOSTS}}


def record(led: dict, host: str, stage: str, evidence: dict,
           available: bool = True) -> dict:
    if host not in HOSTS:
        raise StageDenied("UNKNOWN_HOST", host)
    if stage not in STAGES:
        raise StageDenied("UNKNOWN_STAGE", stage)
    if not available:
        led["rows"][host][stage] = "NOT_OBSERVED"
        return led
    if stage == "Installed" and evidence.get("reason") == "REASONED_NA_NATIVE_ENTRY":
        led["rows"][host][stage] = "REASONED_NA_NATIVE_ENTRY"
        led["evidence"][host][stage] = evidence
        return led
    missing = REQUIRED_EVIDENCE[stage] - set(evidence)
    if missing:
        raise StageDenied("EVIDENCE_INCOMPLETE", ",".join(sorted(missing)))
    kind = str(evidence.get("evidence_kind", "")).lower()
    for hint in DENY_HINTS.get(stage, ()):
        if hint in kind:
            token = {"Loaded": "HOST_PENDING", "Installed": "HOST_PENDING",
                     "Invoked": "HOST_PENDING",
                     "ActualServed": "SERVED_UNVERIFIED",
                     "Consumed": "CONSUMER_UNVERIFIED"}[stage]
            raise StageDenied(token, f"{stage} rejects evidence kind {kind}")
    prev = STAGES.index(stage) - 1
    if prev >= 0:
        prior = led["rows"][host][STAGES[prev]]
        if prior in ("NOT_OBSERVED", "NOT_RUN"):
            raise StageDenied("HOST_ABI_DRIFT", f"{stage} before {STAGES[prev]}")
    led["rows"][host][stage] = "OBSERVED_LOCAL"
    led["evidence"][host][stage] = evidence
    return led


def cross_host_claim(led: dict, as_host: str, stage: str) -> dict:
    """A stage observed for one host can never satisfy another host."""
    if led["rows"][as_host][stage] != "OBSERVED_LOCAL":
        raise StageDenied("HOST_ABI_DRIFT", f"{as_host}/{stage} not observed")
    others = {h: led["rows"][h][stage] for h in HOSTS if h != as_host}
    return {"host": as_host, "stage": stage, "observed": True, "substitutes": others}


def main(argv=None) -> int:
    ap_out = {
        "schema": "FHS5.PLP.W1.HostLedgerProbe@1",
        "stages": STAGES,
        "hosts": HOSTS,
        "note": "facade only records what the caller actually observed",
    }
    if len(sys.argv) > 1 and sys.argv[1] == "--stages":
        sys.stdout.write(json.dumps(ap_out, ensure_ascii=False, indent=2) + "\n")
        return 0
    sys.stdout.write(json.dumps(ap_out, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
