# 02_W2_OPS_ECP｜W2 OPS 受界可逆效果契約

**artifact_id**：`FHS5-PLP/W2/PACK-NF-20261126-r3`
**subject_id**：`FHS-5_PLP/W2/CONTROL_PACK`
**scope**：`W2-NF-01`
**candidate**：`W2-NF-r3-CODEX-PRIMARY`
**kind**：`OPS ECP`（與 `01` DEV ECP 分域）
**狀態**：`PLANNED / NOT_ADMITTED`
**claim ceiling**：本檔是操作契約，不是 Grant、不是已執行結果

> OPS 是獨立的 host effect，不是 DEV 的附屬測試。每個 op 的 HostID／principal／policy epoch／receiver／pre-state／WorldRaw 在本輪一律 `null`；由 `00` §7.2 的 Host/OS/World Reader 在實際環境取得。沒有真 Host、receiver、preimage 或 host-specific recovery 時，只能寫契約，不得宣 `OPS` 完成。

## 0｜OPS 域邊界

### 0.1 適用與不適用

| 項 | OPS 域 | 不屬於 OPS |
|---|---|---|
| 身分 | HostID／OS principal／policy epoch／receiver ABI／output root／target kind | RepoRoot／HEAD／DEV write set（除非同 op 明確含 DEV，仍分欄） |
| 主要 effect | host state、受權 output、process/config 的原子可逆效果 | 只讀摘要、只列檔名、`git diff` |
| 回復 | host-specific compensation／restore／delete-created-only | `git revert`、`git reset`、全 repo rollback |
| 讀回 | 同 Host/Epoch 的 WorldRaw、receiver receipt、consumer parse/use | CLI stdout、exit 0、maker summary |
| 授權 | Owner/issuer 的 OPS scope＋Host/OS ACL＋receiver＋target＋expiry | 以 DEV scope、本機帳號或 W0/W1 舊授權自動取得 |

### 0.2 禁止事項

1. 不以 `git revert` 或任何 DEV reverse 作 OPS recovery。
2. 不以 `exit 0`、`CLI 0`、空 stdout、非空 dict 當世界已達。
3. 不把 W1 的 Host ledger／session／principal 帶入 W2。
4. 不在無 pre-state、無 receiver、無 host-specific recovery 時覆寫 target。
5. 不為求綠改 oracle、改 policy、提權、繞 sandbox／ACL。
6. 不在正式系統做破壞性故障注入；controlled fixture 只在專屬可逆 scratch。
7. 不把 Publisher／Release 當一般 OPS 前件；也不在無 Owner 發布授權時 push／deploy。
8. 未知 effect 不默認 READ；未取得真 host preimage 不覆寫；未取得真 principal/epoch 不執行 OPS。

### 0.3 Principal 分離

| 維度 | DEV | OPS |
|---|---|---|
| 身分 | RepoRoot／HEAD／ACL／WriteSet | HostID／OS Principal／PolicyEpoch／Receiver |
| 主要風險 | 污染工作樹、破壞 preimage | 影響 live Host、無法補償 |
| 回復 | reverse patch／rollback commit | host-specific recovery／compensate |
| 讀回 | git diff／test raw／consumer | WorldRaw／Original Receiver |
| 本輪 | `NOT_ADMITTED` | `NOT_ADMITTED` |

同一 OS 帳號可依法兼任不同責任，但每一域的 ACL、policy、receiver、preimage 必須分別核；不得虛造「兩個帳號」來假裝分離，也不得用 DEV ACL 代替 Host policy。

## 1｜每個 OPS op 的共同契約

