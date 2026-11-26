#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal W2 technical receiver (R06).

Consumes the frozen W1 delivery (not the maker's memory) from a clean root and
returns a receipt with accept/reject, next legal operation, stop and resume.

The receive path is split into three parts so that a rejected delivery can never
trigger a product call or a write:

  verify_delivery(delivery, pins)   pure, read/hash/parse only, short-circuits
  consume_verified(validated, out)  delayed product import, writes only to `out`
  receive(...)                      compatibility wrapper + receipt

The external pins are the only trust root.  A delivery that is consistent with
its own shipped seal is still rejected when it does not match the pins supplied
by the consumer.  It never issues a grant or performs a W2 protected effect.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

PACK_PIN = "61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a"
PIN_KEYS = ("evidence_manifest_sha256", "delivery_seal_sha256", "pack_manifest_sha256")
SCHEMA_MANIFEST = "FHS5.PLP.W1.EvidenceManifest@2"
SCHEMA_SEAL = "FHS5.PLP.W1.DeliverySeal@2"
SCHEMA_RECEIPT = "FHS5.PLP.W2.ReceiveReceipt@1"

# Fail-closed resource bounds.  They are deliberately generous for this corpus
# but stop a manifest or an entry from turning verification into an unbounded
# read.
MAX_MANIFEST_BYTES = 8 * 1024 * 1024
MAX_ENTRY_BYTES = 64 * 1024 * 1024
MAX_ENTRIES = 20000
MAX_PATH_CHARS = 512

_HEX64 = re.compile(r"\A[0-9a-fA-F]{64}\Z")
_DRIVE = re.compile(r"\A[A-Za-z]:")


class NFError(Exception):
    """Local mirror of w1_nf_reader.NFError(token, detail).

    Keeping it local means importing this module never imports product code.
    Product errors raised inside ``consume_verified`` are normalised to this
    class by ``_product_call``.
    """

    def __init__(self, token: str, detail: str = ""):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_digest(root: Path) -> str:
    """Order-stable digest of every regular file below *root* (read only)."""
    rows = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames):
            p = Path(dirpath) / name
            try:
                rel = p.relative_to(root).as_posix()
                if p.is_symlink():
                    rows.append(f"{rel}\0LINK:{os.readlink(p)}")
                    continue
                st = p.stat()
                if not p.is_file():
                    continue
                if st.st_size > MAX_ENTRY_BYTES:
                    rows.append(f"{rel}\0SIZE:{st.st_size}")
                else:
                    rows.append(f"{rel}\0{sha256_file(p)}")
            except OSError:
                rows.append(f"{p.as_posix()}\0UNREADABLE")
    return sha256_bytes("\n".join(rows).encode("utf-8"))


def _read_bounded(p: Path, limit: int):
    """Read at most *limit* bytes; return (data, size) or (None, size>limit)."""
    chunks = []
    total = 0
    with open(p, "rb") as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > limit:
                return None, total
            chunks.append(chunk)
    return b"".join(chunks), total


def _normalise_pins(expected_pins):
    """Return (pins, missing) with lowercase hex values; (None, missing) if bad."""
    if not isinstance(expected_pins, dict):
        return None, list(PIN_KEYS)
    missing = []
    pins = {}
    for key in PIN_KEYS:
        value = expected_pins.get(key)
        if not isinstance(value, str) or not _HEX64.match(value):
            missing.append(key)
        else:
            pins[key] = value.lower()
    if missing:
        return None, missing
    return pins, []


def _confine(root: Path, raw: str):
    """Return None when *raw* is a confined relative POSIX path, else a reason."""
    if not isinstance(raw, str) or not raw:
        return "empty or non-string path"
    if len(raw) > MAX_PATH_CHARS:
        return "path too long"
    if raw != raw.strip():
        return "leading/trailing whitespace"
    if "\\" in raw:
        return "backslash / UNC separator"
    if raw.startswith("/"):
        return "absolute path"
    if "\x00" in raw:
        return "NUL byte"
    if _DRIVE.match(raw):
        return "windows drive prefix"
    for seg in raw.split("/"):
        if seg in ("", ".", ".."):
            return "empty/dot/dotdot segment"
        if seg.endswith(" ") or seg.endswith("."):
            return "windows-truncated segment"
        if ":" in seg:
            return "alternate data stream"
        if any(ord(ch) < 32 for ch in seg):
            return "control character"
    try:
        real = (root / raw).resolve()
    except (OSError, RuntimeError) as exc:  # reparse loop / bad path
        return f"unresolvable path: {exc}"
    root_s = os.path.normcase(str(root))
    real_s = os.path.normcase(str(real))
    if real_s != root_s and not real_s.startswith(root_s + os.sep):
        return "resolves outside delivery_root"
    return None


