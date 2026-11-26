# SUPERSEDED

本目錄（`21_W2_PRODUCT_HERMES_20261126/`）是 **r1（HERMES-F5-W2-PRODUCT-r1）** 的歷史交付，已被後續輪次取代。

## 不要引用本目錄的下列內容

| 檔案／欄位 | 問題 | 正確值所在 |
|---|---|---|
| `FHS-5_PLP_W2_CLOSEOUT.md` 的 `pre_world_digest` = `49c62def3da070a1…` | **寫錯**的值；真實 pre-world 狀態是空集合 | `44136fa3…`（O03／O05／ledger 三處一致） |
| `W2_CASE_LEDGER.json` | 12 案多為 `NOT_RUN`／`STRUCTURAL_ONLY`，非本輪結果 | `24_W2_SCOPED_REPAIR_HERMES_20261126/` |
| `receipts/` 內 OPS 收據 | 有效（10/10、4/4），但屬 r1 run root | 可作歷史證據，不作 current |

## 現行交付

`25_W2_FINAL_HANDOFF_HERMES_20261126/`，入口見 repo 根 `W2_CURRENT.json`。

## 保留理由

本目錄保留作血緣與失敗記錄：r1 的 J1 紅燈（三缺陷）與 `NOT_RUN` 判定是後續 r2–r4b 修補的依據，刪除會使 Finding 失去原始出處。**只讀，不引用為現況。**