| 區塊 | 必要欄 | 取得／驗證 | 拒收例 |
|---|---|---|---|
| identity | project/subject/scope/wave/batch/work/op_id、kind=OPS、candidate、pins、Req/Child/WP/Case | 同版 00/05 | W1 identity 當 W2；op id 重用 |
| authority | Owner/issuer decision、scope、allowed output root、target、expiry/revocation、Host/OS ACL、receiver ABI、原域 applicable ref | Owner＋Host/OS probe | `permission=true`、DEV scope、過期、越 target |
| host pre | host_id/session/OS/version、principal/ACL、policy/epoch、receiver、target path/kind/existence/bytes/hash、process state（如適用）、world reader、lastgood | 真 Host Reader／WorldReader | 無 epoch 造值、借 W1 Host、無 preimage 覆寫 |
| actual op | exact argv/cwd/env allowlist/timeout、receiver input/output contract、atomic temp→replace 或原生受權 effect、必要 process capture | actual help/entry；真 receiver | 猜 CLI、無 timeout、network/deploy/secret 未授權 |
| post/readback | receiver receipt、WorldRaw pre/post bytes/digest、semantic expected checks、same host/epoch/scope/subject、consumer parse/use | 獨立 reader／consumer | exit 0 當世界、只 list/hash |
| compensation | host-specific restore/undo/delete-created-only；pre absent 只刪本 op 創建且 hash/ownership match；不跟隨 link；recovery argv/digest；pre-state readback | 另存 evidence root | `git revert`、強刪、刪他人 |
| unknown | timeout/partial/exit0 mismatch/policy changed → readback by original/native reader；proven outcome 才 decide；stop/reason/lastgood/next/resume | WorldReader/reconcile | 盲重試、retry 代 compensation |
| idempotency | host＋op＋epoch＋work order＋preimage 的 stable key；同 key 先讀回 | 本地 ledger | 無 key 重放 |
| actual | 本輪 `null` | 真跑才填 | 預填 observed |

## 2｜O01 Host / Receiver Probe

| 欄 | 內容 |
|---|---|
| identity | `op_id=OPS-O01`；work=`W2-NF-O01-<run>`；effect=`HOST_READ`（非 effect） |
| Req/Child/WP/Case | W2-B03、W2-NF-C、U-014.a/b/c、WM2-P02、W2-DEV-02 對照 |
| authority | Host READ scope；Owner ref＝`null`；Host ACL＝`null` |
| host pre | 無（只 probe）；不得改 state |
| target | 無 write |
| procedure | 真 Host/session/OS/version/principal/policy/receiver/entrypoint/help probe；見 §2.1 |
| expected | host_id/principal/epoch/receiver 各可取得或明示 `UNBOUND`；entrypoint 可用；版本/argv 可核 |
| readback | 同 probe 重讀；值一致 |
| compensation | N/A；刪本 op 暫存 |
| unknown | `HOST_UNKNOWN` → 停 OPS |
| stop/resume | 無真 Host／receiver → `W2_HOST_BIND`；真值到才 resume |
| actual | `null` |

### 2.1 Probe 命令（placeholder 須先解析）

```powershell
Get-Command codex, python, git
codex --version
codex --help
python --version
whoami
$env:COMPUTERNAME
Get-ExecutionPolicy -Scope Process
icacls <allowed_output_root>
```

不得把作者主機的 `CodexSandboxUsers`、`C:\Users\user` 或 W1 session 當 W2 Host/principal。若真實 Host 是 container/cloud/其他 OS，必須改用該 Host 的 reader/entrypoint；本契約的 Windows 命令只是一種可取得路徑，不是 universal。

### 2.2 輸出

`HostBindingCandidate`：`host_id_ref, session_ref, os, version, principal_ref, acl_ref, policy_epoch, receiver_abi, entrypoint, observed_at`。本輪全 `null`。

## 3｜O02 Exact Target / Host Preimage / Authority

