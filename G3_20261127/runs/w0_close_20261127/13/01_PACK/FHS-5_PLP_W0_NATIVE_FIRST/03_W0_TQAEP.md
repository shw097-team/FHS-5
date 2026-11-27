# 03_W0_TQAEP｜B0-NF Planned Assurance

**identity**：`FHS-5_PLP/W0`｜**batch**：`FHS-5/W0/B0-NF`｜**pack**：`W0-NF-r3-CODEX-PRIMARY`  
**source W0M**：`NF-r3-PRIMARY` `a1f186cc337a4b3828e53f77533df5c97fdda63e132521d861a79b884f0c3aef`  
**claim**：`PLANNED_NOT_EXECUTED`｜**product verdict**：`NOT_RUN`

> 本檔是 B0 可施工 TQAEP，不是已跑 Raw。`F5-W0-T01..24` 是原 Case 身份；`NF-T01..10` 是 Native-first 架構否證。兩組可共用真 raw trace，但分母不混、不重複計數。所有 `PASS` 僅指文件/plan 檢查，產品 verdict 必須由後續具權 Runner/Checker 產生。

## 00｜Assurance 原則

1. **Source/Req 先行**：每個 case 有 source、Requirement/Child、Owner。
2. **Oracle 先凍結**：Fixture/Oracle/expected exit 在執行前由 Checker 或具權規格 Owner 凍結。
3. **Expected/Actual 分欄**：不得用作者表格冒充 raw。
4. **獨立性**：Maker 與 Challenger/Checker 分 session/worktree；Checker 與 Consumer distinct receipts。
5. **分母分帳**：原 24、NF-T 10、QA26、CG-SEM17、38＋28、C16/36/47、RQ0–8、FARP30 不互相抵銷。
6. **共用 raw**：同一真執行可支撐多個 case trace，但 numerator 只計一次；不為湊數重跑。

## 01｜原 24 Case 逐案處置

