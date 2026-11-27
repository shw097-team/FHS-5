#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-scope audit for the standalone receipt gate (test harness only).

Installs a CPython audit hook, executes consumer.py in-process through runpy
and reports every `open` under the W0 root plus any subprocess/network event.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import runpy
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--expected-receipt-sha", required=True)
    ap.add_argument("--downstream-marker")
    a = ap.parse_args()

    target = Path(a.target).resolve()
    root = Path(a.root).resolve()
    receipt = Path(a.receipt).resolve()
    opens: list[str] = []
    events: list[str] = []

    def hook(event, args):
        if event == "open":
            try:
                opens.append(str(args[0]))
            except Exception:
                pass
        elif event.startswith(("subprocess.", "os.system", "os.exec",
                               "os.spawn", "socket.")):
            events.append(event)

    sys.addaudithook(hook)
    sys.argv = [str(target), "--verify-receipt", str(receipt),
                "--expected-receipt-sha", a.expected_receipt_sha]
    if a.downstream_marker:
        sys.argv += ["--downstream-marker", a.downstream_marker]
    code = 0
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        try:
            runpy.run_path(str(target), run_name="__main__")
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 0

    def under_root(p: str) -> bool:
        try:
            return Path(p).resolve().is_relative_to(root)
        except Exception:
            return False

    root_opens = sorted({p for p in opens if p and under_root(p)})
    extra = [p for p in root_opens
             if Path(p).resolve() not in (target, receipt)]
    try:
        gate_stdout = json.loads(captured.getvalue() or "{}")
    except Exception:
        gate_stdout = {"raw": captured.getvalue()[-1000:]}
    print(json.dumps({
        "schema": "FHS5.W0NF.ReceiptGateAudit@1",
        "target": str(target),
        "root": str(root),
        "receipt": str(receipt),
        "exit": code,
        "gate_stdout": gate_stdout,
        "root_opens": root_opens,
        "unexpected_root_opens": extra,
        "process_or_network_events": sorted(set(events)),
        "zero_outside_read": not extra,
        "zero_process_events": not events,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
