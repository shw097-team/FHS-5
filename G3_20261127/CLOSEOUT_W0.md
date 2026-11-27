# W0 CLOSEOUT（W0 closeout delta，2026-11-27）

- 控制包：`W0-G3-PCNF-r2`／`PCNF-W0W2-ADOPT-20261127-01`
- 分支：`codex/w0-w2-g3-native-20261127`
- content commit：`f173214428f1d3b4ea3819182ddb8a6a67cc34f1`
- docs/evidence commit：`dda7779464abf3b6d7cbaeee8a9fbcc93c471137`
- push readback（2026-11-27）：`git push origin HEAD:refs/heads/codex/w0-w2-g3-native-20261127` 回 `unable to get password from user`；`git ls-remote` 仍為 `0099e95373be712e542a058693fdefba31c863c7`。本輪為**本地合規交付**，未繞過憑證、未 force、未改 main/W2_CURRENT。
- 最終 run root：`C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\g3-20261127\G3_20261127\runs\w0_close_20261127\13`
- 最終 handoff：`09_DELIVERY/W0_HANDOFF.md`（sha256 `9f9ae2340212ec5b3171dcf26a9fa85db34aa2da79452bc0d86a389685d17613`）
- 最終 evidence：`10_EVIDENCE/EVIDENCE_MANIFEST.json`（sha256 `5307b70ce521e90fcbea79cbccf5cc2bfad3228f59a2a5fce1aa6228cbf8e7da`）
- 最終 consumer：run `20261127T230849-a4b187dd`，811 checks，`consumed=true`，receipt sha256 `2be63f0da8e97961c067920664aa3df217bd366654bcb16ef280ed824ef327b8`

## 真結果：`W0_DONE`（scoped）

適用範圍：local CODEX／Windows、FHS-5 W0 B0-NF Generic、44 案（24 Original＋10 NF＋10 SAMPLE）、原 14 WP／10 FUO／A-B-C 的當期適用義務。**不是** W1–W4 完成、不是整體 FHS-5 MVP、不是 release、不是不同 principal、不是其他 Host／FHS 485／Fabric Legacy 全量。

| 項 | 結果 |
|---|---|
| 44 案 | **44 PASS／0 FAIL／0 pending**（40 同位復用＋4 受影重跑） |
| NF-T01 | **PASS**：fixed `off_legacy.py` exit 0；double-fail 不再 `ok=True`；reviewer positive＋negative gate 皆成立；三種 forced failure 皆 exit 3／FAIL |
| NF-T08 | **PASS**：byte-exact 凍結四契約（pi `43ea6ea2…`、pd `01de8c30…`、dev_ecp `72e37bf9…`、ops_ecp `241538cd…`）→ Guide `--contracts` 真消費；chain **COMBINED_OK 23/23**；negatives **9/9** 各自 expected code；同入口 live NEG 真拒 |
| NF-T10 | **PASS**：staging consumer `20261127T225645-015592e8`（810 checks）供 finalize；final consumer `20261127T230849-a4b187dd`（811 checks）44/44 接受 |
| G17 | **PASS**：同一 final consumer entry；合法 receipt POS `RECEIPT_SHA_OK`；單 byte mutation exit 3 `RECEIPT_SHA_MISMATCH`；marker 未寫；audit `zero_outside_read=true`、`process_or_network_events=[]` |
| 獨立 Checker | `03_PARTIES/challenge/challenge.json` **PASS 32 checks／0 findings**；pins candidate `bb66a276…`、oracle `112f2902…`、source `fc460883…`、case_set `9624e71d…` |
| fresh W1 minimal | 44 items、`readback_ok=true`；wrong pin／wrong scope／partial handoff 全 typed 拒；checklist `w1_out_pos/w1_checklist.json` sha256 `49bd3a83…` |
| 血緣 | pack `e3772aee…`；candidate `bb66a276…`；preimage `5eab43de…`；oracle `112f2902…`；W0M `c9b1ca9b…` |

## 三案與共同受影

### NF-T01

