<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 01_SOURCE_SCOPE_AND_CONSTRUCTION

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

Input: the selected W0 sources, the M §12.7 case table and the W0M §07/§09/§11 hand-off facts.
Operation: turn Scope/FUO/Effect/ABI/Case/Oracle/Owner into an executable author construction sequence with explicit stop points.
Output: the W0-A eight-step route, W0-B conditional runbook, W0-C applicability ledger, 14 WP and 7 Seam mapping.
Consumer: Guide, Bridge, Original Executor, PI Owner, Case Owner and Program Owner.
NEG: scope expansion, missing child requirement, W4-to-W0 phase overreach, or a gate cycle.
FirstFail: SCOPE_DRIFT / SPLIT_UNVERIFIED / PHASE_OVERREACH_CANDIDATE / GATE_CYCLE_CANDIDATE.

## W0-A 通用 READ/DRAFT 八步

| 步驟 | Input | Operation | Output | Consumer | NEG | FirstFail |
|---|---|---|---|---|---|---|
| A1 Source freeze | 至少一個真非 FHS PLP/Requirement/Case/Oracle 的 bytes、SHA、ACL、版本 | 以真 bytes 建立 SourceLedger；不以檔名或舊快取代替 | SourceLedger + source_manifest_sha256 | Reviewer/PI Owner | 找不到真非 FHS 案例 | `W0-A_CASE_SELECTION`（只停 A 的 E2E） |
| A2 PI/Reviewer | SourceLedger、Goal、Parent/Child/NEG 原句 | 逐子要求檢查 POS/NEG/Exception；混合極性只評有錨定的條款 | PI Review + FirstFail + Owner | Original PI Owner | 「A、B各有」只做 A | `SPLIT_UNVERIFIED`／`REQUIRED_CHILD_MISSING` |
| A3 Guide1 | 真 Scope、FUO、Effect、WaveControl 六身份 | 產生 ThinStart；只引用原 Scope | ThinStart prompt | Bridge/Executor | Guide 把 Scope A 擴成 Scope B | `SCOPE_DRIFT`／`CLARIFY` |
| A4 Bridge 四 API | Source span、SHA、Clause locator、非 Canonical Context | 四個唯讀 API 產生 Context；拒絕 `../`、symlink、UNC、絕對路徑逃逸 | Bridge Context + Body SHA/span | Executor | 路徑逃逸或未知欄位被靜默丟棄 | `PATH_OUTSIDE_ROOT`／`ABI_LOSSY_CROSSWALK` |
| A5 受權 READ/DRAFT | Bridge Context、來源 ACL、隔離輸出根 | 執行合法 READ/DRAFT；沒有 Host/Runner 時只回 `NOT_RUN` | Reader/Draft Raw 或 `NOT_RUN` | Challenge | 以 Mock 或文字總結冒充 ActualServed | `NOT_RUN`／`UNREPRODUCED` |
| A6 Frozen Candidate | Candidate、Oracle、Fixture、Evidence bytes | 凍結 identity、SHA、scope；保存 before SHA | Frozen Candidate | External Challenger | 換 Candidate 卻重用舊 Raw | `FROZEN_IDENTITY_MISMATCH` |
| A7 Challenge POS/NEG | Frozen Candidate、command/exit/raw | 在隔離複本刪必要子項、改 byte、換 Oracle、造 gate cycle | Finding + FirstFail + observed | FAR/Program | 只有文字、沒有 command/exit/raw | `UNREPRODUCED`／`NOT_PROVEN` |
| A8 FAR/Guide2 | Challenge findings、WorldReader 真 Delta | 產生 `RESEARCH_REQUIRED`／`WAIT`／`RESUME`／`PARK` 候選 | Resume candidate | Original Owner/Consumer | FAR 無 Raw 自報 CLOSE 或 Guide 自簽 Release | `RESEARCH_REQUIRED`／`CLOSE_NOT_AUTHORIZED` |

## W0-B 受保護 Native 的條件式 Runbook

