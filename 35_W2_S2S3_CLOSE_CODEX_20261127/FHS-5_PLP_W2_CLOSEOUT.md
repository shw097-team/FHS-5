# FHS-5_PLP W2 CLOSEOUT（第 35_ 輪）

## C1 真修補（Actual RED → GREEN）
| 缺陷 | RED | 修補 | GREEN |
|---|---|---|---|
| W2 case→runner 錯配 | DEV-01 被綁 `check/run_cases_nf.py`（W1 13 案 runner） | §4.1 per-case 綁定（runner＋status），TPM 同步帶欄 | **12 個不同 `RUN-*`**，DEV-01→`RUN-DEV-01`／`BUILD_MINIMAL` |
| consume 非 fail-closed | `if fx and orc`（Path 恆真）→ 缺 oracle 仍給 RUN | 逐項驗存在／sha／runner／status，typed 拒絕 | 缺 oracle → **`ORACLE_MISSING`**、exit 2、`STOP_SCOPED` |
| N04 語義 | Consumed 只驗 sha／選第一個 POS | 產生 scope-bound operation binding（subject/scope/case/runner/fixture/oracle sha） | **PASS** |

## 其他
- N06 4/4；ABI（9 DAG／16 列／12 案／18 子組）；7 案本輪真跑
- N09 **PARTIAL_REUSE**：`contracts_to_operation=false`（operation 段非本契約驅動）

## 判定
`W2_NF_VALIDATED` = **false**｜W2 technical **PARTIAL**｜W3 technical **PARTIAL**｜W3 execution **NOT_CLAIMED**

## NotCovered
N09 operation under contract；4 案歷史復用；R3-04 雙期。
