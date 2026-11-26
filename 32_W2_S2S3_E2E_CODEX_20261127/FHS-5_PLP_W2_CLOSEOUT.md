# FHS-5_PLP W2 CLOSEOUT（當期真產品貫穿）

## 1. 完整 S1 正式 ABI（實質，非 count）
| 視圖 | 真值 |
|---|---|
| PI | 16 列（B01–B13＋NF-A/B/C），欄位 original/fields/type/owner/applicable_op/producer/consumer/required_when/expected_receipt/actual_ref(None)/first_fail/resume |
| PD | 6 WP（WM2-P01..P06）、**42 條 typed DAG edges**、14 HOLD、CR 37 |
| DEV | 7 個 op（DEV-D01..D07，由 01 正文推導）、write-set 2 列 |
| OPS | 6 個 op（O01..O06，含 procedure/expected/readback/compensation/unknown 欄） |
| TQAEP | 12 案（每案 kind POS/NEG/EDGE、fixture／oracle ref、runner、requirement_refs）、18 個 J/N 子組 |
| ENTRY | 六章節（SOURCE/SPEC/EXECUTE/HARNESS LOOP/DONE/STOP） |

契約：`ok=true`、`problems=[]`；CLI `--pack` exit 0。

## 2. N01／N04／N06／N09
- **N01 PASS**：`tpm_contracts_nf.build_contracts` 對真 W2 S1 包，profile `S1-W2`，5 views；修補前真 `SCHEMA_UNSUPPORTED`（FirstFail）
- **N06 PASS 4/4**：真子程序 timeout 產生四類世界狀態 — TO-BEFORE（無檔）、PARTIAL（2/3 檔）、EXIT0-WRONG（三檔但 bytes 錯、exit 0）、TO-AFTER（三檔完整、無 response）
- **N09 PARTIAL**：source→reader→TPM→contracts 三段同 subject 真呼叫；operation 段仍來自 28_ 的 W1 NF 交付，非同一 source
- **N04 PARTIAL**：僅有 W1 歷史 host session；無當期 W2 served/consumed

## 3. 原 12 案
本輪真跑 7（OPS-02／EFFECT-01／AUTH-01／RUNNER-01／DELTA-01／R3-01／R3-02／R3-03 中 7 項）｜REUSE_PASS 1（OPS-01）｜REUSE_PASS_FIXTURE 2（DEV-01/02）｜REUSE_NOT_RERUN 1（R3-04）

## 4. 判定
- `W2_NF_VALIDATED` = **false**：N09 非單一 source 貫穿、N04 缺當期 Host session
- W2 technical **PARTIAL**｜W3 technical **PARTIAL**（五 pin＋Checker＋Consumer 成立）｜W3 execution **NOT_CLAIMED**

## 5. NotCovered
N04 當期 Host served/consumed；N09 單一 source 的 operation+receiver 段；W1 67 ECP 逐義。
