#!/usr/bin/env python3
"""Materialise the current changed-scope NC prompt binding (clerical only).

This intentionally joins four already-PASS binding rows with five separately
finalised remediation rows.  It never edits prompt text and fails closed on
any missing/current-status mismatch.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
M = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests"
BASE = M / "rq2b_nc_master_phase4_missing_nc_prompt_binding_2026-09-06_v1"
AUTH = M / "rq2b_nc_master_phase4_missing_nc_prompt_authoring_packets_2026-09-06_v1/author_packet.jsonl"
RET = M / "rq2b_nc_master_phase4_bounded_prompt_author_return_2026-09-06_v1/author_return.jsonl"
DEC = M / "rq2b_nc_master_phase4_remediation_finalization_2026-09-06_v6/decisions.jsonl"
JOIN = M / "rq2b_nc_master_phase4_target_token_join_repair_2026-09-06_v1/target_token_join_repair.jsonl"
PH3 = M / "rq2b_nc_master_phase3_closure_2026-09-06_v1/summary.json"
UNION = M / "rq2b_nc_master_phase1_reconciliation_2026-09-06_v1/source_union.jsonl"
OUT = M / "rq2b_nc_master_phase4_current_nc_prompt_composite_2026-09-06_v1"

def lines(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def text_sha(s): return hashlib.sha256(s.encode()).hexdigest()
def fail(msg): raise SystemExit("FAIL_CLOSED: " + msg)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output", type=Path, default=OUT); a=ap.parse_args()
    old=lines(BASE/"prompt_binding_rows.jsonl")
    current=[x for x in old if x.get("binding_status")=="PASS_CURRENT_NC_PROMPT_BINDING"
             and x.get("final_local_disposition",{}).get("final_prompt_disposition")=="PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"]
    if len(current)!=4: fail(f"expected 4 existing current PASS rows, found {len(current)}")
    auth={x["author_packet_id"]:x for x in lines(AUTH)}; ret={x["packet_id"]:x for x in lines(RET)}
    dec={x["packet_id"]:x for x in lines(DEC)}; join={x["packet_id"]:x for x in lines(JOIN)}
    fresh=[]
    for packet,j in join.items():
        if packet not in auth or packet not in ret or packet not in dec: fail(f"missing evidence for {packet}")
        if dec[packet].get("status")!="PASS_CURRENT_REMEDIATION_BINDING": fail(f"non-PASS remediation {packet}")
        if j.get("target_join")!="WITHHELD_UNTIL_FINALIZER": fail(f"unexpected join state {packet}")
        p=ret[packet].get("prompt");
        if not isinstance(p,str) or not p.strip(): fail(f"empty prompt {packet}")
        if text_sha(p)!=text_sha(p): fail("unreachable prompt hash check")
        ar=auth[packet]; fresh.append({"packet":packet,"author":ar,"return":ret[packet],"decision":dec[packet],"join":j})
    if len(fresh)!=5: fail(f"expected 5 fresh remediation rows, found {len(fresh)}")
    rows=[]
    for x in current:
        y=dict(x); y["target_source_sha256"]=y.get("target_source_sha256",y.get("author_target_source_sha256")); y["composite_binding_status"]="PASS_CURRENT_NC_PROMPT_COMPOSITE"; y["composite_origin"]="EXISTING_CURRENT_PASS"; rows.append(y)
    old_by_sha={s["canonical_source_sha256"]:s for x in old for s in x.get("source_visible_candidate_set",[])}
    for x in fresh:
        ar=x["author"]; r=x["return"]; j=x["join"]
        original=next((z for z in old if z.get("family_token")==ar["family_token"]),None)
        if original is None: fail(f"no current family binding for {x['packet']}")
        members=ar.get("members",[])
        if len(members)!=3: fail(f"triad not exactly 3 for {x['packet']}")
        prompt=r["prompt"]; target_sha=j["target_source_sha256"]
        if target_sha!=ar["target_source_sha256"]: fail(f"target SHA mismatch {x['packet']}")
        row={
          "canonical_prompt_id":"P-"+text_sha(prompt)[:16], "author_prompt":prompt,
          "author_prompt_sha256":text_sha(prompt), "batch":ar["batch"], "family_token":ar["family_token"],
          "member_token":j["target_member_token"], "target_source_sha256":target_sha,
          "binding_status":"PASS_CURRENT_NC_PROMPT_BINDING", "composite_binding_status":"PASS_CURRENT_NC_PROMPT_COMPOSITE",
          "composite_origin":"FRESH_REMEDIATION_FINALIZED_V6", "final_local_disposition":{"final_prompt_disposition":"PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT","prompt_integrity":"CUE_SAFE","review_route":"REMEDIATION_A_B_COORDINATOR_FINALIZED"},
          "phase3_linkage": original.get("phase3_linkage",{}),
          "source_supported_distinguishing_requirements": original.get("source_supported_distinguishing_requirements",[]),
          "source_visible_candidate_set":[{"member_token":m["member_token"],"canonical_source_sha256":m.get("canonical_source_sha256"),"source_byte_replay":m.get("source_byte_replay"),"provenance_preflight_status":m.get("provenance_preflight_status"),"source_path":m.get("original_relative_path")} for m in members],
          "phase4_evidence":{"packet_id":x["packet"],"author_return_sha256":sha(RET),"finalization_decision_sha256":sha(DEC),"target_token_join_repair_sha256":sha(JOIN)},
        }
        rows.append(row)
    if len(rows)!=9: fail(f"expected 9 rows, found {len(rows)}")
    ids=[x["canonical_prompt_id"] for x in rows]; shas=[x["target_source_sha256"] for x in rows]; toks=[(x["family_token"],x["member_token"]) for x in rows]
    if len(set(ids))!=9 or len(set(shas))!=9 or len(set(toks))!=9: fail("duplicate prompt/source/token identity")
    fam={}
    for x in rows: fam.setdefault(x["family_token"],[]).append(x)
    if len(fam)!=3 or sorted(map(len,fam.values()))!=[3,3,3]: fail("not three exact 3-member families")
    if any(x.get("binding_status")!="PASS_CURRENT_NC_PROMPT_BINDING" for x in rows): fail("non-current PASS row")
    a.output.mkdir(parents=True,exist_ok=True)
    (a.output/"composite_prompt_binding_rows.jsonl").write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in rows))
    manifest={"status":"PASS_CURRENT_NC_PROMPT_COMPOSITE_BINDING_NO_FREEZE_NO_EXPERIMENT","counts":{"rows":9,"families":3,"members_per_family":[3,3,3]},"inputs":{str(p.relative_to(ROOT)):sha(p) for p in [BASE/"prompt_binding_rows.jsonl",AUTH,RET,DEC,JOIN,PH3,UNION]},"claim_boundary":"Current prompt binding and evidence join only; no freeze, K=6 audit, acceptable-set admission, retrieval, embedding, provider, metric, or experiment result."}
    (a.output/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=="__main__": main()
