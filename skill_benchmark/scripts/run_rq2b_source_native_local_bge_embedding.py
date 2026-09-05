#!/usr/bin/env python3
"""Run the frozen local BGE source-native description index on-device only."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PREFLIGHT_DIR = NC_ROOT / "manifests/source_native_description_local_bge_embedding_preflight_2026-09-04"
TEXTS = PREFLIGHT_DIR / "unique_native_description_texts.jsonl"
BINDINGS = PREFLIGHT_DIR / "source_to_text_bindings.jsonl"
MANIFEST = PREFLIGHT_DIR / "manifest.json"
OUTPUT_DIR = NC_ROOT / "review/source_native_local_bge_embedding_2026-09-04"

MODEL_ID = "BAAI/bge-small-en-v1.5"
MODEL_REVISION_REQUESTED = "main"
DIMENSION_EXPECTED = 384
TOP_NEIGHBOURS = 12
BATCH_SIZE = 64


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


def model_file_manifest(model_cache_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(model_cache_dir.rglob("*")):
        if path.is_file():
            rows.append({"relative_path": str(path.relative_to(model_cache_dir)), "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return rows


def resolve_cached_snapshot(model_cache_dir: Path) -> tuple[str, Path]:
    repo_dir = model_cache_dir / "models--BAAI--bge-small-en-v1.5"
    revision_ref = repo_dir / "refs" / MODEL_REVISION_REQUESTED
    if not revision_ref.is_file():
        raise SystemExit("Local BGE snapshot is absent; download must be performed as a separately authorised action")
    commit = revision_ref.read_text(encoding="utf-8").strip()
    snapshot = repo_dir / "snapshots" / commit
    if not commit or not (snapshot / "modules.json").is_file() or not (snapshot / "model.safetensors").is_file():
        raise SystemExit("Local BGE snapshot is incomplete")
    return commit, snapshot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local BGE exact-native-description embedding discovery.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--model-cache-dir", type=Path, default=Path("/private/tmp/rq2b-bge-small-en-v1.5-cache"))
    parser.add_argument("--staging-dir", type=Path, default=Path("/private/tmp/rq2b-local-bge-staging"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.execute:
        raise SystemExit("Refusing model execution without --execute")
    required = [TEXTS, BINDINGS, MANIFEST]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing frozen preflight input(s): {missing}")
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Output directory already exists: {OUTPUT_DIR}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    contract = manifest.get("local_model_contract", {})
    if contract.get("model_id") != MODEL_ID or contract.get("expected_embedding_dimension") != DIMENSION_EXPECTED or contract.get("top_neighbours") != TOP_NEIGHBOURS or contract.get("batch_size") != BATCH_SIZE or contract.get("normalise_embeddings") is not True or contract.get("device_policy") != "CPU_ONLY_FOR_REPRODUCIBLE_LOCAL_EXECUTION" or contract.get("trust_remote_code") is not False:
        raise SystemExit("Frozen local-model contract mismatch")
    texts = read_jsonl(TEXTS)
    bindings = read_jsonl(BINDINGS)
    if len(texts) != 22_765 or len(bindings) != 23_431:
        raise SystemExit("Frozen local embedding payload cardinality mismatch")
    for row in texts:
        if hashlib.sha256(str(row["native_description"]).encode("utf-8")).hexdigest() != row["native_description_sha256"]:
            raise SystemExit("Frozen native description text hash mismatch")

    try:
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as error:
        raise SystemExit(f"Local embedding runtime unavailable: {error}")

    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    model_cache_dir = args.model_cache_dir.resolve()
    model_cache_dir.mkdir(parents=True, exist_ok=True)
    staging_dir = args.staging_dir.resolve()
    if staging_dir.exists():
        raise SystemExit(f"Local BGE staging directory already exists: {staging_dir}")
    staging_dir.mkdir(parents=True)
    progress_path = staging_dir / "progress.json"
    write_json(progress_path, {"status": "RUNNING_MODEL_LOAD", "completed_descriptions": 0, "total_descriptions": len(texts), "started_unix_seconds": time.time()})
    loaded_commit, snapshot_path = resolve_cached_snapshot(model_cache_dir)
    model = SentenceTransformer(
        str(snapshot_path),
        cache_folder=str(model_cache_dir),
        local_files_only=True,
        trust_remote_code=False,
        device="cpu",
    )
    vectors_path_staging = staging_dir / "unique_native_description_embeddings.f32"
    vectors = np.memmap(vectors_path_staging, dtype="float32", mode="w+", shape=(len(texts), DIMENSION_EXPECTED))
    encode_chunk_size = 256
    descriptions = [str(row["native_description"]) for row in texts]
    for start in range(0, len(descriptions), encode_chunk_size):
        end = min(start + encode_chunk_size, len(descriptions))
        chunk = model.encode(
            descriptions[start:end],
            batch_size=BATCH_SIZE,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
            device="cpu",
        ).astype("float32", copy=False)
        if chunk.shape != (end - start, DIMENSION_EXPECTED):
            raise SystemExit(f"Unexpected local embedding chunk shape: {chunk.shape}")
        vectors[start:end] = chunk
        vectors.flush()
        write_json(progress_path, {"status": "RUNNING_LOCAL_CPU_ENCODING", "completed_descriptions": end, "total_descriptions": len(descriptions), "model_id": MODEL_ID, "model_revision_loaded": loaded_commit, "updated_unix_seconds": time.time()})
    vectors.flush()
    vectors = np.asarray(vectors)
    if vectors.shape != (len(texts), DIMENSION_EXPECTED):
        raise SystemExit(f"Unexpected local embedding shape: {vectors.shape}")
    write_json(progress_path, {"status": "RUNNING_NEIGHBOUR_CONSTRUCTION", "completed_descriptions": len(descriptions), "total_descriptions": len(descriptions), "model_id": MODEL_ID, "model_revision_loaded": loaded_commit, "updated_unix_seconds": time.time()})
    text_hashes = [str(row["native_description_sha256"]) for row in texts]
    text_index = {value: index for index, value in enumerate(text_hashes)}
    sources_by_text: dict[str, list[str]] = defaultdict(list)
    for binding in bindings:
        sources_by_text[str(binding["native_description_sha256"])].append(str(binding["canonical_source_sha256"]))
    for values in sources_by_text.values():
        values.sort()
    source_hashes = sorted(str(binding["canonical_source_sha256"]) for binding in bindings)
    source_to_text = {str(binding["canonical_source_sha256"]): str(binding["native_description_sha256"]) for binding in bindings}

    ranking_rows: list[dict[str, Any]] = []
    source_ranks: dict[str, list[tuple[str, float]]] = {}
    block_size = 256
    candidate_text_window = 64
    for start in range(0, len(texts), block_size):
        end = min(start + block_size, len(texts))
        scores = vectors[start:end] @ vectors.T
        for local_index, global_index in enumerate(range(start, end)):
            scores[local_index, global_index] = float("-inf")
            candidate_indices = np.argpartition(-scores[local_index], candidate_text_window - 1)[:candidate_text_window]
            ordered_text_indices = sorted(candidate_indices.tolist(), key=lambda candidate: (-float(scores[local_index, candidate]), text_hashes[candidate]))
            candidate_sources: list[tuple[str, float]] = []
            for candidate_index in ordered_text_indices:
                score = float(scores[local_index, candidate_index])
                if score == float("-inf"):
                    continue
                for source_hash in sources_by_text[text_hashes[candidate_index]]:
                    candidate_sources.append((source_hash, score))
                    if len(candidate_sources) == TOP_NEIGHBOURS:
                        break
                if len(candidate_sources) == TOP_NEIGHBOURS:
                    break
            if len(candidate_sources) != TOP_NEIGHBOURS:
                raise SystemExit("Insufficient dense neighbour candidates")
            for source_hash in sources_by_text[text_hashes[global_index]]:
                source_ranks[source_hash] = candidate_sources
    if set(source_ranks) != set(source_hashes):
        raise SystemExit("Dense source-rank coverage mismatch")
    for seed in source_hashes:
        for rank, (neighbour, score) in enumerate(source_ranks[seed], start=1):
            ranking_rows.append({
                "record_type": "native_description_local_bge_neighbour",
                "seed_source_sha256": seed,
                "neighbour_source_sha256": neighbour,
                "rank": rank,
                "cosine_similarity": score,
                "model_id": MODEL_ID,
                "discovery_route": "LOCAL_BGE_EXACT_NATIVE_DESCRIPTION",
                "claim_boundary": "On-device source-reading priority only; not semantic ground truth or a cluster result.",
            })
    rank_lookup = {(seed, neighbour): rank for seed, ranked in source_ranks.items() for rank, (neighbour, _score) in enumerate(ranked, start=1)}
    mutual: dict[str, set[str]] = defaultdict(set)
    for (left, right), _rank in rank_lookup.items():
        if (right, left) in rank_lookup:
            mutual[left].add(right)
    family_rows: list[dict[str, Any]] = []
    observed: set[tuple[str, str, str]] = set()
    for left in source_hashes:
        for middle, right in combinations(sorted(mutual[left]), 2):
            members = tuple(sorted((left, middle, right)))
            if members in observed:
                continue
            observed.add(members)
            if middle not in mutual[right]:
                continue
            if len({source_to_text[source] for source in members}) != 3:
                continue
            directional_ranks = [rank_lookup[(first, second)] for first in members for second in members if first != second]
            if len(directional_ranks) != 6:
                raise SystemExit("Dense mutual triangle lacks all directional ranks")
            family_rows.append({
                "record_type": "source_native_confusable_family_hypothesis",
                "family_id": "SN-BGE-" + hashlib.sha256("|".join(members).encode("utf-8")).hexdigest()[:16],
                "member_source_sha256": list(members),
                "member_native_description_sha256": [source_to_text[source] for source in members],
                "mutual_directional_ranks": directional_ranks,
                "reciprocal_link_count": 3,
                "rank_fusion_score": sum(1.0 / (60.0 + rank) for rank in directional_ranks),
                "model_id": MODEL_ID,
                "discovery_route": "LOCAL_BGE_EXACT_NATIVE_DESCRIPTION",
                "review_state": "UNREVIEWED_FULL_SOURCE",
                "claim_boundary": "Hypothesis only; complete original sources must establish envelope, independence and contrast.",
            })
    family_rows.sort(key=lambda row: (-row["reciprocal_link_count"], -row["rank_fusion_score"], row["member_source_sha256"]))
    OUTPUT_DIR.mkdir(parents=True)
    vectors_path = OUTPUT_DIR / "unique_native_description_embeddings.f32"
    vectors_path.write_bytes(vectors_path_staging.read_bytes())
    ranking_path = OUTPUT_DIR / "native_description_local_bge_top12.jsonl"
    family_path = OUTPUT_DIR / "all_mutual_triangle_hypotheses.jsonl"
    model_manifest_path = OUTPUT_DIR / "local_model_file_manifest.json"
    write_jsonl(ranking_path, ranking_rows)
    write_jsonl(family_path, family_rows)
    write_json(model_manifest_path, {"model_id": MODEL_ID, "revision_requested": MODEL_REVISION_REQUESTED, "model_revision_loaded": loaded_commit, "snapshot_relative_path": str(snapshot_path.relative_to(model_cache_dir)), "cache_file_manifest": model_file_manifest(model_cache_dir)})
    summary = {
        "status": "PASS_SOURCE_NATIVE_LOCAL_BGE_EXACT_DESCRIPTION_DENSE_INDEX_NO_SEMANTIC_CLUSTER_DECISION",
        "bound_inputs": {relative(TEXTS): sha256_file(TEXTS), relative(BINDINGS): sha256_file(BINDINGS), relative(MANIFEST): sha256_file(MANIFEST)},
        "model": {"model_id": MODEL_ID, "revision_requested": MODEL_REVISION_REQUESTED, "implementation": "sentence-transformers", "device": "cpu", "normalise_embeddings": True, "dimension": int(vectors.shape[1]), "batch_size": BATCH_SIZE, "trust_remote_code": False},
        "counts": {"source_bindings": len(bindings), "unique_native_descriptions": len(texts), "directed_top12_edges": len(ranking_rows), "mutual_triangles": len(family_rows)},
        "outputs": {"unique_native_description_embeddings.f32": sha256_file(vectors_path), "native_description_local_bge_top12.jsonl": sha256_file(ranking_path), "all_mutual_triangle_hypotheses.jsonl": sha256_file(family_path), "local_model_file_manifest.json": sha256_file(model_manifest_path)},
        "claim_boundary": "Local dense description index only. It uses no prompts, labels, full source bodies or outcome data, and does not establish cluster validity, whole-library coverage, acceptable sets, admission, selector performance or a metric.",
    }
    write_json(OUTPUT_DIR / "summary.json", summary)
    write_json(progress_path, {"status": "COMPLETED", "completed_descriptions": len(descriptions), "total_descriptions": len(descriptions), "output_summary": relative(OUTPUT_DIR / "summary.json"), "updated_unix_seconds": time.time()})
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
