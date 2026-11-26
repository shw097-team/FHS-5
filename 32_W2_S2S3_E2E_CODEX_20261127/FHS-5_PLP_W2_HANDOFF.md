# FHS-5_PLP W2 HANDOFF（當期真產品貫穿）

- pack：`S1_PACKS/FHS-5_PLP_W2_NATIVE_FIRST`（`911d06c9…`, tree `cc7d91a1…`）
- candidate：`FIVE_PINS.json`（15 成員，canonical `a5097ce6…`）
- oracle：12 assets/oracles；`OPS_ORACLE_FROZEN.json`（28_）
- case-set：12 案／18 子組／N01–N12
- evidence：`EVIDENCE_MANIFEST.json`＋`EVIDENCE_SEAL.json`（12 檔）
- checker：`CHECKER_FINAL.json`（PASS，10 檢查）
- consumer：`W3_CONSUMER.json`（ACCEPT，7 檢查）

## actual_readback
| 動作 | argv | exit | raw | 結果 |
|---|---|---|---|---|
| W2 CLI | `w2_nf_reader.py --pack … --out …` | 0 | W2_CLI_V2.json | ok/problems empty |
| N01 TPM | `tpm.build_contracts(pack)` | 0 | N09_E2E.json | profile S1-W2, 5 views |
| N06 | `n06b.py` | 0 | N06_UNKNOWN.json | 4/4 |
| checker | `del32.py`（checker 段） | 0 | CHECKER_FINAL.json | PASS |
| W3 consumer | 同上 | 0 | W3_CONSUMER.json | ACCEPT |

## next_legal_action
1. `N04-CURRENT-HOST`：當期 W2 Host session（served/consumed）
2. `N09-SINGLE-SOURCE`：以 S1 W2 為 source 的 operation+receiver 段
3. `W1-67ECP`：逐義核銷

## readiness
W2 PARTIAL／W3 technical PARTIAL／W3 execution NOT_CLAIMED
