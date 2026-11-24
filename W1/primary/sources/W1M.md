# FHS-5_PLP｜W1M｜Guide／Bridge ABI、Host 消費與 Contract Context｜完整實質正文

**artifact_kind**：`WaveMaster`（Wave-level PD／Program Design Master 正文；不是藍圖、不是 Wn 控制小包）
**artifact_id**：`FHS5-PLP/W1M/2026-11-24-wm-v5`｜**wave_id**：`FHS-5_PLP_W1M`｜**subject**：`FHS-5_PLP/W1M`｜**version**：`wm-v5`｜**日期**：2026-11-24（Asia/Taipei）
**supersedes（本輪實讀）**：`FHS-5_PLP_W1M_藍圖_2026-11-24_r5_完整實質正文.md`；bytes `67149`；lines `816`；raw SHA-256 `ebaab15f49b2dc06e5aa079d8a404635c7cb0422e049285d0e277c2e4ce666ed`
**author_state**：`AUTHOR_SELF_CHECK_PASS_WITH_NAMED_HOLDS`
**claim_ceiling**：`PD_AUTHOR_CANDIDATE`（作者端 Wave Master 候選）；**effective ceiling**：`AUTHOR_DESIGN_ONLY`
**not_claimed**：`PI_READY / PD_BOUND / EXECUTION_ADMITTED / NATIVE_PASS / INDEPENDENT_PASS / RELEASED / MISSION_COMPLETE`
**source_pin_set_sha256（本輪 17 源；演算法見 §00.2）**：`4b08a4583d1788b16ad4337e3a7e81200beb85a26de927576aa86b73f0dc9626`
**supersedes_v4（本輪整合＋覆蓋＋取代）**：`FHS-5_PLP_W1M_完整實質正文.md` v4 `dd50933a0ef886a38a4a873c12b71bc2af78f28b7153e4ef79a6d3fe44d789cb`；`FHS-5_PLP_W1M_證據附件.md` v4 `2a84eea7cca71701417fbe02fdac5a22337732539bf4dffa0b79f79cba5f41c0`
**patch_basis**：審查報告 r1 `bbccfd2c758e26f0b5a176e21204c746f257635377fd5f3a098af4cf0bc4460d`；C4 `19202df1c8dc5498d0095d280fbf9ea32620a81b9b0b54f1e216a67eabece554`
**patch_state**：`PATCHED_FROM_v4_REVIEW_R1`；只修受影層，未重寫核心設計
**review_response_state**：`AUTHOR_REPAIR_CANDIDATE_READY_FOR_REVIEW`（作者端修補完成；非 reviewer 已驗收）
**evidence_appendix**：[`FHS-5_PLP_W1M_證據附件.md`](FHS-5_PLP_W1M_證據附件.md)

**卷首讀法**：本冊是 W1 的作者工程入口。`PLANNED / NOT_RUN / UNBOUND / HOLD` 都是實際狀態，不是修辭。任何「PASS」僅指作者自檢；原域 Reader、Issuer、Host、Runner、Checker、Publisher 的收據一律另計。來源優先序：M r3 → B00–B05 → WM r2 → W0M／W0 PRIMARY → r5 → 本輪 W0 本地實讀。所有引用以 `來源ID:SHA[:span]` 表示；未取得 raw bytes 者寫 `UNBOUND`，不以檔名或相似名稱補位。

---

# 00｜Identity／Authority

**Input → Design Operation → Output／Consumer／NEG**

Input：Owner 的 v4 任務請求、17 個已釘選來源、W0 PRIMARY 實體。Operation：固定 artifact 身份、來源集合與權力邊界，辨識 supersedes 與 LastGood。Output：`WaveMasterIdentity`＋`SourceFreezeManifest` → 下游 W1 Pack Author、Reviewer、原域 Reader。NEG：同名不同 SHA、拿 r4 冒充 r5、把作者檔當 Canonical Reader ACK → `SOURCE_IDENTITY_HOLD`／`FALSE_AUTHORITY`。

## 00.1 身份與效力

| 欄位 | 值 | 說明 |
|---|---|---|
| artifact_kind | `WaveMaster` | 13 章 PD／Program 實質設計；非 `ExecutionPack` |
| artifact_id | `FHS5-PLP/W1M/2026-11-24-wm-v5` | 本輪新批次，不覆寫 r5 |
| wave_id／subject | `FHS-5_PLP_W1M`／`FHS-5_PLP/W1M` | Wn 的 wave_id 可與 WM 不同，見 §11 |
| profile | Guide／Bridge ABI、Host 消費與 Contract Context | 對應 WM r2 §09 |
| author_scope | Guide／Bridge ABI 逐欄轉接、三 Host 逐態、Hermes 三功能、四 API 與 BodyResolver、WM1-P01..06 | 不含 W2 Native 與 W3 Challenge 實跑 |
| author_state | `AUTHOR_SELF_CHECK_PASS_WITH_NAMED_HOLDS` | 作者自檢通過但具名 HOLD 未清 |
| claim_ceiling | `PD_AUTHOR_CANDIDATE` | 可交 Wn Pack Author／Reviewer |
| effective ceiling | `AUTHOR_DESIGN_ONLY` | 不產生 Grant、Native PASS、Independent、Release |
| supersedes | W1M r5（`ebaab15f…`） | 實讀 bytes/lines/SHA 一致 |
| LastGood | W1M r5（同上） | 本檔為新候選；未覆寫 LastGood |
| 本輪輸出根 | `C:\Users\user\Documents\Codex\2026-11-24\sbl-tpm-sp-plugin-sbl-tpm-46\outputs\FHS5_WM_AUTHOR_20261124_v4\` | 受權隔離輸出；未寫 W0、r5 或原 Repo |

## 00.2 SourceFreeze（本輪逐檔重算）

`source_pin_set_sha256` 的演算法：將下表 17 列依 `ID|bytes|lines|sha256` 以 LF 串接（UTF-8、無 BOM、無尾端 LF），再取 SHA-256。這是**作者釘選集**，不是原 Reader 收據。

| ID | 檔／角色 | bytes | lines | raw SHA-256 | 本輪狀態 |
|---|---|---:|---:|---|---|
| M | 總藍圖 r3 完整實質正文 | 325511 | 3016 | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` | `READ_VERIFIED` |
| ME | 總藍圖 r3 證據型附錄 | 2292610 | 7779 | `5d9ac76ae4ff52e8bdf870f65dbec4e1ab70dad80453b3f955c2411b8cf91b85` | `READ_VERIFIED`（按需 span） |
| B00 | PROG-00 完整實質正文 | 79605 | 528 | `fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2` | `READ_VERIFIED` |
| B01 | PROJ-01 完整實質正文 | 48177 | 405 | `3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49` | `READ_VERIFIED` |
| B02 | PROJ-02 完整實質正文（Guide） | 47039 | 398 | `1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441` | `READ_VERIFIED` |
| B03 | PROJ-03 完整實質正文（Bridge） | 39898 | 326 | `9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0` | `READ_VERIFIED` |
| B04 | PROJ-04 完整實質正文（Challenge） | 40665 | 332 | `619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066` | `READ_VERIFIED` |
| B05 | PROJ-05 完整實質正文（FAR） | 51163 | 380 | `f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4` | `READ_VERIFIED` |
| WM | 全 WM 藍圖 r2 | 286201 | 2080 | `d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2` | `READ_VERIFIED` |
| W0MB | W0M 完整實質正文 | 29460 | 324 | `3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd` | `READ_VERIFIED` |
| W1R5 | W1M r5 正文（本檔 preimage） | 67149 | 816 | `ebaab15f49b2dc06e5aa079d8a404635c7cb0422e049285d0e277c2e4ce666ed` | `READ_VERIFIED` |
| W2R5 | W2M r5 正文 | 61479 | 833 | `010664f6dd58ad907d670b0d87c2ff22ec4a39141114bbb3032fb2d63495060a` | `READ_VERIFIED` |
| W3R5 | W3M r5 正文 | 61294 | 842 | `27385c16e1dc5d019f68e721fed57c5032d58d39e3f821b703ad3f55001e6f82` | `READ_VERIFIED` |
| W4R5 | W4M r5 正文 | 76587 | 915 | `3463e7762e74606c38b473cc9ff1031650cae128987e99eaef80e20e4b8574e0` | `READ_VERIFIED` |
| H-CLOSE | W0 PRIMARY 交接 | 2840 | 41 | `994264b1273e7127f032e41c72b7a97b0bf8e30139bcbab20eec1e543b5faeb3` | `READ_VERIFIED` |
| H-PATCH | W0 PATCH-03 交接 | 3291 | 61 | `76091015beab172e6bb85a217f2593f762c2416a2e74e9236a00cd09267f231e` | `READ_VERIFIED` |
| PLAN-HIST | 總體規劃報告 | 48847 | 887 | `b5296d87324e13d1989225e9631c4ac7bfdc4ad3b1a3a2fa1e5abb0b4bfd8587` | `READ_VERIFIED` |

**來源角色與衝突規則**：

1. M r3 是當期上位正文；B00–B05 是 Product／Architecture／Program 六冊；WM r2 是分波與 15 檔接口；W0M 是 W0 基線；r5 是四波直接底本。
2. ME、PLAN-HIST、r5 證據附錄、舊控制包屬**證據／方法／血緣**，不並列第二套規範。
3. 任一來源 raw SHA 漂移，只重開受影 slice；不因單一來源變動撤銷其他已驗來源。
4. 同名不同 SHA → `SOURCE_REFERENCE_HASH_CONFLICT`；不得以「最新檔名」推定內容。

## 00.3 本輪實際讀回（OBSERVED_LOCAL／READ_VERIFIED）

| 觀測 | 實際值 | 狀態 | 消費者 |
|---|---|---|---|
| W0 workspace 可列舉 | `C:\Projects\Agent_Workspace\FHS-5_Workspace`：disk 319 files＝318 manifest entries＋manifest 自身 | `READ_VERIFIED` | W1 P01／P03 |
| workspace MANIFEST | 60,097 B；SHA `c947b1e721d6315a7fd50bda32d211246855b4207f9e4ef0c197be011f8b5aaa`；tree `e1d9770bb93b8bbc8895d81b56a699c5e1539a251ec038239264f4453c8dd46d`；hash mismatch 0 | `READ_VERIFIED` | §04 probe |
| W0 PRIMARY | 34 entries；tree `f27263d8e0894fcbf897e38b050dcc894d8873860f7e00271aa30a4c6f5f9446`；`PRIMARY_MANIFEST.json` SHA `f2d6e3dc2f7e56384c02ab401babdd81a6690754c9074233431a9080c579f648` | `READ_VERIFIED` | §03、§09 |
| PRIMARY 逐檔 | 33/34 與 manifest byte/SHA 一致；唯一不符：`PRIMARY_RECEIPT.json`（實體 4,222 B／`6dbdd7bd783bc8680702eba6af9973b2a775823399b3bfb9cda099a5132f2efd`；清冊 3,986 B／`18ad4b8d0c303ea2ba655fb4ec6b6b4dcf64833d4e7e8c1b2ab6b23ce5c3e213`） | `W0_PRIMARY_RECEIPT_STALE_IN_MANIFEST` | §10 HOLD |
| W0 15 檔與 28/28 pack | `SOURCE_MANIFEST.json` 13 sources；`PACKAGE_FILE_MANIFEST.json` 27 entries；24 原 Case | `READ_VERIFIED` | §09／§11 |
| GitHub | `git ls-remote https://github.com/shw097-team/FHS-5` → `getaddrinfo() thread failed to start` | `PUBLIC_EXPORT_UNAVAILABLE`（本輪） | §02 D06；不宣 live read |
| G4 synthetic repo | `tag_normalizer.py` 444 B／`9961be52e60b092a8927704cdc1df0fee4178283d4d494017994ea5f1c92b2da`；preimage 125 B／`13df86fa8b75dc454351e584f8d2f363b0323f8c9b6948851ea40c1428e4423a`；test 547 B／`e2eec52a8edcd67f0b89320c743f12027cce26e1d23528652ca6f5563a1c0162` | `READ_VERIFIED`（bytes）；3 tests `REPORTED` | §03、§09 |
| SQS | `regression-cases.yaml` 871 B／`ec5a0331…`；oracle 7,603 B／`4fa9fb1c…`；5 cases；14 requirements；`has_executable_oracle=false` | `READ_VERIFIED` | §03、§09 |

