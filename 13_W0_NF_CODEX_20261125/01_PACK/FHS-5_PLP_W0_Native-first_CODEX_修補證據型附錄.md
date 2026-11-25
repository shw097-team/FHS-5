# FHS-5_PLP/W0 Native-first｜CODEX 修補證據型附錄

**subject**：`FHS-5_PLP/W0`｜**batch**：`FHS-5/W0/B0-NF`  
**pack**：`W0-NF-r3-CODEX-PRIMARY`｜**artifact**：`FHS5-PLP/W0/PACK-NF-20261125-03`  
**date**：2026-11-25（Asia/Taipei）  
**status**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`  
**product**：`B0/W0 NOT_RUN`｜**not_claimed**：`B0_NF_VALIDATED / W0_NF_VALIDATED / NATIVE_PASS / INDEPENDENT_PASS / W1_TECHNICALLY_READY / W1_EXECUTION_READY / RELEASED / EXTERNAL_OS_REPO_HOST_GRANT`

> 本附件是本輪 CODEX 修補的稽核與交接 evidence，不是第二套規範、不是第七主檔、不是產品 EVIDENCE／CLOSEOUT／HANDOFF actual。主包 root 恰六檔；本附件在主包 root 之外。

## E0｜Output／Identity

| 項目 | 值 |
|---|---|
| output root | `C:\Users\user\Documents\Codex\2026-11-25\new-chat-5\outputs\FHS-5_PLP_W0_Native-first_CODEX_主用修補_交付` |
| pack root | `...\FHS-5_PLP_W0_NATIVE_FIRST`（恰六個規範檔） |
| baseline | `W0-NF-r1`；LastGood 在 `C:\Users\user\Documents\Codex\2026-11-25\new-chat-5\work\lastgood_W0-NF-r1\`；未覆寫 |
| source W0M | `NF-r3-PRIMARY`；106,859 B／1,176 lines；`a1f186cc337a4b3828e53f77533df5c97fdda63e132521d861a79b884f0c3aef` |
| W0M appendix | 30,283 B／374 lines；`6dee9837c50eecd09aa5db4ab8ce95766feb84e91709150cd4a8502c5d2a6b7d` |
| PLAN | `NF-PLAN-r1`；69,997 B／509 lines；`9efa36535762edcbc005f56ecc4687f009e9692c1ca2116919f48a58365d7b85` |
| WORK control | `WORK-W0-PACK-NF-r1`；24,544 B／111 lines；`982d77f997f5239686e79f8426c55ab2dcf98233caf6391932af46c74962d841` |
| checker script（本輪，非產品） | `C:\Users\user\Documents\Codex\2026-11-25\new-chat-5\work\pkg_check.py` |
| checker report | `C:\Users\user\Documents\Codex\2026-11-25\new-chat-5\work\pkg_report.json` |

### E0.1 最終 pack 檔案（外部 seal）

| 檔案 | bytes | SHA-256 |
|---|---:|---|
| `00_W0_PI_PD.md` | 31,783 | `40abf88cc97691fcb4effdc84a8bf874b50c984645b224a1f37dd4e670222e11` |
| `01_W0_DEV_ECP.md` | 11,556 | `76242a989c974186afd0694c6ad68b429de4227518351b352765de5901a5eee6` |
| `02_W0_OPS_ECP.md` | 11,075 | `e3b203cdf1514b84b23ba35a6170786f42e0fd3f3beab16c72cc75ccd093b747` |
| `03_W0_TQAEP.md` | 13,805 | `d1c47e06ee084ca70b39c6036104481b4f34e0cd3b33f1d35fdde8c37c9dbafb` |
| `04_W0_START_THIN_PROMPT.md` | 7,780 | `61535d7af0f8167bc152a088bda3ff6173014b3261711e8f75f0a22e1ca83554` |
| `05_W0_SOURCE_MANIFEST.json` | 18,821 | `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8` |

`05` 的 `pack_files` 只列五 MD，`manifest_self_hash=EXTERNAL_RECORD_ONLY`；本節與同目錄 `EXTERNAL_SEAL.json` 是外部 seal，不自含於 JSON。附件本身不納入 pack digest，避免循環。

## E1｜Source ledger 與讀取層級

完整 32 源在 `05_W0_SOURCE_MANIFEST.json.sources`；本節只列受影與本次實讀。

| ID | 來源 | 版本／bytes／lines | raw SHA-256 | 本輪層級 |
|---|---|---|---:|---|
| S01 | `FHS-5_Native-first_重構\W0M_Native-first_主用可執行_交付\FHS-5_PLP_W0M_完整實質正文.md` | NF-r3-PRIMARY／106,859／1,176 | `a1f186cc…` | `READ_FULL` |
| S02 | 同目錄 `FHS-5_PLP_W0M_證據附件.md` | NF-r3-PRIMARY／30,283／374 | `6dee9837…` | `SELECTED_READ_E0_E4` |
| S03 | `FHS-5_PLP_W0_MASTER_Native-first重構方案.md` | NF-PLAN-r1／69,997／509 | `9efa3653…` | `READ_FULL` |
| S04 | `FHS-5_PLP_W0_Native-first_GPT_WORK_最小執行控制包.md` | WORK-W0-PACK-NF-r1／24,544／111 | `982d77f9…` | `READ_FULL` |
| S14 | `FHS-5_PLP_W2M_完整實質正文.md` | W2M／50,052／766 | `7b42af25…` | `SELECTED_READ §03.1` |
| S15 | `FHS-5_PLP_W4M_完整實質正文.md` | W4M／57,789／819 | `3276aa0e…` | `SELECTED_READ §06.3/§10.2` |
| S16 | `FHS5_W0_CLOSEOUT_PRIMARY_HANDOFF_20261124.md` | W0-PRIMARY／2,840／41 | `994264b1…` | `READ_FULL` |
| S21 | 舊 `02_ORIGINAL_CONTRACT_REFS.json` | W0-EXEC-SEL-20261124-01／1,571／40 | `81d40902…` | `READ_FULL` |
| S23 | 舊 `04_OPS_ECP.md` | W0-EXEC-SEL-20261124-01／4,998／74 | `92131ad4…` | `READ_FULL` |

**修正**：baseline `05` 把 S01/S02 寫成 `C:\Users\user\Downloads\FHS-5\W0M_...`，實際不存在；真路徑在 `FHS-5_Native-first_重構\W0M_Native-first_主用可執行_交付\`。本版已改正並重算 32/32。

### E1.2 舊 15 檔 → 六檔 crosswalk（沿用並重核身份）

| 舊檔 | 新落點 | 保留語義 |
|---|---|---|
| `00_WAVE_RUN_MANIFEST.md` | 00＋05 | Wave/Subject/Scope/Source |
| `00_WAVE_RUN_MANIFEST.json` | 00/05 必要投影 | 機器投影 |
| `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | 00 | Source/Scope/Construction |
| `02_ORIGINAL_CONTRACT_REFS.json` | 00 §07、02 §03 | 原 ref／適用性；`ops_ecp_ref=null` |
| `03_DEV_ECP.md` | 01 | DEV ECP |
| `04_OPS_ECP.md` | 02 | OPS ECP；作者設計骨架，非原域 ref |
| `05_PLANNED_TQAEP.md` | 03 | Case/Oracle/ExpectedRaw |
| `05_PLANNED_TQAEP.json` | 03 必要投影 | `projection_of_sha256` |
| `06_PERMISSION_STOP_RESUME.md` | 00/01/02 | Permission/Stop/Resume |
| `07_EVIDENCE_AND_CHECKER.md` | 03 | Evidence/Checker |
| `08_AS_BUILT_AND_HANDOFF.md` | 執行後 CLOSEOUT/HANDOFF | 施工前只定驗收契約 |
| `09_README_RUN_ORDER.md` | 00/04 | Run order |
| `W0_START_THIN_PROMPT.md` | 04 | ThinStart |
| `SOURCE_MANIFEST.json` | 05 | 真 SHA/bytes/lines |
| `PACKAGE_FILE_MANIFEST.json` | 05/seal | 外部 file digest |