- 真缺陷：`reviewer_double_fail_negative` 在 ON/OFF 雙方 expectation 皆 false 時仍 `ok=True`；reviewer 固定舊 plugin path；reviewer/bridge 缺件時整段跳過仍可 PASS。
- 最小修：動態解析實存 `plp-tpm-review/<ver>/scripts/review_core.py`（不安裝/升級）；double-fail 改為必經 negative control，與 positive 綁定；結構守衛禁止 `on_expected/off_expected/same_semantics` 不成立仍 `ok=True`；缺件即 `bound=false`＋FAIL。
- 實跑：`off_legacy.py` exit 0，gates 全 true；import blocker blocked/allowed 正控成立；reviewer negative `REVIEW_FAIL_CLOSED / OUTPUT_ROOT_NOT_FOUND`；`blocked_attempts=[]`。
- 強制失敗：reviewer cache 不存在、reviewer positive fail、genuine double-fail（`case_ok.md`→malformed 後還原）皆 exit 3／FAIL。
- raw／證據：`runs/w0_close_20261127/agents/t01/EVIDENCE/`（`off_legacy.fixed.json`、`run.meta.json`、`forced_fail.json`、`forced_positive_fail.json`、`forced_double_fail.json`、`raw/fixed/`）。
- Ceiling：隔離為 `PYTHONPATH`＋`sitecustomize` import blocker，不是 OS sandbox/ACL；child/network 未追蹤，列 NotCovered；reviewer 自報 `authority_state=UNBOUND`、`original_acceptance=NOT_ASSERTED`。

### NF-T08

- 直接根因：G3 `runs/w0_full/13` 的四契約是 LF／舊生成物（pi 1330 B），與 Guide/tpm_gate 記錄的 CRLF byte-exact 契約（pi 1477 B, `43ea…`）不符；oracle 亦被重生為 `31dc…`，與 frozen `112f…` 不符。不是四契約語義缺陷。
- 處置：fresh `runs/w0_close_20261127/13` 以 byte-exact 來源＋bundle clone `bb66a276…`；恢復凍結四契約（**不重生**，保留 pre-patch 時間語義）；Guide `--contracts` 實傳；Guide Resume／Bridge／Native／Challenge/FAR/patch/retest 皆以同位置材料驗證。
- 實跑：`pins == 四實檔 SHA`、`source_manifest_match=true`、`requirement_ids` 4（SAMPLE-R1..R4，與 `pi.children` 對位）；chain 23 checks 全 true；negatives 9/9 各自 typed code。
- 同入口 live NEG：只改 `pi.json` 1 byte；原 Guide 不自我拒絕、只記錄被改 pin；chain 的 `TPM-GUIDE-CONTRACT-CONSUMED` 真拒 `CONTRACT_CONTEXT_MISSING`，FAR/retest 零效果。
- 收緊：新增 `TPM-CONTRACTS-FROZEN`，反向核對 `tpm_gate.contracts` 與四實檔；避免只比 Guide pins 的自我一致漂移。
- raw／證據：`runs/w0_close_20261127/agents/t08/EVIDENCE/`（`README.md`、`commands.json`、`chain.fixed.json`、`negatives.fixed.json`、`thin_start.fixed.json`、`live_neg.json`）＋最終 `13/03_PARTIES/collab/`。
- Ceiling：chain 是 pin／欄位消費驗證，不是契約內容簽章；若契約目錄＋Guide＋tpm_gate 全被同步重寫，仍需外部 canonical pin 錨。列 finding，不當 PASS 替代。

### NF-T10／G17

