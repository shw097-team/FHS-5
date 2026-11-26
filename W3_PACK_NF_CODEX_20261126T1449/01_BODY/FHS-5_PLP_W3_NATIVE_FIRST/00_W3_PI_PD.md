# FHS-5_PLP｜W3｜PI／PD 主規範｜Frozen Challenge → FAR Typed Research → Guide Touchpoint-2

**artifact_kind**：`WaveControlPack / PI-PD`
**project_id**：`FHS-5_PLP`｜**wave_id**：`W3`
**subject_id**：`FHS-5_PLP/W3/CONTROL_PACK`｜**scope**：`W3-NF-01`
**artifact_id**：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`｜**version**：`r2`
**profile**：`GENERIC_NATIVE_FIRST`
**selection_state**：`PACK_PRIMARY_SELECTED`（依決策 `W3-PACK-PRIMARY-20261126-01`、§06 V1–V3 PASS 與外置 adoption／seal 綁定；見 §00.2）
**claim_ceiling**：`PACK_PRIMARY / LOCAL_DOCUMENT_VERIFIED / PACK_EXECUTABLE`
**not_claimed**：`W2_NF_VALIDATED`、`W3_TECHNICALLY_READY`、`W3_NF_VALIDATED`、`INDEPENDENT_PASS`、`RELEASED`；`W3_EXECUTION_READY` 只在 §00.2 的 scope／op 內成立
**adoption_decision**：`W3-PACK-PRIMARY-20261126-01`
**supersedes**：`FHS5-PLP/W3/PACK-NF-20261126-r1`（歷史保留，不刪）
**line_count_convention**：`len(raw.decode("utf-8").splitlines())`；1-based inclusive span；不混用 LF-count 與 trailing-newline 計數
**日期**：2026-11-26（Asia/Taipei）
**配對**：`01_W3_DEV_ECP.md`、`02_W3_OPS_ECP.md`、`03_W3_TQAEP.md`、`04_W3_START_THIN_PROMPT.md`、`05_W3_SOURCE_MANIFEST.json`

> **怎麼讀**：本檔是 W3 六檔的唯一主規範。它把「W3 要證明什麼、用哪些原案、哪個工作包產生什麼、什麼不能做、什麼狀態只能保留」寫成可施工契約。`01/02` 只承載保護性寫入與 Host 操作的 exact 契約；`03` 承載逐案 fixture／oracle／runner／expected／observed／NotCovered；`04` 是真實 W3 產品施工的薄啟動；`05` 是機讀來源與檔案 pin。證據附件只承載「來源怎麼核、檢測怎麼做」，不承載第二份規範。
>
> **本檔不主張**：不是 W3M 替代件、不是正式產品測試收據、不是 W2 或 W3 的技術 readiness 宣告。所有 `NOT_RUN`、`UNBOUND`、`HOLD`、`DESIGN` 均為真實狀態；不得為求綠而刪除或改名。本輪文件層已由唯一 Human Owner 預授權採納，但產品層仍 `NOT_CLAIMED`。

---

# 00｜Identity／Authority／Source

## 00.1 身份與法位

| 欄位 | 本包值 | 說明 |
|---|---|---|
| `project_id` | `FHS-5_PLP` | 專案身份 |
| `wave_id` | `W3` | 本波 |
| `subject_id` | `FHS-5_PLP/W3/CONTROL_PACK` | W3 控制包主體，不是 W2 產品主體 |
| `scope` | `W3-NF-01` | 本包 scope；W2 仍為 `W2-NF-01` |
| `artifact_id` | `FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY` | r2 主用文件包；取代 r1 作者候選 |
| `profile` | `GENERIC_NATIVE_FIRST` | Generic 為主；Legacy 只在明示 profile 與原分母內 |
| `selection_state` | `PACK_PRIMARY_SELECTED` | 由唯一 Human Owner 本輪明示預授權＋§06 V1–V3 PASS＋外置 adoption/seal 成立 |
| `executor_effect` | `SOURCE_READ + ISOLATED_DRAFT_WRITE + LOCAL_DOCUMENT_CHECK + BOUNDED_SMOKE + W3_DOC_PUBLISH` | CODEX 是 delegated executor／recorder，不是第二 issuer |
| `product_effect` | `NONE` | 未正式執行 W3 16 原案、未寫 W2 protected writer、未發 Grant／Release |
| `claim_ceiling` | `PACK_PRIMARY / LOCAL_DOCUMENT_VERIFIED / PACK_EXECUTABLE` | 可合法起工；不等同產品 readiness |
| `external_seal` | `../../EXTERNAL_SEAL.json`（pack 外） | 綁定 `05` raw SHA、tree 與版本；不回寫 `05` |
| `LastGood` | `FHS5-PLP/W3/PACK-NF-20261126-r1` | r1 完整保留；本版不覆寫 |

**身份分離**：

1. **W3 文件身份**：本包 `FHS-5_PLP/W3/CONTROL_PACK`／`W3-NF-01`。
2. **W3M 設計身份**：`FHS5-PLP/W3M/2026-11-25-cnf-r2`；是本包的設計依據，不是本包本身。
3. **W2 runtime subject**：`FHS-5_PLP/W2/CONTROL_PACK`／`W2-NF-01`；在本包只作 frozen upstream input，不得改寫成 W3，也不得被 W3 scope 解封。
4. **被測候選 identity**：W2 產品五 member aggregate `8b4b4068…`；本包不得把 W3 文件 SHA 當成該候選 SHA。

## 00.2 本次 Owner 決策、主用綁定與有界授權

### 00.2.1 決策記錄（實質內容）

本輪使用者明示：「對於進行檢測、檢查、修補後產出的修補升級新版定稿 W3 執行控制小包，直接升格／授權／宣達為主用＋可執行施工」，並授權按需使用指定 GitHub 認證及必要上傳。此為本輪唯一決策來源；不再要求第二位 Owner 或逐項事後簽章。

| 決策欄位 | 本輪有效值 |
|---|---|
| `decision_id` | `W3-PACK-PRIMARY-20261126-01` |
| `decision_maker` / `issuer` | 唯一 Human Owner（本任務使用者）；CODEX 為 delegated executor／recorder |
| `subject` / `scope` | `FHS-5_PLP/W3/CONTROL_PACK` / `W3-NF-01`；不含 W2 protected scope |
| `decision_kind` | scoped pack repair + primary adoption + authorized W3 start + pack publication |
| `roots` | `S` 唯讀；`R` 的 O 隔離根與 O 內合法 clone/worktree；`G` 的 W3 文件交付位置；`K` 僅認證程序按需使用 |
| `operations` / `effects` | READ、DRAFT、LOCAL_DOCUMENT_CHECK、隔離 fixture/smoke、O 內 ADD/MODIFY 新版六檔與必要 assets、證據／指標／回復、Git fetch/clone/commit/push 限本輪 W3 文件 |
| `not_authorized` | W2 protected writer、外部 Release、部署、正式產品 DEV 的任意 protected repo 寫入、Host 管理員權限 |
| `effective` / `expiry` | 本次啟動起；本輪修補／交付完成或 Owner 撤權、scope/Host/policy/風險實質變更，以較早者為準 |
| `adoption` | §06 PASS 後以真 `05` SHA／外置 seal／acceptance receipt 綁定；不假稱 Owner 親手事後簽章 |
| `recovery` | 新增物可刪本輪未發布檔；修改用 exact preimage/reverse patch；remote 非破壞性回復以新 commit/pointer 恢復 LastGood，不 force push/reset 共用歷史 |

### 00.2.2 狀態階梯（不得互相冒充）

| 狀態 | 如何成立 | 不可由什麼替代 |
|---|---|---|
| `PACK_PRIMARY_SELECTED` | 本包完整性、內容與可達性 V1–V3 PASS；外置 acceptance 綁 `05` raw SHA／seal | 作者自簽、只有檔案存在、只有 summary |
| `PACK_EXECUTABLE` | 主用包可實際解析、啟動、選合法下一動作；至少真 intake/positive/negative smoke | 只列檔、只傳 hash、只讀 checksum |
| `W3_TECHNICALLY_READY` | W2 required requalification＋當期 clean receive＋真 pin/fixture/runner/capability | 本包 DOC/smoke green |
| `W3_EXECUTION_READY` | 依 scope/op/effect 的真 ACL、roots、preimage、expiry、recovery 與上游前件 | 主用宣達、ECP 表格、`permit=true` |
| `W3_NF_VALIDATED` / `INDEPENDENT_PASS` | 正式產品原判準全成立；distinct Checker/Consumer receipts | 代表樣本、local unit、舊 W2 15/16 收據 |
| `publication_state` | 真 remote branch/commit/current pointer 讀回；或 `PUSH_BLOCKED` | 本地 commit 冒 push、sandbox URL |

### 00.2.3 後續 W3 施工的持續授權

Owner 同意本主用包可按規範自主啟動合法 W3 施工。此授權是**有界 standing authorization**，不是空白 Grant：

| 授權維度 | 內容 |
|---|---|
| 新施工根 | `R` 內新 W3 施工隔離根（例：`R/W3_EXEC_<run_id>`）；不得寫 `S`、W2 protected 路徑或無關專案 |
| 允許 ops | `READ`、`DRAFT`、`P01 intake`、合法本地測試、受界可逆 W3 DEV/OPS、隔離 smoke、受影 retest |
| exact bind | 每個 batch 在第一次副作用前列實際 `path/op/preimage-or-absence/refs/base SHA/rollback`；一次 scope decision 可覆蓋批次，agent 逐步 bind write-set，不另設人類簽核 |
| preimage | ADD 必證 absence；MODIFY 必附真 preimage SHA；同名檔不得靜默覆寫 |
| rollback | 新增物刪除；修改用 exact reverse patch；保留 LastGood；不得 `git reset --hard`／force push 共用歷史 |
| expiry / revocation | 本輪交付完成、Owner 撤權、scope/Host/policy/風險實質變更、受影安全 Finding；以較早者為準 |
| 跨 scope | 共享 W1/W2 模組若涉既有撤權、原政策或超出 W3 文件／隔離施工範圍，只做隔離 proposal／受影 regression；跨 scope 真產品寫入需原授權 |

**W2 例外**：W2 writer 仍 `BLOCKED_NOT_ADMITTED`。任何 W2 真產品寫入需 Owner 在 **W2 scope** 新具名授權；不得用本包 §00.2 解封、刪 marker、改 gate 或重簽原 decision。

### 00.2.4 SoD 與角色

TPM/Reviewer/Case Owner/Source Curator/Repo Owner/Host Owner/Runner/Challenger/FAR/Guide/Checker/Consumer/Publisher 是職責，不是第二人類或每 WP 簽章。CODEX 主 session 調度，可用 native 子代理／另一 read-only session／隔離 worktree 做挑戰與覆核；不新建 queue/issuer daemon。Checker 用可信固定 verifier 及已凍結候選；Maker 自檢不冒獨立產品驗收。Checker verdict 與 fresh Consumer 真 parse/use receipt 分開。平台原規則要求不同 principal/正式原域 Checker 時，缺即 `NOT_CLAIMED`。

### 00.2.5 拒絕面（負例）

以下任一情況必須 zero-write／stop-scoped，不得「先跑再補」：

1. 偽造／過期／錯 subject/scope 的 decision，或要求第二位 Owner 才可採納。
2. 05 raw SHA 與外置 seal 不符、tree 不符、seal 指向舊版本。
3. 以 W3 scope 解封 W2 writer、刪 W2 撤權 marker、改 W2 gate。
4. Advice、Guide NextOperation、`permit=true`、ECP 表格被當 Grant。
5. 同一 process／同一 Maker 自簽 Checker 或 Consumer。
6. 寫 frozen subject/test/oracle/threshold，或 path escape/symlink/junction/reparse 越界。
7. 16 原案被填入假 observed，或未跑宣 `W3_NF_VALIDATED`。
8. secret 進入模型、argv、log、repo 或子代理。

## 00.3 來源角色與作者側 pins

本表以本機實際 bytes 重算；`bytes` 為 raw bytes，`lines` 為 UTF-8 解碼後行數。`PLAN` 與 `WM3` 的 SHA 與控制包 §02.2 給定值一致；`WM0-R4` 與 W0 採納 amendment 一致。本表列 19 個文件來源；`05` 另含 5 個 W2 pack body（`00–04`）與 4 個 W2 pins（current/five pins/05/25 manifest），合計 28 個來源。

| ID | 來源 | bytes | lines | raw SHA-256 | 角色／讀取層級 |
|---|---|---:|---:|---|---|
| `PLAN` | `FHS-5_PLP_W3_CODEX-NATIVE-FIRST_工程方案.md` | 134,580 | 997 | `f15d3da9f0e5fa5ad07e24be5eddb99e80693d67a0e9a049f00991b8057545e3` | 主編製依據；全文讀 |
| `WM3` | `FHS-5_PLP_W3M_CODEX-NATIVE-FIRST_完整實質正文.md` | 63,090 | 961 | `a8addf259097d6507f64c233c704402389c1cb65aba1bb1325d6337341d0c292` | 直接 Wave Master；00–12 與 NF 條款 |
| `WM0-R3` | `FHS-5_PLP_W0M_完整實質正文.md` | 106,859 | 1,176 | `a1f186cc337a4b3828e53f77533df5c97fdda63e132521d861a79b884f0c3aef` | NF-r3-PRIMARY；與 r4 區隔 |
| `WM0-R4` | `..._CODEX-FIRST-r4.md` | 108,861 | 1,191 | `c9b1ca9bbcd5ce87fdbcb0fc373cb8c36d1ad8d404b55c4f7311fc6c2bbddfd5` | W0 採納 amendment；六檔、Owner/SoD、Effect、actual writeback |
| `C0` | `FHS-5_PLP_W0_CLOSEOUT.md` | 21,927 | 290 | `23cfa1f640227c0f3ede052faacbeb14364f5a9337ca436970449de500827b3f` | W0 actual；44 receipts、M1–M3 |
| `H0` | `FHS-5_PLP_W0_HANDOFF.md` | 3,265 | 67 | `21ed226738abbd75b72871f1c6173b83de5cadab661f2d366df8d7e547ff4579` | W0→W1 pins |
| `C1` | `FHS-5_PLP_W1_CLOSEOUT.md` | 9,231 | 172 | `2954523723b8275298299727b3f615d9d717536af464532b9eb2c0100055ac4a` | W1 validated；118 closure rows |
| `H1` | `FHS-5_PLP_W1_HANDOFF.md` | 1,891 | 45 | `ffea91770c055bf800889e268d265d046b81d7ae79433069fcff0b7f489b38d9` | W1→W2 entry/pins |
| `C2` | `FHS-5_PLP_W2_CLOSEOUT.md` | 8,824 | 132 | `6dfba0997862e22efe6dbd22f1fe5db9dd00a8173029111c9a930a84ae127618` | W2 PARTIAL、撤權、W3 P01 |
| `H2` | `FHS-5_PLP_W2_HANDOFF.md` | 5,952 | 112 | `e2c759a9b608deda654ccd9ff90b6c49cc60d3e905c4160a8d3b9419fd05f910` | W2 交接、R0–R7 前置 |
| `B00` | `FHS-5_PLP_PROG-00_CODEX-NATIVE-FIRST_完整實質正文.md` | 126,626 | 908 | `cdd1d76ec20fad19bff96153b11a65a1d0ba98074e4d68d2abfaae5a72c89797` | 上位 Program；§04.B/07.B–12.B |
| `B01` | `FHS-5_PLP_PROJ-01_...md` | 68,023 | 574 | `aa823374dabce5218611a248fda3c8f68a7f0b0d6b51ffa2e4915f7aec4d0392` | TPM/Reviewer；F01–14/U01–16/QA26 |
| `B02` | `FHS-5_PLP_PROJ-02_...md` | 65,006 | 596 | `37022f33e5a67ad3165b0a47d36b359255f13719047fa71508e2b80624fc3884` | Guide；雙觸點、九鍵、U-034 |
| `B03` | `FHS-5_PLP_PROJ-03_...md` | 56,268 | 490 | `a13a9df4252a557a3e246035f136295fe1cad5990e828f9ec3d5df083307db98` | Bridge；四 API、BodyResolver |
| `B04` | `FHS-5_PLP_PROJ-04_...md` | 57,182 | 506 | `fb529a784b7d929f15a23ed63ea82b7d5f5117e927311b1f164eb005da469323` | Challenge；EC-FR01–16、八欄 |
| `B05` | `FHS-5_PLP_PROJ-05_...md` | 67,845 | 557 | `794d91cc8080715886d5dc30b92e74b1f123fbe0aee47256bf1e84d749648dfe` | FAR；FAR-FR01–17、五態、十 Advice |
| `WM4` | `FHS-5_PLP_W4M_CODEX-NATIVE-FIRST_完整實質正文.md` | 72,962 | 1,042 | `f1df5835e44dc8a7aefe38246699bae77f7007f996d318fb6cc7f40fc37c4a22` | W4 接口；不作 W3 前置 |
| `CTRL` | `FHS-5_PLP_W3_GPT-WORK_最小執行控制包.md` | 24,047 | 158 | `SEE_05_SOURCES` | 本輪任務控制；`05` 實算 |
| `START` | `FHS-5_PLP_W3_GPT-WORK_啟動薄PROMPT.md` | 3,121 | 29 | `SEE_05_SOURCES` | 本輪啟動；`05` 實算 |

> `CTRL`／`START` 的 raw SHA 以 `05_W3_SOURCE_MANIFEST.json` 實算值為準；本表不重複填未經 `05` 計算的數字。`B00–B05` 的完整正文未逐句重讀；本包以 `PLAN` 附錄 B 的原義抽取與其 raw SHA/bytes/lines 對位，讀取層級如實記為 `REFERENCED_BY_PLAN_APPENDIX_A`，不冒稱全文人工覆核。

## 00.4 來源優先序與衝突規則

1. 真 Owner 採納與適用原域政策。
2. 六冊有效上位義務與 WM3 CODEX-NF-r2 受影條款。
3. `PLAN` 的編製設計（`W3-NF-PLAN-r1`）。
4. 當期 actual（證明實況，不改義務）。
5. 歷史 support（只作血緣，不作 CURRENT）。

衝突時保留兩個值、來源與最小 CR／HOLD；不以最新檔名、時間或「看起來較新」覆蓋真身份。`WM0-R3` 與 `WM0-R4` 並存：W0 actual 明確採納 r4；本包不把 r3 的 hash 改名成 r4。W2 product 與 delivery 分帳：`dada2354…` 是產品候選，`3346076c…` 是 delivery-only 前進；不得用 delivery commit 冒充產品新 verdict。

## 00.5 Effect 與寫入邊界

| 類別 | 本包狀態 | 說明 |
|---|---|---|
| `SOURCE_READ` | 可 | 只讀 `S` 與 `R` 的相關來源；不掃其他專案或帳密路徑 |
| `ISOLATED_DRAFT_WRITE` | 可 | 只寫 `O` 隔離主用根與 `02_EVIDENCE/raw` |
| `LOCAL_DOCUMENT_CHECK` / `BOUNDED_SMOKE` | 可 | stdlib Python、既有 reader／reviewer、隔離 fixture/smoke；不建第二套產品 harness |
| `W3_DEV` | 有界可 | 限 §00.2.3 的 W3 隔離根與 exact targets；每 batch 先 bind preimage/rollback |
| `W3_OPS` | 有界可 | 限可逆、無 secret、隔離 process；正式產品 Host/principal 未綁時記 `NOT_ADMITTED`，只停受影 |
| `W3_DOC_PUBLICATION` | 可 | 只推本輪 W3 六檔／assets／證據安全 export／指標；不混 W2 或 main 無關歷史 |
| `W2_PROTECTED_WRITE` | 不可 | writer `BLOCKED_NOT_ADMITTED`；需 Owner 在 W2 scope 新授權 |
| `USER` / `RELEASE` / 部署 | 不可 | 無 consent／Publisher；不部署、不 merge、不 Release |

---
# 01｜Goal／JTBD／FUO／Acceptance／Non-goals

## 01.1 JTBD

當一個候選已由 Maker 凍結，但 Owner 需要知道它是否值得繼續投入時，需要一個**可重播、可反證、可交接**的流程：在不能改 Oracle 的前提下找出真實反例，將根因、替代方案與下一步交回 Guide；而不是用「看起來通過」、固定樣本或無盡 HOLD 取代判斷。

## 01.2 Wave Goal

以真 Candidate、Oracle、Fixture、Case 與 Raw 固定受審點；由分立的 Challenger 重現至少一個 POS／NEG 或明確 NotCovered；FAR 在可回取原 Source／World 及 typed retrieval 基礎上提出根因與至少兩個實質可比較方案；再交 Guide 第二觸點產 `NextOperation / STOP / Resume` 候選。W3 的產品閉環還必須包含**另受權的 Native 修補／重測**與**分立的 Checker／Consumer 收據**。

## 01.3 六個 FUO（產品出口）

| FUO | 可觀察出口 | POS | NEG | WP |
|---|---|---|---|---|
| `W3-CODEX-01` Freeze | 五 pin `source/candidate/evidence/oracle/case_set` 各自可重算；fixture／frozen_at／host／policy 另列 | 真 bytes、同 scope、可重開 | 浮動 HEAD、舊 raw、改 oracle、同一 SHA 混域 | P01 |
| `W3-CODEX-02` Run | Generic 真 stdlib/repo runner；原域 runner 另接；argv／exit／stdout／stderr／world raw | 同案 POS/NEG 分開真跑 | 無 runner 宣 REPRODUCED、exit 0 當 PASS | P02 |
| `W3-CODEX-03` Finding | 八欄 Finding＋expected／observed／FirstFail／NotCovered；≥2 不同 failure class | 兩類真反例各自可重放 | summary、固定 template、數量代 raw | P03 |
| `W3-CODEX-04` FAR | RQ0–8、五態、EvidenceGraph、每決策 Finding ≥2 實質 Alternatives、十 Advice 原名 | HIT/ZERO/UNAVAILABLE/BLOCKED/ERROR 分列 | UNAVAILABLE 當 ZERO、單一方案、固定字串 | P04/P05 |
| `W3-CODEX-05` Guide2 | 原七鍵→Guide 九鍵 lossless、兩期真值、ThinResume、Next/Stop/Resume | 同 scope 真 Delta 或真 NoDelta | 缺期、caller bool、單 evidence_sha、跨 scope | P06 |
| `W3-CODEX-06` Native repair | 另受權 patch/retest、new candidate、pre/post/restore、distinct Checker/Consumer | 受影 ChangeCone 最小修補 | Challenge/FAR 寫 subject、撤權仍寫、Maker 自簽 | P06 |

## 01.4 Acceptance（作者側與產品側分開）

| ACC | 正向 | 反向 | 本輪狀態 |
|---|---|---|---|
| `W3-A01` Freeze | 五 pin 有來源、SHA、scope；candidate/evidence/oracle/case set 分開 | 浮動 HEAD、舊 candidate SHA、同一 SHA 混用 | `PACK_PIN_LOCKED`；產品 `UNBOUND` |
| `W3-A02` Runner | 原 Case/Oracle/Fixture/runner/ACL 的 invocation contract 可讀 | 無 Runner 宣 REPRODUCED | `RUNNER_UNBOUND` |
| `W3-A03` Finding | 八欄完整；expected/observed/FirstFail/reproduction | 只有摘要、無 raw | `DESIGN_TEMPLATE_ONLY`；產品 `NOT_RUN` |
| `W3-A04` FAR | 五態各自 request/response/branch；UNAVAILABLE≠ZERO | DB 缺當 ZERO | `DESIGN_ONLY` |
| `W3-A05` Advice | 10/10 原名可檢索；advice 不轉 Grant | 自造第 11 個有權 enum | `DESIGN_ONLY` |
| `W3-A06` Guide2 | Next/Stop/Resume payload；雙期條件 | 無 Delta 宣 PARK | `DESIGN_ONLY` |
| `W3-A07` Claim | 六維分帳；Checker 未簽 | 作者自簽 Independent | `DESIGN_ONLY` |

## 01.5 Done 與 Non-goals

**本輪（A0–A4）Done**：

1. 六檔實際物化、可解析、可消費；五 MD＋一 JSON 為 single truth；r1 完整保留並標 superseded。
2. 來源、上游 W0/W1/W2、W2 partial、原 33 FR、16 原案、六 WP、七 Seam、十 Advice、五態、七／九鍵、14 HOLD、R3-CR、F5-CR、原分母均有實際落點。
3. 16 案有 design fixture/oracle、expected、NotCovered、runner late-bind；observed 全 null、verdict 全 `NOT_RUN`。
4. V1/V2/V3 有真 receipts；BLOCKER/MAJOR 清零；product late-bind 分帳。
5. 外置 seal 綁 `05` raw SHA；`W3_OWNER_ADOPTION.json` 綁預授權來源與 validation；正文與證據附件分開；`W3_CURRENT.json` 指向唯一 active 新包。
6. 必要 GitHub W3 文件已 normal push，遠端 commit/tree/指針真讀回；或明確記 `PUSH_BLOCKED`。

**Non-goals（本輪）**：

1. 不重跑 W0/W1 全量、不修復 W2 writer、不正式執行 W3 16 原案、不施工 W4。
2. 不改寫上位六冊或 W3M；不部署、不發外部 Release。
3. 不新建平台、服務、Registry、Issuer、Queue、Scheduler 或持久調度器。
4. 不以作者 fixture／oracle 冒充原域 freeze；不以 local test 冒充原 Runner；不以 advisory 冒充 Checker；不以文件主用冒充 `W3_NF_VALIDATED`。

---
# 02｜Product SPEC：六 FUO、16 原案與原 33 FR

## 02.1 產品責任與工作包

| 產品責任 | 最小可驗收輸出 | 首個必需證據 | WP |
|---|---|---|---|
| 五 pin 同 scope、可重算 | `FreezeLedger` | 五份 preimage＋bytes＋SHA＋frozen_at | P01 |
| 原案 POS/NEG 真跑 | `CaseRunRecord[]` | argv／exit／stdout／stderr／world raw | P02 |
| 八欄 Finding＋NotCovered | `FindingSet` | 兩類不同 failure class 的 raw | P03 |
| FAR typed retrieval | `FARRetrievalGraph` | 每 Finding 的 RQ0–4、五態、denominator | P04 |
| 根因／替代／十 Advice | `DecisionAdvice` | 反證、NoFit、≥2 方案、owner | P05 |
| Guide2／Delta／修補 | `Guide2Handoff`＋`ChangeSet` | 兩期九鍵、pre/post/restore、distinct receipts | P06 |

## 02.2 16 原案（全部 `observed=null`、`verdict=NOT_RUN`）

原 ID、kind 與 trace 依 `PLAN` §09.1（L582–L597）與 WM3 §02.4／§09.2。fixture/oracle 的 design bytes 見 `03` 與 `05`。

| Case | Kind | WP | 主要 Req／trace | 預期出口（設計） | 狀態 |
|---|---|---|---|---|---|
| `W3-FRZ-01` | POS | P01 | W3-A01, CODEX-01, EC-FR01/02 | 五 pin 同 scope、5/5 可重算 | `NOT_RUN` |
| `W3-FRZ-02` | NEG | P01 | EC-FR02/13 | `FROZEN_IDENTITY_MISMATCH`、零調用 | `NOT_RUN` |
| `W3-RUN-01` | POS | P02–03 | W3-A02, EC-FR05/06/08 | POS 語義相符；NEG 正確拒絕 | `NOT_RUN` |
| `W3-RUN-02` | NEG | P02–03 | EC-FR06/07 | `UNREPRODUCED`／`RUNNER_UNBOUND`／`RAW_UNTRUSTED` | `NOT_RUN` |
| `W3-FAR-01` | NEG | P04 | FAR-FR07 | `UNAVAILABLE` rows=null；偽 zero 拒 | `NOT_RUN` |
| `W3-FAR-02` | POS | P05 | FAR-FR08..12 | ≥2 實質 Alternative、Fit/NoFit | `NOT_RUN` |
| `W3-G2-01` | NEG | P06 | U-034, FAR-FR14 | `DELTA_UNVERIFIED`、不 PARK | `NOT_RUN` |
| `W3-CHK-01` | NEG | P03/P06 | W3-A07, EC-FR12 | `FALSE_AUTHORITY`、Checker null | `NOT_RUN` |
| `W3-R3-01` | POS | P01/P03 | W3M-D06 | `NOT_COVERED`、保 identity | `NOT_RUN` |
| `W3-R3-02` | NEG | P06 | W3M-D06 | count-only → `DELTA_UNVERIFIED` | `NOT_RUN` |
| `W3-R3-03` | POS | P04 | W3M-D05 | 192/0 → 真 `ZERO_RELEVANT_HIT` | `NOT_RUN` |
| `W3-R3-04` | NEG | P03/P06 | W3M-D05 | 22/22 self-check → `FALSE_INDEPENDENT` | `NOT_RUN` |
| `W3-R3-05` | POS | P05 | W3M-D02 | ALT-A/ALT-B 兩實質方案 | `NOT_RUN` |
| `W3-R3-06` | NEG | P01/P04 | W3M-D07 | ACL 13/13 ≠ Original ACK | `NOT_RUN` |
| `W3-FR16-01` | NEG | P03 | EC-FR16 | `WRITE_SCOPE_VIOLATION`、零 mutation | `NOT_RUN` |
| `W3-FR17-01` | NEG | P03/P06 | FAR-FR17 | `FALSE_AUTHORITY`／`FALSE_RELEASE` | `NOT_RUN` |

## 02.3 External Challenge 原 16 FR

以下 16 列保留 B04 原義與 PLAN 附錄 B.1（`PLAN:L873–L888`）的 source span；`Parent` 為原 FR，`Child` 為本包的最小可反證切片。`Exception` 與 `NEG` 不省略；`State` 只表示本包作者側。

| ID | Parent→Child | SourceRef | POS | NEG／Exception | WP | Owner／Consumer | State／FirstFail |
|---|---|---|---|---|---|---|---|
| `EC-FR01` | Source/Scope→CH-EC01 | `PLAN:L873` | 原 PLP bytes、manifest、project/subject/scope 可回取；SourceIdentityView | 同名異 SHA、scope 漂移、clause 不可回取 | P01 | Source Owner／TPM | `DESIGN_ONLY`；`SOURCE_INTEGRITY_FAILED` |
| `EC-FR02` | Candidate Freeze→CH-EC02 | `PLAN:L874` | 五 pin＋HEAD/Host/Epoch 凍結；FrozenCandidateView | 浮動 HEAD、舊 candidate、`CANDIDATE_CHANGED` | P01 | Maker／Challenger | `DESIGN_ONLY`；`FROZEN_IDENTITY_MISMATCH` |
| `EC-FR03` | Claims→CH-EC03 | `PLAN:L875` | 每 claim 拆最小可反證單位；未知不補造 | 無 Child／NEG 的 claim、未知當已證 | P01/P03 | PI Reader／Challenger | `DESIGN_ONLY`；`CLAIM_UNBOUND` |
| `EC-FR04` | Claim↔Contract→CH-EC04 | `PLAN:L876` | claim 與 clause/case/oracle/expected/consumer 雙向 join | unresolved ref 當已綁、只列標題 | P01/P03 | Case Owner／Challenger | `DESIGN_ONLY`；`TRACE_UNBOUND` |
| `EC-FR05` | Runner probe→CH-EC05 | `PLAN:L877` | runner identity/policy/effect/admission 可讀；RunnerCapabilityView | 無 runner、自己 shell 跑、`RUNNER_UNBOUND` | P02 | Runner Owner／P03 | `RUNNER_UNBOUND`；`RUNNER_UNBOUND` |
| `EC-FR06` | POS→CH-EC06 | `PLAN:L878` | 同 frozen candidate POS/fixture/oracle 真跑 | 無 raw 宣 REPRODUCED、改 oracle | P02/P03 | Runner／FAR | `NOT_RUN`；`UNREPRODUCED` |
| `EC-FR07` | NEG/EDGE/SEC→CH-EC07 | `PLAN:L879` | 負例單獨觀測；拒絕與 Case PASS 分開 | 以拒收抵 POS、改 threshold | P02/P03 | Case Owner／FAR | `NOT_RUN`；`NEG_NOT_OBSERVED` |
| `EC-FR08` | Evidence Integrity→CH-EC08 | `PLAN:L880` | command/exit/stdout/stderr/raw SHA/receipt | 文字宣稱、無 raw、`RAW_UNTRUSTED` | P03 | EvidenceReader／Checker | `DESIGN_ONLY`；`RAW_UNTRUSTED` |
| `EC-FR09` | World/Host→CH-EC09 | `PLAN:L881` | 同 scope Repo/Host/WorldRaw/PolicyEpoch/Effect | UNKNOWN 當 READ、Host 混帳 | P03 | WorldReader／Checker | `UNBOUND`；`WORLD_UNBOUND` |
| `EC-FR10` | Findings→CH-EC10 | `PLAN:L882` | 八欄＋FirstFail＋counterexample locator | 只有摘要、固定 ID、無 raw | P03/P04 | Challenger／FAR | `DESIGN_ONLY`；`EVIDENCE_LAUNDERING` |
| `EC-FR11` | NotCovered→CH-EC11 | `PLAN:L883` | 逐案 reason/owner/resume/firstfail | 空白、N/A、當 0 成功 | P03/P04 | Case/Runner Owner | `DESIGN_ONLY`；`NOT_COVERED_LOSS` |
| `EC-FR12` | Advisory Verdict→CH-EC12 | `PLAN:L884` | 只五值 advisory；`original_checker_verdict=null` | `PASS_CHALLENGE`、自簽 Checker | P03/P06 | Challenger／Checker | `DESIGN_ONLY`；`FALSE_AUTHORITY` |
| `EC-FR13` | Rechallenge→CH-EC13 | `PLAN:L885` | 新 candidate/raw/source/oracle 差額；只跑 ChangeCone | 同差額空跑、舊 raw 重用 | P01/P03 | Maker／Case Owner | `DESIGN_ONLY`；`ORACLE_DRIFT` |
| `EC-FR14` | FAR Handoff→CH-EC14 | `PLAN:L886` | 凍結報告、FirstFail、raw、NotCovered 同 scope 交 FAR | 只交 hash、跨 scope | P03/P06 | FAR／Guide | `DESIGN_ONLY`；`HANDOFF_LOSS` |
| `EC-FR15` | Generic Profile→CH-EC15 | `PLAN:L887` | 非 FHS 合法 PLP/phase/effect/case applicability | 強裝 HGK/22WP/485 | P01/P03 | Project Owner／Case Owner | `DESIGN_ONLY`；`PROFILE_GATE_DRIFT` |
| `EC-FR16` | Security/SoD→CH-EC16 | `PLAN:L888` | 受權 read/output roots；subject/oracle/test/threshold write set=[] | 寫原 test/threshold、secret 外送 | P03/P06 | Host/Checker | `DESIGN_ONLY`；`WRITE_SCOPE_VIOLATION` |

## 02.4 FAR 原 17 FR

以下 17 列保留 B05 原義與 PLAN 附錄 B.2（`PLAN:L896–L912`）。`Profile` 欄標示 Generic 或原 Profile 專屬，避免把 Fabric 三源當通用必要。

| ID | Parent→Child | SourceRef | POS | NEG／Exception | WP | Profile／Owner | State／FirstFail |
|---|---|---|---|---|---|---|---|
| `FAR-FR01` | Identity→CH-FAR01 | `PLAN:L896` | Project/subject/scope/source manifest 同小包 join | 檔名猜身份、同名異 SHA | P01/P04 | Generic／Source Owner | `DESIGN_ONLY`；`SOURCE_INTEGRITY_FAILED` |
| `FAR-FR02` | Challenge input→CH-FAR02 | `PLAN:L897` | 每 Finding/command/exit/raw/NotCovered 可 parse | 未重現給成功建議 | P03/P04 | Generic／Challenger | `DESIGN_ONLY`；`RESEARCH_REQUIRED` |
| `FAR-FR03` | Execution observation→CH-FAR03 | `PLAN:L898` | Repo/Host/WorldRaw/FirstFail/LastGood 原 Reader 核 | 只信 caller | P04 | Generic／WorldReader | `UNBOUND`；`OBSERVATION_UNBOUND` |
| `FAR-FR04` | Trace edges→CH-FAR04 | `PLAN:L899` | Finding→clause/case/effect/consumer 有向邊 | 無 reader_state 的邊 | P04 | Generic／PI-PD Reader | `DESIGN_ONLY`；`TRACE_UNBOUND` |
| `FAR-FR05` | Decision question→CH-FAR05 | `PLAN:L900` | 一個具體 decision question＋一個當期 FirstFail | 多個無關失敗混在一起 | P04/P05 | Generic／Research Owner | `DESIGN_ONLY`；`QUESTION_UNBOUND` |
| `FAR-FR06` | Router eligibility→CH-FAR06 | `PLAN:L901` | 原 RouterDecisionRef/WorkOrder 只在原 Profile | 自造 Router、Generic 強制 | P04 | Fabric Profile／Router Owner | `PROFILE_ONLY`；`ORIGINAL_NATIVE_UNBOUND` |
| `FAR-FR07` | Source denominator→CH-FAR07 | `PLAN:L902` | 每源 query/snapshot/origin/disposition/raw；reachable≠0hit | 不可達當零 | P04 | Generic／Retrieval Owner | `DESIGN_ONLY`；`RESEARCH_REQUIRED` |
| `FAR-FR08` | Hypothesis→CH-FAR08 | `PLAN:L903` | 支持、矛盾、反證、Hypothesis 分列 | 衝突裁成偏好答案 | P05 | Generic／Research Owner | `DESIGN_ONLY`；`ABSTAIN` |
| `FAR-FR09` | Search-Before-Build→CH-FAR09 | `PLAN:L904` | code/bind/activate/test 以真 caller/branch/PR/Host 證 | 空 worktree 證不存在 | P04/P05 | Generic／Developer-Host | `DESIGN_ONLY`；`REUSE_NOT_CHECKED` |
| `FAR-FR10` | Root cause→CH-FAR10 | `PLAN:L905` | 受信 root cause raw＋affected ChangeCone | caller claim 當根因 | P05 | Generic／Owner | `DESIGN_ONLY`；`ROOT_CAUSE_UNBOUND` |
| `FAR-FR11` | Alternatives→CH-FAR11 | `PLAN:L906` | 修／延／結／停候選，Fit/NoFit/風險/成本/Next/Resume | 三個空字串、單一方案 | P05 | Generic／Program | `DESIGN_ONLY`；`ALTERNATIVE_INSUFFICIENT` |
| `FAR-FR12` | Ten Advice→CH-FAR12 | `PLAN:L907` | 十原名受證據約束；缺 raw 不 FIX/CLOSE/PARK | 第 11 有權 enum | P05 | Generic／Guide | `DESIGN_ONLY`；`ADVICE_OVERCLAIM` |
| `FAR-FR13` | Guide Touch2→CH-FAR13 | `PLAN:L908` | 同 scope advice/owner/next/expected/resume；非 Grant | Advice=Grant、擴 scope | P06 | Generic／Guide | `DESIGN_ONLY`；`FALSE_AUTHORITY` |
| `FAR-FR14` | Material Delta→CH-FAR14 | `PLAN:L909` | 兩期不同真 Reader receipt；七鍵逐欄比 | 缺期 PARK、單 evidence_sha | P06 | Generic／WorldReader | `DELTA_UNVERIFIED`；`DELTA_UNVERIFIED` |
| `FAR-FR15` | Native WO three sources→CH-FAR15 | `PLAN:L910` | 原 WO/Router/三源 refs 交原 reducer | UNAPPLIED 當已收 | P04 | Fabric Profile／Fabric Owner | `PROFILE_ONLY`；`TRISOURCE_UNBOUND` |
| `FAR-FR16` | Non-FHS profile→CH-FAR16 | `PLAN:L911` | 非 FHS 專案合法 READ；按該案 Owner | 硬寫 HGK/485/W0 前件 | P04 | NonFHS Profile／Project Owner | `DESIGN_ONLY`；`PROFILE_GATE_DRIFT` |
| `FAR-FR17` | Authority/safety→CH-FAR17 | `PLAN:L912` | Effect/Principal/ACL/Checker/Publisher 分帳；FAR 不 mutation | FAR 發 WO/Grant/Release | P05/P06 | Generic／Issuer-Checker | `DESIGN_ONLY`；`FALSE_AUTHORITY` |

## 02.5 Guide／Bridge／TPM 的適用義務

| 來源 | 原義務 | W3 當期消費 | 不主張 |
|---|---|---|---|
| B02 Guide `U-034`／`CG-R2-REQ-09` | FAR Advice→Touch2、MaterialDelta、雙觸點 | P06 的 `Guide2Handoff`／`GuideThinResume`；兩期九鍵 | 不重跑原 Guide 17 案；不把單 `evidence_sha` 當 delta |
| B02 Guide 九鍵 | subject/scope/source/repo/host/policy/oracle/world/first_fail | P06 七鍵→九鍵 lossless crosswalk；source-set 與 pack digest 明示映射 | 不把 `pack_manifest_sha256` 直接當 `source_set` |
| B03 Bridge 四 API | inspect/explain/render/compare；BodyResolver；path/unknown | 可選 SM05；direct 路徑可繞過 Bridge | 不以 Bridge OFF 抵五方產品驗收 |
| B01 TPM F01–14／U01–16／QA26 | 四契約、Reviewer 唯讀、八欄 Finding、FirstFail/ChangeCone | 00/01/02/03 作 TPM 輸入；Reviewer 逐欄覆核 | QA26 未跑不計 PASS |

## 02.6 兩個動態 Finding 的最低要求

W3 不得用固定兩個樣本冒充通用能力。最小動態切片必須：

1. 由 Case Owner 在看到 observed 之前凍結 expected／fixture／case-set。
2. 由分立 Challenger 在隔離 process/worktree 重放，保留 red argv／exit／raw。
3. 至少兩個**不同 failure class**：例如 A 類「安全／准入分類」、B 類「功能／資料消費分類」。
4. 每個 Finding 有八欄、expected/observed/FirstFail、case/child/requirement/oracle trace。
5. 若原來源已無真 defect，可在隔離 fixture 構造受控 mutation，明確標 `TEST_MUTANT_FINDING`；不得假造「W2 發現新缺陷」。

---

# 03｜Architecture SPEC

## 03.1 NF01–NF10 在本包的落點

| ADR | 本包規則 | 反證 |
|---|---|---|
| `NF01` | CODEX Native 是唯一主工程調度／恢復；五方可獨立或按需組合；不建第二 Runtime/Queue/Dispatcher/Issuer | 另建調度器、以裸 executor 冒充五方 PASS |
| `NF02` | Generic 冷啟不預設 HGK/FABRIC/SBL/FHS/PIPD/HERMES；Legacy 明示 Profile | 無舊 provider 仍可 Native；只切 env flag 不算 OFF |
| `NF03` | 真 file/Git/process/tester/oracle/consumer 承接原 Reader/Registry/Runner/ACK 責任 | 無 OriginalReader 仍可讀；假 ref/ACK 拒 |
| `NF04` | HardEdge 需原需求／安全／當期技術必要、具名 producer、可取得路徑；後驗不倒卡前件 | post 卡 pre、W4 Release 卡 W3、cycle 拒 |
| `NF05` | 設計與授權、OS/Repo/Host ACL 分離；READ/DRAFT/DEV/OPS/USER/RELEASE 分帳 | 未知 effect 不默認 READ；無 grant 不試跑 |
| `NF06` | 七 Seam 是資料交換，不是七道 Gate；合法 direct 可 bypass | bypass 不抵五方產品驗收 |
| `NF07` | W0 先證、W1/W2 delta、逐波 late-bind | W0 44 receipts 不抵 W3 16 原案；W4 planned 不冒 actual |
| `NF08` | 六檔 single truth；十五檔只作版本隔離 projection | 自循環 SHA、雙 canonical 拒 |
| `NF09` | 原 ID/Case/Receipt/分母保存；按 profile/host/candidate/observation 分帳 | local47、44 receipts、32 checks 不抵 C16/36/20/30 |
| `NF10` | FirstFail→ChangeCone→最小修補→受影重驗；保 LastGood | 同 key 無材料不重派；缺雙期不 PARK |

## 03.2 架構與資料流

```text
Source/Git/CaseOwner ── SM01 ── TPM + read-only Reviewer
       PI ── SM02 ── PD/Program ── SM03 ── DEV/OPS ECP + TQAEP
                         │
        6-file package ── SM04 ── Guide ThinStart (optional)
                         ├── SM05 ── Bridge read-only context (optional)
                         └── direct verified file/Git read ── CODEX Native
                                   │
                        real command / pre-post / raw
                                   │ SM06
                      Frozen Challenge ── Findings + NotCovered ── FAR
                                   │                         RQ0..8
                                   └─────────────────────────────┤
                                                SM07 Guide Touch2 / direct advice
                                                             │
               (separate role + admitted ECP) CODEX Maker patch/retest
                                                             │
                             new candidate -> re-freeze -> Challenge/Checker
                                                             │
                                       clean Consumer -> W3 closeout -> W4
