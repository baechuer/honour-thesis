#!/usr/bin/env python3
"""Run local RQ1b V2+V3 joint-group analysis; Qwen preflight is local only."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from prepare_rq1b_field_type_confirmatory_v2_qwen_preflight import BASE_URL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL
from prepare_rq1b_joint_field_mask_v21 import GROUPS
from run_rq1b_field_type_confirmatory_v2_bm25 import BM25, bootstrap_mean, metric_for_ranking, render_card, tokens
from run_rq1b_field_type_confirmatory_v2_qwen import cache_load, cache_store, chunks, cosine, load_dotenv, post_once
from run_rq1b_v2_v3_complete_triad_extension import EXTENSION, load_extension, sha256_file


REPO = Path(__file__).resolve().parents[2]
JOINT_EXTENSION = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/working/rq1b_v2_v3_joint_group_extension_2026-08-30"
V2_FREEZE = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_joint_mask_v21_2026-08-29/joint_mask_freeze.json"
V2_BM25 = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_bm25_2026-08-29"
V2_QWEN = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_2026-08-29"
V3_CACHE = REPO / "skill_benchmark/cache/rq1b_v2_v3_complete_triad_extension/qwen/text-embedding-v4/1024"
OUTPUT = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30"
VERSION = "rq1b-v2-v3-joint-group-extension-runner-v1"


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


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()


def text_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_directory(output: Path, files: dict[str, str]) -> None:
    if output.exists():
        raise ValueError(f"refusing to overwrite output: {output}")
    staging = output.parent / f".{output.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        for name, content in files.items():
            path = staging / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        staging.replace(output)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def validate_source_result(root: Path, expected_status: str, expected_rows: int) -> list[dict[str, Any]]:
    manifest = read_json(root / "manifest.json")
    if manifest.get("status") != expected_status:
        raise ValueError(f"unexpected source status: {root}")
    rows_path, summary_path = root / "rows.jsonl", root / "summary.json"
    if manifest.get("artifacts", {}).get("rows.jsonl") != sha256_file(rows_path):
        raise ValueError(f"source rows hash mismatch: {root}")
    if manifest.get("artifacts", {}).get("summary.json") != sha256_file(summary_path):
        raise ValueError(f"source summary hash mismatch: {root}")
    rows = read_jsonl(rows_path)
    keys = {(row.get("routing_family_id"), row.get("prompt_variant"), row.get("condition")) for row in rows}
    if len(rows) != expected_rows or len(keys) != expected_rows:
        raise ValueError(f"source row coverage drift: {root}")
    return rows


def load_scope() -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]], list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    freeze = read_json(JOINT_EXTENSION / "freeze.json")
    if freeze.get("status") != "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_FREEZE_NOT_A_RESULT" or freeze.get("version") != "rq1b-v2-v3-joint-group-extension-freeze-v1":
        raise ValueError("joint extension freeze state drift")
    if freeze.get("v2_joint_freeze_sha256") != sha256_file(V2_FREEZE):
        raise ValueError("V2 eligibility freeze drift")
    if freeze.get("groups") != {condition: list(fields) for condition, fields in GROUPS.items()}:
        raise ValueError("joint group definition drift")
    cards_by_key, families, extension_audit = load_extension()
    if freeze.get("v3_extension_audit") != extension_audit or len(families) != 12:
        raise ValueError("V3 extension provenance drift")
    conditions: dict[str, list[dict[str, Any]]] = {}
    for composition_id in freeze["v3_composition_ids"]:
        full_cards = cards_by_key[f"{composition_id}/FULL"]
        for condition, withheld in GROUPS.items():
            payload = read_json(JOINT_EXTENSION / "conditions" / composition_id / f"{condition}.json")
            if digest(payload) != freeze["condition_sha256"][composition_id][condition]:
                raise ValueError(f"V3 group condition hash drift: {composition_id}/{condition}")
            cards = payload.get("cards")
            if not isinstance(cards, list) or [card.get("label") for card in cards] != [card["label"] for card in full_cards]:
                raise ValueError(f"V3 candidate membership drift: {composition_id}/{condition}")
            for full, masked in zip(full_cards, cards, strict=True):
                for field, value in full["slots"].items():
                    expected = "[FIELD WITHHELD IN THIS REPRESENTATION]" if field in withheld else value
                    if masked["slots"].get(field) != expected:
                        raise ValueError(f"V3 slot mutation: {composition_id}/{condition}/{field}")
            conditions[f"{composition_id}/{condition}"] = cards
    return freeze, cards_by_key, families, conditions


def score_v3_bm25(cards_by_key: dict[str, list[dict[str, Any]]], families: list[dict[str, Any]], conditions: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family in families:
        for condition in ("FULL", *GROUPS):
            cards = cards_by_key[f"{family['composition_id']}/FULL"] if condition == "FULL" else conditions[f"{family['composition_id']}/{condition}"]
            index = BM25([card["label"] for card in cards], [render_card(card["slots"]) for card in cards])
            for variant in ("direct", "paraphrase"):
                started = time.perf_counter()
                rows.append({
                    "status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_BM25_ROW_LOCAL_RESULT",
                    "retriever": "bm25",
                    "integration_stratum": "imported_v3_new",
                    "routing_family_id": family["routing_family_id"],
                    "composition_id": family["composition_id"],
                    "source_composition_id": family["source_composition_id"],
                    "prompt_variant": variant,
                    "condition": condition,
                    "gold_label": family["gold_label"],
                    "candidate_count": len(cards),
                    "query_seconds": time.perf_counter() - started,
                    **metric_for_ranking(index.rank(family["prompts"][variant]["prompt"]), family["gold_label"]),
                })
    expected = len(families) * 2 * (1 + len(GROUPS))
    if len(rows) != expected or len({(row["routing_family_id"], row["prompt_variant"], row["condition"]) for row in rows}) != expected:
        raise ValueError("V3 joint-group BM25 coverage drift")
    return rows


def group_summary(rows: list[dict[str, Any]], family_ids: set[str], condition: str, seed_offset: int) -> dict[str, Any]:
    by_key = {(row["routing_family_id"], row["prompt_variant"], row["condition"]): row for row in rows}
    pairs = []
    for family_id in sorted(family_ids):
        for variant in ("direct", "paraphrase"):
            full = by_key.get((family_id, variant, "FULL"))
            masked = by_key.get((family_id, variant, condition))
            if full is None or masked is None:
                raise ValueError(f"missing pair: {condition}/{family_id}/{variant}")
            pairs.append((full, masked))
    by_composition: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    transitions: Counter[str] = Counter()
    for full, masked in pairs:
        transitions[f"{full['hit_at_1']}_to_{masked['hit_at_1']}"] += 1
        for metric, value in {
            "top1": full["hit_at_1"] - masked["hit_at_1"],
            "mrr": full["mrr"] - masked["mrr"],
            "margin": full["gold_minus_best_wrong_margin"] - masked["gold_minus_best_wrong_margin"],
        }.items():
            by_composition[full["composition_id"]][metric].append(value)
    aggregate = {metric: {composition: statistics.mean(values[metric]) for composition, values in by_composition.items()} for metric in ("top1", "mrr", "margin")}
    def mean_value(which: str, metric: str) -> float:
        return statistics.mean(pair[0 if which == "full" else 1][metric] for pair in pairs)
    return {
        "withheld_fields": list(GROUPS[condition]),
        "routing_family_count": len(family_ids),
        "prompt_pair_count": len(pairs),
        "composition_count": len(by_composition),
        "full": {"top1": mean_value("full", "hit_at_1"), "mrr": mean_value("full", "mrr"), "mean_gold_rank": mean_value("full", "gold_rank"), "mean_margin": mean_value("full", "gold_minus_best_wrong_margin")},
        "masked": {"top1": mean_value("masked", "hit_at_1"), "mrr": mean_value("masked", "mrr"), "mean_gold_rank": mean_value("masked", "gold_rank"), "mean_margin": mean_value("masked", "gold_minus_best_wrong_margin")},
        "full_correct_to_masked_wrong_rate": statistics.mean(full["hit_at_1"] == 1 and masked["hit_at_1"] == 0 for full, masked in pairs),
        "transition_counts": dict(sorted(transitions.items())),
        "composition_bootstrap_full_minus_mask": {
            "top1": bootstrap_mean(aggregate["top1"], 20260870 + seed_offset),
            "mrr": bootstrap_mean(aggregate["mrr"], 20260970 + seed_offset),
            "margin": bootstrap_mean(aggregate["margin"], 20261070 + seed_offset),
        },
    }


def combined_group_rows(v2_rows: list[dict[str, Any]], v3_rows: list[dict[str, Any]], v2_eligibility: dict[str, list[str]], condition: str) -> tuple[list[dict[str, Any]], set[str]]:
    v2_ids = set(v2_eligibility[condition])
    v3_ids = {row["routing_family_id"] for row in v3_rows}
    selected_v2 = [{**row, "integration_stratum": "native_v2_reused"} for row in v2_rows if row["routing_family_id"] in v2_ids and row["condition"] in {"FULL", condition}]
    selected_v3 = [row for row in v3_rows if row["condition"] in {"FULL", condition}]
    expected = (len(v2_ids) + len(v3_ids)) * 2 * 2
    rows = selected_v2 + selected_v3
    keys = {(row["routing_family_id"], row["prompt_variant"], row["condition"]) for row in rows}
    if len(rows) != expected or len(keys) != expected or v2_ids & v3_ids:
        raise ValueError(f"combined group coverage drift: {condition}")
    return rows, v2_ids | v3_ids


def write_bm25(output_root: Path = OUTPUT) -> dict[str, Any]:
    if (output_root / "bm25").exists():
        raise ValueError("refusing to overwrite joint V2+V3 BM25 results")
    started = time.perf_counter()
    freeze, cards_by_key, families, conditions = load_scope()
    v2_eligibility = read_json(V2_FREEZE).get("group_eligible_routing_family_ids")
    if not isinstance(v2_eligibility, dict) or {
        condition: len(v2_eligibility.get(condition, [])) for condition in GROUPS
    } != freeze["v2_eligible_family_counts"]:
        raise ValueError("V2 group eligibility IDs/counts drift")
    v2_rows = validate_source_result(V2_BM25, "RQ1B_JOINT_FIELD_MASK_V21_BM25_LOCAL_RUN_MANIFEST", 696)
    v3_rows = score_v3_bm25(cards_by_key, families, conditions)
    combined: list[dict[str, Any]] = []
    groups: dict[str, Any] = {}
    for position, condition in enumerate(GROUPS, start=1):
        selected, family_ids = combined_group_rows(v2_rows, v3_rows, v2_eligibility, condition)
        combined.extend([{**row, "analysis_group": condition} for row in selected])
        groups[condition] = group_summary(selected, family_ids, condition, position)
    summary = {
        "status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_BM25_SUPPORTING_RESULT",
        "claim_boundary": [
            "This is a supporting joint-field availability analysis, not a single-field causal estimate.",
            "Each group is a separate paired FULL-versus-its-own-mask comparison with its frozen V2 eligibility intersection plus all complete V3 families.",
            "V2 rows are manifest-verified reuse; only 96 V3 rows are newly scored locally.",
        ],
        "retriever": "bm25",
        "groups": groups,
    }
    manifest = {
        "status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_BM25_LOCAL_RUN_MANIFEST",
        "runner_version": VERSION,
        "network_calls": 0,
        "texts_transmitted": 0,
        "thesis_results_written": False,
        "inputs": {"joint_extension_freeze.json": sha256_file(JOINT_EXTENSION / "freeze.json"), "v2_bm25_manifest.json": sha256_file(V2_BM25 / "manifest.json")},
        "counts": {"reused_v2_rows": len(v2_rows), "new_v3_rows": len(v3_rows), "analysis_rows_across_three_group_comparisons": len(combined)},
        "timing": {"new_v3_query_seconds": sum(row["query_seconds"] for row in v3_rows), "wall_seconds": time.perf_counter() - started},
    }
    files = {"v3_rows.jsonl": "".join(json.dumps(row, sort_keys=True) + "\n" for row in v3_rows), "combined_group_rows.jsonl": "".join(json.dumps(row, sort_keys=True) + "\n" for row in combined), "summary.json": json.dumps(summary, indent=2, sort_keys=True) + "\n"}
    for name, content in files.items():
        manifest.setdefault("artifacts", {})[name] = hashlib.sha256(content.encode("utf-8")).hexdigest()
    files["manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    atomic_directory(output_root / "bm25", files)
    return manifest


def qwen_preflight(output_root: Path = OUTPUT, cache_root: Path = V3_CACHE) -> dict[str, Any]:
    if (output_root / "qwen_preflight").exists():
        raise ValueError("refusing to overwrite joint V2+V3 Qwen preflight")
    _, cards_by_key, families, conditions = load_scope()
    inventory: dict[str, dict[str, Any]] = {}
    def register(text: str, role: dict[str, str]) -> None:
        identifier = text_id(text)
        row = inventory.setdefault(identifier, {"text_id": identifier, "text": text, "utf8_bytes": len(text.encode("utf-8")), "local_lexical_token_proxy": len(tokens(text)), "roles": []})
        if row["text"] != text:
            raise ValueError("text hash collision")
        row["roles"].append(role)
    for family in families:
        for variant in ("direct", "paraphrase"):
            register(family["prompts"][variant]["prompt"], {"kind": "query", "routing_family_id": family["routing_family_id"], "prompt_variant": variant})
        for card in cards_by_key[f"{family['composition_id']}/FULL"]:
            register(render_card(card["slots"]), {"kind": "document_full", "composition_id": family["composition_id"], "candidate_label": card["label"]})
        for condition in GROUPS:
            for card in conditions[f"{family['composition_id']}/{condition}"]:
                register(render_card(card["slots"]), {"kind": "document_new_group_mask", "composition_id": family["composition_id"], "condition": condition, "candidate_label": card["label"]})
    all_rows = [inventory[key] for key in sorted(inventory)]
    cached = {row["text_id"] for row in all_rows if cache_load(cache_root, row) is not None}
    missing = [row for row in all_rows if row["text_id"] not in cached]
    missing_roles = {role["kind"] for row in missing for role in row["roles"]}
    if missing_roles - {"document_new_group_mask"}:
        raise ValueError(f"unexpected uncached pre-existing V3 texts: {sorted(missing_roles - {'document_new_group_mask'})}")
    payload = {
        "status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_LOCAL_PREFLIGHT_NOT_EXECUTED",
        "runner_version": VERSION,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "network_calls": 0,
        "texts_transmitted": 0,
        "cache_root": str(cache_root),
        "joint_extension_freeze_sha256": sha256_file(JOINT_EXTENSION / "freeze.json"),
        "text_inventory": all_rows,
        "counts": {"all_unique_texts": len(all_rows), "cache_hits": len(cached), "new_candidate_card_texts": len(missing), "new_query_texts": 0, "new_local_lexical_token_proxy": sum(row["local_lexical_token_proxy"] for row in missing), "new_utf8_bytes": sum(row["utf8_bytes"] for row in missing), "maximum_request_attempts_no_retry": (len(missing) + MAX_BATCH_TEXTS - 1) // MAX_BATCH_TEXTS},
        "authorisation_boundary": {"external_text_transfer_authorized": False, "automatic_retries": 0, "notes": "Only the exact payload below may be authorised later; this file performs no provider request."},
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    manifest = {"status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_PREFLIGHT_LOCAL_NOT_EXECUTED", "payload_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "payload_counts": payload["counts"], "network_calls": 0, "texts_transmitted": 0}
    atomic_directory(output_root / "qwen_preflight", {"payload.json": text, "manifest.json": json.dumps(manifest, indent=2, sort_keys=True) + "\n"})
    return manifest


def validate_qwen_authorisation(authorisation_path: Path, payload_path: Path, output: Path) -> dict[str, Any]:
    authorisation = read_json(authorisation_path)
    required = {
        "status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_ONE_RUN_AUTHORISED",
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


def execute_qwen(cache_root: Path, authorisation_path: Path, dotenv: Path, timeout_seconds: int, output_root: Path = OUTPUT) -> dict[str, Any]:
    payload_path = output_root / "qwen_preflight" / "payload.json"
    payload = read_json(payload_path)
    if payload.get("status") != "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_LOCAL_PREFLIGHT_NOT_EXECUTED":
        raise ValueError("Qwen preflight state drift")
    output = output_root / "qwen"
    if output.exists():
        raise ValueError("refusing to overwrite joint V2+V3 Qwen result")
    authorisation = validate_qwen_authorisation(authorisation_path, payload_path, output)
    actual = payload["counts"]
    for key, value in {
        "maximum_new_texts": actual["new_candidate_card_texts"],
        "maximum_request_attempts": actual["maximum_request_attempts_no_retry"],
        "maximum_successful_calls": actual["maximum_request_attempts_no_retry"],
        "maximum_local_lexical_token_proxy": actual["new_local_lexical_token_proxy"],
        "maximum_utf8_bytes": actual["new_utf8_bytes"],
    }.items():
        if value > authorisation[key]:
            raise ValueError(f"Qwen execution exceeds authorised ceiling: {key}")
    inventory = {row["text_id"]: row for row in payload["text_inventory"]}
    vectors = {identifier: cache_load(cache_root, row) for identifier, row in inventory.items()}
    missing = [row for identifier, row in inventory.items() if vectors[identifier] is None]
    if len(missing) != actual["new_candidate_card_texts"] or any(role["kind"] != "document_new_group_mask" for row in missing for role in row["roles"]):
        raise ValueError("Qwen cache state no longer matches preflight payload")
    load_dotenv(dotenv)
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY unavailable after loading configured dotenv")
    output.mkdir(parents=True)
    requests = output / "requests"
    requests.mkdir()
    attempts = successful = 0
    provider_usage: dict[str, int] = {}
    try:
        for group in chunks(missing):
            if attempts >= authorisation["maximum_request_attempts"] or successful >= authorisation["maximum_successful_calls"]:
                raise ValueError("Qwen call ceiling reached before request")
            attempts += 1
            attempt = {"attempt": attempts, "role": "document_new_group_mask", "text_ids": [row["text_id"] for row in group], "text_count": len(group), "automatic_retry": False}
            (requests / f"request_{attempts:04d}_attempt.json").write_text(json.dumps(attempt, indent=2, sort_keys=True) + "\n")
            started = time.perf_counter()
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
            receipt = {**attempt, "state": "success", "request_seconds": time.perf_counter() - started, "provider_usage": usage}
            (requests / f"request_{attempts:04d}_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            successful += 1
            for key, value in usage.items():
                if isinstance(value, int):
                    provider_usage[key] = provider_usage.get(key, 0) + value
            for row, response_row in zip(group, ordered, strict=True):
                vector = [float(value) for value in response_row.get("embedding", [])]
                if len(vector) != DIMENSIONS or not all(math.isfinite(value) for value in vector):
                    raise ValueError("Qwen returned invalid embedding")
                cache_store(cache_root, row, vector, receipt)
                vectors[row["text_id"]] = vector
            print(f"QWEN_PROGRESS request={attempts}/{actual['maximum_request_attempts_no_retry']} texts={len(group)}", flush=True)

        freeze, cards_by_key, families, conditions = load_scope()
        v2_eligibility = read_json(V2_FREEZE)["group_eligible_routing_family_ids"]
        v2_rows = validate_source_result(V2_QWEN, "RQ1B_JOINT_FIELD_MASK_V21_QWEN_RUN_EXTERNAL_RESULT", 696)
        v3_rows: list[dict[str, Any]] = []
        for family in families:
            for variant in ("direct", "paraphrase"):
                prompt = family["prompts"][variant]["prompt"]
                query_vector = vectors[text_id(prompt)]
                for condition in ("FULL", *GROUPS):
                    cards = cards_by_key[f"{family['composition_id']}/FULL"] if condition == "FULL" else conditions[f"{family['composition_id']}/{condition}"]
                    ranking = sorted(((card["label"], cosine(query_vector, vectors[text_id(render_card(card["slots"]))])) for card in cards), key=lambda item: (-item[1], item[0]))
                    v3_rows.append({"status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_ROW_EXTERNAL_RESULT", "retriever": "qwen-text-embedding-v4", "integration_stratum": "imported_v3_new", "routing_family_id": family["routing_family_id"], "composition_id": family["composition_id"], "source_composition_id": family["source_composition_id"], "prompt_variant": variant, "condition": condition, "gold_label": family["gold_label"], "candidate_count": len(cards), "query_seconds": None, **metric_for_ranking(ranking, family["gold_label"])})
        if len(v3_rows) != 96:
            raise ValueError("V3 Qwen row coverage drift")
        combined: list[dict[str, Any]] = []
        groups: dict[str, Any] = {}
        for position, condition in enumerate(GROUPS, start=1):
            selected, family_ids = combined_group_rows(v2_rows, v3_rows, v2_eligibility, condition)
            combined.extend([{**row, "analysis_group": condition} for row in selected])
            groups[condition] = group_summary(selected, family_ids, condition, position)
        summary = {"status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_SUPPORTING_RESULT", "claim_boundary": ["This is supporting joint-field availability analysis, not a single-field causal estimate.", "Each group retains its frozen V2 eligibility intersection plus all complete V3 families."], "retriever": "qwen-text-embedding-v4", "groups": groups}
        (output / "v3_rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in v3_rows), encoding="utf-8")
        (output / "combined_group_rows.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in combined), encoding="utf-8")
        (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        manifest = {"status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_EXTERNAL_RUN_MANIFEST", "runner_version": VERSION, "payload_sha256": sha256_file(payload_path), "authorisation_sha256": sha256_file(authorisation_path), "execution": {"cache_hits": len(inventory) - len(missing), "cache_misses": len(missing), "request_attempts": attempts, "successful_calls": successful, "provider_usage": provider_usage}, "counts": {"reused_v2_rows": len(v2_rows), "new_v3_rows": len(v3_rows), "analysis_rows_across_three_group_comparisons": len(combined)}, "artifacts": {name: sha256_file(output / name) for name in ("v3_rows.jsonl", "combined_group_rows.jsonl", "summary.json")}, "thesis_results_written": False}
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return manifest
    except Exception:
        raise


def qwen_dry_check(output_root: Path = OUTPUT, cache_root: Path = V3_CACHE) -> dict[str, Any]:
    payload = read_json(output_root / "qwen_preflight" / "payload.json")
    if payload.get("status") != "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_LOCAL_PREFLIGHT_NOT_EXECUTED":
        raise ValueError("Qwen preflight state drift")
    missing = [row for row in payload["text_inventory"] if cache_load(cache_root, row) is None]
    if len(missing) != 36 or any(role["kind"] != "document_new_group_mask" for row in missing for role in row["roles"]):
        raise ValueError("Qwen dry-check cache scope drift")
    return {"status": "PASS_LOCAL_ONLY", "payload_sha256": sha256_file(output_root / "qwen_preflight" / "payload.json"), "new_external_candidate_cards": len(missing), "new_external_queries": 0, "maximum_no_retry_calls": 4, "network_calls": 0}


def check(output_root: Path = OUTPUT) -> dict[str, Any]:
    bm25 = read_json(output_root / "bm25" / "manifest.json")
    if bm25.get("status") != "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_BM25_LOCAL_RUN_MANIFEST":
        raise ValueError("BM25 manifest state drift")
    for name in ("v3_rows.jsonl", "combined_group_rows.jsonl", "summary.json"):
        if bm25.get("artifacts", {}).get(name) != sha256_file(output_root / "bm25" / name):
            raise ValueError(f"BM25 artifact hash drift: {name}")
    rows = read_jsonl(output_root / "bm25" / "combined_group_rows.jsonl")
    expected = 2 * 2 * sum((85, 89, 82))
    if len(rows) != expected:
        raise ValueError("combined group row count drift")
    summary = read_json(output_root / "bm25" / "summary.json")
    if set(summary.get("groups", {})) != set(GROUPS):
        raise ValueError("summary group coverage drift")
    result: dict[str, Any] = {"status": "PASS", "bm25_combined_group_rows": len(rows), "groups": {key: value["routing_family_count"] for key, value in summary["groups"].items()}}
    qwen_root = output_root / "qwen"
    if qwen_root.exists():
        qwen = read_json(qwen_root / "manifest.json")
        if qwen.get("status") != "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_QWEN_EXTERNAL_RUN_MANIFEST":
            raise ValueError("Qwen manifest state drift")
        for name in ("v3_rows.jsonl", "combined_group_rows.jsonl", "summary.json"):
            if qwen.get("artifacts", {}).get(name) != sha256_file(qwen_root / name):
                raise ValueError(f"Qwen artifact hash drift: {name}")
        qwen_rows = read_jsonl(qwen_root / "combined_group_rows.jsonl")
        if len(qwen_rows) != expected:
            raise ValueError("Qwen combined group row count drift")
        qwen_summary = read_json(qwen_root / "summary.json")
        if set(qwen_summary.get("groups", {})) != set(GROUPS):
            raise ValueError("Qwen summary group coverage drift")
        result["qwen_combined_group_rows"] = len(qwen_rows)
        result["qwen_execution"] = qwen["execution"]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bm25", action="store_true")
    parser.add_argument("--qwen-preflight", action="store_true")
    parser.add_argument("--qwen-dry-check", action="store_true")
    parser.add_argument("--qwen-run", action="store_true")
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--dotenv", type=Path, default=Path(".env"))
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if sum((args.bm25, args.qwen_preflight, args.qwen_dry_check, args.qwen_run, args.check)) != 1:
        parser.error("choose exactly one mode")
    if args.bm25:
        result = write_bm25()
    elif args.qwen_preflight:
        result = qwen_preflight()
    elif args.qwen_dry_check:
        result = qwen_dry_check()
    elif args.qwen_run:
        if args.authorisation is None:
            raise ValueError("--authorisation is required for Qwen execution")
        result = execute_qwen(V3_CACHE, args.authorisation, args.dotenv, args.timeout_seconds)
    else:
        result = check()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
