#!/usr/bin/env python3
"""Focused tests for baseline-relative V4.1.2 warning-repair integration."""
from __future__ import annotations

import copy
import unittest

import build_rq2b_v7_i3_v4_1_2_warning_repair_integration as subject


FIELDS = list(subject.shared.FIELD_KEYS)


def item(item_id: str, text: str) -> dict:
    return {
        "id": item_id,
        "text": text,
        "evidence": text,
        "evidence_status": "explicit",
        "confidence": 0.95,
        "selector_usefulness": "high",
    }


def row() -> dict:
    fields = {field: [] for field in FIELDS}
    fields["use_conditions"] = [item("use_1", "use one")]
    fields["workflow_steps"] = [item("workflow_1", "step one")]
    return {
        "schema_version": "fixture",
        "skill_id": "sha256-fixture",
        "skill": "fixture",
        "source": "source",
        "name": "fixture",
        "description": "fixture",
        "family": "fixture",
        "parser": "fixture",
        "fields": fields,
        "absent_fields": [field for field in FIELDS if not fields[field]],
        "field_warnings": [],
        "qa_warnings": [
            {"code": "mixed_role_unsplittable", "field": "constraints_boundaries", "message": "first", "evidence": "old one"},
            {"code": "mixed_role_unsplittable", "field": "constraints_boundaries", "message": "second", "evidence": "old two"},
        ],
    }


def fix_absent(value: dict) -> dict:
    value["absent_fields"] = [field for field in FIELDS if not value["fields"][field]]
    return value


class AtomicMergeTests(unittest.TestCase):
    def test_nonoverlapping_field_edits_merge(self) -> None:
        base = row()
        g1 = copy.deepcopy(base)
        g1["fields"]["use_conditions"][0]["text"] = "use changed"
        g2 = copy.deepcopy(base)
        g2["fields"]["workflow_steps"][0]["text"] = "step changed"
        merged, conflicts = subject.merge_row(base, {1: g1, 2: g2}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(conflicts, [])
        self.assertEqual(merged["fields"]["use_conditions"][0]["text"], "use changed")
        self.assertEqual(merged["fields"]["workflow_steps"][0]["text"], "step changed")

    def test_identical_same_atom_edits_deduplicate(self) -> None:
        base = row()
        g1 = copy.deepcopy(base)
        g1["fields"]["use_conditions"][0]["confidence"] = 0.9
        merged, conflicts = subject.merge_row(base, {1: g1, 2: copy.deepcopy(g1)}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(conflicts, [])
        self.assertEqual(merged["fields"]["use_conditions"][0]["confidence"], 0.9)

    def test_divergent_same_atom_edits_conflict(self) -> None:
        base = row()
        g1 = copy.deepcopy(base)
        g2 = copy.deepcopy(base)
        g1["fields"]["use_conditions"][0]["text"] = "left"
        g2["fields"]["use_conditions"][0]["text"] = "right"
        _, conflicts = subject.merge_row(base, {1: g1, 2: g2}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["reason"], "DIVERGENT_BASELINE_RELATIVE_ATOMIC_EDITS")

    def test_different_warning_edits_merge(self) -> None:
        base = row()
        g1 = copy.deepcopy(base)
        g2 = copy.deepcopy(base)
        g1["qa_warnings"][0]["evidence"] = "new one"
        g2["qa_warnings"][1]["evidence"] = "new two"
        merged, conflicts = subject.merge_row(base, {1: g1, 2: g2}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(conflicts, [])
        self.assertEqual([warning["evidence"] for warning in merged["qa_warnings"]], ["new one", "new two"])

    def test_divergent_same_warning_edits_conflict(self) -> None:
        base = row()
        g1 = copy.deepcopy(base)
        g2 = copy.deepcopy(base)
        g1["qa_warnings"][0]["evidence"] = "left"
        g2["qa_warnings"][0]["evidence"] = "right"
        _, conflicts = subject.merge_row(base, {1: g1, 2: g2}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["area"], "qa_warnings")

    def test_delete_vs_modify_conflicts(self) -> None:
        base = row()
        g1 = copy.deepcopy(base)
        g2 = copy.deepcopy(base)
        g1["fields"]["workflow_steps"] = []
        fix_absent(g1)
        g2["fields"]["workflow_steps"][0]["confidence"] = 0.8
        _, conflicts = subject.merge_row(base, {1: g1, 2: g2}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(len(conflicts), 1)

    def test_duplicate_warning_locator_removal_is_position_stable(self) -> None:
        base = row()
        base["qa_warnings"][1]["message"] = base["qa_warnings"][0]["message"]
        g1 = copy.deepcopy(base)
        del g1["qa_warnings"][0]
        merged, conflicts = subject.merge_row(base, {1: g1}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(conflicts, [])
        self.assertEqual(merged["qa_warnings"], [base["qa_warnings"][1]])

    def test_new_warning_can_be_integrated_when_row_is_authorised(self) -> None:
        base = row()
        g1 = copy.deepcopy(base)
        g1["qa_warnings"].append({"code": "new_warning", "field": "", "message": "new", "evidence": ""})
        merged, conflicts = subject.merge_row(base, {1: g1}, batch_id="I3V41-001", source_row_index=1)
        self.assertEqual(conflicts, [])
        self.assertEqual(merged["qa_warnings"][-1]["code"], "new_warning")

    def test_supplement_rejects_selector_visible_change(self) -> None:
        before = row()
        after = copy.deepcopy(before)
        after["fields"]["use_conditions"][0]["text"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "selector-visible/non-warning"):
            subject.verify_supplement_delta(
                group=3, batch_id="I3V41-001", base_proposal=[before], attempt=[after],
                ledger_rows=[{"skill_id": before["skill_id"]}],
            )

    def test_supplement_accepts_only_warning_evidence(self) -> None:
        before = row()
        after = copy.deepcopy(before)
        after["qa_warnings"][0]["evidence"] = "complete exact evidence"
        subject.verify_supplement_delta(
            group=3, batch_id="I3V41-001", base_proposal=[before], attempt=[after],
            ledger_rows=[{"skill_id": before["skill_id"]}],
        )

    def test_group2_supplement_replays_ledger_snapshots(self) -> None:
        before = row()
        after = copy.deepcopy(before)
        after["fields"]["workflow_steps"] = []
        fix_absent(after)
        subject.verify_supplement_delta(
            group=2, batch_id="I3V41-001", base_proposal=[before], attempt=[after],
            ledger_rows=[{
                "skill_id": before["skill_id"],
                "actions": [{"action": "fixture"}],
                "before": {"fields": before["fields"], "qa_warnings": before["qa_warnings"]},
                "after": {"fields": after["fields"], "qa_warnings": after["qa_warnings"]},
            }],
        )


if __name__ == "__main__":
    unittest.main()
