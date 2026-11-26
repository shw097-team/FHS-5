# W3 Product Case Set — Generic Native profile

**This is a NEW Generic Native product case set. It is not an original-domain oracle.**

Subject: `FHS-5_PLP/W3/CONTROL_PACK` · Scope: `W3-NF-01`
Owner: **separate Case Owner session** (independent of the Maker)
Frozen: `2026-11-26T18:54:10+08:00`
Contract: `03_W3_TQAEP.md` §03 (16 case contracts)
Claim ceiling: `GENERIC_NATIVE_PRODUCT_CASE_SET_ONLY` — **no product PASS is claimed.**

---

## 1. What is in this directory

| Path | Count | What it is |
|---|---:|---|
| `fixtures/<case>.json` | 16 | New `FHS5.PLP.W3.ProductFixture@2` inputs, built from real W3D run values |
| `oracles/<case>.json` | 16 | New `FHS5.PLP.W3.ProductOracle@2` expected token/exit + 3–6 named predicates |
| `CASE_OWNER_FREEZE.json` | 1 | SHA-256 of every fixture/oracle, design-pair digests, and the signed freeze statement |
| `README.md` | 1 | This file |

The design pair is **not** copied. `CASE_OWNER_FREEZE.json` records, per case,
that the new fixture, the new oracle, and the new `input` object all differ from
`C:\Projects\...\W3_FINAL_20261126T1827\pack\assets\{fixtures,oracles}\<case>.json`.
All three comparison flags are `true` for all 16 cases.

The design file `03_W3_TQAEP.md` was only read. Its `observed`/`verdict` fields
were not touched, and nothing under `C:\Projects` was written.

---

## 2. What is real

Every fixture `input` is derived from the actual W3D reference run, not invented:

- **Five real pins** from `evidence/W3D/FREEZE_LEDGER.json`:
  `source=fb3d2ead…9102`, `candidate=8b4b4068…d8d7`, `evidence=cb9bc39d…a903`,
  `oracle=686a2733…54f8`, `case_set=a33e2047…74a4`; plus `pack_manifest_sha256`
  `9c342519…96c4` and `package_tree_sha256` `96c4d3a4…bd08`.
- **Resolved path placeholders**: `<PACK_ROOT>` is resolved at run time; the
  reference run used `C:\Projects\Agent_Workspace\FHS-5_Workspace\W3_FINAL_20261126T1827`.
  Every case-specific path (`pos_neg_child.py`, `raw_POS`/`raw_NEG`, `far_01/*`,
  `TEST_RESULTS`, `canary.txt`) points at the real evidence path.
- **Real counts**: 5 frozen mutations, 4 run defects, 2 providers / 5 FAR
  states, 6
  count periods (`276,275,317,316,318,319`), 192 enumerated files, 3 files in
  `REACHABLE_EMPTY`, 13/13 ACL observations, 79611 generic-read bytes, 2
  alternatives, 2 findings, 12/12 W2 requalified rows.
- **Real mutation names**: `FLOATING_HEAD`, `OLD_CANDIDATE_RAW`,
  `WRONG_SOURCE_PIN`, `SCOPE_DRIFT`, `ORACLE_SWAP`.
- **Real defect names**: `RUNNER_NULL`, `FAKE_SUMMARY`, `MISSING_RAW`,
  `CHANGED_RAW`.
- **Real artefacts**: canary `canary-v1` (SHA-256
  `d6e1d370f7f9cdf8028eebca911681300411553d4b314bcd8f31d5f4aaf5996e`
  recorded in the fixture), findings `F3-W3D-01` (P1
  security/authorization) and `F3-W3D-02` (P2 data consumption), and the
  `W3_PARTIAL_UPSTREAM` candidate state.

`provenance.reference_record_sha256` in each fixture is the real
`raw_sha256` of that case's `record.json`, so the input can be traced back to a
specific observed record.

## 3. What is frozen, and in what order

The **expected** value is the token from `03_W3_TQAEP.md` §03, the exit
semantics, and 3–6 named predicates. It was frozen at `2026-11-26T18:54:10+08:00`
**before this product run**, from the contract text — not from the reference
run's verdict.

Reference-run facts (counts, states, exits) appear under
`input.reference_run_facts` and are labelled provenance. They are inputs to the
product run, not its oracle. A future product runner must produce its own
`observed`, and every predicate must hold on that new record.

The predicates are semantic and checkable from a case record / the real world,
for example:

`five_pins_present_and_distinct`, `pins_reopen_freeze_ledger`,
`pack_tree_unchanged`, `separate_fields_present`, `source_bytes_unchanged`,
`zero_writes`, `runner_not_invoked`, `absent_rows_null`,
`unavailable_is_not_zero`, `no_park`, `canary_unchanged`, `pos_exit_zero`,
`neg_exit_two`, `no_fabricated_bytes`, `observation_layer_not_raised`.
A token match alone never satisfies an oracle.

## 4. The 16 cases

