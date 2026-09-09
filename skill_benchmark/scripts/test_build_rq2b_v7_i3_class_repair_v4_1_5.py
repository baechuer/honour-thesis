#!/usr/bin/env python3
"""Focused regression tests for V7 I3 V4.1.5 source-only repair."""
from __future__ import annotations

import unittest
import json
from pathlib import Path

from build_rq2b_v7_i3_class_repair_v4_1_5 import (
    classify_heading,
    document_blocks,
    non_selection_fragment,
    repair_row,
)


class ClassRepairV415Test(unittest.TestCase):
    def test_versioned_prerequisite_is_one_complete_block(self) -> None:
        source = (
            "# Skill\n\n## Prerequisites\n\n"
            "- Install `starlake-airflow>=0.6.1` or `starlake-dagster>=0.5.1`.\n"
        )
        _, blocks = document_blocks(source)
        self.assertEqual(blocks[0].field, "dependencies_resources")
        self.assertEqual(
            blocks[0].evidence,
            "- Install `starlake-airflow>=0.6.1` or `starlake-dagster>=0.5.1`.",
        )

    def test_inline_contexts_route_following_lists(self) -> None:
        source = (
            "# Skill\n\nReturn one of these packet types:\n\n- `video-production brief`\n\n"
            "If you need more context:\n\n1. What is the audience?\n\n"
            "Related skills:\n\n- [copywriting](../copywriting/SKILL.md)\n"
        )
        _, blocks = document_blocks(source)
        by_evidence = {block.evidence: block.field for block in blocks}
        self.assertEqual(by_evidence["- `video-production brief`"], "output_artifacts")
        self.assertEqual(by_evidence["1. What is the audience?"], "input_preconditions")
        self.assertEqual(by_evidence["- [copywriting](../copywriting/SKILL.md)"], "dependencies_resources")

    def test_extended_heading_classes(self) -> None:
        self.assertEqual(classify_heading("Use This Skill When"), "use_conditions")
        self.assertEqual(classify_heading("Related Skills"), "dependencies_resources")
        self.assertEqual(classify_heading("Gather the minimum context"), "input_preconditions")
        self.assertEqual(classify_heading("Step 1: Gather inputs"), "input_preconditions")
        self.assertIsNone(classify_heading("Email Types Reference"))

    def test_bare_template_and_workflow_noun_are_removed(self) -> None:
        self.assertEqual(
            non_selection_fragment("- Recommended Change", "workflow_steps", None),
            "bare_table_or_template_label",
        )
        self.assertEqual(
            non_selection_fragment("relative sizing before commitment", "workflow_steps", None),
            "non_operational_workflow_fragment",
        )

    def test_output_schema_fence_is_retained(self) -> None:
        _, blocks = document_blocks("# Skill\n\n## Output format\n\n```\nFile: [path]\n```\n")
        fence = next(block for block in blocks if block.kind == "fence")
        self.assertIsNone(non_selection_fragment(fence.evidence, "output_artifacts", fence))

    def test_dependency_supplement_is_not_capped(self) -> None:
        dependencies = "\n".join(f"- dependency {index}" for index in range(1, 22))
        source = f"# Skill\n\n## Dependencies and resources\n\n{dependencies}\n"
        canonical = {
            "source_row_index": 0,
            "skill_id": "sha256-test",
            "source": "source/SKILL.md",
            "source_sha256": "0" * 64,
            "worker_output_sha256": "1" * 64,
            "retained_selector_spans": [],
            "omitted_selector_spans": [],
        }
        worker = {
            "fields": {field: [] for field in (
                "constraints_boundaries", "dependencies_resources", "input_preconditions",
                "output_artifacts", "success_criteria", "use_conditions", "workflow_steps",
            )},
            "absent_fields": [],
        }
        repaired, _ = repair_row(canonical, worker, source)
        self.assertEqual(len(repaired["fields"]["dependencies_resources"]), 21)

    def test_materialized_failed_v5_classes(self) -> None:
        prep = Path(__file__).resolve().parents[1] / "rq2b_naturalistic_confusability" / "preparation"
        package = prep / "v7_phase7_i3_class_repair_2026_09_09_v4_1_5"
        failed = json.loads((prep / "v7_phase7_i3_blinded_qa_final_2026_09_09_v5" / "qa_final_report.json").read_text())
        with (package / "canonical_extractions.jsonl").open() as handle:
            rows = {row["source_sha256"]: row for row in map(json.loads, handle)}
        with (package / "class_repair_ledger.jsonl").open() as handle:
            ledger = {row["source_sha256"]: row for row in map(json.loads, handle)}
        failed_shas = {detail["source_sha256"] for detail in failed["error_details"]}
        self.assertEqual(len(failed_shas), 13)
        self.assertTrue(all(ledger[value]["changed"] for value in failed_shas))

        def by_suffix(suffix: str) -> dict:
            return next(row for row in rows.values() if suffix in row["source"])

        def evidence(row: dict, field: str) -> list[str]:
            return [item["evidence"] for item in row["fields"][field]]

        thermo = by_suffix("opentrons-thermocycler/source/SKILL.original.md")
        thermo_dependencies = evidence(thermo, "dependencies_resources")
        self.assertIn("- **GEN2 features:** API 2.13+", thermo_dependencies)
        self.assertIn("- **Auto-sealing lids:** API 2.15+", thermo_dependencies)
        self.assertIn("- **Recommended:** 2.19+ for full feature support", thermo_dependencies)

        dag = by_suffix("starlake-skills-agents-skills-dag-create/source/SKILL.original.md")
        dag_dependencies = evidence(dag, "dependencies_resources")
        self.assertTrue(any("starlake-airflow>=0.6.1" in value and "starlake-dagster>=0.5.1" in value for value in dag_dependencies))

        for suffix, required in (
            ("mobile-ops-compliance-checker/SKILL.md", "- crash log"),
            ("mobile-ops-timeline-builder/SKILL.md", "- crash log"),
            ("incident-ops-compliance-checker/SKILL.md", "- timeline"),
        ):
            self.assertIn(required, evidence(by_suffix(suffix), "dependencies_resources"))

        slides = by_suffix("slide-deck-visual-auditor/SKILL.md")
        self.assertFalse({"Slide", "Visual or communication issue", "- Impact"} & set(evidence(slides, "workflow_steps")))

        lease = by_suffix("commercial-lease-review/source/SKILL.original.md")
        self.assertNotIn("- Recommended Change", evidence(lease, "workflow_steps"))

        landing = by_suffix("public-skillme-landing-page-copy/source/SKILL.original.md")
        self.assertTrue(any(value.startswith("1. The one promise") for value in evidence(landing, "input_preconditions")))

        video = by_suffix("public-oh-my-video-production/source/SKILL.original.md")
        self.assertIn("- `video-production brief`", evidence(video, "output_artifacts"))
        self.assertNotIn("- `video-production brief`", evidence(video, "workflow_steps"))

        transcript = by_suffix("baoyu-youtube-transcript/source/SKILL.original.md")
        self.assertIn("- Full URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`", evidence(transcript, "input_preconditions"))
        self.assertTrue(any("| `text` | `.md` |" in value for value in evidence(transcript, "output_artifacts")))

        email = by_suffix("agentkits-marketing-skills-email-sequence/source/SKILL.original.md")
        self.assertTrue(any(value.startswith("**Trigger**:") for value in evidence(email, "use_conditions")))
        self.assertTrue(any(value.startswith("1. What triggers entry") for value in evidence(email, "input_preconditions")))
        self.assertTrue(any("onboarding-cro" in value for value in evidence(email, "dependencies_resources")))
        self.assertFalse(any(value.startswith("**Trigger**:") for value in evidence(email, "dependencies_resources")))

        sanitize = by_suffix("gws-modelarmor-sanitize-response/source/SKILL.original.md")
        self.assertIn("- Use for outbound safety (model -> user).", evidence(sanitize, "use_conditions"))
        self.assertTrue(any("gws-shared" in value for value in evidence(sanitize, "dependencies_resources")))

        estimation = by_suffix("public-oh-my-task-estimation/source/SKILL.original.md")
        self.assertNotIn("- relative sizing before commitment", evidence(estimation, "workflow_steps"))
        self.assertTrue(any("references/estimation-modes.md" in value for value in evidence(estimation, "dependencies_resources")))


if __name__ == "__main__":
    unittest.main()
