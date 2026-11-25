# FHS-5_PLP W1 HANDOFF（W2 技術接收候選）

**File ID**：`FHS5-PLP/W1/HANDOFF/NF-r3`
**run_id**：`20261125T222954`｜**pack_manifest_sha256**：`61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a`
**repo**：`codex/w1-nf-r3-20261125` @ `c2d8084ba24dd8df3fa62259bba496f4fb9caa85`
**status**：`W2_TECHNICALLY_READY = NOT_READY`（見 §5 缺口）

---

## 1｜W2 可直接消費的欄位

| 欄 | 值／位置 |
|---|---|
| `subject_id` | `FHS-5_PLP/W1/CONTROL_PACK` |
| `scope` | `W1-NF-01` |
| `pack_manifest_sha256` | `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a` |
| `source_set_sha256` | 見 `evidence/inspect.json` |
| `package_tree_sha256` | 見 `evidence/inspect.json`（digest_domains） |
| `context_sha256` | 由 `bridge_nf.render_agent_context` 產生，不寫入 manifest |
| `entry` | `W1/impl/nf_reader.py`（`inspect` 子命令） |
| `bridge` | `W1/impl/bridge_nf.py`（四 API） |
| `guide` | `W1/impl/guide_nf.py`（四函式／兩模式／九鍵） |
| `tpm` | `W1/impl/tpm_contracts_nf.py`（五視圖＋Reviewer） |
| `consumer` | `W1/impl/w1_consumer.py` |
| `runner` | `W1/check/run_cases_nf.py` |
| `oracle/case set` | pack `assets/oracles`、`assets/fixtures`，26 檔 SHA 已驗 |
| `effect schema` | `permission_state=NONE_GRANTED`、`host_effect=NOT_ADMITTED`、`unknown_effect=FAIL_CLOSED` |

## 2｜真實驗收數據

- 六檔：5 MD／38 DEV／29 OPS／13 Case／26 assets／42 sources／14 HOLD。
- 測例：20 列，PASS 18、NOT_OBSERVED 1、DEFERRED 1、FAIL 0。
- 單元測試：63 tests OK。
- OpenSpec：`w1-nf-r2-product` valid。

## 3｜next／stop／resume

| 欄 | 值 |
|---|---|
| next | W2 於其自身 grant 下重算 pack/manifest/asset/candidate 並決定 protected effect 範圍 |
| stop | 錯 pin／缺 asset／scope 不符／未知 effect／要求 W1 冒 host served |
| resume | 同 subject+scope+pack_manifest_sha256 的 typed receipt；ACL/principal 再驗 |

## 4｜fresh receive 重放

```
python W1/impl/nf_reader.py inspect --pack <pack_root>
python W1/impl/bridge_nf.py inspect --pack <pack_root>
python -m unittest discover -s W1/check -p "test_*.py"
python W1/check/run_cases_nf.py --pack <pack_root> --out <evidence_dir>
```

## 5｜W2 技術准入判定

**NOT_READY**。阻斷：無真實 CODEX host served/consumed raw；Hermes 三 child 未觀測；獨立 Checker 與 maker 同 OS principal；67 ID 未逐份 raw。

解除條件：取得對應真 raw 後重跑 `run_cases_nf.py` 與 seal 重算，再評估。
