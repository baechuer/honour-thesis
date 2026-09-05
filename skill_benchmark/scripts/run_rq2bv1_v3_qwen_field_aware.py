#!/usr/bin/env python3
"""Run one separately authorised RQ2b V3 Qwen B1E-F field-aware retrieval.

Only the seven frozen candidate-field blocks may be sent to Qwen.  Raw-query
vectors are read from the verified Qwen-primary exact-text cache; a missing
query vector fails closed rather than transmitting a query again.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path
from typing import Any

from prepare_rq2bv1_v3_qwen_field_aware_preflight import (
    CACHE_ROOT,
    FIELD_COMPONENT_REPRESENTATION,
    FIELD_ORDER,
    PACKET_NAME,
    PAYLOAD_NAME,
    PREFLIGHT_ROOT,
    REPORT_NAME,
    RESULT_ROOT,
    RUN_ID,
    TIMEOUT_SECONDS,
)
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new
from run_rq2b_qwen import DIMENSIONS, ExactEmbeddingCache, embed_texts


RUNNER_VERSION = "rq2bv1-v3-qwen-field-aware-runner-v1"
RESULT_SCHEMA = "rq2bv1-v3-b1e-f-strict-result-row-v1"
DEFAULT_AUTHORISATION = "skill_benchmark/rq2bv1/approvals/qwen_field_aware_v3_execution_authorisation.json"


def _path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _packet(root: Path) -> tuple[Path, dict[str, Any]]:
    path = root / PREFLIGHT_ROOT / PACKET_NAME
    packet = read_json(path)
    require(packet.get("schema_version") == "rq2bv1-v3-qwen-field-aware-execution-approval-packet-v1", "B1E-F packet schema drift")
    require(packet.get("state") == "awaiting_explicit_external_transfer_authorisation", "B1E-F packet is not awaiting approval")
    return path, packet


def _validate_preflight(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    preflight_root = root / PREFLIGHT_ROOT
    payload_path, report_path = preflight_root / PAYLOAD_NAME, preflight_root / REPORT_NAME
    payload, report = read_json(payload_path), read_json(report_path)
    require(payload.get("schema_version") == "rq2bv1-v3-qwen-field-aware-payload-v1", "B1E-F payload schema drift")
    require(payload.get("state") == "sealed_not_executed", "B1E-F payload is not sealed")
    require(report.get("state") == "preflight_passed_no_network_no_scoring_external_authorisation_required", "B1E-F preflight does not pass")
    require(report["payload"] == {"path": relative(payload_path, root), "sha256": sha256_file(payload_path)}, "B1E-F report/payload drift")
    require(payload["strict_population"] == {"candidate_library_skills": 2433, "strict_prompts": 381, "expected_result_rows": 381}, "B1E-F population drift")
    require(payload["field_components"] == {
        "representation": FIELD_COMPONENT_REPRESENTATION,
        "field_order": list(FIELD_ORDER),
        "empty_field_serialization": "<field label>:\\n",
        "present_field_serialization": "<field label>:\\n- <exact selector evidence>...",
        "candidate_tie_break": "skill_id_ascending",
        "aggregation": "mean_of_descending_top_two_of_seven_cosines",
        "source_representation": "i3c-fielded-evidence",
    }, "B1E-F field method drift")
    for binding_key, label in (
        ("i3c_fielded_artifact", "I3C fielded source artifact"),
        ("query_cache_binding", None),
    ):
        if binding_key == "query_cache_binding":
            for nested_key, nested_label in (
                ("primary_post_run_verification", "Qwen-primary post-run verification"),
                ("primary_result_rows", "Qwen-primary result rows"),
            ):
                binding = payload[binding_key][nested_key]
                path = _path(root, binding["path"])
                require(path.is_file() and sha256_file(path) == binding["sha256"], f"B1E-F {nested_label} drift")
        else:
            binding = payload[binding_key]
            path = _path(root, binding["path"])
            require(path.is_file() and sha256_file(path) == binding["sha256"], f"B1E-F {label} drift")
    inventory_path = _path(root, payload["text_inventory"]["path"])
    require(sha256_file(inventory_path) == payload["text_inventory"]["sha256"], "B1E-F inventory hash drift")
    texts = read_jsonl(inventory_path)
    require(len(texts) == int(payload["text_inventory"]["rows"]), "B1E-F inventory count drift")
    text_by_id = {str(row["text_id"]): row for row in texts}
    require(len(text_by_id) == len(texts), "B1E-F text IDs are not unique")
    for text_id, row in text_by_id.items():
        require(row["text_id"] == row["text_sha256"] == text_id, "B1E-F text digest drift")
        require(int(row["utf8_bytes"]) == len(str(row["text"]).encode("utf-8")), "B1E-F text byte drift")
        require(isinstance(row["roles"], list) and row["roles"], "B1E-F text roles missing")
        for role in row["roles"]:
            require(role.get("kind") == "document_chunk", "B1E-F may contain only document components")
            require(role.get("representation") == FIELD_COMPONENT_REPRESENTATION, "B1E-F role representation drift")
            require(role.get("field_key") in FIELD_ORDER, "B1E-F role field drift")
    documents = payload["documents"]
    require(len(documents) == 2433, "B1E-F candidate count drift")
    skill_ids = [str(document["skill_id"]) for document in documents]
    require(len(skill_ids) == len(set(skill_ids)), "B1E-F candidate identities are not unique")
    for document in documents:
        components = document["components"]
        require(len(components) == 7 and [component["field_key"] for component in components] == list(FIELD_ORDER), "B1E-F seven-field component drift")
        require(all(component["text_id"] in text_by_id for component in components), "B1E-F component text missing")
    prompts_path = _path(root, payload["prompt_artifact"]["path"])
    require(sha256_file(prompts_path) == payload["prompt_artifact"]["sha256"], "B1E-F prompt artifact drift")
    prompts = read_jsonl(prompts_path)
    require(len(prompts) == 381 and len({prompt["prompt_id"] for prompt in prompts}) == 381, "B1E-F prompt population drift")
    bindings = payload["query_cache_binding"]["query_vectors"]
    require(set(bindings) == {str(prompt["prompt_id"]) for prompt in prompts}, "B1E-F query-binding coverage drift")
    return payload, texts, prompts


def _validate_authorisation(root: Path, path: Path, packet_path: Path, packet: dict[str, Any]) -> dict[str, Any]:
    authorisation = read_json(path)
    require(authorisation.get("schema_version") == "rq2bv1-v3-qwen-field-aware-execution-authorisation-v1", "B1E-F authorisation schema drift")
    require(authorisation.get("state") == "explicitly_authorised_for_one_qwen_field_aware_v3_execution", "B1E-F execution is not authorised")
    require(authorisation.get("approved_packet") == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}, "B1E-F packet/authorisation drift")
    for key in ("run_id", "output_dir", "cache_root", "base_url", "model", "dimensions", "timeout_seconds", "automatic_retries", "query_external_text_submissions"):
        require(authorisation.get(key) == packet.get(key), f"B1E-F authorisation mismatch: {key}")
    for key in packet:
        if key.startswith("maximum_"):
            require(authorisation.get(key) == packet[key], f"B1E-F authorisation cap mismatch: {key}")
    require(authorisation.get("thesis_result_writing_authorised") is False, "B1E-F cannot write thesis results")
    require(authorisation.get("execution_scripts") == packet.get("execution_scripts"), "B1E-F execution script binding drift")
    for script in packet["execution_scripts"]:
        script_path = _path(root, script["path"])
        require(script_path.is_file() and sha256_file(script_path) == script["sha256"], f"B1E-F script hash drift: {script['path']}")
    return authorisation


def _normalize(values: Any) -> Any:
    import numpy as np

    matrix = np.asarray(values, dtype=np.float64)
    norms = np.linalg.norm(matrix, axis=-1, keepdims=True)
    require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0.0)), "Invalid B1E-F vector norm")
    return matrix / norms


def _query_vectors(payload: dict[str, Any], prompts: list[dict[str, Any]], cache: ExactEmbeddingCache) -> tuple[dict[str, Any], dict[str, float]]:
    vectors: dict[str, Any] = {}
    timings: dict[str, float] = {}
    bindings = payload["query_cache_binding"]["query_vectors"]
    for prompt in prompts:
        prompt_id = str(prompt["prompt_id"])
        binding = bindings[prompt_id]
        require(binding["prompt_sha256"] == prompt["prompt_sha256"], f"B1E-F prompt binding drift: {prompt_id}")
        require(binding["query_text_sha256"] == __import__("hashlib").sha256(str(prompt["prompt"]).encode("utf-8")).hexdigest(), f"B1E-F query text digest drift: {prompt_id}")
        vector = cache.load(str(prompt["prompt"]))
        require(vector is not None, f"B1E-F cached query vector missing: {prompt_id}")
        vectors[prompt_id] = _normalize(vector)
        timings[prompt_id] = float(binding["reused_primary_cold_query_embedding_seconds"])
    return vectors, timings


def _result_row(
    prompt: dict[str, Any], ranking: list[tuple[str, float]], component_scores: dict[str, list[float]], *, search_seconds: float,
    selector_visible_tokens: int, document_embedding_seconds: float, cold_query_seconds: float,
) -> dict[str, Any]:
    rank_by_id = {skill_id: index for index, (skill_id, _) in enumerate(ranking, start=1)}
    gold_rank = int(rank_by_id[prompt["gold_skill"]])
    top100 = ranking[:100]
    row = {
        "schema_version": RESULT_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "retriever": "qwen-text-embedding-v4-field-aware",
        "representation": FIELD_COMPONENT_REPRESENTATION,
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "strict_gold_rank": gold_rank,
        "strict_hit_at_1": int(gold_rank == 1),
        "strict_recall_at_5": int(gold_rank <= 5),
        "strict_recall_at_20": int(gold_rank <= 20),
        "strict_recall_at_50": int(gold_rank <= 50),
        "strict_recall_at_100": int(gold_rank <= 100),
        "strict_mrr_at_10": 0.0 if gold_rank > 10 else 1.0 / gold_rank,
        "top_5_skill_ids": [skill_id for skill_id, _ in ranking[:5]],
        "top_20_skill_ids": [skill_id for skill_id, _ in ranking[:20]],
        "top_50_skill_ids": [skill_id for skill_id, _ in ranking[:50]],
        "top_100": [{"rank": index, "skill_id": skill_id, "score": float(score)} for index, (skill_id, score) in enumerate(top100, start=1)],
        "query_seconds": float(search_seconds),
        "selector_visible_tokens": int(selector_visible_tokens),
        "one_time_document_embedding_or_index_seconds": float(document_embedding_seconds),
        "retriever_metadata": {
            "model": "text-embedding-v4", "dimensions": DIMENSIONS,
            "field_order": list(FIELD_ORDER), "aggregation": "mean_of_descending_top_two_of_seven_cosines",
            "candidate_tie_break": "skill_id_ascending", "field_components_per_candidate": 7,
            "cold_query_embedding_seconds_reused_from_qwen_primary": float(cold_query_seconds),
            "top_100_component_scores": [
                {"skill_id": skill_id, "field_scores": component_scores[skill_id]} for skill_id, _ in top100
            ],
        },
    }
    _validate_row(row, prompt)
    return row


def _validate_row(row: dict[str, Any], prompt: dict[str, Any]) -> None:
    expected = {
        "schema_version", "runner_version", "retriever", "representation", "prompt_id", "prompt_sha256", "stratum", "group", "gold_skill",
        "strict_gold_rank", "strict_hit_at_1", "strict_recall_at_5", "strict_recall_at_20", "strict_recall_at_50", "strict_recall_at_100", "strict_mrr_at_10",
        "top_5_skill_ids", "top_20_skill_ids", "top_50_skill_ids", "top_100", "query_seconds", "selector_visible_tokens", "one_time_document_embedding_or_index_seconds", "retriever_metadata",
    }
    require(set(row) == expected, "B1E-F result row schema drift")
    for key in ("prompt_id", "prompt_sha256", "stratum", "group", "gold_skill"):
        require(row[key] == prompt[key], f"B1E-F prompt mismatch: {key}")
    require(row["schema_version"] == RESULT_SCHEMA and row["runner_version"] == RUNNER_VERSION, "B1E-F result version drift")
    require(row["retriever"] == "qwen-text-embedding-v4-field-aware" and row["representation"] == FIELD_COMPONENT_REPRESENTATION, "B1E-F result method drift")
    rank = int(row["strict_gold_rank"])
    require(1 <= rank <= 2433, "B1E-F gold rank out of range")
    require(row["strict_hit_at_1"] == int(rank == 1) and row["strict_recall_at_20"] == int(rank <= 20), "B1E-F metric drift")
    top100 = row["top_100"]
    require(isinstance(top100, list) and len(top100) == 100 and [item["rank"] for item in top100] == list(range(1, 101)), "B1E-F Top-100 drift")
    ids = [item["skill_id"] for item in top100]
    require(len(ids) == len(set(ids)) and row["top_5_skill_ids"] == ids[:5] and row["top_20_skill_ids"] == ids[:20] and row["top_50_skill_ids"] == ids[:50], "B1E-F prefix drift")
    metadata = row["retriever_metadata"]
    require(metadata["field_order"] == list(FIELD_ORDER) and metadata["field_components_per_candidate"] == 7, "B1E-F metadata drift")
    scores = metadata["top_100_component_scores"]
    require(len(scores) == 100 and [item["skill_id"] for item in scores] == ids and all(len(item["field_scores"]) == 7 for item in scores), "B1E-F component-score persistence drift")


def _score(payload: dict[str, Any], vectors: dict[str, list[float]], prompts: list[dict[str, Any]], cache: ExactEmbeddingCache, document_seconds: float) -> list[dict[str, Any]]:
    import numpy as np

    documents = payload["documents"]
    skill_ids = [str(document["skill_id"]) for document in documents]
    components = np.asarray([[vectors[component["text_id"]] for component in document["components"]] for document in documents], dtype=np.float64)
    require(components.shape == (2433, 7, DIMENSIONS), "B1E-F component matrix shape drift")
    components = _normalize(components)
    queries, cold_seconds = _query_vectors(payload, prompts, cache)
    selector_tokens = int(payload["counts"]["selector_visible_tokens"])
    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        prompt_id = str(prompt["prompt_id"])
        started = time.perf_counter()
        similarities = components @ queries[prompt_id]
        aggregate = np.sort(similarities, axis=1)[:, -2:].mean(axis=1)
        ranking_indices = sorted(range(len(skill_ids)), key=lambda index: (-float(aggregate[index]), skill_ids[index]))
        ranking = [(skill_ids[index], float(aggregate[index])) for index in ranking_indices]
        details = {skill_ids[index]: [float(value) for value in similarities[index]] for index in ranking_indices[:100]}
        rows.append(_result_row(prompt, ranking, details, search_seconds=time.perf_counter() - started, selector_visible_tokens=selector_tokens, document_embedding_seconds=document_seconds, cold_query_seconds=cold_seconds[prompt_id]))
    require(len(rows) == 381, "B1E-F result row count drift")
    return rows


def _warm_replay(payload: dict[str, Any], cache: ExactEmbeddingCache, texts: list[dict[str, Any]], prompts: list[dict[str, Any]], rows: list[dict[str, Any]], document_seconds: float) -> dict[str, Any]:
    vectors = {str(text["text_id"]): cache.load(str(text["text"])) for text in texts}
    require(all(vector is not None for vector in vectors.values()), "B1E-F warm cache coverage is incomplete")
    replay = _score(payload, {key: value for key, value in vectors.items() if value is not None}, prompts, cache, document_seconds)
    expected = {row["prompt_id"]: row for row in rows}
    actual = {row["prompt_id"]: row for row in replay}
    require(set(actual) == set(expected), "B1E-F warm replay coverage drift")
    for prompt_id in expected:
        require(actual[prompt_id]["top_100"] == expected[prompt_id]["top_100"] and actual[prompt_id]["strict_gold_rank"] == expected[prompt_id]["strict_gold_rank"], f"B1E-F warm ranking drift: {prompt_id}")
    return {"verified_conditions": len(replay)}


def run(root: Path, authorisation_path: Path, api_key_env: str) -> dict[str, Any]:
    payload, texts, prompts = _validate_preflight(root)
    packet_path, packet = _packet(root)
    authorisation = _validate_authorisation(root, authorisation_path, packet_path, packet)
    output_root = root / str(packet["output_dir"])
    staging = output_root.with_name(f".{output_root.name}.staging")
    require(not output_root.exists() and not staging.exists(), "Refusing to overwrite or resume B1E-F scientific output")
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), "Qwen API key environment variable is missing")
    staging.mkdir(parents=True, exist_ok=False)
    write_json_new(staging / "run_started.json", {
        "schema_version": "rq2bv1-v3-qwen-field-aware-run-start-v1", "run_id": packet["run_id"],
        "payload": {"path": relative(root / PREFLIGHT_ROOT / PAYLOAD_NAME, root), "sha256": sha256_file(root / PREFLIGHT_ROOT / PAYLOAD_NAME)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": sha256_file(authorisation_path)},
        "automatic_retries": 0, "query_external_text_submissions": 0,
    })
    progress_root = staging / "request_records"
    progress_root.mkdir(parents=False, exist_ok=False)
    cache = ExactEmbeddingCache(root / str(packet["cache_root"]))
    vectors, ledger = embed_texts(
        texts, cache=cache, api_key=api_key,
        authorisation={
            "maximum_new_texts": int(authorisation["maximum_new_cache_texts"]), "maximum_successful_calls": int(authorisation["maximum_successful_api_calls"]),
            "maximum_request_attempts": int(authorisation["maximum_request_attempts"]), "maximum_local_proxy_tokens": int(authorisation["maximum_new_cache_proxy_tokens"]),
            "maximum_new_utf8_bytes": int(authorisation["maximum_new_cache_utf8_bytes"]), "maximum_external_text_submissions": int(authorisation["maximum_external_text_submissions"]),
            "maximum_external_submission_proxy_tokens": int(authorisation["maximum_external_submission_proxy_tokens"]), "maximum_external_submission_utf8_bytes": int(authorisation["maximum_external_submission_utf8_bytes"]),
            "maximum_cold_query_requests": 0,
        }, timeout_seconds=int(authorisation["timeout_seconds"]), progress_root=progress_root,
    )
    require(ledger["automatic_retries"] == 0 and ledger["cold_query_requests"] == 0 and ledger["external_text_submissions"] <= int(authorisation["maximum_external_text_submissions"]), "B1E-F execution boundary drift")
    require(int(ledger["provider_usage"].get("prompt_tokens", 0)) <= int(authorisation["maximum_provider_prompt_tokens"]), "B1E-F provider-token ceiling exceeded")
    document_seconds = sum(float(record["request_seconds"]) for record in ledger["request_records"])
    rows = _score(payload, vectors, prompts, cache, document_seconds)
    warm = _warm_replay(payload, cache, texts, prompts, rows, document_seconds)
    rows_path, ledger_path = staging / "qwen_field_aware_strict_results.jsonl", staging / "embedding_ledger.json"
    write_jsonl_new(rows_path, rows)
    ledger["reused_query_embeddings"] = 381
    ledger["query_external_text_submissions"] = 0
    write_json_new(ledger_path, ledger)
    manifest = {
        "schema_version": "rq2bv1-v3-qwen-field-aware-run-manifest-v1", "state": "qwen_field_aware_completed_pending_user_result_review",
        "run_id": packet["run_id"], "runner_version": RUNNER_VERSION,
        "method": {"retriever": "qwen-text-embedding-v4-field-aware", "representation": FIELD_COMPONENT_REPRESENTATION, "aggregation": "uniform_top_two", "field_aware": True, "reranking": False},
        "payload": {"path": relative(root / PREFLIGHT_ROOT / PAYLOAD_NAME, root), "sha256": sha256_file(root / PREFLIGHT_ROOT / PAYLOAD_NAME)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": sha256_file(authorisation_path)},
        "embedding_ledger": {"path": relative(output_root / ledger_path.name, root), "sha256": sha256_file(ledger_path)},
        "document_embedding_seconds": document_seconds, "warm_replay": warm,
        "artifacts": {
            "rows": {"path": relative(output_root / rows_path.name, root), "sha256": sha256_file(rows_path), "rows": len(rows)},
            "request_records": [{"path": relative(output_root / "request_records" / item.name, root), "sha256": sha256_file(item)} for item in sorted(progress_root.glob("*.json"))],
        }, "network_calls": ledger["successful_api_calls"], "thesis_result_writing": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.rename(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    import numpy as np

    # Keep the second field unit-normalised at cosine 0.9.  A raw [0.9, 0]
    # vector would normalise to [1, 0] and would not test top-two averaging.
    fields = np.asarray([[1.0, 0.0], [0.9, math.sqrt(1.0 - 0.9**2)], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
    query = np.asarray([1.0, 0.0])
    scores = np.sort((_normalize(fields) @ _normalize(query)), axis=0)[-2:].mean()
    require(abs(float(scores) - 0.95) <= 1e-12, "B1E-F top-two aggregation self-test failed")
    return {"schema_version": "rq2bv1-v3-qwen-field-aware-runner-self-test-v1", "state": "self_test_passed_no_external_call", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--authorisation", type=Path, default=Path(DEFAULT_AUTHORISATION))
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    args = parser.parse_args()
    require(args.self_test != args.execute, "choose exactly one of --self-test or --execute")
    output = self_test() if args.self_test else run(args.root.resolve(), _path(args.root.resolve(), args.authorisation), args.api_key_env)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
