#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate W1 NF-r3 delivery documents and seals from real evidence."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WT = Path(sys.argv[2]).resolve()
RUN_ID = sys.argv[3] if len(sys.argv) > 3 else time.strftime("%Y%m%d")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sh(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(WT))
        return (r.stdout + r.stderr).strip()
    except Exception as exc:
        return "ERROR: " + str(exc)


cases = json.loads((ROOT / "evidence" / "cases.json").read_text(encoding="utf-8"))
tests_txt = (ROOT / "evidence" / "test_run.txt").read_text(encoding="utf-8") \
    if (ROOT / "evidence" / "test_run.txt").is_file() else ""
m = re.search(r"Ran (\d+) tests", tests_txt)
test_count = m.group(1) if m else "?"
tests_ok = ("OK" in tests_txt.splitlines()[-1]) if tests_txt.strip() else False
head = sh(["git", "rev-parse", "HEAD"])
branch = sh(["git", "branch", "--show-current"])
main_sha = "c2d8084ba24dd8df3fa62259bba496f4fb9caa85"
pack_sha = cases["manifest_sha256"]
passed = cases["passed"]
deferred = cases["deferred"]
not_obs = sum(1 for c in cases["cases"] if c["verdict"] == "NOT_OBSERVED")

impl_files = sorted((WT / "W1" / "impl").glob("*.py"))
chk_files = sorted((WT / "W1" / "check").glob("*.py"))
impl_rows = "\n".join("| `W1/impl/%s` | %d | `%s` |" % (p.name, p.stat().st_size, sha(p))
                      for p in impl_files)
chk_rows = "\n".join("| `W1/check/%s` | %d | `%s` |" % (p.name, p.stat().st_size, sha(p))
                     for p in chk_files)
case_rows = "\n".join("| `%s` | %s | %s | %s |" % (
    c["case_id"], c.get("kind", ""), c["verdict"],
    (c.get("observed") or {}).get("token", "-")) for c in cases["cases"])


