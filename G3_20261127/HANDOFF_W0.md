# W0 HANDOFF（W0 → W1）

- **verdict**：`W0_DONE`（scoped：local CODEX／Windows、Generic B0-NF、44/44；非 W1–W4、非整體 MVP、非 release）
- **branch**：`codex/w0-w2-g3-native-20261127`
- **T1 content**：`f173214428f1d3b4ea3819182ddb8a6a67cc34f1`
- **T1 docs/evidence**：`dda7779464abf3b6d7cbaeee8a9fbcc93c471137`
- **T1 push metadata**：`5496cf55bc04b8409359f882952bd872f1ddbb88`
- **T2 content**：`c421c5a7856e397b37170f5401b9f7fe973b74fa`
- **T2 docs/evidence**：`fad50e1f3500107c8847e874dcb23ae4ec7a7a59`
- **pack_manifest_sha256**：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- **w0m_amendment_sha256**：`c9b1ca9bbcd5ce87fdbcb0fc373cb8c36d1ad8d404b55c4f7311fc6c2bbddfd5`
- **candidate_commit**：`bb66a276aae8c5d6aef549832c523587fc47d247`
- **candidate_preimage**：`5eab43de2d3f67d6afbb1c5f6bc390e2c391da36`
- **oracle_sha256**：`112f2902656f1122720ef275ac954e3422f896267f144f27d321fa138be382c6`
- **evidence_manifest_sha256**：`0ebbccf1f09837629b3cb2960dd476c440937f77cc80d4e8ee3d8fdcd3a92527`
- **handoff_sha256**：由 final consumer receipt 實算；本檔不自填
- **run root**：`C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\g3-20261127\G3_20261127\runs\w0_close_20261127\13`
- **final consumer P7**：`20261127T234153-ecdbff08`，863 checks，`consumed=true`，receipt sha256 `1400892233a1246abcf5aefdcba846bbb7bfa3084998a6284e555b9865fd7db2`
- **NF-T10 finalize**：`20261127T225645-015592e8`（810 checks，pre-final staging）
- **G17**：POS／單 byte NEG／zero-read audit 全 PASS（`07_CONSUMER/G17/`）
- **fresh W1 minimal**：44 items、readback_ok；`07_CONSUMER/W1_MIN_CONSUME/`；checklist sha256 `49bd3a83…`（P7 重跑後）
- **independent checker**：`03_PARTIES/challenge/challenge.json` PASS 32 checks／0 findings
- **remote（T1）**：`0099e95… → 5496cf5…`
- **remote（T2）**：`5496cf5… → fad50e1…`，已回讀；T2c metadata commit 只記 readback

## next minimal W1 action

1. 讀 `09_DELIVERY/W0_HANDOFF.md` 與 `07_CONSUMER/W1_MIN_CONSUME/` 的 44 項 checklist。
2. 以本 pins 為基線 requalify 原 14 HOLD／R3-CR；先做來源與 W1M 差額，不重跑 W0。
3. W1 產品施工另需上位採納、W1M／下一包一致與真入口／授權。

## not covered

W1–W4 全分母、FHS 485、HERMES／GPT Host、不同 principal 簽章、Publisher/Release、Fabric/Legacy 全量、OS 級 child/network 隔離、契約外部 canonical pin。詳見 `CLOSEOUT_W0.md` 的「日後待升級區」與 claim ceiling。

## paths

- C/H：`G3_20261127/CLOSEOUT_W0.md`、`G3_20261127/HANDOFF_W0.md`
- evidence：`runs/w0_close_20261127/13/10_EVIDENCE/EVIDENCE_MANIFEST.json`
- receipts：`runs/w0_close_20261127/13/05_TQAEP/receipts/`
- consumer：`runs/w0_close_20261127/13/07_CONSUMER/CONSUMER_MANIFEST.json`
- G17／W1：`runs/w0_close_20261127/13/07_CONSUMER/G17/`、`.../W1_MIN_CONSUME/`
- T3 核銷：`runs/w0_close_20261127/agents/t3/T3_VERIFICATION.md`