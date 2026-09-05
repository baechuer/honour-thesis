#!/usr/bin/env python3
"""Materialise discovery-only B053 source-native first-route hypotheses."""
from __future__ import annotations
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import materialize_rq2b_source_native_b051_legal_regulatory_audit_tax_insurance_civic as m

OUT = m.REVIEW / ("source_native_education_tutoring_course_assessment_learning_content_"
                    "hr_recruiting_onboarding_career_b053_2026-09-05")
BASE = m.REVIEW
B049 = BASE / ("source_native_geospatial_maps_gis_iot_embedded_hardware_robotics_cad_"
               "3d_engineering_scientific_instrument_industrial_operations_b049_2026-09-05/"
               "source_native_reciprocal_family_ledger.jsonl")
B050 = BASE / ("source_native_healthcare_clinical_public_health_bioinformatics_chemistry_"
               "biology_lab_b050_2026-09-05/b050_source_native_semantic_family_queue.jsonl")
B051 = BASE / ("source_native_legal_regulatory_compliance_audit_tax_accounting_insurance_"
               "risk_civic_government_b051_2026-09-05/b051_source_native_semantic_family_queue.jsonl")
ROUTES = (
    ("FLASHCARD_DECK_CREATION", 1),
    ("HIRING_INTERVIEW_DESIGN", 1),
    ("JOB_APPLICATION_DOCUMENT_TAILORING", 16),
    ("JOB_LISTING_SEARCH", 7),
)
BANNED = (r"\bdeveloper\b", r"\bapi\b", r"\bsoftware\b", r"\bproduct onboarding\b",
          r"\bcustomer onboarding\b", r"\bmarketing\b", r"\bemail sequence\b",
          r"\bdrip campaign\b", r"\bhealth\b", r"\bclinical\b", r"\bmedical\b",
          r"\blegal\b", r"\bcompliance\b", r"\bsecurity\b", r"\bdatabase\b",
          r"\bprocurement\b", r"\bgeospatial\b", r"\bmachine learning\b",
          r"\bcreative\b", r"\bvideo\b", r"\baudio\b")

def rows(path):
    return m.read_jsonl(path)

def hashes(path, label):
    found = {str(v) for row in rows(path) for v in row["member_source_sha256"]}
    if len(found) != 75:
        raise SystemExit(f"{label} expected 75 unique hashes, got {len(found)}")
    return found

def first(description):
    return description.split("Do NOT", 1)[0].split("Not for", 1)[0][:500]

def any_match(text, pats):
    return any(re.search(p, text, re.I) for p in pats)

def categories(description):
    text = first(description)
    out = []
    if any_match(text, (r"\bresume\b", r"\bcover letter")) and any_match(text, (r"\bjob\b", r"\brole\b", r"\bapplication", r"\bats\b")):
        out.append("JOB_APPLICATION_DOCUMENT_TAILORING")
    if any_match(text, (r"\bjob search\b", r"\bjob listings?\b", r"\bjob vacancies?\b", r"\bfind (?:a )?job\b")):
        out.append("JOB_LISTING_SEARCH")
    if any_match(text, (r"\bhiring\b", r"\bcandidate\b")) and any_match(text, (r"\binterview\b", r"\bscorecard\b", r"\binterview questions?\b")):
        out.append("HIRING_INTERVIEW_DESIGN")
    if any_match(text, (r"\bflashcards?\b",)):
        out.append("FLASHCARD_DECK_CREATION")
    # Tested to make the wider requested B053 scope auditable.
    if any_match(text, (r"\bcourse\b", r"\bcurriculum\b", r"\bsyllabus\b", r"\blesson plan", r"\binstructional design")):
        out.append("COURSE_OR_CURRICULUM_DESIGN")
    if any_match(text, (r"\btutor(?:ing)?\b", r"\bstudy support\b", r"\bstudy plans?\b")):
        out.append("TUTORING_OR_STUDY_SUPPORT")
    if any_match(text, (r"\bassessment\b", r"\brubric", r"\bgrading\b", r"\bquiz", r"\bexam")) and any_match(text, (r"\bstudent", r"\blearning\b", r"\beducation", r"\bcourse\b", r"\bteach")):
        out.append("EDUCATIONAL_ASSESSMENT_DESIGN")
    if any_match(text, (r"\bworksheet", r"\bstudy guide", r"\blearning (?:content|materials?)", r"\beducational content", r"\bteaching materials?")):
        out.append("LEARNING_CONTENT_CREATION")
    if any_match(text, (r"\bemployee\b", r"\bstaff\b", r"\bnew[- ]hire\b", r"\bhr\b", r"\bhuman resources?\b")) and any_match(text, (r"\bonboarding\b", r"\borientation\b")):
        out.append("EMPLOYEE_ONBOARDING")
    return out

