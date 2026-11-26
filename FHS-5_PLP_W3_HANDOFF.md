# FHS-5_PLP W3｜HANDOFF（W3 → W4 欄級）

- `from_stage`：W3｜`to_stage`：W4
- `handoff_id`：`W3-HANDOFF-20261126T1605`
- `project`：`FHS-5_PLP`｜`work_id`：`W3-NF-01`
- `pack_ref`：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`
- `pack_manifest_sha256`：`9c34251936067a027d2dfc31cd28540336df27c110311590369e49773ddd96c4`
- `package_tree_sha256`：`96c4d3a49ea7e579e601b64b8e4df8173f44c614bdef2910d6fe96a05235bd08`
- `candidate_commit`：`UNBOUND`（W2 product baseline `dada2354…` 仍 PARTIAL；W3 產品 commit 於 push 後另記）
- `oracle_sha256`：`686a2733925cf1d56fcff14ee1b982f0db55895a3647113a959f031b866d54f8`（design oracle set；非 product freeze）
- `case_set_sha256`：`a33e2047eeae517073666786b381a2ec1ed047ccc478384b939e39243d2f74a4`（design case set）
- `evidence_ref`：`evidence/20261126T1605/`
- `checker_ref` / `consumer_ref`：見同目錄 `CHECKER_RECEIPT.json`／`CONSUMER_RECEIPT.json`（本地 distinct process）
- `publication_state`：見 `PUBLICATION_RECEIPT.json`

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

