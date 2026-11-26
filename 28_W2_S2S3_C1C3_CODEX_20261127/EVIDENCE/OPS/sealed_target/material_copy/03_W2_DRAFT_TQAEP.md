# W2 INBOUND DRAFT — TQAEP（13 binding requests）

| ID | Predecessor | Fields | Type | Owner | W0 evidence | Resume minimum |
|---|---|---|---|---|---|---|
| `W2-B01` | Original OperationType | `effect.operation_type`／`effect.token` | enum／string | Effect Owner | `original_effect_registry_ref=null` | 同 Scope typed token |
| `W2-B02` | RepoContext | `repo.root/head/branch/dirty` | object | Repo Owner | 無 repo binding | live probe＋HEAD SHA |
| `W2-B03` | HostID／OS Principal／PolicyEpoch | `host.host_id/principal/epoch` | object | Host／OS Owner | 無 receipt | 同 Host／Epoch readback |
| `W2-B04` | Original DEV ECP | `ecp.dev_ref` | ref | Repo＋Issuer | `original_ecp_ref=null` | 原 DEV ECP typed ref |
| `W2-B05` | Original OPS ECP | `ecp.ops_ref` | ref | Host＋OS | `original_ecp_ref=null` | 原 OPS ECP typed ref |
| `W2-B06` | Issuer | `admission.issuer_id` | string | Original Issuer | `UNBOUND` | Issuer ID＋policy ref |
| `W2-B07` | WorkOrder | `admission.workorder_ref` | ref | Original Issuer | `null` | WorkOrder bytes＋SHA |
| `W2-B08` | ExecutionAdmission | `admission.receipt_ref` | ref | Original Issuer | `null` | 同 Subject／Scope receipt |
| `W2-B09` | Exact WriteSet／preimage | `write_set[]`／`preimage_sha256` | array／64-hex | Repo／OPS Owner | 無 | exact path set＋preimage SHA |
| `W2-B10` | WorldReader／RepoReader | `reader.world`／`reader.repo` | ref | Reader Owner | `UNBOUND` | 同 Host／Epoch readback |
| `W2-B11` | Protected Checker | `checker.receipt_ref` | ref | Checker | `null` | 同 Candidate distinct receipt |
| `W2-B12` | Publisher | `publisher.receipt_ref` | ref | Publisher | `null` | 原 release procedure |
| `W2-B13` | Recovery ABI | `recovery.kind`／`recovery.ref` | enum／ref | Repo／Host Owner | 無 | DEV reverse patch／Host recovery |
