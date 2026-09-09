#!/usr/bin/env python3
"""Create two independent target-blind reviews for every Phase-8 quality packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_review_docket_2026_09_09_v3"
)
OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_review_dispatch_2026_09_09_v1"
)
BUILDER_VERSION = "rq2b-v7-phase8-quality-review-dispatch-builder-v1"
ASSIGNMENT_SCHEMA = "rq2b-v7-phase8-quality-review-assignment-v1"
RETURN_SCHEMA = "rq2b-v7-phase8-quality-review-return-v1"
SOURCE_PACKET_SCHEMA = "rq2b-v7-phase8-target-blind-quality-review-packet-v3"
SLOT_SIZE = 24
SOURCE_FILES = {
    "mixed_lane_split_review_packets.jsonl": 6,
    "prompt_relation_review_packets.jsonl": 51,
    "cue_review_packets.jsonl": 129,
    "source_relation_review_packets.jsonl": 55,
}
SOURCE_SHA256 = {
    "mixed_lane_split_review_packets.jsonl": "deb28633c40e01090baea1c84735695a211e424714879ef69865795f3e947ffc",
    "prompt_relation_review_packets.jsonl": "6cc051b58f5ffd8e5013f6aff1adc11a3b32c95ef512546bfa456739b92df8cd",
    "cue_review_packets.jsonl": "d16d255fd49ff07833ffad1918afdd2ffa76b0218fe682a702f1b4eb28ffdb94",
    "source_relation_review_packets.jsonl": "fd7bf3b85fc727990881d35a6995806924b722ee1deb6036011cab02dd2b2107",
}
PAIR_CYCLE = ((1, 2), (1, 3), (2, 3))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def rows_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(value) for value in values)


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    result = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        require(bool(line), f"blank row: {path}:{number}")
        value = json.loads(line)
        require(isinstance(value, dict), f"non-object row: {path}:{number}")
        result.append(value)
    return result


def source_gate(filename: str, row: dict[str, Any]) -> str:
    if filename == "source_relation_review_packets.jsonl":
        require(row.get("gates") == ["duplication", "semantic_near_copy"], "source gate drift")
        return "source_relation"
    gate = row.get("gate")
    require(gate in {"split", "semantic_near_copy", "cue"}, "packet gate drift")
    return str(gate)


def allowed_decisions(row: dict[str, Any]) -> list[str]:
    value = row.get("required_return", {}).get("decision")
    require(isinstance(value, str), "packet decision contract missing")
    decisions = value.split(" | ")
    require(len(decisions) >= 3 and len(decisions) == len(set(decisions)), "packet decision contract drift")
    return decisions


def build(root: Path = ROOT) -> dict[str, bytes]:
    source_root = root / SOURCE
    require(source_root.is_dir(), "quality docket v3 missing")
    all_rows: list[dict[str, Any]] = []
    source_bindings: dict[str, Any] = {}
    packet_ids: set[str] = set()
    for filename, expected_rows in SOURCE_FILES.items():
        path = source_root / filename
        require(path.is_file(), f"missing quality packet file: {filename}")
        actual_sha = file_sha256(path)
        require(actual_sha == SOURCE_SHA256[filename], f"quality packet hash drift: {filename}")
        values = read_jsonl(path)
        require(len(values) == expected_rows, f"quality packet row drift: {filename}")
        for row in values:
            require(row.get("schema_version") == SOURCE_PACKET_SCHEMA, "source packet schema drift")
            packet_id = row.get("packet_id")
            require(isinstance(packet_id, str) and packet_id not in packet_ids, "packet identity drift")
            packet_ids.add(packet_id)
            all_rows.append({
                "source_packet_file": str(SOURCE / filename),
                "source_packet_file_sha256": actual_sha,
                "packet_sha256": canonical_sha256(row),
                "gate": source_gate(filename, row),
                "allowed_decisions": allowed_decisions(row),
                "packet": row,
            })
        source_bindings[filename] = {"rows": len(values), "sha256": actual_sha}
    require(len(all_rows) == len(packet_ids) == 241, "quality packet union drift")

    ordered = sorted(all_rows, key=lambda item: (hashlib.sha256(item["packet"]["packet_id"].encode()).hexdigest(), item["packet"]["packet_id"]))
    assigned: dict[int, list[dict[str, Any]]] = {1: [], 2: [], 3: []}
    pair_counts: Counter[str] = Counter()
    for index, item in enumerate(ordered):
        pair = PAIR_CYCLE[index % len(PAIR_CYCLE)]
        pair_counts[f"{pair[0]}+{pair[1]}"] += 1
        for reviewer_group in pair:
            assigned[reviewer_group].append({**item, "reviewer_group": reviewer_group})

    payloads: dict[str, bytes] = {}
    slot_counts: dict[str, int] = {}
    for reviewer_group, values in assigned.items():
        values.sort(key=lambda item: item["packet"]["packet_id"])
        for index, item in enumerate(values):
            item["reviewer_slot"] = index // SLOT_SIZE + 1
            item["schema_version"] = ASSIGNMENT_SCHEMA
        slots = sorted({item["reviewer_slot"] for item in values})
        for slot in slots:
            packet_rows = [item for item in values if item["reviewer_slot"] == slot]
            prefix = f"reviewer_group_{reviewer_group}_slot_{slot:03d}"
            payloads[f"{prefix}_packet.jsonl"] = rows_bytes(packet_rows)
            returns = [{
                "schema_version": RETURN_SCHEMA,
                "packet_id": item["packet"]["packet_id"],
                "packet_sha256": item["packet_sha256"],
                "reviewer_group": reviewer_group,
                "reviewer_slot": slot,
                "gate": item["gate"],
                "decision": "PENDING",
                "source_anchors": [],
                "rationale": "",
            } for item in packet_rows]
            payloads[f"{prefix}_return_template.jsonl"] = rows_bytes(returns)
            slot_counts[f"{reviewer_group}:{slot:03d}"] = len(packet_rows)

    return_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "packet_id", "packet_sha256", "reviewer_group", "reviewer_slot", "gate", "decision", "source_anchors", "rationale"],
        "properties": {
            "schema_version": {"const": RETURN_SCHEMA},
            "packet_id": {"type": "string", "pattern": "^P8-(?:SPLIT-MIXED|PRREL|CUE|SRCREL)-[0-9]{4}$"},
            "packet_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "reviewer_group": {"type": "integer", "enum": [1, 2, 3]},
            "reviewer_slot": {"type": "integer", "minimum": 1},
            "gate": {"enum": ["split", "semantic_near_copy", "cue", "source_relation"]},
            "decision": {"type": "string", "minLength": 1},
            "source_anchors": {"type": "array", "items": {"type": "string"}},
            "rationale": {"type": "string", "minLength": 1},
        },
    }
    payloads["reviewer_return_schema.json"] = json_bytes(return_schema)
    report = {
        "schema_version": "rq2b-v7-phase8-quality-review-dispatch-integrity-v1",
        "state": "FROZEN_PENDING_TWO_INDEPENDENT_TARGET_BLIND_RETURNS_PER_PACKET",
        "formal_execution_ready": False,
        "counts": {
            "unique_packets": len(ordered),
            "review_assignments": sum(map(len, assigned.values())),
            "reviewer_groups": {str(group): len(values) for group, values in assigned.items()},
            "pair_counts": dict(sorted(pair_counts.items())),
            "slots": slot_counts,
        },
        "assertions": {
            "each_packet_has_exactly_two_distinct_reviewers": all(sum(item["packet"]["packet_id"] in {row["packet"]["packet_id"] for row in values} for values in assigned.values()) == 2 for item in ordered),
            "target_blind_source_packets_preserved": True,
            "reviewers_must_not_read_other_returns": True,
            "disagreements_or_unclear_require_sealed_coordinator": True,
        },
        "bindings": {"source_packet_files": source_bindings, "reviewer_return_schema_sha256": hashlib.sha256(payloads["reviewer_return_schema.json"]).hexdigest(), "builder_sha256": file_sha256(Path(__file__))},
        "boundary": "Dispatch contains source/prompt-only quality packets and no labels, targets, acceptable sets, retrieval outputs, metrics, or execution authority.",
    }
    payloads["integrity_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 Phase-8 quality review dispatch v1\n\n"
        "Every one of the 241 target-blind quality packets is assigned to exactly two distinct reviewer groups. "
        "The deterministic pair cycle yields 482 assignments: groups 1 and 2 receive 161 each, group 3 receives 160. "
        "Reviewers may read only their packet slots, this README, and the return schema; they must not inspect other reviewer returns, benchmark labels, acceptable sets, retrieval outputs, or metrics.\n\n"
        "For each row, choose exactly one decision from `allowed_decisions`, cite only visible source/prompt anchors, and give a specific rationale. "
        "Any `BLOCKED_OR_UNCLEAR` or reviewer disagreement goes to a sealed coordinator. A return does not itself create a quality PASS or authorise an experiment.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_review_dispatch.py --verify`.\n"
    ).encode()
    return payloads


def verify(root: Path = ROOT) -> None:
    output = root / OUTPUT
    require(output.is_dir(), "quality review dispatch missing")
    expected = build(root)
    actual = {path.name for path in output.iterdir() if path.is_file()}
    require(actual == set(expected), "quality dispatch file-set drift")
    for name, data in expected.items():
        require((output / name).read_bytes() == data, f"quality dispatch artifact drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_PHASE8_QUALITY_REVIEW_DISPATCH_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite quality review dispatch")
        expected = build()
        staging = output.parent / f".{output.name}.staging-{os.getpid()}"
        require(not staging.exists(), "stale quality dispatch staging directory")
        staging.mkdir(parents=True)
        for name, data in expected.items():
            (staging / name).write_bytes(data)
        staging.rename(output)
        status = "PASS_V7_PHASE8_QUALITY_REVIEW_DISPATCH_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