```

資料交換為有界函式／CLI／文件；不另設守護進程、資料庫、Registry、Issuer、Scheduler、中央 WorkOrder server。任何 sidecar 不得代理寫入 subject、case、oracle、threshold、原 Grant。Checker 不得從 Maker 任意可寫路徑載入 verifier。

## 03.3 七 Seam 欄級交接

| Seam | Producer → Consumer | 實質材料 | 負例／必要觀察 |
|---|---|---|---|
| `SM01` | Source → TPM/Reviewer | raw SHA/version/span、Req/Parent/Child/NEG/Exception、來源權利 | 假 ID、缺 Child B、同名異 SHA；readback 實質條款 |
| `SM02` | PI → PD/Program | PI rev/FUO/ACC/capability/typed DAG、適用性、unknown | 無原據 mandatory、cycle/phase overreach |
| `SM03` | PD → ECP/TQAEP | op/root/exact write set/preimage、fixture/oracle/runner、expected/post/recovery | post 不當 pre；ECP not grant |
| `SM04` | Pack → Guide | identity/05 digest、goal/FUO/done/scope/effect/next、actual source bodies | PACKAGE_FIRST 六檔直讀；缺 Bridge 不阻；假 pack 拒 |
| `SM05` | Guide/Bridge 或 direct → Native | BodyResolver 真 clause/Case/locator、context digest/missing/unknown、scope constraints | 四 API 讀回；無 context consumed 不給 chain PASS |
| `SM06` | Native → Challenge → FAR | 五 pin＋actual argv/exit/raw/pre-post＋八欄 Finding/NotCovered/claim | 一對一 same candidate/scope；NoRaw 不重現；不自簽 |
| `SM07` | FAR/delta → Guide/Consumer | typed advice＋alternatives＋七／九鍵＋next/stop/resume＋actual readback | no delta 不派；FAR 不授權；distinct Checker/Consumer |

## 03.4 Search-Before-Build：現存能力與處置

| 現有能力／定位 | 鑑定 | 本包處置 | 不可做 |
|---|---|---|---|
| W0 `13_W0_NF_CODEX_20261125/tools/challenge.py` | 真 32-check 代表模式；固定 pack/oracle/summary | `REUSE_PATTERN`；抽 hash/subprocess/fail-closed，不直接當動態 W3 產品 | 固定 sample 冒全產品 |
| W0 `tools/far_run.py` | DEV_RED/CHALLENGE_PREPATCH 分流；固定 finding/輸出 | `REFERENCE + BUILD_MINIMAL`；以 request+FindingSet 參數化 | 固定模板冒任意 Finding |
| W0 `tools/guide.py` | `touch2(prev,new_evidence_sha)` 單欄 | `REFERENCE_ONLY`；不作 no-delta 判準 | 單欄冒完整 delta |
| W1 `W1/impl/guide_nf.py` | NINE_KEYS、`reconcile_guide_delta` 拒 caller bool、`compare_material`；`_p_source_sha` 讀 pack manifest | `REUSE_FIRST`；驗 source_set≠pack digest crosswalk、兩期真 verifier、FAR handoff | 不重建 Guide |
| W1 `W1/impl/nf_reader.py` | `inspect_package`／`inspect_generic`；schema/manifest/seal 檢查；部分 W1 特化 | `REUSE/REPAIR`；走 generic/W3 contract，不套 W1 asset_count | 套固定 26 |
| W1 `W1/impl/bridge_nf.py` | 四 API、generic 分支、context digest、field fidelity | `REUSE/REPAIR`；驗 W3 dynamic Req/Child/Case 與真 context consume | 只傳 hash |
| W1 `W1/impl/tpm_contracts_nf.py` | profile-driven Generic；仍有 W1 CASE_ROW_RE | `REUSE/REPAIR`；必須驗 W3 16 Case parser/discovery | 因 W1 pattern 漏 W3 row |
| W2 `W1/check/w2_receiver.py`／`w2_nf_reader.py` | 真 W2 接收基線，含已知缺口 | `REUSE_READONLY`；W3 intake 按 W2_CURRENT/五 pin/原 receipts | 擴 schema 未受權 |
| W2 `w2_admission.py`＋`w2_dev_gate.py` | event marker、exact target、canonical root、preimage、recovery；gate pin | `REUSE_AFTER_ADMISSION`；不解除 writer、不移 pin、不換 authority | 模擬 permit |
| pytest/unittest/Repo CLI/Git | 既有原生 tester；W0 已實證 stdlib | `REUSE`；binary pin、argv、timeout、expected exit/raw | 建第二 Runner 平台 |
| Fabric HGK Memory/Knowledge/External Web | 原 patch `UNAPPLIED`、Router/ResearchWO 未取得 | `PROFILE_ONLY`；Generic 用真 source/repo/允許外部查詢 | 偽造三源狀態 |
| `plp-tpm-review 1.0.1` | W0 真 invocation；10 authority/reader UNBOUND | `REUSE_IF_FIT`；先讀 manifest/entrypoint/loaded/invoked/served | 本地能力等同三 Host |

**候選檔案落點（不是已准入 WriteSet）**：優先核現 repo 的 `W1/impl`、`W1/check` 共享能力。若真缺 W3 動態實作且 Owner 同意，可在現有 repo 另開受界 `W3/impl/`（`challenge_nf.py`、`far_nf.py`、必要 intake/consumer）、`W3/check/`（逐案 runner/測試）、`W3/spec/`（真 frozen assets）等最小 slice；Guide/Bridge/TPM 原 shared 模組只做有證據的 compatibility 修補。施工前由 `git ls-files`／搜尋確認存在性，明列每個 ADD/MODIFY/DELETE、父目錄與 preimage，寫入 `01` ECP；不可把 glob 當 grant。

## 03.5 六檔 single truth 與舊接口

| 檔 | 唯一職責 | 主要 consumer | 拒收 |
|---|---|---|---|
| `00_W3_PI_PD.md` | 身份、Goal/FUO/Done、三 SPEC、Req/Child/NEG、WP/DAG、W2 接收、Effect/角色、Stop/Claim、W4 handoff | TPM/Reviewer/Guide/Native/Checker | 空殼、只列標題、假 readiness |
| `01_W3_DEV_ECP.md` | repo/root/HEAD/dirty/preimage、逐檔 write-set、命令/expected post/tests、recovery/UNKNOWN | Maker/Repo Owner | 全 repo glob、無 preimage、ECP 當 Grant |
| `02_W3_OPS_ECP.md` | Host/principal/policy/receiver、output root、argv/timeout/readback/compensation | Executor/Host Owner | `git revert` 當 OPS recovery |
| `03_W3_TQAEP.md` | Case/Req/Child、fixture/oracle/runner、POS/NEG/EDGE/SEC、expected/observed/raw/checker/NotCovered | Case Owner/Checker | summary 代 raw、observed 寫進 expected |
| `04_W3_START_THIN_PROMPT.md` | GOAL/SOURCE/SPEC/EXECUTE/HARNESS LOOP/DONE；授權/stop/next | Guide/Native | 擴 scope、重抄正文 |
| `05_W3_SOURCE_MANIFEST.json` | identity、source SHA/bytes/span、五 MD/資產 digest、上游 handoff pins、self-excluded | Source Curator/Pack Author | 自循環、假 hash、Git blob 當 raw |

舊十五檔只在真舊 consumer 需要時，由同一真源 deterministic 投影；`projection_of_sha256` 指向 `03` raw；不得成為第二 canonical，不得讓舊 guard 反向要求十五檔。無真 consumer 不生成。

---

# 04｜Program SPEC：工作包、DAG、P01 再資格化

## 04.1 兩條互不冒充的工作線

- **作者線 A**：A0 來源凍結／權威判別 → A1 PI/PD/WP/Case 映射 → A2 六檔及 assets → A3 獨立作者覆核與最小修補 → A4 外置 seal／LastGood／Owner 採納（文件層）→ V1–V3 → publication。本輪做到 A4。
- **產品線 E**：P01 接收 W2 delta／Freeze → P02 Runner → P03 Findings → P04 typed research → P05 RCA／alternatives → P06 Guide2／Native repair／retest／Consumer。P04 可在 P03 個別 Finding 成立時開始；不能以未完成 Finding 宣 HIT。
- **跨線相交**：A4 文件採納 → fresh clean receive → scope ready；P01 上游 readback＋每 batch 真准入，才是正式產品效果前件。A0 可用 W2 partial 作來源，不等待 W2 授權；P01 讀取／freeze 需合法 roots 與真 bytes，但不必先取得 protected writer grant 才能讀。**採納不得倒等 fresh receive，fresh receive 也不得倒等產品 PASS**；三者是證據鏈，不是同一 op 的 cycle。

## 04.2 六個工作包

| WP | Input → Operation → Output | Consumer | POS／NEG | Stop |
|---|---|---|---|---|
| `WM3-P01` Freeze | 00/05、W2_CURRENT/25_/24_、W0/W1 upstream、W3 case refs → 驗 schema/identity/bytes/hash/span；五 pin 分凍；W2 R0–R7 | P02/P03、FAR、Checker | 五 pin 可重開；浮動/舊/錯 scope 拒 | `FROZEN_IDENTITY_MISMATCH`／`W3_EVIDENCE`／`W2_ORACLE_UNFROZEN` |
| `WM3-P02` Runner | P01 slice、Case Owner oracle/fixture、roots、runner/Host/ECP → invocation contract、freeze expected、隔離執行、capture raw | P03、W4 | 同案 POS/NEG 真跑；無 runner/raw 拒 | `RUNNER_UNBOUND`／`RAW_UNTRUSTED` |
| `WM3-P03` Challenge | frozen candidate＋cases＋runner＋raw → expected/observed/FirstFail、八欄、NotCovered | FAR、Checker | 兩類 failure class；無 raw/自簽拒 | `EVIDENCE_LAUNDERING`／`FALSE_INDEPENDENT` |
| `WM3-P04` FAR | FindingSet、source refs、repo/Host、decision question、原 Profile WO → RQ0–4、五態、graph | P05、Guide | 真 HIT/ZERO/UNAVAILABLE/BLOCKED/ERROR；偽 zero 拒 | `W3_FAR_SOURCE` |
| `WM3-P05` RCA | graph＋矛盾＋firstfail → RQ5–6、hypothesis/counterevidence/NoFit、≥2 alternatives、十 Advice | Guide2、Owner | 每 Finding 兩實質方案；固定字串/單方案拒 | `RESEARCH_REQUIRED`／`ABSTAIN` |
| `WM3-P06` Guide2/repair | same-scope handoff、兩期 receipts、七／九鍵 → RQ7–8、ThinResume、受權 patch/retest、closeout | Guide/Consumer、W4 | 真 Delta/NoDelta/Unknown；缺期/撤權寫入拒 | `DELTA_UNVERIFIED`／`FALSE_AUTHORITY`／`WRITE_SCOPE_VIOLATION` |

## 04.3 Typed DAG

| From | To | Edge type | Producer → Consumer | Why | Resume |
|---|---|---|---|---|---|
| P01 | P02 | `HARD_SOURCE_VERIFIED` | FreezeLedger → RunnerBindingCandidate | P02 需五 pin | 同 candidate/scope 真 pins |
| P02 | P03 | `HARD_SOURCE_VERIFIED` | CaseRunRecord[] → FindingSet | P03 比 expected/observed | 真 argv/exit/raw |
| P03 | P04 | `HARD_SOURCE_VERIFIED` | FindingSet → FARRetrievalGraph | FAR 從真 Finding 起 | 至少一個完成 Finding |
| P03 | P04 | `SOFT_CONTEXT` | partial Finding → typed retrieval | RQ0–4 可按完成 Finding 先行 | 未完成 Finding 不得當 HIT |
| P04 | P05 | `HARD_SOURCE_VERIFIED` | FARRetrievalGraph → HypothesisLedger | RCA 需 graph/反證 | 有 reader_state 的邊 |
| P05 | P06 | `HARD_SOURCE_VERIFIED` | DecisionAdvice → Guide2Handoff | Guide2 消費 advice/owner/next | 同 subject/scope advice |
| P06 | P01.next | `REVISION_LOOP` | new candidate → new FreezeLedger | 修補後另凍結，不是同一 op 的回退閘 | 新 candidate/evidence |
| P01.next | P02.next | `HARD_SOURCE_VERIFIED` | new FreezeLedger → affected retest | 只重跑受影 ChangeCone | 新五 pin |
| P06 | W4 | `DEFERRED_PROFILE` | W3_HANDOFF → W4 late-bind | W4 只在真 W3 交付後綁定 | W3 actual＋W4M 採納 |

**DAG 規則**：P06→P01.next 是 revision loop，不是同一 op 的 cycle；不得把 final Checker 倒作 P02 前件；不得把 W4 Release 倒卡 W3。任一 `HARD_SOURCE_VERIFIED` 邊缺 producer，不得留白或降級為 `INFO_ONLY` 後宣通。

**准入次序**：`pack adoption (§06)` → `fresh clean receive` → `scope W3_EXECUTION_READY` → `P01..P06`。adoption 只綁文件 05／seal，不要求 W2 產品 PASS；fresh receive 只證明消費者可讀，不改 W2 verdict；產品 readiness 只在 W2 真 requalification 後成立。此三事件各有獨立 receipt，不得互相冒充或形成循環前件。

## 04.4 P01 的 W2 R0–R7 再資格化

| Step | 操作與責任 | 真輸出 | Stop／Resume |
|---|---|---|---|
| `R0` | Source Curator 讀固定 `3346076` 的 `W2_CURRENT`／`25_`／`24_`；核 branch drift、compare、五 member；乾淨 checkout | IntakeIdentityLedger：product/delivery commit、files+sha、lastgood、superseded、source ACL | branch 前進只取新 diff；產品成員改變 → `CANDIDATE_CHANGED` |
| `R1` | P01 READ：核 W2 pack 6+25 assets、採納 decision/manifest、planned TQAEP 與 r3 ledger 逐案 trace；確認 12 Case oracle/fixture/raw locator/期別 | W2RequalificationMatrix（12 rows） | 真源缺或 token/semantic mismatch → Case Owner；先保存歷史 expected/observed |
| `R2` | Case Owner 在 W2 scope 按原需求凍結 12 Case 原義、fixtures/oracles/case set 真 bytes；Writer 不需為合法 READ 解封 | oracle/fixture/case-set digest、freeze_at、algorithm、Case Owner receipt | 找不到原義 → `W2_ORACLE_UNFROZEN`；只停受影案 |
| `R3` | Evidence Curator 逐 raw 封存：stdout/stderr/world/argv/exit/runner/ACL、pre/post/recovery、S1/J1/J2/J3；保歷史與本次分期 | raw index＋manifest＋external seal；fresh checkout byte equality | `W2_EVIDENCE_SEAL_PARTIAL`；不得補造 stdout/exit |
| `R4` | 若需 writer：Human Owner 給 **W2** 新具名授權；保留原 revoked decision/marker；只有原授權責任者按新決策啟用新 scope | 新 decision/roots/targets/ops/expiry/recovery＋真 OS/Repo/Host principal；security review | 缺 grant → `W2_WRITER_BLOCKED`；不動 gate/marker |
| `R5` | W2 原 Maker/Case Runner 對當期候選按原 fixture/oracle 重驗 J1/J3、受影原案、S1Δ；真缺陷才另受權 patch | J1 strict/consumer 真 material；J2 pre/post 分離；J3 兩語義成功、15 typed keys、OFF trace | 任何新 Finding 觸發撤權即停，保 LastGood |
| `R6` | 分立 Checker 對同 candidate/oracle/case-set/evidence、Host/scope 真獨立覆核（不是 r3/舊 21/21） | distinct Checker receipt、verification strength、remaining NC | `W2_INDEPENDENT_PASS` 未得不升格 |
| `R7` | W2 Owner 按完整契約判定 `W2_NF_VALIDATED`（非 W3 自簽），產 final closeout/handoff/pointer；W3 在採納的 W3M/pack 上 fresh clean receiver parse/use/readback | W3 receive receipt（當期候選＋W3 pack digest＋W2 upstream pins） | 缺 actual/current receive → `NOT_CLAIMED`；可續 W3 隔離樣本設計 |

**W2 現況（本輪唯讀核）**：product commit `dada2354b7c25c8f4a316d9fae93827cef0d194e`；delivery commit `3346076c69b00d65e48fdb9ddf894ac4cc09524b`；`W2_CURRENT.json` 指 `25_`／`24_` five pins；`W2_CURRENT` raw SHA `1532901743f1bdc352ca4c9de2fd66896ee6ef1e5fc606eca7ce3cc9616eedfe`（local raw；repo blob 為 `54244c4d…`，兩者不混）；five pins raw `74321487db0f6a1cf02b0eea8b91be0773308cdffc5ab6f7abfa8e16553ddd8f`；W2 pack `05` raw `81daac8ff3f47566d18cc7ebdaee9625ff5ca000b71caac3226841b124f6099b`。狀態 `PARTIAL`；writer `BLOCKED_NOT_ADMITTED`。

**W2 五 pin 接收規格**：

| Pin | 當期已讀值／狀態 | P01 required action |
|---|---|---|
| source | source_set `921de70ca5f273d9bba0ed0d022bb7595e8824d7595e8373b2c43d5ccbbaa044`；pack 05 `81daac8f…` | 真六檔、25 assets、source spans；區分 source_set、05 raw、W3 source_set |
| candidate | 五 member aggregate `8b4b4068313ae4d3ab066d6951add31d225d360ac053771d7d611621101ed8d7`；`verified product set` 但未產品升格 | 原算法/排序/bytes 重建；commit SHA 不是 aggregate |
| oracle | `PARTIALLY_FROZEN`；12 原案只 carried | 真 fixture/oracle bytes，逐案凍結，固定時間/Case Owner |
| case_set | `CARRIED_NOT_REFROZEN`，12 ID | 逐案原義/child/NEG/fixture/runner trace；W2 12 與 W3 16 不混 |
| evidence | `SEALED_AFTER_OBSERVED`，manifest 層 | 每個 raw stdout/stderr/world/receipt 可解析、bytes+SHA、期別、外置 seal |

五 member（G03 所記 raw SHA-256；**待當期 runtime 真 bytes 重算**）：

| path | SHA-256 |
|---|---|
| `W1/check/w2_receiver.py` | `768d6318861215886860ae3a30c9c30bdaec8bdd4732c63ff95996e675522a59` |
| `W1/check/w2_dev_gate.py` | `ecef3f39cf3ae4db1a387cca4eec2d5212d9cce8e1f81d7a91e0cb0ffd170db4` |
| `W1/check/w2_admission.py` | `8caabfffd5c5c07040f0444e1d4ad23cbad939501b61597b726184f4816c4ae3` |
| `W1/impl/w2_nf_reader.py` | `738bfe15ce3220d523a7306f98817dd9f5bc569f87fce107231c34e0e626d980` |
| `W1/check/test_j1_strict.py` | `2967464025d650bc6a82a23019e0b5427b98f16a08acaf957c57b8b8aac17dd4` |

12 原案不可刪：`W2-DEV-01/02`、`W2-OPS-01/02`、`W2-EFFECT-01`、`W2-AUTH-01`、`W2-RUNNER-01`、`W2-DELTA-01`、`W2-R3-01..04`。G03 中部分 oracle locator 為相對 run root，須原 Curator 補真 locator，不自行拼接成已存在路徑。

## 04.5 合法並行與限制

- P04 的 typed retrieval 可在 P03 部分完成時並行，但不得把未完成 Finding 當 HIT。
- P05 不得在 P04 前宣 root cause；P06 不得在 P05 前宣 Delta。
- R2/R3 可在不同 read-only source/copy 下並行準備；R3 seal 須 R2 凍結後的同位資料。
- R5 需要的 protected effects 先 R4；不得以 R6 Checker final 倒卡 R4 入場。
- `merge main` 不在 DAG，除非 Owner 另明示決策。

---

# 05｜Effect／角色／ABI 與失真控制

## 05.1 Effect 分帳

| Effect | 真正權限來源 | 本輪狀態 | 必要證據 | 停止條件 |
|---|---|---|---|---|
| `SOURCE_READ` | 檔案/來源 Owner 的讀權與 ACL | 文件來源已讀；產品來源未綁 | source SHA、span、root、reader identity | path escape、SHA 不符、未授權 |
| `ISOLATED_DRAFT_WRITE` | 使用者/工作區寫權 | 只寫 O 作者根 | before/after SHA、隔離根 | 越界、覆寫來源、symlink/reparse |
| `DEV` | §00.2.3 standing authorization＋Repo/Host ACL | `BOUNDED_STANDING_AUTH`；W2 protected `NOT_ADMITTED` | HEAD、write-set、preimage、diff、test、readback | 缺任一前件、diff 超出 write-set |
| `OPS` | §00.2.3＋Host/OS principal；產品 Host late-bind | `BOUNDED_LOCAL`；產品 `NOT_ADMITTED` | HostID、principal、pre/post、argv/exit、recovery | 錯 principal、無 recovery、UNKNOWN 盲重試 |
| `USER` | 原 consent/data scope | `NOT_CLAIMED` | consent、資料範圍、compensation | 無 consent、範圍不明 |
| `RELEASE` | 原 Publisher/發布 ACL | `NOT_CLAIMED` | Checker/Publisher、發布範圍、readback | 缺 Checker/Publisher |
| `HUMAN_OWNER_SELECTION` | Human Owner 本輪預授權 | 涵蓋 pack repair/adoption/W3 start/publication | adoption receipt、scope、not_claimed | 當成原 Issuer/OS/Checker |

## 05.2 角色與 SoD

| 角色 | 可做 | 不可做 |
|---|---|---|
| Human Owner | 採納規格/包/受界授權、風險 CR、撤權、公開發布決策 | 以聲明替 OS/Repo/Host ACL 或原域 Checker |
| CODEX Native（delegated executor/recorder） | 受界修補、檢測、隔離 smoke、證據、合法 publication；執行 Owner 決策 | 自稱第二 issuer、擴 scope、偽造 raw、代簽產品 verdict |
| Source/Case Curator | 讀來源、凍結 case/oracle、真 raw/manifest | 看到 observed 再改 expected、捏造 locator |
| TPM + Reviewer | 四契約／只讀逐義覆核；缺 Child/HardEdge/偽權拒 | 寫 canonical、發 grant、自簽產品 |
| Guide/Bridge | 有界薄提示／唯讀 context、實際材料 consume | 改 subject、擴權、第二調度 |
| Challenger | 凍結、隔離 run、advisory finding | 寫 subject/test/oracle、簽 independent |
| FAR | Research/RCA/alternatives/advice | 發 WO/Grant/Release、寫 product |
| CODEX Native Maker/Executor | 受權 exact op、真 pre/post/rollback、唯一工程調度 | 越權、改凍結候選、同 process 自驗冒獨立 |
| Checker | 獨立 frozen verification、判 verdict/strength | 替 Consumer 收件、依 Maker 任意可寫 verifier |
| Consumer | 真 parse/use/readback、接收回執 | 以 hash exchange 假 consume、冒 Checker |
| Publisher | 原域合法發布另案 | Git push／MD digest 冒 Release |

同一 Human Owner 可委派不同代理／session／worktree，至少分立 Challenger/Checker 與 Maker；原 policy 要求不同 principal 時不能只換模型。候選自身可能是惡意程式：先靜態檢查、無 secret env、最小權限隔離、timeout 不越界殺他人 process。in-process `sys.modules` 偽造是 W2 已揭露的 `RESIDUAL_LIMIT`，不宣 sandbox 防線完備。

## 05.3 Finding 八欄與五值

```json
{
  "id": "<actual finding id>",
  "severity": "<P1/P2/P3 or adopted original enum>",
  "class": "<actual class>",
  "subject_sha": "<64hex candidate identity>",
  "command": null,
  "exit": null,
  "raw_sha256": "<real raw sha256>",
  "reproduction": "<original reproduction enum>"
}
```

此為 schema 示意，不得直接產假 Finding。真 run command/exit 必須真有；靜態 finding 可依原 ABI 留 null，並 pin 真 observation raw；無 raw 不宣 `REPRODUCED`。`expected/observed/first_fail/case_id/child/fixture/oracle/NotCovered/source_refs/argv` 在原可選欄或 sidecar `FindingTrace` 關聯，不覆蓋八欄。

Advisory 五值僅 `PASS/FAIL/PARTIAL/BLOCKED_HITL/BLOCKED_EXTERNAL`；`UNREPRODUCED` 屬 reproduction/NotCovered，不是第六 verdict。Challenge report `original_checker_verdict=null`；Checker 另簽。

## 05.4 FAR 五態與十 Advice

| State | 真判準 | Raw／決策 |
|---|---|---|
| `HIT` | provider reachable，query 有相關結果 | attempted/reachable=true、rows+locator/digest、denominator、相關性理由 |
| `ZERO_RELEVANT_HIT` | 可達、正確查詢、真 enumeration/coverage，零相關 | rows=0、query/denominator/response raw；不等全庫不存在 |
| `UNAVAILABLE` | provider/DB/root 不存在或不可達 | reachable=false、rows/zero_results=null、原因；`RESEARCH_REQUIRED` |
| `BLOCKED_BY_AUTHORITY` | 原 ACL/policy 拒 | blocked_reason、permission state/attempted；不繞權、不改成零 |
| `ERROR` | 解析/SQL/timeout/執行錯 | error class/message redacted、raw/exit，rows=null 或保 partial |

| Advice 原名 | 真證據前置 | Guide2 alias／責任 |
|---|---|---|
| `FIX_NOW` | 真 RED/Reproduced、當期原需求、code genuine missing/bug，已查 existing | `CODE_FIX`／Developer，另 ECP |
| `BIND_EXISTING` | code 真在、caller/ABI/slot 未綁 | `BIND_REPAIR`／Binder，不重造 Writer |
| `ACTIVATE_HOST` | installed/bound 但 ActualServed 缺 | `ACTIVATE_HOST`／Host Owner，不自啟權 |
| `RUN_AFFECTED_TEST` | case/oracle 已具、raw 缺 | `CASE_TEST`／Runner，不自簽 independent |
| `FIX_PD` | 原 PI/PD 反向不一致且 RepoContext 核真 | `PD_CHANGE`／PD Writer |
| `PI_CHANGE_REQUEST` | 真原 Child/NEG/requirement 未滿足 | `PI_CHANGE`／PI Owner，CR 非完成 |
| `WAIT_ORIGINAL_AUTHORITY` | 真 op 欠 consent/issuer/principal 或已撤權 | `AUTHORITY_REQUEST`／Owner，合法 READ/DRAFT 可續 |
| `DEFER_TO_PHASE` | 原 phase/consumer 明許後波且非當期 hard | `DEFER_TO_WAVE`／Program Owner |
| `RECOMMEND_CLOSE` | 原 scope Done、真 Consumer 接受、所有受影 raw 已 pin | `CLOSE_AFTER_ORIGINAL_ACK`／Consumer，非 Release |
| `PARK_UNTIL_DELTA` | 雙期同 Source/HEAD/Host/Epoch/Oracle/World/FirstFail 真讀回均同 | `PARK_NO_DELTA`／Work Owner，新材料解除 |

`RESEARCH_REQUIRED/ABSTAIN` 是證據不足結論，不是第 11 有權 Advice。十種 Hypothesis 原名保留：`H-CODE-MISSING`、`H-CODE-EXISTS-BINDING-MISSING`、`H-HOST-NOT-ACTUAL_SERVED`、`H-CASE_ORACLE_RUN_MISSING`、`H-PD_DRIFT`、`H-PI_SOURCE_GAP`、`H-AUTHORITY_UNBOUND`、`H-PHASE_NONAPPLICABLE`、`H-RESEARCH_SOURCE_UNAVAILABLE`、`H-ALREADY_COMPLETE_SCOPE`；逐項可適用／NoFit，不硬給固定根因。

## 05.5 Guide 七鍵 ↔ 九鍵

| Guide 原九鍵 | FAR 原七鍵／身份 | Lossless rule |
|---|---|---|
| `subject` | subject（另於七鍵） | 同 runtime identity，非文件 ArtifactSubject |
| `scope` | scope（另於七鍵） | 同 scope 才比；跨 scope 拒 |
| `source_sha` | `source_manifest_sha256` | 原 Owner 明示同 Source 集合；manifest digest、source_set digest、pack digest 不默認等值 |
| `repo_head` | `repo_head` | 真 Git commit；dirty/untracked 另記 |
| `host_id` | `host_id` | 真 Host；CODEX/HERMES/GPT 不混 |
| `policy_epoch` | `policy_epoch` | 真 policy/version 或合法明示無 epoch；不可造值或 caller bool |
| `oracle_sha` | `oracle_sha256` | Case Owner 真 oracle bytes 同位 |
| `world_raw_sha` | `world_raw_sha256` | 真 WorldRaw bytes，不以 exit/summary 代 |
| `first_fail` | `first_fail_id` | 同 Case/Child 真 FirstFail ID，不能 `same_first_fail=true` |

`candidate_sha` 與 `evidence_sha` 是另列 evidence identity（不屬原七鍵或九鍵）。W1 `guide_nf._p_source_sha` 目前取 pack manifest，須透過明示 source-set crosswalk 與真 verifier 核對；不能把任一 hash 當同域。兩期 receipt 必須獨立實際觀測、先後 sequence/time 不同、source/raw/identity 可回取；不同 Host/epoch/Oracle 的新材料可觸發再資格化，但不是同條件 `NO_DELTA` 比較。

| 狀況 | Output | 行動 |
|---|---|---|
| 兩期同位、九鍵全部真、同鍵全相同、candidate/evidence 沒有新實質材料 | `NO_DELTA`（原 ABI 若為 `NO_MATERIAL_DELTA` 等別名則明確 crosswalk） | 停受影重派，可建議 PARK，不關閉 Case |
| 兩期可驗、任一 material 真變，或額外 candidate/evidence 有實質差額 | `NEW_DELTA` 候選（原 token 逐欄映射） | ChangeCone 受影 requalify/retest；identity/authority 改先重新准入 |
| 少一期/少 key/不可驗/單 evidence_sha/複製同 receipt | `DELTA_UNVERIFIED` | 不宣 PARK/no-delta；記所需 evidence、合法 READ 可續 |
| 跨 subject/scope/假 SHA/不可信 verifier | 拒 | 不建立假續工、不提升 claim |

`GuideThinResume`：`prior_prompt_sha`、同 pack ref、advice enum/alias、verified `material_delta`、owner、`next_operation`（effect intent only）、`stop_scope`、`resume_predicate`、`claim_ceiling`。Guide/Consumer 必須 parse 原材料、實際 use 下一操作／阻斷條件；不可只傳 digest 或打印文本。

## 05.6 Receipt 最小欄

`run_id/operation_id/runner_id/binary_sha256/host_id/os_principal/policy_epoch/project_id/subject/scope/fuo/source/candidate/evidence/oracle/case_set/fixture_sha/argv/cwd/env_redacted/timeout/start/end/exit/stdout_ref+sha/stderr_ref+sha/world_raw_ref+sha/pre/post/recovery/expected/observed/case_id/first_fail/observation_layer/actor/verification/signature_state`

null 的理由明示；不得含 token/private key。每條 raw path 解 canonical root，拒 absolute/`..`/UNC/escaping links、duplicate/case collision。各 run/case/phase 獨立 raw，不用上次 stdout 作當次。

---

# 06｜Stop／Resume／HOLD／CR／分母／Claim

## 06.0 V1–V3 驗收矩陣（r2 主用前必讀）

本矩陣是 control §06 在本包的落地；`05.verification` 只存機讀摘要，raw 在 `02_EVIDENCE/raw/`。三個 receipt 各自獨立，不互相冒充。

| Group | Criteria（實質） | r2 結果 | Raw／Receipt | State binding |
|---|---|---|---|---|
| V1 完整性/pin | strict JSON/duplicate key；5 files SHA/bytes/lines；36+ assets；16 case refs join；28 sources raw/bytes/spans/disposition；source_set；package_tree；external seal；clean checkout byte equality；負例 | `PASS` | `02_EVIDENCE/raw/checks/V1.stdout.txt`；`02_EVIDENCE/raw/CHECK_RUN_RECEIPT.json`；`02_EVIDENCE/W3_檢查修補與驗收_證據型附錄.md §04` | 只證明 pack 可重開；不證明產品 |
| V2 原義/可達性 | 33 FR 逐義 join；6 WP/6 FUO；16 案；7 Seam；五態；十 Advice；七/九鍵；24 HOLD；W2 12；typed DAG 無 cycle；active authority/selection；pack vs product 分帳 | `PASS` | `02_EVIDENCE/raw/checks/V2.stdout.txt`；`02_EVIDENCE/W3_檢查修補與驗收_證據型附錄.md §05` | 只證明原義與可達；不證明產品 |
| V3 可消費/啟動 | pack-internal `assets/tools/w3_consumer.py --check/--next`；fresh clean copy；16 case lookup；Freeze POS/NEG；兩 failure class；五態；十 Advice；七/九鍵；兩期/缺期；advice 非 grant；seal/path/duplicate 負例 | `PASS`（DOC/SMOKE） | `02_EVIDENCE/raw/checks/V3_SMOKE.stdout.txt`；`02_EVIDENCE/raw/smoke_clean/SMOKE_RECEIPT.json`；`02_EVIDENCE/W3_檢查修補與驗收_證據型附錄.md §06` | 可合法起工；不等同 16 原案產品 PASS |

**PASS 邊界**：V1–V3 是 `DOC/SMOKE`，不升格 `W3_TECHNICALLY_READY`／`W3_NF_VALIDATED`／`INDEPENDENT_PASS`／`RELEASED`。產品 `COMPONENT/INVOCATION/E2E/HOST` 仍依 `02` 與 `03` 真跑。



## 06.1 14 個上位 HOLD（不自動關閉）

| HOLD | 真缺口 | 本包處置 | Owner／Resume |
|---|---|---|---|
| `W1_HOST_NINE_GRID` | 三 Host 七階段未真觀測 | 只驗當期 target Host；其他留 W1 | Host Owner；逐 Host actual |
| `W1_PLUGIN_ALIAS` | alias 與 installed ID 未證等價 | 查 manifest/loaded ID；不猜等價 | Plugin/Host Owner；identity probe |
| `W1_ABI_BOUND` | 四 API/Guide IO 未真消費 | P06/SM05 真 consume；舊 proposal 留原域 | Guide/Bridge Owner；consumer raw |
| `W1_W0_INPUT` | W1 未取得新版 W0 actual | 由 W0 handoff/consumer 真讀；不以舊 author refs 代替 | W1 Owner；同版 handoff |
| `W0_PRIMARY_RECEIPT_STALE` | public/private receipt 版本差 | 保留歷史；新 manifest 另記 before/after | W0 Curator；真 origin 核對 |
| `W0-A_CASE_SELECTION` | 真非 FHS sample 未定 | G4 實查或 Owner 採 briefcheck；真 oracle | Project/Source Owner；選定＋授權 |
| `W0-B_NOT_ADMITTED` | 無真 DEV/OPS grant | 用實際 repo/host 權限；原 protected effect 仍需原 admission | Repo/Host Owner；真 ECP |
| `ORIGINAL_READER_UNBOUND` | 無原 PIPD typed reader | Generic 用真 file/Git/consumer；legacy 另帳 | PIPD Owner；typed readback |
| `ORACLE_FIXTURE_UNBOUND` | 原 24 Case 無 oracle/fixture bytes | 建新 NF oracle/fixture；原案不冒 PASS | Case Owner；真 bytes |
| `HOST_CAPABILITY_UNBOUND` | 無 actual served | W0/W1 已證部分只按真同位復用；其他另 probe | Host Owner；loaded/invoked/consumed |
| `CHECKER_PUBLISHER_UNBOUND` | 無獨立 checker/publisher | 真獨立 verifier；Publisher 不在本輪 | Checker/Publisher；同 candidate raw |
| `SOURCE_REFERENCE_HASH_CONFLICT` | 同名異 SHA 風險 | 同 ID/version/bytes；只停受影 | Source Curator；version ledger |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` | 1011/485 未解析 ID | Generic OFF 另驗；Legacy 留原分母 | Profile Owner；適用子集 |
| `HOLD_CR-DOC04-STATE-MAP` | 舊 T4/T5 formal transition | 不升格；新版 NF 狀態獨立 | 原 DOC04 具權者；裁決/readback |

