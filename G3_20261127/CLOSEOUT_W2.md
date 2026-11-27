# W2 CLOSEOUT（G3，2026-11-27）

- candidate：`W2-G3-PCNF-r2`；source manifest `7bdc4a0acb497944450d89a2c347d26ca4ac8593f6ee47ac229215a80ff227e0`
- pack tree `957013dd9d1152b5dd259c5d08a068b976ad2b3ef6251a9507128daf75a1bb0c`；case set `a78e689d42265851eba8ea0deb6f125eac4da591c47e49c2f89f610051a16aaf`
- raw：`G3_20261127/runs/w2/`

## 12 原案：**12/12 PASS**

DEV-01：base `9fae9257a3402928efbe6ff0cd66f45761f52846`、preimage `c666740268cce914819e2ba43a0dbd9413de709792ee2c8338b0b67e895c74f0`（9336 B）、MODIFY＋ADD、post `28bc674b564102b4…`、8 tests、reverse/restore、unlisted 不變。
OPS-01：pre `ABSENT`→receipt/material→consumer `all_ok`→`DELETE_CREATED_ONLY`→`ABSENT`；七觀測齊。
其餘 10 案（DEV-02／OPS-02／EFFECT／AUTH／RUNNER／DELTA／R3-01..04）皆有真 observed 與 token。

## UNKNOWN 四類（OPS-O06／W2-CODEX-04）

`runs/w2/raw/unknown/UNKNOWN_FOUR.json`：**PASS**；classes `{'to_before': 'TO_BEFORE', 'to_after': 'TO_AFTER', 'partial': 'PARTIAL', 'exit0_wrong': 'EXIT0_WRONG'}`。
每類為真 subprocess（timeout／partial／exit0）、WorldRaw pre/post、compensation 讀回。

## N09 端到端因果鏈

`runs/w2/raw/N09_CHAIN.json`：**PASS**；九階段
contracts→work_order→admission→dev_effect→ops_effect→readback→recovery→checker→consumer，
每階段有真實檔案與 SHA。`first_fail=None`。

## 授權

DEV `W2-G3-OWNER-20261127-05`、OPS `-06`（isolated roots）；舊 `-01..-04` revoked；`policy_epoch` 誠實記為 `NOT_DECLARED_BY_HOST`。

## Checker／Consumer

- 分離 Checker：**PASS／46 checks**（SEPARATE_PROCESS_SAME_PRINCIPAL）。
- fresh process Consumer：**ACCEPT**。

## 判定

**`W2_SCOPED_VALIDATED`**（本 candidate／本 CODEX local host）。
`W3_TECHNICAL_READY=true`；`W3_ADMITTED=false`（未取得 W3 exact grant，未執行 W3 effect）。

## 未閉項

其他 Host、Publisher／Release、原域 DEV ECP、W3 effect。
