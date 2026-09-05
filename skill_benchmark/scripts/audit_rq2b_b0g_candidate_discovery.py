#!/usr/bin/env python3
"""Validate a completed local B0G-CD pool without exposing benchmark text."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np


FORBIDDEN_TEXT_KEYS = {
    "prompt",
    "source_path",
    "source_text",
    "text",
}
SCORED_STRATA = frozenset({"controlled", "public_gold"})
TOP_K = 10


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeError(f"invalid JSONL at {path}:{line_number}") from error
            require(isinstance(row, dict), f"expected object at {path}:{line_number}")
            rows.append(row)
    return rows


def assert_no_raw_text(value: Any, location: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            require(key not in FORBIDDEN_TEXT_KEYS, f"raw-text key {key!r} found at {location}")
            assert_no_raw_text(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_raw_text(child, f"{location}[{index}]")


def load_source_metadata(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(path):
        skill_id = row["skill_id"]
        require(skill_id not in result, "duplicate source skill ID")
        result[skill_id] = {
            "source_chars": row["source_chars"],
            "source_sha256": row["source_sha256"],
        }
    require(len(result) == 2433, f"expected 2,433 sources, found {len(result)}")
    return result


def load_scored_prompts(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in read_jsonl(path):
        if row.get("stratum") not in SCORED_STRATA:
            continue
        prompt_id = row["prompt_id"]
        require(prompt_id not in result, "duplicate scored prompt ID")
        result[prompt_id] = row["prompt_sha256"]
    require(len(result) == 389, f"expected 389 scored prompts, found {len(result)}")
    return result


def load_scored_seeds(path: Path, prompt_ids: set[str]) -> dict[str, set[str]]:
    grouped = {prompt_id: set() for prompt_id in prompt_ids}
    all_rows = read_jsonl(path)
    included = 0
    excluded = 0
    for row in all_rows:
        if row["prompt_id"] not in grouped:
            excluded += 1
            continue
        grouped[row["prompt_id"]].add(row["candidate_skill_id"])
        included += 1
    require(len(all_rows) == 1914, "B0G-M v3 row count drift")
    require(included == 1862 and excluded == 52, "B0G-M scored/stress partition drift")
    return grouped


def validate_chunk_manifest(
    path: Path,
    source_metadata: dict[str, dict[str, Any]],
    expected_count: int,
) -> dict[str, int]:
    chunks = read_jsonl(path)
    assert_no_raw_text(chunks, path.name)
    require(len(chunks) == expected_count, f"unexpected chunk count in {path.name}")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    descriptors: set[str] = set()
    for row in chunks:
        skill_id = row["skill_id"]
        require(skill_id in source_metadata, "unknown chunk skill ID")
        require(row["source_sha256"] == source_metadata[skill_id]["source_sha256"], "chunk source hash mismatch")
        require(row["descriptor_sha256"] not in descriptors, "duplicate chunk descriptor")
        descriptors.add(row["descriptor_sha256"])
        grouped[skill_id].append(row)
    require(set(grouped) == set(source_metadata), "some sources have no chunks")
    for skill_id, values in grouped.items():
        values.sort(key=lambda row: row["chunk_index"])
        require([row["chunk_index"] for row in values] == list(range(len(values))), "non-contiguous chunk indices")
        require(values[0]["start_char"] == 0, "chunk coverage does not start at zero")
        require(values[-1]["end_char"] == source_metadata[skill_id]["source_chars"], "chunk coverage does not reach source end")
        previous_end = 0
        for row in values:
            require(0 <= row["start_char"] < row["end_char"], "invalid chunk range")
            require(row["start_char"] <= previous_end, "chunk coverage gap")
            previous_end = max(previous_end, row["end_char"])
    return {"chunk_count": len(chunks), "descriptor_count": len(descriptors)}


def validate_cache(cache_root: Path, channel: str, expected_batches: int, expected_chunks: int) -> dict[str, int]:
    directory = cache_root / channel.lower() / "document_batches"
    batches = sorted(directory.glob("batch-*.npz"))
    require(len(batches) == expected_batches, f"unexpected cached batch count for {channel}")
    seen = 0
    for path in batches:
        with np.load(path, allow_pickle=False) as payload:
            vectors = payload["embeddings"]
            descriptors = payload["descriptor_sha256"]
            require(vectors.ndim == 2 and vectors.shape[1] == 1024, f"cached dimension drift in {path.name}")
            require(vectors.shape[0] == descriptors.shape[0], f"cached row mismatch in {path.name}")
            require(bool(np.isfinite(vectors).all()), f"cached non-finite value in {path.name}")
            seen += int(vectors.shape[0])
    with np.load(cache_root / channel.lower() / "queries.npz", allow_pickle=False) as payload:
        vectors = payload["embeddings"]
        require(vectors.shape == (389, 1024), f"cached query shape drift for {channel}")
        require(bool(np.isfinite(vectors).all()), f"cached query non-finite value for {channel}")
    require(seen == expected_chunks, f"cached chunk total drift for {channel}")
    return {"batch_count": len(batches), "chunk_vectors": seen, "query_vectors": 389}


def validate_candidates(
    rows: list[dict[str, Any]],
    prompts: dict[str, str],
    sources: dict[str, dict[str, Any]],
    seeds: dict[str, set[str]],
    d1_chunks: set[str],
    d2_chunks: set[str],
) -> dict[str, Any]:
    assert_no_raw_text(rows, "candidate_pool")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_pairs: set[tuple[str, str]] = set()
    for row in rows:
        prompt_id = row["prompt_id"]
        skill_id = row["candidate_skill_id"]
        require(prompt_id in prompts and row["prompt_sha256"] == prompts[prompt_id], "candidate prompt identity drift")
        require(skill_id in sources, "candidate skill outside frozen inventory")
        require(row["candidate_source_sha256"] == sources[skill_id]["source_sha256"], "candidate source hash drift")
        require((prompt_id, skill_id) not in seen_pairs, "duplicate prompt-candidate row")
        seen_pairs.add((prompt_id, skill_id))
        channels = row["channels"]
        require(channels and set(channels).issubset({"S0", "D1", "D2", "Q0"}), "invalid channel membership")
        for channel in ("D1", "D2"):
            if channel not in channels:
                continue
            evidence = channels[channel]
            require(1 <= evidence["rank"] <= TOP_K, "invalid dense rank")
            require(isinstance(evidence["score"], (int, float)), "non-numeric dense score")
            chunk = evidence["winning_chunk"]
            require(chunk["skill_id"] == skill_id, "winning chunk belongs to another skill")
            require(chunk["descriptor_sha256"] in (d1_chunks if channel == "D1" else d2_chunks), "unknown winning chunk")
        grouped[prompt_id].append(row)
    require(set(grouped) == set(prompts), "candidate pool prompt coverage drift")

    total_d1 = total_d2 = total_q0 = total_s0 = 0
    for prompt_id, values in grouped.items():
        d1 = [row for row in values if "D1" in row["channels"]]
        d2 = [row for row in values if "D2" in row["channels"]]
        q0 = [row for row in values if "Q0" in row["channels"]]
        s0 = {row["candidate_skill_id"] for row in values if "S0" in row["channels"]}
        require(sorted(row["channels"]["D1"]["rank"] for row in d1) == list(range(1, TOP_K + 1)), "D1 Top-10 drift")
        require(sorted(row["channels"]["D2"]["rank"] for row in d2) == list(range(1, TOP_K + 1)), "D2 Top-10 drift")
        require(sorted(row["channels"]["Q0"]["sentinel_ordinal"] for row in q0) == [1, 2], "Q0 sentinel drift")
        require(s0 == seeds[prompt_id], "S0 seed retention drift")
        require(not {row["candidate_skill_id"] for row in q0} & (s0 | {row["candidate_skill_id"] for row in d1} | {row["candidate_skill_id"] for row in d2}), "Q0 collided with discovery union")
        total_d1 += len(d1)
        total_d2 += len(d2)
        total_q0 += len(q0)
        total_s0 += len(s0)
    return {
        "candidate_count": len(rows),
        "candidate_prompts": len(grouped),
        "d1_draws": total_d1,
        "d2_draws": total_d2,
        "q0_draws": total_q0,
        "s0_draws": total_s0,
    }


def write_json_new(path: Path, value: Any) -> None:
    require(not path.exists(), f"refusing to overwrite frozen validation: {path}")
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--prompt-manifest", type=Path, required=True)
    parser.add_argument("--seed-review-pool", type=Path, required=True)
    parser.add_argument("--discovery-dir", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    args = parser.parse_args()

    discovery = json.loads((args.discovery_dir / "discovery_manifest.json").read_text(encoding="utf-8"))
    require(discovery["state"] == "PASS", "discovery did not pass")
    require(discovery["external_requests"] == 0 and discovery["provider_calls"] == 0, "external activity recorded")
    require(not discovery["semantic_review_run"] and not discovery["primary_results_consumed"], "forbidden stage activity recorded")
    sources = load_source_metadata(args.source_manifest)
    prompts = load_scored_prompts(args.prompt_manifest)
    seeds = load_scored_seeds(args.seed_review_pool, set(prompts))
    d1 = validate_chunk_manifest(args.discovery_dir / "d1_chunk_manifest.jsonl", sources, 2443)
    d2 = validate_chunk_manifest(args.discovery_dir / "d2_chunk_manifest.jsonl", sources, 4932)
    rows = read_jsonl(args.discovery_dir / "candidate_pool.jsonl")
    candidate = validate_candidates(rows, prompts, sources, seeds, {row["descriptor_sha256"] for row in read_jsonl(args.discovery_dir / "d1_chunk_manifest.jsonl")}, {row["descriptor_sha256"] for row in read_jsonl(args.discovery_dir / "d2_chunk_manifest.jsonl")})
    cache = {
        "D1": validate_cache(args.cache_root, "D1", 1233, 2443),
        "D2": validate_cache(args.cache_root, "D2", 1337, 4932),
    }
    require(candidate["candidate_count"] == discovery["candidate_count"] == 7710, "candidate count drift")
    require(candidate["d1_draws"] == candidate["d2_draws"] == 3890, "dense draw count drift")
    require(candidate["q0_draws"] == 778 and candidate["s0_draws"] == 1862, "seed or sentinel draw count drift")
    report = {
        "schema_version": "rq2b-b0g-candidate-discovery-audit-v1",
        "state": "PASS",
        "candidate_pool_sha256": sha256_file(args.discovery_dir / "candidate_pool.jsonl"),
        "d1_chunk_manifest_sha256": sha256_file(args.discovery_dir / "d1_chunk_manifest.jsonl"),
        "d2_chunk_manifest_sha256": sha256_file(args.discovery_dir / "d2_chunk_manifest.jsonl"),
        "discovery_manifest_sha256": sha256_file(args.discovery_dir / "discovery_manifest.json"),
        "automatic_checks": {
            "cache": cache,
            "candidates": candidate,
            "d1_chunk_coverage": d1,
            "d2_chunk_coverage": d2,
            "raw_text_keys_absent": True,
            "semantic_review_run": False,
            "primary_results_consumed": False,
            "external_requests": 0,
            "provider_calls": 0,
        },
    }
    write_json_new(args.discovery_dir / "automatic_validation_report.json", report)
    print("B0G-CD automatic validation PASS: metadata-only output; semantic review not run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
