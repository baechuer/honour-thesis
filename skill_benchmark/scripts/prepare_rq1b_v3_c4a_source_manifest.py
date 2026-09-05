#!/usr/bin/env python3
"""Build a hash-verified C4A source manifest from a C1 source-only roster.

This local adapter makes the source bindings expected by the anonymous C4A
packet materialiser. It does not read prompts, targets, labels, selectors, or
results, and it makes no network call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c1-roster", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_existing_output_or_audit")

    unique: dict[str, dict[str, str]] = {}
    failures: list[str] = []
    for row in read_jsonl(args.c1_roster):
        c1_id = str(row.get("c1_review_id", ""))
        for member in row.get("members", []):
            source_id = str(member.get("source_id", ""))
            expected_sha = str(member.get("sha256", ""))
            absolute_path = Path(str(member.get("absolute_path", "")))
            if not source_id or not expected_sha or not absolute_path.is_file():
                failures.append(f"invalid_member:{c1_id}:{source_id or 'missing'}")
                continue
            actual_sha = digest(absolute_path)
            if actual_sha != expected_sha:
                failures.append(f"source_hash_mismatch:{c1_id}:{source_id}")
                continue
            current = {
                "source_id": source_id,
                "sha256": expected_sha,
                "canonical": {"absolute_path": str(absolute_path)},
            }
            if source_id in unique and unique[source_id] != current:
                failures.append(f"inconsistent_source_binding:{source_id}")
            unique[source_id] = current

    audit = {
        "status": "RQ1B_V3_C4A_SOURCE_MANIFEST_PASS_NOT_A_RESULT" if not failures else "RQ1B_V3_C4A_SOURCE_MANIFEST_FAIL_NOT_A_RESULT",
        "c1_roster": str(args.c1_roster),
        "c1_roster_sha256": digest(args.c1_roster),
        "source_count": len(unique),
        "failures": failures,
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": "Hash-verified source binding only; no card, prompt, target, strict label, selector, embedding, metric, or routing result exists.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(unique[source_id], sort_keys=True) + "\n" for source_id in sorted(unique)), encoding="utf-8")
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": audit["status"], "source_count": len(unique), "failures": len(failures)}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
