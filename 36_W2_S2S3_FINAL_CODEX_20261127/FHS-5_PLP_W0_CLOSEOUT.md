# FHS-5_PLP W0 CLOSEOUT（第 36_ 輪）— **DONE（scoped）**

## 1. 假阻斷解除（真根因）
35_ 的 `CONSUMER_RECEIPT_SHA_DRIFT` 是**錯誤 locator**，不是收據漂移：

| 項 | 值 |
|---|---|
| Manifest `consumer_receipt` | `07_CONSUMER/clean_receive/receipt.json` |
| 該檔實際 SHA | `37d567e8b5c6f7a80edcbf61aa68df3569d316a66263122f17405dabdee24fb3` |
| Manifest pin | 同值（一致） |
| 35_ 誤讀 | `07_CONSUMER/consumer_receipt.json`（`7ca6b761…`，另一份收據） |

修正：adapter 改以 Manifest locator 解析＋containment 檢查；負例改用**同一入口**對篡改 bytes 重呼（`RECEIPT_SHA_MISMATCH`），不再自填 `accepted=false`。

## 2. NF／S1 血緣
S1 包以自身 pin（`97017494…`）＋外 seal 驗證；歷史 NF 收據以自身 pin（`e3772aee…`）驗證；兩者以 S1 `05.upstream.original_manifest_sha256` 接續，**不強制等值**。

## 3. Fresh W1 consume（正向）
`EVIDENCE/W0_CONSUME.json`：accepted=true，receipt 803 checks／0 failed、validated/consumed、cli pos_exit 0／neg_exit 2／semantics_ok；44 receipts 全 PASS；14 WP。

## 4. OFF
沿用 34_ 隔離重跑：7/7 PASS、`control_ok=true`（`EVIDENCE/W0_OFF.json`）。

## 判定
**W0 DONE（scoped）**：S1 入口＋OFF＋fresh consume＋44/803 均成立；未重跑 44 案（歷史 REUSE）。
