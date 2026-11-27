# 01_W0_DEV_ECP｜B0-NF Planned DEV Contract

**identity**：`FHS-5_PLP/W0`｜**batch**：`FHS-5/W0/B0-NF`｜**pack**：`W0-NF-r3-CODEX-PRIMARY`  
**source W0M**：`NF-r3-PRIMARY` `a1f186cc337a4b3828e53f77533df5c97fdda63e132521d861a79b884f0c3aef`  
**document state**：`PLANNED`｜**actual**：`NOT_RUN`｜**claim ceiling**：`AUTHOR_PLANNED_ECP`

> 本檔只承載 **planned** contract：exact target、argv、cwd/env/timeout、expected exit/stdout、write-set、preimage/absent、rollback。產品 actual command/exit/stdout/stderr/raw/postimage/recovery 只可進後續 `EVIDENCE/`、`CLOSEOUT`、`HANDOFF`。本檔不因主用升格而取得 OS/Repo 權限；`PLANNED` 不得直送 shell。

## 00｜入口與責任

| 欄 | 值 |
|---|---|
| decision ref | `W0M-NF-PRIMARY-20261125-01`＋`W0-CODEX-FIRST-20261125-01`＋`W0-OPS-NATIVE-20261125-01`；pack `W0-NF-r3-CODEX-PRIMARY` |
| Maker | 後續具權施工代理 |
| Checker | 獨立 session/worktree；不得與 Maker 自簽 |
| Consumer | Executor、Case Owner、Checker |
| Original OPS ECP | 不屬於本 DEV ECP；OPS 另見 `02_W0_OPS_ECP.md` |
| allowed effect | 同一有效授權內多個受界可逆 DEV；每個工作項仍須 exact write-set/preimage；不得批次修改 |
| 無真權限 | `NOT_ADMITTED`；本檔不構成 Grant |

## 01｜D1 Freeze baseline

### 01.1 Repo planning fields

| 欄 | 本輪值 | 取得方式 | Ready 條件 |
|---|---|---|---|
| `repo_root` | `UNBOUND` | Owner 指定後 `git rev-parse --show-toplevel` | absolute path 在授權 root |
| `head` | `UNBOUND` | `git rev-parse HEAD` | 40/64 hex；同次 probe |
| `branch` | `UNBOUND` | `branch --show-current` | real branch/detached |
| `dirty` | `UNBOUND` | `status --porcelain=v1 --untracked-files=all` | 保留他人變更 |
| `untracked` | `UNBOUND` | 同上 | 不清理 |
| `acl/principal` | `UNBOUND` | OS/Git 實際權限 | 只有文件許可→不施工 |
| `preimage` | `UNBOUND` | 逐檔 raw SHA | 缺→不施工 |
| `rollback` | `UNBOUND` | 反向 patch／刪本次新檔 | 不可回復→不納 B0 |

### 01.2 Probe（read-only；$Repo 待 Owner 給）

```powershell
git -C $Repo rev-parse --show-toplevel
git -C $Repo rev-parse HEAD
git -C $Repo branch --show-current
git -C $Repo status --porcelain=v1 --untracked-files=all
git -C $Repo ls-tree -r --name-only HEAD
Get-Command python,git -ErrorAction SilentlyContinue
python --version
git --version
```

**輸出要求**：保存 raw stdout/stderr、exit、cwd、command 與當期 UTC/Asia-Taipei 時間；不從檔名猜 HEAD。若 `$Repo` 不存在或無權，記 `REPO_UNBOUND`，只停 DEV。

## 02｜D2 Sample selection（已由 CODEX 依 Owner 規則選定）

| 選項 | 必要真條件 | 若未成立 |
|---|---|---|
| G4 | 真需求/程式/tests/權利；獨立於 SST；可逆 | 未取得本地實體/權利；**不採用** |
| briefcheck | 無 G4；真 read root；fixture/oracle 可凍結 | **已選定**（`B0-SAMPLE-CODEX-20261125-01`） |

選定理由：W0 CLOSEOUT 只有 G4 `3 tests` 報告，無本地路徑、需求、程式、License、測試或 Owner 指定；無法核真需求/權利/隔離性。依 Owner `W0-CODEX-FIRST-20261125-01` 的 Search-before-Build 規則，直接採 W0M/NF-PLAN 的 briefcheck。以下 path 是本輪實際建置目標。

## 03｜D3 Planned Write-set／Preimage

本輪已選 briefcheck，最小 write-set 如下；每個 path 在 D1 轉為 absolute 並確認 root：

