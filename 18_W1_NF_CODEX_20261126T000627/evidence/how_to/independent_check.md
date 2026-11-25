# Independent read-only check — FHS-5 W1 NF-r5 candidate

- **Candidate**: `C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\18_W1_NF_CODEX_20261126T000627`
- **Pack**: `<candidate>\control_pack\FHS-5_PLP_W1_NATIVE_FIRST`
- **Checker**: `FHS5-W1-NF-r5-independent-readonly`
- **Mode**: read-only; no candidate files were created or modified.
- **Result**: 5 findings — 2 high, 1 medium, 2 low. No affirmative
  `W1_NF_VALIDATED` / `RELEASED` / `INDEPENDENT_PASS` claim was found.

## 1. Evidence manifest and seal

- Rehashed all **116** files listed in `EVIDENCE_MANIFEST.json`: **0**
  mismatches, **0** missing files, byte counts also match.
- `EVIDENCE_MANIFEST.json` raw file sha256 =
  `6f9687dcaaf110588ace59a149a2f375b0a4d91e29e2dbba3a4a92eac78cee8c`.
- `DELIVERY_SEAL.evidence_manifest_sha256` = the same value → **seal binding
  equal: true**. `seal.evidence_file_count` = 116.
- `DELIVERY_SEAL.pack_manifest_sha256` = `61f34a08…bfa30a`.
- `DELIVERY_SEAL.w2_receive_receipt_sha256` =
  `4027412c9f0107dd8a2e09bc0ab21bf413168db68070df9860c79c085e33a564`,
  which equals the actual `W2_RECEIVE_RECEIPT.json` file sha256.

## 2. Pack counts and digest

| Item | Observed | Expected |
|---|---:|---:|
| MD (pack root) | 5 | 5 |
| DEV rows (`## 2` table, header excluded) | 38 | 38 |
| OPS rows (`## 2` table, header excluded) | 29 | 29 |
| Cases (13 fixture case IDs) | 13 | 13 |
| Assets (13 fixtures + 13 oracles) | 26 | 26 |
| Sources | 42 | 42 |
| Holds | 14 | 14 |

- Raw `05_W1_SOURCE_MANIFEST.json` sha256 =
  `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`
  = the stated pin → **digest equal: true**.
- Rebuilt `source_set_sha256` from the 42 `id|sha256|bytes` lines =
  `8f2e484f46ff99bff9e1a0e6bf9dada0daea5ad2ee3b5357deb72435db32636c`,
  equal to the declared value.
- All 5 pack-file hashes and all 26 asset hashes were verified against file
  bytes; 0 bad.

## 3. Unit suite

`python -B -m unittest discover -s check -p test_*.py` → **79 tests, OK**
(no failures, no errors; 3.788 s).

The suite was run from a copy at
`work/checker_out/w1_copy` because `test_off_isolation` creates its temp
directory under `W1/check`. `PYTHONDONTWRITEBYTECODE=1` and `python -B` were
used. The copied 31 Python files reproduce the candidate sha
`806dea5d…70c57`, so the tested code is the candidate code.

## 4. Cases

- Total **20**: **PASS 19**, **DEFERRED 1** (`W1-HERMES-01`), **FAIL 0**,
  `NOT_OBSERVED 0`.
- `candidate_sha` raw value `806dea5d227dfd7de7e1cdf0e3f11303c211ff884ea2c39ef9925c5f35b70c57`;
  independently recomputed from `W1/impl/*.py` + `W1/check/*.py` (31 files) =
  the same value; all 19 rows that carry the field match.
- `source_sha` `8f2e484f…32636c` = recomputed source set.
- `pack_sha` `61f34a08…bfa30a` = pack pin.
- `case_set_sha256` `63a59b87…45cbce` = recomputed from assets; match.
- The four global digests (candidate/source/pack/case-set) are mutually
  distinct.
- 19 PASS evidence hashes are all distinct and each matches its `raw_path`
  file.
- 12 cases carry distinct, non-null oracle hashes; all 12 match the pack
  oracle assets. 8 rows have `oracle_sha256 = null`: `W1-HERMES-01`
  (DEFERRED) plus 7 PASS controls `N01`, `N02`, `N03`, `N04`, `N10`, `N11`,
  `W1-CODEX-05` (see F-03).

