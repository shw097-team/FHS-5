**FHS-5_PLP｜W0M｜Generic Walking Skeleton／Native Candidate／FHS Regression｜完整實質正文**

**artifact_id**：`FHS5-PLP/W0M/AUTHOR-CANDIDATE-20261123-02`｜**wave_id**：`FHS-5_PLP_W0M`｜**subject**：`FHS-5_PLP/W0M`｜**version**：`candidate-v2`｜**base_sha256**：`8b8145c8ec34d3cfb23b551d3a1cdc7bb340b72d40c73b2947d92fd15d9b4128`｜**supersedes_candidate_sha**：`5ff03a23a0e51788a5f5c08e7692f4881f620fbc7b8717816089ff7fb8797d20`｜**supersession**：`SUPERSEDES_V1_CANDIDATE`｜**日期**：2026-11-23（Asia/Taipei）
**base_artifact_id**：`FHS5-PLP/W0M/2026-11-23-r2`｜**base_sha256**：`8b8145c8ec34d3cfb23b551d3a1cdc7bb340b72d40c73b2947d92fd15d9b4128`｜**candidate_revision**：`2`｜**supersedes_candidate_sha**：`5ff03a23a0e51788a5f5c08e7692f4881f620fbc7b8717816089ff7fb8797d20`｜**supersession**：`SUPERSEDES_V1_CANDIDATE`
**author_scope**：W0-A/B/C 三線的作者設計；`F5-W0-01..14`、`F5-W0-T01..24`；不含 W0 十五檔控制包施工或任何 Native 執行。
**author_state**：`AUTHOR_SELF_CHECK_PASS_WITH_HOLDS`｜**repair basis**：`FHS5-PLP/WM-REVIEW/2026-11-23-r1`（F-01..F-08）
**claim_ceiling**：`AUTHOR_W0M_DOCUMENT_CANDIDATE_WITH_NAMED_HOLDS`｜**not_claimed**：`PI_READY / PD_BOUND / EXECUTION_ADMITTED / NATIVE_PASS / INDEPENDENT_PASS / RELEASED`
**upstream_source_sha256**：`M=2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7`；`B00=fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2`；`B01=3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49`；`B02=1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441`；`B03=9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0`；`B04=619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066`；`B05=f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4`；`WM2=d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2`
**unbound**：原 Repo/Host/EffectRegistry/Issuer/Runner/Original Checker/Publisher 全部未綁；`WM2-E` 已定位並核 SHA（`AVAILABLE_NOT_READ`）。
**evidence_appendix_filename**：`FHS-5_PLP_W0M_證據型附錄.md`

**卷首讀法**：十三章 `00–12` 是本波作者規格；表格中的 `PLANNED/NOT_RUN/UNBOUND` 是實際狀態，不是已完成。任何「PASS」只指作者自檢或來源位元核對，不指原域驗收。來源優先序為 M r3 → B00–B05 r4a → WM2 r2；WM2-E 只 SUPPORT。

# 00｜Identity／Authority

**Input → Design Operation → Output／Consumer／NEG**

本冊是 `FHS-5_PLP/W0M` 的 Wave Master 作者藍圖，`artifact_id=FHS5-PLP/W0M/AUTHOR-CANDIDATE-20261123-02`，`version=candidate-v2`，`base_sha256=8b8145c8ec34d3cfb23b551d3a1cdc7bb340b72d40c73b2947d92fd15d9b4128`，`supersedes_candidate_sha=5ff03a23a0e51788a5f5c08e7692f4881f620fbc7b8717816089ff7fb8797d20，supersession=SUPERSEDES_V1_CANDIDATE`。`WaveID=FHS-5_PLP_W0M`，Profile=`GENERIC_NON_FHS`＋`FHS_REGRESSION`，`author_scope`=W0-A/B/C 三線的作者設計；`F5-W0-01..14`、`F5-W0-T01..24`；不含 W0 十五檔控制包施工或任何 Native 執行。。它承接 M r3 §09.1 的 WnM 十三章契約與本輪控制包 §3，不取代 PROG-00／PROJ-01～05 或原 Canonical PI/PD/ECP/TQAEP。〔M:2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7:L659–L681〕、〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1324–L1350〕

