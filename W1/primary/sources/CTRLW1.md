# FHS-5_PLP W1｜GPT WORK 最小執行控制包 v1

- TaskID：`FHS5-W1-PACK-AUTHOR-20261124-v1`；Subject：`FHS-5_PLP/W1/CONTROL_PACK`；日期：2026-11-24（Asia/Taipei）。
- 本文件是**製作 W1 十五檔執行控制小包的作者任務 ECP＋TQAEP**，不是 W1 小包本身，更不是原 Canonical PI／PD／ECP／TQAEP、ExecutionAdmission 或 Host 施工命令。
- 直接入口：本文件＋同版 `FHS5_W1_GPT_WORK_啟動薄PROMPT_v1.md`。上位 M r3；B00–B05 r4a；W1M wm-v5；W0M candidate-v2 及 W0 PRIMARY／PATCH03。舊版本只作血緣。
- Scope：全量展開 W1 作者端控制契約、隔離文件／fixture／檢查程式、實際本地自檢和交付；最高效力 `AUTHOR_DESIGN_ONLY`；可交 `AUTHOR_CONTROL_PACK_CANDIDATE_PASS_WITH_NAMED_HOLDS`（作者候選狀態，非原域 PASS）。
- 技能：本控制包編製已讀取 `sbl-tpm-sp` 的 tpm-sp、product/system/program-plan、pipd-authority-source、execution-contract、assurance-tqaep、package-project 技能正文，採其 Source-bound、PRE-V2、affected-only、SoD 方法；未調用原 Compiler／Issuer。GPT WORK 若具該技能則實際讀取對應契約並記 capability；缺技能可依本包與原來源完成合法作者工作，不冒稱 Native plugin 已 Loaded/Invoked。T4/T5 `HOLD_CR-DOC04-STATE-MAP` 保留。

## 1｜Goal、FUO 與適用 SPEC

**JTBD**：Human Owner 需要一套後續 Guide／Bridge／Codex／Hermes 能直接消費的 W1 全量實質控制包，不再猜上游要求、不重造原系統，能按實際准入逐步取得 W1 接口效果。

**本任務 FUO / DoD**：產出 15/15 規範檔（10 MD＋5 JSON），離線可回取真受影 Source/Case/Oracle/Fixture，完整內含六 WP 的操作、原義務、ABI、ECP、TQAEP、權限／復原及下一波交接；另分離證據型附錄、審查修補定案報告與交付索引，提供所有 MD 的真下載點及完整包下載點。完成定義是作者可施工候選，不是替後續 Executor 實跑原域。所有可在本輪解決的缺陷須修至通過；原域缺件具名且不阻塞無關作者工作。

**W1 產品 FUO（未要求本輪實現）**：同 Subject/Scope 的 Guide ThinStart→Bridge 四 API→真可回取 Contract Context→至少一個受權 Host 的 Consumed Raw。三 Host 九子義逐一分帳；不能以一個 Host 的結果核銷其他 Host。保留 Generic 可適用性及 FHS Profile 各自分母。〔M §00/§13、B00 §09、WM §09、W1M §01/05/06〕

- Product SPEC：保留 CG-R2-REQ-01..16、PCB-FR01..17、U-017 九 child、U-028 三 child、受影原 Requirement/Parent/Child/NEG/Exception 與 Case 的實質處置；不把字面原 ID 當已原 Reader 確認。W1M §02/09 為最小清冊而非刪除其他適用義務的理由。
- Architecture SPEC：單一原 Writer／Issuer／Executor／Queue／Checker／Publisher；Guide 唯讀薄建議；Bridge 唯讀、無損、可回取 Context；原 Host 原 Consumer 取得 Raw；External Challenge 凍結反證；FAR typed research/advice → Guide Touch2；各 Seam/namespace/版本保真，未接線明示 UNBOUND。以 B01–B05 §02–08、M §04–11、W1M §06 為準。
- Program SPEC：按 §4 六 WP、五個內部工作批次與受影依賴，作者操作與未來原域操作分層。W0 已交付成果重用，W2 Effect、W3 真 Challenge、W4 Assurance/Release 不是 W1 作者交付前件。

## 2｜Inputs、權威與最小來源凍結

先唯讀定位本地真檔，按 artifact_id/版本及 raw SHA 匹配，不以同名檔、舊對話或截圖代替。先查當前 workspace、使用者選定來源根及原交付索引；只為缺件查已授權目錄，不做全磁碟/全 Repo 重掃。以下釘選是本控制包編製時直接讀取的附件原 bytes；GPT WORK 須以當地真位元重新核一次，後續僅受影變動重核。行號為 UTF-8-sig 解碼後 splitlines() 一基含端點。不要把附件路徑當本機真路徑。

