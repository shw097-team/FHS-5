# Proposal

## Why

The first W0 delivery proved a representative loop but left four assurance
gaps: NF-T08 counted artifacts instead of consuming them; the consumer did not
verify the oracle or the evidence index and could still run the CLI on a bad
pin; symlink security was `NOT_VERIFIED` on Windows; and OFF relied on env
markers rather than real isolation.

## What Changes

- Add `collab_chain.py`: eight producer→consumer segments plus seven broken-link
  negatives.
- Replace the consumer with a fail-closed 776-check validator that reads 667
  indexed files, the oracle, handoff, seal and candidate before running the CLI.
- Add a POSIX symlink suite executed in WSL2 ext4 (real file/dir symlinks).
- Add real OFF profiles for legacy providers, Bridge and FAR.
- Derive evidence claims from artifacts instead of hardcoding them.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `w0-native-execution`: adds consumed-artifact chain, pre-CLI consumer
  verification, POSIX symlink evidence and isolated OFF profiles.

## Impact

Tools, TQAEP receipts NF-T01/05/06/08/10 and T06, evidence/consumer manifests,
delivery pins. Candidate code is unchanged (`bb66a27`).
