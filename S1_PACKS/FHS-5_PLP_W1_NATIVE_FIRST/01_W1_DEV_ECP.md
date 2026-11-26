# 01_W1_DEV_ECP｜W1 S1 受影主用包（DEV ECP）

**S1 pack**：`W1-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1-r2`  
**supersedes**：`FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1` / `W1-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W1/CONTROL_PACK/2026-11-25-nf-r2` / `W1-NF-r2-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`｜固定 commit `9fae9257a3402928efbe6ff0cd66f45761f52846`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 受影重構的完整正文；本輪已依 Owner 預授權升格為「主用＋受界可施工」（document primary）。S1 節只替換受影 clause；未受影段落、原 ID、原分母、原 fixture/oracle bytes 與歷史證據原樣保留（見文末「原版正文」）。衝突時以原上位原義＋S1 受影條款為準；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## S1-0｜S1 對 DEV ECP 的受影增量

原 38 個 DEV ECP ID（`DEV-APP-01`…`DEV-PERM-01`）逐項保留；本節只加當期 repo 事實與 S2 的精確入口。

### S1-0.1 本輪真 repo 觀測

| Probe | 實際 | 判定 |
|---|---|---|
| `git -C C:\Projects\Agent_Workspace\FHS-5_Workspace rev-parse` | exit 128／`Permission denied` | `REPO_CHDIR_DENIED`；不得宣 live root |
| `git --git-dir=...\.git rev-parse HEAD` | `c2d8084ba24dd8df3fa62259bba496f4fb9caa85` | 只讀 metadata |
| 固定 W1 pack commit `9fae9257…` | `cat-file -t` = `commit`；5 MD＋05＋26 assets 可 `git show` | 來源血緣成立 |
| 本地 W1 六檔 vs Git blob | 6/6 bytes 全等 | `GIT_EQ` |

`repo_root/HEAD/ACL/preimage` 仍 `UNBOUND`。S2 的 P03 必須在 Owner 授權、可 chdir 的隔離 worktree 重做 `DEV-PRE-01`，不得以 `C:\Projects\...` 的 metadata 冒充產品 root。

### S1-0.2 當期 write-set 邊界（S2）

| 類 | 允許 path（relative to authorized worktree） | 前置 |
|---|---|---|
| reader/ABI | `W1/impl/w1_nf_reader.py`、`W1/impl/body_resolver.py`、`W1/impl/bridge_nf.py` | 對應 preimage SHA 或 ABSENT |
| Guide | `W1/impl/guide_nf.py`＋render/negative tests | 四函式／九鍵 spec |
| Host/consumer | `W1/impl/host_facade.py`、`W1/impl/w1_consumer.py` | 真 host probe |
| tests | `W1/check/test_*.py` | frozen fixture/oracle |
| 禁止 | 原 W0/M/B/WM/W1M、舊 primary、`08_*`/`09_*` 歷史、任何 marker/ACL | 只讀 |

不得以全 repo glob 或 `git add -A` 代替 exact write-set；不得把 `git revert` 當 OPS restore。

### S1-0.3 正負例

| 類型 | 輸入 | 期望 |
|---|---|---|
| POS | 合法 root＋exact write-set＋preimage | patch、tests、post SHA、reverse 讀回 |
| NEG | 同名異 SHA／alias 推定 | `SOURCE_IDENTITY_HOLD` |
| NEG | write-set 外變更 | `WRITESET_VIOLATION` |
| NEG | 假 grant／`permit=true` | `FALSE_AUTHORITY`；0 write |
| NEG | heading-only／unknown drop | `ABI_LOSSY_CROSSWALK` |
| 正控 | spy 檢出一次合法 write | 正控 >0；負控 0 |

### S1-0.4 不宣稱

`DEV_EXECUTED=NO`、`EFFECT_VERIFIED=NO`；38 列是原義映射，不是當期已跑。

---

