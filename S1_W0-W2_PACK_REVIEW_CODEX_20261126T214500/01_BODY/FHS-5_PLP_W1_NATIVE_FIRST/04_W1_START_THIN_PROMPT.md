# 04_W1_START_THIN_PROMPT｜W1 S1 受影主用包（START THIN PROMPT）

**S1 pack**：`W1-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1-r2`  
**supersedes**：`FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1` / `W1-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W1/CONTROL_PACK/2026-11-25-nf-r2` / `W1-NF-r2-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`｜固定 commit `9fae9257a3402928efbe6ff0cd66f45761f52846`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 主用包的冷啟入口（document primary）；本輪已依 Owner 預授權升格，只導向 `05`／`00`–`03` 與真前件，不重抄全規範。原義與未受影條款見 00–03；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## 1｜讀取順序

1. `05_W1_SOURCE_MANIFEST.json`（5 MD SHA、10 現行 sources；原 42 源保留於 upstream 原 05、26 assets、14 HOLD、digest contract）。
2. `00_W1_PI_PD.md` S1 節＋§0–§13（6 WP、12 ACC、D01–D09、七 Seam、Host 21 格）。
3. `01_W1_DEV_ECP.md`（38 DEV）與 `02_W1_OPS_ECP.md`（29 OPS）。
4. `03_W1_TQAEP.md`（13 案、N01–04/N10/N11、Guide 16、Bridge 17／38＋28）。
5. `02_EVIDENCE/W1_S1_證據附件.md`（DOC 實跑、mutation、未閉項）。

## 2｜不可刪的 SPEC

- 六檔直讀：本候選 05 `schema=FHS5.PLP.W1.SourceManifest.S1@1`（原版為 `NF@1`）；舊 15 檔只在 legacy schema，標 `projection_of_sha256`。
- TPM/Reviewer 四契約同 work identity；Reviewer 唯讀、不改 subject。
- Guide 兩模式／四函式／九鍵雙期；缺期／單 SHA／caller bool → `DELTA_UNVERIFIED`。
- Bridge 四 API＋BodyResolver；path/reparse/duplicate/UTF-8/size 全拒；unknown 不靜默丟。
- 第二個非 briefcheck 包必須真復用同 ABI。
- Host 七階段逐階分證；CODEX／GPT CHAT／GPT WORK／HERMES 不互抵；HERMES 三 child 分列。
- W2 接收：真 relocation、pins/seal、缺/空/重複 raw、path/reparse、假授權、零 call/write＋正控。

## 3｜授權與前件

| 動作 | 前件 |
|---|---|
| P01/P02 READ／crosswalk | 授權來源＋真 bytes/SHA；不需產品 install |
| P03 DEV | Owner 授權、可 chdir 的隔離 worktree、exact write-set、preimage、recovery |
| P04 Host invoke/serve | 真 host entry、principal、policy、receiver；`Selected`≠`Loaded`≠`Consumed` |
| P05 13 案 | Case Owner freeze；真 fixture/oracle/runner |
| P06 Checker/Consumer | 分立 session；fresh readback |

`ECP`／`Advice`／`permit=true`／exit 0 皆非 Grant 或 PASS。

## 4｜執行（P01→P06）

1. **P01 Identity/Reuse**：H0/六檔/六冊/W1M/alias/version/rights/14 HOLD；選兩個不同包。
2. **P02 ABI**：舊 15→6 逐欄 source/target/type/required/transform/loss/readback；unknown 保留或拒。
3. **P03 Reader/TPM/Guide/Bridge**：真 entry/version；BodyResolver；四契約；四函式／九鍵。
4. **P04 Host/Consumer**：真 invoke/served/consumed；第二包；其他 Host 分帳。
5. **P05 Assurance**：13 案＋子例；POS 合取、NEG 真拒、OFF 正控。
6. **P06 Seal/Handoff**：同 candidate distinct Checker；fresh W2 readback；受影 changeset。

## 5｜Harness Loop

`LastGood → 實作 → 檢測 → FirstFail/ChangeCone → 最小修補 → 受影重驗 → ACCEPT / STOP_SCOPED`

- 同 failure key 最多兩次實質修補；無新料不重派。
- 不改 oracle、不刪分母、不用 13 案核銷 67 ECP。
- P04 最終 Consumed 是 `POST_EVIDENCE`，不倒卡 P03。

## 6｜Done／Stop／Resume

**Done（文件）**：六檔＋05＋seal 可重建；原 ID/分母/14 HOLD 可 join；冷讀可定位 P01–P06。
**Done（產品）**：13 案＋子例真 raw、獨立 Checker、fresh Consumer、第二包；本輪未跑，`W1_NF_VALIDATED=NOT_RUN`。

**Stop**：錯 root/HEAD/preimage、假 grant、越 write-set、Host 不可服務、缺 oracle、Checker 不獨立。
**Resume**：`last_good_ref + first_fail + exact next op + required input`；缺件只停受影 slice。
