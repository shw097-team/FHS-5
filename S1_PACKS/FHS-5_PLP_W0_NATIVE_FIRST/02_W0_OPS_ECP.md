# 02_W0_OPS_ECP｜W0 S1 受影主用包（OPS ECP）

**S1 pack**：`W0-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W0/PACK-S1-20261126-r2`  
**supersedes**：`FHS5-PLP/W0/PACK-S1-20261126-r1` / `W0-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W0/PACK-NF-20261125-03` / `W0-NF-r3-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`｜固定 commit `ae05a74514d2c310f82bbf9bb1a2009078f11c87`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 受影重構的完整正文；本輪已依 Owner 預授權升格為「主用＋受界可施工」（document primary）。S1 節只替換受影 clause；未受影段落、原 ID、原分母、原 fixture/oracle bytes 與歷史證據原樣保留（見文末「原版正文」）。衝突時以原上位原義＋S1 受影條款為準；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## S1-0｜S1 對 OPS ECP 的受影增量

原 O1–O6、effect 分帳、UNKNOWN 與 recovery 全數保留；本節只補「當期 Host 必須重探」與「不得把歷史 host ref 當 current」。

### S1-0.1 歷史 Host 與當期狀態

| 欄 | 原版記錄（2026-11-25） | S1 判定 |
|---|---|---|
| Host kind | `CODEX_LOCAL_WINDOWS` | `HISTORICAL_REPORTED`；S2 需重探 |
| Host ref | `CODEX-LOCAL-dab97dce04ed` | 不得跨期沿用；`HOST_EPOCH_UNVERIFIED` |
| Principal ref | `principal-12dc3e86dd73445f` | 同上；不得以舊 ref 發 OPS |
| Policy version | `FHS5-CODEX-FIRST-2026-11-25` | 同上；Owner 未更新即只作歷史 |
| 本輪作者探測 | 只讀 git metadata；未變更 Host/ACL | `AUTHOR_READ_ONLY` |

### S1-0.2 每 op 的 OPS admission（不得 blanket）

每個 OPS op 在 effect 前必須同時具備：真 HostID／principal／policy epoch（或合法 `NOT_DECLARED_BY_HOST`＋probe raw）、target／output root、exact preimage/absence、receiver ABI、recovery ref、Owner 有效 scope。缺任一即 `NOT_ADMITTED`，只停該 op；READ/DRAFT 與其他 op 可續。

### S1-0.3 O3/O4 的實際邊界

| 步驟 | 允許 | 禁止 |
|---|---|---|
| O3 可逆輸出 | 在授權 `work/` 或 `outputs/` 建新檔；before absent、after bytes/SHA | 寫 source 根、repo 工作樹、或任何 write-set 外路徑 |
| O4 readback | 獨立讀 output／source raw SHA；restore 後 pre-state 讀回 | 用 `git revert` 冒充 OPS recovery；用 exit 0 冒充 effect verified |
| UNKNOWN | 先 readback/reconcile；確認仍 pre 且 idempotent 才最多一次有理由 retry | 盲重試；把 UNKNOWN 改寫成 PASS |

### S1-0.4 撤權與 safety veto

Owner 撤權、scope/target/effect 變更、真 ACL 拒絕、或安全 Finding 未解，皆立即停受影 OPS；不得換 root／換工具／改 marker 繞過。舊 W2 Writer 撤權與本波 OPS 無關，但同樣不可被「新候選」文字解封。

---

## 原版正文（血緣保留；S1 未明示者不變）

> **原版身份（superseded）**：以下為原版 `W0-NF-r3-CODEX-PRIMARY` 的 preamble 與正文，按原 bytes 保留。
>
> 其中所有 `PRIMARY`／`PASS`／`已完成`／`AUTHORIZED` 均屬原版歷史陳述，不適用於本候選；本候選效力只以上方 S1 header 與 S1 節為準。
>
> # 02_W0_OPS_ECP｜CODEX Native 本地 OPS Contract
>
> **identity**：`FHS-5_PLP/W0`｜**batch**：`FHS-5/W0/B0-NF`｜**pack**：`W0-NF-r3-CODEX-PRIMARY`  
> **source W0M**：`NF-r3-PRIMARY`＋`W0M-CODEX-FIRST-r4` 修訂；原 raw `a1f186cc…`；amendment 見 `W0M_CODEX_FIRST/`  
> **document state**：`ADOPTED_LOCAL_CODEX_NATIVE_OPS_ECP`｜**product actual**：由 B0 執行時填入 EVIDENCE  
> **OPS admission**：`ADMITTED_WITHIN_LOCAL_CODEX_SCOPE`（決策 `W0-OPS-NATIVE-20261125-01`）
>
> > 本檔是 Human Owner 依 `W0-CODEX-FIRST-20261125-01` 正式採納的本地 CODEX Native OPS 契約。它承接 FHS-5 Generic Native 主工程當期真正需要的本地操作授權、安全範圍、preimage、readback、restore 與驗收義務；不是 OS/Repo 管理員 grant，也不是原域 Legacy Profile 的 Original OPS ECP 替身。