**GitHub 邊界**：v3／v4 記載的 `main@3b3635ce4447f37de035c07d32ff3b13dd2d48d5` 與 Git tree `0fdb63047c75bdf1212b9395a9e19cebf96ab79c` 只作**歷史 pin**；本輪沒有 live remote read，不得寫成「已重新驗證 GitHub」。W0 公開 export 不等於原 PRIMARY tree，也不等於原 Issuer 收據。

## 00.4 任務邊界與不做事項

| 邊界 | 值 | 拒收例 |
|---|---|---|
| 本輪 effect intent | `READ + ISOLATED_DRAFT_WRITE + LOCAL_CHECK`（作者標籤，不是 EffectRegistry token） | 以 `permission=true` 當原 Admission |
| 可寫範圍 | 僅本輪 output root 的 8 個 MD；W0／r5／M／B／WM 只讀 | 修改 W0 或 r5；寫原 Repo／Host |
| 不生成 | W1–W4 十五檔、施工 `FHS5_Wn_WRITEBACK.json`、原 Canonical PI/PD/ECP/TQAEP、GitHub push | 以「已生成小包」宣 Wn 完成 |
| 不執行 | 原域 DEV／OPS／USER／RELEASE、Native、獨立驗收、發布 | 以本地 author test 冒 Independent |
| 不宣稱 | 三 Host 任一 `Consumed`（除 Codex 的 local tool use，且明示非 plugin served） | 以 SKILL.md 可讀宣 Installed／Invoked |
| 終點 | 本正文＋證據附件；WM 完成即停止 | 跨入 W1 Pack 實作或 W2 Effect |

## 00.5 NEG 與 FirstFail

| 反例 | 預期 FirstFail | 防線 |
|---|---|---|
| 用 r4 舊檔冒充 r5 | `SOURCE_IDENTITY_HOLD` | §00.2 raw SHA 重算 |
| 把 W0 作者 pack 當原 Reader ACK | `FALSE_AUTHORITY` | §02 D01／§10 Claim |
| 把 G4 3 tests 當 W1 Host E2E | `HOST_PENDING` | §03／§09 |
| 把 485 Need 當安裝或 W1 Fit | `DENOMINATOR_LOSS`／`PROFILE_GATE_DRIFT` | §02 邊界；W4M 專章 |
| 把 workspace drift 當 CH-07 | `DELTA_MISREROUTED` | §02 D06；§12 |
| 把作者 `PASS` 字串讀成 Independent | `FALSE_INDEPENDENT` | §10 六維 Claim Ledger |

---

# 01｜Goal／FUO／Acceptance／Non-goals

**Input → Design Operation → Output／Consumer／NEG**

## 01.1 Job 與 Wave Goal

**JTBD**：當 Owner 要把 FHS-5 的 Contract Context 交給受權 Host 實際使用時，需要一條可回取、可驗證、無損的 ABI 路徑，讓 Guide 的 ThinStart、Bridge 的四 API、三種 Host 的載入／呼叫／服務狀態，以及下游 Executor 的消費，都不必各自猜測 schema 或權限。

**Wave Goal（原域）**：把 Guide ThinStart 與 Bridge 四 API 接成同 Scope 的可回取 Contract Context，並為 ChatGPT／Codex／Hermes 三 Host 設計逐格 `Selected / Loaded / Installed / Bound / Invoked / ActualServed / Consumed` 的驗證路線。

**原域 FUO**：至少一個受權 Host 對同 Subject／Scope 的 Contract Context 產生真 `Consumed` Raw；若無 Host Raw，只能交 `HOST_CONSUMPTION_PLANNED/UNBOUND` 的作者接口設計，不宣三 Host PASS。

**本輪作者 FUO**：以 W0 PRIMARY 的 28-file pack、13 源 SHA、24 原 Case 與 1011 分母為真輸入，交出：
1. Guide／Bridge 逐欄 ABI crosswalk（含型別、loss、readback）；
2. 四 API 的 request／response／failure 契約與 BodyResolver 安全邊界；
3. 三 Host 九 child 的逐格狀態與 ExpectedRaw；
4. 可供 W1 Pack Author 直接切分的 §11 十五檔映射；
5. 每個缺口具名 Owner／FirstFail／Resume。

## 01.2 Acceptance（作者端，不是原域）

| ACC | 正向可觀測 | 反向最小反例 | 證據位置 | 本輪判定 |
|---|---|---|---|---|
| W1-A01 Source | 17 源 raw SHA／bytes／lines 可回取；W0 PRIMARY 33/34 一致且 stale 具名 | 換舊 r4、假 SHA、隱藏 receipt stale | §00.2／E1 | `PASS_WITH_NAMED_FINDING` |
| W1-A02 Body | 四 API 能指到具體 Clause／Child／NEG；BodyResolver 拒 `..`、absolute、symlink、duplicate key、非法 UTF-8 | 只回 heading、以 excerpt 冒完整 Clause | §06.2／§09 | `AUTHOR_DESIGN_READY` |
| W1-A03 Host | 九 child 逐項有 observation 類型、Consumer、ExpectedRaw、NEG、Owner | 用一 Host 的 Loaded 抵另一 Host 的 Served | §05.1 | `HOST_PARTIAL_LOCAL_ONLY` |
| W1-A04 ABI | 每個受影欄有 source→target→transform→loss→readback；unknown 不丟 | proposal-2 同尾碼直送、drop unknown | §06.1 | `PASS`（作者 crosswalk） |
| W1-A05 Split | 15 檔逐項有內容、欄位、前件、Consumer、拒收；6 WP 各有代表 slice dry-consume | 只列檔名、核心契約仍須回藍圖猜 | §11 | `PASS`（作者 dry-consume） |
| W1-A06 Claim | 六維分帳；缺原收據只停受影 claim | 作者自檢簽 Independent／Release | §10 | `PASS` |

**NEG 總則**：任何一列若只能以「參見藍圖」交代 operation，即 `AUTHOR_BODY_INCOMPLETE`；任何一列若以歷史 `REPORTED` 冒本輪 `OBSERVED`，即 `EVIDENCE_LAUNDERING`。

## 01.3 Non-goals（本波明確不做）

| # | 不做 | 理由 |
|---:|---|---|
| 1 | 不把 Guide／Bridge 的 `proposal-2` 後綴視為同一 schema | 後綴只表示候選家族 |
| 2 | 不以本會話讀到 `SKILL.md` 代替 Host `Loaded`／`Installed`／`ActualServed` | 檔案可讀≠Host 載入 |
| 3 | 不建立第二 Queue、Issuer、Checker 或 Native Runner | 原域權力分立 |
| 4 | 不把 W0 作者文檔當已 consumed Raw | W0 只有作者 pack |
| 5 | 不把 1011／485 分母當 W1 Host Fit | 分母≠適配 |
| 6 | 不在本輪產出 W1 十五檔或 ThinStart 實體檔 | 本輪止於 WM；小包屬後續任務 |
| 7 | 不修改 W0、r5、M、B、WM 原件 | 只讀來源 |

---

# 02｜Affected PI／Original ID／Child／NEG

**Input → Design Operation → Output／Consumer／NEG**

## 02.1 受影原 ID 與 disposition

本波只取「Guide／Bridge／Host／Context」受影的原 Requirement、Child、NEG、Exception 與 Case。未受影項標 `DEFERRED` 或 `REASONED_NA`，不默認 PASS。

| 原 ID／集合 | 原義 | 本波受影 | disposition | 來源錨點 |
|---|---|---|---|---|
| `U-017` | ChatGPT／Codex／Hermes 各自 Loaded／Invoked／ActualServed | 9 child atoms＋Consumed 觀察 | `UPDATE`；9/9 見 §05.1 | B04 `S03:L183`；M §07.4 |
| `U-028` | Hermes Kanban／Delegation／Swarm 三能力 | 三格獨立 | `RETAIN`；`NOT_OBSERVED` | B04 `S03:L194` |
| B02 `CG-R2-REQ-01..16` | Guide 雙觸點與 16 需求 | ThinStart／Touch2、Host 消費 | `RETAIN`；原 Reader `UNBOUND` | B02 §02 |
| B03 `PCB-FR01..17` | Bridge 17 功能與四 API | Context／BodyResolver／compare | `UPDATE`；四 API 具體欄位見 §06.2 | B03 §06 |
| B02 `CG-SEM01..17` | Guide 原域 17 案 | 只作 Case 映射，不重跑 | `RETAIN`；`NOT_RUN` | B02 §09 |
| B03 `A-PCB-001..022` | Bridge v1.1 審查 Finding | ABI／API 受影引用 | `RETAIN`；原 Host 未綁 | B03 附錄 |
| `FHS5.PLP.WaveControl@proposal-2` | 後續 Wn FileContract | 只作 W1 接收介面 | `INFO_ONLY`；本輪不生成 | WM §15.1 |
| `F5-W0-T01..T24` | W0 24 原 Case | 受影 Host／ABI／Path 反例 | `REUSE`；全部 `CASE_UNBOUND` | W0 05_PLANNED_TQAEP |

**Parent／Child 展開規則**：凡原文含「各有／分別／對應」，保留 `SPLIT_CANDIDATE`；原 Reader 未回時記 `SPLIT_UNVERIFIED`，不以作者語感合併。刪任一 child 必須使 A03／A04 FAIL（`REQUIRED_CHILD_MISSING`）。

### 02.1.1 `U-017` 九 child（原 ID 保留）

| child_id | Host | 原狀態 | 本輪 observation | Consumer | ExpectedRaw | NEG |
|---|---|---|---|---|---|---|
| `U-017/ChatGPT/Loaded` | ChatGPT | Loaded | `NOT_OBSERVED` | 原 Host Loader | `manifest`／`loaded_sha256`／`installer_ref` | 其他態成功不可代 Loaded |
| `U-017/ChatGPT/Invoked` | ChatGPT | Invoked | `NOT_OBSERVED` | 原 Host Invoker | `command`／`exit`／`stdout_sha256`／`stderr_sha256` | 其他態不可代 Invoked |
| `U-017/ChatGPT/ActualServed` | ChatGPT | ActualServed | `NOT_OBSERVED` | 原 Host Consumer | `served_bytes_sha256`／`scope_echo` | 其他態不可代 Served |
| `U-017/Codex/Loaded` | Codex | Loaded | `SKILL_BYTES_READ_LOCAL`（非 loader manifest） | 原 Host Loader | `manifest`／`loaded_sha256`／`installer_ref` | 工具呼叫不可代 Loaded |
| `U-017/Codex/Invoked` | Codex | Invoked | `TOOL_CALLS_LOCAL`（非 plugin native invoke） | 原 Host Invoker | `command`／`exit`／`stdout_sha256`／`stderr_sha256` | 作者工具呼叫不可代 plugin Invoked |
| `U-017/Codex/ActualServed` | Codex | ActualServed | `NOT_OBSERVED` | 原 Host Consumer | `served_bytes_sha256`／`scope_echo` | 其他態不可代 Served |
| `U-017/Hermes/Loaded` | Hermes | Loaded | `NOT_OBSERVED` | 原 Host Loader | `manifest`／`loaded_sha256`／`installer_ref` | 其他 Host 不可代 |
| `U-017/Hermes/Invoked` | Hermes | Invoked | `NOT_OBSERVED` | 原 Host Invoker | `command`／`exit`／`stdout_sha256`／`stderr_sha256` | 其他 Host 不可代 |
| `U-017/Hermes/ActualServed` | Hermes | ActualServed | `NOT_OBSERVED` | 原 Host Consumer | `served_bytes_sha256`／`scope_echo` | 其他 Host 不可代 |

