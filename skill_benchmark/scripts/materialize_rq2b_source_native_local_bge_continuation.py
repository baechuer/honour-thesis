#!/usr/bin/env python3
"""Materialise an outcome-blind, source-disjoint local-BGE discovery queue.

The local BGE run has already happened.  This controller only verifies and
replays its frozen description-only hypotheses; it neither loads a model nor
reads a network/runtime result.  It is deliberately not a semantic, prompt,
admission, retrieval, or metric controller.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
CORPUS = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
BGE_DIR = NC_ROOT / "review/source_native_local_bge_embedding_2026-09-04"
BGE_SUMMARY = BGE_DIR / "summary.json"
BGE_HYPOTHESES = BGE_DIR / "all_mutual_triangle_hypotheses.jsonl"
PHASE0_DIR = NC_ROOT / "review/rq2b_nc_phase0_state_reconciliation_2026-09-05_v2"
PHASE0_SUMMARY = PHASE0_DIR / "summary.json"
PHASE0_INSPECTION_UNION = PHASE0_DIR / "phase0_source_native_inspection_union.jsonl"
DEFAULT_OUTPUT = NC_ROOT / "review/source_native_local_bge_continuation_b067_2026-09-05"

# These fixed hashes bind the controller to the already-completed local CPU
# run and frozen corpus rather than merely accepting a same-shaped substitute.
BGE_SUMMARY_SHA256 = "6102048b16c4879bc8014f696c9fcceebf5cf058d607ac1137a00e2c5e42a23c"
BGE_HYPOTHESES_SHA256 = "3ace910b601799986f255b1915c2f52b01aa886c119a8b0fb5a86b7d5cd3d586"
CORPUS_SHA256 = "62a15f2291ade239ff2c85b361e2259579cecad4ae33fd773352a6da39dd3b56"

BGE_STATUS = "PASS_SOURCE_NATIVE_LOCAL_BGE_EXACT_DESCRIPTION_DENSE_INDEX_NO_SEMANTIC_CLUSTER_DECISION"
PHASE0_STATUS = "PASS_RQ2B_NC_PHASE0_CANONICAL_STATE_RECONCILIATION_NO_EXPERIMENT"
BGE_COUNTS = {
    "source_bindings": 23_431,
    "unique_native_descriptions": 22_765,
    "directed_top12_edges": 281_172,
    "mutual_triangles": 49_646,
}


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


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError:
        return str(path)


def hypothesis_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    """The fixed, source-only priority order: rank fusion then source hashes."""
    return (-float(row["rank_fusion_score"]), tuple(str(value) for value in row["member_source_sha256"]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialise a source-disjoint continuation queue from the frozen local-BGE mutual triangles."
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--batch-label", default="B067")
    parser.add_argument("--expected-families", type=int, default=25)
    parser.add_argument(
        "--additional-source-exclusion-queue",
        action="append",
        default=[],
        type=Path,
        help="Repeatable prior discovery queue. Every listed member source hash is excluded.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and select, but write no output.")
    return parser.parse_args()


def require_file_inputs(paths: list[Path]) -> None:
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(f"missing required immutable input(s): {missing}")


def validate_bge_artifacts() -> dict[str, Any]:
    if sha256_file(BGE_SUMMARY) != BGE_SUMMARY_SHA256:
        raise SystemExit("local BGE summary SHA-256 differs from the hash-bound completed run")
    if sha256_file(BGE_HYPOTHESES) != BGE_HYPOTHESES_SHA256:
        raise SystemExit("local BGE mutual-triangle SHA-256 differs from the hash-bound completed run")
    summary = json.loads(BGE_SUMMARY.read_text(encoding="utf-8"))
    if summary.get("status") != BGE_STATUS:
        raise SystemExit("local BGE summary status is not the required completed description-only status")
    if summary.get("counts") != BGE_COUNTS:
        raise SystemExit("local BGE summary counts differ from the completed hash-bound run")
    if summary.get("outputs", {}).get(BGE_HYPOTHESES.name) != BGE_HYPOTHESES_SHA256:
        raise SystemExit("local BGE summary does not bind the mutual-triangle hypothesis hash")
    if summary.get("model", {}).get("device") != "cpu" or summary.get("model", {}).get("model_id") != "BAAI/bge-small-en-v1.5":
        raise SystemExit("local BGE summary does not bind the required local CPU BGE route")
    return summary


def validate_phase0() -> tuple[dict[str, Any], set[str]]:
    summary = json.loads(PHASE0_SUMMARY.read_text(encoding="utf-8"))
    if summary.get("status") != PHASE0_STATUS:
        raise SystemExit("Phase 0 v2 is not in the required passing canonical state")
    if summary.get("counts", {}).get("source_native_inspection_exact_hash_unique") != 3_922:
        raise SystemExit("Phase 0 v2 inspection-union count differs from 3,922")
    union_hash = sha256_file(PHASE0_INSPECTION_UNION)
    if summary.get("outputs", {}).get(PHASE0_INSPECTION_UNION.name) != union_hash:
        raise SystemExit("Phase 0 v2 summary does not bind its inspection-union hash")
    rows = read_jsonl(PHASE0_INSPECTION_UNION)
    sources = {str(row.get("canonical_source_sha256")) for row in rows}
    if len(rows) != 3_922 or len(sources) != 3_922 or "None" in sources:
        raise SystemExit("Phase 0 v2 inspection union is not an exact 3,922-source set")
    return summary, sources


def additional_exclusions(paths: list[Path]) -> tuple[set[str], dict[str, dict[str, Any]]]:
    excluded: set[str] = set()
    manifests: dict[str, dict[str, Any]] = {}
    for path in paths:
        rows = read_jsonl(path)
        queue_sources: set[str] = set()
        for row in rows:
            members = row.get("member_source_sha256")
            if not isinstance(members, list) or len(members) != 3 or len({str(value) for value in members}) != 3:
                raise SystemExit(f"additional exclusion queue is not a three-distinct-source queue: {path}")
            queue_sources.update(str(value) for value in members)
        if not rows:
            raise SystemExit(f"additional exclusion queue is empty: {path}")
        manifests[relative(path)] = {
            "sha256": sha256_file(path),
            "family_records": len(rows),
            "unique_member_source_hashes": len(queue_sources),
        }
        excluded.update(queue_sources)
    return excluded, manifests


def validate_hypothesis(row: dict[str, Any], corpus: dict[str, dict[str, Any]]) -> tuple[list[str], list[str]]:
    sources = [str(value) for value in row.get("member_source_sha256", [])]
    descriptions = [str(value) for value in row.get("member_native_description_sha256", [])]
    ranks = row.get("mutual_directional_ranks")
    if len(sources) != 3 or len(set(sources)) != 3 or sources != sorted(sources):
        raise SystemExit(f"malformed BGE source triad: {row.get('family_id')}")
    if len(descriptions) != 3 or len(ranks) != 6 or not all(isinstance(rank, int) and 1 <= rank <= 12 for rank in ranks):
        raise SystemExit(f"malformed BGE rank/description binding: {row.get('family_id')}")
    if row.get("record_type") != "source_native_confusable_family_hypothesis" or row.get("discovery_route") != "LOCAL_BGE_EXACT_NATIVE_DESCRIPTION":
        raise SystemExit(f"unexpected BGE hypothesis route: {row.get('family_id')}")
    fusion = row.get("rank_fusion_score")
    if not isinstance(fusion, (int, float)) or not math.isfinite(float(fusion)) or float(fusion) <= 0:
        raise SystemExit(f"malformed BGE rank-fusion score: {row.get('family_id')}")
    for source, description_hash in zip(sources, descriptions):
        record = corpus.get(source)
        if record is None or record.get("index_eligibility") is not True:
            raise SystemExit(f"BGE source is not bound to the frozen eligible description corpus: {source}")
        if record.get("native_description_sha256") != description_hash:
            raise SystemExit(f"BGE description hash differs from frozen corpus: {source}")
    return sources, descriptions


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    if not args.batch_label or not args.batch_label.replace("-", "").isalnum():
        raise SystemExit("--batch-label must be non-empty alphanumeric text (hyphens permitted)")
    output = args.output_dir.resolve()
    if output.exists() and not args.dry_run:
        raise SystemExit(f"refusing to overwrite an existing output directory: {output}")

    additional_paths = [path.resolve() for path in args.additional_source_exclusion_queue]
    require_file_inputs([CORPUS, BGE_SUMMARY, BGE_HYPOTHESES, PHASE0_SUMMARY, PHASE0_INSPECTION_UNION, *additional_paths])
    if sha256_file(CORPUS) != CORPUS_SHA256:
        raise SystemExit("frozen native description corpus SHA-256 differs from its bound value")
    bge_summary = validate_bge_artifacts()
    phase0_summary, phase0_sources = validate_phase0()
    corpus_rows = read_jsonl(CORPUS)
    corpus = {str(row.get("canonical_source_sha256")): row for row in corpus_rows}
    if len(corpus_rows) != 23_450 or len(corpus) != 23_450:
        raise SystemExit("frozen native description corpus cardinality differs from 23,450")
    if sum(row.get("index_eligibility") is True for row in corpus_rows) != 23_431:
        raise SystemExit("frozen native description corpus eligible cardinality differs from 23,431")
    hypotheses = read_jsonl(BGE_HYPOTHESES)
    if len(hypotheses) != BGE_COUNTS["mutual_triangles"]:
        raise SystemExit("BGE mutual-triangle hypothesis cardinality differs from its summary")
    additional_sources, additional_manifest = additional_exclusions(additional_paths)
    excluded_sources = phase0_sources | additional_sources

    # No corpus-content feature, anchor, high-cue, outcome, prompt, review, or
    # family-validity gate is permitted here.  This rank order is the full
    # selection rule after source identity exclusions.
    hypotheses.sort(key=hypothesis_sort_key)
    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    rejected: Counter[str] = Counter()
    for hypothesis in hypotheses:
        sources, description_hashes = validate_hypothesis(hypothesis, corpus)
        members = set(sources)
        if members & phase0_sources:
            rejected["REJECT_PHASE0_V2_INSPECTION_SOURCE_OVERLAP"] += 1
            continue
        if members & additional_sources:
            rejected["REJECT_ADDITIONAL_SOURCE_EXCLUSION_QUEUE_OVERLAP"] += 1
            continue
        if members & used:
            rejected["REJECT_WITHIN_BATCH_SOURCE_COLLISION"] += 1
            continue
        records = [corpus[source] for source in sources]
        source_paths = [list(record["source_paths"]) for record in records]
        native_descriptions = [str(record["native_description"]) for record in records]
        selected.append({
            **hypothesis,
            "batch_id": f"SN-SEM-{args.batch_label}",
            "batch_rank": len(selected) + 1,
            "discovery_route": "HASH_BOUND_LOCAL_CPU_BGE_EXACT_NATIVE_DESCRIPTION_MUTUAL_TRIANGLE",
            "selection_scope": "SOURCE_NATIVE_LOCAL_BGE_DESCRIPTION_ONLY_NAVIGATION_CONTINUATION",
            "member_source_paths": source_paths,
            "member_native_descriptions": native_descriptions,
            "source_native_description_bindings": [
                {"canonical_source_sha256": source, "native_description_sha256": description_hash, "source_paths": paths}
                for source, description_hash, paths in zip(sources, description_hashes, source_paths)
            ],
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "packet_state": "NOT_MATERIALISED_DISCOVERY_QUEUE_ONLY",
            "later_target_blind_paf_obligation": "REQUIRED_AFTER_INDEPENDENT_FULL_SOURCE_REVIEW; record any high-cue finding prospectively in target-blind PAF review. No high-cue classification, exclusion, or selection success is made here.",
            "claim_boundary": "Hash-bound local CPU BGE exact-native-description navigation hypothesis only; it establishes no semantic truth, family validity, provenance/licence result, prompt, admission, selector/retrieval result, acceptable-set result, or metric.",
        })
        used.update(members)
        if len(selected) == args.expected_families:
            break

    result = {
        "selected_families": len(selected),
        "selected_member_occurrences": len(selected) * 3,
        "selected_unique_source_hashes": len(used),
        "intersection_selected_vs_phase0_v2_inspection_union": len(used & phase0_sources),
        "intersection_selected_vs_additional_exclusion_queues": len(used & additional_sources),
        "selection_rejection_counts_before_completion": dict(sorted(rejected.items())),
    }
    if len(selected) != args.expected_families or len(used) != args.expected_families * 3 or used & excluded_sources:
        raise SystemExit(f"BGE continuation selection failure: {json.dumps(result, sort_keys=True)}")
    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "batch_id": f"SN-SEM-{args.batch_label}",
            **result,
            "selected_family_ids": [row["family_id"] for row in selected],
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    output.mkdir(parents=True)
    label_lower = args.batch_label.lower()
    queue_path = output / f"{label_lower}_source_native_local_bge_family_queue.jsonl"
    defer_path = output / "discovery_defer_ledger.jsonl"
    replay_path = output / "source_provenance_byte_replay_ledger.jsonl"
    exclusion_path = output / "historical_source_exclusion_manifest.json"
    dossier_path = output / f"{args.batch_label}_DISCOVERY_DOSSIER_2026-09-05.md"
    summary_path = output / "summary.json"
    write_jsonl(queue_path, selected)

    defers: list[dict[str, Any]] = []
    replays: list[dict[str, Any]] = []
    for family in selected:
        sources = [str(value) for value in family["member_source_sha256"]]
        description_hashes = [str(value) for value in family["member_native_description_sha256"]]
        paths_by_source = family["member_source_paths"]
        defers.append({
            "record_type": "discovery_defer",
            "batch_id": family["batch_id"],
            "batch_rank": family["batch_rank"],
            "family_id": family["family_id"],
            "member_source_sha256": sources,
            "disposition": "DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED",
            "reason": "Description-only local-BGE rank cannot establish a bounded shared envelope, semantic-family validity, independent first routes, operational contrast, provenance/licence sufficiency, promptability, admission, or any result. Independent full-source review and later target-blind PAF are required.",
        })
        for source, description_hash, paths in zip(sources, description_hashes, paths_by_source):
            record = corpus[source]
            if record["native_description_sha256"] != description_hash or record["source_paths"] != paths:
                raise SystemExit(f"frozen corpus path/description binding changed during materialisation: {source}")
            replayed = [sha256_file(WORKSPACE / path) for path in paths]
            if any(value != source for value in replayed):
                raise SystemExit(f"complete original source byte replay failed: {source}")
            replays.append({
                "record_type": "source_provenance_and_byte_replay",
                "family_id": family["family_id"],
                "batch_rank": family["batch_rank"],
                "canonical_source_sha256": source,
                "source_paths": paths,
                "replayed_path_sha256": replayed,
                "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                "native_description": record["native_description"],
                "native_description_sha256": description_hash,
                "native_description_origin": record["native_description_origin"],
                "native_description_literal_replay_status": record["native_description_replay_status"],
                "claim_boundary": "Frozen source path/hash and description replay only; not a substantive source reading, semantic, provenance/licence, prompt, admission, selector/retrieval, or metric decision.",
            })
    if len(replays) != args.expected_families * 3 or len({row["canonical_source_sha256"] for row in replays}) != len(replays):
        raise SystemExit("BGE continuation byte-replay cardinality/disjointness failure")
    write_jsonl(defer_path, defers)
    write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))

    exclusion = {
        "record_type": f"{args.batch_label}_historical_source_exclusion_manifest",
        "claim_boundary": "Hash-membership exclusion only; it establishes no semantic truth, review outcome, provenance/licence finding, prompt, admission, selector/retrieval result, or metric.",
        "phase0_v2": {
            "status": phase0_summary["status"],
            "summary_sha256": sha256_file(PHASE0_SUMMARY),
            "inspection_union": relative(PHASE0_INSPECTION_UNION),
            "inspection_union_sha256": sha256_file(PHASE0_INSPECTION_UNION),
            "inspection_unique_source_hashes": len(phase0_sources),
        },
        "additional_source_exclusion_queues": additional_manifest,
        "additional_exclusion_unique_source_hashes": len(additional_sources),
        "total_excluded_unique_source_hashes": len(excluded_sources),
        "selected_batch_unique_source_hashes": len(used),
        "intersection_selected_vs_all_excluded_sources": len(used & excluded_sources),
    }
    write_json(exclusion_path, exclusion)
    dossier_path.write_text("\n".join([
        f"# {args.batch_label} source-native local-BGE continuation discovery",
        "",
        "Status: **DISCOVERY QUEUE ONLY / UNREAD FULL ORIGINAL SOURCES / NO REVIEW OR ADMISSION**",
        "",
        "This controller replays only the already hash-bound local CPU BGE exact-native-description mutual-triangle output. It rejects every source in the Phase 0 v2 inspection union and every source named by a bound additional exclusion queue, then retains the first source-disjoint triads in frozen rank-fusion descending order, with ordered source-SHA tuples as the tie-breaker.",
        "",
        "The BGE route is navigation only. It does not establish semantic truth, family validity, provenance or licence sufficiency, a prompt, admission, a selector or retrieval result, an acceptable set, or a metric. No source-body feature, anchor, cue gate, prior-pass outcome, prompt, label, or review outcome is used to select a triad.",
        "",
        f"The queue has {len(selected)} triads and {len(used)} source-disjoint hashes. All selected source byte replays pass and all triads remain deferred to independent full-source review. Any high-cue issue is a later, prospective target-blind PAF obligation; it is neither a discovery selection feature nor unreviewed selection success.",
        "",
    ]), encoding="utf-8")
    summary = {
        "batch_id": f"SN-SEM-{args.batch_label}",
        "status": f"PASS_{args.batch_label}_HASH_BOUND_LOCAL_BGE_DISCOVERY_QUEUE_ONLY_UNREVIEWED",
        "claim_boundary": "Local CPU BGE description-only navigation queue only; not semantic truth, family validity, provenance/licence outcome, prompt, admission, acceptable-set audit, selector/retrieval result, or metric.",
        "bound_inputs": {
            "frozen_native_description_corpus": {"path": relative(CORPUS), "sha256": sha256_file(CORPUS)},
            "hash_bound_local_cpu_bge_summary": {"path": relative(BGE_SUMMARY), "sha256": sha256_file(BGE_SUMMARY)},
            "hash_bound_local_cpu_bge_mutual_triangles": {"path": relative(BGE_HYPOTHESES), "sha256": sha256_file(BGE_HYPOTHESES)},
            "phase0_v2_summary": {"path": relative(PHASE0_SUMMARY), "sha256": sha256_file(PHASE0_SUMMARY)},
            "phase0_v2_inspection_union": {"path": relative(PHASE0_INSPECTION_UNION), "sha256": sha256_file(PHASE0_INSPECTION_UNION)},
            "additional_source_exclusion_queues": additional_manifest,
            "historical_source_exclusion_manifest": sha256_file(exclusion_path),
        },
        "method": {
            "route": "HASH_BOUND_LOCAL_CPU_BGE_EXACT_NATIVE_DESCRIPTION_MUTUAL_TRIANGLE",
            "selection_input_boundary": "Only the fixed BGE mutual-triangle rank-fusion fields and member source hashes, the frozen corpus bindings needed to derive literal descriptions and paths, Phase 0 v2 source-hash membership, and explicit additional exclusion-queue source hashes. No model load, network, runtime, source-body content feature, anchor, high-cue feature, past outcome, prompt, label, review, or admission input is used.",
            "base_hypothesis_order": "rank-fusion descending, then ordered member source-SHA256 tuple ascending; retain the first triads that are source-disjoint from Phase 0 v2, additional queues, and earlier selected triads.",
            "source_disjointness_policy": "Reject all 3,922 Phase 0 v2 inspection-union hashes and every hash in each bound additional exclusion queue; require exactly three distinct source hashes per triad and no within-batch source reuse.",
            "high_cue_control": "No high-cue classification, gate, or success claim occurs at discovery. Any high-cue finding must be recorded later as a prospective target-blind PAF obligation after independent full-source review.",
        },
        "bge_validation": {
            "status": bge_summary["status"],
            "counts": bge_summary["counts"],
            "summary_sha256": sha256_file(BGE_SUMMARY),
            "mutual_triangle_sha256": sha256_file(BGE_HYPOTHESES),
            "mutual_triangle_cardinality": len(hypotheses),
        },
        "counts": {**result, "frozen_corpus_sources": len(corpus), "frozen_corpus_index_eligible_sources": 23_431, "phase0_v2_inspection_union_unique_sources": len(phase0_sources), "additional_exclusion_unique_sources": len(additional_sources), "deferred_families": len(defers), "source_byte_replays": len(replays)},
        "verification": {
            "hash_bound_local_cpu_bge_summary_and_hypotheses": "PASS",
            "phase0_v2_inspection_union_binding": "PASS",
            "source_disjointness_vs_all_bound_exclusions": "PASS",
            "within_selected_batch_source_disjointness": "PASS",
            "original_source_byte_replay": f"PASS_{len(replays)}_OF_{len(replays)}",
            "all_selected_families_deferred_pending_independent_full_source_review": f"PASS_{len(defers)}_OF_{len(defers)}",
            "high_cue_is_later_target_blind_paf_obligation_not_discovery_success": "PASS",
        },
        "outputs": {},
        "limitations": [
            "A local BGE description rank is a deterministic navigation priority, not semantic truth, family validity, or a retrieval metric.",
            "Byte replay preserves source identity only; it is not a substantive full-source or provenance/licence review.",
            "All selected triads remain unreviewed and deferred; later independent full-source review and target-blind PAF controls carry the substantive obligations.",
        ],
    }
    summary["outputs"] = {
        queue_path.name: sha256_file(queue_path),
        defer_path.name: sha256_file(defer_path),
        replay_path.name: sha256_file(replay_path),
        exclusion_path.name: sha256_file(exclusion_path),
        dossier_path.name: sha256_file(dossier_path),
    }
    write_json(summary_path, summary)
    print(json.dumps({"output": relative(output), "counts": summary["counts"], "outputs": summary["outputs"]}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
