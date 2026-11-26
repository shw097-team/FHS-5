#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stdlib contract tests for the W3 slice (POS and NEG)."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "impl"))

import w3_far
import w3_guide2
from w3_advice import validate_alternatives
from w3_common import (ADVICE, W3Error, load_json_strict, resolve_inside,
                       sha256_file, write_json)
from w3_intake import verify_pack
from w3_repair import guard_write


class TestStrictJson(unittest.TestCase):
    def test_duplicate_key_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.json")
            open(p, "w", encoding="utf-8").write('{"a": 1, "a": 2}')
            with self.assertRaises(W3Error) as cm:
                load_json_strict(p)
            self.assertEqual(cm.exception.token, "DUPLICATE_KEY")


class TestPathContainment(unittest.TestCase):
    def test_dotdot_refused(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(W3Error) as cm:
                resolve_inside(d, "../outside.txt")
            self.assertEqual(cm.exception.token, "INVALID_PATH")

    def test_absolute_refused(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(W3Error):
                resolve_inside(d, "C:/Windows/system32")

    def test_inside_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            p = resolve_inside(d, "sub/x.txt")
            self.assertTrue(os.path.abspath(p).startswith(os.path.abspath(d)))

    def test_protected_write_refused(self):
        with tempfile.TemporaryDirectory() as d:
            for rel in ("W1/check/test_j1_strict.py", "oracle.json",
                        "threshold.json", "subject/00.md"):
                with self.assertRaises(W3Error) as cm:
                    guard_write(rel, d)
                self.assertEqual(cm.exception.token, "WRITE_SCOPE_VIOLATION")


class TestFarStates(unittest.TestCase):
    def test_all_five_states(self):
        with tempfile.TemporaryDirectory() as d:
            hit = os.path.join(d, "hit")
            zero = os.path.join(d, "zero")
            absent = os.path.join(d, "absent")
            os.makedirs(hit)
            os.makedirs(zero)
            open(os.path.join(hit, "TOKEN_refusal.txt"), "w").write("x")
            open(os.path.join(zero, "a.txt"), "w").write("x")
            allowed = [d]
            states = [
                w3_far.query_dir("h", hit, "TOKEN", allowed)["state"],
                w3_far.query_dir("z", zero, "NOPE", allowed)["state"],
                w3_far.query_dir("u", absent, "x", allowed)["state"],
                w3_far.query_dir("b", os.path.dirname(d), "x", allowed)["state"],
                w3_far.query_dir("e", hit, "[", allowed)["state"],
            ]
            self.assertEqual(set(states), set(w3_far.FAR_STATES))
            u = w3_far.query_dir("u", absent, "x", allowed)
            self.assertIsNone(u["rows"])
            self.assertIsNone(u["zero_results"])

    def test_injected_zero_not_hit(self):
        r = w3_far.validate_injected_claim({"state": "HIT", "zero_results": 0})
        self.assertEqual(r["token"], "RESEARCH_REQUIRED")
        self.assertFalse(r["accepted"])


class TestAdvice(unittest.TestCase):
    def test_ten_original_names(self):
        self.assertEqual(len(ADVICE), 10)
        self.assertEqual(len(set(ADVICE)), 10)

    def test_single_alternative_refused(self):
        r = validate_alternatives([{"id": "A", "type": "FIX_NOW", "fit": "x", "nofit": "y"}])
        self.assertFalse(r["ok"])
        self.assertEqual(r["token"], "ALTERNATIVE_INSUFFICIENT")

    def test_two_alternatives_pass(self):
        r = validate_alternatives([
            {"id": "A", "type": "FIX_NOW", "fit": "x", "nofit": "y"},
            {"id": "B", "type": "BIND_EXISTING", "fit": "p", "nofit": "q"},
        ])
        self.assertTrue(r["ok"])
        self.assertEqual(r["token"], "ALTERNATIVES_SUBSTANTIVE")


def _period(d, name, value, observed_at):
    os.makedirs(d, exist_ok=True)
    receipts = {"subject": {}, "scope": {}}
    seven = {
        "source_sha": value, "repo_head": "a" * 40, "host_id": "H",
        "policy_epoch": "P", "oracle_sha": "b" * 64,
        "world_raw_sha": value, "first_fail": "NONE",
    }
    for k, v in seven.items():
        p = os.path.join(d, k + ".txt")
        open(p, "w", encoding="utf-8").write(json.dumps(
            {"period": name, "k": k, "v": v, "t": observed_at}))
        receipts[k] = {"ref": p, "sha256": sha256_file(p)}
    return {"period": name, "identity": {"subject": "S", "scope": "W3-NF-01"},
            "seven": seven, "receipts": receipts, "observed_at": observed_at}


class TestGuide2(unittest.TestCase):
    def test_missing_period(self):
        self.assertEqual(w3_guide2.reconcile([])["state"], "DELTA_UNVERIFIED")

    def test_caller_boolean(self):
        p = {"caller_verified": True}
        self.assertEqual(
            w3_guide2.reconcile([p, p], verifier_receipt={"verified": True})["state"],
            "DELTA_UNVERIFIED")

    def test_single_sha(self):
        self.assertEqual(
            w3_guide2.reconcile([], verifier_receipt={"verified": True},
                                declared_single_sha="d" * 64)["state"],
            "DELTA_UNVERIFIED")

    def test_two_period_no_delta_and_new_delta(self):
        with tempfile.TemporaryDirectory() as d:
            p1 = _period(os.path.join(d, "p1"), "P1", "c" * 64, "2026-11-26T10:00:00")
            p2 = _period(os.path.join(d, "p2"), "P2", "c" * 64, "2026-11-26T10:00:05")
            n = w3_guide2.reconcile([p1, p2], verifier_receipt={"verified": True})
            self.assertEqual(n["state"], "PARK_NO_DELTA")
            p3 = _period(os.path.join(d, "p3"), "P3", "d" * 64, "2026-11-26T10:00:09")
            m = w3_guide2.reconcile([p1, p3], verifier_receipt={"verified": True})
            self.assertEqual(m["state"], "NEW_MATERIAL_EVIDENCE")
            self.assertIn("world_raw_sha", m["changed_keys"])

    def test_copied_receipt_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p1 = _period(os.path.join(d, "p1"), "P1", "c" * 64, "2026-11-26T10:00:00")
            p2 = dict(p1)
            p2["observed_at"] = "2026-11-26T10:00:05"
            r = w3_guide2.reconcile([p1, p2], verifier_receipt={"verified": True})
            self.assertEqual(r["state"], "DELTA_UNVERIFIED")
            self.assertEqual(r["reason"], "copied receipt")


class TestPack(unittest.TestCase):
    def test_sixteen_cases_not_run(self):
        pack = os.environ.get("W3_PACK")
        if not pack:
            self.skipTest("W3_PACK not set")
        man = load_json_strict(os.path.join(pack, "05_W3_SOURCE_MANIFEST.json"))
        self.assertEqual(len(man["case_refs"]), 16)
        self.assertEqual(len({c["case_id"] for c in man["case_refs"]}), 16)
        for c in man["case_refs"]:
            self.assertIsNone(c["observed"])
            self.assertEqual(c["verdict"], "NOT_RUN")

    def test_pack_seal(self):
        pack = os.environ.get("W3_PACK")
        ext = os.environ.get("W3_EXT")
        if not (pack and ext):
            self.skipTest("W3_PACK/W3_EXT not set")
        v = verify_pack(pack, os.path.join(ext, "EXTERNAL_SEAL.json"),
                        os.path.join(ext, "W3_OWNER_ADOPTION.json"),
                        os.path.join(ext, "W3_CURRENT.json"))
        self.assertTrue(v["ok"], v["issues"])


if __name__ == "__main__":
    unittest.main()
