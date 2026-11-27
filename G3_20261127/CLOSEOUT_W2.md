# W2 CLOSEOUT（G3，2026-11-27）

- candidate：`W2-G3-PCNF-r2`
- source manifest SHA-256：`7bdc4a0acb497944450d89a2c347d26ca4ac8593f6ee47ac229215a80ff227e0`
- pack tree SHA-256：`957013dd9d1152b5dd259c5d08a068b976ad2b3ef6251a9507128daf75a1bb0c`
- case set SHA-256：`a78e689d42265851eba8ea0deb6f125eac4da591c47e49c2f89f610051a16aaf`
- raw：`G3_20261127/runs/w2/`；summary：`runs/w2/W2_RESULT.json`

## 12 原案：**12/12 PASS**

| 案 | 實際觀測 |
|---|---|
| W2-DEV-01 POS | base `9fae9257a3402928efbe6ff0cd66f45761f52846`；preimage `c666740268cce914819e2ba43a0dbd9413de709792ee2c8338b0b67e895c74f0`（9336 B，與 ECP 記錄一致）；MODIFY＋ADD 真 gate apply；post `28bc674b564102b4…`／`7a364a28d2ea295e…`；`test_j1_receiver.py` **8 tests OK**；reverse 回 preimage；world 還原後 test absent；unlisted 不變 |
| W2-DEV-02 NEG | caller HEAD≠live → `REPO_HEAD_MISMATCH`；wrote=[]；receiver SHA 不變 |
| W2-OPS-01 POS | pre WorldRaw `ABSENT` → receiver 原子建立 `OPS-A/` receipt＋material → 獨立 consumer `all_ok` → `DELETE_CREATED_ONLY` → pre State 讀回 `ABSENT`；七觀測齊 |
| W2-OPS-02 NEG | `GIT_REVERT` → `RECOVERY_KIND_MISMATCH`；spy 空、world 不變 |
| W2-EFFECT-01 NEG | OPAQUE／PATH_INFERRED／空 token → `EFFECT_UNBOUND`；effect_calls=0 |
| W2-AUTH-01 NEG | issuer=null／expired／wrong principal → `FALSE_AUTHORITY`；0 effect |
| W2-RUNNER-01 NEG | 無 runner／oracle／fixture → `RUNNER_UNBOUND`；executed=false |
| W2-DELTA-01 POS | 兩期由 W0／W1 真 result 產生；same→`REUSE_LASTGOOD`；delta→`NEW_MATERIAL_EVIDENCE`；缺期→`DELTA_UNVERIFIED` |
| W2-R3-01 POS | 13 列＋3 NF；owner／resume 齊；null 保留 |
| W2-R3-02 NEG | G4 歷史 bytes → `NOT_ADMITTED` |
| W2-R3-03 NEG | historical preimage only／live null → `WRITESET_UNBOUND`；0 write |
| W2-R3-04 EDGE | 318 vs 317 → `WORKSPACE_DRIFT_BOUNDED` |

## Minimal repairs（根因 → 修復 → 重驗）

1. **ADD 不可執行（36_ 的 `0 executable` 根因之一）**：`w2_dev_gate.parse_patch` 拒絕 `/dev/null`，而 ADD 只能以此形式送 `git apply`。修補為「僅 `new file mode`＋a 側 null 可接受」，其餘 null 仍拒。`test_w2_gate` 12 tests OK。
2. **World 污染**：driver 匯入時產生 `__pycache__` 被判 foreign dirty。以 `sys.dont_write_bytecode`／`PYTHONDONTWRITEBYTECODE=1` 修正，非改 Oracle。

## 授權邊界

DEV 使用新決策 `W2-G3-OWNER-20261127-05`（isolated world、exact 2 target）；OPS 使用 `-06`（isolated output root、CREATE `OPS-A`）。舊 `-01` terminated、`-02/-03` superseded、`-04` pending 全列 revoked；未復活。

## Checker／Consumer

- 分離 Checker（同 principal）：**40 檢查 PASS**（PASS）。
- fresh process Consumer（同 principal）：**ACCEPT**。

## 判定

`W2_SCOPED_VALIDATED`（本 candidate、本 CODEX local host）。不宣其他 Host、Publisher／Release、原域 DEV ECP。
`W3_TECHNICAL_READY=true`；`W3_ADMITTED=false`（未取得 W3 exact grant，未執行 W3 effect）。
