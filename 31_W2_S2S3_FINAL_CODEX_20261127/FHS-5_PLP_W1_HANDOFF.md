# FHS-5_PLP W1 HANDOFF（K1–K3）

- pack：`d1c74153…`（`S1_PACKS/FHS-5_PLP_W1_NATIVE_FIRST`）
- candidate：`W1/impl/s1_reader.py`、`W1/check/packloc.py`、`W1/check/run_off_task.py`
- oracle：S1 seal `593314d5…`；W2M §03.1 sha `2b98be96…`
- evidence：`EVIDENCE/TESTS_K1_FINAL.stdout.txt`、`J3_ONOFF.json`
- checker/consumer：J2/J3 以真 artifact 產生九鍵與投影；fresh consumer 於 28_ 對 W1 材料 readback
- next_legal_action：`K2-W1-ECP`（67 ECP 逐義）、`K1-W1-HOST`（Host/第二包重跑）
- readiness：W1 technical = PARTIAL
