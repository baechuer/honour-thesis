#!/usr/bin/env python3
"""Record path-level source-artifact risks for Wave 034 T0 review.

This deterministic inventory is only a reading-order aid. It makes no
semantic, cluster, routing, prompt, label, or scientific eligibility decision.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


RISK_MARKERS = {
    "template_path": ("template",),
    "evaluation_path": ("/eval", "/grader", "/grading"),
    "test_path": ("/test", "tests/"),
    "repository_metadata_path": (".github/", "issue_template"),
    "example_path": ("example", "sample"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--status-prefix", default="RQ1B_V3_W34")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = [
        json.loads(line)
        for line in args.inventory.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    risk_counts: Counter[str] = Counter()
    rows = []
    for record in records:
        path = str(record["artifact_path"]).lower()
        markers = sorted(
            label for label, fragments in RISK_MARKERS.items() if any(fragment in path for fragment in fragments)
        )
        risk_counts.update(markers)
        rows.append(
            {
                "source_id": record["amendment_source_id"],
                "artifact_path": record["artifact_path"],
                "repository_ref": record["repository_ref"],
                "path_level_risk_markers": markers,
                "status": f"{args.status_prefix}_T0_PATH_RISK_READING_AID_NOT_A_CLUSTER",
                "claim_boundary": "Path strings are mechanical reading-priority signals only. A marker does not reject a source; absence of a marker does not establish a natural skill, shared envelope, peer alternative, C1 eligibility, prompt, label, selector input, or result.",
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    report = {
        "status": f"{args.status_prefix}_T0_PATH_RISK_INVENTORY_PASS_NOT_A_CLUSTER",
        "source_count": len(rows),
        "path_risk_counts": dict(sorted(risk_counts.items())),
        "network_calls": 0,
        "texts_transmitted": 0,
        "boundary": "Path-level structural risk inventory only; no automatic rejection or scientific conclusion.",
    }
    args.output.with_name("T0_PATH_RISK_INVENTORY_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
