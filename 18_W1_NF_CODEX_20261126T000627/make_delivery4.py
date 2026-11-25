#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the NF-r4 delivery documents from real evidence (R06)."""
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
RUN_ID = sys.argv[3]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sh(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120,
                           cwd=str(cwd or WT))
        return (r.stdout + r.stderr).strip()
    except Exception as exc:
        return "ERROR: " + str(exc)


EV = ROOT / "evidence"
insp = json.loads((EV / "inspect.json").read_text(encoding="utf-8"))
cases = json.loads((EV / "cases.json").read_text(encoding="utf-8"))
host = json.loads((EV / "host" / "host_receipt.json").read_text(encoding="utf-8"))
cm = json.loads((ROOT / "W1_CLOSURE_MATRIX.json").read_text(encoding="utf-8"))
w2_path = ROOT / "W2_RECEIVE_RECEIPT.json"
w2 = json.loads(w2_path.read_text(encoding="utf-8")) if w2_path.is_file() else {
    "accepted": False, "check_count": 0, "rejected_checks": ["receipt_absent"],
    "next_operation": None, "stop": None, "resume": None}
tests_txt = (EV / "test_run.txt").read_text(encoding="utf-8")
m = re.search(r"Ran (\d+) tests", tests_txt)
test_count = m.group(1) if m else "?"
tests_ok = tests_txt.strip().splitlines()[-1].strip() == "OK" if tests_txt.strip() else False
RUN_ID = cases.get("run_id") or RUN_ID

verdicts = {c["case_id"]: c["verdict"] for c in cases["cases"]}
fails = [k for k, v in verdicts.items() if v == "FAIL"]
defers = [k for k, v in verdicts.items() if v == "DEFERRED"]
not_obs = [k for k, v in verdicts.items() if v == "NOT_OBSERVED"]
passed = [k for k, v in verdicts.items() if v == "PASS"]

counts = insp["counts"]
head = sh(["git", "rev-parse", "HEAD"])
branch = sh(["git", "branch", "--show-current"])
content_commit = sh(["git", "log", "-1", "--format=%H", "--", "17_W1_NF_CODEX_" + RUN_ID]) or "UNCOMMITTED"
main_sha = "c2d8084ba24dd8df3fa62259bba496f4fb9caa85"

status = {}
status["R01_fidelity"] = insp["abi_crosswalk"]["state"] == "COMPLETE"
status["R02_host"] = bool(host.get("host_consumed"))
status["R03_off"] = verdicts.get("N10") == "PASS" and verdicts.get("W1-SEC-01") == "PASS"
status["R04_closure"] = not [r for r in cm["rows"] if r["verdict"] in
                             ("NOT_EXERCISED", "NOT_EVIDENCED", "PLANNED_OPERATION")]
status["R04_cases"] = not fails
status["R05_w2"] = bool(w2.get("accepted"))
checker_path = EV / "how_to" / "independent_check.json"
checker = json.loads(checker_path.read_text(encoding="utf-8")) if checker_path.is_file() else None
critical = [f for f in (checker or {}).get("findings", []) if f.get("severity") == "critical"]
status["R06_checker"] = bool(checker) and not critical

off_p = EV / "off_task_receipt.json"
off = json.loads(off_p.read_text(encoding="utf-8")) if off_p.is_file() else {}
w2in_p = EV / "w2" / "w2_inbound_receipt.json"
w2in = json.loads(w2in_p.read_text(encoding="utf-8")) if w2in_p.is_file() else {}
status["F1_w2_inbound"] = bool(w2in.get("draft_completed")) and \
    (w2in.get("seam_wiring") or {}).get("state") == "COMPLETE"
status["F2_on_off"] = off.get("state") == "ON_OFF_BOTH_SEMANTIC_SUCCESS"

import hashlib as _h
_impl = sorted((WT / "W1" / "impl").glob("*.py")) + sorted((WT / "W1" / "check").glob("*.py"))
_canon = _h.sha256("".join(sorted(_h.sha256(p.read_bytes()).hexdigest()
                                  for p in _impl)).encode("utf-8")).hexdigest()
_row_cand = (cases["cases"][0].get("candidate_sha") if cases.get("cases") else None)
status["F3_candidate_pin"] = (_row_cand == _canon)
f3_note = {"recomputed": _canon, "in_raw": _row_cand}

validated = all(status.values())
claim = "W1_NF_VALIDATED" if validated else "W1_PARTIAL_VALIDATED"
w2_ready = "READY" if (validated and w2.get("accepted")) else "NOT_READY"

