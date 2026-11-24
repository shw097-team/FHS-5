<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W0","scope":"W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED","wave_id":"W0","batch_id":"W0-CODEX-REPAIR-20261123-01","source_manifest_sha256":"22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f"} -->

# 06_PERMISSION_STOP_RESUME

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

Input: Effect、Owner、原 Issuer/OS Principal、WorkOrder/Admission、Repo/Host/Epoch 與現有回執。
Operation: 把 READ/DRAFT/DEV/OPS/USER/RELEASE 的效力、停止點與恢復條件分帳。
Output: 每個 Effect 的允許狀態、缺件、Owner、Stop 與 Resume predicate。
Consumer: Guide、Bridge、Original Executor、Issuer、Host Owner、Publisher。
NEG: 把 ECP intent 當 Grant、把 skill 可讀當 Host Installed、或把作者 PASS 當 Independent PASS。
FirstFail: FALSE_AUTHORITY / NOT_ADMITTED / ORIGINAL_RECEIPT_UNVERIFIED。

## Effect 效力矩陣

| Effect | 本輪效力 | 原權限主體 | 必要回執 | Stop | Resume predicate |
|---|---|---|---|---|---|
| `SOURCE_READ` | 允許，限選定來源 | Source/Guide Owner | source SHA、Scope、ACL | SHA/ACL 不符或 path escape | 同 Scope 真 bytes 與可讀 ACL |
| `ISOLATED_DRAFT_WRITE` | 允許，限本輸出根 | Pack Author | 隔離 root、before SHA | 越界、symlink/reparse、寫來源根 | 新隔離 root 與可讀回檔案 |
| `DEV` | `NOT_ADMITTED` | Repo Owner + Original Issuer | OperationType、Repo HEAD、WriteSet、WorkOrder/Admission | 缺任一前件 | 同 Repo/Scope 的 typed receipt + preimage |
| `OPS` | `NOT_ADMITTED` | Host Owner + OS Principal + Issuer | HostID、PolicyEpoch、Receiver ABI、WorkOrder/Admission | 缺任一前件或 recovery ABI | 同 Host/Epoch 的 typed receipt + WorldRaw 能力 |
| `USER` | `NOT_CLAIMED` | Original Consent Owner | 原 consent/data scope | 無 consent 或資料範圍不明 | 原 consent 與 compensation |
| `RELEASE` | `NOT_CLAIMED` | Original Publisher | Checker/Publisher receipt、GCP/GHP 門檻 | 缺 Checker/Publisher | 同 Candidate/Scope 的原發布收據 |
| `HUMAN_OWNER_SELECTION` | 已記錄；本地可執行主選 | Human Owner | selection receipt | 當成 Original Issuer/OS/Checker | 原域 typed receipt |

## Human Owner 可執行主選

| 欄 | 值 |
|---|---|
| selection_id | `W0-EXEC-SEL-20261124-01` |
| selection_effect | `OWNER_AUTHORIZED_LOCAL_W0_A_C` |
| W0-A | `EXECUTABLE_ROUTE_SELECTED`；真 Case 未得時回 `W0-A_CASE_SELECTION` |
| W0-B | `NOT_ADMITTED_ORIGINAL_DOMAIN`；不因 Owner 選擇而變成 Repo/Host Grant |
| W0-C | `EXECUTABLE_APPLICABILITY_SELECTED` |
| original_domain_receipts | `null` |

Owner 選擇只授權本地 W0-A/C 控制包執行與 W0-B 的條件式準備；不替代原 Issuer/OS Principal/Checker。若要把 W0-B 變成可執行，必須另取得 Original OperationType、Repo/Host、WorkOrder、ExecutionAdmission 與 WorldReader。


## 具名 HOLD

| HOLD | 真缺口 | Owner | Resume predicate |
|---|---|---|---|
| `W0-A_CASE_SELECTION` | 尚無真非 FHS PLP/Requirement/Case/Oracle 的選定 bytes | Original Project/Source Owner | 同 Scope 真 bytes + Case/Oracle 可回取 |
| `W0-B_NOT_ADMITTED` | 無 Issuer/WorkOrder/Repo/Host/OperationType/Admission | Original Issuer/Executor | 同 Scope Admission + ECP + WorldRaw 能力 |
| `ORIGINAL_READER_UNBOUND` | 無 PI/PD/ECP/TQAEP/Case 的 typed reader 回執 | Original PIPD Reader/Case Owner | typed readback（reader name/version、subject、scope、source SHA） |
| `ORACLE_FIXTURE_UNBOUND` | 24 原 Case 無 Oracle/Fixture bytes | Original Case/Oracle Owner | 真 Case/Oracle/Fixture bytes + SHA |
| `HOST_CAPABILITY_UNBOUND` | 無 Host ActualServed 證據 | Host Owner | manifest/loaded/invoked/consumed 四段證據 |
| `CHECKER_PUBLISHER_UNBOUND` | 無 Protected Checker/Publisher | Original Checker/Publisher | 同 Candidate/Scope/Host/PolicyEpoch 的獨立收據 |
| `SOURCE_REFERENCE_HASH_CONFLICT` | W0MB §00 與 W0ME E1 的歷史 CTRL/START 指紋可能不同 | W0M Author | 以本輪實讀 CTRL/START SHA 對位，不再單邊採信 |

## LastGood 與 UNKNOWN

LastGood 是本 15 檔 + 13 個來源副本 + 證據附錄的 hash-stable 版本；逐檔 SHA 見附錄 E6。任何替換先寫 tmp、再 rename，並保留 before SHA。`UNKNOWN` 先由 Original WorldReader/HostReader reconcile，再決定 retry/compensate/fail；作者端不盲重試。

## 重試上限

同一 `Subject/Scope/SourceSHA/FirstFail` 在沒有新 Source/Oracle/Host/Epoch/Admission Delta 時，最多兩次有根據的作者修補；仍未解記 `HOLD/PARK + Owner + Resume`，不無限重派，也不新增第二 Gate。
