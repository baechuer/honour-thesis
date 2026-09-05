#!/usr/bin/env python3
"""Offline adapter tests for RQ2a selectors; sends no benchmark text externally."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import run_rq2a_fixed_candidate_matrix as fixed
from rq2a_selector_common import (
    FIELD_ORDER,
    bm25_scores,
    load_run_data,
    repo_root,
    self_test,
    tie_aware_metrics,
    write_json_atomic,
)
from run_rq2a_field_aware_selector import (
    aggregate,
    choose_aggregation,
    field_component_text,
)


class FakeTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [index + 1 for index, _ in enumerate(text.split())]


def deterministic_vector(text: str, dimensions: int) -> list[float]:
    values = [0.0 for _ in range(dimensions)]
    for index, character in enumerate(text.encode("utf-8")):
        values[index % dimensions] += (character + 1) / 256
    return values


def test_embedding_client() -> None:
    calls: list[dict[str, Any]] = []
    original_post_json = fixed.post_json

    def fake_post_json(
        url: str,
        api_key: str,
        payload: dict[str, Any],
        timeout_seconds: int,
    ) -> dict[str, Any]:
        del url, api_key, timeout_seconds
        calls.append(payload)
        dimensions = int(payload["dimensions"])
        return {
            "data": [
                {
                    "index": index,
                    "embedding": deterministic_vector(text, dimensions),
                }
                for index, text in enumerate(payload["input"])
            ],
            "usage": {
                "prompt_tokens": sum(len(text.split()) for text in payload["input"]),
                "total_tokens": sum(len(text.split()) for text in payload["input"]),
            },
        }

    try:
        fixed.post_json = fake_post_json
        with tempfile.TemporaryDirectory(prefix="rq2a-adapter-test-") as temporary:
            legacy_root = Path(temporary) / "legacy"
            client = fixed.RQ2aEmbeddingClient(
                provider="synthetic",
                base_url="https://not-called.example/v1",
                api_key="not-a-real-key",
                model="synthetic-v1",
                dimensions=4,
                cache_dir=Path(temporary),
                timeout_seconds=1,
                max_audit_tokens=10,
                legacy_cache_dir=legacy_root,
            )
            texts = ["alpha beta", "gamma delta", "epsilon"]
            first = client.embed_many(
                texts,
                batch_size=2,
                progress_label="synthetic",
            )
            assert len(first) == 3
            assert len(calls) == 2
            assert client.stats["cache_misses"] == 3
            assert client.stats["api_calls"] == 2
            assert client.stats["provider_usage"]["total_tokens"] == 5

            second = client.embed_many(
                texts,
                batch_size=2,
                progress_label="synthetic-cache",
            )
            assert second == first
            assert len(calls) == 2
            assert client.stats["cache_hits"] == 3

            legacy_text = "legacy exact"
            legacy_path, requested_dimensions = client.legacy_cache_paths(
                legacy_text
            )[-1]
            assert requested_dimensions is None
            write_json_atomic(
                legacy_path,
                {"embedding": deterministic_vector(legacy_text, 4)},
            )
            before_legacy_calls = len(calls)
            legacy_result = client.embed_many(
                [legacy_text],
                batch_size=1,
                progress_label="synthetic-legacy",
            )
            assert len(legacy_result[legacy_text]) == 4
            assert len(calls) == before_legacy_calls
            assert client.stats["legacy_cache_hits"] == 1

            try:
                client.embed_many(
                    ["one two three four five six seven eight nine ten eleven"],
                    batch_size=1,
                    progress_label="too-long",
                )
            except ValueError as exc:
                assert "no-truncation guard" in str(exc)
            else:
                raise AssertionError("No-truncation guard accepted an overlength text")
    finally:
        fixed.post_json = original_post_json


def test_cross_encoder_preflight_without_model() -> None:
    scorer = object.__new__(fixed.SkillRouterCrossEncoder)
    scorer.tokenizer = FakeTokenizer()
    scorer.max_length = 500
    scorer.stats = {
        "maximum_model_tokens": 0,
        "minimum_model_tokens": None,
    }
    input_ids = scorer.build_input_ids("query text", "document text")
    assert input_ids
    assert scorer.stats["maximum_model_tokens"] == len(input_ids)

    scorer.max_length = len(input_ids) - 1
    try:
        scorer.build_input_ids("query text", "document text")
    except ValueError as exc:
        assert "no-truncation limit" in str(exc)
    else:
        raise AssertionError("Cross-encoder preflight silently accepted truncation")


def test_real_artifact_alignment() -> None:
    input_dir = repo_root() / "rq2a_matched_content"
    representations = [
        "shared-only",
        "same-facts-fielded",
        "same-facts-flat",
        "same-facts-prose",
        "same-facts-order-controlled",
        "same-facts-diluted-1x",
        "same-facts-diluted-2x",
        "same-facts-diluted-4x",
    ]
    protocol, prompts, indexes = load_run_data(
        input_dir,
        "development",
        representations,
        clusters_per_field=1,
    )
    assert len(prompts) == 15
    assert len({prompt["cluster_id"] for prompt in prompts}) == 7
    assert all(len(index) == 21 for index in indexes.values())

    labels = protocol["field_labels"]
    fielded = indexes["same-facts-fielded"]
    for row in fielded.values():
        for field in FIELD_ORDER:
            block = field_component_text(
                field,
                row["canonical_fields"][field],
                labels,
            )
            assert block in row["selector_visible_text"]


def field_aware_choice_rows(
    maximum: list[tuple[float, float]],
    uniform_top_two: list[tuple[float, float]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for aggregation, metrics in (
        ("maximum", maximum),
        ("uniform-top-two", uniform_top_two),
    ):
        for index, (top1, mrr) in enumerate(metrics, start=1):
            rows.append(
                {
                    "selector": f"qwen-field-aware-{aggregation}",
                    "cluster_id": f"cluster-{index}",
                    "prompt_id": f"prompt-{index}",
                    "top1_tie_adjusted": top1,
                    "mrr_tie_adjusted": mrr,
                }
            )
    return rows


def test_field_aware_choice_rule() -> None:
    top1_wins = choose_aggregation(
        field_aware_choice_rows(
            [(1.0, 0.5), (1.0, 0.5)],
            [(1.0, 1.0), (0.0, 1.0)],
        )
    )
    assert top1_wins["selected_aggregation"] == "maximum"

    mrr_breaks_tie = choose_aggregation(
        field_aware_choice_rows(
            [(1.0, 0.5), (0.0, 0.5)],
            [(1.0, 0.8), (0.0, 0.8)],
        )
    )
    assert mrr_breaks_tie["selected_aggregation"] == "uniform-top-two"

    exact_tie = choose_aggregation(
        field_aware_choice_rows(
            [(1.0, 0.5), (0.0, 0.5)],
            [(1.0, 0.5), (0.0, 0.5)],
        )
    )
    assert exact_tie["selected_aggregation"] == "uniform-top-two"

    malformed = field_aware_choice_rows(
        [(1.0, 1.0)],
        [(1.0, 1.0)],
    )
    malformed[-1]["prompt_id"] = "different-prompt"
    try:
        choose_aggregation(malformed)
    except ValueError as exc:
        assert "identical prompts" in str(exc)
    else:
        raise AssertionError("Aggregation choice accepted unmatched prompts")


def main() -> None:
    self_test()
    test_embedding_client()
    test_cross_encoder_preflight_without_model()
    test_real_artifact_alignment()
    test_field_aware_choice_rule()
    component_scores = [0.3, 0.2, 0.1, 0.0, -0.1, -0.2, -0.3]
    assert aggregate(component_scores, "maximum") == 0.3
    assert abs(aggregate(component_scores, "uniform-top-two") - 0.25) < 1e-12
    try:
        aggregate([0.3, 0.2], "maximum")
    except ValueError as exc:
        assert "exactly 7" in str(exc)
    else:
        raise AssertionError("Field-aware aggregation accepted missing fields")
    assert bm25_scores("alpha", ["alpha", "beta", "gamma"])[0] > 0
    assert tie_aware_metrics(["a", "b", "c"], [1, 1, 0], "a")[
        "top1_tie_adjusted"
    ] == 0.5
    print(
        "RQ2a selector adapter tests: PASS "
        "(synthetic API/cache, no-truncation, real artifact alignment)"
    )


if __name__ == "__main__":
    main()
