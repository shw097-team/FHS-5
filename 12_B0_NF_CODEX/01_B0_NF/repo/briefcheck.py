#!/usr/bin/env python3
"""briefcheck B0 candidate v2: fail-closed duplicate/ambiguous handling."""
import argparse, hashlib, json, os, sys
from pathlib import Path

def emit(code, status, sha256=None, provided=None, missing=None):
    print(json.dumps({"source_sha256": sha256, "provided": provided or [], "missing": missing or [], "status": status},
                     ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return code

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--sha256", required=True)
    a = p.parse_args(argv)
    root = Path(a.root).resolve(strict=True)
    rel = a.input
    if not rel or os.path.isabs(rel) or rel.startswith("\\\\") or ":" in rel:
        return emit(3, "INVALID_PATH")
    if any(part == ".." for part in Path(rel).parts):
        return emit(3, "INVALID_PATH")
    try:
        target = (root / rel).resolve(strict=True)
    except OSError:
        return emit(3, "INVALID_PATH")
    try:
        if os.path.normcase(os.path.commonpath([str(root), str(target)])) != os.path.normcase(str(root)):
            return emit(3, "INVALID_PATH")
    except ValueError:
        return emit(3, "INVALID_PATH")
    if not target.is_file():
        return emit(3, "INVALID_PATH")
    data = target.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != a.sha256.lower():
        return emit(3, "SHA_MISMATCH", actual)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return emit(3, "INVALID_ENCODING", actual)
    checked = set(); seen = {"A": 0, "B": 0}; malformed = False
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if not s.startswith("- ["):
            continue
        if len(s) == 7 and s[0:3] == "- [" and s[3] in " xX" and s[4] == "]" and s[5] == " " and s[6] in "AB":
            seen[s[6]] += 1
            if s[3].lower() == "x":
                checked.add(s[6])
        else:
            malformed = True
    if malformed:
        return emit(3, "INVALID_FORMAT", actual, sorted(checked))
    if seen["A"] > 1:
        return emit(3, "INVALID_DUP", actual, sorted(checked))
    if seen["B"] > 1:
        return emit(3, "INVALID_FORMAT", actual, sorted(checked))
    missing = [x for x in ("A", "B") if x not in checked]
    if missing:
        return emit(2, "MISSING", actual, sorted(checked), missing)
    return emit(0, "COMPLETE", actual, sorted(checked), [])

if __name__ == "__main__":
    sys.exit(main())
