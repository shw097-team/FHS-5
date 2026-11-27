# W2 HANDOFF

- 已驗：12/12 案；DEV-01 真 MODIFY＋ADD、8 tests、reverse、restore；OPS-01 真 effect／七觀測／compensation；Checker 40 PASS；Consumer ACCEPT。
- raw：`runs/w2/raw/`；candidate 成員見 `evidence/FIVE_PINS.json`。
- 授權：DEV `-05`、OPS `-06`（本輪 isolated roots）；舊決策 revoked。
- 未驗：其他 Host、Publisher／Release、原域 DEV ECP、W3 effect。
- 下一合法 action：以 `evidence/W3_CONSUMER.json` 作最小 W3 消費；W3 exact grant 取得後才可執行 W3 effect。
- 不得：把 `W2_SCOPED_VALIDATED` 當 `RELEASE`；把舊 grant 帶入 W3。
