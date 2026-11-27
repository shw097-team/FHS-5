# W2 HANDOFF

- 真狀態：9 PASS＋3 NOT_ADMITTED；N09 NOT_ADMITTED；UNKNOWN 4/4。
- 授權：`AUTHORITY_REQUEST` DEV `-05`／OPS `-06`（REQUEST_ONLY）。
- 下一合法 action：Owner／Issuer 對 exact target/prestate/recovery 簽發 `ISSUED`，再重跑 DEV-01／DEV-02／OPS-01，重算 N09 與 Checker。
- 不得：以 prompt、runner 或本地檔案自簽 grant。
