import argparse, hashlib, json, sys
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--candidate", default=None)
    ap.add_argument("--evidence", default=None)
    a = ap.parse_args()
    pack = Path(a.pack).resolve()
    mpath = pack/"05_W0_SOURCE_MANIFEST.json"
    m = json.loads(mpath.read_text(encoding="utf-8"))
    files = []
    ok = True
    for x in m["pack_files"]:
        p = pack/x["path"]
        h = sha(p); b = p.stat().st_size
        good = h == x["sha256"] and b == x["bytes"]
        ok = ok and good
        files.append({"path": x["path"], "sha256": h, "bytes": b, "ok": good})
    mode = "PACKAGE_FIRST"
    body_sufficient = ok
    if not body_sufficient:
        mode = "CONTEXT_AUGMENTED"
    delta = {
        "source_sha": m["authority"]["source_w0m_sha256"],
        "candidate_sha": a.candidate,
        "evidence_sha": a.evidence,
        "requirement_ids": ["SAMPLE-R1","SAMPLE-R2","SAMPLE-R3","SAMPLE-R4"],
        "case_ids": ["F5-W0-T01","F5-W0-T03","F5-W0-T06","F5-W0-T13","NF-T01"],
        "findings": [],
        "next_action": "run B0 current READY task",
        "stop_conditions": ["pack digest mismatch","no write-set/preimage","path escape/secret","false permit"],
        "not_covered": ["HERMES/GPT CHAT/GPT WORK host execution","full U26/CG-SEM17","release"],
    }
    out = {
        "schema": "FHS5.B0NF.GuideThinStart@1",
        "claim_ceiling": "BUILD_MINIMAL_GUIDE_REFERENCE",
        "pack": str(pack),
        "mode": mode,
        "pack_digest": hashlib.sha256(json.dumps(files, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
        "files": files,
        "goal": "Complete B0-NF five-party representative loop with CODEX Native DEV/OPS",
        "done": ["five-party individual+combined","DEV/OPS readback","Challenge/FAR","OFF","consumer"],
        "limits": ["local CODEX scope","no external admin/release","no HERMES/GPT host claim"],
        "next": "run briefcheck candidate challenge",
        "delta": delta,
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"mode": mode, "pack_ok": ok, "delta_keys": len(delta)}, ensure_ascii=False))
    return 0 if ok else 3

if __name__ == "__main__":
    sys.exit(main())
