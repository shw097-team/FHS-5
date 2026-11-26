# 00_W0_PI_PD｜W0 S1 受影主用包（PI／PD）

**S1 pack**：`W0-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W0/PACK-S1-20261126-r2`  
**supersedes**：`FHS5-PLP/W0/PACK-S1-20261126-r1` / `W0-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W0/PACK-NF-20261125-03` / `W0-NF-r3-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`｜固定 commit `ae05a74514d2c310f82bbf9bb1a2009078f11c87`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 受影重構的完整正文；本輪已依 Owner 預授權升格為「主用＋受界可施工」（document primary）。S1 節只替換受影 clause；未受影段落、原 ID、原分母、原 fixture/oracle bytes 與歷史證據原樣保留（見文末「原版正文」）。衝突時以原上位原義＋S1 受影條款為準；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## S1-0｜來源、效力與閱讀順序

| 欄 | 實際值 |
|---|---|
| 本候選 | `W0-S1-r2-CODEX-PRIMARY`（`FHS5-PLP/W0/PACK-S1-20261126-r2`） |
| 取代關係（候選） | `supersedes` `FHS5-PLP/W0/PACK-NF-20261125-03` / `W0-NF-r3-CODEX-PRIMARY`；**原版仍是現行主用，未切 Current** |
| 上位採納 | `PENDING`：PLAN r1 raw `7d628073…`、ADR r1 raw `a36b22fe…` 在本地未見 Owner 採納紀錄（`adoption_ref=null`）；本候選只依其設計條款編製，不宣設計生效 |
| 原版血緣 | 05 raw `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`；固定 commit `ae05a74514d2c310f82bbf9bb1a2009078f11c87`；本輪以 `git show` 重讀 18/18 檔與本地 bytes 全等 |
| 施工授權 | 本輪僅 READ/DRAFT/隔離編包；未新增 DEV/OPS/Repo/Host 權，未解封任何 protected 路徑 |
| 產品狀態 | `B0_NF=NOT_RUN`、`W0_NF_VALIDATED=NOT_CLAIMED`、`NATIVE_PASS=NOT_RUN`、`RELEASE=NOT_CLAIMED` |

閱讀順序：本節（S1 受影條款）→ 05 manifest → 原 §00–§11 正文 → 03 測例 → 04 薄入口。原正文的 `PLANNED`／`NOT_RUN` 仍是產品狀態；S1 只改文件承載，不把任何歷史 receipt 升為當期 PASS。

## S1-1｜DD01–DD10 在本波的落地

| DD | 本波落地條款 | 落點 | 必測反證 |
|---|---|---|---|
| DD01 唯一施工 Runtime | CODEX Native 是 S2 唯一調度／恢復；W0 五方按需；不新增 queue/dispatcher/issuer | 04；§04 DAG；§02 | 產品 OFF 時 Native direct DEV/test/recover 仍可完成；不得冒五方 PASS |
| DD02 Generic／Profile 隔離 | Generic 不硬依賴 HGK/FABRIC/SBL/FHS/PIPD/HERMES；Legacy 只在明示 profile | 02 O5；03 NF-T01/05/06 | cold fresh process＋真 import/call blocker＋positive control；env flag 不算 |
| DD03 五方獨立＋七 Seam | TPM/Reviewer、Guide、Bridge、Challenge、FAR 各自入口；direct file/Git 合法 | §02、§05、03 NF-T07/T08 | 有／無 optional provider 皆可完成合法操作；direct 不抵產品驗收 |
| DD04 成熟工具替代 | Git／PowerShell／Python stdlib／unittest／既有 13_ tools 優先；不自建 Reader/Registry/Runner | 01 §01；02 §01；03 §04 | 真 executable/version/argv/exit；工具存在≠PASS |
| DD05 授權分離 | READ/DRAFT/DEV/OPS/USER/RELEASE 分域；`permit=true`、ECP、Advice 皆非 Grant；撤權即停 | 01 §08；02 §00.3/§08 | 錯 root/HEAD/preimage/越 write-set/過期假授權 → 零 effect；合法正控成功 |
| DD06 操作／觀察／Oracle／Verdict 分離 | 先 admission 後 effect；exit 與語義分離；expected 先凍結 | 03 §00/§04/§05 | exit 0 但 post 錯 → `EFFECT_NOT_VERIFIED`；崩潰≠合法拒絕 |
| DD07 可信驗收角色 | Maker 不自簽；Checker 分立；Consumer fresh readback；不同 principal 依原政策 | 03 §04/§05；04 | 改 oracle／假 raw／自填 PASS → 拒收 |
| DD08 原義／分母守恆 | 14 WP、24 原案、NF-T01..10、SAMPLE R1–R10、44 歷史分帳全保留；不刪分母 | §04；03 §01–§03 | 雙向 ID join；缺／重／假 ID 拒；count-only 不造 ID |
| DD09 六檔單一真源 | 5 MD＋1 JSON；05 自 SHA 外置；原檔 bytes 不改 | 05；`02_EVIDENCE/seals/W0_PACK_SEAL.json` | strict JSON；無 self-hash；seal 對 05 raw bytes |
| DD10 真依賴與局部停止 | 只留真 HardEdge；post 不作 pre；同 failure key 無新料不重派 | §04.1；§04.3；本節 STOP 表 | 循環／phase overreach → 拒；缺件只停受影項 |

## S1-2｜14 WP、S2 切片與產品／施工分界

原 `F5-W0-01..14` 全數保留，語義不改；本節只加「S2 怎麼合法接續」與「哪些是文件、哪些是產品」。

| S2 切片 | 對應原 WP | 實際輸入 | 合法出口 | 不可冒稱 |
|---|---|---|---|---|
| `W0-R1` 來源與成果復用 | 01/05/14 | 13_ tools、B0 runner、原 44 receipts、source/evidence pins | 同位可回讀即 `REUSE`；只列真差額 | 44 receipts 不是本輪新跑 |
| `W0-R2` Native DEV/OPS 正控 | 08/12/13 | 真 git root/HEAD、exact write-set、preimage、可逆 output root | 真 patch/test/reverse 與 OPS readback/restore | 文件 `PLANNED` 不是 effect |
| `W0-R3` Legacy/Guide/Bridge/FAR OFF | 06/07/10 | cold isolated profile、import blocker、leak positive control | 兩路成功且語義投影相同；forbidden=0 | 只改 env 不是 OFF |
| `W0-R4` 五方按需與 consumer | 02/09/11/13 | 五方真入口、frozen candidate、fresh read-only consumer | 逐方 invoke/consume；pins/raw 同位 | direct bypass 不抵五方 PASS |
| `W0-R5` Windows 安全反證 | 07/09/12 | junction/symlink/reparse/ACL/Unicode/EOL/size/path traversal | 正控能抓越界；拒絕零 write/effect | 不可用 WSL 證 Windows native |

