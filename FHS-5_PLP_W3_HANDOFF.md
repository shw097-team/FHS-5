# FHS-5_PLP W3｜HANDOFF（W3 → W4 欄級）

- `from_stage`：W3｜`to_stage`：W4
- `handoff_id`：`W3-HANDOFF-20261126T1605`
- `project`：`FHS-5_PLP`｜`work_id`：`W3-NF-01`
- `pack_ref`：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`
- `pack_manifest_sha256`：`9c34251936067a027d2dfc31cd28540336df27c110311590369e49773ddd96c4`
- `package_tree_sha256`：`96c4d3a49ea7e579e601b64b8e4df8173f44c614bdef2910d6fe96a05235bd08`
- `candidate_commit`：local `4bfc0145acf1bf30e2072935086db269115c6b3a`（tree `021ccc54b585c7211715ef1db9e6df2d5db88775`）；base W2 product `dada2354…`；push `PUSH_BLOCKED`
- `oracle_sha256`：`686a2733925cf1d56fcff14ee1b982f0db55895a3647113a959f031b866d54f8`（design oracle set；非 product freeze）
- `case_set_sha256`：`a33e2047eeae517073666786b381a2ec1ed047ccc478384b939e39243d2f74a4`（design case set）
- `evidence_ref`：`evidence/20261126T1605/`
- `checker_ref`：`CHECKER_RECEIPT.json` sha `48f804d681e27e74…`；verifier sha `00bbdb755c005ca5…`（distinct local process）
- `consumer_ref`：`CONSUMER_RECEIPT.json` sha `49cecd81e473909e…`；verifier sha `1515a0c6d37f4f72…`（fresh local process）
- `publication_state`：`PUSH_BLOCKED`（local commit/tree only; no remote readback）

## 五 pin

| pin | value | state |
|---|---|---|
| `source` | `fb3d2eada010506c8d491c88df9536fa52c5b553c6eef5d589a30edfc3a59102` | W3 source_set over 28 sources |
| `candidate` | `8b4b4068313ae4d3ab066d6951add31d225d360ac053771d7d611621101ed8d7` | W2 five-member verified product set (upstream frozen input) |
| `evidence` | `cb9bc39d9a541db86571c3eda05db61674e69813029caa519054da054a2ca903` | W3 pack external seal over manifest+tree |
| `oracle` | `686a2733925cf1d56fcff14ee1b982f0db55895a3647113a959f031b866d54f8` | digest over 16 design oracle rows (not product-frozen) |
| `case_set` | `a33e2047eeae517073666786b381a2ec1ed047ccc478384b939e39243d2f74a4` | digest over plan index + 16 case ids |

## W4 可消費欄位

| W4 欄 | 本輪值 |
|---|---|
| `FindingSet[].raw_sha256` | `c7125b139052f96a…`, `446cf2f755087aac…` |
| `NotCovered[]` | 16 案 product state `NOT_COVERED`；W2 12 rows `NOT_REQUALIFIED` |
| `FARRetrievalGraph` | `far/FAR_GRAPH.json`；五態 BLOCKED_BY_AUTHORITY,ERROR,HIT,UNAVAILABLE,ZERO_RELEVANT_HIT |
| `DecisionAdvice` | `ADVICE/DECISION_ADVICE.json`；advice 非 grant |
| `W3_DELTA` | P1/P2 `PARK_NO_DELTA`；P1/P3 `NEW_MATERIAL_EVIDENCE` |
| `ChangeSet` | `W3_CHANGESET.json`；pack/W2 零寫入 |
| `CheckerReceipt` vs `ConsumerReceipt` | distinct local process；strength=`LOCAL_DISTINCT_PROCESS` |

## local delivery

| item | value |
|---|---|
| branch | `codex/w3-product-20261126T1605` |
| base commit | `dada2354b7c25c8f4a316d9fae93827cef0d194e` |
| content commit | `4bfc0145acf1bf30e2072935086db269115c6b3a` |
| content tree | `021ccc54b585c7211715ef1db9e6df2d5db88775` |
| receipt commit | `46d2db9e8f2c1cf961e0391716661dac8337186f` |
| redaction commit | `9df876789c97c11faa887e69243acdd913649905` |
| remote | `https://github.com/shw097-team/FHS-5` |
| pushed | `false` |
| blocker | `PUSH_BLOCKED`（credential egress needs explicit Owner approval） |

## readiness

| claim | value | reason |
|---|---|---|
| `W4_TECHNICALLY_READY` | **NOT_CLAIMED** | W3 未 `W3_NF_VALIDATED`；W4 當期採納入口未取得 |
| `W4_EXECUTION_READY` | **NOT_CLAIMED** | 缺 W4 具名施工授權、Host/ACL、逐 op authority/preimage/recovery |

## next legal action

1. W4 只可先合法 READ/DRAFT，不得以本 handoff 當 W4 施工 Grant。
2. 取得 W4M 當期採納入口與具名授權後，按 W4 原 entry contract late-bind。
3. 若 Owner 要升 W3：先補 Case Owner freeze + 真 Host/runner + distinct Checker + fresh Consumer。

## NotCovered / Resume

- `W2_WRITER_BLOCKED`：Owner 於 W2 scope 新具名授權；保留原 marker。
- `PRODUCT_HOST_UNBOUND`：指名 HostID/principal/ACL/policy epoch。
- `PRODUCT_RUNNER_UNBOUND`：指名 binary/SHA/argv/cwd/timeout。
- `CASE_OWNER_FREEZE_MISSING`：16 案真 bytes + frozen_at + Case Owner。
- `DISTINCT_ORIGINAL_CHECKER_MISSING`：原域不同 principal。
- `W2_MATRIX_AUDIT`：r3 ledger 10 rows／全 raw:null；W2-OPS-01/W2-DELTA-01 無 case row；aggregate `8b4b…` 不可重算；不得重用 W2 verdict。

