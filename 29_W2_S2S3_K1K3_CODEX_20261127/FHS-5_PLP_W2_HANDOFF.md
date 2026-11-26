# FHS-5_PLP W2 HANDOFF（K1–K3）

- pack：`FHS5-PLP/W2/PACK-S1-20261126-r2`（`911d06c9…`）＋ `S1_PACKS/` 實體
- candidate：`CANDIDATE_PINS.json`（11 成員，canonical `f06b1be8…`）
- oracle：`OPS_ORACLE_FROZEN.json`；J2 判例集 `J2_NINEKEYS.json`
- case-set：J1-T01..T08、J2-T01..T07、OPS-O01..O06、J3
- evidence：`EVIDENCE/`（19 檔）
- checker：`CHECKER_VERDICT.json`（PASS，分立程序）
- consumer：`CONSUMER_READBACK.json`（ACCEPT，fresh）

## actual_readback
| 動作 | argv | exit | raw | 結果 |
|---|---|---|---|---|
| S1 inspect | `pytest test_s1_schema.py` | 0 | TESTS_K1_FINAL | 5 案綠 |
| J2 | `j2_ninekeys.py` | 0 | J2_NINEKEYS.json | 7/7 |
| J3 | `run_off_task.py --material … --w2m W2M` | 0 | J3_ONOFF.json | both 13 |
| OPS | `ops_a.py`（O01–O06） | 0 | O0*.json | O03 accepted、O04 VERIFIED、O05 還原 |

## next_legal_action
1. `K2-N-SET`：N01–N12 成套
2. `K2-R3`：R3-01/02 原域隔離與 13+3 接線
3. `K2-OPS02`：pre-existing target 的 host restore

## readiness
W2 technical = PARTIAL｜W2 execution = NOT_CLAIMED｜W3 technical = NOT_ASSESSED
