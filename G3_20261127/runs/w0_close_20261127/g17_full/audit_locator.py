#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import contextlib, io, json, runpy, sys
from pathlib import Path

def main():
    w1, handoff, root, repo, out_root, receipt, expected = sys.argv[1:8]
    outside = Path(receipt).resolve()
    opens = []
    def hook(event, args):
        if event == "open":
            try:
                opens.append(str(Path(args[0]).resolve()))
            except Exception:
                try: opens.append(str(args[0]))
                except Exception: pass
    sys.addaudithook(hook)
    sys.argv = [w1, "--handoff", handoff, "--root", root, "--repo", repo,
                "--out-root", out_root, "--scope", "W0", "--receipt", receipt,
                "--expected-receipt-sha", expected]
    code = 0
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        try:
            runpy.run_path(w1, run_name="__main__")
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 0
    print(json.dumps({"exit": code, "outside_receipt": str(outside),
                      "outside_opened": str(outside) in opens,
                      "outside_open_count": sum(1 for p in opens if p == str(outside)),
                      "opens_total": len(opens),
                      "consumer_stdout_tail": captured.getvalue()[-600:]},
                     ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())