| # | path（candidate） | type | preimage | planned change |
|---:|---|---|---|---|
| 1 | `samples/briefcheck/requirements.md` | new | `absent` | A/B 兩必要 Child 與格式 |
| 2 | `samples/briefcheck/briefcheck.py` | new | `absent` | root confinement、UTF-8、SHA、parse、JSON、exit |
| 3 | `samples/briefcheck/tests/__init__.py` | new（條件式） | `absent` | 若 `unittest discover` 需要 package |
| 4 | `samples/briefcheck/tests/test_briefcheck.py` | new | `absent` | POS/NEG/EDGE/SEC |
| 5 | `samples/briefcheck/fixtures/case_ok.md` | new | `absent` | `- [x] A`＋`- [x] B` |
| 6 | `samples/briefcheck/fixtures/case_missing.md` | new | `absent` | 只有 A |
| 7 | `samples/briefcheck/fixtures/case_dup.md` | new | `absent` | 重複 A |
| 8 | `samples/briefcheck/fixtures/case_bad_path.md` | new | `absent` | 路徑負例 descriptor（真正的 outside/symlink 由測試臨時建立） |
| 9 | `samples/briefcheck/fixtures/case_bad_utf8.md` | new | `absent` | invalid UTF-8 bytes |
| 10 | `samples/briefcheck/fixtures/case_ambiguous.md` | new | `absent` | 重複 B |
| 11 | `samples/briefcheck/fixtures/case_malformed.md` | new | `absent` | 缺 checkbox／非法行 |

**不建立** `case_hash_mismatch.md`：hash mismatch 由 `case_ok.md`＋錯 `--sha256` 在測試時產生，依 W0M §08.3 不另造來源。任何其他 path、既有檔覆寫、全 repo glob 都停止。

**Preimage 規則**：new=`absent`；modified=raw bytes/SHA；不含其他使用者 dirty/untracked。`tests/__init__.py` 只在 entrypoint 真需要時建立；不建立空殼。

**Planned diff scope**：只允許上表 11 條 path（其中 `tests/__init__.py` 條件式）。diff 超界即 `WRITE_SET_VIOLATION`。

## 04｜D4 Planned CLI contract

```text
python -m briefcheck --root <approved_read_root> --input <root-relative-path> --sha256 <expected-source-sha>
```

| 欄 | planned |
|---|---|
| cwd | sample repo root（D1 由 entrypoint 決定） |
| env | 只加必要 `PYTHONIOENCODING=utf-8`；不注入 secrets |
| timeout | 30 秒；實際值由 D5 觀測後凍結 |
| stdout | 穩定 UTF-8 JSON：`source_sha256, provided, missing, status` |
| stderr | 短錯誤碼；不含 root 外路徑或正文 |
| exit | `0=COMPLETE`；`2=MISSING`；`3=INVALID` |
| 副作用 | 正常跑不寫 source；R4 wrapper 另寫 output root |

**Expected JSON 形狀（所有 case 同 schema）**：

```json
{"source_sha256":"<hex-or-null>","provided":["A"],"missing":["B"],"status":"MISSING"}
```

`status` 只允許 `COMPLETE`、`MISSING`、`INVALID_DUP`、`INVALID_PATH`、`INVALID_ENCODING`、`SHA_MISMATCH`、`INVALID_FORMAT`。錯誤時 `provided/missing` 可為 `[]`，但不得輸出 root 外路徑或正文。

## 05｜D5 Tests／Readback

### 05.1 Baseline and unit

```text
python -m unittest discover -s tests -v
```

僅在 tests 目錄實際存在且屬本次 sample 時執行；baseline 失敗先記 red，不把環境問題當 code PASS。

### 05.2 Planned acceptance matrix

| ID | fixture／argv | expected exit/status | assertion／side effect |
|---|---|---|---|
| R1 | `case_ok.md`；`--input case_ok.md --sha256 <ok>` | 0/COMPLETE | `provided=["A","B"]`；source bytes 不變；stdout 可 parse |
| R2 | `case_missing.md` | 2/MISSING | `provided=["A"]`、`missing=["B"]`；parent 不 PASS |
| R3 | `case_dup.md` | 3/INVALID_DUP | 不因一個有效就 PASS |
| R4 | `case_bad_path.md`；另建 outside canary，argv `--input ../outside/canary.md`、absolute、UNC、symlink/junction | 3/INVALID_PATH | 不讀 root 外；stdout/stderr 不含 canary 內容或 root 外路徑 |
| R5 | `case_bad_utf8.md` | 3/INVALID_ENCODING | 不回顯原文；source bytes 不變 |
| R6 | `case_ok.md`＋錯 `--sha256` | 3/SHA_MISMATCH | 不先 COMPLETE 再降級 |
| R7 | `case_ambiguous.md` | 3/INVALID_FORMAT | fail closed |
| R8 | `case_malformed.md` | 3/INVALID_FORMAT | fail closed |
| R9 | `case_ok.md` 連跑兩次 | 0/COMPLETE | stdout byte/語義同值 |
| R10 | R1＋受權 output wrapper | 0/COMPLETE | source SHA 不變；output 可刪回 absent |

### 05.3 Path／symlink 的實際測試設計（不可只列 bad_path 檔名）

