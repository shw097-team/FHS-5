# FHS-5_PLP W1 HANDOFF（C1–C3 本輪）

- pack：`FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1-r2`（manifest `d1c74153…`）與歷史 `18_W1_NF_…`（pin `61f34a08…`）
- candidate：`W1/check/*`（106 綠）＋ `packloc.py` 可攜解析
- oracle/case-set：`run_cases_nf` 13 案；raw 於 `EVIDENCE/raw/W1_CASES`
- checker/consumer：本輪以 OPS-A 的 fresh consumer 對 W1 材料做真 parse（requirements=13）
- readiness：W1 technical = PARTIAL
- next_legal_action：`C1-W1-S1SCHEMA`（Reader 接受 `FHS5.PLP.W1.SourceManifest.S1@1` 並真核 identity/required fields）
- owner/resume：Owner 不變
