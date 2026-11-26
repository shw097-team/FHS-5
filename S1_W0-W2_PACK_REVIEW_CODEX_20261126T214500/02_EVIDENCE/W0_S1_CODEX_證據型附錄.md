# W0 S1 CODEX 證據型附錄（獨立檢修）

**review run**：`S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500`｜**reviewer**：CODEX Native main session（本地）｜**時間**：2026-11-26（Asia/Taipei）  
**subject**：`FHS5-PLP/W0/PACK-S1-20261126-r2`｜**candidate**：`W0-S1-r2-CODEX-PRIMARY`｜**adoption**：`PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION`  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`｜**product**：`B0／W0_NF_VALIDATED = NOT_RUN`  
**review strength**：主 session 自驗＋獨立重跑；非獨立產品 Checker，未產生產品驗收。

## 1｜身份、bytes 與可回取

| 檔 | bytes | SHA-256 |
|---|---:|---|
| `00_W0_PI_PD.md` | 40020 | `e9714d312ad07203d3cda5fd3652ec6f1918f711278230718fb49e8081f9a2c7` |
| `01_W0_DEV_ECP.md` | 16120 | `c0755bd7d6d16ca0f3b4acf65f8c51373bad61c75ead0af99ff2ec252fd84b85` |
| `02_W0_OPS_ECP.md` | 14787 | `863331d96f662a866febe15f11f35748a308eb6384c3519e2b23f0e8749f1906` |
| `03_W0_TQAEP.md` | 17698 | `f8ecb7518e834fc4584cce5188e49ade8a2f489c77938a4d659e06194085d3f2` |
| `04_W0_START_THIN_PROMPT.md` | 4454 | `83cddd44b39799dd44afd32a3d69cf0c3ff7dbac7efad88f1c1f4ccc727f408b` |
| `05_W0_SOURCE_MANIFEST.json` | 13270 | `97017494984e1d1a3b1b62de61f28c6ab0aea7a7f1caf67f65925039033c5e98` |

- 外置 seal：`02_EVIDENCE/seals/W0_PACK_SEAL.json`（1847 bytes，`653b0dc0548e00b9fd8867f423072fb943d199af609f290f50149568cece69bf`）
- pack tree（5 檔）：`b5b67fd1c24586cdad78f908cba17b4b39e66a19a417d5d83daa8b765fe58ff1`
- adoption record：`02_EVIDENCE/seals/S1_ADOPTION_RECORD.json`（`831ebcaecf47ecd0fa8c484bd816179b4ee394d512dca4ab1b92162b76d23c81`）；decision `S1-W0W2-CODEX-ADOPT-20261126-01`
- current pointer：`02_EVIDENCE/seals/S1_CURRENT_POINTER.json`（`e804a68e7c4d71b6c9638935e4d850103541dbea96bff4191eeab8a383d494e2`）
- review results：`02_EVIDENCE/S1_CODEX_REVIEW_RESULTS.json`（`2e8e8cf4aeb7f8184b382fdde77bca54f71e6531f5b3dc7a5968ad74e4bc3861`）
- 原上游 05：`e3772aeed0ac1460a55b5c3659eda3d939a01ad393926b74a3d552ec7b0b97d8`（原 05 sources 保留於 upstream；本 S1 05 列 10 現行 sources）

## 2｜檢修 ChangeCone（只動受影）

| 受影 | before → after | 理由／證據 |
|---|---|---|
| 六檔 header／05 身份 | `Wn-S1-r1-AUTHOR-CANDIDATE` → `Wn-S1-r2-CODEX-PRIMARY`；`AUTHOR_CANDIDATE_NOT_ADOPTED` → `PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION` | 本輪 Owner 預授權只對已驗合格包升格；產品 claim 不變 |
| 04 SOURCE 計數（W1/W2） | 「42 sources」→「10 現行 sources；原 42／24 源保留於 upstream」 | 04 與 05 不一致（FirstFail FF-01） |
| 05 denominators | 補 `wp`／`fuo`／`receiver_checks`／`b_index_*` | 控制包列明的原分母須機器可讀（FF-02） |
| 05 upstream | 加 `source_manifest_sources{count,sha256}` | 保留原 05 來源集可回取，不以精簡冒刪除 |
| seal／adoption | 重算 tree、05 raw、外置採納與 Current | 採納須綁最終 bytes（FF-03） |

## 3｜C1–C7 實查（本波）

| 面 | 觀察 | 判定 |
|---|---|---|
| C1 架構／雙去耦合 | C1 DD01–04 以 Native 五方與七 Seam 落地；C2 原 ID 全保留；C3 DAG 無 cycle 且 post 不作 pre；C5 04→R1–R5 可冷啟；C6 D1–D7/O1–O6 有真入口與 placeholder 停點。 | PASS（文件） |
| C2 原義／內部一致 | 原 ID token 對原版逐檔比對：missing=0；14 WP、24 原案（F5-W0-T01..T24）、NF-T01..T10、SAMPLE R1–R10、44 歷史分帳（24＋10＋10）、14 HOLD、W0 無外置 asset（fixture inline 於 03） | PASS（修 FF-01/02 後） |
| C3 阻斷／鏈路 | typed DAG 無 cycle；HARD edge 有原據與停點；post/Publisher 不作 pre | PASS |
| C4 Owner／issuer | 單一 Human Owner；ECP/Advice/permit 非 Grant；W2 舊撤權不動 | PASS |
| C5 Native E2E／冷啟 | 04 可讀 05→00→01/02/03 並定位第一個合法 op；未解析值有 placeholder/stop | PASS（文件；產品 NOT_RUN） |
| C6 DEV/OPS ECP | 01 有 exact write-set／preimage／reverse／post；02 有 host/principal/epoch/receiver/WorldRaw/compensation；入口 UNBOUND 如實標記 | PASS（文件）／產品 NotCovered |
| C7 TQAEP | 原案 exact set、fixture/oracle、POS 合取、NEG 真拒、缺/空/重複 CaseSet 與 runner 假冒有反例 | PASS（文件） |

## 4｜V1–V3／DOC 檢測（真跑）

| DOC | 方法（實際） | 結果 |
|---|---|---|
| DOC-01 | 5 MD 非空／UTF-8；05 strict JSON（dup-key hook）；pack_files 5 列 bytes/SHA 對實檔 | PASS |
| DOC-02 | 05/seal 對 05 raw、5 MD、assets bytes/SHA；tree 重算；sources 10/10 可回取 | PASS |
| DOC-03 | 原 00–03 的 ID token 集合對新版逐檔 join（missing=0）；case/denominator 對 03 文本 | PASS |
| DOC-04 | 04 cold-start 段落逐項對 00/01/02/03/05 章節存在性；first op 可定位 | PASS |
| DOC-05 | adoption/claim/撤權／無 Grant：05 `not_claimed` 不含 ADOPTED 後仍保留產品禁宣；W2 Writer 仍 BLOCKED | PASS |
| DOC-06 | clean copy 重跑同一檢查（退回路徑）；index/seal/adoption/current 互相可核 | PASS |

**隔離反證（本輪 10 例，全部正確拒絕）**：missing_03、empty_00、duplicate_json_key、byte_flip、path_escape、seal_tamper、draft_flag、wrong_case_id、asset_flip、orphan_oracle。完整 errors 見 `S1_CODEX_REVIEW_RESULTS.json`。

## 5｜FirstFail 與修補重驗

| # | FirstFail | 修補 | 重驗 |
|---|---|---|---|
| FF-01 | 04 宣稱 42 sources，05 實為 10 | 改為 10 現行 sources；原 42／24 記入 upstream | 04↔05 join；grep 無殘留（歷史引言除外） |
| FF-02 | 05 分母缺項 | 補 wp/fuo/receiver_checks/b_index | 05 strict parse＋seal 重算 |
| FF-03 | 採納狀態仍 AUTHOR_CANDIDATE、draft=true | r2 身份＋採納＋外 seal/Current | 身份/狀態檢查＋fresh readback |
| FF-04 | 檢修工具對缺 03 會 crash | 改為明示 reject | 10/10 反證通過 |

## 6｜原義／分母守恆與歷史

- 14 WP、24 原案（F5-W0-T01..T24）、NF-T01..T10、SAMPLE R1–R10、44 歷史分帳（24＋10＋10）、14 HOLD、W0 無外置 asset（fixture inline 於 03）
- 歷史：694 evidence／803 consumer checks／10 fail-closed／32 Challenge 只作 HISTORICAL_REPORTED
- 原版 00–03 逐段保留率 95.9–100%（正規化段落比對）；所有原 ID token 0 missing。
- 原 NF 包與 r1 候選均未覆寫；LastGood 可讀。

## 7｜未閉項與下一合法動作

- 產品：`B0／W0_NF_VALIDATED = NOT_RUN`；本輪不發任何 DEV/OPS/Host/Release 權限。
- Next：S2 W0-R1 復用 13_ tools／44 receipts → R2 最小 DEV/OPS 正控 → R3 OFF → R5 Windows 安全；缺真 repo/host 只停受影 slice。
- 真阻斷（如適用）：repo chdir/ACL、Host/receiver、Owner 具名 protected scope、獨立 Checker；只停受影 slice，保 LastGood 與 Resume。
