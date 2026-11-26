#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BodyResolver tests: containment, strict JSON, span, TOCTOU-linked guards."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import body_resolver as br

from packloc import resolve_pack

PACK = resolve_pack()


class TestBodyResolver(unittest.TestCase):
    def test_pos_span_digest(self):
        r = br.resolve_body(PACK, "03_W1_TQAEP.md", 30, 60)
        self.assertEqual(r["line_end"] - r["line_start"] + 1, 31)
        self.assertEqual(len(r["line_sha256"]), 64)
        self.assertFalse(r["is_excerpt"])

    def test_pos_clause_full_body(self):
        c = br.resolve_clause(PACK, "01_W1_DEV_ECP.md", "2｜38 個原 DEV ECP ID：逐原義 Native 承接")
        self.assertFalse(c["clause"]["is_heading_only"])
        self.assertGreater(len(c["full_text"]), 1000)

    def test_neg_absolute(self):
        with self.assertRaises(br.NFError) as cm:
            br.resolve_body(PACK, "C:/x.md", 1, 1)
        self.assertIn(cm.exception.token, ("PATH_OUTSIDE_ROOT", "ABSOLUTE_PATH"))

    def test_neg_dotdot(self):
        with self.assertRaises(br.NFError):
            br.resolve_body(PACK, "../05_W1_SOURCE_MANIFEST.json", 1, 1)

    def test_neg_unc(self):
        with self.assertRaises(br.NFError):
            br.resolve_body(PACK, "//server/share/x.md", 1, 1)

    def test_neg_backslash(self):
        with self.assertRaises(br.NFError):
            br.resolve_body(PACK, "a\\b.md", 1, 1)

    def test_neg_span(self):
        with self.assertRaises(br.NFError) as cm:
            br.resolve_body(PACK, "00_W1_PI_PD.md", 5, 2)
        self.assertEqual(cm.exception.token, "SPAN_OUT_OF_RANGE")

    def test_neg_dup_key(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "d.json"
            p.write_text('{"a":1,"a":2}', encoding="utf-8")
            with self.assertRaises(br.NFError) as cm:
                br.load_json_strict(p)
            self.assertEqual(cm.exception.token, "STRICT_JSON_REJECT")
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    def test_neg_nan(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "n.json"
            p.write_text('{"a":NaN}', encoding="utf-8")
            with self.assertRaises(br.NFError):
                br.load_json_strict(p)
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    def test_neg_bad_utf8(self):
        with self.assertRaises(br.NFError) as cm:
            br.decode_utf8(b"\xff\xfe", "x")
        self.assertEqual(cm.exception.token, "UTF8_INVALID")

    def test_neg_oversize(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "big.md"
            with open(p, "wb") as fh:
                fh.seek(br.MAX_FILE_BYTES + 4)
                fh.write(b"x")
            with self.assertRaises(br.NFError) as cm:
                br.read_bounded(p, "big.md")
            self.assertEqual(cm.exception.token, "OVERSIZE_FILE")
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    def test_scan_within_limits(self):
        s = br.scan_pack(PACK)
        self.assertLessEqual(s["files"], br.MAX_FILES)
        self.assertGreater(s["files"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
