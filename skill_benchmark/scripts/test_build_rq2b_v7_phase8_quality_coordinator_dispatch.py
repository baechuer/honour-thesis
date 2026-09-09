#!/usr/bin/env python3
"""Focused checks for the sealed Phase-8 quality coordinator dispatch."""
from __future__ import annotations

import json
import unittest

from build_rq2b_v7_phase8_quality_coordinator_dispatch import build, scan_forbidden_keys


class CoordinatorDispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payloads = build()
        cls.groups = {
            group: [json.loads(line) for line in cls.payloads[f"coordinator_group_{group}_packet.jsonl"].splitlines()]
            for group in (1, 2, 3)
        }

    def test_counts_disjointness_and_coverage(self) -> None:
        self.assertEqual([len(self.groups[group]) for group in (1, 2, 3)], [37, 36, 36])
        ids = [{row["packet_id"] for row in self.groups[group]} for group in (1, 2, 3)]
        self.assertFalse(ids[0] & ids[1] or ids[0] & ids[2] or ids[1] & ids[2])
        self.assertEqual(len(set.union(*ids)), 109)

    def test_sealed_payload_has_no_outcome_or_label_keys(self) -> None:
        self.assertEqual(scan_forbidden_keys(self.groups), [])

    def test_required_returns_are_pending_and_bound(self) -> None:
        for rows in self.groups.values():
            for row in rows:
                self.assertEqual(row["required_return"]["decision"], "PENDING")
                self.assertEqual(row["required_return"]["packet_id"], row["packet_id"])
                self.assertIn(row["sealed_packet"]["required_return"]["decision"], ("PENDING",))


if __name__ == "__main__":
    unittest.main()