## 00｜OPS 邊界與實際 Host

### 00.1 法位

| 欄 | 值 |
|---|---|
| 契約類型 | `LOCAL_CODEX_NATIVE_OPS_ECP` |
| 採納決策 | `W0-OPS-NATIVE-20261125-01`（Human Owner 正式裁決） |
| 上位修訂 | `W0-CODEX-FIRST-20261125-01`；W0M §05.5 #5／§08.5 的 CODEX-first amendment |
| 原 Original OPS ECP #5 | 歷史身份保留；`HISTORICAL_UNBOUND`；只在真正需要原域契約的 Legacy Profile 另接 |
| 不建立 | 第二 Runtime／Queue／Dispatcher／Issuer／Registry／ACK／Reader 服務 |
| 不偽造 | OS/Repo/Host 管理員權限、原域 receipt、Publisher/Release |

### 00.2 本輪實際 Host／principal（CODEX 自主 probe）

| 欄 | 實際值 | 取得方式 |
|---|---|---|
| Host kind | `CODEX_LOCAL_WINDOWS` | 目前 CODEX desktop 執行環境 |
| OS | `Microsoft Windows 10.0.26200` | `RuntimeInformation.OSDescription` |
| Host ref | `CODEX-LOCAL-dab97dce04ed` | `SHA256(COMPUTERNAME)` 前 12 hex；不記錄原名 |
| OS principal ref | `principal-12dc3e86dd73445f` | `SHA256(USERDOMAIN\USERNAME)` 前 16 hex；不記錄原名 |
| Policy version | `FHS5-CODEX-FIRST-2026-11-25` | 本次 Owner 決策 |
| Python | 3.11.9 | `python --version` |
| Git | 2.53.0.windows.1 | `git --version` |
| CODEX CLI | 可用（`codex.ps1`） | `Get-Command codex` |
| Sandbox temp | `...\openai.codex_...\AC\#!sandbox...\Temp` | 環境實際值 |
| Workspace write root | `C:\Users\user\Documents\Codex\2026-11-25\new-chat-5` | 本輪授權工作區 |
| Output/evidence root | `...\outputs\FHS-5_PLP_W0_Native-first_CODEX_主用修補_交付` 與 `work\B0-NF` | 本輪建立，不寫來源 |
| HERMES | binary 存在但 install state 不可寫 | 保留 `HOST_SERVING_UNVERIFIED` 歷史觀測；不阻斷 CODEX |

**Actual boundary**：本契約只覆蓋 local CODEX 的檔案/CLI/程序/sandbox 操作；不覆蓋遠端部署、OS 服務安裝、註冊表/ACL 變更、金融/個資外部 effect 或公開發布。

### 00.3 Effect 分帳（本輪）

| Effect | 本輪 | 邊界 |
|---|---|---|
| `SOURCE_READ` | `ADMITTED` | 只讀授權 root；SHA/span |
| `ISOLATED_DRAFT_WRITE` | `ADMITTED` | 只寫 `work/`、`outputs/`；不寫來源 |
| `DEV` | `ADMITTED_WITH_WRITESET` | 只在新隔離 Git repo；逐檔 write-set/preimage |
| `OPS` | `ADMITTED_WITHIN_LOCAL_SCOPE` | 本契約 O1–O6；受 preimage/readback/restore |
| `USER` | `NOT_AUTHORIZED` | 無外部 consent |
| `RELEASE` | `NOT_AUTHORIZED` | 無 Publisher |
| `EXTERNAL_ADMIN` | `NOT_AUTHORIZED` | 不改 Host/ACL/route |

## 01｜O1 CODEX Native 冷啟與 readiness

### 01.1 Probe

```powershell
Get-Command codex,python,git -ErrorAction SilentlyContinue
codex --version
python --version
git --version
$env:COMPUTERNAME
[System.Runtime.InteropServices.RuntimeInformation]::OSDescription
```

### 01.2 Planned Native start

| 欄 | 值 |
|---|---|
| session | 目前 CODEX 執行 session／後續 `codex exec` 或互動 session；以實際可用為準 |
| manifest | `05_W0_SOURCE_MANIFEST.json` |
| input | `04_W0_START_THIN_PROMPT.md` |
| cwd | 本輪 pack root 或 `work\B0-NF` |
| timeout | 120 秒初值；實測後凍結 |
| expected | 真讀 pack digest、建立 session/task ref、可執行 probe |

