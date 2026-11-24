# FHS-5_PLP_W0｜本地 GPT Work 最小執行控制包 v1.0

> **任務**：編製 `FHS-5_PLP_W0` 的**執行控制小包**（十五份當期固定文件），另以獨立 Markdown 保存來源與自檢證據；不是編製 W0M，也不是在本輪執行 W0 Native。
>
> **Task ID（作者任務）**：`FHS5-PLP-W0-CONTROLPACK-AUTHOR-20261123-01`；**交付類型**：`AUTHOR_CONTROL_PACK_CANDIDATE`。
>
> **執行者**：已獲使用者授權的本地 GPT Work，僅有來源 READ、授權隔離目錄 DRAFT/WRITE、可核對的本地自檢權；**無**原 Repo/Host DEV/OPS/USER/RELEASE 權。
>
> **根本界線**：`FHS-5_PLP_W0`（執行控制小包）≠ `FHS-5_PLP_W0M`（上位 Wave Master）≠ 歷史 `FHS_vNEXT/W0`（另一 Subject）。本輪只產生供合法下游使用的控制契約與證據，不觸發原執行器、不偽造 Original Reader、Issuer、Checker 或 Publisher。
>
> **規範狀態**：本檔是交給 Work 的作者側任務控制材料，不是 PIPD Canonical ECP/TQAEP；包內 `03_DEV_ECP.md`／`04_OPS_ECP.md` 是同樣受原 Reader 限制的**設計／執行條件文件**。未取得原 Admission，不可執行受保護 Effect。

## 0｜任務卡、先行結果與最輕治理

| 欄 | 最小可驗內容 |
|---|---|
| Goal | 由已完成的 W0M 正文＋證據附錄，編製具真來源、版本、Scope、ECP／TQAEP、Case／Oracle、Stop／Resume、ThinStart 與交接的 W0 **十五檔**控制包，另附一份**非規範證據型 MD**。 |
| Persona/JTBD | Wave Pack Author 使 Guide／Bridge／既有受權 Codex/Hermes、原 Case Owner／Checker 能讀懂「本波可做什麼、必要前件、遇阻如何停止與恢復」，不需重讀六冊全部文檔。 |
| FUO | 真正可讀且相互釘選的 W0 十五檔；合法 W0-A READ／隔離 DRAFT 具有明確路由；W0-B 原 Native 受有權准入約束並可 HOLD；W0-C FHS 回歸不縮原 ID 分母；Case 保留 POS／NEG／可觀察結果；有實際 bytes/SHA/載點。 |
| 本次 Done | 作者文件**十五檔實體**與獨立附錄均可讀、所屬身份與內容交叉相符、所需操作正文不是空殼；完成本地作者 QA、交出真檔載點與具名 HOLD。不得因未發生的 Native／Independent／Release 而誤判作者文件必須失敗。 |
| Non-goals | 不重製 W0M/W1M～W4M、不修改原 PROG/PROJ、不重造原 PIPD Canonical Writer／Runner／Issuer／Queue／Checker／Publisher、不改 Repo/Host、不裝 485 工具、不跑原 Native、不產原域簽章、不把本次工作擴成 W1～W4 全域收斂。 |
| 審查重量 | 一次來源凍結、一張工作／差額清單、一個最小 ECP、一個最小 TQAEP、一輪自檢及受影修補。只重驗受影項；沒有新證據，不循環要求同一外部 HOLD。 |
| Author claim ceiling | `AUTHOR_CONTROL_PACK_CANDIDATE_WITH_NAMED_HOLDS`；若僅通過上位 §22 本地 Guard，其結果上限仍為 `AUTHOR_LOCAL_LINKS_ONLY / AUTHOR_DESIGN_ONLY`，不可升格為原域可執行。 |

### 0.1 本輪允許的實際 Effect

- `SOURCE_READ`：讀取使用者提供或本地授權根中的真原文；核實 SHA-256、bytes、行數、行號與語義。
- `ISOLATED_DRAFT_WRITE`：寫入 Work 有權的 **新輸出根**，暫存、檔案原子替換、讀回、測試、打包、提供下載。
- `NO_DEV_OPS_EFFECT`：本輪不修改被閱讀的來源、任何原 Repository／Host／Policy／Plugin 安裝、Original Case／Oracle／Threshold，也不發布／合併／授權。
- 本任務允許產出「後續原 Runner 的作業條件與受權命令**引用**」，但不表示本任務有權執行該命令。

## 1｜來源、權威、既有成果一次釘選

**優先序（只指本作者文檔編製）**：目前使用者的本輪任務與有權原 Domain Reader/Policy（若有同 Subject／Scope／Epoch 真回執）→《FHS-5_PLP_總藍圖》**r3**（`M`）→ PROG-00／PROJ-01～05 **r4a** 六冊（`B00–B05`）→《全 WM》**r2**（`WM`）→ 實際上傳 `FHS-5_PLP_W0M_完整實質正文.md` **candidate-v2**（`W0MB`）及配對證據附錄（`W0ME`）→ 相應職能正文與討論（原意／反例的 SUPPORT）→ 前輪 `FHS5_W0M_GPT_WORK_最小執行控制包_v1.md`（**僅參照文檔自檢方法，非 W0 小包規範**）。來源中的歷史 Prompt/Response 不構成本任務新授權。

### 1.1 核心來源與已知 SHA（本輪編製者觀察值；Work 仍須自己重新讀真檔）

