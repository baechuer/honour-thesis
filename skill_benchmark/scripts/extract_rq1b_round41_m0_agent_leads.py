#!/usr/bin/env python3
"""Extract JSONL navigation leads from persisted, unmodified RQ1b M0 replies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED = {
    "repository_url",
    "source_repository_path",
    "skill_locator_url",
    "skill_title_or_name",
    "capability_summary",
    "discovery_domain",
    "discovery_rationale",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--round-label", default="R41")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    accepted = 0
    failures: list[str] = []
    files: list[str] = []
    for raw_path in sorted(args.input_dir.glob("*.md")):
        rows: list[dict[str, Any]] = []
        for line_number, source_line in enumerate(raw_path.read_text(encoding="utf-8").splitlines(), start=1):
            line = source_line.strip()
            if not (line.startswith("{") and line.endswith("}")):
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                failures.append(f"invalid_json:{raw_path.name}:{line_number}:{error.msg}")
                continue
            if not isinstance(row, dict):
                failures.append(f"non_object:{raw_path.name}:{line_number}")
                continue
            missing = sorted(key for key in REQUIRED if not str(row.get(key, "")).strip())
            if missing:
                failures.append(f"missing_fields:{raw_path.name}:{line_number}:{','.join(missing)}")
                continue
            row.pop("uncertainty", None)
            rows.append(row)
        output_path = args.output_dir / f"{raw_path.stem}.jsonl"
        output_path.write_text(
            "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
        files.append(str(output_path))
        accepted += len(rows)
    summary = {
        "status": f"{args.round_label}_M0_AGENT_LEADS_EXTRACTED_NOT_ADMITTED" if not failures else f"{args.round_label}_M0_AGENT_LEADS_EXTRACTED_WITH_FORMAT_WARNINGS_NOT_ADMITTED",
        "raw_reply_file_count": len(files),
        "accepted_navigation_lead_count": accepted,
        "format_failures": failures,
        "output_files": files,
        "exclusions": [
            "Extraction changes no agent-provided lead claim and does not validate a path or source body.",
            "These rows are public navigation leads only, not admitted sources, candidate clusters, prompts, labels, or results.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "raw_reply_file_count", "accepted_navigation_lead_count", "format_failures")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
