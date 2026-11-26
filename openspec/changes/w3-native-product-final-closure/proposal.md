# W3 native product final closure

## Why

The prior run delivered a design-layer engine but no product freeze, no W2
requalification and no W4 inbound. This change records the final-closure
attempt, the real W2 read-only requalification, and the governance blocker that
prevents relabelling design fixtures as product oracles.

## What Changes

- Requalify the 12 W2 cases read-only against real isolated repo/process raw.
- Record the W3 16-case design evidence and the rejected product-freeze attempt.
- Produce an F1-F5 closure ledger, coverage matrix and W4 inbound.
- Keep W2_NF_VALIDATED, W3_NF_VALIDATED, INDEPENDENT_PASS, W4 readiness and
  RELEASED explicitly NOT_CLAIMED.

## Impact

- Affected specs: w3-final-closure (new)
- Code: W2/impl, W2/check, W3/impl, W3/check, W4/check
- Not affected: adopted W3 r2 pack bytes, W2 protected writer/gate/marker
