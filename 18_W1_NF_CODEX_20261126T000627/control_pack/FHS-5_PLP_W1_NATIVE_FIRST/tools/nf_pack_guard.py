#!/usr/bin/env python3
"""FHS-5 PLP W1 NF pack guard.

Read-only verifier for the six-file W1 control pack. It is a test asset,
not a seventh normative document.

Usage:
  python tools/nf_pack_guard.py verify --root <pack_root> [--seal <seal.json>] [--json-out <file>]

Exit 0 only when every required check passes. Exit 2 on any reject.
"""
import argparse
import hashlib
import json
import os
import re
import sys

SCHEMA = "FHS5.PLP.W1.SourceManifest.NF@1"
PACK_VERSION = "W1-NF-r2-CODEX-PRIMARY"
PACK_NAMES = [
    "00_W1_PI_PD.md",
    "01_W1_DEV_ECP.md",
    "02_W1_OPS_ECP.md",
    "03_W1_TQAEP.md",
    "04_W1_START_THIN_PROMPT.md",
]
MANIFEST = "05_W1_SOURCE_MANIFEST.json"
IDENT = {
    "project_id": "FHS-5_PLP",
    "subject_id": "FHS-5_PLP/W1/CONTROL_PACK",
    "scope": "W1-NF-01",
    "wave_id": "W1",
    "batch_id": "W1-NF-01",
}
CASES = [
    "W1-HOST-01", "W1-HOST-02", "W1-HOST-03", "W1-HERMES-01",
    "W1-ABI-01", "W1-ABI-02", "W1-SEC-01", "W1-API-01",
    "W1-R3-01", "W1-R3-02", "W1-R3-03", "W1-R3-04", "W1-R3-05",
]
HOLDS = [
    "W1_HOST_NINE_GRID", "W1_PLUGIN_ALIAS", "W1_ABI_BOUND", "W1_W0_INPUT",
    "W0_PRIMARY_RECEIPT_STALE", "W0-A_CASE_SELECTION", "W0-B_NOT_ADMITTED",
    "ORIGINAL_READER_UNBOUND", "ORACLE_FIXTURE_UNBOUND",
    "HOST_CAPABILITY_UNBOUND", "CHECKER_PUBLISHER_UNBOUND",
    "SOURCE_REFERENCE_HASH_CONFLICT", "W0C_DENOMINATOR_ID_LIST_UNBOUND",
    "HOLD_CR-DOC04-STATE-MAP",
]


class Reject(Exception):
    def __init__(self, token, detail):
        super().__init__(f"{token}: {detail}")
        self.token = token
        self.detail = detail


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def file_info(path):
    b = read_bytes(path)
    return {"bytes": len(b), "sha256": sha_bytes(b), "lines": len(b.decode("utf-8").splitlines())}


def strict_json(path):
    duplicates = []

    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                duplicates.append(k)
            seen.add(k)
        return dict(pairs)

    def bad_const(x):
        raise Reject("STRICT_JSON_REJECT", f"non-finite constant {x}")

    raw = read_bytes(path)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise Reject("STRICT_JSON_REJECT", f"invalid UTF-8: {e}")
    try:
        obj = json.loads(text, object_pairs_hook=hook, parse_constant=bad_const)
    except Reject:
        raise
    except Exception as e:
        raise Reject("STRICT_JSON_REJECT", f"parse error: {e}")
    if duplicates:
        raise Reject("STRICT_JSON_REJECT", f"duplicate keys: {sorted(set(duplicates))}")
    return obj, raw


def hexn(s, n):
    return isinstance(s, str) and len(s) == n and all(c in "0123456789abcdef" for c in s.lower())


def inside(root, path):
    r = os.path.realpath(root)
    p = os.path.realpath(path)
    try:
        return os.path.commonpath([r, p]) == r
    except ValueError:
        return False


def parse_ids(text, prefix, two_parts=True):
    if two_parts:
        pat = rf"`({prefix}-[A-Z]+-\d{{2}})`"
    else:
        pat = rf"`({prefix}-\d{{2}})`"
    return sorted(set(re.findall(pat, text)))


