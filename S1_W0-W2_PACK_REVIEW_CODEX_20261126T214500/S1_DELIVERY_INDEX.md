# S1 W0–W2 CODEX 檢修交付索引（PRIMARY／DOCUMENT）

**run_id**：`S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500`｜**decision**：`S1-W0W2-CODEX-ADOPT-20261126-01`｜**時間**：2026-11-26（Asia/Taipei）  
**review root（O）**：`C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500`  
**claim ceiling**：`S1_DOC_VALIDATED_DOCUMENT_ONLY`｜**product**：`NOT_RUN`｜**W2 Writer**：`BLOCKED_NOT_ADMITTED`

> 本索引只證明 S1 三套控制包完成實質檢修、文件驗收與依 Owner 預授權的主用升格；不是產品 PASS、不是 ECP/Advice/Grant，也不發任何外部 DEV/OPS/Host/Release 權限。

## 1｜最終判定（實際結果）

| Wave | DOC-01..06 | V1／V2／V3 | 主用／可施工入口 | 產品狀態 | 最小未閉項 |
|---|---|---|---|---|---|
| W0 | PASS×6 | PASS／PASS（文件）／PASS | `W0-S1-r2-CODEX-PRIMARY`；S2 入口 R1 | `B0_NF=NOT_RUN` | repo/ACL bind、B0 未跑 |
| W1 | PASS×6 | PASS／PASS（文件）／PASS | `W1-S1-r2-CODEX-PRIMARY`；S2 入口 P01 | `W1_NF_VALIDATED=NOT_RUN` | Host serve/consume、獨立 Checker |
| W2 | PASS×6 | PASS／PASS（文件）／PASS | `W2-S1-r2-CODEX-PRIMARY`；S3 入口 R0 | `PARTIAL`：12 案 NOT_RUN；Writer BLOCKED | 具名 protected scope、真 repo/host、12 案 raw |

## 2｜三套六檔（15 MD＋3 JSON）

