"""Narrow safety and replay tests for approved-plan/local-view preparation."""
import json
import tempfile
import unittest
from pathlib import Path

import freeze_rq2_approved_research_plan as plan
import build_rq2b_v7_analysis_freeze as analysis_freeze
import prepare_rq2b_v7_phase7_i1_i2 as prep


class PreparationTests(unittest.TestCase):
    def test_minimal_view_and_utf8_identity(self):
        text = "技能 source\r\nkeep trailing spaces  \n"
        row = prep.view(prep.sha(text.encode()), "I2-original", text)
        self.assertEqual(set(row), {"schema_version", "source_sha256", "representation", "selector_text", "selector_text_sha256"})
        self.assertEqual(row["source_sha256"], row["selector_text_sha256"])
        self.assertEqual(row["selector_text"].encode(), text.encode())

    def test_no_overwrite_or_silent_repair(self):
        with tempfile.TemporaryDirectory(prefix="rq2b-preparation-test-") as folder:
            p = Path(folder) / "derived.jsonl"
            prep.write_missing(p, b"original\n")
            prep.write_missing(p, b"original\n")
            with self.assertRaises(ValueError):
                prep.write_missing(p, b"replacement\n")
            self.assertEqual(p.read_bytes(), b"original\n")

    def test_phase7_outputs_replay_and_preserve_scope(self):
        files, payloads = prep.build()
        for name, data in files.items():
            self.assertEqual((prep.ROOT / prep.OUTPUT / name).read_bytes(), data)
        for name, data in payloads.items():
            self.assertEqual((prep.ROOT / prep.CACHE / name).read_bytes(), data)
            rows = [json.loads(line) for line in data.splitlines()]
            self.assertEqual(len(rows), 3798)
            self.assertEqual(len({r['source_sha256'] for r in rows}), 3798)
        report = json.loads(files['mechanical_report.json'])
        self.assertFalse(report['formal_execution_ready'])
        self.assertEqual(report['network_calls'], 0)

    def test_approved_plan_is_not_inference_or_expansion_authority(self):
        expected = plan.build()
        self.assertEqual((plan.ROOT / plan.OUTPUT / 'plan_freeze.json').read_bytes(), expected)
        record = json.loads(expected)
        self.assertFalse(record['execution']['formal_selector_execution_authorised'])
        self.assertFalse(record['future_scope']['assume_new_background_candidates_negative'])
        self.assertTrue(record['future_scope']['admission_and_nested_scale_levels_not_sealed'])
        self.assertEqual(record['counts']['source_candidates'], 3798)
        self.assertEqual(record['analysis']['primary_comparisons'], ['P1', 'P2', 'P3', 'P4', 'P5'])

    def test_pre_outcome_analysis_freeze_is_label_isolated(self):
        files = analysis_freeze.build()
        for name, data in files.items():
            self.assertEqual((analysis_freeze.ROOT / analysis_freeze.OUTPUT / name).read_bytes(), data)
        runtime = [json.loads(line) for line in files['label_free_query_runtime.jsonl'].splitlines()]
        labels = [json.loads(line) for line in files['offline_label_adapter.jsonl'].splitlines()]
        dependencies = [json.loads(line) for line in files['dependency_ledger.jsonl'].splitlines()]
        report = json.loads(files['freeze_report.json'])
        self.assertEqual(len(runtime), 1077)
        self.assertEqual(set(runtime[0]), {'schema_version', 'prompt_id', 'prompt_sha256', 'prompt'})
        self.assertEqual(len(labels), len(dependencies), 1077)
        self.assertEqual(sum(len(row['acceptable_set_source_sha256']) for row in labels), 1325)
        self.assertEqual(sum(len(row['judged_candidate_dispositions']) for row in labels), 8979)
        self.assertEqual(report['counts']['dependency_groups'], 355)
        self.assertFalse(report['scientific_results_observed'])
        self.assertEqual(report['provider_calls'], 0)


if __name__ == '__main__':
    unittest.main()
