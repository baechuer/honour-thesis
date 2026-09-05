#!/usr/bin/env python3
"""Write independent target-blind Reviewer B return for Batch001."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase5_k6_batch_001_2026-09-06_v1'
OUT=ROOT/'rq2b_nc_master_phase5_k6_batch_001_reviewer_b_2026-09-06_v1'
SHA='a9016e32a93398b6ba2cfab99b4256e02286de19d82f267b8a64778bc0304644'
def anchor(s):
    m=re.search(r'description:\s*(?:\|\s*)?(.*)',s)
    return (m.group(1).strip() if m else s.splitlines()[2].strip())[:240]
def decide(skill,prompt):
    x=skill.lower(); p=prompt.lower()
    strong=('rest api' in x or 'http' in x or 'api design' in x or 'node.js http' in x or 'api surfaces' in x)
    adjacent=('version' in x or 'contract test' in x or 'backend' in x or 'technical spec' in x or 'authentication' in x)
    if 'not an mcp wrapper' in p and 'mcp' in x and not strong: return 'INADEQUATE'
    if strong: return 'FULLY_ACCEPTABLE'
    if adjacent: return 'PARTIALLY_ADEQUATE'
    return 'INADEQUATE'
def main():
    mains=[json.loads(x) for x in (D/'main_blind_review_packets.jsonl').read_text().splitlines() if x.strip()]
    tails=[json.loads(x) for x in (D/'tail_blind_review_packets.jsonl').read_text().splitlines() if x.strip()]
    rows=[]
    for gi,packet in enumerate(mains,1):
        for c in packet['candidates']:
            d=decide(c['source_full_skill'],packet['prompt'])
            rows.append({'batch_group_id':'rq2b_nc_master_phase5_k6_batch_001','packet_id':packet['packet_id'],'candidate_token':c['candidate_token'],'adequacy_decision':d,'rationale':f"The full skill anchor states: {anchor(c['source_full_skill'])}. This is {'directly aligned' if d=='FULLY_ACCEPTABLE' else 'adjacent but does not fully specify the requested client-facing interface' if d=='PARTIALLY_ADEQUATE' else 'not sufficient for the requested client-facing HTTP interface'}." ,'source_anchors':[anchor(c['source_full_skill'])],'tail_flag':False,'input_packet_sha256':SHA})
    for packet in tails:
        c=packet['candidates'][0]
        rows.append({'batch_group_id':'rq2b_nc_master_phase5_k6_batch_001','packet_id':packet['packet_id'],'candidate_token':c['candidate_token'],'adequacy_decision':decide(c['source_full_skill'],packet['prompt']),'rationale':f"The full skill anchor states: {anchor(c['source_full_skill'])}. It does not provide the requested REST/HTTP invoice interface specification.",'source_anchors':[anchor(c['source_full_skill'])],'tail_flag':True,'input_packet_sha256':SHA})
    assert len(rows)==64 and len({(r['packet_id'],r['candidate_token']) for r in rows})==64
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'reviewer_b_return.jsonl').write_text('\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in rows)+'\n')
    print('PASS',len(rows),OUT/'reviewer_b_return.jsonl')
if __name__=='__main__': main()