| Case／類型 | 處置 | Input／注入 | Expected／Oracle（exit/status） | Runner／方法 | FirstFail | NotCovered |
|---|---|---|---|---|---|---|
| `F5-W0-T01` POS | KEEP | 真 source bytes＋合法 READ | source SHA/span/root 一致；無 OPS/Publisher Gate；`0`／`READ_OK` | 真 file read＋hash；source inventory | `SOURCE_IDENTITY` | 無（B0 必需） |
| `F5-W0-T02` NEG | KEEP | source 改一 byte | `SOURCE_INTEGRITY_FAILED`；舊 trace 不沿用；`3` | mutation fixture；expected hash mismatch | `SOURCE_INTEGRITY_FAILED` | 無 |
| `F5-W0-T03` NEG | KEEP | A 有、B 缺 | parent 不 PASS；`missing=["B"]`；`2` | `case_missing.md`；CLI/Reviewer | `REQUIRED_CHILD_MISSING` | 無 |
| `F5-W0-T04` NEG | REPLACE | 自造 OriginalID/Reader ACK | 不得升格；合法 direct READ 不被阻；`no-op` | 假 ID/receipt 不接受 | `FALSE_AUTHORITY` | 無 |
| `F5-W0-T05` NEG | KEEP | Guide 擴 Scope A→B | scope/write-set 不變；clarify/拒 | ThinStart mutation；compare allowlist | `GUIDE_SCOPE_DRIFT` | 無 |
| `F5-W0-T06` SEC | KEEP＋強化 | `../`、absolute、UNC、symlink/junction/reparse | 不讀 root 外；source hash 不變；`3/INVALID_PATH` | §03.2 path 生成＋outside canary | `BRIDGE_BOUNDARY_FAIL` | symlink 建立失敗時該子例 `NOT_VERIFIED` |
| `F5-W0-T07` EDGE | OPTIONAL | legacy proposal-1→2 或 unknown required field | 舊相容另帳；新版 reject/保真，不靜默丟 | 新 consumer unknown-schema 負例 | `SCHEMA_UNSUPPORTED` | Legacy proposal 半 `DEFER` |
| `F5-W0-T08` NEG | KEEP | code 可見但 Host 未 bound | `BIND/ACTIVATE`，不判 CODE_MISSING | capability probe；no synthetic missing | `HOST_CAPABILITY_UNBOUND` | HERMES 專屬 activation 移至 Compatibility，不阻 CODEX |
| `F5-W0-T09` NEG | KEEP | 注入 W4 Release 作 W0 READ 前置 | `PHASE_OVERREACH_CANDIDATE`；READ 可走 | 靜態 DAG/trace review | `PHASE_OVERREACH_CANDIDATE` | 無 |
| `F5-W0-T10` NEG | KEEP | 同操作 post-readback 作 admission 前置 | cycle；不執行該 effect | DAG edge review；`12`/`12'` 區分 | `GATE_CYCLE_CANDIDATE` | 無 |
| `F5-W0-T11` NEG | REPLACE | `permit=true`／越 write-set／無真 grant | no-op；pre/post 不變；`NOT_ADMITTED` | 真權限檢查；假 permit 實驗 | `FALSE_AUTHORITY` | 真 grant 若未取得，只驗 no-op 半 |
| `F5-W0-T12` NEG | REPLACE | unknown effect alias | `EFFECT_MAPPING_UNVERIFIED`，不默認 READ | no-op 負例；不建 Registry | `EFFECT_MAPPING_UNVERIFIED` | 無 |
| `F5-W0-T13` POS | KEEP | 真授權 DEV/OPS | pre/post/readback/recovery 正確；`0` | 多筆受界可逆 DEV＋本地 CODEX OPS | `EFFECT_NOT_VERIFIED` | 外部 Host/Legacy Profile 另驗 |
| `F5-W0-T14` NEG | KEEP | exit 0 但 output/state 錯 | `EFFECT_NOT_VERIFIED` | controlled mutation；checker 判 semantic | `EFFECT_NOT_VERIFIED` | 無 |
| `F5-W0-T15` NEG | KEEP | Challenge 改 subject/oracle | 拒收；該證據不採用 | hash mismatch/candidate mutation | `ORACLE_DRIFT` | 無 |
| `F5-W0-T16` EDGE | KEEP | candidate 變更重用舊 raw | frozen identity mismatch；只重驗受影 | new candidate digest；stale raw | `CANDIDATE_CHANGED` | 無 |
| `F5-W0-T17` NEG | KEEP | 只有文字，無 argv/exit/raw | `UNREPRODUCED/NOT_PROVEN` | negative input；no raw | `UNREPRODUCED` | 無 |
| `F5-W0-T18` NEG | KEEP | source 不可達卻 `zero_results` | `RESEARCH_REQUIRED/ABSTAIN`；不填 0 | simulated unavailable；status split | `ZERO_FROM_UNAVAILABLE` | 無 |
| `F5-W0-T19` NEG | REPLACE | FAR 無真 raw 或越 Owner scope 自 CLOSE | 不 `FIX_NOW/CLOSE` | advice policy test；scope check | `FALSE_CLOSE` | Fabric 三源 `DEFER` |
| `F5-W0-T20` EDGE | KEEP | 同名 FirstFail 但有新 raw | 不直接 PARK；重鑑定受影 | old/new raw pair；delta check | `NO_DELTA_REWRITE_DENIED` | 無 |
| `F5-W0-T21` NEG | KEEP／簡化 | 無新 delta 反覆重派 | 停同質重派；不建 PARK service | retry log；same key | `NO_DELTA_REWRITE_DENIED` | 無 |
| `F5-W0-T22` NEG | KEEP | Guide CLOSE 但無 Checker/Publisher | 不得 RELEASE；`CLOSEOUT_ADVICE` | closeout advice test；no publisher | `RELEASE_NOT_CLAIMED` | Publisher |
| `F5-W0-T23` SEC | KEEP | 包內 secret sentinel | 不外流；redaction；不入 raw | secret sentinel fixture；scan | `SECRET_LEAK`／`EVIDENCE_LAUNDERING` | 無 |
| `F5-W0-T24` POS/NEG | KEEP＋profile | Generic OFF READ；FHS 缺適用 ID | Generic 可 READ；FHS 適用子集缺 ID 拒；485 全量 DEFER | OFF cold start；profile applicability | `PROFILE_GATE_DRIFT` | FHS 485 全量 `DEFER` |

**處置統計**：24/24 有落點；`KEEP` 17、`KEEP／簡化` 1（T21）、`REPLACE` 4（T04/T11/T12/T19）、`OPTIONAL` 1（T07）、`KEEP＋Profile-scoped DEFER` 1（T24）。統計只是文件處置，不是 pass rate。

### 01.1 B0 分母

B0 的必需分母是 `T01..T24` 的必要語義（T07 Legacy 半、T24 485 全量半可 `DEFER`）＋`NF-T01..10`。T04/T08/T09/T10/T12 可與 B0 的來源、能力、phase、cycle、effect 判定共用真 trace，但每個原 case 都需 verdict 或 NotCovered。不得只用 `case_ok`/`case_missing` 兩個 fixture 代表全部。

## 02｜NF-T01..10 架構否證

