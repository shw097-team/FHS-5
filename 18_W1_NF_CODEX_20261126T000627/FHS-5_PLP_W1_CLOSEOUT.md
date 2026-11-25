# FHS-5_PLP W1 CLOSEOUT（NF-r4，R01–R06 收尾）

**File ID**：`FHS5-PLP/W1/CLOSEOUT/NF-r4`
**run_id**：`20261126T003047`
**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`｜**scope**：`W1-NF-01`
**pack_manifest_sha256**：`61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`
**repo**：`codex/w1-nf-r3-20261125`｜`content_commit` `UNCOMMITTED`｜`head` `d378e6a08240e9e56e892fcca8a6ac20fbe54a97`｜base `c2d8084ba24dd8df3fa62259bba496f4fb9caa85`
**判定**：`W1_NF_VALIDATED`｜`W2_TECHNICALLY_READY = READY`
**不宣稱**：`RELEASED`、`M-DONE`、`GPT_CHAT_PASS`、`GPT_WORK_PASS`、`HERMES_PASS`、`W2_EXECUTION_READY`

---

## 1｜R01–R06 實際狀態

| 項 | 狀態 |
|---|---|
| R01_fidelity | PASS |
| R02_host | PASS |
| R03_off | PASS |
| R04_closure | PASS |
| R04_cases | PASS |
| R05_w2 | PASS |
| R06_checker | PASS |
| F1_w2_inbound | PASS |
| F2_on_off | PASS |
| F3_candidate_pin | PASS |

### R01 通用產品語義

- `tpm_contracts_nf`: profile-driven（`W1` 保留真分母，`GENERIC` 不寫死 38/29/13）；契約五視圖為實質內容（需求、Child、ACC、capability、typed DAG、Effect、Recovery、Oracle）。
- Reviewer 唯讀、八欄 Finding、`first_fail` 與 `change_cone`；Finding raw 為真實觀測 payload 的 canonical digest，不是 subject SHA。
- Guide 四函式；`next/stop/resume` 由凍結 04 段落推導，`original_verifier` 會被實際呼叫，回傳非 `verified=true` 即 `DELTA_UNVERIFIED`。
- Bridge 欄級 `field_fidelity`：source value → transform → target value → readback，`missing` 由實算產生。

ABI 狀態：`COMPLETE`；field fidelity 由 `bridge_nf.verify_field_fidelity` 實算。

### R02 真 CODEX Host／Consumer

| 階段 | 觀測 |
|---|---|
| Selected | OBSERVED_LOCAL |
| Loaded | OBSERVED_LOCAL |
| Installed | REASONED_NA_NATIVE_ENTRY |
| Bound | OBSERVED_LOCAL |
| Invoked | OBSERVED_LOCAL |
| ActualServed | OBSERVED_LOCAL |
| Consumed | OBSERVED_LOCAL |

- 兩次真實 `codex exec` session：`01a21375-665e-71c3-b1af-8b1e701b5707`（W1 pack）與 `01a21375-9b1f-7cd2-a4bc-a848ae6ff44a`（W0 pack）。
- 版本：`codex 0.169.0-alpha.11.1`；served 方式：invocation payload（nested Codex 無可用 file-read 工具，已如實記錄）。
- 每個產物由獨立 consumer 程序 parse/use/readback；pkgA 的 fixture/oracle SHA 與 pack 實值逐欄比對。

### R03 Native OFF／安全

- `off_isolation.cold_off_probe`：5 個 legacy runtime 全部 blocked，`positive_control("json")` imported=True（證明探針不是瞎的）。
- 7 類路徑攻擊全 `PATH_OUTSIDE_ROOT`；canary 前後 digest 不變；symlink 探針在本機回 `NOT_VERIFIED`（Windows 特權不足，未提權）。
- `env_flag_only_reject`：純 env flag 不得作為隔離證據。

### R04 證據與核銷

- 共用 Closure Matrix：`W1_CLOSURE_MATRIX.json`（118 列）。
- 計數：| COVERED_BY_SHARED_OPERATION | 62 |；| DEFERRED | 3 |；| EVIDENCED | 17 |；| EVIDENCED_WITH_DEFERRED_HOSTS | 1 |；| EXERCISED_INDIVIDUALLY | 2 |；| HOLD_PRESERVED_NOT_CLOSED | 14 |；| NOT_APPLICABLE_THIS_ROUND | 1 |；| PASS | 18 |
- Observation 分離 `candidate_sha / source_sha / pack_sha / oracle_sha256 / case_set_sha256 / evidence_sha256`。

### R05 W2 技術接收

- 獨立 `w2_receiver`：accepted = `True`，checks = `29`，rejected = `[]`。
- next operation：`W2-READ: build the 13-row Draft BindingRequest plan inside W2-READ-01; no grant, no protected effect`

### R06 封存

- 交付本身含 evidence manifest、seal、closure matrix、host receipt、W2 receipt、OpenSpec change。
- 發佈記錄外置於 `PUBLICATION_STATUS.md`，不在被 commit 的文件內反覆寫自身 HEAD。

### F1 真 W2 入站

- W2 DRAFT 材料：13 列 BindingRequest，來源 W2M §03.1（`evidence/w2/material`）。
- 真 CODEX session：`01a21379-31e7-73d1-98bb-4d2870f612e9`，產出 13 列分類 artifact，獨立 consumer 逐列驗證。
- 五條 Seam 接線：`5/5`，state `COMPLETE`。
- `permission_state=NONE_GRANTED`、`grant_issued=false`。

### F2 ON／OFF

- 同一 W2 任務：ON `13` 列、OFF `13` 列，投影相等 `True`。
- Legacy cold OFF `True`、正控 import `True`。
- OFF 子程序未 import TPM／Guide／Bridge：`[]`。

### F3 候選與證據

- candidate 重算 `e28d959093c7f1a3…` vs raw `e28d959093c7f1a3…`，一致 `True`。
- NEG 未拒絕即 FAIL、POS 空觀測即 FAIL、exit 0 但未 consumed 不計 PASS（`check/test_negative_control.py`）。

---

## 2｜測例（20 列）

| Case | Kind | Verdict | token |
|---|---|---|---|
| `W1-HOST-01` | POS | PASS | - |
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

PASS 19｜NOT_OBSERVED 0｜DEFERRED 1｜FAIL 0
單元測試：79 tests OK

## 3｜實作檔

| 檔 | bytes | sha256 |
|---|---:|---|
| `W1/impl/abi_guard.py` | 2198 | `3b4cc1648bc294b0028d52a0ecc0584a2eac048815c6dfc57a0da1f53ee34337` |
| `W1/impl/body_resolver.py` | 11776 | `d1ee5c7e1b299a0bdc7fa22842872ab5682d6ec786c1ccd1ec06d62293bba857` |
| `W1/impl/bridge_nf.py` | 17946 | `b671eacf08ad7ab423874e7c799ea84188b26e53968c59e4b86f2bc38d8f78db` |
| `W1/impl/guide_nf.py` | 13516 | `90e9b6b5fbd596ca85150ddb2bb721f4cdc1c1cc49ce0f34d5617040096c928e` |
| `W1/impl/host_facade.py` | 4291 | `ae002913a440d08a6218000249d01982a81b34ce33afaaad7e732135a9425c56` |
| `W1/impl/nf_reader.py` | 24272 | `60246bd748bf01c542266a374b07d058d18bd68991c573cb3b6c1663d6283ac2` |
| `W1/impl/off_isolation.py` | 23568 | `955f93a838717cc15f4da5c068b858a9f01f6074c76716ee916cfb7ab5ce7965` |
| `W1/impl/tpm_contracts_nf.py` | 20111 | `6e71e219c50f4ef92e830edea43e933f74c836caa5f11c416a14caba8e5126fb` |
| `W1/impl/w1_bridge_reference.py` | 36580 | `dc0d1041a473a96493c887f279f75dcc1eca077c39242de47faffd44e12050a8` |
| `W1/impl/w1_consumer.py` | 6602 | `b380fbbb1d780892e8ecdeb855c607b5bc8392705b0f0c7ceffe9f10e57cb7d5` |
| `W1/impl/w1_nf_reader.py` | 29071 | `87d01399104f8899c1ed494b8e9b2edb3bef0fd79ceca36920ecda47140baa63` |
| `W1/impl/w2_inbound.py` | 11374 | `391dd7072ca84ab3ef40a859867efc2cdcfd3be186ab9e6892e44d145aab0555` |

## 4｜測試與 runner

| 檔 | bytes | sha256 |
|---|---:|---|
| `W1/check/closure_matrix.py` | 11362 | `ea0658f3ac78073ec8c5afca87598a8c950c0732dc6306dcb14bb8da107119e4` |
| `W1/check/m22_guard_ref.py` | 16143 | `74d76b3581d1a5cab1d7178b86c8c4227363421256bf8b21e44da10be4b6ef4c` |
| `W1/check/replay_hashes.py` | 1999 | `c1743ff95f26340f83104aa8f1f94dafd30b55554dc4de2be47a87efb0587572` |
| `W1/check/run_cases.py` | 4981 | `a498149b0a9105435bbec96de9ac4899d87e669a12ea86d3456fce64ff5609be` |
| `W1/check/run_cases_nf.py` | 28725 | `06d569719ee6057821001a3d377c5cd95cc1a4daecb36e0a0abde43986b002a7` |
| `W1/check/run_harness.py` | 11420 | `3384841787d4d68c1c56fbb62dfe1776720b02205d58ffbf30c9e915a957dd9f` |
| `W1/check/run_host_nf.py` | 16450 | `a2254a440c72127d5d44d159fc0dc0620da68287a716b397441d31d01edcca0f` |
| `W1/check/run_off_task.py` | 6058 | `30f93fbc2ba23d0e766ae19515e77fc4fa60efedec9ac260122acfa226e17551` |
| `W1/check/run_w2_inbound.py` | 8923 | `22c537497ae7b9465df882ab4127cc638fb2029a26ed52676df7c2a907d0a2d7` |
| `W1/check/test_body_resolver.py` | 3597 | `c320686ed8306a36785727470139f5189b0ccbab67943bc14703204d28407154` |
| `W1/check/test_bridge_body.py` | 3554 | `5333e1a107b3b7858f83ad09e74be18d3f65a69f582593c5ce3190333da20bc9` |
| `W1/check/test_consumer.py` | 3554 | `2f77c51c0c8f9a521014852767c0ed6c1f9e3a7ea10713de4983055b4067966c` |
| `W1/check/test_guide_nine_keys.py` | 5340 | `4b0b6c76090197d219834ef437a6fa00a6c3dd8116435bcdef9cf489cdc07673` |
| `W1/check/test_negative_control.py` | 2700 | `81914102eeb907d6eca534e47f41163be24a35576180e45b10cfd0b15995423e` |
| `W1/check/test_nf_reader.py` | 3928 | `647dafa2d69b355e5f837ef097b225eb5060559a09a5c93cdd3ab913656ef47d` |
| `W1/check/test_off_isolation.py` | 9402 | `2615072eb11bbf2c6aebe12e3b01ff5f2830069ea31c48c0a93ca260790d3fcf` |
| `W1/check/test_tpm_contracts.py` | 3508 | `fb92ba67d4ed2c3aa0538bb5afecd06898e5cd305984af234083882f64425aac` |
| `W1/check/w1_guard.py` | 14331 | `41ec2fc0183ddfd0b43e0a988bba84a9ae24e78657e060d5749c243e7dedce4a` |
| `W1/check/w2_receiver.py` | 9336 | `c666740268cce914819e2ba43a0dbd9413de709792ee2c8338b0b67e895c74f0` |

## 5｜殘餘與 Next

無當期必要缺口。
- HERMES 三 child：`DEFERRED`（未掛載），不阻 Generic。
- 真 Windows junction/reparse：`NOT_VERIFIED`（未提權）。

## 6｜結論

`W1_NF_VALIDATED`；`W2_TECHNICALLY_READY = READY`。證據見 `evidence/`、`W1_CLOSURE_MATRIX.json`、`W2_RECEIVE_RECEIPT.json`。
