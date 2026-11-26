# 03_W2_TQAEP｜W2 測試、驗收與證據計畫

**artifact_id**：`FHS5-PLP/W2/PACK-NF-20261126-r3`
**subject_id**：`FHS-5_PLP/W2/CONTROL_PACK`
**scope**：`W2-NF-01`
**candidate**：`W2-NF-r3-CODEX-PRIMARY`
**狀態**：`PLANNED / NOT_RUN`
**claim ceiling**：本檔是 planned TQAEP，不是已執行產品驗收

> 本檔把 12 個 W2 原案、N01–N12 跨波反證、J1–J3 的 18 個局部子組，寫成可 freeze、可執行、可逐義判定的驗收計畫。所有 `observed=null`、`verdict=NOT_RUN`，直到在真 candidate／真 Host／真 runner 上取得 actual raw。作者文件層的 `DOC_MUTATION_EXECUTED` 只證明文件包可檢測，**不**證明產品案 PASS。

## 0｜測試治理

### 0.1 基本規則

1. **expected 先於 observed**：oracle／predicate 必須在執行前凍結；不得看到結果再改 expected。
2. **一個 child 一個 observation**：同一 raw 可支持多義務，但每個 child 必須明列對應 observed fields 與判定；不得用一個 hash 生成多項假成功。
3. **POS 全合取**：所有 applicable predicate 真 observed＋identity valid 才 PASS；非空 dict、檔存在、exit 0 都不夠。
4. **NEG 真拒絕**：必須 observed 到 expected token／no protected effect；「沒有報錯」不是 PASS。
5. **NOT_RUN 保留**：缺 runner／fixture／oracle／Host 時寫 `NOT_RUN` 或 `RUNNER_UNBOUND`；不得用作者自檢升 PASS。
6. **觀察層分帳**：author／unit／component／invocation／E2E／Host；W0 policy unit 不抵 W2 E2E；W1 session 不抵 W2 Host。
7. **Checker／Consumer 分立**：Checker 是後驗，Consumer 讀實質；同一人可委派兩個 session，但不得冒不同 principal。
8. **原 12 是唯一 W2 原案分母**：N01–N12 是跨波反證組，不合成新的 12；J1–J3 子組不新增原案分母。

### 0.2 觀察 receipt 最小欄

```text
run_id, subject_id, scope, project_id, wave_id, batch_id, work_id, op_id,
candidate_sha256, source_manifest_sha256, source_set_sha256, pack_sha256,
fixture_sha256, oracle_sha256, case_set_sha256,
argv, cwd, tool_id, tool_version, host_id, principal_ref, policy_epoch, timeout,
exit, stdout_sha256, stderr_sha256, raw_ref, raw_sha256,
expected, observed, verdict, first_fail, reproduction,
pre_ref, post_ref, readback_ref, recovery_ref,
checker_id, consumer_id, observation_layer, not_covered
```

### 0.3 Verdict 語彙

| Verdict | 條件 | 不可 |
|---|---|---|
| `PASS` | 所有 applicable predicate 真 observed＋identity valid＋raw 可重放 | 非空即 PASS |
| `FAIL` | 任一 expected 不成立、NEG 未拒、token 錯、exit0 未 readback | 改名 HOLD 洗掉 |
| `NOT_RUN` | 有 Case 但未執行 | 填 observed |
| `NOT_OBSERVED` | 有執行但未取到必要觀測 | 當 PASS |
| `DEFERRED` | 明文交給後波／其他 owner | 當 PASS |
| `NotCovered` | 已知缺口，保留 owner/resume | 靜默刪除 |
| `UNKNOWN` | 世界不可判，待 reconcile | 改寫成 PASS/FAIL |

### 0.4 本輪作者的 12 案狀態

全部 `PLANNED / NOT_RUN`。`assets/fixtures/*.json` 與 `assets/oracles/*.json` 是**作者設計輸入**，不是已 freeze 的產品 oracle；真 candidate 到 P04 時必須重新 freeze，並在 05 記錄真 SHA。作者 oracle 的 SHA 只證明「設計輸入被固定」，不證明「原域 oracle 已取得」。

## 1｜12 原案逐案

### 1.1 W2-DEV-01（POS）

