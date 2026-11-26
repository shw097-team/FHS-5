# S4 最小 ChangeSet（Oracle-driven）

- PROG-00：S1 Reader 新增 `SourceManifest.S1@1` dispatch（W0/W1/W2），保留 NF@1/NF@2。
- PROJ-01：`s1_reader` 提供 manifest/source_set_sha256/source_refs/requirements（含 material 狀態）。
- PROJ-03：gate 增結構預檢（write-set/preimage/recovery 先行），拒絕 token 更精確。
- WM：W2 7 原案 NEG/POS 成立；requirement bodies 仍缺（16 declared vs 4 ids）。
- 交付：`30_W2_S2S3_ORACLE_CODEX_20261127/`（candidate `f8b5e89d…`）