| Wave | 檔（相對 O） | bytes | SHA-256 | 本地載點 |
|---|---|---:|---|---|
| W0 | `01_BODY/FHS-5_PLP_W0_NATIVE_FIRST/00_W0_PI_PD.md` | 40020 | `e9714d312ad07203d3cda5fd3652ec6f1918f711278230718fb49e8081f9a2c7` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W0_NATIVE_FIRST\00_W0_PI_PD.md` |
| W0 | `01_BODY/FHS-5_PLP_W0_NATIVE_FIRST/01_W0_DEV_ECP.md` | 16120 | `c0755bd7d6d16ca0f3b4acf65f8c51373bad61c75ead0af99ff2ec252fd84b85` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W0_NATIVE_FIRST\01_W0_DEV_ECP.md` |
| W0 | `01_BODY/FHS-5_PLP_W0_NATIVE_FIRST/02_W0_OPS_ECP.md` | 14787 | `863331d96f662a866febe15f11f35748a308eb6384c3519e2b23f0e8749f1906` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W0_NATIVE_FIRST\02_W0_OPS_ECP.md` |
| W0 | `01_BODY/FHS-5_PLP_W0_NATIVE_FIRST/03_W0_TQAEP.md` | 17698 | `f8ecb7518e834fc4584cce5188e49ade8a2f489c77938a4d659e06194085d3f2` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W0_NATIVE_FIRST\03_W0_TQAEP.md` |
| W0 | `01_BODY/FHS-5_PLP_W0_NATIVE_FIRST/04_W0_START_THIN_PROMPT.md` | 4454 | `83cddd44b39799dd44afd32a3d69cf0c3ff7dbac7efad88f1c1f4ccc727f408b` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W0_NATIVE_FIRST\04_W0_START_THIN_PROMPT.md` |
| W0 | `01_BODY/FHS-5_PLP_W0_NATIVE_FIRST/05_W0_SOURCE_MANIFEST.json` | 13270 | `97017494984e1d1a3b1b62de61f28c6ab0aea7a7f1caf67f65925039033c5e98` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W0_NATIVE_FIRST\05_W0_SOURCE_MANIFEST.json` |
| W1 | `01_BODY/FHS-5_PLP_W1_NATIVE_FIRST/00_W1_PI_PD.md` | 41886 | `b0c4a260d272168b277d18b4ba3c17c07eb8821e0314e6d7298b202f37a7d42a` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W1_NATIVE_FIRST\00_W1_PI_PD.md` |
| W1 | `01_BODY/FHS-5_PLP_W1_NATIVE_FIRST/01_W1_DEV_ECP.md` | 24767 | `c20cf0f1cc8af8138e04ae3f9c01b16dc6aa6cadc9bb1f2a544166564147e2e9` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W1_NATIVE_FIRST\01_W1_DEV_ECP.md` |
| W1 | `01_BODY/FHS-5_PLP_W1_NATIVE_FIRST/02_W1_OPS_ECP.md` | 15457 | `49c625632a8eb5cfd82fab0ec7b68411011a5222b3fcdb9a12fda3254aa0600f` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W1_NATIVE_FIRST\02_W1_OPS_ECP.md` |
| W1 | `01_BODY/FHS-5_PLP_W1_NATIVE_FIRST/03_W1_TQAEP.md` | 23508 | `36dc623a45c313f5751e7173054fb2d22b818251f4e396c26de4abf1dc965cfc` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W1_NATIVE_FIRST\03_W1_TQAEP.md` |
| W1 | `01_BODY/FHS-5_PLP_W1_NATIVE_FIRST/04_W1_START_THIN_PROMPT.md` | 4547 | `c92e2cc0510c8b7d225513a588ce4c2eeb115d2ba009281356a012fa3413e03c` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W1_NATIVE_FIRST\04_W1_START_THIN_PROMPT.md` |
| W1 | `01_BODY/FHS-5_PLP_W1_NATIVE_FIRST/05_W1_SOURCE_MANIFEST.json` | 16876 | `d1c741533bea41b8d786ec870b6f66323739a65ebdafd241545dc4afa9dff28c` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W1_NATIVE_FIRST\05_W1_SOURCE_MANIFEST.json` |
| W2 | `01_BODY/FHS-5_PLP_W2_NATIVE_FIRST/00_W2_PI_PD.md` | 69222 | `c83815061a7604ed6f276c6dba50b216e9dd96d0742f0c52ac86468d56d53e7c` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W2_NATIVE_FIRST\00_W2_PI_PD.md` |
| W2 | `01_BODY/FHS-5_PLP_W2_NATIVE_FIRST/01_W2_DEV_ECP.md` | 25747 | `698ffe006ec2b8a4dcf45ef24cd1a40f8d7f0360a1e647f509a83eb98310147b` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W2_NATIVE_FIRST\01_W2_DEV_ECP.md` |
| W2 | `01_BODY/FHS-5_PLP_W2_NATIVE_FIRST/02_W2_OPS_ECP.md` | 23141 | `58a34bfc1d4a57b5c878dca05edfbf6c32bc64c755a1592659affaa2777e5ddf` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W2_NATIVE_FIRST\02_W2_OPS_ECP.md` |
| W2 | `01_BODY/FHS-5_PLP_W2_NATIVE_FIRST/03_W2_TQAEP.md` | 25938 | `a539ab2ee57c20f413d657b09c7f8016e4c7074fae64c32abda15b71d540dfcc` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W2_NATIVE_FIRST\03_W2_TQAEP.md` |
| W2 | `01_BODY/FHS-5_PLP_W2_NATIVE_FIRST/04_W2_START_THIN_PROMPT.md` | 5121 | `45686eb470f8d790b8d37c748a3db7442492fdf270713ee3208d0badd042b8b4` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W2_NATIVE_FIRST\04_W2_START_THIN_PROMPT.md` |
| W2 | `01_BODY/FHS-5_PLP_W2_NATIVE_FIRST/05_W2_SOURCE_MANIFEST.json` | 17216 | `911d06c98eef8edea13bf0c82956a55d420daa93e7599f3344f317a84486b65b` | `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\01_BODY\FHS-5_PLP_W2_NATIVE_FIRST\05_W2_SOURCE_MANIFEST.json` |

## 3｜證據型附錄、外置 seal／採納／Current

| 檔（相對 O） | bytes | SHA-256 | 用途 |
|---|---:|---|---|
| `02_EVIDENCE/W0_S1_CODEX_證據型附錄.md` | 6830 | `1a17ef9b65902614ef8c3e4cb0c1bc2ab80ed5dfa14ce261b5a72081cf8d877e` | 本輪 C1–C7、V1–V3、修補史 |
| `02_EVIDENCE/W1_S1_CODEX_證據型附錄.md` | 6801 | `304e72334f7ea36cded66d4ac116d719316d23df75e44cd2d247726303bdf5d4` | 本輪 C1–C7、V1–V3、修補史 |
| `02_EVIDENCE/W2_S1_CODEX_證據型附錄.md` | 6936 | `61cdf801cf84bcd5b8493bf8b53afedfc0164dafc8f2fbf33f6f4f8f23bc5470` | 本輪 C1–C7、V1–V3、修補史 |
| `02_EVIDENCE/seals/W0_PACK_SEAL.json` | 1847 | `653b0dc0548e00b9fd8867f423072fb943d199af609f290f50149568cece69bf` | 外置 pack seal（5 檔＋assets） |
| `02_EVIDENCE/seals/W1_PACK_SEAL.json` | 6112 | `27431b0a743cd4e3ba7349e8d2e39d782ee6cb3f02e5873132c8bf25647cfe62` | 外置 pack seal（5 檔＋assets） |
| `02_EVIDENCE/seals/W2_PACK_SEAL.json` | 5954 | `1aa5f4af659a0edfccd9c7c2144015f6364f0a80e4c6e8575a8778c786bf9ea5` | 外置 pack seal（5 檔＋assets） |
| `02_EVIDENCE/seals/S1_ADOPTION_RECORD.json` | 3906 | `831ebcaecf47ecd0fa8c484bd816179b4ee394d512dca4ab1b92162b76d23c81` | Owner 預授權落地／三包主用 |
| `02_EVIDENCE/seals/S1_CURRENT_POINTER.json` | 1796 | `e804a68e7c4d71b6c9638935e4d850103541dbea96bff4191eeab8a383d494e2` | 當期主用／LastGood 指標 |
| `02_EVIDENCE/S1_CODEX_REVIEW_RESULTS.json` | 10719 | `2e8e8cf4aeb7f8184b382fdde77bca54f71e6531f5b3dc7a5968ad74e4bc3861` | 機器可讀檢測／反證結果 |
| `02_EVIDENCE/seals/S1_PUBLICATION_RECEIPT.json` | 2639 | `8db6a8519da2dd0273abb962b5c97e7ec8701ca137814146c33908cf1f6335d3` | 發布狀態／讀回（見 §7） |

作者原證據保留：`02_EVIDENCE/W0_S1_證據附件.md`、`W1_S1_證據附件.md`、`W2_S1_證據附件.md`、`doc_results.json`（作者自檢，不作為本輪判定權威；本輪已獨立重跑）。

## 4｜Assets（原 bytes，包內相對位置）

| Wave | 數量 | 內容 |
|---|---:|---|
| W0 | 0 | fixture inline 於 03 |
| W1 | 26 | 13 fixtures＋13 oracles |
| W2 | 25 | case_index＋12 fixtures＋12 oracles |

## 5｜本輪實修（FirstFail → 修補 → 重驗）

| # | FirstFail | 修補 | 重驗 |
|---|---|---|---|
| FF-01 | 04（W1/W2）宣稱 42 sources，05 實為 10 | 改為 10 現行 sources；原 42／24 記入 05 upstream | 04↔05 join；grep |
| FF-02 | 05 分母缺 wp／fuo／receiver_checks／13+3 | 補齊機器可讀欄 | strict parse＋seal 重算 |
| FF-03 | 採納狀態仍候選、draft=true | r2 身份＋採納＋seal/Current | 身份、狀態、fresh readback |
| FF-04 | 檢修工具缺 03 會 crash | 改為明示 reject | 10/10 反證 |

## 6｜主用／LastGood

| Wave | Active（主用） | Manifest SHA-256 | Pack tree | LastGood（保留） |
|---|---|---|---|---|
| W0 | `FHS5-PLP/W0/PACK-S1-20261126-r2`／`W0-S1-r2-CODEX-PRIMARY` | `97017494984e1d1a3b1b62de61f28c6ab0aea7a7f1caf67f65925039033c5e98` | `b5b67fd1c24586cdad78f908cba17b4b39e66a19a417d5d83daa8b765fe58ff1` | `FHS5-PLP/W0/PACK-NF-20261125-03`（W0-NF-r3-CODEX-PRIMARY） |
| W1 | `FHS5-PLP/W1/CONTROL_PACK/2026-11-26-s1-r2`／`W1-S1-r2-CODEX-PRIMARY` | `d1c741533bea41b8d786ec870b6f66323739a65ebdafd241545dc4afa9dff28c` | `593314d503a162caea4c05dc263cd6e68511cfe5b70446043560bc757347d18f` | `FHS5-PLP/W1/CONTROL_PACK/2026-11-25-nf-r2`（W1-NF-r2-CODEX-PRIMARY） |
| W2 | `FHS5-PLP/W2/PACK-S1-20261126-r2`／`W2-S1-r2-CODEX-PRIMARY` | `911d06c98eef8edea13bf0c82956a55d420daa93e7599f3344f317a84486b65b` | `cc7d91a1f7f63e89b93c9a216286d746cccd0622c14d9448afc8a935cbb77943` | `FHS5-PLP/W2/PACK-NF-20261126-r3`（W2-NF-r3-CODEX-PRIMARY） |

## 7｜GitHub 發布與遠端讀回

- 狀態：`PUBLISH_BLOCKED_PENDING_DESTINATION_AUTHORIZATION`｜Repo：`https://github.com/shw097-team/FHS-5`｜branch：`codex/s1-w0-w2-dd-primary-20261126T214500`
- push：未執行（platform policy rejected the push as external publication of project documents without explicit user approval; no push command executed and no workaround attempted）
- content commit（本地）：`802a68ad8ba678985c7b477b71e9d2ec150af2e8`｜tree：`edcd6cb433b10dd308402c956ea9a748badf9c4e`
- delivery commit：`PENDING（本地收據 commit）`
- `git ls-remote` readback：`N/A (not pushed)`
- 遠端內容核對：`N/A`

