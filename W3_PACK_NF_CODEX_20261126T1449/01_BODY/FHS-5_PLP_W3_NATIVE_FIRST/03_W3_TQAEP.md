# FHS-5_PLP｜W3｜TQAEP｜測例、Oracle、Assurance

**artifact_kind**：`WaveControlPack / TQAEP`
**subject_id**：`FHS-5_PLP/W3/CONTROL_PACK`｜**scope**：`W3-NF-01`
**artifact_id**：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`｜**version**：`r2`
**selection_state**：`PACK_PRIMARY_SELECTED`（決策 `W3-PACK-PRIMARY-20261126-01`）
**claim_ceiling**：`PACK_PRIMARY / LOCAL_DOCUMENT_VERIFIED / PACK_EXECUTABLE`
**本檔 Effect**：`SOURCE_READ + LOCAL_DOCUMENT_CHECK + BOUNDED_SMOKE`；正式產品 runner 仍依 `01/02` late-bind
**本檔不授予**：任何產品 runner、任何 original case 執行、任何 Checker verdict

> **一句話**：本檔把 W3 的 16 原案逐案寫成可被 runner 消費的契約。每一案的 fixture／oracle 都是 **PROPOSED_DESIGN**，`observed=null`、`verdict=NOT_RUN`；真 oracle 必須由 Case Owner 在看到結果前用真 bytes 凍結。沒有真 runner／oracle／fixture 的案，只能 `NOT_RUN`／`NotCovered`，不得填假 exit、假 raw 或假 PASS。r2 另加 §12 的 DOC/SMOKE 層，證明材料可消費；它不是 16 原案的產品 PASS。

---
# 01｜分母、觀察層與 Oracle freeze rule

## 01.1 分母分帳

| 集合 | 數量／ID | 本包處置 |
|---|---|---|
| W3 原案 | 16（§03） | 當期主驗收；required 未跑則 partial |
| W2 原案 | 12（`W2-DEV-01/02`、`W2-OPS-01/02`、`W2-EFFECT-01`、`W2-AUTH-01`、`W2-RUNNER-01`、`W2-DELTA-01`、`W2-R3-01..04`） | upstream requalify；不併入 W3 16 |
| W0 | SAMPLE10＋`F5-W0-T01..24`＋`NF-T01..10` = 44 | 只按真同位來源復用；不重跑、不抵 W3 |
| Challenge 原域 | `EC-FR01..16`、`EC-WP01..09`、`EC-T01..26`、`EC-X27..36`（26+10）、local47、C16/F5-T12 | 功能/WP/Case/例外/local 分帳；未得 `NOT_RUN`／`C16_NOT_RUN` |
| FAR 原域 | `FAR-FR01..17`、`FAR-WP01..12`、`FAR-T01..20`、`FARP30`（10 POS/12 NEG/3 EDGE/5 SEC）、local35（25+10）、`FAR-Q0..Q10`、RQ0–8、十 Advice | 當期適用能力需測；35 不抵 20/30 |
| Guide 原域 | `CG-R2-REQ01..16`、`U01..26`、`CG-SEM01..17`、local50 | Touch2/九鍵當期適用；原 17/三 Host 另案 |
| Bridge 原域 | `PCB-FR01..17`、`A-PCB-001..022`、`AV3-001..030`、38+28 | 四 API 及 W3 新材料消費；原 66 獨立 |
| TPM/Reviewer | `F01..14`、`U01..16`、QA26、35 tool | 四契約/真 reviewer；QA26 未跑不抵 |
| Program/FHS | `U-001..056`、`R01..24`、`P00-01..06`、FHS 22/36/50/39/96/192/485、1011=576 identified+435 unresolved slots | Generic 不強制 485；W4 依 Profile 真適用 |
| 跨波 | `N01..12`、`RQ01..07`、14 HOLD、`R3-CR01..12`、`F5-CR01..25` | 保原 namespace；CR/RQ/HOLD 非測例 |

## 01.2 觀察層

| 層 | 意思 | 可支持 |
|---|---|---|
| `DOC` | 文件存在、可 parse、欄位一致 | 作者文件驗收 |
| `DESIGN` | 作者設計 fixture/oracle/predicate | 可施工性，不是產品結果 |
| `COMPONENT` | 單一函式/reader 真跑 | 元件行為 |
| `INVOCATION` | 真 process/argv/exit/raw | 執行契約 |
| `E2E` | 多角色材料真消費 | 產品閉環 |
| `HOST` | 真 Host/principal/policy | Host 效果 |

本檔所有 16 案為 `DESIGN`；不得寫成 `COMPONENT`／`E2E`／`HOST` PASS。

## 01.1A 33 FR 原義 crosswalk（EC 16＋FAR 17）

本表由 `05.case_refs[].requirement_refs` 反向生成；每一列都通過 machine join。`profile_only` 表示該 FR 在原 Profile 才成立，W3 以 profile-only／ReasonedNC 保留，不刪原義。`NOT_RUN` 表示原案尚未真跑，不是已通過。

| FR | primary case | 原案狀態 | profile_only | smoke |
|---|---|---|---|---|
| `EC-FR01` | `W3-FRZ-01` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `EC-FR02` | `W3-FRZ-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `EC-FR03` | `W3-CHK-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR04` | `W3-CHK-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR05` | `W3-RUN-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR06` | `W3-RUN-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR07` | `W3-RUN-02` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR08` | `W3-RUN-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR09` | `W3-RUN-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR10` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `EC-FR11` | `W3-R3-04` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR12` | `W3-CHK-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR13` | `W3-FRZ-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `EC-FR14` | `W3-FAR-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `EC-FR15` | `W3-FR16-01` | `NOT_RUN` | `true` | `MATERIAL_PARSE_OK` |
| `EC-FR16` | `W3-FR16-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `FAR-FR01` | `W3-FRZ-01` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR02` | `W3-RUN-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `FAR-FR03` | `W3-RUN-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `FAR-FR04` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR05` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR06` | `W3-FR16-01` | `NOT_RUN` | `true` | `MATERIAL_PARSE_OK` |
| `FAR-FR07` | `W3-FAR-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |
| `FAR-FR08` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR09` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR10` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR11` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR12` | `W3-FAR-02` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR13` | `W3-G2-01` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR14` | `W3-G2-01` | `NOT_RUN` | `false` | `SMOKE_PASS` |
| `FAR-FR15` | `W3-FR16-01` | `NOT_RUN` | `true` | `MATERIAL_PARSE_OK` |
| `FAR-FR16` | `W3-FR16-01` | `NOT_RUN` | `true` | `MATERIAL_PARSE_OK` |
| `FAR-FR17` | `W3-FR17-01` | `NOT_RUN` | `false` | `MATERIAL_PARSE_OK` |

**對位規則**：primary case 必須在其 `requirement_refs` 包含該 FR；本表 33/33 由 05 反向生成，不是字串存在性。若 FR 需真 Host/World/Fabric，該案仍 `NOT_RUN`。

## 01.3 Oracle freeze rule

1. Case Owner 按有效原義簽定 expected，**先於 observed**。
2. 原 oracle/fixture bytes 單獨存放 read-only；本包 design oracle 不取代原域。
3. 新 candidate 若 oracle 不變，必保持相同 hash。
4. 變更需求或 oracle 必須正式 CR＋新 case/oracle revision；舊 FAIL 保留。
5. 所有 actual 只寫 evidence/closeout，不回改 `03` 預期。
6. 無真 oracle 的案保持 `NOT_RUN`／`NotCovered`；不得用 synthetic 代替原域。

## 01.4 設計 fixture／oracle 的邊界

| 欄 | 本包值 | 真值要求 |
|---|---|---|
| `design_state` | `PROPOSED_DESIGN_FIXTURE`／`PROPOSED_DESIGN_ORACLE` | 真 Case Owner freeze |
| `case_owner` | `UNASSIGNED_DESIGN` | 具名 Case Owner |
| `frozen_at` | `2026-11-26T14:14:10+08:00`（設計時間） | 真 freeze 時間 |
| `expected.exit` | `0`／`2` design placeholder | 真 runner ABI exit |
| `observed` | `null` | 真 run 後另存 |
| `verdict` | `NOT_RUN` | 真 run 後另判 |

---

# 02｜Case contract 欄位

每案必須有以下欄位；`03` 逐案寫實，`05` 以 `case_refs[]` 機讀。

| 欄位 | 必要 | 說明 |
|---|---|---|
| `case_id` | 是 | 原 16 ID，不重編 |
| `kind` | 是 | POS／NEG／EDGE／SEC |
| `requirement_refs` | 是 | 原 FR／ACC／W3M trace |
| `child` | 是 | 最小可反證切片 |
| `fixture_ref`＋`sha256`＋`bytes` | 是 | design 或真 fixture；真值另 freeze |
| `oracle_ref`＋`sha256`＋`bytes` | 是 | expected 先於 observed |
| `runner`＋`args`＋`cwd`＋`timeout` | 是 | 真 runner 未得時記 `UNBOUND`＋late-bind |
| `preconditions` | 是 | roots／ACL／fixture／oracle／Host |
| `expected_exit` | 是 | 真 ABI 或 design placeholder |
| `expected_raw` | 是 | token＋predicate＋raw assertions |
| `predicate` | 是 | 語義判準，不只看 exit |
| `observed` | 是 | 未跑 `null` |
| `verdict` | 是 | 未跑 `NOT_RUN` |
| `not_covered` | 是 | 原因／owner／resume |
| `checker_route` | 是 | 分立 Checker |
| `consumer` | 是 | 下一方 |

**Case contract schema**：`assets/schema/W3_CASE_CONTRACT.schema.json`。此 schema 是 design projection；真 consumer 若要求原 ABI，必須另做版本隔離映射，不把本 schema 當原 canonical。

---

# 03｜16 原案逐案契約

> 下列 SHA/bytes 為本包 design fixture/oracle 的實際 raw 值。`expected_exit` 的 `0/2` 是 design placeholder；`拒` 的語義是 non-success＋typed token＋零副作用，不是發明原 exit code。

### W3-FRZ-01｜POS｜WM3-P01

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-FRZ-01`／`POS`／`WM3-P01` |
| `requirement_refs`／`child` | `W3-A01`, `W3-CODEX-01`, `EC-FR01`, `EC-FR02`, `FAR-FR01`／`CH-FRZ-01-POS` |
| `fixture_ref` | `assets/fixtures/W3-FRZ-01.json`；SHA-256 `2ea7be05d07cdb3e25e2f46f420f95ed86582fbf73d5ebda11c28115fef4de92`；bytes `2065` |
| `oracle_ref` | `assets/oracles/W3-FRZ-01.json`；SHA-256 `e17d90664f86d14764748822ed834e8301faa431a6eb5e3ec92c341edf464316`；bytes `1171` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-FRZ-01-runner`；argv `python <real-runner> --case W3-FRZ-01 --fixture assets/fixtures/W3-FRZ-01.json --oracle assets/oracles/W3-FRZ-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`fixture_time, host_policy, pins, scope, subject`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `0`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `FREEZE_LEDGER_VERIFIED`；predicate：all five pins reopen; source/candidate/evidence/oracle/case_set are distinct; no source byte changed; fixture/time/host/policy are separate fields；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | all five pins reopen; source/candidate/evidence/oracle/case_set are distinct; no source byte changed; fixture/time/host/policy are separate fields |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | real W2/W3 five-pin preimages are not frozen; the product freeze runner is UNBOUND; design digests are not product identity |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Challenger; FAR; Checker |
| `source trace` | `PLAN:L582`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-FRZ-02｜NEG｜WM3-P01

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-FRZ-02`／`NEG`／`WM3-P01` |
| `requirement_refs`／`child` | `W3-A01`, `EC-FR02`, `EC-FR13`／`CH-FRZ-02-NEG` |
| `fixture_ref` | `assets/fixtures/W3-FRZ-02.json`；SHA-256 `e8b585981912599db1279ee893ec4e1fdf3203e35a9713a05e91118c8de8d204`；bytes `1296` |
| `oracle_ref` | `assets/oracles/W3-FRZ-02.json`；SHA-256 `5d00ebde2b1dfde9dbac39109976c3557300f96fc0c6ccd4ee69c726922c76d8`；bytes `1159` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-FRZ-02-runner`；argv `python <real-runner> --case W3-FRZ-02 --fixture assets/fixtures/W3-FRZ-02.json --oracle assets/oracles/W3-FRZ-02.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`mutations, runner_expected_not_invoked, scope, source_sentinel, subject`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `FROZEN_IDENTITY_MISMATCH`；predicate：each subcase refuses before runner invocation; zero writes; source sentinel unchanged; applicable downstream token CANDIDATE_CHANGED or ORACLE_DRIFT is named；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | each subcase refuses before runner invocation; zero writes; source sentinel unchanged; applicable downstream token CANDIDATE_CHANGED or ORACLE_DRIFT is named |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | the real refusal exit code must be frozen from the real intake ABI; exit 2 is a design placeholder |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | P02; Checker |
| `source trace` | `PLAN:L583`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-RUN-01｜POS｜WM3-P02/WM3-P03

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-RUN-01`／`POS`／`WM3-P02/WM3-P03` |
| `requirement_refs`／`child` | `W3-A02`, `EC-FR05`, `EC-FR06`, `EC-FR08`, `EC-FR09`, `FAR-FR02`, `FAR-FR03`／`CH-RUN-01-POS` |
| `fixture_ref` | `assets/fixtures/W3-RUN-01.json`；SHA-256 `a13f479256e9d6f7ffb5beb77e7947ebb4a113fb9eb0b217a73cad61cec8779e`；bytes `1272` |
| `oracle_ref` | `assets/oracles/W3-RUN-01.json`；SHA-256 `34b9a16a3e1fca2fb45e2bfbed90f453b297386ec1dcffc6d763e31c0b2e1e80`；bytes `1120` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-RUN-01-runner`；argv `python <real-runner> --case W3-RUN-01 --fixture assets/fixtures/W3-RUN-01.json --oracle assets/oracles/W3-RUN-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`case_pair, fixture, isolation, oracle, runner, timeout_s`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `0`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `SEMANTIC_MATCH`；predicate：POS expected matches; NEG produces the expected refusal; Case PASS and operation-not-established are recorded separately; both raw records are independent；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | POS expected matches; NEG produces the expected refusal; Case PASS and operation-not-established are recorded separately; both raw records are independent |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | the original runner/oracle/fixture are UNBOUND; exit 0 alone is not PASS |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | P03; FAR |
| `source trace` | `PLAN:L584`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-RUN-02｜NEG｜WM3-P02/WM3-P03

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-RUN-02`／`NEG`／`WM3-P02/WM3-P03` |
| `requirement_refs`／`child` | `W3-A02`, `EC-FR06`, `EC-FR07`／`CH-RUN-02-NEG` |
| `fixture_ref` | `assets/fixtures/W3-RUN-02.json`；SHA-256 `41be9072ed9ed4e3ef58244e451bfdd1d67193be46d076b5af891f1b79a851d8`；bytes `1120` |
| `oracle_ref` | `assets/oracles/W3-RUN-02.json`；SHA-256 `d07cc6baadc48d00ab5578489b784bb9f9168a335cef930ceda42e971bbbd121`；bytes `1092` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-RUN-02-runner`；argv `python <real-runner> --case W3-RUN-02 --fixture assets/fixtures/W3-RUN-02.json --oracle assets/oracles/W3-RUN-02.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`defects, executed_expected, runner`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `UNREPRODUCED`；predicate：each defect maps to UNREPRODUCED / RUNNER_UNBOUND / RAW_UNTRUSTED; executed=false; no fake exit; no stdout substitution；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | each defect maps to UNREPRODUCED / RUNNER_UNBOUND / RAW_UNTRUSTED; executed=false; no fake exit; no stdout substitution |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | a real CaseRunner/Curator must supply the missing raw before any REPRODUCED claim |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | FAR; CaseRunner |
| `source trace` | `PLAN:L585`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-FAR-01｜NEG｜WM3-P04

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-FAR-01`／`NEG`／`WM3-P04` |
| `requirement_refs`／`child` | `W3-A04`, `FAR-FR07`, `EC-FR14`／`CH-FAR-01-NEG` |
| `fixture_ref` | `assets/fixtures/W3-FAR-01.json`；SHA-256 `f2107fadf360f449026f47e757d7a28cbb0a2aa72fc9bec43df73a5aae2799e2`；bytes `1310` |
| `oracle_ref` | `assets/oracles/W3-FAR-01.json`；SHA-256 `b7eb3f62208784e3bf8e17aa2561828dd82c48abb8f73a0f8d2cb2948128aca6`；bytes `1161` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-FAR-01-runner`；argv `python <real-runner> --case W3-FAR-01 --fixture assets/fixtures/W3-FAR-01.json --oracle assets/oracles/W3-FAR-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`injected_claim, provider_missing, providers`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `UNAVAILABLE`；predicate：missing provider yields UNAVAILABLE with rows=null and zero_results=null; the injected zero becomes RESEARCH_REQUIRED; the reachable empty control is ZERO_RELEVANT_HIT with denominator；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | missing provider yields UNAVAILABLE with rows=null and zero_results=null; the injected zero becomes RESEARCH_REQUIRED; the reachable empty control is ZERO_RELEVANT_HIT with denominator |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | Fabric/ResearchWO is not available; Generic legal local query is a design control only |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Guide; Research Owner |
| `source trace` | `PLAN:L586`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-FAR-02｜POS｜WM3-P05

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-FAR-02`／`POS`／`WM3-P05` |
| `requirement_refs`／`child` | `W3-A04`, `W3-A05`, `FAR-FR08`, `FAR-FR09`, `FAR-FR10`, `FAR-FR11`, `FAR-FR12`, `EC-FR10`, `FAR-FR04`, `FAR-FR05`／`CH-FAR-02-POS` |
| `fixture_ref` | `assets/fixtures/W3-FAR-02.json`；SHA-256 `b894d39b74d14c48bc241fa12273229c32df18087d2b44ced54a460455881d61`；bytes `1662` |
| `oracle_ref` | `assets/oracles/W3-FAR-02.json`；SHA-256 `2831c3420f0bdaeb5f84b704b5eb7b6353e7bf949359625be1217f0f48a02bbd`；bytes `1127` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-FAR-02-runner`；argv `python <real-runner> --case W3-FAR-02 --fixture assets/fixtures/W3-FAR-02.json --oracle assets/oracles/W3-FAR-02.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`alternatives, cost, evidence_refs, finding_ref, owner, risk, rollback`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `0`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `ALTERNATIVES_SUBSTANTIVE`；predicate：at least two different alternatives each with evidence, counterevidence, cost/risk (UNKNOWN allowed), ChangeCone, expected raw, owner and rollback; no fixed template；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | at least two different alternatives each with evidence, counterevidence, cost/risk (UNKNOWN allowed), ChangeCone, expected raw, owner and rollback; no fixed template |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | no real Finding/raw exists; this is a design contract only |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Guide; Owner |
| `source trace` | `PLAN:L587`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-G2-01｜NEG｜WM3-P06

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-G2-01`／`NEG`／`WM3-P06` |
| `requirement_refs`／`child` | `W3-A06`, `U-034`, `FAR-FR14`, `FAR-FR13`／`CH-G2-01-NEG` |
| `fixture_ref` | `assets/fixtures/W3-G2-01.json`；SHA-256 `34c0c4dd9a19f6f92bd4e8e7a83bb4561977a17922cc9dcaf09bb13185a717ee`；bytes `1198` |
| `oracle_ref` | `assets/oracles/W3-G2-01.json`；SHA-256 `639e31a68902f9e1566345d4ef9be7fe8e3f03195d5ef505251e79ba95bad9bd`；bytes `1091` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-G2-01-runner`；argv `python <real-runner> --case W3-G2-01 --fixture assets/fixtures/W3-G2-01.json --oracle assets/oracles/W3-G2-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`caller_verified, periods, requested_claim, single_evidence_sha`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `DELTA_UNVERIFIED`；predicate：one period / caller boolean / single evidence_sha cannot produce PARK or NO_DELTA; no re-dispatch; the two-period positive control is separately required；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | one period / caller boolean / single evidence_sha cannot produce PARK or NO_DELTA; no re-dispatch; the two-period positive control is separately required |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | WorldReader two-period receipts are UNBOUND |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Guide; Program |
| `source trace` | `PLAN:L588`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-CHK-01｜NEG｜WM3-P03/WM3-P06

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-CHK-01`／`NEG`／`WM3-P03/WM3-P06` |
| `requirement_refs`／`child` | `W3-A07`, `EC-FR12`, `EC-FR03`, `EC-FR04`／`CH-CHK-01-NEG` |
| `fixture_ref` | `assets/fixtures/W3-CHK-01.json`；SHA-256 `0598ea40dccf1a5e8726ab9e8b95432917b69761dd37f54c18f88f0560dfaef0`；bytes `1113` |
| `oracle_ref` | `assets/oracles/W3-CHK-01.json`；SHA-256 `ffac9777f253e3c4ba5ab97e893a821537a17b5ad39dfaf1c739adeca90de655`；bytes `1098` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-CHK-01-runner`；argv `python <real-runner> --case W3-CHK-01 --fixture assets/fixtures/W3-CHK-01.json --oracle assets/oracles/W3-CHK-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`advisory_verdict, report_role, requested_write`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `FALSE_AUTHORITY`；predicate：advisory PASS cannot write original_checker_verdict; publisher action refused; checker verdict remains null; report does not authorize；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | advisory PASS cannot write original_checker_verdict; publisher action refused; checker verdict remains null; report does not authorize |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | no protected Checker signer exists; this is a design refusal contract |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Checker |
| `source trace` | `PLAN:L589`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-R3-01｜POS｜WM3-P01/WM3-P03

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-R3-01`／`POS`／`WM3-P01/WM3-P03` |
| `requirement_refs`／`child` | `W3-A01`, `W3M-D06`／`CH-R3-01-POS` |
| `fixture_ref` | `assets/fixtures/W3-R3-01.json`；SHA-256 `380bf0618ca4225ee192df57ee2873bed5d2b37aebc1f28bceb59d63f03fba3d`；bytes `1162` |
| `oracle_ref` | `assets/oracles/W3-R3-01.json`；SHA-256 `919d3a61d9c585985731b40020891e3fcad6d752e07d618e3a786700ec9fb6cd`；bytes `1025` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-R3-01-runner`；argv `python <real-runner> --case W3-R3-01 --fixture assets/fixtures/W3-R3-01.json --oracle assets/oracles/W3-R3-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`locator, requested_action`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `0`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `NOT_COVERED`；predicate：identity is preserved; missing bytes stay missing; no fabricated raw; no promotion to full coverage；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | identity is preserved; missing bytes stay missing; no fabricated raw; no promotion to full coverage |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | original CH-07 bytes are not present |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Curator; W4 |
| `source trace` | `PLAN:L590`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-R3-02｜NEG｜WM3-P06

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-R3-02`／`NEG`／`WM3-P06` |
| `requirement_refs`／`child` | `W3-A06`, `W3M-D06`／`CH-R3-02-NEG` |
| `fixture_ref` | `assets/fixtures/W3-R3-02.json`；SHA-256 `54e37ff3c50b667d0b0a613ac8df10140d334e35d95cfcb30581764920a26de5`；bytes `1399` |
| `oracle_ref` | `assets/oracles/W3-R3-02.json`；SHA-256 `b5fc365df3d3a84de3072a2e1929d3199929f99fe3038180ebaad5943488a186`；bytes `1020` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-R3-02-runner`；argv `python <real-runner> --case W3-R3-02 --fixture assets/fixtures/W3-R3-02.json --oracle assets/oracles/W3-R3-02.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`claimed, counts, world_raw_present`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `DELTA_UNVERIFIED`；predicate：count-only historical series is not WorldRaw; no PARK; two same-scope real receipts are required；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | count-only historical series is not WorldRaw; no PARK; two same-scope real receipts are required |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | no two-period WorldReader raw |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Guide; WorldReader |
| `source trace` | `PLAN:L591`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-R3-03｜POS｜WM3-P04

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-R3-03`／`POS`／`WM3-P04` |
| `requirement_refs`／`child` | `W3-A04`, `W3M-D05`／`CH-R3-03-POS` |
| `fixture_ref` | `assets/fixtures/W3-R3-03.json`；SHA-256 `d0faad1c968b24f38fbec29577f083b5ad3eb8eb168e0c78f60ea2f868296cf6`；bytes `1122` |
| `oracle_ref` | `assets/oracles/W3-R3-03.json`；SHA-256 `9fbc7a90f788b53aca480873f04159c96b7839bd864c6dfa763e502e3e83e30f`；bytes `1151` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-R3-03-runner`；argv `python <real-runner> --case W3-R3-03 --fixture assets/fixtures/W3-R3-03.json --oracle assets/oracles/W3-R3-03.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`case_oracle_like, denominator, enumerated_files, fresh_enumeration, query, root`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `0`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `ZERO_RELEVANT_HIT`；predicate：the historical root/query is scoped and enumerated; zero is relative to that root/query, not the whole library; missing original raw stays NotCovered；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | the historical root/query is scoped and enumerated; zero is relative to that root/query, not the whole library; missing original raw stays NotCovered |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | the 192-file historical raw is not re-enumerated in this author round; fresh results are a separate period |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | FAR; Research Owner |
| `source trace` | `PLAN:L592`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-R3-04｜NEG｜WM3-P03/WM3-P06

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-R3-04`／`NEG`／`WM3-P03/WM3-P06` |
| `requirement_refs`／`child` | `W3-A07`, `W3M-D05`, `EC-FR11`／`CH-R3-04-NEG` |
| `fixture_ref` | `assets/fixtures/W3-R3-04.json`；SHA-256 `a983c5be6cfaf5f16f266121a455cdb20593b120bc857af420d8b4422d1db0a1`；bytes `1063` |
| `oracle_ref` | `assets/oracles/W3-R3-04.json`；SHA-256 `5eeb73dc78972d540aaae6d506ff2cb3869177bbd7c9a6d662a56820f4bc44e1`；bytes `1007` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-R3-04-runner`；argv `python <real-runner> --case W3-R3-04 --fixture assets/fixtures/W3-R3-04.json --oracle assets/oracles/W3-R3-04.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`requested_claim, same_process, same_worktree, self_check`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `FALSE_INDEPENDENT`；predicate：self-check cannot raise the observation layer; a distinct Checker receipt is required；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | self-check cannot raise the observation layer; a distinct Checker receipt is required |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | no distinct Checker exists |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Checker |
| `source trace` | `PLAN:L593`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-R3-05｜POS｜WM3-P05

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-R3-05`／`POS`／`WM3-P05` |
| `requirement_refs`／`child` | `W3-A04`, `W3M-D02`／`CH-R3-05-POS` |
| `fixture_ref` | `assets/fixtures/W3-R3-05.json`；SHA-256 `ff731933792526da13c5188757027f63dfdbf452830559b8956e307edbb07bf2`；bytes `1427` |
| `oracle_ref` | `assets/oracles/W3-R3-05.json`；SHA-256 `6b14d77c459b6c4c64b4d68976db0338d6a5fecc544eb936aa83ee24ef224878`；bytes `1067` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-R3-05-runner`；argv `python <real-runner> --case W3-R3-05 --fixture assets/fixtures/W3-R3-05.json --oracle assets/oracles/W3-R3-05.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`alternatives, old_problem_reopened, root_cause`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `0`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `ALTERNATIVES_SUBSTANTIVE`；predicate：two substantive alternatives with Fit/NoFit and owner/scope; no new root cause or license claim without evidence；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | two substantive alternatives with Fit/NoFit and owner/scope; no new root cause or license claim without evidence |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | original sample rights/designation are not available |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | FAR; Owner |
| `source trace` | `PLAN:L594`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-R3-06｜NEG｜WM3-P01/WM3-P04

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-R3-06`／`NEG`／`WM3-P01/WM3-P04` |
| `requirement_refs`／`child` | `W3-A01`, `W3M-D07`／`CH-R3-06-NEG` |
| `fixture_ref` | `assets/fixtures/W3-R3-06.json`；SHA-256 `e33ba60504566a85cbf30b178436d7d973dba60e12db49286edc82f4d78dd13e`；bytes `1053` |
| `oracle_ref` | `assets/oracles/W3-R3-06.json`；SHA-256 `422f1e6f9ea5339b421838405e077da50334ac44f9898179713a6e9b736bf4c6`；bytes `1029` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-R3-06-runner`；argv `python <real-runner> --case W3-R3-06 --fixture assets/fixtures/W3-R3-06.json --oracle assets/oracles/W3-R3-06.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`acl_observation, original_reader, requested_claim`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `ORIGINAL_READER_UNBOUND`；predicate：a Generic file read continues; the original-domain ACK is not claimed; no invented reader；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | a Generic file read continues; the original-domain ACK is not claimed; no invented reader |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | original Source Owner/Reader is absent |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Source Owner; Checker |
| `source trace` | `PLAN:L595`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-FR16-01｜NEG｜WM3-P03

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-FR16-01`／`NEG`／`WM3-P03` |
| `requirement_refs`／`child` | `W3-A07`, `EC-FR16`, `EC-FR15`, `FAR-FR06`, `FAR-FR15`, `FAR-FR16`／`CH-FR16-01-NEG` |
| `fixture_ref` | `assets/fixtures/W3-FR16-01.json`；SHA-256 `bc8f6e1de1211cc127c3971072fb7c7b03ebe55c00e44bd8467e546918e9b068`；bytes `1133` |
| `oracle_ref` | `assets/oracles/W3-FR16-01.json`；SHA-256 `77b8ef4f564dd77deefd46270bba4018f70462f7ad29a4eb51e6331819824537`；bytes `1132` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-FR16-01-runner`；argv `python <real-runner> --case W3-FR16-01 --fixture assets/fixtures/W3-FR16-01.json --oracle assets/oracles/W3-FR16-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`canary, pre_hashes, report_write_set`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `WRITE_SCOPE_VIOLATION`；predicate：malicious report write set is refused; zero subject/oracle/test/threshold mutation; canary unchanged; an independent Native role ECP is still required for any product patch；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | malicious report write set is refused; zero subject/oracle/test/threshold mutation; canary unchanged; an independent Native role ECP is still required for any product patch |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | no protected product target is touched in this design case |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Security; Repo Owner |
| `source trace` | `PLAN:L596`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |


