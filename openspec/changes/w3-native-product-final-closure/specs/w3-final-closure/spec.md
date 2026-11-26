# w3-final-closure

## ADDED Requirements

### Requirement: Design and product evidence are separated
The system SHALL keep design-layer observations distinct from product-frozen
evidence and SHALL refuse to relabel design fixtures as product oracles.

#### Scenario: Product freeze without independent Case Owner
- **WHEN** only design fixtures and the same maker are available
- **THEN** the product freeze is refused and the product claim remains NOT_CLAIMED

### Requirement: Read-only W2 requalification
The system SHALL run the twelve W2 cases in isolated copies with real process
raw and a distinct checker without writing the W2 protected tree.

#### Scenario: Twelve-case read-only run
- **WHEN** the published W2 fixtures and oracles are frozen in a read-only copy
- **THEN** all twelve cases produce raw and the checker reports PASS

### Requirement: Honest W4 inbound
The system SHALL produce a W4 inbound with false readiness when the W3 product
validation is not established.

#### Scenario: Missing product validation
- **WHEN** W3 product cases are not validated
- **THEN** W4_TECHNICALLY_READY and W4_EXECUTION_READY are false
