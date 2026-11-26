# 02_W1_OPS_ECP｜W1 S1 受影主用包（OPS ECP）

**S1 pack**：`W1-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1-r2`  
**supersedes**：`FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1` / `W1-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W1/CONTROL_PACK/2026-11-25-nf-r2` / `W1-NF-r2-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`｜固定 commit `9fae9257a3402928efbe6ff0cd66f45761f52846`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 受影重構的完整正文；本輪已依 Owner 預授權升格為「主用＋受界可施工」（document primary）。S1 節只替換受影 clause；未受影段落、原 ID、原分母、原 fixture/oracle bytes 與歷史證據原樣保留（見文末「原版正文」）。衝突時以原上位原義＋S1 受影條款為準；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## S1-0｜S1 對 OPS ECP 的受影增量

原 29 個 OPS ECP ID（`OPS-APP-01`…`OPS-RESUME-01`）與 O1–O6 全保留；本節只加 Host 分帳與當期 admission。

### S1-0.1 Host 觀測的歷史與當期

| Host | 原版狀態 | S1 判定 |
|---|---|---|
| CODEX | `OBSERVED_LOCAL`（CLI 可執行）；W1 entry 未建 | 歷史；S2 需真 entry/invoke |
| GPT CHAT | `NOT_OBSERVED` | 不互抵；需真 manifest/consumer |
| GPT WORK | `NOT_OBSERVED` | 不互抵 |
| HERMES | `DEFERRED` | 三 child 分列；不阻 CODEX |

### S1-0.2 每 op admission

真 HostID／version／entry／loader manifest、principal／ACL、policy epoch、receiver ABI、pre/post world state、Owner scope。`Installed` 不因 `Selected` 推定；`ActualServed` 不因 exit 0 推定；`Consumed` 不因收到 bytes 推定。

### S1-0.3 安全與 recovery

| 項 | 要求 |
|---|---|
| 撤權 | Owner 撤權或 ACL 拒絕即停該 Host 該 stage；不得換 root／工具 |
| recovery | install/register/bind 必須有對應 uninstall/unregister/unbind 或 `REASONED_NA`；`git revert` 不適用 |
| UNKNOWN | 先 readback/reconcile；不得盲 retry；worker 未結束不解除隔離 |
| 跨 Host | CODEX／GPT CHAT／GPT WORK／HERMES 各自 raw；不得一格拉三格 |

### S1-0.4 不宣稱

`HOST_PASS=NO`、`CONSUMED=NOT_RUN`、`HERMES_COMPATIBILITY=NOT_CLAIMED`。

---

## 原版正文（血緣保留；S1 未明示者不變）

> **原版身份（superseded）**：以下為原版 `W1-NF-r2-CODEX-PRIMARY` 的 preamble 與正文，按原 bytes 保留。
>
> 其中所有 `PRIMARY`／`PASS`／`已完成`／`AUTHORIZED` 均屬原版歷史陳述，不適用於本候選；本候選效力只以上方 S1 header 與 S1 節為準。
>
> # FHS-5_PLP_W1_NATIVE_FIRST｜02 W1 OPS ECP（主用修補定案）
>
> **File ID**：`FHS5-PLP/W1/CONTROL_PACK/02_W1_OPS_ECP`
> **pack_version**：`W1-NF-r2-CODEX-PRIMARY`
> **project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`｜**scope**：`W1-NF-01`
> **wave_id**：`W1`｜**batch_id**：`W1-NF-01`｜**date**：2026-11-25（Asia/Taipei）
> **source_manifest_ref**：`05_W1_SOURCE_MANIFEST.json`（第六身份讀時衍生）
> **Effect（本檔）**：W1 最小本地 OPS 的 planned ECP；本輪不執行 Host 安裝／服務。
> **Authority**：Owner 已對 W1 同域受界可逆 OPS 預授權；每操作仍須當期 HostID／principal／policy／entry／ACL／receiver 核實。ECP≠Grant。
> **Claim ceiling**：`W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`；Host actual `NOT_RUN`。
>
> ---

## 1｜Host／Principal／Policy／Receiver（真 probe）

| 欄 | 實際值 | 證據／限制 |
|---|---|---|
| OS | Windows（本機） | Python 3.11.9／Git 2.53.0.windows.1 |
| 主 Host | CODEX CLI `codex-cli 0.164.0` | `codex --version`；僅 Selected，非 W1 plugin loaded |
| 第二 Host | 無正式 GPT CHAT/WORK/HERMES 掛載 | 各自 `NOT_OBSERVED`；不互抵 |
| Principal | 本機 sandbox 使用者（非原 Host principal） | 不 dump 帳號／環境；原域 principal `UNBOUND` |
| ACL | 來源根唯讀；原 `FHS-5_Workspace` 讀可、寫 DENIED；**W1 worktree `FHS-5_W1_NF_r2` 寫 OK**；交付根可寫 | 真寫入 probe；W1 DEV/invoke 已實際開始 |
| Policy／Epoch | `UNBOUND` | 無具名 policy service；不造 epoch；以實際 policy 檔案／sandbox 設定為可得替代，未得記 UNVERIFIED |
| Receiver ABI | `W1/impl/w1_nf_reader.py` 的 `inspect` JSON 已作 receiver candidate；獨立 consumer 尚未建 | `PARTIAL_LOCAL`；D4 補 |
| Output root | 本輪 `outputs/.../evidence`；產品階段由 Owner 指定隔離根 | 不寫全域 |
| 安裝狀態 | W1 plugin 未安裝；native CLI entry 已實跑 | 不強制 install；`REASONED_NA_NATIVE_ENTRY` 非 PASS |
| 網路 | 受限 | GitHub push／release `NOT_ADMITTED` |

**本輪 OPS 結論**：可做 read-only probe 與文件；真 Host activation／invoke／serve 不成立，因 W1 entry 未建且無原 Host ACL／principal。此為真缺口，不以 `install` 模板補造。

---

## 2｜29 個原 OPS ECP ID：逐原義 Native 承接

> 讀法同 01：原義取自舊 `04_OPS_ECP.md` 與 W1M §02.4B；每列保留 live Host 安全責任，不因 `PROFILE_ONLY`／`DEFER_HOST` 消失。`O#` 指 §3。

