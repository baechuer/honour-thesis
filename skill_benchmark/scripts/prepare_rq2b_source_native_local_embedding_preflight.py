#!/usr/bin/env python3
"""Freeze an on-device BGE description-only embedding payload without model execution."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CORPUS = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
OUTPUT_DIR = NC_ROOT / "manifests/source_native_description_local_bge_embedding_preflight_2026-09-04"

MODEL_ID = "BAAI/bge-small-en-v1.5"
MODEL_REVISION_REQUESTED = "main"
DIMENSION_EXPECTED = 384
TOP_NEIGHBOURS = 12
BATCH_SIZE = 64


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def main() -> int:
    required = [PROTOCOL, CORPUS]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Output directory already exists: {OUTPUT_DIR}")
    source_rows = [row for row in read_jsonl(CORPUS) if row.get("index_eligibility") is True]
    if len(source_rows) != 23_431:
        raise SystemExit("Expected 23,431 literal-replay native descriptions")
    source_rows.sort(key=lambda row: str(row["canonical_source_sha256"]))
    text_rows: dict[str, dict[str, Any]] = {}
    bindings: list[dict[str, Any]] = []
    for row in source_rows:
        source_hash = str(row["canonical_source_sha256"])
        text = str(row["native_description"])
        text_hash = str(row["native_description_sha256"])
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != text_hash:
            raise SystemExit(f"Native description hash mismatch: {source_hash}")
        text_rows.setdefault(text_hash, {"native_description_sha256": text_hash, "native_description": text})
        bindings.append({
            "canonical_source_sha256": source_hash,
            "native_description_sha256": text_hash,
            "source_byte_replay": row["source_byte_replay"],
            "native_description_replay_status": row["native_description_replay_status"],
        })
    texts = [text_rows[key] for key in sorted(text_rows)]
    OUTPUT_DIR.mkdir(parents=True)
    text_path = OUTPUT_DIR / "unique_native_description_texts.jsonl"
    binding_path = OUTPUT_DIR / "source_to_text_bindings.jsonl"
    write_jsonl(text_path, texts)
    write_jsonl(binding_path, bindings)
    manifest = {
        "status": "PASS_SOURCE_NATIVE_LOCAL_BGE_EMBEDDING_PREFLIGHT_NO_MODEL_LOAD_OR_NETWORK_CALL",
        "bound_inputs": {relative(PROTOCOL): sha256_file(PROTOCOL), relative(CORPUS): sha256_file(CORPUS)},
        "local_model_contract": {
            "model_id": MODEL_ID,
            "model_revision_requested": MODEL_REVISION_REQUESTED,
            "implementation": "sentence-transformers",
            "expected_embedding_dimension": DIMENSION_EXPECTED,
            "device_policy": "CPU_ONLY_FOR_REPRODUCIBLE_LOCAL_EXECUTION",
            "normalise_embeddings": True,
            "batch_size": BATCH_SIZE,
            "top_neighbours": TOP_NEIGHBOURS,
            "retry_policy": "NO_AUTOMATIC_RETRY",
            "trust_remote_code": False,
        },
        "payload_scope": "Exact public original native descriptions only. No full skill body, prompt, label, review, provenance, rank or source origin is model input.",
        "counts": {"source_bindings": len(bindings), "unique_native_descriptions": len(texts), "native_description_utf8_bytes": sum(len(row["native_description"].encode("utf-8")) for row in texts)},
        "outputs": {"unique_native_description_texts.jsonl": sha256_file(text_path), "source_to_text_bindings.jsonl": sha256_file(binding_path)},
        "claim_boundary": "Preflight only. It makes no model load, network call, dense ranking, family hypothesis, review, admission, selector or metric result.",
    }
    write_json(OUTPUT_DIR / "manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
