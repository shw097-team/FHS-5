# FHS-5_PLP/W0｜W0-NF CODEX-first CLOSEOUT

**project**：`FHS-5_PLP`｜**subject**：`FHS-5_PLP/W0`｜**batch**：`FHS-5/W0/B0-NF`  
**date**：2026-11-25（Asia/Taipei）｜**stage**：`W0`（B0-NF）  
**pack**：`W0-NF-r3-CODEX-PRIMARY`（`artifact FHS5-PLP/W0/PACK-NF-20261125-03`）  
**pack manifest SHA-256**：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`  
**W0M amendment**：`CODEX-FIRST-r4`，SHA-256 `c9b1ca9bbcd5ce87fdbcb0fc373cb8c36d1ad8d404b55c4f7311fc6c2bbddfd5`  
**baseline (public main)**：`43ac7581da1c9b280d5fb4e5b968e70635d945bf`  
**candidate preimage**：`5eab43de2d3f67d6afbb1c5f6bc390e2c391da36`（v2）  
**candidate final**：`bb66a276aae8c5d6aef549832c523587fc47d247`（v3，`12'`）  
**verdict**：`B0_NF_VALIDATED`｜`W0_NF_VALIDATED`  
**round**：`W0-NF-HARDEN-20261125-02`（最小補強：NF-T08／Consumer／symlink／OFF）
**W1**：`W1_TECHNICALLY_READY`；`W1_EXECUTION_READY` = `NOT_CLAIMED`  
**not_claimed**：`NATIVE_PASS_FOR_OTHER_HOSTS`、`INDEPENDENT_PASS_WITH_DIFFERENT_PRINCIPAL`、`W1–W4 COMPLETE`、`FHS 485 FULL`、`RELEASED`、`EXTERNAL_OS_REPO_HOST_GRANT`

> 本檔只記錄本輪可重播的實際證據。`PASS` 指對應 receipt 的 argv/exit/raw 與凍結 oracle 相符；不指 W1–W4 全分母、其他 Host、原域 Publisher 或 Release。

## 1｜Identity 與來源

| 欄 | 實際值 |
|---|---|
| decision | `W0-CODEX-FIRST-20261125-01`、`W0-OPS-NATIVE-20261125-01`、`B0-SAMPLE-CODEX-20261125-01`、`W0M-NF-PRIMARY-20261125-01` |
| write root | `C:\Projects\Agent_Workspace\FHS-5_Workspace\13_W0_NF_CODEX_20261125` |
| pack files | 5 MD + manifest；5/5 SHA 與 bytes 相符（`01_PACK`） |
| external seal | `01_PACK/EXTERNAL_SEAL.json`；manifest self hash 不內嵌 |
| repo (workspace) | `shw097-team/FHS-5` 公開 clone，main `43ac758`；local branch `codex/b0-nf-20261125` |
| candidate repo | `02_CANDIDATE/repo`（由 `12_B0_NF_CODEX/01_B0_NF/repo.bundle` clone） |
| OpenSpec | 2.0.0；change `w0-nf-codex-20261125`；`openspec validate --strict` 通過 |

## 2｜A／B／C disposition

| 線 | disposition | 實際證據 | NotCovered |
|---|---|---|---|
| `W0-A` 來源、PI/Review、Guide、Bridge、READ/DRAFT | `OBSERVED_LOCAL_SLICE` | 5/5 pack pins；四契約＋兩 gate；Reviewer exit 0／0 defects；Guide Touch1/Touch2；Bridge 四 API | 完整 U26/CG-SEM17、Bridge 38+28 |
| `W0-B` 本地 Native DEV/OPS | `NATIVE_LOCAL_PASS_WITH_NOT_COVERED` | v2→v3 red→patch→retest；O1–O5；output/readback/restore；OFF imports `[]` | 原域 OS/Repo/Host grant、不同 principal |
| `W0-C` FHS Legacy／Profile | `PROFILE_SCOPED` | Generic OFF 可讀；FHS 缺 ID 被拒（`PROFILE_GATE_DRIFT`）；485 全量 `DEFER` | FHS 22/36/50/39/96/192/485 完整回歸 |

## 3｜14 WP disposition

