# FHS-5/W0｜UPSTREAM_CHANGESET（W0-NF CODEX-first）

**change_id**：`W0-NF-CS-20261125-02`｜**date**：2026-11-25（Asia/Taipei）

| 欄 | 內容 |
|---|---|
| Source | W0M `NF-r3-PRIMARY` `a1f186cc…`＋`CODEX-FIRST-r4` `c9b1ca9b…`；W0 pack `e3772aee…`；W0M §00.6／§05.1／§05.5 #5／§08.1／§08.5 |
| Old dependency | 舊 W0 以 Original OPS ECP typed ref、OriginalReader／Registry／Runner／ACK 為前置；一次可逆 DEV 限制；HERMES 主工程前置 |
| Finding | `F-W0NF-001`：invalid `--root` 產生 traceback、exit 1（應 `INVALID_PATH`／3）；raw `04_DEV_OPS/raw/red_v2.stderr.txt`，SHA 見 FAR finding |
| Root cause | `Path(root).resolve(strict=True)` 未捕捉 `OSError`，且未檢查 `is_dir` |
| Decision | `KEEP` NF-ADR 與本地 OPS 採納；`REPLACE` 該 fail-open 行為；`DEFER` FHS 485、HERMES、完整 W1–W4 分母 |
| New requirement | invalid root 必須 fail closed；44 案 receipt＋五 pin；W1 consumer 錯 pin 拒 |
| Impact | PROG-00 有效責任／七 Seam；PROJ-01（TPM/Reviewer）、PROJ-02（Guide）、PROJ-03（Bridge）、PROJ-04（Challenge）、PROJ-05（FAR）；WM/W0M 之 B0 狀態與 W1 準入；case T09/T13/T14/T24；分母不變 |
| Regression | 44/44 receipts；Challenge 32 checks；Reviewer 0 defects；Bridge 三項安全拒；OPS O1–O5；12 tests＋2 probe |
| Owner | Human Owner（決策）；CODEX（執行） |
| last_good_ref | pack `e3772aee…`＋candidate v2 `5eab43d`＋`12_B0_NF_CODEX` evidence |
| resume_predicate | W1M 採納；或新 candidate/oracle 使本 pins 失效；或 Owner 提供 W1 入口 |

## 受影條文回寫（工作區版本）

以下回寫以「受影段落替換稿」形式存放於 `09_DELIVERY/UPSTREAM_WRITEBACK/`，保留原檔與原 SHA，不覆寫 Downloads 來源；正式採納前不標 `CURRENT`。

| 上游 | 受影響段 | 變更 |
|---|---|---|
| MASTER | W0 分波狀態、B0/W0 claim、NF-ADR 執行狀態 | `B0/W0 NOT_RUN` → `B0_NF_VALIDATED／W0_NF_VALIDATED`（附 pins） |
| PROG-00 | 有效責任、七 Seam SM01–SM07、六檔、no-global-gate | 加本地 OPS 與 Challenge/consumer 實證；保留原分母 |
| PROJ-01 | Reviewer 缺 B／無源 Gate | 加 `REQUIRED_CHILD_MISSING`／`SOURCE_UNBOUND` |
| PROJ-02 | Guide Touch1/Touch2、九鍵、Scope | 加 `SCOPE_DRIFT`／`HOLD_NO_DELTA` 實證 |
| PROJ-03 | Bridge 四 API、路徑／scope | 加 W0 package view 與三項安全拒 |
| PROJ-04 | Challenge 五 pin／八欄 Finding | 加 30 checks、0 findings、checker worktree |
| PROJ-05 | FAR Finding／≥2 方案／七鍵 | 加 F-W0NF-001 與 3 方案 |
| WM／W0M | B0 狀態、W1 準入、NotCovered | `W1_TECHNICALLY_READY`；`W1_EXECUTION_READY=NOT_CLAIMED` |
| W1M | 以本 pins 為輸入、14 HOLD requalify | 新增 resume 條件；不提前宣 W1 施工 |

## 未關閉項

- `W1_HOST_NINE_GRID`、`W1_PLUGIN_ALIAS`、`W1_ABI_BOUND`、`W1_W0_INPUT`（本次已提供 W0 input，待 W1 真消費）。
- `ORIGINAL_READER_UNBOUND`、`CHECKER_PUBLISHER_UNBOUND`、`W0-B_NOT_ADMITTED`（原域）、`W0C_DENOMINATOR_ID_LIST_UNBOUND`。
- HERMES Compatibility、FHS 485 全量、W1–W4 完整分母。

