<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 03_DEV_ECP

## 身份與效力

| 欄 | 值 |
|---|---|
| project_id | `FHS-5_PLP` |
| subject_id | `FHS-5_PLP/W0` |
| scope | `W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED` |
| wave_id | `W0` |
| batch_id | `W0-CODEX-REPAIR-20261123-01` |
| source_manifest_sha256 | `22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f` |
| claim_ceiling | `AUTHOR_DESIGN_ONLY` |
| author_label | `AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS` |
| review_mode | `AUTHOR_REVIEW_ONLY` |

## 契約摘要

Input: 原 OperationType、RepoContext、exact WriteSet、Original DEV ECP/TQAEP、Issuer/WorkOrder/Admission。
Operation: 只設計並條件式描述 W0-B 的第一個最小可逆 DEV Effect；本輪不寫 Repo。
Output: 可交接的 DEV pre/post、diff/test、readback、rollback 與 UNKNOWN reconcile 條件。
Consumer: Original Repo Owner、Issuer、Executor、Case Owner。
NEG: caller 自報 HEAD、假 permit、無 WriteSet、或把 ECP 意圖當 Grant。
FirstFail: W0-B_NOT_ADMITTED / DEV_ECP_UNBOUND / REPO_HEAD_MISMATCH / WRITESET_UNBOUND。

Applicability: W0-B DEV design only. 本輪狀態 `NOT_ADMITTED`；沒有原 Repo/Issuer/WorkOrder/Admission 時不產生任何 Repo Write。

Preconditions: 已綁定的 Original OperationType；Repo Root/HEAD/branch/dirty/untracked；ACL 與可讀 preimage；原 DEV ECP 的 exact WriteSet 與 test list；Original TQAEP Case；Issuer/WorkOrder/ExecutionAdmission；同 Subject/Scope/Host/PolicyEpoch 的 Readback 能力。

Postconditions: 只出現 Admission 允許的 postimage；diff 與原 ECP 預期一致；受影 tests 有 command/exit/raw；Repo/WorldReader 可讀回；rollback 或補償可執行。

Permission: 原 Repo Owner 與 Original Issuer。作者文件與本 ECP 設計不是 Grant；`permit=true`、複製的 WorkOrder 字串或本地腳本都不能替代 typed receipt。

Readback: 以 Original Repo Reader 讀回 HEAD、postimage、diff、test raw；同一 Subject/Scope/Host/Epoch 才可比較。CLI exit 0 但 Repo/WorldRaw 不符，仍是 `EFFECT_NOT_VERIFIED`。

Recovery: DEV 使用原 ECP 指定的 rollback commit 或反向 patch；保留 LastGood 與 before SHA。`git revert` 只可在 DEV 且原 ECP 明確指定時使用，不可拿來代替 OPS Host recovery。

## 第一個最小可逆 Effect 的條件式 Runbook

| 步驟 | 必要輸入 | 操作 | 輸出／Readback | NEG | FirstFail |
|---|---|---|---|---|---|
| D1 | Original OperationType | 解析 effect，不用拼字猜 | `OperationType` | 未知 alias | `EFFECT_MAPPING_UNVERIFIED` |
| D2 | Repo Root/HEAD/branch/dirty/untracked | 只讀核對 | RepoContext | caller HEAD | `REPO_HEAD_MISMATCH` |
| D3 | exact WriteSet、preimage、ACL | 凍結寫入集合 | WriteSet + preimage SHA | 多檔或無 preimage | `WRITESET_UNBOUND` |
| D4 | Issuer/WorkOrder/Admission | 驗 typed receipt | Admission ref | 假 permit/WorkOrder | `W0-B_NOT_ADMITTED` |
| D5 | D1–D4 | 只做第一個最小可逆操作 | command/exit/stdout/stderr digest + effect receipt | 同批多改 | `NOT_ADMITTED` |
| D6 | postimage、test list、Reader | 讀回 diff/test/RepoRaw | Postimage + test raw SHA | 只看 exit 0 | `EFFECT_NOT_VERIFIED` |
| D7 | 原 rollback commit／反向 patch | 失敗時恢復 | LastGood + recovery raw | 無 recovery 或錯 kind | `RECOVERY_KIND_MISMATCH` |
| D8 | Frozen Candidate + Raw | 交原 Checker | Original assurance ref 或 NOT_RUN | Maker 自簽 | `INDEPENDENT_NOT_CLAIMED` |

## Idempotency / Retry / UNKNOWN

Idempotency key 必須由 `task_id + Original OperationType + Repo HEAD + WriteSet SHA + Admission ref` 組成；同一 key 重放只能得到同一 postimage 或明確 no-op。Retry 只允許暫時 I/O 失敗，且先讀回再重試；`UNKNOWN` 先交 Original Repo/WorldReader reconcile，不得盲目重送 Effect。同一 Subject/Scope/SourceSHA/FirstFail 在沒有新證據時最多兩次修補，之後記 `HOLD/PARK` 與 Owner。

## NEG / FirstFail

| NEG | 預期 FirstFail |
|---|---|
| caller 自報 HEAD 或 branch | `REPO_HEAD_MISMATCH` |
| `permission=true` 或複製的 WorkOrder | `W0-B_NOT_ADMITTED` |
| 無 exact WriteSet 或 preimage | `WRITESET_UNBOUND` |
| 同批修改超出 Admission | `NOT_ADMITTED` |
| CLI exit 0 但 diff/RepoRaw 不符 | `EFFECT_NOT_VERIFIED` |
| UNKNOWN 直接 retry | `UNKNOWN_RETRY_DENIED` |

## Stop / Resume

Stop：缺 Original OperationType、Repo HEAD/preimage/ACL、WriteSet、Issuer/WorkOrder/Admission，或任何 path 逃逸。Resume：由 Original Repo Owner/Issuer 提供同 Subject/Scope/Host/PolicyEpoch 的 typed receipt、exact WriteSet、preimage 與 Readback 能力；本檔不自行解除 HOLD。

## 不授權聲明

本檔是 DEV ECP 的設計與施工條件，不是 Canonical ECP、不是 Grant、不是 Repo Write 授權。W0-B 的 `NOT_ADMITTED` 不阻止 W0-A/C 的作者文件交付。
