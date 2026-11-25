# FHS-5｜B0-NF CODEX-first Delivery

**decision**：`W0-CODEX-FIRST-20261125-01`｜`W0-OPS-NATIVE-20261125-01`｜`B0-SAMPLE-CODEX-20261125-01`  
**pack**：`W0-NF-r3-CODEX-PRIMARY`｜**B0**：`B0_REPRESENTATIVE_PASS_WITH_NOT_COVERED`｜**W0**：`W0_PARTIAL_VALIDATED`

## 入口

1. `00_CONTROL_PACK/FHS-5_PLP_W0_NATIVE_FIRST/00_W0_PI_PD.md`
2. `00_CONTROL_PACK/FHS-5_PLP_W0_Native-first_CODEX_修補證據型附錄.md`
3. `01_B0_NF/evidence/five_party_summary.json`
4. `02_W0_CLOSEOUT/W0_CLOSEOUT.md`
5. `02_W0_CLOSEOUT/W0_HANDOFF.md`

## 目錄

| Path | Content |
|---|---|
| `00_CONTROL_PACK/` | r3 六檔、r3 證據附錄、外部 seal、W0M CODEX-first amendment |
| `01_B0_NF/repo/` | 實際 briefcheck repo（requirements/tests/fixtures/code） |
| `01_B0_NF/repo.bundle` | Git history bundle（red→patch→green） |
| `01_B0_NF/tools/` | guide/challenge/far/consumer/ops；W1 Bridge reference 重用副本 |
| `01_B0_NF/evidence/` | 五方、DEV/OPS、challenge、FAR、consumer、bridge、review |
| `02_W0_CLOSEOUT/` | W0 CLOSEOUT/HANDOFF/UPSTREAM_CHANGESET |
| `INTEGRATION_LEDGER.json` | 舊 W0/W1 workspace 抽取／重用／參照對位 |

## 實際結果

- Reviewer：真實 `plp-tpm-review 1.0.1`，0 defects、5 unbound。
- Guide：`PACKAGE_FIRST`，9-key delta。
- Bridge：重用既有 `w1_bridge_reference.py`，selftest 22/22，四 API。
- Challenge：獨立 worktree，19/19 checks，0 findings。
- FAR：2 alternatives、10 advice。
- DEV：red v1 2 failures → patch → green 10 tests。
- OPS：POS/NEG、output/readback/restore、Provider OFF imports `NONE`。
- Consumer：`consumed=true`。

## 邊界

- 不是 HERMES／GPT CHAT／GPT WORK 的實際 Host 驗收。
- 不是完整 W1–W4、完整 QA26/U26/CG-SEM17/38＋28/C16/ECR/FARP30。
- 不是 Release；未取得外部 OS/Repo/Host grant。
- B0 的 maker/checker 是角色分離（獨立 worktree/process），同 OS principal；未偽造不同 principal。
