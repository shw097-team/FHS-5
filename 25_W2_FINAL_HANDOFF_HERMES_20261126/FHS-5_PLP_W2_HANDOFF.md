# FHS-5_PLP_W2_HANDOFF（最終版｜給全新 SESSION）

**from**：`W2-FINAL-DELTA`（本 session 終點）
**to**：W3 P01（Primary Operator），或 Owner 決定重開 W2 時的接續者
**handoff_id**：`W2-NF-HANDOFF-20261126-05`
**baseline commit**：`dada2354b7c25c8f4a316d9fae93827cef0d194e`（branch `hermes/w2-product-20261126`，tree `9b20abed003f`）
**repo**：https://github.com/shw097-team/FHS-5
**狀態**：`PARTIAL` — 受影工作閉環，缺陷已具名，未達 `W2_NF_VALIDATED`

---

## 00｜三十秒上手

```
讀 repo 根 W2_CURRENT.json  →  它指出 current 交付、主用包、superseded 清單與 claim 狀態
再讀 25_W2_FINAL_HANDOFF_HERMES_20261126/FHS-5_PLP_W2_CLOSEOUT.md
```

**不要**從 `21_`／`22_`／`23_` 開始讀（superseded，`21_` 有錯的 digest，已加 SUPERSEDED 標記）。

---

## 01｜接手前必須知道的三件事

### 1.1 保護寫入目前是停用的，而且這是正確的

`W2_NATIVE_RUNS/W2_SECURITY_FINDING.json` 存在 → `derive()`／`require()`／`apply_patch()` 一律拒絕（`ADMISSION_TERMINATED_BY_SECURITY_FINDING`）。這不是故障，是原 Owner 決策「有效期至出現安全 Finding 為止」的兌現。

**要重開 protected writer，唯一路徑是 Owner 重新授權**，內容需含：`subject/scope`、`allowed_roots`（真路徑）、`targets`、`ops`（MODIFY/ADD/DELETE 逐項）、`effect`、`有效期`、`recovery`。不得在 chat 收集口令；不得自建收集器；Token／私鑰不得進模型、子代理、argv、日誌、Git。

### 1.2 沒有任何東西被升格為主用

四輪（r1→r4b→final-delta）都沒有讓 `W2_NF_VALIDATED` 成立，因此依契約不得升格、不得 merge main。`main` 停在 `c2d8084`。若 Owner 要合併，那是**新的決策**，不是本 handoff 的隱含授權。

### 1.3 本 session 修正了套件層的兩個真缺陷

- 新增 `W2_CURRENT.json`（原本 21/22/23/24 並列、無指標）
- 新增 `21_.../SUPERSEDED.md`（原本含錯的 `pre_world_digest` `49c62def`，真值 `44136fa3…`）

---

## 02｜可用的實績（真的跑過、有 raw）

| 項目 | 結果 | 原始證據位置 |
|---|---|---|
| J1 獨立 oracle | 21/21 PASS | `20261126T1121_W2_PRODUCT/30_VERIFY/raw/CHECKER_J1_ORACLE.json` |
| J1 strict（maker 測試） | 6/6 | `…/20_DEV/worktree/W1/check/test_j1_receiver.py` |
| S1 v2（保護寫入閘） | 13 PASS / 0 FAIL / 1 RESIDUAL_LIMIT | `…/50_EVIDENCE/S1_VERIFICATION.json` |
| S1 delta（四差額＋事件撤權） | 6 PASS / 0 FAIL | `…/50_EVIDENCE/S1_DELTA.json` |
| S2 E2E ON/OFF | 23/23 PASS，15 typed 鍵一致 | `…/50_EVIDENCE/S2_E2E.json` |
| OPS O03／O04／O05 | 8 檔世界效果｜10/10 VERIFIED｜4/4 RECOVERED | `20261126T1121_W2_PRODUCT/50_EVIDENCE/ops/` |
| 12 原案 runner | 10/10（另 2 案由他案成立） | `20261126T1225_W2_FINAL_CLOSURE/…/W2_CASE_LEDGER.json` |
| W3 clean receive | 15/15（r2）｜16/16（r3，對 `ef325c1`） | `22_…/W3_RECEIVE_RECEIPT.json`、`23_…` |
| Candidate 5 檔 | aggregate `8b4b4068…`（完整值見五 pins） | `24_…/W2_FIVE_PINS.json` |
| frozen ECP | `ec26f6a2…` | `20261126T1121_W2_PRODUCT/00_PREFLIGHT/P03_DEV_D04_frozen_ecp.json` |