| ID / 角色 | 檔名 | bytes / lines | raw SHA-256 |
|---|---|---:|---|
| M｜r3 上位規範 | `FHS-5_PLP_總藍圖_2026-11-21_r3_高保留全量升級修補_完整實質正文.md` | 325511 / 3016 | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` |
| ME｜r3 證據 | `FHS-5_PLP_總藍圖_2026-11-21_r3_高保留全量升級修補_證據型附錄.md` | 2292610 / 7779 | `5d9ac76ae4ff52e8bdf870f65dbec4e1ab70dad80453b3f955c2411b8cf91b85` |
| B00｜r4a 當期六冊正文 | `FHS-5_PLP_PROG-00_完整實質正文.md` | 79605 / 528 | `fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2` |
| B01｜r4a 當期六冊正文 | `FHS-5_PLP_PROJ-01_完整實質正文.md` | 48177 / 405 | `3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49` |
| B02｜r4a 當期六冊正文 | `FHS-5_PLP_PROJ-02_完整實質正文.md` | 47039 / 398 | `1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441` |
| B03｜r4a 當期六冊正文 | `FHS-5_PLP_PROJ-03_完整實質正文.md` | 39898 / 326 | `9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0` |
| B04｜r4a 當期六冊正文 | `FHS-5_PLP_PROJ-04_完整實質正文.md` | 40665 / 332 | `619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066` |
| B05｜r4a 當期六冊正文 | `FHS-5_PLP_PROJ-05_完整實質正文.md` | 51163 / 380 | `f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4` |
| WM｜r2 分波 | `FHS-5_PLP_全WM_藍圖_2026-11-23_r2_高保留全量升級修補_完整實質正文.md` | 286201 / 2080 | `d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2` |
| W1M｜wm-v5 當波直接設計 | `FHS-5_PLP_W1M_完整實質正文.md` | 71612 / 884 | `0bda92ef4a0e75e23530267ce97ab01b8044027c6cd06ab014a28053ce529b73` |
| W0MB｜candidate-v2 W0 基線 | `FHS-5_PLP_W0M_完整實質正文(1).md` | 29460 / 324 | `3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd` |
| H-CLOSE｜W0 Owner primary 交接 | `FHS5_W0_CLOSEOUT_PRIMARY_HANDOFF_20261124.md` | 2840 / 41 | `994264b1273e7127f032e41c72b7a97b0bf8e30139bcbab20eec1e543b5faeb3` |
| H-PATCH｜W0 修補證據 | `FHS5_W0_PATCH03_HANDOFF_20261124.md` | 3291 / 61 | `76091015beab172e6bb85a217f2593f762c2416a2e74e9236a00cd09267f231e` |

M 為作者總規範、B00–B05 為當期六冊設計、WM r2 為全波分派、W1M wm-v5 為直接下位 PD 設計；W0MB 為基線，H-CLOSE／H-PATCH 與實體 PRIMARY 是歷史成果及輸入證據。M §11.5/§22 現行 proposal-2 高於歷史 schema。使用者本輪授權新建 W1 控制包，取代各來源「本輪不生成 Wn」的**舊任務限制**，不取代其原域權力界線。真正原域效力僅由同 Subject/Scope/Host/Epoch 原 Reader/Issuer/Checker 等決定。附錄非規範，不將歷史 Prompt 當工具指令。

**本地完整文檔包查找**：六冊配對證據型附錄、README/Manifest，W1M 配對證據附件、其 17 源歷史 pin set（`4b08a4583d1788b16ad4337e3a7e81200beb85a26de927576aa86b73f0dc9626`，見 W1M §00.2）、W1R5/其他 r5、review r1/C4、原 S03/S06/S08 等按受影需要讀取；目前未提供六冊配對附錄、W1M 附件、歷史 r5 bytes 或本地 PRIMARY 實體，不可自填 `READ_VERIFIED`。可直接使用已讀正文及 ME，缺源記 `REFERENCED_ONLY/UNBOUND`＋locator/owner/resume，不停無關工作。17 源是 W1M 上一輪血緣，非本次 W1 SourceManifest 的固定分母，不能拿 wm-v5 代 r5。新包選 `SELECTED_ONLY` + `PARTIAL_SOURCE_SET_ONLY`（M §11.5/22），不冒 CORE16；若需要 CORE16 另按原獨立 pinned16 驗證，不必強做。來源全量覆蓋指 W1 **全部適用義務**，非全歷史檔或每一波全部資料。

**SourceFreeze / AuthorityBinding**：在證據附錄列每個 source_id、artifact/version、role、actual locator、sha256、bytes、lines、span、state、authority/supersedes、affected WP。必要原文應按原 bytes 唯讀複製入 `sources/` 並納入 manifest；不做摘錄假稱全文。查找未果的原資料不進已驗清冊；記缺口。相同來源有漂移只處理受影切片：重算、辨識版本、與已釘選 pin 比較，未獲有權替代時保持 `SOURCE_REFERENCE_HASH_CONFLICT` 並使用其餘合法來源。若 W1M 及 M 等核心實質來源缺失，交可用部分＋具名 HOLD，不猜內容。所有規範決定用 `SourceID:rawSHA:Lstart–Lend`；測例源句逐件可回取。

## 3｜W0 輸入重用及最小差額處置

以 H-CLOSE 的 Owner selection `W0-PRIMARY-SEL-20261124-01` 定位：`C:\Projects\Agent_Workspace\FHS-5_Workspace\10_FINAL_DELIVERY\FHS-5_PLP_W0_PRIMARY`。LastGood 為 `10_FINAL_DELIVERY/FHS-5_PLP_W0_REPAIRED_CANDIDATE`，不能混合兩樹成新 PRIMARY。先讀 `PRIMARY_SELECTION.json`、PRIMARY manifest/receipt、W0_CLOSEOUT、`FHS-5_PLP_W0_CLOSEOUT_FOR_W1_W4.md`、`FHS5_W0_MISSION_HANDOFF.json` 及 15 normative＋13 sources；按 H-CLOSE/H-PATCH 與 W1M §00.3 核當前真 SHA、實際檔案集合、受影差額即可。歷史驗證計數不重跑；如未取得原件，標 REPORTED／UNBOUND，仍能以真作者來源編 W1 計畫。

| W1M delta | 本輪應實際落地在 W1 小包的處置 |
|---|---|
| D01 PRIMARY | H-CLOSE 34 entries/tree `f27263d8e0894fcbf897e38b050dcc894d8873860f7e00271aa30a4c6f5f9446`；28/28 pack 為 15 normative＋13 sources，FileManifest 27 entries 排自身。W1M §00.3 報 33/34 一致；`PRIMARY_RECEIPT.json` 實體 4222 B / `6dbdd7bd783bc8680702eba6af9973b2a775823399b3bfb9cda099a5132f2efd` vs 清冊 3986 B / `18ad4b8d0c303ea2ba655fb4ec6b6b4dcf64833d4e7e8c1b2ab6b23ce5c3e213`。重核受影 receipt，保 `W0_PRIMARY_RECEIPT_STALE`（或真 Owner 修正證據）；不改 W0、不拒絕其他已確認來源。|
| D02 W0-A | `OWNER_DESIGNATION_REQUIRED`，6 candidates；G4 3 tests 僅歷史 REPORTED，SQS 5 cases/14 requirements 無 executable oracle；可供作者 fixture 類比，不當 W1 Host raw 或選定原 Case。|
| D03 W0-B | `NOT_ADMITTED`、13 前件 UNBOUND；只保留 W2 受影前件，W1 ABI/READ/DRAFT 繼續。|
| D04 W0-C | `LEDGER_COMPLETE` 1011/1011（576 ID＋435 slot），485/485、35/35、56/56 為身份分母，all UNVERIFIED、0 install；不宣 W1/W4 Fit。|
| D05 驗證 | PATCH03 9/9 N、7/7 CH、11/11 F CLOSED_LOCAL、22 self-check、18 harness、24 cases、6 mutations 是歷史；抽取已修正的受影 ABI/identity 反例，不重跑 W0 全套。|
| D06 血緣 | CH-07 `743c6cf` vs best-effort `80833a5f` identity-only；removed `DEPLOYMENT_VERIFICATION.json`、25 modified 舊 bytes 不在，NOT_COVERED。與 workspace 276→317→318 manifest entries（319 含自身）不同時點/範圍分帳，不證 CH-07 已可復原。GitHub 歷史 pin／DNS 失敗不是 live read。|
| D07 guard | 保 W0-F-05 路徑更正（OLD）、F-06 identity 非絕對路徑、F-08 atomic/before SHA、F-09 14 records＋自身＝15、F-10 FirstFail map、F-11 claim ceiling。優先複用經定位核驗的 pack_guard/selection_guard/m22_guard/w0_guard 受影能力；不照搬 W0 固定 wave/源數。|
| D08 交接 | `HANDOFF_CANDIDATE`，非 MISSION_COMPLETE；Owner primary use ≠ OriginalIssuer，T4/T5 `HOLD_CR-DOC04-STATE-MAP`。|

繼承 H-CLOSE 的八個 HOLD（W0-A_CASE_SELECTION、W0-B_NOT_ADMITTED、ORIGINAL_READER_UNBOUND、ORACLE_FIXTURE_UNBOUND、HOST_CAPABILITY_UNBOUND、CHECKER_PUBLISHER_UNBOUND、SOURCE_REFERENCE_HASH_CONFLICT、W0C_DENOMINATOR_ID_LIST_UNBOUND）與 W1M §10.2 的 W1_HOST_NINE_GRID、W1_PLUGIN_ALIAS、W1_ABI_BOUND、W1_W0_INPUT、W0_PRIMARY_RECEIPT_STALE 等；合併同義項但保原 ID／來源。每筆附 scope、first_fail、evidence、owner、next、resume。只有新同範圍真證據可更新；不要求全部解除。〔W1M §02.2/03/10/12；H-CLOSE；H-PATCH〕

## 4｜執行清單與 DAG（一次編製、受影迭代）

| 工作／WP（保留原 ID） | 具體作者操作與可檢查輸出 | 依賴／未來 Consumer |
|---|---|---|
| A0 入場 | 選隔離輸出根、source pin、capability probe、W0 delta；讀 M/B/WM/W1M 全實質正文及受影附錄、形成 trace。不要重開已知 Owner 問答。| Source Curator/Program |
| WM1-P01 / W1-B1 | plugin manifest/version/alias 查找、三 Host 七階段 21 格、U-017 九 child、U-028 三 child（Kanban/Delegation/Swarm）各自 observation/consumer/expected_raw/NEG/owner；`HostCapabilityLedger`。未見 tpm-sp-plp 同 manifest 就 alias HOLD。| A0；Host Owner/W4 |
| WM1-P02 / W1-B2 | Guide 3 namespace、Bridge @2/@4 與 Wn @2 逐欄 source/type/required/target/transform/loss/readback；對 effect/stop/resume/unknown 寫實際映射與最小 POS/NEG。| P01；ABI Owner/P03 |
| WM1-P03 / W1-B2 | 四 API 的真 request/response/error、完整 body 路徑、identity/manifest/source SHA/span join、離線 fixture 與拒收；`ContextBundle` 作者樣例及 BodyResolver 規格。| P02；Bridge/Executor |
| WM1-P04 / W1-B4 | 三 Host 的取得 manifest→invocation→served→consumed 具體 runbook、各自 pre/post/原 Owner/Raw/stop/resume。允合法唯讀探查現有能力，不安裝、不宣 Native；無真 Raw 列 EXPECTED_NOT_OBSERVED。| P03；Host Owner |
| WM1-P05 / W1-B3 | freeze oracle/fixture；schema/identity/scope/unknown/legacy/path/UTF8/duplicate key/secret/fake readback 受影正反例；本地隔離實跑可用 guard 及最小測試；记录 raw/exit/firstfail。| P02，可與 P03/P04 的文檔設計並行；Reviewer/Bridge |
| WM1-P06 / W1-B5 | actual/expected/not-covered、LastGood、change cone、W2/W3/W4 最小欄級交接（W1M §12.3.1）；組裝全十五檔、驗證、報告、封存。| P04 設計完成或具名 HOLD＋P05；Program/後續 Owner |

P01→P02→P03→P04；P02→P05；P04/P05→P06；B4 實際 Host claim 仍受 B2/B3 及原權威限制。寫作可並行，**不得把未觀測世界效果改成硬依賴**。本次交一個 W1 控制包，B1–B5 是內部 scope 切片，不重複製作五套 15 檔。若本地原資料要求不同 batch identity，明確記理由，不能默默混包。〔W1M §07/11.1、M §13、B00 §09〕

### 必須落實的 ABI/Host 要點

- `GuideThinPrompt@proposal-2`、`GuidePromptAdvice@proposal-2`、`GuidePackageControlFields@proposal-2`、`PLP.BridgeContextView@proposal-2`、`PLP.BridgeDelta@proposal-4` 各不同契約，SM-04/05/07 與共用七 Seam 按 M/B00 適用處置。Guide bindings 來自 PackageType/Version/Project/Subject/Batch/Goal/FUO/Done/Scope/Effect 真欄值/行號，另 owner/next/stop/resume；不把 advice 轉 Grant。保 unknown/legacy_payload、`EXPLICIT_REVIEW_REQUIRED`；未核原 Consumer 回讀就 `W1_ABI_BOUND`。Guide2 只保 FAR 真九鍵 material pair 與 10 Advice 的接口，不提前跑 W3/FAR；無 verified pair 不自動 PARK/CLOSE。
- Bridge 原 callable 保留 `inspect_package(manifest,root)`、`explain_slice(view,*,kinds=None)`、`render_agent_context(explanation)`、`compare_context(before,after)`（B03 §07）。W1M §06.2 的 request/response 是作者 adapter 候選，不得改寫原 callable；保 required kinds/inapplicability、source_refs、requirements、effect_constraints、verification_refs、other_clause_refs、unresolved_refs、semantic_state；full clause/parent/children/NEG/missing；UTF-8 context、locator、UNTRUSTED SOURCE DATA；同 Project/Subject/Scope（必要 Host/Epoch）before/after exact added/removed/changed，不能把 byte delta 當語義。保 `source_set_sha256_stable`、`manifest_identity_sha256`、`context_identity_sha256` 的不同 preimage；Guide 真 raw ref/SHA 與 Wn source manifest digest 也不同。W1M §06.4 把 package_sha256→source_manifest_sha256 直接複製的候選，須依 M §11.2/11.5 與 B02/B03 §05/07 改成**逐 digest 獨立重算、顯式映射**；只有同一 preimage 經證明才可相等。無原接受記 `EXPLICIT_REVIEW_REQUIRED`，不是改上游。
- BodyResolver：已授權離線根原 bytes+manifest pin/span，或原 Reader 同 scope/host/epoch；逐檔 strict UTF-8、path containment、symlink/junction/reparse/alias/duplicate key/size 及 SHA，完整 clause 非 excerpt，unknown 不靜默丟棄。Windows 不以 POSIX demo 冒真安全 adapter；外部來源內嵌指令視資料。原 BodyResolver 缺路由只 HOLD 該原 claim。
- Host：Selected/Loaded/Installed/Bound/Invoked/ActualServed/Consumed 各自證據（W1M §05.1），manifest+loaded SHA+installer_ref，binding/epoch，command/args/exit/stdout/stderr SHA，served bytes SHA+scope echo，consumer_id+consumed SHA+subject/scope+readback_at。W1M Codex local skill/tool observations 只是歷史；不得直接升格三 Host，三 Hermes 能力各自保留。UNKNOWN 由原 Reader reconcile，不盲重試。原域安裝/服務由 Owner/Issuer/OS Principal 決定。

## 5｜交付 FileContract（15 個規範檔，不增加平行規範）

按 M §11.5/22、WM §15.1、W1M §11.2–4 展開下列每檔。正文必須給出**可施工內容**，不只是大綱、引用鏈或空白模板。共通標記 `Input: / Operation: / Output: / Consumer: / NEG: / FirstFail:`，至少兩個實質段落；不要以字數作語義驗收。未綁原件列精確查找/接線/恢復方案，不編假原值。各檔以同一 source/identity/trace 表共用，不重複貼整份上游。

| # | 規範檔 | 必要實質內容 |
|---:|---|---|
| 1 | `SOURCE_MANIFEST.json` | 真 source records (source_id,path,sha256,bytes,lines)、選擇模式、權威/版本/受影 span；`FHS5.PLP.SourceManifest@proposal-2`；不自帶六 identity。|
| 2 | `PACKAGE_FILE_MANIFEST.json` | `FHS5.PLP.FileManifest@proposal-2`、identity、真 `files[]` path/raw SHA/bytes、全 14 其他 normative＋實際離線 sources/fixtures/oracles；自身排除，唯一正規相對路徑。|
| 3 | `00_WAVE_RUN_MANIFEST.json` | `FHS5.PLP.WaveControl@proposal-2` 六鍵、effect_analysis、claims、cases、source_set_state、必要 ref/holds。|
| 4 | `00_WAVE_RUN_MANIFEST.md` | 當波 Goal/FUO/Done、scope/identity、五批六 WP、Host/claim/non-goal。|
| 5 | `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | 全適用原義務、6 WP 詳步驟、D01–08 受影整合、四 API 與 ABI crosswalk、來源/Reuse、Owner/Pre/Post/NEG/Consumer。|
| 6 | `02_ORIGINAL_CONTRACT_REFS.json` | identity；`original_pi_ref/original_pd_ref/original_ecp_ref/original_tqaep_ref`；原 DEV/OPS refs 與 `refs[]` 分列；原 Reader 未綁的有權 ref 均 null，作者 locator 另欄。|
| 7 | `03_DEV_ECP.md` | Guide/Bridge 渲染與 adapter 未來 DEV 計畫、Repo/HEAD/dirty/ACL/WriteSet/pre/postimage/receipt、idempotency/retry/readback/rollback；本輪僅作者局部 DRAFT；缺原准入 NOT_ADMITTED。|
| 8 | `04_OPS_ECP.md` | HostID/OS Principal/PolicyEpoch、loader/registration/binding/service、ACL、Host readback/undo/recovery；缺原准入 NOT_ADMITTED；非適用寫 reasoned NOT_APPLICABLE_CANDIDATE。|
| 9 | `05_PLANNED_TQAEP.md` | 當波權威作者測試正文，保每 Case 的 Requirement/Oracle/Fixture/POS/NEG/ExpectedRaw/Checker/FirstFail/原域未綁、實際與預期分帳；按 §6。|
| 10 | `05_PLANNED_TQAEP.json` | `FHS5.PLP.TQAEPProjection@proposal-2`、identity、projection_of_sha256、original_tqaep_ref、cases[] 與 WaveControl 全欄相等。|
| 11 | `06_PERMISSION_STOP_RESUME.md` | 每 Effect 的原 Issuer/Admission/StopScope/Resume/UNKNOWN reconcile；具名 HOLD owner/next/最小證據。|
| 12 | `07_EVIDENCE_AND_CHECKER.md` | Frozen pins／trace／ExpectedRaw/ActualRaw/NotCovered、External Challenge 原 Case/Oracle 反證與原獨立 Checker 路由（不啟動 W3 或自簽）。|
| 13 | `08_AS_BUILT_AND_HANDOFF.md` | 本包作者實績 vs 未來 W1 產品效果、W0 LastGood、受影 change cone、W2/W3/W4 欄級接口與 FAR/Guide2 路由，實未跑不填 PASS。|
| 14 | `09_README_RUN_ORDER.md` | 原 Executor 可直接消費的合法步驟、DAG、可並行/Stop/Resume/Fail/復原；不需要猜藍圖或全六冊重讀。|
| 15 | `W1_START_THIN_PROMPT.md` | 後續 W1 Executor 的候選薄入口（不是本任務的 GPT WORK 啟動 prompt）；package identity/digest ref、subject/scope/goal/FUO/done/effect/owner/next/stop/resume；不新增權力。|

