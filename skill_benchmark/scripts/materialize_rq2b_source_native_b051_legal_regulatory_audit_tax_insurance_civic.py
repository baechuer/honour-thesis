#!/usr/bin/env python3
"""Materialise the discovery-only B051 legal/regulatory/civic queue.

Selection reads only the frozen literal native descriptions and the frozen
reciprocal-triangle ledger.  Complete source bytes are read only after the
queue is fixed, to replay the already-recorded hashes; this is preservation,
not source review.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from materialize_rq2b_source_native_b046_commerce_ops import (
    B039_LEDGER, B040_PACKETS, B041_PACKETS, B042_PACKETS, B043_PACKETS,
    B044_PACKETS, B045_PACKETS, BOOTSTRAP_SUMMARY, CORPUS, CORPUS_SUMMARY,
    HYPOTHESES, PROTOCOL, REVIEW, WORKSPACE, b001_b038_keys, b039_hashes,
    digest, family_path_count, packet_hashes, read_jsonl, relative, write_jsonl,
)

OUTPUT = REVIEW / (
    "source_native_legal_regulatory_compliance_audit_tax_accounting_"
    "insurance_risk_civic_government_b051_2026-09-05"
)
B046_PACKETS = REVIEW / (
    "source_native_commerce_ecommerce_retail_sales_travel_hospitality_"
    "real_estate_logistics_procurement_b046_2026-09-04/"
    "b046_source_native_three_skill_full_original_packets.jsonl"
)
B047_PACKETS = REVIEW / (
    "source_native_academic_scientific_research_literature_review_"
    "citation_management_technical_writing_knowledge_organisation_"
    "statistics_mathematics_b047_2026-09-04/"
    "b047_source_native_three_skill_full_original_packets.jsonl"
)
B048_PACKETS = REVIEW / (
    "source_native_local_system_administration_desktop_productivity_"
    "document_conversion_ocr_pdf_spreadsheets_filesystem_file_organisation_"
    "backup_recovery_accessibility_input_b048_2026-09-04/"
    "b048_source_native_three_skill_full_original_packets.jsonl"
)
B049_LEDGER = REVIEW / (
    "source_native_geospatial_maps_gis_iot_embedded_hardware_robotics_cad_"
    "3d_engineering_scientific_instrument_industrial_operations_b049_2026-09-05/"
    "source_native_reciprocal_family_ledger.jsonl"
)
B050_QUEUE = REVIEW / (
    "source_native_healthcare_clinical_public_health_bioinformatics_chemistry_"
    "biology_lab_b050_2026-09-05/b050_source_native_semantic_family_queue.jsonl"
)

# These patterns are applied solely to each frozen, literal native description.
# A family needs one category shared by all three descriptions.  This is a
# first-route *hypothesis* gate, not a full-source semantic-family decision.
ALLOWED = {
    "legal": (
        r"(?<!for )\blegal\b", r"\blaw\b", r"\bcourt\b", r"\bstatute\b",
        r"\blitigation\b", r"\bcounsel\b", r"\blawyer\b", r"\blegal document(?:s)?\b",
        r"\bcontract review\b", r"\breview contracts?\b", r"\bcontract clause\b",
        r"\bcontract\b[^.]{0,160}\b(?:clause|nda|msa|agreement|obligation|redline|terms|legal|risk)\b",
        r"\b(?:clause|nda|msa|agreement|obligation|redline|terms|legal|risk)\b[^.]{0,160}\bcontract\b",
        r"\bagreement(?:s)?\b",
        r"\bmaster services? agreement\b", r"\bnon-disclosure\b", r"\bnda\b",
        r"\bdata processing agreement\b", r"\bterms of service\b",
    ),
    "regulatory_compliance": (
        r"\bregulat(?:ion|ory|ed|e)\b", r"\bISO(?:/IEC)?\b",
        r"\bdata protection (?:act|law)\b", r"\bGDPR\b",
        r"\bcompliance (?:advisor|assistant|program|framework|assessment|check)\b",
    ),
    "audit_assurance": (
        r"\binternal audit\b", r"\bexternal (?:financial )?audit\b",
        r"\bfinancial audit\b", r"\bSOX(?: 404)?\b", r"\baudit samples?\b",
        r"\baudit workpapers?\b", r"\binternal controls?\b", r"\bcontrol testing\b",
    ),
    "tax_accounting": (
        r"\btax(?:ation|es)?\b", r"\baccounting\b", r"\baccountant\b",
        r"\bbookkeep(?:ing|er)\b", r"\bgeneral ledger\b", r"\bfinancial statements?\b",
        r"\bbalance sheet\b", r"\bjournal entr(?:y|ies)\b",
    ),
    "insurance_risk": (
        r"\binsurance\b", r"\bunderwriting\b", r"\binsurance claims?\b",
        r"\brisk management\b", r"\brisk assessment\b", r"\brisk register\b",
    ),
    "civic_government": (
        r"\bgovernment\b", r"\bpublic sector\b", r"\bcivic\b", r"\bmunicipal\b",
        r"\bcitizen(?:s)?\b", r"\bpublic policy\b", r"\blegislation\b", r"\bpermits?\b",
        r"\bpublic benefits?\b", r"\bgovernment service(?:s)?\b",
    ),
}
COMPILED_ALLOWED = {
    name: tuple(re.compile(pattern, re.I) for pattern in patterns)
    for name, patterns in ALLOWED.items()
}

# Scope-routing exclusions intentionally do not contain the allowed expressions.
# They prevent a generic lexical neighbour from a previously completed lane
# becoming a B051 candidate merely because it also uses a broad compliance word.
PROHIBITED = tuple(re.compile(pattern, re.I) for pattern in (
    r"\bcreative\b", r"\bgraphic(?:s)?\b", r"\billustrat", r"\btypography\b",
    r"\bvideo\b", r"\baudio\b", r"\bpresentation\b", r"\bslides?\b", r"\bux\b",
    r"\bmachine learning\b", r"\bdeep learning\b", r"\blarge language model\b",
    r"\bdata science\b", r"\bdata pipeline\b", r"\bdatabase(?:s)?\b", r"\bsql\b",
    r"\bvulnerabilit", r"\bmalware\b", r"\bpenetration test", r"\bobservability\b",
    r"\bsoftware\b", r"\bdeveloper\b", r"\bprogramming\b", r"\bdevops\b",
    r"\bapi\b", r"\bendpoint(?:s)?\b", r"\bschema\b", r"\btest[- ]suite\b",
    r"\bsource code\b", r"\bcodebase\b", r"\brepository\b", r"\bgithub\b",
    r"\bopen[- ]source\b", r"\bagentic\b", r"\bplugin(?:s)?\b", r"\bmcp\b",
    r"\bkubernetes\b", r"\bdocker\b", r"\bsource control\b", r"\bpull request\b",
    r"\bhealth(?:care)?\b", r"\bpatient(?:s)?\b", r"\bclinical\b", r"\bmedical\b",
    r"\bbioinformatics\b", r"\bgenom(?:e|ic|ics)\b", r"\bchem(?:istry|ical)\b",
    r"\beducation\b", r"\bteach(?:ing|er)?\b", r"\bstudent(?:s)?\b", r"\bcurriculum\b",
    r"\btravel\b", r"\bhospitality\b", r"\bretail\b", r"\be-?commerce\b",
    r"\blogistics\b", r"\bprocurement\b", r"\bwarehouse\b", r"\bgeospatial\b",
    r"\bgis\b", r"\brobotics\b", r"\biot\b", r"\bcad\b", r"\b3d\b",
    r"\bscientific instrument", r"\bindustrial operations\b",
    r"\bliterature review\b", r"\bcitation(?:s)?\b", r"\bbibliograph", r"\btheorem\b",
    r"\bcalendar\b", r"\bmeeting notes?\b", r"\bcustomer support\b", r"\bcrm\b",
    r"\bhuman resources\b", r"\bhr\b", r"\brecruit(?:ing|ment)?\b",
))


def categories(description: str) -> list[str]:
    return [name for name, patterns in COMPILED_ALLOWED.items()
            if any(pattern.search(description) for pattern in patterns)]


def member_hashes(rows: list[dict[str, Any]], label: str) -> set[str]:
    values = {str(source) for row in rows for source in row["member_source_sha256"]}
    if len(values) != 75:
        raise SystemExit(f"{label} must bind exactly 75 unique member source hashes, found {len(values)}")
    return values


def short_lead(descriptions: list[str]) -> str:
    """Keep an auditable, non-evaluative pointer to the native descriptions."""
    return " | ".join(" ".join(text.split())[:180] for text in descriptions)


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing B051 root: {OUTPUT}")
    inputs = (PROTOCOL, CORPUS, CORPUS_SUMMARY, HYPOTHESES, BOOTSTRAP_SUMMARY,
              B039_LEDGER, B040_PACKETS, B041_PACKETS, B042_PACKETS,
              B043_PACKETS, B044_PACKETS, B045_PACKETS, B046_PACKETS,
              B047_PACKETS, B048_PACKETS, B049_LEDGER, B050_QUEUE)
    for path in inputs:
        if not path.is_file():
            raise SystemExit(f"missing frozen/canonical input: {path}")

    keys = b001_b038_keys()
    b001_b038 = set().union(*(
        {str(row["canonical_source_sha256"]) for row in read_jsonl(path)}
        for path in keys.values()
    ))
    if len(b001_b038) != 2850:
        raise SystemExit("B001-B038 exclusion cardinality mismatch")
    prior_parts = {
        "B001_B038": b001_b038,
        "B039": b039_hashes(),
        "B040": packet_hashes(B040_PACKETS, "SN-LEX-B040"),
        "B041": packet_hashes(B041_PACKETS, "SN-LEX-B041"),
        "B042": packet_hashes(B042_PACKETS, "SN-LEX-B042"),
        "B043": packet_hashes(B043_PACKETS, "SN-LEX-B043"),
        "B044": packet_hashes(B044_PACKETS, "SN-LEX-B044"),
        "B045": packet_hashes(B045_PACKETS, "SN-LEX-B045"),
        "B046": packet_hashes(B046_PACKETS, "SN-LEX-B046"),
        "B047": packet_hashes(B047_PACKETS, "SN-LEX-B047"),
        "B048": packet_hashes(B048_PACKETS, "SN-LEX-B048"),
        "B049": member_hashes(read_jsonl(B049_LEDGER), "B049"),
        "B050": member_hashes(read_jsonl(B050_QUEUE), "B050"),
    }
    excluded = set().union(*prior_parts.values())
    # B049 and B050 have three historical queue-member overlaps. Preserve the
    # two ledgers in full, but use their set union for the fresh-source gate.
    # This is a historical-ledger fact, not a B051 semantic conclusion.
    b049_b050_overlap = sorted(prior_parts["B049"] & prior_parts["B050"])
    if len(excluded) != 3747 or sum(len(part) for part in prior_parts.values()) != 3750 or len(b049_b050_overlap) != 3:
        raise SystemExit("B001-B050 exclusion union/cardinality mismatch")

    corpus_rows = read_jsonl(CORPUS)
    corpus = {str(row["canonical_source_sha256"]): row for row in corpus_rows}
    hypotheses = read_jsonl(HYPOTHESES)
    if len(corpus) != 23450 or len(hypotheses) != 49823:
        raise SystemExit("frozen corpus/hypothesis cardinality mismatch")
    hypotheses.sort(key=lambda row: (-int(row["reciprocal_link_count"]),
                                     -float(row["rank_fusion_score"]),
                                     -family_path_count(row), row["member_source_sha256"]))

    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    rejections: Counter[str] = Counter()
    prohibited_hits: Counter[str] = Counter()
    for hypothesis in hypotheses:
        hashes = [str(value) for value in hypothesis["member_source_sha256"]]
        if len(hashes) != 3 or len(set(hashes)) != 3:
            raise SystemExit(f"malformed non-triad hypothesis: {hypothesis['family_id']}")
        if any(value not in corpus for value in hashes):
            raise SystemExit(f"corpus binding missing: {hypothesis['family_id']}")
        members = set(hashes)
        if members & excluded:
            rejections["REJECT_HISTORICAL_B001_B050_SOURCE_OVERLAP"] += 1
            continue
        if members & used:
            rejections["REJECT_WITHIN_B051_SOURCE_COLLISION"] += 1
            continue
        descriptions = [str(corpus[value]["native_description"]) for value in hashes]
        shared = sorted(set.intersection(*(set(categories(description)) for description in descriptions)))
        if not shared:
            rejections["REJECT_NO_SHARED_B051_NATIVE_WORKFLOW_CATEGORY"] += 1
            continue
        matched = [pattern.pattern for description in descriptions for pattern in PROHIBITED
                   if pattern.search(description)]
        if matched:
            rejections["REJECT_PROHIBITED_PRIOR_LANE_SCOPE_INDICATOR"] += 1
            prohibited_hits.update(set(matched))
            continue
        selected.append({
            **hypothesis,
            "batch_id": "SN-SEM-B051",
            "batch_rank": len(selected) + 1,
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "selection_scope": "LEGAL_REGULATORY_COMPLIANCE_AUDIT_TAX_ACCOUNTING_INSURANCE_RISK_CIVIC_GOVERNMENT_FIRST_ROUTE_HYPOTHESES_ONLY",
            "source_native_category_intersection": shared,
            "native_description_first_route_hypothesis": short_lead(descriptions),
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "packet_state": "NOT_MATERIALISED_DISCOVERY_QUEUE_ONLY",
            "claim_boundary": "Source-native reciprocal-neighbour hypothesis only; no full-source semantic-family or first-route decision, and no downstream result.",
        })
        used.update(members)
        if len(selected) == 25:
            break
    if len(selected) != 25 or len(used) != 75 or used & excluded:
        raise SystemExit(
            f"B051 selection failure: families={len(selected)}, sources={len(used)}, "
            f"rejections={dict(rejections)}, selected={[row['family_id'] for row in selected]}"
        )

    OUTPUT.mkdir(parents=True)
    queue_path = OUTPUT / "b051_source_native_semantic_family_queue.jsonl"
    write_jsonl(queue_path, selected)

    provenance_replays: list[dict[str, Any]] = []
    dispositions: list[dict[str, Any]] = []
    for family in selected:
        family_hashes = list(family["member_source_sha256"])
        dispositions.append({
            "record_type": "discovery_defer",
            "batch_id": family["batch_id"],
            "batch_rank": family["batch_rank"],
            "family_id": family["family_id"],
            "member_source_sha256": family_hashes,
            "disposition": "DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED",
            "reason": "A native-description reciprocal hypothesis cannot establish bounded envelope, independent first routes, operational contrast, provenance/licence adequacy, or promptability; those require later independent full-source review.",
        })
        for source_hash, description_hash, source_paths in zip(
                family_hashes, family["member_native_description_sha256"], family["member_source_paths"]):
            record = corpus[source_hash]
            if (record["native_description_sha256"] != description_hash
                    or record["source_paths"] != source_paths):
                raise SystemExit(f"frozen description/path binding mismatch: {source_hash}")
            replay_hashes = []
            for source_path in source_paths:
                found = hashlib.sha256((WORKSPACE / source_path).read_bytes()).hexdigest()
                if found != source_hash:
                    raise SystemExit(f"source-byte replay failed: {source_path}")
                replay_hashes.append(found)
            provenance_replays.append({
                "record_type": "source_provenance_and_byte_replay",
                "canonical_source_sha256": source_hash,
                "source_paths": source_paths,
                "replayed_path_sha256": replay_hashes,
                "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                "native_description_sha256": description_hash,
                "native_description_origin": record["native_description_origin"],
                "native_description_literal_replay_status": record["native_description_replay_status"],
                "population_membership": record["population_membership"],
                "final_intake_role": record["final_intake_role"],
                "claim_boundary": "Frozen-record provenance and byte replay only; no provenance/licence assessment or downstream decision.",
            })
    if len(provenance_replays) != 75 or len({row["canonical_source_sha256"] for row in provenance_replays}) != 75:
        raise SystemExit("B051 byte-replay cardinality failure")
    replay_path = OUTPUT / "source_provenance_byte_replay_ledger.jsonl"
    disposition_path = OUTPUT / "discovery_rejection_and_defer_ledger.jsonl"
    write_jsonl(replay_path, sorted(provenance_replays, key=lambda row: row["canonical_source_sha256"]))
    write_jsonl(disposition_path, dispositions)

    exclusion_manifest = {
        "record_type": "B051_historical_source_exclusion_manifest",
        "claim_boundary": "Hash-membership exclusion only; it does not establish semantic distinctness or any review outcome.",
        "batches": {key: {"unique_source_hashes": len(value)} for key, value in prior_parts.items()},
        "B001_B050_unique_source_hashes": len(excluded),
        "historical_internal_queue_overlap": {
            "B049_B050_source_hashes": b049_b050_overlap,
            "B049_B050_overlap_count": len(b049_b050_overlap),
        },
        "selection_unique_source_hashes": len(used),
        "intersection_B051_vs_B001_B050": len(used & excluded),
        "historical_ledger_inputs": {
            "B001_B038_internal_reconciliation_keys": {key: digest(path) for key, path in keys.items()},
            "B039_source_native_discovery_ledger": digest(B039_LEDGER),
            "B040_full_original_source_packets": digest(B040_PACKETS),
            "B041_full_original_source_packets": digest(B041_PACKETS),
            "B042_full_original_source_packets": digest(B042_PACKETS),
            "B043_full_original_source_packets": digest(B043_PACKETS),
            "B044_full_original_source_packets": digest(B044_PACKETS),
            "B045_full_original_source_packets": digest(B045_PACKETS),
            "B046_full_original_source_packets": digest(B046_PACKETS),
            "B047_full_original_source_packets": digest(B047_PACKETS),
            "B048_full_original_source_packets": digest(B048_PACKETS),
            "B049_source_native_reciprocal_family_ledger": digest(B049_LEDGER),
            "B050_source_native_semantic_family_queue": digest(B050_QUEUE),
        },
    }
    exclusion_path = OUTPUT / "historical_source_exclusion_manifest.json"
    exclusion_path.write_text(json.dumps(exclusion_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = {
        "batch_id": "SN-SEM-B051",
        "status": "PASS_B051_DISCOVERY_QUEUE_ONLY_UNREVIEWED",
        "claim_boundary": "Discovery queue only; not a source review, provenance/licence outcome, prompt, target assessment, admission, acceptable-set audit, selector result, or metric.",
        "bound_inputs": {
            "protocol": digest(PROTOCOL),
            "source_native_description_corpus": digest(CORPUS),
            "source_native_description_corpus_summary": digest(CORPUS_SUMMARY),
            "frozen_lexical_mutual_triangle_hypotheses": digest(HYPOTHESES),
            "frozen_lexical_bootstrap_summary": digest(BOOTSTRAP_SUMMARY),
            "historical_source_exclusion_manifest": digest(exclusion_path),
        },
        "method": {
            "route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "semantic_intent_boundary": "The selection seeks a shared literal workflow category as a first-route hypothesis. It does not treat lexical links or category matches as established semantic confusability.",
            "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, distinct-source-path count descending, then sorted member source hashes; first non-overlapping 25 after fixed gates",
            "allowed_scope_filter": "all three literal frozen native descriptions share one predeclared B051 workflow category and none matches a prohibited prior-lane indicator",
            "permitted_categories": list(ALLOWED),
            "prohibited_scope_indicators": [pattern.pattern for pattern in PROHIBITED],
            "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "prior outcome", "prompt", "label", "cluster membership"],
            "fresh_source_policy": "exclude every B001-B050 queued/ledger source hash, including B049/B050 source-only and unadmitted material; require source-disjoint members within B051",
        },
        "counts": {
            "frozen_corpus_sources": len(corpus),
            "frozen_reciprocal_hypotheses": len(hypotheses),
            "historical_exclusion_B001_B050_unique_source_hashes": len(excluded),
            "b051_families": len(selected),
            "b051_member_occurrences": sum(len(row["member_source_sha256"]) for row in selected),
            "b051_unique_source_hashes": len(used),
            "source_hash_overlap_B051_vs_B001_B050": len(used & excluded),
            "within_B051_source_hash_collisions": 75 - len(used),
            "source_byte_replays": len(provenance_replays),
            "selection_rejection_counts_before_completion": dict(sorted(rejections.items())),
            "top_prohibited_scope_indicators": prohibited_hits.most_common(30),
            "family_shared_category_counts": dict(sorted(Counter(
                category for row in selected for category in row["source_native_category_intersection"]
            ).items())),
            "permitted_category_family_counts_including_zero": {
                category: sum(category in row["source_native_category_intersection"] for row in selected)
                for category in ALLOWED
            },
            "deferred_families": len(dispositions),
        },
        "queue": queue_path.name,
        "full_source_review_packet_materializer_compatibility": {
            "status": "PASS_QUEUE_HAS_REQUIRED_TRIAD_BINDING_FIELDS",
            "required_fields_present": ["family_id", "batch_rank", "member_source_sha256", "discovery_route"],
            "each_member_source_sha256_length": 3,
            "packet_materialisation_status": "NOT_RUN_BY_B051_DISCOVERY_ONLY_SCOPE",
        },
        "outputs": {
            queue_path.name: digest(queue_path),
            replay_path.name: digest(replay_path),
            disposition_path.name: digest(disposition_path),
            exclusion_path.name: digest(exclusion_path),
        },
        "verification": {
            "source_disjointness_B051_vs_B001_B050": "PASS",
            "original_source_byte_replay": "PASS_75_OF_75",
            "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS",
            "all_selected_families_deferred_pending_independent_full_source_review": "PASS_25_OF_25",
        },
        "limitations": [
            "The frozen reciprocal rank and literal category screen only prioritise reading; neither is semantic similarity ground truth or a retrieval metric.",
            "No complete original source was read for substantive review; byte replay is preservation only.",
            "All selected families remain deferred until later independent full-source review can test bounded envelope, independent first routes, operational contrast, provenance/licence adequacy and promptability.",
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    dossier = f"""# B051 source-native legal, regulatory/compliance, audit, tax/accounting, insurance/risk and civic/government discovery\n\nDate: 2026-09-05  \nBatch: `SN-SEM-B051`  \nStatus: **DISCOVERY QUEUE ONLY / UNREAD FULL ORIGINAL SOURCES / NO REVIEW OR ADMISSION**\n\n## Scope and boundary\n\nThis prospective queue is limited to legal, regulatory/compliance, audit and\nassurance, tax/accounting, insurance/risk, and civic/government workflow\nlanguage. It seeks three-skill **first-route hypotheses** from source-native\ndescriptions: same user-facing workflow envelope with potentially different\nprocedural routes. That is deliberately stronger than topic-word co-occurrence,\nbut remains a hypothesis until independent reviewers read the full preserved\noriginal skills.\n\nNo B051 source review, provenance/licence assessment, prompt work, target\nassessment, acceptable-set audit, admission, selector run or metric has been\nperformed. Byte replay below preserves the already frozen source binding; it is\nnot source review.\n\n## Frozen inputs and deterministic route\n\n- Frozen source-native corpus: 23,450 sources,\n  `manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl`, SHA-256\n  `{digest(CORPUS)}`.\n- Frozen reciprocal-triangle universe: 49,823 hypotheses,\n  `review/source_native_lexical_bootstrap_2026-09-04/all_mutual_triangle_hypotheses.jsonl`, SHA-256\n  `{digest(HYPOTHESES)}`.\n- Canonical B001--B050 historical exclusion set: 3,750 unique source hashes,\n  reconstructed and hash-bound in `historical_source_exclusion_manifest.json`.\n  This explicitly includes every B049 and B050 queue member, whether or not it\n  was later reviewed or admitted.\n\nThe only discovery route is\n`LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION`. It uses the frozen\nreciprocal native-description index and the protocol's deterministic ranking:\nreciprocal-link count descending, rank-fusion score descending, distinct source\npaths descending, then sorted member hashes. A source-native scope gate requires\nall three descriptions to share one declared B051 workflow category; a fixed\nprior-lane indicator gate removes mixed-domain lexical neighbours. The route\ndoes not use full source bodies, titles, paths, provenance status, prompts,\nlabels, outcomes or cluster membership to select a family.\n\n## Queue, provenance and defer boundary\n\n`b051_source_native_semantic_family_queue.jsonl` has 25 records. Each has a\nfamily ID, batch rank, exactly three canonical `member_source_sha256` values,\nand an explicit discovery route, so it can be supplied without schema repair to\na later full-source packet materialiser. It additionally retains original\nmember path and native-description hash bindings from the frozen hypothesis.\n\n`source_provenance_byte_replay_ledger.jsonl` records all 75 canonical hashes,\ncomplete preserved-source paths, frozen provenance fields and successful\nSHA-256 byte replays. It records no provenance or licence judgment.\n\nAll 25 families are recorded in `discovery_rejection_and_defer_ledger.jsonl`\nas `DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED`, with their exact member source\nhashes. The reason is uniform: native descriptions cannot establish the shared\nbounded envelope, independent first routes, member-level operational contrast,\nsource-quality sufficiency or promptability required by the protocol.\n\nMechanical non-selection reasons before reaching 25 are recorded as aggregate\ncounts in `summary.json`: historical B001--B050 source overlap, within-B051\nsource collision, no shared B051 native workflow category, and prohibited\nprior-lane indicator. None is a substantive family rejection.\n\n## Source-disjointness result\n\nThe B051 queue contains 25 families, 75 member occurrences and 75 unique\ncanonical source hashes. Its intersection with the B001--B050 reconstructed\nhistorical source-hash set is **0**; no source hash repeats within B051. The\nreplay ledger reports **75/75** preserved source-byte hash matches.\n\n## Limitation\n\nThe lexical reciprocal index is a discovery priority, not semantic ground\ntruth or a retrieval metric. This discovery dossier therefore does not claim\nthat any selected triad is a semantically confusable cluster, a valid RQ2\ncase, a provenance-qualified candidate, or a suitable prompt target.\n"""
    dossier = dossier.replace("3,750 unique source hashes", "3,747 unique source hashes")
    dossier = dossier.replace(
        "was later reviewed or admitted.\n\nThe only discovery route",
        "was later reviewed or admitted. B049 and B050 share three historical queue hashes; both ledgers and their 3,747-hash union are retained.\n\nThe only discovery route",
    )
    dossier_path = OUTPUT / "B051_DISCOVERY_DOSSIER_2026-09-05.md"
    dossier_path.write_text(dossier, encoding="utf-8")
    summary["outputs"][dossier_path.name] = digest(dossier_path)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": relative(OUTPUT), "counts": summary["counts"],
                      "output_hashes": summary["outputs"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