def main():
    if OUT.exists():
        raise SystemExit(f"refusing overwrite: {OUT}")
    inputs = (m.PROTOCOL, m.CORPUS, m.CORPUS_SUMMARY, m.HYPOTHESES, m.BOOTSTRAP_SUMMARY,
              m.B039_LEDGER, m.B040_PACKETS, m.B041_PACKETS, m.B042_PACKETS, m.B043_PACKETS,
              m.B044_PACKETS, m.B045_PACKETS, m.B046_PACKETS, m.B047_PACKETS, m.B048_PACKETS,
              B049, B050, B051)
    if any(not p.is_file() for p in inputs):
        raise SystemExit("missing a frozen/canonical B053 input")
    key_paths = m.b001_b038_keys()
    prior = {"B001_B038": {str(r["canonical_source_sha256"]) for p in key_paths.values() for r in rows(p)},
             "B039": m.b039_hashes(),
             "B040": m.packet_hashes(m.B040_PACKETS, "SN-LEX-B040"),
             "B041": m.packet_hashes(m.B041_PACKETS, "SN-LEX-B041"),
             "B042": m.packet_hashes(m.B042_PACKETS, "SN-LEX-B042"),
             "B043": m.packet_hashes(m.B043_PACKETS, "SN-LEX-B043"),
             "B044": m.packet_hashes(m.B044_PACKETS, "SN-LEX-B044"),
             "B045": m.packet_hashes(m.B045_PACKETS, "SN-LEX-B045"),
             "B046": m.packet_hashes(m.B046_PACKETS, "SN-LEX-B046"),
             "B047": m.packet_hashes(m.B047_PACKETS, "SN-LEX-B047"),
             "B048": m.packet_hashes(m.B048_PACKETS, "SN-LEX-B048"),
             "B049": hashes(B049, "B049"), "B050": hashes(B050, "B050"), "B051": hashes(B051, "B051")}
    excluded = set().union(*prior.values())
    if len(excluded) != 3822:
        raise SystemExit(f"B001-B051 union mismatch: {len(excluded)}")
    corpus = {str(r["canonical_source_sha256"]): r for r in rows(m.CORPUS)}
    hypotheses = rows(m.HYPOTHESES)
    if len(corpus) != 23450 or len(hypotheses) != 49823:
        raise SystemExit("frozen corpus/hypothesis cardinality mismatch")
    hypotheses.sort(key=lambda r: (-int(r["reciprocal_link_count"]), -float(r["rank_fusion_score"]), -m.family_path_count(r), r["member_source_sha256"]))
    candidates = {name: [] for name, _ in ROUTES}
    counts, broader = Counter(), Counter()
    route_labels = set(candidates)
    for h in hypotheses:
        hs = [str(x) for x in h["member_source_sha256"]]
        if len(hs) != 3 or len(set(hs)) != 3 or any(x not in corpus for x in hs):
            raise SystemExit(f"bad frozen triad: {h['family_id']}")
        if set(hs) & excluded:
            counts["REJECT_HISTORICAL_B001_B051_SOURCE_OVERLAP"] += 1
            continue
        desc = [str(corpus[x]["native_description"]) for x in hs]
        shared = sorted(set.intersection(*(set(categories(d)) for d in desc)))
        broader.update(shared)
        shared = [x for x in shared if x in route_labels]
        if not shared:
            counts["REJECT_NO_SHARED_B053_FIRST_ROUTE_CATEGORY"] += 1
            continue
        if any(any_match(first(d), BANNED) for d in desc):
            counts["REJECT_PROHIBITED_PRIOR_LANE_FIRST_ROUTE_INDICATOR"] += 1
            continue
        for route in shared:
            candidates[route].append((h, desc, shared))
    selected = []
    for route, quota in ROUTES:
        if len(candidates[route]) < quota:
            raise SystemExit(f"insufficient {route}: {len(candidates[route])}")
        for h, desc, shared in candidates[route][:quota]:
            selected.append({**h, "batch_id": "SN-SEM-B053", "batch_rank": len(selected) + 1,
                "discovery_route": "LEXICAL_RECIPROCAL_TRIANGLE_EXACT_NATIVE_DESCRIPTION_FIRST_ROUTE_SCOPE_GATE",
                "selection_scope": "EDUCATION_TUTORING_COURSE_ASSESSMENT_LEARNING_CONTENT_HR_RECRUITING_ONBOARDING_CAREER_FIRST_ROUTE_HYPOTHESES_ONLY",
                "source_native_first_route_category_intersection": shared,
                "native_description_first_route_hypothesis": " | ".join(" ".join(first(d).split())[:180] for d in desc),
                "review_state": "UNREVIEWED_FULL_SOURCE", "packet_state": "NOT_MATERIALISED_DISCOVERY_QUEUE_ONLY",
                "claim_boundary": "Literal native-description first-route hypothesis only; no full-source semantic-family, operational-route, or downstream decision."})
    occurrences = [x for f in selected for x in f["member_source_sha256"]]
    unique = set(occurrences)
    if len(selected) != 25 or len(occurrences) != 75 or unique & excluded:
        raise SystemExit("B053 selection failure")
    OUT.mkdir(parents=True)
    queue = OUT / "b053_source_native_semantic_family_queue.jsonl"
    m.write_jsonl(queue, selected)
    links, defers = [], []
    for family in selected:
        defers.append({"record_type": "discovery_defer", "batch_id": family["batch_id"], "batch_rank": family["batch_rank"],
                       "family_id": family["family_id"], "member_source_sha256": family["member_source_sha256"],
                       "disposition": "DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED",
                       "reason": "Native-description first-route evidence cannot establish bounded envelope, independent operational routes, member contrast, source adequacy, or promptability; later independent full-source review is required."})
        for source, desc_hash, paths in zip(family["member_source_sha256"], family["member_native_description_sha256"], family["member_source_paths"]):
            record = corpus[source]
            if record["native_description_sha256"] != desc_hash or record["source_paths"] != paths:
                raise SystemExit(f"binding mismatch: {source}")
            replay = [hashlib.sha256((m.WORKSPACE / p).read_bytes()).hexdigest() for p in paths]
            if any(x != source for x in replay):
                raise SystemExit(f"source replay mismatch: {source}")
            links.append({"record_type": "original_source_replay_provenance_link", "family_id": family["family_id"],
                          "batch_rank": family["batch_rank"], "canonical_source_sha256": source, "source_paths": paths,
                          "replayed_path_sha256": replay, "native_description_sha256": desc_hash,
                          "native_description_origin": record["native_description_origin"],
                          "claim_boundary": "Frozen path/hash replay and provenance pointer only; no source or provenance assessment."})
    replay_path, defer_path = OUT / "original_source_replay_provenance_link_ledger.jsonl", OUT / "discovery_rejection_and_defer_ledger.jsonl"
    m.write_jsonl(replay_path, links); m.write_jsonl(defer_path, defers)
    exclusion = {"record_type": "B053_historical_source_exclusion_manifest",
        "claim_boundary": "Hash-membership exclusion only; no semantic or review result.",
        "batches": {k: {"unique_source_hashes": len(v)} for k, v in prior.items()},
        "B001_B051_unique_source_hashes": len(excluded), "selection_member_occurrences": len(occurrences),
        "selection_unique_source_hashes": len(unique), "intersection_B053_vs_B001_B051": len(unique & excluded),
        "B052_cross_batch_intersection": "NOT_CHECKED_BY_DIRECTION; must be checked before any B053 review.",
        "historical_ledger_inputs": {**{f"B001_B038_{k}": m.digest(v) for k, v in key_paths.items()},
             "B039": m.digest(m.B039_LEDGER), "B040": m.digest(m.B040_PACKETS), "B041": m.digest(m.B041_PACKETS),
             "B042": m.digest(m.B042_PACKETS), "B043": m.digest(m.B043_PACKETS), "B044": m.digest(m.B044_PACKETS),
             "B045": m.digest(m.B045_PACKETS), "B046": m.digest(m.B046_PACKETS), "B047": m.digest(m.B047_PACKETS),
             "B048": m.digest(m.B048_PACKETS), "B049": m.digest(B049), "B050": m.digest(B050), "B051": m.digest(B051)}}
    exclusion_path = OUT / "historical_source_exclusion_manifest.json"
    exclusion_path.write_text(json.dumps(exclusion, indent=2, sort_keys=True) + "\n")
    summary = {"batch_id": "SN-SEM-B053", "status": "PASS_B053_DISCOVERY_QUEUE_ONLY_UNREVIEWED",
      "claim_boundary": "Discovery queue only; not source review, provenance/licence outcome, prompt, target assessment, admission, acceptable-set audit, selector result, or metric.",
      "bound_inputs": {"protocol": m.digest(m.PROTOCOL), "source_native_description_corpus": m.digest(m.CORPUS),
        "frozen_lexical_mutual_triangle_hypotheses": m.digest(m.HYPOTHESES), "historical_source_exclusion_manifest": m.digest(exclusion_path)},
      "method": {"route": "LEXICAL_RECIPROCAL_TRIANGLE_EXACT_NATIVE_DESCRIPTION_FIRST_ROUTE_SCOPE_GATE",
        "selection_input_boundary": "Only frozen literal native descriptions, frozen reciprocal-triangle fields, and B001-B051 source-hash membership; never source body, title, heading, path, provenance status, prompts, labels, outcomes, or cluster membership.",
        "base_hypothesis_order": "reciprocal-link descending, rank-fusion descending, distinct source-path count descending, then sorted source hashes; fixed route quotas retain first candidates in this order",
        "route_quotas": dict(ROUTES), "cross_family_source_policy": "No within-B053 source-disjointness claim; source reuse across distinct reciprocal triads is reported.",
        "fresh_source_policy": "Exclude every B001-B051 queued/ledger source hash.",
        "B052_boundary": "B052 was not inspected or used. B052-B053 hash intersection remains to be checked before review."},
      "counts": {"frozen_corpus_sources": len(corpus), "frozen_reciprocal_hypotheses": len(hypotheses),
        "historical_exclusion_B001_B051_unique_source_hashes": len(excluded), "b053_families": len(selected),
        "b053_member_occurrences": len(occurrences), "b053_unique_source_hashes": len(unique),
        "cross_family_repeated_member_occurrences": len(occurrences) - len(unique),
        "source_hash_overlap_B053_vs_B001_B051": len(unique & excluded), "source_replay_provenance_link_occurrences": len(links),
        "deferred_families": len(defers), "route_category_family_counts": dict(Counter(x for r in selected for x in r["source_native_first_route_category_intersection"])),
        "broader_B053_first_route_triads_before_quota": dict(broader), "mechanical_nonselection_counts": dict(counts)},
      "queue": queue.name, "full_source_review_packet_materializer_compatibility": {"status": "PASS_QUEUE_HAS_REQUIRED_TRIAD_BINDING_FIELDS",
        "required_fields_present": ["family_id", "batch_rank", "member_source_sha256", "discovery_route"],
        "each_member_source_sha256_length": 3, "packet_materialisation_status": "NOT_RUN_BY_B053_DISCOVERY_ONLY_SCOPE"},
      "outputs": {queue.name: m.digest(queue), replay_path.name: m.digest(replay_path), defer_path.name: m.digest(defer_path), exclusion_path.name: m.digest(exclusion_path)},
      "verification": {"source_disjointness_B053_vs_B001_B051": "PASS", "original_source_hash_path_replay": "PASS_75_OF_75_OCCURRENCES",
        "all_selected_families_deferred_pending_independent_full_source_review": "PASS_25_OF_25", "B052_cross_batch_intersection": "NOT_RUN_MUST_CHECK_BEFORE_REVIEW"}}
    dossier = f"""# B053 source-native education, learning-content, HR/recruiting and career discovery

Date: 2026-09-05
Batch: `SN-SEM-B053`
Status: **DISCOVERY QUEUE ONLY / UNREAD FULL ORIGINAL SOURCES / NO REVIEW OR ADMISSION**

## Scope and boundary

This prospective queue covers education/tutoring/course/assessment-design and learning-content creation, plus HR/recruiting/onboarding and career-support workflow language. It seeks three-skill **first-route hypotheses**: all three literal native descriptions expose one same bounded user-facing route at the start of their description. That is stronger than topic/title similarity, but remains a hypothesis until independent readers inspect the full preserved originals.

No source review, provenance/licence assessment, prompts, targets, audits, admission, selector run, or metric has been performed. Path/hash replay preserves frozen source binding only; it is not source review.

## Frozen inputs and route

The frozen source-native corpus has 23,450 sources (SHA-256 `{m.digest(m.CORPUS)}`), and the frozen reciprocal-triangle universe has 49,823 hypotheses (SHA-256 `{m.digest(m.HYPOTHESES)}`). The actual B001--B051 historical source-hash union is 3,822 unique hashes, rebuilt and bound in `historical_source_exclusion_manifest.json`.

The truthful route is `LEXICAL_RECIPROCAL_TRIANGLE_EXACT_NATIVE_DESCRIPTION_FIRST_ROUTE_SCOPE_GATE`. It reads only frozen literal native descriptions, reciprocal-triangle ordering, and source-hash exclusion. It never selects from source bodies, titles, headings, paths, provenance status, prompts, labels, outcomes, or cluster membership. Fixed quotas retain 1 flashcard-deck, 1 hiring-interview, 16 job-application-document, and 7 job-listing-search hypotheses. Course/curriculum, tutoring/study-support, educational-assessment, broader learning-content, and employee-onboarding predicates were tested but had no qualifying triad selected after B001--B051 exclusion; this is a discovery-screen fact, not evidence of their absence from the original pool.

## Queue, replay links, and defer evidence

`b053_source_native_semantic_family_queue.jsonl` contains 25 triads with exactly three canonical source hashes and an explicit route, compatible with a later full-source packet materialiser. `original_source_replay_provenance_link_ledger.jsonl` preserves each occurrence's hash, original source path, byte replay, and native-description hash/origin, without a provenance judgment. `discovery_rejection_and_defer_ledger.jsonl` defers every family because descriptions cannot establish bounded envelopes, independent operational routes, contrast, source adequacy, or promptability.

The 25 families have 75 member occurrences. A source can support more than one distinct reciprocal three-skill hypothesis, so B053 does not claim within-batch source disjointness; exact unique-source and repeat counts are in `summary.json`. The selected unique-hash intersection with B001--B051 is **0**.

## Required later check

**B052 was deliberately not inspected or used. The B052--B053 source-hash intersection remains to be checked before any B053 review.**

## Limitation

The reciprocal lexical index and literal first-route gate are discovery prioritisation, not semantic ground truth or a retrieval metric. This dossier does not establish semantic confusability, a valid RQ2 case, provenance quality, or suitability as a prompt target.
"""
    dossier_path = OUT / "B053_DISCOVERY_DOSSIER_2026-09-05.md"
    dossier_path.write_text(dossier)
    summary["outputs"][dossier_path.name] = m.digest(dossier_path)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": m.relative(OUT), "counts": summary["counts"], "output_hashes": summary["outputs"]}, indent=2))

if __name__ == "__main__":
    main()
