#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S1 W2 contract extraction: WP, DAG, HOLD, cases, subcases, ops.

Everything comes from the adopted pack body.  Nothing is invented: a section
that is absent yields an explicit status instead of a synthetic row.
"""
from __future__ import annotations

import re

WP_ID = re.compile(r"^\|\s*(WM2-P\d{2})")
CASE_HEAD = re.compile(r"^### 1\.(\d+) (W2-[A-Z0-9-]+)（([A-Z]+)）")
KV = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$")
OPS_ID = re.compile(r"\b(OPS-O0[1-6])\b|\bO0([1-6])\b")


def _cells(line):
    return [c.strip().strip("`").replace("`", "") for c in line.strip().strip("|").split("|")]


def parse_wp(text):
    rows = []
    for line in text.splitlines():
        if not WP_ID.match(line):
            continue
        c = _cells(line)
        if len(c) < 9:
            continue
        rows.append({"id": c[0], "owner": c[1], "input": c[2], "operation": c[3],
                     "output": c[4], "consumer": c[5], "acc": c[6],
                     "neg_first_fail": c[7], "next_resume": c[8]})
    return rows


NODE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
KINDS = {"HARD", "SOFT", "POST", "AUTHOR_DOC_ORDER", "UNVERIFIED"}


def parse_dag(text):
    """Parse only the 5.2 DAG section; empty/invalid rows are rejected."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("### 5.2")), None)
    if start is None:
        return [], ["DAG_SECTION_MISSING"]
    edges, problems, seen = [], [], set()
    for line in lines[start + 1:]:
        if line.startswith("### ") or line.startswith("## ") or line.startswith("**圖性質"):
            break
        if not line.startswith("|") or "→" not in line:
            continue
        c = _cells(line)
        if len(c) < 2:
            continue
        if c[0].strip().lower().startswith("from"):
            continue
        a, _, b = c[0].partition("→")
        a, b = a.strip(), b.strip()
        if not a or not b:
            problems.append("EMPTY_ENDPOINT:" + c[0][:40])
            continue
        if not NODE.match(a) or not NODE.match(b):
            problems.append("NON_NODE:" + c[0][:40])
            continue
        kind = c[1].strip().upper()
        if kind not in KINDS:
            problems.append("UNKNOWN_KIND:" + kind)
            continue
        key = (a, b, kind)
        if key in seen:
            problems.append("DUPLICATE:" + f"{a}->{b}")
            continue
        seen.add(key)
        edges.append({"from": a, "to": b, "kind": kind,
                      "origin": c[2] if len(c) > 2 else "",
                      "reason": c[3] if len(c) > 3 else "",
                      "if_absent": c[4] if len(c) > 4 else ""})
    return edges, problems


def dag_cycle(edges):
    adj = {}
    for e in edges:
        adj.setdefault(e["from"], []).append(e["to"])
    state, path = {}, []

    def dfs(n):
        state[n] = 1
        path.append(n)
        for m in adj.get(n, []):
            if state.get(m) == 1:
                return path[path.index(m):] + [m]
            if state.get(m) is None:
                cyc = dfs(m)
                if cyc:
                    return cyc
        path.pop()
        state[n] = 2
        return None

    for n in list(adj):
        if state.get(n) is None:
            cyc = dfs(n)
            if cyc:
                return cyc
    return None


def parse_holds(text):
    holds, in_sec = [], False
    for line in text.splitlines():
        if line.startswith("### 8.1"):
            in_sec = True
            continue
        if in_sec and line.startswith("### 8.2"):
            break
        if in_sec and line.startswith("|"):
            c = _cells(line)
            if len(c) >= 3 and c[0] not in ("原 HOLD",) and "---" not in c[0]:
                holds.append({"id": c[0], "disposition": c[1], "scope": c[2]})
    return holds


def parse_cases(tqaep):
    """Parse 03 §1.N blocks: id, kind, and the key/value table."""
    cases, cur = [], None
    for line in tqaep.splitlines():
        m = CASE_HEAD.match(line)
        if m:
            if cur:
                cases.append(cur)
            cur = {"n": int(m.group(1)), "id": m.group(2), "kind": m.group(3),
                   "fields": {}}
            continue
        if cur is not None:
            if line.startswith("### 1.") and not CASE_HEAD.match(line):
                continue
            if line.startswith("## ") or line.startswith("### 2"):
                cases.append(cur)
                cur = None
                continue
            kv = KV.match(line)
            if kv and kv.group(1) not in ("欄",):
                cur["fields"][kv.group(1)] = kv.group(2)
    if cur:
        cases.append(cur)
    for c in cases:
        f = c["fields"]
        c["fixture_ref"] = f.get("fixture", "")
        c["oracle_ref"] = f.get("oracle", "")
        c["runner"] = f.get("runner", "")
        c["predicates"] = f.get("expected predicates", "")
        c["requirement_refs"] = f.get("requirement_refs", "")
        c["child"] = f.get("child", "")
    return cases


def parse_jn(tqaep):
    """Return J1..J3 sub-group ids and N01..N12 ids actually named."""
    j = {f"J{i}": sorted(set(re.findall(rf"J{i}-T0[1-6]", tqaep))) for i in (1, 2, 3)}
    n = sorted(set(re.findall(r"\bN\d{2}\b", tqaep)))
    return j, n


def parse_ops(ops_text):
    """O01..O06 sections from 02_W2_OPS_ECP.md."""
    out = []
    for m in re.finditer(r"^## (\d+)｜(O0[1-6])[^\n]*$", ops_text, re.M):
        start = m.end()
        nxt = ops_text.find("\n## ", start)
        body = ops_text[start: nxt if nxt != -1 else len(ops_text)]
        rows = {}
        for line in body.splitlines():
            kv = KV.match(line)
            if kv:
                rows[kv.group(1)] = kv.group(2)
        out.append({"id": m.group(2), "section": m.group(1),
                    "identity": rows.get("identity", ""),
                    "authority": rows.get("authority", ""),
                    "procedure": rows.get("procedure", ""),
                    "expected": rows.get("expected", ""),
                    "readback": rows.get("readback", ""),
                    "compensation": rows.get("compensation", ""),
                    "unknown": rows.get("unknown", "")})
    return out

def parse_runner_table(tqaep):
    """03 §4 table: case | fixture | oracle | runner | ..."""
    rows, in_sec = {}, False
    for line in tqaep.splitlines():
        if line.startswith("## 4"):
            in_sec = True
            continue
        if in_sec and (line.startswith("## 5") or line.startswith("## 6")):
            break
        if in_sec and line.startswith("|"):
            c = _cells(line)
            if len(c) >= 4 and c[0].startswith("W2-"):
                rows[c[0]] = {"fixture": c[1], "oracle": c[2], "runner": c[3],
                              "runner_status": c[4] if len(c) > 4 else "",
                              "source": "03_W2_TQAEP.md#4"}
    return rows


def parse_dev_locators(dev_text):
    """Real section locator per DEV-D0x (line numbers from the adopted body)."""
    out = {}
    for i, line in enumerate(dev_text.splitlines(), 1):
        m = re.match(r"^##+ (\d+\S*)?.*?(DEV-D\d{2})\b", line)
        if m:
            out[m.group(2)] = {"line": i, "title": line.strip()[:120],
                               "source": "01_W2_DEV_ECP.md"}
    return out


def parse_entry_sections(entry_text):
    return [l.strip("# ").strip() for l in entry_text.splitlines() if l.startswith("## ")]
