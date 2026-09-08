#!/usr/bin/env python3
"""Prepare/replay V7 I3 V4.1 inputs after the pre-output lexical-gate correction."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import prepare_rq2b_v7_i3_full_reextraction_v4 as v4


ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
OLD_PACKAGE = PREP / "v7_phase7_i3_full_reextraction_2026_09_09_v4"
OUTPUT = PREP / "v7_phase7_i3_full_reextraction_2026_09_09_v4_1"
CACHE = Path("skill_benchmark/cache/rq2b_v7_phase7_i3_full_reextraction_2026_09_09_v4_1")
INSTRUCTION = Path("skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V4_1.md")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def build() -> tuple[dict[str, bytes], dict[str, bytes]]:
    old_files, old_payloads = v4.build()
    old_report_bytes = (ROOT / OLD_PACKAGE / "preparation_report.json").read_bytes()
    if old_files["preparation_report.json"] != old_report_bytes:
        raise ValueError("superseded V4 preparation drift")
    assignments = [json.loads(line) for line in old_files["full_reextraction_assignment_manifest.jsonl"].splitlines()]
    instruction_hash = sha((ROOT / INSTRUCTION).read_bytes())
    for assignment in assignments:
        number = assignment["batch_id"].removeprefix("I3V4-")
        assignment["batch_id"] = "I3V41-" + number
        assignment["input_path"] = str(CACHE / f"inputs/i3v41_input_{number}.jsonl")
        assignment["expected_output_path"] = str(CACHE / f"outputs/i3v41_output_{number}.jsonl")
        assignment["instruction_path"] = str(INSTRUCTION)
        assignment["instruction_sha256"] = instruction_hash
        assignment["state"] = "UNSTARTED"
    if len(assignments) != 95 or sum(row["row_count"] for row in assignments) != 3798:
        raise ValueError("V4.1 assignment coverage mismatch")
    payloads = {}
    for old_name, data in old_payloads.items():
        number = Path(old_name).stem.removeprefix("i3v4_input_")
        payloads[f"inputs/i3v41_input_{number}.jsonl"] = data
    if len(payloads) != 95 or sha(b"".join(payloads[name] for name in sorted(payloads))) != "63eeb7503a2e76fc3ce03c9a0b3d644e264020057d04d7c9c952a950691f176a":
        raise ValueError("V4.1 input-byte preservation mismatch")
    assignment_data = rows_bytes(assignments)
    old_report = json.loads(old_report_bytes)
    report = {
        "schema_version": "rq2b-v7-phase7-i3-full-reextraction-preparation-v4.1",
        "state": "PENDING_3798_SOURCE_ONLY_V4_1_EXTRACTIONS",
        "formal_execution_ready": False,
        "network_calls": 0,
        "selector_runs": 0,
        "counts": old_report["counts"],
        "bindings": {
            **{key: value for key, value in old_report["bindings"].items() if key != "instruction_sha256" and key != "builder_sha256"},
            "superseded_v4_preparation_report_sha256": sha(old_report_bytes),
            "instruction_sha256": instruction_hash,
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "tracked_artifacts": {"full_reextraction_assignment_manifest.jsonl": {"sha256": sha(assignment_data), "rows": 95}},
        "local_inputs": {"rows": 3798, "batches": 95, "aggregate_sha256": sha(b"".join(payloads[name] for name in sorted(payloads)))},
        "change_from_v4": "Pre-output implementation correction only: metadata-key rejection is restricted to structurally identified candidate frontmatter, and clear not-for/use-prohibition language is distinguished from grammatical negation describing an input state.",
        "unchanged": ["3798 source bytes and identities", "same seven fields", "same 95 batch membership and extractor groups", "V7 prompts and K=6 packets", "labels and acceptable sets", "fresh QA thresholds"],
        "completion_gates": old_report["completion_gates"],
    }
    files = {
        "full_reextraction_assignment_manifest.jsonl": assignment_data,
        "preparation_report.json": json_bytes(report),
        "README.md": (
            "# V7 Phase-7 I3 full re-extraction V4.1\n\n"
            "State: `PENDING_3798_SOURCE_ONLY_V4_1_EXTRACTIONS`. V4 was superseded before any worker output. V4.1 changes only false-positive safeguards for source-internal task language; all 3,798 source bytes, identities, seven fields, 95 batch memberships, V7 prompts, K=6 packets, labels and QA thresholds are unchanged.\n\n"
            "Workers read only their assigned `i3v41_input_NNN.jsonl` and `I3C_SUBAGENT_EXTRACTION_V4_1.md`. Replay: `python3 -B skill_benchmark/scripts/prepare_rq2b_v7_i3_full_reextraction_v4_1.py --verify`.\n"
        ).encode(),
    }
    return files, payloads


def require_equal(path: Path, data: bytes) -> None:
    if path.read_bytes() != data:
        raise ValueError(f"artifact drift: {path}")


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    files, payloads = build()
    if args.verify:
        for name, data in files.items():
            require_equal(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            require_equal(ROOT / CACHE / name, data)
        status = "PASS_V7_I3_V4_1_FULL_REEXTRACTION_PREPARATION_REPLAY"
    else:
        if (ROOT / OUTPUT).exists() or (ROOT / CACHE).exists():
            raise FileExistsError("refusing to overwrite V4.1 re-extraction preparation")
        for name, data in files.items():
            write_new(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            write_new(ROOT / CACHE / name, data)
        status = "PASS_V7_I3_V4_1_FULL_REEXTRACTION_PREPARATION_CREATED"
    print(json.dumps({"status": status, "sources": 3798, "batches": 95}, sort_keys=True))


if __name__ == "__main__":
    main()