## 本輪最小補強（HARDEN-02）

| 欄 | 內容 |
|---|---|
| Source | 前輪 W0 `15b063e`；NF-T08／NF-T10／T06／NF-T01/05/06 受影 |
| Finding A | NF-T08 以 summary 數量判 `COMBINED_OK`，缺 challenge 仍 fallback；無真實材料鏈 |
| Finding B | Consumer 未核 oracle、未驗 evidence 索引內容、錯 pin 仍可能跑 CLI |
| Finding C | symlink 因 Windows 權限 `NOT_VERIFIED`，未完成安全義務 |
| Finding D | OFF 以 env marker／importtime 代替真隔離，FAR OFF 無實際 patch |
| Root cause | assurance/harness 以摘要代替真實消費；Host 權限差異 |
| Decision | `REPLACE` 上述判定；`KEEP` candidate v3（無產品 byte 變更） |
| New requirement | collab chain 8 段＋7 負例；consumer 776 checks＋10 負例；WSL symlink 8 案；三種 OFF 真隔離 |
| Impact | tools（collab_chain／consumer／off_*／security_*／evidence_manifest）、TQAEP NF-T01/05/06/08/10、T06、challenge 排除 consumer-staged T10、delivery pins |
| Regression | 44/44 receipts；challenge PASS（43 candidate receipts）；consumer consumed；10+7 negatives rejected |
| last_good_ref | 前輪 evidence `cb71b632…`＋candidate `bb66a27` |
| resume_predicate | 新 candidate 或 oracle 變更；W1M 採納；Host 權限改變 |

## FINAL-HANDOFF-RECONCILE（M1／M2／M3）

| 欄 | 內容 |
|---|---|
| M1 Finding | GitHub blobs 與 Evidence Manifest 147 檔 bytes 不符；oracle raw `60bafa…` vs pin `112f29…` |
| M1 Root cause | Git clean filter 在加入時把 CRLF 轉 LF；working bytes 未變 |
| M1 Decision | 以 byte-preserving `hash-object --no-filters`／`update-index` 還原 147 個 CRLF blob，不改 Manifest |
| M2 Finding | Reviewer ON／OFF 共用不存在的 outroot，雙失敗仍 parity PASS |
| M2 Decision | 獨立 outroot＋expected semantics；雙失敗負例拒絕 |
| M3 Finding | 契約／context 未真正被下游消費；consumer 依賴 workspace 絕對路徑 |
| M3 Decision | contract_context＋native_context 真實消費；`--root`＋bundle 重建 candidate；clean clone 803 checks |
| Impact | tools、NF-T01/T08 receipts、Evidence／Consumer manifests、HANDOFF freeze、delivery docs |
| last_good_ref | Oracle `112f2902…`；Candidate `bb66a27`；evidence `50c158e3…` |

## W0-CLOSEOUT-DELTA-20261127（T2/T3）

| 欄 | 內容 |
|---|---|
| Change | W0 closeout delta：NF-T01 child／network observation、既有 40 案／NF-T08／T10/G17/W1 核銷、GitHub 交付 |
| NF-T01 | 保留 double-fail 拒絕、reviewer 動態定位、缺件 FAIL；新增 CPython audit observer（loader/import/open/call/child/os.system/loopback/ctypes），positive probe 全 true、absent-control 真拒；OFF 實跑 child=2（僅 guide→git 唯讀）、network=0、native=0、legacy attempts=0 |
| NF-T01 ceiling | OS-level sandbox、native 孫程序、`-S/-E/-I`、kernel egress、audit 只觀測不阻止；不以 Python audit 冒充 OS 隔離 |
| T3 核銷 | 40/40 reused receipts byte-identical；NF-T08 frozen contracts/Guide/chain 23/23/NEG 9/9/live NEG；T10 staging→finalize→final 無循環；G17 zero-read；W1 44 items |
| Final evidence | manifest `0ebbccf1…`；final consumer P7 `20261127T234153-ecdbff08`（863 checks，`consumed=true`）；receipt `14008922…`；handoff `3e5d6104…` |
| Docs fix | OpenSpec 41→40、NF-T05 reused；handoff G17 路徑 `07_CONSUMER/G17`；754 evidence 檔；INDEX 表頭與 checkpoint 對齊 |
| Push | T1 credential-assisted push：0099e95 → 5496cf5；T2 delta 後再推最終 commit 並回讀（見 CLOSEOUT／final report） |
| last_good_ref | Oracle `112f2902…`；Candidate `bb66a276…`；pack `e3772aee…`；content baseline `f1732144…` |