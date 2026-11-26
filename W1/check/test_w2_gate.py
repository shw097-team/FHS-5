#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generation-2 gate tests (F1): READ cannot write, patch structure, recovery,
trust overrides, fake receipts, and a positive apply/reverse cycle."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import w2_admission as A  # noqa: E402
import w2_dev_gate as G  # noqa: E402

F1 = "W1/check/a.py"
F2 = "W1/check/b.py"


def two_file_patch():
    return (
        f"diff --git a/{F1} b/{F1}\n--- a/{F1}\n+++ b/{F1}\n"
        "@@ -1 +1 @@\n-one\n+ONE\n"
        f"diff --git a/{F2} b/{F2}\n--- a/{F2}\n+++ b/{F2}\n"
        "@@ -1 +1 @@\n-two\n+TWO\n"
    )


@unittest.skipUnless(os.environ.get("W2_DECISION_PATH"), "no pinned decision")
class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gate_"))
        self.repo = self.tmp / "world"
        (self.repo / "W1" / "check").mkdir(parents=True)
        (self.repo / F1).write_bytes(b"one\n")
        (self.repo / F2).write_bytes(b"two\n")
        for cmd in (["init", "-q"], ["config", "user.name", "t"],
                    ["config", "user.email", "t@t"], ["add", "-A"],
                    ["commit", "-qm", "base"]):
            subprocess.run(["git", "-C", str(self.repo), *cmd], check=True,
                           capture_output=True)
        self.head = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"],
                                   capture_output=True, text=True).stdout.strip()
        self._saved = (A.WRITE_ROOT, A.ALLOWED_OPS)
        A.WRITE_ROOT = str(self.repo)
        A.ALLOWED_OPS = ((F1, "MODIFY"), (F2, "MODIFY"))
        self.ws = [{"path": F1, "operation": "MODIFY",
                    "preimage_sha256": G.sha256_file(self.repo / F1)},
                   {"path": F2, "operation": "MODIFY",
                    "preimage_sha256": G.sha256_file(self.repo / F2)}]

    def tearDown(self):
        A.WRITE_ROOT, A.ALLOWED_OPS = self._saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    def asserted(self, **kw):
        rec = A.derive("DEV", "W2-NF-01", self.repo, self.ws)
        base = {"effect": "REPOSITORY_WRITE", "scope": "W2-NF-01",
                "head": self.head, "admission": rec,
                "recovery": {"kind": "REVERSE_PATCH_ON_COPY"}}
        base.update(kw)
        return base

    def bytes_of(self, rel):
        return (self.repo / rel).read_bytes()

    # F1-a: a READ decision must never reach the writer
    def test_read_only_cannot_write(self):
        d = G.check(self.asserted(effect="REPOSITORY_READ"), self.repo, self.ws)
        self.assertFalse(d["writes_allowed"])
        before = self.bytes_of(F1)
        r = G.apply_patch(self.asserted(effect="REPOSITORY_READ"), self.repo,
                          self.ws, two_file_patch())
        self.assertFalse(r["ok"])
        self.assertEqual(r["first_fail"], "WRITE_NOT_AUTHORISED")
        self.assertEqual(r["wrote"], [])
        self.assertEqual(self.bytes_of(F1), before)

    # F1-b: recovery must be present and known
    def test_missing_recovery_refused(self):
        a = self.asserted()
        a.pop("recovery")
        d = G.check(a, self.repo, self.ws)
        self.assertFalse(d["ok"])
        self.assertEqual(d["first_fail"], "RECOVERY_KIND_MISMATCH")
        self.assertEqual(G.apply_patch(a, self.repo, self.ws, two_file_patch())["wrote"], [])

    def test_unknown_recovery_refused(self):
        a = self.asserted(recovery={"kind": "MAGIC_RESTORE"})
        d = G.check(a, self.repo, self.ws)
        self.assertEqual(d["first_fail"], "RECOVERY_KIND_MISMATCH")

    def test_git_recovery_refused(self):
        a = self.asserted(recovery={"kind": "GIT_RESET"})
        self.assertEqual(G.check(a, self.repo, self.ws)["first_fail"],
                         "RECOVERY_KIND_MISMATCH")

    # F1-c: patch structure cannot smuggle a rename or a foreign section
    def test_rename_escape_refused(self):
        p = (f"diff --git a/{F1} b/OUTSIDE.py\nrename from {F1}\n"
             f"rename to OUTSIDE.py\n--- a/{F1}\n+++ b/OUTSIDE.py\n"
             "@@ -1 +1 @@\n-one\n+ONE\n")
        r = G.apply_patch(self.asserted(), self.repo, self.ws, p)
        self.assertFalse(r["ok"])
        self.assertIn(r["first_fail"], ("PATCH_OP_UNSUPPORTED", "WRITE_SET_UNBOUND"))
        self.assertFalse((self.repo / "OUTSIDE.py").exists())

    def test_a_b_path_mismatch_refused(self):
        p = (f"diff --git a/{F1} b/{F1}\n--- a/{F2}\n+++ b/{F1}\n"
             "@@ -1 +1 @@\n-two\n+ONE\n")
        r = G.apply_patch(self.asserted(), self.repo, self.ws, p)
        self.assertFalse(r["ok"])
        self.assertEqual(r["first_fail"], "PATCH_PATH_MISMATCH")

    def test_extra_section_refused(self):
        p = two_file_patch() + (
            "diff --git a/extra.txt b/extra.txt\n--- a/extra.txt\n+++ b/extra.txt\n"
            "@@ -1 +1 @@\n-x\n+y\n")
        r = G.apply_patch(self.asserted(), self.repo, self.ws, p)
        self.assertEqual(r["first_fail"], "WRITE_SET_UNBOUND")

    # F1-d: trust overrides and forged receipts
    def test_trust_override_rejected(self):
        with self.assertRaises(A.AdmissionError) as ctx:
            A.derive("DEV", "W2-NF-01", self.repo, self.ws,
                     request={"write_root": str(self.tmp)})
        self.assertEqual(ctx.exception.token, "TRUST_OVERRIDE_REJECTED")

    def test_wrong_scope_and_domain(self):
        with self.assertRaises(A.AdmissionError) as ctx:
            A.derive("DEV", "W2-NF-02", self.repo, self.ws)
        self.assertEqual(ctx.exception.token, "SCOPE_MISMATCH")
        with self.assertRaises(A.AdmissionError) as ctx:
            A.derive("OPS", "W2-NF-01", self.repo, self.ws)
        self.assertEqual(ctx.exception.token, "PRINCIPAL_DOMAIN_MISMATCH")

    def test_forged_receipt_rejected(self):
        a = self.asserted()
        a["admission"] = json.loads(json.dumps(a["admission"]))
        a["admission"]["fields"]["targets"] = ["W1/check/evil.py:MODIFY"]
        self.assertEqual(G.check(a, self.repo, self.ws)["first_fail"],
                         "FALSE_AUTHORITY")

    def test_subset_write_set_refused(self):
        with self.assertRaises(A.AdmissionError) as ctx:
            A.derive("DEV", "W2-NF-01", self.repo, self.ws[:1])
        self.assertEqual(ctx.exception.token, "WRITE_SET_UNBOUND")

    # F1-e: the positive control
    def test_positive_apply_then_reverse(self):
        a = self.asserted()
        pre = {e["path"]: e["preimage_sha256"] for e in self.ws}
        r = G.apply_patch(a, self.repo, self.ws, two_file_patch())
        self.assertTrue(r["ok"], r["first_fail"])
        self.assertEqual(len(r["wrote"]), 2)
        self.assertEqual(self.bytes_of(F1), b"ONE\n")
        rev = G.reverse(two_file_patch(), self.repo, self.ws, pre)
        self.assertTrue(rev["ok"], rev.get("first_fail"))
        # reverse proves restorability on a copy; the repo itself is restored
        # by the caller (the world-restore step), not by reverse().
        self.assertEqual(rev["restored"][F1], pre[F1])
        self.assertEqual(self.bytes_of(F1), b"ONE\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
