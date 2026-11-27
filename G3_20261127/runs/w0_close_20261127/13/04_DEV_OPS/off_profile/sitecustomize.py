import os, sys, json
_BLOCK = ("hgk", "fabric", "sbl", "fhs", "pipd", "hermes")
class _Blocker:
    def find_spec(self, fullname, path=None, target=None):
        top = fullname.split(".")[0].lower()
        if any(top.startswith(b) for b in _BLOCK):
            try:
                with open(os.environ["FHS5_TRACE"], "a", encoding="utf-8") as f:
                    f.write(json.dumps({"blocked": fullname}) + "\n")
            except Exception:
                pass
            raise ImportError("FHS5_LEGACY_BLOCKED:" + fullname)
        return None
sys.meta_path.insert(0, _Blocker())
