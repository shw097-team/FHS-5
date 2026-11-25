#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Negative control for the case runner verdict logic (F3.1).

A NEG case that does not raise must NOT be a PASS, and a POS case that returns
nothing must NOT be a PASS.  This test drives the real emit() with a synthetic
case body, so the guarantee lives in the runner, not in a comment.
"""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "impl"))
sys.path.insert(0, str(HERE))

import run_cases_nf as runner

PACK = Path(os.environ.get(
    "W1_PACK",
    r"C:/Users/user/Downloads/FHS-5/FHS-5_PLP_W0-W4_實作/W1/"
    r"W1_Native-first_CODEX_主用修補_交付/FHS-5_PLP_W1_NATIVE_FIRST"))


class TestRunnerVerdict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="w1-verdict-"))
        cls.ctx = runner.Ctx(str(PACK), str(cls.tmp))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_neg_without_rejection_is_fail(self):
        rec = self.ctx.emit("META-NEG", "NEG", "self-check",
                            {"expect_token": "SOME_TOKEN"},
                            lambda: {"no_raise": True})
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["first_fail"], "NEG_NOT_REJECTED")

    def test_neg_with_expected_token_is_pass(self):
        def body():
            raise runner.NFError("SOME_TOKEN", "raised as expected")
        rec = self.ctx.emit("META-NEG2", "NEG", "self-check",
                            {"expect_token": "SOME_TOKEN"}, body)
        self.assertEqual(rec["verdict"], "PASS")

    def test_neg_with_wrong_token_is_fail(self):
        def body():
            raise runner.NFError("OTHER_TOKEN", "wrong")
        rec = self.ctx.emit("META-NEG3", "NEG", "self-check",
                            {"expect_token": "SOME_TOKEN"}, body)
        self.assertEqual(rec["verdict"], "FAIL")

    def test_pos_empty_observation_is_fail(self):
        rec = self.ctx.emit("META-POS", "POS", "self-check", {"real": True},
                            lambda: {})
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["first_fail"], "POS_EMPTY_OBSERVATION")

    def test_exit0_without_consumed_is_not_pass(self):
        rec = self.ctx.emit("W1-HOST-01", "POS", "self-check", {"real": True},
                            lambda: {"host_consumed": False, "exit": 0})
        self.assertEqual(rec["verdict"], "NOT_OBSERVED")
        self.assertEqual(rec["first_fail"], "HOST_PENDING")


if __name__ == "__main__":
    unittest.main(verbosity=2)
