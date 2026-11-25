# FHS-5_PLP｜W0M｜Native-first 主用可執行版｜完整實質正文

**artifact_id**：`FHS5-PLP/W0M/PRIMARY-EXECUTABLE-NF-20261125-03`
**wave_id**：`FHS-5_PLP_W0M`　**subject**：`FHS-5_PLP/W0M`
**version**：`CODEX-FIRST-r4`　**日期**：2026-11-25（Asia/Taipei）
**base_artifact**：`FHS5-PLP/W0M/AUTHOR-CANDIDATE-20261123-02`（原 `candidate-v2`）
**base_artifact_sha256**：`3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd`
**original_base_sha256**：`8b8145c8ec34d3cfb23b551d3a1cdc7bb340b72d40c73b2947d92fd15d9b4128`（歷史 candidate-v2 卷首 base，不是本輪 raw 底本）
**supersedes_candidate_sha256**：`51c994f9e2ccccc14676f02bd84549fa12a91a4377e1dcfeee8b39e5316ddd43`（NF-r2 正文 raw SHA）
**supersession**：`SUPERSEDED_BY_HUMAN_OWNER_CODEX_FIRST_DECISION_W0-CODEX-FIRST-20261125-01`；本檔保留 NF-r3-PRIMARY 全文，僅就 §00.2.2、§05.1、§05.5 #5、§08.1、§08.5 作 CODEX-first 修訂。
**design_basis**：`NF-PLAN-r1`（`9efa36535762edcbc005f56ecc4687f009e9692c1ca2116919f48a58365d7b85`）、`WORK-W0M-NF-r1`（`1d7f1c53184967937fe468fe58b3ec8056ec5848fd77e62021546880973572f4`）。
**review_basis**：`REVIEW-W0M-NF-r1`（`ca5b55a00e86b4d94b66139ace73d807b3e965cffb3037f2b99594b8d92ff665`）；本版逐項關閉 BLK-01/02、MAJ-01..04、MIN-01..05。
**promotion_basis**：使用者（Human Owner）於 2026-11-25 直接授權升格為主用並可執行；授權記錄見 §00.2.2。
**author_scope**：FHS-5 本地 primary W0M Current；含 00–12、14 WP、24 原 Case、七 Seam、NF-R/T 與六檔 W0 包編製契約；授權進行受界的 W0/B0 本地執行。不含外部發布、跨專案部署或原域 PASS。
**author_state**：`PRIMARY_USE_SELECTED_AUTHOR_SELF_CHECK_PASS`
**claim_ceiling**：`PRIMARY_LOCAL_W0M_CURRENT_WITH_SCOPED_EXECUTION_AUTHORIZATION`
**not_claimed**：`B0_NF_VALIDATED / W0_NF_VALIDATED / NATIVE_PASS / INDEPENDENT_PASS / W1_TECHNICALLY_READY / W1_EXECUTION_READY / RELEASED / EXTERNAL_OS_REPO_HOST_GRANT`
**evidence_appendix**：[FHS-5_PLP_W0M_證據附件.md](FHS-5_PLP_W0M_證據附件.md)

**卷首讀法**：本冊是 FHS-5 本地 primary W0M Current，已由使用者授權受界執行；它不是 W0 六檔控制包，也不是產品驗收報告或外部原域採納收據。文中 `PLANNED`、`NOT_RUN`、`UNVERIFIED`、`UNBOUND` 仍是實際狀態；任何「PASS」只指文件自檢或來源位元核對。來源優先序為：使用者主用／執行授權與 NF-PLAN-r1 → 原 W0M 的有效責任 → MASTER/PROG/PROJ 的未受影原意 → 實際證據；歷史討論與舊綠燈只能作 SUPPORT。

---

# 00｜Identity／Authority

**章契約**｜Input：本輪指示、NF-PLAN-r1、WORK-W0M-NF-r1、原 W0M candidate-v2、上位七冊與既有 W0/W1 證據。Operation：建立單一新版身份、法位、來源釘選與 claim 邊界。Output：FHS-5 本地 primary W0M Current＋受界執行授權記錄。Consumer：W0 Pack Author、Program Owner、五方 Owner、Reviewer、Executor。ACC：身份一致、法位可回取、作者／主用／產品完成分離。NEG：同名舊件、假 Owner 採納、把文件自檢或主用授權當 Native PASS。FirstFail：`IDENTITY_DRIFT`、`FALSE_AUTHORITY`、`CLAIM_CEILING_VIOLATION`。

## 00.1 身份與責任邊界

| 欄位 | 本冊值 | 說明 |
|---|---|---|
| `project_id`／`subject_id` | `FHS-5_PLP`／`FHS-5_PLP/W0M` | Wave Master 層，不是產品 `W0` 控制包 |
| `artifact_id` | `FHS5-PLP/W0M/PRIMARY-EXECUTABLE-NF-20261125-03` | FHS-5 本地 primary W0M |
| `version` | `NF-r3-PRIMARY` | 以主用升格取代 NF-r2；保留 NF-r1/NF-r2 SHA 作血緣 |
| `base`／`supersedes` | `candidate-v2`（raw `3acac018…`）／NF-r2 `51c994…` | 原 14 WP、24 Case、七 Seam 的血緣底本；`8b8145…` 只作歷史 base |
| `profile` | `GENERIC_NATIVE_FIRST + FHS_LEGACY_REGRESSION_OPTIONAL` | Generic 為主；FHS 相容只在採納及適用分母內 |
| `author_scope` | 本地 primary Current＋受界執行授權 | 可編 W0 六檔、執行 B0 設計範圍；外部權限仍須真實 |
| `claim_ceiling` | 本地主用、受界可執行 | 不是 `W0_NF_VALIDATED`、Native 或 Release |
| `evidence_appendix` | `FHS-5_PLP_W0M_證據附件.md` | 來源、差額、DOC 檢測與後續交接，不另立規格 |

**作者完成與產品完成分離**：

1. 本輪完成的是「把 W0 應該做什麼、如何施工、如何否證、如何交接」寫成可讀契約。
2. 產品完成必須另有一份受權 W0 控制包、真 Repo/Host 探查、真 DEV/OPS、獨立 Checker、actual raw 與 consumer readback。
3. 本冊的 `AUTHOR_SELF_CHECK_PASS` 只覆蓋 DOC-01..05 文件驗收；不得轉寫為 `B0_NF_VALIDATED`、`W0_NF_VALIDATED`、`NATIVE_PASS` 或 `RELEASED`。
4. `FHS-5/W0/B0-NF` 是 PLAN 建議的最小執行 Batch，不是原 W0-B（Protected Native）分線，也不是 SST 的 B0。
5. 本次主用升格與執行授權只影響 FHS-5 本地 Current 的可用性與受界施工，不把上述產品／外部 claim 自動升格。
6. 後續 B0 若發現真差額，依 §10 的 FirstFail/ChangeCone 局部暫停與修補；不以「已主用」掩蓋失敗或跳過獨立驗收。

## 00.2 本輪作者重構依據與法位

使用者本次已直接作出 FHS-5 本地主用與受界執行授權；不把「主用」寫成外部產品或 Host 的原域 acceptance。以下是本輪授權記錄：

### 00.2.1 單人 Owner 與 issuer 通則

在 FHS-5 範圍內，**唯一 Human Owner 是唯一的產品設計採納與內部授權／簽核決策來源**。`issuer` 是 Owner 的授權責任與可追溯決策，不是必須新建的 Runtime 服務；不得因「缺 Issuer」再建 Queue、Registry、簽核平台或第二位人類。

1. Owner 可在一次決策中指定 scope、operation、write-set、allowed roots、期限與撤權條件；在此範圍內由代理／會話／工作樹自主讀取、施工、檢測、修補、重驗。
2. 只有真差額、越界／風險變更、不可逆操作、公開發布或原外部政策要求的重大變更，才回 Owner；普通 READ、受影修補與 WP 推進不需要第二位人類聯署。
3. Repo Owner、Host Owner、Source Curator、Reviewer、Challenger、Checker、Consumer、Publisher 是**責任**，不是額外必需的人類角色。Owner 可委派不同代理／會話／工作樹履行；外部 OS/Repo/Host/Publisher 權限仍須真實存在，Owner 不得自造。
4. Maker 與 Challenger／Independent verifier 至少分離 session/worktree；若原政策要求不同 principal，必須真不同 principal。相同模型或同一把 write key 不構成獨立。
5. Checker 與 Consumer 是同 Scope 的**兩個 distinct receipts**：Checker 給 assurance verdict，Consumer 給接收／使用回執；一個簽章或一份 manifest 不得兼任兩者。Publisher 只按原發布程序 Release，不在 B0 的必要範圍。

### 00.2.2 主用與受界執行授權記錄

| 欄位 | 實際值 |
|---|---|
| `decision_id` | `W0M-NF-PRIMARY-20261125-01` |
| `decision_kind` | `HUMAN_OWNER_LOCAL_PRIMARY_PROMOTION_AND_SCOPED_EXECUTION_AUTHORIZATION` |
| `codex_first_decision` | `W0-CODEX-FIRST-20261125-01`（Human Owner 正式裁決：CODEX-first／Native-first；本檔受影條款隨之修訂） |
| 決策人 | 使用者（Human Owner） |
| 日期／時區 | 2026-11-25（Asia/Taipei） |
| 適用 Subject／Scope | `FHS-5_PLP/W0M`；`FHS-5/W0/B0-NF` 的 W0M → W0 Pack → B0 本地執行 |
| 採納 ADR | NF01–NF10（本冊 §00.3） |
| 授權 Effect | `SOURCE_READ`、隔離 `DRAFT`、多個受界可逆 `DEV`、本地 `OPS` run/readback/restore；同一有效授權內可自主接續多個必要操作與迭代，不逐次回 Owner；B0 五方代表能力與獨立驗收 |
| 允許 Roots | 由 Owner 在 W0 控制包或後續指示中指定的工作區、產品 checkout、sandbox、source root、evidence root；未指定前不得寫入 |
| 寫入 Set | 以 §04 的逐檔 write-set/preimage 為準；不得全 repo glob |
| 外部／發布 Effect | `USER`、`RELEASE`、遠端部署、跨專案寫入仍需原 consent/Publisher/ACL 與真權限；本授權不自動授予 |
| 期限／撤權 | 至 Owner 撤權、Scope/Repo/Host/Effect 變更或安全 Finding 為止 |
| 代理與 SoD | Owner 可委派多個代理／session/worktree；Maker 與 Checker 分離；Checker/Consumer distinct receipts |
| 回 Owner 條件 | 真差額、越界、風險變更、不可逆 effect、發布或原外部政策要求的重大變更 |

**不可誤讀**：此授權是 FHS-5 內部的設計採納與本地執行許可，不是 OS/Repo/Host 的管理員權限、不是 Publisher receipt、不是 `B0_NF_VALIDATED` 或 `W0_NF_VALIDATED`。若真實 ACL、grant、preimage 或安全前件不存在，受影 effect 仍必須 `NOT_ADMITTED`。OPS 依 `W0-OPS-NATIVE-20261125-01` 的本地 CODEX Native OPS ECP 承接，不再要求舊框架 Original OPS ECP typed ref。

## 00.3 NF-ADR：本冊採用的最小上位裁決

| ADR | 本冊有效規則 | 取代／隔離範圍 | 驗收與負例 |
|---|---|---|---|
| NF01 | Native Executor 是唯一調度與恢復主體；FHS-5 五方是可獨立調用的工程工具，不建立第二 Runtime／Queue／Dispatcher／Issuer | 舊「FHS 必須掌控 Native LOOP」的假設 | 五方可獨立 invoke；無常駐第二調度器；以裸 Hermes 冒充五方 PASS 則拒 |
| NF02 | Generic Native 不預設 HGK／FABRIC／SBL／FHS／PIPD 運行契約；Legacy Compatibility 必須明示選用、獨立分母 | 舊 Generic 冷啟的框架硬依賴 | 無舊 provider 冷啟、同 Scope 功能 parity；只改環境變數不算 OFF 證據 |
| NF03 | 原 Reader／EffectRegistry／CaseRegistry／RawSchema／專屬 Runner／ACK 不是通用 mandatory 服務；由真檔案/Git、實際權位、既有測試器、獨立 oracle 與直接 consumer readback 承接有效責任 | 舊 W0M §04–10 的 universal binding request | 無 OriginalReader 仍可合法讀；無 Registry 仍可測試；偽造 ID/ACK 拒 |
| NF04 | 每一 HardEdge 必須有原需求／安全／當期技術必要性、具名 producer 與可執行取得途徑；後波輸出與同操作後驗不得作前置 | 舊 DAG 的順序硬化與後驗倒置 | 真 DAG 無環；缺 producer 的必需邊不得留白；`GATE_CYCLE_CANDIDATE` 拒 |
| NF05 | PI/PD/ECP/TQAEP 是設計；READ、隔離 DRAFT、DEV、OPS、外部效應、發布分開授權；無真權限不跑 | 舊「文件核准即效果核准」 | 越權 no-op；未知 effect 不默認 READ；假 permit 不生效 |
| NF06 | 五方獨立使用；七 Seam 是必要資訊交換，不是全域 ABI Gate；只有真 consumer 實際消費才算接上 | 舊「七 Seam 全鏈才能做任何事」 | Bridge/FAR OFF 時，合法 direct 工作可繼續；B0 的五方產品驗證不得被旁路取代 |
| NF07 | W0 先實證，B0 最小；W1 的完整三 Host/W2 全 effect/W3 深迭代/W4 發布不倒卡 B0 | 舊 W4 Release 倒灌 W0 READ | 合法 READ 不受 W1–W4 未完成影響；B0 不因文件量大自動升級 |
| NF08 | W0 後續包以 §11 的六檔為單一真源；舊 15 檔只在實際 consumer 需要時生成版本隔離的衍生 projection | 舊 15 檔雙寫、自循環 manifest | 六檔可施工；舊 projection 不得反向成為新 canonical；空殼包拒 |
| NF09 | 原 ID、Case、Receipt、分母永保追溯；新版必要性按 Requirement/Case crosswalk 決定；未測、延期、NotCovered 不計 PASS | 舊「1011/485 全綠才算 Generic 可用」 | 原分母與新分母分帳；Legacy 未驗不抵 Generic，也不冒充 Legacy PASS |
| NF10 | 失敗必記 FirstFail、ChangeCone、Owner、LastGood 與下一合法動作；只停受影效果，不全域封死 | 舊「缺件即整個 W0 HOLD」 | 權限/來源/設計/程式/架構/驗收分流；無新 delta 不重派 |

## 00.4 來源釘選與版本處理

本冊直接使用的來源與實算身份如下；完整 ledger、讀取層級與章節定位見證據附件 E1。

