<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜Run Order

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的合法執行順序，批次 `W1-PACK-01`。讀者不必重讀六冊藍圖，也不得跳過 Precondition 或把作者包當原域命令。

## 1. 入口與身份

先讀 `00_WAVE_RUN_MANIFEST.md` 與 `00_WAVE_RUN_MANIFEST.json`，確認六 identity 與 `claim_ceiling=AUTHOR_DESIGN_ONLY`。再讀 `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` 取得 16 源、原義務、六 WP、ABI 與四 API。需要機器 join 時讀 `SOURCE_MANIFEST.json`／`PACKAGE_FILE_MANIFEST.json`／`02_ORIGINAL_CONTRACT_REFS.json`／`05_PLANNED_TQAEP.json`。

Input: 本包根。
Operation: 按下列步驟讀、驗、停、續。
Output: 可重現的本地檢查結果或受影 HOLD。
Consumer: W1 Executor／Program。
NEG: 拿 W0 prompt 跑 W1 包 → `CONTRACT_SCOPE_MISMATCH`。
FirstFail: `IDENTITY_MISMATCH`。

## 2. DAG 與步驟

1. **S0 來源**：以 `SOURCE_MANIFEST.json` 重算每檔 SHA／bytes／lines；不一致即 `SOURCE_INTEGRITY_FAILED`，只停該源。
2. **S1 身份**：核 10 MD header、11 JSON／FileManifest／Case scope 的六鍵一致。
3. **S2 結構**：跑 `check/w1_guard.py` 與 `check/m22_guard_ref.py check-pack`；只接受 `AUTHOR_LOCAL_LINKS_ONLY`。
4. **S3 ABI**：讀 `01` §5–§7 與 `03`／`04`；以 `check/run_cases.py --pack-root FHS-5_PLP_W1_PRIMARY` 執行 fixtures 的 `request`／`predicate`；結果只 `AUTHOR_LOCAL_RULE_ONLY`，不代表原 ABI 已被 Consumer 接受。
5. **S4 Case**：讀 `05_PLANNED_TQAEP.md` 與 JSON；確認 13 案 oracle／fixture SHA，24 W0 disposition 未減。
6. **S5 Host**：按 `04` 的七階段逐 Host 取 Raw；缺 receipt 即 `HOST_PENDING`，不得代償。
7. **S6 交接**：讀 `08` 的 W2／W3／W4 欄級接口；未跑項目保持 NotCovered。

DAG：S0→S1→S2→S3；S3→S4；S3→S5；S4／S5→S6。不得 cycle；不得把 S5 的 Host Raw 當 S3 前件。

## 3. 可並行與不可並行

可並行：S3 的 Guide 與 Bridge crosswalk；S4 的 fixture 撰寫與 S5 的 Host 文件設計；不同 Host 的 observation 可並行但不得互相抵帳。

不可並行：未完成 S0 就宣 S2 PASS；未完成 S3 就宣 S5 `Invoked`；未完成 S5 就宣 `Consumed`；未完成 S4 就宣 Case 已驗。

## 4. Stop／Resume／Fail

Stop：來源缺失只停受影源；Host 缺 receipt 只停該 Host；原 Issuer／Checker／Publisher 缺只停 DEV／OPS／Independent／Release。其他章節繼續。

Resume：同 Subject／Scope／Host／Epoch 的 typed receipt；不得以本地檔或作者 CLI 補位。

Fail：同 first_fail 且無新差額不原樣重試；連續兩個有實質修補的回合仍同首錯，停該 slice 並列 owner／最小證據／resume。

## 5. 復原

本輪復原限於交付根：保留前一個真 LastGood、以同卷 staging→atomic rename、重算受影 SHA。原 Repo／Host 復原另走 `03_DEV_ECP.md`／`04_OPS_ECP.md` 的原 Owner 路徑；不得以 `git revert` 當 Host recovery。

## 6. 最小命令

在交付根執行：

```text
python check/w1_guard.py --pack-root FHS-5_PLP_W1_PRIMARY --delivery-root .
python check/m22_guard_ref.py check-pack --pack-root FHS-5_PLP_W1_PRIMARY
python check/replay_hashes.py --root FHS-5_PLP_W1_PRIMARY
python check/run_cases.py --pack-root FHS-5_PLP_W1_PRIMARY
```

四個命令都只讀；exit 0 僅代表本地連結一致，不代表原域接受。任何 `AUTHOR_GUARD_FAIL_CLOSED` 依 `first_fail` 修受影檔，不降 Oracle、不刪 Case。
