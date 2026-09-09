#!/usr/bin/env python3
"""Focused no-inference tests for the Phase-8 BM25 B1 V2 runner."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch

import run_rq2b_v7_first_matrix_bm25_b1_v2 as runner

from run_rq2b_v7_first_matrix_bm25_b1_v2 import (
    AUTHORISATION_SCHEMA,
    CELLS,
    FIXED_REPRESENTATIONS,
    GlobalBM25,
    TOP_K,
    make_row,
    self_test,
    text_sha256,
    validate_root_release,
    validate_rows,
)


def expect_failure(callable_: Any, message_fragment: str) -> None:
    try:
        callable_()
    except ValueError as error:
        if message_fragment not in str(error):
            raise AssertionError(f"Wrong failure: {error}") from error
    else:
        raise AssertionError(f"Expected failure containing: {message_fragment}")


def lexical_ranking_test() -> None:
    sources = [f"{index:064x}" for index in range(120)]
    documents = [(source, "irrelevant content") for source in sources]
    documents[7] = (sources[7], "specialist routing routing phrase")
    index = GlobalBM25(documents)
    assert index.rank("specialist routing phrase")[0][0] == sources[7]
    ties = index.rank("absent vocabulary")
    assert ties == [(source, 0.0) for source in sources[:TOP_K]]


def official_row_contract_test() -> None:
    sources = [f"{index:064x}" for index in range(TOP_K)]
    source_set = set(sources)
    prompt = {
        "prompt_id": "synthetic-prompt",
        "prompt": "route a synthetic task",
        "prompt_sha256": text_sha256("route a synthetic task"),
    }
    ranking = [(source, 0.0) for source in sources]
    rows = []
    for representation, cell in CELLS.items():
        rows.append(make_row(
            run_id="synthetic-no-execution",
            representation=representation,
            condition={"retriever": "BM25", "persisted_candidate_source": cell},
            prompt=prompt,
            ranking=ranking,
            wall_time_ms=0.0,
        ))
    validate_rows(rows, [prompt], source_set)

    wrong_cell = copy.deepcopy(rows)
    wrong_cell[0]["first_stage_cell_id"] = "B99"
    expect_failure(lambda: validate_rows(wrong_cell, [prompt], source_set), "first-stage cell drift")

    poisoned = copy.deepcopy(rows)
    poisoned[0]["ranked_candidates"][0]["target_source_sha256"] = sources[0]
    expect_failure(lambda: validate_rows(poisoned, [prompt], source_set), "prohibited label/outcome key")


def pending_root_release_test(root: Path) -> None:
    pending = {
        "schema_version": AUTHORISATION_SCHEMA,
        "state": "PENDING_EXPLICIT_USER_ROOT_RELEASE",
        "one_use": True,
        "consumed": False,
        "root_release_id": "pending",
        "run_id": "must-not-run",
        "attempt_id": "must-not-run",
        "payload": {},
        "phase8": {},
        "destinations": {},
        "ceilings": {},
    }
    with tempfile.TemporaryDirectory(dir=root / "skill_benchmark/cache") as directory:
        path = Path(directory) / "pending.json"
        path.write_text(json.dumps(pending), encoding="utf-8")
        expect_failure(lambda: validate_root_release(root, path), "BM25 execution is not root-released")


def dynamic_i3_boundary_test() -> None:
    assert FIXED_REPRESENTATIONS == {
        "I1-discovery": {
            "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i1-discovery.jsonl",
            "sha256": "0fc34abe8ca3f5d23bcc563f496831e37628491ddc65caeb9c7a284d5d1ff8dd",
        },
        "I2-original": {
            "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i2-original.jsonl",
            "sha256": "8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec",
        },
    }
    assert "I3C-fielded" not in FIXED_REPRESENTATIONS
    assert "I3-flat" not in FIXED_REPRESENTATIONS


def failed_attempt_receipt_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        authorisation = root / "authorisation.json"
        payload_path = root / "payload.json"
        authorisation.write_text("{}\n", encoding="utf-8")
        payload_path.write_text("{}\n", encoding="utf-8")
        output = root / "skill_benchmark/cache/output"
        attempt = root / "skill_benchmark/cache/attempt"
        release = {
            "run_id": "synthetic-failure",
            "attempt_id": "attempt-1",
            "root_release_id": "release-1",
            "ceilings": {"maximum_wall_time_seconds": 1.0},
            "_destinations": {"output_dir": output, "attempt_dir": attempt},
        }
        with (
            patch.object(runner, "validate_root_release", return_value=(release, payload_path, {})),
            patch.object(runner, "load_inputs", side_effect=ValueError("synthetic input failure")),
        ):
            expect_failure(lambda: runner.execute(root, authorisation), "synthetic input failure")
        assert (attempt / "run_started.json").is_file()
        failure = json.loads((attempt / "run_failed.json").read_text(encoding="utf-8"))
        assert failure["error"] == "synthetic input failure"
        assert not output.exists()


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    report = self_test()
    lexical_ranking_test()
    official_row_contract_test()
    pending_root_release_test(root)
    dynamic_i3_boundary_test()
    failed_attempt_receipt_test()
    assert "torch" not in sys.modules
    assert "transformers" not in sys.modules
    assert "numpy" not in sys.modules
    print(json.dumps({
        "status": "PASS_V7_BM25_B1_V2_FOCUSED_NO_INFERENCE_TESTS",
        "runner_self_test": report["status"],
        "network_calls": 0,
        "model_loads": 0,
        "model_forwards": 0,
        "checks": {
            "lexical_ranking_and_sha_ties": True,
            "official_b1_row_contract": True,
            "recursive_outcome_key_rejection": True,
            "pending_one_use_release_blocks_execution": True,
            "authoritative_i1_i2_v2_binding": True,
            "final_i3_payload_only": True,
            "failed_attempt_receipted_without_output": True,
            "ml_runtime_not_imported": True,
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
