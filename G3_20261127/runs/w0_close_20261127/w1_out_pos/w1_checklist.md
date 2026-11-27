# W0 -> W1 minimal consume checklist

- generated_at: `2026-11-27T15:09:06+00:00`
- scope: `FHS-5_PLP/W0`
- pack_manifest_sha256: `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- candidate_commit: `bb66a276aae8c5d6aef549832c523587fc47d247`
- oracle_sha256: `112f2902656f1122720ef275ac954e3422f896267f144f27d321fa138be382c6`
- evidence_manifest_sha256: `5307b70ce521e90fcbea79cbccf5cc2bfad3228f59a2a5fce1aa6228cbf8e7da`
- cases: 44

## next_legal_action

W1 以本 pins 為基線 requalify 14 HOLD／R3-CR，先做來源與 W1M 差額，不重跑 W0；W1 產品施工另需上位採納與 W1M／下一包一致。

## items

| case | kind | expected first_fail | w0 verdict | receipt sha (12) | raw refs |
|---|---|---|---|---|---|
| `SAMPLE-R1` | SAMPLE | `-` | PASS | `d1481de39514` | - |
| `SAMPLE-R2` | SAMPLE | `-` | PASS | `0afe72d2794e` | - |
| `SAMPLE-R3` | SAMPLE | `-` | PASS | `e938cfbaf7d4` | - |
| `SAMPLE-R5` | SAMPLE | `-` | PASS | `9c3715fc1dbe` | - |
| `SAMPLE-R6` | SAMPLE | `-` | PASS | `22208d571a39` | - |
| `SAMPLE-R7` | SAMPLE | `-` | PASS | `6f2dc4865715` | - |
| `SAMPLE-R8` | SAMPLE | `-` | PASS | `5f1f29a2623c` | - |
| `SAMPLE-R9` | SAMPLE | `-` | PASS | `adb789cac900` | - |
| `SAMPLE-R10` | SAMPLE | `-` | PASS | `25d384d1df3a` | - |
| `SAMPLE-R4` | SAMPLE | `-` | PASS | `62205659f9dd` | `SAMPLE-R4.observed.json` |
| `F5-W0-T01` | POS | `SOURCE_IDENTITY` | PASS | `03dcc70fe803` | `F5-W0-T01.observed.json` |
| `F5-W0-T02` | NEG | `SOURCE_INTEGRITY_FAILED` | PASS | `d09a4d8b070b` | `F5-W0-T02.observed.json` |
| `F5-W0-T03` | NEG | `REQUIRED_CHILD_MISSING` | PASS | `14d39c4a9c18` | - |
| `F5-W0-T04` | NEG | `FALSE_AUTHORITY` | PASS | `6f88cf981b63` | `F5-W0-T04.meta.json`, `F5-W0-T04.observed.json`, `F5-W0-T04.stderr.txt`, `F5-W0-T04.stdout.txt` |
| `F5-W0-T05` | NEG | `GUIDE_SCOPE_DRIFT` | PASS | `93ac2bd6792e` | `F5-W0-T05.meta.json`, `F5-W0-T05.observed.json`, `F5-W0-T05.stderr.txt`, `F5-W0-T05.stdout.txt` |
| `F5-W0-T06` | SEC | `BRIDGE_BOUNDARY_FAIL` | PASS | `bedc2ac30245` | `F5-W0-T06.observed.json` |
| `F5-W0-T07` | EDGE | `SCHEMA_UNSUPPORTED` | PASS | `e0792c58578e` | `F5-W0-T07.meta.json`, `F5-W0-T07.observed.json`, `F5-W0-T07.stderr.txt`, `F5-W0-T07.stdout.txt` |
| `F5-W0-T08` | NEG | `HOST_CAPABILITY_UNBOUND` | PASS | `2cb10dad5e84` | `F5-W0-T08.meta.json`, `F5-W0-T08.observed.json`, `F5-W0-T08.stderr.txt`, `F5-W0-T08.stdout.txt` |
| `F5-W0-T09` | NEG | `PHASE_OVERREACH_CANDIDATE` | PASS | `9c030b245503` | `F5-W0-T09.meta.json`, `F5-W0-T09.observed.json`, `F5-W0-T09.stderr.txt`, `F5-W0-T09.stdout.txt` |
| `F5-W0-T10` | NEG | `GATE_CYCLE_CANDIDATE` | PASS | `bf46ebedf06d` | `F5-W0-T10.meta.json`, `F5-W0-T10.observed.json`, `F5-W0-T10.stderr.txt`, `F5-W0-T10.stdout.txt` |
| `F5-W0-T11` | NEG | `FALSE_AUTHORITY` | PASS | `48c16e76438b` | `F5-W0-T11.meta.json`, `F5-W0-T11.observed.json`, `F5-W0-T11.stderr.txt`, `F5-W0-T11.stdout.txt` |
| `F5-W0-T12` | NEG | `EFFECT_MAPPING_UNVERIFIED` | PASS | `a8b2c72111a7` | `F5-W0-T12.meta.json`, `F5-W0-T12.observed.json`, `F5-W0-T12.stderr.txt`, `F5-W0-T12.stdout.txt` |
| `F5-W0-T13` | POS | `EFFECT_NOT_VERIFIED` | PASS | `0b61087da2c3` | `F5-W0-T13.observed.json` |
| `F5-W0-T14` | NEG | `EFFECT_NOT_VERIFIED` | PASS | `a6c8ca2809dc` | `F5-W0-T14.meta.json`, `F5-W0-T14.observed.json`, `F5-W0-T14.stderr.txt`, `F5-W0-T14.stdout.txt` |
| `F5-W0-T15` | NEG | `ORACLE_DRIFT` | PASS | `aea879b4c2f0` | `F5-W0-T15.meta.json`, `F5-W0-T15.observed.json`, `F5-W0-T15.stderr.txt`, `F5-W0-T15.stdout.txt` |
| `F5-W0-T16` | EDGE | `CANDIDATE_CHANGED` | PASS | `96b00a365ee4` | `F5-W0-T16.meta.json`, `F5-W0-T16.observed.json`, `F5-W0-T16.stderr.txt`, `F5-W0-T16.stdout.txt` |
| `F5-W0-T17` | NEG | `UNREPRODUCED` | PASS | `d01d92ddbe51` | `F5-W0-T17.meta.json`, `F5-W0-T17.observed.json`, `F5-W0-T17.stderr.txt`, `F5-W0-T17.stdout.txt` |
| `F5-W0-T18` | NEG | `ZERO_FROM_UNAVAILABLE` | PASS | `eb803affaa00` | `F5-W0-T18.meta.json`, `F5-W0-T18.observed.json`, `F5-W0-T18.stderr.txt`, `F5-W0-T18.stdout.txt` |
| `F5-W0-T19` | NEG | `FALSE_CLOSE` | PASS | `3f07b9dedec0` | `F5-W0-T19.meta.json`, `F5-W0-T19.observed.json`, `F5-W0-T19.stderr.txt`, `F5-W0-T19.stdout.txt` |
| `F5-W0-T20` | EDGE | `NO_DELTA_REWRITE_DENIED` | PASS | `1b9ccca8bc8c` | `F5-W0-T20.meta.json`, `F5-W0-T20.observed.json`, `F5-W0-T20.stderr.txt`, `F5-W0-T20.stdout.txt` |
| `F5-W0-T21` | NEG | `NO_DELTA_REWRITE_DENIED` | PASS | `d9d004b9d89b` | `F5-W0-T21.meta.json`, `F5-W0-T21.observed.json`, `F5-W0-T21.stderr.txt`, `F5-W0-T21.stdout.txt` |
| `F5-W0-T22` | NEG | `RELEASE_NOT_CLAIMED` | PASS | `e8e013d7501a` | `F5-W0-T22.meta.json`, `F5-W0-T22.observed.json`, `F5-W0-T22.stderr.txt`, `F5-W0-T22.stdout.txt` |
| `F5-W0-T23` | SEC | `SECRET_LEAK` | PASS | `5f33c812d483` | `F5-W0-T23.meta.json`, `F5-W0-T23.observed.json`, `F5-W0-T23.stderr.txt`, `F5-W0-T23.stdout.txt` |
| `F5-W0-T24` | POS/NEG | `PROFILE_GATE_DRIFT` | PASS | `f8ab2d71c569` | `F5-W0-T24.meta.json`, `F5-W0-T24.observed.json`, `F5-W0-T24.stderr.txt`, `F5-W0-T24.stdout.txt` |
| `NF-T01` | NF | `ARCHITECTURE_REWORK_REQUIRED` | PASS | `e483abd52f7d` | `NF-T01.meta.json`, `NF-T01.observed.json`, `NF-T01.stderr.txt`, `NF-T01.stdout.txt`, `requal_NF-T01.meta.json`, `requal_NF-T01.stderr.txt`, `requal_NF-T01.stdout.txt` |
| `NF-T02` | NF | `FALSE_READER` | PASS | `0f6db5b624b8` | `NF-T02.meta.json`, `NF-T02.observed.json`, `NF-T02.stderr.txt`, `NF-T02.stdout.txt` |
| `NF-T03` | NF | `EFFECT_NOT_VERIFIED` | PASS | `0934e2b8ff06` | `NF-T03.meta.json`, `NF-T03.observed.json`, `NF-T03.stderr.txt`, `NF-T03.stdout.txt` |
| `NF-T04` | NF | `RUNNER_UNBOUND` | PASS | `1b133517a54f` | `NF-T04.meta.json`, `NF-T04.observed.json`, `NF-T04.stderr.txt`, `NF-T04.stdout.txt` |
| `NF-T05` | NF | `OFF_PARITY_UNPROVEN` | PASS | `44baaa500bc6` | `NF-T05.meta.json`, `NF-T05.observed.json`, `NF-T05.stderr.txt`, `NF-T05.stdout.txt` |
| `NF-T06` | NF | `FALSE_RESEARCH_GATE` | PASS | `f4c13fe6d8d3` | `NF-T06.meta.json`, `NF-T06.observed.json`, `NF-T06.stderr.txt`, `NF-T06.stdout.txt` |
| `NF-T07` | NF | `FALSE_CAPABILITY` | PASS | `5ae4f94c902b` | `NF-T07.meta.json`, `NF-T07.observed.json`, `NF-T07.stderr.txt`, `NF-T07.stdout.txt` |
| `NF-T08` | NF | `UNREPRODUCED` | PASS | `acec518386b8` | `NF-T08-chain.meta.json`, `NF-T08-chain.stderr.txt`, `NF-T08-chain.stdout.txt`, `NF-T08-negatives.meta.json`, `NF-T08-negatives.stderr.txt`, `NF-T08-negatives.stdout.txt`, `NF-T08.meta.json`, `NF-T08.observed.json` |
| `NF-T09` | NF | `NO_DELTA_REWRITE_DENIED` | PASS | `2f585fa80655` | `NF-T09.meta.json`, `NF-T09.observed.json`, `NF-T09.stderr.txt`, `NF-T09.stdout.txt` |
| `NF-T10` | NF | `HANDOFF_UNCONSUMED` | PASS | `39770f244785` | `NF-T10.meta.json`, `NF-T10.observed.json`, `NF-T10.stderr.txt`, `NF-T10.stdout.txt` |

## not_covered

- W1–W4 全分母、FHS 485、HERMES／GPT Host、不同 principal 簽章、Publisher/Release。
