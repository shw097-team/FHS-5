# W0 HANDOFF（G17 真消費入口，W0 → W1）

- **verdict**：`W0_DONE`（scoped：local CODEX／Windows、Generic B0-NF、44/44；非 W1–W4、非整體 MVP、非 release）
- **branch**：`codex/w0-w2-g3-native-20261127`
- **T1**：content `f1732144…`；docs `dda7779…`；metadata `5496cf5…`
- **T2**：content `c421c5a…`；docs `fad50e1…`；metadata `f60c15e…`
- **T3**：content `a8c37de6796e875dd82b0a55ae19303cd02ed5f2`；docs/evidence 本檔所在 commit
- **pack_manifest_sha256**：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- **w0m_amendment_sha256**：`c9b1ca9bbcd5ce87fdbcb0fc373cb8c36d1ad8d404b55c4f7311fc6c2bbddfd5`
- **candidate_commit**：`bb66a276aae8c5d6aef549832c523587fc47d247`
- **candidate_preimage**：`5eab43de2d3f67d6afbb1c5f6bc390e2c391da36`
- **oracle_sha256**：`112f2902656f1122720ef275ac954e3422f896267f144f27d321fa138be382c6`
- **evidence_manifest_sha256**：`12ddc3c3f9b6805d1c9657e2e110a5ef87231bd6b78c090b1d94c6ad3fc0e26a`
- **handoff_sha256**：由 final consumer receipt 實算；本檔不自填
- **run root**：`C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\g3-20261127\G3_20261127\runs\w0_close_20261127\13`
- **final consumer P8**：`20261128T000245-5dc3792c`，863 checks，`consumed=true`，receipt sha256 `1b4bbcc96df5ecde55dcf5c8337b493fbf5fff13b09e053d83ab021dd2e2a63c`
- **NF-T10 finalize**：`20261127T225645-015592e8`（810 checks，pre-final staging）
- **W1 consume**：`w1_out_pos/`，44 items、readback true；checklist `96e66d6f…`；consume receipt `cc872413…`
- **G17 full**：POS／單 byte NEG `RECEIPT_SHA_MISMATCH`／outside locator `RECEIPT_LOCATOR_OUTSIDE`／audit zero outside read；`g17_full/G17_SUMMARY.json` PASS
- **independent checker**：`03_PARTIES/challenge/challenge.json` PASS 32 checks／0 findings
- **remote**：T1 `0099e95 → 5496cf5`；T2 `5496cf5 → fad50e1`，metadata `f60c15e`；T3 待 push 後回讀（見 final report）

## next minimal W1 action

1. 讀 `09_DELIVERY/W0_HANDOFF.md` 與 `w1_out_pos/w1_checklist.json`（44 items）。
2. 以本 pins 為基線 requalify 原 14 HOLD／R3-CR；先做來源與 W1M 差額，不重跑 W0。
3. W1 產品施工另需上位採納、W1M／下一包一致與真入口／授權。

## not covered

W1–W4 全分母、FHS 485、HERMES／GPT Host、不同 principal 簽章、Publisher/Release、Fabric/Legacy 全量、OS 級 child/network 隔離、契約外部 canonical pin。10 個 SAMPLE item 的 `raw_refs` 為空，但有有效 `receipt`＋`receipt_sha256` locator。詳見 `CLOSEOUT_W0.md`。

## paths

- C/H：`G3_20261127/CLOSEOUT_W0.md`、`G3_20261127/HANDOFF_W0.md`
- evidence：`runs/w0_close_20261127/13/10_EVIDENCE/EVIDENCE_MANIFEST.json`
- receipts：`runs/w0_close_20261127/13/05_TQAEP/receipts/`
- consumer：`runs/w0_close_20261127/13/07_CONSUMER/CONSUMER_MANIFEST.json`
- G17：`runs/w0_close_20261127/g17_full/`
- W1：`runs/w0_close_20261127/w1_out_pos/`
- T3 核銷：`runs/w0_close_20261127/agents/t3/T3_VERIFICATION.md`