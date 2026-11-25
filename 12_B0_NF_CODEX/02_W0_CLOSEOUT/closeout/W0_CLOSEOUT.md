# FHS-5_PLP/W0｜B0-NF CLOSEOUT（CODEX-first）

**decision**：`W0-CODEX-FIRST-20261125-01`｜`W0-OPS-NATIVE-20261125-01`｜`B0-SAMPLE-CODEX-20261125-01`  
**subject**：`FHS-5_PLP/W0`｜**batch**：`FHS-5/W0/B0-NF`｜**date**：2026-11-25（Asia/Taipei）  
**verdict**：`B0_REPRESENTATIVE_PASS_WITH_NOT_COVERED`  
**W0 status**：`W0_PARTIAL_VALIDATED`（非 `W0_NF_VALIDATED`；完整 W1–W4 與全分母未跑）

## 1｜B0 五方代表能力

| 方 | 實作 | 實際結果 | 證據 |
|---|---|---|---|
| TPM＋Reviewer | 真實 `plp-tpm-review 1.0.1` `review_core.py` | `REVIEW_SOURCE_LOCATED_ONLY`；0 defects；5 unbound（authority/reader） | `evidence/review/` |
| Guide | `BUILD_MINIMAL` `guide_min.py` | `PACKAGE_FIRST`；5/5 pack files ok；9-key delta | `evidence/guide/thin_start.json` |
| Bridge | `REUSE` 既有 `w1_bridge_reference.py` | selftest 22/22；inspect/explain/render/compare | `evidence/bridge/` |
| Challenge | `BUILD_MINIMAL` checker，獨立 worktree | PASS；19 checks；0 findings；五 pin | `evidence/challenge/challenge.json` |
| FAR | `BUILD_MINIMAL` `far_min.py` | 2 alternatives；10 advice；chosen ALT-1 | `evidence/far/far.json` |

## 2｜CODEX Native DEV/OPS

| 項 | 結果 | 證據 |
|---|---|---|
| Sample | briefcheck 自主選定；G4 無本地實體/權利 | `evidence/frozen_oracle.json` |
| Red v1 | 10 tests；2 failures（R3 duplicate A、R7 ambiguous B） | `evidence/tests/red_v1.txt` |
| Patch `12'` | seen[A]/seen[B] fail-closed | `evidence/tests/patch_12prime.diff` |
| Green v2 | 10 tests OK（1 skipped：junction 權限） | `evidence/tests/green_v2.txt` |
| OPS | O1–O6；POS exit 0、NEG exit 2、output/readback/restore、Provider OFF imports `NONE` | `evidence/ops/ops.json` |
| Consumer | `consumed=true`；checker PASS | `evidence/consumer/consumer_receipt.json` |

## 3｜Pins

```text
source    fc46088355071109d6dc4051da4db25d3246000515ea1f254be14d78121d294c
candidate 5eab43de2d3f67d6afbb1c5f6bc390e2c391da36
evidence  ef977e0855e7d3dc633aaa5d2b0a78976a3ee530667596f5b8f031dbf262c6d5
oracle    3cc26ed8e74a150e4c354fa9596d706e1e30552a217d940ba14c17c2f5bd12e1
case_set  93c7f91c6d78288d052ec701798c98dbf2717b3ceef6d486751e95105ca90f7c
```

## 4｜NotCovered

- HERMES／GPT CHAT／GPT WORK 的實際 Host 執行與相容性測試。
- 完整 U26／CG-SEM17／QA26／C16／EC-36／local47／38＋28／FARP30 分母。
- W1–W4 全波施工與驗收。
- Publisher/Release 與外部 OS/Repo/Host grant。
- junction 建立受 Windows 權限限制，該子例 `SKIPPED`；absolute/`..`/UNC 已實測拒。

## 5｜Why not W0_NF_VALIDATED

B0 已證明五方代表能力、red→patch→retest、OPS、OFF、獨立 checker、consumer。但 W0 的完整必要 FUO/Case 與產品全分母尚未全部實跑，故只能 `W0_PARTIAL_VALIDATED`。下一波 W1 以本 B0 的 pack/candidate/evidence pins 為基線，不從零重建。