| 身份欄 | 本冊值 |
|---|---|
| artifact_id | `FHS5-PLP/W0M/AUTHOR-CANDIDATE-20261123-02` |
| wave_id | `FHS-5_PLP_W0M` |
| subject | `FHS-5_PLP/W0M` |
| profile | `GENERIC_NON_FHS`＋`FHS_REGRESSION` |
| version／base／supersedes | `candidate-v2`／`8b8145c8ec34d3cfb23b551d3a1cdc7bb340b72d40c73b2947d92fd15d9b4128`／`5ff03a23a0e51788a5f5c08e7692f4881f620fbc7b8717816089ff7fb8797d20`（supersedes v1 candidate） |
| author_scope | W0-A/B/C 三線的作者設計；`F5-W0-01..14`、`F5-W0-T01..24`；不含 W0 十五檔控制包施工或任何 Native 執行。 |
| claim_ceiling | `AUTHOR_W0M_DOCUMENT_CANDIDATE_WITH_NAMED_HOLDS` |
| author_state | `AUTHOR_SELF_CHECK_PASS_WITH_HOLDS` |
| not_claimed | `PI_READY / PD_BOUND / EXECUTION_ADMITTED / NATIVE_PASS / INDEPENDENT_PASS / RELEASED` |
| evidence_appendix | `FHS-5_PLP_W0M_證據型附錄.md` |

**上游來源釘選**：`M`（`2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7`）、`B00`（`fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2`）、`B01`（`3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49`）、`B02`（`1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441`）、`B03`（`9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0`）、`B04`（`619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066`）、`B05`（`f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4`）、`WM2`（`d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2`）；控制包 `05d2c8139bd2d3a6abc86de0f8e700a4d02c1b5b15c3c485a9c3258a5ee7c715`、啟動薄 `ff9a1d50427c96ea10282c22fc0485600807f1d9f52b5bd94168c5d92579d12d`。`WM2-E` 實際存在：`FHS-5_PLP_全WM\藍圖\..._證據型附錄.md`，566626 bytes／1836 行，SHA `0fd5f233ba66589534de328fde03b11bbe619252f0e5aba5d76c79d67e7e3b9e`，本輪 `AVAILABLE_NOT_READ`，只作 SUPPORT。

NEG：以歷史 `FHS_vNEXT/W0` 或舊 `W0` scoped close 取代本 `W0M` 身份；以本檔 SHA 當原 Canonical 收據；把作者 Scope 寫入原 runtime `subject_id`。上述均為 `SOURCE_OR_SCOPE_DRIFT`，只停受影引用，不撤不受影來源。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1111–L1115〕

# 01｜Goal／FUO／Non-goals

**Input → Design Operation → Output／Consumer／NEG**

**Wave Goal**：把 W0 的三條 Slice（A 非 FHS 合法 Source Read／隔離 Draft、B 原准入才可逆 Native、C FHS 原 ID 守恆）編成一份可施工、可否證的 Wave Master 藍圖，作為後續 W0 控制十五檔的作者上位。

**FUO**：FUO-A：一條真 Source/Req→Reviewer→Guide1→Bridge 四 API→合法原 Executor READ/DRAFT→Frozen Challenge→FAR→Guide2 的最小資料鏈設計。FUO-B：真 WorkOrder/Issuer/Repo/Host/ECP/TQAEP 存在時的一筆可逆 Native Effect 設計；否則 `NOT_ADMITTED`。FUO-C：FHS-only 原集合在適用 Profile 下不丟卡，Generic 不背 FHS 485 Gate。

**Non-goals**：

| # | 本波不做 |
|---|---|
| 1 | 不生成 W0 十五檔控制小包（屬後續 W0 任務）。 |
| 2 | 不以本地純函式或模板冒充 Host/Runner E2E。 |
| 3 | 不把 W4 Release 當 W0-A READ 的前件。 |
| 4 | 不要求 Generic 非 FHS 專案安裝 485 ToolNeed。 |

**受影 Acceptance／NEG**：正向必須有同 Scope 的 SourceLocator、ExpectedRaw 設計、Owner/Consumer；負向必須能指出 `AUTHOR_BODY_INCOMPLETE`、`SOURCE_OR_AUTHORITY_DRIFT`、`FALSE_AUTHORITY` 或本波專屬 FirstFail。本輪沒有原 Runtime Raw，所有正向 Acceptance 只到 `AUTHOR_DESIGN_READY`，不升 `ORIGINAL_ACCEPTED`。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1328–L1342〕

Output：`WaveGoalCard` → Program Owner／Wave Curator／下游 Wn 作者。NEG：只寫「完成全部」或無 ExpectedRaw 的泛用 Goal，退回落實 FUO。

# 02｜Affected PI／Original ID／Child／NEG

**Input → Design Operation → Output／Consumer／NEG**

**AffectedPISlice**：只取本波受影的原 Requirement／Child／NEG／Exception 與 Case；未受影項標 `DEFERRED` 或 `REASONED_NA`，不默認 PASS。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1332〕