**產品／施工分界**：本候選的「完成」只等於六檔可讀、可定位 WP、可執行下一合法切片；`B0`、`W0_NF_VALIDATED`、`NATIVE_PASS`、`INDEPENDENT_PASS` 均為 `NOT_RUN`／`NOT_CLAIMED`。歷史 694 evidence、803 consumer checks、10 fail-closed、32 Challenge 僅在原同位條件下作 `HISTORICAL_REPORTED`，不得寫成當期实测。

**Typed DAG（S2）**：`05 已存在 → R1 → R2 → R4`；`R1 → R3`（OFF 需先有真 pack/命令）；`R2 → R5`（安全反證需真 write/effect 入口）；`R2/R3 → R4` 的 consumer 是 `POST_EVIDENCE`，不倒卡 R2。`R5` 失敗只停受影安全 claim，不停一般 READ/DRAFT。

**Owner／Stop／Resume**：

| 缺口 | 停止 | 仍可做 | Resume |
|---|---|---|---|
| product repo root/HEAD/ACL | R2 DEV | 文件、來源核銷、測例設計 | Owner 指定授權 checkout＋live probe |
| Host/principal/policy epoch | R2 OPS | R1／R3 設計、DEV | 同 Host/Epoch readback |
| 真 fixture/oracle/runner | 受影 case | 其他 NF／SAMPLE 設計 | Case Owner 凍結 bytes |
| 獨立 Checker/Consumer | independent claim | 作者自檢 | distinct session receipt |
| 原域 Legacy typed ref | FHS profile 子集 | Generic 路徑 | 原域 typed ref 或明列 NotCovered |

## S1-3｜作者驗收與不宣稱

本候選的作者層檢測（DOC-01..06）以真 parse／hash／ID join／隔離負例執行，結果記於 `02_EVIDENCE/W0_S1_證據附件.md` 與 `02_EVIDENCE/doc_results.json`；不以文件含 `PASS` 字串判綠。作者自檢強度為 `SELF_REVIEW`，不是獨立產品 Checker。

不宣稱：`B0_PASS`、`W0_NF_VALIDATED`、`INDEPENDENT_PASS`、`W1_TECHNICALLY_READY`、`RELEASE`、任何外部 OS/Repo/Host grant。

---

## 原版正文（血緣保留；S1 未明示者不變）

