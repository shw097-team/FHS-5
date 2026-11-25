# W2 INBOUND DRAFT — PI/PD（非正式主用）

**status**：`DRAFT`｜**artifact**：`FHS5-PLP/W2/INBOUND_DRAFT/2026-11-25-r1`
**project_id**：`FHS-5_PLP`｜**subject_id**：`FHS-5_PLP/W2/INBOUND_DRAFT`
**scope**：`W2-READ-01`｜**wave_id**：`W2`｜**batch_id**：`W2-IN-DRAFT-01`
**source**：W2M §03.1（sha256 `2b98be965651721257164c555f7e9f86228e5e6dd15787c0540c1a6a0cd90093`）

Job to be done：將 W0-B 13 個 UNBOUND 前件整理成 W2 DRAFT BindingRequest 清單（READ／DRAFT，不發 Grant、不執行 protected effect）。

**Non-goals**：不發 Grant；不執行 W2 protected DEV／OPS；不建立正式 W2 主用包；不改 W0 歷史。

## ACC（DRAFT）

- 13/13 每列具備 required fields、Owner、Resume 最小證據、W0 證據狀態。
- 全部列 `UNBOUND`，不得自行改為 true。
- 任何 output 僅為 DRAFT，`permission_state=NONE_GRANTED`。
