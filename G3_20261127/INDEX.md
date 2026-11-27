# G3 W0–W2 整合交接索引

| 欄 | 值 |
|---|---|
| 控制包 | `FHS-5_PLP_W0-W2_執行控制包_FINAL`；decision `PCNF-W0W2-ADOPT-20261127-01` |
| 基準 | `a2281bf5542d53ed67b678c0d5b91d0793cc81c4` |
| 施工分支 | `codex/w0-w2-g3-native-20261127` |
| 內容 commit | `aad5a6de58ddba8d58b558f375be6e53db7ea7ef` |
| 文件 commit | `9c6bb8987a4128de47d303e322016d1a419ba553` |
| Checker | `evidence/CHECKER.json`：PASS／46 checks（SEPARATE_PROCESS_SAME_PRINCIPAL） |
| Consumer | `evidence/W3_CONSUMER.json`：ACCEPT |
| Checkpoint | `CHECKPOINT_AB.md`：A/B `COMPLETE_SCOPED` |
| W3 | technical `READY`；execution `NOT_ADMITTED` |

## 五 pin

| pin | 值 |
|---|---|
| source W0 | `baa516b5675589c1a329cd5f65970d8d6c12b7892dd7c079115e1251c9e6e96d` |
| source W1 | `f00b4ee93611e738e409d40758aa320b0bfec3ef0a01fea04dbf5bcb9f1566dc` |
| source W2 | `7bdc4a0acb497944450d89a2c347d26ca4ac8593f6ee47ac229215a80ff227e0` |
| candidate aggregate | `4874c347226afd33b204f5b0fae05f44fbeae6ac8e46d086d3420baf3a4d6988`（60 成員） |
| oracle W0／W1／W2 | `da6fa6f3615f4043…`／`9e5c6a83b719c400…`／`a78e689d42265851…` |
| case set | W0 44／W1 13／W2 12 |
| evidence manifest | `e5299bbb553eabdc9b6d2b1192436fda97a514f39124159a7c07204119150966` |
| seal | `f6dc5bb9aac2b6265b97fb12ddf9c7f2f3b3e5e91edb0434b707629704633703` |

## 已驗／未驗 ledger

| Wave | 已驗 | 未驗 |
|---|---|---|
| W0 | **44/44**、consumer 803/0、SAMPLE/R4/R10/OFF | HERMES/GPT、FHS 485 |
| W1 | 12/13、67 ECP 61 PASS、第二包、115 tests | HERMES-01、ChatGPT/GPT WORK、1 結構性 PARTIAL |
| W2 | **12/12**、UNKNOWN 四類、N09 九階段、Checker、Consumer | 其他 Host、Release、原域 ECP、W3 effect |

## 原 raw 定位

- W0：`runs/w0_full/delivery/`、`runs/w0/raw/`
- W1：`runs/w1/raw/`（ECP67_MEASURED、SECOND_PACK）
- W2：`runs/w2/raw/`（UNKNOWN_FOUR、N09_CHAIN）
- 封存：`evidence/EVIDENCE_MANIFEST.json`（420 檔）＋`SEAL.json`

## 下一步

1. W1：Hermes 三 child／第二 principal。
2. W3：以 `W3_CONSUMER.json` 作 P01 輸入；取得 exact grant 後才施工。
