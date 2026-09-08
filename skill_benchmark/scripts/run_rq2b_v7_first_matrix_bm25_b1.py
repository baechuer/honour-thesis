#!/usr/bin/env python3
"""Run the four label-free BM25 cells in the V7 first matrix.

The runner has a deliberately closed intake: the frozen label-free query
runtime, source manifest, condition manifest, and four representation views.
It has no configurable label, outcome, provider, embedding, reranker, or
offline-analysis input.
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import platform
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
MATRIX_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1"
ANALYSIS_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1"
I1_I2_ROOT = ROOT / "skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_08_v1"
I3_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_merged_2026_09_08_v1"
CONTRACT_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_runner_output_analysis_contract_2026_09_09_v1"
OUTPUT_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_bm25_b1_run_2026_09_09_v1"
STAGING_ROOT = OUTPUT_ROOT.with_name(f".{OUTPUT_ROOT.name}.staging")

RUNTIME_PATH = ANALYSIS_ROOT / "label_free_query_runtime.jsonl"
SOURCE_MANIFEST_PATH = MATRIX_ROOT / "source_manifest.jsonl"
CONDITION_PATH = MATRIX_ROOT / "first_matrix_conditions.jsonl"
SCHEMA_PATH = CONTRACT_ROOT / "b1_runner_output_schema.json"

RUNNER_VERSION = "rq2b-v7-first-matrix-bm25-b1-runner-v1"
RUN_ID = "rq2b-v7-first-matrix-bm25-b1-2026-09-09-v1"
ROW_SCHEMA_VERSION = "rq2b-v7-b1-runner-output-v1"
RECEIPT_SCHEMA_VERSION = "rq2b-v7-first-matrix-bm25-b1-receipt-v1"
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
K1 = 1.5
B = 0.75
TOP_K = 100
EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
TOKEN_RE = re.compile(r"[a-z0-9]+")

EXPECTED_INPUT_SHA256 = {
    RUNTIME_PATH: "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    SOURCE_MANIFEST_PATH: "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    CONDITION_PATH: "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
    SCHEMA_PATH: "e9af1eb941ef95d9ce65f7edec7f88320cd9b2d879b66163250d767f39af906b",
    I1_I2_ROOT / "i1-discovery.jsonl": "672928a98f31cf65aa90be752191495a9bebefec929b1d2b8b804afe66b3744e",
    I1_I2_ROOT / "i2-original.jsonl": "8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec",
    I3_ROOT / "i3c_fielded.jsonl": "cb1fd58e61b97d1c21fa41a995f508a7e323127d3f14542ca8ed3f736a291595",
    I3_ROOT / "i3_flat.jsonl": "3697e15a308774ec97ed8df2cb4a108e32f2e049fadfcee3d2efcf671d088b74",
}

CELLS = (
    ("B01", "I1-discovery", I1_I2_ROOT / "i1-discovery.jsonl"),
    ("B04", "I2-original", I1_I2_ROOT / "i2-original.jsonl"),
    ("B07", "I3C-fielded", I3_ROOT / "i3c_fielded.jsonl"),
    ("B10", "I3-flat", I3_ROOT / "i3_flat.jsonl"),
)

ROW_KEYS = {
    "schema_version", "status", "run_id", "condition_id",
    "first_stage_cell_id", "prompt_id", "prompt_sha256",
    "representation", "retriever", "persisted_candidate_source",
    "source_union_sha256", "top_k", "score_semantics",
    "top20_binding_sha256", "ranked_candidates", "cost",
}
COST_KEYS = {
    "wall_time_ms", "provider_calls", "input_tokens", "output_tokens",
    "window_forwards", "cache_hits", "retry_count", "timeout_count",
    "failure_count",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def lexical_tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{relative(path)} is not a JSON object")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"{relative(path)}:{line_number}: blank row")
            value = json.loads(raw)
            require(isinstance(value, dict), f"{relative(path)}:{line_number}: row is not an object")
            rows.append(value)
    return rows


def write_text_new(path: Path, value: str) -> None:
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(value)


def write_json_new(path: Path, value: Any) -> None:
    write_text_new(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("x", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def verify_input_hashes() -> None:
    for path, expected in EXPECTED_INPUT_SHA256.items():
        require(path.is_file(), f"missing frozen input: {relative(path)}")
        actual = sha256_file(path)
        require(actual == expected, f"frozen input hash drift: {relative(path)}: {actual} != {expected}")


def load_queries() -> list[dict[str, Any]]:
    rows = read_jsonl(RUNTIME_PATH)
    require(len(rows) == EXPECTED_QUERIES, "label-free runtime must contain 1,077 rows")
    require(len({row.get("prompt_id") for row in rows}) == EXPECTED_QUERIES, "prompt IDs are not unique")
    require(len({row.get("prompt_sha256") for row in rows}) == EXPECTED_QUERIES, "prompt hashes are not unique")
    for row in rows:
        require(
            set(row) == {"schema_version", "prompt_id", "prompt_sha256", "prompt"},
            f"unexpected label-free runtime fields for {row.get('prompt_id')}",
        )
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1", "runtime schema drift")
        require(isinstance(row["prompt_id"], str) and row["prompt_id"], "invalid prompt ID")
        require(isinstance(row["prompt"], str) and row["prompt"], "invalid prompt text")
        require(row["prompt_sha256"] == sha256_text(row["prompt"]), f"prompt hash mismatch: {row['prompt_id']}")
    return rows


def load_source_identities() -> set[str]:
    rows = read_jsonl(SOURCE_MANIFEST_PATH)
    require(len(rows) == EXPECTED_SOURCES, "source manifest must contain 3,798 rows")
    identities = {row.get("sha256") for row in rows}
    require(len(identities) == EXPECTED_SOURCES, "source manifest identities are not unique")
    require(all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) for value in identities), "invalid source identity")
    return identities


def load_conditions() -> dict[str, dict[str, Any]]:
    rows = read_jsonl(CONDITION_PATH)
    conditions = {str(row["condition_id"]): row for row in rows}
    require(len(rows) == len(conditions) == 36, "first-matrix condition manifest must contain 36 unique rows")
    selected: dict[str, dict[str, Any]] = {}
    for cell_id, representation, _ in CELLS:
        condition_id = f"{cell_id}-G0"
        require(condition_id in conditions, f"missing condition {condition_id}")
        row = conditions[condition_id]
        require(row["representation"] == representation, f"{condition_id}: representation drift")
        require(row["retriever"] == "BM25" and row["reranker"] == "NONE", f"{condition_id}: method drift")
        require(row["persisted_candidate_source"] == cell_id, f"{condition_id}: persisted source drift")
        require(row["query_count"] == EXPECTED_QUERIES, f"{condition_id}: query count drift")
        require(row["source_union_sha256"] == SOURCE_UNION_SHA256, f"{condition_id}: source union drift")
        require(row["prompt_manifest_sha256"] == PROMPT_MANIFEST_SHA256, f"{condition_id}: prompt manifest drift")
        selected[cell_id] = row
    return selected


def load_representation(path: Path, representation: str, sources: set[str]) -> list[tuple[str, str]]:
    rows = read_jsonl(path)
    require(len(rows) == EXPECTED_SOURCES, f"{representation}: expected 3,798 rows")
    documents: list[tuple[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        source_sha256 = row.get("source_sha256")
        selector_text = row.get("selector_text")
        require(row.get("representation") == representation, f"{representation}: row representation drift")
        require(isinstance(source_sha256, str) and source_sha256 in sources, f"{representation}: unknown source")
        require(source_sha256 not in seen, f"{representation}: duplicate source {source_sha256}")
        require(isinstance(selector_text, str) and selector_text, f"{representation}: empty selector text")
        require(row.get("selector_text_sha256") == sha256_text(selector_text), f"{representation}: selector hash mismatch for {source_sha256}")
        seen.add(source_sha256)
        documents.append((source_sha256, selector_text))
    require(seen == sources, f"{representation}: source coverage mismatch")
    return sorted(documents, key=lambda item: item[0])


class GlobalBM25:
    def __init__(self, documents: list[tuple[str, str]]) -> None:
        require(len(documents) == EXPECTED_SOURCES, "BM25 corpus must contain 3,798 documents")
        self.source_sha256 = [source for source, _ in documents]
        require(self.source_sha256 == sorted(self.source_sha256), "BM25 source identities must be SHA-sorted")
        require(len(set(self.source_sha256)) == EXPECTED_SOURCES, "BM25 source identities must be unique")
        self.document_lengths: list[int] = []
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for document_index, (_, text) in enumerate(documents):
            tokens = lexical_tokens(text)
            self.document_lengths.append(len(tokens))
            for term, frequency in Counter(tokens).items():
                self.postings[term].append((document_index, frequency))
        self.average_document_length = statistics.mean(self.document_lengths)
        require(self.average_document_length > 0.0, "BM25 corpus has no lexical tokens")
        self.idf = {
            term: math.log(1.0 + (EXPECTED_SOURCES - len(posting) + 0.5) / (len(posting) + 0.5))
            for term, posting in self.postings.items()
        }

    def rank_top100(self, query: str) -> list[tuple[str, float]]:
        scores: dict[int, float] = defaultdict(float)
        for term, query_frequency in Counter(lexical_tokens(query)).items():
            posting = self.postings.get(term)
            if posting is None:
                continue
            idf = self.idf[term]
            for document_index, frequency in posting:
                denominator = frequency + K1 * (
                    1.0 - B + B * self.document_lengths[document_index] / self.average_document_length
                )
                scores[document_index] += (
                    query_frequency * idf * frequency * (K1 + 1.0) / denominator
                )
        require(all(math.isfinite(score) and score > 0.0 for score in scores.values()), "BM25 produced invalid scores")
        ranked_matches = heapq.nsmallest(
            TOP_K,
            scores.items(),
            key=lambda item: (-item[1], self.source_sha256[item[0]]),
        )
        ranking = [(self.source_sha256[index], float(score)) for index, score in ranked_matches]
        if len(ranking) < TOP_K:
            matched = set(scores)
            for index, source_sha256 in enumerate(self.source_sha256):
                if index not in matched:
                    ranking.append((source_sha256, 0.0))
                    if len(ranking) == TOP_K:
                        break
        require(len(ranking) == TOP_K and len({source for source, _ in ranking}) == TOP_K, "invalid Top-100")
        return ranking


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


def make_row(
    *, cell_id: str, condition: dict[str, Any], prompt: dict[str, Any],
    ranking: list[tuple[str, float]], wall_time_ms: float,
) -> dict[str, Any]:
    condition_id = f"{cell_id}-G0"
    candidates = [
        {"rank": rank, "source_sha256": source_sha256, "score": score}
        for rank, (source_sha256, score) in enumerate(ranking, 1)
    ]
    return {
        "schema_version": ROW_SCHEMA_VERSION,
        "status": "SUCCESS",
        "run_id": RUN_ID,
        "condition_id": condition_id,
        "first_stage_cell_id": cell_id,
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "representation": condition["representation"],
        "retriever": condition["retriever"],
        "persisted_candidate_source": condition["persisted_candidate_source"],
        "source_union_sha256": condition["source_union_sha256"],
        "top_k": TOP_K,
        "score_semantics": "HIGHER_IS_BETTER",
        "top20_binding_sha256": top20_binding_sha256(
            condition_id=condition_id,
            prompt_id=prompt["prompt_id"],
            prompt_sha256=prompt["prompt_sha256"],
            ordered_source_sha256=(source for source, _ in ranking[:20]),
        ),
        "ranked_candidates": candidates,
        "cost": {
            "wall_time_ms": wall_time_ms,
            "provider_calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "window_forwards": 0,
            "cache_hits": 0,
            "retry_count": 0,
            "timeout_count": 0,
            "failure_count": 0,
        },
    }


def validate_rows(
    rows: list[dict[str, Any]], queries: list[dict[str, Any]],
    conditions: dict[str, dict[str, Any]], sources: set[str],
) -> None:
    prompt_by_id = {row["prompt_id"]: row for row in queries}
    expected_keys = {(f"{cell_id}-G0", prompt_id) for cell_id, _, _ in CELLS for prompt_id in prompt_by_id}
    actual_keys: set[tuple[str, str]] = set()
    for row_number, row in enumerate(rows, 1):
        prefix = f"B1 row {row_number}"
        require(set(row) == ROW_KEYS, f"{prefix}: output schema fields drift")
        require(row["schema_version"] == ROW_SCHEMA_VERSION and row["status"] == "SUCCESS", f"{prefix}: status/schema")
        require(row["run_id"] == RUN_ID, f"{prefix}: run ID")
        cell_id = row["first_stage_cell_id"]
        condition_id = row["condition_id"]
        require(cell_id in conditions and condition_id == f"{cell_id}-G0", f"{prefix}: condition identity")
        condition = conditions[cell_id]
        prompt_id = row["prompt_id"]
        require(prompt_id in prompt_by_id, f"{prefix}: unknown prompt")
        require(row["prompt_sha256"] == prompt_by_id[prompt_id]["prompt_sha256"], f"{prefix}: prompt hash")
        for field in ("representation", "retriever", "persisted_candidate_source", "source_union_sha256"):
            require(row[field] == condition[field], f"{prefix}: {field}")
        require(row["top_k"] == TOP_K and row["score_semantics"] == "HIGHER_IS_BETTER", f"{prefix}: ranking contract")
        candidates = row["ranked_candidates"]
        require(isinstance(candidates, list) and len(candidates) == TOP_K, f"{prefix}: Top-100 length")
        candidate_sources: list[str] = []
        previous: tuple[float, str] | None = None
        for rank, candidate in enumerate(candidates, 1):
            require(set(candidate) == {"rank", "source_sha256", "score"}, f"{prefix}: candidate fields")
            require(candidate["rank"] == rank, f"{prefix}: candidate rank")
            source_sha256 = candidate["source_sha256"]
            score = candidate["score"]
            require(source_sha256 in sources, f"{prefix}: candidate source")
            require(not isinstance(score, bool) and isinstance(score, (int, float)) and math.isfinite(score), f"{prefix}: candidate score")
            current = (-float(score), source_sha256)
            require(previous is None or previous <= current, f"{prefix}: score/SHA ordering")
            previous = current
            candidate_sources.append(source_sha256)
        require(len(set(candidate_sources)) == TOP_K, f"{prefix}: duplicate candidate")
        expected_binding = top20_binding_sha256(
            condition_id=condition_id,
            prompt_id=prompt_id,
            prompt_sha256=row["prompt_sha256"],
            ordered_source_sha256=candidate_sources[:20],
        )
        require(row["top20_binding_sha256"] == expected_binding, f"{prefix}: Top-20 binding")
        cost = row["cost"]
        require(set(cost) == COST_KEYS, f"{prefix}: cost fields")
        require(isinstance(cost["wall_time_ms"], (int, float)) and not isinstance(cost["wall_time_ms"], bool) and math.isfinite(cost["wall_time_ms"]) and cost["wall_time_ms"] >= 0, f"{prefix}: wall time")
        require(all(cost[key] == 0 for key in COST_KEYS - {"wall_time_ms"}), f"{prefix}: local BM25 non-wall costs must be zero")
        key = (condition_id, prompt_id)
        require(key not in actual_keys, f"{prefix}: duplicate output key")
        actual_keys.add(key)
    require(actual_keys == expected_keys, f"four-cell output coverage mismatch: {len(actual_keys)} != {len(expected_keys)}")


def render_readme(*, b1_sha256: str, runner_sha256: str) -> str:
    return f"""# V7 first-matrix BM25 B1 run v1