上述皆為**受影證據**，不是 `W2_NF_VALIDATED`。

---

## 03｜W3 P01 待接續（依序）

| # | 待辦 | 前置 | 完成判準 |
|---|---|---|---|
| 1 | **Owner 重新授權**（若需重開 writer） | Owner 決策 | 具名 receipt，含 roots/targets/ops/有效期/recovery |
| 2 | 12 原案 oracle／case-set **真凍結** | 無 | 逐案 fixture/oracle bytes＋digest；現為 `CARRIED_NOT_REFROZEN` |
| 3 | evidence **逐 raw 封存**＋外置 seal | #2 | 現僅 manifest 級（`SEALED_AFTER_OBSERVED`） |
| 4 | 對 `dada235` 候選取**獨立覆核 receipt** | #1 | 分立 Verifier 對同候選 PASS（現 `INDEPENDENT_PASS` NOT_CLAIMED） |
| 5 | J3 ON/OFF 對**當期**候選重跑 | #1 | 兩邊語義成功、投影一致、禁用 import 零 |
| 6 | W3 主用包與 W3M 接收契約 | W3 Owner | 現 `W3_PACK_ABSENT`，不得先建 Consumer |
| 7 | （可選）Owner 決定是否 merge main | Owner | 合併需明示授權；本 session 未動 main |

**不要做的事**：不要把 15/16/23/21/13 這些數字相加成「已通過」；不要用舊 SP 的 PASS 抵當期；不要改 oracle 求綠；不要以 HERMES 成功冒充 CODEX 產品成功。

---

## 04｜陷阱清單

| 陷阱 | 說明 |
|---|---|
| `21_` 的 CLOSEOUT | 含錯的 `49c62def…`；真值 `44136fa3…`。已加 SUPERSEDED |
| `W2_FIVE_PINS.candidate` | 名為 candidate 是**正確**的，不是漏升格 |
| 兩個 W3 收據 | 15/15 對 `ce4f10f`（r2）、16/16 對 `ef325c1`（r3）；都不是當期 |
| `RESIDUAL_LIMIT` | `sys.modules` 僞造不在防線內，這是已揭露的限制，不是待修 bug |
| `R` 不是 `main` | R 的工作樹在 `codex/b0-nf-20261125`（`c2d8084`），產品在 `hermes/w2-product-20261126`。**先 `git switch`／建 worktree，不要誤以為 R 的 HEAD 就是產品 HEAD** |
| SQS 根 | `SQS-THC_MVP_Workspace` 另有授權 session 在跑，不要介入 |

---

## 05｜環境

| 工具 | 版本 |
|---|---|
| Python | 3.14.9（另有 CPython 3.12.13） |
| git | 2.56.1 |
| codex-cli | 0.164.0 |
| openspec | 2.0.0 |
| hermes | v0.23.3 |

GitHub 認證：`C:\Projects\Agent_Workspace\API KEY\GITHUB-REPO_SHW097-4.txt`，僅經臨時 `GIT_CONFIG_GLOBAL` 的 `http.extraheader` 注入，token 不落 argv／log／repo。

---

## 06｜Resume predicate（一句話）

> 當 Owner 對 `W2-NF-01` 給出新的具名授權（roots／targets／ops／有效期／recovery），且 12 原案 oracle 已用真 bytes 凍結，即可在 `dada235` 之上重開 protected writer，並對同一候選重跑 J1／J3 與獨立覆核。

---

## 07｜Not covered

`W2_NF_VALIDATED`、`W3_TECHNICALLY_READY`、`W3_EXECUTION_READY`、`INDEPENDENT_PASS`、`RELEASED`、`primary-use 升格`、`merge main`。
