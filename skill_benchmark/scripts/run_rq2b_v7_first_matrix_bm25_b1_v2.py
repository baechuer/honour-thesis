#!/usr/bin/env python3
"""Run the four Phase-8-released V7 BM25 B1 cells.

This V2 runner has no default scientific input or output package.  It is inert
unless a one-use root release binds an exact Phase-8 label-free payload.  I1/I2
are fixed to the authoritative 2026-09-09 v2 artifacts; final V4.1 I3 paths and
hashes arrive only through that payload.  No provider, model, result, label or
offline analysis input exists in the runner contract.
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import os
import platform
import re
import statistics
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


RUNNER_VERSION = "rq2b-v7-first-matrix-bm25-b1-runner-v2"
PAYLOAD_SCHEMA = "rq2b-v7-bm25-b1-phase8-payload-v2"
AUTHORISATION_SCHEMA = "rq2b-v7-bm25-b1-root-release-v2"
ROW_SCHEMA = "rq2b-v7-b1-runner-output-v1"
RECEIPT_SCHEMA = "rq2b-v7-first-matrix-bm25-b1-receipt-v2"

EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
TOP_K = 100
K1 = 1.5
B = 0.75
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
TOKEN_RE = re.compile(r"[a-z0-9]+")

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_analysis_freeze_2026_09_08_v1/label_free_query_runtime.jsonl"
)
SOURCE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/source_manifest.jsonl"
)
CONDITIONS_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/first_matrix_conditions.jsonl"
)
VALIDATOR_REL = Path("skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py")
FIXED_INPUT_SHA256 = {
    RUNTIME_REL: "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    SOURCE_REL: "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    CONDITIONS_REL: "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
}
FIXED_REPRESENTATIONS = {
    "I1-discovery": {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i1-discovery.jsonl",
        "sha256": "0fc34abe8ca3f5d23bcc563f496831e37628491ddc65caeb9c7a284d5d1ff8dd",
    },
    "I2-original": {
        "path": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i2-original.jsonl",
        "sha256": "8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec",
    },
}
CELLS = {
    "I1-discovery": "B01",
    "I2-original": "B04",
    "I3C-fielded": "B07",
    "I3-flat": "B10",
}
PROHIBITED_KEY_TOKENS = {
    "target", "gold", "label", "acceptable", "adequacy", "judged",
    "unjudged", "metric", "hit", "mrr", "recall", "ground_truth",
    "correctness", "a_q", "j_q", "d_q",
}
ROW_KEYS = {
    "schema_version", "status", "run_id", "condition_id",
    "first_stage_cell_id", "prompt_id", "prompt_sha256", "representation",
    "retriever", "persisted_candidate_source", "source_union_sha256",
    "top_k", "score_semantics", "top20_binding_sha256",
    "ranked_candidates", "cost",
}
COST_KEYS = {
    "wall_time_ms", "provider_calls", "input_tokens", "output_tokens",
    "window_forwards", "cache_hits", "retry_count", "timeout_count",
    "failure_count",
}
CEILING_KEYS = {
    "maximum_queries", "maximum_sources", "maximum_output_rows",
    "maximum_ranked_candidates", "maximum_wall_time_seconds",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def exact_keys(value: Any, expected: set[str], field: str) -> None:
    require(isinstance(value, dict), f"{field}: expected object")
    require(set(value) == expected, f"{field}: keys drift: {sorted(set(value) ^ expected)}")


def root_path(root: Path, value: str, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: path missing")
    supplied = Path(value)
    path = supplied.resolve() if supplied.is_absolute() else (root / supplied).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return path


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"Blank JSONL row: {path}:{line_number}")
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected JSON object: {path}:{line_number}")
            rows.append(value)
    return rows


def write_json_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def reject_outcome_keys(value: Any, location: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            # ``cache_hits`` is a required official cost field, not an outcome.
            prohibited = normalized != "cache_hits" and any(
                token in normalized for token in PROHIBITED_KEY_TOKENS
            )
            require(not prohibited, f"{location}: prohibited label/outcome key: {key}")
            reject_outcome_keys(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_outcome_keys(child, f"{location}[{index}]")


def validate_artifact(root: Path, value: Any, *, field: str, rows: int | None = None) -> Path:
    exact_keys(value, {"path", "sha256", "rows"}, field)
    require(is_sha256(value["sha256"]), f"{field}: invalid SHA-256")
    if rows is not None:
        require(value["rows"] == rows, f"{field}: row-count binding drift")
    path = root_path(root, value["path"], field=f"{field}.path")
    require(path.is_file(), f"{field}: missing artifact")
    require(file_sha256(path) == value["sha256"], f"{field}: artifact hash drift")
    return path


def validate_payload(root: Path, path: Path) -> dict[str, Any]:
    payload = read_json(path)
    exact_keys(payload, {"schema_version", "state", "runner_version", "implementation", "phase8", "inputs", "counts", "method", "isolation"}, "payload")
    require(payload["schema_version"] == PAYLOAD_SCHEMA, "Payload schema drift")
    require(payload["state"] == "SEALED_LABEL_FREE_PHASE8_PAYLOAD", "Payload is not Phase-8 sealed")
    require(payload["runner_version"] == RUNNER_VERSION, "Payload runner version drift")

    implementation = payload["implementation"]
    exact_keys(implementation, {"runner", "official_output_validator"}, "payload.implementation")
    expected_paths = {
        "runner": Path(__file__).resolve(),
        "official_output_validator": (root / VALIDATOR_REL).resolve(),
    }
    for role, expected_path in expected_paths.items():
        value = implementation[role]
        exact_keys(value, {"path", "sha256"}, f"payload.implementation.{role}")
        require(root_path(root, value["path"], field=f"implementation.{role}.path") == expected_path, f"Implementation path drift: {role}")
        require(value["sha256"] == file_sha256(expected_path), f"Implementation hash drift: {role}")

    phase8 = payload["phase8"]
    exact_keys(phase8, {"status", "receipt", "final_v4_1_i3_hashes_bound"}, "payload.phase8")
    require(phase8["status"] == "PASS" and phase8["final_v4_1_i3_hashes_bound"] is True, "Payload Phase-8 gate is not PASS")
    receipt_path = validate_artifact(root, {**phase8["receipt"], "rows": 1}, field="payload.phase8.receipt", rows=1)
    receipt = read_json(receipt_path)
    require(receipt.get("status") == "PASS_PHASE8_ROOT_READY_PENDING_EXPLICIT_PER_RUN_AUTHORISATION", "Phase-8 receipt status drift")
    require(receipt.get("execution_authorised") is False, "Phase-8 receipt must not itself authorise execution")

    inputs = payload["inputs"]
    exact_keys(inputs, {"runtime", "source_manifest", "conditions", "representations"}, "payload.inputs")
    fixed_inputs = {
        "runtime": (RUNTIME_REL, EXPECTED_QUERIES),
        "source_manifest": (SOURCE_REL, EXPECTED_SOURCES),
        "conditions": (CONDITIONS_REL, 36),
    }
    for role, (fixed_path, expected_rows) in fixed_inputs.items():
        expected = {"path": fixed_path.as_posix(), "sha256": FIXED_INPUT_SHA256[fixed_path], "rows": expected_rows}
        require(inputs[role] == expected, f"Fixed input drift: {role}")
        validate_artifact(root, inputs[role], field=f"payload.inputs.{role}", rows=expected_rows)

    representations = inputs["representations"]
    exact_keys(representations, set(CELLS), "payload.inputs.representations")
    for representation, value in representations.items():
        exact_keys(value, {"path", "sha256", "rows", "phase8_final", "extraction_protocol"}, f"representations.{representation}")
        require(value["rows"] == EXPECTED_SOURCES and value["phase8_final"] is True, f"{representation}: final Phase-8 binding missing")
        if representation in FIXED_REPRESENTATIONS:
            expected = FIXED_REPRESENTATIONS[representation]
            require(value["path"] == expected["path"] and value["sha256"] == expected["sha256"], f"{representation}: authoritative v2 binding drift")
            require(value["extraction_protocol"] == "SOURCE_NATIVE_PHASE7_V2", f"{representation}: extraction protocol drift")
        else:
            require(value["extraction_protocol"] == "I3C_SUBAGENT_EXTRACTION_V4_1", f"{representation}: final V4.1 protocol missing")
        validate_artifact(root, {"path": value["path"], "sha256": value["sha256"], "rows": value["rows"]}, field=f"representations.{representation}", rows=EXPECTED_SOURCES)

    require(payload["counts"] == {"queries": EXPECTED_QUERIES, "sources": EXPECTED_SOURCES, "representations": 4, "b1_cells": 4, "b1_output_rows": 4 * EXPECTED_QUERIES}, "Payload counts drift")
    require(payload["method"] == {"retriever": "BM25", "tokenizer": "lowercase_[a-z0-9]+", "query_term_frequency": "multiplicative", "idf": "ln(1+(N-df+0.5)/(df+0.5))", "k1": K1, "b": B, "stable_tie_break": "source_sha256_ascending", "top_k": TOP_K}, "Payload method drift")
    require(payload["isolation"] == {"labels_or_results_read": False, "selector_inputs_are_source_only": True, "offline_scorer_run": False}, "Payload isolation drift")
    return payload


def validate_root_release(root: Path, path: Path) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Root release must be inside repository root") from error
    require(path.is_file(), "Root-release authorisation is missing")
    value = read_json(path)
    exact_keys(value, {"schema_version", "state", "one_use", "consumed", "root_release_id", "run_id", "attempt_id", "payload", "phase8", "destinations", "ceilings"}, "root_release")
    require(value["schema_version"] == AUTHORISATION_SCHEMA, "Root-release schema drift")
    require(value["state"] == "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_ROOT_RELEASED_EXECUTION", "BM25 execution is not root-released")
    require(value["one_use"] is True and value["consumed"] is False, "Root release is not unused one-use authority")
    for field in ("root_release_id", "run_id", "attempt_id"):
        require(isinstance(value[field], str) and value[field], f"Root-release {field} missing")
    exact_keys(value["payload"], {"path", "sha256"}, "root_release.payload")
    require(is_sha256(value["payload"]["sha256"]), "Payload SHA missing")
    payload_path = root_path(root, value["payload"]["path"], field="root_release.payload.path")
    require(payload_path.is_file() and file_sha256(payload_path) == value["payload"]["sha256"], "Root-release payload drift")
    payload = validate_payload(root, payload_path)
    require(value["phase8"] == {"status": "PASS", "receipt_sha256": payload["phase8"]["receipt"]["sha256"]}, "Root-release Phase-8 binding drift")
    exact_keys(value["destinations"], {"output_dir", "attempt_dir"}, "root_release.destinations")
    destinations = {role: root_path(root, item, field=f"destinations.{role}") for role, item in value["destinations"].items()}
    require(len(set(destinations.values())) == 2, "Output and attempt destinations must be distinct")
    for role, destination in destinations.items():
        require(relative(destination, root).startswith("skill_benchmark/cache/"), f"{role}: destination must be under skill_benchmark/cache")
        require(not destination.exists(), f"{role}: destination already exists")
    exact_keys(value["ceilings"], CEILING_KEYS, "root_release.ceilings")
    require(value["ceilings"]["maximum_queries"] == EXPECTED_QUERIES, "Query ceiling drift")
    require(value["ceilings"]["maximum_sources"] == EXPECTED_SOURCES, "Source ceiling drift")
    require(value["ceilings"]["maximum_output_rows"] == 4 * EXPECTED_QUERIES, "Output-row ceiling drift")
    require(value["ceilings"]["maximum_ranked_candidates"] == 4 * EXPECTED_QUERIES * TOP_K, "Ranked-candidate ceiling drift")
    require(isinstance(value["ceilings"]["maximum_wall_time_seconds"], (int, float)) and not isinstance(value["ceilings"]["maximum_wall_time_seconds"], bool) and value["ceilings"]["maximum_wall_time_seconds"] > 0, "Wall-time ceiling invalid")
    value["_destinations"] = destinations
    return value, payload_path, payload


def lexical_tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


class GlobalBM25:
    def __init__(self, documents: list[tuple[str, str]]) -> None:
        require(bool(documents), "BM25 corpus is empty")
        self.source_sha256 = [source for source, _ in documents]
        require(self.source_sha256 == sorted(self.source_sha256), "BM25 identities must be SHA-sorted")
        require(len(set(self.source_sha256)) == len(documents), "BM25 identities must be unique")
        self.document_lengths: list[int] = []
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for index, (_, text) in enumerate(documents):
            tokens = lexical_tokens(text)
            self.document_lengths.append(len(tokens))
            for term, frequency in Counter(tokens).items():
                self.postings[term].append((index, frequency))
        self.average_document_length = statistics.mean(self.document_lengths)
        require(self.average_document_length > 0.0, "BM25 corpus has no lexical tokens")
        n = len(documents)
        self.idf = {term: math.log(1.0 + (n - len(posting) + 0.5) / (len(posting) + 0.5)) for term, posting in self.postings.items()}

    def rank(self, query: str, k: int = TOP_K) -> list[tuple[str, float]]:
        require(0 < k <= len(self.source_sha256), "Invalid BM25 Top-K")
        scores: dict[int, float] = defaultdict(float)
        for term, query_frequency in Counter(lexical_tokens(query)).items():
            for index, frequency in self.postings.get(term, []):
                denominator = frequency + K1 * (1.0 - B + B * self.document_lengths[index] / self.average_document_length)
                scores[index] += query_frequency * self.idf[term] * frequency * (K1 + 1.0) / denominator
        require(all(math.isfinite(score) and score > 0.0 for score in scores.values()), "BM25 produced invalid scores")
        ranked = heapq.nsmallest(k, scores.items(), key=lambda item: (-item[1], self.source_sha256[item[0]]))
        result = [(self.source_sha256[index], float(score)) for index, score in ranked]
        if len(result) < k:
            matched = set(scores)
            for index, source in enumerate(self.source_sha256):
                if index not in matched:
                    result.append((source, 0.0))
                    if len(result) == k:
                        break
        return result


def top20_binding_sha256(*, condition_id: str, prompt_id: str, prompt_sha256: str, ordered_source_sha256: Iterable[str]) -> str:
    return canonical_sha256({"schema_version": "rq2b-v7-top20-binding-v1", "condition_id": condition_id, "prompt_id": prompt_id, "prompt_sha256": prompt_sha256, "ordered_source_sha256": list(ordered_source_sha256)})


def load_inputs(root: Path, payload: dict[str, Any]) -> tuple[list[dict[str, Any]], set[str], dict[str, dict[str, Any]], dict[str, list[tuple[str, str]]]]:
    inputs = payload["inputs"]
    prompts = read_jsonl(root_path(root, inputs["runtime"]["path"], field="runtime.path"))
    require(len(prompts) == EXPECTED_QUERIES, "Runtime query count drift")
    require(len({row.get("prompt_id") for row in prompts}) == EXPECTED_QUERIES, "Runtime prompt identity drift")
    for row in prompts:
        exact_keys(row, {"schema_version", "prompt_id", "prompt_sha256", "prompt"}, "runtime row")
        reject_outcome_keys(row)
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1", "Runtime schema drift")
        require(row["prompt_sha256"] == text_sha256(row["prompt"]), "Runtime prompt hash drift")

    source_rows = read_jsonl(root_path(root, inputs["source_manifest"]["path"], field="source_manifest.path"))
    source_ids = {row.get("sha256") for row in source_rows}
    require(len(source_rows) == len(source_ids) == EXPECTED_SOURCES and all(is_sha256(value) for value in source_ids), "Source identity coverage drift")

    condition_rows = read_jsonl(root_path(root, inputs["conditions"]["path"], field="conditions.path"))
    by_id = {row.get("condition_id"): row for row in condition_rows}
    require(len(condition_rows) == len(by_id) == 36, "Condition manifest coverage drift")
    conditions: dict[str, dict[str, Any]] = {}
    for representation, cell in CELLS.items():
        condition = by_id.get(f"{cell}-G0")
        require(condition is not None, f"Missing condition {cell}-G0")
        require(condition.get("representation") == representation and condition.get("retriever") == "BM25" and condition.get("reranker") == "NONE", f"{cell}-G0: method drift")
        require(condition.get("persisted_candidate_source") == cell, f"{cell}-G0: candidate-source drift")
        require(condition.get("source_union_sha256") == SOURCE_UNION_SHA256 and condition.get("prompt_manifest_sha256") == PROMPT_MANIFEST_SHA256, f"{cell}-G0: root binding drift")
        conditions[representation] = condition

    representations: dict[str, list[tuple[str, str]]] = {}
    for representation, binding in inputs["representations"].items():
        path = root_path(root, binding["path"], field=f"representations.{representation}.path")
        rows = read_jsonl(path)
        require(len(rows) == EXPECTED_SOURCES, f"{representation}: row count drift")
        seen: set[str] = set()
        documents: list[tuple[str, str]] = []
        for row in rows:
            reject_outcome_keys(row)
            source = row.get("source_sha256")
            text = row.get("selector_text")
            require(row.get("representation") == representation, f"{representation}: row identity drift")
            require(source in source_ids and source not in seen, f"{representation}: source identity drift")
            require(isinstance(text, str) and text and row.get("selector_text_sha256") == text_sha256(text), f"{representation}: selector text drift")
            seen.add(source)
            documents.append((source, text))
        require(seen == source_ids, f"{representation}: source coverage drift")
        representations[representation] = sorted(documents)
    return prompts, {str(value) for value in source_ids}, conditions, representations


def make_row(*, run_id: str, representation: str, condition: dict[str, Any], prompt: dict[str, Any], ranking: list[tuple[str, float]], wall_time_ms: float) -> dict[str, Any]:
    cell = CELLS[representation]
    condition_id = f"{cell}-G0"
    candidates = [{"rank": rank, "source_sha256": source, "score": score} for rank, (source, score) in enumerate(ranking, 1)]
    return {
        "schema_version": ROW_SCHEMA,
        "status": "SUCCESS",
        "run_id": run_id,
        "condition_id": condition_id,
        "first_stage_cell_id": cell,
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "representation": representation,
        "retriever": condition["retriever"],
        "persisted_candidate_source": condition["persisted_candidate_source"],
        "source_union_sha256": SOURCE_UNION_SHA256,
        "top_k": TOP_K,
        "score_semantics": "HIGHER_IS_BETTER",
        "top20_binding_sha256": top20_binding_sha256(condition_id=condition_id, prompt_id=prompt["prompt_id"], prompt_sha256=prompt["prompt_sha256"], ordered_source_sha256=(item["source_sha256"] for item in candidates[:20])),
        "ranked_candidates": candidates,
        "cost": {"wall_time_ms": wall_time_ms, "provider_calls": 0, "input_tokens": 0, "output_tokens": 0, "window_forwards": 0, "cache_hits": 0, "retry_count": 0, "timeout_count": 0, "failure_count": 0},
    }


def validate_rows(rows: list[dict[str, Any]], prompts: list[dict[str, Any]], sources: set[str]) -> None:
    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    expected = {(f"{cell}-G0", prompt_id) for cell in CELLS.values() for prompt_id in prompt_by_id}
    actual: set[tuple[str, str]] = set()
    run_ids: set[str] = set()
    for index, row in enumerate(rows, 1):
        exact_keys(row, ROW_KEYS, f"row {index}")
        reject_outcome_keys(row)
        require(row["schema_version"] == ROW_SCHEMA and row["status"] == "SUCCESS", f"row {index}: schema/status drift")
        require(isinstance(row["run_id"], str) and row["run_id"], f"row {index}: run identity drift")
        run_ids.add(row["run_id"])
        require(row["prompt_id"] in prompt_by_id and row["prompt_sha256"] == prompt_by_id[row["prompt_id"]]["prompt_sha256"], f"row {index}: prompt binding drift")
        representation = row["representation"]
        require(representation in CELLS, f"row {index}: representation drift")
        cell = CELLS[representation]
        require(row["condition_id"] == f"{cell}-G0", f"row {index}: condition drift")
        require(row["first_stage_cell_id"] == cell, f"row {index}: first-stage cell drift")
        require(row["retriever"] == "BM25", f"row {index}: retriever drift")
        require(row["persisted_candidate_source"] == cell, f"row {index}: persisted source drift")
        require(row["source_union_sha256"] == SOURCE_UNION_SHA256, f"row {index}: source-union drift")
        require(row["top_k"] == TOP_K and row["score_semantics"] == "HIGHER_IS_BETTER", f"row {index}: ranking contract drift")
        candidates = row["ranked_candidates"]
        require(len(candidates) == TOP_K, f"row {index}: Top-100 required")
        previous: tuple[float, str] | None = None
        identities: list[str] = []
        for rank, candidate in enumerate(candidates, 1):
            exact_keys(candidate, {"rank", "source_sha256", "score"}, f"row {index}.candidate")
            require(isinstance(candidate["rank"], int) and not isinstance(candidate["rank"], bool) and candidate["rank"] == rank, f"row {index}: candidate rank drift")
            require(is_sha256(candidate["source_sha256"]) and candidate["source_sha256"] in sources, f"row {index}: candidate identity drift")
            require(isinstance(candidate["score"], (int, float)) and not isinstance(candidate["score"], bool), f"row {index}: candidate score type drift")
            current = (-float(candidate["score"]), candidate["source_sha256"])
            require(math.isfinite(float(candidate["score"])) and (previous is None or previous <= current), f"row {index}: score order drift")
            previous = current
            identities.append(candidate["source_sha256"])
        require(len(set(identities)) == TOP_K, f"row {index}: duplicate candidates")
        require(row["top20_binding_sha256"] == top20_binding_sha256(condition_id=row["condition_id"], prompt_id=row["prompt_id"], prompt_sha256=row["prompt_sha256"], ordered_source_sha256=identities[:20]), f"row {index}: Top-20 binding drift")
        exact_keys(row["cost"], COST_KEYS, f"row {index}.cost")
        require(all(isinstance(row["cost"][key], int) and not isinstance(row["cost"][key], bool) and row["cost"][key] == 0 for key in COST_KEYS - {"wall_time_ms"}), f"row {index}: non-wall BM25 cost must be integer zero")
        require(isinstance(row["cost"]["wall_time_ms"], (int, float)) and not isinstance(row["cost"]["wall_time_ms"], bool) and math.isfinite(row["cost"]["wall_time_ms"]) and row["cost"]["wall_time_ms"] >= 0, f"row {index}: wall time drift")
        key = (row["condition_id"], row["prompt_id"])
        require(key not in actual, f"row {index}: duplicate output key")
        actual.add(key)
    require(actual == expected, "Four-cell B1 coverage drift")
    require(len(run_ids) == 1, "B1 rows must share one run identity")


def execute(root: Path, authorisation_path: Path) -> dict[str, Any]:
    release, payload_path, payload = validate_root_release(root, authorisation_path)
    output_dir = release["_destinations"]["output_dir"]
    attempt_dir = release["_destinations"]["attempt_dir"]
    staging = output_dir.parent / f".{output_dir.name}.staging-{os.getpid()}"
    require(not staging.exists(), f"Stale staging directory: {staging}")
    started = time.perf_counter()
    attempt_dir.mkdir(parents=True, exist_ok=False)
    run_started = attempt_dir / "run_started.json"
    write_json_new(run_started, {
        "schema_version": "rq2b-v7-bm25-b1-run-start-v2",
        "run_id": release["run_id"],
        "attempt_id": release["attempt_id"],
        "root_release_id": release["root_release_id"],
        "payload_sha256": file_sha256(payload_path),
        "authorisation_sha256": file_sha256(authorisation_path),
        "started_at_utc": utc_now(),
    })
    try:
        prompts, sources, conditions, representations = load_inputs(root, payload)
        rows: list[dict[str, Any]] = []
        per_representation: dict[str, Any] = {}
        for representation, documents in representations.items():
            index_started = time.perf_counter()
            index = GlobalBM25(documents)
            index_seconds = time.perf_counter() - index_started
            query_seconds = 0.0
            for prompt in prompts:
                query_started = time.perf_counter()
                ranking = index.rank(prompt["prompt"], TOP_K)
                elapsed_ms = (time.perf_counter() - query_started) * 1000.0
                query_seconds += elapsed_ms / 1000.0
                rows.append(make_row(run_id=release["run_id"], representation=representation, condition=conditions[representation], prompt=prompt, ranking=ranking, wall_time_ms=elapsed_ms))
                require(time.perf_counter() - started <= release["ceilings"]["maximum_wall_time_seconds"], "Wall-time ceiling exceeded")
            per_representation[representation] = {"cell": CELLS[representation], "documents": len(documents), "queries": len(prompts), "index_seconds": index_seconds, "query_seconds": query_seconds}
        validate_rows(rows, prompts, sources)
        require(len(rows) <= release["ceilings"]["maximum_output_rows"], "Output-row ceiling exceeded")
        require(len(rows) * TOP_K <= release["ceilings"]["maximum_ranked_candidates"], "Candidate ceiling exceeded")
        staging.mkdir(parents=True, exist_ok=False)
        b1_path = staging / "b1.jsonl"
        write_jsonl_new(b1_path, rows)
        receipt = {
            "schema_version": RECEIPT_SCHEMA,
            "status": "COMPLETE_B01_B04_B07_B10_LABEL_FREE_BM25_B1_V2",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "root_release_id": release["root_release_id"],
            "runner": {"version": RUNNER_VERSION, "path": relative(Path(__file__), root), "sha256": file_sha256(Path(__file__))},
            "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
            "authorisation": {"path": relative(authorisation_path, root), "sha256": file_sha256(authorisation_path)},
            "phase8": release["phase8"],
            "method": payload["method"],
            "counts": {"queries": len(prompts), "sources": len(sources), "cells": 4, "rows": len(rows), "ranked_candidates": len(rows) * TOP_K},
            "per_representation": per_representation,
            "cost": {"wall_time_seconds": time.perf_counter() - started, "provider_calls": 0, "network_calls": 0, "model_forwards": 0, "automatic_retries": 0, "monetary_cost_usd": 0.0},
            "artifacts": {"b1": {"path": relative(output_dir / "b1.jsonl", root), "sha256": file_sha256(b1_path), "rows": len(rows)}},
            "completed_at_utc": utc_now(),
        }
        write_json_new(staging / "run_receipt.json", receipt)
        write_json_new(attempt_dir / "run_completed.json", {"schema_version": "rq2b-v7-bm25-b1-run-complete-v2", "run_id": release["run_id"], "b1_sha256": file_sha256(b1_path), "rows": len(rows), "completed_at_utc": utc_now()})
        staging.rename(output_dir)
        return receipt
    except Exception as error:
        write_json_new(attempt_dir / "run_failed.json", {"schema_version": "rq2b-v7-bm25-b1-run-failure-v2", "run_id": release["run_id"], "error_type": type(error).__name__, "error": str(error), "failed_at_utc": utc_now()})
        raise


def self_test() -> dict[str, Any]:
    sources = [f"{index:064x}" for index in range(120)]
    documents = [(source, "irrelevant content") for source in sources]
    documents[9] = (sources[9], "ocr scanned pdf ocr")
    documents[10] = (sources[10], "ocr native pdf")
    index = GlobalBM25(documents)
    require(index.rank("OCR scanned PDF")[0][0] == sources[9], "Synthetic relevance ordering failed")
    ties = index.rank("term-not-in-corpus")
    require([source for source, _ in ties] == sources[:TOP_K], "Synthetic SHA tie-break failed")
    require(all(score == 0.0 for _, score in ties), "Synthetic absent-term scores failed")
    require(set(FIXED_REPRESENTATIONS) == {"I1-discovery", "I2-original"}, "Final I3 hashes must remain payload-only")
    return {"status": "PASS_BM25_B1_V2_SYNTHETIC_NO_EXECUTION_SELF_TEST", "scientific_rows_created": 0, "network_calls": 0, "model_forwards": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--authorisation", type=Path)
    args = parser.parse_args()
    if args.self_test:
        report = self_test()
    else:
        require(args.authorisation is not None, "--authorisation is required")
        root = args.root.resolve()
        authorisation = args.authorisation if args.authorisation.is_absolute() else root / args.authorisation
        report = execute(root, authorisation)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
