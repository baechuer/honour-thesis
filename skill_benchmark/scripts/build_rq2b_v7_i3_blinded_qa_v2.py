#!/usr/bin/env python3
"""Freeze the clarified V7 I3 blinded-QA calibration instrument (v2).

The 120-row source-only sample and cross-assignment are copied byte-for-byte
from v1.  V2 changes only the synthetic calibration cases and reviewer
guidance after v1 exposed internally inconsistent calibration expectations.
No benchmark prompt, label, acceptable set, or retrieval result is read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
PREP = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation"
V1 = PREP / "v7_phase7_i3_blinded_qa_2026_09_08_v1"
OUTPUT = PREP / "v7_phase7_i3_blinded_qa_2026_09_09_v2"
COPIED_FILES = (
    "blinded_reviewer_packet.jsonl",
    "sampling_key_do_not_give_reviewer.jsonl",
    "review_slots/qa_slot_01.jsonl",
    "review_slots/qa_slot_02.jsonl",
    "review_slots/qa_slot_03.jsonl",
    "review_slots/qa_slot_04.jsonl",
    "review_slots/qa_slot_05.jsonl",
    "review_slots/qa_slot_06.jsonl",
    "reviewer_return_schema.json",
)
FIELD_KEYS = (
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "constraints_boundaries",
    "dependencies_resources",
    "success_criteria",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def calibration() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    def empty() -> dict[str, list[dict[str, str]]]:
        return {field: [] for field in FIELD_KEYS}

    cases = [
        {
            "source": "Use when processing born-digital PDFs.",
            "field": "use_conditions",
            "evidence": "Use when processing born-digital PDFs.",
            "critical": False,
            "major": False,
            "affected": [],
            "codes": [],
        },
        {
            "source": "Input: a .proto schema.",
            "field": "output_artifacts",
            "evidence": "Input: a .proto schema.",
            "critical": False,
            "major": True,
            "affected": ["output_artifacts"],
            "codes": ["WRONG_OPERATIONAL_FIELD"],
        },
        {
            "source": "Do not use for scanned PDFs.",
            "field": "workflow_steps",
            "evidence": "Do not use for scanned PDFs.",
            "critical": False,
            "major": True,
            "affected": ["workflow_steps"],
            "codes": ["BOUNDARY_POLARITY_MISCLASSIFIED"],
        },
        {
            "source": "Use when reconciling payment disputes.",
            "field": "use_conditions",
            "evidence": "The user needs help.",
            "critical": True,
            "major": False,
            "affected": ["use_conditions"],
            "codes": ["EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING"],
        },
        {
            "source": "Requires the GitHub API and a token.",
            "field": "dependencies_resources",
            "evidence": "Requires the GitHub API and a token.",
            "critical": False,
            "major": False,
            "affected": [],
            "codes": [],
        },
        {
            "source": "Use when normalising DOCX citations.\nNormalize citation punctuation.",
            "field": "workflow_steps",
            "evidence": "Normalize citation punctuation.",
            "critical": False,
            "major": True,
            "affected": ["use_conditions"],
            "codes": ["MISSING_SELECTION_CRITICAL_CONTENT"],
        },
        {
            "source": "Input: account ID and date range.",
            "field": "input_preconditions",
            "evidence": "Input:",
            "critical": False,
            "major": True,
            "affected": ["input_preconditions"],
            "codes": ["NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN"],
        },
        {
            "source": "Verify the exported archive opens successfully.",
            "field": "success_criteria",
            "evidence": "Verify the exported archive opens successfully.",
            "critical": False,
            "major": False,
            "affected": [],
            "codes": [],
        },
    ]
    fixtures: list[dict[str, Any]] = []
    answers: list[dict[str, Any]] = []
    for index, case in enumerate(cases, 1):
        fields = empty()
        fields[str(case["field"])] = [{
            "id": f"item_{index}",
            "evidence": case["evidence"],
            "evidence_status": "explicit",
        }]
        review_id = f"CAL2-{index:03d}"
        fixtures.append({
            "review_id": review_id,
            "source_text": case["source"],
            "native_selector_metadata": {"name": "Calibration", "description": ""},
            "selector_visible_evidence": fields,
        })
        answers.append({
            "review_id": review_id,
            "critical_error": case["critical"],
            "major_error": case["major"],
            "affected_fields": case["affected"],
            "error_codes": case["codes"],
        })
    return fixtures, answers


GUIDANCE = """# V7 blinded I1/I3 extraction-fidelity QA v2

Judge only whether native name/description plus the visible evidence faithfully preserve source information that could materially change skill selection. Do not judge any benchmark prompt, target, acceptable set, ranking, or result. Do not use network access.

The packet contains only evidence that the actual I3C/I3-flat serializers retain. A heading or duplicate already omitted by the serializer is not visible and must not be scored. Do not demand exhaustive summarisation: report missing content only when the omitted source fact could distinguish the skill from a plausible neighbour and is not already fully carried by native name/description or another retained span.

