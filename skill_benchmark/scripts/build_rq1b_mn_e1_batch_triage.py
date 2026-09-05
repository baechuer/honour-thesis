#!/usr/bin/env python3
"""Build a local-only E1 batch triage queue; never make a T2 decision.

The output is deliberately a pre-screen: its deterministic lexical markers
prioritise full-source human/agent curation but cannot establish whether three
public skills are structurally parallel first routes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
SIGNAL_PATTERNS = {
    "route_out": re.compile(r"\\b(not for|instead use|use .{0,45} instead|route .{0,45} to|handoff|hand off|refer to|outside (?:this )?scope)\\b", re.I),
    "prerequisite": re.compile(r"\\b(prerequisite|before (?:you|starting|using)|requires?|must have|install|set up|setup)\\b", re.I),
    "input_output_chain": re.compile(r"\\b(then|after (?:that|you|the)|next step|followed by|use .{0,35} output|feeds? into)\\b", re.I),
    "container": re.compile(r"\\b(end-to-end|all-in-one|comprehensive|unified|complete workflow|every phase)\\b", re.I),
    "specialised_implementation": re.compile(r"\\b(only for|specifically for|dedicated to|speciali[sz]ed|framework|package|library|version)\\b", re.I),
    "interface_only": re.compile(r"\\b(configuration|config(?:ure|uration)?|yaml|json|cli|api|table[- ]columns|parameter(?:s|ise)?)\\b", re.I),
}
HIGH_RISK_KINDS = {"route_out", "prerequisite", "input_output_chain", "container", "specialised_implementation", "interface_only"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def json_line(value: dict[str, Any]) -> str:
    """Fail rather than emitting non-standard JSON into an audit manifest."""

    return json.dumps(value, ensure_ascii=True, sort_keys=True, allow_nan=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_family(path: str) -> str:
    parts = Path(path).parts
    if "staged_sources" in parts:
        return parts[parts.index("staged_sources") + 1]
    if "public_imported_background" in parts:
        return "public_imported_background"
    return "other_local_source_family"


def headings(text: str, limit: int = 8) -> list[str]:
    values = [match.group(1).strip() for line in text.splitlines() if (match := re.match(r"^#{1,6}\\s+(.+?)\\s*$", line))]
    return values[:limit]


def literal_signals(path: Path, limit_per_kind: int = 4) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        compact = re.sub(r"\\s+", " ", line).strip()
        if not compact:
            continue
        for kind, pattern in SIGNAL_PATTERNS.items():
            if len(result.get(kind, [])) < limit_per_kind and pattern.search(compact):
                result.setdefault(kind, []).append({"line": number, "text": compact[:360]})
    return result


def parent_sources(row: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(item) for item in row["pair_source_records"]]


def existing_t2_candidate_ids(rows: list[dict[str, Any]]) -> set[str]:
    values: set[str] = set()
    for row in rows:
        values.update(str(value) for value in row.get("candidate_skill_ids", [])[2:])
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t0-t1", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t0_t1_pair_audit.jsonl")
    parser.add_argument("--t2", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t2_source_screening.jsonl")
    parser.add_argument("--max-candidates", type=int, default=12)
    parser.add_argument("--output", type=Path, default=ROOT / "manifest/rq1b_mn_e1_batch_triage_2026-08-26.jsonl")
    parser.add_argument("--summary", type=Path, default=ROOT / "manifest/rq1b_mn_e1_batch_triage_2026-08-26_summary.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    t0_rows = read_jsonl(args.t0_t1)
    t2_rows = read_jsonl(args.t2)
    covered_parent_ids = {str(row.get("parent_pair_cluster_id") or row.get("cluster_id")) for row in t2_rows}
    remaining = [row for row in t0_rows if str(row["cluster_id"]) not in covered_parent_ids]
    frozen_ids = {skill for row in t0_rows for skill in row["candidate_skill_ids"]}
    prior_t2_thirds = existing_t2_candidate_ids(t2_rows)

    occurrence: Counter[str] = Counter(
        str(candidate["third_skill_id"])
        for row in remaining
        for candidate in row.get("third_candidate_navigation_shortlist", [])[: args.max_candidates]
    )
    triage_rows: list[dict[str, Any]] = []
    category_counts: Counter[str] = Counter()

    for row in sorted(remaining, key=lambda item: str(item["cluster_id"])):
        parent_records = parent_sources(row)
        parent_integrity_ok = all(
            Path(record["source_path"]).is_file() and sha256(Path(record["source_path"])) == record["source_sha256"]
            for record in parent_records
        )
        candidate_rows: list[dict[str, Any]] = []
        for candidate in row.get("third_candidate_navigation_shortlist", [])[: args.max_candidates]:
            source_path = Path(candidate["source_path"])
            integrity_ok = source_path.is_file() and sha256(source_path) == candidate["source_sha256"]
            signals = literal_signals(source_path) if integrity_ok else {}
            risk_kinds = sorted(kind for kind in signals if kind in HIGH_RISK_KINDS)
            candidate_id = str(candidate["third_skill_id"])
            candidate_rows.append(
                {
                    "third_skill_id": candidate_id,
                    "source_path": str(source_path),
                    "source_sha256": candidate["source_sha256"],
                    "source_family": source_family(str(source_path)),
                    "t1_origin": candidate.get("origin"),
                    "t1_name": candidate.get("name"),
                    "t1_shared_navigation_terms": candidate.get("shared_navigation_terms", []),
                    "source_integrity_ok": integrity_ok,
                    "candidate_headings": headings(source_path.read_text(encoding="utf-8")) if integrity_ok else [],
                    "literal_structural_signals": signals,
                    "deterministic_risk_kinds": risk_kinds,
                    "is_frozen_candidate": candidate_id in frozen_ids,
                    "appears_as_prior_t2_third": candidate_id in prior_t2_thirds,
                    "same_batch_t1_shortlist_count": occurrence[candidate_id],
                }
            )

        valid_candidates = [item for item in candidate_rows if item["source_integrity_ok"] and not item["is_frozen_candidate"]]
        low_risk = [item for item in valid_candidates if not item["deterministic_risk_kinds"]]
        if not parent_integrity_ok:
            triage_status = "NEEDS_PARENT_REVIEW"
            reason = "At least one immutable parent source no longer matches its recorded hash."
        elif not valid_candidates:
            triage_status = "NO_PLAUSIBLE_THIRD"
            reason = "No source-integrity-valid, unfrozen T1 candidate remains."
        elif low_risk:
            triage_status = "READY_FOR_T2"
            reason = "At least one T1 candidate has retained shared navigation terms and no deterministic risk marker; full-source T2 must decide structural parallelism."
        elif any(item["same_batch_t1_shortlist_count"] > 1 or item["appears_as_prior_t2_third"] for item in valid_candidates):
            triage_status = "NEEDS_PARENT_REVIEW"
            reason = "Every remaining candidate has a lexical structural-risk marker and one or more reuse conflicts; parent curator must decide whether any full-source T2 review is justified."
        else:
            triage_status = "LIKELY_NONPARALLEL"
            reason = "Every retained T1 candidate has one or more deterministic route/chain, container, specialised, or interface markers; this is not a T2 rejection."
        category_counts[triage_status] += 1
        triage_rows.append(
            {
                "e1_status": "BATCH_TRIAGE_LOCAL_ONLY_NOT_A_T2_DECISION",
                "triage_status": triage_status,
                "cluster_id": row["cluster_id"],
                "wave_id": row.get("wave_id"),
                "primary_field": row["primary_field"],
                "parent_candidate_skill_ids": row["candidate_skill_ids"],
                "parent_source_hashes": row["candidate_hashes"],
                "parent_source_families": [source_family(str(item["source_path"])) for item in parent_records],
                "parent_headings": {item["skill_id"]: headings(Path(item["source_path"]).read_text(encoding="utf-8")) for item in parent_records},
                "t1_pair_shared_navigation_terms": row.get("pair_shared_navigation_terms", []),
                "t1_shortlist_count": row.get("shortlist_count", 0),
                "retained_top_candidates": candidate_rows,
                "triage_reason": reason,
                "next_action": "SOURCE_ONLY_T2" if triage_status == "READY_FOR_T2" else "PARENT_QUEUE_REVIEW",
                "boundary": "Deterministic local triage only. It does not assess semantic parallelism, triad validity, prompts, gold labels, acceptable sets, retrieval, or any scientific outcome."
            }
        )

    expected_remaining = len(t0_rows) - len(covered_parent_ids)
    if len(remaining) != expected_remaining:
        raise SystemExit(f"Coverage mismatch: expected {expected_remaining} remaining pairs, found {len(remaining)}")
    if args.output.exists():
        prior_ids = {str(row["cluster_id"]) for row in read_jsonl(args.output)}
        current_ids = {str(row["cluster_id"]) for row in triage_rows}
        if prior_ids and prior_ids != current_ids:
            raise SystemExit(
                "Refusing to overwrite a historical triage snapshot after T2 coverage changed. "
                "Use a new versioned --output and --summary path for a new triage run."
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json_line(row) for row in triage_rows), encoding="utf-8")
    summary = {
        "status": "LOCAL_BATCH_TRIAGE_COMPLETE_NOT_A_T2_OR_SCIENTIFIC_RESULT",
        "t0_t1_frozen_pair_count": len(t0_rows),
        "existing_t2_parent_coverage": len(covered_parent_ids),
        "remaining_parent_pairs_triaged": len(triage_rows),
        "coverage_total": len(covered_parent_ids) + len(triage_rows),
        "triage_status_counts": dict(sorted(category_counts.items())),
        "source_only_boundary": True,
        "no_network_or_model": True,
        "outputs": {"triage_manifest": str(args.output), "summary": str(args.summary)},
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