舊 15 檔不雙寫 canonical；本輪只讀受影條文，未把未讀全冊當已讀。

## E2｜Findings／實際修補／重驗

| ID | Source:section | Target | Observed／反例 | Severity | Root cause | Repair | Recheck |
|---|---|---|---|---|---|---|---|
| F-01 | baseline `05` sources S01/S02 | 05 | 兩個 W0M source path 不存在；真檔在 `FHS-5_Native-first_重構\...` | BLOCKER | 路徑少一層 | 改正 path；重算 32/32 | `PKG-01.7` PASS |
| F-02 | W0M §10.5/§10.5A；控制包 §04 | 00 §07.3 | baseline 只說「W1 14 HOLD＋R3-CR requalify」，沒有逐項 ID/狀態；10.5A 未落點 | MAJOR | 以繼承引用代替實質 ledger | 加 14 HOLD 表＋R3-CR01..12＋WM2E 表，全 `OPEN_PRESERVED` | `PKG-02.7/02.8` PASS |
| F-03 | W0M §05.5／W2M §03.1 | 00 §07 | 13+3 只有狀態/取得，缺 producer/Owner/next/resume/受影 effect | MAJOR | 表欄不足 | 擴成 6 欄；原域狀態與 Generic 替代分開 | `PKG-02` PASS |
| F-04 | W0M §05.5 #5／§08.5 | 02 §03 | baseline 未記錄對舊 OPS ECP／refs 的實查；只說 UNBOUND | MAJOR | 未做真 ref 調查 | 實查舊 `04_OPS_ECP`（`AUTHOR_DESIGN_ONLY`）、`02_ORIGINAL_CONTRACT_REFS`（`ops_ecp_ref=null`）、W2M #5；保留 `NOT_ADMITTED`；提一次最小裁決文字 | `PKG-03.3` PASS |
| F-05 | 控制包 §06／DONE | 00 §09.2 | 無逐效果 `B0_EXECUTION_READINESS` 與第一個合法動作 | MAJOR | readiness 只在舊附件 E6 | 加 11 列效果表＋第一個只讀動作 | `PKG-04/05` PASS |
| F-06 | 控制包 §06／W0M §12.2–12.5 | 00 §10.2–10.3 | 只有 Handoff/W1 not_claimed，無 CLOSEOUT/CHANGESET 欄與回寫順序 | MAJOR | 交接契約缺 | 加三工件最小欄＋6 步回寫順序 | 語義 PASS |
| F-07 | W0M §08.3 | 01 §03；03 §03 | baseline 另建 `case_hash_mismatch.md`（與 W0M「不另造來源」衝突）；path 負例只寫檔名 | MAJOR | fixture 設計漂移 | 移除 hash fixture，改 `case_ok`＋錯 SHA；加 junction/symlink/outside canary 真生成與 argv | `PKG-04.3/04.4` PASS |
| F-08 | 控制包 §04 PKG-02/03 | 03 §01/02 | 24 案表缺逐案 FirstFail/NotCovered | MAJOR | 表欄不足 | 24 列加 FirstFail/NotCovered；NF-T 同 | `PKG-02.4/02.5` PASS |
| F-09 | 03 §03.2 | 03 | baseline 子項全標 R1，與 SAMPLE-R1..R4 不一致 | MINOR | 標籤錯 | 改 R1/R2/R3/R4 對齊 | 語義 PASS |
| F-10 | 控制包 §03.3 | 04 | 缺 bootstrap 命令與 checkpoint/UNKNOWN 續行欄 | MAJOR | 薄提示只到流程 | 加第一個只讀 PowerShell、checkpoint schema、reconcile 規則 | `PKG-04.5` PASS |
| F-11 | W0M §03.2；控制包 §00 | 00 §08 | capability ledger 太薄；Hermes/W1/G4 實際狀態未落 | MAJOR | 只留目標表 | 加 2026-11-25 真 probe（OS/PS/Python/Git/Hermes/Codex/Node）＋disposition | 實測 PASS |
| F-12 | 控制包 §06 升格方法 | 00 §01.3；05 lineage | 無本次主用選定記錄／baseline 血緣 | MAJOR | 只繼承 W0M 授權 | 加 `W0-PACK-NF-PRIMARY-20261125-02`、baseline 六檔 hash、附件 hash | `PKG-05.4` PASS |

