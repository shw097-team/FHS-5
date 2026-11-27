# w0-native-execution Specification

## Purpose
Define the local CODEX-native execution contract for the FHS-5 W0 B0-NF batch:
what must be frozen, executed, refused and handed to W1.

## Requirements

### Requirement: Frozen pack identity

The executor MUST verify the manifest digest, every pack file digest and byte
count, and the W0M amendment digest before any construction.

#### Scenario: Digest mismatch

- **WHEN** any pack file digest or byte count differs from the manifest
- **THEN** the executor stops affected work with `PACKAGE_INTEGRITY_HOLD` and
  does not overwrite the source

### Requirement: Four construction contracts

The TPM path MUST produce PI, PD, DEV ECP and OPS ECP contracts from real source
pins and repo context, and MUST fail closed when a required child or source pin
is absent.

#### Scenario: Missing child B

- **WHEN** the sample source provides only A while the contract requires A and B
- **THEN** the gate returns `REQUIRED_CHILD_MISSING`, exit 2, parent FAIL

#### Scenario: No source pin

- **WHEN** a contract has no 64-hex source pin
- **THEN** the gate returns `SOURCE_UNBOUND`, exit 3, not admitted

### Requirement: Fail-closed sample CLI

`briefcheck` MUST accept only a relative path inside an approved existing root,
MUST verify SHA-256, MUST reject invalid UTF-8, duplicate, ambiguous and
malformed checklists, and MUST NOT write the source.

#### Scenario: Path escape

- **WHEN** the input is `../`, an absolute path, a UNC path, or traverses a
  junction
- **THEN** the CLI exits 3 with `INVALID_PATH` and never reads or echoes the
  outside canary

#### Scenario: Invalid root

- **WHEN** the approved root does not exist or is a file
- **THEN** the CLI exits 3 with `INVALID_PATH` and no traceback

### Requirement: Reversible local OPS

The local OPS slice MUST run a positive and a negative CLI case, write one
output under the approved output root, read it back, restore it, and prove the
source is unchanged.

#### Scenario: Output restore

- **WHEN** the output file is written and then removed
- **THEN** the pre-state is absent, the post-state is absent, and the source
  digest is unchanged

### Requirement: Provider OFF parity

The B0 direct path MUST run without importing HGK, FABRIC, SBL, FHS, PIPD or
HERMES modules, and MUST produce the same result in a marked environment.

#### Scenario: Import trace

- **WHEN** the CLI runs under `-X importtime` in a clean profile
- **THEN** the legacy module list is empty and the marked run has identical
  stdout and exit

### Requirement: Evidence receipts and independent challenge

Every case MUST have a receipt with candidate/source/fixture/oracle pins, argv,
exit, stdout/stderr digests, separate expected and observed, a verdict and
`not_covered`.

#### Scenario: Independent check

- **WHEN** the checker runs in a separate worktree and process
- **THEN** it re-executes POS/NEG/security cases, recomputes pins, finds no
  subject or oracle change, and emits a verdict with five pins

### Requirement: W1 handoff consumption

The handoff MUST carry pack, candidate, evidence and oracle pins, and a named
consumer MUST re-read them and refuse a wrong pack pin.

#### Scenario: Wrong pin

- **WHEN** the handoff pack digest is altered
- **THEN** the consumer refuses consumption

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
