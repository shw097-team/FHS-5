# 04_W0_START_THIN_PROMPT｜CODEX Native 自主施工入口

**project**：`FHS-5_PLP`｜**subject**：`FHS-5_PLP/W0`｜**batch**：`FHS-5/W0/B0-NF`  
**pack**：`W0-NF-r3-CODEX-PRIMARY`｜**manifest**：`./05_W0_SOURCE_MANIFEST.json`  
**goal**：以本地 CODEX 為主工程 Host，自主完成 B0-NF 的五方代表能力、真 DEV/OPS、獨立反證、修補、OFF 與 consumer readback，再推進 W0–W4。

## 0｜先讀與就緒判定

1. 讀 `05_W0_SOURCE_MANIFEST.json`，核 `project_id`、`wave_id`、`batch_id`、`pack_files` 的 path/SHA/bytes。
2. 讀 `00_W0_PI_PD.md` §00–§11、`01_W0_DEV_ECP.md`、`02_W0_OPS_ECP.md`、`03_W0_TQAEP.md`。
3. 檢查 5 個 pack digest 與實際 bytes；manifest 自身 hash 只看外部 seal，不在 JSON 內循環。
4. 檢查 CODEX/Python/Git、真 repo/root/HEAD/branch/dirty、sandbox、SP/Skill、實際可用工具與必要權限；未知記 `UNBOUND`，不猜。
5. 若任一 pack digest/identity/UTF-8/JSON/link 不符：`PACKAGE_INTEGRITY_HOLD`，停止受影執行。

**第一個合法動作（只讀）**：

```powershell
$Pack = (Resolve-Path '.').Path   # 本 prompt 所在 pack root
$m = Get-Content -LiteralPath (Join-Path $Pack '05_W0_SOURCE_MANIFEST.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$m.pack_files | ForEach-Object {
  $p = Join-Path $Pack $_.path
  $h = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower()
  $b = (Get-Item -LiteralPath $p).Length
  [pscustomobject]@{ path=$_.path; hash_ok=($h -eq $_.sha256); bytes_ok=($b -eq $_.bytes) }
}
Get-Command codex,python,git -ErrorAction SilentlyContinue
codex --version
python --version
git --version
```

任何 `hash_ok/bytes_ok=false` 即停。HERMES 不存在、不可寫或未 Served 只記 `HOST_SERVING_UNVERIFIED` Compatibility 觀測，不阻斷 CODEX 主工程。

## 1｜授權與主工程邊界

- `W0-CODEX-FIRST-20261125-01`：CODEX 為 B0/W0–W4 主工程執行者；HERMES 移至後續 Compatibility。
- `W0-OPS-NATIVE-20261125-01`：本地 CODEX Native OPS ECP 已採納；不再以舊框架 Original OPS ECP typed ref 作 Generic 前置。
- 同一有效授權內可自主接續多個受界可逆 DEV/OPS 與迭代；每個工作項仍須真 write-set、preimage、權限與 recovery。
- Maker／Reviewer／Checker／Consumer 是責任分工，不是多位 Human Owner；用獨立 worktree/session/process 做角色分離，不自簽、不偽造不同 principal。
- 真外部權限、越界、不可逆重大風險、公開發布或外部政策才集中回 Owner 一次；其他合法工作續行。

## 2｜Sample 自主選定（已預授權）

1. 先查 G4／等價非 SST 案例的真需求、程式、權利、tests、Oracle、隔離性、可逆性。
2. 若符合 B0 FUO，直接選定、復用並補足差額。
3. 若不存在、不可合法使用、不適合或成本高於最小新建，直接用 briefcheck。
4. 選定後記錄實際證據與理由，凍結 requirements/fixtures/Oracle，立即施工。
5. 不得用 G4 舊報告、briefcheck 示例輸出或裸 CODEX 普通工作冒充五方產品驗收。

本輪已選 **briefcheck**（G4 無本地實體/權利/需求；W0 CLOSEOUT 只有 3 tests 報告）。

## 3｜執行順序（CODEX Native）

```text
read manifest + pack + probe
→ freeze source/requirements/child/NEG
→ PI/PD/DEV/OPS/TQAEP present
→ Guide ThinStart
→ optional Bridge context
→ bounded DEV (briefcheck) with write-set/preimage
→ local OPS run/output/readback/restore
→ freeze candidate + oracle + fixture
→ independent Challenge POS/NEG
→ FAR finding + >=2 alternatives
→ Guide resume or direct fix
→ patch as 12' revision
→ affected retest + consumer readback
→ W0 CLOSEOUT/HANDOFF/UPSTREAM_CHANGESET
```

狀態以 `00` §09.2 的 `B0_EXECUTION_READINESS` 為準。若某節點是 `UNBOUND`，跳到下一個不依賴它的 `READY` 節點；不要全包停死。

## 4｜執行規則

