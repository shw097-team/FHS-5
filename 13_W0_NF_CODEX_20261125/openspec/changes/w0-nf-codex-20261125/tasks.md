# Tasks

## 1. Reconcile and freeze

- [x] 1.1 Verify `05_W0_SOURCE_MANIFEST.json` digest `e3772aee…` and all five pack file hashes/bytes.
- [x] 1.2 Verify S33 W0M CODEX-FIRST-r4 digest `c9b1ca9b…`.
- [x] 1.3 Probe Python 3.11.9, Git 2.53.0, Codex CLI 0.164.0, OpenSpec 2.0.0.
- [x] 1.4 Freeze repo baseline `5eab43d` and record preimages.

## 2. Contracts and parties

- [x] 2.1 Generate PI/PD/DEV ECP/OPS ECP from real pins (`03_PARTIES/tpm`).
- [x] 2.2 Run missing-B and no-source gates.
- [x] 2.3 Run real `plp-tpm-review` 1.0.1: 0 defects, 10 authority/reader unbound.
- [x] 2.4 Guide Touch1/Touch2 with nine-key delta and scope-drift refusal.
- [x] 2.5 Bridge four APIs with path/scope/cross-subject negatives.

## 3. DEV and OPS

- [x] 3.1 Freeze the red probe (invalid root, exit 1).
- [x] 3.2 Patch as `12'` and commit candidate v3 `bb66a27`.
- [x] 3.3 Retest 12 unit tests plus the 2-test probe.
- [x] 3.4 OPS O1–O5: POS/NEG, output, readback, restore, OFF trace.

## 4. TQAEP

- [x] 4.1 Freeze oracle before execution.
- [x] 4.2 Run SAMPLE-R1..R10 with real junction path escape.
- [x] 4.3 Run `F5-W0-T01..T24` with per-case receipts.
- [x] 4.4 Run `NF-T01..T10`.
- [x] 4.5 Summarize 44/44 receipts and not-covered.

## 5. Independent assurance and delivery

- [x] 5.1 Run independent Challenge in a separate worktree: 30 checks, 0 findings.
- [x] 5.2 Record FAR finding with three alternatives and fail-closed close.
- [x] 5.3 Write CLOSEOUT, HANDOFF and UPSTREAM_CHANGESET.
- [x] 5.4 W1 consumer re-reads pack/candidate/evidence and refuses a wrong pin.
- [x] 5.5 Publish the W0 evidence bundle to `shw097-team/FHS-5`.
