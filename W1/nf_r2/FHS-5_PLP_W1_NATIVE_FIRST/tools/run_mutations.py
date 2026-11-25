#!/usr/bin/env python3
"""Isolated mutation suite for the W1 NF pack guard.

Copies the delivery tree to a temp directory, applies one mutation per run,
and asserts that nf_pack_guard rejects with an expected token. The real pack
is never modified.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

PACK = "FHS-5_PLP_W1_NATIVE_FIRST"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def info(p):
    b = open(p, "rb").read()
    return len(b), sha(b), len(b.decode("utf-8").splitlines())


def reseal(pack, seal):
    mp = os.path.join(pack, "05_W1_SOURCE_MANIFEST.json")
    m = json.load(open(mp, encoding="utf-8"))
    for e in m["pack_files"]:
        b, h, n = info(os.path.join(pack, e["path"]))
        e.update(bytes=b, sha256=h, lines=n)
    open(mp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    raw = open(mp, "rb").read()
    s = json.load(open(seal, encoding="utf-8"))
    s["pack_manifest_sha256"] = sha(raw)
    s["pack_files"] = [{"path": e["path"], "sha256": e["sha256"], "bytes": e["bytes"], "lines": e["lines"]} for e in m["pack_files"]]
    open(seal, "w", encoding="utf-8", newline="\n").write(
        json.dumps(s, ensure_ascii=False, indent=2) + "\n")


def run_guard(pack, seal):
    p = subprocess.run([sys.executable, os.path.join(pack, "tools", "nf_pack_guard.py"),
                        "verify", "--root", pack, "--seal", seal],
                       capture_output=True, text=True, encoding="utf-8")
    try:
        out = json.loads(p.stdout)
    except Exception:
        out = {"result": "PARSE_FAIL", "stdout": p.stdout, "stderr": p.stderr}
    return p.returncode, out


def mutate(name, fn, expected, reseal_after=True):
    with tempfile.TemporaryDirectory() as td:
        src = os.path.dirname(os.path.abspath(__file__))
        src = os.path.dirname(os.path.dirname(src))  # delivery root
        dst = os.path.join(td, "delivery")
        shutil.copytree(src, dst)
        pack = os.path.join(dst, PACK)
        seal = os.path.join(dst, "evidence", "SEAL.json")
        fn(pack, seal)
        if reseal_after:
            reseal(pack, seal)
        rc, out = run_guard(pack, seal)
        tok = out.get("token")
        ok = rc != 0 and tok in expected
        print(f"{'PASS' if ok else 'FAIL'} {name}: rc={rc} token={tok} expected={sorted(expected)}")
        if not ok:
            print(json.dumps(out, ensure_ascii=False)[:800])
        return ok


def main():
    results = []

    def flip(pack, seal):
        p = os.path.join(pack, "00_W1_PI_PD.md")
        b = open(p, "rb").read()
        open(p, "wb").write(b + b"X")
    results.append(mutate("byte_flip_00", flip, {"DIGEST_MISMATCH"}, reseal_after=False))

    def crlf(pack, seal):
        p = os.path.join(pack, "01_W1_DEV_ECP.md")
        b = open(p, "rb").read().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        open(p, "wb").write(b)
    results.append(mutate("crlf_01", crlf, {"EOL_NON_CANONICAL", "DIGEST_MISMATCH"}))

    def delete(pack, seal):
        os.remove(os.path.join(pack, "03_W1_TQAEP.md"))
    results.append(mutate("delete_03", delete, {"PACK_INCOMPLETE_LOCAL"}, reseal_after=False))

    def dupkey(pack, seal):
        p = os.path.join(pack, "05_W1_SOURCE_MANIFEST.json")
        t = open(p, encoding="utf-8").read()
        t = t.replace('"schema":', '"schema": "X",\n  "schema":', 1)
        open(p, "w", encoding="utf-8", newline="\n").write(t)
    results.append(mutate("duplicate_json_key", dupkey, {"STRICT_JSON_REJECT"}, reseal_after=False))

    def nan(pack, seal):
        p = os.path.join(pack, "05_W1_SOURCE_MANIFEST.json")
        t = open(p, encoding="utf-8").read()
        t = t.replace('"profile":', '"bad": NaN,\n  "profile":', 1)
        open(p, "w", encoding="utf-8", newline="\n").write(t)
    results.append(mutate("nan_value", nan, {"STRICT_JSON_REJECT"}, reseal_after=False))

    def escape(pack, seal):
        p = os.path.join(pack, "05_W1_SOURCE_MANIFEST.json")
        m = json.load(open(p, encoding="utf-8"))
        m["pack_files"][0]["path"] = "../evil.md"
        open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    results.append(mutate("path_traversal", escape, {"PATH_OUTSIDE_ROOT", "PACK_INCOMPLETE_LOCAL"}, reseal_after=False))

    def identity(pack, seal):
        p = os.path.join(pack, "02_W1_OPS_ECP.md")
        t = open(p, encoding="utf-8").read()
        t = t.replace("**project_id**：`FHS-5_PLP`", "**project_id**：`FHS-5_XXX`", 1)
        open(p, "w", encoding="utf-8", newline="\n").write(t)
    results.append(mutate("identity_mismatch", identity, {"IDENTITY_MISMATCH"}))

    def drop_dev(pack, seal):
        p = os.path.join(pack, "01_W1_DEV_ECP.md")
        lines = open(p, encoding="utf-8").read().splitlines()
        out, dropped = [], False
        for ln in lines:
            if not dropped and ln.startswith("| `DEV-PERM-01`"):
                dropped = True
                continue
            out.append(ln)
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    results.append(mutate("drop_dev_id", drop_dev, {"ID_SET_INCOMPLETE"}))

    def dag_cycle(pack, seal):
        p = os.path.join(pack, "05_W1_SOURCE_MANIFEST.json")
        m = json.load(open(p, encoding="utf-8"))
        m["dag"]["edges"].append(["P06", "P01"])
        open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    results.append(mutate("dag_cycle", dag_cycle, {"DAG_CYCLE"}))

    def self_embed(pack, seal):
        p = os.path.join(pack, "05_W1_SOURCE_MANIFEST.json")
        m = json.load(open(p, encoding="utf-8"))
        m["pack_manifest_sha256"] = "0" * 64
        open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    results.append(mutate("manifest_self_embed", self_embed, {"MANIFEST_SELF_EMBED"}, reseal_after=False))

    def asset_flip(pack, seal):
        p = os.path.join(pack, "assets", "fixtures", "W1-HOST-01.json")
        b = open(p, "rb").read()
        open(p, "wb").write(b + b" ")
    results.append(mutate("asset_byte_flip", asset_flip, {"ASSET_DIGEST_MISMATCH"}))

    def upstream_pin(pack, seal):
        p = os.path.join(pack, "05_W1_SOURCE_MANIFEST.json")
        m = json.load(open(p, encoding="utf-8"))
        m["upstream_handoff"]["pack_sha256"] = "0" * 64
        open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    results.append(mutate("upstream_pin_mismatch", upstream_pin, {"UPSTREAM_PIN_MISMATCH"}))

    print(json.dumps({"suite": "W1_NF_MUTATIONS", "total": len(results),
                      "passed": sum(results), "result": "PASS" if all(results) else "FAIL"},
                     ensure_ascii=False))
    return 0 if all(results) else 2


if __name__ == "__main__":
    sys.exit(main())
