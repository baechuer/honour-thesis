#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


PRIORITY_FIELDS = [
    "routing_trigger",
    "resources_references",
    "safety_side_effects",
    "constraints_boundaries",
    "input_precondition",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pick_cases(disagreements: list[dict[str, Any]], per_field: int, total: int) -> list[dict[str, Any]]:
    by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in disagreements:
        by_field[item["field"]].append(item)

    selected: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for field in PRIORITY_FIELDS:
        field_items = sorted(
            by_field.get(field, []),
            key=lambda item: (item["relation"], item["skill"]),
        )
        for item in field_items[:per_field]:
            key = (item["skill"], item["field"], item["relation"])
            if key not in seen:
                selected.append(item)
                seen.add(key)

    remaining = sorted(
        disagreements,
        key=lambda item: (
            0 if item["field"] in PRIORITY_FIELDS else 1,
            item["field"],
            item["relation"],
            item["skill"],
        ),
    )
    for item in remaining:
        if len(selected) >= total:
            break
        key = (item["skill"], item["field"], item["relation"])
        if key not in seen:
            selected.append(item)
            seen.add(key)
    return selected[:total]


def clean(value: Any, limit: int = 400) -> str:
    if isinstance(value, list):
        text = " / ".join(str(item) for item in value)
    else:
        text = str(value or "")
    text = text.replace("|", "\\|").replace("\n", " ")
    return text[:limit]


def render(summary: dict[str, Any], cases: list[dict[str, Any]]) -> str:
    lines = [
        "# Public Skill Field Disagreement Review Packet",
        "",
        "Purpose: targeted manual review of heuristic/model disagreements from the 200-skill public field audit.",
        "",
        f"- Skills compared in source report: {summary['skills_compared']}",
        f"- Total selected disagreement cases: {len(cases)}",
        "",
        "Review labels to fill:",
        "",
        "- `heuristic_correct`",
        "- `model_correct`",
        "- `both_partly_correct`",
        "- `both_wrong_or_unclear`",
        "- `definition_needs_refinement`",
        "",
        "Priority fields: routing trigger, resources/references, safety/side-effects, constraints/boundaries, and input/precondition.",
        "",
        "## Field Agreement Snapshot",
        "",
        "| Field | Agreement | Heuristic Only | Model Only |",
        "|---|---:|---:|---:|",
    ]
    for field, data in summary["field_summary"].items():
        lines.append(
            f"| `{field}` | {data['agreement_pct']:.1%} | "
            f"{data['heuristic_only']} | {data['model_only']} |"
        )

    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Skill | Field | Type | Heuristic | Model | Heuristic Evidence | Model Evidence | Model Reason | Manual Decision | Notes |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in cases:
        lines.append(
            f"| `{item['skill']}` | `{item['field']}` | `{item['relation']}` | "
            f"`{item['heuristic_status']}` | `{item['model_status']}` | "
            f"{clean(item.get('heuristic_evidence'))} | {clean(item.get('model_evidence'))} | "
            f"{clean(item.get('model_reason'), 260)} |  |  |"
        )

    lines.extend(
        [
            "",
            "## How To Use This Packet",
            "",
            "- If many `routing_trigger` heuristic-only cases are false positives, refine the definition so broad descriptions do not automatically count as high-quality routing conditions.",
            "- If many `resources_references` heuristic-only cases are false positives, require concrete files, URLs, directories, bundled references, or linked skills.",
            "- If `safety_side_effects` remains sparse after manual review, classify it as proposed/weakly observed rather than an established public-skill convention.",
            "- Use the reviewed cases to finalize observed/extractable/proposed field categories before Step 7 field ablations are interpreted.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Build a targeted manual review packet for public-skill field disagreements.")
    parser.add_argument("--agreement-json", default=str(repo_root / "outputs" / "public_skill_field_agreement_report.json"))
    parser.add_argument("--output-md", default=str(repo_root / "outputs" / "public_skill_field_disagreement_review_packet.md"))
    parser.add_argument("--per-field", type=int, default=8)
    parser.add_argument("--total", type=int, default=50)
    args = parser.parse_args()

    summary = load_json(Path(args.agreement_json))
    cases = pick_cases(summary["disagreements"], args.per_field, args.total)
    output = Path(args.output_md)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(summary, cases), encoding="utf-8")
    print(f"Selected disagreement cases: {len(cases)}")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
