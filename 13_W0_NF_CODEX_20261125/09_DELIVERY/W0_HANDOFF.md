# FHS-5_PLP/W0｜HANDOFF（W0 → W1）

- **handoff_id**：`W0-NF-HANDOFF-20261125-03`
- **from_stage**：`W0 / B0-NF`
- **to_stage**：`W1`
- **project/work_id**：`FHS-5_PLP/W0`｜batch `FHS-5/W0/B0-NF`
- **pack_ref**：`W0-NF-r3-CODEX-PRIMARY`（`FHS5-PLP/W0/PACK-NF-20261125-03`）
- **pack_manifest_sha256**：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- **w0m_amendment_sha256**：`c9b1ca9bbcd5ce87fdbcb0fc373cb8c36d1ad8d404b55c4f7311fc6c2bbddfd5`
- **candidate_ref**：`W0-NF briefcheck v3`
- **candidate_commit**：`bb66a276aae8c5d6aef549832c523587fc47d247`
- **candidate_preimage**：`5eab43de2d3f67d6afbb1c5f6bc390e2c391da36`
- **oracle_sha256**：`112f2902656f1122720ef275ac954e3422f896267f144f27d321fa138be382c6`
- **evidence_ref**：`10_EVIDENCE/EVIDENCE_MANIFEST.json`
- **evidence_manifest_sha256**：`68ee498768ed5195565bae5a397fff25e98b9ad1462fd4c3d666ed89b2e97f1c`
- **consumer_manifest_sha256**：SEE `07_CONSUMER/CONSUMER_MANIFEST.sha256`
- **case_set**：SAMPLE 10＋`F5-W0-T01..24`＋`NF-T01..10` = 44
- **target_consumer**：W1 / CODEX Native（`tools/consumer.py`，`W1-consumer/CODEX-Native-1`）
- **consumer_version**：`@3`

## actual_readback

| 欄 | 值 |
|---|---|
| argv | `python tools/consumer.py --handoff 09_DELIVERY/W0_HANDOFF.md --evidence-manifest 10_EVIDENCE/EVIDENCE_MANIFEST.json --publish-manifest` |
| exit | `0`；最新 `run_id`／receipt 以 `07_CONSUMER/LATEST.json` 為準 |
| raw | `07_CONSUMER/runs/<run_id>/raw/pos.*`、`neg.*` |
| action | 先核 identity／pack／seal／W0M／candidate／oracle／handoff／evidence 667 檔索引與路徑，再重跑 POS/NEG |
| result | `consumed=true`；實際 checks／negatives 以 `07_CONSUMER/LATEST.json` 與 `negatives.json` 為準；錯 pin／raw／schema／路徑負例全部 fail-closed 且 `cli_executed=false` |

## next_legal_action

W1 以本 pins 為基線 requalify 14 HOLD／R3-CR，先做來源與 W1M 差額，不重跑 W0；W1 產品施工另需上位採納與 W1M／下一包一致。

## dependencies

- W1M／W1 下一包與本 W0 pins 一致。
- W1 必要入口、能力與授權（未具時 `W1_EXECUTION_READY=NOT_CLAIMED`）。
- Bridge 38＋28、C16 等完整分母另案。

## resume_predicate

W1M 受影條款正式採納；或真實 W0 pin／candidate／oracle 變更需 requalify；或 Owner 提供 W1 入口／授權。

## not_covered

W1–W4 全分母、FHS 485、HERMES／GPT Host、不同 principal 簽章、Publisher/Release。

## readiness

| 層 | 值 | 理由 |
|---|---|---|
| `w1_technical_readiness` | `W1_TECHNICALLY_READY` | W0 validated（44/44）＋真 handoff＋clean-receive consumer 真讀回（見 Consumer Manifest 推導） |
| `w1_execution_readiness` | `NOT_CLAIMED` | 尚缺上位採納、W1M／下一包一致與 W1 真入口／授權 |

## publication_state

本輪 `15b063e..e49b7b5` 已 fast-forward 推送；後續 docs/archive commit 以同一流程補推。
詳見 `PUBLICATION_STATUS.md`。

## stop／resume

- 錯 pack SHA／candidate／oracle：拒收，記 `PIN_MISMATCH`，不重跑。
- 同 Finding 無新 raw：`NO_DELTA_REWRITE_DENIED`。
- 權限／越界／不可逆：停受影操作，回 Owner。


