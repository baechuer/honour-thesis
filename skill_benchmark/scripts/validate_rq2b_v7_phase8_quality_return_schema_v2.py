#!/usr/bin/env python3
"""Validate the prospective Phase-8 quality-return schema-envelope amendment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
V1_SCHEMA_PATH = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_review_dispatch_2026_09_09_v1/reviewer_return_schema.json"
)
V2_PACKAGE = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_review_return_schema_amendment_2026_09_09_v2"
)
V2_SCHEMA_PATH = V2_PACKAGE / "reviewer_return_schema_v2.json"
V1_SCHEMA_SHA256 = "d639fc02dae7aace52254533b1596f2a872212b21612b14881d8da5814a26723"
V2_SCHEMA_SHA256 = "30af0ae7a9067df460968974fd878ae1b57327e309071dab01f0341dd8182cc7"
OLD_PATTERN = r"^P8-(?:SPLIT-MIXED|PRREL|CUE|SRCREL)-[0-9]{4}$"
NEW_PATTERN = r"^P8-(?:SPLIT-MIXED|PRREL|CUE|SRCREL)-[0-9]{3,}$"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        require(bool(line), f"blank row: {path}:{number}")
        value = json.loads(line)
        require(isinstance(value, dict), f"non-object row: {path}:{number}")
        values.append(value)
    return values


def load_and_verify_schema_delta() -> tuple[dict[str, Any], dict[str, Any]]:
    require(file_sha256(V1_SCHEMA_PATH) == V1_SCHEMA_SHA256, "frozen v1 return schema hash drift")
    require(file_sha256(V2_SCHEMA_PATH) == V2_SCHEMA_SHA256, "prospective v2 return schema hash drift")
    v1 = read_json(V1_SCHEMA_PATH)
    v2 = read_json(V2_SCHEMA_PATH)
    require(v1["properties"]["packet_id"]["pattern"] == OLD_PATTERN, "unexpected v1 packet_id pattern")
    expected = copy.deepcopy(v1)
    expected["properties"]["packet_id"]["pattern"] = NEW_PATTERN
    require(v2 == expected, "schema amendment changes more than /properties/packet_id/pattern")
    require(
        v2["properties"]["schema_version"]["const"]
        == v1["properties"]["schema_version"]["const"],
        "payload schema_version changed",
    )
    return v1, v2


def validate_schema_row(row: dict[str, Any], schema: dict[str, Any], location: str) -> None:
    properties = schema["properties"]
    required = set(schema["required"])
    require(set(row) == required == set(properties), f"schema keys mismatch: {location}")
    require(row["schema_version"] == properties["schema_version"]["const"], f"schema_version mismatch: {location}")
    require(isinstance(row["packet_id"], str) and re.fullmatch(properties["packet_id"]["pattern"], row["packet_id"]) is not None, f"packet_id pattern mismatch: {location}")
    require(isinstance(row["packet_sha256"], str) and re.fullmatch(properties["packet_sha256"]["pattern"], row["packet_sha256"]) is not None, f"packet_sha256 mismatch: {location}")
    require(type(row["reviewer_group"]) is int and row["reviewer_group"] in properties["reviewer_group"]["enum"], f"reviewer_group mismatch: {location}")
    require(type(row["reviewer_slot"]) is int and row["reviewer_slot"] >= properties["reviewer_slot"]["minimum"], f"reviewer_slot mismatch: {location}")
    require(row["gate"] in properties["gate"]["enum"], f"gate mismatch: {location}")
    require(isinstance(row["decision"], str) and len(row["decision"]) >= properties["decision"]["minLength"], f"decision mismatch: {location}")
    require(isinstance(row["rationale"], str) and len(row["rationale"]) >= properties["rationale"]["minLength"], f"rationale mismatch: {location}")
    require(isinstance(row["source_anchors"], list) and all(isinstance(value, str) for value in row["source_anchors"]), f"source_anchors mismatch: {location}")


def validate_files(packet_path: Path, return_path: Path) -> dict[str, Any]:
    _, schema = load_and_verify_schema_delta()
    assignments = read_jsonl(packet_path)
    returns = read_jsonl(return_path)
    require(len(assignments) == len(returns), "packet/return row-count mismatch")
    split_ids: list[str] = []
    for index, (assignment, returned) in enumerate(zip(assignments, returns), 1):
        location = f"{return_path}:{index}"
        validate_schema_row(returned, schema, location)
        packet = assignment.get("packet")
        require(isinstance(packet, dict), f"assignment packet missing: {packet_path}:{index}")
        require(returned["packet_id"] == packet.get("packet_id"), f"packet identity mismatch: {location}")
        require(returned["packet_sha256"] == assignment.get("packet_sha256"), f"packet hash binding mismatch: {location}")
        require(returned["reviewer_group"] == assignment.get("reviewer_group"), f"reviewer_group binding mismatch: {location}")
        require(returned["reviewer_slot"] == assignment.get("reviewer_slot"), f"reviewer_slot binding mismatch: {location}")
        require(returned["gate"] == assignment.get("gate"), f"gate binding mismatch: {location}")
        allowed = assignment.get("allowed_decisions")
        require(isinstance(allowed, list) and returned["decision"] in allowed, f"decision outside assignment contract: {location}")
        if returned["packet_id"].startswith("P8-SPLIT-MIXED-"):
            split_ids.append(returned["packet_id"])
    return {
        "schema_artifact_version": "rq2b-v7-phase8-quality-review-return-schema-amendment-v2",
        "status": "SCHEMA_ENVELOPE_VALID",
        "quality_pass_authorized": False,
        "rows": len(returns),
        "split_packet_ids": split_ids,
        "packet_path": str(packet_path),
        "packet_sha256": file_sha256(packet_path),
        "return_path": str(return_path),
        "return_sha256": file_sha256(return_path),
        "v1_schema_sha256": V1_SCHEMA_SHA256,
        "v2_schema_sha256": V2_SCHEMA_SHA256,
        "changed_json_pointers": ["/properties/packet_id/pattern"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-path", required=True, type=Path)
    parser.add_argument("--return-path", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(validate_files(args.packet_path, args.return_path), sort_keys=True))


if __name__ == "__main__":
    main()
