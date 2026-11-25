# W1 UPSTREAM CHANGESET（本輪實際差額，不冒充全系統採納）

**run_id**：`20261125T222954`｜**scope**：`W1-NF-01`

## 1｜execution-scope amendments（本輪 worktree 內實作並明示）

| ID | 原條文 | 實際差額 | 落點 |
|---|---|---|---|
| `A1` | 05 `sources` 以 `LOCAL_VERIFIED` 記錄，reader 缺席即硬停 `SOURCE_MISSING` | 缺席改記 `LOCAL_MISSING_RECORDED` 並保留 recorded sha；present 但 bytes 不同仍硬停 | `W1/impl/nf_reader.py::_verify_sources` |
| `A2` | 00 §12 15→6 只給表格 | 逐欄 crosswalk＋LossLedger＋`unknown_drop=0` 可機器驗 | `W1/impl/nf_reader.py::_crosswalk` |
| `A3` | 00 §4 digest 分域為文字 | `digest_domains` 實作；`context_sha256` 明示由 render 產生 | `W1/impl/nf_reader.py::_digest_domains` |
| `A4` | 01 §完整 Clause/Parent/Child/NEG/Exception | `parse_clauses` 產生層級、NEG token、Exception 標記 | `W1/impl/body_resolver.py` |
| `A5` | 02 §1 記載 worktree `FHS-5_W1_NF_r2` | 本輪改於 R 內新 worktree `C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3`；歷史目錄不改 | 本檔 §3 |

## 2｜需回寫的 MASTER／PROG／PROJ／WM／W2M 條文（候選，未採納）

1. `MASTER` W1 狀態列：追加 `W1_PARTIAL_VALIDATED (run 20261125T222954)`。
2. `PROG-00` §Seams：SM05 註明 reader 對缺席來源採 recorded-missing，不視為 Gate。
3. `W2M` §接收：新增 `W1-CODEX-05` 第二包 profile capability 差異驗收。
4. `WM` W1M §12.3：把「16/16 reader tests」更新為 63 tests／20 列測例。

以上皆為候選文字，不改上游檔；採納需新一輪 Owner 裁決。

## 3｜RepoContext 實際值

- 來源根（唯讀）：見 05 `sources.source_root`
- 本輪工作根：`C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3`
- 分支：`codex/w1-nf-r3-20261125`｜HEAD：`a539b1c3dab89b4fd62d3cc537191cd6ce2ad74e`
- base：`c2d8084ba24dd8df3fa62259bba496f4fb9caa85`（main，未 force、未改歷史）
