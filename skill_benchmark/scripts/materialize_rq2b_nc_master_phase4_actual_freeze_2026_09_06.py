#!/usr/bin/env python3
"""Build a fresh outcome-blind K=6 packet from the current Master state.

This adapter deliberately reconstructs current inputs; it does not copy old
packet rows or outcomes.  It delegates deterministic, source-native navigation
and opaque packet construction to the existing audited implementation.
"""
from __future__ import annotations
import hashlib, importlib.util, json, re, shutil, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
M = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/manifests"
CUR = M / "rq2b_nc_master_phase3_preflight_2026-09-06_v1"
TERM = CUR / "terminal_source_union.jsonl"
UNION = CUR / "candidate_source_union.jsonl"
PARENT = ROOT / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
OLD = M / "rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2"
COMP = M / "rq2b_nc_master_phase4_current_nc_prompt_composite_2026-09-06_v1/composite_prompt_binding_rows.jsonl"
OUT = M / "RQ2b-NC-master-phase4-audit-input-2026-09-06_v2"
AD = M / "rq2b_nc_master_phase4_actual_freeze_adapter_2026-09-06_v1"
ADP = M / "rq2b_nc_master_phase4_actual_freeze_profiles_2026-09-06_v1"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def dump(p, xs): p.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True)+"\n" for x in xs), encoding="utf-8")
def source_path(row):
    h=row["canonical_source_sha256"]
    hist=row.get("historical_base_candidate",{})
    b=hist.get("provenance_binding",{}) if isinstance(hist,dict) else {}
    if b.get("source_path"):
        return b["source_path"] if b["source_path"].startswith("skill_benchmark/") else "skill_benchmark/" + b["source_path"]
    if isinstance(hist, dict):
        for rec in hist.get("rq1_records", []) + hist.get("rq1_exact_reuse_records", []) + hist.get("v3_identity_records", []):
            if isinstance(rec, dict) and isinstance(rec.get("source_path"), str):
                p=rec["source_path"]; return p if p.startswith("skill_benchmark/") else "skill_benchmark/"+p
    for origin in row.get("local_nc_origin_records", []):
        if isinstance(origin, dict):
            for p in origin.get("source_paths", []):
                if isinstance(p, str): return p if p.startswith("skill_benchmark/") else "skill_benchmark/" + p
            pr=origin.get("provenance_record", {})
            for p in pr.get("source_paths", []) if isinstance(pr,dict) else []:
                if isinstance(p, str): return p if p.startswith("skill_benchmark/") else "skill_benchmark/" + p
    return None

