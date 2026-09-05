#!/usr/bin/env python3
"""Score only RQ1b's imported V3 triads and reuse verified V2 results.

The local BM25 mode produces 192 new V3 rows and a stratified 1,584-row
harmonised view. The Qwen preflight is local only; the Qwen execution path is
fail-stop and requires a fresh, exact-payload authorisation file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import time
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from build_rq1b_v2_v3_complete_triad_extension import CONDITIONS, FIELDS, build as verify_extension
from prepare_rq1b_field_type_confirmatory_v2_qwen_preflight import (
    BASE_URL,
    DIMENSIONS,
    MAX_BATCH_TEXTS,
    MODEL,
)
from run_rq1b_field_type_confirmatory_v2_bm25 import BM25, metric_for_ranking, render_card, tokens
from run_rq1b_field_type_confirmatory_v2_qwen import (
    cache_load,
    cache_store,
    chunks,
    cosine,
    load_dotenv,
    post_once,
)


REPO = Path(__file__).resolve().parents[2]
EXTENSION = REPO / "skill_benchmark/rq1b_final_public_corpus_v1/v2_v3_complete_triad_extension_2026-08-30"
V2_ROOT = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28"
V2_BM25 = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_bm25_2026-08-29"
V2_QWEN = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_qwen_2026-08-29"
DEFAULT_OUTPUT = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30"
DEFAULT_CACHE = REPO / "skill_benchmark/cache/rq1b_v2_v3_complete_triad_extension/qwen/text-embedding-v4/1024"

RUNNER_VERSION = "rq1b-v2-v3-complete-triad-extension-runner-v1"
CONDITION_ORDER = tuple(CONDITIONS)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"JSONL object rows required: {path}")
    return rows


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def atomic_directory(output: Path, files: dict[str, str]) -> None:
    if output.exists():
        raise ValueError(f"refusing to overwrite output: {output}")
    staging = output.parent / f".{output.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        for name, text in files.items():
            path = staging / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        staging.replace(output)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def validate_v2_reuse(source: Path, expected_status: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = read_json(source / "manifest.json")
    if manifest.get("status") != expected_status:
        raise ValueError(f"unexpected V2 result state: {source}")
    rows_path, summary_path = source / "rows.jsonl", source / "summary.json"
    artifacts = manifest.get("artifacts", {})
    if artifacts.get("rows.jsonl") != sha256_file(rows_path) or artifacts.get("summary.json") != sha256_file(summary_path):
        raise ValueError(f"V2 result hash mismatch: {source}")
    rows = read_jsonl(rows_path)
    expected = 87 * 2 * len(CONDITION_ORDER)
    keys = {(row.get("routing_family_id"), row.get("prompt_variant"), row.get("condition")) for row in rows}
    if len(rows) != expected or len(keys) != expected:
        raise ValueError(f"V2 result coverage drift: {source}")
    if {row.get("condition") for row in rows} != set(CONDITION_ORDER):
        raise ValueError(f"V2 result condition coverage drift: {source}")
    return rows, {
        "result_root": relative(source),
        "manifest_sha256": sha256_file(source / "manifest.json"),
        "rows_sha256": sha256_file(rows_path),
        "summary_sha256": sha256_file(summary_path),
        "row_count": len(rows),
        "routing_family_count": len({row["routing_family_id"] for row in rows}),
        "prompt_count": len({(row["routing_family_id"], row["prompt_variant"]) for row in rows}),
    }


def load_extension() -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], dict[str, Any]]:
    verified = verify_extension(EXTENSION, True)
    if verified["prospective_harmonised_matrix"]["strict_preserved_routing_families"] != 99:
        raise ValueError("combined extension contract drift")
    combined = read_json(EXTENSION / "combined_matrix_manifest.json")
    audit = read_json(EXTENSION / "compatibility_audit.json")
    if combined.get("status") != "RQ1B_V2_PLUS_V3_HARMONISED_FUTURE_SELECTOR_MANIFEST_NOT_A_RESULT":
        raise ValueError("extension future-matrix manifest state drift")
    if audit.get("status") != "RQ1B_V2_PLUS_V3_COMPLETE_TRIAD_COMPATIBILITY_AUDIT_PASS_NOT_A_SELECTOR_RESULT":
        raise ValueError("extension compatibility audit state drift")
    compositions = read_json(EXTENSION / "extension_composition_manifest_private.json").get("rows")
    families = read_json(EXTENSION / "extension_routing_family_manifest_private.json").get("rows")
    if not isinstance(compositions, list) or not isinstance(families, list) or len(compositions) != 4 or len(families) != 12:
        raise ValueError("extension composition/family count drift")
    by_composition = {row["composition_id"]: row for row in compositions}
    if len(by_composition) != 4 or {row["composition_id"] for row in families} != set(by_composition):
        raise ValueError("extension composition/family binding drift")
    cards_by_key: dict[str, list[dict[str, Any]]] = {}
    for composition_id, entry in sorted(by_composition.items()):
        labels = {candidate["label"] for candidate in entry["private_candidates"]}
        if entry.get("candidate_count") != 3 or len(labels) != 3:
            raise ValueError(f"extension candidate cardinality drift: {composition_id}")
        for condition in CONDITION_ORDER:
            payload = read_json(EXTENSION / "conditions" / composition_id / f"{condition}.json")
            if (
                payload.get("status") != "RQ1B_V2_PLUS_V3_IMPORTED_CONDITION_NOT_A_RESULT"
                or payload.get("composition_id") != composition_id
                or payload.get("condition") != condition
                or tuple(payload.get("field_order", [])) != tuple(FIELDS)
            ):
                raise ValueError(f"extension condition binding drift: {composition_id}/{condition}")
            cards = payload.get("cards")
            if not isinstance(cards, list) or {card.get("label") for card in cards if isinstance(card, dict)} != labels:
                raise ValueError(f"extension candidate membership drift: {composition_id}/{condition}")
            for card in cards:
                slots = card.get("slots")
                if not isinstance(slots, dict) or set(slots) != set(FIELDS) or any(not isinstance(slots[field], str) for field in FIELDS):
                    raise ValueError(f"extension card schema drift: {composition_id}/{condition}/{card.get('label')}")
            cards_by_key[f"{composition_id}/{condition}"] = cards
    normalised = []
    for family in families:
        prompts = {item["prompt_variant"]: item for item in family.get("prompt_lineage", [])}
        if set(prompts) != {"direct", "paraphrase"} or any(sha256_text(item["prompt"]) != item["prompt_sha256"] for item in prompts.values()):
            raise ValueError(f"extension prompt binding drift: {family.get('routing_family_id')}")
        if family.get("strict_gold_card") not in {candidate["label"] for candidate in by_composition[family["composition_id"]]["private_candidates"]}:
            raise ValueError(f"extension gold card drift: {family.get('routing_family_id')}")
        normalised.append({
            "routing_family_id": family["routing_family_id"],
            "composition_id": family["composition_id"],
            "source_composition_id": family["source_composition_id"],
            "gold_label": family["strict_gold_card"],
            "prompts": prompts,
        })
    normalised.sort(key=lambda row: row["routing_family_id"])
    return cards_by_key, normalised, {
        "extension_root": relative(EXTENSION),
        "combined_matrix_manifest_sha256": sha256_file(EXTENSION / "combined_matrix_manifest.json"),
        "compatibility_audit_sha256": sha256_file(EXTENSION / "compatibility_audit.json"),
        "extension_composition_manifest_sha256": sha256_file(EXTENSION / "extension_composition_manifest_private.json"),
        "extension_routing_family_manifest_sha256": sha256_file(EXTENSION / "extension_routing_family_manifest_private.json"),
    }


def rows_for_bm25(cards_by_key: dict[str, list[dict[str, Any]]], families: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family in families:
        composition_id = family["composition_id"]
        for condition in CONDITION_ORDER:
            cards = cards_by_key[f"{composition_id}/{condition}"]
            ranking_index = BM25([card["label"] for card in cards], [render_card(card["slots"]) for card in cards])
            for variant in ("direct", "paraphrase"):
                started = time.perf_counter()
                ranking = ranking_index.rank(family["prompts"][variant]["prompt"])
                rows.append({
                    "status": "RQ1B_V2_V3_EXTENSION_BM25_ROW_LOCAL_RESULT",
                    "retriever": "bm25",
                    "integration_stratum": "imported_v3_new",
                    "routing_family_id": family["routing_family_id"],
                    "composition_id": composition_id,
                    "source_composition_id": family["source_composition_id"],
                    "prompt_variant": variant,
                    "condition": condition,
                    "gold_label": family["gold_label"],
                    "candidate_count": len(cards),
                    "query_seconds": time.perf_counter() - started,
                    **metric_for_ranking(ranking, family["gold_label"]),
                })
    validate_extension_rows(rows)
    return rows


def validate_extension_rows(rows: list[dict[str, Any]]) -> None:
    expected = 12 * 2 * len(CONDITION_ORDER)
    keys = {(row["routing_family_id"], row["prompt_variant"], row["condition"]) for row in rows}
    if len(rows) != expected or len(keys) != expected:
        raise ValueError("extension score-row coverage drift")
    if {row["candidate_count"] for row in rows} != {3}:
        raise ValueError("extension candidate cardinality drift in rows")


def with_stratum(rows: list[dict[str, Any]], stratum: str, source: str) -> list[dict[str, Any]]:
    return [{**row, "integration_stratum": stratum, "integration_source": source} for row in rows]


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        raise ValueError("empty metric input")
    return {
        "row_count": len(rows),
        "routing_family_count": len({row["routing_family_id"] for row in rows}),
        "prompt_count": len({(row["routing_family_id"], row["prompt_variant"]) for row in rows}),
        "top1": mean(row["hit_at_1"] for row in rows),
        "mrr": mean(row["mrr"] for row in rows),
        "mean_gold_rank": mean(row["gold_rank"] for row in rows),
        "mean_gold_minus_best_wrong_margin": mean(row["gold_minus_best_wrong_margin"] for row in rows),
    }


def condition_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["condition"]].append(row)
    return {condition: metrics(grouped[condition]) for condition in CONDITION_ORDER}


def all_family_field_deltas(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_key = {(row["routing_family_id"], row["prompt_variant"], row["condition"]): row for row in rows}
    results = {}
    for condition, field in zip(CONDITION_ORDER[1:], FIELDS, strict=True):
        paired = []
        for family_id, variant in sorted({(row["routing_family_id"], row["prompt_variant"]) for row in rows}):
            full = by_key.get((family_id, variant, "FULL"))
            masked = by_key.get((family_id, variant, condition))
            if full is None or masked is None:
                raise ValueError(f"full/mask pairing missing: {family_id}/{variant}/{condition}")
            paired.append((full, masked))
        results[field] = {
            "condition": condition,
            "prompt_pair_count": len(paired),
            "full_minus_mask_top1": mean(full["hit_at_1"] - masked["hit_at_1"] for full, masked in paired),
            "full_minus_mask_mrr": mean(full["mrr"] - masked["mrr"] for full, masked in paired),
            "full_minus_mask_margin": mean(
                full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"]
                for full, masked in paired
            ),
            "full_correct_to_masked_wrong_rate": mean(
                full["hit_at_1"] == 1 and masked["hit_at_1"] == 0 for full, masked in paired
            ),
        }
    return results


def write_bm25(output_root: Path) -> dict[str, Any]:
    cards, families, extension_provenance = load_extension()
    v2_rows, v2_reuse = validate_v2_reuse(V2_BM25, "RQ1B_FIELD_TYPE_V2_BM25_LOCAL_RUN_MANIFEST")
    v3_rows = rows_for_bm25(cards, families)
    combined = with_stratum(v2_rows, "native_v2_reused", relative(V2_BM25)) + v3_rows
    if len(combined) != 1584:
        raise ValueError("combined BM25 row count drift")
    summary = {
        "status": "RQ1B_V2_V3_EXTENSION_BM25_STRATIFIED_RESULT",
        "claim_boundary": [
            "V2 rows are verified reuse, not recomputation.",
            "Imported V3 all-family field deltas are supplemental complete-triad perturbation estimates, not V2 field-eligibility estimates.",
            "The harmonised all-family view is reported separately and does not replace native V2 primary field-eligible analysis.",
        ],
        "native_v2_reused": {
            "reuse": v2_reuse,
            "condition_metrics": condition_metrics(with_stratum(v2_rows, "native_v2_reused", relative(V2_BM25))),
        },
        "imported_v3_new": {
            "condition_metrics": condition_metrics(v3_rows),
            "all_complete_triad_field_deltas": all_family_field_deltas(v3_rows),
        },
        "harmonised_all_families_supplemental": {
            "condition_metrics": condition_metrics(combined),
            "all_family_field_deltas": all_family_field_deltas(combined),
        },
    }
    manifest = {
        "status": "RQ1B_V2_V3_EXTENSION_BM25_LOCAL_RUN_MANIFEST",
        "runner_version": RUNNER_VERSION,
        "network_calls": 0,
        "texts_transmitted": 0,
        "thesis_results_written": False,
        "extension_provenance": extension_provenance,
        "v2_reuse": v2_reuse,
        "counts": {"new_v3_rows": len(v3_rows), "reused_v2_rows": len(v2_rows), "harmonised_rows": len(combined)},
    }
    files = {
        "v3_rows.jsonl": "".join(json.dumps(row, sort_keys=True) + "\n" for row in v3_rows),
        "combined_rows.jsonl": "".join(json.dumps(row, sort_keys=True) + "\n" for row in combined),
        "summary.json": json.dumps(summary, indent=2, sort_keys=True) + "\n",
    }
    for name, text in files.items():
        manifest.setdefault("artifacts", {})[name] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    files["manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    atomic_directory(output_root / "bm25", files)
    return manifest


def register_text(inventory: dict[str, dict[str, Any]], text: str, role: dict[str, str]) -> str:
    identifier = sha256_text(text)
    row = inventory.get(identifier)
    if row is None:
        row = {
            "text_id": identifier,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "local_lexical_token_proxy": len(tokens(text)),
            "roles": [],
        }
        inventory[identifier] = row
    elif row["text"] != text:
        raise ValueError("text SHA-256 collision")
    row["roles"].append(role)
    return identifier


def totals(inventory: dict[str, dict[str, Any]], identifiers: set[str]) -> dict[str, int]:
    rows = [inventory[identifier] for identifier in identifiers]
    return {
        "texts": len(rows),
        "utf8_bytes": sum(row["utf8_bytes"] for row in rows),
        "local_lexical_token_proxy": sum(row["local_lexical_token_proxy"] for row in rows),
    }


def build_qwen_payload(cache_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    cards, families, extension_provenance = load_extension()
    inventory: dict[str, dict[str, Any]] = {}
    documents, queries = [], []
    for key, cards_for_condition in sorted(cards.items()):
        composition_id, condition = key.split("/", 1)
        for card in cards_for_condition:
            identifier = register_text(inventory, render_card(card["slots"]), {
                "kind": "document", "composition_id": composition_id, "condition": condition, "candidate_label": card["label"],
            })
            documents.append({"composition_id": composition_id, "condition": condition, "candidate_label": card["label"], "text_id": identifier})
    for family in families:
        for variant in ("direct", "paraphrase"):
            identifier = register_text(inventory, family["prompts"][variant]["prompt"], {
                "kind": "query", "routing_family_id": family["routing_family_id"], "prompt_variant": variant,
            })
            queries.append({"routing_family_id": family["routing_family_id"], "composition_id": family["composition_id"], "prompt_variant": variant, "text_id": identifier})
    text_rows = [inventory[key] for key in sorted(inventory)]
    document_ids = {row["text_id"] for row in documents}
    query_ids = {row["text_id"] for row in queries}
    cache_root.mkdir(parents=True, exist_ok=True)
    cached = {row["text_id"] for row in text_rows if cache_load(cache_root, row) is not None}
    missing = set(inventory) - cached
    missing_documents, missing_queries = missing & document_ids, missing & query_ids
    payload = {
        "status": "RQ1B_V2_V3_EXTENSION_QWEN_LOCAL_PREFLIGHT_NOT_EXECUTED",
        "runner_version": RUNNER_VERSION,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "network_calls": 0,
        "texts_transmitted": 0,
        "cache_root": str(cache_root),
        "extension_provenance": extension_provenance,
        "text_inventory": text_rows,
        "documents": documents,
        "queries": queries,
        "counts": {
            "strict_routing_families": len(families),
            "strict_prompts": len(queries),
            "document_instances": len(documents),
            "unique_document_texts": len(document_ids),
            "unique_query_texts": len(query_ids),
            "unique_texts": len(text_rows),
            "cache_hits": totals(inventory, cached),
            "new_document_texts": totals(inventory, missing_documents),
            "new_query_texts": totals(inventory, missing_queries),
            "new_texts": totals(inventory, missing),
            "maximum_request_attempts_no_retry": math.ceil(len(missing_documents) / MAX_BATCH_TEXTS) + math.ceil(len(missing_queries) / MAX_BATCH_TEXTS),
            "maximum_successful_calls_no_retry": math.ceil(len(missing_documents) / MAX_BATCH_TEXTS) + math.ceil(len(missing_queries) / MAX_BATCH_TEXTS),
            "expected_new_v3_rows": 12 * 2 * len(CONDITION_ORDER),
            "expected_harmonised_rows_after_v2_reuse": 1584,
        },
        "authorisation_boundary": {
            "external_text_transfer_authorized": False,
            "paid_api_authorized": False,
            "automatic_retries": 0,
            "notes": "Queries and V3 rendered candidate cards remain local until an exact-payload authorisation is recorded.",
        },
    }
    return payload, {"cards": cards, "families": families}


def write_qwen_preflight(output_root: Path, cache_root: Path) -> dict[str, Any]:
    payload, _ = build_qwen_payload(cache_root)
    payload_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    manifest = {
        "status": "RQ1B_V2_V3_EXTENSION_QWEN_PREFLIGHT_LOCAL_NOT_EXECUTED",
        "payload_sha256": hashlib.sha256(payload_text.encode("utf-8")).hexdigest(),
        "payload_counts": payload["counts"],
        "network_calls": 0,
        "texts_transmitted": 0,
    }
    atomic_directory(output_root / "qwen_preflight", {
        "payload.json": payload_text,
        "manifest.json": json.dumps(manifest, indent=2, sort_keys=True) + "\n",
    })
    return manifest


def validate_qwen_authorisation(path: Path, payload_path: Path, output: Path) -> dict[str, Any]:
    authorisation = read_json(path)
    required = {
        "status": "RQ1B_V2_V3_EXTENSION_QWEN_ONE_RUN_AUTHORISED",
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "payload_sha256": sha256_file(payload_path),
        "output_dir": str(output),
        "automatic_retries": 0,
    }
    for key, value in required.items():
        if authorisation.get(key) != value:
            raise ValueError(f"Qwen authorisation mismatch: {key}")
    for key in ("maximum_new_texts", "maximum_request_attempts", "maximum_successful_calls", "maximum_local_lexical_token_proxy", "maximum_utf8_bytes"):
        if not isinstance(authorisation.get(key), int) or authorisation[key] < 0:
            raise ValueError(f"Qwen authorisation ceiling missing: {key}")
    return authorisation


def embed_missing(payload: dict[str, Any], cache_root: Path, authorisation: dict[str, Any], output: Path, timeout_seconds: int) -> tuple[dict[str, list[float]], dict[str, Any]]:
    inventory = {row["text_id"]: row for row in payload["text_inventory"]}
    vectors = {identifier: cache_load(cache_root, row) for identifier, row in inventory.items()}
    missing = [row for identifier, row in inventory.items() if vectors[identifier] is None]
    documents = [row for row in missing if any(role["kind"] == "document" for role in row["roles"])]
    queries = [row for row in missing if any(role["kind"] == "query" for role in row["roles"])]
    actual = {
        "maximum_new_texts": len(missing),
        "maximum_request_attempts": len(chunks(documents)) + len(chunks(queries)),
        "maximum_successful_calls": len(chunks(documents)) + len(chunks(queries)),
        "maximum_local_lexical_token_proxy": sum(row["local_lexical_token_proxy"] for row in missing),
        "maximum_utf8_bytes": sum(row["utf8_bytes"] for row in missing),
    }
    for key, value in actual.items():
        if value > authorisation[key]:
            raise ValueError(f"Qwen execution exceeds authorised ceiling: {key}")
    load_dotenv(Path(authorisation.get("dotenv", ".env")))
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY unavailable after loading configured dotenv")
    requests = output / "requests"
    requests.mkdir(parents=True, exist_ok=True)
    attempts = successful = 0
    provider_usage: dict[str, int] = {}
    groups_by_role = (("document", chunks(documents)), ("query", chunks(queries)))
    for role, groups in groups_by_role:
        for group in groups:
            if attempts >= authorisation["maximum_request_attempts"] or successful >= authorisation["maximum_successful_calls"]:
                raise ValueError("Qwen call ceiling reached before request")
            attempts += 1
            attempt = {"attempt": attempts, "role": role, "text_ids": [row["text_id"] for row in group], "text_count": len(group), "automatic_retry": False}
            (requests / f"request_{attempts:04d}_attempt.json").write_text(json.dumps(attempt, indent=2, sort_keys=True) + "\n")
            begun = time.perf_counter()
            try:
                response = post_once(api_key, [row["text"] for row in group], timeout_seconds)
            except Exception as error:
                failure = {**attempt, "state": "failed_stop_no_retry", "error_type": type(error).__name__, "error": str(error)}
                (requests / f"request_{attempts:04d}_failure.json").write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n")
                raise RuntimeError(f"Qwen request {attempts} failed; no retry was attempted") from error
            data, usage = response.get("data"), response.get("usage") or {}
            if not isinstance(data, list) or len(data) != len(group):
                raise ValueError("Qwen response count mismatch")
            ordered = sorted(data, key=lambda row: int(row["index"]))
            if [int(row["index"]) for row in ordered] != list(range(len(group))):
                raise ValueError("Qwen response index mismatch")
            receipt = {**attempt, "state": "success", "request_seconds": time.perf_counter() - begun, "provider_usage": usage}
            (requests / f"request_{attempts:04d}_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
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
            print(f"QWEN_PROGRESS request={attempts}/{actual['maximum_request_attempts']} role={role} texts={len(group)}", flush=True)
    return {identifier: vector for identifier, vector in vectors.items() if vector is not None}, {
        "cache_hits": len(inventory) - len(missing),
        "cache_misses": len(missing),
        "request_attempts": attempts,
        "successful_calls": successful,
        "provider_usage": provider_usage,
    }


def write_qwen_result(output_root: Path, cache_root: Path, authorisation_path: Path, timeout_seconds: int) -> dict[str, Any]:
    preflight = output_root / "qwen_preflight"
    payload_path = preflight / "payload.json"
    payload = read_json(payload_path)
    if payload.get("status") != "RQ1B_V2_V3_EXTENSION_QWEN_LOCAL_PREFLIGHT_NOT_EXECUTED":
        raise ValueError("Qwen preflight state drift")
    output = output_root / "qwen"
    if output.exists():
        raise ValueError(f"refusing to overwrite Qwen output: {output}")
    authorisation = validate_qwen_authorisation(authorisation_path, payload_path, output)
    output.mkdir(parents=True)
    try:
        vectors, execution = embed_missing(payload, cache_root, authorisation, output, timeout_seconds)
        _, families, _ = load_extension()
        documents = {(row["composition_id"], row["condition"], row["candidate_label"]): row["text_id"] for row in payload["documents"]}
        queries = {(row["routing_family_id"], row["prompt_variant"]): row["text_id"] for row in payload["queries"]}
        rows = []
        for family in families:
            for variant in ("direct", "paraphrase"):
                query_vector = vectors[queries[(family["routing_family_id"], variant)]]
                for condition in CONDITION_ORDER:
                    candidates = [row for row in payload["documents"] if row["composition_id"] == family["composition_id"] and row["condition"] == condition]
                    ranking = sorted(
                        ((row["candidate_label"], cosine(query_vector, vectors[row["text_id"]])) for row in candidates),
                        key=lambda item: (-item[1], item[0]),
                    )
                    rows.append({
                        "status": "RQ1B_V2_V3_EXTENSION_QWEN_ROW_EXTERNAL_RESULT",
                        "retriever": "qwen-text-embedding-v4",
                        "integration_stratum": "imported_v3_new",
                        "routing_family_id": family["routing_family_id"],
                        "composition_id": family["composition_id"],
                        "source_composition_id": family["source_composition_id"],
                        "prompt_variant": variant,
                        "condition": condition,
                        "gold_label": family["gold_label"],
                        "candidate_count": len(candidates),
                        "query_seconds": None,
                        **metric_for_ranking(ranking, family["gold_label"]),
                    })
        validate_extension_rows(rows)
        v2_rows, v2_reuse = validate_v2_reuse(V2_QWEN, "RQ1B_FIELD_TYPE_V2_QWEN_RUN_EXTERNAL_RESULT")
        combined = with_stratum(v2_rows, "native_v2_reused", relative(V2_QWEN)) + rows
        if len(combined) != 1584:
            raise ValueError("combined Qwen row count drift")
        summary = {
            "status": "RQ1B_V2_V3_EXTENSION_QWEN_STRATIFIED_RESULT",
            "claim_boundary": [
                "V2 rows are verified reuse, not recomputation.",
                "Imported V3 all-family field deltas are supplemental complete-triad perturbation estimates, not V2 field-eligibility estimates.",
                "The harmonised all-family view is reported separately and does not replace native V2 primary field-eligible analysis.",
            ],
            "native_v2_reused": {"reuse": v2_reuse, "condition_metrics": condition_metrics(with_stratum(v2_rows, "native_v2_reused", relative(V2_QWEN)))},
            "imported_v3_new": {"condition_metrics": condition_metrics(rows), "all_complete_triad_field_deltas": all_family_field_deltas(rows)},
            "harmonised_all_families_supplemental": {"condition_metrics": condition_metrics(combined), "all_family_field_deltas": all_family_field_deltas(combined)},
        }
        (output / "v3_rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
        (output / "combined_rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in combined), encoding="utf-8")
        (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        manifest = {
            "status": "RQ1B_V2_V3_EXTENSION_QWEN_EXTERNAL_RUN_MANIFEST",
            "runner_version": RUNNER_VERSION,
            "payload_sha256": sha256_file(payload_path),
            "authorisation_sha256": sha256_file(authorisation_path),
            "execution": execution,
            "v2_reuse": v2_reuse,
            "counts": {"new_v3_rows": len(rows), "reused_v2_rows": len(v2_rows), "harmonised_rows": len(combined)},
            "artifacts": {name: sha256_file(output / name) for name in ("v3_rows.jsonl", "combined_rows.jsonl", "summary.json")},
            "thesis_results_written": False,
        }
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return manifest
    except Exception:
        raise


def self_test() -> dict[str, Any]:
    cards, families, _ = load_extension()
    if len(rows_for_bm25(cards, families)) != 192:
        raise ValueError("extension BM25 self-test count failed")
    v2_rows, _ = validate_v2_reuse(V2_BM25, "RQ1B_FIELD_TYPE_V2_BM25_LOCAL_RUN_MANIFEST")
    if len(v2_rows) != 1392:
        raise ValueError("V2 reuse self-test count failed")
    return {"status": "PASS_LOCAL_ONLY", "network_calls": 0, "new_v3_rows": 192, "reused_v2_rows": 1392}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--bm25", action="store_true")
    parser.add_argument("--qwen-preflight", action="store_true")
    parser.add_argument("--qwen-run", action="store_true")
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    modes = sum((args.bm25, args.qwen_preflight, args.qwen_run, args.self_test))
    if modes != 1:
        parser.error("choose exactly one mode")
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
    elif args.bm25:
        print(json.dumps(write_bm25(args.output_root), indent=2, sort_keys=True))
    elif args.qwen_preflight:
        print(json.dumps(write_qwen_preflight(args.output_root, args.cache_root), indent=2, sort_keys=True))
    else:
        if args.authorisation is None:
            raise ValueError("--authorisation is required for Qwen execution")
        print(json.dumps(write_qwen_result(args.output_root, args.cache_root, args.authorisation, args.timeout_seconds), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
