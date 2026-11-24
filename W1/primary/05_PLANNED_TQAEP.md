<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜Planned TQAEP（作者）

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的 Planned TQAEP 正文，批次 `W1-PACK-01`。它凍結 W1 的作者測試分母、Oracle、Fixture 與 ExpectedRaw，供未來原 Runner／Checker 接續。它不是原 Canonical TQAEP，也不代表任何 Case 已由原域跑過。

## 1. 分母與分帳

三層分母分開，不互相抵銷：

1. **原域分母（保留、不重跑）**：Guide `CG-SEM01..17`（17）、Bridge 原 38＋28（66）、W0 `F5-W0-T01..T24`（24）。全部 `CASE_UNBOUND`／`NOT_RUN`。
2. **W1 作者案（本檔 13 案）**：W1M wm-v5 §09.1 的前八案＋`W1-R3-01..05`。每案有真本地 fixture／oracle，標 `AUTHOR_FIXTURE_NOT_LIVE`。
3. **本輪 harness（H1–H8）**：作者驗收 oracle，檢查本包的結構、來源、ABI、安全、Host、收斂與交付；不取代原 Case。

欄位讀法：Requirement: 原 Requirement／Case 的文字依據與 source span。Case: 本包唯一 Case ID 與 kind。Oracle: 作者 oracle 檔與判準。POS: 正向可觀測結果。NEG: 反向最小反例與 FirstFail。ExpectedRaw: 未來 Runner 必須回傳的 raw 欄位。Checker: 未來應由哪個角色驗。

Input: W1M §09.1 的 13 案定義、W0 24 案清冊、B02／B03 的原 Case 名稱、真 source spans。
Operation: 凍結每案的 Requirement／Oracle／Fixture／POS／NEG／ExpectedRaw，寫成 MD 與 JSON 投影。
Output: 本檔＋`oracles/*.json`＋`fixtures/*.json`＋`05_PLANNED_TQAEP.json`。
Consumer: 未來原 Runner／Protected Checker／W3 External Challenge。
NEG: 改 Oracle 求綠、刪 NEG、以作者 fixture 冒原 Raw → `ORACLE_DRIFT`／`TQAEP_CONTRACT_MISMATCH`。
FirstFail: `RUNNER_UNBOUND`（原域）／`PROJECTION_MISMATCH`（本包結構）。

## 2. W1 十三案