## 原版正文（血緣保留；S1 未明示者不變）

> **原版身份（superseded）**：以下為原版 `W1-NF-r2-CODEX-PRIMARY` 的 preamble 與正文，按原 bytes 保留。
>
> 其中所有 `PRIMARY`／`PASS`／`已完成`／`AUTHORIZED` 均屬原版歷史陳述，不適用於本候選；本候選效力只以上方 S1 header 與 S1 節為準。
>
> # FHS-5_PLP_W1_NATIVE_FIRST｜01 W1 DEV ECP（主用修補定案）
>
> **File ID**：`FHS5-PLP/W1/CONTROL_PACK/01_W1_DEV_ECP`
> **pack_version**：`W1-NF-r2-CODEX-PRIMARY`
> **project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`｜**scope**：`W1-NF-01`
> **wave_id**：`W1`｜**batch_id**：`W1-NF-01`｜**date**：2026-11-25（Asia/Taipei）
> **source_manifest_ref**：`05_W1_SOURCE_MANIFEST.json`（第六身份讀時衍生）
> **Effect（本檔）**：W1 產品 DEV 的 planned ECP；本輪文件階段不執行產品寫入。
> **Authority**：本輪 Owner 已對「合格定案＋W1 同域受界可逆 DEV／最小 OPS」預授權；**ECP 本身不是 Grant**，每一真操作仍須當期 live root／ACL／principal／policy／exact WriteSet 核實。
> **Claim ceiling**：`W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`；產品 actual `NOT_RUN`。
>
> ---

## 1｜RepoContext 與本機真 probe（2026-11-25）

| 欄 | 實際值 | 證據 |
|---|---|---|
| 來源根 | `C:\Users\user\Downloads\FHS-5`（遞迴唯讀） | 本輪大量實讀；寫入未授權 |
| 既有工程 repo | `C:\Projects\Agent_Workspace\FHS-5_Workspace`（原樹未改） | `.git` 存在 |
| W1 實作 worktree | `C:\Projects\Agent_Workspace\FHS-5_W1_NF_r2` | `git worktree add` 自 `c2d8084…` 建立 |
| repo branch | `codex/w1-nf-r2-20261125`（worktree）；原樹仍 `codex/b0-nf-20261125` | `git status --branch` 實讀 |
| repo HEAD | `c2d8084ba24dd8df3fa62259bba496f4fb9caa85` | 兩樹同 base；與 PLAN 基線 main 同 commit |
| remote origin | `https://github.com/shw097-team/FHS-5.git` | `.git/config` 實讀 |
| dirty／untracked | worktree 起始 clean；本輪新增 `W1/impl/w1_nf_reader.py`、`W1/check/test_w1_nf_reader.py`、evidence raw（未 commit 前為 untracked）；原樹未動 | 不假 clean |
| repo 寫入 ACL | worktree **WRITE_OK**（本輪使用 `require_escalated` 真寫入；使用者明示授權）；原樹仍唯讀 | 產品 DEV 已實際開始 |
| 本輪可寫根 | outputs ＋ `C:\Projects\Agent_Workspace\FHS-5_W1_NF_r2`（worktree） | 兩者均實際可寫 |
| Python | `3.11.9` | `python --version` |
| Git | `2.53.0.windows.1` | `git --version` |
| CODEX CLI | `codex-cli 0.164.0`（`codex.ps1`）；`codex exec --help` 可讀 | `codex --version`／`exec --help`；只證非互動入口存在，不證 W1 plugin loaded |
| OpenSpec | `2.0.0`（`openspec.ps1`） | `openspec --version`；只證 CLI 存在 |
| 網路／GitHub | `ls-remote`／push 成功；remote branch `codex/w1-nf-r2-20261125` = `8d250c6c9d88d4c6d3c53117f396d39ab7a4596d`；main 未動（`c2d8084…`） | token 經暫存 credential store 使用；未輸出 |