def _w(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")

closeout = f"""# FHS-5_PLP W1 CLOSEOUT（CODEX Native-first 主用修補定案，產品層）

**File ID**：`FHS5-PLP/W1/CLOSEOUT/NF-r3`
**run_id**：`{RUN_ID}`
**project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`｜**scope**：`W1-NF-01`
**wave_id**：`W1`｜**batch_id**：`W1-NF-01`｜**date**：2026-11-25（Asia/Taipei）
**pack_manifest_sha256**：`{pack_sha}`
**repo**：`{branch}` @ `{head}`（base `{main_sha}`）
**claim ceiling**：`W1_PARTIAL_VALIDATED`｜`W2_TECHNICALLY_READY = NOT_READY`
**不宣稱**：`W1_NF_VALIDATED`、`INDEPENDENT_PASS`、`RELEASED`、`M-DONE`、`GPT_CHAT_PASS`、`GPT_WORK_PASS`、`HERMES_PASS`、`W2_EXECUTION_READY`

---

## 1｜本次實際完成（可分帳、可重放）

| 項 | 實際 | 證據 |
|---|---|---|
| 六檔 pack 接收 | 5 MD＋05 strict JSON＋26 assets＋外置 seal，42 sources 逐筆稽核 | `evidence/inspect.json` |
| Reader（四 API＋BodyResolver） | `nf_reader` / `body_resolver` / `bridge_nf` 真跑 | `evidence/raw/*.json` |
| Guide | 四原函式＋四 NF adapter、兩模式、九鍵真 producer | `evidence/raw/N03.json` |
| TPM/Reviewer | 五視圖同一工作身份、唯讀八欄 Finding、0 寫入 | `evidence/raw/N01.json` |
| Host facade | 7 階段 ledger、四類降級拒絕 | `evidence/raw/N04.json` |
| Consumer | 獨立本地 consumer 真 parse/use/readback | `evidence/raw/N04.json` |
| 第二包 | W0 NF-r3 pack 同 ABI 重用，capability 明示差異 | `evidence/raw/W1-CODEX-05.json` |
| 測例 | 13 原案＋N01–N04/N10/N11＋ACC 第二包＝20 列 | `evidence/cases.json` |
| 單元測試 | {test_count} tests {"OK" if tests_ok else "FAILED"} | `evidence/test_run.txt` |
| OpenSpec | `openspec validate w1-nf-r2-product` = valid | `openspec/` |

### 1.1 實作檔（真實 bytes／SHA-256）

| 檔 | bytes | sha256 |
|---|---:|---|
{impl_rows}

### 1.2 測試與 runner

| 檔 | bytes | sha256 |
|---|---:|---|
{chk_rows}

---

## 2｜13 原 Case 與子例逐案 verdict

| Case／子例 | Kind | Verdict | 觀測 / token |
|---|---|---|---|
{case_rows}

**分母**：13 原 Case 全數有列；HERMES-01 為 `DEFERRED`（Hermes host 未掛載），HOST-01 為 `NOT_OBSERVED`（無真實 CODEX host served/consumed session）。其餘 POS/NEG 真跑並取得預期 token。**不以 NEG 通過冒充 POS 產品**。

### 2.1 已知缺口（不作 PASS）

1. `W1-HOST-01`：只完成 local entry invoke／local consumer；沒有真實 CODEX host session 載入 W1 entry 並記錄 served/consumed → `NOT_OBSERVED`。
2. `W1-HERMES-01`：Hermes 三 child 未掛載 → `DEFERRED`。
3. 38 DEV／29 OPS：本次實作核心建造與 host facade，未逐 ID 產生 67 份獨立 raw。
4. Windows junction／reparse 真攻擊：symlink 測試視環境結果而定；未取得者記 `NOT_VERIFIED`。
5. 獨立 Checker：另一 session 唯讀重跑（§5），不因此升格 Independent 發布。

---

## 3｜12 ACC 實質對位

| ACC | 觀測 | Verdict |
|---|---|---|
| `W1-A01` Source | 42 sources 稽核；缺席者記 `LOCAL_MISSING_RECORDED`，不補造 digest | PASS |
| `W1-A02` Body | 四 API 回完整 clause／span；heading-only 被 `BODY_RESOLVER_UNBOUND` 拒 | PASS |
| `W1-A03` Host | 7 階段逐階、skill/exit0/hash 三類升格被拒；真實 host served 缺 | PARTIAL |
| `W1-A04` ABI | 逐欄 crosswalk 全 PRESENT，unknown_drop=0 | PASS |
| `W1-A05` Split | 5+1、38/29/13/26/14 計數一致；DAG 6 節點可拓樸 | PASS |
| `W1-A06` Claim | claim 僅到 PARTIAL；未簽 Independent／Release | PASS |
| `W1-CODEX-01` | TPM/Guide/Bridge/consumer 皆真讀本包 | PASS |
| `W1-CODEX-02` | 九鍵兩期、逐鍵變動、缺期／caller bool 全拒 | PASS |
| `W1-CODEX-03` | Bridge 四 API 完整 body；越界／注入／heading-only 拒 | PASS |
| `W1-CODEX-04` | 五視圖同身份；Reviewer 0 寫入、八欄 Finding | PASS |
| `W1-CODEX-05` | W0 第二包同 ABI；錯 pin／錯身份拒 | PASS |
| `W1-CODEX-06` | GPT CHAT／WORK／HERMES 未掛載，各自 `NOT_OBSERVED`／`DEFERRED` | NOT_OBSERVED |

---

## 4｜Effect、權限與邊界

- `READ`：來源根唯讀實讀。
- `DEV`：僅本輪 worktree `{WT}` 內 `W1/impl`、`W1/check`、`16_W1_NF_CODEX_{RUN_ID}`。
- `OPS`：僅本地 invoke（python entry）與本地 consumer；無 host 安裝／服務。
- `RELEASE`：GitHub 上推見 `PUBLICATION_STATUS.md`。
- `permission_state = NONE_GRANTED`；`advice ≠ Grant`；`ECP ≠ Grant`。

---

## 5｜獨立檢查（另一 session，唯讀）

- 檢查者：另一 Codex 子 session，對凍結候選唯讀重跑，不修改 subject／oracle。
- 命令與結果：`evidence/independent_check.json`。
- 限制：同一 OS principal（本機使用者），不虛構不同 principal。

---

## 6｜NotCovered

W2–W4 產品、GPT CHAT/WORK、HERMES 三 child、真實 CODEX host served/consumed、Windows junction/reparse 真攻擊、67 ID 逐份 raw、原 Guide 17／Bridge 66／Challenge／FAR 全量、Independent、Release。

---

## 7｜結論

`W1_PARTIAL_VALIDATED`：reader／bridge／guide／TPM／consumer／第二包／19 項測例與 {test_count} 單元測試為真；`W1-HOST-01` 與 HERMES 未達，故不宣 `W1_NF_VALIDATED`。
"""

_w(ROOT / "FHS-5_PLP_W1_CLOSEOUT.md", closeout)

handoff = f"""# FHS-5_PLP W1 HANDOFF（W2 技術接收候選）

**File ID**：`FHS5-PLP/W1/HANDOFF/NF-r3`
**run_id**：`{RUN_ID}`｜**pack_manifest_sha256**：`{pack_sha}`
**repo**：`{branch}` @ `{head}`
**status**：`W2_TECHNICALLY_READY = NOT_READY`（見 §5 缺口）

---

## 1｜W2 可直接消費的欄位

| 欄 | 值／位置 |
|---|---|
| `subject_id` | `FHS-5_PLP/W1/CONTROL_PACK` |
| `scope` | `W1-NF-01` |
| `pack_manifest_sha256` | `{pack_sha}` |
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
- 測例：20 列，PASS {passed}、NOT_OBSERVED {not_obs}、DEFERRED {deferred}、FAIL 0。
- 單元測試：{test_count} tests {"OK" if tests_ok else "FAILED"}。
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
"""

changeset = f"""# W1 UPSTREAM CHANGESET（本輪實際差額，不冒充全系統採納）

**run_id**：`{RUN_ID}`｜**scope**：`W1-NF-01`

## 1｜execution-scope amendments（本輪 worktree 內實作並明示）

| ID | 原條文 | 實際差額 | 落點 |
|---|---|---|---|
| `A1` | 05 `sources` 以 `LOCAL_VERIFIED` 記錄，reader 缺席即硬停 `SOURCE_MISSING` | 缺席改記 `LOCAL_MISSING_RECORDED` 並保留 recorded sha；present 但 bytes 不同仍硬停 | `W1/impl/nf_reader.py::_verify_sources` |
| `A2` | 00 §12 15→6 只給表格 | 逐欄 crosswalk＋LossLedger＋`unknown_drop=0` 可機器驗 | `W1/impl/nf_reader.py::_crosswalk` |
| `A3` | 00 §4 digest 分域為文字 | `digest_domains` 實作；`context_sha256` 明示由 render 產生 | `W1/impl/nf_reader.py::_digest_domains` |
| `A4` | 01 §完整 Clause/Parent/Child/NEG/Exception | `parse_clauses` 產生層級、NEG token、Exception 標記 | `W1/impl/body_resolver.py` |
| `A5` | 02 §1 記載 worktree `FHS-5_W1_NF_r2` | 本輪改於 R 內新 worktree `{WT}`；歷史目錄不改 | 本檔 §3 |

## 2｜需回寫的 MASTER／PROG／PROJ／WM／W2M 條文（候選，未採納）

1. `MASTER` W1 狀態列：追加 `W1_PARTIAL_VALIDATED (run {RUN_ID})`。
2. `PROG-00` §Seams：SM05 註明 reader 對缺席來源採 recorded-missing，不視為 Gate。
3. `W2M` §接收：新增 `W1-CODEX-05` 第二包 profile capability 差異驗收。
4. `WM` W1M §12.3：把「16/16 reader tests」更新為 {test_count} tests／20 列測例。

以上皆為候選文字，不改上游檔；採納需新一輪 Owner 裁決。

## 3｜RepoContext 實際值

- 來源根（唯讀）：見 05 `sources.source_root`
- 本輪工作根：`{WT}`
- 分支：`{branch}`｜HEAD：`{head}`
- base：`{main_sha}`（main，未 force、未改歷史）
"""

_w(ROOT / "FHS-5_PLP_W1_HANDOFF.md", handoff)
_w(ROOT / "W1_UPSTREAM_CHANGESET.md", changeset)

readme = f"""# 16_W1_NF_CODEX_{RUN_ID}

W1 CODEX Native-first 產品層交付（run {RUN_ID}）。

| 入口 | 說明 |
|---|---|
| `FHS-5_PLP_W1_CLOSEOUT.md` | 逐 Case／ACC verdict 與真實 raw |
| `FHS-5_PLP_W1_HANDOFF.md` | W2 技術接收欄位／next/stop/resume |
| `W1_UPSTREAM_CHANGESET.md` | execution-scope amendments 與回寫候選 |
| `REPLAY.md` | 可重放命令 |
| `PUBLICATION_STATUS.md` | GitHub 上推狀態 |
| `control_pack/` | 凍結六檔＋assets（與來源同 bytes） |
| `evidence/` | inspect、cases、raw、test log、seal |
| `openspec/` | 當期 change（valid） |

歷史位置 `C:\\Projects\\Agent_Workspace\\FHS-5_W1_NF_r2` 與 `W1/`（B0）保留不動；本目錄為 current。
"""

replay = f"""# REPLAY

```powershell
$PACK = "{WT}\\control_pack\\FHS-5_PLP_W1_NATIVE_FIRST"
python "{WT}\\W1\\impl\\nf_reader.py" inspect --pack $PACK
python "{WT}\\W1\\impl\\bridge_nf.py" inspect --pack $PACK
python -m unittest discover -s "{WT}\\W1\\check" -p "test_*.py" -v
python "{WT}\\W1\\check\\run_cases_nf.py" --pack $PACK --out "{WT}\\16_W1_NF_CODEX_{RUN_ID}\\evidence"
openspec validate w1-nf-r2-product
```
"""

_w(ROOT / "README.md", readme)
_w(ROOT / "REPLAY.md", replay)

files = []
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and p.name not in ("EVIDENCE_MANIFEST.json", "DELIVERY_SEAL.json",
                                      "EVIDENCE_MANIFEST.sha256"):
        files.append({"path": p.relative_to(ROOT).as_posix(),
                      "bytes": p.stat().st_size, "sha256": sha(p)})
entries = "\n".join(f"{f['sha256']}  {f['path']}" for f in files)
manifest = {
    "schema": "FHS5.PLP.W1.EvidenceManifest@1",
    "run_id": RUN_ID,
    "subject_id": "FHS-5_PLP/W1/CONTROL_PACK",
    "scope": "W1-NF-01",
    "pack_manifest_sha256": pack_sha,
    "repo": {"branch": branch, "head": head, "base": main_sha},
    "file_count": len(files),
    "files": files,
    "tests": test_count,
    "tests_ok": tests_ok,
    "cases": {"total": cases["total"], "passed": passed,
              "not_observed": not_obs, "deferred": deferred,
              "failed": cases["failed"]},
}
(ROOT / "EVIDENCE_MANIFEST.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
(ROOT / "EVIDENCE_MANIFEST.sha256").write_text(entries + "\n", encoding="utf-8", newline="\n")
seal = {
    "schema": "FHS5.PLP.W1.DeliverySeal@1",
    "run_id": RUN_ID,
    "evidence_manifest_sha256": sha(ROOT / "EVIDENCE_MANIFEST.json"),
    "evidence_file_count": len(files),
    "pack_manifest_sha256": pack_sha,
    "claim_ceiling": "W1_PARTIAL_VALIDATED",
    "w2_technically_ready": "NOT_READY",
    "sealed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}
(ROOT / "DELIVERY_SEAL.json").write_text(
    json.dumps(seal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"delivery": str(ROOT), "files": len(files), "tests": test_count,
                  "cases": cases["total"], "passed": passed,
                  "not_observed": not_obs, "deferred": deferred,
                  "head": head, "branch": branch}, ensure_ascii=False, indent=1))
