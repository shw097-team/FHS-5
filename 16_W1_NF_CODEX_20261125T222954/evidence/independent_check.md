# Independent check — W1_NF_r3 (20261125T222954)

**Mode:** independent-readonly · **writes_to_candidate:** 0

## 1. Evidence manifest recompute
- Checked **86/86** listed files (declared file_count 86).
- SHA-256 mismatches: **0**; byte mismatches: **0**; missing: **0**.
- EVIDENCE_MANIFEST.json sha256 = `74fb7b322a029a08621090e1749491c7e2e141a358fe80a22fbd45badd27b786`; matches DELIVERY_SEAL: **True**.
- `.sha256` sidecar: 86 entries, 0 differences.
- Delivery dir has 90 files; the 4 unlisted are bundle meta: .gitattributes, DELIVERY_SEAL.json, EVIDENCE_MANIFEST.json, EVIDENCE_MANIFEST.sha256.

## 2. Frozen pack
- 05 manifest sha256 = `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a` → **matches pin: True**.
- 5 MD + 05 manifest: **5 MD**, 1 manifest; pack_files order/digests **True**.
- Assets: **26** (13 fixtures + 13 oracles), digests **True**.
- IDs: **DEV 38**, **OPS 29**, **cases 13** (14 regex matches incl. scope `W1-NF-01`), **sources 42**, **holds 14**.
- source_set_sha256 matches declared: **True**.
- Present sources **17/42**, missing **25**, digest differences among present **0**.
- `nf_pack_guard.py verify` = **REJECT / SOURCE_MISSING / PLAN** (first absent source). Reader records these as LOCAL_MISSING_RECORDED.

## 3. Unit tests
- `python -B -m unittest discover -s W1\check -p "test_*.py"` → **63 tests, OK, exit 0**.

## 4. Case runner
- With `W1_SECOND_PACK`: **total 20** — PASS 18, NOT_OBSERVED 1, DEFERRED 1, FAIL 0.
- Without `W1_SECOND_PACK`: **total 19** (17 PASS / 1 NOT_OBSERVED / 1 DEFERRED); W1-CODEX-05 is omitted.
- All emitted raw_sha256/stdout_sha256 recomputed and matched; no PASS without a real artifact; HERMES-01 DEFERRED with exit/raw = null.

| Case | Verdict | | Case | Verdict |
|---|---|---|---|---|
| `W1-HOST-01` | NOT_OBSERVED | | `W1-R3-03` | PASS |
| `W1-HOST-02` | PASS | | `W1-R3-04` | PASS |
| `W1-HOST-03` | PASS | | `W1-R3-05` | PASS |
| `W1-HERMES-01` | DEFERRED | | `N01` | PASS |
| `W1-ABI-01` | PASS | | `N02` | PASS |
| `W1-ABI-02` | PASS | | `N03` | PASS |
| `W1-SEC-01` | PASS | | `N04` | PASS |
| `W1-API-01` | PASS | | `N10` | PASS |
| `W1-R3-01` | PASS | | `N11` | PASS |
| `W1-R3-02` | PASS | | `W1-CODEX-05` | PASS |

## 5. Adversarial probes
- (a) Path traversal (`..`, drive letter, UNC, absolute, backslash, NUL): **all rejected** with `PATH_OUTSIDE_ROOT` (12/12, both resolve_body and resolve_inside).
- (b) Duplicate JSON key: **rejected** with `STRICT_JSON_REJECT` (top-level, nested, and a duplicate injected into a copied 05 manifest).
- (c) Wrong manifest pin: **rejected** with `SOURCE_INTEGRITY_FAILED` for `bridge_nf.inspect_package` and `w1_consumer.consume`; correct pin accepted.

## 6. Claim ceiling audit
- Claim ceiling is `W1_PARTIAL_VALIDATED` (DELIVERY_SEAL.json:7, CLOSEOUT:9).
- **No positive claim** of `W1_NF_VALIDATED`, `INDEPENDENT_PASS`, `RELEASED` or `NATIVE_PASS`. All hits are not_claimed lists, HOLD tables, or the `H6_fake_claims` mutation fixture in run_harness.py.
- `inspect.json` claims: w1_nf_validated=NOT_RUN, independent=NOT_RUN, release=NOT_ADMITTED.
- **Gap:** CLOSEOUT:131 cites `evidence/independent_check.json`, which does not exist and is not in the evidence manifest.
- **Gap:** stated HEAD `c2d8084…` (base) differs from actual HEAD `bb87f441…`.

