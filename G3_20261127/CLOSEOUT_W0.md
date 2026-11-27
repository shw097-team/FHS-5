# W0 CLOSEOUT（G3，2026-11-27）

- candidate：`W0-G3-PCNF-r2`；source manifest `baa516b5675589c1a329cd5f65970d8d6c12b7892dd7c079115e1251c9e6e96d`
- pack tree `e21ad49c2ab1742bd2a0d2f2dfd973522bbf755c820127b4936b8d432776b71d`；case set `da6fa6f3615f4043c90045089ee355c5888036d2900e3cdf646e9120e7db2d81`
- 全量 raw：`G3_20261127/runs/w0_full/delivery/`；摘要 `runs/w0_full/W0_FULL_RESULT.json`
- 代表切片：`G3_20261127/runs/w0/`

## 全量 44 案（本輪真跑）

| cohort | 數量 | 結果 |
|---|---:|---|
| Original `F5-W0-T01..T24` | 24 | PASS |
| NF `NF-T01..T10` | 10 | PASS |
| SAMPLE `R1..R10` | 10 | PASS |
| 合計 | 44 | **44 PASS／0 FAIL／0 PENDING** |

- 執行：candidate 由 `repo.bundle` materialize 至 `bb66a276…`，`tools/tqaep_run.py` 真跑 44 案；receipts／raw 見 `delivery/05_TQAEP/`。
- fresh consumer：`20261127T181933-cb670f34`，`consumed=true`、**803 checks／0 failed**；`07_CONSUMER/` 與 `10_EVIDENCE/EVIDENCE_MANIFEST.json`。
- NF-T10 由 consumer 後置 receipt 綁定（`tools/finalize_t10.py`），非自填。

## 代表切片（保留）

SAMPLE 10/10、R4 `../`／absolute／UNC／真 junction、R10 output/restore、cold OFF＋`BLOCKED_IMPORT` 正控：`runs/w0/raw/`。

## 判定

**`W0_DONE`（package 分母 44/44）**。`44 receipts` 不再只是 reuse：本輪為 fresh run；歷史 receipts 另存不覆寫。
`B0 product validation` 仍不宣（W0 是 Foundation；非 W0M 產品驗收）。

## NotCovered

- HERMES／GPT host execution（W0 不適用；W1/W2 另帳）。
- FHS 485 full regression（原包 DEFER）。
