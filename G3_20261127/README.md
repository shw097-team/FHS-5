# G3 W0–W2 Native-first 施工包（2026-11-27）

實際施工結果；verdict 均來自在場 raw。

| Wave | 判定 | 主要數字 |
|---|---|---|
| W0 | `W0_DONE`（package 分母） | 44/44；consumer 803/0 |
| W1 | `W1_SCOPED_PARTIAL` | 12/13；67 ECP 61 PASS；第二包 PASS；115 tests |
| W2 | `W2_SCOPED_VALIDATED` | 12/12；UNKNOWN 4/4；N09 PASS |
| W3 | `TECHNICAL_READY`／`NOT_ADMITTED` | 未取得 exact grant |

模組：`lib/g3pack.py`、`W0/run_w0.py`、`W1/run_w1.py`＋`run_ecp.py`＋`run_second_pack.py`、
`W2/run_w2.py`＋`run_unknown.py`＋`n09_chain.py`、`check/checker.py`／`consumer.py`／`finalize.py`。
文件：`CLOSEOUT_W*`、`HANDOFF_W*`、`INDEX.md`、`CHECKPOINT_AB.md`。