### E2.1 FirstFail → ChangeCone → 重驗（實際 loop）

| 次序 | FirstFail | ChangeCone | 修補 | 重驗 |
|---:|---|---|---|---|
| 1 | `PKG-03.1`：00 缺 `GATE_CYCLE_CANDIDATE`/`PHASE_OVERREACH_CANDIDATE` 的 DAG 反例 | 00 §04 | 新增 §04.3 六條反例 | 重跑 checker：PASS |
| 2 | `PKG-03.2`：01 缺 `NOT_ADMITTED`（有 FALSE_AUTHORITY/no-op/git revert） | 01 §00/§09 | 加「無真權限→NOT_ADMITTED」與假 permit→FALSE_AUTHORITY | 重跑 checker：PASS |
| 3 | 00 baseline 路徑用相對 `work/...`，交付後易誤讀 | 00 header、05 lineage | 改 absolute LastGood path | 重跑 checker＋manifest：PASS |

同一 Finding 各修一次；無重複無差額修補。未達兩次上限。

## E3｜PKG-01..05 實際檢測

**方法**：`python work\pkg_check.py <pack>`；報告 `work\pkg_report.json`。實際結果：**33/33 checks PASS；7/7 破壞性反例 caught；verdict=PASS**。

| 組 | 檢查數 | 實際結果 |
|---|---:|---|
| PKG-01 結構／完整性 | 9 | 6/6 檔、嚴格 UTF-8 無 BOM、JSON parse、5/5 pack hash/bytes/lines、32/32 source、無 self-cycle、所有相對 link 可解析 |
| PKG-02 保留／追溯 | 9 | NF01–10、NF-R01–10、14 WP、24 原 Case、10 NF-T、7 Seam、14 HOLD、12+1 CR、具名產品分母全部落點 |
| PKG-03 Native-first／阻斷 | 5 | direct/Reader/Registry/Runner/ACK、Bridge/FAR OFF、post-evidence、W4 倒卡、假 permit、未知 effect、`12/12'`、OPS #5 gate 均有拒絕語義 |
| PKG-04 可施工／否證 | 5 | D1–D7、O1–O6、fixtures/exit/status、path 真測設計、bootstrap/checkpoint 均存在 |
| PKG-05 交付／claim | 5 | 01/02 無 actual-positive；03 `PLANNED_NOT_EXECUTED`；主用 provenance；外部 seal |

