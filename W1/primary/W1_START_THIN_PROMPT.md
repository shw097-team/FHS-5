<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# W1｜Start Thin Prompt（作者候選）

這是 `FHS-5_PLP/W1/CONTROL_PACK` 的下一手薄入口，批次 `W1-PACK-01`。它是給後續 W1 Executor 的候選薄提示，不是本任務的 GPT WORK 啟動 prompt，也不新增任何權力。

## 0. 這是什麼

本檔只把真小包的身份、目標、FUO、Done、Scope、Effect、Owner、Next、Stop、Resume 壓成一頁。任何未列入的權限、WriteSet、Host 安裝或 Release 都不存在。

## 1. Package identity

- `project_id`：`FHS-5_PLP`
- `subject_id`：`FHS-5_PLP/W1/CONTROL_PACK`
- `scope`：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`
- `wave_id`：`W1`
- `batch_id`：`W1-PACK-01`
- `source_manifest_sha256`：`8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47`
- `package_file_manifest`：`PACKAGE_FILE_MANIFEST.json`（以檔內 SHA 解析；不在本文寫自身最終 digest）

## 2. Goal／FUO／Done

Goal：把 Guide ThinStart 與 Bridge 四 API 接成同 Scope 的可回取 Contract Context，並為三 Host 的七階段建立可驗證路線。

FuO：至少一個受權 Host 對同 Subject／Scope 產生真 `Consumed` Raw；未得前只交作者接口設計。

Done：15 檔可讀回；13 案有真 fixture／oracle；六 WP 有 dry-consume；H1–H8 本地通過或有具名 HOLD；索引／ZIP／seal 一致。

## 3. Scope／Effect

Scope 只含本包所列的 Guide／Bridge ABI、四 API、BodyResolver、三 Host 觀察與 W2–W4 接口。Effect 為 `SOURCE_READ + ISOLATED_DRAFT_WRITE + LOCAL_CHECK + LOCAL_PACKAGE`；DEV／OPS／USER／RELEASE 全部 `NOT_ADMITTED`。

## 4. Owner／Next／Stop／Resume

Owner：Wave Curator（作者）／Human Owner（選用與優先級）。Next：讀 `09_README_RUN_ORDER.md`，先跑 S0–S2，再按 S3–S6 取受影證據。Stop：來源不符、越出交付根、缺原 Issuer／Host／Checker 時，只停受影 claim。Resume：同 Subject／Scope／Host／Epoch 的 typed receipt。

## 5. 禁止

不得把本薄提示當 WorkOrder、Grant、Admission 或 Release；不得改 W0／上游／原 Repo／Host；不得以作者 fixture 冒原 Runner；不得以一個 Host 的結果核銷其他 Host；不得自簽 Independent。

Input: 本包 manifest／Case／ABI。
Operation: 依 Run Order 受影讀取與本地檢查。
Output: 受影 Raw 或 HOLD。
Consumer: W1 Executor。
NEG: 擴 Scope 或加 WriteSet → `SCOPE_DRIFT`。
FirstFail: `EXECUTION_ADMISSION_MISSING`。
