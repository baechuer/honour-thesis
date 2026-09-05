import hashlib, json, os, subprocess
from pathlib import Path

ROOT = Path('/Users/jackyzhang/Work/Honour Thesis')
BASE = ROOT/'skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1'
OUT = ROOT/'skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase3_return_integrity_2026-09-06_v2'
OUT.mkdir(parents=True, exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def rows(p):
    if not p.exists(): return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def paths(obj, out):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if 'path' in k.lower() and isinstance(v,str): out.append((k,v))
            paths(v,out)
    elif isinstance(obj,list):
        for v in obj: paths(v,out)

def audit(kind, packet_name, expected, ret_a, ret_b, allowed):
    packet=BASE/packet_name
    psha=sha(packet) if packet.exists() else None
    result={'kind':kind,'packet':str(packet),'packet_exists':packet.exists(),'packet_sha256':psha,'expected':expected,'reviewers':{}}
    packet_rows=rows(packet)
    ids=[r.get('packet_id') for r in packet_rows]
    result['packet_rows']=len(packet_rows); result['packet_unique_ids']=len(set(ids)); result['packet_duplicate_ids']=len(ids)-len(set(ids))
    path_checks=[]
    for r in packet_rows:
        vals=[]; paths(r,vals)
        for k,v in vals:
            if v.startswith('/') or v.startswith('skill_benchmark/'):
                q=Path(v) if v.startswith('/') else ROOT/v
                path_checks.append({'field':k,'path':v,'exists':q.exists()})
    result['referenced_paths']=path_checks
    result['path_failures']=[x for x in path_checks if not x['exists']]
    for label, file_name, reviewer in [('A',ret_a,'A'),('B',ret_b,'B')]:
        p=BASE.parent/file_name
        exists=p.exists(); rs=rows(p)
        bad=[]
        for r in rs:
            if r.get('reviewer')!=reviewer: bad.append('reviewer_field')
            if r.get('relation_decision') not in allowed and kind!='cue': bad.append('decision_domain')
            if kind=='cue' and r.get('cue_decision') not in allowed: bad.append('decision_domain')
            if not isinstance(r.get('rationale'),str) or not r.get('rationale').strip(): bad.append('missing_rationale')
            if not isinstance(r.get('source_anchors'),list): bad.append('missing_source_anchors')
            if r.get('semantic_packet_sha256')!=psha: bad.append('packet_sha_mismatch')
        rid=[r.get('packet_id') for r in rs]; expected_ids=set(ids)
        result['reviewers'][label]={'path':str(p),'exists':exists,'rows':len(rs),'unique_ids':len(set(rid)),'duplicate_ids':len(rid)-len(set(rid)),'missing_ids':sorted(expected_ids-set(rid)),'extra_ids':sorted(set(rid)-expected_ids),'bad_records':sorted(set(bad)),'all_sha_match':bool(rs) and all(r.get('semantic_packet_sha256')==psha for r in rs)}
    return result

relation={'DUPLICATE_CLUSTER','RELATED_BUT_DISTINCT','BLOCKED_OR_UNCLEAR'}
cue={'AVOIDABLE_IDENTITY_CUE','DECLARED_NECESSARY_CUE_STRATUM','NOT_A_CUE','UNCLEAR'}
audits=[audit('source_relation','source_relation_reviewer_packet.jsonl',45,'rq2b_nc_master_phase3_changed_scope_source_reviewer_a_2026-09-06_v1/reviewer_a_return.jsonl','rq2b_nc_master_phase3_changed_scope_source_reviewer_b_2026-09-06_v1/reviewer_b_return.jsonl',relation), audit('prompt_relation','prompt_relation_reviewer_packet.jsonl',45,'rq2b_nc_master_phase3_changed_scope_prompt_reviewer_a_2026-09-06_v1/reviewer_a_return.jsonl','rq2b_nc_master_phase3_changed_scope_prompt_reviewer_b_2026-09-06_v1/reviewer_b_return.jsonl',relation)]
cue_screen=rows(BASE/'prompt_cue_screen.jsonl')
cue_packet=BASE/'prompt_cue_reviewer_packet.jsonl'
audits.append({'kind':'prompt_cue','screen_rows':len(cue_screen),'screen_unique_ids':len({r.get('packet_id') for r in cue_screen}),'screen_dispositions':sorted({r.get('mechanical_disposition') for r in cue_screen}),'screen_all_no_signal':len(cue_screen)==9 and all(r.get('mechanical_disposition')=='PASS_NO_MECHANICAL_CUE_SIGNAL' for r in cue_screen),'packet_exists':cue_packet.exists(),'packet_rows':len(rows(cue_packet)),'packet_sha256':sha(cue_packet) if cue_packet.exists() else None,'expected_reviewer_returns':0,'reviewers':{}})
issues=[]
for a in audits:
    if a['kind']=='prompt_cue':
        if not a['screen_all_no_signal'] or a['packet_rows']!=0: issues.append('prompt_cue mechanical screen/empty packet inconsistency')
        continue
    for who,x in a['reviewers'].items():
        if not x['exists']: issues.append(f"{a['kind']} reviewer {who}: BLOCKED_MISSING_RETURN")
        if x['rows']!=a['expected'] or x['missing_ids'] or x['extra_ids'] or x['bad_records']: issues.append(f"{a['kind']} reviewer {who}: integrity failure")
report={'status':'PASS_RETURN_INTEGRITY' if not issues else 'BLOCKED_RETURN_INTEGRITY','scope':'Mechanical integrity only; no semantic decisions or library admission.','audits':audits,'issues':issues}
report['git_diff_check']=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True).stdout
(OUT/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'issues':issues,'output':str(OUT/'report.json')},ensure_ascii=False))