def topo(nodes, edges):
    n = set(nodes)
    for a, b in edges:
        if a not in n or b not in n:
            raise Reject("DAG_NODE_UNKNOWN", f"{a}->{b}")
    indeg = {x: 0 for x in n}
    adj = {x: [] for x in n}
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    q = [x for x in nodes if indeg[x] == 0]
    out = []
    while q:
        x = q.pop(0)
        out.append(x)
        for y in adj[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                q.append(y)
    if len(out) != len(nodes):
        raise Reject("DAG_CYCLE", "topological sort incomplete")
    return out


def verify(root, seal_path=None):
    root = os.path.abspath(root)
    report = {"root": root, "checks": [], "rejects": []}

    def ok(name, detail=""):
        report["checks"].append({"check": name, "result": "PASS", "detail": detail})

    if not os.path.isdir(root):
        raise Reject("ROOT_MISSING", root)

    entries = sorted(os.listdir(root))
    allowed_root = set(PACK_NAMES + [MANIFEST, "assets", "tools"])
    extra = [e for e in entries if e not in allowed_root]
    if extra:
        raise Reject("PACK_EXTRA_FILE", str(extra))
    for d in ("assets", "tools"):
        if not os.path.isdir(os.path.join(root, d)):
            raise Reject("PACK_DIR_MISSING", d)
    ok("pack_root_layout", "5 MD + 05 + assets/ + tools/ only")

    mp = os.path.join(root, MANIFEST)
    if not os.path.isfile(mp):
        raise Reject("PACK_INCOMPLETE_LOCAL", MANIFEST)
    m, mraw = strict_json(mp)
    if m.get("schema") != SCHEMA:
        raise Reject("SCHEMA_UNSUPPORTED", str(m.get("schema")))
    if m.get("pack_version") != PACK_VERSION:
        raise Reject("VERSION_MISMATCH", str(m.get("pack_version")))
    for k, v in IDENT.items():
        if m.get(k) != v:
            raise Reject("IDENTITY_MISMATCH", f"{k}={m.get(k)!r} expected {v!r}")
    ok("manifest_schema_identity", SCHEMA)

    if m.get("claim_ceiling") != "W1_PACK_PRIMARY_AUTHORIZED_FOR_SCOPED_CONSTRUCTION":
        raise Reject("CLAIM_MISMATCH", str(m.get("claim_ceiling")))
    nc = m.get("not_claimed") or []
    for need in ("W1_NF_VALIDATED", "NATIVE_PASS", "INDEPENDENT_PASS", "RELEASED"):
        if need not in nc:
            raise Reject("CLAIM_MISMATCH", f"not_claimed missing {need}")
    er = (m.get("readiness") or {}).get("w1_execution_ready")
    claimed = m.get("claimed_now") or []
    if er == "READY":
        if "W1_EXECUTION_READY" not in claimed:
            raise Reject("CLAIM_MISMATCH", "W1_EXECUTION_READY READY but not in claimed_now")
        ev = (m.get("readiness") or {}).get("w1_execution_ready_evidence") or {}
        for k in ("worktree", "branch", "entry", "tests", "first_operation_raw", "acl"):
            if not ev.get(k):
                raise Reject("EXECUTION_READY_EVIDENCE_MISSING", k)
    elif "W1_EXECUTION_READY" not in nc:
        raise Reject("CLAIM_MISMATCH", "W1_EXECUTION_READY neither READY nor not_claimed")

    pfs = m.get("pack_files")
    if not isinstance(pfs, list) or [p.get("path") for p in pfs] != PACK_NAMES:
        raise Reject("PACK_INCOMPLETE_LOCAL", "pack_files must list exactly the five MD in canonical order")
    texts = {}
    infos = {}
    for p in pfs:
        name = p["path"]
        path = os.path.join(root, name)
        if not os.path.isfile(path):
            raise Reject("PACK_INCOMPLETE_LOCAL", name)
        if not inside(root, path):
            raise Reject("PATH_OUTSIDE_ROOT", name)
        b = read_bytes(path)
        infos[name] = file_info(path)
        i = infos[name]
        if (p.get("bytes"), p.get("sha256"), p.get("lines")) != (i["bytes"], i["sha256"], i["lines"]):
            raise Reject("DIGEST_MISMATCH", f"{name} declared={p.get('bytes')}/{p.get('sha256')}/{p.get('lines')} actual={i['bytes']}/{i['sha256']}/{i['lines']}")
        if b"\r\n" in b:
            raise Reject("EOL_NON_CANONICAL", name)
        try:
            texts[name] = b.decode("utf-8")
        except UnicodeDecodeError as e:
            raise Reject("UTF8_INVALID", f"{name}: {e}")
    ok("pack_files_digest", "5/5 bytes/sha256/lines exact")

    man_hash = sha_bytes(mraw)
    for name, t in texts.items():
        if man_hash in t:
            raise Reject("MANIFEST_SELF_EMBED", name)
        if not t.startswith("# ") or "**File ID**：" not in t:
            raise Reject("MD_HEADER_INVALID", name)
        exact = {
            "project_id": "**project_id**：`FHS-5_PLP`",
            "subject_id": "**subject_id**：`FHS-5_PLP/W1/CONTROL_PACK`",
            "scope": "**scope**：`W1-NF-01`",
            "wave_id": "**wave_id**：`W1`",
            "batch_id": "**batch_id**：`W1-NF-01`",
        }
        for k, token in exact.items():
            if token not in t:
                raise Reject("IDENTITY_MISMATCH", f"{name} missing exact {k} header")
        if PACK_VERSION not in t:
            raise Reject("VERSION_MISMATCH", name)
        if "source_manifest_ref" not in t:
            raise Reject("IDENTITY_MISMATCH", f"{name} missing source_manifest_ref")
    ok("md_identity_version", "all five MD carry identity + version + manifest ref")

    if m.get("manifest_self_hash") != "EXTERNAL_RECORD_ONLY":
        raise Reject("MANIFEST_SELF_HASH", str(m.get("manifest_self_hash")))
    if "pack_manifest_sha256" in m:
        raise Reject("MANIFEST_SELF_EMBED", "pack_manifest_sha256 must live outside 05")
    dc = m.get("digest_contract") or {}
    for k in ("file_sha256", "pack_manifest_sha256", "source_set_sha256", "context_sha256", "package_tree_sha256", "legacy_package_sha256"):
        if k not in dc:
            raise Reject("DIGEST_DOMAIN_MISSING", k)
    ok("digest_domains", "declared")

    # ID sets in the canonical tables.
    dev = parse_ids(texts["01_W1_DEV_ECP.md"], "DEV")
    ops = parse_ids(texts["02_W1_OPS_ECP.md"], "OPS")
    if len(dev) != 38:
        raise Reject("ID_SET_INCOMPLETE", f"DEV unique={len(dev)}")
    if len(ops) != 29:
        raise Reject("ID_SET_INCOMPLETE", f"OPS unique={len(ops)}")
    t3 = texts["03_W1_TQAEP.md"]
    missing_cases = [c for c in CASES if c not in t3]
    if missing_cases:
        raise Reject("CASE_SET_INCOMPLETE", str(missing_cases))
    for sub in ("N01", "N02", "N03", "N04", "N10", "N11"):
        if sub not in t3:
            raise Reject("SUBCASE_MISSING", sub)
    t0 = texts["00_W1_PI_PD.md"]
    for c in CASES:
        if c not in t0 and c not in t3:
            raise Reject("CASE_SET_INCOMPLETE", c)
    for i in range(1, 7):
        if f"P0{i}" not in t0:
            raise Reject("WP_MISSING", f"P0{i}")
    for i in range(1, 10):
        if f"D0{i}" not in t0:
            raise Reject("DELTA_MISSING", f"D0{i}")
    for i in range(1, 11):
        if f"NF{i:02d}" not in t0:
            raise Reject("NF_MISSING", f"NF{i:02d}")
    for i in range(1, 8):
        if f"SM{i:02d}" not in t0:
            raise Reject("SEAM_MISSING", f"SM{i:02d}")
    for i in range(1, 7):
        if f"W1-CODEX-0{i}" not in t0:
            raise Reject("ACC_MISSING", f"W1-CODEX-0{i}")
    for i in range(1, 7):
        if f"W1-A0{i}" not in t0:
            raise Reject("ACC_MISSING", f"W1-A0{i}")
    for h in HOLDS:
        if h not in t0:
            raise Reject("HOLD_MISSING", h)
    t4 = texts["04_W1_START_THIN_PROMPT.md"]
    for sec in ("GOAL", "SOURCE", "SPEC", "EXECUTE", "HARNESS LOOP", "DONE", "STOP", "RESUME"):
        if sec not in t4:
            raise Reject("THIN_PROMPT_INCOMPLETE", sec)
    ok("id_sets", f"DEV={len(dev)} OPS={len(ops)} CASES={len(CASES)}")

    nodes = m.get("dag", {}).get("nodes") or []
    edges = m.get("dag", {}).get("edges") or []
    order = topo(nodes, [tuple(e) for e in edges])
    if set(nodes) != {f"P0{i}" for i in range(1, 7)}:
        raise Reject("DAG_NODE_SET", str(nodes))
    ok("dag_topology", "->".join(order))

    assets = m.get("assets") or []
    if len(assets) != 26:
        raise Reject("ASSET_SET_INCOMPLETE", f"count={len(assets)}")
    seen = set()
    for a in assets:
        key = (a.get("case_id"), a.get("kind"))
        if key in seen:
            raise Reject("ASSET_DUPLICATE", str(key))
        seen.add(key)
        rel = a.get("path")
        if not isinstance(rel, str) or rel.startswith(("/", "\\")) or ".." in rel.split("/"):
            raise Reject("PATH_OUTSIDE_ROOT", str(rel))
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.isfile(p) or not inside(root, p):
            raise Reject("ASSET_MISSING", rel)
        i = file_info(p)
        if (i["bytes"], i["sha256"]) != (a.get("bytes"), a.get("sha256")):
            raise Reject("ASSET_DIGEST_MISMATCH", rel)
    for c in CASES:
        for kind in ("fixture", "oracle"):
            if (c, kind) not in seen:
                raise Reject("ASSET_SET_INCOMPLETE", f"{c}/{kind}")
    ok("assets", "26/26 exact, 13 cases x 2")

    ss = m.get("sources") or []
    ids = [s.get("id") for s in ss]
    if len(ids) != len(set(ids)):
        raise Reject("SOURCE_DUPLICATE", str(ids))
    for s in ss:
        av = s.get("availability")
        if av == "LOCAL_VERIFIED":
            sr = s.get("source_root")
            rel = s.get("path")
            if not sr or not rel:
                raise Reject("SOURCE_LOCATOR_MISSING", str(s.get("id")))
            p = os.path.join(sr, rel)
            if not os.path.isfile(p) or not inside(sr, p):
                raise Reject("SOURCE_MISSING", str(s.get("id")))
            i = file_info(p)
            if (i["bytes"], i["sha256"], i["lines"]) != (s.get("bytes"), s.get("sha256"), s.get("lines")):
                raise Reject("SOURCE_DIGEST_MISMATCH", str(s.get("id")))
        elif av == "REMOTE_ONLY_UNBOUND":
            if s.get("sha256") is not None or s.get("bytes") is not None:
                raise Reject("SOURCE_FAKE_DIGEST", str(s.get("id")))
            if not s.get("reason"):
                raise Reject("SOURCE_REASON_MISSING", str(s.get("id")))
            if not hexn(s.get("git_blob_sha1") or "", 40):
                raise Reject("SOURCE_GIT_BLOB_INVALID", str(s.get("id")))
        else:
            raise Reject("SOURCE_AVAILABILITY_UNKNOWN", f"{s.get('id')}={av}")
    ok("sources", f"{len(ss)} domains checked")

    # source_set digest recompute from local/remote sha? Contract: only rows with sha256.
    lines = []
    for s in sorted([x for x in ss if x.get("sha256")], key=lambda x: x["id"]):
        lines.append(f"{s['id']}|{s['sha256']}|{s['bytes']}\n")
    calc = sha_bytes("".join(lines).encode("utf-8"))
    if dc.get("source_set_sha256_value") != calc:
        raise Reject("SOURCE_SET_DIGEST_MISMATCH", f"declared={dc.get('source_set_sha256_value')} calc={calc}")
    ok("source_set_digest", calc)

    uh = m.get("upstream_handoff") or {}
    for k in ("w0_handoff_id", "pack_sha256", "w0m_sha256", "candidate_commit", "oracle_sha256", "evidence_manifest_sha256", "consumer_manifest_sha256"):
        if not uh.get(k):
            raise Reject("UPSTREAM_PIN_MISSING", k)
    for k in ("pack_sha256", "w0m_sha256", "oracle_sha256", "evidence_manifest_sha256", "consumer_manifest_sha256"):
        if not hexn(uh[k], 64):
            raise Reject("UPSTREAM_PIN_INVALID", k)
    if not hexn(uh["candidate_commit"], 40):
        raise Reject("UPSTREAM_PIN_INVALID", "candidate_commit")
    smap = {s["id"]: s for s in ss if s.get("sha256")}
    cross = {
        "pack_sha256": "W0-05",
        "w0m_sha256": "W0M",
        "handoff_sha256": "H0",
        "closeout_sha256": "C0",
        "w1m_sha256": "W1M",
        "plan_sha256": "PLAN",
        "workctrl_sha256": "WORKCTRL",
        "codexctrl_sha256": "CODEXCTRL",
    }
    for pin, sid in cross.items():
        if sid not in smap or uh.get(pin) != smap[sid]["sha256"]:
            raise Reject("UPSTREAM_PIN_MISMATCH", f"{pin} != {sid}")
    ok("upstream_pins", "H0/W0/W0M/oracle/evidence/consumer")

    seal = seal_path or os.path.join(os.path.dirname(root), "evidence", "SEAL.json")
    if not os.path.isfile(seal):
        raise Reject("SEAL_MISSING", seal)
    sm, _ = strict_json(seal)
    if sm.get("pack_manifest_sha256") != man_hash:
        raise Reject("SEAL_MISMATCH", "pack_manifest_sha256")
    sfiles = {p.get("path"): (p.get("sha256"), p.get("bytes"), p.get("lines")) for p in sm.get("pack_files", [])}
    for name, i in infos.items():
        if sfiles.get(name) != (i["sha256"], i["bytes"], i["lines"]):
            raise Reject("SEAL_MISMATCH", name)
    asset_lines = sorted(f"{a['path']}|{a['sha256']}|{a['bytes']}\n" for a in assets)
    asset_digest = sha_bytes("".join(asset_lines).encode("utf-8"))
    if sm.get("assets_tree_sha256") != asset_digest or sm.get("asset_count") != 26:
        raise Reject("SEAL_MISMATCH", "assets tree")
    if sm.get("w1_execution_ready") != er:
        raise Reject("CLAIM_MISMATCH", "seal w1_execution_ready")
    ok("external_seal", man_hash)

    report["pack_manifest_sha256"] = man_hash
    report["asset_count"] = 26
    report["result"] = "PASS"
    return report


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--root", required=True)
    v.add_argument("--seal")
    v.add_argument("--json-out")
    args = ap.parse_args(argv)
    try:
        report = verify(args.root, args.seal)
    except Reject as e:
        report = {"result": "REJECT", "token": e.token, "detail": e.detail}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8", newline="\n") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
                f.write("\n")
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