| WP | disposition | 退出證據 |
|---|---|---|
| `F5-W0-01` SourceFreeze | `PASS` | manifest＋5 檔 SHA/bytes；`01_PACK` |
| `F5-W0-02` PluginIdentity | `PASS_WITH_BINDING_NOTE` | Reviewer plugin 實跑；Bridge 重用；Guide/FAR/Challenge `BUILD_MINIMAL`；未偽造 Host install |
| `F5-W0-03` PI/Reviewer | `PASS` | `03_PARTIES/tpm/pi.json`、`pd.json`、`dev_ecp.json`、`ops_ecp.json`；缺 B／無源 gate；Reviewer 0 defects |
| `F5-W0-04` W0M-PD | `PASS` | PD 綁定 repo `5eab43d`、write-set、preimage |
| `F5-W0-05` W0-Control | `PASS` | 六檔未改；manifest 相符 |
| `F5-W0-06` GuideThinStart | `PASS` | `PACKAGE_FIRST`、九鍵、`SCOPE_DRIFT` 拒、`HOLD_NO_DELTA` |
| `F5-W0-07` BridgeRead | `PASS` | inspect/explain/render/compare；path/scope/cross-subject 拒 |
| `F5-W0-08` NativeRead | `PASS` | 41 案真 subprocess＋1 案 import-trace；2 案 composite path suite 明列 4 個 sub_runs；44 receipts 全部有 exit/raw |
| `F5-W0-09` FrozenChallenge | `PASS` | 五 pin；frozen oracle；獨立 process／隔離副本 |
| `F5-W0-10` ResearchCandidate | `PASS` | FAR 真 Finding、3 方案、10 advice、七鍵 |
| `F5-W0-11` GuideResume | `PASS` | ThinResume；同質即 `HOLD_NO_DELTA` |
| `F5-W0-12` NativeProtected | `PASS` | DEV v3＋OPS O1–O5；pre/post/restore |
| `F5-W0-13` Assurance | `PASS` | 32 checks、0 findings、五 pin；Maker/Checker 分 process／隔離副本 |
| `F5-W0-14` Delta/Handoff | `PASS` | CLOSEOUT／HANDOFF／CHANGESET；consumer `consumed=true` |

## 4｜24 原 Case＋10 NF 真 verdict

分母：SAMPLE 10＋`F5-W0-T01..24`＋`NF-T01..10` = 44 receipts；**44 PASS、0 FAIL**。逐案 receipt 在 `05_TQAEP/receipts/`，匯總 `05_TQAEP/summary.json`。

