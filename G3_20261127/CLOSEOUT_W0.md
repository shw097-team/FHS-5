# W0 CLOSEOUT（G17 真消費入口與最終結案，2026-11-28）

- 控制包：`W0-G3-PCNF-r2`／`PCNF-W0W2-ADOPT-20261127-01`
- 分支：`codex/w0-w2-g3-native-20261127`
- T1 content：`f173214428f1d3b4ea3819182ddb8a6a67cc34f1`
- T1 docs/evidence：`dda7779464abf3b6d7cbaeee8a9fbcc93c471137`
- T1 metadata：`5496cf55bc04b8409359f882952bd872f1ddbb88`
- T2 content：`c421c5a7856e397b37170f5401b9f7fe973b74fa`
- T2 docs/evidence：`fad50e1f3500107c8847e874dcb23ae4ec7a7a59`
- T2c metadata：`f60c15e58ac73e0c825172be08066b7290bbe261`
- T3 content：`a8c37de6796e875dd82b0a55ae19303cd02ed5f2`
- T3 docs/evidence：本檔所在 commit（以 `git log -- G3_20261127/CLOSEOUT_W0.md` 回讀）
- 最終 run root：`C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\g3-20261127\G3_20261127\runs\w0_close_20261127\13`
- 最終 handoff：`09_DELIVERY/W0_HANDOFF.md`（sha256 `20b82d765425f9761437b14f562cc507d4d5ebb0456568d708351177d14e69c5`）
- 最終 evidence：`10_EVIDENCE/EVIDENCE_MANIFEST.json`（sha256 `12ddc3c3f9b6805d1c9657e2e110a5ef87231bd6b78c090b1d94c6ad3fc0e26a`）
- 最終 consumer P8：run `20261128T000245-5dc3792c`，**863 checks**，`consumed=true`，receipt sha256 `1b4bbcc96df5ecde55dcf5c8337b493fbf5fff13b09e053d83ab021dd2e2a63c`
- 最終 W1 consume：`w1_out_pos/`，44 items、readback true；checklist sha256 `96e66d6fd7901007cbdd8d7855a49a498a5bcf9e0fd58fb28f2c92242ab1d318`；consume receipt sha256 `cc872413ef62dde438efdc382994af83645693099d9986b53902a287e6d7166a`
- G17 full suite：**PASS**（`g17_full/G17_SUMMARY.json`）

## 真結果：`W0_DONE`（scoped）

適用範圍：local CODEX／Windows、FHS-5 W0 B0-NF Generic、44 案（24 Original＋10 NF＋10 SAMPLE）、原 14 WP／10 FUO／A-B-C 的當期適用義務。**不是** W1–W4 完成、不是整體 FHS-5 MVP、不是 release、不是不同 principal、不是其他 Host／FHS 485／Fabric Legacy 全量。

| 項 | 結果 |
|---|---|
| 44 案 | **44 PASS／0 FAIL／0 pending**（40 同位復用＋4 受影重跑：NF-T01/07/08/10） |
| G17 | **PASS**：同一完整 W1 Consumer 入口；POS 真 receipt parse/use/checklist/readback；單 byte NEG `RECEIPT_SHA_MISMATCH`；outside locator `RECEIPT_LOCATOR_OUTSIDE`；audit `outside_opened=false` |
| NF-T01 | **PASS**：double-fail 拒絕、reviewer gate、CPython audit loader/open/child/os.system/loopback/ctypes；OFF legacy `0`、network `0`、native `0`、child `2`（僅 guide→git 唯讀） |
| NF-T08 | **PASS**：frozen four contracts `43ea/01de/72e3/2415`、Guide `--contracts`、chain **23/23**、NEG **9/9**、live one-byte NEG `CONTRACT_CONTEXT_MISSING` |
| NF-T10 | **PASS**：staging `20261127T225645-015592e8`（810 checks）→ finalize → P8 `20261128T000245-5dc3792c`（863 checks）44/44 |
| Checker | **PASS 32 checks／0 findings** |
| 同位核銷 | 40/40 reused receipts byte-identical；`0/40` 與 stale `w0_full/13` 相同；NF-T05 `31f0694c…` byte-identical |
| W1 | 44 items、readback；wrong pin／scope／partial 仍 typed 拒；`raw_refs` 10 個 SAMPLE 為空但 `receipt`＋`receipt_sha256` locator 有效 |

## G17 真消費入口（本輪）

