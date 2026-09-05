#!/usr/bin/env python3
"""Canonicalise Wave 039 navigation leads without reading public skill bodies."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


REQUIRED_TOP = {"lane", "leads", "boundary_acknowledgement"}
REQUIRED_LEAD = {
    "origin_url", "owner", "repository", "domain", "metadata_rationale",
    "likely_skill_path_hints", "navigation_url",
}


def owner_repo(origin_url: str) -> str:
    # Historic amendments sometimes store a GitHub artefact URL rather than a
    # repository root. For origin deduplication, retain only its owner/repo
    # prefix; M0 still writes the canonical repository root in its output.
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:/.*)?", origin_url.strip())
    if not match:
        raise ValueError(f"invalid_github_origin:{origin_url}")
    return f"{match.group(1).lower()}/{match.group(2).lower()}"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def frozen_origins(frame_root: Path) -> set[str]:
    manifests = [frame_root / "source_frame_2026-08-29" / "canonical_sources.jsonl"]
    manifests.extend(sorted(frame_root.glob("d1_source_intake_wave_*/source_frame_amendment/canonical_sources_amendment.jsonl")))
    result = set()
    for path in manifests:
        if not path.is_file():
            continue
        for row in read_jsonl(path):
            origin = row.get("origin_url") or row.get("canonical", {}).get("origin_url")
            if isinstance(origin, str) and origin.startswith("https://github.com/"):
                result.add(owner_repo(origin))
                continue
            # The original local frame predates origin_url storage, but its
            # staged origin key retains an owner--repository-hash suffix.
            origin_key = row.get("canonical", {}).get("origin_key", "")
            match = re.search(r"-m1-([a-z0-9_.-]+)--([a-z0-9_.-]+?)-[0-9a-f]{8}$", str(origin_key), re.IGNORECASE)
            if match:
                result.add(f"{match.group(1).lower()}/{match.group(2).lower()}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0-dir", type=Path, required=True)
    parser.add_argument("--frame-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    raw_paths = sorted(args.m0_dir.glob("*.json"))
    if not raw_paths:
        raise SystemExit("no_raw_m0_returns")
    prior = frozen_origins(args.frame_root)
    seen, records, aliases = set(), [], []
    raw_count = 0
    for path in raw_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if set(payload) != REQUIRED_TOP or not isinstance(payload["leads"], list):
            raise SystemExit(f"invalid_top_schema:{path}")
        for lead in payload["leads"]:
            raw_count += 1
            if set(lead) != REQUIRED_LEAD:
                raise SystemExit(f"invalid_lead_schema:{path}")
            if not all(isinstance(lead[key], str) and lead[key].strip() for key in REQUIRED_LEAD - {"likely_skill_path_hints"}):
                raise SystemExit(f"invalid_string_value:{path}")
            if not isinstance(lead["likely_skill_path_hints"], list) or not all(isinstance(value, str) and value.strip() for value in lead["likely_skill_path_hints"]):
                raise SystemExit(f"invalid_path_hints:{path}")
            key = owner_repo(lead["origin_url"])
            if key != f"{lead['owner'].lower()}/{lead['repository'].lower()}":
                raise SystemExit(f"owner_repository_mismatch:{path}:{key}")
            if key in seen:
                aliases.append({"owner_repo": key, "raw_return": path.name, "status": "RQ1B_V3_W39_M0_WITHIN_WAVE_ORIGIN_ALIAS_NOT_ADMITTED"})
                continue
            seen.add(key)
            records.append({
                "discovery_id": f"RQ1B-V3-W39-M0-{len(records) + 1:03d}",
                "origin_url": f"https://github.com/{key}",
                "owner_repo": key,
                "discovery_lane": payload["lane"],
                "domain": lead["domain"],
                "metadata_rationale": lead["metadata_rationale"],
                "likely_skill_path_hints": lead["likely_skill_path_hints"],
                "navigation_url": lead["navigation_url"],
                "prior_source_frame_origin_overlap": key in prior,
                "m0_status": "RQ1B_V3_W39_M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
                "claim_boundary": "Navigation metadata only. No source body was read, pinned, captured, parsed, embedded, scored or used to form a cluster.",
            })
    records.sort(key=lambda row: (row["prior_source_frame_origin_overlap"], row["owner_repo"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    alias_path = args.output.parent / "w39_m0_within_wave_origin_aliases.jsonl"
    alias_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in aliases), encoding="utf-8")
    report = {
        "status": "RQ1B_V3_W39_M0_MERGE_PASS_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "raw_return_count": len(raw_paths),
        "raw_lead_count": raw_count,
        "within_wave_origin_alias_count": len(aliases),
        "unique_lead_count": len(records),
        "prior_source_frame_origin_overlap_count": sum(row["prior_source_frame_origin_overlap"] for row in records),
        "fresh_navigation_candidate_count": sum(not row["prior_source_frame_origin_overlap"] for row in records),
        "lane_counts": dict(sorted(Counter(row["discovery_lane"] for row in records).items())),
        "network_calls": 0,
        "source_body_reads": 0,
        "source_body_transfers": 0,
        "claim_boundary": "M0 is navigation-only discovery and does not admit a source or establish a candidate composition, prompt, label, selector input, metric or result.",
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("unique_lead_count", "fresh_navigation_candidate_count", "prior_source_frame_origin_overlap_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
