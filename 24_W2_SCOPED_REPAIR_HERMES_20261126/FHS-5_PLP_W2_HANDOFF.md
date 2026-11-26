# FHS-5_PLP_W2_HANDOFF — r4 Producer 材料（供 W3 P01）

**from**：`HERMES-F5-W2-SCOPED-REPAIR-r4`　**基線 commit**：`660da33`

## 可接收範圍

| 材料 | 位置 | 狀態 |
|---|---|---|
| Candidate（受驗產品集合） | `W2_FIVE_PINS.json` candidate 段（5 檔 sha） | 已凍結 |
| Source／Oracle／CaseSet／Evidence pin | 同檔，沿用 r3 | 未受影 |
| S1 反證 | `S1_VERIFICATION.json`（7 列，含世界狀態） | 完成 |
| S2 E2E／ON-OFF | `S2_E2E.json`（23/23） | 完成 |
| J1 Checker | r3 `23_.../receipts/checker_j1_oracle.json`（21/21） | 受影未變，沿用 |

## 待 W3 驗證項（本輪不宣）

- W3 真 Consumer 的 typed parse/use/readback
- EvidenceGraph `W2.Effect` 節點與 Challenge evidence_refs
- `policy_epoch` 仍未宣告

## 不宣

`W2_NF_VALIDATED`、`W3_TECHNICALLY_READY`、`W3_EXECUTION_READY`、`INDEPENDENT_PASS`、`RELEASED`、`M-DONE`。


## r4b→FINAL-DELTA 增補

| 項 | 值 |
|---|---|
| S1 v2 | 13 PASS / 0 FAIL / 1 RESIDUAL_LIMIT（`sys.modules` 僞造，已揭露不宣稱已修） |
| S1 delta | 6 PASS / 0 FAIL（target-set 綁定、ADD parent probe、元件級 confinement、finding 事件撤權、控制） |
| S2 | 23/23（未受本輪影響） |
| Candidate | 5 檔 re-frozen，aggregate `8b4b4068313ae4d3ab066d6951add31d225d360ac053771d7d611621101ed8d7` |
| Oracle / CaseSet | **未重新凍結**，具名交 W3 P01 接續，不得當作已凍結 digest |
| Writer | `BLOCKED_NOT_ADMITTED` — 決策條款「出現安全 Finding 為止」已實際生效 |

W3 P01 待接續：12 原案 oracle/case-set 重新凍結、Evidence 封存、W3 Consumer typed 接收。