**結論**：W1 產品施工入口已建立並真跑第一個合法操作（`inspect`）；`W1_EXECUTION_READY=READY` 的 root／ACL／entry／input 條件已具。最終 13 案／獨立 consumer／Host served/consumed 仍未跑，故 `W1_NF_VALIDATED` 仍 `NOT_CLAIMED`。

---

## 2｜38 個原 DEV ECP ID：逐原義 Native 承接

> 讀法：`原義` 為舊 `03_DEV_ECP.md`／W1M §02.4B 的實質語義，不是標籤；`Native 承接` 是可直接施工的 operation；`Pre` 與 `Post` 為每操作最小證據。`D#` 指 §3 的建造步。任何列都不因 `PROFILE_ONLY` 而刪安全責任（D02）。

| ID | 原義 → Native 承接（operation／目標） | Pre（真前件） | Post／Readback | Recovery／NEG | 步 |
|---|---|---|---|---|---|
| `DEV-APP-01` | Applicability：分 author／pack／product 三域，判本操作是否 W1 產品 DEV。寫 `applicability` 入 D1 ledger：domain、effect、owner、scope。 | 真 root／scope／effect class | ledger 條目＋hash；與 05 authority 對讀 | 把 pack DRAFT 當 product DEV → `ECP_NOT_GRANT` | D1 |
| `DEV-EFF-01` | Effect tokens：以 `READ/DRAFT/DEV/OPS/USER/RELEASE` 明示；未知 token 不由路徑或檔名推定。ledger 記 token 來源。 | manifest authority／owner grant | token＋來源 locator；未知 → 0 寫入 | 未知 effect 默認 READ → `EFFECT_UNBOUND` | D1 |
| `DEV-PRE-01` | Precondition 1：live `root`、`HEAD`、`branch`、`dirty`、`untracked`、allowed roots、ACL、scope。以 `git rev-parse --show-toplevel/HEAD`、`status --porcelain=v2`、`branch --show-current`、ACL probe 取真值。 | repo 可讀、git 可執行 | `repo_probe.json`（root/head/branch/dirty/untracked/acl） | 缺任一 → `REPO_BINDING_UNBOUND`；錯 HEAD 停 | D1 |
| `DEV-PRE-02` | Precondition 2：每個 target 的 preimage raw bytes／SHA-256，或明確 `ABSENT`。新檔不得以空檔冒充 preimage。 | 逐檔 `Get-Item`／`Get-FileHash` 或 Python | `preimage[]`（path/bytes/sha256/absent） | synthetic preimage → `PREIMAGE_UNBOUND` | D1 |
| `DEV-PRE-03` | Precondition 3：真 operation class 與 effect class；非 W1 產品 effect 不執行。ledger 記 op id→effect。 | effect registry／manifest | op/effect join | 由檔名推定 → `EFFECT_UNBOUND` | D1 |
| `DEV-PRE-04` | Precondition 4：Owner scoped grant（subject/scope/roots/writes/effect/expiry/revoke）＋真 OS/Repo ACL；不以 `permit=true` 代替。 | 本輪 Owner 裁決＋真 ACL | `authority.json`：grant ref、acl、principal | 無真權仍寫 → `FALSE_AUTHORITY` | D1 |
| `DEV-PRE-05` | Local toolchain／output root：Python 3.11、Git、CODEX entry、隔離 output root；不得寫全域。 | 版本探測；root 存在 | `toolchain.json`＋output root | 寫全域／來源根 → `OUTPUT_ROOT_INVALID` | D1 |
| `DEV-WS-01` | WriteSet 1：Guide renderer（`guide_nf.py`）與其 render/negative tests；只產 thin text／advice，不發 Grant。 | D2 完成；preimage | 檔 diff＋`render_thin` POS/NEG raw | 擴 scope／寫原 Guide → `WRITESET_VIOLATION` | D3 |
| `DEV-WS-02` | WriteSet 2：Bridge native reader／legacy projection（`bridge_nf.py`、`nf_reader.py`）；六檔直讀、舊投影另檔。 | 05/schema/六檔真 bytes | `inspect_package` 回 5+1＋source refs | 改原 reference parser → `WRITESET_VIOLATION` | D2 |
| `DEV-WS-03` | WriteSet 3：BodyResolver（`body_resolver.py`）；canonicalize／strict parse／span／size／link 防護。 | root／limits／fixture | resolver POS＋path/UTF8/dup/oversize NEG raw | 繞 containment → `PATH_OUTSIDE_ROOT` | D3 |
| `DEV-WS-04` | WriteSet 4：Host facade／consumer adapter（`host_facade.py`、`w1_consumer.py`）；只輸出實際 invoked/served/consumed，不偷裝 Host。 | P03 entry；真 host probe | consumer action/readback＋stage ledger | 以 facade 冒 install/serve → `HOST_PENDING` | D4 |
| `DEV-PROH-01` | Prohibition 1：不改 W0/LastGood/M/B/WM/W1M/舊 primary；只讀。 | 來源 hash 基線 | outside diff＝0 | 任一原件變更 → `SOURCE_MUTATION` | D1–D7 |
| `DEV-PROH-02` | Prohibition 2：不改 frozen Case/Oracle/Registry；需要新預期時建新版本＋新 hash。 | 13×2 asset hash | 新 oracle 獨立版本；舊 hash 不變 | 改 oracle 求綠 → `ORACLE_DRIFT` | D5 |
| `DEV-PROH-03` | Prohibition 3：不讀密鑰／未授權外部資料；不跨根、不 link 逸出。 | secret scan pattern；root containment | 無 secret、no outside read/write | 讀 secret／越根 → `SECRET_OR_ESCAPE` | D1–D7 |
| `DEV-PROH-04` | Prohibition 4：不以 `git revert`／`reset --hard`／`clean -fd` 代替 OPS 恢復；產品 DEV 復原用 preimage／reverse patch。 | preimage＋staging | reverse patch／readback | 用 revert 代 restore → `RECOVERY_KIND_MISMATCH` | D6 |
| `DEV-OP-01` | Operation 1：live RepoContext 探查（同 PRE-01）並固定 `repo_ctx_ref`；非 Git 則 `NON_GIT_FILE_CONTEXT`＋snapshot。 | root 可讀 | `repo_ctx_ref`（含 non-git 判定） | 假 HEAD／假 git → `REPO_BINDING_UNBOUND` | D1 |
| `DEV-OP-02` | Operation 2：逐 target preimage／ABSENT；D6 repair 前重查。 | 逐檔工具 | preimage hash 表 | preimage 漂移 → `PREIMAGE_DRIFT` | D1/D6 |
| `DEV-OP-03` | Operation 3：只寫 exact WriteSet；post 以 diff／tree check 證 outside 不變。 | WriteSet 清單 | `git diff --name-only` 或檔案樹 diff；outside＝0 | 全 repo glob／越檔 → `WRITESET_VIOLATION` | D2–D6 |
| `DEV-OP-04` | Operation 4：真 callable 的 POS/NEG，不只 policy：四 API 對六檔 fixture、Guide 對兩模式、九鍵對兩期、BodyResolver 對邊界。 | entry 可執行；fixture 凍結 | 每 API POS＋NEG raw／exit | 只跑 rule／policy → `CALLABLE_UNVERIFIED` | D3–D5 |
| `DEV-OP-05` | Operation 5：postimage SHA、diff、test raw、exit；raw 唯一 run_id，不覆寫正負例。 | 操作完成 | `post/`＋`raw/` 檔＋SHA | 無 raw 宣 PASS → `OBSERVATION_RAW_MISSING` | D2–D6 |
| `DEV-OP-06` | Operation 6：真 receiver 同 scope 讀回實際 output；不只比 hash。 | receiver 可達 | `readback.json`（consumer/scope/bytes/sha） | 只 hash 不比內容 → `CONSUMER_UNVERIFIED` | D4/D7 |
| `DEV-ADP-01` | Adapter 1：Guide 只建議／薄 prompt，`permission_state=NONE_GRANTED`；advice 不得升 WorkOrder。 | 原 Guide 契約 | thin prompt＋advice fixture | advice 發 Grant → `FALSE_AUTHORITY` | D3 |
| `DEV-ADP-02` | Adapter 2：Bridge 唯讀；context constraint 不等 Grant；不寫原 canonical。 | 授權 root 唯讀 | response fixture＋no-write raw | 寫原 canonical → `WRITESET_VIOLATION` | D3 |
| `DEV-ADP-03` | Adapter 3：BodyResolver 完整 path／strict parse／span／line SHA；unknown 保真或拒。 | limits＋fixture | 6 類 NEG raw | 丟 unknown → `ABI_LOSSY_CROSSWALK` | D3 |
| `DEV-ADP-04` | Adapter 4：Host facade 依真 invoked/served/consumed 分帳；不把 Skill bytes 或 exit 0 升格。 | host probe | stage ledger | 升格 → `HOST_PENDING` | D4 |
| `DEV-POST-01` | Postcondition 1：六檔＋manifest 五 digest；15 舊血緣另帳、不混 canonical。 | 五 MD 真 bytes | 05 pack_files 5/5；外置 seal | 05 自嵌／雙 canonical → `MANIFEST_CYCLE` | D7 |
| `DEV-POST-02` | Postcondition 2：每 Case fixture/oracle SHA 與 03/05 join 一致；舊 oracle 不改。 | 26 assets | join 表全 match | 改舊 oracle → `ORACLE_DRIFT` | D5/D7 |
| `DEV-POST-03` | Postcondition 3：六身份在 00–04、05、asset scope 一致；第六鍵讀時合成。 | 05 raw bytes | `identity_check.json` | 任一鍵漂移 → `IDENTITY_MISMATCH` | D7 |
| `DEV-POST-04` | Postcondition 4：planned claims 不冒 actual；每 claim 有 evidence class。 | claim ledger | `claims.json`（false/NOT_RUN） | 未跑填 PASS → `AS_BUILT_OVERCLAIM` | D7 |
| `DEV-POST-05` | Postcondition 5：來源／未授權目標不變、diff 可回取；交付根外無寫。 | outside canary | canary unchanged＋diff | 來源變更 → `SOURCE_MUTATION` | D7 |
| `DEV-RB-01` | Readback 1：新六檔 guard/結構 readback；舊 guard 只對 legacy schema，不判新包 PASS。 | 新 validator | `nf_pack_guard verify` 真 exit/raw | 用舊 guard 判新包 → `GUARD_DOMAIN_MIX` | D7 |
| `DEV-RB-02` | Readback 2：Case/raw/source 真 join，非摘要；每 raw 有 run_id。 | raw 已產生 | join 表＋raw locator | 摘要冒 raw → `EVIDENCE_LAUNDERING` | D5–D7 |
| `DEV-RB-03` | Readback 3：真 SHA／fixture／oracle replay；比 expected語義，不只 exit 0。 | 凍結 pins | replay raw＋verdict | 只 exit 0 → `SEMANTIC_MISMATCH` | D5 |
| `DEV-RB-04` | Readback 4：真產品 POS/NEG raw、獨立核驗（不同 session/worktree），不只 rule。 | Checker 分立 | independent raw＋finding | Maker 自簽 Independent → `FALSE_INDEPENDENT` | D6/D7 |
| `DEV-IDEM-01` | Idempotency 1：同 identity/revision/operation key 已成效 → no-op，不重寫。 | op key | `noop` readback | 重複寫入 → `IDEMPOTENCY_VIOLATION` | D2–D6 |
| `DEV-IDEM-02` | Idempotency 2：暫時 I/O 只能重試 1 次；`UNKNOWN` 先 reconcile，不盲重試。 | raw 狀態 | retry 記錄＋ reconcile | 盲重試 → `UNKNOWN_BLIND_RETRY` | D6 |
| `DEV-IDEM-03` | Idempotency 3：LastGood／同卷 staging／reverse patch／diff；保原 raw。 | LastGood 已存 | restore readback | 刪證據／destructive reset → `RECOVERY_KIND_MISMATCH` | D6 |
| `DEV-PERM-01` | No DEV grant：本 ECP 不授權任何寫入；無有效 grant／ACL 只做 READ/DRAFT。 | authority 檢查 | 0 產品寫入 | 以 ECP 當 Grant → `ECP_NOT_GRANT` | D1 |