| Case | Kind | Requirement／來源 span | POS 或預期 | NEG／FirstFail | 本輪狀態 |
|---|---|---|---|---|---|
| `W1-HOST-01` | POS | W1M §09.1；M §11.7 U-017 | 某 Host 對同 Scope Context 產生真 `Consumed` Raw | 無 Raw 宣 Consumed → `HOST_PENDING` | `NOT_RUN` |
| `W1-HOST-02` | NEG | W1M §09.1；B02 §10 | 正確拒絕跨 Host 代償 | ChatGPT `Loaded` 抵 Hermes `Served` → `HOST_ABI_DRIFT` | `LOCAL_RULE_PASS` |
| `W1-HOST-03` | NEG | W1M §09.1；B02 §09 | 正確拒絕 skill 可讀升格 | 只讀 `SKILL.md` 宣 `Invoked` → `HOST_PENDING` | `LOCAL_RULE_PASS` |
| `W1-HERMES-01` | POS | W1M §09.1；M §11.7 U-028 | Kanban／Delegation／Swarm 三格分開各有 Raw | 三格合併或一格拉三格 → `REQUIRED_CHILD_MISSING` | `NOT_OBSERVED` |
| `W1-ABI-01` | NEG | W1M §09.1；B03 §05 | 拒絕 Guide `@2` 直送 Bridge `@2` | 同尾碼直送 → `EXPLICIT_REVIEW_REQUIRED` | `LOCAL_RULE_PASS` |
| `W1-ABI-02` | NEG | W1M §09.1；B03 §05 | 拒絕 proposal-1 未 crosswalk 升 @2 | 只 rename 或 drop unknown → `LOSSY_MIGRATION` | `LOCAL_RULE_PASS` |
| `W1-SEC-01` | SEC | W1M §09.1；B02 §08 EX-G-S01 | Context 內嵌指令只標記、不執行 | 執行 `ignore permission` → `UNTRUSTED_SOURCE_DATA` | `LOCAL_RULE_PASS` |
| `W1-API-01` | POS | W1M §09.1；B03 §07 | 四 API 可完整回取 Clause／NEG，不是 heading／excerpt | 只回 heading → `BODY_RESOLVER_UNBOUND` | `NOT_RUN` |
| `W1-R3-01` | POS | W1M §09.1；D01／D07 | 以 W0 PRIMARY 34 清冊（實體 36 檔、33/34 byte 一致）、27 entries pack、13 源作 inspect 輸入 | 隱藏 receipt stale → `AUTHOR_REVIEW_PARTIAL` | `AUTHOR_REVIEW_PARTIAL` |
| `W1-R3-02` | NEG | W1M §09.1；本輪 Codex 實例 | 拒絕 skill bytes read 當 Host `Loaded`／`Installed` | 升格 → `HOST_PENDING` | `LOCAL_RULE_PASS` |
| `W1-R3-03` | NEG | W1M §09.1；D05 | 拒絕缺 `effect`／`resume` 仍宣完整 | 缺欄仍 complete → `ABI_LOSSY_CROSSWALK` | `LOCAL_RULE_PASS` |
| `W1-R3-04` | EDGE | W1M §09.1；D06b | workspace 317→318 與 PRIMARY 分帳 | 混樹 → `WORKSPACE_DRIFT_BOUNDED` | `LOCAL_RULE_PASS` |
| `W1-R3-05` | NEG | W1M §09.1；D06 | 拒絕 CH-07 identity-only 冒舊 bytes 恢復 | 宣可恢復 → `EVIDENCE_LAUNDERING`／`DELTA_MISROUTED` | `LOCAL_RULE_PASS` |

Oracle 與 Fixture：每案一對，路徑為 `oracles/<case_id>.json` 與 `fixtures/<case_id>.json`，兩者 SHA 已列入 `PACKAGE_FILE_MANIFEST.json` 與 `cases[]`。Oracle 只寫作者判準與 expected state，不偽造原 Runner 輸出。

ExpectedRaw（每案共同必要欄）：

- Host：`host_id`、`manifest`、`loaded_sha256`、`installer_ref`、`policy_epoch`。
- Invocation：`command`、`args`、`exit`、`stdout_sha256`、`stderr_sha256`。
- Served：`served_bytes_sha256`、`scope_echo`、`served_at`。
- Consumed：`consumer_id`、`consumed_sha256`、`subject`、`scope`、`readback_at`。
- ABI：`package_sha256`、`subject`、`scope`、`unknown_fields[]`、`legacy_payload`。
- Case：`case_id`、`kind`、`requirement_ref`、`clause_text`、`oracle_sha256`、`fixture_sha256`。

Checker: 原域 Case 由原 Case Owner／Protected Checker；作者 13 案只由 `SELF_CHECK_ONLY` 自檢，未來可由 W3 External Challenge 以同 Subject／Scope／Candidate／Oracle 重現。作者不自簽 Independent。

## 3. W0 24 案 disposition

