#!/usr/bin/env python3
"""Materialise B046 discovery-only commerce/operations packets.

The replay reads only frozen literal native descriptions until selection is
complete.  Original source bytes are then preserved verbatim and rehashed.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from materialize_rq2b_source_native_b045_collaboration_ops import (
    BOOTSTRAP_SUMMARY, B039_LEDGER, B040_PACKETS, B041_PACKETS, B042_PACKETS,
    B043_PACKETS, B044_PACKETS, CORPUS, CORPUS_SUMMARY, HYPOTHESES, PROTOCOL,
    REVIEW, WORKSPACE, b001_b038_keys, b039_hashes, digest, family_path_count,
    packet_hashes, read_jsonl, relative, write_jsonl,
)

OUTPUT = REVIEW / "source_native_commerce_ecommerce_retail_sales_travel_hospitality_real_estate_logistics_procurement_b046_2026-09-04"
B045_PACKETS = REVIEW / "source_native_collaboration_project_management_meeting_notes_email_calendar_crm_customer_support_workflow_automation_b045_2026-09-04/b045_source_native_three_skill_full_original_packets.jsonl"

# Applied only to the frozen native-description literals.  The family must
# share at least one permitted task-family category across all three members.
ALLOWED = {
    "commerce": (r"\bcommerce\b", r"\bcommercial(?:ize|isation|ization)?\b", r"\bmarketplace\b", r"\bmerchant(?:s)?\b", r"\bproduct catalog(?:ue)?\b", r"\border management\b", r"\bproduct listing(?:s)?\b"),
    "ecommerce": (r"\be-?commerce\b", r"\bonline (?:store|shop|retail)\b", r"\bwebshop\b", r"\bshopping cart\b", r"\bshopify\b", r"\bwoocommerce\b", r"\bbigcommerce\b", r"\bcustomer orders?\b"),
    "retail": (r"\bretail\b", r"\bpoint[- ]of[- ]sale\b", r"\bpos\b", r"\bstore operations\b", r"\bcashier\b", r"\bmerchandise\b"),
    "sales": (r"\bsales?\b", r"\bsell(?:ing)?\b", r"\bdeal desk\b", r"\bsales enablement\b", r"\bsales pipeline\b", r"\bquota\b", r"\bterritor(?:y|ies)\b", r"\bquote(?:s|d)?\b", r"\bprospecting\b", r"\blead generation\b", r"\bbusiness development\b", r"\bgo-to-market\b", r"\boutbound\b", r"\bclosing deals?\b", r"\bconversion(?:s)?\b", r"\bprospects?\b", r"\bleads?\b", r"\baccount executive\b", r"\bcold outreach\b", r"\bb2[bc]\b", r"\brevenue(?: growth)?\b", r"\bsales calls?\b", r"\bsales demos?\b"),
    "travel": (r"\btravel\b", r"\btrip(?:s)?\b", r"\bitinerary\b", r"\bflight(?:s)?\b", r"\btourism\b", r"\bvacation\b", r"\btour(?:s|ing)?\b", r"\baccommodation(?:s)?\b"),
    "hospitality": (r"\bhospitality\b", r"\bhotel(?:s)?\b", r"\brestaurant(?:s)?\b", r"\bguest service\b", r"\bbooking(?:s)?\b", r"\breservation(?:s)?\b", r"\blodging\b", r"\bresort(?:s)?\b", r"\bcheck-in\b"),
    "real_estate": (r"\breal estate\b", r"\brealtor\b", r"\bproperty (?:listing|management|sale|sales)\b", r"\blisting(?:s)?\b", r"\bhome(?:s)?\b", r"\bresidential\b", r"\brental(?:s)?\b", r"\bleasing\b"),
    "logistics": (r"\blogistics\b", r"\bsupply chain\b", r"\bshipping\b", r"\bfreight\b", r"\bwarehouse\b", r"\bfulfil+l?ment\b", r"\bdelivery\b", r"\binventory\b", r"\btransportation\b", r"\bfleet\b", r"\bshipment(?:s)?\b", r"\btracking\b"),
    "procurement": (r"\bprocurement\b", r"\bpurchasing\b", r"\bsourcing\b", r"\bvendor management\b", r"\bpurchase order\b", r"\bsupplier(?:s)?\b", r"\brfq\b", r"\brfp\b", r"\btender(?:s)?\b", r"\bsupply management\b", r"\bvendor selection\b", r"\bsupplier relationship\b"),
}
COMPILED_ALLOWED = {name: tuple(re.compile(pattern, re.I) for pattern in patterns)
                    for name, patterns in ALLOWED.items()}

# Literal-description routing exclusions.  They deliberately include prior
# continuation scopes and the user-specified negative task families.
PROHIBITED = tuple(re.compile(pattern, re.I) for pattern in (
    # Creative/design/media.
    r"\bcreative\b", r"\bdesign(?:ing|er)?\b", r"\bgraphic(?:s)?\b", r"\billustrat", r"\btypography\b", r"\blayout\b", r"\bvisual\b", r"\bmedia\b", r"\bvideo\b", r"\baudio\b", r"\bpodcast\b", r"\bphotograph", r"\bpresentation\b", r"\bslides?\b", r"\bpowerpoint\b", r"\bkeynote\b", r"\bimage(?:s)?\b", r"\binfographic\b", r"\bposter\b", r"\bflyer\b", r"\bux\b", r"\buser experience\b", r"\buser interface\b", r"\bui design\b", r"\bwireframe\b", r"\bprototype\b", r"\bbranding?\b", r"\bcopywrit", r"\bseo\b", r"\bsocial media\b",
    # Legal/HR/finance/governance.
    r"\blegal\b", r"\blaw\b", r"\bcourt\b", r"\bcontract\b", r"\bcompliance\b", r"\bregulat", r"\bgovernance\b", r"\baudit\b", r"\brisk management\b", r"\bhuman resources\b", r"\brecruit", r"\bemployee\b", r"\bpayroll\b", r"\bfinance\b", r"\bfinancial\b", r"\baccounting\b", r"\bbudget\b", r"\binvoice\b", r"\btax\b", r"\binvest(?:ment|ing)\b",
    # Education/health/lifestyle.
    r"\beducation\b", r"\bteach(?:ing|er)?\b", r"\bstudent(?:s)?\b", r"\bcurriculum\b", r"\blesson(?:s)?\b", r"\bclassroom\b", r"\bpedagog", r"\bhomework\b", r"\bexam(?:s|ination)?\b", r"\bstudy(?:ing)?\b", r"\btutor(?:ing)?\b", r"\bcoach(?:ing|es)?\b", r"\bmentor(?:ing)?\b", r"\bhealth(?:care)?\b", r"\bpatient(?:s)?\b", r"\bclinical\b", r"\bmedical\b", r"\bmedicine\b", r"\btherapy\b", r"\bwell[- ]?being\b", r"\bwellness\b", r"\bmental health\b", r"\bfitness\b", r"\bworkout\b", r"\bexercise\b", r"\bnutrition\b", r"\bdiet\b", r"\bsleep\b", r"\bmindfulness\b", r"\bmeditation\b", r"\blifestyle\b", r"\bhousehold\b", r"\bgardening\b", r"\bcooking\b", r"\brecipes?\b",
    # Data/ML/security/observability.
    r"\bdata science\b", r"\bdata analys", r"\bmachine learning\b", r"\bdeep learning\b", r"\bneural network\b", r"\blarge language model\b", r"\bllm(?:s)?\b", r"\bmodel inference\b", r"\bmodel training\b", r"\bai eval", r"\bmodel eval", r"\bmodel benchmark", r"\bdata pipeline\b", r"\bdata ingestion\b", r"\bdata transformation\b", r"\bdata warehouse\b", r"\bdata lake\b", r"\bdata orchestrat", r"\bdatabase(?:s)?\b", r"\bsql\b", r"\bpostgres(?:ql)?\b", r"\bmysql\b", r"\bmongodb\b", r"\bsecurity\b", r"\bvulnerabilit", r"\bthreat model\b", r"\bpenetration test", r"\bencrypt(?:ion|ed)?\b", r"\bauthenti[ck]ation\b", r"\bauthori[sz]ation\b", r"\bmalware\b", r"\bprivacy\b", r"\bpii\b", r"\bpersonally identifiable\b", r"\bdata anonymi[sz]", r"\bdata redaction\b", r"\bdata minimization\b", r"\bobservability\b", r"\bmonitoring\b", r"\bdistributed tracing\b", r"\btelemetry\b", r"\blog(?:s|ging)\b", r"\bmetrics\b", r"\balert(?:ing|s)?\b",
    # Collaboration/CRM/email/calendar and developer/DevOps categories.
    r"\bcollaboration\b", r"\bcollaborative\b", r"\bproject management\b", r"\bmeeting notes?\b", r"\bmeeting minutes\b", r"\bemail(?:s)?\b", r"\binbox\b", r"\bcalendar\b", r"\bschedul(?:e|ing|er)\b", r"\bappointment(?:s)?\b", r"\bcrm\b", r"\bcustomer relationship management\b", r"\bcustomer support\b", r"\bcustomer service\b", r"\bhelp ?desk\b", r"\bsupport ticket(?:s|ing)?\b", r"\bworkflow automation\b", r"\bautomate workflows?\b", r"\bsoftware\b", r"\bdeveloper\b", r"\bdevelopment\b", r"\bcode\b", r"\bprogramming\b", r"\bapi\b", r"\bsdk\b", r"\bdevops\b", r"\bci/cd\b", r"\bcontinuous integration\b", r"\bcontinuous delivery\b", r"\bkubernetes\b", r"\bdocker\b", r"\bterraform\b", r"\binfrastructure as code\b", r"\bsource control\b", r"\bversion control\b", r"\bgit(?:hub|lab)?\b", r"\bcommit(?:s|ting)?\b", r"\bpull request\b", r"\bcode review\b", r"\bdeployment\b", r"\bbuild pipeline\b",
))

def categories(description: str) -> list[str]:
    return [name for name, patterns in COMPILED_ALLOWED.items() if any(pattern.search(description) for pattern in patterns)]

def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing B046 root: {OUTPUT}")
    inputs = (PROTOCOL, CORPUS, CORPUS_SUMMARY, HYPOTHESES, BOOTSTRAP_SUMMARY, B039_LEDGER, B040_PACKETS, B041_PACKETS, B042_PACKETS, B043_PACKETS, B044_PACKETS, B045_PACKETS)
    for path in inputs:
        if not path.is_file():
            raise SystemExit(f"missing frozen input: {path}")
    keys = b001_b038_keys()
    b001_b038 = set().union(*({str(row["canonical_source_sha256"]) for row in read_jsonl(path)} for path in keys.values()))
    if len(b001_b038) != 2850:
        raise SystemExit("B001-B038 exclusion cardinality mismatch")
    prior_parts = {
        "B001_B038": b001_b038, "B039": b039_hashes(),
        "B040": packet_hashes(B040_PACKETS, "SN-LEX-B040"), "B041": packet_hashes(B041_PACKETS, "SN-LEX-B041"),
        "B042": packet_hashes(B042_PACKETS, "SN-LEX-B042"), "B043": packet_hashes(B043_PACKETS, "SN-LEX-B043"),
        "B044": packet_hashes(B044_PACKETS, "SN-LEX-B044"), "B045": packet_hashes(B045_PACKETS, "SN-LEX-B045"),
    }
    excluded = set().union(*prior_parts.values())
    if len(excluded) != 3375 or sum(len(part) for part in prior_parts.values()) != 3375:
        raise SystemExit("B001-B045 exclusion union must contain 3,375 source hashes")
    corpus_rows = read_jsonl(CORPUS)
    corpus = {str(row["canonical_source_sha256"]): row for row in corpus_rows}
    hypotheses = read_jsonl(HYPOTHESES)
    if len(corpus) != 23450 or len(hypotheses) != 49823:
        raise SystemExit("frozen corpus/hypothesis cardinality mismatch")
    hypotheses.sort(key=lambda row: (-int(row["reciprocal_link_count"]), -float(row["rank_fusion_score"]), -family_path_count(row), row["member_source_sha256"]))
    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    exclusions: Counter[str] = Counter()
    prohibited_hits: Counter[str] = Counter()
    for hypothesis in hypotheses:
        hashes = [str(value) for value in hypothesis["member_source_sha256"]]
        if any(value not in corpus for value in hashes):
            raise SystemExit(f"corpus binding missing: {hypothesis['family_id']}")
        members = set(hashes)
        if members & excluded:
            exclusions["prior_B001_B045_inspected_source_overlap"] += 1; continue
        if members & used:
            exclusions["within_B046_source_collision"] += 1; continue
        descriptions = [str(corpus[value]["native_description"]) for value in hashes]
        shared = sorted(set.intersection(*(set(categories(description)) for description in descriptions)))
        if not shared:
            exclusions["no_shared_allowed_task_family"] += 1; continue
        matched = [pattern.pattern for description in descriptions for pattern in PROHIBITED if pattern.search(description)]
        if matched:
            exclusions["prohibited_scope_indicator"] += 1; prohibited_hits.update(set(matched)); continue
        selected.append({**hypothesis, "batch_id": "SN-LEX-B046", "batch_rank": len(selected) + 1, "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION", "selection_scope": "COMMERCE_ECOMMERCE_RETAIL_SALES_TRAVEL_HOSPITALITY_REAL_ESTATE_LOGISTICS_PROCUREMENT_FAMILIES_ONLY", "source_native_category_intersection": shared, "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE", "claim_boundary": "Source-native reciprocal-neighbour selection only; no semantic-family decision or downstream result."})
        used.update(members)
        if len(selected) == 25: break
    if len(selected) != 25 or len(used) != 75 or used & excluded:
        diagnostic = [(row["batch_rank"], row["source_native_category_intersection"], row["family_id"]) for row in selected]
        top_hits = prohibited_hits.most_common(30)
        raise SystemExit(f"B046 selection failure: families={len(selected)}, sources={len(used)}, exclusions={dict(exclusions)}, prohibited={top_hits}, selected={diagnostic}")
    OUTPUT.mkdir(parents=True)
    ledger = OUTPUT / "source_native_reciprocal_family_ledger.jsonl"
    write_jsonl(ledger, selected)
    packets: list[dict[str, Any]] = []
    replays: list[dict[str, Any]] = []
    for family in selected:
        members = []
        for source_hash, description_hash, source_paths in zip(family["member_source_sha256"], family["member_native_description_sha256"], family["member_source_paths"]):
            record = corpus[source_hash]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != source_paths:
                raise SystemExit(f"frozen description/path binding mismatch: {source_hash}")
            originals, replay_hashes = [], []
            for source_path in source_paths:
                raw = (WORKSPACE / source_path).read_bytes(); found = hashlib.sha256(raw).hexdigest()
                if found != source_hash: raise SystemExit(f"source-byte replay failed: {source_path}")
                replay_hashes.append(found); originals.append({"source_path": source_path, "canonical_source_sha256": source_hash, "preserved_original_skill_utf8": raw.decode("utf-8")})
            members.append({"canonical_source_sha256": source_hash, "native_description": record["native_description"], "native_description_sha256": description_hash, "source_native_allowed_categories": categories(record["native_description"]), "preserved_complete_original_sources": originals})
            replays.append({"record_type": "original_source_byte_replay", "canonical_source_sha256": source_hash, "source_paths": source_paths, "replayed_path_sha256": replay_hashes, "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256", "native_description_sha256": description_hash, "native_description_literal_replay_status": record["native_description_replay_status"], "claim_boundary": "Byte and native-description replay only; no downstream decision."})
        packets.append({"record_type": "source_native_three_skill_full_original_packet", "batch_id": "SN-LEX-B046", "batch_rank": family["batch_rank"], "family_id": family["family_id"], "selection_scope": family["selection_scope"], "source_native_category_intersection": family["source_native_category_intersection"], "reciprocal_neighbour_provenance": {"reciprocal_link_count": family["reciprocal_link_count"], "mutual_directional_ranks": family["mutual_directional_ranks"], "rank_fusion_score": family["rank_fusion_score"], "hypothesis_source_hashes": family["member_source_sha256"]}, "members": members, "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE", "claim_boundary": "Packet only; no semantic-family, prompt, adequacy, admission, selector, retrieval-result, or metric result."})
    if len(replays) != 75 or len({row["canonical_source_sha256"] for row in replays}) != 75:
        raise SystemExit("B046 replay cardinality failure")
    packet_path, replay_path = OUTPUT / "b046_source_native_three_skill_full_original_packets.jsonl", OUTPUT / "source_byte_replay_ledger.jsonl"
    write_jsonl(packet_path, packets); write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))
    summary = {"status": "PASS_B046_DISCOVERY_ONLY_SOURCE_NATIVE_COMMERCE_OPERATIONS_PACKETS", "claim_boundary": "Discovery packets only. These 25 three-skill hypotheses are not semantic-family findings, RQ2 cases, final-library entries, acceptable alternatives, retrieval results, or metrics.", "bound_inputs": {"protocol": digest(PROTOCOL), "source_native_description_corpus": digest(CORPUS), "source_native_description_corpus_summary": digest(CORPUS_SUMMARY), "frozen_lexical_mutual_triangle_hypotheses": digest(HYPOTHESES), "frozen_lexical_bootstrap_summary": digest(BOOTSTRAP_SUMMARY), "prior_B001_B038_internal_reconciliation_keys": {key: digest(path) for key, path in keys.items()}, "B039_source_native_discovery_ledger": digest(B039_LEDGER), "B040_full_original_source_packets": digest(B040_PACKETS), "B041_full_original_source_packets": digest(B041_PACKETS), "B042_full_original_source_packets": digest(B042_PACKETS), "B043_full_original_source_packets": digest(B043_PACKETS), "B044_full_original_source_packets": digest(B044_PACKETS), "B045_full_original_source_packets": digest(B045_PACKETS)}, "method": {"route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION", "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, distinct-source-path count descending, then sorted member source hashes", "allowed_scope_filter": "all three literal frozen native descriptions share at least one predeclared allowed task family and none matches a prohibited-scope indicator", "permitted_categories": list(ALLOWED), "prohibited_scope_indicators": [pattern.pattern for pattern in PROHIBITED], "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "prior outcome", "prompt", "label", "cluster membership"], "fresh_source_policy": "exclude every B001-B045 inspected source hash, including source-only and unadmitted queues; require source-disjoint members within B046"}, "counts": {"frozen_corpus_sources": len(corpus), "frozen_hypotheses": len(hypotheses), "prior_inspected_source_hashes_B001_B045": len(excluded), "prior_inspected_source_hashes_by_batch": {key: len(value) for key, value in prior_parts.items()}, "b046_families": len(selected), "b046_source_hashes": len(used), "b046_original_source_replays": len(replays), "source_hash_overlap_B046_vs_B001_B045": len(used & excluded), "selection_exclusions_encountered_before_completion": dict(sorted(exclusions.items())), "family_shared_category_counts": dict(sorted(Counter(category for row in selected for category in row["source_native_category_intersection"]).items()))}, "outputs": {ledger.name: digest(ledger), packet_path.name: digest(packet_path), replay_path.name: digest(replay_path)}, "verification": {"source_disjointness_B046_vs_B001_B045": "PASS", "original_source_byte_replay": "PASS_75_OF_75", "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS", "full_original_skill_materials_bound_for_later_reading": "PASS_25_PACKETS_75_SOURCES"}, "limitations": ["A lexical reciprocal-neighbour priority is not semantic similarity ground truth or a retrieval metric.", "The description-only scope screen is a routing constraint, not a source-quality, semantic-family, eligibility, or downstream decision.", "This batch does not perform review, provenance assessment, prompt work, adequacy work, admission, selector execution, or metrics."]}
    (OUTPUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": relative(OUTPUT), "counts": summary["counts"], "output_hashes": summary["outputs"]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