| 欄 | 內容 |
|---|---|
| requirement_refs | U-013.a RepoContext／U-013.b Pre-Post／U-013.c WriteSet；W2-CODEX-01；W2-A03 |
| child | 三 child 各別 observation；不得用「DEV 已完成」合併 |
| profile／host／effect | Generic DEV／真 repo／`REPOSITORY_WRITE` |
| fixture | `assets/fixtures/W2-DEV-01.json`（**2 target**：MODIFY `W1/check/w2_receiver.py`＋ADD `W1/check/test_j1_receiver.py`，與 `01` §5.1 完全相同；preimage/absence；expected post） |
| oracle | `assets/oracles/W2-DEV-01.json`（exact write set、pre/post SHA、tests、reverse restore） |
| runner | `RUN-DEV-01`（`BUILD_MINIMAL`；真候選上以 actual help 綁 argv） |
| expected predicates | ① caller HEAD=live HEAD；② write set 精確等於 fixture；③ 每 target preimage/absence 真；④ patch 後 post SHA 等於 expected；⑤ affected tests exit/stdio 符合；⑥ reverse 後 preimage 讀回；⑦ unlisted 檔不變 |
| expected_raw_schema | repo pre、patch diff、post hashes、test stdout/stderr、diff raw、reverse raw |
| preconditions | Owner DEV 授權、repo ACL、preimage、recovery、frozen oracle |
| stop/resume | 任一 HARD 前件缺→停；真 receipt 到才 resume |
| checker_route | 分立 Checker 對 frozen candidate/oracle/raw 重跑 |
| not_covered | 原域 DEV ECP、不同 principal、W3/W4 全量 |

### 1.2 W2-DEV-02（NEG）

| 欄 | 內容 |
|---|---|
| requirement_refs | U-013.a；W2-R3-03；J1-T02 |
| child | caller HEAD ≠ live HEAD；另加 stale ACL／stale preimage 子例 |
| fixture | `assets/fixtures/W2-DEV-02.json`（caller_head=h-old、live_head=h-live） |
| oracle | `assets/oracles/W2-DEV-02.json`（`REPO_HEAD_MISMATCH`、write_count=0、target unchanged） |
| expected | 早拒；無 patch／無 write；pre/post target hash 相同；`REPO_HEAD_MISMATCH` 或適用 token |
| stop/resume | 若只做字串比對、未讀 live HEAD，FAIL；真 HEAD 到才 resume |
| not_covered | 真實 race／TOCTOU 由 J1-T04 另行覆蓋 |

### 1.3 W2-OPS-01（POS）

| 欄 | 內容 |
|---|---|
| requirement_refs | U-014.a HostID／U-014.b OS Principal／U-014.c PolicyEpoch／U-014.d Recovery；W2-CODEX-02；W2-A03/A05 |
| child | 四 child 各別 observation；不得用「OPS 已完成」合併 |
| profile／host／effect | 真 Host／真 principal/epoch／`HOST_EFFECT` |
| fixture | `assets/fixtures/W2-OPS-01.json`（host/pre/post/receiver/compensation 形狀） |
| oracle | `assets/oracles/W2-OPS-01.json`（pre/post WorldRaw、receiver consumed、host-specific restore、pre-state readback） |
| runner | `RUN-OPS-01`（`BUILD_MINIMAL`；真 Host receiver 上綁 argv） |
| expected predicates | ① host/principal/epoch/receiver 真；② pre WorldRaw；③ atomic effect；④ post WorldRaw 符合；⑤ receiver parse/use；⑥ compensation 不是 git revert；⑦ pre-state readback |
| expected_raw_schema | host pre、receiver argv/exit、WorldRaw pre/post、receiver receipt、compensation raw |
| preconditions | Owner OPS 授權、Host/OS ACL、output root、preimage、recovery |
| stop/resume | 缺 Host/receiver/recovery→停；真 receipt 到才 resume |
| not_covered | 其他 Host、container/cloud、Publisher |

### 1.4 W2-OPS-02（NEG）

