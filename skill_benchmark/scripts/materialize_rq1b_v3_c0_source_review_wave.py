#!/usr/bin/env python3
"""Materialise a diversified, source-only C0 review wave from lexical triad drafts.

This is an administrative triage step. It does not create prompts, gold labels,
field annotations, selector inputs, or a scoreable benchmark.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-c0-source-review-wave-v1"
GENERIC_SHARED_TERMS = {
    "analysis", "architecture", "assistant", "automation", "best", "build",
    "code", "configuration", "data", "design", "development", "guide",
    "integration", "management", "model", "platform", "security", "skill",
    "system", "testing", "tool", "troubleshooting", "workflow",
}
TITLE_TOKEN_RE = re.compile(r"[a-z][a-z0-9]{1,}")
CONTAINER_TITLE_PHRASES = {
    "best-practices", "best practices", "expert", "guide", "patterns",
    "universal", "workflow", "workflows",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def source_lookup(source_manifest: Path) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(source_manifest):
        canonical = row["canonical"]
        lookup[row["source_id"]] = {
            "source_id": row["source_id"],
            "sha256": row["sha256"],
            "alias_count": row["alias_count"],
            "absolute_path": canonical["absolute_path"],
            "relative_path": canonical["relative_path"],
            "origin_key": canonical["origin_key"],
            "source_root": canonical["source_root"],
        }
    return lookup


def independent_title_signal_terms(title: str, shared_terms: set[str]) -> set[str]:
    return set(TITLE_TOKEN_RE.findall(title.casefold())) - shared_terms


def has_noncontained_title_signals(row: dict[str, Any]) -> bool:
    """Remove obvious bare-topic and title-subset containers from review priority.

    This is deliberately a review-order heuristic, not a semantic rejection.
    """
    shared_terms = set(row["shared_title_terms"])
    titles = [member["title"] for member in row["members"]]
    if any(phrase in title.casefold() for title in titles for phrase in CONTAINER_TITLE_PHRASES):
        return False
    signals = [independent_title_signal_terms(title, shared_terms) for title in titles]
    if any(not terms for terms in signals):
        return False
    return not any(
        left <= right
        for left_index, left in enumerate(signals)
        for right_index, right in enumerate(signals)
        if left_index != right_index
    )


def excluded_sources_from_rosters(paths: list[Path]) -> set[str]:
    return {
        member["source_id"]
        for path in paths
        for row in read_jsonl(path)
        for member in row["members"]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-dir", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--target-triads", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--wave-id", default="W1", help="Stable local wave identity, for example W1 or W2.")
    parser.add_argument(
        "--require-noncontained-title-signals",
        action="store_true",
        help="Prioritise only triads without a bare-topic/subset/container title pattern; not a scientific exclusion.",
    )
    parser.add_argument(
        "--exclude-roster",
        type=Path,
        action="append",
        default=[],
        help="Prior C0 roster whose source IDs must not be reused; may be repeated.",
    )
    args = parser.parse_args()

    if args.output_dir.exists():
        raise ValueError(f"refusing to overwrite review wave: {args.output_dir}")
    draft_path = args.draft_dir / "cluster_drafts.jsonl"
    draft_manifest_path = args.draft_dir / "cluster_draft_manifest.json"
    draft_manifest = json.loads(draft_manifest_path.read_text())
    if not draft_manifest.get("require_distinct_normalized_titles"):
        raise ValueError("C0 review must start from the distinct-title lexical queue")
    rows = read_jsonl(draft_path)
    sources = source_lookup(args.source_manifest)
    shared_counts = Counter(tuple(row["shared_title_terms"]) for row in rows)
    excluded_source_ids = excluded_sources_from_rosters(args.exclude_roster)

    # Prefer a specific shared title signal, while enforcing one source and one
    # shared-term family per packet. This improves coverage; it is not a score.
    ranked: list[tuple[float, dict[str, Any]]] = []
    for row in rows:
        shared = tuple(row["shared_title_terms"])
        if not shared or any(term in GENERIC_SHARED_TERMS for term in shared):
            continue
        specificity = math.log((len(rows) + 1) / shared_counts[shared])
        ranked.append((row["local_fts_similarity_proxy"] + specificity, row))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["draft_id"]))

    selected: list[dict[str, Any]] = []
    used_source_ids: set[str] = set()
    used_shared_terms: set[tuple[str, ...]] = set()
    for priority, row in ranked:
        member_ids = set(row["member_source_ids"])
        shared = tuple(row["shared_title_terms"])
        if member_ids & used_source_ids or member_ids & excluded_source_ids or shared in used_shared_terms:
            continue
        if args.require_noncontained_title_signals and not has_noncontained_title_signals(row):
            continue
        if any(member_id not in sources for member_id in member_ids):
            continue
        members = []
        for draft_member in row["members"]:
            source = sources[draft_member["source_id"]]
            members.append({**draft_member, **source})
        selected.append(
            {
                "c0_review_id": f"RQ1B-V3-C0-{args.wave_id}-{len(selected) + 1:03d}",
                "lexical_draft_id": row["draft_id"],
                "triage_priority_proxy": priority,
                "shared_title_terms": list(shared),
                "independent_title_signal_terms": {
                    member["source_id"]: sorted(independent_title_signal_terms(member["title"], set(shared)))
                    for member in row["members"]
                },
                "members": members,
                "candidate_count": 3,
                "review_status": "UNREVIEWED_SOURCE_ONLY",
                "claim_boundary": "This packet is source-only C0 screening. It contains no prompt, intended winner, gold label, field annotation, selector output, or metric.",
                "review_questions": [
                    "Do all three sources plausibly occupy one common broad task envelope?",
                    "Does each source specify a distinct operational role, prerequisite, input-output chain, boundary, dependency, or procedure that could make a later request route differently?",
                    "Is any member merely a copied implementation, container, interface-only wrapper, or broad umbrella rather than a distinct candidate skill?",
                    "Can the triad advance to C1 source-evidence construction without inventing a prompt or label?",
                ],
                "allowed_outcomes": [
                    "ADVANCE_C1_SOURCE_EVIDENCE",
                    "REJECT_NO_COMMON_ENVELOPE",
                    "REJECT_NONPARALLEL_OR_COMPONENT",
                    "REJECT_COPY_OR_DERIVATIVE",
                    "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
                    "NEEDS_PARENT_REVIEW",
                ],
            }
        )
        used_source_ids.update(member_ids)
        used_shared_terms.add(shared)
        if len(selected) == args.target_triads:
            break
    if len(selected) != args.target_triads:
        raise ValueError(f"only selected {len(selected)} / {args.target_triads} diversified triads")

    staging = args.output_dir.parent / f".{args.output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        (staging / "c0_review_roster.jsonl").write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in selected)
        )
        for start in range(0, len(selected), args.batch_size):
            batch = selected[start : start + args.batch_size]
            batch_number = start // args.batch_size + 1
            (staging / f"batch_{batch_number:02d}.json").write_text(
                json.dumps(
                    {
                        "review_scope": "SOURCE_ONLY_C0",
                        "instructions": "Read only the listed original source artifacts. Do not inspect prompts, labels, prior results, representations, or selector outputs. Return one allowed outcome and exact source evidence for each triad.",
                        "items": batch,
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
        manifest = {
            "status": "RQ1B_V3_C0_SOURCE_REVIEW_WAVE_MATERIALISED_LOCAL_ONLY",
            "version": VERSION,
            "draft_manifest_sha256": sha256_file(draft_manifest_path),
            "source_manifest_sha256": sha256_file(args.source_manifest),
            "triads": len(selected),
            "batches": math.ceil(len(selected) / args.batch_size),
            "batch_size": args.batch_size,
            "wave_id": args.wave_id,
            "source_reuse_count": len(used_source_ids),
            "reused_sources": 0,
            "excluded_prior_roster_source_count": len(excluded_source_ids),
            "excluded_prior_rosters": [str(path) for path in args.exclude_roster],
            "require_noncontained_title_signals": args.require_noncontained_title_signals,
            "network_calls": 0,
            "texts_transmitted": 0,
            "claim_boundary": "Materialisation is a diversified source-only triage roster. It is not semantic validation, a strict-gold decision, a field-presence audit, or a retrieval experiment.",
            "artifacts": {"c0_review_roster.jsonl": sha256_file(staging / "c0_review_roster.jsonl")},
        }
        (staging / "c0_review_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(args.output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