| ID | 原義 → Native 承接（operation／目標） | Pre（真前件） | Post／Readback | Recovery／NEG | 步 |
|---|---|---|---|---|---|
| `OPS-APP-01` | Applicability：判本 Host／階段是否真適用；非一律 N/A。ledger 記 host/stage/scope。 | Host probe | `applicability.json` | 全 N/A 掩真 effect → `HOST_PENDING` | O1 |
| `OPS-EFF-01` | Host effect tokens：明示 install/register/bind/invoke/serve/consume/restore；未知拒。 | manifest／Host policy | effect token＋來源 | 未知當 READ → `EFFECT_UNBOUND` | O1 |
| `OPS-PRE-01` | Precondition 1：真 HostID、version、entry、loader manifest、installed applicability。 | `codex --version`、entry probe | `host_probe.json` | 假 installed → `HOST_PENDING` | O1 |
| `OPS-PRE-02` | Precondition 2：真 principal／ACL／output root；不以 sandbox 身份冒原域。 | ACL probe | principal／acl／root 記錄 | 無權仍 invoke → `FALSE_AUTHORITY` | O1 |
| `OPS-PRE-03` | Precondition 3：當期 Owner grant；原域 typed receipt 另帳。 | grant ref | `authority.json` | 以 ECP 當 grant → `ECP_NOT_GRANT` | O1 |
| `OPS-PRE-04` | Precondition 4：真 policy／epoch 或可回取 policy identity；UNKNOWN 先 reconcile。 | policy 檔／設定 | `policy_ref` 或 `UNVERIFIED` | 造 epoch → `POLICY_EPOCH_FABRICATED` | O1 |
| `OPS-PRE-05` | Receiver ABI：描述 consumer 的 input／output／readback／scope echo；pre/post world raw 讀法。 | ABI 文件 | `receiver_abi.json` | 只 hash 無內容 → `CONSUMER_UNVERIFIED` | O1/O5 |
| `OPS-CON-01` | ChatGPT：各自真格位／manifest／installer／consumer，不與 CODEX 互抵；保留原 ChatGPT 血緣。 | 真 host 掛載 | `NOT_OBSERVED`／各自 raw | 以 CODEX 抵 ChatGPT → `HOST_ABI_DRIFT` | O1 |
| `OPS-CON-02` | Codex：真 native/plug-in entry、principal、receipt；W1 entry 未建則 `BUILD_MINIMAL`。 | CLI／entry help | Selected/Invoked raw（建後） | skill bytes 冒 Loaded → `HOST_PENDING` | O1–O5 |
| `OPS-CON-03` | Hermes：三 child Kanban／Delegation／Swarm 後置；不抵 CODEX。 | Hermes 掛載 | `DEFERRED`＋三 child | 一格拉三格 → `REQUIRED_CHILD_MISSING` | O1 |
| `OPS-OP-01` | Host operation 1：僅真需要且受權才 install/activate；已可用不強裝；記 installer/activation raw。 | Host policy／preimage | installer ref／pre/post | 靜默安裝 → `UNAUTHORIZED_INSTALL` | O2 |
| `OPS-OP-02` | Host operation 2：register/load，記 manifest／version／LoadedSHA；不假 plugin loaded。 | loader API | registration＋loaded_sha256 | 名稱相似認同 → `W1_PLUGIN_ALIAS` | O2 |
| `OPS-OP-03` | Host operation 3：bind subject/scope/identity/policy；binding 不創 Grant。 | scope／policy | binding record＋scope echo | 擴 scope → `SCOPE_DRIFT` | O2 |
| `OPS-OP-04` | Host operation 4：真 invocation argv／cwd／env／timeout／exit／stdout／stderr。 | entry／inputs | `invoke_raw.json`＋SHA | 錯 scope／timeout 盲重試 → `INVOCATION_UNVERIFIED` | O3 |
| `OPS-OP-05` | Host operation 5：actual served bytes、scope echo、served_at；語義錯不宣 served。 | invoke 完成 | `served_raw`＋served_sha256 | 以 exit 0 冒 served → `SERVED_UNVERIFIED` | O4 |
| `OPS-OP-06` | Host operation 6：獨立 consumer parse/use/readback；不同 consumer 與 maker 分立。 | served raw | `consumed.json`＋readback | 只 hash 不比內容 → `CONSUMER_UNVERIFIED` | O5 |
| `OPS-POST-01` | 7-stage row per host：每 Host 七階段各自證據或 `REASONED_NA_NATIVE_ENTRY`；不跳階。 | 每階段 raw | 21 格 ledger | 一階抵另一階 → `HOST_ABI_DRIFT` | O5 |
| `OPS-POST-02` | Evidence class only：`OBSERVED_LOCAL`／`HOST_RAW`／`CONSUMER_ACTUAL` 等不互推。 | 證據分類 | class＋locator | policy unit 冒 E2E → `EVIDENCE_LAUNDERING` | O5 |
| `OPS-POST-03` | Independent consumed：consumer 與 checker 不同責任；不以同一 raw 生成器自簽。 | 分立主體 | independent receipt | 作者自簽 → `FALSE_INDEPENDENT` | O5 |
| `OPS-POST-04` | Hermes 3 child rows：Kanban／Delegation／Swarm 各 observation／consumer／ExpectedRaw／NEG／owner。 | Hermes 環境 | 三列 | 合併 → `REQUIRED_CHILD_MISSING` | O5 |
| `OPS-POST-05` | No install/service raw：未安裝／未服務就明示，不以本地 probe 代。 | probe 結果 | `NOT_INSTALLED`／`NOT_OBSERVED` | 以容器 probe 冒 Host → `HOST_PENDING` | O5 |
| `OPS-RB-01` | Container probe：只證本機能力（Python／Git／CLI），不證服務。 | 版本命令 | `container_probe.txt` | 升格 Host → `HOST_PENDING` | O1 |
| `OPS-RB-02` | Host readback：真 host entry／served／consumer readback，不用作者 summary。 | host raw | readback json | 摘要冒 raw → `EVIDENCE_LAUNDERING` | O4–O5 |
| `OPS-REC-01` | Host recovery 1：install／activation 依原 Host uninstall／rollback；保 preimage。 | installer ref／preimage | post-restore readback | `git revert` 代 → `RECOVERY_KIND_MISMATCH` | O2/O6 |
| `OPS-REC-02` | Host recovery 2：registration／binding 回復；無效果則記 `REASONED_NA`。 | registration record | unregister／unbind raw | 留孤兒 binding → `RECOVERY_INCOMPLETE` | O6 |
| `OPS-REC-03` | Host recovery 3：service／process／config／output 復原與讀回。 | pre world | pre/post world SHA | 刪 log 代 → `EVIDENCE_LOSS` | O6 |
| `OPS-REC-04` | Host recovery 4：UNKNOWN／partial 先 reconcile，再同 grant compensation；不盲重試。 | 狀態讀回 | reconcile 記錄 | 盲重試 → `UNKNOWN_BLIND_RETRY` | O6 |
| `OPS-STOP-01` | Stop scope：只停受影 effect／Host／stage；其他合法工作繼續。 | 缺口定位 | stop ledger | 全域 HOLD → `OVERBLOCK` | O6 |
| `OPS-RESUME-01` | Typed resume predicate：同 subject/scope/host/policy 的真 receipt 或新 grant；不靠假 ACK。 | resume 證據 | resume record | `permit=true` 補位 → `FALSE_AUTHORITY` | O6 |

