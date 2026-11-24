# FHS-5_PLP_W0 證據型附錄（非規範）

## E0 身份／Claim

| 欄 | 值 |
|---|---|
| Task | `FHS5-PLP-W0-CODEX-REVIEW-REPAIR-20261123-01` / PATCH-03 |
| Subject | `FHS-5_PLP/W0/CONTROL_PACK` |
| project_id | `FHS-5_PLP` |
| subject_id | `FHS-5_PLP/W0` |
| scope | `W0-A/B/C AUTHOR CONTROL PACK; SOURCE_READ+ISOLATED_DRAFT_WRITE; W0-B NOT_ADMITTED` |
| wave_id | `W0` |
| batch_id | `W0-CODEX-REPAIR-20261123-01` |
| source_manifest_sha256 | `22eebb6c002179b6e7401c29b3c1a2877a208b73b68f1e62f50c0b63f786ef7f` |
| claim ceiling | `AUTHOR_CONTROL_PACK_CANDIDATE_PASS_WITH_HOLDS` |
| original domain | `UNBOUND` |
| LastGood | pre-challenge `743c6cf` identity; PATCH-03 candidate tree in `CANDIDATE_MANIFEST.json` |

## E1 真 SourceLedger

| source_id | role | bytes | lines | SHA-256 |
|---|---|---:|---:|---|
| `M` | 最高作者端藍圖 | 325511 | 3016 | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` |
| `B00` | Program Master | 79605 | 528 | `fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2` |
| `B01` | Reviewer/TPM-SP | 48177 | 405 | `3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49` |
| `B02` | Guide | 47039 | 398 | `1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441` |
| `B03` | Bridge | 39898 | 326 | `9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0` |
| `B04` | Challenge | 40665 | 332 | `619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066` |
| `B05` | FAR | 51163 | 380 | `f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4` |
| `WM` | 全 WM | 286201 | 2080 | `d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2` |
| `W0MB` | W0M candidate 正文 | 29460 | 324 | `3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd` |
| `W0ME` | W0M candidate 附錄（非規範） | 11799 | 136 | `0c5e89e451260fe2f8ae7050a89313ba3e9a4850e4c49d4bc59f5954b79ffd09` |
| `W0M-CTRL` | W0M 控制包方法參照 | 27088 | 250 | `d9cdf61b5f5f4e3bfc616d2fe5410bfc0c553e0769deb258f933cd2832933cd3` |
| `CTRLW0` | 本任務控制包 | 36913 | 264 | `a9fca81717c980e8522a322323f68847281d7037a1b792b46b6e56ffa9207814` |
| `STARTW0` | 本任務啟動薄 | 4247 | 27 | `6acf3020064700d0e365cd33674a98f66778701d46d8897eaa1ab86162970e0d` |

13/13 bytes/lines/SHA re-read; `SELECTED_ONLY`, not CORE16. `SOURCE_REFERENCE_HASH_CONFLICT` bounded to W0M historical CTRL/START; W0 pack impact NONE.

## E2 OriginalID／WP／Case／Seam／Tool Applicability

### 14 WP

| WP | Name | This round |
|---|---|---|
| `F5-W0-01` | SourceFreeze | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-02` | PluginIdentity | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-03` | PI-Reviewer | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-04` | W0M-PD | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-05` | W0-Control | AUTHOR_COMPLETE_LOCAL |
| `F5-W0-06` | GuideThinStart | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-07` | BridgeRead | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-08` | NativeRead | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-09` | FrozenChallenge | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-10` | ResearchCandidate | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-11` | GuideResume | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-12` | NativeProtected | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-13` | OriginalAssurance | NOT_RUN_OR_CONDITIONAL |
| `F5-W0-14` | Delta-Handoff | NOT_RUN_OR_CONDITIONAL |

### 24 Case（原 M §12.7；全 CASE_UNBOUND）

