#!/usr/bin/env python3
"""Fail-closed finalizer for the five Phase-4 remediation packets.

The first pass is deliberately usable with no returns: it stages a manifest and
reports missing returns.  It never joins reviewer decisions to the hidden target
until A/B agreement (or a coordinator return) is complete.  Coordinator packets
must contain packet evidence only; the target join is read solely by this script.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
PACK = BASE / "manifests/rq2b_nc_master_phase4_remediation_review_packets_2026-09-06_v1"
OUT = BASE / "manifests/rq2b_nc_master_phase4_remediation_finalization_2026-09-06_v1"
DEFAULT_REPAIR = BASE / "manifests/rq2b_nc_master_phase4_target_token_join_repair_2026-09-06_v1/target_token_join_repair.jsonl"
DEFAULT_A = BASE / "manifests/rq2b_nc_master_phase4_remediation_reviewer_a_2026-09-06_v1/reviewer_a_return.jsonl"
DEFAULT_B = BASE / "manifests/rq2b_nc_master_phase4_remediation_reviewer_b_2026-09-06_v1/reviewer_b_return.jsonl"
DEFAULT_C = BASE / "manifests/rq2b_nc_master_phase4_remediation_coordinator_2026-09-06_v1/coordinator_return.jsonl"
ADEQUACY = {"MOST_SUITABLE", "FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"}
SAFE_CUES = {"NOT_A_CUE", "DECLARED_NECESSARY_CUE_STRATUM"}

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def write(p: Path, rows: list[dict[str, Any]]) -> None:
    p.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows), encoding="utf-8")
def fail(code: str, **kw: Any) -> int:
    print(json.dumps({"status": code, **kw}, indent=2, sort_keys=True)); return 2
def leaks_target_or_provenance(x: Any) -> bool:
    if isinstance(x, dict):
        for k, v in x.items():
            kl = str(k).lower()
            if kl.startswith("target_") or kl in {"target_join", "target_member_token", "author_mapping", "source_path", "source_paths", "source_hash", "source_sha256", "source_hashes"}: return True
            if leaks_target_or_provenance(v): return True
    elif isinstance(x, list): return any(leaks_target_or_provenance(v) for v in x)
    return False

def normal(r: dict[str, Any]) -> tuple[Any, Any]:
    aa = r.get("candidate_assessments")
    if not isinstance(aa, list): raise ValueError("candidate_assessments missing")
    vals = []
    seen = set()
    for x in aa:
        t, a = x.get("candidate_token"), x.get("adequacy")
        if not isinstance(t, str) or t in seen or a not in ADEQUACY: raise ValueError("bad assessment")
        if "source_anchors" not in x: raise ValueError("source_anchors missing")
        seen.add(t); vals.append((t, a))
    if len(vals) != 3: raise ValueError("assessment count is not three")
    cue = r.get("cue_decision")
    if cue not in SAFE_CUES | {"AVOIDABLE_IDENTITY_CUE", "UNCLEAR", "CUE_SAFE", "DECLARED_NECESSARY_CUE_STRATUM", "NOT_A_CUE"} or "cue_anchors" not in r:
        raise ValueError("bad cue decision")
    return tuple(sorted(vals)), (cue, tuple(r.get("cue_anchors") or []))

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--output-dir", type=Path, default=OUT); ap.add_argument("--validate-only", action="store_true")
    ap.add_argument("--reviewer-a", type=Path, default=DEFAULT_A); ap.add_argument("--reviewer-b", type=Path, default=DEFAULT_B); ap.add_argument("--coordinator", type=Path, default=DEFAULT_C)
    ap.add_argument("--target-token-repair", type=Path, default=None, help="Explicitly accept a validated clerical token repair join")
    a = ap.parse_args(); out = a.output_dir.resolve()
    required = [PACK / "reviewer_a_packet.jsonl", PACK / "reviewer_b_packet.jsonl", PACK / "internal_target_join.jsonl"]
    if any(not p.is_file() for p in required): return fail("BLOCKED_MISSING_REMEDIATION_PACKETS", missing=[str(p) for p in required if not p.is_file()])
    pa, pb, joins = read(required[0]), read(required[1]), read(required[2])
    if a.target_token_repair is not None:
        rp = a.target_token_repair.resolve()
        if not rp.is_file(): return fail("BLOCKED_TARGET_TOKEN_REPAIR_MISSING", path=str(rp))
        repairs = read(rp)
        if len(repairs) != 5 or any(x.get("target_join") != "WITHHELD_UNTIL_FINALIZER" or not x.get("target_candidate_token") for x in repairs):
            return fail("BLOCKED_TARGET_TOKEN_REPAIR_SCHEMA")
        if {x.get("packet_id") for x in repairs} != {x.get("packet_id") for x in joins}:
            return fail("BLOCKED_TARGET_TOKEN_REPAIR_ID_SET")
        joins = repairs
    ids_a, ids_b = {x.get("packet_id") for x in pa}, {x.get("packet_id") for x in pb}
    if len(pa) != 5 or len(pb) != 5 or None in ids_a or None in ids_b or ids_a != ids_b:
        return fail("BLOCKED_REMEDIATION_PACKET_ID_SET", reviewer_a=sorted(ids_a), reviewer_b=sorted(ids_b))
    IDS = ids_a
    if len(joins) != 5 or {x.get("packet_id") for x in joins} != IDS: return fail("BLOCKED_TARGET_JOIN_ID_SET")
    by_a, by_b, by_j = ({x["packet_id"]: x for x in z} for z in (pa, pb, joins))
    ra_path, rb_path, rc_path = a.reviewer_a.resolve(), a.reviewer_b.resolve(), a.coordinator.resolve()
    missing = [p.name for p in (ra_path, rb_path) if not p.is_file()]
    if missing:
        if not a.validate_only and not out.exists():
            out.mkdir(parents=True); (out / "staging.json").write_text(json.dumps({"status":"PENDING_TWO_INDEPENDENT_REVIEW_RETURNS","expected_packet_ids":sorted(IDS),"missing_returns":missing,"coordinator_boundary":"Coordinator sees sealed packet-only disagreements; it never receives internal_target_join or target mapping."}, indent=2)+"\n", encoding="utf-8")
        return fail("PENDING_REMEDIATION_REVIEW_RETURNS", missing_returns=missing, coordinator_must_not_see_target_join=True)
    try: ra, rb = read(ra_path), read(rb_path)
    except Exception as e: return fail("BLOCKED_RETURN_JSON", error=str(e))
    if len(ra) != 5 or len(rb) != 5 or {x.get("packet_id") for x in ra} != IDS or {x.get("packet_id") for x in rb} != IDS: return fail("BLOCKED_RETURN_ID_SET_OR_COUNT")
    for reviewer, rs, ps, path in (("A",ra,by_a,ra_path),("B",rb,by_b,rb_path)):
        for r in rs:
            pid=r["packet_id"]
            if r.get("reviewer") not in (None, reviewer): return fail("BLOCKED_REVIEWER_IDENTITY", packet_id=pid)
            # Established return schema calls this field review_packet_sha256.
            if r.get("review_packet_sha256") not in (None, sha(PACK / ("reviewer_a_packet.jsonl" if reviewer=="A" else "reviewer_b_packet.jsonl"))): return fail("BLOCKED_REVIEW_PACKET_SHA", packet_id=pid, reviewer=reviewer)
            try: normal(r)
            except ValueError as e: return fail("BLOCKED_RETURN_SCHEMA", packet_id=pid, reviewer=reviewer, error=str(e))
    A={x["packet_id"]:x for x in ra}; B={x["packet_id"]:x for x in rb}; disagreements=[]; resolved={}; supports={}
    for pid in sorted(IDS):
        na, nb = normal(A[pid]), normal(B[pid])
        supports[pid] = {"reviewer_a": A[pid], "reviewer_b": B[pid]}
        if na == nb: resolved[pid] = na
        else: disagreements.append({"packet_id":pid,"reviewer_a":na,"reviewer_b":nb,"review_boundary":"Packet-only disagreement. No target join, target token, source path, or intended mapping is included."})
    if disagreements:
        # Seal a coordinator packet before blocking. It is deliberately built
        # from the opaque reviewer packet, never from internal_target_join.
        sealed=[]
        for d in disagreements:
            pid=d["packet_id"]
            sealed.append({"packet_id":pid,"prompt":by_a[pid]["prompt"],"candidates":by_a[pid]["candidates"],
                "reviewer_a_support":A[pid],"reviewer_b_support":B[pid],
                "input_hashes":{"reviewer_a_packet_sha256":sha(required[0]),"reviewer_b_packet_sha256":sha(required[1]),"reviewer_a_return_sha256":sha(ra_path),"reviewer_b_return_sha256":sha(rb_path)},
                "review_boundary":"Resolve only the adequacy mapping and cue decision. Do not infer target, author, source path/hash, prior disposition, rank, retrieval, outcome, or acceptable-set membership.",
                "coordinator_return_schema":{"packet_id":pid,"candidate_assessments":[{"candidate_token":"C-*","adequacy":"MOST_SUITABLE | FULLY_ACCEPTABLE | PARTIALLY_ADEQUATE | INADEQUATE | UNCLEAR","rationale":"","source_anchors":[]}],"cue_decision":"NOT_A_CUE | DECLARED_NECESSARY_CUE_STRATUM | AVOIDABLE_IDENTITY_CUE | UNCLEAR","cue_anchors":[]}})
        if not a.validate_only:
            out.mkdir(parents=True, exist_ok=True); write(out/"sealed_disagreement_packets.jsonl", sealed)
        if not rc_path.is_file(): return fail("PENDING_COORDINATOR_FOR_DISAGREEMENTS", disagreement_packet_ids=[x["packet_id"] for x in disagreements], sealed_disagreement_count=len(sealed), coordinator_must_not_see_target_join=True)
        rc=read(rc_path)
        if len(rc)!=len(disagreements) or {x.get("packet_id") for x in rc}!={x["packet_id"] for x in disagreements}: return fail("BLOCKED_COORDINATOR_ID_SET")
        for r in rc:
            if r.get("reviewer") != "C" or r.get("sealed_packet_sha256") != sha(out/"sealed_disagreement_packets.jsonl") or leaks_target_or_provenance(r): return fail("BLOCKED_COORDINATOR_PACKET_BOUNDARY", packet_id=r.get("packet_id"))
            try: resolved[r["packet_id"]]=normal(r); supports[r["packet_id"]]["coordinator"] = r
            except ValueError as e: return fail("BLOCKED_COORDINATOR_SCHEMA", packet_id=r.get("packet_id"), error=str(e))
    decisions=[]
    for pid in sorted(IDS):
        vals, cue = resolved[pid]; j=by_j[pid]
        target=j.get("target_candidate_token") if a.target_token_repair is not None else j.get("target_member_token")
        # `normal()` deliberately returns the decision signature only
        # (candidate token, adequacy).  Rationale/anchors are preserved in
        # reviewer_support_evidence.jsonl, but do not define agreement.
        amap={t:v for t,v in vals}; target_ok=amap.get(target) in {"MOST_SUITABLE","FULLY_ACCEPTABLE"}
        alternate=any(t!=target and v in {"MOST_SUITABLE","FULLY_ACCEPTABLE"} for t,v in vals)
        cue_ok=cue[0] in SAFE_CUES
        status="PASS_CURRENT_REMEDIATION_BINDING" if target_ok and not alternate and cue_ok else "BLOCK_CURRENT_REMEDIATION_BINDING"
        decisions.append({"packet_id":pid,"status":status,"rule":"designated target must be MOST_SUITABLE/FULLY_ACCEPTABLE; no alternate may be fully acceptable; cue must be non-avoidable and non-unclear","cue_decision":cue[0],"target_member_token":target if status.startswith("PASS") else None})
    if a.validate_only: print(json.dumps({"status":"PASS_FINALIZATION_READY","decisions":decisions},indent=2)); return 0
    out.mkdir(parents=True, exist_ok=True); write(out/"decisions.jsonl", decisions)
    write(out/"reviewer_support_evidence.jsonl", [{"packet_id":pid,"support":supports[pid]} for pid in sorted(supports)])
    final_status = "PASS_CURRENT_REMEDIATION_FINALIZED_NO_EXPERIMENT" if all(x["status"].startswith("PASS") for x in decisions) else "BLOCKED_CURRENT_REMEDIATION_BINDING"
    (out/"summary.json").write_text(json.dumps({"status":final_status,"counts":{"packets":5,"disagreements":len(disagreements),"blocked_decisions":sum(x["status"].startswith("BLOCK") for x in decisions)},"coordinator_boundary":"Coordinator cannot see internal_target_join.","bound_inputs":{"reviewer_a_return_path":str(ra_path),"reviewer_a_return_sha256":sha(ra_path),"reviewer_b_return_path":str(rb_path),"reviewer_b_return_sha256":sha(rb_path),"coordinator_return_path":str(rc_path) if rc_path.is_file() else None,"coordinator_return_sha256":sha(rc_path) if rc_path.is_file() else None,"sealed_disagreement_packets_sha256":sha(out/"sealed_disagreement_packets.jsonl") if (out/"sealed_disagreement_packets.jsonl").is_file() else None,"target_join_path":str(required[2]),"target_join_sha256":sha(required[2]),"target_token_repair_path":str(a.target_token_repair.resolve()) if a.target_token_repair is not None else None,"target_token_repair_sha256":sha(a.target_token_repair.resolve()) if a.target_token_repair is not None else None}},indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":final_status,"output_dir":str(out)},indent=2)); return 0 if final_status.startswith("PASS") else 2
if __name__ == "__main__": raise SystemExit(main())