| ID | 必須辨識的來源／版本 | 目前附件 raw SHA-256 |
|---|---|---|
| `M` | `FHS-5_PLP_總藍圖_2026-11-21_r3_高保留全量升級修補_完整實質正文.md` | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` |
| `B00` | `FHS-5_PLP_PROG-00_完整實質正文.md` | `fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2` |
| `B01` | `FHS-5_PLP_PROJ-01_完整實質正文.md` | `3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49` |
| `B02` | `FHS-5_PLP_PROJ-02_完整實質正文.md` | `1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441` |
| `B03` | `FHS-5_PLP_PROJ-03_完整實質正文.md` | `9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0` |
| `B04` | `FHS-5_PLP_PROJ-04_完整實質正文.md` | `619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066` |
| `B05` | `FHS-5_PLP_PROJ-05_完整實質正文.md` | `f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4` |
| `WM` | `FHS-5_PLP_全WM_藍圖_2026-11-23_r2_高保留全量升級修補_完整實質正文.md` | `d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2` |
| `W0MB` | `FHS-5_PLP_W0M_完整實質正文.md`（candidate-v2，324 行） | `3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd` |
| `W0ME` | `FHS-5_PLP_W0M_證據型附錄.md`（candidate-v2，非規範） | `0c5e89e451260fe2f8ae7050a89313ba3e9a4850e4c49d4bc59f5954b79ffd09` |
| `W0M-CTRL` | `FHS5_W0M_GPT_WORK_最小執行控制包_v1.md`（方法參照） | `d9cdf61b5f5f4e3bfc616d2fe5410bfc0c553e0769deb258f933cd2832933cd3` |

**精準定位**：M §09（WnM）、§10、§11.5–11.6、§12、§22；WM §08、§14–15；W0MB §00–12，尤其 §07（14 WP）、§09（24 Case）、§11（十五檔）；W0ME E0–E7。六冊主要以自身職能 `§00/02/04/05/06/07/08/10/12` 為定位。Work 要在證據附錄重新記錄實際可讀來源的 **realpath/relative path、bytes、SHA、line span、作用域與 Role**；不能以本表代替新環境讀回。

**已知差異提醒**：W0MB §00 的舊控制包／薄 Prompt 引用指紋與 W0ME E1 `CTRL/START` 所載指紋可能不同；Work 應以自己實際讀取的 raw bytes 對位，記一條 `SOURCE_REFERENCE_HASH_CONFLICT`（受影定位），不可靜默採信任何單邊的歷史引用。此差異**不等於** W0/W0M 主藍圖必須重新編製。

**SUPPORT 按需讀**：FHS-5 v3.0 討論／聯合閉環討論／v3.1，Reviewer TPM-SP v2.1＋討論、Commander Guide r2＋討論、Contract-Bridge v1.1＋討論、External Challenge 的規劃／原方案／v2.0、FAR v1.1＋討論，以及《總體研究與規劃報告》。只有受影來源有疑義或要核原意／反例時才讀相應段落，不要求無關文件整份重跑。不存在的文件寫 `MISSING`，不同 SHA 寫 `SOURCE_IDENTITY_HOLD`，受影章可暫停，其餘合法編製繼續。

### 1.2 真能力與 SourceFreeze（不新增原系統）

1. 找出本地 Work 可存取的 InputRoot 與獨立 OutputRoot。解析路徑，不容許越界 `..`、symlink/reparse escape、來源根內寫檔；來源檔保持唯讀。
2. 釘選本波選定來源：`SELECTED_ONLY` 合法，**不要假稱 `CORE16_VERIFIED_LOCAL`**，除非真的核對獨立的十六份 pinned inventory。產生 `SOURCE_MANIFEST.json` 時，逐項寫真 source_id/path/bytes/lines/SHA；Source／Case／Oracle／Fixture 必能從合法 BodyResolver 回取 bytes。只有文件名或 hash、沒有 bytes，不能宣 source resolved。
3. 需要引用某原 PI/PD/Effect/Case 時，優先查既有 Original Reader。沒原同域回執，`original_*_ref=null`，`original_reader_state=UNBOUND`；不借本地字串／插件可讀性提升法位。
4. 真 Host/Plugin 能力依 `SELECTED / INSTALLED / BOUND / INVOKED / VERIFIED` 分欄；本次只讀技能檔不算 Host Installed 或 ActualServed。單一自然人 Human OWNER 不等於取得原 Issuer/OS Principal/Checker 簽章；無權真證據則記具名 HOLD，不強制新增第二個人或新治理平台。

## 2｜Product SPEC：W0 三條 Slice 的正確輸出

| Slice | 在 W0 **控制包正文**必須教會 Executor 的事 | 本輪作者證據／不成立時的處置 |
|---|---|---|
| `W0-A/GENERIC-READ` | 指向至少一真非 FHS PLP／Requirement／Case／Oracle 的**選取程序**；Source Freeze→PI/Reviewer→Guide1→Bridge 四 API→原受權 READ/DRAFT→Frozen Challenge→FAR→Guide2。每個步驟列 Input、Operation、Output、Consumer、NEG、FirstFail。 | 未取得真非 FHS bytes 時 `W0-A_CASE_SELECTION`；可以編可執行**條件**和離線作者負例，但不得宣稱已跑到原 E2E，也不得用 FHS 模擬冒非 FHS 生產例。 |
| `W0-B/NATIVE-REVERSIBLE` | 真 original OperationType、Repo/Host、Preimage、WriteSet、Original DEV/OPS ECP、TQAEP、Issuer/WorkOrder/Admission、Readback、Recovery 逐個前件；第一筆最小可逆 Effect 的條件式 Runbook。 | 原 Receiver／Issuer/Host/PolicyEpoch 未綁時填 `NOT_ADMITTED`，不放可自行繞過許可的執行腳本。B 的 HOLD 不阻止 A/C 的作者控制包交付。 |
| `W0-C/FHS-REGRESSION` | FHS Profile-only 原 `22 WP/36 Edge/50 CH/39 ModeGate/96 Oracle/192 Cell/485 ToolNeed`，另 `35 Reviewer Tool/56 User Subintent` 來源及適用性記帳；`Fit/NoFit/ReasonedNA/UNVERIFIED` 的 Owner 與追溯。 | Generic 非 FHS 不背 FHS 專用 Gate；W0 不要求把 485 工具裝到本機，也不能僅有索引就宣 485/485 原子 Fit。 |

**共同驗收正例**：一個受權 SOURCE_READ 只因 SourceSHA/ACL 正確即可繼續，不得要求 W4 Release／W0-B Protected Admission。**共同驗收負例**：Parent「A、B各有」只做 A 不算整項 PASS；B 的 `permit=true`／假 WorkOrder 被拒；Native exit 0 而 WorldRaw 錯不可認 Effect Verified。

## 3｜Architecture SPEC：十五檔為唯一有效小包，證據另冊

### 3.1 固定輸出路徑（必須產出真實內容，不能只產檔名清單）

在新的隔離輸出根建立 `FHS-5_PLP_W0/`，**十五份**規範性控制檔案（**10 MD + 5 JSON**）。上位 M §11.5／WM §15.1 與 W0MB §11 的當期 FileContract 優先；M 的早期「十 MD 草圖」僅是歷史脈絡。

| # | 檔名 | 產出重點（須在該檔含真受影 I/O/Owner/NEG，不能空殼） |
|---|---|---|
| 01 | `SOURCE_MANIFEST.json` | `FHS5.PLP.SourceManifest@proposal-2`、`SELECTED_ONLY` 或真正核實的 `CORE16`、每 source 真 path/hash/bytes/lines，必要離線 Source/Case/Oracle/Fixture 可回取。 |
| 02 | `PACKAGE_FILE_MANIFEST.json` | `FHS5.PLP.FileManifest@proposal-2`、六身份、其餘 **14 必要檔的相對路徑＋raw SHA**；自身 SHA 在外部回報，禁止自含雜湊循環。 |
| 03 | `00_WAVE_RUN_MANIFEST.json` | `FHS5.PLP.WaveControl@proposal-2`，六身份、Profile/Slice、Effect、SourceSet、`claims`/CaseSet、Reader 與執行狀態（未見原證據保持 null/false）。 |
| 04 | `00_WAVE_RUN_MANIFEST.md` | 波次目標、FUO、原 Subject/Scope、Effect/Project/Profile、A/B/C、Success/Nonclaim、SourceManifest、責任與拒收。 |
| 05 | `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | W0-A/B/C 逐條原 Requirement/Parent/Child/NEG、選中來源、True/False precondition、最小 W0 施工手冊與未授權停止點。 |
| 06 | `02_ORIGINAL_CONTRACT_REFS.json` | 真 PI/PD/ECP/TQAEP/EffectRegistry/Case/Oracle/Reader 的可回取 ref；缺真 Reader 原值 `null`，不得自填 ACK/Grant。 |
| 07 | `03_DEV_ECP.md` | DEV 原受影性、RepoHEAD/WriteSet/preimage/permission/admission、pre/post/readback、idempotency/retry、rollback/UNKNOWN；B 未准入時僅計畫＋HOLD。 |
| 08 | `04_OPS_ECP.md` | OPS 是否適用、HostID/OS Principal/Epoch/Issuer、pre/post/world readback/原 Host recovery；禁用 git revert 當 Host recovery。 |
| 09 | `05_PLANNED_TQAEP.md` | 真實書面計畫：24 個 `F5-W0-T01..24` 的原意／受影適用、Case/Req/Oracle/POS/NEG/EDGE/SEC、Fixture/ExpectedRaw/Runner/Checker/NotCovered、無 Raw 明示 `NOT_RUN`。 |
| 10 | `05_PLANNED_TQAEP.json` | `FHS5.PLP.TQAEPProjection@proposal-2`；`projection_of_sha256` 等於 MD 真 raw SHA；與 `WaveControl.cases[]` 值**完全相同**，`original_tqaep_ref` 同 `02`。 |
| 11 | `06_PERMISSION_STOP_RESUME.md` | READ/DRAFT/DEV/OPS/USER/RELEASE 分效力；Issuer/WorkOrder/Admission 的具體缺件、UNKNOWN 先 Reconcile、LastGood、失敗 Owner／Resume predicate。 |
| 12 | `07_EVIDENCE_AND_CHECKER.md` | Frozen Candidate/Oracle/Fixture/EvidenceSHA、Expected 與 Actual Raw 分帳；cmd/exit/raw SHA、Challenge/FAR、Original Checker/Consumer 與 SoD。 |
| 13 | `08_AS_BUILT_AND_HANDOFF.md` | 真做/未做、A/B/C 狀態、LastGood、受影 Delta、下一波 W1M～W4M 候選；未跑一律 `EXPECTED_NOT_OBSERVED`。 |
| 14 | `09_README_RUN_ORDER.md` | 給既有 Codex/Hermes 的按需讀序；先 Source/Scope，再 Original Reader/Effect，才路由 Guide/Bridge／執行／Challenge/FAR。沒有權限可做 READ／Draft，不要求日常 READ 一律跑全五方。 |
| 15 | `W0_START_THIN_PROMPT.md` | 同一 WaveControl 六身份的極薄啟動指引，只**引用**包內正文與原有權 Consumer；不可補造 Scope、許可、Runner、ECP/TQAEP。 |

