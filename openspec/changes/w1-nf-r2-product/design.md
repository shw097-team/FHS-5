# Design

## Context

W1 NF-r2 is a six-file pack (5 MD + strict JSON manifest) with an external
seal. The reader must never trust the pack path, never normalize CRLF, and
never turn a local read into a host or release claim.

## Decisions

1. `w1_nf_reader.py` stays untouched as the historical entry; `nf_reader.py`
   is the superset and is the only production entry.
2. Missing sources are recorded, never fabricated; a present source with the
   wrong bytes is a hard failure.
3. `body_resolver` is the single read path for the pack, so all TOCTOU, size
   and link checks apply once.
4. The nine Guide keys are produced by functions that read real artefacts; a
   caller boolean or a single evidence sha always yields DELTA_UNVERIFIED.

## Risks

- A real CODEX host session is not observable in this environment, so
  W1-HOST-01 stays NOT_OBSERVED and W1_NF_VALIDATED is not claimed.
