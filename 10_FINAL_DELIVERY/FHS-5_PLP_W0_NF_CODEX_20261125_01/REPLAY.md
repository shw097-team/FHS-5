# 重播說明（W0-NF）

所有命令皆在 `C:\Projects\Agent_Workspace\FHS-5_Workspace\13_W0_NF_CODEX_20261125` 執行；
Python 3.11.9、Git 2.53.0。raw stdout/stderr 在對應 `raw/`。

```powershell
cd C:\Projects\Agent_Workspace\FHS-5_Workspace\13_W0_NF_CODEX_20261125

# 1. 封存核對
python tools\tpm_contracts.py

# 2. Guide / Bridge
python tools\guide.py
python tools\bridge_run.py

# 3. DEV red→patch→retest（候選已在 bb66a27；重播需回到 5eab43d 之 clone）
python tools\dev_patch.py

# 4. OPS 與 OFF trace
python tools\ops_run.py

# 5. FAR
python tools\far_run.py

# 6. 44 案 TQAEP
python tools\tqaep_run.py

# 7. 獨立 Challenge（full 需 44 receipts）
python tools\challenge.py --candidate 02_CANDIDATE\repo --oracle 05_TQAEP\oracle.json `
  --receipts 05_TQAEP\receipts --pack 01_PACK\FHS-5_PLP_W0_NATIVE_FIRST `
  --summary 05_TQAEP\summary.json --out 03_PARTIES\challenge\challenge.json `
  --workroot 06_CHECKER\full --mode full

# 8. 證據 manifest
python tools\evidence_manifest.py

# 9. W1 consumer
python tools\consumer.py --pack 01_PACK\FHS-5_PLP_W0_NATIVE_FIRST --repo 02_CANDIDATE\repo `
  --handoff 09_DELIVERY\W0_HANDOFF.md --evidence-manifest 10_EVIDENCE\EVIDENCE_MANIFEST.json
```

**注意**：`dev_patch.py` 會以目前 HEAD 為 preimage 重新 commit；重播請在 clone 上操作，
不要改動已凍結的 `bb66a27`。正常重播只需 1、2、4、5、6、7、8、9。

預期：TQAEP `44/44 PASS`；Challenge `PASS`（31 checks、0 findings）；
consumer `consumed=true`；OPS `PASS`；legacy imports `[]`。