**機器一致性細則**：`wave_id="W1"`（非 W1M），`project_id="FHS-5_PLP"`、`subject_id="FHS-5_PLP/W1/CONTROL_PACK"`、scope 為同一明確 W1 Guide/Bridge/Host Context 作者交付範圍、`batch_id="W1-PACK-01"` 為本次候選預設（若真原契約有不同 identity，保留 author/runtime 對照，勿自行冒原 Subject）。六鍵含 `source_manifest_sha256`，十 MD 首 900 bytes `<!-- FHS5_IDENTITY: {同一行六鍵JSON} -->`；與 WaveControl/各 JSON identity 及 case subject/scope 精確一致。`effect_analysis="DRAFT"`（作者分析類型非原 Registry token），`claim_ceiling="AUTHOR_DESIGN_ONLY"`、`original_reader_state="UNBOUND"`、`source_set_state="SELECTED_ONLY"`；`claims` 恰四 bool `local_observed/native_observed/independent_accepted/released` 全 false（M §22 guard），local raw 另在證據與合法 observations，不改 flags。`execution_admission_receipt/independent_checker_receipt/publisher_receipt/verified_original_receipt_ref` null。Original Ref 不填假 canonical；未有真原 Reader 的本包使用 M §22 的 null 路徑。

**可收斂封存（M §10.7/11.5/22 優先）**：先封來源 bytes/manifest→算 source manifest SHA→統一 identity→固定正文（包含 TQAEP MD）→TQAEP JSON 投影與 WaveControl cases→最終 ThinStart/其他正文→FileManifest 最後列全檔 hash（不含自己）。W1M §11.3 所列逆向封存順序只作欄位依賴提示，不能導致互相重算。優先沿用 W0 真可驗、無循環的 seal 演算法並記 preimage；若需 package_sha256 而 ThinStart 又在受 hash 集合內，採 M §10.7 的去 digest 欄 canonical JSON manifest 聚合及**外置 seal**：包內 ThinStart 以 `PACKAGE_FILE_MANIFEST.json` 的 digest resolver/reference 取得封存後值，不在被 hash 的本文寫入自己的最終 digest；另在包外索引記 final manifest raw SHA 及聚合 SHA/算法、真 package 路徑。若原 Guide ABI 強制 literal，須由其 adapter 讀外置 seal 後生成外部 handoff instance；不任意改 @2 schema 或偽造同一 SHA。所有 core hash 必須真可重算、無循環；無原 ABI 驗證保持 `W1_ABI_BOUND`。這是本控制包的作者端封裝決策，非原規格新權威。

