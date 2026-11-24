<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜權限、Stop 與 Resume

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的權限與停復正文，批次 `W1-PACK-01`。每個 Effect 的 Issuer、Admission、StopScope、Resume 與 UNKNOWN reconcile 分開列；不得用一個 `permission=true` 概括全部。

## 1. 角色與權力分層

| 角色 | 本輪是否持有 | 可做 | 不可做 |
|---|---|---|---|
| Human Owner | 是（任務授權） | 指定 scope、批准作者交付 | 自動成為 Issuer／OS Principal／Checker |
| Wave Curator／作者 | 是 | READ、隔離 DRAFT、LOCAL CHECK | 寫原 Repo／Host、簽 Independent |
| Original Issuer | `UNBOUND` | 發 WorkOrder／Admission | 由作者代簽 |
| OS Principal | `UNBOUND` | 在 Host 執行 OPS | 以本機 sandbox 用戶冒充 |
| Original Reader | `UNBOUND` | 讀回 canonical PI／PD | 由本地 pack 代替 |
| Protected Checker | `UNBOUND` | 出 Independent verdict | 由作者自檢代替 |
| Publisher | `UNBOUND` | Release | 由 MD SHA 代替 |

**單一自然人多角色的條件**：同一自然人可同時持有 Human Owner 與一個或多個原技術角色，**僅當**原 Policy／SoD 的 `RoleBinding` 明確允許，且該角色所需 Host／Scope／Epoch 前件齊備；未取得該判定時記 `ORIGINAL_POLICY_UNBOUND`，不得以本包作者身分補位。Maker 與 Protected Checker 在任何情況下不得由同一執行者自簽。

Input: H-CLOSE 的 Owner selection、W1M §05／§10、M §11.7 的 U-013／U-014 分帳。
Operation: 逐 Effect 建 permission／stop／resume 列，缺原權者標 null 與 HOLD。
Output: 本檔＋`00_WAVE_RUN_MANIFEST.json` 的 `effect_classes`／`holds`。
Consumer: Executor／Program／原域 Owner。
NEG: 作者授權當原 Admission → `FALSE_AUTHORITY`。
FirstFail: `EFFECT_UNBOUND`／`EXECUTION_ADMISSION_MISSING`。

## 2. 每個 Effect 的 Issuer 與 Admission

| Effect | 本輪 | Issuer | Admission | StopScope | Resume predicate |
|---|---|---|---|---|---|
| READ | 允許（已授權來源） | 不需要原 Issuer | 只需 source ACL／SHA | 來源不符即停該讀取 | 真 bytes／pin 一致 |
| DRAFT | 允許（隔離根） | 不需要原 Issuer | 隔離寫入＋diff／cleanup | 越出交付根即停 | 合法根＋preimage |
| DEV | `NOT_ADMITTED` | 原 Repo Owner／Issuer | 必須有 `ExecutionAdmission` | 停 Repo 寫入 | live HEAD＋ACL＋preimage＋WriteSet |
| OPS | `NOT_ADMITTED` | 原 Host Owner／OS Principal | 必須有 Host Admission | 停該 Host 安裝／服務 | HostID＋Principal＋Epoch＋loader |
| USER | 不適用 | 原 consent Owner | 必須有資料範圍與補償 | 停使用者資料效果 | 原 consent receipt |
| RELEASE | `NOT_ADMITTED` | 原 Publisher | GHP-02 適用回執 | 停發布 | Publisher receipt |

本輪 `execution_admission_receipt`、`independent_checker_receipt`、`publisher_receipt`、`verified_original_receipt_ref` 全為 null。`claims` 四 bool 全 false。

## 3. Stop scope