### W3-FR17-01｜NEG｜WM3-P03/WM3-P06

| 欄 | 值 |
|---|---|
| `case_id`／`kind`／`wp` | `W3-FR17-01`／`NEG`／`WM3-P03/WM3-P06` |
| `requirement_refs`／`child` | `W3-A07`, `FAR-FR17`／`CH-FR17-01-NEG` |
| `fixture_ref` | `assets/fixtures/W3-FR17-01.json`；SHA-256 `ca65a5701883f74ff5ddbd3777b828dc466425c766c39f45b44d65265fe6c967`；bytes `1086` |
| `oracle_ref` | `assets/oracles/W3-FR17-01.json`；SHA-256 `4df87ec8b6d58fd82477d90b5f923c8f66cdc30b750901fbde32708a9a320d05`；bytes `1044` |
| `runner`／`args`／`cwd`／`timeout` | `UNBOUND::W3/W3-FR17-01-runner`；argv `python <real-runner> --case W3-FR17-01 --fixture assets/fixtures/W3-FR17-01.json --oracle assets/oracles/W3-FR17-01.json --out <isolated-run-root>`；cwd `<isolated-case-root>`；timeout `120s` |
| `preconditions` | subject=`FHS-5_PLP/W3/CONTROL_PACK`；scope=`W3-NF-01`；input keys=`actor, requested_effects, target`；runner=`UNBOUND` 直到 Case Owner late-bind；不得寫 subject/oracle；隔離 cwd；timeout 120s |
| `expected_exit` | `2`（DESIGN_PLACEHOLDER；真值由 Case Owner 從 runner ABI 凍結） |
| `expected_raw` | token `FALSE_AUTHORITY`；predicate：FAR refuses WorkOrder/Grant/Release and subject/Host writes; authority=NONE; a separate Publisher/Checker is required；另需 argv／exit／stdout／stderr／pre-post raw |
| `predicate` | FAR refuses WorkOrder/Grant/Release and subject/Host writes; authority=NONE; a separate Publisher/Checker is required |
| `observed`／`verdict` | `null`／`NOT_RUN` |
| `not_covered` | no Publisher/Checker is present |
| `checker_route` | 分立 Checker（未取得）；同 candidate/scope/Host/epoch；不與 Maker/Challenger 同 process |
| `consumer` | Checker; Publisher |
| `source trace` | `PLAN:L597`；`WM3 §02.4／§09.B`；`assets/schema/W3_PLAN_INDEX.json` |

