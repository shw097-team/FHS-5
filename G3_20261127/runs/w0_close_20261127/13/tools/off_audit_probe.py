#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NF-T01 observation positive control.

Actually triggers every category the OFF harness claims to observe, so a live
observer is proven rather than assumed:

* legacy provider import attempt (blocked by the OFF profile)
* file open / write / readback
* child process spawn (subprocess.Popen + _winapi.CreateProcess)
* Python grandchild that inherits the profile (second observed pid)
* real loopback TCP send/recv (socket.bind/connect, payload must round-trip)
* native library load and call (ctypes.dlopen + ctypes.call_function)
* os.system call (os.system audit event)

Each action reports its own result; the harness cross-checks those results
against the audit stream.  Exit code is 0 only when every action behaved as
expected.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import socket
import subprocess
import sys
import threading
from pathlib import Path

GRANDCHILD = r'''
import os, sys
path = os.path.join(sys.argv[1], "grandchild.txt")
with open(path, "w", encoding="utf-8") as fh:
    fh.write("GRANDCHILD")
print("GRANDCHILD_OK")
'''


def probe_blocked_import(expect: str) -> dict:
    rec = {"expect": expect}
    try:
        import hgk_core  # noqa: F401
    except ImportError as exc:
        rec.update({"blocked": True, "imported": False, "error": str(exc)})
    except Exception as exc:  # anything else is a real failure
        rec.update({"blocked": False, "imported": False,
                    "error": type(exc).__name__ + ": " + str(exc)})
    else:
        rec.update({"blocked": False, "imported": True,
                    "value": getattr(hgk_core, "VALUE", None)})
    if expect == "blocked":
        rec["ok"] = bool(rec["blocked"] and "FHS5_LEGACY_BLOCKED" in rec.get("error", ""))
    else:
        rec["ok"] = bool(rec["imported"])
    return rec


def probe_open(workdir: Path) -> dict:
    path = workdir / "probe_marker.txt"
    data = b"FHS5-NF-T01-OBSERVED"
    path.write_bytes(data)
    back = path.read_bytes()
    return {"path": str(path), "bytes": len(data),
            "sha256": hashlib.sha256(back).hexdigest(),
            "readback_ok": back == data, "ok": back == data}


def probe_child(workdir: Path) -> dict:
    r = subprocess.run([sys.executable, "-c", "print('CHILD_OK')"],
                       capture_output=True, text=True, timeout=60)
    return {"exit": r.returncode, "stdout": r.stdout.strip(),
            "ok": r.returncode == 0 and "CHILD_OK" in r.stdout}


def probe_grandchild(workdir: Path) -> dict:
    r = subprocess.run([sys.executable, "-c", GRANDCHILD, str(workdir)],
                       capture_output=True, text=True, timeout=60)
    path = workdir / "grandchild.txt"
    body = path.read_text(encoding="utf-8") if path.is_file() else ""
    return {"exit": r.returncode, "stdout": r.stdout.strip(), "file": str(path),
            "file_body": body,
            "ok": r.returncode == 0 and "GRANDCHILD_OK" in r.stdout and body == "GRANDCHILD"}


def probe_loopback() -> dict:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    got = []
    err = []

    def accept():
        try:
            conn, _ = srv.accept()
            got.append(conn.recv(16))
            conn.sendall(b"PONG")
            conn.close()
        except Exception as exc:
            err.append(type(exc).__name__ + ": " + str(exc))

    t = threading.Thread(target=accept, daemon=True)
    t.start()
    sent, received = b"PING", b""
    try:
        c = socket.create_connection(("127.0.0.1", port), timeout=5)
        c.sendall(sent)
        c.settimeout(5)
        received = c.recv(16)
        c.close()
    except Exception as exc:
        err.append(type(exc).__name__ + ": " + str(exc))
    finally:
        t.join(5)
        srv.close()
    return {"port": port, "sent": sent.decode(), "received": received.decode(),
            "server_received": [b.decode("utf-8", "replace") for b in got],
            "errors": err,
            "ok": received == b"PONG" and got == [sent] and not err}


def probe_ctypes() -> dict:
    try:
        k32 = ctypes.CDLL("kernel32")
        pid = int(k32.GetCurrentProcessId())
        tick = int(k32.GetTickCount())
        pointer = ctypes.cast(k32.GetCurrentProcessId, ctypes.c_void_p).value
        ok = pid == os.getpid() and tick >= 0 and bool(pointer)
        return {"library": "kernel32", "pid": pid, "tick": tick,
                "resolved_pointer": bool(pointer), "ok": ok}
    except Exception as exc:
        return {"library": "kernel32", "error": type(exc).__name__ + ": " + str(exc),
                "ok": False}


def probe_os_system() -> dict:
    rc = os.system("cmd /c exit 7")
    return {"command": "cmd /c exit 7", "rc": rc, "errorlevel": rc >> 8,
            "ok": rc in (0, 7)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--expect", choices=("blocked", "allowed"), default="blocked")
    ns = ap.parse_args()
    workdir = Path(ns.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    result = {
        "schema": "FHS5.W0NF.AuditProbe@1",
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "off_profile": os.environ.get("FHS5_OFF_PROFILE") == "1",
        "audit_env_set": bool(os.environ.get("FHS5_AUDIT")),
        "blocked_import": probe_blocked_import(ns.expect),
        "open_marker": probe_open(workdir),
        "child": probe_child(workdir),
        "grandchild": probe_grandchild(workdir),
        "loopback": probe_loopback(),
        "ctypes_load": probe_ctypes(),
        "os_system": probe_os_system(),
    }
    actions = ["blocked_import", "open_marker", "child", "grandchild",
               "loopback", "ctypes_load", "os_system"]
    result["action_results"] = {name: bool(result[name]["ok"]) for name in actions}
    result["all_ok"] = all(result["action_results"].values())
    text = json.dumps(result, ensure_ascii=False, indent=2)
    Path(ns.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["all_ok"] else 3


if __name__ == "__main__":
    sys.exit(main())