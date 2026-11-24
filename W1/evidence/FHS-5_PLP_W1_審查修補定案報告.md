# FHS-5_PLP W1｜審查修補定案報告

- TaskID：`FHS5-W1-CODEX-REPAIR-20261124-v1`｜Subject：`FHS-5_PLP/W1/CONTROL_PACK`｜Batch：`W1-PACK-01`
- 基線：`FHS5_W1_AUTHOR_20261124_v1`（保留，不覆寫）
- 修補候選：`FHS-5_PLP_W1_REPAIRED_CANDIDATE`
- Claim ceiling：`AUTHOR_DESIGN_ONLY`；最終狀態：**`AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS`**
- 這不是原域准入、Native PASS、Independent PASS 或 Release；原 Reader／Issuer／Checker／Publisher 仍各自裁決。

## 1. 基線→最終裁決

基線審查（`W1_REVIEW_20261124_v1`）為 `REVIEW_AFFECTED_HOLD / REPAIR_REQUIRED`，12 項本地缺陷（1×P1、5×P2、6×P3）。本輪已完成所有可在本地解決的缺陷；沒有把 FAIL 改名 HOLD、沒有刪 oracle／分母、沒有降低 claim。

| 項目 | 基線 | 最終 |
|---|---|---|
| 本地 verdict | `REVIEW_AFFECTED_HOLD` | `REPAIR_COMPLETE_LOCAL` |
| 交付狀態 | `AUTHOR_CONTROL_PACK_CANDIDATE_PASS_WITH_NAMED_HOLDS` | `AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS` |
| P1 缺陷 | 2 處失效引用 | 0 |
| P2 缺陷 | 5 | 0 |
| P3 缺陷 | 6 | 0（全部修正或改為可回取證據） |
| 規範檔 | 15/15 | 15/15（同固定檔名與版本身份） |
| 來源 | 16 | 16（未改） |
| Case | 13 | 13（9 可執行規則、4 POS 待原執行器） |
| FileManifest | 56 | 58（新增 2 個 inventory 帳） |
| Guard | 555 checks | 671 checks |
| Harness 反例 | 10/10 | 17/17 |
| 原域 HOLD | 13 | 14（補回 `HOLD_CR-DOC04-STATE-MAP`） |

## 2. Finding → 根因 → 最小修補 → 重驗

| ID | 基線缺陷（first-fail） | 根因 | 最小修補 | 重驗 |
|---|---|---|---|---|
| F-01 P2 | 6 處「17 源」vs manifest 16（`SOURCE_COUNT_TEXT_MISMATCH`） | 封存後回寫未同步計數 | 6 處改 16；guard 加全文計數檢查 | `w1_guard` 671 checks；`H9_source_count_text` 被拒 |
| F-02 P1 | `check/replay.py` 不存在；`raw/host_probe.txt` 未產（`FileNotFoundError`） | 改名／刪檔未回寫 | 改 `replay_hashes.py`；實際產生 host probe（CONTAINER_ONLY） | 引用存在檢查通過；`doc_ref_exists` 0 FAIL |
| F-03 P2 | 刪 REQ/FR 列、截斷 clause、反轉 kind、漂移 first_fail 皆可通過 | guard 以存在／計數代替集合等價 | exact clause（w1＋m22）、REQ/FR 各恰一次、kind 圖、oracle first_fail 對讀、w1 duplicate-key loader | 新增 5 突變全拒；harness 17/17 |
| F-04 P2 | 56/35/485/22/36/50/39/96/192 無逐項 disposition | 以彙總數字代替身份帳 | 485 全 ID ledger＋23 族 denominator ledger＋01 §9／07 引用 | 485/485、23 族；10 W1 受影／217 W0-C／258 W2–W4 |
| F-05 P2 | fixture 只有 statement，不可執行 | 把「有檔／有 pin」當 fixture 實質 | 9 案加 `request`／`predicate`／`expect_error`；13 oracle 加 procedure；新增 `run_cases.py` | 9 executed／9 PASS／4 NOT_RUN（POS 未被 NEG 抵帳） |
| F-06 P3 | 「Seam」0 次；namespace 未標版本；DAG 未 typed | 架構索引缺漏 | 01 §5.1 七 Seam 表、三個 Guide `@proposal-2`、Bridge `@-2/-4`；01 §4 typed DAG | 7 seam 列、5 namespace 標籤；guard 檢查通過 |
| F-07 P3 | seal aggregate 不可重現；索引漏 2 raw | 人手補欄／索引未更新 | seal 記演算法並重算；索引列全部 raw | 見 `DELIVERY_SEAL.json` 與 §6 |
| F-08 P3 | 附錄 4 列行數錯（289/21/192/92） | 舊版數字未更新 | 改 194/13/185/112 | 與 manifest lines 一致 |
| F-09 P3 | 06 缺單人多角色條件 | 只寫「不可自動成為」 | 加 Policy/SoD `RoleBinding` 條件與 `ORIGINAL_POLICY_UNBOUND` | 06 可回取；不影響 SoD |
| F-10 P3 | `host_claims` 把 SKILL_BYTES／TOOL_CALLS 放 observation | 階段欄與本地證據混用 | observation 改 `NOT_OBSERVED`，另設 `local_evidence` | guard 檢查 local_evidence ⇒ observation=NOT_OBSERVED |
| F-11 P2 | 作者報告把 H3/H8 標 PASS_LOCAL | 自評未隨缺陷更新 | 本報告重評，不以自檢代原域 | 見 §4 |
| F-12 P3 | `HOLD_CR-DOC04-STATE-MAP` 未進 holds | 只在 D08 一句 | holds／06 表補第 14 筆 | 14 HOLD；guard 檢查存在 |

