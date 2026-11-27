# Checkpoint A／B 實證整合

## Checkpoint A（W0／W1）

| 項 | 實證 |
|---|---|
| W0 To-Be／AsBuilt | Foundation 44/44；`runs/w0_full/W0_FULL_RESULT.json` |
| W1 To-Be／AsBuilt | 13 案 12 PASS＋1 DEFERRED；67 ECP 61 PASS／1 PARTIAL／3 DEFERRED／2 NA |
| W1 產品能力 | 第二包 `SECOND_PACK.json`；115 tests；API 84 clauses；Guide 九鍵 |
| W2M～W4M 對位 | W2 控制包已用於 W2 施工；W3 介面為 `W3_CONSUMER.json`；W4 不在本輪 |

## Checkpoint B（W2／W3）

| 項 | 實證 |
|---|---|
| W2 AsBuilt | 12/12；DEV base `9fae9257a3402928efbe6ff0cd66f45761f52846`；OPS 七觀測 |
| Actual ChangeSet | W0 44、W1 67、W2 12；修補：gate ADD、host facade Invoked、TPM G3 profile、case dedupe |
| Authority／Effect／Recovery | decisions -05/-06；DEV reverse；OPS delete-created-only；UNKNOWN 四類 |
| W3 上游候選 | 五 pin `evidence/FIVE_PINS.json`；manifest `e5299bbb553eabdc…`；seal `f6dc5bb9aac2b626…` |
| W3 P01 Freeze | candidate aggregate `4874c347226afd33b204f5b0fae05f44fbeae6ac8e46d086d3420baf3a4d6988`；typed contracts（SECOND_PACK）；Checker／Consumer |
| W3 技術就緒 | `true`（contracts＋checker＋consumer＋pins） |
| W3 施工准入 | **`NOT_ADMITTED`**：未取得 W3 exact grant；未執行 W3 effect |

## 判定

- `CHECKPOINT_A=COMPLETE_SCOPED`
- `CHECKPOINT_B=COMPLETE_SCOPED`
- `W3_TECHNICAL_READY=YES`
- `W3_ADMITTED=NO`