### E3.1 破壞性／隔離反例（copy 上執行，不改正本）

| # | 注入 | 預期 | 實際 |
|---:|---|---|---|
| NEG-01 | 改 00 一個 byte | pack hash mismatch | caught |
| NEG-02 | 刪 03 | missing file | caught |
| NEG-03 | 改 manifest source path 為不存在 | source missing | caught |
| NEG-04 | 加 `[x](missing.md)` | broken link | caught |
| NEG-05 | 把 05 加進 `pack_files` | self-hash cycle | caught |
| NEG-06 | 在 01 注入 `DEV_EXECUTED=YES` | planned-only 違規 | caught |
| NEG-07 | 把 02 的 `NOT_ADMITTED` 全改 `ADMITTED` | OPS gate 移除 | caught |

**限制**：這是文件級 mutation，不是 B0 產品破壞性測試；不宣產品 Native/Independent PASS。

### E3.2 從 04 單一入口的桌面 E2E 走查

| # | 步驟 | 輸入 | 預期 | 實際 | Verdict |
|---:|---|---|---|---|---|
| 1 | 讀 05／核 seal | pack root | 5/5 hash/bytes、JSON parse | checker 5/5 | PASS |
| 2 | Source READ | W0M 真 bytes | SHA 與 manifest 一致 | 32/32 | PASS |
| 3 | Guide ThinStart | 04 §0 | 單一 manifest 入口、無擴 scope | 存在 | PASS（planned） |
| 4 | D1 repo probe | Owner `$Repo` | root/HEAD/dirty 或 `UNBOUND` | `UNBOUND`（未指定） | 誠實阻斷 |
| 5 | D2 sample | G4/briefcheck | Owner 選定或 `SAMPLE_SELECTION_REQUIRED` | 未選 | 誠實阻斷 |
| 6 | D3 write-set | briefcheck | 11 path、preimage absent、diff scope | 有 | PASS（planned） |
| 7 | D4 CLI | briefcheck | argv/exit/schema/timeout | 有 | PASS（planned） |
| 8 | D5 tests | 10 cases | POS/NEG/EDGE/SEC＋path 真測 | 有 | PASS（planned） |
| 9 | D6 recovery | preimage/新增檔 | 反向 patch／只刪本次 | 有 | PASS（planned） |
| 10 | D7 `12'` | 新 revision | 新 ECP/preimage/readback，無 cycle | 有 | PASS（planned） |
| 11 | O1 Host | Hermes | session/task ref | binary 存在、install 不可寫 | `NOT_ADMITTED` |
| 12 | O2–O4 | OPS #5 | gate 或真執行 | gate 保留 | `NOT_ADMITTED` |
| 13 | O5–O6 | OFF/consumer | trace/readback 或 planned | planned | PASS（planned） |
| 14 | Challenge/FAR | frozen candidate | POS/NEG＋≥2 方案 | 無真 raw | `NOT_RUN` |
| 15 | Handoff | actual raw | consumer readback | 未跑 | 誠實阻斷 |

