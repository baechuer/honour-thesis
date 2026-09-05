#!/usr/bin/env python3
"""Independently verify the immutable V3 B2 Top-20 preflight locally."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from prepare_rq2bv1_v3_b2_top20_preflight import (
    B1_RESULT_SOURCES,
    CONDITION_SCHEMA,
    FORBIDDEN_PROVIDER_KEYS,
    PAIR_MAX_TOKENS,
    PREFLIGHT_DIR,
    PREFLIGHT_SCHEMA,
    PRIMARY_K,
    ROOT,
    read_json,
    read_jsonl,
    relative,
    require,
    sha256_file,
    sha256_json,
    write_json,
)


def verify(root: Path, directory: Path) -> dict[str, Any]:
    manifest = read_json(directory / "manifest.json")
    report_path = root / manifest["preflight_report"]["path"]
    require(report_path == directory / "preflight_report.json", "Preflight report final-path binding drift")
    require(sha256_file(report_path) == manifest["preflight_report"]["sha256"], "Preflight report hash drift")
    report = read_json(report_path)
    require(report["schema_version"] == PREFLIGHT_SCHEMA, "Preflight report schema drift")
    require(report["state"] == "prepared_local_zero_network_no_reranker_execution", "Unexpected preflight state")
    require(report["boundary"]["network_calls"] == report["boundary"]["provider_text_submissions"] == report["boundary"]["model_forward_passes"] == 0, "Preflight crossed execution boundary")

    artifacts = report["artifacts"]
    paths: dict[str, Path] = {}
    rows: dict[str, list[dict[str, Any]]] = {}
    for name, binding in artifacts.items():
        path = root / binding["path"]
        require(path.is_file(), f"Missing final preflight artifact: {name}")
        require(path.parent == directory, f"Preflight artifact is not in final output root: {name}")
        require(".staging" not in str(path), f"Preflight artifact refers to staging: {name}")
        require(sha256_file(path) == binding["sha256"], f"Preflight artifact hash drift: {name}")
        value = read_jsonl(path)
        require(len(value) == int(binding["rows"]), f"Preflight artifact row count drift: {name}")
        paths[name], rows[name] = path, value

    conditions = rows["conditions"]
    private = rows["strict_bindings"]
    pairs = rows["unique_pairs"]
    require(len(conditions) == len(private) == 4572, "B2 condition count drift")
    require(len(pairs) == 73415, "B2 unique pair count drift")
    pair_by_id = {row["pair_id"]: row for row in pairs}
    private_by_id = {row["condition_id"]: row for row in private}
    require(len(pair_by_id) == len(pairs), "Duplicate B2 pair IDs")
    require(len(private_by_id) == len(private), "Duplicate strict bindings")

    b1_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    source_by_name = {name: (relative_path, retriever) for name, relative_path, retriever in B1_RESULT_SOURCES}
    for source_name, relative_path, expected_retriever in B1_RESULT_SOURCES:
        source_rows = read_jsonl(root / relative_path)
        for row in source_rows:
            key = (source_name, row["representation"], row["prompt_id"])
            require(key not in b1_by_key, f"Duplicate B1 source condition: {key}")
            require(row["retriever"] == expected_retriever, f"B1 retriever drift: {key}")
            b1_by_key[key] = row
    require(len(b1_by_key) == 4572, "Completed B1 matrix coverage drift")

    referenced_pair_ids: set[str] = set()
    for condition in conditions:
        require(condition["schema_version"] == CONDITION_SCHEMA, "B2 condition schema drift")
        require(not (set(condition) & FORBIDDEN_PROVIDER_KEYS), "Provider condition label leakage")
        condition_id = condition["condition_id"]
        private_row = private_by_id.get(condition_id)
        require(private_row is not None, f"Missing private strict binding: {condition_id}")
        require(len(condition["candidate_skill_ids"]) == PRIMARY_K, "B2 candidate count drift")
        require(len(set(condition["candidate_skill_ids"])) == PRIMARY_K, "B2 duplicate candidate")
        require(condition["candidate_list_sha256"] == sha256_json(condition["candidate_skill_ids"]), "B2 candidate list hash drift")
        require(condition["candidate_skill_ids"] == [row["skill_id"] for row in condition["candidates"]], "B2 candidate order drift")
        b1_row = b1_by_key[(condition["b1_source"], condition["representation"], condition["prompt_id"])]
        require(condition["first_stage_retriever"] == b1_row["retriever"], "B2 first-stage retriever drift")
        require(condition["candidate_skill_ids"] == b1_row["top_20_skill_ids"], "B2 mutated persisted Top-20")
        require(private_row["strict_candidate_positive"] == int(private_row["gold_skill"] in condition["candidate_skill_ids"]), "Strict candidate-positive drift")
        for candidate in condition["candidates"]:
            require(candidate["skill_id"] in condition["candidate_skill_ids"], "Candidate outside Top-20")
            require(candidate["windows"], "Candidate has no selector-visible windows")
            for window in candidate["windows"]:
                pair = pair_by_id.get(window["pair_id"])
                require(pair is not None, "Condition references missing unique pair")
                require(pair["prompt_id"] == condition["prompt_id"] and pair["representation"] == condition["representation"], "Pair condition provenance drift")
                require(pair["skill_id"] == candidate["skill_id"], "Pair candidate identity drift")
                require(pair["window_text"] == window["text"], "Pair selector-visible text drift")
                require(pair["window_text_sha256"] == window["text_sha256"], "Pair text hash drift")
                require(int(pair["pair_input_token_count"]) <= PAIR_MAX_TOKENS, "Pair token limit drift")
                referenced_pair_ids.add(pair["pair_id"])
    require(referenced_pair_ids == set(pair_by_id), "Unique pair inventory has orphan or missing pair")

    return {
        "schema_version": "rq2bv1-v3-b2-top20-preflight-verification-v1",
        "state": "passed_local_preflight_integrity_verification",
        "preflight_manifest": {"path": relative(directory / "manifest.json", root), "sha256": sha256_file(directory / "manifest.json")},
        "checks": {
            "strict_b1_conditions": len(b1_by_key),
            "b2_conditions": len(conditions),
            "private_strict_bindings": len(private),
            "unique_pairs": len(pairs),
            "top20_order_bound_to_completed_b1": len(conditions),
            "provider_label_leakage_conditions": 0,
            "pair_token_limit_violations": 0,
            "network_calls": 0,
            "model_forward_passes": 0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--directory", type=Path, default=Path(PREFLIGHT_DIR))
    args = parser.parse_args()
    root = args.root.resolve()
    directory = args.directory if args.directory.is_absolute() else root / args.directory
    result = verify(root, directory)
    output = directory / "preflight_verification.json"
    write_json(output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
