# FHS-5_PLP_W2_CLOSEOUT — r4 局部增補

**任務**：`HERMES-F5-W2-SCOPED-REPAIR-r4`｜**基線**：`660da337ac4ed57bccd6db0789ea4d9238f5b46b`
**run root**：`W2_NATIVE_RUNS/20261126T1240_W2_SCOPED_REPAIR`｜**時間**：2026-11-26T13:01:41+0800

本輪只做 S1／S2，不重跑 M1～M3，不重編 NF-r3。

## S1｜真安全入口（7/7）

修掉 r3 的兩個真洞：

1. `require_verified_admission` **由 caller 選擇** → 整條旗標刪除。`w2_dev_gate.check()` 現在**無條件**呼叫 `w2_admission.require()`；READ/DRAFT 走另一個 `check_readonly()`（結構上不能寫）。
2. `verify_receipt()` 只自證 receipt 自身 fields digest → 改為**模組層 TRUST 常數**（decision sha `1ef19c0f…`）＋**使用時重讀磁碟決策文件**，並核 domain/scope/subject/effects/撤權 marker。caller 不能提供 pin、decision path 或關閉檢查。

驗收（每列都驗世界狀態，不只看 `check()` 回傳）：

| case | expected | 世界狀態 |
|---|---|---|
| R1 不可信 admission | `FALSE_AUTHORITY` | target/canary 未變 |
| R2 外來 pin 的 receipt | `FALSE_AUTHORITY` | 未變 |
| R3 READ／未知 effect 進 writer | `EFFECT_UNBOUND` | 未變 |
| R4 過期 preimage | `WRITE_SET_UNBOUND` | 未變 |
| R5 非法 recovery（git revert） | `RECOVERY_KIND_MISMATCH` | 未變 |
| R6 真受界正向 | 成功 | post 變、未列 target 不變、canary 不變、reverse 還原 |
| R7 J1 受影負例 | 拒收 | product call **0**、交付樹未變 |

**7/7 PASS**（檔：`S1_VERIFICATION.json`）

## S2｜一次正式 W2 E2E（23/23）

以正式 NF-r3 包的 parsed values 驅動 ECP（16 requirements、12 cases、37 CR、14+6 HOLD），不再用舊 `W2_DRAFT`：

- ON：`w2_nf_reader.build_contracts` ＋ `guide_nf`（imported 非空）
- OFF：純 json 直接解析，import blocker 正控回 `BLOCKED`，imported 為空
- 兩側各自產出 typed receipt（effect）→ 讀回 → delete-created-only → 讀回 pre-state
- 比較 **15 個 typed 鍵**（subject/scope/pack sha/requirements/cases/crs/holds/source_set/permission_state/ecp_is_grant/effect/readback/recovery），非只比 exit 或 boolean

`ECP is not a grant`、`permission_state=NONE_GRANTED` 兩側皆成立。

## 狀態分帳

| 判定 | 值 |
|---|---|
| S1 | 成立（7/7，分立 Verifier 覆核進行中） |
| S2 | 成立（23/23） |
| `W2_NF_VALIDATED` | **保留 NOT_CLAIMED** — 本輪未重跑 12 原案與 J3，只修受影入口與 E2E；不以前輪結果自動升格 |
| `W3_TECHNICALLY_READY` | **NOT_CLAIMED** — 待 W3 真 Consumer 接收 |
| `W3_EXECUTION_READY`／`INDEPENDENT_PASS`／`RELEASED` | `NOT_CLAIMED` |

## 具名限制

- Kanban／Swarm 仍未使用（本輪首次真用 `delegate_task` 派 Verifier）
- OpenSpec change 未建
- `policy_epoch` `NOT_DECLARED_BY_HOST`
- 14 HOLD＋6 專項、37 CR 全 RETAINED