**合計 29／29**；原 21 格與 U-017／U-028 不減。

---

## 3｜O1–O6 操作

| 步 | Operation | 真 Input／Command（或發現路徑） | Post／Readback | Recovery |
|---|---|---|---|---|
| `O1` | Read/probe | `codex --version`、`python --version`、`git --version`、`Get-Command codex,openspec`；entry `--help`；ACL／principal／output root probe；H0 真接收 | `host_probe.json`（version/entry/acl/principal/policy/receiver）；不升格 installed | 無 effect；不 install |
| `O2` | Activate（條件適用） | 既有 entry 優先；真需 install/register/bind 時：installer/loader 真命令＋version＋rights＋Host 寫入範圍＋preimage＋Owner 授權 | installer／registration／binding raw＋LoadedSHA | uninstall／unregister／unload／restore；`git revert` 不算 |
| `O3` | Invoke | W1 entry（建後）argv／cwd／env／timeout；只讀或受權 output | `invoke_raw.json`：exit／stdout/stderr SHA／scope | 停受影；readback 後才重試 |
| `O4` | Serve | 真 served bytes、scope echo、source locator、structured errors | `served_raw`＋served_sha256＋served_at | host-specific restore |
| `O5` | Consume | 獨立 consumer parse/use 實際材料＋受界任務＋readback；第二不同包 | `consumed.json`＋action/readback；錯 pin 拒 | 刪本次 output；重讀 |
| `O6` | Restore/Unknown | 依原操作 compensation；pre/post world；UNAVAILABLE／UNKNOWN 保狀態 | 原 preimage／absent 讀回 | 不可恢復或越權即停；不 destructive reset |