**合計 38／38**；每列均保原 `PRE/WS/PROH/OP/ADP/POST/RB/IDEM/PERM` 語義。原 27 個 `ORIGINAL_DOMAIN_HOLD` 仍在原域未閉合；本表只承接 Generic 安全與可執行責任。

---

## 3｜D1–D7 建造操作（文件／產品分界）

| 步 | 本輪實際狀態 | 證據 |
|---|---|---|
| `D1` | **DONE_LOCAL**：worktree、HEAD、branch、ACL、preimage、output root 已核 | `nf_r2_inspect_probe.json`、worktree `git status` |
| `D2` | **DONE_MINIMAL**：`W1/impl/w1_nf_reader.py` 六檔 schema dispatch／四 API-like／BodyResolver／strict JSON | 16/16 unittest；`inspect` raw |
| `D3` | **PARTIAL**：Guide/Bridge 的 explain/render/compare 已有最小 native 實作；TPM 四契約與 Guide 九鍵 verifier 尚未建 | `explain`/`render`/selftest |
| `D4` | **NOT_RUN**：第二不同包、獨立 consumer、Host served/consumed | — |
| `D5` | **NOT_RUN**：13 原案真 runner（fixture/oracle 已凍結） | assets 26 |
| `D6` | **PARTIAL**：本 reader 的 mutation 16 案已 fail-closed；產品 FirstFail loop 未跑 | unittest |
| `D7` | **PARTIAL**：本文件包已 seal；repo commit/push 待執行 | seal |

