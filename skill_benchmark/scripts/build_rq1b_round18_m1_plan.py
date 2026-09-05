#!/usr/bin/env python3
"""Build a provenance-pinned Round 18 M1 plan from M0 leads and HEAD probes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_probe(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "status\tpublic_url\tpinned_commit":
        raise ValueError("unexpected_probe_header")
    result: dict[str, str] = {}
    for line_no, line in enumerate(lines[1:], start=2):
        parts = line.split("\t")
        if len(parts) != 3 or parts[0] != "REACHABLE" or not parts[2]:
            raise ValueError(f"unreachable_or_invalid_probe:{line_no}")
        if parts[1] in result:
            raise ValueError(f"duplicate_probe_url:{parts[1]}")
        result[parts[1]] = parts[2]
    return result


def github_origin(url: str) -> str:
    parsed = urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise ValueError(f"not_canonical_github_root:{url}")
    return f"{parts[0]}/{parts[1]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    m0_rows = read_jsonl(args.m0)
    probe = read_probe(args.probe)
    urls = {str(row["canonical_public_source_url"]) for row in m0_rows}
    if urls != set(probe):
        raise SystemExit(f"probe_coverage_mismatch:m0={len(urls)}:probe={len(probe)}")
    sources: list[dict[str, object]] = []
    for row in sorted(m0_rows, key=lambda item: str(item["canonical_public_source_url"])):
        url = str(row["canonical_public_source_url"])
        sources.append({
            "round18_source_candidate_id": row["round18_source_candidate_id"],
            "origin": github_origin(url),
            "repository_url": url,
            "pinned_commit": probe[url],
            "domains": row["domains"],
            "originating_discovery_ids": row["originating_discovery_ids"],
            "navigation_hints": row["navigation_hints"],
            "licence_status_observations": row["licence_status_observations"],
            "caveats": row["caveats"],
            "m1_intake_status": "M1_PINNED_PUBLIC_SOURCE_PENDING_LOCAL_BYTE_STAGING_NOT_A_CLUSTER_OR_RESULT",
        })
    payload = {
        "status": "M1_BATCH_PLAN_PINNED_NOT_YET_STAGED_NOT_A_CLUSTER_OR_RESULT",
        "round": "RQ1b cross-source Round 18",
        "purpose": "Discovery-first public source expansion. Every source is pinned by a public HEAD probe before any local sparse acquisition. Local M1 may byte-stage qualifying original SKILL.md files but cannot form clusters or prompts.",
        "source_count": len(sources),
        "m0_canonical_lead_file": str(args.m0),
        "head_probe_file": str(args.probe),
        "m1_actions_only": [
            "Acquire a local non-executed sparse working copy at the recorded public commit.",
            "Byte-stage qualifying original SKILL.md files with source URL, commit, SHA-256, frontmatter, and observed licence state.",
            "Screen exact-byte duplicates against prior public RQ1b and background source roots.",
            "Build source-only navigation metadata for later full-source C0A review.",
        ],
        "explicit_exclusions": [
            "No source content is executed.",
            "No semantic grouping, candidate composition, prompt, gold label, acceptable set, retrieval input, embedding, selector call, metric, or result is created by M1.",
            "Missing declared licence remains recorded provenance, not an admission exclusion.",
        ],
        "sources": sources,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "source_count": len(sources)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
