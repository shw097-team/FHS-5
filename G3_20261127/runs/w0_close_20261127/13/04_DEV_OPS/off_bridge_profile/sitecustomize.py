import os, sys, json
class _B:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] == "w1_bridge_reference":
            try:
                with open(os.environ["FHS5_TRACE"], "a", encoding="utf-8") as f:
                    f.write(json.dumps({"blocked": fullname}) + "\n")
            except Exception:
                pass
            raise ImportError("FHS5_BRIDGE_BLOCKED:" + fullname)
        return None
sys.meta_path.insert(0, _B())