### 02.1.2 `U-028` 三 child

| child_id | 功能 | 本輪作者設計 | 原 Host 證據 | 不可做的事 |
|---|---|---|---|---|
| `U-028/Hermes/Kanban` | WorkItem／進度管理 | 只保留 WorkItem→狀態映射與 readback 欄 | `HERMES_KANBAN_NOT_OBSERVED` | 以本地 todo 檔當 Kanban Raw |
| `U-028/Hermes/Delegation` | Native 子代理／分配 | 只保留 assignment／runner／result 契約 | `HERMES_DELEGATION_NOT_OBSERVED` | 以作者自身工具呼叫當 Delegation |
| `U-028/Hermes/Swarm` | 並行協作 | 只保留 independent source view 邊界 | `HERMES_SWARM_NOT_OBSERVED` | 以多個本地命令當 Swarm |
## 02.2 W0 Delta（D01–D08）逐項處置

| Delta | disposition | 受影章 | 本波實質處理 |
|---|---|---|---|
| D01 PRIMARY | `REUSE` | §00／§02／§11 | 重用 34-file 清冊、13 源 SHA、28/28 pack 作 `inspect_package` 的作者輸入；不重掃歷史根 |
| D02 W0-A | `REUSE+UPDATE` | §03／§09 | G4 3 tests 作 W1 API fixture 類比；SQS case+oracle 只作 Case 結構參考；Owner 指名仍 HOLD |
| D03 W0-B | `RETAIN` | §03／§10 | 13 前件不屬 W1 ABI 路徑；保留為 W2 下游 HOLD，不以 W0-B 阻擋 Host ABI 設計 |
| D04 W0-C | `REUSE` | §03／§11 | 1011 分母作 W1 Context 的 Profile 邊界示例；不在 W1 宣 485 Fit |
| D05 驗證修補 | `UPDATE` | §09／§10 | guard 10/0/1、NT 7/7、mutations 6/6 轉成 W1 Host／ABI 反例；只重驗受影 ABI／identity |
| D06 血緣 | `UPDATE` | §00／§02／§09／§12 | CH-07 只承繼 identity-only（`743c6cf`／`80833a5f`／移除 `DEPLOYMENT_VERIFICATION.json`／25 modified 舊 bytes 不在）→ `NOT_COVERED` |
| D07 guard 子項 | `REUSE` | §06／§09 | BodyResolver 的 path containment、UTF-8、duplicate key、ACL 13/13 歷史觀測轉為 P03 驗收欄 |
| D08 handoff | `RETAIN` | §10／§12 | W0 `HANDOFF_CANDIDATE` 與 T4/T5 HOLD 沿用；W1 不簽 Release |

### 02.2.1 D07 六個 F-ID 的受影回寫

| W0 F-ID | 原證據／教訓 | 受影欄 | 本波位置 | 驗證 | Owner |
|---|---|---|---|---|---|
| `W0-F-05` | 2/13 `original_path` 缺 `OLD\`；`SOURCE_LOCATOR_CORRECTION.json` `692b08b5…` | source／path／ABI locator | §00／§02／§06 | path 存在、bytes／SHA 不變 | Source Curator |
| `W0-F-06` | selection receipt 內嵌作者絕對路徑；改以 digest／identity 驗證 | 路徑與 identity 分離 | §04／§12 | digest 可驗、relocated receipt 可讀 | Pack Author |
| `W0-F-08` | deployment 非 atomic、無 before-SHA；改 tmp＋`os.replace` | recovery／atomic | §08／§09 | tmp→replace、before/after tree SHA | Repo/Host Owner |
| `W0-F-09` | 「15 檔」實為 14 file records＋1 top-level；SOURCE_MANIFEST 不自帶 identity | 四波 §00／§11 語義 | §00／§11 | 15 檔說法一致、manifest 不自指 | Pack Author |
| `W0-F-10` | FirstFail token drift；`TOKEN_MAP.json` `6e0dcd49…` | FirstFail 映射 | §09／§10 | local subcode 保留、canonical token 對位 | Checker |
| `W0-F-11` | claim ceiling 用語；`CLAIM_CEILING_MAP.json` `7f7a8c5b…` | claim／handoff | §10／§12 | effective ceiling ≤ selection ceiling | Program Owner |

**D07 邊界**：只回寫 W0 已 `CLOSED_LOCAL` 的教訓；不把 W0 作者修補升為原域 ACL／Reader ACK。

## 02.3 24 原 Case 的 W1 disposition（ID 全保留）

| Case | Type | disposition | 本波用途 |
|---|---|---|---|
| `F5-W0-T01` | POS | `UPDATE` | POS source anchor |
| `F5-W0-T02` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T03` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T04` | NEG | `UPDATE` | fake Reader NEG |
| `F5-W0-T05` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T06` | SEC | `UPDATE` | path escape SEC |
| `F5-W0-T07` | EDGE | `UPDATE` | proposal-2 NEG |
| `F5-W0-T08` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T09` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T10` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T11` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T12` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T13` | POS | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T14` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T15` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T16` | EDGE | `UPDATE` | candidate reuse EDGE |
| `F5-W0-T17` | NEG | `UPDATE` | no raw NEG |
| `F5-W0-T18` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T19` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T20` | EDGE | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T21` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T22` | NEG | `RETAIN` | 原義保留；不重跑 |
| `F5-W0-T23` | SEC | `UPDATE` | secret masking SEC |
| `F5-W0-T24` | POS/NEG | `UPDATE` | Generic／FHS POS/NEG |

**Case 邊界**：24 個 `F5-W0-T01..T24` 仍 `CASE_UNBOUND`；本輪只抽 ID／條件／ExpectedRaw，不宣 Runner。

---

# 03｜Search-Before-Build／Existing Capability

**Input → Design Operation → Output／Consumer／NEG**

## 03.1 逐能力探查

| 探查對象 | 本輪實際觀察 | 決策 | NoFit／NEG |
|---|---|---|---|
| `sbl-tpm-sp` 插件技能 | `C:\Users\user\.codex\plugins\cache\created-by-me-remote\sbl-tpm-sp\0.3.1-rc.1\skills\tpm-sp\SKILL.md` 可讀；自載 `claim_ceiling: HOST_PENDING` | `REUSE`（作者方法） | 以 skill 可讀宣 Host Installed／Consumed → `HOST_PENDING` |
| Plugin alias／manifest | 只見 `sbl-tpm-sp` 路徑與 `sbl-tpm-sp:` 前綴；未見 `tpm-sp-plp` 同 manifest | `BIND_CANDIDATE` | 名稱相似推定同一 plugin → `W1_PLUGIN_ALIAS` |
| Guide 三 namespace | B02 作者設計；無原 Consumer readback | `BIND_CANDIDATE` | `proposal-2` 同名直送 → `EXPLICIT_REVIEW_REQUIRED` |
| Bridge 四 API | B03 §整合註記 07.A 有 request／response／failure；無真 invocation | `BIND_CANDIDATE` | regex／parse PASS 當 E2E → `QUALIFICATION_UNPROVEN` |
| W0 15-file pack | 34-file primary、28/28 pack、13 sources；本輪可讀且 SHA 重算 | `REUSE`（inspect 輸入） | 把 W0 pack 當 Host consumed → `FALSE_AUTHORITY` |
| W0 BodyResolver 防護 | 13/13 源 ACL 歷史觀測；path／UTF-8／duplicate-key 反例 7/7；本輪抽核 `sources/M.md` icacls | `REUSE`（安全欄） | 歷史 13/13 當本輪 Original ACL ACK → `ORIGINAL_READER_UNBOUND` |
| W0-A G4 | `tag_normalizer` 444 B（本輪核 bytes／SHA）；3 tests／exit 0／stderr `1527dfca…`（W0 `REPORTED`，本輪未重跑） | `REUSE`（fixture 類比） | 當 W1 Host 消費 Raw → `HOST_PENDING` |
| SQS `SQS-LEGACY-REGRESSION-013` | 5 cases、14-requirement frozen oracle；無 W0-A designation | `REUSE`（Case 結構參考） | 當 W1 E2E → `CASE_UNBOUND` |
| ChatGPT／Hermes Host | 本輪無 loader／invoker／readback | `BUILD_CANDIDATE`（adapter 設計） | 一 Host Loaded 抵另一 Host → `HOST_ABI_DRIFT` |
| Codex 本會話 | 可讀 plugin skill bytes、可呼叫 `exec_command`／`apply_patch`；無 Host installer receipt | `ACTIVATE_LOCAL_ONLY` | 工具呼叫當 plugin ActualServed → `HOST_PENDING` |

## 03.2 四 API 的作者手動類比（不是原 Bridge 執行）

本輪以 W0 PRIMARY 為輸入，人工演練：

1. `inspect_package`：核 28 檔／13 源／24 Case，記錄 33/34 primary 一致與 receipt stale。
2. `explain_slice`：以 M `L1010–L1039` 的 24 Case 作 clause 集合，保留 parent/child/NEG 與 missing。
3. `render_agent_context`：產出本正文的 Context 版本；不冒充 API 回應。
4. `compare_context`：比較 PATCH03 276/275、PRIMARY 317/316、live 318/319 的計數差，只作 `DELTA_UNVERIFIED` 示例。

狀態一律 `AUTHOR_EXERCISED_MANUAL_ANALOGUE`；不填 API PASS、exit code 或 Raw SHA。

## 03.3 G4／SQS 的嚴格限制

| 候選 | 可用的部分 | 不可用的部分 | W1 用途 |
|---|---|---|---|
| G4 | 444 B post、125 B preimage、547 B test；3 tests `REPORTED` exit 0 | 無 LICENSE、無 `.git`、無原 Issuer、`w0a_designation=false` | 作 `render_agent_context` 的 fixture 類比與 rollback 樣板 |
| SQS | 5 cases、14 requirements、frozen oracle digest `501732af…` | `has_executable_oracle=false`；無 Owner 指名 | 作 `explain_slice` 的 clause／requirement 結構參考 |

## 03.4 既有 guard 的用法

