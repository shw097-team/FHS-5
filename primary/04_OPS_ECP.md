<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 04_OPS_ECP

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

Input: HostID、OS Principal、PolicyEpoch、Original Receiver ABI、OperationType/WorkOrder/Admission、Host preimage。
Operation: 只設計並條件式描述 W0-B 的第一個最小可逆 OPS Effect；本輪不產生 Host Effect。
Output: 可交接的 Host pre/post、WorldReader、Original Receiver readback 與 Host-specific recovery。
Consumer: Original Host Owner、OS Principal、Issuer、Executor、Checker。
NEG: 假 Host/OS Principal、無 Admission、或以 generic git revert 作 OPS recovery。
FirstFail: W0-B_NOT_ADMITTED / OPS_ECP_UNBOUND / RECOVERY_KIND_MISMATCH / WORLD_READER_UNBOUND。

Applicability: W0-B OPS design only. 本輪狀態 `NOT_ADMITTED`；沒有原 Host/OS Principal/Issuer/Receiver ABI 時不產生任何 Host Effect。

Preconditions: HostID 與環境 identity；OS Principal 與 UAC/SID；PolicyEpoch；Original Receiver ABI 與 OperationType；WorkOrder/ExecutionAdmission；Host preimage；同 Host/Epoch 的 WorldReader；Host-specific recovery 能力。

Postconditions: 只出現 Admission 允許的 Host post；Original Receiver 可讀回；WorldRaw 與原 Oracle/Expected 可比；recovery/compensation 可執行；不留第二 Queue/Issuer/Checker。

Permission: 原 Host Owner、OS Principal 與 Original Issuer。DEV Repo Principal 不可互換成 OPS Principal；作者檔案、skill 可讀性或本地腳本都不是 Host Grant。

Readback: 以同 Host/Epoch 的 Original WorldReader 讀回 Host post、receiver receipt 與 WorldRaw；CLI exit 0 但 WorldRaw 不符仍不通過。UNKNOWN 先 reconcile，不盲重試。

Recovery: 使用 Host 專屬 recovery/compensation；不得以 generic `git revert` 代替。若原 Receiver 沒有 recovery ABI，記 `RECOVERY_KIND_MISMATCH` 並停。

## 第一個最小可逆 OPS Effect 的條件式 Runbook

| 步驟 | 必要輸入 | 操作 | 輸出／Readback | NEG | FirstFail |
|---|---|---|---|---|---|
| O1 | Original OperationType | 解析 effect | `OperationType` | 未知 token | `EFFECT_MAPPING_UNVERIFIED` |
| O2 | HostID、OS Principal、PolicyEpoch | 核對環境 identity | HostContext | 假 Host 或錯 Principal | `HOST_PRINCIPAL_MISMATCH` |
| O3 | Host preimage、Receiver ABI | 凍結 preimage 與 ABI | preimage SHA + ABI ref | ABI 不明 | `RECEIVER_ABI_UNBOUND` |
| O4 | Issuer/WorkOrder/Admission | 驗 typed receipt | Admission ref | 假 permit/WorkOrder | `W0-B_NOT_ADMITTED` |
| O5 | O1–O4 | 只做第一個最小可逆 Host 操作 | command/exit/stdout/stderr digest + receiver receipt | 同批多改 | `NOT_ADMITTED` |
| O6 | Original WorldReader | 讀回 Host post/WorldRaw | WorldRaw SHA | 只看 CLI exit 0 | `EFFECT_NOT_VERIFIED` |
| O7 | Host-specific recovery | 失敗時恢復 | Recovery raw + LastGood | git revert 作 OPS recovery | `RECOVERY_KIND_MISMATCH` |
| O8 | Frozen Candidate + Raw | 交原 Checker/Consumer | Original assurance ref 或 NOT_RUN | Maker 自簽 | `INDEPENDENT_NOT_CLAIMED` |

## NEG / FirstFail

| NEG | 預期 FirstFail |
|---|---|
| 假 HostID／OS Principal | `HOST_PRINCIPAL_MISMATCH` |
| 無 WorkOrder/Admission | `W0-B_NOT_ADMITTED` |
| Receiver ABI 或 OperationType 不明 | `RECEIVER_ABI_UNBOUND`／`EFFECT_MAPPING_UNVERIFIED` |
| `git revert` 當 OPS recovery | `RECOVERY_KIND_MISMATCH` |
| CLI exit 0 但 WorldRaw 不符 | `EFFECT_NOT_VERIFIED` |
| UNKNOWN 直接 retry | `UNKNOWN_RETRY_DENIED` |

## Idempotency / Retry / UNKNOWN

Idempotency key 必須含 `HostID + Original OperationType + PolicyEpoch + WorkOrder/Admission + preimage SHA`。Retry 只允許可證的暫時性失敗，且先做 WorldReader reconcile；`UNKNOWN` 不盲重試。作者端不建立第二 Issuer/Queue/Checker。

## Stop / Resume

Stop：缺 HostID/OS Principal/PolicyEpoch、Receiver ABI、WorkOrder/Admission、preimage 或 WorldReader。Resume：Original Host Owner/OS Principal/Issuer 提供同 Host/Subject/Scope/PolicyEpoch 的 typed receipt、preimage、ABI 與 WorldRaw 能力。

## 不授權聲明

本檔是 OPS ECP 的設計與施工條件，不是 Canonical ECP、不是 Grant、不是 Host Effect 授權。W0-B `NOT_ADMITTED` 是本輪的正確狀態。
