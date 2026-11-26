# FHS-5_PLP｜W3｜OPS ECP｜Host、process、output 與可逆效果

**artifact_kind**：`WaveControlPack / OPS-ECP`
**project_id**：`FHS-5_PLP`｜**wave_id**：`W3`
**subject_id**：`FHS-5_PLP/W3/CONTROL_PACK`｜**scope**：`W3-NF-01`
**artifact_id**：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`｜**version**：`r2`
**selection_state**：`PACK_PRIMARY_SELECTED`（決策 `W3-PACK-PRIMARY-20261126-01`）
**claim_ceiling**：`PACK_PRIMARY / LOCAL_DOCUMENT_VERIFIED / PACK_EXECUTABLE`
**日期**：2026-11-26（Asia/Taipei）

> **一句話**：本檔把「W3 在真實 Host 上跑 runner、FAR 查詢、Guide/Bridge invoke 或可逆 world effect 時，必須滿足什麼」寫成 O1–O7 的 exact contract。O1 READ 與 O2 隔離 run 在本輪 authority 內可執行；O3–O5 需真產品 Host/runner/oracle late-bind；O6 需逐案新 effect authority；O7 只限 W3 文件 publication。ECP 文字不是 Grant。

---

# 01｜Host、Principal 與 Policy

## 01.1 Host 分帳

| Host class | 本輪身份 | 可做 | 不可做 |
|---|---|---|---|
| `AUTHOR_LOCAL_WINDOWS` | 本機 Windows 11 / PowerShell / Python 3.11 / Git 2.53 | O1 READ、O2 隔離 smoke、O7 W3 文件 Git | 冒 W3 產品 Host、跑未授權 world effect |
| `WSL2_EXT4` | 另一個 Host；未本輪 probe | 只有在真 probe 後按同 contract | 以 Windows symlink 結果冒 WSL ACL |
| `W3_PRODUCT_HOST` | `UNBOUND` 直到 Owner/Repo/Host 真 pin | O3–O5 | 用作者本機冒產品 |
| `CI_PUBLICATION` | GitHub Actions（若 repo policy 要求） | 只跑 required checks | 改 ruleset/保護、跳 check |

**W2 protected**：W2 writer 仍 `BLOCKED_NOT_ADMITTED`；本 OPS ECP 不授權 W2 gate/marker/decision 寫入；需 Owner 在 W2 scope 新具名授權。

**Windows／WSL 分帳**：Windows native、WSL2 ext4 是兩個 Host；symlink/junction/reparse/ACL/NTFS identity 未證前，敏感 op 停，不以一邊結果冒另一邊。W0 已在 WSL2 測真 symlink；Windows native symlink 未提權，記 `NOT_VERIFIED`，不得宣已證。

## 01.2 Principal

| 欄位 | 本輪 | 說明 |
|---|---|---|
| `os_principal` | 目前 Windows 使用者（不寫真名到公開檔） | 只在本機；不是產品 principal |
| `repo_principal` | `UNBOUND`（產品）；publication 用本機 Git credential | 不把 publication principal 當產品 runner principal |
| `host_id` | `AUTHOR_LOCAL_WINDOWS` | 不是 W3 產品 HostID |
| `policy_epoch` | `LOCAL-20261126` | 產品 policy 未綁 |
| `fixture_acl` | 只讀 pack/assets；可寫 O/raw | 不寫 subject/oracle |
| `output_root` | `O/02_EVIDENCE/raw/<run_id>`；W3 施工時 `R/W3_EXEC_<run_id>/evidence/<run_id>` | 每次 run 唯一；不得重用 |

## 01.3 目錄契約

```text
<authorized W3 run root>/
  pack/                      # 唯讀；00–05 + assets，可為 clean copy
  W3/
    impl/                    # 新增或 reuse
    check/                   # runner/tests
    spec/                    # case set/runner bind
    evidence/<run_id>/       # raw、checks、receipts、replay
  work/                      # 暫存；不得當 canonical