| 步驟 | Input／前件 | Operation | Output／Readback | NEG | FirstFail |
|---|---|---|---|---|---|
| B1 Effect | 原 Effect Registry 的 typed OperationType | 解析 effect，不用相對／絕對／UNC 拼字決定 | `OperationType` | 未知 token 或 alias | `EFFECT_MAPPING_UNVERIFIED` |
| B2 Repo | Repo Root、HEAD、branch、dirty/untracked、ACL、preimage | 只讀核對，不寫 | RepoContext | caller 自報 HEAD | `REPO_HEAD_MISMATCH` |
| B3 WriteSet | 原 ECP 的 exact WriteSet、preimage、test list | 凍結將寫入的檔案與 diff 預期 | WriteSet + preimage SHA | 超出 WriteSet 或無 preimage | `WRITESET_UNBOUND` |
| B4 Admission | Original Issuer、WorkOrder、ExecutionAdmission、PolicyEpoch | 只驗 typed receipt，不接受 `permit=true` 字串 | Admission receipt ref | 缺 Issuer/WorkOrder/Admission | `W0-B_NOT_ADMITTED` |
| B5 First effect | B1–B4 全部成立 | 只執行 Admission 允許的第一個最小可逆操作 | command/exit/stdout/stderr digest + effect receipt | 一批多改或繞過 Admission | `NOT_ADMITTED` |
| B6 Post/Readback | 原 WorldReader/Repo Reader、同 Subject/Scope/Host/Epoch | 讀回 postimage 與 WorldRaw；CLI 0 但 Raw 不符仍不通過 | Postimage + WorldRaw SHA | 只信 CLI exit=0 | `EFFECT_NOT_VERIFIED` |
| B7 Recovery | 原 DEV rollback commit 或 OPS Host-specific recovery | 失敗時走原 ECP recovery；UNKNOWN 先 reconcile | Recovery raw + LastGood | 用 generic git revert 作 OPS recovery | `RECOVERY_KIND_MISMATCH` |
| B8 Assurance | Frozen Candidate、Raw、Checker 角色 | 交原 Checker/Consumer；本輪不自簽 | Original assurance ref 或 NOT_RUN | Maker 自簽 Independent | `INDEPENDENT_NOT_CLAIMED` |

## W0-C FHS Profile 回歸

FHS Profile-only 分母：`22 WP / 36 Edge / 50 H1 / 39 ModeGate / 96 Oracle / 192 Cell / 485 ToolNeed`，另有 `35 Reviewer Tool / 56 User Subintent`。本輪只建立可追的適用性帳，不宣 `485/485` Fit，也不要求安裝 485 套工具。每一原 ID 只能落 `Fit / NoFit / ReasonedNA / UNVERIFIED` 之一，並記 Owner 與來源 locator；Generic 非 FHS 路線不背 FHS-only Gate。

| 集合 | 分母 | 本輪狀態 | Owner |
|---|---:|---|---|
| W0 Core WP | 22 | `APPLICABILITY_PLANNED`；只做本波受影項 | Program/Tool Owner |
| Edge | 36 | `INDEX_ONLY`；未逐原子核銷 | Architecture Owner |
| H1 | 50 | `INDEX_ONLY` | System Owner |
| ModeGate | 39 | `INDEX_ONLY` | Program Owner |
| Oracle | 96 | `ORACLE_REGISTRY_UNBOUND` | Case/Oracle Owner |
| Cell | 192 | `INDEX_ONLY` | Architecture Owner |
| ToolNeed | 485 | `INDEX_ONLY`；不宣全 Fit | Tool Owner |
| Reviewer Tool | 35 | `INDEX_ONLY` | Reviewer Owner |
| User Subintent | 56 | `INDEX_ONLY` | Product Owner |

## 14 WP 狀態

