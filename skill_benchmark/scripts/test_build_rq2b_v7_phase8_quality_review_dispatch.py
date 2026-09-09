#!/usr/bin/env python3
"""Focused tests for the target-blind Phase-8 quality review dispatch."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path


SCRIPT = Path(__file__).with_name("build_rq2b_v7_phase8_quality_review_dispatch.py")
SPEC = importlib.util.spec_from_file_location("quality_dispatch", SCRIPT)
assert SPEC and SPEC.loader
dispatch = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = dispatch
SPEC.loader.exec_module(dispatch)


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


class QualityDispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payloads = dispatch.build()
        cls.packet_rows = [
            row
            for name, data in cls.payloads.items()
            if name.endswith("_packet.jsonl")
            for row in rows(data)
        ]

    def test_exact_two_distinct_reviewers_per_packet(self) -> None:
        reviewers: dict[str, set[int]] = defaultdict(set)
        counts = Counter()
        for row in self.packet_rows:
            reviewers[row["packet"]["packet_id"]].add(row["reviewer_group"])
            counts[row["reviewer_group"]] += 1
        self.assertEqual(len(reviewers), 241)
        self.assertTrue(all(len(value) == 2 for value in reviewers.values()))
        self.assertEqual(counts, {1: 161, 2: 161, 3: 160})

    def test_packet_hash_and_allowed_decisions_are_bound(self) -> None:
        for row in self.packet_rows:
            self.assertEqual(row["schema_version"], dispatch.ASSIGNMENT_SCHEMA)
            self.assertEqual(row["packet_sha256"], dispatch.canonical_sha256(row["packet"]))
            expected = row["packet"]["required_return"]["decision"].split(" | ")
            self.assertEqual(row["allowed_decisions"], expected)

    def test_return_templates_cover_assignments(self) -> None:
        packet_ids = Counter(row["packet"]["packet_id"] for row in self.packet_rows)
        returned_ids = Counter()
        for name, data in self.payloads.items():
            if name.endswith("_return_template.jsonl"):
                for row in rows(data):
                    returned_ids[row["packet_id"]] += 1
                    self.assertEqual(row["decision"], "PENDING")
                    self.assertEqual(row["rationale"], "")
        self.assertEqual(packet_ids, returned_ids)

    def test_no_outcome_identity_keys_added(self) -> None:
        prohibited = {"target", "gold", "acceptable_set", "selector_result", "metric", "outcome"}
        def walk(value: object) -> None:
            if isinstance(value, dict):
                self.assertFalse(set(value) & prohibited)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(self.packet_rows)


if __name__ == "__main__":
    unittest.main()