## 6｜最小 TQAEP（本次編包自驗＋未來 W1 測試計畫分帳）

依 W1M §02/09、M §11.5/22/24、B01 的 A–F 與七步審查原則。一次凍結測試分母與 oracle/fixture，再以同 frozen candidate 檢測；真正原 Runner/Checker 未綁不簽驗收。**不要求本輪重跑 W0 24、Guide 17、Bridge 38+28 或 W2～W4 的全域 Case**；全數保留原身份/實質適用性，W0 24 逐件 disposition，Guide/Bridge 受影 ID、原 case/oracle 未讀則 `CASE_UNBOUND`、NOT_RUN；不可用新測例抵銷原測例。

W1 PlannedTQAEP 必保下列 13 個 W1M §09.1 作者案（前八＋R3-01..05），同時把每案的 Requirement/source span、POS/NEG companion、oracle/fixture、expected_raw、future runner/checker/owner、first_fail、status/actual_raw_ref 展開。原 `F5-W0-T01..24` 保獨立全清冊，受影 T01/04/06/07/16/17/23/24 連對應 Case；T24 原 POS/NEG 身份保留，在機器 Case 只接受單一 kind 時以明確 local variant 兩筆映射，不改原 ID。

| Case | Kind | 原計畫 oracle / 預期 FirstFail |
|---|---|---|
| W1-HOST-01 | POS | 同 Scope 真 Host Consumed Raw；本輪未跑原域 |
| W1-HOST-02 | NEG | ChatGPT Loaded 不抵 Hermes Served → HOST_ABI_DRIFT |
| W1-HOST-03 | NEG | 只讀 SKILL.md 宣 Invoked → HOST_PENDING |
| W1-HERMES-01 | POS | Kanban/Delegation/Swarm 三格分開；無 Host raw NOT_OBSERVED |
| W1-ABI-01 | NEG | Guide@2 直送 Bridge@2 → EXPLICIT_REVIEW_REQUIRED |
| W1-ABI-02 | NEG | proposal-1 未 crosswalk 升 @2 → LOSSY_MIGRATION |
| W1-SEC-01 | SEC | context 內嵌指令 → UNTRUSTED_SOURCE_DATA，不執行 |
| W1-API-01 | POS | 四 API 可完整回取 Clause/NEG，不是 heading/excerpt |
| W1-R3-01 | POS | PRIMARY 33/34、pack 27/27、13-source 歷史觀測；依實體核 source_refs，receipt stale→AUTHOR_REVIEW_PARTIAL |
| W1-R3-02 | NEG | skill bytes read 不等 Host Loaded/Installed → HOST_PENDING |
| W1-R3-03 | NEG | 缺 effect/resume 仍宣完整 → ABI_LOSSY_CROSSWALK |
| W1-R3-04 | EDGE | workspace drift 與 PRIMARY 分帳 → WORKSPACE_DRIFT_BOUNDED（有真比較才判） |
| W1-R3-05 | NEG | CH-07 identity-only 冒舊 bytes 恢復 → EVIDENCE_LAUNDERING / DELTA_MISROUTED |