---

## 4｜Host 矩陣、21 格與 child

| Host | Selected | Loaded | Installed | Bound | Invoked | ActualServed | Consumed |
|---|---|---|---|---|---|---|---|
| CODEX | `OBSERVED_LOCAL`（codex-cli 0.164.0） | `NOT_OBSERVED`（W1 未作 plugin loader 載入） | `REASONED_NA_NATIVE_ENTRY`（CLI 內建；非 PASS） | `OBSERVED_LOCAL`（worktree/scope） | `OBSERVED_LOCAL`（`w1_nf_reader.py inspect`） | `OBSERVED_LOCAL`（inspect JSON／context bytes） | `NOT_OBSERVED`（獨立 consumer 未建） |
| GPT CHAT | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` |
| GPT WORK | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` |
| HERMES | `DEFERRED` | `DEFERRED` | `DEFERRED` | `DEFERRED` | `DEFERRED` | `DEFERRED` | `DEFERRED` |

**U-017 九 child**（原名保留）：ChatGPT／Codex／Hermes × Loaded／Invoked／ActualServed。每 child 需 `observation／consumer／ExpectedRaw／NEG／owner`；本輪全 `NOT_OBSERVED`。

**U-028 三 child**（原名保留）：Hermes `Kanban`／`Delegation`／`Swarm`。三格各有 raw、consumer、ExpectedRaw、NEG、owner；不得以一格拉三格；本輪 `DEFERRED`。

**GPT CHAT/WORK**：各自真 plugin/host evidence；不得以 CODEX CLI 或本包文件代替。**HERMES Compatibility**：CODEX 主工程全波完成後另測，非 W1 建造前件。

---

## 5｜安全、停止與恢復

- `skill bytes` ≠ `Loaded`；`exit 0` ≠ `ActualServed`；`served` ≠ `Consumed`；`hash 相同` ≠ `consumer 實際使用`。
- 錯 principal／ACL／scope、未知 effect、無 output root、無 entry → 停受影 effect；其他合法 READ／DRAFT 繼續。
- 復原：以原 Host uninstall／rollback／service restore，記 before/after world SHA；`git revert` 不是 OPS 恢復。
- UNKNOWN：先真 readback／reconcile；已成效 no-op；未成效且同 grant、同 preimage 才補償或重試一次。
- Resume：同 subject/scope/host/policy 的真 typed receipt 或新 grant；不靠 `permit=true`、public commit、skill 可讀、作者 CLI exit 0。
- 本輪無 installer／service raw；CODEX 的 invoke/serve 只到 local reader，`Consumed` 仍是 `NOT_OBSERVED`；不以 local probe 升格為 independent。