> **原版身份（superseded）**：以下為原版 `W0-NF-r3-CODEX-PRIMARY` 的 preamble 與正文，按原 bytes 保留。
>
> 其中所有 `PRIMARY`／`PASS`／`已完成`／`AUTHORIZED` 均屬原版歷史陳述，不適用於本候選；本候選效力只以上方 S1 header 與 S1 節為準。
>
> # FHS-5_PLP/W0｜Native-first PI/PD／B0-NF
>
> **artifact_id**：`FHS5-PLP/W0/PACK-NF-20261125-03`  
> **version**：`W0-NF-r3-CODEX-PRIMARY`｜**date**：2026-11-25（Asia/Taipei）  
> **project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W0`  
> **wave_id**：`FHS-5_PLP/W0`｜**batch_id**：`FHS-5/W0/B0-NF`  
> **source W0M**：`FHS5-PLP/W0M/PRIMARY-EXECUTABLE-NF-20261125-03`，`NF-r3-PRIMARY`，raw SHA `a1f186cc337a4b3828e53f77533df5c97fdda63e132521d861a79b884f0c3aef`，106,859 bytes／1,176 lines；另有 `W0M-CODEX-FIRST-r4` amendment（§00.6、§05.1、§05.5 #5、§08.1、§08.5）  
> **pack authority**：`W0M-NF-PRIMARY-20261125-01`＋`W0-CODEX-FIRST-20261125-01`＋`W0-OPS-NATIVE-20261125-01`（Human Owner 正式裁決：CODEX-first／Native-first；B0 sample 自主選定；本地 CODEX Native OPS ECP）  
> **baseline pack**：`W0-NF-r1`（GPT WORK 六檔；LastGood 保存於 `C:\Users\user\Documents\Codex\2026-11-25\new-chat-5\work\lastgood_W0-NF-r1\`，不覆寫）  
> **claim ceiling**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（CODEX-first）  
> **not_claimed**：`B0_NF_VALIDATED / W0_NF_VALIDATED / NATIVE_PASS / INDEPENDENT_PASS / W1_TECHNICALLY_READY / W1_EXECUTION_READY / RELEASED / EXTERNAL_OS_REPO_HOST_GRANT`
>
> > 本檔是 W0 的 PI/PD 與六檔主包入口，不是產品執行報告。`PLANNED`、`UNBOUND`、`NOT_ADMITTED`、`NOT_RUN` 均為實際狀態。任何「PASS」只指本輪文件與 pack 自驗，不指 B0/W0 產品通過。主用升格只表示本控制包可在其受界範圍內被下一輪使用，不表示任何真 Repo/Host/OPS 權限已取得。

## 00｜Goal／FUO／Done／Non-goal

### 00.1 Wave Goal

在已升格的 NF-r3-PRIMARY W0M＋CODEX-first amendment 下，將舊 W0 15 檔高保留重構為可被本地 CODEX Native 實際讀取的六檔主包；用一個真 Generic 小任務 `FHS-5/W0/B0-NF` 證明：

1. 真需求與來源可被 TPM＋Reviewer 編成 PI/PD/DEV ECP/OPS ECP/TQAEP。
2. Guide 以 `PACKAGE_FIRST` 產生 ThinStart，必要時才 `CONTEXT_AUGMENTED`。
3. Native Executor 可完成一筆有權、可逆的本地 DEV/OPS，含 readback 與 restore。
4. Challenge 以凍結候選作獨立 POS/NEG；FAR 以真 Finding 產生至少兩個實質方案。
5. 真 red→patch→retest 只回歸受影 ChangeCone。
6. Legacy/optional OFF 後，不受影工作仍可執行；五方自身產品驗證不被 direct bypass 取代。

### 00.2 FUO

> 在授權的本地環境，對一個真 Generic 工程需求，五方可獨立及協作生成可施工包；完成一筆可逆 code/operation；獨立重現一正一負；產生真 Finding、兩個方案、受影修補與再驗；關閉可選職能後，合法 direct 工作仍可完成；真 consumer 可讀回交接。

### 00.3 Done

| 層級 | Done 條件 |
|---|---|
| Pack | 六檔存在、JSON 可 parse、五 MD/JSON bytes/SHA 一致、links/UTF-8/table 通過、附件外部 seal 正確 |
| B0 | PI/PD/ECP/TQAEP 被真環境採用；五方 individual＋combined 真 invoke；合法 DEV/OPS；Challenge/FAR/修補；OFF；安全；獨立 Checker；consumer readback 全部真通過 |
| W0 | B0 成功且採納版 W0 全部必要 FUO/Case 已涵蓋；不足時只加最少 Bn |

本輪只追求 Pack Done；B0/W0 為 `NOT_RUN`。

### 00.4 Non-goals

- 不物化七個以上主檔；不把證據附件當第七規範檔。
- 不改 W0M、PLAN、MASTER/PROG/PROJ、WM、舊 W0/W1、產品 repo 或 Host。
- 不以 HERMES 安裝／Serving 作為主工程前置；HERMES 相容性另立工作包；不生成 actual receipt。
- 不建立第二 Runtime/Queue/Dispatcher/Issuer/Registry/ACK/Publisher。
- 不以舊 18/18、22/22、24/24、3 tests 或作者自檢宣產品 PASS。
- 不以 W4 Release、三 Host、全 485/1011 或 Publisher 作 B0 前置。

## 01｜主用來源、法位與授權

### 01.1 來源

| ID | 來源（實際路徑） | 版本／bytes／lines | raw SHA-256 | 用途／讀取層級 |
|---|---|---|---:|---|
| `W0M` | `...\FHS-5_Native-first_重構\W0M_Native-first_主用可執行_交付\FHS-5_PLP_W0M_完整實質正文.md` | `NF-r3-PRIMARY`／106,859／1,176 | `a1f186cc337a4b3828e53f77533df5c97fdda63e132521d861a79b884f0c3aef` | 直接規格／READ_FULL |
| `W0M-E` | 同目錄 `FHS-5_PLP_W0M_證據附件.md` | `NF-r3-PRIMARY`／30,283／374 | `6dee9837c50eecd09aa5db4ab8ce95766feb84e91709150cd4a8502c5d2a6b7d` | SUPPORT／SELECTED_READ（E0–E4） |
| `W0M-AMD` | `...\W0M_CODEX_FIRST\FHS-5_PLP_W0M_完整實質正文_CODEX-FIRST-r4.md` | `CODEX-FIRST-r4`／見附件 E9 | 見附件 E9 | CODEX-first 修訂／READ_FULL |
| `PLAN` | `...\FHS-5_Native-first_重構\FHS-5_PLP_W0_MASTER_Native-first重構方案.md` | `NF-PLAN-r1`／69,997／509 | `9efa36535762edcbc005f56ecc4687f009e9692c1ca2116919f48a58365d7b85` | B0/六檔/回寫／READ_FULL |
| `CTRL` | `...\FHS-5_Native-first_重構\FHS-5_PLP_W0_Native-first_GPT_WORK_最小執行控制包.md` | `WORK-W0-PACK-NF-r1`／24,544／111 | `982d77f997f5239686e79f8426c55ab2dcf98233caf6391932af46c74962d841` | 上一輪編包要求／READ_FULL |
| `W2M` | `...\FHS-5_PLP_WM\FHS-5_PLP_W2M_完整實質正文.md` | `W2M`／50,052／766 | `7b42af255c9056f83136c8cc1f053c8ac2821cc165f59101e4d4fcb5836a9edc` | 原 13 前件／SELECTED_READ §03.1 |
| `W4M` | `...\FHS-5_PLP_WM\FHS-5_PLP_W4M_完整實質正文.md` | `W4M`／57,789／819 | `3276aa0ea87ac12fe3169fcc7f19243ec2937069218442f8d61af53c9df70067` | Checker/Consumer／SELECTED_READ §06.3/§10.2 |
| `OLD-PACK` | `...\FHS-5_PLP_W0-W4_實作\W0\FHS5_PLP_W0_FINAL_20261124\FHS-5_PLP_W0_EXECUTABLE_FINAL\` 15 檔 | `W0-EXEC-SEL-20261124-01` | 見附件 E1.2 | 舊→新 crosswalk／READ_FULL |
| `W0-CLOSE` | `...\FHS-5_PLP_W0-W4_實作\W0\FHS5_W0_CLOSEOUT_PRIMARY_HANDOFF_20261124.md` | `W0-PRIMARY`／2,840／41 | `994264b1273e7127f032e41c72b7a97b0bf8e30139bcbab20eec1e543b5faeb3` | 既有 HOLD/G4 線索／READ_FULL |

來源優先：本次 Owner 指令→已採納 NF-r3-PRIMARY 與 NF-PLAN 的受影有效裁決→未受影原產品、安全、相容義務→待修包；真觀測用於證明/反駁設計，不自動改需求。所有來源只讀，本輪不覆寫。

### 01.2 授權

| 欄 | 值 |
|---|---|
| decision_id | `W0M-NF-PRIMARY-20261125-01` |
| Owner | 使用者（Human Owner） |
| 授權 | 本地 primary＋CODEX-first 受界執行；W0 六檔修補、文件自驗、主用升格與後續 W0–W4 工程 |
| 可執行 | READ、隔離 DRAFT、多個受界可逆 DEV、本地 CODEX OPS run/readback/restore（真權限時） |
| 不可自行授予 | 外部 OS/Repo/Host grant、Publisher release、跨專案寫入、Actual receipt |
| 單一授權 | 不再重簽每個 WP；不建第二人類、Issuer 或 Registry |

真 roots/write-set/principal 仍由後續 W0 執行者在 §01/§02 的 probe 後填實；本 pack 只提供 planned 與取得方式。

### 01.3 本次主用升格記錄（由 Owner 預授權，非 CODEX 簽章）

| 欄 | 值 |
|---|---|
| pack decision_id | `W0-CODEX-FIRST-20261125-01`（pack `W0-NF-r3-CODEX-PRIMARY`） |
| decision_kind | `HUMAN_OWNER_CODEX_FIRST_PROMOTION_WITH_SCOPED_MULTI_OPERATION_AUTHORIZATION` |
| 依據 | Human Owner 正式裁決（CODEX-first／Native-first、B0 sample 自主、本地 CODEX Native OPS ECP）＋`W0M-NF-PRIMARY-20261125-01` |
| 選用版本 | `W0-NF-r3-CODEX-PRIMARY`（000–05 六檔＋外部證據附件＋W0M amendment） |
| 取代 | `W0-NF-r2-PRIMARY`／`W0-NF-r1`（LastGood／歷史，不刪） |
| Scope | `FHS-5/W0/B0-NF` 的 pack 讀取、CODEX Native Guide、DEV/OPS、Challenge/FAR、B0 與後續 W0–W4 受界工程 |
| 限制 | 只在合法 CODEX 工作區寫入；不改來源、外部 Host/ACL/憑證；不發布；HERMES Compatibility 另包 |
| 有效期／撤權 | 至 Owner 撤權、Scope/Repo/Host/Effect 變更或安全 Finding；權限拒絕即停受影 effect |
| 明示 | 此記錄是 Human Owner 正式裁決的落地，不是 CODEX 自造簽章、不是 OS/Repo/Host/Publisher grant；真權限仍須存在 |

### 01.4 作者完成、主用與產品完成分離

1. 本輪完成的是「可施工控制包」與其文件自驗；不是 B0/W0 產品完成。
2. `PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION` 只覆蓋本 pack 在其 Scope 內可被下一輪使用。
3. 產品完成仍須真 Repo/Host、真 DEV/OPS、獨立 Checker、actual raw 與 consumer readback。
4. 任何 `PASS` 只覆蓋 PKG-01..05 文件檢測，不覆蓋 B0/W0/Native/Independent/Release。

## 02｜Product SPEC：五方與 B0

| 方 | 真正功能 | 本包落點 | 不可降級 |
|---|---|---|---|
| TPM＋Reviewer | PI/PD/DEV/OPS/TQAEP；QA26/F01–F14 的反查 | 00/01/02/03 | Parent/Child/NEG、缺 B、無源 Gate |
| Guide | `PACKAGE_FIRST`；不足才 `CONTEXT_AUGMENTED`；Touch1/Touch2；ThinStart/Resume；九鍵 Delta | 00/04 | 不擴 Scope、不假 ACK、`DELTA_UNVERIFIED` 不假 PARK |
| Bridge | `inspect_package`／`explain_slice`／`render_agent_context`／`compare_context`；38＋28 | 00/03 | root confinement、SHA/span、unknown 保真 |
| Challenge | 五 pin；frozen candidate；獨立 POS/NEG；八欄 Finding；C16/EC-36/local47 | 03 | 不改受審、無 raw 不 proven |
| FAR | RQ0–8；≥2 Alternative；10 Advice；七鍵；T20/FARP30/local35 | 03/04 | UNAVAILABLE≠ZERO；無證據不 CLOSE |

### 02.1 A/B/C 與 B0-NF

| 名稱 | 功能／Batch | 本波 | 不是 |
|---|---|---|---|
| W0-A | 真來源、PI/Review、Guide、Bridge、READ/DRAFT | planned＋條件化 | 不是文件排版 |
| W0-B | 有權 Native DEV/OPS、readback、restore | planned；真權限才可 | 不是 B0 |
| W0-C | FHS Legacy ID／Profile 適用性 | deferred／profile-only | 不是 Generic 前置 |
| `B0-NF` | 一個真 Generic 小任務的五方＋Native 閉環 | 首個 Batch；本輪不跑 | 不是 SST B0、不是原 W0-B |

### 02.2 具名產品契約與原分母

這些是 FHS-5 自身產品分母；B0 只做代表案例，完整分母留 W1–W4，不與 24/10 混算。

| 產品 | 具名契約／分母 | B0 代表 | 後續 |
|---|---|---|---|
| Reviewer | `QA26`／`F01–F14`；14 功能 | 缺 B、無源 Gate、反向 provenance | W1 原分母 |
| Guide | `U26`；`CG-SEM01–17`、`CG-X01–X13`、`CG-FAR-01–10`；admin `20/50`；`PACKAGE_FIRST`、`CONTEXT_AUGMENTED`、Touch1/Touch2、九鍵 Delta、WAIT/PARK | ThinStart/Resume；package-first；九鍵可核 | W1/W3 |
| Bridge | `inspect_package`／`explain_slice`／`render_agent_context`／`compare_context`；原 `38＋28` | 四 API on/off；path/identity compare | W1 38＋28 |
| Challenge | `C16`／`EC-36`（EC-T01..26＋EC-X27..36）／local `47`；五 pin；八欄 Finding | frozen POS/NEG；C16 另帳 | W1/W4 原 Runner |
| FAR | `FAR-FR01–17`；`RQ0–8`；10 Advice；FAR 七鍵；`FAR-T20`／`FARP30`／local `35`；五種 source status | ≥2 方案；真 Finding；source status | W1/W3；Fabric Profile |
| FHS Legacy | `22/36/50/39/96/192/485`；`1011/576/435`；`35/56` | Generic 不背；FHS 適用子集 | W0-C/W4 |

**判讀**：`PACKAGE_FIRST` 優先，body 不足才 `CONTEXT_AUGMENTED`；Guide 九鍵與 FAR 七鍵不同 schema；Challenge C16 與 local47 不互代；UNAVAILABLE≠ZERO。

## 03｜Architecture SPEC與 NF01–10

| ADR | 實施規則 | 本包檢核 |
|---|---|---|
| NF01 | Native Executor 唯一調度；五方按需 | 無第二 Queue/Dispatcher |
| NF02 | Generic 不預設 HGK/FABRIC/SBL/FHS/PIPD | OFF 冷啟／parity 計畫 |
| NF03 | 無 OriginalReader/Registry/Runner/ACK mandatory | 真 file/Git/測試/readback 替代 |
| NF04 | HardEdge 有 producer；後驗不作前置 | §04 DAG |
| NF05 | 設計≠權限；READ/DRAFT/DEV/OPS/外部/Release 分帳 | 01/02 effect boundary |
| NF06 | 五方可獨立；七 Seam 非全域 ABI Gate | §05 Seam 表 |
| NF07 | B0 先行；W1–W4 不倒卡 W0 | §04 B0／W1 |
| NF08 | 六檔單一真源；舊 15 檔只做血緣/必要 projection | 05 manifest、附件 crosswalk |
| NF09 | 原 ID/分母/Receipt 永保；未測不 PASS | 03 分母 |
| NF10 | FirstFail/ChangeCone/Owner/LastGood 局部停復 | 附件 PKG loop |

## 04｜Program SPEC：14 WP 與 typed DAG

| WP | Input → Operation → Output | Owner／Consumer | 退出／NEG |
|---|---|---|---|
| `F5-W0-01` SourceFreeze | 真來源 → bytes/SHA/span/ACL → SourceLedger | Curator→Reviewer | 同名異 SHA→`SOURCE_INTEGRITY_FAILED` |
| `F5-W0-02` PluginIdentity | repo/skills/Host probe → alias/installed/bound/invoked | Host Owner→Program | 技能可讀≠serviced |
| `F5-W0-03` PI/Reviewer | 來源/Goal → PI、Child/NEG、缺 B、無源 Gate | Reviewer→PD | `REQUIRED_CHILD_MISSING` |
| `F5-W0-04` W0M-PD | PI＋actual capability → 13 章／B0 slice／edges | Wave→Pack | 未 probe 不填 HEAD/權限 |
| `F5-W0-05` W0-Control | W0M＋真環境 → 六檔／manifest | Pack→Guide/Executor | 空殼／缺檔→`PACKAGE_INTEGRITY_HOLD` |
| `F5-W0-06` GuideThinStart | pack digest/Goal/Done/Effect → ThinStart | Guide→Executor | 擴 Scope→`SCOPE_DRIFT` |
| `F5-W0-07` BridgeRead | root/pack → 四 API／span/SHA/compare | Bridge→Guide | 越界／loss→`BRIDGE_BOUNDARY_FAIL` |
| `F5-W0-08` NativeRead | pack/context＋Host → 真 read/run raw | Executor→Challenge | 手寫摘要不算 actual |
| `F5-W0-09` FrozenChallenge | candidate/oracle/fixture → frozen POS/NEG/Finding | Challenger→FAR | 改 oracle→拒收 |
| `F5-W0-10` ResearchCandidate | 真 Finding → 根因／≥2 方案／成本未知 | FAR→Guide | UNAVAILABLE≠ZERO |
| `F5-W0-11` GuideResume | finding/delta/LastGood → ThinResume/next | Guide→Executor | 無 delta 不重派 |
| `F5-W0-12` NativeProtected | 採納 ECP＋真權限 → 可逆 DEV/OPS＋readback | Maker→Checker | 無權→`NOT_ADMITTED` |
| `F5-W0-13` Assurance | frozen candidate＋raw → 獨立 verdict | Checker→Program | Maker 不自簽 |
| `F5-W0-14` Delta/Handoff | actual/nonclaim → CLOSEOUT/HANDOFF/ChangeSet | Program→W1 | expected≠actual |

### 04.1 Typed edges

`HARD_PRE`：01→03→04→05（本輪已完成 05 物化）；B0 從已存在的 05 進入 06/08/12（依影響）；09 需真 candidate；12 需 ECP/真權限；13 需 frozen final＋raw；14 需 09/12/13。  
`OPTIONAL_INFO`：02 探查可與 01/03 並行；07 Bridge 可選；Legacy inventory 不阻 Generic。  
`POST_EVIDENCE`：actual raw、CLOSEOUT、HANDOFF、MASTER 回寫不得作同操作前置。  
`DEFERRED`：W1 三 Host、W2 全 effects、W3 深迭代、W4 發布、FHS 485 全量。  
`UNVERIFIED`：G4 實體、真 Repo/ACL、HERMES Compatibility、W1–W4 尚未取證；本地 CODEX OPS 依 `W0-OPS-NATIVE-20261125-01` 承接。

### 04.2 B0 順序

```text
[本輪已完成] 01 Source freeze → 03 PI/Reviewer → 04 PD → 05 pack（本包）
[下一輪 B0 起點] 05 已存在 → 02 capability probe → 06 GuideStart → 08 NativeRead
                                              ├→ 07 Bridge（optional）
                                              └→ 12 NativeProtected（真權限）
