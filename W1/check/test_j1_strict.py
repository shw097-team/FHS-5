#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""J1 strictness tests (S1 .. S6) — the residual contract from the r2 closure.

Run from W1/check:

    python -m unittest -v test_j1_strict

Covers what the first repair round did not:
  S1 duplicate JSON keys refused          S4 exact scope field (no substring)
  S2 NaN / Infinity refused               S5 TOCTOU: swap between verify and consume
  S3 BOM refused                          S6 control: clean verify -> consume
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import w2_receiver as R  # noqa: E402

WORKTREE = HERE.parents[1]

BASE_IDENT = {
    "subject_id": "FHS-5_PLP/W1/CONTROL_PACK",
    "scope": "W1-NF-01",
    "permission_state": "NONE_GRANTED",
    "producer_identity": "FHS-5_PLP/W1/CONTROL_PACK",
    "consumer_identity": "FHS-5_PLP/W2/CONSUMER",
    "expected_pack_sha256": None,
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pins_for(root: Path) -> dict:
    return {
        "evidence_manifest_sha256": sha_bytes((root / "EVIDENCE_MANIFEST.json").read_bytes()),
        "delivery_seal_sha256": sha_bytes((root / "DELIVERY_SEAL.json").read_bytes()),
        "pack_manifest_sha256": R.PACK_PIN,
    }


def find_delivery() -> Path:
    for pattern in ("18_W1_NF_*", "17_W1_NF_*"):
        for cand in sorted(WORKTREE.glob(pattern)):
            if (cand / "EVIDENCE_MANIFEST.json").is_file():
                return cand
    raise unittest.SkipTest("no frozen W1 delivery found in the worktree")


class J1StrictTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._src = find_delivery()

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="j1s_"))
        self.d = self.tmp / "delivery"
        shutil.copytree(self._src, self.d)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # --- S1 duplicate keys ------------------------------------------------
    def test_s1_duplicate_keys_refused(self):
        man = self.d / "EVIDENCE_MANIFEST.json"
        raw = man.read_text(encoding="utf-8")
        # inject a second "schema" key at the top level
        raw = raw.replace('"schema"', '"schema": "dup", "schema"', 1)
        man.write_text(raw, encoding="utf-8", newline="\n")
        res = R.verify_delivery(self.d, pins_for(self.d))
        self.assertFalse(res["ok"])
        self.assertIn("duplicate", json.dumps(res["checks"]).lower())

    # --- S2 NaN / Infinity -----------------------------------------------
    def test_s2_non_finite_refused(self):
        man = self.d / "EVIDENCE_MANIFEST.json"
        obj = json.loads(man.read_text(encoding="utf-8"))
        obj["__probe"] = float("nan")
        man.write_text(json.dumps(obj), encoding="utf-8", newline="\n")
        res = R.verify_delivery(self.d, pins_for(self.d))
        self.assertFalse(res["ok"])

    # --- S3 BOM -----------------------------------------------------------
    def test_s3_bom_refused(self):
        man = self.d / "EVIDENCE_MANIFEST.json"
        man.write_bytes(b"\xef\xbb\xbf" + man.read_bytes())
        res = R.verify_delivery(self.d, pins_for(self.d))
        self.assertFalse(res["ok"])
        self.assertIn("BOM", json.dumps(res["checks"]))

    # --- S4 exact scope field --------------------------------------------
    def test_s4_scope_is_exact_not_substring(self):
        # requested scope is a strict prefix of the handoff's field value
        ident = dict(BASE_IDENT, scope="W1-NF-0")
        res = R.verify_delivery(self.d, pins_for(self.d))
        self.assertTrue(res["ok"], "control verify must pass first")
        receipt = R.receive(self.d, ident, pins_for(self.d), self.tmp / "out")
        self.assertFalse(receipt["accepted"])
        self.assertEqual(receipt["first_fail"], "SCOPE_MISMATCH")
        self.assertEqual(receipt["product_calls"], {"build_contracts": 0, "seam_wiring": 0})

    def test_s4b_scope_field_absent_from_prose_only(self):
        # remove the machine field but keep the scope in prose: must refuse
        hand = self.d / "FHS-5_PLP_W1_HANDOFF.md"
        text = hand.read_text(encoding="utf-8")
        filtered = "\n".join(l for l in text.splitlines()
                             if not l.strip().startswith("scope:"))
        hand.write_text(filtered, encoding="utf-8", newline="\n")
        seal = self.d / "DELIVERY_SEAL.json"
        man = self.d / "EVIDENCE_MANIFEST.json"
        obj = json.loads(man.read_text(encoding="utf-8"))
        for f in obj.get("files") or []:
            if f["path"].endswith("FHS-5_PLP_W1_HANDOFF.md"):
                f["sha256"] = sha_bytes(hand.read_bytes())
                f["bytes"] = hand.stat().st_size
        man.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="\n")
        so = json.loads(seal.read_text(encoding="utf-8"))
        so["evidence_manifest_sha256"] = sha_bytes(man.read_bytes())
        seal.write_text(json.dumps(so, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")
        r = R.receive(self.d, dict(BASE_IDENT), pins_for(self.d), self.tmp / "out2")
        self.assertFalse(r["accepted"])
        self.assertEqual(r["first_fail"], "SCOPE_MISMATCH")

    # --- S5 TOCTOU --------------------------------------------------------
    def test_s5_swap_between_verify_and_consume(self):
        pins = pins_for(self.d)
        verified = R.verify_delivery(self.d, pins)
        self.assertTrue(verified["ok"])
        # swap the manifest after verification
        man = self.d / "EVIDENCE_MANIFEST.json"
        man.write_bytes(man.read_bytes() + b"\n")
        with self.assertRaises(R.NFError) as ctx:
            R.consume_verified(verified, self.tmp / "out3")
        self.assertIn("TOCTOU", str(ctx.exception))
        self.assertEqual(list((self.tmp / "out3").rglob("*")) if (self.tmp / "out3").exists() else [], [])

    # --- S6 control -------------------------------------------------------
    def test_s6_clean_verify_then_consume(self):
        pins = pins_for(self.d)
        verified = R.verify_delivery(self.d, pins)
        self.assertTrue(verified["ok"])
        out = self.tmp / "out4"
        res = R.consume_verified(verified, out)
        self.assertTrue(res["ok"])
        self.assertGreater(res["product_calls"]["build_contracts"], 0)


if __name__ == "__main__":
    unittest.main()