**Readiness**：`READY`（CODEX CLI 可用）。HERMES 的 `HOST_SERVING_UNVERIFIED` 不作為 O1 阻斷；HERMES 只在 Compatibility 另驗。

## 02｜O2 Planned local CLI run

### 02.1 Entrypoint

本輪 B0 選 `briefcheck`（Search-before-Build 後由 CODEX 依 Owner 規則自主選定）：

```text
python -m briefcheck --root <approved_read_root> --input case_ok.md --sha256 <expected>
python -m briefcheck --root <approved_read_root> --input case_missing.md --sha256 <expected>
```

`case_ok` 期望 `exit 0`、`status COMPLETE`；`case_missing` 期望 `exit 2`、`missing ["B"]`。

### 02.2 argv/cwd/env/timeout

| 欄 | 值 |
|---|---|
| cwd | B0 repo root（D1 凍結） |
| env | `PYTHONIOENCODING=utf-8`；不加 secret |
| stdout | stable UTF-8 JSON |
| stderr | 短錯誤碼；不洩露 root/正文 |
| timeout | 30 秒；實測後凍結 |
| write | O2 正常不寫 source/output |

### 02.3 Required actual evidence

`session/task ref`、manifest/pack digest、argv、cwd、env、exit、stdout/stderr path+SHA、Host/version、observer。actual 只寫 `EVIDENCE/`，不寫回本檔。

## 03｜原 Original OPS ECP #5 的 CODEX-first 處置

### 03.1 歷史調查（保留）

| 來源 | 實際內容 | 結論 |
|---|---|---|
| 舊 W0 `04_OPS_ECP.md`（`92131ad4…`） | `claim_ceiling=AUTHOR_DESIGN_ONLY`；明示「不是 Canonical ECP、不是 Grant」 | 不是原域 typed ref |
| 舊 `02_ORIGINAL_CONTRACT_REFS.json`（`81d40902…`） | `ops_ecp_ref=null`；`original_issuer_state=UNBOUND` | 無原域收據 |
| W2M §03.1 #5 | `Original OPS ECP` 狀態 `UNBOUND` | 無 typed ref |
| W0M §05.5 #5／§08.5 | 舊規格以原 OPS ECP 為 OPS 閘 | 已由本次 Owner 裁決修訂 |

### 03.2 正式裁決（已生效）

> `W0-OPS-NATIVE-20261125-01`：對 FHS-5 Generic Native 主工程，採納本 `02_W0_OPS_ECP.md` 作為本地 CODEX Native OPS ECP，承接 O1–O6 的本地非部署操作。原 Original OPS ECP #5 保留歷史身份與 Legacy Profile 適用性，不再作為 Generic CODEX 本地 OPS 的必要前置。HostID/Principal/PolicyVersion/Output Root/Recovery 由 CODEX 在合法環境自主 probe 與核實；不偽造 OS/Repo/Host 權限，不建立專屬 Epoch/Registry/Issuer/ACK/Reader。

**衝突消除**：W0M §05.5 #5 的 `UNBOUND` 狀態標記為 `HISTORICAL_UNBOUND`；§08.5 的「O2–O4 NOT_ADMITTED」改為「在本地 principal/scope/preimage/recovery 成立時 ADMITTED」。`W0M-CODEX-FIRST-r4` 已記錄 §00.6 修訂摘要。

### 03.3 前件狀態

| 項目 | 狀態 | 取得 |
|---|---|---|
| Local OPS ECP | `ADOPTED` | 本檔＋`W0-OPS-NATIVE-20261125-01` |
| Host ref | `READY` | `CODEX-LOCAL-dab97dce04ed` |
| Principal ref | `READY` | `principal-12dc3e86dd73445f` |
| Policy version | `READY` | `FHS5-CODEX-FIRST-2026-11-25` |
| Receiver ABI | `LOCAL_JSON_STDOUT_V1` | briefcheck stdout schema |
| Output root | `READY`（work/B0-NF/evidence） | 本輪建立 |
| Preimage | 每個操作前凍結 | O3 前 |
| Recovery | 刪本次新檔／preimage 還原 | O4 |
| Original OPS ECP | `HISTORICAL_UNBOUND` | 只在 Legacy Profile 另接 |

## 04｜O3 可逆輸出

1. 以受權 wrapper 將已知 `case_ok` stdout 寫入 output root 的新檔。
2. 記錄 before absent、after bytes/SHA、source SHA（不變）。
3. 讀回 output 內容與 JSON schema。
4. 若 output root 不在授權範圍、無 preimage 或 wrapper 會寫 source，停止。
5. 不得把 stdout 直接導向 source 根或 repository 工作樹。

