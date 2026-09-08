#!/usr/bin/env python3
"""Focused tests for prospective I3 V4 lexical safety gates."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_rq2b_v7_i3_v4_batch import validate_v4_semantics  # noqa: E402


FIELDS = {
    "use_conditions": [],
    "input_preconditions": [],
    "output_artifacts": [],
    "workflow_steps": [],
    "constraints_boundaries": [],
    "dependencies_resources": [],
    "success_criteria": [],
}


def item(item_id: str, evidence: str) -> dict:
    return {
        "id": item_id,
        "text": evidence,
        "evidence": evidence,
        "evidence_status": "explicit",
        "confidence": 0.9,
        "selector_usefulness": "high",
    }


def output(field: str, value: dict) -> dict:
    fields = copy.deepcopy(FIELDS)
    fields[field].append(value)
    return {"fields": fields, "field_warnings": {}, "qa_warnings": []}


class V4SafetyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.input = {"skill_id": "sha256-test"}

    def test_clean_atomic_use_condition_passes(self) -> None:
        self.assertEqual(validate_v4_semantics(self.input, output("use_conditions", item("use_1", "Use when drafting a contract."))), (1, 0))

    def test_negative_use_condition_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "negative/polarity"):
            validate_v4_semantics(self.input, output("use_conditions", item("use_1", "Do not use for incident response.")))

    def test_raw_description_key_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "raw description syntax"):
            validate_v4_semantics(self.input, output("use_conditions", item("use_1", "description: Use for reports.")))

    def test_controlled_metadata_leakage_rejected(self) -> None:
        leaked = "category: public-style-controlled\n- controlled-confusability\nsource_style: public_style_controlled\ncluster_id: psc_test"
        with self.assertRaisesRegex(ValueError, "controlled-corpus metadata leakage"):
            validate_v4_semantics(self.input, output("constraints_boundaries", item("boundary_1", leaked)))

    def test_duplicate_evidence_across_fields_rejected(self) -> None:
        value = "Requires a CSV input."
        row = output("input_preconditions", item("input_1", value))
        row["fields"]["dependencies_resources"].append(item("dependency_1", value))
        with self.assertRaisesRegex(ValueError, "duplicated across fields"):
            validate_v4_semantics(self.input, row)


if __name__ == "__main__":
    unittest.main()