| 欄 | 內容 |
|---|---|
| identity | `op_id=OPS-O02`；work=`W2-NF-O02-<run>`；pre-state |
| Req/Child/WP/Case | W2-B03/B08/B09/NF-C、U-014.a/b/c、W2-AUTH-01、W2-OPS-01 |
| authority | OPS scope＋Host/OS ACL＋allowed output root＋target；Owner ref＝`null` |
| host pre | O01 binding；逐 target existence/kind/bytes/SHA；absent 需 parent probe；output root 可寫性 |
| write set | 空（只 freeze）；不得先寫再驗 |
| procedure | target raw hash／existence／ownership；WorldReader pre snapshot；lastgood；receiver schema/version；admission 對位 |
| expected | exact target set、preimage/absence receipt、WorldRaw pre、receiver contract、admission/scope/target 一致 |
| readback | 第二 reader 重讀 preimage/WorldRaw |
| compensation | N/A |
| unknown | `HOST_UNKNOWN`／`WORLD_UNKNOWN` → 停 O03 |
| stop/resume | 無 pre-state／越 target／principal mismatch → 停；真 receipt 到才 resume |
| actual | `null` |

### 3.1 Admission 檢查（不是 Grant 生成）

| 檢查 | Expected | 反例 |
|---|---|---|
| Owner/issuer ref | 同 subject/scope、未過期、未撤銷 | `permission=true`、作者 ECP |
| scope/target | exact target 在 allowed root 內 | 超 scope、symlink 逃逸 |
| principal/epoch | 同 Host/OS domain | DEV principal、W1 epoch |
| preimage/absence | 真 receipt | 空 SHA、舊 bytes |
| receiver | 真 ABI/schema/version | 無 receiver 或猜 schema |

## 4｜O03 Actual Receipt-Producing Work（OPS-A）

| 欄 | 內容 |
|---|---|
| identity | `op_id=OPS-O03`；work=`W2-NF-O03-<run>`；kind=OPS；effect=`HOST_EFFECT`（受權原子 output/receiver effect） |
| Req/Child/WP/Case | W2-CODEX-02、W2-B03/B08/B09/B13/NF-B/NF-C、U-014、WM2-P05、W2-OPS-01、N05/N06 |
| authority | O02 通過的 Owner 授權、Host/OS ACL、allowed output root、exact target、receiver；`null` 則不得執行 |
| host pre | O02 preimage/WorldRaw/lastgood；output root 可寫；無他人檔案衝突 |
| target/write set | 只列 allowed output root 內的當期 W2 工作產物/receipt；不得刪歷史交付；若 pre absent，只建立本 op 新檔 |
| procedure | ① 建 unique run dir（含 op/epoch/time/random）；② 以修正後 receiver 或 Native direct consumer 產生當期 W2 binding/effect receipt/material；③ atomic `temp→replace`；④ capture argv/cwd/exit/stdout/stderr/tool version；⑤ 立即 post readback |
| expected | 真 target bytes/absence post；receiver receipt 可 parse；semantic fields 與 expected 一致；consumer 真 use；same Host/Epoch |
| readback | 不同程序讀 receiver receipt／WorldRaw；重算 SHA；consumer parse/use |
| compensation | 見 O05；host-specific restore 或 delete-created-only；不 `git revert` |
| idempotency | `(host_id, op, epoch, work_order, preimage)`；同 key 先讀回，不重派 |
| unknown | timeout/partial/exit0-wrong-post → O06；不得直接重跑 |
| stop/resume | 無授權／receiver／preimage／recovery → 停；真 receipt 到才 resume |
| actual | `null` |

### 4.1 OPS-A 最小合法 slice

1. 在 Owner 授權的**隔離 output root**（不是 Downloads、不是 W1 sealed root）建立唯一 run dir。
2. 用 **`R2` receiver**（＝ `01` DEV-D04 產出的已修正 receiver；若 Owner 不允許改 W1，則為 `01` D02 選定並受權建成的 W2 thin wrapper —— 兩者都是受權 DEV op 的產物，不在此另造）對當期 W2 六檔/pins 做真 parse/use/readback，產出：
   - `w2_binding_receipt.json`（scope/host/epoch/pins/parsed summary）；
   - `w2_effect_material/`（必要的工作資料，如 source→Req→ECP→Case index）；
   - `world_pre.json`／`world_post.json`（target hashes/absence/consumer readback）。
