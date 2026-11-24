<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜DEV ECP（作者計畫）

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的 DEV ECP 作者計畫，批次 `W1-PACK-01`。它不是原 Canonical DEV ECP，不是 Grant，也不是任何 Repo 施工命令。原 RepoContext 未綁，所有 Repo 寫入維持 `NOT_ADMITTED`。

## 1. Applicability 與 Effect

Applicability: W1 的 DEV 範圍只含 Guide／Bridge adapter 的未來渲染與作者本地檔案生成；本輪實際執行限於已授權隔離根的 `ISOLATED_DRAFT_WRITE + LOCAL_CHECK`。產品 Repo 的 `DEV_REPO_WRITE` 不適用本輪。

Effect: 作者描述為 `SOURCE_READ + ISOLATED_DRAFT_WRITE + LOCAL_CHECK + LOCAL_PACKAGE`。原 `OperationType` 必須由 pinned Original Effect Registry 取得；目前 Registry `UNBOUND`，故任何 DEV token 皆 `EFFECT_UNBOUND`。不得由路徑、檔名或字串相似推斷 READ／DRAFT／DEV。

Input: B02 Guide 四函式契約、B03 Bridge 四 API、W1M §08 的 Effect 表、W0 PRIMARY 的 15 檔與 13 源。
Operation: 把「未來在原 Repo 落地的 adapter 變更」寫成可檢查的 Pre／Post／Readback／Rollback 計畫，並在本輪以隔離 fixture 驗證結構。
Output: 本 ECP＋`fixtures/` 的 DEV 反例。
Consumer: Repo Owner／Guide／Bridge Dev／W2 Executor。
NEG: 把本 ECP 的 `permission` 文字當核准 → `ECP_NOT_GRANT`。
FirstFail: `EXECUTION_ADMISSION_MISSING`／`EFFECT_UNBOUND`。

## 2. Preconditions

Preconditions:

1. 原 Repo Owner 提供 live `root`、`HEAD`、`branch`、`dirty`、`untracked`、ACL 與 permitted WriteSet；任何一項缺即 `REPO_BINDING_UNBOUND`。
2. 每個 target 的 preimage bytes 與 SHA-256 已由原 Repo Reader 讀回；不得以 G4 synthetic preimage 冒充。
3. 原 EffectRegistry 回傳 `OperationType`；DEV 與 DRAFT 不得互換。
4. 原 Issuer／Receiver 出具同 Subject／Scope 的 `ExecutionAdmission`；本輪此欄為 null。
5. 本地檢查能力可用（Python 3.11＋stdlib），且輸出根為已存在、非來源子孫的隔離目錄。

若僅有作者授權而無原 Repo Reader，本 ECP 只到 `AUTHOR_DESIGN_READY`；不得執行 `git apply`、`git commit` 或任何 Repo 寫入。

## 3. WriteSet 與禁止範圍

本輪 WriteSet 限於交付根內：`FHS-5_PLP_W1_PRIMARY/`、`evidence/`、`check/`、`DELIVERY_INDEX.md`、`FHS-5_PLP_W1_PRIMARY.zip`。未來受權 DEV 的候選 WriteSet（未核准）為：

| target | 變更型態 | 禁止 |
|---|---|---|
| Guide adapter renderer | 讀 Guide bindings，產 UTF-8 ThinStart | 新增 Scope／WriteSet／Grant |
| Bridge adapter projection | 讀 manifest／span，產 Context view | 寫原 Canonical JSON |
| BodyResolver adapter | 安全讀取＋SHA／span 驗證 | 繞過 path containment |
| Host facade | 文檔 context 輸出 | 安裝／註冊／啟動 Host |

禁止：改 W0 PRIMARY／LastGood、改 M／B／WM／W1M、改原 Case／Oracle、改原 Registry、寫 secrets、以 `git revert` 代替 OPS recovery。

## 4. Operation 與 Adapter 計畫

Operation（未來受權時）：Step 1 以 live probe 固定 RepoContext；Step 2 對每個 target 記 preimage SHA；Step 3 只改 WriteSet 內檔案，Guide／Bridge 各自保持 namespace；Step 4 以原 callable 跑 POS／NEG fixture；Step 5 產 postimage SHA、diff、test raw；Step 6 交原 Receiver readback。

本輪作者等價操作：在隔離根生成 10 MD＋5 JSON、sources、fixtures、oracles；以 `check/w1_guard.py` 與 M §22 guard 檢查；所有變更只影響本輪交付根。

Adapter 邊界：Guide 只輸出文字建議，`permission_state=NONE_GRANTED`、`original_reader=UNBOUND`；Bridge 唯讀，`effect_permission=NONE`；Host facade 只輸出 `DOCUMENT_CONTEXT_ONLY`，不宣 `ACTUAL_SERVED`。

## 5. Postconditions 與 Readback

Postconditions:

1. 15 個規範檔存在，`PACKAGE_FILE_MANIFEST.json` 逐檔 SHA／bytes 可重算。
2. 每個 Case 的 `oracle_path`／`fixture_path` 真可讀，SHA 一致；`05_PLANNED_TQAEP.json.projection_of_sha256` 等於 MD 真 SHA。
3. 六 identity 在 WaveControl、FileManifest、10 MD header、Case scope 中精確一致。
4. `claims` 四 bool 全 false；receipt 四欄 null。
5. 來源 bytes 未被修改；交付根外無寫入。

Readback: 以 `python check/w1_guard.py --pack-root FHS-5_PLP_W1_PRIMARY` 與 `python check/m22_guard_ref.py check-pack --pack-root FHS-5_PLP_W1_PRIMARY` 讀回；兩者只回 `AUTHOR_LOCAL_LINKS_ONLY`，不回原域 acceptance。另以 `check/replay_hashes.py` 重算每個 fixture／oracle／source SHA；以 `check/run_cases.py --pack-root FHS-5_PLP_W1_PRIMARY` 執行作者可執行的規則 fixture（結果只 `AUTHOR_LOCAL_RULE_ONLY`）。

Readback 證據放 `evidence/raw/`：命令、exit code、stdout／stderr SHA、失敗清單。無 raw 的敘述不算 readback。

## 6. Idempotency、Retry 與 Recovery

Idempotency key：`TaskID + source_manifest_sha256 + PRIMARY_selection + wave + revision`。同 key 重放只回同輸出或 no-op；異值建新候選並保 LastGood。

Retry：只允許暫時 I/O；`UNKNOWN` 先核 bytes／manifest／scope，再決定是否重試。不得因同一 first_fail 無新差額而原樣重跑；連續兩個有實質修補的回合仍同首錯，即停該 slice 並列具名 HOLD。

Recovery: 本輪以同卷 staging → 驗證 → atomic rename；失敗只清本輪 staging，不動來源與 W0。未來 Repo 失敗由原 Repo Owner 依其 ECP 回復 LastGood，保留 before／after diff；不得以刪除證據或改 Oracle 求綠。

Permission: 本 ECP 不授予任何 DEV 寫入。`execution_admission_receipt=null`、`original_ecp_ref=null`、`effect_registry=UNBOUND`；Executor 見到任何 `permission=true` 字樣都必須拒收為 `FALSE_AUTHORITY`。
