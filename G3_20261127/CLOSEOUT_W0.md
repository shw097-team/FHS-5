# W0 CLOSEOUT（W0 final closeout delta，2026-11-27）

- 控制包：`W0-G3-PCNF-r2`／`PCNF-W0W2-ADOPT-20261127-01`
- 分支：`codex/w0-w2-g3-native-20261127`
- T1 content commit：`f173214428f1d3b4ea3819182ddb8a6a67cc34f1`
- T1 docs/evidence commit：`dda7779464abf3b6d7cbaeee8a9fbcc93c471137`
- T1 push metadata：`5496cf55bc04b8409359f882952bd872f1ddbb88`
- T2 content commit：`c421c5a7856e397b37170f5401b9f7fe973b74fa`
- T2 docs/evidence commit：`fad50e1f3500107c8847e874dcb23ae4ec7a7a59`
- T2 push readback：`5496cf5 → fad50e1`；remote head `fad50e1`。本 T2c metadata commit 只記錄 readback，不變更內容。
- 最終 run root：`C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\g3-20261127\G3_20261127\runs\w0_close_20261127\13`
- 最終 handoff：`09_DELIVERY/W0_HANDOFF.md`（sha256 `3e5d6104d6fccbe7d46a5484b26340247f13054358e9ab8dd81b27f5ae92673d`）
- 最終 evidence：`10_EVIDENCE/EVIDENCE_MANIFEST.json`（sha256 `0ebbccf1f09837629b3cb2960dd476c440937f77cc80d4e8ee3d8fdcd3a92527`）
- 最終 consumer P7：run `20261127T234153-ecdbff08`，**863 checks**，`consumed=true`，receipt sha256 `1400892233a1246abcf5aefdcba846bbb7bfa3084998a6284e555b9865fd7db2`

## 真結果：`W0_DONE`（scoped）

適用範圍：local CODEX／Windows、FHS-5 W0 B0-NF Generic、44 案（24 Original＋10 NF＋10 SAMPLE）、原 14 WP／10 FUO／A-B-C 的當期適用義務。**不是** W1–W4 完成、不是整體 FHS-5 MVP、不是 release、不是不同 principal、不是其他 Host／FHS 485／Fabric Legacy 全量。

| 項 | 結果 |
|---|---|
| 44 案 | **44 PASS／0 FAIL／0 pending**（40 同位復用＋4 受影重跑） |
| NF-T01 | **PASS**：double-fail 不再 PASS；reviewer positive／negative gate 成立；新增 CPython audit loader/open/child/os.system/loopback/ctypes 觀測；positive probe 全 true、absent-control 真拒；OFF `legacy_import_attempts=[]`、`child_events=2`（僅 guide→git 唯讀）、`network_events=0`、`native_events=0` |
| NF-T08 | **PASS**：frozen four contracts（`43ea6ea2…`／`01de8c30…`／`72e37bf9…`／`241538cd…`）→ Guide `--contracts`；chain **COMBINED_OK 23/23**；NEG **9/9**；live one-byte NEG `CONTRACT_CONTEXT_MISSING` |
| NF-T10 | **PASS**：staging `20261127T225645-015592e8`（810 checks）供 finalize；final P7 `20261127T234153-ecdbff08`（863 checks）44/44 接受 |
| G17 | **PASS**：同 final consumer entry；POS `RECEIPT_SHA_OK`；單 byte NEG exit 3 `RECEIPT_SHA_MISMATCH`；marker 未寫；audit `zero_outside_read=true`、`process_or_network_events=[]` |
| 獨立 Checker | **PASS 32 checks／0 findings** |
| fresh W1 minimal | 44 items、`readback_ok=true`；wrong pin／scope／partial 全 typed 拒 |
| 同位核銷 | 40/40 reused receipts **byte-identical**；`0/40` 與 stale `w0_full/13` 相同；NF-T05 `off_bridge.json` `31f0694c…` byte-identical |
| 血緣 | pack `e3772aee…`；candidate `bb66a276…`；preimage `5eab43de…`；oracle `112f2902…`；W0M `c9b1ca9b…` |

