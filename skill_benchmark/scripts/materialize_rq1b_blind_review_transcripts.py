#!/usr/bin/env python3
"""Recover exact local RQ1b blind-review tables from completed agent sessions.

The source files are local Codex session transcripts, not an external service.
This script copies only the reviewer role, original blinded instruction, and
final response table into the workspace so a frozen manifest is auditable.
It does not ask a model to review anything again and does not inspect any
authoring packet, source map, selection, or retrieval result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REVIEWER_RE = re.compile(r"You are blinded reviewer ([AB][123])")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output_text(message: dict[str, Any]) -> str:
    return "\n".join(
        part.get("text", "")
        for part in message.get("content", [])
        if part.get("type") == "output_text"
    ).strip()


def input_text(message: dict[str, Any]) -> str:
    return "\n".join(
        part.get("text", "")
        for part in message.get("content", [])
        if part.get("type") == "input_text"
    ).strip()


def recover(path: Path) -> tuple[str, str, str]:
    reviewer = None
    instruction = None
    final = None
    for line in path.read_text().splitlines():
        row = json.loads(line)
        payload = row.get("payload", {})
        if payload.get("type") != "message":
            continue
        if payload.get("role") == "user":
            text = input_text(payload)
            match = REVIEWER_RE.search(text)
            if match:
                reviewer = match.group(1)
                instruction = text
        elif payload.get("role") == "assistant" and payload.get("phase") == "final_answer":
            text = output_text(payload)
            if text.startswith("| packet_id | task | acceptable candidates"):
                final = text
    if reviewer is None or instruction is None or final is None:
        raise ValueError(f"not a complete blinded-review transcript: {path}")
    return reviewer, instruction, final


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sessions", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    recovered = [recover(path) + (path,) for path in args.sessions]
    reviewer_ids = [item[0] for item in recovered]
    if set(reviewer_ids) != {"A1", "B1", "A2", "B2", "A3", "B3"}:
        raise SystemExit(f"expected A1/B1/A2/B2/A3/B3 exactly, got {reviewer_ids}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for reviewer, instruction, final, source_path in sorted(recovered):
        output_path = args.output_dir / f"{reviewer}.md"
        output_path.write_text(
            "# RQ1b Wave 001 Blinded Reviewer " + reviewer + "\n\n"
            "Status: `RECOVERED LOCAL REVIEW TRANSCRIPT / NOT HUMAN REVIEW / NO RETRIEVAL`\n\n"
            "## Original Instruction\n\n"
            + instruction
            + "\n\n## Returned Candidate Labels\n\n"
            + final
            + "\n"
        )
        records.append({
            "reviewer": reviewer,
            "source_session_path": str(source_path),
            "source_session_sha256": sha256(source_path),
            "recovered_response_path": str(output_path),
            "recovered_response_sha256": sha256(output_path),
        })
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({
        "status": "RECOVERED_LOCAL_MODEL_ASSISTED_BLIND_REVIEW_RECORDS",
        "reviewers": records,
    }, indent=2) + "\n")
    print(json.dumps({"reviewer_count": len(records), "manifest": str(args.manifest)}, indent=2))


if __name__ == "__main__":
    main()
