#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the real 13+3 contract table from 00_W2_PI_PD.md §4.1.

The 16 rows are W2-B01..B13 plus W2-NF-A/B/C — not 16 U-xxx identifiers.
"""
from __future__ import annotations

import re

ROW_ID = re.compile(r"^(W2-B\d{2}|W2-NF-[ABC])$")
EXPECTED = [f"W2-B{i:02d}" for i in range(1, 14)] + ["W2-NF-A", "W2-NF-B", "W2-NF-C"]


def _cells(line: str):
    return [c.strip().strip("`").strip().replace("`","") for c in line.strip().strip("|").split("|")]


def _split_head(cell: str):
    parts = [p.strip() for p in cell.split("；")]
    while len(parts) < 4:
        parts.append("")
    return {"original": parts[0], "fields": parts[1], "type": parts[2],
            "owner": "；".join(parts[3:])}


def parse_13_plus_3(text: str) -> dict:
    """Return {rows, missing, extra, by_id} with typed fields per row."""
    rows, seen = [], []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        c = _cells(line)
        if len(c) < 12 or not ROW_ID.match(c[0]):
            continue
        if c[0] in seen:
            raise ValueError("DUPLICATE_ROW:" + c[0])
        head = _split_head(c[1])
        rows.append({
            "id": c[0],
            "original": head["original"],
            "fields": head["fields"],
            "type": head["type"],
            "owner": head["owner"],
            "original_state": c[2],
            "native_equivalent": c[3],
            "applicable_op": c[4],
            "producer": c[5],
            "consumer": c[6],
            "required_when": c[7],
            "expected_receipt": c[8],
            "actual_ref": (None if c[9].strip().lower() in ("null", "") else c[9]),
            "first_fail": c[10],
            "resume": c[11],
        })
        seen.append(c[0])
    missing = [i for i in EXPECTED if i not in seen]
    extra = [i for i in seen if i not in EXPECTED]
    # NF-OWNER-FILL: the NF rows carry the role in the original column, not
    # a four-part header; fill from the table's own Producer/Consumer text.
    for r in rows:
        if r["id"] == "W2-NF-A":
            r["owner"] = "Case Owner"
        elif r["id"] == "W2-NF-B":
            r["owner"] = "Host/Receiver Owner"
        elif r["id"] == "W2-NF-C":
            r["owner"] = "Host/OS Reader"
    return {"rows": rows, "count": len(rows), "missing": missing, "extra": extra,
            "by_id": {r["id"]: r for r in rows}}