| ID | 來源 | bytes | SHA-256 | 本輪用途 |
|---|---|---:|---|---|
| `PLAN` | `FHS-5_PLP_W0_MASTER_Native-first重構方案.md` | 69,997 | `9efa36535762edcbc005f56ecc4687f009e9692c1ca2116919f48a58365d7b85` | NF01–NF10、B0、六檔、TQAEP、回寫 |
| `CTRL` | `FHS-5_PLP_W0M_Native-first_GPT_WORK_最小執行控制包.md` | 17,668 | `1d7f1c53184967937fe468fe58b3ec8056ec5848fd77e62021546880973572f4` | 本輪 A1–A4 與 DOC-01..05 |
| `W0M-OLD` | `FHS-5_PLP_W0M.md`（candidate-v2） | 29,460 | `3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd` | 14 WP、24 Case、七 Seam、原 HOLD |
| `M` | MASTER r3 完整實質正文 | 325,511 | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` | 產品原意、七 Seam、W0 基線 |
| `B00` | PROG-00 r4a | 79,605 | `fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2` | Program、W0/Wn 責任 |
| `B01`–`B05` | PROJ-01～05 r4a | 48,177／47,039／39,898／40,665／51,163 | `30058864…`／`1a9fd643…`／`9ce12fd8…`／`619c5a93…`／`f6f043e1…` | 五方產品責任 |
| `WM` | 全 WM r2 | 286,201 | `d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2` | Wn 章節模板、後波責任 |
| `W0-CLOSE` | W0 PRIMARY 交接 | 2,840 | `994264b1273e7127f032e41c72b7a97b0bf8e30139bcbab20eec1e543b5faeb3` | 既有綠燈、HOLD、G4 候選 |
| `W1-RCPT` | W1 PRIMARY 收據 | 1,191 | `bd3306be1fc608bd5e7459e25c62a09d7a5b1ce03ee7ec830a24a8dfb53758ea` | W1 本地主選與 not_claimed |

規則：同名不同 SHA 一律隔離；來源缺頁只影響引用它的條款；不作全冊默認失效。GitHub 的 Git blob SHA 不是 raw SHA-256；本冊不把兩者混用。

## 00.5 章契約與 DOC 邊界

本書 00–12 每章都有 Input／Operation／Output／Consumer／ACC／NEG／FirstFail。文件自檢只證明「可讀、可追溯、可施工、無假宣稱」，不證明產品行為。對未知的 Repo、Host、命令、Oracle、憑證或 Owner 簽名，正文一律保留 `待後續 probe/fill`，由實際有權者在 W0 控制包填實。

---

## 00.6 CODEX-first／Native-first 修訂（2026-11-25 Human Owner 裁決）

本節是 `W0-CODEX-FIRST-20261125-01` 的正式修訂摘要，優先於本檔其餘受影舊文；未受影的 14 WP、24 Case、七 Seam、NF-R/T 與安全責任全部保留。

| 受影條款 | 修訂 |
|---|---|
| §00.2.2 授權 | 由「一次可逆 DEV」改為同一有效授權內多個受界可逆 DEV/OPS 與自主接續；仍須逐工作項取得真 write-set/preimage/權限/recovery |
| §05.1 Host | 本地 CODEX 為主工程 Host；HERMES 移至後續 Compatibility，不阻斷 CODEX |
| §05.5 #5 Original OPS ECP | 採納本地 CODEX Native OPS ECP 等價承接；原域身份保留，Legacy Profile 另接 |
| §08.1 B0 前置 | 以 CODEX Native OPS ECP 取代舊 Original OPS ECP 強制前置 |
| §08.5 OPS 工作令 | O1–O6 可在真 principal/scope/preimage/recovery 成立時執行；不以 HERMES 不可服務為阻斷 |

**非聲稱**：本修訂不建立第二 Runtime/Queue/Dispatcher/Issuer/Registry/ACK；不偽造 OS/Repo/Host 權限；不把 CODEX 本地測試冒充 HERMES 或其他 Host 已通過。

# 01｜Goal／FUO／Non-goals

**章契約**｜Input：FHS-5 五方產品定位、原 W0 A/B/C、PLAN B0。Operation：把 Wave Goal 收斂成一個真 Generic 小型工程任務與可否定義。Output：WaveGoalCard、B0 FUO、W0 Done。Consumer：Program Owner、W0 Pack Author、五方 Owner。ACC：一個真任務可覆蓋五方代表能力且不前移 W1–W4。NEG：以 SST 案例、舊 G4 報告或作者文件冒充真跑。FirstFail：`FUO_OVERBROAD`、`SAMPLE_NOT_AUTHORIZED`、`PHASE_OVERREACH_CANDIDATE`。

## 01.1 Product SPEC：五方可獨立使用、按需協作

FHS-5 是五個可獨立使用、按需協作的工程輔助職能，不是第二套 Agent Runtime、政策引擎或治理服務。

| 方 | 真正產品責任 | 最小可見輸出 | 不能被刪掉的安全／效果 |
|---|---|---|---|
| TPM-SP＋Reviewer | 將真需求與來源編成 PI/PD/DEV ECP/OPS ECP/TQAEP；保留 QA26／F01–F14 的審查責任；反查 Parent/Child/NEG、缺 B、無源 Gate、不可施工前置 | 四契約＋具體 Finding／修訂；QA26 代表案例 | 需求追溯、Child 完整、來源 pin、可施工性診斷；W0 不全跑 QA26 但不得省略分母 |
| Commander Guide | ThinStart／ThinResume；`PACKAGE_FIRST` 優先，body 不足才 `CONTEXT_AUGMENTED`；Touch1/Touch2 雙觸點；保 Scope、Done、Stop/Resume；九鍵 Delta 與 WAIT/PARK 責任 | 可直接被 Native Executor 消費的薄提示、續行與九鍵 Delta advice | 不擴 Scope、不假 ACK、不以 `CLOSE` 代替 Publisher；缺雙期 Reader 記 `DELTA_UNVERIFIED` |
| Contract Bridge | `inspect_package`／`explain_slice`／`render_agent_context`／`compare_context`，安全唯讀 Context；保留原 38＋28 契約分母 | 四 API 結果與 path/identity 比較 | 根目錄 confinement、span/SHA、未知欄位保真；Bridge 只作按需 Context |
| External Challenge | 五 pin（source/candidate/evidence/oracle/case_set）、凍結候選與 oracle、獨立 POS/NEG、八欄 Finding；C16／EC-36／local47 分帳 | frozen identity、argv/exit/raw、reproduction、NotCovered | 不改受審 candidate/oracle；C16 與 local47 不互代；raw 可重現 |
| FAR | RQ0–RQ8、至少兩個實質 Alternative、10 類 Advice、FAR 七鍵、source status、T20／FARP30／local35 分帳；給最小 Next | RQ 結果、兩方案、風險、Advice、Stop/Resume | source unavailable ≠ zero；無證據不 CLOSE；Fabric 三源只在原 Profile |

目標專案使用 FHS-5 時只調用需要的工具；未安裝 Bridge/FAR 不得阻斷本來能合法完成的工程。FHS-5 自身開發時，五方是本產品要驗證的功能，不能以裸 Hermes 完成無關任務就宣稱五方通過。上述具名契約是產品分母，不是 Generic W0 的全域硬 Gate；W0 只作代表案例，完整分母依 §02.5 分帳至 W1/W2–W4。

## 01.2 W0-A／B／C 與 B0 的正確關係

| 名稱 | 性質 | 本波責任 | 不是什麼 |
|---|---|---|---|
| W0-A | 功能／效果分線 | 真來源讀取、PI/Review、ThinStart、Bridge Context、合法 READ/DRAFT | 不是只做文件排版 |
| W0-B | 功能／效果分線 | 在有真權限時完成一筆可逆 Native DEV/OPS effect、readback、restore | 不是 B0；沒有真權限就 `NOT_ADMITTED` |
| W0-C | 功能／效果分線 | FHS Legacy 的適用性、ID 守恆與 Profile 負例；Generic 不背 485 | 不是 Generic 完成前提 |
| `FHS-5/W0/B0-NF` | 執行 Batch | 用一個真 Generic 小任務串起五方代表能力、真 DEV/OPS、獨立反證、修補、交接與 OFF parity | 不是原 W0-B、不是 SST B0、不是「全五方所有 Profile 已驗」 |

一個 Batch 可以覆蓋多個分線的必要子集，但分線 claim 與 Batch claim 分開記錄。B0 成功後，若已涵蓋新版 W0 全部必需 FUO/Case，可直接結案 W0；若有真差額，只追加最少 `Bn`，不預設 B1、B2 數目。

## 01.3 B0 最小 FUO

> 在已授權的本地 Native 環境，不載入舊通用治理框架，對一個真正的小型 Generic 工程需求，實際使用 FHS-5 五方核心能力生成可施工包、完成一筆可逆 code 或 operation、獨立重現一正一負、研究一個真 Finding、修補並再驗、完成 consumer readback；關閉可選職能後，不受影工作仍能執行。

**B0 必要結果**：

1. 真需求／來源有 raw SHA、span、Owner、允許 root；不是示例字串。
2. TPM＋Reviewer 生成 PI/PD/DEV/OPS/TQAEP，並能具體指出「缺 B」或「無源 mandatory」。
3. Guide 的 ThinStart 被真 Native Executor 讀取；不是只貼 prompt。
4. Bridge 四 API 在 ON 時有真輸入／輸出；OFF 時 direct 路徑可用。Bridge 專屬安全案例另驗。
5. 一筆有權 DEV 與一筆本地 OPS/run+readback+restore；無權或未知操作不執行。
6. Challenge 在凍結 candidate/oracle 後得到真 POS/NEG raw；Challenger 不改受審物。
7. FAR 面對真 Finding 提出至少兩個實質根因／方案，記成本與未知；無證據不 CLOSE。
8. 至少一筆真 red→patch→retest（或誠實標示的 controlled mutation），只回歸受影 cone。
9. Legacy/optional OFF 冷啟有實際載入/呼叫觀察；不是只改環境變數。
10. 真 consumer 讀回 pack、candidate、raw、next；不以作者摘要或假 ACK 代替。

## 01.4 B0 樣本選擇

**第一順位：合法復用既有 G4 或等價候選。** 先查 W0 CLOSEOUT 所述 G4 的真來源、需求、程式、測試、Owner/權利、是否獨立於 SST、是否可安全改動。W0-CLOSE 只報告 G4「3 tests OK」與可跑候選；本輪沒有取得其本地實體，因此目前是 `REPORTED_RUNNABLE / OWNER_DESIGNATION_REQUIRED`，不是已選定。

**第二順位：若無可用既有案例，採用 PLAN §07 的新 Generic 微型任務 `briefcheck`。** 它是真需求、真 CLI、真測試與真可逆輸出，不是 Bridge 的替代品，也不是五方本身。

| 樣本需求 | 可測行為 | 必要負例 |
|---|---|---|
| SAMPLE-R1 | 讀授權 root 內 UTF-8 Markdown；input 為 root 內相對路徑；核 SHA | 絕對路徑、`..`、symlink/junction/reparse escape、非法編碼、hash mismatch 拒 |
| SAMPLE-R2 | 來源規定 A、B 兩個獨立必需項；精確 parse `- [x] A`／`- [x] B`；parent PASS iff 兩項都存在、勾選且唯一 | 缺 B、重複、模糊、格式錯誤 fail closed |
| SAMPLE-R3 | stdout 穩定 UTF-8 JSON：`source_sha256, provided, missing, status`；不回寫來源；0=完整，2=缺項，3=無效/越權 | 錯誤訊息不洩露 root 外路徑或敏感正文 |
| SAMPLE-R4 | 同 source 執行兩次結果相同；在授權 output root 作一次可逆寫入並 readback | 不得用 `git revert` 冒充 OPS/檔案回復；來源 bytes 不變 |

樣本選擇、Owner 採納、exact root、fixture/oracle bytes 及真授權，必須在 W0 控制包施工前落定。本冊不宣稱 G4 或 briefcheck 已被選定或執行。

## 01.5 W0 Done 與 Non-goals

**B0 Done（建議新標籤，非原枚舉）**：`B0_NF_VALIDATED` 只在 §12.1 全部必要條件有真 evidence 時成立；否則只能是 `B0_PARTIAL_VALIDATED`、`B0_BLOCKED_EXTERNAL` 或 `B0_ARCHITECTURE_REWORK_REQUIRED`。

**W0 Done**：`W0_NF_VALIDATED` 需 B0 成功，且採納版 W0 的全部必需 FUO/Case 已涵蓋；缺項追加最少 Bn 並整合 recheck。W0 Done 不等於 `MISSION_COMPLETE`、Original Acceptance 或 Release。

| # | 本波不做 |
|---|---|
| 1 | 不物化六檔 W0 控制包；只在 §11 定義其規格。 |
| 2 | 本輪（主用升格輪）不跑 B0/W0 產品程式、Hermes、Bridge、Challenge 或 FAR；B0 執行依 §00.2.2 授權，屬下一控制步驟。 |
| 3 | 不把 W1 三 Host、W2 全 effects、W3 深迭代、W4 發布當 W0 前置。 |
| 4 | 不要求 Generic 專案安裝 FHS 485、HGK、FABRIC、SBL 或 PIPD。 |
| 5 | 不以刪除真產品功能、降低安全或改 oracle 製造 Native-first 成功。 |
| 6 | 不簽 Owner、Issuer、OS Principal、Checker、Publisher 的收據。 |

---

# 02｜Affected PI／Requirement／Child／NEG

**章契約**｜Input：PLAN §06–07、原 14 WP/24 Case、MASTER 與五 PROJ 原意。Operation：建立 NF-R01..10 的需求樹、Child、NEG、Exception 與原 ID crosswalk。Output：AffectedPISlice。Consumer：TPM/Reviewer、PD Owner、Case Owner、Program。ACC：原安全意圖與 Child 完整、沒有無源 mandatory。NEG：缺 B 父項 PASS、把 FHS 485 套到 Generic、把新 NF 案覆寫原案 PASS。FirstFail：`REQUIRED_CHILD_MISSING`、`UNSOURCED_MANDATORY`、`PROFILE_GATE_DRIFT`。

## 02.1 需求建立方法

1. 先以 SourceLocator 固定來源、raw SHA、span 與版本；不從摘要或檔名推定。
2. 將「A、B 各有／分別／對應」拆成獨立 Child；`SPLIT_CANDIDATE` 未經真 Review 前不得標 `SPLIT_VERIFIED`。
3. 每個 Parent 只有在全部必要 Child 存在且被消費時才可 PASS；缺一 Child 即 `REQUIRED_CHILD_MISSING`。
4. 新 NF ID 是作者候選，不改寫原 ID；原 ID 保留於 crosswalk 與 Case/Oracle ledger。
5. 沒有來源、安全或當期技術必要性的 mandatory 一律 `UNSOURCED_MANDATORY`，不得因舊文件出現過就繼承。

## 02.2 NF-R01–NF-R10：需求、Child、驗收與負例

| ID／原追溯 | Parent → Child | 驗收 | NEG／Exception |
|---|---|---|---|
| `NF-R01` 真來源與計畫（W0-01/03、T01–T03、B01） | `R01.1` source freeze／SHA／span；`R01.2` Requirement/Child/NEG/Exception 拆分；`R01.3` PI/PD/ECP/TQAEP 語義完整 | 真 bytes、完整 Child、可施工四契約；Reviewer 能指出缺 B 或無源 Gate | 同名異 SHA、缺 B 父項 PASS、假 OriginalID；來源不可得則只停受影 PI，不編造 |
| `NF-R02` 薄提示與續行（W0-06/11、B02） | `R02.1` ThinStart 讀真包；`R02.2` Scope/Done/Stop 不擴張；`R02.3` 同源差額 ThinResume | Native 實際讀包 digest、action ref；scope 不變；同源 delta 可續 | 只貼 prompt、Guide 擴 Scope、拿舊包冒新包；無 FAR 時可直接修明確錯誤 |
| `NF-R03` 唯讀 Bridge（W0-07、B03） | `R03.1` inspect；`R03.2` explain slice；`R03.3` render context；`R03.4` compare；`R03.5` root confinement | 四 API 真輸入輸出；span/NEG/exception；on/off 比較；越界拒 | `../`、symlink/junction/reparse、UNC、絕對路徑；未知 schema 靜默丟義 |
| `NF-R04` 有界 Native 工程（W0-08/12、B00/B04） | `R04.1` 一筆授權 DEV；`R04.2` 一筆本地 OPS run/write；`R04.3` post-readback；`R04.4` restore | 真 diff、command、exit、raw、pre/post、recovery；effect 與 ECP 一致 | 假 permit、越 write-set、未知 effect、CLI 0 但 state 不符；無權即 `NOT_ADMITTED` |
| `NF-R05` 獨立反證（W0-09/13、B04） | `R05.1` frozen candidate/oracle/fixture；`R05.2` POS/NEG；`R05.3` challenger no-write；`R05.4` stale raw 重驗 | 真 argv/exit/raw；oracle 先凍結；maker/challenger 分責 | 改 oracle/candidate、只有文字總結、重用不同 candidate 的舊 raw |
| `NF-R06` FAR 研究（W0-10、B05） | `R06.1` 真 Finding；`R06.2` ≥2 根因或方案；`R06.3` 成本/未知/反證；`R06.4` 最小 Next | Finding 八欄可回取；兩方案有比較；無證據 `RESEARCH_REQUIRED` | source unavailable 填 zero、自報 `FIX_NOW/CLOSE`、超過 Owner scope |
| `NF-R07` 收斂（W0-11/14、B02/B05） | `R07.1` red；`R07.2` 受影 patch；`R07.3` affected retest；`R07.4` no-delta stop | 至少一次實質 red→patch→green；只回歸 ChangeCone；無新 delta 停 | 只改 status、換 task ID 無限重派、修改預期使紅變綠 |
| `NF-R08` Generic 去耦合（M§04/05/12、T24） | `R08.1` cold-off；`R08.2` optional-off parity；`R08.3` load/import/call trace；`R08.4` Legacy 分帳 | 無舊 provider 冷啟完成代表功能；Bridge/FAR OFF 不阻 direct；舊相容另驗 | 非必要框架仍 hard import、只改 env、以 keyword count 當去耦合 |
| `NF-R09` 交接（P00-05、W0-14、M§16） | `R09.1` pack/candidate/raw 指針；`R09.2` consumer readback；`R09.3` W1 技術/施工准入分層；`R09.4` MASTER 回寫 | 新 session 或具名 consumer 真讀；錯版/舊 SHA 拒；雙層准入分開 | 只有 manifest、假 ACK、把作者候選當原域接受 |
| `NF-R10` 安全與權限（T05/06/11/12/15/23） | `R10.1` real root/ACL；`R10.2` exact write-set/secret hygiene；`R10.3` unknown/recovery；`R10.4` 獨立驗收 | 越界/洩密/未知寫入拒；pre/post/restore 可證；checker 不改受審物 | 以作者檔案或 skill 可讀當 Grant；未知 effect 默認 READ；secret 進 fixture/報告 |

**Parent/Child 判定**：NF-R01 是來源與規劃的根；NF-R02–R07 是五方與收斂效果；NF-R08–R10 是架構、交接與安全橫切。橫切需求不能被當成「全部完成才可做任何事」的總 Gate；它們對每個受影 Slice 提供必要條件。

## 02.3 原 ID crosswalk

| 原集合 | 本冊位置 | 新狀態 | 不可誤讀 |
|---|---|---|---|
| `F5-W0-01..14` | §07 逐項契約 | 全保留；B0 重新分配 | 原 ID 存在不等於已執行 |
| `F5-W0-T01..24` | §09 逐案處置 | 全保留；KEEP/REPLACE/OPTIONAL/DEFER 分開 | 新 NF 案不覆寫原案 PASS |
| `SM01..SM07` | §06 | 七 Seam 全保留、具體化 IO | Seam 不是全域 ABI Gate |
| `U-011` | NF-R01、T03 | A/B 缺 B 父項不得 PASS | 不以父項總分抵銷 |
| `U-017` | §10、W1 三 Host | W0 只驗本輪 target Host；九格 deferred | 不宣三 Host PASS |
| `U-028` | §10、W1 能力 | W0 只驗所需 Native 任務能力；Kanban/Delegation/Swarm 三格 deferred | 不以文件清單冒充 |
| `U-046` | §00、§10 | Author/Effect/Independent/Release 分帳 | 作者 PASS ≠ Native PASS |
| 原 15 檔 | §11 crosswalk | 六檔新真源；舊 15 檔歷史/衍生 | 不雙寫 Current |
| 原 W0/W1 14 HOLD | §10.5 | 全部保留，逐一給新處置 | 不改名自動解除 |
| 原 W0M R3-CR／WM2E | §10.5A | 另列 1:1，不與 14 混為一 | 無 CLOSE、無 overclaim |
| 產品具名分母 | §02.5、§09.5 | QA26、CG-SEM17、38＋28、C16/36/47、RQ0–8、FARP30 等保留 | 不與 24/10 混算 |
| 22/36/50/39/96/192/485 等 | §02.4 | FHS Profile 原分母保全 | 不跨分母抵銷、不套 Generic |

## 02.4 FHS Legacy／Profile 適用性

| 對象 | 本波處置 | 理由 |
|---|---|---|
| Generic 非 FHS 任務 | 不要求 485、FHS 22/36/50/39/96/192、三 Host 或 Fabric | NF02/NF09；Generic 的完成分母只含本次採納 NF 需求 |
| FHS Profile 回歸 | 只在產品承諾或 Owner 採納時，按適用 ID/Slot 子集驗 | 1011 ledger、576 可辨識 ID＋435 未解析 slot、485/485 索引、0 install、全 UNVERIFIED 是既有事實 |
| Legacy proposal-1/2、C16/F5-T12、原 ACK/Reader | 保持原適用域與歷史；新版 IO 不冒舊 ABI | 未知欄位保真或明確 reject；不靜默丟義 |
| 未提供 ID 清單的舊分母 | `UNBOUND`／`DEFERRED`，記 Owner 與下一個取件動作 | 不宣全量覆蓋，不把未驗算 PASS |

**重要邊界**：`NF-R08` 的「Legacy OFF parity」不是「Legacy 功能已刪除或已通過」。若本次產品承諾某項相容性，必須另立適用案例、真 consumer 與分母；未承諾的部分如實標 NotCovered/Deferred。

## 02.5 產品具名契約與原分母 ledger

以下分母是 FHS-5 自身產品驗收帳，不是 Generic W0 的完成分母。W0 只做代表能力與可施工性；完整產品分母保留至 W1/W2–W4，不得用 24 Case／10 NF Case 的結果替代，也不得跨分母相加抵銷。

| 產品 | 具名契約／原分母 | W0 處置 | 後續／NotCovered |
|---|---|---|---|
| Reviewer | `QA26`／`F01–F14`；14 功能與反向 provenance | 以代表 POS/NEG 檢缺 B、無源 Gate、不可施工；不全跑 | W1/Reviewer 原分母；QA26 各案另立 |
| Guide | `U26`；`CG-SEM01–17`、`CG-X01–X13`、`CG-FAR-01–10`；local `20/50`；`PACKAGE_FIRST`、`CONTEXT_AUGMENTED`、Touch1/Touch2、九鍵 Delta、`WAIT/PARK` | ThinStart/Resume＋package-first 與不足時 context-augmented 代表；九鍵以可核資料呈現；不全跑 | W1/W3M；缺雙期 Reader 為 `DELTA_UNVERIFIED`，不作正式 PARK |
| Bridge | 四 API；原 `38＋28` 契約；Source/Scope/Clause/Case 保真 | 四 API on/off、path/identity compare；Bridge 安全代表案例 | W1 原 38＋28；未逐案跑者 NotCovered |
| External Challenge | `C16`／`EC-36`（EC-T01..26＋EC-X27..36）／local `47`；五 pin；八欄 Finding | frozen POS/NEG；C16 Legacy 另記；local47 與 C16 分帳 | C16／EC-36 原 Runner；W1/W4 |
| FAR | `FAR-FR01–17`；`RQ0–RQ8`；10 類 Advice；FAR 七鍵；`FAR-T20`／`FARP30`／local `35`；三源 typed status | 至少兩方案、RQ 代表、source status、Advice 與七鍵；Fabric 三源 DEFER | W1/W3；原 Router／WorkOrder／R8 只在真 Profile |
| FHS Legacy | `22 WP／36 Edge／50 H1／39 ModeGate／96 Oracle／192 Cell／485 ToolNeed`；`1011/576/435`；`35/56` | Generic 不背；FHS 只作適用子集與 ID 守恆 | W0-C/W4；未解析 slot 保持 UNBOUND |

**判讀規則**：

1. 具名契約出現不等於該產品已通過；W0 的代表案例不得填滿 QA26、CG-SEM17、38＋28、C16/36/47、RQ0–8 或 FARP30。
2. `PACKAGE_FIRST` 與 `CONTEXT_AUGMENTED` 是 Guide 的兩種資料取得模式；前者優先，只有 Package body 不足才要求 Bridge context。
3. Guide 九鍵與 FAR 七鍵不是同一 schema；`source_manifest_sha256` 與 `source_sha` 需原 Owner 明確指向同一 Source 集合，不得名字換等值。
4. FAR 的 `HIT / ZERO_RELEVANT_HIT / UNAVAILABLE / BLOCKED_BY_AUTHORITY / ERROR` 是五種不同事實；`UNAVAILABLE` 不填 0。
5. Challenge 五 pin 不互代；八欄 Finding 的 strict schema 不被 EvidenceGraph 的 expected/observed 欄污染。
6. 所有原分母保留原名與 Owner；W0 只新增 `NF-T` 與 B0 代表案，不能把原分母刪除、改名或加總。

---

# 03｜Existing Capability／Search-Before-Build

**章契約**｜Input：本地 repo/檔案、skills/plugins、CLI、Host、測試器、W0 PRIMARY、W1 reference、G4 等既有成果。Operation：逐能力探查、分級、指定 REUSE/BIND/ACTIVATE/REPAIR/BUILD_MINIMAL/AUTHORITY_REQUEST/CONTRACT_DECISION/OPTIONAL/DEFER。Output：ExistingCapabilityLedger＋下一動作。Consumer：W0 Pack Author、Executor、Host Owner、Reviewer。ACC：每項有實際位置或明確未知，不以未綁推缺碼。NEG：未探查即 BUILD、skill 可讀即 Host installed、舊報告當本輪重跑。FirstFail：`REUSE_NOT_CHECKED`、`CAPABILITY_UNVERIFIED`、`FALSE_CAPABILITY`。

## 03.1 Search-Before-Build 順序

1. 先查真 repo、檔案、branch、manifest、測試、LastGood 與 open PR；只查受影能力。
2. 再查已安裝 skills/plugins/CLI 的可執行入口與版本；「在技能清單可見」只算 `INDEX_VISIBLE`。
3. 再查 Host 的 loaded/invoked/consumed 或實際 session/task 行為；沒有三層證據不得說 serviced。
4. 只有以上都無法支援，且需求真必要，才 `BUILD_MINIMAL`；不建第二 Reader/Registry/Runner/ACK/Queue。
5. 每項只留一個主處置，附 Owner、下一個具體動作、ACC 與 Stop；`UNBOUND` 不是處置。

## 03.2 既有能力台帳

| 能力／位置 | 本輪實際可見 | 分級 | 下一動作 |
|---|---|---|---|
| `plp-tpm-review` 插件（本機技能索引） | 技能索引可見；未在本輪對產品來源執行 review；保留 QA26 分母 | `INDEX_VISIBLE / NOT_EXECUTED` | 在 W0 以真來源執行 Reviewer 代表案；QA26 不全跑；保留 exit/raw |
| `sbl-tpm-sp` 技能群 | 多份 TPM/Program 技能索引可見；未當成產品 runtime | `METHOD_REUSE_CANDIDATE` | 只在 W0 控制包需要時採其方法契約，不假設 Host 已安裝 |
| `FHS-5_TPM-SP` 本地資料夾 | 目錄存在；本輪未逐檔讀 manifest/code | `LOCAL_PATH_VISIBLE / UNVERIFIED` | W0 probe manifest、skills、install；不以資料夾存在當 Host served |
| `FHS-5_Commander Guide` 本地資料夾 | 目錄存在；Guide 契約已由 PROJ-02 交叉核對；未執行 | `LOCAL_PATH_VISIBLE / CONTRACT_READ / NOT_EXECUTED` | W0 驗 PACKAGE_FIRST／CONTEXT_AUGMENTED、Touch1/2、九鍵 |
| `FHS-5_Contract-Bridge` 本地資料夾 | 目錄存在；四 API 契約已知；未執行 | `LOCAL_PATH_VISIBLE / NOT_EXECUTED` | W0 四 API on/off；保留 38＋28 分母 |
| `FHS-5_External Challenge` 本地資料夾 | 目錄存在；skill `sbl-external-challenge-sp` 在可用技能索引 | `LOCAL_PATH_VISIBLE / SKILL_INDEX_VISIBLE / NOT_EXECUTED` | W0 frozen POS/NEG；C16/36/47 分帳 |
| `FHS-5_FAR` 本地資料夾 | 目錄存在；未確認 Fabric autonomous research 入口 | `LOCAL_PATH_VISIBLE / UNVERIFIED` | W0 先查 RQ0–8、10 Advice、七鍵；Fabric 三源不作 Generic 前置 |
| W0 PRIMARY 15 檔＋13 sources | 已讀 CLOSEOUT、TQAEP；未逐檔重跑全部 guard | `READ_PARTIAL / HISTORY_KEEP` | 保留 LastGood；由 W0 以真源重核，不重跑舊綠燈當新產品驗收 |
| W1 Bridge reference | PLAN/W1 報告候選路徑 `W1/impl/w1_bridge_reference.py`（四 API、selftest/inspect/explain）；本輪實際搜尋未在 `Downloads\FHS-5` 找到 `w1_bridge_reference.py`，故不作已存在宣稱 | `REPORTED_PATH / ACTUAL_LOCAL_UNVERIFIED` | 在真實 W1 repo 隔離 clone 定位；若不存在，記 `BIND_EXISTING` 缺件，不重造 Bridge 服務 |
| W1 checks／fixtures／oracles | 實際可見：`W1_PRIMARY_20261124_v1\check\replay_hashes.py`、`w1_guard.py`、`m22_guard_ref.py`、`run_cases.py`、`run_harness.py`；fixtures/oracles 由 W1 PRIMARY 索引列出 | `LOCAL_PATH_VISIBLE / REPLAY_CANDIDATE` | 只在隔離 copy 跑；`run_cases`/`run_harness` 會寫 output/mutants；raw/exit 另存；不把作者 reference 當 Native PASS |
| W1M／W2M／W3M／W4M | 四份正文實際存在並已 hash；本輪只讀受影契約段，不逐冊全文 | `HASHED / SELECTED_READ` | 產品分母與 13 前件引用；不重編後波 |
| G4 | W0 CLOSEOUT 報告 3 tests OK；本輪未取得實際本地路徑 | `REPORTED_RUNNABLE / OWNER_DESIGNATION_REQUIRED` | Owner 指定或提供真來源；核需求/權利/Oracle；否則走 briefcheck |
| NativePicker／G1–G3／SQS legacy | 只作歷史候選／Legacy 對照 | `OPTIONAL / LEGACY_ONLY` | 不當 Generic 主樣本；需要時另案 |
| Hermes Host | 本輪未 probe 版本、route、session | `HOST_UNVERIFIED` | W0 以 `Get-Command`、help、實際 session 探查；無三層證據則停對應 effect |
| Python／Git／測試器 | 文件工作有 Python/Git 可用；產品 repo 版本未確認 | `TOOL_PRESENT / PRODUCT_ENV_UNVERIFIED` | W0 記錄實際版本、cwd、argv、exit；缺工具不猜替代 |
| Bridge 四 API 正式產品 | 未確認正式插件與 Host 消費 | `UNVERIFIED` | 先 BIND/ACTIVATE；確證缺才 BUILD_MINIMAL；B0 產品測試不可省 |
| Guide／Challenge／FAR 正式產品 | 未確認正式入口與 Host 消費 | `UNVERIFIED` | 各自 probe；可重用技能/CLI，不造治理 service |
| Legacy FHS 485／1011 | 只在歷史 ledger/索引可見 | `LEGACY_UNVERIFIED` | 不進 Generic 分母；承諾相容時另立適用子集 |

## 03.3 處置語義

| 處置 | 使用時機 | 最小退出 |
|---|---|---|
| `REUSE` | 現有 code/CLI 已能用且 fit | 真 invoke＋consumer readback |
| `BIND_EXISTING` | code 存在但未接線 | 實際接線＋on/off 證據 |
| `ACTIVATE_HOST` | 已安裝但未啟用 | loaded/invoked/consumed 三層 |
| `REPAIR` | 已重現 bug | red→patch→affected retest |
| `BUILD_MINIMAL` | 真探查後確證缺 | 最小產品功能＋測試，不建服務 |
| `AUTHORITY_REQUEST` | 功能存在但缺權 | 精確操作/root/期限/具權者 |
| `CONTRACT_DECISION` | 原契約衝突或不明 | 受影 Owner 裁決，保留 LastGood |
| `OPTIONAL` | 當期無必要、可 bypass | 明示 off 與 NotCovered |
| `DEFER` | 後波或無資料 | Owner＋ResumePredicate |

**NEG**：把「技能索引可見」當 Host installed；把「W1 報告 9/13 pass」當 W0 本輪重跑；只因沒有 ACK 就重造 Reader/Runner；未探查即說 `CODE_MISSING`；把 G4 舊 3 tests 當 B0 五方實證。

---

# 04｜RepoContext／Binding／Write-set

**章契約**｜Input：真 product repo 或授權檔案根。Operation：以 Git/檔案原生能力探查 root、HEAD、branch、dirty、untracked、ACL、write-set、preimage。Output：RepoContext 與 `RepoBindingRequest`。Consumer：PD Owner、Maker、Checker、Repo Owner。ACC：每個值來自同一時間點真 probe；未知為 null/UNVERIFIED。NEG：caller 自填 HEAD、用 docs 根冒充 product repo、未授權先寫。FirstFail：`REPO_HEAD_MISMATCH`、`PD_UNBOUND`、`WRITE_SET_UNBOUND`。

## 04.1 本輪 RepoContext

本輪只取得 `C:\Users\user\Downloads\FHS-5` 的來源讀取權與指定交付目錄寫入權；它不是產品 Git repo，也不是 B0 施工 repo。因此：

| 欄位 | 本輪值 | 說明 |
|---|---|---|
| `repo_context` | `null` | 未對產品 repo 執行 probe |
| `repo_root/head/branch/dirty` | `null` | 不從來源路徑或檔名推定 |
| `read_scope` | 使用者提供之 FHS-5 來源＋交付目錄 | 只讀來源；交付目錄只寫本輪兩檔 |
| `write_scope` | 本輪兩份 MD | 不代表產品 repo 寫權 |
| `product_write_scope` | `[]` | 本輪不寫產品 Repo |
| `preimage/rollback` | `NOT_APPLICABLE_FOR_PRODUCT` | 文件交付另保留來源不覆蓋 |

**NEG**：把 `Downloads\FHS-5` 當 `$Repo`；把本輪 MD 寫入權當 B0 DEV grant；用 `HEAD` 字串冒充 live HEAD；以 Windows 路徑猜測 Linux Host。

## 04.2 W0 施工前的原生 probe

以下命令是 W0 Pack Author 的取證設計，不是本輪已對產品 repo 執行。`$Repo` 必須由 Owner 指定為實際存在的授權 checkout；若命令不存在或 exit 非 0，記真錯誤，不另造 Reader。

```powershell
 # 只讀；$Repo 由 Owner 指定，禁止使用未確認路徑