| 欄 | 內容 |
|---|---|
| requirement_refs | U-014.d；W2-A05；J3-T02 |
| child | 把 `git revert` 送成 OPS recovery；另加 `git reset`／全 repo rollback 子例 |
| fixture | `assets/fixtures/W2-OPS-02.json`（recovery_kind=GIT_REVERT） |
| oracle | `assets/oracles/W2-OPS-02.json`（`RECOVERY_KIND_MISMATCH`、effect_count=0、repo 不執行 git） |
| expected | 早拒；zero host effect；不得以 DEV/Repo recovery 代替 |
| stop/resume | 若把 git revert 當 OPS 並實際改世界，FAIL；真 host recovery 到才 resume |
| not_covered | 不同 Host 的 recovery 具體 argv |

### 1.5 W2-EFFECT-01（NEG）

| 欄 | 內容 |
|---|---|
| requirement_refs | W2-B01；ADR-W2-02；W2-CODEX-05 |
| child | 未知 token／path 推斷 operation；fake READ 子例 |
| fixture | `assets/fixtures/W2-EFFECT-01.json`（token=UNKNOWN、path heuristic） |
| oracle | `assets/oracles/W2-EFFECT-01.json`（`EFFECT_UNBOUND` 或 `EFFECT_MAPPING_UNVERIFIED`；no default READ） |
| expected | 停 effect mapping；不得 call effect；不得把未知當 READ |
| stop/resume | 真 typed token 到才 resume |
| not_covered | 原 EffectRegistry 全量 |

### 1.6 W2-AUTH-01（NEG）

| 欄 | 內容 |
|---|---|
| requirement_refs | W2-B06/B07/B08；ADR-W2-02；U-046 |
| child | `permission=true` 無 Issuer；過期 scope；wrong principal |
| fixture | `assets/fixtures/W2-AUTH-01.json`（permission=true、issuer=null、scope_expired） |
| oracle | `assets/oracles/W2-AUTH-01.json`（`FALSE_AUTHORITY`／`NOT_ADMITTED`；pre/post unchanged） |
| expected | 早拒；no effect；不得用 ECP/author 文件代替 |
| stop/resume | 真 Owner/issuer/ACL 到才 resume |
| not_covered | 原域 Issuer 簽章 |

### 1.7 W2-RUNNER-01（NEG）

| 欄 | 內容 |
|---|---|
| requirement_refs | W2-NF-A；W2-CODEX-06 |
| child | 無 runner/oracle/fixture；只有 local unit summary；fake executed |
| fixture | `assets/fixtures/W2-RUNNER-01.json`（runner=null、oracle=null、unit_summary only） |
| oracle | `assets/oracles/W2-RUNNER-01.json`（`RUNNER_UNBOUND`；executed=false；raw=null） |
| expected | 不得宣 executed；不得用非空 summary 抵 |
| stop/resume | 真 runner/version/argv 到才 resume |
| not_covered | 真 runner 的全量案例 |

### 1.8 W2-DELTA-01（POS）

| 欄 | 內容 |
|---|---|
| requirement_refs | J2-T05/T06；W2-B10；Guide 九鍵 |
| child | 同 subject/scope/candidate 的兩期九鍵＋真 verifier；同 firstfail |
| fixture | `assets/fixtures/W2-DELTA-01.json`（period A/B 九鍵、verifier 形狀） |
| oracle | `assets/oracles/W2-DELTA-01.json`（全同→`REUSE_LASTGOOD`；缺 verifier/一期→`DELTA_UNVERIFIED`） |
| expected | 兩期**各自獨立取得**的真 raw；verifier 驗 before/after 與 receipts；candidate/evidence 無受影 delta |
| variants | `same`（九鍵全同→`REUSE_LASTGOOD`）與 `delta`（僅 `world_raw_sha` 一鍵不同→`NEW_MATERIAL_EVIDENCE`／requalify）；兩個都要判對，只判一邊不算 PASS |
| fixture 地位 | `fixture_never_sufficient=true`：fixture 只給形狀，不得以其數值當兩期事實；`fixture-only PARK` 為 forbidden token |
| stop/resume | 無第二期→`DELTA_UNVERIFIED`，不 PARK；真雙期到才 resume |
| not_covered | W3 FAR 七鍵全量 |

### 1.9 W2-R3-01（POS）