- BUG-1：`consumer.py --verify-receipt` 是 standalone 支路，POS `receipt_parsed=false`、`downstream_effect=marker_only`，不是完整產品入口。
- BUG-2：`w1_min_consume.py` 的 LATEST receipt locator 只計算 `is_file()` 後就 `load_json`，confinement 未成為拒絕條件。
- 修補：
  - `w1_min_consume.py` 主路新增：handoff pins → `07_CONSUMER` locator confinement → trusted expected（explicit pin 或 `CONSUMER_MANIFEST`）→ receipt bytes SHA → 同一份 verified bytes parse → receipt handoff/evidence/consumed/validation → 44-item checklist/readback。
  - `finalize_t10.py` 的 receipt locator 同樣先 confinement，再 `is_file`/load。
  - `consumer.py --verify-receipt` 保留為元件測試，不再作為 G17 唯一實證。
- POS（P8 receipt `1b4bbcc…`，expected 同值）：exit `0`；`receipt_parsed=true`、`receipt_consumed=true`；checklist 44 items、readback true；checklist `96e66d6f…`；consume receipt `cc872413…`。
- NEG 單 byte（consumer_root 內同一 receipt 複本，offset 半長 XOR 1，expected 不變）：exit `3` `RECEIPT_SHA_MISMATCH`；`output_written=false`、無 checklist。
- NEG outside locator：exit `3` `RECEIPT_LOCATOR_OUTSIDE`；audit `outside_opened=false`、`outside_open_count=0`；無 checklist。
- 證據：`g17_full/g17_pos.json`、`g17_neg_byte.json`、`g17_neg_locator.json`、`G17_SUMMARY.json`、`audit_locator.py`。

## 三案與既有成果

### NF-T01（T2）

- 真缺陷：double-fail 仍 `ok=True`；reviewer 固定舊 path；缺件跳過。
- 修：動態 reviewer locator；double-fail negative control 與 positive 綁定；缺件 FAIL；CPython audit observer＋probe。
- 證據：`04_DEV_OPS/off_legacy.json`、`04_DEV_OPS/raw/audit/*.jsonl`、`agents/t2/EVIDENCE/`。
- Ceiling：OS sandbox／ACL／mount、native 孫程序、`-S/-E/-I`／scrubbed env、native library kernel egress 未覆蓋；audit 只觀測不阻止。

### NF-T08

- 舊 `w0_full/13` 四契約為 LF／舊生成物（pi 1330 B），與 byte-exact CRLF（pi 1477 B、`43ea…`）不符；oracle 亦為 `31dc…`。不是契約語義缺陷。
- 恢復 frozen contracts（不重生、不改 oracle）；Guide `--contracts`；chain 23/23；NEG 9/9；`TPM-CONTRACTS-FROZEN` 反向核對；live one-byte NEG `CONTRACT_CONTEXT_MISSING`。
- Ceiling：chain 是 pin／欄位消費驗證，不是契約內容簽章；全鏈同步重寫仍需外部 canonical anchor。

### NF-T10／W1

- CP-D08：staging 810 checks → finalize NF-T10（staging receipt `6690425f…`）→ P8 863 checks 44/44。
- `finalize_t10.py` 支援 explicit receipt／run／LATEST＋SHA gate；stale 皆 `STALE_*` 零寫入；本輪另補 locator confinement。
- W1 minimal：`w1_min_consume.py` 獨立 clone／process 真讀 handoff/pack/seal/W0M/repo/oracle/evidence/summary/44 receipts/raw；44 items、readback；wrong pin／scope／partial 真拒。
- 10 個 SAMPLE item 的 `raw_refs` 為空，但 `receipt`＋`receipt_sha256` 已提供有效 receipt locator；不另造 raw。

## T3 核銷與文件修正

- 40 案：40/40 receipt byte-identical；0/40 與 `w0_full/13` 相同；artifact/raw 全同；NF-T05 byte-identical。
- NF-T08：frozen contracts／tpm_gate／Guide pins／source_manifest_match／4 IDs／chain 23/23／NEG 9/9／live NEG 全成立。
- NF-T10/G17/W1：staging receipt 與 NF-T10 綁定值一致；P8 另立、無循環；G17/W1 成立。
- 文件：OpenSpec 41→40、NF-T05 reused；handoff G17 路徑 `07_CONSUMER/G17`；INDEX 表頭／checkpoint／evidence 754 檔對齊；UPSTREAM_CHANGESET 已追加 delta；新增 `validate_w0_close_20261127.log`。
- Canonical 內層 `13/09_DELIVERY/W0_CLOSEOUT.md` 是歷史交付；本 `G3_20261127/CLOSEOUT_W0.md` 才是當期正式 C/H。

## 同位復用與受影

| 類 | 案 | 處置 |
|---|---|---|
| 受影重跑 | NF-T01、NF-T07、NF-T08、NF-T10 | byte-exact source＋materialized `bb66a276…`；新 run/receipt/raw |
| 同位復用 | 其餘 40 案（含 NF-T05） | 原 candidate/pack/oracle/receipt/raw 不變 |
| 未重跑 | 原 44 全量、W1–W4、FHS 485、Fabric/Legacy 全量 | 依原 scope／適用性保留 |

