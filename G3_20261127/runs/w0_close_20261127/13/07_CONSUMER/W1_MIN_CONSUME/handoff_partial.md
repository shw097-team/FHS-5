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
- **evidence_manifest_sha256**：`0ebbccf1f09837629b3cb2960dd476c440937f77cc80d4e8ee3d8fdcd3a92527`
- **consumer_manifest_sha256**：SEE `07_CONSUMER/CONSUMER_MANIFEST.sha256`
- **case_set**：SAMPLE 10＋`F5-W0-T01..24`＋`NF-T01..10` = 44
- **target_consumer**：W1 / CODEX Native（`tools/consumer.py`，`W1-consumer/CODEX-Native-1`）
- **consumer_version**：`@3`

## actual_readback

| 欄 | 值 |
|---|---|
| argv | `python tools/consumer.py --root . --allow-pending-t10`（staging）→ `python tools/consumer.py --root . --publish-manifest`（final） |
| exit | staging `0`；final `0`（以 `07_CONSUMER/LATEST.json` 與 `CONSUMER_MANIFEST.json` 為準） |
| raw | `07_CONSUMER/runs/<run_id>/raw/pos.*`、`neg.*`；`07_CONSUMER/neg_raw/consumer_positive.*` |
| action | 核 identity／pack／seal／W0M／candidate／oracle／handoff／evidence **754 檔**索引與路徑，再重跑 POS/NEG |
| result | staging 810 checks、`consumed=true`（T10 pending）；final 44/44、`consumed=true`；10 負例 fail-closed 且 `cli_executed=false`；G17 在 `07_CONSUMER/G17/` |
| t10 | `NF-T10` 由 `20261127T225645-015592e8` finalize；final consumer run 見 `07_CONSUMER/LATEST.json` |
| affected | `NF-T01`／`NF-T07`／`NF-T08`／`NF-T10` 受影重跑；`NF-T01` 含 CPython audit loader/open/child/os.system/loopback/ctypes 觀測；其餘 40 案同位復用 |
## next_legal_action

W1 以本 pins 為基線 requalify 14 HOLD／R3-CR，先做來源與 W1M 差額，不重跑 W0；W1 產品施工另需上位採納與 W1M／下一包一致。

## dependencies

- W1M／W1 下一包與本 W0 pins 一致。
- W1 必要入口、能力與授權（未具時 `W1_EXECUTION_READY=NOT_CLAIMED`）。
- Bridge 38＋28、C16 等完整分母另案。

## resume_predicate

W1M 受影條款正式採納；或真實 W0 pin／candidate／oracle 變更需 requalify；或 Owner 提供 W1 入口／授權。

## readiness

| 層 | 值 | 理由 |
|---|---|---|
| `w1_technical_readiness` | `W1_TECHNICALLY_READY` | W0 44/44（40 同位復用＋4 受影重跑；NF-T01 audit observation）＋真 handoff＋staging/final consumer 真讀回 |
| `w1_execution_readiness` | `NOT_CLAIMED` | 尚缺上位採納、W1M／下一包一致與 W1 真入口／授權 |

fresh W1 minimal consume：見 `07_CONSUMER/W1_MIN_CONSUME/`（44 items、parse/use/readback；wrong pin/scope/partial 真拒）；不代表 W1 產品執行或 W1 完成。
## publication_state

本輪先本地 commit 並回讀；如既有合法 GitHub 推送授權有效，僅推 `codex/w0-w2-g3-native-20261127` 施工分支並回讀 commit，不 force、不 merge main、不改 `W2_CURRENT`。實際狀態以 `PUBLICATION_STATUS.md` 與 `G3_CURRENT.json` 為準。
## stop／resume

- 錯 pack SHA／candidate／oracle：拒收，記 `PIN_MISMATCH`，不重跑。
- 同 Finding 無新 raw：`NO_DELTA_REWRITE_DENIED`。
- 權限／越界／不可逆：停受影操作，回 Owner。


