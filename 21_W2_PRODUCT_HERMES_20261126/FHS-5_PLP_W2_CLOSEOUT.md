# FHS-5_PLP_W2_CLOSEOUT

**任務**：`HERMES-F5-W2-PRODUCT-r1`
**subject／scope**：`FHS-5_PLP/W2/CONTROL_PACK`／`W2-NF-01`
**candidate**：`W2-NF-r3-CODEX-PRIMARY`（`FHS5-PLP/W2/PACK-NF-20261126-r3`）
**採納基線**：分支 `hermes/w2-pack-nf-primary-20261126`，HEAD `35d5387f9c98eaebc2d4cee742afcb4509a7d8c3`
**R**：`C:\Projects\Agent_Workspace\FHS-5_Workspace`（唯一工程寫入根）
**run root**：`W2_NATIVE_RUNS/20261126T1121_W2_PRODUCT/`
**時間**：2026-11-26（Asia/Taipei）

## STATUS

`PARTIAL — 真 DEV 與真 OPS 兩域皆已實跑並讀回；W2_NF_VALIDATED 未成立`

- `W2_EXECUTION_READY`：**成立**（首個合法 op 已在真前件下准入並產生世界效果）
- `W2_NF_VALIDATED`：**不成立**（12 原案中 3 PASS、1 PASS_WITH_CAVEAT、1 PARTIAL、3 STRUCTURAL_ONLY、4 NOT_RUN；J3 未跑）
- `W3_TECHNICALLY_READY`：`NOT_CLAIMED`（本輪未產 W3 receive 材料）
- `INDEPENDENT_PASS`：`NOT_CLAIMED`（Checker 與 Maker 不同 session，但同 principal）
- `RELEASED`／`M-DONE`：`NOT_CLAIMED`

## 1｜基線核對（實算，非引用）

| 項 | 宣告值 | 實測 | 結果 |
|---|---|---|---|
| 採用 HEAD | `35d5387f…` | `35d5387f…`（fetch 後 `rev-parse`） | MATCH |
| `05_W2_SOURCE_MANIFEST.json` raw | `81daac8f…`／65,377 B | `81daac8f…`／65,377 B | MATCH |
| `W2_OWNER_DECISION.json` raw | `1ef19c0f…` | `1ef19c0f…`（4,595 B） | MATCH |
| 五 MD + 25 assets | manifest 自載 | 5/5、25/25 | MATCH |
| source-set digest | `921de70c…` | `921de70c…` | MATCH |
| G1 receiver pin | `c6667402…`／9,336 B | 由 `git cat-file blob` 重算 | MATCH |

包以 `git archive` 自採用 commit 落 `10_PACK`（35 檔），不以 Downloads 副本當真源。

## 2｜真 DEV（DEV-D01 → D07）

worktree：`20_DEV/worktree`，分支 `w2nf/dev-d04`，base `35d5387f`，dirty 0。R 主工作樹全程未動（untracked 維持 2,365）。

| op | 結果 |
|---|---|
| D01/D02/D03 | 真 probe 與 target 凍結；preimage `c6667402…` 實測 |
| **D04** | **EFFECT_APPLIED**。write set 恰 2 檔，無 unlisted drift |
| D05 | maker 測試 `python -m unittest test_j1_receiver` exit 0（6/6）；本輪獨立 oracle 21/21 PASS；硬化探測 PASS |
| D06 | **RECOVERED**：反向 patch 在獨立同前像副本套用後回到 `c6667402…`（位元級），新增檔刪除；候選仍在 worktree |
| D07 | candidate frozen（見 §5） |

| # | path | op | before | after |
|---|---|---|---|---|
| 1 | `W1/check/w2_receiver.py` | MODIFY | `c6667402…`（9,336 B） | `ee92c8c8…`（38,753 B） |
| 2 | `W1/check/test_j1_receiver.py` | ADD | absent | `0dab8ebf…`（18,158 B） |

生產者：`codex-cli 0.164.0`（`codex exec -s workspace-write`，真 CODEX 為產品 writer）。

### 2.1 修補前後的可觀測差異

修補前後都以同一組探針對 pinned／修補後 bytes 實跑：

| 缺陷 | 修補前（pinned） | 修補後 |
|---|---|---|
| 失敗路徑仍呼叫產品 | `build_contracts`×3、`seam_wiring`×1（假 grant／錯 pin） | 0／0 |
| `../` 逃逸 | `evidence_manifest_recompute` 回 ok=true | `first_fail=PATH_ESCAPE`（外部 pin 重新對齊後仍拒，證明是 confinement 而非 pin 檢查擋下） |
| 真實 junction 逃逸 | 未測 | `first_fail=PATH_ESCAPE`（`mklink /J` 真建立） |
| 輸入端被覆寫 | `context_bundle.md` 被接收動作覆寫 | 交付樹前後 hash 不變 |
| 僞造 pack 檔 | `pack_inspect` 拒（既有控制） | 仍拒（未退化） |

## 3｜真 OPS（O01 → O06）

output root：`40_OPS`（受權、隔離）。R2 receiver ＝ D04 修補後的 `w2_receiver.py`。

