# Independent Read-Only Check — FHS-5 W1 NF-r4 Candidate

- **Checker:** independent-checker-r4 (read-only)
- **Candidate:** `C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3`
- **Delivery:** `...\17_W1_NF_CODEX_20261125T232008`
- **Checked at:** 2026-11-25 ~23:30 +08:00
- **Verdict:** **PASS WITH FINDINGS** — integrity, pack pin, tests, cases, closure and W2 shape
  verify; two medium traceability defects and one host-identity gap remain.

## Method and write statement

All commands ran with `PYTHONDONTWRITEBYTECODE=1` and `python -B`. Nothing was written under the
candidate.

`W1\check\test_off_isolation.py` calls `tempfile.mkdtemp(prefix="w1_r03_test_", dir=str(HERE))`,
which writes inside the check directory. Therefore `W1\impl` and `W1\check` were **copied** to
`work\checker_out\candidate_copy\W1` and the suite was run from that copy with
`W1_PACK` pointed at the real frozen pack. Pre-existing `__pycache__` files under the candidate are
timestamped 22:29, before this review; they were neither created nor touched here.

## 1. Evidence manifest recompute

| Item | Result |
|---|---|
| Entries listed | 100 |
| Files recomputed | 100 |
| SHA-256 mismatches | **0** |
| Missing files | 0 |
| Recomputed manifest SHA-256 | `cd0ca55ebcd1d4d077eaf0802122c78c19c5d9aebd40250f548ae5ff2b41082e` |
| `DELIVERY_SEAL.evidence_manifest_sha256` | `cd0ca55ebcd1d4d077eaf0802122c78c19c5d9aebd40250f548ae5ff2b41082e` |
| Seal binding | **OK (equal)** |

`file_count` (100) equals the number of manifest rows and the seal's `evidence_file_count` (100).

## 2. Pack facts

| Fact | Expected | Measured | Match |
|---|---|---|---|
| Pack MD files | 5 | 5 (`00`–`04`) | yes |
| DEV ids | 38 | 38 unique `DEV-*-NN` | yes |
| OPS ids | 29 | 29 unique `OPS-*-NN` | yes |
| Cases (fixture set) | 13 | 13 fixtures | yes |
| Assets | 26 | 26 (13 fixtures + 13 oracles; manifest 26) | yes |
| Sources | 42 | 42 | yes |
| Holds | 14 | 14 | yes |
| Pack manifest SHA-256 | `61f34a08…4bfa30a` | `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a` | yes |

Pack manifest digest equals the pin and the seal/manifest `pack_manifest_sha256`.

## 3. Test suite

Copied tree, `python -B -m unittest discover -s W1\check -p "test_*.py"`:

```
Ran 74 tests in 2.349s

OK
```

- Count **74**, result **OK**.
- Recorded `evidence/test_run.txt` independently shows 74 tests, OK (2.622s).

## 4. Case evidence (`evidence/cases.json`)

| Item | Value |
|---|---|
| Rows | 20 (13 named + 6 subcases + 1 ACC) |
| PASS | 19 |
| FAIL | **0** |
| DEFERRED | 1 (`W1-HERMES-01`, reason "Hermes host not mounted", exit/observed null) |
| PASS with no execution | **none** (all PASS rows have non-null exit and raw digest) |
| Raw evidence SHA checked | 19/19 match `raw_sha256` |
| Digest split | `candidate`, `source/pack`, `case_set`, `oracle`, `evidence` are not all equal → OK |

Note: `source_sha` and `pack_sha` are identical in every row (both the pack pin), so two of the six
digest domains collapse. See F-04.

## 5. Host receipt (`evidence/host/host_receipt.json`)

| Item | Result |
|---|---|
| `host_consumed` | **true** |
| Packages | 2 |
| Session ids | `01a2134b-0117-7393-83fe-63f07e89a19e`, `01a2134b-2ce2-79c1-8716-e9a1f78556fc` — distinct |
| Stage values | 6 × `OBSERVED_LOCAL`, 1 × `REASONED_NA_NATIVE_ENTRY` (7 stages, non-constant) |
| Served text SHA | `b90dca5b88135a630c4cd20d20b097179eb2c93f1057ebce9bc60e2e05d4caad` (present, 64 hex) |

Hardcode assessment: the ledger is non-constant and `stage_evidence` carries distinct per-stage
detail, so it does not look naively hardcoded. However, the 7-stage row is byte-identical across the
global ledger and both packages, only two values are ever used, and only one global
`ActualServed`/`Invoked` block exists (for pkg2). Package A has no per-package served digest or
per-package stage evidence in the receipt. See F-06.

## 6. Closure matrix (`W1_CLOSURE_MATRIX.json`)

| Verdict | Count |
|---|---|
| COVERED_BY_SHARED_OPERATION | 62 |
| PASS | 18 |
| EVIDENCED | 17 |
| HOLD_PRESERVED_NOT_CLOSED | 14 |
| DEFERRED | 3 |
| EXERCISED_INDIVIDUALLY | 2 |
| NOT_APPLICABLE_THIS_ROUND | 1 |
| NOT_OBSERVED | 1 |
| **Rows** | **118** |

- PASS rows without an `evidence_ref`: **0** (18/18 have refs).
- But **9 rows cite a missing `independent_check.json`**, including `P06` with verdict `EVIDENCED`.
  See F-02.
