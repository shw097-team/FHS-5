# Spec Delta

## ADDED Requirements

### Requirement: Collaboration chain consumes artifacts

NF-T08 MUST verify that each party consumes the previous party's real output
pins, not merely that tools ran.

#### Scenario: Broken finding link

- **WHEN** FAR's finding id or raw digest differs from the frozen Challenge
- **THEN** the chain returns `FINDING_MISMATCH` or `RAW_MISMATCH`

### Requirement: Consumer fails closed before the CLI

The consumer MUST verify identity, pack, seal, W0M, candidate, oracle, handoff,
evidence index and path confinement before executing the product CLI.

#### Scenario: Wrong oracle pin

- **WHEN** the handoff oracle pin differs from the frozen oracle
- **THEN** the consumer rejects with `PIN_MISMATCH_ORACLE` and `cli_executed=false`

### Requirement: POSIX symlink evidence

The path security suite MUST include real file and directory symlinks on a
POSIX host, with an inside-link positive control.

#### Scenario: Symlink escape

- **WHEN** the input is a symlink to the outside canary
- **THEN** the CLI exits 3 with `INVALID_PATH`, no leak, and an inside link
  still returns `COMPLETE`

### Requirement: Isolated OFF profiles

Legacy providers, Bridge and FAR MUST be made unavailable in a real subprocess
profile, with controls, while B0 entries still work.

#### Scenario: Legacy import blocked

- **WHEN** a script imports `hgk_core` under the OFF profile
- **THEN** the import fails and is recorded; the same import succeeds without
  the profile
