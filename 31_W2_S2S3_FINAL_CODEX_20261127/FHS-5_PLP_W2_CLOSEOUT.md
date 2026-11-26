# FHS-5_PLP W2 CLOSEOUT（真源契約對位）

## 1. W2-REQ-BODY 假阻斷已消除（真原據）
前輪以 `U-\d{3}` 對比 `denominators.requirements=16`，屬分母類型錯置。
真 16 列為 `W2-B01..B13` ＋ `W2-NF-A/B/C`，來源：

- 當期 `S1_PACKS/FHS-5_PLP_W2_NATIVE_FIRST/00_W2_PI_PD.md` §4.1（12 欄完整表）
- 原 NF-r3 manifest（commit `35d5387`，raw sha `81daac8f…`，含 `dag`／`dev_ops_locators`／`subcases`）

實作：新增 `W1/impl/req_parse.py`，`s1_reader` 解析 16 列（id／original／fields／type／owner／native／applicable_op／producer／consumer／required_when／expected_receipt／actual_ref／first_fail／resume），缺失或重複即 `REQUIREMENT_TABLE_INCOMPLETE`。

Crosswalk：`A_CROSSWALK.json` — 原 manifest sha 相符、16/16 id 對位、DAG/locators/subcases 均在（B04/B05 owner 僅全形／半形差異）。

## 2. 正式 ABI 驗收（非 inspector）
- `build_contracts(S1 W2)`：`ok=true`、`problems=[]`、六視圖齊備、requirements=16、cases=12
- CLI：`python w2_nf_reader.py --pack … --out …` → `{"ok": true, "problems": []}`、**exit 0**
- 另外修兩處真契約錯配：ENTRY 章節依 S1 04 實際六章（SOURCE/SPEC/EXECUTE/HARNESS LOOP/DONE/STOP，大小寫不敏感）；`permission_state` 由 manifest 自身 `authority.actual_grant` 文字推導（`NONE_GRANTED`），並保留來源

## 3. 原案（12 案分帳）
PASS 7（OPS-02、EFFECT-01、AUTH-01、RUNNER-01、DELTA-01、R3-01、R3-02、R3-03 其中 7 項本輪真跑）｜REUSE_PASS 1（OPS-01）｜REUSE_PASS_FIXTURE 2（DEV-01/02）｜REUSE_NOT_RERUN 1（R3-04）

## 4. J／N
J1 PASS（118 entries 真接收＋T01..08）｜J2 PASS（7/7）｜J3 `ON_OFF_BOTH_SEMANTIC_SUCCESS`
N：PASS 7、PARTIAL 4（N01/N04/N06/N09）、DEFER 1（N08）

## 5. 判定
`W2_NF_VALIDATED` = **false**（仍缺：Host served/consumed 真觀測 N04、UNKNOWN 全分類 N06、端到端 slice N09、Source→TPM 真包 N01）

## 6. 真阻斷
- N01/N04/N06/N09 需真 Host session／多 op／timeout-before fixture
- 12 案中 DEV-01/02、OPS-01、R3-04 為歷史同位復用，未重跑
