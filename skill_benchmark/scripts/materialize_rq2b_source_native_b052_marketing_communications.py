#!/usr/bin/env python3
"""Materialise discovery-only B052 source-native marketing/communications triads."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from materialize_rq2b_source_native_b051_legal_regulatory_audit_tax_insurance_civic import (
    B039_LEDGER, B040_PACKETS, B041_PACKETS, B042_PACKETS, B043_PACKETS,
    B044_PACKETS, B045_PACKETS, B046_PACKETS, B047_PACKETS, B048_PACKETS,
    B049_LEDGER, B050_QUEUE, BOOTSTRAP_SUMMARY, CORPUS, CORPUS_SUMMARY,
    HYPOTHESES, PROTOCOL, REVIEW, WORKSPACE, b001_b038_keys, b039_hashes,
    digest, family_path_count, member_hashes, packet_hashes, read_jsonl,
    relative, write_jsonl,
)

OUTPUT = REVIEW / "source_native_marketing_advertising_seo_social_community_web_analytics_journalism_publishing_localisation_communications_b052_2026-09-05"
B051_QUEUE = REVIEW / "source_native_legal_regulatory_compliance_audit_tax_accounting_insurance_risk_civic_government_b051_2026-09-05/b051_source_native_semantic_family_queue.jsonl"

# A shared bounded workflow category and two or more route cues are required.
# Both use literal frozen native descriptions only, so they prioritise later
# reading without making a full-source semantic-family finding.
ALLOWED = {
    "marketing_strategy": (r"\bmarketing\b", r"\bmarket research\b", r"\bbrand strategy\b", r"\bpositioning\b"),
    "advertising_campaigns": (r"\badvertis(?:e|ing|ement)\b", r"\bad campaign\b", r"\bpaid media\b", r"\bmedia buying\b", r"\bpay-per-click\b", r"\bppc\b"),
    "search_optimisation": (r"\bseo\b", r"\bsearch engine optimization\b", r"\bsearch rankings?\b", r"\bkeyword research\b", r"\bserp\b", r"\borganic traffic\b"),
    "social_community_management": (r"\bsocial media\b", r"\bcommunity management\b", r"\bcommunity engagement\b", r"\bonline community\b", r"\binfluencer marketing\b"),
    "web_analytics": (r"\bweb analytics\b", r"\bgoogle analytics\b", r"\bga4\b", r"\bconversion tracking\b", r"\bweb traffic\b", r"\bsite analytics\b"),
    "journalism_reporting": (r"\bjournalis[mt]\b", r"\bnewsroom\b", r"\breporting\b", r"\breporter\b"),
    "publishing_editorial": (r"\bpublisher\b", r"\bpublishing\b", r"\bpublication\b", r"\beditorial\b", r"\bmanuscript\b"),
    "localisation_language": (r"\blocali[sz]ation\b", r"\binternationali[sz]ation\b", r"\btranslation\b"),
    "communications_pr": (r"\bpublic relations\b", r"\bpress release\b", r"\bcommunications?\b", r"\bstakeholder engagement\b", r"\bexternal communications?\b"),
}
ROUTE_CUES = {
    "marketing_strategy": (r"\bbrand\b", r"\bmarket research\b", r"\bproduct marketing\b", r"\bpartner\b", r"\bcontent marketing\b", r"\bemail marketing\b", r"\bdemand generation\b", r"\bcompetitive\b", r"\bgo-to-market\b"),
    "advertising_campaigns": (r"\bgoogle ads\b|\badwords\b", r"\bmeta\b|\bfacebook\b", r"\blinkedin\b", r"\btiktok\b", r"\bmedia buying\b", r"\bdisplay ads?\b", r"\bsearch ads?\b", r"\bcampaign optimiz"),
    "search_optimisation": (r"\bkeyword\b", r"\btechnical seo\b", r"\bon-page\b", r"\blink building\b", r"\bcontent (?:cluster|brief|roadmap)\b", r"\blocal seo\b", r"\bseo audit\b", r"\bserp\b"),
    "social_community_management": (r"\bposts?\b|\bcaption\b|\bthreads?\b", r"\bschedul", r"\bcommunity (?:management|engagement)\b", r"\bsocial listening\b", r"\binfluencer\b", r"\bhashtag\b"),
    "web_analytics": (r"\bgoogle analytics\b|\bga4\b", r"\bconversion tracking\b", r"\btag manager\b", r"\btraffic\b", r"\bfunnel\b", r"\bexperiment\b|\ba/?b test", r"\bgoogle ads\b"),
    "journalism_reporting": (r"\breporting\b|\breporter\b", r"\bfact[- ]check|\bverification\b", r"\binterview\b", r"\barticle\b|\bstory\b", r"\bdata journalism\b", r"\bbroadcast\b"),
    "publishing_editorial": (r"\bedit(?:ing|or)\b", r"\barticle\b|\bstory\b", r"\bpublication\b", r"\bmanuscript\b", r"\bpeer review\b"),
    "localisation_language": (r"\btranslation\b", r"\blocali[sz]ation\b", r"\binternationali[sz]ation\b", r"\blanguage\b", r"\brtl\b", r"\bplural\b"),
    "communications_pr": (r"\bpublic relations\b|\bpress release\b", r"\bstakeholder\b", r"\bexternal communications?\b", r"\bcommunications? (?:strategy|plan)\b", r"\bnewsletter\b", r"\binternal communications?\b"),
}
A = {key: tuple(re.compile(p, re.I) for p in value) for key, value in ALLOWED.items()}
R = {key: tuple(re.compile(p, re.I) for p in value) for key, value in ROUTE_CUES.items()}


def categories(text: str) -> list[str]:
    return [key for key, patterns in A.items() if any(p.search(text) for p in patterns)]


def route_cues(text: str, category: str) -> list[str]:
    return [p.pattern for p in R[category] if p.search(text)]


def lead(texts: list[str]) -> str:
    return " | ".join(" ".join(text.split())[:180] for text in texts)


def historical_parts() -> dict[str, set[str]]:
    keys = b001_b038_keys()
    b001_b038 = set().union(*({str(row["canonical_source_sha256"]) for row in read_jsonl(path)} for path in keys.values()))
    if len(b001_b038) != 2850:
        raise SystemExit("B001-B038 exclusion cardinality mismatch")
    return {
        "B001_B038": b001_b038, "B039": b039_hashes(),
        "B040": packet_hashes(B040_PACKETS, "SN-LEX-B040"), "B041": packet_hashes(B041_PACKETS, "SN-LEX-B041"),
        "B042": packet_hashes(B042_PACKETS, "SN-LEX-B042"), "B043": packet_hashes(B043_PACKETS, "SN-LEX-B043"),
        "B044": packet_hashes(B044_PACKETS, "SN-LEX-B044"), "B045": packet_hashes(B045_PACKETS, "SN-LEX-B045"),
        "B046": packet_hashes(B046_PACKETS, "SN-LEX-B046"), "B047": packet_hashes(B047_PACKETS, "SN-LEX-B047"),
        "B048": packet_hashes(B048_PACKETS, "SN-LEX-B048"),
        "B049": member_hashes(read_jsonl(B049_LEDGER), "B049"),
        "B050": member_hashes(read_jsonl(B050_QUEUE), "B050"),
        "B051": member_hashes(read_jsonl(B051_QUEUE), "B051"),
    }


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing B052 root: {OUTPUT}")
    inputs = (PROTOCOL, CORPUS, CORPUS_SUMMARY, HYPOTHESES, BOOTSTRAP_SUMMARY, B039_LEDGER, B040_PACKETS, B041_PACKETS, B042_PACKETS, B043_PACKETS, B044_PACKETS, B045_PACKETS, B046_PACKETS, B047_PACKETS, B048_PACKETS, B049_LEDGER, B050_QUEUE, B051_QUEUE)
    for path in inputs:
        if not path.is_file(): raise SystemExit(f"missing frozen/canonical input: {path}")
    parts = historical_parts()
    excluded = set().union(*parts.values())
    b049_b050_overlap = sorted(parts["B049"] & parts["B050"])
    b051_prior_overlap = parts["B051"] & (excluded - parts["B051"])
    if len(excluded) != 3822 or sum(len(x) for x in parts.values()) != 3825 or len(b049_b050_overlap) != 3 or b051_prior_overlap:
        raise SystemExit("B001-B051 actual-union/cardinality mismatch")
    corpus = {str(row["canonical_source_sha256"]): row for row in read_jsonl(CORPUS)}
    hypotheses = read_jsonl(HYPOTHESES)
    if len(corpus) != 23450 or len(hypotheses) != 49823: raise SystemExit("frozen corpus/hypothesis cardinality mismatch")
    hypotheses.sort(key=lambda row: (-int(row["reciprocal_link_count"]), -float(row["rank_fusion_score"]), -family_path_count(row), row["member_source_sha256"]))
    selected: list[dict[str, Any]] = []; used: set[str] = set(); rejected: Counter[str] = Counter()
    for hypothesis in hypotheses:
        hashes = [str(x) for x in hypothesis["member_source_sha256"]]
        if len(hashes) != 3 or len(set(hashes)) != 3: raise SystemExit(f"malformed non-triad: {hypothesis['family_id']}")
        if any(x not in corpus for x in hashes): raise SystemExit(f"corpus binding missing: {hypothesis['family_id']}")
        members = set(hashes)
        if members & excluded: rejected["REJECT_HISTORICAL_B001_B051_SOURCE_OVERLAP"] += 1; continue
        if members & used: rejected["REJECT_WITHIN_B052_SOURCE_COLLISION"] += 1; continue
        texts = [str(corpus[x]["native_description"]) for x in hashes]
        shared = sorted(set.intersection(*(set(categories(text)) for text in texts)))
        if not shared: rejected["REJECT_NO_SHARED_B052_NATURAL_WORKFLOW_ENVELOPE"] += 1; continue
        qualified, cue_map = [], {}
        for category in shared:
            per_member = [route_cues(text, category) for text in texts]
            distinct = sorted({cue for cues in per_member for cue in cues})
            if len(distinct) >= 2:
                qualified.append(category)
                cue_map[category] = {"member_route_cues": per_member, "distinct_route_cue_count": len(distinct)}
        if not qualified: rejected["REJECT_NO_NATIVE_FIRST_ROUTE_DIVERSITY_CUE"] += 1; continue
        selected.append({**hypothesis, "batch_id": "SN-SEM-B052", "batch_rank": len(selected) + 1, "discovery_route": "LEXICAL_RECIPROCAL_NATIVE_DESCRIPTION_WITH_WORKFLOW_AND_ROUTE_CUE_GATES", "selection_scope": "MARKETING_ADVERTISING_SEO_SOCIAL_COMMUNITY_WEB_ANALYTICS_JOURNALISM_PUBLISHING_LOCALISATION_COMMUNICATIONS_NATURAL_FIRST_ROUTE_HYPOTHESES_ONLY", "source_native_category_intersection": qualified, "source_native_route_cue_hypothesis": cue_map, "native_description_first_route_hypothesis": lead(texts), "review_state": "UNREVIEWED_FULL_SOURCE", "packet_state": "NOT_MATERIALISED_DISCOVERY_QUEUE_ONLY", "claim_boundary": "Description-only shared-workflow and route-cue hypothesis; no full-source semantic-family, independent-first-route, operational-contrast, provenance, or downstream decision."})
        used.update(members)
        if len(selected) == 25: break
    if len(selected) != 25 or len(used) != 75 or used & excluded: raise SystemExit(f"B052 selection failure: families={len(selected)}, sources={len(used)}, rejections={dict(rejected)}")
    OUTPUT.mkdir(parents=True)
    queue_path = OUTPUT / "b052_source_native_semantic_family_queue.jsonl"; write_jsonl(queue_path, selected)
    replays, defers = [], []
    for family in selected:
        hashes = list(family["member_source_sha256"])
        defers.append({"record_type": "discovery_defer", "batch_id": family["batch_id"], "batch_rank": family["batch_rank"], "family_id": family["family_id"], "member_source_sha256": hashes, "disposition": "DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED", "reason": "Native descriptions and route cues cannot establish bounded envelope, independent first routes, operational contrast, provenance/licence adequacy, or promptability; later independent full-source review is required."})
        for source_hash, description_hash, paths in zip(hashes, family["member_native_description_sha256"], family["member_source_paths"]):
            record = corpus[source_hash]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != paths: raise SystemExit(f"frozen description/path binding mismatch: {source_hash}")
            found = [hashlib.sha256((WORKSPACE / path).read_bytes()).hexdigest() for path in paths]
            if any(value != source_hash for value in found): raise SystemExit(f"source-byte replay failed: {source_hash}")
            replays.append({"record_type": "source_provenance_and_byte_replay", "canonical_source_sha256": source_hash, "source_paths": paths, "replayed_path_sha256": found, "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256", "native_description_sha256": description_hash, "native_description_origin": record["native_description_origin"], "native_description_literal_replay_status": record["native_description_replay_status"], "population_membership": record["population_membership"], "final_intake_role": record["final_intake_role"], "claim_boundary": "Frozen-record source/provenance pointer and byte replay only; no provenance/licence assessment or downstream decision."})
    if len(replays) != 75 or len({row["canonical_source_sha256"] for row in replays}) != 75: raise SystemExit("B052 byte-replay cardinality failure")
    replay_path = OUTPUT / "source_provenance_byte_replay_ledger.jsonl"; defer_path = OUTPUT / "discovery_rejection_and_defer_ledger.jsonl"
    write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"])); write_jsonl(defer_path, defers)
    keys = b001_b038_keys()
    exclusion = {"record_type": "B052_historical_source_exclusion_manifest", "claim_boundary": "Hash-membership exclusion only; it establishes no semantic or review outcome.", "batches": {key: {"unique_source_hashes": len(value)} for key, value in parts.items()}, "B001_B051_member_hashes_in_all_historical_ledgers": sum(len(value) for value in parts.values()), "B001_B051_unique_source_hashes": len(excluded), "historical_internal_queue_overlap": {"B049_B050_source_hashes": b049_b050_overlap, "B049_B050_overlap_count": len(b049_b050_overlap)}, "selection_unique_source_hashes": len(used), "intersection_B052_vs_B001_B051": len(used & excluded), "historical_ledger_inputs": {"B001_B038_internal_reconciliation_keys": {key: digest(path) for key, path in keys.items()}, "B039_source_native_discovery_ledger": digest(B039_LEDGER), "B040_full_original_source_packets": digest(B040_PACKETS), "B041_full_original_source_packets": digest(B041_PACKETS), "B042_full_original_source_packets": digest(B042_PACKETS), "B043_full_original_source_packets": digest(B043_PACKETS), "B044_full_original_source_packets": digest(B044_PACKETS), "B045_full_original_source_packets": digest(B045_PACKETS), "B046_full_original_source_packets": digest(B046_PACKETS), "B047_full_original_source_packets": digest(B047_PACKETS), "B048_full_original_source_packets": digest(B048_PACKETS), "B049_source_native_reciprocal_family_ledger": digest(B049_LEDGER), "B050_source_native_semantic_family_queue": digest(B050_QUEUE), "B051_source_native_semantic_family_queue": digest(B051_QUEUE)}}
    exclusion_path = OUTPUT / "historical_source_exclusion_manifest.json"; exclusion_path.write_text(json.dumps(exclusion, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {"batch_id": "SN-SEM-B052", "status": "PASS_B052_DISCOVERY_QUEUE_ONLY_UNREVIEWED", "claim_boundary": "Discovery queue only; not source review, provenance/licence outcome, prompt, target assessment, admission, acceptable-set audit, selector result, or metric.", "bound_inputs": {"protocol": digest(PROTOCOL), "source_native_description_corpus": digest(CORPUS), "source_native_description_corpus_summary": digest(CORPUS_SUMMARY), "frozen_lexical_mutual_triangle_hypotheses": digest(HYPOTHESES), "frozen_lexical_bootstrap_summary": digest(BOOTSTRAP_SUMMARY), "historical_source_exclusion_manifest": digest(exclusion_path)}, "method": {"route": "LEXICAL_RECIPROCAL_NATIVE_DESCRIPTION_WITH_WORKFLOW_AND_ROUTE_CUE_GATES", "semantic_intent_boundary": "Selection requires a shared predeclared user-workflow envelope plus at least two route cues from literal native descriptions. This is a natural first-route hypothesis, not a semantic-family decision.", "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, distinct-source-path count descending, then sorted member hashes; first non-overlapping 25 after fixed gates", "permitted_categories": list(ALLOWED), "route_cues": ROUTE_CUES, "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "prior outcome", "prompt", "label", "cluster membership"], "fresh_source_policy": "exclude every B001-B051 queued, reviewed, unadmitted, and discovery-ledger source hash via actual union; require source-disjoint members within B052"}, "counts": {"frozen_corpus_sources": len(corpus), "frozen_reciprocal_hypotheses": len(hypotheses), "historical_exclusion_B001_B051_unique_source_hashes": len(excluded), "historical_member_hashes_in_all_B001_B051_ledgers": sum(len(value) for value in parts.values()), "b052_families": len(selected), "b052_member_occurrences": 75, "b052_unique_source_hashes": len(used), "source_hash_overlap_B052_vs_B001_B051": len(used & excluded), "within_B052_source_hash_collisions": 75 - len(used), "source_byte_replays": len(replays), "selection_rejection_counts_before_completion": dict(sorted(rejected.items())), "family_shared_category_counts": dict(sorted(Counter(category for row in selected for category in row["source_native_category_intersection"]).items())), "deferred_families": len(defers)}, "queue": queue_path.name, "full_source_review_packet_materializer_compatibility": {"status": "PASS_QUEUE_HAS_REQUIRED_TRIAD_BINDING_FIELDS", "required_fields_present": ["family_id", "batch_rank", "member_source_sha256", "discovery_route"], "each_member_source_sha256_length": 3, "packet_materialisation_status": "NOT_RUN_BY_B052_DISCOVERY_ONLY_SCOPE"}, "outputs": {queue_path.name: digest(queue_path), replay_path.name: digest(replay_path), defer_path.name: digest(defer_path), exclusion_path.name: digest(exclusion_path)}, "verification": {"source_disjointness_B052_vs_B001_B051": "PASS", "original_source_byte_replay": "PASS_75_OF_75", "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS", "all_selected_families_deferred_pending_independent_full_source_review": "PASS_25_OF_25"}, "limitations": ["The reciprocal description index, shared workflow category, and route cues prioritise future reading only; they are not semantic truth, a review outcome, or a retrieval metric.", "No complete original source was read for substantive review; byte replay is preservation only.", "All selected families remain deferred pending independent full-source review."]}
    summary_path = OUTPUT / "summary.json"; summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    dossier = "\n".join(["# B052 source-native marketing and communications discovery", "", "Date: 2026-09-05  ", "Batch: `SN-SEM-B052`  ", "Status: **DISCOVERY QUEUE ONLY / UNREAD FULL ORIGINAL SOURCES / NO REVIEW OR ADMISSION**", "", "## Scope and boundary", "", "This queue covers marketing, advertising, SEO, social-media/community management, web analytics, journalism/reporting, publishing/editorial work, localisation/language work, and communications/PR. It selects natural three-skill first-route hypotheses by requiring a shared user-workflow envelope and at least two description-level route cues. This is stronger than topic-word co-occurrence, but is not a full-source semantic finding.", "", "No source review, provenance/licence assessment, prompts, targets, audit, admission, selector run, or metric was performed. Byte replay preserves frozen source binding only.", "", "## Frozen inputs and actual-union exclusion", "", f"The frozen source-native corpus contains 23,450 records (SHA-256 `{digest(CORPUS)}`); the reciprocal-triangle universe contains 49,823 hypotheses (SHA-256 `{digest(HYPOTHESES)}`). The actual B001--B051 source exclusion union contains 3,822 unique hashes from every historical reconciliation key, discovery ledger, queue, and full-source packet ledger, including unadmitted/discovery-only material. The B049/B050 ledgers share three member hashes, retained as a set-union fact.", "", "## Queue, preservation, and defer boundary", "", "`b052_source_native_semantic_family_queue.jsonl` has 25 deterministic triads. Each record has `family_id`, `batch_rank`, exactly three `member_source_sha256` values, `discovery_route`, original source-path/native-description bindings, and a route-cue hypothesis, so it is compatible with the canonical full-source materialiser without schema repair.", "", "`source_provenance_byte_replay_ledger.jsonl` preserves original source and frozen provenance replay pointers, without judging provenance or licence. `discovery_rejection_and_defer_ledger.jsonl` records all 25 selected triads as deferred pending independent full-source review. Mechanical non-selection counts are in `summary.json` and are not substantive rejections.", "", "## Source-disjointness result", "", "B052 has 25 families, 75 member occurrences, and 75 unique source hashes. Its intersection with the actual B001--B051 union is **0**; no B052 source repeats, and byte replay passes for **75/75** selected hashes.", "", "## Limitation", "", "The native-description workflow and route-cue gate is not proof of a shared bounded objective, independent first routes, or operational contrast, and is not a retrieval metric. All substantive decisions remain deferred to later independent full-source review.", ""])
    dossier_path = OUTPUT / "B052_DISCOVERY_DOSSIER_2026-09-05.md"; dossier_path.write_text(dossier, encoding="utf-8")
    summary["outputs"][dossier_path.name] = digest(dossier_path); summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": relative(OUTPUT), "counts": summary["counts"], "output_hashes": summary["outputs"]}, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
