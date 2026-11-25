# FHS-5_PLP W1 HANDOFF（NF-r4 → W2）

**run_id**：`20261125T233359`｜**pack_manifest_sha256**：`61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`
**repo**：`codex/w1-nf-r3-20261125`｜`content_commit` `UNCOMMITTED`
**status**：`W1_NF_VALIDATED`｜W2 `READY`

## 1｜W2 消費欄位

```
subject_id: FHS-5_PLP/W1/CONTROL_PACK
scope: W1-NF-01
pack_manifest_sha256: 61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a
entry: W1/impl/nf_reader.py
bridge: W1/impl/bridge_nf.py
guide: W1/impl/guide_nf.py
tpm: W1/impl/tpm_contracts_nf.py
consumer: W1/impl/w1_consumer.py
runner: W1/check/run_cases_nf.py
```

| 欄 | 值 |
|---|---|
| subject / scope | `FHS-5_PLP/W1/CONTROL_PACK` / `W1-NF-01` |
| pack_manifest_sha256 | `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a` |
| source_set_sha256 | `8f2e484f46ff99bff9e1a0e6bf9dada0daea5ad2ee3b5357deb72435db32636c` |
| evidence manifest | `EVIDENCE_MANIFEST.json`（逐檔 sha256，seal 外置綁定） |
| closure matrix | `W1_CLOSURE_MATRIX.json`（118 列） |
| host receipt | `evidence/host/host_receipt.json` |
| W2 receipt | `W2_RECEIVE_RECEIPT.json` |
| entry / bridge / guide / tpm / consumer / runner | `W1/impl`、`W1/check` |

## 2｜next / stop / resume

- next：`W2-READ: consume W1 SourceRefs/EffectConstraints/HostCapabilityLedger, choose one READ/DRAFT task inside W2 scope`
- stop：`wrong candidate/pack/oracle/evidence/handoff/scope, or any fake grant`
- resume：`same subject+scope+pack pin typed receipt; re-verify ACL/principal`

## 3｜重放

```
python W1/check/run_host_nf.py --w1-pack <pack> --second-pack <w0 pack> --out <evidence>/host
python W1/check/run_cases_nf.py --pack <pack> --out <evidence>
python W1/check/closure_matrix.py --pack <pack> --evidence <evidence> --out W1_CLOSURE_MATRIX.json
python W1/check/w2_receiver.py --delivery . --out W2_RECEIVE_RECEIPT.json
```
