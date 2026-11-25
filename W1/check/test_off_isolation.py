#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for ``off_isolation`` (FHS-5 W1 / R03).

These tests assert *observed* behaviour, not declared behaviour:

* the cold-off probe really blocks the forbidden runtimes, and the same probe
  really detects a successful import (negative control);
* the resolver really raises for all 7 path attacks;
* the canary really notices a byte change (negative control);
* the link probe is either REJECT or an honest NOT_VERIFIED.

Run from this directory with:

    set PYTHONDONTWRITEBYTECODE=1
    python -B -m unittest test_off_isolation -v
"""
from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
IMPL = Path(os.environ.get("W1_IMPL", str(HERE.parent / "impl")))
if str(IMPL) not in sys.path:
    sys.path.insert(0, str(IMPL))

import off_isolation as oi  # noqa: E402  (path bootstrap above)

PACK = os.environ.get("W1_PACK") or oi.DEFAULT_PACK_ROOT
HEX64 = set("0123456789abcdef")


def _is_hex64(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX64


class TestOffIsolation(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.pack = PACK
        if not Path(cls.pack).is_dir():
            raise AssertionError(f"W1_PACK is not a directory: {cls.pack}")
        cls.impl = oi._impl_dir()
        if not Path(cls.impl, "body_resolver.py").is_file():
            raise AssertionError(f"W1_IMPL has no body_resolver.py: {cls.impl}")
        cls.tmp = tempfile.mkdtemp(prefix="w1_r03_test_", dir=str(HERE))

    @classmethod
    def tearDownClass(cls) -> None:
        import shutil

        shutil.rmtree(cls.tmp, ignore_errors=True)

    # -- 1) cold-off -------------------------------------------------------
    def test_01_cold_off_probe_blocks_really_absent_runtimes(self) -> None:
        res = oi.cold_off_probe("FHS5-W1-R03", oi.FORBIDDEN_RUNTIME_MODULES)

        self.assertEqual(res["feature"], "FHS5-W1-R03")
        self.assertIsInstance(res["argv"], list)
        self.assertEqual(res["argv"][0], sys.executable)
        self.assertEqual(res["argv"][1], "-c")
        self.assertTrue(res["cwd"])
        self.assertEqual(res["exit"], 0, msg=f"stderr: {res['stderr'][:800]}")
        # The probes must carry real hashes of the real child streams.
        self.assertTrue(_is_hex64(res["stdout_sha256"]))
        self.assertTrue(_is_hex64(res["stderr_sha256"]))
        self.assertEqual(
            res["stdout_sha256"],
            hashlib.sha256(res["stdout"].encode("utf-8")).hexdigest(),
        )
        self.assertEqual(sorted(res["blocked"]), sorted(oi.FORBIDDEN_RUNTIME_MODULES))
        self.assertEqual(res["leaked"], [])
        self.assertIs(res["cold_off"], True, msg=f"leaked={res['leaked']}")
        self.assertEqual(res["state"], "OBSERVED")

    def test_02_cold_off_probe_detects_a_real_import(self) -> None:
        """Negative control: the same probe must see ``json`` import."""
        res = oi.cold_off_probe("negative-control", ["json"])
        self.assertEqual(res["exit"], 0, msg=res["stderr"][:800])
        self.assertEqual(res["leaked"], ["json"])
        self.assertEqual(res["blocked"], [])
        self.assertIs(res["cold_off"], False)
        self.assertEqual(res["state"], "LEAK_DETECTED")

    def test_03_cold_off_rejects_bad_module_names(self) -> None:
        with self.assertRaises(ValueError):
            oi.cold_off_probe("x", ["os; import sys"])
        with self.assertRaises(ValueError):
            oi.cold_off_probe("x", [])

    # -- 2) positive control ----------------------------------------------
    def test_04_positive_control_observes_import(self) -> None:
        res = oi.positive_control("json")
        self.assertEqual(res["module"], "json")
        self.assertEqual(res["exit"], 0, msg=res["stderr_sha256"])
        self.assertIs(res["imported"], True)
        self.assertEqual(res["state"], "OBSERVED")
        self.assertTrue(_is_hex64(res["stdout_sha256"]))
        self.assertTrue(_is_hex64(res["stderr_sha256"]))

    def test_05_positive_control_reports_a_missing_module(self) -> None:
        missing = "hgk_runtime_positive_control_absent"
        res = oi.positive_control(missing)
        self.assertEqual(res["exit"], 0)
        self.assertIs(res["imported"], False)
        self.assertEqual(res["state"], "CONTROL_FAILED")

    # -- 3) env flag is not evidence --------------------------------------
    def test_06_env_flag_only_reject_is_structured_and_touches_no_env(self) -> None:
        before = dict(os.environ)
        res = oi.env_flag_only_reject("W1_COLD_OFF=1")
        after = dict(os.environ)

        self.assertIs(res["rejected"], True)
        self.assertEqual(res["token"], "ENV_FLAG_NOT_EVIDENCE")
        self.assertEqual(res["marker"], "W1_COLD_OFF=1")
        self.assertEqual(res["evidence"], "none")
        self.assertIs(res["env_read"], False)
        self.assertIs(res["env_written"], False)
        self.assertEqual(before, after, "env_flag_only_reject must not touch os.environ")

    # -- 4) path attacks ---------------------------------------------------
    def test_07_path_attack_suite_rejects_all_seven(self) -> None:
        attacks = oi.path_attack_suite(self.pack)

        self.assertEqual(len(attacks), 7, msg=[a["attack"] for a in attacks])
        self.assertEqual(
            [a["attack_label"] for a in attacks],
            ["absolute", "unc", "drive_relative", "dotdot",
             "backslash", "nul", "empty"],
        )
        for entry in attacks:
            with self.subTest(attack=entry["attack"], label=entry["attack_label"]):
                self.assertIs(
                    entry["rejected"], True,
                    msg=f"NOT rejected: {entry!r}",
                )
                self.assertTrue(entry["token"], msg=f"no token: {entry!r}")
                self.assertNotEqual(entry["token"], "UNEXPECTED_EXCEPTION")

        # Attack values must be the real strings, including the NUL byte.
        by_label = {a["attack_label"]: a["attack"] for a in attacks}
        self.assertEqual(by_label["absolute"], "C:/x.md")
        self.assertEqual(by_label["unc"], "//srv/share/x.md")
        self.assertEqual(by_label["drive_relative"], "C:x.md")
        self.assertEqual(by_label["dotdot"], "..")
        self.assertEqual(by_label["backslash"], "a\\b.md")
        self.assertEqual(by_label["nul"], "a\x00b.md")
        self.assertEqual(by_label["empty"], "")

    # -- 5) link probe -----------------------------------------------------
    def test_08_link_probe_is_rejected_or_honestly_not_verified(self) -> None:
        target = os.path.join(self.pack, "00_W1_PI_PD.md")
        base = os.path.join(self.tmp, "links")
        res = oi.link_probe(base, target)

        self.assertIn(res["state"], {"REJECT", "NOT_VERIFIED"}, msg=repr(res))
        if res["state"] == "NOT_VERIFIED":
            self.assertIs(res["link_created"], False)
            self.assertIn("reason", res)
            self.assertIn("symlink", res["reason"].lower())
        else:
            self.assertIs(res["link_created"], True)
            self.assertTrue(res["token"], msg=repr(res))
            # At least one of the two gates must have refused the link.
            self.assertFalse(
                res["read_bounded_accepted"] is True
                and res["resolve_inside_accepted"] is True,
                msg=repr(res),
            )
            self.assertIn(res.get("stage"), {"read_bounded", "resolve_inside"})

    # -- 6) canary ---------------------------------------------------------
    def test_09_canary_reports_untouched_file_unchanged(self) -> None:
        target = os.path.join(self.pack, "00_W1_PI_PD.md")
        before = oi.snapshot([target])
        self.assertTrue(_is_hex64(before[target]["sha256"]))
        self.assertGreater(before[target]["bytes"], 0)

        res = oi.canary_check([target], before)
        self.assertIs(res["unchanged"], True, msg=res["diff"])
        self.assertEqual(res["diff"], [])
        self.assertEqual(res["checked"][0]["sha256"], before[target]["sha256"])

    def test_10_canary_detects_a_real_byte_change(self) -> None:
        """Negative control: the canary must not always say "unchanged"."""
        copy = os.path.join(self.tmp, "canary_copy.md")
        with open(copy, "wb") as fh:
            fh.write(b"alpha\n")
        before = oi.snapshot([copy])

        with open(copy, "ab") as fh:
            fh.write(b"beta\n")

        res = oi.canary_check([copy], before)
        self.assertIs(res["unchanged"], False)
        self.assertEqual(len(res["diff"]), 1)
        self.assertEqual(res["diff"][0]["path"], copy)
        self.assertIn("sha256_changed", res["diff"][0]["reason"])
        self.assertIn("bytes_changed", res["diff"][0]["reason"])

    def test_11_canary_flags_a_missing_file(self) -> None:
        ghost = os.path.join(self.tmp, "does_not_exist.md")
        before = {ghost: {"sha256": "0" * 64, "bytes": 1}}
        res = oi.canary_check([ghost], before)
        self.assertIs(res["unchanged"], False)
        self.assertEqual(res["diff"][0]["reason"], "unreadable_or_missing")


if __name__ == "__main__":
    unittest.main(verbosity=2)
