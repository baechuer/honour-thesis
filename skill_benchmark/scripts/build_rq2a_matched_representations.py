#!/usr/bin/env python3
"""Build deterministic matched-content representations for RQ2a."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


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

FIELD_CONFIG = {
    "use_condition": {
        "label": "Use Condition",
        "shared_key": "shared_use_condition",
    },
    "input_precondition": {
        "label": "Input / Precondition",
        "shared_key": "shared_input_precondition",
    },
    "output_artifact": {
        "label": "Output Artifact",
        "shared_key": "shared_output_artifact",
    },
    "workflow_procedure": {
        "label": "Workflow / Procedure",
        "shared_key": "shared_workflow_steps",
    },
    "dependency_resource": {
        "label": "Dependency / Resource",
        "shared_key": "shared_dependencies",
    },
    "boundary_not_for": {
        "label": "Boundary / Not For",
        "shared_key": "shared_boundaries",
    },
    "success_verification": {
        "label": "Success / Verification",
        "shared_key": "shared_success_criteria",
    },
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


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def normalise_items(value: Any, *, context: str) -> list[str]:
    if isinstance(value, str):
        items = [value.strip()]
    elif isinstance(value, list):
        items = [str(item).strip() for item in value]
    else:
        raise TypeError(f"{context}: expected string or list, received {type(value).__name__}")
    if not items or any(not item for item in items):
        raise ValueError(f"{context}: empty proposition value")
    return items


def split_digest(field: str, cluster_id: str) -> str:
    return sha256_text(f"{SPLIT_SEED}\n{field}\n{cluster_id}")


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


def relative_to_root(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def candidate_fields(unit: dict[str, Any], skill: dict[str, Any]) -> dict[str, list[str]]:
    target_field = str(unit["field"])
    if target_field not in FIELD_CONFIG:
        raise ValueError(f"{unit['cluster_id']}: unsupported target field {target_field}")
    fields: dict[str, list[str]] = {}
    for field in FIELD_ORDER:
        if field == target_field:
            if field not in skill:
                raise KeyError(f"{unit['cluster_id']}/{skill['skill_id']}: missing candidate field {field}")
            value = skill[field]
        else:
            shared_key = FIELD_CONFIG[field]["shared_key"]
            if shared_key not in unit:
                raise KeyError(f"{unit['cluster_id']}: missing non-target source {shared_key}")
            value = unit[shared_key]
        fields[field] = normalise_items(
            value,
            context=f"{unit['cluster_id']}/{skill['skill_id']}/{field}",
        )
    return fields


def format_field_value(field: str, items: list[str]) -> str:
    if len(items) == 1:
        return items[0]
    if field == "workflow_procedure":
        return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))
    return "\n".join(f"- {item}" for item in items)


def render_shared_only(unit: dict[str, Any]) -> str:
    shared_context = str(unit.get("shared_context", "")).strip()
    if not shared_context:
        raise ValueError(f"{unit['cluster_id']}: empty shared_context")
    return f"Skill candidate\n\n{shared_context}"


def render_fielded(
    fields: dict[str, list[str]],
    field_order: list[str] | None = None,
) -> str:
    order = field_order or FIELD_ORDER
    blocks = ["Skill candidate"]
    for field in order:
        blocks.append(
            f"{FIELD_CONFIG[field]['label']}\n{format_field_value(field, fields[field])}"
        )
    return "\n\n".join(blocks)


def render_flat(fields: dict[str, list[str]]) -> str:
    value_blocks = ["\n".join(fields[field]) for field in FIELD_ORDER]
    return "Skill candidate\n\n" + "\n\n---\n\n".join(value_blocks)


def prose_value(items: list[str]) -> str:
    rendered = [
        item if item.endswith((".", "!", "?")) else f"{item}."
        for item in items
    ]
    return " ".join(rendered)


def render_prose(fields: dict[str, list[str]]) -> str:
    text = (
        "This skill is used under these conditions: "
        f"{prose_value(fields['use_condition'])} "
        "Its input or precondition is: "
        f"{prose_value(fields['input_precondition'])} "
        "It produces this output artifact: "
        f"{prose_value(fields['output_artifact'])} "
        "It follows this workflow or procedure: "
        f"{prose_value(fields['workflow_procedure'])} "
        "It depends on these resources or capabilities: "
        f"{prose_value(fields['dependency_resource'])} "
        "It is outside scope under these boundaries: "
        f"{prose_value(fields['boundary_not_for'])} "
        "Success is verified by: "
        f"{prose_value(fields['success_verification'])}"
    )
    return f"Skill candidate\n\n{text}"


def render_diluted(fielded_text: str, padding_ids: list[str]) -> str:
    padding = "\n".join(f"- {PADDING_BLOCKS[padding_id]}" for padding_id in padding_ids)
    return f"{fielded_text}\n\nSupport Notes\n{padding}"


def text_counts(text: str) -> dict[str, int]:
    return {
        "character_count": len(text),
        "utf8_byte_count": len(text.encode("utf-8")),
        "word_count": len(WORD_RE.findall(text)),
        "audit_token_count": len(AUDIT_TOKEN_RE.findall(text)),
    }


def build_order_rotation_map(
    units_by_field: dict[str, list[dict[str, Any]]],
) -> dict[str, int]:
    rotations: dict[str, int] = {}
    for field_index, field in enumerate(FIELD_ORDER):
        ordered = sorted(
            units_by_field[field],
            key=lambda unit: (split_digest(field, unit["cluster_id"]), unit["cluster_id"]),
        )
        for rank, unit in enumerate(ordered):
            rotations[unit["cluster_id"]] = (rank + field_index) % len(FIELD_ORDER)
    return rotations


def rotate(items: list[str], amount: int) -> list[str]:
    amount %= len(items)
    return items[amount:] + items[:amount]


def representation_text(
    representation: str,
    unit: dict[str, Any],
    fields: dict[str, list[str]],
    rotation: int,
) -> tuple[str, list[str], list[str]]:
    if representation == "shared-only":
        return render_shared_only(unit), [], []
    if representation == "same-facts-fielded":
        return render_fielded(fields), FIELD_ORDER.copy(), []
    if representation == "same-facts-flat":
        return render_flat(fields), FIELD_ORDER.copy(), []
    if representation == "same-facts-prose":
        return render_prose(fields), FIELD_ORDER.copy(), []
    if representation == "same-facts-order-controlled":
        order = rotate(FIELD_ORDER, rotation)
        return render_fielded(fields, order), order, []
    if representation in PADDING_BY_REPRESENTATION:
        padding_ids = PADDING_BY_REPRESENTATION[representation]
        return render_diluted(render_fielded(fields), padding_ids), FIELD_ORDER.copy(), padding_ids
    raise ValueError(f"Unsupported representation: {representation}")


def load_sources(
    root: Path,
) -> tuple[
    dict[str, list[dict[str, Any]]],
    list[dict[str, Any]],
    dict[str, str],
]:
    rq1_root = root / "rq1a_field_discriminability"
    units_by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    prompts: list[dict[str, Any]] = []
    prompt_file_hashes: dict[str, str] = {}

    for field in FIELD_ORDER:
        suite_dir = rq1_root / field
        unit_paths = sorted((suite_dir / "clusters").glob("*/unit.json"))
        if len(unit_paths) != 50:
            raise ValueError(f"{field}: expected 50 unit files, found {len(unit_paths)}")
        for unit_path in unit_paths:
            unit = json.loads(unit_path.read_text(encoding="utf-8"))
            if unit.get("field") != field:
                raise ValueError(
                    f"{unit_path}: expected field {field}, found {unit.get('field')}"
                )
            if len(unit.get("skills", [])) != 3:
                raise ValueError(f"{unit_path}: expected exactly three candidate skills")
            unit["_source_path"] = relative_to_root(unit_path, root)
            unit["_source_sha256"] = file_sha256(unit_path)
            unit["_split_digest"] = split_digest(field, unit["cluster_id"])
            units_by_field[field].append(unit)

        prompts_path = suite_dir / "prompts.jsonl"
        suite_prompts = read_jsonl(prompts_path)
        expected_prompts = 150 if field == "boundary_not_for" else 100
        if len(suite_prompts) != expected_prompts:
            raise ValueError(
                f"{field}: expected {expected_prompts} prompts, found {len(suite_prompts)}"
            )
        prompt_file_hashes[relative_to_root(prompts_path, root)] = file_sha256(prompts_path)
        for prompt in suite_prompts:
            if prompt.get("field") != field:
                raise ValueError(
                    f"{prompts_path}: prompt {prompt.get('prompt_id')} has field "
                    f"{prompt.get('field')}, expected {field}"
                )
            prompt["_source_file"] = relative_to_root(prompts_path, root)
            prompt["_source_row_sha256"] = sha256_json(
                {key: value for key, value in prompt.items() if not key.startswith("_")}
            )
            prompts.append(prompt)

    return units_by_field, prompts, prompt_file_hashes


def make_split(units_by_field: dict[str, list[dict[str, Any]]]) -> dict[str, str]:
    split: dict[str, str] = {}
    for field in FIELD_ORDER:
        ordered = sorted(
            units_by_field[field],
            key=lambda unit: (unit["_split_digest"], unit["cluster_id"]),
        )
        for index, unit in enumerate(ordered):
            split[unit["cluster_id"]] = "development" if index < 10 else "confirmatory"
    return split


def build_prompt_rows(
    prompts: list[dict[str, Any]],
    units_by_id: dict[str, dict[str, Any]],
    split: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    prompt_ids: set[str] = set()
    for prompt in sorted(prompts, key=lambda row: row["prompt_id"]):
        prompt_id = str(prompt["prompt_id"])
        if prompt_id in prompt_ids:
            raise ValueError(f"Duplicate prompt_id: {prompt_id}")
        prompt_ids.add(prompt_id)
        cluster_id = str(prompt["cluster_id"])
        unit = units_by_id.get(cluster_id)
        if unit is None:
            raise ValueError(f"{prompt_id}: unknown cluster {cluster_id}")
        source_candidate_ids = [skill["skill_id"] for skill in unit["skills"]]
        prompt_candidate_ids = list(prompt.get("candidate_skill_ids", []))
        if set(source_candidate_ids) != set(prompt_candidate_ids):
            raise ValueError(f"{prompt_id}: candidate identities do not align with unit")
        gold_skill_id = str(prompt["gold_skill_id"])
        if gold_skill_id not in source_candidate_ids:
            raise ValueError(f"{prompt_id}: gold is not one of the three candidates")
        query_text = str(prompt["prompt"]).strip()
        routing_context = str(prompt.get("routing_context", "")).strip()
        if routing_context:
            query_text += f"\n\nRouting context:\n{routing_context}"
        rows.append(
            {
                "schema_version": "rq2a-prompt-v1",
                "protocol_version": PROTOCOL_VERSION,
                "prompt_id": prompt_id,
                "cluster_id": cluster_id,
                "field": prompt["field"],
                "split": split[cluster_id],
                "prompt_variant": prompt["prompt_variant"],
                "prompt": str(prompt["prompt"]).strip(),
                "routing_context": routing_context,
                "query_text": query_text,
                "gold_skill_id": gold_skill_id,
                "candidate_skill_ids": source_candidate_ids,
                "source_prompt_file": prompt["_source_file"],
                "source_prompt_row_sha256": prompt["_source_row_sha256"],
                "source_unit_path": unit["_source_path"],
                "source_unit_sha256": unit["_source_sha256"],
                **text_counts(query_text),
            }
        )
    return rows


def build_representation_rows(
    root: Path,
    units_by_field: dict[str, list[dict[str, Any]]],
    prompt_file_hashes: dict[str, str],
    split: dict[str, str],
    rotations: dict[str, int],
) -> dict[str, list[dict[str, Any]]]:
    rows_by_representation: dict[str, list[dict[str, Any]]] = {
        representation: [] for representation in REPRESENTATIONS
    }
    for field in FIELD_ORDER:
        prompt_source_path = relative_to_root(
            root / "rq1a_field_discriminability" / field / "prompts.jsonl",
            root,
        )
        for unit in sorted(units_by_field[field], key=lambda item: item["cluster_id"]):
            cluster_id = unit["cluster_id"]
            rotation = rotations[cluster_id]
            for candidate_index, skill in enumerate(unit["skills"]):
                fields = candidate_fields(unit, skill)
                proposition_hashes = {
                    field_name: sha256_json(fields[field_name])
                    for field_name in FIELD_ORDER
                }
                all_propositions_sha256 = sha256_json(fields)
                for representation in REPRESENTATIONS:
                    text, field_order, padding_ids = representation_text(
                        representation,
                        unit,
                        fields,
                        rotation,
                    )
                    row = {
                        "schema_version": "rq2a-representation-row-v1",
                        "protocol_version": PROTOCOL_VERSION,
                        "serialiser_version": SERIALISER_VERSION,
                        "representation": representation,
                        "split": split[cluster_id],
                        "field": field,
                        "cluster_id": cluster_id,
                        "skill_id": skill["skill_id"],
                        "candidate_index": candidate_index,
                        "display_name": skill.get("display_name", ""),
                        "role": skill["role"],
                        "gold_skill_id": unit["gold_skill_id"],
                        "source_unit_path": unit["_source_path"],
                        "source_unit_sha256": unit["_source_sha256"],
                        "source_prompt_file": prompt_source_path,
                        "source_prompt_file_sha256": prompt_file_hashes[prompt_source_path],
                        "split_digest": unit["_split_digest"],
                        "canonical_fields": fields,
                        "field_proposition_sha256": proposition_hashes,
                        "all_propositions_sha256": all_propositions_sha256,
                        "field_order": field_order,
                        "order_rotation": rotation if representation == "same-facts-order-controlled" else None,
                        "padding_blocks": padding_ids,
                        "selector_visible_text": text,
                        "selector_visible_text_sha256": sha256_text(text),
                        **text_counts(text),
                    }
                    rows_by_representation[representation].append(row)
    return rows_by_representation


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(
                json.dumps(
                    row,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )


def length_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in ("character_count", "utf8_byte_count", "word_count", "audit_token_count"):
        values = [int(row[key]) for row in rows]
        result[key] = {
            "min": min(values),
            "median": statistics.median(values),
            "mean": statistics.mean(values),
            "max": max(values),
        }
    return result


def build_split_markdown(
    units_by_field: dict[str, list[dict[str, Any]]],
    prompts: list[dict[str, Any]],
    split: dict[str, str],
) -> str:
    prompt_counts: Counter[tuple[str, str]] = Counter(
        (prompt["field"], split[prompt["cluster_id"]]) for prompt in prompts
    )
    lines = [
        "# RQ2a Deterministic Cluster Split",
        "",
        f"- Protocol: `{PROTOCOL_VERSION}`",
        f"- Seed: `{SPLIT_SEED}`",
        "- Rule: SHA-256 sort within field; first 10 development, remaining 40 confirmatory.",
        "",
        "| Field | Development Clusters | Confirmatory Clusters | Development Prompts | Confirmatory Prompts |",
        "|---|---:|---:|---:|---:|",
    ]
    for field in FIELD_ORDER:
        clusters = units_by_field[field]
        dev = sum(split[unit["cluster_id"]] == "development" for unit in clusters)
        confirm = len(clusters) - dev
        lines.append(
            f"| `{field}` | {dev} | {confirm} | "
            f"{prompt_counts[(field, 'development')]} | "
            f"{prompt_counts[(field, 'confirmatory')]} |"
        )
    lines.extend(["", "## Development Clusters", ""])
    for field in FIELD_ORDER:
        cluster_ids = sorted(
            unit["cluster_id"]
            for unit in units_by_field[field]
            if split[unit["cluster_id"]] == "development"
        )
        lines.append(f"- `{field}`: " + ", ".join(f"`{item}`" for item in cluster_ids))
    return "\n".join(lines) + "\n"


def choose_sample_clusters(
    units_by_field: dict[str, list[dict[str, Any]]],
    split: dict[str, str],
) -> dict[str, dict[str, str]]:
    samples: dict[str, dict[str, str]] = {}
    for field in FIELD_ORDER:
        ordered = sorted(
            units_by_field[field],
            key=lambda unit: (unit["_split_digest"], unit["cluster_id"]),
        )
        samples[field] = {
            split_name: next(
                unit["cluster_id"]
                for unit in ordered
                if split[unit["cluster_id"]] == split_name
            )
            for split_name in ("development", "confirmatory")
        }
    return samples


def build_samples_markdown(
    samples: dict[str, dict[str, str]],
    rows_by_representation: dict[str, list[dict[str, Any]]],
) -> str:
    lookup = {
        (row["representation"], row["cluster_id"], row["role"]): row
        for rows in rows_by_representation.values()
        for row in rows
    }
    lines = [
        "# RQ2a Representation Samples",
        "",
        "One gold candidate is shown for one development and one confirmatory cluster per field.",
        "Candidate and gold metadata shown in headings are reviewer-only and are not part of selector-visible text.",
        "",
    ]
    for field in FIELD_ORDER:
        lines.append(f"## {FIELD_CONFIG[field]['label']}")
        lines.append("")
        for split_name in ("development", "confirmatory"):
            cluster_id = samples[field][split_name]
            lines.append(f"### `{cluster_id}` ({split_name})")
            lines.append("")
            for representation in REPRESENTATIONS:
                row = lookup[(representation, cluster_id, "gold")]
                lines.append(f"#### `{representation}`")
                lines.append("")
                lines.append("```text")
                lines.append(row["selector_visible_text"])
                lines.append("```")
                lines.append("")
    return "\n".join(lines)


def main() -> None:
    root = skill_benchmark_root()
    parser = argparse.ArgumentParser(
        description="Build deterministic RQ2a matched-content representation artifacts."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=root / "rq2a_matched_content",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing builder-owned artifacts. Never use after confirmatory freeze.",
    )
    args = parser.parse_args()

    output_root = args.output_root.resolve()
    representations_dir = output_root / "representations"
    owned_paths = [
        output_root / "protocol.json",
        output_root / "split.json",
        output_root / "split.md",
        output_root / "prompts.jsonl",
        output_root / "manifest.json",
        output_root / "representation_samples.md",
        *[representations_dir / f"{representation}.jsonl" for representation in REPRESENTATIONS],
    ]
    existing = [path for path in owned_paths if path.exists()]
    if existing and not args.overwrite:
        joined = "\n".join(str(path) for path in existing[:10])
        raise SystemExit(
            "Builder-owned artifacts already exist. Refusing to overwrite without "
            f"--overwrite:\n{joined}"
        )

    output_root.mkdir(parents=True, exist_ok=True)
    representations_dir.mkdir(parents=True, exist_ok=True)

    units_by_field, source_prompts, prompt_file_hashes = load_sources(root)
    units_by_id = {
        unit["cluster_id"]: unit
        for units in units_by_field.values()
        for unit in units
    }
    split = make_split(units_by_field)
    rotations = build_order_rotation_map(units_by_field)
    prompt_rows = build_prompt_rows(source_prompts, units_by_id, split)
    rows_by_representation = build_representation_rows(
        root,
        units_by_field,
        prompt_file_hashes,
        split,
        rotations,
    )

    protocol = {
        "schema_version": "rq2a-protocol-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "status": "authorised_frozen_for_implementation",
        "scope": "rq2a_only",
        "split_seed": SPLIT_SEED,
        "field_order": FIELD_ORDER,
        "field_labels": {
            field: FIELD_CONFIG[field]["label"] for field in FIELD_ORDER
        },
        "representations": REPRESENTATIONS,
        "padding_blocks": PADDING_BLOCKS,
        "padding_by_representation": PADDING_BY_REPRESENTATION,
        "source_root": "rq1a_field_discriminability",
        "source_cluster_count": len(units_by_id),
        "source_prompt_count": len(prompt_rows),
        "candidate_count_per_cluster": 3,
        "thesis_write_blocked_pending_user_review": True,
    }
    (output_root / "protocol.json").write_text(stable_json(protocol), encoding="utf-8")

    split_payload = {
        "schema_version": "rq2a-split-v1",
        "protocol_version": PROTOCOL_VERSION,
        "seed": SPLIT_SEED,
        "algorithm": "sha256_sort_within_field_first_10_development",
        "clusters": [
            {
                "field": field,
                "cluster_id": unit["cluster_id"],
                "split": split[unit["cluster_id"]],
                "split_digest": unit["_split_digest"],
                "source_unit_path": unit["_source_path"],
                "source_unit_sha256": unit["_source_sha256"],
                "order_rotation": rotations[unit["cluster_id"]],
            }
            for field in FIELD_ORDER
            for unit in sorted(units_by_field[field], key=lambda item: item["cluster_id"])
        ],
    }
    (output_root / "split.json").write_text(stable_json(split_payload), encoding="utf-8")
    (output_root / "split.md").write_text(
        build_split_markdown(units_by_field, source_prompts, split),
        encoding="utf-8",
    )
    write_jsonl(output_root / "prompts.jsonl", prompt_rows)

    file_records: list[dict[str, Any]] = []
    for representation, rows in rows_by_representation.items():
        path = representations_dir / f"{representation}.jsonl"
        write_jsonl(path, rows)
        file_records.append(
            {
                "representation": representation,
                "path": relative_to_root(path, root),
                "row_count": len(rows),
                "sha256": file_sha256(path),
                "length_summary": length_summary(rows),
                "split_counts": dict(Counter(row["split"] for row in rows)),
                "field_counts": dict(Counter(row["field"] for row in rows)),
            }
        )

    samples = choose_sample_clusters(units_by_field, split)
    samples_path = output_root / "representation_samples.md"
    samples_path.write_text(
        build_samples_markdown(samples, rows_by_representation),
        encoding="utf-8",
    )

    rotation_counts = Counter(rotations.values())
    manifest = {
        "schema_version": "rq2a-representation-manifest-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "source": {
            "cluster_count": len(units_by_id),
            "prompt_count": len(prompt_rows),
            "candidate_count": sum(len(unit["skills"]) for unit in units_by_id.values()),
            "field_cluster_counts": {
                field: len(units_by_field[field]) for field in FIELD_ORDER
            },
            "prompt_file_hashes": prompt_file_hashes,
        },
        "split": {
            "development_clusters": sum(value == "development" for value in split.values()),
            "confirmatory_clusters": sum(value == "confirmatory" for value in split.values()),
            "development_prompts": sum(row["split"] == "development" for row in prompt_rows),
            "confirmatory_prompts": sum(row["split"] == "confirmatory" for row in prompt_rows),
            "split_json_sha256": file_sha256(output_root / "split.json"),
        },
        "prompt_artifact": {
            "path": relative_to_root(output_root / "prompts.jsonl", root),
            "row_count": len(prompt_rows),
            "sha256": file_sha256(output_root / "prompts.jsonl"),
        },
        "representations": file_records,
        "order_rotation_counts": {
            str(rotation): rotation_counts[rotation]
            for rotation in range(len(FIELD_ORDER))
        },
        "samples": samples,
        "samples_path": relative_to_root(samples_path, root),
        "samples_sha256": file_sha256(samples_path),
    }
    (output_root / "manifest.json").write_text(stable_json(manifest), encoding="utf-8")

    print(f"Built RQ2a protocol {PROTOCOL_VERSION}")
    print(f"Clusters: {len(units_by_id)}")
    print(f"Prompts: {len(prompt_rows)}")
    print(f"Candidates per representation: {len(next(iter(rows_by_representation.values())))}")
    print(f"Representations: {len(rows_by_representation)}")
    print(f"Output: {output_root}")


if __name__ == "__main__":
    main()
