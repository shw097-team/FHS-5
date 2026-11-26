#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TPM contract + reviewer tests: five views, one identity, read-only reviewer."""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import nf_reader as reader
import tpm_contracts_nf as tpm
import w1_nf_reader as base

from packloc import resolve_pack

PACK = resolve_pack()

WI = {"project_id": "FHS-5_PLP", "subject_id": "FHS-5_PLP/W1/CONTROL_PACK",
      "scope": "W1-NF-01", "wave_id": "W1", "batch_id": "W1-NF-01",
      "work_id": "W1-TEST"}


class TestTPM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = tpm.build_contracts(str(PACK), WI)

    def test_five_views_one_identity(self):
        self.assertEqual(set(self.c["views"]), {"PI", "PD", "DEV", "OPS", "TQAEP"})
        ids = {v["work_id"] for v in self.c["views"].values()}
        self.assertEqual(ids, {"W1-TEST"})

    def test_counts(self):
        self.assertEqual(self.c["views"]["DEV"]["count"], 38)
        self.assertEqual(self.c["views"]["OPS"]["count"], 29)
        self.assertEqual(self.c["views"]["TQAEP"]["count"], 13)

    def test_pi_pd_not_merged(self):
        self.assertIn("constraints", self.c["views"]["PI"])
        self.assertIn("typed_dag", self.c["views"]["PD"])

    def test_neg_work_identity_incomplete(self):
        with self.assertRaises(base.NFError) as cm:
            tpm.build_contracts(str(PACK), {"project_id": "FHS-5_PLP"})
        self.assertEqual(cm.exception.token, "WORK_IDENTITY_INCOMPLETE")

    def test_neg_identity_mismatch(self):
        bad = dict(WI, scope="W9-OTHER")
        with self.assertRaises(base.NFError) as cm:
            tpm.build_contracts(str(PACK), bad)
        self.assertEqual(cm.exception.token, "IDENTITY_MISMATCH")

    def test_reviewer_readonly(self):
        r = tpm.review(self.c, str(PACK))
        self.assertEqual(r["wrote_bytes"], 0)
        self.assertEqual(r["finding_count"], 0)
        self.assertGreater(r["checks"], 10)
        for f in r["findings"]:
            self.assertEqual(set(f), {"id", "severity", "class", "subject_sha",
                                      "command", "exit", "raw_sha256", "reproduction"})

    def test_reviewer_detects_subject_mutation(self):
        bad = dict(self.c)
        r = tpm.review(bad, str(PACK), expected_subject_sha={"00_W1_PI_PD.md": "0" * 64})
        self.assertEqual(r["findings"][0]["class"], "subject_mutation_denied")
        self.assertEqual(r["findings"][0]["severity"], "critical")

    def test_reviewer_detects_missing_binding(self):
        broken = {"views": {"PD": {}}}
        r = tpm.review(broken, str(PACK))
        self.assertTrue(any(f["class"] in ("missing_binding", "contract_missing_field")
                            for f in r["findings"]))
        self.assertTrue(r["change_cone"])
        self.assertIsNotNone(r["first_fail"])

    def test_assets_pin_join(self):
        cases = self.c["views"]["TQAEP"]["cases"]
        insp = reader.inspect_package(PACK)
        amap = {(a["case_id"], a["kind"]): a["sha256"] for a in insp["asset_refs"]}
        for c in cases:
            self.assertEqual(c["oracle_sha256"], amap[(c["case_id"], "oracle")])
            self.assertEqual(c["fixture_sha256"], amap[(c["case_id"], "fixture")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