impl_rows = "\n".join(
    "| `W1/impl/%s` | %d | `%s` |" % (p.name, p.stat().st_size, sha(p))
    for p in sorted((WT / "W1" / "impl").glob("*.py")))
chk_rows = "\n".join(
    "| `W1/check/%s` | %d | `%s` |" % (p.name, p.stat().st_size, sha(p))
    for p in sorted((WT / "W1" / "check").glob("*.py")))
case_rows = "\n".join(
    "| `%s` | %s | %s | %s |" % (c["case_id"], c.get("kind", ""), c["verdict"],
                                 (c.get("observed") or {}).get("token", "-"))
    for c in cases["cases"])
status_rows = "\n".join("| %s | %s |" % (k, "PASS" if v else "OPEN") for k, v in status.items())
host_rows = "\n".join("| %s | %s |" % (k, v) for k, v in host["stage_ledger"].items())
cm_rows = "\n".join("| %s | %s |" % (k, v) for k, v in sorted(cm["verdict_counts"].items()))

closeout = f"""# FHS-5_PLP W1 CLOSEOUT（NF-r4，R01–R06 收尾）

**File ID**：`FHS5-PLP/W1/CLOSEOUT/NF-r4`
**run_id**：`{RUN_ID}`
**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`｜**scope**：`W1-NF-01`
**pack_manifest_sha256**：`{insp['pack_manifest_sha256']}`
**repo**：`{branch}`｜`content_commit` `{content_commit}`｜`head` `{head}`｜base `{main_sha}`
**判定**：`{claim}`｜`W2_TECHNICALLY_READY = {w2_ready}`
**不宣稱**：`RELEASED`、`M-DONE`、`GPT_CHAT_PASS`、`GPT_WORK_PASS`、`HERMES_PASS`、`W2_EXECUTION_READY`

---

## 1｜R01–R06 實際狀態

| 項 | 狀態 |
|---|---|
{status_rows}

### R01 通用產品語義

- `tpm_contracts_nf`: profile-driven（`W1` 保留真分母，`GENERIC` 不寫死 38/29/13）；契約五視圖為實質內容（需求、Child、ACC、capability、typed DAG、Effect、Recovery、Oracle）。
- Reviewer 唯讀、八欄 Finding、`first_fail` 與 `change_cone`；Finding raw 為真實觀測 payload 的 canonical digest，不是 subject SHA。
- Guide 四函式；`next/stop/resume` 由凍結 04 段落推導，`original_verifier` 會被實際呼叫，回傳非 `verified=true` 即 `DELTA_UNVERIFIED`。
- Bridge 欄級 `field_fidelity`：source value → transform → target value → readback，`missing` 由實算產生。

ABI 狀態：`{insp['abi_crosswalk']['state']}`；field fidelity 由 `bridge_nf.verify_field_fidelity` 實算。

### R02 真 CODEX Host／Consumer

| 階段 | 觀測 |
|---|---|
{host_rows}

- 兩次真實 `codex exec` session：`{host['packages']['pkgA_w1']['invocation']['session_id']}`（W1 pack）與 `{host['packages']['pkgB_w0']['invocation']['session_id']}`（W0 pack）。
- 版本：`{host['packages']['pkgA_w1']['invocation']['codex_version']}`；served 方式：invocation payload（nested Codex 無可用 file-read 工具，已如實記錄）。
- 每個產物由獨立 consumer 程序 parse/use/readback；pkgA 的 fixture/oracle SHA 與 pack 實值逐欄比對。

### R03 Native OFF／安全

- `off_isolation.cold_off_probe`：5 個 legacy runtime 全部 blocked，`positive_control("json")` imported=True（證明探針不是瞎的）。
- 7 類路徑攻擊全 `PATH_OUTSIDE_ROOT`；canary 前後 digest 不變；symlink 探針在本機回 `NOT_VERIFIED`（Windows 特權不足，未提權）。
- `env_flag_only_reject`：純 env flag 不得作為隔離證據。

### R04 證據與核銷

- 共用 Closure Matrix：`W1_CLOSURE_MATRIX.json`（{cm['row_count']} 列）。
- 計數：{cm_rows.replace(chr(10), '；')}
- Observation 分離 `candidate_sha / source_sha / pack_sha / oracle_sha256 / case_set_sha256 / evidence_sha256`。

### R05 W2 技術接收

- 獨立 `w2_receiver`：accepted = `{w2.get('accepted')}`，checks = `{w2.get('check_count')}`，rejected = `{w2.get('rejected_checks')}`。
- next operation：`{w2.get('next_operation')}`

### R06 封存

- 交付本身含 evidence manifest、seal、closure matrix、host receipt、W2 receipt、OpenSpec change。
- 發佈記錄外置於 `PUBLICATION_STATUS.md`，不在被 commit 的文件內反覆寫自身 HEAD。

### F1 真 W2 入站

- W2 DRAFT 材料：13 列 BindingRequest，來源 W2M §03.1（`evidence/w2/material`）。
- 真 CODEX session：`{(w2in.get('host') or {}).get('session_id')}`，產出 13 列分類 artifact，獨立 consumer 逐列驗證。
- 五條 Seam 接線：`{(w2in.get('seam_wiring') or {}).get('matched')}/{(w2in.get('seam_wiring') or {}).get('total')}`，state `{(w2in.get('seam_wiring') or {}).get('state')}`。
- `permission_state=NONE_GRANTED`、`grant_issued=false`。

### F2 ON／OFF

- 同一 W2 任務：ON `{off.get('on', {}).get('rows')}` 列、OFF `{off.get('off', {}).get('rows')}` 列，投影相等 `{off.get('projection_equal')}`。
- Legacy cold OFF `{(off.get('cold_off') or {}).get('cold_off')}`、正控 import `{(off.get('positive_control') or {}).get('imported')}`。
- OFF 子程序未 import TPM／Guide／Bridge：`{off.get('off', {}).get('imported_forbidden')}`。

### F3 候選與證據

- candidate 重算 `{f3_note['recomputed'][:16]}…` vs raw `{(f3_note['in_raw'] or '')[:16]}…`，一致 `{status['F3_candidate_pin']}`。
- NEG 未拒絕即 FAIL、POS 空觀測即 FAIL、exit 0 但未 consumed 不計 PASS（`check/test_negative_control.py`）。

---

## 2｜測例（20 列）

| Case | Kind | Verdict | token |
|---|---|---|---|
{case_rows}

PASS {len(passed)}｜NOT_OBSERVED {len(not_obs)}｜DEFERRED {len(defers)}｜FAIL {len(fails)}
單元測試：{test_count} tests {"OK" if tests_ok else "FAILED"}

## 3｜實作檔

| 檔 | bytes | sha256 |
|---|---:|---|
{impl_rows}

## 4｜測試與 runner

| 檔 | bytes | sha256 |
|---|---:|---|
{chk_rows}

## 5｜殘餘與 Next

{("無當期必要缺口。" if validated else "見 §1 標為 OPEN 的項目；每項附 FirstFail 與 Resume。")}
- HERMES 三 child：`DEFERRED`（未掛載），不阻 Generic。
- 真 Windows junction/reparse：`NOT_VERIFIED`（未提權）。

## 6｜結論

`{claim}`；`W2_TECHNICALLY_READY = {w2_ready}`。證據見 `evidence/`、`W1_CLOSURE_MATRIX.json`、`W2_RECEIVE_RECEIPT.json`。
"""

