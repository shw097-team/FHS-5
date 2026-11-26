# FHS-5_PLP W2 Native-first｜HERMES 修補輪｜證據型附錄

**附錄身份**：`FHS5-PLP/W2/PACK-NF-20261126-r3/APPENDIX`
**主體包**：`FHS-5_PLP_W2_NATIVE_FIRST/`（5 MD＋1 JSON＋25 assets；`artifact_id=FHS5-PLP/W2/PACK-NF-20261126-r3`，candidate `W2-NF-r3-CODEX-PRIMARY`）
**外置封存（本檔記錄、05 不自含）**：`05_W2_SOURCE_MANIFEST.json` raw SHA-256 ＝ `81daac8ff3f47566d18cc7ebdaee9625ff5ca000b71caac3226841b124f6099b`，65377 bytes
**日期**：2026-11-26（Asia/Taipei）　**輪次 ID**：`HERMES-F5-W2-PACK-NF-FINAL-r1`
**本附錄性質**：證據與選用記錄，**不是**第七份規範檔，也不是產品驗收、不是 Checker verdict、不是 Grant。

## 0｜Claim ceiling（第一屏）

| 維度 | 本輪值 | 不宣稱 |
|---|---|---|
| 文件層選用 | `W2_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（承接本輪 Owner 預授權） | 產品 PASS |
| 原域 Issuer 收據 | `owner_ref = null`（未取得） | `ORIGINAL_READER_ACK` |
| 任何 op 的 admission | `NOT_ADMITTED` / `permission_state=NONE_GRANTED` | `W2_EXECUTION_READY` |
| 產品效果 | 無（本輪未執行任何 DEV/OPS） | `NATIVE_PASS` |
| 獨立驗收 | 無（本輪的 review 是同 principal、不同 session） | `INDEPENDENT_PASS` |
| 發布 | 見 §9（Git push ≠ Release） | `RELEASED` |
| 波結案 | 未宣 | `W2_NF_VALIDATED`、`M-DONE` |

一句話：**本輪把一份作者候選文件包修到「文件層可施工、可檢測、可追溯」，並依 Owner 指示選為 W2 主用依據；產品效果、獨立驗收與發布都還沒發生。**

## 1｜本輪做了什麼／沒做什麼

**做了**

1. 凍結 r1 前像（31 檔逐檔 byte-identical 複製，原樹未動）。
2. 以**自建**驗證器（非作者 `validate_pack.py`）執行 33 項文件層斷言：r1 28/28、r2 28/28、r3 33/33。
3. 以 14 個負向 mutation 證明驗證器 fail-closed：三代皆 14/14 偵測、來源樹前後 digest 不變。
4. 兩輪修補：r1→r2（D-01..D-06）、r2→r3（獨立 reviewer 25 項發現中的 23 項；2 項已於 r2 修）。
5. 委派**另一個 session** 做對抗式覆核（同 principal，非同 principal），其 verdict 為 `REWORK_REQUIRED`；本輪據以完成第二輪修補。
6. 產出本附錄、外置封存與 `PACK_POINTER.json`。

**沒做**

1. 未執行任何 W2 產品 DEV/OPS、未 `codex exec`、未發 Grant、未改 W1 sealed delivery。
2. 未重跑 W0 44 receipts 或 W1 79 tests；只引用其 recorded 值並標明未重驗。
3. 未取得原域 13+3 的 typed receipt（`reader_state=UNBOUND` 已逐列聲明）。
4. 未對抗式覆核者之外的第三方取得獨立 Checker verdict。
5. 未 merge 至 `main`、未 tag、未改 release；push 狀態見 §9。

## 2｜Owner 預授權記錄與其界線

| 欄位 | 值 |
|---|---|
| `decision_kind` | `HUMAN_OWNER_PREAUTHORIZED_CONDITIONAL_PRIMARY_AND_SCOPED_CONSTRUCTION` |
| 決策來源 | 本輪使用者指令（要求執行 `FHS-5_PLP_W2_CODEX_Native-first_HERMES_啟動薄PROMPT`）；其原文載明「使用者已預授權合格新版直接升格／授權／宣達『主用＋可執行施工』，不再重請同一決策；依控制包 §04.2 綁定 final identity/05 SHA/適用 W2M/受影規格/作用域，actual ACL/逐 op preconditions 仍需下一手核實，不冒 Grant/W2_EXECUTION_READY/Native/Independent/Release」 |
| 綁定對象 | 本附錄所記 `artifact_id` 與 `05` raw SHA（見首屏） |
| 生效條件 | 本附錄存在且其封存 digest 與實際 `05` bytes 相符；不符則回到 `PACK_SELECTION_UNVERIFIED` |
| 不覆蓋 | 原域 Issuer receipt、任何 op 的 ACL/principal/preimage、`W2_EXECUTION_READY`、產品效果、獨立驗收、Release |
| 撤權 | Owner 隨時可撤；scope/Repo/Host/effect 變更或安全發現即失效 |

**精確語義**：`owner_ref=null` 記錄的是**原域 Issuer 收據未取得**，與本選用是兩個不同欄位（`00` §4.2 規則 7–8）。issuer 在 W2 範圍內是**唯一 Human Owner 的授權責任**（WM0 §00.2.1），不是未現身的第三方；原域 typed receipt 若存在則另欄保存，不存在則 `UNBOUND`。

## 3｜來源驗證（本機實算，非原域接收）

演算法：SHA-256 over raw bytes，無編碼正規化、不以 Git blob SHA 代替。root 解析依 `05.source_roots`（`S`＝Downloads 唯讀來源根；`WORK`＝作者工作根）。

| source id | 狀態 | bytes | sha256 前 16 |
|---|---|---|---|
| `M` | BYTE_IDENTICAL | 325511 | 2026da4b847c1368 |
| `B00` | BYTE_IDENTICAL | 126626 | cdd1d76ec20fad19 |
| `B01` | BYTE_IDENTICAL | 68023 | aa823374dabce521 |
| `B02` | BYTE_IDENTICAL | 65006 | 37022f33e5a67ad3 |
| `B03` | BYTE_IDENTICAL | 56268 | a13a9df4252a557a |
| `B04` | BYTE_IDENTICAL | 57182 | fb529a784b7d929f |
| `B05` | BYTE_IDENTICAL | 67845 | 794d91cc80807158 |
| `WM0` | BYTE_IDENTICAL | 108861 | c9b1ca9bbcd5ce87 |
| `WM1` | BYTE_IDENTICAL | 99289 | a91c4ed36cc29773 |
| `WM2` | BYTE_IDENTICAL | 67015 | 2b98be9656517212 |
| `C0` | BYTE_IDENTICAL | 21927 | 23cfa1f640227c0f |
| `H0` | BYTE_IDENTICAL | 3265 | 21ed226738abbd75 |
| `C1` | BYTE_IDENTICAL | 9231 | 2954523723b82752 |
| `H1` | BYTE_IDENTICAL | 1891 | ffea91770c055bf8 |
| `PLAN` | BYTE_IDENTICAL | 123698 | f92213a1aabcde15 |
| `CONTROL` | BYTE_IDENTICAL | 32402 | 7f0de5f58b708094 |
| `W1-05` | BYTE_IDENTICAL | 35959 | 61f34a08fa63190b |
| `W2-DRAFT-MANIFEST` | BYTE_IDENTICAL | 4611 | c251ebc0f9ad292f |
| `W2-INBOUND-RECEIPT` | BYTE_IDENTICAL | 11018 | 2633ad90af8ddc33 |
| `W2-RECEIVE-RECEIPT` | BYTE_IDENTICAL | 5560 | 896e84632c3c6c8b |
| `W1-DELIVERY-SEAL` | BYTE_IDENTICAL | 566 | f177229271e4ec60 |
| `W1-RECEIVER` | GIT_PATH_PIN | 9336 | c666740268cce914 |
| `W1-INBOUND` | GIT_PATH_PIN | 11374 | 391dd7072ca84ab3 |
| `W1-GUIDE` | GIT_PATH_PIN | 13516 | 90e9b6b5fbd596ca |

**統計**：24 源中 21 個 byte-identical、3 個 git-path pin（未重開 bytes，`read_level=RECORDED_PIN_NOT_REOPENED`）、0 absent、0 mismatch。
**source_set_sha256** 重算 ＝ `921de70ca5f273d9bba0ed0d022bb7595e8824d7595e8373b2c43d5ccbbaa044`（與宣告相符；僅用 `id|sha256|bytes`，故 `CONTROL` 換路徑不改變該值）。

**已修的來源定位缺陷**：`CONTROL` 宣告路徑指向 `W2/…`，實際檔案已被移至 `W2/OLD/…`（bytes 32402、SHA 相同）。r2 起改正路徑並記 `relocated_from`，digest 與 bytes 不動。

## 4｜三版血緣與逐檔 digest

| 版本 | artifact_id | 05 raw SHA-256 | 角色 |
|---|---|---|---|
| r1 | `FHS5-PLP/W2/PACK-NF-20261126-r1` | `738cf348da5f093131cef890f52127143872c5ea58104f9020e6586df33f46bd` | 作者候選（GPT WORK） |
| r2 | `FHS5-PLP/W2/PACK-NF-20261126-r2` | `a69a25b69eb98c505b55b9547d103cb0c21f230525360fd3f6ba67f04f206669` | 本輪第一修補（定位/指涉/身分） |
| r3 | `FHS5-PLP/W2/PACK-NF-20261126-r3` | `81daac8ff3f47566d18cc7ebdaee9625ff5ca000b71caac3226841b124f6099b` | 本輪第二修補（獨立覆核 23 項） |

| 檔案 | r1 | r2 | **r3** | bytes |
|---|---|---|---|---|
| `00_W2_PI_PD.md` | 49cb8850fcc7 | 2d96219ab634 | **87899d130562** | 60853 |
| `01_W2_DEV_ECP.md` | 4573a65c2b8d | a76e7b785577 | **8c70e65eb020** | 21795 |
| `02_W2_OPS_ECP.md` | 3e543030a991 | 54fa9a56ed1d | **3716a5041155** | 19372 |
| `03_W2_TQAEP.md` | 82dcf6e666c4 | a040b2dba1bd | **f4ee27300421** | 22289 |
| `04_W2_START_THIN_PROMPT.md` | 9e81a80053d4 | a061683461da | **b62a62e8a43b** | 7104 |
| `05_W2_SOURCE_MANIFEST.json` | 738cf348da5f | a69a25b69eb9 | **81daac8ff3f4** | 65377 |
| `assets/cases/case_index.json` | b85ff62161fb | b85ff62161fb | **b85ff62161fb** | 6325 |
| `assets/fixtures/W2-AUTH-01.json` | 80502748eece | 80502748eece | **80502748eece** | 893 |
| `assets/fixtures/W2-DELTA-01.json` | 73452d47f9b4 | 73452d47f9b4 | **cb61b06f0055** | 3521 |
| `assets/fixtures/W2-DEV-01.json` | af2b2df7a4ab | af2b2df7a4ab | **dea304084db5** | 3380 |
| `assets/fixtures/W2-DEV-02.json` | 99f910663b7f | 99f910663b7f | **99f910663b7f** | 940 |
| `assets/fixtures/W2-EFFECT-01.json` | 3492f8cc0b77 | 3492f8cc0b77 | **3492f8cc0b77** | 821 |
| `assets/fixtures/W2-OPS-01.json` | 03494b3cca8e | 03494b3cca8e | **03494b3cca8e** | 1492 |
| `assets/fixtures/W2-OPS-02.json` | 168e857025f5 | 168e857025f5 | **168e857025f5** | 834 |
| `assets/fixtures/W2-R3-01.json` | 5c721f1524cb | 5c721f1524cb | **5c721f1524cb** | 3032 |
| `assets/fixtures/W2-R3-02.json` | 9867a71507bc | 9867a71507bc | **9867a71507bc** | 1124 |
| `assets/fixtures/W2-R3-03.json` | 8566b623ab3d | 8566b623ab3d | **8566b623ab3d** | 978 |
| `assets/fixtures/W2-R3-04.json` | 7c8ba861cbce | 7c8ba861cbce | **7c8ba861cbce** | 837 |
| `assets/fixtures/W2-RUNNER-01.json` | 7ea614b4f40f | 7ea614b4f40f | **7ea614b4f40f** | 768 |
| `assets/oracles/W2-AUTH-01.json` | 6365e89546a7 | 6365e89546a7 | **6365e89546a7** | 880 |
| `assets/oracles/W2-DELTA-01.json` | 260a96693420 | 260a96693420 | **155dc1054bcc** | 1221 |
| `assets/oracles/W2-DEV-01.json` | 668f332e4a41 | 668f332e4a41 | **48df3438c53b** | 1433 |
| `assets/oracles/W2-DEV-02.json` | 4d29d6270963 | 4d29d6270963 | **4d29d6270963** | 841 |
| `assets/oracles/W2-EFFECT-01.json` | a1e4c91f86e9 | a1e4c91f86e9 | **a1e4c91f86e9** | 838 |
| `assets/oracles/W2-OPS-01.json` | 9d5e723084ad | 9d5e723084ad | **9d5e723084ad** | 1160 |
| `assets/oracles/W2-OPS-02.json` | a5d8732e4271 | a5d8732e4271 | **a5d8732e4271** | 831 |
| `assets/oracles/W2-R3-01.json` | 970ec9d73646 | 970ec9d73646 | **970ec9d73646** | 880 |
| `assets/oracles/W2-R3-02.json` | 3b2ed871b64c | 3b2ed871b64c | **3b2ed871b64c** | 760 |
| `assets/oracles/W2-R3-03.json` | 1f9d9e155317 | 1f9d9e155317 | **1f9d9e155317** | 794 |
| `assets/oracles/W2-R3-04.json` | d26358c730d2 | d26358c730d2 | **d26358c730d2** | 859 |
| `assets/oracles/W2-RUNNER-01.json` | 22931f33af7a | 22931f33af7a | **22931f33af7a** | 805 |

> `05` 在三版間被重新序列化（`indent=1`），因此它的 bytes 差異大於語義差異；語義 diff 已逐鍵檢查，且 `pack_files`/`assets`/`cases` 的 digest 以最終 bytes 重算。`source_set_sha256` 三版相同。
> 行尾：全 pack 為 LF（CR byte count = 0，實測）。交付分支以 `.gitattributes` `* -text` 固定，避免 Git 正規化改變已雜湊的 bytes。

## 5｜缺陷登記與修補

### 5.1 第一輪（r1→r2；自建檢測發現）

| ID | 級別 | 缺陷 | 修補 |
|---|---|---|---|
| D-01 | MAJOR | `05.sources[CONTROL].path` 不解析（檔已移至 `W2/OLD/`） | 改正路徑；bytes/SHA 不變；記 `relocated_from` |
| D-02 | MINOR | `03` §5.2 的 Case 欄引用 op id `OPS-06`（非 12 原案之一） | 改引 `OPS-01` ＋ UNKNOWN 子例 `OPS-O06`／N06 |
| D-03 | COSMETIC | `00` §2.1 誤植「9 六檔 single truth」 | 刪去多餘 `9 ` |
| D-04 | MINOR | `05.j_seam_locators[SM01..SM07]` 主定位指 `§6.1`（實為 J1） | 改指 `§2.2` seam 表 |
| D-05 | COSMETIC | `00` §6.3 的 J3-T01..06 為散文，J1/J2 為表 | 改為表，可檢索性一致 |
| D-06 | — | 版本身分未反映修補 | r1→r2 identity、lineage、readiness 同步 |

### 5.2 第二輪（r2→r3；獨立 session 覆核發現）

覆核 verdict `REWORK_REQUIRED`：blocking 2、major 14、minor 9。下表為逐項處置（`Q*` 為覆核編號）。

| ID | 級別 | 缺陷（覆核所述） | 處置 |
|---|---|---|---|
| Q3-01 | BLOCKING | 16 列 `required_when` 被壓成同一句，使 Checker(B11)/Publisher(B12) 成為效果的**前置** | 逐列改寫（16 個不同值）；B11 明列 `POST only`、B12 `RELEASE only`；B10 的 post readback 明列非前置 |
| Q1-01 | BLOCKING | r2 宣告 `PRIMARY_AUTHORIZED…` 卻同時 `owner_ref=null`，讀起來像已完成採納 | 明列狀態語義、把綁定移往外置附錄、加 `PACK_SELECTION_UNVERIFIED` 回退；`owner_ref` 與選用分欄說明 |
| Q1-03 | MAJOR | 正文要求外置 seal，但包內沒有附錄 | 本附錄交付；封存 digest 見首屏 |
| Q1-02 | MAJOR | 同一根目錄下有兩套完整而互異的 00–05，無指標 | r1/r2 前像移出交付根並改名；加入 `PACK_POINTER.json` 指明 canonical |
| Q1-04 | MINOR | `W2_TECHNICALLY_READY` 未列入不宣稱 | 加入 `not_claimed`，並註明是上游 recorded 值、本包不重驗 |
| Q2-01 | MAJOR | `W2-DEV-01` fixture 用 G4/`tag_normalizer` 路徑，與 ADR-W2-04 及 `01` §5.1 唯一 write set 衝突 | fixture/oracle 改綁 `01` §5.1 的 2 target（1 MODIFY＋1 ADD）；新增 `write_set_binding`、禁 G4 類比路徑、delete target 清空 |
| Q2-02 | MAJOR | `W2-DELTA-01` fixture 兩期數值全同，答案被 fixture 預先決定 | 加 `same`/`delta` 兩個變體（後者僅 `world_raw_sha` 不同）、`fixture_never_sufficient=true`、oracle 要求兩個判定都對 |
| Q2-03 | MAJOR | 24 個 W0 原案被聚合成「44 receipts」，16 個 RETAIN ID 消失，T24 disposition 被反轉 | 新增 §3.2B 逐案 24 列（Type/disposition 依 WM2 §02.3），T24 改回 `REUSE` |
| Q2-04 | MAJOR | 15→6 的 `02_ORIGINAL_CONTRACT_REFS.json` 對映缺 `sha/span/reader_state` 三欄 | 16 列補 `source_sha/span/reader_state`（明示 null/UNBOUND 與理由）；該投影列標 `PARTIAL_UNBOUND` |
| Q2-05 | MINOR | `F5-CR24` 掉「五份」量詞 | 還原 |
| Q2-06 | MINOR | RQ-04 掉「W1 link/reparse 部分 NOT_VERIFIED」、RQ-05 掉「有語義缺口」 | 兩處還原 |
| Q2-07 | MINOR | 同一 FirstFail 兩種拼法（`WRITESET_UNBOUND`／`WRITE_SET_UNBOUND`）當機器 token | `00` §0.3 宣告 canonical 與 alias；oracle 兩種皆接受 |
| Q2-09 | MINOR | 25 個 asset 共用同一個 role 字串 | 改為 `case_fixture`／`case_oracle`／`case_index`，並帶 `case_id` |
| Q3-02 | MAJOR | 三條邊由 `AUTHOR_DOC_ORDER`/`UNVERIFIED` 升 `HARD` 卻無出處 | 每邊新增 `wm2_class` 與 `hardening_reason`；`00` 表加「WM2 §07.7 原類」欄 |
| Q3-03 | MAJOR | 宣告 `P02→P03 HARD` 卻同時交付未 bind 的 01/02 | 明列：該邊約束 **exec bind 進 P05**，不約束 P03 草稿（PLAN §03.3 許可） |
| Q3-04 | MAJOR | O03 一邊自我補償、一邊要求 O04 讀 post，兩種互斥順序並存 | 定為單向：O03 只產出、**不補償**；O04 讀 post 判定；O05 才補償並讀回 pre-state；`04` 同步 |
| Q3-05 | MAJOR | P03 階段要求 ChangeSet（P06 產物）與 Bridge context | J2 拆 `J2-pre`／`J2-post`；ChangeSet 只在 post；direct 模式以 `DIRECT_CONTEXT` 代替 |
| Q3-06 | MINOR | OPS receipt 無 checker 欄，Checker/Consumer 在 OPS 域塌成一個 | receipt 加 `checker_id`／`checker_receipt_sha256`，並明列與 consumer 為兩個 distinct receipt |
| Q4-01 | MAJOR | B07/B08 的 producer 寫「Original Issuer」，而該實體在本包記錄為 null | 依 WM0 §00.2.1 明列 issuer ＝ 唯一 Human Owner 的授權責任；原域 receipt 另欄 |
| Q4-02 | MAJOR | policy epoch 無可取得 producer，且禁造 → OPS 永久停 | 定義 `epoch_state=NOT_DECLARED_BY_HOST`（附 probe 原始輸出的事實記錄，非造值） |
| Q4-03 | MAJOR | OPS 的 receiver 是 DEV 產物卻無跨域邊；替代品「Native direct consumer」無定義 | 定義 `R2` receiver（DEV-D04 產物或 D02 選定的 thin wrapper）；新增 `DEV-D04 → OPS-O03` HARD op-edge |
| Q4-04 | MAJOR | J2 要求 Bridge 的 42/17/25 分帳，direct 模式無 token 可記 | 定義 `BRIDGE_RESPONSE_ABSENT`；禁止以本地 24 列冒算，也禁止因此拒收合法 direct op |
| Q4-05 | MINOR | `00` §0.4 以完成式敘述檢測與覆核已做 | 改寫為判準（未達不得宣），並指向本附錄 |
| Q2-08 | MINOR | （r2 已修）`OPS-06` 非存在 Case | 已於 D-02 修 |
| Q3-07 | MINOR | （r2 已修）`SM01..SM07` 定位錯指 §6.1 | 已於 D-04 修 |

**未採納的覆核意見（具名）**：無。覆核的 25 項全部接受並處置；其中 2 項在 r2 已修，故 r3 實際動 23 項。

## 6｜實際執行的文件檢測（DOC_MUTATION_EXECUTED）

驗證器：`check/validate_pack.py`（自建，33 斷言，非作者實作）。負向 harness：`check/run_mutations.py`（14 mutations，每個在獨立副本上執行；來源樹前後 digest 比對）。

### 6.1 r3 斷言結果（33/33 PASS）

| 檢查 | Verdict | 內容 |
|---|---|---|
| `PKG01-01` | PASS | six canonical files present |
| `PKG01-02` | PASS | all six decode as UTF-8, no BOM |
| `PKG04-01` | PASS | strict JSON ok (no duplicate keys) |
| `PKG04-01b` | PASS | no NaN/Infinity literals |
| `PKG01-03` | PASS | identity consistent across 5 MD + 05 |
| `PKG01-04` | PASS | pack_files digests/bytes match actual |
| `PKG01-05` | PASS | sources verified byte-identical: 21 ok, 3 git-pin, 0 absent, 0 mismatch |
| `PKG01-06` | PASS | source_set_sha256 recomputes |
| `PKG01-07` | PASS | every declared source path resolves at its declared root |
| `PKG02-01` | PASS | 16 requirement rows, all 15 required fields |
| `PKG02-02` | PASS | 12 original case IDs exact, each with fixture/oracle/runner/status |
| `PKG02-03` | PASS | 6 WP / 6 ACC / 6 CODEX-FUO / 7 Seam / D01-D08 all present in 00 |
| `PKG02-04` | PASS | 14 holds / 6 special holds / 37 CR / 7 RQ retained |
| `PKG02-05` | PASS | 15->6 projection has 15 rows |
| `PKG02-06` | PASS | J1/J2/J3 = 18 subcases, N01-N12 = 12 |
| `PKG03-01` | PASS | DAG acyclic (topological order covers all nodes); no POST edge reused as reverse HARD |
| `PKG03-02` | PASS | each of 6 WPs joins 00 5.1 row + 00 5.3 dry-consume row + a real consumer artefact |
| `PKG03-04` | PASS | required_when is per-row; Checker/Publisher are POST/RELEASE, not effect preconditions |
| `PKG03-05` | PASS | dag.op_edges reference operation sections that exist in 01/02 |
| `PKG03-06` | PASS | every DAG edge carries its upstream class |
| `PKG04-02b` | PASS | asset roles distinguish fixture/oracle/index |
| `PKG02-01b` | PASS | requirement rows carry source_sha/span/reader_state |
| `PKG03-03` | PASS | each case has a section in 03 with not_covered |
| `PKG04-02` | PASS | 25 assets exist, digests match, set equals 12 fixtures + 12 oracles + case_index |
| `PKG04-03` | PASS | no traversal/absolute locators in manifest |
| `PKG04-04` | PASS | 05 does not embed its own digest; manifest_self_hash=EXTERNAL_RECORD_ONLY |
| `PKG04-04b` | PASS | 05 is self-excluded from pack_files |
| `PKG04-05` | PASS | draft=false (official, not DRAFT variant) |
| `PKG05-01` | PASS | J1 section present with short-circuit-before-consume rule |
| `PKG05-02` | PASS | Guide nine keys all named in 00 |
| `PKG06-01` | PASS | 04 has all six sections |
| `PKG06-02` | PASS | 04 carries stop/resume and an explicit not-applicable boundary |
| `PKG06-03` | PASS | exactly one start entry |

### 6.2 負向 mutation（14/14 偵測；來源樹未動）

| ID | mutation | 預期失敗檢查 | exit | 實際失敗檢查 |
|---|---|---|---|---|
| POS | none (positive control) | none | 0 | — |
| M01 | flip one byte inside 01 (silent content drift) | PKG01-04 | 1 | PKG01-04 |
| M02 | duplicate JSON key 'scope' | PKG04-01 | 1 | PKG04-01 |
| M03 | NaN literal in case_count | PKG04-01b | 1 | PKG04-01b |
| M04 | path traversal in an asset locator | PKG04-03 | 1 | PKG04-02, PKG04-03 |
| M05 | drop case W2-R3-04 from cases[] | PKG02-02 | 1 | PKG02-02 |
| M06 | drop requirement W2-B12 (Publisher) from requirements[] | PKG02-01 | 1 | PKG02-01 |
| M07 | tamper pack_files sha256 for 00 | PKG01-04 | 1 | PKG01-04 |
| M08 | draft=true (DRAFT variant posing as official) | PKG04-05 | 1 | PKG04-05 |
| M09 | declare manifest_self_hash as an embedded digest | PKG04-04 | 1 | PKG04-04 |
| M13 | list 05 itself among pack_files (self-entry) | PKG04-04b | 1 | PKG01-04, PKG04-04b |
| M10 | identity drift in 02 only | PKG01-03 | 1 | PKG01-03, PKG01-04 |
| M11 | delete one oracle asset | PKG04-02 | 1 | PKG04-02 |
| M12 | add P06->P01 HARD edge (cycle) | PKG03-01 | 1 | PKG03-01, PKG03-06 |

**正向控制（POS）**：未變異副本 exit 0、無失敗檢查 → 證明偵測不是「恆真」。
**來源未動**：每次執行前後對來源樹做全樹 digest，`source_untouched = True`。
**兩代皆測**：r1 與 r2 各 14/14（見 `check/results/mutations_r1.json`、`mutations_r2.json`）。

### 6.3 一個誠實的更正

初次執行時本驗證器把 `PKG03-02`（WP dry-consume）判成 FAIL，理由是「`01`/`02` 內找不到字串 `WM2-P06`」。查核後確認是**驗證器謂詞寫錯**：dry-consume 要求的是「00 的 WP 列＋00 §5.3 列＋有真實 consumer 產物解析到該 WP」，不是要求在 op 檔內出現 WP 字串（`WM2-P01` 本就由 cases 解析，不由 DEV/OPS op 解析）。已改成正確謂詞並在程式中留註；此更正**放寬的是錯誤的謂詞，不是放寬缺陷**——新謂詞仍要求三個條件同時成立，且逐 WP 印出解析來源。

同理，`M09`（把 manifest 自身 digest 嵌入檔案）在設計上**無法構造**：替換 digest 會改變 digest，兩趟不能收斂——這正好證明 `manifest_self_hash=EXTERNAL_RECORD_ONLY` 是唯一正確形狀。故該 mutation 改為兩個可構造的負例（宣告內嵌 digest、把 05 列進 pack_files）。

## 7｜REV01..06 覆核紀錄

| REV | 範圍 | 本輪如何做 | 結果 |
|---|---|---|---|
| REV-01 | 高保留／需求來源 | 逐 ID 計數＋與 WM2 §02.3/§03.1、PLAN §13 對讀；24 W0 案逐案表 | 修 Q2-03/Q2-04/Q2-05/Q2-06 |
| REV-02 | Native-first／最小治理 | 檢查是否新增 Runtime/Queue/Issuer；direct route 是否仍可用 | 未新增；direct 分支補 `DIRECT_CONTEXT`/`BRIDGE_RESPONSE_ABSENT` |
| REV-03 | 三 SPEC／ECP／TQAEP 可施工性 | 每 op 是否具 producer/取得途徑/expected/recovery/stop；`required_when` 逐列 | 修 Q3-01/Q3-04/Q4-01/Q4-02/Q4-03 |
| REV-04 | 跨檔／跨波 | 身分一致、DAG 邊類與出處、J1–J3 落點、15→6 | 修 Q3-02/Q3-03/Q3-05 |
| REV-05 | 證據／安全／獨立 | 33 斷言＋14 mutation；Checker/Consumer 是否分立 | 修 Q3-06；新增多項機器檢查 |
| REV-06 | 自主收斂／薄入口 | `04` 六段、單一入口、stop/resume、有限 loop | 修 Q4-05；`04` 與 `02` 順序對齊 |

**獨立性聲明**：§5.2 的第二輪覆核由**另一個 session** 執行（不同 context、唯讀、不得改檔），但**同 principal／同模型**。因此它可作為「非同一次撰寫的對抗式覆核」，**不可**作為 `INDEPENDENT_PASS`（原政策若要求不同 principal，須真不同 principal）。

## 8｜數字對帳（避免互代）

| 量 | 值 | 不可拿來代替 |
|---|---|---|
| 文件層斷言 | r1 28/28、r2 28/28、r3 33/33 | 產品測試通過數 |
| 負向 mutation | 14/14 ×3 代 | 「測試很多」不等於產品可證 |
| 來源 | 24 源：21 byte-identical、3 git-pin、0 absent/mismatch | 原域接收 |
| 義務分母 | 16 前件、12 原案、6 WP、6+6 ACC、7 Seam、18 J 子組、12 N、15 投影、14 HOLD＋6 專項、37 CR、7 RQ | 不是 PASS 數，是**分母保留** |
| 產品狀態 | `NOT_RUN` ×12 案；`NOT_ADMITTED`；0 次 effect | 任何 PASS/Ready |
| 覆核 | 1 次獨立 session 覆核（同 principal） | `INDEPENDENT_PASS` |
| 版本 | r1／r2／r3 三份 05 digest 各異 | 不可互引為同一 candidate |

## 9｜交付結構與發布狀態

```
R = C:\Projects\Agent_Workspace\FHS-5_Workspace\20_W2_PACK_HERMES_FINAL_20261126
  PACK_POINTER.json                     ← 指標：canonical 是哪一份
  00_frozen_input/r1/…                  ← r1 前像（唯讀，非 canonical）
  00_frozen_input/r2/…                  ← r2 前像（唯讀，非 canonical）
  W2_Native-first_HERMES_主用修補_交付/
    FHS-5_PLP_W2_NATIVE_FIRST/          ← canonical r3（5 MD＋1 JSON＋assets）
    FHS-5_PLP_W2_Native-first_HERMES_修補證據型附錄.md   ← 本檔
  check/                                ← 驗證器、mutation harness、results
  publish/repo/                         ← 交付分支的工作 clone
```

**發布狀態**：見下節
Git push 不等於 Product Release；本輪不 tag、不 merge `main`、不改 default branch。

## 10｜下一個合法動作

1. **Owner**：以本附錄首屏的 `artifact_id` ＋ `05` raw SHA 確認選用（或撤權）。確認後本包的 `PRIMARY_AUTHORIZED…` 才有外部依據；否則維持 `PACK_SELECTION_UNVERIFIED`。
2. **CODEX（下一手）**：以 `04_W2_START_THIN_PROMPT.md` 啟動；第一個動作是 P01/P02 的可信 read/bind，不是寫入。
3. **第一個寫入前必須具備**（缺一即停該 op，不降級）：Owner 的真 scope/decision、repo root/HEAD/ACL、exact preimage/absence、`01` §5.1 的 exact write set、reverse 能力；OPS 另需 host/principal、`epoch_state`（真值或合法 `NOT_DECLARED_BY_HOST`）、`R2` receiver、output root、補償能力。
4. **不可跳過**：J1 先驗後消費（拒收短路、零 product call）、`J2-pre`／`J2-post` 分離、O03 不自我補償、Checker 與 Consumer 兩個 distinct receipt。
