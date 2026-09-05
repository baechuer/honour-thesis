#!/usr/bin/env python3
"""Materialise only the two Phase-0-authorised B053 residual triads.

The original B053 discovery queue is immutable evidence.  This controller does
not repair its 23 quarantined collision families; it derives a new, explicit
two-family review queue from the authoritative Phase-0 residual disposition.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
SOP = NC_ROOT / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
PHASE0 = NC_ROOT / "review/rq2b_nc_phase0_state_reconciliation_2026-09-05_v2"
PHASE0_SUMMARY = PHASE0 / "summary.json"
PHASE0_FAMILIES = PHASE0 / "phase0_family_state.jsonl"
PHASE0_SOURCES = PHASE0 / "phase0_source_native_inspection_union.jsonl"
B053_ROOT = NC_ROOT / "review/source_native_education_tutoring_course_assessment_learning_content_hr_recruiting_onboarding_career_b053_2026-09-05"
B053_QUEUE = B053_ROOT / "b053_source_native_semantic_family_queue.jsonl"
CORPUS = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
OUTPUT = NC_ROOT / "review/source_native_b053_residual_disjoint_triads_2026-09-05"


def digest(path: Path) -> str:
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


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite: {OUTPUT}")
    required = [SOP, PHASE0_SUMMARY, PHASE0_FAMILIES, PHASE0_SOURCES, B053_QUEUE, CORPUS]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"missing required input(s): {missing}")
    phase0 = json.loads(PHASE0_SUMMARY.read_text(encoding="utf-8"))
    if phase0.get("status") != "PASS_RQ2B_NC_PHASE0_CANONICAL_STATE_RECONCILIATION_NO_EXPERIMENT":
        raise SystemExit("requires passing Phase 0 reconciliation")
    residual_ids = sorted(
        str(row["family_token"])
        for row in read_jsonl(PHASE0_FAMILIES)
        if row.get("batch") == "B053" and row.get("phase0_state") == "DEFERRED_UNREVIEWED_FULL_SOURCE_REQUIRED"
    )
    if len(residual_ids) != 2:
        raise SystemExit(f"expected two B053 residuals, got {residual_ids}")
    queue_by_id = {str(row["family_id"]): row for row in read_jsonl(B053_QUEUE)}
    if len(queue_by_id) != 25 or not set(residual_ids) <= set(queue_by_id):
        raise SystemExit("B053 queue cannot reconstruct Phase-0 residual selection")
    selected = [dict(queue_by_id[family_id]) for family_id in residual_ids]
    source_hashes = [str(source_hash) for row in selected for source_hash in row["member_source_sha256"]]
    if len(source_hashes) != 6 or len(set(source_hashes)) != 6:
        raise SystemExit("B053 residuals are not two source-disjoint triads")
    phase0_source_by_hash = {str(row["canonical_source_sha256"]): row for row in read_jsonl(PHASE0_SOURCES)}
    for source_hash in source_hashes:
        history = phase0_source_by_hash.get(source_hash)
        if not history or history.get("inspection_batches") != ["B053"]:
            raise SystemExit(f"B053 residual source not uniquely isolated from B001-B052: {source_hash}")
    corpus = {str(row["canonical_source_sha256"]): row for row in read_jsonl(CORPUS)}
    if any(source_hash not in corpus for source_hash in source_hashes):
        raise SystemExit("residual source absent from frozen corpus")
    for rank, row in enumerate(selected, start=1):
        row["batch_id"] = "SN-SEM-B053-RESIDUAL"
        row["batch_rank"] = rank
        row["discovery_route"] = "PHASE0_AUTHORISED_B053_SOURCE_DISJOINT_RESIDUAL_REPLAY"
        row["selection_scope"] = "ONLY_TWO_B053_PHASE0_DEFERRED_RESIDUALS_NO_QUARANTINED_COMPONENT_MEMBER"
        row["review_state"] = "UNREVIEWED_FULL_SOURCE"
        row["packet_state"] = "NOT_MATERIALISED_DISCOVERY_QUEUE_ONLY"
        row["claim_boundary"] = "Authorised source-disjoint B053 residual replay only; no semantic-family, source-review, provenance, prompt, admission, selector, or metric decision."
    OUTPUT.mkdir(parents=True)
    queue_path = OUTPUT / "b053_residual_source_native_semantic_family_queue.jsonl"
    replay_path = OUTPUT / "source_provenance_byte_replay_ledger.jsonl"
    defer_path = OUTPUT / "discovery_defer_ledger.jsonl"
    write_jsonl(queue_path, selected)
    replays: list[dict[str, Any]] = []
    defers: list[dict[str, Any]] = []
    for row in selected:
        hashes = [str(value) for value in row["member_source_sha256"]]
        defers.append({
            "record_type": "discovery_defer",
            "batch_id": row["batch_id"],
            "batch_rank": row["batch_rank"],
            "family_id": row["family_id"],
            "member_source_sha256": hashes,
            "disposition": "DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED",
            "reason": "Phase 0 isolated a source-disjoint residual but did not review its complete originals; independent full-source review remains required.",
        })
        for source_hash, description_hash, paths in zip(hashes, row["member_native_description_sha256"], row["member_source_paths"]):
            source = corpus[source_hash]
            if source["native_description_sha256"] != description_hash or source["source_paths"] != paths:
                raise SystemExit(f"frozen source binding mismatch: {source_hash}")
            replayed = [digest(WORKSPACE / path) for path in paths]
            if any(value != source_hash for value in replayed):
                raise SystemExit(f"source byte replay failed: {source_hash}")
            replays.append({
                "record_type": "source_provenance_and_byte_replay",
                "family_id": row["family_id"],
                "batch_rank": row["batch_rank"],
                "canonical_source_sha256": source_hash,
                "source_paths": paths,
                "replayed_path_sha256": replayed,
                "source_byte_replay_status": "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256",
                "native_description_sha256": description_hash,
                "native_description_origin": source["native_description_origin"],
                "claim_boundary": "Frozen source identity replay only; not a provenance adequacy or downstream decision.",
            })
    write_jsonl(replay_path, sorted(replays, key=lambda row: row["canonical_source_sha256"]))
    write_jsonl(defer_path, defers)
    summary = {
        "batch_id": "SN-SEM-B053-RESIDUAL",
        "status": "PASS_B053_RESIDUAL_SOURCE_DISJOINT_QUEUE_ONLY_UNREVIEWED",
        "claim_boundary": "Residual discovery queue only; no full-source review, provenance/licence result, prompt, adequate alternative, library admission, selector result, or metric.",
        "bound_inputs": {
            "master_pre_experiment_sop": digest(SOP),
            "phase0_summary": digest(PHASE0_SUMMARY),
            "phase0_family_state": digest(PHASE0_FAMILIES),
            "phase0_source_union": digest(PHASE0_SOURCES),
            "immutable_original_B053_queue": digest(B053_QUEUE),
            "source_native_description_corpus": digest(CORPUS),
        },
        "method": {
            "selection": "Select exactly the two B053 Phase-0 residuals with DEFERRED_UNREVIEWED_FULL_SOURCE_REQUIRED; never select a quarantined connected-component member.",
            "source_disjointness": "Each residual is a three-distinct-source triad; all six sources have inspection_batches exactly [B053], mechanically proving no B001-B052 collision in the Phase-0 source union.",
            "quarantine_preservation": "The original 25-family B053 queue and the Phase-0 23-family quarantine ledger remain unmodified.",
        },
        "counts": {"residual_families": 2, "residual_source_occurrences": 6, "residual_unique_sources": 6, "source_overlap_residual_vs_B001_B052": 0, "source_byte_replays": len(replays), "deferred_families": len(defers)},
        "outputs": {queue_path.name: digest(queue_path), replay_path.name: digest(replay_path), defer_path.name: digest(defer_path)},
        "verification": {"within_residual_source_disjointness": "PASS", "source_disjointness_vs_B001_B052": "PASS", "original_source_byte_replay": "PASS_6_OF_6", "quarantined_B053_members_reintroduced": 0},
    }
    write_json(OUTPUT / "summary.json", summary)
    print(json.dumps({"output": str(OUTPUT.relative_to(WORKSPACE)), "counts": summary["counts"], "outputs": summary["outputs"]}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