---

# 04｜N01–N12 跨波反證

以下 12 列是獨立帳，不新增 W3 原案分母；每列只停受影，不把其他波未完成當全域 blocker。

| ID | W3 適用操作與真出口 | 失敗判準／其他波處置 |
|---|---|---|
| `N01` source→TPM | 真 W3 clauses/Child/NEG→PI/PD/ECP/TQAEP→Reviewer 讀回 | 假 source、缺 Child B，不能以 W1 receipt 抵 W3 input |
| `N02` six-file ABI | 真 W3 六檔、schema、body、file/pack/source hash、四 API/legacy optional | fake hash/unknown/LOSSY/path reject；不抵 38+28 |
| `N03` Guide Delta | 真九鍵/兩期 verifier；new/no/unknown | 缺期、caller bool、單 evidence_sha 拒 |
| `N04` Host actual | CODEX manifest/entry loaded/invoked/served/consumed | 假 alias、僅本地 code；GPT/HERMES 各別未驗 |
| `N05` Native authority/recovery | 每 op ECP/ACL/preimage/pre-post/recovery 真；revoked 反例 | writer 無權仍寫/恢復不符/OPS `git revert` 拒 |
| `N06` UNKNOWN | 未識別 effect/schema/field typed unknown，保 unknown 且停受影 | UNKNOWN 當 READ、丟欄拒 |
| `N07` frozen challenge | W3 5 pins、fixture/runner/raw/role-separated、≥2 classes | oracle drift／fake raw／自簽拒 |
| `N08` FAR dynamic | 真兩 Finding 各查詢、五態、≥2 alternatives、十 Advice | 固定樣本、UNAVAILABLE=ZERO、Advice=grant 拒 |
| `N09` combined E2E | 五方實質材料 consumption、Native patch/retest、Guide2；同 Scope pins | 只互傳 hash/無實際 invoke；direct bypass 不抵五方 |
| `N10` OFF/security | 受控 clean-off import/loader trace、正控、path/symlink/secret、相同語義成功 | 同失敗 parity、marker-only、escaping root 拒 |
| `N11` fresh receive | clean checkout，逐 raw/manifest seal、true material consume、negative short-circuit | stale receipt、同工作樹 fallback、wrong pin/raw/scope 拒 |
| `N12` applicability/release | Generic/FHS profile and denominators、Checker/Consumer distinct、W4 handoff | 485 強制 Generic、advisory/push 冒 Release 拒；W4 適用全案另驗 |

