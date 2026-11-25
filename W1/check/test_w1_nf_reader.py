#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POS/NEG tests for W1 NF-r2 reader.

Run from the repo root:
    python -m unittest W1/check/test_w1_nf_reader.py -v

The real pack is supplied by W1_NF_PACK_ROOT or defaults to the delivered
path used during the W1 construction run. Mutation tests copy the delivery
tree to a temp directory and never modify the real pack.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "W1" / "impl"))

import w1_nf_reader as nf  # noqa: E402

DEFAULT_PACK = Path(
    r"C:\Users\user\Documents\Codex\2026-11-25\new-chat-11\outputs"
    r"\W1_Native-first_CODEX_主用修補_交付\FHS-5_PLP_W1_NATIVE_FIRST"
)
PACK = Path(os.environ.get("W1_NF_PACK_ROOT", str(DEFAULT_PACK)))


def delivery_root(pack: Path) -> Path:
    return pack.parent


class NFReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not PACK.is_dir():
            raise unittest.SkipTest(f"pack not found: {PACK}")

    def test_inspect_real_pack(self):
        r = nf.inspect_package(PACK)
        self.assertEqual(r["schema"], "FHS5.PLP.W1.NFInspect@1")
        self.assertEqual(r["counts"]["pack_files"], 5)
        self.assertEqual(r["counts"]["dev"], 38)
        self.assertEqual(r["counts"]["ops"], 29)
        self.assertEqual(r["counts"]["cases"], 13)
        self.assertEqual(r["counts"]["assets"], 26)
        self.assertEqual(r["counts"]["sources"], 42)
        self.assertEqual(r["dag"]["topological_order"], ["P01", "P02", "P03", "P04", "P05", "P06"])
        self.assertEqual(r["permission_state"], "NONE_GRANTED")
        self.assertEqual(r["claims"]["w1_execution_ready"], "READY")

    def test_explain_full_sections(self):
        e = nf.explain_slice(PACK, "abi")
        self.assertTrue(e["sections"])
        for s in e["sections"]:
            self.assertFalse(s["is_heading_only"])
            self.assertGreater(len(s["text"]), len(s["heading"]))
            self.assertEqual(len(s["text_sha256"]), 64)

    def test_render_marks_untrusted(self):
        i = nf.inspect_package(PACK)
        e = nf.explain_slice(PACK, "cases")
        r = nf.render_agent_context(i, "Codex", i["identity"]["scope"], e["sections"])
        self.assertEqual(r["permission_state"], "NONE_GRANTED")
        self.assertFalse(r["consumed"])
        self.assertTrue(r["untrusted_markers"], "expected at least one untrusted marker in case sections")
        self.assertIn("UNTRUSTED SOURCE DATA", r["context_utf8"])
        self.assertEqual(len(r["context_sha256"]), 64)

    def test_resolve_body_span(self):
        b = nf.resolve_body(PACK, "00_W1_PI_PD.md", 1, 20)
        self.assertFalse(b["is_excerpt"])
        self.assertEqual(b["line_start"], 1)
        self.assertEqual(b["line_end"], 20)
        self.assertIn("FHS-5_PLP_W1_NATIVE_FIRST", b["full_text"])

    def test_compare_same_subject(self):
        a = nf.inspect_package(PACK)
        b = nf.inspect_package(PACK)
        c = nf.compare_context(a, b)
        self.assertTrue(c["comparable"])
        self.assertEqual(c["added"], [])
        self.assertEqual(c["removed"], [])
        self.assertEqual(c["changed"], [])

    def test_compare_cross_scope_rejected(self):
        a = nf.inspect_package(PACK)
        b = json.loads(json.dumps(a))
        b["identity"]["scope"] = "OTHER-SCOPE"
        with self.assertRaises(nf.NFError) as ctx:
            nf.compare_context(a, b)
        self.assertEqual(ctx.exception.token, "COMPARE_CROSS_SUBJECT_DENY")


class NFMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not PACK.is_dir():
            raise unittest.SkipTest(f"pack not found: {PACK}")

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.dst = Path(self.td.name) / "delivery"
        shutil.copytree(delivery_root(PACK), self.dst)
        self.pack = self.dst / PACK.name

    def tearDown(self):
        self.td.cleanup()

    def reseal(self):
        mp = self.pack / "05_W1_SOURCE_MANIFEST.json"
        m = json.loads(mp.read_text(encoding="utf-8"))
        for e in m["pack_files"]:
            info = nf.file_info(self.pack / e["path"])
            e.update(info)
        mp.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        seal_path = self.dst / "evidence" / "SEAL.json"
        s = json.loads(seal_path.read_text(encoding="utf-8"))
        s["pack_manifest_sha256"] = nf.sha256_bytes(mp.read_bytes())
        s["pack_files"] = [{"path": e["path"], **nf.file_info(self.pack / e["path"])} for e in m["pack_files"]]
        seal_path.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    def assert_reject(self, token):
        with self.assertRaises(nf.NFError) as ctx:
            nf.inspect_package(self.pack)
        self.assertEqual(ctx.exception.token, token)

    def test_byte_flip(self):
        p = self.pack / "00_W1_PI_PD.md"
        p.write_bytes(p.read_bytes() + b"X")
        self.assert_reject("DIGEST_MISMATCH")

    def test_missing_pack_file(self):
        (self.pack / "03_W1_TQAEP.md").unlink()
        self.assert_reject("PACK_INCOMPLETE_LOCAL")

    def test_duplicate_json_key(self):
        mp = self.pack / "05_W1_SOURCE_MANIFEST.json"
        t = mp.read_text(encoding="utf-8")
        mp.write_text(t.replace('"schema":', '"schema": "X",\n  "schema":', 1), encoding="utf-8", newline="\n")
        self.assert_reject("STRICT_JSON_REJECT")

    def test_nan_value(self):
        mp = self.pack / "05_W1_SOURCE_MANIFEST.json"
        t = mp.read_text(encoding="utf-8")
        mp.write_text(t.replace('"profile":', '"bad": NaN,\n  "profile":', 1), encoding="utf-8", newline="\n")
        self.assert_reject("STRICT_JSON_REJECT")

    def test_path_traversal(self):
        mp = self.pack / "05_W1_SOURCE_MANIFEST.json"
        m = json.loads(mp.read_text(encoding="utf-8"))
        m["pack_files"][0]["path"] = "../evil.md"
        mp.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        self.assert_reject("PACK_INCOMPLETE_LOCAL")

    def test_identity_mismatch(self):
        p = self.pack / "02_W1_OPS_ECP.md"
        t = p.read_text(encoding="utf-8").replace("**project_id**：`FHS-5_PLP`", "**project_id**：`FHS-5_XXX`", 1)
        p.write_text(t, encoding="utf-8", newline="\n")
        self.reseal()
        self.assert_reject("IDENTITY_MISMATCH")

    def test_drop_dev_id(self):
        p = self.pack / "01_W1_DEV_ECP.md"
        lines = p.read_text(encoding="utf-8").splitlines()
        out, dropped = [], False
        for ln in lines:
            if not dropped and ln.startswith("| `DEV-PERM-01`"):
                dropped = True
                continue
            out.append(ln)
        p.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
        self.reseal()
        self.assert_reject("ID_SET_INCOMPLETE")

    def test_dag_cycle(self):
        mp = self.pack / "05_W1_SOURCE_MANIFEST.json"
        m = json.loads(mp.read_text(encoding="utf-8"))
        m["dag"]["edges"].append(["P06", "P01"])
        mp.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        self.reseal()
        self.assert_reject("DAG_CYCLE")

    def test_asset_digest(self):
        p = self.pack / "assets" / "fixtures" / "W1-HOST-01.json"
        p.write_bytes(p.read_bytes() + b" ")
        self.assert_reject("ASSET_DIGEST_MISMATCH")

    def test_seal_mismatch(self):
        s = self.dst / "evidence" / "SEAL.json"
        obj = json.loads(s.read_text(encoding="utf-8"))
        obj["pack_manifest_sha256"] = "0" * 64
        s.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        self.assert_reject("SEAL_MISMATCH")


if __name__ == "__main__":
    unittest.main(verbosity=2)