**W2 專項 HOLD**：

| HOLD | 缺口 | Owner | Resume predicate |
|---|---|---|---|
| `W2_WRITER_BLOCKED` | 原 decision 被自身 finding 條款終止 | Human Owner | 具名 roots/targets/ops/expiry/recovery 新授權 |
| `W2_ORACLE_UNFROZEN` | 12 原案 oracle/case-set 僅 carried | Case Owner | 真 bytes 凍結並重算 digest |
| `W2_EVIDENCE_SEAL_PARTIAL` | evidence 僅 manifest 級 | Checker | 逐 raw 封存＋外置 seal |
| `W2_INDEPENDENT_PASS` | 修補後無獨立覆核 | Checker | 對 `dada235` 候選的獨立 receipt |

**W3 專項 HOLD**：

| HOLD | 缺口 | Owner | Resume predicate |
|---|---|---|---|
| `W3_PACK_ABSENT` | 已由 r2 `PACK_PRIMARY_SELECTED`＋adoption/seal 關閉 | W3 Owner | `CLOSED_BY_ADOPTION`；fresh receive 另記，不再阻合法起工 |
| `W3_RUNNER` | 原 Case/Runner 未得 | CaseRunner/Case Owner | 同 scope argv/exit/raw/fixture/oracle |
| `W3_EVIDENCE` | Evidence/WorldReader 未簽 | Evidence/WorldReader | trust chain＋WorldRaw |
| `W3_FAR_SOURCE` | Fabric typed source/ResearchWO 未得 | Fabric/HGK Router | HIT/ZERO/UNAVAILABLE 原 receipt |
| `W3_DELTA` | 兩期 World/HEAD/Oracle/FirstFail 未得 | WorldReader/Program | 兩期真 receipt |
| `W3_INDEPENDENT` | 原 Checker 未簽 | Protected Checker | 同 Candidate/Scope verdict |

