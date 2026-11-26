# w3-product-harness

## ADDED Requirements

### Requirement: Isolated W3 product execution
The system SHALL execute the sixteen W3 design cases as separate processes
inside an isolated run root and SHALL record argv, exit, stdout, stderr and the
observed token for each case.

#### Scenario: All design cases execute
- **WHEN** the adopted pack verifies and the run root is isolated
- **THEN** all sixteen cases produce a record and the frozen pack bytes are unchanged

#### Scenario: Product overclaim is refused
- **WHEN** a case has only a design oracle
- **THEN** the product case state remains NOT_COVERED and W3_NF_VALIDATED is not claimed

### Requirement: Typed FAR states
The system SHALL distinguish HIT, ZERO_RELEVANT_HIT, UNAVAILABLE,
BLOCKED_BY_AUTHORITY and ERROR, and SHALL NOT report an unreachable provider as
zero.

#### Scenario: Absent provider
- **WHEN** a provider root does not exist
- **THEN** the state is UNAVAILABLE with null rows and null zero_results

### Requirement: Advice is not a grant
The system SHALL use only the ten original advice names, SHALL provide at least
two substantive alternatives per decision finding, and SHALL record
advice_is_grant=false.

#### Scenario: Single alternative
- **WHEN** fewer than two alternatives are supplied
- **THEN** the decision is refused with ALTERNATIVE_INSUFFICIENT
