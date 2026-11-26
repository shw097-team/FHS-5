# FHS-5_PLP W2 Upstream Audit — W3 P01 Intake (Read-Only)

**Auditor role**: W2 upstream auditor (read-only) · **Date**: 2026-11-26 · **Subject**: `FHS-5_PLP/W2/CONTROL_PACK`, scope `W2-NF-01`
**Mode**: read-only. Nothing under `C:\Projects` was created, modified, moved, or deleted. Only this report was written.
**Evidence rule**: document statements are not evidence. Every digest below was recomputed in this session from bytes on disk or from git blobs at the named commit.

## 0. Bottom line

- The W2RequalificationMatrix is **not executable as a PASS matrix today**: 12/12 case definitions are carried, **0/12 are frozen**, 10/12 have an r3 verdict row with `raw: null`, and 2/12 (W2-OPS-01, W2-DELTA-01) have **no case row at all**.
- **No W2 verdict can be reused by W3.** The r3 ledger was produced at `660da33`, whose `w2_dev_gate.py` and `w2_admission.py` are byte-different from the frozen candidate.
- Oracle status `PARTIALLY_FROZEN` and case-set status `CARRIED_NOT_REFROZEN` are **true**, but the freeze is weaker than declared: 1 of 5 frozen locators is missing and 1 pins an obsolete receiver.
- Writer state `BLOCKED_NOT_ADMITTED` is **true** and currently enforced.

## 1. Locators actually read (and where the given locators did not resolve)