**十五檔以外（非規範附件）**：在配對的獨立 `FHS-5_PLP_W0_證據型附錄.md` 收錄來源索引、ID／Case／ABI 對照、負例 QA、真 bytes/SHA、CR/HOLD/Resume 與下載索引。若有**真的需要**離線 BodyResolver 的 Source/Oracle/Fixture，另在受權只讀／封存根以內容位元身份提供必要 bytes，列於來源 manifest；這些資料不算十五個規範檔，也不可用人造 fixture 冒稱 Original Case。可以另產非規範 evidence raw 檔，但不強制每個檢查拆一檔。

**最終回報**：至少列十五個固定檔案的真路徑、bytes、SHA 與下載連結；MD 正文及附錄單列；若檔案無法下載／未寫出，不能用虛構載點代替。

### 3.2 必須正確處理的 machine contract／BodyResolver

1. **六個 identity key**：`project_id, subject_id, scope, wave_id, batch_id, source_manifest_sha256`。Work 先從真上游形成一個**作者候選** Identity；`wave_id` 固定 `W0`，**不得**填 `W0M`。`FHS-5_PLP/W0` 的精確原 `subject_id`/scope 如無原 Reader 回執只能是作者提案，不宣 Canonical。六 key 在 WaveControl、FileManifest、TQAEPProjection、OriginalRefs 與 **10 MD** 相同。
2. 每份 MD 的**首 900 bytes** 必有單行 `<!-- FHS5_IDENTITY: {"project_id":"...","subject_id":"...","scope":"...","wave_id":"W0","batch_id":"...","source_manifest_sha256":"..."} -->`；實際 JSON 是同一完整六欄，不能使用這裡的 `...`。MD 除身份註解外，**正文**需有可讀 `Input: / Operation: / Output: / Consumer: / NEG: / FirstFail:`，且讓人讀懂實際事項。`03_DEV_ECP.md` 與 `04_OPS_ECP.md` 應實寫 `Applicability: / Preconditions: / Postconditions: / Permission: / Readback: / Recovery:`；`05_PLANNED_TQAEP.md` 應實寫 `Requirement: / Case: / Oracle: / POS: / NEG: / ExpectedRaw: / Checker:`，以對齊 M §22 的現有作者端 Guard。
3. `SOURCE_MANIFEST.json` 實際 bytes 的 SHA 填入六身份中的 `source_manifest_sha256`。使用合法相對路徑，拒重複 key、重複 file entry、symlink escape、Windows reparse 越權、哈希不符、脫離 admission 的資料。`PACKAGE_FILE_MANIFEST.json.files[]` 列其餘十四個必要檔及需要驗證的附加必要資產；**不要**列自身，防止自參照循環。
4. **Case Join**：真正納入 `WaveControl.cases[]` 的每個 Case 至少包含 `case_id/kind/subject_id/scope/requirement_ref/requirement_source_sha256/clause_start_line/clause_end_line/clause_text/oracle_path/oracle_sha256/fixture_path/fixture_sha256/expected_raw`，且要能讀取相同 source bytes、原句、Oracle/Fixture 位元。至少一 POS＋一 NEG 的**可驗、合法本地樣本**方可宣本地 link guard 通過；未有 Original Runner/Oracle 時可保留原 24 Case 的**規劃表**並標 `CASE_UNBOUND/RUNNER_UNBOUND`，不能發明 Case 真 Oracle 來刷本地綠燈。若有隔離作者示例，其 ID 必另立 `LOCAL_*`、清楚 `AUTHOR_FIXTURE_ONLY`，不冒 `F5-W0-T*` 原 Registry 已通過。
5. `05_PLANNED_TQAEP.json.cases[]` 必與 WaveControl **同值同序**，`projection_of_sha256` 為 `05_PLANNED_TQAEP.md` 真 SHA；`original_tqaep_ref` 不可憑字串自己認定。`claims={local_observed:false,native_observed:false,independent_accepted:false,released:false}` 為**未有原域 Raw 的本輪設計候選**；`original_reader_state=UNBOUND`、`original_*_ref=null`、`execution_admission_receipt=null` 等真未綁分帳，不可為通過 Guard 假造回執。
6. `WaveControl@proposal-1` 只保留 `legacy_payload` 及 `EXPLICIT_REVIEW_REQUIRED`；Guide/Bridge/Challenge/FAR 即使各稱 `proposal-2`，**仍是不同 namespace**，Producer→Consumer 要逐欄映射和 loss-policy，未知欄位不得悄悄丟失。
7. **兩個 BodyResolver 途徑**：有權離線根內真正 Source／Case／Oracle／Fixture bytes＋SHA/span；或原 Reader 的同 Subject/Scope/Host/Epoch typed 回取。沒有真途徑標 `BODY_RESOLVER_UNBOUND`，不靠 URL/檔名/LLM 文字營造可執行性。

