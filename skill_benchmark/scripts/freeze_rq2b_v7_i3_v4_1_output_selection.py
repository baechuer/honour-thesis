#!/usr/bin/env python3
"""Freeze and select one mechanically valid V4.1 output per extraction batch."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from merge_rq2b_i3c import canonical_extraction
from prepare_rq2b_v7_i3_full_reextraction_v4_1 import CACHE, build as build_inputs
from validate_rq2b_v7_i3_v4_1_1_batch import PREP, ROOT, validate_v4_1_1_semantics


OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_output_selection_2026_09_09_v1")


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


def attempt_paths(number: str) -> list[Path]:
    original = ROOT / CACHE / f"outputs/i3v41_output_{number}.jsonl"
    require(original.is_file(), f"original V4.1 output missing: {number}")
    reissues = sorted((ROOT / CACHE / "reissues").glob(f"i3v41_output_{number}_reissue_*.jsonl"))
    return [original, *reissues]


def reconstructed_input(assignment: dict, input_payloads: dict[str, bytes]) -> bytes:
    name = str(Path(assignment["input_path"]).relative_to(CACHE))
    data = input_payloads[name]
    require(sha(data) == assignment["input_sha256"], f"V4.1 reconstructed input drift: {assignment['batch_id']}")
    return data


def validate_attempt(assignment: dict, data: bytes, input_payloads: dict[str, bytes]) -> dict:
    input_rows = rows(reconstructed_input(assignment, input_payloads))
    output_rows = rows(data)
    require(len(input_rows) == len(output_rows) == assignment["row_count"], f"V4.1 attempt row mismatch: {assignment['batch_id']}")
    items = warnings = 0
    for input_row, output_row in zip(input_rows, output_rows, strict=True):
        canonical_extraction(input_row, output_row)
        row_items, row_warnings = validate_v4_1_1_semantics(input_row, output_row)
        items += row_items
        warnings += row_warnings
    return {"rows": len(output_rows), "items": items, "warnings_pending_source_only_disposition": warnings}


def build() -> dict[str, bytes]:
    assignments_path = ROOT / PREP / "full_reextraction_assignment_manifest.jsonl"
    assignments = rows(assignments_path.read_bytes())
    require(len(assignments) == 95, "V4.1 selection requires exactly 95 assignments")
    require(sum(row["row_count"] for row in assignments) == 3798, "V4.1 selection requires exactly 3,798 rows")
    require(len({row["batch_id"] for row in assignments}) == 95, "duplicate V4.1 assignment batch ID")
    _, input_payloads = build_inputs()
    payloads: dict[str, bytes] = {}
    ledger: list[dict] = []
    for assignment in assignments:
        batch_id = assignment["batch_id"]
        number = batch_id.removeprefix("I3V41-")
        attempts = []
        for attempt_number, path in enumerate(attempt_paths(number), 1):
            data = path.read_bytes()
            try:
                result = validate_attempt(assignment, data, input_payloads)
                status, error = "PASS", None
            except Exception as exc:
                result = None
                status, error = "INVALID_PRESERVED_NOT_SELECTABLE", f"{type(exc).__name__}: {exc}"
            tracked = Path("attempts") / batch_id / f"attempt_{attempt_number:03d}.jsonl"
            payloads[str(tracked)] = data
            match = re.fullmatch(rf"i3v41_output_{number}_reissue_(\d{{3}})\.jsonl", path.name)
            attempts.append({
                "attempt_number": attempt_number,
                "attempt_kind": "ORIGINAL" if attempt_number == 1 else "TRACEABLE_REISSUE" if match else "NONCANONICAL_ATTEMPT",
                "local_source_path": str(path.relative_to(ROOT)),
                "tracked_path": str(OUTPUT / tracked),
                "sha256": sha(data),
                "rows": assignment["row_count"],
                "validator_status": status,
                "validator_error": error,
                "selected": False,
                "reissue_number": int(match.group(1)) if match else None,
                "validator_summary": result,
            })
        selectable = [
            row for row in attempts
            if row["validator_status"] == "PASS" and row["attempt_kind"] in {"ORIGINAL", "TRACEABLE_REISSUE"}
        ]
        require(selectable, f"no valid V4.1 attempt: {batch_id}")
        selected = max(selectable, key=lambda row: -1 if row["reissue_number"] is None else row["reissue_number"])
        selected["selected"] = True
        ledger.append({
            "schema_version": "rq2b-v7-i3-v4.1-output-selection-v1",
            "batch_id": batch_id,
            "input_sha256": assignment["input_sha256"],
            "row_count": assignment["row_count"],
            "attempts": attempts,
            "selected_attempt_number": selected["attempt_number"],
            "selected_output_path": selected["tracked_path"],
            "selected_output_sha256": selected["sha256"],
            "selection_rule": "HIGHEST_VALID_THREE_DIGIT_TRACEABLE_REISSUE_ELSE_ORIGINAL",
        })
    ledger_data = rows_bytes(ledger)
    report = {
        "schema_version": "rq2b-v7-i3-v4.1-output-selection-report-v1",
        "state": "PASS_95_BATCHES_SELECTED_PENDING_MERGE_AND_FRESH_BLINDED_QA",
        "formal_execution_ready": False,
        "counts": {
            "batches": len(ledger),
            "rows": sum(row["row_count"] for row in ledger),
            "attempts": sum(len(row["attempts"]) for row in ledger),
            "selected_reissues": sum(any(attempt["selected"] and attempt["attempt_kind"] == "TRACEABLE_REISSUE" for attempt in row["attempts"]) for row in ledger),
        },
        "bindings": {
            "assignment_manifest_sha256": sha(assignments_path.read_bytes()),
            "selection_ledger_sha256": sha(ledger_data),
            "builder_sha256": sha(Path(__file__).read_bytes()),
            "validator_sha256": sha((Path(__file__).parent / "validate_rq2b_v7_i3_v4_1_1_batch.py").read_bytes()),
            "validator_base_sha256": sha((Path(__file__).parent / "validate_rq2b_v7_i3_v4_1_batch.py").read_bytes()),
            "canonicalizer_sha256": sha((Path(__file__).parent / "merge_rq2b_i3c.py").read_bytes()),
            "input_builder_sha256": sha((Path(__file__).parent / "prepare_rq2b_v7_i3_full_reextraction_v4_1.py").read_bytes()),
        },
        "boundary": "Selection is mechanical provenance only. It is not semantic QA and does not authorise selectors.",
    }
    payloads["selection_ledger.jsonl"] = ledger_data
    payloads["integrity_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 I3 V4.1 output selection\n\n"
        "All attempts are preserved. The highest mechanically valid traceable reissue is selected, otherwise the original. This package remains pending merge and a genuinely fresh blinded QA sample.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/freeze_rq2b_v7_i3_v4_1_output_selection.py --verify`.\n"
    ).encode()
    return payloads


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "V4.1 selection package missing")
    assignments_path = ROOT / PREP / "full_reextraction_assignment_manifest.jsonl"
    assignments = rows(assignments_path.read_bytes())
    ledger_path = root / "selection_ledger.jsonl"
    report_path = root / "integrity_report.json"
    ledger = rows(ledger_path.read_bytes())
    report = json.loads(report_path.read_bytes())
    require(len(assignments) == len(ledger) == report["counts"]["batches"] == 95, "V4.1 selection replay batch mismatch")
    require(sum(row["row_count"] for row in ledger) == report["counts"]["rows"] == 3798, "V4.1 selection replay row mismatch")
    require(report["state"] == "PASS_95_BATCHES_SELECTED_PENDING_MERGE_AND_FRESH_BLINDED_QA", "V4.1 selection state drift")
    require(report["bindings"]["assignment_manifest_sha256"] == sha(assignments_path.read_bytes()), "V4.1 assignment binding drift")
    require(report["bindings"]["selection_ledger_sha256"] == sha(ledger_path.read_bytes()), "V4.1 ledger binding drift")
    require(report["bindings"]["builder_sha256"] == sha(Path(__file__).read_bytes()), "V4.1 selection builder drift")
    require(report["bindings"]["validator_sha256"] == sha((Path(__file__).parent / "validate_rq2b_v7_i3_v4_1_1_batch.py").read_bytes()), "V4.1.1 validator drift")
    require(report["bindings"]["validator_base_sha256"] == sha((Path(__file__).parent / "validate_rq2b_v7_i3_v4_1_batch.py").read_bytes()), "V4.1 validator base drift")
    require(report["bindings"]["canonicalizer_sha256"] == sha((Path(__file__).parent / "merge_rq2b_i3c.py").read_bytes()), "V4.1 canonicalizer drift")
    require(report["bindings"]["input_builder_sha256"] == sha((Path(__file__).parent / "prepare_rq2b_v7_i3_full_reextraction_v4_1.py").read_bytes()), "V4.1 input builder drift")
    _, input_payloads = build_inputs()
    tracked_paths = set()
    for assignment, selection in zip(assignments, ledger, strict=True):
        require(selection["batch_id"] == assignment["batch_id"], "V4.1 selection order drift")
        require(selection["input_sha256"] == assignment["input_sha256"], "V4.1 selection input drift")
        require(sum(bool(row["selected"]) for row in selection["attempts"]) == 1, "V4.1 selected-attempt cardinality mismatch")
        selectable = []
        for attempt in selection["attempts"]:
            path = ROOT / attempt["tracked_path"]
            tracked_paths.add(str(path.relative_to(root)))
            data = path.read_bytes()
            require(sha(data) == attempt["sha256"], f"V4.1 tracked attempt drift: {path}")
            try:
                summary = validate_attempt(assignment, data, input_payloads)
                current_status, current_error = "PASS", None
            except Exception as exc:
                summary = None
                current_status, current_error = "INVALID_PRESERVED_NOT_SELECTABLE", f"{type(exc).__name__}: {exc}"
            require(current_status == attempt["validator_status"], "V4.1 attempt validator disposition drift")
            require(current_error == attempt["validator_error"], "V4.1 attempt validator error drift")
            if current_status == "PASS":
                require(summary == attempt["validator_summary"], "V4.1 passing attempt summary drift")
                if attempt["attempt_kind"] in {"ORIGINAL", "TRACEABLE_REISSUE"}:
                    selectable.append(attempt)
            else:
                require(attempt["validator_error"] and attempt["validator_summary"] is None, "V4.1 invalid attempt disposition drift")
        require(selectable, f"V4.1 no selectable replay attempt: {assignment['batch_id']}")
        expected = max(selectable, key=lambda row: -1 if row["reissue_number"] is None else row["reissue_number"])
        selected = next(row for row in selection["attempts"] if row["selected"])
        require(selected["attempt_number"] == expected["attempt_number"] == selection["selected_attempt_number"], "V4.1 latest-reissue selection drift")
        require(selected["tracked_path"] == selection["selected_output_path"] and selected["sha256"] == selection["selected_output_sha256"], "V4.1 selected output binding drift")
    actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
    require(actual == tracked_paths | {"selection_ledger.jsonl", "integrity_report.json", "README.md"}, "V4.1 selection file-set drift")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_I3_V4_1_OUTPUT_SELECTION_REPLAY"
    else:
        expected = build()
        require(not root.exists(), "refusing to overwrite V4.1 selection package")
        for name, data in expected.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_V4_1_OUTPUT_SELECTION_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