Critical codes (critical=true, major=false):
- EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING
- BENCHMARK_OR_ROUTING_LEAKAGE

Major codes (critical=false, major=true), only when selection meaning materially changes:
- WRONG_OPERATIONAL_FIELD
- MISSING_SELECTION_CRITICAL_CONTENT
- NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN
- BOUNDARY_POLARITY_MISCLASSIFIED

Field rules: `dependencies_resources` is for packages, tools, APIs, files, credentials and external resources. `input_preconditions` is for task input/state a caller must supply. A prohibition/not-for statement belongs in `constraints_boundaries`, not workflow. Workflow evidence must itself express an operation; a bare heading or noun fragment is not self-contained.

Error-code precedence prevents double-counting one defect. Critical codes take precedence over majors. For the same visible span, use BOUNDARY_POLARITY_MISCLASSIFIED instead of WRONG_OPERATIONAL_FIELD; use NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN instead of also calling the same truncated span missing; use WRONG_OPERATIONAL_FIELD instead of also calling that same span missing from its destination field. MISSING_SELECTION_CRITICAL_CONTENT is for a distinct material fact that has no adequate visible carrier.

`affected_fields` names the current defective container for a retained bad/misplaced span. For genuinely missing content, name the destination field where the omitted fact belongs. Do not add both origin and destination merely because a span is misplaced.

Do not report a major for harmless overlap, formatting, an empty source-absent field, or information already fully carried by native name/description. Critical and major are mutually exclusive for a row. A clean row has both false and no codes. Notes must quote exact source evidence for every error and follow the precedence above.
"""


def build() -> dict[str, bytes]:
    v1_manifest_path = V1 / "manifest.json"
    v1_manifest = json.loads(v1_manifest_path.read_bytes())
    require(v1_manifest["state"] == "FROZEN_PENDING_THREE_CROSS_ASSIGNED_REVIEWER_GROUPS", "v1 QA packet state drift")
    files = {name: (V1 / name).read_bytes() for name in COPIED_FILES}
    for name in COPIED_FILES:
        expected = v1_manifest["artifacts"][name]["sha256"]
        require(sha(files[name]) == expected, f"v1 copied artifact drift: {name}")
    fixtures, answers = calibration()
    files["calibration_input.jsonl"] = rows_bytes(fixtures)
    files["calibration_answer_key_do_not_give_reviewer.jsonl"] = rows_bytes(answers)
    files["reviewer_guidance.md"] = GUIDANCE.encode()
    manifest = {
        "schema_version": "rq2b-v7-i3-blinded-qa-packet-v2",
        "state": "FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS",
        "formal_execution_ready": False,
        "sample_size": 120,
        "review_slots": 6,
        "rows_per_slot": 20,
        "calibration_rows": 8,
        "sample_disposition": "BYTE_IDENTICAL_TO_V1; v1 sample returns are invalid because calibration did not pass and are not selected",
        "reviewer_requirement": "fresh reviewer contexts; no access to v1 returns, hidden keys, labels, prompts, or results",
        "pass_rule": v1_manifest["pass_rule"],
        "counts": v1_manifest["counts"],
        "cross_assignment": v1_manifest["cross_assignment"],
        "calibration_change": {
            "threshold_changed": False,
            "reason": "v1 fixtures encoded contradictory or undefined expectations for missing content and affected_fields; v2 isolates one intended defect and freezes precedence",
            "error_code_precedence_frozen": True,
        },
        "bindings": {
            "v1_manifest_sha256": sha(v1_manifest_path.read_bytes()),
            "v1_blinded_packet_sha256": sha(files["blinded_reviewer_packet.jsonl"]),
            "v1_sampling_key_sha256": sha(files["sampling_key_do_not_give_reviewer.jsonl"]),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
    }
    manifest["artifacts"] = {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in files.items()}
    files["manifest.json"] = json_bytes(manifest)
    files["README.md"] = (
        "# V7 Phase-7 blinded I1/I3 QA v2\n\n"
        "V2 retains the exact 120-row v1 source-only sample and cross-assignment, but replaces the ambiguous synthetic calibration instrument with isolated cases, explicit error-code precedence and a defined `affected_fields` convention. The scientific threshold is unchanged. V1 returns remain preserved but are not accepted.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_blinded_qa_v2.py --verify`.\n"
    ).encode()
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.verify:
        require(OUTPUT.is_dir(), "v2 QA packet is missing")
        actual = {path.relative_to(OUTPUT) for path in OUTPUT.rglob("*") if path.is_file()}
        require(actual == {Path(name) for name in expected}, "v2 QA file-set drift")
        for name, data in expected.items():
            require((OUTPUT / name).read_bytes() == data, f"v2 QA artifact drift: {name}")
        status = "PASS_V7_I3_BLINDED_QA_V2_PACKET_REPLAY"
    else:
        require(not OUTPUT.exists(), "refusing to overwrite versioned v2 QA packet")
        for name, data in expected.items():
            path = OUTPUT / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_BLINDED_QA_V2_PACKET_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT.relative_to(ROOT))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
