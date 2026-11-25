# Publication status（FHS-5 W0-NF）

| 欄 | 值 |
|---|---|
| authorized target | `https://github.com/shw097-team/FHS-5`（public，Owner 指定） |
| local commits | 前輪 `f8732527..c0d2b94`；本輪 M1 `2fc2c29`＋`7af6748`、M2/M3 與交付續 commit（以 `git log -1` 為準） |
| remote main | `c0d2b9476385ec708d518347ac543fd19a4d9a44`（M1/M2/M3 待推送） |
| push | Owner 已授權；以受權 token 檔經 credential helper fast-forward，不 force |
| result | M1 byte-preserving 修復已本地完成；M2/M3 commit 後推送 |
| verification | 上推後 `git ls-remote` 與 GitHub raw 重新核對 |
| this round | `LOCAL_COMMITS_READY`→推送→clean-receive Consumer |
| next legal action | commit M2/M3；push；從遠端 clone 執行 Consumer |

**邊界**：本檔在推送前不代表 remote 已更新；推送後以 `git ls-remote` 與 raw 核對為準。
