<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜Wave Control 正文（作者候選）

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的作者端 Wave Control 正文，批次 `W1-PACK-01`。它不是原 Canonical PI／PD／ECP／TQAEP，不是 ExecutionAdmission，也不是任何 Host 的施工命令。最高效力 `AUTHOR_DESIGN_ONLY`；所有原域收據欄位保持 null。

## 0. 身份、來源與效力

Identity（六鍵，與 JSON／FileManifest／TQAEP projection 完全同一）：

- `project_id`：`FHS-5_PLP`
- `subject_id`：`FHS-5_PLP/W1/CONTROL_PACK`
- `scope`：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`
- `wave_id`：`W1`
- `batch_id`：`W1-PACK-01`
- `source_manifest_sha256`：`8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47`

來源模式 `SELECTED_ONLY` ＋ `PARTIAL_SOURCE_SET_ONLY`；本包釘選 16 個實際可回取來源（M／ME 以外之正文與 W0 交接、本輪控制包與啟動薄、W0 PRIMARY 兩份實體證據），不冒 CORE16。W1M wm-v5 的歷史 17 源 pin set `4b08a4583d1788b16ad4337e3a7e81200beb85a26de927576aa86b73f0dc9626` 只作血緣，**不是**本包 SourceManifest 的分母。

Input: 12 個釘選來源（M r3、B00–B05 r4a、WM r2、W1M wm-v5、W0MB candidate-v2、H-CLOSE、H-PATCH）＋ CTRLW1／STARTW1 ＋ W0 PRIMARY 實體 manifest/receipt。
Operation: 逐檔重算 bytes／lines／raw SHA-256，選 `SELECTED_ONLY`，建立 SourceFreeze 與 W0 差額帳。
Output: `SOURCE_MANIFEST.json`＋本 WaveControl＋後續 13 個規範檔。
Consumer: W1 Executor／Bridge／W2 Program／原域 Owner（只讀）。
NEG: 同名換版、假 SHA、以 r5 冒 wm-v5、以 workspace 樹冒 PRIMARY → `SOURCE_IDENTITY_HOLD`。
FirstFail: `SOURCE_INTEGRITY_FAILED`／`SOURCE_REFERENCE_HASH_CONFLICT`。

## 1. Goal／FUO／Done

**Job to be done**：Human Owner 需要一套 Guide／Bridge／Codex／Hermes 可直接消費的 W1 全量控制包，使後續 Executor 不必猜上游要求、不重造原系統，能按實際准入逐步取得 W1 接口效果。

**本輪作者 Goal**：把 W1M wm-v5 的設計切成 15 個可施工規範檔，內含六個 WP 的操作、原義務、逐欄 ABI、四 API、三 Host 九子義與 Hermes 三能力、DEV／OPS ECP、Planned TQAEP、Stop／Resume 與下一波交接。

**本輪作者 FUO（Done）**：

1. 15/15 規範檔（10 MD＋5 JSON）實際存在，逐檔可讀回、可重算 SHA。
2. 每個 Case 有真本地 fixture／oracle（標 `AUTHOR_FIXTURE_NOT_LIVE`），原 Case 身份另欄保存。
3. 六 WP 各有一個可 dry-consume 的 Input→Operation→Output／Consumer slice。
4. 本輪 H1–H8 作者自檢與反例實跑，raw 可回取；失敗已修或具名 HOLD。
5. 全部交付有索引、ZIP、外置 seal；15 檔數與 SHA 一致。

**W1 產品 FUO（本輪不要求實現）**：同 Subject／Scope 的 Guide ThinStart → Bridge 四 API → 真可回取 Contract Context → 至少一個受權 Host 的 `Consumed` Raw。三 Host 九子義逐一分帳；一個 Host 的結果不能核銷其他 Host。

## 2. Scope 與 Non-goals

本包只涵蓋 Guide／Bridge ABI 逐欄轉接、四 API 作者契約、BodyResolver 邊界、三 Host 七階段與 Hermes 三 child 的 observation 設計，以及 W2／W3／W4 的欄級交接介面。

明確不做：不改 W0 PRIMARY／LastGood、不改上游 M／B／WM／W1M、不改原 Repo／Host；不安裝或註冊插件；不啟動原 Native、W2–W4；不自簽 Grant／Independent／Release；不生成假 `FHS5_Wn_WRITEBACK.json`；不以作者 fixture 充原 Runner；不把 1011／485 分母當 W1 Host Fit。

## 3. 五個內部批次與六個 WP

| Batch | Scope | WP／Case | 依賴 | 出口 |
|---|---|---|---|---|
| W1-B1 Identity | plugin／alias／三 Host 能力 | WM1-P01、W1-HOST-03、W1-R3-02 | 無 | `HostCapabilityLedger` |
| W1-B2 ABI | Guide 三 namespace、Bridge 四 API | WM1-P02、WM1-P03、W1-ABI-01／02 | B1 source ledger | `ContextBundle` 設計 |
| W1-B3 Adversarial | scope／unknown／path／secret | WM1-P05、W1-SEC-01、W1-API-01 | B2 | `AdversarialABIReport` |
| W1-B4 Host | 三 Host 逐態、Hermes 三格 | WM1-P04、W1-HOST-01／02、W1-HERMES-01 | B2／B3 | `HostObservationLedger` |
| W1-B5 Closure | AsBuilt／handoff | WM1-P06、W1-R3-01..05 | B4 或具名 HOLD | `WaveClosure` |

六 WP 的實質步驟在 `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` §4；typed DAG 為 `P01 -requires-> P02 -requires-> P03 -requires-> P04`、`P02 -requires-> P05`、`P04 -requires-> P06`、`P05 -requires-> P06`（`requires` 表示下游依賴上游，不是反向阻斷）。P02 與 P05 可並行；P04 未取得 B2 的 ABI 不得宣 Invoked；P06 未取得 P04 的 Raw 不得宣 Consumed。`W0-B_NOT_ADMITTED` 只經 `deferred_to_wave` 影響 W2，不是 W1 作者閉合前件。

## 4. Host／Claim／Effect 分帳

| Host | 七階段本輪狀態 | 可宣 | 不可宣 |
|---|---|---|---|
| ChatGPT | 全 `NOT_OBSERVED` | 只可寫 adapter 設計 | `Loaded`／`Installed`／`Consumed` |
| Codex | `Selected`＝session capability；`Loaded`＝skill bytes read；`Bound`＝plugin version path；`Invoked`＝local tool calls；`Installed`／`ActualServed`／`Consumed`＝`NOT_OBSERVED` | 只可寫 `HOST_PARTIAL_LOCAL_ONLY` | plugin native Invoked／ActualServed |
| Hermes | 全 `NOT_OBSERVED`；Kanban／Delegation／Swarm 三格分開 | 只可寫三格 ExpectedRaw | 任一格 `Verified` |

`claims` 恰四 bool，全 false：`local_observed`／`native_observed`／`independent_accepted`／`released`。local 證據另放證據附錄與合法 observations，不改 flags。

Effect 只到作者描述：`SOURCE_READ + ISOLATED_DRAFT_WRITE + LOCAL_CHECK + LOCAL_PACKAGE`。DEV／OPS／USER／RELEASE 全部 `NOT_ADMITTED`；原 EffectRegistry token `UNBOUND`。`effect_analysis="DRAFT"` 是本包的分析類型，不是原 Registry token。

## 5. 交付與停止

交付拓撲：`FHS-5_PLP_W1_PRIMARY/`（15 normative＋sources／fixtures／oracles／inventory）、`evidence/`（證據型附錄、審查修補定案報告、raw）、`check/`（重現入口）、`DELIVERY_INDEX.md`、`FHS-5_PLP_W1_PRIMARY.zip`。索引與 ZIP digest 外置記於 `DELIVERY_SEAL.json`，不做自含循環。

具名 HOLD 為 14 筆：原 13 筆＋`HOLD_CR-DOC04-STATE-MAP`（T4/T5，只在受影 claim 生效）。停止條件：核心來源缺失或不可修時，交 `AUTHOR_PARTIAL_WITH_NAMED_HOLDS`；原域未綁只停受影 claim，其他合法作者工作繼續。本輪完成交付即停止，不跨入 W2 施工。