**結論**：沒有「無 producer 的無解硬 Gate」；pack 讀取／Source READ／Guide／文件與隔離 DRAFT 有合法下一步；OPS 與 sample 的阻斷有具名 Owner 與 resume。錯 exit／semantic／timeout／UNKNOWN／restart／optional tool／no-auth／next-task 的處置分別在 01 §06/§08、02 §09、03 §08、04 §5–6。

### E3.3 Hard-edge DAG 拓撲檢查

`python work\dag_check.py`；節點 15（01–14＋`12a`/`12b`），hard edge 22；**acyclic=true**。拓撲序一例：`01,02,03,04,05,06,07,12a,08,09,10,11,12b,13,14`。`12a`（初始 effect）與 `12b`（`12'` patch）是不同節點；`07 Bridge` 是 `OPTIONAL_INFO`，不入 hard edge 骨幹。`post-readback` 沒有回邊到同操作 admission。

## E4｜真 read-only probe（2026-11-25）

| 對象 | 實際觀測 | 判定 |
|---|---|---|
| OS | Microsoft Windows 10.0.26200 | `TOOL_PRESENT` |
| PowerShell | 7.6.9 | `TOOL_PRESENT` |
| Python | 3.11.9（`...\Python311\python.exe`） | `TOOL_PRESENT` |
| Git | 2.53.0.windows.1 | `TOOL_PRESENT` |
| Hermes | binary `...\hermes\bin\hermes.exe` 存在；`hermes --version` 回報 install state 不可寫（`.install.lock`） | `HOST_BINARY_PRESENT / HOST_SERVING_UNVERIFIED` |
| Codex CLI | `codex.ps1` 存在 | `TOOL_PRESENT` |
| Node | `node.exe` 存在 | `TOOL_PRESENT`（非必要） |
| product repo | 未指定 root；未 probe | `UNBOUND` |
| G4 | 只有 CLOSEOUT 的 3 tests 報告；無本地實體/需求/權利 | `REPORTED_RUNNABLE` |
| W1 reference | `W1/impl/w1_bridge_reference.py` 未找到 | `UNVERIFIED` |
| W1 checks | `replay_hashes.py` 等可見 | `REPLAY_CANDIDATE`；未跑 |
| Original OPS ECP | 舊 `04_OPS_ECP` 是 `AUTHOR_DESIGN_ONLY`；`ops_ecp_ref=null` | `UNBOUND` |

## E5｜剩餘缺口／Owner／Resume

