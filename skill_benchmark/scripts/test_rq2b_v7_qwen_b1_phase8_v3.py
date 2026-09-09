#!/usr/bin/env python3
"""Focused no-provider regression tests for Phase-8 Qwen B1 V3."""

from __future__ import annotations

import ast
import json
import tempfile
from pathlib import Path
from unittest import mock

from build_rq2b_v7_qwen_b1_phase8_v3_preflight import (
    AUTHORISATION_SCHEMA,
    CONDITIONS_REL,
    EXPECTED_SOURCES,
    I1_I2_BINDINGS,
    PAYLOAD_SCHEMA,
    REPRESENTATION_CELLS,
    RUNNER_REL,
    RUNNER_VERSION,
    SKILLROUTER_CELLS,
    V3ExactEmbeddingCache,
    embedding_request_bytes,
    file_sha256,
    predictable_ceilings,
    read_jsonl,
    self_test as preflight_self_test,
    validate_qwen_condition_mapping,
    validate_representation_manifest_bindings,
)
from run_rq2b_v7_qwen_b1_phase8_v3 import (
    RUNTIME_CEILING_KEYS,
    execute_embedding_plan,
    self_test as runner_self_test,
    validate_one_use_release_state,
    validate_release_hash_bindings,
    validate_release_ceilings,
)
from validate_rq2b_v7_runner_outputs import (
    B1_SCHEMA_VERSION,
    RunnerAuthority,
    top20_binding_sha256,
    validate_b1_row,
)


ROOT = Path(__file__).resolve().parents[2]


def expect_failure(callable_, fragment: str) -> None:
    try:
        callable_()
    except ValueError as error:
        assert fragment in str(error), f"wrong failure: {error}"
    else:
        raise AssertionError(f"expected failure containing {fragment!r}")


def condition_mapping_test() -> None:
    rows = read_jsonl(ROOT / CONDITIONS_REL)
    qwen = {
        row["persisted_candidate_source"]: row
        for row in rows
        if row.get("reranker") == "NONE" and row.get("retriever") == "Qwen-text-embedding-v4"
    }
    validate_qwen_condition_mapping(qwen)
    assert set(qwen) == {"B02", "B05", "B08", "B11"}
    skillrouter = {
        row["persisted_candidate_source"]: row
        for row in rows
        if row.get("reranker") == "NONE" and row.get("retriever") == "SkillRouter-Embedding-0.6B"
    }
    assert set(skillrouter) == SKILLROUTER_CELLS
    expect_failure(
        lambda: validate_qwen_condition_mapping(skillrouter),
        "Qwen B1 cannot bind SkillRouter cells",
    )


def stale_representation_binding_test() -> None:
    phase8_expected = {
        **{name: dict(binding) for name, binding in I1_I2_BINDINGS.items()},
        "I3C-fielded": {"path": "phase8/final_2026_09_09_v4_1_i3c.jsonl", "sha256": "3" * 64},
        "I3-flat": {"path": "phase8/final_2026_09_09_v4_1_i3_flat.jsonl", "sha256": "4" * 64},
    }
    representations = {
        name: {
            **binding,
            "rows": EXPECTED_SOURCES,
            "provenance": "AUTHORITATIVE_2026_09_09_V2" if name in I1_I2_BINDINGS else "FINAL_PHASE8_V4_1",
        }
        for name, binding in phase8_expected.items()
    }
    validate_representation_manifest_bindings(representations, phase8_expected)
    stale_i1 = json.loads(json.dumps(representations))
    stale_i1["I1-discovery"]["sha256"] = "a" * 64
    expect_failure(
        lambda: validate_representation_manifest_bindings(stale_i1, phase8_expected),
        "stale or non-Phase8 representation binding",
    )
    stale_i3 = json.loads(json.dumps(representations))
    stale_i3["I3C-fielded"]["path"] = "old_extraction/i3c.jsonl"
    expect_failure(
        lambda: validate_representation_manifest_bindings(stale_i3, phase8_expected),
        "stale or non-Phase8 representation binding",
    )


