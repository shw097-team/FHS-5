#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader tests: real pack POS + structural NEG."""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import body_resolver as br
import nf_reader as reader
import w1_nf_reader as base

PACK = Path(os.environ.get(
    "W1_PACK",
    r"C:/Users/user/Downloads/FHS-5/FHS-5_PLP_W0-W4_實作/W1/"
    r"W1_Native-first_CODEX_主用修補_交付/FHS-5_PLP_W1_NATIVE_FIRST"))


class TestReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.insp = reader.inspect_package(PACK)

    def test_counts(self):
        self.assertEqual(self.insp["counts"],
                         {"pack_files": 5, "dev": 38, "ops": 29, "cases": 13,
                          "assets": 26, "sources": 42, "holds": 14})

    def test_manifest_sha_matches_upstream_pin(self):
        self.assertEqual(self.insp["pack_manifest_sha256"],
                         "61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a")

    def test_digest_domains_distinct(self):
        d = self.insp["digest_domains"]
        self.assertNotEqual(d["pack_manifest_sha256"], d["package_tree_sha256"])
        self.assertEqual(d["source_set_sha256"], self.insp["source_set_sha256"])
        self.assertIsNone(d["context_sha256"])

    def test_clause_index_has_negatives(self):
        self.assertGreater(self.insp["clause_index"]["clause_count"], 40)
        self.assertGreater(self.insp["clause_index"]["negative_markers"], 10)

    def test_abi_state_complete(self):
        self.assertEqual(self.insp["abi_crosswalk"]["state"], "COMPLETE")
        self.assertEqual(self.insp["abi_crosswalk"]["legacy_row_count"], 15)

    def test_missing_source_recorded_not_faked(self):
        missing = [s for s in self.insp["source_refs"] if s.get("local_missing")]
        self.assertTrue(missing, "expected at least one absent recorded source")
        for s in missing:
            self.assertIsNone(s.get("sha256"))
            self.assertEqual(s["availability"], "LOCAL_MISSING_RECORDED")

    def test_identity_echo(self):
        i = self.insp["identity"]
        self.assertEqual(i["subject_id"], "FHS-5_PLP/W1/CONTROL_PACK")
        self.assertEqual(i["scope"], "W1-NF-01")

    def test_neg_wrong_identity(self):
        with self.assertRaises(base.NFError) as cm:
            reader.inspect_package(PACK, expected_identity={
                "project_id": "FHS-5_PLP", "subject_id": "X",
                "scope": "W1-NF-01", "wave_id": "W1", "batch_id": "W1-NF-01"})
        self.assertEqual(cm.exception.token, "IDENTITY_MISMATCH")

    def test_neg_tampered_byte(self):
        import shutil
        import tempfile
        tmp = Path(tempfile.mkdtemp(prefix="w1-tamper-"))
        try:
            dst = tmp / "pack"
            shutil.copytree(PACK, dst)
            (tmp / "evidence").mkdir()
            shutil.copy2(PACK.parent / "evidence" / "SEAL.json", tmp / "evidence" / "SEAL.json")
            p = dst / "02_W1_OPS_ECP.md"
            b = bytearray(p.read_bytes())
            b[40] = ord("Z") if b[40] != ord("Z") else ord("Y")
            p.write_bytes(bytes(b))
            with self.assertRaises(base.NFError) as cm:
                reader.inspect_package(dst)
            self.assertEqual(cm.exception.token, "DIGEST_MISMATCH")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_neg_dag_cycle(self):
        with self.assertRaises(base.NFError) as cm:
            base._topo(["A", "B"], [["A", "B"], ["B", "A"]])
        self.assertEqual(cm.exception.token, "DAG_CYCLE")

    def test_unknown_is_preserved(self):
        x = self.insp["abi_crosswalk"]
        self.assertEqual(x["unknown_drop"], 0)
        for row in x["entity_fields"]:
            self.assertTrue(row["unknown_preserved"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
