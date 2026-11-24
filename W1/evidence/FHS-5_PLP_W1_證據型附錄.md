# FHS-5_PLP W1｜證據型附錄（修補後）

- TaskID：`FHS5-W1-CODEX-REPAIR-20261124-v1`｜Subject：`FHS-5_PLP/W1/CONTROL_PACK`｜Batch：`W1-PACK-01`
- 基線：`FHS5_W1_AUTHOR_20261124_v1/FHS-5_PLP_W1`（唯讀保留）
- 修補候選：`W1_CODEX_REPAIR_20261124_v1/FHS-5_PLP_W1_REPAIRED_CANDIDATE`
- 本附錄是作者證據，不是第二套規範，也不是原域 Reader／Runner／Checker 的收據；最高效力 `AUTHOR_DESIGN_ONLY`。
- 輸出根：`<USER_HOME>\Documents\Codex\2026-11-24\new-chat-10\outputs\W1_CODEX_REPAIR_20261124_v1`

## E0｜Scope、方法與版本

本輪在隔離根內，先對基線做完整 A–F／H1–H8 審查（12 項本地缺陷），再以「最小受影修補」直接修改候選包，重跑 guard／replay／harness／case rules 與重封。未改基線、W0 PRIMARY、上游來源、產品 Repo／Host、原 Case／Oracle。

版本鏈：M r3、B00–B05 r4a、WM r2、W1M wm-v5、W0MB candidate-v2、W0 PRIMARY（Owner local promotion）、CTRLW1 v1、STARTW1 v1、基線作者候選、本輪 repaired candidate。歷史 r5／review r1／C4 未提供實體，維持 `UNBOUND`。

## E1｜SourceFreeze（16 源）

`SOURCE_MANIFEST.json` 未變（SHA `8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47`）；16 源逐檔 bytes／lines／SHA 均與基線及上游原件一致。

| ID | bytes | lines | raw SHA-256 | 狀態 |
|---|---:|---:|---|---|
| M | 325511 | 3016 | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` | READ_VERIFIED |
| B00 | 79605 | 528 | `fee7e533388ae1ac1149fca350b0b4dcd9bbe232b705e413528a933cef7e09e2` | READ_VERIFIED |
| B01 | 48177 | 405 | `3005886449f45c10e4aa87c5c8a59af9e00f988e99a606c2e853f351c4c72d49` | READ_VERIFIED |
| B02 | 47039 | 398 | `1a9fd64370be1da7b3f23a5a0b09e1dbde0712b369d4cb9787b669d1fa372441` | READ_VERIFIED |
| B03 | 39898 | 326 | `9ce12fd8fa5c1027bc10161efac03275e271d38537f816cebd233f23ae1317d0` | READ_VERIFIED |
| B04 | 40665 | 332 | `619c5a9370b531c5cba3128edcfcb939d51e6cd45301c7795634ac4c954e6066` | READ_VERIFIED |
| B05 | 51163 | 380 | `f6f043e1605b65c5faf24f8b9a72cde1218bf4151c4f9cfec8b9034aa2e5a3b4` | READ_VERIFIED |
| WM | 286201 | 2080 | `d2fa0db998c68288dfcb256137aba7603c308b53b9e17441c46cc64f63b6ffe2` | READ_VERIFIED |
| W1M | 71612 | 884 | `0bda92ef4a0e75e23530267ce97ab01b8044027c6cd06ab014a28053ce529b73` | READ_VERIFIED |
| W0MB | 29460 | 324 | `3acac0184f137202a8d3cc589f612e28f4f8c5f9e352835f2bd33aec8c5f31cd` | READ_VERIFIED |
| H-CLOSE | 2840 | 41 | `994264b1273e7127f032e41c72b7a97b0bf8e30139bcbab20eec1e543b5faeb3` | READ_VERIFIED |
| H-PATCH | 3291 | 61 | `76091015beab172e6bb85a217f2593f762c2416a2e74e9236a00cd09267f231e` | READ_VERIFIED |
| CTRLW1 | 35609 | 194 | `b126770c76335654e4496c5cb86485cb448bc5e04b13b9760661879e4924897a` | READ_VERIFIED |
| STARTW1 | 2336 | 13 | `2b151705f5389a295620fa7579ecc2e3515b2fb4a628be1201e1f4c8b0ba54de` | READ_VERIFIED |
| W0-PRIMARY-MANIFEST | 5914 | 185 | `f2d6e3dc2f7e56384c02ab401babdd81a6690754c9074233431a9080c579f648` | READ_VERIFIED |
| W0-PRIMARY-RECEIPT | 4222 | 112 | `6dbdd7bd783bc8680702eba6af9973b2a775823399b3bfb9cda099a5132f2efd` | READ_VERIFIED |

修補前附錄曾把 CTRLW1／STARTW1／W0-MANIFEST／W0-RECEIPT 寫成 289／21／192／92 行；本版已改為實測 194／13／185／112（F-08 已修）。

## E2｜W0 PRIMARY／LastGood 差額

實體 36 檔＝23 root＋13 sources；`PRIMARY_MANIFEST.json` 34 entries；33/34 byte＋SHA 一致；唯一不符為 `PRIMARY_RECEIPT.json`（實體 4,222 B／`6dbdd7bd…` vs 清冊 3,986 B／`18ad4b8d…`）。`PACKAGE_FILE_MANIFEST.json` 27 entries、`SOURCE_MANIFEST` 13 sources。候選包的 D01／W1-R3-01 陳述與此一致。

LastGood：`10_FINAL_DELIVERY/FHS-5_PLP_W0_REPAIRED_CANDIDATE`；PRIMARY：`10_FINAL_DELIVERY/FHS-5_PLP_W0_PRIMARY`。本輪未改 W0。

## E3｜Trace、分母與工具身份

- 15 規範檔：10 MD＋5 JSON，固定檔名不變。
- 6 WP：`WM1-P01..P06`；5 batch：`W1-B1..B5`；typed DAG 邊已寫入 `01` §4。
- 16 `CG-R2-REQ`、17 `PCB-FR`、U-017 九 child、U-028 三 child：逐項在位。
- 13 W1 作者 Case：clause 與 W1M L663–675 逐字相同；9 案可執行規則、4 案 POS 需原執行器。
- 24 W0 Case：8 UPDATE（T01/04/06/07/16/17/23/24）＋16 RETAIN。
- 工具：`inventory/TOOL_IDENTITY_LEDGER.json` 485/485 原 ID；10 筆 W1 受影、217 筆 W0-C、258 筆 W2–W4；`HostFit`／`original_ack` 全 `UNBOUND`。
- 分母：`inventory/DENOMINATOR_LEDGER.json` 23 族（56 子義、35 Reviewer Tool、22 WP、36 Edge、50 H1、39 ModeGate、96 Oracle、192 Cell、485 ToolNeed、W0-C 1011、QA26、C16/36/47、FAR-T20/FARP30/35、Bridge 38+28、Guide 17、W0 24、W1 13）。未提供 ID 清單者保留 `UNBOUND` 與 owner，不宣全量覆蓋。

## E4｜實跑命令、exit 與 raw

```text
python check/w1_guard.py --pack-root FHS-5_PLP_W1_REPAIRED_CANDIDATE --delivery-root .
→ W1_AUTHOR_LOCAL_LINKS_ONLY；671 checks；sources 16、cases 13、w0 24、wps 6；exit 0

