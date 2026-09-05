#!/usr/bin/env python3
"""Generate local lexical near-neighbour triad drafts from a frozen RQ1b v3 source frame."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import time
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-local-fts-triad-discovery-v1"
TOKEN_RE = re.compile(r"[a-z][a-z0-9]{2,}")
STOPWORDS = {
    "agent", "agents", "ai", "and", "assistant", "automation", "best", "builder", "code", "claude", "coding", "for", "guide", "how", "in", "kit", "management", "skill", "skills", "the", "this", "to", "tool", "tools", "using", "with", "workflow", "workflows",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def title_terms(title: str) -> list[str]:
    return [token for token in TOKEN_RE.findall(title.casefold()) if token not in STOPWORDS]


def normalized_title(title: str) -> str:
    return " ".join(TOKEN_RE.findall(title.casefold()))


def fts_query(terms: list[str]) -> str | None:
    unique = list(dict.fromkeys(terms))[:4]
    return " OR ".join(unique) if unique else None


def build(
    source_frame_dir: Path,
    index_dir: Path,
    output_dir: Path,
    max_drafts: int,
    require_distinct_normalized_titles: bool,
) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite candidate drafts: {output_dir}")
    certificate_path = source_frame_dir / "SOURCE_FRAME_FREEZE_CERTIFICATE.json"
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("status") != "RQ1B_V3_PUBLIC_SOURCE_FRAME_FROZEN_LOCAL_ONLY":
        raise ValueError("source frame is not frozen")
    census_path = index_dir / "structural_census.json"
    census = json.loads(census_path.read_text())
    if census.get("source_frame_certificate_sha256") != sha256_file(certificate_path):
        raise ValueError("source-index/source-frame binding drift")
    database_path = index_dir / "source_discovery.sqlite"
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        metadata_rows = connection.execute(
            "SELECT source_id, origin_key, title, lexical_token_count FROM source_metadata WHERE lexical_token_count >= 100 ORDER BY source_id"
        ).fetchall()
        metadata = {row["source_id"]: dict(row) for row in metadata_rows}
        drafts_by_key: dict[tuple[str, ...], dict[str, Any]] = {}
        queried = zero_neighbor = 0
        started = time.perf_counter()
        for position, seed in enumerate(metadata_rows, start=1):
            terms = title_terms(seed["title"])
            query = fts_query(terms)
            if query is None:
                continue
            queried += 1
            matches = connection.execute(
                "SELECT source_id, bm25(source_fts) AS bm25_rank FROM source_fts WHERE source_fts MATCH ? ORDER BY bm25(source_fts) LIMIT 36",
                (query,),
            ).fetchall()
            eligible = []
            seed_terms = set(terms)
            for match in matches:
                candidate = metadata.get(match["source_id"])
                if candidate is None or candidate["source_id"] == seed["source_id"]:
                    continue
                if candidate["origin_key"] == seed["origin_key"]:
                    continue
                common = sorted(seed_terms & set(title_terms(candidate["title"])))
                if not common:
                    continue
                eligible.append((candidate, common, -float(match["bm25_rank"])))
            if len(eligible) < 2:
                zero_neighbor += 1
                continue
            selected = []
            used_origins = {seed["origin_key"]}
            used_titles = {normalized_title(seed["title"])}
            for candidate, common, rank in eligible:
                if candidate["origin_key"] in used_origins:
                    continue
                candidate_title = normalized_title(candidate["title"])
                if require_distinct_normalized_titles and candidate_title in used_titles:
                    continue
                selected.append((candidate, common, rank))
                used_origins.add(candidate["origin_key"])
                used_titles.add(candidate_title)
                if len(selected) == 2:
                    break
            if len(selected) != 2:
                continue
            members = [dict(seed), *(candidate for candidate, _, _ in selected)]
            member_ids = tuple(sorted(member["source_id"] for member in members))
            common_terms = sorted(set.intersection(*(set(title_terms(member["title"])) for member in members)))
            if not common_terms:
                continue
            proxy = sum(rank for _, _, rank in selected) / len(selected)
            existing = drafts_by_key.get(member_ids)
            draft = {
                "draft_id": f"RQ1B-V3-DRAFT-{len(drafts_by_key) + 1:06d}",
                "member_source_ids": list(member_ids),
                "candidate_count": 3,
                "distinct_origin_count": len({member["origin_key"] for member in members}),
                "members": [
                    {
                        "source_id": member["source_id"],
                        "origin_key": member["origin_key"],
                        "title": member["title"],
                        "lexical_token_count": member["lexical_token_count"],
                    }
                    for member in members
                ],
                "shared_title_terms": common_terms,
                "local_fts_similarity_proxy": proxy,
                "seed_source_id": seed["source_id"],
                "source_status": (
                    "LOCAL_LEXICAL_DISTINCT_TITLE_DRAFT_ONLY"
                    if require_distinct_normalized_titles
                    else "LOCAL_LEXICAL_DRAFT_ONLY"
                ),
                "claim_boundary": "Shared title terms and FTS rank are triage aids. Distinct normalized titles only remove obvious copied-name candidates; neither condition establishes semantic similarity, strict-gold, field-contrast, or selector evidence.",
            }
            if existing is None or draft["local_fts_similarity_proxy"] > existing["local_fts_similarity_proxy"]:
                drafts_by_key[member_ids] = draft
            if position % 500 == 0 or position == len(metadata_rows):
                print(f"CLUSTER_DRAFT_PROGRESS seeds={position}/{len(metadata_rows)} drafts={len(drafts_by_key)}", flush=True)
        drafts = sorted(drafts_by_key.values(), key=lambda row: (-row["local_fts_similarity_proxy"], row["member_source_ids"]))[:max_drafts]
    finally:
        connection.close()
    for index, row in enumerate(drafts, start=1):
        row["draft_id"] = f"RQ1B-V3-DRAFT-{index:06d}"
    staging = output_dir.parent / f".{output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        drafts_path = staging / "cluster_drafts.jsonl"
        drafts_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in drafts))
        manifest = {
            "status": "RQ1B_V3_CLUSTER_DRAFTS_LOCAL_ONLY",
            "builder_version": VERSION,
            "source_frame_certificate_sha256": sha256_file(certificate_path),
            "structural_census_sha256": sha256_file(census_path),
            "input_sources_considered": len(metadata_rows),
            "seeds_queried": queried,
            "seeds_without_two_cross-origin_title-neighbours": zero_neighbor,
            "draft_triads_retained": len(drafts),
            "max_drafts": max_drafts,
            "require_distinct_normalized_titles": require_distinct_normalized_titles,
            "network_calls": 0,
            "texts_transmitted": 0,
            "elapsed_seconds": time.perf_counter() - started,
            "artifacts": {"cluster_drafts.jsonl": sha256_file(drafts_path)},
            "next_gate": "Source-only semantic-envelope and operational-contrast review. Drafts may be rejected without becoming cluster failures.",
        }
        (staging / "cluster_draft_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-frame-dir", type=Path, required=True)
    parser.add_argument("--index-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-drafts", type=int, default=10_000)
    parser.add_argument(
        "--require-distinct-normalized-titles",
        action="store_true",
        help="Exclude triads with repeated normalized titles; intended only as an obvious-copy triage filter.",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            build(
                args.source_frame_dir,
                args.index_dir,
                args.output_dir,
                args.max_drafts,
                args.require_distinct_normalized_titles,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
