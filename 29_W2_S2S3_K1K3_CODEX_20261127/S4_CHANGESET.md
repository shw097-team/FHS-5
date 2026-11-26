# S4 回寫最小 ChangeSet（K1–K3）

- MASTER / W0_STATUS：W0 未重新資格化（NOT_CLAIMED）；歷史 44 receipts 保留。
- PROG-00 / SEAMS：W1/W2 Reader 新增 `SourceManifest.S1@1` dispatch；NF@1/NF@2 保留；`packloc.resolve_s1_pack` 明確區分 S1 與 NF。
- PROJ-01..05：無介面變更；Admission 由 `W1/authority/trust.json` 配置驅動（DEV/OPS 分域）。
- WM / W2：OPS-A 真 effect＋readback＋delete-created-only 補償；J2 九鍵 7/7；J3 ON/OFF parity 成立；N 系列未成套。
- 交付目錄：`29_W2_S2S3_K1K3_CODEX_20261127/`
- 候選：11 成員，canonical `f06b1be83a20b5a7c654ec1b445048be72e19aaf34f0db886f432c882c4cf07a`
