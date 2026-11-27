#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Redact local account/machine identifiers before evidence is published."""
from __future__ import annotations

import json
import os
from pathlib import Path

HOME = str(Path.home())
USER = os.environ.get("USERNAME", "")
COMPUTER = os.environ.get("COMPUTERNAME", "")


def text(s: str) -> str:
    if HOME:
        s = s.replace(HOME, "<HOME>")
        s = s.replace(HOME.replace("\\", "\\\\"), "<HOME>")
    if USER:
        s = s.replace(USER, "<USER>")
    if COMPUTER:
        s = s.replace(COMPUTER, "<HOST>")
    return s


def obj(x):
    if isinstance(x, str):
        return text(x)
    if isinstance(x, list):
        return [obj(v) for v in x]
    if isinstance(x, dict):
        return {k: obj(v) for k, v in x.items()}
    return x


def file_json(p: Path):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return False
    p.write_text(json.dumps(obj(d), ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")
    return True
