#!/usr/bin/env python3
"""Build a source-only reading inventory for a public-source amendment.

The output is deliberately descriptive: artifact identifiers, provenance,
byte size, and the first literal Markdown title/headings.  It does not infer
task similarity, cluster membership, or scientific eligibility.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADING = re.compile(r"^#{1,3}\s+(.+?)\s*$")
NAME = re.compile(r"^(?:name|title)\s*:\s*[\"']?(.+?)[\"']?\s*$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--status-prefix", default="RQ1B_V3_D1_W9")
    return parser.parse_args()


def literal_markers(path: Path) -> tuple[str | None, list[str]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    name = None
    headings: list[str] = []
    for line in lines[:180]:
        if name is None:
            name_match = NAME.match(line.strip())
            if name_match:
                name = name_match.group(1).strip()
        heading_match = HEADING.match(line)
        if heading_match and len(headings) < 12:
            headings.append(heading_match.group(1).strip())
    if name is None and headings:
        name = headings[0]
    return name, headings


def main() -> int:
    args = parse_args()
    records = [json.loads(line) for line in args.amendment.read_text(encoding="utf-8").splitlines() if line]
    inventory: list[dict] = []
    for record in records:
        raw_path = Path(record["canonical"]["local_raw_path"])
        inferred_name, headings = literal_markers(raw_path)
        inventory.append(
            {
                "amendment_source_id": record["amendment_source_id"],
                "artifact_path": record["canonical"]["artifact_path"],
                "byte_count": record["byte_count"],
                "inferred_literal_name_or_first_heading": inferred_name,
                "intake_lane": record["intake_lane"],
                "local_raw_path": record["canonical"]["local_raw_path"],
                "raw_artifact_url": record["canonical"]["raw_artifact_url"],
                "repository_ref": record["canonical"]["repository_ref"],
                "source_sha256": record["canonical"]["source_sha256"],
                "literal_markdown_headings": headings,
                "status": f"{args.status_prefix}_SOURCE_ONLY_READING_INVENTORY_NOT_A_CLUSTER",
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for record in inventory:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps({"record_count": len(inventory), "status": f"{args.status_prefix}_SOURCE_ONLY_INVENTORY_PASS_NOT_A_CLUSTER"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