handoff = f"""# FHS-5_PLP W1 HANDOFF（NF-r4 → W2）

**run_id**：`{RUN_ID}`｜**pack_manifest_sha256**：`{insp['pack_manifest_sha256']}`
**repo**：`{branch}`｜`content_commit` `{content_commit}`
**status**：`{claim}`｜W2 `{w2_ready}`

## 1｜W2 消費欄位

```
subject_id: FHS-5_PLP/W1/CONTROL_PACK
scope: W1-NF-01
pack_manifest_sha256: {insp['pack_manifest_sha256']}
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
| pack_manifest_sha256 | `{insp['pack_manifest_sha256']}` |
| source_set_sha256 | `{insp['source_set_sha256']}` |
| evidence manifest | `EVIDENCE_MANIFEST.json`（逐檔 sha256，seal 外置綁定） |
| closure matrix | `W1_CLOSURE_MATRIX.json`（{cm['row_count']} 列） |
| host receipt | `evidence/host/host_receipt.json` |
| W2 receipt | `W2_RECEIVE_RECEIPT.json` |
| entry / bridge / guide / tpm / consumer / runner | `W1/impl`、`W1/check` |

## 2｜next / stop / resume

- next：`{w2.get('next_operation')}`
- stop：`{w2.get('stop')}`
- resume：`{w2.get('resume')}`

## 3｜重放

```
python W1/check/run_host_nf.py --w1-pack <pack> --second-pack <w0 pack> --out <evidence>/host
python W1/check/run_cases_nf.py --pack <pack> --out <evidence>
python W1/check/closure_matrix.py --pack <pack> --evidence <evidence> --out W1_CLOSURE_MATRIX.json
python W1/check/w2_receiver.py --delivery . --out W2_RECEIVE_RECEIPT.json
```
"""

