#!/usr/bin/env python3
"""Materialise B041 creative/design/media discovery packets only.

Selection replays the frozen reciprocal lexical hypotheses and exact native
descriptions.  It does not read original bodies until after a family is fixed;
complete originals are then copied verbatim into unreviewed packets.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW = NC / "review"
PROTOCOL = REVIEW / "SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CORPUS = NC / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
CORPUS_SUMMARY = CORPUS.parent / "summary.json"
HYPOTHESES = REVIEW / "source_native_lexical_bootstrap_2026-09-04/all_mutual_triangle_hypotheses.jsonl"
BOOTSTRAP_SUMMARY = HYPOTHESES.parent / "summary.json"
OUTPUT = REVIEW / "source_native_creative_design_media_lexical_continuation_b041_2026-09-04"
B039_LEDGER = REVIEW / "source_native_dense_lexical_union_b039_2026-09-04/source_native_discovery_ledger.jsonl"
B040_QUEUE = REVIEW / "source_native_engineering_lexical_continuation_b040_2026-09-04/batch_040_full_source_review_queue_internal.jsonl"

# This scope partition is applied to literal, frozen native descriptions only.
# It deliberately does not inspect titles, paths, provenance, source bodies,
# prior results, prompts, labels, or review/admission outcomes.
CATEGORY_PATTERNS = {
    "creative_design": (
        r"\bcreative\b", r"\bdesign(?:ing|er)?\b", r"\bgraphic(?:s)?\b",
        r"\billustrat(?:e|ion|or)\b", r"\btypography\b", r"\blayout\b",
        r"\bvisual identity\b",
    ),
    "media": (
        r"\bmedia\b", r"\bvideo\b", r"\baudio\b", r"\bpodcast\b",
        r"\bphotograph(?:y|er)?\b", r"\bmotion graphics?\b", r"\bbroadcast\b",
    ),
    "presentation": (
        r"\bpresentation\b", r"\bslides?\b", r"\bslide deck\b",
        r"\bpowerpoint\b", r"\bkeynote\b", r"\bspeaker notes?\b",
    ),
    "visual_content": (
        r"\bvisual content\b", r"\bimages?\b", r"\binfographic\b",
        r"\bvisuali[sz]ation\b", r"\bposter\b", r"\bflyer\b",
        r"\bsocial (?:media )?content\b",
    ),
    "ux": (
        r"\bux\b", r"\buser experience\b", r"\buser interface\b",
        r"\bui design\b", r"\bwireframe\b", r"\bprototype\b",
        r"\busability\b", r"\binteraction design\b",
    ),
    "brand": (
        r"\bbrand(?:ing)?\b", r"\bbrand identity\b", r"\bbrand kit\b",
        r"\bbrand guidelines?\b", r"\bbrand voice\b",
    ),
    "marketing_content": (
        r"\bmarketing\b", r"\bcontent marketing\b", r"\bmarketing content\b",
        r"\bcampaign\b", r"\bcopywrit(?:e|ing|er)\b", r"\bseo\b",
        r"\bsocial media\b", r"\bpromotional content\b",
    ),
}
COMPILED_CATEGORIES = {
    category: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for category, patterns in CATEGORY_PATTERNS.items()
}
PROHIBITED_SCOPE = tuple(re.compile(pattern, re.IGNORECASE) for pattern in (
    r"\blegal\b", r"\blaw\b", r"\bcourt\b", r"\bcontract\b", r"\bcompliance\b",
    r"\bregulat(?:ion|ory)\b", r"\bgovernance\b", r"\baudit\b", r"\brisk management\b",
    r"\bhuman resources\b", r"\brecruit(?:ing|ment)?\b", r"\bemployee\b", r"\bpayroll\b",
    r"\bfinance\b", r"\bfinancial\b", r"\baccounting\b", r"\bbudget\b", r"\binvoice\b",
    r"\btax\b", r"\binvest(?:ment|ing)\b", r"\bsoftware\b", r"\bdeveloper\b",
    r"\bdevelopment\b", r"\bcode\b", r"\bprogramming\b", r"\bapi\b", r"\bsdk\b",
    r"\bdevops\b", r"\bci/cd\b", r"\bcontinuous integration\b", r"\bkubernetes\b",
    r"\bdocker\b", r"\bterraform\b", r"\binfrastructure\b", r"\bcloud\b", r"\bgit\b",
    r"\brepository\b", r"\bsource control\b", r"\bversion control\b", r"\btesting\b",
    r"\bpackage management\b", r"\bdependency\b", r"\bfrontend\b", r"\bbackend\b",
))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def family_path_count(row: dict[str, Any]) -> int:
    return len({path for paths in row["member_source_paths"] for path in paths})


def categories(description: str) -> list[str]:
    return [category for category, patterns in COMPILED_CATEGORIES.items() if any(pattern.search(description) for pattern in patterns)]


def prior_b001_b038_keys() -> dict[str, Path]:
    found: dict[str, Path] = {}
    pattern = re.compile(r"batch_(\d+)_full_source_review_packets/internal_reconciliation_key\.jsonl$")
    for path in REVIEW.glob("**/internal_reconciliation_key.jsonl"):
        match = pattern.search(relative(path))
        if match and 1 <= int(match.group(1)) <= 38:
            batch = f"B{int(match.group(1)):03d}"
            if batch in found:
                raise SystemExit(f"duplicate {batch} reconciliation key")
            found[batch] = path
    expected = {f"B{index:03d}" for index in range(1, 39)}
    if set(found) != expected:
        raise SystemExit(f"B001-B038 key mismatch: missing={sorted(expected - set(found))}")
    return dict(sorted(found.items()))


def b039_hashes() -> set[str]:
    records = read_jsonl(B039_LEDGER)
    if len(records) != 25:
        raise SystemExit("B039 discovery ledger must contain 25 families")
    values = {str(member["source_byte_sha256"]) for record in records for member in record["member_records"]}
    if len(values) != 75:
        raise SystemExit("B039 ledger must bind 75 distinct sources")
    return values


def b040_hashes() -> set[str]:
    records = read_jsonl(B040_QUEUE)
    if len(records) != 25:
        raise SystemExit("B040 queue must contain 25 families")
    values = {str(source) for record in records for source in record["member_source_sha256"]}
    if len(values) != 75:
        raise SystemExit("B040 queue must bind 75 distinct sources")
    return values


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing output: {OUTPUT}")
    for path in (PROTOCOL, CORPUS, CORPUS_SUMMARY, HYPOTHESES, BOOTSTRAP_SUMMARY, B039_LEDGER, B040_QUEUE):
        if not path.is_file():
            raise SystemExit(f"missing required input: {path}")

    keys = prior_b001_b038_keys()
    b001_b038 = set()
    for batch, path in keys.items():
        records = read_jsonl(path)
        if len(records) != 75:
            raise SystemExit(f"{batch} key does not contain 75 sources")
        b001_b038.update(str(record["canonical_source_sha256"]) for record in records)
    if len(b001_b038) != 2850:
        raise SystemExit(f"B001-B038 must bind 2,850 distinct sources, got {len(b001_b038)}")
    b039 = b039_hashes()
    b040 = b040_hashes()
    if b001_b038 & b039 or b001_b038 & b040 or b039 & b040:
        raise SystemExit("B001-B040 inspected-source sets are unexpectedly non-disjoint")
    excluded = b001_b038 | b039 | b040
    if len(excluded) != 3000:
        raise SystemExit(f"B001-B040 exclusion set must contain 3,000 sources, got {len(excluded)}")

    corpus_rows = read_jsonl(CORPUS)
    corpus = {str(row["canonical_source_sha256"]): row for row in corpus_rows}
    if len(corpus) != 23450:
        raise SystemExit("frozen corpus source count mismatch")
    hypotheses = read_jsonl(HYPOTHESES)
    hypotheses.sort(key=lambda row: (-int(row["reciprocal_link_count"]), -float(row["rank_fusion_score"]), -family_path_count(row), row["member_source_sha256"]))

    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    exclusion_counts: Counter[str] = Counter()
    for hypothesis in hypotheses:
        member_hashes = [str(value) for value in hypothesis["member_source_sha256"]]
        if any(value not in corpus for value in member_hashes):
            raise SystemExit(f"hypothesis member absent from corpus: {hypothesis['family_id']}")
        member_set = set(member_hashes)
        if member_set & excluded:
            exclusion_counts["prior_B001_B040_inspected_source_overlap"] += 1
            continue
        if member_set & used:
            exclusion_counts["within_B041_source_collision"] += 1
            continue
        descriptions = [str(corpus[value]["native_description"]) for value in member_hashes]
        if any(pattern.search(description) for description in descriptions for pattern in PROHIBITED_SCOPE):
            exclusion_counts["prohibited_noncreative_scope"] += 1
            continue
        shared = sorted(set.intersection(*(set(categories(description)) for description in descriptions)))
        if not shared:
            exclusion_counts["no_shared_creative_design_media_category"] += 1
            continue
        selected.append({
            **hypothesis,
            "batch_id": "SN-LEX-B041",
            "batch_rank": len(selected) + 1,
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "selection_scope": "CREATIVE_DESIGN_MEDIA_PRESENTATION_VISUAL_UX_BRAND_MARKETING_CONTENT_FAMILIES_ONLY",
            "source_native_category_intersection": shared,
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "claim_boundary": "Fresh-source creative/design/media lexical reading priority only; not a cluster result.",
        })
        used.update(member_set)
        if len(selected) == 25:
            break
    if len(selected) != 25 or len(used) != 75 or used & excluded:
        raise SystemExit("B041 selection failure")

    OUTPUT.mkdir(parents=True)
    queue = OUTPUT / "batch_041_full_source_review_queue_internal.jsonl"
    write_jsonl(queue, selected)

    packets: list[dict[str, Any]] = []
    replays: list[dict[str, Any]] = []
    for family in selected:
        members = []
        for source_hash, description_hash, expected_paths in zip(family["member_source_sha256"], family["member_native_description_sha256"], family["member_source_paths"]):
            record = corpus[source_hash]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != expected_paths:
                raise SystemExit(f"frozen native binding mismatch: {source_hash}")
            originals = []
            replay_hashes = []
            for source_path in record["source_paths"]:
                path = WORKSPACE / source_path
                source_bytes = path.read_bytes()
                replay_hash = hashlib.sha256(source_bytes).hexdigest()
                if replay_hash != source_hash:
                    raise SystemExit(f"original source byte replay failed: {source_path}")
                replay_hashes.append(replay_hash)
                originals.append({"source_path": source_path, "canonical_source_sha256": source_hash, "preserved_original_skill_utf8": source_bytes.decode("utf-8")})
            members.append({
                "canonical_source_sha256": source_hash,
                "native_description": record["native_description"],
                "native_description_sha256": description_hash,
                "native_description_origin": record["native_description_origin"],
                "native_description_literal_replay_status": record["native_description_replay_status"],
                "source_byte_replay": record["source_byte_replay"],
                "source_native_creative_design_media_categories": categories(record["native_description"]),
                "preserved_complete_original_sources": originals,
            })
            replays.append({
                "record_type": "original_source_byte_replay",
                "canonical_source_sha256": source_hash,
                "source_paths": record["source_paths"],
                "replayed_path_sha256": replay_hashes,
                "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                "native_description_sha256": description_hash,
                "native_description_literal_replay_status": record["native_description_replay_status"],
                "claim_boundary": "Byte and native-description replay only; no source review, provenance decision, or eligibility outcome.",
            })
        packets.append({
            "record_type": "source_native_confusable_family_full_original_source_packet",
            "batch_id": "SN-LEX-B041",
            "batch_rank": family["batch_rank"],
            "family_id": family["family_id"],
            "selection_scope": family["selection_scope"],
            "source_native_category_intersection": family["source_native_category_intersection"],
            "reciprocal_neighbour_provenance": {
                "reciprocal_link_count": family["reciprocal_link_count"],
                "mutual_directional_ranks": family["mutual_directional_ranks"],
                "rank_fusion_score": family["rank_fusion_score"],
                "hypothesis_source_hashes": family["member_source_sha256"],
            },
            "members": members,
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "claim_boundary": "Packet only; no source review, provenance review, prompt, adequacy, acceptable-set, admission, selector, retrieval result, or metric result.",
        })
    if len(replays) != 75 or len({row["canonical_source_sha256"] for row in replays}) != 75:
        raise SystemExit("B041 source replay cardinality failure")
    packets_path = OUTPUT / "batch_041_full_original_source_packets.jsonl"
    replay_path = OUTPUT / "source_byte_replay_ledger.jsonl"
    write_jsonl(packets_path, packets)
    write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))

    summary = {
        "status": "PASS_B041_DISCOVERY_ONLY_SOURCE_NATIVE_CREATIVE_DESIGN_MEDIA_FAMILY_PACKETS",
        "bound_inputs": {
            "protocol": digest(PROTOCOL),
            "source_native_description_corpus": digest(CORPUS),
            "source_native_description_corpus_summary": digest(CORPUS_SUMMARY),
            "frozen_lexical_mutual_triangle_hypotheses": digest(HYPOTHESES),
            "frozen_lexical_bootstrap_summary": digest(BOOTSTRAP_SUMMARY),
            "prior_B001_B038_internal_reconciliation_keys": {batch: digest(path) for batch, path in keys.items()},
            "B039_source_native_discovery_ledger": digest(B039_LEDGER),
            "B040_full_source_review_queue": digest(B040_QUEUE),
        },
        "method": {
            "route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, distinct-source-path count descending, then sorted member source hashes",
            "creative_design_media_filter": "all three literal source-native descriptions share at least one predeclared permitted category and none matches a prohibited scope indicator; categories and regexes are recorded in this script",
            "permitted_categories": list(CATEGORY_PATTERNS),
            "prohibited_scope_indicators": [pattern.pattern for pattern in PROHIBITED_SCOPE],
            "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "provenance status", "prior review outcome", "prompt", "label", "cluster membership"],
            "fresh_source_policy": "exclude every B001-B040 inspected source hash, including source-only and unadmitted queues; require source-disjoint members within B041",
        },
        "counts": {
            "frozen_corpus_sources": len(corpus_rows),
            "frozen_hypotheses": len(hypotheses),
            "prior_inspected_source_hashes_B001_B038": len(b001_b038),
            "prior_inspected_source_hashes_B039": len(b039),
            "prior_inspected_source_hashes_B040": len(b040),
            "prior_inspected_source_hashes_B001_B040": len(excluded),
            "b041_families": len(selected),
            "b041_source_hashes": len(used),
            "b041_original_source_replays": len(replays),
            "source_hash_overlap_B041_vs_B001_B040": len(used & excluded),
            "selection_exclusions_encountered_before_completion": dict(sorted(exclusion_counts.items())),
            "family_shared_category_counts": dict(sorted(Counter(category for row in selected for category in row["source_native_category_intersection"]).items())),
        },
        "outputs": {
            queue.name: digest(queue),
            packets_path.name: digest(packets_path),
            replay_path.name: digest(replay_path),
        },
        "verification": {
            "source_disjointness_B041_vs_B001_B040": "PASS",
            "original_source_byte_replay": "PASS_75_OF_75",
            "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS",
            "full_original_skill_materials_bound_for_later_review": "PASS_25_PACKETS_75_SOURCES",
        },
        "limitations": [
            "A lexical reciprocal-neighbour priority is not semantic similarity ground truth, a source-quality result, a family-validity decision, or a retrieval metric.",
            "The creative/design/media description filter is a scope restriction, not source review, provenance assessment, promptability assessment, or eligibility decision.",
            "No source review, provenance review, prompt authoring, prompt adequacy, acceptable-set work, admission, final-library eligibility, selector result, or metric has occurred.",
            "The dense source-native route remains unexecuted; this continuation does not repair that limitation or establish dense-versus-lexical coverage.",
        ],
        "claim_boundary": "Discovery packets only. These 25 hypotheses are not reviewed clusters, RQ2 cases, final-library entries, acceptable alternatives, retrieval results, or metrics.",
    }
    (OUTPUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": relative(OUTPUT), "counts": summary["counts"], "output_hashes": summary["outputs"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