- CP-D08 順序：其他 required set／Checker 具備後，先 staging consumer（`--allow-pending-t10`）`20261127T225645-015592e8`（810 checks）→ 以該 receipt finalize NF-T10（`consumer_run_id` 同此，checks 810）→ 重建 evidence/handoff → final consumer `20261127T230849-a4b187dd`（811 checks，44/44）正式接受。
- `finalize_t10.py` 不再默讀舊 `negatives.positive.run_id`；支援 explicit receipt/run／LATEST＋receipt SHA gate；stale handoff/evidence/negatives 皆 `STALE_*` 零寫入。
- G17 同入口：`consumer.py --verify-receipt` 先算 bytes SHA；POS `RECEIPT_SHA_OK`＋marker；NEG 單 byte exit 3 `RECEIPT_SHA_MISMATCH`、`receipt_parsed=false`、marker 不存在；audit 只開 receipt/consumer.py，zero outside read／zero process/network。
- fresh W1：`w1_min_consume.py` 在獨立 clone／process 真讀 handoff/pack/seal/W0M/repo/oracle/evidence/summary/44 receipts/raw，產出 44 項 checklist 並 readback；wrong pin `PIN_MISMATCH_ORACLE`、wrong scope `SCOPE_MISMATCH`、partial `HANDOFF_INCOMPLETE` 皆 exit 3、zero output。
- raw／證據：`13/07_CONSUMER/G17/`、`13/07_CONSUMER/W1_MIN_CONSUME/`、`13/07_CONSUMER/runs/20261127T230849-a4b187dd/`、`13/07_CONSUMER/CONSUMER_MANIFEST.json`。

## 同位復用與受影

| 類 | 案 | 處置 |
|---|---|---|
| 受影重跑 | NF-T01、NF-T07、NF-T08、NF-T10 | byte-exact source＋materialized `bb66a276…`；新 run/receipt/raw |
| 同位復用 | 其餘 40 案（含 NF-T05） | 原 candidate/pack/oracle/receipt/raw 不變；`off_bridge.json` 與舊樹 byte-identical |
| 未重跑 | 原 44 全量、W1–W4、FHS 485、Fabric/Legacy 全量 | 依原 scope／適用性保留，不以局部 PASS 外推 |

原 14 WP、10 FUO、A/B/C、DEV/OPS/TQAEP 必要證據沿用同位 raw；A（READ/DRAFT）成立，B 為 local scoped DEV/OPS 既有證據，C 的 Profile/HOLD 保留。原 44 分母、ID、kind、expected 未改。

## 實際變更（Actual ChangeSet）

| 路徑 | 變更 | 理由 |
|---|---|---|
| `13_W0_NF_CODEX_20261125/tools/off_legacy.py` | 修 | double-fail 不再 PASS；reviewer 動態解析；缺件 FAIL；強制失敗控制 |
| `13_W0_NF_CODEX_20261125/tools/collab_chain.py` | 修 | 新增 `TPM-CONTRACTS-FROZEN` 反向核對 |
| `13_W0_NF_CODEX_20261125/tools/consumer.py` | 修 | 新增 `--verify-receipt` G17/T10 共用 gate；LATEST 記 receipt/handoff/evidence SHA |
| `13_W0_NF_CODEX_20261125/tools/finalize_t10.py` | 修 | current receipt／run／LATEST＋SHA gate；拒 stale |
| `13_W0_NF_CODEX_20261125/tools/w1_min_consume.py` | 新 | fresh W1 minimal consume／checklist readback／typed 拒 |
| `13_W0_NF_CODEX_20261125/tools/record_affected.py` | 新 | 只重錄受影 case，合併 44 summary；不重跑全量 |
| `13_W0_NF_CODEX_20261125/openspec/changes/w0-close-20261127/` | 新 | 既有 OpenSpec flow 的最小 W0 delta（proposal/spec/design/tasks） |
| `13_W0_NF_CODEX_20261125/05_TQAEP/{summary.json,receipts/,oracle.json}` | 更新受影 | 40 復用＋4 新 receipt；summary 44/44；oracle 不重生 |
| `13_W0_NF_CODEX_20261125/09_DELIVERY/W0_HANDOFF.md` | 更新 | evidence pin、actual readback、readiness、publication 狀態 |
| `13_W0_NF_CODEX_20261125/10_EVIDENCE/EVIDENCE_MANIFEST.json` | 重建 | 702 files／44 receipts；sha `5307b70c…` |
| `13_W0_NF_CODEX_20261125/07_CONSUMER/` | 新 run／G17／W1 | staging/final receipts、negatives、G17、W1 consume |

## LastGood／rebuild／recovery