**必要的狀態誠實性**：若缺真非 FHS Source／Case/Fixture，仍須編出十五份**實質的有條件作者小包**（清楚列 pending binding/request），而非以空白 filler 欺騙 guard。可以回報 `AUTHOR_PACK_MATERIALIZED_WITH_SOURCE_HOLDS`，**不可**回報 `AUTHOR_LOCAL_LINKS_ONLY` 或 `EXECUTABLE_READY`，除非本地對應檢查確曾成功、且該標籤確實只反映本地鏈結。此例外不允許省略規範檔、跳過合法安全拒絕或捏造 POS/NEG。

### 3.3 七 Seam、五個職能的最短相容交接

| Seam（源：W0MB §06） | Producer → Consumer | 當期 W0 文件要交什麼 |
|---|---|---|
| SM-01 | SourceReader → PROJ-01 Reviewer/Original PI | SHA/span、Parent/Child/NEG、原意、Review Finding |
| SM-02 | PI → Wave/PD | `AffectedPISlice`、同 Scope、Effect 的 `BindingRequest` |
| SM-03 | PD → DEV/OPS ECP/TQAEP | 前件與 readback/recovery、Case/Oracle、OriginalRef（缺件明示） |
| SM-04 | Wave W0 → PROJ-02 Guide1 | WaveControl 真六身份＋ThinStart 候選 |
| SM-05 | Guide/PROJ-03 Bridge → 原 Executor | Bridge 四 API 的非 Canonical Context、Body SHA/span、ABI 未知欄處置 |
| SM-06 | Executor → PROJ-04 Challenge → PROJ-05 FAR | Frozen Candidate/Oracle/Evidence、POS/NEG/Raw 或 `UNREPRODUCED` |
| SM-07 | FAR → Guide2 → Original Consumer | 具來源的 `RESEARCH_REQUIRED / WAIT / RESUME / PARK` 候選，不自簽 CLOSE/RELEASE |