06/08/12 → 09 Challenge → 10 FAR → 11 Resume → 12' patch
09/12'/13 final＋OFF → 14 Handoff
```

`12` 初始 effect 與 `12'` patch 是不同 revision；不得以 `12` 的 post-readback 作 `12'` 前置。B0 不重編 05；若真差額需改 pack，走受影 ChangeCone 與新版本，不覆寫已選用主包。

### 04.3 DAG 反例（必須拒絕）

| 反例 | 判定 |
|---|---|
| `W4 Release → W0 READ` | `PHASE_OVERREACH_CANDIDATE`；READ 不受 W4 未完成影響 |
| `post-readback → 同操作 admission` | `GATE_CYCLE_CANDIDATE`；不得執行該 effect |
| `05 pack → 04 PD` 當 runtime 前置 | 文件編排倒置；B0 不重編 pack |
| `07 Bridge → 08 direct read` 被畫成 hard | `OPTIONAL_INFO` 硬化；direct 應可走 |
| 「等原 Reader」而無 producer | `UNVERIFIED`；改 direct／`AUTHORITY_REQUEST`／`CONTRACT_DECISION` |
| `12'` 被當成同一 `12` 節點 | `GATE_CYCLE_CANDIDATE`；必須新 revision/ECP |

## 05｜七 Seam 最小 IO