### 4.1 READ/DRAFT

- 只讀 manifest 指定 source 與授權 root；檢查 SHA/span/version。
- DRAFT 只寫隔離 output；不得寫 source 或 repo。
- README、舊報告、舊 manifest 或作者摘要不代替真 bytes。

### 4.2 DEV

- 依 `01_W0_DEV_ECP.md`；先 freeze repo/root/HEAD/dirty/write-set/preimage。
- 只動 planned write-set；不得全 repo glob。
- 正常執行不得改 source；output 另寫。
- `12'` patch 是新 candidate/revision；新 ECP/preimage/readback；不得把 `12` 的 post-readback 作前置。

### 4.3 OPS

- 依 `02_W0_OPS_ECP.md` 的本地 CODEX Native OPS ECP；O1–O6 在真 principal/scope/preimage/output root/recovery 成立時執行。
- 不跑外部部署、遠端寫入、Publisher 或不可逆 effect。
- `git revert` 不是 OPS recovery；UNKNOWN 先 reconcile，不盲重試。
- HERMES 不可服務只記 Compatibility；不阻斷 CODEX OPS。

### 4.4 TEST/VERIFY

- 先凍結 expected/fixture/oracle；Runner 記錄 argv/cwd/env/timeout/exit/raw SHA。
- Checker 與 Maker 分 worktree/session/process；Consumer 是 distinct receipt。
- exit 0 但語義/狀態錯→`EFFECT_NOT_VERIFIED`。
- `UNAVAILABLE`≠ZERO；`UNREPRODUCED`≠PASS；舊 raw 不可重用於新 candidate。
- path 負例必須真建 absolute/`..`/UNC/symlink/junction 與 outside canary。

### 4.5 OFF/PARITY

- 在隔離 profile 不載入舊 HGK/FABRIC/SBL/FHS/PIPD；記 load/import/call trace。
- Bridge/FAR OFF 時，合法 direct path 仍可走。
- B0 五方產品測試不能被 direct bypass 抵銷；Bridge ON/FAR ON 需另案。

## 5｜Checkpoint／中斷續行

每次完成一個節點，寫一份最小 checkpoint（放隔離 `work/B0-NF/checkpoints/`）：

```text
checkpoint_id, pack_sha256, candidate_sha256, last_good_ref,
completed_tasks[], current_task, next_legal_action,
unknown_effects[], open_holds[], owner_decisions_pending[],
evidence_refs[], timestamp
```

中斷後先 reconcile：核 pack/candidate digest、last good、未結 task、下一合法操作、未知 effect；不得猜測已成功或重放未知寫入。若 checkpoint 與實際不符，以實際 file/process/consumer readback 為準，記 `RECONCILE_MISMATCH`。

## 6｜Stop／Resume

| 觸發 | 動作 |
|---|---|
| pack hash/identity 不符 | `PACKAGE_INTEGRITY_HOLD`；不執行 |
| 無真 repo/ACL | `AUTHORITY_REQUEST`；停受影 DEV |
| 無 sample | `SAMPLE_SELECTION_REQUIRED`（本輪已選 briefcheck） |
| 假 permit/WorkOrder | `FALSE_AUTHORITY`；no-op |
| path escape/secret | 停、redact、記 incident |
| 真 red | 先 freeze、定位 ChangeCone；修補後只回歸受影 |
| 無新 delta | 停同質重派；記 HOLD/Next |
| 不可逆/越界/發布 | 回 Owner；不自行擴權 |
| HERMES 不可服務 | 記 Compatibility；CODEX 續行 |

## 7｜Done 與交接

### B0 Done

- 五方 individual＋combined 真 invoke。
- 合法 DEV/OPS＋pre/post/readback/restore。
- Challenge 真 POS/NEG、FAR ≥2 方案、red→patch→retest。
- OFF parity、安全、Checker distinct、consumer readback。

### 本輪只可宣

`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（pack 文件層）；B0 verdict 由實際 EVIDENCE 判定。不得宣 `NATIVE_PASS`/`INDEPENDENT_PASS`/`W1_*`/`RELEASED`，除非有同 Scope 真證據。

### 交接

真跑後生成 `EVIDENCE/`、`B0_CLOSEOUT.md`、`B0_HANDOFF.md`；W0 完整後才 `W0_CLOSEOUT`/`W0_HANDOFF`/`W0_UPSTREAM_CHANGESET`。每份 handoff 必含 pack/candidate/source/evidence SHA、argv/exit/raw、consumer readback、next/owner/stop/resume、NotCovered；欄位見 `00` §10.2。

## 8｜本 prompt 的邊界

本檔只供 CODEX Native 讀取，不重抄 MASTER，不發明 `/goal`、工具、模型、route 或產品 actual。HERMES 相容性測試另立工作包；不得以 CODEX 本地結果冒充 HERMES/GPT CHAT/GPT WORK 已通過。