| 原 ID／集合 | 原義 | 本波受影 | 適用性 |
|---|---|---|---|
| `F5-W0-01..F5-W0-14` | 原 14 個 W0 WP | 全部保留為作者設計分配 | `APPLICABLE`（設計）；Runtime `NOT_RUN` |
| `F5-W0-T01..F5-W0-T24` | 原 24 個 W0 測試 | 全部保留 Expected/FirstFail | `PLANNED_NOT_EXECUTED` |
| `U-011` | A/B 缺 B 不得父項 PASS | 作為 W0-A PI Review 的硬 NEG | `APPLICABLE` |
| `U-017` | 三 Host 分別 Loaded/Invoked/Served | W1M 才做九格；W0M 只交 Host identity request | `DEFERRED_TO_W1M` |
| `U-028` | Hermes Kanban/Delegation/Swarm 三分 | W1M 才做三格 | `DEFERRED_TO_W1M` |
| `U-046` | Author vs Effect 分帳 | W0-A/B/C claim ceiling 主軸 | `APPLICABLE` |
| FHS `22/36/50/39/96/192/485` | FHS Profile 原分母 | 只做適用 Slice 的 ID 守恆與 Fit/NoFit 候選 | `FHS_PROFILE_ONLY` |
| Generic 非 FHS 案例 | A 線真輸入 | 尚未選定 → `GENERIC_CASE_SELECTION_REQUEST` | `UNBOUND` |

**操作**：先由 SourceRef 建 `RequirementUnit`，再按 Parent/Child/NEG 拆原子；「各有／分別／對應」保留 `SPLIT_CANDIDATE`，原 Reader 未回時 `SPLIT_UNVERIFIED`。Output：`AffectedPISlice/Trace` → PD／Reviewer。NEG：Parent 少 B 仍全項 PASS；把 FHS-only ID 套到 Generic；把 `DEFERRED` 寫成 PASS。FirstFail 分別為 `REQUIRED_CHILD_MISSING`、`PROFILE_GATE_DRIFT`、`PHASE_OVERREACH_CANDIDATE`。

# 03｜Search-Before-Build／Existing Capability

**Input → Design Operation → Output／Consumer／NEG**

**Search-Before-Build**：對每個受影能力先查現有 Source／Plugin／Repo／Host／Case／LastGood，再分 `REUSE / BIND / ACTIVATE / REPAIR / BUILD_CANDIDATE`。沒有真探查證據時只能是 `CAPABILITY_UNVERIFIED`，不得直接 `CODE_MISSING`。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1333〕

| 探查對象 | 已知／現有 | 本波決策 | 未探查／NEG |
|---|---|---|---|
| 舊 `FHS_vNEXT/W0` | 已 scoped close，不同 Subject | 只作歷史血緣，不轉授 | 同名 W0 取代新 W0M→拒 |
| `sbl-tpm-sp` 技能 | 本輪可讀 6 份 SKILL.md | 只用方法契約 | Skill 可讀≠Host installed |
| Guide／Bridge 既有技能 | B02/B03 已有作者設計 | W0M 交 identity/Scope，W1M 才做 Host 消費 | 未載入卻宣 served→拒 |
| 原 Repo/Host/W0 Case | 未取得真 probe/Runner | 只交 BindingRequest | 未查即建新 W0 Code→拒 |
| FHS 485 | 只索引，不裝 | 只做受影 Slot Fit/NoFit 候選 | Generic 強裝 485→拒 |

Output：`ExistingCapabilityLedger` → Wave Owner／Executor。NEG：只因文件沒有 ACK 就重造 Runner／Queue／Reviewer；未讀私有 Archive 就宣 NoFit；把「技能可讀」當 Host Installed。FirstFail：`REUSE_NOT_CHECKED`、`PRIVATE_ARCHIVE_UNBOUND`、`HOST_PENDING`。

# 04｜RepoContext／Binding Request

**Input → Design Operation → Output／Consumer／NEG**

**RepoContext**：本輪原 Repo probe 未取得，故 `repo_context=null`。以下是給 Original Repo Owner 的 `RepoBindingRequest`，不是已綁定值。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1334〕

| 欄位 | 本波值 | 說明 |
|---|---|---|
| `repo_context` | `null` | 未取得原 Repo Reader probe |
| `RepoBindingRequest` | `{root:null, head:null, branch:null, dirty:null, acl:null, write_set:[], preimage:null}` | 交 Original Repo Owner |
| `read_scope` | 已授權來源唯讀 | 不等於 Repo write 權 |
| `write_scope` | `[]` | 本輪不寫原 Repo |
| NEG | caller 自填 HEAD/ACL 當已綁 | `PD_UNBOUND` |

**設計規則**：RepoRoot/HEAD/branch/dirty/untracked/ACL/preimage/WriteSet 必須來自原 Repo Reader 的同次 probe；作者只保存 `null` 與 request。Output：`RepoBindingCandidate` → Original Repo Owner／PD Owner。NEG：用 caller 字串 `head` 冒充 live HEAD；把 `repo_context=null` 寫成 `PD_BOUND`；在未准入時給 WriteSet。FirstFail：`REPO_HEAD_MISMATCH`、`PD_UNBOUND`、`WRITE_SET_UNBOUND`。

