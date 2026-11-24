<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 09_README_RUN_ORDER

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

Input: 本包 15 檔、13 個來源副本、W0M candidate-v2 與可用的 Original Reader。
Operation: 按需讀取，先 Source/Scope，再 OriginalRef/ECP，才路由 Guide/Bridge/Challenge/FAR。
Output: 合法 READ/DRAFT，或明確 HOLD/Resume。
Consumer: Codex、Hermes、Guide、Bridge、Case Owner、Executor。
NEG: 未讀 Source/Scope 直接執行；把 W0M 當 W0 15 檔；日常 READ 強制跑全五方。
FirstFail: PACKAGE_INTEGRITY_HOLD / NOT_ADMITTED / ORIGINAL_READER_UNBOUND。

## 可執行入口

1. 讀 `00_WAVE_RUN_MANIFEST.json.execution_selection` 與外部 `W0_EXECUTABLE_PRIMARY_SELECTION.json`，確認 `selection_id=W0-EXEC-SEL-20261124-01`。
2. 讀 `SOURCE_MANIFEST.json` / `00` / `01` / `02`；六身份、來源 bytes/SHA 與 `human_owner_selection_ref` 必須一致。
3. W0-A：可做受權 `SOURCE_READ`／隔離 `ISOLATED_DRAFT_WRITE`；無真非 FHS Case 時回 `W0-A_CASE_SELECTION`。
4. W0-B：看到 `NOT_ADMITTED_ORIGINAL_DOMAIN` 即停；不得以 Owner 選擇代替 Original Issuer/Repo/Host/Admission。
5. W0-C：只做 FHS ID 適用性；不宣 485 Fit。


## 按需讀序

1. `SOURCE_MANIFEST.json`：先確認 13 個來源的真 bytes/lines/SHA 與 `SELECTED_ONLY`。
2. `00_WAVE_RUN_MANIFEST.md/json`：確認六身份、A/B/C、claims 全 false。
3. `02_ORIGINAL_CONTRACT_REFS.json`：確認原 PI/PD/ECP/TQAEP/Oracle/Issuer 全部 null/UNBOUND。
4. `01_SOURCE_SCOPE_AND_CONSTRUCTION.md`：讀 W0-A 八步、W0-B Runbook、W0-C、14 WP、7 Seam。
5. `03_DEV_ECP.md`／`04_OPS_ECP.md`：B 線無 Admission 即停；不要把它們當 Grant。
6. `05_PLANNED_TQAEP.md/json`：讀 24 Case 原句/行號/ExpectedRaw；不要當實跑 Raw。
7. `06_PERMISSION_STOP_RESUME.md`／`07_EVIDENCE_AND_CHECKER.md`／`08_AS_BUILT_AND_HANDOFF.md`／`W0_START_THIN_PROMPT.md`：找 Owner/Stop/Resume 與交接。

## 停止規則

來源 SHA/bytes 不符、path 逃逸、六身份不一致、TQAEP projection 不一致、FileManifest digest 不符、claims 有任何 true、或 Original receipt 被字串冒充，立即 `PACKAGE_INTEGRITY_HOLD`／`FALSE_AUTHORITY`。

## Consumer 路由

Guide 只消費 WaveControl/ThinStart；Bridge 只消費 Source span 與四 API Context；Executor 只消費原 Admission 與 ECP；Challenge 只消費 Frozen Candidate；FAR 只消費 Challenge Raw；Original Checker/Publisher 只由其原域簽署。不要把同一份作者檔送給所有 Consumer 當成已核准。

## 日常 READ

日常 `SOURCE_READ` 不必每次跑 Guide/Bridge/Challenge/FAR 全五方；只有受影 Slice 才需要相應 Raw。需要 DRAFT 時只寫隔離輸出根；需要 DEV/OPS 時必須先有原 Admission。
