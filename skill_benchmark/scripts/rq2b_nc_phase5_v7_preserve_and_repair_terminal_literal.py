#!/usr/bin/env python3
"""Preserve then repair one known terminal-only JSON format drift.

The repair is permitted only for the exact byte suffix ``}\\n\\n`` where the
middle two bytes are a literal backslash and ``n`` outside the JSON document.
The exact original is archived as base64 before the canonical working copy is
made parseable.  No review content, anchors, labels, or fields are altered.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
RAW_ROOT = (
    WORKSPACE
    / "skill_benchmark/rq2b_naturalistic_confusability/review"
    / "RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--microbatch", type=int, required=True)
    parser.add_argument("--version", type=int, default=1)
    parser.add_argument("--lane", choices=("A", "B"), required=True)
    parser.add_argument("--batch-id", action="append", required=True)
    args = parser.parse_args()
    batch_ids = args.batch_id
    if len(batch_ids) != 12 or len(set(batch_ids)) != 12:
        raise SystemExit("a microbatch repair must name exactly 12 distinct groups")

    destination = (
        WORKSPACE
        / "skill_benchmark/rq2b_naturalistic_confusability/review"
        / f"RQ2B-NC-phase5-v7-machine-b-microbatch-{args.microbatch:03d}-"
        f"reviewer-{args.lane.lower()}-syntax-repair-preservation-2026-09-08-v{args.version}"
    )
    if destination.exists():
        raise SystemExit(f"refusing to overwrite a preservation package: {destination}")
    archive = destination / "raw_original_returns_base64"
    archive.mkdir(parents=True)

    entries = []
    canonical = RAW_ROOT / f"reviewer_{args.lane}"
    for batch_id in batch_ids:
        path = canonical / f"{batch_id}.json"
        raw = path.read_bytes()
        if not raw.endswith(b"}\\n\n"):
            raise SystemExit(f"{path} does not have the permitted literal terminal suffix")
        repaired = raw[:-3] + b"\n"
        json.loads(repaired.decode("utf-8"))
        archived_path = archive / f"{batch_id}.base64"
        archived_path.write_bytes(base64.b64encode(raw) + b"\n")
        if base64.b64decode(archived_path.read_bytes()) != raw:
            raise RuntimeError(f"archive replay mismatch for {batch_id}")
        path.write_bytes(repaired)
        entries.append(
            {
                "batch_id": batch_id,
                "canonical_return_path": str(path.relative_to(WORKSPACE)),
                "preserved_raw_base64_path": str(archived_path.relative_to(WORKSPACE)),
                "original_sha256": sha256(raw),
                "repaired_sha256": sha256(repaired),
                "transformation": "remove only the terminal non-JSON literal bytes backslash+n; retain one final newline",
                "semantic_change": False,
                "archive_replay_verified": True,
            }
        )

    ledger = {
        "schema_version": "rq2b_nc_phase5_v7_terminal_literal_preservation_repair_v1",
        "scope": "format repair only; no review semantics or target information touched",
        "microbatch": args.microbatch,
        "reviewer_lane": args.lane,
        "entries": entries,
    }
    (destination / "format_repair_ledger.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )
    (destination / "README.md").write_text(
        "# Preserved terminal-literal format repair\n\n"
        "The original non-parseable byte stream is retained as a base64 artifact. "
        "The canonical copy removes only the literal terminal `\\\\n` outside JSON, "
        "then retains one final newline. No reviewer content is changed.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
