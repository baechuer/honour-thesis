#!/usr/bin/env python3
"""Census bounded public GitHub roots for pinned SKILL.md paths.

This M1 navigation step reads only public repository-tree metadata. It never
downloads a skill body, executes code, or judges a skill's quality or cluster
eligibility. Each selected root is attempted once; all outcomes persist.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_repo(url: str) -> tuple[str, str]:
    parts = url.rstrip("/").split("/")
    if len(parts) != 2 + 3 or parts[:3] != ["https:", "", "github.com"]:
        raise ValueError(f"unsupported_github_url:{url}")
    return parts[3], parts[4]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leads", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--per-lane", type=int, default=5)
    parser.add_argument("--status-prefix", default="RQ1B_V3_D1_W20")
    args = parser.parse_args()
    if not 1 <= args.per_lane <= 10:
        raise SystemExit("per_lane_must_be_1_to_10")
    if args.output.exists() or args.summary.exists():
        raise SystemExit("refusing_to_overwrite_existing_output")

    by_lane: dict[str, list[dict]] = defaultdict(list)
    for lead in read_jsonl(args.leads):
        domains = lead.get("domains")
        lane = str(domains[0]) if isinstance(domains, list) and domains else "unclassified"
        by_lane[lane].append(lead)
    selected = [lead for lane in sorted(by_lane) for lead in by_lane[lane][:args.per_lane]]
    outcomes: list[dict] = []
    for lead in selected:
        root = str(lead["canonical_public_source_url"])
        lane = str(lead["domains"][0])
        try:
            owner, repo = parse_repo(root)
            endpoint = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
            request = Request(endpoint, headers={"Accept": "application/vnd.github+json", "User-Agent": "rq1b-v3-w20-tree-census"})
            with urlopen(request, timeout=30) as response:  # nosec B310: fixed public GitHub endpoint
                payload = json.loads(response.read().decode("utf-8"))
            commit = payload.get("sha")
            tree = payload.get("tree")
            if not isinstance(commit, str) or not isinstance(tree, list):
                raise ValueError("missing_tree_payload")
            paths = sorted(str(item.get("path", "")) for item in tree if isinstance(item, dict) and str(item.get("path", "")).endswith("SKILL.md"))
            outcome = {
                "status": f"{args.status_prefix}_TREE_CENSUS_SUCCESS_NOT_A_CLUSTER",
                "discovery_id": lead.get("discovery_id"),
                "lane": lane,
                "origin_url": root,
                "repository_ref": f"{owner}/{repo}@{commit}",
                "pinned_commit": commit,
                "skill_md_paths": paths,
                "skill_md_path_count": len(paths),
                "tree_endpoint": endpoint,
            }
        except HTTPError as error:
            outcome = {"status": f"{args.status_prefix}_TREE_CENSUS_HTTP_FAILURE_NOT_A_CLUSTER", "discovery_id": lead.get("discovery_id"), "lane": lane, "origin_url": root, "error": f"HTTP_{error.code}"}
        except (URLError, TimeoutError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
            outcome = {"status": f"{args.status_prefix}_TREE_CENSUS_FAILURE_NOT_A_CLUSTER", "discovery_id": lead.get("discovery_id"), "lane": lane, "origin_url": root, "error": f"{type(error).__name__}:{error}"}
        outcomes.append(outcome)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(outcome, ensure_ascii=True, sort_keys=True) + "\n")
            handle.flush()

    successes = [row for row in outcomes if row["status"].endswith("TREE_CENSUS_SUCCESS_NOT_A_CLUSTER")]
    summary = {
        "status": f"{args.status_prefix}_TREE_CENSUS_COMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "selected_root_count": len(selected),
        "successful_root_count": len(successes),
        "roots_with_skill_md_count": sum(bool(row["skill_md_path_count"]) for row in successes),
        "skill_md_path_count": sum(row["skill_md_path_count"] for row in successes),
        "failure_count": len(outcomes) - len(successes),
        "lane_selection_counts": {lane: min(len(rows), args.per_lane) for lane, rows in sorted(by_lane.items())},
        "network_calls": len(outcomes),
        "texts_downloaded": 0,
        "boundary": "Public repository-tree metadata only. No skill body was downloaded, read, executed, admitted as source evidence, or treated as a candidate, cluster, prompt, label, selector input, metric, or result.",
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
