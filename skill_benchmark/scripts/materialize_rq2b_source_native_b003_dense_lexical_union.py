#!/usr/bin/env python3
"""Materialise an unread source-reading queue from frozen lexical+BGE ranks.

The output is mechanical candidate prioritisation only.  It never reads full
source bodies, prompts, labels, review outcomes, or provenance roles.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
DESIGN = NC_ROOT / "review/B003_CANDIDATE_DISCOVERY_PRE_RESULT_NO_EXECUTION_DESIGN_2026-09-04.md"
DESCRIPTION_BINDINGS = NC_ROOT / "manifests/source_native_description_local_bge_embedding_preflight_2026-09-04/source_to_text_bindings.jsonl"
LEXICAL_RANKS = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/native_description_lexical_top12.jsonl"
BGE_RANKS = NC_ROOT / "review/source_native_local_bge_embedding_2026-09-04/native_description_local_bge_top12.jsonl"
BGE_SUMMARY = NC_ROOT / "review/source_native_local_bge_embedding_2026-09-04/summary.json"
B001_QUEUE = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_queue_internal.jsonl"
B002_QUEUE = NC_ROOT / "review/source_native_lexical_continuation_2026-09-04/batch_002_full_source_review_queue_internal.jsonl"
OUTPUT_DIR = NC_ROOT / "review/source_native_dense_lexical_union_b003_2026-09-04"

TOP_NEIGHBOURS = 12
BATCH_FAMILIES = 25
ROUTE_LEXICAL = "LEXICAL_ONLY_BOOTSTRAP_EXACT_NATIVE_DESCRIPTION"
ROUTE_BGE = "LOCAL_BGE_EXACT_NATIVE_DESCRIPTION"
SOURCE_READING_QUEUE_FILENAME = re.compile(r"^batch_\d{3}_full_source_review_queue_internal\.jsonl$")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def require_top12_rank_rows(rows: list[dict[str, Any]], route: str) -> dict[tuple[str, str], int]:
    ranks: dict[tuple[str, str], int] = {}
    by_seed: defaultdict[str, list[int]] = defaultdict(list)
    for row in rows:
        if row.get("discovery_route") != route:
            raise SystemExit(f"Unexpected discovery route in frozen rank input: {row.get('discovery_route')}")
        seed = str(row.get("seed_source_sha256"))
        neighbour = str(row.get("neighbour_source_sha256"))
        rank = row.get("rank")
        if len(seed) != 64 or len(neighbour) != 64 or seed == neighbour or not isinstance(rank, int) or not 1 <= rank <= TOP_NEIGHBOURS:
            raise SystemExit("Malformed frozen source-native rank row")
        key = (seed, neighbour)
        if key in ranks:
            raise SystemExit("Duplicate directed neighbour in frozen rank input")
        ranks[key] = rank
        by_seed[seed].append(rank)
    if not ranks or any(sorted(values) != list(range(1, len(values) + 1)) for values in by_seed.values()):
        raise SystemExit("Frozen rank rows are not contiguous per seed")
    return ranks


def prior_source_hashes(path: Path, expected_families: int) -> set[str]:
    rows = read_jsonl(path)
    if len(rows) != expected_families:
        raise SystemExit(f"Expected exactly {expected_families} families in prior queue: {path}")
    sources = [str(source) for row in rows for source in row.get("member_source_sha256", [])]
    if len(sources) != expected_families * 3 or len(set(sources)) != len(sources):
        raise SystemExit(f"Prior queue does not bind {expected_families * 3} distinct sources: {path}")
    return set(sources)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise a source-native dense-plus-lexical union reading queue.")
    parser.add_argument("--batch-label", default="B003")
    parser.add_argument("--batch-id", default="SN-UNION-B003")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--queue-filename", default="batch_003_full_source_review_queue_internal.jsonl")
    parser.add_argument("--design", type=Path, default=DESIGN)
    parser.add_argument("--prior-queues", type=Path, nargs="+", default=[B001_QUEUE, B002_QUEUE])
    parser.add_argument("--expected-families-per-prior-queue", type=int, default=BATCH_FAMILIES)
    parser.add_argument("--batch-families", type=int, default=BATCH_FAMILIES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.batch_label.strip() or not args.batch_id.strip() or not args.queue_filename.strip():
        raise SystemExit("Batch label, batch id and queue filename must be non-empty")
    if args.expected_families_per_prior_queue < 1 or args.batch_families < 1:
        raise SystemExit("Expected and batch family counts must be positive")
    output_dir = args.output_dir.resolve()
    design_path = args.design.resolve()
    prior_queue_paths = [path.resolve() for path in args.prior_queues]
    if len(prior_queue_paths) != len(set(prior_queue_paths)):
        raise SystemExit("Prior reviewed queues must be unique")
    if any(not SOURCE_READING_QUEUE_FILENAME.fullmatch(path.name) for path in prior_queue_paths):
        raise SystemExit("Prior reviewed queues must be explicit source-reading queue artifacts")
    required = [PROTOCOL, design_path, DESCRIPTION_BINDINGS, LEXICAL_RANKS, BGE_RANKS, BGE_SUMMARY, *prior_queue_paths]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing frozen source-native union input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")

    bge_summary = json.loads(BGE_SUMMARY.read_text(encoding="utf-8"))
    if bge_summary.get("status") != "PASS_SOURCE_NATIVE_LOCAL_BGE_EXACT_DESCRIPTION_DENSE_INDEX_NO_SEMANTIC_CLUSTER_DECISION":
        raise SystemExit("BGE rank input does not have the required frozen local-index status")

    bindings = read_jsonl(DESCRIPTION_BINDINGS)
    source_to_description = {str(row["canonical_source_sha256"]): str(row["native_description_sha256"]) for row in bindings}
    if len(bindings) != 23_431 or len(source_to_description) != 23_431:
        raise SystemExit("Expected 23,431 unique source-to-native-description bindings")

    lexical = require_top12_rank_rows(read_jsonl(LEXICAL_RANKS), ROUTE_LEXICAL)
    bge = require_top12_rank_rows(read_jsonl(BGE_RANKS), ROUTE_BGE)
    bge_seeds = {seed for seed, _neighbour in bge}
    if bge_seeds != set(source_to_description):
        raise SystemExit("Local BGE ranks do not cover the frozen source-native population")
    if any(seed not in source_to_description or neighbour not in source_to_description for seed, neighbour in set(lexical) | set(bge)):
        raise SystemExit("Rank source absent from frozen native-description bindings")

    prior_source_sets = [prior_source_hashes(path, args.expected_families_per_prior_queue) for path in prior_queue_paths]
    excluded = set().union(*prior_source_sets)
    expected_excluded = len(prior_source_sets) * args.expected_families_per_prior_queue * 3
    if len(excluded) != expected_excluded:
        raise SystemExit("Prior reviewed-source queues are not pairwise source-disjoint")

    route_ranks: defaultdict[tuple[str, str], dict[str, int]] = defaultdict(dict)
    for route, rows in ((ROUTE_LEXICAL, lexical), (ROUTE_BGE, bge)):
        for pair, rank in rows.items():
            route_ranks[pair][route] = rank

    eligible = set(source_to_description) - excluded
    outgoing: defaultdict[str, set[str]] = defaultdict(set)
    for (seed, neighbour), _route_values in route_ranks.items():
        if seed in eligible and neighbour in eligible:
            outgoing[seed].add(neighbour)
    reciprocal: defaultdict[str, set[str]] = defaultdict(set)
    for seed, neighbours in outgoing.items():
        for neighbour in neighbours:
            if seed in outgoing[neighbour]:
                reciprocal[seed].add(neighbour)

    hypotheses: list[dict[str, Any]] = []
    observed: set[tuple[str, str, str]] = set()
    excluded_same_description = 0
    for left in sorted(eligible):
        for middle, right in combinations(sorted(reciprocal[left]), 2):
            members = tuple(sorted((left, middle, right)))
            if members in observed:
                continue
            observed.add(members)
            if middle not in reciprocal[right]:
                continue
            description_hashes = [source_to_description[source] for source in members]
            if len(set(description_hashes)) != 3:
                excluded_same_description += 1
                continue
            directed_route_ranks = []
            fusion = 0.0
            for source in members:
                for neighbour in members:
                    if source == neighbour:
                        continue
                    route_values = route_ranks.get((source, neighbour), {})
                    if not route_values:
                        raise SystemExit("Reciprocal triad lacks a directed frozen rank")
                    contributions = []
                    for route, rank in sorted(route_values.items()):
                        contribution = 1.0 / (60.0 + rank)
                        fusion += contribution
                        contributions.append({"route": route, "rank": rank, "contribution": contribution})
                    directed_route_ranks.append({"from_source_sha256": source, "to_source_sha256": neighbour, "route_ranks": contributions})
            hypotheses.append({
                "record_type": "source_native_dense_lexical_union_family_hypothesis",
                "family_id": "SN-UNION-" + hashlib.sha256("|".join(members).encode("utf-8")).hexdigest()[:16],
                "member_source_sha256": list(members),
                "member_native_description_sha256": description_hashes,
                "reciprocal_link_count": 3,
                "directed_route_ranks": directed_route_ranks,
                "rank_fusion_score": fusion,
                "discovery_route": "FROZEN_LOCAL_BGE_PLUS_FROZEN_LEXICAL_EXACT_NATIVE_DESCRIPTION",
                "review_state": "UNREVIEWED_FULL_SOURCE",
                "claim_boundary": "Mechanical source-reading hypothesis only; full original sources must establish envelope, independence and contrast.",
            })

    hypotheses.sort(key=lambda row: (-int(row["reciprocal_link_count"]), -float(row["rank_fusion_score"]), row["member_source_sha256"]))
    queue: list[dict[str, Any]] = []
    selected_sources: set[str] = set()
    excluded_source_collision = 0
    for hypothesis in hypotheses:
        members = set(str(value) for value in hypothesis["member_source_sha256"])
        if members & selected_sources:
            excluded_source_collision += 1
            continue
        queue.append({
            **hypothesis,
            "batch_id": args.batch_id,
            "batch_rank": len(queue) + 1,
            "claim_boundary": "Unread source-reading queue only; full-source A/B review remains mandatory before any family, prompt or later audit eligibility claim.",
        })
        selected_sources.update(members)
        if len(queue) == args.batch_families:
            break
    if len(queue) != args.batch_families or len(selected_sources) != args.batch_families * 3:
        raise SystemExit("Could not materialise the requested number of disjoint unread hypotheses")

    output_dir.mkdir(parents=True)
    hypotheses_path = output_dir / "all_union_mutual_triangle_hypotheses.jsonl"
    queue_path = output_dir / args.queue_filename
    write_jsonl(hypotheses_path, hypotheses)
    write_jsonl(queue_path, queue)
    route_contributions = Counter(
        contribution["route"]
        for hypothesis in hypotheses
        for edge in hypothesis["directed_route_ranks"]
        for contribution in edge["route_ranks"]
    )
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_FROZEN_LOCAL_BGE_LEXICAL_UNION_UNREVIEWED_FAMILY_HYPOTHESES",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "parameters": {
            "candidate_routes": [ROUTE_LEXICAL, ROUTE_BGE],
            "top_neighbours_per_route": TOP_NEIGHBOURS,
            "rank_fusion": "sum(1/(60+rank)) over route-specific directed triad edges",
            "fresh_source_policy": "exclude_every_source_hash_in_the_explicit_prior_reviewed_queues; disjoint_members_within_current_batch",
            "batch_families": args.batch_families,
        },
        "counts": {
            "source_native_population": len(source_to_description),
            "prior_reviewed_queues": len(prior_queue_paths),
            "prior_reviewed_hashes_by_queue": {relative(path): len(source_set) for path, source_set in zip(prior_queue_paths, prior_source_sets)},
            "total_excluded_reviewed_hashes": len(excluded),
            "eligible_unread_sources": len(eligible),
            "union_mutual_triangles_before_batch_cap": len(hypotheses),
            "triangles_excluded_same_native_description": excluded_same_description,
            "current_batch_source_collision_skips": excluded_source_collision,
            "current_batch_families": len(queue),
            "current_batch_sources": len(selected_sources),
            "route_contributions_across_all_hypotheses": dict(sorted(route_contributions.items())),
        },
        "outputs": {
            "all_union_mutual_triangle_hypotheses.jsonl": sha256_file(hypotheses_path),
            args.queue_filename: sha256_file(queue_path),
        },
        "claim_boundary": "A frozen-rank source-reading queue only. No full-source review, confusable-cluster decision, provenance decision, prompt, acceptable-set result, coverage claim, admission, selector result or metric has occurred.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