| Locator | Result |
|---|---|
| `...\20261126T1240_W2_SCOPED_REPAIR\20_DEV\worktree\W2_CURRENT.json` | read; sha256 `1532901743f1bdc3…` |
| `...\20261126T1240_W2_SCOPED_REPAIR\24_W2_SCOPED_REPAIR_HERMES_20261126\W2_FIVE_PINS.json` | **does not exist at run root**; real file is under `20_DEV\worktree\24_…\W2_FIVE_PINS.json` (sha256 `74321487db0f6a1c…`) |
| `...\25_W2_FINAL_HANDOFF_HERMES_20261126\FHS-5_PLP_W2_HANDOFF.md` | exists only under `20_DEV\worktree\`; sha256 `e2c759a9b608deda…` |
| `...\25_W2_FINAL_HANDOFF_HERMES_20261126\FHS-5_PLP_W2_CLOSEOUT.md` | exists only under `20_DEV\worktree\`; sha256 `6dfba0997862e22e…` |
| `...\W3_PACK_PRIMARY_CODEX_20261126T1449\01_BODY\FHS-5_PLP_W3_NATIVE_FIRST\00_W3_PI_PD.md` §04.4 (lines 446–482) | read |
| `...\20261126T1240_W2_SCOPED_REPAIR\30_VERIFY\raw\CHECKER_J1_ORACLE.json` (pinned by five pins) | **MISSING**; `30_VERIFY` contains only `expected_pins.json` and `tmp/` |

## 2. Product commit vs delivery commit (verified)

| Item | Value | Byte check |
|---|---|---|
| `main` | `c2d8084ba24dd8df3fa62259bba496f4fb9caa85` | does **not** contain the delivery (`merge-base --is-ancestor` = NO) |
| Product commit | `dada2354b7c25c8f4a316d9fae93827cef0d194e`, tree `9b20abed003f…` | "freeze the candidate"; 22 commits / 456 files vs main |
| Delivery commit | `3346076c69b00d65e48fdb9ddf894ac4cc09524b`, tree `2c4fdf05c755…` | parent = `dada235`; 23 commits / 461 files vs main |
| Published ref | `origin/hermes/w2-product-20261126` = `3346076` | delivery commit is published |
| Member blobs at `dada235` vs `3346076` | 5/5 **identical** | packaging-only delta confirmed |
| `W2_CURRENT` git blob | `54244c4df38b…` (git blob SHA, not sha256) | W3 §04.4 distinction is correct |

**Verified**: the distinction is real and load-bearing. `dada235` = product/candidate content; `3346076` = same content + pointer, superseded marker, closeout/handoff. Working-tree bytes at `3346076` match the commit blobs for every file audited.

## 3. Five candidate members, recomputed at `3346076` (and identical at `dada235`)

| Member | Pinned SHA-256 | Recomputed | Match |
|---|---|---|---|
| `W1/check/w2_receiver.py` | `768d63188612…` | `768d6318861215886860ae3a30c9c30bdaec8bdd4732c63ff95996e675522a59` | YES |
| `W1/check/w2_dev_gate.py` | `ecef3f39cf3a…` | `ecef3f39cf3ae4db1a387cca4eec2d5212d9cce8e1f81d7a91e0cb0ffd170db4` | YES |
| `W1/check/w2_admission.py` | `8caabfff…` | `8caabfffd5c5c07040f0444e1d4ad23cbad939501b61597b726184f4816c4ae3` | YES |
| `W1/impl/w2_nf_reader.py` | `738bfe15…` | `738bfe15ce3220d523a7306f98817dd9f5bc569f87fce107231c34e0e626d980` | YES |
| `W1/check/test_j1_strict.py` | `29674640…` | `2967464025d650bc6a82a23019e0b5427b98f16a08acaf957c57b8b8aac17dd4` | YES |

- **aggregate_digest `8b4b4068…` is NOT reproducible from the five member hashes by any declared or obvious canonicalization.** 18 schemes were tested (sorted/unsorted, raw concat, JSON indent 0/1/2, `path:sha`, `sha  path`, LF/CRLF); none matched. The algorithm is undeclared. Treat the aggregate as a claimed value requiring the W2 Curator’s algorithm, not as a recomputable pin.

## 4. W2RequalificationMatrix — 12 rows against actual bytes

Legend: `L2` = `20261126T1225_W2_FINAL_CLOSURE/50_EVIDENCE/W2_CASE_LEDGER_R2.json`; `A` = `20_DEV/worktree/19_W2_NF_CODEX_20261126/FHS-5_PLP_W2_NATIVE_FIRST/assets`; `OPS` = `20261126T1121_W2_PRODUCT/50_EVIDENCE/ops`; `G9` = `…/23_W2_FINAL_CLOSURE_HERMES_20261126/W2_GUIDE_NINE_KEYS.json`. Hash prefixes are auditor-recomputed fixture/oracle bytes.

| # | Case | True current state | Evidence locator actually read | W3 action allowed |
|---|---|---|---|---|
| 1 | W2-DEV-01 (POS) | CARRIED, not frozen; r3 PASS, `raw:null`; re-run BLOCKED | `L2.cases[0]`; `A/fixtures…` fx `dea30408` / or `48df3438` | READ + re-freeze (R2); re-run only after R4 grant; no verdict reuse |
| 2 | W2-DEV-02 (NEG) | CARRIED, not frozen; r3 PASS, `raw:null`; re-run BLOCKED | `L2.cases[1]`; fx `99f91066` / or `4d29d627` | READ + re-freeze; re-run only after R4; no verdict reuse |
| 3 | W2-OPS-01 (POS) | CARRIED, not frozen; **NO r3 case row**; proxy only; re-run BLOCKED | absent from `L2`; `OPS/OPS_O04_CONSUMER_READBACK.json` (10/10) + `OPS_O05_COMPENSATION_POS.json` (4/4); fx `03494b3c` / or `9d5e7230` | READ + re-freeze; treat proxy as history only; re-run after R4 |
| 4 | W2-OPS-02 (NEG) | CARRIED, not frozen; r3 PASS, `raw:null`; re-run BLOCKED | `L2.cases[6]`; fx `168e8570` / or `a5d8732e` | READ + re-freeze; re-run after R4; no verdict reuse |
| 5 | W2-EFFECT-01 (NEG) | CARRIED, not frozen; r3 PASS, `raw:null`; re-run BLOCKED | `L2.cases[2]`; fx `3492f8cc` / or `a1e4c91f` | READ + re-freeze; re-run after R4; no verdict reuse |
| 6 | W2-AUTH-01 (NEG) | CARRIED, not frozen; r3 PASS, `raw:null`; re-run BLOCKED (would pass for the wrong reason) | `L2.cases[3]`; fx `80502748` / or `6365e895` | READ + re-freeze; **do not** re-run under the finding marker; R4 first |
| 7 | W2-RUNNER-01 (NEG) | CARRIED, not frozen; r3 PASS, `raw:null`; static re-run allowed | `L2.cases[7]`; fx `7ea614b4` / or `22931f33` | READ + re-freeze; static re-run permitted; no verdict reuse |
| 8 | W2-DELTA-01 (POS) | CARRIED, not frozen; **NO r3 case row**; proxy only; static re-run allowed | absent from `L2`; `G9` P1/P2, `delta_verdict=NEW_MATERIAL_EVIDENCE`, P2 `oracle_sha:null`; fx `cb61b06f` / or `155dc105` | READ + re-freeze; static re-run permitted; proxy ≠ PASS |
| 9 | W2-R3-01 (POS) | CARRIED, not frozen; r3 PASS, `raw:null`; static re-run allowed | `L2.cases[8]`; fx `5c721f15` / or `970ec9d7` | READ + re-freeze; static re-run permitted; no verdict reuse |
| 10 | W2-R3-02 (NEG) | CARRIED, not frozen; r3 PASS, `raw:null`; re-run BLOCKED | `L2.cases[5]`; fx `9867a715` / or `3b2ed871` | READ + re-freeze; re-run after R4; no verdict reuse |
| 11 | W2-R3-03 (NEG) | CARRIED, not frozen; r3 PASS, `raw:null`; re-run BLOCKED | `L2.cases[4]`; fx `8566b623` / or `1f9d9e15` | READ + re-freeze; re-run after R4; no verdict reuse |
| 12 | W2-R3-04 (EDGE) | CARRIED, not frozen; r3 PASS, `raw:null`; static re-run allowed | `L2.cases[9]`; fx `7c8ba861` / or `d26358c7` | READ + re-freeze; static re-run permitted; no verdict reuse |

- **Byte availability**: all 12 fixtures and all 12 oracles exist in pack `19_…` (24 files). No file has a frozen digest in `W2_FIVE_PINS`. Auditor set digest `9e24c1279ed317da43b8d6280ad10b782242205510660a3e3126652b27c745cc` (sha256 over sorted `path sha256\n`, **auditor-computed, not a W2 pin**).
- **Historical r1 ledger** (`20261126T1121/60_CLOSEOUT/W2_CASE_LEDGER.json`) has 12 rows but 4 `NOT_RUN`, 3 `STRUCTURAL_ONLY`, 1 `PARTIAL`; it is superseded and must not be summed with r3.

## 5. Findings

1. **r3 ledger has 10 rows, not 12.** `W2_CASE_LEDGER_R2.json` `total: 10`, all PASS, `raw: null` on every row. W2-OPS-01 and W2-DELTA-01 are absent. The handoff’s “10/10 (另 2 案由他案成立)” is a prose claim, not a case row.
2. **No per-case raw exists.** No stdout/stderr/exit/world/runner locator is attached to any of the 10 rows; the final round did not re-run them (`W2_FIVE_PINS.case_set.note` says so).
3. **r3 verdicts are on different code.** At r3 HEAD `660da33`: `w2_dev_gate.py` = `421adb1d…` and `w2_admission.py` = `a5f85a89…`, both **DIFF** from the frozen candidate (`ecef3f39…`, `8caabfff…`). Gate/admission behavior is exactly what most cases assert.
4. **Oracle freeze is incomplete.** Of the 5 “frozen” locators, `j1_expected_pins`, `s1`, `s1_delta`, `s2` resolve; `j1_checker_oracle` (`30_VERIFY/raw/CHECKER_J1_ORACLE.json`) **does not exist**. `PARTIALLY_FROZEN` is true, but the frozen set itself is not closed.
5. **`expected_pins.json` pins the W1 receiver `c6667402…` (9,336 bytes at `9fae925`), not the W2 candidate `768d6318…`.** Therefore the “J1 21/21” figure is evidence about the W1 delivery receiver, not about the current candidate.
6. **W2-OPS-01 proxy is on an older candidate.** `OPS_O03` records `w2_receiver_sha256 = ee92c8c8…` (38,753 bytes); `O04` 10/10 and `O05` 4/4 are real, but against that older receiver. `O03.w2_pack_parse.ok = false` (`PACK_INCOMPLETE_LOCAL`).
7. **W2-DELTA-01 proxy is not a PASS.** `G9` records `delta_verdict = NEW_MATERIAL_EVIDENCE`; P2 `oracle_sha` is `null` and `policy_epoch` is `unknown` (“two nulls are not a same-value claim”). This is a delta disclosure, not a case verdict.
8. **Aggregate digest is unverifiable as published.** `8b4b4068…` does not equal any tested canonicalization of the five member hashes or bytes; no algorithm is declared in the pack, pins, or receipts.
9. **r3 closeout conflicts with the final handoff.** `20261126T1225/60_CLOSEOUT/FHS-5_PLP_W2_CLOSEOUT.md` lines 12 and 53–56 claim `W2_NF_VALIDATED` “成立” and “12/12 原案全部 PASS”. The later `25_` closeout/handoff and `W2_CURRENT.claim_state` set `W2_NF_VALIDATED = NOT_CLAIMED`. The later artifact governs; the r3 claim is not evidence.
10. **Evidence pin is the `24_` manifest, not `25_`.** `W2_PUBLICATION_RECEIPT_r4b.json.delivery_manifest_sha256 = d4ba971f…` matches `24_/DELIVERY_MANIFEST.json` (7 files). `25_/DELIVERY_MANIFEST.json` (`bec9a2fb…`) is not pinned by any receipt (`manifest_self_hash: EXTERNAL_RECORD_ONLY`).
11. **Confirmed statuses**: `oracle = PARTIALLY_FROZEN`; `case_set = CARRIED_NOT_REFROZEN` (12 IDs); `writer = BLOCKED_NOT_ADMITTED`; marker `W2_NATIVE_RUNS/W2_SECURITY_FINDING.json` exists; `S1_DELTA` D4/D4b PASS with `ADMISSION_TERMINATED_BY_SECURITY_FINDING` / `FALSE_AUTHORITY`; S1 = 13 PASS/0 FAIL/1 `RESIDUAL_LIMIT`; S2 = 23/23.
12. **Delivery-pack status is intact**: `19_/05_W2_SOURCE_MANIFEST.json` = `81daac8f…` (65,377 B), 6 pack files + 25 assets; `W2_CURRENT` = `15329017…`; five pins = `74321487…`; closeout/handoff hashes match the receipt.

## 6. Can any W2 verdict be reused by W3? — No

A W2 verdict is reusable only if it is on the same candidate, same oracle bytes, same case set, with raw and an independent receipt. None holds:

- candidate changed (`660da33` → `dada235`/`3346076`) and the changed files are gate/admission;
- every r3 row is `raw: null` and was not re-run in the final round;
- 2 of 12 cases were never executed as cases;
- oracle/case-set were not re-frozen, so there is no frozen expected value to compare;
- `INDEPENDENT_PASS` is `NOT_CLAIMED` (verifier verdict FAIL, F1–F4; patch unreviewed);
- the active finding marker changes the first-fail ordering, so a re-run today would produce a different result for the wrong reason.

## 7. Signed-off statement — what W3 may NOT claim

I, the read-only W2 upstream auditor, sign off that as of 2026-11-26, on the bytes cited above, **W3 may NOT claim**:

1. `W2_NF_VALIDATED`, W2 acceptance, or “12/12 current PASS”.
2. Any W2 case PASS as current-candidate evidence, or that the 12-case denominator is closed.
3. That the oracle is fully frozen or that the case set is re-frozen.
4. That J1 21/21, r3 10/10, or the `8b4b4068…` aggregate validates the frozen candidate.
5. That W2-OPS-01 or W2-DELTA-01 was executed as a 12-case row.
6. `INDEPENDENT_PASS`, `W3_TECHNICALLY_READY`, `W3_EXECUTION_READY`, `RELEASED`, primary-use promotion, or merge to `main`.
7. That the protected writer is admitted, or that any protected write may proceed without a new Owner authorization (roots/targets/ops/expiry/recovery).
8. That the 15/15 (r2) or 16/16 (r3) W3 receive receipts are current.
9. That the aggregate digest has been reproduced; the algorithm is undeclared.

W3 P01 may proceed only with R0/R1 READ inventory, R2 Case-Owner re-freeze from real bytes, and R3 evidence work; execution remains gated on R4 and later R6.

**Signed**: W2 upstream auditor (read-only), 2026-11-26. No file under `C:\Projects` was altered.
