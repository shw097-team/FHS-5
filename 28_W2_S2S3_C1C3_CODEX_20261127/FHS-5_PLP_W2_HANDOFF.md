# FHS-5_PLP W2 HANDOFF（C1–C3 本輪）

- pack：`FHS5-PLP/W2/PACK-S1-20261126-r2`（manifest `911d06c9…`）
- candidate：`W2-S2S3-20261126T225929` ＋ 本輪 authority 化 admission/gate
- oracle：`EVIDENCE/OPS/OPS_ORACLE_FROZEN.json`（前置凍結）
- case-set：OPS-O01..O06、J1 clean receive
- evidence：`EVIDENCE/OPS/*`（raw＋SHA）
- checker：`CHECKER_VERDICT.json`（PASS，separate process）
- consumer：`CONSUMER_READBACK.json`（ACCEPT，fresh process）

## actual_readback
| 動作 | argv（摘要） | exit | raw | 結果 |
|---|---|---|---|---|
| O03 receive | `python ops_receive.py <wt> <delivery> <target> <receipt> <admission>` | 0 | O03_EFFECT.json | accepted=true, 118 entries, 6 files |
| O04 readback | `python ops_reader.py <target> <receipt>` | 0 | O04_READBACK.json | VERIFIED |
| O05 compensate | `python ops_compensate.py <target> <inventory>` | 0 | O05_COMPENSATION.json | target_absent=true |
| O06 timeout | 同上，timeout=0.9s | killed | O06_PARTIAL.json | TO_AFTER → compensated |
| checker | `python ops_checker.py <evidence>` | 0 | CHECKER_VERDICT.json | PASS |
| consumer | `python ops_consumer.py <evidence>` | 0 | CONSUMER_READBACK.json | ACCEPT |

## dependencies
Python 3.11.9、Git 2.53.0、pytest 9.1.1；全程在 R 內；無網路部署。

## next_legal_action
1. `C2-J3-ONOFF`：同任務 ON/OFF 與 leak 正控
2. `C2-J2-NINEKEYS`：兩期九鍵與 ChangeSet verifier
3. 12 案其餘與 N 系列核銷

## readiness
- W2 technical：PARTIAL（OPS-A 成立；12 案/J2/J3 未成立）
- W2 execution：NOT_CLAIMED
- W3 technical：NOT_ASSESSED

## publication
見 28_/PUBLICATION 與 remote tip 讀回；未 force push、未 merge main、未發 Release。
