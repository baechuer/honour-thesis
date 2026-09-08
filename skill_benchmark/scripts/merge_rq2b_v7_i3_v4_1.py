#!/usr/bin/env python3
"""Merge selected full-corpus V4.1 extractions into matched I3C/I3-flat views."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from merge_rq2b_i3c import canonical_extraction, representation_row, summarize
from freeze_rq2b_v7_i3_v4_1_output_selection import verify as verify_selection
from prepare_rq2b_v7_i3_full_reextraction_v4_1 import CACHE, build as build_inputs
from rq2b_common import serialize_i3_flat, serialize_i3c
from validate_rq2b_v7_i3_v4_1_1_batch import PREP, ROOT, validate_v4_1_1_semantics


SELECTION = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_output_selection_2026_09_09_v1")
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_merged_2026_09_09_v4_1")
I1_I2 = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_2026_09_09_v2")
MERGER_VERSION = "rq2b-v7-i3-full-corpus-v4.1-merger-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in values).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build() -> dict[str, bytes]:
    verify_selection()
    assignments_path = ROOT / PREP / "full_reextraction_assignment_manifest.jsonl"
    selection_path = ROOT / SELECTION / "selection_ledger.jsonl"
    assignments = rows(assignments_path.read_bytes())
    selections = rows(selection_path.read_bytes())
    require(len(assignments) == len(selections) == 95, "V4.1 batch coverage mismatch")
    selection_report_path = ROOT / SELECTION / "integrity_report.json"
    selection_report = json.loads(selection_report_path.read_bytes())
    require(selection_report["state"] == "PASS_95_BATCHES_SELECTED_PENDING_MERGE_AND_FRESH_BLINDED_QA", "V4.1 selection report state mismatch")
    require(selection_report["bindings"]["assignment_manifest_sha256"] == sha(assignments_path.read_bytes()), "V4.1 selection assignment binding mismatch")
    require(selection_report["bindings"]["selection_ledger_sha256"] == sha(selection_path.read_bytes()), "V4.1 selection ledger binding mismatch")
    selection_by_batch = {row["batch_id"]: row for row in selections}
    require(len(selection_by_batch) == 95, "duplicate V4.1 selection batch ID")
    _, input_payloads = build_inputs()
    combined: list[tuple[dict, dict]] = []
    batch_inventory = []
    for assignment in assignments:
        batch_id = assignment["batch_id"]
        selected = selection_by_batch.get(batch_id)
        require(selected is not None and selected["input_sha256"] == assignment["input_sha256"], f"V4.1 selection mismatch: {batch_id}")
        input_name = str(Path(assignment["input_path"]).relative_to(CACHE))
        input_data = input_payloads[input_name]
        output_data = (ROOT / selected["selected_output_path"]).read_bytes()
        require(sha(input_data) == assignment["input_sha256"], f"V4.1 input drift: {batch_id}")
        require(sha(output_data) == selected["selected_output_sha256"], f"V4.1 output drift: {batch_id}")
        input_rows, output_rows = rows(input_data), rows(output_data)
        require(len(input_rows) == len(output_rows) == assignment["row_count"], f"V4.1 row mismatch: {batch_id}")
        for input_row, output_row in zip(input_rows, output_rows, strict=True):
            canonical_extraction(input_row, output_row)
            validate_v4_1_1_semantics(input_row, output_row)
            combined.append((input_row, output_row))
        batch_inventory.append({
            "batch_id": batch_id,
            "extractor_group": assignment["extractor_group"],
            "input_sha256": assignment["input_sha256"],
            "selected_output_sha256": selected["selected_output_sha256"],
            "rows": assignment["row_count"],
        })
    combined.sort(key=lambda pair: pair[0]["source_row_index"])
    require(len(combined) == 3798, "V4.1 source coverage mismatch")
    require([row[0]["source_row_index"] for row in combined] == list(range(3798)), "V4.1 source order mismatch")
    require(len({row[0]["source_sha256"] for row in combined}) == 3798, "V4.1 source identity collision")
    canonical_rows, fielded_rows, flat_rows, worker_rows = [], [], [], []
    for input_row, output_row in combined:
        canonical, retained, _ = canonical_extraction(input_row, output_row)
        canonical["merger_version"] = MERGER_VERSION
        canonical_rows.append(canonical)
        worker_rows.append(output_row)
        fielded_rows.append(representation_row(canonical, "I3C-fielded", serialize_i3c(input_row["name"], input_row["description"], retained)))
        flat_rows.append(representation_row(canonical, "I3-flat", serialize_i3_flat(input_row["name"], input_row["description"], retained)))
    summary = summarize(canonical_rows, fielded_rows, flat_rows)
    require(summary["parse_failures"] == summary["identity_failures"] == summary["evidence_substring_failures"] == 0, "V4.1 automatic integrity failure")
    require(summary["i3c_i3flat_evidence_match_rows"] == 3798, "V4.1 matched-evidence failure")
    payloads = {
        "worker_outputs.jsonl": rows_bytes(worker_rows),
        "canonical_extractions.jsonl": rows_bytes(canonical_rows),
        "i3c_fielded.jsonl": rows_bytes(fielded_rows),
        "i3_flat.jsonl": rows_bytes(flat_rows),
    }
    warning_counts = Counter(
        warning.get("code", "warning")
        for row in canonical_rows
        for warning in row["qa_warnings"]
        if isinstance(warning, dict)
    )
    manifest = {
        "schema_version": "rq2b-v7-phase7-i3-full-corpus-merged-v4.1",
        "state": "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING",
        "formal_execution_ready": False,
        "retrieval_or_reranking_runs": 0,
        "provider_calls": 0,
        "merger_version": MERGER_VERSION,
        "counts": {"sources": 3798, "fresh_full_corpus": 3798, "batches": 95},
        "bindings": {
            "preparation_report_sha256": sha((ROOT / PREP / "preparation_report.json").read_bytes()),
            "assignment_manifest_sha256": sha(assignments_path.read_bytes()),
            "selection_ledger_sha256": sha(selection_path.read_bytes()),
            "selection_report_sha256": sha(selection_report_path.read_bytes()),
            "i1_i2_v2_report_sha256": sha((ROOT / I1_I2 / "mechanical_report.json").read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "automatic_summary": summary,
        "qa_warning_codes": dict(sorted(warning_counts.items())),
        "batch_inventory": batch_inventory,
        "artifacts": {name: {"sha256": sha(data), "rows": len(data.splitlines()), "utf8_bytes": len(data)} for name, data in payloads.items()},
        "semantic_qa": {"required": True, "state": "PENDING_NEW_120_ROW_SOURCE_ONLY_SAMPLE", "historical_sample_inherited": False, "execution_authorised": False},
    }
    payloads["manifest.json"] = json_bytes(manifest)
    payloads["README.md"] = (
        "# V7 Phase-7 I3 full-corpus V4.1 merge\n\n"
        "All 3,798 sources have fresh source-only extractions. I3C and I3-flat use the same retained evidence multiset. Automatic integrity passing is not selector authority; a new 120-row blinded semantic QA remains mandatory.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/merge_rq2b_v7_i3_v4_1.py --verify`.\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1 merged package missing")
        require({path.name for path in root.iterdir()} == set(expected), "V4.1 merged file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1 merged artifact drift: {name}")
        status = "PASS_V7_I3_V4_1_MERGE_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1 merged package")
        root.mkdir(parents=True)
        for name, data in expected.items():
            (root / name).write_bytes(data)
        status = "PASS_V7_I3_V4_1_MERGE_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
