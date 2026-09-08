#!/usr/bin/env python3
"""Merge validated V7 I3 reuse and fresh extraction into portable artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from merge_rq2b_i3c import canonical_extraction, representation_row, summarize
from prepare_rq2b_v7_i3_extraction import (
    CACHE as EXTRACTION_CACHE,
    OUTPUT as EXTRACTION_PREP,
    SOURCE_PACKAGE,
    build as build_extraction_inputs,
    current_input,
)
from rq2b_common import serialize_i3_flat, serialize_i3c


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_merged_2026_09_08_v1")
SELECTION = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_output_selection_2026_09_08_v1")
MERGER_VERSION = "rq2b-v7-i3-merger-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def read_rows_bytes(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.splitlines()]


def read_rows(path: Path) -> list[dict[str, Any]]:
    return read_rows_bytes(path.read_bytes())


def load_fresh_outputs(assignments: list[dict[str, Any]], replay: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if replay:
        path = ROOT / OUTPUT / "fresh_worker_outputs.jsonl"
        require(path.is_file(), "portable fresh worker output is missing")
        all_outputs = read_rows(path)
        by_skill = {row["skill_id"]: row for row in all_outputs}
        require(len(by_skill) == len(all_outputs), "duplicate portable fresh worker output identity")
    else:
        by_skill = {}
        selections = read_rows(ROOT / SELECTION / "selection_ledger.jsonl")
        require(len(selections) == len(assignments), "I3 output selection coverage mismatch")
        selection_by_batch = {row["batch_id"]: row for row in selections}
        for assignment in assignments:
            selected = selection_by_batch.get(assignment["batch_id"])
            require(selected is not None and selected["input_sha256"] == assignment["input_sha256"],
                    f"fresh output selection mismatch: {assignment['batch_id']}")
            output_path = ROOT / selected["selected_output_path"]
            require(output_path.is_file(), f"selected fresh output missing: {assignment['batch_id']}")
            require(sha_path(output_path) == selected["selected_output_sha256"],
                    f"selected fresh output hash mismatch: {assignment['batch_id']}")
            for row in read_rows(output_path):
                require(row["skill_id"] not in by_skill, f"duplicate fresh worker identity: {row['skill_id']}")
                by_skill[row["skill_id"]] = row
        all_outputs = []
    batch_reports: list[dict[str, Any]] = []
    ordered: list[dict[str, Any]] = []
    _, input_payloads = build_extraction_inputs(None)
    for assignment in assignments:
        input_name = str(Path(assignment["input_path"]).relative_to(EXTRACTION_CACHE))
        inputs_data = input_payloads[input_name]
        require(sha_bytes(inputs_data) == assignment["input_sha256"], f"fresh input replay mismatch: {assignment['batch_id']}")
        inputs = read_rows_bytes(inputs_data)
        outputs = []
        for input_row in inputs:
            output_row = by_skill.get(input_row["skill_id"])
            require(output_row is not None, f"fresh output row missing: {input_row['skill_id']}")
            canonical_extraction(input_row, output_row)
            outputs.append(output_row)
        output_data = rows_bytes(outputs)
        if not replay:
            selected = selection_by_batch[assignment["batch_id"]]
            require(sha_bytes(output_data) == selected["selected_output_sha256"],
                    f"fresh output order or serialization drift: {assignment['batch_id']}")
        batch_reports.append({
            "batch_id": assignment["batch_id"],
            "input_sha256": assignment["input_sha256"],
            "output_sha256": sha_bytes(output_data),
            "rows": len(outputs),
        })
        ordered.extend(outputs)
    require(len(ordered) == 1368 and len({row["skill_id"] for row in ordered}) == 1368, "fresh output coverage mismatch")
    if replay:
        require(len(all_outputs) == len(ordered), "extra portable fresh worker outputs")
    return ordered, batch_reports


def build(replay: bool) -> dict[str, bytes]:
    assignments = read_rows(ROOT / EXTRACTION_PREP / "fresh_assignment_manifest.jsonl")
    reused = read_rows(ROOT / EXTRACTION_PREP / "reused_worker_outputs.jsonl")
    fresh, batch_reports = load_fresh_outputs(assignments, replay)
    worker_by_id = {row["skill_id"]: row for row in [*reused, *fresh]}
    require(len(reused) == 2430 and len(worker_by_id) == 3798, "combined worker output coverage mismatch")

    sources = read_rows(ROOT / SOURCE_PACKAGE / "source_manifest.jsonl")
    canonical_rows: list[dict[str, Any]] = []
    fielded_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    for index, source in enumerate(sources):
        input_row = current_input(index, source)
        output_row = worker_by_id.get(input_row["skill_id"])
        require(output_row is not None, f"combined output missing: {input_row['skill_id']}")
        canonical, retained, _ = canonical_extraction(input_row, output_row)
        canonical["merger_version"] = MERGER_VERSION
        fielded_text = serialize_i3c(input_row["name"], input_row["description"], retained)
        flat_text = serialize_i3_flat(input_row["name"], input_row["description"], retained)
        canonical_rows.append(canonical)
        fielded_rows.append(representation_row(canonical, "I3C-fielded", fielded_text))
        flat_rows.append(representation_row(canonical, "I3-flat", flat_text))
    require([row["source_row_index"] for row in canonical_rows] == list(range(3798)), "canonical source order mismatch")
    require(len({row["source_sha256"] for row in canonical_rows}) == 3798, "canonical source SHA collision")
    automatic_summary = summarize(canonical_rows, fielded_rows, flat_rows)
    require(automatic_summary["parse_failures"] == 0, "I3 parse failure")
    require(automatic_summary["identity_failures"] == 0, "I3 identity failure")
    require(automatic_summary["evidence_substring_failures"] == 0, "I3 evidence grounding failure")
    require(automatic_summary["i3c_i3flat_evidence_match_rows"] == 3798, "I3 matched-evidence failure")

    payloads = {
        "fresh_worker_outputs.jsonl": rows_bytes(fresh),
        "canonical_extractions.jsonl": rows_bytes(canonical_rows),
        "i3c_fielded.jsonl": rows_bytes(fielded_rows),
        "i3_flat.jsonl": rows_bytes(flat_rows),
    }
    warning_counts = Counter()
    fresh_ids = {row["skill_id"] for row in fresh}
    for row in canonical_rows:
        if row["qa_warnings"]:
            warning_counts["fresh" if row["skill_id"] in fresh_ids else "reused"] += 1
    manifest = {
        "schema_version": "rq2b-v7-phase7-i3-merged-manifest-v1",
        "state": "AUTOMATIC_INTEGRITY_PASS_FRESH_CURRENT_BLINDED_SEMANTIC_QA_PENDING",
        "formal_execution_ready": False,
        "retrieval_or_reranking_runs": 0,
        "provider_calls": 0,
        "merger_version": MERGER_VERSION,
        "counts": {"sources": 3798, "reused_pending_current_qa": 2430, "fresh": 1368, "fresh_batches": 35},
        "bindings": {
            "source_manifest_sha256": sha_path(ROOT / SOURCE_PACKAGE / "source_manifest.jsonl"),
            "extraction_preparation_report_sha256": sha_path(ROOT / EXTRACTION_PREP / "preparation_report.json"),
            "fresh_assignment_manifest_sha256": sha_path(ROOT / EXTRACTION_PREP / "fresh_assignment_manifest.jsonl"),
            "reused_worker_outputs_sha256": sha_path(ROOT / EXTRACTION_PREP / "reused_worker_outputs.jsonl"),
            "fresh_output_selection_ledger_sha256": sha_path(ROOT / SELECTION / "selection_ledger.jsonl"),
            "fresh_output_selection_report_sha256": sha_path(ROOT / SELECTION / "integrity_report.json"),
            "builder_sha256": sha_path(Path(__file__).resolve()),
        },
        "automatic_summary": automatic_summary,
        "rows_with_qa_warnings_by_provenance": dict(sorted(warning_counts.items())),
        "fresh_batch_inventory": batch_reports,
        "artifacts": {name: {"sha256": sha_bytes(data), "rows": len(data.splitlines()), "utf8_bytes": len(data)} for name, data in payloads.items()},
        "semantic_qa": {
            "required": True,
            "state": "PENDING",
            "minimum_rows": 120,
            "historical_v3_qa_inherited": False,
            "execution_authorised": False,
        },
    }
    payloads["manifest.json"] = json_bytes(manifest)
    payloads["README.md"] = (
        "# V7 Phase-7 I3 merged artifacts\n\n"
        "This package combines 2,430 source-SHA-identical unambiguous V3 extractions with 1,368 fresh source-only V7 extractions. "
        "All 3,798 rows pass schema, identity, exact-source-substring and I3C/I3-flat evidence-multiset checks.\n\n"
        "The artifacts are not yet authorised for formal selectors: the historical V3 semantic-QA attempt is not inherited, and a fresh current blinded, stratified semantic QA remains mandatory.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/merge_rq2b_v7_i3.py --verify`\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / OUTPUT
    expected = build(args.verify)
    if args.verify:
        require(output.is_dir(), "merged I3 package is missing")
        require({path.name for path in output.iterdir()} == set(expected), "merged I3 file-set drift")
        for name, data in expected.items():
            require((output / name).read_bytes() == data, f"merged I3 artifact drift: {name}")
        status = "PASS_V7_I3_MERGE_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite versioned merged I3 package")
        output.mkdir(parents=True)
        for name, data in expected.items():
            (output / name).write_bytes(data)
        status = "PASS_V7_I3_MERGE_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