## 06.2 R3-CR01–12（原名保留）

| CR | 原名 | Owner | 解鎖／狀態 |
|---|---|---|---|
| `R3-CR01` | `tpm-sp-plp` vs `plp-tpm-review` 真 Host alias | Plugin Owner | 三 Host manifest/version/actual-served；`OPEN_PRESERVED` |
| `R3-CR02` | Original PIPD／PI-PD/ECP/TQAEP 及 Case Reader | Original Writer/Reader | 同 SourceSHA/Subject/Scope typed receipt；`OPEN_PRESERVED` |
| `R3-CR03` | RepoRoot/HEAD/Dirty/ACL/Preimage/WriteSet | Repo Owner | 真 probe／原 PD late-bind；`OPEN_PRESERVED` |
| `R3-CR04` | Host/OS/EffectRegistry/Issuer/Admission/Recovery | Host/Issuer | 原 Policy/ECP/ActualWorldRaw；`OPEN_PRESERVED` |
| `R3-CR05` | Guide/Bridge/Challenge/FAR 真 Host Loaded/Invoked | 各 Host Owner | Call/Exit/Response SHA/Consumer readback；`OPEN_PRESERVED` |
| `R3-CR06` | Original Runner/Oracle/Checker/Publisher | 原不同 Checker/Publisher | 同 Subject/Scope/Host/Epoch Raw receipt；`OPEN_PRESERVED` |
| `R3-CR07` | 485/35 Tool Slot Fit/License/Pin/NoFit | FHS Tool Owner | 逐受影 Need 原 Reader/HostFit；`OPEN_PRESERVED` |
| `R3-CR08` | r2 引用原大型 FHS_vNEXT 五檔與 skipped 對話局部缺 bytes | Original Source Reader | 真 bytes/sha/line；`OPEN_PRESERVED` |
| `R3-CR09` | Actions v7 Pin/Runner、原 Repo Ruleset/Required Checks | GitHub Repo CI Owner | 當期 Release/Signature/Policy/Ruleset readback；`OPEN_PRESERVED` |
| `R3-CR10` | 原 Fabric FAR Patch、ResearchWorkOrder/三源現況 | Fabric Original Owner | Router/Provider Raw＋同 Scope Reader；`OPEN_PRESERVED` |
| `R3-CR11` | Actual W0-A Local Host/OriginalConsumer 真 E2E | 原 Executor/Guide/Bridge/Challenge Owners | 同 Scope command/exit/raw；`OPEN_PRESERVED` |
| `R3-CR12` | Actual W0-B 世界效果與回復/獨立驗收 | 原 Issuer/Runner/Checker | Admission+Pre/Post/Raw+Recovery；`OPEN_PRESERVED` |

