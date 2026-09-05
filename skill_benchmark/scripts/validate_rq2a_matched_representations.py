#!/usr/bin/env python3
"""Validate RQ2a matched-content artifacts against source and protocol gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROTOCOL_VERSION = "rq2a-matched-content-v1.0"
SERIALISER_VERSION = "rq2a-serialiser-v1.4"
SPLIT_SEED = "rq2a-v1-2026-07-26"

FIELD_ORDER = [
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "dependency_resource",
    "boundary_not_for",
    "success_verification",
]

FIELD_LABELS = {
    "use_condition": "Use Condition",
    "input_precondition": "Input / Precondition",
    "output_artifact": "Output Artifact",
    "workflow_procedure": "Workflow / Procedure",
    "dependency_resource": "Dependency / Resource",
    "boundary_not_for": "Boundary / Not For",
    "success_verification": "Success / Verification",
}

SHARED_KEYS = {
    "use_condition": "shared_use_condition",
    "input_precondition": "shared_input_precondition",
    "output_artifact": "shared_output_artifact",
    "workflow_procedure": "shared_workflow_steps",
    "dependency_resource": "shared_dependencies",
    "boundary_not_for": "shared_boundaries",
    "success_verification": "shared_success_criteria",
}

REPRESENTATIONS = [
    "shared-only",
    "same-facts-fielded",
    "same-facts-flat",
    "same-facts-prose",
    "same-facts-order-controlled",
    "same-facts-diluted-1x",
    "same-facts-diluted-2x",
    "same-facts-diluted-4x",
]

PADDING_BLOCKS = {
    "P1": "Carry out the assigned work carefully and consistently.",
    "P2": "Keep an orderly account of progress during completion.",
    "P3": "Check the finished material before delivery.",
    "P4": "State any remaining caveats clearly for the recipient.",
}

PADDING_BY_REPRESENTATION = {
    "same-facts-diluted-1x": ["P1"],
    "same-facts-diluted-2x": ["P1", "P2"],
    "same-facts-diluted-4x": ["P1", "P2", "P3", "P4"],
}

AUDIT_TOKEN_RE = re.compile(r"\w+|[^\w\s]", flags=re.UNICODE)
WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks: list[dict[str, Any]] = []

    def check(self, condition: bool, name: str, detail: str) -> None:
        self.checks.append(
            {
                "name": name,
                "passed": bool(condition),
                "detail": detail,
            }
        )
        if not condition:
            self.errors.append(f"{name}: {detail}")

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


def skill_benchmark_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
    return rows


def normalise_items(value: Any, context: str) -> list[str]:
    if isinstance(value, str):
        items = [value.strip()]
    elif isinstance(value, list):
        items = [str(item).strip() for item in value]
    else:
        raise TypeError(f"{context}: expected string/list, got {type(value).__name__}")
    if not items or any(not item for item in items):
        raise ValueError(f"{context}: empty proposition")
    return items


def expected_fields(unit: dict[str, Any], skill: dict[str, Any]) -> dict[str, list[str]]:
    target = unit["field"]
    fields: dict[str, list[str]] = {}
    for field in FIELD_ORDER:
        value = skill[field] if field == target else unit[SHARED_KEYS[field]]
        fields[field] = normalise_items(
            value,
            f"{unit['cluster_id']}/{skill['skill_id']}/{field}",
        )
    return fields


def split_digest(field: str, cluster_id: str) -> str:
    return sha256_text(f"{SPLIT_SEED}\n{field}\n{cluster_id}")


def rotate(items: list[str], amount: int) -> list[str]:
    amount %= len(items)
    return items[amount:] + items[:amount]


def normalise_whitespace(text: str) -> str:
    return " ".join(text.split())


def phrase_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.casefold())


def contains_phrase(text: str, phrase: str) -> bool:
    haystack = phrase_tokens(text)
    needle = phrase_tokens(phrase)
    if not needle:
        return False
    width = len(needle)
    return any(haystack[index : index + width] == needle for index in range(len(haystack) - width + 1))


def text_counts(text: str) -> dict[str, int]:
    return {
        "character_count": len(text),
        "utf8_byte_count": len(text.encode("utf-8")),
        "word_count": len(WORD_RE.findall(text)),
        "audit_token_count": len(AUDIT_TOKEN_RE.findall(text)),
    }


def source_units(root: Path) -> dict[str, dict[str, Any]]:
    units: dict[str, dict[str, Any]] = {}
    for field in FIELD_ORDER:
        paths = sorted((root / "rq1a_field_discriminability" / field / "clusters").glob("*/unit.json"))
        if len(paths) != 50:
            raise ValueError(f"{field}: expected 50 source units, found {len(paths)}")
        for path in paths:
            unit = json.loads(path.read_text(encoding="utf-8"))
            cluster_id = unit["cluster_id"]
            if cluster_id in units:
                raise ValueError(f"Duplicate source cluster: {cluster_id}")
            unit["_source_path"] = path.relative_to(root).as_posix()
            unit["_source_sha256"] = file_sha256(path)
            units[cluster_id] = unit
    return units


def expected_split_and_rotations(
    units: dict[str, dict[str, Any]],
) -> tuple[dict[str, str], dict[str, int]]:
    split: dict[str, str] = {}
    rotations: dict[str, int] = {}
    by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for unit in units.values():
        by_field[unit["field"]].append(unit)
    for field_index, field in enumerate(FIELD_ORDER):
        ordered = sorted(
            by_field[field],
            key=lambda unit: (split_digest(field, unit["cluster_id"]), unit["cluster_id"]),
        )
        for rank, unit in enumerate(ordered):
            cluster_id = unit["cluster_id"]
            split[cluster_id] = "development" if rank < 10 else "confirmatory"
            rotations[cluster_id] = (rank + field_index) % len(FIELD_ORDER)
    return split, rotations


def validate_protocol(
    validation: Validation,
    protocol: dict[str, Any],
) -> None:
    validation.check(
        protocol.get("protocol_version") == PROTOCOL_VERSION,
        "protocol-version",
        f"expected {PROTOCOL_VERSION}, found {protocol.get('protocol_version')}",
    )
    validation.check(
        protocol.get("serialiser_version") == SERIALISER_VERSION,
        "serialiser-version",
        f"expected {SERIALISER_VERSION}, found {protocol.get('serialiser_version')}",
    )
    validation.check(
        protocol.get("scope") == "rq2a_only",
        "rq2a-only-scope",
        f"scope={protocol.get('scope')}",
    )
    validation.check(
        protocol.get("thesis_write_blocked_pending_user_review") is True,
        "thesis-write-boundary",
        "protocol must block thesis writes pending user review",
    )


def validate_split(
    validation: Validation,
    split_payload: dict[str, Any],
    units: dict[str, dict[str, Any]],
    expected_split: dict[str, str],
    expected_rotations: dict[str, int],
) -> None:
    rows = split_payload.get("clusters", [])
    validation.check(
        len(rows) == 350,
        "split-row-count",
        f"expected 350, found {len(rows)}",
    )
    ids = [row.get("cluster_id") for row in rows]
    validation.check(
        len(ids) == len(set(ids)) == 350,
        "split-identity-uniqueness",
        f"rows={len(ids)}, unique={len(set(ids))}",
    )
    for row in rows:
        cluster_id = row["cluster_id"]
        unit = units.get(cluster_id)
        if unit is None:
            validation.error(f"split-unknown-cluster: {cluster_id}")
            continue
        expected_digest = split_digest(unit["field"], cluster_id)
        if row.get("split_digest") != expected_digest:
            validation.error(f"split-digest-mismatch: {cluster_id}")
        if row.get("split") != expected_split[cluster_id]:
            validation.error(f"split-assignment-mismatch: {cluster_id}")
        if row.get("order_rotation") != expected_rotations[cluster_id]:
            validation.error(f"order-rotation-mismatch: {cluster_id}")
        if row.get("source_unit_sha256") != unit["_source_sha256"]:
            validation.error(f"split-source-hash-mismatch: {cluster_id}")
    counts = Counter(row.get("split") for row in rows)
    validation.check(
        counts == {"development": 70, "confirmatory": 280},
        "split-counts",
        f"counts={dict(counts)}",
    )
    rotation_counts = Counter(row.get("order_rotation") for row in rows)
    validation.check(
        rotation_counts == {rotation: 50 for rotation in range(7)},
        "order-counterbalance",
        f"rotation_counts={dict(rotation_counts)}",
    )


def validate_prompts(
    validation: Validation,
    prompt_rows: list[dict[str, Any]],
    units: dict[str, dict[str, Any]],
    expected_split: dict[str, str],
) -> None:
    validation.check(
        len(prompt_rows) == 750,
        "prompt-row-count",
        f"expected 750, found {len(prompt_rows)}",
    )
    prompt_ids = [row.get("prompt_id") for row in prompt_rows]
    validation.check(
        len(prompt_ids) == len(set(prompt_ids)) == 750,
        "prompt-identity-uniqueness",
        f"rows={len(prompt_ids)}, unique={len(set(prompt_ids))}",
    )
    for row in prompt_rows:
        cluster_id = row["cluster_id"]
        unit = units.get(cluster_id)
        if unit is None:
            validation.error(f"prompt-unknown-cluster: {row['prompt_id']} -> {cluster_id}")
            continue
        expected_candidates = [skill["skill_id"] for skill in unit["skills"]]
        if row.get("candidate_skill_ids") != expected_candidates:
            validation.error(f"prompt-candidate-order-mismatch: {row['prompt_id']}")
        if row.get("gold_skill_id") != unit["gold_skill_id"]:
            validation.error(f"prompt-gold-mismatch: {row['prompt_id']}")
        if row.get("split") != expected_split[cluster_id]:
            validation.error(f"prompt-split-mismatch: {row['prompt_id']}")
        if row.get("source_unit_sha256") != unit["_source_sha256"]:
            validation.error(f"prompt-source-hash-mismatch: {row['prompt_id']}")
        if row.get("query_text", "").strip() == "":
            validation.error(f"prompt-empty-query: {row['prompt_id']}")
        for key, value in text_counts(row["query_text"]).items():
            if row.get(key) != value:
                validation.error(f"prompt-{key}-mismatch: {row['prompt_id']}")
    counts = Counter(row.get("split") for row in prompt_rows)
    validation.check(
        counts == {"development": 150, "confirmatory": 600},
        "prompt-split-counts",
        f"counts={dict(counts)}",
    )


def validate_manifest_files(
    validation: Validation,
    root: Path,
    output_root: Path,
    manifest: dict[str, Any],
) -> None:
    representation_records = {
        row["representation"]: row for row in manifest.get("representations", [])
    }
    validation.check(
        set(representation_records) == set(REPRESENTATIONS),
        "manifest-representation-set",
        f"found={sorted(representation_records)}",
    )
    for representation, record in representation_records.items():
        path = root / record["path"]
        validation.check(
            path.exists(),
            f"manifest-file-exists-{representation}",
            str(path),
        )
        if path.exists():
            validation.check(
                file_sha256(path) == record.get("sha256"),
                f"manifest-file-hash-{representation}",
                f"path={path}",
            )
    prompt_record = manifest.get("prompt_artifact", {})
    prompt_path = root / prompt_record.get("path", "")
    validation.check(
        prompt_path.exists(),
        "manifest-prompt-file-exists",
        str(prompt_path),
    )
    if prompt_path.exists():
        validation.check(
            file_sha256(prompt_path) == prompt_record.get("sha256"),
            "manifest-prompt-file-hash",
            str(prompt_path),
        )
    split_path = output_root / "split.json"
    validation.check(
        file_sha256(split_path) == manifest.get("split", {}).get("split_json_sha256"),
        "manifest-split-file-hash",
        str(split_path),
    )


def validate_representation_rows(
    validation: Validation,
    rows_by_representation: dict[str, list[dict[str, Any]]],
    units: dict[str, dict[str, Any]],
    expected_split: dict[str, str],
    expected_rotations: dict[str, int],
) -> dict[str, Any]:
    expected_keys = {
        (cluster_id, skill["skill_id"])
        for cluster_id, unit in units.items()
        for skill in unit["skills"]
    }
    row_lookup: dict[tuple[str, str, str], dict[str, Any]] = {}

    for representation, rows in rows_by_representation.items():
        keys = [(row["cluster_id"], row["skill_id"]) for row in rows]
        validation.check(
            len(rows) == 1050,
            f"row-count-{representation}",
            f"expected 1050, found {len(rows)}",
        )
        validation.check(
            len(keys) == len(set(keys)) == 1050 and set(keys) == expected_keys,
            f"identity-alignment-{representation}",
            f"rows={len(keys)}, unique={len(set(keys))}, expected={len(expected_keys)}",
        )
        for row in rows:
            cluster_id = row["cluster_id"]
            skill_id = row["skill_id"]
            row_lookup[(representation, cluster_id, skill_id)] = row
            unit = units.get(cluster_id)
            if unit is None:
                validation.error(f"{representation}: unknown cluster {cluster_id}")
                continue
            skill = next(
                (item for item in unit["skills"] if item["skill_id"] == skill_id),
                None,
            )
            if skill is None:
                validation.error(f"{representation}: unknown skill {cluster_id}/{skill_id}")
                continue
            expected = expected_fields(unit, skill)
            if row.get("canonical_fields") != expected:
                validation.error(f"{representation}: canonical fields mismatch {cluster_id}/{skill_id}")
            if row.get("all_propositions_sha256") != sha256_json(expected):
                validation.error(f"{representation}: proposition hash mismatch {cluster_id}/{skill_id}")
            expected_field_hashes = {
                field: sha256_json(expected[field]) for field in FIELD_ORDER
            }
            if row.get("field_proposition_sha256") != expected_field_hashes:
                validation.error(f"{representation}: field hash mismatch {cluster_id}/{skill_id}")
            if row.get("source_unit_sha256") != unit["_source_sha256"]:
                validation.error(f"{representation}: source hash mismatch {cluster_id}/{skill_id}")
            if row.get("split") != expected_split[cluster_id]:
                validation.error(f"{representation}: split mismatch {cluster_id}/{skill_id}")
            text = row.get("selector_visible_text", "")
            if not text:
                validation.error(f"{representation}: empty text {cluster_id}/{skill_id}")
                continue
            if row.get("selector_visible_text_sha256") != sha256_text(text):
                validation.error(f"{representation}: text hash mismatch {cluster_id}/{skill_id}")
            for key, value in text_counts(text).items():
                if row.get(key) != value:
                    validation.error(f"{representation}: {key} mismatch {cluster_id}/{skill_id}")

            forbidden_exact = [
                skill_id,
                str(skill.get("display_name", "")),
                cluster_id,
            ]
            if any(value and value.casefold() in text.casefold() for value in forbidden_exact):
                validation.error(f"{representation}: identity leakage {cluster_id}/{skill_id}")
            punctuated_metadata_markers = [
                "role:",
                "target field:",
                "field suite:",
                "cluster id:",
            ]
            phrase_metadata_markers = [
                "gold skill",
                "option a",
                "option b",
                "option c",
            ]
            if any(
                marker in text.casefold() for marker in punctuated_metadata_markers
            ) or any(
                contains_phrase(text, marker) for marker in phrase_metadata_markers
            ):
                validation.error(f"{representation}: metadata marker leakage {cluster_id}/{skill_id}")

            if representation == "same-facts-order-controlled":
                expected_order = rotate(FIELD_ORDER, expected_rotations[cluster_id])
                if row.get("field_order") != expected_order:
                    validation.error(f"order-controlled schedule mismatch {cluster_id}/{skill_id}")
                if row.get("order_rotation") != expected_rotations[cluster_id]:
                    validation.error(f"order-controlled rotation mismatch {cluster_id}/{skill_id}")
            elif representation == "shared-only":
                if row.get("field_order") != []:
                    validation.error(f"shared-only field_order must be empty {cluster_id}/{skill_id}")
            elif row.get("field_order") != FIELD_ORDER:
                validation.error(f"{representation}: canonical order mismatch {cluster_id}/{skill_id}")

            if representation == "same-facts-flat":
                lines = {line.strip().casefold() for line in text.splitlines()}
                leaked_labels = [
                    label for label in FIELD_LABELS.values() if label.casefold() in lines
                ]
                if leaked_labels:
                    validation.error(
                        f"flat field labels present {cluster_id}/{skill_id}: {leaked_labels}"
                    )

            if representation == "same-facts-prose":
                normalised_text = normalise_whitespace(text)
                if ".." in text or ".;" in text:
                    validation.error(
                        f"prose punctuation artifact {cluster_id}/{skill_id}"
                    )
                for field in FIELD_ORDER:
                    for proposition in expected[field]:
                        if normalise_whitespace(proposition) not in normalised_text:
                            validation.error(
                                f"prose missing proposition {cluster_id}/{skill_id}/{field}: "
                                f"{proposition[:80]}"
                            )

    same_fact_representations = [
        representation
        for representation in REPRESENTATIONS
        if representation != "shared-only"
    ]
    for cluster_id, skill_id in sorted(expected_keys):
        hashes = {
            row_lookup[(representation, cluster_id, skill_id)]["all_propositions_sha256"]
            for representation in same_fact_representations
        }
        if len(hashes) != 1:
            validation.error(f"cross-representation proposition mismatch {cluster_id}/{skill_id}")

    for cluster_id, unit in units.items():
        shared_texts = {
            row_lookup[("shared-only", cluster_id, skill["skill_id"])]["selector_visible_text"]
            for skill in unit["skills"]
        }
        if len(shared_texts) != 1:
            validation.error(f"shared-only siblings differ: {cluster_id}")

        fielded_by_skill = {
            skill["skill_id"]: row_lookup[
                ("same-facts-fielded", cluster_id, skill["skill_id"])
            ]["selector_visible_text"]
            for skill in unit["skills"]
        }
        leakage_terms = [str(term) for term in unit.get("leakage_terms", [])]
        target_values = [
            proposition
            for skill in unit["skills"]
            for proposition in normalise_items(
                skill[unit["field"]],
                f"{cluster_id}/{skill['skill_id']}/{unit['field']}",
            )
        ]
        for representation, padding_ids in PADDING_BY_REPRESENTATION.items():
            suffixes: set[str] = set()
            for skill in unit["skills"]:
                skill_id = skill["skill_id"]
                text = row_lookup[(representation, cluster_id, skill_id)]["selector_visible_text"]
                fielded = fielded_by_skill[skill_id]
                expected_suffix = "\n\nSupport Notes\n" + "\n".join(
                    f"- {PADDING_BLOCKS[padding_id]}" for padding_id in padding_ids
                )
                if text != fielded + expected_suffix:
                    validation.error(f"{representation}: prefix/suffix mismatch {cluster_id}/{skill_id}")
                suffixes.add(text[len(fielded) :])
            if len(suffixes) != 1:
                validation.error(f"{representation}: sibling padding differs {cluster_id}")
            padding_text = next(iter(suffixes), "")
            for phrase in [*leakage_terms, *target_values]:
                if contains_phrase(padding_text, phrase):
                    validation.error(
                        f"{representation}: padding leakage {cluster_id}: {phrase!r}"
                    )

    length_report: dict[str, Any] = {}
    for representation, rows in rows_by_representation.items():
        values = [row["audit_token_count"] for row in rows]
        length_report[representation] = {
            "min": min(values),
            "median": statistics.median(values),
            "mean": statistics.mean(values),
            "max": max(values),
        }
    fielded_median = length_report["same-facts-fielded"]["median"]
    length_sensitivity: dict[str, Any] = {}
    for comparison in ("same-facts-flat", "same-facts-prose"):
        comparison_median = length_report[comparison]["median"]
        relative_difference = abs(comparison_median - fielded_median) / fielded_median
        length_sensitivity[comparison] = {
            "fielded_median": fielded_median,
            "comparison_median": comparison_median,
            "relative_difference": relative_difference,
            "sensitivity_required": relative_difference > 0.10,
        }
        if relative_difference > 0.10:
            validation.warning(
                f"length-sensitivity-required: fielded vs {comparison} median differs "
                f"by {relative_difference:.1%}"
            )
    return {
        "length_summary_audit_tokens": length_report,
        "length_sensitivity": length_sensitivity,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# RQ2a Matched-Content Representation Validation",
        "",
        f"- Protocol: `{report['protocol_version']}`",
        f"- Status: **{report['status']}**",
        f"- Errors: {len(report['errors'])}",
        f"- Warnings: {len(report['warnings'])}",
        "",
        "## Gate Summary",
        "",
        "| Check | Passed | Detail |",
        "|---|---:|---|",
    ]
    for check in report["checks"]:
        detail = str(check["detail"]).replace("|", "\\|")
        lines.append(f"| `{check['name']}` | {'yes' if check['passed'] else 'no'} | {detail} |")

    lines.extend(["", "## Length Audit", ""])
    lines.extend(
        [
            "| Representation | Min | Median | Mean | Max |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for representation, summary in report["length"]["length_summary_audit_tokens"].items():
        lines.append(
            f"| `{representation}` | {summary['min']} | {summary['median']:.1f} | "
            f"{summary['mean']:.1f} | {summary['max']} |"
        )

    lines.extend(["", "## Length Sensitivity Triggers", ""])
    for comparison, item in report["length"]["length_sensitivity"].items():
        lines.append(
            f"- `same-facts-fielded` versus `{comparison}`: "
            f"{item['relative_difference']:.1%}; "
            f"sensitivity required = `{str(item['sensitivity_required']).lower()}`."
        )

    lines.extend(["", "## Errors", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"][:200])
        if len(report["errors"]) > 200:
            lines.append(f"- ... {len(report['errors']) - 200} additional errors in JSON report.")
    else:
        lines.append("- None.")

    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- A structural pass establishes identity, proposition, hash, order, padding, and leakage integrity.",
            "- A length-sensitivity warning is not a structural failure, but the required sensitivity must be built before confirmatory scoring.",
            "- This validator does not establish selector accuracy; it only protects the causal representation comparison.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    root = skill_benchmark_root()
    parser = argparse.ArgumentParser(description="Validate RQ2a matched-content artifacts.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=root / "rq2a_matched_content",
    )
    args = parser.parse_args()

    output_root = args.output_root.resolve()
    validation = Validation()

    protocol = json.loads((output_root / "protocol.json").read_text(encoding="utf-8"))
    split_payload = json.loads((output_root / "split.json").read_text(encoding="utf-8"))
    manifest = json.loads((output_root / "manifest.json").read_text(encoding="utf-8"))
    prompt_rows = read_jsonl(output_root / "prompts.jsonl")
    rows_by_representation = {
        representation: read_jsonl(
            output_root / "representations" / f"{representation}.jsonl"
        )
        for representation in REPRESENTATIONS
    }

    units = source_units(root)
    expected_split, expected_rotations = expected_split_and_rotations(units)

    validate_protocol(validation, protocol)
    validate_split(
        validation,
        split_payload,
        units,
        expected_split,
        expected_rotations,
    )
    validate_prompts(validation, prompt_rows, units, expected_split)
    validate_manifest_files(validation, root, output_root, manifest)
    length = validate_representation_rows(
        validation,
        rows_by_representation,
        units,
        expected_split,
        expected_rotations,
    )

    status = "PASS_WITH_REQUIRED_LENGTH_SENSITIVITY"
    if validation.errors:
        status = "FAIL"
    elif not any(
        item["sensitivity_required"]
        for item in length["length_sensitivity"].values()
    ):
        status = "PASS"

    report = {
        "schema_version": "rq2a-representation-validation-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "status": status,
        "checks": validation.checks,
        "errors": validation.errors,
        "warnings": validation.warnings,
        "length": length,
    }
    json_path = output_root / "validation_report.json"
    md_path = output_root / "validation_report.md"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")

    print(f"Status: {status}")
    print(f"Errors: {len(validation.errors)}")
    print(f"Warnings: {len(validation.warnings)}")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    if validation.errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