| Seam | Producer→Consumer | 最小輸出 | 版本／NEG |
|---|---|---|---|
| SM01 | Source→TPM/Reviewer | source SHA/span/Child/NEG | raw SHA；同名異 SHA 拒 |
| SM02 | PI→PD | req/acceptance/capability/edges | PI/PD revision；無源 mandatory 拒 |
| SM03 | PD→ECP/TQAEP | op/root/writes/preimage/argv/oracle | PD/ECP/TQAEP id；後驗不前置 |
| SM04 | Pack→Guide | pack digest/FUO/Done/limits | pack digest；不擴 Scope |
| SM05 | Guide/Bridge→Executor | direct ref 或 context/span/digest | context id；Bridge OFF direct |
| SM06 | Executor→Challenge→FAR | candidate/oracle/raw/Finding/NotCovered | 五 pin；不改受審 |
| SM07 | FAR/delta→Guide/Consumer | advice/next/stop/readback | evidence id；假 ACK 拒 |

## 06｜Requirement、Child、NEG、Exception

| ID | Parent→Child | NEG／Exception | 本包落點 |
|---|---|---|---|
| NF-R01 真來源/計畫 | R01.1 freeze；R01.2 Child；R01.3 四契約 | 同名異 SHA、缺 B、假 ID | 00/03 |
| NF-R02 薄提示 | R02.1 package-first；R02.2 scope；R02.3 resume | 只貼 prompt、擴 Scope | 04 |
| NF-R03 Bridge | R03.1–4 四 API；R03.5 confinement | path escape、unknown loss | 00/03 |
| NF-R04 Native | R04.1 DEV；R04.2 OPS；R04.3 readback；R04.4 restore | 假 permit、越寫集、CLI 0 但 state 錯 | 01/02 |
| NF-R05 Challenge | R05.1 五 pin；R05.2 POS/NEG；R05.3 no-write；R05.4 stale raw | 改 oracle/candidate、無 raw | 03 |
| NF-R06 FAR | R06.1 Finding；R06.2 ≥2 方案；R06.3 成本/未知；R06.4 Next | UNAVAILABLE=0、FIX_NOW 無據 | 03/04 |
| NF-R07 收斂 | R07.1 red；R07.2 patch；R07.3 retest；R07.4 stop | 只改 status、無限重派 | 01/02/03 |
| NF-R08 去耦合 | R08.1 cold-off；R08.2 optional parity；R08.3 trace；R08.4 Legacy | 隱性 import、只改 env | 00/02 |
| NF-R09 交接 | R09.1 pins；R09.2 consumer；R09.3 W1 雙層；R09.4 回寫 | 假 manifest/ACK | 00/04 |
| NF-R10 安全 | R10.1 root/ACL；R10.2 writes/secret；R10.3 unknown/recovery；R10.4 獨立 | 技能可讀=Grant、未知 effect=READ | 01/02/03 |

