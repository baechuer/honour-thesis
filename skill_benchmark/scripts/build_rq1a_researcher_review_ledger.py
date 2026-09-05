#!/usr/bin/env python3
"""Build a pending, researcher-facing RQ1a cluster review ledger.

This creates no review decision. It only makes the authored units reviewable
one by one and preserves the difference between mechanical checks and a later
researcher sign-off.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUITE_ROOT = ROOT / "skill_benchmark/rq1a_field_discriminability"
DEFAULT_OUTPUT = SUITE_ROOT / "human_review_2026-08-30"
CORE_FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "dependency_resource",
    "boundary_not_for",
    "success_verification",
    "workflow_procedure",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def review_record(field: str, unit_path: Path) -> dict:
    unit = json.loads(unit_path.read_text(encoding="utf-8"))
    skills = unit["skills"]
    gold = next(skill for skill in skills if skill["skill_id"] == unit["gold_skill_id"])
    alternatives = [skill for skill in skills if skill["skill_id"] != unit["gold_skill_id"]]
    return {
        "schema_version": "RQ1A_RESEARCHER_REVIEW_LEDGER_V1",
        "field": field,
        "cluster_id": unit["cluster_id"],
        "unit_path": str(unit_path.relative_to(ROOT)),
        "gold_skill_id": unit["gold_skill_id"],
        "gold_field_value": gold.get(field),
        "alternative_skill_ids": [skill["skill_id"] for skill in alternatives],
        "alternative_field_values": {skill["skill_id"]: skill.get(field) for skill in alternatives},
        "prompt_variants": unit.get("prompt_variants", {}),
        "mechanical_unit_status": unit.get("status"),
        "researcher_review_status": "PENDING_RESEARCHER_REVIEW",
        "reviewer": None,
        "reviewed_at": None,
        "decisions": {
            "gold_is_unique_for_each_prompt_variant": None,
            "both_alternatives_are_plausible_near_neighbours": None,
            "target_field_is_the_decisive_skill_side_distinction": None,
            "prompt_variants_preserve_gold_intent_without_name_or_title_leakage": None,
            "retain_in_primary_rq1a": None,
        },
        "review_notes": None,
    }


def readme(records: list[dict]) -> str:
    field_counts = {field: sum(record["field"] == field for record in records) for field in CORE_FIELDS}
    lines = [
        "# RQ1a Researcher Review Ledger",
        "",
        "## Purpose",
        "",
        "This ledger makes the 350 researcher-authored RQ1a field-isolation clusters reviewable one cluster at a time. It does not itself constitute review evidence. At creation, every row is `PENDING_RESEARCHER_REVIEW` even where the source unit has passed a mechanical rubric check.",
        "",
        "## What To Review",
        "",
        "For each cluster, read its `unit.json`, the two or three prompt variants, and the three rendered sibling skills. Then decide whether: (1) the intended gold is uniquely fully adequate for every prompt variant; (2) both alternatives remain plausible near-neighbours; (3) the named target field is the decisive skill-side distinction, while shared context truly remains shared; (4) prompt wording preserves intended meaning without title/name leakage; and (5) the cluster should remain in the primary RQ1a analysis.",
        "",
        "A `NO` decision should retain a concise reason in `review_notes`. A cluster can be marked `EXCLUDE_FROM_PRIMARY_RQ1A` without deleting its frozen source/result artifact. Only rows actually reviewed by the named researcher can later be called researcher-reviewed in the thesis.",
        "",
        "## Current Scope",
        "",
        f"- Total core clusters: {len(records)}",
        *[f"- `{field}`: {field_counts[field]} clusters" for field in CORE_FIELDS],
        "- Review state at creation: 0 reviewed; all pending.",
        "- Excluded from this ledger: the `examples_test` negative-control suite, because it is not a primary operational-field causal suite.",
        "",
        "## Files",
        "",
        "- `review_ledger.jsonl`: one editable review record per core cluster.",
        "- `review_manifest.json`: deterministic inventory and generation facts.",
        "- `README.md`: this protocol.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    records = []
    for field in CORE_FIELDS:
        for unit_path in sorted((SUITE_ROOT / field / "clusters").glob("*/unit.json")):
            records.append(review_record(field, unit_path))
    if len(records) != 350:
        raise ValueError(f"expected 350 core RQ1a units, found {len(records)}")
    cluster_ids = [record["cluster_id"] for record in records]
    if len(cluster_ids) != len(set(cluster_ids)):
        raise ValueError("cluster IDs must be unique across core RQ1a suites")
    if args.check:
        print(json.dumps({"status": "PASS", "core_clusters": len(records), "pending": len(records)}, indent=2))
        return
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "review_ledger.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    manifest = {
        "schema_version": "RQ1A_RESEARCHER_REVIEW_MANIFEST_V1",
        "created_scope": "core RQ1a field-isolation suites only",
        "core_fields": list(CORE_FIELDS),
        "core_cluster_count": len(records),
        "reviewed_count_at_creation": 0,
        "pending_count_at_creation": len(records),
        "review_claim_boundary": "Mechanical rubric checks and researcher-authored design are not human-review sign-off. Thesis wording must remain pending until individual ledger rows are completed.",
    }
    (args.output_dir / "review_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "README.md").write_text(readme(records), encoding="utf-8")
    print(json.dumps({"status": "PASS", "output_dir": str(args.output_dir), "core_clusters": len(records)}, indent=2))


if __name__ == "__main__":
    main()
