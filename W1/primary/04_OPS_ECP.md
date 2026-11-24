<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜OPS ECP（作者計畫）

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的 OPS ECP 作者計畫，批次 `W1-PACK-01`。它不是原 Canonical OPS ECP，不是 Host 安裝單，也不是服務啟動命令。所有 Host effect 維持 `NOT_ADMITTED`。

## 1. Applicability 與 Effect

Applicability: W1 的 OPS 受影面是「未來把 Guide／Bridge adapter 註冊到 ChatGPT／Codex／Hermes」所需的 HostID、OS Principal、PolicyEpoch、loader、binding、service、ACL、readback 與 recovery 契約。本輪不執行安裝、註冊、綁定或啟動。

Effect: `SOURCE_READ + ISOLATED_DRAFT_WRITE + LOCAL_CHECK + LOCAL_PACKAGE`；OPS／USER／RELEASE 皆 `NOT_ADMITTED`。原 EffectRegistry 未綁，Host effect token 不得由 plugin 名稱或安裝路徑推定。

Input: W1M §05 的三 Host 七階段、B02／B03 的 Host 缺件表、H-CLOSE 的 Principal 分帳、W0 的 ACL 歷史觀測。
Operation: 寫出每個 Host 的 Pre／Post／WorldReader／Recovery 與最小 Raw 欄位；以本地唯讀探查確認容器能力，不升格為 Host 能力。
Output: 本 OPS ECP＋`00_WAVE_RUN_MANIFEST.json.host_claims[]`。
Consumer: 各 Host Owner／OS Principal／W4。
NEG: 以 `git revert` 當 Host recovery → `RECOVERY_KIND_MISMATCH`。
FirstFail: `HOST_PENDING`／`PRINCIPAL_DOMAIN_MISMATCH`。

## 2. Preconditions

Preconditions:

1. 原 Host Owner 提供 `HostID`、版本、loader manifest、installer_ref、`LoadedSHA`。
2. 原 OS Principal 提供 ACL raw 與受權路徑；不得以本機 `CodexSandboxUsers` 冒充原 Principal。
3. 原 Issuer 提供同 Subject／Scope／Host／PolicyEpoch 的 `ExecutionAdmission`；本輪 null。
4. `PolicyEpoch` 已固定，且每次寫入前可重讀；`UNKNOWN` 先由原 WorldReader reconcile。
5. Receiver ABI 與 PreWorldRaw／PostWorldRaw 的讀法已指定。

缺少任一項時，只可保存 `HOST_PENDING` 的 adapter 設計；不得執行 `install`、`register`、`enable`、`start`。

## 3. Host 契約與權限

| Host | HostID 來源 | Principal | 必要 receipt | 不可代償 |
|---|---|---|---|---|
| ChatGPT | 原 Host manifest | 原 OS Principal | installer＋loader＋binding＋consumer readback | Codex 的 Loaded |
| Codex | 原 Host manifest | 原 OS Principal | installer＋loaded_sha256＋invocation raw | 作者工具呼叫 |
| Hermes | 原 Host manifest | 原 OS Principal | installer＋binding＋三能力各自 Raw | Kanban 抵 Delegation／Swarm |

Permission: 本 ECP 不授予安裝或服務權。`publisher_receipt=null`、`execution_admission_receipt=null`、`verified_original_receipt_ref=null`。任何 Host 的 `Installed` 必須有 installer 或 registration receipt；`Bound` 必須有 binding record；`ActualServed` 必須有 served bytes 與 scope echo；`Consumed` 必須有 consumer readback。四者不可互推。

## 4. Operation（未來受權）

Operation: Step 1 以原 Host loader 安裝指定版本，記 installer exit／stdout／stderr SHA；Step 2 以原 registration API 註冊，記 manifest 與 loaded SHA；Step 3 綁定 Subject／Scope／PolicyEpoch；Step 4 以最小 request 呼叫，記 command／args／exit／stdout／stderr SHA；Step 5 取 ActualServed bytes 與 scope echo；Step 6 由 Consumer 讀回並記 consumed SHA 與時間。

每一步只能由該 Host Owner 在該 Host 原環境執行；作者只提供步驟與 ExpectedRaw。若 Host 只提供文檔型 skill（如本輪 Codex 可讀 `SKILL.md`），只能記 `SKILL_BYTES_READ_LOCAL`，不得記 `Installed`。

## 5. Postconditions 與 Readback

Postconditions:

1. 每 Host 七階段各有一列狀態與證據型別；`NOT_OBSERVED` 明示，不以空白代替。
2. `host_claims[]` 的 observation 只使用允許的 evidence class。
3. 三 Host 的 `Consumed` 各自獨立；同一 Host 的 `Loaded` 不核銷另一階段。
4. Hermes 三 child 各有 `child_id`、observation、Consumer、ExpectedRaw、NEG、Owner。
5. 本輪未產生任何 installer／service raw，故 Host 欄位保持 `HOST_PENDING`。

Readback: Host Owner 以原 loader／invoker／service log 回讀；作者以 `evidence/raw/host_probe.txt`（本輪已實際產生）記錄「本機可見／不可見」的容器事實，並在報告中標 `CONTAINER_ONLY`。不得把容器事實當產品 Host 事實。

## 6. Recovery 與 Stop／Resume

Recovery: 原 Host 的復原必須使用該 Host 的 uninstall／rollback／service restore，記 before／after world SHA 與 exit；不得用通用 `git revert` 或刪除 log 代替。若 Host 回復不可用，記 `HOST_RECOVERY_UNBOUND`，只停該 Host 的 claim。

Stop: 缺 HostID、Principal、PolicyEpoch、loader、installer、binding、consumer readback 任一項，停該 Host 的該階段；其他 Host 與作者章節繼續。

Resume: 同 Subject／Scope／Host／PolicyEpoch 的 typed receipt；不得以 plugin 名稱、skill 可讀、public commit 或作者 CLI exit 0 補位。
