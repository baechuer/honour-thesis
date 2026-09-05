#!/usr/bin/env python3
"""Materialise B037 from frozen lexical hypotheses, excluding B001-B036."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

W = Path(__file__).resolve().parents[2]
N = W / "skill_benchmark/rq2b_naturalistic_confusability"
P = N / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
H = N / "review/source_native_lexical_bootstrap_2026-09-04/all_mutual_triangle_hypotheses.jsonl"
R = N / "review"
O = R / "source_native_dense_lexical_union_b037_2026-09-04"
Q = O / "batch_037_full_source_review_queue_internal.jsonl"

def rows(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return str(p.relative_to(W))
def main():
    if O.exists(): raise SystemExit(f"Output directory already exists: {O}")
    if not P.is_file() or not H.is_file(): raise SystemExit("Missing protocol or frozen hypotheses")
    found = {}
    pat = re.compile(r"batch_(\d+)_full_source_review_packets/internal_reconciliation_key\.jsonl$")
    for p in R.glob("**/internal_reconciliation_key.jsonl"):
        m = pat.search(rel(p))
        if m and int(m.group(1)) <= 36:
            b = int(m.group(1))
            if b in found: raise SystemExit(f"Duplicate B{b:03d} key")
            found[b] = p
    if set(found) != set(range(1,37)): raise SystemExit("Incomplete B001-B036 ledger")
    prior = set()
    for b,p in found.items():
        r=rows(p)
        if len(r)!=75: raise SystemExit(f"B{b:03d} key row count")
        prior.update(x["canonical_source_sha256"] for x in r)
    if len(prior)!=2700: raise SystemExit("Prior source ledger not disjoint")
    hs=rows(H); hs.sort(key=lambda x:(-x["reciprocal_link_count"],-x["rank_fusion_score"],x["member_source_sha256"]))
    out=[]; used=set(); prior_ex=collision=0
    for x in hs:
        m=set(x["member_source_sha256"])
        if m&prior: prior_ex+=1; continue
        if m&used: collision+=1; continue
        out.append({**x,"batch_id":"SN-LEX-B037","batch_rank":len(out)+1,"discovery_route":"LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION","review_state":"UNREVIEWED_FULL_SOURCE","claim_boundary":"Fresh-source lexical reading priority only; complete original sources remain authoritative for later decisions. Not dense semantic coverage or a cluster result."})
        used|=m
        if len(out)==25: break
    if len(out)!=25 or len(used)!=75 or used&prior: raise SystemExit("Could not form source-disjoint B037")
    O.mkdir(parents=True)
    Q.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in out),encoding="utf-8")
    s={"status":"PASS_SOURCE_NATIVE_LEXICAL_ONLY_CONTINUATION_B037_UNREVIEWED_FAMILY_HYPOTHESES","bound_inputs":{rel(P):digest(P),rel(H):digest(H),"prior_reconciliation_keys":{f"B{b:03d}":digest(p) for b,p in sorted(found.items())}},"parameters":{"batch_families":25,"fresh_source_policy":"exclude_all_source_hashes_in_B001_to_B036; disjoint_members_within_B037","ranking_rule":"frozen_reciprocal_link_count_then_rank_fusion_then_distinct_source_paths_then_sorted_member_hashes","discovery_route":"LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION","dense_status":"NOT_EXECUTED_NO_PROVIDER_CREDENTIAL_IN_PROCESS_ENVIRONMENT_NO_PROVIDER_CONTACT"},"counts":{"prior_batches":36,"prior_source_hashes":len(prior),"b037_families":25,"b037_sources":len(used),"hypotheses_excluded_due_to_prior_source_overlap":prior_ex,"hypotheses_excluded_due_to_b037_source_collision":collision},"outputs":{Q.name:digest(Q)},"claim_boundary":"B037 source-reading queue only; no review, prompt, adequacy, admission, acceptable-set, selector, or metric result has occurred."}
    (O/"summary.json").write_text(json.dumps(s,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(s,ensure_ascii=False,sort_keys=True))
if __name__=="__main__": main()