# 05｜Host／Effect／Admission Request

**Input → Design Operation → Output／Consumer／NEG**

**Host/Effect**：本輪未取得 Original HostID／OS Principal／PolicyEpoch／EffectRegistry／Issuer，故 `host_effect=null`。以下表格只保存受影 Effect 類別與 `HostEffectBindingRequest`。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1335〕

| Slice | Host／Effect | 本波值 | 可否證設計 |
|---|---|---|---|
| A | READ／DRAFT | `effect_class=READ/DRAFT`；`host=null` | 合法 Source Read；不用 Admission |
| B | Native DEV／OPS | `effect=UNBOUND`；`admission=null` | 只交 ECP/Admission request；`NOT_ADMITTED` |
| C | FHS Profile | `profile=FHS_REGRESSION`；`host=null` | 只核原 ID 守恆；不執行 485 |
| NEG | `permit=true`／假 WorkOrder | 拒 | `FALSE_AUTHORITY` |

**規則**：Effect token 只由原 Effect Registry 決定，不由路徑、檔名或相似字串推斷；`permission=true`／`admitted=true` 不是原 Issuer 收據。Output：`HostEffectLedger/Request` → Issuer／Original Host Reader。NEG：作者授權當原 Admission；未知 Effect 默認 READ；把 OPS 的 OS Principal 與 DEV 的 Repo Principal 互換。FirstFail：`EFFECT_UNBOUND`、`FALSE_AUTHORITY`、`PRINCIPAL_DOMAIN_MISMATCH`。

# 06｜Architecture／Seam／ABI／ADR

**Input → Design Operation → Output／Consumer／NEG**

**Architecture／ABI**：本波只使用七 Seam 中適用部分；Producer→Consumer、版本與 Loss policy 如下。`proposal-2` 後綴不構成兼容證明，未知欄位保留 `legacy_payload` 與 `EXPLICIT_REVIEW_REQUIRED`。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1336〕、〔M:2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7:L842–L910〕

| Seam | W0M 適用 | Producer→Consumer | 本波輸出 |
|---|---|---|---|
| SM-01 Source→PI | 全部 | SourceReader→Reviewer | SourceInventory／PIReview |
| SM-02 PI→PD | A/B | PI→W0M-PD | AffectedPISlice／PDRequest |
| SM-03 PD→ECP/TQAEP | B/C | PD→ECP/Case | ECPRequest／PlannedTQAEP |
| SM-04 Wn→Guide | A | W0M→Guide1 | ThinStart 候選 |
| SM-05 Guide/Bridge→Executor | A | Guide→Bridge→Executor | Contract Context 候選 |
| SM-06 Executor→Challenge→FAR | A/B | Executor→Challenge→FAR | Frozen/POS/NEG/NotCovered |
| SM-07 FAR→Guide→Consumer | A/B | FAR→Guide2→Consumer | ThinResume/WAIT/PARK 候選 |

**Trust/ADR**：單一 Human Owner 不自動取得 Issuer／OS Principal／Checker 權；作者文件只可讀 Source，不可寫 Canonical。Output：`WaveArchitectureDecision` → 五 PROJ／Original Consumer。NEG：把兩個 `@proposal-2` 直接互送；丟 unknown field；以 ABI 名稱相同推定 Consumer 已支援。FirstFail：`ABI_LOSSY_CROSSWALK`、`SCHEMA_UNSUPPORTED`、`CONSUMER_UNVERIFIED`。

# 07｜Program DAG／Owner／Edge Type

**Input → Design Operation → Output／Consumer／NEG**

**Program DAG**：下表每個節點標 Owner、前置與邊型別。`HARD_SOURCE_VERIFIED` 只在真的有原 typed receipt 時使用；本輪多數是 `AUTHOR_DOC`／`INFO_ONLY`／`UNVERIFIED`。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1337〕

| WP／節點 | 前置 | 型別 | Owner | 本波退出 |
|---|---|---|---|---|
| F5-W0-01 SourceFreeze | — | HARD_SOURCE | Source Curator | SourceInventory 或 HOLD |
| F5-W0-02 PluginIdentity | 01 | INFO_ONLY | Plugin/Host Owner | IdentityLedger |
| F5-W0-03 PI/Reviewer | 01 | HARD_SOURCE | Reviewer/Original PI | PIReview |
| F5-W0-04 W0M-PD | 02,03 | AUTHOR_DOC | Wave Owner | PD/A-B-C design |
| F5-W0-05 W0-Control | 04 | AUTHOR_DOC | Pack Author | 15-file split |
| F5-W0-06 GuideThinStart | 04 | INFO_ONLY | Guide Owner | ThinStart candidate |
| F5-W0-07 BridgeRead | 06 | INFO_ONLY | Bridge Owner | Context candidate |
| F5-W0-08 NativeRead | 07 | UNVERIFIED | Executor/Host | READ/DRAFT or NOT_RUN |
| F5-W0-09 FrozenChallenge | 08 | UNVERIFIED | Challenger | Frozen/NotCovered |
| F5-W0-10 ResearchCandidate | 09 | UNVERIFIED | FAR | Research candidate |
| F5-W0-11 GuideResume | 10 | UNVERIFIED | Guide/Program | Resume candidate |
| F5-W0-12 NativeProtected | 04,05 | UNVERIFIED | Issuer/Executor | NOT_ADMITTED |
| F5-W0-13 OriginalAssurance | 12 | UNVERIFIED | Original Checker | NOT_RUN |
| F5-W0-14 Delta/Handoff | 11,13 | AUTHOR_DOC | Program Owner | Delta/Handoff |

