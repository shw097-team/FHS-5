# FHS-5_PLP/W0｜HANDOFF（B0→W1）

- handoff_id: `W0-B0NF-HANDOFF-20261125-01`
- from_stage: `B0-NF`
- to_stage: `W1`
- project/work_id: `FHS-5_PLP/W0`
- pack_ref: `W0-NF-r3-CODEX-PRIMARY`
- pack_manifest_sha256: `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`
- candidate_ref: `5eab43de2d3f67d6afbb1c5f6bc390e2c391da36`
- evidence_ref: `ef977e0855e7d3dc633aaa5d2b0a78976a3ee530667596f5b8f031dbf262c6d5`
- target_consumer: W1 / CODEX Native
- actual_readback: consumer_receipt `consumed=true`; checker `PASS`
- next_legal_action: W1 source freeze + Bridge 38+28 denominator + adapter on this pack/candidate
- owner: W1 Owner (CODEX role)
- dependencies: W1M/plan；Bridge reference；W0 evidence pins
- resume_predicate: W1 pack adopted + real required preconditions
- not_covered: 見 W0_CLOSEOUT §4
- w1_technical_readiness: `READY_WITH_THIS_B0_BASELINE`
- w1_execution_readiness: `NOT_CLAIMED`（需 W1 受影採納/入口/授權）

**Consumer rule**：W1 必須真讀本 handoff、pack、candidate、evidence 與 pins；不得以 ACK 字串或 manifest 存在代替。