在 test fixture 的 **temp root**（`$TestRoot`）外建立 `$Outside`：

```powershell
$Outside = Join-Path $env:TEMP ("briefcheck_outside_" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $Outside | Out-Null
Set-Content -LiteralPath (Join-Path $Outside 'canary.md') -Value "OUTSIDE_CANARY_DO_NOT_READ" -Encoding utf8
$Root = Join-Path $env:TEMP ("briefcheck_root_" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $Root | Out-Null
# junction：一般使用者可建；symlink 需 Developer Mode/管理權，失敗則記 NOT_VERIFIED，不改預期
New-Item -ItemType Junction -Path (Join-Path $Root 'escape_dir') -Target $Outside | Out-Null
New-Item -ItemType SymbolicLink -Path (Join-Path $Root 'escape_link') -Target (Join-Path $Outside 'canary.md') -ErrorAction SilentlyContinue
```

argv 至少四種：`--input ../canary.md`、`--input <absolute path>`、`--input \\localhost\share\...`（UNC 不連線，只驗拒）、`--input escape_dir/canary.md`；symlink 建立成功時加 `escape_link`。Oracle：exit 3、status `INVALID_PATH`、stdout/stderr 不含 `OUTSIDE_CANARY_DO_NOT_READ`；source/outside bytes 不變。junction/symlink 建立被拒時記 `NOT_VERIFIED`，不得假 PASS。

### 05.4 Post-readback

1. 讀回 `git diff` 與 status；只允許 write-set。
2. 讀回 source raw SHA；必須同 preimage。
3. 讀回 output bytes/SHA、source bytes/SHA；正常跑不得寫 source。
4. Console exit 0 但 JSON/語義不符→`EFFECT_NOT_VERIFIED`。
5. Actual stdout/stderr/exit/raw 只寫 EVIDENCE；本檔不填。

## 06｜D6 Recovery／Rollback

| 情境 | 處置 |
|---|---|
| 既有檔修改失敗 | 用 preimage 反向 patch；核 SHA |
| 新檔錯誤 | 只刪本次 write-set 內新檔；不刪他人檔 |
| source 被動到 | 立即停、從 preimage/備份恢復、記 incident |
| output 寫入失敗 | 刪本次 output，source 不動；記 `RECOVERY_KIND_MISMATCH` 若 OPS |
| UNKNOWN | 先 readback/reconcile；不盲重試 |

`git revert` 只可在 DEV 且 ECP 明列時使用；不得作 OPS 回復。

## 07｜D7 `12'` Patch/Revision

| 欄 | 初始 `12` | 修補 `12'` |
|---|---|---|
| candidate | 初版 sample | 新 commit/tree/hash |
| ECP | 本檔 | 新 revision 的受影 ECP |
| preimage | 初版 | 受影檔新 preimage |
| admission | 原 effect | 新 revision 的 admission/既有授權範圍 |
| test | baseline POS/NEG | 只跑 affected POS/NEG/security/consumer |
| readback | 初版 | patch 後 postimage |

不得把 `12` 的 post-readback 當 `12'` 的前置；不得為 `12'` 每次重簽普通 WP。若 `12'` 超出一次可逆 DEV 或 scope，回 Owner 一次裁決，不自行擴權。

## 08｜Authority／Stop／Resume

| 缺件 | 停點 | Resume |
|---|---|---|
| repo/HEAD/ACL | 全 DEV | Owner 真 root＋ACL |
| write-set/preimage | 受影檔 | 逐檔 exact set＋preimage |
| Original OperationType | effect | 採納 ECP typed token |
| sample/owner | D3/D4 | 已選 briefcheck；不再請求 Owner |
| fixture/oracle | D5 | Checker 凍結 |
| 越界 | 立即停 | 還原受影變更＋新 write-set |
| 假 permit | 不施工 | 真權限/決策 |

**Idempotency key**：`task_id + operation_type + repo_head + write_set_sha + grant_ref`。同 key 只允許同 postimage 或 no-op；UNKNOWN 先 reconcile。

## 09｜NEG

- 以本檔當 Grant、以 `permit=true` 當權限。
- 假 permit／無真 grant → `FALSE_AUTHORITY`；越權操作必須 no-op，pre/post 不變。
- 把 actual 預填進 01。
- 使用全 repo glob 或改寫 write-set 外檔案。
- 用 `git revert` 冒充 OPS recovery。
- 以測試 harness 綠燈代替 source/JSON/readback。
- 把 `12'` 當同一 candidate。
- 以 `case_hash_mismatch.md` 另造來源（應以 `case_ok.md`＋錯 SHA）。
- 只寫 `case_bad_path.md` 檔名，未真測 absolute/`..`/UNC/symlink/junction/reparse。

## 10｜Not claimed

`DEV_EXECUTED=NO`、`EFFECT_VERIFIED=NO`、`B0_PASS=NO`。本檔的 `PLANNED` 不是產品 actual。
