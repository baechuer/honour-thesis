#!/usr/bin/env python3
"""Materialise B044 discovery-only exact-native-description packets."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from materialize_rq2b_source_native_b043_education_health_lifestyle import (
    BOOTSTRAP_SUMMARY, CORPUS, CORPUS_SUMMARY, HYPOTHESES, NC, PROTOCOL,
    REVIEW, WORKSPACE, b001_b038_keys, b039_hashes, b040_hashes, digest,
    family_path_count, read_jsonl, relative, write_jsonl,
)

OUTPUT = REVIEW / "source_native_data_ml_ai_evaluation_data_engineering_databases_security_privacy_observability_b044_2026-09-04"
B041 = REVIEW / "source_native_creative_design_media_lexical_continuation_b041_2026-09-04/batch_041_full_original_source_packets.jsonl"
B042 = REVIEW / "source_native_business_governance_lexical_continuation_b042_2026-09-04/batch_042_full_original_source_packets.jsonl"
B043 = REVIEW / "source_native_education_training_coaching_health_wellbeing_consumer_lifestyle_b043_2026-09-04/b043_source_native_three_skill_full_original_packets.jsonl"

# Applied only to frozen literal native descriptions.  A selected family must
# share one category; no full source body or source metadata influences this.
ALLOWED = {
    "data_science": (r"\bdata science\b", r"\bdata analys(?:is|tics)\b", r"\bstatistical analys", r"\bexploratory data", r"\bdata visualization\b"),
    "machine_learning_ai": (r"\bmachine learning\b", r"\bdeep learning\b", r"\bneural network", r"\blarge language model", r"\bllm(?:s)?\b", r"\bmodel inference\b", r"\bmodel training\b"),
    "ai_evaluation": (r"\bai eval(?:uation|s)?\b", r"\bmodel eval(?:uation|s)?\b", r"\bmodel benchmark", r"\bbenchmark(?:ing)? models?\b", r"\bevaluat(?:e|ing) (?:an )?(?:ai |ml |machine learning |language )?model"),
    "data_engineering": (r"\bdata pipeline", r"\betl\b", r"\belt\b", r"\bdata ingestion\b", r"\bdata transformation\b", r"\bdata warehouse\b", r"\bdata lake\b", r"\bdata orchestrat"),
    "databases": (r"\bdatabase(?:s)?\b", r"\bsql\b", r"\bpostgres(?:ql)?\b", r"\bmysql\b", r"\bmongodb\b", r"\bquery optimization\b"),
    "security": (r"\bsecurity\b", r"\bvulnerabilit", r"\bthreat model", r"\bpenetration test", r"\bencrypt(?:ion|ed)?\b", r"\bauthenti[ck]ation\b", r"\bauthori[sz]ation\b", r"\bmalware\b"),
    "privacy": (r"\bprivacy\b", r"\bpii\b", r"\bpersonally identifiable", r"\bdata anonymi[sz]", r"\bdata redaction\b", r"\bdata minimization\b"),
    "observability": (r"\bobservability\b", r"\bmonitoring\b", r"\bdistributed tracing\b", r"\btelemetry\b", r"\blog(?:s|ging)\b", r"\bmetrics\b", r"\balert(?:ing|s)?\b"),
}
COMPILED_ALLOWED = {key: tuple(re.compile(x, re.I) for x in values) for key, values in ALLOWED.items()}

# Scope exclusions likewise inspect descriptions only.  ``training`` is not
# banned because it can describe ML model training; education-specific terms are.
PROHIBITED = tuple(re.compile(x, re.I) for x in (
    # Creative/design/media.
    r"\bcreative\b", r"\bdesign(?:ing|er)?\b", r"\bgraphic(?:s)?\b", r"\billustrat", r"\btypography\b", r"\blayout\b", r"\bvisual\b", r"\bmedia\b", r"\bvideo\b", r"\baudio\b", r"\bpodcast\b", r"\bphotograph", r"\bpresentation\b", r"\bslides?\b", r"\bpowerpoint\b", r"\bkeynote\b", r"\bimage(?:s)?\b", r"\binfographic\b", r"\bposter\b", r"\bflyer\b", r"\bux\b", r"\buser experience\b", r"\buser interface\b", r"\bui design\b", r"\bwireframe\b", r"\bprototype\b", r"\bbranding?\b", r"\bmarketing\b", r"\bcopywrit", r"\bseo\b", r"\bsocial media\b",
    # Legal/HR/finance/governance.
    r"\blegal\b", r"\blaw\b", r"\bcourt\b", r"\bcontract\b", r"\bcompliance\b", r"\bregulat", r"\bgovernance\b", r"\baudit\b", r"\brisk management\b", r"\bhuman resources\b", r"\brecruit", r"\bemployee\b", r"\bpayroll\b", r"\bfinance\b", r"\bfinancial\b", r"\baccounting\b", r"\bbudget\b", r"\binvoice\b", r"\btax\b", r"\binvest(?:ment|ing)\b",
    # Education/health/lifestyle (do not exclude ML model training).
    r"\beducation\b", r"\bteach(?:ing|er)?\b", r"\bstudent(?:s)?\b", r"\bcurriculum\b", r"\blesson(?:s)?\b", r"\bclassroom\b", r"\bpedagog", r"\bhomework\b", r"\bexam(?:s|ination)?\b", r"\bstudy(?:ing)?\b", r"\btutor(?:ing)?\b", r"\bcoach(?:ing|es)?\b", r"\bmentor(?:ing)?\b", r"\bhealth(?:care)?\b", r"\bpatient(?:s)?\b", r"\bclinical\b", r"\bmedical\b", r"\bmedicine\b", r"\btherapy\b", r"\bwell[- ]?being\b", r"\bwellness\b", r"\bmental health\b", r"\bfitness\b", r"\bworkout\b", r"\bexercise\b", r"\bnutrition\b", r"\bdiet\b", r"\bsleep\b", r"\bmindfulness\b", r"\bmeditation\b", r"\blifestyle\b", r"\bhousehold\b", r"\bgardening\b", r"\bcooking\b", r"\brecipes?\b",
    # General DevOps/source-control/CI/CD, retained only as exclusions.
    r"\bdevops\b", r"\bci/cd\b", r"\bcontinuous integration\b", r"\bcontinuous delivery\b", r"\bkubernetes\b", r"\bdocker\b", r"\bterraform\b", r"\binfrastructure as code\b", r"\bsource control\b", r"\bversion control\b", r"\bgit(?:hub|lab)?\b", r"\bcommit(?:s|ting)?\b", r"\bpull request\b", r"\bcode review\b", r"\bdeployment\b", r"\bbuild pipeline\b",
))

def categories(text: str) -> list[str]:
    return [name for name, patterns in COMPILED_ALLOWED.items() if any(p.search(text) for p in patterns)]

def packet_hashes(path: Path) -> set[str]:
    rows = read_jsonl(path)
    values = {str(member["canonical_source_sha256"]) for row in rows for member in row["members"]}
    if len(rows) != 25 or len(values) != 75:
        raise SystemExit(f"unexpected inspected-packet cardinality: {path}")
    return values

def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing B044 root: {OUTPUT}")
    for path in (PROTOCOL, CORPUS, CORPUS_SUMMARY, HYPOTHESES, BOOTSTRAP_SUMMARY, B041, B042, B043):
        if not path.is_file(): raise SystemExit(f"missing frozen input: {path}")
    keys = b001_b038_keys()
    b001_b038 = set().union(*({str(row["canonical_source_sha256"]) for row in read_jsonl(path)} for path in keys.values()))
    if len(b001_b038) != 2850: raise SystemExit("B001-B038 exclusion cardinality mismatch")
    prior_parts = {"B001_B038": b001_b038, "B039": b039_hashes(), "B040": b040_hashes(), "B041": packet_hashes(B041), "B042": packet_hashes(B042), "B043": packet_hashes(B043)}
    excluded = set().union(*prior_parts.values())
    corpus_rows = read_jsonl(CORPUS); corpus = {str(row["canonical_source_sha256"]): row for row in corpus_rows}
    hypotheses = read_jsonl(HYPOTHESES)
    if len(corpus) != 23450 or len(hypotheses) != 49823: raise SystemExit("frozen corpus/hypothesis cardinality mismatch")
    hypotheses.sort(key=lambda row: (-int(row["reciprocal_link_count"]), -float(row["rank_fusion_score"]), -family_path_count(row), row["member_source_sha256"]))
    selected: list[dict[str, Any]] = []; used: set[str] = set(); exclusions: Counter[str] = Counter()
    for hypothesis in hypotheses:
        hashes = [str(v) for v in hypothesis["member_source_sha256"]]
        if any(v not in corpus for v in hashes): raise SystemExit(f"corpus binding missing: {hypothesis['family_id']}")
        members = set(hashes)
        if members & excluded: exclusions["prior_B001_B043_inspected_source_overlap"] += 1; continue
        if members & used: exclusions["within_B044_source_collision"] += 1; continue
        descriptions = [str(corpus[v]["native_description"]) for v in hashes]
        if any(p.search(d) for d in descriptions for p in PROHIBITED): exclusions["prohibited_scope_indicator"] += 1; continue
        shared = sorted(set.intersection(*(set(categories(d)) for d in descriptions)))
        if not shared: exclusions["no_shared_allowed_task_family"] += 1; continue
        selected.append({**hypothesis, "batch_id": "SN-LEX-B044", "batch_rank": len(selected)+1, "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION", "selection_scope": "DATA_ML_AI_EVALUATION_DATA_ENGINEERING_DATABASES_SECURITY_PRIVACY_OBSERVABILITY_FAMILIES_ONLY", "source_native_category_intersection": shared, "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE", "claim_boundary": "Source-native reciprocal-neighbour selection only; no semantic-family decision or downstream result."})
        used.update(members)
        if len(selected) == 25: break
    if len(selected) != 25 or len(used) != 75 or used & excluded: raise SystemExit("B044 selection failure")
    OUTPUT.mkdir(parents=True)
    ledger = OUTPUT / "source_native_reciprocal_family_ledger.jsonl"; write_jsonl(ledger, selected)
    packets: list[dict[str, Any]] = []; replays: list[dict[str, Any]] = []
    for family in selected:
        members = []
        for source_hash, description_hash, source_paths in zip(family["member_source_sha256"], family["member_native_description_sha256"], family["member_source_paths"]):
            record = corpus[source_hash]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != source_paths: raise SystemExit(f"description/path binding mismatch: {source_hash}")
            originals = []; replay_hashes = []
            for source_path in source_paths:
                raw = (WORKSPACE / source_path).read_bytes(); found = hashlib.sha256(raw).hexdigest()
                if found != source_hash: raise SystemExit(f"source-byte replay failed: {source_path}")
                replay_hashes.append(found); originals.append({"source_path": source_path, "canonical_source_sha256": source_hash, "preserved_original_skill_utf8": raw.decode("utf-8")})
            members.append({"canonical_source_sha256": source_hash, "native_description": record["native_description"], "native_description_sha256": description_hash, "native_description_origin": record["native_description_origin"], "native_description_literal_replay_status": record["native_description_replay_status"], "source_byte_replay": record["source_byte_replay"], "source_native_allowed_categories": categories(record["native_description"]), "preserved_complete_original_sources": originals})
            replays.append({"record_type": "original_source_byte_replay", "canonical_source_sha256": source_hash, "source_paths": source_paths, "replayed_path_sha256": replay_hashes, "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256", "native_description_sha256": description_hash, "native_description_literal_replay_status": record["native_description_replay_status"], "claim_boundary": "Byte and native-description replay only; no eligibility or downstream decision."})
        packets.append({"record_type": "source_native_three_skill_full_original_packet", "batch_id": "SN-LEX-B044", "batch_rank": family["batch_rank"], "family_id": family["family_id"], "selection_scope": family["selection_scope"], "source_native_category_intersection": family["source_native_category_intersection"], "reciprocal_neighbour_provenance": {"reciprocal_link_count": family["reciprocal_link_count"], "mutual_directional_ranks": family["mutual_directional_ranks"], "rank_fusion_score": family["rank_fusion_score"], "hypothesis_source_hashes": family["member_source_sha256"]}, "members": members, "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE", "claim_boundary": "Packet only; no semantic-family, eligibility, prompt, adequacy, admission, selector, retrieval-result, or metric result."})
    if len(replays) != 75 or len({r["canonical_source_sha256"] for r in replays}) != 75: raise SystemExit("B044 replay cardinality failure")
    packet_path = OUTPUT / "b044_source_native_three_skill_full_original_packets.jsonl"; replay_path = OUTPUT / "source_byte_replay_ledger.jsonl"
    write_jsonl(packet_path, packets); write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))
    summary = {"status": "PASS_B044_DISCOVERY_ONLY_SOURCE_NATIVE_ALLOWED_FAMILY_PACKETS", "claim_boundary": "Discovery packets only. These 25 three-skill hypotheses are not semantic-family findings, RQ2 cases, final-library entries, acceptable alternatives, retrieval results, or metrics.", "bound_inputs": {"protocol": digest(PROTOCOL), "source_native_description_corpus": digest(CORPUS), "source_native_description_corpus_summary": digest(CORPUS_SUMMARY), "frozen_lexical_mutual_triangle_hypotheses": digest(HYPOTHESES), "frozen_lexical_bootstrap_summary": digest(BOOTSTRAP_SUMMARY), "prior_B001_B038_internal_reconciliation_keys": {k: digest(v) for k,v in keys.items()}, "B041_full_original_source_packets": digest(B041), "B042_full_original_source_packets": digest(B042), "B043_full_original_source_packets": digest(B043)}, "method": {"route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION", "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, distinct-source-path count descending, then sorted member source hashes", "allowed_scope_filter": "all three literal source-native descriptions share at least one predeclared allowed category and none matches a prohibited-scope indicator", "permitted_categories": list(ALLOWED), "prohibited_scope_indicators": [p.pattern for p in PROHIBITED], "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "provenance status", "prior outcome", "prompt", "label", "cluster membership"], "fresh_source_policy": "exclude every B001-B043 inspected source hash, including source-only and unadmitted queues; require source-disjoint members within B044"}, "counts": {"frozen_corpus_sources": len(corpus), "frozen_hypotheses": len(hypotheses), "prior_inspected_source_hashes_B001_B038": len(b001_b038), "prior_inspected_source_hashes_B001_B043_union": len(excluded), "prior_inspected_source_hashes_by_batch": {k: len(v) for k,v in prior_parts.items()}, "b044_families": len(selected), "b044_source_hashes": len(used), "b044_original_source_replays": len(replays), "source_hash_overlap_B044_vs_B001_B043": len(used & excluded), "selection_exclusions_encountered_before_completion": dict(sorted(exclusions.items())), "family_shared_category_counts": dict(sorted(Counter(c for r in selected for c in r["source_native_category_intersection"]).items()))}, "outputs": {ledger.name: digest(ledger), packet_path.name: digest(packet_path), replay_path.name: digest(replay_path)}, "verification": {"source_disjointness_B044_vs_B001_B043": "PASS", "original_source_byte_replay": "PASS_75_OF_75", "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS", "full_original_skill_materials_bound_for_later_reading": "PASS_25_PACKETS_75_SOURCES"}, "limitations": ["A lexical reciprocal-neighbour priority is not semantic similarity ground truth or a retrieval metric.", "The description-only scope screen is a routing constraint, not a source-quality, semantic-family, eligibility, or downstream decision.", "The dense source-native route remains unexecuted; this continuation does not repair that limitation or establish dense-versus-lexical coverage."]}
    (OUTPUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({"output": relative(OUTPUT), "counts": summary["counts"], "output_hashes": summary["outputs"]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
