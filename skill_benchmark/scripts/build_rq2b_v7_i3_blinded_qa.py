#!/usr/bin/env python3
"""Build a fresh 120-row source-only blinded QA packet for V7 I1/I3 views."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from merge_rq2b_i3c import FIELD_KEYS
from prepare_rq2b_v7_i3_extraction import SOURCE_PACKAGE, build as build_inputs, current_input


ROOT = Path(__file__).resolve().parents[2]
MERGED = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_merged_2026_09_08_v1")
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_08_v1")
SAMPLE_PER_PROVENANCE = 60
PER_LENGTH_QUARTILE = 15
MIN_PRESENT_PER_FIELD_AND_PROVENANCE = 5
SEED = "rq2b-v7-i3-qa-2026090803"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def stable_key(*values: object) -> str:
    return sha((SEED + "|" + "|".join(str(value) for value in values)).encode())


def length_quartiles(sources: list[dict[str, Any]]) -> dict[str, str]:
    ordered = sorted(sources, key=lambda row: (row["bytes"], row["sha256"]))
    result = {}
    for index, source in enumerate(ordered):
        result[source["sha256"]] = f"Q{min(3, index * 4 // len(ordered)) + 1}"
    return result


def visible_fields(canonical: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    result = {field: [] for field in FIELD_KEYS}
    for span in canonical["retained_selector_spans"]:
        result[span["field_key"]].append({
            "id": span["item_id"],
            "evidence": span["evidence"],
            "evidence_status": "explicit",
        })
    return result


def sample_provenance(rows: list[dict[str, Any]], provenance: str) -> list[dict[str, Any]]:
    pool = [row for row in rows if row["provenance"] == provenance]
    selected: list[dict[str, Any]] = []
    for quartile in ("Q1", "Q2", "Q3", "Q4"):
        candidates = sorted((row for row in pool if row["length_quartile"] == quartile),
                            key=lambda row: stable_key(provenance, quartile, row["skill_id"]))
        require(len(candidates) >= PER_LENGTH_QUARTILE, f"insufficient QA rows: {provenance}/{quartile}")
        selected.extend(candidates[:PER_LENGTH_QUARTILE])
    selected_ids = {row["skill_id"] for row in selected}
    for field in FIELD_KEYS:
        while sum(field in row["present_fields"] for row in selected) < MIN_PRESENT_PER_FIELD_AND_PROVENANCE:
            candidates = sorted(
                (row for row in pool if row["skill_id"] not in selected_ids and field in row["present_fields"]),
                key=lambda row: stable_key("swap-in", provenance, field, row["skill_id"]),
            )
            require(candidates, f"cannot cover QA field: {provenance}/{field}")
            incoming = candidates[0]
            removable = []
            for row in selected:
                if row["length_quartile"] != incoming["length_quartile"]:
                    continue
                if all(
                    current_field not in row["present_fields"]
                    or sum(current_field in item["present_fields"] for item in selected) > MIN_PRESENT_PER_FIELD_AND_PROVENANCE
                    for current_field in FIELD_KEYS
                ):
                    removable.append(row)
            require(removable, f"cannot preserve QA quotas while adding: {provenance}/{field}")
            outgoing = max(removable, key=lambda row: stable_key("swap-out", provenance, field, row["skill_id"]))
            selected.remove(outgoing)
            selected_ids.remove(outgoing["skill_id"])
            selected.append(incoming)
            selected_ids.add(incoming["skill_id"])
    require(len(selected) == SAMPLE_PER_PROVENANCE and len(selected_ids) == SAMPLE_PER_PROVENANCE, "QA sample coverage mismatch")
    require(Counter(row["length_quartile"] for row in selected) == Counter({f"Q{i}": 15 for i in range(1, 5)}), "QA quartile balance mismatch")
    return selected


def assign_reviewer_groups(selected: list[dict[str, Any]]) -> dict[str, int]:
    assignment: dict[str, int] = {}
    counts = Counter()
    fresh = sorted((row for row in selected if row["provenance"] == "FRESH"), key=lambda row: stable_key("fresh-assign", row["skill_id"]))
    for row in fresh:
        allowed = [group for group in (1, 2, 3) if group != row["extractor_group"] and counts[(group, "FRESH")] < 20]
        require(allowed, "cannot cross-assign fresh QA rows")
        group = min(allowed, key=lambda value: (counts[(value, "FRESH")], value))
        assignment[row["skill_id"]] = group
        counts[(group, "FRESH")] += 1
    reused = sorted((row for row in selected if row["provenance"] == "REUSED"), key=lambda row: stable_key("reuse-assign", row["skill_id"]))
    for row in reused:
        group = min((1, 2, 3), key=lambda value: (counts[(value, "REUSED")], value))
        require(counts[(group, "REUSED")] < 20, "reuse QA group overflow")
        assignment[row["skill_id"]] = group
        counts[(group, "REUSED")] += 1
    for group in (1, 2, 3):
        require(counts[(group, "FRESH")] == counts[(group, "REUSED")] == 20, f"QA group balance mismatch: {group}")
    return assignment


def calibration() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    def empty() -> dict[str, list[dict[str, str]]]:
        return {field: [] for field in FIELD_KEYS}

    fixtures, answers = [], []
    cases = [
        ("Use when processing born-digital PDFs.\nOutput: UTF-8 text.", "Use when processing born-digital PDFs.", "use_conditions", False, False, []),
        ("Input: a .proto schema.\nOutput: compatibility report.", "Input: a .proto schema.", "output_artifacts", False, True, ["WRONG_OPERATIONAL_FIELD"]),
        ("Do not use for scanned PDFs.", "Do not use for scanned PDFs.", "workflow_steps", False, True, ["BOUNDARY_POLARITY_MISCLASSIFIED"]),
        ("Use when reconciling payment disputes.", "The user needs help.", "use_conditions", True, False, ["EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING"]),
        ("Requires the GitHub API and a token.", "Requires the GitHub API and a token.", "dependencies_resources", False, False, []),
        ("Use only for DOCX manuscripts.\nNormalize citation punctuation.", "Normalize citation punctuation.", "workflow_steps", False, True, ["MISSING_SELECTION_CRITICAL_CONTENT"]),
        ("Before the session, gather:\n- account ID\n- date range", "Before the session, gather:", "input_preconditions", False, True, ["NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN"]),
        ("Verify the exported archive opens successfully.", "Verify the exported archive opens successfully.", "success_criteria", False, False, []),
    ]
    for index, (source, evidence, field, critical, major, codes) in enumerate(cases, 1):
        fields = empty()
        fields[field] = [{"id": f"item_{index}", "evidence": evidence, "evidence_status": "explicit"}]
        review_id = f"CAL-{index:03d}"
        fixtures.append({"review_id": review_id, "source_text": source, "native_selector_metadata": {"name": "Calibration", "description": ""}, "selector_visible_evidence": fields})
        answers.append({"review_id": review_id, "critical_error": critical, "major_error": major, "affected_fields": [field] if critical or major else [], "error_codes": codes})
    return fixtures, answers


GUIDANCE = """# V7 blinded I1/I3 extraction-fidelity QA