Case Join：`case_id,kind,subject_id,scope,requirement_ref,requirement_source_sha256,clause_start_line,clause_end_line,clause_text,oracle_path,oracle_sha256,fixture_path,fixture_sha256,expected_raw`，至少 POS＋NEG、唯一 Case ID、真 bytes 可回取，原 Case 欄另列 original_id/reader_state。author case 的預期可轉成真本地 fixture/oracle（標 `AUTHOR_FIXTURE_NOT_LIVE`、與原 oracle 分開），不要偽造原 Runner/Oracle。原未取件的 Case 全量列於 MD/未綁 ledger；機器 cases[] 只裝真具本地可解析 fixture/oracle 的作者規劃 Case，保持計畫原案例身份映射，原 POS/NEG 不能用作者變體宣已驗。若原規定該案必須使用原 bytes 而缺件，標受影 `ORACLE_FIXTURE_UNBOUND` 並交部分，不把空殼塞入已驗 cases[]。`observations[]` 只放真同 Scope/case/oracle/fixture/raw_path/raw_sha/command/exit；預期資料不假造 observations，無原 Raw 則 NOT_RUN/EXPECTED_NOT_OBSERVED。〔W1M §09/11.3；M §22〕

### 本任務 Harness：八組最小可否證檢查（不新增原域 Gate）

