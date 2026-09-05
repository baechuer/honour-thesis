#!/usr/bin/env python3
"""Freeze the public native-description embedding payload; make no API calls."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CORPUS_DIR = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04"
CORPUS = CORPUS_DIR / "source_native_description_corpus.jsonl"
CORPUS_SUMMARY = CORPUS_DIR / "summary.json"
OUTPUT_DIR = NC_ROOT / "manifests/source_native_description_embedding_preflight_2026-09-04"

BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
MODEL = "text-embedding-v4"
DIMENSIONS = 1024
MAX_BATCH_TEXTS = 10
TIMEOUT_SECONDS = 60


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def lexical_token_proxy(value: str) -> int:
    return len(re.findall(r"\S+", value))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def main() -> int:
    required = [PROTOCOL, CORPUS, CORPUS_SUMMARY]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Output directory already exists: {OUTPUT_DIR}")

    rows = read_jsonl(CORPUS)
    if len(rows) != 23_450:
        raise SystemExit("Native-description corpus must bind exactly 23,450 sources")
    eligible = [row for row in rows if row.get("index_eligibility") is True]
    if len(eligible) != 23_431:
        raise SystemExit("Expected exactly 23,431 literal-replayed native descriptions")
    if any(row.get("native_description_replay_status") != "LITERAL_REPLAY_PASS" for row in eligible):
        raise SystemExit("Eligible description lacks literal source replay")

    texts: dict[str, dict[str, Any]] = {}
    source_bindings: list[dict[str, Any]] = []
    for row in eligible:
        text = str(row["native_description"])
        text_hash = sha256_text(text)
        texts.setdefault(text_hash, {
            "text_id": text_hash,
            "text": text,
            "text_sha256": text_hash,
            "utf8_bytes": len(text.encode("utf-8")),
            "local_lexical_token_proxy": lexical_token_proxy(text),
            "role": "native_source_description",
            "scope": "PUBLIC_ORIGINAL_SOURCE_DESCRIPTION_ONLY",
        })
        source_bindings.append({
            "canonical_source_sha256": row["canonical_source_sha256"],
            "text_id": text_hash,
            "native_description_sha256": row["native_description_sha256"],
            "source_paths": row["source_paths"],
            "population_membership": row["population_membership"],
            "claim_boundary": "Binding only; source identity is excluded from embedding text.",
        })
    text_rows = sorted(texts.values(), key=lambda row: row["text_id"])
    source_bindings.sort(key=lambda row: row["canonical_source_sha256"])
    calls = math.ceil(len(text_rows) / MAX_BATCH_TEXTS)
    payload = {
        "status": "RQ2B_SOURCE_NATIVE_DESCRIPTION_DENSE_PREFLIGHT_NOT_EXECUTED",
        "schema_version": "rq2b-source-native-description-dense-payload-v1",
        "protocol": relative(PROTOCOL),
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "max_batch_texts": MAX_BATCH_TEXTS,
        "timeout_seconds": TIMEOUT_SECONDS,
        "text_inventory": text_rows,
        "counts": {
            "bound_sources": len(source_bindings),
            "excluded_nonreplayable_descriptions": len(rows) - len(eligible),
            "unique_description_texts": len(text_rows),
            "maximum_request_attempts_no_retry": calls,
            "maximum_successful_calls_no_retry": calls,
            "maximum_utf8_bytes": sum(row["utf8_bytes"] for row in text_rows),
            "maximum_local_lexical_token_proxy": sum(row["local_lexical_token_proxy"] for row in text_rows),
        },
        "claim_boundary": [
            "Only exact public original source descriptions are eligible for transfer.",
            "No title, heading, full source body, prompt, cluster, provenance, label or review result is transferred.",
            "Embeddings are discovery aids only and produce no cluster, prompt, label, acceptable-set, selector or metric.",
        ],
    }
    OUTPUT_DIR.mkdir(parents=True)
    payload_path = OUTPUT_DIR / "payload.json"
    bindings_path = OUTPUT_DIR / "source_to_text_bindings.jsonl"
    write_json(payload_path, payload)
    write_jsonl(bindings_path, source_bindings)
    authorisation = {
        "schema_version": "rq2b-source-native-description-dense-execution-authorisation-v1",
        "state": "EXPLICIT_USER_AUTHORISATION_RECORDED_PENDING_EXECUTION",
        "user_authorisation_record": "2026-09-04 user approved the source-native SOP and instructed the work to begin continuously.",
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "payload_sha256": sha256_file(payload_path),
        "automatic_retries": 0,
        "maximum_new_texts": len(text_rows),
        "maximum_request_attempts": calls,
        "maximum_successful_calls": calls,
        "maximum_utf8_bytes": payload["counts"]["maximum_utf8_bytes"],
        "maximum_local_lexical_token_proxy": payload["counts"]["maximum_local_lexical_token_proxy"],
        "scope": "Public original native descriptions only; local persistence; source-to-source cluster discovery only.",
    }
    authorisation_path = OUTPUT_DIR / "execution_authorisation.json"
    write_json(authorisation_path, authorisation)
    manifest = {
        "status": "PASS_SOURCE_NATIVE_DESCRIPTION_DENSE_PREFLIGHT_NO_EXTERNAL_CALL",
        "bound_inputs": {
            relative(CORPUS): sha256_file(CORPUS),
            relative(CORPUS_SUMMARY): sha256_file(CORPUS_SUMMARY),
        },
        "outputs": {
            "payload.json": sha256_file(payload_path),
            "source_to_text_bindings.jsonl": sha256_file(bindings_path),
            "execution_authorisation.json": sha256_file(authorisation_path),
        },
        "counts": payload["counts"],
        "claim_boundary": payload["claim_boundary"],
    }
    write_json(OUTPUT_DIR / "manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
