from __future__ import annotations
import hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
M = BASE / "manifests/rq2b_nc_master_phase4_current_nc_prompt_composite_2026-09-06_v1"
OUT = BASE / "manifests/rq2b_nc_master_phase4_current_nc_prompt_composite_audit_2026-09-06_v3"

def sha(p: Path) -> str:
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def text_sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()
def loadj(p): return json.loads(p.read_text())
def main():
    defects=[]; checks=[]
    manifest=loadj(M/'manifest.json'); rows=[json.loads(x) for x in (M/'composite_prompt_binding_rows.jsonl').read_text().splitlines() if x.strip()]
    checks.append({'check':'manifest_declares_9_rows_3_families','pass':manifest.get('counts')=={'families':3,'members_per_family':[3,3,3],'rows':9}})
    if not checks[-1]['pass']: defects.append(checks[-1])
    checks.append({'check':'row_count','pass':len(rows)==9,'observed':len(rows)})
    if len(rows)!=9: defects.append(checks[-1])
    fams=defaultdict(list)
    for r in rows:fams[r.get('family_token')].append(r)
    checks.append({'check':'three_families_three_rows','pass':len(fams)==3 and sorted(map(len,fams.values()))==[3,3,3],'observed':{k:len(v) for k,v in fams.items()}})
    if not checks[-1]['pass']: defects.append(checks[-1])
    pids=[r.get('canonical_prompt_id') for r in rows]; members=[(r.get('family_token'),r.get('member_token')) for r in rows]
    for name, vals in [('unique_prompt_ids',pids),('unique_family_member_pairs',members)]:
        c={'check':name,'pass':len(vals)==len(set(vals))}; checks.append(c)
        if not c['pass']: defects.append(c)
    required={'PASS_CURRENT_NC_PROMPT_BINDING','PASS_CURRENT_NC_PROMPT_COMPOSITE'}
    for i,r in enumerate(rows):
        ok=True; reasons=[]
        if r.get('binding_status')!='PASS_CURRENT_NC_PROMPT_BINDING': ok=False; reasons.append('binding_status')
        if r.get('composite_binding_status')!='PASS_CURRENT_NC_PROMPT_COMPOSITE': ok=False; reasons.append('composite_binding_status')
        if not isinstance(r.get('author_prompt'),str) or text_sha(r['author_prompt'])!=r.get('author_prompt_sha256'): ok=False; reasons.append('prompt_sha')
        f=r.get('final_local_disposition') or {}
        if f.get('final_prompt_disposition')!='PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT': ok=False; reasons.append('final_disposition')
        if f.get('intended_target_blind_decision') not in (None,'MOST_SUITABLE'): ok=False; reasons.append('target_decision')
        if f.get('prompt_integrity')!='CUE_SAFE': ok=False; reasons.append('cue_safe')
        vis=r.get('source_visible_candidate_set') or []
        if len(vis)!=3 or len({x.get('canonical_source_sha256') for x in vis})!=3: ok=False; reasons.append('three_visible_sources')
        for x in vis:
            if x.get('provenance_preflight_status')!='PASS_BACKGROUND_PIN_LICENSE_AND_BYTE_REPLAY' or x.get('source_byte_replay') not in (None,'PASS_SHA256_MATCH'): ok=False; reasons.append('provenance_status')
            if x.get('source_path') and Path(x['source_path']).exists() and sha(ROOT/x['source_path']) != x.get('canonical_source_sha256'): ok=False; reasons.append('source_replay')
            if x.get('source_path_sha256') and x.get('source_path_sha256') != x.get('canonical_source_sha256'): ok=False; reasons.append('source_path_sha')
        ph=r.get('phase3_linkage') or {}
        if not ph.get('prompt_cue_screen') or len(ph.get('prompt_relation_packet_ids') or [])!=5: ok=False; reasons.append('phase3_linkage')
        target=r.get('target_canonical_source_sha256')
        if target and target not in {x.get('canonical_source_sha256') for x in vis}: ok=False; reasons.append('target_not_in_visible_set')
        if target and r.get('target_source_sha256') and target != r.get('target_source_sha256'): ok=False; reasons.append('target_sha_alias')
        c={'check':'row_%02d_integrity'%(i+1),'pass':ok,'family':r.get('family_token'),'prompt':r.get('canonical_prompt_id'),'reasons':reasons}
        checks.append(c)
        if not ok: defects.append(c)
    # Validate all declared composite input digests and existence.
    inp=[]
    for rel, expected in (manifest.get('inputs') or {}).items():
        p=ROOT/rel; ok=p.exists() and sha(p)==expected
        c={'check':'declared_input_sha:'+rel,'pass':ok,'observed_sha':sha(p) if p.exists() else None,'expected_sha':expected}
        checks.append(c); inp.append(c)
        if not ok: defects.append(c)
    # Existing current binding must be exactly represented, with fresh v6 rows allowed only for the five repaired prompts.
    origins=Counter(r.get('composite_origin') for r in rows)
    checks.append({'check':'origin_counts','pass':origins==Counter({'EXISTING_CURRENT_PASS':4,'FRESH_REMEDIATION_FINALIZED_V6':5}),'observed':dict(origins)})
    if checks[-1]['pass'] is False: defects.append(checks[-1])
    status='PASS_CURRENT_NC_PROMPT_COMPOSITE_MECHANICAL_AUDIT_NO_FREEZE_NO_EXPERIMENT' if not defects else 'BLOCKED_CURRENT_NC_PROMPT_COMPOSITE_MECHANICAL_AUDIT'
    report={'status':status,'claim_boundary':'Mechanical current NC prompt composite identity/provenance/evidence audit only; no freeze, K=6 audit, acceptable-set admission, retrieval, embedding, provider, metric, or experiment result.','counts':{'rows':len(rows),'families':len(fams),'defects':len(defects),'checks':len(checks),'origin_counts':dict(origins)},'checks':checks,'defects':defects,'inputs':{'composite_manifest':str(M/'manifest.json'),'composite_rows':str(M/'composite_prompt_binding_rows.jsonl'),'composite_manifest_sha256':sha(M/'manifest.json'),'composite_rows_sha256':sha(M/'composite_prompt_binding_rows.jsonl')}}
    OUT.mkdir(parents=True,exist_ok=False); (OUT/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':status,'rows':len(rows),'families':len(fams),'defects':len(defects),'report':str(OUT/'report.json')},indent=2))
    raise SystemExit(0 if not defects else 2)
if __name__=='__main__': main()