**原十四 WP 的完整輸入／操作／輸出契約**（不能只留 DAG 節點）：

| 原 ID | 必需輸入 → 作者／原操作 → 可見輸出 | 負例、停止與 Owner |
|---|---|---|
| `F5-W0-01 SourceFreeze` | 核真 Source bytes/SHA/span/ACL、Select set/CORE16 → SourceInventory | 同名異 SHA→`SOURCE_INTEGRITY_FAILED`；Original Source Reader |
| `F5-W0-02 PluginIdentity` | 原 Plugin Manifest、Host 原 Reader → Alias/Selected/Installed/Bound/Invoked | Skill 本地可讀≠Host Serviced；Plugin/Host Owner |
| `F5-W0-03 PI/Reviewer` | Goal、U/Child/NEG/Case→PI 作者 Review/FirstFail/Owner | 少 B Child／假原 Reader→SPLIT/READER HOLD；Reviewer/Original PI |
| `F5-W0-04 W0M-PD` | PI/Source、真環境可見度→A/B/C、Effect、DAG、受影 BindingRequest | 字串 HEAD 冒 `PD_BOUND`→撤回；Wave/Original PD Owner |
| `F5-W0-05 W0-Control` | W0M→15 檔 proposal-2 當波小包、ECP/TQAEP、OriginalRef | 缺檔/空殼/Scope mismatch→`PACKAGE_INTEGRITY_HOLD`；Pack Author |
| `F5-W0-06 GuideThinStart` | 真 W0 identity/FUO/Done/Effect→ThinStart | Guide 擴權→CLARIFY；Guide Owner |
| `F5-W0-07 BridgeRead` | 真離線 Body/SourceSHA/ClauseSpan→非 Canonical Bridge Context／四 API | `../`/symlink／虛假 OriginalID→拒收；Bridge/Host Security |
| `F5-W0-08 NativeRead` | 原 READ/DRAFT 合法許可、Context→真原 Executor command/exit/Raw | Mock／文字回報不當 ActualServed；Executor/Host Owner |
| `F5-W0-09 FrozenChallenge` | Candidate/Oracle/Evidence Frozen、Runner/Fixture→POS/NEG/NotCovered | 無 Runner／改受審 Oracle→UNREPRODUCED；Challenger Owner |
| `F5-W0-10 ResearchCandidate` | 真 Raw/Findings/Original Source→RootCause 候選＋多方案／Typed Status | Source unavailable≠ZERO；FAR/Fabric Owner |
| `F5-W0-11 GuideResume` | FAR Advice＋WorldReader 真 Delta→ThinResume/WAIT/PARK 候選 | 未經原 Publisher 不能 RELEASE；Guide/Program Owner |
| `F5-W0-12 NativeProtected` | **僅真 Admission**、Repo/Host/ECP→受保護可逆 Effect＋WorldRaw | 假 Permit 或不明 OperationType→NOT_ADMITTED；Original Issuer/Executor |
| `F5-W0-13 OriginalAssurance` | 原 Checker/Consumer 真 Case/Raw→同 Scope 原接收 | Advisory/FAR/Maker 自簽→REJECT；Original Checker |
| `F5-W0-14 Delta/Handoff` | A/B/C As-Built/FirstFail/HOLD→AffectedDelta、W1M 候選 | 無真 Delta 反覆重派→停止；Program/Wave Owner |

**DAG 規則**：只允許 `AUTHOR_DOC_ORDER`、`INFO_ONLY`、`HARD_SOURCE_VERIFIED`、`UNVERIFIED` 四類；同一 Effect 的 WorldRaw 不得成為自身 Admission 的前件；W4 Release 不得倒卡 W0 READ。Output：`WaveDependencyGraph` → Program／Pack Author。NEG：cycle、以未來 Release 作前件、把未驗證邊畫成 HARD。FirstFail：`GATE_CYCLE_CANDIDATE`、`PHASE_OVERREACH_CANDIDATE`、`UNVERIFIED_EDGE_AS_HARD`。