| 欄 | 內容 |
|---|---|
| requirement_refs | 13+3 全部；W2-B01..B13、NF-A/B/C；W2-CODEX-05 |
| child | 13 原列各自 owner/receipt；3 NF 分帳；原 null 保持 |
| fixture | `assets/fixtures/W2-R3-01.json`（13 列＋3 NF 的 owner/field/resume 形狀） |
| oracle | `assets/oracles/W2-R3-01.json`（每列有 owner/typed request/receipt route；不得填 true） |
| expected | 13+3 可逐項回取；null 不冒 true；post/Publisher 不當 pre |
| stop/resume | 缺列→FAIL；真 source/receipt 到才 resume |
| not_covered | 原域 13/13 CLOSE |

### 1.10 W2-R3-02（NEG）

| 欄 | 內容 |
|---|---|
| requirement_refs | ADR-W2-04；D02/D03；W2-CODEX-06 |
| child | G4 3 historical tests 當 W2 admitted effect／License Fit |
| fixture | `assets/fixtures/W2-R3-02.json`（G4 444/125/547 bytes＋3 tests reported） |
| oracle | `assets/oracles/W2-R3-02.json`（`NOT_ADMITTED`；不採 G4 作 effect/License Fit） |
| expected | 早拒；不得用 G4 升 W2 |
| stop/resume | 真 W2 candidate/effect 到才另驗 |
| not_covered | G4 原域 |

### 1.11 W2-R3-03（NEG）

| 欄 | 內容 |
|---|---|
| requirement_refs | U-013.b/c；W0-F-08/D06；W2-B09 |
| child | G4/CH-07 歷史 preimage 當真 repo preimage |
| fixture | `assets/fixtures/W2-R3-03.json`（historical_preimage=G4 pre；live_preimage=null） |
| oracle | `assets/oracles/W2-R3-03.json`（`WRITESET_UNBOUND`；no write；原字面保留） |
| expected | 早拒；不得用舊 bytes 補；target unchanged |
| stop/resume | 真 repo preimage 到才 resume |
| not_covered | CH-07 舊 bytes（不存在） |

### 1.12 W2-R3-04（EDGE）

| 欄 | 內容 |
|---|---|
| requirement_refs | W0-F-09；W2-B02/B10；N11 |
| child | 318 manifest vs 317 closeout、不同期 source/receipt |
| fixture | `assets/fixtures/W2-R3-04.json`（318/317 分帳、期別） |
| oracle | `assets/oracles/W2-R3-04.json`（`WORKSPACE_DRIFT_BOUNDED`；分版本/受影；不全域重寫） |
| expected | 分期正確；受影 only；舊 bytes 不偽造 |
| stop/resume | 真期別/pins 到才 resume |
| not_covered | 全 workspace 歷史重驗 |

## 2｜N01–N12 跨波反證映射

| 原 group | W2 適用安排 | 掛點 | 不宣稱 |
|---|---|---|---|
| N01 Source→TPM | 真 W2 六檔 input、TPM structured material；Reviewer 反向 Req/Child/NEG/無源 hard；direct 可用 | P01/P03、R3-01、J2-T01 | 不抵 QA26 |
| N02 six-file ABI | strict raw/SHA/bytes、source span、四 API/BodyResolver、loss/missing/unknown；舊 projection optional | P01/P02/P03、J1/J2 | 不抵 Bridge 38+28 |
| N03 Guide Delta | 真 W2 兩期九鍵、verifier/lastgood、wrong subject/no proof | P02/P06、DELTA-01、J2-T05/06 | 不冒完整 Guide PASS |
| N04 Host actual | 當期 Host invoke/served/consumed；W1 ledger 保；Installed 若 direct N/A reasoned | P02/P05、OPS-01 | 其他 Host 不宣 |
| N05 Native authority/recovery | 真 DEV+OPS+多 op、fake permit/no preimage/錯域/恢復 | P03/P05/P06、DEV/OPS/AUTH；J3 | 不抵 W0/W1 全量 |
| N06 UNKNOWN | timeout/partial/exit0-wrong-semantic 真受界 fixture；先 readback→決策 | P05/P06、OPS-01/O06 | 不把 UNKNOWN 改寫 |
| N07 frozen Challenge | W2 freeze 五 pin/fixture/oracle/case-set/WorldRaw/checker；W3 全量 | P06、RUNNER-01 | 不宣 EC all pass |
| N08 FAR dynamic | known root 可直修；未知研究 typed finding/real source；交 W3 | P06 | 不強制 FAR，不以 UNAVAILABLE=zero |
| N09 combined E2E | W2 當期 source→op→reader→consumer slice；W0 8 segments 不抵 W3/W4 | P01..06、J2/J3 | 本輪 scope |
| N10 OFF/security | J1-T02..06、J3-T02；real import/call controls、path/reparse scoped、同任務 effect+restore | P02/P04/P05/P06 | 保 Windows 未驗限制 |
| N11 fresh receive | clean isolated snapshot、exact pins、case IDs/semantic/raw、wrong pin early reject＋true material consume | J1、J3-T05、P06、W3 entry | 不再讀原 workspace |
| N12 applicability/release | Generic vs FHS、原分母不抵、Publisher 後置；W4 full | 00/03/05、P06 | 不把 W4 倒卡 W2 |

