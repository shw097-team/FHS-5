# W1 CLOSURE MATRIX

- pack_manifest_sha256: `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`
- rows: 118

| COVERED_BY_SHARED_OPERATION | 62 |
| DEFERRED | 3 |
| EVIDENCED | 17 |
| EVIDENCED_WITH_DEFERRED_HOSTS | 1 |
| EXERCISED_INDIVIDUALLY | 2 |
| HOLD_PRESERVED_NOT_CLOSED | 14 |
| NOT_APPLICABLE_THIS_ROUND | 1 |
| PASS | 18 |

| ID | Child | Applicable | Operation | Evidence | Verdict |
|---|---|---|---|---|---|
| `P01` | - | True | identity/pins/dag consume | evidence/inspect.json | EVIDENCED |
| `P02` | - | True | ABI crosswalk + loss ledger | evidence/raw/N02.json | EVIDENCED |
| `P03` | - | True | reader/bridge/guide/TPM build | evidence/raw/N03.json | EVIDENCED |
| `P04` | - | True | real CODEX host served/consumed | evidence/host/host_receipt.json | EVIDENCED |
| `P05` | - | True | 13 cases + subcases + NEG | evidence/cases.json | EVIDENCED |
| `P06` | - | True | closure matrix + seal + handoff | evidence/how_to/independent_check.json | EVIDENCED |
| `DEV-ADP-01` | - | True | guide advice never a grant | evidence/raw/N03.json | COVERED_BY_SHARED_OPERATION |
| `DEV-ADP-02` | - | True | bridge read-only (wrote_bytes=0) | evidence/raw/N02.json | COVERED_BY_SHARED_OPERATION |
| `DEV-ADP-03` | - | True | body resolver strict parse + span | evidence/raw/N10.json | COVERED_BY_SHARED_OPERATION |
| `DEV-ADP-04` | - | True | host facade anti-upgrade | evidence/raw/N04.json | COVERED_BY_SHARED_OPERATION |
| `DEV-APP-01` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-EFF-01` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-IDEM-01` | - | True | idempotent writes + LastGood + reverse patch | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `DEV-IDEM-02` | - | True | idempotent writes + LastGood + reverse patch | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `DEV-IDEM-03` | - | True | idempotent writes + LastGood + reverse patch | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `DEV-OP-01` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-OP-02` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-OP-03` | - | True | exact writeset + POS/NEG APIs + raw per run_id + consumer re | evidence/raw/N04.json | COVERED_BY_SHARED_OPERATION |
| `DEV-OP-04` | - | True | exact writeset + POS/NEG APIs + raw per run_id + consumer re | evidence/raw/N04.json | COVERED_BY_SHARED_OPERATION |
| `DEV-OP-05` | - | True | exact writeset + POS/NEG APIs + raw per run_id + consumer re | evidence/raw/N04.json | COVERED_BY_SHARED_OPERATION |
| `DEV-OP-06` | - | True | exact writeset + POS/NEG APIs + raw per run_id + consumer re | evidence/raw/N04.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PERM-01` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-POST-01` | - | True | digest domains + identity + outside canary | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-POST-02` | - | True | asset pins + claim ledger | evidence/cases.json | COVERED_BY_SHARED_OPERATION |
| `DEV-POST-03` | - | True | digest domains + identity + outside canary | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-POST-04` | - | True | asset pins + claim ledger | evidence/cases.json | COVERED_BY_SHARED_OPERATION |
| `DEV-POST-05` | - | True | digest domains + identity + outside canary | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PRE-01` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PRE-02` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PRE-03` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PRE-04` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PRE-05` | - | True | nf_reader.inspect_package + evidence/inspect.json | evidence/inspect.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PROH-01` | - | True | no-write checker + canary + abi_guard + recovery kind | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PROH-02` | - | True | no-write checker + canary + abi_guard + recovery kind | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PROH-03` | - | True | no-write checker + canary + abi_guard + recovery kind | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-PROH-04` | - | True | no-write checker + canary + abi_guard + recovery kind | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-RB-01` | - | True | guard/readback/replay/independent checker | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-RB-02` | - | True | guard/readback/replay/independent checker | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-RB-03` | - | True | guard/readback/replay/independent checker | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-RB-04` | - | True | guard/readback/replay/independent checker | evidence/how_to/independent_check.json | COVERED_BY_SHARED_OPERATION |
| `DEV-WS-01` | - | True | guide_nf.inspect_guide_request / render_thin_prompt | evidence/raw/N03.json | COVERED_BY_SHARED_OPERATION |
| `DEV-WS-02` | - | True | bridge_nf.explain_slice + compare_context | evidence/raw/N02.json | COVERED_BY_SHARED_OPERATION |
| `DEV-WS-03` | - | True | body_resolver.resolve_body/parse_clauses | evidence/raw/N10.json | COVERED_BY_SHARED_OPERATION |
| `DEV-WS-04` | - | True | host_facade + run_host_nf real host run | evidence/host/host_receipt.json | EXERCISED_INDIVIDUALLY |
| `OPS-APP-01` | - | True | host probe + effect tokens | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-CON-01` | - | True | GPT CHAT not observed | evidence/host/host_receipt.json | NOT_APPLICABLE_THIS_ROUND |
| `OPS-CON-02` | - | True | CODEX real invoke/serve/consume | evidence/host/host_receipt.json | EXERCISED_INDIVIDUALLY |
| `OPS-CON-03` | - | True | Hermes three children deferred | evidence/host/host_receipt.json | DEFERRED |
| `OPS-EFF-01` | - | True | host probe + effect tokens | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-OP-01` | - | True | native entry, no install; loaded sha | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-OP-02` | - | True | native entry, no install; loaded sha | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-OP-03` | - | True | bind/invoke/serve/consume with real argv and readback | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-OP-04` | - | True | bind/invoke/serve/consume with real argv and readback | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-OP-05` | - | True | bind/invoke/serve/consume with real argv and readback | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-OP-06` | - | True | bind/invoke/serve/consume with real argv and readback | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-POST-01` | - | True | stage ledger + evidence class + consumer split | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-POST-02` | - | True | stage ledger + evidence class + consumer split | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-POST-03` | - | True | stage ledger + evidence class + consumer split | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-POST-04` | - | True | Hermes child rows | evidence/host/host_receipt.json | DEFERRED |
| `OPS-POST-05` | - | True | stage ledger + evidence class + consumer split | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-PRE-01` | - | True | host probe + effect tokens | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-PRE-02` | - | True | host probe + effect tokens | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-PRE-03` | - | True | host probe + effect tokens | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-PRE-04` | - | True | host probe + effect tokens | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-PRE-05` | - | True | host probe + effect tokens | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-RB-01` | - | True | container/host readback | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-RB-02` | - | True | container/host readback | evidence/host/host_receipt.json | COVERED_BY_SHARED_OPERATION |
| `OPS-REC-01` | - | True | no install; uninstall n/a; restore by reverse patch; unknown | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `OPS-REC-02` | - | True | no install; uninstall n/a; restore by reverse patch; unknown | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `OPS-REC-03` | - | True | no install; uninstall n/a; restore by reverse patch; unknown | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `OPS-REC-04` | - | True | no install; uninstall n/a; restore by reverse patch; unknown | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `OPS-RESUME-01` | - | True | stop scope + typed resume | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `OPS-STOP-01` | - | True | stop scope + typed resume | evidence/raw/N11.json | COVERED_BY_SHARED_OPERATION |
| `W1-HOST-01` | - | True | run_cases_nf case W1-HOST-01 | evidence/raw/W1-HOST-01.json | PASS |
| `W1-HOST-02` | - | True | run_cases_nf case W1-HOST-02 | evidence/raw/W1-HOST-02.json | PASS |
| `W1-HOST-03` | - | True | run_cases_nf case W1-HOST-03 | evidence/raw/W1-HOST-03.json | PASS |
| `W1-HERMES-01` | - | True | run_cases_nf case W1-HERMES-01 | - | DEFERRED |
| `W1-ABI-01` | - | True | run_cases_nf case W1-ABI-01 | evidence/raw/W1-ABI-01.json | PASS |
| `W1-ABI-02` | - | True | run_cases_nf case W1-ABI-02 | evidence/raw/W1-ABI-02.json | PASS |
| `W1-SEC-01` | - | True | run_cases_nf case W1-SEC-01 | evidence/raw/W1-SEC-01.json | PASS |
| `W1-API-01` | - | True | run_cases_nf case W1-API-01 | evidence/raw/W1-API-01.json | PASS |
| `W1-R3-01` | - | True | run_cases_nf case W1-R3-01 | evidence/raw/W1-R3-01.json | PASS |
| `W1-R3-02` | - | True | run_cases_nf case W1-R3-02 | evidence/raw/W1-R3-02.json | PASS |
| `W1-R3-03` | - | True | run_cases_nf case W1-R3-03 | evidence/raw/W1-R3-03.json | PASS |
| `W1-R3-04` | - | True | run_cases_nf case W1-R3-04 | evidence/raw/W1-R3-04.json | PASS |
| `W1-R3-05` | - | True | run_cases_nf case W1-R3-05 | evidence/raw/W1-R3-05.json | PASS |
| `SUBCASE-N01` | N01 | True | run_cases_nf subcase N01 | evidence/raw/N01.json | PASS |
| `SUBCASE-N02` | N02 | True | run_cases_nf subcase N02 | evidence/raw/N02.json | PASS |
| `SUBCASE-N03` | N03 | True | run_cases_nf subcase N03 | evidence/raw/N03.json | PASS |
| `SUBCASE-N04` | N04 | True | run_cases_nf subcase N04 | evidence/raw/N04.json | PASS |
| `SUBCASE-N10` | N10 | True | run_cases_nf subcase N10 | evidence/raw/N10.json | PASS |
| `SUBCASE-N11` | N11 | True | run_cases_nf subcase N11 | evidence/raw/N11.json | PASS |
| `W1-A01` | - | True | source audit + identity | evidence/inspect.json | EVIDENCED |
| `W1-A02` | - | True | full clause body + span | evidence/raw/N02.json | EVIDENCED |
| `W1-A03` | - | True | seven-stage host ledger | evidence/host/host_receipt.json | EVIDENCED |
| `W1-A04` | - | True | field-level ABI fidelity | evidence/inspect.json | EVIDENCED |
| `W1-A05` | - | True | split counts + DAG | evidence/inspect.json | EVIDENCED |
| `W1-A06` | - | True | claim ceiling audit | evidence/how_to/independent_check.json | EVIDENCED |
| `W1-CODEX-01` | - | True | TPM/Guide/Bridge/consumer read | evidence/raw/N01.json | EVIDENCED |
| `W1-CODEX-02` | - | True | nine-key dual period | evidence/raw/N03.json | EVIDENCED |
| `W1-CODEX-03` | - | True | four bridge APIs full body | evidence/raw/N02.json | EVIDENCED |
| `W1-CODEX-04` | - | True | five views same identity | evidence/raw/N01.json | EVIDENCED |
| `W1-CODEX-05` | - | True | second package same ABI | evidence/raw/W1-CODEX-05.json | EVIDENCED |
| `W1-CODEX-06` | - | True | multi-host accounting | evidence/host/host_receipt.json | EVIDENCED_WITH_DEFERRED_HOSTS |
| `W1_HOST_NINE_GRID` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `W1_PLUGIN_ALIAS` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `W1_ABI_BOUND` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `W1_W0_INPUT` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `W0_PRIMARY_RECEIPT_STALE` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `W0-A_CASE_SELECTION` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `W0-B_NOT_ADMITTED` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `ORIGINAL_READER_UNBOUND` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `ORACLE_FIXTURE_UNBOUND` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `HOST_CAPABILITY_UNBOUND` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `CHECKER_PUBLISHER_UNBOUND` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `SOURCE_REFERENCE_HASH_CONFLICT` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
| `HOLD_CR-DOC04-STATE-MAP` | - | True | named HOLD preserved | control_pack/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md | HOLD_PRESERVED_NOT_CLOSED |
