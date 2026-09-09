#!/usr/bin/env python3
"""Focused no-provider tests for the Phase-8 return-schema amendment."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_rq2b_v7_phase8_quality_return_schema_v2.py")
SPEC = importlib.util.spec_from_file_location("quality_return_schema_v2", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)

DISPATCH = validator.ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_quality_review_dispatch_2026_09_09_v1"
)
PACKET = DISPATCH / "reviewer_group_2_slot_006_packet.jsonl"
RETURN = DISPATCH / "returns/reviewer_group_2_slot_006_return.jsonl"


class QualityReturnSchemaAmendmentTests(unittest.TestCase):
    def test_only_packet_id_pattern_changes(self) -> None:
        v1, v2 = validator.load_and_verify_schema_delta()
        expected = copy.deepcopy(v1)
        expected["properties"]["packet_id"]["pattern"] = validator.NEW_PATTERN
        self.assertEqual(v2, expected)
        self.assertEqual(
            v1["properties"]["schema_version"]["const"],
            v2["properties"]["schema_version"]["const"],
        )

    def test_existing_packet_id_families_and_lengths(self) -> None:
        _, v2 = validator.load_and_verify_schema_delta()
        pattern = v2["properties"]["packet_id"]["pattern"]
        for packet_id in (
            "P8-SPLIT-MIXED-003",
            "P8-PRREL-0002",
            "P8-CUE-0002",
            "P8-SRCREL-0003",
            "P8-CUE-10000",
        ):
            self.assertIsNotNone(re.fullmatch(pattern, packet_id), packet_id)
        for packet_id in (
            "P8-SPLIT-MIXED-03",
            "P8-OTHER-0001",
            "p8-CUE-0002",
            "P8-CUE-00A2",
        ):
            self.assertIsNone(re.fullmatch(pattern, packet_id), packet_id)

    def test_v1_rejects_and_v2_accepts_frozen_split_ids(self) -> None:
        v1, v2 = validator.load_and_verify_schema_delta()
        old_pattern = v1["properties"]["packet_id"]["pattern"]
        new_pattern = v2["properties"]["packet_id"]["pattern"]
        for packet_id in ("P8-SPLIT-MIXED-003", "P8-SPLIT-MIXED-004", "P8-SPLIT-MIXED-005"):
            self.assertIsNone(re.fullmatch(old_pattern, packet_id))
            self.assertIsNotNone(re.fullmatch(new_pattern, packet_id))

    def test_frozen_group2_slot6_validates_without_quality_pass(self) -> None:
        receipt = validator.validate_files(PACKET, RETURN)
        self.assertEqual(receipt["status"], "SCHEMA_ENVELOPE_VALID")
        self.assertFalse(receipt["quality_pass_authorized"])
        self.assertEqual(receipt["rows"], 24)
        self.assertEqual(
            receipt["split_packet_ids"],
            ["P8-SPLIT-MIXED-003", "P8-SPLIT-MIXED-004", "P8-SPLIT-MIXED-005"],
        )

    def test_identity_mismatch_still_fails_closed(self) -> None:
        assignments = validator.read_jsonl(PACKET)
        returns = validator.read_jsonl(RETURN)
        assignments = assignments[:1]
        returns = returns[:1]
        returns[0]["packet_id"] = "P8-CUE-9999"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet_path = root / "packet.jsonl"
            return_path = root / "return.jsonl"
            packet_path.write_text(json.dumps(assignments[0], sort_keys=True) + "\n", encoding="utf-8")
            return_path.write_text(json.dumps(returns[0], sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "packet identity mismatch"):
                validator.validate_files(packet_path, return_path)


if __name__ == "__main__":
    unittest.main()