---

# 05｜J1／J2／J3 上游受影

| 編號 | 契約 | W3 消費 | 不可做 |
|---|---|---|---|
| `J1` strict read-before-consume | 錯 pin/raw/shape → zero downstream calls/writes | P01 intake 讀 W2 五 pin／pack／raw | 先 invoke 再驗 |
| `J2-pre` contract input | 契約輸入真材料；不含 actual post | P01/P02 的 invocation contract | 把 post 當 pre |
| `J2-post` post verification | 執行後 ChangeSet／readback；不回卡同一 op | P06 patch/retest 的 post | 把 final Checker 設為 P02 前件 |
| `J3` ON/OFF true semantic parity | 兩路語義成功、15 typed keys、OFF import trace | X09；W2 當期重驗另案 | 同失敗、同 exit、同 hash 給 parity |

W3 也測上述模式對自有當期包的適用子案，獨立記 trace；不得引用舊 15/16/23/21/13 數字作成功。

---

# 06｜兩個動態 Finding 的設計

## 06.1 Finding A：安全／准入分類

| 欄 | 內容 |
|---|---|
| 可重現條件 | 對已撤權或錯 exact target 的隔離候選調用受信 gate；期望拒絕、零寫入、sentinel 不變；若實際誤收或錯誤 token 才形成反例 |
| 正控 | 合法隔離 op 在同一 gate 成功，證明 gate 不是全拒 |
| 差額來源 | W2 S1Δ D1/D4/D4b、C2 §2；W3 不重打已報告閉環；以當期 raw 才決定是否真 defect |
| 可反證根因 | `H-AUTHORITY_UNBOUND` vs `H-CODE-EXISTS-BINDING-MISSING` 或真 code defect；若被正確拒絕，記正常 veto，不宣已發現 bypass |
| Alternative 1 | `WAIT_ORIGINAL_AUTHORITY`：若原撤權正確，維持 writer blocked；Owner 新 decision 後才恢復對應 op |
| Alternative 2 | `FIX_NOW`（條件式）：只有真重現安全缺陷且原安全政策要求修時，受權 Maker 最小 patch/重驗；否則 NoFit |
| 反證／風險 | 無真新 grant、錯 root、被 revoked 仍寫；同 Finding 不改 oracle 求綠；原 restriction 正確≠bug |
| rollback／resume | 舊 candidate 保留；exact reverse patch、恢復 sentinel；新授權且同 pin/真 oracle |

