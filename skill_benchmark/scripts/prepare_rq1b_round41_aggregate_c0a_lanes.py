#!/usr/bin/env python3
"""Partition the Round 41 aggregate pool into disjoint metadata-only C0A lanes."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


LANES = {
    "document_research": ("pdf", "document", "docx", "slide", "presentation", "spreadsheet", "xlsx", "research", "report", "citation", "literature", "paper"),
    "product_design": ("frontend", "web", "mobile", "android", "ios", "react", "flutter", "ui", "ux", "design", "game", "accessibility"),
    "systems_data_security": ("test", "testing", "security", "cloud", "database", "deployment", "devops", "observability", "monitor", "incident", "infrastructure", "kubernetes", "api"),
    "business_operations": ("finance", "legal", "contract", "marketing", "sales", "crm", "customer", "procurement", "recruit", "analytics", "investment", "compliance"),
    "content_productivity": ("writing", "content", "social", "video", "image", "calendar", "email", "meeting", "productivity", "translation", "communication"),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def text(row: dict[str, Any]) -> str:
    values = (
        row.get("source_name"),
        row.get("source_description_preview"),
        row.get("source_heading_preview"),
        row.get("source_repository_path"),
    )
    return " ".join(str(value or "") for value in values).lower()


def score_lane(row: dict[str, Any], keywords: tuple[str, ...]) -> int:
    value = text(row)
    return sum(len(re.findall(rf"(?<![a-z0-9]){re.escape(word)}(?![a-z0-9])", value)) for word in keywords)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--maximum-per-origin", type=int, default=6)
    parser.add_argument("--maximum-per-lane", type=int, default=180)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pool = read_jsonl(args.pool)
    assignments: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    unassigned = 0
    for row in pool:
        scores = {lane: score_lane(row, keywords) for lane, keywords in LANES.items()}
        best_score = max(scores.values())
        if best_score == 0:
            unassigned += 1
            continue
        best_lane = next(lane for lane in LANES if scores[lane] == best_score)
        assignments[best_lane].append((best_score, row))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    lane_counts: dict[str, dict[str, int]] = {}
    for lane in LANES:
        selected: list[dict[str, Any]] = []
        by_origin: Counter[str] = Counter()
        for score, row in sorted(assignments[lane], key=lambda item: (-item[0], str(item[1]["origin"]), str(item[1]["source_repository_path"]), str(item[1]["skill_id"]))):
            origin = str(row["origin"])
            if by_origin[origin] >= args.maximum_per_origin or len(selected) >= args.maximum_per_lane:
                continue
            by_origin[origin] += 1
            selected.append({
                "c0a_status": "SOURCE_NAVIGATION_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT",
                "c0a_lane": lane,
                "metadata_keyword_score": score,
                "fresh_round41_source": "m1_round41_" in str(row.get("source_inventory", "")),
                **row,
                "exclusions": [
                    "This card contains only source navigation metadata, not an original source body.",
                    "Keyword assignment is an administrative work partition, not semantic peer validation.",
                    "No cluster, prompt, label, acceptable set, retrieval input, model call, metric, or result exists.",
                ],
            })
        output = args.output_dir / f"c0a_round41_aggregate_{lane}_navigation.jsonl"
        output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in selected), encoding="utf-8")
        outputs[lane] = str(output)
        lane_counts[lane] = {"source_records": len(selected), "origins": len(by_origin), "fresh_round41_records": sum(row["fresh_round41_source"] for row in selected)}

    summary = {
        "status": "C0A_ROUND41_AGGREGATE_DISJOINT_METADATA_LANES_READY_NOT_A_CLUSTER_OR_RESULT",
        "pool_input_count": len(pool),
        "unassigned_zero_keyword_count": unassigned,
        "assignment_rule": "Each source is assigned to its highest fixed keyword lane; ties use the declared lane order. Per-origin and per-lane caps are administrative diversity controls only.",
        "maximum_per_origin": args.maximum_per_origin,
        "maximum_per_lane": args.maximum_per_lane,
        "lane_counts": lane_counts,
        "outputs": outputs,
        "exclusions": [
            "C0A agents may propose directions from metadata but may not read original source bodies.",
            "Any proposal must still pass source-isolated C0B, C1, C2/C3, blind C4, C5, and C6.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "lane_counts": lane_counts, "unassigned_zero_keyword_count": unassigned}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