# 08｜DEV／OPS Strategy／NOT_ADMITTED

**Input → Design Operation → Output／Consumer／NEG**

**DEV/OPS strategy**：本波只寫適用的 Construction/ECP **計畫**；不是 Canonical ECP，也不是 Grant。所有受保護 Effect 在缺原 Admission 時一律 `NOT_ADMITTED`。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1338〕、〔M:2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7:L1221–L1259〕

| 線 | 輸入 | 設計操作 | 輸出 | 停機 |
|---|---|---|---|---|
| W0-A READ/DRAFT | 真 Source/Case/ACL | Freeze→Review→ThinStart→Context→READ/DRAFT | reader/draft raw 或 `NOT_RUN` | 無 Host/Runner 只停 A 實跑 |
| W0-B Native | Original ECP/Admission/Repo/Host | 最小可逆 Effect→Readback→Recovery | `NOT_ADMITTED`（本輪） | 無原 Issuer 停 B |
| W0-C FHS | 原 FHS ID/Slot | Fit/NoFit/Reasoned N/A | Applicability ledger | 丟適用 ID 停 C |
| NEG | 假 permit／git revert 作 OPS recovery | 拒 | FirstFail | 受影 Slice |

Output：`EffectStrategy` → Original ECP/Executor。NEG：把 ECP 意圖當成已核准；用 `git revert` 當 OPS Host recovery；CLI exit 0 但 WorldRaw 不符仍標 PASS；`UNKNOWN` 直接 retry。FirstFail：`ECP_NOT_GRANT`、`RECOVERY_KIND_MISMATCH`、`EFFECT_NOT_VERIFIED`、`UNKNOWN_RETRY_DENIED`。

# 09｜TQAEP Strategy／Case／Oracle

**Input → Design Operation → Output／Consumer／NEG**

**TQAEP strategy**：以下是本波受影 Case/Oracle/Fixture/ExpectedRaw 的作者計畫。沒有原 Runner／Checker 時全部 `NOT_RUN`／`UNBOUND`；本表不是原 TQAEP。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1339〕、〔M:2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7:L1116–L1131〕

| 原 Case | 類型／注入要點 | 預期正確結果／FirstFail |
|---|---|---|
| `F5-W0-T01` | POS：真 Source+合法 READ | SourceAnchor/Scope 同位、無 OPS Gate |
| `F5-W0-T02` | NEG：Source 改一 byte | `SOURCE_INTEGRITY_FAILED` |
| `F5-W0-T03` | NEG：「A、B 各有」少 B | Parent 不能 PASS，Child 缺件 |
| `F5-W0-T04` | NEG：自造 OriginalID/Reader ACK | `ORIGINAL_READER_UNBOUND` |
| `F5-W0-T05` | NEG：Guide 擴大 Scope | Scope mismatch/Clarify |
| `F5-W0-T06` | SEC：Bridge ../、symlink、絕對路徑逃逸 | Root 外拒讀／不寫 Subject |
| `F5-W0-T07` | EDGE：legacy proposal-1 給 proposal-2 | `EXPLICIT_REVIEW_REQUIRED` |
| `F5-W0-T08` | NEG：有原 Code 但 Host 未 Bound | BIND/ACTIVATE 非 CODE_MISSING |
| `F5-W0-T09` | NEG：W4 Release 倒灌成 W0 READ 前件 | `PHASE_OVERREACH_CANDIDATE` |
| `F5-W0-T10` | NEG：WorldRaw 作同操作 Admission 前件 | `GATE_CYCLE_CANDIDATE` |
| `F5-W0-T11` | NEG：Caller permit=true／假 WorkOrder | `NOT_ADMITTED`，不跑 DEV/OPS |
| `F5-W0-T12` | NEG：未知 Effect token／Alias | `EFFECT_MAPPING_UNVERIFIED` |
| `F5-W0-T13` | POS：真有權 Native + post-readback | 真 World/Repo Oracle/Raw 正確 |
| `F5-W0-T14` | NEG：CLI 0 但 WorldRaw 錯 | 不標 Effect Verified |
| `F5-W0-T15` | NEG：Challenge 修改原 Oracle | Subject Mutation 拒收 |
| `F5-W0-T16` | EDGE：不同 Candidate 重用 Challenge Raw | Frozen Identity 不一致，受影重挑戰 |
| `F5-W0-T17` | NEG：Challenger 無 command/exit/raw | `UNREPRODUCED/NOT_PROVEN` |
| `F5-W0-T18` | NEG：FAR UNAVAILABLE 被填 zero | `RESEARCH_REQUIRED` |
| `F5-W0-T19` | NEG：FAR 自報 FIX_NOW/CLOSE | 缺 Original Source/Raw，不能升級 |
| `F5-W0-T20` | EDGE：FirstFail 同名但有新 Raw/Oracle | 不能直接 PARK；計受影 Delta |
| `F5-W0-T21` | NEG：無 Delta 仍同 Case 無限重派 | 真兩期無變時才 PARK 候選 |
| `F5-W0-T22` | NEG：Guide CLOSE 但 Checker/Publisher 缺 | 不得 RELEASE |
| `F5-W0-T23` | SEC：小包包含 token／secret | 不外送、不記敏感 Raw |
| `F5-W0-T24` | POS/NEG：Generic 不背 FHS 485；FHS 丟適用 ID | Generic 可 READ／FHS 必拒丟 ID |

