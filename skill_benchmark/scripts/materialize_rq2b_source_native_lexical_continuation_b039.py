#!/usr/bin/env python3
"""Materialise B039 as a source-native, non-engineering reading queue only.

This is deliberately restricted to discovery: it replays frozen, original
native descriptions and binds complete original source bytes for later
independent review.  It makes no source-quality, semantic-family, prompt,
admission, or acceptable-set decision.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW_ROOT = NC_ROOT / "review"
PROTOCOL = REVIEW_ROOT / "SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CORPUS = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
HYPOTHESES = REVIEW_ROOT / "source_native_lexical_bootstrap_2026-09-04/all_mutual_triangle_hypotheses.jsonl"
OUTPUT_DIR = REVIEW_ROOT / "source_native_dense_lexical_union_b039_2026-09-04"
QUEUE = OUTPUT_DIR / "batch_039_full_source_review_queue_internal.jsonl"
DISCOVERY_LEDGER = OUTPUT_DIR / "source_native_discovery_ledger.jsonl"
SOURCE_REPLAY_LEDGER = OUTPUT_DIR / "source_byte_replay_ledger.jsonl"
FULL_SOURCE_PACKETS = OUTPUT_DIR / "batch_039_full_source_packets_unreviewed.jsonl"

BATCH_SIZE = 25
TOP_NEIGHBOURS = 12

# User-directed partition screen, deliberately applied only to the exact native
# descriptions after the frozen neighbour graph was built.  It excludes the
# engineering/developer route reserved for the parallel batch.  The screen is
# a routing constraint, not a substantive source assessment.
ENGINEERING_EXCLUSION_RE = re.compile(
    r"\b(?:developer(?:s)?|development|developing|code|coding|programming|api|sdk|cli|git|repository|"
    r"ci/cd|docker|kubernetes|infrastructure|cloud|tests?|testing|software|package|npm|maven|devops|"
    r"deployment|terraform|pulumi|source control|version control|security|application|mobile|configuration|"
    r"worker|queue|metrics|telemetry|database|sql|tokeni[sz]er|tokeni[sz]ation|machine learning|model|figma|"
    r"frontend|backend|architecture|release|documentation for engineers|c\+\+|java|php|javascript|android|"
    r"swift|react|node\.js|build|artifact|dependency|container|pipeline|html|skill artifact|SKILL\.md|"
    r"agent|src/|slash command|issues?|pull requests?|\bpr\b|prompt(?:s)? as versioned|bpe|wordpiece|rust|"
    r"heap snapshots?|call sites?|allocation|memory footprint|performance profiling|cognitive architecture|"
    r"permissions review|tool calls?|terminal sessions?|\bbash\b|auto[- ]?approves?|review hook)\b",
    re.IGNORECASE,
)
END_USER_APPLICATION_INCLUSION_RE = re.compile(
    r"\b(?:grant|legal|law|court|contract|store|shopify|seo|catalog|presentation|slide|meeting|event|travel|"
    r"planning|knowledge management|risk management|property management|scenario|community management|"
    r"product management|data|chart|research|business|stakeholder|brand|social content|document|workbook|"
    r"journal|publication|marketing|sales|customer|content|writer|writing|email|accounting|finance|budget|"
    r"invoice|tax|recruit|human resources|employee|payroll|health|clinical|patient|education|teaching|"
    r"learning|translation|language|media|news|compliance|policy|procurement|operations)\b|[\u4e00-\u9fff]",
    re.IGNORECASE,
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def family_path_count(row: dict[str, Any]) -> int:
    return len({path for member_paths in row["member_source_paths"] for path in member_paths})


def prior_review_keys() -> dict[int, Path]:
    keys: dict[int, Path] = {}
    pattern = re.compile(r"batch_(\d+)_full_source_review_packets/internal_reconciliation_key\.jsonl$")
    for path in REVIEW_ROOT.glob("**/internal_reconciliation_key.jsonl"):
        match = pattern.search(relative(path))
        if match and int(match.group(1)) <= 37:
            batch = int(match.group(1))
            if batch in keys:
                raise SystemExit(f"Duplicate B{batch:03d} reconciliation key")
            keys[batch] = path
    if set(keys) != set(range(1, 38)):
        raise SystemExit("B001-B037 reconciliation-key ledger is incomplete")
    return keys


def main() -> int:
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Refusing to overwrite existing output: {OUTPUT_DIR}")
    for required in (PROTOCOL, CORPUS, HYPOTHESES):
        if not required.is_file():
            raise SystemExit(f"Missing required input: {required}")

    keys = prior_review_keys()
    prior_source_hashes: set[str] = set()
    for batch, path in sorted(keys.items()):
        records = read_jsonl(path)
        if len(records) != 75:
            raise SystemExit(f"B{batch:03d} reconciliation key does not bind 75 sources")
        prior_source_hashes.update(str(record["canonical_source_sha256"]) for record in records)
    if len(prior_source_hashes) != 2775:
        raise SystemExit("B001-B037 prior-source ledger is not source-disjoint")

    b038_queue = REVIEW_ROOT / "source_native_dense_lexical_union_b038_2026-09-04/batch_038_full_source_review_queue_internal.jsonl"
    if not b038_queue.is_file():
        raise SystemExit("B038 source-only reserve queue is missing")
    b038_records = read_jsonl(b038_queue)
    if len(b038_records) != BATCH_SIZE:
        raise SystemExit("B038 source-only reserve must contain exactly 25 families")
    b038_source_hashes = {str(source) for record in b038_records for source in record["member_source_sha256"]}
    if len(b038_source_hashes) != 75 or prior_source_hashes & b038_source_hashes:
        raise SystemExit("B038 source-only reserve is not a fresh 75-source set")
    excluded_source_hashes = prior_source_hashes | b038_source_hashes

    corpus_records = read_jsonl(CORPUS)
    corpus = {str(record["canonical_source_sha256"]): record for record in corpus_records}
    if len(corpus) != 23450:
        raise SystemExit("Unexpected frozen source-native corpus cardinality")
    hypotheses = read_jsonl(HYPOTHESES)
    hypotheses.sort(
        key=lambda record: (
            -int(record["reciprocal_link_count"]),
            -float(record["rank_fusion_score"]),
            -family_path_count(record),
            record["member_source_sha256"],
        )
    )

    queue: list[dict[str, Any]] = []
    used_source_hashes: set[str] = set()
    excluded_prior_overlap = 0
    excluded_partition = 0
    excluded_within_batch_collision = 0
    for hypothesis in hypotheses:
        members = {str(source) for source in hypothesis["member_source_sha256"]}
        if members & excluded_source_hashes:
            excluded_prior_overlap += 1
            continue
        descriptions = [str(corpus[source]["native_description"]) for source in hypothesis["member_source_sha256"]]
        joined_descriptions = "\n".join(descriptions)
        if ENGINEERING_EXCLUSION_RE.search(joined_descriptions) or not END_USER_APPLICATION_INCLUSION_RE.search(joined_descriptions):
            excluded_partition += 1
            continue
        if members & used_source_hashes:
            excluded_within_batch_collision += 1
            continue
        queue.append(
            {
                **hypothesis,
                "batch_id": "SN-LEX-B039",
                "batch_rank": len(queue) + 1,
                "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
                "partition_route": "NON_ENGINEERING_END_USER_APPLICATION_DESCRIPTION_ONLY",
                "review_state": "UNREVIEWED_FULL_SOURCE",
                "claim_boundary": "Fresh-source lexical reading priority only. The non-engineering partition is a user-directed description-only routing constraint, not a source review, eligibility result, cluster result, prompt, admission, acceptable-set, selector, or metric.",
            }
        )
        used_source_hashes.update(members)
        if len(queue) == BATCH_SIZE:
            break
    if len(queue) != BATCH_SIZE or len(used_source_hashes) != 75 or used_source_hashes & excluded_source_hashes:
        raise SystemExit("Could not materialise 25 source-disjoint B039 families")

    output_member_hashes = [source for record in queue for source in record["member_source_sha256"]]
    if len(set(output_member_hashes)) != 75:
        raise SystemExit("B039 has an intra-batch source collision")
    OUTPUT_DIR.mkdir(parents=True)
    write_jsonl(QUEUE, queue)

    packet_records: list[dict[str, Any]] = []
    source_replays: list[dict[str, Any]] = []
    source_replay_seen: set[str] = set()
    discovery_records: list[dict[str, Any]] = []
    for queue_record in queue:
        member_records: list[dict[str, Any]] = []
        ledger_members: list[dict[str, Any]] = []
        for member_index, source_hash in enumerate(queue_record["member_source_sha256"], start=1):
            corpus_record = corpus[source_hash]
            source_paths = [str(path) for path in corpus_record["source_paths"]]
            replay_paths = [WORKSPACE / path for path in source_paths]
            missing_paths = [relative(path) for path in replay_paths if not path.is_file()]
            if missing_paths:
                raise SystemExit(f"Missing preserved source path(s) for {source_hash}: {missing_paths}")
            byte_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in replay_paths]
            if any(byte_hash != source_hash for byte_hash in byte_hashes):
                raise SystemExit(f"Original source byte replay failed for {source_hash}")
            complete_original_skill = replay_paths[0].read_text(encoding="utf-8")
            member_records.append(
                {
                    "member_token": f"S-{member_index}",
                    "source_byte_sha256": source_hash,
                    "complete_original_skill": complete_original_skill,
                }
            )
            ledger_members.append(
                {
                    "source_byte_sha256": source_hash,
                    "source_paths": source_paths,
                    "native_description": corpus_record["native_description"],
                    "native_description_sha256": corpus_record["native_description_sha256"],
                    "native_description_origin": corpus_record["native_description_origin"],
                    "native_description_replay_status": corpus_record["native_description_replay_status"],
                }
            )
            if source_hash not in source_replay_seen:
                source_replay_seen.add(source_hash)
                source_replays.append(
                    {
                        "record_type": "original_source_byte_replay",
                        "canonical_source_sha256": source_hash,
                        "source_paths": source_paths,
                        "replayed_path_sha256": byte_hashes,
                        "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                        "native_description": corpus_record["native_description"],
                        "native_description_sha256": corpus_record["native_description_sha256"],
                        "native_description_origin": corpus_record["native_description_origin"],
                        "native_description_replay_status": corpus_record["native_description_replay_status"],
                        "claim_boundary": "Byte and native-description replay only; no source review or provenance decision.",
                    }
                )
        family_token = "F-" + hashlib.sha256(queue_record["family_id"].encode("utf-8")).hexdigest()[:16]
        packet_records.append(
            {
                "packet_type": "UNREVIEWED_FULL_ORIGINAL_SOURCE_PACKET",
                "family_token": family_token,
                "members": member_records,
                "review_state": "NOT_REVIEWED",
                "claim_boundary": "Complete preserved originals for later independent review only; no reviewer assessment is included.",
            }
        )
        discovery_records.append(
            {
                "record_type": "source_native_discovery_selection",
                "batch_id": "SN-LEX-B039",
                "batch_rank": queue_record["batch_rank"],
                "family_id": queue_record["family_id"],
                "family_token": family_token,
                "member_records": ledger_members,
                "mutual_directional_ranks": queue_record["mutual_directional_ranks"],
                "reciprocal_link_count": queue_record["reciprocal_link_count"],
                "rank_fusion_score": queue_record["rank_fusion_score"],
                "distinct_source_path_count": family_path_count(queue_record),
                "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
                "partition_route": "NON_ENGINEERING_END_USER_APPLICATION_DESCRIPTION_ONLY",
                "partition_screen": "No engineering-exclusion regex match and at least one end-user/application inclusion regex match, applied to the exact native descriptions only after frozen reciprocal-neighbour hypotheses were loaded.",
                "review_state": "UNREVIEWED_FULL_SOURCE",
                "claim_boundary": "Selection and reciprocal-neighbour provenance only; not a source review, eligibility, cluster, prompt, admission, acceptable-set, selector, or metric result.",
            }
        )
    if len(source_replays) != 75 or len(packet_records) != BATCH_SIZE or len(discovery_records) != BATCH_SIZE:
        raise SystemExit("B039 packet or replay-ledger count failure")
    write_jsonl(DISCOVERY_LEDGER, discovery_records)
    write_jsonl(SOURCE_REPLAY_LEDGER, sorted(source_replays, key=lambda record: record["canonical_source_sha256"]))
    write_jsonl(FULL_SOURCE_PACKETS, packet_records)

    summary = {
        "status": "PASS_SOURCE_NATIVE_LEXICAL_ONLY_CONTINUATION_B039_UNREVIEWED_FAMILY_HYPOTHESES",
        "bound_inputs": {
            relative(PROTOCOL): digest(PROTOCOL),
            relative(CORPUS): digest(CORPUS),
            relative(HYPOTHESES): digest(HYPOTHESES),
            "B001_B037_reconciliation_keys": {f"B{batch:03d}": digest(path) for batch, path in sorted(keys.items())},
            "B038_source_only_reserve_queue": digest(b038_queue),
        },
        "parameters": {
            "batch_families": BATCH_SIZE,
            "frozen_lexical_top_neighbours": TOP_NEIGHBOURS,
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "ranking_rule": "reciprocal_link_count_desc_then_rank_fusion_desc_then_distinct_source_path_count_desc_then_sorted_member_source_hashes_asc",
            "fresh_source_policy": "exclude_every_source_hash_in_B001_to_B037_reconciliation_keys_and_B038_source_only_reserve_queue; disjoint_members_within_B039",
            "partition": {
                "route": "NON_ENGINEERING_END_USER_APPLICATION_DESCRIPTION_ONLY",
                "directive": "B039 is reserved for non-engineering end-user/application task families: productivity, CRM/support, content/publishing, finance/operations, and research/data analysis. Developer tooling, DevOps, source control, CI/CD, cloud/infrastructure, testing, code generation, and package management are excluded for the parallel engineering batch.",
                "screen_input": "exact frozen native descriptions only; no title, source path, full source body, provenance, prompt, outcome, or manual source review used",
                "engineering_exclusion_regex": ENGINEERING_EXCLUSION_RE.pattern,
                "end_user_application_inclusion_regex": END_USER_APPLICATION_INCLUSION_RE.pattern,
            },
            "dense_status": "NOT_EXECUTED_NO_PROVIDER_CREDENTIAL_IN_PROCESS_ENVIRONMENT_NO_PROVIDER_CONTACT",
        },
        "counts": {
            "prior_batches": 38,
            "B001_B037_prior_source_hashes": len(prior_source_hashes),
            "B038_source_only_reserve_hashes": len(b038_source_hashes),
            "B001_B038_excluded_source_hashes": len(excluded_source_hashes),
            "b039_families": len(queue),
            "b039_sources": len(used_source_hashes),
            "b039_original_source_replays": len(source_replays),
            "hypotheses_excluded_due_to_prior_source_overlap": excluded_prior_overlap,
            "hypotheses_excluded_by_non_engineering_partition": excluded_partition,
            "hypotheses_excluded_due_to_b039_source_collision": excluded_within_batch_collision,
        },
        "outputs": {
            QUEUE.name: digest(QUEUE),
            DISCOVERY_LEDGER.name: digest(DISCOVERY_LEDGER),
            SOURCE_REPLAY_LEDGER.name: digest(SOURCE_REPLAY_LEDGER),
            FULL_SOURCE_PACKETS.name: digest(FULL_SOURCE_PACKETS),
        },
        "verification": {
            "source_disjointness_B039_vs_B001_B038": "PASS",
            "original_source_byte_replay": "PASS_75_OF_75",
            "native_description_replay_status": "PASS_75_OF_75_FROM_FROZEN_CORPUS",
            "full_original_skill_materials_bound_for_later_review": "PASS_25_PACKETS_75_SOURCES",
        },
        "claim_boundary": "B039 is a source-native lexical discovery queue with unreviewed full-original-source packets. It contains no source review, provenance decision, prompt authoring, target adequacy review, acceptable-set audit, eligibility or admission declaration, retrieval metric, selector result, or final-library change.",
        "limitations": [
            "Dense semantic retrieval remains unexecuted because no provider credential/transport decision is recorded; this lexical continuation does not establish dense coverage or a lexical-versus-dense comparison.",
            "The user-directed partition screen is a conservative description-only routing constraint. It may exclude in-scope end-user work that uses an excluded technical word or retain a lead whose complete original source later requires rejection; only later independent full-source review can decide the family rubric.",
        ],
    }
    write_json(OUTPUT_DIR / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