| Case | verdict | 關鍵 observed |
|---|---|---|
| `SAMPLE-R1..R10` | `PASS` | R2 `MISSING ["B"]` exit 2；R3 `INVALID_DUP`；R5 `INVALID_ENCODING`；R6 `SHA_MISMATCH`；R7/R8 `INVALID_FORMAT`；R9 兩次同值；R10 output 寫入後刪除、source SHA 不變 |
| `F5-W0-T01` | `PASS` | requirements SHA `fc4608…` 相符 |
| `F5-W0-T02` | `PASS` | 一 byte mutation 後 SHA 不符，拒舊 trace |
| `F5-W0-T03` | `PASS` | 缺 B → exit 2、parent FAIL |
| `F5-W0-T04` | `PASS` | 假 ACK／`permit=true` → `FALSE_AUTHORITY` no-op；direct READ 仍可 |
| `F5-W0-T05` | `PASS` | 擴 Scope → `SCOPE_DRIFT` exit 3 |
| `F5-W0-T06` | `PASS` | Windows：`..`／absolute／UNC／junction 均 `INVALID_PATH`；WSL2 ext4：真 file/dir symlink 亦 `INVALID_PATH`，root 內 link 正向 `COMPLETE`；canary 未讀、SHA 不變 |
| `F5-W0-T07` | `PASS` | 未知 schema → `SCHEMA_UNSUPPORTED`；未知欄保真；Legacy 半 `DEFER` |
| `F5-W0-T08` | `PASS` | code 存在、console 未 bound → `BIND_EXISTING`，非 `CODE_MISSING` |
| `F5-W0-T09` | `PASS` | `W0_READ → W4_RELEASE` → `PHASE_OVERREACH_CANDIDATE`；READ 可走 |
| `F5-W0-T10` | `PASS` | `OP ↔ POST_READBACK` → `GATE_CYCLE_CANDIDATE`；不執行 |
| `F5-W0-T11` | `PASS` | 假 permit no-op；sentinel pre/post SHA 相同 |
| `F5-W0-T12` | `PASS` | 未知 effect → `EFFECT_MAPPING_UNVERIFIED` |
| `F5-W0-T13` | `PASS` | CLI exit 0 且 OPS PASS |
| `F5-W0-T14` | `PASS` | exit 0 但語義不符 → `EFFECT_NOT_VERIFIED` |
| `F5-W0-T15` | `PASS` | oracle 一 byte 變更 → `ORACLE_DRIFT` |
| `F5-W0-T16` | `PASS` | 舊 candidate raw 重用 → `CANDIDATE_CHANGED` |
| `F5-W0-T17` | `PASS` | 文字宣稱無 argv/exit/raw → `UNREPRODUCED` |
| `F5-W0-T18` | `PASS` | 來源不可達 → `UNAVAILABLE`、`zero_results=null`、`RESEARCH_REQUIRED` |
| `F5-W0-T19` | `PASS` | 無 raw → `FALSE_CLOSE`；有 raw 才 `CLOSE_PERMITTED` |
| `F5-W0-T20` | `PASS` | 新 raw → `REQUALIFY`；完全相同 → `NO_DELTA_REWRITE_DENIED` |
| `F5-W0-T21` | `PASS` | 同 key 三次 → 停重派 |
| `F5-W0-T22` | `PASS` | 無 Checker/Publisher → `CLOSEOUT_ADVICE`／`RELEASE_NOT_CLAIMED` |
| `F5-W0-T23` | `PASS` | 合成 secret → `SECRET_LEAK`；redacted 無 secret |
| `F5-W0-T24` | `PASS` | Generic `GENERIC_OK`；FHS 缺 ID → `PROFILE_GATE_DRIFT`；485 `DEFER` |
| `NF-T01` | `PASS` | 模組清單無 HGK/FABRIC/SBL/FHS/PIPD/HERMES；marked 環境 parity |
| `NF-T02` | `PASS` | 無 OriginalReader；真 file pin；path 負例 |
| `NF-T03` | `PASS` | 無 Registry/Issuer；真 pre/post/restore |
| `NF-T04` | `PASS` | stdlib unittest 12/12；oracle 先凍結 |
| `NF-T05` | `PASS` | direct 路徑未匯入 `w1_bridge_reference`；import-time 正控可偵測 Bridge；Bridge ON 專屬案未涵蓋 |
| `NF-T06` | `PASS` | FAR OFF 時明確 bug 可直接 patch／retest |
| `NF-T07` | `PASS` | 五方各有真 invocation 證據：TPM meta exit、Guide pack_ok、Bridge 四 exit、Challenge checks、FAR raw pin |
| `NF-T08` | `PASS` | 協作鏈完整：契約→start→run→challenge→FAR→patch→resume→retest |
| `NF-T09` | `PASS` | red exit 1 → patch → 12 tests＋2 probe OK |
| `NF-T10` | `PASS` | consumer interim `accepted=true`；錯 pin 拒 |

## 5｜五方 individual／combined

| 方 | 實作 | 實際結果 | 證據 |
|---|---|---|---|
| TPM＋Reviewer | 四契約生成＋真 `plp-tpm-review 1.0.1` `review_core.py` | `REVIEW_SOURCE_LOCATED_ONLY`；0 defects；10 authority/reader unbound；缺 B／無源 gate 正常 | `03_PARTIES/tpm/` |
| Guide | `BUILD_MINIMAL` `tools/guide.py` | `PACKAGE_FIRST`；5/5 pack；九鍵；Touch1/Touch2；scope 拒 | `03_PARTIES/guide/` |
| Bridge | `REUSE` `w1_bridge_reference.py`（SHA `dc0d1041…`） | inspect 24 declared／0 mismatched；explain 9 cases；render；compare 1 changed；三項安全拒 | `03_PARTIES/bridge/` |
| Challenge | `BUILD_MINIMAL` `tools/challenge.py`，獨立 process／隔離副本 | 32 checks、0 findings、五 pin；NF-T10 由 consumer 另行釘住 | `03_PARTIES/challenge/challenge.json` |
| FAR | `BUILD_MINIMAL` `tools/far_run.py` | F-W0NF-001；RQ0–8；3 方案；10 advice；七鍵；false close 拒 | `03_PARTIES/far/` |

