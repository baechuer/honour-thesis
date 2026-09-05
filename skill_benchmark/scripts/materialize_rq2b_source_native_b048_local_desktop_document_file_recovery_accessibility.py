#!/usr/bin/env python3
"""Materialise B048 discovery-only local/desktop/document/file-access packets.

Selection reads only frozen literal native descriptions. Complete original
source bytes are preserved and rehashed only after selection is finished.
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
from materialize_rq2b_source_native_b047_academic_scientific import (
    ALLOWED as B047_ALLOWED,
    B046_PACKETS,
    PROHIBITED as B047_PROHIBITED,
)

OUTPUT = REVIEW / "source_native_local_system_administration_desktop_productivity_document_conversion_ocr_pdf_spreadsheets_filesystem_file_organisation_backup_recovery_accessibility_input_b048_2026-09-04"
B047_PACKETS = REVIEW / "source_native_academic_scientific_research_literature_review_citation_management_technical_writing_knowledge_organisation_statistics_mathematics_b047_2026-09-04/b047_source_native_three_skill_full_original_packets.jsonl"

ALLOWED = {
    "local_system_administration": (
        r"\blocal system administration\b", r"\bsystem administrat", r"\bsystem admin\b",
        r"\boperating system\b", r"\bmacos\b", r"\bwindows\b", r"\blinux\b",
        r"\bdevice settings\b", r"\bsystem settings\b", r"\bcontrol panel\b",
        r"\bapplication settings\b", r"\bdesktop settings\b", r"\buser account\b",
    ),
    "desktop_productivity": (
        r"\bdesktop productivity\b", r"\bdesktop application\b", r"\boffice suite\b",
        r"\bword processor\b", r"\btext editor\b", r"\bnote taking\b", r"\btask list\b",
        r"\bpersonal productivity\b", r"\bclipboard\b", r"\bproductivity\b",
        r"\bdesktop\b", r"\btext document\b", r"\bplain text\b",
    ),
    "document_conversion_ocr_pdf_spreadsheets": (
        r"\bdocument conversion\b", r"\bconvert (?:a |an )?(?:document|file|pdf)\b",
        r"\bocr\b", r"\boptical character recognition\b", r"\bpdf\b", r"\bspreadsheet\b",
        r"\bexcel\b", r"\bworkbook\b", r"\bcsv\b", r"\btabular file\b",
        r"\bdocuments?\b", r"\bextract (?:text|tables?)\b", r"\bmerge pdf\b",
        r"\bsplit pdf\b", r"\bscan(?:ned|ning)?\b",
    ),
    "filesystem_file_organisation": (
        r"\bfile system\b", r"\bfilesystem\b", r"\bfile organisation\b",
        r"\bfile organization\b", r"\bfile manager\b", r"\bfolder(?:s)?\b",
        r"\bdirectory\b", r"\brename files?\b", r"\borganise files?\b",
        r"\borganize files?\b", r"\bduplicate files?\b", r"\bfiles?\b",
        r"\bmove files?\b", r"\bfile names?\b", r"\bfile metadata\b",
    ),
    "backup_recovery": (
        r"\bbackup\b", r"\brestore\b", r"\brecovery\b", r"\brecover files?\b",
        r"\bdata recovery\b", r"\bdisaster recovery\b", r"\barchive files?\b",
        r"\bfile sync\b", r"\bsynchroni[sz](?:e|ation)\b", r"\brestore point\b",
    ),
    "accessibility_input": (
        r"\baccessibility\b", r"\bscreen reader\b", r"\bvoice control\b", r"\bvoice input\b",
        r"\bkeyboard\b", r"\bmouse\b", r"\binput device\b", r"\binput method\b",
        r"\bspeech recognition\b", r"\bdictation\b", r"\bassistive technolog",
        r"\bkeyboard shortcut\b", r"\bhotkey\b", r"\btyping\b", r"\bpointer\b",
    ),
}
COMPILED_ALLOWED = {name: tuple(re.compile(pattern, re.I) for pattern in patterns)
                    for name, patterns in ALLOWED.items()}

# B047's prohibition list covers every earlier continuation scope. Add the
# B047 academic/scientific families so B048 remains inside its stated route.
PROHIBITED = tuple(pattern for pattern in B047_PROHIBITED
                   if pattern.pattern != r"\bconversion(?:s)?\b") + tuple(
    re.compile(pattern, re.I)
    for patterns in B047_ALLOWED.values()
    for pattern in patterns
)


def categories(description: str) -> list[str]:
    return [name for name, patterns in COMPILED_ALLOWED.items()
            if any(pattern.search(description) for pattern in patterns)]


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing B048 root: {OUTPUT}")
    inputs = (PROTOCOL, CORPUS, CORPUS_SUMMARY, HYPOTHESES, BOOTSTRAP_SUMMARY,
              B039_LEDGER, B040_PACKETS, B041_PACKETS, B042_PACKETS,
              B043_PACKETS, B044_PACKETS, B045_PACKETS, B046_PACKETS, B047_PACKETS)
    for path in inputs:
        if not path.is_file():
            raise SystemExit(f"missing frozen input: {path}")
    keys = b001_b038_keys()
    b001_b038 = set().union(*({str(row["canonical_source_sha256"])
                                for row in read_jsonl(path)} for path in keys.values()))
    if len(b001_b038) != 2850:
        raise SystemExit("B001-B038 exclusion cardinality mismatch")
    prior_parts = {
        "B001_B038": b001_b038, "B039": b039_hashes(),
        "B040": packet_hashes(B040_PACKETS, "SN-LEX-B040"),
        "B041": packet_hashes(B041_PACKETS, "SN-LEX-B041"),
        "B042": packet_hashes(B042_PACKETS, "SN-LEX-B042"),
        "B043": packet_hashes(B043_PACKETS, "SN-LEX-B043"),
        "B044": packet_hashes(B044_PACKETS, "SN-LEX-B044"),
        "B045": packet_hashes(B045_PACKETS, "SN-LEX-B045"),
        "B046": packet_hashes(B046_PACKETS, "SN-LEX-B046"),
        "B047": packet_hashes(B047_PACKETS, "SN-LEX-B047"),
    }
    excluded = set().union(*prior_parts.values())
    if len(excluded) != 3525 or sum(len(part) for part in prior_parts.values()) != 3525:
        raise SystemExit("B001-B047 exclusion union must contain 3,525 source hashes")
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
    exclusions: Counter[str] = Counter()
    prohibited_hits: Counter[str] = Counter()
    for hypothesis in hypotheses:
        hashes = [str(value) for value in hypothesis["member_source_sha256"]]
        if any(value not in corpus for value in hashes):
            raise SystemExit(f"corpus binding missing: {hypothesis['family_id']}")
        members = set(hashes)
        if members & excluded:
            exclusions["prior_B001_B047_inspected_source_overlap"] += 1
            continue
        if members & used:
            exclusions["within_B048_source_collision"] += 1
            continue
        descriptions = [str(corpus[value]["native_description"]) for value in hashes]
        shared = sorted(set.intersection(*(set(categories(description)) for description in descriptions)))
        if not shared:
            exclusions["no_shared_allowed_task_family"] += 1
            continue
        matched = [pattern.pattern for description in descriptions for pattern in PROHIBITED
                   if pattern.search(description)]
        if matched:
            exclusions["prohibited_scope_indicator"] += 1
            prohibited_hits.update(set(matched))
            continue
        selected.append({**hypothesis, "batch_id": "SN-LEX-B048", "batch_rank": len(selected) + 1,
                         "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
                         "selection_scope": "LOCAL_SYSTEM_ADMINISTRATION_DESKTOP_PRODUCTIVITY_DOCUMENT_CONVERSION_OCR_PDF_SPREADSHEETS_FILESYSTEM_FILE_ORGANISATION_BACKUP_RECOVERY_ACCESSIBILITY_INPUT_FAMILIES_ONLY",
                         "source_native_category_intersection": shared,
                         "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE",
                         "claim_boundary": "Source-native reciprocal-neighbour selection only; no semantic-family decision or downstream result."})
        used.update(members)
        if len(selected) == 25:
            break
    if len(selected) != 25 or len(used) != 75 or used & excluded:
        diagnostic = [(row["batch_rank"], row["source_native_category_intersection"], row["family_id"])
                      for row in selected]
        raise SystemExit(f"B048 selection failure: families={len(selected)}, sources={len(used)}, "
                         f"exclusions={dict(exclusions)}, prohibited={prohibited_hits.most_common(30)}, "
                         f"selected={diagnostic}")
    OUTPUT.mkdir(parents=True)
    ledger = OUTPUT / "source_native_reciprocal_family_ledger.jsonl"
    write_jsonl(ledger, selected)
    packets: list[dict[str, Any]] = []
    replays: list[dict[str, Any]] = []
    for family in selected:
        members = []
        for source_hash, description_hash, source_paths in zip(
                family["member_source_sha256"], family["member_native_description_sha256"],
                family["member_source_paths"]):
            record = corpus[source_hash]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != source_paths:
                raise SystemExit(f"frozen description/path binding mismatch: {source_hash}")
            originals, replay_hashes = [], []
            for source_path in source_paths:
                raw = (WORKSPACE / source_path).read_bytes()
                found = hashlib.sha256(raw).hexdigest()
                if found != source_hash:
                    raise SystemExit(f"source-byte replay failed: {source_path}")
                replay_hashes.append(found)
                originals.append({"source_path": source_path, "canonical_source_sha256": source_hash,
                                  "preserved_original_skill_utf8": raw.decode("utf-8")})
            members.append({"canonical_source_sha256": source_hash,
                            "native_description": record["native_description"],
                            "native_description_sha256": description_hash,
                            "source_native_allowed_categories": categories(record["native_description"]),
                            "preserved_complete_original_sources": originals})
            replays.append({"record_type": "original_source_byte_replay", "canonical_source_sha256": source_hash,
                            "source_paths": source_paths, "replayed_path_sha256": replay_hashes,
                            "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                            "native_description_sha256": description_hash,
                            "native_description_literal_replay_status": record["native_description_replay_status"],
                            "claim_boundary": "Byte and native-description replay only; no downstream decision."})
        packets.append({"record_type": "source_native_three_skill_full_original_packet", "batch_id": "SN-LEX-B048",
                        "batch_rank": family["batch_rank"], "family_id": family["family_id"],
                        "selection_scope": family["selection_scope"],
                        "source_native_category_intersection": family["source_native_category_intersection"],
                        "reciprocal_neighbour_provenance": {"reciprocal_link_count": family["reciprocal_link_count"],
                            "mutual_directional_ranks": family["mutual_directional_ranks"],
                            "rank_fusion_score": family["rank_fusion_score"],
                            "hypothesis_source_hashes": family["member_source_sha256"]},
                        "members": members, "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE",
                        "claim_boundary": "Packet only; no semantic-family, prompt, adequacy, admission, selector, retrieval-result, or metric result."})
    if len(replays) != 75 or len({row["canonical_source_sha256"] for row in replays}) != 75:
        raise SystemExit("B048 replay cardinality failure")
    packet_path = OUTPUT / "b048_source_native_three_skill_full_original_packets.jsonl"
    replay_path = OUTPUT / "source_byte_replay_ledger.jsonl"
    write_jsonl(packet_path, packets)
    write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))
    summary = {
        "status": "PASS_B048_DISCOVERY_ONLY_SOURCE_NATIVE_LOCAL_DESKTOP_DOCUMENT_FILE_RECOVERY_ACCESSIBILITY_PACKETS",
        "claim_boundary": "Discovery packets only. These 25 three-skill hypotheses are not semantic-family findings, RQ2 cases, final-library entries, acceptable alternatives, retrieval results, or metrics.",
        "bound_inputs": {"protocol": digest(PROTOCOL), "source_native_description_corpus": digest(CORPUS),
            "source_native_description_corpus_summary": digest(CORPUS_SUMMARY),
            "frozen_lexical_mutual_triangle_hypotheses": digest(HYPOTHESES),
            "frozen_lexical_bootstrap_summary": digest(BOOTSTRAP_SUMMARY),
            "prior_B001_B038_internal_reconciliation_keys": {key: digest(path) for key, path in keys.items()},
            "B039_source_native_discovery_ledger": digest(B039_LEDGER),
            "B040_full_original_source_packets": digest(B040_PACKETS), "B041_full_original_source_packets": digest(B041_PACKETS),
            "B042_full_original_source_packets": digest(B042_PACKETS), "B043_full_original_source_packets": digest(B043_PACKETS),
            "B044_full_original_source_packets": digest(B044_PACKETS), "B045_full_original_source_packets": digest(B045_PACKETS),
            "B046_full_original_source_packets": digest(B046_PACKETS), "B047_full_original_source_packets": digest(B047_PACKETS)},
        "method": {"route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, distinct-source-path count descending, then sorted member source hashes",
            "allowed_scope_filter": "all three literal frozen native descriptions share at least one predeclared allowed task family and none matches a prohibited-scope indicator",
            "permitted_categories": list(ALLOWED), "prohibited_scope_indicators": [pattern.pattern for pattern in PROHIBITED],
            "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "prior outcome", "prompt", "label", "cluster membership"],
            "fresh_source_policy": "exclude every B001-B047 inspected source hash, including source-only and unadmitted queues; require source-disjoint members within B048"},
        "counts": {"frozen_corpus_sources": len(corpus), "frozen_hypotheses": len(hypotheses),
            "prior_inspected_source_hashes_B001_B047": len(excluded),
            "prior_inspected_source_hashes_by_batch": {key: len(value) for key, value in prior_parts.items()},
            "b048_families": len(selected), "b048_source_hashes": len(used), "b048_original_source_replays": len(replays),
            "source_hash_overlap_B048_vs_B001_B047": len(used & excluded),
            "selection_exclusions_encountered_before_completion": dict(sorted(exclusions.items())),
            "family_shared_category_counts": dict(sorted(Counter(category for row in selected for category in row["source_native_category_intersection"]).items()))},
        "outputs": {ledger.name: digest(ledger), packet_path.name: digest(packet_path), replay_path.name: digest(replay_path)},
        "verification": {"source_disjointness_B048_vs_B001_B047": "PASS", "original_source_byte_replay": "PASS_75_OF_75",
            "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS", "full_original_skill_materials_bound_for_later_reading": "PASS_25_PACKETS_75_SOURCES"},
        "limitations": ["A lexical reciprocal-neighbour priority is not semantic similarity ground truth or a retrieval metric.",
            "The description-only scope screen is a routing constraint, not a source-quality, semantic-family, eligibility, or downstream decision.",
            "This batch does not perform review, provenance assessment, prompt work, adequacy work, admission, selector execution, or metrics."],
    }
    (OUTPUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": relative(OUTPUT), "counts": summary["counts"], "output_hashes": summary["outputs"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
