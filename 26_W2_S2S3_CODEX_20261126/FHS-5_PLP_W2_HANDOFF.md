# FHS-5_PLP_W2_HANDOFF（S2/S3 本輪）

- pack: `FHS5-PLP/W2/PACK-S1-20261126-r2`（manifest `911d06c9…`）
- candidate: `W2-S2S3-20261126T225929`（六成員，雙 aggregate 見 `W2_CANDIDATE_S2S3.json`）
- oracle: `50_PROBES/probe_authority_injection.py`（凍結於修補前）
- case-set: J1-T01..T08、S1..S6、W1 全套 pytest
- evidence: `60_EVIDENCE/raw/{STAGE1,STAGE2,APPLY,REVERSE,PROBE_*}.json`
- checker: 獨立程序重開 raw 與 oracle（同 principal，非 INDEPENDENT_PASS）
- consumer: 未於本輪建立 fresh W3 typed consume

## actual_readback

| 動作 | argv | exit | raw | 結果 |
|---|---|---|---|---|
| pre-patch probe | `probe_authority_injection.py <world> <run>\_t` | 3 | `PROBE_PRE_PATCH.json` | RED_ACCEPTED（真缺陷） |
| gate apply | `dev_gate.apply_patch` | 0 | `APPLY.json` | wrote 2 檔，post sha 已變 |
| tests | `pytest test_j1_receiver.py test_j1_strict.py` | 0 | `TESTS_POST_PATCH.stdout.txt` | 15 passed |
| post probe | 同上 | 0 | `PROBE_POST_PATCH.json` | GREEN |
| reverse | `dev_gate.reverse` | 0 | `REVERSE.json` | restored == preimage |
| world restore | `git apply -R` | 0 | `STAGE2.json` | world digest 相同 |
| full suite | `pytest` in `W1/check` | 1 | `TESTS_FULL_CANDIDATE.stdout.txt` | 19 failed, 50 passed, 25 errors, 15 subtests passed in 11.30s |

## dependencies

Python 3.11.9、pytest 9.1.1、Git 2.53。temp 全部在 run 內；未使用網路。

## next_legal_action

1. 以同一候選跑 W2-OPS-A（`verify_delivery → consume_verified → receive`）與 OPS ECP。
2. 依 03 §1–3 凍結 12 原案／N01–N12 oracle 後逐案真跑（J1/J2/J3）。
3. 另取 OPS host effect 的具名 scope（本決策只涵蓋 DEV-A 二檔）。

## owner / resume

- owner: 本 thread user（單一 issuer）
- resume: 同 candidate pins + 同 oracle bytes；不得以舊 summary 代替 raw

## readiness

- W2 technical: **PARTIAL**（DEV-A 與安全矩陣成立；OPS/12 案未成立）
- W2 execution: **NOT_CLAIMED**
- W3 technical: **NOT_ASSESSED**

## publication

本輪 commit 與遠端讀回見 `PUBLICATION_S2S3.json`；未 force push、未 merge main、未發 Release。

## W1 補記

- 13 案 runner：17 PASS／1 DEFERRED／1 NOT_RUN（ACC-05）／1 NOT_OBSERVED；raw 在 EVIDENCE/raw/W1_CASES/cases.json。
- 全套 pytest 基線＝修補後除新增 2 案外完全相同（19F/25E），根因為測試預設歷史絕對 pack 路徑；next_legal_action 增加：把 W1 測試預設 pack root 改為 repo 相對或 env，另立 W1 修補 scope。
