#!/usr/bin/env python3
"""Prepare a disjoint, local-only RQ1b V3 Wave 037 T0 review roster.

This ranks existing lexical triage drafts after new-source discovery was
temporarily stopped by the Wave 036 GitHub API rate limit. It is only a review
ordering aid: it neither rejects nor validates a cluster.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


CONTAINER_TERMS = {
    "base", "best", "connector", "container", "docs", "framework", "guide",
    "integration", "manager", "overview", "reference", "setup", "template",
    "tutorial", "utils", "workflow", "wrapper",
}
SOURCE_ID_RE = re.compile(r"RQ1B-V3-SRC-\d{6}")
BOUNDARY = (
    "Wave 037 is a local source-only reading assignment after Wave 036 network "
    "rate limiting. Lexical rank and title-risk indicators only order T0 review; "
    "they establish no cluster, prompt, gold label, selector input, metric, "
    "field effect, retrieval result, or thesis claim."
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def historical_reviewed_ids(frame_root: Path) -> set[str]:
    """Collect only earlier C0 review and V3 C6 source references."""
    result: set[str] = set()
    for path in frame_root.glob("c0_source_review_wave_*/c0_review_roster.jsonl"):
        result.update(SOURCE_ID_RE.findall(path.read_text(encoding="utf-8")))
    for path in frame_root.glob("**/c6_freeze*/**/*.jsonl"):
        result.update(SOURCE_ID_RE.findall(path.read_text(encoding="utf-8")))
    for path in frame_root.glob("**/c6_freeze*/**/*.json"):
        result.update(SOURCE_ID_RE.findall(path.read_text(encoding="utf-8")))
    return result


def title_risk_terms(titles: list[str]) -> list[str]:
    tokens = set()
    for title in titles:
        tokens.update(token for token in re.split(r"[^a-z0-9]+", title.lower()) if token)
    return sorted(tokens & CONTAINER_TERMS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frame-root", type=Path, required=True)
    parser.add_argument("--drafts", type=Path, required=True)
    parser.add_argument("--canonical-sources", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--triad-count", type=int, default=18)
    args = parser.parse_args()

    if args.triad_count <= 0:
        raise SystemExit("triad_count_must_be_positive")
    if args.output_dir.exists():
        raise SystemExit("refusing_to_overwrite_existing_output_dir")

    source_index = {}
    for row in read_jsonl(args.canonical_sources):
        canonical = row["canonical"]
        source_index[row["source_id"]] = {
            "source_id": row["source_id"],
            "sha256": row["sha256"],
            "absolute_path": canonical["absolute_path"],
            "relative_path": canonical["relative_path"],
            "origin_key": canonical["origin_key"],
        }

    reviewed = historical_reviewed_ids(args.frame_root)
    drafts = read_jsonl(args.drafts)
    evaluated: list[dict] = []
    skip = Counter()
    for draft in drafts:
        members = draft.get("members", [])
        ids = draft.get("member_source_ids", [])
        if len(ids) != 3 or len(set(ids)) != 3:
            skip["invalid_member_ids"] += 1
            continue
        if any(source_id in reviewed for source_id in ids):
            skip["historically_reviewed_source"] += 1
            continue
        if any(source_id not in source_index for source_id in ids):
            skip["unknown_source"] += 1
            continue
        if len({source_index[source_id]["origin_key"] for source_id in ids}) != 3:
            skip["non_distinct_origins"] += 1
            continue
        titles = [member.get("title", "") for member in members]
        risk_terms = title_risk_terms(titles)
        evaluated.append({
            "draft": draft,
            "titles": titles,
            "risk_terms": risk_terms,
            "priority": float(draft.get("local_fts_similarity_proxy", 0.0)) - 2.0 * len(risk_terms),
            "shared_key": "|".join(draft.get("shared_title_terms", [])) or "__none__",
        })

    # Deterministic greedy selection: diverse lexical envelopes, no source reuse.
    evaluated.sort(key=lambda row: (-row["priority"], row["draft"]["draft_id"]))
    selected: list[dict] = []
    used_sources: set[str] = set()
    used_shared_keys: set[str] = set()
    for prefer_unique_shared_key in (True, False):
        for row in evaluated:
            if len(selected) >= args.triad_count:
                break
            draft = row["draft"]
            ids = set(draft["member_source_ids"])
            if ids & used_sources:
                continue
            if prefer_unique_shared_key and row["shared_key"] in used_shared_keys:
                continue
            selected.append(row)
            used_sources.update(ids)
            used_shared_keys.add(row["shared_key"])
        if len(selected) >= args.triad_count:
            break

    if len(selected) != args.triad_count:
        raise SystemExit(f"insufficient_disjoint_triads:{len(selected)}:{args.triad_count}")

    args.output_dir.mkdir(parents=True)
    roster_path = args.output_dir / "t0_review_roster.jsonl"
    rows = []
    for index, row in enumerate(selected, start=1):
        draft = row["draft"]
        rendered_members = []
        for member in draft["members"]:
            source = source_index[member["source_id"]]
            path = Path(source["absolute_path"])
            if not path.is_file() or sha256_file(path) != source["sha256"]:
                raise SystemExit(f"source_binding_failure:{source['source_id']}")
            rendered_members.append({**source, "title": member.get("title", "")})
        rows.append({
            "t0_review_id": f"RQ1B-V3-W37-T0-{index:03d}",
            "lexical_draft_id": draft["draft_id"],
            "candidate_count": 3,
            "members": rendered_members,
            "shared_title_terms": draft.get("shared_title_terms", []),
            "lexical_priority_proxy": draft.get("local_fts_similarity_proxy"),
            "title_risk_terms": row["risk_terms"],
            "allowed_outcomes": [
                "READY_FOR_C1", "LIKELY_NONPARALLEL", "NO_PLAUSIBLE_TRIAD",
                "NEEDS_PARENT_REVIEW",
            ],
            "claim_boundary": BOUNDARY,
        })
    roster_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    audit = {
        "status": "RQ1B_V3_W37_LOCAL_T0_ROSTER_PASS_NOT_A_CLUSTER",
        "draft_count": len(drafts),
        "historically_reviewed_source_count": len(reviewed),
        "eligible_draft_count": len(evaluated),
        "selected_triad_count": len(rows),
        "selected_source_count": len(used_sources),
        "selection_skips": dict(sorted(skip.items())),
        "disjoint_sources": len(used_sources) == len(rows) * 3,
        "roster_sha256": sha256_file(roster_path),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    (args.output_dir / "T0_ROSTER_AUDIT.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
