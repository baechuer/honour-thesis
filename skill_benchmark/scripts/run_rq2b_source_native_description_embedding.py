#!/usr/bin/env python3
"""Execute one authorised native-description embedding payload with no retry."""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import math
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PAYLOAD_DIR = NC_ROOT / "manifests/source_native_description_embedding_preflight_2026-09-04"
PAYLOAD_PATH = PAYLOAD_DIR / "payload.json"
AUTHORISATION_PATH = PAYLOAD_DIR / "execution_authorisation.json"
OUTPUT_DIR = NC_ROOT / "review/source_native_description_embedding_run_2026-09-04"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def post_once(api_key: str, base_url: str, model: str, dimensions: int, texts: list[str], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{base_url}/embeddings",
        data=json.dumps({"model": model, "input": texts, "dimensions": dimensions, "encoding_format": "float"}, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("Embedding response is not an object")
    return payload


def validate(payload: dict[str, Any], authorisation: dict[str, Any]) -> None:
    if payload.get("status") != "RQ2B_SOURCE_NATIVE_DESCRIPTION_DENSE_PREFLIGHT_NOT_EXECUTED":
        raise RuntimeError("Unexpected payload status")
    if authorisation.get("state") != "EXPLICIT_USER_AUTHORISATION_RECORDED_PENDING_EXECUTION":
        raise RuntimeError("Execution authorisation state does not permit this run")
    if authorisation.get("payload_sha256") != sha256_file(PAYLOAD_PATH):
        raise RuntimeError("Payload hash does not match execution authorisation")
    for key in ("base_url", "model", "dimensions"):
        if authorisation.get(key) != payload.get(key):
            raise RuntimeError(f"Authorisation mismatch: {key}")
    if authorisation.get("automatic_retries") != 0:
        raise RuntimeError("Automatic retries are prohibited")
    inventory = payload.get("text_inventory")
    if not isinstance(inventory, list) or not inventory:
        raise RuntimeError("Missing text inventory")
    text_ids = [str(row.get("text_id")) for row in inventory]
    if len(text_ids) != len(set(text_ids)):
        raise RuntimeError("Text inventory IDs are not unique")
    if any(not isinstance(row.get("text"), str) or not row["text"] for row in inventory):
        raise RuntimeError("Text inventory has an invalid description")
    expected_calls = math.ceil(len(inventory) / int(payload["max_batch_texts"]))
    if authorisation.get("maximum_new_texts") != len(inventory):
        raise RuntimeError("Authorised text count mismatch")
    if authorisation.get("maximum_request_attempts") != expected_calls:
        raise RuntimeError("Authorised request-attempt count mismatch")
    if authorisation.get("maximum_successful_calls") != expected_calls:
        raise RuntimeError("Authorised successful-call count mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Perform the pre-authorised network requests.")
    args = parser.parse_args()
    if not args.execute:
        raise SystemExit("Refusing to contact provider without --execute")
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Refusing to overwrite output directory: {OUTPUT_DIR}")
    if not PAYLOAD_PATH.is_file() or not AUTHORISATION_PATH.is_file():
        raise SystemExit("Missing frozen payload or execution authorisation")
    payload = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    authorisation = json.loads(AUTHORISATION_PATH.read_text(encoding="utf-8"))
    validate(payload, authorisation)
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise SystemExit("DASHSCOPE_API_KEY is unavailable in the process environment")

    inventory = payload["text_inventory"]
    batch_size = int(payload["max_batch_texts"])
    dimensions = int(payload["dimensions"])
    request_count = math.ceil(len(inventory) / batch_size)
    OUTPUT_DIR.mkdir(parents=True)
    receipts_dir = OUTPUT_DIR / "requests"
    receipts_dir.mkdir()
    (OUTPUT_DIR / "text_ids.jsonl").write_text(
        "".join(json.dumps({"index": index, "text_id": row["text_id"], "text_sha256": row["text_sha256"]}, sort_keys=True) + "\n" for index, row in enumerate(inventory)),
        encoding="utf-8",
    )
    vectors_path = OUTPUT_DIR / "embeddings.float32"
    usage_totals: dict[str, int] = {}
    successful = 0
    if array.array("f").itemsize != 4:
        raise RuntimeError("Host float representation is not four bytes")
    with vectors_path.open("wb") as vector_handle:
        for request_index, start in enumerate(range(0, len(inventory), batch_size), start=1):
            batch = inventory[start:start + batch_size]
            attempt = {
                "request_index": request_index,
                "request_count": request_count,
                "text_ids": [row["text_id"] for row in batch],
                "text_count": len(batch),
                "automatic_retry": False,
            }
            write_json(receipts_dir / f"request_{request_index:04d}_attempt.json", attempt)
            begun = time.perf_counter()
            try:
                response = post_once(api_key, str(payload["base_url"]), str(payload["model"]), dimensions, [row["text"] for row in batch], int(payload["timeout_seconds"]))
            except Exception as error:
                write_json(receipts_dir / f"request_{request_index:04d}_failure.json", {
                    **attempt,
                    "state": "FAILED_STOP_NO_RETRY",
                    "error_type": type(error).__name__,
                    "error": str(error),
                })
                raise RuntimeError(f"Request {request_index} failed; no retry was attempted") from error
            data = response.get("data")
            if not isinstance(data, list) or len(data) != len(batch):
                raise RuntimeError(f"Provider response count mismatch at request {request_index}")
            ordered = sorted(data, key=lambda item: int(item["index"]))
            if [int(item["index"]) for item in ordered] != list(range(len(batch))):
                raise RuntimeError(f"Provider response index mismatch at request {request_index}")
            for item in ordered:
                vector = [float(value) for value in item.get("embedding", [])]
                if len(vector) != dimensions or not all(math.isfinite(value) for value in vector):
                    raise RuntimeError(f"Invalid embedding at request {request_index}")
                array.array("f", vector).tofile(vector_handle)
            vector_handle.flush()
            usage = response.get("usage") if isinstance(response.get("usage"), dict) else {}
            for key, value in usage.items():
                if isinstance(value, int):
                    usage_totals[key] = usage_totals.get(key, 0) + value
            successful += 1
            write_json(receipts_dir / f"request_{request_index:04d}_receipt.json", {
                **attempt,
                "state": "SUCCESS",
                "request_seconds": time.perf_counter() - begun,
                "provider_usage": usage,
            })
            print(f"DENSE_PROGRESS request={request_index}/{request_count} texts={len(batch)}", flush=True)

    expected_bytes = len(inventory) * dimensions * 4
    if vectors_path.stat().st_size != expected_bytes:
        raise RuntimeError("Embedding binary length mismatch")
    with vectors_path.open("rb") as vector_handle:
        for index in range(len(inventory)):
            vector = array.array("f")
            try:
                vector.fromfile(vector_handle, dimensions)
            except EOFError as error:
                raise RuntimeError(f"Embedding binary ends early at index {index}") from error
            if len(vector) != dimensions or not all(math.isfinite(value) for value in vector):
                raise RuntimeError(f"Embedding integrity failed at index {index}")
            if not any(value != 0.0 for value in vector):
                raise RuntimeError(f"Embedding has zero norm at index {index}")
    result = {
        "status": "PASS_SOURCE_NATIVE_DESCRIPTION_DENSE_EMBEDDINGS_DISCOVERY_AID_ONLY",
        "payload_sha256": sha256_file(PAYLOAD_PATH),
        "authorisation_sha256": sha256_file(AUTHORISATION_PATH),
        "counts": {"unique_description_texts": len(inventory), "successful_calls": successful, "request_attempts": successful, "dimensions": dimensions},
        "provider_usage": usage_totals,
        "artifacts": {"embeddings.float32": sha256_file(vectors_path), "text_ids.jsonl": sha256_file(OUTPUT_DIR / "text_ids.jsonl")},
        "claim_boundary": "Embeddings rank source-native descriptions only; they are not source cards, clusters, labels, prompts, acceptable sets, selectors, or metrics.",
    }
    write_json(OUTPUT_DIR / "manifest.json", result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
