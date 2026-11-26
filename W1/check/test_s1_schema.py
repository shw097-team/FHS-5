#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K1-A acceptance: S1 SourceManifest@1 is really read, not string-matched."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
IS_IMPL = (HERE.parent / "impl")
sys.path.insert(0, str(IS_IMPL))

import s1_reader as S  # noqa: E402

WT = HERE.parents[1]
PACKS = WT / "S1_PACKS"
SEALS = PACKS / "SEALS"


def pack(wave):
    p = PACKS / f"FHS-5_PLP_{wave}_NATIVE_FIRST"
    if not p.is_dir():
        raise unittest.SkipTest("S1 packs not present")
    return p


class S1SchemaTests(unittest.TestCase):
    def test_w1_counts_and_seal(self):
        r = S.inspect_s1(pack("W1"), SEALS / "W1_PACK_SEAL.json", expected_wave="W1")
        self.assertEqual(r["abi"], "SourceManifest.S1@1")
        self.assertEqual(r["counts"]["dev"], 38)
        self.assertEqual(r["counts"]["ops"], 29)
        self.assertEqual(r["counts"]["cases"], 13)
        self.assertEqual(r["counts"]["assets"], 26)
        self.assertEqual(r["counts"]["holds"], 14)
        self.assertEqual(r["manifest_sha256"],
                         "d1c741533bea41b8d786ec870b6f66323739a65ebdafd241545dc4afa9dff28c")
        self.assertEqual(r["pack_tree_sha256"],
                         "593314d503a162caea4c05dc263cd6e68511cfe5b70446043560bc757347d18f")
        self.assertTrue(r["seal_verified"])
        self.assertEqual(r["identity"]["subject_id"], "FHS-5_PLP/W1/CONTROL_PACK")

    def test_w2_counts_and_seal(self):
        r = S.inspect_s1(pack("W2"), SEALS / "W2_PACK_SEAL.json", expected_wave="W2")
        self.assertEqual(r["counts"]["cases"], 12)
        self.assertEqual(r["counts"]["assets"], 25)
        self.assertEqual(r["denominators"]["requirements"], 16)
        self.assertEqual(r["manifest_sha256"],
                         "911d06c98eef8edea13bf0c82956a55d420daa93e7599f3344f317a84486b65b")
        self.assertTrue(r["seal_verified"])

    def test_neg_tampered_asset(self):
        tmp = Path(tempfile.mkdtemp(prefix="s1neg_"))
        try:
            d = tmp / "p"
            shutil.copytree(pack("W1"), d)
            a = d / "assets" / "oracles" / "W1-ABI-01.json"
            a.write_bytes(a.read_bytes() + b"\n")
            with self.assertRaises(S.S1Error) as ctx:
                S.inspect_s1(d, SEALS / "W1_PACK_SEAL.json")
            self.assertEqual(ctx.exception.token, "DIGEST_MISMATCH")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_neg_seal_binding(self):
        tmp = Path(tempfile.mkdtemp(prefix="s1seal_"))
        try:
            d = tmp / "p"
            shutil.copytree(pack("W2"), d)
            seal = json.loads((SEALS / "W2_PACK_SEAL.json").read_text(encoding="utf-8"))
            seal["manifest"]["sha256"] = "0" * 64
            sp = tmp / "seal.json"
            sp.write_text(json.dumps(seal), encoding="utf-8")
            with self.assertRaises(S.S1Error) as ctx:
                S.inspect_s1(d, sp)
            self.assertEqual(ctx.exception.token, "SEAL_BINDING")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_neg_self_hash_claim(self):
        tmp = Path(tempfile.mkdtemp(prefix="s1self_"))
        try:
            d = tmp / "p"
            shutil.copytree(pack("W1"), d)
            m = d / "05_W1_SOURCE_MANIFEST.json"
            doc = json.loads(m.read_text(encoding="utf-8"))
            doc["manifest_self_hash"] = "sha256:deadbeef"
            m.write_text(json.dumps(doc), encoding="utf-8")
            with self.assertRaises(S.S1Error) as ctx:
                S.inspect_s1(d)
            self.assertEqual(ctx.exception.token, "MANIFEST_SELF_HASH")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
