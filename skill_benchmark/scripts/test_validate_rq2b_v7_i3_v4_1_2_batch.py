#!/usr/bin/env python3
"""Focused tests for the V4.1.2 source-bounded warning-evidence amendment."""
from __future__ import annotations

import copy
import unittest

import merge_rq2b_i3c as legacy
from validate_rq2b_v7_i3_v4_1_2_batch import canonical_extraction_v4_1_2


def fixture() -> tuple[dict, dict]:
    evidence = "x" * 700
    source = f"---\nname: Example\ndescription: Example task.\n---\n{evidence}\n"
    input_row = {
        "source_row_index": 0,
        "skill_id": "sha256-" + "a" * 64,
        "family": "test",
        "source": "test/source",
        "source_sha256": "a" * 64,
        "name": "Example",
        "description": "Example task.",
        "text": source,
    }
    output_row = {
        "schema_version": "I3C_SUBAGENT_EXTRACTION_V2",
        "parser": "codex_subagent",
        "family": "test",
        "skill": None,
        "skill_id": input_row["skill_id"],
        "name": "Example",
        "description": "Example task.",
        "source": "test/source",
        "fields": {field: [] for field in legacy.FIELD_KEYS},
        "absent_fields": sorted(legacy.FIELD_KEYS),
        "field_warnings": {},
        "qa_warnings": [{
            "code": "mixed_role_unsplittable",
            "field": "constraints_boundaries",
            "message": "Complete mixed-role passage requires source-only review.",
            "evidence": evidence,
        }],
    }
    return input_row, output_row


class WarningEvidenceAmendmentTests(unittest.TestCase):
    def test_legacy_cap_rejects_complete_700_character_evidence(self) -> None:
        input_row, output_row = fixture()
        with self.assertRaisesRegex(ValueError, "Invalid I3C warning evidence"):
            legacy.canonical_extraction(input_row, output_row)

    def test_amendment_accepts_complete_exact_source_substring(self) -> None:
        input_row, output_row = fixture()
        canonical, _, _ = canonical_extraction_v4_1_2(input_row, output_row)
        self.assertEqual(canonical["qa_warnings"][0]["evidence"], "x" * 700)

    def test_amendment_rejects_non_substring(self) -> None:
        input_row, output_row = fixture()
        changed = copy.deepcopy(output_row)
        changed["qa_warnings"][0]["evidence"] = "y" * 700
        with self.assertRaisesRegex(ValueError, "Non-substring I3C warning evidence"):
            canonical_extraction_v4_1_2(input_row, changed)

    def test_message_cap_is_unchanged(self) -> None:
        input_row, output_row = fixture()
        changed = copy.deepcopy(output_row)
        changed["qa_warnings"][0]["message"] = "m" * 501
        with self.assertRaisesRegex(ValueError, "Invalid I3C warning message"):
            canonical_extraction_v4_1_2(input_row, changed)


if __name__ == "__main__":
    unittest.main()
