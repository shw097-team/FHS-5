#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consumer + host facade tests: real parse/use, anti-upgrade, no cross-host."""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import host_facade as hf
import nf_reader as reader
import w1_consumer as consumer
import w1_nf_reader as base

from packloc import resolve_pack

PACK = resolve_pack()
SHA = "61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a"


class TestConsumer(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="w1-cons-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_consume_real(self):
        r = consumer.consume(str(PACK), "case-checklist", "W1-API-01", SHA, str(self.tmp))
        self.assertTrue(r["readback_verified"])
        self.assertTrue(r["parsed_not_hashed_only"])
        self.assertEqual(r["scope_echo"], "W1-NF-01")
        self.assertTrue(Path(r["readback_path"]).is_file())

    def test_consume_neg_wrong_pin(self):
        with self.assertRaises(base.NFError) as cm:
            consumer.consume(str(PACK), "case-checklist", "W1-API-01", "0" * 64, str(self.tmp))
        self.assertEqual(cm.exception.token, "SOURCE_INTEGRITY_FAILED")

    def test_consume_neg_unknown_case(self):
        with self.assertRaises(base.NFError):
            consumer.consume(str(PACK), "case-checklist", "W1-NOPE-99", SHA, str(self.tmp))


class TestHostFacade(unittest.TestCase):
    def test_stages_in_order(self):
        led = hf.ledger()
        hf.record(led, "CODEX", "Selected", {"host_id": "codex", "version": "1"})
        hf.record(led, "CODEX", "Loaded", {"slots": ["e"], "loaded_sha256": "a" * 64})
        self.assertEqual(led["rows"]["CODEX"]["Loaded"], "OBSERVED_LOCAL")

    def test_neg_skill_as_loaded(self):
        led = hf.ledger()
        hf.record(led, "CODEX", "Selected", {"host_id": "codex", "version": "1"})
        with self.assertRaises(hf.StageDenied) as cm:
            hf.record(led, "CODEX", "Loaded",
                      {"slots": ["s"], "loaded_sha256": "a" * 64, "evidence_kind": "skill_bytes"})
        self.assertEqual(cm.exception.token, "HOST_PENDING")

    def test_neg_exit0_as_served(self):
        with self.assertRaises(hf.StageDenied) as cm:
            hf.record(hf.ledger(), "CODEX", "ActualServed",
                      {"served_bytes_sha256": "x", "scope_echo": "s", "served_at": "t",
                       "evidence_kind": "exit0"})
        self.assertEqual(cm.exception.token, "SERVED_UNVERIFIED")

    def test_neg_skip_stage(self):
        with self.assertRaises(hf.StageDenied) as cm:
            hf.record(hf.ledger(), "CODEX", "Consumed",
                      {"consumer_id": "c", "consumed_sha256": "x", "action": "a",
                       "readback_at": "t"})
        self.assertEqual(cm.exception.token, "HOST_ABI_DRIFT")

    def test_neg_cross_host_substitution(self):
        led = hf.ledger()
        hf.record(led, "CODEX", "Selected", {"host_id": "codex", "version": "1"})
        with self.assertRaises(hf.StageDenied):
            hf.cross_host_claim(led, "HERMES", "Selected")
        r = hf.cross_host_claim(led, "CODEX", "Selected")
        self.assertEqual(r["substitutes"]["HERMES"], "NOT_OBSERVED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
