# W0 HANDOFF

- 已驗：SAMPLE 10/10、R4（含 junction）、R10 output、44 receipts reuse、cold OFF＋正控。
- raw：`runs/w0/raw/`（SAMPLE-R1..R10、R4-variants、R10-output、receipts-44、OFF）。
- 未驗：`F5-W0-T01..T24`、`NF-T01..T10`、803 consumer checks。
- 下一合法 action：在 Owner 指定 repo／runner 下重跑 24 原案；或接受 W0 scoped partial 並把 W1 已驗切片作下游輸入。
- 不得：把 44 reuse 當 44 PASS；把 SAMPLE 當 B0 全量。
