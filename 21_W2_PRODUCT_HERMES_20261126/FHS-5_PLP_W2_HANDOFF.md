# FHS-5_PLP_W2_HANDOFF

**from**：`HERMES-F5-W2-PRODUCT-r1`（W2-NF-01 施工輪）
**to**：W3 接收／W2 續行
**run root**：`C:\Projects\Agent_Workspace\FHS-5_Workspace\W2_NATIVE_RUNS\20261126T1121_W2_PRODUCT`

## 1｜交給 W3 的 typed 欄（已凍結，可直接 parse）

| producer field | 值 | 位置 |
|---|---|---|
| `WorldEffectLedger.effect_receipt` | `OPS-O03` 的 receiver receipt（accepted=true、44 checks、sha 見 ledger） | `50_EVIDENCE/ops/OPS_O03_WORLD_EFFECT_POS.json` |
| `pre/post.world_sha256` | `49c62def…`（空）→ `5d6c7006…` | 同上 `pre_world`／`post_world` |
| `recovery.kind/ref` | `HOST_SPECIFIC_DELETE_CREATED_ONLY`，4/4 讀回 pre-state | `50_EVIDENCE/ops/OPS_O05_COMPENSATION_POS.json` |
| `UNKNOWN` | 無（本輪無 unknown-world 事件）；負例 `SCOPE_MISMATCH` 另列 | `50_EVIDENCE/ops/NEG_scope_mismatch_receipt.json` |
| `admission.receipt_ref` | `W2-NF-PRIMARY-20261126-01`（只作證據，不是 W3 Grant） | `10_PACK/19_W2_NF_CODEX_20261126/W2_OWNER_DECISION.json` |
| DEV candidate | `W1/check/w2_receiver.py` `ee92c8c8…`；`test_j1_receiver.py` `0dab8ebf…` | worktree／branch |
| 外置 pins | `30_VERIFY/expected_pins.json` | 同 run root |

**W3 不可拿去當 Grant 的東西**：上述 admission ref、本輪的 `W2_EXECUTION_READY`、任何 `OPS-O03` 收據。W3 需要自己的當期主用包與 Owner 決策。

## 2｜W3 接收的最小合法下一步

1. 以 `W2M §12.3.1` 產 clean receive：新根、五 pin（source/candidate/evidence/oracle/case-set）＋fixture/runner。
2. 先補本輪缺的三件：J3 OFF parity、J2-post ChangeSet、W2-DEV-02。
3. 錯 pin／跨 epoch／缺 raw／假 Grant 一律早拒。

## 3｜要 Owner 裁決的一件（會影響發布）

本輪工程寫入全部落在 R（`FHS-5_Workspace`），未觸碰 SQS 或其他 repo。Git 發布目標分支為 `hermes/w2-product-20261126`（自 `35d5387f` 接續，不 force、不 merge main）。若 Owner 不核准，本輪交付以本地 run root 為準，發布另案。

## 4｜工具實績（本輪實跑，非引用）

| 工具 | 版本 | 用途 |
|---|---|---|
| `codex`（CODEX Native） | `codex-cli 0.164.0`，ChatGPT 登入 | 產品 writer：D04 兩檔 patch＋測試 |
| `git` | 2.56.1.windows.1 | worktree／archive／diff／blob 重算 |
| `python` | 3.14.9（Hermes venv；codex 另用 3.12.13 自跑） | 測試、oracle、OPS |
| `openspec` | 2.0.0 | 在 worktree 內 `list` 可用（既有 change `w1-nf-r2-product`）；W2 change 未建 |
| `hermes` | v0.23.3 | 外層任務執行、Kanban/委派未用於本輪（見 §6） |

## 5｜Resume predicate

| 缺口 | predicate |
|---|---|
| J3 | 同 candidate 的隔離 ON/OFF roots 建好，且正控能偵測一次真 import/call |
| J2-post | 交付 commit 存在（本 handoff 之後） |
| W3 receive | W3 當期包或最小接收材料存在 |
| `policy_epoch` | Host 宣告 epoch；未宣告前一律 `NOT_DECLARED_BY_HOST` |

## 6｜明確未用／未做（不得被讀成已做）

- 未建立 Kanban board／Swarm／`delegate_task` 子代理：本輪以單一主 session＋CODEX writer 完成，屬外層協作方式的縮減，`NOT_OBSERVED`。
- 未建 OpenSpec W2 change（`openspec list` 只用於確認 worktree 內既有 change）。
- 未產 `W3_RECEIVE_RECEIPT`。
- 未執行任何 W3 protected effect。
