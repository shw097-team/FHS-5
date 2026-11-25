# FHS-5_PLP W0-NF CODEX-first 交付索引

**verdict**：`B0_NF_VALIDATED`／`W0_NF_VALIDATED`；`W1_TECHNICALLY_READY`；
`W1_EXECUTION_READY=NOT_CLAIMED`；`RELEASED=NOT_CLAIMED`。

## 入口

1. `FHS-5_PLP_W0_CLOSEOUT.md`：完整 CLOSEOUT（A/B/C、14 WP、44 案、五方、DEV/OPS、pins、NotCovered）。
2. `FHS-5_PLP_W0_HANDOFF.md`：W1 handoff（pins、consumer readback、readiness 兩層）。
3. `W0_UPSTREAM_CHANGESET.md`：Finding、決策、影響、last good、resume。
4. `EVIDENCE_MANIFEST.json`：證據檔 SHA/bytes 索引、pins、claims 與 workspace-only 說明。
5. `REPLAY.md`：從 raw 重播的實際命令。
6. `UPSTREAM_WRITEBACK/`：MASTER／PROG-00／PROJ-01..05／WM 的受影段替換稿（待採納）。
7. `PUBLICATION_STATUS.md`：local commit 與 push 被安全審查拒絕的實際狀態。

## 原始證據位置

`C:\Projects\Agent_Workspace\FHS-5_Workspace\13_W0_NF_CODEX_20261125\`

| 目錄 | 內容 |
|---|---|
| `01_PACK` | 封存六檔、W0M r4、external seal、歷史附錄（標 superseded） |
| `02_CANDIDATE/repo` | briefcheck Git repo；v2 `5eab43d` → v3 `bb66a27` |
| `03_PARTIES` | TPM 四契約／Reviewer、Guide、Bridge、Challenge、FAR |
| `04_DEV_OPS` | red／patch／retest、OPS O1–O5、OFF trace |
| `05_TQAEP` | oracle、44 receipts、raw、summary |
| `06_CHECKER` | Challenge 的隔離副本與 raw |
| `07_CONSUMER` | W1 consumer receipt 與 raw |
| `08_OPENSPEC` | OpenSpec 2.0 change（另有 `openspec/` 根） |
| `09_DELIVERY` | CLOSEOUT/HANDOFF/CHANGESET 與上游替換稿 |
| `10_EVIDENCE` | 證據 manifest |

## 邊界

- 不是 W1–W4 完整分母、不是 FHS 485、不是 HERMES／GPT Host、不是 Release。
- Checker 與 Maker 為同 OS principal 的 process／隔離副本分離；不同 principal 未宣。
- symlink 建立受 OS 權限限制，記 `NOT_VERIFIED`；junction 已實測。