def ceiling_and_stale_receipt_test() -> None:
    counts = {key: index + 1 for index, key in enumerate(sorted({
        "maximum_new_cache_entries",
        "maximum_new_cache_content_proxy_tokens",
        "maximum_new_cache_model_input_proxy_tokens",
        "maximum_new_cache_utf8_bytes",
        "maximum_external_text_submissions",
        "maximum_external_content_proxy_tokens",
        "maximum_external_model_input_proxy_tokens",
        "maximum_external_text_utf8_bytes",
        "maximum_external_request_body_utf8_bytes",
        "cold_query_requests",
        "maximum_request_attempts",
        "maximum_successful_calls",
    }))}
    payload = {"predictable_ceilings": predictable_ceilings(counts)}
    release = {
        "ceilings": {
            **payload["predictable_ceilings"],
            "maximum_provider_reported_total_tokens": 1000,
            "maximum_wall_time_seconds": 60,
        }
    }
    validate_release_ceilings(release, payload)
    insufficient = json.loads(json.dumps(release))
    insufficient["ceilings"]["maximum_request_attempts"] -= 1
    expect_failure(lambda: validate_release_ceilings(insufficient, payload), "Insufficient")
    assert set(release["ceilings"]) == set(payload["predictable_ceilings"]) | RUNTIME_CEILING_KEYS

    # A preflight receipt is stale as soon as either bound byte hash changes.
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        payload_path = root / "payload.json"
        preflight_path = root / "preflight.json"
        payload_path.write_text("{}\n", encoding="utf-8")
        preflight_path.write_text("{}\n", encoding="utf-8")
        phase8 = {
            "receipt": {"sha256": "5" * 64},
            "root_manifest": {"sha256": "6" * 64},
        }
        binding = {
            "payload": {"path": "payload.json", "sha256": file_sha256(payload_path)},
            "preflight": {"path": "preflight.json", "sha256": file_sha256(preflight_path)},
            "phase8": {
                "receipt_sha256": "5" * 64,
                "root_manifest_sha256": "6" * 64,
            },
        }
        validate_release_hash_bindings(
            release=binding, root=root, payload_path=payload_path,
            preflight_path=preflight_path, payload={"phase8": phase8},
        )
        preflight_path.write_text('{"changed":true}\n', encoding="utf-8")
        expect_failure(
            lambda: validate_release_hash_bindings(
                release=binding, root=root, payload_path=payload_path,
                preflight_path=preflight_path, payload={"phase8": phase8},
            ),
            "preflight binding drift",
        )


def one_use_release_test() -> None:
    release = {
        "state": "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_QWEN_B1_EXECUTION",
        "one_use": True,
        "consumed": False,
    }
    validate_one_use_release_state(release)
    replay = dict(release, consumed=True)
    expect_failure(lambda: validate_one_use_release_state(replay), "not fresh and one-use")


def ast_literal_test() -> None:
    tree = ast.parse((ROOT / RUNNER_REL).read_text(encoding="utf-8"))
    literals = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Constant):
            literals[node.targets[0].id] = node.value.value
    assert literals["RUNNER_VERSION"] == RUNNER_VERSION
    assert literals["PAYLOAD_SCHEMA"] == PAYLOAD_SCHEMA
    assert literals["AUTHORISATION_SCHEMA"] == AUTHORISATION_SCHEMA


def official_validator_test() -> None:
    authority = RunnerAuthority.load()
    prompt = next(iter(authority.prompts.values()))
    sources = sorted(authority.sources)[:100]
    condition = authority.b1_conditions["B02-G0"]
    row = {
        "schema_version": B1_SCHEMA_VERSION,
        "status": "SUCCESS",
        "run_id": "synthetic-no-provider",
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
            condition_id="B02-G0", prompt_id=prompt["prompt_id"],
            prompt_sha256=prompt["prompt_sha256"], ordered_source_sha256=sources[:20],
        ),
        "ranked_candidates": [
            {"rank": rank, "source_sha256": source, "score": 0.0}
            for rank, source in enumerate(sources, 1)
        ],
        "cost": {
            "wall_time_ms": 1.0, "provider_calls": 1, "input_tokens": 2,
            "output_tokens": 0, "window_forwards": 1, "cache_hits": 0,
            "retry_count": 0, "timeout_count": 0, "failure_count": 0,
        },
    }
    validate_b1_row(row, authority, 1)


