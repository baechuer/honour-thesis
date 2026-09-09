#!/usr/bin/env python3
"""Focused synthetic tests for V7 I3 V4.1.4 source-only class repair."""
from __future__ import annotations

import unittest

from build_rq2b_v7_i3_class_repair_v4_1_4 import (
    classify_heading,
    containing_block,
    markdown_blocks,
    markdown_headings,
    polarity_field,
    special_field,
)


class ClassRepairTest(unittest.TestCase):
    def test_truncated_bullet_expands_to_complete_continuation_block(self) -> None:
        source = (
            "# Skill\n\n## Prerequisites & environment\n\n"
            "- A working CI/CD pipeline that already builds, bakes a golden image (or\n"
            "  prepares an Ansible-driven config push), and deploys safely.\n"
            "- A second prerequisite.\n"
        )
        headings = markdown_headings(source)
        blocks = markdown_blocks(source, headings)
        position = source.index("- A working")
        block = containing_block(blocks, position)
        self.assertIsNotNone(block)
        assert block is not None
        self.assertEqual(block.field, "dependencies_resources")
        self.assertEqual(
            block.evidence,
            "- A working CI/CD pipeline that already builds, bakes a golden image (or\n"
            "  prepares an Ansible-driven config push), and deploys safely.",
        )

    def test_strong_heading_field_mapping(self) -> None:
        cases = {
            "Use when": "use_conditions",
            "Inputs to collect": "input_preconditions",
            "Dependencies / Resources": "dependencies_resources",
            "Procedure": "workflow_steps",
            "Deliverables": "output_artifacts",
            "Do NOT": "constraints_boundaries",
            "Quality bar": "success_criteria",
        }
        for heading, expected in cases.items():
            with self.subTest(heading=heading):
                self.assertEqual(classify_heading(heading), expected)

    def test_nested_step_heading_inherits_workflow(self) -> None:
        source = "## Workflow\n\n### Step 1: Inspect\n\nOpen the source.\n"
        blocks = markdown_blocks(source, markdown_headings(source))
        self.assertEqual([block.field for block in blocks], ["workflow_steps"])

    def test_polarity_and_resource_and_numbered_operation_mapping(self) -> None:
        self.assertEqual(
            polarity_field("Do not change code until evidence identifies one cause.", "workflow_steps"),
            "constraints_boundaries",
        )
        self.assertEqual(
            special_field("Documentation: [API reference](https://example.test/docs)", "output_artifacts"),
            "dependencies_resources",
        )
        self.assertEqual(
            special_field("4. Return the resource map.", "output_artifacts"),
            "workflow_steps",
        )


if __name__ == "__main__":
    unittest.main()
