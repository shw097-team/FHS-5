# FHS-5_PLP W2 Native-first｜主用 ＋ 可執行施工｜宣達

**宣達 ID**：`W2-NF-PRIMARY-DECL-20261126-01`
**對應決策**：`W2-NF-PRIMARY-20261126-01`（`W2_OWNER_DECISION.json`，raw SHA-256 `1ef19c0f0b4212c087a43bf3b8e415f844004448cc0848bafb7da0aeba191ff7`）
**決策人**：Human Owner（W2 範圍內唯一 owner & issuer of record）
**日期**：2026-11-26（Asia/Taipei）　**決策原文**：「把修補後的新版W2，授權/升格/宣達 為『主用 + 可執行施工』。」

## 0｜Claim ceiling（第一屏）

| 維度 | 本宣達成立 | 仍然不成立 |
|---|---|---|
| 文件層主用 | ✅ `PRIMARY_AUTHORIZED` | 產品 PASS |
| 受界施工授權 | ✅ `AUTHORIZED_SCOPED`（逐 op 核前件） | blanket permit |
| Bootstrap | ✅ `ENABLED_AFTER_ROOTS_NAMED` | 已可無條件寫入 |
| `W2_EXECUTION_READY` | ❌ | 需首個合法 op 准入實際驗過 |
| 產品效果 / 獨立驗收 / Release | ❌ | `NATIVE_PASS`／`INDEPENDENT_PASS`／`RELEASED` |
| 原域 Issuer 收據 | ❌（`owner_ref` 仍 null） | `ORIGINAL_DOMAIN_ACCEPTANCE` |

**一句話**：主用與施工**授權**已成立；**產品實效尚未發生**，第一筆寫入仍取決於 Owner 指名 roots 與該 op 的全部技術前件。

## 1｜裁決要旨

1. 修補後版本 `FHS5-PLP/W2/PACK-NF-20261126-r3`（candidate `W2-NF-r3-CODEX-PRIMARY`）升格為 **W2 當期主用依據**。
2. 授權 **W2 範圍內的必要可逆 DEV/OPS 施工**，範圍以本宣達 §3 為限。
3. **不**改動任何已封存的 pack bytes：決策以 `05` 的 raw SHA 引用本體，而非重切本體。事後改 bytes 即等於改掉 Owner 核准過的對象。
4. 授權**不**上溯：W1 sealed delivery、W0 交付、原域 Issuer 收據皆不受影響，也不被本宣達取代。

## 2｜對象與固定身份

| 項 | 值 |
|---|---|
| `artifact_id` | `FHS5-PLP/W2/PACK-NF-20261126-r3` |
| `candidate` | `W2-NF-r3-CODEX-PRIMARY` |
| `05` raw SHA-256 | `81daac8ff3f47566d18cc7ebdaee9625ff5ca000b71caac3226841b124f6099b`（65,377 bytes） |
| `source_set_sha256` | `921de70ca5f273d9bba0ed0d022bb7595e8824d7595e8373b2c43d5ccbbaa044` |
| 上游 WM2 | `FHS5-PLP/W2M/2026-11-25-cnf-r2`，raw SHA-256 `2b98be965651721257164c555f7e9f86228e5e6dd15787c0540c1a6a0cd90093`（67,015 bytes） |
| 受影條款 | WM2 §00.6／§01.4／§02.4／§02.4A／§03.B／§04.B／§05.B／§06.B／§07.8／§08.6／§09.B／§10.4／§11.5／§12.6（等價承接；未受影上位義務不變） |
| 固定 pack 位置 | `https://github.com/shw097-team/FHS-5/blob/d2589deae0a1c5df944fcb899e117123cbc7f4e6/19_W2_NF_CODEX_20261126/FHS-5_PLP_W2_NATIVE_FIRST/05_W2_SOURCE_MANIFEST.json` |
| 證據附錄 | `FHS-5_PLP_W2_Native-first_HERMES_修補證據型附錄.md`（外置封存；digest 見 publication receipt） |

## 3｜生效範圍

