# FHS-5_PLP_W0_CLOSEOUT_FOR_W1_W4

> **Single-MD handoff package.** W1–W4 should read this MD first, then open the primary selection and primary manifest. The candidate is retained as LastGood; do not use it as authority.

## 0. Entry Contract

| 欄 | 值 |
|---|---|
| package_id | `FHS-5_PLP_W0_W1W4_HANDOFF-20261124-01` |
| primary_selection | `W0-PRIMARY-SEL-20261124-01` |
| primary_root | `10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY` |
| primary_manifest | `10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY/PRIMARY_MANIFEST.json` |
| primary_manifest_tree | `f27263d8e0894fcbf897e38b050dcc894d8873860f7e00271aa30a4c6f5f9446` |
| source_manifest_sha256 | `22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f` |
| package_file_manifest_sha256 | `bcb93066f2f0c3841d7ee05c3cc306f0ab74a88512381e5ee99f0badb6887a4b` |
| claim_ceiling | `HANDOFF_CANDIDATE`（not Original Acceptance） |
| T4/T5 formal transition | `HOLD_CR-DOC04-STATE-MAP` |
| original domain | `UNBOUND` |

W1–W4 must enter from `PRIMARY_SELECTION.json` + `PRIMARY_MANIFEST.json`. The `FHS-5_PLP_W0_REPAIRED_CANDIDATE` root is history/LastGood only.

## 1. Six Identities

`project_id=FHS-5_PLP`; `subject_id=FHS-5_PLP/W0`; `scope=W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED`; `wave_id=W0`; `batch_id=W0-CODEX-REPAIR-20261123-01`; `source_manifest_sha256=22eebb6c…`.

## 2. 15-File Contract

| File | Bytes | SHA-256 |
|---|---:|---|
| `SOURCE_MANIFEST.json` | 6835 | `22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f` |
| `PACKAGE_FILE_MANIFEST.json` | 5706 | `bcb93066f2f0c3841d7ee05c3cc306f0ab74a88512381e5ee99f0badb6887a4b` |
| `00_WAVE_RUN_MANIFEST.json` | 35150 | `527bc8fda1f09549022b14a32e0c80426657dbdddc2b041af2e21fc5d63131d0` |
| `00_WAVE_RUN_MANIFEST.md` | 5790 | `656e5d3245d99427014c0a0fd98a0223d52c96b3aeb5f517d58210ff33b0aba6` |
| `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | 9312 | `b38d390c8b72d227fbead24a4c4daecf3a9620d63de19cc0bc9153bdc13551c2` |
| `02_ORIGINAL_CONTRACT_REFS.json` | 1571 | `81d4090227038d8ebbfde63307fb220357d76964d37bb73c7dbc602ed96bcce6` |
| `03_DEV_ECP.md` | 5219 | `f86e35e955eac119ab5cbffe9b8c669436608c716c474384e99031e2cdea7f89` |
| `04_OPS_ECP.md` | 4998 | `92131ad43685ae2fc12289f7e15778e7c48442007d50715026f861dbc6975353` |
| `05_PLANNED_TQAEP.json` | 32038 | `c7a2eb493bcf0bd795756f1f0bb124a7fa5b544a213a5440448f6d83c9549177` |
| `05_PLANNED_TQAEP.md` | 8175 | `88ca6d0c7d85b06936c00bd1c4a5073b08cfc6305c200a5cdc331ba61b9ce5bc` |
| `06_PERMISSION_STOP_RESUME.md` | 5189 | `04f5d51f2114c8e90b549f94a02e847174f69910ab80c5dd6cd02429fa31a48c` |
| `07_EVIDENCE_AND_CHECKER.md` | 3878 | `b11f359bf3cff10c6643998bceb698219e53bc839970a3a7021b3d42fdbfd85c` |
| `08_AS_BUILT_AND_HANDOFF.md` | 3689 | `4bb54b5f86aab647833b7ac10f5726f481ddcf0977399aa0e94974ced96e9413` |
| `09_README_RUN_ORDER.md` | 3559 | `22f776d382264188497c72ed72bd3285eb47a2ed7a0090b6f6cd0388cf8b2491` |
| `W0_START_THIN_PROMPT.md` | 2795 | `0629179ff67516384e01c86990587d5eba405e079e66c6adf9175b49ee11c305` |

13 body-resolver sources are under `.../sources/`. `PACKAGE_FILE_MANIFEST.json` has 27 entries and excludes itself; `SOURCE_MANIFEST` has 13 sources with bytes/lines/SHA.

## 3. W0 Closeout Summary

| Slice | Status |
|---|---|
| W0-A | `W0-A_CASE_SELECTION` / `OWNER_DESIGNATION_REQUIRED`; 6 candidates; G4 3 tests OK; SQS case+oracle |
| W0-B | `NOT_ADMITTED`; 13 prerequisites UNBOUND |
| W0-C | `LEDGER_COMPLETE`; 1011/1011; 485/35/56; all UNVERIFIED |

Verification: harness 18/18; self-check 22/22; challenge 7/7; audit 11/11; pack 28/28; TQAEP 24/24; ACL 13/13; trace 276/275; changed 261; scripts 31; guard 10/0/1; mutations 6/6.

## 4. Named Holds

| HOLD |
|---|
| `W0-A_CASE_SELECTION` |
| `W0-B_NOT_ADMITTED` |
| `ORIGINAL_READER_UNBOUND` |
| `ORACLE_FIXTURE_UNBOUND` |
| `HOST_CAPABILITY_UNBOUND` |
| `CHECKER_PUBLISHER_UNBOUND` |
| `SOURCE_REFERENCE_HASH_CONFLICT` |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` |