Judge only whether native name/description plus the visible evidence faithfully preserve source information that could change skill selection. Do not judge any benchmark prompt, target, acceptable set, ranking, or result. Do not use network access.

The packet contains only evidence that the actual I3C/I3-flat serializers retain. A heading or duplicate already omitted by the serializer is not visible and must not be scored.

Critical codes (critical=true, major=false):
- EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING
- BENCHMARK_OR_ROUTING_LEAKAGE

Major codes (critical=false, major=true), only when selection meaning materially changes:
- WRONG_OPERATIONAL_FIELD
- MISSING_SELECTION_CRITICAL_CONTENT
- NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN
- BOUNDARY_POLARITY_MISCLASSIFIED

`dependencies_resources` is for packages, tools, APIs, files, credentials and external resources. `input_preconditions` is for the task input/state a caller must supply. A prohibition/not-for statement belongs in `constraints_boundaries`, not workflow. Workflow evidence must itself express an operation; a bare Step heading or noun fragment is not self-contained.

Do not report a major for harmless overlap, formatting, an empty source-absent field, or information already fully carried by native name/description. Critical and major are mutually exclusive for a row. A clean row has both false and no codes. Notes must quote exact evidence for every error.
"""


def build() -> dict[str, bytes]:
    manifest = json.loads((ROOT / MERGED / "manifest.json").read_bytes())
    require(manifest["state"] == "AUTOMATIC_INTEGRITY_PASS_FRESH_CURRENT_BLINDED_SEMANTIC_QA_PENDING", "merged I3 is not QA-ready")
    canonical = read_rows(ROOT / MERGED / "canonical_extractions.jsonl")
    fresh_ids = {row["skill_id"] for row in read_rows(ROOT / MERGED / "fresh_worker_outputs.jsonl")}
    sources = read_rows(ROOT / SOURCE_PACKAGE / "source_manifest.jsonl")
    require(len(canonical) == len(sources) == 3798, "QA population mismatch")
    quartiles = length_quartiles(sources)

    fresh_batch_by_id: dict[str, int] = {}
    _, input_payloads = build_inputs(None)
    for relative, data in sorted(input_payloads.items()):
        batch_number = int(Path(relative).stem.rsplit("_", 1)[-1])
        for row in [json.loads(line) for line in data.splitlines()]:
            fresh_batch_by_id[row["skill_id"]] = batch_number
    require(set(fresh_batch_by_id) == fresh_ids, "fresh batch provenance mismatch")

    population = []
    for index, (source, extraction) in enumerate(zip(sources, canonical, strict=True)):
        input_row = current_input(index, source)
        require(input_row["source_sha256"] == extraction["source_sha256"], "QA source/canonical mismatch")
        fields = visible_fields(extraction)
        batch_number = fresh_batch_by_id.get(extraction["skill_id"])
        extractor_group = None if batch_number is None else 1 if batch_number <= 12 else 2 if batch_number <= 24 else 3
        population.append({
            "source_row_index": index,
            "skill_id": extraction["skill_id"],
            "source_sha256": extraction["source_sha256"],
            "source_path": extraction["source"],
            "source_text": input_row["text"],
            "name": extraction["name"],
            "description": extraction["description"],
            "visible_fields": fields,
            "present_fields": sorted(field for field, items in fields.items() if items),
            "length_quartile": quartiles[extraction["source_sha256"]],
            "provenance": "FRESH" if extraction["skill_id"] in fresh_ids else "REUSED",
            "fresh_batch": batch_number,
            "extractor_group": extractor_group,
        })
    selected = [*sample_provenance(population, "REUSED"), *sample_provenance(population, "FRESH")]
    reviewer_groups = assign_reviewer_groups(selected)
    selected.sort(key=lambda row: stable_key("review-id", row["skill_id"]))

    reviewer_rows, key_rows = [], []
    for index, row in enumerate(selected, 1):
        review_id = "V7-I3-QA-" + sha((SEED + "|" + row["skill_id"]).encode())[:16].upper()
        reviewer_rows.append({
            "review_id": review_id,
            "source_text": row["source_text"],
            "native_selector_metadata": {"name": row["name"], "description": row["description"]},
            "selector_visible_evidence": row["visible_fields"],
        })
        key_rows.append({
            "review_id": review_id,
            "sample_index": index,
            "source_row_index": row["source_row_index"],
            "source_sha256": row["source_sha256"],
            "source_path": row["source_path"],
            "provenance": row["provenance"],
            "length_quartile": row["length_quartile"],
            "present_fields": row["present_fields"],
            "fresh_batch": row["fresh_batch"],
            "extractor_group": row["extractor_group"],
            "assigned_reviewer_group": reviewer_groups[row["skill_id"]],
        })
    visible_by_id = {row["review_id"]: row for row in reviewer_rows}
    files: dict[str, bytes] = {
        "blinded_reviewer_packet.jsonl": rows_bytes(reviewer_rows),
        "sampling_key_do_not_give_reviewer.jsonl": rows_bytes(key_rows),
        "reviewer_guidance.md": GUIDANCE.encode(),
    }
    for group in (1, 2, 3):
        group_keys = [row for row in key_rows if row["assigned_reviewer_group"] == group]
        reuse = sorted((row for row in group_keys if row["provenance"] == "REUSED"), key=lambda row: stable_key("slot", row["review_id"]))
        fresh = sorted((row for row in group_keys if row["provenance"] == "FRESH"), key=lambda row: stable_key("slot", row["review_id"]))
        require(len(reuse) == len(fresh) == 20, f"reviewer group imbalance: {group}")
        for within_group in (0, 1):
            slot = (group - 1) * 2 + within_group + 1
            slot_keys = [*reuse[within_group * 10:(within_group + 1) * 10], *fresh[within_group * 10:(within_group + 1) * 10]]
            slot_rows = [visible_by_id[row["review_id"]] for row in sorted(slot_keys, key=lambda row: stable_key("slot-order", row["review_id"]))]
            files[f"review_slots/qa_slot_{slot:02d}.jsonl"] = rows_bytes(slot_rows)
    fixtures, answers = calibration()
    files["calibration_input.jsonl"] = rows_bytes(fixtures)
    files["calibration_answer_key_do_not_give_reviewer.jsonl"] = rows_bytes(answers)
    return_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["review_id", "review_status", "critical_error", "major_error", "affected_fields", "error_codes", "reviewer_notes", "reviewer_group"],
        "properties": {
            "review_id": {"type": "string"},
            "review_status": {"const": "COMPLETE"},
            "critical_error": {"type": "boolean"},
            "major_error": {"type": "boolean"},
            "affected_fields": {"type": "array", "uniqueItems": True, "items": {"enum": list(FIELD_KEYS)}},
            "error_codes": {"type": "array", "uniqueItems": True, "items": {"enum": ["EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING", "BENCHMARK_OR_ROUTING_LEAKAGE", "WRONG_OPERATIONAL_FIELD", "MISSING_SELECTION_CRITICAL_CONTENT", "NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN", "BOUNDARY_POLARITY_MISCLASSIFIED"]}},
            "reviewer_notes": {"type": "string", "minLength": 1},
            "reviewer_group": {"enum": [1, 2, 3]},
        },
    }
    files["reviewer_return_schema.json"] = json_bytes(return_schema)
    report = {
        "schema_version": "rq2b-v7-i3-blinded-qa-packet-v1",
        "state": "FROZEN_PENDING_THREE_CROSS_ASSIGNED_REVIEWER_GROUPS",
        "formal_execution_ready": False,
        "sample_size": 120,
        "review_slots": 6,
        "rows_per_slot": 20,
        "calibration_rows": 8,
        "sampling_seed": SEED,
        "counts": {
            "provenance": dict(sorted(Counter(row["provenance"] for row in key_rows).items())),
            "length_quartile": dict(sorted(Counter(row["length_quartile"] for row in key_rows).items())),
            "reviewer_group": dict(sorted(Counter(row["assigned_reviewer_group"] for row in key_rows).items())),
            "present_field_rows": {field: sum(field in row["present_fields"] for row in key_rows) for field in FIELD_KEYS},
        },
        "cross_assignment": "Fresh rows are never assigned to the group that extracted their batch; each group receives 20 reused and 20 fresh rows in two 20-row slots.",
        "pass_rule": {
            "calibration": "each reviewer group must exactly match all 8 hidden answers before its returns are accepted",
            "critical_error_rows": 0,
            "maximum_major_error_rows": 6,
            "maximum_major_error_rate": 0.05,
            "field_stratum_rule": "for every field represented in at least 20 sampled rows, major_error_rows/represented_rows must be <=0.05; any field below 20 is reported but not separately thresholded",
            "failure_action": "repair the entire affected rule/class, preserve originals, rebuild all representations, then draw a fresh versioned sample; never repair only sampled rows",
        },
        "bindings": {
            "merged_manifest_sha256": sha((ROOT / MERGED / "manifest.json").read_bytes()),
            "canonical_extractions_sha256": sha((ROOT / MERGED / "canonical_extractions.jsonl").read_bytes()),
            "source_manifest_sha256": sha((ROOT / SOURCE_PACKAGE / "source_manifest.jsonl").read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
    }
    report["artifacts"] = {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in files.items()}
    files["manifest.json"] = json_bytes(report)
    files["README.md"] = (
        "# V7 Phase-7 blinded I1/I3 QA\n\n"
        "Six 20-row slots form a 120-row sample: 60 reused and 60 fresh, with exact length-quartile balance. Fresh rows are cross-assigned away from their extractor group. "
        "Reviewers receive only source text, native I1 metadata and actual selector-visible retained evidence.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_blinded_qa.py --verify`\n"
    ).encode()
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    output = ROOT / OUTPUT
    if args.verify:
        require(output.is_dir(), "V7 I3 QA packet is missing")
        actual_files = {path.relative_to(output) for path in output.rglob("*") if path.is_file()}
        require(actual_files == {Path(name) for name in expected}, "V7 I3 QA file-set drift")
        for name, data in expected.items():
            require((output / name).read_bytes() == data, f"V7 I3 QA artifact drift: {name}")
        status = "PASS_V7_I3_BLINDED_QA_PACKET_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite versioned V7 I3 QA packet")
        for name, data in expected.items():
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_BLINDED_QA_PACKET_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
