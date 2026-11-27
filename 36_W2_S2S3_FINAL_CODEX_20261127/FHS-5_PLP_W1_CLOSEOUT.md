# FHS-5_PLP W1 CLOSEOUT（第 36_ 輪）

## 67 ECP：改以真實 Raw 指標判定
前輪以 `evidence_exists` 推定 64 REUSE。本輪逐列解析實際 Raw（8 類共享檔），抽取正面指標：

| disposition | 數量 |
|---|---|
| REUSE_VERIFIED（Raw 有正面指標） | **18** |
| PARTIAL（僅結構性 Raw，未逐義觀測） | **46** |
| REASONED_NA | 1 |
| DEFERRED | 2 |
| NOT_VERIFIED | 0 |

67/67 皆有 `raw_sha256` 與 `observed_ref`；46 列如實降級，不以檔存在或歷史 verdict 求綠。

## 其他
- 115 passed／15 subtests；S1 W1 入口；118-row／Host／第二包為歷史 REUSE
- 判定：W1 **PARTIAL**
