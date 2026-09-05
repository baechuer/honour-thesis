#!/usr/bin/env python3
"""Deterministic, fail-closed Phase-3 changed-scope reconciliation."""
import argparse,hashlib,json
from pathlib import Path
DOM={'source_relation':{'DUPLICATE_CLUSTER','RELATED_BUT_DISTINCT','BLOCKED_OR_UNCLEAR'},'prompt_relation':{'RELATED_BUT_DISTINCT','SPLIT_LEAKAGE','TRANSFORMED_DUPLICATE','UNCLEAR'},'prompt_cue':{'AVOIDABLE_IDENTITY_CUE','DECLARED_NECESSARY_CUE_STRATUM','NOT_A_CUE','UNCLEAR'}}
def load(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []
def dg(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--packet-dir',type=Path,default=Path('skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1')); ap.add_argument('--reviewer-a',type=Path,action='append'); ap.add_argument('--reviewer-b',type=Path,action='append'); ap.add_argument('--coordinator',type=Path,action='append'); ap.add_argument('--out',type=Path,default=Path('skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_changed_scope_qa_reconciliation_2026-09-06_v3')); a=ap.parse_args(); d,o=a.packet_dir,a.out; o.mkdir(parents=True,exist_ok=True)
 files={k:d/(k+'_reviewer_packet.jsonl') for k in DOM}; packets={k:load(v) for k,v in files.items()}; expected={k:[x.get('packet_id') for x in v] for k,v in packets.items()}; errs=[]
 for k,v in expected.items():
  if None in v or len(v)!=len(set(v)): errs.append(k+':duplicate_or_missing_packet_id')
 allid=set(sum(expected.values(),[])); kind={p:k for k,vs in expected.items() for p in vs}
 def read(ps): return sum((load(p) for p in (ps or [])),[])
 ar,br,cr=read(a.reviewer_a),read(a.reviewer_b),read(a.coordinator)
 def index(v,who):
  z={}
  for x in v:
   p=x.get('packet_id')
   if p in z: errs.append(who+':duplicate_return:'+str(p))
   z[p]=x
  return z
 A,B,C=index(ar,'A'),index(br,'B'),index(cr,'C')
 def validate(v,w,coord=False):
  for x in v:
   p=x.get('packet_id'); k=kind.get(p); dec=x.get('relation_decision') or x.get('cue_decision')
   if not k: errs.append(w+':unexpected:'+str(p)); continue
   if x.get('reviewer')!=w: errs.append(w+':wrong_reviewer:'+str(p))
   if dec not in DOM[k]: errs.append(w+':bad_decision:'+str(p))
   if not x.get('rationale') or not isinstance(x.get('source_anchors'),list): errs.append(w+':missing_rationale_or_anchors:'+str(p))
   h=x.get('semantic_packet_sha256') or x.get('packet_sha256')
   if h!=dg(files[k]): errs.append(w+':collection_hash_mismatch:'+str(p))
 validate(ar,'A'); validate(br,'B')
 disagreements={p for p in allid if A.get(p) and B.get(p) and (A[p].get('relation_decision') or A[p].get('cue_decision'))!=(B[p].get('relation_decision') or B[p].get('cue_decision'))}
 if set(C)!=disagreements: errs.append('coordinator:exact_disagreement_id_set_required')
 validate(cr,'C',True)
 rec=[]; sealed=[]
 for p in sorted(allid):
  x,y=A.get(p),B.get(p)
  if not x or not y: rec.append({'packet_id':p,'status':'BLOCKED_MISSING_RETURNS'}); continue
  dx=x.get('relation_decision') or x.get('cue_decision'); dy=y.get('relation_decision') or y.get('cue_decision'); c=C.get(p)
  if p in disagreements:
   if not c: rec.append({'packet_id':p,'status':'BLOCKED_MISSING_COORDINATOR'}); continue
   dec=c.get('relation_decision') or c.get('cue_decision')
   st='RETAINED_AGREEMENT' if dec in {'RELATED_BUT_DISTINCT','NOT_A_CUE'} else ('DECLARED_NECESSARY_CUE_STRATUM' if dec=='DECLARED_NECESSARY_CUE_STRATUM' else ('REMEDIATION_OR_EXCLUSION_REQUIRED' if dec in {'DUPLICATE_CLUSTER','SPLIT_LEAKAGE','TRANSFORMED_DUPLICATE','AVOIDABLE_IDENTITY_CUE'} else 'BLOCKED_UNCLEAR'))
   rec.append({'packet_id':p,'status':st,'decision':dec}); sealed.append({'packet_id':p,'reviewer_a_decision':dx,'reviewer_b_decision':dy,'review_boundary':'Packet-only; no targets, rankings, retrieval outcomes, or acceptable-set history.'}); continue
  dec=dx
  if dec in {'RELATED_BUT_DISTINCT','NOT_A_CUE'}: st='RETAINED_AGREEMENT'
  elif dec=='DECLARED_NECESSARY_CUE_STRATUM': st='DECLARED_NECESSARY_CUE_STRATUM'
  elif dec in {'DUPLICATE_CLUSTER','SPLIT_LEAKAGE','TRANSFORMED_DUPLICATE','AVOIDABLE_IDENTITY_CUE'}: st='REMEDIATION_OR_EXCLUSION_REQUIRED'
  else: st='BLOCKED_UNCLEAR'
  rec.append({'packet_id':p,'status':st,'decision':dec})
 (o/'sealed_disagreement_packets.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in sealed))
 blockers=errs+['BLOCKED_MISSING_HISTORICAL_SOURCE_PROVENANCE'] if not packets['prompt_relation'] else errs
 good=all(x['status'] in {'RETAINED_AGREEMENT','DECLARED_NECESSARY_CUE_STRATUM','COORDINATOR_DECISION'} for x in rec) and not blockers and set(A)==allid==set(B)
 status='PASS_CHANGED_SCOPE_RECONCILIATION' if good else ('BLOCKED_SOURCE_ONLY_PARTIAL' if packets['source_relation'] and not packets['prompt_relation'] else 'BLOCKED_CHANGED_SCOPE_RECONCILIATION')
 summary={'status':status,'counts':{k+'_packets':len(v) for k,v in packets.items()}|{'records':len(rec),'A_returns':len(ar),'B_returns':len(br),'coordinator_returns':len(cr),'sealed_disagreements':len(sealed)},'collection_sha256':{k:dg(v) for k,v in files.items()},'return_input_sha256':{'A':[dg(p) for p in (a.reviewer_a or [])],'B':[dg(p) for p in (a.reviewer_b or [])],'C':[dg(p) for p in (a.coordinator or [])]},'validation_errors':blockers,'historical_decisions_inherited':False,'retrieval_or_embedding_executed':False}
 (o/'final_record_status.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in rec)); (o/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n'); print(json.dumps(summary,indent=2)); return 0 if good else 2
if __name__=='__main__': raise SystemExit(main())
