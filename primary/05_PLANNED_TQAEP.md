<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 05_PLANNED_TQAEP

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

Input: M §12.7 L1010–L1039 的 24 個原 Case、原 Oracle/Fixture 狀態與 Checker 角色。
Operation: 把每個 Case 的注入、預期 FirstFail/正確出口、Owner 與來源行號編成可審的 TQAEP 計畫。
Output: 24 個 Case 的規劃表與 ExpectedRaw 結構；沒有 Raw 時明示 NOT_RUN/CASE_UNBOUND。
Consumer: Original Case Owner、Runner、Checker、Program/FAR。
NEG: 以作者表或本地 QA 冒充原 Runner；改 Oracle/Threshold 讓 FAIL 變綠。
FirstFail: RUNNER_UNBOUND / ORACLE_UNBOUND / CASE_UNBOUND / EVIDENCE_LAUNDERING。

Requirement: M §12.7 L1010–L1039，24 個 `F5-W0-T01..T24` 的原始注入、預期 FirstFail/正確出口與 Owner。

Case: 24 個 Case 逐 ID；每個 Case 使用原 M 表格的精確行號（L1014–L1037）與該行原文，不使用泛用模板或前輪摘要代替。

Oracle: 原 Case/Oracle/Fixture bytes 未取得；24 個 `oracle_path`/`oracle_sha256` 皆為 null，狀態 `ORACLE_UNBOUND`。本檔不發明原 Oracle。

POS: T01、T13、T24 的 POS 半；NEG: T02–T12、T14–T23、T24 的 NEG 半。

ExpectedRaw: 每個 Case 的 `expected_raw` 是結構化物件，`state=PLANNED_NOT_EXECUTED`、`raw_state=NO_ORIGINAL_RAW`；不是實跑 Raw。

Checker: Original CaseRunner/Checker `UNBOUND`；本輪只有 `AUTHOR_REVIEW_ONLY`，不宣 `INDEPENDENT_PASS`。

## 24 Case 規劃表

