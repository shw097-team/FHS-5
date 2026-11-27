# S4 最小 ChangeSet（第 36_ 輪）

| 上位 | 受影真證據 |
|---|---|
| W0M | 假阻斷更正（locator 而非 drift）、NF/S1 血緣、fresh consume PASS（803/0）、OFF PASS → **W0 DONE（scoped）** |
| W1M | 67 ECP 改以真 Raw 指標判定：18 pass／46 partial／1 NA／2 DEFER |
| W2M | 12 RUN-* 綁定但無 executable（BUILD_MINIMAL_PENDING）、N04 PASS、N09 STOP_SCOPED |
| PROJ-01 | per-case runner ID／status、TPM 帶欄 |
| PROJ-03 | consumer fail-closed |
| PROJ-05 | FAR 仍依原適用 DEFER |

明確更正：35_ S4 中「W0 receipt SHA drift」為錯誤解讀，正式 AsBuilt 不採用。