3. 由**不同程序**讀回 receipt/material，重算 SHA，確認 semantic。
4. 在另一受權 evidence root 保存 raw。**O03 不自行補償**：移除／還原只由 O05 執行；O04 必須在 O05 之前讀到 post state，否則無效果可驗。
5. 若只做 READ、不產生受保護世界狀態，不得算 OPS-A；必須有真 pre/post/compensation。

**Why this is OPS, not DEV**：它在受權 Host/output 上改變檔案世界狀態，需 host pre/post、receiver、compensation 與 WorldReader；不是 repo patch。

### 4.2 輸出 receipt 最小欄

`run_id, subject/scope, project/wave/batch/work/op, candidate_sha, source_manifest_sha256, pack_sha, host_id, principal_ref, policy_epoch/epoch_state, receiver_id/version, argv, cwd, timeout, exit, stdout_sha256, stderr_sha256, pre_world_sha256, post_world_sha256, receiver_receipt_sha256, semantic_expected, observed, verdict, first_fail, raw_ref, compensation_ref, consumer_id, consumer_readback_sha256, **checker_id, checker_receipt_sha256**`。

`checker_id` 與 `consumer_id` 必須是**兩個 distinct receipt**（`00` §0.2、`03` §0.1.7）；Maker 不得自簽 independent，OPS 的 maker 收據不因帶了 consumer readback 就成為 Checker verdict。

## 5｜O04 Compare WorldRaw / Semantic / Consumed

| 欄 | 內容 |
|---|---|
| identity | `op_id=OPS-O04`；work=`W2-NF-O04-<run>`；post compare |
| Req/Child/WP/Case | W2-CODEX-02/04、W2-OPS-01、N04/N06、J3-T01 |
| authority | READ evidence；不改 target |
| host pre | O03 post；same Host/Epoch/scope |
| procedure | 重算 pre/post WorldRaw；比 expected predicate；consumer parse/use；確認 `consumed=true` 由實際 parse 推導 |
| expected | post 世界符合 expected；consumer 真讀；不是 exit0／非空 dict |
| readback | 第二 reader 重算；raw locator 可移植 |
| compensation | 不在此 op 執行；失敗交 O05/O06 |
| unknown | exit0 但 post 不符 → `EFFECT_NOT_VERIFIED`；世界不可知 → `WORLD_UNKNOWN` |
| stop/resume | 語義不符 → 停 claim；必要 rollback/compensate；真 reader 到才 resume |
| actual | `null` |

### 5.1 判定表

| 狀況 | Verdict | 動作 |
|---|---|---|
| exit 0＋post expected＋consumer consumed | `VERIFIED` | 可進 O05（若需 restore）／P06 |
| exit 0＋post 不符 | `EFFECT_NOT_VERIFIED` | 不升 PASS；補償／最小修補 |
| exit≠0＋post 已達 | `VERIFIED_WITH_EXIT_ANOMALY` | 讀回確認，不重跑 |
| exit≠0＋post 未達 | `FAILED_PRE` | 可依法一次 retry 或 stop |
| partial | `PARTIAL` | 限定補償或 stop |
| 世界不可知 | `UNKNOWN` | O06 readback/reconcile |

## 6｜O05 Restore / Compensate / Verify Pre-State

