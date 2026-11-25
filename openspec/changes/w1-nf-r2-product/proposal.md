# W1 NF-r2 product entry

## Why

The W1 control pack (`W1-NF-r2-CODEX-PRIMARY`) was validated only at the
document layer. The product entry (reader, bridge, guide, TPM, consumer,
case runner) existed only as a partial D2 skeleton with 16 reader tests and no
case run, no consumer, and no closeout/handoff.

## What Changes

- Add `W1/impl/nf_reader.py` as the production reader with a field-level
  legacy-15 to NF ABI crosswalk, explicit digest domains and a clause index.
- Add `W1/impl/body_resolver.py` with path containment, strict JSON, bounded
  sizes and a stat/read/stat TOCTOU check.
- Add `W1/impl/bridge_nf.py` with the four Bridge APIs over full clause bodies.
- Add `W1/impl/guide_nf.py` with the four original Guide functions, two modes
  and a nine-key dual-period verifier driven by real producers.
- Add `W1/impl/tpm_contracts_nf.py` with five views on one work identity and a
  read-only eight-column reviewer.
- Add `W1/impl/w1_consumer.py`, `W1/impl/host_facade.py` and
  `W1/check/run_cases_nf.py`.
- Add six test modules covering POS and NEG per API.

## Impact

- Affected specs: w1-nf-reader
- Affected code: W1/impl, W1/check
- No change to the frozen six-file pack, W0, or upstream volumes.
