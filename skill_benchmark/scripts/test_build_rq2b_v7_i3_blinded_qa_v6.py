#!/usr/bin/env python3
"""Mechanical contract checks for the frozen V4.1.5 QA v6 packet."""
from __future__ import annotations

import json
import unittest

import build_rq2b_v7_i3_blinded_qa_v6 as builder


class BlindedQaV6Test(unittest.TestCase):
    def test_frozen_packet_contract(self) -> None:
        payloads = builder.build()
        manifest = json.loads(payloads["manifest.json"])
        self.assertEqual(manifest["sample_size"], 120)
        self.assertEqual(manifest["previous_samples_excluded"], 360)
        self.assertEqual(manifest["counts"]["extractor_group"], {"1": 40, "2": 40, "3": 40})
        self.assertEqual(manifest["counts"]["reviewer_group"], {"1": 40, "2": 40, "3": 40})
        self.assertEqual(manifest["counts"]["length_quartile"], {"Q1": 30, "Q2": 30, "Q3": 30, "Q4": 30})
        self.assertTrue(all(value >= 20 for value in manifest["counts"]["present_field_rows"].values()))
        self.assertEqual(len(manifest["bindings"]["previous_qa_packages"]), 3)
        self.assertEqual(
            manifest["pass_rule"],
            {
                "calibration": "each reviewer group exactly matches all 8 hidden answers",
                "critical_error_rows": 0,
                "maximum_major_error_rows": 6,
                "maximum_major_error_rate": 0.05,
                "field_stratum_rule": "for each field represented in at least 20 rows, major error rate must be <=0.05",
                "failure_action": "repair the full affected class and draw another fresh versioned sample; never patch only sampled rows",
            },
        )
        key_rows = [json.loads(line) for line in payloads["sampling_key_do_not_give_reviewer.jsonl"].splitlines()]
        self.assertEqual(len(key_rows), len({row["source_sha256"] for row in key_rows}))
        slot_ids = []
        for slot in range(1, 7):
            rows = [json.loads(line) for line in payloads[f"review_slots/qa_slot_{slot:02d}.jsonl"].splitlines()]
            self.assertEqual(len(rows), 20)
            slot_ids.extend(row["review_id"] for row in rows)
        self.assertEqual(len(slot_ids), len(set(slot_ids)))


if __name__ == "__main__":
    unittest.main()
