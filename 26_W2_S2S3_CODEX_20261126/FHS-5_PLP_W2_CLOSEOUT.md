# FHS-5_PLP_W2_CLOSEOUT（S2/S3 本輪）

本檔為本輪實際施工結果，不繼承任何未重跑的宣稱。

## 1. 本輪真實完成

| 項 | 實際結果 | 證據 |
|---|---|---|
| R0 來源／三包位元一致 | W0/W1/W2 manifest sha256 與 S1 採納記錄逐字相符 | `STAGE1.json` |
| R1 兩種 aggregate 重算 | historical `8b4b4068…`、canonical `b30e8a2d…` 由 3346076 真 blob bytes 復現 | `W2_FIVE_PINS` 前值 + 本輪重算 |
| R1 新候選重凍 | 六成員（五＋`test_j1_receiver.py`）雙 aggregate | `W2_CANDIDATE_S2S3.json` |
| R1 admission 分離 | generation-2：trust 檔在 write root 之外、caller 不得覆寫 root/scope/issuer/expiry | `40_TRUST/` + S1–S12 |
| R1 安全矩陣 | 19/19 PASS，全部拒絕 `wrote=[]`、world digest 前後相同 | `STAGE2.json` |
| R2/R3 DEV-A | gate `check`→`apply_patch`→pytest→post readback→`reverse`→世界還原 | `APPLY.json`、`REVERSE.json` |
| 真 RED→GREEN | 修補前 receiver 接受 unlisted entry 與 junction alias（真 RED）；修補後 `UNLISTED_ENTRY` / `PATH_ESCAPE` | `PROBE_PRE_PATCH.json`、`PROBE_POST_PATCH.json` |

## 2. 真 RED（修補前，同一 oracle、同一輸入）

- `unlisted_entry`: accepted=true（應拒）
- `reparse_alias`: 實際以 junction 建立，accepted=true（應拒）

原因：`verify_delivery` 只核對 manifest 列舉項，未檢查 delivery tree 內未列舉檔；`_confine` 只拒「解析後在 root 外」，root 內別名（junction）可通過。receiver 其後把 `delivery_root` 交給 seam wiring，故未列舉 bytes 會成為權威輸入。

## 3. 修補內容（DEV-A，僅二檔）

- `W1/check/w2_receiver.py`：新增 reparse point 拒絕（含父層）與 delivery tree 檔案集精確比對；envelope（manifest/seal/.sha256/consumer receipt）除外。
- `W1/check/test_j1_receiver.py`：新增 J1-T07（unlisted entry）與 J1-T08（junction alias），皆要求拒絕且 `product_calls` 為零。

## 4. 分帳（實際）

- ECP：本輪只覆蓋 W2 DEV-A（2 檔）與其 recovery；**其餘 W2 DEV/OPS ECP、12 原案、OPS-A 未執行，維持原帳**。
- W0：本輪未重跑，僅核 S1 採納位元；W0 產品 claim 不變。
- W1：以候選樹跑 `W1/check` pytest 全套；J1 receiver 6→8 案；J1 strict 7 案。原文 67 ECP / 13 案未重跑，維持原帳。
- 安全：generation-2 拒絕路徑 12 項（S1–S12）＋通過路徑 7 項（P1–P7）。

## 5. 未成立（不得冒結案）

- `W2_NF_VALIDATED` **未成立**：12 原案、OPS-A、J3 雙期未於本輪真跑。
- `W3_TECHNICALLY_READY` / `W3_EXECUTION_READY` 未宣。
- 舊 `W2-NF-PRIMARY-20261126-01` 仍為 terminated，未被本輪復活；新決策 `W2-S2S3-OWNER-20261126-02` 僅覆蓋 world 內二檔。
- 獨立 Checker：本輪以獨立程序／獨立 oracle 重開（非同 session 自驗），仍未達「不同 principal」。
