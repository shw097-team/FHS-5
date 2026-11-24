<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 00_WAVE_RUN_MANIFEST

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

## 可執行主選（Human Owner）

| 欄 | 值 |
|---|---|
| selection_id | `W0-EXEC-SEL-20261124-01` |
| status | `PRIMARY_EXECUTABLE_SELECTION` |
| selected_by | `HUMAN_OWNER` |
| selected_at | `2026-11-24` |
| authority_kind | `HUMAN_OWNER_SELECTION_NOT_ORIGINAL_ISSUER` |
| execution_lane | `OWNER_AUTHORIZED_LOCAL_W0_A_C` |
| W0-A | `EXECUTABLE_ROUTE_SELECTED`（真非 FHS Case 未得時仍回 `W0-A_CASE_SELECTION`） |
| W0-B | `NOT_ADMITTED_ORIGINAL_DOMAIN` |
| W0-C | `EXECUTABLE_APPLICABILITY_SELECTED` |
| original_domain_receipts | `null` |

本版是新版 W0 十五檔的**可執行主選**。這是 Human Owner 的本地選擇，不是 Original Issuer、OS Principal、Repo/Host Admission、Protected Checker 或 Publisher 的收據；W0-B 仍必須等原域 Admission。外部 selection receipt 為 `W0_EXECUTABLE_PRIMARY_SELECTION.json`。


## 契約摘要

Input: task-pinned W0 sources, W0M candidate-v2 and the original W0 15-file candidate.
Operation: review the original candidate, repair only a new output copy, re-run affected checks and hand off an author candidate.
Output: the repaired 15-file W0 pack, a byte-identical source set, an evidence appendix and a review report.
Consumer: Guide, Bridge, Original Executor, Case Owner, Checker and Publisher.
NEG: fake Reader/Issuer/Host/Grant, using W0M as W0, or claiming Native PASS without an original runner.
FirstFail: SOURCE_OR_AUTHORITY_DRIFT / NOT_ADMITTED / CASE_UNBOUND / PACKAGE_INTEGRITY_HOLD.

## 波次目標與 FUO

本波要讓既有的 Guide／Bridge／受權 Codex／Hermes 能只靠本包讀懂：W0-A 何時可合法 READ/DRAFT、W0-B 為何在缺原 Admission 時必須停止、W0-C 如何保留 FHS Profile 原 ID 分母。FUO 是「可讀、可定位、可停止、可恢復」的作者控制候選，不是原域實跑。

## A/B/C Slice

| Slice | 本波作者狀態 | 允許 | 不可宣稱 |
|---|---|---|---|
| W0-A Generic READ/DRAFT | `CASE_UNBOUND`；八步路由與停止點已寫 | 受權來源的 `SOURCE_READ`、隔離 `ISOLATED_DRAFT_WRITE` | 未取得真非 FHS Case/Oracle/Runner 前，不宣 E2E 完成 |
| W0-B Native Reversible | `NOT_ADMITTED` | 只保留條件式 Runbook 與 ECP 設計 | 不執行 DEV/OPS，不簽 WorkOrder/Admission |
| W0-C FHS Regression | `APPLICABILITY_PLANNED` | 只做 ID 適用性、分母與 Owner 記帳 | 不宣 485/485 Fit，不把 Generic 強綁 FHS Gate |

## Success 與 Nonclaim

Success：15 個規範檔與 13 個來源副本可重新讀取；六身份一致；每個 `F5-W0-T01..24` 有原 M §12.7 的精確行號與原文；W0-B 明確 `NOT_ADMITTED`；W0-A/C 有可交接的條件與具名 HOLD。

Nonclaim：`PI_READY`、`PD_BOUND`、`EXECUTION_ADMITTED`、`NATIVE_PASS`、`INDEPENDENT_PASS`、`RELEASED`。本輪審查是 `AUTHOR_REVIEW_ONLY`，不是原 Independent Acceptance。

## 十五檔清單

| # | 檔案 | 類型 | 本輪角色 |
|---|---|---|---|
| 1 | `SOURCE_MANIFEST.json` | JSON | 13 個選定來源的真 bytes/lines/SHA 與可回取副本 |
| 2 | `PACKAGE_FILE_MANIFEST.json` | JSON | 其餘 14 個規範檔與 13 個來源副本的 digest；不含自身 |
| 3 | `00_WAVE_RUN_MANIFEST.json` | JSON | WaveControl、六身份、24 Case、claims 與 unbound 狀態 |
| 4 | `00_WAVE_RUN_MANIFEST.md` | MD | 本檔：波次目標、Slice、Success/Nonclaim |
| 5 | `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | MD | W0-A 八步、W0-B Runbook、W0-C、14 WP、7 Seam |
| 6 | `02_ORIGINAL_CONTRACT_REFS.json` | JSON | 原 PI/PD/ECP/TQAEP/Oracle/Issuer 的 null 與 UNBOUND |
| 7 | `03_DEV_ECP.md` | MD | DEV 設計、Pre/Post、WriteSet、Readback、Recovery |
| 8 | `04_OPS_ECP.md` | MD | OPS 設計、Host/Principal/Epoch、WorldRaw、Host recovery |
| 9 | `05_PLANNED_TQAEP.md` | MD | 24 Case 的原句、行號、ExpectedRaw 與 Checker 狀態 |
| 10 | `05_PLANNED_TQAEP.json` | JSON | MD 的真 SHA 投影與同值同序 cases |
| 11 | `06_PERMISSION_STOP_RESUME.md` | MD | READ/DRAFT/DEV/OPS/USER/RELEASE 分權與具名 Resume |
| 12 | `07_EVIDENCE_AND_CHECKER.md` | MD | Frozen/Expected/Actual Raw、Challenge/FAR、SoD |
| 13 | `08_AS_BUILT_AND_HANDOFF.md` | MD | As-Built、LastGood、Delta、W1M–W4M 交接 |
| 14 | `09_README_RUN_ORDER.md` | MD | 給 Codex/Hermes 的按需讀序 |
| 15 | `W0_START_THIN_PROMPT.md` | MD | 同六身份的極薄啟動指引 |

## 責任、拒收與 No-Global-Gate

- 作者只對新輸出根負責；原始 M/B00–B05/WM/W0M/CTRL/START 與原候選保持唯讀。
- Single Human Owner 不是 Original Issuer、OS Principal、Case Runner 或 Checker；不得以人類授權字串補造原域回執。
- 無真非 FHS Case 只停 W0-A 的 E2E，不停 W0-A/C 的作者文件交付；無 W0-B Admission 只停 B，不倒灌 W1–W4 或 Release。
- 不以 W4 Release 作 W0 READ 前件，不以同一 Effect 的 WorldRaw 作自身 Admission 前件，不新增第二 Writer/Issuer/Queue/Checker/Publisher。