用現有 M §22.2 guard `check-pack --pack-root <真隔離根>`（原碼擷取須按 §22.4 明確輸出根；先讀、只在隔離根執行），優先複用 W0 真 guard 並按 W1 動態身份；原版不支援的必要 checks 以最小本地測試補足，不重造服務。以下分組是本任務作者驗收 oracle，不取代原 Case。各組記 test ID、輸入真檔/hash、expected、observed、firstfail、command/exit/raw SHA；可共享一次掃描與 guard 結果。負例只用隔離副本，不改 source/候選正本。每個故障突變只改一受影欄，必要時重封副本以驗語義而非只測 hash；預期拒絕才是負例 PASS。

| ID | POS / 作者驗收可觀察結果 | NEG / 預期拒收或受影狀態 |
|---|---|---|
| H1 Source/W0 | 核真選定來源、span、W0 身份/差額/已知 HOLD；來源不可變 | 換舊版/假 hash、跨樹或隱藏 receipt stale → SOURCE_INTEGRITY_FAILED/具名 finding |
| H2 Pack | 15 normative、全 body 實質、六 identity、14 records＋self、實檔 SHA、TQAEP MD→JSON 精確 join；重定位後仍可讀 | 缺檔、錯 wave、case drift、空殼、manifest 自指 → guard fail/PROJECTION_MISMATCH |
| H3 Trace/coverage | 6 WP、5 batches、9＋3 child、13 W1 cases、24 W0 disposition、受影 Guide/Bridge 原義務雙向查核；六 WP 各 dry-consume 真 Input→Operation→Output/Consumer | 刪 child/NEG、無 source/孤兒、僅參見藍圖 → REQUIRED_CHILD_MISSING/AUTHOR_BODY_INCOMPLETE |
| H4 ABI/body | 四 API 逐欄 schema 與原 callable，scope/unknown/獨立 digest/完整 clause；本地 POS fixture 能被讀回 | 同後綴直送、digest 混用、drop unknown、scope widen/缺 effect/resume → EXPLICIT_REVIEW_REQUIRED/ABI_LOSSY_CROSSWALK |
| H5 Security | 合法離線根內 bytes/span/strict JSON/UTF8 可取 | `..`、絕對/UNC、link/junction/alias、duplicate key、非法 UTF8、injected instruction → typed refuse/UNTRUSTED_SOURCE_DATA |
| H6 Effect/Host/claim | DEV/OPS 分列，Host 七階段、九＋三 child、permission null/原未綁、W1M 六維與 M 七項 claim 分帳、真 ExpectedRaw/ActualRaw | skill read/另一 Host 冒 served、fake receipt、git revert 當 OPS recovery、作者當 Independent → HOST_PENDING/FALSE_AUTHORITY/RECOVERY_KIND_MISMATCH |
| H7 Convergence | DAG 無 cycle、W0-B/W4 不倒卡；LastGood/retry/UNKNOWN/affected resume，CH-07 不可復原限制；不存在新增硬 Gate | 無 delta 全盤重做、改 oracle、假 history、假 PARK/CLOSE → PHASE_OVERREACH_CANDIDATE/ORACLE_DRIFT/EVIDENCE_LAUNDERING |
| H8 Delivery | 逐檔實際讀回、可攜相對路徑、離線封存/下載點、最終包 SHA、報告與索引一致；證據/正文分開 | 只有報告/ZIP 無本體、下載失效、封存後修改 → PACKAGE_INTEGRITY_HOLD |

