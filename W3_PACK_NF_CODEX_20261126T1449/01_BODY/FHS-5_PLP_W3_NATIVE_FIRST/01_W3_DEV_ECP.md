# FHS-5_PLP｜W3｜DEV ECP｜受界 W3 施工與寫入契約

**artifact_kind**：`WaveControlPack / DEV-ECP`
**project_id**：`FHS-5_PLP`｜**wave_id**：`W3`
**subject_id**：`FHS-5_PLP/W3/CONTROL_PACK`｜**scope**：`W3-NF-01`
**artifact_id**：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`｜**version**：`r2`
**selection_state**：`PACK_PRIMARY_SELECTED`（決策 `W3-PACK-PRIMARY-20261126-01`）
**claim_ceiling**：`PACK_PRIMARY / LOCAL_DOCUMENT_VERIFIED / PACK_EXECUTABLE`
**日期**：2026-11-26（Asia/Taipei）

> **一句話**：本檔不是「再向 Owner 要一次授權」的表格；它是已主用 W3 包的 DEV exact contract。每次真正寫入前，執行者只在批次層綁定 `path/op/preimage/rollback`，檢查真 ACL 與 scope，然後執行；W2 protected writer 不在本檔授權內。

---

# 01｜Goal 與授權法位

## 01.1 本 ECP 要解決什麼

W3 產品施工需要新增或修改受界程式與測試，讓 `FreezeLedger → CaseRunRecord → FindingSet → FARRetrievalGraph → DecisionAdvice → Guide2Handoff → 受權 repair/retest → new freeze → Checker/Consumer` 可由 CODEX Native 實際執行、留 raw、可回滾。若只停在文件、fixture 與計畫，`PACK_EXECUTABLE` 不成立。

本 ECP 的 Done：

1. 每個 W3 施工 batch 都有精確路徑、操作、preimage 或 absence、命令、expected exit、raw、rollback 與受影測試。
2. 新增能力優先重用既有 `W1/impl`、`W1/check`、TPM/Reviewer/Challenge/FAR/Guide/Bridge caller；只有真缺口才建最小 `W3/` slice。
3. 受保護的 W2 writer、原 frozen subject/test/oracle/threshold 完全不在 write set。
4. 任何失敗只停受影 effect；其他合法 READ/DRAFT 續作；不以 exit 0 當 semantic PASS。

## 01.2 授權來源與邊界

| 欄位 | 有效值 |
|---|---|
| `decision_id` | `W3-PACK-PRIMARY-20261126-01` |
| `decision_maker` / `issuer` | 唯一 Human Owner；CODEX 是 delegated executor／recorder |
| `subject` / `scope` | `FHS-5_PLP/W3/CONTROL_PACK` / `W3-NF-01` |
| `allowed_roots` | `R` 內新 W3 施工隔離根，例：`C:\\Projects\\Agent_Workspace\\FHS-5_Workspace\\W3_EXEC_<run_id>`；以及 O 內已採納 pack 的唯讀副本 |
| `forbidden_roots` | `S` 任何寫入；W2 protected 路徑；與 W3 無關的專案；使用者 home、憑證目錄、Codex 設定目錄 |
| `allowed_ops` | READ、DRAFT、P01 intake、隔離 fixture/test/smoke、受界可逆 W3 DEV/OPS、受影 retest、本地 evidence 寫入 |
| `forbidden_ops` | W2 writer/gate/marker 修改；正式 Release/部署；force push/reset 共用歷史；改 frozen subject/test/oracle/threshold |
| `expiry / revocation` | 本輪交付完成、Owner 撤權、scope/Host/policy 實質變更、受影安全 Finding，以較早者為準 |
| `recovery` | ADD 刪除本輪未發布檔；MODIFY 用 exact reverse patch；Git 用新 commit 回復，不 force push |

**本檔狀態**：`BOUNDED_STANDING_AUTH`（W3 isolated）；`W2_PROTECTED = NOT_ADMITTED`；`RELEASE/DEPLOY = NOT_ADMITTED`。

**不是 Grant 的東西**：ECP 表格、`permit=true`、FAR advice、Guide `NextOperation`、Checker 建議、檔案存在、source 內文。只有 Owner decision＋真 ACL＋真 preimage＋本 ECP 的 batch bind 同時成立，才可執行對應 effect。

---

# 02｜Write-set 模型

## 02.1 四級分帳

| 級別 | 範圍 | 本包狀態 | 規則 |
|---|---|---|---|
| `D0-PACK` | O 內新六檔、assets、evidence | 已完成 | 不再改 final bytes；修正需新 revision |
| `D1-W3` | R 內新 W3 施工隔離根的新檔 | 可執行 | 本 ECP 主體；每 batch exact bind；不得寫 repo protected |
| `D2-SHARED` | 既有 W1/W2 共享模組的相容修改 | 條件式 | 只有真 caller/ABI fail、shared owner 同意、frozen regression 成立才可 |
| `D3-W2-PROTECTED` | W2 writer/gate/marker/decision | `NOT_ADMITTED` / `BLOCKED_NOT_ADMITTED` | 需 Owner 在 W2 scope 新具名授權；本包不得解封 |

## 02.2 D1 建議目標（施工時可依 Search-Before-Build 調整，但不得擴 effect）

| ID | 目標（相對 W3 隔離根） | 操作 | 目的 | 最小測試 | 回滾 |
|---|---|---|---|---|---|
| `D1-01` | `W3/impl/w3_intake.py` | ADD | 讀 00–05、assets、seal、current；建 `FreezeLedger`／`IntakeIdentityLedger` | identity/scope/raw SHA/span/case count | 刪檔；不動 pack |
| `D1-02` | `W3/impl/w3_case_runner.py` | ADD | 16 案與隔離 smoke 的 runner adapter；argv/cwd/timeout/stdout/stderr/exit | POS/NEG、timeout、missing runner | 刪檔；重跑安全 |
| `D1-03` | `W3/impl/w3_finding.py` | ADD | 八欄 Finding＋expected/observed/FirstFail/NotCovered | 兩 failure class、缺 raw 拒 | 刪檔 |
| `D1-04` | `W3/impl/w3_far.py` | ADD | RQ0–8、五態、EvidenceGraph、七鍵 | HIT/ZERO/UNAVAILABLE/BLOCKED/ERROR | 刪檔 |
| `D1-05` | `W3/impl/w3_advice.py` | ADD | 每 Finding ≥2 alternatives、十 Advice 原名、Fit/NoFit/成本/風險/rollback | 單方案拒、第 11 enum 拒 | 刪檔 |
| `D1-06` | `W3/impl/w3_guide2.py` | ADD | 七鍵→九鍵 lossless、兩期 delta、Next/STOP/Resume | 缺期不 PARK、跨 scope 拒 | 刪檔 |
| `D1-07` | `W3/impl/w3_repair.py` | ADD | 受權 patch/retest routing、new candidate freeze、Checker/Consumer 分帳 | advice 非 grant、撤權拒寫 | 刪檔 |
| `D1-08` | `W3/check/run_w3_case.py` | ADD | 單案 CLI；輸出 raw receipt | 16 案 discovery、unknown case 拒 | 刪檔 |
| `D1-09` | `W3/check/test_w3_contracts.py` | ADD | stdlib unittest：schema、五態、十 Advice、七/九鍵、path safety | 全綠；負例紅 | 刪檔 |
| `D1-10` | `W3/spec/W3_CASE_SET.json` | ADD | 16 案 ID/kind/req/fixture/oracle/runner binding | 16 join、duplicate 拒 | 刪檔 |
| `D1-11` | `W3/spec/W3_RUNNER_BIND.json` | ADD | runner identity/policy/argv/timeout/Host | 無 runner 時 `UNBOUND` | 刪檔 |
| `D1-12` | `W3/evidence/<run_id>/` | ADD | raw、checks、receipts、replay | manifest/bytes/SHA | 刪本 run 目錄 |

**Search-Before-Build 優先序**：

1. 先查 W1 `nf_reader.py`、`bridge_nf.py`、`tpm_contracts_nf.py`、`guide_nf.py` 的 caller/ABI 是否已支援 W3 16 案與 source domain；能 reuse 就不建 D1-01/02/03。
2. 再查 W0 `challenge.py`、`far_run.py`、`guide.py` 的 pattern；只參考，不把 W0 sample 當 W3 輸入。
3. 再查 repo 既有 `W1/check` 的 runner/guard/replay；能 bind 就不建第二 harness。
4. 只有以上皆缺、且真 caller/contract 證實缺口，才建最小 `W3/impl`。

## 02.3 D2 條件式共享修改

| ID | 目標 | 操作 | 何時允許 | 必跑 regression | 回滾 |
|---|---|---|---|---|---|
| `D2-01` | `W1/impl/nf_reader.py` | MODIFY | 真 W3 05/source_set 無法 parse，且 shared owner 同意 | W1 reader cases + W3 intake | exact reverse patch |
| `D2-02` | `W1/impl/bridge_nf.py` | MODIFY | 四 API 真 fail 於 W3 新材料，且 direct 路徑不足以滿足 consumer | Bridge 原 38+28 受影 + W3 consume | exact reverse patch |
| `D2-03` | `W1/impl/tpm_contracts_nf.py` | MODIFY | W3 16 Case parser/discovery 真漏 row | W1 TPM/Reviewer cases | exact reverse patch |
| `D2-04` | `W1/impl/guide_nf.py` | MODIFY | 七/九鍵真 lossless fail | Guide 原 17 受影 + W3 Guide2 | exact reverse patch |
| `D2-05` | `W1/check/*` | MODIFY | 真 guard/replay 不支援 W3 schema | 全部受影 W1 測試 | exact reverse patch |

**禁止**：因「想統一」重寫整個 W1；改 W2 trust/marker；把 W3 scope 借給 W2；以新 hash 冒原 ABI。

## 02.4 D3 W2 protected（明確排除）

以下一律 `NOT_ADMITTED`，直到 Owner 在 **W2 scope** 新具名授權：

- `W2_CURRENT.json`、`25_` closeout/handoff/manifest、`24_` five pins；
- `W2_NATIVE_RUNS/W2_SECURITY_FINDING.json` 或任何撤權 marker；
- W2 writer、dev gate、admission、receiver 的 trust 設定；
- W2 12 案的 oracle/fixture/case-set 真 bytes（可由 W2 Case Owner 在 W2 scope 凍結，但不由 W3 代簽）。

W3 只可讀 W2 的公開/交付 bytes，建 `W2RequalificationMatrix`；不得把 W2 `PARTIAL` 當 PASS。

---

# 03｜Batch bind 程序（每次副作用前）

## 03.1 八步

1. **Scope check**：確認 subject=`FHS-5_PLP/W3/CONTROL_PACK`、scope=`W3-NF-01`、decision 未過期、未被撤權。
2. **Root check**：`Resolve-Path`／`realpath` 後確認 target 在 allowed root 內；拒絕 prefix-sibling、`..`、symlink/junction/reparse escape、大小寫碰撞。
3. **Preimage**：MODIFY 取真 SHA-256、bytes、mtime；ADD 證明 absence；若同名檔存在，改 MODIFY 並附 preimage，不得靜默覆寫。
4. **Write-set**：列 exact paths；不得 glob；不得 `git add .`；不得順手改相鄰檔。
5. **Expected**：先凍結 command、argv、cwd、timeout、expected exit、expected token、predicate；看到 observed 後不得改。
6. **ACL/Effect**：確認 OS 使用者、repo principal、Host、policy epoch；產品 Host 未綁時只做隔離 smoke。
7. **Execute**：最小命令；capture stdout/stderr/exit；不把 secret 傳入 env；timeout 不得殺他人 process。
8. **Readback**：post SHA、diff、test raw、consumer parse；失敗則 exact rollback，記 FirstFail。

## 03.2 Batch receipt 最小欄

```json
{
  "batch_id": "W3-DEV-<run_id>-<nn>",
  "decision_id": "W3-PACK-PRIMARY-20261126-01",
  "subject_id": "FHS-5_PLP/W3/CONTROL_PACK",
  "scope": "W3-NF-01",
  "root": "<absolute W3 isolated root>",
  "targets": [{"path": "...", "op": "ADD|MODIFY", "preimage_sha256": null, "post_sha256": "..."}],
  "commands": [{"argv": [], "cwd": "...", "timeout_s": 120, "exit": 0}],
  "expected": {"exit": 0, "token": "...", "predicate": "..."},
  "observed": {"exit": 0, "stdout_sha256": "...", "stderr_sha256": "..."},
  "affected_tests": ["..."],
  "rollback": {"kind": "delete|reverse_patch", "ref": "..."},
  "acl": {"principal": "...", "host": "...", "policy_epoch": "..."},
  "verdict": "PASS|FAIL|PARTIAL|BLOCKED_HITL|BLOCKED_EXTERNAL",
  "raw_ref": "02_EVIDENCE/raw/..."
}
```

`PASS` 只表示該 batch 的 exact predicate 成立；不升格為產品 `W3_NF_VALIDATED`。

---

# 04｜Commands、tests 與 raw

## 04.1 基本命令

```powershell
# 只讀 intake
python .\W3\check\run_w3_case.py --pack <pack-root> --case W3-FRZ-01 --dry-read

# 隔離 smoke（無產品 Host）
python .\W3\check\run_w3_case.py --pack <pack-root> --case W3-FRZ-01 --isolated

# 契約測試
python -m unittest discover -s .\W3\check -p "test_*.py" -v

# 受影 regression（只有 D2 真改時）
python -m unittest discover -s .\W1\check -p "test_*.py" -v
```

## 04.2 Exit / predicate

| 情況 | exit | verdict | 備註 |
|---|---:|---|---|
| expected/observed semantic match | 0 | `PASS` | 需 token+predicate+raw |
| 正確拒絕（NEG/security） | 2 | `PASS`（負例） | 拒絕本身是預期 |
| 權限/ACL 阻斷 | 3 | `BLOCKED_HITL`／`BLOCKED_EXTERNAL` | 不繞權 |
| runner 缺失 | 4 | `NOT_RUN`／`RUNNER_UNBOUND` | 不 shell 替代 |
| 不可重現 | 5 | `UNREPRODUCED` | reproduction 欄，不是第六 verdict |
| 內部錯誤 | 1 | `FAIL` | 保 raw |

exit 0 不是 semantic PASS；必須有 expected-before-observed、raw SHA、predicate 與 consumer parse。

## 04.3 raw 保存

- stdout、stderr、world、argv、cwd、exit、runner identity、Host、policy epoch、pre/post SHA。
- 每個 raw 有 bytes+sha256；manifest 與 raw 分開；不用 summary 代 raw。
- 私有 raw 不推 public；公開 export 用邏輯 locator＋redaction。

---

# 05｜受影測試與變更控制

## 05.1 測試層級

| 層 | 範圍 | 何時跑 | 不可冒充 |
|---|---|---|---|
| `UNIT` | 單一 parser/predicate | 每次 D1 修改 | 產品 E2E |
| `CONTRACT` | schema、五態、十 Advice、七/九鍵、路徑安全 | 每次 pack/reader 修改 | 真 runner |
| `SMOKE` | 隔離 fixture 跨 Freeze→Finding→FAR→Guide2 | 每批 D1 整合 | 16 原案全量 |
| `AFFECTED` | 受影 case/consumer | 修補後 | 全域 readiness |
| `PRODUCT` | 真 16 案＋Host | 真 runner/oracle/Host 綁定後 | 文件 PASS |

## 05.2 每次修補的最小回流

```text
FirstFail + expected/observed + raw
  → ChangeCone（哪些 case/consumer/模組受影）
  → 最小 patch（exact write set）
  → affected RED → GREEN
  → new candidate freeze（若產品 candidate 變）
  → distinct Checker / fresh Consumer
  → ACCEPT 或 STOP_SCOPED
```

同一 failure key 無新材料不重派；最多兩次有實質差額修補；暫態 READ/fetch 可一次有理由 retry。

## 05.3 安全負例（必測）

1. 05 raw SHA 與 seal 不符 → zero write。
2. `../`、絕對路徑、junction/reparse escape → `INVALID_PATH`。
3. duplicate JSON key → 拒。
4. 16 案 observed 非 null 或 verdict 非 `NOT_RUN` 的 design 包 → 拒升格。
5. advice/NextOperation 被當 Grant → `FALSE_AUTHORITY`。
6. 同一 process 自簽 Checker/Consumer → `FALSE_INDEPENDENT`。
7. W2 writer revoked 仍寫 → `BLOCKED_BY_AUTHORITY`。
8. secret 出現在 argv/env/log → 立即停，清理，記 security finding。

---

# 06｜W2 接續與分工

W3 DEV 不得把 W2 當已驗收，也不得解封 W2。R0–R7 的責任：

| Step | W3 DEV 可做 | 不可做 |
|---|---|---|
| R0 | 讀 W2 current/delivery、五 member、pins；建 intake ledger | 改 W2 current |
| R1 | 讀 W2 pack 6+25 assets、12 案 trace | 代 W2 簽 verdict |
| R2 | 準備隔離 fixture/schema/reader | 凍結 W2 oracle/case-set |
| R3 | 設計 raw manifest/seal 格式 | 補造 W2 stdout/exit |
| R4 | 記 `W2_WRITER_BLOCKED`、resume predicate | 借 W3 scope 寫 W2 |
| R5 | 只讀受影 raw；必要時隔離 regression | 改 W2 gate/marker |
| R6 | 提供 distinct review 的介面 | 冒原域 Checker |
| R7 | fresh receive W3 pack；記 receipt | 以 W3 receive 升 W2 |

---

# 07｜Rollback／Recovery

| 類型 | 方法 | 驗證 |
|---|---|---|
| ADD 檔 | 刪除本輪未發布檔 | 目錄 byte/SHA 回到 preimage |
| MODIFY 檔 | exact reverse patch；保留 before bytes | post SHA == preimage |
| 測試污染 | 刪除 run 目錄；重跑乾淨 copy | raw 不含舊 run |
| Git 本地 | 新 commit 或 restore 指定檔；不用 reset 共用歷史 | `git status` 乾淨 |
| Git remote | 新 commit 補正；不 force push | remote readback |
| 程序 | 終止自身 child；讀回 exit/pid | 無 orphan |
| 安全事件 | 停受影 writer；保 LastGood；記 finding | 不刪原 marker |

**LastGood**：每次 batch 前保存 `preimage` 與 `lastgood_ref`；失敗不覆蓋。r1 是本輪文件 LastGood；不得刪。

---

# 08｜Stop／Resume

## 08.1 立即停（只停受影）

- 偽造/過期 decision、scope 漂移、seal 不符。
- 寫 frozen subject/test/oracle/threshold。
- path escape/symlink/junction/reparse、大小寫碰撞。
- 撤權仍寫、W2 marker 被動。
- secret 進入 argv/env/log/repo。
- 不可逆或未知 effect。
- 同一 process 自簽 Checker/Consumer。

## 08.2 可續

- 缺 runner/oracle/Host/ACL：只停該案或該 op；其他 READ/DRAFT/文件/隔離 smoke 續作。
- 暫態網路/讀取失敗：一次有理由 retry；仍失敗記 typed blocker。
- 產品未跑：保 `NOT_RUN`；文件主用與合法起工不受阻。

## 08.3 Resume predicate

必須是同 subject/scope、同 candidate/pin（或真新 revision）、真 raw/ACL、預期命令與 rollback 可重建；不得用「Owner 再看看」當唯一 predicate。

---

# 09｜Done 與交付

DEV 完成的最小證明：

1. D1 目標（或 reuse 的實際 caller）可執行；命令/exit/raw 可重播。
2. 16 案 discovery 與 case refs join 成立；未跑案仍 `NOT_RUN`。
3. 至少一 POS、一 NEG、兩類 failure class、五態、十 Advice、七/九鍵 smoke 真跑。
4. 受影測試 RED→GREEN；無未處置 BLOCKER/MAJOR。
5. `W3_DEV_RECEIPT.json`、raw manifest、batch ledger、rollback 記錄齊。
6. 未宣 `W3_NF_VALIDATED`／`INDEPENDENT_PASS`／`RELEASED`，除非原判準真成立。

---

**本檔終點**：W3 DEV 的可施工 exact contract 已成立；W2 protected 仍 `BLOCKED_NOT_ADMITTED`；正式產品 verdict 不在本檔代簽。
