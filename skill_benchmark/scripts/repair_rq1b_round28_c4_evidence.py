#!/usr/bin/env python3
"""Repair four C4 evidence spans without altering blind adequacy judgments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPAIRS = {
    "c4_round28_reviewer_A_2026-08-28.json": [
        (
            'If codebase evidence shows shipped work NOT mentioned in the spec, list it as \\"beyond_spec\\"',
            'If codebase evidence shows shipped work NOT mentioned in the spec,\\n   list it as \\"beyond_spec\\" and flag that the Confluence page needs',
        ),
        (
            'Commit links — GitHub compare URLs between the last green and first red build',
            '**Commit links** — GitHub compare URLs between the last green and first red build',
        ),
    ],
    "c4_round28_reviewer_B_2026-08-28.json": [
        (
            'If no evidence exists, mark the deliverable as \\"not_started\\" or \\"unclear\\" with low confidence.',
            'If no evidence exists,\\n   mark the deliverable as \\"not_started\\" or \\"unclear\\" with low confidence.',
        ),
        (
            'Commit links — GitHub compare URLs between the last green and first red build',
            '**Commit links** — GitHub compare URLs between the last green and first red build',
        ),
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--working-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    changed: list[str] = []
    for filename, replacements in REPAIRS.items():
        path = args.working_dir / filename
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements:
            if old not in text or text.count(old) != 1:
                raise SystemExit(f"expected_exactly_one_old_span:{filename}:{old}")
            if new in text:
                raise SystemExit(f"replacement_already_present:{filename}:{new}")
            text = text.replace(old, new, 1)
        json.loads(text)
        path.write_text(text, encoding="utf-8")
        if text != original:
            changed.append(filename)
    print(json.dumps({"status": "C4_EVIDENCE_SPAN_REPAIR_ONLY", "changed": changed, "adequacy_or_rationale_changed": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