## 5. Host receipt

- `host_consumed = true`.
- **2 distinct sessions**:
  `01a21375-665e-71c3-b1af-8b1e701b5707` (pkgA_w1) and
  `01a21375-9b1f-7cd2-a4bc-a848ae6ff44a` (pkgB_w0).
- **7 stages**: Selected, Loaded, Installed (`REASONED_NA_NATIVE_ENTRY`),
  Bound, Invoked, ActualServed, Consumed. The other six are
  `OBSERVED_LOCAL`.
- Per-package served sha (reconstructed from the invocation payload; both
  match):
  - `pkgA_w1`: `09c49f5d88f1254677372c20d30683cfb49ca00d3a14af154d7899b992291dc9`
    (434 bytes)
  - `pkgB_w0`: `eefa21ff58b111fc3d3f13877c292559950d01493ac61ea7b3a18fa5367885b0`
    (306 bytes)
- Both context hashes and both canonical artifact hashes match their files;
  both consumer readbacks exist and their sha256 values match.

## 6. W2 inbound receipt

- `draft_completed = true`; artifact has 13 rows.
- `seam_wiring = 5/5` (`COMPLETE`).
- Session `01a21379-31e7-73d1-98bb-4d2870f612e9`, distinct from both host
  sessions.
- Consumer checks: all 8 true; `consumer.parsed.all = true`.
- `permission_state = NONE_GRANTED`; `grant_issued = false`.
- `draft_material.manifest_sha256` matches the shipped
  `05_W2_SOURCE_MANIFEST.json` (`c251ebc0…bfa8`).

## 7. OFF task receipt

- `state = ON_OFF_BOTH_SEMANTIC_SUCCESS`; `on_rows = 13`, `off_rows = 13`;
  `projection_equal = true`.
- `cold_off = true`; blocked 5 (`hgk_runtime`, `fabric_runtime`,
  `sbl_runtime`, `pipd_runtime`, `hermes_runtime`); leaked 0.
- Positive control: module `json`, imported `true`, state `OBSERVED`.
- Forbidden imports in the OFF path: `[]` (guard scope:
  `tpm_contracts_nf`, `guide_nf`, `bridge_nf`, `w2_inbound`).
