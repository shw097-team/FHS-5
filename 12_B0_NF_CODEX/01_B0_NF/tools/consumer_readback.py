import argparse, hashlib, json, sys
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--checker", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    pack = Path(a.pack).resolve()
    m = json.loads((pack/"05_W0_SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    pack_ok = all(sha(pack/x["path"]) == x["sha256"] for x in m["pack_files"])
    ch = json.loads(Path(a.checker).read_text(encoding="utf-8"))
    cand_ok = ch.get("pins", {}).get("candidate") is not None
    out = {
        "schema": "FHS5.B0NF.ConsumerReceipt@1",
        "consumer_id": "consumer-readback/1",
        "pack": str(pack),
        "pack_manifest_sha256": sha(pack/"05_W0_SOURCE_MANIFEST.json"),
        "pack_files_ok": pack_ok,
        "candidate": a.candidate,
        "checker": a.checker,
        "checker_verdict": ch.get("verdict"),
        "checker_pins": ch.get("pins"),
        "consumed": bool(pack_ok and cand_ok),
        "readback": "manifest+checker+candidate pins read",
        "next": "W0 CLOSEOUT/HANDOFF" if pack_ok and cand_ok else "STOP",
        "not_claimed": ["HERMES/GPT host execution","release"],
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"consumed": out["consumed"], "checker": out["checker_verdict"]}, ensure_ascii=False))
    return 0 if out["consumed"] else 3

if __name__ == "__main__":
    sys.exit(main())