def main():
    if OUT.exists(): raise SystemExit(f"refusing overwrite: {OUT}")
    AD.mkdir(parents=True, exist_ok=True); ADP.mkdir(parents=True, exist_ok=True)
    union=rows(UNION); terminal=rows(TERM); current={x["canonical_source_sha256"] for x in terminal}
    # Current parent and NC prompt populations are explicit current-state inputs.
    parent=rows(PARENT)
    oldp=rows(OLD/"nc_prompt_manifest.jsonl")
    triads={}
    for x in terminal: triads.setdefault((x["batch"],x["family_token"]),set()).add(x["canonical_source_sha256"])
    nc=[]
    for x in oldp:
        key=(x.get("discovery_batch"),x.get("family_token"))
        target=x.get("intended_target_source_sha256")
        if key in triads and target in triads[key]:
            y=dict(x); y.pop("audit_cluster_id",None); y.pop("audit_prompt_id",None); y.update({"cluster_id": f"NC-{key[0]}-{key[1]}", "candidate_source_sha256": sorted(triads[key]), "prompt_id": x.get("audit_prompt_id"), "prompt_text_sha256": x.get("prompt_text_sha256",x.get("prompt_sha256"))})
            nc.append(y)
    # Replace the three changed families with the current composite bindings.
    comp=rows(COMP)
    nc=[x for x in nc if (x.get("discovery_batch"),x.get("family_token")) not in {("B013","F-59796e6dce627ba4"),("B015","F-1f956c52aa7f0c9d"),("B015","F-98199f9119042f1a")}]
    for x in comp:
        nc.append({"cluster_id":f"NC-{x['batch']}-{x['family_token']}","candidate_source_sha256":sorted(triads[(x['batch'],x['family_token'])]),"prompt":x["author_prompt"],"prompt_id":x["canonical_prompt_id"],"prompt_text_sha256":x["author_prompt_sha256"],"cue_stratum":"CURRENT_COMPOSITE_CUE_SAFE","discovery_batch":x["batch"],"family_token":x["family_token"]})
    # Preserve only the three current prompts per current family, deduplicated.
    seen=set(); clean=[]
    for x in nc:
        if x["prompt_id"] not in seen: seen.add(x["prompt_id"]); clean.append(x)
    nc=clean
    if len(parent)!=381 or len(nc)!=147 or len({x["cluster_id"] for x in nc})!=49: raise SystemExit(f"current population drift: parent={len(parent)} nc={len(nc)} clusters={len({x['cluster_id'] for x in nc})}")
    clusters=[]
    for cid,g in __import__('itertools').groupby(sorted(nc,key=lambda x:x["cluster_id"]), key=lambda x:x["cluster_id"]):
        g=list(g); clusters.append({"cluster_id":cid,"candidate_source_sha256":g[0]["candidate_source_sha256"],"prompt_ids":[x["prompt_id"] for x in g]})
    summary={"status":"PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE","claim_boundary":"Current reconstructed inputs only; no experiment.","counts":{"candidate_sources":len(union),"parent_prompts":len(parent),"nc_prompts":len(nc),"nc_clusters":len(clusters)}}
    dump(AD/"candidate_source_union_for_phase4.jsonl",union); dump(AD/"parent_prompt_manifest_for_phase5.jsonl",parent); dump(AD/"nc_prompt_manifest_for_phase4.jsonl",nc); dump(AD/"nc_cluster_manifest_for_phase4.jsonl",clusters)
    (AD/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    # Reconstruct source-native profiles and path ledger for all current hashes.
    profiles=[]; paths=[]
    oldprof=rows(M/"rq2b_nc_phase4_navigation_profiles_2026-09-05/navigation_profiles.jsonl"); oldby={x["canonical_source_sha256"]:x for x in oldprof}
    oldpaths=rows(M/"rq2b_nc_phase4_navigation_profiles_2026-09-05/source_path_resolution_ledger.jsonl"); oldpathby={x["canonical_source_sha256"]:x.get("selected_workspace_relative_path") for x in oldpaths}
    comp_paths={i.get("canonical_source_sha256"):i.get("source_path") for x in comp for i in x.get("source_visible_candidate_set",[]) if isinstance(i,dict)}
    for u in union:
        h=u["canonical_source_sha256"]; p=oldby.get(h); sp=source_path(u) or comp_paths.get(h) or oldpathby.get(h)
        if p is None:
            if not sp: raise SystemExit(f"no declared source path: {h}")
            txt=(ROOT/sp).read_text(encoding="utf-8-sig"); title=txt.splitlines()[0].lstrip("# ").strip() or h[:12]
            p={"canonical_source_sha256":h,"profile_schema_version":"rq2b_nc_phase4_source_native_navigation_profile_v1","relevance_source_name":title,"relevance_source_description":txt[:3000],"relevance_heading_profile":txt[:6000],"source_name":title,"source_description":txt[:3000],"source_headings":[title],"scope_boundary":"OUTCOME_BLIND_NAVIGATION_ONLY_NOT_A_LABEL_RANKING_OR_METRIC","relevance_excluded_provider_product_tokens":["anthropic","chatgpt","claude","codex","gemini","openai"]}
        profiles.append(p); paths.append({"canonical_source_sha256":h,"declared_source_paths":[sp] if sp else [],"selected_workspace_relative_path":sp,"selected_source_byte_sha256":h,"path_resolution_tier":"CURRENT_MASTER_PROVENANCE_REPLAY"})
    dump(ADP/"navigation_profiles.jsonl",profiles); dump(ADP/"source_path_resolution_ledger.jsonl",paths)
    (ADP/"navigation_profile_summary.json").write_text(json.dumps({"status":"PASS_SOURCE_NATIVE_NAVIGATION_PROFILE_MATERIALISATION_OUTCOME_BLIND_ONLY","count":len(profiles)})+"\n")
    (ADP/"summary.json").write_text(json.dumps({"status":"PASS_SOURCE_NATIVE_NAVIGATION_PROFILE_MATERIALISATION_OUTCOME_BLIND_ONLY","count":len(profiles)})+"\n")
    (AD/"summary.json").write_text(json.dumps({"status":"PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE","claim_boundary":"Current reconstructed inputs only; no experiment.","counts":{"candidate_sources":len(union),"parent_prompts":len(parent),"nc_prompts":len(nc),"nc_clusters":len(clusters)}})+"\n")
    spec=importlib.util.spec_from_file_location("opt",ROOT/"skill_benchmark/scripts/materialize_rq2b_nc_phase4_option1_k6_audit_input_2026_09_05.py"); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.PHASE3=AD; mod.PROFILES=ADP; mod.OUT=OUT
    mod.PARENT_IDENTITIES=ROOT/"skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
    import sys; sys.argv=[sys.argv[0],"--output-dir",str(OUT)]; rc=mod.main()
    if rc==0:
        q=json.loads((OUT/"summary.json").read_text()); q["current_master_state"]={"source_union_sha256":sha(AD/"candidate_source_union_for_phase4.jsonl"),"parent_prompt_sha256":sha(AD/"parent_prompt_manifest_for_phase5.jsonl"),"nc_prompt_sha256":sha(AD/"nc_prompt_manifest_for_phase4.jsonl"),"nc_prompt_count":147,"nc_family_count":49,"k":6}; (OUT/"summary.json").write_text(json.dumps(q,indent=2,sort_keys=True)+"\n")
    return rc
if __name__=="__main__": raise SystemExit(main())