- All other evidence refs resolve under the delivery, `evidence/`, or pack root.

## 7. W2 receive receipt

| Item | Value |
|---|---|
| `accepted` | **true** |
| Checks | **23** (23 recorded, 0 rejected) |
| Grant issued | **no** — `permission_state = NONE_GRANTED`, no grant/protected-effect keys |
| Boundary | "W2 receives evidence only; no grant issued, no protected effect" |
| `seal_manifest_binding` | `ea5aaa2566c7b7c7a13bc55d893675b936653e22b6864f359368f3eed0ac5c49` |

That binding value is **not** the delivered manifest hash (`cd0ca55e…`). See F-01.

## 8. Claim audit

Scanned 178 `.md`/`.json`/`.txt` files across the delivery, frozen pack, `W1\primary`, and
`W1\evidence`, looking for `W1_NF_VALIDATED`, `RELEASED`, `INDEPENDENT_PASS`, `NATIVE_PASS`.

- 131 token occurrences found.
- **0 affirmative claims** that the candidate is validated/released/independently passed.
- 128 occurrences are entries inside `"not_claimed": [...]` arrays.
- 3 occurrences are upstream state-table rows:
  - `W1/primary/sources/M.md:1049` — RELEASE state table (text carries a negative qualifier).
  - `W1/primary/sources/W0MB.md:246` — W0-B target state with `Host/Issuer HOLD`.
  - `W1/primary/sources/WM.md:1427` — release-state enum list.
- `FHS-5_PLP_W1_CLOSEOUT.md:8-9` claims only `W1_PARTIAL_VALIDATED` and explicitly disclaims
  `RELEASED`, `M-DONE`, `GPT_CHAT_PASS`, `GPT_WORK_PASS`, `HERMES_PASS`, `W2_EXECUTION_READY`.

**Result: no unsupported W1_NF_VALIDATED / RELEASED / INDEPENDENT_PASS claim found.**

## Findings

### F-01 — Medium — W2 receipt binds a superseded manifest

`W2_RECEIVE_RECEIPT.json` records `seal_manifest_binding` as `ea5aaa25…`, while the delivered
`EVIDENCE_MANIFEST.json` hashes to `cd0ca55e…` (matching the seal). `ea5aaa25…` also matches neither
the raw bytes nor LF-normalized or canonical-JSON forms of the delivered manifest, so the receipt
binds a different manifest revision and its "seal_manifest_binding ok" check does not hold for the
delivered bytes. The build script loads the W2 receipt and then rewrites the closeout/handoff/
changeset and regenerates the manifest (`make_delivery4.py:261-295`); the receipt timestamp
15:21:20Z precedes the seal 15:21:41Z.

### F-02 — Medium — Dangling closure evidence refs

9 closure rows cite `independent_check.json` (three path spellings), which is absent from the
delivery, the frozen pack, and `evidence/`. `P06` carries verdict `EVIDENCED`, so a pass-equivalent
row points at non-existent evidence. Affected: `P06`, `DEV-PROH-01..04`, `DEV-RB-01..04`.
`W1_CLOSURE_MATRIX.md:22,49-56` reproduces the same refs.

### F-03 — Medium — Second host package has `subject: "None"` and no value check

`pkgB_w0_artifact.json` (and `pkgB_w0_stdout.txt`) contain `"subject": "None"` and
`"next_action": null`. `host_receipt.json` sets `per_package.pkg2.value_check = null`, so no
subject/scope/fixture join was done for that package, yet its stage row records
Bound/Invoked/ActualServed/Consumed as `OBSERVED_LOCAL`. The receipt also holds only one global
served-text digest and one `Invoked` argv (for pkg2/work_b), so package A's served digest is not in
the receipt.

### F-04 — Low — Weak digest separation

`source_sha == pack_sha == 61f34a08…` in all 20 case rows. The six digest fields are not all
identical, so the required split is technically satisfied, but two declared domains are the same
value everywhere.

### F-05 — Low — Run-id mismatch

Cases/host evidence use run id `20261125T232032`; delivery, manifest, and seal use
`20261125T232008`. Consistent with a later evidence sub-run, but not unified.

### F-06 — Low — Stage-row uniformity

The 7-stage rows are identical in the global ledger and both packages, with only
`OBSERVED_LOCAL`/`REASONED_NA_NATIVE_ENTRY` values. Not proof of hardcoding (distinct
`stage_evidence` exists), but per-package rows are undifferentiated copies.

## NOT_VERIFIED / limits

- **Authenticity of the Codex host sessions is NOT_VERIFIED.** The two session ids are distinct,
  well-formed UUIDs and the artifacts/stdout are present, but an offline read-only check cannot
  re-prove that they came from live `codex exec` processes. Only receipt content and artifacts were
  inspected.
- **Stage-value truth is NOT_VERIFIED beyond cross-checks.** Values were compared across the ledger,
  per-package rows, and `stage_evidence`; no live host probe was repeated.
- **W2 acceptance is stale** (F-01); the receipt's own `evidence_manifest_recompute` result (`[]`)
  cannot be attributed to the delivered manifest.

## Artifacts

- `work/checker_out/independent_check_r4.json`
- `work/checker_out/facts.json` (raw measurements)
- `work/checker_out/test_run_copied.txt` (reproduced test run)