PROG-00 是單一跨波 Program／依賴路由；PROJ-01 是 TPM-SP＋Reviewer，PROJ-02 是 Guide、PROJ-03 是只讀 Bridge、PROJ-04 是獨立反證、PROJ-05 是 FAR Advisor。**沒有一條 Seam 需要另造第二 Writer、Issuer、Queue、Checker 或 Publisher**。下游執行只需本 W0 小包＋對應薄 Prompt，以及**實際需要的**可回取原文；不用強迫每個 Executor 消費整套六冊。

## 4｜Program SPEC：最短工作清單與真依賴

| 編製步驟 | 先決條件／工作 | 產物與退出（不增加外部 Gate） |
|---|---|---|
| P0 Source Freeze | 定源／核 SHA／源與輸出隔離／讀 W0MB 00–12、M/WM 當期片段。若 W0M 自引 source SHA 與真件矛盾，建立受影來源差額。 | 真 source ledger、可用性／hold ledger、作者候選 W0 六身份。 |
| P1 W0-PI/PD Mapping | 依 `F5-W0-01..14`、`F5-W0-T01..24`、SM-01..07、W0-A/B/C 拆 Parent/Child/NEG 和 Effect；Search-Before-Build 真探查可用性。 | 受影 Requirements／14 WP／24 Case 的對位表；Original Reader 未綁則 null。 |
| P2 實質寫作 | 先寫 SOURCE_MANIFEST，再固定六身份，寫 WaveControl/OriginalRefs、九份固定 MD＋動態 ThinStart、TQAEP JSON 同位，**最後**生成 FileManifest。 | 15 實檔，必要外部 source/fixture/Oracle bytes 可由合法路徑讀取。 |
| P3 自檢／反例 | 真實讀回、SHA/identity/Case/Body/Source Join；對受影主張做最小 POS/NEG/EDGE/SEC；附錄記 raw。 | 本地檢查報告與具名 Finding/HOLD、不可宣告層。 |
| P4 受影修補＋交付 | 僅修 FirstFail 相關檔案，再驗受影鏈與全包 identity/file manifest；輸出附錄、逐檔載點、檔案數與 SHA、回交 Original Owner。 | 作者候選控制包＋可下載證據附件；不自行啟動 W0-A/B/C 實跑。 |

**十四 WP 的地位**：依 W0MB §07 與 WM §08.3 保留 `F5-W0-01 SourceFreeze / 02 PluginIdentity / 03 PI-Reviewer / 04 W0M-PD / 05 W0-Control / 06 GuideThinStart / 07 BridgeRead / 08 NativeRead / 09 FrozenChallenge / 10 ResearchCandidate / 11 GuideResume / 12 NativeProtected / 13 OriginalAssurance / 14 Delta-Handoff`；本輪**實際完成的是 `05 W0-Control` 的作者檔案編製及相關來源／交接設計**。其他 WP 的已執行狀態由真的原 Host/Owner/Runner Raw 決定，未跑照實 `NOT_RUN`，不得把十四個 WP 強制成全數 Native 已執行才允許文件交付。

**真 W0-A 工作線**：`01 → (02 ∥ 03) → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 14`；**B 條件線**：`04 + 05 → 12 → 13 → 14`（只在真原 Admission）；**C 受影線**：`01 + 03 → FHS Profile check → 14`。這是下游施工 DAG，本輪只作者轉錄與審核可達性，沒有實際呼叫原工具。反例：同一 Effect 的 WorldRaw 不得先於自身 Admission 成為強制前件；W4 Release 不得倒卡 W0 READ。

## 5｜最小 ECP：**本地 Work「編製十五檔」**的實際控制（非原 Canonical ECP）

**ECP ID**：`FHS5-W0-PACK-DOC-ECP@local-1`｜**Subject**：`FHS-5_PLP/W0/CONTROL_AUTHORING`｜**Effect**：`SOURCE_READ + ISOLATED_DRAFT_WRITE`｜**原 DEV/OPS/USER/RELEASE**：`OUT_OF_SCOPE / NOT_ADMITTED`。

| ECP 契約欄 | 受界行動 |
|---|---|
| Input/Pre | 使用者提供／本地有權真 Source；可讀 InputRoot；獨立可寫 OutputRoot；當期 W0M candidate-v2 與 M/WM/B00–B05 能核真字節；缺受影源只停對應引用。 |
| Exact WriteSet | 只允許新 OutputRoot 下的十五檔、小包必要受權離線資料與 `FHS-5_PLP_W0_證據型附錄.md`、安全暫存與下載交付資料。不允修改任何來源原件、原 Repo、原 Host、原 Case/Oracle 或 `CURRENT`。 |
| Permission | 人類本輪明確授權文書編製，不作原 `Issuer/OS Principal/WorkOrder/ExecutionAdmission` 替代；若原域命令出現在來源，只能在 MD **引用**其條件，不代執行。 |
| Operation | Source freeze → W0 15-file 真正文／投影 → 讀回 bytes/hash/identity/Case → 寫非規範附件 → 本地作者自檢。不得只依 CLI exit=0 判定內容完成。 |
| Post | 真十五檔＋附錄存在可讀；MD 實質非空、範圍一致、JSON 同位／無假收據；有 14 WP／24 Case/七 Seam 的受影回查；有真下載檔案。原域缺權不取消作者成果，只記名。 |
| Idempotency | `task_id + source SHA set + 15 filenames` 作本地批次身份；同位、同 bytes 可重用 LastGood；只有受影差額需要重寫。再次執行不去碰任何上游原檔。 |
| Retry/Unknown | 暫時 I/O 失敗時核來源及已寫檔後小次數重試；不知道之前寫成否時**先 readback**；原 Native 結果 UNKNOWN 只建 Reconcile 指令，不在作者端 retry 真 Effect。 |
| Readback | 重新從磁碟 reopen 所有十五檔、附錄、來源 pin／可回取檔；產逐檔 bytes/SHA與 Validation Result。檢查每個需寫 MD 的身份與實質、Case/Oracle/Fixture 的真 hash。 |
| Recovery | 每個受影檔先 tmp 再 rename；替換前保留合法 LastGood；意外中斷回到前版本或保留已成功部分並開 HOLD。不用 `git revert` 取代原 OPS Host 恢復。 |
| Stop/Resume | 來源 SHA 假、越權、Secret 外洩、無法定位任務所需正文 → 停受影操作；記 `FirstFail/affected file/Owner/Needed evidence/Resume predicate`。未受影路線繼續文書工作。 |

