# 01_W2_DEV_ECP｜W2 S1 受影主用包（DEV ECP）

**S1 pack**：`W2-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W2/PACK-S1-20261126-r2`  
**supersedes**：`FHS5-PLP/W2/PACK-S1-20261126-r1` / `W2-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W2/PACK-NF-20261126-r3` / `W2-NF-r3-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `81daac8ff3f47566d18cc7ebdaee9625ff5ca000b71caac3226841b124f6099b`｜固定 commit `35d5387f9c98eaebc2d4cee742afcb4509a7d8c3`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 受影重構的完整正文；本輪已依 Owner 預授權升格為「主用＋受界可施工」（document primary）。S1 節只替換受影 clause；未受影段落、原 ID、原分母、原 fixture/oracle bytes 與歷史證據原樣保留（見文末「原版正文」）。衝突時以原上位原義＋S1 受影條款為準；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## S1-0｜S1 對 DEV ECP 的受影增量

原 `DEV-D01..D07` 全保留；本節把 S3 的 DEV-A 寫成可直接施工的契約，並固定「不得碰 protected 原檔」。

### S1-0.1 RepoContext（當期）

| 欄 | 值／取得 | 狀態 |
|---|---|---|
| repo root | Owner 指定可 chdir 的隔離 worktree；`git rev-parse --show-toplevel` | `UNBOUND`（本輪未取得） |
| base | Product `dada2354…`；Delivery `3346076c…` | 可定位（本輪 `git show` 成功） |
| HEAD/branch/dirty | `rev-parse HEAD`／`branch --show-current`／`status --porcelain=v2` | `UNBOUND` |
| ACL/principal | 真 OS ACL；不以文件許可代替 | `UNBOUND` |
| preimage | 逐 target raw SHA／ABSENT | `UNBOUND` |
| 禁止 | 原 `C:\Projects\...\FHS-5_Workspace` 工作樹、protected marker、W3 分支 | — |

### S1-0.2 最小 DEV-A（W2-DEV-01）

| 欄 | 內容 |
|---|---|
| WriteSet | **MODIFY** `W1/check/w2_receiver.py`（preimage `768d6318…`）；**ADD** `W1/check/test_j1_receiver.py`（ABSENT） |
| 目的 | 把 verify-only 與 consume 分離；verify 失敗短路，零 product call／零 input write；成功才 consume |
| 前置 | caller HEAD=live HEAD；exact write set；preimage；Owner DEV scope；recovery；frozen tests |
| 操作 | `git apply --check` 預查（非 admission）→ 受權 apply_patch → affected tests → post SHA → reverse |
| Expected | patch diff 只含 2 target；post SHA 在 oracle；tests exit 0 且 stdout 符合；reverse 後 preimage 讀回；unlisted 檔不變 |
| NEG | HEAD 不符 `REPO_HEAD_MISMATCH`；preimage drift；write-set 外變更；`permit=true`；越界 path |
| Recovery | reverse patch＋SHA 讀回；不得 `reset --hard` 未知樹 |
| 不宣稱 | 原域 DEV ECP；不同 principal；W3/W4 全量 |

### S1-0.3 正控與不可冒充

正控：spy 必須檢出一次真 write/call；否則 `OBSERVER_UNPROVEN`。負控：所有拒絕必須 `write_count=0`、target bytes 不變。exit 0 但 post 錯 → `EFFECT_NOT_VERIFIED`；只有 `git diff --check` 通過不算完成。

### S1-0.4 不宣稱

`DEV_EXECUTED=NO`；`W2-DEV-01=NOT_RUN`；`W2 Writer` 仍 `BLOCKED_NOT_ADMITTED`。本檔不是 Grant。

---

## 原版正文（血緣保留；S1 未明示者不變）

> **原版身份（superseded）**：以下為原版 `W2-NF-r3-CODEX-PRIMARY` 的 preamble 與正文，按原 bytes 保留。
>
> 其中所有 `PRIMARY`／`PASS`／`已完成`／`AUTHORIZED` 均屬原版歷史陳述，不適用於本候選；本候選效力只以上方 S1 header 與 S1 節為準。
>
> # 01_W2_DEV_ECP｜W2 DEV 受界可逆操作契約
>
> **artifact_id**：`FHS5-PLP/W2/PACK-NF-20261126-r3`
> **subject_id**：`FHS-5_PLP/W2/CONTROL_PACK`
> **scope**：`W2-NF-01`
> **candidate**：`W2-NF-r3-CODEX-PRIMARY`
> **kind**：`DEV ECP`（與 `02` OPS ECP 分域）
> **狀態**：`PLANNED / NOT_ADMITTED`
> **claim ceiling**：本檔是操作契約，不是 Grant、不是已執行結果
>
> > 本檔只描述 DEV 域的受界、可逆、可讀回操作。每個 op 的 runtime 值（repo root/HEAD/ACL/preimage/argv 實測/post）在本輪一律 `null`／`PENDING`；由 `00` §7.2 的 producer 在實際環境取得。任何未取得的欄位不得以檔名、舊 bytes、caller 自報或 G4 類比補位。

## 0｜DEV 域邊界

### 0.1 適用與不適用

| 項 | DEV 域 | 不屬於 DEV |
|---|---|---|
| 身分 | RepoRoot／HEAD／branch／dirty／untracked／ACL／exact write set／preimage | HostID／OS principal／policy epoch／receiver |
| 主要 effect | 受界 repository write（patch／新增／刪除）＋受影測試 | Host state、deployment、process、network、secret |
| 回復 | reverse patch／受界 rollback commit／還原 preimage | `git reset --hard`、`git clean -fd`、全 repo revert、OPS compensation |
| 讀回 | git diff／postimage SHA／test raw／RepoReader／consumer parse | WorldRaw／Original Receiver receipt |
| 授權 | Owner/issuer 的 DEV scope＋repo ACL＋exact write set | 以 OPS scope 或 DEV scope 自動取得 OPS 權 |

### 0.2 禁止事項

1. 不執行 `git reset --hard`、`git clean -fd`、無界 `checkout`、全 repo `revert`、全 repo glob 寫入。
2. 不清除他人 dirty／untracked；不覆寫未列入 write set 的檔案。
3. 不以 caller 自報 HEAD／preimage、舊 commit、G4 preimage 或 workspace manifest 代替 live probe。
4. 不以 patch apply 成功、test exit 0、CLI 0 或作者 summary 代替 semantic post＋readback。
5. 不在同一 op 混入 OPS host effect；不把 W0/W1 舊授權帶入 W2。
6. 不修改 NF-r5 sealed delivery；修補只在新的 isolated branch/worktree 或 W2 wrapper，且需當期 write set。
7. 不把 `01` 文件存在、`admitted` 欄位或 Owner 的一般指示當成 Grant。

### 0.3 本輪作者主機觀測（只作 late-bind 起點，不是 W2 runtime）

| Probe | 實際值 | 狀態 |
|---|---|---|
| Python | 3.11.9 | `AUTHOR_HOST_OBSERVED` |
| Git | 2.53.0.windows.1 | `AUTHOR_HOST_OBSERVED` |
| Codex CLI entry | `C:\Users\user\AppData\Roaming\npm\codex.ps1` | `ENTRY_PRESENT`；版本未在作者回合執行產品 |
| W2 runtime repo | `null` | `W2_REPO_BIND` |
| W2 runtime host | `null` | `W2_HOST_BIND` |
| 授權 | `null` | `NOT_ADMITTED` |

> 這些是作者環境的 read-only 觀測，不可當 CODEX W2 Host 的 `Selected/Loaded/...` 證據，也不可寫入 W2 `HostCapabilityLedger` 的 observed 欄。

## 1｜每個 DEV op 的共同契約

每個 op 必須有下表全部欄位；缺任何 HARD 欄位即停該 op。

| 區塊 | 必要欄 | 取得／驗證 | 拒收例 |
|---|---|---|---|
| identity | project/subject/scope/wave/batch/work/op_id、kind=DEV、candidate、source/pack pins、Req/Child/WP/Case refs | 05 pins＋本檔 local clause；同版一致 | W1 producer identity 當 W2；op id 重用 |
| permission | Owner 採納 ID、真授權 ref、allowed roots、exact operation、risk、expiry/revocation、OS/Repo ACL、native work order、原域 applicable ref | Owner decision／repo probe；ECP≠Grant | `permission=true`、過期、越 scope、caller bool |
| repo pre | 同次 `rev-parse --show-toplevel`／HEAD／branch/detached／`status --porcelain=v2 --untracked-files=all`／remote/ref／ACL／dirty preservation／candidate baseline | live git＋ACL；同次 snapshot | root 與工作區混淆、假 HEAD、dirty 不清理他人 |
| write set | 每 target relative path/kind/operation/add-modify-delete、before exists/bytes/SHA、mode/metadata、allowed post shape；rename 列兩端 | 逐檔 probe；absent 需 parent probe | 全 repo glob、未列刪除、空字串冒 absent |
| procedure | exact argv/cwd/env allowlist/timeout、必要 test command、sandbox/讀取權、patch artifact/ref/SHA | 本機 actual help／entry；未實測不猜 | 未測 help 猜 CLI、執行來源內命令、含 secret |
| expected/post | 每 path after digest/absence、diff raw/SHA、test exit/stdout/stderr/raw、semantic acceptance | frozen predicate＋實算 | CLI 0 當成功、unlisted drift |
| readback | RepoReader/live Git/file bytes/consumer parse；same subject/scope/head/candidate | 獨立程序或 reader | maker 自報 summary |
| recovery | per-file immutable preimage、reverse patch SHA、dry check、恢復副本 readback；dirty conflict 不覆寫 | 另存 preimage；獨立 copy 驗 reverse | 無 preimage、未知 target、全 repo restore |
| idempotency | task＋op＋HEAD＋write set＋admission 的 stable key；同 key 先讀回 | 本地 ledger | 無 key 重放 |
| unknown | `REPO_UNKNOWN`／`WRITE_SET_UNBOUND`／`EFFECT_NOT_VERIFIED` 的 readback route | RepoReader | 盲重試、UNKNOWN 改寫 |
| stop/resume | stop scope、lastgood、next、resume predicate | 每 op 記錄 | 全域停或無 resume |
| actual | 本輪 `null`；施工後真 raw locator/SHA | 只有真跑才填 | 作者回合預填 observed |

## 2｜DEV-D01 Probe / Freeze Binding

| 欄 | 內容 |
|---|---|
| identity | `op_id=DEV-D01`；work=`W2-NF-D01-<run>`；kind=DEV；effect=`REPOSITORY_READ`（read-only，非 write effect） |
| Req/Child/WP/Case | W2-B02、U-013.a、WM2-P02、W2-R3-03/04；J1-T01/T03 |
| permission | READ scope＋allowed roots；Owner 採納 ref＝`null`（本輪）；真 repo ACL＝`null` |
| repo pre | 同次 probe；不得只讀 manifest |
| write set | 空（本 op 無 write） |
| procedure | 見 §2.1 命令；cwd=真 repo 或上層可讀 root；timeout 30s／命令 |
| expected | root 存在、HEAD 40-hex、dirty/untracked 完整、ACL 可讀或明示 `UNBOUND`、candidate baseline 可定位 |
| readback | 相同命令重讀或獨立 shell；值一致 |
| recovery | N/A（無 write）；若 probe 產生暫存，刪本 op 建立的暫存並讀回 |
| idempotency | `(subject, scope, op_id, repo_root, head)` |
| unknown | `REPO_UNKNOWN` → 停 DEV write；不改 repo |
| stop/resume | 錯 root/HEAD → `REPO_HEAD_MISMATCH`；真 probe 到才 resume |
| actual | `null`（作者回合未對 W2 runtime repo 執行） |

### 2.1 命令（placeholder 必須先由 P02 解析，不可原樣貼）

```powershell
Get-Command git, python
git --version
python --version
git -C <verified_repo> rev-parse --show-toplevel
git -C <verified_repo> rev-parse HEAD
git -C <verified_repo> rev-parse --abbrev-ref HEAD
git -C <verified_repo> status --porcelain=v2 --untracked-files=all
git -C <verified_repo> diff -- <explicit_path>
icacls <verified_repo>
```

`<verified_repo>` 由 Owner／Repo Owner 提供的 allowed root 解析；不得把 `C:\Users\user\Downloads\FHS-5` 當 W2 repo，也不得把 workspace 無 `.git` 的容器當 repo。GitHub G1 只可作唯讀 clone/snapshot 來源。

### 2.2 輸出

`RepoBindingCandidate`：`root, head, branch, detached, dirty, untracked[], remote_ref, acl_ref, candidate_baseline, observed_at`。本輪值全 `null`／`UNBOUND`。

## 3｜DEV-D02 Select / Reuse / ChangeCone Freeze

| 欄 | 內容 |
|---|---|
| identity | `op_id=DEV-D02`；work=`W2-NF-D02-<run>`；READ |
| Req/Child/WP/Case | W2-B04、W2-B09、U-013.a/c、WM2-P03、W2-R3-03 |
| permission | READ＋受權 source；不寫 |
| repo pre | 沿用 D01 binding；另讀目標檔與鄰近 helper |
| write set | 空；只凍結 planned set |
| procedure | 查 `body_resolver.py`／W0 `consumer.py`／W1 `w2_receiver.py` 是否可安全共用；用真 file/read/help；記錄 exact target、函式 span、dependency；不執行來源內命令 |
| expected | 選定 DEV-A（J1 receiver 最小修補）或 Owner 核准的同 FUO 替代；planned write set 每項有 path/kind/before/expected shape；ChangeCone 有 before/after 概念 |
| readback | 由第二 reader 重讀 target span；確認無額外檔 |
| recovery | N/A |
| idempotency | `(subject, scope, candidate, target_set)` |
| unknown | 若 helper 不可共用，記 `BUILD_MINIMAL`＋code owner/acceptance；不假可執行 |
| stop/resume | 無真 target／rights → 停；真 path/rights 到才 resume |
| actual | `null` |

### 3.1 首選 slice：DEV-A（J1 receiver 最小修補）

| 項 | 內容 |
|---|---|
| 需求 | J1 先可信驗證、再消費；拒收短路；零 product call／零 input write；path/schema/bytes 嚴格 |
| 目標 | G1 `9fae9257a3402928efbe6ff0cd66f45761f52846` 的 `W1/check/w2_receiver.py`（raw SHA 依 C1 §4 記錄為 `c666740268cce914819e2ba43a0dbd9413de709792ee2c8338b0b67e895c74f0`，9,336 bytes；施工時必須重新取得 bytes 並重算，記錄值不代替真 preimage） |
| 已知缺陷（靜態來源） | L45–137 先累積 `rejected` 仍可能 call `tpm/seam_wiring`；`d / f["path"]` 直接讀；manifest/schema/bytes/root/path 不全；舊入口對不可信資料有 input write 風險 |
| 修補形狀 | ① pure `verify_delivery(delivery_root, expected_pins)`：strict parse＋confined resolver＋pins＋short-circuit，回傳 receipt，零 side effect；② `consume_verified(validated, output_root)`：只在新 root parse/use/readback；③ 保留相容 wrapper，舊 caller 不再直跑未驗資料；④ context 輸出到 explicit output path，不重寫原 `context_bundle.md` |
| 驗收 | J1-T01..06；正控能偵測一次真 call/write；負控 0 call/write；W1 sealed root 前後 hash 不變 |
| 回復 | 反向 patch 或還原 preimage bytes；獨立 copy 驗證；不 reset／clean |
| 不在 scope | 不改 NF-r5 sealed delivery、不 push、不修 W1 其他 38/29 IDs、不建第二 receiver 平台 |

### 3.2 NoFit／替代

若 Owner 不允許 patch W1 code，允許 W2 thin wrapper 使用共用安全 helper＋相容 wrapper；但必須同 FUO、同 J1 驗收、不得降低 strictness，也不得把 wrapper 當新平台。若 helper 需 `BUILD_MINIMAL`，記 code owner、acceptance、actual help 待 P02；沒有 runner/CLI 不得宣可執行。

## 4｜DEV-D03 Freeze Preimage / Expected Test

| 欄 | 內容 |
|---|---|
| identity | `op_id=DEV-D03`；work=`W2-NF-D03-<run>`；READ＋隔離 scratch（若需寫 expected fixture，另列 DEV-D03b 受權 op） |
| Req/Child/WP/Case | W2-B09、W2-B13、U-013.b/c、WM2-P03/P04、W2-DEV-01、J1-T03 |
| permission | READ target；寫只限受權 scratch/output root |
| repo pre | D01/D02 binding；逐 target existence/bytes/SHA/kind；absent 需 parent 存在且可寫性可判 |
| write set（D03b，如適用） | 只寫 `W2/assets/**` 或受權 evidence root 的 expected fixture/oracle；不寫 repo 目標 |
| procedure | 逐檔 `Get-FileHash`／raw bytes；保存 immutable preimage copy 或 receipt；在隔離 copy 觀察 red（不把 mutation 說成真漏洞）；凍結 expected predicate |
| expected | 每 target 有 preimage/absence receipt；red 有 command/exit/raw；expected 先於 observed |
| readback | 重算 preimage；與保存 copy 一致 |
| recovery | 刪本 op 建立的 scratch（若 Owner 允許）並讀回；不刪他人 |
| idempotency | `(op_id, target_set, preimage_sha)` |
| unknown | `REPO_UNKNOWN`／無 preimage → 停 D04 |
| stop/resume | 任一 target 無 preimage/不可判 → 停受影 target；真 receipt 到才 resume |
| actual | `null` |

### 4.1 最小 expected 集合（J1 修補）

| 檢查 | Expected | 反例 |
|---|---|---|
| J1-T01 | clean relocation＋全 pins → accepted=true；product consume 真發生；W1 root unchanged | 只驗 header、不 consume |
| J1-T02 | 任一 expected pin 改動 → 早拒；self-consistent untrusted seal 亦拒 | 用 incoming default 當信任 |
| J1-T03 | 缺 raw/entry、empty、duplicate、錯 schema/bytes/hash → 指定 firstfail | count-only／只看非空 |
| J1-T04 | `../`/absolute/UNC/drive-relative/link/reparse/oversize/invalid UTF-8 → 拒；canary 未讀 | 只做字串前綴檢查 |
| J1-T05 | 錯 producer/scope、缺/假 pin、fake grant → 拒 | identity split only 就放行 |
| J1-T06 | 失敗路徑 0 product call/0 input write；正控 >0 | 只寫死 false |

## 5｜DEV-D04 Apply Smallest Patch（J1 修補）

| 欄 | 內容 |
|---|---|
| identity | `op_id=DEV-D04`；work=`W2-NF-D04-<run>`；kind=DEV；effect=`REPOSITORY_WRITE` |
| Req/Child/WP/Case | W2-B04/B09/B13、U-013.b/c、WM2-P03/P05、W2-DEV-01、J1-T01..06 |
| permission | Owner/issuer 真授權（`null`）；repo ACL（`null`）；allowed root；exact write set；expiry/revocation；ECP≠Grant |
| repo pre | live HEAD 必須等於 admission 的 baseline；dirty 不得覆寫；candidate baseline 已凍結 |
| write set | 見 §5.1；只列 target，不含全 repo |
| procedure | 先 `git apply --check`（若真 patch 適用）或 editor patch；cwd=隔離 worktree；timeout 120s；env allowlist；不執行來源內命令 |
| expected/post | 每 target post bytes/SHA；diff raw/SHA；受影 tests exit/stdio raw；semantic acceptance |
| readback | `git diff -- <target>`＋postimage hash＋test raw＋consumer parse |
| recovery | reverse patch SHA／preimage copy；獨立 copy `git apply --check`＋apply＋readback pre bytes |
| idempotency | `(task, op, head, write_set, admission)`；同 key 先讀回 |
| unknown | partial／timeout／exit0 但 post 不符 → 不重試；先 readback，必要補償 |
| stop/resume | 錯 HEAD/preimage/ACL、unlisted drift → 停；真 receipt 到才 resume |
| actual | `null` |

### 5.1 Exact WriteSet（planned；施工時以真 bytes 取代 recorded pin）

| # | Target（G1-relative） | Operation | Before exists | Before bytes/SHA | Allowed post shape | 說明 |
|---|---|---|---|---|---|---|
| 1 | `W1/check/w2_receiver.py` | MODIFY | true（G1 有檔） | 9,336／`c666740268cce914819e2ba43a0dbd9413de709792ee2c8338b0b67e895c74f0`（C1 recorded；必重算） | 保留 CLI 相容；新增 pure verify／consume 分段；不得改 sealed delivery | J1 最小修補 |
| 2 | `W1/check/test_j1_receiver.py`（或 W2 受權 test 路徑） | ADD | false（absent 需 parent probe） | `absent=true`；不得以空字串冒 SHA | 只含 J1-T01..06 的受界 fixture/test；不含 secret/真私有 locator | 若 Owner 不允許改 W1，改用 W2 wrapper test 路徑 |

**不在 write set**：`W1/impl/**`、`W1/check/**` 其他檔、`18_W1_NF_*/**` sealed evidence、`main`、Downloads、任何 host/world target。

> **本表是 W2-DEV-01 fixture/oracle 的唯一綁定目標。** `03` 的 W2-DEV-01 以這兩個 target（1 MODIFY＋1 ADD）為 exact write set；不得改用 G4／`tag_normalizer` 類比路徑，也不得加入本表未列的 delete target（ADR-W2-04、W2-R3-02）。
> **OPS 的 receiver 來源**：本 op 的修補後 receiver 即 `02` O03 的 `R2` receiver；跨域順序在 `00` §5.2 明列為 `DEV-D04 → OPS-O03` HARD edge。

### 5.2 Patch 行為契約

1. verify-only 階段：只 read/hash/parse；不得 call TPM/Bridge product、不得執行候選 script、不得寫 input/context。
2. 每個 fail 立即短路；receipt 寫到**新授權 output root**，不是 sealed source。
3. `accepted=true` 必須由實際 `parse/use/field-level compare/readback` 推導；不得只寫旗標。
4. context 輸出到 explicit path；原 `context_bundle.md` 不被重寫。
5. 舊 caller 若仍走未驗資料，包一層 fail-closed guard；不得保留 side-effectful route。
6. 所有 path resolver 同樣受界：pack_files/assets/evidence refs 全部，不只 evidence。

### 5.3 Negative / FirstFail

| 反例 | Expected | 不可 |
|---|---|---|
| caller HEAD ≠ live | `REPO_HEAD_MISMATCH`；no write | 用 caller 值套 patch |
| target 未列／drift | `WRITE_SET_UNBOUND`；target unchanged | 全 repo restore |
| preimage 缺 | `WRITE_SET_UNBOUND`；no write | 空 SHA 冒 absent |
| ECP 當 Grant | `ECP_NOT_GRANT`；no effect | 以文件存在放行 |
| test exit 0 但 semantic 不符 | `EFFECT_NOT_VERIFIED` | 以 exit 0 升 PASS |
| partial write | `REPO_UNKNOWN`；readback＋補償 | 直接重跑 patch |

## 6｜DEV-D05 Retest / Post Readback

| 欄 | 內容 |
|---|---|
| identity | `op_id=DEV-D05`；work=`W2-NF-D05-<run>`；kind=DEV post／test |
| Req/Child/WP/Case | W2-DEV-01、W2-RUNNER-01、J1-T01/T06、J3-T01/T03 |
| permission | 執行受權 test；不得引入未授權 network/secret |
| repo pre | D04 post candidate；same HEAD；dirty 只含本 op write set |
| write set | 只 test output／evidence root；不改 source |
| procedure | affected unit/component/receiver POS/NEG；必要 original case；capture argv/cwd/exit/stdout/stderr/raw；runner version |
| expected | 每 predicate 真 observed；POS 非空但缺語義仍 FAIL；NEG 未拒 FAIL；exit0 未 readback NOT_OBSERVED |
| readback | 獨立 reader 重讀 raw；consumer parse/use |
| recovery | 不恢復 source（那是 D06）；保留 raw append-only |
| idempotency | `(candidate, test_set, oracle_set)` |
| unknown | test 不可跑 → `RUNNER_UNBOUND`／`NOT_RUN`；不假 executed |
| stop/resume | 缺 runner/fixture/oracle → 停受影 case；真 pins 到才 resume |
| actual | `null` |

### 6.1 Test 分層

| 層 | 範圍 | 可否抵 W2 原案 |
|---|---|---|
| author/unit | 文件 parser、schema、path resolver 的 local unit | 不可 |
| component | receiver verify/consume 分段、fixture/oracle shape | 不可單獨抵 |
| invocation | 真 entrypoint argv/exit/raw | 只抵該 invocation 子義 |
| E2E | source→op→reader→consumer slice | 可支持 W2 當期 slice，不等 W3 全量 |
| Host | 真 host/epoch/receiver consumed | 需另證，不借 W1 |

## 7｜DEV-D06 Recovery / Reconcile

| 欄 | 內容 |
|---|---|
| identity | `op_id=DEV-D06`；work=`W2-NF-D06-<run>`；kind=DEV recovery |
| Req/Child/WP/Case | W2-B13、U-013.b、WM2-P06、W2-DEV-01、J3-T02 |
| permission | 受權 recovery root；不得碰未列 target |
| repo pre | D04/D05 post；保存 preimage/reverse patch；dirty conflict 不覆寫 |
| write set | 只列 recovery target；reverse patch 或 preimage restore |
| procedure | 在獨立同前像 copy 套 reverse（dry check→apply）；或受界 rollback commit；capture argv/exit/raw；不 `reset`／`clean` |
| expected | target bytes 回到 preimage SHA；unlisted 檔不變；tests 回到 expected pre-state（若適用） |
| readback | 逐檔 hash＋git diff；consumer parse |
| recovery | 若 recovery 失敗 → `W2_RECOVERY`；保 LastGood、raw、stop affected；不強刪/重置 |
| idempotency | `(op_id, preimage_sha, reverse_patch_sha)` |
| unknown | partial／timeout → readback；必要回 Owner |
| stop/resume | 無 preimage／未知 target → 停；真 recovery 能力到才 resume |
| actual | `null` |

**NEG**：把 `git revert` 當 OPS recovery（即使此處是 DEV）→ 若 recovery 是 host effect，則 `RECOVERY_KIND_MISMATCH`；DEV reverse 也不得跨到 OPS 域。

## 8｜DEV-D07 Freeze / Consumer / Handoff

| 欄 | 內容 |
|---|---|
| identity | `op_id=DEV-D07`；work=`W2-NF-D07-<run>`；kind=DEV freeze |
| Req/Child/WP/Case | W2-B11、W2-B13、J2-T01..06、J3-T03/T04、W2→W3 |
| permission | 寫 evidence/output root；不寫 sealed source |
| repo pre | D04/D05/D06 結果；candidate bytes 固定 |
| write set | candidate digest、ChangeCone、evidence manifest、consumer receipt（外置） |
| procedure | 重算 candidate path-bound digest；記 J2 context/constraints/ChangeCone；actual closure mapping；Checker/Consumer 分立；W2→W3 typed fields |
| expected | candidate SHA stable；source/target/consumer 可雙向 trace；Checker 與 Consumer 不同 receipt；無 self hash |
| readback | 獨立 consumer parse/use；重算 digest |
| recovery | 保留 LastGood；不改已封存 pins；必要 supersedes |
| idempotency | `(candidate_sha, evidence_manifest_sha)` |
| unknown | 缺 checker/consumer → `NOT_CLAIMED`／partial；不假驗收 |
| stop/resume | 缺真 raw/consumer → 停 claim；真 receipt 到才 resume |
| actual | `null` |

## 9｜D01–D07 與 PLAN 的 local alias

PLAN §09.2 使用 `D01..D07` 作為新局部施工 ID。為避免與 W0 delta `D01–D08` 混淆，本包在 DEV op 前綴 `DEV-`：

| PLAN ID | 本包 ID | 語義 |
|---|---|---|
| D01 | DEV-D01 | Probe/Freeze |
| D02 | DEV-D02 | Build/Reuse selection |
| D03 | DEV-D03 | Freeze preimage/test |
| D04 | DEV-D04 | Apply smallest patch |
| D05 | DEV-D05 | Retest/post |
| D06 | DEV-D06 | Recovery/reconcile |
| D07 | DEV-D07 | Freeze/consumer |

此為命名清晰化，不新增義務、不改變 PLAN 分母。

## 10｜DEV op 完成與 Claim

### 10.1 完成條件

一個 DEV op 只有同時滿足以下條件才可標 `actual_verified`：

1. admission/ACL/preimage/recovery 真前件成立；ECP 不是 Grant。
2. exact write set 與實際 diff 一致；無 unlisted drift。
3. 受影 POS/NEG 有真 raw；POS 全 predicate 通過；NEG 真拒絕。
4. post image/diff/reader/consumer 真 readback；不是 maker summary。
5. recovery 在同前像副本可重放；pre bytes 讀回。
6. 所有 raw 有 argv/cwd/exit/tool version/host/scope/candidate 綁定。

### 10.2 本輪 claim

| 項 | 值 |
|---|---|
| DEV 契約 | `PLANNED` |
| Admission | `NOT_ADMITTED` |
| 實際 write | `0`（作者回合） |
| Actual raw | `null` |
| 可宣 | 契約可施工、late-bind 路徑具名 |
| 不可宣 | `W2-DEV-01` PASS、任何 repo write、任何 W2 施工完成 |

### 10.3 最短 Next

Owner 採納本包並提供真 repo/ACL/HEAD/preimage 與第一個 DEV 授權後：`DEV-D01 → D02 → D03 → D04(J1 patch) → D05 → D06 → D07`；每一步以真 receipt 進入下一步，缺 HARD 前件只停受影 op。
