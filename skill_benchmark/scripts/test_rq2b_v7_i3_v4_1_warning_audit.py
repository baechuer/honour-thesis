#!/usr/bin/env python3
"""Focused tests for the V4.1 warning-audit contracts."""
from __future__ import annotations

import unittest

from build_rq2b_v7_i3_v4_1_warning_audit import assign_reviewer_groups, warning_pairs
from finalize_rq2b_v7_i3_v4_1_warning_audit import validate_return


class WarningAuditTests(unittest.TestCase):
    def packet(self) -> dict:
        return {
            "issue_id": "I3W-0123456789abcdef0123",
            "extractor_group": 1,
            "reviewer_group": 2,
            "source_sha256": "a" * 64,
            "selected_output_sha256": "b" * 64,
        }

    def returned(self) -> dict:
        packet = self.packet()
        return {
            "schema_version": "rq2b-v7-i3-v4.1-warning-audit-return-v1",
            "issue_id": packet["issue_id"],
            "reviewer_group": packet["reviewer_group"],
            "source_sha256": packet["source_sha256"],
            "selected_output_sha256": packet["selected_output_sha256"],
            "decision": "ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION",
            "evidence_is_exact_and_complete": True,
            "warning_is_justified": True,
            "field_assignment_is_correct": True,
            "rationale": "The complete mixed-role sentence is retained only as a boundary.",
        }

    def test_warning_union_deduplicates_optional_mirror(self) -> None:
        warning = {"code": "mixed_role_unsplittable", "message": "mixed", "evidence": "full sentence"}
        row = {
            "skill_id": "skill",
            "field_warnings": {"constraints_boundaries": [warning]},
            "qa_warnings": [{"field": "constraints_boundaries", **warning}],
        }
        self.assertEqual(len(warning_pairs(row)), 1)
        row["qa_warnings"] = []
        self.assertEqual(warning_pairs(row)[0][1]["field"], "constraints_boundaries")

    def test_assignment_never_uses_extractor_group(self) -> None:
        issues = [
            {"issue_id": f"I3W-{index:020x}", "extractor_group": (index % 3) + 1, "reviewer_group": None}
            for index in range(30)
        ]
        assign_reviewer_groups(issues)
        self.assertTrue(all(row["reviewer_group"] != row["extractor_group"] for row in issues))

    def test_accept_requires_all_three_source_checks(self) -> None:
        validate_return(self.packet(), self.returned())
        returned = self.returned()
        returned["field_assignment_is_correct"] = False
        with self.assertRaisesRegex(ValueError, "unanimous source checks"):
            validate_return(self.packet(), returned)


if __name__ == "__main__":
    unittest.main()
