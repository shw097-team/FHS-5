#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""J1 receiver acceptance tests (J1-T01 .. J1-T06).

Run from W1/check:

    python -m unittest -v test_j1_receiver

All fixtures are written to an OS temporary directory and removed afterwards.
No network, no real secret, and the source delivery is never mutated.
"""
from __future__ import annotations

import builtins
import hashlib
import json
import os
import shutil
import subprocess
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
ZERO_CALLS = {"build_contracts": 0, "seam_wiring": 0}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def delivery_pins(root: Path) -> dict:
    return {
        "evidence_manifest_sha256": sha_bytes(
            (root / "EVIDENCE_MANIFEST.json").read_bytes()),
        "delivery_seal_sha256": sha_bytes(
            (root / "DELIVERY_SEAL.json").read_bytes()),
        "pack_manifest_sha256": R.PACK_PIN,
    }


def find_delivery() -> Path:
    for pattern in ("18_W1_NF_*", "17_W1_NF_*"):
        for cand in sorted(WORKTREE.glob(pattern)):
            if ((cand / "EVIDENCE_MANIFEST.json").is_file()
                    and (cand / "DELIVERY_SEAL.json").is_file()
                    and (cand / "control_pack").is_dir()):
                return cand.resolve()
    raise unittest.SkipTest("no W1 delivery tree next to the worktree")


def entry(path: str, data: bytes) -> dict:
    return {"path": path, "sha256": sha_bytes(data), "bytes": len(data)}


def make_delivery(root: Path, manifest_entries, files=None, manifest_obj=None,
                  manifest_bytes=None, seal_binding=None) -> dict:
    """Build a tiny self-consistent delivery and return its external pins."""
    root.mkdir(parents=True, exist_ok=True)
    for rel, data in (files or {}).items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    if manifest_bytes is None:
        obj = manifest_obj if manifest_obj is not None else {
            "schema": R.SCHEMA_MANIFEST,
            "pack_manifest_sha256": R.PACK_PIN,
            "files": list(manifest_entries),
        }
        manifest_bytes = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
    (root / "EVIDENCE_MANIFEST.json").write_bytes(manifest_bytes)
    manifest_sha = sha_bytes(manifest_bytes)
    seal = {
        "schema": R.SCHEMA_SEAL,
        "evidence_manifest_sha256": manifest_sha if seal_binding is None else seal_binding,
        "pack_manifest_sha256": R.PACK_PIN,
    }
    seal_bytes = json.dumps(seal, ensure_ascii=False).encode("utf-8")
    (root / "DELIVERY_SEAL.json").write_bytes(seal_bytes)
    return {
        "evidence_manifest_sha256": manifest_sha,
        "delivery_seal_sha256": sha_bytes(seal_bytes),
        "pack_manifest_sha256": R.PACK_PIN,
    }


def make_junction(link: Path, target: Path) -> None:
    try:
        os.symlink(target, link, target_is_directory=True)
        return
    except OSError:
        pass
    res = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise unittest.SkipTest(f"cannot create symlink/junction: {res.stderr.strip()}")


def open_spy():
    """Record every path passed to builtins.open while a verification runs."""
    opened = []
    real_open = builtins.open

    def spy(file, *args, **kwargs):
        try:
            opened.append(os.path.normcase(str(Path(file).resolve())))
        except OSError:
            opened.append(str(file))
        return real_open(file, *args, **kwargs)

    return opened, mock.patch("builtins.open", spy)


def norm(p: Path) -> str:
    return os.path.normcase(str(p.resolve()))


class J1ReceiverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="j1_receiver_"))
        cls.addClassCleanup(shutil.rmtree, cls.tmp, True)
        cls.source = find_delivery()
        cls.clean = cls.tmp / "clean_delivery"
        shutil.copytree(cls.source, cls.clean)
        cls.pins = delivery_pins(cls.clean)
        cls.manifest = json.loads(
            (cls.clean / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix=self._testMethodName + "_",
                                          dir=self.tmp))

    def ident(self, **overrides) -> dict:
        ident = dict(BASE_IDENT)
        ident.update(overrides)
        return ident

    def assert_no_output(self, out: Path):
        if out.exists():
            self.assertEqual([p for p in out.rglob("*") if p.is_file()], [])

    # ---- J1-T01 -------------------------------------------------------
    def test_j1_t01_clean_delivery_and_consume(self):
        before = R.tree_digest(self.clean)
        verified = R.verify_delivery(self.clean, self.pins)

        self.assertTrue(verified["ok"], verified["first_fail"])
        self.assertIsNone(verified["first_fail"])
        self.assertEqual(verified["verified_entries"], len(self.manifest["files"]))
        self.assertEqual(verified["verified_paths"],
                         [f["path"] for f in self.manifest["files"]])
        self.assertEqual(verified["manifest_sha256"],
                         self.pins["evidence_manifest_sha256"])
        self.assertEqual(verified["pins_used"], self.pins)
        self.assertEqual([c["name"] for c in verified["checks"] if not c["ok"]], [])

        out = self.work / "out"
        receipt = R.receive(self.clean, self.ident(), self.pins, out)

        self.assertTrue(receipt["accepted"], receipt["rejected_checks"])
        self.assertEqual(receipt["product_calls"],
                         {"build_contracts": 1, "seam_wiring": 1})
        self.assertTrue(receipt["consume_performed"])
        self.assertEqual(receipt["verified_entries"],
                         len(self.manifest["files"]))
        self.assertTrue((out / "material_copy" / "context_bundle.md").is_file())
        self.assertTrue((out / "material_copy"
                         / "05_W2_SOURCE_MANIFEST.json").is_file())
        self.assertEqual([c["name"] for c in receipt["checks"] if not c["ok"]], [])

        after = R.tree_digest(self.clean)
        self.assertEqual(after, before)
        self.assertEqual(receipt["delivery_tree_sha256"], before)
        self.assertEqual(receipt["delivery_tree_sha256_after"], before)

    # ---- J1-T02 -------------------------------------------------------
    def test_j1_t02_pin_tamper_and_forged_seal(self):
        bad_manifest = dict(self.pins)
        bad_manifest["evidence_manifest_sha256"] = "0" * 64
        v = R.verify_delivery(self.clean, bad_manifest)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "BYTES_MISMATCH")

        bad_seal = dict(self.pins)
        bad_seal["delivery_seal_sha256"] = "1" * 64
        v = R.verify_delivery(self.clean, bad_seal)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "BYTES_MISMATCH")

        bad_pack = dict(self.pins)
        bad_pack["pack_manifest_sha256"] = "2" * 64
        v = R.verify_delivery(self.clean, bad_pack)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "BYTES_MISMATCH")

        missing = dict(self.pins)
        missing.pop("delivery_seal_sha256")
        v = R.verify_delivery(self.clean, missing)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "PINS_MISSING")

        # Self-consistent forgery: manifest + seal agree with each other, but
        # the consumer's external pins still point at the original bytes.
        forged = self.work / "forged"
        shutil.copytree(self.clean, forged)
        payload = b"forged-evidence\n"
        (forged / "evidence" / "forged_extra.txt").write_bytes(payload)
        man = json.loads((forged / "EVIDENCE_MANIFEST.json").read_text(
            encoding="utf-8"))
        man["files"].append({"path": "evidence/forged_extra.txt",
                             "sha256": sha_bytes(payload), "bytes": len(payload)})
        forged_manifest = json.dumps(man, ensure_ascii=False, indent=2).encode("utf-8")
        (forged / "EVIDENCE_MANIFEST.json").write_bytes(forged_manifest)
        seal = json.loads((forged / "DELIVERY_SEAL.json").read_text(encoding="utf-8"))
        seal["evidence_manifest_sha256"] = sha_bytes(forged_manifest)
        (forged / "DELIVERY_SEAL.json").write_bytes(
            json.dumps(seal, ensure_ascii=False).encode("utf-8"))
        resealed = json.loads((forged / "DELIVERY_SEAL.json").read_text(
            encoding="utf-8"))
        self.assertEqual(resealed["evidence_manifest_sha256"],
                         sha_bytes(forged_manifest))
        self.assertNotEqual(sha_bytes(forged_manifest),
                            self.pins["evidence_manifest_sha256"])

        v = R.verify_delivery(forged, self.pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "BYTES_MISMATCH")

    # ---- J1-T03 -------------------------------------------------------
    def test_j1_t03_schema_missing_and_bytes(self):
        missing = self.work / "missing_raw"
        shutil.copytree(self.clean, missing)
        pins = delivery_pins(missing)
        victim = missing / "evidence" / "raw" / "_host.json"
        self.assertTrue(victim.is_file())
        victim.unlink()
        v = R.verify_delivery(missing, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "ENTRY_MISSING")

        empty = self.work / "empty"
        pins = make_delivery(empty, [], manifest_bytes=b"")
        v = R.verify_delivery(empty, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "SCHEMA_INVALID")

        payload = b"dup\n"
        dup = self.work / "duplicate"
        pins = make_delivery(dup, [entry("a.txt", payload), entry("a.txt", payload)],
                             files={"a.txt": payload})
        v = R.verify_delivery(dup, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "SCHEMA_INVALID")

        wrong_schema = self.work / "wrong_schema"
        pins = make_delivery(
            wrong_schema, [entry("a.txt", b"a")], files={"a.txt": b"a"},
            manifest_obj={"schema": "FHS5.Bogus@1",
                          "pack_manifest_sha256": R.PACK_PIN,
                          "files": [entry("a.txt", b"a")]})
        v = R.verify_delivery(wrong_schema, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "SCHEMA_INVALID")

        wrong_bytes = self.work / "wrong_bytes"
        shutil.copytree(self.clean, wrong_bytes)
        pins = delivery_pins(wrong_bytes)
        (wrong_bytes / "evidence" / "cases.json").write_bytes(b"{}")
        v = R.verify_delivery(wrong_bytes, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "BYTES_MISMATCH")

    # ---- J1-T04 -------------------------------------------------------
    def test_j1_t04_root_confinement(self):
        outside = self.work / "outside"
        canary = outside / "canary" / "ESCAPE.txt"
        canary.parent.mkdir(parents=True)
        canary.write_bytes(b"CANARY-MUST-NOT-BE-READ\n")
        canary_sha = sha_bytes(canary.read_bytes())
        canary_entry = {"path": "", "sha256": canary_sha,
                        "bytes": canary.stat().st_size}

        escape_paths = [
            ("traversal", "../outside/canary/ESCAPE.txt"),
            ("absolute", "/etc/passwd"),
            ("unc", "\\\\server\\share\\ESCAPE.txt"),
            ("drive_relative", "C:canary/ESCAPE.txt"),
        ]
        for name, raw_path in escape_paths:
            with self.subTest(case=name):
                d = self.work / name
                item = dict(canary_entry, path=raw_path)
                pins = make_delivery(d, [item])
                opened, patch = open_spy()
                with patch:
                    v = R.verify_delivery(d, pins)
                self.assertFalse(v["ok"])
                self.assertEqual(v["first_fail"], "PATH_ESCAPE")
                self.assertEqual(v["verified_entries"], 0)
                self.assertNotIn(raw_path, v["verified_paths"])
                self.assertNotIn(norm(canary), opened)

        # Symlink / junction escape: the link is inside, the target is not.
        link_case = self.work / "junction"
        secret_dir = self.work / "outside_dir"
        secret_dir.mkdir()
        secret = secret_dir / "secret.txt"
        secret.write_bytes(b"OUTSIDE-JUNCTION-SECRET\n")
        pins = make_delivery(link_case, [entry("linkdir/secret.txt",
                                               secret.read_bytes())])
        make_junction(link_case / "linkdir", secret_dir)
        opened, patch = open_spy()
        with patch:
            v = R.verify_delivery(link_case, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "PATH_ESCAPE")
        self.assertEqual(v["verified_entries"], 0)
        self.assertNotIn(norm(secret), opened)

        # Oversize entry is rejected before it is hashed.
        big = self.work / "oversize"
        payload = b"x" * 4096
        pins = make_delivery(big, [entry("big.bin", payload)],
                             files={"big.bin": payload})
        with mock.patch.object(R, "MAX_ENTRY_BYTES", 1024):
            v = R.verify_delivery(big, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "ENTRY_TOO_LARGE")

        # Invalid UTF-8 manifest is rejected even when its pin matches.
        bad_utf8 = self.work / "bad_utf8"
        payload = b'{"schema": "\xff\xfe", "files": []}'
        pins = make_delivery(bad_utf8, [], manifest_bytes=payload)
        v = R.verify_delivery(bad_utf8, pins)
        self.assertFalse(v["ok"])
        self.assertEqual(v["first_fail"], "SCHEMA_INVALID")

    # ---- J1-T05 -------------------------------------------------------
    def test_j1_t05_identity_scope_and_fake_grant(self):
        cases = [
            ("fake_grant", self.ident(permission_state="GRANTED"),
             "FAKE_GRANT", "no_fake_grant"),
            ("wrong_scope", self.ident(scope="W9-BOGUS-SCOPE"),
             "SCOPE_MISMATCH", "handoff_scope"),
            ("wrong_producer",
             self.ident(producer_identity="FHS-5_PLP/W2/CONSUMER"),
             "IDENTITY_MISMATCH", "identity_split"),
            ("false_pack_pin", self.ident(expected_pack_sha256="9" * 64),
             "PACK_PIN_MISMATCH", "caller_pack_pin"),
        ]
        for name, ident, token, check in cases:
            with self.subTest(case=name):
                out = self.work / ("out_" + name)
                receipt = R.receive(self.clean, ident, self.pins, out)
                self.assertFalse(receipt["accepted"])
                self.assertEqual(receipt["first_fail"], token)
                self.assertIn(check, receipt["rejected_checks"])
                self.assertEqual(receipt["product_calls"], ZERO_CALLS)
                self.assertFalse(receipt["consume_performed"])
                self.assert_no_output(out)

        missing_pin = dict(self.pins)
        missing_pin.pop("pack_manifest_sha256")
        out = self.work / "out_missing_pin"
        receipt = R.receive(self.clean, self.ident(), missing_pin, out)
        self.assertFalse(receipt["accepted"])
        self.assertEqual(receipt["first_fail"], "PINS_MISSING")
        self.assertIn("pins_present", receipt["rejected_checks"])
        self.assertEqual(receipt["product_calls"], ZERO_CALLS)
        self.assert_no_output(out)

    # ---- J1-T06 -------------------------------------------------------
    def test_j1_t06_failure_path_has_no_product_calls(self):
        out_fail = self.work / "out_fail"
        receipt = R.receive(self.clean, self.ident(), None, out_fail)
        self.assertFalse(receipt["accepted"])
        self.assertEqual(receipt["first_fail"], "PINS_MISSING")
        self.assertEqual(receipt["product_calls"], ZERO_CALLS)
        self.assertFalse(receipt["consume_performed"])
        self.assert_no_output(out_fail)

        out_preflight = self.work / "out_preflight"
        receipt = R.receive(self.clean, self.ident(permission_state="GRANTED"),
                            self.pins, out_preflight)
        self.assertFalse(receipt["accepted"])
        self.assertEqual(receipt["product_calls"], ZERO_CALLS)
        self.assert_no_output(out_preflight)

        out_unverified = self.work / "out_unverified"
        with self.assertRaises(R.NFError) as ctx:
            R.consume_verified({"ok": False, "pins_used": self.pins}, out_unverified)
        self.assertEqual(ctx.exception.token, "NOT_VERIFIED")
        self.assert_no_output(out_unverified)

        # The delivery tree is never an output root.
        inside = self.clean / "w2_out_should_not_exist"
        receipt = R.receive(self.clean, self.ident(), self.pins, inside)
        self.assertFalse(receipt["accepted"])
        self.assertEqual(receipt["first_fail"], "OUTPUT_ROOT_INVALID")
        self.assertEqual(receipt["product_calls"], ZERO_CALLS)
        self.assertFalse(inside.exists())

        # Positive control for the same path.
        out_ok = self.work / "out_ok"
        receipt = R.receive(self.clean, self.ident(), self.pins, out_ok)
        self.assertTrue(receipt["accepted"], receipt["rejected_checks"])
        self.assertGreater(receipt["product_calls"]["build_contracts"], 0)
        self.assertGreater(receipt["product_calls"]["seam_wiring"], 0)
        self.assertTrue((out_ok / "material_copy" / "context_bundle.md").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
