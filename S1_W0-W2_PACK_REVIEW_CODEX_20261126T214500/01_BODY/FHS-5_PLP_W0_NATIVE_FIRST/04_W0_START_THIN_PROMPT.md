# 04_W0_START_THIN_PROMPT｜W0 S1 受影主用包（START THIN PROMPT）

**S1 pack**：`W0-S1-r2-CODEX-PRIMARY`  
**artifact_id**：`FHS5-PLP/W0/PACK-S1-20261126-r2`  
**supersedes**：`FHS5-PLP/W0/PACK-S1-20261126-r1` / `W0-S1-r1-AUTHOR-CANDIDATE`（本輪檢修升格版）；其原上游 `FHS5-PLP/W0/PACK-NF-20261125-03` / `W0-NF-r3-CODEX-PRIMARY`（S1 scope 內由本包接替，原包保留）  
**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（依本輪 Owner 預授權；S1 文件主用，非產品驗收）  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`  
**author**：GPT WORK（原編）＋CODEX Native S1 review（本輪檢修）｜**date**：2026-11-26（Asia/Taipei）  
**source pin**：原 05 raw `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`｜固定 commit `ae05a74514d2c310f82bbf9bb1a2009078f11c87`  
**product state**：`NOT_RUN`（文件完成不等於產品驗收）

> 本檔是 S1 主用包的冷啟入口（document primary）；本輪已依 Owner 預授權升格，只導向 `05`／`00`–`03` 與真前件，不重抄全規範。原義與未受影條款見 00–03；S1 未明示者不變。文件主用與可施工性不等於產品驗收，也不發外部 DEV/OPS/Host/Release 權限。

## 1｜先讀什麼

1. 本包 `05_W0_SOURCE_MANIFEST.json`（來源、pack files、assets、unresolved）。
2. `00_W0_PI_PD.md` 的 S1 節＋§00–§11（14 WP、七 Seam、原 13 前件、44 分帳）。
3. `01_W0_DEV_ECP.md`（D1–D7、11 path write-set）與 `02_W0_OPS_ECP.md`（O1–O6）。
4. `03_W0_TQAEP.md`（24＋10＋10 分母、fixture/expected、五 pin）。
5. 需要時讀 `02_EVIDENCE/W0_S1_證據附件.md`；不要先跑命令再看 expected。

## 2｜授權邊界

| 動作 | 本輪 |
|---|---|
| READ 授權來源／Git blob | 允許 |
| DRAFT 隔離文件 | 允許（只寫本次授權 work/output root） |
| DEV（`samples/briefcheck`） | 需真 repo root/HEAD/ACL＋exact write-set＋preimage＋Owner scope |
| OPS（local O1–O6） | 需真 Host/principal/policy epoch/output root/recovery；歷史 host ref 不沿用 |
| USER／RELEASE／外部 Host | 不授權 |

ECP、Advice、`permit=true`、文件 SHA 皆非 Grant；任一 UNKNOWN 先 readback，不盲 effect。

## 3｜執行順序（S2 切片，非新 WP）

```text
R1 來源/成果復用 → R2 Native 正控（DEV 或 OPS）
      ├→ R3 OFF/import blocker/positive control
      └→ R5 Windows 安全反證
R2/R3 → R4 五方按需＋fresh consumer
```

- **R1**：讀原 13_ tools、B0 runner、44 receipts；同位可回讀即 REUSE，只列真差額。
- **R2**：先 D1 真 probe；再 exact write-set/preimage；patch→tests→post SHA→reverse；或 O1–O4 output/readback/restore。正控必須能檢出一次真 write/call。
- **R3**：cold fresh process；真 import/call blocker；ON/OFF 同任務、同凍結輸入；兩路皆成功才 parity；env flag 不算 OFF。
- **R4**：五方各自入口；direct 只證解耦，不抵產品 invoke/serve/consume；consumer fresh parse/readback。
- **R5**：`../`／absolute／UNC／junction／symlink／reparse／Unicode／EOL／size；outside canary 未讀；WSL 不代 Windows。

## 4｜唯一 Harness Loop

`LastGood/真來源 → 實作 → 檢測 → FirstFail/ChangeCone → 最小修補 → 受影重驗 → ACCEPT 或 STOP_SCOPED`

- 同 failure key 最多兩次有實質差額修補；暫態讀取最多一次有理由 retry。
- 無新料不重派；不改 oracle／降門檻／刪分母求綠。
- 缺件只停受影 slice；其他合法工作續做。

## 5｜Checkpoint／Stop／Resume

每個 op 保存：candidate SHA、preimage、argv/cwd/env、exit、stdout/stderr SHA、post SHA、recovery、owner、not_covered。中途停止時寫 `RESUME`：`last_good_ref + first_fail + exact next op + required input`。

| 缺口 | 停止 | Resume |
|---|---|---|
| repo root/HEAD/ACL | R2 DEV | 真 probe＋preimage |
| Host/principal/epoch | R2 OPS | 同 Host readback |
| fixture/oracle | 受影 case | Case Owner freeze |
| Checker/Consumer | independent claim | distinct receipt |
| 原域 Legacy ref | FHS profile | 原 typed ref／NotCovered |

## 6｜Done

- 文件：六檔可讀、05 strict、seal 對 05 raw bytes、原 ID／分母可 join。
- S2：受影切片有真 argv/exit/raw/pre-post/recovery；未跑保持 `NOT_RUN`。
- 不因 S1 文件完成而宣 `B0_PASS`／`W0_NF_VALIDATED`／`RELEASE`。