原 14 WP、10 FUO、A/B/C、DEV/OPS/TQAEP 必要證據沿用同位 raw；A（READ/DRAFT）成立，B 為 local scoped DEV/OPS 既有證據，C 的 Profile/HOLD 保留。原 44 分母、ID、kind、expected 未改。

## Actual ChangeSet（本輪）

| 路徑 | 變更 | 理由 |
|---|---|---|
| `tools/w1_min_consume.py` | 修 | receipt locator confinement／trusted expected／bytes SHA／parse 接入真正主路 |
| `tools/finalize_t10.py` | 修 | receipt locator 先 confinement 再讀 |
| `tools/consumer.py` | 保留 | `--verify-receipt` 作元件測試；G17 不再以其為唯一實證 |
| `05_TQAEP`／`10_EVIDENCE` | 更新 | P8 受影 consumer、evidence `12ddc3c…` |
| `07_CONSUMER` | 新增 P8 run | `20261128T000245-5dc3792c`、g17_neg receipt |
| `w1_out_pos/` | 更新 | 44-item checklist `96e66d6f…`、consume receipt `cc872413…` |
| `g17_full/` | 新增 | POS／NEG byte／NEG locator／audit／summary |
| `G3_20261127/{CLOSEOUT_W0,HANDOFF_W0,INDEX,CHECKPOINT_AB,RUN_RECORD}` | 更新 | 正式交付與 G17 結案 |
| `G3_CURRENT.json` | 更新 | W0 DONE、P8/G17 pins、push readback |

## LastGood／rebuild／recovery

- LastGood：candidate `bb66a276…`、preimage `5eab43de…`、pack `e3772aee…`、oracle `112f2902…`、frozen contracts `43ea/01de/72e3/2415`。
- Rebuild：copy 13 → run root；clone bundle＋checkout；Guide `--contracts` → Resume → Bridge → Native → chain → record_affected → consumer staging/negatives/finalize → evidence → final consumer P8 → G17 full → W1 consume。
- Recovery：不改 sealed pack/oracle/expected；不 force push、不改 main/W2_CURRENT。

## 日後待升級區（非封存、非 PASS）

| 原 ID／路徑 | 原意 | 當期原因 | 替代／保留 | 恢復條件 |
|---|---|---|---|---|
| OS sandbox／ACL／mount | OFF 全效果觀測 | 目前 CPython audit | NotCovered | Native/OS sandbox 能力 |
| native 孫程序／kernel egress | 全 child/network 觀測 | 目前 Python audit 邊界 | NotCovered | OS/ETW 能力 |
| 契約外部 canonical anchor | 防 coherent rewrite | chain 已核 tpm_gate，全鏈同步重寫仍需外部錨 | claim ceiling | 未來 trust-root |
| 不同 principal、其他 Host、FHS 485、W4 Publisher | 原 Profile／波次 | 非當期 W0 Generic 必要 | 原帳保留 | 原波次／授權 |
| 原 14 HOLD／12 R3-CR／WM2E | 原帳 | 只處置直接受影 | 保留 | 原波次 |
| 舊 `w0_full/13`／舊 delivery 子集 | 舊 41/44 run | stale bytes／不可作 consumer root | 歷史保留 | 歷史追溯 |

## Claim ceiling

- 不宣 W1–W4 完成、Checkpoint A 全部完成、W2/W3 准入、FHS-5 整體 MVP、release、不同 principal、其他 Host、FHS 485、Fabric/Legacy 全量。
- NF-T01 OS-level 隔離未成立；NF-T08 契約內容簽章／全鏈同步重寫未解；NF-T10 只宣 W1 minimal consume，不宣 W1 產品執行。
- G17 已接真 W1 Consumer 主路；standalone gate 僅元件測試。

## OpenSpec／子代理／PC10

- OpenSpec：`13_W0_NF_CODEX_20261125/openspec` 的 `w0-close-20261127` 更新；`openspec validate --strict` valid；未重 init。
- 子代理：T1 交付/憑證、T2 NF-T01 觀測、T3 核銷；Maker／Checker／Consumer 分責；不同 principal 未宣。
- PC10：G17 同一根因群（完整性未接入主路）一次有新材料的實質修補；未重設 budget。

## 下一步（W1 最小）

1. 讀 `w1_out_pos/w1_checklist.json`（44 items）與 `09_DELIVERY/W0_HANDOFF.md`。
2. 以本 pins 為基線 requalify 原 14 HOLD／R3-CR；不重跑 W0。
3. W1 產品施工另需上位採納、W1M／下一包一致與真入口／授權。