Combined：`NF-T08` 收據串接契約→Guide→DEV→OPS→Challenge→FAR→`12'`→resume→retest，各段有 raw。

## 6｜Native DEV／OPS actual

| 項 | 實際 | 證據 |
|---|---|---|
| Host | Windows 10.0.26200；Python 3.11.9；Git 2.53.0；Codex CLI 0.169.0-alpha.11.1 | `04_DEV_OPS/ops.json` O1 |
| Host ref | `CODEX-LOCAL-…`（只記截斷 hash，不記原名） | O1 |
| Principal ref | `principal-…`（只記截斷 hash） | O1 |
| Red | invalid `--root` → traceback、exit 1；`INVALID_ROOT_TRACEBACK` | `04_DEV_OPS/raw/red_v2.*` |
| Patch `12'` | try/except + `is_dir`；commit `bb66a27` | `04_DEV_OPS/patch_12prime.diff` |
| Retest | probe 2/2 OK；suite 12/12 OK | `04_DEV_OPS/raw/green_v3*` |
| OPS O2 | POS exit 0 COMPLETE；NEG exit 2 MISSING | `ops.json` |
| OPS O3/O4 | output 寫入、readback、刪除回 absent；source 不變 | `ops.json` |
| OPS O5 | import trace 無 legacy；marked parity | `04_DEV_OPS/off.json` |
| Recovery | 只刪本次 output；preimage `5eab43d` 可回 | `dev_patch.json` preimage |

## 7｜Assurance

| 欄 | 值 |
|---|---|
| Checker | `tools/challenge.py`；separate process＋isolated copy（不寫 subject `.git`）；same OS principal（如實記錄） |
| Oracle | `05_TQAEP/oracle.json`，SHA `112f2902656f1122720ef275ac954e3422f896267f144f27d321fa138be382c6` |
| Case set | 44 receipts；`case_set` SHA 見 `challenge.json` pins |
| Checker pins | source `fc460883…`；candidate `bb66a27`；evidence `19e57b0d…`（43 candidate receipts，checker 重算，排除 consumer-staged T10）；oracle `112f2902…`；case_set `9624e71d…` |
| Verdict | `PASS`；32 checks；0 findings |
| Consumer | `07_CONSUMER/CONSUMER_MANIFEST.json` 釘住 receipt＋raw；handoff 另釘其 SHA |
| FirstFail | red `INVALID_ROOT_TRACEBACK`；已修補並只回歸受影 cone |
| LastGood | pack `e3772aee…`＋candidate v2 `5eab43d`＋v2 evidence（`12_B0_NF_CODEX`） |

## 8｜Claim ceiling

| Claim | 值 | 依據／限制 |
|---|---|---|
| Pack | `PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION` | 六檔＋seal |
| B0 | `B0_NF_VALIDATED` | 五方＋DEV/OPS＋Challenge/FAR＋OFF＋consumer |
| W0 | `W0_NF_VALIDATED` | 44 必要案＋14 WP；W1–W4 全分母不在本閘 |
| W1 technical | `W1_TECHNICALLY_READY` | W0 validated＋handoff＋consumer readback |
| W1 execution | `NOT_CLAIMED` | 需上位採納與 W1M／下一包一致 |
| Release | `NOT_CLAIMED` | 無 Publisher |

## 9｜NotCovered（不計入 PASS）

- W1 `38＋28`、C16／EC-36／local47、FARP30／local35、U26／CG-SEM17、QA26 完整分母。
- FHS 22/36/50/39/96/192/485 完整回歸（本次 `DEFER`）。
- HERMES／GPT CHAT／GPT WORK 主機執行與相容性。
- 不同 OS principal 的獨立簽章；本次為同 principal 的 process/worktree 分離。
- symlink 已在 WSL2 ext4 實測（Windows 本機無 `SeCreateSymbolicLink`，未提權）；Windows junction 另測。
- 原域 Original OPS ECP、Original Reader、Issuer、Publisher。

## 10｜Next legal action

