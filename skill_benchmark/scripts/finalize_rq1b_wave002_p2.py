#!/usr/bin/env python3
"""Validate and summarise local Wave 002 P2 blinded-review responses.

The script treats only acceptable-set agreement as a P2 adjudication trigger,
as required by the codebook. It retains stricter non-acceptable label
differences and reviewer cue flags for later P3 curation.
"""

from __future__ import annotations

import json
import argparse
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication/review/wave_002")
INPUT = ROOT / "blind_review_response_manifest.json"
OUTPUT = ROOT / "p2_acceptable_set_consensus.json"
LABELS = {"acceptable", "plausible_but_insufficient", "not_acceptable"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    responses = json.loads(args.input.read_text())
    roles = {row["role"]: row for row in responses["reviewer_responses"]}
    if len(roles) < 2:
        raise ValueError("at least two reviewer roles are required")

    packet_roles: dict[str, list[str]] = {}
    for role, reviewer in roles.items():
        assigned = reviewer["assigned_packets"]
        if set(assigned) != set(reviewer["responses"]):
            raise ValueError(f"{role} assigned and response packet sets differ")
        for packet_id, response in reviewer["responses"].items():
            if response["tasks"] != ["A", "B"]:
                raise ValueError(f"{role} {packet_id} must cover both prompt variants")
            labels = response["labels"]
            if set(labels) != {"A", "B"} or set(labels.values()) - LABELS:
                raise ValueError(f"{role} {packet_id} has invalid artifact labels")
            computed = sorted(artifact for artifact, label in labels.items() if label == "acceptable")
            if computed != sorted(response["acceptable_set"]):
                raise ValueError(f"{role} {packet_id} acceptable set conflicts with labels")
            packet_roles.setdefault(packet_id, []).append(role)

    if not packet_roles or any(len(value) != 2 for value in packet_roles.values()):
        raise ValueError("every reviewed packet must have exactly two independent reviews")

    consensus = []
    cue_flags = []
    for packet_id in sorted(packet_roles):
        first_role, second_role = sorted(packet_roles[packet_id])
        first = roles[first_role]["responses"][packet_id]
        second = roles[second_role]["responses"][packet_id]
        acceptable_set_agreement = sorted(first["acceptable_set"]) == sorted(second["acceptable_set"])
        label_differences = {
            artifact: [first["labels"][artifact], second["labels"][artifact]]
            for artifact in ("A", "B")
            if first["labels"][artifact] != second["labels"][artifact]
        }
        flags = [
            {"reviewer": role, "flag": flag}
            for role, response in ((first_role, first), (second_role, second))
            for flag in response.get("flags", [])
        ]
        cue_flags.extend({"packet_id": packet_id, **flag} for flag in flags)
        for task in ("A", "B"):
            consensus.append({
                "packet_id": packet_id,
                "task": task,
                "reviewer_roles": [first_role, second_role],
                "acceptable_set_by_reviewer": {
                    first_role: first["acceptable_set"],
                    second_role: second["acceptable_set"],
                },
                "acceptable_set_agreement": acceptable_set_agreement,
                "adjudication_required": not acceptable_set_agreement,
                "adjudicated_acceptable_set": first["acceptable_set"] if acceptable_set_agreement else None,
                "nonacceptable_label_differences": label_differences,
                "reviewer_flags": flags,
            })

    summary = {
        "status": "P2_ACCEPTABLE_SET_CONSENSUS_COMPLETE_NOT_P3_REVIEWED_NOT_VALID",
        "boundary": "Model-assisted blinded curation only; not human annotation, retrieval, or external-model evidence.",
        "packet_count": len(packet_roles),
        "prompt_count": len(consensus),
        "independent_reviewer_task_rows": 2 * len(consensus),
        "acceptable_set_agreement_count": sum(row["acceptable_set_agreement"] for row in consensus),
        "adjudication_required_count": sum(row["adjudication_required"] for row in consensus),
        "agreed_singleton_prompt_count": sum(
            row["acceptable_set_agreement"] and len(row["adjudicated_acceptable_set"] or []) == 1
            for row in consensus
        ),
        "nonacceptable_label_difference_prompt_count": sum(
            bool(row["nonacceptable_label_differences"]) for row in consensus
        ),
        "reviewer_flag_count": len(cue_flags),
        "reviewer_flags": cue_flags,
        "consensus": consensus,
    }
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: summary[key] for key in summary if key.endswith("count")}, indent=2))
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