### D1 Bootstrap 與 LastGood

1. 真 probe：`git -C <root> rev-parse --show-toplevel`、`rev-parse HEAD`、`branch --show-current`、`status --porcelain=v2`；`python --version`、`git --version`、`codex --version`。若 `<root>` 非 Git，記 `NON_GIT_FILE_CONTEXT`＋檔案快照。
2. 讀 05→00→01/02/03/04，回報 `next/op/required inputs/expected/stop/resume`，形成 `bootstrap_consume.json`（`BOOTSTRAP_CONSUME≠W1_PRODUCT_CONSUMED`）。
3. 保存 LastGood 指標（`last_good_ref`）與本輪 staging 路徑；不得覆寫來源。
4. 建 `authority.json`：Owner 裁決 ref、scope、roots、effect classes、expiry/revoke、ACL/principal probe、exact WriteSet、preimage/ABSENT。

**本輪實際**：D1 文件 probe 已完成；產品 repo 寫入 `NOT_ADMITTED`（ACL deny），bootstrap 接收已完成（見證據附件 E7）。

### D2 ABI／reader

- **已建** `W1/impl/w1_nf_reader.py`：嚴格讀 `FHS5.PLP.W1.SourceManifest.NF@1`、五 MD、assets、sources、identity、digest、seal、DAG、ID set。
- **已建** 四 API-like：`inspect_package`／`explain_slice`／`render_agent_context`／`compare_context`；`resolve_body` 為 span reader。舊 `w1_bridge_reference.py` 保留為 legacy parser／安全參考，不直接判新 schema PASS。
- **已建** `W1/check/test_w1_nf_reader.py`：16 tests（real pack、full sections、untrusted marker、span、compare、byte flip、missing file、dup key、NaN、path traversal、identity、drop DEV、DAG cycle、asset digest、seal mismatch）。
- **實際驗收**：`inspect` 回 5 files／38 DEV／29 OPS／13 cases／26 assets／42 sources／14 holds；`selftest` 4/4 PASS；unittest 16/16 OK。
- **尚未**：legacy 15 projection 的 `projection_of_sha256` 僅在舊 consumer 需要時生成；本輪未生成。

