# FHS-5_PLP W2 CLOSEOUT（K1–K3）

基線：9afbcb2e4839bceb3edc8aab0da99e3b0aa0d3c2｜候選：11 成員，canonical aggregate `f06b1be8…`

## 本輪真跑
| 項 | 實際 | Raw |
|---|---|---|
| S1 Schema/ABI | `s1_reader.inspect_s1` 讀 `SourceManifest.S1@1`：5 檔 bytes/sha/lines、26 assets、13 cases、denominators、digest domains；外部 seal 重算 pack tree（W1 `593314d5…`、W2 `cc7d91a1…`） | EVIDENCE/TESTS_K1_FINAL.stdout.txt |
| J2 九鍵雙期 | 7/7 判例 PASS；changed_keys = repo_head、world_raw_sha | EVIDENCE/J2_NINEKEYS.json |
| J3 ON/OFF | ON 13 列、OFF 13 列、cold-off blocked、正控 true → `ON_OFF_BOTH_SEMANTIC_SUCCESS` | EVIDENCE/J3_ONOFF.json |
| 回歸 | 111 passed／15 subtests | EVIDENCE/TESTS_K1_FINAL.stdout.txt |

## 原義核銷（CLOSURE_MATRIX.json）
PASS 6（OPS-01、EFFECT-01、RUNNER-01、DELTA-01、J1、J2）｜PASS_AT_FIXTURE_SCOPE 2（DEV-01/02）｜PARTIAL 3（OPS-02、AUTH-01、R3-03）｜NOT_VERIFIED 3（R3-01、R3-02、N 系列）｜REUSE 1（R3-04）｜J3 = ON_OFF_BOTH_SEMANTIC_SUCCESS

## 判定
`W2_NF_VALIDATED` = **false**：N01–N12 未成套、R3-01/02 未重驗、OPS-02/AUTH-01 僅部分覆蓋。

## NotCovered
N01–N12 成套實跑；R3-01 13+3 接線；R3-02 原域隔離；第二 OS principal 驗收。