| # | Case | Kind | Contract token | Exit | Generic Native input anchor |
|---:|---|---|---|---:|---|
| 1 | `W3-FRZ-01` | POS | `FREEZE_LEDGER_VERIFIED` | 0 | 5 real pins + ledger + pack tree |
| 2 | `W3-FRZ-02` | NEG | `FROZEN_IDENTITY_MISMATCH` | 2 | 5 real mutation names |
| 3 | `W3-RUN-01` | POS | `SEMANTIC_MATCH` | 0 | real POS/NEG child + 2 raw roots |
| 4 | `W3-RUN-02` | NEG | `UNREPRODUCED` | 2 | 4 real defect names |
| 5 | `W3-FAR-01` | NEG | `UNAVAILABLE` | 2 | `ABSENT_DB` + `REACHABLE_EMPTY(3)` |
| 6 | `W3-FAR-02` | POS | `ALTERNATIVES_SUBSTANTIVE` | 0 | 2 alternatives + 2 findings |
| 7 | `W3-G2-01` | NEG | `DELTA_UNVERIFIED` | 2 | 1 period + 1 evidence SHA |
| 8 | `W3-CHK-01` | NEG | `FALSE_AUTHORITY` | 2 | advisory PASS + 2 refused writes |
| 9 | `W3-R3-01` | POS | `NOT_COVERED` | 0 | `743c6cf` / `80833a5f` identity |
| 10 | `W3-R3-02` | NEG | `DELTA_UNVERIFIED` | 2 | 6 real count periods |
| 11 | `W3-R3-03` | POS | `ZERO_RELEVANT_HIT` | 0 | `TEST_RESULTS` / 192 files / 0 rows |
| 12 | `W3-R3-04` | NEG | `FALSE_INDEPENDENT` | 2 | self-check `22/22`, same process |
| 13 | `W3-R3-05` | POS | `ALTERNATIVES_SUBSTANTIVE` | 0 | 2 designation alternatives |
| 14 | `W3-R3-06` | NEG | `ORIGINAL_READER_UNBOUND` | 2 | ACL `13/13`, 79611 bytes |
| 15 | `W3-FR16-01` | NEG | `WRITE_SCOPE_VIOLATION` | 2 | 4-target write set + canary |
| 16 | `W3-FR17-01` | NEG | `FALSE_AUTHORITY` | 2 | FAR + 3 refused effects |

Exit semantics are explicit in each oracle: POS needs child exit 0 **and** the
token **and** every predicate; NEG needs child exit 2 **and** the token **and**
zero side effects. The engine-wrapper `exit=0` is never accepted as a refusal.

## 5. What remains NotCovered

This set is a **Generic Native projection**. It does not become an original-domain
oracle and does not validate W3:

- **Product runner / Host ABI**: UNBOUND. No product process was run; `exit` is
  the contract placeholder corroborated only by the reference child exit.
- **No independent Checker**: `W3-CHK-01` and `W3-R3-04` freeze the refusal
  shape only; no protected Checker signer exists, so `INDEPENDENT_PASS` stays false.
- **No original-domain cases**: the EC/FAR/Challenge/Guide/Bridge/TPM original
  families were not re-produced. `W3-FAR-01`/`W3-FAR-02` use a local Generic
  provider, not Fabric/ResearchWO.
- **Five-pin preimages**: the design `oracle` and `case_set` pins remain
  `PROPOSED_DESIGN_*`; the real product freeze is not re-signed here.
- **W2 upstream is PARTIAL**: `W2_NF_VALIDATED=false`, protected
  writer/gate/marker remains `BLOCKED_NOT_ADMITTED`, `W2-R3-*` are read-only
  requalified rows.
- **Open mutant findings**: `F3-W3D-01` (P1: guard removed, write allowed) and
  `F3-W3D-02` (P2: absent provider collapsed to zero) are recorded, not fixed.
- **Missing original bytes / raw**: `W3-R3-01` (CH-07), `W3-R3-02` (two-period
  WorldReader raw), `W3-R3-03` (192-file historical raw), `W3-R3-06` (original
  Source Owner/Reader) remain missing or single-period.
- **No product PASS**: `W3_NF_VALIDATED`, `W3_TECHNICALLY_READY`,
  `W3_EXECUTION_READY`, `RELEASED` are all `false` in the reference run. This
  set changes none of that.

## 6. How to verify

```powershell
$d = 'C:\Users\user\Documents\Codex\2026-11-26\new-chat-7\work\product_case_owner'
# 16 + 16
(Get-ChildItem "$d\fixtures\*.json").Count
(Get-ChildItem "$d\oracles\*.json").Count
# Recompute the freeze digests and compare
Get-ChildItem "$d\fixtures\*.json","$d\oracles\*.json" | ForEach-Object {
  $h = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower()
  "{0}  {1}" -f $h, $_.Name
}
```

Each oracle has 3–6 predicates, each with an `id`, an `assertion` and a
`verify` expression over `record.*`. The freeze file lists every digest and
states that expected was frozen before the product run.