## 3｜J1–J3 局部子組

### 3.1 J1-T01..06

| ID | 類型 | Fixture 形狀 | Expected |
|---|---|---|---|
| J1-T01 | POS | clean relocation＋全 pins＋真 W2 material | accepted=true；parsed/readback；W1 root unchanged |
| J1-T02 | NEG | 逐一改 pack/candidate/oracle/case-set/evidence/handoff pin＋self-consistent seal | 早拒；zero product call |
| J1-T03 | NEG | 缺 raw/entry、empty、duplicate path/key、錯 schema/bytes/hash | 指定 firstfail；非 count-only |
| J1-T04 | SEC | `../`/absolute/UNC/drive-relative/link/reparse/oversize/invalid UTF-8 | 拒；canary 未讀；無越界 |
| J1-T05 | NEG | 錯 producer/scope、缺/假 pin、fake grant、identity split only | 拒；input unchanged |
| J1-T06 | SEC | 失敗 spy/canary；正控真 call/write | 負控 0；正控 >0 |

### 3.2 J2-T01..06

| ID | 類型 | 檢查 | Expected |
|---|---|---|---|
| J2-T01 | POS | 真六檔五列 SourceRefs/EffectConstraints/Context/HostLedger/ChangeCone readback | 五列 source→target→consumer 真值；unknown 明列 |
| J2-T02 | NEG | 改 source id/hash／遺 unresolved/host_effect | 拒或 explicit review；無默默 loss |
| J2-T03 | NEG | context hash/scope/host obs mutation | 無 fake Consumed；`CONTEXT_SCOPE_MISMATCH`／`W2_HOST_BIND` |
| J2-T04 | NEG | ChangeSet 缺失／錯 path/SHA／缺 before／錯 subject | 拒或 `DELTA_UNVERIFIED`；`changeset_present=false` 不 COMPLETE |
| J2-T05 | POS | 真 pre/post＋另一合法同狀態重讀 | 真 delta／同值各正確；九鍵完整 |
| J2-T06 | NEG | 缺 verifier／一期、假 caller true、candidate pin change、cross subject | `DELTA_UNVERIFIED`／原拒絕；不 PARK |

### 3.3 J3-T01..06

| ID | 類型 | 檢查 | Expected |
|---|---|---|---|
| J3-T01 | POS/NEG | POS 錯 expected/nonempty；NEG 未拒/wrong token；exit0 wrong semantic | 對應 FAIL；不得升 PASS |
| J3-T02 | OFF/SEC | 同任務 ON/OFF＋雙敗拒＋leak 正控＋cold isolation | 雙方真成功；forbidden=0；positive control 成立 |
| J3-T03 | POS | affected ECP/ACC child evidence＋frozen pins | 每 child 有對應 raw；pins 不漂移 |
| J3-T04 | POS | final independent rerun/receipt 真新 pin、無 input 修改 | Checker 分立；input 前後不變 |
| J3-T05 | POS | clean relocated receive＋evidence bytes 完整 | 可移植；bytes/SHA 完整 |
| J3-T06 | NEG | fake original oracle／old checker／raw reuse | 拒；`DELTA_UNVERIFIED`／`EVIDENCE_LAUNDERING` |

