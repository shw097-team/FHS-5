# G3 W0–W2 整合交接索引（真狀態）

| 欄 | 值 |
|---|---|
| 控制包 | `FHS-5_PLP_W0-W2_執行控制包_FINAL` |
| 基準 | `a2281bf`；本輪基線 `ef40abf` |
| 分支 | `codex/w0-w2-g3-native-20261127` |
| 內容 commit | `aad5a6de58ddba8d58b558f375be6e53db7ea7ef` |
| 文件 commit | `9c6bb8987a4128de47d303e322016d1a419ba553` |
| Checker | `PASS／44 checks` |
| Consumer | `BLOCKED_NOT_ADMITTED` |
| W0 | **PARTIAL 41/44** |
| W1 | **SCOPED_PARTIAL**：12/13；67 ECP 51 observed |
| W2 | **NOT_ADMITTED**：9 PASS＋3 NOT_ADMITTED |
| W3 | **NOT_ADMITTED** |

## 五 pin（結構化）

| pin | 值 |
|---|---|
| source W0／W1／W2 | `baa516b56755…`／`f00b4ee93611…`／`7bdc4a0acb49…` |
| candidate aggregate | `3490388ef7cce32a5cbfcfd46c174cddbd610bb818886bc24a165b7ccbb0043b`（60 成員） |
| oracle aggregate W0／W1／W2 | `45632470e5a3…`／`a741098618a2…`／`70cbc5017a39…` |
| case set W0／W1／W2 | 44／13／12 |
| evidence manifest | `c2c5ae8808416b06c8846c52ad2869a0caf7ebb8fee2fff8b9758870e4a60c62` |
| seal | `08705b48702f8f3b614de3b910bbf2deeb2a499f9ad259885049bf262b675edf` |

## 已驗／未驗

| Wave | 已驗 | 未驗 |
|---|---|---|
| W0 | 41 案 PASS | NF-T01、NF-T08、NF-T10；consumer 拒絕 |
| W1 | 12/13、51 ECP observed、第二包、115 tests | 10 NOT_ADMITTED、1 partial、3 host |
| W2 | 9 非效果案、UNKNOWN 4/4 | DEV-01／DEV-02／OPS-01、N09 受保護段 |

## 外部依賴

1. W0：NF-T08 契約上下文、NF-T01 cold OFF 契約、NF-T10 重綁。
2. W1：Hermes／ChatGPT／第二 principal。
3. W2：Owner／Issuer 對 `-05`／`-06` 簽發 ISSUED。
4. W3：W2 admitted 後另取 W3 exact grant。