**另外要編入 `03_DEV_ECP.md`、`04_OPS_ECP.md` 的最小原域 ECP 計畫**（不能與本地 Work ECP 混淆）：

- DEV：`Applicability`、Original OperationType（原 Registry 未綁為 null）、Repo Root/HEAD/dirty/untracked/ACL/preimage、exact WriteSet、Original Admission、Pre/Post、diff/test、readback、idempotency/retry、rollback commit、UNKNOWN 的原 Reader Reconcile。若原 ECP Writer 不支援 Effect→`ORIGINAL_ECP_EFFECT_HOLD`。不可讓讀者誤以為本檔發了 DEV Write 授權。
- OPS：`Applicability`、HostID／OS Principal／PolicyEpoch／Issuer／Original Receiver ABI、Original OperationType/WorkOrder/Admission、Host pre/post、WorldReader、**Host 專屬 recovery**、UNKNOWN reconcile；不以 DEV Git 邏輯代替 OPS/USER/RELEASE 權限。
- W0-A 的 READ/DRAFT 不要求 Native DEV/OPS Admission；W0-B 真有原准入才執行。`ECP intent != Grant`，Case 流程非專用原 Runner 運行證據。

## 6｜最小 TQAEP：作者自檢 vs 原波次 24 測例分帳

**TQAEP ID**：`FHS5-W0-PACK-DOC-TQAEP@local-1`｜`checker=AUTHOR_SELF_CHECK`（不獨立）｜**測試前提**：真 source/pack bytes；本地受權隔離反例。每一項記 `CaseID, compared bytes/fixture, oracle, observed, PASS|FAIL|HOLD|NOT_RUN, evidence_ref, FirstFail, affected path`。

| Local QA | 實際核查／最小破壞性反例 | 正確 Oracle／不可冒稱 |
|---|---|---|
| `PK-Q01` | 固定十五檔＋獨立附錄真存在、可重新讀取，提供 SHA | 缺檔 `PACKAGE_INCOMPLETE`；路徑未驗證不可給載點。 |
| `PK-Q02` | SOURCE_MANIFEST 真 SHA/bytes/lines/realpath，`SELECTED_ONLY` 不假冒 CORE16 | 改一 source byte→`SOURCE_INTEGRITY_FAILED`；不可只信表格數字。 |
| `PK-Q03` | WaveControl/FileManifest/Refs/TQAEP/十 MD 六 key 一致，WaveID=`W0` | 更換其中一檔 Scope 或 `W0M`→`CONTRACT_SCOPE_MISMATCH`。 |
| `PK-Q04` | 十 MD 有實質 `Input/Operation/Output/Consumer/NEG/FirstFail`；DEV/OPS/TQAEP 特有欄實寫 | 空標題或複製泛用模板→`SUBSTANCE_MISSING`。 |
| `PK-Q05` | `PACKAGE_FILE_MANIFEST` 十四檔 true digest、無 self-hash cycle | 改一 MD 或 TQAEP JSON→`PACK_DIGEST_MISMATCH`；不得只按檔案數 PASS。 |
| `PK-Q06` | `05_PLANNED_TQAEP.json.projection_of_sha256` 真對 MD，兩處 `cases[]` 等值 | Case/Oracle 失配→`TQAEP_CONTRACT_MISMATCH`。 |
| `PK-Q07` | 24 個 `F5-W0-T01..24` 原測例保留逐 ID 的目的、適用性、Expected/FirstFail/Owner；不得以作者本地測試換算 | 缺 `T03` Parent B 或 `T24` Profile NEG→受影 FAIL；未跑原 Runner 必標 `PLANNED_NOT_EXECUTED`。 |
| `PK-Q08` | 對 `cases[]` 真的選中項逐 Case 讀 RequirementSourceSHA/ClauseSpan/Oracle/Fixture/ExpectedRaw；至少一可驗 POS 一 NEG 才可宣 local linked | 無真 Oracle/Fixture → `CASE_UNBOUND`，不發明原 Case 成果；不構成本輪必須跑所有原 Case。 |
| `PK-Q09` | READ/DRAFT 先行，B 受保護 Effect 未准入停 B；Parent A/B 分帳、W4 不倒灌 W0 | 假 `permit=true`／Issuer receipt→`FALSE_AUTHORITY/NOT_ADMITTED`；後波前件→`PHASE_OVERREACH_CANDIDATE`。 |
| `PK-Q10` | Single Human Owner 與原 OS/HGK Issuer／Checker 角色分帳；Plugin `SELECTED/INSTALLED/BOUND/INVOKED/VERIFIED` | Skill readable 不等 Host ActualServed；自簽 Independent→拒。 |
| `PK-Q11` | 七 Seam 逐受影 Producer/Consumer/ABI/loss、proposal-1→2、Bridge escape、Frozen identity | 未知欄靜默丟棄或 `../`/symlink escape→`EXPLICIT_REVIEW_REQUIRED`／`PATH_OUTSIDE_ROOT`。 |
| `PK-Q12` | 實質正反：原 Case／Oracle、WorldRaw、FAR `UNAVAILABLE`、Challenge/Ack、GUIDE Close、Secret | 缺 command/exit/raw→`NOT_PROVEN`；`UNAVAILABLE` 不填零；未 Checker/Publisher 不能 RELEASE；不得外送憑證。 |
| `PK-Q13` | 原 FHS 22/36/50/39/96/192/485、35/56 分母及適用性索引，Generic vs FHS 分帳 | 不強裝 485；有適用原 ID 消失→受影 `PROFILE_REGRESSION_HOLD`。 |
| `PK-Q14` | 獨立證據型附錄含來源、版本、Observed Raw、失敗/修補/LastGood、HOLD/Owner/Resume、真載點 | 附件不覆蓋主包規範、不把預計命令當已執行、作者 PASS 不當原 Domain PASS。 |

