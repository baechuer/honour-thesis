#!/usr/bin/env python3
"""Rebuild the five Phase-4 hidden target joins from sealed source evidence.

This is a clerical, append-only repair.  It never reads reviewer decisions and
does not make an adequacy, cue, retrieval, or admission decision.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
PACK = BASE / "manifests/rq2b_nc_master_phase4_remediation_review_packets_2026-09-06_v1"
AUTHOR = BASE / "manifests/rq2b_nc_master_phase4_missing_nc_prompt_authoring_packets_2026-09-06_v1/author_packet.jsonl"
OUT = BASE / "manifests/rq2b_nc_master_phase4_target_token_join_repair_2026-09-06_v1"

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p: Path):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def dump(p: Path, xs):
    p.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True)+"\n" for x in xs), encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--output-dir", type=Path, default=OUT); ap.add_argument("--validate-only", action="store_true")
    a = ap.parse_args(); out = a.output_dir.resolve()
    apath = AUTHOR; jpath = PACK / "internal_target_join.jsonl"
    rapaths = [PACK / "reviewer_a_packet.jsonl", PACK / "reviewer_b_packet.jsonl"]
    required = [apath, jpath, *rapaths]
    if any(not p.is_file() for p in required):
        print(json.dumps({"status":"BLOCKED_REPAIR_INPUT_MISSING","missing":[str(p) for p in required if not p.is_file()]}, indent=2)); return 2
    authors = rows(apath); joins = rows(jpath); pa, pb = rows(rapaths[0]), rows(rapaths[1])
    by_author = {x["author_packet_id"]: x for x in authors}
    by_join = {x["packet_id"]: x for x in joins}
    by_pa = {x["packet_id"]: x for x in pa}; by_pb = {x["packet_id"]: x for x in pb}
    ids = set(by_author) & set(by_join) & set(by_pa) & set(by_pb)
    expected = set(by_join)
    if ids != expected or len(ids) != 5:
        print(json.dumps({"status":"BLOCKED_REPAIR_PACKET_ID_SET","expected":sorted(expected),"resolved":sorted(ids)}, indent=2)); return 2
    repaired = []
    for pid in sorted(ids):
        au, j, ra, rb = by_author[pid], by_join[pid], by_pa[pid], by_pb[pid]
        members = au.get("members")
        target_token = j.get("target_member_token")
        target_sha = j.get("target_source_sha256")
        if not isinstance(members, list) or len(members) != 3 or target_token not in {m.get("member_token") for m in members}:
            print(json.dumps({"status":"BLOCKED_REPAIR_MEMBER_ORDER","packet_id":pid}, indent=2)); return 2
        idx = next(i for i,m in enumerate(members, 1) if m.get("member_token") == target_token)
        member_sha = members[idx-1].get("canonical_source_sha256")
        if member_sha != target_sha:
            print(json.dumps({"status":"BLOCKED_REPAIR_SOURCE_SHA_MISMATCH","packet_id":pid,"target_sha":target_sha,"member_sha":member_sha}, indent=2)); return 2
        # A/B packets may be independently shuffled.  Join by the SHA of the
        # complete original skill, then require both opaque packets to expose
        # the same token for that source (never by reviewer order).
        def token_for(packet):
            hits = [c.get("candidate_token") for c in packet.get("candidates", [])
                    if hashlib.sha256(c.get("complete_original_skill", "").encode()).hexdigest() == target_sha]
            return hits[0] if len(hits) == 1 else None
        ta, tb = token_for(ra), token_for(rb)
        ca = [x.get("candidate_token") for x in ra.get("candidates", [])]
        cb = [x.get("candidate_token") for x in rb.get("candidates", [])]
        if ta is None or ta != tb or len(set(ca)) != 3 or len(set(cb)) != 3:
            print(json.dumps({"status":"BLOCKED_REPAIR_OPAQUE_CANDIDATE_SOURCE_JOIN","packet_id":pid,"a":ca,"b":cb,"target_sha":target_sha,"token_a":ta,"token_b":tb}, indent=2)); return 2
        expected_candidate = ta
        repaired.append({"packet_id":pid,"target_join":"WITHHELD_UNTIL_FINALIZER","target_member_token":target_token,"target_candidate_token":expected_candidate,"target_source_sha256":target_sha,"member_index_1_based":idx,"mapping_basis":"author_packet_members_order + internal_target_join target_member_token/source_sha256 + identical opaque reviewer candidate order","input_hashes":{"author_packet_sha256":digest(apath),"internal_target_join_sha256":digest(jpath),"reviewer_a_packet_sha256":digest(rapaths[0]),"reviewer_b_packet_sha256":digest(rapaths[1])},"claim_boundary":"Clerical target-token join only; no reviewer, semantic, cue, retrieval, acceptable-set, or admission decision."})
    summary={"status":"PASS_TARGET_TOKEN_JOIN_REPAIR_MATERIALISED_NO_REVIEW_OR_EXPERIMENT","counts":{"packets":len(repaired)},"bound_inputs":{str(p.relative_to(ROOT)):digest(p) for p in required},"outputs":{"target_token_join_repair.jsonl":None}}
    if a.validate_only:
        summary["outputs"]={}; print(json.dumps(summary, indent=2, sort_keys=True)); return 0
    out.mkdir(parents=True, exist_ok=True); dump(out/"target_token_join_repair.jsonl", repaired); summary["outputs"]["target_token_join_repair.jsonl"]=digest(out/"target_token_join_repair.jsonl")
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":summary["status"],"output_dir":str(out),"counts":summary["counts"]},indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