## 三案與 T2/T3

### NF-T01（T2 補證）

- 真缺陷：`reviewer_double_fail_negative` 在 ON/OFF 雙方 expectation 皆 false 時仍 `ok=True`；reviewer 固定舊 plugin path；缺件跳過仍可 PASS。
- 最小修：動態 reviewer locator；double-fail 改必經 negative control 並與 positive 綁定；缺件 `bound=false`＋FAIL；結構守衛禁止假 `ok`。
- T2 新觀測：`tools/off_audit_site/sitecustomize.py`＋`tools/off_audit_probe.py`；CPython `sys.addaudithook` 記錄 import/open/subprocess/os.system/socket/ctypes；positive probe 觸發 blocked legacy import、child、grandchild、os.system、loopback roundtrip、native dlopen，absent-control 為空且被拒。
- OFF 實跑：legacy import attempts `[]`；child events `2`（guide→`git rev-parse` 唯讀 helper）；network `0`；native `0`；產品 ON/OFF 語義仍成功。
- 強制失敗：reviewer cache 不存在、reviewer positive fail、genuine double-fail 皆 exit 3／FAIL。
- Raw／證據：`13/04_DEV_OPS/raw/audit/*.jsonl`、`04_DEV_OPS/off_legacy.json`、`agents/t2/EVIDENCE/`（若已落盤）。
- Ceiling：OS-level sandbox、native 孫程序、`-S/-E/-I`／scrubbed env、native library 內部 kernel egress、audit 只觀測不阻止，均列 `not_covered`；不以 Python audit 冒充 OS 隔離。

### NF-T08

- 直接根因：舊 `w0_full/13` 的四契約是 LF／舊生成物（pi 1330 B），與 byte-exact CRLF 契約（pi 1477 B、`43ea…`）不符；oracle 亦被重生為 `31dc…`。不是四契約語義缺陷。
- 處置：fresh run root 恢復凍結四契約，**不重生**、不改 oracle；Guide `--contracts` 實傳；Guide Resume／Bridge／Native／Challenge/FAR/patch/retest 皆同位置驗證。
- 實跑：pins == 四實檔；`source_manifest_match=true`；requirement IDs 4（SAMPLE-R1..R4）；chain 23 checks；NEG 9/9 各自 expected code。
- 收緊：`TPM-CONTRACTS-FROZEN` 反向核對 `tpm_gate.contracts`；live NEG 只改 `pi.json` 1 byte，chain 真拒 `CONTRACT_CONTEXT_MISSING`，FAR/retest 零效果。
- Ceiling：chain 是 pin／欄位消費驗證，不是契約內容簽章；契約目錄＋Guide＋tpm_gate 全同步重寫仍需外部 canonical anchor。

### NF-T10／G17／W1

- CP-D08：staging `20261127T225645-015592e8`（810 checks）→ finalize NF-T10 → final P7 `20261127T234153-ecdbff08`（863 checks）44/44 接受。
- `finalize_t10.py` 不默讀舊 `negatives.positive.run_id`；current receipt／run／LATEST＋SHA gate；stale 皆 typed 拒、零寫入。
- G17 同入口：POS `RECEIPT_SHA_OK`＋marker；單 byte NEG exit 3 `RECEIPT_SHA_MISMATCH`、`receipt_parsed=false`、marker 不存在；audit zero outside read／zero process。
- fresh W1：`w1_min_consume.py` 獨立 clone／process 真讀 handoff/pack/seal/W0M/repo/oracle/evidence/summary/44 receipts/raw，產出 44 項 checklist 並 readback；wrong pin `PIN_MISMATCH_ORACLE`、wrong scope `SCOPE_MISMATCH`、partial `HANDOFF_INCOMPLETE` 皆 exit 3、zero output。
- Raw：`13/07_CONSUMER/G17/`、`13/07_CONSUMER/W1_MIN_CONSUME/`、`13/07_CONSUMER/runs/20261127T234153-ecdbff08/`、`CONSUMER_MANIFEST.json`。

