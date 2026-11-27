# G3 工程衛生整理（2026-11-27）

## 分層判定

| 項目 | 位置 | 判定 |
|---|---|---|
| G3 控制包 | `FHS-5_PLP_W0-W2_第三代Native-first_執行控制包_FINAL/` | 主用（文件），未改 bytes |
| G3 施工交付 | `G3_20261127/` | **候選（未升格主用）** |
| 36_ S2/S3 | `36_W2_S2S3_FINAL_CODEX_20261127/` | `W2_CURRENT.json` 仍為主用指標；G3 未取代 |
| 歷史 13_／W1 | 原目錄 | 不動；G3 只讀引用 |

## 為何不升格

- W0：41/44（NF-T01、NF-T08、NF-T10）。
- W1：12/13；67 ECP 51 observed／10 NOT_ADMITTED／1 partial／3 host。
- W2：9 PASS＋3 NOT_ADMITTED（無 ISSUED grant）。
- W3：NOT_ADMITTED。

未達原包驗收，故 G3 保持候選，不併入 `main`、不改 `W2_CURRENT.json` 的 adopted primary。

## 保留／刪除

保留：`runs/w0_full/13`（sealed-pack run root，含 receipts/raw）、`w0_full/delivery`、`w2/raw`、`w2_selfauth_prior/raw`、`w1/raw`、`evidence/**`。
刪除：`w0/world`、`w0/off`、`w0/cli`、`w2/dev/world`、`w2_selfauth_prior/dev|ops`、`__pycache__`。
理由：可重建、非唯一證據；證據 root 不動。`RUN_RECORD.json` 記錄重建方式。

## 安全

- 遠端 tree 無 credential／temp 檔。
- 本地 `w2_selfauth_prior` 僅為歷史證據，不作為 grant。
