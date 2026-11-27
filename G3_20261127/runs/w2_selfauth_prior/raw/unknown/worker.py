
import sys, time
from pathlib import Path
kind = sys.argv[1]
root = Path(sys.argv[2])
if kind == "to_before":
    time.sleep(5)
elif kind == "to_after":
    (root / "world.txt").write_text("POST\n", encoding="utf-8")
    time.sleep(5)
elif kind == "partial":
    (root / "a.txt").write_text("POST-A\n", encoding="utf-8")
    time.sleep(5)
elif kind == "exit0_wrong":
    (root / "world.txt").write_text("WRONG\n", encoding="utf-8")
    sys.exit(0)