## T3 核銷（唯讀）

- 40 案：40/40 receipt byte-identical 於 source 13；`0/40` 相同於 stale `w0_full/13`；artifact/raw 全同；NF-T05 byte-identical。
- NF-T08：frozen contracts、tpm_gate、Guide pins、source_manifest_match、4 IDs、chain 23/23、NEG 9/9、live NEG 全成立；frozen-control 亦 22/22。
- NF-T10/G17/W1：staging receipt SHA `6690425f…` 與 NF-T10 綁定值一致；final P7 另立、無循環；G17/W1 成立。
- Manifest/Checker/Git：T3 對 702 檔逐一重算全對（T2 後為 754 檔，新 manifest `0ebbccf1…`）；challenge 32/0；`W2_CURRENT` 與 candidate 產品 0 變動。
- T3 文件差額已修：OpenSpec 41→40、NF-T05 reused；handoff G17 路徑 `07_CONSUMER/G17`；evidence 檔數 754；INDEX 表頭與 checkpoint 對齊；UPSTREAM_CHANGESET 追加本輪 delta。

## 同位復用與受影

| 類 | 案 | 處置 |
|---|---|---|
| 受影重跑 | NF-T01、NF-T07、NF-T08、NF-T10 | byte-exact source＋materialized `bb66a276…`；新 run/receipt/raw |
| 同位復用 | 其餘 40 案（含 NF-T05） | 原 candidate/pack/oracle/receipt/raw 不變 |
| 未重跑 | 原 44 全量、W1–W4、FHS 485、Fabric/Legacy 全量 | 依原 scope／適用性保留 |

原 14 WP、10 FUO、A/B/C、DEV/OPS/TQAEP 必要證據沿用同位 raw；A（READ/DRAFT）成立，B 為 local scoped DEV/OPS 既有證據，C 的 Profile/HOLD 保留。原 44 分母、ID、kind、expected 未改。

## 實際變更（Actual ChangeSet）

| 路徑 | 變更 | 理由 |
|---|---|---|
| `tools/off_legacy.py` | 修 | double-fail 拒絕、reviewer 動態定位、缺件 FAIL、audit 整合 |
| `tools/off_audit_probe.py` | 新 | loader/child/os.system/loopback/ctypes positive probe |
| `tools/off_audit_site/sitecustomize.py` | 新 | CPython audit observer＋import blocker |
| `tools/off_audit_site` | 新 | observation site（隨 tools 進 manifest） |
| `tools/collab_chain.py` | 修 | `TPM-CONTRACTS-FROZEN` |
| `tools/consumer.py` | 修 | `--verify-receipt` G17/T10 gate |
| `tools/finalize_t10.py` | 修 | current receipt／run／LATEST＋SHA gate |
| `tools/w1_min_consume.py` | 新 | fresh W1 minimal consume |
| `tools/record_affected.py` | 新 | 只重錄受影 case |
| `openspec/changes/w0-close-20261127/` | 新/修 | 既有 OpenSpec flow 最小 W0 delta；41→40 修正 |
| `05_TQAEP/{summary.json,receipts/,oracle.json}` | 更新 | 40 復用＋4 新 receipt；summary 44/44 |
| `09_DELIVERY/W0_HANDOFF.md` | 更新 | evidence pin、actual readback、readiness、G17/754 檔 |
| `10_EVIDENCE/EVIDENCE_MANIFEST.json` | 重建 | 754 files／44 receipts；sha `0ebbccf1…` |
| `07_CONSUMER/` | 新 run／G17／W1 | P7 receipt 863 checks、G17、W1 |
| `G3_20261127/{CLOSEOUT_W0,HANDOFF_W0,INDEX,CHECKPOINT_AB,RUN_RECORD}.md/json` | 更新 | T4 正式交付 |