| Case／Req | 執行 | Oracle／判定 | FirstFail | NotCovered／失敗意義 |
|---|---|---|---|---|
| `NF-T01/R08` | 隔離 profile 不載入 HGK/FABRIC/SBL/FHS/PIPD；cold-off B0 read/test；記 load/import/call trace | 同 scope parity；無 hard import | `ARCHITECTURE_REWORK_REQUIRED` | Fabric 原 Profile `DEFER` |
| `NF-T02/R01/R03` | 無 OriginalReader；真 file/Git pin；Bridge/direct；hash/path 負例 | source SHA/span；越界拒 | `FALSE_READER` | 假 Reader 前置/安全被移除 |
| `NF-T03/R04/R10` | 無 EffectRegistry/Issuer service；真 sandbox/OS gain；write/run＋restore；越權 no-op | pre/post/readback/recovery；越權無效 | `EFFECT_NOT_VERIFIED` | 無法安全執行/誤允許 |
| `NF-T04/R05` | 無 CaseRegistry/Runner；stdlib/repo runner POS/NEG；checker 不改 oracle | argv/exit/raw；oracle 先凍結 | `RUNNER_UNBOUND` | 無法實跑/假驗收 |
| `NF-T05/R03/R08` | Bridge OFF；direct pack read；與 ON 比較 | direct 可完成；Bridge 專屬另驗 | `OFF_PARITY_UNPROVEN` | Bridge ON 專屬案 `DEFER` |
| `NF-T06/R06/R07` | FAR OFF；明確 bug direct patch/retest；FAR ON 另驗兩方案 | 明確錯不被研究 gate 卡死 | `FALSE_RESEARCH_GATE` | FAR ON 的 Fabric 專屬 `DEFER` |
| `NF-T07/R01–R06` | 五方 individual：TPM/Reviewer、Guide、Bridge、Challenge、FAR | 每方真輸入/輸出/consumer | `FALSE_CAPABILITY` | 未安裝的方 `NotCovered` |
| `NF-T08/R01–R07` | 真協作：req→四契約→start→run→frozen challenge→research→patch→resume→retest | 每段真 raw；NotCovered 明列 | `UNREPRODUCED` | 外部 Host/Legacy 另驗 |
| `NF-T09/R07` | 真 red/controlled mutation→patch→new candidate→affected regression | 實質差額；同質停 | `NO_DELTA_REWRITE_DENIED` | 無 |
| `NF-T10/R09` | 新 session/consumer 真讀 pack/pin/raw/next；錯版拒 | consumer action/readback；W1 差額 | `HANDOFF_UNCONSUMED` | W1 准入另層 |

## 03｜Sample fixtures／args／expected

### 03.1 Fixture bytes／產生方法

以下 `PLANNED_FIXTURE`；Checkers 先凍結 bytes/SHA，Maker 只讀。檔案一律 UTF-8 無 BOM、LF（除 `case_bad_utf8.md` 為原始 bytes）。

| Fixture | 精確 bytes（或以 hex 表示） | 用途 |
|---|---|---|
| `case_ok.md` | `- [x] A\n- [x] B\n` | R1/R9 POS |
| `case_missing.md` | `- [x] A\n` | 缺 B；exit 2 |
| `case_dup.md` | `- [x] A\n- [x] A\n- [x] B\n` | duplicate A；exit 3 |
| `case_bad_path.md` | `path-escape descriptor\n`（真正的 outside/absolute/UNC/symlink 由 §03.2 臨時建立） | path escape；exit 3 |
| `case_bad_utf8.md` | hex `2d 20 5b 78 5d 20 41 0a ff 0a` | invalid UTF-8；exit 3 |
| `case_ambiguous.md` | `- [x] A\n- [x] B\n- [x] B\n` | 重複 B；exit 3 |
| `case_malformed.md` | `- [A\n-\n- [x] B\n` | 格式錯誤；exit 3 |

**`case_hash_mismatch` 不另建檔**：使用 `case_ok.md` 的 bytes，CLI 傳入錯誤 `--sha256`；expected `3/SHA_MISMATCH`。此為 W0M §08.3 的明確要求，避免第二來源。

### 03.2 CLI／Expected mapping（子項與 SAMPLE 對齊）

| SAMPLE 子項 | Fixture／argv | Exit | Status | Oracle／不可接受 |
|---|---|---:|---|---|
| R1 path absolute／`..`／UNC | `case_bad_path.md` + 臨時 outside canary；`--input ../canary.md`、absolute、UNC | 3 | `INVALID_PATH` | 不讀 root 外；不洩露路徑/canary |
| R1 symlink／junction／reparse | `$Root\escape_dir` junction→outside；`escape_link` 若可建 | 3 | `INVALID_PATH` | 不跟隨；source/outside bytes 不變 |
| R1 invalid UTF-8 | `case_bad_utf8.md` | 3 | `INVALID_ENCODING` | 不回顯原文 |
| R1 hash mismatch | `case_ok.md`＋錯 `--sha256` | 3 | `SHA_MISMATCH` | 不先 COMPLETE |
| R2 missing B | `case_missing.md` | 2 | `MISSING` | `missing=["B"]`；parent fail |
| R2 duplicate | `case_dup.md` | 3 | `INVALID_DUP` | 不因一個有效 PASS |
| R2 ambiguous | `case_ambiguous.md` | 3 | `INVALID_FORMAT` | fail closed |
| R2 malformed | `case_malformed.md` | 3 | `INVALID_FORMAT` | fail closed |
| R3 stable JSON | `case_ok.md` 兩次 | 0 | `COMPLETE` | stdout 同值 |
| R4 reversible output | output wrapper | 0 | `COMPLETE` | source unchanged；output 可刪 |

