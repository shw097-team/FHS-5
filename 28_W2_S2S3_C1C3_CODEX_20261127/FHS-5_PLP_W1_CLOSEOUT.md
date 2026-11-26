# FHS-5_PLP W1 CLOSEOUT（C1–C3 本輪）

## 真跑
- `W1/check` 全套 pytest：**106 passed、15 subtests**（修正 packloc 後；基線為 19 failed／25 errors）。
- `run_cases_nf`（13 案）：17 PASS／1 DEFERRED／1 NOT_RUN（ACC W1-CODEX-05）／1 NOT_OBSERVED（前輪同包實跑，本輪未重跑）。
- W1→W2 真接收：本輪在 OPS-A 中由 `receive()` 對 `18_W1_NF_…` 完成 118 檔 verify＋consume（accepted=true）。

## 未完成
- 67 ECP 未逐項重核；118-row Closure Matrix 未逐列重開。
- `W1-HOST-01`、`W1-CODEX-05` 第二真包未於本輪重跑（沿用歷史 Raw）。
- S1 `SourceManifest.S1@1` schema 接線未完成：Reader 仍以 NF 包 pin 運作。

## 判定
W1 validated = **PARTIAL**（suite 與接收真成立；ECP 原義與 S1 schema 未完成）。
