# G3 W0–W2 整合交接索引

| 欄 | 值 |
|---|---|
| 控制包 | `FHS-5_PLP_W0-W2_執行控制包_FINAL`；decision `PCNF-W0W2-ADOPT-20261127-01` |
| 基準 | S2/S3 `a2281bf5542d53ed67b678c0d5b91d0793cc81c4`（`codex/w0-w2-s2-s3-20261126T225929`） |
| 施工分支 | `codex/w0-w2-g3-native-20261127` |
| 內容 commit | `aad5a6de58ddba8d58b558f375be6e53db7ea7ef` |
| 交付 commit（docs） | `9c6bb8987a4128de47d303e322016d1a419ba553` |
| LastGood | `a2281bf`（未改動）；本輪未 force push、未 merge main |
| Checker | `evidence/CHECKER.json`：PASS／40 checks |
| Consumer | `evidence/W3_CONSUMER.json`：ACCEPT |
| W3 | technical `READY`；execution `NOT_ADMITTED` |

## 五 pin

| pin | 值 |
|---|---|
| source W0 | `baa516b5675589c1a329cd5f65970d8d6c12b7892dd7c079115e1251c9e6e96d` |
| source W1 | `f00b4ee93611e738e409d40758aa320b0bfec3ef0a01fea04dbf5bcb9f1566dc` |
| source W2 | `7bdc4a0acb497944450d89a2c347d26ca4ac8593f6ee47ac229215a80ff227e0` |
| candidate aggregate | `cfc7a1aac11b452bcef6b158bc38e0db7e082762d0305132242606a68f37be63`（56 成員） |
| oracle W0／W1／W2 | `da6fa6f3615f4043…`／`9e5c6a83b719c400…`／`a78e689d42265851…` |
| case set | W0 44／W1 13／W2 12 |
| evidence manifest | `56bf848c172ccdf2c85976c7522e1f4cb4d2796f09974fefa0a8b346ec14f4f3` |
| seal | `40d6e0715e77aa1e06edaa0e3f4efe4e7d06f955ff8d2974f51bffeeb7ac6942` |

## 已驗／未驗 ledger

| Wave | 已驗（本輪真 raw） | 未驗／NotCovered |
|---|---|---|
| W0 | SAMPLE 10/10、R4（含 junction）、R10、44 receipts reuse、OFF＋正控 | 24 原案、10 NF-T、803 checks |
| W1 | 12/13 案、API 84 clauses、Guide 九鍵、CODEX host 7 階段、115 tests、67 中 15 列 | HERMES-01、67 中 52 列、plugin Loaded/Installed、其他 Host |
| W2 | 12/12 案、DEV 真 apply/test/reverse/restore、OPS 真 effect/compensation、Checker、Consumer | 其他 Host、Publisher/Release、原域 DEV ECP、W3 effect |

## 原 raw 定位

`G3_20261127/runs/{w0,w1,w2}/raw/`；每個 raw 均有 argv／cwd／exit／stdout／stderr／pre-post／expected-observed。
`evidence/EVIDENCE_MANIFEST.json` 逐檔 bytes／SHA；`evidence/SEAL.json` 對 manifest；manifest 不嵌自身。

## 下一步

1. W0：Owner 指定 24 原案 runner 後補跑，或接受 scoped partial。
2. W1：綁 Hermes 與補 67 ECP 逐列 observed。
3. W2：以 `W3_CONSUMER.json` 為 W3 minimal readback；取得 W3 exact grant 後才可執行 W3。
