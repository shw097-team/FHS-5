# Design

## Context

The candidate `bb66a27` is stable. The gaps are in assurance tooling and
evidence, not product bytes. Windows lacks `SeCreateSymbolicLink`; WSL2
Ubuntu-24.04 with Python 3.12 is available and non-root.

## Goals / Non-Goals

**Goals:** real chain consumption, fail-closed consumer, real symlink and OFF.

**Non-Goals:** W1–W4 denominators, other hosts, different principal, release.

## Decisions

1. **Stage the consumer/checker loop**: NF-T10 is `PENDING_CONSUMER` during the
   checker; the consumer finalizes it. Checker pins exclude NF-T10 so the
   post-checker receipt cannot invalidate them.
2. **Evidence manifest claims are derived** from receipts, challenge, collab,
   security and OFF. W1 readiness lives in the separate Consumer Manifest to
   avoid a hash cycle.
3. **Symlink test runs on WSL2 ext4**, not a mock; Windows junction remains a
   separate case. No privilege or ACL change.
4. **OFF uses an import blocker** (`sitecustomize`) with positive/negative
   controls, and FAR OFF applies the real `12'` diff to an isolated v2 clone.

## Risks / Trade-offs

- Same OS principal for checker/consumer; recorded.
- NF-T10 is consumer-finalized by design; checker explicitly excludes it.
- The FAR-OFF patch is LF-normalized; content is byte-identical after
  normalization and the source hash is recorded.
