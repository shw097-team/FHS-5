# W0 HANDOFF

- 真狀態：41 PASS／2 FAIL（NF-T01、NF-T08）／1 pending（NF-T10）；consumer 拒絕。
- raw：`runs/w0_full/delivery/`；摘要 `W0_FULL_RESULT.json`。
- 下一合法 action：補 NF-T08 契約上下文、修 NF-T01 cold OFF、重綁 NF-T10；或接受 W0 PARTIAL。
- 不得：把前輪 44/44（d3e5 pack）當 sealed pack 結果。
