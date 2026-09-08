#!/usr/bin/env python3
"""Regression tests for V7 I3 batch-validator reporting."""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_rq2b_v7_i3_batch as validator


class ReportOutputPathTest(unittest.TestCase):
    def test_reports_actual_repo_relative_reissue_path(self) -> None:
        reissue = validator.ROOT / (
            "skill_benchmark/cache/rq2b_v7_phase7_i3_extraction_2026_09_08_v1/"
            "reissues/i3_output_001_reissue_008.jsonl"
        )
        self.assertEqual(
            validator.report_output_path(reissue),
            "skill_benchmark/cache/rq2b_v7_phase7_i3_extraction_2026_09_08_v1/"
            "reissues/i3_output_001_reissue_008.jsonl",
        )

    def test_reports_external_path_as_absolute(self) -> None:
        external = Path("/tmp/rq2b-validator-regression-output.jsonl")
        self.assertEqual(validator.report_output_path(external), str(external.resolve()))


if __name__ == "__main__":
    unittest.main()
