#!/usr/bin/env python3
"""Build and validate opaque local B0G batched-review packets.

This controller never calls a provider or scores a selector. It separates the
metadata-only plan from the ignored local packet cache that contains raw prompt
and source text for the explicitly authorised blinded semantic review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


VERSION_ID = "rq2b-full-library-v1-2026-08-02"
SEED = "2026080901"
MAX_UNITS_PER_BATCH = 48
MAX_CHARS_PER_BATCH = 250_000
ROLES = ("A", "B")
LABELS = {"fully_acceptable", "partially_suitable", "not_suitable", "uncertain"}
PLAN_FIELDS = {
    "assignment_token",
    "unit_token",
    "reviewer_role",
    "batch_id",
    "batch_ordinal",
    "prompt_sha256",
    "candidate_source_sha256",
    "prompt_chars",
    "source_chars",
    "combined_chars",
}
PLAN_MANIFEST_FIELDS = {
    "schema_version",
    "state",
    "seed",
    "units",
    "initial_assignments",
    "maximum_total_decisions",
    "roles",
    "max_units_per_batch",
    "max_chars_per_batch",
    "batch_counts",
    "plan_path",
    "plan_sha256",
    "input_sha256",
    "network_calls",
    "provider_calls",
    "semantic_decisions",
    "raw_text_in_plan",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def version_root(root: Path) -> Path:
    return root / "skill_benchmark" / "rq2b_full_library" / VERSION_ID


def review_root(root: Path) -> Path:
    return version_root(root) / "b0g_semantic_review_v2_2026-08-09"


def cache_root(root: Path) -> Path:
    return root / "skill_benchmark" / "cache" / "rq2b_b0g_semantic_review_v2" / VERSION_ID


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"Missing JSONL input: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        require(isinstance(row, dict), f"Non-object row in {path}:{line_number}")
        rows.append(row)
    return rows


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


def opaque_token(prefix: str, *parts: str) -> str:
    digest = sha256_text("|".join((SEED, prefix, *parts)))[:24]
    return f"{prefix}_{digest}"


def input_paths(root: Path) -> dict[str, Path]:
    frozen = version_root(root)
    return {
        "candidate_pool": frozen / "b0g_cd_2026-08-09" / "candidate_pool.jsonl",
        "source_manifest": frozen / "source_manifest.jsonl",
        "prompt_manifest": frozen / "prompt_manifest.jsonl",
    }


def build_units(root: Path) -> list[dict[str, Any]]:
    paths = input_paths(root)
    candidates = read_jsonl(paths["candidate_pool"])
    sources = {row["skill_id"]: row for row in read_jsonl(paths["source_manifest"])}
    prompts = {row["prompt_id"]: row for row in read_jsonl(paths["prompt_manifest"])}
    units: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in candidates:
        require(set(candidate) == {
            "candidate_skill_id",
            "candidate_source_sha256",
            "channels",
            "prompt_id",
            "prompt_sha256",
        }, "Candidate-pool schema mismatch")
        prompt = prompts.get(candidate["prompt_id"])
        source = sources.get(candidate["candidate_skill_id"])
        require(prompt is not None, "Candidate references missing prompt")
        require(source is not None, "Candidate references missing source")
        require(candidate["prompt_sha256"] == prompt["prompt_sha256"], "Prompt hash mismatch")
        require(candidate["candidate_source_sha256"] == source["source_sha256"], "Source hash mismatch")
        unit_token = opaque_token("unit", candidate["prompt_id"], candidate["candidate_skill_id"])
        require(unit_token not in seen, "Opaque-token collision")
        seen.add(unit_token)
        units.append(
            {
                "unit_token": unit_token,
                "prompt_sha256": prompt["prompt_sha256"],
                "candidate_source_sha256": source["source_sha256"],
                "prompt_chars": prompt["prompt_chars"],
                "source_chars": source["source_chars"],
                "combined_chars": prompt["prompt_chars"] + source["source_chars"],
                "_prompt_id": candidate["prompt_id"],
                "_skill_id": candidate["candidate_skill_id"],
            }
        )
    require(len(units) == 7_710, f"Expected 7,710 units, got {len(units)}")
    return units


def deterministic_order(units: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
    return sorted(
        units,
        key=lambda row: sha256_text(f"{SEED}|{role}|{row['unit_token']}"),
    )


def plan_batches(units: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
    batches: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    batch_index = 0
    for unit in deterministic_order(units, role):
        over_count = len(current) >= MAX_UNITS_PER_BATCH
        over_chars = current and current_chars + unit["combined_chars"] > MAX_CHARS_PER_BATCH
        if over_count or over_chars:
            batches.append(
                {
                    "batch_id": f"{role}-{batch_index:04d}",
                    "role": role,
                    "units": current,
                    "combined_chars": current_chars,
                }
            )
            batch_index += 1
            current = []
            current_chars = 0
        current.append(unit)
        current_chars += unit["combined_chars"]
    if current:
        batches.append(
            {
                "batch_id": f"{role}-{batch_index:04d}",
                "role": role,
                "units": current,
                "combined_chars": current_chars,
            }
        )
    return batches


def build_plan(root: Path) -> dict[str, Any]:
    review = review_root(root)
    plan_path = review / "review_plan.jsonl"
    manifest_path = review / "review_plan_manifest.json"
    require(not plan_path.exists() and not manifest_path.exists(), "Review plan already exists")
    units = build_units(root)
    plan_rows: list[dict[str, Any]] = []
    batch_counts: dict[str, int] = {}
    for role in ROLES:
        batches = plan_batches(units, role)
        batch_counts[role] = len(batches)
        for batch in batches:
            for ordinal, unit in enumerate(batch["units"], start=1):
                plan_rows.append(
                    {
                        "assignment_token": opaque_token("review", unit["unit_token"], role),
                        "unit_token": unit["unit_token"],
                        "reviewer_role": role,
                        "batch_id": batch["batch_id"],
                        "batch_ordinal": ordinal,
                        "prompt_sha256": unit["prompt_sha256"],
                        "candidate_source_sha256": unit["candidate_source_sha256"],
                        "prompt_chars": unit["prompt_chars"],
                        "source_chars": unit["source_chars"],
                        "combined_chars": unit["combined_chars"],
                    }
                )
    require(len(plan_rows) == 15_420, "Initial assignment count mismatch")
    require(len({row["assignment_token"] for row in plan_rows}) == len(plan_rows), "Assignment-token collision")
    write_jsonl_new(plan_path, sorted(plan_rows, key=lambda row: row["assignment_token"]))
    manifest = {
        "schema_version": "rq2b-b0g-batched-review-plan-v1",
        "state": "planned_no_raw_packets_or_decisions",
        "seed": SEED,
        "units": len(units),
        "initial_assignments": len(plan_rows),
        "maximum_total_decisions": len(plan_rows) + len(units),
        "roles": list(ROLES),
        "max_units_per_batch": MAX_UNITS_PER_BATCH,
        "max_chars_per_batch": MAX_CHARS_PER_BATCH,
        "batch_counts": batch_counts,
        "plan_path": str(plan_path.relative_to(root)),
        "plan_sha256": sha256_file(plan_path),
        "input_sha256": {name: sha256_file(path) for name, path in input_paths(root).items()},
        "network_calls": 0,
        "provider_calls": 0,
        "semantic_decisions": 0,
        "raw_text_in_plan": False,
    }
    write_json_new(manifest_path, manifest)
    return manifest


def load_plan(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    review = review_root(root)
    plan_path = review / "review_plan.jsonl"
    manifest_path = review / "review_plan_manifest.json"
    plan = read_jsonl(plan_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(set(manifest) == PLAN_MANIFEST_FIELDS, "Review-plan manifest schema mismatch")
    require(manifest["schema_version"] == "rq2b-b0g-batched-review-plan-v1", "Review-plan manifest version mismatch")
    require(manifest["state"] == "planned_no_raw_packets_or_decisions", "Unexpected plan state")
    require(manifest["seed"] == SEED, "Review-plan seed mismatch")
    require(manifest["roles"] == list(ROLES), "Review-plan role list mismatch")
    require(manifest["max_units_per_batch"] == MAX_UNITS_PER_BATCH, "Review-plan unit cap mismatch")
    require(manifest["max_chars_per_batch"] == MAX_CHARS_PER_BATCH, "Review-plan character cap mismatch")
    require(manifest["raw_text_in_plan"] is False, "Review plan records raw text")
    require(
        manifest["network_calls"] == manifest["provider_calls"] == manifest["semantic_decisions"] == 0,
        "Review plan records execution activity",
    )
    require(
        manifest["plan_path"] == str(plan_path.relative_to(root)),
        "Review-plan path binding mismatch",
    )
    require(
        manifest["input_sha256"] == {name: sha256_file(path) for name, path in input_paths(root).items()},
        "Review-plan input binding drift",
    )
    require(manifest["plan_sha256"] == sha256_file(plan_path), "Review-plan hash drift")
    require(len(plan) == 15_420, "Review-plan row count mismatch")
    require(manifest["units"] == 7_710, "Review-plan unit count mismatch")
    require(manifest["initial_assignments"] == len(plan), "Review-plan assignment count mismatch")
    require(manifest["maximum_total_decisions"] == len(plan) + manifest["units"], "Review-plan total-decision cap mismatch")
    require(all(set(row) == PLAN_FIELDS for row in plan), "Review-plan row schema mismatch")
    assignments: set[str] = set()
    unit_roles: set[tuple[str, str]] = set()
    units: Counter[str] = Counter()
    batches: dict[str, list[dict[str, Any]]] = {}
    for row in plan:
        require(
            isinstance(row["assignment_token"], str) and row["assignment_token"].startswith("review_"),
            "Review-plan assignment token is invalid",
        )
        require(isinstance(row["unit_token"], str) and row["unit_token"].startswith("unit_"), "Review-plan unit token is invalid")
        require(row["reviewer_role"] in ROLES, "Review-plan role is invalid")
        require(
            isinstance(row["batch_id"], str) and row["batch_id"].startswith(f"{row['reviewer_role']}-"),
            "Review-plan batch role mismatch",
        )
        require(
            isinstance(row["batch_ordinal"], int) and 1 <= row["batch_ordinal"] <= MAX_UNITS_PER_BATCH,
            "Review-plan batch ordinal is invalid",
        )
        require(
            all(
                isinstance(row[key], str) and len(row[key]) == 64
                for key in ("prompt_sha256", "candidate_source_sha256")
            ),
            "Review-plan hash field is invalid",
        )
        require(
            all(isinstance(row[key], int) and row[key] >= 0 for key in ("prompt_chars", "source_chars", "combined_chars")),
            "Review-plan character field is invalid",
        )
        require(row["combined_chars"] == row["prompt_chars"] + row["source_chars"], "Review-plan character sum mismatch")
        require(row["assignment_token"] not in assignments, "Duplicate review assignment")
        assignments.add(row["assignment_token"])
        key = (row["unit_token"], row["reviewer_role"])
        require(key not in unit_roles, "Duplicate unit-role assignment")
        unit_roles.add(key)
        units[row["unit_token"]] += 1
        batches.setdefault(row["batch_id"], []).append(row)
    require(len(units) == manifest["units"] and all(count == 2 for count in units.values()), "Review-plan A/B coverage mismatch")
    batch_counts = Counter(batch_id.split("-", 1)[0] for batch_id in batches)
    require(dict(sorted(batch_counts.items())) == manifest["batch_counts"], "Review-plan batch-count mismatch")
    for batch_id, rows in batches.items():
        require(len(rows) <= MAX_UNITS_PER_BATCH, "Review-plan batch exceeds unit cap")
        require({row["batch_ordinal"] for row in rows} == set(range(1, len(rows) + 1)), "Review-plan batch ordinals are not contiguous")
        chars = sum(row["combined_chars"] for row in rows)
        require(len(rows) == 1 or chars <= MAX_CHARS_PER_BATCH, f"Review-plan batch exceeds character cap: {batch_id}")
    return plan, manifest


def unit_lookup(root: Path) -> dict[str, dict[str, Any]]:
    return {row["unit_token"]: row for row in build_units(root)}


def expected_packet_rows(root: Path, assignments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Reconstruct the only permitted packet rows from frozen prompt/source bytes."""
    units = unit_lookup(root)
    paths = input_paths(root)
    sources = {row["skill_id"]: row for row in read_jsonl(paths["source_manifest"])}
    prompts = {row["prompt_id"]: row for row in read_jsonl(paths["prompt_manifest"])}
    packet_rows: list[dict[str, Any]] = []
    for assignment in sorted(assignments, key=lambda row: row["batch_ordinal"]):
        unit = units[assignment["unit_token"]]
        prompt = prompts[unit["_prompt_id"]]
        source = sources[unit["_skill_id"]]
        source_bytes = (root / source["source_path"]).read_bytes()
        require(hashlib.sha256(source_bytes).hexdigest() == source["source_sha256"], "Source byte hash drift")
        require(sha256_text(prompt["prompt"]) == prompt["prompt_sha256"], "Prompt hash drift")
        packet_rows.append(
            {
                "review_token": assignment["assignment_token"],
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
    plan, manifest = load_plan(root)
    assignments = [row for row in plan if row["batch_id"] == batch_id]
    require(assignments, f"Unknown batch: {batch_id}")
    require(len(assignments) <= MAX_UNITS_PER_BATCH, "Batch exceeds unit limit")
    packet_rows = expected_packet_rows(root, assignments)
    packet_chars = sum(len(row["user_request"]) + len(row["candidate_skill_document"]) for row in packet_rows)
    require(
        len(packet_rows) == 1 or packet_chars <= MAX_CHARS_PER_BATCH,
        "Batch exceeds character limit without single-unit exception",
    )
    cache = cache_root(root) / "packets"
    packet_path = cache / f"{batch_id}.jsonl"
    write_jsonl_new(packet_path, packet_rows)
    return {
        "batch_id": batch_id,
        "packet_path": str(packet_path),
        "packet_sha256": sha256_file(packet_path),
        "assignments": len(packet_rows),
        "packet_chars": packet_chars,
        "plan_sha256": manifest["plan_sha256"],
        "network_calls": 0,
    }


def validate_batch(root: Path, batch_id: str) -> dict[str, Any]:
    plan, manifest = load_plan(root)
    assignments = [row for row in plan if row["batch_id"] == batch_id]
    require(assignments, f"Unknown batch: {batch_id}")
    packet_path = cache_root(root) / "packets" / f"{batch_id}.jsonl"
    decision_path = cache_root(root) / "decisions" / f"{batch_id}.jsonl"
    packet_rows = read_jsonl(packet_path)
    decisions = read_jsonl(decision_path)
    require(packet_rows == expected_packet_rows(root, assignments), "Packet does not match frozen prompt/source reconstruction")
    expected = {row["assignment_token"] for row in assignments}
    packet_by_token = {row["review_token"]: row for row in packet_rows}
    require(set(packet_by_token) == expected, "Packet token set mismatch")
    require(len(decisions) == len(expected), "Decision count mismatch")
    seen: set[str] = set()
    sanitized: list[dict[str, Any]] = []
    for decision in decisions:
        require(set(decision) == {"review_token", "label", "reason", "source_evidence"}, "Decision schema mismatch")
        token = decision["review_token"]
        require(isinstance(token, str) and token in expected and token not in seen, "Decision token mismatch")
        seen.add(token)
        require(decision["label"] in LABELS, "Invalid decision label")
        require(isinstance(decision["reason"], str) and 1 <= len(decision["reason"].strip()) <= 1_200, "Invalid decision reason")
        evidence = decision["source_evidence"]
        require(isinstance(evidence, list) and len(evidence) <= 3 and all(isinstance(item, str) for item in evidence), "Invalid evidence list")
        source_text = packet_by_token[token]["candidate_skill_document"]
        require(all(item and item in source_text for item in evidence), "Non-substring source evidence")
        sanitized.append(
            {
                "review_token": token,
                "label": decision["label"],
                "decision_sha256": sha256_text(json.dumps(decision, sort_keys=True)),
            }
        )
    require(seen == expected, "Missing decision token")
    output_dir = review_root(root) / "validated_decisions"
    output_path = output_dir / f"{batch_id}.jsonl"
    write_jsonl_new(output_path, sorted(sanitized, key=lambda row: row["review_token"]))
    summary = {
        "batch_id": batch_id,
        "state": "validated_blinded_decisions_no_adjudication",
        "assignments": len(expected),
        "label_counts": dict(sorted(Counter(row["label"] for row in sanitized).items())),
        "packet_sha256": sha256_file(packet_path),
        "decision_sha256": sha256_file(decision_path),
        "validated_decisions_path": str(output_path.relative_to(root)),
        "validated_decisions_sha256": sha256_file(output_path),
        "plan_sha256": manifest["plan_sha256"],
        "network_calls": 0,
        "provider_calls": 0,
    }
    write_json_new(output_dir / f"{batch_id}.validation.json", summary)
    return summary


def summary(root: Path) -> dict[str, Any]:
    plan, manifest = load_plan(root)
    validated_dir = review_root(root) / "validated_decisions"
    validated = sorted(validated_dir.glob("*.validation.json")) if validated_dir.exists() else []
    completed_batches = {json.loads(path.read_text(encoding="utf-8"))["batch_id"] for path in validated}
    all_batches = {row["batch_id"] for row in plan}
    return {
        "schema_version": "rq2b-b0g-batched-review-summary-v1",
        "state": "semantic_review_in_progress" if completed_batches else "planned_no_decisions",
        "plan_sha256": manifest["plan_sha256"],
        "initial_assignments": len(plan),
        "batches_total": len(all_batches),
        "batches_validated": len(completed_batches),
        "assignments_validated": sum(
            json.loads(path.read_text(encoding="utf-8"))["assignments"] for path in validated
        ),
        "batches_pending": len(all_batches - completed_batches),
        "network_calls": 0,
        "provider_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--plan", action="store_true")
    actions.add_argument("--materialise-batch")
    actions.add_argument("--validate-batch")
    actions.add_argument("--summary", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    root = args.root.resolve()
    if args.plan:
        result = build_plan(root)
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
