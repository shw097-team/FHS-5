# FHS-5_PLP｜W3｜START THIN PROMPT｜CODEX Native 產品施工

**用途**：本檔是已主用 W3 六檔的產品施工薄提示。它不是本輪修補 prompt，也不是 `00–03` 的摘要；啟動時只讀必要條款與真材料。
**artifact_id**：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`
**scope**：`W3-NF-01`｜**decision**：`W3-PACK-PRIMARY-20261126-01`
**pack_state**：`PACK_PRIMARY_SELECTED` / `PACK_EXECUTABLE`（本檔啟動前即成立；產品 readiness 另判）

---

## GOAL

在已主用 W3 pack 的同一 scope 內，完成可由 CODEX Native 無人值守啟動與交接的 W3 閉環：

`Frozen Challenge → FAR typed research → Guide Touchpoint-2 → 受權 Native repair/retest → distinct Checker / fresh Consumer → CLOSEOUT/HANDOFF`。

先做 W2 partial intake，不假設 W2 已驗收；先選材料齊且已具權的 P01/R0/R1 或隔離 smoke，不等待不存在的全域 readiness。

## 啟動檢查（一次）

1. 讀 `../../EXTERNAL_SEAL.json`、`../../W3_OWNER_ADOPTION.json`、`../../W3_CURRENT.json`；確認 `05` raw SHA、tree、artifact_id、scope 相符。任一不符即 `STOP_SCOPED`。
2. 讀本包 `00` 的 §00.2（決策/狀態/持續授權）、§02（33 FR）、§04（六 WP/DAG）、§07（W4 handoff）；`01` 的 write-set/rollback；`02` 的 O1–O7；`03` 的 16 案；`05` 的 sources/assets/case_refs/holds。
3. 讀 W2 `W2_CURRENT.json`、`25_` final handoff、`24_` five pins、`19_` pack；記 product/delivery 分帳、`PARTIAL`、writer `BLOCKED_NOT_ADMITTED`、oracle/case-set `CARRIED_NOT_REFROZEN`、raw seal partial。
4. 確認 `03` 的 16 案仍 `NOT_RUN`、`observed=null`；若被預填，拒絕啟動並記 `FALSE_OBSERVED`。

## 授權（已成立，不再逐項請示）

- 唯一 Human Owner 已預授權本 W3 pack 的修補、採納、合法起工與必要文件上推；決策 `W3-PACK-PRIMARY-20261126-01`。
- 允許：`R` 內新 W3 施工隔離根的 READ/DRAFT、P01 intake、隔離 fixture/test/smoke、受界可逆 W3 DEV/OPS、受影 retest、evidence、W3 文件 publication。
- 每 batch 只 bind exact `path/op/preimage/rollback`，檢查真 ACL/scope；一般 READ/可逆隔離修補/重驗不用新 grant。
- 不允許：W2 protected writer、改 W2 gate/marker、正式 Release/部署、force push、改 frozen subject/test/oracle/threshold、secret 進模型/argv/log。
- 產品 Host/runner/oracle 未 late-bind 時，只停受影 effect；其他合法工作續作。

## EXECUTE

1. **P01 Intake/Freeze**：建 `FreezeLedger`／`W2RequalificationMatrix`；五 pin 分開；W2 R0–R3 可先做合法 READ/準備；R4 只在 Owner 給 W2 新授權時。
2. **P02 Runner**：先 Search-Before-Build，重用 W1 `nf_reader`/runner/guard；缺則在 D1 exact target 建最小 adapter；固定 argv/cwd/timeout/expected；跑同案 POS/NEG，capture raw。
3. **P03 Challenge/Finding**：以 expected-before-observed 產八欄 Finding；至少兩類 failure class；NotCovered 逐案 reason/owner/resume；不得自簽 Checker。
4. **P04 FAR**：RQ0–8、五態、EvidenceGraph；每源 query/denominator/raw/time/scope/freshness/independence；UNAVAILABLE≠ZERO。
5. **P05 RCA/Alternatives/Advice**：每 decision Finding ≥2 實質 alternatives、Fit/NoFit、成本/風險/rollback；十 Advice 原名；advice 不是 Grant。
6. **P06 Guide2/repair/retest**：七鍵→九鍵 lossless；兩期真 receipt 或 `DELTA_UNVERIFIED`；缺期不 PARK；受權 patch 只改受影 ChangeCone；新 candidate 另 freeze/retest；distinct Checker/Consumer 分帳。
7. 每步記 actual receipt 並選下一個合法動作；不建第二 Runtime/Queue/Issuer/Registry。

## HARNESS LOOP

```text
READ 真 pack/seal/current/W2 pins
  → FirstFail + change_cone
  → Search-Before-Build（先 reuse 既有 caller）
  → 最小受權 patch（exact write set）
  → 受影 RED/GREEN + readback
  → new candidate freeze（若產品候選變）
  → distinct review / fresh consume
  → ACCEPT 或 STOP_SCOPED / PARTIAL
```

- 同 failure key 無新材料不重派；最多兩次有實質差額修補；暫態 READ/fetch 一次有理由 retry。
- 不改 oracle/threshold/gate 求綠；不用 exit 0 當 semantic PASS；不用同失敗當 parity。
- 安全 veto 只停受影；其他合法 READ/DRAFT 繼續。
- 缺 runner/oracle/Host/ACL 時，記 typed blocker 與最小 resume，不以空白或 `0` 補位。

## DONE

1. P01–P06 的實際輸出與 raw 可重播；16 原案 observed/verdict 依真跑更新，未跑仍 `NOT_RUN`。
2. 至少一 POS、一 NEG、兩類動態 finding、五態、十 Advice、七/九鍵、缺期/偽權/越界負例有真 receipt。
3. Guide 只回 `NextOperation/STOP/Resume` 候選；Next 不是 Grant；STOP 只停受影；Resume 有真 predicate。
4. 受影修補有新 candidate freeze、pre/post/restore、受影 retest；Checker/Consumer 分開。
5. 產 `W3_CLOSEOUT`／`W3_HANDOFF`／`W3_CHANGESET`／`W3_DELTA`，記 `W3_TECHNICALLY_READY`／`W3_EXECUTION_READY`／`W3_NF_VALIDATED` 的真實分帳；未成立即 `NOT_CLAIMED`。
6. W2 仍 `PARTIAL`／writer blocked；不得用 W3 成果解封或冒 W2 verdict。
7. 不 merge 無關 main/W2 歷史、不 force push、不 Release。

## 啟動拒絕條件

- seal/adoption/current 與 `05` 不符、scope/artifact_id 漂移。
- 16 案被填假 observed、case refs 少於 16、assets 缺、source span 越界。
- 要求用 W3 scope 解 W2 writer、刪 W2 marker、改 gate。
- 要求寫 frozen subject/test/oracle/threshold、path escape、secret 外送、不可逆 effect。
- 以 advice/Next/`permit=true`/ECP 表格當 Grant。

遇到任一項：zero-write、保 LastGood、交 typed blocker/Resume；不要「先跑再補」。

---

**薄提示終點**：啟動者應能直接選 P01/R0/R1 或隔離 smoke 開始，不需要再產計畫或等待 Owner 重複授權；但不得把文件主用當產品 readiness。
