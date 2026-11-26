# 04_W2_START_THIN_PROMPT｜W2 S1 受影主用包（START THIN PROMPT）

**S1 pack**：`W2-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W2/PACK-S1-20261126-r2`  
**supersedes**：`FHS5-PLP/W2/PACK-S1-20261126-r1` / `W2-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W2/PACK-NF-20261126-r3` / `W2-NF-r3-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `81daac8ff3f47566d18cc7ebdaee9625ff5ca000b71caac3226841b124f6099b`｜固定 commit `35d5387f9c98eaebc2d4cee742afcb4509a7d8c3`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 主用包的冷啟入口（document primary）；本輪已依 Owner 預授權升格，只導向 `05`／`00`–`03` 與真前件，不重抄全規範。原義與未受影條款見 00–03；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## 1｜SOURCE

1. `05_W2_SOURCE_MANIFEST.json`：5 MD SHA、10 現行 sources（原 24 源保留於 upstream）；25 assets、13+3、five pins、37 CR、14 HOLD。
2. `00_W2_PI_PD.md` S1 節＋§0–§10：三 SPEC、13+3、6 WP、DAG、J1–J3、權限。
3. `01_W2_DEV_ECP.md`（D01–D07）與 `02_W2_OPS_ECP.md`（O01–O06）。
4. `03_W2_TQAEP.md` §1–§3：12 原案、N01–N12、J1–J3。
5. `02_EVIDENCE/W2_S1_證據附件.md`：five pins 重算、DOC 實跑、未閉項。

## 2｜不可刪的 SPEC

- 12 原案 ID／kind 不改；POS 合取、NEG 真拒、exit 0 不算 PASS。
- 13+3 是逐 op 適用索引，不是 16 boolean gate；B10–B12 是 POST/RELEASE，不作 pre。
- 五 pin 分期：source／candidate／oracle／case-set／evidence；post-run seal 不回填 pre-freeze。
- 真 Gate/Admission/Receiver；`verify_delivery→consume_verified→receive` 必須 parsed/use/readback。
- DEV 用受權 Git patch/check/test/reverse；OPS 用 receiver/pre-post WorldRaw/compensation；`git revert` 不代 OPS。
- UNKNOWN 先 reconcile；不盲 retry。
- 舊 W2 撤權保持；不改 root/gate/token 繞過。

## 3｜授權（每 op 核，不 blanket）

| 域 | 必要前件 | 本輪 |
|---|---|---|
| READ/DRAFT | 授權來源／隔離根 | 可 |
| DEV | 真 root/HEAD/ACL、exact write-set、preimage、Owner scope、recovery | `UNBOUND` |
| OPS | 真 Host/principal/epoch/receiver/target/prestate/recovery | `UNBOUND` |
| W2 Writer | 新具名 protected scope（另取） | `BLOCKED_NOT_ADMITTED` |
| Release | Publisher/channel/ACL | 不授權 |

## 4｜EXECUTE（R0→R5）

**R0 實體與 pins**
- 以 Product `dada2354…` 為 LastGood、Delivery `3346076c…` 定位；建新 candidate 前先核 ancestry/tree。
- 五成員 raw bytes 重算（本輪已 MATCH）：`768d6318…`、`ecef3f39…`、`8caabfff…`、`738bfe15…`、`29674640…`；historical `8b4b4068…`、canonical `b30e8a2d…`。
- 不把 W3 替身當 W2；不把五 member aggregate 當全部 five pins。

**R1 Admission 去耦合（P01/P02/P03）**
- 拆「可信當期配置」與「operation request」；固定歷史 TRUST 不可由 caller 決定。
- 先跑安全 RED：錯 root/target/expiry/scope/issuer/principal、撤權、假 receipt、path escape、未知 effect、preimage mismatch、reparse drift。
- 每個拒絕：0 writer/receiver call、0 input/target mutation；正控能檢出一次真 call。

**R2 真 DEV-A**
- MODIFY `W1/check/w2_receiver.py`＋ADD `W1/check/test_j1_receiver.py`。
- `git apply --check` 只作預查；真 apply→tests→post SHA→reverse；unlisted 不變。

**R3 真 OPS-A／多 op／UNKNOWN**
- 真 Host/ACL/epoch/receiver；pre/post WorldRaw；host compensation；pre-state readback。
- timeout/partial/UNKNOWN → 隔離＋readback＋reconcile；worker 未結束不解除。

**R4/R5 12 案與正式驗收**
- 以 03 §1 frozen oracle 逐案；12 案 verdict 或 NotCovered。
- 同 candidate Checker；fresh W3 consumer 只讀交接；W3 不自簽 W2。

## 5｜Harness Loop

`LastGood → 實作 → 檢測 → FirstFail/ChangeCone → 最小修補 → 受影重驗 → ACCEPT / STOP_SCOPED`

- 同 failure key 最多兩次有新材料修補；暫態讀取最多一次 retry。
- 不改 expected/oracle；不用 read-only 12/12 抵真 effect；不把 marker smoke 當產品。
- 缺 protected scope 只停 effect，READ/DRAFT/TQAEP 可續。

## 6｜DONE

- 文件：六檔＋05＋seal；13+3 逐列 owner/resume；five pins 可回取。
- 產品（S3）：12 案＋J1–J3 適用語義、真 DEV/OPS、Recovery、同 candidate Checker、W3 fresh consume。
- 未達只可 `W2_PARTIAL`，不得寫 `W2_NF_VALIDATED=true`。

## 7｜STOP

無 W2 具名 scope、錯 root/preimage、假 grant、未知 effect、缺 Host/receiver、缺 oracle、撤權未解、Checker 不獨立、W3 要求自簽 W2。