| # | 缺口 | 受影 | Owner | ResumePredicate |
|---:|---|---|---|---|
| 1 | 真 product repo/root/HEAD/dirty | DEV、NativeRead | Repo Owner | live probe＋ACL |
| 2 | Hermes install owner/route/session | O1、OPS | Host Owner | 修復 install 或指定等效 route |
| 3 | Original OPS ECP #5 | O2–O4 | Host/OS Owner | 原 typed ref 或 02 §03.2 一次裁決 |
| 4 | G4／briefcheck 選定 | B0 sample | Project/Source Owner | 真需求/權利/tests |
| 5 | fixture/oracle/Checker | Challenge/TQAEP | Case/Checker | 凍結 bytes/expected |
| 6 | 真 DEV/OPS 權限 | 12/02 | Repo/Host Owner | exact root/write-set/期限 |
| 7 | W1 14 HOLD＋R3-CR | W1 | W1 Owner | W0 handoff＋requalify |
| 8 | MASTER/PROG/PROJ/WM 回寫 | 後波 | Program | 真 W0 Raw |

**一次合併 Owner 決策**：sample（G4/briefcheck）＋OPS ECP #5；在完成前，pack 讀取、Source READ、Guide ThinStart、文件/隔離 DRAFT 可續。

## E6｜B0 execution readiness（摘要）

| 效果 | 狀態 | 下一個動作 |
|---|---|---|
| Pack read／manifest | `READY` | HERMES 讀 05＋04 |
| Source READ | `READY_WITH_ROOT` | Owner 指定 root/ACL |
| Guide ThinStart | `READY_WITH_PACK` | 真 pack path |
| Bridge 四 API | `PLANNED` | 真 probe／隔離實作 |
| DEV（briefcheck） | `PLANNED` | D1 probe／Owner 指定隔離 repo |
| OPS | `NOT_ADMITTED` | OPS #5 決策＋Host ACL |
| Challenge | `PLANNED` | Checker 凍結 oracle |
| FAR | `PLANNED` | 真 Finding 後 |
| G4/briefcheck | `SAMPLE_SELECTION_REQUIRED` | Owner 一次選定 |
| W1/Release | `NOT_CLAIMED` | W0 actual／原發布程序 |

## E7｜主用授權、scope 與非聲稱

| 欄 | 值 |
|---|---|
| 授權來源 | 本輪使用者指令（執行 W0 Native-first 啟動薄 PROMPT）＋`W0M-NF-PRIMARY-20261125-01` |
| pack decision | `W0-PACK-NF-PRIMARY-20261125-02` |
| 主用版本 | `W0-NF-r2-PRIMARY` |
| scope | `FHS-5/W0/B0-NF` pack 讀取、Guide ThinStart、planned DEV/OPS、Challenge/FAR 設計與受界執行 |
| 限制 | 只寫新隔離交付區；不改來源/產品/Host/ACL/憑證；不發布 |
| 明示 | 本授權是 Owner 指令的記錄，不是 CODEX 簽章、不是 OS/Repo/Host/Publisher grant |

**非聲稱**：`B0_NF_VALIDATED`、`W0_NF_VALIDATED`、`NATIVE_PASS`、`INDEPENDENT_PASS`、`W1_TECHNICALLY_READY`、`W1_EXECUTION_READY`、`RELEASED`、`EXTERNAL_OS_REPO_HOST_GRANT` 均未成立；`B0/W0 product=NOT_RUN`。

## E8｜交付索引與第一個 HERMES 動作

| 檔 | 實際路徑 | bytes | SHA（前 8） |
|---|---|---:|---|
| 00 | `...\FHS-5_PLP_W0_NATIVE_FIRST\00_W0_PI_PD.md` | 30,915 | `e8f2e289` |
| 01 | `...\01_W0_DEV_ECP.md` | 11,208 | `48546d3a` |
| 02 | `...\02_W0_OPS_ECP.md` | 11,683 | `847f307d` |
| 03 | `...\03_W0_TQAEP.md` | 13,756 | `9ad1b507` |
| 04 | `...\04_W0_START_THIN_PROMPT.md` | 8,131 | `648c2ac7` |
| 05 | `...\05_W0_SOURCE_MANIFEST.json` | 17,570 | `37307960` |
| evidence | 本檔 | 見外部 seal | 見 `EXTERNAL_SEAL.json` |