## 07｜原 13 前件＋NF 3

原域狀態一律 `UNBOUND`，不因本包作者設計改為 `READY`；每項列原域狀態、Generic 替代／取得、Producer/Owner、Next/Resume、受影 effect。

| # | 原前件 | 原域狀態 | Generic 替代／取得 | Producer／Owner | Next／Resume | 受影 effect |
|---:|---|---|---|---|---|---|
| 1 | Original OperationType | `UNBOUND` | 同 Scope typed token；否則只做 READ/DRAFT | Effect Owner | 提供 typed token | DEV/OPS |
| 2 | RepoContext | `UNBOUND` | D1 `git rev-parse`/`status` live probe | Repo Owner | Owner 指定授權 checkout | DEV |
| 3 | HostID／OS Principal／PolicyEpoch | `UNBOUND` | O1 Host probe（`Get-Command`/help/session） | Host／OS Owner | 同 Host/Epoch identity | OPS |
| 4 | Original DEV ECP | `UNBOUND` | 本包 01 planned ECP；原 canonical 另接 | Repo＋Owner | 原 typed ref 或採納本 ECP | DEV |
| 5 | **Original OPS ECP** | **`HISTORICAL_UNBOUND`／`ADOPTED_LOCAL`** | **已由 `W0-OPS-NATIVE-20261125-01` 採納本地 CODEX Native OPS ECP；原域身份保留** | Human Owner＋CODEX Host | 本地 O1–O6 可執行；Legacy Profile 才接原 typed ref | OPS O1–O6（本地） |
| 6 | Issuer | `UNBOUND` | Owner 授權責任（非服務） | Human Owner | 真權限決策記錄 | DEV/OPS |
| 7 | WorkOrder | `UNBOUND` | 真 bytes/SHA；無不施工 | Owner／原 Issuer | WorkOrder ref | DEV/OPS |
| 8 | ExecutionAdmission | `UNBOUND` | 真 receipt；`permit=true` 無效 | Owner／原 Issuer | 同 Scope receipt | DEV/OPS |
| 9 | Exact WriteSet/preimage | `UNBOUND` | 01 逐檔 write-set＋preimage/absent | Repo／Host Owner | 逐檔 absolute＋SHA | DEV/OPS |
| 10 | WorldReader/RepoReader | `UNBOUND` | 直接 file/Git/process/consumer readback | Reader Owner | 同 Host/Epoch readback | DEV/OPS |
| 11 | Protected Checker | `UNBOUND` | 獨立 session/worktree verifier | Checker Owner | distinct verdict | Assurance |
| 12 | Publisher | `UNBOUND` | 不在 B0；原發布程序另接 | Publisher | Release 前 | Release（非 B0） |
| 13 | Recovery ABI | `UNBOUND` | DEV 反向 patch；OPS Host recovery | Repo／Host Owner | 真 recovery ref | DEV/OPS |
| NF-1 | Original TQAEP/Case | `UNBOUND`／`PLANNED` | 03 新 NF fixtures＋原 24 映射 | Case／Checker Owner | 凍結 expected | Challenge |
| NF-2 | Original Receiver ABI | `UNBOUND` | NF local IO；必要時 Contract Decision | Host／Consumer Owner | ABI ref 或本地 IO | OPS |
| NF-3 | Host preimage | `UNBOUND` | O3 前 pre-state probe | Repo／Host Owner | before SHA | OPS |

**階段閘（CODEX-first）**：第 5 項已由本地 CODEX Native OPS ECP 承接；O1–O6 可在真 principal/scope/preimage/output root/recovery 成立時執行。原域 Original OPS ECP 只保留歷史與 Legacy Profile 適用性；不得用 `permit=true` 或本機 CLI 冒充原域 receipt。

### 07.3 歷史 HOLD／R3-CR／WM2E（全部保留，不關閉）