1. W1 以本 HANDOFF pins 為基線，不從零重建；先 requalify 14 HOLD＋R3-CR。
2. W1M／下一包需與本 pack／candidate 一致，才可升 `W1_EXECUTION_READY`。
3. 完整分母另案；不把本 44 案當 W1–W4 通過。
4. HERMES Compatibility 另立工作包。
5. GitHub 上推：Owner 批准後已 fast-forward `43ac758..f3add20` 至
   `shw097-team/FHS-5` main；remote raw 已驗 HTTP 200。

## 11｜來源內部不一致的 reconcile（保留封存）

`01_PACK/FHS-5_PLP_W0_Native-first_CODEX_修補證據型附錄.md` §E10 記錄的是
**上一輪 `12_B0_NF_CODEX` 的歷史結果**（pins `5eab43d / ef977e / 3cc26e / 93c7f9`），
與本 pack `00_W0_PI_PD.md` §00.3／§10.1 的作者狀態 `B0 NOT_RUN` 並存，屬來源內部時間差。

- 該附錄 **未修改**（封存 SHA `f1fe41a6…`，bytes 20,291），僅在本輪 manifest 標 `superseded_annex`。
- 本輪 CLOSEOUT 不引用該附錄的 pins 或 verdict 作證據。
- 本輪所有 pins 均由 `03_PARTIES/challenge/challenge.json` 與 `05_TQAEP/summary.json` 重新產生。
- Reason：不以歷史附錄洗白本輪，也不覆寫封存來源。

## 12｜獨立審查與本輪修正

本輪在交付前由一個獨立 agent session 做 read-only 對抗審查（未修改任何檔），
其 `INDEPENDENT_REVIEW_FAIL` 的 13 項已被逐項處理：

| # | 原 finding | 處置 | 修正後證據 |
|---:|---|---|---|
| 1 | 封存附錄 §E10 與 pack §00 狀態衝突 | 保留封存；manifest 標 `superseded_annex`；本輪不引用 | §11、`EVIDENCE_MANIFEST.json.superseded_annex` |
| 2 | 34/44 receipt 的 argv/exit 由 verdict 推導 | 41 案真 subprocess＋1 案 import-trace；2 案 composite 明列 sub_runs；無 verdict 推導 exit | `receipts/*.json.execution_kind` |
| 3 | T02 為 tautology | `integrity_gate.py` 真跑，exit 3、`SOURCE_INTEGRITY_FAILED` | `F5-W0-T02.json` |
| 4 | 13 案由常數 stub 判分 | `policy_cli.py` 每案兩面控制（fake/valid、overreach/legal、same/new…）；屬 policy unit test，非候選產品碼 | 各 policy receipt `controls` |
| 5 | NF-T07 只看檔案存在 | 改檢查真 invocation 證據：TPM meta exit、Guide pack_ok、Bridge 四 exit、Challenge checks、FAR raw pin；改稱 `PARTIES_INVOKED` | `NF-T07.json` |
| 6 | OFF/parity 空泛 | 改 prefix detector＋`hgk_core` 負控；parity 改標「env marker invariance」 | `04_DEV_OPS/off.json.detector_control` |
| 7 | Checker 獨立性與 NO-WRITE 空窗 | 隔離副本；NO-WRITE 快照跨全程；加 `NO-GIT-WRITE`（HEAD/index/worktrees）＋mutant 自測；並 prune 舊 worktree 登記 | `challenge.json` `MUTANT-DETECTABLE`、`NO-WRITE`、`NO-GIT-WRITE` |
| 8 | Oracle 未凍結、3/5 pins 自導 | `frozen_at`＋candidate pin；evidence/case_set 由 checker 重算；case_set 含 fixture/expected | `challenge.json` `PIN-RECOMPUTE` |
| 9 | T05 主題錯置 | 改由 `policy_cli` 呼叫 Guide，in-scope/out-of-scope 兩面 | `F5-W0-T05.json` |
| 10 | symlink 標示不一致 | symlink 不再計入 `ok`；Challenge 記 `not_verified`；T06 `not_covered` 明列 | `challenge.json.not_verified` |
| 11 | Bridge counts 表面矛盾 | summary 加 reconciliation notes | `bridge_summary.json.reconciliation_notes` |
| 12 | Guide pin 過期、RQ3 誇大 | Guide 於 v3 後重跑；FAR RQ3 只列 R11 | `guide/thin_start.json`、`far.json` |
| 13 | 肯定項 | 真 red→patch、真 junction path suite、claim ceilings 保留 | `dev_patch.json`、`F5-W0-T06.json` |

