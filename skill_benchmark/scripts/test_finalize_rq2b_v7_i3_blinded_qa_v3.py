#!/usr/bin/env python3
"""Focused tests for V4.1 blinded-QA return validation."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from finalize_rq2b_v7_i3_blinded_qa_v3 import validate_return  # noqa: E402


def clean() -> dict:
    return {
        "review_id": "V7-I3-V41-QA-TEST",
        "review_status": "COMPLETE",
        "critical_error": False,
        "major_error": False,
        "affected_fields": [],
        "error_codes": [],
        "reviewer_notes": "No material extraction-fidelity error.",
        "reviewer_group": 1,
    }


class ReturnValidationTest(unittest.TestCase):
    def test_clean_return_passes(self) -> None:
        validate_return(clean(), 1)

    def test_major_without_field_is_rejected(self) -> None:
        row = clean()
        row.update({"major_error": True, "error_codes": ["WRONG_OPERATIONAL_FIELD"]})
        with self.assertRaisesRegex(ValueError, "major-code/field mismatch"):
            validate_return(row, 1)

    def test_major_with_field_passes(self) -> None:
        row = clean()
        row.update({
            "major_error": True,
            "affected_fields": ["workflow_steps"],
            "error_codes": ["WRONG_OPERATIONAL_FIELD"],
        })
        validate_return(row, 1)


if __name__ == "__main__":
    unittest.main()
