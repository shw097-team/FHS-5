# Design

## Context

The W0 pack already fixes the product scope: a Generic sample (`briefcheck`),
five parties (TPM+Reviewer, Guide, Bridge, Challenge, FAR), a local CODEX Native
OPS contract, and a 24+10 case plan. The existing candidate `5eab43d` has real
history (v1 red, v2 duplicate fix). The W1 Bridge reference
(`w1_bridge_reference.py`) exists and is reusable without modification.

## Goals / Non-Goals

**Goals:**
- Real executions with raw stdout/stderr and per-case pins.
- Role separation by process and git worktree, recorded as the same OS principal.
- Fail-closed behavior for path escape, missing child, false authority, oracle
  drift, stale raw, unavailable-as-zero and release claims.
- A W1 consumer that refuses a wrong pack pin.

**Non-Goals:**
- Full W1 38+28, C16/EC-36/local47, FARP30/local35 or U26/QA26 denominators.
- FHS 485 full regression (recorded `DEFER`).
- Different-principal independence, HERMES/GPT host execution or release.

## Decisions

1. **Reuse the W1 Bridge reference**, wrapped over a generated W0 package view
   with its own `SOURCE_MANIFEST.json` and `PACKAGE_FILE_MANIFEST.json`.
   Alternative: rewrite a W0 bridge; rejected because reuse is real and the
   four APIs are already implemented.
2. **Build minimal Guide/FAR/Challenge references.** They are small, auditable
   Python tools with explicit exits and JSON output. Alternative: use prose
   only; rejected because the pack forbids text-only claims.
3. **Stdlib `unittest` only.** No new dependency, no registry, no scheduler.
4. **The `12'` patch is a new commit** (`bb66a27`) on top of `5eab43d`, with a
   new preimage and a new retest. The v2 post-readback is not used as a
   prerequisite.
5. **Junction is tested; symlink is honestly `NOT_VERIFIED`.** Creating a
   symlink requires Developer Mode or elevation in this host; the receipt
   records the gap instead of asserting a pass.

## Risks / Trade-offs

- Same OS principal for maker and checker: mitigated by a separate process,
  separate worktree and a checker that hashes the subject before and after.
- 44 receipts do not mean the full product denominators; every receipt carries
  `not_covered` where applicable.
- The OFF parity is an import/behavior trace, not a full uninstall proof.
- A later change to the candidate or oracle invalidates these pins; the W1
  consumer refuses mismatches.
