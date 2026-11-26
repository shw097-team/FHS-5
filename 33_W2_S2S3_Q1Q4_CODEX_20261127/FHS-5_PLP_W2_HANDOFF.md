# FHS-5_PLP W2 HANDOFF（Q1–Q4）

- pack：`S1_PACKS/FHS-5_PLP_W2_NATIVE_FIRST`（`911d06c9…`, tree `cc7d91a1…`）
- candidate：16 成員，canonical `cb66d77bc8e1282cd18c1d8ebaa55f49ee1059dba55bc1cd33f0d097671a6794`
- oracle：12 `assets/oracles`；`OPS_ORACLE_FROZEN.json`
- case-set：12 案／18 子組／9 DAG edges／14 HOLD／37 CR
- evidence：`EVIDENCE_MANIFEST.json`＋`EVIDENCE_SEAL.json`
- checker：`CHECKER_FINAL.json`（PASS）
- consumer：`W3_CONSUMER.json`（ACCEPT_PARTIAL）

## actual_readback
| 動作 | argv | exit | raw | 結果 |
|---|---|---|---|---|
| W2 CLI | `w2_nf_reader.py --pack … --out …` | 0 | W2_CLI_V4.json | ok, problems=[] |
| Q1 測試 | `pytest test_s1_contracts.py` | 0 | 4 passed | DAG/runner/dup/case |
| 全套 | `pytest W1/check` | 0 | TESTS_Q1.stdout.txt | 115 passed |
| N06 | `n06b.py` | 0 | N06_UNKNOWN.json | 4/4 |
| checker | `del33.py` | 0 | CHECKER_FINAL.json | PASS |
| W3 | 同上 | 0 | W3_CONSUMER.json | ACCEPT_PARTIAL |

## next_legal_action
`N04-CURRENT-HOST`、`N09-SINGLE-SOURCE`、`W0-OFF-RERUN`、`W1-67ECP`

## readiness
W2 PARTIAL｜W3 technical PARTIAL｜W3 execution NOT_CLAIMED