## 8｜下一合法工單

| Wave | 第一合法 op | 必要前件 | 不得 |
|---|---|---|---|
| W0 | S2 W0-R1：復用 13_ tools／44 receipts | 只讀來源＋同位 evidence | 重跑 44、宣 B0 PASS |
| W1 | S2 P01：Identity/Reuse freeze | 授權來源、真 bytes/SHA | 用 13 案核銷 67 ECP |
| W2 | S3 R0：隔離 candidate＋five pins | Product `dada2354…`、Delivery `3346076c…` | 把 W3 替身當 W2、解封 Writer |

W2 之後：R1 安全 RED（零 effect）→（具名 protected scope 後）R2 DEV-A／R3 OPS-A → R4 12 案 → R5 正式驗收與 W3 fresh consume。

## 9｜未閉項（如實）

- 三波產品案全 `NOT_RUN`；本輪未產生任何 actual raw、產品 Checker 或 Consumer receipt。
- W2 原 Writer 撤權與安全 Finding 不動；protected write 需 S3 新具名 scope。
- 本機 repo `git -C` chdir 被拒（`REPO_CHDIR_DENIED`）；已用 `--git-dir` 讀 blob 與推送路徑完成必要核對。
- 上游 MASTER/PROG/PROJ/WM 回寫屬 S4，未做。

## 10｜取得方式

- 全部檔案在 `C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500`；逐檔完整路徑見 §2/§3，可直接開啟。
- 可選整包 ZIP：`C:\Projects\Agent_Workspace\FHS-5_Workspace\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500\S1_W0-W2_PACK_REVIEW_CODEX_20261126T214500.zip`（若存在）。
- 未造外部下載 URL；GitHub 內容以 commit-pinned 路徑引用。
