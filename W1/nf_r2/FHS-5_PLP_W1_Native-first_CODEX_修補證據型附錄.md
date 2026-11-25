# FHS-5_PLP_W1_Native-first｜CODEX 修補證據型附錄

**File ID**：`FHS5-PLP/W1/CONTROL_PACK/2026-11-25-nf-r2-EVIDENCE`
**pack_version**：`W1-NF-r2-CODEX-PRIMARY`｜**scope**：`W1-NF-01`｜**date**：2026-11-25（Asia/Taipei）
**Claim ceiling**：`W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（文件與主用選定）；**Execution readiness**：`W1_EXECUTION_READY = READY`；**Not claimed**：`W1_NF_VALIDATED`、`NATIVE_PASS`、`INDEPENDENT_PASS`、`RELEASED`、`M-DONE`、`GPT_CHAT_PASS`、`GPT_WORK_PASS`、`HERMES_PASS`。

> 本附件是唯一共用稽核附件，不是第七 normative，也不是 Current Registry。它記錄本輪實際做到的檢查、來源、修補、反證、缺口與 seal；產品 actual 一律 `NOT_RUN`。

---

## E0｜本輪執行摘要與實際邊界

| 項 | 實際 |
|---|---|
| 任務 | 對 `W1_Native-first_交付` 執行 CODEX 啟動薄 PROMPT：檢測、修補、有限迭代、自驗收、主用定案 |
| 輸入候選 | `W1-NF-r1-CODEX-CANDIDATE`（5 MD＋05，16,518 B 05；見 E8） |
| 輸出主包 | `FHS-5_PLP_W1_NATIVE_FIRST/`：5 MD＋05＋26 assets＋tools |
| 輸出根 | `C:\Users\user\Documents\Codex\2026-11-25\new-chat-11\outputs\W1_Native-first_CODEX_主用修補_交付`（本 sandbox 實際可寫；`C:\Users\user\Downloads\FHS-5` 與產品 repo 為唯讀，故未在 Downloads 建立交付根） |
| 檔案 effect | `READ + ISOLATED_DRAFT_WRITE + LOCAL_CHECK + LOCAL_PACKAGE`；產品 DEV/OPS `NOT_RUN` |
| 產品 repo probe | 原樹 `FHS-5_Workspace`：HEAD `c2d8084…`、branch `codex/b0-nf-20261125`、remote `shw097-team/FHS-5`；原樹寫入 DENIED。**W1 worktree `FHS-5_W1_NF_r2`：branch `codex/w1-nf-r2-20261125`，WRITE_OK** |
| 文件 verdict | `W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`（只對文件／主用／同域施工授權） |
| 產品 verdict | `PRODUCT_NOT_RUN`；`W1_EXECUTION_READY=READY`（entry／ACL／首個 `inspect` 操作已具；最終 product consumed 未跑） |
| 已真跑 | strict JSON／5+1／digest／identity／ID set／DAG／assets／sources／seal；12 個隔離 mutation；bootstrap 讀回；**W1 reader 16/16 unittest＋首個 `inspect` 操作** |
| 未跑 | 13 原案產品、四 API 真產品、CODEX served/consumed、第二包、GPT/HERMES、W2–4、Independent、Release |

**主用與施工授權記錄**：`OWNER-W1-NF-r2-20261125`。來源為本 thread 使用者指令（執行該薄 PROMPT，其文本明示「合格修補定案直接升格主用＋授權可施工，無須再次逐 WP 核簽」）。本附錄不把該裁決擴張為 OS ACL、Repo policy、七冊正式採納、外部 Host 或 public release。

---

## E1｜SourceFreeze（42 sources：42 local verified＋0 remote unbound）

來源根：`C:\Users\user\Downloads\FHS-5`（設計來源，唯讀）＋`C:\Projects\Agent_Workspace\FHS-5_Workspace`（repo 實作／證據，唯讀原樹）。`lines` 以 UTF-8 `splitlines` 計；完整 path 與 lines 見 05 `sources[]` 與 `evidence/raw/source_freeze.json`。本地 **42/42** bytes/SHA match；remote unbound 0。

| ID | 角色／檔名（尾段） | bytes | SHA-256 | 讀取層級 |
|---|---|---:|---|---|
| `PLAN` | W1 工程方案 | 86,117 | `999f3e3bf917cde57cc6ea8069a750e26356e103d5529990506809a7f0091a90` | FULL |
| `WORKCTRL` | GPT WORK 控制包 | 32,464 | `ef18e6a87aa4ee8ca12b76194b07c16bdc5631b7fd5531a8079f621510029659` | FULL |
| `CODEXCTRL` | CODEX 修補控制包 | 40,674 | `f01a8110cfedaacf13b986531b536096db4d3e4e42a5d1049d3df67f9a36d4ff` | FULL |
| `STARTCTRL` | CODEX 啟動薄 PROMPT | 3,518 | `ef99fbca090b7913799aecc3f3a5c2510f7bff0afdaae56f33d8105d5550b39e` | FULL |
| `W1M` | W1M NF-r2 正文 | 99,289 | `a91c4ed36cc2977372a5333bce068abe6a5e222b95cda5fe5dc81ef6cfe6c9c1` | KEY_SECTIONS |
| `W1M-EVIDENCE` | W1M 證據附件 | 8,185 | `b32068f591f69e681da1534809fcd36f81986bf16afc60c0b73b3af703407e87` | PIN_ONLY |
| `W1M-CLOSEOUT` | W1M 重構 CLOSEOUT/HANDOFF | 14,191 | `e13c36a7b7f9aa7620cf4d474e79635ac137bd600523b1198ac9031b03590bda` | PIN_ONLY |
| `W1M-OLD` | W1M wm-v5 血緣 | 71,612 | `0bda92ef4a0e75e23530267ce97ab01b8044027c6cd06ab014a28053ce529b73` | PIN_ONLY |
| `M` | M r3 總藍圖 | 325,511 | `2026da4b847c1368e44e4488443b6ba58416b269fc7c67b3c1faed8cfd19f2c7` | PIN_ONLY |
| `W0M` | W0M CODEX-FIRST-r4 | 108,861 | `c9b1ca9bbcd5ce87fdbcb0fc373cb8c36d1ad8d404b55c4f7311fc6c2bbddfd5` | PIN_ONLY |
| `H0` | W0 HANDOFF v3 | 3,265 | `21ed226738abbd75b72871f1c6173b83de5cadab661f2d366df8d7e547ff4579` | PIN_ONLY |
| `C0` | W0 CLOSEOUT | 21,927 | `23cfa1f640227c0f3ede052faacbeb14364f5a9337ca436970449de500827b3f` | PIN_ONLY |
| `W0-05` | W0 SourceManifest | 18,821 | `e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8` | PIN_ONLY |
| `W0M-ADMISSION` | WM/W0M/W1M admission | 810 | `aab38714754df4e6fc16daa339da24a60ae560cc95491756ae7967b4252f098c` | FULL |
| `B00NF` | PROG-00 NF-r2 | 126,626 | `cdd1d76ec20fad19bff96153b11a65a1d0ba98074e4d68d2abfaae5a72c89797` | PIN_ONLY |
| `B01NF` | PROJ-01 NF-r2 | 68,023 | `aa823374dabce5218611a248fda3c8f68a7f0b0d6b51ffa2e4915f7aec4d0392` | PIN_ONLY |
| `B02NF` | PROJ-02 NF-r2 | 65,006 | `37022f33e5a67ad3165b0a47d36b359255f13719047fa71508e2b80624fc3884` | PIN_ONLY |
| `B03NF` | PROJ-03 NF-r2 | 56,268 | `a13a9df4252a557a3e246035f136295fe1cad5990e828f9ec3d5df083307db98` | PIN_ONLY |
| `B04NF` | PROJ-04 NF-r2 | 57,182 | `fb529a784b7d929f15a23ed63ea82b7d5f5117e927311b1f164eb005da469323` | PIN_ONLY |
| `B05NF` | PROJ-05 NF-r2 | 67,845 | `794d91cc8080715886d5dc30b92e74b1f123fbe0aee47256bf1e84d749648dfe` | PIN_ONLY |
| `W1-RUNHARNESS` | repo `W1/check/run_harness.py`（Downloads 舊副本另存 11,369／`64f4c85b…`） | 11,420 | `3384841787d4d68c1c56fbb62dfe1776720b02205d58ffbf30c9e915a957dd9f` | PIN_ONLY |
| `W1OLD-00JSON` | 舊 00 Wave JSON | 31,876 | `212863778f4a390fb5867774b117bfe5d1031229614542d150b227ba152242eb` | PIN_ONLY |
| `W1OLD-00MD` | 舊 00 Wave MD | 7,018 | `66f566863b8ff6b972f4b0edc6077c25b7219cf35948dad9378c61d1b5adb896` | FULL |
| `W1OLD-01` | 舊 01 Source/Scope | 22,004 | `6a61d9b5ab401c4c6c584ce51028ff8f5136215f491487e36b14717c3814d718` | FULL |
| `W1OLD-02` | 舊 02 Original refs | 1,644 | `b0ab99f24e9bf4df6a1221059730458ba3114557d6e38afdd0fd3ac1317e2daf` | PIN_ONLY |
| `W1OLD-03` | 舊 03 DEV ECP | 6,302 | `5ab52cebd19e5822ee4035fb9b0f880cc1d256a82841f3c8b4f607fdfd15037f` | FULL |
| `W1OLD-04` | 舊 04 OPS ECP | 5,513 | `87591f5b710376987dd5c45ca2dbd3530e3e3b979fa578cb8c6e53ea366b8ff6` | FULL |
| `W1OLD-05JSON` | 舊 05 TQAEP JSON | 22,034 | `ba6405919707f799c30441bb7ee9f3fe58ccbcf35e588d708d0a40ff5064ca90` | PIN_ONLY |
| `W1OLD-05MD` | 舊 05 TQAEP MD | 8,797 | `48233e467dfeb1c8611f77d6b725e467fa1288020b9c29438faf9b7d1f530ef4` | FULL |
| `W1OLD-06` | 舊 06 Permission/Stop/Resume | 6,659 | `7d5114bf6e6cd75ec3d50b2925974d0a4c48d842aa209f2d3d30f9c85ca6e9a5` | FULL |
| `W1OLD-07` | 舊 07 Evidence/Checker | 4,008 | `f02eea4e6e390fdbb870b4d73dcc97ba2af55b377f9bbacc1557bd3ae70ee11b` | FULL |
| `W1OLD-08` | 舊 08 AsBuilt/Handoff | 4,808 | `62e53cce751b24dbbeba48b3b7d32588e22d5c1ac07d4cb7224b7fdac4c26560` | FULL |
| `W1OLD-09` | 舊 09 README/Run Order | 4,070 | `8838433b0c36c9185f9b8af3d49ddfb00749774ba2f797b6cf1f2f5a580f59f4` | FULL |
| `W1OLD-PFM` | 舊 PackageFileManifest | 9,730 | `7dc11eba6d2a063f12758ca31ed5a91b25f026a6409134e00e04d2bd49bbbabb` | PIN_ONLY |
| `W1OLD-SM` | 舊 SourceManifest | 7,904 | `8bfb8be467c53c66a048846a48cd5f7f2726c3ac61caed4d75b5285616d59f47` | PIN_ONLY |
| `W1OLD-START` | 舊 ThinStart | 2,964 | `f51ee80069f380bd5bb3015146e012a06fd6d0a0a708b9f92fecf7d43bac08bb` | FULL |
| `W1-ECP-MATRIX` | repo 67 ECP closure matrix（解析 38＋29） | 25,518 | `729fdaae6c249a21b3c38a6688c973d7ad88baa6404775b3a36d5ef9f2db452b` | FULL_67_ROWS |
| `W1-EXEC-REPORT` | repo W1 execution report | 3,354 | `3379fb8965137d1a76ee16e07cca57b7701632c337de51185a93148cb98cd9c0` | FULL |
| `W1-HOLDS` | repo W1 14 named holds | 2,755 | `a0fef9299f9daf64997610f5b900b8d40ba17d096c605ed5e9400d802b0f7ca4` | FULL |
| `W1-IMPL` | repo `W1/impl/w1_bridge_reference.py`（legacy reference） | 36,580 | `dc0d1041a473a96493c887f279f75dcc1eca077c39242de47faffd44e12050a8` | CODE_READ |
| `W0-GUIDE` | repo `13_W0_NF_CODEX_20261125/tools/guide.py` | 6,216 | `6be9b02bcc8207b36793351c3e4b5d447b485780e2a7ff0295d1d9dba21799e8` | CODE_READ |
| `W0-TPMCONTRACTS` | repo `13_W0_NF_CODEX_20261125/tools/tpm_contracts.py` | 11,913 | `e49e94eda45ea8117a9a3da6fa21f1f77749606ad0d4ba6f5f8fd78f369a4193` | CODE_READ |

**更正**：初次 source probe 只搜尋 `Downloads`，誤把上述 6 項標為 remote-only；後續在 `C:\Projects\Agent_Workspace\FHS-5_Workspace` 找到真檔，bytes/SHA 與候選 05 宣告一致。現已改為 local verified；Git blob SHA-1（`7ed2649a…`、`efee8549…`、`cc8f7455…`、`c8cdd58d…`、`cad7c2f4…`、`17903d9d…`）只作血緣，不當 raw SHA-256。來源內命令／prompt 只作資料。

---

## E2｜15→6 遷移與無損對照

| 舊檔 | 新落點 | 保留實質 | 負例 |
|---|---|---|---|
| `00_WAVE_RUN_MANIFEST.md/.json` | 00＋05 | identity、Goal/FUO/Done、effect、claim、holds、host ledger | 舊 author Done 冒產品 Done |
| `01_SOURCE_SCOPE_AND_CONSTRUCTION.md` | 00/01/02 | source/scope、P01–06、四 API、BodyResolver、七 Seam、W0 D01–08 | 只留索引 |
| `02_ORIGINAL_CONTRACT_REFS.json` | 05＋00 | 原 PI/PD/ECP/TQAEP refs；缺 ref null＋reason | 假 ACK |
| `03_DEV_ECP.md` | 01 | 38 ID、pre/post、WriteSet、readback、restore、admission | universal registry |
| `04_OPS_ECP.md` | 02 | 29 ID、Host/ACL/receiver、activation/invoke/serve/consume、recovery | 全 N/A |
| `05_PLANNED_TQAEP.md/.json` | 03 | 13 ID、原分母、fixture/oracle、ExpectedRaw | 13 PASS 冒全產品 |
| `06_PERMISSION_STOP_RESUME.md` | 00/01/02/04 | 單人 issuer、scoped grant、stop/resume、UNKNOWN | permit=true 發權 |
| `07_EVIDENCE_AND_CHECKER.md` | 03＋本附件 | 五 pin、NotCovered、Checker/Consumer 分立、actual=null | 作者自簽 Independent |
| `08_AS_BUILT_AND_HANDOFF.md` | 00 expected＋真 CLOSEOUT | LastGood/ChangeCone/接收 | 作者 AsBuilt 冒產品 |
| `09_README_RUN_ORDER.md` | 00 DAG＋04 | 下一合法動作、依賴方向、有限修補 | 第七啟動檔 |
| `W1_START_THIN_PROMPT.md` | 04 | GOAL/SOURCE/SPEC/EXECUTE/HARNESS/DONE/STOP/RESUME | 新增權限 |
| `SOURCE_MANIFEST.json` | 05 | bytes/SHA/span/rights/selection；16/17 歷史分帳 | 歷史 16 當新分母 |
| `PACKAGE_FILE_MANIFEST.json` | 05＋外置 seal | SHA/self exclude/path/duplicate/bytes | 雙 canonical |

舊十五檔未生成 projection；只在真舊 consumer 需要時另算 `projection_of_sha256`，不作第二 canonical。

---

## E3｜67 ECP 逐 ID trace（38 DEV＋29 OPS）

`A`=CLOSED_AUTHOR_LOCAL、`H`=CLOSED_WITH_NAMED_HOLD、`O`=ORIGINAL_DOMAIN_HOLD。`KEEP`／`REPLACE_NATIVE`／`DEFER_HOST` 為本包 disposition；原域 receipt 不在本包冒充。新位置指本包章節；驗收指 03/01/02 的實際 case/讀回。

| ECP ID | Requirement | old | NF | 新位置 | 驗收／consumer |
|---|---|---|---|---|---|
| `DEV-APP-01` | Applicability | A | KEEP | 01 §2 D1 | applicability ledger；P01 |
| `DEV-EFF-01` | Effect tokens | H | REPLACE_NATIVE | 01 D1 | effect enum/unknown reject；P02 |
| `DEV-PRE-01` | Precondition 1 | O | REPLACE_NATIVE | 01 D1 | repo/ACL probe；P01 |
| `DEV-PRE-02` | Precondition 2 | O | REPLACE_NATIVE | 01 D1 | preimage/ABSENT；D1 |
| `DEV-PRE-03` | Precondition 3 | O | REPLACE_NATIVE | 01 D1 | op/effect class；P02 |
| `DEV-PRE-04` | Precondition 4 | O | REPLACE_NATIVE | 01 D1 | grant/ACL；P01 |
| `DEV-PRE-05` | Toolchain/output root | A | KEEP | 01 D1 | versions/root；P01 |
| `DEV-WS-01` | WriteSet 1 Guide | A | KEEP | 01 WS | exact target；D3 |
| `DEV-WS-02` | WriteSet 2 Bridge | A | KEEP | 01 WS | exact target；D2–D3 |
| `DEV-WS-03` | WriteSet 3 BodyResolver | A | KEEP | 01 WS | exact target；D3 |
| `DEV-WS-04` | WriteSet 4 Host facade | A | KEEP | 01 WS | exact target；D4 |
| `DEV-PROH-01` | Protect W0/LastGood | A | KEEP | 01 §2 | outside diff；D1–D7 |
| `DEV-PROH-02` | Protect case/oracle | A | KEEP | 01 §2 | oracle hash；D5 |
| `DEV-PROH-03` | No secret/cross-root | A | KEEP | 01 §2 | secret/escape scan；D1–D7 |
| `DEV-PROH-04` | No git revert as OPS | A | KEEP | 01 §2 | recovery kind；D6 |
| `DEV-OP-01` | Live RepoContext | O | REPLACE_NATIVE | 01 D1 | repo_ctx；P01 |
| `DEV-OP-02` | Preimage SHA | O | REPLACE_NATIVE | 01 D1 | per-file SHA；D1 |
| `DEV-OP-03` | Write only WriteSet | O | REPLACE_NATIVE | 01 D2–D6 | diff outside=0；D3 |
| `DEV-OP-04` | Callable POS/NEG | O | REPLACE_NATIVE | 01 D3–D5 | API/Guide nine-key；P03 |
| `DEV-OP-05` | Post/diff/test raw | A | KEEP | 01 §5 | raw/exit；D2–D6 |
| `DEV-OP-06` | Receiver readback | O | REPLACE_NATIVE | 01 D4 | consumer readback；P04 |
| `DEV-ADP-01` | Guide boundary | A | KEEP | 01 §2 | advice≠grant；D3 |
| `DEV-ADP-02` | Bridge read-only | A | KEEP | 01 §2 | no write；D3 |
| `DEV-ADP-03` | BodyResolver | A | KEEP | 01 §2 | path/UTF8/dup；D3 |
| `DEV-ADP-04` | Host facade stages | A | KEEP | 01 §2 | invoked/served/consumed；D4 |
| `DEV-POST-01` | 5+1 manifest | A | KEEP | 01 D7 | 5/5 digest；D7 |
| `DEV-POST-02` | Case fixture/oracle | A | KEEP | 01 D5 | 26 assets；D5 |
| `DEV-POST-03` | Six identity | A | KEEP | 01 D7 | identity check；D7 |
| `DEV-POST-04` | Claims not actual | A | KEEP | 01 D7 | claims ledger；D7 |
| `DEV-POST-05` | Sources unchanged | A | KEEP | 01 D7 | outside canary；D7 |
| `DEV-RB-01` | New pack readback | A | KEEP | 01 D7 | guard；D7 |
| `DEV-RB-02` | Case/source join | A | KEEP | 01 D5 | join table；D5 |
| `DEV-RB-03` | SHA/fixture replay | A | KEEP | 01 D5 | replay；D5 |
| `DEV-RB-04` | Real product POS/NEG | A | KEEP | 01 D6 | independent raw；P05 |
| `DEV-IDEM-01` | Idempotency key | A | KEEP | 01 D6 | no-op；D6 |
| `DEV-IDEM-02` | Retry/UNKNOWN | A | KEEP | 01 D6 | one retry；D6 |
| `DEV-IDEM-03` | LastGood/rollback | A | KEEP | 01 D6 | restore；D6 |
| `DEV-PERM-01` | No DEV grant | A | KEEP | 01 §7 | ECP≠grant；P01 |
| `OPS-APP-01` | Applicability | A | KEEP | 02 §2 O1 | host/stage ledger；P01 |
| `OPS-EFF-01` | Host effect tokens | H | REPLACE_NATIVE | 02 O1 | unknown reject；O1 |
| `OPS-PRE-01` | Precondition 1 | O | REPLACE_NATIVE | 02 O1 | HostID/entry；O1 |
| `OPS-PRE-02` | Precondition 2 | O | REPLACE_NATIVE | 02 O1 | principal/ACL；O1 |
| `OPS-PRE-03` | Precondition 3 | O | REPLACE_NATIVE | 02 O1 | grant；O1 |
| `OPS-PRE-04` | Precondition 4 | O | REPLACE_NATIVE | 02 O1 | policy/epoch；O1 |
| `OPS-PRE-05` | Receiver ABI | A | KEEP | 02 O1/O5 | receiver ABI；O1 |
| `OPS-CON-01` | ChatGPT | O | DEFER_HOST | 02 §4 | GPT 分帳；pending |
| `OPS-CON-02` | Codex | O | REPLACE_NATIVE | 02 O1–O5 | CODEX entry；P04 |
| `OPS-CON-03` | Hermes | O | DEFER_HOST | 02 §4 | 三 child；deferred |
| `OPS-OP-01` | Install/activate | O | REPLACE_NATIVE | 02 O2 | conditional；O2 |
| `OPS-OP-02` | Register/load | O | REPLACE_NATIVE | 02 O2 | manifest/Loaded；O2 |
| `OPS-OP-03` | Bind scope | O | REPLACE_NATIVE | 02 O2 | binding；O2 |
| `OPS-OP-04` | Invoke | O | REPLACE_NATIVE | 02 O3 | argv/exit；O3 |
| `OPS-OP-05` | Serve | O | REPLACE_NATIVE | 02 O4 | served bytes；O4 |
| `OPS-OP-06` | Consume | O | REPLACE_NATIVE | 02 O5 | consumer readback；O5 |
| `OPS-POST-01` | 7-stage rows | A | KEEP | 02 §4 | 21 格；O5 |
| `OPS-POST-02` | Evidence class | A | KEEP | 02 §4 | class only；O5 |
| `OPS-POST-03` | Independent consumed | A | KEEP | 02 §4 | distinct consumer；O5 |
| `OPS-POST-04` | Hermes 3 child | A | KEEP | 02 §4 | 三列；deferred |
| `OPS-POST-05` | No install/service raw | A | KEEP | 02 §4 | NOT_OBSERVED；O5 |
| `OPS-RB-01` | Container probe | A | KEEP | 02 O1 | probe only；O1 |
| `OPS-RB-02` | Host readback | O | REPLACE_NATIVE | 02 O4–O5 | readback；O4–O5 |
| `OPS-REC-01` | Recovery 1 | O | REPLACE_NATIVE | 02 O2/O6 | uninstall/rollback；O6 |
| `OPS-REC-02` | Recovery 2 | O | REPLACE_NATIVE | 02 O6 | unbind；O6 |
| `OPS-REC-03` | Recovery 3 | O | REPLACE_NATIVE | 02 O6 | service/config；O6 |
| `OPS-REC-04` | Recovery 4 | O | REPLACE_NATIVE | 02 O6 | reconcile；O6 |
| `OPS-STOP-01` | Stop scope | A | KEEP | 02 O6 | scoped stop；O6 |
| `OPS-RESUME-01` | Typed resume | A | KEEP | 02 O6 | typed receipt；O6 |

合計 67（38＋29）；原 27 個 O 檔仍為原域 HOLD，未在本包假閉合。

---

## E4｜13 原 Case、26 assets 與真 bytes

| Case | Kind | fixture SHA-256 | oracle SHA-256 | 本輪 |
|---|---|---|---|---|
| `W1-HOST-01` | POS | `168aa72567745ebce907c951076323fd2db527e35502ec1ed912f309632a3fda` | `c92846be150cfcfbd9400e5bf23d50ad73b1ca897d10e921ad3120e387573e68` | assets verified；product `NOT_RUN` |
| `W1-HOST-02` | NEG | `9159143898ac741d8726390d60e776d3065ab40e7cfd3d48027d861c6f5ccea9` | `0af129228279a3b0fa80bd00a696175c6aa649ac7ad2e5f239b434ae0ffaa9fe` | assets verified；product `NOT_RUN` |
| `W1-HOST-03` | NEG | `1d7de26b5528bf6819d9647d52cc54e6c40c1b9adafb752f216422e6d41cc1a6` | `f91f4fbb09a9c66c2f6f6aee9848f9774bc98d3a1c9195c48c6d95aabb55cf6f` | assets verified；product `NOT_RUN` |
| `W1-HERMES-01` | POS | `8f9f784917c312770e052406e59e06aa7cc35296e176fe06cdd8ba7cd730d79a` | `101103bdcc2475558c02de4162efb5e10a93aa729db8a4b5e4315d928be9edbf` | `DEFERRED` |
| `W1-ABI-01` | NEG | `a0e18b8bfabc41c97d7b2ab368cbda5e6e310d35fd2713cbde4e62868b4de196` | `09e608cd0fae844eac6caac5e5ed5d8f100b1ef484c9f1d21066305865867f19` | assets verified；product `NOT_RUN` |
| `W1-ABI-02` | NEG | `9a62f6d1912f1ebf707202882c47916f4e9bcae1420a820fa031358a022f9ae6` | `ea236a6629f8f12222f5d90140a9d2362488b8449da998b4f1d6f1ed6ec90c2f` | assets verified；product `NOT_RUN` |
| `W1-SEC-01` | SEC | `3a0c56efde4454937375624e485e92f975f68e4862d10b9de4bc8e7c5ab0fc67` | `284675cc464e870b419ffe5e5cec54a9a252cffcf5238b32c020d5b5b45fc82d` | assets verified；product `NOT_RUN` |
| `W1-API-01` | POS | `5d94e2ddb9cce903900b66ba55e03cf434d899eab321914c0d87ce0817bf0745` | `0d3c5e3256dd4c6cfba30788c5c875222efa0fea50b5d1f842f09fd01ef97443` | assets verified；product `NOT_RUN` |
| `W1-R3-01` | POS | `c786785e330bf09060b60fe9e8767f637345331f51ab512f1e00a59d210d54bf` | `6f256ac33dafe2a7c21d7cb5a39c099578ba60427d03d280c6923277877d4be3` | bootstrap 文件層 `DOC_CHECK_ACTUAL`；產品 `NOT_RUN` |
| `W1-R3-02` | NEG | `52a2009c258c18faa016c8a4a813ca6ac10c2f3b8dc9dcdb60064ed5be0c5f3d` | `6c3b0182b44a2fc850eac9773c85047fb7ba38aae9b533bf04228c5677853aac` | assets verified；product `NOT_RUN` |
| `W1-R3-03` | NEG | `066909b9f3228bca6064a0e4437e3e06183b2e63806ab6653a2323038e0a42ba` | `ce7e1e2092f85091bf9e95337092de7af4b1df8e1e81e1718815007df5ed6caa` | assets verified；product `NOT_RUN` |
| `W1-R3-04` | EDGE | `c6cc18e9c9459f3d7ee260973cb8a4d95d246685ece659675b443120c2534a36` | `b8321db4c322bff2e04baf85d914aa4b4a5360c669987ccb5aeebf8e0aa13eda` | assets verified；product `NOT_RUN` |
| `W1-R3-05` | NEG | `59552d7790f88b818f79883d42a5894dfc8a295b80957c5d2eff06ce3f592da2` | `1c6ccd0a53d14f40058fef76ee51d89762c00290280333e3b452c37d43f10b45` | assets verified；product `NOT_RUN` |

**本輪實測**：`assets/` 26 檔，13 fixtures＋13 oracles，bytes/SHA 全 match（`assets_tree_sha256=1d71d4b14aa71a678cf10cea6a66a00d08af3fee1fc08fdf842c0c9100f3bf92`）。此為「交貨可重算」，不是原 Host raw。

---

## E5｜14 Named HOLD（原名／owner／next）

| HOLD | 本輪狀態 | Owner | 最小解除 |
|---|---|---|---|
| `W1_HOST_NINE_GRID` | OPEN_SCOPED | 各 Host Owner | 每 Host 七階段真 raw；U-017 九 child |
| `W1_PLUGIN_ALIAS` | OPEN_SCOPED | Plugin Owner | 同 manifest／LoadedID／version／entry |
| `W1_ABI_BOUND` | OPEN_SCOPED | ABI Owner | 逐欄 crosswalk＋consumer readback |
| `W1_W0_INPUT` | REQUALIFY_W1 | W1 Source Curator | 當期 H0/六檔真接收 |
| `W0_PRIMARY_RECEIPT_STALE` | HISTORICAL_SCOPED | W0 Curator | 原 receipt 差額保留，不修舊 |
| `W0-A_CASE_SELECTION` | RESOLVED_FOR_W0_GENERIC | W0 Owner | W1 不同包另選 |
| `W0-B_NOT_ADMITTED` | PROFILE_ONLY／REQUALIFY | Original Issuer | 原域 typed receipt |
| `ORIGINAL_READER_UNBOUND` | REPLACE_NATIVE／PROFILE_ONLY | Reader Owner | Generic file/Git/Reviewer 或原域 readback |
| `ORACLE_FIXTURE_UNBOUND` | REQUALIFY_BY_CASE | Case Owner | 每案真 bytes |
| `HOST_CAPABILITY_UNBOUND` | OPEN_SCOPED | Host Owner | 真本地入口／七階段 |
| `CHECKER_PUBLISHER_UNBOUND` | SPLIT_RESPONSIBILITY | Checker／Publisher | 分立 receipt |
| `SOURCE_REFERENCE_HASH_CONFLICT` | REQUALIFY_BY_SOURCE | Source Curator | 合法替換或排除受影切片 |
| `W0C_DENOMINATOR_ID_LIST_UNBOUND` | PROFILE_ONLY／OPEN | W0-C Owner | 原 ID 清單 |
| `HOLD_CR-DOC04-STATE-MAP` | PROFILE_ONLY | DOC04 Owner | 原 state-map readback |

---

## E6｜W1-D01–D09 精確替換、採納與待決

| ID | 原條款／defect | 本包 replacement | 落點 | 採納狀態 |
|---|---|---|---|---|
| `D01` | W1M §00.6／§05.B／§08.6／§11.5 vs §01.4／§03.B／§07.8：W1 只 READ/DRAFT，DEV/OPS 全屬 W2；與正式 reader/contract 建造矛盾 | 編包：READ/DRAFT/local check。W1 產品：在 Owner 同域 scoped grant＋真 ACL/root 下，允許必要本地 DEV（reader／TPM／Guide／Bridge／consumer）與最小 OPS（invoke／必要可逆 activation／restore）；W2 另驗通用 protected effect；無權不做；install 非預設 | 00 §2/§10；01 D1–D7；02 O1–O6；04 | `ADOPTED_SCOPED_THIS_ROUND`（限 W1；不擴 OS/Repo/Host） |
| `D02` | §02.4B `PROFILE_ONLY` 可能連 Generic 安全責任一起刪 | 原域 receipt 才 Profile；live root/preimage/WriteSet/callable/ACL/post/readback/recovery/未知 fail-closed 全保留；27 原域 HOLD 不假 close | 01 §2 38 列；02 §2 29 列 | IMPLEMENTED |
| `D03` | package/source/manifest/source-set/context digest 混用；六身份自循環 | 分域 digest；05 只記五 MD file SHA；外置 seal 記 05 SHA；MD 不嵌最終 05 SHA；第六鍵讀時合成；legacy 另算 | 00 §4；05 digest_contract；E10 | IMPLEMENTED |
| `D04` | 舊 API 寫死 15 檔；缺 OriginalReader 即停 Generic；無新 schema 映射 | schema-dispatch 直讀六檔 05；BodyResolver 真 file/Git/span；Generic 由真來源＋Reviewer 證；舊 15 只 legacy；原 canonical `UNBOUND` | 00 §6.3；01 D2；03 N02 | IMPLEMENTED |
| `D05` | Guide 四函式與 NF 名稱不同；九鍵曾單 evidence_sha 承載 | 兩組原名＋逐欄 crosswalk；九鍵逐鍵真 producer/verifier；缺期／單 SHA／caller bool → `DELTA_UNVERIFIED`；跨域 → `NEW_SUBJECT_REVIEW_REQUIRED`；同域實質差 → `NEW_MATERIAL_EVIDENCE`；全同才 `PARK_NO_DELTA` 候選 | 00 §6.2；03 N03；04 SPEC | IMPLEMENTED |
| `D06` | 七階段被當固定 install 順序；W1_EXECUTION_READY 以最終 consumed 自扣 | 逐階真證；內建入口 `REASONED_NA_NATIVE_ENTRY`（非 PASS）；bootstrap 接收是准入前件，最終 product consumed 是後驗；不以 P04/P06 倒卡 P03 | 00 §7；02 §4；04 DONE | IMPLEMENTED |
| `D07` | 「13 案外不新增分母」可能省 Guide/TPM/六檔新子義 | 13 原 ID／語義／POS/NEG/child 不減；N01–04/N10/N11 具名子例、獨立分母；N05–09/N12 保本波必要與後波全量 | 03 §2–§3 | IMPLEMENTED |
| `D08` | 六冊 author current≠正式採納；W1M `NOT CURRENT`；PLAN4 §16.2 需有效裁決 | 本輪只承接 W1 同域主用＋scoped construction；不宣七冊／全系統採納；`WORKSPACE_REVISION_PENDING_ADOPTION` 原樣記；其他 scope 新裁決 | 00 §0；E9 | `ADOPTED_SCOPED_THIS_ROUND`（限 W1） |
| `D09` | 歷史 667/694、絕對路徑、CH-07 identity-only、CRLF 混帳 | 當期 C0/H0/consumer pins；可攜相對 locator＋source root；fresh receive 重算；CH-07 只 identity；CRLF 不 normalize | 00 §9；05 sources；03 N11 | IMPLEMENTED |

**D01/D08 的效力邊界**：本次 Owner 裁決只覆蓋「W1 六檔主用＋同域受界可逆施工」；不覆蓋七冊正式採納、W2–W4、OS/Repo policy、外部 Host、public release。若上位有效限制與此衝突，以更嚴格者為準，並提出一次最小受影裁決請求，不默認擴權。

---

## E7｜PKG-01–05 實際檢測、mutation 與 raw

### E7.1 五組共用驗收

| PKG | 檢查（實際） | 結果 | 證據 |
|---|---|---|---|
| `PKG-01` 結構／身份／bytes | 6 檔存在、UTF-8 strict、05 duplicate/NaN 拒、5 MD SHA/bytes/lines、identity、assets/sources、seal | PASS | `guard_result.json` |
| `PKG-02` 高保留／雙向追溯 | 38＋29 ID、13 Case、6 WP、12 ACC、14 HOLD、D01–09、NF01–10、SM01–07、Guide/Bridge/TPM/原分母 | PASS（文件層）；產品 `NOT_RUN` | 00–03、E2–E5 |
| `PKG-03` Native-first／依賴／治理 | 無 universal OriginalReader/15 檔/HERMES/W2/W4 hard gate；P01→P06 拓樸；未知 effect fail closed；單人 Owner；D01/D08 scoped | PASS | 00 §4/§5/§11；guard DAG |
| `PKG-04` 可施工／自動化／安全 | 六 WP dry-consume；67 per-ID 操作；13 案＋子例 fixture/oracle；per-op pre/post/readback/UNKNOWN；bootstrap 真接收；mutation 12 項；reader 16/16；首個 `inspect` 真操作 | PASS（文件＋隔離＋entry）；最終產品 `NOT_RUN` | 01/02/03；`bootstrap_consume.json`；`mutation_results.txt`；`nf_r2_inspect_probe.json` |
| `PKG-05` 交付／誠實／收斂 | 主包＋附錄實讀、seal、raw/claim/NotCovered、adoption/ACL/entry gap、文件 vs 產品分帳 | PASS | E8–E10 |

### E7.2 隔離 mutation（副本；真包未改）

| # | Mutation | 期望 | 實際 token |
|---|---|---|---|
| 1 | 00 加 1 byte | DIGEST_MISMATCH | `DIGEST_MISMATCH` |
| 2 | 01 轉 CRLF | EOL／DIGEST | `EOL_NON_CANONICAL` |
| 3 | 刪 03 | PACK_INCOMPLETE | `PACK_INCOMPLETE_LOCAL` |
| 4 | 05 duplicate key | STRICT_JSON_REJECT | `STRICT_JSON_REJECT` |
| 5 | 05 NaN | STRICT_JSON_REJECT | `STRICT_JSON_REJECT` |
| 6 | 05 `../evil.md` | PATH／INCOMPLETE | `PACK_INCOMPLETE_LOCAL` |
| 7 | 02 project_id | IDENTITY_MISMATCH | `IDENTITY_MISMATCH` |
| 8 | 01 刪 1 DEV row | ID_SET_INCOMPLETE | `ID_SET_INCOMPLETE` |
| 9 | 05 DAG 加 P06→P01 | DAG_CYCLE | `DAG_CYCLE` |
| 10 | 05 自嵌 pack_manifest_sha256 | MANIFEST_SELF_EMBED | `MANIFEST_SELF_EMBED` |
| 11 | fixture 加 1 byte | ASSET_DIGEST_MISMATCH | `ASSET_DIGEST_MISMATCH` |
| 12 | upstream `pack_sha256` 改 0 | UPSTREAM_PIN_MISMATCH | `UPSTREAM_PIN_MISMATCH` |

**總計 12/12 期望拒收**（`evidence/raw/mutation_results.txt`）。此證明 guard 對結構／digest／身份／DAG／asset／upstream pin 的 fail-closed；不證明產品語義。

### E7.3 W1 reader 首個合法操作（W1_EXECUTION_READY 證據）

| 項 | 實際 |
|---|---|
| worktree | `C:\Projects\Agent_Workspace\FHS-5_W1_NF_r2` |
| branch／base | `codex/w1-nf-r2-20261125`／`c2d8084ba24dd8df3fa62259bba496f4fb9caa85` |
| entry | `W1/impl/w1_nf_reader.py`（`inspect`／`explain`／`render`／`compare`／`resolve`／`selftest`） |
| tests | `W1/check/test_w1_nf_reader.py`：**16/16 OK**（含 10 個 mutation NEG） |
| selftest | 4/4 PASS |
| first op | `python W1/impl/w1_nf_reader.py inspect --pack <pack> --out W1/evidence/nf_r2_inspect_probe.json` |
| result | 5 files／38 DEV／29 OPS／13 cases／26 assets／42 sources／14 holds；DAG `P01→P02→P03→P04→P05→P06`；exit 0 |
| claim | `W1_EXECUTION_READY=READY`；`W1_PRODUCT_CONSUMED=NOT_RUN`；`W1_NF_VALIDATED=NOT_RUN` |

### E7.4 Raw locator

| Raw | 路徑 |
|---|---|
| Guard 結構結果 | `evidence/raw/guard_result.json` |
| Mutation 結果 | `evidence/raw/mutation_results.txt` |
| SourceFreeze | `evidence/raw/source_freeze.json` |
| Host probe | `evidence/raw/host_probe.json`、`host_probe.txt` |
| Bootstrap 接收 | `evidence/raw/bootstrap_consume.json` |
| 候選缺陷 | `evidence/raw/candidate_findings.json` |
| 最終讀回 | `evidence/raw/final_readback.json` |
| 外置 seal | `evidence/SEAL.json` |

### E7.5 Walkthrough 與 actual 分帳

| 類 | 本輪 |
|---|---|
| `DOC_CHECK_ACTUAL` | 5+1、strict JSON、SHA/bytes/lines、identity、ID set、DAG、assets、sources、seal、11 mutations |
| `BOOTSTRAP_CONSUME_ACTUAL` | 05→00→01/02/03/04 真讀、next/op/inputs/expected/stop |
| `DESIGN_WALKTHROUGH` | 四 API、Guide 九鍵、TPM 四契約、BodyResolver、Host O1–O6、13 案 runner |
| `HISTORICAL_REPORTED` | 舊 W1 67 closure、22/22、17/17、21 格 0 consumed、W0 44/803/694 |
| `PRODUCT_NOT_RUN` | 全部 13 案產品、真 served/consumed、第二包、GPT/HERMES、W2–4、Independent、Release |

---

## E8｜候選 preimage、缺陷與修補前後

| 檔 | 候選 bytes／SHA | 定案 bytes／SHA |
|---|---|---|
| `00_W1_PI_PD.md` | 11,684／`d2975f5a…` | 34,565／`f6dd84cb…` |
| `01_W1_DEV_ECP.md` | 9,107／`a9b30e83…` | 20,729／`772557b0…` |
| `02_W1_OPS_ECP.md` | 7,022／`a01d84b5…` | 12,290／`14b1571a…` |
| `03_W1_TQAEP.md` | 6,371／`1f2ea48b…` | 19,804／`66a53d28…` |
| `04_W1_START_THIN_PROMPT.md` | 1,892／`167cbf7b…` | 10,028／`a4b0f9cb…` |
| `05_W1_SOURCE_MANIFEST.json` | 16,518／`0ddcf3c0…` | 35,780／`a7b1ef35…` |

**10 個 finding（全文見 `candidate_findings.json`）**：

| ID | Severity | 摘要 | 修補 | 重驗 |
|---|---|---|---|---|
| `F-01` | HIGH | 5 MD `lines` 全部 +1；E7 誤稱 digest mismatch | splitlines 重算，seal 更新 | guard DIGEST PASS |
| `F-02` | HIGH（本輪 probe 範圍錯誤，非候選缺陷） | 候選 `W1-HARNESS` 11,420／`33848417…` 對應 repo 檔；初次只查 Downloads 的 11,369／`64f4c85b…` 而誤判 | 以 repo canonical（11,420／`3384…`）為 source；Downloads 副本另註血緣 | source freeze 42/42；repo copy match |
| `F-03` | HIGH（本輪 probe 範圍錯誤，非候選缺陷） | matrix/report/holds/impl 在 repo 本地存在，hash 與候選一致；初次只查 Downloads 而誤標 remote | 改 LOCAL_VERIFIED；W1M §02.4B 仍作交叉讀 | guard sources PASS；matrix 67 rows parsed |
| `F-04` | MEDIUM | W0M path 是標籤，不是 locator | 真路徑＋重算 | guard sources PASS |
| `F-05` | CRITICAL | 01/02 67 列多為 placeholder，無 per-ID operation | 38/29 全列操作 | guard DEV/OPS 計數 |
| `F-06` | HIGH | 03 13 案缺 requirement/child/expected 明細；assets 外置 | 擴表＋bundled 26 assets | guard assets 26 |
| `F-07` | HIGH | 04 只有 25 行，缺 SOURCE/EXECUTE/HARNESS/STOP/RESUME | 重寫完整入口 | guard sections PASS |
| `F-08` | CRITICAL | 候選 E7 記 FAIL（DEV 37/38、缺 HOST-01、universal gate）卻 E9 宣布 AUTHOR_PASS；重測不符 | 以真 guard＋12 mutation 取代；verdict 分層 | guard PASS；mutation 12/12 |
| `F-09` | HIGH | claim 仍 AUTHOR_DOCUMENT_ONLY，與 Owner 預授權衝突；且無限制清單 | 記 OWNER…；scoped primary；後續另以真 repo worktree／reader 證據宣 `W1_EXECUTION_READY=READY` | guard claim PASS |
| `F-10` | MEDIUM | 05 缺 digest_contract/dag/holds/readiness/product_scope/seal | 補齊＋外置 seal | guard 全 PASS |

**LastGood**：候選原檔仍在 `W1_Native-first_交付` 唯讀未改；本定案是新的隔離根。來源與原 oracle 未變。

---

## E9｜採納、ACL、入口缺口、readiness 與下一合法動作

| 缺口 | 實際 | 影響 | 下一合法動作 |
|---|---|---|---|
| 七冊正式採納 | `WM__W0M_W1M_ADMISSION.md`：`WORKSPACE_REVISION_PENDING_ADOPTION` | 不改 W1 文件主用；不能宣全系統 M-DONE | 若 W2+ 需七冊，Owner 一次受影採納；W1 不重簽 |
| 產品 repo 寫 ACL | 原樹寫 DENIED；**W1 worktree `FHS-5_W1_NF_r2` WRITE_OK**（本輪 escalated 寫入） | W1 DEV 可施工；原樹未改 | 已在 worktree 進行；不再重複授權 |
| W1 entry | `W1/impl/w1_nf_reader.py` 已建；TPM 四契約／Guide 九鍵／獨立 consumer 未建 | reader invoke/serve 可；final consumed 未 | D3–D4 在 worktree 接續 |
| 13 案產品 | 未跑 | 無 W1_NF_VALIDATED | 真 runner/raw＋獨立 checker |
| 第二包 | 未選 | 通用性未證 | P01 選非 briefcheck 不同 subject/scope |
| GPT CHAT/WORK／HERMES | 無掛載 | 各自 pending/deferred | 各自 Host 資格 |
| 遠端 matrix/impl | repo 本地已有；初次 probe 只查 Downloads 誤標 | 已改 local verified；無假 digest | 以 repo 固定 commit 讀；push 前驗 remote |
| Windows link 攻擊 | 無 symlink privilege | 真防護未驗 | 具權 Windows host 另測；不以 WSL2 冒 |

**Readiness**：

| 狀態 | 值 |
|---|---|
| `W1_TECHNICALLY_READY` | H0 已記錄；本輪 pins 重算一致 |
| `W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION` | 文件／主用：已達（guard＋PKG） |
| `BOOTSTRAP_CONSUME_ACTUAL` | 已達（05→00→01/02/03/04 讀回） |
| `W1_EXECUTION_READY` | **READY**：worktree 寫權、reader entry、16/16 tests、首個 `inspect` 操作、真 inputs 已具 |
| `W1_NF_VALIDATED`／Independent／Release | `NOT_RUN`／`NOT_ADMITTED` |

**第一合法產品操作（已執行）**：worktree D1（root/HEAD/ACL/preimage/WriteSet）＋D2 reader 已跑；`inspect` 真回 5／38／29／13／26／42／14。下一步 D3 TPM/Guide 九鍵、D4 獨立 consumer／第二包、D5 13 案。若真 scope／Host 權不足，停受影，不以文件 PASS 代替。

---

## E10｜05 外置 seal、五 MD 與 assets 實測

| 檔 | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `00_W1_PI_PD.md` | 34,565 | 349 | `f6dd84cbfad05e8e3d452f0e6f5c6f9539e149573bec51c396c60b91bf76f8d1` |
| `01_W1_DEV_ECP.md` | 20,729 | 200 | `772557b0749759ca2893b72ed99feb049cf38446e8100f8713bcb38ab4d499af` |
| `02_W1_OPS_ECP.md` | 12,290 | 110 | `14b1571ab26474c325c2f001c8fddee7cc81c4abbec79152e669c6f5766d44e5` |
| `03_W1_TQAEP.md` | 19,804 | 213 | `66a53d2854debafc599b8a4f6611aa44236d099d380d93828c43aa20e227c691` |
| `04_W1_START_THIN_PROMPT.md` | 10,028 | 120 | `a4b0f9cb750d8374ef649c78215d489c434706eb05693e5f63b92b6d17905eb9` |
| `05_W1_SOURCE_MANIFEST.json` | 35,780 | 987 | `a7b1ef358c8e7a9740e5f1ef487ecd7777ded0a1f8246daee562cba909810a80` |

**外置 seal**：`evidence/SEAL.json`。

| 欄 | 值 |
|---|---|
| `pack_manifest_sha256` | `a7b1ef358c8e7a9740e5f1ef487ecd7777ded0a1f8246daee562cba909810a80`（= sha256(raw 05)） |
| `pack_files` | 5 MD bytes/SHA/lines 全 match（本表） |
| `asset_count` | 26 |
| `assets_tree_sha256` | `1d71d4b14aa71a678cf10cea6a66a00d08af3fee1fc08fdf842c0c9100f3bf92` |
| `source_set_sha256` | `8f2e484f46ff99bff9e1a0e6bf9dada0daea5ad2ee3b5357deb72435db32636c`（42 local 真 digest 定義） |
| `verdict` | `W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION` |
| `w1_execution_ready` | `READY` |
| `product_actual` | `NOT_RUN` |

**封存拓撲**：sources/assets 真 bytes → 五 MD → 05 raw → 外置 seal／本附錄。五 MD 不嵌最終 05 SHA；05 不嵌 seal SHA；seal 不回填主包。`manifest_self_hash=EXTERNAL_RECORD_ONLY`。

**讀回**：以上 digest 由 `evidence/raw/final_readback.json` 從交付根重新讀取後計算；guard 以同根重跑 PASS。若後續修改任一 MD，必須重算 05 受影欄與 seal，不能沿用本表。

---

## E11｜實際 verdict、NotCovered、停止點

**Verdict**：`W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`。
**Reason**：六檔完整可讀；D01–09 實質落地；38/29/13/6/12/14 與 Guide/Bridge/TPM 分母保；PKG-01–05 文件必要義務通過；5+1 digest/identity/DAG/assets/sources/seal 可重算；12 個 mutation fail-closed；W1 reader 16/16＋首個 `inspect` 真操作；主用／同域施工授權及 `W1_EXECUTION_READY=READY` 已由本輪 Owner 裁決與真 ACL 記錄；最終產品 actual 未冒 PASS。

**NotCovered**：13 案真跑、完整 TPM/Guide 九鍵、獨立 consumer 與第二不同包、CODEX 最終 served/consumed、GPT CHAT/WORK、HERMES 三 child、Windows symlink/reparse 真攻擊、W2–W4、Independent、Release、public push（token 已備但尚未執行）。

**本輪停止點**：文件主用、bootstrap、W1 reader entry、首個 `inspect` 操作完成；`W1_EXECUTION_READY=READY`。D3–D5 未完成，故不得以本附錄或六檔替代 W1 CLOSEOUT/HANDOFF，也不得把文件 PASS 當 `W1_NF_VALIDATED`。

**Next**：`04_W1_START_THIN_PROMPT.md` → D3 TPM/Guide 九鍵 → D4 獨立 consumer＋第二包 → 13 案／N01–04/N10/N11 → P06／Handoff → commit/push `codex/w1-nf-r2-20261125`。若真 Host 權不足，只停受影，不逐 WP 重簽。