## 06.3 F5-CR01–25（原名索引）

| CR | 原名／未知 | Owner | 解鎖／狀態 |
|---|---|---|---|
| `F5-CR01` | identity | W1/W3 Owner | 同 scope identity；`OPEN_PRESERVED` |
| `F5-CR02` | ABI | W1 Owner | lossless crosswalk；`OPEN_PRESERVED` |
| `F5-CR03` | source identity | Source Curator | 同 ID/bytes；`OPEN_PRESERVED` |
| `F5-CR04` | RepoContext | Repo Owner | live probe；`OPEN_PRESERVED` |
| `F5-CR05` | authority | Owner/Issuer | named decision/ACL；`OPEN_PRESERVED` |
| `F5-CR06` | Bridge | Bridge Owner | four API actual consume；`OPEN_PRESERVED` |
| `F5-CR07` | Guide Touch2 | Guide Owner | two-period nine keys；`OPEN_PRESERVED` |
| `F5-CR08` | Runner/Case | Case Runner | real argv/exit/raw；`OPEN_PRESERVED` |
| `F5-CR09` | FAR source | Research Owner | typed query receipt；`OPEN_PRESERVED` |
| `F5-CR10` | FAR retrieval | Research Owner | five-state ledger；`OPEN_PRESERVED` |
| `F5-CR11` | Profile ToolFit | W4 Tool Owner | per-slot Fit/NoFit；`OPEN_PRESERVED` |
| `F5-CR12` | Checker | Checker Owner | distinct verdict；`OPEN_PRESERVED` |
| `F5-CR13` | two-period delta | WorldReader/Guide | two real receipts；`OPEN_PRESERVED` |
| `F5-CR14` | ECP/TQAEP per wave | Pack Author | real ECP/TQAEP；`OPEN_PRESERVED` |
| `F5-CR15` | Consumer/Publisher | Consumer/Publisher | distinct receipt/Release；`OPEN_PRESERVED` |
| `F5-CR16` | 配對證據附錄及原 Audit 未全掛載 | Source Curator | 原 audit bytes；`OPEN_PRESERVED` |
| `F5-CR17` | Workflow action SHA 是否符合原 Repo Host Policy | Repo CI Owner | action ref/runner ABI/policy；`OPEN_PRESERVED` |
| `F5-CR18` | 公開/私有 Repo 與功能授權/Rulesets 適用性 | Repo Owner | ruleset/required-check readback；`OPEN_PRESERVED` |
| `F5-CR19` | SBOM/SLSA provenance 原 Publisher/Consumer 接收 | CI/Publisher | verify-attestation receipt；`OPEN_PRESERVED` |
| `F5-CR20` | Tool version/License/OS/HostFit | Tool/Legal/Host Owner | license/pins/NoFit；`OPEN_PRESERVED` |
| `F5-CR21` | Pipeline Required Check 名稱與改版衝突 | Repo Owner | exact context readback；`OPEN_PRESERVED` |
| `F5-CR22` | 2026 web/support 時效、社群樣本數 | Research Owner | version pin/dated record；`OPEN_PRESERVED` |
| `F5-CR23` | Windows reparse point、ACL、NTFS 身分 | Windows OS Reader | OS probe；`OPEN_PRESERVED` |
| `F5-CR24` | 14 核心外歷史文檔五份未本輪本地重驗 | Source Curator | real bytes/SHA；`OPEN_PRESERVED` |
| `F5-CR25` | 原密鑰外流、私有 repo 混 public CI | Security/Repo Owner | secret scan/data class；`OPEN_PRESERVED` |

