#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Source integrity gate: compare a real file digest to an expected pin.
Exit 0 READ_OK, 3 SOURCE_INTEGRITY_FAILED."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path", required=True)
    p.add_argument("--expected", required=True)
    a = p.parse_args()
    path = Path(a.path)
    if not path.is_file():
        print(json.dumps({"status": "SOURCE_UNREACHABLE", "path": str(path)}, ensure_ascii=False))
        return 3
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    ok = actual == a.expected.lower()
    print(json.dumps({
        "status": "READ_OK" if ok else "SOURCE_INTEGRITY_FAILED",
        "expected": a.expected.lower(), "actual": actual, "bytes": len(data),
        "lines": len(data.decode("utf-8", "replace").splitlines()),
        "reject_old_trace": not ok,
    }, ensure_ascii=False, sort_keys=True))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