def _is_within(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(str(child))
    parent_s = os.path.normcase(str(parent))
    return child_s == parent_s or child_s.startswith(parent_s + os.sep)


def _parse_json_bytes(raw: bytes):
    """Strict UTF-8 + JSON parse; return (obj, error).

    Rejects: invalid UTF-8, duplicate object keys, NaN/Infinity/-Infinity, BOM,
    and trailing content.  A duplicated key is how an attacker smuggles a second
    "sha256" past a first-wins reader, so it must be refused, not resolved.
    """
    if raw[:3] == b"\xef\xbb\xbf":
        return None, "BOM not allowed"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, f"not UTF-8: {exc}"

    duplicates = []

    def _pairs(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                duplicates.append(k)
            seen.add(k)
        return dict(pairs)

    def _const(name):
        raise ValueError(f"non-finite constant not allowed: {name}")

    try:
        obj = json.loads(text, object_pairs_hook=_pairs, parse_constant=_const)
    except (json.JSONDecodeError, ValueError) as exc:
        return None, f"not JSON: {exc}"
    if duplicates:
        return None, f"duplicate keys: {sorted(set(duplicates))[:5]}"
    return obj, None


def _check(checks, name, ok, detail):
    checks.append({"name": name, "check": name, "ok": bool(ok),
                   "detail": str(detail)[:300]})
    return bool(ok)


def _verify_result(checks, ok, first_fail, delivery_root, pins, manifest_sha,
                   verified, manifest=None, seal_sha=None, tree=None,
                   verified_paths=None):
    manifest = manifest or {}
    return {
        "schema": "FHS5.PLP.W2.DeliveryVerification@1",
        "ok": bool(ok),
        "first_fail": first_fail,
        "checks": checks,
        "check_count": len(checks),
        "delivery_root": str(delivery_root),
        "pins_used": dict(pins or {}),
        "manifest_sha256": manifest_sha,
        "delivery_seal_sha256": seal_sha,
        "delivery_tree_sha256": tree,
        "verified_entries": int(verified),
        "verified_paths": list(verified_paths or []),
        "manifest_subject_id": manifest.get("subject_id"),
        "manifest_scope": manifest.get("scope"),
        "manifest_run_id": manifest.get("run_id"),
        "manifest_pack_manifest_sha256": manifest.get("pack_manifest_sha256"),
        "seal_evidence_manifest_sha256": manifest.get("_seal_binding"),
        "permission_boundary": ("verify_delivery reads and hashes only; no product "
                                "import, no write, no grant"),
    }


def verify_delivery(delivery_root, expected_pins) -> dict:
    """Pure delivery verification.  Read/hash/parse only; short-circuits.

    Failure tokens: PINS_MISSING, ENTRY_MISSING, SCHEMA_INVALID,
    BYTES_MISMATCH, PATH_ESCAPE, ENTRY_TOO_LARGE.
    """
    checks = []
    try:
        d = Path(delivery_root).resolve()
    except OSError:
        d = Path(delivery_root).absolute()

    pins, missing = _normalise_pins(expected_pins)
    if pins is None:
        _check(checks, "pins_present", False, "missing/invalid: " + ", ".join(missing))
        return _verify_result(checks, False, "PINS_MISSING", d, {}, None, 0)
    _check(checks, "pins_present", True, ", ".join(sorted(pins)))

    if not d.is_dir():
        _check(checks, "delivery_root", False, "not a directory")
        return _verify_result(checks, False, "ENTRY_MISSING", d, pins, None, 0)

    man_p = d / "EVIDENCE_MANIFEST.json"
    seal_p = d / "DELIVERY_SEAL.json"
    if not man_p.is_file():
        _check(checks, "manifest_present", False, "EVIDENCE_MANIFEST.json missing")
        return _verify_result(checks, False, "ENTRY_MISSING", d, pins, None, 0)

    raw, size = _read_bounded(man_p, MAX_MANIFEST_BYTES)
    if raw is None:
        _check(checks, "manifest_size", False, f"{size} bytes > {MAX_MANIFEST_BYTES}")
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins, None, 0)
    manifest_sha = sha256_bytes(raw)
    if not _check(checks, "evidence_manifest_pin",
                  manifest_sha == pins["evidence_manifest_sha256"],
                  {"expected": pins["evidence_manifest_sha256"], "actual": manifest_sha}):
        return _verify_result(checks, False, "BYTES_MISMATCH", d, pins,
                              manifest_sha, 0)

    if not seal_p.is_file():
        _check(checks, "seal_present", False, "DELIVERY_SEAL.json missing")
        return _verify_result(checks, False, "ENTRY_MISSING", d, pins,
                              manifest_sha, 0)
    seal_raw, seal_size = _read_bounded(seal_p, MAX_MANIFEST_BYTES)
    if seal_raw is None:
        _check(checks, "seal_size", False, f"{seal_size} bytes")
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0)
    seal_sha = sha256_bytes(seal_raw)
    if not _check(checks, "delivery_seal_pin",
                  seal_sha == pins["delivery_seal_sha256"],
                  {"expected": pins["delivery_seal_sha256"], "actual": seal_sha}):
        return _verify_result(checks, False, "BYTES_MISMATCH", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)

    man, err = _parse_json_bytes(raw)
    if err is not None or not isinstance(man, dict):
        _check(checks, "manifest_parse", False, err or "not a JSON object")
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)
    _check(checks, "manifest_parse", True, "utf-8 json object")
    if not _check(checks, "manifest_schema", man.get("schema") == SCHEMA_MANIFEST,
                  man.get("schema")):
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)

    files = man.get("files")
    if not isinstance(files, list) or not files:
        _check(checks, "manifest_files", False, type(files).__name__)
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)
    if len(files) > MAX_ENTRIES:
        _check(checks, "manifest_files", False, f"{len(files)} entries")
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)

    seen = set()
    for idx, entry in enumerate(files):
        if not isinstance(entry, dict):
            _check(checks, "manifest_entry_schema", False, f"files[{idx}] not object")
            return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)
        path = entry.get("path")
        digest = entry.get("sha256")
        if not isinstance(path, str) or not isinstance(digest, str):
            _check(checks, "manifest_entry_schema", False,
                   f"files[{idx}] path/sha256 type")
            return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)
        if not _HEX64.match(digest):
            _check(checks, "manifest_entry_schema", False,
                   f"files[{idx}] sha256 not 64 hex")
            return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)
        key = os.path.normcase(path)
        if key in seen:
            _check(checks, "manifest_entry_schema", False,
                   f"duplicate path: {path}")
            return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)
        seen.add(key)
    _check(checks, "manifest_entry_schema", True, f"{len(files)} entries")

    claimed_pack = man.get("pack_manifest_sha256")
    if not isinstance(claimed_pack, str) or not _HEX64.match(claimed_pack):
        _check(checks, "manifest_pack_pin", False, "missing/invalid")
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)
    if not _check(checks, "manifest_pack_pin",
                  claimed_pack.lower() == pins["pack_manifest_sha256"],
                  {"expected": pins["pack_manifest_sha256"],
                   "claimed": claimed_pack.lower()}):
        return _verify_result(checks, False, "BYTES_MISMATCH", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)

    seal, err = _parse_json_bytes(seal_raw)
    if err is not None or not isinstance(seal, dict):
        _check(checks, "seal_parse", False, err or "not a JSON object")
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)
    _check(checks, "seal_parse", True, "utf-8 json object")
    if seal.get("schema") not in (None, SCHEMA_SEAL):
        _check(checks, "seal_schema", False, seal.get("schema"))
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)
    binding = seal.get("evidence_manifest_sha256")
    if not isinstance(binding, str) or not _HEX64.match(binding):
        _check(checks, "seal_manifest_binding", False, "missing/invalid")
        return _verify_result(checks, False, "SCHEMA_INVALID", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)
    if not _check(checks, "seal_manifest_binding",
                  binding.lower() == manifest_sha,
                  {"seal": binding.lower(), "recomputed": manifest_sha}):
        return _verify_result(checks, False, "BYTES_MISMATCH", d, pins,
                              manifest_sha, 0, seal_sha=seal_sha)
    seal_pack = seal.get("pack_manifest_sha256")
    if isinstance(seal_pack, str) and _HEX64.match(seal_pack):
        if not _check(checks, "seal_pack_pin",
                      seal_pack.lower() == pins["pack_manifest_sha256"],
                      {"seal": seal_pack.lower()}):
            return _verify_result(checks, False, "BYTES_MISMATCH", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)

    # Confinement is decided for every entry before any entry byte is read.
    targets = []
    for entry in files:
        reason = _confine(d, entry["path"])
        if reason is not None:
            _check(checks, "path_confinement", False,
                   f"{entry['path']!r}: {reason}")
            return _verify_result(checks, False, "PATH_ESCAPE", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)
        try:
            real = (d / entry["path"]).resolve()
        except (OSError, RuntimeError) as exc:
            _check(checks, "path_confinement", False,
                   f"{entry['path']!r}: unresolvable: {exc}")
            return _verify_result(checks, False, "PATH_ESCAPE", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)
        if not _is_within(real, d):
            _check(checks, "path_confinement", False,
                   f"{entry['path']!r}: resolves outside delivery_root")
            return _verify_result(checks, False, "PATH_ESCAPE", d, pins,
                                  manifest_sha, 0, seal_sha=seal_sha)
        targets.append((entry, real))
    _check(checks, "path_confinement", True, f"{len(files)} relative paths confined")

    verified_paths = []
    for entry, p in targets:
        if not p.is_file():
            _check(checks, "evidence_bytes", False,
                   f"missing: {entry['path']}")
            return _verify_result(checks, False, "ENTRY_MISSING", d, pins,
                                  manifest_sha, len(verified_paths),
                                  seal_sha=seal_sha, verified_paths=verified_paths)
        try:
            entry_size = p.stat().st_size
        except OSError as exc:
            _check(checks, "evidence_bytes", False,
                   f"stat failed: {entry['path']}: {exc}")
            return _verify_result(checks, False, "ENTRY_MISSING", d, pins,
                                  manifest_sha, len(verified_paths),
                                  seal_sha=seal_sha, verified_paths=verified_paths)
        if entry_size > MAX_ENTRY_BYTES:
            _check(checks, "evidence_bytes", False,
                   f"oversize: {entry['path']} ({entry_size} > {MAX_ENTRY_BYTES})")
            return _verify_result(checks, False, "ENTRY_TOO_LARGE", d, pins,
                                  manifest_sha, len(verified_paths),
                                  seal_sha=seal_sha, verified_paths=verified_paths)
        actual = sha256_file(p)
        if actual != entry["sha256"].lower():
            _check(checks, "evidence_bytes", False,
                   f"sha mismatch: {entry['path']}")
            return _verify_result(checks, False, "BYTES_MISMATCH", d, pins,
                                  manifest_sha, len(verified_paths),
                                  seal_sha=seal_sha, verified_paths=verified_paths)
        declared = entry.get("bytes")
        if isinstance(declared, int) and not isinstance(declared, bool):
            if declared != entry_size:
                _check(checks, "evidence_bytes", False,
                       f"byte count mismatch: {entry['path']}")
                return _verify_result(checks, False, "BYTES_MISMATCH", d, pins,
                                      manifest_sha, len(verified_paths),
                                      seal_sha=seal_sha, verified_paths=verified_paths)
        verified_paths.append(entry["path"])

    _check(checks, "evidence_bytes", True, f"{len(verified_paths)} entries recomputed")
    tree = tree_digest(d)
    _check(checks, "delivery_tree", True, tree)
    man["_seal_binding"] = binding.lower()
    return _verify_result(checks, True, None, d, pins, manifest_sha,
                          len(verified_paths), manifest=man, seal_sha=seal_sha,
                          tree=tree, verified_paths=verified_paths)


