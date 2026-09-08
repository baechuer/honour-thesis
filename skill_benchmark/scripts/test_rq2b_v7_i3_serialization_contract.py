#!/usr/bin/env python3
"""Regression tests for raw, canonical-semantic and portable I3 hashes."""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import freeze_rq2b_v7_i3_output_selection as selection
import merge_rq2b_v7_i3 as merger


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class SelectionSerializationContractTest(unittest.TestCase):
    def test_valid_attempt_does_not_require_canonical_raw_format(self) -> None:
        raw = b'{ "z": 2, "a": "value" }\n'
        with patch.object(selection, "canonical_extraction") as validate:
            rows = selection.validate_attempt([{"input": 1}], raw, "I3-test")
        self.assertEqual(rows, [{"z": 2, "a": "value"}])
        validate.assert_called_once()
        self.assertNotEqual(raw, selection.rows_bytes(rows))

    def test_canonical_semantic_hash_ignores_json_formatting(self) -> None:
        first = selection.read_rows_bytes(b'{ "z": 2, "a": "value" }\n')
        second = selection.read_rows_bytes(b'{"a":"value","z":2}\n')
        self.assertEqual(
            digest(selection.canonical_semantic_rows_bytes(first)),
            digest(selection.canonical_semantic_rows_bytes(second)),
        )


class MergerSerializationContractTest(unittest.TestCase):
    def ledger(self, path: Path, raw: bytes, rows: list[dict[str, object]]) -> dict[str, object]:
        return {
            "selected_output_path": str(path),
            "selected_output_sha256": digest(raw),
            "selected_output_raw_sha256": digest(raw),
            "selected_output_canonical_semantic_jsonl_sha256": digest(
                selection.canonical_semantic_rows_bytes(rows)
            ),
            "canonical_semantic_jsonl_serializer": selection.CANONICAL_SEMANTIC_JSONL_SERIALIZER,
        }

    def test_merger_verifies_raw_then_canonical_semantic_hash(self) -> None:
        raw = b'{ "z": 2, "a": "value" }\n'
        rows = selection.read_rows_bytes(raw)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "selected.jsonl"
            path.write_bytes(raw)
            ledger = self.ledger(path, raw, rows)
            with patch.object(merger, "ROOT", Path("/")):
                actual_rows, raw_sha, canonical_sha = merger.selected_output_rows(ledger, "I3-test")
            self.assertEqual(actual_rows, rows)
            self.assertEqual(raw_sha, digest(raw))
            self.assertEqual(canonical_sha, digest(selection.canonical_semantic_rows_bytes(rows)))

            path.write_bytes(b'{"a":"value","z":2}\n')
            with patch.object(merger, "ROOT", Path("/")):
                with self.assertRaisesRegex(ValueError, "raw output hash mismatch"):
                    merger.selected_output_rows(ledger, "I3-test")

    def test_portable_serializer_is_independent_of_semantic_hash_serializer(self) -> None:
        rows = [{"z": 2, "a": "value"}]
        self.assertNotEqual(
            merger.portable_rows_bytes(rows),
            selection.canonical_semantic_rows_bytes(rows),
        )

    def test_merger_rejects_canonical_semantic_hash_drift_after_raw_hash_passes(self) -> None:
        raw = b'{"a":"value","z":2}\n'
        rows = selection.read_rows_bytes(raw)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "selected.jsonl"
            path.write_bytes(raw)
            ledger = self.ledger(path, raw, rows)
            ledger["selected_output_canonical_semantic_jsonl_sha256"] = "0" * 64
            with patch.object(merger, "ROOT", Path("/")):
                with self.assertRaisesRegex(ValueError, "canonical semantic hash mismatch"):
                    merger.selected_output_rows(ledger, "I3-test")


if __name__ == "__main__":
    unittest.main()
