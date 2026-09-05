#!/usr/bin/env python3
"""Aggregate validated B0G reviews and run approved blinded adjudications.

This local controller never calls a provider, scores a selector, or exposes
initial A/B labels in an adjudication packet. It is deliberately separate from
the frozen initial-review controller: its only inputs are the frozen plan,
metadata-only validated decisions, and the source/prompt manifests required to
materialise a permitted third blind review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import build_rq2b_b0g_batched_review as initial


ROLE = "C"
PREFIX = "adjudication"
LABELS = initial.LABELS
ELIGIBILITY_LABELS = {"fully_acceptable", "uncertain"}
PLAN_FIELDS = {
    "adjudication_token",
    "unit_token",
    "batch_id",
    "batch_ordinal",
    "prompt_sha256",
    "candidate_source_sha256",
    "prompt_chars",
    "source_chars",
    "combined_chars",
}
PACKET_FIELDS = {"review_token", "user_request", "candidate_skill_document", "rubric"}
VALIDATION_FIELDS = {
    "batch_id",
    "state",
    "assignments",
    "label_counts",
    "packet_sha256",
    "decision_sha256",
    "validated_adjudications_path",
    "validated_adjudications_sha256",
    "plan_sha256",
    "network_calls",
    "provider_calls",
}
MANIFEST_FIELDS = {
    "schema_version",
    "state",
    "initial_plan_sha256",
    "initial_validation_inventory_sha256",
    "eligibility_rule",
    "eligible_units",
    "max_units_per_batch",
    "max_chars_per_batch",
    "batch_count",
    "plan_path",
    "plan_sha256",
    "network_calls",
    "provider_calls",
    "raw_text_in_plan",
}
INITIAL_VALIDATION_FIELDS = {
    "batch_id",
    "state",
    "assignments",
    "label_counts",
    "packet_sha256",
    "decision_sha256",
    "validated_decisions_path",
    "validated_decisions_sha256",
    "plan_sha256",
    "network_calls",
    "provider_calls",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_text(json.dumps(value, sort_keys=True, separators=(",", ":")))


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def root_dir(root: Path) -> Path:
    return initial.review_root(root) / "adjudication_v1_2026-08-09"


def cache_dir(root: Path) -> Path:
    return initial.cache_root(root) / "adjudication"


def write_json_new(path: Path, value: Any) -> None:
    require(not path.exists(), f"Refusing to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    require(not path.exists(), f"Refusing to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"Missing JSON input: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON input is not an object: {path}")
    return value


def validate_raw_decisions(
    packet_rows: list[dict[str, Any]], decisions: list[dict[str, Any]], expected: set[str], context: str
) -> list[dict[str, Any]]:
    require(all(set(row) == PACKET_FIELDS for row in packet_rows), f"{context} packet schema mismatch")
    packet_by_token = {row["review_token"]: row for row in packet_rows}
    require(len(packet_by_token) == len(packet_rows) and set(packet_by_token) == expected, f"{context} packet token mismatch")
    require(len(decisions) == len(expected), f"{context} decision count mismatch")
    sanitized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for decision in decisions:
        require(set(decision) == {"review_token", "label", "reason", "source_evidence"}, f"{context} decision schema mismatch")
        token = decision["review_token"]
        require(token in expected and token not in seen, f"{context} decision token mismatch")
        require(decision["label"] in LABELS, f"{context} label mismatch")
        require(isinstance(decision["reason"], str) and 1 <= len(decision["reason"].strip()) <= 1_200, f"{context} reason mismatch")
        evidence = decision["source_evidence"]
        require(isinstance(evidence, list) and len(evidence) <= 3 and all(isinstance(item, str) for item in evidence), f"{context} evidence schema mismatch")
        source_text = packet_by_token[token]["candidate_skill_document"]
        require(all(item and item in source_text for item in evidence), f"{context} non-substring source evidence")
        seen.add(token)
        sanitized.append(
            {
                "review_token": token,
                "label": decision["label"],
                "decision_sha256": sha256_text(json.dumps(decision, sort_keys=True)),
            }
        )
    require(seen == expected, f"{context} decision token coverage mismatch")
    return sorted(sanitized, key=lambda row: row["review_token"])


def validated_initial_labels(root: Path) -> tuple[list[dict[str, Any]], dict[str, str], str]:
    """Fail closed unless every A/B assignment has a validated metadata record."""
    plan, manifest = initial.load_plan(root)
    validation_dir = initial.review_root(root) / "validated_decisions"
    validation_paths = sorted(validation_dir.glob("*.validation.json"))
    expected_by_batch: dict[str, set[str]] = defaultdict(set)
    assignment_by_token = {row["assignment_token"]: row for row in plan}
    for row in plan:
        expected_by_batch[row["batch_id"]].add(row["assignment_token"])
    require(
        {path.stem.removesuffix(".validation") for path in validation_paths} == set(expected_by_batch),
        "Initial validation-batch coverage mismatch",
    )
    labels: dict[str, str] = {}
    inventory: list[dict[str, str]] = []
    for validation_path in validation_paths:
        validation = read_json(validation_path)
        require(set(validation) == INITIAL_VALIDATION_FIELDS, "Initial validation schema mismatch")
        batch_id = validation.get("batch_id")
        require(batch_id in expected_by_batch, "Unexpected initial validation batch")
        require(validation.get("state") == "validated_blinded_decisions_no_adjudication", "Initial validation state mismatch")
        require(validation.get("plan_sha256") == manifest["plan_sha256"], "Initial validation plan mismatch")
        require(validation.get("assignments") == len(expected_by_batch[batch_id]), "Initial validation count mismatch")
        packet_path = initial.cache_root(root) / "packets" / f"{batch_id}.jsonl"
        raw_decision_path = initial.cache_root(root) / "decisions" / f"{batch_id}.jsonl"
        require(is_sha256(validation.get("packet_sha256")), "Initial packet hash shape mismatch")
        require(is_sha256(validation.get("decision_sha256")), "Initial decision hash shape mismatch")
        require(initial.sha256_file(packet_path) == validation["packet_sha256"], "Initial packet hash mismatch")
        require(initial.sha256_file(raw_decision_path) == validation["decision_sha256"], "Initial raw-decision hash mismatch")
        decision_path = root / str(validation.get("validated_decisions_path", ""))
        require(decision_path == validation_dir / f"{batch_id}.jsonl", "Initial validation decision path mismatch")
        require(initial.sha256_file(decision_path) == validation.get("validated_decisions_sha256"), "Initial validated-decision hash mismatch")
        packet_rows = initial.read_jsonl(packet_path)
        raw_decisions = initial.read_jsonl(raw_decision_path)
        rows = initial.read_jsonl(decision_path)
        assignments = [row for row in plan if row["batch_id"] == batch_id]
        require(packet_rows == initial.expected_packet_rows(root, assignments), "Initial packet does not match frozen source/prompt reconstruction")
        expected_rows = validate_raw_decisions(packet_rows, raw_decisions, expected_by_batch[batch_id], "Initial")
        require(rows == expected_rows, "Initial validated-decision content drift")
        require(validation.get("label_counts") == dict(sorted(Counter(row["label"] for row in rows).items())), "Initial validation label-count mismatch")
        require(validation.get("network_calls") == validation.get("provider_calls") == 0, "Initial validation boundary mismatch")
        seen: set[str] = set()
        for row in rows:
            require(set(row) == {"review_token", "label", "decision_sha256"}, "Initial validated-decision schema mismatch")
            token = row["review_token"]
            require(token in expected_by_batch[batch_id] and token not in seen, "Initial validated-decision token mismatch")
            require(row["label"] in LABELS, "Initial validated-decision label mismatch")
            require(is_sha256(row["decision_sha256"]), "Initial decision hash mismatch")
            seen.add(token)
            labels[token] = row["label"]
        require(seen == expected_by_batch[batch_id], "Initial validated-decision token coverage mismatch")
        inventory.append(
            {
                "batch_id": batch_id,
                "packet_sha256": str(validation["packet_sha256"]),
                "decision_sha256": str(validation["decision_sha256"]),
                "validated_decisions_sha256": str(validation["validated_decisions_sha256"]),
            }
        )
    require(set(labels) == set(assignment_by_token), "Initial label coverage mismatch")
    return plan, labels, canonical_sha256(sorted(inventory, key=lambda row: row["batch_id"]))


def eligible_units(root: Path) -> tuple[list[dict[str, Any]], str, str]:
    plan, labels, inventory_sha = validated_initial_labels(root)
    by_unit: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for assignment in plan:
        label = labels[assignment["assignment_token"]]
        by_unit[assignment["unit_token"]][assignment["reviewer_role"]] = {"assignment": assignment, "label": label}
    rows: list[dict[str, Any]] = []
    for unit_token, roles in by_unit.items():
        require(set(roles) == set(initial.ROLES), "Initial A/B role coverage mismatch")
        a_label = roles["A"]["label"]
        b_label = roles["B"]["label"]
        if a_label == b_label or not ({a_label, b_label} & ELIGIBILITY_LABELS):
            continue
        reference = roles["A"]["assignment"]
        rows.append(
            {
                "unit_token": unit_token,
                "prompt_sha256": reference["prompt_sha256"],
                "candidate_source_sha256": reference["candidate_source_sha256"],
                "prompt_chars": reference["prompt_chars"],
                "source_chars": reference["source_chars"],
                "combined_chars": reference["combined_chars"],
            }
        )
    return rows, initial.load_plan(root)[1]["plan_sha256"], inventory_sha


def deterministic_order(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: sha256_text(f"{initial.SEED}|{ROLE}|{row['unit_token']}"))


def plan_rows_for_eligible(eligible: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plan_rows: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    batch_index = 0

    def append_current() -> None:
        nonlocal batch_index, current, current_chars
        for ordinal, row in enumerate(current, start=1):
            plan_rows.append(
                {
                    "adjudication_token": initial.opaque_token(PREFIX, row["unit_token"]),
                    "unit_token": row["unit_token"],
                    "batch_id": f"{ROLE}-{batch_index:04d}",
                    "batch_ordinal": ordinal,
                    "prompt_sha256": row["prompt_sha256"],
                    "candidate_source_sha256": row["candidate_source_sha256"],
                    "prompt_chars": row["prompt_chars"],
                    "source_chars": row["source_chars"],
                    "combined_chars": row["combined_chars"],
                }
            )
        batch_index += 1
        current = []
        current_chars = 0

    for row in deterministic_order(eligible):
        over_count = len(current) >= initial.MAX_UNITS_PER_BATCH
        over_chars = current and current_chars + row["combined_chars"] > initial.MAX_CHARS_PER_BATCH
        if over_count or over_chars:
            append_current()
        current.append(row)
        current_chars += row["combined_chars"]
    if current:
        append_current()
    require(len(plan_rows) == len(eligible), "Adjudication planning count mismatch")
    require(len({row["adjudication_token"] for row in plan_rows}) == len(plan_rows), "Adjudication-token collision")
    return sorted(plan_rows, key=lambda row: row["adjudication_token"])


def build_adjudication_plan(root: Path) -> dict[str, Any]:
    output_root = root_dir(root)
    plan_path = output_root / "adjudication_plan.jsonl"
    manifest_path = output_root / "adjudication_plan_manifest.json"
    require(not plan_path.exists() and not manifest_path.exists(), "Adjudication plan already exists")
    eligible, initial_plan_sha, inventory_sha = eligible_units(root)
    plan_rows = plan_rows_for_eligible(eligible)
    write_jsonl_new(plan_path, plan_rows)
    manifest = {
        "schema_version": "rq2b-b0g-adjudication-plan-v1",
        "state": "eligible_planned_no_adjudication_decisions",
        "initial_plan_sha256": initial_plan_sha,
        "initial_validation_inventory_sha256": inventory_sha,
        "eligibility_rule": "A/B labels disagree and at least one label is fully_acceptable or uncertain",
        "eligible_units": len(eligible),
        "max_units_per_batch": initial.MAX_UNITS_PER_BATCH,
        "max_chars_per_batch": initial.MAX_CHARS_PER_BATCH,
        "batch_count": len({row["batch_id"] for row in plan_rows}),
        "plan_path": str(plan_path.relative_to(root)),
        "plan_sha256": initial.sha256_file(plan_path),
        "network_calls": 0,
        "provider_calls": 0,
        "raw_text_in_plan": False,
    }
    write_json_new(manifest_path, manifest)
    return manifest


def load_adjudication_plan(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    output_root = root_dir(root)
    plan_path = output_root / "adjudication_plan.jsonl"
    manifest_path = output_root / "adjudication_plan_manifest.json"
    plan = initial.read_jsonl(plan_path)
    manifest = read_json(manifest_path)
    require(set(manifest) == MANIFEST_FIELDS, "Adjudication manifest schema mismatch")
    require(manifest["schema_version"] == "rq2b-b0g-adjudication-plan-v1", "Adjudication manifest version mismatch")
    require(manifest["state"] == "eligible_planned_no_adjudication_decisions", "Adjudication manifest state mismatch")
    require(manifest["plan_path"] == str(plan_path.relative_to(root)), "Adjudication plan-path mismatch")
    require(manifest["plan_sha256"] == initial.sha256_file(plan_path), "Adjudication plan hash mismatch")
    require(manifest["raw_text_in_plan"] is False and manifest["network_calls"] == manifest["provider_calls"] == 0, "Adjudication manifest boundary mismatch")
    eligible, initial_plan_sha, inventory_sha = eligible_units(root)
    require(manifest["initial_plan_sha256"] == initial_plan_sha, "Initial-plan binding drift")
    require(manifest["initial_validation_inventory_sha256"] == inventory_sha, "Initial-validation binding drift")
    require(manifest["eligible_units"] == len(eligible), "Eligible-unit count drift")
    require(manifest["batch_count"] == len({row["batch_id"] for row in plan}), "Adjudication batch-count mismatch")
    require(len(plan) == len(eligible), "Adjudication plan row count mismatch")
    require(all(set(row) == PLAN_FIELDS for row in plan), "Adjudication plan row schema mismatch")
    require(plan == plan_rows_for_eligible(eligible), "Adjudication plan is not the prescribed deterministic plan")
    seen_tokens: set[str] = set()
    by_batch: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in plan:
        require(row["adjudication_token"].startswith("adjudication_"), "Adjudication token prefix mismatch")
        require(row["batch_id"].startswith(f"{ROLE}-"), "Adjudication batch role mismatch")
        require(row["adjudication_token"] not in seen_tokens, "Duplicate adjudication token")
        seen_tokens.add(row["adjudication_token"])
        require(row["combined_chars"] == row["prompt_chars"] + row["source_chars"], "Adjudication character sum mismatch")
        by_batch[row["batch_id"]].append(row)
    for batch_id, rows in by_batch.items():
        require(len(rows) <= initial.MAX_UNITS_PER_BATCH, f"Adjudication batch exceeds unit cap: {batch_id}")
        require({row["batch_ordinal"] for row in rows} == set(range(1, len(rows) + 1)), "Adjudication ordinals are not contiguous")
        chars = sum(row["combined_chars"] for row in rows)
        require(len(rows) == 1 or chars <= initial.MAX_CHARS_PER_BATCH, f"Adjudication batch exceeds character cap: {batch_id}")
    return plan, manifest


def expected_packet_rows(root: Path, assignments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    units = initial.unit_lookup(root)
    paths = initial.input_paths(root)
    sources = {row["skill_id"]: row for row in initial.read_jsonl(paths["source_manifest"])}
    prompts = {row["prompt_id"]: row for row in initial.read_jsonl(paths["prompt_manifest"])}
    packet_rows: list[dict[str, Any]] = []
    for assignment in sorted(assignments, key=lambda row: row["batch_ordinal"]):
        unit = units[assignment["unit_token"]]
        prompt = prompts[unit["_prompt_id"]]
        source = sources[unit["_skill_id"]]
        source_bytes = (root / source["source_path"]).read_bytes()
        require(hashlib.sha256(source_bytes).hexdigest() == source["source_sha256"], "Adjudication source hash drift")
        require(sha256_text(prompt["prompt"]) == prompt["prompt_sha256"], "Adjudication prompt hash drift")
        packet_rows.append(
            {
                "review_token": assignment["adjudication_token"],
                "user_request": prompt["prompt"],
                "candidate_skill_document": source_bytes.decode("utf-8"),
                "rubric": {
                    "fully_acceptable": "Fulfils every material request requirement.",
                    "partially_suitable": "Relevant but misses a material requirement.",
                    "not_suitable": "Does not solve the requested task.",
                    "uncertain": "The supplied request and source do not support a reliable judgement.",
                },
            }
        )
    return packet_rows


def materialise_batch(root: Path, batch_id: str) -> dict[str, Any]:
    plan, manifest = load_adjudication_plan(root)
    assignments = [row for row in plan if row["batch_id"] == batch_id]
    require(assignments, f"Unknown adjudication batch: {batch_id}")
    packet_rows = expected_packet_rows(root, assignments)
    packet_chars = sum(len(row["user_request"]) + len(row["candidate_skill_document"]) for row in packet_rows)
    require(len(packet_rows) == 1 or packet_chars <= initial.MAX_CHARS_PER_BATCH, "Adjudication packet exceeds character cap")
    packet_path = cache_dir(root) / "packets" / f"{batch_id}.jsonl"
    write_jsonl_new(packet_path, packet_rows)
    return {"batch_id": batch_id, "assignments": len(packet_rows), "packet_chars": packet_chars, "packet_path": str(packet_path), "packet_sha256": initial.sha256_file(packet_path), "plan_sha256": manifest["plan_sha256"], "network_calls": 0}


def validate_batch(root: Path, batch_id: str) -> dict[str, Any]:
    plan, manifest = load_adjudication_plan(root)
    assignments = [row for row in plan if row["batch_id"] == batch_id]
    require(assignments, f"Unknown adjudication batch: {batch_id}")
    expected = {row["adjudication_token"] for row in assignments}
    packet_path = cache_dir(root) / "packets" / f"{batch_id}.jsonl"
    decision_path = cache_dir(root) / "decisions" / f"{batch_id}.jsonl"
    packet_rows = initial.read_jsonl(packet_path)
    decisions = initial.read_jsonl(decision_path)
    expected_packet = expected_packet_rows(root, assignments)
    require(packet_rows == expected_packet, "Adjudication packet does not match frozen source/prompt reconstruction")
    sanitized = validate_raw_decisions(packet_rows, decisions, expected, "Adjudication")
    output_dir = root_dir(root) / "validated_adjudications"
    output_path = output_dir / f"{batch_id}.jsonl"
    write_jsonl_new(output_path, sanitized)
    summary = {"batch_id": batch_id, "state": "validated_blinded_adjudications_no_acceptable_set", "assignments": len(expected), "label_counts": dict(sorted(Counter(row["label"] for row in sanitized).items())), "packet_sha256": initial.sha256_file(packet_path), "decision_sha256": initial.sha256_file(decision_path), "validated_adjudications_path": str(output_path.relative_to(root)), "validated_adjudications_sha256": initial.sha256_file(output_path), "plan_sha256": manifest["plan_sha256"], "network_calls": 0, "provider_calls": 0}
    write_json_new(output_dir / f"{batch_id}.validation.json", summary)
    return summary


def validated_adjudication_records(
    root: Path, plan: list[dict[str, Any]], manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    validation_dir = root_dir(root) / "validated_adjudications"
    validations = sorted(validation_dir.glob("*.validation.json")) if validation_dir.exists() else []
    expected_by_batch: dict[str, set[str]] = defaultdict(set)
    for row in plan:
        expected_by_batch[row["batch_id"]].add(row["adjudication_token"])
    records: list[dict[str, Any]] = []
    for validation_path in validations:
        validation = read_json(validation_path)
        require(set(validation) == VALIDATION_FIELDS, "Adjudication validation schema mismatch")
        batch_id = validation["batch_id"]
        require(batch_id in expected_by_batch, "Unexpected adjudication validation batch")
        require(validation["state"] == "validated_blinded_adjudications_no_acceptable_set", "Adjudication validation state mismatch")
        require(validation["plan_sha256"] == manifest["plan_sha256"], "Adjudication validation plan mismatch")
        require(validation["assignments"] == len(expected_by_batch[batch_id]), "Adjudication validation count mismatch")
        require(validation["network_calls"] == validation["provider_calls"] == 0, "Adjudication validation boundary mismatch")
        packet_path = cache_dir(root) / "packets" / f"{batch_id}.jsonl"
        decision_path = cache_dir(root) / "decisions" / f"{batch_id}.jsonl"
        output_path = root / str(validation["validated_adjudications_path"])
        require(output_path == validation_dir / f"{batch_id}.jsonl", "Adjudication validation output path mismatch")
        require(initial.sha256_file(packet_path) == validation["packet_sha256"], "Adjudication packet hash mismatch")
        require(initial.sha256_file(decision_path) == validation["decision_sha256"], "Adjudication raw-decision hash mismatch")
        require(initial.sha256_file(output_path) == validation["validated_adjudications_sha256"], "Adjudication sanitized hash mismatch")
        decisions = initial.read_jsonl(decision_path)
        sanitized = initial.read_jsonl(output_path)
        assignments = [row for row in plan if row["batch_id"] == batch_id]
        expected_packet = expected_packet_rows(root, assignments)
        packet_rows = initial.read_jsonl(packet_path)
        require(packet_rows == expected_packet, "Adjudication validation packet reconstruction mismatch")
        expected_sanitized = validate_raw_decisions(packet_rows, decisions, expected_by_batch[batch_id], "Adjudication")
        require(sanitized == expected_sanitized, "Adjudication sanitized decision content drift")
        require(validation["label_counts"] == dict(sorted(Counter(row["label"] for row in sanitized).items())), "Adjudication validation label-count mismatch")
        records.append(validation)
    require(len({record["batch_id"] for record in records}) == len(records), "Duplicate adjudication validation batch")
    return records


def summary(root: Path) -> dict[str, Any]:
    plan, manifest = load_adjudication_plan(root)
    records = validated_adjudication_records(root, plan, manifest)
    completed = {record["batch_id"] for record in records}
    all_batches = {row["batch_id"] for row in plan}
    return {"schema_version": "rq2b-b0g-adjudication-summary-v1", "state": "adjudication_complete_pending_acceptable_set" if completed == all_batches else "adjudication_in_progress", "plan_sha256": manifest["plan_sha256"], "eligible_units": len(plan), "batches_total": len(all_batches), "batches_validated": len(completed), "assignments_validated": sum(record["assignments"] for record in records), "batches_pending": len(all_batches - completed), "network_calls": 0, "provider_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--build-plan", action="store_true")
    actions.add_argument("--materialise-batch")
    actions.add_argument("--validate-batch")
    actions.add_argument("--summary", action="store_true")
    parser.add_argument("--root", type=Path, default=initial.repo_root())
    args = parser.parse_args()
    root = args.root.resolve()
    if args.build_plan:
        result = build_adjudication_plan(root)
    elif args.materialise_batch:
        result = materialise_batch(root, args.materialise_batch)
    elif args.validate_batch:
        result = validate_batch(root, args.validate_batch)
    else:
        result = summary(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