**`12'` 套用方式**：以完整檔替換寫入 `briefcheck.py`，再以 `git diff` 產生
`patch_12prime.diff` 作為變更描述（blob `563ab34..ec43559`）。未以 `git apply`
重放該 diff；此點如實記錄。

**殘留限制**：`oracle.frozen_at` 為建立凍結檔時的標記，非外部時間戳服務；
`guide.delta.evidence_sha` 在 Touch1 起點為 `null`（尚無 evidence），Touch2 才填；
policy T 案是 `policy.py` 的單元測試，不是候選產品碼的行為。

## 13｜本輪最小補強（A／B／C／D）

### A｜NF-T08 真協作閉環

| 段 | producer → consumer | 實際 pin／結果 |
|---|---|---|
| Source→TPM | pack → 四契約＋Reviewer | manifest `e3772aee…`；Reviewer exit 0／0 defects |
| TPM→Guide | 契約 → ThinStart | `PACKAGE_FIRST`；delta candidate `bb66a27` |
| Guide→Bridge | pack → 四 API | inspect mismatched 0；explain 9 cases；三項安全拒 |
| Bridge→Native | Bridge pin → v2 red→`12'`→v3 | preimage `5eab43d`；red exit 1；patch `d785e3ee…`；retest 12 tests＋probe 0 |
| Native→Challenge | v2 clone → frozen Finding | `CH-F-W0NF-001`；raw `4be2c111…` |
| Challenge→FAR | Finding → RQ0–8／3 方案 | FAR finding 同一 id；chosen `ALT-1`；evidence `4be2c111…` |
| FAR→Guide Resume | MaterialDelta → Touch2 | `RESUME`；findings 含 `CH-F-W0NF-001`；candidate `bb66a27` |
| Resume→Retest | v3＋凍結 oracle | challenge PASS；44 receipts |

- 驗證器：`tools/collab_chain.py`，8 segments／20 checks，verdict `COMBINED_OK`。
- 斷鏈負例 7 個全部拒絕：missing raw、wrong candidate、wrong oracle、no challenge、wrong finding、no patch delta、cross subject。

### B｜Consumer fail-closed＋NF-T10

- `tools/consumer.py` v3：先核 identity／pack／seal／W0M／candidate／oracle／handoff／evidence **667 檔索引**（SHA/bytes／路徑 confinement），全部通過才跑 POS/NEG。
- 每次 run 唯一 `run_id`＋獨立 `runs/<id>/` raw，不覆寫。
- 正向：前輪 782 checks；本輪 clean-receive **803 checks**（§15），POS 0/COMPLETE、NEG 2/MISSING。
- 負例 10 個全部 `cli_executed=false`：wrong pack／candidate／oracle／evidence、mutated raw、missing file、bad schema、duplicate pin、cross subject、path escape。
- NF-T10 由 consumer 收據最終化，Checker 不重複自簽；Consumer Manifest 外部 `.sha256` 釘住。

### C｜Symlink／reparse 安全

- Windows 本機無 `SeCreateSymbolicLink`（WinError 1314，未提權）→ 依既有 WSL Ubuntu-24.04／Python 3.12.3／uid 1000 隔離環境補驗。
- 真 file symlink、dir symlink、相對 symlink、root 內正向 link 皆實建。
- 8 案例：POS `COMPLETE`；`..`／absolute／UNC／file link／dir link／relative link 全部 exit 3／`INVALID_PATH`；root 內 link 正向 `COMPLETE`。
- canary 未讀、outside/source SHA 不變；測試後清理，不跟隨 link 刪 target。

### D｜Legacy／Bridge／FAR OFF 真隔離

| OFF | 隔離方式 | 結果 |
|---|---|---|
| Legacy | `sitecustomize` import blocker（hgk/fabric/sbl/fhs/pipd/hermes）＋正負控制 | 6 個 B0 入口（briefcheck 正負、Reviewer、Guide、Bridge inspect/explain）全部同結果、0 blocked attempts |
| Bridge | `w1_bridge_reference` import 阻斷＋Native direct reader | 9 cases 同集合；pack SHA 相同；direct 不依賴 Bridge |
| FAR | 停用 FAR 路徑，v2 clone 套 `12'` diff | patch exit 0；post==v3；suite 0；probe 0；`far_tool_invoked=false` |