| 缺口 | 停止範圍 | 仍可繼續 | Owner |
|---|---|---|---|
| ChatGPT loader／install | ChatGPT 的 `Loaded` 以後 | Codex／Hermes 設計、四 API 設計 | ChatGPT Host Owner |
| Hermes 三能力 | Kanban／Delegation／Swarm 各自 | W1 文件與 ABI | Hermes Host Owner |
| Guide／Bridge consumer | 該 ABI 的 `Consumed` | crosswalk、BodyResolver 設計 | ABI Owner |
| Original Issuer | Host adapter 安裝／任何 effect | READ／DRAFT | Original Issuer |
| Protected Checker | Independent claim | 作者自檢 | Checker |
| W0-A 指定 | 原 Case 的 Host 使用 | W1 作者 13 案 | Original Project／Source Owner |
| W0-B | W2 前件 | W1 ABI／READ | Original Issuer／Repo／Host |

Stop 只停受影 claim，不停其他合法章節；外部 HOLD 不要求清零才交文檔。

## 4. Resume predicate

每個 HOLD 的 resume 必須是同 Subject／Scope（必要時同 Host／PolicyEpoch）的 typed receipt。不得以本地檔、`permit=true`、skill 可讀、public commit、歷史 `REPORTED` 或作者 CLI exit 0 補位。Resume 只解除受影 HOLD；其他 HOLD 保留。

## 5. UNKNOWN reconcile 與具名 HOLD

UNKNOWN 世界狀態先由原 Reader／WorldReader 讀回，再決定是否重試；不得盲重試或把 UNKNOWN 當 0／false。HOLD 清冊：

| HOLD／FirstFail | 缺口 | Owner | 解除最小證據 |
|---|---|---|---|
| `W1_HOST_NINE_GRID` | ChatGPT／Hermes 全態、Codex 後三態未觀測 | 各 Host Owner | 每 Host manifest／LoadedSHA／Invocation／Consumer readback |
| `W1_PLUGIN_ALIAS` | 只見 `sbl-tpm-sp`，未見 `tpm-sp-plp` 同 manifest | Plugin／Host Owner | 原 manifest／Loaded ID 同一性 |
| `W1_ABI_BOUND` | Guide／Bridge `@proposal-2` 無真 Consumer crosswalk | ABI Owner | 逐欄 field→target→loss→readback |
| `W1_W0_INPUT` | W0 只有作者 pack，無真 Host Raw | W0 Wave Owner | 只接受作者 Source／Case／Proposal |
| `W0_PRIMARY_RECEIPT_STALE` | 實體 4,222／`6dbdd7bd` vs 清冊 3,986／`18ad4b8d` | W0 Curator／Human Owner | 重算或書面確認 |
| `W0-A_CASE_SELECTION` | 6 候選無 Owner 指名 | Original Project／Source Owner | 指名或 typed ReasonedNA |
| `W0-B_NOT_ADMITTED` | 13 前件 UNBOUND | Original Issuer／Repo／Host | 13 前件 typed receipt |
| `ORIGINAL_READER_UNBOUND` | 無原 Canonical Reader | Reader Owner | 同 Scope typed readback |
| `ORACLE_FIXTURE_UNBOUND` | 原 Case Oracle／Fixture 未得 | Case Owner | 同 Case 真 bytes |
| `HOST_CAPABILITY_UNBOUND` | 三 Host 能力未得 | Host Owner | 七階段 Raw |
| `CHECKER_PUBLISHER_UNBOUND` | 無 Protected Checker／Publisher | Checker／Publisher | distinct receipt |
| `SOURCE_REFERENCE_HASH_CONFLICT` | 同名不同 SHA 之來源族 | Source Curator | 有權替代或排除受影切片 |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` | 1011 身份（576 ID＋435 slot）清單未得 | W0-C Owner | 原 ID 清單 |
| `HOLD_CR-DOC04-STATE-MAP` | T4/T5 DOC04 狀態圖未由原 Reader 對齊 | Original Reader／DOC04 Owner | 同 Subject／Scope 的 DOC04 state-map typed readback |

Resume 不得要求全部 HOLD 解除；只解除受影項。