## 5. W1–W4 Write-back Protocol

Each wave returns `FHS5_Wn_WRITEBACK.json`:

| Field | Required |
|---|---|
| `schema` | `FHS5.PLP.Wn.Writeback@local-1` |
| `wave_id` | `W1` / `W2` / `W3` / `W4` |
| `subject_id` | `FHS-5_PLP/Wn` |
| `source_manifest_sha256` | re-pinned; never reuse W0 without re-read |
| `base_primary_selection` | `W0-PRIMARY-SEL-20261124-01` |
| `candidate_sha256` | frozen candidate |
| `changed_artifacts[]` | path, bytes, SHA |
| `tests[]` | command, exit, raw SHA, oracle, NOT_RUN |
| `holds[]` | FirstFail, owner, resume predicate |
| `original_actions[]` | reader/issuer/checker/publisher/release |
| `claim_ceiling` | `AUTHOR_DESIGN_ONLY` or lower |
| `owner` | wave author |

W1–W4 must not: create a second writer/issuer/queue/checker/publisher; turn W0 author claims into Original Reader ACK; use W4 Release as a W0 precondition; install 485 tools into the Generic lane; self-sign independent acceptance.

## 6. Wave Entry / Exit

| Wave | Entry | Exit (author) |
|---|---|---|
| W1 | W0 primary selection + source re-pin + W1 scope | W1 candidate + write-back + tests/holds |
| W2 | W1 write-back + affected scope | W2 candidate + write-back + tests/holds |
| W3 | W2 write-back + FHS profile applicability | W3 candidate + write-back + profile ledger |
| W4 | W3 write-back + original Checker/Publisher path | W4 release candidate; Release only by Original Publisher |

## 7. Do-Not-Assume

- W0 is not `PI_READY / PD_BOUND / EXECUTION_ADMITTED / NATIVE_PASS / INDEPENDENT_PASS / RELEASED`.
- W0-A E2E is not run; W0-B is not admitted; W0-C is not adjudicated.
- The 24 `F5-W0-T01..T24` cases are `CASE_UNBOUND`.
- The 15 files are the author control pack, not original canonical PIPD.

## 8. Artifact Index

- `10_FINAL_DELIVERY/PRIMARY_SELECTION.json`
- `10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY/PRIMARY_MANIFEST.json`
- `10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY/PRIMARY_DELIVERY_INDEX.json`
- `10_FINAL_DELIVERY/FHS-5_PLP_W0_CLOSEOUT.md`
- `10_FINAL_DELIVERY/FHS5_W0_MISSION_HANDOFF.json`
- `10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY/FHS-5_PLP_W0_證據型附錄.md`
- `10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY/FHS-5_PLP_W0_驗收審查與修補定案報告.md`

**Final:** `HANDOFF_CANDIDATE`; W1–W4 may start read-only write-back planning; Original acceptance remains with the original domain.
