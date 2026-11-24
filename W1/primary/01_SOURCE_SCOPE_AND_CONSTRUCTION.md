<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜來源、原義務與施工正文

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的 Construction 正文，批次 `W1-PACK-01`。它把 M r3 的 FileContract、W1M wm-v5 的 W1 設計、B02／B03 的 Guide／Bridge ABI 與 W0 PRIMARY 的實體差額，落成 Executor 可直接讀的施工內容。效力 `AUTHOR_DESIGN_ONLY`。

## 1. SourceFreeze 與選擇模式

| ID | 角色 | 版本 | bytes | lines | raw SHA-256 | 本輪狀態 |
|---|---|---|---:|---:|---|---|
| M | 上位總藍圖 | r3 | 325511 | 3016 | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` | READ_VERIFIED |
| B00 | Program Master | r4a | 79605 | 528 | `fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2` | READ_VERIFIED |
| B01 | TPM-SP／Reviewer | r4a | 48177 | 405 | `3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49` | READ_VERIFIED |
| B02 | Guide | r4a | 47039 | 398 | `1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441` | READ_VERIFIED |
| B03 | Bridge | r4a | 39898 | 326 | `9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0` | READ_VERIFIED |
| B04 | External Challenge | r4a | 40665 | 332 | `619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066` | READ_VERIFIED |
| B05 | FAR | r4a | 51163 | 380 | `f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4` | READ_VERIFIED |
| WM | 全 WM | r2 | 286201 | 2080 | `d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2` | READ_VERIFIED |
| W1M | 當波設計 | wm-v5 | 71612 | 884 | `0bda92ef4a0e75e23530267ce97ab01b8044027c6cd06ab014a28053ce529b73` | READ_VERIFIED |
| W0MB | W0 基線 | candidate-v2 | 29460 | 324 | `3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd` | READ_VERIFIED |
| H-CLOSE | W0 Owner 交接 | v1 | 2840 | 41 | `994264b1273e7127f032e41c72b7a97b0bf8e30139bcbab20eec1e543b5faeb3` | READ_VERIFIED |
| H-PATCH | W0 PATCH03 | v1 | 3291 | 61 | `76091015beab172e6bb85a217f2593f762c2416a2e74e9236a00cd09267f231e` | READ_VERIFIED |
| CTRLW1 | 本任務控制包 | v1 | 35609 | — | 見 `SOURCE_MANIFEST.json` | READ_VERIFIED |
| STARTW1 | 本任務啟動薄 | v1 | 2336 | — | 見 `SOURCE_MANIFEST.json` | READ_VERIFIED |
| W0-PRIMARY-MANIFEST | W0 PRIMARY 清冊實體 | local | 5914 | — | 見 `SOURCE_MANIFEST.json` | READ_VERIFIED |
| W0-PRIMARY-RECEIPT | W0 PRIMARY 收據實體 | local | 4222 | — | `6dbdd7bd783bc8680702eba6af9973b2a775823399b3bfb9cda099a5132f2efd` | READ_VERIFIED |

ME（r3 證據附錄，2,292,610 bytes／`5d9ac76a…`）按需 span 讀取，未複製入包；標 `REFERENCED_ONLY`。六冊配對證據附錄、W1M r5 歷史 bytes、review r1／C4 未提供本地實體，保持 `UNBOUND`，不以檔名補位。

Input: 上表真 bytes。
Operation: 逐檔 SHA／bytes／lines 重算，選 16 源，建 pinned manifest；同名不同 SHA 只重開受影切片。
Output: `SOURCE_MANIFEST.json`＋本表。
Consumer: Source Curator／Bridge／Executor。
NEG: 以舊版或摘要冒原文 → `SOURCE_IDENTITY_HOLD`。
FirstFail: `SOURCE_INTEGRITY_FAILED`。

## 2. 原義務 disposition

Guide 的 `CG-R2-REQ-01..16` 全部保留，不因四個函式縮分母：

| ID | 保留義務 | W1 處置 |
|---|---|---|
| `CG-R2-REQ-01` | 真 Package bytes／SHA／Subject／Scope 收件 | `inspect_package` 前置 |
| `CG-R2-REQ-02` | Phase／Wave／Batch 可選但不混身份 | 六 identity 分欄 |
| `CG-R2-REQ-03` | 只投影原 PI／PD／ECP／TQAEP／OriginalID | `02` 全 null＋locator 另欄 |
| `CG-R2-REQ-04` | source／claim／applicability 三自檢 | 本包 guard 三層 |
| `CG-R2-REQ-05` | AuthorReady 與 EffectDone 分級 | `claim_ceiling` 分帳 |
| `CG-R2-REQ-06` | 單一純文字薄 START | `W1_START_THIN_PROMPT.md` |
| `CG-R2-REQ-07` | RESUME 只看九鍵 | `06` 的 resume predicate |
| `CG-R2-REQ-08` | Effect 六分類只作導覽 | `effect_classes` 不授權 |
| `CG-R2-REQ-09` | FAR 十 Advice 交 Touch2 | `08` 的 Guide2 路由 |
| `CG-R2-REQ-10` | 不建第二 Writer／Checker／Scheduler | 全包 non-goal |
| `CG-R2-REQ-11` | Frozen Candidate／Evidence／Oracle SHA | `07` 與 seal |
| `CG-R2-REQ-12` | 不可信引文不改權限 | `UNTRUSTED SOURCE DATA` |
| `CG-R2-REQ-13` | 三 Host 分別載入與回讀 | 21 格 host claims |
| `CG-R2-REQ-14` | Search-Before-Build | 重用 W0 guard／plugin 技能 |
| `CG-R2-REQ-15` | 本地 CI 實跑不冒原域 | `SELF_CHECK_ONLY` |
| `CG-R2-REQ-16` | FHS 485／35 等原分母不降級 | 分母另帳，不宣 Fit |

Bridge 的 `PCB-FR01..17` 全部保留：

| ID | 保留義務 | W1 處置 |
|---|---|---|
| `PCB-FR01` | 識別 Project／Package／Subject／Scope／Phase | `inspect_package` identity |
| `PCB-FR02` | raw bytes／SHA／alias 安全 | BodyResolver |
| `PCB-FR03` | 分讀 PI／PD／DEV／OPS／TQAEP | `kinds` 枚舉 |
| `PCB-FR04` | SPEC 與治理 | `other_clause_refs` |
| `PCB-FR05` | Parent／Child／NEG／例外 | `explain_slice.children[]` |
| `PCB-FR06` | 雙向 trace | 來源 span＋Case join |
| `PCB-FR07` | DEV ECP 欄位 | `03` |
| `PCB-FR08` | OPS ECP 欄位 | `04` |
| `PCB-FR09` | Case／Oracle／POS／NEG／ExpectedRaw | `05` |
| `PCB-FR10` | Phase／Batch／Applicability | identity＋`inapplicability` |
| `PCB-FR11` | Guide→Bridge handoff | §5 crosswalk |
| `PCB-FR12` | 三 Host 同義 Context | `render_agent_context` |
| `PCB-FR13` | before／after 差額 | `compare_context` |
| `PCB-FR14` | 缺源安全降級 | `unresolved_refs[]` |
| `PCB-FR15` | 防來源內嵌指令 | untrusted marker |
| `PCB-FR16` | 非 FHS 不灌 485 | 分母分帳 |
| `PCB-FR17` | 無第二 Writer | non-goal |

另保留 Guide 原 17 案 `CG-SEM01..17`（全 `NOT_RUN`）與 Bridge 原 22 個 Finding `A-PCB-001..022`（各維持原效力，不與 `AV3-001..030` 合併）；兩組只作分母與反例索引，不以本包 13 案核銷。

`U-017` 九 child 全部保留：ChatGPT、Codex、Hermes 各 `Loaded`／`Invoked`／`ActualServed` 一列，互不代償。`U-028` 三 child 全部保留：Hermes `Kanban`／`Delegation`／`Swarm` 各自 observation、Consumer、ExpectedRaw、NEG、Owner。

W1M §02.3 的 24 個 `F5-W0-T01..T24` 全部保留原 ID；受影者 `T01／T04／T06／T07／T16／T17／T23／T24` 另給 W1 disposition，其餘 `RETAIN`／`NOT_RUN`，不得以新作者 Case 抵銷。

Case 對位：`W1-HOST-01`、`W1-HOST-02`、`W1-HOST-03`、`W1-HERMES-01`、`W1-ABI-01`、`W1-ABI-02`、`W1-SEC-01`、`W1-API-01`、`W1-R3-01`、`W1-R3-02`、`W1-R3-03`、`W1-R3-04`、`W1-R3-05`。每案的 Requirement／Oracle／Fixture／ExpectedRaw 在 `05_PLANNED_TQAEP.md`，本檔只給施工對位。

## 3. W0 D01–D08 差額處置

| Delta | 本輪實際觀測 | disposition | 對 W1 的影響 |
|---|---|---|---|
| D01 PRIMARY | 實體 36 檔＝23 root＋13 sources；`PRIMARY_MANIFEST.json` 34 entries；`PRIMARY_RECEIPT.json` 4,222 B／`6dbdd7bd…`，清冊記 3,986 B／`18ad4b8d…`；tree pin `f27263d8…` | `W0_PRIMARY_RECEIPT_STALE` 保留 | 仍可作 inspect 輸入；不得宣 receipt 已更正 |
| D02 W0-A | 6 candidates、`OWNER_DESIGNATION_REQUIRED`；G4 3 tests 只 `REPORTED`；SQS 5 cases／14 requirements、`has_executable_oracle=false` | `OWNER_DESIGNATION_REQUIRED` | 只作 fixture 類比；不當 W1 Host Raw |
| D03 W0-B | `NOT_ADMITTED`、13 前件 UNBOUND | `RETAIN` | 只擋 W2 前件，不擋 W1 ABI／READ |
| D04 W0-C | 1011/1011（576 ID＋435 slot）、485/485、35/35、56/56 全 `UNVERIFIED`、0 install | `LEDGER_COMPLETE` | 分母帳，不宣 W1／W4 Fit |
| D05 驗證 | PATCH03 9/9 N、7/7 CH、11/11 F、22 self-check、18 harness、24 cases、6 mutations 為歷史 | `REUSE_AFFECTED_ONLY` | 抽受影 ABI／identity 反例，不重跑 W0 全套 |
| D06 血緣 | CH-07 `743c6cf` vs best-effort `80833a5f` identity-only；`DEPLOYMENT_VERIFICATION.json` removed；25 modified 舊 bytes 不在 | `NOT_COVERED` | 不得宣舊 bytes 可復原 |
| D07 guard | F-05 路徑更正、F-06 identity 非絕對路徑、F-08 atomic／before SHA、F-09 14 records＋self、F-10 FirstFail map、F-11 claim ceiling | `REUSE` | 轉成 W1 的 path／identity／atomic／claim 檢查 |
| D08 handoff | `HANDOFF_CANDIDATE`，非 `MISSION_COMPLETE`；Owner primary use ≠ Original Issuer；T4/T5 `HOLD_CR-DOC04-STATE-MAP` | `RETAIN` | W1 不簽 Release |

## 4. 六 WP 施工步驟

**Typed DAG edges**（單向；`requires`＝from 依賴 to）：`WM1-P01 -requires-> WM1-P02`、`WM1-P02 -requires-> WM1-P03`、`WM1-P03 -requires-> WM1-P04`、`WM1-P02 -requires-> WM1-P05`、`WM1-P04 -requires-> WM1-P06`、`WM1-P05 -requires-> WM1-P06`。不存在的反向邊不得用來倒卡早波；W0-B 以 `deferred_to_wave(W2)` 保留，W4 以 `post_acceptance` 保留。

**WM1-P01 Identity／Reuse**：Step 1 以 SourceManifest 找 plugin 檔、alias、版本、bytes、SHA；Step 2 建 `HostCapabilityLedger`（Host×七階段一列）；Step 3 對 U-017 九 child 逐一填 observation／Consumer／ExpectedRaw／NEG／Owner；Step 4 對 U-028 三 child 分開填；Step 5 檢查 alias 是否同一 manifest，不能證明即 `W1_PLUGIN_ALIAS`。Output 交 Host Owner 與 W4。NEG：skill 可讀宣 Installed → `HOST_PENDING`。

**WM1-P02 ABI Crosswalk**：Step 1 逐 namespace 列欄位、型別、必選、來源、Consumer；Step 2 對每 source field 填 target／transform／loss／readback；Step 3 unknown／legacy 建 `legacy_payload` 與 `EXPLICIT_REVIEW_REQUIRED`；Step 4 建 POS／NEG fixture（同值直送、擴 Scope、drop unknown、`@2` 升 `@4`）；Step 5 指到 §5 列與目標檔。Output 交 Bridge／Guide ABI Owner。

**WM1-P03 四 API／BodyResolver**：Step 1 `inspect_package` 核 manifest／identity／16 源／13 Case；Step 2 `explain_slice` 按 view／kinds 取 clause，保 parent／child／NEG／missing；Step 3 `render_agent_context` 產 UTF-8 context 附 SourceLocator 與 untrusted 標記；Step 4 `compare_context` 只比同 Subject／Scope，輸出 exact tuple；Step 5 BodyResolver 逐 body 檢查 path containment／duplicate key／UTF-8／SHA／span。Output 交 Executor／Host Consumer。

**WM1-P04 Host Actual Read**：Step 1 每 Host 先確認 Selected／Loaded，無則停該 Host；Step 2 取 Invocation raw（command／args／exit／stdout／stderr SHA）；Step 3 取 ActualServed（served bytes SHA／scope echo／served_at）；Step 4 取 Consumed（consumer_id／consumed SHA／subject／scope／readback_at）；Step 5 對 U-017 九 child，缺一即 `REQUIRED_CHILD_MISSING`。

**WM1-P05 Adversarial ABI Tests**：Step 1 為 scope widen／unknown／no host／legacy／ACL escape／fake readback 各建最小 fixture（隔離副本）；Step 2 執行 schema／path／SHA／UTF-8／unknown 保留檢查；Step 3 記 expected／observed／firstfail／reproduction；Step 4 指到受影 API 欄與 repair 位置。Output 交 Reviewer。

**WM1-P06 AsBuilt／Next**：Step 1 分 actual／expected／not-covered；Step 2 建 ABI change cone；Step 3 交 W2 adapter interface（非 consumed）；Step 4 寫 W1→W2／W3 的 input／AcceptedRaw／限制。Output 交 Program。

## 5. Guide／Bridge ABI 逐欄 crosswalk

### 5.1 七 Seam 與 namespace 版本

| Seam | 上游 Producer | 下游 Consumer | 受影欄位 | 越界後果 |
|---|---|---|---|---|
| S1 Package 收件 | 原小包 Writer | Guide | package bytes／SHA／Subject／Scope | `SOURCE_IDENTITY_HOLD` |
| S2 Guide 建議 | Guide | Bridge | ThinStart bindings、advice、九鍵 Delta | `EXPLICIT_REVIEW_REQUIRED` |
| S3 Context 投影 | Bridge | Executor／Host Consumer | source_refs、requirements、NEG、unresolved | `CONTEXT_SCOPE_MISMATCH` |
| S4 DEV 控制 | DEV ECP | Repo Owner | WriteSet、pre/postimage、readback、rollback | `ECP_NOT_GRANT` |
| S5 OPS 控制 | OPS ECP | Host Owner／OS Principal | HostID、Principal、Epoch、loader、service | `HOST_PENDING` |
| S6 驗收 | TQAEP | Runner／Checker | Case、Oracle、Fixture、ExpectedRaw | `ORACLE_DRIFT` |
| S7 交接／回寫 | AsBuilt | W2／W3／W4 | 欄級 handoff、LastGood、NotCovered | `PHASE_OVERREACH_CANDIDATE` |

Guide 三 namespace 分立：`GuideThinPrompt@proposal-2`、`GuidePromptAdvice@proposal-2`、`GuidePackageControlFields@proposal-2`；Bridge：`PLP.BridgeContextView@proposal-2`、`PLP.BridgeDelta@proposal-4`；Wave：`FHS5.PLP.WaveControl@proposal-2`。同後綴不得直送；只有逐欄 crosswalk 後才可映射。

| Source field | Target | 型別 | Transform | Loss policy | Readback |
|---|---|---|---|---|---|
| `GuideThinPrompt.package_sha256` | Wn `source_manifest_sha256` | 64-hex | **獨立重算**，不直接複製 | 不同 preimage → `SOURCE_IDENTITY_HOLD` | Consumer echo 同 SHA |
| `GuideThinPrompt.subject`／`scope` | Wn `subject_id`／`scope` | string | 只允許同值 | 擴張 → `SCOPE_DRIFT` | echo 同值 |
| `GuideThinPrompt.goal`／`fuo`／`done` | Wn Goal／FUO／Done | string | 文字保留；`done` 必可觀測 | 字串 PASS → `EXPECTED_RAW_MISSING` | 對照 Case |
| `GuideThinPrompt.effect` | Original EffectRegistry token | enum | 只查表 | 未知 → `EFFECT_UNBOUND` | Registry／Issuer receipt |
| `GuideThinPrompt.owner`／`next`／`stop`／`resume` | Wn Owner／Next／Stop／Resume | object | 角色不寫個人；Stop 可執行 | 缺 resume → `RESUME_UNBOUND` | Owner 簽收 |
| `GuidePromptAdvice.advice_kind`／`reason`／`owner` | Guide2 advice | enum／string | 保留 kind／reason | 當 Grant → `FALSE_AUTHORITY` | Guide2 只回 advice |
| `GuidePackageControlFields.identity`／`bindings` | Bridge `inspect_package` | object | identity 對 manifest；bindings 對 Source／Effect | 衝突 → `EXPLICIT_REVIEW_REQUIRED` | 兩份 manifest 對讀 |
| `BridgeContextView.source_refs` | Context source list | array | 每筆 `(kind,path,SHA,span)` | 只 heading → `CONTEXT_SCOPE_MISMATCH` | BodyResolver raw SHA |
| `…requirements`／`effect_constraints`／`verification_refs`／`unresolved_refs` | SliceExplanation | array | 保留 Parent／Child／NEG／missing | 丟 unknown → `ABI_LOSSY_CROSSWALK` | 完整 clause 回讀 |
| `…source_set_sha256_stable` | Context digest | 64-hex | 只對 source 集合重算 | 舊 digest → `SOURCE_INTEGRITY_FAILED` | 同 digest |
| `…manifest_identity_sha256` | Context identity | 64-hex | 對 normalized manifest 重算 | 混用 → `MANIFEST_IDENTITY_LOSS` | 兩期 manifest |
| `…context_identity_sha256` | Context identity | 64-hex | 綁 source＋manifest＋phase＋Guide raw | 缺 Guide → `NOT_SUPPLIED` | Consumer echo |
| `BridgeDelta@proposal-4.added/removed/changed` | Guide2 delta | array | exact `(kind,path,SHA)` | `@2` rename → `SCHEMA_UNSUPPORTED` | before／after 兩期 |
| `BodyResolver.source_local_id`／`raw_sha256`／`line_start`／`line_end`／`line_sha256`／`full_text`／`path_scope` | Context body | mixed | 每次重核 manifest 與 root | 任一不符 → `BODY_RESOLVER_UNBOUND`／`PATH_OUTSIDE_ROOT` | 原 Reader 或離線封存 |

四個 digest 必須各自獨立重算：`source_set_sha256_stable`（排序 source rows）、`manifest_identity_sha256`（normalized manifest）、`context_identity_sha256`（再綁 phase 與 Guide raw）、`package_sha256`（package manifest／file set）。只有 preimage 被證明相同才可相等；W1M §06.4 曾把 `package_sha256` 直接複製到 `source_manifest_sha256` 的候選，本包依 M §11.2／11.5 改為顯式映射，無原 Consumer 接受記 `W1_ABI_BOUND`。

## 6. 四 API request／response／failure

| API | Request 必選 | Response | Failure | Consumer |
|---|---|---|---|---|
| `inspect_package(manifest, root)` | root、manifest_path、expected_identity、expected_source_manifest_sha256 | source_refs[]、requirements[]、effect_constraints[]、verification_refs[]、unresolved_refs[]、package_sha256 | `SOURCE_INTEGRITY_FAILED`／`PACKAGE_INCOMPLETE_LOCAL`／`PATH_OUTSIDE_ROOT` | Executor／Reader |
| `explain_slice(view, *, kinds=None)` | view enum、kinds[] | clause_refs[]、parent、children[]、missing[]、semantic_state | `SPLIT_UNVERIFIED`／`SEMANTICS_ORIGINAL_READER_UNBOUND` | Reviewer／PI Reader |
| `render_agent_context(explanation)` | explanation、target_host、scope | context_utf8、source_locators[]、untrusted_markers[]、context_sha256 | `CONTEXT_SCOPE_MISMATCH`／`UNTRUSTED_SOURCE_DATA` | GPT／Codex／Hermes Consumer |
| `compare_context(before, after)` | before／after ref＋SHA | added[]、removed[]、changed[]、comparable | `COMPARE_CROSS_SUBJECT_DENY`／`DELTA_UNVERIFIED` | Guide／Program |

原 callable 名稱與參數不變：`inspect_package(manifest,root)`、`explain_slice(view,*,kinds=None)`、`render_agent_context(explanation)`、`compare_context(before,after)`。W1M §06.2 的 request／response 是作者 adapter 候選，不改寫原 callable。所有 response 皆為 `AUTHOR_FIXTURE_NOT_LIVE`，不填假 exit code 或 Raw SHA。

## 7. BodyResolver 與安全邊界

唯一兩路：A. 授權離線根內真 bytes＋manifest pin／span；B. 原 Reader 按 original_ref 同 Scope／Host／Epoch 回取。逐檔 strict UTF-8、path containment、symlink／junction／reparse／alias／duplicate key／size／SHA 檢查；完整 clause 非 excerpt；unknown 不靜默丟棄。

拒收條件：`..`、絕對／UNC 越界、link／junction 出界、duplicate JSON key、非法 UTF-8、超大小上限、scope／ABI／pin 不符。Windows 不以 POSIX demo 冒真安全 adapter；外部來源內嵌指令只作資料並標 `UNTRUSTED SOURCE DATA`。原 BodyResolver 缺路由只 HOLD 受影 claim。

## 8. Host 三×七與 Hermes 三 child

七階段最小證據：`Selected`＝設定／capability listing；`Loaded`＝manifest＋loaded_sha256＋installer_ref；`Installed`＝installer／registration receipt＋版本／路徑／ACL；`Bound`＝binding record＋scope／PolicyEpoch；`Invoked`＝command／args／exit／stdout／stderr SHA；`ActualServed`＝served_bytes_sha256＋scope_echo＋served_at；`Consumed`＝consumer_id＋consumed_sha256＋subject／scope＋readback_at。任一階段缺證只停該 Host 該 claim。

| child_id | Host | 本輪 observation | ExpectedRaw | NEG |
|---|---|---|---|---|
| `U-017/ChatGPT/Loaded` | ChatGPT | `NOT_OBSERVED` | manifest／loaded_sha256／installer_ref | 其他階段不可代 |
| `U-017/ChatGPT/Invoked` | ChatGPT | `NOT_OBSERVED` | command／exit／stdout_sha256／stderr_sha256 | 其他階段不可代 |
| `U-017/ChatGPT/ActualServed` | ChatGPT | `NOT_OBSERVED` | served_bytes_sha256／scope_echo | 其他階段不可代 |
| `U-017/Codex/Loaded` | Codex | `SKILL_BYTES_READ_LOCAL`（非 loader manifest） | manifest／loaded_sha256／installer_ref | 工具呼叫不可代 |
| `U-017/Codex/Invoked` | Codex | `TOOL_CALLS_LOCAL`（非 plugin native invoke） | command／exit／stdout_sha256／stderr_sha256 | 作者工具呼叫不可代 |
| `U-017/Codex/ActualServed` | Codex | `NOT_OBSERVED` | served_bytes_sha256／scope_echo | 其他階段不可代 |
| `U-017/Hermes/Loaded` | Hermes | `NOT_OBSERVED` | manifest／loaded_sha256／installer_ref | 其他 Host 不可代 |
| `U-017/Hermes/Invoked` | Hermes | `NOT_OBSERVED` | command／exit／stdout_sha256／stderr_sha256 | 其他 Host 不可代 |
| `U-017/Hermes/ActualServed` | Hermes | `NOT_OBSERVED` | served_bytes_sha256／scope_echo | 其他 Host 不可代 |

本輪實觀：ChatGPT 全 `NOT_OBSERVED`；Codex 到 `TOOL_CALLS_LOCAL`（非 plugin native invoke）；Hermes 全 `NOT_OBSERVED`。`U-028/Hermes/Kanban`、`U-028/Hermes/Delegation`、`U-028/Hermes/Swarm` 三格分別 `HERMES_*_NOT_OBSERVED`；不得以本地待辦清單、作者工具呼叫或多個本地命令冒充。

## 9. 工具／選型與分母分帳

工具與分母的逐項帳不在正文重抄，放在 `inventory/TOOL_IDENTITY_LEDGER.json`（485 個 ToolNeed 原 ID，取自 ME E5，逐筆保留 `original_source／legacy_card／asset_kind／original_disposition／v3_action／primary_consumer`；10 筆 primary_consumer 落在 W1，標 `W1_AFFECTED_RETAINED_UNBOUND`；217 筆 `DEFERRED_TO_W0_C`；258 筆 `OUT_OF_W1_SCOPE`（W2–W4））與 `inventory/DENOMINATOR_LEDGER.json`（56 子義、35 Reviewer Tool、22 WP、36 Edge、50 H1、39 ModeGate、96 Oracle、192 Cell、485 ToolNeed、W0-C 1011、QA26、C16/36/47、FAR-T20/FARP30/35、Bridge 38+28、17 Guide、24 W0、13 W1）。所有 `HostFit`／`original_ack` 未得者一律 `UNBOUND`；這些分母不是 W1 完成 Gate，也不得用 1011/485 宣 W1 Fit。

## 10. Owner／Pre／Post／NEG／Consumer

| 工作 | Owner | Pre | Post／Readback | NEG | Consumer |
|---|---|---|---|---|---|
| SourceFreeze | Source Curator | 真 bytes 可回取 | manifest SHA＋bytes／lines | 假 SHA | Bridge／Executor |
| ABI crosswalk | Guide／Bridge ABI Owner | B02／B03 原文 | 逐欄 loss／readback 表 | 同尾碼直送 | W2 |
| 四 API | Bridge Owner | 原 callable＋manifest | response fixture＋unresolved | 只 heading | Executor |
| Host observation | 各 Host Owner | loader／installer | 七階段 Raw | 跨 Host 代償 | W4 |
| Case／Oracle | Case Owner | 原 Case registry | POS／NEG＋ExpectedRaw | 作者 fixture 冒原 | Checker |
| Closure | Program Owner | P04／P05 或 HOLD | AsBuilt＋handoff | 未跑填 PASS | W2 |

FirstFail 總則：只可回「參見藍圖」而無 operation → `AUTHOR_BODY_INCOMPLETE`；歷史 `REPORTED` 冒本輪 `OBSERVED` → `EVIDENCE_LAUNDERING`；作者自檢冒 Independent → `FALSE_INDEPENDENT`。
