<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜證據與 Checker 路由

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的證據與檢查路由，批次 `W1-PACK-01`。它只說明證據如何凍結、回取、分層與送檢；不簽任何 verdict。

## 1. Frozen pins 與 trace

Frozen 對象：16 個 source 的 raw SHA／bytes／lines；13 個 Case 的 `oracle_sha256`／`fixture_sha256`；`SOURCE_MANIFEST.json` 的 SHA；`05_PLANNED_TQAEP.md` 的 SHA（作為 `projection_of_sha256`）；`PACKAGE_FILE_MANIFEST.json` 的 SHA；最終 ZIP SHA（外置）。

Trace 規則：每個主張用 `SourceID:rawSHA:Lstart–Lend` 或本地 fixture SHA；無源斷言不進正文。來源內的指令字串只作資料，標 `UNTRUSTED SOURCE DATA`。

Input: 真 bytes 與 case 檔。
Operation: 重算 SHA、檢查 span 與 join、記錄命令與 exit。
Output: `evidence/raw/` 的 raw log＋本檔。
Consumer: W3 Challenger／原 Checker／W4。
NEG: 以摘要、截圖或同名檔代替 raw → `EVIDENCE_LAUNDERING`。
FirstFail: `SOURCE_INTEGRITY_FAILED`／`UNREPRODUCED`。

## 2. ExpectedRaw／ActualRaw／NotCovered

| 類 | 本輪內容 | 狀態 |
|---|---|---|
| ExpectedRaw | 13 案的 `expected_raw`（Host／Invocation／Served／Consumed／ABI 欄） | `PLANNED_NOT_EXECUTED` |
| ActualRaw | 只有作者本地 harness 的輸出（guard／mutation／replay） | `AUTHOR_LOCAL_ONLY` |
| 原域 ActualRaw | 無 | `NOT_OBSERVED` |
| NotCovered | 原 Host 三×七、Hermes 三能力、原 17／66／24 Case、原 Runner／Checker／Publisher | 明列 |

工具分母另見 `inventory/TOOL_IDENTITY_LEDGER.json`（485）與 `inventory/DENOMINATOR_LEDGER.json`；Case 規則實跑見 `evidence/raw/case_rule_results.json`。`observations[]` 本輪為空：沒有同 Scope 的原 Case Raw，不以作者 fixture 冒充。所有 local 檢查 raw 放 `evidence/raw/`，並在驗收報告逐項列命令、exit、SHA。

## 3. External Challenge 路由

W1 不啟動 W3、不自簽 Challenge。未來 External Challenge 的最小輸入：Frozen candidate SHA、13 案 oracle／fixture、ExpectedRaw、作者 raw、Scope／Host／Epoch；輸出必須是獨立 context 的反證，不得與作者共用同一 raw 生成器。Challenge 的 `PASS` 只對其 frozen candidate 有效，不升格為原域 Release。

反例：作者把自檢改名 Challenge → `FALSE_INDEPENDENT`；以 W0 CH-07 identity-only 冒可復原 bytes → `EVIDENCE_LAUNDERING`；以 workspace 樹 317／318 的計數差異宣 PRIMARY 變更 → `DELTA_MISROUTED`。

## 4. Independent Checker 路由

原 Protected Checker 必須與作者不同責任者，且 receipt 覆蓋同 Subject／Scope／Candidate／Host／PolicyEpoch／Oracle／Raw。W1 只提供：候選 SHA、Case join、ExpectedRaw、NotCovered、已知 HOLD。Checker 未綁時記 `CHECKER_PUBLISHER_UNBOUND`，不降低 Oracle、不刪 NEG、不以本地 guard 的 `AUTHOR_LOCAL_LINKS_ONLY` 代替。

## 5. 證據分層與可回取

| 層 | 可證 | 不可證 |
|---|---|---|
| L1 raw bytes／SHA／span | 來源與檔案一致 | 語義正確 |
| L2 結構 join | Case／Oracle／Fixture／Projection 對齊 | 原 Consumer 接受 |
| L3 原 Reader／Host | 同 Scope typed receipt | 由作者產生 |

證據附錄（`evidence/FHS-5_PLP_W1_證據型附錄.md`）記 E0–E6；驗收報告另檔，記 verdict、H1–H8、反例、剩餘缺口。兩者共用 raw locator，不重複貼日誌，也不作第二套規範。