## 06.4 RQ01–07

| RQ | 原意 | 本包落點 |
|---|---|---|
| `RQ01` | 真協作/fallback | P01–P06 的分立角色與 direct 路徑 |
| `RQ02` | 五方實質 consume | SM01–SM07 的 consumer readback |
| `RQ03` | 真 OFF | X09；兩路語義成功，不以同失敗 parity |
| `RQ04` | path security | `02` O1/O2、X10；absolute/`..`/UNC/symlink/reparse |
| `RQ05` | fresh receiver | P06／Consumer；clean checkout、wrong pin 拒 |
| `RQ06` | 九鍵 | P06；七鍵→九鍵 lossless |
| `RQ07` | publication/version reconcile | 本輪不改 repo；publication state 只作 evidence |

## 06.5 原分母 ledger（不作加總達成率）

| Namespace | 原分母／識別 | W3 disposition |
|---|---|---|
| W3 原案 | 16（§02.2／PLAN §09.1） | 當期主驗收；required 未跑則 partial |
| W2 | 12 + J1/J2/J3/S1/S1Δ/S2 | upstream requalify；不併 W3 16 |
| W0 | SAMPLE10、F5-W0-T01..24、NF-T01..10 | 44 actual；scoped reuse，不重跑/抵原案 |
| Challenge | EC-FR01..16、EC-WP01..09、EC-T01..26、EC-X27..36（26+10）、local47、C16/F5-T12 | 功能/WP/Case/例外/local 分帳；未得 `NOT_RUN`／`C16_NOT_RUN` |
| FAR | FAR-FR01..17、FAR-WP01..12、FAR-T01..20、FARP30（10 POS/12 NEG/3 EDGE/5 SEC）、local35（25+10）、FAR-Q0..Q10、RQ0..8、十 Advice | 當期適用能力需測；35 不抵 20/30 |
| Guide | CG-R2-REQ01..16、U01..26、CG-SEM01..17、local50 | Touch2/九鍵當期適用；原 17/三 Host 另案 |
| Bridge | PCB-FR01..17、A-PCB-001..022、AV3-001..030、38+28 | 四 API 及 W3 新材料消費；原 66 獨立 |
| TPM/Reviewer | F01..14、U01..16、QA26、35 tool | 四契約/真 reviewer；QA26 未跑不抵 |
| Program/FHS | U-001..056、R01..24、P00-01..06、FHS 22/36/50/39/96/192/485、1011=576 identified+435 unresolved slots | Generic 不強制 485；W4 依 Profile 真適用；count-only 不是 ID/ToolFit/PASS |
| 跨波 | N01..12、RQ01..07、14 HOLD、R3-CR01..12、F5-CR01..25 | 保原 namespace、owner/resume；CR/RQ/HOLD 非測例，不以數量算 PASS |

