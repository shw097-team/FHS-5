# FHS-5_PLP W2 CLOSEOUT（Oracle-driven）

候選：13 成員，canonical `f8b5e89d…`

## 正式 S1 入口（本輪真修補）
| 缺陷 | Actual RED | 修正後 |
|---|---|---|
| `w2_nf_reader` dispatch 用未定義 `source_root` | NameError | 改用 `root` |
| `s1_reader` 對 `external_seal`（字串）呼叫 `.get()` | AttributeError（未顯式給 path 時） | 字串/字典皆可，並 fallback `S1_PACKS/SEALS/` |
| W0 套用 W1 分母鍵 | DENOMINATOR_MISSING | W0 用 nf/sample/historical_receipts/wp |
| `build_contracts` 缺 `pack_manifest_sha256`/`manifest` | KeyError | S1Inspect@2 提供 ABI 欄位 |
| `nf_reader` 硬編 05_W1 名 | W0 PACK_INCOMPLETE_LOCAL | 依 wave 選 05 |

入口實跑：W0（cases 24, seal ok）、W1（dev38/ops29/cases13/assets26/holds14, tree 593314d5…）、W2（cases12/assets25, tree cc7d91a1…, contracts 六視圖）。

## 原案（本輪真跑 7 案，7/7 PASS）
RUNNER-01 `RUNNER_UNBOUND`、OPS-02 `RECOVERY_KIND_MISMATCH`（zero git op）、R3-01 13 列＋3 NF（POS）、R3-02 `NOT_ADMITTED`、R3-03 `WRITE_SET_UNBOUND`（zero write）、EFFECT-01 `EFFECT_UNBOUND`、AUTH-01（wrong domain＋forged receipt 皆拒）。

## 真 gap（不冒結案）
W2 S1 `denominators.requirements=16`，但六檔正文只有 4 個 `U-` 識別碼且無 requirement bodies → `requirement_material=IDENTIFIER_ONLY`。正式 W2 產品驗收仍需上游 16 條 requirement 實質材料。

## 判定
- W2 `W2_NF_VALIDATED` = **false**（requirement bodies 缺、N01–N12 未掃）
- W2 技術：PARTIAL（S1 入口、7 原案、OPS-A/J1–J3 成立）
- W3 technical／execution：NOT_ASSESSED
