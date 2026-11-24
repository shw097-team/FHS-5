<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 08_AS_BUILT_AND_HANDOFF

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

Input: 原候選、修補 Finding、重驗 Raw、W0M/原 Reader 狀態與下游 W1M–W4M 接口。
Operation: 記錄真實做了什麼、沒做什麼、LastGood、受影 Delta 與下一波交接。
Output: 可讀的 As-Built、Delta 與 Handoff 候選。
Consumer: Program Owner、W1M–W4M Author、Original Consumer。
NEG: 把文件完成當 Native 完成、把 W0 15 檔當已執行、或把 W4 Release 倒灌 W0。
FirstFail: EXPECTED_NOT_OBSERVED / DELTA_UNBOUND / PHASE_OVERREACH_CANDIDATE。

## 可執行定案

| 項目 | 值 |
|---|---|
| final_pack | `FHS-5_PLP_W0_EXECUTABLE_FINAL` |
| selection_id | `W0-EXEC-SEL-20261124-01` |
| status | `PRIMARY_EXECUTABLE_SELECTION` |
| W0-A | `EXECUTABLE_ROUTE_SELECTED` |
| W0-B | `NOT_ADMITTED_ORIGINAL_DOMAIN` |
| W0-C | `EXECUTABLE_APPLICABILITY_SELECTED` |
| Original Reader/Issuer/Runner/Checker/Publisher | `UNBOUND`／`NOT_RUN` |

本定案版以 `FHS-5_PLP_W0_REPAIRED_CANDIDATE` 為 LastGood 基礎；只新增 selection 與執行入口，不改原 Source/Case/Oracle/Threshold，也不把 W0-B 升格為原域可執行。


## As-Built

| 項目 | 本輪作者 As-Built | 原域狀態 |
|---|---|---|
| 15 檔 | 已物化、可重新讀取、六身份一致 | 非 Canonical |
| 13 來源副本 | 已 copy 並重算 bytes/lines/SHA | `SELECTED_ONLY`，非 CORE16 |
| W0-A | 八步路由、Guide/Bridge/Challenge/FAR 條件 | `CASE_UNBOUND` |
| W0-B | DEV/OPS ECP 設計與第一最小 Effect Runbook | `NOT_ADMITTED` |
| W0-C | 22/36/50/39/96/192/485、35/56 的適用性帳 | `APPLICABILITY_PLANNED` |
| 本地 Guard | M §22 Guard 跑到 oracle 邊界；等價 Guard 檢查結構 | `AUTHOR_REVIEW_ONLY` |
| Native/Independent/Release | 未執行 | `NOT_RUN`／`NOT_CLAIMED` |

## LastGood

LastGood 是本 15 檔 + 13 個來源副本 + 證據附錄的 hash-stable 版本。逐檔 bytes/SHA 見 `FHS-5_PLP_W0_證據型附錄.md` 的 E6 交付索引；不在本檔重複嵌入會循環的自身 digest。

## Delta

本輪只有**文件級 Delta**：來源 manifest 改為可回取相對路徑與 `coverage_claim`；WaveControl 補齊 Guard 需要的 claims/receipt 欄；24 Case 改為 M §12.7 的精確行號與原句；TQAEP projection 與 cases 同值；ECP/OPS/TQAEP/權限/證據各檔補實質。沒有 Repo/Host/Native/WorldRaw Delta。

## W1M–W4M 交接

後續 W1M–W4M 只接受本包的受影 Source/Scope/Effect 與具名 HOLD；不得把 W0 15 檔當已 Native 執行，不得把 W1–W4 的 Release 當 W0 READ 前件。W0-A/C 的作者候選可在 `WITH_NAMED_HOLDS` 下交接；W0-B 必須等原 Admission。

## 標籤

本輪標籤：`AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS`。不是 `PI_READY`、`PD_BOUND`、`EXECUTION_ADMITTED`、`NATIVE_PASS`、`INDEPENDENT_PASS` 或 `RELEASED`。