### D3 產品核心（TPM／Guide／Bridge）

- `tpm_contracts_nf.py`：同 work identity 產 PI／PD／DEV／OPS／TQAEP 五視圖；缺 B／無源 gate／格式對但 bytes 錯 → 拒。
- `guide_nf.py`：四原函式＋四 NF 函式 adapter；`PACKAGE_FIRST`／`CONTEXT_AUGMENTED`；九鍵 verifier 從真 file/receipt 讀，不用 caller bool。
- `body_resolver.py`：canonicalize＋strict JSON＋span＋size＋link 防護。
- `bridge_nf.py`：`explain_slice`／`render_agent_context`／`compare_context`；完整 Clause/Parent/Child/NEG/Exception；unknown 不丟。
- 驗收：每 API 至少 1 POS＋1 NEG raw；九鍵每鍵變／缺期／跨 scope 各 1 NEG；BodyResolver 至少 path／UTF8／dup／oversize／symlink 五 NEG。

### D4 Native consumer 與第二包

- `w1_consumer.py`：讀 context（或直接讀六檔），執行一個受界、可觀測、不涉 W2 保護效果的任務（例如：抽取指定 Case 的 Requirement/Child/NEG 並生成受 scope 約束的 checklist），輸出 action／readback／scope echo。
- 第二個非 briefcheck 小包：任何同 schema 的不同 subject/scope 工作包（可由 W0/W1 真材料構造），不得硬碼本包 ID。
- 驗收：consumer 真 parse/use；錯 pin／缺 clause／scope 擴張拒；第二包重用同一 API。

