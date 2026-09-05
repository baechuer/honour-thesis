#!/usr/bin/env python3
"""Materialise the first target-blind Phase-5 K=6 review batch.

This is an allocation-only controller.  It deliberately does not inspect or
join any target/label/rank/result artefacts and does not produce review
decisions.  The Phase-4 v2 packets are copied by value into a new, append-only
batch envelope so later reviewer returns can be audited independently.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "rq2b_naturalistic_confusability/manifests/RQ2b-NC-master-phase4-audit-input-2026-09-06_v2"
OUT = ROOT / "rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase5_k6_batch_001_2026-09-06_v1"

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def load(name): return [json.loads(x) for x in (INP/name).read_text().splitlines() if x.strip()]
def canon(x): return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    ledger = load("prompt_k6_allocation_ledger.jsonl")
    mains = load("main_blind_review_packets.jsonl")
    tails = load("tail_blind_review_packets.jsonl")
    # Ledger order is the frozen allocation order.  No sorting or re-ranking.
    groups = []
    seen = set()
    for row in ledger:
        pid = row["prompt_id"]
        if pid not in seen:
            groups.append(row); seen.add(pid)
        if len(groups) == 8: break
    assert len(groups) == 8
    ids = {r["prompt_id"] for r in groups}
    main_by = {r["prompt_sha256"]: r for r in mains}
    tail_by = {}
    for r in tails: tail_by.setdefault(r["prompt_sha256"], []).append(r)
    selected_main = [main_by[r["prompt_sha256"]] for r in groups]
    selected_tail = [tail_by[r["prompt_sha256"]][i] for r in groups for i in range(2)]
    assert all(len(r["candidates"]) == 6 for r in selected_main)
    assert all(len(r["candidates"]) == 1 for r in selected_tail)
    assert len(selected_tail) == 16

    # Packet IDs remain opaque, while batch IDs give a deterministic audit key.
    batch_rows = []
    for ix, (g, m) in enumerate(zip(groups, selected_main), 1):
        batch_rows.append({"batch_group_id": f"B001-G{ix:02d}", "batch_order": ix,
                           "prompt_id": g["prompt_id"], "prompt_sha256": g["prompt_sha256"],
                           "packet_id": m["packet_id"], "packet_kind": "K6_MAIN",
                           "main_candidate_count": 6, "tail_packet_count": 2,
                           "source_input_sha256": sha(canon(m).encode())})
    (OUT/"batch_group_allocation.jsonl").write_text("\n".join(canon(x) for x in batch_rows)+"\n")
    (OUT/"main_blind_review_packets.jsonl").write_text("\n".join(canon(x) for x in selected_main)+"\n")
    (OUT/"tail_blind_review_packets.jsonl").write_text("\n".join(canon(x) for x in selected_tail)+"\n")

    schemas = {
      "reviewer_A": {"reviewer_role":"independent_target_blind_A", "return_fields":["batch_group_id","packet_id","candidate_token","adequacy_decision","rationale","source_anchors","tail_flag","input_packet_sha256"], "adequacy_decision_enum":["FULLY_ACCEPTABLE","PARTIALLY_ADEQUATE","INADEQUATE","UNCLEAR"]},
      "reviewer_B": {"reviewer_role":"independent_target_blind_B", "return_fields":["batch_group_id","packet_id","candidate_token","adequacy_decision","rationale","source_anchors","tail_flag","input_packet_sha256"], "adequacy_decision_enum":["FULLY_ACCEPTABLE","PARTIALLY_ADEQUATE","INADEQUATE","UNCLEAR"]},
      "boundary": {"target_blind":True, "forbidden_inputs":["target labels","assigned targets","retrieval ranks","retrieval outcomes","acceptable-set decisions","embeddings","reranking","provider calls"], "review_only":"Judge adequacy of the visible full skill against the visible prompt; cite anchors from that skill and do not infer target identity."}
    }
    (OUT/"reviewer_return_schemas.json").write_text(json.dumps(schemas, indent=2, ensure_ascii=False)+"\n")
    files = {}
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name != "manifest.json": files[p.name] = sha(p.read_bytes())
    manifest = {"status":"PENDING_A_B", "batch_id":"RQ2B-NC-P5-B001", "phase":"PHASE5_K6_OUTCOME_BLIND_REVIEW",
      "allocation_rule":"first eight unique prompt groups in frozen Phase-4 v2 ledger order",
      "k":6, "main_packet_count":8, "main_candidate_assessments":48,
      "tail_packet_count":16, "tail_candidate_assessments":16, "total_blind_packets":24,
      "total_candidate_assessments":64, "input_dir":str(INP),
      "input_file_sha256":{n:sha((INP/n).read_bytes()) for n in ["prompt_k6_allocation_ledger.jsonl","main_blind_review_packets.jsonl","tail_blind_review_packets.jsonl"]},
      "output_file_sha256":files,
      "limitations":["Allocation only; no A/B returns or K=6 results are present.","No target, label, rank, retrieval outcome, embedding, reranking, or provider call is included.","Full source skill text is retained exactly inside the opaque blind packets."]}
    manifest["packet_collection_sha256"] = sha((OUT/"main_blind_review_packets.jsonl").read_bytes()+(OUT/"tail_blind_review_packets.jsonl").read_bytes())
    (OUT/"manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+"\n")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))

if __name__ == "__main__": main()
