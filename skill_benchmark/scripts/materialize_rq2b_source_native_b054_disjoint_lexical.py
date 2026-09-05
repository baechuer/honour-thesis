#!/usr/bin/env python3
"""Materialise a source-disjoint, description-only B054 discovery queue.

This is deliberately a discovery controller, not a semantic-family judgement.
It selects fresh reciprocal lexical triads with a non-generic shared lexical
anchor, then defers every triad to independent full-source review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
SOP = NC_ROOT / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
CORPUS = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
HYPOTHESES = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/all_mutual_triangle_hypotheses.jsonl"
PHASE0 = NC_ROOT / "review/rq2b_nc_phase0_state_reconciliation_2026-09-05_v2"
PHASE0_SUMMARY = PHASE0 / "summary.json"
PHASE0_SOURCE_UNION = PHASE0 / "phase0_source_native_inspection_union.jsonl"
OUTPUT = NC_ROOT / "review/source_native_remaining_pool_disjoint_lexical_b054_2026-09-05"

GENERIC_TERMS = {
    "about", "agent", "agents", "also", "and", "are", "assistant", "best", "can", "create",
    "for", "from", "help", "how", "into", "more", "not", "of", "on", "or", "skill", "skills",
    "that", "the", "their", "this", "to", "use", "used", "using", "with", "you", "your",
    "when", "where", "will", "work", "workflow", "tasks", "task", "support", "provide",
    "generate", "make", "build", "design", "manage", "analysis", "data", "content", "project",
    "user", "users", "ask", "asks", "asked", "what", "says", "need", "needs", "first",
    "application", "applications", "review", "reviews", "prepare", "plan", "plans",
}
DOMAIN_TERMS = {
    "android", "api", "browser", "cloud", "database", "deployment", "desktop", "docker", "endpoint",
    "flutter", "frontend", "ios", "javascript", "kernel", "kubernetes", "logs", "mobile", "monitoring",
    "numpy", "pytorch", "python", "react", "restful", "security", "server", "swift", "tablet", "web",
}
LOW_CUE_WORKFLOW_TERMS = {
    "accounting", "advertising", "assessment", "brand", "budget", "campaign", "candidate", "client",
    "contract", "course", "customer", "education", "finance", "hiring", "interview", "job", "learning",
    "marketing", "meeting", "onboarding", "presentation", "proposal", "resume", "sales", "social", "strategy",
    "training",
}
HIGH_CUE_TECHNICAL_TERMS = {
    "android", "api", "browser", "cloud", "database", "deployment", "docker", "flutter", "frontend", "ios",
    "html", "http", "javascript", "json", "kubernetes", "mobile", "node", "numpy", "openapi", "python",
    "fine-tuning", "lora", "pytorch", "qlora", "rate-limit-handler", "rate_limit_handler", "react",
    "regression", "server", "swift", "web",
}
ANCHOR_SETS = {"technical": DOMAIN_TERMS, "low_cue_workflow": LOW_CUE_WORKFLOW_TERMS}
TOKEN = re.compile(r"[a-z][a-z0-9_-]{3,}", re.I)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def content_terms(text: str) -> set[str]:
    return {term.lower() for term in TOKEN.findall(text) if term.lower() not in GENERIC_TERMS}


def sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    paths = row.get("member_source_paths", [])
    distinct_path_count = len({path for member in paths for path in member})
    return (
        -int(row["reciprocal_link_count"]),
        -float(row["rank_fusion_score"]),
        -distinct_path_count,
        tuple(str(value) for value in row["member_source_sha256"]),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise B054 source-disjoint lexical discovery triads.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--expected-families", type=int, default=25)
    parser.add_argument("--batch-label", default="B054")
    parser.add_argument("--minimum-domain-anchors", type=int, default=2)
    parser.add_argument("--anchor-set", choices=sorted(ANCHOR_SETS), default="technical")
    parser.add_argument("--exclude-high-cue-technical-terms", action="store_true")
    parser.add_argument(
        "--additional-source-exclusion-queue",
        action="append",
        type=Path,
        default=[],
        help="A prior source-disjoint discovery queue whose three-member hashes must also be excluded. Repeatable.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    if args.minimum_domain_anchors < 0:
        raise SystemExit("--minimum-domain-anchors cannot be negative")
    anchor_set = ANCHOR_SETS[args.anchor_set]
    output = args.output_dir.resolve()
    if output.exists() and not args.dry_run:
        raise SystemExit(f"refusing to overwrite an existing output directory: {output}")
    additional_queues = [path.resolve() for path in args.additional_source_exclusion_queue]
    required = [SOP, CORPUS, HYPOTHESES, PHASE0_SUMMARY, PHASE0_SOURCE_UNION, *additional_queues]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"missing required immutable input(s): {missing}")
    phase0 = json.loads(PHASE0_SUMMARY.read_text(encoding="utf-8"))
    if phase0.get("status") != "PASS_RQ2B_NC_PHASE0_CANONICAL_STATE_RECONCILIATION_NO_EXPERIMENT":
        raise SystemExit("B054 requires a passing Phase 0 state reconciliation")
    phase0_sources = {str(row["canonical_source_sha256"]) for row in read_jsonl(PHASE0_SOURCE_UNION)}
    if len(phase0_sources) != 3922:
        raise SystemExit(f"Phase 0 inspection source-union mismatch: {len(phase0_sources)}")
    additional_sources: set[str] = set()
    additional_queue_hashes: dict[str, str] = {}
    for queue in additional_queues:
        queue_rows = read_jsonl(queue)
        queue_sources = {str(source_hash) for row in queue_rows for source_hash in row.get("member_source_sha256", [])}
        if not queue_rows or len(queue_sources) != len(queue_rows) * 3:
            raise SystemExit(f"additional exclusion queue is not source-disjoint triads: {queue}")
        if queue_sources & phase0_sources or queue_sources & additional_sources:
            raise SystemExit(f"additional exclusion queue overlaps an earlier source universe: {queue}")
        additional_sources.update(queue_sources)
        additional_queue_hashes[str(queue.relative_to(WORKSPACE))] = sha256_file(queue)
    historical_sources = phase0_sources | additional_sources
    corpus = {str(row["canonical_source_sha256"]): row for row in read_jsonl(CORPUS)}
    hypotheses = read_jsonl(HYPOTHESES)
    if len(corpus) != 23450 or len(hypotheses) != 49823:
        raise SystemExit("frozen corpus/hypothesis cardinality mismatch")
    hypotheses.sort(key=sort_key)

    used: set[str] = set()
    selected: list[dict[str, Any]] = []
    rejections: Counter[str] = Counter()
    anchor_counts: Counter[str] = Counter()
    for hypothesis in hypotheses:
        source_hashes = [str(value) for value in hypothesis["member_source_sha256"]]
        if len(source_hashes) != 3 or len(set(source_hashes)) != 3:
            raise SystemExit(f"malformed frozen triad: {hypothesis.get('family_id')}")
        if any(source_hash not in corpus for source_hash in source_hashes):
            raise SystemExit(f"corpus binding missing: {hypothesis.get('family_id')}")
        members = set(source_hashes)
        if members & historical_sources:
            rejections["REJECT_B001_B053_INSPECTION_SOURCE_OVERLAP"] += 1
            continue
        if members & used:
            rejections["REJECT_WITHIN_B054_SOURCE_COLLISION"] += 1
            continue
        descriptions = [str(corpus[source_hash]["native_description"]) for source_hash in source_hashes]
        anchors = sorted(set.intersection(*(content_terms(description) for description in descriptions)))
        domain_anchors = sorted(set(anchors) & anchor_set)
        if len(anchors) < 2:
            rejections["REJECT_FEWER_THAN_TWO_NON_GENERIC_SHARED_DESCRIPTION_TERMS"] += 1
            continue
        if len(domain_anchors) < args.minimum_domain_anchors:
            rejections[f"REJECT_FEWER_THAN_{args.minimum_domain_anchors}_DECLARED_DOMAIN_ANCHORS"] += 1
            continue
        member_terms = set().union(*(content_terms(description) for description in descriptions))
        if args.exclude_high_cue_technical_terms and member_terms & HIGH_CUE_TECHNICAL_TERMS:
            rejections["REJECT_HIGH_CUE_TECHNICAL_DESCRIPTION_TERM"] += 1
            continue
        selected.append({
            **hypothesis,
            "batch_id": f"SN-SEM-{args.batch_label}",
            "batch_rank": len(selected) + 1,
            "discovery_route": "LEXICAL_RECIPROCAL_TRIANGLE_EXACT_NATIVE_DESCRIPTION_TWO_NON_GENERIC_SHARED_TERM_GATE",
            "selection_scope": f"REMAINING_FROZEN_SOURCE_NATIVE_POOL_SOURCE_DISJOINT_LEXICAL_NATURAL_FIRST_ROUTE_HYPOTHESES_MINIMUM_{args.minimum_domain_anchors}_DECLARED_DOMAIN_ANCHORS",
            "source_native_shared_anchor_terms": anchors,
            "source_native_declared_domain_anchors": domain_anchors,
            "source_native_anchor_set": args.anchor_set,
            "native_description_first_route_hypothesis": " | ".join(" ".join(text.split())[:180] for text in descriptions),
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "packet_state": "NOT_MATERIALISED_DISCOVERY_QUEUE_ONLY",
            "claim_boundary": "Description-only lexical reciprocal and shared-anchor hypothesis; no full-source semantic-family, independent-first-route, operational-contrast, provenance, prompt, admission, selector, or metric decision.",
        })
        used.update(members)
        anchor_counts.update(anchors)
        if len(selected) == args.expected_families:
            break
    result = {
        "batch_id": f"SN-SEM-{args.batch_label}",
        "selected_families": len(selected),
        "selected_member_occurrences": len(selected) * 3,
        "selected_unique_sources": len(used),
        "source_overlap_vs_all_bound_prior_sources": len(used & historical_sources),
        "selection_rejection_counts_before_completion": dict(sorted(rejections.items())),
        "shared_anchor_term_frequency": dict(sorted(anchor_counts.items())),
    }
    if len(selected) != args.expected_families or len(used) != args.expected_families * 3 or used & historical_sources:
        raise SystemExit(f"B054 selection failure: {json.dumps(result, sort_keys=True)}")
    if args.dry_run:
        print(json.dumps({
            **result,
            "selected_family_anchor_preview": [
                {"family_id": row["family_id"], "anchors": row["source_native_shared_anchor_terms"]}
                for row in selected
            ],
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    output.mkdir(parents=True)
    queue_path = output / f"{args.batch_label.lower()}_source_native_semantic_family_queue.jsonl"
    defer_path = output / "discovery_defer_ledger.jsonl"
    replay_path = output / "source_provenance_byte_replay_ledger.jsonl"
    exclusion_path = output / "historical_source_exclusion_manifest.json"
    write_jsonl(queue_path, selected)
    defers: list[dict[str, Any]] = []
    replays: list[dict[str, Any]] = []
    for family in selected:
        source_hashes = [str(value) for value in family["member_source_sha256"]]
        defers.append({
            "record_type": "discovery_defer",
            "batch_id": family["batch_id"],
            "batch_rank": family["batch_rank"],
            "family_id": family["family_id"],
            "member_source_sha256": source_hashes,
            "disposition": "DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED",
            "reason": "Lexical reciprocal and literal description anchors cannot establish a bounded shared envelope, independent first routes, operational contrast, provenance/licence sufficiency, or promptability; independent full-source A/B review is required.",
        })
        for source_hash, description_hash, paths in zip(
            source_hashes, family["member_native_description_sha256"], family["member_source_paths"]
        ):
            record = corpus[source_hash]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != paths:
                raise SystemExit(f"frozen corpus binding mismatch: {source_hash}")
            replayed = [sha256_file(WORKSPACE / path) for path in paths]
            if any(value != source_hash for value in replayed):
                raise SystemExit(f"complete-source byte replay failed: {source_hash}")
            replays.append({
                "record_type": "source_provenance_and_byte_replay",
                "family_id": family["family_id"],
                "batch_rank": family["batch_rank"],
                "canonical_source_sha256": source_hash,
                "source_paths": paths,
                "replayed_path_sha256": replayed,
                "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                "native_description_sha256": description_hash,
                "native_description_origin": record["native_description_origin"],
                "native_description_literal_replay_status": record["native_description_replay_status"],
                "claim_boundary": "Frozen path/hash replay and provenance pointer only; not a source/provenance assessment or downstream decision.",
            })
    if len(replays) != args.expected_families * 3 or len({row["canonical_source_sha256"] for row in replays}) != len(replays):
        raise SystemExit("B054 source replay cardinality/disjointness failure")
    write_jsonl(defer_path, defers)
    write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))
    exclusion = {
        "record_type": f"{args.batch_label}_historical_source_exclusion_manifest",
        "claim_boundary": "Hash-membership exclusion only; it establishes no semantic or review outcome.",
        "phase0_status": phase0["status"],
        "phase0_source_union": str(PHASE0_SOURCE_UNION.relative_to(WORKSPACE)),
        "phase0_source_union_sha256": sha256_file(PHASE0_SOURCE_UNION),
        "B001_B053_inspection_unique_source_hashes": len(phase0_sources),
        "additional_discovery_exclusion_unique_source_hashes": len(additional_sources),
        "total_prior_source_exclusion_unique_source_hashes": len(historical_sources),
        "additional_discovery_queue_sha256": additional_queue_hashes,
        "selected_batch_unique_source_hashes": len(used),
        "intersection_selected_batch_vs_all_bound_prior_sources": len(used & historical_sources),
    }
    write_json(exclusion_path, exclusion)
    summary = {
        "batch_id": f"SN-SEM-{args.batch_label}",
        "status": f"PASS_{args.batch_label}_DISCOVERY_QUEUE_ONLY_UNREVIEWED",
        "claim_boundary": "Discovery queue only; not full-source review, provenance/licence outcome, prompt, target assessment, admission, acceptable-set audit, selector result, or metric.",
        "bound_inputs": {
            "master_pre_experiment_sop": sha256_file(SOP),
            "source_native_description_corpus": sha256_file(CORPUS),
            "frozen_lexical_mutual_triangle_hypotheses": sha256_file(HYPOTHESES),
            "phase0_summary": sha256_file(PHASE0_SUMMARY),
            "additional_discovery_exclusion_queues": additional_queue_hashes,
            "historical_source_exclusion_manifest": sha256_file(exclusion_path),
        },
        "method": {
            "route": "LEXICAL_RECIPROCAL_TRIANGLE_EXACT_NATIVE_DESCRIPTION_TWO_NON_GENERIC_SHARED_TERM_GATE",
            "selection_input_boundary": "Only frozen literal native descriptions, frozen reciprocal-triangle fields, the Phase 0 B001-B053 hash-membership union, and any bound earlier discovery queue source hashes; never source bodies, titles, headings, paths, provenance outcomes, prompts, labels, review outcomes, or cluster membership.",
            "base_hypothesis_order": "reciprocal-link descending, rank-fusion descending, distinct source-path count descending, then ordered source hashes; retain first source-disjoint triads after fixed gates.",
            "source_disjointness_policy": "Exclude all B001-B053 inspection sources and any bound earlier discovery queues; require exactly three distinct sources per family and no source reuse within this batch.",
            "semantic_intent_boundary": "At least two non-generic shared terms, plus the declared minimum count of domain anchors, and reciprocal lexical links prioritise potentially confusable first routes for later source reading. They are not semantic truth or a review result.",
            "generic_term_set": sorted(GENERIC_TERMS),
            "declared_anchor_set_name": args.anchor_set,
            "declared_domain_anchor_set": sorted(anchor_set),
            "minimum_declared_domain_anchor_count": args.minimum_domain_anchors,
            "high_cue_technical_term_exclusion": sorted(HIGH_CUE_TECHNICAL_TERMS) if args.exclude_high_cue_technical_terms else None,
        },
        "counts": {**result, "frozen_corpus_sources": len(corpus), "frozen_reciprocal_hypotheses": len(hypotheses), "deferred_families": len(defers), "source_byte_replays": len(replays)},
        "outputs": {},
        "verification": {
            "source_disjointness_vs_all_bound_prior_sources": "PASS",
            "within_selected_batch_source_disjointness": "PASS",
            "original_source_byte_replay": f"PASS_{len(replays)}_OF_{len(replays)}",
            "all_selected_families_deferred_pending_independent_full_source_review": f"PASS_{len(defers)}_OF_{len(defers)}",
        },
        "limitations": [
            "The lexical reciprocal and shared-anchor gate is a deterministic reading-priority rule, not a semantic-family finding or retrieval metric.",
            "No complete original source was substantively reviewed here; byte replay preserves identity only.",
            "Every selected family remains deferred until independent full-source A/B review and downstream local gates close.",
        ],
    }
    dossier_path = output / f"{args.batch_label}_DISCOVERY_DOSSIER_2026-09-05.md"
    dossier_path.write_text(
        "\n".join([
            f"# {args.batch_label} source-native disjoint lexical discovery",
            "",
            "Status: **DISCOVERY QUEUE ONLY / UNREAD FULL ORIGINAL SOURCES / NO REVIEW OR ADMISSION**",
            "",
            f"The queue selects fresh frozen reciprocal lexical triads only when all three literal native descriptions share at least two non-generic terms, including at least {args.minimum_domain_anchors} declared technical or workflow-domain anchor(s). It excludes every bound prior source and prevents reuse within this batch. This is a deterministic priority rule for independent readers, not proof that the triad is a naturalistic semantic-confusability family.",
            "",
            f"The batch contains {len(selected)} triads and {len(used)} source-disjoint original skills. Every source byte replay passed; all triads are deferred to independent full-source A/B review. No prompt, adequate alternative, final-library entry, selector output, retrieval result, or metric was created.",
            "",
        ]),
        encoding="utf-8",
    )
    summary["outputs"] = {
        queue_path.name: sha256_file(queue_path),
        defer_path.name: sha256_file(defer_path),
        replay_path.name: sha256_file(replay_path),
        exclusion_path.name: sha256_file(exclusion_path),
        dossier_path.name: sha256_file(dossier_path),
    }
    summary_path = output / "summary.json"
    write_json(summary_path, summary)
    print(json.dumps({"output": str(output.relative_to(WORKSPACE)), "counts": summary["counts"], "outputs": summary["outputs"]}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