**第一個 HERMES 合法動作**：只讀 `04` §0 的 PowerShell，重算 5 個 pack digest、解析 05、`Get-Command python,git,hermes`＋版本；若 `hermes --version` 仍回 install state 不可寫，記 `HOST_SERVING_UNVERIFIED`，不啟動 OPS。其後等待 Owner 一次合併決策（sample＋OPS ECP #5）。


## E9｜CODEX-first 正式裁決與樣本／OPS 落地

| 決策 | 落地 |
|---|---|
| `W0-CODEX-FIRST-20261125-01` | CODEX 為 B0/W0–W4 主工程 Host；HERMES 移至 Compatibility；多操作受界授權；樣本自主 |
| `W0-OPS-NATIVE-20261125-01` | 本地 CODEX Native OPS ECP 採納；W0M §00.6/§05.1/§05.5 #5/§08.1/§08.5 amended（`W0M_CODEX_FIRST/...r4.md`） |
| `B0-SAMPLE-CODEX-20261125-01` | G4 無本地實體/需求/權利/tests；選 briefcheck |

## E10｜B0-NF 實際執行結果（2026-11-25）

| 方／項 | 實作 | 結果 | 證據 |
|---|---|---|---|
| TPM＋Reviewer | 真實 `plp-tpm-review 1.0.1` `review_core.py` | `REVIEW_SOURCE_LOCATED_ONLY`；0 defects；5 unbound | `01_B0_NF/evidence/review/` |
| Guide | `guide_min.py`（BUILD_MINIMAL） | `PACKAGE_FIRST`；5/5 pack files；9-key delta | `01_B0_NF/evidence/guide/thin_start.json` |
| Bridge | `REUSE` `w1_bridge_reference.py` | selftest 22/22；inspect/explain/render/compare | `01_B0_NF/evidence/bridge/` |
| Challenge | `run_checker.py`（獨立 worktree） | PASS；19 checks；0 findings | `01_B0_NF/evidence/challenge/challenge.json` |
| FAR | `far_min.py` | 2 alternatives；10 advice；ALT-1 | `01_B0_NF/evidence/far/far.json` |
| DEV red | briefcheck v1 | 2 failures（R3/R7） | `01_B0_NF/evidence/tests/red_v1.txt` |
| Patch `12'` | seen[A]/seen[B] fail-closed | diff 可重播 | `01_B0_NF/evidence/tests/patch_12prime.diff` |
| DEV green | v2 | 10 tests OK（1 junction skip） | `01_B0_NF/evidence/tests/green_v2.txt` |
| OPS | O1–O6 | POS 0、NEG 2、output/readback/restore、OFF imports `NONE` | `01_B0_NF/evidence/ops/ops.json` |
| Consumer | 具名 consumer | `consumed=true`；checker PASS | `01_B0_NF/evidence/consumer/consumer_receipt.json` |

**B0 verdict**：`B0_REPRESENTATIVE_PASS_WITH_NOT_COVERED`；**W0 status**：`W0_PARTIAL_VALIDATED`（非 `W0_NF_VALIDATED`）。

**Pins**

```text
source    fc46088355071109d6dc4051da4db25d3246000515ea1f254be14d78121d294c
candidate 5eab43de2d3f67d6afbb1c5f6bc390e2c391da36
evidence  ef977e0855e7d3dc633aaa5d2b0a78976a3ee530667596f5b8f031dbf262c6d5
oracle    3cc26ed8e74a150e4c354fa9596d706e1e30552a217d940ba14c17c2f5bd12e1
case_set  93c7f91c6d78288d052ec701798c98dbf2717b3ceef6d486751e95105ca90f7c
```

**NotCovered**：HERMES／GPT CHAT／GPT WORK 實際 Host；完整 U26／CG-SEM17／QA26／C16／EC-36／local47／38＋28／FARP30；W1–W4 全波；Publisher/Release；junction 子例（Windows 權限）。


**文件結束**｜`W0-NF-r2-PRIMARY`｜CODEX 修補證據型附錄
