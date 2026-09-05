#!/usr/bin/env python3
"""Materialise deterministic, target-blind Phase-5 Batch 002."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "rq2b_naturalistic_confusability/manifests/RQ2b-NC-master-phase4-audit-input-2026-09-06_v2"
OUT = ROOT / "rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase5_k6_batch_002_2026-09-06_v1"
PREV = ROOT / "rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase5_k6_batch_001_2026-09-06_v1"
sha = lambda b: hashlib.sha256(b).hexdigest()
canon = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def load(n): return [json.loads(x) for x in (INP/n).read_text().splitlines() if x.strip()]

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    ledger, mains, tails = load("prompt_k6_allocation_ledger.jsonl"), load("main_blind_review_packets.jsonl"), load("tail_blind_review_packets.jsonl")
    groups=[]; seen=set()
    for row in ledger:
        if row["prompt_id"] not in seen: groups.append(row); seen.add(row["prompt_id"])
    groups = groups[8:16]
    assert len(groups)==8 and len({g["prompt_id"] for g in groups})==8
    old = {json.loads(x)["prompt_id"] for x in (PREV/"batch_group_allocation.jsonl").read_text().splitlines() if x.strip()}
    assert not old.intersection({g["prompt_id"] for g in groups})
    mb={r["prompt_sha256"]:r for r in mains}; tb={}
    for r in tails: tb.setdefault(r["prompt_sha256"],[]).append(r)
    sm=[mb[g["prompt_sha256"]] for g in groups]; st=[tb[g["prompt_sha256"]][i] for g in groups for i in range(2)]
    assert all(len(r["candidates"])==6 for r in sm) and all(len(r["candidates"])==1 for r in st)
    rows=[]
    for i,(g,m) in enumerate(zip(groups,sm),1):
        rows.append({"batch_group_id":f"B002-G{i:02d}","batch_order":i,"prompt_id":g["prompt_id"],"prompt_sha256":g["prompt_sha256"],"packet_id":m["packet_id"],"packet_kind":"K6_MAIN","main_candidate_count":6,"tail_packet_count":2,"source_input_sha256":sha(canon(m).encode())})
    (OUT/"batch_group_allocation.jsonl").write_text("\n".join(canon(x) for x in rows)+"\n")
    (OUT/"main_blind_review_packets.jsonl").write_text("\n".join(canon(x) for x in sm)+"\n")
    (OUT/"tail_blind_review_packets.jsonl").write_text("\n".join(canon(x) for x in st)+"\n")
    schemas={"reviewer_A":{"reviewer_role":"independent_target_blind_A","return_fields":["batch_group_id","packet_id","candidate_token","adequacy_decision","rationale","source_anchors","tail_flag","input_packet_sha256"],"adequacy_decision_enum":["FULLY_ACCEPTABLE","PARTIALLY_ADEQUATE","INADEQUATE","UNCLEAR"]},"reviewer_B":{"reviewer_role":"independent_target_blind_B","return_fields":["batch_group_id","packet_id","candidate_token","adequacy_decision","rationale","source_anchors","tail_flag","input_packet_sha256"],"adequacy_decision_enum":["FULLY_ACCEPTABLE","PARTIALLY_ADEQUATE","INADEQUATE","UNCLEAR"]},"boundary":{"target_blind":True,"forbidden_inputs":["target labels","assigned targets","retrieval ranks","retrieval outcomes","acceptable-set decisions","embeddings","reranking","provider calls"],"review_only":"Judge visible full skill against visible prompt and cite source anchors."}}
    (OUT/"reviewer_return_schemas.json").write_text(json.dumps(schemas,indent=2,ensure_ascii=False)+"\n")
    names=["batch_group_allocation.jsonl","main_blind_review_packets.jsonl","tail_blind_review_packets.jsonl","reviewer_return_schemas.json"]
    files={n:sha((OUT/n).read_bytes()) for n in names}
    m={"status":"PENDING_A_B","batch_id":"RQ2B-NC-P5-B002","phase":"PHASE5_K6_OUTCOME_BLIND_REVIEW","allocation_rule":"prompt groups 9-16 in frozen Phase-4 v2 ledger order; Batch001 groups excluded","k":6,"main_packet_count":8,"main_candidate_assessments":48,"tail_packet_count":16,"tail_candidate_assessments":16,"total_blind_packets":24,"total_candidate_assessments":64,"input_dir":str(INP),"input_file_sha256":{n:sha((INP/n).read_bytes()) for n in ["prompt_k6_allocation_ledger.jsonl","main_blind_review_packets.jsonl","tail_blind_review_packets.jsonl"]},"output_file_sha256":files,"packet_collection_sha256":sha((OUT/"main_blind_review_packets.jsonl").read_bytes()+(OUT/"tail_blind_review_packets.jsonl").read_bytes()),"limitations":["Allocation only; no A/B returns or decisions.","No target, label, rank, outcome, embedding, reranking, or provider call included.","Full original skill text retained exactly inside opaque blind packets."]}
    (OUT/"manifest.json").write_text(json.dumps(m,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(m,indent=2,ensure_ascii=False))
if __name__=="__main__": main()
