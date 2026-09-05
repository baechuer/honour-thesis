#!/usr/bin/env python3
"""Build a local-only, cache-aware Qwen preflight for RQ1b v2.1 joint masks."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any

from prepare_rq1b_field_type_confirmatory_v2_qwen_preflight import (
    BASE_URL,
    DIMENSIONS,
    MAX_BATCH_TEXTS,
    MODEL,
    register_text,
)
from prepare_rq1b_joint_field_mask_v21 import CONDITIONS, GROUPS, load_joint_condition, load_joint_scope
from run_rq1b_field_type_confirmatory_v2_bm25 import render_card, tokens
from run_rq1b_field_type_confirmatory_v2_qwen import cache_load


PREFLIGHT_VERSION = "rq1b-joint-field-mask-v21-qwen-preflight-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cached(cache_root: Path, row: dict[str, Any]) -> bool:
    return cache_load(cache_root, row) is not None


def totals(inventory: dict[str, dict[str, Any]], identifiers: set[str]) -> dict[str, int]:
    rows = [inventory[identifier] for identifier in identifiers]
    return {
        "texts": len(rows),
        "utf8_bytes": sum(row["utf8_bytes"] for row in rows),
        "local_lexical_token_proxy": sum(row["local_lexical_token_proxy"] for row in rows),
    }


def build(joint_root: Path, output_dir: Path, cache_root: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite Qwen preflight: {output_dir}")
    freeze, source_root, families, eligible = load_joint_scope(joint_root)
    inventory: dict[str, dict[str, Any]] = {}
    documents, queries = [], []
    strict_compositions = sorted({family["composition_id"] for family in families})
    for composition_id in strict_compositions:
        for condition in CONDITIONS:
            for card in load_joint_condition(joint_root, freeze, composition_id, condition):
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
    document_ids = {row["text_id"] for row in documents}
    query_ids = {row["text_id"] for row in queries}
    cached_ids = {row["text_id"] for row in text_rows if cached(cache_root, row)}
    missing_ids = {row["text_id"] for row in text_rows} - cached_ids
    missing_document_ids, missing_query_ids = missing_ids & document_ids, missing_ids & query_ids
    payload = {
        "status": "RQ1B_JOINT_FIELD_MASK_V21_QWEN_PAYLOAD_LOCAL_PREFLIGHT_NOT_EXECUTED",
        "preflight_version": PREFLIGHT_VERSION,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "network_calls": 0,
        "texts_transmitted": 0,
        "joint_root": str(joint_root),
        "source_v2_root": str(source_root),
        "joint_freeze_sha256": sha256_file(joint_root / "joint_mask_freeze.json"),
        "cache_root": str(cache_root),
        "conditions": list(CONDITIONS),
        "groups": {condition: list(fields) for condition, fields in GROUPS.items()},
        "text_inventory": text_rows,
        "documents": documents,
        "queries": queries,
        "counts": {
            "strict_routing_families": len(families),
            "strict_compositions": len(strict_compositions),
            "group_eligible_families": {condition: len(ids) for condition, ids in eligible.items()},
            "prompt_instances": len(queries),
            "document_instances": len(documents),
            "unique_document_texts": len(document_ids),
            "unique_query_texts": len(query_ids),
            "unique_texts": len(text_rows),
            "cache_hits": totals(inventory, cached_ids),
            "cache_misses": totals(inventory, missing_ids),
            "new_document_texts": totals(inventory, missing_document_ids),
            "new_query_texts": totals(inventory, missing_query_ids),
            "maximum_request_attempts_no_retry": math.ceil(len(missing_document_ids) / MAX_BATCH_TEXTS) + math.ceil(len(missing_query_ids) / MAX_BATCH_TEXTS),
            "maximum_successful_calls_no_retry": math.ceil(len(missing_document_ids) / MAX_BATCH_TEXTS) + math.ceil(len(missing_query_ids) / MAX_BATCH_TEXTS),
            "expected_score_rows": len(families) * 2 * len(CONDITIONS),
        },
        "authorisation_boundary": {
            "external_text_transfer_authorized": False,
            "paid_api_authorized": False,
            "automatic_retries": 0,
            "notes": "Cache-hit embeddings are validated locally and are not sent. Local lexical token proxy is an audit estimate, not provider billing usage.",
        },
    }
    staging = output_dir.parent / f".{output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale Qwen preflight staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        (staging / "payload.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        manifest = {
            "status": "RQ1B_JOINT_FIELD_MASK_V21_QWEN_PREFLIGHT_MANIFEST_NOT_EXECUTED",
            "payload_sha256": sha256_file(staging / "payload.json"),
            "payload_counts": payload["counts"],
            "network_calls": 0,
            "texts_transmitted": 0,
        }
        (staging / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--joint-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.joint_root, args.output_dir, args.cache_root), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
