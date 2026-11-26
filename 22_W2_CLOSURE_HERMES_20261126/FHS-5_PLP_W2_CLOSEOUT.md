# FHS-5_PLP_W2_CLOSEOUT (r2 closure)

**任務**：`HERMES-F5-W2-CLOSURE-r2`｜**subject／scope**：`FHS-5_PLP/W2/CONTROL_PACK`／`W2-NF-01`
**candidate**：`W2-NF-r3-CODEX-PRIMARY`｜**採用基線**：`35d5387f`（`hermes/w2-pack-nf-primary-20261126`）
**run root**：`W2_NATIVE_RUNS/20261126T1152_W2_CLOSURE/`｜**時間**：2026-11-26T12:06:09+0800

## STATUS

`PARTIAL — R01/R02/R03/R04 的受影義務實跑並讀回；R05 W3 接收已產收據；J3 ON/OFF 未跑`

| 判定 | 值 |
|---|---|
| `W2_EXECUTION_READY` | 成立（本輪 op 都在真前件下准入並產生效果） |
| `W2_NF_VALIDATED` | **不成立** — 12 原案 10/10 於本輪 runner 通過，但 J3 ON/OFF 未執行 |
| `W3_TECHNICALLY_READY` | 視 W3 收據（見 CLOSEOUT 尾） |
| `INDEPENDENT_PASS` | `NOT_CLAIMED`（Checker 與 Maker 同 principal、不同 session） |

## R01｜正式 W2 六檔真消費（修正前輪 `w2_pack_parse.ok=false`）

新增 `W1/impl/w2_nf_reader.py`（`FHS5.PLP.W2.SourceManifest.NF@2` 的真 Reader）。
前輪失敗原因：W1 的 `nf_reader.inspect_package` 找 `05_W1_SOURCE_MANIFEST.json`，對 W2 包必然 `PACK_INCOMPLETE_LOCAL`。

本輪實測輸出（`W2_CONTRACTS.json`）：

- views = `DEV, ENTRY, OPS, PD, PI, TQAEP`
- counts：pack_files 5、assets 25、sources 24、requirements 16、cases 12、CR 37、HOLD 14、W2 專項 6
- `DEV.write_set_rows_parsed` 由 `01_W2_DEV_ECP.md` 的表真解析（非 count）
- `ok = True`，`problems = []`

OPS-O03 重跑後 `w2_pack_ok = True`（前輪為 false）。

### J1 殘餘安全（6 → 7 子例）

| 項 | 修補 | 證據 |
|---|---|---|
| duplicate JSON keys | `_parse_json_bytes` 全拒 | S1 PASS |
| NaN／Infinity | `parse_constant` 拒絕 | S2 PASS |
| BOM | 拒 | S3 PASS |
| identity 用 substring | 改為 `scope:` 欄位精確比對 | S4／S4b PASS |
| verify→consume 綁定 | `consume_verified` 重算 manifest/seal，`TOCTOU_DRIFT` | S5 PASS |
| 控制 | 乾淨驗證→consume 仍成功 | S6 PASS |

`python -m unittest test_j1_strict` **7/7**；`test_j1_receiver` **6/6**（無回歸）。

## R02｜原案、UNKNOWN、兩域效果

### 12 原案（本輪真 runner，`W2_CASE_LEDGER_R2.json`）

PASS 10／FAIL 0，共 10 案：
W2-DEV-01, W2-DEV-02, W2-EFFECT-01, W2-AUTH-01, W2-R3-03, W2-R3-02, W2-OPS-02, W2-RUNNER-01, W2-R3-01, W2-R3-04

每案都有獨立 expected／observed／verdict，使用真 scratch git repo 與真 `w2_dev_gate.py`（本輪新增，DEV 准入閘：effect token、admission、scope、principal domain、live HEAD、exact write set、preimage、dirty 保留、recovery kind）。

發現並修正的環境差額：Windows `subprocess` 文字模式把 patch 的 `\n` 轉成 `\r\n`，導致 `git apply`／`patch -R` 以「different line endings」失敗。改為 bytes 輸入後通過 — 這也是 prompt 指出的「Windows subprocess raw capture」同源問題。

### UNKNOWN 四類（`W2_UNKNOWN_FIXTURES.json`）

| fixture | 真狀態 | 決策 |
|---|---|---|
| F-TO-BEFORE | `STILL_PRE` | `RETRY_ONCE_ALLOWED_IF_GRANT_VALID_AND_IDEMPOTENT` |
| F-TO-AFTER | `POST_REACHED` | `VERIFY_NO_OP_DO_NOT_REPEAT` |
| F-PARTIAL | `PARTIAL` | `SCOPED_COMPENSATION_OR_STOP` |
| F-EXIT0-WRONG | `EXIT0_WRONG_POST` | `EFFECT_NOT_VERIFIED_NOT_PASS` |

4/4 PASS；每筆都是 runner 造成的真磁碟狀態，不是傳入 enum。

### 兩域效果（重跑）

- DEV：gate → apply → post sha → reverse（byte-exact 還原 preimage）
- OPS：O03 exit 0、accepted `True`、created 8 檔、pre `44136fa355b3…` → post `4ebfa5f7e7a6…`
- O04 `VERIFIED` 10/10
- O05 `RECOVERED` 4/4，`HOST_SPECIFIC_DELETE_CREATED_ONLY`，world 回 pre

## R03｜ChangeSet、Guide 九鍵雙期

- ChangeSet：committed 17 列、pending 3 列，每列 exact kind/path/before/after；`changeset_present=True`
- Guide 九鍵：`delta_verdict = NEW_MATERIAL_EVIDENCE`；相同鍵 ['subject', 'scope', 'source_sha', 'host_id']；不同鍵 ['repo_head', 'policy_epoch', 'oracle_sha', 'world_raw_sha', 'first_fail']
- `policy_epoch` 兩期皆 null 但記為 **unknown，非 same**（兩個 null 不是同值主張）

## R04｜證據差額處置

| 差額 | 處置 |
|---|---|
| `maker_tests.txt` 934 B／916 B（CRLF） | 加 `.gitattributes` `21_W2_PRODUCT_HERMES_20261126/** -text` 並 `git add --renormalize`；現 worktree 934 = blob 934 |
| CLOSEOUT 寫 `49c62def…` vs 收據 `44136fa3…` | 真值為 `44136fa3…`（O03/O05/ledger 一致）；前輪 CLOSEOUT 文字為錯，本輪以真值記並保留歷史差額 |

## 未完成（具名，不假結案）

| 項 | FirstFail | Owner | Resume |
|---|---|---|---|
| J3 真 ON/OFF | `NOT_RUN` | W2 Executor | 同 candidate 的隔離 ON/OFF roots＋正控 |
| W3 正式包 | `W3_PACK_ABSENT` | W3 Owner | W3 當期主用包 |
| `policy_epoch` | `NOT_DECLARED_BY_HOST` | Host Owner | Host 宣告 epoch |

## 原始證據

全部在 `W2_NATIVE_RUNS/20261126T1152_W2_CLOSURE/`：`00_PREFLIGHT`、`30_VERIFY/raw_*`、`40_OPS`（已回復）、`50_EVIDENCE`、`60_CLOSEOUT`。
