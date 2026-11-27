# w0-native-execution delta

## ADDED Requirements

### Requirement: Byte-bound four-contract consumption

Guide MUST consume the four TPM contract files by their actual bytes and MUST expose pins, source manifest match and requirement IDs that the collaboration checks can compare with the frozen files.

#### Scenario: Stale contract copy

- **WHEN** the contract files in the run root differ from the pins recorded by Guide or the frozen source
- **THEN** the collaboration chain fails with `CONTRACT_CONTEXT_MISSING` or an equivalent typed code and does not claim `COMBINED_OK`

#### Scenario: Live mutation

- **WHEN** one contract byte is changed and Guide is invoked at the same entry with the mutated directory
- **THEN** the chain refuses the context before FAR, patch or retest effects

### Requirement: Receipt integrity gate

The consumer MUST verify a receipt digest from raw bytes before parsing it or performing any downstream operation.

#### Scenario: One-byte receipt mutation

- **WHEN** a valid receipt copy is changed by one byte
- **THEN** the same consumer entry returns `RECEIPT_SHA_MISMATCH`, writes no downstream marker and reads no outside file

### Requirement: Fresh W1 minimal consumption

A fresh process MUST parse the current W0 handoff and pins, generate a W1-usable checklist from a real W0 requirement or case, write it under an authorised output root, and read it back.

#### Scenario: Wrong scope or partial

- **WHEN** the pin, scope or required evidence is wrong or partial
- **THEN** the consumer returns a typed refusal and writes no checklist

## MODIFIED Requirements

### Requirement: Provider OFF parity

The B0 direct path MUST run without importing HGK, FABRIC, SBL, FHS, PIPD or HERMES modules, with real ON/OFF exits, import observation and a positive control. A reviewer double failure MUST be a rejected negative control, not a parity success.

#### Scenario: Import trace

- **WHEN** the CLI runs under `-X importtime` in a clean profile
- **THEN** the legacy module list is empty and the marked run has identical stdout and exit

#### Scenario: Double failure

- **WHEN** the reviewer is given an absent output root and both ON/OFF runs fail
- **THEN** the run records a rejected negative control and does not treat the entry as `ok=True`

### Requirement: W1 handoff consumption

The handoff MUST carry pack, candidate, evidence, oracle and consumer pins, and a named fresh consumer MUST re-read them, use the data and read back its produced W1 artifact; it MUST refuse wrong pin, wrong scope and partial input.

#### Scenario: Wrong pin

- **WHEN** the handoff pack or oracle digest is altered
- **THEN** the consumer refuses before use and produces no output

#### Scenario: Partial input

- **WHEN** a required receipt or handoff section is missing
- **THEN** the consumer returns a typed partial refusal and does not acknowledge consumption

## ADDED Requirements

### Requirement: Receipt gate on the real W1 consumer path

The real W1 Consumer MUST confine the receipt locator to the consumer root, resolve a trusted expected receipt digest before reading, hash the receipt bytes, and only then parse and use the receipt. A failure MUST occur before checklist output or any downstream product effect.

#### Scenario: Single-byte receipt mutation

- **WHEN** a valid receipt copy is changed by one byte and the trusted expected digest is unchanged
- **THEN** the same W1 Consumer entry returns `RECEIPT_SHA_MISMATCH`, writes no checklist, and does not parse the receipt

#### Scenario: Outside receipt locator

- **WHEN** the receipt locator resolves outside the consumer root
- **THEN** the consumer returns `RECEIPT_LOCATOR_OUTSIDE` before reading the locator target, with zero outside read
