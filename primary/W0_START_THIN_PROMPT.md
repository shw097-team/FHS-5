<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# W0_START_THIN_PROMPT

## 身份與效力

| 欄 | 值 |
|---|---|
| project_id | `FHS-5_PLP` |
| subject_id | `FHS-5_PLP/W0` |
| scope | `W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED` |
| wave_id | `W0` |
| batch_id | `W0-CODEX-REPAIR-20261123-01` |
| source_manifest_sha256 | `22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f` |
| claim_ceiling | `AUTHOR_DESIGN_ONLY` |
| author_label | `AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS` |
| review_mode | `AUTHOR_REVIEW_ONLY` |

## 契約摘要

Input: `SOURCE_MANIFEST.json`、`00_WAVE_RUN_MANIFEST.json`、`01_SOURCE_SCOPE_AND_CONSTRUCTION.md`、`02_ORIGINAL_CONTRACT_REFS.json`。
Operation: 先確認六身份與 Source，再決定 W0-A READ/DRAFT；W0-B 只回 NOT_ADMITTED；W0-C 只做適用性。
Output: Source-bound READ/DRAFT 候選，或具名 HOLD/Resume。
Consumer: Original Executor、Guide、Bridge、Case Owner。
NEG: 不新增 Scope、不簽 Grant、不跑 Native、不以 W0M 代替 W0。
FirstFail: SOURCE_OR_AUTHORITY_DRIFT / NOT_ADMITTED / CASE_UNBOUND。

## 可執行主選

本版由 Human Owner 選為可執行主選：`selection_id=W0-EXEC-SEL-20261124-01`、`authority_kind=HUMAN_OWNER_SELECTION_NOT_ORIGINAL_ISSUER`。先讀 `00_WAVE_RUN_MANIFEST.json.execution_selection` 與外部 selection receipt；W0-A/C 可在本地 owner-authorized lane 執行，W0-B 只回 `NOT_ADMITTED_ORIGINAL_DOMAIN`。若 W0-A 缺真非 FHS Case，回 `W0-A_CASE_SELECTION`，不要造案例。


## 啟動指令

讀取本包的 `SOURCE_MANIFEST.json`、`00_WAVE_RUN_MANIFEST.json`、`01_SOURCE_SCOPE_AND_CONSTRUCTION.md` 與 `02_ORIGINAL_CONTRACT_REFS.json`。若六身份一致且來源 bytes/SHA 正確，只可進行 W0-A 的受權 `SOURCE_READ` 或隔離 `ISOLATED_DRAFT_WRITE`；若缺真非 FHS Case，回 `W0-A_CASE_SELECTION`，不要造案例。

W0-B 在任何缺 Original OperationType/Repo/Host/ECP/Issuer/WorkOrder/Admission 的情況下直接回 `NOT_ADMITTED`。W0-C 只建立 FHS ID 適用性帳，不強裝 485，不縮原 ID 分母。

## Stop

來源 SHA/bytes 不符、path 逃逸、六身份不一致、claims 有 true、或 Original receipt 是字串冒充，立即停止受影操作並記 `PACKAGE_INTEGRITY_HOLD`／`FALSE_AUTHORITY`。

## Resume

只由 Original Owner 提供同 Subject/Scope/Host/PolicyEpoch 的 typed Source/Reader/Issuer/Checker 收據；本包不自行解除 HOLD，也不新增第二 Gate。