**本輪狀態**：`READY`（output root 已指定；執行時填 actual）。

## 05｜O4 Readback／Restore

| 步驟 | 要求 | 失敗 |
|---|---|---|
| before | output absent 或 preimage SHA | 無 before→不跑 |
| after | output bytes/SHA | 不符→`EFFECT_NOT_VERIFIED` |
| source | source raw SHA 不變 | 變動→立即停／恢復 |
| restore | 原 absent 只刪本次 output；有 preimage 則還原 | 不可恢復→停 |
| final | source/output final state 可讀 | 不能確認→UNKNOWN reconcile |

`git revert` 不可作 OPS recovery；檔案層補償與 preimage 還原才是本 B0 的回復依據。

## 06｜O5 Provider OFF／optional parity

### 06.1 OFF 條件

- 隔離 profile 不載入 HGK/FABRIC/SBL/FHS/PIPD general providers。
- 以實際 load/import/call trace 或等價觀察，不以環境變數單獨宣稱。
- 在 OFF 下重跑 briefcheck 的 direct path（不經 Bridge/FAR）。

### 06.2 Parity

| 路徑 | ON | OFF | 判定 |
|---|---|---|---|
| Source/package direct read | 可用 | 可用 | 不受影 |
| briefcheck POS/NEG | 可用 | 可用 | 結果相同 |
| Bridge 四 API | 另驗 | 不要求 | OFF 時 direct 可用 |
| FAR 研究 | 另驗 | 對明確 bug 可 bypass | 不在 OPS Gate |

五方自身產品驗證不可只用 OFF/direct 完成；Bridge/FAR 專屬案另在 ON 驗。

## 07｜O6 Consumer 接力

新 session 或具名 consumer 必須：

1. 讀 `05_W0_SOURCE_MANIFEST.json` 與 `04_W0_START_THIN_PROMPT.md`。
2. 核 manifest SHA/bytes、source identity、pack status。
3. 讀 actual `EVIDENCE/` 與 `HANDOFF`。
4. 執行下一個合法 readback 或 NO-OP；不得用 ACK 字串代替。
5. 錯版/舊 SHA 拒收；無 consumer readback 只記 partial。

## 08｜CODEX OPS admission matrix

| 步驟 | 狀態 | 解鎖條件 |
|---|---|---|
| O1 CODEX 冷啟 | `READY` | CODEX CLI／session 可用 |
| O2 CLI 正負 | `READY_WITH_SAMPLE` | briefcheck repo/preimage/oracle |
| O3 可逆輸出 | `READY_WITH_OUTPUT_ROOT` | output root＋preimage |
| O4 readback/restore | `READY_WITH_RECOVERY` | 檔案層 recovery |
| O5 Provider OFF | `PLANNED` | 隔離 profile＋run trace |
| O6 Consumer | `READY_AFTER_EVIDENCE` | 真 handoff |

## 09｜UNKNOWN／Retry／Stop

| 情況 | 處置 |
|---|---|
| command timeout | 先 readback；未確認 state 不重跑 |
| session 中斷 | 查 process/output；reconcile |
| output 寫入未知 | 停 O3；查檔案 state；不盲刪 |
| source 變動 | 停；恢復 preimage；記 incident |
| 權限被拒 | `AUTHORITY_REQUEST`；提供精確 root/principal/期限 |
| 無真 sample | `SAMPLE_SELECTION_REQUIRED`；其他 READ 可續 |
| HERMES 不可服務 | 記 Compatibility 觀測；不阻斷 CODEX |

同一 transient I/O 最多一次重試；同一 Finding 最多兩次有實質差額修補；無 delta 停。

## 10｜NEG

- 把本檔當原域 Original OPS ECP 或 OS/Repo/Host 管理員 grant。
- 把 `permit=true`、Owner local selection 或 CODEX 可啟動當外部 grant。
- 以 DEV ECP 代替 OPS ECP。
- 以 `git revert` 作 OPS recovery。
- 只改 env 就宣 Provider OFF。
- 只貼 prompt 就宣 Native consumed。
- 在 output/source 根外寫入或讀取。
- 以 HERMES 不可服務阻斷 CODEX 主工程。
- 宣稱其他 Host（HERMES/GPT CHAT/GPT WORK）已實際通過。

## 11｜Not claimed

`EXTERNAL_GRANT=NO`、`OS_ADMIN=NO`、`PUBLISHER_RELEASE=NO`、`HERMES_COMPATIBILITY_PASS=NO`、`OTHER_HOST_PASS=NO`。本檔只承接本地 CODEX OPS；產品 B0/W0 verdict 由實際 EVIDENCE/CLOSEOUT 判定。