## 06.2 Finding B：功能／資料消費分類

| 欄 | 內容 |
|---|---|
| 可重現條件 | 給 W3 dynamic Guide/FAR/Challenge 一份真 new case／兩期不同 material；期望真解析、識別 delta、正確分流；若固定 sample、只比 evidence_sha 或 source hash 域混用才形成反例 |
| 差額來源 | W0 `far_run`／`guide` reference 限制，W1 `guide_nf` 已有九鍵；先查 W1 現在是否正確，不預判仍壞 |
| 可反證根因 | `H-CODE-EXISTS-BINDING-MISSING` vs `H-CODE-MISSING`／`H-PD_DRIFT`；以 caller/entry/fixtures 判別 |
| Alternative 1 | `BIND_EXISTING`：若 W1 九鍵/通用程式真在，最小 adapter/trace 修正；保原 ABI |
| Alternative 2 | `FIX_NOW`：若真缺 dynamic input/實際 child，最小補通用函式；若已有同能力則 NoFit，避免重造 |
| 反證／風險 | 未讀原 caller、只改 schema 名、兩期同失敗、固定兩個範例仍是假通用 |
| rollback／resume | per-file reverse patch；新材料/真 caller/reader；Guide next 不自授權 |

## 06.3 若無真 defect

不為湊兩案假造產品 bug。可在隔離 fixture 明確構造受控 mutation（錯 pin、未知 schema、固定 template、單期、偽 zero），先凍結預期，再實際產紅及 distinct class，標 `TEST_MUTANT_FINDING`。此可證 W3 Challenge/FAR 對反例的產品能力，但不是「W2 發現新缺陷」。完整 W3 仍須真產品 candidate 和當期 16 原案退出。

