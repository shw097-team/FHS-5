# FHS-5_PLP W2 HANDOFF（真源契約對位）

- pack：`S1_PACKS/FHS-5_PLP_W2_NATIVE_FIRST`（`911d06c9…`，tree `cc7d91a1…`）
- candidate：`FIVE_PINS.json`（13 成員，canonical `ee90fc92…`）
- oracle：`OPS_ORACLE_FROZEN.json`（28_）、`W2_CASES.json`、`A_CROSSWALK.json`
- case-set：12 原案／J1-T01..08／J2-T01..07／N01–N12
- evidence：`EVIDENCE_MANIFEST.json` ＋ `EVIDENCE_SEAL.json`（12 檔）
- checker：`CHECKER_FINAL.json`（PASS，分立程序）
- consumer：`W3_CONSUMER.json`（ACCEPT，fresh；16 requirements／12 cases／6 views）

## actual_readback
| 動作 | argv | exit | raw | 結果 |
|---|---|---|---|---|
| W2 contracts | `w2_nf_reader.py --pack … --out …` | 0 | W2_CLI.json | ok=true, problems=[] |
| 7 案 | `w2_cases.py` | 0 | W2_CASES.json | 7/7 PASS |
| crosswalk | `cross.py` | 0 | A_CROSSWALK.json | 16/16 |
| checker | `final_check.py checker` | 0 | CHECKER_FINAL.json | PASS |
| W3 consumer | `final_check.py consumer` | 0 | W3_CONSUMER.json | ACCEPT |

## next_legal_action
`N04-HOST-SERVED`（真 Host session served/consumed）、`N06-UNKNOWN-MATRIX`、`N09-E2E-SLICE`

## readiness
W2 technical PARTIAL｜W2 execution NOT_CLAIMED｜W3 technical PARTIAL｜W3 execution NOT_CLAIMED