| ID | 真缺口 | 本包處置 | Owner／Resume |
|---|---|---|---|
| `W1_HOST_NINE_GRID` | 三 Host 七階段未觀測 | 保留；B0 只驗 target Host | Host Owner／逐 Host actual |
| `W1_PLUGIN_ALIAS` | alias 與 installed ID 未證等價 | 保留 | Plugin Owner／identity probe |
| `W1_ABI_BOUND` | 四 API/Guide IO 未真消費 | 保留 | Guide/Bridge Owner／consumer raw |
| `W1_W0_INPUT` | W1 未取得新版 W0 actual | 保留 | W1 Owner／同版 handoff |
| `W0_PRIMARY_RECEIPT_STALE` | public/private receipt 版本差 | 保留歷史；本 manifest 記 before/after | Source Curator／origin 核對 |
| `W0-A_CASE_SELECTION` | 真非 FHS sample 未定 | 保留；G4 實查或 briefcheck | Project/Source Owner／一次選定 |
| `W0-B_NOT_ADMITTED` | 原域 protected DEV/OPS 無 grant | 原域保留；**本地 CODEX DEV/OPS 已由 `W0-CODEX-FIRST` 受界授權** | Repo/Host Owner／原域 ECP；CODEX 本地照 01/02 |
| `ORIGINAL_READER_UNBOUND` | 無原 PIPD typed reader | 保留；Generic direct | Reader Owner／typed readback |
| `ORACLE_FIXTURE_UNBOUND` | 原 24 Case 無 oracle/fixture bytes | 保留；03 建新 NF oracle | Case Owner／真 bytes |
| `HOST_CAPABILITY_UNBOUND` | 無 actual served | 保留；本輪 probe 記 binary/限制 | Host Owner／loaded/invoked/consumed |
| `CHECKER_PUBLISHER_UNBOUND` | 無獨立 checker/publisher | 保留 | Checker/Publisher／distinct receipt |
| `SOURCE_REFERENCE_HASH_CONFLICT` | 歷史 receipt 指紋可能不同 | 保留；本 manifest 重算 | Source Curator／version ledger |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` | 1011/485 未解析 ID | 保留 | Profile Owner／適用子集 |
| `HOLD_CR-DOC04-STATE-MAP` | 舊 T4/T5 formal transition | 保留；不升格 | 原 DOC04 具權者／裁決 |

| 原 CR | 對位 | 狀態 | Owner／Next |
|---|---|---|---|
| `R3-CR01` | `W1_PLUGIN_ALIAS`／`W1_HOST_NINE_GRID` | `OPEN_PRESERVED` | Host Owner／alias+Host |
| `R3-CR02` | `ORIGINAL_READER_UNBOUND` | `OPEN_PRESERVED` | Reader Owner／typed readback |
| `R3-CR03` | `W0-B_NOT_ADMITTED`／第 2 項 | `OPEN_PRESERVED` | Repo Owner／RepoContext |
| `R3-CR04` | `W0-B_NOT_ADMITTED`／第 6–8 項 | `OPEN_PRESERVED` | Issuer／receipt 分列 |
| `R3-CR05` | `HOST_CAPABILITY_UNBOUND`／`W1_ABI_BOUND` | `OPEN_PRESERVED` | Host Owner／三層證據 |
| `R3-CR06` | `CHECKER_PUBLISHER_UNBOUND` | `OPEN_PRESERVED` | Checker／distinct receipts |
| `R3-CR07` | W4M ToolFit/License `DEFER` | `OPEN_PRESERVED` | W4 Owner／35/485 子集 |
| `R3-CR08` | `SOURCE_REFERENCE_HASH_CONFLICT` | `OPEN_PRESERVED` | Source Curator／origin |
| `R3-CR09` | W1 CI/Ruleset `DEFER` | `OPEN_PRESERVED` | Program Owner／真 CI |
| `R3-CR10` | FAR Fabric `PROFILE/DEFER` | `OPEN_PRESERVED` | FAR Owner／原 Profile |
| `R3-CR11` | `W0-A_CASE_SELECTION` | `OPEN_PRESERVED` | Project Owner／sample |
| `R3-CR12` | `W0-B_NOT_ADMITTED`／第 13 項 | `OPEN_PRESERVED` | Repo/Host Owner／Recovery ABI |
| `WM2E_NOT_READ` | W0M 證據附件 E1 | `HISTORICAL_SUPPORT_ONLY` | Source Curator／需要時讀 |

本輪不因新增主用包而關閉任何一項；同一 ID/Scope 無真證據不得改為 CLOSE。

## 08｜Capability／Repo／Host 的實際 planning context

### 08.1 本輪 read-only probe（2026-11-25，Asia/Taipei）

| 對象 | 實際觀測 | 狀態／disposition |
|---|---|---|
| OS | Microsoft Windows 10.0.26200 | `TOOL_PRESENT` |
| PowerShell | 7.6.9 | `TOOL_PRESENT` |
| Python | 3.11.9（`...\Python311\python.exe`） | `TOOL_PRESENT` |
| Git | 2.53.0.windows.1 | `TOOL_PRESENT` |
| CODEX Native Host | 目前 CODEX desktop session；Python 3.11.9；Git 2.53.0；workspace write root 可用 | `READY`（主工程 Host） |
| HERMES（Compatibility） | binary 存在；`hermes --version` 回報 install state 不可寫 | `HOST_BINARY_PRESENT / HOST_SERVING_UNVERIFIED`；**不阻斷 CODEX**；另立 Compatibility |
| Codex CLI | `codex.ps1` 存在 | `TOOL_PRESENT`（本輪用其原生互動，不另建 harness） |
| Node | 存在 | `TOOL_PRESENT`（非必需） |
| product repo | 未指定 root；未執行 Git probe | `UNBOUND` |
| G4 | 只有 W0 CLOSEOUT 的 3 tests 報告；無本地路徑/需求/權利 | `REPORTED_RUNNABLE / OWNER_DESIGNATION_REQUIRED` |
| briefcheck | 尚未建；03 有 bytes/argv/oracle | `PLANNED` |
| W1 reference | `W1/impl/w1_bridge_reference.py` 本地未找到 | `UNVERIFIED`；不假存在 |
| W1 checks | `replay_hashes.py`、`w1_guard.py`、`m22_guard_ref.py`、`run_cases.py`、`run_harness.py` 可見 | `REPLAY_CANDIDATE`；未跑 |
| 五方資料夾 | TPM-SP／Guide／Bridge／Challenge／FAR 目錄可見 | `LOCAL_PATH_VISIBLE`；未宣 Host served |
| Python/Git 產品環境 | 文件工作可用；產品 repo 版本未確認 | `TOOL_PRESENT / PRODUCT_ENV_UNVERIFIED` |

### 08.2 能力處置

| 能力 | 處置 | 最小退出 |
|---|---|---|
| FHS-5 五方資料夾 | `REUSE`／`BIND_EXISTING` | 真 invoke＋consumer readback |
| W1 checks | `REPLAY_CANDIDATE`（只在隔離 copy） | 真 raw/exit；不當 Native PASS |
| W1 reference | `BIND_EXISTING` 或缺件 `BUILD_MINIMAL` | 真 repo probe；不假存在 |
| G4 | `REUSE`（若真符合） | 需求/權利/tests/oracle |
| briefcheck | `BUILD_MINIMAL`（若 Owner 選定） | 03 fixture/oracle 凍結 |
| CODEX Native | `REUSE`／`ACTIVATE_HOST` | 本輪 session＋worktree/process 分離 |
| HERMES Compatibility | `DEFER` | 全波 CODEX 基線後另驗 install/route/session |
| product repo | `AUTHORITY_REQUEST` | 授權 checkout |
| Local CODEX Native OPS ECP | `ADOPTED` | 02 §03；`W0-OPS-NATIVE-20261125-01` |

### 08.3 Planned probe（下一輪 D1/O1；不填 actual）

```powershell
# $Repo 由 Owner 指定；未授權路徑不查
git -C $Repo rev-parse --show-toplevel
git -C $Repo rev-parse HEAD
git -C $Repo branch --show-current
git -C $Repo status --porcelain=v1 --untracked-files=all
git -C $Repo ls-tree -r --name-only HEAD
Get-Command codex,python,git -ErrorAction SilentlyContinue
python --version
git --version
codex --version
```

## 09｜B0 Sample decision 與 execution readiness

### 09.1 Sample decision

| 選項 | 條件 | 本輪狀態 |
|---|---|---|
| G4 | 真需求/程式/tests/權利/獨立於 SST/可逆 | `NOT_SELECTED`：無本地實體/需求/權利/tests |
| briefcheck | 無 G4 時的最小新 Generic CLI | **`SELECTED`**（`B0-SAMPLE-CODEX-20261125-01`）；本輪建置 |

選定理由與 G4 排除證據見附件 E9.1；briefcheck 的 R1–R4、fixture/expected exit 在 03。

### 09.2 `B0_EXECUTION_READINESS`（按效果分帳，非全包 admission）

| 效果／操作 | 狀態 | 理由 | 下一個合法動作 |
|---|---|---|---|
| Pack read／manifest 核對 | `READY` | 本輪六檔/SHA/JSON/link 自驗 | CODEX 讀 05＋04 |
| Source READ | `READY_WITH_ROOT` | 真 file＋SHA；需 Owner root | 指定 root/ACL |
| Guide ThinStart | `READY_WITH_PACK` | 04 是單一入口 | 真 pack path |
| Bridge 四 API | `PLANNED` | 本地 reference 未找到 | 真 Bridge probe／隔離實作 |
| DEV（briefcheck） | `PLANNED` | 真 repo/write-set/preimage 未取 | D1 probe／Owner 指定隔離 repo |
| OPS run/write/restore | `READY_WITH_LOCAL_SCOPE` | 本地 CODEX Native OPS ECP 已採納；真 principal/output root/recovery 已具 | 02 O1–O6；執行時填 actual |
| Challenge | `PLANNED` | fixture/oracle 未凍結 | Checker 凍結 bytes |
| FAR | `PLANNED` | 尚無真 Finding | B0 執行後 |
| G4 或 briefcheck | `briefcheck SELECTED` | `B0-SAMPLE-CODEX-20261125-01`；G4 無本地實體/權利 | 直接建置並執行 |
| W1 技術/施工 | `NOT_CLAIMED` | 需 W0 actual handoff | W0 後 |
| Release | `NOT_CLAIMED` | Publisher 未簽 | 原發布程序 |

**第一個合法接續動作**（不需新簽核）：在任一隔離工作區以 PowerShell 重算 `05` 的 pack_files SHA/bytes、解析 JSON、檢查相對入口，並跑 `Get-Command codex,python,git` 與版本 probe；此步只讀。其後直接依 Owner 規則選 G4/briefcheck 並執行 B0。

## 10｜Handoff／ChangeSet／W1 not_claimed

### 10.1 Claim 與交接邊界

| 欄 | 值 |
|---|---|
| Pack status | `PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION` |
| B0 | `NOT_RUN`；execution authorized but not executed |
| W1 technical | `NOT_CLAIMED`；需 W0 actual handoff＋consumer readback |
| W1 execution | `NOT_CLAIMED`；需上位受影採納及下一包一致 |
| Release | `NOT_CLAIMED`；Publisher 未簽 |
| 回寫 | W0 真 Raw 後 MASTER→PROG→PROJ→WM/Wn |

### 10.2 HANDOFF／CLOSEOUT／CHANGESET 最小欄（計畫）

| 工件 | 最小欄 |
|---|---|
| `HANDOFF` | `handoff_id, from_stage, to_stage, project/work_id, pack_ref+sha, candidate_ref+sha, source_refs, evidence_refs, target_consumer+version, actual_readback(argv/exit/raw/action), next_legal_action, owner, dependencies, resume_predicate, not_covered, w1_technical_readiness, w1_execution_readiness` |
| `CLOSEOUT` | identity／source/pack digest／baseline/head／new commit/tree；A/B/C disposition；14 WP disposition；24＋10 Case verdict 或 NotCovered；五方 individual/combined；Native actual＋OFF；Checker/oracle/FirstFail/LastGood；每個 claim 的 ceiling |
| `UPSTREAM_CHANGESET` | source/section/requirement/version/hash；old dependency；Finding raw；root cause；Decision（KEEP/REPLACE/REMOVE/OPTIONAL/DEFER）；new requirement；impact（PROG/PROJ/WM/Wn/consumer/ABI/case/分母）；regression；owner；`last_good_ref`；`resume_predicate` |

### 10.3 回寫順序（未來，不在本輪執行）

1. W0 真 Raw→FirstFail→responsibility→original requirement/case→ChangeCone 建 ChangeSet。
2. 先回寫 MASTER 受影段（共通法位、Product、Architecture/ADR/Seam、Program、WnM、FileContract、W0、分波、Delta、guard/claims/CR）。
3. 再回寫 PROG-00 有效責任、7 Seam、六檔、分母、CR。
4. 再平行回寫五 PROJ 的非重疊受影段。
5. 最後跨冊一致性：版本、欄位、case、consumer、未受影內容、無源 mandatory。
6. WM/W0M/W1M..W4M 只在真 material delta 後更新。

## 11｜Remaining gaps 與最小 Owner 決策

1. 真 product repo/root/HEAD/write-set/preimage（Repo Owner）。
2. HERMES Compatibility install/route/session；移至全波 CODEX 基線後（Host Owner）。
3. 真 fixture/oracle/independent checker 的產品級擴充（Case/Checker Owner）。
4. W1 14 HOLD＋R3-CR requalify；MASTER/PROG/PROJ/WM 未回寫（W1/Program Owner）。
5. 其他 Host（GPT CHAT／GPT WORK／HERMES）實際掛載／消費驗收（各 Host Owner）。

**已由本次 Owner 裁決，不再請求**：B0 sample 選擇（CODEX 自主）、Original OPS ECP #5（本地 CODEX Native OPS ECP 承接）、主用升格與多操作受界施工授權。其餘只在真外部權限/越界/發布時集中回 Owner 一次。

