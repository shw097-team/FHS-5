# FHS-5_PLP W1 — Author Control Pack, Execution Evidence, and Reference Adapter

This is the owner-authorized **public reference export** of the FHS-5_PLP W1 execution.
It is a **local author execution with named original-domain holds**, not Original Acceptance.

## Status

| Field | Value |
|---|---|
| subject_id | `FHS-5_PLP/W1/CONTROL_PACK` |
| selection_id | `W1-PRIMARY-SEL-20261124-01` |
| repair_id | `W1-PRIMARY-REPAIR-20261124-02` |
| claim ceiling | `AUTHOR_DESIGN_ONLY` |
| execution claim | `AUTHOR_LOCAL_EXECUTION_ONLY` |
| self-acceptance | `AUTHOR_LOCAL_EXECUTION_COMPLETE_WITH_14_NAMED_HOLDS` |
| original Reader / Issuer / Host / Runner / Checker / Publisher | `UNBOUND` |

## Start here

1. `evidence/W1_EXECUTION_REPORT.md` — S0–S6, harness loop, ECP/TQAEP result.
2. `evidence/10_W1_ECP_TQAEP_CLOSURE_MATRIX.json` — 67 ECP items and 13 TQAEP cases.
3. `evidence/11_W1_SELF_ACCEPTANCE.json` — local self-acceptance.
4. `evidence/12_W1_NAMED_HOLDS.json` — 14 original-domain holds.
5. `primary/` — 15 normative files + 16 sources + 13 fixtures + 13 oracles + inventory.
6. `impl/w1_bridge_reference.py` — executable author reference adapter (22/22 self-checks).

## Verification snapshot

| Check | Result |
|---|---|
| normative files | 15/15 |
| sources | 16/16 pack pins; 14 direct + 2 relocated originals verified |
| cases | 13/13 with fixture/oracle; 9 local rule pass, 1 reference-impl pass, 1 inspect pass, 2 host HOLD |
| harness | 17/17 mutants rejected |
| reference adapter | 22/22 checks pass |
| WP dry-consume | 6/6 accounted |
| host grid | 21/21 cells accounted; 0 consumed |
| Hermes children | 3/3 accounted; 0 observed |
| delivery audit | 28/28 checks pass |
| ECP closure | 67/67 accounted; author-local open = 0 |

## What is not claimed

`PI_READY`, `PD_BOUND`, `EXECUTION_ADMITTED`, `NATIVE_PASS`, `INDEPENDENT_PASS`, `RELEASED`, `MISSION_COMPLETE` are **not claimed**.

The following remain original-domain holds:

- Host install/register/bind/invoke/served/consumed Raw.
- Original 17 Guide, 66 Bridge, and 24 W0 cases.
- Original Reader, Runner, Protected Checker and Publisher.
- W0-A owner designation and W0-B admission.
- CH-07 old-byte recovery.
- W2–W4 construction.

## Public-export hygiene

- No credential or token is included.
- Local raw logs and ACL/principal records are not included.
- Execution summaries have absolute local roots replaced by labels such as `<WORKSPACE>` and `<PRIMARY_ROOT>`.
- `primary/SOURCE_MANIFEST.json` retains authoring-local `original_path` provenance, as in the W0 public export; these values are provenance only.
- The local full-delivery ZIP and `DELIVERY_SEAL.json` are not published because they embed local raw evidence.

See `PUBLIC_SCOPE.json` for the included/excluded list and redaction counts.

## Reproduce the public checks

From the repository root:

```powershell
python W1/check/replay_hashes.py --root W1/primary
python W1/check/w1_guard.py --pack-root W1/primary --delivery-root W1
python W1/check/m22_guard_ref.py check-pack --pack-root W1/primary
python W1/check/run_cases.py --pack-root W1/primary --out W1/evidence/raw
python W1/check/run_harness.py
```

`run_harness.py` derives its paths from `W1/check`, so it runs against `W1/primary`.