| Case | Type | Line | Expected (excerpt) | State |
|---|---|---|---|---|
| `F5-W0-T01` | POS | L1014 | SourceAnchor/Scope 正確，無新 OPS Gate | `CASE_UNBOUND` |
| `F5-W0-T02` | NEG | L1015 | `SOURCE_INTEGRITY_FAILED`，不得沿用舊 Trace | `CASE_UNBOUND` |
| `F5-W0-T03` | NEG | L1016 | Parent 不得全 PASS／開具名 Child 缺件 | `CASE_UNBOUND` |
| `F5-W0-T04` | NEG | L1017 | `ORIGINAL_READER_UNBOUND`，拒升格 | `CASE_UNBOUND` |
| `F5-W0-T05` | NEG | L1018 | Source mismatch/Clarify，不能覆蓋 W0 原 Scope | `CASE_UNBOUND` |
| `F5-W0-T06` | SEC | L1019 | 不讀出 admitted root，不寫被審來源 | `CASE_UNBOUND` |
| `F5-W0-T07` | EDGE | L1020 | `EXPLICIT_REVIEW_REQUIRED`，保留未知欄位 | `CASE_UNBOUND` |
| `F5-W0-T08` | NEG | L1021 | 分類 BIND/ACTIVATE，不假定 CODE_MISSING | `CASE_UNBOUND` |
| `F5-W0-T09` | NEG | L1022 | 報 `PHASE_OVERREACH_CANDIDATE` | `CASE_UNBOUND` |
| `F5-W0-T10` | NEG | L1023 | `GATE_CYCLE_CANDIDATE` | `CASE_UNBOUND` |
| `F5-W0-T11` | NEG | L1024 | 無原 Issuer Receipt → 不做 DEV/OPS | `CASE_UNBOUND` |
| `F5-W0-T12` | NEG | L1025 | `EFFECT_MAPPING_UNVERIFIED`，不默認 READ | `CASE_UNBOUND` |
| `F5-W0-T13` | POS | L1026 | 真 World/Repo effect SHA/Oracle 可觀察 | `CASE_UNBOUND` |
| `F5-W0-T14` | NEG | L1027 | 不標 Effect Verified | `CASE_UNBOUND` |
| `F5-W0-T15` | NEG | L1028 | Subject mutation 拒收、撤 Challenge Claim | `CASE_UNBOUND` |
| `F5-W0-T16` | EDGE | L1029 | Frozen identity mismatch → re-challenge affected | `CASE_UNBOUND` |
| `F5-W0-T17` | NEG | L1030 | `UNREPRODUCED/NOT_PROVEN` | `CASE_UNBOUND` |
| `F5-W0-T18` | NEG | L1031 | `UNAVAILABLE/BLOCKED/ERROR ≠ ZERO` | `CASE_UNBOUND` |
| `F5-W0-T19` | NEG | L1032 | 缺真 Original Reader/World Raw→`RESEARCH_REQUIRED` | `CASE_UNBOUND` |
| `F5-W0-T20` | EDGE | L1033 | 不能 PARK；依受影 Delta 重讀 | `CASE_UNBOUND` |
| `F5-W0-T21` | NEG | L1034 | `PARK_UNTIL_DELTA` **僅在真兩期證據成立時** | `CASE_UNBOUND` |
| `F5-W0-T22` | NEG | L1035 | `CLOSEOUT_ADVICE` 不得 RELEASE | `CASE_UNBOUND` |
| `F5-W0-T23` | SEC | L1036 | 敏感資訊遮罩，不外流 | `CASE_UNBOUND` |
| `F5-W0-T24` | POS | L1037 | Generic READ 通；FHS 適用 ID 不得被省略 | `CASE_UNBOUND` |

### 7 Seam

| Seam | Contract |
|---|---|
| SM-01 | SourceReader → Reviewer/PI: SHA/span/Parent/Child/NEG |
| SM-02 | PI → Wave/PD: AffectedPISlice/BindingRequest |
| SM-03 | PD → DEV/OPS ECP/TQAEP: pre/post/readback/recovery/Case/Oracle |
| SM-04 | Wave W0 → Guide1: six identities + ThinStart |
| SM-05 | Guide/Bridge → Executor: four APIs + path/ABI loss policy |
| SM-06 | Executor → Challenge → FAR: Frozen/POS/NEG/Raw or UNREPRODUCED |
| SM-07 | FAR → Guide2 → Consumer: RESEARCH_REQUIRED/WAIT/RESUME/PARK only |

### W0-C denominators

| Set | Declared | Entries | Shrink |
|---|---:|---:|---|
| W0 Core WP | 22 | 22 | NO_SHRINK |
| Edge | 36 | 36 | NO_SHRINK |
| H1 | 50 | 50 | NO_SHRINK |
| ModeGate | 39 | 39 | NO_SHRINK |
| Oracle | 96 | 96 | NO_SHRINK |
| Cell | 192 | 192 | NO_SHRINK |
| ToolNeed | 485 | 485 | NO_SHRINK |
| Reviewer Tool | 35 | 35 | NO_SHRINK |
| User Subintent | 56 | 56 | NO_SHRINK |

1011 entries; 485 ToolNeed IDs match M §20.4; 35 T01–T35; 56 U-001–U-056; all `UNVERIFIED`; 0 tools installed.

## E3 Local QA／Destructive Raw

