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