Output：`WaveAssurancePlan` → Original Case/Checker。NEG：local unit PASS 當 Original Runner；UNAVAILABLE 當 ZERO；改 Oracle/Threshold 使 FAIL 變綠；以作者 `PASS` 字串冒 Independent。FirstFail：`RUNNER_UNBOUND`、`EVIDENCE_LAUNDERING`、`ORACLE_DRIFT`、`FALSE_INDEPENDENT`。

# 10｜Claim／Stop／Resume／HOLD

**Input → Design Operation → Output／Consumer／NEG**

**Claim Ledger**：Author／Original Native／Independent／Release 四層分帳。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1340〕、〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1732–L1810〕

| Claim | 本波可宣 | 不可宣 | 證據 |
|---|---|---|---|
| Source | 8 核心來源＋10 目標 SHA 可核（六冊 R4 的來源清冊另列 B00 E1） | 原 Reader 已接受 | E1 |
| W0-A | 作者設計＋`NOT_RUN` | `OBSERVED_LOCAL_SLICE` | A/B/C slice |
| W0-B | `NOT_ADMITTED` | `NATIVE_PASS` | Host/Issuer HOLD |
| W0-C | `APPLICABILITY_PLANNED` | FHS 485 全 PASS | ID ledger |
| Independent | `NOT_CLAIMED` | `INDEPENDENT_PASS` | Original Checker HOLD |
| Release | `NOT_CLAIMED` | `RELEASED` | Publisher HOLD |

**具名 HOLD／FirstFail／Owner／Resume**：

| HOLD／FirstFail | 真缺口 | Original Owner | 解除最小證據 |
|---|---|---|---|
| `W0-A_CASE_SELECTION` | 真非 FHS PLP/Case/Oracle 尚未選定 | Original Project/Source Owner | 提供一個同 Scope 真 bytes+Coverage 的非 FHS 案例 |
| `R3-CR02` | 原 PI/PD/ECP/TQAEP/Case Reader 未綁 | Original PIPD Reader/Case Owner | 同 SourceSHA/Subject/Scope typed readback |
| `R3-CR03/04` | Repo/Host/Effect/Admission 未得 | Repo/Host Owner、OS Principal、Issuer | 真 HEAD/preimage/ACL、原 OperationType/Admission |
| `R3-CR05` | 三 Host 未 ActualServed | 各 Plugin/Host Owner | 每 Host Loaded/Invoked/Consumed Raw |
| `R3-CR06` | Runner/Checker/Publisher 未簽 | CaseRunner、Protected Checker、Publisher | 同 Candidate/Oracle/Scope 真 Raw |

Output：`WaveGateLedger` → Owner／Guide。NEG：缺原 Effect 卻把所有 Claim 一起停；把 W4 Release 當 W0 READ 前件；以作者自檢簽 Original PASS。FirstFail：`CLAIM_CEILING_VIOLATION`、`PHASE_OVERREACH_CANDIDATE`、`FALSE_AUTHORITY`。

# 11｜Wn Pack Split／Fifteen Files

**Input → Design Operation → Output／Consumer／NEG**

**Wn Pack Split**：以下只是後續對應的 W0～W4 十五檔切分，**本輪不生成十五檔控制包**。每個切分保留 SourceRef、ThinPrompt 與 OriginalConsumer。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1341〕

