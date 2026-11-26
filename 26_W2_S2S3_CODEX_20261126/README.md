# 26_W2_S2S3_CODEX_20261126

本目錄是本輪 S2／S3 的實際施工與證據，不覆寫 19／21–25。

- 施工基線 commit：`3346076c69b00d65e48fdb9ddf894ac4cc09524b`
- 受閘 world：`W2_NATIVE_RUNS/S2S3_20261126T225929/20_WORLD`（本機，不入 repo）
- 決策：`DECISION/W2_OWNER_DECISION_S2S3.json`（generation-2，僅二檔 DEV）
- 舊決策 `W2-NF-PRIMARY-20261126-01` 仍 terminated，未復活

## 本輪實跑

| 項 | 結果 |
|---|---|
| 安全矩陣 S1–S12 + P1–P7 | 19/19 PASS，拒絕皆 wrote=[] |
| DEV-A | gate apply → pytest 15 passed → 真 readback → reverse 還原 |
| 修補前探針 | RED_ACCEPTED（unlisted entry、junction alias） |
| 修補後探針 | GREEN |
| W1 13 案 runner | {'NOT_OBSERVED': 1, 'PASS': 17, 'DEFERRED': 1, 'NOT_RUN': 1} |
| W1 全套 pytest | 修補前 19F/48P/25E；修補後 19F/50P/25E（+2 為新增 J1-T07/T08，無回歸） |

既有 19 failed／25 errors 為 reader 的 PACK pin 與本樹狀態不符，基線同樣存在，非本輪引入；
如實保留，未以 PASS 冒結案。

## 未成立

- `W2_NF_VALIDATED`：12 原案、OPS-A、J3 未真跑。
- W3 technical／execution readiness 未宣。
