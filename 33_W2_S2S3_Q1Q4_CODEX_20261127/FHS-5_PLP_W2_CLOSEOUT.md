# FHS-5_PLP W2 CLOSEOUT（Q1–Q4）

scope：`FHS-5_PLP/W2/CONTROL_PACK`｜candidate：16 成員 `cb66d77b…`｜five pins：`FIVE_PINS.json`

## Q1 真 ABI 修補（Actual RED → GREEN）
| 項 | RED | 修正 | GREEN |
|---|---|---|---|
| DAG | `parse_dag` 掃全文：42 列、32 空端點、1 表頭 | 只解析 §5.2、節點/kind/重複/空端點拒絕、cycle 自算 | **9 列、0 problems、無 cycle** |
| cases | 10 個 runner 空 | 由 03 §4 Runner 表綁定 | **12/12 有 runner** |
| DEV | locator 只有檔名 | 由 `## N｜DEV-D0x` 取真行號 | **7/7 有 line** |
| ENTRY | 以字串包含判章節 | 改判 `## ` heading | 7 章節 |
| 重複列 | 靜默忽略 | 真拋 `DUPLICATE_ROW` | 測試拒絕 |

契約 `ok=true`、`problems=[]`；CLI `--pack` exit 0；`115 passed / 15 subtests`。

## Q2 Host／E2E
- N01 **PASS**：TPM `S1-W2` profile，5 views（真 W2 六檔）
- N06 **PASS 4/4**：真子程序 timeout → TO-BEFORE／PARTIAL／EXIT0-WRONG／TO-AFTER，皆以檔案狀態分類
- N09 **PARTIAL**：source→reader→TPM→contracts 三段同 process、同 subject；operation 段仍來自 18_/W1
- N04 **PARTIAL**：僅 W1 歷史 host session，無當期 W2 served/consumed

## Q3 原義核銷
REUSE_VERIFIED 5｜RERUN_PASS 12｜NOT_RUN 2（W0 OFF、W1 67 ECP）｜REUSE_NOT_RERUN 1（R3-04）｜PARTIAL 2（N04/N09）

## Q4 正式驗收
- Checker **PASS**（15 檢查：pins、seal、ABI、DAG 9、WP6/HOLD14/CR37、OPS6、DEV7 locator、12 runner、16 rows、18 subcases、7 案、N06、115 測試）
- Fresh W3 Consumer **ACCEPT_PARTIAL**：`product_state=PARTIAL`、`w2_validated=false`（不升格）

## 判定
`W2_NF_VALIDATED` = **false**｜W2 technical **PARTIAL**｜W3 technical **PARTIAL**｜W3 execution **NOT_CLAIMED**

## NotCovered
N04 當期 Host、N09 單一 source、W0 OFF 重跑、W1 67 ECP 逐義、R3-04 雙期。