| 欄 | 值 |
|---|---|
| `subject_id` | `FHS-5_PLP/W2/CONTROL_PACK` |
| `scope` | `W2-NF-01` |
| 已授權 effect | `SOURCE_READ`、`ISOLATED_DRAFT`、**`DEV`（可逆，逐 op）**、**`OPS`（可逆，逐 op）** |
| 未授權 effect | `USER`（consent/data scope）、`RELEASE`、外部部署、以 push 當 Release、任何不可逆效果 |
| `allowed_roots` | **`PENDING_OWNER_SPECIFICATION`** — 未指名 repo/host/output root 前，只可 READ/DRAFT 與 P01/P02 探查，不得寫入任何 root |
| 期限／撤權 | 至 Owner 撤權，或 subject/scope/artifact/Repo/Host/effect 變更，或出現安全 Finding 為止 |

## 4｜施工前件（每一 op 都必須成立，缺一即停該 op）

1. Owner 決策覆蓋該 op（本宣達＋該 op 的 scope/target）。
2. repo `root/HEAD/branch/dirty/untracked` 與 ACL 真值（同次 probe；非 caller 自報）。
3. exact preimage 或 absent 實測（不得以空字串或舊 bytes 冒）。
4. `01 §5.1` 的 exact write set；不得全 repo glob、不得加入未列 delete target。
5. reverse patch／host-specific recovery 可用，且 dry check 通過。
6. OPS 另需：host/principal、`epoch_state`（真值或合法 `NOT_DECLARED_BY_HOST`）、`R2` receiver、output root、補償能力。
7. 接縫：J1 先驗證後消費（拒收短路、零 product call、零 input write）；`J2-pre`／`J2-post` 分離；J3 真 OFF＋正控；Checker 與 Consumer 為**兩個 distinct receipt**。
8. O03 只產出、**不自我補償**；O04 讀 post 判定；O05 才補償並讀回 pre-state。

## 5｜已驗／未驗（不得互代）

**已驗（文件層，可重算）**

- 33/33 文件層斷言（r1 28/28、r2 28/28），14/14 負向 mutation ×3 代，來源樹前後 digest 不變。
- 24 來源：21 byte-identical、3 git-path pin；`source_set` 三版不變。
- 一個 **distinct session** 對抗式覆核，verdict `REWORK_REQUIRED`；25 項全部處置（23 於 r3、2 於 r2）。
- 分支上推後 fresh clone 逐檔 sha256 回讀：**33/33 byte-identical**，無 EOL 正規化；`main` 未動。
- 16 前件列、12 原案、6 WP、6+6 ACC、7 Seam、18 J 子組、12 N、15→6 投影、14 HOLD＋6 專項、37 CR、7 RQ 逐義在位。

**未驗（具名）**

1. W1 `w2_receiver.py` 等在 `9fae925` 的實體 bytes 未重開（`RECORDED_PIN_NOT_REOPENED`）；施工前必須重算。
2. Bridge `source_refs[]` 42/17/25 不可本機重算；已定義 `BRIDGE_RESPONSE_ABSENT`。
3. Windows reparse/link 全覆蓋未證。
4. 未重跑 W0 44 receipts／W1 79 tests（只引用 recorded）。
5. 12 原案全部 `NOT_RUN`；產品效果 0 次。
6. **無**不同 principal 的獨立 Checker verdict。

## 6｜下一手入口

1. **Owner**：指名 `repo root`、`host`、`output root`（三者任一未指名即只能 READ/DRAFT）。
2. **CODEX**：由 `04_W2_START_THIN_PROMPT.md` 啟動 → P01/P02 可信 read/bind → P03/P04 契約與凍結 → 首個受權 op 准入 → P05/P06。
3. 首個 op 准入實際通過後，才可另宣 `W2_EXECUTION_READY`；本宣達不預支。

## 7｜Stop／Resume

**Stop**：錯 pack/candidate/oracle/scope、假 grant、未知 effect、無 preimage／recovery、principal mismatch、roots 未指名、J1 驗證失敗。
**Resume**：同 subject/scope/pack pin 的 typed receipt；重核 ACL/principal/preimage；只解受影。

## 8｜這不是什麼

不是產品驗收、不是 Checker verdict、不是 Grant 的替代品、不是 Release、不是 merge 到 `main`、不是原域採納、不是第二套規範。
