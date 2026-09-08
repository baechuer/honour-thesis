#!/usr/bin/env python3
"""Freeze all V7 I3 attempts and select the latest traceable reissue per batch.

This is a provenance/mechanical selection only.  It does not replace the fresh
independent extraction-fidelity QA required before selector execution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from merge_rq2b_i3c import canonical_extraction
from prepare_rq2b_v7_i3_extraction import CACHE, OUTPUT as EXTRACTION_PREP, build as build_inputs


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_output_selection_2026_09_08_v1")
CANONICAL_SEMANTIC_JSONL_SERIALIZER = "jsonl-utf8-sort-keys-compact-lf-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_rows_bytes(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(rows: list[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def canonical_semantic_rows_bytes(rows: list[dict[str, Any]]) -> bytes:
    """Serialize parsed rows for a format-insensitive semantic content hash."""
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in rows
    ).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def validate_attempt(inputs: list[dict[str, Any]], data: bytes, batch_id: str) -> list[dict[str, Any]]:
    outputs = read_rows_bytes(data)
    require(len(inputs) == len(outputs), f"attempt row count mismatch: {batch_id}")
    for input_row, output_row in zip(inputs, outputs, strict=True):
        canonical_extraction(input_row, output_row)
    return outputs


def local_attempt_paths(batch_number: str) -> list[Path]:
    original = ROOT / CACHE / f"outputs/i3_output_{batch_number}.jsonl"
    require(original.is_file(), f"original output missing: I3-{batch_number}")
    candidates = {
        *sorted((ROOT / CACHE / "reissues").glob(f"i3_output_{batch_number}*.jsonl")),
        *sorted((ROOT / CACHE / "outputs").glob(f"i3_output_{batch_number}*.jsonl")),
    }
    candidates.discard(original)
    return [original, *sorted(candidates, key=lambda path: path.as_posix())]


def create() -> None:
    output = ROOT / OUTPUT
    require(not output.exists(), "refusing to overwrite versioned I3 selection freeze")
    assignments = read_rows_bytes((ROOT / EXTRACTION_PREP / "fresh_assignment_manifest.jsonl").read_bytes())
    _, payloads = build_inputs(None)
    artifact_payloads: dict[Path, bytes] = {}
    ledger: list[dict[str, Any]] = []
    selected_reissue_batches = 0
    total_attempts = 0
    for assignment in assignments:
        batch_id = assignment["batch_id"]
        number = batch_id.removeprefix("I3-")
        input_name = str(Path(assignment["input_path"]).relative_to(CACHE))
        input_data = payloads[input_name]
        require(sha(input_data) == assignment["input_sha256"], f"input replay mismatch: {batch_id}")
        inputs = read_rows_bytes(input_data)
        local_paths = local_attempt_paths(number)
        attempts = []
        selectable_reissues: list[tuple[int, int]] = []
        for index, path in enumerate(local_paths, 1):
            data = path.read_bytes()
            try:
                outputs = validate_attempt(inputs, data, batch_id)
                validator_status, validator_error = "PASS", None
                canonical_semantic_sha256 = sha(canonical_semantic_rows_bytes(outputs))
            except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
                validator_status, validator_error = "INVALID_PRESERVED_NOT_SELECTABLE", f"{type(error).__name__}: {error}"
                canonical_semantic_sha256 = None
            tracked = Path("attempts") / batch_id / f"attempt_{index:03d}.jsonl"
            artifact_payloads[tracked] = data
            reissue_match = re.fullmatch(rf"i3_output_{number}_reissue_(\d{{3}})\.jsonl", path.name)
            if reissue_match is not None and validator_status == "PASS":
                selectable_reissues.append((int(reissue_match.group(1)), index))
            attempts.append({
                "attempt_number": index,
                "attempt_kind": "ORIGINAL" if index == 1 else "CANONICAL_TRACEABLE_REISSUE" if reissue_match is not None else "NONCANONICAL_OR_INVALID_ATTEMPT_PRESERVED",
                "local_source_path": str(path.relative_to(ROOT)),
                "tracked_path": str(OUTPUT / tracked),
                "sha256": sha(data),
                "raw_sha256": sha(data),
                "canonical_semantic_jsonl_sha256": canonical_semantic_sha256,
                "rows": len(inputs),
                "validator_status": validator_status,
                "validator_error": validator_error,
                "selected": False,
            })
        original_selectable = attempts[0]["validator_status"] == "PASS"
        require(selectable_reissues or original_selectable, f"no mechanically valid output attempt: {batch_id}")
        selected_attempt_number = max(selectable_reissues)[1] if selectable_reissues else 1
        attempts[selected_attempt_number - 1]["selected"] = True
        total_attempts += len(attempts)
        if attempts[selected_attempt_number - 1]["attempt_kind"] == "CANONICAL_TRACEABLE_REISSUE":
            selected_reissue_batches += 1
        selected_attempt = next(row for row in attempts if row["selected"])
        ledger.append({
            "schema_version": "rq2b-v7-i3-output-selection-ledger-v2",
            "batch_id": batch_id,
            "input_sha256": assignment["input_sha256"],
            "row_count": assignment["row_count"],
            "attempts": attempts,
            "selected_attempt_number": selected_attempt_number,
            "selected_output_path": selected_attempt["tracked_path"],
            "selected_output_sha256": selected_attempt["raw_sha256"],
            "selected_output_raw_sha256": selected_attempt["raw_sha256"],
            "selected_output_canonical_semantic_jsonl_sha256": selected_attempt["canonical_semantic_jsonl_sha256"],
            "canonical_semantic_jsonl_serializer": CANONICAL_SEMANTIC_JSONL_SERIALIZER,
            "selection_rule": "HIGHEST_CANONICAL_THREE_DIGIT_TRACEABLE_REISSUE_IF_PRESENT_ELSE_ORIGINAL; noncanonical vN attempts preserved but never selected; mechanical provenance freeze pending independent semantic QA",
        })
    ledger_data = rows_bytes(ledger)
    report = {
        "schema_version": "rq2b-v7-i3-output-selection-freeze-report-v2",
        "status": "PASS_ALL_ATTEMPTS_PRESERVED_AND_MECHANICALLY_VALIDATED_PENDING_INDEPENDENT_SEMANTIC_QA",
        "formal_execution_ready": False,
        "retrieval_or_reranking_runs": 0,
        "provider_calls": 0,
        "counts": {
            "batches": len(ledger),
            "selected_rows": sum(row["row_count"] for row in ledger),
            "total_attempt_files": total_attempts,
            "batches_selecting_reissue": selected_reissue_batches,
            "batches_selecting_original": len(ledger) - selected_reissue_batches,
        },
        "bindings": {
            "assignment_manifest_sha256": sha((ROOT / EXTRACTION_PREP / "fresh_assignment_manifest.jsonl").read_bytes()),
            "selection_ledger_sha256": sha(ledger_data),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "serialization_contract": {
            "selected_output_sha256_semantics": "RAW_BYTES_SHA256",
            "canonical_semantic_jsonl_sha256_semantics": "PARSED_JSON_ROWS_FORMAT_INSENSITIVE_SHA256",
            "canonical_semantic_jsonl_serializer": CANONICAL_SEMANTIC_JSONL_SERIALIZER,
        },
        "boundary": "A selected reissue passed schema/identity/exact-substring validation and was explicitly preserved. Selection is not a semantic-fidelity pass; fresh blinded QA remains mandatory.",
    }
    output.mkdir(parents=True)
    for relative, data in artifact_payloads.items():
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (output / "selection_ledger.jsonl").write_bytes(ledger_data)
    (output / "integrity_report.json").write_bytes(json_bytes(report))
    (output / "README.md").write_text(
        "# V7 I3 output-attempt selection freeze\n\n"
        "Every original and reissue attempt is retained byte-for-byte. The latest numbered traceable reissue is selected when present; otherwise the original is selected. "
        "This is a mechanical/provenance choice only and does not grant semantic QA or selector-execution authority.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/freeze_rq2b_v7_i3_output_selection.py --verify`\n",
        encoding="utf-8",
    )


def verify() -> None:
    output = ROOT / OUTPUT
    require(output.is_dir(), "I3 selection freeze is missing")
    ledger_path = output / "selection_ledger.jsonl"
    report_path = output / "integrity_report.json"
    ledger = read_rows_bytes(ledger_path.read_bytes())
    report = json.loads(report_path.read_bytes())
    assignments = read_rows_bytes((ROOT / EXTRACTION_PREP / "fresh_assignment_manifest.jsonl").read_bytes())
    _, payloads = build_inputs(None)
    require(len(ledger) == len(assignments) == 35, "selection batch coverage mismatch")
    for assignment, row in zip(assignments, ledger, strict=True):
        require(row["batch_id"] == assignment["batch_id"], "selection batch order mismatch")
        input_name = str(Path(assignment["input_path"]).relative_to(CACHE))
        input_data = payloads[input_name]
        require(sha(input_data) == row["input_sha256"] == assignment["input_sha256"], "selection input drift")
        inputs = read_rows_bytes(input_data)
        require(row["attempts"] and sum(attempt["selected"] for attempt in row["attempts"]) == 1, "selection attempt mismatch")
        for attempt in row["attempts"]:
            path = ROOT / attempt["tracked_path"]
            data = path.read_bytes()
            require(sha(data) == attempt["sha256"], f"tracked attempt hash drift: {path}")
            require(attempt["raw_sha256"] == attempt["sha256"], f"tracked raw hash alias drift: {path}")
            if attempt["validator_status"] == "PASS":
                outputs = validate_attempt(inputs, data, row["batch_id"])
                require(
                    sha(canonical_semantic_rows_bytes(outputs)) == attempt["canonical_semantic_jsonl_sha256"],
                    f"tracked canonical semantic hash drift: {path}",
                )
                require(attempt["validator_error"] is None, "passing attempt has validator error")
            else:
                require(attempt["validator_status"] == "INVALID_PRESERVED_NOT_SELECTABLE" and attempt["validator_error"],
                        "invalid attempt disposition mismatch")
                require(attempt["canonical_semantic_jsonl_sha256"] is None,
                        "invalid attempt has canonical semantic hash")
        selected = next(attempt for attempt in row["attempts"] if attempt["selected"])
        require(selected["selected"] and selected["tracked_path"] == row["selected_output_path"], "selected path mismatch")
        require(
            selected["raw_sha256"] == row["selected_output_sha256"] == row["selected_output_raw_sha256"],
            "selected raw output hash mismatch",
        )
        require(
            selected["canonical_semantic_jsonl_sha256"]
            == row["selected_output_canonical_semantic_jsonl_sha256"],
            "selected canonical semantic output hash mismatch",
        )
        require(row["canonical_semantic_jsonl_serializer"] == CANONICAL_SEMANTIC_JSONL_SERIALIZER,
                "selected canonical serializer drift")
    require(report["bindings"]["selection_ledger_sha256"] == sha(ledger_path.read_bytes()), "selection ledger binding drift")
    require(report["counts"]["selected_rows"] == 1368, "selected row count mismatch")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        verify()
        status = "PASS_V7_I3_OUTPUT_SELECTION_REPLAY"
    else:
        create()
        status = "PASS_V7_I3_OUTPUT_SELECTION_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
