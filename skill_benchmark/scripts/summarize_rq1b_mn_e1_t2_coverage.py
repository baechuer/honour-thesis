#!/usr/bin/env python3
"""Summarise E1 T2 coverage without re-adjudicating any source screen.

Codes are deterministic, non-exclusive labels over already recorded
parent-curator rejection rationale. They are a reporting aid, not a new T2
decision, semantic-fidelity result, or retrieval result.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
REASON_CODES = {
    "NO_SHARED_ENVELOPE_OR_ORTHOGONAL": re.compile(r"no shared|lacks? (?:the )?.{0,35} envelope|outside .{0,35} envelope|not inside .{0,35} envelope|outside the same decision object|no source-defined broad|orthogonal|unrelated|obviously mismatched|not a plausible parallel", re.I),
    "CONTAINER_OR_SUBSUMPTION": re.compile(r"container|subsum|general (?:extractor|workflow|route|tool)|broader .{0,35}(?:route|workflow|programme|program)", re.I),
    "PREREQUISITE_OR_LATER_STAGE": re.compile(r"prerequisite|later.stage|after .{0,35}(?:draft|first)|staged roles?|sequential|downstream|creation-to-revision", re.I),
    "COMPOSABLE_OR_SUPPORTING_COMPONENT": re.compile(r"composable|complementary|supporting (?:work|component)|component|explicitly chain|broad-audit/sub-protocol|policy-to-implementation", re.I),
    "SPECIALISED_IMPLEMENTATION_OR_SCOPE": re.compile(r"speciali[sz]ed|package|framework|model.specific|named .{0,35}(?:package|tool)|conditional specialisation", re.I),
    "INTERFACE_OR_CONFIGURATION_BOUND": re.compile(r"interface|configur|table.columns|schema.driven", re.I),
    "DUPLICATE_OR_NOMINAL_VARIANT": re.compile(r"same (?:general |externally )?(?:configured )?(?:tabular|extract|workflow)|identical|only .{0,35}(?:name|metadata)", re.I),
    "TRUE_SUBSTITUTE_OR_MATERIAL_OVERLAP": re.compile(r"plausibly satisfy|plausible substitute|overlaps materially|multi.adequate", re.I),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t2", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t2_source_screening.jsonl")
    parser.add_argument("--output", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t2_coverage_report_2026-08-26.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_jsonl(args.t2)
    parent_ids = {str(row.get("parent_pair_cluster_id") or row.get("cluster_id")) for row in rows}
    rejection_rows = [row for row in rows if row["e1_status"] == "T2_REJECTED_THIRD_CANDIDATE_RETAINS_FROZEN_PAIR"]
    coded: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for row in rejection_rows:
        reason = str(row["rejection_reason"])
        codes = [code for code, pattern in REASON_CODES.items() if pattern.search(reason)]
        if not codes:
            codes = ["UNCLASSIFIED_REQUIRES_PARENT_READING"]
        counts.update(codes)
        coded.append(
            {
                "screen_id": row["screen_id"],
                "parent_pair_cluster_id": row["parent_pair_cluster_id"],
                "primary_field": row["primary_field"],
                "reason_codes_nonexclusive": codes,
                "rejection_reason": reason,
            }
        )
    report = {
        "status": "T2_COVERAGE_AND_REASON_CODE_REPORT_NOT_A_RE_ADJUDICATION",
        "parent_pair_coverage": len(parent_ids),
        "source_screen_decision_count": len(rows),
        "source_screen_status_counts": dict(sorted(Counter(row["e1_status"] for row in rows).items())),
        "rejection_record_count": len(rejection_rows),
        "reason_code_counts_nonexclusive": dict(sorted(counts.items())),
        "unclassified_rejection_count": counts["UNCLASSIFIED_REQUIRES_PARENT_READING"],
        "coded_rejection_records": coded,
        "boundary": "Codes are deterministic reporting labels applied to existing parent-curator rationale. They do not add, replace, or alter a T2 decision; categories are non-exclusive and are not retrieval or semantic-fidelity results.",
    }
    if len(parent_ids) != 74:
        raise SystemExit(f"Expected 74 covered parent pairs, found {len(parent_ids)}")
    if len(rejection_rows) != 69:
        raise SystemExit(f"Expected 69 rejection rows, found {len(rejection_rows)}")
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in report if key != "coded_rejection_records"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