| # | 十五檔 | 內容 | Owner |
|---|---|---|---|
| 1 | `00_WAVE_RUN_MANIFEST.md` | Wave/Subject/Scope/SourceManifest | Wave Curator |
| 2 | `00_WAVE_RUN_MANIFEST.json` | 同 MD 的資料投影 | Pack Author |
| 3 | `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | Source/Scope/Construction | Source Curator |
| 4 | `02_ORIGINAL_CONTRACT_REFS.json` | Original PI/PD/ECP/TQAEP refs | Original Reader |
| 5 | `03_DEV_ECP.md` | DEV ECP | PIPD/Repo |
| 6 | `04_OPS_ECP.md` | OPS ECP | HGK/Host |
| 7 | `05_PLANNED_TQAEP.md` | Case/Oracle/ExpectedRaw | Case Owner |
| 8 | `05_PLANNED_TQAEP.json` | MD 的 SHA 投影 | Pack Author |
| 9 | `06_PERMISSION_STOP_RESUME.md` | Permission/Stop/Resume | Program |
| 10 | `07_EVIDENCE_AND_CHECKER.md` | Evidence/Checker | Checker |
| 11 | `08_AS_BUILT_AND_HANDOFF.md` | AsBuilt/Delta/Handoff | Wave Owner |
| 12 | `09_README_RUN_ORDER.md` | Run order | Pack Author |
| 13 | `{wave_id}_START_THIN_PROMPT.md` | ThinStart | Guide |
| 14 | `SOURCE_MANIFEST.json` | 真 Source SHA/bytes/lines | Source Curator |
| 15 | `PACKAGE_FILE_MANIFEST.json` | 每檔 raw SHA | Pack Author |

**W0M 對應章／Owner 摘要**（與上表同 15 檔）：

| W0 十五檔 | 內容 | W0M 章 | Owner |
|---|---|---|---|
| 00_WAVE_RUN_MANIFEST.md/.json | Wave/Subject/Scope/SourceManifest | 00 | Wave Curator |
| 01_SOURCE_SCOPE_AND_CONSTRUCTION.md | Source/Case/A-B-C | 02/03/04 | Source/Wave |
| 02_ORIGINAL_CONTRACT_REFS.json | Original PI/PD/ECP refs | 05/06 | Original Reader |
| 03_DEV_ECP.md | DEV ECP | 08 | PIPD/Repo |
| 04_OPS_ECP.md | OPS ECP | 08 | HGK/Host |
| 05_PLANNED_TQAEP.md/.json | 24 T cases | 09 | Case Owner |
| 06_PERMISSION_STOP_RESUME.md | Stop/Resume | 10 | Program |
| 07_EVIDENCE_AND_CHECKER.md | Evidence/Checker | 09/10 | Checker |
| 08_AS_BUILT_AND_HANDOFF.md | AsBuilt/Delta | 12 | Wave Owner |
| 09_README_RUN_ORDER.md | Run order | 11 | Pack Author |
| `{wave_id}_START_THIN_PROMPT.md` | ThinStart | 11 | Guide |
| SOURCE_MANIFEST.json | 真 SHA | 00 | Source Curator |
| PACKAGE_FILE_MANIFEST.json | 檔 SHA | 11 | Pack Author |

**切分規則**：十五檔中的 MD 是實質正文，JSON 是原文 SHA 投影；`05_PLANNED_TQAEP.json.projection_of_sha256` 必須等於 MD 真 SHA；少檔／空殼／Scope mismatch 一律 `PACKAGE_INTEGRITY_HOLD`。Output：`ExecutionPackSplit` → Guide／Pack Author。NEG：把本 WnM 當十五檔已施工；只給檔名不給 ECP/TQAEP 實質；把 WnM 的 SHA 當原 Canonical。FirstFail：`PACKAGE_INCOMPLETE`、`PACKAGE_INTEGRITY_HOLD`、`TQAEP_CONTRACT_MISMATCH`。

# 12｜As-Built／Handoff／Next Wave

**Input → Design Operation → Output／Consumer／NEG**

**As-Built／Handoff**：本冊只完成作者端十三章、受影 PI、Seam/ABI、DAG、ECP/TQAEP 策略、Stop/Resume 與 Wn 切分；未執行任何原 Runtime。〔WM2:d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2:L1342〕、〔M:2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7:L2989–L3016〕

| Handoff 欄 | 值 |
|---|---|
| Kind | `W0M_AUTHOR_CANDIDATE_WITH_NAMED_HOLDS` |
| Next | W1M Host 消費；W2M 受權 Effect；W3M Challenge/FAR；W4M Assurance |
| LastGood | 本對 MD 的 SHA |
| Delta | 無真 Runtime Delta；只有作者設計 |
| OriginalConsumer | Wave Curator／Original PI/PD/Repo/Host/Checker |
| NotCovered | W0-A/B/C 實跑、W0 十五檔施工、Native、Independent、Release |

**下一波／外部 HOLD**：W1M（Guide/Bridge Host 消費）＋W2M（受權 DEV/OPS）＋W3M（Challenge/FAR/Guide2）＋W4M（Assurance）。本冊的 `AUTHOR_BODY_ONLY` 不解除下列任一原域 HOLD：W0-A_CASE_SELECTION；R3-CR02；R3-CR03/04；R3-CR05；R3-CR06。

Output：`WaveClosureAndHandoff` → 下一波 Program／Original Consumer。NEG：Wn 未跑就填 AsBuilt PASS；把本冊 SHA 當 Release；無 Material Delta 重寫整個下一波。FirstFail：`AS_BUILT_OVERCLAIM`、`RELEASE_NOT_CLAIMED`、`NO_DELTA_REWRITE_DENIED`。
