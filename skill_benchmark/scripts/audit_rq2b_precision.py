#!/usr/bin/env python3
"""Prospective, outcome-free precision scenarios for RQ2b paired contrasts."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "skill_benchmark" / "outputs" / "rq2b" / "preflight"
PROMPTS = PREFLIGHT / "prompt_inventory.jsonl"
OUTPUT_JSON = PREFLIGHT / "precision_audit.json"
OUTPUT_MD = PREFLIGHT / "precision_audit.md"
ONE_SIDED_Z_95 = 1.6448536269514722
DISCORDANCE_SCENARIOS = (0.05, 0.10, 0.20)


def main() -> None:
    rows = [
        json.loads(line)
        for line in PROMPTS.read_text(encoding="utf-8").splitlines()
        if line
    ]
    strata = {}
    for stratum in ("controlled", "public_gold"):
        selected = [row for row in rows if row["stratum"] == stratum]
        groups = Counter(row["group"] for row in selected)
        scenarios = []
        for discordance in DISCORDANCE_SCENARIOS:
            independent_pair_se = math.sqrt(discordance / len(selected))
            scenarios.append(
                {
                    "discordance_rate": discordance,
                    "independent_pair_standard_error": independent_pair_se,
                    "one_sided_95_half_width": ONE_SIDED_Z_95 * independent_pair_se,
                }
            )
        strata[stratum] = {
            "prompt_count": len(selected),
            "group_count": len(groups),
            "minimum_group_size": min(groups.values()),
            "maximum_group_size": max(groups.values()),
            "scenarios": scenarios,
        }

    report = {
        "schema_version": "rq2b-prefreeze-precision-audit-v1",
        "state": "prospective_outcome_free_not_result",
        "network_calls": 0,
        "noninferiority_margin": 0.03,
        "one_sided_confidence": 0.95,
        "method": "independent-pair nominal lower-bound scenarios",
        "grouping_field": "prompt_inventory.group",
        "limitation": (
            "Family-group dependence is not estimated without outcomes and may "
            "increase uncertainty beyond these nominal independent-pair values."
        ),
        "strata": strata,
    }
    OUTPUT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# RQ2b Prospective Precision Audit",
        "",
        "This is outcome-free design evidence, not a scientific result.",
        "",
        "| Stratum | Prompts | Groups | Discordance | One-sided 95% nominal half-width |",
        "|---|---:|---:|---:|---:|",
    ]
    for stratum, data in strata.items():
        for scenario in data["scenarios"]:
            lines.append(
                f"| {stratum} | {data['prompt_count']} | {data['group_count']} | "
                f"{scenario['discordance_rate']:.0%} | "
                f"{scenario['one_sided_95_half_width']:.2%} |"
            )
    lines.extend(
        [
            "",
            "Family-group dependence may widen the final grouped-bootstrap interval. "
            "The 3-point margin is therefore stringent and can legitimately produce "
            "an inconclusive non-inferiority decision.",
            "",
        ]
    )
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report["strata"], indent=2))


if __name__ == "__main__":
    main()
