# FHS-5_PLP W2 CLOSEOUT（C1–C3 本輪）

## 1. 本輪真跑（OPS-A 垂直）
| Op | 實際 | Raw |
|---|---|---|
| O01 Host/Receiver probe | principal `desktop-57eo414\user`、host `DESKTOP-57EO414`、python 3.11.9、git 2.53.0、policy epoch `NOT_DECLARED_BY_HOST` | EVIDENCE/OPS/O01_HOST_PROBE.json |
| O02 Exact target / preimage | target 事先不存在（pre_absent=true）、output root 存在、admission 由 authority 決策簽發 | O02_ADMISSION.json / O02_ADMISSION_RECEIPT.json |
| O03 真 effect | 以正式 `w2_receiver.receive()` 執行；exit 0；accepted=true；verified_entries=118；product_calls build_contracts=1、seam_wiring=1；產物 6 檔、digest `cb58f92d…` | O03_EFFECT.json / O03_RECEIPT.json |
| O04 獨立讀回 | 不同程序重讀：receipt、material parse、tree before==after、inventory 重算 → **VERIFIED**；封存副本與 live 相同 | O04_READBACK.json / O04_SEALED_COPY.json |
| O05 補償 | delete-created-only（逐檔 hash 比對）→ target 不存在、output root 回到 pre digest | O05_COMPENSATION.json / O05_POST_STATE.json |
| O06 UNKNOWN | timeout 於效果中斷：6 檔已落地、receipt 未寫 → 分類 **TO_AFTER**，先讀回再補償，未盲重試 | O06_PARTIAL.json / O06_COMPENSATION.json |

## 2. 正式驗收
- Frozen oracle：`OPS_ORACLE_FROZEN.json`（實跑後才寫 checker，未回填）
- 分立唯讀 Checker：**PASS**（`CHECKER_VERDICT.json`，16 checks 全過，同 principal／不同 process）
- Fresh Consumer：**ACCEPT**（`CONSUMER_READBACK.json`；實際 parse context_bundle 與 W2 inbound manifest，requirements=13）
- 消費者首次假設錯誤（期待 cases=16）之 REJECT raw 保留於 `CONSUMER_READBACK_v1_REJECT.json`；修正僅限 consumer 斷言，非產品

## 3. 原義分帳
- **已成立**：W2-OPS-01 的 O01–O06 垂直（真 effect／WorldRaw／recovery／UNKNOWN 分類）；J1 clean receive（118 檔真驗證＋真 consume）
- **復用**：DEV-A（上一輪 apply/test/reverse）、Receiver J1-T07/T08、兩 aggregate
- **未成立**：W2 原 12 案其餘 11 案、J2 九鍵兩期、J3 真 ON/OFF、N01–N12 全量、6 FUO/ACC 逐項
- **未動**：37 CR／14 HOLD 原帳保留

## 4. 判定
- `W2_NF_VALIDATED` = **false**（12 案／J2／J3 未完成）
- W2 產品：**PARTIAL**，OPS-A 垂直已真跑

## 5. NotCovered / Resume
- J3 真 ON/OFF 與 leak 正控
- J2 兩期九鍵與 ChangeSet verifier
- 12 案其餘項與 N 系列
- exact next op：`C2-J3-ONOFF`、`C2-J2-NINEKEYS`
