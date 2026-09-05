#!/usr/bin/env python3
"""Seal a local-only Qwen payload preflight for the frozen RQ1b v2 BM25 twin."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq1b_field_type_confirmatory_v2_common import canonical_entries
from run_rq1b_field_type_confirmatory_v2_bm25 import CONDITIONS, load_condition, load_strict_families, render_card, tokens


BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
MODEL = "text-embedding-v4"
DIMENSIONS = 1024
MAX_BATCH_TEXTS = 10
PREFLIGHT_VERSION = "rq1b-field-type-v2-qwen-preflight-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_id(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def register_text(inventory: dict[str, dict[str, Any]], text: str, role: dict[str, str]) -> str:
    identifier = text_id(text)
    row = inventory.get(identifier)
    if row is None:
        inventory[identifier] = {
            "text_id": identifier,
            "text": text,
            "utf8_bytes": len(text.encode()),
            "local_lexical_token_proxy": len(tokens(text)),
            "roles": [role],
        }
    else:
        if row["text"] != text:
            raise ValueError("SHA-256 collision in Qwen payload")
        row["roles"].append(role)
    return identifier


def cache_path(cache_root: Path, identifier: str) -> Path:
    return cache_root / f"{identifier}.json"


def build(root: Path, output_dir: Path, cache_root: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite preflight: {output_dir}")
    families, _ = load_strict_families(root)
    entries = canonical_entries(root)
    inventory: dict[str, dict[str, Any]] = {}
    documents, queries = [], []
    strict_compositions = sorted({family["composition_id"] for family in families})
    for composition_id in strict_compositions:
        entry = entries[composition_id]
        for condition in CONDITIONS:
            for card in load_condition(root, composition_id, condition, entry):
                identifier = register_text(
                    inventory,
                    render_card(card["slots"]),
                    {"kind": "document", "composition_id": composition_id, "condition": condition, "candidate_label": card["label"]},
                )
                documents.append({"composition_id": composition_id, "condition": condition, "candidate_label": card["label"], "text_id": identifier})
    for family in families:
        for variant, prompt in family["prompts"].items():
            identifier = register_text(
                inventory,
                prompt,
                {"kind": "query", "routing_family_id": family["routing_family_id"], "prompt_variant": variant},
            )
            queries.append({"routing_family_id": family["routing_family_id"], "composition_id": family["composition_id"], "prompt_variant": variant, "text_id": identifier})
    text_rows = [inventory[key] for key in sorted(inventory)]
    document_ids, query_ids = {row["text_id"] for row in documents}, {row["text_id"] for row in queries}
    cached_ids = {row["text_id"] for row in text_rows if cache_path(cache_root, row["text_id"]).is_file()}
    missing_ids = {row["text_id"] for row in text_rows} - cached_ids
    missing_document_ids, missing_query_ids = missing_ids & document_ids, missing_ids & query_ids
    def totals(ids: set[str]) -> dict[str, int]:
        rows = [inventory[identifier] for identifier in ids]
        return {"texts": len(rows), "utf8_bytes": sum(row["utf8_bytes"] for row in rows), "local_lexical_token_proxy": sum(row["local_lexical_token_proxy"] for row in rows)}
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_QWEN_PAYLOAD_LOCAL_PREFLIGHT_NOT_EXECUTED",
        "preflight_version": PREFLIGHT_VERSION,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "network_calls": 0,
        "texts_transmitted": 0,
        "root": str(root),
        "cache_root": str(cache_root),
        "text_inventory": text_rows,
        "documents": documents,
        "queries": queries,
        "counts": {
            "strict_routing_families": len(families),
            "strict_compositions": len(strict_compositions),
            "prompt_instances": len(queries),
            "document_instances": len(documents),
            "unique_document_texts": len(document_ids),
            "unique_query_texts": len(query_ids),
            "unique_texts": len(text_rows),
            "cache_hits": totals(cached_ids),
            "cache_misses": totals(missing_ids),
            "new_document_texts": totals(missing_document_ids),
            "new_query_texts": totals(missing_query_ids),
            "maximum_request_attempts_no_retry": (
                math.ceil(len(missing_document_ids) / MAX_BATCH_TEXTS)
                + math.ceil(len(missing_query_ids) / MAX_BATCH_TEXTS)
            ),
            "maximum_successful_calls_no_retry": (
                math.ceil(len(missing_document_ids) / MAX_BATCH_TEXTS)
                + math.ceil(len(missing_query_ids) / MAX_BATCH_TEXTS)
            ),
            "expected_score_rows": len(families) * 2 * len(CONDITIONS),
        },
        "authorisation_boundary": {
            "external_text_transfer_authorized": False,
            "paid_api_authorized": False,
            "automatic_retries": 0,
            "notes": "Local lexical token proxy is an audit estimate, not provider billing usage. Exact provider usage is recorded only if an authorised call succeeds.",
        },
    }
    staging = output_dir.parent / f".{output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale preflight staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        (staging / "payload.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        manifest = {
            "status": "RQ1B_FIELD_TYPE_V2_QWEN_PREFLIGHT_MANIFEST_NOT_EXECUTED",
            "payload_sha256": sha256_file(staging / "payload.json"),
            "payload_counts": payload["counts"],
            "network_calls": 0,
            "texts_transmitted": 0,
        }
        (staging / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(output_dir)
    except Exception:
        import shutil
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.root, args.output_dir, args.cache_root), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
