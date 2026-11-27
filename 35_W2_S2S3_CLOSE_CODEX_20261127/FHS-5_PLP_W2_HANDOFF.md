# FHS-5_PLP W2 HANDOFF（第 35_ 輪）

- pack：`S1_PACKS/FHS-5_PLP_W2_NATIVE_FIRST`（`911d06c9…`）
- candidate：16 成員 `b845efa6…`｜五 pin：`FIVE_PINS.json`
- oracle：12 assets/oracles｜case-set：12 案／18 子組／9 DAG
- evidence：`EVIDENCE_MANIFEST.json`＋`EVIDENCE_SEAL.json`（11 檔）
- checker：`CHECKER_FINAL.json`（PASS，14 檢查）
- consumer：`W3_CONSUMER.json`（ACCEPT_PARTIAL）

## actual_readback
| 動作 | argv | exit | raw | 結果 |
|---|---|---|---|---|
| N04 | `python n04_host.py` | 0 | N04_LEDGER.json | PASS，runner RUN-DEV-01 |
| N04 NEG | 同上（缺 oracle） | 2 | N04_LEDGER.negative | ORACLE_MISSING |
| W2 CLI | `w2_nf_reader.py --pack …` | 0 | W2_CLI_V5.json | ok |
| checker | `del35.py` | 0 | CHECKER_FINAL.json | PASS |
| W3 | 同上 | 0 | W3_CONSUMER.json | ACCEPT_PARTIAL |

## runtime
`runtime/n04_host.py`、`serve.py`、`consume.py`

## next_legal_action
`N09-OPERATION-UNDER-CONTRACT`

## readiness
W2 PARTIAL｜W3 technical PARTIAL｜W3 execution NOT_CLAIMED