**Claims**：`B0_NF_VALIDATED`、`W0_NF_VALIDATED`；`W1_TECHNICALLY_READY`（consumer 782 checks／10 negatives）；`W1_EXECUTION_READY=NOT_CLAIMED`。

## 14｜FINAL-HANDOFF-RECONCILE（M1／M2／M3）

### M1｜Evidence bytes 與 HANDOFF pin

- 根因：147 個文字證據在加入 Git 時被 clean filter CRLF→LF；working bytes 仍與原 Manifest 相符，但 blob／GitHub raw 不符。
- 處置：以 `hash-object -w --no-filters`＋`update-index --cacheinfo` 還原原 CRLF blob（oracle 1 檔＋其餘 146 檔），不改內容、不改歷史 PASS。
- 統計：673 索引；526 blob 原本相符；**147 需 CRLF 還原**；0 無法解析。
- 驗證：fresh clone 673/673 SHA 相符；oracle 回復原 pin `112f2902…`；`git ls-files --eol` 顯示 `i/crlf w/crlf attr/-text`。
- HANDOFF／Consumer：凍結 HANDOFF，從遠端 clone 以 bundle 重建 candidate 後執行 final Consumer（見 §15）。

### M2｜Reviewer ON／OFF 正向

- 根因：ON／OFF 共用同一 outroot 且未建立，Reviewer 兩邊 `OUTPUT_ROOT_NOT_FOUND` exit 2，parity 只比 exit／SHA 而誤判 PASS。
- 修補：ON／OFF 各自獨立 output root；expected semantics 為 exit 0、`REVIEW_SOURCE_LOCATED_ONLY`、`defects=0`；比較 state／defects／authority_state。
- 結果：ON／OFF 皆 exit 0、state 相同、0 blocked attempts。
- 負例：兩邊同時使用不存在 outroot → 兩邊失敗；新判定 `false_parity_rejected=true`，不給 parity PASS。

### M3｜協作查缺與最終 Consumer

- NF-T08 新增必要材料消費：Guide 實際載入四契約 pins（`contract_context`）；Native 實際解析 Bridge `context_utf8` 的 9 個 case／locator／clause hash 並跑 POS/NEG（`native_context.json`）。
- 協作鏈：**8 segments／22 checks**；負例由 7 增至 **9**（另含 contracts_not_consumed、context_not_consumed），全部拒絕。
- Final Consumer：改為 `--root`＋bundle 重建 candidate，可在乾淨 clone 消費；不得回讀原 workspace。clean-receive 結果見 §15。

## 15｜Clean-receive 最終 Consumer（實際結果）

| 項 | 值 |
|---|---|
| 接收位置 | fresh `git clone https://github.com/shw097-team/FHS-5` at `234e2b1`（content commit；results-only 後續 commit 只追加 07） |
| Candidate | 由 `02_CANDIDATE/repo.bundle` 重建，checkout `bb66a27`；未讀原 workspace repo |
| Evidence | `50c158e3…`（694 檔索引；clone 內 694/694 SHA 相符） |
| HANDOFF | 凍結 bytes；receipt `handoff_sha256` 與 clone 內 HANDOFF 完全相符 |
| Consumer | exit 0；`consumed=true`；**803 checks**；POS `COMPLETE`、NEG `MISSING ["B"]` |
| 負例 | 10/10 fail-closed、`cli_executed=false`（wrong pack/candidate/oracle/evidence、mutated raw、missing、schema、duplicate、cross-subject、path escape） |
| Consumer Manifest | `e490b88efeea4489893dabd1bf33f61c926e61a82d34aeb1414ad9f6fe55d360` |
| Receipt | `07_CONSUMER/clean_receive/receipt.json`，SHA `37d567e8…`；run `clean-234-20261125154058` |

**W1 technical** 由 Consumer Manifest 推導：`receipt_consumed=true`、`handoff_bytes_match=true`、
`evidence_bytes_match=true`、`negatives_rejected=true`、`evidence_B0/W0=true`。