## 3. A–F 覆蓋（同一 trace）

| 軸 | 結果 | 證據／界線 |
|---|---|---|
| A 來源／身份／封裝 | `PASS_LOCAL` | 16 源 byte 相同；15 檔固定名；10 MD header、TQAEP projection、58 筆 FM、ZIP 條目一致 |
| B 原意／功能／完整性 | `PASS_LOCAL` | 16 REQ、17 FR、9＋3 child、13 Case（clause 逐字）、24 W0（8 UPDATE／16 RETAIN） |
| C ABI／鏈路 | `DESIGN_READY` | 四 API 名稱／參數、七 Seam、五 namespace、四 digest 各自 preimage；無原 Consumer 接受 |
| D Program／治理 | `PASS_LOCAL` | typed DAG 無循環；W0-B 只 `deferred_to_wave(W2)`；W4 `post_acceptance`；無自創全域 Gate |
| E 施工／可達性 | `PARTIAL` | 本地 READ／DRAFT／rule check 可做；Bridge 實作、Host loader、Repo ACL 未綁 |
| F 檢測／交付 | `PASS_LOCAL`（本地） | 671 checks、REPLAY_OK、17/17 反例、9/9 可執行 Case、ZIP 重定位讀回 |

## 4. H1–H8

| 群組 | 判定 | 說明 |
|---|---|---|
| H1 Source/W0 | `PASS_LOCAL` | 16 源、W0 33/34、receipt stale、27 entries、13 sources 全部重現；附錄行數已修 |
| H2 Pack／機器契約 | `PASS_LOCAL` | 15 檔、58 entries、六身份、projection、case join、全 SHA；17/17 突變拒收 |
| H3 Trace／覆蓋 | `PASS_LOCAL` | 16＋17＋24＋13＋6＋5＋9＋3 全在位；REQ/FR 各恰一次；clause exact |
| H4 ABI／BodyResolver | `DESIGN_READY`／`NOT_RUN` | 七 Seam、namespace、四 API、四 digest、BodyResolver 規則；無真 adapter |
| H5 安全 | `PASS_LOCAL` | traversal、dup key、symlink、scope drift、fake claim/receipt、注入字串皆拒 |
| H6 Effect／Host／claim | `PASS_LOCAL`（claim）／`HOLD`（Host） | claims/receipts 正確；21 格、9＋3 child；工具 485 帳；Host 仍未觀測 |
| H7 Program／收斂 | `PASS_LOCAL` | typed DAG、stop/resume/lastgood、14 HOLD；無全局 Gate |
| H8 交付／Claim | `PASS_LOCAL` | 逐檔讀回、索引、ZIP、外置 seal、重定位；無封存後漂移 |

## 5. 移除的過治理與保留的真安全前件

**移除／避免**：沒有新增 Queue、Issuer、Checker、Publisher、第二 Writer 或固定全域 Gate；沒有要求 13 個原 HOLD 全清零；沒有把 1011／485 當 W1 Fit；沒有把 W0-B 或 W4 倒卡 W1 作者閉合；沒有把 skill 可讀升格為 Host 階段。

**保留的真安全前件**：Source pin／SHA、strict JSON／UTF-8、path containment、symlink／junction 拒絕、`UNTRUSTED SOURCE DATA`、DEV／OPS 分離、OPS 不用 `git revert`、Protected Checker 獨立、`claims` 全 false、receipt null、T4/T5 DOC04 HOLD。