**Path 生成**：見 `01_W0_DEV_ECP.md` §05.3；使用 `$env:TEMP` 隨機 root/outside，`New-Item -ItemType Junction` 與 `SymbolicLink`（後者失敗記 `NOT_VERIFIED`）。測試必須斷言 stdout/stderr 不含 `OUTSIDE_CANARY_DO_NOT_READ`，且 outside canary 檔的 `LastWriteTime`/SHA 不變。

## 04｜Oracle／Runner／Independence

| 資產 | 要求 |
|---|---|
| Oracle | Checker/規格 Owner 先凍結 expected exit/status/JSON/semantic |
| Fixture | 真 bytes/SHA；不含 secret；Maker 只讀 |
| Candidate | commit/tree or hash manifest；含 source/oracle/case pins |
| Runner | 真 pytest/unittest/CLI；記錄 cwd/argv/env/timeout |
| Checker | 獨立 session/worktree；不改 candidate/oracle |
| Consumer | 同 Scope distinct receipt；不得與 Checker 共用一個簽章 |
| Evidence | argv/exit/stdout/stderr/raw SHA、pre/post/recovery |

## 05｜五 pin、Finding、Receipt

| 欄 | 要求 |
|---|---|
| `pins.source` | 來源 raw SHA |
| `pins.candidate` | 變更後 tree/manifest SHA |
| `pins.evidence` | raw bytes/SHA |
| `pins.oracle` | 凍結 oracle SHA |
| `pins.case_set` | case/fixture set SHA |

**八欄 Finding**：`id,severity,class,subject_sha,command,exit,raw_sha256,reproduction`。expected/observed/oracle/source/case/next 另放 evidence，不修改 strict schema。

**Receipt**：

```text
run_id, case_id, candidate_sha, source_sha, fixture_sha, oracle_sha,
cwd, argv, env, timeout, exit, stdout_sha, stderr_sha,
pre_state, post_state, recovery_ref, expected, observed,
verdict, first_fail, checker_id, consumer_ref, not_covered
```

`expected` 與 `observed` 分欄；`NOT_RUN` 不填 PASS；`UNBOUND` 不填 ZERO。

## 06｜B0 工作流

```text
select G4 or briefcheck
→ freeze source/requirements/fixtures/oracle
→ run POS/NEG/security
→ freeze candidate/evidence
→ independent Challenge
→ FAR finding + ≥2 alternatives
→ Guide resume / direct fix
→ patch under 12'
→ affected retest + consumer readback
```

Challenge 不得改 candidate/oracle；FAR 不得發 WorkOrder/Grant/Release；Maker 不得自簽 independent verdict。

## 07｜NotCovered／分母

| 分母 | 本輪 |
|---|---|
| 24 原 Case | 文件 mapping；產品 `NOT_RUN` |
| 10 NF-T | planned；產品 `NOT_RUN` |
| QA26／F01–F14 | W0 只代表；完整 W1 |
| CG-SEM17／20／50 | Guide 代表；完整 W1/W3 |
| Bridge 38＋28 | 四 API 代表；完整 W1 |
| C16/EC-36/local47 | 另帳；不混 |
| RQ0–8／FARP30／local35 | 代表；Fabric 另 Profile |
| FHS 22/36/50/39/96/192/485 | Generic 不背；Profile 另驗 |

## 08｜Stop／FirstFail

| FirstFail | 處置 |
|---|---|
| `RUNNER_UNBOUND` | 只做 plan；不寫 verdict |
| `ORACLE_UNBOUND` | 不跑受影 case |
| `EVIDENCE_LAUNDERING` | 拒假 raw；重取 |
| `ORACLE_DRIFT` | 停；回 Spec/Checker |
| `FALSE_INDEPENDENT` | 失敗；分離 session |
| `CANDIDATE_CHANGED` | 新 revision；舊 raw 失效 |
| `UNREPRODUCED` | 不接受為 Finding/Pass |
| `ZERO_FROM_UNAVAILABLE` | 拒；`RESEARCH_REQUIRED` |

## 09｜Not claimed

`PRODUCT_CASES=NOT_RUN`、`NF_T=NOT_RUN`、`B0_VALIDATED=NO`、`INDEPENDENT_ACCEPTED=NO`。本檔只提供後續 Runner/Checker 的可施工 TQAEP。
