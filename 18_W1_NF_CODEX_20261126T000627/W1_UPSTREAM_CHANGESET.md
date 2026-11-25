# W1 UPSTREAM CHANGESET（NF-r4）

**run_id**：`20261126T003047`｜scope `W1-NF-01`

## 1｜本輪 execution-scope amendments

| ID | 差額 | 落點 |
|---|---|---|
| `A6` | TPM 由 W1 硬碼改為 profile registry；GENERIC 只要求最小欄位 | `tpm_contracts_nf.py` |
| `A7` | Guide 的 next/stop/resume 由凍結 04 段落推導，移除固定字串 | `guide_nf.py::_thin_nav` |
| `A8` | Bridge 新增 `field_fidelity`（source→transform→target→readback），`missing` 改實算 | `bridge_nf.py` |
| `A9` | Host served 以 invocation payload 提供（nested Codex 無 file-read），argv 與 sha 如實記錄 | `check/run_host_nf.py` |
| `A10` | Observation 分離 candidate/source/pack/oracle/case_set/evidence 六種身份 | `check/run_cases_nf.py` |

## 2｜回寫候選（未採納）

1. `W1M §12.3`：把 reader 測試數改為實測 79，並註明 closure matrix 為核銷主表。
2. `W2M §接收`：採用 `w2_receiver` 的 6 類拒收檢查作為最小驗收。
3. `PROG-00 §SM05`：記錄 host served 可為 invocation payload（非必為 file）。

## 3｜歷史分帳

- NF-r3 交付 `16_W1_NF_CODEX_20261125T222954` 保留，不覆寫。
- 本輪新增 `17_W1_NF_CODEX_20261126T003047`。