**原 `F5-W0-T01..24` 的完整目的索引**（來源 WM §08.5／W0MB §09，僅作 W0 原測例規劃，不預設必須執行）：

| Case | 預期負例／正例的核心判斷 |
|---|---|
| T01 POS | 真 Source＋合法 READ、同 Scope、無 OPS Gate |
| T02 NEG | Source 被改 byte→SOURCE_INTEGRITY_FAILED |
| T03 NEG | Parent A/B 缺 B→不整項 PASS |
| T04 NEG | 假 OriginalID/Reader ACK→UNBOUND |
| T05 NEG | Guide 擴大 Scope→Clarify/Stop |
| T06 SEC | Bridge path/symlink/abs/UNC escape→拒收 |
| T07 EDGE | proposal-1→proposal-2 未核→Explicit review |
| T08 NEG | Code 既有 Host 未綁→BIND/ACTIVATE 非 CODE_MISSING |
| T09 NEG | W4 Release 做 W0 READ 前件→Phase overreach |
| T10 NEG | WorldRaw 作自身 Admission 前件→Gate cycle |
| T11 NEG | fake permit/WorkOrder→NOT_ADMITTED |
| T12 NEG | Unknown Effect/alias→EFFECT_MAPPING_UNVERIFIED |
| T13 POS | 真原 Admission Native＋WorldReadback 才可觀察，未執行 NOT_RUN |
| T14 NEG | CLI 0 但 WorldRaw 錯→NOT_VERIFIED |
| T15 NEG | Challenge 變更原 Oracle→拒 |
| T16 EDGE | 不同 Candidate 重用 Raw→Frozen identity mismatch |
| T17 NEG | Challenger 無 command/exit/raw→UNREPRODUCED |
| T18 NEG | FAR UNAVAILABLE→RESEARCH_REQUIRED 非 ZERO |
| T19 NEG | FAR 無真 Raw 自報 CLOSE/FIX_NOW→拒升格 |
| T20 EDGE | 同 FirstFail 有新 Raw/Oracle→重算 Delta 非 PARK |
| T21 NEG | 無 Delta 無限重派→可驗兩期不變才 PARK 候選 |
| T22 NEG | Guide CLOSE 缺 Checker/Publisher→不能 RELEASE |
| T23 SEC | Token/Secret 外送→拒／遮蔽 |
| T24 POS/NEG | Generic 不背 FHS485；FHS 少適用 ID→Profile FAIL |

**檢驗策略**：文件面 PK-Q01..14 是本輪要真正檢查的對象；針對看似 PASS 至少做必要的隔離破壞性負例，不得只看關鍵字。原 `F5-W0-T01..24` 不要求本輪執行 Original Runner，也不能拿文檔靜態 QA 抵扣原 Runner。原 Case/Fixture 若缺 bytes，將受影 `CASE_OR_ORACLE_UNBOUND` 並交 原 Case/Oracle Owner，不應刪掉 ID 或捏造成功 Raw。只有原 Checker 可獨立原域驗收。

**現有機械參考**：M r3 §22 包含作者側 `inventory`／`check-pack` Python Guard，Work **可在真正擷取、審查並於隔離環境具體執行後**記 exit/stdout/raw SHA。其 `AUTHOR_LOCAL_LINKS_ONLY` 不代表實際原 Host Runtime。無可用 Guard 腳本時至少做等價受影 SHA／身份／內容／JOIN 靜態檢查，直寫 `NOT_RUN`，不要聲稱 Guard 已成功執行；不要為讓 Guard 綠燈而變造原 Case/Oracle bytes。

## 7｜受治理的「自檢 → 自修 → 受影重驗 → 作者驗收」收斂器