## LastGood／rebuild／recovery

- LastGood：candidate `bb66a276…`（preimage `5eab43de…`）、pack `e3772aee…`、oracle `112f2902…`、frozen contracts `43ea/01de/72e3/2415`。
- Rebuild：copy byte-exact 13 → run root；clone bundle＋checkout；Guide `--contracts` → Resume → Bridge → Native → chain → record_affected NF-T01/07/08 → consumer staging/negatives/finalize → evidence → final consumer → challenge → G17 → W1。
- Recovery：不改 sealed pack/oracle/expected；失敗只回原 candidate/preimage 與凍結 artifacts；不 force push、不改 main/W2_CURRENT。

## 日後待升級區（非封存、非 PASS）

| 原 ID／路徑 | 原意 | 當期原因 | 替代／保留 | 恢復條件 |
|---|---|---|---|---|
| 舊 `off_legacy.py` 固定 1.0.1 路徑 | 真 OFF reviewer | 已動態 locator | 舊 bytes 在 Git 歷史 | 固定版本重現 |
| `runs/w0_full/13` LF 契約／重生 oracle | 舊 41/44 run | byte drift，不作當期證據 | 保留歷史；新 run root 才是證據 | 歷史追溯 |
| `runs/w0_full/delivery` 子集 | 舊交付 | 缺 01_PACK/09_DELIVERY/02_CANDIDATE，不能作 consumer root | 保留；新 run root | 重建完整交付 |
| 契約外部 canonical anchor | 防 coherent rewrite | chain 已核 tpm_gate；全鏈同步重寫仍需外部錨 | 列 finding／claim ceiling | 未來 trust-root |
| OS 級 child/network 隔離 | OFF 全效果觀測 | 目前 CPython audit 觀測；非 OS sandbox | 列 NotCovered | Native/OS sandbox 能力 |
| 不同 principal、其他 Host、FHS 485、W4 Publisher | 原 Profile／波次 | 非當期 W0 Generic 必要 | 原帳保留 | 原波次／授權 |
| 舊 803-check consumer | W0→W1 接受 | 保留並擴充 receipt gate | 現行 consumer | 完整相容性研究 |

## 未閉合／claim ceiling

- 原 14 HOLD／12 R3-CR／WM2E 未全數關閉；只處置直接受影者，其餘依原表保留。
- 不宣 W1–W4 完成、Checkpoint A 全部完成、W2/W3 准入、FHS-5 整體 MVP、release、不同 principal、其他 Host、FHS 485、Fabric/Legacy 全量。
- NF-T01 OS-level child/network 隔離未成立；NF-T08 契約內容簽章／全鏈 synchronous rewrite 未解；NF-T10 只宣 W1 minimal consume，不宣 W1 產品執行。
- 遠端交付：T1 `0099e95 → 5496cf5`；T2 `5496cf5 → fad50e1`（content `c421c5a`＋docs `fad50e1`），remote head 回讀 `fad50e1`；T2c metadata commit 只記 readback。

## OpenSpec／子代理／PC10

- OpenSpec：既有 `13_W0_NF_CODEX_20261125/openspec` root 的 `w0-close-20261127` 更新；`openspec validate --strict` valid；未重 init。
- 子代理：T1（交付/憑證）、T2（NF-T01 觀測）、T3（核銷）各自 scratch；Maker／Checker／Consumer 分責；不同 principal 未宣。
- PC10：NF-T01、NF-T08、NF-T10 各一次有新材料的實質修補；未重設 failure budget。

## 下一步（W1 最小）

1. 讀 `07_CONSUMER/W1_MIN_CONSUME/w1_out_pos/w1_checklist.json`（44 items）與 `09_DELIVERY/W0_HANDOFF.md`。
2. 以 W0 pins 為基線 requalify 原 14 HOLD／R3-CR；先做來源與 W1M 差額，不重跑 W0。
3. W1 產品施工另需上位採納、W1M／下一包一致與真入口／授權。