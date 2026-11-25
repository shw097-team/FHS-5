#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge tests: four APIs, full body, untrusted markers, exact compare."""
import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "impl"))

import bridge_nf as bridge
import nf_reader as reader
import w1_nf_reader as base

PACK = Path(os.environ.get(
    "W1_PACK",
    r"C:/Users/user/Downloads/FHS-5/FHS-5_PLP_W0-W4_實作/W1/"
    r"W1_Native-first_CODEX_主用修補_交付/FHS-5_PLP_W1_NATIVE_FIRST"))


class TestBridge(unittest.TestCase):
    def test_inspect_pos(self):
        r = bridge.inspect_package(str(PACK / "05_W1_SOURCE_MANIFEST.json"), str(PACK))
        self.assertEqual(r["manifest_sha256"], "61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a")
        self.assertGreaterEqual(len(r["requirements"]), 80)
        self.assertEqual(r["effect_constraints"]["permission_state"], "NONE_GRANTED")
        self.assertEqual(r["wrote_bytes"], 0)

    def test_inspect_neg_wrong_pin(self):
        with self.assertRaises(base.NFError) as cm:
            bridge.inspect_package(str(PACK / "05_W1_SOURCE_MANIFEST.json"), str(PACK),
                                   expected_sha256="0" * 64)
        self.assertEqual(cm.exception.token, "SOURCE_INTEGRITY_FAILED")

    def test_explain_full_body(self):
        e = bridge.explain_slice(str(PACK), "abi")
        self.assertTrue(e["sections"])
        for s in e["sections"]:
            self.assertFalse(s["is_heading_only"])
            self.assertTrue(s["text"])
        self.assertEqual(e["semantic_state"], "FULL_SECTION_TEXT")

    def test_explain_carries_parent_chain(self):
        e = bridge.explain_slice(str(PACK), "abi")
        self.assertTrue(any(v for v in e["parent_chain"].values()))

    def test_explain_neg_unknown_view(self):
        with self.assertRaises(base.NFError) as cm:
            bridge.explain_slice(str(PACK), "nope")
        self.assertEqual(cm.exception.token, "VIEW_UNKNOWN")

    def test_render_markers_and_no_grant(self):
        e = bridge.explain_slice(str(PACK), "dev")
        r = bridge.render_agent_context(e, "Codex", "W1-NF-01")
        self.assertEqual(r["permission_state"], "NONE_GRANTED")
        self.assertFalse(r["consumed"])
        self.assertEqual(r["context_sha256"], reader.sha256_bytes(r["context_utf8"].encode("utf-8")))

    def test_render_neg_scope_mismatch(self):
        e = bridge.explain_slice(str(PACK), "dev")
        with self.assertRaises(base.NFError) as cm:
            bridge.render_agent_context(e, "Codex", "W2-OTHER")
        self.assertEqual(cm.exception.token, "CONTEXT_SCOPE_MISMATCH")

    def test_render_neg_unknown_host(self):
        e = bridge.explain_slice(str(PACK), "dev")
        with self.assertRaises(base.NFError):
            bridge.render_agent_context(e, "UnknownHost")

    def test_compare_same_is_park(self):
        a = reader.inspect_package(PACK)
        b = reader.inspect_package(PACK)
        c = bridge.compare_context(a, b)
        self.assertEqual(c["state"], "PARK_NO_DELTA_CANDIDATE")
        self.assertEqual(c["changed"], [])

    def test_compare_neg_cross_subject(self):
        a = reader.inspect_package(PACK)
        b = json.loads(json.dumps(a))
        b["identity"]["subject_id"] = "OTHER/SUBJECT"
        with self.assertRaises(base.NFError) as cm:
            bridge.compare_context(a, b)
        self.assertEqual(cm.exception.token, "COMPARE_CROSS_SUBJECT_DENY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
