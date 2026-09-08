#!/usr/bin/env python3
"""Validate label-free V7 B36+C6 runner outputs before offline label join.

This module deliberately has no path to the offline label adapter or D_q.  It
validates only frozen queries, sources, condition authority, ranking identity,
hash bindings, cost fields, and complete 12-cell B1 / 30-condition B2 coverage.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1"
ANALYSIS = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1"

RUNTIME_PATH = ANALYSIS / "label_free_query_runtime.jsonl"
CORE_PATH = MATRIX / "first_matrix_conditions.jsonl"
BRIDGE_PATH = MATRIX / "fixed_candidate_bridge_conditions.jsonl"
SOURCE_PATH = MATRIX / "source_manifest.jsonl"

EXPECTED_FILE_SHA256 = {
    RUNTIME_PATH: "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    CORE_PATH: "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
    BRIDGE_PATH: "d659ff98a5a2534478f68ab44794e4df7d89b23eb3a44a2fbf335cdca42366f7",
    SOURCE_PATH: "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
}

B1_SCHEMA_VERSION = "rq2b-v7-b1-runner-output-v1"
B2_SCHEMA_VERSION = "rq2b-v7-b2-runner-output-v1"
HEX = set("0123456789abcdef")
PROHIBITED_KEY_TOKENS = {
    "target", "gold", "label", "acceptable", "adequacy", "judged",
    "unjudged", "metric", "hit", "mrr", "recall", "ground_truth",
    "correctness", "a_q", "j_q", "d_q",
}
B1_KEYS = {
    "schema_version", "status", "run_id", "condition_id",
    "first_stage_cell_id", "prompt_id", "prompt_sha256", "representation",
    "retriever", "persisted_candidate_source", "source_union_sha256",
    "top_k", "score_semantics", "top20_binding_sha256",
    "ranked_candidates", "cost",
}
B2_KEYS = {
    "schema_version", "status", "run_id", "condition_id", "phase",
    "prompt_id", "prompt_sha256", "representation", "first_stage_retriever",
    "reranker", "persisted_candidate_source", "source_union_sha256",
    "input_top20_binding_sha256", "reranker_input_sha256", "score_semantics",
    "input_candidates", "reranked_candidates", "cost",
}
B1_COST_KEYS = {
    "wall_time_ms", "provider_calls", "input_tokens", "output_tokens",
    "window_forwards", "cache_hits", "retry_count", "timeout_count",
    "failure_count",
}
B2_COST_KEYS = B1_COST_KEYS | {"candidate_pairs"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    opener = gzip.open if path.suffix == ".gz" else Path.open
    if path.suffix == ".gz":
        handle_context = opener(path, mode="rt", encoding="utf-8", newline="")
    else:
        handle_context = opener(path, mode="r", encoding="utf-8", newline="")
    with handle_context as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            require(isinstance(value, dict), f"{path}:{line_no}: row is not an object")
            rows.append(value)
    return rows


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def top20_binding_sha256(
    *, condition_id: str, prompt_id: str, prompt_sha256: str,
    ordered_source_sha256: Iterable[str],
) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-top20-binding-v1",
        "condition_id": condition_id,
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_sha256,
        "ordered_source_sha256": list(ordered_source_sha256),
    })


def reranker_input_sha256(
    *, condition_id: str, prompt_id: str, prompt_sha256: str,
    input_top20_binding_sha256: str,
    input_candidates: list[dict[str, Any]],
) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-reranker-input-binding-v1",
        "condition_id": condition_id,
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_sha256,
        "input_top20_binding_sha256": input_top20_binding_sha256,
        "input_candidates": input_candidates,
    })


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def finite_number(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)


def normalized_key_tokens(key: str) -> set[str]:
    normalized = key.lower().replace("-", "_").replace(" ", "_")
    tokens = set(normalized.split("_")) | {normalized}
    for phrase in ("ground_truth", "a_q", "j_q", "d_q"):
        if phrase in normalized:
            tokens.add(phrase)
    return tokens


def reject_label_keys(value: Any, path: str = "row") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            require(
                not (normalized_key_tokens(str(key)) & PROHIBITED_KEY_TOKENS),
                f"{path}: prohibited label/outcome key {key!r}",
            )
            reject_label_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_label_keys(child, f"{path}[{index}]")


def exact_keys(value: dict[str, Any], expected: set[str], path: str) -> None:
    missing = expected - set(value)
    extra = set(value) - expected
    require(not missing and not extra, f"{path}: missing={sorted(missing)} extra={sorted(extra)}")


def validate_cost(cost: Any, *, b2: bool, path: str) -> None:
    require(isinstance(cost, dict), f"{path}: cost must be an object")
    exact_keys(cost, B2_COST_KEYS if b2 else B1_COST_KEYS, path)
    require(finite_number(cost["wall_time_ms"]) and cost["wall_time_ms"] >= 0, f"{path}: invalid wall_time_ms")
    for key in sorted((B2_COST_KEYS if b2 else B1_COST_KEYS) - {"wall_time_ms"}):
        require(isinstance(cost[key], int) and not isinstance(cost[key], bool) and cost[key] >= 0, f"{path}: invalid {key}")
    if b2:
        require(cost["candidate_pairs"] == 20, f"{path}: B2 candidate_pairs must equal 20")


@dataclass(frozen=True)
class RunnerAuthority:
    prompts: dict[str, dict[str, Any]]
    sources: set[str]
    b1_conditions: dict[str, dict[str, Any]]
    b2_conditions: dict[str, dict[str, Any]]

    @classmethod
    def load(cls) -> "RunnerAuthority":
        for path, expected in EXPECTED_FILE_SHA256.items():
            actual = file_sha256(path)
            require(actual == expected, f"authority hash drift: {path}: {actual} != {expected}")
        runtime = read_jsonl(RUNTIME_PATH)
        prompts = {str(row["prompt_id"]): row for row in runtime}
        require(len(prompts) == len(runtime) == 1077, "runtime prompts are not the frozen 1,077 unique queries")
        source_rows = read_jsonl(SOURCE_PATH)
        sources = {str(row["sha256"]) for row in source_rows}
        require(len(sources) == len(source_rows) == 3798, "source manifest is not the frozen 3,798-source union")
        core = read_jsonl(CORE_PATH)
        bridge = read_jsonl(BRIDGE_PATH)
        require(len(core) == 36 and len(bridge) == 6, "condition authority must be B36+C6")
        b1 = {str(row["condition_id"]): row for row in core if row["reranker"] == "NONE"}
        b2 = {str(row["condition_id"]): row for row in core if row["reranker"] != "NONE"}
        b2.update({str(row["condition_id"]): row for row in bridge})
        require(len(b1) == 12 and len(b2) == 30, "condition authority must yield 12 B1 and 30 materialised B2 conditions")
        require("C2-Q" not in b2 and "C2-S" not in b2, "C2 aliases must not be materialised")
        return cls(prompts=prompts, sources=sources, b1_conditions=b1, b2_conditions=b2)


def validate_b1_row(row: dict[str, Any], authority: RunnerAuthority, row_no: int) -> None:
    path = f"B1 row {row_no}"
    reject_label_keys(row, path)
    exact_keys(row, B1_KEYS, path)
    require(row["schema_version"] == B1_SCHEMA_VERSION, f"{path}: schema_version")
    require(row["status"] == "SUCCESS", f"{path}: only SUCCESS scientific rows are valid")
    require(isinstance(row["run_id"], str) and row["run_id"], f"{path}: run_id")
    condition_id = str(row["condition_id"])
    require(condition_id in authority.b1_conditions, f"{path}: unknown B1 condition {condition_id}")
    condition = authority.b1_conditions[condition_id]
    cell = condition_id.removesuffix("-G0")
    require(row["first_stage_cell_id"] == cell, f"{path}: first_stage_cell_id mismatch")
    prompt_id = str(row["prompt_id"])
    require(prompt_id in authority.prompts, f"{path}: unknown prompt")
    prompt = authority.prompts[prompt_id]
    require(row["prompt_sha256"] == prompt["prompt_sha256"], f"{path}: prompt hash mismatch")
    for key in ("representation", "retriever", "persisted_candidate_source", "source_union_sha256"):
        require(row[key] == condition[key], f"{path}: {key} differs from condition authority")
    require(row["persisted_candidate_source"] == cell, f"{path}: persisted source must equal B1 cell")
    require(row["top_k"] == 100 and row["score_semantics"] == "HIGHER_IS_BETTER", f"{path}: Top100/score contract")
    ranked = row["ranked_candidates"]
    require(isinstance(ranked, list) and len(ranked) == 100, f"{path}: exactly 100 candidates required")
    sources: list[str] = []
    for index, candidate in enumerate(ranked, 1):
        cpath = f"{path}.ranked_candidates[{index - 1}]"
        require(isinstance(candidate, dict), f"{cpath}: object required")
        exact_keys(candidate, {"rank", "source_sha256", "score"}, cpath)
        require(candidate["rank"] == index, f"{cpath}: rank must equal array position")
        require(is_sha256(candidate["source_sha256"]) and candidate["source_sha256"] in authority.sources, f"{cpath}: source identity")
        require(finite_number(candidate["score"]), f"{cpath}: finite numeric score required")
        sources.append(candidate["source_sha256"])
    require(len(set(sources)) == 100, f"{path}: candidate identities must be unique")
    expected_binding = top20_binding_sha256(
        condition_id=condition_id, prompt_id=prompt_id,
        prompt_sha256=row["prompt_sha256"], ordered_source_sha256=sources[:20],
    )
    require(row["top20_binding_sha256"] == expected_binding, f"{path}: Top20 binding hash mismatch")
    validate_cost(row["cost"], b2=False, path=f"{path}.cost")


def validate_b2_row(
    row: dict[str, Any], authority: RunnerAuthority,
    b1_by_key: dict[tuple[str, str], dict[str, Any]], row_no: int,
) -> None:
    path = f"B2 row {row_no}"
    reject_label_keys(row, path)
    exact_keys(row, B2_KEYS, path)
    require(row["schema_version"] == B2_SCHEMA_VERSION, f"{path}: schema_version")
    require(row["status"] == "SUCCESS", f"{path}: only SUCCESS scientific rows are valid")
    require(isinstance(row["run_id"], str) and row["run_id"], f"{path}: run_id")
    condition_id = str(row["condition_id"])
    require(condition_id in authority.b2_conditions, f"{path}: unknown B2 condition or forbidden alias {condition_id}")
    condition = authority.b2_conditions[condition_id]
    prompt_id = str(row["prompt_id"])
    require(prompt_id in authority.prompts, f"{path}: unknown prompt")
    require(row["prompt_sha256"] == authority.prompts[prompt_id]["prompt_sha256"], f"{path}: prompt hash mismatch")
    for key in ("phase", "representation", "reranker", "persisted_candidate_source", "source_union_sha256"):
        require(row[key] == condition[key], f"{path}: {key} differs from condition authority")
    require(row["first_stage_retriever"] == condition["retriever"], f"{path}: first-stage retriever mismatch")
    require(row["score_semantics"] == "HIGHER_IS_BETTER", f"{path}: score semantics")
    b1_condition_id = f"{condition['persisted_candidate_source']}-G0"
    b1_key = (b1_condition_id, prompt_id)
    require(b1_key in b1_by_key, f"{path}: missing persisted B1 source row {b1_key}")
    b1_row = b1_by_key[b1_key]
    expected_sources = [item["source_sha256"] for item in b1_row["ranked_candidates"][:20]]
    require(row["input_top20_binding_sha256"] == b1_row["top20_binding_sha256"], f"{path}: B1 Top20 binding mismatch")
    inputs = row["input_candidates"]
    require(isinstance(inputs, list) and len(inputs) == 20, f"{path}: exactly 20 input candidates required")
    input_sources: list[str] = []
    for index, candidate in enumerate(inputs, 1):
        cpath = f"{path}.input_candidates[{index - 1}]"
        require(isinstance(candidate, dict), f"{cpath}: object required")
        exact_keys(candidate, {"input_rank", "source_sha256", "candidate_view_sha256"}, cpath)
        require(candidate["input_rank"] == index, f"{cpath}: input rank must equal array position")
        require(candidate["source_sha256"] == expected_sources[index - 1], f"{cpath}: persisted B1 identity/order drift")
        require(is_sha256(candidate["candidate_view_sha256"]), f"{cpath}: candidate view hash")
        input_sources.append(candidate["source_sha256"])
    expected_input_hash = reranker_input_sha256(
        condition_id=condition_id, prompt_id=prompt_id,
        prompt_sha256=row["prompt_sha256"],
        input_top20_binding_sha256=row["input_top20_binding_sha256"],
        input_candidates=inputs,
    )
    require(row["reranker_input_sha256"] == expected_input_hash, f"{path}: reranker input hash mismatch")
    reranked = row["reranked_candidates"]
    require(isinstance(reranked, list) and len(reranked) == 20, f"{path}: exactly 20 reranked candidates required")
    output_sources: list[str] = []
    expected_input_rank = {source: index for index, source in enumerate(input_sources, 1)}
    for index, candidate in enumerate(reranked, 1):
        cpath = f"{path}.reranked_candidates[{index - 1}]"
        require(isinstance(candidate, dict), f"{cpath}: object required")
        exact_keys(candidate, {"rank", "input_rank", "source_sha256", "score"}, cpath)
        require(candidate["rank"] == index, f"{cpath}: rank must equal array position")
        require(candidate["source_sha256"] in expected_input_rank, f"{cpath}: output identity not in frozen input")
        require(candidate["input_rank"] == expected_input_rank[candidate["source_sha256"]], f"{cpath}: input_rank identity mismatch")
        require(finite_number(candidate["score"]), f"{cpath}: finite numeric score required")
        output_sources.append(candidate["source_sha256"])
    require(len(set(output_sources)) == 20 and set(output_sources) == set(input_sources), f"{path}: reranker must permute exactly the input identities")
    validate_cost(row["cost"], b2=True, path=f"{path}.cost")


def validate_outputs(
    b1_rows: list[dict[str, Any]], b2_rows: list[dict[str, Any]],
    authority: RunnerAuthority, *, require_complete: bool = True,
) -> dict[str, Any]:
    b1_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for row_no, row in enumerate(b1_rows, 1):
        validate_b1_row(row, authority, row_no)
        key = (str(row["condition_id"]), str(row["prompt_id"]))
        require(key not in b1_by_key, f"duplicate B1 row {key}")
        b1_by_key[key] = row
    b2_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for row_no, row in enumerate(b2_rows, 1):
        validate_b2_row(row, authority, b1_by_key, row_no)
        key = (str(row["condition_id"]), str(row["prompt_id"]))
        require(key not in b2_by_key, f"duplicate B2 row {key}")
        b2_by_key[key] = row
    expected_b1 = {(c, p) for c in authority.b1_conditions for p in authority.prompts}
    expected_b2 = {(c, p) for c in authority.b2_conditions for p in authority.prompts}
    require(set(b1_by_key) <= expected_b1 and set(b2_by_key) <= expected_b2, "unexpected output scope")
    if require_complete:
        require(set(b1_by_key) == expected_b1, f"B1 incomplete: got {len(b1_by_key)}, expected {len(expected_b1)}")
        require(set(b2_by_key) == expected_b2, f"B2 incomplete: got {len(b2_by_key)}, expected {len(expected_b2)}")
    return {
        "status": "PASS_LABEL_FREE_RUNNER_OUTPUT_VALIDATION",
        "queries": len(authority.prompts),
        "b1_cells": len(authority.b1_conditions),
        "b2_materialised_conditions": len(authority.b2_conditions),
        "outcome_conditions": len(authority.b1_conditions) + len(authority.b2_conditions),
        "b1_rows": len(b1_rows),
        "b2_rows": len(b2_rows),
        "c2_alias_rows": 0,
        "complete_scope_required": require_complete,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--b1", type=Path, required=True, help="Label-free B1 JSONL")
    parser.add_argument("--b2", type=Path, required=True, help="Label-free B2 JSONL")
    parser.add_argument("--allow-incomplete", action="store_true", help="Validate a shard; B2 still requires its B1 rows")
    args = parser.parse_args()
    report = validate_outputs(
        read_jsonl(args.b1), read_jsonl(args.b2), RunnerAuthority.load(),
        require_complete=not args.allow_incomplete,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
