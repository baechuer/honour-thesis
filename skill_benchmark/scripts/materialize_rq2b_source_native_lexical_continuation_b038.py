#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
W=Path(__file__).resolve().parents[2];N=W/'skill_benchmark/rq2b_naturalistic_confusability';R=N/'review';P=R/'SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md';H=R/'source_native_lexical_bootstrap_2026-09-04/all_mutual_triangle_hypotheses.jsonl';O=R/'source_native_dense_lexical_union_b038_2026-09-04';Q=O/'batch_038_full_source_review_queue_internal.jsonl'
def rs(p):return [json.loads(x) for x in p.read_text().splitlines() if x]
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise SystemExit('output exists')
 keys={};pat=re.compile(r'batch_(\d+)_full_source_review_packets/internal_reconciliation_key\.jsonl$')
 for p in R.glob('**/internal_reconciliation_key.jsonl'):
  m=pat.search(str(p.relative_to(W)))
  if m and int(m.group(1))<=37:keys[int(m.group(1))]=p
 if set(keys)!=set(range(1,38)):raise SystemExit('incomplete ledger')
 prior=set()
 for b,p in keys.items():
  a=rs(p)
  if len(a)!=75:raise SystemExit('bad ledger')
  prior|={x['canonical_source_sha256'] for x in a}
 if len(prior)!=2775:raise SystemExit('reuse ledger')
 hs=rs(H);hs.sort(key=lambda x:(-x['reciprocal_link_count'],-x['rank_fusion_score'],x['member_source_sha256']))
 out=[];used=set()
 for x in hs:
  m=set(x['member_source_sha256'])
  if m&prior or m&used:continue
  out.append({**x,'batch_id':'SN-LEX-B038','batch_rank':len(out)+1,'discovery_route':'LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION','review_state':'UNREVIEWED_FULL_SOURCE','claim_boundary':'Fresh-source lexical reading priority only; not a cluster result.'});used|=m
  if len(out)==25:break
 if len(out)!=25 or len(used)!=75 or used&prior:raise SystemExit('selection failure')
 O.mkdir(parents=True);Q.write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in out))
 s={'status':'PASS_SOURCE_NATIVE_LEXICAL_ONLY_CONTINUATION_B038_UNREVIEWED_FAMILY_HYPOTHESES','bound_inputs':{'protocol':sh(P),'hypotheses':sh(H),'prior_keys':{f'B{b:03d}':sh(p) for b,p in keys.items()}},'counts':{'prior_batches':37,'prior_source_hashes':len(prior),'b038_families':25,'b038_sources':75},'outputs':{Q.name:sh(Q)},'claim_boundary':'Queue only; no review, prompt, admission, or metric.'};(O/'summary.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n');print(json.dumps(s))
if __name__=='__main__':main()