---

# 07｜九鍵、OFF、fresh receive 的必要條件

## 07.1 九鍵負例

| 負例 | 預期 |
|---|---|
| 只有一期 | `DELTA_UNVERIFIED`；不 PARK |
| caller `verified=true` | 拒；不用 caller bool 代替 verifier |
| 單 `evidence_sha` | `DELTA_UNVERIFIED` |
| 兩期同 receipt 複製 | 拒 |
| 跨 subject/scope | 拒；不續工 |
| source-set／pack digest 混 | `SOURCE_HASH_DOMAIN_MIX` |
| oracle/Host/epoch drift | 重新資格化；不是同條件 NO_DELTA |
| 額外 candidate/evidence 真差額 | `NEW_DELTA` 候選；受影 retest |

## 07.2 ON／OFF

- ON：實際調用 TPM/Reviewer、Guide、Bridge、Challenge、FAR，驗 loaded/invoked/served、同 scope 真 body/context 和 raw/Advice 被下一方使用；不是 CLI inventory。
- OFF：fresh process＋clean isolated environment＋import blocker（正控證 blocker 真有效）＋module/loader trace；合法 Native file/Git/tester 直接路徑不載入禁用 legacy/選定 SP；不只切 env marker；各自 output root。
- 比較：同 scope/同 Oracle/fixture、同等合法能力，兩路 semantic success；run_id/output path 等非語義欄 normalize、保原 raw。兩路都 fail、同 exit、同 hash 均不給 parity。

## 07.3 Fresh receive

1. fresh checkout 固定 delivery commit。
2. 驗 `W3_CURRENT`（若未來存在）→外置 seal→`05`→5 MD/assets→W2 upstream pins→五 pin→Case/actual raw。
3. 解析實際 clause/Case/Guide Next/Stop/NotCovered。
4. 重放合法 POS/NEG 或交接要求的真 readback。
5. 負例：wrong pack/candidate/oracle/case-set/evidence、mutated raw、missing、schema/duplicate/cross-subject/path escape/stale receipt/wrong profile、缺 material consumption；均在 product call 前 fail closed，記 `cli_executed=false`／no input writes。
6. distinct Checker receipt＋Consumer receipt 是兩份材料；任一缺不聲稱兩者完成。

---

# 08｜W3 補強測試族（X01–X12，不增／替原 16）

| Group | 子案與預期 | 觀察層 |
|---|---|---|
| `X01` source & manifest | W3 6-file/asset SHA/bytes；duplicate JSON key、path/case collision、自循環 digest、unknown schema、missing source span、mutation 1 byte、wrong upstream five pins；全部早拒，正常包能讀正文 | component/invocation |
| `X02` upstream intake | wrong W2 product SHA vs delivery SHA、superseded 21/22/23、old W3 15/16 receipt、oracle carried、raw null、candidate member mismatch；只記 partial/拒，不自動發 readiness | invocation/E2E |
| `X03` dynamic findings | 至少兩實際不同 failure class；非固定 case request、case count 變化；oracle mutation/old candidate/no raw 拒；expected/observed/firstfail 和八欄 mapping | component + invocation + E2E |
| `X04` typed five-state | 真合法 local HIT/真 ZERO/隔離 absent UNAVAILABLE/權限拒 BLOCKED/解析錯 ERROR；各 query、denominator、raw；同 source mirror 不重算；Fabric OFF 不阻 Generic | component/invocation |
| `X05` ten Advice | 逐 enum positive 適用 predicate、負例缺證/錯 scope/偽 grant，至少兩 alternatives 每 Finding；`RESEARCH_REQUIRED/ABSTAIN` 不發權；NoFit 有反證 | component/invocation |
| `X06` delta & resume | true same/new、逐一 9 key 缺值、兩期錯序/同 receipt 複製、跨 scope、source-set/pack digest 混、fake verifier、oracle/Host/epoch drift、額外 candidate/evidence 真差額 | component/invocation/E2E |
| `X07` protected safety | revoked marker 與真 policy、exact target/ops、preimage absent/parent、root prefix-sibling、unknown effect、trust pin、race/reparse/ACL where applicable；各負例零 write/unlisted unchanged；residual 明列 | policy unit/component/Host（分帳） |
| `X08` recovery | 合法受界 patch/OPS actual pre/post/restore；exit0 semantic mismatch 仍 FAIL；只恢復本輪 artifact；oracle 不動 | invocation/E2E |
| `X09` isolation/off | 另 process/checkout、受控 `sys.path`/plugin absence、import/loader trace、禁止 HGK/FABRIC/SBL/FHS/PIPD/HERMES、Bridge/FAR 可 bypass；positive control 可檢到被禁 import；兩次語義成功且 projection 一致；雙失敗拒 | invocation/E2E/Host |
| `X10` path & byte | `..`/absolute/UNC、symlink/junction/reparse、relative link in-root 正控、prefix-sibling、Windows/WSL 分適用性；raw CRLF/LF mutation 拒；fresh checkout 每 raw bytes equality | component/Host |
| `X11` consume and SoD | TPM 真生成契約、Reviewer consume、Guide pack context、Bridge/direct body、Native 真 Case、Challenge/FAR/Guide2 真 raw use；偽裝只傳 SHA 拒；Checker/Consumer 不同 receipt；錯 raw/candidate/oracle/pack/Host/scope short-circuit | E2E/Host |
| `X12` stop/resume / publication | 同 failure key 無 delta 不派、最多兩次差額修補、grant revoke 即停；current pointer 唯一、superseded、fresh clean receive；public push≠Release、private raw 不上傳 | policy unit/E2E |

