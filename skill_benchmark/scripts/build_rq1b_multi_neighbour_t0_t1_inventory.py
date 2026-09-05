#!/usr/bin/env python3
"""Build a local-only T0/T1 navigation audit for RQ1b pair-to-triad expansion.

This intentionally uses only preserved source metadata and deterministic token
overlap to help a human find possible third public artifacts. It does not make
a semantic-neighbour decision, write prompts, assign labels, run a model, or
produce a retrieval result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+.#/_-]{2,}")
STOPWORDS = {
    "about", "across", "agent", "also", "and", "are", "artifact", "artifacts", "best", "build", "building",
    "can", "check", "choose", "code", "common", "create", "creating", "does", "ensure", "example", "examples",
    "first", "for", "from", "guide", "have", "how", "includes", "including", "instructions", "into", "its",
    "keep", "key", "main", "new", "needs", "not", "one", "only", "or", "original", "output", "overview",
    "practices", "process", "provide", "public", "recommended", "references", "right", "route", "run", "skill",
    "skills", "step", "steps", "task", "template", "templates", "the", "their", "this", "tips", "use", "used",
    "user", "using", "when", "with", "workflow", "workflows", "your",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalise_terms(*values: str) -> set[str]:
    text = " ".join(values).lower()
    return {token for token in TOKEN_RE.findall(text) if token not in STOPWORDS and not token.isnumeric()}


def markdown_headings(text: str, limit: int = 8) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(1).strip())
        if len(headings) >= limit:
            break
    return headings


def preview(value: str, limit: int = 320) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 3].rstrip() + "..."


def staged_import_records(staged_root: Path) -> dict[str, dict[str, Any]]:
    """Read non-Wave-003 staged originals as candidate navigation material."""

    records: dict[str, dict[str, Any]] = {}
    for import_path in sorted(staged_root.glob("*/skills/*/source/IMPORT.json")):
        stage_name = import_path.parts[-5]
        if stage_name.startswith("wave_003-"):
            continue
        imported = json.loads(import_path.read_text(encoding="utf-8"))
        original_path = import_path.with_name("SKILL.original.md")
        if not original_path.is_file():
            continue
        skill_id = str(imported["skill_id"])
        text = original_path.read_text(encoding="utf-8")
        records[skill_id] = {
            "skill_id": skill_id,
            "source_path": str(original_path),
            "source_sha256": sha256(original_path),
            "source_bytes": original_path.stat().st_size,
            "frontmatter_name": str(imported.get("frontmatter_name") or ""),
            "frontmatter_description": str(imported.get("frontmatter_description") or ""),
            "headings": markdown_headings(text),
            "origin": str(imported.get("origin") or stage_name),
            "inventory_scope": "STAGED_PRE_WAVE003",
        }
    return records


def source_inventory_records(inventory_path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(inventory_path):
        source_path = Path(str(row["source_path"]))
        if not source_path.is_file():
            continue
        records[str(row["skill_id"])] = {
            "skill_id": str(row["skill_id"]),
            "source_path": str(source_path),
            "source_sha256": str(row["source_sha256"]),
            "source_bytes": int(row["source_bytes"]),
            "frontmatter_name": str(row.get("frontmatter_name") or ""),
            "frontmatter_description": str(row.get("frontmatter_description") or ""),
            "headings": [str(item) for item in row.get("headings") or []],
            "origin": "PRE_WAVE003_SOURCE_INVENTORY",
            "inventory_scope": "PRE_WAVE003",
        }
    return records


def draft_candidate_ids(clusters_dir: Path) -> set[str]:
    ids: set[str] = set()
    for card_path in sorted(clusters_dir.glob("*/cluster_card.md")):
        text = card_path.read_text(encoding="utf-8")
        ids.update(re.findall(r"`((?:public|wave003)-[^`]+)`", text))
    return ids


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-001", type=Path, default=ROOT / "manifest/wave_001_frozen_manifest.jsonl")
    parser.add_argument("--wave-002", type=Path, default=ROOT / "manifest/wave_002_frozen_manifest.jsonl")
    parser.add_argument("--source-inventory", type=Path, default=ROOT / "manifest/source_inventory.jsonl")
    parser.add_argument("--staged-root", type=Path, default=ROOT / "staged_sources")
    parser.add_argument("--clusters-dir", type=Path, default=ROOT / "clusters")
    parser.add_argument("--shortlist-size", type=int, default=12)
    parser.add_argument(
        "--max-term-document-frequency",
        type=float,
        default=0.03,
        help="Retain a navigation term only when it appears in at most this fraction of source records.",
    )
    parser.add_argument("--output-audit", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t0_t1_pair_audit.jsonl")
    parser.add_argument("--output-summary", type=Path, default=ROOT / "manifest/rq1b_mn_e1_t0_t1_summary.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    frozen_rows = read_jsonl(args.wave_001) + read_jsonl(args.wave_002)
    frozen_ids = {skill_id for row in frozen_rows for skill_id in row["candidate_skill_ids"]}
    frozen_hashes = {sha for row in frozen_rows for sha in row["source_hashes"].values()}
    pairs = [row for row in frozen_rows if len(row["candidate_skill_ids"]) == 2]
    triplets = [row for row in frozen_rows if len(row["candidate_skill_ids"]) == 3]
    other_cardinalities = [row["cluster_id"] for row in frozen_rows if len(row["candidate_skill_ids"]) not in {2, 3}]

    source_records = source_inventory_records(args.source_inventory)
    source_records.update(staged_import_records(args.staged_root))
    held_draft_ids = draft_candidate_ids(args.clusters_dir)

    eligible: list[dict[str, Any]] = []
    exclusion_counts: Counter[str] = Counter()
    for record in source_records.values():
        if record["skill_id"] in frozen_ids:
            exclusion_counts["already_frozen_candidate"] += 1
            continue
        if record["skill_id"] in held_draft_ids:
            exclusion_counts["held_by_existing_source_backed_draft"] += 1
            continue
        if record["source_sha256"] in frozen_hashes:
            exclusion_counts["exact_byte_duplicate_of_frozen_candidate"] += 1
            continue
        source_path = Path(record["source_path"])
        if not source_path.is_file() or sha256(source_path) != record["source_sha256"]:
            exclusion_counts["source_integrity_failure"] += 1
            continue
        record["navigation_terms"] = normalise_terms(
            record["frontmatter_name"], record["frontmatter_description"], " ".join(record["headings"])
        )
        eligible.append(record)

    # Markdown skill templates share a lot of boilerplate. Remove terms that
    # recur throughout the local source inventory before making lexical
    # navigation suggestions; this is still not a semantic similarity score.
    term_document_frequency: Counter[str] = Counter()
    for record in source_records.values():
        raw_terms = normalise_terms(
            record["frontmatter_name"], record["frontmatter_description"], " ".join(record["headings"])
        )
        term_document_frequency.update(raw_terms)
    max_document_frequency = max(1, int(len(source_records) * args.max_term_document_frequency))
    for record in source_records.values():
        raw_terms = normalise_terms(
            record["frontmatter_name"], record["frontmatter_description"], " ".join(record["headings"])
        )
        record["navigation_terms"] = {term for term in raw_terms if term_document_frequency[term] <= max_document_frequency}

    if other_cardinalities:
        raise SystemExit(f"Unexpected frozen candidate cardinalities: {other_cardinalities}")
    if len(frozen_ids) != 163:
        raise SystemExit(f"Expected 163 frozen candidate IDs, found {len(frozen_ids)}")
    if len(pairs) != 74 or len(triplets) != 5:
        raise SystemExit(f"Expected 74 pairs and 5 triplets, found {len(pairs)} and {len(triplets)}")

    audit_rows: list[dict[str, Any]] = []
    for pair in sorted(pairs, key=lambda row: str(row["cluster_id"])):
        first_id, second_id = pair["candidate_skill_ids"]
        first = source_records.get(first_id)
        second = source_records.get(second_id)
        if not first or not second:
            audit_rows.append(
                {
                    "e1_status": "T0_FAIL_FROZEN_SOURCE_NOT_IN_LOCAL_NAVIGATION_INVENTORY",
                    "cluster_id": pair["cluster_id"],
                    "candidate_skill_ids": pair["candidate_skill_ids"],
                    "missing_candidate_ids": [skill_id for skill_id in pair["candidate_skill_ids"] if skill_id not in source_records],
                }
            )
            continue

        first_terms = normalise_terms(first["frontmatter_name"], first["frontmatter_description"], " ".join(first["headings"]))
        second_terms = normalise_terms(second["frontmatter_name"], second["frontmatter_description"], " ".join(second["headings"]))
        shared_terms = first_terms & second_terms
        ranked: list[tuple[tuple[int, int, int, str], dict[str, Any]]] = []
        for candidate in eligible:
            candidate_terms = candidate["navigation_terms"]
            overlap_first = first_terms & candidate_terms
            overlap_second = second_terms & candidate_terms
            common_overlap = shared_terms & candidate_terms
            # A candidate must overlap both source artifacts at least once to
            # remain a navigation suggestion. This is lexical triage only.
            if not overlap_first or not overlap_second:
                continue
            sort_key = (
                len(common_overlap),
                min(len(overlap_first), len(overlap_second)),
                len(overlap_first | overlap_second),
                candidate["skill_id"],
            )
            ranked.append((sort_key, candidate))
        ranked.sort(key=lambda item: item[0], reverse=True)
        shortlist: list[dict[str, Any]] = []
        for sort_key, candidate in ranked[: args.shortlist_size]:
            candidate_terms = candidate["navigation_terms"]
            shortlist.append(
                {
                    "third_skill_id": candidate["skill_id"],
                    "source_path": candidate["source_path"],
                    "source_sha256": candidate["source_sha256"],
                    "origin": candidate["origin"],
                    "inventory_scope": candidate["inventory_scope"],
                    "name": candidate["frontmatter_name"],
                    "description_preview": preview(candidate["frontmatter_description"]),
                    "shared_navigation_terms": sorted(shared_terms & candidate_terms),
                    "overlap_with_first": sorted(first_terms & candidate_terms),
                    "overlap_with_second": sorted(second_terms & candidate_terms),
                    "navigation_rank_components": {
                        "shared_pair_term_overlap": sort_key[0],
                        "minimum_per_candidate_overlap": sort_key[1],
                        "combined_pair_overlap": sort_key[2],
                    },
                }
            )
        audit_rows.append(
            {
                "e1_status": "T1_LOCAL_NAVIGATION_SHORTLIST_NOT_A_TRIAD",
                "cluster_id": pair["cluster_id"],
                "wave_id": pair.get("wave_id", "W1"),
                "primary_field": pair["primary_field"],
                "candidate_skill_ids": [first_id, second_id],
                "candidate_hashes": pair["source_hashes"],
                "pair_source_records": [
                    {
                        "skill_id": first_id,
                        "source_path": first["source_path"],
                        "source_sha256": first["source_sha256"],
                        "name": first["frontmatter_name"],
                        "description_preview": preview(first["frontmatter_description"]),
                    },
                    {
                        "skill_id": second_id,
                        "source_path": second["source_path"],
                        "source_sha256": second["source_sha256"],
                        "name": second["frontmatter_name"],
                        "description_preview": preview(second["frontmatter_description"]),
                    },
                ],
                "pair_shared_navigation_terms": sorted(shared_terms),
                "shortlist_count": len(shortlist),
                "third_candidate_navigation_shortlist": shortlist,
                "boundary": "Lexical source-metadata navigation only. A T2 full-source screen must establish any triadic relation; this row has no prompt, label, acceptability, semantic-neighbour, selector, embedding, or retrieval decision.",
            }
        )

    args.output_audit.parent.mkdir(parents=True, exist_ok=True)
    args.output_audit.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in audit_rows), encoding="utf-8"
    )
    summary = {
        "status": "T0_T1_PASS_LOCAL_NAVIGATION_AUDIT_NOT_A_TRIAD_OR_RESULT",
        "frozen_cluster_count": len(frozen_rows),
        "frozen_pair_count": len(pairs),
        "frozen_triplet_count": len(triplets),
        "frozen_unique_candidate_count": len(frozen_ids),
        "source_navigation_record_count": len(source_records),
        "eligible_unfrozen_source_record_count": len(eligible),
        "excluded_source_record_counts": dict(sorted(exclusion_counts.items())),
        "pair_rows_written": len(audit_rows),
        "pair_t0_fail_count": sum(row["e1_status"].startswith("T0_FAIL") for row in audit_rows),
        "pair_rows_with_navigation_shortlist": sum(bool(row.get("third_candidate_navigation_shortlist")) for row in audit_rows),
        "shortlist_size_limit": args.shortlist_size,
        "max_navigation_term_document_frequency": max_document_frequency,
        "max_navigation_term_document_frequency_fraction": args.max_term_document_frequency,
        "excluded_scopes": [
            "Wave 003 source artifacts are intentionally excluded from this targeted Wave 001/002 repair pass.",
            "No semantic similarity score, embedding, model, selector, reranker, prompt, gold label, acceptable set, or retrieval result was created.",
            "All navigation suggestions require T2 complete-source review before they may be called a triad or source-backed draft.",
        ],
        "outputs": {"audit": str(args.output_audit), "summary": str(args.output_summary)},
    }
    args.output_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
