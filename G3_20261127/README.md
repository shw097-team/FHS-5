# G3 W0–W2 Native-first 施工包（G3-FINAL-DELTA，2026-11-27）

本目錄為真狀態交付；verdict 均來自在場 raw，沒有把 request 當 grant。

| Wave | 判定 | 主要數字 |
|---|---|---|
| W0 | `PARTIAL` | 41 PASS／2 FAIL（NF-T01、NF-T08）／1 pending（NF-T10）；consumer 拒絕 |
| W1 | `SCOPED_PARTIAL` | 12/13；67 ECP 51 observed／10 NOT_ADMITTED／1 partial／3 host／2 NA；第二包 PASS；115 tests |
| W2 | `NOT_ADMITTED` | 9 PASS＋3 NOT_ADMITTED；UNKNOWN 4/4；N09 NOT_ADMITTED |
| W3 | `NOT_ADMITTED` | contracts／pins／checker 可用；無 ISSUED grant |

模組：`lib/g3pack.py`、`W0/run_w0.py`、`W1/run_w1.py`＋`run_ecp.py`＋`run_second_pack.py`、
`W2/run_w2.py`＋`run_unknown.py`＋`n09_chain.py`、`check/checker.py`／`consumer.py`／`finalize.py`。

R04 信任邊界：`run_w2.py` 只產生 `REQUEST_ONLY` decision；`w2_admission` 拒絕非 `ISSUED`；
`dev_driver.py` 不再由 caller 設定 write root／allowed ops；`ops_receiver.py` 需外部 ISSUED admission。

文件：`CLOSEOUT_W*`、`HANDOFF_W*`、`INDEX.md`、`CHECKPOINT_AB.md`。
