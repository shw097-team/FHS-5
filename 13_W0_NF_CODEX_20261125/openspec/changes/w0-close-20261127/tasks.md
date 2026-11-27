# Tasks

## 1. Freeze and replay

- [x] 1.1 Confirm byte-exact source vs stale run-root contracts/oracle and record the root cause.
- [x] 1.2 Create a fresh `runs/w0_close_20261127/13` copy and materialise the candidate bundle at `bb66a27`.
- [ ] 1.3 Record the 41 reused same-position receipts and the affected set.

## 2. NF-T01

- [ ] 2.1 Remove reviewer double-fail acceptance and resolve the installed reviewer path.
- [ ] 2.2 Run real ON/OFF parity, import blocker controls and a forced-failure control.
- [ ] 2.3 Write the affected NF-T01 receipt/raw and rerun NF-T05 if the Bridge package changed.

## 3. NF-T08

- [ ] 3.1 Re-run TPM contracts, Guide with `--contracts`, Guide Resume, Bridge and Native context.
- [ ] 3.2 Prove pins/source/IDs match and `chain=COMBINED_OK`, negatives 9/9 typed rejections.
- [ ] 3.3 Run one live mutated-contract negative at the same entry and write the receipt/raw.

## 4. Consumer, G17, NF-T10

- [ ] 4.1 Add the shared receipt SHA gate and prove mutation refusal with zero downstream.
- [ ] 4.2 Run the 803-check consumer with T10 pending, finalise T10 from the current receipt, then consume again.
- [ ] 4.3 Run the fresh W1 minimal consumer POS and wrong pin/scope/partial NEGs with readback.

## 5. Checker and delivery

- [ ] 5.1 Independent checker reads frozen expected plus actual raw and emits a verdict.
- [ ] 5.2 Rebuild summary/evidence manifest/handoff from 41 reused plus new affected receipts.
- [ ] 5.3 Update W0 CLOSEOUT/HANDOFF/Actual ChangeSet, commit and read back the branch if authorised.