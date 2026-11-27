# Design

## Root cause

The committed W0 source and frozen oracle are byte-exact (contract `pi.json` 1477 bytes, `43ea6ea2...`; oracle `112f2902...`). The G3 `runs/w0_full/13` copy contains LF-normalised contracts (1330 bytes) and a regenerated oracle (`31dc70b0...`), so Guide pins, `source_manifest_match`, `thin_resume.oracle_sha` and the collaboration chain are stale relative to the copy. The 41 PASS receipts remain same-position; NF-T01/07/08/10 are the affected receipts and the other 40 are reused. NF-T05 is byte-identical and reused.

## Decisions

1. Rebuild the affected evidence in a fresh `runs/w0_close_20261127/13` copy from the byte-exact committed source and a bundle clone at `bb66a27`; never edit the sealed pack or the old delivery.
2. Preserve `05_TQAEP/oracle.json` bytes and the 40 unaffected receipts. Rerun only NF-T01, NF-T07, NF-T08 and NF-T10; NF-T05 is reused byte-identical; reuse the same-position DEV/FAR/Challenge artifacts.
3. Make the reviewer double-fail a negative control. A double failure may not be counted as parity success; a failed reviewer positive makes NF-T01 FAIL.
4. G17 and NF-T10 share `consumer.py --verify-receipt`: SHA is checked from raw bytes before JSON parse, git, CLI or downstream reads. A marker proves the positive path reached downstream and the mutated path did not.
5. NF-T10 is staged: other required cases PASS, consumer runs with `--allow-pending-t10`, the real receipt finalises NF-T10, then a second fresh consumer consumes the final delivery. The finalizer takes the current run/receipt explicitly and refuses stale IDs.
6. The independent checker reads frozen expected plus actual raw in a separate process/worktree; same-principal separation is stated as a claim ceiling, not a different-principal claim.

## Evidence reuse

The 40 unaffected receipts keep their original candidate `bb66a27`, oracle `112f2902...`, pack `e3772aee...` and raw. New receipts use new run IDs and raw under the fresh run root. `summary.json` is rebuilt from the 40 reused plus the new affected receipts; it is not the old 44/44 summary.

## Claim ceiling

This change closes only the current W0 blockers. It does not claim W1-W4 completion, different-principal signatures, other hosts, release or the complete FHS-5 MVP.

## G17 main-path wiring

The standalone `consumer.py --verify-receipt` gate remains a component test. The real G17 POS/NEG path is the full `w1_min_consume.py` entry: handoff pins -> confined receipt locator -> trusted expected digest -> bytes SHA -> parse -> receipt pins/verdict -> 44-item checklist/readback. The expected digest is an explicit pin or the delivery's `CONSUMER_MANIFEST`; the mutated receipt cannot supply its own expected. The locator is confined to `07_CONSUMER` before `is_file`/read, so an outside path is refused before content access.
