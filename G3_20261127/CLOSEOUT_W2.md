# W2 CLOSEOUT（G3-FINAL-DELTA，2026-11-27）

- candidate：`W2-G3-PCNF-r2`；manifest `7bdc4a0acb497944450d89a2c347d26ca4ac8593f6ee47ac229215a80ff227e0`

## 真結果：**9 PASS＋3 NOT_ADMITTED**

| 類 | 案 |
|---|---|
| PASS | `W2-EFFECT-01`、`W2-AUTH-01`、`W2-RUNNER-01`、`W2-DELTA-01`、`W2-R3-01..04`、`W2-OPS-02`（共 9） |
| NOT_ADMITTED | `W2-DEV-01`、`W2-DEV-02`、`W2-OPS-01` |

## R04 信任邊界修復

- `run_w2.py` 不再自簽 Owner Decision；decision 標 `grant_state=REQUEST_ONLY`、`issuer_state=PENDING_EXTERNAL_ISSUER`。
- `w2_admission` 對非 `ISSUED` 一律 `NOT_ADMITTED`。
- `dev_driver.py` 移除 caller 設定 `WRITE_ROOT`／`ALLOWED_OPS`。
- `ops_receiver.py` 需外部 `--admission` 且 `grant_state=ISSUED`，否則 exit 2。
- 結果：DEV／OPS effect 皆 fail-closed；前輪 self-auth 證據保留於 `runs/w2_selfauth_prior/`，不作為 grant。

## UNKNOWN 四類

`PASS`；分類**只由 observed state**（pre/post/exit）推導，非 `kind`；補償以 saved preimage 還原。

## N09

`NOT_ADMITTED`（`first_fail=NOT_ADMITTED`）。已切斷與 Checker/Consumer 的循環：N09 只到 recovery，Checker 後驗，Consumer 再下游。

## Checker／Consumer

- Checker：**PASS／44 checks**。
- Consumer：**BLOCKED_NOT_ADMITTED**（`evidence_accepted=True`、`admitted=False`）。

## 判定

**`W2_NOT_ADMITTED`**。需外部 Owner／Issuer 對 exact operation（DEV `-05`／OPS `-06`）簽發 `grant_state=ISSUED` 後，才可重跑受保護效果並申請 W3。