- LastGood：candidate `bb66a276…`（preimage `5eab43de…`）、pack `e3772aee…`、oracle `112f2902…`、frozen contracts `43ea/01de/72e3/2415`。
- Rebuild：copy byte-exact `13_W0_NF_CODEX_20261125` → `G3_20261127/runs/w0_close_20261127/13`；`git clone 02_CANDIDATE/repo.bundle`＋checkout `bb66a276…`；`guide --contracts` → `guide_resume` → `bridge_run` → `native_context` → `collab_chain` → `record_affected --case NF-T01/07/08` → consumer staging/negatives/finalize → `challenge --mode full` → final consumer → G17/W1。
- Recovery：不改 sealed pack/oracle/expected；失敗只回原 candidate/preimage 與凍結 artifacts；不 force push、不改 main/W2_CURRENT。

## 日後待升級區（非封存、非 PASS）

| 原 ID／路徑 | 原意 | 當期原因 | 替代／保留 | 恢復條件 |
|---|---|---|---|---|
| 舊 `off_legacy.py` 固定 `plp-tpm-review/1.0.1` 路徑 | 真 OFF reviewer 入口 | 已改動態解析，舊硬編碼不再使用 | 動態 locator；舊 bytes 在 Git 歷史 | 需要固定版本重現時 |
| `G3_20261127/runs/w0_full/13` 的 LF 契約／重生 oracle | 舊 41/44 run | byte drift，不作當期證據 | 保留歷史；使用 `w0_close_20261127/13` | 歷史追溯／對照 |
| `runs/w0_full/delivery` 子集 | 舊交付證據 | 缺 01_PACK/09_DELIVERY/02_CANDIDATE，不能作 consumer root | 保留；新 run root 才是可消費根 | 需要重建完整交付時 |
| 契約外部 canonical pin／自我一致 mutation | 防 coherent rewrite | chain 已核 tpm_gate，但全鏈同步重寫仍需外部錨 | 列 finding／claim ceiling | 未來 trust-root 設計 |
| OS 級 child/network 隔離 | OFF 全效果觀測 | 目前只 Python import blocker | 維持 NotCovered | 需要 Native/OS sandbox 能力 |
| 不同 principal、其他 Host、FHS 485、W4 Publisher | 原 Profile／波次 | 非當期 W0 Generic 必要 | 原帳保留 | 原波次／授權 |
| 舊 803-check consumer 專用承載 | W0→W1 接受 | 保留並擴充 receipt gate，未退役 | 現行 consumer | 完整相容性研究 |

## 未閉合／claim ceiling

- 原 14 HOLD／12 R3-CR／WM2E 未全數關閉；只處置直接受影者，其餘依原表保留。
- 不宣 W1–W4 完成、Checkpoint A 全部完成、W2/W3 准入、FHS-5 整體 MVP、release、不同 principal、其他 Host、FHS 485、Fabric/Legacy 全量。
- NF-T01 child/network 未觀測；NF-T08 契約內容簽章／全鏈 synchronous rewrite 未解；NF-T10 只宣 W1 minimal consume，不宣 W1 產品執行。
- push 未回讀前不宣成功。

## OpenSpec／子代理／PC10

- OpenSpec：既有 `13_W0_NF_CODEX_20261125/openspec` root 新增 `w0-close-20261127`，`openspec validate --strict` 有效；未重 init、未建第二流程。
- 子代理：T01（NF-T01）、T08（NF-T08）、T10（Consumer/G17/T10）各自專屬 scratch；Maker／Checker／Consumer 分責；不同 principal 未宣。
- PC10：NF-T01 一次實質修補（double-fail/locator）、NF-T08 一次（byte-exact 契約＋反向核對）、NF-T10 一次（current receipt＋gate/W1）；未重設 failure budget。

## 下一步（W1 最小）

1. 讀 `07_CONSUMER/W1_MIN_CONSUME/w1_out_pos/w1_checklist.json`（44 items）與 `09_DELIVERY/W0_HANDOFF.md`。
2. 以 W0 pins 為基線 requalify 原 14 HOLD／R3-CR；先做來源與 W1M 差額，不重跑 W0。
3. W1 產品施工另需上位採納、W1M／下一包一致與真入口／授權；不得把本 W0 DONE 當 W1 完成。