## 6. 封存、ZIP 與可重現

- 封存順序：來源（未變）→ 六 identity → 正文修正 → TQAEP MD → TQAEP JSON 投影／cases → WaveControl cases → FileManifest（58，不含自身）→ 索引 → ZIP → 外置 seal。
- 外置 seal 的 `package_manifest_aggregate_sha256` 演算法：對 `PACKAGE_FILE_MANIFEST.json` 的 `files[]` 做 canonical JSON（`sort_keys=True`、`separators=(",",":")`、UTF-8）後 SHA-256；演算法與 preimage 寫入 `DELIVERY_SEAL.json`，可重算。
- ZIP 不含自身與 seal；索引不含自身或 ZIP digest。最終解包到新目錄，15 檔與離線依賴齊全，重跑 w1／m22／replay／run_cases 全 exit 0。
- Reviewer sidecar：`plp-tpm-review 1.0.1` 的 `review_core.py` 以 `PLP.REVIEW.REQUEST@2` 真執行，回 `REVIEW_SOURCE_LOCATED_ONLY`、`defects 0`、`unbound 81`、exit 0；sidecar 存於 `evidence/reviewer_sidecar/review-12f3062e70d45a226b1c0495/`。`authority_state=UNBOUND` 如實保留。第一次 request 手寫 polarity 產生的 9 筆 `POLARITY_DRIFT` 經核為 request 啟發式 artifact，移除呼叫方 polarity 後重跑為 0 defects，不列為包缺陷。

## 7. 可立即施工的 scope 與第一個合法操作

| 可立即做（不需新原域准入） | 第一個操作 | 產出 |
|---|---|---|
| Source READ／pin 核對 | `python check/replay_hashes.py --root FHS-5_PLP_W1_REPAIRED_CANDIDATE` | REPLAY_OK raw |
| 結構／身份／projection 自檢 | `python check/w1_guard.py --pack-root ... --delivery-root .` | 671 checks |
| 作者規則 fixture 執行 | `python check/run_cases.py --pack-root ...` | 9/9 PASS、4 NOT_RUN |
| Guide／Bridge Context 作者 adapter | 按 01 §5–§7 建 request／response，不寫 Repo | Context 候選；`W1_ABI_BOUND` 保留 |
| DEV／OPS 契約準備 | 按 03／04 填 preimage／WriteSet／HostID／Principal／Epoch | 可審 ECP 草稿；`NOT_ADMITTED` |

**需原域准入**：任何 Repo 寫入（DEV）、Host 安裝／註冊／綁定／啟動（OPS）、使用者資料效果（USER）、發布（RELEASE）。最小解除分別是：Repo Owner 的 live HEAD／ACL／WriteSet＋ExecutionAdmission；Host Owner／OS Principal 的 HostID／loader／installer／Epoch＋Host Admission；原 Publisher receipt。Protected Checker 必須是 distinct 執行者。

## 8. 剩餘 HOLD 與未覆蓋

14 具名 HOLD：`W1_HOST_NINE_GRID`、`W1_PLUGIN_ALIAS`、`W1_ABI_BOUND`、`W1_W0_INPUT`、`W0_PRIMARY_RECEIPT_STALE`、`W0-A_CASE_SELECTION`、`W0-B_NOT_ADMITTED`、`ORIGINAL_READER_UNBOUND`、`ORACLE_FIXTURE_UNBOUND`、`HOST_CAPABILITY_UNBOUND`、`CHECKER_PUBLISHER_UNBOUND`、`SOURCE_REFERENCE_HASH_CONFLICT`、`W0C_DENOMINATOR_ID_LIST_UNBOUND`、`HOLD_CR-DOC04-STATE-MAP`。

未覆蓋：三 Host 七階段真 Raw、Hermes 三能力、原 17 Guide／66 Bridge／24 W0 執行、原 Runner／Checker／Publisher、package-first 全鏈 dry-consume、W2–W4 施工、CH-07 舊 bytes 復原。以上皆不得由本輪本地結果推導為 PASS。

## 9. 邊界聲明

本報告是**作者端修補與本地自檢**，不是 Independent 或 Original Acceptance。審查階段（read-only）與作者修補階段的責任分離仍成立；本輪沒有代替原 Writer 簽 canonical，也沒有代替原 Checker 簽 verdict。任何「已可施工」只指控制包足以讓後續原 Executor 依合法 scope 操作，不代表已准入或已執行。

`AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS`
