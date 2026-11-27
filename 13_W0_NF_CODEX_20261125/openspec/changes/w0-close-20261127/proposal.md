# Proposal

## Why

The G3 W0 run reported 41/44 because its run root contained LF-normalised copies of the four TPM contracts and a regenerated oracle, while the frozen Guide/Resume pins referred to the committed byte-exact CRLF blobs. NF-T01 also accepted a reviewer double-fail entry as `ok=True`. The result is a real lineage and refusal defect, not a reason to rebuild W0.

## What Changes

- Fix `off_legacy.py` so reviewer double-fail is a required negative control, never an accepted positive entry; resolve the installed reviewer by actual path.
- Re-run the four-contract -> Guide -> Bridge/Native -> Challenge/FAR -> patch/resume/retest chain from byte-exact source and materialised candidate `bb66a27`, preserving oracle `112f2902...`.
- Reuse the 41 unaffected same-position receipts; do not rerun the other 41 cases.
- Add a shared consumer receipt-integrity gate for NF-T10/G17: one-byte mutation must return `RECEIPT_SHA_MISMATCH` before any downstream read.
- Add a thin fresh W1 minimal consumer that parses the current handoff, uses a real W0 requirement/case to write and read back a W1 checklist, and refuses wrong pin/scope/partial.
- Update the existing W0 C/H, Actual ChangeSet and evidence, not a second report system.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `w0-native-execution`: tighten OFF double-fail refusal, byte-bound contract consumption, receipt integrity and fresh W1 consumption.

## Impact

`13_W0_NF_CODEX_20261125/tools/{off_legacy,consumer,finalize_t10,w1_min_consume}.py`, W0 receipts/raw, evidence manifest, W0 CLOSEOUT/HANDOFF and Actual ChangeSet. No W1-W4 product execution, no main/W2_CURRENT change, no new runtime, registry or issuer.