Status: `PASS_B01_B04_B07_B10_LABEL_FREE_LOCAL_BM25_EXECUTION`.

This package contains exactly the four local BM25 first-stage cells requested
for the frozen V7 first matrix: B01/I1-discovery, B04/I2-original,
B07/I3C-fielded and B10/I3-flat. Each cell covers all 1,077 label-free runtime
queries against all 3,798 frozen source identities and persists Top-100.

The runner reads no target, gold, acceptable-set, judgement, review-outcome,
offline-label or prior selector-output artifact. It performs no network,
provider, embedding, reranking or offline-scoring call.

BM25 is lowercase `[a-z0-9]+`, k1=1.5, b=0.75, with multiplicative query-term
frequency. Rankings use descending score and ascending `source_sha256` as the
stable tie-break. Row-level cost records measured local query wall time; all
provider/token/window/retry/timeout/failure counters are zero.

## Artifacts

- `b1.jsonl`: 4,308 strict `rq2b-v7-b1-runner-output-v1` rows; SHA-256 `{b1_sha256}`.
- `run_receipt.json`: exact input, runner, parameter, coverage, cost and output bindings.
- runner: `skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1.py`; SHA-256 `{runner_sha256}`.

## Replay

From the repository root, verification is label-free and read-only:

```sh
python3 -B skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1.py --verify
python3 -B skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py \\
  --b1 skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_bm25_b1_run_2026_09_09_v1/b1.jsonl \\
  --b2 /dev/null --allow-incomplete
```