| Script | 靜態閱讀所見 | 本波可複用 | 限制 |
|---|---|---|---|
| `pack_guard.py` | 10 MD＋5 JSON；PACKAGE 自排除／唯一／SHA／bytes；`safe_rel` 拒 `\`、`:`、`..`；六身份；claims all false | §11 FileManifest 與身份檢查 | 不執行原 Case／Oracle |
| `selection_guard.py` | schema／status／HUMAN_OWNER／authority；digest 或 strict path；15 檔；W0-B `NOT_ADMITTED`；receipt null | §04 identity／§10 claim | digest 不代表原 Issuer |
| `m22_guard.py` | Source／File／TQAEP schema；duplicate JSON key；symlink；path containment；FirstFail token | §06 BodyResolver／§09 token | 非原 Checker |
| `w0_guard.py` | identity／source／package／TQAEP／M12.7／authority／path／holds／denominator／source-conflict | 四波 local preflight | 原 Runner 未綁 |

Output：`ExistingCapabilityLedger` → Wave Owner／Executor。NEG：只因文件沒有 ACK 就重造 Runner／Queue／Reviewer；未讀私有 Archive 就宣 NoFit。FirstFail：`REUSE_NOT_CHECKED`、`PRIVATE_ARCHIVE_UNBOUND`、`HOST_PENDING`。

---

# 04｜RepoContext／Binding Request

**Input → Design Operation → Output／Consumer／NEG**

## 04.1 本波 RepoContext

本波**不改任何產品 Repo**，故 `repo_context=null`。W1 的 `RepoBindingRequest` 只針對 Guide／Bridge adapter 的未來位置，不是已綁定值；也不把 W0 workspace 當產品 Repo。

| 欄位 | 型別 | 本輪值 | 必要來源 | 拒收 |
|---|---|---|---|---|
| `repo.root` | string | `null` | Original Repo Reader | 以 workspace 路徑冒充 |
| `repo.head` | 40-hex | `null` | live git probe | caller 自報 HEAD |
| `repo.branch` | string | `null` | live probe | 由檔名推斷 |
| `repo.dirty` | bool | `null` | live probe | 以 manifest 無 mismatch 推 clean |
| `repo.untracked[]` | string[] | `null` | live probe | 省略 untracked |
| `repo.acl_ref` | string | `null` | ACL reader | 歷史 13/13 當本輪 |
| `adapter_path` | string | `null` | Repo Owner | 以 `PROPOSED_NOT_APPLIED` 當已存在 |
| `preimage_sha256` | 64-hex | `null` | Repo Reader | 以 G4 preimage 冒充 |
| `write_set[]` | string[] | `[]` | 未准入 | 未准入先給 WriteSet |

## 04.2 本輪 local probe（只證容器，不證產品 Repo）

| Probe | 結果 | 可用的結論 | 不可推論 |
|---|---|---|---|
| W0 workspace root | 可列舉；319 files、MANIFEST 318＋self | `WORKSPACE_READ_OK` | 產品 Repo 已綁 |
| workspace MANIFEST | SHA `c947b1e7…`、tree `e1d9770b…`、hash mismatch 0 | `MANIFEST_SELF_CONSISTENT` | 原 Reader ACK |
| `.git` | 未觀察到 workspace `.git`；`git -C` 回 `Permission denied` | `REPO_CONTEXT_UNBOUND` | `PD_BOUND` |
| PRIMARY root | 36 實體檔＝34 清冊＋index＋manifest 自身；tree `f27263d8…`；33/34 byte 一致 | `PRIMARY_MOSTLY_UNCHANGED` | receipt 已更正 |
| G4 root | `08_AUDIT_REMEDIATION\CANDIDATE_QUALIFICATION\G4\synthetic_repo` 可讀 | `CANDIDATE_READ_OK` | 原 RepoContext |

## 04.3 RepoBindingRequest 的恢復條件

| 請求欄 | Owner | 最小可接受證據 | FirstFail | Resume |
|---|---|---|---|---|
| `repo.root/head/branch` | Original Repo Owner | 同 Subject／Scope 的 live git probe＋HEAD SHA | `REPO_HEAD_MISMATCH` | 同 HEAD 的 readback |
| `repo.dirty/untracked` | Original Repo Owner | `git status --porcelain=v2` raw | `REPO_CONTEXT_UNBOUND` | 同 probe 重讀 |
| `repo.acl_ref` | OS Principal／Repo Owner | ACL raw＋scope | `ACL_UNBOUND` | 同路徑 ACL readback |
| `adapter_path` | Guide／Bridge Owner | 實際路徑、preimage、write scope | `WRITE_SET_UNBOUND` | 原 ECP 准入後的 path set |
| `preimage_sha256` | Repo Reader | 每個 target 的 preimage bytes／SHA | `PREIMAGE_UNBOUND` | 同位元重算 |

**設計規則**：RepoRoot／HEAD／branch／dirty／untracked／ACL／preimage／WriteSet 必須來自原 Repo Reader 的同次 probe；作者只保存 `null` 與 request。Output：`RepoBindingCandidate` → Original Repo Owner／PD Owner。NEG：caller 字串 `head` 冒充 live HEAD；`repo_context=null` 寫成 `PD_BOUND`；未准入給 WriteSet。FirstFail：`REPO_HEAD_MISMATCH`、`PD_UNBOUND`、`WRITE_SET_UNBOUND`。
---

# 05｜Host／Effect／Issuer／Permission

**Input → Design Operation → Output／Consumer／NEG**

## 05.1 三 Host 七階段（summary，不取代九 child）

| Host | Selected | Loaded | Installed | Bound | Invoked | ActualServed | Consumed | 本輪狀態 |
|---|---|---|---|---|---|---|---|---|
| ChatGPT | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `HOST_PENDING` |
| Codex | `CAPABILITY_LISTED_IN_SESSION` | `SKILL_BYTES_READ_LOCAL` | `NOT_OBSERVED` | `PLUGIN_VERSION_PATH_OBSERVED` | `TOOL_CALLS_LOCAL` | `NOT_OBSERVED` | `NOT_OBSERVED` | `HOST_PARTIAL_LOCAL_ONLY` |
| Hermes | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `NOT_OBSERVED` | `HOST_PENDING` |

**階段定義與最小證據**：
1. `Selected`：Owner／Host 設定中出現目標 plugin／skill；證據是設定或 capability listing，不是載入。
2. `Loaded`：Host loader 讀入 bytes；需 `manifest`、`loaded_sha256`、`installer_ref`。
3. `Installed`：有 installer／registration receipt；需版本、路徑、ACL。
4. `Bound`：Host 把 plugin 绑定到特定 scope／policy epoch；需 binding record。
5. `Invoked`：有 invocation；需 `command`、`args`、`exit`、stdout／stderr SHA。
6. `ActualServed`：Host 對 Consumer 真正輸出；需 `served_bytes_sha256`、`scope_echo`。
7. `Consumed`：Consumer 讀回並回報；需 `consumer_id`、`consumed_sha256`、`subject`／`scope`。

**七階段不可互推**：Loaded 不證 Installed；Installed 不證 Bound；Invoked 不證 Served；Served 不證 Consumed。任一階段缺證只停該 Host 的該 claim，不停其他 Host 或作者章節。

## 05.2 權限與 Principal（不因單一 Owner 合併）

| 角色 | 本波是否持有 | 可做 | 不可做 | 來源 |
|---|---|---|---|---|
| Human Owner | 是（任務授權） | 指定 scope、批准作者交付 | 自動成為 Issuer／OS Principal／Checker | H-CLOSE |
| Wave Curator／作者 | 是 | READ、隔離 DRAFT、LOCAL CHECK | 寫原 Repo／Host、簽 Independent | 本檔 |
| Original Issuer | `UNBOUND` | 發 WorkOrder／Admission | 由作者代簽 | W0-B |
| OS Principal | `UNBOUND` | 在 Host 執行 OPS | 以本機 `CodexSandboxUsers` 冒充 | W0-B OPS |
| Original Reader | `UNBOUND` | 讀回 canonical PI/PD | 由本地 pack 代替 | 全來源 |
| Protected Checker | `UNBOUND` | Independent verdict | 由作者自檢代替 | W4 |
| Publisher | `UNBOUND` | Release | 由 MD SHA 代替 | W4 |

**Effect 邊界**：W1 只允許 `SOURCE_READ`＋`ISOLATED_DRAFT_WRITE`＋`LOCAL_CHECK`。Host adapter 安裝、plugin registration、repo／host write 一律 `NOT_ADMITTED`。Effect token 只由原 Effect Registry 決定；不得由路徑、檔名或相似字串推斷。

## 05.3 Stop scope 與恢復

| 缺口 | 停止範圍 | 仍可繼續 | Owner | Resume predicate |
|---|---|---|---|---|
| ChatGPT loader／install receipt | ChatGPT 的 Loaded 以後 claim | Codex／Hermes 設計、四 API 設計 | ChatGPT Host Owner | 同 Scope manifest／LoadedSHA |
| Hermes 三能力 | Hermes Kanban／Delegation／Swarm 各自 | W1 文件與 ABI | Hermes Host Owner | 同 Host 三格 Raw |
| Guide／Bridge consumer | 該 ABI 的 Consumed claim | crosswalk、BodyResolver 設計 | ABI Owner | 逐欄 consumer readback |
| Original Issuer | Host adapter install／任何 effect | READ／DRAFT | Original Issuer | 同 Subject／Scope Admission |
| Protected Checker | Independent claim | 作者自檢 | Checker | 同 Candidate 的 distinct receipt |

Output：`HostEffectLedger`＋`PermissionMatrix` → Issuer／Host Owner／Program。NEG：作者授權當原 Admission；未知 Effect 默認 READ；OPS principal 與 DEV principal 互換。FirstFail：`EFFECT_UNBOUND`、`FALSE_AUTHORITY`、`PRINCIPAL_DOMAIN_MISMATCH`、`HOST_PENDING`。

---

# 06｜Architecture／Seam／ABI／ADR

**Input → Design Operation → Output／Consumer／NEG**

## 06.1 七 Seam 的 W1 受影部分

| Seam／ABI | Producer→Consumer | 版本 | 本波輸出 | 未知欄位處理 | NEG |
|---|---|---|---|---|---|
| `GuideThinPrompt` | Wn→Guide | `@proposal-2` | ThinStart candidate | 保留 `legacy_payload` | Scope 擴張 |
| `GuidePromptAdvice` | Guide→Operator | `@proposal-2` | Advice candidate | 保留 kind／reason | 當 WorkOrder |
| `GuidePackageControlFields` | Wn→Guide | `@proposal-2` | control map | 與 Bridge 分欄 | 與 Bridge 同 schema |
| `PLP.BridgeContextView` | Bridge→Executor | `@proposal-2` | Context view | unknown→`EXPLICIT_REVIEW_REQUIRED` | 只 heading |
| `PLP.BridgeDelta` | Bridge→Guide | `@proposal-4` | Delta view | `@2` 字串不升 `@4` | schema 混用 |
| SM-04 | Wn→Guide | — | Package identity | 缺則 null | 假 Package |
| SM-05 | Guide／Bridge→Executor | — | consumed candidate | 無 Host readback 留 UNBOUND | 假 consumed |
| SM-07 | FAR→Guide Touch2 | — | ThinResume | advice 不轉 Grant | CLOSE→Release |

## 06.2 Bridge 四 API 的具名契約

以下 request／response 是**作者 fixture**（`AUTHOR_FIXTURE_NOT_LIVE`），不是原 Bridge 回應；不得填假 exit code 或 Raw SHA。

### 06.2.1 `inspect_package`

| 欄 | 型別 | 必選 | 說明 | 拒收 |
|---|---|---|---|---|
| `request.root` | string | 是 | 受權 package root | 越界／symlink |
| `request.manifest_path` | string | 是 | `PACKAGE_FILE_MANIFEST.json` | 自指／缺檔 |
| `request.expected_identity` | object | 是 | 六 identity keys | 不一致 |
| `request.expected_source_manifest_sha256` | 64-hex | 是 | 來源 manifest SHA | 漂移 |
| `response.source_refs[]` | array | 是 | 每筆 `(kind,path,sha256,span)` | 空陣列冒充完整 |
| `response.requirements[]` | array | 是 | 原 Requirement／Child／NEG 候選 | 丟 child |
| `response.effect_constraints[]` | array | 是 | effect token／permission | 由路徑猜 |
| `response.unresolved_refs[]` | array | 是 | 不可回取的來源 | 靜默丟棄 |
| `response.package_sha256` | 64-hex | 是 | 重算 digest | 用舊 digest |

**Failure**：`SOURCE_INTEGRITY_FAILED`（SHA 不符）、`PACKAGE_INCOMPLETE_LOCAL`（缺必要檔）、`PATH_OUTSIDE_ROOT`（路徑逸出）。Consumer：原 Executor／Reader。

### 06.2.2 `explain_slice`

| 欄 | 型別 | 必選 | 說明 | 拒收 |
|---|---|---|---|---|
| `request.view` | enum | 是 | `requirements`／`architecture`／`program`／`assurance` | 未定義 enum |
| `request.kinds[]` | string[] | 是 | 指定 clause kind | 空集合 |
| `response.clause_refs[]` | array | 是 | `(source_id,sha256,line_start,line_end)` | 只 heading |
| `response.parent` | object | 是 | 原 Parent ID／span | 缺 parent |
| `response.children[]` | array | 是 | 每個 child 的 ID／NEG／exception | 合併 child |
| `response.missing[]` | array | 是 | 無法解析的 clause | 假完整 |

**Failure**：`SPLIT_UNVERIFIED`（child 拆分未經原 Reader）、`SEMANTICS_ORIGINAL_READER_UNBOUND`（原語義未回）。Consumer：Reviewer／PI Reader。

### 06.2.3 `render_agent_context`

| 欄 | 型別 | 必選 | 說明 | 拒收 |
|---|---|---|---|---|
| `request.explanation` | object | 是 | 上一 API 的 response | 自造 clause |
| `request.target_host` | enum | 是 | `chatgpt`／`codex`／`hermes`／`generic` | 未支援值 |
| `request.scope` | string | 是 | 同 Subject／Scope | Scope 擴張 |
| `response.context_utf8` | bytes | 是 | UTF-8 正文 | 非 UTF-8 |
| `response.source_locators[]` | array | 是 | 每個主張的 locator | 無源斷言 |
| `response.untrusted_markers[]` | array | 是 | 來源內指令標記 | 當指令執行 |
| `response.context_sha256` | 64-hex | 是 | context digest | 與 bytes 不符 |

**Failure**：`CONTEXT_SCOPE_MISMATCH`、`UNTRUSTED_SOURCE_DATA`（來源含 `ignore permission` 等字串時只標記、不執行）。Consumer：GPT／Codex／Hermes Consumer。

### 06.2.4 `compare_context`

| 欄 | 型別 | 必選 | 說明 | 拒收 |
|---|---|---|---|---|
| `request.before` | object | 是 | 前一期 context ref＋SHA | 浮動 HEAD |
| `request.after` | object | 是 | 後一期 context ref＋SHA | 不同 Subject |
| `response.added[]` | array | 是 | `(kind,path,sha256)` | 只寫「有變」 |
| `response.removed[]` | array | 是 | 同上 | 省略移除 |
| `response.changed[]` | array | 是 | 同上 | 語義推論代替 |
| `response.comparable` | bool | 是 | 同 Subject／Scope／Host／Epoch | 跨 Subject 比較 |

**Failure**：`COMPARE_CROSS_SUBJECT_DENY`、`DELTA_UNVERIFIED`（兩期不同構）。Consumer：Guide／Program。

## 06.3 BodyResolver 契約

| 欄 | 型別 | 規則 |
|---|---|---|
| `source_local_id` | string | 必須在 SourceManifest |
| `raw_sha256` | 64-hex | 與 manifest 重算一致 |
| `line_start`／`line_end` | int | `1 ≤ start ≤ end ≤ lines` |
| `line_sha256` | 64-hex | 該 span 的 SHA |
| `full_text` | UTF-8 | 不得只給 excerpt |
| `path_scope` | object | 受權 root；拒 absolute／UNC／`..`／symlink／junction |
| `reader_state` | enum | `OFFLINE_PINNED`／`ORIGINAL_READER`／`UNBOUND` |

**拒絕條件**：duplicate JSON key、非法 UTF-8、超過大小上限、scope／ABI／pin 不符、reparse point 出界。無離線封存且無原 Reader 時 `BODY_RESOLVER_UNBOUND`；不得以摘要或相似檔代替完整 Clause。

## 06.4 ABI 逐欄 crosswalk（作者）

| Source field（@2） | Target | 型別 | Transform | Loss policy | Readback |
|---|---|---|---|---|---|
| `GuideThinPrompt.package_sha256` | Wn `source_manifest_sha256` | 64-hex | 直接複製、重算 | 不同 bytes → `SOURCE_IDENTITY_HOLD` | Consumer echo 同 SHA |
| `GuideThinPrompt.subject`／`scope` | Wn `subject_id`／`scope` | string | 只允許同值 | 擴張 → `SCOPE_DRIFT` | echo 同值 |
| `GuideThinPrompt.goal`／`fuo`／`done` | Wn Goal／FUO／Done | string | 文字保留；`done` 必須可觀測 | 字串 PASS → `EXPECTED_RAW_MISSING` | 對照 §09 Case |
| `GuideThinPrompt.effect` | Original EffectRegistry token | enum | 只查表 | 未知 → `EFFECT_UNBOUND` | Registry／Issuer receipt |
| `GuideThinPrompt.owner`／`next`／`stop`／`resume` | Wn Owner／Next／Stop／Resume | object | 角色不寫個人；Stop 可執行 | 缺 resume → `RESUME_UNBOUND` | Owner 簽收 |
| `GuidePromptAdvice.advice_kind`／`reason`／`owner` | Guide2 advice | enum／string | 保留 kind／reason | 當 Grant → `FALSE_AUTHORITY` | Guide2 只回 advice |
| `GuidePackageControlFields.identity`／`bindings` | Bridge `inspect_package` | object | identity 對 manifest；bindings 對 Source／Effect | 衝突 → `EXPLICIT_REVIEW_REQUIRED` | 兩份 manifest 對讀 |
| `BridgeContextView.source_refs` | Context source list | array | 每筆 `(kind,path,SHA,span)` | 只 heading → `CONTEXT_SCOPE_MISMATCH` | BodyResolver raw SHA |
| `…requirements`／`effect_constraints`／`verification_refs`／`unresolved_refs` | SliceExplanation／context | array | 保留 Parent／Child／NEG／missing | 丟 unknown → `ABI_LOSSY_CROSSWALK` | 完整 clause 回讀 |
| `…source_set_sha` | Context digest | 64-hex | 對 13 源／pack 重算 | 舊 digest → `SOURCE_INTEGRITY_FAILED` | 同 digest |
| `BridgeDelta@proposal-4.added/removed/changed` | Guide2 delta | array | exact `(kind,path,SHA)` | `@2` rename → `SCHEMA_UNSUPPORTED` | before／after 兩期 |
| `BodyResolver.source_local_id`／`raw_sha256`／`line_start`／`line_end`／`line_sha256`／`full_text`／`path_scope` | Context body | mixed | 每次重核 manifest 與 root | 任一不符 → `BODY_RESOLVER_UNBOUND`／`PATH_OUTSIDE_ROOT` | 原 Reader 或離線封存 |

## 06.5 狀態轉移與 ADR

**Host 狀態機**：`Selected → Loaded → Installed → Bound → Invoked → ActualServed → Consumed`。每個箭頭只能由對應證據觸發；不得跳階。任一階段可回 `UNKNOWN`，`UNKNOWN` 只能由原 Host Reader reconcile，不可由作者重試補位。

**ADR-W1-01**：Guide 與 Bridge 各自持有 namespace，不因 `@proposal-2` 同尾碼而共用 schema；跨接一律經 §06.4 crosswalk。
**ADR-W1-02**：unknown 欄位保留在 `legacy_payload`，並標 `EXPLICIT_REVIEW_REQUIRED`；不得丟棄以求 parse 通過。
**ADR-W1-03**：Context 產出必須附 SourceLocator 與 `UNTRUSTED SOURCE DATA` 標記；來源內的指令字串是資料，不是任務指令。
**ADR-W1-04**：W1 不建立第二條 Host 寫路；Host 安裝與服務由各 Host Owner 執行。

Output：`WaveArchitectureDecision`＋`ABI Crosswalk` → 五 PROJ／Original Consumer。NEG：`@2` 直送、丟 unknown、以名稱相同推定 Consumer 已支援。FirstFail：`ABI_LOSSY_CROSSWALK`、`SCHEMA_UNSUPPORTED`、`CONSUMER_UNVERIFIED`。

---

# 07｜六個原 WP 的實質 Operation／DAG／Owner／Run Order

**Input → Design Operation → Output／Consumer／NEG**

## 07.1 WM1-P01 Identity／Reuse

| 項 | 內容 |
|---|---|
| Input | 原 plugin manifest／alias／version／capability；三 Host Reader；W0 PRIMARY 來源 |
| Step 1 | 以 `SourceManifest` 找 plugin 檔與 alias；記 absolute path、bytes、SHA、版本 |
| Step 2 | 建 `HostCapabilityLedger`：每 Host × 七階段一列，observation 類型只用 §00.3 的 evidence class |
| Step 3 | 對 `U-017` 九 child 逐一填 observation、Consumer、ExpectedRaw、NEG、Owner |
| Step 4 | 對 `U-028` 三 child 分開填 Hermes 三格，不合併 |
| Step 5 | 檢查 alias 是否同一 manifest；不能證明時記 `W1_PLUGIN_ALIAS` |
| Output | `HostCapabilityLedger`（作者）→ Plugin Owner／Host Owner |
| Consumer | W1 P04、W4 Host Fit |
| NEG／FirstFail | 以 skill 可讀宣 Installed → `HOST_PENDING`；名稱相似推定 alias → `W1_PLUGIN_ALIAS` |
| 本輪狀態 | `HOST_PARTIAL_LOCAL_ONLY`（僅 Codex local tool use） |

## 07.2 WM1-P02 ABI Crosswalk

| 項 | 內容 |
|---|---|
| Input | B02 Guide 三 namespace、B03 Bridge 四 API、WM §05 Seam、W0 proposal-2 |
| Step 1 | 逐 namespace 列欄位、型別、必選、來源、消費者 |
| Step 2 | 對每個 source field 填 target、transform、loss policy、readback |
| Step 3 | 對 unknown／legacy 欄位建 `legacy_payload` 與 `EXPLICIT_REVIEW_REQUIRED` |
| Step 4 | 建 POS／NEG fixture：同值直送、擴 Scope、drop unknown、`@2` 升 `@4` |
| Step 5 | 對每個 target 指到具體 §06.4 列與 §11 目標檔 |
| Output | `ABI Crosswalk`＋`LossLedger` → Bridge／Guide ABI Owner |
| Consumer | W1 P03、Wn Pack Author |
| NEG／FirstFail | 同尾碼直送 → `EXPLICIT_REVIEW_REQUIRED`；丟 unknown → `ABI_LOSSY_CROSSWALK` |
| 本輪狀態 | `AUTHOR_DESIGN_READY`（無 Consumer readback） |

## 07.3 WM1-P03 四 API／BodyResolver

| 項 | 內容 |
|---|---|
| Input | B03 四 API 契約、W0 15 檔、13 源、Clause span |
| Step 1 | `inspect_package`：核 manifest、identity、13 源、24 Case；輸出 source_refs／requirements／effect_constraints／unresolved_refs |
| Step 2 | `explain_slice`：按 view／kinds 取 clause；保留 parent／child／NEG／missing |
| Step 3 | `render_agent_context`：產 UTF-8 context，附 SourceLocator 與 untrusted 標記 |
| Step 4 | `compare_context`：只比同 Subject／Scope；輸出 added／removed／changed exact tuple |
| Step 5 | BodyResolver：逐 body 檢查 path containment、duplicate key、UTF-8、SHA、span |
| Output | `ContextBundle`（作者 fixture）→ Executor／Host Consumer |
| Consumer | W1 P04、W2 Executor、W3 Challenger |
| NEG／FirstFail | path escape → `PATH_OUTSIDE_ROOT`；excerpt 冒 Clause → `BODY_RESOLVER_UNBOUND`；跨 Subject compare → `COMPARE_CROSS_SUBJECT_DENY` |
| 本輪狀態 | `AUTHOR_EXERCISED_MANUAL_ANALOGUE`；無 API exit／Raw |

## 07.4 WM1-P04 Host Actual Read

| 項 | 內容 |
|---|---|
| Input | 三 Host loader／invoker／env／return；同 Scope 的 Context |
| Step 1 | 對每 Host 先確認 Selected／Loaded 證據；無則停該 Host |
| Step 2 | 取得 Invocation raw：command、args、exit、stdout／stderr SHA |
| Step 3 | 取得 ActualServed：served bytes SHA、scope echo、served_at |
| Step 4 | 取得 Consumed：consumer_id、consumed SHA、subject／scope、readback_at |
| Step 5 | 對照 `U-017` 九 child，缺一即 `REQUIRED_CHILD_MISSING` |
| Output | `HostObservationLedger` → Host Owner／Program |
| Consumer | W1 P06、W4 Host Fit |
| NEG／FirstFail | 以一 Host 抵另一 Host → `HOST_ABI_DRIFT`；無 Raw 宣 PASS → `HOST_PENDING` |
| 本輪狀態 | `NOT_OBSERVED`（ChatGPT／Hermes）；Codex 只 local |

## 07.5 WM1-P05 Adversarial ABI Tests

| 項 | 內容 |
|---|---|
| Input | Scope widen、unknown／lossy、no host、legacy、ACL escape、fake readback |
| Step 1 | 為每類建最小 fixture（隔離副本，不改原 source/oracle） |
| Step 2 | 執行作者檢查：schema、path、SHA、UTF-8、unknown 保留 |
| Step 3 | 記 expected／observed／firstfail／reproduction |
| Step 4 | 對每個 finding 指到受影 API 欄與 repair 位置 |
| Output | `AdversarialABIReport` → Reviewer／Bridge Owner |
| Consumer | W1 P06、W3 Challenger |
| NEG／FirstFail | parser PASS 當 E2E → `QUALIFICATION_UNPROVEN`；改 oracle 求綠 → `ORACLE_DRIFT` |
| 本輪狀態 | 8 原 Case＋R3-01..05 規劃；實跑者標 `AUTHOR_REPLAY` |

## 07.6 WM1-P06 AsBuilt／Next

| 項 | 內容 |
|---|---|
| Input | P01–P05 的輸出、W0 已知實績、HOLD |
| Step 1 | 分帳 actual／expected／not-covered |
| Step 2 | 建 ABI change cone：哪些欄影響哪些 Consumer |
| Step 3 | 對 W2 交 Host adapter 的 interface（不是 consumed） |
| Step 4 | 寫 W1→W2／W3 的 input、AcceptedRaw、限制 |
| Output | `WaveClosure`＋`Handoff` → W2／W3 Program |
| Consumer | 下一波作者、原 Owner |
| NEG／FirstFail | 無 delta 全盤重做 → `PHASE_OVERREACH_CANDIDATE`；Wn 未跑填 AsBuilt PASS → `AS_BUILT_OVERCLAIM` |
| 本輪狀態 | `PD_AUTHOR_CANDIDATE` |

## 07.7 DAG 與 Run Order

| 節點 | 前置 | 邊型別 | 退出狀態 |
|---|---|---|---|
| WM1-P01 | — | `INFO_ONLY` | `HOST_PENDING` |
| WM1-P02 | P01 | `AUTHOR_DOC_ORDER` | Crosswalk |
| WM1-P03 | P02 | `HARD_SOURCE_VERIFIED`（只證 bytes） | API plan |
| WM1-P04 | P03 | `UNVERIFIED` | `NOT_OBSERVED` |
| WM1-P05 | P02 | `AUTHOR_DOC_ORDER` | Test plan |
| WM1-P06 | P04,P05 | `AUTHOR_DOC_ORDER` | Handoff |

**合法並行**：P02 與 P05 可在 P01 後並行；P04 不得在 P03 前宣 served；P06 不得在 P04 前宣 consumed。**禁止**：cycle；以 W4 Release 作 P01 前件；把 G4 local tests 畫成 `HARD_VERIFIED` Host 邊。FirstFail：`GATE_CYCLE_CANDIDATE`、`PHASE_OVERREACH_CANDIDATE`、`UNVERIFIED_EDGE_AS_HARD`。

---

# 08｜DEV／OPS／READ／DRAFT Construction／ECP

**Input → Design Operation → Output／Consumer／NEG**

本節只寫 W1 適用的 Construction／ECP **計畫**；不是 Canonical ECP，也不是 Grant。所有受保護 Effect 在缺原 Admission 時一律 `NOT_ADMITTED`。

| 動作 | Precondition | Operation（作者設計） | Post／Readback | Retry／Idempotency | Recovery | 本輪狀態 |
|---|---|---|---|---|---|---|
| Guide ThinStart render | 同 Scope Source／Goal／FUO | 以 §06.4 欄位生成 UTF-8 text；不含新 Scope | 重算 context SHA；比對 source locator | key＝task＋source pin＋wave＋revision | 丟棄本輪 staging，保留 LastGood | `AUTHOR_DESIGN_READY` |
| Bridge Context render | 四 API 契約、離線 body | 依 §06.2 產 request／response；BodyResolver 檢查 | response SHA、unresolved_refs | 同 key no-op | 還原前一 context | `AUTHOR_DESIGN_READY` |
| Host adapter install | installer manifest、PolicyEpoch、ACL、Issuer | 不由作者執行 | 需 Host loader receipt | 不重試 | 原 Host uninstall／rollback | `NOT_ADMITTED` |
| Host invoke | 已 install／bound | 不由作者執行 | invocation raw | 只暫時 I/O | Host-specific | `NOT_OBSERVED` |
| Native effect | Original Admission | 不屬 W1 | — | — | — | `NOT_ADMITTED` |

**Idempotency**：`TaskID＋source_pin_set_sha256＋PRIMARY_selection＋target_wave＋revision`。同 key 重放只回同輸出或 no-op；異值保 LastGood 並建新候選。
**Retry**：只允許暫時 I/O；`UNKNOWN` 先核 bytes／manifest，不盲重試。
**Atomic**：所有 staging 寫入同卷，完成後 atomic rename；失敗只清本輪暫存，不動原件。
**NEG**：把 ECP 意圖當核准 → `ECP_NOT_GRANT`；以 `git revert` 當 Host recovery → `RECOVERY_KIND_MISMATCH`；CLI exit 0 但 Context SHA 不符 → `EFFECT_NOT_VERIFIED`。

Output：`EffectStrategy` → Original ECP／Executor。本輪不執行任何 Native。
---

# 09｜TQAEP Strategy／Case／Oracle

**Input → Design Operation → Output／Consumer／NEG**

## 09.1 原 Case 分母與作者 Case

**原 Case 分母（保留，不重跑）**：B02 `CG-SEM01..17`（17）、B03 38＋28（66）、W0 `F5-W0-T01..T24`（24）。本輪只使用其 ID、條件、ExpectedRaw；全部 `CASE_UNBOUND`／`NOT_RUN`。

| Case | 類型 | 預期／FirstFail | 本輪狀態 | 來源／對應 |
|---|---|---|---|---|
| `W1-HOST-01` | POS | 某 Host 真 Consumed，同 Scope Raw | `NOT_RUN` | 無；W0 T01 只到 Source |
| `W1-HOST-02` | NEG | ChatGPT Loaded 抵 Hermes Served | `HOST_ABI_DRIFT` | W0 T04 Host 版 |
| `W1-HOST-03` | NEG | 只讀 SKILL.md 宣 Invoked | `HOST_PENDING` | 本輪 Codex 實例 |
| `W1-HERMES-01` | POS | Kanban／Delegation／Swarm 三格分開 | `NOT_OBSERVED` | 無 |
| `W1-ABI-01` | NEG | Guide proposal-2 直送 Bridge proposal-2 | `EXPLICIT_REVIEW_REQUIRED` | W0 T07 |
| `W1-ABI-02` | NEG | proposal-1 無 crosswalk 升 proposal-2 | `LOSSY_MIGRATION` | W0 T07 變體 |
| `W1-SEC-01` | SEC | Context 內嵌 `ignore permission` | `UNTRUSTED_SOURCE_DATA` | W0 T23 |
| `W1-API-01` | POS | 四 API 完整 Clause／NEG 可回取 | `NOT_RUN` | W0 T01／T06 |
| `W1-R3-01` | POS | 以 W0 PRIMARY 34 清冊（33/34）、27/27 pack、13-source manifest 作 inspect 輸入；source_refs 與 body SHA 可回取 | `AUTHOR_REVIEW_PARTIAL`（receipt stale） | D01／D07 |
| `W1-R3-02` | NEG | plugin skill bytes read 當 Host Loaded／Installed | `HOST_PENDING` | 本輪 Codex |
| `W1-R3-03` | NEG | crosswalk 缺 `effect`／`resume` 仍宣完整 | `ABI_LOSSY_CROSSWALK` | D05 |
| `W1-R3-04` | EDGE | workspace 317→318、PRIMARY 不變 | `WORKSPACE_DRIFT_BOUNDED` | D06b |
| `W1-R3-05` | NEG | CH-07 identity-only 當可恢復舊 bytes | `EVIDENCE_LAUNDERING`／`DELTA_MISROUTED` | D06 |

## 09.2 ExpectedRaw 欄位（每 Case 的觀測點）

| Case 群 | ExpectedRaw 必要欄 | 可觀測點 | 缺件狀態 |
|---|---|---|---|
| Host 消費 | `host_id`、`loaded_sha256`、`installer_ref`、`policy_epoch` | Host manifest／loader log | `HOST_PENDING` |
| Invocation | `command`、`args`、`exit`、`stdout_sha256`、`stderr_sha256` | Host invoker raw | `NOT_OBSERVED` |
| Served | `served_bytes_sha256`、`scope_echo`、`served_at` | Host service response | `NOT_OBSERVED` |
| Consumed | `consumer_id`、`consumed_sha256`、`subject`／`scope`、`readback_at` | Consumer readback | `NOT_OBSERVED` |
| ABI readback | `package_sha256`、`subject`、`scope`、`unknown_fields[]`、`legacy_payload` | Consumer echo | `ABI_LOSSY_CROSSWALK` |

**Oracle 凍結**：作者 oracle 在執行前固定於本節；不得在看到結果後降標、刪 Case 或改 threshold。原 Case 的 POS／NEG 不因本輪作者測試而通過。

## 09.3 A01–A08 的 W1 適用項

| ACC | W1 檢查 | 本輪結果 |
|---|---|---|
| A01 Source | 17 源 SHA；W0 primary tree；33/34 一致 | `SELF_CHECK_PASS_WITH_FINDING`（receipt stale） |
| A02 W0 extraction | L1 15 檔／13 源、G4／SQS 限制、CH-07 分帳 | `SELF_CHECK_PASS` |
| A03 High retention | 13 章、6 WP、8 原 Case、4＋ W0 HOLD、U-017 9/9、U-028 3/3 | `SELF_CHECK_PASS` |
| A04 W1 | 四 API 名、逐欄 crosswalk、三 Host＋三 Hermes、`HOST_PENDING` | `SELF_CHECK_PASS` |
| A05 W2 | N/A（W1 不執行 Effect） | `N/A` |
| A06 W3 | N/A（W1 不執行 Challenge） | `N/A` |
| A07 W4 | N/A（W1 不簽 Assurance） | `N/A` |
| A08 Closure | 與 W2／W3 的 handoff 欄一致；正文可讀 | `SELF_CHECK_PASS` |

---

# 10｜Claim／Stop／Resume／HOLD

**Input → Design Operation → Output／Consumer／NEG**

## 10.1 六維 Claim Ledger

| 維度 | 本波可宣 | 不可宣 | 證據 |
|---|---|---|---|
| Author | W1 十三章、crosswalk、四 API 契約、九 child | 作者即原域 | 本檔 |
| Source | 17 源 SHA 重算；W0 PRIMARY 33/34；pack 27/27 | Original Reader ACK | E1 |
| ABI | 逐欄 crosswalk 完成 | Consumer 已接受 | §06.4 |
| Host | `HOST_PARTIAL_LOCAL_ONLY`（Codex） | 三 Host PASS／Consumed | §05 |
| Independent | `NOT_CLAIMED` | `INDEPENDENT_PASS` | Checker HOLD |
| Release | `NOT_CLAIMED` | `RELEASED` | Publisher HOLD |

## 10.2 具名 HOLD／FirstFail／Owner／Resume

| HOLD／FirstFail | 真缺口 | Owner | 解除最小證據 | 受影範圍 |
|---|---|---|---|---|
| `W1_HOST_NINE_GRID` | ChatGPT／Hermes 全態與 Codex Installed／ActualServed／Consumed 未觀測 | 各 Plugin／Host Owner | 每 Host manifest／LoadedSHA／Invocation／Consumer readback | Host claim |
| `W1_PLUGIN_ALIAS` | 只見 `sbl-tpm-sp`，未見 `tpm-sp-plp` 同 manifest | Plugin／Host Owner | 原 manifest／Loaded ID 同一性 | alias claim |
| `W1_ABI_BOUND` | Guide／Bridge proposal-2 無真 Consumer crosswalk | Guide／Bridge ABI Owner | 逐欄 field→target→loss→readback | ABI claim |
| `W1_W0_INPUT` | W0 只有作者 pack，無真 Host Raw | W0 Wave Owner | 只接受作者 Source／Case／Proposal | W1 輸入 |
| `W0_PRIMARY_RECEIPT_STALE` | `PRIMARY_RECEIPT.json` 實體 4,222／`6dbdd7bd` vs 清冊 3,986／`18ad4b8d` | W0 Wave Curator／Human Owner | 重算或更正 manifest，或書面確認 receipt 為後加 | source claim |
| `W0-A_CASE_SELECTION` | 6 候選無 Owner 指名 | Original Project／Source Owner | G4／SQS 指名或 typed ReasonedNA | Case claim |
| `W0-B_NOT_ADMITTED` | 13 前件 UNBOUND | Original Issuer／Repo／Host | 13 前件 typed receipt | W2 前件 |
| `ORIGINAL_READER_UNBOUND` | 無原 Canonical Reader | Original Reader Owner | 同 Scope typed readback | 全波 |
| `CHECKER_PUBLISHER_UNBOUND` | 無 Protected Checker／Publisher | Checker／Publisher | 同 Candidate 的 distinct receipt | Independent／Release |

## 10.3 Stop 與 Resume 規則

**Stop**：缺原 Reader／Issuer／Host／Runner／Checker／Publisher 時，只停該受影 claim；不停其他合法作者章節。外部 HOLD 不要求清零才交文檔。
**Resume**：每個 HOLD 的 resume predicate 必須是同 Subject／Scope（必要時同 Host／PolicyEpoch）的 typed receipt；不得以本地檔、`permit=true`、skill 可讀或 public commit 補位。
**NEG**：缺原 Effect 卻把所有 Claim 一起停 → `CLAIM_CEILING_VIOLATION`；W4 Release 當 W0 READ 前件 → `PHASE_OVERREACH_CANDIDATE`；FAIL 改名 HOLD → `FALSE_AUTHORITY`。

---

# 11｜ExecutionPackSplit（15 檔完整切分設計；本輪不生成檔案）

**Input → Design Operation → Output／Consumer／NEG**

本節是**下游 W1 Pack Author／Bridge 可直接消費的工程內容**：從本冊節／欄位／操作映射到每個未來檔的內容、原 ABI／Consumer、required／optional、拒收與待綁定方式。不是只列 15 個檔名，也不是在本輪生成 15 檔。

## 11.1 切批策略與依賴

| Batch | Scope | 包含 WP／Case | 依賴 | 可並行 | 出口 |
|---|---|---|---|---|---|
| W1-B1 Identity | plugin／alias／Host capability | P01、W1-R3-02 | 無 | 與 B2 的 crosswalk 文件可並行 | `HostCapabilityLedger` |
| W1-B2 ABI | Guide／Bridge 三 namespace、四 API | P02、P03、W1-ABI-01／02 | B1 的 source ledger | 與 B3 的 fixture 可並行 | `ContextBundle` 設計 |
| W1-B3 Adversarial | scope／unknown／path／secret | P05、W1-SEC-01、W1-API-01 | B2 | 與 B4 文件可並行 | `AdversarialABIReport` |
| W1-B4 Host | 三 Host 逐態 | P04、W1-HOST-01..03、HERMES-01 | B2／B3 | 各 Host 可並行，但不得互相抵帳 | `HostObservationLedger` |
| W1-B5 Closure | AsBuilt／handoff | P06、R3-01..05 | B4 或 HOLD | — | `WaveClosure` |

**依賴規則**：B2 不得在 B1 的 source identity 未定前宣完整；B4 不得在 B2 的 ABI 未定前宣 Invoked；B5 不得把 B4 的 `NOT_OBSERVED` 寫成 PASS。W4 Release 不得倒卡 B1 READ。

## 11.2 15 檔逐項映射

| # | 未來檔 | 必要內容（本冊來源） | 關鍵欄位 | 前件 | Consumer | 拒收／待綁定 |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_MANIFEST.json` | §00.2 的 17 源；W1 當批選擇、locator、bytes／lines／SHA、span；SELECTED_ONLY／CORE16 適用 | `source_id,path,sha256,bytes,lines,selection_mode` | 真來源可回取 | Source Curator／Bridge | 假 SHA、缺 bytes → `SOURCE_INTEGRITY_FAILED` |
| 2 | `PACKAGE_FILE_MANIFEST.json` | §11.2 全部必要 body／resolver／fixture；hash 排除與自排除 | `identity, files[], self_excluded:true, duplicates_rejected:true` | 檔案集合已凍結 | Pack Author | 自指、symlink、duplicate、path escape → `PACKAGE_INTEGRITY_HOLD` |
| 3 | `00_WAVE_RUN_MANIFEST.json` | §00／§01／§07；WaveControl 六身份、scope、effect、cases、claim | `project_id,subject_id,scope,wave_id,batch_id,source_manifest_sha256,claim_ceiling` | SourceManifest SHA | Executor／Program | legacy@1、假 receipt → `SCHEMA_UNSUPPORTED` |
| 4 | `00_WAVE_RUN_MANIFEST.md` | §01 Goal／FUO／§07 operation／§10 NEG；首 900 bytes 放 `FHS5_IDENTITY` | 目標、操作、Consumer、NEG／FirstFail、身份投影 | 同 JSON identity | Operator／Guide | 身份與 JSON 不符 → `IDENTITY_MISMATCH` |
| 5 | `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | §02 原義務、§03 選型、§04 前件、§06 ABI、§07 operation、§08 ECP | 原 ID、scope、non-goal、owner、construction plan | 原 PI／PD ref | Pack Author／Executor | 只寫「參見藍圖」→ `AUTHOR_BODY_INCOMPLETE` |
| 6 | `02_ORIGINAL_CONTRACT_REFS.json` | §02／§04／§05／§06／§09 的原 PI／PD／ECP／TQAEP ref；未讀回 null | `refs[]{kind,original_id,sha256,span,reader_state}` | 原 Reader | Bridge／Executor | 假 receipt → `FALSE_AUTHORITY` |
| 7 | `03_DEV_ECP.md` | §07／§08；Guide／Bridge render 的 Pre／Post／WriteSet／readback／rollback／idempotency | `effect,permission,write_set,pre,post,readback,rollback,retry` | 原 DEV ECP | Repo Owner | 未准入寫「可執行」→ `ECP_NOT_GRANT` |
| 8 | `04_OPS_ECP.md` | §05／§08；HostID／Principal／Epoch、Host-specific recovery | `host_id,principal,policy_epoch,pre,post,world_reader,recovery` | 原 OPS ECP | Host Owner | `git revert` 當 OPS recovery → `RECOVERY_KIND_MISMATCH` |
| 9 | `05_PLANNED_TQAEP.md` | §09 原 Case／Oracle／Fixture／ExpectedRaw／Checker；POS＋NEG | `case_id,kind,requirement_ref,oracle,fixture,expected_raw,checker` | Case registry | Original Case Owner | 只有 JSON、無 NEG → `TQAEP_CONTRACT_MISMATCH` |
| 10 | `05_PLANNED_TQAEP.json` | §09／§11 的 `projection_of_sha256`、`cases[]` 與 WaveControl 相等 | `projection_of_sha256,cases[]` | MD 真 SHA | Pack Author | projection 不等 MD SHA → `PROJECTION_MISMATCH` |
| 11 | `06_PERMISSION_STOP_RESUME.md` | §05／§08／§10；Issuer、准入、stop scope、resume、UNKNOWN reconcile | `issuer,admission,stop_scope,resume_predicate,unknown_route` | 原 Issuer | Program／Operator | `permission=true` 當 Grant → `FALSE_AUTHORITY` |
| 12 | `07_EVIDENCE_AND_CHECKER.md` | §09／§10／§12；Frozen／WorldRaw／NotCovered／Checker 路由與效力 | `evidence_refs,not_covered,checker_route,claim_effect` | Frozen candidate | Checker／Consumer | 作者自檢當 Independent → `FALSE_INDEPENDENT` |
| 13 | `08_AS_BUILT_AND_HANDOFF.md` | §12；actual／expected 分帳、LastGood、change cone、未來 Wn raw | `actual,expected,lastgood,change_cone,handoff` | 真 Raw 或 HOLD | 下一波／Owner | 未跑填 PASS → `AS_BUILT_OVERCLAIM` |
| 14 | `09_README_RUN_ORDER.md` | §07／§08／§09／§10；依真依賴與權限的 run order、失敗與續工 | `steps[],preconditions[],failures[],resume` | DAG | Operator | 順序違反 DAG → `RUN_ORDER_CYCLE` |
| 15 | `{wave_id}_START_THIN_PROMPT.md` | §06／§07／§11；只引用真小包與來源的 ThinStart | `package_sha256,subject,scope,goal,fuo,done,effect,owner,next,stop,resume` | Package identity | Guide | 另造 scope／permission → `SCOPE_DRIFT` |

## 11.3 Wn 六身份與 MD 投影

`project_id, subject_id, scope, wave_id, batch_id, source_manifest_sha256` 六鍵必須在 WaveControl JSON、十份 MD 首 900 bytes 的 `FHS5_IDENTITY`、Case Join、Projection SHA 中一致。`WaveControl.wave_id` 是 `W1`（或實際批次），WM 的 `wave_id` 是 `FHS-5_PLP_W1M`；兩者共享血緣但不強迫字串相等。`05_PLANNED_TQAEP.json.projection_of_sha256` 必須等於 `05_PLANNED_TQAEP.md` 的真 SHA；`cases[]` 必須與 WaveControl 的 cases 逐欄相同。

**Case Join 欄位**：`case_id, kind, subject_id, scope, requirement_ref, requirement_source_sha256, clause_start_line, clause_end_line, clause_text, oracle_path, oracle_sha256, fixture_path, fixture_sha256, expected_raw`。至少一 POS 一 NEG；原 Oracle／Fixture 必須在 admitted root；未跑案例不得生成 fake command／Raw。

**FileManifest 規則**：不自包含自身 digest；拒絕 symlink／junction／duplicate key／path escape；封存順序為檔案內容→FileManifest→SourceManifest→WaveControl→Projection→FHS5_IDENTITY。`SOURCE_MANIFEST` 不自帶 identity（W0-F-09）。

**BodyResolver 兩路**：A. 授權離線根內真 bytes＋manifest SHA／span；B. 原 OriginalReader 按 original_ref 同 Scope／Host／Epoch 回取。只拿 URL、SourceSHA 或助手回覆不算原 Reader。

## 11.4 六 WP 的 dry-consume（代表 Slice）

| WP | 代表 Slice（covered IDs） | 來源 | Operation → 輸出 | ABI／Consumer | Case／POS／NEG | Recovery／Resume | 未來檔／欄位 |
|---|---|---|---|---|---|---|---|
| P01 | ChatGPT Loaded＋Codex Invoked（U-017/ChatGPT/Loaded、U-017/Codex/Invoked） | plugin path、session capability、W0 identity | 建 capability ledger；標 `NOT_OBSERVED`／`TOOL_CALLS_LOCAL` | Host Owner；`HostCapabilityLedger` | W1-HOST-03 NEG；W1-R3-02 | 缺 loader → `W1_HOST_NINE_GRID` | `00_WAVE_RUN_MANIFEST.json.host_claims[]` |
| P02 | `GuideThinPrompt.package_sha256→WaveControl.source_manifest_sha256`（CG-R2-REQ-01、PCB-FR01） | B02／B03、W0 SM | 複製＋重算；unknown 保留 | Guide／Bridge ABI Owner | W1-ABI-01 NEG | 漂移 → `SOURCE_IDENTITY_HOLD` | `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` §ABI |
| P03 | `inspect_package` 以 34/33、27/27、13 源作輸入（PCB-FR02..05、W1-API-01） | W0 PRIMARY、13 源 | 產 source_refs／unresolved_refs；BodyResolver 檢查 | Executor／Reader | W1-API-01 POS `NOT_RUN` | path escape → `PATH_OUTSIDE_ROOT` | `05_PLANNED_TQAEP.json.cases[]`＋`07_EVIDENCE_AND_CHECKER.md` |
| P04 | Hermes Kanban／Delegation／Swarm 三格（U-028 三 child、W1-HERMES-01） | Host settings／reader（缺） | 三格獨立 observation | Hermes Host Owner | W1-HERMES-01 POS `NOT_OBSERVED` | 缺 Host → `W1_HOST_NINE_GRID` | `00_WAVE_RUN_MANIFEST.md` Host 段 |
| P05 | scope widen／unknown／path／secret 四類（W1-ABI-02、W1-SEC-01、F5-W0-T06/T07/T23） | 本冊 §06.4／§09 fixture | 產 expected／observed／firstfail | Reviewer／Bridge Owner | 四 NEG 可重播 | 改 oracle → `ORACLE_DRIFT` | `07_EVIDENCE_AND_CHECKER.md` |
| P06 | W1→W2 adapter interface（W1-R3-01、W1-R3-05） | P01–P05 輸出、CH-07 | 分 actual／expected／not-covered | W2 Program | W1-R3-05 NEG | 無 delta 重做 → `PHASE_OVERREACH` | `08_AS_BUILT_AND_HANDOFF.md`、ThinStart |

**全量覆蓋說明**：上表六個 slice 只作下游可消費性測試；全量原義務仍逐項在 §02、§06、§09 與附件 E3 對位。Slice 不取代全量，也不把未列 Case 刪除。

---

# 12｜As-Built／Handoff／Next Wave

**Input → Design Operation → Output／Consumer／NEG**

## 12.1 本輪 As-Built（作者實績）

| 項目 | 實際 | 狀態 |
|---|---|---|
| 來源釘選 | 17 源逐檔 bytes／lines／SHA 重算；pin set `4b08a458…` | `READ_VERIFIED` |
| W0 PRIMARY | 34 entries、tree `f27263d8…`、33/34 一致；receipt stale 具名 | `PASS_WITH_NAMED_FINDING` |
| W0 workspace | 319 files、318 manifest＋self、tree `e1d9770b…` | `READ_VERIFIED` |
| G4／SQS | bytes／SHA 實讀；3 tests `REPORTED` 未重跑；SQS 無 executable oracle | `READ_VERIFIED`／`REPORTED` |
| GitHub | DNS 失敗；用歷史 pin，不宣 live read | `PUBLIC_EXPORT_UNAVAILABLE` |
| 本正文 | 00–12 十三章、6 WP、8 原 Case、9＋3 child、四 API、15 檔映射 | `PD_AUTHOR_CANDIDATE` |
| 未做 | Native、Wn 15 檔、原 Runner、Independent、Release | `NOT_RUN`／`UNBOUND` |

## 12.2 W0 真實 AsBuilt（歷史證據，非本輪重跑）

| 事實 | 值 | 效力 |
|---|---|---|
| W0 15 normative＋13 sources | byte 相同；`SOURCE_MANIFEST.json` `22eebb6c…` | `REPORTED`／`READ_VERIFIED` |
| pack | 28/28；`PACKAGE_FILE_MANIFEST.json` `bcb93066…` | `READ_VERIFIED` |
| TQAEP | 24/24 規劃 | 規劃≠執行 |
| W0-C | 1011/1011；576 ID＋435 slot；485/485、35/35、56/56；全 `UNVERIFIED`；0 install | 分母帳 |
| F／CH／N | F 11/11、CH 7/7、N 9/9 `CLOSED_LOCAL`；2 original actions open | 作者收斂 |
| CH-07 | identity-only：`743c6cf`／`80833a5f`；`DEPLOYMENT_VERIFICATION.json` removed；25 modified 舊 bytes 不在 | `NOT_COVERED` |

## 12.3 跨 WM 交接（W1→W2／W3／W4）

| 交接項 | 給 W2 | 給 W3 | 給 W4 |
|---|---|---|---|
| 輸入 | 四 API interface、Host adapter 設計、`W1_ABI_BOUND` | Frozen 可用的 Source／Case 結構、`W1_R3` 反例 | Host Fit 欄、Generic 候選限制 |
| 不可用 | 不得把未 consumed 當 Native 前置 | 不得把作者 fixture 當原 Runner | 不得把 W1 作者 PASS 當 Independent |
| ExpectedRaw | Host 七階段、Invocation／Served／Consumed | 五 pin、Finding 八欄 | Profile／License／Consumer |
| 具名限制 | `W1_HOST_NINE_GRID`、`W1_PLUGIN_ALIAS` | `W1_ABI_BOUND`、`W0_PRIMARY_RECEIPT_STALE` | 同上 |

### 12.3.1 欄級 handoff（W1→W2）

| producer field（W1） | consumer field（W2） | transform／validation | loss／unknown | NEG／FirstFail | consumer readback |
|---|---|---|---|---|---|
| `inspect_package.response.source_refs[]` | `02_ORIGINAL_CONTRACT_REFS.json.refs[]` | filter `kind=source`；重算 SHA／span | `unresolved_refs[]` 保留 | `SOURCE_IDENTITY_HOLD` | W2 refs echo 同 SHA |
| `inspect_package.response.effect_constraints[]` | `01_SOURCE_SCOPE...effect_constraints[]` | 只作 advisory；不產生 token | 未知 effect 保留 | `EFFECT_UNBOUND` | 原 EffectRegistry 對照 |
| `ContextBundle.context_sha256` | `03_DEV_ECP.pre.context_ref`／`04_OPS_ECP.pre.context_ref` | 直接複製＋重算 | Scope mismatch 停 | `CONTEXT_SCOPE_MISMATCH` | ECP pre 回讀同 SHA |
| `HostCapabilityLedger.host_claims[]` | `02_ORIGINAL_CONTRACT_REFS.host_refs[]` | observation 類型原樣 | `NOT_OBSERVED` 不升 true | `W2_HOST_BIND` | 原 Host readback |
| `compare_context.changed[]` | `01_SOURCE_SCOPE...change_cone[]` | exact `(kind,path,sha)` | 不作語義推論 | `DELTA_UNVERIFIED` | 兩期 raw |

---

## 12.4 未來 Wn 回寫契約（本輪不生成）

以下只保留**契約**，供未來合法 W1 Wn 任務依真 candidate／Raw 產出；本輪不生成 `FHS5_Wn_WRITEBACK.json`，也不把本正文 SHA 當 Wn candidate SHA。

| 欄位 | 型別 | 意義 | 本輪值 |
|---|---|---|---|
| `schema` | string | 固定 `FHS5.PLP.Wn.Writeback@local-1` | `DEFINED_NOT_EMITTED` |
| `wave_id` | string | 未來 Wn 的 wave（例 `W1`） | `null` |
| `subject_id` | string | 同 Wn subject | `null` |
| `source_manifest_sha256` | 64-hex | 未來 SourceManifest | `null` |
| `base_primary_selection` | string | 例 `W0-PRIMARY-SEL-20261124-01` | `W0-PRIMARY-SEL-20261124-01`（歷史） |
| `candidate_sha256` | 64-hex | 未來真 candidate | `null` |
| `changed_artifacts[]` | array | path／bytes／sha256 | `[]` |
| `tests[]` | array | id／command／exit／raw_sha256 | `[]` |
| `holds[]` | array | id／reason／owner／resume | 本冊 §10.2 可作輸入 |
| `original_actions[]` | array | 原域待辦 | 本冊 §10.2 |
| `claim_ceiling` | string | 不得高於實際 | `AUTHOR_DESIGN_ONLY` |
| `owner` | string | Wave Curator／Human Owner | 同 |

**回寫條件**：真 Wn candidate 已存在、Tests 有 raw、Holds 具名、Owner 簽收；否則保持 `EXPECTED_NOT_OBSERVED`。不得用本正文 digest 冒 `candidate_sha256`。

## 12.5 NEG 與 FirstFail

| 反例 | FirstFail |
|---|---|
| 以 r4 覆 r5 | `SOURCE_IDENTITY_HOLD` |
| W0 作者 pack 當 Native | `FALSE_AUTHORITY` |
| G4 當 E2E | `HOST_PENDING`／`QUALIFICATION_UNPROVEN` |
| 485 當 install | `DENOMINATOR_LOSS` |
| r5 當 Release | `FALSE_RELEASE` |
| 未跑 Wn 填 AsBuilt PASS | `AS_BUILT_OVERCLAIM` |

**本冊終點**：`PD_AUTHOR_CANDIDATE`；WM 完成即停止，不跨入 W1 十五檔或 W2 Effect。