git -C $Repo rev-parse --show-toplevel
git -C $Repo rev-parse HEAD
git -C $Repo branch --show-current
git -C $Repo status --porcelain=v1 --untracked-files=all
git -C $Repo ls-tree -r --name-only HEAD
Get-Command python,git,hermes -ErrorAction SilentlyContinue
python --version
git --version
```

`RepoContext` 最小資料：

| 欄 | 語義 | 不合格處置 |
|---|---|---|
| `root` | absolute real path，經 `rev-parse --show-toplevel` | 不在授權範圍→`REPO_UNBOUND` |
| `head` | 40/64 字元 commit，非 caller 字串 | 不符→`REPO_HEAD_MISMATCH` |
| `branch`／`detached` | 實際 branch 或 detached 狀態 | 不明→不寫 |
| `dirty`／`untracked` | 完整 porcelain，保留他人修改 | 有未隔離變更→不得 reset/stash 清除 |
| `allowed_roots` | 來源根、產品根、輸出根分開 | 交叉授權→拒絕 |
| `write_set` | 逐檔 absolute path、new/modified/deleted、reason | 缺 preimage/邊界→`WRITE_SET_UNBOUND` |
| `preimage` | 既有檔 bytes/SHA；新增檔記 absent | 缺→不施工 |
| `rollback` | 反向 patch／刪本次新檔／受權 revert | 不可回復外部效果→不納 B0 |
| `acl/principal` | OS/Repo 實際權限與 identity | 只有文件核准→`NOT_ADMITTED` |

## 04.3 Write-set、preimage 與污染控制

1. `write_set` 必須逐路徑列出，不得只用 `**/*`、整個 repo 或未受限 glob。
2. 修改既有檔前保存 raw preimage；新增檔記 `absent`，rollback 僅刪本次受權新增檔。
3. 不動使用者既有 dirty/untracked；不 `git reset --hard`、不強制 checkout、不以 stash 清空。
4. 不在原 primary 上跑會寫 output 或生成 mutants 的舊 harness；一律隔離 copy/worktree。
5. 若 preimage、rollback 或 write-set 任一無法證明，停止受影 DEV；其他合法 READ 可繼續。
6. 產出的 evidence 根與 source 根分離；evidence 不進公開 repo，public export 需另行 redaction/掃描。

## 04.4 B0 repo 選擇標準

B0 repo 必須：獨立於 SST；有真需求與可讀測試；Owner 有合法修改權；可在隔離 worktree 操作；有可逆的單一輸出效果；不需要外部 Admin/金融/發布權限。若 G4 符合，優先復用；若不符合，才在 Owner 指定的新隔離 repo 建 briefcheck。**不得把「找不到原 repo」寫成 `PD_BOUND`。**

---

# 05｜Host／Effect／Permission

**章契約**｜Input：實際 Native Host、OS/Repo principal、授權操作、ECP 與 effect 類型。Operation：把 READ、DRAFT、DEV、OPS、USER、RELEASE 分帳並驗真權限。Output：HostEffectLedger／ECP request。Consumer：Executor、Host Owner、Issuer/具權者、Checker。ACC：每個 effect 有 principal、root、write-set、preimage、readback、recovery；無權不跑。NEG：作者檔案當 Grant、`permit=true`、未知 effect 默認 READ、DEV principal 跨 OPS。FirstFail：`FALSE_AUTHORITY`、`EFFECT_UNBOUND`、`PRINCIPAL_DOMAIN_MISMATCH`。

## 05.1 Native Host 與 FHS-5 邊界

本地 CODEX（Codex Native）等 Native Executor 擁有 Goal/Plan、任務調度、工具呼叫與恢復；HERMES 為後續 Compatibility 對象，不是 FHS-5 主工程的強制前置。FHS-5 不建立第二 Host、Queue、Issuer、Effect Registry 或全域 Gate。FHS-5 的 PI/PD/ECP/TQAEP 是給 Host 消費的設計；Host 的實際命令、exit、raw、readback 才是效果證據。

本輪以本地 CODEX 的實際 probe 為 B0 主工程 Host；HERMES 的 binary/install 限制只保留為歷史 Compatibility 觀測，不阻斷 CODEX 的合法 DEV/OPS。

## 05.2 Effect 分帳

| Effect | 真正權限來源 | 本輪狀態 | 必要證據 | 停止條件 |
|---|---|---|---|---|
| `SOURCE_READ` | 檔案/來源 Owner 的讀權與 ACL | 文件來源已讀；產品來源未綁 | source SHA、span、root、reader identity | path escape、SHA 不符、未授權 |
| `ISOLATED_DRAFT_WRITE` | 使用者/工作區寫權 | 本輪只寫交付目錄 | before/after SHA、隔離根 | 越界、覆寫來源、symlink/reparse |
| `DEV` | Repo Owner＋授權操作（真 grant/ECP） | `NOT_ADMITTED` | HEAD、write-set、preimage、diff、test、readback | 缺任一前件、diff 超出 write-set |
| `OPS` | Host Owner＋OS Principal＋授權操作 | `NOT_ADMITTED` | HostID、principal、pre/post、argv/exit、recovery | 錯 principal、無 recovery、UNKNOWN 盲重試 |
| `USER` | 原 consent/data scope | `NOT_CLAIMED` | consent、資料範圍、compensation | 無 consent、範圍不明 |
| `RELEASE` | 原 Publisher/發布 ACL | `NOT_CLAIMED` | Checker/Publisher、發布範圍、readback | 缺 Checker/Publisher |
| `HUMAN_OWNER_SELECTION` | Human Owner 本地選用 | 只涵蓋本輪作者交付 | selection receipt、not_claimed | 當成原 Issuer/OS/Checker |

**`permit=true` 或複製的 WorkOrder 不是 Grant。** 權限來源必須是可追溯的當期授權（具權者、principal、範圍、期限、操作類型）；若原政策要求 typed receipt，必須保留真 receipt。若沒有原 Issuer 服務，可由 OS/Git/Repo/Host 的實際權限與 Owner 授權承接，但不可自造一種新的「Issuer」服務。

## 05.3 Principal 與安全邊界

| Domain | 可觀測 identity | 不可互換 |
|---|---|---|
| Repo DEV | Git identity／repo ACL／worktree | 不可當 OS Admin 或 OPS principal |
| OPS Host | OS user/SID/UAC／HostID | 不可用 repo write 權代替 |
| Source READ | 檔案 ACL／read root | 不可因能讀 docs 就讀產品 secrets |
| Evidence | 隔離 evidence root／write ACL | 不可寫進 public repo 或來源根 |
| Checker | 獨立 session/worktree/具權 checker | Maker 不可自簽 Independent |

Secret hygiene：fixture 不含真 token/secret；報告只記 sentinel 與 redaction 證據。若真 secret 被讀到，先停、縮受影範圍、記 incident owner；不得寫入 raw、對話或公開 artifact。

## 05.4 Provider OFF 與 optional bypass

1. OFF 必須在隔離 profile 真的不載入舊 provider；記 load/import/call trace 或等價可觀察證據。
2. 只改環境變數、改 label 或從未啟動舊 provider，不足以證明「舊依賴已移除」。
3. Bridge OFF 時，Guide／Native Executor 必須能直接讀完整 pack；FAR OFF 時，明確根因的 bug 必須能直接 patch/retest。
4. OFF parity 只對不受影工作；若舊 provider 是某項產品功能的真必要條件，記 NotCovered/Contract Decision，不假裝 parity。
5. B0 的五方產品驗證不能被「OFF 後 direct 可用」抵銷；兩者是不同 claim。

## 05.5 原 13 前件的分流

以下以 W2M §03.1 的 **原 13 前件名稱與順序** 為主鍵，逐項保存 1:1 身份；不以合併列替代。當前無真值者一律 `UNBOUND`，不是 `NOT_APPLICABLE`，也不因本冊作者設計而變 `READY`。

| 原# | 原名 | 新版 disposition | state | Owner | next／resume | 不可誤讀 |
|---:|---|---|---|---|---|---|
| 1 | Original OperationType | `BIND_EXISTING`／`CONTRACT_DECISION` | `UNBOUND` | Effect Owner | 同 Scope typed token；否則只做 READ/DRAFT | 未知 alias 不默認 READ |
| 2 | RepoContext | `DIRECT_PROBE` | `UNBOUND` | Repo Owner | live root/HEAD/branch/dirty probe | 不再要求專屬 Repo Reader |
| 3 | HostID／OS Principal／PolicyEpoch | `HOST_PROBE` | `UNBOUND` | Host／OS Owner | 同 Host/Epoch identity 與 readback | 只驗本輪 target Host，不要求三 Host |
| 4 | Original DEV ECP | `PD_NEW_ECP`＋原 canonical 另接 | `UNBOUND` | Repo＋Owner/Issuer | 新版 DEV ECP；若原仍適用，附原 typed ref | 新版設計不冒充原 Grant |
| 5 | **Original OPS ECP** | `ADOPTED_LOCAL_CODEX_NATIVE_OPS_ECP`／原域歷史保留 | `ADOPTED_LOCAL`（決策 `W0-OPS-NATIVE-20261125-01`） | Human Owner＋CODEX Host | 本地 CODEX Native OPS ECP 承接 O1–O6；原域 typed ref 只在 Legacy Profile 需要時另接 | **不得用舊框架缺失阻斷 Generic CODEX OPS**；不得偽造原域 receipt |
| 6 | Issuer | `AUTHORITY_DECISION` | `UNBOUND` | Human Owner 的授權責任／原 Issuer | issuer id＋policy ref；無服務時用真權限決策 | issuer 是責任，不是必建服務 |
| 7 | WorkOrder | `AUTHORITY_REQUEST` | `UNBOUND` | Owner／原 Issuer | WorkOrder bytes＋SHA；無即不施工 | 複製字串不是 Grant |
| 8 | ExecutionAdmission | `AUTHORITY_REQUEST` | `UNBOUND` | Owner／原 Issuer | 同 Subject/Scope receipt；否則 `NOT_ADMITTED` | `permit=true` 無效 |
| 9 | Exact WriteSet／preimage | `EXACT_WRITESET` | `UNBOUND` | Repo／Host Owner | 逐檔 path set＋preimage；新增記 absent | 全 repo glob 無效 |
| 10 | WorldReader／RepoReader | `DIRECT_READBACK` | `UNBOUND` | Reader Owner／原 Host | 同 Host/Epoch、檔案/process/consumer readback | 不建 WorldReader service；CLI 0 不等 state 正確 |
| 11 | Protected Checker | `INDEPENDENT_VERIFIER` | `UNBOUND` | Checker Owner | 同 Candidate/Scope distinct verdict | Maker 不自簽；Checker／Consumer 不合併 |
| 12 | Publisher | `DEFER` | `UNBOUND` | Publisher | 原 release procedure；不在 B0 | Guide CLOSE 不等於 Release |
| 13 | Recovery ABI | `DIRECT_RECOVERY` | `UNBOUND` | Repo／Host Owner | DEV 反向 patch；OPS Host 專屬補償 | 不以 `git revert` 冒充 OPS recovery |

**新增 NF 前件（不屬於原 13，另列）**：

| NF 前件 | disposition | state | Owner | next／resume |
|---|---|---|---|---|
| Original TQAEP／Case | `NEW_NF_ORACLE`＋原案另帳 | `UNBOUND`／`PLANNED` | Case／Checker Owner | 原 24 案保留映射；新 NF fixture/oracle 先凍結 |
| Original Receiver ABI | `NF_LOCAL_IO`／必要時 `CONTRACT_DECISION` | `UNBOUND` | Host／Consumer Owner | 新 NF IO；舊 ABI 只做版本隔離映射 |
| Host preimage | `PRE_STATE_PROBE` | `UNBOUND` | Repo／Host Owner | 操作前保存 file/process/world preimage |

**階段閘（CODEX-first 修訂）**：第 5 項已由 `W0-OPS-NATIVE-20261125-01` 採納本地 CODEX Native OPS ECP 等價承接；O1–O6 可在本地實際 principal、write-set、preimage、output root、recovery 成立時執行。原域 Original OPS ECP 的歷史身份與 Legacy Profile 適用性保留；不得用本機 CLI 可執行或 `permit=true` 冒充原域 receipt。13 項與新增 NF 前件的原域 HOLD 未被本表關閉。

---

# 06｜Architecture／Seven Seams／ADR

**章契約**｜Input：五方責任、Host 能力、七 Seam 原意、Legacy 契約。Operation：定義 producer/consumer、最小 IO、identity/version、negative、bypass 與兼容策略。Output：WaveArchitectureDecision。Consumer：Pack Author、實作者、consumer、Checker。ACC：七 Seam 各有真消費；無第二 Runtime；未知欄位不靜默丟。NEG：Seam 變全域 ABI Gate、`@proposal-2` 名稱相同即兼容、Bridge/FAR 被強制。FirstFail：`ABI_LOSSY_CROSSWALK`、`SCHEMA_UNSUPPORTED`、`CONSUMER_UNVERIFIED`。

## 06.1 Architecture SPEC

架構只有四層責任：

1. **Native Executor**：目標、計畫、任務、工具、恢復。
2. **FHS-5 五方工具**：按需產生或消費 PI/PD、ThinStart/Resume、Context、Challenge、FAR advice。
3. **工程實體**：Git/檔案、OS、Python/既有測試器、Repo/Host 權限。
4. **證據與 consumer**：raw、SHA、readback、下游實際讀取。

沒有第五層「FHS 治理 Runtime」。Scope、Schema、Runner 等一般工程概念保留，但不自動長成專屬服務。

## 06.2 七 Seam 的最小契約

| Seam | Producer → Consumer | 必要輸入 | 最小輸出 | Identity／版本 | NEG／Bypass |
|---|---|---|---|---|---|
| `SM01` Source→PI | 實際檔案/Git → TPM/Reviewer | project、work_id、source ref、raw SHA、span | Requirement/Child/NEG/Exception inventory | source id＋raw SHA＋版本；不得用同名 | 同名異 SHA、假 ID 拒；無來源則不編 |
| `SM02` PI→PD | TPM/Reviewer → Wave/PD Owner | req IDs、acceptance、constraints、actual capability | work items、effect boundary、typed edges | PI/PD revision＋source digest | 無源 mandatory、缺 B 拒；文件順序不當 runtime |
| `SM03` PD→ECP/TQAEP | PD → DEV/OPS/TQAEP | op、root、writes、preimage、command、oracle/fixture | ECP 與 planned cases／expected raw | PD/ECP/TQAEP id＋candidate/source SHA | 權限另證；後驗 raw 不得前置 |
| `SM04` Pack→Guide | W0 control pack → Guide | pack path/digest、goal/FUO/Done、limits、next | ThinStart／ThinResume | pack digest＋wave/batch id | 不發 Grant、不擴 scope；無 Guide 可直讀 |
| `SM05` Guide/Bridge→Executor | Guide/唯讀 Bridge → Native Executor | package ref；必要時 source ref/span/context/digest/missing | 可執行 context／直接包引用 | context id＋source/pack digest | Bridge OFF 時 direct；四 API 安全另驗 |
| `SM06` Executor→Challenge→FAR | Executor → Challenger → FAR | frozen candidate、source/evidence/oracle/case pins、argv/exit/raw | POS/NEG、Finding、NotCovered | candidate/oracle/fixture SHA 必須同位 | Challenger 不改受審；FAR 無證據不 close |
| `SM07` FAR/delta→Guide/Consumer | FAR 或 actual delta → Guide/consumer | finding、hypothesis、alternative、next/owner/stop | ThinResume、handoff、readback | evidence id＋candidate revision | 無 FAR 可直接修明確錯；假 ACK 拒 |

## 06.3 七 Seam 的實作規則

1. **Markdown 是主要可讀契約**；只有真機器 consumer 需要的欄位放 JSON。JSON 不得成為第二份手寫 canonical。
2. 新增 Native-first IO 使用明確 `NF` 命名；不冒用 `@proposal-2` 或舊 ABI。
3. 舊 consumer 需要兼容時，逐欄映射、保留 unknown 或明確 reject，輸出 loss report；不得靜默丟必需欄。
4. Finding 保留原 B04 八欄 `id,severity,class,subject_sha,command,exit,raw_sha256,reproduction` 的可重用語義；expected/observed/oracle/source/case/next 放同一 evidence record，不污染 strict schema。
5. 五 pin 是五個真 bytes identity（candidate/source/evidence/oracle/case），不是五個服務。
6. Seam 的 consumer 必須有真消費證據；只寫「已交付」而無讀取，不算接通。
7. 同一資料可在多個 case 重用，但 numerator 不可重複計；每個 consumer 只記一次有效消費。

## 06.4 Generic／Legacy 隔離

| 層 | Generic Native-first | Legacy Compatibility |
|---|---|---|
| 入口 | 直接檔案/Git、Guide、可選 Bridge | 原 Reader/loader/parser，明示 opt-in |
| Schema | NF 版本化 IO；未知欄位保真 | 原 proposal/C16/舊 ABI，保持原域 |
| Test | 實際 pytest/unittest/CLI、獨立 oracle | 原 case/fixture/receipt，另立分母 |
| Failure | 缺 capability 按 §03 處置 | 缺原 receipt 記 Legacy 未驗，不倒卡 Generic |
| Claim | Generic 完成只覆蓋採納 NF 範圍 | 不冒充原域接受或 485 全綠 |

**Bridge/FAR direct bypass**：Bridge 是唯讀 Context 工具，不是所有工作的必經閘；FAR 是研究工具，不是每個明確 bug 的必經流程。Bridge/FAR OFF 時，合法 direct 工作可繼續。然而 B0 作為 FHS-5 自身產品測試，必須另有 Bridge ON 四 API 與 FAR ON 真 Finding 案例，不能只用 bypass 完成 B0 五方 claim。

## 06.5 Architecture NEG

- 把七 Seam 當成一個必須全通過的 ABI Gate；
- 以相同 namespace 名稱推定語義兼容；
- 把未知欄位丟掉後宣 lossless；
- 在 Host 外另建 Queue/Dispatcher/Issuer；
- 以文件中的 `INFO_ONLY` 標籤掩蓋實際被硬化的順序；
- 以 Bridge/FAR 不存在為由刪除 READ/DEV 的合法 direct 能力。

---

# 07｜Program SPEC／14 WP／DAG

**章契約**｜Input：NF-R01..10、實際能力、七 Seam、B0 樣本、Owner/consumer。Operation：把原 14 WP 編成可施工契約、B0 分配、typed edges 與平行策略。Output：WaveDependencyGraph＋WorkPackage contracts。Consumer：W0 Pack Author、Executor、Program Owner、Checker。ACC：每 WP 有輸入、操作、輸出、Owner、退出/負例；HardEdge 有 producer、無環。NEG：只列 WP 名稱、把後驗當前置、optional 硬化。FirstFail：`GATE_CYCLE_CANDIDATE`、`UNVERIFIED_EDGE_AS_HARD`、`PHASE_OVERREACH_CANDIDATE`。

## 07.1 Edge 語義

| 類型 | 意義 | 可否阻擋無關工作 | 必要欄 |
|---|---|---|---|
| `HARD_PRE` | 當期真必要來源、安全、技術或授權前件 | 只阻受影 WP | source/ref、producer、readiness、gap owner |
| `OPTIONAL_INFO` | 有助但不必要；缺時可 direct | 否 | optional reason、fallback |
| `POST_EVIDENCE` | 同一操作之後才產生的證據 | 不可作前置 | producing operation、evidence id |
| `DEFERRED` | 後波或未採納 | 否 | 觸發條件、owner |
| `UNVERIFIED` | 只知可能存在，未證實 | 不可升 hard | probe next、stop |

**硬規則**：`POST_EVIDENCE` 不得反向成為同操作 `HARD_PRE`；W4 Release 不得成為 W0 READ 前置；文件的章節順序不是 runtime Gate。

## 07.2 十四 WP 的完整契約

| WP | 必要輸入 → 操作 → 輸出 | Owner／Consumer | 退出、NEG／FirstFail |
|---|---|---|---|
| `F5-W0-01` SourceFreeze | 真來源、版本、span、ACL、selected sample → 讀 bytes、算 SHA、解衝突、凍結 → SourceInventory | Source Curator → Reviewer/Pack/Checker | 真來源可回取；同名異 SHA 隔離；`SOURCE_INTEGRITY_FAILED` |
| `F5-W0-02` PluginIdentity | 本地 repo、skills、manifest、Host probe → 判 alias/installed/bound/invoked/consumed → CapabilityLedger | Host/Plugin Owner → Program | 每項有 disposition；skill 可讀≠installed；`HOST_CAPABILITY_UNBOUND` |
| `F5-W0-03` PI/Reviewer | Goal、來源、Child/NEG/Case → 建 PI、反向 review、找缺 B/無源 Gate → PIReview/Finding | TPM/Reviewer → PD Owner | Parent 缺 Child 拒；無源 mandatory 拒；`REQUIRED_CHILD_MISSING` |
| `F5-W0-04` W0M-PD | PI、actual capability、Host/Repo 可見度 → 編 13 章、B0 slice、effect、edges → PD/W0M design | Wave Owner → Pack Author | 不填假 HEAD/權限；未探查標 UNVERIFIED；`PD_UNBOUND` |
| `F5-W0-05` W0-Control | W0M、六檔規格、真環境/授權 → 物化六檔、檢查可讀/可測 → W0 pack | Pack Author → Guide/Executor/Checker | 空殼、缺檔、Scope mismatch 拒；`PACKAGE_INTEGRITY_HOLD` |
| `F5-W0-06` GuideThinStart | 真 pack digest、Goal/FUO/Done/effect/stop → 生成 ThinStart 並交 Native 消費 → start record | Guide → Executor | 不擴 scope、不假 consumed；`GUIDE_SCOPE_DRIFT` |
| `F5-W0-07` BridgeRead | 授權 root、pack/source、view → 四 API、span/SHA、compare、安全路徑 → Context/比較結果 | Bridge → Guide/Executor/consumer | 越界拒、未知欄位保真；`BRIDGE_BOUNDARY_FAIL` |
| `F5-W0-08` NativeRead | pack/direct 或 Bridge context、真 Host → 真讀/執行、收 argv/exit/raw → Native evidence | Executor → Challenge/Checker | 手寫摘要不算；無真 Host 則 `NOT_RUN` |
| `F5-W0-09` FrozenChallenge | candidate、oracle、fixture、case set → 凍結、獨立 POS/NEG、Finding → challenge raw | Challenger → FAR/Checker | 不改受審物；無 raw 不稱 proven；`UNREPRODUCED` |
| `F5-W0-10` ResearchCandidate | 真 Finding、repo/raw、來源狀態 → 根因、≥2 方案、成本/未知 → FAR advice | FAR → Guide/Program | UNAVAILABLE≠ZERO；無證據不 CLOSE；`RESEARCH_REQUIRED` |
| `F5-W0-11` GuideResume | Finding/delta、可選 FAR、LastGood → ThinResume/next/stop → resume record | Guide → Executor/Checker | 無 delta 不重派；不發 Grant；`NO_DELTA_REWRITE_DENIED` |
| `F5-W0-12` NativeProtected | 採納 ECP、真 DEV/OPS 權限、preimage → 一筆可逆 effect、readback、restore → actual effect | Maker/Executor → Challenger/Checker | 無權 `NOT_ADMITTED`；越 write-set 停；`EFFECT_NOT_VERIFIED` |
| `F5-W0-13` Assurance | frozen final candidate、真 raw、consumer → 獨立 verdict、NotCovered → assurance record | Checker/Consumer → Program | Maker 不自簽；Publisher 非當期前置；`FALSE_INDEPENDENT` |
| `F5-W0-14` Delta/Handoff | A/B/C actual、nonclaims、HOLD → CLOSEOUT/HANDOFF/ChangeSet → next pack | Program/Wave Owner → W1/上游 | 不把 expected 當 actual；無真 delta 不重寫全波；`AS_BUILT_OVERCLAIM` |

## 07.3 B0 的 WP 分配與順序

```text
01 SourceFreeze ─┬─> 03 PI/Reviewer ─> 04 W0M/PD ─> 05 W0 Pack
02 Capability ───┘                         │
                                           ├─> 06 GuideStart ─> 08 NativeRead
                                           ├─> 07 Bridge（可選、獨立測）
                                           └─> 12 NativeProtected（真權限時）
06/08/12 ─> 09 FrozenChallenge
09（根因不明）─> 10 FAR ─> 11 GuideResume ─> 12' patch
09（根因明確）─────────────────────────────> 12' patch
09/12'/13 final pass＋OFF ─> 14 Delta/Handoff
```

- `02` 可與 `01/03` 並行，但只對被選 Host 的必要能力構成 `HARD_PRE`；不要求三 Host。
- `05` 是 W0 施工包，卻不是本輪 W0M 作者的產物；本輪只提供其規格。
- `07` 是 Bridge 專屬產品測試，不阻 `08` 的合法 direct；B0 需另在 ON 時驗四 API。
- `12` 的 effect 必須在 `04` 的 PD 與 `05` 的 ECP 之後；不可先寫再補授權。
- `14` 只消費 `09/12/13` 的真實結果；不是 `09` 的前置。
- `12` 是第一次受權 effect；`12'` 是 challenge/FAR 後的新 candidate/revision patch，必須有新的 ECP/admission、preimage 與 readback。`12` 的 post-readback 不得作 `12'` 的前置，`12'` 也不得被 cycle 檢測器當成同一個 `12` 節點。

## 07.4 平行、續行與追加切片

| 可平行 | 條件 | 合併規則 |
|---|---|---|
| Source/legacy 盤點、capability probe | 只讀，互不寫同一檔 | 單一 Source Curator 合併 |
| PI review 與 Host/repo probe | 不共享 write-set | 由 PD Owner 合併 |
| Bridge 專屬測試與 Native direct | 不同 root/session | 分帳 claim，不互相替代 |
| 多個非重疊 case/fixture 執行 | 各自 evidence root | 單一 Checker 彙整，不重複計 numerator |
| W1 legacy 合法 read | 不冒充 W0 | 只作 info/LastGood，不作 W0 硬前置 |

**B0 不足時的 Bn**：只有當採納版 W0 有未覆蓋的必需 FUO/Case，才依 ChangeCone 建最少 Bn。Bn 必須有真差額、受影 Requirement/Case、owner、預算/停止條件與不重跑範圍；不因「看起來完整」而加波。

## 07.5 DAG 反例

- `W4 Release → W0 READ`：`PHASE_OVERREACH_CANDIDATE`。
- `post-readback → same effect admission`：`GATE_CYCLE_CANDIDATE`。
- `05 pack → 04 PD`：文件編排倒置，非 runtime 前置；不得形成 cycle。
- `07 Bridge → 08 direct read` 被畫成 hard：optional 硬化；direct 應可走。
- 無 producer 的「等原 Reader」：`UNVERIFIED_EDGE_AS_HARD`，需改為 direct/ AUTHORITY_REQUEST/ CONTRACT_DECISION。

---

# 08｜DEV／OPS Strategy／可派工 Runbook

**章契約**｜Input：採納版 PD、真 Repo/Host、exact write-set、preimage、授權、sample/oracle。Operation：寫出可施工 DEV/OPS 工作令、命令邊界、readback、restore 與 Provider OFF。Output：B0 Runbook／ECP 設計。Consumer：Maker、Executor、Host Owner、Checker。ACC：每個命令真可執行或明示待 probe；pre/post 可證；無權不跑。NEG：placeholder 直送執行器、假 exit、以 git revert 當 OPS 回復、只改 env 當 OFF。FirstFail：`ECP_NOT_GRANT`、`RECOVERY_KIND_MISMATCH`、`EFFECT_NOT_VERIFIED`。

## 08.1 B0 啟動前置

| 前置 | 真值要求 | 未滿足時 |
|---|---|---|
| Product repo | Owner 指定、實際存在、可隔離 worktree | 只做 read/probe；不寫 |
| Sample | G4 真需求/程式/測試或新 briefcheck 採納 | 只保留 sample decision，不施工 |
| 權限 | Repo 寫權／Host run 權／輸出 root 的實際 principal | `AUTHORITY_REQUEST`，停受影 effect |
| CODEX Native OPS ECP | 本地 `02_W0_OPS_ECP.md` 的宿主/principal/scope/preimage/readback/recovery；決策 `W0-OPS-NATIVE-20261125-01` | 未成立→`AUTHORITY_REQUEST`；只停受影 effect |
| Source/oracle | 真 bytes、SHA、expected、fixture 位置 | 不跑受影 case |
| Host | 本地 CODEX 版本、OS principal、sandbox、工具；HERMES 另作 Compatibility | 不宣 Native consumed；CODEX 主工程可續 |
| Checker | 與 Maker 分離的 session/worktree/具權者 | 只能 partial，不宣 Independent |
| 回滾 | 修改檔 preimage；新檔刪除；OPS 專屬 recovery | 不納 B0 |

## 08.2 B0 DEV 工作令

| Work item | 輸入／操作 | 實際產物／ACC | Stop／恢復 |
|---|---|---|---|
| `B0-D1` Freeze baseline | 真 `$Repo`；跑 §04 probe；列出 exact write-set、每檔 preimage（新增記 absent）、test plan、output/evidence root | baseline ref、dirty snapshot、allowed roots、write-set、preimage SHA | scope/HEAD 變→reconcile；不寫來源 |
| `B0-D2` 四契約＋Review | 查真 TPM/Reviewer；生成 PI/PD/DEV/OPS/TQAEP；做缺 B／無源 hard gate 負例；輸出 Finding 與修訂 | 四契約＋具體 Finding／diff；parent/child 可追 | 無真能力→`BUILD_MINIMAL`；規格不清→Owner decision |
| `B0-D3` Guide/Bridge | Guide 讀真 pack；Bridge 四 API 最小受影適配；legacy parser 保持獨立 | 真 invocation、context、path/identity compare；on/off 各一 | 無 Bridge→direct 主線可走；B0 四 API 留 NotCovered，不假 PASS |
| `B0-D4` 最小 DEV | 依採納 sample 實作一個可逆 code change；只動 write-set | 真 Git diff、test command、pre/post、source unchanged | 未授權不施工；diff 超出→停止並還原受影變更 |
| `B0-D5` Challenge/FAR | 凍結 candidate/oracle/fixture；獨立 POS/NEG；真 Finding；FAR 至少兩方案；Guide 續行 | 真 red 原因／raw、兩方案、patch intent、retest 計畫 | checker 不改 candidate；無真 red 不稱完成 |
| `B0-D6` 修補與再驗 | Maker 按 finding patch；重新凍結；回放受影 POS/NEG、安全、OFF、consumer | final commit/diff/raw；green 與 NotCovered 分帳 | 失敗按 §10；不改 oracle 還就 |
| `B0-D7` 交接 | 新 session/具名 consumer 真讀 pack、candidate、raw、next | consumer readback、CLOSEOUT/HANDOFF/ChangeSet | 介面不能讀→先修，不假 ACK |

**D2/D3 可在不同 write-set 並行**；D4 必須在 PD/ECP 批准後；D5/D6 是有界迭代，不是無限重派。

## 08.3 briefcheck 的候選契約（採納後才生效）

若 Owner 不採 G4，則新隔離樣本至少包含：

```text
samples/briefcheck/requirements.md
samples/briefcheck/briefcheck.py
samples/briefcheck/tests/test_briefcheck.py
samples/briefcheck/fixtures/case_ok.md
samples/briefcheck/fixtures/case_missing.md
samples/briefcheck/fixtures/case_dup.md
samples/briefcheck/fixtures/case_bad_path.md
samples/briefcheck/fixtures/case_bad_utf8.md
samples/briefcheck/fixtures/case_hash_mismatch.md（可由 `case_ok.md`＋錯 SHA 產生，不另造來源）
samples/briefcheck/fixtures/case_ambiguous.md
samples/briefcheck/fixtures/case_malformed.md
```

候選 CLI：

```text
python -m briefcheck --root <approved_read_root> --input <root-relative-path> --sha256 <expected-source-sha>
```

輸出契約：

```json
{
  "source_sha256": "<64 hex>",
  "provided": ["A", "B"],
  "missing": [],
  "status": "COMPLETE"
}
```

exit：`0=完整`、`2=缺項`、`3=無效/越權/編碼/SHA 不符`。stdout 是穩定 UTF-8 JSON；錯誤不輸出 root 外路徑、原文全文或 secrets。執行兩次同 source 必須同值；不得回寫 source。`python -m unittest discover -s tests -v` 只在實際 tests 目錄存在且屬本次 sample 時使用。

**這些是新樣本待建目標，不是 repo 既有命令。** Pack Author 必須在 D1 把實際 entrypoint、cwd、argv、fixture SHA、oracle 換成真值；不得把 placeholder 送進執行器或預填結果。

**必要 fixture／argv／expected exit／oracle mapping**：

| SAMPLE 子項 | fixture／輸入 | argv 要點 | expected exit | expected status | oracle／不可接受 |
|---|---|---|---:|---|---|
| R1 absolute／`..`／symlink／junction／reparse | `case_bad_path.md` | `--input case_bad_path.md` | 3 | `INVALID_PATH` | 不得讀 root 外；輸出不得含 root 外路徑 |
| R1 invalid UTF-8 | `case_bad_utf8.md` | `--input case_bad_utf8.md` | 3 | `INVALID_ENCODING` | 不得回顯原文；source bytes 不改 |
| R1 hash mismatch | `case_hash_mismatch.md`／`case_ok.md`＋錯 `--sha256` | 同 `case_ok.md` | 3 | `SHA_MISMATCH` | 不得先當 COMPLETE 再降級 |
| R2 missing B | `case_missing.md` | 同 | 2 | `MISSING` | `missing=["B"]`；父項不 PASS |
| R2 duplicate | `case_dup.md` | 同 | 3 | `INVALID_DUP` | 不因其中一個有效就 PASS |
| R2 ambiguous／malformed | `case_ambiguous.md`／`case_malformed.md` | 同 | 3 | `INVALID_FORMAT` | fail closed；不得猜測 A/B |
| R3 stable JSON | `case_ok.md` 連跑兩次 | 同 | 0 | `COMPLETE` | `provided=["A","B"]`；stdout byte/語義同值 |
| R4 reversible output | `case_ok.md`＋受權 wrapper | 同，output root 另指 | 0 | `COMPLETE` | source SHA 不變；output 可刪回 absent |

每個 SAMPLE 子項必須有 fixture／argv／expected exit／oracle；未建或未跑者標 `PLANNED`／`NOT_RUN`，不得只用 `case_ok`＋`case_missing` 代替全部負例。

## 08.4 DEV 安全與回復

| 控制 | 要求 |
|---|---|
| Write-set | 逐檔 absolute；只允許本次新檔／受控修改；不得 glob 全 repo |
| Preimage | 既有檔 raw bytes/SHA；新增檔 absent；變更前保存 |
| Patch 邊界 | diff 只能落在 write-set；超界即停止並還原 |
| 測試 | 先跑 baseline，再跑受影 unit/contract/security；記錄 command/exit/raw |
| Readback | 讀回 postimage、diff、test raw；不以 exit 0 代替語義 |
| Rollback | 修改檔用 preimage/反向 patch；新增檔只刪本次檔；不得清除他人變更 |
| External effect | 若無法完全回復，排除在 B0；不以 `git revert` 冒充 Host recovery |

## 08.5 B0 OPS 工作令

**准入提示（CODEX-first 修訂）**：§05.5 第 5 項已由 `W0-OPS-NATIVE-20261125-01` 採納本地 CODEX Native OPS ECP。O1–O6 在本地實際 principal、write-set、preimage、output root 與 recovery 成立時可執行；HERMES 不可服務不阻斷 CODEX OPS。原域 Legacy Profile 才需原 Original OPS ECP。

| 步驟 | 真操作 | 必要證據 | 失敗／恢復 |
|---|---|---|---|
| `O1` Native 冷啟 | 使用確認可用的 local Native route；載入真 ThinStart；建立 session/task | session ref、pack digest、tool invocation、read/consumed 觀察 | 無 route→`HOST_UNVERIFIED`；只貼 prompt 不算 |
| `O2` CLI 正負運行 | 在同一 allowed root 跑 `case_ok.md` 與 `case_missing.md`；記錄 argv/exit/stdout/stderr | 與凍結 oracle 一致；exit 0 不抵錯誤輸出 | 不符→依 §10 鑑定，不重試未知 |
| `O3` 可逆輸出 | 以受權 wrapper 將 stdout 落至 sandbox output；驗 bytes/hash、source 不變 | 一筆真 file effect＋pre/post readback | 越 output root→停止；不留未記錄檔 |
| `O4` 回復 | 原無檔則只刪本次生成檔；有 preimage 則還原；核 final state | before/after/recovery 一致 | UNKNOWN 先 reconcile，不盲重跑 |
| `O5` Provider OFF | 隔離 profile 不載入舊框架；重跑 direct 與必需行為 | load/import/call trace；同 scope parity | 功能仍依賴舊 provider→architecture finding |
| `O6` Consumer 接力 | 新 session/具名 consumer 讀 HANDOFF、按同版本執行下一合法 readback | 真 consumer action、錯版拒收 | 不能讀→修介面，不假 ACK |

OPS 的 B0 最小內容不是部署系統服務，而是 Native 啟動／續行、一個本地 CLI 的受權運行與輸出、readback、restore。不得要求遠端 Admin、金融或發布權限。

## 08.6 Idempotency、Retry、Unknown

1. Idempotency key 至少含：`task_id + operation_type + repo/host + preimage_sha + write_set_sha + grant_ref`。
2. 同一 key 重放只允許同 postimage 或明確 no-op；不得產生第二份不同效果。
3. 只允許可證的暫時 I/O 失敗重試；重試前先 readback。
4. `UNKNOWN` 先查 pre/post/world/file state 與 Host session；不能確認時停受影操作，不盲 retry。
5. 同一 Finding 最多兩次有實質差額的修補；超出交 Owner/architect 或具名停等。
6. 權限拒絕、完整性失敗、未知寫入不可用「再試一次」掩蓋。

## 08.7 DEV/OPS NEG

| NEG | 預期 |
|---|---|
| caller 自報 HEAD/branch | `REPO_HEAD_MISMATCH`；不寫 |
| `permit=true`／複製 WorkOrder | `FALSE_AUTHORITY`／`NOT_ADMITTED` |
| write-set 外修改 | 停止、還原、`WRITE_SET_VIOLATION` |
| CLI exit 0 但 state/oracle 錯 | `EFFECT_NOT_VERIFIED` |
| `git revert` 當 OPS recovery | `RECOVERY_KIND_MISMATCH` |
| 未知 effect 默認 READ | `EFFECT_MAPPING_UNVERIFIED` |
| 只改 env 就宣 OFF | `OFF_PARITY_UNPROVEN` |
| 只貼 prompt 就宣 Native consumed | `NATIVE_CONSUMPTION_UNPROVEN` |

---

# 09｜TQAEP／24 原 Case／NF-T01..10

**章契約**｜Input：原 T01–T24、NF-R01..10、真 fixture/oracle/runner/checker。Operation：逐案處置、設計 POS/NEG、凍結 expected、實跑 actual、獨立判定。Output：WaveAssurancePlan＋EvidenceReceipt。Consumer：Case Owner、Checker、FAR、consumer。ACC：每必需案有 source/req、fixture、oracle、command、exit、raw、verdict；Expected/Actual 分欄。NEG：UNAVAILABLE 當 zero、改 oracle、作者自簽、原/新分母混算。FirstFail：`RUNNER_UNBOUND`、`EVIDENCE_LAUNDERING`、`ORACLE_DRIFT`、`FALSE_INDEPENDENT`。

## 09.1 基本分帳

- 原 `F5-W0-T01..24` 是歷史 Case 帳；本冊逐案給新版處置，但不把新 NF 結果填入原案 PASS。
- NF-T01..10 是新架構否證案；可與原案共用同一個真 raw trace，但 numerator 只算一次有效執行，分母分開。
- `Expected` 在執行前由 Checker/規格 Owner 凍結；`Observed` 由實跑填；`Verdict` 由獨立 Checker 依 oracle 判斷。
- 沒有真 Runner/Oracle/Fixture 的案只能 `PLANNED`／`NOT_RUN`／`UNBOUND`；不得用作者表格代替。
- Legacy 專屬案若本次產品未承諾，記 `DEFER`／`NotCovered`；不自動算 Generic PASS，也不全部 HOLD。

## 09.2 原 24 Case 的逐案處置

| 原 Case | 處置／理由 | B0 可執行 Oracle／判定 |
|---|---|---|
| `F5-W0-T01` | `KEEP`：真來源與合法 READ 是基礎正向 | 授權 root 內真 file、正確 SHA/span；無 OPS/Publisher gate；有 source inventory 與 read raw |
| `F5-W0-T02` | `KEEP`：byte mutation 防來源漂移 | 對 source 改一 byte；expected SHA 不符；拒舊 trace，記 `SOURCE_INTEGRITY_FAILED` |
| `F5-W0-T03` | `KEEP`：缺 B 不得父項 PASS | `case_missing.md` 只有 A；exit 2／missing 含 B；Reviewer 指名 child；父項不 PASS |
| `F5-W0-T04` | `REPLACE`：不以不存在的 OriginalReader 為前置，但假 ID/ACK 仍拒 | 呼叫者自造 ID/receipt 不得獲得任何權限或驗收；合法 direct READ 不被阻 |
| `F5-W0-T05` | `KEEP`：Guide 不得擴 Scope | A scope 請求被改為 B；allowed root/write-set 不變；拒越權並保留原文 |
| `F5-W0-T06` | `KEEP`＋強化 | `../`、absolute、UNC、symlink/junction/reparse；真讀不得越 root；source SHA 不變 |
| `F5-W0-T07` | `OPTIONAL`：Legacy proposal 兼容另帳；Generic 保留 unknown 負例 | 新版 consumer 對未知 required 欄／版本須 reject 或保真；舊 proposal-1/2 只在原適用域驗 |
| `F5-W0-T08` | `KEEP`：有 code 未啟用不是 CODE_MISSING | 真 code 可見但 Host 未 bound→`BIND_EXISTING/ACTIVATE_HOST`；不得直接 BUILD |
| `F5-W0-T09` | `KEEP`：W4 Release 不倒灌 W0 | 注入 W4 hard-pre；Reviewer 報 `PHASE_OVERREACH_CANDIDATE`；合法 READ 仍可走 |
| `F5-W0-T10` | `KEEP`：後驗不得作前置 | 把自己 post-readback 當 admission prerequisite；DAG 檢出 cycle；不執行該 effect |
| `F5-W0-T11` | `REPLACE`：權限來源改真 OS/Repo/Host grant，但假 permit 仍拒 | `permit=true`／越 write-set／無真 grant→no-op；pre/post 不變；`NOT_ADMITTED` |
| `F5-W0-T12` | `REPLACE`：無 Registry 仍不得默認 READ | 未知 effect alias→拒執行/clarify；`EFFECT_MAPPING_UNVERIFIED`；不建專屬 Registry |
| `F5-W0-T13` | `KEEP`：有權 Native 正向 | 真授權 DEV/OPS 各一筆；pre/post/readback/recovery 正確；raw 可重播 |
| `F5-W0-T14` | `KEEP`：exit 0 不等效果正確 | controlled mutation 使 exit 0 但 output 錯；Checker FAIL；`EFFECT_NOT_VERIFIED` |
| `F5-W0-T15` | `KEEP`：Challenger 不改受審物 | 修改 subject/oracle→拒收；hash mismatch；不採用該證據 |
| `F5-W0-T16` | `KEEP`：candidate 變更後舊 raw 失效 | candidate digest 變、舊 raw 重用→mismatch；只重驗受影 case |
| `F5-W0-T17` | `KEEP`：只有文字總結不成立 | 無 argv/exit/raw→`UNREPRODUCED/NOT_PROVEN`；不得升 Finding |
| `F5-W0-T18` | `KEEP`：UNAVAILABLE ≠ ZERO | 來源不可達時 FAR 回 `RESEARCH_REQUIRED/ABSTAIN`；不得填 0 |
| `F5-W0-T19` | `REPLACE`：不以原 Fabric Reader 為必要，但 FAR 不得越證據/權限 | 無真 raw 或超出 Owner scope→不可 `FIX_NOW/CLOSE`；合法本地證據足夠則可研究 |
| `F5-W0-T20` | `KEEP`：同名 FirstFail 有新 raw 需重鑑定 | 新 source/candidate/expected/raw 存在→不得直接 PARK；計受影 delta |
| `F5-W0-T21` | `KEEP／簡化`：有限停止，不建 PARK service | 同 source/candidate/host/fixture/oracle/FirstFail 無新證據→停重派；有真兩期才比較 no-delta |
| `F5-W0-T22` | `KEEP`：Guide CLOSE ≠ Release | 缺 Checker/Publisher 時不得 RELEASE；記 `CLOSEOUT_ADVICE` 與 not_claimed |
| `F5-W0-T23` | `KEEP`：secret hygiene | sentinel 進 fixture/錯誤路徑；報告/公開輸出無 secret；redaction raw 與 private hash 分開 |
| `F5-W0-T24` | `KEEP＋profile scoped`：Generic 不背 485，FHS 丟適用 ID 必拒 | Generic OFF 冷啟＋合法 READ 成功；FHS 適用子集缺 ID 則該 Profile 拒；485 全量回歸 `DEFER` |

**處置統計**：24/24 有落點；`KEEP` 17、`KEEP／簡化` 1（T21）、`REPLACE` 4（T04/T11/T12/T19）、`OPTIONAL` 1（T07）、`KEEP＋Profile-scoped DEFER` 1（T24）。合計 24。上述統計只是文件處置，不是 pass rate。

## 09.3 NF-T01..10：Native-first 架構否證

| Case／Req | 真執行 | Oracle／判定 | 失敗意義 |
|---|---|---|---|
| `NF-T01/R08` | 隔離 profile 不載入 HGK/FABRIC/SBL/FHS/PIPD general providers；冷啟 B0 代表功能；記 load/import/call trace | 同 scope 結果 parity；無非必要 hard import | 舊框架仍為必要依賴→`ARCHITECTURE_REWORK_REQUIRED` |
| `NF-T02/R01/R03` | 無 OriginalReader service；TPM 以真 file/Git pin；Bridge/合法 direct read 成功；hash/path 負例 | 真 SHA/span；越界拒；不建 Reader | 假 Reader 前置或安全被移除 |
| `NF-T03/R04/R10` | 無 EffectRegistry/Issuer service；用實際 sandbox/OS/owner 範圍；真可逆 write/run＋restore；越權 no-op | pre/post/readback/recovery 正確；越權無效 | 無法安全執行或誤允許越權 |
| `NF-T04/R05` | 無 CaseRegistry/專屬 Runner；用實際 stdlib/repo runner POS/NEG；獨立 checker 不改 oracle | 真 command/exit/raw；oracle 先凍結 | 無法實跑或假驗收 |
| `NF-T05/R03/R08` | Bridge OFF；Native 直接消費完整 pack；與 Bridge-on 的合法結果比較 | direct 可完成；Bridge 專屬案另在 ON 驗 | optional info 被硬化 |
| `NF-T06/R06/R07` | FAR OFF；對明確根因直接 patch/retest；FAR-on 另驗真 root-cause/兩方案 | 明確錯誤不被研究 gate 卡死 | 所有 bug 被 FAR 硬擋 |
| `NF-T07/R01..R06` | 五方各自單獨 invoke：TPM＋Reviewer、Guide、Bridge 四 API、Challenge、FAR | 每方有真輸入/輸出/consumer | 不必要的兄弟依賴或工具未運行 |
| `NF-T08/R01..R07` | 真協作閉環：需求→四契約→start→run→frozen challenge→research→patch→resume→retest | 每段有真 raw，non-covered 明列 | 只有裸 Hermes 或文件候選 |
| `NF-T09/R07` | 一筆真 red（或誠實 controlled mutation）→受影 patch→新 candidate→affected regression | 有實質差額；同質失敗停止 | 只改 status、改 oracle、無限循環 |
| `NF-T10/R09` | B0/W0 handoff 由新 session/具名 consumer 真讀 pack/pin/raw/next；錯版拒 | consumer action/readback；W1 差額具體 | 只有 ACK 字串、無真接收 |

## 09.4 Fixture、Oracle 與 Runner

| 資產 | 要求 | Owner／不可寫者 |
|---|---|---|
| `fixture` | 真 bytes；含 POS/NEG/EDGE/SEC；不含真 secret；有 SHA | Case Owner 凍結；Maker 只讀 |
| `oracle` | 依有效 PI 寫 expected exit、provided/missing/status、semantic state、security refusal | Checker/規格 Owner 先凍結；Maker 不可改 |
| `runner` | 實際 pytest/unittest/CLI 或 repo 既有命令；有 cwd、argv、timeout | Executor 執行；Checker 可重播 |
| `candidate` | Git commit/tree 或 hash manifest；含 source/case-set pins | Maker 凍結；Challenger 不改 |
| `evidence` | raw stdout/stderr、exit、pre/post/recovery、SHA | Checker/Executor 保存；不得覆寫 |

**獨立性**：Maker 與 Challenger/Independent verifier 至少使用分離工作樹／session；若原政策要求不同 principal，必須真不同。相同模型、相同 process 或同一把 write key 不構成 Independent。Checker verdict 與 Consumer readback 是同 Scope 的兩個 distinct receipts；一份簽章或一個 manifest 不得同時扮演兩者。

**B0 fixture 完整性**：SAMPLE-R1/R2/R3/R4 的每個必要負例（invalid UTF-8、hash mismatch、duplicate、ambiguous／malformed、path escape）都必須有 §08.3 的 fixture／argv／expected exit／oracle；沒有者只能標 `PLANNED`，不得用 `case_ok`／`case_missing` 兩案代替。

## 09.5 B0 覆蓋與分母

B0 的必需分母是 `T01..T24` 全部的必要語義，加上 `NF-T01..T10`；其中 `T07` 的 Legacy proposal 相容半與 `T24` 的 485 全量半，只在本次產品承諾時納入，否則記 `DEFER/NotCovered`，但 `T07` 的 Generic unknown-schema 負例與 `T24` 的 Generic OFF／FHS applicable 負例仍必需。`T04/T08/T09/T10/T12` 可與 B0 的來源、能力、phase、cycle、effect 判定共用同一個真 raw trace，但每個原 Case 都必須有明確 verdict 或 NotCovered；不得為了湊 34 案重複跑同一效果，也不得跳過結構負例。

| 分母 | 內容 | 本輪狀態 |
|---|---|---|
| 原 W0 Case | `T01..24` | 文件處置完成；產品 `NOT_RUN` |
| NF 架構案 | `NF-T01..10` | 已設計；產品 `PLANNED` |
| 原 14 WP | `F5-W0-01..14` | 契約完成；執行狀態依 B0 |
| 七 Seam | `SM01..07` | 契約完成；consumer 證據待 B0 |
| FHS Legacy | 22/36/50/39/96/192/485、1011 ledger 等 | 未驗；不進 Generic 分母 |
| 產品具名分母 | QA26／F01–F14；U26／CG-SEM17/20/50；Bridge 38＋28；C16/EC-36/local47；RQ0–8／10 Advice／T20／FARP30/local35 | 只作代表案例；完整分母依 §02.5 分帳至 W1/W2–W4 |
| 檔案自檢 | DOC-01..05 | 另見證據附件；不是產品測試 |

## 09.6 每次執行的最小 receipt

```text
run_id, case_id, candidate_ref/sha, source_refs, fixture_sha, oracle_sha,
cwd, argv, runtime/version, exit (timeout/interrupted 另標),
stdout_path+sha, stderr_path+sha, pre_state, post_state, recovery_ref,
expected, observed, verdict, first_fail, checker_identity, not_covered
```

`expected` 與 `observed` 不得同欄；`exit 0` 不得越過語義 oracle；`NOT_RUN` 不得填 `PASS`；`UNBOUND` 不得填 `ZERO`。redaction 後的 public raw 需標明與 private raw 的關係，不混比 hash。

## 09.7 TQAEP NEG

- 用本地文件檢查冒充原 Case 執行；
- 先看 actual 再改 oracle；
- 由 Maker 修改 fixture/oracle 或自簽 verdict；
- 重用不同 candidate 的舊 raw 不重驗；
- 把 24 原案與 10 NF 案相加成「34 通過」；
- Legacy 全量未驗就宣 FHS Profile PASS；
- 沒有 Raw 卻寫 `INDEPENDENT_PASS`。

---

# 10｜Stop／Resume／HOLD／Claim

**章契約**｜Input：claim、FirstFail、raw/delta、Owner、LastGood、權限/unknown。Operation：分層 claim、定位 ChangeCone、執行有限修補、決定局部停復。Output：WaveGateLedger／StopResumeRecord。Consumer：Program、Owner、Guide、Checker。ACC：每個停點有真缺口、owner、下一個合法動作；無新 delta 不重驗。NEG：全體 HOLD、把 UNKNOWN 當 NA/PASS、無限重派、改 oracle 收斂。FirstFail：`CLAIM_CEILING_VIOLATION`、`NO_DELTA_REWRITE_DENIED`、`UNKNOWN_RETRY_DENIED`。

## 10.1 Claim Ledger

| Claim 層 | 本輪可宣 | 不可宣 | 依據 |
|---|---|---|---|
| 文件／來源 | 新版 00–12、14 WP、24 Case、NF-R/T、七 Seam 已寫；來源 bytes/SHA 可核 | 原域採納、原 Reader ACK | 證據附件 E1/E3/E4 |
| Primary／Author | `PRIMARY_LOCAL_W0M_CURRENT_WITH_SCOPED_EXECUTION_AUTHORIZATION` | `B0_NF_VALIDATED`／`W0_NF_VALIDATED`／外部 Grant | §00.2.2、DOC 自檢 |
| W0-A | 設計與施工入口完整 | `OBSERVED_LOCAL_SLICE`／Native READ PASS | 本輪未跑 |
| W0-B | 條件式 DEV/OPS ECP、權限邊界 | `NATIVE_PASS`／`W0-B 完成` | 無真 repo/host grant |
| W0-C | Legacy 適用性與 OFF 設計 | FHS 485 全 PASS／1011 全驗 | 未跑、未採納 |
| Challenge/FAR | 獨立性、oracle、方案設計 | `INDEPENDENT_PASS`／`FIX_NOW` | 未跑 |
| Release | 交接欄位設計 | `RELEASED`／`MISSION_COMPLETE` | 無 Publisher |

**Claim 規則**：每個 claim 必須有 scope、source/candidate SHA、evidence、owner 與 not_covered。作者自檢、本地 rule check、舊 W1 綠燈、W0 舊 18/18 或 24/24 設計帳，均不得升級為產品 Native/Independent PASS。

## 10.2 FirstFail 與處置

| FirstFail 類 | 典型訊號 | 最小處置 | 不應做 |
|---|---|---|---|
| `ENV_HOST_ROUTE` | binary 不存在、session 不起、route 不明 | 查實際版本/help/root/session；安全 route 不明則停 | 猜命令、下載未知工具 |
| `AUTHORITY` | ACL 拒、write 被拒、principal 不符 | 精確列出操作/root/writes/期限/具權者；其他 READ 可繼續 | 自造 Grant、改 label |
| `SOURCE_IDENTITY` | 同名異 SHA、span 漂移、版本不明 | 隔離、重取真 bytes、選有效版本 | 沿用舊 trace |
| `CAPABILITY` | code 可見未 bound、skill 未 installed | `BIND/ACTIVATE/REPAIR/BUILD_MINIMAL` | 未查即重寫 |
| `SPEC_PI_PD` | 缺 Child、無源 mandatory、ECP 不可施工 | 回 Spec Owner，保凍結 oracle；更新受影版本 | 施工中偷改需求 |
| `ARCHITECTURE` | 舊框架仍 hard import、Seam 硬化、cycle | 在合法無舊框架環境重現、定位 import/config/callsite | 以文件自檢證明 |
| `IMPLEMENTATION` | 真 red、測試失敗、錯 output | 最小 patch、affected regression、獨立 challenge | 改 oracle/閾值 |
| `UNKNOWN_EFFECT` | timeout、中斷、state 不明 | 先 readback/reconcile；確認後才 retry/compensate | 盲重試 |
| `NO_DELTA` | 同 source/candidate/host/fixture/oracle/FirstFail 無新證據 | 停同質重派，記 HOLD | 換 task ID 重跑 |

## 10.3 有限 HARNESS LOOP

```text
inspect real baseline → choose legal slice and expected
→ freeze preimage/oracle/candidate → execute bounded action
→ collect actual raw → independent compare
→ PASS: record / FAIL: FirstFail + ChangeCone
→ patch only affected cone → refreeze → rerun affected POS/NEG/security/consumer
→ close, scoped hold, or architecture rework with named next action
```

上限：同一 read I/O transient 可 retry 一次並先 readback；同一 Finding 最多兩次有實質差額的修補；同質失敗停。權限拒絕、完整性失敗、未知寫入不重試。循環用新 candidate/revision，不是靜態 DAG cycle。

## 10.4 ChangeCone／LastGood

1. `ChangeCone` 由受影 Requirement、Case、source、candidate 檔、Seam、consumer 與 effect 組成。
2. 只重跑 cone 內 POS/NEG/security/consumer；不重跑無關全量，但安全 veto 每次都適用。
3. `LastGood` 是最近一組 hash-stable 的 source/pack/candidate/evidence；修改前保存。
4. 新 candidate 必須重算 digest；舊 raw 只對舊 digest 有效。
5. 修補不得跨出 write-set；跨 cone 的需求變更回 Spec Owner，另立版本。

## 10.5 HOLD 台帳（原 14 項全部保留）

| HOLD | 真缺口 | 新版處置 | Owner／Resume |
|---|---|---|---|
| `W1_HOST_NINE_GRID` | 三 Host 七階段未真觀測 | B0 只驗本輪 target Host；其他 Host 留 W1 | Host Owner；逐 Host actual |
| `W1_PLUGIN_ALIAS` | alias 與 installed ID 未證等價 | 查 manifest/loaded ID；不猜等價 | Plugin/Host Owner；identity probe |
| `W1_ABI_BOUND` | 四 API/Guide IO 未真消費 | B0 on/off 真 invoke；舊 proposal 留原域 | Guide/Bridge Owner；consumer raw |
| `W1_W0_INPUT` | W1 未取得新版 W0 actual | 由 W0 handoff/consumer 真讀；不以舊 author refs 代替 | W1 Owner；同版 handoff |
| `W0_PRIMARY_RECEIPT_STALE` | public/private receipt 版本差 | 保留歷史；新 manifest 另記 before/after | Source Curator；真 origin 核對 |
| `W0-A_CASE_SELECTION` | 真非 FHS sample 未定 | G4 實查或 Owner 採 briefcheck；真 oracle | Project/Source Owner；選定＋授權 |
| `W0-B_NOT_ADMITTED` | 無真 DEV/OPS grant | 用實際 repo/host 權限；原 protected effect 仍需原 admission | Repo/Host Owner；真 ECP |
| `ORIGINAL_READER_UNBOUND` | 無原 PIPD typed reader | Generic 用真 file/Git/consumer；legacy 另帳 | PIPD Owner；typed readback |
| `ORACLE_FIXTURE_UNBOUND` | 原 24 Case 無 oracle/fixture bytes | 建新 NF oracle/fixture；原案不冒 PASS | Case Owner；真 bytes |
| `HOST_CAPABILITY_UNBOUND` | 無 actual served | W0 真 probe；只記已證 | Host Owner；loaded/invoked/consumed |
| `CHECKER_PUBLISHER_UNBOUND` | 無獨立 checker/publisher | 真獨立 verifier；Publisher 不在 B0 | Checker/Publisher；同 candidate raw |
| `SOURCE_REFERENCE_HASH_CONFLICT` | 歷史 CTRL/START 指紋可能不同 | 本輪已重算 PLAN/CTRL；下游以同一 manifest 對位 | Source Curator；version ledger |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` | 1011/485 未解析 ID | Generic OFF 另驗；Legacy 留原分母 | Profile Owner；適用子集 |
| `HOLD_CR-DOC04-STATE-MAP` | 舊 T4/T5 formal transition | 不升格；新版 NF 狀態獨立 | 原 DOC04 具權者；裁決/readback |

**不得**因新增本冊而關閉任何原 HOLD；本冊只提供新適用路徑與 not_claimed。

## 10.5A 歷史 R3-CR／WM2E crosswalk

原 W0M 的 14 項不是所有歷史 HOLD 的聯集；MASTER §26.2 的 `R3-CR01..12` 與原 W0M 附錄的 `WM2E_NOT_READ` 另行保留。下表只作血緣與責任對位，**沒有一項被 CLOSE**。

| 原 HOLD／CR | 新版落點 | 狀態 | 下一步／Owner |
|---|---|---|---|
| `R3-CR01` | `W1_PLUGIN_ALIAS`／`W1_HOST_NINE_GRID` | `OPEN_PRESERVED` | Host alias/manifest；Host Owner |
| `R3-CR02` | `ORIGINAL_READER_UNBOUND` | `OPEN_PRESERVED` | 原 PIPD typed readback；Reader Owner |
| `R3-CR03` | `W0-B_NOT_ADMITTED`／§05.5 第 2 項 | `OPEN_PRESERVED` | RepoContext live probe；Repo Owner |
| `R3-CR04` | `W0-B_NOT_ADMITTED`／§05.5 第 6–8 項 | `OPEN_PRESERVED` | Issuer/WorkOrder/Admission 分列 receipt |
| `R3-CR05` | `HOST_CAPABILITY_UNBOUND`／`W1_ABI_BOUND` | `OPEN_PRESERVED` | loaded/invoked/consumed；Host Owner |
| `R3-CR06` | `CHECKER_PUBLISHER_UNBOUND` | `OPEN_PRESERVED` | Checker 與 Consumer distinct receipts；Publisher 另列 |
| `R3-CR07` | `W4M ToolFit/License DEFER` | `OPEN_PRESERVED` | 35/485 適用子集與授權；W4 Owner |
| `R3-CR08` | `SOURCE_REFERENCE_HASH_CONFLICT` | `OPEN_PRESERVED` | origin/public 分核；Source Curator |
| `R3-CR09` | `W1 CI/Ruleset DEFER` | `OPEN_PRESERVED` | W1/W4M 真 CI；Program Owner |
| `R3-CR10` | `FAR Fabric PROFILE/DEFER` | `OPEN_PRESERVED` | Router/三源只在原 Profile；FAR Owner |
| `R3-CR11` | `W0-A_CASE_SELECTION` | `OPEN_PRESERVED` | 真 sample＋Owner designation；Project Owner |
| `R3-CR12` | `W0-B_NOT_ADMITTED`／§05.5 第 13 項 | `OPEN_PRESERVED` | 真 effect＋Recovery ABI；Repo/Host Owner |
| `WM2E_NOT_READ` | 證據附件 E1 讀取層級 | `HISTORICAL_SUPPORT_ONLY` | 需要時由 Source Curator 讀；不當 CURRENT |

**防 overclaim**：新版只說「原 W1/W0 的 14 項全部保留」＋「R3-CR01..12/WM2E 另列」，不把它們說成同一個 14 或全部已處理。任何一項要 CLOSE，必須有同 ID、同 Scope、真 Owner 收據與 next-state evidence。

## 10.6 局部阻斷

1. 缺 Bridge 只停 Bridge 專屬測試；Guide direct、TPM、Challenge、FAR 可繼續。
2. 缺 FAR 只停「需研究」的 Finding；明確 bug 可依 §10.3 直接修。
3. 缺 DEV/OPS 權限只停該 effect；READ/DRAFT、文件、測試設計可繼續。
4. 缺 FHS Legacy 來源只停受影子集；Generic B0 不因 485 未全驗而停。
5. 缺 consumer 時先修交接介面；不得用假 ACK 解鎖 Release。

## 10.7 Unknown 與失敗鑑定

`UNKNOWN` 不是 PASS/NA。先查 pre/post、world/file state、Host session、process 與 evidence；不能排除副作用時停受影操作。B0 失敗必須分類：

| 根因 | 證據 | 下一步 |
|---|---|---|
| 環境/Host | 命令/版本/session/route 真錯誤 | 修環境或換合法 route；不判架構失敗 |
| 權限 | ACL/grant 缺失 | AUTHORITY_REQUEST；其他 read 可續 |
| 樣本 | 需求/資料不適合 | 換 sample，保留理由 |
| 設計/規格 | 缺 Child、ECP 不可施工 | 回 Spec Owner，重凍結 |
| 程式 | 真 red、可重現 bug | patch＋affected retest |
| 架構 | 去耦合後必要功能不能運作 | `ARCHITECTURE_REWORK_REQUIRED`，回 ADR/W0M/pack |
| 驗收 | oracle/runner/獨立性不足 | 修 checker/證據，不改預期 |

---

# 11｜Wn Pack Split／六檔 W0 編包契約

**章契約**｜Input：本冊 00–12、真環境、真權限、source/case/oracle。Operation：定義六檔單一真源、consumer、舊 15 檔 crosswalk、projection 規則。Output：ExecutionPackSpec。Consumer：W0 Pack Author、Guide、Executor、Checker。ACC：六檔可獨立編製、每個內容有真源、舊 consumer 有映射。NEG：雙寫 canonical、舊 guard 倒卡新包、空殼/只引用 W0M。FirstFail：`PACKAGE_INCOMPLETE`、`PACKAGE_INTEGRITY_HOLD`、`TQAEP_CONTRACT_MISMATCH`。

## 11.1 單一真源：六檔

下一輪 W0 控制包應放在 Owner 指定目錄（建議 `FHS-5_PLP_W0_NATIVE_FIRST/`），恰含六個主檔。每檔必須有實質正文；不得只寫「見 W0M」。

| # | 檔名 | 必備實質內容 | 主要 consumer |
|---|---|---|---|
| 1 | `00_W0_PI_PD.md` | Goal/FUO/Done/non-goal；NF01–10；source clause；NF-R01..10 Parent/Child/NEG；A/B/C+B0；capability/IO；14 WP/edges；work order sequence；effect boundary；sample/repo context；W1 not_claimed | Program、Reviewer、Guide、Executor、Checker |
| 2 | `01_W0_DEV_ECP.md` | exact repo/root/HEAD/branch/dirty（probe 值或 `UNBOUND`）；逐檔 write-set；preimage/absent；**planned exact argv/cwd/env/timeout、expected exit/stdout assertions、planned diff scope**；bounded Maker；tests；readback/undo；禁寫；authority gaps/next。不得在本檔填 actual result | Maker、Repo Owner、Checker |
| 3 | `02_W0_OPS_ECP.md` | 已 probe 的 Hermes profile/route 或 `UNBOUND`＋**planned invocation**；Python/Git versions；entrypoint；input/output；argv；timeout；expected exit/stdout；readback；stop/reconcile/recovery；no external effect default。不得在本檔填 actual result | Executor、Host Owner、Checker |
| 4 | `03_W0_TQAEP.md` | 24 case crosswalk；NF-T；真 oracle/fixture pins；expected exit/raw；independent verifier；security negatives；scope-specific pass/not covered；receipt schema | Case Owner、Checker、FAR |
| 5 | `04_W0_START_THIN_PROMPT.md` | 單一 pack ref；goal；stage；authority limits；execute/test/fix；B0 done；CLOSEOUT/next；不重抄 MASTER、不加不存在 tool/route | Guide、Native Executor |
| 6 | `05_W0_SOURCE_MANIFEST.json` | source paths、raw SHA/bytes/lines/version/role；其餘五檔 SHA；project/wave/batch/scope；manifest 自身 hash 外部記錄；source/pack identity 分開 | Source Curator、Pack Author、consumer |

## 11.2 各檔的拒收條件

| 檔 | 不可接受 |
|---|---|
| `00` | 只有 WP 名稱、沒有 Child/NEG/edge；未填 source/capability；把 `INFO_ONLY` 畫成 hard |
| `01` | 全 repo glob、無 preimage、無 rollback、把 ECP 當 Grant、無可執行 planned argv/cwd/timeout/write-set、把 actual result 寫進 planned ECP |
| `02` | 假 Hermes 版本/route；只貼 prompt 當 consumed；無 timeout/readback/recovery、無 planned argv/expected exit；把 actual result 寫進 planned ECP |
| `03` | 24 原案漏項；無 oracle；把 actual 寫成 expected；Maker 自簽；Legacy/Generic 混算 |
| `04` | 重複 MASTER；擴 Scope；虛構工具；把未跑寫成 Done；沒有 Stop/Resume |
| `05` | 自含自身 hash 循環；Git blob SHA 當 raw SHA；缺 bytes/lines/role；source/pack 混一 |

## 11.3 舊 15 檔 → 六檔 crosswalk

| 舊 15 檔 | 新落點 | 保留語義 |
|---|---|---|
| `00_WAVE_RUN_MANIFEST.md` | `00`＋`05` | Wave/Subject/Scope/Source |
| `00_WAVE_RUN_MANIFEST.json` | 由 `00`/`05` 生成必要投影 | 同 MD 的機器投影 |
| `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | `00` | Source/Scope/Construction |
| `02_ORIGINAL_CONTRACT_REFS.json` | `00` 的 Legacy ref／適用性 | 原 PI/PD/ECP/TQAEP refs |
| `03_DEV_ECP.md` | `01` | DEV ECP |
| `04_OPS_ECP.md` | `02` | OPS ECP |
| `05_PLANNED_TQAEP.md` | `03` | Case/Oracle/ExpectedRaw |
| `05_PLANNED_TQAEP.json` | 由 `03` 生成投影 | `projection_of_sha256` |
| `06_PERMISSION_STOP_RESUME.md` | `01`/`02`＋`00` 安全段 | Permission/Stop/Resume |
| `07_EVIDENCE_AND_CHECKER.md` | `03` | Evidence/Checker |
| `08_AS_BUILT_AND_HANDOFF.md` | 執行後 CLOSEOUT/HANDOFF | 施工前只定驗收契約 |
| `09_README_RUN_ORDER.md` | `00`/`04` | Run order |
| `{wave_id}_START_THIN_PROMPT.md` | `04` | ThinStart |
| `SOURCE_MANIFEST.json` | `05` | 真 Source SHA/bytes/lines |
| `PACKAGE_FILE_MANIFEST.json` | `05` 的 file hash 段／外部 seal | 每檔 raw SHA |

JSON 只在真 consumer 需要時，由同一真源**生成**，不能與 MD 手動雙寫；舊 loader 需要相容時，保持版本隔離與 loss report，不讓舊 guard 反向要求 15 檔。

## 11.4 `05_W0_SOURCE_MANIFEST.json` 最小結構

```json
{
  "schema": "FHS5.PLP.W0.SourceManifest.NF@1",
  "project_id": "FHS-5_PLP",
  "wave_id": "FHS-5_PLP/W0",
  "batch_id": "B0-NF",
  "scope": "<adopted W0 scope>",
  "nf_adr": ["NF01", "NF02", "NF03", "NF04", "NF05", "NF06", "NF07", "NF08", "NF09", "NF10"],
  "pack_files": [
    {"path": "00_W0_PI_PD.md", "sha256": "<computed-file-sha256>", "bytes": 0},
    {"path": "01_W0_DEV_ECP.md", "sha256": "<computed-file-sha256>", "bytes": 0},
    {"path": "02_W0_OPS_ECP.md", "sha256": "<computed-file-sha256>", "bytes": 0},
    {"path": "03_W0_TQAEP.md", "sha256": "<computed-file-sha256>", "bytes": 0},
    {"path": "04_W0_START_THIN_PROMPT.md", "sha256": "<computed-file-sha256>", "bytes": 0}
  ],
  "sources": [
    {"id": "S01", "path": "<actual path>", "version": "<actual>", "role": "source", "sha256": "<raw>", "bytes": 0, "lines": 0}
  ],
  "manifest_self_hash": "EXTERNAL_RECORD_ONLY"
}
```

`bytes:0` 是結構示例，不得當真值交付；Pack Author 必填實算。`manifest_self_hash` 不可自含循環；以外部 receipt/seal 記錄。

## 11.5 編包與執行順序

1. 先由 `00` 固化 Goal/FUO/14 WP/edges、source/authority 與 B0 sample。
2. 再由 `01`/`02` 固化 exact DEV/OPS 邊界；以 probe 填環境值（版本/route/root/principal），但不得填執行結果；執行結果留待 EVIDENCE。
3. 由 `03` 固化原 24 案 crosswalk、NF-T、oracle/fixture、checker 與 receipt。
4. 由 `04` 生成單一 ThinStart；不重抄整冊，不加不存在工具。
5. 最後由 `05` 實算五檔和來源；外部記錄自身 hash。
6. 執行前做 pack integrity：六檔存在、UTF-8、link/digest、source/pack identity、TQAEP 投影、no self-cycle。
7. 六檔以外的 EVIDENCE、CLOSEOUT、HANDOFF、CHANGESET 是執行後工件，不預先填 actual。

**`planned` 與 `actual` 的硬分界**：

- `01/02` 只承載 `PLANNED`：exact 目標、argv、cwd、env、timeout、expected exit/stdout、write-set、preimage/absent、rollback。
- `actual` 的 command/exit/stdout/stderr/raw/preimage/postimage/recovery 只在執行後進 `EVIDENCE/`、`CLOSEOUT`、`HANDOFF`；pack integrity 不要求、也不得接受 actual。
- 若 `01/02` 出現 actual result、未標來源的 exit code 或「本輪已跑」字樣，pack 檢查直接 `PACKAGE_INTEGRITY_HOLD`。
- 未取得真 Repo/Host 時，`01/02` 的環境欄可填 `UNBOUND` 與 probe 方法；不得以假值通過。

## 11.6 本輪邊界

本輪**不生成**六檔、`EVIDENCE/`、`B0_CLOSEOUT.md`、`B0_HANDOFF.md`、`W0_CLOSEOUT.md`、`W0_HANDOFF.md` 或 `W0_UPSTREAM_CHANGESET.md`。本章只提供下一輪可控的編包規格；任何六檔實體必須由下一輪作者依真環境建立。

---

# 12｜As-Built／Handoff／Next Wave

**章契約**｜Input：B0/W0 真證據、NotCovered、LastGood、W1 既有成果、上游 source。Operation：判定 B0/W0 狀態、產 CLOSEOUT/HANDOFF/ChangeSet、分層 W1 准入、排 MASTER 回寫。Output：WaveClosure、Handoff、UpstreamChangeSet。Consumer：Program、W1/後波、上游 Owner。ACC：每欄有真 ref；沒有 actual 就空白/NotRun；consumer 真讀回。NEG：Expected 當 actual、Wn 未跑填 AsBuilt PASS、W4 倒灌 W0、無 delta 重寫全波。FirstFail：`AS_BUILT_OVERCLAIM`、`RELEASE_NOT_CLAIMED`、`HANDOFF_UNCONSUMED`。

## 12.1 B0／W0 退出

| 狀態 | 成立條件 |
|---|---|
| `B0_NF_VALIDATED` | 採納版 B0 PI/PD/ECP/TQAEP；五方 individual＋協作真 invoke；合法 DEV/OPS；獨立 POS/NEG；red→patch→retest；Legacy/optional OFF；安全；consumer readback 全部真通過 |
| `B0_PARTIAL_VALIDATED` | 有真證據但未達全部必要條件；逐能力列 FirstFail、NotCovered、下一操作 |
| `B0_BLOCKED_EXTERNAL` | 具名外部環境/權限/來源缺口；只封受影 effect，其他合法工作可續 |
| `B0_ARCHITECTURE_REWORK_REQUIRED` | 依 §10.7 真否證；回 ADR/W0M/pack/實作，不虛報完成 |
| `W0_NF_VALIDATED` | B0 成功且採納版 W0 全部必需 FUO/Case 已涵蓋；缺項追加最少 Bn、整合 recheck |

`W0_NF_VALIDATED` 不等於 `MISSION_COMPLETE`、Original Acceptance 或 Release。即使 W0 未全過，也可做有證據的 partial CLOSEOUT 與架構回修。

**主用不預判 B0**：§00.2.2 已授權本地執行，但 `B0_NF_VALIDATED` 仍只能由真 PI/PD/ECP/TQAEP、真五方 invoke、真 DEV/OPS、獨立 POS/NEG、OFF parity、安全與 consumer readback 成立。授權是「可以做」，不是「已做完」。

## 12.2 CLOSEOUT 最小欄

| 區 | 必填 |
|---|---|
| Identity | project、work_id、scope、stage(B0/W0)、source/pack digest、baseline/head、new commit/tree、NF-ADR refs |
| A/B/C | 各線實際 disposition、NotCovered |
| WP | `F5-W0-01..14` 實際 disposition |
| Case | 24 原案映射＋NF-T 真 verdict／NotCovered；分母不混 |
| 五方 | individual／combined outcome、真 consumer |
| Native | actual DEV/OPS/undo、Host/session、Provider OFF trace |
| Assurance | checker identity、oracle/fixture pin、FirstFail、LastGood |
| Claim | 每個 claim 的 ceiling、not_claimed、未跑項 |

**不得**把 expected 寫成 actual；不得只寫「全部通過」；不得用作者自檢代替 checker。

## 12.3 HANDOFF 最小欄

```text
handoff_id, from_stage, to_stage, project/work_id,
pack_ref+sha, candidate_ref+sha, source_refs, evidence_refs,
target_consumer+version, actual_readback(argv/exit/raw/action),
next_legal_action, owner, dependencies, resume_predicate,
not_covered, w1_technical_readiness, w1_execution_readiness
```

Consumer 必須真讀 pack、pin、actual output 與 next；不能讀回時保持 partial，不以 ACK 字串或 manifest 存在代替。W1 的技術與施工准入分開：

| 層 | 判定 |
|---|---|
| `W1_TECHNICALLY_READY` | W0_NF_VALIDATED＋真 handoff＋W1 必需輸入可被實際/具權 consumer 消費 |
| `W1_EXECUTION_READY` | 上位受影條款正式採納、W1M/下一包一致、必要能力/授權/入口到位；舊 W1 候選按差額 requalify |

## 12.4 UPSTREAM_CHANGESET 最小欄

| 欄 | 內容 |
|---|---|
| Source | 原 source/section/requirement/version/hash |
| Old dependency | 被取代的 Reader/Registry/Runner/15 檔/Gate |
| Finding | 真 raw、FirstFail、重現 |
| Root cause | 環境/權限/規格/程式/架構/驗收 |
| Decision | 採納 NF-ADR、KEEP/REPLACE/REMOVE/OPTIONAL/DEFER |
| New requirement | NF-R/NF-T、owner、acceptance |
| Impact | PROG/PROJ/WM/Wn、consumer、ABI、case、分母 |
| Regression | 受影 POS/NEG/consumer，LastGood |
| Owner | 該 ChangeSet 的決策／施工責任人 |
| `last_good_ref` | 最近 hash-stable 的 source/pack/candidate/evidence 參照 |
| `resume_predicate` | 何種新證據、權限或版本可恢復受影工作 |

每個 REMOVE 必須有正反向 trace 與理由；不得以全文 keyword count 清零作完成指標。

## 12.5 MASTER／PROG／PROJ／WM 回寫順序

1. 先由 W0 真 Raw→FirstFail→responsibility→original requirement/case→ChangeCone 建 ChangeSet。
2. 先回寫 MASTER 共通法位、Product、Architecture/ADR/Seam、Program、WnM、FileContract、W0、分波、Delta、guard/claims/CR 的受影段。
3. 再回寫 PROG-00：P00-01..06 有效責任、7 Seam、六檔、分母、CR；NoGlobalGate。
4. 再平行回寫五 PROJ 的非重疊受影段：TPM/Reviewer、Guide、Bridge、Challenge、FAR。
5. 最後一次跨冊一致性：版本、欄位、case、consumer、未受影內容、無源 mandatory。
6. WM/W0M/W1M..W4M 只在真 material delta 後更新；W1 既有成果按差額 requalify，不重啟全部工程。
7. 未受影段落保留；不得把未採納相容變更混稱 CURRENT。

## 12.6 本輪 As-Built 與交接

| 項目 | 本輪實際 |
|---|---|
| W0M 正文 | 已寫成；00–12；14 WP、24 Case、7 Seam、NF-R/T 均在位 |
| 證據附件 | 已寫成；來源、差額、DOC 檢測、後續交接 |
| 來源 | 只讀；未覆寫 PLAN/Master/W0M/W0/W1/MASTER |
| 主用／授權 | `W0M-NF-PRIMARY-20261125-01`；本地 primary，受界可執行 |
| 產品 Repo/Host | 未寫、未跑；受界執行已授權，實際 ACL/grant/host 仍待 probe |
| B0/W0 | `NOT_RUN`；不是 `B0_NF_VALIDATED` |
| Native/Independent/Release | `NOT_CLAIMED` |
| 下一輪 | 依 §11 編六檔 W0 包；先 probe 真環境、選 G4/briefcheck、凍結 oracle |

**交接限制**：本冊可供作者層的 W0 編包，但不提供任何實際環境值、權限、Oracle 或產品 Raw。下一輪若缺真 Repo/Host/sample，只停受影施工，不以本冊的候選命令代跑。

## 12.7 最終作者聲明

本冊完成了原 W0M 的 Native-first 作者重構，並經 Human Owner 於 2026-11-25 升格為本地 primary Current、授予受界可執行許可：保留 14 WP、24 Case、七 Seam 與原安全責任；把 Generic 的非必要 Reader/Registry/Runner/ACK/15 檔依賴降為 Legacy 或直接能力；將 B0 最小實證、真權限、獨立驗收、Optional bypass、有限 LOOP、W0→W1 交接與 MASTER 實證回寫寫成可施工契約。它**不是** B0/W0 產品實跑報告，也不代表任何原域 HOLD、外部權限或 Release 已解除。

---

**文件結束**｜W0M `NF-r3-PRIMARY`｜本地主用＋受界可執行
