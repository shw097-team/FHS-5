# REPLAY

```powershell
$PACK = "C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\control_pack\FHS-5_PLP_W1_NATIVE_FIRST"
python "C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\W1\impl\nf_reader.py" inspect --pack $PACK
python "C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\W1\impl\bridge_nf.py" inspect --pack $PACK
python -m unittest discover -s "C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\W1\check" -p "test_*.py" -v
python "C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\W1\check\run_cases_nf.py" --pack $PACK --out "C:\Projects\Agent_Workspace\FHS-5_Workspace\worktrees\W1_NF_r3\16_W1_NF_CODEX_20261125T222954\evidence"
openspec validate w1-nf-r2-product
```