---

# 09｜Receipt、Checker、Consumer

## 09.1 CaseRunRecord 最小欄

```json
{
  "run_id": "<unique>",
  "operation_id": "P02/<case_id>",
  "runner_id": "<real or UNBOUND>",
  "binary_sha256": "<real or null>",
  "host_id": "<real or UNBOUND>",
  "os_principal": "<redacted or UNBOUND>",
  "policy_epoch": "<real or NOT_DECLARED_BY_HOST>",
  "project_id": "FHS-5_PLP",
  "subject": "FHS-5_PLP/W3/CONTROL_PACK",
  "scope": "W3-NF-01",
  "case_id": "<16 id>",
  "kind": "POS|NEG|EDGE|SEC",
  "source": {"ref": "...", "sha256": "..."},
  "candidate": {"ref": "...", "sha256": "..."},
  "evidence": {"ref": "...", "sha256": "..."},
  "oracle": {"ref": "...", "sha256": "..."},
  "case_set": {"ref": "...", "sha256": "..."},
  "fixture_sha256": "<real>",
  "argv": [],
  "cwd": "<isolated>",
  "env_redacted": {},
  "timeout_s": 120,
  "start": null,
  "end": null,
  "exit": null,
  "stdout_ref": null,
  "stdout_sha256": null,
  "stderr_ref": null,
  "stderr_sha256": null,
  "world_raw_ref": null,
  "world_raw_sha256": null,
  "pre": null,
  "post": null,
  "recovery": null,
  "expected": {"exit": 0, "token": "..."},
  "observed": null,
  "verdict": "NOT_RUN",
  "first_fail": null,
  "observation_layer": "DESIGN",
  "actor": null,
  "verification": "NOT_SIGNED",
  "signature_state": "NONE"
}
```

## 09.2 Checker

1. Checker 是**分立 role**，不是 Maker、Challenger、FAR 或 Guide。
2. 只讀 frozen candidate/oracle/case-set/raw；不從 Maker 任意可寫路徑載入 verifier。
3. 給 verdict/strength；不替 Consumer 收件。
4. 同 candidate/scope/Host/epoch；跨 candidate 的舊 verdict 不重用。
5. 本輪無 protected Checker；所有獨立性為 `NOT_CLAIMED`。

## 09.3 Consumer

1. fresh checkout；固定 delivery commit。
2. 真 parse/use/readback；不只比 digest。
3. 錯 pack/candidate/oracle/case-set/evidence/mutated raw/missing/schema/duplicate/cross-subject/path escape/stale receipt/wrong profile → fail closed。
4. 記 `cli_executed`／`input_writes`／`consumed`。
5. Checker 與 Consumer 是 distinct receipts；本輪未取得。

---

# 10｜執行順序、Stop／Resume、完成判定

## 10.1 執行順序

```text
P01 Freeze/Intake
  → P02 Runner (POS/NEG)
  → P03 Challenge/Finding/NotCovered
  → P04 FAR RQ0-4
  → P05 RCA/Alternatives/Ten Advice
  → P06 Guide2/Delta
  → (若需 repair) 另受權 Maker patch → new candidate → new freeze
  → affected P02/P03 retest
  → distinct Checker
  → fresh Consumer
  → W3 closeout/handoff
```

## 10.2 Stop／Resume

| 條件 | 停什麼 | Resume |
|---|---|---|
| 缺 runner/oracle/fixture | 只停該案 REPRODUCED | Case Owner 真 bytes/runner/ACL |
| 錯 pin/舊 raw | 只停同 slice | 同位真 pins 或 CR/re-freeze |
| UNAVAILABLE | 只停依賴該源的根因/CLOSE/PARK | 真 provider/typed receipt |
| 缺兩期 | 不 PARK/no-delta | 兩期同位真 receipt |
| 缺 Checker | 不宣 Independent | distinct verdict |
| 撤權/安全 Finding | 停受影 writer | Owner 新決策；不刪 marker |
| 同 failure key 無新材料 | 不重派 | 真新 material |

## 10.3 完成判定（W3_NF_VALIDATED，非本輪）

1. 採納當期 W3M/六檔/外 seal；真 inputs 同 identity；W2 actual requalification＋clean receipt。
2. 16 原案逐案滿足 applicable expected；required 缺 raw/未跑/FAIL/scope 漂移均不能全波 PASS。
3. 六 FUO 六 WP 有實際可重播出口；兩種動態 Finding；FAR 五態/RQ/alternatives/十 Advice/七九鍵/雙期；真 Native patch/retest 與 recovery，或原設計採納的切片中有權說明 no-repair applicability。
4. 安全 veto 清楚：無未解除 critical safety finding；真授權未撤；exact write set/pre-post/restore。
5. 同 candidate/oracle/case-set/scope 之分立 Checker 真驗收、fresh Consumer 真 parse/use/readback，兩份 distinct receipts。
6. 真 CLOSEOUT/HANDOFF/CHANGESET 與 current pointer 可重建；raw seal fresh checkout 一致。

---

# 11｜設計 fixture／oracle 清冊

