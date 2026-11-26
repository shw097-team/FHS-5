# FHS-5_PLP｜W3 r2｜主用交付索引（public export）

**artifact_id**：`FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY`｜**version**：`r2`｜**subject**：`FHS-5_PLP/W3/CONTROL_PACK`｜**scope**：`W3-NF-01`

## 01｜主用狀態

| 狀態 | 值 | 說明 |
|---|---|---|
| `PACK_PRIMARY_SELECTED` | **YES** | 依 `W3-PACK-PRIMARY-20261126-01`、V1–V3 clean PASS、外置 seal/adoption |
| `PACK_EXECUTABLE` | **YES** | `assets/tools/w3_consumer.py --check/--next` 真跑；可選 `P01_READ` |
| `W3_TECHNICALLY_READY` | NOT_CLAIMED | W2 PARTIAL；需 requalification＋clean receive |
| `W3_NF_VALIDATED` / `INDEPENDENT_PASS` | NOT_CLAIMED | 16 原案仍 NOT_RUN |
| `RELEASED` | NOT_CLAIMED | 無 Publisher/外部 Release |

**合法下一步**：`P01_READ`／`R0_REOPEN`／`R1_README`／`ISOLATED_SMOKE`；W2 writer 仍 `BLOCKED_NOT_ADMITTED`。

## 02｜驗收

| Group | Result | Raw |
|---|---|---|
| V1 完整性/pin | PASS | `02_EVIDENCE/W3_檢查修補與驗收_證據型附錄.md` §04 |
| V2 原義/可達性 | PASS | `02_EVIDENCE/W3_檢查修補與驗收_證據型附錄.md` §05 |
| V3 可消費/啟動 | PASS（DOC/SMOKE） | `assets/tools/w3_consumer.py`；`02_EVIDENCE/W3_檢查修補與驗收_證據型附錄.md` §06 |

Clean run byte equality：`True`；V1/V2/V3/consumer 全部 exit 0。

## 03｜檔案與載點

| 檔案 | bytes | SHA-256 | 本地載點 |
|---|---:|---|---|
|  `00_W3_PI_PD.md`  |  77829  |  `8d9ff66626ab63571497d2620ac86e782b1de92b789f0c6b2e09b03cc096ec90`  | `01_BODY/FHS-5_PLP_W3_NATIVE_FIRST/00_W3_PI_PD.md` |
|  `01_W3_DEV_ECP.md`  |  16083  |  `2f943e1e5e6b333c05efc67b0cdfd0882049a07a401d42cf5fa23a779c61b5cd`  | `01_BODY/FHS-5_PLP_W3_NATIVE_FIRST/01_W3_DEV_ECP.md` |
|  `02_W3_OPS_ECP.md`  |  9910  |  `d4c244a7080793777aef7e35e595dab525cc25816effc4ec7146a68bd6c89c23`  | `01_BODY/FHS-5_PLP_W3_NATIVE_FIRST/02_W3_OPS_ECP.md` |
|  `03_W3_TQAEP.md`  |  59884  |  `d0d49c8c4930f1fa1e78e5432d5c327b4b446f34e2876c36e9d91e6b09802df9`  | `01_BODY/FHS-5_PLP_W3_NATIVE_FIRST/03_W3_TQAEP.md` |
|  `04_W3_START_THIN_PROMPT.md`  |  5938  |  `0ce02166f8cea579d31a1a8b9422f31da9244cc270a7a0447d7f1c1b93b46ddc`  | `01_BODY/FHS-5_PLP_W3_NATIVE_FIRST/04_W3_START_THIN_PROMPT.md` |
|  `05_W3_SOURCE_MANIFEST.json`  |  79611  |  `9c34251936067a027d2dfc31cd28540336df27c110311590369e49773ddd96c4`  | `01_BODY/FHS-5_PLP_W3_NATIVE_FIRST/05_W3_SOURCE_MANIFEST.json` |
|  `EXTERNAL_SEAL.json`  |  1104  |  `cb9bc39d9a541db86571c3eda05db61674e69813029caa519054da054a2ca903`  | `EXTERNAL_SEAL.json` |
|  `W3_OWNER_ADOPTION.json`  |  2641  |  `330476e77ec4bb2f1c20b25ca4d79ba751f67f48ac44d6a5cb5e235bde540bee`  | `W3_OWNER_ADOPTION.json` |
|  `W3_CURRENT.json`  |  1237  |  `7536e09e87e6e769a15b3689569838a24a9e2ab623487b88892df4f6e93aeddf`  | `W3_CURRENT.json` |
|  `W3_來源追溯與原義保全_證據型附錄.md`  |  18003  |  `0bcc990461a03806cd789cbe4876a835103b5b8f87d625a22264e5f0f080f0ad`  | `02_EVIDENCE/W3_來源追溯與原義保全_證據型附錄.md` |
|  `W3_檢查修補與驗收_證據型附錄.md`  |  8799  |  `dc2bfe875fa6f9e03fae195c1302dabcd0b5e8a888ec8db8dee5e1c5db4e7f46`  | `02_EVIDENCE/W3_檢查修補與驗收_證據型附錄.md` |
|  `W3_採納授權與GitHub讀回_證據型附錄.md`  |  3542  |  `311d5ab7742a7083c7a9eaa5085e5015f27a1a3b16de6a942aa7aece16075630`  | `02_EVIDENCE/W3_採納授權與GitHub讀回_證據型附錄.md` |

**證據 raw**：私有，未上推；公開只提供三份證據附錄與 `w3_consumer.py`。

## 04｜LastGood 與回復

| 項目 | 值 |
|---|---|
| LastGood | `FHS5-PLP/W3/PACK-NF-20261126-r1`；05 raw `88508d0bf7e7e557fe2447db07966197108c136a7634f34ed6c89ea5759a13ad` |
| 回復 | 刪本輪未發布新增物；MODIFY exact reverse；remote 用新 commit，不 force push |
| r1 | 完整保留，標 superseded，不刪 |

## 05｜Publication

| 項目 | 值 |
|---|---|
| remote | `https://github.com/shw097-team/FHS-5` |
| branch | `codex/w3-pack-nf-primary-20261126` |
| commit / readback | 見 `02_EVIDENCE/W3_採納授權與GitHub讀回_證據型附錄.md` §04 |
| state | `PUSHED_PENDING_READBACK`（推送後更新） |

## 06｜限制

- 16 原案、正式 W3 E2E、W2 requalification、產品 Checker/Consumer 未跑；不得宣產品 readiness。
- 私有 raw 與 SOURCE_LOCATORS 不公開；公開 manifest 用 logical locator。
- 本地主用與 GitHub 文件 publication 不等同 `RELEASED`。

