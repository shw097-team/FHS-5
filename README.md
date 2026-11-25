# FHS-5｜Current: W0-NF CODEX-first validated

最新交付：`13_W0_NF_CODEX_20261125`（B0_NF_VALIDATED／W0_NF_VALIDATED；44 receipts；Challenge 31 checks）與 final delivery 目錄 `10_FINAL_DELIVERY/FHS-5_PLP_W0_NF_CODEX_20261125_01`。

歷史：`12_B0_NF_CODEX`（B0 representative／W0 partial）。

---

# FHS-5_PLP W0 — Control Pack, Closeout and Evidence

## W1 — Author Control Pack and Execution Evidence

`W1/` contains the owner-authorized W1 public reference export: 15 normative files, 16 sources, 13 fixtures/oracles, S0–S6 execution evidence, a 67-item ECP/TQAEP closure matrix, 14 named holds, and an executable author reference adapter.

Status: `AUTHOR_LOCAL_EXECUTION_COMPLETE_WITH_14_NAMED_HOLDS`; claim ceiling `AUTHOR_DESIGN_ONLY`; not Original Acceptance.

Start at [`W1/README.md`](W1/README.md).

This is the owner-authorized **public reference export** of the FHS-5_PLP W0 execution. It is a **HANDOFF_CANDIDATE**, not Original Acceptance.

## Start here

1. `closeout/FHS-5_PLP_W0_CLOSEOUT.md` — full closeout, promotion, verification, holds.
2. `closeout/FHS-5_PLP_W0_CLOSEOUT_FOR_W1_W4.md` — single-MD W1–W4 handoff package.
3. `closeout/PRIMARY_SELECTION_PUBLIC.json` — human-owner primary selection (public derivative).
4. `primary/` — 15 normative files (10 MD + 5 JSON) + 13 body-resolver sources + evidence appendix + review report.
5. `evidence/` — harness, self-check, closure matrices, trace/changed verification, guard/ACL/discovery summaries.

## Identity

| Field | Value |
|---|---|
| project_id | `FHS-5_PLP` |
| subject_id | `FHS-5_PLP/W0` |
| selection_id | `W0-PRIMARY-SEL-20261124-01` |
| source_manifest_sha256 | `22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f` |
| package_file_manifest_sha256 | `bcb93066f2f0c3841d7ee05c3cc306f0ab74a88512381e5ee99f0badb6887a4b` |
| public primary manifest tree | `81c235ba69105b654c8853ef5e46390dc4bc1c378c566c8b92f9887854b453e5` |
| claim | `AUTHOR_CONTROL_PACK_CANDIDATE_PASS_WITH_HOLDS` / `AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS` |

## Status

| Slice | Status |
|---|---|
| W0-A | `W0-A_CASE_SELECTION` / `OWNER_DESIGNATION_REQUIRED`（6 candidates；G4 runnable；legacy SQS candidate） |
| W0-B | `NOT_ADMITTED`（13 original-domain prerequisites UNBOUND） |
| W0-C | `LEDGER_COMPLETE`（1011/1011；485/485 ToolNeed IDs；all UNVERIFIED；0 install） |

## Verification snapshot

- harness 18/18; self-check 22/22
- challenge 7/7; audit 11/11（2 original actions open）
- pack 28/28; TQAEP 24/24; ACL 13/13; guard 10/0/1; mutations 6/6; G4 3 tests OK

## Important boundaries

- Original Reader / Issuer / OS Principal / Repo-Host Admission / Runner / Protected Checker / Publisher are `UNBOUND`.
- The 24 `F5-W0-T01..T24` cases are `CASE_UNBOUND`.
- T4/T5 formal transition is `HOLD_CR-DOC04-STATE-MAP`.
- This repository is not a license grant or original acceptance; see `NOTICE.md`.
- No credentials, raw ACLs, or raw external path inventories are included.

