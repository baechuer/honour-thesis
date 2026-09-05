#!/usr/bin/env python3
"""Verify complete RQ2b warm state with zero API calls and model forwards."""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_b1s_implementation_seal,
    verify_frozen_manifest,
    version_root,
    write_json_new,
)
from run_rq2b_bm25 import GlobalBM25, annotate_unresolved_public_equivalents, rank_row
from run_rq2b_qwen import DIMENSIONS, ExactEmbeddingCache
from run_rq2b_skillrouter_embedding import (
    DIMENSIONS as SKILLROUTER_EMBEDDING_DIMENSIONS,
    ExactEmbeddingCache as SkillRouterEmbeddingCache,
    score_payload as score_skillrouter_embedding_payload,
)
from run_rq2b_skillrouter import WindowScoreCache, rerank_one, verify_denominator_identity


INVARIANT_B1_FIELDS = (
    "strict_gold_rank",
    "acceptable_gold_rank",
    "strict_hit_at_1",
    "acceptable_hit_at_1",
    "strict_recall_at_5",
    "acceptable_recall_at_5",
    "strict_recall_at_20",
    "acceptable_recall_at_20",
    "strict_recall_at_50",
    "acceptable_recall_at_50",
    "strict_recall_at_100",
    "acceptable_recall_at_100",
    "strict_reciprocal_rank",
    "acceptable_reciprocal_rank",
    "top_5_skill_ids",
    "top_20_skill_ids",
    "top_50_skill_ids",
)
QWEN_SENSITIVITY_FIELDS = (
    "strict_gold_document_chunk_count",
    "strict_gold_document_chunk_class",
    "strict_gold_selector_utf8_bytes",
    "strict_gold_source_length_quartile",
)
SKILLROUTER_EMBEDDING_SENSITIVITY_FIELDS = (
    "strict_gold_document_model_tokens",
    "strict_gold_selector_utf8_bytes",
    "strict_gold_source_length_quartile",
)
TOP_100_ENTRY_KEYS = {"rank", "skill_id", "score", "destination_class"}
B1_SCORE_REL_TOLERANCE = 1e-12
B1_SCORE_ABS_TOLERANCE = 1e-12


def require_top_100_equal(
    observed: list[dict[str, Any]],
    expected: list[dict[str, Any]],
    label: str,
) -> None:
    require(len(observed) == len(expected), f"Warm B1 top-100 length mismatch ({label})")
    for index, (observed_entry, expected_entry) in enumerate(
        zip(observed, expected, strict=True),
        start=1,
    ):
        require(
            set(observed_entry) == set(expected_entry) == TOP_100_ENTRY_KEYS,
            f"Warm B1 top-100 schema mismatch ({label}/{index})",
        )
        for field in ("rank", "skill_id", "destination_class"):
            require(
                observed_entry[field] == expected_entry[field],
                f"Warm B1 top-100 mismatch ({label}/{index}): {field}",
            )
        observed_score = float(observed_entry["score"])
        expected_score = float(expected_entry["score"])
        require(
            math.isfinite(observed_score)
            and math.isfinite(expected_score)
            and math.isclose(
                observed_score,
                expected_score,
                rel_tol=B1_SCORE_REL_TOLERANCE,
                abs_tol=B1_SCORE_ABS_TOLERANCE,
            ),
            f"Warm B1 top-100 score mismatch ({label}/{index})",
        )


