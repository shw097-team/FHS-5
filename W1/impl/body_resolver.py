#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FHS-5_PLP W1 NF-r2 BodyResolver (W1 product DEV, D3).

Canonicalises an authorized pack root and contains every read inside it;
rejects absolute / drive / UNC / dot-segment / link / reparse paths,
duplicate JSON keys, invalid UTF-8 and NaN constants; enforces bounded
sizes; performs a stat/read/stat TOCTOU check; returns full clause text and
a Clause/Parent/Child/NEG/Exception view.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
from typing import Any

import w1_nf_reader as base

NFError = base.NFError
PathDenied = base.PathDenied

MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_FILES = 256
MAX_LINES = 100_000
FILE_ATTRIBUTE_REPARSE_POINT = 0x400

NEG_TOKEN_RE = re.compile(r"\b([A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]{2,})+)\b")
ID_CELL_RE = re.compile(r"`((?:DEV|OPS)-[A-Z]+-\d{2})`")
HEADING_RE = re.compile(r"^(#{2,6})\s+(.*\S)\s*$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_reparse(st: os.stat_result) -> bool:
    return bool(int(getattr(st, "st_file_attributes", 0)) & FILE_ATTRIBUTE_REPARSE_POINT)


def canonical_root(root: str | os.PathLike) -> Path:
    p = Path(root)
    if not p.exists():
        raise NFError("PACK_INCOMPLETE_LOCAL", f"root not found: {p}")
    rp = p.resolve(strict=True)
    st = os.stat(rp)
    if _is_reparse(st):
        raise PathDenied("root is a reparse point")
    if not stat.S_ISDIR(st.st_mode):
        raise NFError("OUTPUT_ROOT_INVALID", str(rp))
    return rp


def _split_rel(rel: str) -> list[str]:
    if not isinstance(rel, str) or not rel:
        raise PathDenied("BAD_RELATIVE_PATH")
    if "\x00" in rel:
        raise PathDenied("NUL_IN_PATH")
    if "\\" in rel:
        raise PathDenied("BACKSLASH_PATH")
    if rel.startswith("//"):
        raise PathDenied("UNC_PATH")
    if rel.startswith("/"):
        raise PathDenied("ABSOLUTE_PATH")
    if ":" in rel:
        raise PathDenied("DRIVE_PATH")
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise PathDenied("DOT_SEGMENT")
    if PurePosixPath(rel).is_absolute():
        raise PathDenied("ABSOLUTE_PATH")
    return parts


def resolve_inside(root: Path, rel: str, must_exist: bool = True) -> Path:
    parts = _split_rel(rel)
    cur = root
    for part in parts:
        nxt = cur / part
        if not nxt.exists():
            if must_exist:
                raise NFError("PACK_INCOMPLETE_LOCAL", rel)
            try:
                cur.resolve(strict=True).relative_to(root)
            except ValueError as exc:
                raise PathDenied(rel) from exc
            return nxt
        st = os.stat(nxt, follow_symlinks=False)
        if stat.S_ISLNK(st.st_mode) or _is_reparse(st):
            raise PathDenied(f"link/reparse at {part}")
        try:
            nxt.resolve(strict=True).relative_to(root)
        except ValueError as exc:
            raise PathDenied(rel) from exc
        cur = nxt
    return cur.resolve(strict=True)


def read_bounded(path: Path, rel: str) -> bytes:
    st1 = os.stat(path)
    if not stat.S_ISREG(st1.st_mode):
        raise PathDenied(f"not a regular file: {rel}")
    if _is_reparse(st1):
        raise PathDenied(f"reparse file: {rel}")
    if st1.st_size > MAX_FILE_BYTES:
        raise NFError("OVERSIZE_FILE", f"{rel}: {st1.st_size}")
    data = path.read_bytes()
    st2 = os.stat(path)
    if (st1.st_size, st1.st_mtime_ns, getattr(st1, "st_ino", 0)) != (
        st2.st_size,
        st2.st_mtime_ns,
        getattr(st2, "st_ino", 0),
    ):
        raise NFError("TOCTOU_DRIFT", rel)
    if len(data) != st2.st_size:
        raise NFError("TOCTOU_DRIFT", f"{rel}: short read")
    return data


def decode_utf8(data: bytes, rel: str) -> str:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise NFError("UTF8_INVALID", f"{rel}: {exc}") from exc
    if text.startswith("\ufeff"):
        text = text[1:]
    return text


def load_json_strict(path: Path, rel: str | None = None) -> tuple[Any, bytes]:
    name = rel or path.name
    data = read_bounded(path, name)
    text = decode_utf8(data, name)
    dups: list[str] = []

    def hook(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                dups.append(k)
            out[k] = v
        return out

    def bad(x):
        raise NFError("STRICT_JSON_REJECT", f"non-finite constant {x}")

    try:
        obj = json.loads(text, object_pairs_hook=hook, parse_constant=bad)
    except NFError:
        raise
    except Exception as exc:
        raise NFError("STRICT_JSON_REJECT", str(exc)) from exc
    if dups:
        raise NFError("STRICT_JSON_REJECT", f"duplicate keys {sorted(set(dups))}")
    return obj, data


def scan_pack(root: Path) -> dict:
    total_files = 0
    total_bytes = 0
    total_lines = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for name in sorted(filenames):
            fp = Path(dirpath) / name
            total_files += 1
            if total_files > MAX_FILES:
                raise NFError("TOO_MANY_FILES", str(total_files))
            total_bytes += os.stat(fp).st_size
            if fp.suffix.lower() in (".md", ".json", ".txt", ".py"):
                try:
                    total_lines += len(decode_utf8(read_bounded(fp, name), name).splitlines())
                except NFError as exc:
                    if exc.token != "UTF8_INVALID":
                        raise
            if total_lines > MAX_LINES:
                raise NFError("TOO_MANY_LINES", str(total_lines))
    return {"files": total_files, "bytes": total_bytes, "lines": total_lines,
            "limits": {"files": MAX_FILES, "bytes": MAX_FILE_BYTES, "lines": MAX_LINES}}


def _negatives(text: str) -> list[dict]:
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        if "→" not in line and "拒" not in line and "REJECT" not in line.upper():
            continue
        for t in dict.fromkeys(NEG_TOKEN_RE.findall(line)):
            if "_" in t and len(t) <= 48:
                out.append({"token": t, "line": i})
    return out


def _exceptions(text: str) -> list[dict]:
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        if "不適用" in line or "reasoned_na" in low or "exception" in low or "例外" in line:
            out.append({"kind": "EXCEPTION", "line": i, "text": line.strip()[:160]})
    return out


def parse_clauses(text: str, path: str, source_sha256: str) -> list[dict]:
    lines = text.splitlines()
    stack: list[tuple[int, dict]] = []
    clauses: list[dict] = []
    open_clause: dict | None = None
    buf: list[str] = []

    def flush(end_line: int) -> None:
        nonlocal open_clause, buf
        if open_clause is None:
            return
        body = "\n".join(buf).strip()
        open_clause["line_end"] = max(end_line, open_clause["line_start"])
        open_clause["text"] = body
        open_clause["text_sha256"] = sha256_bytes(body.encode("utf-8"))
        open_clause["is_heading_only"] = body == ""
        open_clause["negatives"] = _negatives(body)
        open_clause["exceptions"] = _exceptions(body)
        open_clause["ids"] = sorted(set(ID_CELL_RE.findall(body)))
        clauses.append(open_clause)
        open_clause, buf = None, []

    for idx, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if m:
            flush(idx - 1)
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            parent_id = stack[-1][1]["clause_id"] if stack else None
            cid = f"{path}#{m.group(2)}"
            node = {
                "clause_id": cid, "path": path, "heading": m.group(2), "level": level,
                "line_start": idx, "line_end": idx, "parent": parent_id, "children": [],
                "text": "", "text_sha256": "", "source_sha256": source_sha256,
                "is_heading_only": True, "negatives": [], "exceptions": [], "ids": [],
            }
            if stack:
                stack[-1][1]["children"].append(cid)
            stack.append((level, node))
            open_clause, buf = node, []
        elif open_clause is not None:
            buf.append(line)
    flush(len(lines))
    return clauses


def resolve_clause(root: str | os.PathLike, rel: str, heading: str) -> dict:
    r = canonical_root(root)
    p = resolve_inside(r, rel)
    data = read_bounded(p, rel)
    text = decode_utf8(data, rel)
    sha = sha256_bytes(data)
    lines = text.splitlines()
    for c in parse_clauses(text, rel, sha):
        if c["heading"] == heading or c["clause_id"].endswith("#" + heading):
            if c["is_heading_only"]:
                raise NFError("BODY_RESOLVER_UNBOUND", f"{rel}#{heading}")
            span = "\n".join(lines[c["line_start"] - 1:c["line_end"]])
            return {
                "schema": "FHS5.PLP.W1.ClauseResolve@1", "path": rel,
                "path_scope": "PACK_ROOT", "raw_sha256": sha,
                "line_start": c["line_start"], "line_end": c["line_end"],
                "line_sha256": sha256_bytes(span.encode("utf-8")),
                "full_text": c["text"], "is_excerpt": False, "clause": c,
            }
    raise NFError("CLAUSE_NOT_FOUND", f"{rel}#{heading}")


def resolve_body(root: str | os.PathLike, rel: str, start: int, end: int) -> dict:
    r = canonical_root(root)
    p = resolve_inside(r, rel)
    data = read_bounded(p, rel)
    text = decode_utf8(data, rel)
    lines = text.splitlines()
    if type(start) is not int or type(end) is not int or not (1 <= start <= end <= len(lines)):
        raise NFError("SPAN_OUT_OF_RANGE", f"{start}-{end}")
    if end - start + 1 > MAX_LINES:
        raise NFError("SPAN_TOO_LARGE", f"{start}-{end}")
    body = "\n".join(lines[start - 1:end])
    return {
        "schema": "FHS5.PLP.W1.BodyResolver@1", "path": rel, "path_scope": "PACK_ROOT",
        "resolved_path": str(p), "raw_sha256": sha256_bytes(data), "bytes": len(data),
        "line_start": start, "line_end": end,
        "line_sha256": sha256_bytes(body.encode("utf-8")), "full_text": body,
        "is_excerpt": False, "reader_state": "PINNED_BYTES",
    }


def main(argv=None) -> int:
    import argparse
    import sys

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("resolve")
    a.add_argument("--pack", required=True)
    a.add_argument("--path", required=True)
    a.add_argument("--start", type=int, required=True)
    a.add_argument("--end", type=int, required=True)
    b = sub.add_parser("clause")
    b.add_argument("--pack", required=True)
    b.add_argument("--path", required=True)
    b.add_argument("--heading", required=True)
    c = sub.add_parser("scan")
    c.add_argument("--pack", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "resolve":
            out = resolve_body(args.pack, args.path, args.start, args.end)
        elif args.cmd == "clause":
            out = resolve_clause(args.pack, args.path, args.heading)
        else:
            out = {"schema": "FHS5.PLP.W1.PackScan@1", **scan_pack(canonical_root(args.pack))}
    except NFError as exc:
        sys.stdout.write(json.dumps({"result": "REJECT", "token": exc.token,
                                     "detail": exc.detail}, ensure_ascii=False, indent=2) + "\n")
        return 2
    sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
