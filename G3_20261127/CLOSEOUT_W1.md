# W1 CLOSEOUT（G3，2026-11-27）

- candidate：`W1-G3-PCNF-r2`
- source manifest SHA-256：`f00b4ee93611e738e409d40758aa320b0bfec3ef0a01fea04dbf5bcb9f1566dc`
- pack tree SHA-256：`22fa47302ebcbb185b98b2c5d0a2bfa90b68becf31cd9f393be4d2ebdd669004`
- case set SHA-256：`9e5c6a83b719c400c8d38e82156f494de8d3da65e9ccf32cef3c6c2b8dfd8262`
- raw：`G3_20261127/runs/w1/`；summary：`runs/w1/W1_RESULT.json`

## 13 原案

**12 PASS＋1 DEFERRED**（`W1-HERMES-01`：真 falsifier 觀測到 `REQUIRED_CHILD_MISSING`，但 Hermes host 未綁，POS 不宣）。

| 案例 | 觀測 |
|---|---|
| W1-R3-01 | 5 MD＋05＋26 assets＋13 cases＋13 WO；identity／tree／case-set 重算一致 |
| W1-HOST-01 | CODEX native 七階段 ledger：Selected/Loaded/Installed(REASONED_NA)/Bound/Invoked/ActualServed/Consumed；consumer readback SHA `0bb1ffe49e11271a…` |
| W1-HOST-02 | 跨 Host 代償 → `HOST_ABI_DRIFT` |
| W1-HOST-03 / R3-02 | skill 證據 → `HOST_PENDING`（含本輪 minimal repair，見下） |
| W1-API-01 | 5 檔、84 clauses、167 NEG markers、27 exceptions；span 全有效 |
| W1-ABI-01/02 | `EXPLICIT_REVIEW_REQUIRED`／`LOSSY_MIGRATION` |
| W1-SEC-01 | 內嵌指令標 `UNTRUSTED_SOURCE_DATA`，未執行、未升權 |
| W1-R3-03/04/05 | `ABI_LOSSY_CROSSWALK`／`WORKSPACE_DRIFT_BOUNDED`／`EVIDENCE_LAUNDERING` |

## Guide／Host／ECP

- Guide 九鍵：same→`PARK_NO_DELTA`；delta→`NEW_MATERIAL_EVIDENCE`（changed `['world_raw_sha']`）；缺期→`DELTA_UNVERIFIED`。
- Host 21 格：本輪 observed 7/21（僅 CODEX 七階段）。
- 67 ECP ledger：本輪真 observed **15/67**；其餘沿用 prior disposition（PARTIAL 36／REUSE_VERIFIED 13／DEFERRED 2／REASONED_NA 1）。

## Minimal repair（FirstFail → 修復 → 重驗）

`W1-HOST-03` 首次把 skill-only `Invoked` 判成 `HOST_ABI_DRIFT`（facade 的 deny hint 缺 Invoked）。修補 `W1/impl/host_facade.py`：新增 `Invoked: (skill, skill_bytes, readme)` 與 `HOST_PENDING` token；`python -m unittest discover -s W1\check` **115 tests OK**；重跑 HOST-03 得 `HOST_PENDING`。

## 判定

`W1_SCOPED_PARTIAL`。12 案與 API／Guide／host/ECP 本輪真跑；`W1_NF_VALIDATED=false`（HERMES 未綁、67 列未全 observed）。
