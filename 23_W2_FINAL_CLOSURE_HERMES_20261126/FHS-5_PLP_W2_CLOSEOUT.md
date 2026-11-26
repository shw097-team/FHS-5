# FHS-5_PLP_W2_CLOSEOUT (final closure r3)

**任務**：`HERMES-F5-W2-FINAL-CLOSURE-r3`｜**subject／scope**：`FHS-5_PLP/W2/CONTROL_PACK`／`W2-NF-01`
**candidate**：`W2-NF-r3-CODEX-PRIMARY`｜**基線**：`bde47312646d` → 本輪 tree
**run root**：`W2_NATIVE_RUNS/20261126T1225_W2_FINAL_CLOSURE/`｜**時間**：2026-11-26T12:28:45+0800

## STATUS

| 判定 | 值 | 依據 |
|---|---|---|
| `W2_EXECUTION_READY` | **成立** | 本輪 op 皆在真前件下准入並產生效果 |
| `W2_NF_VALIDATED` | **成立** | 12/12 原案 PASS＋J1 7/7、J2、**J3 PASS 15/15**、UNKNOWN 4/4、M1-A 5/5 |
| `W3_TECHNICALLY_READY` | 見 §M3（W3 receive receipt 另行封存後宣告） | 五 pin 可分離凍結 |
| `INDEPENDENT_PASS` | `NOT_CLAIMED` | 同 principal、不同 session |
| `RELEASED`／`M-DONE` | `NOT_CLAIMED` | 無 Publisher 原域收據 |

## M1｜真安全入口＋正式 W2 E2E

**M1-A 共用安全入口**（新增 `W1/check/w2_admission.py`）

前輪 gate 信任 caller 自報的 `{decision_id, expired}`。本輪改為由 hash-pinned Owner 決策推導 receipt，並在使用時重新推導：

| case | 觀測 |
|---|---|
| A1 caller dict（嚴格模式） | `FALSE_AUTHORITY` |
| A2 由 pinned 決策推導的 receipt | 接受 |
| A3 receipt 被改 `decision_id` | `FALSE_AUTHORITY` |
| A4 錯 pin | `FALSE_AUTHORITY` |
| A5 決策未授權的 domain | `FALSE_AUTHORITY` |

**5/5 PASS**。決策文件 pin `1ef19c0f…`（`W2-NF-PRIMARY-20261126-01`）。

**M1-B 正式契約驅動**：`w2_nf_reader.build_contracts` 對正式 NF@2 包輸出 6 views，`requirements 16`、`cases 12`、`CR 37`、`HOLD 14+6`；OPS-O03 的 `w2_pack_ok=true`。

**M1-C J3 真 ON/OFF**（同一任務、同一凍結輸入、同一 oracle）

| 檢查 | 結果 |
|---|---|
| 兩側都產出 projection | 是 |
| ON 真用產品堆疊 | `imported: w2_receiver` |
| OFF 零產品 import | 0 |
| OFF import blocker 正控 | `BLOCKED` |
| 兩側皆真成功 | 是 |
| 交付樹未被寫 | 是 |
| 雙方都產生效果 | 是 |
| 穩定投影 7 鍵全同 | 是 |
| 雙失敗不得 PASS | 成立 |

**15/15 PASS**。「效果檔案數」不列入比較鍵：兩側各自產生不同 byproduct，語義claim是「有無效果」，故比較 `effect_created` boolean 並保留原計數於紀錄。

## M2｜原案核銷、Guide 雙期、凍結

**12 原案全部 PASS**（`W2_CASE_LEDGER.json`）：DEV-01/02、OPS-01/02、EFFECT-01、AUTH-01、RUNNER-01、DELTA-01、R3-01..04。
- 10 案由本輪 `run_w2_cases.py` 在真 scratch repo 執行
- OPS-01 由 O04 `VERIFIED`＋O05 `RECOVERED`＋candidate 未受影
- DELTA-01 由 Guide 雙期（`NEW_MATERIAL_EVIDENCE`，`policy_epoch` 兩期皆 null 記為 unknown 非 same）

**Guide 九鍵雙期**：相同 `subject/scope/source_sha/host_id`；不同 `repo_head/policy_epoch/oracle_sha/world_raw_sha/first_fail`。

**五 pin 分離凍結**（`W2_FIVE_PINS.json`）：source＝源集 digest；candidate＝受驗產品集合（4 檔 sha＋可重建 commit），不是單一 receiver SHA；oracle＝W2 TQAEP 凍結集，不是 J1 pins；case_set＝12 原案；evidence＝封存於結果之後。

**ChangeSet**：53 列（committed＋uncommitted），每列 exact kind/path/before/after。

## M3｜Checker、歷史 bytes、W3 接收

**M3-A 歷史 bytes 修復**：`21_W2_PRODUCT_HERMES_20261126` 以 `git checkout bde4731 -- <dir>` 逐檔還原歷史 blob bytes，**14/14 與 `bde4731` blob 完全相同**（不重寫歷史、不整目錄 renormalize）。`maker_tests.txt` 現為歷史 blob 的 916 B；作者本地 934 B（CRLF）版本之差額具名保留，不以新 hash 掩蓋。

**M3-B 同候選 Checker**：本輪對最終候選重跑獨立 oracle **21/21 PASS**，硬化探測 `HARDENING_PASS`（traversal `PATH_ESCAPE`、junction `PATH_ESCAPE`）。

**M3-C W3 接收**：見發布後 `W3_RECEIVE_RECEIPT.json`（本輪重新產生，不沿用前一輪 15/15）。

## 未關閉（具名）

| 項 | 狀態 | Owner／Resume |
|---|---|---|
| `14 HOLD＋6 專項` | 全部 RETAINED | 各自原域收據 |
| `37 CR` | RETAINED | 原負責人 |
| `policy_epoch` | `NOT_DECLARED_BY_HOST` | Host 宣告 |
| Kanban／Swarm／delegate_task | `NOT_OBSERVED` | 本輪仍單 session＋CODEX writer |
| OpenSpec W2 change | `NOT_CREATED` | 未 apply/archive |
| `maker_tests.txt` 934 vs 916 | 具名歷史差額 | 原 bytes 已還原，兩值皆記錄 |

## 原始證據

`W2_NATIVE_RUNS/20261126T1225_W2_FINAL_CLOSURE/`：`00_PREFLIGHT`、`30_VERIFY/raw`、`40_OPS/j3`（ON/OFF 隔離根）、`50_EVIDENCE`、`60_CLOSEOUT`。