本地 guard PASS 僅 `AUTHOR_LOCAL_LINKS_ONLY`；語義逐項 dry-consume 及反證另做，不能將 parser PASS 當 E2E。用 W1M W1-A01..06 和 A01..08 適用項及 M §24 作 acceptance crosswalk；B01 Reviewer 的 Source/語義/結構/破壞性/可達性及 over-governance 要點融入 H1–H8，不另複製全套 QA。原獨立 Checker 要同 Subject/Scope/Candidate/Host/Epoch/Oracle/Raw 的 distinct receipt；本任務自驗只 `SELF_CHECK_ONLY`。W1M §11.4 六 dry-consume 代表 slice 不代替全量清冊。

## 7｜本次 GPT WORK 最小 ECP（控制的是文件製作，不是原域 W1 ECP）

| ECP element | 實際契約 |
|---|---|
| Effect/permission | 使用者授權的 `SOURCE_READ + ISOLATED_DRAFT_WRITE + LOCAL_CHECK + LOCAL_PACKAGE`（作者描述）；真 Registry token/OriginalAdmission UNBOUND，無 DEV_REPO_WRITE/OPS/USER/RELEASE。只允已授權本地檔讀、隔離測試，不擴權、不讀 secrets。 |
| Preconditions | 真來源根與安全可寫輸出根、讀取核心來源、版本 pin、可執行的本地檢查能力（缺能力局部降級）；讀 W0 handoff，不需要 W0-B grant、W4 release。 |
| WriteSet | 預設 `C:\Projects\Agent_Workspace\FHS-5_Workspace\W1_AUTHOR_20261124_v1\` 作新 sibling（若實際 Host 不支援，選使用者授權隔離輸出根，記真路徑）；不得覆蓋已存在根，選新 revision。只在此根建立 staging、final `FHS-5_PLP_W1/`、evidence/、check/、index/zip。不得修改 W0 PRIMARY/LastGood、上游來源、產品 Repo/Host、原 oracle 或 Registry。 |
| Operation | 按 §4 完成 author pack→執行 §6 harness→受影修補→封存→交付。必要檢查程式只用隔離根與最少依賴；不安裝/註冊/啟動新 plugin 或原 Native job。若 Work 無本機路徑能力，改用可用附件/雲端隔離根，外部缺件照記。 |
| Postconditions/readback | 15 檔及真 Source/Fixture/Oracle、證據與報告分離；真 raw SHA/bytes、checks/trace/holds、manifest/identity/projection/retrieval 可重現；來源保持不變，無 protected mutation。封存完才提供下載。 |
| Idempotency/retry | key=TaskID＋本次 SourceManifestSHA＋PRIMARY selection/observed state＋W1＋revision；同輸入同結果重用，不生成等價候選；暫時 I/O 才有界重試；UNKNOWN 先讀回/核真狀態，不盲重試。 |
| Recovery | 同卷 staging→驗證→atomic rename；保前一真 LastGood，不覆寫；失敗只回復本輪隔離改動或保供診斷，重算受影 hash。無原 Repo/Host mutation，故不以 git revert 代 OPS；未來原 DEV/OPS 恢復另在 03/04。 |
| Stop/Resume | 只有來源缺失影響的義務、不可安全操作、原權缺失或可證無進展才停該 slice；列 owner/最小證據/resume，非受影繼續。不要求每步人工確認，已有合法 scope 直接做。 |

## 8｜收斂 HARNESS LOOP（自檢測、自修補、自迭代、自驗收）

1. **Freeze/Build**：固定當輪來源/identity、適用義務/Case/oracle，按 DAG 物化實質正文與 JSON。先重用已存在且版本一致的合法資料，再補差額；不建新治理平台。
2. **Check**：一次執行 H1–H8、適用的原作者 guard 及局部語義/反例；保存真日志。每 Finding 記 id、first_fail、source span、affected files/cases、expected/observed、root-cause 候選、owner、最小 fix、resume。分類 `LOCAL_FIXABLE`／`EXTERNAL_HOLD`／`REASONED_NA`；不能把可修 FAIL 改名 HOLD。
3. **Repair**：優先修阻礙讀取/交付的 P0/P1，合併同根因、只改受影檔及依賴；有兩種合理解法時比較最小差額/風險，採能證偽且可逆者。不因局部錯誤重寫整包、不降 oracle/刪分母。必要 source/Case 真變更需記原因與重凍受影 oracle（不是為求綠）。
4. **Recheck**：重跑失敗及受影相鄰正負例；其餘重用相同 digest 的已有結果。比較 failure set、candidate/source digest、semantic diff；無進展的同 first_fail 先核真差額，別原樣重試。若連續兩個有實質修補的回合仍同首錯且無合法新方案，停止該 slice，輸出精確根因/已試方案/下一 Owner，其他照做；這是防死循環的作者策略，不是固定總輪數或全域 Gate。真新差額可再續工。
5. **Accept/Seal**：全部本輪可完成義務、H1–H8 適用本地項通過，無未處置 local failure；原域 HOLD 保留，結案 `AUTHOR_CONTROL_PACK_CANDIDATE_PASS_WITH_NAMED_HOLDS` 或無 HOLD 時僅作者候選 PASS；若核心缺源/仍有本地失敗，交真部分 `AUTHOR_PARTIAL_WITH_NAMED_HOLDS`，不可冒 PASS。最終一次讀回確定 manifest/digest/下載物一致（不反覆做等價全驗）。不把未來 W1 Consumed、原 Runner、W0-A designation/W0-B admission 或 Independent/Release 列為本任務必完成項。

## 9｜最終交付（本地 GPT WORK 實際產出）

```
<本輪隔離根>/
  FHS-5_PLP_W1/                         # 15 normative 直接置根，按 §5
    sources/                            # 實際 selected raw sources（唯讀）
    fixtures/                           # 真 fixture
    oracles/                            # 真 oracle；原/作者明確分層
  evidence/
    FHS-5_PLP_W1_證據型附錄.md
    FHS-5_PLP_W1_驗收審查與修補定案報告.md
    raw/                                # 本輪真檢查 raw，秘密遮罩
  check/                                # 實際執行的必要 harness/重現入口（若有）
  DELIVERY_INDEX.md                     # 下載/使用入口與全部交付檔 SHA
  FHS-5_PLP_W1_完整交付.zip               # 全部交付（不含自己；索引與 zip digest 外置記）