python check/m22_guard_ref.py check-pack --pack-root FHS-5_PLP_W1_REPAIRED_CANDIDATE
→ AUTHOR_LOCAL_LINKS_ONLY；case_count 13；exit 0

python check/replay_hashes.py --root FHS-5_PLP_W1_REPAIRED_CANDIDATE
→ REPLAY_OK；files 58、mismatches []；exit 0

python check/run_cases.py --pack-root FHS-5_PLP_W1_REPAIRED_CANDIDATE
→ CASE_RULES_PASS；9 executed／9 passed／4 not run；exit 0

python check/run_harness.py
→ positive_pass true；negatives 17/17；SELF_CHECK_PASS_WITH_NAMED_HOLDS；exit 0

python work/validate_repaired.py <pack> <delivery>
→ 20 PASS／0 FAIL
```

raw：`evidence/raw/harness_results.json`（`48ebc23d…`）、`harness_summary.txt`、`case_rule_results.json`（`5ad83309…`）、`host_probe.txt`（`983c800a…`，CONTAINER_ONLY）。

17 個 harness 反例：原 10 組＋`H9_cg_req_row`、`H9_pcb_fr_row`、`H9_clause_truncate`、`H9_kind_flip`、`H9_firstfail_drift`、`H9_source_count_text`、`H9_extra_file`，全部在隔離副本重封（除 extra file）後被拒。

## E5｜Claim、HOLD、NotCovered

- Claim：`local_observed/native_observed/independent_accepted/released` 四 bool 全 false；四個 receipt 全 null。
- 14 具名 HOLD：原 13＋`HOLD_CR-DOC04-STATE-MAP`（T4/T5）。
- 未跑：三 Host 七階段、Hermes 三能力、原 17／66／24、原 Runner／Checker／Publisher、真正 W1 DEV／OPS、package-first 全鏈 dry-consume。
- 允許：Source READ、隔離 DRAFT、local guard／rule check、local package。DEV／OPS／USER／RELEASE 仍 `NOT_ADMITTED`。

## E6｜最終檔案清冊

| # | 檔 | bytes | SHA-256 |
|---:|---|---:|---|
| 1 | `00_WAVE_RUN_MANIFEST.md` | 7018 | `66f566863b8ff6b972f4b0edc6077c25b7219cf35948dad9378c61d1b5adb896` |
| 2 | `00_WAVE_RUN_MANIFEST.json` | 31876 | `212863778f4a390fb5867774b117bfe5d1031229614542d150b227ba152242eb` |
| 3 | `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | 22004 | `6a61d9b5ab401c4c6c584ce51028ff8f5136215f491487e36b14717c3814d718` |
| 4 | `02_ORIGINAL_CONTRACT_REFS.json` | 1644 | `b0ab99f24e9bf4df6a1221059730458ba3114557d6e38afdd0fd3ac1317e2daf` |
| 5 | `03_DEV_ECP.md` | 6302 | `5ab52cebd19e5822ee4035fb9b0f880cc1d256a82841f3c8b4f607fdfd15037f` |
| 6 | `04_OPS_ECP.md` | 5513 | `87591f5b710376987dd5c45ca2dbd3530e3e3b979fa578cb8c6e53ea366b8ff6` |
| 7 | `05_PLANNED_TQAEP.md` | 8797 | `48233e467dfeb1c8611f77d6b725e467fa1288020b9c29438faf9b7d1f530ef4` |
| 8 | `05_PLANNED_TQAEP.json` | 22034 | `ba6405919707f799c30441bb7ee9f3fe58ccbcf35e588d708d0a40ff5064ca90` |
| 9 | `06_PERMISSION_STOP_RESUME.md` | 6659 | `7d5114bf6e6cd75ec3d50b2925974d0a4c48d842aa209f2d3d30f9c85ca6e9a5` |
| 10 | `07_EVIDENCE_AND_CHECKER.md` | 4008 | `f02eea4e6e390fdbb870b4d73dcc97ba2af55b377f9bbacc1557bd3ae70ee11b` |
| 11 | `08_AS_BUILT_AND_HANDOFF.md` | 4808 | `62e53cce751b24dbbeba48b3b7d32588e22d5c1ac07d4cb7224b7fdac4c26560` |
| 12 | `09_README_RUN_ORDER.md` | 4070 | `8838433b0c36c9185f9b8af3d49ddfb00749774ba2f797b6cf1f2f5a580f59f4` |
| 13 | `PACKAGE_FILE_MANIFEST.json` | 9730 | `7dc11eba6d2a063f12758ca31ed5a91b25f026a6409134e00e04d2bd49bbbabb` |
| 14 | `SOURCE_MANIFEST.json` | 7904 | `8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47` |
| 15 | `W1_START_THIN_PROMPT.md` | 2964 | `f51ee80069f380bd5bb3015146e012a06fd6d0a0a708b9f92fecf7d43bac08bb` |
| — | `inventory/TOOL_IDENTITY_LEDGER.json` | 310493 | `578c3a8c9a17b14a8837dce4c173feab20592001940ff63f1e12b9f5a6f0db2e` |
| — | `inventory/DENOMINATOR_LEDGER.json` | 6537 | `e1092ed9266ad588a1a70018cf5bcd5067bc81320b01ee72c37dce44b242b8cf` |


