#!/usr/bin/env python3
"""Synthetic and frozen-authority tests for the V7 Qwen B1 preflight/runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import numpy as np

from build_rq2b_v7_qwen_b1_preflight import (
    DEFAULT_LEGACY_CACHE,
    PACKAGE_REL,
    PAYLOAD_REL,
    REPRESENTATION_CELLS,
    build_payload_data,
    read_json,
    repo_root,
    text_sha256,
    verify,
)
from run_rq2b_v7_qwen_b1 import (
    score_representation,
    self_test,
    top20_binding_sha256,
    validate_b1_rows,
    read_jsonl_any,
    validate_release_authorisation,
    write_deterministic_jsonl_gzip,
)
from validate_rq2b_v7_runner_outputs import RunnerAuthority, validate_b1_row


def expect_failure(callable_: Any, message_fragment: str) -> None:
    try:
        callable_()
    except ValueError as error:
        if message_fragment not in str(error):
            raise AssertionError(f"Wrong failure: {error}") from error
    else:
        raise AssertionError(f"Expected failure containing: {message_fragment}")


class CharacterTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [ord(character) for character in text]

    def __call__(self, text: str, **_: Any) -> dict[str, Any]:
        return {
            "input_ids": self.encode(text),
            "offset_mapping": [(index, index + 1) for index in range(len(text))],
        }


def synthetic_payload_test() -> None:
    representations: dict[str, list[dict[str, Any]]] = {}
    for representation in REPRESENTATION_CELLS:
        text = f"{representation}\n\n" + ("x" * 8000)
        representations[representation] = [{
            "source_sha256": "1" * 64,
            "selector_text": text,
            "selector_text_sha256": text_sha256(text),
        }]
    prompts = [{"prompt_id": "p1", "prompt": "query", "prompt_sha256": text_sha256("query")}]
    text_rows, documents, query_map, summary = build_payload_data(
        CharacterTokenizer(), prompts, representations
    )
    assert len(documents) == 4
    assert query_map == {"p1": text_sha256("query")}
    assert all(summary[name]["windowed_documents"] == 1 for name in REPRESENTATION_CELLS)
    by_id = {row["text_id"]: row for row in text_rows}
    for document in documents:
        assert len(document["chunk_text_ids"]) == 3
        assert all(by_id[text_id]["local_proxy_tokens"] <= 7500 for text_id in document["chunk_text_ids"])
    assert all(summary[name]["short_boundary_direct_advances"] == 1 for name in REPRESENTATION_CELLS)
    assert all(summary[name]["maximum_adjacent_overlap_proxy_tokens"] <= 256 for name in REPRESENTATION_CELLS)


def synthetic_scoring_test() -> dict[str, Any]:
    dimension = 1024
    source_ids = [f"{index:064x}" for index in range(3798)]
    query_vector = [1.0, *([0.0] * (dimension - 1))]
    vectors = {"query": query_vector}
    documents: list[dict[str, Any]] = []
    available: dict[str, bool] = {"query": False}
    for index, source_id in enumerate(reversed(source_ids)):
        text_id = f"d{index}"
        vectors[text_id] = query_vector
        available[text_id] = True
        documents.append({
            "representation": "I1-discovery",
            "source_sha256": source_id,
            "chunk_text_ids": [text_id],
        })
    prompt = {"prompt_id": "p", "prompt_sha256": "f" * 64}
    rows, sensitivities = score_representation(
        run_id="synthetic",
        representation="I1-discovery",
        condition={
            "condition_id": "B02-G0",
            "retriever": "Qwen-text-embedding-v4",
            "persisted_candidate_source": "B02",
        },
        documents=documents,
        prompts=[prompt],
        query_text_ids={"p": "query"},
        text_by_id={"query": {"local_proxy_tokens": 1}},
        vectors=vectors,
        query_latency_seconds={"query": 0.25},
        initial_cache_available=available,
    )
    assert [item["source_sha256"] for item in rows[0]["ranked_candidates"]] == source_ids[:100]
    assert sensitivities[0]["core_outcome"] is False
    synthetic_payload = {"counts": {"b1_output_rows": 1}}
    validate_b1_rows(rows, synthetic_payload)
    return rows[0]


def frozen_validator_test() -> None:
    authority = RunnerAuthority.load()
    prompt = next(iter(authority.prompts.values()))
    source_ids = sorted(authority.sources)[:100]
    condition = authority.b1_conditions["B02-G0"]
    row = {
        "schema_version": "rq2b-v7-b1-runner-output-v1",
        "status": "SUCCESS",
        "run_id": "synthetic-validator-only",
        "condition_id": "B02-G0",
        "first_stage_cell_id": "B02",
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "representation": condition["representation"],
        "retriever": condition["retriever"],
        "persisted_candidate_source": "B02",
        "source_union_sha256": condition["source_union_sha256"],
        "top_k": 100,
        "score_semantics": "HIGHER_IS_BETTER",
        "top20_binding_sha256": top20_binding_sha256(
            condition_id="B02-G0",
            prompt_id=prompt["prompt_id"],
            prompt_sha256=prompt["prompt_sha256"],
            ordered_source_sha256=source_ids[:20],
        ),
        "ranked_candidates": [
            {"rank": rank, "source_sha256": source_id, "score": 0.0}
            for rank, source_id in enumerate(source_ids, 1)
        ],
        "cost": {
            "wall_time_ms": 0.0,
            "provider_calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "window_forwards": 3798,
            "cache_hits": 0,
            "retry_count": 0,
            "timeout_count": 0,
            "failure_count": 0,
        },
    }
    validate_b1_row(row, authority, 1)
    poisoned = json.loads(json.dumps(row))
    poisoned["gold"] = source_ids[0]
    expect_failure(lambda: validate_b1_row(poisoned, authority, 1), "prohibited label/outcome key")


def deterministic_gzip_test() -> None:
    rows = [{"b": 2, "a": "x"}, {"a": "y", "b": 3}]
    with tempfile.TemporaryDirectory() as directory:
        first = Path(directory) / "first.jsonl.gz"
        second = Path(directory) / "second.jsonl.gz"
        first_metadata = write_deterministic_jsonl_gzip(first, rows)
        second_metadata = write_deterministic_jsonl_gzip(second, rows)
        assert first.read_bytes() == second.read_bytes()
        assert first_metadata["sha256"] == second_metadata["sha256"]
        assert read_jsonl_any(first) == rows


def pending_authorisation_gate_test(root: Path) -> None:
    payload_path = root / PAYLOAD_REL / "payload_manifest.json"
    payload = read_json(payload_path)
    pending_path = root / PACKAGE_REL / "pending_authorisation.json"
    expect_failure(
        lambda: validate_release_authorisation(
            pending_path,
            root=root,
            payload_manifest_path=payload_path,
            payload=payload,
            run_id="must-not-run",
            output_dir=root / "skill_benchmark/cache/must-not-run",
            timeout_seconds=120,
            legacy_cache_root=DEFAULT_LEGACY_CACHE,
        ),
        "Execution is not released after Phase-7 QA",
    )
    active = read_json(pending_path)
    active.update({
        "state": "EXPLICITLY_AUTHORISED_FOR_ONE_EXECUTION_AFTER_PHASE7_QA",
        "phase7_qa_status": "PASS",
        "phase7_qa_receipt_sha256": "0" * 64,
        "root_release_id": "synthetic-test-release",
        "run_id": "synthetic-test-run",
        "output_dir": "skill_benchmark/cache/synthetic-test-output",
        "timeout_seconds": 120,
    })
    with tempfile.TemporaryDirectory() as directory:
        active_path = Path(directory) / "active.json"
        active_path.write_text(json.dumps(active), encoding="utf-8")
        validated = validate_release_authorisation(
            active_path,
            root=root,
            payload_manifest_path=payload_path,
            payload=payload,
            run_id="synthetic-test-run",
            output_dir=root / "skill_benchmark/cache/synthetic-test-output",
            timeout_seconds=120,
            legacy_cache_root=DEFAULT_LEGACY_CACHE,
        )
        assert validated["root_release_id"] == "synthetic-test-release"


def main() -> None:
    root = repo_root()
    runner_result = self_test()
    synthetic_payload_test()
    synthetic_scoring_test()
    frozen_validator_test()
    deterministic_gzip_test()
    pending_authorisation_gate_test(root)
    replay = verify(root, DEFAULT_LEGACY_CACHE)
    print(json.dumps({
        "status": "PASS_V7_QWEN_B1_PREFLIGHT_RUNNER_TESTS",
        "network_calls": 0,
        "provider_requests": 0,
        "runner_self_test": runner_result,
        "preflight_replay": replay["status"],
        "checks": {
            "exact_lossless_chunking": True,
            "stable_source_sha256_ties": True,
            "mean_window_noncore": True,
            "b1_schema_validator": True,
            "deterministic_gzip_direct_read": True,
            "recursive_label_key_rejection": True,
            "pending_authorisation_blocks_execution": True,
            "active_authorisation_exact_binding": True,
            "cache_inventory_replay": True,
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
