#!/usr/bin/env python3
"""Build append-only Phase-3 changed-scope QA packets (no semantic decisions).

Navigation is deliberately lexical (path/name tokens only).  Outputs are review
packets, never admissions, exclusions, retrieval outcomes, or acceptable-set
decisions.  The packet contains complete originals for nominated source pairs so
two independent reviewers can work target-blind.
"""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
M = ROOT / "rq2b_naturalistic_confusability/manifests"
PRE = M / "rq2b_nc_master_phase3_preflight_2026-09-06_v1"
OUT = M / "rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1"
ADDED = set(json.loads((PRE/"union_change_log.json").read_text())["added_master_phase1_hashes"])

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def loadl(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def toks(s): return set(re.findall(r"[a-z0-9]{3,}", s.lower()))
def dump(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True)+"\n" for x in rows))

def resolve_source(rel):
    """Resolve workspace-relative manifest paths without permitting escapes."""
    if not isinstance(rel, str) or not rel: return None
    p = (WORKSPACE / rel).resolve()
    try: p.relative_to(WORKSPACE.resolve())
    except ValueError: return None
    return p if p.is_file() else None

def main():
    candidate = loadl(PRE/"candidate_source_union.jsonl")
    fresh = [x for x in candidate if x["canonical_source_sha256"] in ADDED]
    # Resolve source paths from the provenance-bearing current union.  Missing
    # paths are retained as an explicit blocker rather than silently omitted.
    records=[]
    for x in fresh:
        o=x["local_nc_origin_records"][0]; paths=[z for z in o.get("source_paths",[]) if isinstance(z,str)]
        path=resolve_source(paths[0]) if paths else None
        text=path.read_text(errors="replace") if path and path.is_file() else ""
        records.append({"sha":x["canonical_source_sha256"],"family":o["family_token"],"member":o["member_token"],"batch":o["discovery_batch"],"path":paths[0] if paths else None,"text":text})
    # Lexical nomination is only a queueing signal.  Use path/name overlap and
    # cap the packet to five candidates per new source for reproducible review.
    allrec=[]
    for x in candidate:
        o=(x.get("local_nc_origin_records") or [None])[0]
        if not o: continue
        paths=[z for z in o.get("source_paths",[]) if isinstance(z,str)]; p=resolve_source(paths[0]) if paths else None
        allrec.append({"sha":x["canonical_source_sha256"],"family":o.get("family_token"),"member":o.get("member_token"),"path":paths[0] if paths else None,"text":p.read_text(errors="replace") if p and p.is_file() else ""})
        h=x.get("historical_base_candidate") or {}
        for v in h.get("v3_identity_records",[]):
            vp=resolve_source(v.get("source_path"))
            if vp and vp.is_file(): allrec.append({"sha":x["canonical_source_sha256"],"family":None,"member":None,"path":v.get("source_path"),"text":vp.read_text(errors="replace")})
    def skill_source(name):
        q=toks(name)
        for c in allrec:
            if c["text"] and q & toks(Path(c["path"] or "").stem): return c["text"]
        return ""
    screen=[]; packets=[]
    for i,r in enumerate(records,1):
        rt=toks(Path(r["path"] or "").stem)
        scored=[]
        for c in allrec:
            if c["sha"]==r["sha"]: continue
            score=len(rt & toks(Path(c["path"] or "").stem))
            if score: scored.append((score,c))
        scored=sorted(scored,key=lambda z:(-z[0],z[1]["sha"]))[:5]
        for j,(score,c) in enumerate(scored,1):
            sid=f"CS-SRCREL-{i:03d}-{j:02d}"
            screen.append({"screen_id":sid,"new_source_sha256":r["sha"],"new_family_token":r["family"],"candidate_source_sha256":c["sha"],"candidate_family_token":c["family"],"lexical_signal":{"path_stem_token_overlap":score},"mechanical_disposition":"REVIEW_REQUIRED_NOT_A_SEMANTIC_DUPLICATE_DECISION","navigation_boundary":"Lexical path/name nomination only; no embedding, retrieval, provider or semantic decision."})
            packets.append({"packet_id":sid,"candidate_a":{"opaque_token":"A","source_original":r["text"]},"candidate_b":{"opaque_token":"B","source_original":c["text"]},"return_schema":{"relation_decision":"DUPLICATE_CLUSTER | RELATED_BUT_DISTINCT | BLOCKED_OR_UNCLEAR","rationale":"","source_anchors":[],"triad_independence_preserved":None},"review_boundary":"Compare source meaning and independence only. Do not infer targets, labels, ranks, retrieval outcomes, acceptable sets, or final-library admission."})
    # Prompt scope is explicitly limited to the nine changed prompts.  Build a
    # lexical-only comparison queue against the historical 381-prompt corpus.
    prompts=[]; prompt_screen=[]; cue_screen=[]; cue_packets=[]
    corpus=[]; seen_corpus=set()
    for p in M.glob("**/parent_prompt_manifest.jsonl"):
        for row in loadl(p):
            key=(row.get("prompt_id"),row.get("prompt_sha256"))
            if isinstance(row.get("prompt"),str) and key not in seen_corpus:
                seen_corpus.add(key); corpus.append(row)
    hist_map={}
    for row in corpus:
        name=row.get("gold_skill","")
        hits=list((ROOT/"skills").glob(f"**/{name}/SKILL.md")) if name else []
        if len(hits)==1 and hits[0].is_file() and hits[0].read_text(errors="replace").strip():
            hist_map[name]={"text":hits[0].read_text(errors="replace"),"path":str(hits[0].relative_to(WORKSPACE)),"sha256":sha(hits[0])}
    for batch in ("b013","b015"):
        for p in (ROOT/f"rq2b_naturalistic_confusability/review/source_native_dense_lexical_union_{batch}_2026-09-04").glob("**/reconciliation/prompt_authoring/author_return.jsonl"):
            for n,row in enumerate(loadl(p),1):
                if row.get("family_token") in {r["family"] for r in records}:
                    prompts.append({"packet_id":f"CS-PR-{row['family_token']}-{n:02d}","family_token":row["family_token"],"member_sha256":row.get("target_source_sha256"),"prompt_text":row.get("prompt",""),"source_original":next((r["text"] for r in records if r["sha"]==row.get("target_source_sha256")),"")})
    for i,a in enumerate(prompts,1):
        scored=[]
        for b in corpus:
            bt=b.get("prompt",""); score=len(toks(a["prompt_text"]) & toks(bt))
            if score: scored.append((score,b))
        pool=sorted([(len(toks(a["prompt_text"]) & toks(b.get("prompt",""))),b) for b in corpus],key=lambda z:(-z[0],z[1].get("prompt_id",z[1].get("family_token",""))))
        for j,(score,b) in enumerate(pool[:5],1):
            pid=f"CS-PRREL-{i:03d}-{j:02d}"
            prompt_text=b.get("prompt",""); hm=hist_map.get(b.get("gold_skill",""),{}); bsource=b.get("complete_original_skill","") or hm.get("text","")
            if not a["source_original"].strip() or not bsource.strip():
                prompt_screen.append({"screen_id":pid,"prompt_a_id":a["packet_id"],"prompt_b_id":b.get("prompt_id","UNKNOWN"),"lexical_signal":{"content_token_overlap":score},"mechanical_disposition":"BLOCKED_MISSING_HISTORICAL_SOURCE_PROVENANCE"})
                continue
            prompt_screen.append({"screen_id":pid,"prompt_a_id":a["packet_id"],"prompt_b_id":b.get("prompt_id",b.get("family_token","UNKNOWN")),"lexical_signal":{"content_token_overlap":score},"mechanical_disposition":"REVIEW_REQUIRED_NOT_A_SEMANTIC_DUPLICATE_DECISION"})
            prompt_packets=[{"side":"A","opaque_token":"A1","prompt":a["prompt_text"],"complete_original_skill":a["source_original"]},{"side":"B","opaque_token":"B1","prompt":prompt_text,"complete_original_skill":bsource}]
            # The corpus may not expose originals; retain the packet but fail
            # closed at validation rather than silently treating it as visible.
            prompts[-1].setdefault("_pairs",[]).append({"packet_id":pid,"associated_source_sets":prompt_packets,"historical_source_provenance":{"relative_path":hm.get("path"),"sha256":hm.get("sha256")},"return_schema":{"relation_decision":"RELATED_BUT_DISTINCT | SPLIT_LEAKAGE | TRANSFORMED_DUPLICATE | UNCLEAR","rationale":"","source_anchors":[]},"review_boundary":"Compare prompt relation and source-supported distinction only. Do not infer targets, labels, ranks, retrieval outcomes, or acceptable sets."})
    for a in prompts:
        text=a["prompt_text"].lower(); path=next((r["path"] for r in records if r["sha"]==a["member_sha256"]),"")
        signals=[]
        for term in set(re.findall(r"[a-z0-9][a-z0-9._/-]{2,}",path.lower())):
            if term in text: signals.append({"matched_text":term,"signal":"TARGET_SOURCE_PATH_OR_TITLE_LITERAL"})
        if signals:
            for s in signals:
                cid=f"CS-CUE-{len(cue_screen)+1:03d}"; cue_screen.append({"packet_id":cid,"prompt_id":a["packet_id"],"mechanical_finding":{**s,"mechanical_disposition":"REVIEW_REQUIRED"}}); cue_packets.append({"packet_id":cid,"prompt":a["prompt_text"],"mechanical_finding":{**s,"mechanical_disposition":"REVIEW_REQUIRED"},"return_schema":{"cue_decision":"AVOIDABLE_IDENTITY_CUE | DECLARED_NECESSARY_CUE_STRATUM | NOT_A_CUE | UNCLEAR","packet_id":cid,"rationale":"","source_anchors":[]},"review_boundary":"Decide only whether the finding is an avoidable identity cue or source-anchored necessary task condition. Do not decide target adequacy, labels, rank, or retrieval."})
        else: cue_screen.append({"packet_id":f"CS-CUE-NONE-{a['packet_id']}","prompt_id":a["packet_id"],"mechanical_disposition":"PASS_NO_MECHANICAL_CUE_SIGNAL"})
    relation_packets=[q for a in prompts for q in a.get("_pairs",[])]
    if any(not x["text"].strip() for x in records) or any(not p["candidate_a"]["source_original"].strip() or not p["candidate_b"]["source_original"].strip() for p in packets):
        raise RuntimeError("FAIL_CLOSED: missing or empty source original in changed-scope packet")
    for p in packets:
        p["candidate_a"].update({"sha256":hashlib.sha256(p["candidate_a"]["source_original"].encode()).hexdigest(),"length":len(p["candidate_a"]["source_original"])})
        p["candidate_b"].update({"sha256":hashlib.sha256(p["candidate_b"]["source_original"].encode()).hexdigest(),"length":len(p["candidate_b"]["source_original"])})
    dump(OUT/"source_relation_screen.jsonl",screen); dump(OUT/"source_relation_reviewer_packet.jsonl",packets)
    dump(OUT/"prompt_relation_screen.jsonl",prompt_screen); dump(OUT/"prompt_relation_reviewer_packet.jsonl",relation_packets)
    dump(OUT/"prompt_cue_screen.jsonl",cue_screen); dump(OUT/"prompt_cue_reviewer_packet.jsonl",cue_packets)
    manifest={"status":"PASS_PACKET_CONSTRUCTION_ONLY_NO_SEMANTIC_APPROVAL","scope":"Only 9 newly added B013/B015 sources; B052 removals cannot create admissions.","repair_provenance":{"repair":"Invalidated incomplete lone-prompt v1 packet and regenerated historical-schema relation/cue packets before any reviews.","resolver":"safe workspace-contained resolver; missing/empty originals fail closed","content_binding":"Opaque source text is bound by SHA-256 and length; identity fields withheld."},"counts":{"candidate_union":len(candidate),"fresh_sources":len(records),"source_relation_screen":len(screen),"source_relation_packets":len(packets),"changed_prompt_records":len(prompts),"prompt_relation_screen":len(prompt_screen),"prompt_relation_packets":len(relation_packets),"prompt_cue_screen":len(cue_screen),"prompt_cue_packets":len(cue_packets),"historical_prompt_corpus":len(corpus)},"inputs":{"preflight_sha256":sha(PRE/"summary.json"),"union_change_log_sha256":sha(PRE/"union_change_log.json")},"review_requirements":["two independent target-blind source reviewers plus coordinator for disagreements","two independent prompt relation and cue reviewers plus coordinator","semantic/cue decisions remain BLOCKED until returns are reconciled"],"assumptions":["lexical nomination is navigation only","empty lexical nomination is not evidence of independence","full original skill text is provided without targets/selectors/results"]}
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
