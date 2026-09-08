#!/usr/bin/env python3
"""Focused tests for V4.1 structurally scoped extraction gates."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_rq2b_v7_i3_v4_1_batch import validate_v4_1_semantics  # noqa: E402


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


class V41SafetyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.input = {"skill_id": "sha256-test", "text": "---\nname: demo\ndescription: Use for reports.\n---\n\nBody."}

    def test_clean_atomic_use_condition_passes(self) -> None:
        self.input["text"] += "\nUse when drafting a contract."
        self.assertEqual(validate_v4_1_semantics(self.input, output("use_conditions", item("use_1", "Use when drafting a contract."))), (1, 0))

    def test_explicit_not_for_rejected(self) -> None:
        self.input["text"] += "\nDo not use for incident response."
        with self.assertRaisesRegex(ValueError, "explicit not-for"):
            validate_v4_1_semantics(self.input, output("use_conditions", item("use_1", "Do not use for incident response.")))

    def test_input_state_negation_passes(self) -> None:
        evidence = "Use when the user does not yet have a migration plan."
        self.input["text"] += "\n" + evidence
        self.assertEqual(validate_v4_1_semantics(self.input, output("input_preconditions", item("input_1", evidence))), (1, 0))

    def test_raw_frontmatter_description_key_rejected(self) -> None:
        evidence = "description: Use for reports."
        with self.assertRaisesRegex(ValueError, "raw frontmatter description"):
            validate_v4_1_semantics(self.input, output("use_conditions", item("use_1", evidence)))

    def test_body_description_key_passes(self) -> None:
        evidence = "description: Explain when the skill should run."
        self.input["text"] += "\n```yaml\n" + evidence + "\n```"
        self.assertEqual(validate_v4_1_semantics(self.input, output("workflow_steps", item("workflow_1", evidence))), (1, 0))

    def test_frontmatter_benchmark_key_rejected(self) -> None:
        evidence = "gold_label: hidden"
        self.input["text"] = "---\nname: demo\n" + evidence + "\n---\nBody."
        with self.assertRaisesRegex(ValueError, "forbidden candidate metadata"):
            validate_v4_1_semantics(self.input, output("constraints_boundaries", item("boundary_1", evidence)))

    def test_body_gold_label_field_passes(self) -> None:
        evidence = "gold_label: expected_class"
        self.input["text"] += "\nExample schema:\n" + evidence
        self.assertEqual(validate_v4_1_semantics(self.input, output("output_artifacts", item("output_1", evidence))), (1, 0))

    def test_controlled_frontmatter_leakage_rejected(self) -> None:
        evidence = "category: public-style-controlled\ntags: [controlled-confusability]\nsource_style: public_style_controlled\ncluster_id: psc_test"
        self.input["text"] = "---\nname: demo\n" + evidence + "\n---\nBody."
        with self.assertRaisesRegex(ValueError, "controlled-corpus metadata leakage"):
            validate_v4_1_semantics(self.input, output("constraints_boundaries", item("boundary_1", evidence)))

    def test_duplicate_evidence_across_fields_rejected(self) -> None:
        evidence = "Requires a CSV input."
        self.input["text"] += "\n" + evidence
        row = output("input_preconditions", item("input_1", evidence))
        row["fields"]["dependencies_resources"].append(item("dependency_1", evidence))
        with self.assertRaisesRegex(ValueError, "duplicated across fields"):
            validate_v4_1_semantics(self.input, row)


if __name__ == "__main__":
    unittest.main()