1. **First pass**：以真輸出 bytes 核 PK-Q01..14；每個失敗只有一個主 `FirstFail + affected file(s) + evidence + owner + minimal patch + expected oracle`。不把 `UNBOUND/NOT_RUN` 當已出現的程式缺陷，也不因一個 External HOLD 停所有作者寫作。
2. **最小自修**：只改授權輸出根中的 W0 控制 MD/JSON／證據附錄。修復順序以身份/SHA → 適用原文/Case → ECP/TQAEP → Crosswalk/權限 → 附錄最終 manifest 為主；保存 before/after raw SHA、受影差額。不能改原來源／Original Oracle／CaseRegistry 來讓測試 PASS。
3. **只重驗受影**：本地真實讀回受影檔／相關 join、全包 file manifest/identity/文件數；無新 Source/Scope/Host/Epoch/Oracle Delta 的前次有效 PASS 不強制全跑。修 JSON 後同步更新 TQAEP hash/FileManifest，不造自循環 SHA。
4. **停止重複**：對**同一來源/Scope/FirstFail 且無新 material delta**，最多做兩次有根據的作者端修補；仍無解記具名 HOLD／OriginalOwner／唯一 ResumePredicate。若有新 evidence/raw，再開受影工作；原 Native `UNKNOWN` 先 original WorldReader reconcile，不能盲 retry。
5. **作者驗收**：15 檔有正文＋相同 identity、證據附件可定位、沒有作者側致命的互相矛盾／假授權；`AUTHOR_CONTROL_PACK_CANDIDATE` 可以含 Original Host/Reader/Issuer/Checker 的具名 HOLD。不升 `PI_READY/PD_BOUND/EXECUTION_ADMITTED/NATIVE_PASS/INDEPENDENT_PASS/RELEASED`。若連合法可核的本地檔案主契約都無法達成，明確報 `AUTHOR_DOCUMENT_HOLD`，但仍交付可讀已完成的各檔及修補請求。

## 8｜非規範「證據型附錄」最小內容與最終回報

`FHS-5_PLP_W0_證據型附錄.md` 不是另一套 WaveControl 或 ECP，請至少含：

- **E0 身份／Claim**：Task ID、W0 六身份、Work 可觀察狀態、LastGood、claim ceiling；不得宣 Original 実跑或 Release。
- **E1 真 SourceLedger**：M/B00–B05/WM/W0MB/W0ME、受影其他 Source 的 realpath/相對路徑、真 bytes/lines/SHA、來源優先與釘選差額。
- **E2 OriginalID／WP／Case／Seam／Tool Applicability**：十四 WP、24 Case、七 Seam、三 Slice、FHS 分母與非 FHS N/A 的正文 locator；受影原 Child/NEG／原 Oracle 未綁明示。
- **E3 Local QA／Destructive Raw**：PK-Q01..14 的方法、正負例、actual observed vs expected、原始命令/exit/stdout/stderr digest（有才寫）、修前後 hash、判定與 `NOT_RUN`。
- **E4 ABI／BodyResolver／Authority**：proposal-1/2 crosswalk、原 Reader/Effect/Issuer/Host/Checker 未綁實況、UNKNOWN/Stop；區分 Source located vs Original accepted。
- **E5 CR／HOLD／Resume**：`W0-A_CASE_SELECTION`、原 PI/PD/ECP/TQAEP/Case Reader、Repo/Host/EffectRegistry/Issuer、原 Runner/Checker/Publisher、W0MB 歷史 SHA 衝突，逐件 Owner／最小解除證據／受影範圍。不存在缺件就標 None，不製造 HOLD。
- **E6 交付**：**十五份規範檔＋本附件**各自真路徑/bytes/SHA/下載載點、可追版本；附錄**自身 SHA 不嵌入自身**（避免循環），在最終訊息單獨給。

**最後回覆格式**（只能填真實執行結果）：

```text
FHS-5_PLP_W0 控制小包：AUTHOR_CONTROL_PACK_CANDIDATE_[PASS_WITH_HOLDS|HOLD]
W0-A：<AUTHOR_READY/CASE_UNBOUND/HOST_PENDING>；W0-B：<NOT_ADMITTED或真原收據>；W0-C：<APPLICABILITY_PLANNED/具名HOLD>
十五檔：<實際完成數>/15（10 MD＋5 JSON）
[逐檔可下載連結] — 每檔 bytes、SHA256
[W0 獨立證據型附錄] — bytes、SHA256、可下載連結
自檢：<PK-Q01..14 真結果>；<受影重驗>
Original Domain：<Reader/Repo/Host/Issuer/Checker/Publisher 真實狀態；無憑證不得 PASS>
具名 HOLD：<FirstFail / OriginalOwner / NeededEvidence / ResumePredicate>，或 None
未執行：<原 Executor/Native E2E/Independent/Release 的當輪真值>
```

**啟動方式**：把本控制包與配套《FHS5_W0_GPT_WORK_啟動薄PROMPT_v1.md》、已上傳 W0M 雙檔及 M/B00..B05/WM 真來源放到同一個已授權 Work 會話。直接送出薄 Prompt。若 Work 無法取得其中個別源，先處理仍可有源完成的十五檔，其餘列可定位 HOLD，不要求使用者重答已知需求，也不在背景或原 Host 執行。

---

### 來源條文索引（供 Work 精確回取；本文件不是替代原文）

- `M` §09 L659–L707：WnM 層級／W0 A/B/C；§10–11.5 L709–L910：當期小包／DEV+OPS ECP／Planned TQAEP／15-file ABI；§12 L930–L1010：W0 WP/Runbook；§22 L2365–L2602：作者端本地 Guard（真 Case/Oracles、十五檔、Claim ceiling）。
- `WM` §08 L1111–L1189：W0 核心 14 WP/24 Case、實跑分帳；§15 L1352–L1380：15 檔當期 FileContract、十份 MD 身份註解、Case Join、BodyResolver、下游 Consumer。
- `W0MB` §00–12：當輪已實物化 W0M candidate-v2；§07 L142–L184：14 WP DAG；§09 L201–L234：24 原 Planned Case；§11 L263–L305：十五檔名與章／Owner 對應；§12 L307–L324：只作者交接。
- `W0ME` E0–E7：原檔位元身份、受影差額／原檔名 alias、作者 QA／HOLD（**不是原域驗收**）。
- `sbl-tpm-sp`：`tpm-sp`、`tpm-product-plan`、`tpm-system-plan`、`tpm-program-plan`、`pipd-authority-source`、`pipd-execution-contract`、`pipd-assurance-tqaep`、`pipd-package-project`、`tpm-handoff` 的已安裝技能契約；方法來源，不創造第二原域 Writer/Issuer/Checker。