## 06.6 Stop／Resume／Claim

| FirstFail／trigger | 立即動作 | 重新進入 |
|---|---|---|
| `PIN_MISMATCH`／`FROZEN_IDENTITY_MISMATCH`／`ORACLE_DRIFT`／`CANDIDATE_CHANGED` | 停同 slice、不重用 raw、不改 oracle | 同位真 pins 或正式 CR/re-freeze |
| `FALSE_AUTHORITY`／`ADMISSION_TERMINATED_BY_SECURITY_FINDING`／`WRITE_SCOPE_VIOLATION` | 停受影 writer、保存 raw/未列 target hashes；security finding 觸發撤權 | Owner 真新決策、查 ACL/admission；禁止刪 marker 逃避 |
| `INVALID_PATH`／`RAW_UNTRUSTED`／`SECRET_LEAK` | 停受影 read/export，封存私有 raw，僅 redacted export | Security/Curator 真安全 readback；必要 rotate 由原 Owner |
| `UNREPRODUCED`／`RUNNER_UNBOUND`／`RESEARCH_REQUIRED` | 保 `NOT_RUN`／`ABSTAIN`，合法資料探查可續 | 具名原 fixture/runner/source/raw |
| `DELTA_UNVERIFIED`／`NO_DELTA_REWRITE_DENIED` | 不派、不假 PARK，保 LastGood | 真新 material 或 two-period verified pair |
| `FALSE_INDEPENDENT`／`FALSE_RELEASE`／`DENOMINATOR_LOSS` | 拒 claim、保原結果 | distinct Checker/Consumer/Publisher 或補逐 ID 真 evidence |