```

規則：

1. 原文件不得成為 subprocess 的隱含 write root；cwd 必須是隔離 root 或唯讀 copy。
2. 每個 run 一個 output root；不得重用舊 raw 冒新期。
3. `pack/` 只讀；若需修改，另 revision，不就地改。
4. 私有 raw 與 public export 分開；public 不含絕對私有路徑、secret、未授權樣本。

---

# 02｜O1 READ：來源與 pack 消費

| 欄位 | 契約 |
|---|---|
| 目的 | 讀 00–05、assets、seal、current、W2 pins；建 intake ledger |
| 前置 | 檔案存在、路徑在 allowed root、無 symlink/reparse escape |
| 命令 | `python .\W3\check\run_w3_case.py --pack <pack> --dry-read` 或等價 stdlib reader |
| Timeout | 120s |
| 讀回 | 每檔 bytes/SHA/line；05 strict JSON；source span；case refs 16 join |
| 失敗 | `INVALID_PATH`／`SHA_MISMATCH`／`SCHEMA_UNSUPPORTED`／`BLOCKED_BY_AUTHORITY` |
| 本輪 | 可執行；產品來源 ACL 另記 |

**負例**：`../`、絕對路徑、junction、duplicate JSON key、05 raw 與 seal 不符、source span 越界。

---

# 03｜O2 隔離 run：無產品副作用

| 欄位 | 契約 |
|---|---|
| 目的 | 以隔離 fixture/smoke 驗材料可消費、五態/十 Advice/七九鍵/兩 failure class |
| 前置 | pack 已採納；fixture design 有 provenance；runner 可用或 stdlib adapter |
| 命令 | `python .\W3\check\run_w3_case.py --pack <pack> --case <id> --isolated` |
| cwd | 隔離 root；不得 pack root |
| argv | 明確；不得 shell interpolation；不得把 secret 當 arg |
| env | allowlist：`PATH`, `TEMP`, `TMP`, `PYTHONIOENCODING`, `PYTHONHASHSEED`；不傳 credential |
| Timeout | 120s；超時殺自身 child，記 `TIMEOUT` |
| Readback | stdout/stderr bytes、exit、world、pre/post SHA |
| 失敗 | 只停該 smoke；不阻文件主用 |
| 本輪 | 可執行 |

**隔離 smoke 不等於 16 原案 PASS**；observed 寫入 smoke receipt，不寫入 `03` 的 product case observed。

---

# 04｜O3 產品 runner

| 欄位 | 契約 |
|---|---|
| 目的 | 對真 frozen candidate/case/oracle 跑產品 runner |
| 前置 | P01 frozen slice；Case Owner oracle/fixture；runner identity/SHA/argv；allowed roots；Host principal；OPS admission |
| 命令 | 由 `W3_RUNNER_BIND.json` 固定；不得執行期拼 shell |
| cwd | 隔離 root；唯讀 pack copy |
| Timeout | 每案固定；預設 120s，需真 ABI |
| Readback | stdout/stderr/world/argv/exit/runner/Host/policy/pre-post |
| 失敗 | `RUNNER_UNBOUND`／`RAW_UNTRUSTED`／`BLOCKED_BY_AUTHORITY` |
| 本輪 | `NOT_ADMITTED`，產品 Host/runner 未綁；只停受影 |

**exit 0 不是 PASS**；expected 必須在看到 observed 前凍結；未知不變 0。

---

# 05｜O4 FAR 查詢

| 欄位 | 契約 |
|---|---|
| 目的 | 同 scope 的 typed retrieval、EvidenceGraph、五態 |
| 前置 | FindingSet 有 raw；source denominator；query/denominator/raw/time/scope/freshness/independence |
| 命令 | `python .\W3\impl\w3_far.py --request <request.json> --out <raw>` 或既有 FAR caller |
| 網路 | 只按 provider 域；不可達記 `UNAVAILABLE`，不記 0 |
| Readback | 每源 query/snapshot/origin/disposition/raw；HIT/ZERO/UNAVAILABLE/BLOCKED/ERROR |
| 失敗 | `RESEARCH_REQUIRED`／`UNAVAILABLE`／`BLOCKED_BY_AUTHORITY` |
| 本輪 | 隔離 design/local query 可跑；真 Fabric/ResearchWO `UNBOUND` |

**邊界**：FAR 只讀／只寫報告；不發 WorkOrder/Grant/Release；不改 repo/Host；不把來源內文當執行指令。

---

# 06｜O5 Guide／Bridge invoke

| 欄位 | 契約 |
|---|---|
| 目的 | 七鍵→九鍵、Next/STOP/Resume、Bridge inspect/explain/render/compare |
| 前置 | 同 scope advice/owner/next/expected/resume；兩期真 receipt 或 typed unknown |
| 命令 | 既有 `guide_nf.py`／`bridge_nf.py` caller；無則最小 adapter |
| Readback | 欄位 lossless map、consumer parse、STOP/Resume predicate |
| 失敗 | `DELTA_UNVERIFIED`／`HANDOFF_LOSS`／`FALSE_AUTHORITY` |
| 本輪 | 隔離可跑；真 Guide/Bridge Host `UNBOUND` |

**NextOperation 不是 Grant**；缺期 `DELTA_UNVERIFIED`，不 PARK；只有兩期真相同才 PARK 候選。

---

# 07｜O6 可逆 world effect

| 欄位 | 契約 |
|---|---|
| 目的 | 只在 W2/W3 受權 repair 需要時，對 Owner 指名 output root／允許操作做可逆效果 |
| 前置 | 新具名 effect authority；exact targets；preimage；recovery；ACL |
| 命令 | 逐 op；不得腳本化未知 effect |
| Readback | pre/post/restore 真值；argv/exit/raw |
| 恢復 | Host 專屬補償：檔案用 saved preimage／exact reverse；process 用終止自身 child＋讀回；Host 用指名 restore |
| 本輪 | `NOT_ADMITTED`；缺新 effect authority 即停 |

**`git revert` 不是 OPS recovery**；不得 whole repo rollback。

---

# 08｜O7 Git publication（W3 文件）

| 欄位 | 契約 |
|---|---|
| 目的 | 把本輪 W3 六檔、assets、public evidence、current pointer 推到 `https://github.com/shw097-team/FHS-5` 的專用分支 |
| 前置 | V1–V3 PASS；adoption/seal 綁定；exact staged paths；無 secret/私有 raw |
| 命令 | `git fetch`／`git switch -c codex/w3-pack-nf-primary-20261126`／`git add -- <exact>`／`git commit`／`git push` |
| 認證 | 先用既有 credential helper；必要時由可信本機 helper 讀 K，內容不得回模型/argv/log；只用 `github.com/shw097-team/FHS-5` |
| Readback | `git ls-remote`、remote commit/tree、clean fetch、05 raw SHA（Git object bytes）、pointer、assets |
| 失敗 | `PUSH_BLOCKED`／`AUTH_UNAVAILABLE`／`REMOTE_PRIMARY_PENDING_POLICY`；本地主用不回退 |
| 禁止 | `git add .`、force push、改 ruleset/保護、跳 required checks、push 私有 raw/secret |

