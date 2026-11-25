# FHS-5_PLP_W1_NATIVE_FIRST｜03 W1 TQAEP（主用修補定案）

**File ID**：`FHS5-PLP/W1/CONTROL_PACK/03_W1_TQAEP`
**pack_version**：`W1-NF-r2-CODEX-PRIMARY`
**project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`｜**scope**：`W1-NF-01`
**wave_id**：`W1`｜**batch_id**：`W1-NF-01`｜**date**：2026-11-25（Asia/Taipei）
**source_manifest_ref**：`05_W1_SOURCE_MANIFEST.json`（第六身份讀時衍生）
**Verdict**：文件層 `DOC_CHECK_ACTUAL`；產品層 `PRODUCT_NOT_RUN`。本檔是凍結的 planned cases／oracle／runner 契約，不是產品 PASS。

---

## 0｜分母分帳（不混加、不互抵）

| 分母 | 原量 | 本包處置 | 本輪狀態 |
|---|---:|---|---|
| W1 原 Case | 13 | 全 ID／原義／POS/NEG/child 保留（§1） | planned；`NOT_RUN` |
| W1 原 ECP | 67（38 DEV＋29 OPS） | 01／02 逐 ID 承接 | 文件映射完成；產品 `NOT_RUN` |
| 六 WP | 6 | 00 §5、§5 DAG | dry-consume 完成 |
| ACC | 6 原＋6 CODEX | 00 §3 | 文件層；產品 `NOT_RUN` |
| 14 Named HOLD | 14 | 00 §9、§11 與附件 E5 | 原名／owner／next 保留 |
| Guide 原義務 | `CG-R2-REQ01–16` | §4 全保 | 原義保留；產品 `NOT_RUN` |
| Guide 原 Case | `CG-SEM01–17` | §4 全保 | `NOT_RUN`／`UNBOUND` |
| Bridge 原 FR | `PCB-FR01–17` | §4 全保 | 原義保留 |
| Bridge 原 38＋28 | 66 | §4 分帳 | `NOT_RUN`／`UNBOUND` |
| Bridge Findings／AV3 | `A-PCB-001–022`／`AV3-001–030` | §4 分帳 | 不與本包 13 案互抵 |
| Challenge | `EC-FR01–16`／`C16=F5-T12`／`EC-T01–26`＋`EC-X27–36`／local47 | 後波接口 | 非 W1 前件；`NOT_RUN` |
| FAR | `FAR-FR01–17`／`RQ0–8`／`T20`／`FARP30`／local35／`Q0–10`／十 Advice／七鍵 | Guide2/FAR 接口保留 | W3 全量另驗 |
| FHS Legacy | 22／36／50／39／96／192／485（30/24/25/20/386）；1011=576＋435；35／56 | 分母另帳 | 不阻 Generic；不宣 Fit |
| W0 案 | 24 original＋10 NF＋10 sample＝44 receipts | §3 全 dispositions | `HISTORICAL_REPORTED`，不重跑 |
| TPM | `F01–14`／`U01–16`／`QA26`／35 tools | 00 §6.1；10 UNBOUND 保留 | 能力映射；`NOT_RUN` |

---

## 1｜13 原 Case（fixture/oracle 真 bytes；產品 `NOT_RUN`）

> Fixture/oracle 已複製到本包 `assets/fixtures/`、`assets/oracles/`，SHA 由 05 驗算。它們是作者凍結 fixture，不是原 Host raw。Source span 指 W1M r2（99,289 B／`a91c4ed3…`）之實讀段落；W1M 行號以 `splitlines` 計。

| Case | Kind | Requirement／source span | POS（真可觀測） | NEG／FirstFail | Fixture SHA | Oracle SHA | Runner／actual | Checker／Consumer |
|---|---|---|---|---|---|---|---|---|
| `W1-HOST-01` | POS | W1M §09.1 L889–908；M §11.7 U-017 | CODEX（或指定 Host）同 scope 真 `Consumed` raw：consumer_id、consumed_sha256、readback_at | 無 raw 宣 consumed → `HOST_PENDING`；只讀 H0／briefcheck 不計 | `168aa72567745ebce907c951076323fd2db527e35502ec1ed912f309632a3fda` | `c92846be150cfcfbd9400e5bf23d50ad73b1ca897d10e921ad3120e387573e68` | `W1/check/run_cases_nf.py`（待建）；`NOT_RUN` | 獨立 Checker／真 Host Consumer |
| `W1-HOST-02` | NEG | W1M §09.1；B02 §10 | 正確拒跨 Host 代償，回 `HOST_ABI_DRIFT` | ChatGPT `Loaded` 抵 Hermes `Served` → `HOST_ABI_DRIFT` | `9159143898ac741d8726390d60e776d3065ab40e7cfd3d48027d861c6f5ccea9` | `0af129228279a3b0fa80bd00a696175c6aa649ac7ad2e5f239b434ae0ffaa9fe` | 同上；`NOT_RUN`（舊 `LOCAL_RULE_PASS` 只作歷史） | Checker |
| `W1-HOST-03` | NEG | W1M §09.1；B02 §09 | 拒 skill 可讀升格，回 `HOST_PENDING` | 只讀 `SKILL.md` 宣 Invoked → `HOST_PENDING` | `1d7de26b5528bf6819d9647d52cc54e6c40c1b9adafb752f216422e6d41cc1a6` | `f91f4fbb09a9c66c2f6f6aee9848f9774bc98d3a1c9195c48c6d95aabb55cf6f` | 同上；`NOT_RUN` | Checker |
| `W1-HERMES-01` | POS | W1M §09.1；M §11.7 U-028 | Kanban／Delegation／Swarm 三 child 各有真 raw，缺一即拒 | 三格合併／一格拉三格 → `REQUIRED_CHILD_MISSING` | `8f9f784917c312770e052406e59e06aa7cc35296e176fe06cdd8ba7cd730d79a` | `101103bdcc2475558c02de4162efb5e10a93aa729db8a4b5e4315d928be9edbf` | 待 Hermes；`DEFERRED`／`NOT_RUN` | Hermes Host Consumer |
| `W1-ABI-01` | NEG | W1M §09.1；B03 §05 | 拒 Guide `@2` 直送 Bridge `@2`，回 `EXPLICIT_REVIEW_REQUIRED` | 同尾碼直送 → `EXPLICIT_REVIEW_REQUIRED` | `a0e18b8bfabc41c97d7b2ab368cbda5e6e310d35fd2713cbde4e62868b4de196` | `09e608cd0fae844eac6caac5e5ed5d8f100b1ef484c9f1d21066305865867f19` | 同上；`NOT_RUN` | Checker |
| `W1-ABI-02` | NEG | W1M §09.1；B03 §05 | 拒 proposal-1 未 crosswalk 升 `@2`，回 `LOSSY_MIGRATION` | 只 rename／drop unknown → `LOSSY_MIGRATION` | `9a62f6d1912f1ebf707202882c47916f4e9bcae1420a820fa031358a022f9ae6` | `ea236a6629f8f12222f5d90140a9d2362488b8449da998b4f1d6f1ed6ec90c2f` | 同上；`NOT_RUN` | Checker |
| `W1-SEC-01` | SEC | W1M §09.1；B02 §08 EX-G-S01 | Context 內嵌指令只標 `UNTRUSTED_SOURCE_DATA`，不執行、不升權 | 執行 `ignore permission`／讀 secret／越根 → `UNTRUSTED_SOURCE_DATA`／`SECRET_OR_ESCAPE` | `3a0c56efde4454937375624e485e92f975f68e4862d10b9de4bc8e7c5ab0fc67` | `284675cc464e870b419ffe5e5cec54a9a252cffcf5238b32c020d5b5b45fc82d` | 同上；`NOT_RUN` | Checker＋安全 reviewer |
| `W1-API-01` | POS | W1M §09.1；B03 §07 | 四 API 回完整 Clause/Parent/Child/NEG/Exception/span；非 heading／excerpt | 只回 heading／錯 span／缺 child → `BODY_RESOLVER_UNBOUND` | `5d94e2ddb9cce903900b66ba55e03cf434d899eab321914c0d87ce0817bf0745` | `0d3c5e3256dd4c6cfba30788c5c875222efa0fea50b5d1f842f09fd01ef97443` | 待 P03；`NOT_RUN` | Reviewer／Native Consumer |
| `W1-R3-01` | POS | W1M §09.1；D01/D07 | 以當期 H0/六檔/六冊/plan pins 真 inspect；5+1＋assets 全 match | 用 stale/隱藏 receipt → `AUTHOR_REVIEW_PARTIAL`／`SOURCE_IDENTITY_HOLD` | `c786785e330bf09060b60fe9e8767f637345331f51ab512f1e00a59d210d54bf` | `6f256ac33dafe2a7c21d7cb5a39c099578ba60427d03d280c6923277877d4be3` | 本輪 bootstrap 真跑；文件層 `DOC_CHECK_ACTUAL`；產品 `NOT_RUN` | Native／Checker |
| `W1-R3-02` | NEG | W1M §09.1；本輪 Codex 實例 | 拒 skill bytes 當 Loaded／Installed，回 `HOST_PENDING` | 升格 → `HOST_PENDING` | `52a2009c258c18faa016c8a4a813ca6ac10c2f3b8dc9dcdb60064ed5be0c5f3d` | `6c3b0182b44a2fc850eac9773c85047fb7ba38aae9b533bf04228c5677853aac` | 同上；`NOT_RUN` | Checker |
| `W1-R3-03` | NEG | W1M §09.1；D05 | 拒缺 effect／resume 仍宣完整，回 `ABI_LOSSY_CROSSWALK` | 缺欄 complete → `ABI_LOSSY_CROSSWALK` | `066909b9f3228bca6064a0e4437e3e06183b2e63806ab6653a2323038e0a42ba` | `ce7e1e2092f85091bf9e95337092de7af4b1df8e1e81e1718815007df5ed6caa` | 同上；`NOT_RUN` | Checker |
| `W1-R3-04` | EDGE | W1M §09.1；D06b | workspace 非受影變動與固定 pack bytes 分帳，回 `WORKSPACE_DRIFT_BOUNDED` | 混樹 → `WORKSPACE_DRIFT_BOUNDED`／`DELTA_MISROUTED` | `c6cc18e9c9459f3d7ee260973cb8a4d95d246685ece659675b443120c2534a36` | `b8321db4c322bff2e04baf85d914aa4b4a5360c669987ccb5aeebf8e0aa13eda` | 同上；`NOT_RUN` | Checker |
| `W1-R3-05` | NEG | W1M §09.1；D06 | 拒 CH-07 identity-only 冒可還原舊 bytes，回 `EVIDENCE_LAUNDERING` | 宣可恢復 → `EVIDENCE_LAUNDERING`／`DELTA_MISROUTED` | `59552d7790f88b818f79883d42a5894dfc8a295b80957c5d2eff06ce3f592da2` | `1c6ccd0a53d14f40058fef76ee51d89762c00290280333e3b452c37d43f10b45` | 同上；`NOT_RUN` | Checker |

**共同 ExpectedRaw**（每案至少）：

```
Host:      host_id, manifest, loaded_sha256, installer_ref, policy_epoch
Invocation:command, args, cwd, env_class, exit, stdout_sha256, stderr_sha256, timeout_ms
Served:    served_bytes_sha256, scope_echo, served_at
Consumed:  consumer_id, consumed_sha256, subject, scope, action, readback_at
ABI:       package_sha256, subject, scope, unknown_fields[], legacy_payload
Case:      case_id, kind, requirement_ref, clause_text, oracle_sha256, fixture_sha256, run_id
```

**判定**：每案 verdict 僅 `PASS`／`FAIL`／`NOT_RUN`／`NOT_OBSERVED`／`DEFERRED`／`UNVERIFIED`。本輪只有 `W1-R3-01` 的文件層 bootstrap 為 `DOC_CHECK_ACTUAL`；其餘產品列 `NOT_RUN`／`DEFERRED`。

---

## 2｜W1 當期子例（N01–N04／N10／N11）

| 子例 | 對應 | POS（必真可觀測） | NEG（每負例 fail-closed） | Fixture／Runner | Consumer |
|---|---|---|---|---|---|
| `N01` TPM/Reviewer | QA26／F01–14、W0 T01/03/04 | 真 A+B 複合需求、真不同非 briefcheck 小包，產 PI/PD/DEV/OPS/TQAEP 四類契約；Reviewer 真 Finding＋FirstFail | 缺 B、無源 mandatory、格式對但 bytes 錯、假權限、Reviewer 改 subject → 拒 | 真 source body/span；`tpm_contracts_nf`＋`test_tpm_contracts.py`；`NOT_RUN` | TPM／Reviewer |
| `N02` 六檔 ABI | W1-API/ABI、Bridge 38+28 | 無 15 投影仍四 API 直讀；完整 Clause/Parent/Child/NEG/Exception；舊投影 lossless 另檔 | 錯 schema/type/missing、同尾碼、缺 effect／resume、path escape、unknown drop → 拒 | 本包六檔＋assets；`bridge_nf`／`test_bridge_body.py`；`NOT_RUN` | Native／Reviewer |
| `N03` Guide Delta | SEM17、W3-G2 | 兩模式、四函式；九鍵真雙期全同 → `PARK_NO_DELTA` 候選；逐鍵真差 → `NEW_MATERIAL_EVIDENCE` | 單 evidence_sha、caller bool、缺期、跨 subject/scope、candidate/oracle drift → `DELTA_UNVERIFIED`／`NEW_SUBJECT_REVIEW_REQUIRED` | 兩期真 receipt/context；`guide_nf`／`test_guide_nine_keys.py`；`NOT_RUN` | Guide／Reviewer |
| `N04` Host actual | HOST-01..03、U-017 | CODEX 真 entry/argv/invoke/served/consumed；第二不同材料亦真用 context | skill-only、跨 host、只 hash、缺 raw、exit 0 冒 served → 拒 | 真 host probe／entry；`w1_consumer`＋host ledger；`NOT_RUN` | Native／Host Consumer |
| `N10` OFF／security | NF-T01/05/06/T06 | Legacy/Bridge/Guide 冷 OFF 且 ON/OFF 各自語義成功；正控能阻舊 import；FAR OFF 在 W1 direct 合法 | 兩邊同失敗 parity、secret leak、prompt injection、`..`／absolute／UNC／symlink／junction／reparse／dup key／oversize／outside canary → 拒 | OFF fixture／link canary／safe-path fixture；`NOT_RUN`（本輪只靜態設計） | Host／Security Checker |
| `N11` fresh receive | NF-T10、W4-CONSUMER | 從新根重算 5+1＋26 assets＋identity＋DAG；相對 locator；同 scope case raw | 錯 pin／bytes／path／schema／absolute locator → 不執行、不升格 | `nf_pack_guard verify` 已在本輪真跑（見 §5）；`DOC_CHECK_ACTUAL` | Consumer |

**N05–N09／N12**：W2 Native 多效果、W3 Challenge/FAR 全量、W4 Independent/Release 各自後波；本包只保留接口與必要反例，不預跑、不宣 PASS。

---

## 3｜W0 24 原案 disposition（ID 全保留；不重跑）

| Case | disposition | W1 用途 |
|---|---|---|
| `F5-W0-T01` | UPDATE | POS source anchor；不作 Host raw |
| `F5-W0-T02` | RETAIN | 原義保留 |
| `F5-W0-T03` | RETAIN | 原義保留 |
| `F5-W0-T04` | UPDATE | fake Reader NEG → 鄰接 W1-HOST-02 |
| `F5-W0-T05` | RETAIN | 原義保留 |
| `F5-W0-T06` | UPDATE | path escape SEC → 鄰接 W1-SEC-01 |
| `F5-W0-T07` | UPDATE | proposal-2 NEG → 鄰接 W1-ABI-01 |
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
| `F5-W0-T24` | UPDATE | Generic／FHS POS＋NEG；雙身份保留 |

W0 44 receipts＝24 original＋10 NF＋10 sample；其中 13 policy unit ≠ 44 product E2E。本輪不重跑；歷史 `REPORTED` 不作 W1 `OBSERVED`。

**W0 D01–D08 血緣（原名保留，不重寫歷史）**：

| W0 Delta | 原義 | W1 處置 |
|---|---|---|
| `D01 PRIMARY` | 實體 36 檔／manifest 34 entries；receipt 4,222 vs 清冊 3,986 | `W0_PRIMARY_RECEIPT_STALE` 保留；只作 inspect 輸入，不宣 receipt 已更正 |
| `D02 W0-A` | 6 candidates／G4 3 tests REPORTED／SQS 無 executable oracle | 只作 fixture 類比；不作 W1 Host raw |
| `D03 W0-B` | `NOT_ADMITTED`、13 前件 UNBOUND | 只擋 W2 前件；不擋 W1 ABI/READ |
| `D04 W0-C` | 1011（576 ID＋435 slot）／485／35／56 全 UNVERIFIED、0 install | 分母另帳；不宣 W1/W4 Fit |
| `D05 驗證` | PATCH03 9/9 N、7/7 CH、11/11 F、22 self-check、18 harness、24 cases、6 mutations 為歷史 | `REUSE_AFFECTED_ONLY`；不重跑 W0 全套 |
| `D06 血緣` | CH-07 `743c6cf` vs best-effort `80833a5f` identity-only；25 modified 舊 bytes 不在 | `NOT_COVERED`；不宣舊 bytes 可復原 |
| `D07 guard` | F-05 路徑、F-06 identity、F-08 atomic、F-09 14 records＋self、F-10 FirstFail、F-11 claim ceiling | `REUSE` 為 W1 path/identity/atomic/claim 檢查 |
| `D08 handoff` | `HANDOFF_CANDIDATE` 非 MISSION_COMPLETE；Owner primary≠Original Issuer；T4/T5 HOLD | `RETAIN`；W1 不簽 Release |

**CR 血緣**：`R3-CR01..12`、`F5-CR01..16`、`NF-r2 F5-CR17..25` 原名／原義／owner／next 保留在舊 primary 與 W1M `§10.4`；本包不將任何一項合併銷號，也不因 13 案通過而 close。`F5-CR16` 原配對證據附錄未全掛載，保持 `UNBOUND`；`F5-CR17..25`（含 CI action SHA 等）按真適用性在 W1/W4 另證。

---

## 4｜原具名義務保留（不縮分母）

### 4.1 Guide `CG-R2-REQ01–16`

| ID | 保留義務 | 本包落點 |
|---|---|---|
| `CG-R2-REQ-01` | 真 package bytes／SHA／subject／scope 收件 | 00 §6.2；`receive_package` |
| `CG-R2-REQ-02` | phase/wave/batch 可選但不混身份 | 00 §1 |
| `CG-R2-REQ-03` | 只投影原 PI/PD/ECP/TQAEP/OriginalID | 00 §12；05 refs |
| `CG-R2-REQ-04` | source／claim／applicability 三自檢 | 01 §2；05 authority |
| `CG-R2-REQ-05` | AuthorReady 與 EffectDone 分級 | 00 §2；03 判定 |
| `CG-R2-REQ-06` | 單一純文字薄 START | 04 |
| `CG-R2-REQ-07` | RESUME 只看九鍵 | 00 §6.2；04 |
| `CG-R2-REQ-08` | Effect 六分類只作導覽 | 00 §10 |
| `CG-R2-REQ-09` | FAR 十 Advice 接 Touch2 | 00 §13；03 §6 |
| `CG-R2-REQ-10` | 不建第二 Writer/Checker/Scheduler | 00 §4 |
| `CG-R2-REQ-11` | Frozen Candidate/Evidence/Oracle SHA | 03 §1；05 |
| `CG-R2-REQ-12` | 不可信引文不改權限 | 00 §6.3；03 N10 |
| `CG-R2-REQ-13` | 三 Host 分別載入與回讀 | 02 §4 |
| `CG-R2-REQ-14` | Search-Before-Build | 00 §8 |
| `CG-R2-REQ-15` | 本地 CI 實跑不冒原域 | 03 §5 |
| `CG-R2-REQ-16` | FHS 485／35 分母不降級 | 03 §0 |

### 4.2 Bridge `PCB-FR01–17`

`PCB-FR01` identity；`FR02` raw/alias 安全；`FR03` 分讀 PI/PD/DEV/OPS/TQAEP；`FR04` SPEC/治理；`FR05` Parent/Child/NEG/例外；`FR06` 雙向 trace；`FR07` DEV 欄位；`FR08` OPS 欄位；`FR09` Case/Oracle/POS/NEG/ExpectedRaw；`FR10` phase/batch/applicability；`FR11` Guide→Bridge handoff；`FR12` 三 Host 同義 context；`FR13` before/after delta；`FR14` 缺源安全降級；`FR15` 防內嵌指令；`FR16` 非 FHS 不灌 485；`FR17` 無第二 writer。全部原義保留於 00 §6.3、01/02 與 §5 crosswalk，不因六檔重構刪除。

**另**：`CG-SEM01–17`（17）、Bridge 38＋28（66）、`A-PCB-001–022`、`AV3-001–030`、Challenge／FAR／FHS 分母皆保留；本輪不重跑、不以 13 案核銷。

---

## 5｜文件層實跑與反證（DOC_CHECK_ACTUAL）

**六 WP dry-consume（實讀 00→01/02→03→04→05，不只看檔名）**：

| WP | 00 入口 | 01/02 操作 | 03 驗收 | 04 接續 | 05 證據 | Producer→Consumer |
|---|---|---|---|---|---|---|
| `P01` | §1/§5/§7 | D1；O1 | A01/A05 | SOURCE／P01 | sources／H0 pins／assets | H0/六檔/plugin → CapabilityLedger → P02/P04 |
| `P02` | §6 | D2；O1 | N02 | EXECUTE 2 | digest_contract／legacy 15 refs | 舊 15/6/Guide/Bridge → Crosswalk → P03/P05 |
| `P03` | §6 | D3；O1 | N01/N02/N03 | EXECUTE 3 | 5 MD digest／assets | 真六檔/root/span → 四 API/TPM/Guide → Native/P04 |
| `P04` | §7 | D4；O2–O5 | N04／`W1-HOST-01` | EXECUTE 4 | host_probe／upstream | P03 entry → CODEX invoke/serve/consume → P06 |
| `P05` | §3/§11 | D5；O6 | §1/§2 全 13＋子例 | EXECUTE 5 | checks／mutation raws | frozen case → adversarial report → P03/P06 |
| `P06` | §13 | D7；O6 | §6 | DONE／NEXT | seal／readback | P04/P05 → CLOSEOUT/HANDOFF → W2–W4 |

**實讀結論**：六 WP 都有真 producer／entry／consumer 欄位；P03/P04 的產品 entry 尚未建造，狀態是 `BOOTSTRAP_PENDING` 而非「無 producer 的 hard gate」；P06 的最終 consumed 是 `POST_EVIDENCE`，不反卡 P03。

| 檢查 | 方法 | 期望 | 實際 |
|---|---|---|---|
| 5+1 結構 | `python tools/nf_pack_guard.py verify --root .` | 5 MD＋05、無第七規範檔 | 見證據附件 E7 |
| strict JSON | duplicate-key hook＋`parse_constant` 拒 NaN/Infinity | 05 合法；duplicate/NaN 拒 | 見 E7 |
| 5 MD SHA/bytes/lines | raw bytes 重算，lines＝UTF-8 splitlines | 05 `pack_files` 全 match | 見 E7 |
| identity | 00–04 共同五鍵＋05；第六鍵讀時合成 | 全一致；MD 不含 05 SHA | 見 E7 |
| ID set | 38 DEV／29 OPS／13 Case／6 WP／14 HOLD／12 ACC／D01–09／NF01–10／SM01–07 | 每 ID 至少一次；canonical 表計數正確 | 見 E7 |
| DAG | 05 `dag` edges 拓樸排序 | 無 cycle；P01→P06 | 見 E7 |
| assets | 26 檔 SHA/bytes 對 03/05 | 全 match | 見 E7 |
| sources | 本地可得者 SHA/bytes；遠端缺者記 availability + reason | 無假 digest | 見 E7 |
| 外置 seal | `evidence/SEAL.json` vs 05 raw SHA | match；05 不嵌 seal | 見 E7 |

**隔離 mutation（每項在副本，不改真包）**：改 1 byte、CRLF 轉換、刪 03、duplicate JSON key、NaN、`../` pack path、錯 identity、刪 1 個 DEV ID、DAG 加 cycle、05 自嵌 SHA。期望全部 `REJECT`；實際結果見附件 E7（不以 mutation 通過冒充產品）。

---

## 6｜Observation schema、Checker／Consumer 分離

每 actual 最小欄：`case_id, kind, requirement_ref, child, subject, scope, profile, host, candidate_sha, source_sha, pack_sha, oracle_sha, fixture_sha, runner_id, runner_version, argv, cwd, timeout_ms, expected, observed, exit, stdout_sha256, stderr_sha256, raw_sha256, verdict, first_fail, not_covered, recovery_ref, checker_id, consumer_id`。

Evidence class：`DOC_CHECK_ACTUAL`、`DESIGN_WALKTHROUGH`、`BOOTSTRAP_CONSUME_ACTUAL`、`HISTORICAL_REPORTED`、`PRODUCT_NOT_RUN`、`INDEPENDENT_CHECK`、`CONSUMER_ACTUAL`、`RELEASE_ACTUAL`。一個 raw 可支持多項檢查，但不可把 policy unit 當 product E2E 或把 maker raw 當 independent。

**Checker／Consumer 分立**：Checker 在 Maker 之外的 session/worktree 重跑凍結 case，驗 no-write；Consumer 另外 parse/use 實際材料並回報 action/readback。本輪未綁獨立 Checker／Consumer，故不宣 Independent／Consumed。

---

## 7｜NotCovered 與後續

- 13 原案產品真跑、N01–04/N10/N11 真判、真 W1 runner。
- CODEX 真 served/consumed、第二不同小包。
- W1 plugin 真 Loaded／Installed；GPT CHAT/WORK；HERMES 三 child。
- Windows symlink／junction／reparse 真攻擊（本輪只設計與靜態檢查；不以 WSL2 冒 Windows）。
- W2–W4、Independent、Release、public push。
- 原 Guide 17／Bridge 66／W0 24／Challenge／FAR 全量重跑。

以上不因本包文件合格而消失；後續 04 依 01/02 真授權與 ACL 接續。