| op | 結果 | 關鍵值 |
|---|---|---|
| O01/O02 | host/principal/epoch/target/preimage 真 probe | `DESKTOP-57EO414`／`desktop-57eo414\user`／`epoch_state=NOT_DECLARED_BY_HOST` |
| **O03** | **EFFECT_APPLIED**（exit 0、accepted=true、44 checks） | pre-world digest `49c62def…`（空）→ post `5d6c7006…`；created 8 檔；`stage → os.replace` 原子發布 |
| **O04** | **VERIFIED 10/10**（另一程序讀回） | receipt sha 一致、交付樹未變、material 在交付樹外 |
| **O05** | **RECOVERED 4/4** | `HOST_SPECIFIC_DELETE_CREATED_ONLY`；刪 8 檔；world 回到 pre digest；`git_revert/reset/clean` 皆 false |

**負例（保留為證據）**：以 `--scope W2-NF-01` 呼叫 R2 時被拒（exit 5、`first_fail=SCOPE_MISMATCH`）。原因是 receiver 的主體是 W1 交付（`W1-NF-01`），W2 subject 由 WorldEffectRecord 承載。此為真觀測，未事後改寫。

## 4｜J1 真接收

- 修補前 6 案：3 缺陷成立、2 控制成立（`20_DEV/j1_red/raw/J1_VERIFY_ONLY.json`）
- 修補後：maker 6/6、本輪獨立 oracle 21/21、硬化探測 H0/H1/H2 全 PASS
- 外置信任根：`30_VERIFY/expected_pins.json`（不由交付自帶 seal 自證）
- 未產生 `W2_RECEIVE_RECEIPT` 之外的 W3 接收（見 §6）

## 5｜J2／J3 與 W2 六檔消費

| 項 | 狀態 |
|---|---|
| W2 六檔真 parse | `CONSUMED 21/21`（`50_EVIDENCE/W2_PACK_CONSUMER_RECEIPT.json`）：strict JSON、6 檔重算、25 assets、16 requirements、12 cases、37 CR、14 HOLD＋6 專項、case_index exact set |
| 為何 BUILD_MINIMAL | repo 的 `nf_reader.inspect_package` 拒收 W2 包（`PACK_INCOMPLETE_LOCAL: 05_W1_SOURCE_MANIFEST.json`）；無既有 W2 consumer |
| J2-pre | 欄級讀回成立（上列） |
| J2-post | `NOT_RUN`：本輪未在 J2 時點產 ChangeSet（ChangeSet 是後驗，不倒卡 P03） |
| J3 | `NOT_RUN`：ON/OFF parity、正控、雙失敗拒未執行 |

## 6｜W3 接續

`NOT_CLAIMED`。可交 W3 的 typed 欄位已備（`WorldEffectLedger`：effect receipt、pre/post world digest、recovery kind、epoch_state、admission ref），但缺：

1. 五 pin × fixture/runner 的凍結清冊（部分已在 pins/case ledger，未成 W3 接收包）
2. J3 OFF 證據
3. Guide 九鍵雙期

最短 Next：先補 J3 與 J2-post，再以 `W2M §12.3.1` 產 W3 clean receive。

## 7｜Claim 分帳

| 可宣 | 不可宣 |
|---|---|
| 真 DEV 一筆（2 檔、pre/post、reverse 讀回） | `W2-DEV-02`／`W2-DELTA-01` PASS |
| 真 OPS 一筆（pre/post WorldRaw、consumer、host-specific compensation） | `W2_NF_VALIDATED` |
| J1 修補真有效（21/21＋硬化） | `INDEPENDENT_PASS` |
| `W2_EXECUTION_READY` | `W3_TECHNICALLY_READY`／`RELEASED`／`M-DONE` |

## 8｜原始證據位置

全部在 run root（`W2_NATIVE_RUNS/20261126T1121_W2_PRODUCT/`）：

- `00_PREFLIGHT/P01_pack_integrity.json`、`P02_repo_host_bind.json`
- `20_DEV/j1_red/raw/J1_VERIFY_ONLY.json`
- `30_VERIFY/expected_pins.json`、`checker_j1.py`＋`raw/CHECKER_J1_ORACLE.json`、`harden_probe.py`＋`raw/HARDENING_PROBE.json`、`raw_maker_tests.txt`、`recovery/`
- `40_OPS/`（世界效果，已由 O05 回復；`OPS_O03/O04/O05` 紀錄在 `50_EVIDENCE/ops/`）
- `50_EVIDENCE/W2_PACK_CONSUMER_RECEIPT.json`
- `60_CLOSEOUT/W2_WORLD_EFFECT_LEDGER.json`、`W2_CASE_LEDGER.json`

## 9｜未完成與 Resume predicate

| 項 | FirstFail | Owner | Resume |
|---|---|---|---|
| J3 ON/OFF parity | `NOT_RUN` | W2 Executor | 同 candidate 的隔離 ON/OFF roots＋正控 |
| J2-post ChangeSet | `NOT_RUN` | W2 Executor | 交付 commit 後的 exact kind/path/before/after |
| W2-DEV-02 caller-HEAD 不符 | `NOT_RUN` | W2 Executor | 注入 caller HEAD 與 live 不符 |
| W3 receive | `W3_PACK_ABSENT` | W3 Owner | W3 正式包或最小接收材料 |
| `policy_epoch` | `NOT_DECLARED_BY_HOST` | Host Owner | Host 宣告 epoch；本輪以事實記錄，未造值 |