| 欄 | 內容 |
|---|---|
| identity | `op_id=OPS-O05`；work=`W2-NF-O05-<run>`；compensation |
| Req/Child/WP/Case | W2-B13、U-014.d、WM2-P06、W2-OPS-01/02、J3-T02 |
| authority | 受權 recovery root；只碰本 op target |
| host pre | O03/O04 post；preimage/absence；ownership/hash 可核；他人檔案不碰 |
| write set | host-specific restore／undo／delete-created-only；不跟隨 link |
| procedure | ① 讀 pre-state；② 若 pre 存在，restore 原 bytes/ownership（合法且可逆）；③ 若 pre absent，只刪本 op 創建且 hash/ownership match 的 target；④ capture argv/exit/raw；⑤ 讀回 pre-state |
| expected | target 回到 preimage/absence；unrelated 檔不變；WorldRaw 回到 pre；consumer 讀回 |
| readback | 同 Host/Epoch WorldReader；逐檔 hash；ownership |
| compensation | 若補償失敗 → `W2_RECOVERY`；保 LastGood/raw；回 Owner，不強刪 |
| unknown | 無法判定 ownership/hash → 停；不刪 |
| stop/resume | 無 preimage／未知 target → 停；真 recovery 能力到才 resume |
| actual | `null` |

### 6.1 `RECOVERY_KIND_MISMATCH`

`git revert`、`git reset`、DEV reverse、全 repo rollback 都不是 OPS compensation。若把它們送進 OPS recovery，必須早拒、zero host effect、記 `RECOVERY_KIND_MISMATCH`；不得先用它們改世界再說「已恢復」。

## 7｜O06 UNKNOWN / Reconcile / OFF / Clean Receive

| 欄 | 內容 |
|---|---|
| identity | `op_id=OPS-O06`；work=`W2-NF-O06-<run>`；reconcile |
| Req/Child/WP/Case | W2-CODEX-04、W2-B10/B13、N06/N10/N11、J3-T02/T05 |
| authority | READ/reconcile；effect 只在授權且 idempotent 時 |
| host pre | O03–O05 raw；lastgood；policy epoch |
| procedure | ① 以原/native reader 重讀世界；② 分類 timeout-before／timeout-after／partial／exit0-wrong-post；③ 確證 post 已達→驗證；仍 pre→必要一次 retry；partial→補償/stop；④ OFF/clean receive 用隔離 root＋正控 |
| expected | 四類 observed 分帳；不盲重試；OFF 雙方真成功＋正控；clean receive 早拒錯 pin |
| readback | 第二 reader；raw/exit/argv |
| compensation | 依分類；失敗回 Owner |
| unknown | 不得以 retry 代替 reconcile；`UNKNOWN_RETRY_DENIED` |
| stop/resume | 世界不可知 → 停受影 op；真 reader/policy 到才 resume |
| actual | `null` |

### 7.1 四類 controlled fixture（隔離、可逆、不得碰正式系統）

| Fixture | 注入 | 必要 observed | 允許決策 |
|---|---|---|---|
| F-TO-BEFORE | 寫入前 timeout | pre 世界不變；無 partial | 可一次有理由 retry（若權限有效/idempotent） |
| F-TO-AFTER | 寫入後失去 response | post 已達但無 receipt | 先 readback；確證後驗證，不重複 |
| F-PARTIAL | 部分輸出 | partial target set；hash 可核 | 限定補償或 stop；不得重跑全量 |
| F-EXIT0-WRONG | exit 0 但 post 不符 | exit/raw/post 三者不一致 | `EFFECT_NOT_VERIFIED`；不升 PASS |

每一 fixture 必須有 runner 造成的真狀態、raw、readback；只傳 enum 不算。F-PARTIAL 可與 `W2-OPS-01` 的 scratch 子例共享，但每個 child 要獨立 observed。

### 7.2 OFF / clean receive

1. **同一 W2 合法任務**：ON 用 applicable TPM/Guide/Bridge；OFF Native direct 不 import optional products/Legacy；隔離 ON/OFF roots。
2. **PASS 合取**：雙方 exit/semantic 真成功；同 stable full applicable projection；blocker/positive control 成立；forbidden imports/calls=0；同 preimage/recovery/無越界。
3. **空 env flag 不算**；需真 import/call block／absent probe＋positive control；negative double-failure。
4. **Clean receive**：乾淨隔離 snapshot、exact pins、case IDs/semantic/raw；錯 pin 早拒＋真 material consume；不再讀原 workspace。