def _load_products():
    """Delayed product import; only reachable through consume_verified."""
    impl = Path(__file__).resolve().parent.parent / "impl"
    if str(impl) not in sys.path:
        sys.path.insert(0, str(impl))
    import nf_reader          # noqa: WPS433 (deliberate local import)
    import tpm_contracts_nf   # noqa: WPS433
    import w2_inbound         # noqa: WPS433
    return nf_reader, tpm_contracts_nf, w2_inbound


def _product_call(fn, *args, **kwargs):
    """Call a product function and normalise its NFError to our local class."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - token-preserving translation
        token = getattr(exc, "token", None)
        if token:
            raise NFError(str(token), str(getattr(exc, "detail", ""))) from exc
        raise


def consume_verified(validated, output_root) -> dict:
    """Consume a *verified* delivery.  Product calls happen only here.

    The W2 material is copied to ``<output_root>/material_copy`` first; the
    product seam wiring receives the copy, so the delivery tree is never a
    write target.
    """
    if not isinstance(validated, dict) or validated.get("ok") is not True:
        raise NFError("NOT_VERIFIED", "verify_delivery did not return ok=True")
    if not validated.get("pins_used"):
        raise NFError("NOT_VERIFIED", "pins_used missing")

    d = Path(validated["delivery_root"]).resolve()
    pins = dict(validated["pins_used"])
    out = Path(output_root).resolve() if output_root is not None else (
        Path.cwd() / "w2_receive_output").resolve()
    if _is_within(out, d):
        raise NFError("OUTPUT_ROOT_INVALID",
                      "output_root must not be inside the delivery tree")

    # TOCTOU: the bytes that were verified must still be the bytes on disk now.
    # Without this, a delivery can be verified clean and then swapped before the
    # product call, and consume_verified would still report ok.
    _man_p = d / "EVIDENCE_MANIFEST.json"
    _seal_p = d / "DELIVERY_SEAL.json"
    try:
        _now_manifest = sha256_file(_man_p)
        _now_seal = sha256_file(_seal_p)
    except OSError as exc:
        raise NFError("TOCTOU_UNREADABLE", str(exc)) from exc
    if _now_manifest != validated.get("manifest_sha256") \
            or _now_seal != validated.get("delivery_seal_sha256"):
        raise NFError("TOCTOU_DRIFT",
                      str({"manifest": [validated.get("manifest_sha256"), _now_manifest],
                           "seal": [validated.get("delivery_seal_sha256"), _now_seal]}))

    checks, rejected, reasons = [], [], []
    calls = {"build_contracts": 0, "seam_wiring": 0}
    first_fail = {"value": None}

    def chk(name, ok, detail, token=None):
        checks.append({"name": name, "check": name, "ok": bool(ok),
                       "detail": str(detail)[:300]})
        if not ok:
            rejected.append(name)
            reasons.append(f"{name}: {detail}")
            if first_fail["value"] is None:
                first_fail["value"] = token or name.upper()
        return bool(ok)

    def done(ok, **extra):
        result = {
            "ok": bool(ok),
            "accepted": bool(ok),
            "first_fail": first_fail["value"],
            "checks": checks,
            "check_count": len(checks),
            "rejected_checks": rejected,
            "reasons": reasons,
            "product_calls": dict(calls),
            "output_root": str(out),
            "material_copy": str(out / "material_copy"),
        }
        result.update(extra)
        return result

    # Re-check the pinned bytes at consume time (small TOCTOU window).
    man_p = d / "EVIDENCE_MANIFEST.json"
    seal_p = d / "DELIVERY_SEAL.json"
    try:
        man_sha = sha256_file(man_p)
        seal_sha = sha256_file(seal_p)
    except OSError as exc:
        chk("delivery_still_present", False, exc, "ENTRY_MISSING")
        return done(False)
    if not chk("delivery_still_present",
               man_sha == pins["evidence_manifest_sha256"]
               and seal_sha == pins["delivery_seal_sha256"],
               {"manifest": man_sha, "seal": seal_sha}, "DELIVERY_CHANGED"):
        return done(False)
    tree_before = tree_digest(d)
    if not chk("delivery_tree_before", tree_before == validated.get("delivery_tree_sha256"),
               tree_before, "DELIVERY_CHANGED"):
        return done(False)

    hand_p = d / "FHS-5_PLP_W1_HANDOFF.md"
    close_p = d / "FHS-5_PLP_W1_CLOSEOUT.md"
    cases_p = d / "evidence" / "cases.json"
    if not chk("delivery_files_present",
               all(p.is_file() for p in (hand_p, close_p, cases_p)),
               "handoff/closeout/cases", "ENTRY_MISSING"):
        return done(False)

    reader, tpm, w2i = _load_products()
    pack = d / "control_pack" / "FHS-5_PLP_W1_NATIVE_FIRST"

    insp = None
    try:
        insp = _product_call(reader.inspect_package, pack)
    except NFError as exc:
        chk("pack_inspect", False, f"{exc.token}:{exc.detail}", exc.token)
        return done(False)
    if not chk("pack_inspect", insp["pack_manifest_sha256"] == pins["pack_manifest_sha256"],
               insp["pack_manifest_sha256"], "PACK_PIN_MISMATCH"):
        return done(False)
    if not chk("pack_counts", insp["counts"] == {"pack_files": 5, "dev": 38, "ops": 29,
                                                 "cases": 13, "assets": 26, "sources": 42,
                                                 "holds": 14}, insp["counts"],
               "PACK_COUNT_MISMATCH"):
        return done(False)

    text = hand_p.read_text(encoding="utf-8")
    for token in ("subject_id", "scope", "pack_manifest_sha256", "entry", "bridge",
                  "guide", "tpm", "consumer", "runner", "next", "stop", "resume"):
        chk("handoff_field:" + token, token in text, token, "HANDOFF_INCOMPLETE")

    try:
        cases = json.loads(cases_p.read_text(encoding="utf-8"))
        verdicts = {c["case_id"]: c["verdict"] for c in cases["cases"]}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        chk("cases_present", False, exc, "SCHEMA_INVALID")
        verdicts, cases = {}, {}
    else:
        chk("cases_present", len(verdicts) >= 20, len(verdicts), "SCHEMA_INVALID")
        chk("host_consumed", verdicts.get("W1-HOST-01") == "PASS",
            verdicts.get("W1-HOST-01"), "HOST_NOT_CONSUMED")

    w2mat = d / "evidence" / "w2" / "material"
    if not chk("w2_material_present", w2mat.is_dir(), str(w2mat), "W2_MATERIAL_MISSING"):
        return done(False)
    copy = out / "material_copy"
    try:
        out.mkdir(parents=True, exist_ok=True)
        shutil.copytree(w2mat, copy, dirs_exist_ok=True)
    except OSError as exc:
        chk("material_copy", False, exc, "OUTPUT_WRITE_FAILED")
        return done(False)
    chk("material_copy", True, str(copy))

    w2_ident = {"project_id": "FHS-5_PLP",
                "subject_id": "FHS-5_PLP/W2/INBOUND_DRAFT",
                "scope": "W2-READ-01", "wave_id": "W2",
                "batch_id": "W2-IN-DRAFT-01", "work_id": "W2-RECEIVER"}
    calls["build_contracts"] += 1
    try:
        w2c = _product_call(tpm.build_contracts, str(copy), w2_ident)
    except NFError as exc:
        chk("w2_contracts", False, f"{exc.token}:{exc.detail}", exc.token)
        return done(False)
    chk("w2_contracts", len(w2c["views"]) == 5, list(w2c["views"]),
        "W2_CONTRACT_VIEWS")
    reqs = w2c["views"]["TQAEP"].get("requirements") or []
    chk("w2_requirements_13", len(reqs) == 13, len(reqs), "W2_REQUIREMENTS")

    calls["seam_wiring"] += 1
    try:
        wiring = _product_call(w2i.seam_wiring, pack, copy, d)
    except NFError as exc:
        chk("five_seam_wiring", False, f"{exc.token}:{exc.detail}", exc.token)
        return done(False)
    chk("five_seam_wiring", wiring["state"] == "COMPLETE",
        {"matched": wiring["matched"], "total": wiring["total"]}, "SEAM_WIRING")
    thin = d / "evidence" / "w2" / "thin_start.md"
    chk("thin_start_present", thin.is_file(), str(thin), "ENTRY_MISSING")

    tree_after = tree_digest(d)
    chk("delivery_tree_unchanged", tree_after == tree_before,
        {"before": tree_before, "after": tree_after}, "DELIVERY_MUTATED")

    next_op = ("W2-READ: build the 13-row Draft BindingRequest plan inside W2-READ-01; "
               "no grant, no protected effect")
    consumed = {
        "source_refs": len(insp["source_refs"]),
        "effect_constraints": {"permission_state": "NONE_GRANTED",
                               "unknown_effect": "FAIL_CLOSED"},
        "host_capability_ledger": "evidence/host/host_receipt.json",
        "context_sha256_source": "bridge_nf.render_agent_context",
        "change_cone": json.loads((d / "W1_CLOSURE_MATRIX.json").read_text(
            encoding="utf-8")).get("verdict_counts", {})
        if (d / "W1_CLOSURE_MATRIX.json").is_file() else {},
        "unresolved_refs": len(insp["unresolved_refs"]),
        "nine_keys": "guide_nf.produce_nine_keys",
    }
    return done(not rejected, insp=insp, cases=cases, verdicts=verdicts,
                next_operation=next_op if not rejected else None,
                consumed=consumed, wiring={"matched": wiring["matched"],
                                           "total": wiring["total"],
                                           "state": wiring["state"]},
                delivery_tree_sha256_before=tree_before,
                delivery_tree_sha256_after=tree_after,
                w2_task={"kind": "READ",
                         "action": "verify W1 candidate and select next op",
                         "readback": "all checks above",
                         "accepted": not rejected})


def _preflight(ident, validated):
    """Identity/scope checks that must reject before any product call."""
    checks, rejected, reasons = [], [], []
    fail = {"value": None}

    def chk(name, ok, detail, token):
        checks.append({"name": name, "check": name, "ok": bool(ok),
                       "detail": str(detail)[:300]})
        if not ok:
            rejected.append(name)
            reasons.append(f"{name}: {detail}")
            if fail["value"] is None:
                fail["value"] = token
        return bool(ok)

    state = ident.get("permission_state")
    chk("no_fake_grant", state in (None, "NONE_GRANTED"), state, "FAKE_GRANT")

    expected_pack = ident.get("expected_pack_sha256")
    pin_pack = validated["pins_used"]["pack_manifest_sha256"]
    chk("caller_pack_pin",
        expected_pack is None or str(expected_pack).lower() == pin_pack,
        expected_pack, "PACK_PIN_MISMATCH")

    producer = ident.get("producer_identity")
    consumer = ident.get("consumer_identity")
    chk("identity_split", bool(producer) and bool(consumer) and producer != consumer,
        {"producer": producer, "consumer": consumer}, "IDENTITY_MISMATCH")
    chk("subject_identity",
        bool(producer) and producer == validated.get("manifest_subject_id"),
        {"producer": producer, "manifest": validated.get("manifest_subject_id")},
        "IDENTITY_MISMATCH")

    hand_p = Path(validated["delivery_root"]) / "FHS-5_PLP_W1_HANDOFF.md"
    try:
        hand = hand_p.read_text(encoding="utf-8")
    except OSError as exc:
        chk("handoff_scope", False, exc, "ENTRY_MISSING")
    else:
        # exact field match, not a substring test: "W1-NF-01" must not be
        # satisfied by "W1-NF-011" or by the phrase inside prose
        scope = ident.get("scope")
        import re as _re
        field = None
        for line in hand.splitlines():
            m = _re.match(r"^\s*(?:[-*]\s*)?scope\s*[:=]\s*(.+?)\s*$", line)
            if m:
                field = m.group(1).strip().strip("`").strip()
                break
        chk("handoff_scope",
            field is not None and scope is not None and field == scope,
            {"field": field, "requested": scope}, "SCOPE_MISMATCH")
    return checks, rejected, reasons, fail["value"]


def _coerce_pins(expected_pins):
    if isinstance(expected_pins, dict):
        return expected_pins
    if isinstance(expected_pins, (str, os.PathLike)):
        try:
            return json.loads(Path(expected_pins).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
    return None


def _receipt(ident, rejected, reasons, checks, insp, cases, *, first_fail=None,
             verified=0, product_calls=None, pins=None, manifest_sha=None,
             validated=None, consumed=None, extra=None):
    receipt = {
        "schema": SCHEMA_RECEIPT,
        "receiver": "w2_receiver (independent)",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "w2_identity": ident,
        "accepted": not rejected,
        "first_fail": first_fail,
        "rejected_checks": rejected,
        "reasons": reasons,
        "checks": checks,
        "check_count": len(checks),
        "permission_boundary": ("W2 receives evidence only; no grant issued, "
                                "no protected effect"),
        "pack_manifest_sha256": (insp or {}).get("pack_manifest_sha256"),
        "w1_claim_seen": "W1_PARTIAL_VALIDATED" if any(
            "W1_PARTIAL_VALIDATED" in str(r) for r in reasons) else "see CLOSEOUT",
        "verified_entries": int(verified),
        "product_calls": dict(product_calls or {"build_contracts": 0,
                                               "seam_wiring": 0}),
        "pins_used": dict(pins or {}),
        "manifest_sha256": manifest_sha,
        "delivery_root": (validated or {}).get("delivery_root"),
        "delivery_tree_sha256": (validated or {}).get("delivery_tree_sha256"),
        "consume_performed": consumed is not None,
        "receipt_excluded_from_manifest": True,
        "stop": ("wrong candidate/pack/oracle/evidence/handoff/scope, missing pins, "
                 "path escape, or any fake grant"),
        "resume": ("same subject+scope+pack pin typed receipt; pins supplied "
                   "externally; re-verify ACL/principal"),
    }
    if validated is not None:
        receipt["manifest_sha256_at_receive"] = validated.get("manifest_sha256")
        receipt["seal_evidence_manifest_sha256_at_receive"] = validated.get(
            "seal_evidence_manifest_sha256")
    if consumed is not None:
        receipt["consumed"] = consumed
    if extra:
        receipt.update(extra)
    return receipt


def receive(delivery, w2_identity, expected_pins=None, output_root=None) -> dict:
    """Compatibility wrapper: verify first, consume only when verified."""
    ident = dict(w2_identity or {})
    pins = _coerce_pins(expected_pins)
    validated = verify_delivery(delivery, pins)
    checks = list(validated["checks"])
    rejected = [c["name"] for c in validated["checks"] if not c["ok"]]
    reasons = [f"{c['name']}: {c['detail']}" for c in validated["checks"] if not c["ok"]]

    if not validated["ok"]:
        return _receipt(ident, rejected, reasons, checks, None, None,
                        first_fail=validated["first_fail"],
                        verified=validated["verified_entries"],
                        product_calls={"build_contracts": 0, "seam_wiring": 0},
                        pins=validated["pins_used"],
                        manifest_sha=validated["manifest_sha256"],
                        validated=validated,
                        extra={"next_operation": None,
                               "w2_task": {"kind": "READ",
                                           "action": "reject delivery",
                                           "readback": "verify_delivery checks",
                                           "accepted": False},
                               "verified_paths": validated["verified_paths"]})

    pre_checks, pre_rejected, pre_reasons, pre_fail = _preflight(ident, validated)
    checks.extend(pre_checks)
    rejected.extend(pre_rejected)
    reasons.extend(pre_reasons)
    if pre_rejected:
        return _receipt(ident, rejected, reasons, checks, None, None,
                        first_fail=pre_fail,
                        verified=validated["verified_entries"],
                        product_calls={"build_contracts": 0, "seam_wiring": 0},
                        pins=validated["pins_used"],
                        manifest_sha=validated["manifest_sha256"],
                        validated=validated,
                        extra={"next_operation": None,
                               "w2_task": {"kind": "READ",
                                           "action": "reject identity/scope",
                                           "readback": "preflight checks",
                                           "accepted": False},
                               "verified_paths": validated["verified_paths"]})

    try:
        consumed = consume_verified(validated, output_root)
    except NFError as exc:
        return _receipt(ident, rejected + [exc.token], reasons + [str(exc)],
                        checks, None, None,
                        first_fail=exc.token,
                        verified=validated["verified_entries"],
                        product_calls={"build_contracts": 0, "seam_wiring": 0},
                        pins=validated["pins_used"],
                        manifest_sha=validated["manifest_sha256"],
                        validated=validated,
                        extra={"next_operation": None,
                               "w2_task": {"kind": "READ",
                                           "action": "reject before consume",
                                           "readback": str(exc),
                                           "accepted": False},
                               "verified_paths": validated["verified_paths"]})
    checks.extend(consumed["checks"])
    rejected = [c["name"] for c in checks if not c["ok"]]
    reasons = [f"{c['name']}: {c['detail']}" for c in checks if not c["ok"]]
    first_fail = validated["first_fail"] if not validated["ok"] else consumed["first_fail"]
    return _receipt(ident, rejected, reasons, checks, consumed.get("insp"), None,
                    first_fail=first_fail,
                    verified=validated["verified_entries"],
                    product_calls=consumed["product_calls"],
                    pins=validated["pins_used"],
                    manifest_sha=validated["manifest_sha256"],
                    validated=validated,
                    consumed=consumed.get("consumed"),
                    extra={"next_operation": consumed.get("next_operation"),
                           "w2_task": consumed.get("w2_task"),
                           "verified_paths": validated["verified_paths"],
                           "material_copy": consumed.get("material_copy"),
                           "output_root": consumed.get("output_root"),
                           "delivery_tree_sha256_after": consumed.get(
                               "delivery_tree_sha256_after"),
                           "w2_wiring": consumed.get("wiring")})


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--delivery", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scope", default="W1-NF-01")
    ap.add_argument("--expect-pack-sha", default=None)
    ap.add_argument("--pins", default=None,
                    help="external pins json with evidence_manifest_sha256, "
                         "delivery_seal_sha256, pack_manifest_sha256")
    ap.add_argument("--output-root", default=None,
                    help="write root for the material copy; never the delivery")
    args = ap.parse_args(argv)

    pins = None
    if args.pins:
        try:
            pins = json.loads(Path(args.pins).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pins = None  # fail closed, never fall back to the shipped seal
    ident = {"subject_id": "FHS-5_PLP/W1/CONTROL_PACK", "scope": args.scope,
             "permission_state": "NONE_GRANTED",
             "producer_identity": "FHS-5_PLP/W1/CONTROL_PACK",
             "consumer_identity": "FHS-5_PLP/W2/CONSUMER",
             "expected_pack_sha256": args.expect_pack_sha}
    out = Path(args.out)
    out_root = Path(args.output_root) if args.output_root else (
        out.resolve().parent / (out.stem + "_artifacts"))
    r = receive(Path(args.delivery), ident, pins, out_root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"accepted": r["accepted"], "first_fail": r["first_fail"],
                      "checks": r["check_count"],
                      "rejected": r["rejected_checks"][:5],
                      "product_calls": r["product_calls"],
                      "next": r.get("next_operation")}, ensure_ascii=False))
    return 0 if r["accepted"] else 5


if __name__ == "__main__":
    raise SystemExit(main())