## 4｜Fixtures／Oracles／Runner

### 4.1 Asset 清單（作者設計輸入）

| Case | Fixture | Oracle | Runner | 狀態 |
|---|---|---|---|---|
| W2-DEV-01 | `assets/fixtures/W2-DEV-01.json` | `assets/oracles/W2-DEV-01.json` | `RUN-DEV-01` | `BUILD_MINIMAL` |
| W2-DEV-02 | `assets/fixtures/W2-DEV-02.json` | `assets/oracles/W2-DEV-02.json` | `RUN-DEV-02` | `BUILD_MINIMAL` |
| W2-OPS-01 | `assets/fixtures/W2-OPS-01.json` | `assets/oracles/W2-OPS-01.json` | `RUN-OPS-01` | `BUILD_MINIMAL` |
| W2-OPS-02 | `assets/fixtures/W2-OPS-02.json` | `assets/oracles/W2-OPS-02.json` | `RUN-OPS-02` | `BUILD_MINIMAL` |
| W2-EFFECT-01 | `assets/fixtures/W2-EFFECT-01.json` | `assets/oracles/W2-EFFECT-01.json` | `RUN-EFFECT-01` | `PREFLIGHT_ONLY` |
| W2-AUTH-01 | `assets/fixtures/W2-AUTH-01.json` | `assets/oracles/W2-AUTH-01.json` | `RUN-AUTH-01` | `PREFLIGHT_ONLY` |
| W2-RUNNER-01 | `assets/fixtures/W2-RUNNER-01.json` | `assets/oracles/W2-RUNNER-01.json` | `RUN-RUNNER-01` | `PREFLIGHT_ONLY` |
| W2-DELTA-01 | `assets/fixtures/W2-DELTA-01.json` | `assets/oracles/W2-DELTA-01.json` | `RUN-DELTA-01` | `PREFLIGHT_ONLY` |
| W2-R3-01 | `assets/fixtures/W2-R3-01.json` | `assets/oracles/W2-R3-01.json` | `RUN-R3-01` | `PREFLIGHT_ONLY` |
| W2-R3-02 | `assets/fixtures/W2-R3-02.json` | `assets/oracles/W2-R3-02.json` | `RUN-R3-02` | `PREFLIGHT_ONLY` |
| W2-R3-03 | `assets/fixtures/W2-R3-03.json` | `assets/oracles/W2-R3-03.json` | `RUN-R3-03` | `PREFLIGHT_ONLY` |
| W2-R3-04 | `assets/fixtures/W2-R3-04.json` | `assets/oracles/W2-R3-04.json` | `RUN-R3-04` | `PREFLIGHT_ONLY` |

### 4.2 Runner 契約

每個 runner 在 P04 必須提供：

```text
runner_id, version, tool_id, argv, cwd, timeout,
input_schema, output_schema, exit_meaning,
fixture_ref/sha, oracle_ref/sha, case_set_sha,
host_requirement, effect_requirement, forbidden_side_effects
```

沒有真 runner 時，記 `BUILD_MINIMAL`／`RUNNER_UNBOUND`，不得寫 `python runner.py <case>` 這種不可重放假 argv。P04 的 runner 可由真 test code 作 oracle，但必須明示 identity；不得事後改 expected。

### 4.3 Asset 治理

1. 作者 fixture/oracle 只作設計輸入；真 candidate 到 P04 時重新 freeze，記真 SHA。
2. 不得先看 observed 再寫 oracle；規格錯需新 rev、新 pins、重驗，舊保留。
3. 有真原域 oracle/fixture 時保原 bytes/version/rights；無則明示 local oracle，不冒充原域。
4. Asset 不新增規範；不得把 asset 當第七 canonical 檔。
5. 缺 asset／runner／Host 時，對應 case `RUNNER_UNBOUND`／`NOT_RUN`，不阻不受影 READ。

## 5｜6+6 ACC 的 Case 對位

### 5.1 W2-A01..06