| WP | 前置 | 本輪 As-Built | 狀態 |
|---|---|---|---|
| F5-W0-01 SourceFreeze | — | 13 個選定來源已 copy 並重算 bytes/lines/SHA | `AUTHOR_PARTIAL_SOURCE_SET` |
| F5-W0-02 PluginIdentity | 01 | `sbl-tpm-sp` 技能與 `plp-tpm-review` 腳本可讀；host 未被證明 Installed/Served | `AUTHOR_OBSERVED_LOCAL_ONLY` |
| F5-W0-03 PI/Reviewer | 01 | 無 Original PI Reader；只做作者審查 | `NOT_RUN` |
| F5-W0-04 W0M-PD | 02,03 | 只轉錄 W0M 的 A/B/C 與 Effect 設計 | `AUTHOR_DOC_ONLY` |
| F5-W0-05 W0-Control | 04 | 本 15 檔修補候選 | `AUTHOR_COMPLETE_WITH_HOLDS` |
| F5-W0-06 GuideThinStart | 04 | `W0_START_THIN_PROMPT.md` 候選 | `CANDIDATE` |
| F5-W0-07 BridgeRead | 06 | 四 API 與 path/ABI NEG 已寫 | `CANDIDATE` |
| F5-W0-08 NativeRead | 07 | 無 Host/Runner | `NOT_RUN` |
| F5-W0-09 FrozenChallenge | 08 | 無 Candidate/Oracle/Runner | `NOT_RUN` |
| F5-W0-10 ResearchCandidate | 09 | 只有 FAR 型別與 Resume 設計 | `CANDIDATE` |
| F5-W0-11 GuideResume | 10 | 只有 Resume/WAIT/PARK 候選 | `CANDIDATE` |
| F5-W0-12 NativeProtected | 04,05 | 無 Admission | `NOT_ADMITTED` |
| F5-W0-13 OriginalAssurance | 12 | 無 Original Checker | `NOT_RUN` |
| F5-W0-14 Delta/Handoff | 11,13 | 文件 Delta 與具名 HOLD | `AUTHOR_READY_WITH_HOLDS` |

## 七 Seam

| Seam | Producer → Consumer | 本包輸出 | NEG | FirstFail |
|---|---|---|---|---|
| SM-01 | SourceReader → Reviewer/PI | 真 bytes/SHA/span、M §12.7 原句 | 同名異 SHA | `SOURCE_INTEGRITY_FAILED` |
| SM-02 | PI → Wave/PD | AffectedPISlice、BindingRequest 欄位 | 假 HEAD 或字串 PD_BOUND | `PD_UNBOUND` |
| SM-03 | PD → ECP/TQAEP | DEV/OPS 前件、Case/Oracle 欄位 | ECP 自授權 | `ECP_NOT_GRANT` |
| SM-04 | Wave W0 → Guide1 | 六身份、A/B/C、ThinStart | Guide 擴 Scope | `SCOPE_DRIFT` |
| SM-05 | Guide/Bridge → Executor | 四 API Context、Body SHA/span | path/UNC/symlink escape | `PATH_OUTSIDE_ROOT` |
| SM-06 | Executor → Challenge → FAR | Frozen、POS/NEG、Raw 或 NOT_RUN | 無 Runner 宣 REPRODUCED | `UNREPRODUCED` |
| SM-07 | FAR → Guide2 → Consumer | Resume/WAIT/PARK 候選 | 自簽 CLOSE/RELEASE | `CLOSE_NOT_AUTHORIZED` |

## 共同驗收 POS/NEG

POS：一個受權 `SOURCE_READ` 只因 source SHA、Scope、ACL 正確即可繼續，不要求 W4 Release 或 W0-B Protected Admission。NEG：Parent「A、B各有」只做 A 不算整項 PASS；`permit=true`／假 WorkOrder 被拒；Native exit 0 但 WorldRaw 錯不可認 Effect Verified。

## 未授權停止點

缺真非 FHS Case、缺原 PI/PD/ECP/TQAEP Reader、缺 Repo/Host/Issuer/Admission、缺原 Case/Oracle/Fixture、缺 Checker/Publisher，均只停受影 Slice；不得以作者文件或本地腳本補造原域回執。
