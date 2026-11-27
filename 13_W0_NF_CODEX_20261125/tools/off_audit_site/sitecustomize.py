# -*- coding: utf-8 -*-
"""FHS-5 NF-T01 observation profile (stdlib only, no product imports).

Loaded through ``PYTHONPATH`` as ``sitecustomize``.  Two independent,
env-gated duties:

* ``FHS5_OFF_PROFILE=1`` installs the legacy import blocker used by the OFF
  run (same block list / same message as the r1 harness).
* ``FHS5_AUDIT=<path>`` appends CPython audit events as JSONL.

The audit hook is observation only: it never blocks, rewrites or reorders the
product's own calls.  This file must stay dependency-free so that loading it
cannot itself create the effects it is supposed to observe.
"""
import json
import os
import re
import sys

_BLOCK = ("hgk", "fabric", "sbl", "fhs", "pipd", "hermes")
_TRACE = os.environ.get("FHS5_TRACE")
_OFF = os.environ.get("FHS5_OFF_PROFILE") == "1"

_SECRET = re.compile(
    r"(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9]{16,}|AKIA_[0-9A-Z]{16})"
)

_EVENTS = (
    "import", "open",
    "subprocess.Popen", "os.system", "os.exec", "os.spawn", "os.posix_spawn",
    "socket.", "ctypes.", "_winapi.CreateProcess", "os.remove", "os.rename",
)


def _log_blocked(fullname):
    if not _TRACE:
        return
    try:
        with open(_TRACE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"blocked": fullname}) + "\n")
    except Exception:
        pass


class _Blocker:
    def find_spec(self, fullname, path=None, target=None):
        top = fullname.split(".")[0].lower()
        if any(top.startswith(prefix) for prefix in _BLOCK):
            _log_blocked(fullname)
            raise ImportError("FHS5_LEGACY_BLOCKED:" + fullname)
        return None


if _OFF:
    sys.meta_path.insert(0, _Blocker())


def _install_audit(path):
    """Append audit events to *path*.  Never raises into the product."""
    try:
        fh = open(path, "a", encoding="utf-8", buffering=1)
    except Exception:
        return False

    pid = os.getpid()
    state = {"busy": False, "n": 0, "truncated": False}
    limit = 200000

    def text(value):
        try:
            if isinstance(value, bytes):
                out = value.decode("utf-8", "replace")
            elif isinstance(value, str):
                out = value
            elif type(value).__module__ == "socket":
                out = "<socket>"
            else:
                out = repr(value)
        except Exception:
            out = "<unrepr>"
        return out[:240]

    def project(event, args):
        if event in ("import", "open"):
            return [text(args[0]), text(args[1]) if len(args) > 1 else ""]
        if event == "subprocess.Popen":
            return [text(args[0]), text(args[1])]
        if event.startswith(("socket.", "ctypes.")):
            return [text(a) for a in args[:2]]
        return [text(a) for a in args[:3]]

    def hook(event, args):
        if state["busy"] or state["truncated"]:
            return
        if not event.startswith(_EVENTS):
            return
        state["busy"] = True
        try:
            if state["n"] >= limit:
                state["truncated"] = True
                fh.write(json.dumps({"pid": pid, "event": "_truncated"}) + "\n")
                return
            state["n"] += 1
            line = json.dumps(
                {"pid": pid, "ppid": os.getppid(), "event": event,
                 "args": project(event, args)},
                ensure_ascii=False,
            )
            fh.write(_SECRET.sub("[REDACTED]", line) + "\n")
        except Exception:
            pass
        finally:
            state["busy"] = False

    sys.addaudithook(hook)
    return True


_AUDIT = os.environ.get("FHS5_AUDIT")
if _AUDIT:
    _install_audit(_AUDIT)