| Case | Kind | Fixture | Fixture SHA-256 | bytes | Oracle | Oracle SHA-256 | bytes | Verdict |
|---|---|---|---|---:|---|---|---:|---|
| `W3-FRZ-01` | POS | `assets/fixtures/W3-FRZ-01.json` | `2ea7be05d07cdb3e25e2f46f420f95ed86582fbf73d5ebda11c28115fef4de92` | 2065 | `assets/oracles/W3-FRZ-01.json` | `e17d90664f86d14764748822ed834e8301faa431a6eb5e3ec92c341edf464316` | 1171 | `NOT_RUN` |
| `W3-FRZ-02` | NEG | `assets/fixtures/W3-FRZ-02.json` | `e8b585981912599db1279ee893ec4e1fdf3203e35a9713a05e91118c8de8d204` | 1296 | `assets/oracles/W3-FRZ-02.json` | `5d00ebde2b1dfde9dbac39109976c3557300f96fc0c6ccd4ee69c726922c76d8` | 1159 | `NOT_RUN` |
| `W3-RUN-01` | POS | `assets/fixtures/W3-RUN-01.json` | `a13f479256e9d6f7ffb5beb77e7947ebb4a113fb9eb0b217a73cad61cec8779e` | 1272 | `assets/oracles/W3-RUN-01.json` | `34b9a16a3e1fca2fb45e2bfbed90f453b297386ec1dcffc6d763e31c0b2e1e80` | 1120 | `NOT_RUN` |
| `W3-RUN-02` | NEG | `assets/fixtures/W3-RUN-02.json` | `41be9072ed9ed4e3ef58244e451bfdd1d67193be46d076b5af891f1b79a851d8` | 1120 | `assets/oracles/W3-RUN-02.json` | `d07cc6baadc48d00ab5578489b784bb9f9168a335cef930ceda42e971bbbd121` | 1092 | `NOT_RUN` |
| `W3-FAR-01` | NEG | `assets/fixtures/W3-FAR-01.json` | `f2107fadf360f449026f47e757d7a28cbb0a2aa72fc9bec43df73a5aae2799e2` | 1310 | `assets/oracles/W3-FAR-01.json` | `b7eb3f62208784e3bf8e17aa2561828dd82c48abb8f73a0f8d2cb2948128aca6` | 1161 | `NOT_RUN` |
| `W3-FAR-02` | POS | `assets/fixtures/W3-FAR-02.json` | `b894d39b74d14c48bc241fa12273229c32df18087d2b44ced54a460455881d61` | 1662 | `assets/oracles/W3-FAR-02.json` | `2831c3420f0bdaeb5f84b704b5eb7b6353e7bf949359625be1217f0f48a02bbd` | 1127 | `NOT_RUN` |
| `W3-G2-01` | NEG | `assets/fixtures/W3-G2-01.json` | `34c0c4dd9a19f6f92bd4e8e7a83bb4561977a17922cc9dcaf09bb13185a717ee` | 1198 | `assets/oracles/W3-G2-01.json` | `639e31a68902f9e1566345d4ef9be7fe8e3f03195d5ef505251e79ba95bad9bd` | 1091 | `NOT_RUN` |
| `W3-CHK-01` | NEG | `assets/fixtures/W3-CHK-01.json` | `0598ea40dccf1a5e8726ab9e8b95432917b69761dd37f54c18f88f0560dfaef0` | 1113 | `assets/oracles/W3-CHK-01.json` | `ffac9777f253e3c4ba5ab97e893a821537a17b5ad39dfaf1c739adeca90de655` | 1098 | `NOT_RUN` |
| `W3-R3-01` | POS | `assets/fixtures/W3-R3-01.json` | `380bf0618ca4225ee192df57ee2873bed5d2b37aebc1f28bceb59d63f03fba3d` | 1162 | `assets/oracles/W3-R3-01.json` | `919d3a61d9c585985731b40020891e3fcad6d752e07d618e3a786700ec9fb6cd` | 1025 | `NOT_RUN` |
| `W3-R3-02` | NEG | `assets/fixtures/W3-R3-02.json` | `54e37ff3c50b667d0b0a613ac8df10140d334e35d95cfcb30581764920a26de5` | 1399 | `assets/oracles/W3-R3-02.json` | `b5fc365df3d3a84de3072a2e1929d3199929f99fe3038180ebaad5943488a186` | 1020 | `NOT_RUN` |
| `W3-R3-03` | POS | `assets/fixtures/W3-R3-03.json` | `d0faad1c968b24f38fbec29577f083b5ad3eb8eb168e0c78f60ea2f868296cf6` | 1122 | `assets/oracles/W3-R3-03.json` | `9fbc7a90f788b53aca480873f04159c96b7839bd864c6dfa763e502e3e83e30f` | 1151 | `NOT_RUN` |
| `W3-R3-04` | NEG | `assets/fixtures/W3-R3-04.json` | `a983c5be6cfaf5f16f266121a455cdb20593b120bc857af420d8b4422d1db0a1` | 1063 | `assets/oracles/W3-R3-04.json` | `5eeb73dc78972d540aaae6d506ff2cb3869177bbd7c9a6d662a56820f4bc44e1` | 1007 | `NOT_RUN` |
| `W3-R3-05` | POS | `assets/fixtures/W3-R3-05.json` | `ff731933792526da13c5188757027f63dfdbf452830559b8956e307edbb07bf2` | 1427 | `assets/oracles/W3-R3-05.json` | `6b14d77c459b6c4c64b4d68976db0338d6a5fecc544eb936aa83ee24ef224878` | 1067 | `NOT_RUN` |
| `W3-R3-06` | NEG | `assets/fixtures/W3-R3-06.json` | `e33ba60504566a85cbf30b178436d7d973dba60e12db49286edc82f4d78dd13e` | 1053 | `assets/oracles/W3-R3-06.json` | `422f1e6f9ea5339b421838405e077da50334ac44f9898179713a6e9b736bf4c6` | 1029 | `NOT_RUN` |
| `W3-FR16-01` | NEG | `assets/fixtures/W3-FR16-01.json` | `bc8f6e1de1211cc127c3971072fb7c7b03ebe55c00e44bd8467e546918e9b068` | 1133 | `assets/oracles/W3-FR16-01.json` | `77b8ef4f564dd77deefd46270bba4018f70462f7ad29a4eb51e6331819824537` | 1132 | `NOT_RUN` |
| `W3-FR17-01` | NEG | `assets/fixtures/W3-FR17-01.json` | `ca65a5701883f74ff5ddbd3777b828dc466425c766c39f45b44d65265fe6c967` | 1086 | `assets/oracles/W3-FR17-01.json` | `4df87ec8b6d58fd82477d90b5f923c8f66cdc30b750901fbde32708a9a320d05` | 1044 | `NOT_RUN` |

**清冊說明**：`bytes` 與 `sha256` 是本包 design 檔的 raw 值；`05` 會再列一次並以 `case_refs[]` 交叉引用。真 Case Owner freeze 後，必須以新 bytes／SHA／`frozen_at`／`case_owner` 取代；舊 design 值只作歷史，不冒充真 oracle。

# 12｜DOC/SMOKE 層（r2 新增；不替代 16 原案）

## 12.1 目的與界線

§12 只證明「主用包的材料可被 fresh consumer 實際 parse/use，且能選合法下一動作」。它不是產品 `COMPONENT/INVOCATION/E2E/HOST` PASS，不改 §03 的 `observed=null`／`verdict=NOT_RUN`。

## 12.2 Smoke 路徑（最小但實質）

```text
FreezeLedger (05 + seal + current)
  → CaseRunRecord (design fixture + expected + isolated runner)
  → FindingSet (POS + NEG + two failure classes)
  → FARRetrievalGraph (HIT / ZERO_RELEVANT_HIT / UNAVAILABLE / BLOCKED_BY_AUTHORITY / ERROR)
  → DecisionAdvice (≥2 alternatives + 10 original advice names)
  → Guide2Handoff (7 keys → 9 keys + two-period delta)
  → repair proposal / retest routing (advice not grant)
```

每步需有 raw、exit、stdout/stderr SHA、consumer parse；只傳 hash 或只列檔不算 PASS。

## 12.3 必要負例

| 負例 | 預期 |
|---|---|
| 05 raw 與 seal 不符 | `SEAL_MISMATCH`，zero write |
| duplicate JSON key | `DUPLICATE_KEY`，拒 |
| source span 越界 | `SPAN_OOB`，拒 |
| case refs 少於 16 或 duplicate case | `CASE_REF_COUNT`／`CASE_DUPLICATE`，拒 |
| 16 案 observed 非 null | `FALSE_OBSERVED`，拒 |
| advice 當 Grant | `FALSE_AUTHORITY`，拒 |
| 缺兩期 | `DELTA_UNVERIFIED`，不 PARK |
| W2 blocked | 只停 W2 受影，W3 READ/smoke 續 |
| `../`／junction/reparse | `INVALID_PATH`，zero write |

## 12.4 Smoke receipt

見 `02_EVIDENCE/raw/smoke/`；每個 receipt 記 `command/argv/exit/stdout_sha256/stderr_sha256/assertions/consumer/verdict`。smoke 的 verdict 只能是 `SMOKE_PASS`／`SMOKE_FAIL`，不得寫成產品 `PASS`。

---

**本檔終點**：16 案契約已成文；全部 `observed=null`、`verdict=NOT_RUN`；§12 只提供 DOC/SMOKE 可消費證明；沒有任何產品 runner PASS、Checker verdict 或 Consumer receipt。
