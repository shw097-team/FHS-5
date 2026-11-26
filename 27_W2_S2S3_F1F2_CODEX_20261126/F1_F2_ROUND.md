# F1／F2 本輪結果（S2/S3 續工）

## F1 正式入口收斂（已完成）
- `W1/check/w2_admission.py`、`W1/check/w2_dev_gate.py` 已改為 generation-2 正式入口；run-local 版本不再是被引用路徑。
- 特性：撤權以 decision_id 可攜判斷（fresh clone 無 marker 亦拒）；絕對 expiry；拒 caller 覆寫 root/scope/issuer/expiry；exact op set；lexical 與 resolved 分離、逐層 reparse 檢查；READ 決策永遠到不了 writer（`WRITE_NOT_AUTHORISED`）；patch 結構化解析（a/b 同路徑、拒 rename/copy/mode/null）；recovery 必填且同義；post readback 與 write-set 外污染偵測。
- 限制（如實）：gen-1 對 `effect=REPOSITORY_READ` 的 apply 實際以 `FALSE_AUTHORITY` 拒絕，**本輪未重現該項 RED**；本輪為加固與收斂，不是修復已重現漏洞。`GATE_PROBE_GEN1/GEN2` 均 GREEN。

## F2 W0／W1 最小再資格化（部分完成）
- 修正歷史 Downloads 絕對 pack root：新增 `W1/check/packloc.py`（env → repo-relative 18_/17_/16_），7 個測試與 `off_isolation.DEFAULT_PACK_ROOT` 改用它。
- 效果：`W1/check` 全套 pytest 由基線 **19 failed／25 errors／48 passed** → **0 failed／0 errors／106 passed**（15 subtests）。
- 新增 `test_w2_gate.py`（11 案）覆蓋 READ 不可寫、patch 結構、recovery、信任覆寫、假 receipt、subset write-set、正控 apply+reverse。

## 未完成（不得冒結案）
- F3 W2 真 OPS（O01–O06）、OPS-A 未跑：需另取 OPS host effect 具名 scope（target/root/principal/epoch/expiry/recovery）。
- F4 原 12 案／N01–N12／J2 九鍵／J3 真 ON/OFF 未核銷。
- F5 同候選 Checker／Fresh Consumer／五 pin 外 seal／W3 真接收未完成。
- W0 未重跑；W1 67 ECP 未逐項重核。

## 判定
- W0 validated：**NOT_CLAIMED（本輪未重驗）**
- W1 validated：**PARTIAL**（可攜性與 suite 真綠；67 ECP 原義未逐項核銷）
- W2 validated／`W2_NF_VALIDATED`：**false**（OPS／12 案／J3 未跑）
- W3 technical／execution readiness：**NOT_ASSESSED**