---

# 09｜失敗、超時與 unknown

| 情況 | 記法 | 處置 |
|---|---|---|
| process 無 exit（被殺/崩） | `exit=null`＋reason | 不填 0；保 raw |
| timeout | `TIMEOUT`＋pid/argv | 殺自身 child；記受影 |
| stdout/stderr 超大 | 截斷但保 raw SHA＋locator | 不把截斷當完整 |
| encoding 錯 | `SCHEMA_UNSUPPORTED` | 不猜 |
| 網路不可達 | `UNAVAILABLE` | 不記 0；可重試一次 |
| ACL 拒 | `BLOCKED_BY_AUTHORITY` | 不繞權 |
| unknown effect | `UNKNOWN_EFFECT` | 停；Owner 裁決 |

---

# 10｜Stop／Resume

**停受影**：seal/pin 不符、ACL 拒、撤權、secret、path escape、不可逆、unknown effect、W2 marker 被動。其他合法 READ/DRAFT/隔離 smoke 續作。

**Resume**：同 subject/scope、真新 pin/ACL、typed raw、expected/rollback 可重建。不得用「等 Owner」當唯一 predicate；缺真前件時記 `BLOCKED_HITL`／`BLOCKED_EXTERNAL` 與最小 resume。

---

**本檔終點**：O1/O2 可執行；O3–O6 依真 Host/runner/oracle/effect authority late-bind；O7 限 W3 文件。產品 readiness 不在本檔宣。