- **Caveat**: the receipt records no OFF input path/sha, and the shipped
  `context_bundle.md` produces 0 parsed rows under `_off_native.py` (the
  shipped `03_W2_DRAFT_TQAEP.md` has 13 rows but uses `W2-Bxx` ids that the
  script's digit-only filter rejects). The 13-row parity is therefore not
  reproducible from the candidate alone (see F-05).

## 8. Closure matrix

- 118 rows; declared `row_count = 118`; counts sum to 118:
  `EVIDENCED 17`, `COVERED_BY_SHARED_OPERATION 62`,
  `EXERCISED_INDIVIDUALLY 2`, `NOT_APPLICABLE_THIS_ROUND 1`,
  `DEFERRED 3`, `PASS 18`, `EVIDENCED_WITH_DEFERRED_HOSTS 1`,
  `HOLD_PRESERVED_NOT_CLOSED 14`.
- **Dangling PASS/EVIDENCED references (2)**:
  - `P06` — `evidence/how_to/independent_check.json` missing
  - `W1-A06` — `evidence/how_to/independent_check.json` missing
- Eight more `COVERED_BY_SHARED_OPERATION` rows (`DEV-PROH-01..04`,
  `DEV-RB-01..04`) cite the same missing file; 10 rows total are affected.
  `W1_CLOSURE_MATRIX.md` lines 22, 49–56 and 114 carry these references.

## 9. W2 receive receipt

- `accepted = true`; `check_count = 29`; all 29 checks `ok = true`.
- No grant: `permission_boundary` says no grant, no protected effect.
- **Hash inconsistency**: the receipt records
  `manifest_sha256_at_receive = 88fcbcdc…92730f7` and its
  `seal_manifest_binding` check reports
  `seal = recomputed = 88fcbcdc…92730f7`, but the delivered manifest and seal
  are `6f9687dc…78cee8c`. The final seal still hashes the receipt file
  (`4027412c…`), so the receipt is sealed into a delivery whose manifest it
  did not accept (see F-02).

## 10. Claim audit

Scanned the 4 root Markdown documents and the 5 pack Markdown documents.
Six occurrences of the three tokens were found; all are explicit
disclaimers or conditional rules:

| File | Line | Disposition |
|---|---:|---|
| `control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md` | 10 | `Not claimed` |
| `control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md` | 72 | `NOT_CLAIMED` |
| `control_pack/FHS-5_PLP_W1_NATIVE_FIRST/01_W1_DEV_ECP.md` | 33 | `仍 NOT_CLAIMED` |
| `control_pack/FHS-5_PLP_W1_NATIVE_FIRST/04_W1_START_THIN_PROMPT.md` | 100 | conditional (`才可`) |
| `control_pack/FHS-5_PLP_W1_NATIVE_FIRST/04_W1_START_THIN_PROMPT.md` | 104 | `NOT_CLAIMED` |
| `FHS-5_PLP_W1_CLOSEOUT.md` | 9 | `不宣稱` |

No affirmative `W1_NF_VALIDATED`, `RELEASED`, or `INDEPENDENT_PASS` claim
without evidence was found.

## Findings

### F-01 — High — closure traceability

Two EVIDENCED closure rows cite
`evidence/how_to/independent_check.json`, which is absent from this candidate:

- `P06` (closure matrix + seal + handoff)
- `W1-A06` (claim-ceiling audit)

Eight further `COVERED_BY_SHARED_OPERATION` rows cite the same missing file,
so 10 rows rest on a non-existent artifact. The file exists only in the
earlier `17_W1_NF_CODEX_20261125T232008` deliverable.

Evidence: `W1_CLOSURE_MATRIX.json` rows P06, W1-A06, DEV-PROH-01..04,
DEV-RB-01..04; `W1_CLOSURE_MATRIX.md:22,49-56,114`.

### F-02 — High — W2 acceptance bound to a different manifest

`W2_RECEIVE_RECEIPT.json` records
`manifest_sha256_at_receive = 88fcbcdc9bbefd7dc7095da2ad2667a262fefc8b73a3061005e98606492730f7`
and its `seal_manifest_binding` check reports
`seal = recomputed = 88fcbcdc…`. The delivered
`EVIDENCE_MANIFEST.json` and
`DELIVERY_SEAL.evidence_manifest_sha256` are
`6f9687dcaaf110588ace59a149a2f375b0a4d91e29e2dbba3a4a92eac78cee8c`.
The final seal does hash the receipt file
(`4027412c…e33a564` matches), so the receipt is shipped with a delivery it
did not accept.

### F-03 — Low — oracle binding gap

Seven PASS rows (`N01`, `N02`, `N03`, `N04`, `N10`, `N11`,
`W1-CODEX-05`) have `oracle_sha256 = null`; only the 12 pack cases carry
oracle digests. Those 12 hashes are unique and match the pack assets, and
all 19 PASS evidence hashes are unique, so this is a coverage gap rather
than digest reuse.

### F-04 — Low — reproduction argv points at a non-existent file

The 19 full observations record
`...\W1\impl\run_cases_nf.py` as `argv[0]`, but that file does not exist.
The runner is `...\W1\check\run_cases_nf.py` (and `runner_id` correctly says
`check/run_cases_nf.py`). The recorded command cannot be replayed as-is.

### F-05 — Medium — OFF projection input is unbound

`off_task_receipt.json` records only `rows`, `exit`, and
`imported_forbidden` for the OFF path; it records no input locator or input
sha256. Running the shipped `_off_native.py` against the shipped
`context_bundle.md` yields `rows=[]`; the shipped W2 TQAEP has 13 rows but
its first column is `W2-Bxx`, which the script's digit-only filter rejects.
The 13-row OFF parity therefore cannot be recomputed from the candidate
alone. The empty forbidden-import result is observed but is vacuous for the
same reason.

## Deliverables

- JSON: `C:\Users\user\Documents\Codex\2026-11-25\new-chat-12\work\checker_out\independent_check_r5.json`
- Markdown: this file
