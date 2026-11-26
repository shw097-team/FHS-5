#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 contract tests: real DAG, runners, duplicates, missing case."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "impl"))

import contracts_s1 as C  # noqa: E402
import req_parse  # noqa: E402
import w2_nf_reader as R  # noqa: E402

WT = HERE.parents[1]
PACK = WT / "S1_PACKS" / "FHS-5_PLP_W2_NATIVE_FIRST"


@unittest.skipUnless(PACK.is_dir(), "S1 pack not present")
class S1Contracts(unittest.TestCase):
    def test_pos_real_dag_and_runners(self):
        c = R.build_contracts(PACK)
        self.assertTrue(c["ok"], c["problems"])
        v = c["views"]
        self.assertEqual(v["PD"]["edge_count"], 9)
        self.assertIsNone(v["PD"]["cycle"])
        self.assertEqual(v["PD"]["dag_problems"], [])
        self.assertEqual(v["PD"]["wp"][0].split()[0], "WM2-P01")
        self.assertEqual(len(v["PD"]["holds"]), 14)
        self.assertEqual(v["PD"]["crs"], 37)
        self.assertTrue(all(x["runner"] for x in v["TQAEP"]["cases"]))
        self.assertEqual(len(v["TQAEP"]["cases"]), 12)
        self.assertEqual(len(v["PI"]["requirements"]), 16)
        self.assertEqual(v["DEV"]["locators"]["DEV-D01"]["line"], 124)

    def test_neg_broken_dag_row_rejected(self):
        tmp = Path(tempfile.mkdtemp(prefix="s1dag_"))
        try:
            d = tmp / "p"
            shutil.copytree(PACK, d)
            f = d / "00_W2_PI_PD.md"
            t = f.read_text(encoding="utf-8")
            t = t.replace("| P01 → P02 | HARD |", "| P01 → | HARD |", 1)
            f.write_text(t, encoding="utf-8", newline="\n")
            edges, problems = C.parse_dag(t)
            self.assertTrue(any(p.startswith("EMPTY_ENDPOINT") for p in problems),
                            problems)
            # the pack is rejected at the earliest verifiable layer (seal),
            # and the DAG parser itself already returns a typed problem
            with self.assertRaises(Exception):
                R.build_contracts(d)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_neg_duplicate_requirement_row(self):
        tmp = Path(tempfile.mkdtemp(prefix="s1dup_"))
        try:
            d = tmp / "p"
            shutil.copytree(PACK, d)
            f = d / "00_W2_PI_PD.md"
            t = f.read_text(encoding="utf-8")
            line = next(l for l in t.splitlines() if l.startswith("| W2-B01 |"))
            t = t.replace(line, line + "\n" + line, 1)
            f.write_text(t, encoding="utf-8", newline="\n")
            with self.assertRaises(ValueError) as ctx:
                req_parse.parse_13_plus_3(t)
            self.assertIn("DUPLICATE_ROW", str(ctx.exception))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_neg_missing_case_block(self):
        tmp = Path(tempfile.mkdtemp(prefix="s1case_"))
        try:
            d = tmp / "p"
            shutil.copytree(PACK, d)
            f = d / "03_W2_TQAEP.md"
            t = f.read_text(encoding="utf-8")
            i = t.index("### 1.12")
            j = t.find("### ", i + 10)
            t = t[:i] + (t[j:] if j != -1 else "")
            f.write_text(t, encoding="utf-8", newline="\n")
            with self.assertRaises(Exception):
                R.build_contracts(d)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