def require_b1_equal(observed: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    for field in INVARIANT_B1_FIELDS:
        require(observed[field] == expected[field], f"Warm B1 mismatch ({label}): {field}")
    require_top_100_equal(observed["top_100"], expected["top_100"], label)


def annotate_warm_prompts(
    prompts: list[dict[str, Any]],
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Apply the same destination-class annotation as both cold B1 runners."""
    return annotate_unresolved_public_equivalents(prompts, sources)


def verify_bm25(root: Path, manifest_paths: list[Path], prompts: list[dict[str, Any]]) -> dict[str, Any]:
    checked_rows = 0
    total_seconds = 0.0
    manifests = 0
    for manifest_path in manifest_paths:
        manifest = read_json(manifest_path)
        if manifest.get("schema_version") != "rq2b-bm25-run-manifest-v1":
            continue
        require(manifest.get("state") == "complete_scientific_b1_local", f"Incomplete BM25 run: {manifest_path}")
        require(manifest.get("version_id") == VERSION_ID, f"Wrong BM25 version: {manifest_path}")
        index_path = root / manifest["artifacts"]["index"]["path"]
        rows_path = root / manifest["artifacts"]["rows"]["path"]
        require(sha256_file(index_path) == manifest["artifacts"]["index"]["sha256"], "BM25 warm index drift")
        require(sha256_file(rows_path) == manifest["artifacts"]["rows"]["sha256"], "BM25 warm rows drift")
        index = GlobalBM25.from_persisted(read_json(index_path))
        expected_by_prompt = {row["prompt_id"]: row for row in read_jsonl(rows_path)}
        require(len(expected_by_prompt) == len(prompts), "BM25 warm prompt coverage mismatch")
        started = time.perf_counter()
        for prompt in prompts:
            observed = rank_row(
                prompt,
                index.rank(prompt["prompt"]),
                representation=manifest["representation"],
                query_seconds=0.0,
            )
            require_b1_equal(observed, expected_by_prompt[prompt["prompt_id"]], f"bm25/{manifest['representation']}/{prompt['prompt_id']}")
            checked_rows += 1
        total_seconds += time.perf_counter() - started
        manifests += 1
    require(manifests == 4 and checked_rows == 4 * len(prompts), "BM25 warm matrix is incomplete")
    return {
        "manifests": manifests,
        "rows_verified": checked_rows,
        "warm_query_seconds": total_seconds,
        "network_calls": 0,
    }


def normalized_matrix(vectors: list[list[float]]) -> Any:
    import numpy as np

    matrix = np.asarray(vectors, dtype=np.float64)
    require(matrix.ndim == 2 and matrix.shape[1] == DIMENSIONS, "Qwen warm vector matrix shape mismatch")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0.0)), "Qwen warm vector norm mismatch")
    return matrix / norms


def verify_qwen(root: Path, manifest_paths: list[Path], prompts: list[dict[str, Any]]) -> dict[str, Any]:
    import numpy as np

    qwen_manifests = [path for path in manifest_paths if read_json(path).get("schema_version") == "rq2b-qwen-run-manifest-v1"]
    require(len(qwen_manifests) == 1, "Qwen warm verification requires exactly one complete run")
    manifest_path = qwen_manifests[0]
    manifest = read_json(manifest_path)
    require(manifest.get("state") == "complete_scientific_b1_external", "Qwen warm run is incomplete")
    require(manifest.get("version_id") == VERSION_ID, "Qwen warm run version mismatch")
    payload_path = root / manifest["payload_manifest_path"]
    require(sha256_file(payload_path) == manifest["payload_manifest_sha256"], "Qwen warm payload drift")
    payload = read_json(payload_path)
    text_path = root / payload["text_inventory"]["path"]
    require(sha256_file(text_path) == payload["text_inventory"]["sha256"], "Qwen warm text inventory drift")
    result_path = root / manifest["artifacts"]["rows"]["path"]
    require(sha256_file(result_path) == manifest["artifacts"]["rows"]["sha256"], "Qwen warm result drift")
    expected = {
        (row["retriever"], row["representation"], row["prompt_id"]): row
        for row in read_jsonl(result_path)
    }
    cache = ExactEmbeddingCache(root / "skill_benchmark/cache/rq2b/embeddings")
    vector_by_id: dict[str, list[float]] = {}
    cache_started = time.perf_counter()
    for row in read_jsonl(text_path):
        vector = cache.load(row["text"])
        require(vector is not None, f"Qwen warm cache miss: {row['text_id']}")
        vector_by_id[row["text_id"]] = vector
    cache_seconds = time.perf_counter() - cache_started

    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    checked = 0
    scoring_started = time.perf_counter()
    for representation, documents in payload["documents"].items():
        skill_ids = [row["skill_id"] for row in documents]
        skill_index = {skill_id: index for index, skill_id in enumerate(skill_ids)}
        chunk_vectors: list[list[float]] = []
        starts: list[int] = []
        chunk_counts: list[int] = []
        for document in documents:
            starts.append(len(chunk_vectors))
            values = [vector_by_id[text_id] for text_id in document["chunk_text_ids"]]
            chunk_counts.append(len(values))
            chunk_vectors.extend(values)
        chunk_matrix = normalized_matrix(chunk_vectors)
        mean_vectors = []
        for start, count in zip(starts, chunk_counts, strict=True):
            mean = chunk_matrix[start : start + count].mean(axis=0)
            norm = np.linalg.norm(mean)
            require(bool(np.isfinite(norm)) and norm > 0.0, "Qwen warm mean-vector norm mismatch")
            mean_vectors.append(mean / norm)
        mean_matrix = np.vstack(mean_vectors)

        for prompt_id, query_id in payload["query_text_ids"].items():
            prompt = prompt_by_id[prompt_id]
            query = normalized_matrix([vector_by_id[query_id]])[0]
            flat_scores = chunk_matrix @ query
            max_scores = np.maximum.reduceat(flat_scores, np.asarray(starts, dtype=np.int64))
            mean_scores = mean_matrix @ query
            max_ranking = sorted(
                zip(skill_ids, (float(value) for value in max_scores), strict=True),
                key=lambda item: (-item[1], item[0]),
            )
            mean_ranking = sorted(
                zip(skill_ids, (float(value) for value in mean_scores), strict=True),
                key=lambda item: (-item[1], item[0]),
            )
            observed_max = rank_row(
                prompt,
                max_ranking,
                representation=representation,
                query_seconds=0.0,
                retriever="qwen-max-chunk",
                aggregation="maximum_chunk_cosine",
            )
            observed_mean = rank_row(
                prompt,
                mean_ranking,
                representation=representation,
                query_seconds=0.0,
                retriever="qwen-mean-chunk-sensitivity",
                aggregation="cosine_of_l2_normalized_chunk_mean",
            )
            gold_document = documents[skill_index[prompt["gold_skill"]]]
            sensitivity_metadata = {
                "strict_gold_document_chunk_count": len(gold_document["chunk_text_ids"]),
                "strict_gold_document_chunk_class": (
                    "one_chunk" if len(gold_document["chunk_text_ids"]) == 1 else "multi_chunk"
                ),
                "strict_gold_selector_utf8_bytes": gold_document["selector_utf8_bytes"],
                "strict_gold_source_length_quartile": gold_document["source_length_quartile"],
            }
            observed_max.update(sensitivity_metadata)
            observed_mean.update(sensitivity_metadata)
            require_b1_equal(observed_max, expected[("qwen-max-chunk", representation, prompt_id)], f"qwen-max/{representation}/{prompt_id}")
            require_b1_equal(observed_mean, expected[("qwen-mean-chunk-sensitivity", representation, prompt_id)], f"qwen-mean/{representation}/{prompt_id}")
            for field in QWEN_SENSITIVITY_FIELDS:
                require(
                    observed_max[field] == expected[("qwen-max-chunk", representation, prompt_id)][field],
                    f"Qwen warm sensitivity mismatch (max/{representation}/{prompt_id}): {field}",
                )
                require(
                    observed_mean[field] == expected[("qwen-mean-chunk-sensitivity", representation, prompt_id)][field],
                    f"Qwen warm sensitivity mismatch (mean/{representation}/{prompt_id}): {field}",
                )
            stored_winners = expected[("qwen-max-chunk", representation, prompt_id)]["winning_chunk_by_top_100_skill"]
            for skill_id, _ in max_ranking[:100]:
                document_index = skill_index[skill_id]
                start = starts[document_index]
                count = chunk_counts[document_index]
                winning = int(np.argmax(flat_scores[start : start + count]))
                require(stored_winners[skill_id] == winning, f"Qwen warm winning-chunk mismatch: {prompt_id}/{skill_id}")
            checked += 2
    require(checked == 8 * len(prompts), "Qwen warm matrix is incomplete")
    return {
        "manifests": 1,
        "rows_verified": checked,
        "cache_entries_verified": len(vector_by_id),
        "cache_load_seconds": cache_seconds,
        "warm_scoring_seconds": time.perf_counter() - scoring_started,
        "network_calls": 0,
        "api_calls": 0,
    }


def verify_skillrouter_embedding(
    root: Path,
    manifest_paths: list[Path],
    prompts: list[dict[str, Any]],
) -> dict[str, Any]:
    manifests = [
        path
        for path in manifest_paths
        if read_json(path).get("schema_version")
        == "rq2b-skillrouter-embedding-run-manifest-v1"
    ]
    require(len(manifests) == 1, "SkillRouter embedding warm verification requires one complete run")
    manifest = read_json(manifests[0])
    require(
        manifest.get("state") == "complete_scientific_b1_skillrouter_embedding",
        "SkillRouter embedding warm run is incomplete",
    )
    require(manifest.get("version_id") == VERSION_ID, "SkillRouter embedding warm version mismatch")
    require(
        manifest.get("dimensions") == SKILLROUTER_EMBEDDING_DIMENSIONS,
        "SkillRouter embedding warm dimension mismatch",
    )
    payload_path = root / manifest["payload_manifest_path"]
    require(
        sha256_file(payload_path) == manifest["payload_manifest_sha256"],
        "SkillRouter embedding warm payload drift",
    )
    payload = read_json(payload_path)
    text_path = root / payload["text_inventory"]["path"]
    require(
        sha256_file(text_path) == payload["text_inventory"]["sha256"],
        "SkillRouter embedding warm text inventory drift",
    )
    result_path = root / manifest["artifacts"]["rows"]["path"]
    require(
        sha256_file(result_path) == manifest["artifacts"]["rows"]["sha256"],
        "SkillRouter embedding warm result drift",
    )
    expected = {
        (row["representation"], row["prompt_id"]): row
        for row in read_jsonl(result_path)
    }
    cache = SkillRouterEmbeddingCache(root / "skill_benchmark/cache/rq2b/embeddings")
    vectors: dict[str, list[float]] = {}
    cache_started = time.perf_counter()
    for row in read_jsonl(text_path):
        vector = cache.load(row["text"])
        require(vector is not None, f"SkillRouter embedding warm cache miss: {row['text_id']}")
        vectors[row["text_id"]] = vector
    cache_seconds = time.perf_counter() - cache_started
    scoring_started = time.perf_counter()
    observed_rows = score_skillrouter_embedding_payload(payload, vectors, prompts)
    for observed in observed_rows:
        key = (observed["representation"], observed["prompt_id"])
        require(key in expected, f"Unexpected SkillRouter embedding warm row: {key}")
        require_b1_equal(observed, expected[key], f"skillrouter-embedding/{key[0]}/{key[1]}")
        for field in SKILLROUTER_EMBEDDING_SENSITIVITY_FIELDS:
            require(observed[field] == expected[key][field], f"SkillRouter embedding warm metadata mismatch: {key}/{field}")
    require(len(observed_rows) == len(expected), "SkillRouter embedding warm matrix is incomplete")
    return {
        "manifests": 1,
        "rows_verified": len(observed_rows),
        "cache_entries_verified": len(vectors),
        "cache_load_seconds": cache_seconds,
        "warm_scoring_seconds": time.perf_counter() - scoring_started,
        "network_calls": 0,
        "model_forwards": 0,
    }


def skillrouter_scientific_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scientific_rows: list[dict[str, Any]] = []
    for row in rows:
        aggregation_seconds = row.get("rerank_aggregation_seconds")
        require(
            isinstance(aggregation_seconds, (int, float))
            and not isinstance(aggregation_seconds, bool)
            and math.isfinite(float(aggregation_seconds))
            and float(aggregation_seconds) >= 0.0,
            "SkillRouter cold row lacks valid aggregation timing",
        )
        scientific_rows.append(
            {
                key: value
                for key, value in row.items()
                if key != "rerank_aggregation_seconds"
            }
        )
    return scientific_rows


def verify_skillrouter(root: Path, manifest_paths: list[Path]) -> dict[str, Any]:
    skillrouter_manifests = [path for path in manifest_paths if read_json(path).get("schema_version") == "rq2b-skillrouter-run-manifest-v1"]
    require(len(skillrouter_manifests) == 1, "SkillRouter warm verification requires exactly one complete run")
    manifest_path = skillrouter_manifests[0]
    manifest = read_json(manifest_path)
    require(manifest.get("state") == "complete_scientific_b2", "SkillRouter warm run is incomplete")
    require(manifest.get("version_id") == VERSION_ID, "SkillRouter warm run version mismatch")
    payload_path = root / manifest["payload_path"]
    require(sha256_file(payload_path) == manifest["payload_sha256"], "SkillRouter warm payload drift")
    payload = read_json(payload_path)
    windows_path = root / payload["window_inventory"]["path"]
    pairs_path = root / payload["pair_inventory"]["path"]
    conditions_path = root / payload["condition_inventory"]["path"]
    for path, artifact in (
        (windows_path, payload["window_inventory"]),
        (pairs_path, payload["pair_inventory"]),
        (conditions_path, payload["condition_inventory"]),
    ):
        require(sha256_file(path) == artifact["sha256"], f"SkillRouter warm payload artifact drift: {path}")
    result_path = root / manifest["artifacts"]["rows"]["path"]
    require(sha256_file(result_path) == manifest["artifacts"]["rows"]["sha256"], "SkillRouter warm result drift")
    expected_rows = read_jsonl(result_path)

    cache = WindowScoreCache(root / "skill_benchmark/cache/rq2b/reranker")
    window_scores: dict[str, float] = {}
    started = time.perf_counter()
    for window in read_jsonl(windows_path):
        score = cache.load(
            representation=window["representation"],
            query=window["query"],
            document_window=window["document_window"],
        )
        require(score is not None, f"SkillRouter warm cache miss: {window['window_id']}")
        window_scores[window["window_id"]] = score
    pair_scores: dict[str, dict[str, float]] = {}
    for pair in read_jsonl(pairs_path):
        scores = [window_scores[window_id] for window_id in pair["window_ids"]]
        pair_scores[pair["pair_id"]] = {
            "maximum_window_score": max(scores),
            "mean_window_score": sum(scores) / len(scores),
        }
    prompt_path = root / payload["prompt_manifest"]["path"]
    prompt_by_id = {row["prompt_id"]: row for row in read_jsonl(prompt_path)}
    observed_rows = [
        rerank_one(condition, pair_scores, prompt_by_id[condition["prompt_id"]])
        for condition in read_jsonl(conditions_path)
    ]
    verify_denominator_identity(observed_rows)
    expected_scientific_rows = skillrouter_scientific_rows(expected_rows)
    require(
        observed_rows == expected_scientific_rows,
        "SkillRouter warm rerank scientific rows differ from the cold run",
    )
    return {
        "manifests": 1,
        "rows_verified": len(observed_rows),
        "window_scores_verified": len(window_scores),
        "warm_rerank_seconds": time.perf_counter() - started,
        "network_calls": 0,
        "model_forwards": 0,
    }


def run(root: Path, b1_root: Path, b2_root: Path, output_path: Path) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    require(not output_path.exists(), f"Refusing to overwrite warm verification: {output_path}")
    prompts = annotate_warm_prompts(
        read_jsonl(version_root(root) / "prompt_manifest.jsonl"),
        read_jsonl(version_root(root) / "source_manifest.jsonl"),
    )
    b1_manifests = sorted(b1_root.glob("*/manifest.json"))
    b2_manifests = sorted(b2_root.glob("*/manifest.json"))
    report = {
        "schema_version": "rq2b-warm-state-verification-v1",
        "version_id": VERSION_ID,
        "state": "complete_zero_external_calls_zero_model_forwards",
        "network_calls": 0,
        "api_calls": 0,
        "model_forwards": 0,
        "bm25": verify_bm25(root, b1_manifests, prompts),
        "qwen": verify_qwen(root, b1_manifests, prompts),
        "skillrouter_embedding": verify_skillrouter_embedding(root, b1_manifests, prompts),
        "skillrouter": verify_skillrouter(root, b2_manifests),
        "inputs": {
            "b1_manifests": [
                {"path": relative(path, root), "sha256": sha256_file(path)}
                for path in b1_manifests
            ],
            "b2_manifests": [
                {"path": relative(path, root), "sha256": sha256_file(path)}
                for path in b2_manifests
            ],
        },
    }
    write_json_new(output_path, report)
    return report


def self_test() -> dict[str, Any]:
    index = GlobalBM25(
        ["a", "b"],
        ["alpha exact document", "beta nearby document"],
    )
    restored = GlobalBM25.from_persisted(index.persisted_index())
    require(index.rank("alpha document") == restored.rank("alpha document"), "Warm BM25 self-test failed")
    top_entry = {
        "rank": 1,
        "skill_id": "a",
        "score": 0.75,
        "destination_class": "strict_gold",
    }
    expected = {"strict_gold_rank": 1, "top_100": [top_entry]}
    observed = {"strict_gold_rank": 1, "top_100": [dict(top_entry)]}
    for field in INVARIANT_B1_FIELDS:
        expected.setdefault(field, 1 if "rank" not in field and "skill_ids" not in field else [] if "skill_ids" in field else 1)
        observed[field] = expected[field]
    require_b1_equal(observed, expected, "synthetic")
    score_drift_rejected: dict[str, bool] = {}
    for retriever in ("bm25", "qwen", "skillrouter_embedding"):
        drifted = json.loads(json.dumps(observed))
        drifted["top_100"][0]["score"] += 1e-6
        rejected = False
        try:
            require_b1_equal(drifted, expected, f"synthetic-{retriever}")
        except ValueError:
            rejected = True
        require(rejected, f"Warm {retriever} score-drift self-test failed")
        score_drift_rejected[retriever] = rejected
    destination_drift = json.loads(json.dumps(observed))
    destination_drift["top_100"][0]["destination_class"] = "background_unrelated"
    destination_drift_rejected = False
    try:
        require_b1_equal(destination_drift, expected, "synthetic-destination")
    except ValueError:
        destination_drift_rejected = True
    require(destination_drift_rejected, "Warm destination-class drift self-test failed")
    raw_public_prompt = {
        "prompt_id": "public-equivalent",
        "stratum": "public-gold",
        "group": "synthetic",
        "prompt_sha256": "f" * 64,
        "gold_skill": "authored",
        "valid_skills": ["authored"],
        "closest_alternatives": [],
    }
    public_sources = [
        {
            "skill_id": "authored",
            "source_name": "Shared capability",
            "source_policy": "authored_skill",
        },
        {
            "skill_id": "public-copy",
            "source_name": "Shared capability",
            "source_policy": "public_original",
        },
    ]
    annotated_public_prompt = annotate_warm_prompts(
        [raw_public_prompt],
        public_sources,
    )[0]
    require(
        annotated_public_prompt["unresolved_public_equivalents"] == ["public-copy"],
        "Warm unresolved-public-equivalent annotation self-test failed",
    )
    unresolved_equivalent_roundtrip: dict[str, bool] = {}
    unresolved_destination_drift_rejected: dict[str, bool] = {}
    public_ranking = [("public-copy", 0.9), ("authored", 0.8)]
    for retriever in ("bm25", "qwen-max-chunk", "skillrouter-embedding"):
        cold_row = rank_row(
            annotated_public_prompt,
            public_ranking,
            representation="i1-discovery",
            query_seconds=0.0,
            retriever=retriever,
        )
        warm_row = rank_row(
            annotated_public_prompt,
            public_ranking,
            representation="i1-discovery",
            query_seconds=0.0,
            retriever=retriever,
        )
        require_b1_equal(warm_row, cold_row, f"synthetic-unresolved-{retriever}")
        unresolved_equivalent_roundtrip[retriever] = True
        drifted_public = json.loads(json.dumps(warm_row))
        drifted_public["top_100"][0]["destination_class"] = "background_unrelated"
        rejected = False
        try:
            require_b1_equal(
                drifted_public,
                cold_row,
                f"synthetic-unresolved-drift-{retriever}",
            )
        except ValueError:
            rejected = True
        require(rejected, f"Warm unresolved destination drift self-test failed: {retriever}")
        unresolved_destination_drift_rejected[retriever] = rejected
    cold_skillrouter = [{"prompt_id": "p1", "score": 1.0, "rerank_aggregation_seconds": 0.01}]
    warm_skillrouter = [{"prompt_id": "p1", "score": 1.0}]
    require(
        skillrouter_scientific_rows(cold_skillrouter) == warm_skillrouter,
        "Warm SkillRouter runtime-field exclusion self-test failed",
    )
    return {
        "state": "synthetic_warm_verification_only",
        "network_calls": 0,
        "api_calls": 0,
        "model_forwards": 0,
        "bm25_persisted_roundtrip": True,
        "bm25_score_only_drift_rejected": score_drift_rejected["bm25"],
        "qwen_score_only_drift_rejected": score_drift_rejected["qwen"],
        "skillrouter_embedding_score_only_drift_rejected": score_drift_rejected["skillrouter_embedding"],
        "destination_class_drift_rejected": destination_drift_rejected,
        "bm25_unresolved_equivalent_roundtrip": unresolved_equivalent_roundtrip["bm25"],
        "qwen_unresolved_equivalent_roundtrip": unresolved_equivalent_roundtrip["qwen-max-chunk"],
        "skillrouter_embedding_unresolved_equivalent_roundtrip": unresolved_equivalent_roundtrip["skillrouter-embedding"],
        "bm25_unresolved_destination_drift_rejected": unresolved_destination_drift_rejected["bm25"],
        "qwen_unresolved_destination_drift_rejected": unresolved_destination_drift_rejected["qwen-max-chunk"],
        "skillrouter_embedding_unresolved_destination_drift_rejected": unresolved_destination_drift_rejected["skillrouter-embedding"],
        "skillrouter_runtime_field_excluded": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--b1-root", type=Path, default=Path("skill_benchmark/outputs/rq2b/b1"))
    parser.add_argument("--b2-root", type=Path, default=Path("skill_benchmark/outputs/rq2b/b2"))
    parser.add_argument("--output", type=Path, default=Path("skill_benchmark/outputs/rq2b/analysis/warm_state_verification.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        root = args.root.resolve()
        b1_root = args.b1_root if args.b1_root.is_absolute() else root / args.b1_root
        b2_root = args.b2_root if args.b2_root.is_absolute() else root / args.b2_root
        output = args.output if args.output.is_absolute() else root / args.output
        result = run(root, b1_root, b2_root, output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
