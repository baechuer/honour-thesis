import json, glob, os

root = 'skill_benchmark/rq2b_naturalistic_confusability/manifests'
cl = root + '/rq2b_nc_master_phase3_closure_2026-09-06_v1'
checks, blockers = [], []
def check(name, ok, observed=None):
    checks.append({'check': name, 'status': 'PASS' if ok else 'BLOCK', 'observed': observed})
    if not ok: blockers.append(name)
def rows(path):
    return [json.loads(line) for line in open(path) if line.strip()]

u = rows(root + '/rq2b_nc_master_phase3_preflight_2026-09-06_v1/candidate_source_union.jsonl')
t = rows(root + '/rq2b_nc_master_phase3_preflight_2026-09-06_v1/terminal_source_union.jsonl')
check('delta_arithmetic', 3810 - 6 + 9 == 3813, '3810 - 6 + 9 = 3813')
check('prospective_union_count', len(u) == 3813, len(u))
check('terminal_count', len(t) == 147, len(t))
families = {x.get('family_token') for x in t}
sizes = {f: sum(x.get('family_token') == f for x in t) for f in families}
check('terminal_49_triads', len(families) == 49 and set(sizes.values()) == {3}, {'families': len(families), 'sizes': sorted(set(sizes.values()))})

for kind, packet, a, b in [
    ('source', 'source_relation_reviewer_packet.jsonl', 'rq2b_nc_master_phase3_changed_scope_source_reviewer_a_2026-09-06_v1/reviewer_a_return.jsonl', 'rq2b_nc_master_phase3_changed_scope_source_reviewer_b_2026-09-06_v1/reviewer_b_return.jsonl'),
    ('prompt', 'prompt_relation_reviewer_packet.jsonl', 'rq2b_nc_master_phase3_changed_scope_prompt_reviewer_a_2026-09-06_v1/reviewer_a_return.jsonl', 'rq2b_nc_master_phase3_changed_scope_prompt_reviewer_b_2026-09-06_v1/reviewer_b_return.jsonl')]:
    p = root + '/rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1/' + packet
    ids = {x.get('packet_id') or x.get('record_id') for x in rows(p)}
    obs = []
    for path in (a, b):
        rr = rows(root + '/' + path)
        rids = {x.get('packet_id') or x.get('record_id') for x in rr}
        obs.append({'rows': len(rr), 'unique_ids': len(rids), 'same_ids': rids == ids})
    check(kind + '_returns_45_ab', all(x['rows'] == 45 and x['unique_ids'] == 45 and x['same_ids'] for x in obs), obs)

cue = rows(root + '/rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1/prompt_cue_screen.jsonl')
cp = rows(root + '/rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1/prompt_cue_reviewer_packet.jsonl')
check('cue_9_no_signal_zero_packets', len(cue) == 9 and len(cp) == 0, {'screen': len(cue), 'packets': len(cp)})
blob = '\n'.join(open(p, errors='ignore').read().lower() for p in glob.glob(cl + '/*'))
check('no_execution_or_results_claimed', 'retrieval_or_embedding_executed": false' in blob and 'no audit-input freeze' in blob)
summary = json.load(open(cl + '/summary.json'))
check('superseded_dry_run_excluded', 'superseded_before_final_replay' not in str(summary.get('final_artifact', '')), summary.get('final_artifact'))
report = {'status': 'PASS_PHASE3_CLOSURE_MECHANICAL_INTEGRITY' if not blockers else 'BLOCK_PHASE3_CLOSURE_MECHANICAL_INTEGRITY', 'checks': checks, 'blockers': blockers, 'scope': 'Independent mechanical audit only; no semantic decisions; no canonical union modification; no retrieval, embedding, provider, metric, or experiment execution.'}
out = root + '/rq2b_nc_master_phase3_closure_integrity_2026-09-06_v1/report.json'
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w') as f: json.dump(report, f, indent=2); f.write('\n')
print(json.dumps(report, indent=2))
