# G3 W0–W2 Native-first 施工包（2026-11-27）

本目錄是 `FHS-5_PLP_W0-W2_執行控制包_FINAL`（`PCNF-W0W2-ADOPT-20261127-01`）的實際施工結果。
所有 verdict 都來自本目錄下的真 raw；沒有 raw 的項目一律標 `NOT_RUN` / `DEFERRED` / `NotCovered`。

## 內容

| 路徑 | 作用 |
|---|---|
| `lib/g3pack.py` | G3 三包 strict reader（5 MD＋05＋assets＋cases＋work orders＋external seal） |
| `W0/run_w0.py` | 10 個 SAMPLE、R4 路徑變體、R10 output、44 receipts 核對、cold OFF |
| `W1/run_w1.py` | 13 原案、Guide 九鍵、四 API／BodyResolver、CODEX host ledger、67 ECP ledger |
| `W2/run_w2.py` | 12 原案；DEV-01 真 apply/test/reverse/restore；OPS-01 真 effect/WorldRaw/compensation |
| `check/checker.py` | 獨立 Checker（40 檢查，重導 predicate，不信 runner bool） |
| `check/consumer.py` | fresh W3 面向 Consumer（manifest／seal／checker／DEV／OPS 重讀） |
| `check/finalize.py` | redaction、五 pin、evidence manifest、外置 seal |
| `runs/` | 真 argv／exit／stdout／stderr／raw／pre-post hash |
| `evidence/` | `FIVE_PINS.json`、`EVIDENCE_MANIFEST.json`、`SEAL.json`、`CHECKER.json`、`W3_CONSUMER.json` |

## 重現

```powershell
python G3_20261127/W0/run_w0.py --pack <W0 pack> --out G3_20261127/runs/w0
python G3_20261127/W1/run_w1.py --pack <W1 pack> --out G3_20261127/runs/w1
python G3_20261127/W2/run_w2.py --pack <W2 pack> --out G3_20261127/runs/w2
python G3_20261127/check/finalize.py
python G3_20261127/check/checker.py
python G3_20261127/check/finalize.py
python G3_20261127/check/consumer.py
```

`runs/*/world`、`runs/*/off`、`_scratch` 是隔離執行目錄，不進版控；raw 只保留可讀觀測。

## 判定摘要

| Wave | 判定 | 主要缺口 |
|---|---|---|
| W0 | `SCOPED_PARTIAL` | 24 原案／10 NF-T 未重跑；44 receipts 為 reuse-verified |
| W1 | `SCOPED_PARTIAL` | HERMES-01 DEFERRED；67 ECP 只有 15 列本輪真 observed |
| W2 | `SCOPED_VALIDATED`（本 candidate／本 host） | 其他 Host、Publisher/Release、原域 DEV ECP |
| W3 | `TECHNICAL_READY`／`NOT_ADMITTED` | 需 W3 exact grant，未執行 W3 effect |
