# Tasks

## 1. Freeze and replay

- [x] 1.1 Confirm byte-exact source vs stale run-root contracts/oracle and record the root cause.
- [x] 1.2 Create a fresh `runs/w0_close_20261127/13` copy and materialise the candidate bundle at `bb66a27`.
- [x] 1.3 Record the 40 reused same-position receipts and the affected set.

## 2. NF-T01

- [x] 2.1 Remove reviewer double-fail acceptance and resolve the installed reviewer path.
- [x] 2.2 Run real ON/OFF parity, import blocker controls and a forced-failure control.
- [x] 2.3 Write the affected NF-T01 receipt/raw and rerun NF-T05 if the Bridge package changed.

## 3. NF-T08

- [x] 3.1 Re-run TPM contracts, Guide with `--contracts`, Guide Resume, Bridge and Native context.
- [x] 3.2 Prove pins/source/IDs match and `chain=COMBINED_OK`, negatives 9/9 typed rejections.
- [x] 3.3 Run one live mutated-contract negative at the same entry and write the receipt/raw.

## 4. Consumer, G17, NF-T10

- [x] 4.1 Add the shared receipt SHA gate and prove mutation refusal with zero downstream.
- [x] 4.2 Run the 803-check consumer with T10 pending, finalise T10 from the current receipt, then consume again.
- [x] 4.3 Run the fresh W1 minimal consumer POS and wrong pin/scope/partial NEGs with readback.

## 5. Checker and delivery

- [x] 5.1 Independent checker reads frozen expected plus actual raw and emits a verdict.
- [x] 5.2 Rebuild summary/evidence manifest/handoff from 40 reused plus new affected receipts.
- [x] 5.3 Update W0 CLOSEOUT/HANDOFF/Actual ChangeSet, commit and read back the branch if authorised.
## 6. Closeout evidence

- [x] 6.1 Content commit `f173214428f1d3b4ea3819182ddb8a6a67cc34f1`; final consumer `20261127T230849-a4b187dd` (811 checks); evidence `5307b70c…`; G17/W1 minimal PASS.
- [x] 6.2 C/H `G3_20261127/CLOSEOUT_W0.md`／`HANDOFF_W0.md`；push 未回讀前不宣成功。


## 7. G17 true consumer entry

- [x] 7.1 Confine the receipt locator to `07_CONSUMER` before any `is_file`/read in `w1_min_consume.py`.
- [x] 7.2 Resolve the expected receipt digest from an explicit pin or `CONSUMER_MANIFEST`, then hash the bytes before parse.
- [x] 7.3 Parse/use the verified receipt on the real W1 Consumer path and generate the 44-item checklist with readback.
- [x] 7.4 Same-entry single-byte NEG returns `RECEIPT_SHA_MISMATCH` with zero checklist/output.
- [x] 7.5 Outside locator returns `RECEIPT_LOCATOR_OUTSIDE` before content read; audit shows zero outside read.
- [x] 7.6 P8 final consumer / W1 consume / G17 full suite recorded; C/H and INDEX updated.
