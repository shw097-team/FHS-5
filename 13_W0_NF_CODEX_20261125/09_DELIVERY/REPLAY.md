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

# 9. 本輪補強：prepatch Challenge / FAR / Guide Resume / WSL symlink / OFF
python tools\challenge_prepatch.py
python tools\far_run.py
python tools\guide_resume.py
python tools\security_wsl.py
python tools\off_legacy.py
python tools\off_bridge.py
python tools\off_far.py

# 10. 44 案（NF-T08 內含 collab chain，NF-T10 先 staged）
python tools\tqaep_run.py
python tools\challenge.py --candidate 02_CANDIDATE\repo --oracle 05_TQAEP\oracle.json `
  --receipts 05_TQAEP\receipts --pack 01_PACK\FHS-5_PLP_W0_NATIVE_FIRST `
  --summary 05_TQAEP\summary.json --out 03_PARTIES\challenge\challenge.json `
  --workroot 06_CHECKER\full --mode full

# 11. W1 consumer：stage1（允許 T10 pending）＋負例，最終化，再正式接收
python tools\consumer.py --handoff 09_DELIVERY\W0_HANDOFF.md `
  --evidence-manifest 10_EVIDENCE\EVIDENCE_MANIFEST.json --allow-pending-t10
python tools\consumer_negatives.py --handoff 09_DELIVERY\W0_HANDOFF.md `
  --evidence 10_EVIDENCE\EVIDENCE_MANIFEST.json
python tools\finalize_t10.py
python tools\evidence_manifest.py
python tools\consumer.py --handoff 09_DELIVERY\W0_HANDOFF.md `
  --evidence-manifest 10_EVIDENCE\EVIDENCE_MANIFEST.json --publish-manifest
```

**注意**：`dev_patch.py` 會以目前 HEAD 為 preimage 重新 commit；重播請在 clone 上操作，
不要改動已凍結的 `bb66a27`。正常重播只需 1、2、4、5、6、7、8、9。

預期：TQAEP `44/44 PASS`；Challenge `PASS`（32 checks、0 findings）；
consumer `consumed=true`（776 checks、10 negatives）；OPS `PASS`；
Legacy OFF `PASS`、Bridge OFF `PASS`、FAR OFF `PASS`；WSL security `PASS`。