def no_network_self_tests() -> None:
    with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")) as network:
        assert preflight_self_test()["network_calls"] == 0
        assert runner_self_test()["provider_requests"] == 0
        network.assert_not_called()


def immutable_single_attempt_failure_test() -> None:
    document_text = "document"
    query_text = "query"
    texts = []
    cache_rows = []
    for text, role in ((document_text, "document_chunk"), (query_text, "query")):
        text_id = __import__("hashlib").sha256(text.encode("utf-8")).hexdigest()
        row = {
            "text_id": text_id, "text_sha256": text_id, "text": text,
            "content_proxy_tokens": len(text), "model_input_proxy_tokens": len(text) + 2,
            "special_token_proxy_tokens": 2, "utf8_bytes": len(text.encode("utf-8")),
            "roles": [{"kind": role}],
        }
        texts.append(row)
        cache_rows.append({"text_id": text_id, "cache_hit": False, "cache_entry_sha256": None})
    document_id, query_id = [row["text_id"] for row in texts]
    body = embedding_request_bytes([document_text])
    requests = [{
        "request_index": 0, "request_role": "document_batch", "text_ids": [document_id],
        "content_proxy_tokens": len(document_text),
        "model_input_proxy_tokens": len(document_text) + 2,
        "text_utf8_bytes": len(document_text.encode("utf-8")),
        "request_body_utf8_bytes": len(body),
        "request_body_sha256": __import__("hashlib").sha256(body).hexdigest(),
    }]
    calls = 0

    def fail_once(_api_key: str, _body: bytes, _timeout: int):
        nonlocal calls
        calls += 1
        raise RuntimeError("synthetic provider failure")

    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        ceilings = {
            "maximum_request_attempts": 1,
            "maximum_successful_calls": 1,
            "maximum_external_text_submissions": 1,
            "maximum_external_content_proxy_tokens": len(document_text),
            "maximum_external_model_input_proxy_tokens": len(document_text) + 2,
            "maximum_external_text_utf8_bytes": len(document_text.encode("utf-8")),
            "maximum_external_request_body_utf8_bytes": len(body),
            "maximum_provider_reported_total_tokens": 100,
            "maximum_wall_time_seconds": 10,
        }
        try:
            execute_embedding_plan(
                text_rows=texts, cache_rows=cache_rows,
                planned_requests=requests,
                cache=V3ExactEmbeddingCache(temp / "cache", create=True),
                api_key="synthetic", timeout_seconds=1,
                attempt_dir=temp / "attempts", ceilings=ceilings,
                request_fn=fail_once,
            )
        except RuntimeError as error:
            assert str(error) == "synthetic provider failure"
        else:
            raise AssertionError("synthetic provider failure should propagate")
        assert calls == 1
        assert (temp / "attempts/attempt_000000.json").is_file()
        assert (temp / "attempts/failure_000000.json").is_file()
        assert not (temp / "attempts/success_000000.json").exists()
        # The query request was never attempted after the first failure.
        assert query_id not in json.loads((temp / "attempts/attempt_000000.json").read_text())["text_ids"]


def main() -> None:
    condition_mapping_test()
    stale_representation_binding_test()
    ceiling_and_stale_receipt_test()
    one_use_release_test()
    ast_literal_test()
    official_validator_test()
    no_network_self_tests()
    immutable_single_attempt_failure_test()
    print(json.dumps({
        "status": "PASS_QWEN_B1_PHASE8_V3_FOCUSED_TESTS",
        "network_calls": 0,
        "provider_requests": 0,
        "checks": {
            "qwen_cells_B02_B05_B08_B11": True,
            "skillrouter_cells_rejected": True,
            "authoritative_i1_i2_v2_bindings": True,
            "stale_i1_and_nonfinal_i3_rejected": True,
            "stale_hash_detected": True,
            "insufficient_ceiling_rejected": True,
            "consumed_root_release_rejected": True,
            "ast_visible_contract_literals": True,
            "official_b1_validator": True,
            "self_tests_no_network": True,
            "immutable_attempt_receipts_and_zero_retry": True,
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
