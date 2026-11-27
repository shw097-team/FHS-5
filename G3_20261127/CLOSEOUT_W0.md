# W0 CLOSEOUT（G3，2026-11-27）

- candidate：`W0-G3-PCNF-r2`
- source manifest SHA-256：`baa516b5675589c1a329cd5f65970d8d6c12b7892dd7c079115e1251c9e6e96d`
- pack tree SHA-256：`e21ad49c2ab1742bd2a0d2f2dfd973522bbf755c820127b4936b8d432776b71d`
- case set SHA-256：`da6fa6f3615f4043c90045089ee355c5888036d2900e3cdf646e9120e7db2d81`
- raw：`G3_20261127/runs/w0/`；summary：`runs/w0/W0_RESULT.json`

## 實際完成

| 項 | 觀測 | verdict |
|---|---|---|
| SAMPLE R1–R10 | 真 subprocess；exit／status 對 frozen oracle | **10/10 PASS** |
| R4 路徑 | `../`、absolute、UNC、junction（真 `mklink /J`）皆 `INVALID_PATH`；canary SHA 前後相同 | PASS |
| R10 output | 真 output 檔、source SHA 不變、刪除回 absent | PASS |
| 44 receipts | 13_/05_TQAEP/receipts 44 檔；cohorts {'original': 24, 'NF': 10, 'SAMPLE': 10}；全部 parse＋必要欄 | **REUSE_VERIFIED 44/44** |
| cold OFF | forbidden provider 由 meta_path 阻擋；正控觸發 `BLOCKED_IMPORT`；OFF 執行仍 COMPLETE | PASS |

## 判定

`W0_SCOPED_PARTIAL`。SAMPLE 十案與 OFF／路徑／output 為本輪真跑；44 receipts 只作同 scope 血緣復用，未重跑。
不宣 `B0_VALIDATED`，不宣 `F5-W0-T01..T24` 或 `NF-T01..T10` 產品 PASS。

## 未閉項

- `F5-W0-T01..T24`（24）本輪 `NOT_RUN`；需原 runner／原 Host raw。
- `NF-T01..T10`（10）本輪 `NOT_RUN`；OFF 只覆 R 層。
- 803 consumer checks 為歷史另帳，未在本輪重跑。