**Claim ledger**：

| 維度 | 本輪可宣 | 不可宣 | 證據 |
|---|---|---|---|
| Author | 六檔、33 FR、16 案、五態、十 Advice、兩 Finding 設計 | 作者即原域 | 本包 |
| Source | 28 源＋上游 pins 可回取 | Original Reader ACK | 來源證據附件 |
| Frozen | 作者 design pins | 原 Frozen Candidate | §00.3／§04.4 |
| Challenge | design contract | `REPRODUCED` | `03` 全 `NOT_RUN` |
| FAR | typed/root-cause/alternative 設計 | `FIX_NOW`／`CLOSE` | 五態／十 Advice 設計 |
| Independent | `NOT_CLAIMED` | `INDEPENDENT_PASS` | Checker HOLD |
| Release | `NOT_CLAIMED` | `RELEASED` | Publisher HOLD |

---

# 07｜W4 Handoff 與變更控制

## 07.1 W3 → W4 欄級 handoff

| W3 producer field | W4 consumer field／原 W4M 意義 | Transform／負例 |
|---|---|---|
| W3 identity、pack SHA、source_manifest_sha、candidate commit/aggregate、case_set/oracle/fixture/evidence seal | W4 frozen input identity | same target subject/scope trace；五 pin 各自核，不能用 W3M hash 冒候選 |
| `FindingSet[].raw_sha256`＋raw locator | `W4_DENOM_RAW.evidence_refs[]` | 保 case/child/finding/raw 同位；原域證據不假補 |
| `NotCovered[]`＋ledger 原 ID | `W4_DENOM_RAW.not_covered[]` | 每案 reason/owner/resume/firstfail，不能當 0 |
| `FARRetrievalGraph`／Hypothesis／Advice | W4 evidence/checker FAR refs | typed five-state preserved；UNAVAILABLE 不 ZERO；Advice 非 grant |
| `C16/EC-T26/EC-X10/FAR-T20/FARP30` 各分母 | W4 原分母 rows、Profile applicability | 原 ID/count/state 各別，不合併 |
| `W3_DELTA`／`MaterialDeltaReceipt` | W4 not_covered/next/resume | 兩期同位與 source/host/epoch；缺期 `DELTA_UNVERIFIED` |
| `CheckerReceipt` vs `ConsumerReceipt` | W4 assurance/receiver prerequisites | distinct、candidate-specific |
| `ChangeSet` actual pre/post/restore | W4 as-built，requalify scope | 真 changed targets/impact/affected tests；post 不當原 op precondition |

Handoff 必須有 `from_stage=W3 / to_stage=W4 / handoff_id / project / work_id / pack_ref / pack_manifest_sha256 / candidate_commit / candidate_preimage / oracle_sha256 / case_set_sha256 / evidence_ref / evidence_manifest_sha256 / checker_ref / consumer_ref / actual_readback{argv,exit,raw,action,result} / next_legal_action / dependencies / resume_predicate / not_covered / readiness / publication_state`。Handoff 本身 raw SHA 由外置 seal/consumer receipt 綁定。W3 PARTIAL 時，W4 可先合法 READ/DRAFT，正式 `W4_TECHNICALLY_READY/EXECUTION_READY` 不自動成立。

## 07.2 ChangeSet 與回寫

按 `FirstFail → source/version/span → original Req/Child/NEG → actual ABI/caller → affected WP/Case → before/after path+SHA → test/raw → consumer/owner` 輸出，記 `new_material`／`NoDelta`、LastGood/rollback。只更新真正受影的 PROG/PROJ/WnM/pack 或產品；上游已採納規格若需改動用 CR 及 Owner 原責任者，不能自稱整冊回寫已完成。原 W3M `FHS5.PLP.Wn.Writeback@local-1` 仍屬原設計 contract：actual 有真 candidate/source manifest/tests/holds/original_actions/owner 才可 emit，未跑不生成假 receipt。W3 pack writer 不自建 canonical product writer。

## 07.3 已知差額與下一合法動作

| 差額 | 影響 | 處置 |
|---|---|---|
| W2 `PARTIAL`；writer `BLOCKED_NOT_ADMITTED` | W3 技術 readiness 不能成立 | 保留；P01 只做合法 READ/DRAFT；Owner 另給 W2 授權 |
| W2 oracle/case-set `CARRIED_NOT_REFROZEN` | 12 原案不可當真 freeze | R2 Case Owner 真 bytes；W3 不代簽 |
| W2 evidence manifest 級 | 逐 raw seal 缺 | R3 Curator；缺 raw 具名 NC |
| W2 TQAEP/ledger token/target 差異 | 舊 verdict 不可直接重用 | Case Owner 裁決；先保存歷史 FAIL |
| W0M r3 vs r4 | 同名不同版本 | 保兩版；W0 actual 採 r4 |
| B00–B05 未全文人工覆核 | 原義抽取依 PLAN 附錄 B | 記 `REFERENCED_BY_PLAN_APPENDIX_A`；受影時回原源 |
| 正式 W3 產品 16 案未跑 | 不可宣 `W3_NF_VALIDATED` | 依 `03` 與 standing authorization 啟動；observed 留 null 直至真跑 |
| 產品 Host/runner/oracle 未 late-bind | 不可宣 `W3_EXECUTION_READY` 全域 | 逐 batch bind；缺則只停受影 op |

**下一合法動作**：

1. 已主用採納；Owner 若要求變更，走 CR／新 revision，不覆寫本版。
2. 後續 CODEX Native 依 `04` 啟動，先選材料齊且已具權的 P01/R0/R1 或隔離 smoke；依 `01/02` 逐 batch 綁 write-set；依 `03` 逐案執行。
3. W2 原責任者依 §04.4 R0–R7 完成可先合法處理的來源、Oracle/CaseSet、raw seal；若需 protected writer，Owner 另給 **W2** 具名授權。
4. 不得把本包 DOC green 當 `W3_NF_VALIDATED`；產品 readiness 依真 probe 另記。

---
---

**本檔終點**：W3 PI/PD r2 已為主用文件包；產品狀態仍為 `NOT_RUN`／`UNBOUND`／`NOT_CLAIMED`，依 `04` 與 standing authorization 真執行。
