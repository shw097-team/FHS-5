# W0 CLOSEOUT（G3-FINAL-DELTA，2026-11-27）

- 控制包：`W0-G3-PCNF-r2`（G3 manifest `baa516b5675589c1a329cd5f65970d8d6c12b7892dd7c079115e1251c9e6e96d`）
- 執行 pack（sealed）：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- candidate：`bb66a276aae8c5d6aef549832c523587fc47d247`

## 真結果：**PARTIAL（41／44）**

| 項 | 結果 |
|---|---|
| 總數 | 44（24 Original＋10 NF＋10 SAMPLE） |
| PASS | **41** |
| FAIL | **2**：`NF-T01`（cold OFF contract mismatch）、`NF-T08`（`CONTRACT_CONTEXT_MISSING`；negatives `NEGATIVE_LEAK`） |
| Pending | **1**：`NF-T10` |
| Consumer | `20261127T192118-a43ed6da`：**consumed=false**、`RECEIPT_VERDICT`；failed 含 `RECEIPT-NF-T01`／`RECEIPT-NF-T08`／`CHALLENGE-ORACLE`／`COLLAB-VERDICT`／`OFF-off_legacy` |

## 血緣（本輪修正）

前輪 44/44 是對 `d3e5c258…` pack；與 seal 的 `e3772aee…` 不符。本輪已還原 sealed pack 並重跑：

- G3 控制 manifest：`baa516b5675589c1a329cd5f65970d8d6c12b7892dd7c079115e1251c9e6e96d`
- sealed／actual pack：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- 兩者不同，故 W0 不能沿用前輪 DONE；以 sealed pack 的 41/44 為準。

## 判定

**`W0_PARTIAL`**。不宣 `W0_DONE`、不宣 803/0。NF-T01／NF-T08 的契約上下文需補；NF-T10 需重綁 fresh consumer。
`runs/w0_full/delivery/` 保留 receipts／raw；`W0_FULL_RESULT.json` 為權威摘要。