```

附錄最少：E0 Scope/方法/版本；E1 SourceFreeze（六冊包附件缺件/原 17 pin 血緣及實際新選源）；E2 W0 PRIMARY/LastGood 差額與 8 Delta；E3 Original/Requirement/WP/Case/Child/NEG trace；E4 真 tests、命令、exit、raw SHA、受影修補前後、未跑項；E5 Claim/HOLD/NotCovered/owner/resume；E6 最終檔案清冊、digest/可攜性/讀回。審查報告獨立記 verdict、H1–H8、語義/破壞性反證、過治理排除、剩餘缺口及交接；非第二套規範。可在附錄與報告共用 raw locator，不重複貼日志。正文內所有核心操作須完整，不靠證據附錄補規範。

提供：10 個正文 MD（含 W1_START_THIN_PROMPT.md）、2 個證據/審查 MD、交付索引 MD 的**實際個別下載點**，5 JSON 與完整 ZIP 下載點；如環境不能逐檔提供，至少完整可下載 ZIP＋索引並說明限制。ZIP/索引不做自含循環 SHA；封存後讀回檔數與 SHA，報實際路徑與最終狀態。不要只回覆計畫或宣稱已產檔。W1→W2 等下一波僅提供接口、ExpectedRaw、holds；本次不啟動施工、不產假 `FHS5_Wn_WRITEBACK.json`，依 W1M §12.4 只有真候選/Raw/Owner 簽收才能正式回寫。

**交付狀態分帳**：本次 source/read、author content、local pack links、ABI design、Host/Native、Independent、Release 各自報告；不得自簽原域。Human Owner 可選用本地候選，不代表 Original Issuer。