The official validator's incomplete mode is intentional: this package is the
four BM25-cell B1 shard only and does not fabricate the other eight B1 cells or
any B2 rows.
"""


def receipt_costs(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "query_wall_time_ms": sum(float(row["cost"]["wall_time_ms"]) for row in rows),
        "provider_calls": sum(row["cost"]["provider_calls"] for row in rows),
        "input_tokens": sum(row["cost"]["input_tokens"] for row in rows),
        "output_tokens": sum(row["cost"]["output_tokens"] for row in rows),
        "window_forwards": sum(row["cost"]["window_forwards"] for row in rows),
        "cache_hits": sum(row["cost"]["cache_hits"] for row in rows),
        "retry_count": sum(row["cost"]["retry_count"] for row in rows),
        "timeout_count": sum(row["cost"]["timeout_count"] for row in rows),
        "failure_count": sum(row["cost"]["failure_count"] for row in rows),
        "monetary_cost_usd": 0.0,
    }


def execute() -> dict[str, Any]:
    require(not OUTPUT_ROOT.exists(), f"refusing to overwrite {relative(OUTPUT_ROOT)}")
    require(not STAGING_ROOT.exists(), f"stale staging directory exists: {relative(STAGING_ROOT)}")
    verify_input_hashes()
    queries = load_queries()
    sources = load_source_identities()
    conditions = load_conditions()
    run_started = utc_now()
    run_start_ns = time.perf_counter_ns()
    rows: list[dict[str, Any]] = []
    per_cell: list[dict[str, Any]] = []
    for cell_id, representation, view_path in CELLS:
        cell_start_ns = time.perf_counter_ns()
        load_start_ns = time.perf_counter_ns()
        documents = load_representation(view_path, representation, sources)
        load_ms = (time.perf_counter_ns() - load_start_ns) / 1_000_000.0
        index_start_ns = time.perf_counter_ns()
        index = GlobalBM25(documents)
        index_ms = (time.perf_counter_ns() - index_start_ns) / 1_000_000.0
        cell_rows: list[dict[str, Any]] = []
        for prompt in queries:
            query_start_ns = time.perf_counter_ns()
            ranking = index.rank_top100(prompt["prompt"])
            wall_time_ms = (time.perf_counter_ns() - query_start_ns) / 1_000_000.0
            cell_rows.append(make_row(
                cell_id=cell_id,
                condition=conditions[cell_id],
                prompt=prompt,
                ranking=ranking,
                wall_time_ms=wall_time_ms,
            ))
        rows.extend(cell_rows)
        per_cell.append({
            "cell_id": cell_id,
            "condition_id": f"{cell_id}-G0",
            "representation": representation,
            "representation_path": relative(view_path),
            "representation_sha256": EXPECTED_INPUT_SHA256[view_path],
            "documents": len(documents),
            "queries": len(cell_rows),
            "rows": len(cell_rows),
            "average_document_length_lexical_tokens": index.average_document_length,
            "corpus_lexical_tokens": sum(index.document_lengths),
            "unique_terms": len(index.postings),
            "representation_load_and_validation_ms": load_ms,
            "index_build_ms": index_ms,
            "query_wall_time_ms": sum(float(row["cost"]["wall_time_ms"]) for row in cell_rows),
            "cell_wall_time_ms": (time.perf_counter_ns() - cell_start_ns) / 1_000_000.0,
        })
    validate_rows(rows, queries, conditions, sources)
    runner_path = Path(__file__).resolve()
    runner_sha256 = sha256_file(runner_path)
    STAGING_ROOT.mkdir(parents=False, exist_ok=False)
    b1_path = STAGING_ROOT / "b1.jsonl"
    write_jsonl_new(b1_path, rows)
    b1_sha256 = sha256_file(b1_path)
    readme = render_readme(b1_sha256=b1_sha256, runner_sha256=runner_sha256)
    readme_path = STAGING_ROOT / "README.md"
    write_text_new(readme_path, readme)
    run_finished = utc_now()
    receipt = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "status": "PASS_B01_B04_B07_B10_LABEL_FREE_LOCAL_BM25_EXECUTION",
        "run_id": RUN_ID,
        "runner": {
            "path": relative(runner_path),
            "sha256": runner_sha256,
            "version": RUNNER_VERSION,
        },
        "execution_basis": "EXPLICIT_CURRENT_TASK_BM25_B1_B01_B04_B07_B10_ONLY",
        "scope": {
            "cells": [cell_id for cell_id, _, _ in CELLS],
            "conditions": [f"{cell_id}-G0" for cell_id, _, _ in CELLS],
            "representations": [representation for _, representation, _ in CELLS],
            "queries_per_cell": EXPECTED_QUERIES,
            "source_candidates_per_query": EXPECTED_SOURCES,
            "top_k": TOP_K,
        },
        "method": {
            "retriever": "BM25",
            "tokenizer": "lowercase_[a-z0-9]+",
            "query_term_frequency": "multiplicative",
            "idf": "ln(1+(N-df+0.5)/(df+0.5))",
            "k1": K1,
            "b": B,
            "tie_break": "source_sha256_ascending",
            "score_semantics": "HIGHER_IS_BETTER",
        },
        "label_isolation": {
            "runtime": "label_free_query_runtime_only",
            "labels_read": False,
            "prior_selector_outputs_read": False,
            "offline_scorer_run": False,
        },
        "external_activity": {
            "network_calls": 0,
            "provider_calls": 0,
            "embedding_calls": 0,
            "reranking_calls": 0,
        },
        "inputs": {
            relative(path): {"sha256": expected}
            for path, expected in sorted(EXPECTED_INPUT_SHA256.items(), key=lambda item: relative(item[0]))
        },
        "counts": {
            "cells": len(CELLS),
            "queries": len(queries),
            "sources": len(sources),
            "rows": len(rows),
            "ranked_candidates": len(rows) * TOP_K,
            "unique_output_keys": len({(row["condition_id"], row["prompt_id"]) for row in rows}),
        },
        "cost": receipt_costs(rows),
        "per_cell": per_cell,
        "outputs": {
            "README.md": {"bytes": readme_path.stat().st_size, "sha256": sha256_file(readme_path)},
            "b1.jsonl": {"bytes": b1_path.stat().st_size, "rows": len(rows), "sha256": b1_sha256},
        },
        "validation": {
            "frozen_input_hashes": "PASS",
            "representation_source_coverage": "PASS_4_X_3798",
            "internal_b1_schema_and_coverage": "PASS_4_X_1077",
            "top20_binding_hashes": "PASS",
            "stable_score_then_source_sha256_order": "PASS",
        },
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "timing": {
            "started_at_utc": run_started,
            "finished_at_utc": run_finished,
            "total_wall_time_ms": (time.perf_counter_ns() - run_start_ns) / 1_000_000.0,
        },
    }
    write_json_new(STAGING_ROOT / "run_receipt.json", receipt)
    STAGING_ROOT.rename(OUTPUT_ROOT)
    return receipt


def verify_package() -> dict[str, Any]:
    verify_input_hashes()
    queries = load_queries()
    sources = load_source_identities()
    conditions = load_conditions()
    require(OUTPUT_ROOT.is_dir(), f"missing output package: {relative(OUTPUT_ROOT)}")
    require(
        {path.name for path in OUTPUT_ROOT.iterdir()} == {"README.md", "b1.jsonl", "run_receipt.json"},
        "output package inventory drift",
    )
    receipt = read_json(OUTPUT_ROOT / "run_receipt.json")
    require(receipt.get("schema_version") == RECEIPT_SCHEMA_VERSION, "receipt schema drift")
    require(receipt.get("status") == "PASS_B01_B04_B07_B10_LABEL_FREE_LOCAL_BM25_EXECUTION", "receipt status drift")
    require(receipt.get("run_id") == RUN_ID, "receipt run ID drift")
    require(receipt["runner"]["sha256"] == sha256_file(Path(__file__).resolve()), "runner hash drift")
    for filename in ("README.md", "b1.jsonl"):
        artifact = receipt["outputs"][filename]
        path = OUTPUT_ROOT / filename
        require(artifact["sha256"] == sha256_file(path), f"{filename} output hash drift")
        require(artifact["bytes"] == path.stat().st_size, f"{filename} byte-size drift")
    rows = read_jsonl(OUTPUT_ROOT / "b1.jsonl")
    validate_rows(rows, queries, conditions, sources)
    require(receipt["outputs"]["b1.jsonl"]["rows"] == len(rows) == len(CELLS) * EXPECTED_QUERIES, "receipt row count drift")
    require(receipt["counts"]["rows"] == len(rows), "receipt coverage count drift")
    require(receipt["counts"]["ranked_candidates"] == len(rows) * TOP_K, "receipt candidate count drift")
    require(receipt["cost"] == receipt_costs(rows), "receipt row-cost aggregate drift")
    return {
        "status": "PASS_BM25_B1_PACKAGE_VERIFICATION",
        "run_id": RUN_ID,
        "cells": len(CELLS),
        "queries_per_cell": EXPECTED_QUERIES,
        "sources": EXPECTED_SOURCES,
        "rows": len(rows),
        "ranked_candidates": len(rows) * TOP_K,
        "b1_sha256": sha256_file(OUTPUT_ROOT / "b1.jsonl"),
        "receipt_sha256": sha256_file(OUTPUT_ROOT / "run_receipt.json"),
    }


def self_test() -> dict[str, Any]:
    original_sources = [f"{index:064x}" for index in range(EXPECTED_SOURCES)]
    documents = [(source, "irrelevant") for source in original_sources]
    documents[9] = (documents[9][0], "ocr scanned pdf ocr")
    documents[10] = (documents[10][0], "ocr native pdf")
    index = GlobalBM25(documents)
    direct = index.rank_top100("OCR scanned PDF")
    require(direct[0][0] == original_sources[9], "synthetic BM25 relevance ordering failed")
    ties = index.rank_top100("term-not-in-corpus")
    require([source for source, _ in ties] == original_sources[:TOP_K], "synthetic SHA tie-break failed")
    require(all(score == 0.0 for _, score in ties), "synthetic absent-term scores failed")
    return {
        "status": "PASS_BM25_B1_SYNTHETIC_SELF_TEST",
        "tokenizer": "lowercase_[a-z0-9]+",
        "k1": K1,
        "b": B,
        "tie_break": "source_sha256_ascending",
        "scientific_rows_created": 0,
        "network_calls": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true", help="Run synthetic BM25 checks only")
    mode.add_argument("--execute", action="store_true", help="Run the four frozen BM25 B1 cells once")
    mode.add_argument("--verify", action="store_true", help="Verify the persisted label-free package")
    args = parser.parse_args()
    if args.self_test:
        report = self_test()
    elif args.execute:
        report = execute()
    else:
        report = verify_package()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