| Case | 類型 | 原行 | 注入／受審行為 | 預期 FirstFail／正確出口 | Owner | 狀態 |
|---|---|---|---:|---|---|---|
| `F5-W0-T01` | POS | L1014 | 真 Source SHA＋合法 READ W0 | SourceAnchor/Scope 正確，無新 OPS Gate | Source/Guide Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T02` | NEG | L1015 | 任意原 Source 改一 byte | `SOURCE_INTEGRITY_FAILED`，不得沿用舊 Trace | Source Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T03` | NEG | L1016 | 「A、B各有」缺 B 的 Case | Parent 不得全 PASS／開具名 Child 缺件 | TPM/PI Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T04` | NEG | L1017 | 呼叫者自造 OriginalID/Reader Ack 字串 | `ORIGINAL_READER_UNBOUND`，拒升格 | PIPD Reader | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T05` | NEG | L1018 | Guide Prompt 將 Scope A 擴為 Scope B | Source mismatch/Clarify，不能覆蓋 W0 原 Scope | Guide/Bridge | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T06` | SEC | L1019 | Bridge 使用 `../`/symlink escape/非法絕對路徑 | 不讀出 admitted root，不寫被審來源 | Bridge/Host Security | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T07` | EDGE | L1020 | Bridge legacy proposal-1 提交 proposal-2 consumer | `EXPLICIT_REVIEW_REQUIRED`，保留未知欄位 | Bridge Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T08` | NEG | L1021 | 有原 Code，但未 Host Bound | 分類 BIND/ACTIVATE，不假定 CODE_MISSING | Reviewer/FAR | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T09` | NEG | L1022 | 未來 W4 Release 反向當 W0 READ 前件 | 報 `PHASE_OVERREACH_CANDIDATE` | Program/PI Reader | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T10` | NEG | L1023 | 一操作的 WorldRaw 作同操作 Admission 前件 | `GATE_CYCLE_CANDIDATE` | Program/Checker | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T11` | NEG | L1024 | Caller `permit=true`／虛假 WorkOrder | 無原 Issuer Receipt → 不做 DEV/OPS | Issuer/Host | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T12` | NEG | L1025 | 未知 Effect token／相似命名 alias | `EFFECT_MAPPING_UNVERIFIED`，不默認 READ | Effect Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T13` | POS | L1026 | 受權 Native Slice 操作+真正 post-readback | 真 World/Repo effect SHA/Oracle 可觀察 | Original Runner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T14` | NEG | L1027 | CLI exit 0 但 WorldRaw 與 Oracle 不符 | 不標 Effect Verified | WorldReader/Checker | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T15` | NEG | L1028 | Challenge 修改原 Oracle/Threshold | Subject mutation 拒收、撤 Challenge Claim | External Challenger | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T16` | EDGE | L1029 | 不同 CandidateSHA 使用同 Challenge Raw | Frozen identity mismatch → re-challenge affected | Challenge Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T17` | NEG | L1030 | Challenger 只有文字總結，無 cmd/exit/raw | `UNREPRODUCED/NOT_PROVEN` | Challenge Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T18` | NEG | L1031 | FAR research 來源不可達但 `zero_results=true` | `UNAVAILABLE/BLOCKED/ERROR ≠ ZERO` | FAR/Original Fabric | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T19` | NEG | L1032 | FAR JSON 自報 `root_cause_claim=FIX_NOW`／CLOSE | 缺真 Original Reader/World Raw→`RESEARCH_REQUIRED` | FAR Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T20` | EDGE | L1033 | 兩期同 FirstFail 但新 Source/Oracle/Raw 存在 | 不能 PARK；依受影 Delta 重讀 | Program/FAR | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T21` | NEG | L1034 | 無新 Material Delta，反覆重新派相同 Case | `PARK_UNTIL_DELTA` **僅在真兩期證據成立時** | Program/WorldReader | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T22` | NEG | L1035 | 原 Checker/Publisher 仍缺，Guide 回 `CLOSE` | `CLOSEOUT_ADVICE` 不得 RELEASE | Original Checker/Publisher | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T23` | SEC | L1036 | 小包含密鑰／令牌且欲寫報告 | 敏感資訊遮罩，不外流 | Project Host/Security | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |
| `F5-W0-T24` | POS/NEG | L1037 | Generic 不載 FHS 485 仍完成合法 READ；FHS Profile 缺適用 ID | Generic READ 通；FHS 適用 ID 不得被省略 | Profile/Tool Owner | `CASE_UNBOUND`／`PLANNED_NOT_EXECUTED` |

## 執行語義

只有真正跑過的 Case 才能填 `command/exit/raw_sha256/reproduction`。本輪沒有 Original Runner、Original Oracle、Original Fixture 或 Protected Checker，因此所有 `F5-W0-T01..24` 一律 `PLANNED_NOT_EXECUTED`／`CASE_UNBOUND`。作者本地 QA 只覆蓋本包結構、來源 bytes、六身份、投影與檔案 digest，不能核銷原 Runner。

## 作者本地 QA 與原 Runner 分帳

| 層 | 本輪可觀察 | 不可升格 |
|---|---|---|
| 文件結構 | 15 檔存在、六身份一致、14 檔 FileManifest、TQAEP 投影 | 不是原 Case PASS |
| 來源 bytes | 13 個選定來源 copy 後 SHA/bytes/lines 重算 | 不是 Original Reader ACK |
| Case join | 24 個原 M 行號/原句可回取 | Oracle/Fixture/Runner 仍 UNBOUND |
| 原 Runner | 未執行 | `NATIVE_PASS`／`INDEPENDENT_PASS` 不宣 |

## T24 的雙極性

T24 原類型是 `POS/NEG`，本表保留 `kind=POS` 與 `kind_secondary=NEG`，不把 NEG 半丟失：POS 半是 Generic 在沒有 FHS 485 Gate 時仍可完成合法 READ；NEG 半是 FHS Profile 缺少適用 ID 時必須報 Profile FAIL。

## Stop / Resume

Stop：缺 Original Case/Oracle/Fixture bytes、缺 Original Runner、缺 Protected Checker，或試圖改 Oracle/Threshold 讓 FAIL 變綠。Resume：Original Case Owner 提供同 Subject/Scope 的 Case/Oracle/Fixture bytes 與 Runner；Original Checker 提供同 Candidate/Scope/Host/PolicyEpoch 的獨立收據。
