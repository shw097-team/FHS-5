# Proposal

## Why

`FHS-5/W0/B0-NF` was authorized by `W0-CODEX-FIRST-20261125-01` to move from a
planned control pack to real local evidence: five-party invocation, a bounded
reversible DEV/OPS slice, independent challenge, FAR alternatives and a real
W1 consumer. The prior round delivered a representative B0 but left W0 at
`W0_PARTIAL_VALIDATED`; the remaining required case semantics had no receipts.

## What Changes

- Execute the sealed `W0-NF-r3-CODEX-PRIMARY` pack without modifying it.
- Generate the four TPM contracts (PI, PD, DEV ECP, OPS ECP) from real bytes and
  gate them on missing child B and absent source pins.
- Extend the briefcheck candidate from v2 to v3 (`12'`) after a real red:
  invalid `--root` raised `FileNotFoundError` and exited 1.
- Produce 44 per-case receipts: SAMPLE-R1..R10, `F5-W0-T01..T24`,
  `NF-T01..T10`, with argv/exit/raw and separate expected/observed.
- Run local OPS O1–O5 including a reversible output write and an import trace
  showing no HGK/FABRIC/SBL/FHS/PIPD modules.
- Run an independent Challenge in a separate git worktree and process.
- Record a FAR finding with three alternatives and fail-closed close policy.
- Deliver CLOSEOUT, HANDOFF and UPSTREAM_CHANGESET; consume the handoff as W1.

## Capabilities

### New Capabilities

- `w0-native-execution`: the local CODEX-native execution contract for W0 —
  frozen source, four contracts, fail-closed sample CLI, reversible OPS,
  evidence receipts, independent challenge and W1 handoff consumption.

### Modified Capabilities

None. This change does not alter the existing W1 or Legacy capability specs.

## Impact

- New delivery root `13_W0_NF_CODEX_20261125` in the authorized workspace.
- Candidate repository `02_CANDIDATE/repo`, commit v3 (child of the frozen B0
  candidate `5eab43d`).
- No change to the sealed control pack, W0M, MASTER/PROG/PROJ/WM or any
  external Host.
- No release, publisher signature, or external OS/Repo grant is claimed.
