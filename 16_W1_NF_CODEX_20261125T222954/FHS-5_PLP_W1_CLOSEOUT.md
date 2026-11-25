# FHS-5_PLP W1 CLOSEOUT（CODEX Native-first 主用修補定案，產品層）

**File ID**：`FHS5-PLP/W1/CLOSEOUT/NF-r3`
**run_id**：`20261125T222954`
**project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`｜**scope**：`W1-NF-01`
**wave_id**：`W1`｜**batch_id**：`W1-NF-01`｜**date**：2026-11-25（Asia/Taipei）
**pack_manifest_sha256**：`61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`
**repo**：`codex/w1-nf-r3-20261125` @ `c2d8084ba24dd8df3fa62259bba496f4fb9caa85`（base `c2d8084ba24dd8df3fa62259bba496f4fb9caa85`）
**claim ceiling**：`W1_PARTIAL_VALIDATED`｜`W2_TECHNICALLY_READY = NOT_READY`
**不宣稱**：`W1_NF_VALIDATED`、`INDEPENDENT_PASS`、`RELEASED`、`M-DONE`、`GPT_CHAT_PASS`、`GPT_WORK_PASS`、`HERMES_PASS`、`W2_EXECUTION_READY`

---

## 1｜本次實際完成（可分帳、可重放）

| 項 | 實際 | 證據 |
|---|---|---|
| 六檔 pack 接收 | 5 MD＋05 strict JSON＋26 assets＋外置 seal，42 sources 逐筆稽核 | `evidence/inspect.json` |
| Reader（四 API＋BodyResolver） | `nf_reader` / `body_resolver` / `bridge_nf` 真跑 | `evidence/raw/*.json` |
| Guide | 四原函式＋四 NF adapter、兩模式、九鍵真 producer | `evidence/raw/N03.json` |
| TPM/Reviewer | 五視圖同一工作身份、唯讀八欄 Finding、0 寫入 | `evidence/raw/N01.json` |
| Host facade | 7 階段 ledger、四類降級拒絕 | `evidence/raw/N04.json` |
| Consumer | 獨立本地 consumer 真 parse/use/readback | `evidence/raw/N04.json` |
| 第二包 | W0 NF-r3 pack 同 ABI 重用，capability 明示差異 | `evidence/raw/W1-CODEX-05.json` |
| 測例 | 13 原案＋N01–N04/N10/N11＋ACC 第二包＝20 列 | `evidence/cases.json` |
| 單元測試 | 63 tests OK | `evidence/test_run.txt` |
| OpenSpec | `openspec validate w1-nf-r2-product` = valid | `openspec/` |

### 1.1 實作檔（真實 bytes／SHA-256）

| 檔 | bytes | sha256 |
|---|---:|---|
| `W1/impl/body_resolver.py` | 11776 | `d1ee5c7e1b299a0bdc7fa22842872ab5682d6ec786c1ccd1ec06d62293bba857` |
| `W1/impl/bridge_nf.py` | 12946 | `baf1cfb2080382054b1db61ffa37970116e90b0c2494fb80ffa715336b0ca297` |
| `W1/impl/guide_nf.py` | 11705 | `abbda08f2198d862a60f9e530b38b8085436d24de5158947d75702f82da1c90b` |
| `W1/impl/host_facade.py` | 4291 | `ae002913a440d08a6218000249d01982a81b34ce33afaaad7e732135a9425c56` |
| `W1/impl/nf_reader.py` | 23997 | `6bca5c58b25b5cefea1ae9c1d20a286a99974dcc680e1fecd8c0b5ea9c3180c6` |
| `W1/impl/tpm_contracts_nf.py` | 11073 | `00f1222a26df56a14c5da69478f18009161f729b4722f4ac837652db250b1346` |
| `W1/impl/w1_bridge_reference.py` | 36580 | `dc0d1041a473a96493c887f279f75dcc1eca077c39242de47faffd44e12050a8` |
| `W1/impl/w1_consumer.py` | 6602 | `b380fbbb1d780892e8ecdeb855c607b5bc8392705b0f0c7ceffe9f10e57cb7d5` |
| `W1/impl/w1_nf_reader.py` | 29071 | `87d01399104f8899c1ed494b8e9b2edb3bef0fd79ceca36920ecda47140baa63` |

### 1.2 測試與 runner

| 檔 | bytes | sha256 |
|---|---:|---|
| `W1/check/m22_guard_ref.py` | 16143 | `74d76b3581d1a5cab1d7178b86c8c4227363421256bf8b21e44da10be4b6ef4c` |
| `W1/check/replay_hashes.py` | 1999 | `c1743ff95f26340f83104aa8f1f94dafd30b55554dc4de2be47a87efb0587572` |
| `W1/check/run_cases.py` | 4981 | `a498149b0a9105435bbec96de9ac4899d87e669a12ea86d3456fce64ff5609be` |
| `W1/check/run_cases_nf.py` | 27299 | `fdff7a29d47741d01f9c82ebc9416c9b61cfd57d122e71a77b6048a363df43d4` |
| `W1/check/run_harness.py` | 11420 | `3384841787d4d68c1c56fbb62dfe1776720b02205d58ffbf30c9e915a957dd9f` |
| `W1/check/test_body_resolver.py` | 3597 | `c320686ed8306a36785727470139f5189b0ccbab67943bc14703204d28407154` |
| `W1/check/test_bridge_body.py` | 3554 | `5333e1a107b3b7858f83ad09e74be18d3f65a69f582593c5ce3190333da20bc9` |
| `W1/check/test_consumer.py` | 3554 | `2f77c51c0c8f9a521014852767c0ed6c1f9e3a7ea10713de4983055b4067966c` |
| `W1/check/test_guide_nine_keys.py` | 5254 | `7446ac2b0a8b800a71dc231d3bc4b890635e062aaa975c86943f6e9c5bbb86f8` |
| `W1/check/test_nf_reader.py` | 3928 | `647dafa2d69b355e5f837ef097b225eb5060559a09a5c93cdd3ab913656ef47d` |
| `W1/check/test_tpm_contracts.py` | 3364 | `e0f4c2bcf438bf23187f63ef44d5ebc1d059dfcea80b930d2452ccf985bf3de4` |
| `W1/check/w1_guard.py` | 14331 | `41ec2fc0183ddfd0b43e0a988bba84a9ae24e78657e060d5749c243e7dedce4a` |

---

## 2｜13 原 Case 與子例逐案 verdict

| Case／子例 | Kind | Verdict | 觀測 / token |
|---|---|---|---|
| `W1-HOST-01` | POS | NOT_OBSERVED | - |
| `W1-HOST-02` | NEG | PASS | HOST_ABI_DRIFT |
| `W1-HOST-03` | NEG | PASS | HOST_PENDING |
| `W1-HERMES-01` | POS | DEFERRED | - |
| `W1-ABI-01` | NEG | PASS | EXPLICIT_REVIEW_REQUIRED |
| `W1-ABI-02` | NEG | PASS | LOSSY_MIGRATION |
| `W1-SEC-01` | SEC | PASS | - |
| `W1-API-01` | POS | PASS | - |
| `W1-R3-01` | POS | PASS | - |
| `W1-R3-02` | NEG | PASS | HOST_PENDING |
| `W1-R3-03` | NEG | PASS | ABI_LOSSY_CROSSWALK |
| `W1-R3-04` | EDGE | PASS | - |
| `W1-R3-05` | NEG | PASS | EVIDENCE_LAUNDERING |
| `N01` | SUBCASE | PASS | - |
| `N02` | SUBCASE | PASS | - |
| `N03` | SUBCASE | PASS | - |
| `N04` | SUBCASE | PASS | - |
| `N10` | SUBCASE | PASS | - |
| `N11` | SUBCASE | PASS | - |
| `W1-CODEX-05` | ACC | PASS | - |

**分母**：13 原 Case 全數有列；HERMES-01 為 `DEFERRED`（Hermes host 未掛載），HOST-01 為 `NOT_OBSERVED`（無真實 CODEX host served/consumed session）。其餘 POS/NEG 真跑並取得預期 token。**不以 NEG 通過冒充 POS 產品**。

### 2.1 已知缺口（不作 PASS）

1. `W1-HOST-01`：只完成 local entry invoke／local consumer；沒有真實 CODEX host session 載入 W1 entry 並記錄 served/consumed → `NOT_OBSERVED`。
2. `W1-HERMES-01`：Hermes 三 child 未掛載 → `DEFERRED`。
3. 38 DEV／29 OPS：本次實作核心建造與 host facade，未逐 ID 產生 67 份獨立 raw。
4. Windows junction／reparse 真攻擊：symlink 測試視環境結果而定；未取得者記 `NOT_VERIFIED`。
5. 獨立 Checker：另一 session 唯讀重跑（§5），不因此升格 Independent 發布。

---

## 3｜12 ACC 實質對位

| ACC | 觀測 | Verdict |
|---|---|---|
| `W1-A01` Source | 42 sources 稽核；缺席者記 `LOCAL_MISSING_RECORDED`，不補造 digest | PASS |
| `W1-A02` Body | 四 API 回完整 clause／span；heading-only 被 `BODY_RESOLVER_UNBOUND` 拒 | PASS |
| `W1-A03` Host | 7 階段逐階、skill/exit0/hash 三類升格被拒；真實 host served 缺 | PARTIAL |
| `W1-A04` ABI | 逐欄 crosswalk 全 PRESENT，unknown_drop=0 | PASS |
| `W1-A05` Split | 5+1、38/29/13/26/14 計數一致；DAG 6 節點可拓樸 | PASS |
| `W1-A06` Claim | claim 僅到 PARTIAL；未簽 Independent／Release | PASS |
| `W1-CODEX-01` | TPM/Guide/Bridge/consumer 皆真讀本包 | PASS |
| `W1-CODEX-02` | 九鍵兩期、逐鍵變動、缺期／caller bool 全拒 | PASS |
| `W1-CODEX-03` | Bridge 四 API 完整 body；越界／注入／heading-only 拒 | PASS |
| `W1-CODEX-04` | 五視圖同身份；Reviewer 0 寫入、八欄 Finding | PASS |
| `W1-CODEX-05` | W0 第二包同 ABI；錯 pin／錯身份拒 | PASS |
| `W1-CODEX-06` | GPT CHAT／WORK／HERMES 未掛載，各自 `NOT_OBSERVED`／`DEFERRED` | NOT_OBSERVED |

---

## 4｜Effect、權限與邊界

- `READ`：來源根唯讀實讀。
- `DEV`：僅本輪 worktree `C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3` 內 `W1/impl`、`W1/check`、`16_W1_NF_CODEX_20261125T222954`。
- `OPS`：僅本地 invoke（python entry）與本地 consumer；無 host 安裝／服務。
- `RELEASE`：GitHub 上推見 `PUBLICATION_STATUS.md`。
- `permission_state = NONE_GRANTED`；`advice ≠ Grant`；`ECP ≠ Grant`。

---

## 5｜獨立檢查（另一 session，唯讀）

- 檢查者：另一 Codex 子 session，對凍結候選唯讀重跑，不修改 subject／oracle。
- 命令與結果：`evidence/independent_check.json`。
- 限制：同一 OS principal（本機使用者），不虛構不同 principal。

---

## 6｜NotCovered

W2–W4 產品、GPT CHAT/WORK、HERMES 三 child、真實 CODEX host served/consumed、Windows junction/reparse 真攻擊、67 ID 逐份 raw、原 Guide 17／Bridge 66／Challenge／FAR 全量、Independent、Release。

---

## 7｜結論

`W1_PARTIAL_VALIDATED`：reader／bridge／guide／TPM／consumer／第二包／19 項測例與 63 單元測試為真；`W1-HOST-01` 與 HERMES 未達，故不宣 `W1_NF_VALIDATED`。
