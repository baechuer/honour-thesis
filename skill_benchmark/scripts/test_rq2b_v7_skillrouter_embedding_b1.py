#!/usr/bin/env python3
"""No-inference tests for the V7 SkillRouter embedding B1 runner."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import numpy as np

from run_rq2b_v7_skillrouter_embedding_b1 import (
    AUTHORISATION_SCHEMA,
    DIMENSIONS,
    EXPECTED_SOURCES,
    FIXED_REPRESENTATION_INPUTS,
    MODEL_MAX_TOKENS,
    QUERY_INSTRUCTION,
    REPRESENTATION_CELLS,
    ExactEmbeddingCache,
    build_work_inventory,
    cache_key,
    exact_length_batches,
    file_sha256,
    maximum_window_cosine_scores,
    normalized_vector,
    online_row_cost,
    self_test,
    text_sha256,
    top20_binding_sha256,
    validate_root_release,
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
    """Character IDs plus two deterministic model special tokens."""

    def encode(self, text: str, add_special_tokens: bool = True) -> list[int]:
        ids = [ord(character) for character in text]
        return [1, *ids, 2] if add_special_tokens else ids


def exact_window_inventory_test() -> None:
    tokenizer = CharacterTokenizer()
    representations: dict[str, list[dict[str, Any]]] = {}
    for representation in REPRESENTATION_CELLS:
        text = f"# {representation}\n\n" + ("x" * 8000)
        representations[representation] = [{
            "source_sha256": "1" * 64,
            "selector_text": text,
            "selector_text_sha256": text_sha256(text),
        }]
    prompt = "route this task"
    inventory, documents, query_ids, summary = build_work_inventory(
        tokenizer,
        [{"prompt_id": "p1", "prompt": prompt, "prompt_sha256": text_sha256(prompt)}],
        representations,
    )
    assert set(documents) == set(REPRESENTATION_CELLS)
    assert all(summary[name]["windowed_documents"] == 1 for name in REPRESENTATION_CELLS)
    assert all(summary[name]["document_windows"] >= 2 for name in REPRESENTATION_CELLS)
    for representation, rows in documents.items():
        assert len(rows) == 1, representation
        chunks = rows[0]["chunks"]
        assert chunks[0]["start_char"] == 0
        assert chunks[-1]["end_char"] == len(representations[representation][0]["selector_text"])
        assert all(chunk["content_tokens"] <= 7500 for chunk in chunks)
        assert all(chunk["model_input_tokens"] <= MODEL_MAX_TOKENS for chunk in chunks)
        assert all(chunk["model_input_tokens"] == chunk["content_tokens"] + 2 for chunk in chunks)
        assert all(chunk["content_token_ids_sha256"] != chunk["model_input_token_ids_sha256"] for chunk in chunks)
        assert all(current["start_char"] <= previous["end_char"] for previous, current in zip(chunks, chunks[1:]))
    query_item = inventory[query_ids["p1"]]
    assert query_item["text"] == QUERY_INSTRUCTION + prompt
    assert query_item["model_input_tokens"] == len(tokenizer.encode(QUERY_INSTRUCTION + prompt))
    assert query_item["content_tokens"] == len(tokenizer.encode(QUERY_INSTRUCTION + prompt, add_special_tokens=False))
    assert any(
        chunk["content_tokens"] == 7500 and chunk["model_input_tokens"] == 7502
        for rows in documents.values() for chunk in rows[0]["chunks"]
    )


def exact_batch_test() -> None:
    items = [
        {"text_id": f"id-{index:02d}", "model_input_tokens": 7502 if index < 18 else 7503}
        for index in range(21)
    ]
    batches = exact_length_batches(items)
    assert [len(batch) for batch in batches] == [16, 2, 3]
    assert all(len(batch) <= 16 for batch in batches)
    assert all(len({item["model_input_tokens"] for item in batch}) == 1 for batch in batches)


def maximum_window_test() -> None:
    first = normalized_vector([1.0, *([0.0] * (DIMENSIONS - 1))])
    second = normalized_vector([0.0, 1.0, *([0.0] * (DIMENSIONS - 2))])
    query = np.asarray(first, dtype=np.float64)
    windows = np.asarray([second, first, second], dtype=np.float64)
    # Document 1 has two windows and must receive its best (second) window.
    scores = maximum_window_cosine_scores(windows, [0, 2], query)
    assert scores.tolist() == [1.0, 0.0]


def online_cost_boundary_test() -> None:
    miss = online_row_cost(
        query_model_input_tokens=37,
        query_embedding_ms=4.5,
        scoring_ms=1.25,
        query_initial_cache_hit=False,
    )
    hit = online_row_cost(
        query_model_input_tokens=37,
        query_embedding_ms=0.0,
        scoring_ms=1.25,
        query_initial_cache_hit=True,
    )
    assert miss == {
        "wall_time_ms": 5.75,
        "provider_calls": 0,
        "input_tokens": 37,
        "output_tokens": 0,
        "window_forwards": 1,
        "cache_hits": 0,
        "retry_count": 0,
        "timeout_count": 0,
        "failure_count": 0,
    }
    assert hit["window_forwards"] == 1
    assert hit["input_tokens"] == 37
    assert hit["cache_hits"] == 1
    assert hit["wall_time_ms"] == 1.25


def cache_contract_test() -> None:
    item = {
        "text_id": text_sha256("synthetic"),
        "text": "synthetic",
        "text_sha256": text_sha256("synthetic"),
        "content_token_ids_sha256": "2" * 64,
        "content_tokens": 9,
        "model_input_token_ids_sha256": "3" * 64,
        "model_input_tokens": 11,
        "roles": [{"kind": "document_window"}],
    }
    vector = normalized_vector([1.0, *([0.0] * (DIMENSIONS - 1))])
    with tempfile.TemporaryDirectory() as directory:
        cache = ExactEmbeddingCache(Path(directory))
        path = cache.store(item, vector)
        assert path.name == f"{cache_key(item)}.json"
        assert cache.load(item) == vector
        changed = dict(item)
        changed["model_input_token_ids_sha256"] = "4" * 64
        assert cache.load(changed) is None
        assert file_sha256(path)


def frozen_schema_test() -> None:
    authority = RunnerAuthority.load()
    prompt = next(iter(authority.prompts.values()))
    sources = sorted(authority.sources)[:100]
    condition = authority.b1_conditions["B03-G0"]
    row = {
        "schema_version": "rq2b-v7-b1-runner-output-v1",
        "status": "SUCCESS",
        "run_id": "synthetic-no-inference",
        "condition_id": "B03-G0",
        "first_stage_cell_id": "B03",
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "representation": condition["representation"],
        "retriever": condition["retriever"],
        "persisted_candidate_source": condition["persisted_candidate_source"],
        "source_union_sha256": condition["source_union_sha256"],
        "top_k": 100,
        "score_semantics": "HIGHER_IS_BETTER",
        "top20_binding_sha256": top20_binding_sha256(
            condition_id="B03-G0",
            prompt_id=prompt["prompt_id"],
            prompt_sha256=prompt["prompt_sha256"],
            ordered_source_sha256=sources[:20],
        ),
        "ranked_candidates": [
            {"rank": rank, "source_sha256": source, "score": 0.0}
            for rank, source in enumerate(sources, 1)
        ],
        "cost": {
            "wall_time_ms": 0.0,
            "provider_calls": 0,
            "input_tokens": 1,
            "output_tokens": 0,
            "window_forwards": 1,
            "cache_hits": 0,
            "retry_count": 0,
            "timeout_count": 0,
            "failure_count": 0,
        },
    }
    validate_b1_row(row, authority, 1)
    poisoned = json.loads(json.dumps(row))
    poisoned["target"] = sources[0]
    expect_failure(lambda: validate_b1_row(poisoned, authority, 1), "prohibited label/outcome key")


def pending_release_gate_test(root: Path) -> None:
    pending = {
        "schema_version": AUTHORISATION_SCHEMA,
        "state": "PENDING_PHASE8_ROOT_RELEASE",
        "root_release_id": "pending",
        "run_id": "must-not-run",
        "attempt_id": "must-not-run",
        "payload": {},
        "phase8": {},
        "window_amendment": {},
        "model_snapshot": {},
        "runtime": {},
        "destinations": {},
        "ceilings": {},
    }
    with tempfile.TemporaryDirectory(dir=root / "skill_benchmark/cache") as directory:
        path = Path(directory) / "pending.json"
        path.write_text(json.dumps(pending), encoding="utf-8")
        expect_failure(
            lambda: validate_root_release(root, path),
            "Scientific execution is not root-released",
        )


def unknown_i3_binding_boundary_test() -> None:
    assert set(FIXED_REPRESENTATION_INPUTS) == {"I1-discovery", "I2-original"}
    assert FIXED_REPRESENTATION_INPUTS["I1-discovery"] == {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i1-discovery.jsonl",
        "sha256": "0fc34abe8ca3f5d23bcc563f496831e37628491ddc65caeb9c7a284d5d1ff8dd",
    }
    assert FIXED_REPRESENTATION_INPUTS["I2-original"] == {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i2-original.jsonl",
        "sha256": "8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec",
    }
    assert "I3C-fielded" not in FIXED_REPRESENTATION_INPUTS
    assert "I3-flat" not in FIXED_REPRESENTATION_INPUTS


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    runner_report = self_test()
    exact_window_inventory_test()
    exact_batch_test()
    maximum_window_test()
    online_cost_boundary_test()
    cache_contract_test()
    frozen_schema_test()
    pending_release_gate_test(root)
    unknown_i3_binding_boundary_test()
    assert "torch" not in sys.modules
    assert "transformers" not in sys.modules
    print(json.dumps({
        "status": "PASS_V7_SKILLROUTER_EMBEDDING_B1_NO_INFERENCE_TESTS",
        "network_calls": 0,
        "model_loads": 0,
        "model_forwards": 0,
        "runner_self_test": runner_report["status"],
        "checks": {
            "complete_exact_7500_256_content_token_windows": True,
            "separate_special_inclusive_model_input_binding": True,
            "authoritative_i1_i2_phase7_v2_binding": True,
            "released_query_instruction": True,
            "exact_length_no_padding_batch_plan": True,
            "maximum_query_to_window_cosine": True,
            "per_row_cost_is_online_query_only": True,
            "immutable_hash_bound_l2_cache": True,
            "official_b1_schema_compatibility": True,
            "recursive_outcome_key_rejection": True,
            "pending_root_release_blocks_execution": True,
            "final_i3_hashes_not_hard_coded": True,
            "torch_and_transformers_not_imported": True,
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