### D5 凍結測例

- 13 原案 fixture/oracle 已在本包 `assets/`（26 檔）凍結；runner 從真 entry/help 得，未建則 `BUILD_MINIMAL`。
- N01–N04/N10/N11 建立子例 fixture（隔離根），每例 expected／firstfail／raw 欄位先凍結再跑。
- 未跑案件一律 `NOT_RUN`；不得填假 exit／sha。

### D6 最小 repair

- FirstFail → 根因（source/contract/capability/authority/environment/implementation/oracle/consumer/architecture）→ ChangeCone → 只在 scope 內修 → 受影重驗。
- 同 finding 最多兩次**有實質差額**的修補；暫時 READ I/O 只重試一次；無新差額／同首錯不變／真權缺 → 停受影，列 LastGood/Next/Resume。

### D7 Seal／handoff

- 五 MD 定稿 → 05（含真 SHA/bytes/lines）→ 外置 seal（05 SHA、五 MD、assets）。
- fresh receive：從新根重算 5+1、assets、identity、DAG、ID set；錯 pin 拒。
- 只在真 grant 下 commit/push；本輪 `NOT_ADMITTED`，不改 GitHub。

---

## 4｜Exact WriteSet（產品階段）

| Target（W1 產品工作區相對路徑） | 型態 | Preimage |
|---|---|---|
| `W1/impl/nf_reader.py` | 新增 | `ABSENT` |
| `W1/impl/bridge_nf.py` | 新增 | `ABSENT` |
| `W1/impl/body_resolver.py` | 新增 | `ABSENT` |
| `W1/impl/guide_nf.py` | 新增 | `ABSENT` |
| `W1/impl/tpm_contracts_nf.py` | 新增 | `ABSENT` |
| `W1/impl/w1_consumer.py` | 新增 | `ABSENT` |
| `W1/impl/host_facade.py` | 新增 | `ABSENT` |
| `W1/check/test_nf_reader.py` | 新增 | `ABSENT` |
| `W1/check/test_guide_nine_keys.py` | 新增 | `ABSENT` |
| `W1/check/test_bridge_body.py` | 新增 | `ABSENT` |
| `W1/check/test_consumer.py` | 新增 | `ABSENT` |
| `W1/evidence/**/raw/**` | 新增 | `ABSENT`（唯一 run_id） |