| ACC | 主要 Case／檢查 | 次要 |
|---|---|---|
| W2-A01 Source | R3-01、J1-T02/T03 | N01/N02 |
| W2-A02 Binding | R3-01、R3-03、DEV-02 | N02 |
| W2-A03 ECP | DEV-01、OPS-01/02 | AUTH-01 |
| W2-A04 Admission | AUTH-01、OPS-01 | J1-T05 |
| W2-A05 Recovery | DEV-01、OPS-01/02、DELTA-01 | J3-T02 |
| W2-A06 Split | R3-01、R3-04 | 15→6 dry-consume |

### 5.2 W2-CODEX-01..06

| ACC | 主要 Case | 產品出口 |
|---|---|---|
| W2-CODEX-01 真 DEV | DEV-01/02 | exact diff/tests/readback/restore |
| W2-CODEX-02 真 OPS | OPS-01/02 | WorldRaw/receiver/compensation |
| W2-CODEX-03 多 op | DEV-01＋OPS-01（UNKNOWN 子例掛 OPS-O06／N06，不新增原案） | 每 op 各自前件/raw |
| W2-CODEX-04 UNKNOWN | OPS-06、DELTA-01 | 四類 observed＋reconcile |
| W2-CODEX-05 13+3 | R3-01/EFFECT-01/AUTH-01 | 逐項 owner/receipt/null |
| W2-CODEX-06 12 原案 | 全部 12 | expected/raw/NOT_RUN |

## 6｜執行順序、Freeze 與 Stop/Resume

### 6.1 順序

1. P01/P02：source/effect binding、J1 靜態/safe read；不執行 effect。
2. P03/P04：ECP＋fixture/oracle/runner freeze；J1 修補的 ECP 在此。
3. P05：Owner admission 後，先 DEV-A 或 OPS-A；每 op 立即 readback。
4. P06：per-op reconcile、12 案 verdict、J3 final Checker、Consumer。

### 6.2 Freeze 規則

- 先 freeze source/candidate/case-set/oracle/fixture，再跑；proof pin 不循環。
- evidence manifest 收 raw/bytes/SHA；Checker/Consumer 對封存 core 的指紋與同 candidate，後置 append。
- 不為嵌入自身收據反覆更新 manifest；具名 self-excluded list＋outer binding。
- 不以 evidence SHA 當 candidate；不以 Git blob SHA 當 raw SHA256；不把 CRLF 正規化後 digest 冒原 bytes。

### 6.3 Stop / Resume

| 缺口 | 停止 | 仍可繼續 | Resume |
|---|---|---|---|
| 真 runner/oracle | 受影 case | 其他 case／READ | 同 candidate freeze |
| 真 Host | OPS case | DEV 設計／TQAEP | 真 Host/principal |
| 真 repo | DEV case | OPS 設計／TQAEP | 真 repo/preimage |
| Owner admission | effect | 文件/READ | 同 scope receipt |
| Checker | independent claim | author self-check | distinct receipt |

## 7｜原分母與 NotCovered

| 集合 | 本包處理 | 不抵扣 |
|---|---|---|
| W0 44 receipts（10 sample＋24 原＋10 NF） | 歷史 pattern；M1–M3 受影 reuse | 不作 W2 PASS |
| W1 20 observations／79 tests／118 matrix | baseline scoped；J1–J3 血緣 | 不作 W2 原案 PASS |
| WM1..4 55 Case | 本波只 12 原案 | 不把 W3/4 前移 |
| B01 QA26／B02 完整 Guide／B03 38+28／B04 EC 全量／B05 FAR 全量 | 受影引用 | 不以本包核銷 |
| FHS 1011/576/435/485 | PROFILE_ONLY/OPEN | 不填假 ID |

**NotCovered（本輪）**：真 W2 runtime repo/host/ACL/preimage/receiver、真 12 case raw、真 Checker/Consumer、W3 Challenge/FAR 全量、W4 Release、原域 13/13 CLOSE、Windows reparse 全覆蓋。

## 8｜Claim

| 項 | 值 |
|---|---|
| TQAEP | `PLANNED` |
| 12 原案 | 全部 `NOT_RUN` |
| Assets | 作者設計輸入；真 SHA 見 05 |
| 可宣 | 每案有 expected/fixture/oracle/runner route/stop/resume |
| 不可宣 | 任何 W2 原案 PASS、產品驗收、Independent／Release |
