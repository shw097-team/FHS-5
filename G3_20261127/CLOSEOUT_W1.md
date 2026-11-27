# W1 CLOSEOUT（G3-FINAL-DELTA，2026-11-27）

- candidate：`W1-G3-PCNF-r2`；manifest `f00b4ee93611e738e409d40758aa320b0bfec3ef0a01fea04dbf5bcb9f1566dc`
- 13 原案：**12 PASS＋1 DEFERRED**（HERMES-01）

## 67 ECP measured（v2，predicate 計算）

`runs/w1/raw/ECP67_MEASURED.json`：**51 OBSERVED／10 NOT_ADMITTED／1 PARTIAL／3 DEFERRED_HOST／2 REASONED_NA**。

- 不再有固定 PASS 表：每列由 predicate 讀 actual artifact 計算。
- `NOT_ADMITTED` 為 W2 受保護效果在無外部 ISSUED grant 下的正確結果。
- PARTIAL：`OPS-POST-03`（同 principal）。
- DEFERRED_HOST：ChatGPT、Hermes（2 列）。
- REASONED_NA：install／registration recovery。

## 第二工作包（R-001 修復）

- G3 三欄 ECP 表現在正確解析成 `rows`；`DEV-D01` 等 ID pattern 修正。
- Reviewer：**兩包 findings=0、first_fail=null**；`SECOND_PACK.json` **PASS**。
- W1 13 案／W2 12 案五視圖：PI/PD/DEV/OPS/TQAEP＝12/8/7/7/8。
- 115 tests OK。

## 判定

**`W1_SCOPED_PARTIAL`**：產品能力與第二包已閉合；剩餘為外部 Host／第二 principal 與 W2 admission 依賴。