## 8｜Late-bind 與 stop/resume

| 欄 | Producer | 取得 | Consumer | 必要時點 | FirstFail | Resume |
|---|---|---|---|---|---|---|
| host_id | Host Reader | 真 Host/session probe | O01/O02 | OPS pre | `W2_HOST_BIND` | 同 Host readback |
| principal | OS Reader | `whoami`/token/ACL | O02 | OPS pre | `PRINCIPAL_DOMAIN_MISMATCH` | 真 principal |
| policy epoch／`epoch_state` | Host/Policy Reader | policy snapshot/version；host 未宣告時記 `epoch_state=NOT_DECLARED_BY_HOST` ＋ probe 原始輸出（事實記錄，非造值） | O02 | OPS pre | `W2_HOST_BIND`（僅 probe 不可執行時） | 真 epoch 或合法 `NOT_DECLARED_BY_HOST` |
| receiver | Host/Receiver Owner | entrypoint/help/schema | O03 | effect pre | `CONSUMER_UNVERIFIED` | 真 receiver |
| target/preimage | WorldReader | 逐 target existence/bytes/SHA | O02 | effect pre | `WRITE_SET_UNBOUND` | 真 preimage |
| output root | Owner/Host Owner | allowed root＋ACL | O03 | effect pre | `NOT_ADMITTED` | 真授權 |
| recovery | Host Owner | host-specific argv/dry check | O05 | 可恢復能力 pre | `W2_RECOVERY` | 真 recovery |
| WorldRaw | WorldReader | same Host/Epoch raw | O04/O05 | post | `EFFECT_NOT_VERIFIED` | 真 reader |
| admission | Owner/issuer | decision/work order/ACL | O02 | effect pre | `W2_ADMISSION` | 同 scope receipt |

**Stop scope**：缺 Host/principal/epoch → 停 OPS，不阻 DEV 設計；缺 receiver/recovery → 停受影 effect，不阻其他合法 op；缺 WorldReader → 停 claim，不把 exit 0 當結果。

## 9｜OPS op 完成與 Claim

### 9.1 完成條件

1. O02 admission/ACL/principal/epoch/target/preimage 真成立。
2. O03 真改變受權世界狀態，atomic，有 argv/exit/raw。
3. O04 post WorldRaw 與 semantics 真 observed；consumer 真 consume。
4. O05 host-specific compensation 真執行、pre-state 讀回；不是 `git revert`。
5. O06 若有 UNKNOWN，四類有真 readback；不盲重試。
6. 所有 raw 綁 subject/scope/host/epoch/candidate/receiver。

### 9.2 本輪 claim

| 項 | 值 |
|---|---|
| OPS 契約 | `PLANNED` |
| Host/Receiver | `null`／`W2_HOST_BIND` |
| Admission | `NOT_ADMITTED` |
| 實際 host effect | `0`（作者回合） |
| Actual raw | `null` |
| 可宣 | 契約可施工、compensation/UNKNOWN 路徑具名 |
| 不可宣 | `W2-OPS-01` PASS、任何 host effect、任何 W2 施工完成 |

### 9.3 最短 Next

Owner 採納並提供真 Host/principal/epoch（或合法 `NOT_DECLARED_BY_HOST`）/receiver（`R2`）/output root/preimage/recovery 後：`O01 → O02 → O03(OPS-A) → O04 → O05 → O06`。順序是**單向**的：O03 只產出效果、**不補償**；O04 讀 post 並判定；O05 才移除／還原並讀回 pre-state；O06 只在 UNKNOWN 時接手。O03 必須是真 receipt-producing work，不是只讀摘要。
