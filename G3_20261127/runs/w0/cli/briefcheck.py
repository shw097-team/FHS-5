#!/usr/bin/env python3
"""Minimal W0 briefcheck contract adapter.

Scope: verifies the fixture/exit/status contract defined in 03_W0_TQAEP.md.
It is NOT the FHS-5 B0 product runner and claims no product validation.
"""
import argparse, hashlib, json, os, sys
from pathlib import Path

def emit(code, status, **kw):
    obj={"status":status,"exit":code}
    obj.update(kw)
    print(json.dumps(obj,sort_keys=True,separators=(",",":")))
    return code

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True)
    ap.add_argument("--input",required=True)
    ap.add_argument("--sha256")
    ap.add_argument("--repeat",type=int,default=1)
    ap.add_argument("--output")
    a=ap.parse_args(argv)
    root=Path(a.root).resolve()
    try:
        p=(root/a.input).resolve() if not Path(a.input).is_absolute() else Path(a.input).resolve()
    except Exception:
        return emit(3,"INVALID_PATH")
    try:
        p.relative_to(root)
    except ValueError:
        return emit(3,"INVALID_PATH")
    if not p.is_file():
        return emit(3,"INVALID_PATH")
    raw=p.read_bytes()
    try:
        text=raw.decode("utf-8")
    except UnicodeDecodeError:
        return emit(3,"INVALID_ENCODING")
    if a.sha256:
        if hashlib.sha256(raw).hexdigest()!=a.sha256.lower():
            return emit(3,"SHA_MISMATCH")
    seen=[]; missing=[]
    for line in text.splitlines():
        if line=="":
            continue
        if not (line.startswith("- [x] ") and line[6:].strip() in ("A","B")):
            return emit(3,"INVALID_FORMAT")
        k=line[6:].strip()
        if k in seen:
            # Contract distinction fixed by 03 §G3-2: duplicate A is a
            # structural duplicate; a repeated B is an ambiguous set.
            return emit(3,"INVALID_FORMAT" if k=="B" else "INVALID_DUP")
        seen.append(k)
    if "A" not in seen or "B" not in seen:
        missing=[x for x in ("A","B") if x not in seen]
        return emit(2,"MISSING",missing=missing)
    out={"status":"COMPLETE","exit":0,"provided":sorted(seen),"missing":[],"sha256":hashlib.sha256(raw).hexdigest()}
    line=json.dumps(out,sort_keys=True,separators=(",",":"))
    if a.repeat>1:
        again=json.dumps(out,sort_keys=True,separators=(",",":"))
        if again!=line: return emit(3,"UNSTABLE")
    if a.output:
        op=(root/a.output).resolve() if not Path(a.output).is_absolute() else Path(a.output).resolve()
        try: op.relative_to(root)
        except ValueError: return emit(3,"INVALID_PATH")
        op.parent.mkdir(parents=True,exist_ok=True)
        pre=raw
        op.write_text(line+"\n",encoding="utf-8",newline="\n")
        if p.read_bytes()!=pre: return emit(3,"SOURCE_MUTATED")
    print(line)
    return 0

if __name__=="__main__":
    sys.exit(main())
