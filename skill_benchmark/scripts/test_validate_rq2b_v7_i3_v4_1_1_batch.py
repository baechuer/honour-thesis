#!/usr/bin/env python3
"""Focused tests for the V4.1.1 unsupported-label polarity correction."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_validate_rq2b_v7_i3_v4_1_batch import item, output  # noqa: E402
from validate_rq2b_v7_i3_v4_1_1_batch import validate_v4_1_1_semantics  # noqa: E402


class V411PolarityTest(unittest.TestCase):
    def test_unsupported_outcome_label_passes(self) -> None:
        evidence = "The task is a support check: decide whether the wording is supported, overstated, partially supported, or unsupported."
        input_row = {"skill_id": "sha256-test", "text": "---\nname: demo\n---\n" + evidence}
        self.assertEqual(validate_v4_1_1_semantics(input_row, output("use_conditions", item("use_1", evidence))), (1, 0))

    def test_unsupported_platform_route_out_rejected(self) -> None:
        evidence = "Do not use this workflow on an unsupported platform."
        input_row = {"skill_id": "sha256-test", "text": "---\nname: demo\n---\n" + evidence}
        with self.assertRaisesRegex(ValueError, "explicit not-for"):
            validate_v4_1_1_semantics(input_row, output("use_conditions", item("use_1", evidence)))

    def test_is_unsupported_route_out_rejected(self) -> None:
        evidence = "Use when the input format is unsupported."
        input_row = {"skill_id": "sha256-test", "text": "---\nname: demo\n---\n" + evidence}
        with self.assertRaisesRegex(ValueError, "explicit not-for"):
            validate_v4_1_1_semantics(input_row, output("use_conditions", item("use_1", evidence)))


if __name__ == "__main__":
    unittest.main()
