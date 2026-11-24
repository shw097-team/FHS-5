# FHS-5_PLP W1｜PRIMARY 後續修補附錄

- Repair ID：`W1-PRIMARY-REPAIR-20261124-02`
- Baseline selection：`W1-PRIMARY-SEL-20261124-01`
- Claim ceiling：`AUTHOR_DESIGN_ONLY`
- Status：`AUTHOR_PRIMARY_REPAIRED_WITH_NAMED_HOLDS`

本附錄只記錄 Human Owner 將修補候選升格為 primary 之後發現的**封裝漂移**。它不改來源、fixture、oracle、Case、分母、Oracle 門檻或 claim ceiling。

## 1. 發現

| ID | 級別 | 發現 | 根因 |
|---|---|---|---|
| F-13 | P2 | `05_PLANNED_TQAEP.md` §5 的可執行命令仍指向 `FHS-5_PLP_W1_REPAIRED_CANDIDATE` | primary relabel 只改 3 個檔，未同步 TQAEP 正文命令 |
| F-14 | P3 | `evidence/raw/*.json` 的 `pack` 欄仍指向 retired author root | raw 在升格前產生，升格後未重跑 |
| F-15 | P3 | `PRIMARY_MANIFEST.json.root` 仍指向 retired author root | primary metadata 未改成可搬移的相對根 |

## 2. 修補

1. 將 TQAEP 正文命令改為 `--pack-root FHS-5_PLP_W1_PRIMARY`，重算 TQAEP MD SHA，並更新 JSON 的 `projection_of_sha256`。
2. 在 primary 根重跑 `replay_hashes.py`、`run_cases.py`、`run_harness.py`，重建 `evidence/raw/case_rule_results.json`、`harness_results.json` 與 `host_probe.txt`。
3. 將 `PRIMARY_MANIFEST.root` 改為可搬移的相對標籤，重算 FileManifest、PrimaryManifest、索引、ZIP 與外置 seal。
4. 以 `POST_PROMOTION_REPAIR_RECEIPT.json` 保存 before／after SHA；不覆寫 `PRIMARY_SELECTION.json` 或 `PRIMARY_RECEIPT.json` 的歷史事實。

## 3. 不變項

- 16 個來源 bytes 不變。
- 13 個 fixture／oracle bytes 不變。
- 13 個 Case 的 clause、kind、first_fail、分母不變。
- 24 個 W0 disposition 不變。
- `claims` 四 bool 全 false；receipt 四欄 null。
- 14 個具名 HOLD 不變。
- 原 Reader／Issuer／Host／Runner／Checker／Publisher 仍 `UNBOUND`。

## 4. 重驗

修補後的命令、exit、stdout SHA 與結果在 `POST_PROMOTION_REPAIR_RECEIPT.json`、`DELIVERY_SEAL.json` 與 workspace 的 `11_W1_EXECUTION_20261124/` 可回取。

## 5. 邊界

本附錄是作者端封裝修補，不是原域 ExecutionAdmission、Native PASS、Independent PASS 或 Release。
