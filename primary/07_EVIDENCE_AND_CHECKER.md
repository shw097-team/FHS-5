<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 07_EVIDENCE_AND_CHECKER

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

Input: Frozen Candidate、Oracle/Fixture、Evidence bytes、command/exit/stdout/stderr、WorldRaw 與 Checker 角色。
Operation: 把 Expected 與 Actual 分帳，保存可重播 Raw；沒有 Raw 時只記 NOT_RUN/UNREPRODUCED。
Output: 可追溯的 evidence ledger、Challenge/FAR 狀態與 SoD 限制。
Consumer: External Challenger、FAR、Original Checker、Consumer。
NEG: 文字總結冒充 command/exit/raw、UNAVAILABLE 填零、或作者自簽 Independent。
FirstFail: EVIDENCE_UNBOUND / UNREPRODUCED / ORACLE_DRIFT / FALSE_INDEPENDENT。

## Frozen Candidate

| 欄 | 本輪值 | 說明 |
|---|---|---|
| candidate_sha256 | `null` | 尚未有經原 Runner 凍結的 Candidate |
| oracle_sha256 | `null` | 24 原 Case 的 Oracle 未取得 |
| fixture_sha256 | `null` | 原 Fixture 未取得 |
| subject_id | `FHS-5_PLP/W0` | 六身份 |
| scope | `W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED` | 本包 Scope |
| freeze_state | `UNBOUND` | 只有作者文件，不是原 Frozen Candidate |

## Expected 與 Actual Raw

Expected：`05_PLANNED_TQAEP.json.cases[].expected_raw` 是 `PLANNED_NOT_EXECUTED` 的結構化物件，記預期 FirstFail/正確出口、M 行號與 Owner；它不是 Raw bytes。Actual：本輪沒有 Original Runner，全部 `null`/`NOT_RUN`；不得把作者表格或本地結構檢查當 Actual WorldRaw。

## Command / Exit / Raw

Original Runner 的 `command/exit/stdout/stderr/raw_sha256` 本輪全部 `NOT_RUN`。本輪實際執行的只有本地作者 Guard 與 `plp-tpm-review` 的唯讀 extraction；其 command/exit/output SHA 記在證據附錄 E3，且只代表本地審查，不代表原域執行。

## Challenge / FAR

Challenge：只有 POS/NEG/EDGE/SEC 計畫，沒有 Original Runner 或 Frozen Candidate，狀態 `UNREPRODUCED`。FAR：只保留 `RESEARCH_REQUIRED`／`WAIT`／`RESUME`／`PARK` 的 typed 設計；`UNAVAILABLE` 不填零，無真 Raw 不自報 `CLOSE`/`FIX_NOW`。

## Checker / SoD

Original Checker `UNBOUND`；作者與 Maker 不可自簽 Independent。只有原 Protected Checker 能在同 Subject/Candidate/Scope/Host/PolicyEpoch/FUO 下給出獨立結果；Publisher 才擁有 Release。本輪 `review_mode=AUTHOR_REVIEW_ONLY`，`INDEPENDENT_PASS` 不宣。

## Evidence Ledger

| 證據 | 狀態 | Owner | Resume |
|---|---|---|---|
| Original PI/PD/ECP/TQAEP reader | `UNBOUND` | Original PIPD Reader | typed receipt |
| Original Case/Oracle/Fixture | `UNBOUND` | Case/Oracle Owner | 真 bytes + SHA |
| Original Runner Raw | `NOT_RUN` | Executor/Host | command/exit/raw |
| Original Checker | `UNBOUND` | Protected Checker | 同 Candidate 獨立收據 |
| Publisher | `UNBOUND` | Publisher | 原發布門檻 |

## 不可冒稱

不得生成看似有效的 Checker receipt、Issuer grant、permit、Original Reader ACK 或 WorldRaw；不得把 `UNAVAILABLE` 當 `ZERO`；不得改 Oracle/Threshold 讓 FAIL 變綠；不得把本地 `PASS` 字串升格為原域 PASS。
