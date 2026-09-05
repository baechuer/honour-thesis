#!/usr/bin/env python3
"""Materialise B043 discovery-only source-native packets.

Family selection replays only frozen exact native descriptions and reciprocal
neighbour hypotheses.  Full originals are copied only after the family is
fixed, so their bodies cannot influence B043 selection.
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
B039_LEDGER = REVIEW / "source_native_dense_lexical_union_b039_2026-09-04/source_native_discovery_ledger.jsonl"
B040_PACKETS = REVIEW / "source_native_engineering_lexical_continuation_b040_2026-09-04/batch_040_full_original_source_packets.jsonl"
OUTPUT = REVIEW / "source_native_education_training_coaching_health_wellbeing_consumer_lifestyle_b043_2026-09-04"

# These patterns are applied only to the frozen literal native-description
# field.  A family needs one allowed category in common across all members.
ALLOWED_CATEGORY_PATTERNS = {
    "education": (
        r"\beducation\b", r"\bteach(?:ing|er)?\b", r"\bstudent(?:s)?\b",
        r"\bcurriculum\b", r"\blesson(?:s)?\b", r"\bclassroom\b",
        r"\bpedagog(?:y|ical)\b", r"\bhomework\b", r"\bexam(?:s|ination)?\b",
        r"\bstudy(?:ing)?\b", r"\btutor(?:ing)?\b",
    ),
    "training": (
        r"\btraining\b", r"\btrain(?:ing)?\b", r"\bpractice(?:s)?\b",
        r"\bskills? development\b", r"\blearning plan\b",
    ),
    "coaching": (
        r"\bcoach(?:ing|es)?\b", r"\bmentor(?:ing)?\b", r"\bcoachee\b",
    ),
    "health": (
        r"\bhealth(?:care)?\b", r"\bpatient(?:s)?\b", r"\bclinical\b",
        r"\bmedical\b", r"\bmedicine\b", r"\btherapy\b",
    ),
    "wellbeing": (
        r"\bwell[- ]?being\b", r"\bwellness\b", r"\bmental health\b",
        r"\bfitness\b", r"\bworkout\b", r"\bexercise\b", r"\bnutrition\b",
        r"\bdiet\b", r"\bsleep\b", r"\bmindfulness\b", r"\bmeditation\b",
    ),
    "consumer_lifestyle": (
        r"\blifestyle\b", r"\bpersonal (?:life|routine|organization|planning)\b",
        r"\bhousehold\b", r"\bhome (?:care|organization|maintenance)\b",
        r"\bgardening\b", r"\bcooking\b", r"\brecipes?\b",
    ),
}
COMPILED_ALLOWED = {
    category: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for category, patterns in ALLOWED_CATEGORY_PATTERNS.items()
}

# Any match removes the complete three-source family.  These are scope
# constraints, not judgements about source quality or suitability.
PROHIBITED_SCOPE = tuple(re.compile(pattern, re.IGNORECASE) for pattern in (
    # Creative/design/media/visual-content.
    r"\bcreative\b", r"\bdesign(?:ing|er)?\b", r"\bgraphic(?:s)?\b",
    r"\billustrat(?:e|ion|or)\b", r"\btypography\b", r"\blayout\b",
    r"\bvisual\b", r"\bmedia\b", r"\bvideo\b", r"\baudio\b",
    r"\bpodcast\b", r"\bphotograph(?:y|er)?\b", r"\bpresentation\b",
    r"\bslides?\b", r"\bpowerpoint\b", r"\bkeynote\b", r"\bimage(?:s)?\b",
    r"\binfographic\b", r"\bposter\b", r"\bflyer\b", r"\bux\b",
    r"\buser experience\b", r"\buser interface\b", r"\bui design\b",
    r"\bwireframe\b", r"\bprototype\b", r"\bbranding?\b", r"\bmarketing\b",
    r"\bcopywrit(?:e|ing|er)\b", r"\bseo\b", r"\bsocial media\b",
    # Legal/compliance/HR/finance/governance.
    r"\blegal\b", r"\blaw\b", r"\bcourt\b", r"\bcontract\b",
    r"\bcompliance\b", r"\bregulat(?:ion|ory)\b", r"\bgovernance\b",
    r"\baudit\b", r"\brisk management\b", r"\bhuman resources\b",
    r"\brecruit(?:ing|ment)?\b", r"\bemployee\b", r"\bpayroll\b",
    r"\bfinance\b", r"\bfinancial\b", r"\baccounting\b", r"\bbudget\b",
    r"\binvoice\b", r"\btax\b", r"\binvest(?:ment|ing)\b",
    # Software engineering/DevOps.
    r"\bsoftware\b", r"\bdeveloper\b", r"\bdevelopment\b", r"\bcode\b",
    r"\bprogramming\b", r"\bapi\b", r"\bsdk\b", r"\bdevops\b",
    r"\bci/cd\b", r"\bcontinuous integration\b", r"\bkubernetes\b",
    r"\bdocker\b", r"\bterraform\b", r"\binfrastructure\b", r"\bcloud\b",
    r"\bgit\b", r"\brepository\b", r"\bsource control\b", r"\bversion control\b",
    r"\btesting\b", r"\bpackage management\b", r"\bdependency\b",
    r"\bfrontend\b", r"\bbackend\b", r"\bdeployment\b", r"\bcommand line\b",
    r"\bcli\b", r"\bdatabase\b", r"\bsql\b",
))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def categories(description: str) -> list[str]:
    return [
        category for category, patterns in COMPILED_ALLOWED.items()
        if any(pattern.search(description) for pattern in patterns)
    ]


def family_path_count(row: dict[str, Any]) -> int:
    return len({path for paths in row["member_source_paths"] for path in paths})


def b001_b038_keys() -> dict[str, Path]:
    found: dict[str, Path] = {}
    pattern = re.compile(r"batch_(\d+)_full_source_review_packets/internal_reconciliation_key\.jsonl$")
    for path in REVIEW.glob("**/internal_reconciliation_key.jsonl"):
        match = pattern.search(relative(path))
        if match and 1 <= int(match.group(1)) <= 38:
            batch = f"B{int(match.group(1)):03d}"
            if batch in found:
                raise SystemExit(f"duplicate reconciliation key: {batch}")
            found[batch] = path
    expected = {f"B{number:03d}" for number in range(1, 39)}
    if set(found) != expected:
        raise SystemExit(f"B001-B038 key mismatch: missing={sorted(expected - set(found))}")
    return dict(sorted(found.items()))


def b039_hashes() -> set[str]:
    rows = read_jsonl(B039_LEDGER)
    hashes = {str(member["source_byte_sha256"]) for row in rows for member in row["member_records"]}
    if len(rows) != 25 or len(hashes) != 75:
        raise SystemExit("B039 ledger cardinality mismatch")
    return hashes


def b040_hashes() -> set[str]:
    rows = read_jsonl(B040_PACKETS)
    hashes = {str(member["canonical_source_sha256"]) for row in rows for member in row["members"]}
    if len(rows) != 25 or len(hashes) != 75:
        raise SystemExit("B040 packet cardinality mismatch")
    return hashes


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing B043 root: {OUTPUT}")
    for path in (PROTOCOL, CORPUS, CORPUS_SUMMARY, HYPOTHESES, BOOTSTRAP_SUMMARY, B039_LEDGER, B040_PACKETS):
        if not path.is_file():
            raise SystemExit(f"missing frozen input: {path}")

    keys = b001_b038_keys()
    b001_b038: set[str] = set()
    for batch, path in keys.items():
        rows = read_jsonl(path)
        hashes = {str(row["canonical_source_sha256"]) for row in rows}
        if len(rows) != 75 or len(hashes) != 75:
            raise SystemExit(f"{batch} inspected-source key cardinality mismatch")
        b001_b038.update(hashes)
    if len(b001_b038) != 2850:
        raise SystemExit(f"B001-B038 expected 2,850 sources, got {len(b001_b038)}")
    b039 = b039_hashes()
    b040 = b040_hashes()
    excluded = b001_b038 | b039 | b040
    if len(excluded) != 3000 or b001_b038 & b039 or b001_b038 & b040 or b039 & b040:
        raise SystemExit("B001-B040 inspected-source exclusion set mismatch")

    corpus_rows = read_jsonl(CORPUS)
    corpus = {str(row["canonical_source_sha256"]): row for row in corpus_rows}
    if len(corpus_rows) != 23450 or len(corpus) != 23450:
        raise SystemExit("frozen corpus cardinality mismatch")
    hypotheses = read_jsonl(HYPOTHESES)
    if len(hypotheses) != 49823:
        raise SystemExit("frozen reciprocal-hypothesis cardinality mismatch")
    hypotheses.sort(key=lambda row: (
        -int(row["reciprocal_link_count"]),
        -float(row["rank_fusion_score"]),
        -family_path_count(row),
        row["member_source_sha256"],
    ))

    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    exclusions: Counter[str] = Counter()
    for hypothesis in hypotheses:
        member_hashes = [str(value) for value in hypothesis["member_source_sha256"]]
        if any(value not in corpus for value in member_hashes):
            raise SystemExit(f"source absent from frozen corpus: {hypothesis['family_id']}")
        member_set = set(member_hashes)
        if member_set & excluded:
            exclusions["prior_B001_B040_inspected_source_overlap"] += 1
            continue
        if member_set & used:
            exclusions["within_B043_source_collision"] += 1
            continue
        descriptions = [str(corpus[value]["native_description"]) for value in member_hashes]
        if any(pattern.search(description) for description in descriptions for pattern in PROHIBITED_SCOPE):
            exclusions["prohibited_scope_indicator"] += 1
            continue
        shared_categories = sorted(set.intersection(*(set(categories(description)) for description in descriptions)))
        if not shared_categories:
            exclusions["no_shared_allowed_task_family"] += 1
            continue
        selected.append({
            **hypothesis,
            "batch_id": "SN-LEX-B043",
            "batch_rank": len(selected) + 1,
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "selection_scope": "EDUCATION_TRAINING_COACHING_HEALTH_WELLBEING_CONSUMER_LIFESTYLE_FAMILIES_ONLY",
            "source_native_category_intersection": shared_categories,
            "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE",
            "claim_boundary": "Source-native reciprocal-neighbour selection only; no semantic-family decision or downstream result.",
        })
        used.update(member_set)
        if len(selected) == 25:
            break
    if len(selected) != 25 or len(used) != 75 or used & excluded:
        raise SystemExit("B043 selection failure")

    OUTPUT.mkdir(parents=True)
    discovery = OUTPUT / "source_native_reciprocal_family_ledger.jsonl"
    write_jsonl(discovery, selected)

    packets: list[dict[str, Any]] = []
    replays: list[dict[str, Any]] = []
    for family in selected:
        members: list[dict[str, Any]] = []
        for source_hash, description_hash, expected_paths in zip(
            family["member_source_sha256"],
            family["member_native_description_sha256"],
            family["member_source_paths"],
        ):
            record = corpus[source_hash]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != expected_paths:
                raise SystemExit(f"frozen description/path binding mismatch: {source_hash}")
            originals = []
            replay_hashes = []
            for source_path in expected_paths:
                source_bytes = (WORKSPACE / source_path).read_bytes()
                replay_hash = hashlib.sha256(source_bytes).hexdigest()
                if replay_hash != source_hash:
                    raise SystemExit(f"source-byte replay failed: {source_path}")
                replay_hashes.append(replay_hash)
                originals.append({
                    "source_path": source_path,
                    "canonical_source_sha256": source_hash,
                    "preserved_original_skill_utf8": source_bytes.decode("utf-8"),
                })
            members.append({
                "canonical_source_sha256": source_hash,
                "native_description": record["native_description"],
                "native_description_sha256": description_hash,
                "native_description_origin": record["native_description_origin"],
                "native_description_literal_replay_status": record["native_description_replay_status"],
                "source_byte_replay": record["source_byte_replay"],
                "source_native_allowed_categories": categories(record["native_description"]),
                "preserved_complete_original_sources": originals,
            })
            replays.append({
                "record_type": "original_source_byte_replay",
                "canonical_source_sha256": source_hash,
                "source_paths": expected_paths,
                "replayed_path_sha256": replay_hashes,
                "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                "native_description_sha256": description_hash,
                "native_description_literal_replay_status": record["native_description_replay_status"],
                "claim_boundary": "Byte and native-description replay only; no eligibility or downstream decision.",
            })
        packets.append({
            "record_type": "source_native_three_skill_full_original_packet",
            "batch_id": "SN-LEX-B043",
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
            "packet_state": "UNREAD_FULL_ORIGINAL_SOURCE",
            "claim_boundary": "Packet only; no semantic-family, eligibility, prompt, adequacy, admission, selector, retrieval-result, or metric result.",
        })
    if len(replays) != 75 or len({row["canonical_source_sha256"] for row in replays}) != 75:
        raise SystemExit("B043 replay cardinality failure")
    packets_path = OUTPUT / "b043_source_native_three_skill_full_original_packets.jsonl"
    replay_path = OUTPUT / "source_byte_replay_ledger.jsonl"
    write_jsonl(packets_path, packets)
    write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))

    summary = {
        "status": "PASS_B043_DISCOVERY_ONLY_SOURCE_NATIVE_ALLOWED_FAMILY_PACKETS",
        "claim_boundary": "Discovery packets only. These 25 three-skill hypotheses are not semantic-family findings, RQ2 cases, final-library entries, acceptable alternatives, retrieval results, or metrics.",
        "bound_inputs": {
            "protocol": digest(PROTOCOL),
            "source_native_description_corpus": digest(CORPUS),
            "source_native_description_corpus_summary": digest(CORPUS_SUMMARY),
            "frozen_lexical_mutual_triangle_hypotheses": digest(HYPOTHESES),
            "frozen_lexical_bootstrap_summary": digest(BOOTSTRAP_SUMMARY),
            "prior_B001_B038_internal_reconciliation_keys": {batch: digest(path) for batch, path in keys.items()},
            "B039_source_native_discovery_ledger": digest(B039_LEDGER),
            "B040_full_original_source_packets": digest(B040_PACKETS),
        },
        "method": {
            "route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "base_hypothesis_order": "frozen reciprocal-link descending, rank-fusion descending, distinct-source-path count descending, then sorted member source hashes",
            "allowed_scope_filter": "all three literal source-native descriptions share at least one predeclared allowed category and none matches a prohibited-scope indicator; patterns are recorded in this script",
            "permitted_categories": list(ALLOWED_CATEGORY_PATTERNS),
            "prohibited_scope_indicators": [pattern.pattern for pattern in PROHIBITED_SCOPE],
            "prohibited_selection_inputs": ["source body", "title", "heading", "source path", "source origin", "provenance status", "prior outcome", "prompt", "label", "cluster membership"],
            "fresh_source_policy": "exclude every B001-B040 inspected source hash, including source-only and unadmitted queues; require source-disjoint members within B043",
        },
        "counts": {
            "frozen_corpus_sources": len(corpus_rows),
            "frozen_hypotheses": len(hypotheses),
            "prior_inspected_source_hashes_B001_B038": len(b001_b038),
            "prior_inspected_source_hashes_B039": len(b039),
            "prior_inspected_source_hashes_B040": len(b040),
            "prior_inspected_source_hashes_B001_B040": len(excluded),
            "b043_families": len(selected),
            "b043_source_hashes": len(used),
            "b043_original_source_replays": len(replays),
            "source_hash_overlap_B043_vs_B001_B040": len(used & excluded),
            "selection_exclusions_encountered_before_completion": dict(sorted(exclusions.items())),
            "family_shared_category_counts": dict(sorted(Counter(category for row in selected for category in row["source_native_category_intersection"]).items())),
        },
        "outputs": {
            discovery.name: digest(discovery),
            packets_path.name: digest(packets_path),
            replay_path.name: digest(replay_path),
        },
        "verification": {
            "source_disjointness_B043_vs_B001_B040": "PASS",
            "original_source_byte_replay": "PASS_75_OF_75",
            "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS",
            "full_original_skill_materials_bound_for_later_reading": "PASS_25_PACKETS_75_SOURCES",
        },
        "limitations": [
            "A lexical reciprocal-neighbour priority is not semantic similarity ground truth or a retrieval metric.",
            "The description-only scope screen is a routing constraint, not a source-quality, semantic-family, eligibility, or downstream decision.",
            "The dense source-native route remains unexecuted; this continuation does not repair that limitation or establish dense-versus-lexical coverage.",
        ],
    }
    (OUTPUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": relative(OUTPUT), "counts": summary["counts"], "output_hashes": summary["outputs"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