## 7. Findings
- **F1-independent-check-evidence-absent** [medium/claim_without_evidence] — CLOSEOUT §5 cites evidence/independent_check.json as the independent-check result, but the file is absent from the delivery and is not among the 86 files listed in EVIDENCE_MANIFEST.json; make_delivery.py only embeds the text reference and never writes the file.
  - Evidence: FHS-5_PLP_W1_CLOSEOUT.md:131; make_delivery.py:152; Test-Path 16_W1_NF_CODEX_20261125T222954/evidence/independent_check.json = False; EVIDENCE_MANIFEST.json files=86 (no independent_check.json)
- **F2-negative-cases-use-runner-local-helpers** [medium/validation_depth] — Four PASS observations exercise helper functions defined inside run_cases_nf.py, not any W1/impl product code: W1-ABI-01 -> crosswalk_version_guard(), W1-ABI-02 -> abi_completeness(), W1-R3-03 -> require_effect_resume(), W1-R3-05 -> a hardcoded claim dict. Those PASS verdicts do not evidence the implementation rejecting a real malformed artifact.
  - Evidence: W1/check/run_cases_nf.py:171 def crosswalk_version_guard; :183 def abi_completeness; :261 def require_effect_resume; :282 def c_r3_05; grep found these defs only in run_cases_nf.py, none in W1/impl/*.py
- **F3-stated-head-is-base-not-delivered-commit** [low/identity_pin_inaccuracy] — Closeout/handoff/changeset state repo HEAD = c2d8084... (the base), but the worktree HEAD is bb87f441... on the same branch. The stated HEAD is not the delivered commit.
  - Evidence: git rev-parse HEAD = bb87f441d0e16d7371e064b3ce614a0972709889; FHS-5_PLP_W1_CLOSEOUT.md:8; FHS-5_PLP_W1_HANDOFF.md:5; W1_UPSTREAM_CHANGESET.md:28
- **F4-derived-exit-and-argv-fields** [low/evidence_semantics] — Each observation's exit is derived in-process (0 normal return, 2 NFError, 1 other exception) and argv points at run_cases_nf.py; it is not a subprocess exit code. Raw/stdout hashes are genuine (recomputed), and the unexecuted W1-HERMES-01 is DEFERRED with exit=null and raw_sha256=null, so no unexecuted case is marked PASS.
  - Evidence: W1/check/run_cases_nf.py:77,89,98 (exit assignments), :120 (skip exit None / raw_sha256 None); independent recompute: 20/20 raw_ok=True, 20/20 stdout_ok=True; W1-HERMES-01 verdict=DEFERRED exit=None raw_sha=None
- **F5-second-pack-env-gate** [low/reproducibility] — Without W1_SECOND_PACK the runner emits 19 observations and omits W1-CODEX-05 entirely (absent, not NOT_RUN). The delivered 20-count depends on an external env var plus a second W0 pack.
  - Evidence: my run without env: total=19 (17 PASS / 1 NOT_OBSERVED / 1 DEFERRED); with W1_SECOND_PACK: total=20 (18 PASS); W1/check/run_cases_nf.py:577
- **F6-pack-guard-rejects-on-missing-sources** [low/source_coverage] — nf_pack_guard.py verify REJECTs with SOURCE_MISSING(PLAN): only 17 of 42 declared LOCAL_VERIFIED sources are present at probe time; 25 are absent and none of the present ones differ. The product reader downgrades absent recorded sources to LOCAL_MISSING_RECORDED (amendment A1) and inspect.json records 25 missing. The closeout's '42 sources 逐筆稽核' wording overstates digest-verification coverage.
  - Evidence: nf_pack_guard.py verify -> {result:REJECT, token:SOURCE_MISSING, detail:PLAN}; enumeration present=17 missing=25 digest_diff=0; evidence/inspect.json source_local_missing=25; FHS-5_PLP_W1_CLOSEOUT.md §1 table row '42 sources 逐筆稽核'
- **F7-manifest-lists-86-of-90-files** [info/manifest_scope] — EVIDENCE_MANIFEST.json lists 86 evidence files while the delivery dir holds 90. The 4 unlisted files are bundle meta (.gitattributes, DELIVERY_SEAL.json, EVIDENCE_MANIFEST.json, EVIDENCE_MANIFEST.sha256). No listed file is missing and no listed sha/bytes mismatch.
  - Evidence: on_disk=90 listed=86 unlisted=['.gitattributes','DELIVERY_SEAL.json','EVIDENCE_MANIFEST.json','EVIDENCE_MANIFEST.sha256']; checked=86 sha_mismatches=0 bytes_mismatches=0

## 8. Writes / limitations
- `writes_to_candidate = 0`. All python runs used `PYTHONDONTWRITEBYTECODE=1` and `-B`; final sweep found 0 candidate files with mtime after 22:33:00 (newest 22:32:08).
- Checker and maker share the same OS principal; this is not a different-principal independence claim.
- 25 external sources are absent at probe time; their absence was observed, not fetched.
