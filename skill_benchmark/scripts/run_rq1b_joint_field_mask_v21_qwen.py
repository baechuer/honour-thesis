#!/usr/bin/env python3
"""Execute an explicitly authorised Qwen embedding twin for RQ1b v2.1 joint masks."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
from pathlib import Path
from typing import Any

from prepare_rq1b_field_type_confirmatory_v2_qwen_preflight import BASE_URL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL
from prepare_rq1b_joint_field_mask_v21 import CONDITIONS, load_joint_scope
from prepare_rq1b_joint_field_mask_v21_qwen_preflight import PREFLIGHT_VERSION
from run_rq1b_field_type_confirmatory_v2_bm25 import metric_for_ranking
from run_rq1b_field_type_confirmatory_v2_qwen import cache_load, cache_store, chunks, cosine, load_dotenv, post_once
from run_rq1b_joint_field_mask_v21_bm25 import summarize


RUNNER_VERSION = "rq1b-joint-field-mask-v21-qwen-runner-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_authorisation(path: Path, payload_path: Path, output_dir: Path) -> dict[str, Any]:
    auth = json.loads(path.read_text())
    required = {
        "status": "RQ1B_JOINT_FIELD_MASK_V21_QWEN_ONE_RUN_AUTHORISED",
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "payload_sha256": sha256_file(payload_path),
        "output_dir": str(output_dir),
        "automatic_retries": 0,
    }
    for key, value in required.items():
        if auth.get(key) != value:
            raise ValueError(f"joint Qwen authorisation mismatch: {key}")
    for key in ("maximum_new_texts", "maximum_request_attempts", "maximum_successful_calls", "maximum_local_lexical_token_proxy", "maximum_utf8_bytes"):
        if not isinstance(auth.get(key), int) or auth[key] < 0:
            raise ValueError(f"joint Qwen authorisation ceiling missing: {key}")
    return auth


def embed_missing(payload: dict[str, Any], cache_root: Path, api_key: str, auth: dict[str, Any], progress: Path, timeout_seconds: int) -> tuple[dict[str, list[float]], dict[str, Any]]:
    inventory = {row["text_id"]: row for row in payload["text_inventory"]}
    cached = {identifier: cache_load(cache_root, row) for identifier, row in inventory.items()}
    missing = [row for identifier, row in inventory.items() if cached[identifier] is None]
    documents = [row for row in missing if any(role["kind"] == "document" for role in row["roles"])]
    queries = [row for row in missing if any(role["kind"] == "query" for role in row["roles"])]
    totals = {
        "texts": len(missing),
        "local_lexical_token_proxy": sum(row["local_lexical_token_proxy"] for row in missing),
        "utf8_bytes": sum(row["utf8_bytes"] for row in missing),
        "calls": len(chunks(documents)) + len(chunks(queries)),
    }
    for key, actual in {
        "maximum_new_texts": totals["texts"],
        "maximum_request_attempts": totals["calls"],
        "maximum_successful_calls": totals["calls"],
        "maximum_local_lexical_token_proxy": totals["local_lexical_token_proxy"],
        "maximum_utf8_bytes": totals["utf8_bytes"],
    }.items():
        if actual > auth[key]:
            raise ValueError(f"joint Qwen execution exceeds authorised ceiling: {key}")
    vectors = {identifier: vector for identifier, vector in cached.items() if vector is not None}
    progress.mkdir(parents=True, exist_ok=True)
    attempts = successful = 0
    provider_usage: dict[str, int] = {}
    for role, groups in (("document", chunks(documents)), ("query", chunks(queries))):
        for group in groups:
            if attempts >= auth["maximum_request_attempts"] or successful >= auth["maximum_successful_calls"]:
                raise ValueError("joint Qwen call ceiling reached before request")
            attempt = {"attempt": attempts + 1, "role": role, "text_ids": [row["text_id"] for row in group], "text_count": len(group), "automatic_retry": False}
            (progress / f"request_{attempts + 1:04d}_attempt.json").write_text(json.dumps(attempt, indent=2, sort_keys=True) + "\n")
            attempts += 1
            begun = time.perf_counter()
            try:
                response = post_once(api_key, [row["text"] for row in group], timeout_seconds)
            except Exception as exc:
                failure = {**attempt, "state": "failed_stop_no_retry", "error_type": type(exc).__name__, "error": str(exc)}
                (progress / f"request_{attempts:04d}_failure.json").write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n")
                raise RuntimeError(f"joint Qwen request {attempts} failed; no retry was attempted") from exc
            elapsed = time.perf_counter() - begun
            data, usage = response.get("data"), response.get("usage") or {}
            if not isinstance(data, list) or len(data) != len(group):
                raise ValueError("joint Qwen response count mismatch")
            ordered = sorted(data, key=lambda row: int(row["index"]))
            if [int(row["index"]) for row in ordered] != list(range(len(group))):
                raise ValueError("joint Qwen response index mismatch")
            receipt = {**attempt, "state": "success", "request_seconds": elapsed, "provider_usage": usage}
            (progress / f"request_{attempts:04d}_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            successful += 1
            for key, value in usage.items():
                if isinstance(value, int):
                    provider_usage[key] = provider_usage.get(key, 0) + value
            for row, item in zip(group, ordered, strict=True):
                vector = [float(value) for value in item.get("embedding", [])]
                if len(vector) != DIMENSIONS or not all(math.isfinite(value) for value in vector):
                    raise ValueError("joint Qwen returned invalid embedding")
                cache_store(cache_root, row, vector, receipt)
                vectors[row["text_id"]] = vector
            print(f"QWEN_PROGRESS request={attempts}/{totals['calls']} role={role} texts={len(group)} cache_written={len(group)}", flush=True)
    return vectors, {"cache_hits": len(inventory) - len(missing), "cache_misses": len(missing), "request_attempts": attempts, "successful_calls": successful, "provider_usage": provider_usage}


def run(payload_dir: Path, cache_root: Path, output_dir: Path, authorisation: Path, dotenv: Path, timeout_seconds: int) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite joint Qwen output: {output_dir}")
    payload_path = payload_dir / "payload.json"
    payload = json.loads(payload_path.read_text())
    if payload.get("status") != "RQ1B_JOINT_FIELD_MASK_V21_QWEN_PAYLOAD_LOCAL_PREFLIGHT_NOT_EXECUTED" or payload.get("preflight_version") != PREFLIGHT_VERSION:
        raise ValueError("unexpected joint Qwen payload status")
    auth = validate_authorisation(authorisation, payload_path, output_dir)
    joint_root = Path(payload["joint_root"])
    if payload.get("joint_freeze_sha256") != sha256_file(joint_root / "joint_mask_freeze.json"):
        raise ValueError("joint Qwen freeze binding drift")
    freeze, _, families, eligible = load_joint_scope(joint_root)
    if payload.get("conditions") != list(CONDITIONS) or payload["counts"].get("expected_score_rows") != len(families) * 2 * len(CONDITIONS):
        raise ValueError("joint Qwen payload scoring scope drift")
    load_dotenv(dotenv)
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY unavailable after loading configured dotenv")
    output_dir.mkdir(parents=True)
    vectors, execution = embed_missing(payload, cache_root, api_key, auth, output_dir / "requests", timeout_seconds)
    documents = {(row["composition_id"], row["condition"], row["candidate_label"]): row["text_id"] for row in payload["documents"]}
    queries = {(row["routing_family_id"], row["prompt_variant"]): row["text_id"] for row in payload["queries"]}
    rows: list[dict[str, Any]] = []
    for family in families:
        for variant in ("direct", "paraphrase"):
            query_vector = vectors[queries[(family["routing_family_id"], variant)]]
            for condition in CONDITIONS:
                cards = load_joint_condition(joint_root, freeze, family["composition_id"], condition)
                ranking = sorted(
                    ((card["label"], cosine(query_vector, vectors[documents[(family["composition_id"], condition, card["label"])]])) for card in cards),
                    key=lambda item: (-item[1], item[0]),
                )
                rows.append({"status": "RQ1B_JOINT_FIELD_MASK_V21_QWEN_ROW_EXTERNAL_RESULT", "retriever": "qwen-text-embedding-v4", "routing_family_id": family["routing_family_id"], "composition_id": family["composition_id"], "prompt_variant": variant, "condition": condition, "gold_label": family["gold_label"], "candidate_count": len(cards), "query_seconds": None, **metric_for_ranking(ranking, family["gold_label"])})
    if len(rows) != payload["counts"]["expected_score_rows"]:
        raise ValueError("joint Qwen score-row coverage mismatch")
    summary = summarize(rows, eligible)
    (output_dir / "rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    manifest = {"status": "RQ1B_JOINT_FIELD_MASK_V21_QWEN_RUN_EXTERNAL_RESULT", "runner_version": RUNNER_VERSION, "payload_sha256": sha256_file(payload_path), "authorisation_sha256": sha256_file(authorisation), "execution": execution, "artifacts": {"rows.jsonl": sha256_file(output_dir / "rows.jsonl"), "summary.json": sha256_file(output_dir / "summary.json")}, "thesis_results_written": False}
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload-dir", type=Path)
    parser.add_argument("--cache-root", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--dotenv", type=Path, default=Path(".env"))
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    if any(value is None for value in (args.payload_dir, args.cache_root, args.output_dir, args.authorisation)):
        raise ValueError("payload, cache, output and authorisation paths are required")
    print(json.dumps(run(args.payload_dir, args.cache_root, args.output_dir, args.authorisation, args.dotenv, args.timeout_seconds), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