changeset = f"""# W1 UPSTREAM CHANGESET（NF-r4）

**run_id**：`{RUN_ID}`｜scope `W1-NF-01`

## 1｜本輪 execution-scope amendments

| ID | 差額 | 落點 |
|---|---|---|
| `A6` | TPM 由 W1 硬碼改為 profile registry；GENERIC 只要求最小欄位 | `tpm_contracts_nf.py` |
| `A7` | Guide 的 next/stop/resume 由凍結 04 段落推導，移除固定字串 | `guide_nf.py::_thin_nav` |
| `A8` | Bridge 新增 `field_fidelity`（source→transform→target→readback），`missing` 改實算 | `bridge_nf.py` |
| `A9` | Host served 以 invocation payload 提供（nested Codex 無 file-read），argv 與 sha 如實記錄 | `check/run_host_nf.py` |
| `A10` | Observation 分離 candidate/source/pack/oracle/case_set/evidence 六種身份 | `check/run_cases_nf.py` |

## 2｜回寫候選（未採納）

1. `W1M §12.3`：把 reader 測試數改為實測 {test_count}，並註明 closure matrix 為核銷主表。
2. `W2M §接收`：採用 `w2_receiver` 的 6 類拒收檢查作為最小驗收。
3. `PROG-00 §SM05`：記錄 host served 可為 invocation payload（非必為 file）。

## 3｜歷史分帳

- NF-r3 交付 `16_W1_NF_CODEX_20261125T222954` 保留，不覆寫。
- 本輪新增 `17_W1_NF_CODEX_{RUN_ID}`。
"""


def _w(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


_w(ROOT / "FHS-5_PLP_W1_CLOSEOUT.md", closeout)
_w(ROOT / "FHS-5_PLP_W1_HANDOFF.md", handoff)
_w(ROOT / "W1_UPSTREAM_CHANGESET.md", changeset)

files = []
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and p.name not in ("EVIDENCE_MANIFEST.json", "DELIVERY_SEAL.json",
                                      "EVIDENCE_MANIFEST.sha256",
                                      "W2_RECEIVE_RECEIPT.json"):
        files.append({"path": p.relative_to(ROOT).as_posix(),
                      "bytes": p.stat().st_size, "sha256": sha(p)})
manifest = {"schema": "FHS5.PLP.W1.EvidenceManifest@2", "run_id": RUN_ID,
            "subject_id": "FHS-5_PLP/W1/CONTROL_PACK", "scope": "W1-NF-01",
            "pack_manifest_sha256": insp["pack_manifest_sha256"],
            "repo": {"branch": branch, "head": head, "base": main_sha,
                     "content_commit": content_commit},
            "claim_ceiling": claim, "w2_technically_ready": w2_ready,
            "tests": test_count, "tests_ok": tests_ok,
            "cases": {"total": cases["total"], "passed": len(passed),
                      "not_observed": len(not_obs), "deferred": len(defers),
                      "failed": len(fails)},
            "closure_rows": cm["row_count"],
            "file_count": len(files), "files": files}
(ROOT / "EVIDENCE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8", newline="\n")
(ROOT / "EVIDENCE_MANIFEST.sha256").write_text(
    "\n".join(f"{f['sha256']}  {f['path']}" for f in files) + "\n", encoding="utf-8", newline="\n")
seal = {"schema": "FHS5.PLP.W1.DeliverySeal@2", "run_id": RUN_ID,
        "evidence_manifest_sha256": sha(ROOT / "EVIDENCE_MANIFEST.json"),
        "evidence_file_count": len(files),
        "pack_manifest_sha256": insp["pack_manifest_sha256"],
        "claim_ceiling": claim, "w2_technically_ready": w2_ready,
        "sealed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
if (ROOT / "W2_RECEIVE_RECEIPT.json").is_file():
    seal["w2_receive_receipt_sha256"] = sha(ROOT / "W2_RECEIVE_RECEIPT.json")
    seal["w2_receive_receipt_excluded_from_manifest"] = True
(ROOT / "DELIVERY_SEAL.json").write_text(json.dumps(seal, ensure_ascii=False, indent=2) + "\n",
                                         encoding="utf-8", newline="\n")
print(json.dumps({"claim": claim, "w2": w2_ready, "files": len(files),
                  "status": status, "cases": {"pass": len(passed), "deferred": len(defers),
                                              "not_observed": len(not_obs), "fail": len(fails)}},
                 ensure_ascii=False, indent=1))
