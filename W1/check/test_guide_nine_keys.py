#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guide tests: four functions, two modes, nine real keys."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import guide_nf as guide
import nf_reader as reader
import w1_nf_reader as base

PACK = Path(os.environ.get(
    "W1_PACK",
    r"C:/Users/user/Downloads/FHS-5/FHS-5_PLP_W0-W4_實作/W1/"
    r"W1_Native-first_CODEX_主用修補_交付/FHS-5_PLP_W1_NATIVE_FIRST"))


def ctx(tmp: Path, world: str = "1", first_fail="NONE"):
    return {
        "identity": {"subject_id": "FHS-5_PLP/W1/CONTROL_PACK", "scope": "W1-NF-01"},
        "pack_manifest_sha256": "61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a",
        "repo_head_file": str(tmp / "head.txt"),
        "host_id_file": str(tmp / "host.json"),
        "policy_file": str(tmp / "policy.json"),
        "oracle_file": str(tmp / "oracle.json"),
        "world_raw_file": str(tmp / ("world%s.json" % world)),
        "first_fail": first_fail,
    }


def seed(tmp: Path):
    (tmp / "head.txt").write_text("c2d8084ba24dd8df3fa62259bba496f4fb9caa85\n", encoding="utf-8")
    (tmp / "host.json").write_text('{"host_id": "codex-cli"}\n', encoding="utf-8")
    (tmp / "policy.json").write_text('{"policy_epoch": "PE-1"}\n', encoding="utf-8")
    (tmp / "oracle.json").write_text('{"o": 1}\n', encoding="utf-8")
    (tmp / "world1.json").write_text('{"w": 1}\n', encoding="utf-8")
    (tmp / "world2.json").write_text('{"w": 2}\n', encoding="utf-8")


class TestGuide(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="w1-guide-"))
        seed(self.tmp)

    def test_receive_package(self):
        r = guide.inspect_guide_request({}, str(PACK))
        self.assertEqual(r["package_state"], "RECEIVED_ACTUAL")
        self.assertEqual(r["next"], "P03")
        self.assertEqual(r["permission_state"], "NONE_GRANTED")

    def test_receive_neg_scope(self):
        with self.assertRaises(base.NFError) as cm:
            guide.inspect_guide_request({"scope": "W2-XYZ"}, str(PACK))
        self.assertEqual(cm.exception.token, "CONTEXT_SCOPE_MISMATCH")

    def test_advice_two_modes(self):
        for mode in guide.MODES:
            a = guide.select_bounded_advice(
                {"identity": {"scope": "W1-NF-01"}, "mode": mode,
                 "evidence": {"policy_epoch": "PE-1", "oracle_sha": "x" * 64}},
                {"requested_effect": "READ"})
            self.assertFalse(a["advice_is_grant"])
            self.assertEqual(a["permission_state"], "NONE_GRANTED")

    def test_advice_neg_effect(self):
        with self.assertRaises(base.NFError) as cm:
            guide.select_bounded_advice(
                {"identity": {"scope": "W1-NF-01"}, "mode": "PACKAGE_FIRST",
                 "evidence": {"a": 1}}, {"requested_effect": "RELEASE"})
        self.assertEqual(cm.exception.token, "EFFECT_UNBOUND")

    def test_thin_prompt(self):
        a = {"mode": "PACKAGE_FIRST", "advice": ["read"], "scope_echo": "W1-NF-01"}
        t = guide.render_thin_prompt({"identity": {"subject_id": "S", "scope": "W1-NF-01"}}, a)
        self.assertIn("permission_state: NONE_GRANTED", t["thin_prompt_utf8"])
        self.assertEqual(len(t["thin_prompt_sha256"]), 64)

    def test_nine_keys_all_produced(self):
        k = guide.produce_nine_keys(ctx(self.tmp))
        self.assertEqual(sorted(k), sorted(guide.NINE_KEYS))
        self.assertIsNotNone(k["repo_head"])
        self.assertEqual(k["first_fail"], "NONE")

    def test_delta_same_park(self):
        a = ctx(self.tmp)
        b = ctx(self.tmp)
        self.assertEqual(guide.reconcile_guide_delta(a, b)["state"], "PARK_NO_DELTA")

    def test_delta_changed(self):
        a = ctx(self.tmp, "1")
        b = ctx(self.tmp, "2")
        d = guide.reconcile_guide_delta(a, b)
        self.assertEqual(d["state"], "NEW_MATERIAL_EVIDENCE")
        self.assertIn("world_raw_sha", d["changed_keys"])

    def test_delta_neg_missing_period(self):
        self.assertEqual(guide.reconcile_guide_delta(ctx(self.tmp), {})["state"],
                         "DELTA_UNVERIFIED")

    def test_delta_neg_missing_key(self):
        a = ctx(self.tmp)
        b = ctx(self.tmp)
        b["policy_file"] = str(self.tmp / "absent.json")
        self.assertEqual(guide.reconcile_guide_delta(a, b)["state"], "DELTA_UNVERIFIED")

    def test_delta_neg_caller_bool(self):
        a = ctx(self.tmp)
        b = ctx(self.tmp)
        b["caller_verified"] = True
        self.assertEqual(guide.reconcile_guide_delta(a, b)["state"], "DELTA_UNVERIFIED")

    def test_delta_neg_cross_scope(self):
        a = ctx(self.tmp)
        b = ctx(self.tmp)
        b["identity"]["scope"] = "W2-XYZ"
        self.assertEqual(guide.reconcile_guide_delta(a, b)["state"],
                         "NEW_SUBJECT_REVIEW_REQUIRED")

    def test_delta_neg_single_sha_only(self):
        a = ctx(self.tmp)
        b = ctx(self.tmp)
        b = {"identity": a["identity"], "evidence_sha": "a" * 64}
        self.assertEqual(guide.reconcile_guide_delta(a, b)["state"], "DELTA_UNVERIFIED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
