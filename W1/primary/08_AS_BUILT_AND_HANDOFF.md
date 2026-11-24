<!-- FHS5_IDENTITY: {"project_id":"FHS-5_PLP","subject_id":"FHS-5_PLP/W1/CONTROL_PACK","scope":"W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write","wave_id":"W1","batch_id":"W1-PACK-01","source_manifest_sha256":"8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47"} -->
# FHS-5_PLP W1｜As-Built 與交接

- Scope：`W1 Guide/Bridge ABI + 3-Host consumption + Contract Context author pack; SOURCE_READ+ISOLATED_DRAFT_WRITE+LOCAL_CHECK+LOCAL_PACKAGE; no repo/host/native/release write`

本檔是 `FHS-5_PLP/W1/CONTROL_PACK` 的 As-Built 與下一波交接，批次 `W1-PACK-01`。它把「本輪作者實際做到」與「W1 產品未來應做到」分帳，並給 W2／W3／W4 欄級接口。

## 1. 本輪作者實績

| 項目 | 實際 | 狀態 |
|---|---|---|
| 來源釘選 | 16 源逐檔 bytes／lines／SHA 重算 | `READ_VERIFIED` |
| W0 PRIMARY | 實體 36 檔（23 root＋13 sources）；`PRIMARY_MANIFEST.json` 34 entries；33/34 byte 一致；receipt 4,222／`6dbdd7bd…` vs 清冊 3,986／`18ad4b8d…` | `PASS_WITH_NAMED_FINDING` |
| 15 規範檔 | 10 MD＋5 JSON，逐檔 SHA 可重算 | `MATERIALIZED` |
| 13 作者 Case | 每案真 fixture／oracle，`AUTHOR_FIXTURE_NOT_LIVE` | `PLANNED` |
| H1–H8 | 本地 POS／NEG 實跑，raw 可回取 | `SELF_CHECK_ONLY` |
| 未做 | Native、Host 安裝、原 Runner、Independent、Release | `NOT_RUN`／`UNBOUND` |

Input: W1M wm-v5、W0 PRIMARY、B02／B03、CTRLW1。
Operation: 物化 15 檔、產 fixture／oracle、跑 harness、封存。
Output: 本包＋索引＋ZIP。
Consumer: W2 Program／W3／W4／Human Owner。
NEG: 未跑填 PASS → `AS_BUILT_OVERCLAIM`。
FirstFail: `PHASE_OVERREACH_CANDIDATE`。

## 2. 與未來 W1 產品效果分帳

本輪只到「作者可施工候選」。W1 產品 FUO 仍是：至少一個受權 Host 對同 Subject／Scope 的 Contract Context 產生真 `Consumed` Raw。該 Raw 未出現前，三 Host 只可寫 `HOST_PENDING`／`HOST_PARTIAL_LOCAL_ONLY`；不得以本包的 MD／JSON、Codex skill 可讀、G4 tests 或 W0 作者 pack 代替。

## 3. W0 LastGood 與 change cone

LastGood：`10_FINAL_DELIVERY/FHS-5_PLP_W0_REPAIRED_CANDIDATE`；PRIMARY：`10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY`。兩樹不混合成新 PRIMARY。W1 不改 W0；只讀其 15 normative＋13 sources 與 manifest／receipt 作為 inspect 輸入。

Change cone：Guide field 變 → 直接 Bridge consumer＋該 Case；Bridge API 欄變 → Context／Case／W2 refs；Host 狀態變 → 該 Host 的 claim 與 W4 Fit；Source SHA 變 → 受影 span 與 Case，不重跑全包。W0 receipt stale 只影響 source claim，不阻塞 ABI 設計。

## 4. W2／W3／W4 欄級接口

| Producer（W1） | Consumer（W2） | Transform／validation | Loss／unknown | NEG |
|---|---|---|---|---|
| `inspect_package.response.source_refs[]` | `02_ORIGINAL_CONTRACT_REFS.json.refs[]` | filter `kind=source`；重算 SHA／span | `unresolved_refs[]` 保留 | `SOURCE_IDENTITY_HOLD` |
| `inspect_package.response.effect_constraints[]` | `01_SOURCE_SCOPE...effect_constraints[]` | 只作 advisory；不產 token | 未知 effect 保留 | `EFFECT_UNBOUND` |
| `ContextBundle.context_sha256` | `03_DEV_ECP.pre.context_ref`／`04_OPS_ECP.pre.context_ref` | 直接複製＋重算 | Scope mismatch 停 | `CONTEXT_SCOPE_MISMATCH` |
| `HostCapabilityLedger.host_claims[]` | `02_ORIGINAL_CONTRACT_REFS.host_refs[]` | observation 類型原樣 | `NOT_OBSERVED` 不升 true | `W2_HOST_BIND` |
| `compare_context.changed[]` | `01_SOURCE_SCOPE...change_cone[]` | exact `(kind,path,sha)` | 不作語義推論 | `DELTA_UNVERIFIED` |

W3 收到：13 案結構、ExpectedRaw、作者 raw、`W1_ABI_BOUND`／`W0_PRIMARY_RECEIPT_STALE`。W3 不得把作者 fixture 當原 Runner。W4 收到：三 Host 九子義、Hermes 三格、Generic 適用性、Claim Ceiling；W4 不得把 W1 作者 PASS 當 Independent／Release。

## 5. FAR／Guide2 路由

Guide2 只保留 FAR 真九鍵 material pair 與十 Advice 的接口；本輪不跑 W3／FAR。無 verified pair 不自動 PARK／CLOSE；`CLOSE` 只是 closeout reminder，不是 Publisher 接受。`reconcile_guide_delta` 無原 verifier 一律 `DELTA_UNVERIFIED`。

## 6. Claim ceiling 與 NotCovered

Claim ceiling：`AUTHOR_DESIGN_ONLY`；交付狀態 `AUTHOR_REPAIRED_CONSTRUCTION_HANDOFF_CANDIDATE_WITH_NAMED_HOLDS`（作者施工交接候選；不是原域准入）。Not claimed：`PI_READY／PD_BOUND／EXECUTION_ADMITTED／NATIVE_PASS／INDEPENDENT_PASS／RELEASED／MISSION_COMPLETE`。

NotCovered：原 Host 實際消費、原 17／66／24 Case、原 Runner／Checker／Publisher、W0-A 指定、W0-B 准入、CH-07 舊 bytes 復原、W2–W4 施工。
