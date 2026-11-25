# w1-nf-reader

## ADDED Requirements

### Requirement: Native six-file inspection

The reader SHALL inspect the six-file pack, verify the manifest, the five MD
digests, the twenty-six assets, the external seal and the identity, and SHALL
report counts, digest domains and a source audit.

#### Scenario: real pack

- **WHEN** the reader inspects the frozen W1 pack
- **THEN** it reports 5 pack files, 38 DEV, 29 OPS, 13 cases, 26 assets,
  42 sources and 14 holds, and the manifest digest equals the recorded pin

#### Scenario: tampered byte

- **WHEN** any pack file byte differs from the manifest
- **THEN** the reader rejects with DIGEST_MISMATCH

### Requirement: Body resolution

The resolver SHALL reject absolute, drive, UNC, dot-segment, link and reparse
paths, duplicate JSON keys, NaN constants, invalid UTF-8 and oversize files,
and SHALL verify that a file did not change between stat and read.

#### Scenario: path escape

- **WHEN** a relative path contains `..`, a drive letter or a UNC prefix
- **THEN** the resolver rejects without reading outside the pack root

### Requirement: Guide nine-key delta

The Guide SHALL produce all nine keys from real artefacts and SHALL return
DELTA_UNVERIFIED when a key or a period is missing or when only a caller
boolean is supplied.

#### Scenario: single changed key

- **WHEN** one key differs in the same subject and scope
- **THEN** the verdict is NEW_MATERIAL_EVIDENCE with that key listed