**Primary relabel**：主用包把 `00`／`03`／`09` 內的資料夾 token 由 `FHS-5_PLP_W1_REPAIRED_CANDIDATE` 改為 `FHS-5_PLP_W1_PRIMARY`，以使主用路徑的命令可直接執行；語義未改。審查基線 `PACKAGE_FILE_MANIFEST.json` 為 `a66da402…`，主用包為 `7dc11eba…`。

另含 16 `sources/`、13 `fixtures/`、13 `oracles/`；`PACKAGE_FILE_MANIFEST.json` 58 筆（不含自身），已逐筆重算。

封存：`SOURCE_MANIFEST.json` `8bfb8be4…`；`05_PLANNED_TQAEP.md` `48233e46…`（= `projection_of_sha256`）；`PACKAGE_FILE_MANIFEST.json` `a66da402…`。ZIP／索引 digest 外置於 `DELIVERY_SEAL.json`，不自含循環。

## E7｜Reviewer sidecar（真執行）

使用 `plp-tpm-review 1.0.1` 的 `scripts/review_core.py`，以 `PLP.REVIEW.REQUEST@2` 對修補候選執行：

```text
python scripts/review_core.py --request work/review-request.json \
  --input-root FHS-5_PLP_W1_REPAIRED_CANDIDATE \
  --outroot reviewer_sidecar_v2
→ state REVIEW_SOURCE_LOCATED_ONLY；authority UNBOUND；defects 0；unbound 81；exit 0
```

Sidecar：`evidence/reviewer_sidecar/review-12f3062e70d45a226b1c0495/`（00–04＋`REVIEW_PACKAGE_MANIFEST.json`，6 檔）。這是 reviewer 本地結果，不是原域接受；81 個 `UNBOUND` 是原 Reader／PI/PD ref／Case Reader 缺失的如實降級。

第一次 request 由呼叫方手寫 `polarity`，工具以自身 NEG 字串啟發式判為 `POLARITY_DRIFT`（9 筆）；核對後確認是 request 側宣告與工具啟發式不一致，不是候選包缺陷。移除呼叫方 `polarity` 宣告後重跑，得到 0 defects；該次 artifact 不列入 pack finding。