| Check | Subject | Result | Evidence |
|---|---|---|---|
| PK-Q01 | 15 normative + appendix exist/readback | **PASS** | candidate 28 files + appendix |
| PK-Q02 | SOURCE_MANIFEST 13/13 bytes/lines/SHA | **PASS** | 13/13 |
| PK-Q03 | six identities, wave W0 | **PASS** | 14 file records + 1 top-level |
| PK-Q04 | MD substance Input/Operation/Output/Consumer/NEG/FirstFail | **PASS** | 15 files non-empty |
| PK-Q05 | PACKAGE_FILE_MANIFEST 27 entries, no self hash | **PASS** | 27/27 |
| PK-Q06 | TQAEP projection_of_sha256 | **PASS** | 88ca6d0c… |
| PK-Q07 | 24 F5-W0-T01..24 retained | **PASS** | 24/24 CASE_UNBOUND |
| PK-Q08 | per-case Oracle/Fixture/expected raw | **HOLD** | ORACLE_FIXTURE_UNBOUND; original runner absent |
| PK-Q09 | READ/DRAFT vs B protected; no phase overreach | **PASS** | NOT_ADMITTED; no W4 gate |
| PK-Q10 | Human Owner vs original Issuer/Checker | **PASS** | original UNBOUND |
| PK-Q11 | seven seams + path/ABI | **PASS** | 27 paths, 0 escape |
| PK-Q12 | POS/NEG raw, UNAVAILABLE not zero | **PASS** | 7/7 NT; no fake raw |
| PK-Q13 | FHS denominators 22/36/50/39/96/192/485/35/56 | **PASS** | 1011/1011 |
| PK-Q14 | evidence appendix + delivery index | **PASS** | E0-E6 + index |

Destructive: source byte tamper → `SOURCE_INTEGRITY_FAILED`; TQAEP case drop → `TQAEP_PROJECTION_MISMATCH`; claims true → `CLAIM_CEILING_VIOLATION`; `../` → `PATH_OUTSIDE_ROOT`; string receipt → `ORIGINAL_READER_UNBOUND`; M 12.7 edit → `M_SECTION_12_7_VERIFY` fail. 6/6 detected.

## E4 ABI／BodyResolver／Authority

| 欄 | 值 |
|---|---|
| original_pi_ref / pd / ecp / tqaep | `null` |
| original_reader_state | `UNBOUND` |
| execution_admission_receipt | `null` |
| independent_checker_receipt | `null` |
| publisher_receipt | `null` |
| body resolver | local selected sources + pack copies; original reader unbound |
| proposal-1/2 | `EXPLICIT_REVIEW_REQUIRED` for legacy proposal-1 consumers |

## E5 CR／HOLD／Resume

| HOLD | Owner | Resume predicate |
|---|---|---|
| `W0-A_CASE_SELECTION` | Original Project/Source Owner + Case/Oracle Owner | Original Project/Source Owner designates one non-FHS candidate for W0-A (candidate case id + requirement/case/oracle bytes + expected result + ACL + typed receipt), or records typed ReasonedNA. |
| `W0-B_NOT_ADMITTED` | Original Issuer/Repo/Host/OS Principal | Original Issuer/Repo/Host supply typed OperationType, RepoContext, HostID/OS Principal/PolicyEpoch, exact WriteSet/preimage, WorkOrder, ExecutionAdmission, WorldReader/RepoReader and recovery ABI under the same Subject/Scope. |
| `ORIGINAL_READER_UNBOUND` | Original PIPD Reader / Case Owner | Typed readback with reader name/version, subject, scope and source SHA. |
| `ORACLE_FIXTURE_UNBOUND` | Original Case/Oracle Owner | Real Case/Oracle/Fixture bytes plus SHA under the same Subject/Scope. |
| `HOST_CAPABILITY_UNBOUND` | Host Owner | Four-stage host evidence under the same Host/PolicyEpoch. |
| `CHECKER_PUBLISHER_UNBOUND` | Original Protected Checker / Publisher | Same Candidate/Scope/Host/PolicyEpoch independent receipt. |
| `SOURCE_REFERENCE_HASH_CONFLICT` | W0M Author / Original W0M Owner | W0M domain owner supplies typed provenance; W0 pack impact is already NONE. |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` | FHS Profile Owners (Program/Architecture/System/Case-Oracle) | Original ID lists plus Owner/locator for each denominator, or an explicit ReasonedNA ruling. |

## E6 Delivery

15 normative files + 13 body-resolver sources + this appendix + review report + `DELIVERY_INDEX.json` + `CANDIDATE_MANIFEST.json` + `CANDIDATE_RECEIPT.json`. See `DELIVERY_INDEX.json` for path/bytes/SHA.
