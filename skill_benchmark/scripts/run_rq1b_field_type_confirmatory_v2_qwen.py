#!/usr/bin/env python3
"""Execute the explicitly authorised Qwen embedding twin of RQ1b v2.

The script is fail-stop and has no automatic retry. It reads a sealed local
payload, persists exact-text embeddings locally and scores only each frozen
composition's own candidate set.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any

from prepare_rq1b_field_type_confirmatory_v2_qwen_preflight import BASE_URL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL
from run_rq1b_field_type_confirmatory_v2_bm25 import CONDITIONS, load_strict_families, metric_for_ranking, summarize


RUNNER_VERSION = "rq1b-field-type-v2-qwen-runner-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def cache_load(cache_root: Path, row: dict[str, Any]) -> list[float] | None:
    path = cache_root / f"{row['text_id']}.json"
    if not path.is_file():
        return None
    payload = json.loads(path.read_text())
    if (
        payload.get("schema_version") != "rq1b-field-type-v2-qwen-cache-v1"
        or payload.get("base_url") != BASE_URL
        or payload.get("model") != MODEL
        or payload.get("dimensions") != DIMENSIONS
        or payload.get("text_id") != row["text_id"]
    ):
        raise ValueError(f"Qwen cache binding invalid: {path}")
    vector = payload.get("embedding")
    if not isinstance(vector, list) or len(vector) != DIMENSIONS:
        raise ValueError(f"Qwen cache vector invalid: {path}")
    values = [float(value) for value in vector]
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f"Qwen cache has non-finite vector: {path}")
    return values


def cache_store(cache_root: Path, row: dict[str, Any], vector: list[float], request_record: dict[str, Any]) -> None:
    cache_root.mkdir(parents=True, exist_ok=True)
    path = cache_root / f"{row['text_id']}.json"
    if path.exists():
        raise ValueError(f"refusing to overwrite Qwen cache: {path}")
    payload = {
        "schema_version": "rq1b-field-type-v2-qwen-cache-v1",
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "text_id": row["text_id"],
        "text_sha256": row["text_id"],
        "local_lexical_token_proxy": row["local_lexical_token_proxy"],
        "provider_usage": request_record.get("provider_usage", {}),
        "embedding": vector,
    }
    temporary = cache_root / f".{row['text_id']}.tmp"
    temporary.write_text(json.dumps(payload, sort_keys=True) + "\n")
    temporary.replace(path)


def l2(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if not norm or not math.isfinite(norm):
        raise ValueError("invalid Qwen vector norm")
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(l2(left), l2(right), strict=True))


def post_once(api_key: str, texts: list[str], timeout_seconds: int) -> dict[str, Any]:
    body = json.dumps({"model": MODEL, "input": texts, "dimensions": DIMENSIONS, "encoding_format": "float"}, ensure_ascii=False).encode()
    request = urllib.request.Request(
        f"{BASE_URL}/embeddings",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        payload = json.loads(response.read().decode())
    if not isinstance(payload, dict):
        raise ValueError("Qwen response is not an object")
    return payload


def chunks(rows: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    return [rows[index:index + MAX_BATCH_TEXTS] for index in range(0, len(rows), MAX_BATCH_TEXTS)]


def validate_authorisation(path: Path, payload_path: Path, output_dir: Path) -> dict[str, Any]:
    auth = json.loads(path.read_text())
    required = {
        "status": "RQ1B_FIELD_TYPE_V2_QWEN_ONE_RUN_AUTHORISED",
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "payload_sha256": sha256_file(payload_path),
        "output_dir": str(output_dir),
        "automatic_retries": 0,
    }
    for key, value in required.items():
        if auth.get(key) != value:
            raise ValueError(f"Qwen authorisation mismatch: {key}")
    for key in ("maximum_new_texts", "maximum_request_attempts", "maximum_successful_calls", "maximum_local_lexical_token_proxy", "maximum_utf8_bytes"):
        if not isinstance(auth.get(key), int) or auth[key] < 0:
            raise ValueError(f"Qwen authorisation ceiling missing: {key}")
    return auth


def embed_missing(
    payload: dict[str, Any], cache_root: Path, api_key: str, auth: dict[str, Any], progress: Path, timeout_seconds: int
) -> tuple[dict[str, list[float]], dict[str, Any]]:
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
    ceilings = {
        "maximum_new_texts": totals["texts"],
        "maximum_request_attempts": totals["calls"],
        "maximum_successful_calls": totals["calls"],
        "maximum_local_lexical_token_proxy": totals["local_lexical_token_proxy"],
        "maximum_utf8_bytes": totals["utf8_bytes"],
    }
    for key, actual in ceilings.items():
        if actual > auth[key]:
            raise ValueError(f"Qwen execution exceeds authorised ceiling: {key}")
    vectors = {identifier: vector for identifier, vector in cached.items() if vector is not None}
    progress.mkdir(parents=True, exist_ok=True)
    attempts = successful = 0
    provider_usage: dict[str, int] = {}
    total_calls = totals["calls"]
    for role, groups in (("document", chunks(documents)), ("query", chunks(queries))):
        for group in groups:
            if attempts >= auth["maximum_request_attempts"] or successful >= auth["maximum_successful_calls"]:
                raise ValueError("Qwen call ceiling reached before request")
            attempt = {"attempt": attempts + 1, "role": role, "text_ids": [row["text_id"] for row in group], "text_count": len(group), "automatic_retry": False}
            (progress / f"request_{attempts + 1:04d}_attempt.json").write_text(json.dumps(attempt, indent=2, sort_keys=True) + "\n")
            attempts += 1
            begun = time.perf_counter()
            try:
                response = post_once(api_key, [row["text"] for row in group], timeout_seconds)
            except Exception as exc:
                failure = {**attempt, "state": "failed_stop_no_retry", "error_type": type(exc).__name__, "error": str(exc)}
                (progress / f"request_{attempts:04d}_failure.json").write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n")
                raise RuntimeError(f"Qwen request {attempts} failed; no retry was attempted") from exc
            elapsed = time.perf_counter() - begun
            data, usage = response.get("data"), response.get("usage") or {}
            if not isinstance(data, list) or len(data) != len(group):
                raise ValueError("Qwen response count mismatch")
            ordered = sorted(data, key=lambda row: int(row["index"]))
            if [int(row["index"]) for row in ordered] != list(range(len(group))):
                raise ValueError("Qwen response index mismatch")
            receipt = {**attempt, "state": "success", "request_seconds": elapsed, "provider_usage": usage}
            (progress / f"request_{attempts:04d}_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            successful += 1
            for key, value in usage.items():
                if isinstance(value, int):
                    provider_usage[key] = provider_usage.get(key, 0) + value
            for row, item in zip(group, ordered, strict=True):
                vector = [float(value) for value in item.get("embedding", [])]
                if len(vector) != DIMENSIONS or not all(math.isfinite(value) for value in vector):
                    raise ValueError("Qwen returned invalid embedding")
                cache_store(cache_root, row, vector, receipt)
                vectors[row["text_id"]] = vector
            print(
                f"QWEN_PROGRESS request={attempts}/{total_calls} role={role} texts={len(group)} cache_written={len(group)}",
                flush=True,
            )
    return vectors, {"cache_hits": len(inventory) - len(missing), "cache_misses": len(missing), "request_attempts": attempts, "successful_calls": successful, "provider_usage": provider_usage}


def run(payload_dir: Path, cache_root: Path, output_dir: Path, authorisation_path: Path, dotenv: Path, timeout_seconds: int) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite Qwen output: {output_dir}")
    payload_path = payload_dir / "payload.json"
    payload = json.loads(payload_path.read_text())
    if payload.get("status") != "RQ1B_FIELD_TYPE_V2_QWEN_PAYLOAD_LOCAL_PREFLIGHT_NOT_EXECUTED":
        raise ValueError("unexpected Qwen payload state")
    auth = validate_authorisation(authorisation_path, payload_path, output_dir)
    load_dotenv(dotenv)
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY unavailable after loading configured dotenv")
    output_dir.mkdir(parents=True)
    vectors, execution = embed_missing(payload, cache_root, api_key, auth, output_dir / "requests", timeout_seconds)
    docs = {(row["composition_id"], row["condition"], row["candidate_label"]): row["text_id"] for row in payload["documents"]}
    queries = {(row["routing_family_id"], row["prompt_variant"]): row["text_id"] for row in payload["queries"]}
    families, eligible = load_strict_families(Path(payload["root"]))
    rows = []
    for family in families:
        family_id = family["routing_family_id"]
        composition_id = family["composition_id"]
        gold_label = family["gold_label"]
        for variant in ("direct", "paraphrase"):
            query_vector = vectors[queries[(family_id, variant)]]
            for condition in CONDITIONS:
                candidate_rows = [row for row in payload["documents"] if row["composition_id"] == composition_id and row["condition"] == condition]
                ranking = sorted(((row["candidate_label"], cosine(query_vector, vectors[row["text_id"]])) for row in candidate_rows), key=lambda item: (-item[1], item[0]))
                rows.append({"status": "RQ1B_FIELD_TYPE_V2_QWEN_ROW_EXTERNAL_RESULT", "retriever": "qwen-text-embedding-v4", "routing_family_id": family_id, "composition_id": composition_id, "prompt_variant": variant, "condition": condition, "gold_label": gold_label, "candidate_count": len(candidate_rows), "query_seconds": None, **metric_for_ranking(ranking, gold_label)})
    if len(rows) != payload["counts"]["expected_score_rows"]:
        raise ValueError("Qwen score-row coverage mismatch")
    summary = summarize(rows, eligible)
    (output_dir / "rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    manifest = {"status": "RQ1B_FIELD_TYPE_V2_QWEN_RUN_EXTERNAL_RESULT", "runner_version": RUNNER_VERSION, "payload_sha256": sha256_file(payload_path), "authorisation_sha256": sha256_file(authorisation_path), "execution": execution, "artifacts": {"rows.jsonl": sha256_file(output_dir / "rows.jsonl"), "summary.json": sha256_file(output_dir / "summary.json")}, "thesis_results_written": False}
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
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        row = {"text_id": "synthetic", "local_lexical_token_proxy": 2}
        vector = [1.0] * DIMENSIONS
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache_store(root, row, vector, {"provider_usage": {}})
            if cache_load(root, row) != vector or abs(cosine(vector, vector) - 1.0) > 1e-9:
                raise ValueError("Qwen local cache/cosine self-test failed")
        print(json.dumps({"status": "pass_synthetic_no_external_call", "network_calls": 0}, sort_keys=True))
        return
    if any(value is None for value in (args.payload_dir, args.cache_root, args.output_dir, args.authorisation)):
        raise ValueError("payload, cache, output and authorisation paths are required for execution")
    print(json.dumps(run(args.payload_dir, args.cache_root, args.output_dir, args.authorisation, args.dotenv, args.timeout_seconds), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
