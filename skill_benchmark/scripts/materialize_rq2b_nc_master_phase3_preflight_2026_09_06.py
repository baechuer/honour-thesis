#!/usr/bin/env python3
"""Append-only Master Phase-3 structural preflight (no retrieval or embedding).

This controller deliberately emits a blocked/needs-review package when the
semantic checks cannot be established mechanically.  It never changes a
historical manifest and never creates an audit input or acceptable-set label.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NC = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
M = NC / "manifests"
SOP = NC / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
P0 = M / "rq2b_nc_master_phase0_reconciliation_2026-09-06_v1"
P1 = M / "rq2b_nc_master_phase1_reconciliation_2026-09-06_v1"
BASE = M / "current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
HISTORICAL = M / "rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2/candidate_source_union.jsonl"
PARENT = ROOT / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def rel(p): return str(p.relative_to(ROOT))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output-dir", type=Path, required=True); a=ap.parse_args()
    out=a.output_dir.resolve()
    if out.exists(): raise SystemExit(f"Refusing to overwrite append-only output: {out}")
    bound={}; blockers=[]; checks=[]
    required=[SOP, P0/"summary.json", P1/"summary.json", P1/"source_union.jsonl", P1/"family_state_ledger.jsonl", P0/"phase0_family_state.jsonl", P0/"phase0_batch_state.jsonl", BASE, HISTORICAL, PARENT]
    for p in required:
        if p.is_file(): bound[rel(p)]=digest(p)
        else: blockers.append({"check": "required_binding", "status":"BLOCK", "path":rel(p)})
    terminal=[]
    if (P1/"source_union.jsonl").is_file():
        terminal=rows(P1/"source_union.jsonl")
    checks.append({"check":"phase1_terminal_source_rows","status":"PASS" if len(terminal)==147 else "BLOCK","observed":len(terminal),"expected":147})
    if len(terminal)!=147: blockers.append(checks[-1])
    hashes=[r.get("canonical_source_sha256") for r in terminal]
    bad=[r for r in terminal if not isinstance(r.get("canonical_source_sha256"),str) or not re.fullmatch(r"[0-9a-f]{64}",r["canonical_source_sha256"])]
    dup=[h for h,n in defaultdict(int).items()]
    counts=defaultdict(int)
    for h in hashes: counts[h]+=1
    duplicate_hashes=sorted(h for h,n in counts.items() if n>1)
    checks.append({"check":"exact_sha_source_union","status":"PASS" if not bad else "BLOCK","invalid_rows":len(bad),"unique_hashes":len(set(hashes))})
    if bad: blockers.append(checks[-1])
    checks.append({"check":"exact_duplicate_or_alias_hashes","status":"BLOCK" if duplicate_hashes else "PASS","duplicate_hashes":duplicate_hashes})
    if duplicate_hashes: blockers.append(checks[-1])
    # B052 is explicitly the fresh 3-member closure; reject historical five-row material.
    b052=[r for r in terminal if r.get("batch")=="B052"]
    checks.append({"check":"B052_fresh_closure","status":"PASS" if len(b052)==9 else "BLOCK","rows":len(b052),"note":"fresh 3-member families only; historical 5-member rows excluded"})
    if len(b052)!=9: blockers.append(checks[-1])
    historical = rows(HISTORICAL) if HISTORICAL.is_file() else []
    historical_by_hash = {r.get("canonical_source_sha256"): r for r in historical}
    fresh_b052 = {r.get("canonical_source_sha256") for r in b052}
    old_b052 = {h for h,r in historical_by_hash.items() if any(x.get("discovery_batch")=="B052" for x in r.get("local_nc_origin_records", []))}
    removed = sorted(old_b052 - fresh_b052)
    additions = [r for r in terminal if r.get("batch") in {"B013","B015"} and r.get("canonical_source_sha256") not in historical_by_hash]
    provenance_cache={}
    for r in terminal:
        if r.get("batch") in {"B013","B015"} and isinstance(r.get("origin"),str):
            q=ROOT/r["origin"]
            if q.is_file(): provenance_cache.update({x.get("canonical_source_sha256"):x for x in rows(q)})
    provenance_missing=[]
    union = dict(historical_by_hash)
    for h in removed: union.pop(h, None)
    for r in additions:
        h=r["canonical_source_sha256"]; p=provenance_cache.get(h)
        if not isinstance(p,dict) or not p.get("source_paths"): provenance_missing.append(h); continue
        union[h]={"canonical_source_sha256":h,"historical_base_candidate":None,"local_nc_origin_records":[{"phase_stratum":"MASTER_PHASE1","discovery_batch":r.get("batch"),"family_token":r.get("family_token"),"member_token":p.get("member_token"),"provenance_record":p,"source_paths":p.get("source_paths")} ]}
    checks.append({"check":"prospective_source_canonical_union_rebuild","status":"PASS" if len(historical)==3810 and len(removed)==6 and len(additions)==9 and len(union)==3813 and not provenance_missing else "BLOCK","historical":len(historical),"removed":len(removed),"added":len(additions),"rebuilt":len(union),"provenance_missing":provenance_missing})
    if checks[-1]["status"]!="PASS": blockers.append(checks[-1])
    families=defaultdict(list)
    for r in terminal: families[(r.get("batch"),r.get("family_token"))].append(r)
    triad_bad=[k for k,v in families.items() if len(v)!=3 or len({x.get("canonical_source_sha256") for x in v})!=3]
    checks.append({"check":"member_triads","status":"PASS" if not triad_bad else "BLOCK","family_count":len(families),"bad_families":triad_bad})
    if triad_bad: blockers.append(checks[-1])
    # Prompt and semantic checks are intentionally fail-closed until a reviewer-bound closure exists.
    semantic=["semantic_near_copy","prompt_target_provider_repository_path_cues"]
    for name in semantic:
        item={"check":name,"status":"NEEDS_REVIEW","reason":"not decidable from exact hashes/mechanical fields; no PASS by assumption"}; blockers.append(item); checks.append(item)
    parents=rows(PARENT) if PARENT.is_file() else []
    parent_ids=[r.get("prompt_id") for r in parents]; parent_texts=[r.get("prompt_sha256") for r in parents]
    pc={"check":"parent_v3_prompt_identity_set","status":"PASS" if len(parents)==381 and len(set(parent_ids))==381 and len(set(parent_texts))==381 else "BLOCK","rows":len(parents),"unique_prompt_ids":len(set(parent_ids)),"unique_prompt_text_hashes":len(set(parent_texts))}
    checks.append(pc)
    if pc["status"]!="PASS": blockers.append(pc)
    status="BLOCKED_MASTER_PHASE3_PREFLIGHT" if blockers else "PASS_MASTER_PHASE3_STRUCTURAL_PREFLIGHT_SEMANTIC_QA_PENDING"
    summary={"status":status,"claim_boundary":"Preflight only; no retrieval, embedding, audit-input freeze, acceptable-set label, metric, or thesis result.","counts":{"terminal_source_rows":len(terminal),"terminal_families":len(families),"unique_exact_source_hashes":len(set(hashes)),"historical_union":len(historical),"union_removed":len(removed),"union_added":len(additions),"prospective_union":len(union),"blockers":len(blockers)},"checks":checks,"blockers":blockers,"bound_inputs":dict(sorted(bound.items())),"union_change_log":{"removed_b052_hashes":removed,"added_master_phase1_hashes":sorted(r["canonical_source_sha256"] for r in additions)}}
    out.mkdir(parents=True)
    (out/"terminal_source_union.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in terminal),encoding="utf-8")
    (out/"candidate_source_union.jsonl").write_text("".join(json.dumps(union[h],sort_keys=True)+"\n" for h in sorted(union)),encoding="utf-8")
    (out/"union_change_log.json").write_text(json.dumps(summary["union_change_log"],indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (out/"preflight_checks.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in checks),encoding="utf-8")
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"output_dir":str(out),"status":status,"counts":summary["counts"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