若工作區已有同名檔，該檔改列 `MODIFY` 並在 preimage 記 bytes/SHA；無 preimage 不得覆寫。任何未列 target 皆不可寫。

**禁止**：全 repo glob、`git reset --hard`、`git clean -fd`、force push、改原 oracle／W0/M/B/WM/W1M/舊 primary、讀 secret／API key、未授權外部 effect、以 `git revert` 代 OPS 恢復。

---

## 5｜Command／Expected／Recovery

| 操作 | Planned command（真 entry 由 `--help` 具體化） | Expected | Recovery |
|---|---|---|---|
| Pack 結構驗證（本輪已跑） | `python tools/nf_pack_guard.py verify --root <pack_root>` | exit 0；5/5、26 assets、ID/DAG/identity/seal 全過 | 修受影檔；不改來源 |
| Reader／API（本輪已跑） | `python W1/impl/w1_nf_reader.py inspect --pack <pack_root> --out <raw>` | 5／38／29／13／26／42／14；exit 0 | reverse patch；保 raw |
| Reader tests（本輪已跑） | `python -m unittest W1/check/test_w1_nf_reader.py -v` | 16/16 OK；POS＋NEG | 只回受影 |
| Guide 九鍵 | `python -m pytest W1/check/test_guide_nine_keys.py -q` | 9 鍵逐變＋缺期／跨域／單 SHA 全拒 | 只回受影 |
| TPM 四契約 | `python -m pytest W1/check/test_tpm_contracts.py -q` | 四契約同 identity；缺 B／無源拒 | 保原契約 |
| Consumer | `python W1/impl/w1_consumer.py --pack <root> --task <bounded_task> --out <approved>` | parsed action/readback；錯 pin 拒 | 刪本次 output；重讀 |
| 13 案 | `python W1/check/run_cases_nf.py --pack <root> --out <approved>`（建造後） | 每案 POS/NEG raw；未跑 NOT_RUN | 受影重跑 |

**UNKNOWN**：timeout／partial／exit 0 但語義錯 → 先 readback；已成效 no-op；未成效且 preimage 仍符合、grant 仍有效、操作 idempotent 才重試一次。不得把 UNKNOWN 當 0／false。

---

## 6｜Bootstrap 接收實錄（本輪）

| 項 | 實際 |
|---|---|
| 入口 | 05 `schema`＋00 identity／§5 DAG |
| 讀取 | 5 MD＋05 strict JSON＋26 assets（真 SHA 重算） |
| 回報 | `next=P01`、`op=真 H0/六檔 pins 核對與 CapabilityLedger`、`required inputs=repo root/ACL/entry/第二包`、`expected=文件全過＋bootstrap raw`、`stop=錯 pin／無 ACL／未知 effect` |
| 狀態 | `BOOTSTRAP_CONSUME_ACTUAL`；`W1_PRODUCT_CONSUMED=NOT_RUN` |

---

## 7｜NotCovered

產品 repo 寫入（ACL deny）、真 W1 entry 建造、13 案真 runner、CODEX served/consumed、第二不同小包實跑、GPT CHAT/WORK/HERMES、Windows symlink/reparse 真攻擊、W2–4、Independent、Release。以上不因文件合格而消失。
