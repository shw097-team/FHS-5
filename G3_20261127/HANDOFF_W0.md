# W0 HANDOFF（W0 → W1）

- **verdict**：`W0_DONE`（scoped：local CODEX／Windows、Generic B0-NF、44/44；非 W1–W4、非整體 MVP、非 release）
- **branch**：`codex/w0-w2-g3-native-20261127`
- **content commit**：`f173214428f1d3b4ea3819182ddb8a6a67cc34f1`
- **docs/evidence commit**：`dda7779464abf3b6d7cbaeee8a9fbcc93c471137`
- **pack_manifest_sha256**：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- **w0m_amendment_sha256**：`c9b1ca9bbcd5ce87fdbcb0fc373cb8c36d1ad8d404b55c4f7311fc6c2bbddfd5`
- **candidate_commit**：`bb66a276aae8c5d6aef549832c523587fc47d247`
- **candidate_preimage**：`5eab43de2d3f67d6afbb1c5f6bc390e2c391da36`
- **oracle_sha256**：`112f2902656f1122720ef275ac954e3422f896267f144f27d321fa138be382c6`
- **evidence_manifest_sha256**：`5307b70ce521e90fcbea79cbccf5cc2bfad3228f59a2a5fce1aa6228cbf8e7da`
- **handoff_sha256**：`9f9ae2340212ec5b3171dcf26a9fa85db34aa2da79452bc0d86a389685d17613`
- **run root**：`C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\g3-20261127\G3_20261127\runs\w0_close_20261127\13`
- **final consumer**：`20261127T230849-a4b187dd`，811 checks，`consumed=true`，receipt sha256 `2be63f0da8e97961c067920664aa3df217bd366654bcb16ef280ed824ef327b8`
- **NF-T10 finalize**：`20261127T225645-015592e8`（810 checks，pre-final staging）
- **G17**：POS／單 byte NEG／zero-read audit 全 PASS（`07_CONSUMER/G17/`）
- **fresh W1 minimal**：44 items、readback_ok；`07_CONSUMER/W1_MIN_CONSUME/w1_out_pos/w1_checklist.json`（sha256 `49bd3a83…`）
- **independent checker**：`03_PARTIES/challenge/challenge.json` PASS 32 checks／0 findings

## next minimal W1 action

1. 讀 `09_DELIVERY/W0_HANDOFF.md` 與 `07_CONSUMER/W1_MIN_CONSUME/w1_out_pos/w1_checklist.json`（44 items）。
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

## push

本 HANDOFF 已在本地 commit（content `f1732144…`、docs/evidence `dda7779…`）。push 嘗試回 `unable to get password from user`，remote HEAD 回讀仍為 `0099e953…`；本輪為本地合規交付，未繞過憑證。不 force／merge main／改 `W2_CURRENT`。