| Case | disposition | W1 用途 |
|---|---|---|
| `F5-W0-T01` | UPDATE | POS source anchor；不作 Host Raw |
| `F5-W0-T02` | RETAIN | 原義保留 |
| `F5-W0-T03` | RETAIN | 原義保留 |
| `F5-W0-T04` | UPDATE | fake Reader NEG → W1-HOST-02 |
| `F5-W0-T05` | RETAIN | 原義保留 |
| `F5-W0-T06` | UPDATE | path escape SEC → W1-SEC-01 鄰接 |
| `F5-W0-T07` | UPDATE | proposal-2 NEG → W1-ABI-01 |
| `F5-W0-T08` | RETAIN | 原義保留 |
| `F5-W0-T09` | RETAIN | 原義保留 |
| `F5-W0-T10` | RETAIN | 原義保留 |
| `F5-W0-T11` | RETAIN | 原義保留 |
| `F5-W0-T12` | RETAIN | 原義保留 |
| `F5-W0-T13` | RETAIN | 原義保留 |
| `F5-W0-T14` | RETAIN | 原義保留 |
| `F5-W0-T15` | RETAIN | 原義保留 |
| `F5-W0-T16` | UPDATE | candidate reuse EDGE |
| `F5-W0-T17` | UPDATE | no raw NEG |
| `F5-W0-T18` | RETAIN | 原義保留 |
| `F5-W0-T19` | RETAIN | 原義保留 |
| `F5-W0-T20` | RETAIN | 原義保留 |
| `F5-W0-T21` | RETAIN | 原義保留 |
| `F5-W0-T22` | RETAIN | 原義保留 |
| `F5-W0-T23` | UPDATE | secret masking SEC |
| `F5-W0-T24` | UPDATE | Generic／FHS POS＋NEG；原雙身份保留 |

24 案原 POS／NEG 身份全部保留，不因 W1 新增 13 案而減少。`T24` 的 POS／NEG 在機器 `cases[]` 以單一 kind 呈現時，另在 MD 保 `kind_secondary=NEG` 與原 ID 映射；不以作者 variant 宣原案已驗。

## 4. 凍結方式與反例

凍結順序：先寫 oracle／fixture → 算 SHA → 寫 `cases[]` → 寫本 MD → 算本 MD SHA → 寫 TQAEP JSON 的 `projection_of_sha256` 與同 `cases[]`。看到結果後不得降標、刪 Case、改 threshold 或換 Oracle。

反例：改 Oracle 求綠 → `ORACLE_DRIFT`；只跑 NEG 就宣 POS → `POSITIVE_CASE_MISSING`；以 W0 24 案歷史 `REPORTED` 冒 W1 `OBSERVED` → `EVIDENCE_LAUNDERING`；用同一 raw 檔覆蓋多案 → `RAW_REUSED_ACROSS_CASES`；以字串 command／exit 無 raw → `OBSERVATION_RAW_PIN_MISMATCH`。

可執行 Case 的本地規則實跑見 §5；全量 harness 見交付根 `evidence/FHS-5_PLP_W1_審查修補定案報告.md` 的 A–F／H1–H8；原 17 Guide、66 Bridge、24 W0 案不重跑，並在報告的 NotCovered 明列。


## 5. 可執行 Case 的本地規則實跑（AUTHOR_LOCAL_RULE_ONLY）

13 案中 9 案（7 NEG＋1 SEC＋1 EDGE）在 fixture 具 `request` 與 `predicate`，由 `check/run_cases.py` 對作者規則求值；4 案 POS 仍需原 Bridge／Host／W0 PRIMARY 執行器，保持 `NOT_RUN`。

- 命令：`python check/run_cases.py --pack-root FHS-5_PLP_W1_PRIMARY`
- 輸出：交付根 `evidence/raw/case_rule_results.json`
- 效力：只證明作者規則的可執行性與拒收一致性（`AUTHOR_LOCAL_RULE_ONLY`），**不**證明原 ABI 已被原 Consumer 接受，也不把 NEG 的拒收拿來證明 POS。
- 反例規則：同後綴直送、未 crosswalk 升版、跨 Host 代償、skill bytes 升 Loaded、缺 effect／resume、identity-only 恢復、內嵌指令、workspace 混樹；任一規則若回錯 token 或未拒，`run_cases.py` 必須 exit 2。
