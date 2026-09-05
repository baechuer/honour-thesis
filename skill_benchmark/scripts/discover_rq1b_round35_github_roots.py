#!/usr/bin/env python3
"""Collect navigation-only GitHub repository leads for RQ1b Round 35.

The program uses the public GitHub repository-search endpoint. It deliberately
does not fetch repository trees or source files: every returned root remains an
M0 navigation lead until the frozen M1--C6 protocol admits it. HTTP failures
are recorded once and are not retried automatically.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


QUERIES = {
    "broad_agent_skills": '"agent skills" in:readme',
    "claude_code_skills": '"Claude Code" skills in:readme',
    "codex_skills": 'Codex skills in:readme',
    "openai_skill_format": '"SKILL.md" in:readme',
    "business_operations": 'agent skills sales marketing operations in:readme',
    "data_research": 'agent skills data research analytics in:readme',
    "documents_creative": 'agent skills pdf document writing in:readme',
    "software_systems": 'agent skills software database devops in:readme',
    "product_collaboration": 'agent skills product project customer in:readme',
    "scientific_specialist": 'agent skills science bioinformatics in:readme',
}


def request_search(query: str, per_page: int) -> tuple[list[dict[str, object]], str | None]:
    url = "https://api.github.com/search/repositories?" + urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": per_page}
    )
    request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "rq1b-public-discovery"})
    try:
        with urlopen(request, timeout=30) as response:  # nosec B310: fixed public API root
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return [], f"HTTP_{error.code}"
    except URLError as error:
        return [], f"URL_ERROR_{error.reason}"
    except TimeoutError:
        return [], "TIMEOUT"
    items = payload.get("items")
    if not isinstance(items, list):
        return [], "MISSING_ITEMS"
    return [item for item in items if isinstance(item, dict)], None


def row(query_lane: str, rank: int, item: dict[str, object]) -> dict[str, object] | None:
    url = item.get("html_url")
    full_name = item.get("full_name")
    if not isinstance(url, str) or not isinstance(full_name, str) or not url.startswith("https://github.com/"):
        return None
    topics = item.get("topics") if isinstance(item.get("topics"), list) else []
    return {
        "discovery_id": f"R35-M0-{query_lane.upper()}-{rank:03d}",
        "canonical_public_source_url": url.rstrip("/"),
        "domains": [query_lane.replace("_", "-"), *[str(topic) for topic in topics[:8]]],
        "source_family_hints": ["GitHub repository-search navigation lead", str(item.get("owner", {}).get("type", "unknown")) if isinstance(item.get("owner"), dict) else "unknown-owner"],
        "navigation_hints": [f"GitHub repository search query: {QUERIES[query_lane]}", f"repository full_name: {full_name}"],
        "caveats": ["M0 navigation lead only; no source artifact, repository tree, or skill body was inspected", "Repository-search relevance does not establish SKILL.md presence or candidacy"],
        "licence_status_observations": ["NOT_OBSERVED_AT_M0"],
        "m0_status": "M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--per-query", type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.per_query <= 100:
        raise SystemExit("per_query_must_be_between_1_and_100")

    rows: list[dict[str, object]] = []
    failures: list[dict[str, str]] = []
    seen: set[str] = set()
    for lane, query in QUERIES.items():
        items, failure = request_search(query, args.per_query)
        if failure:
            failures.append({"lane": lane, "query": query, "failure": failure})
            continue
        for rank, item in enumerate(items, start=1):
            record = row(lane, rank, item)
            if record is None:
                continue
            root = str(record["canonical_public_source_url"])
            if root in seen:
                continue
            seen.add(root)
            rows.append(record)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(item, ensure_ascii=True, sort_keys=True) + "\n" for item in rows), encoding="utf-8")
    summary = {
        "status": "M0_ROUND35_PUBLIC_SEARCH_DISCOVERY_COMPLETE_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "observed_on": date.today().isoformat(),
        "query_count": len(QUERIES),
        "per_query_limit": args.per_query,
        "raw_unique_navigation_lead_count": len(rows),
        "failures": failures,
        "exclusions": [
            "Only public repository-search metadata was requested.",
            "No repository tree or skill source body was fetched, read, executed, or treated as candidate evidence.",
            "No source is admitted and no composition, prompt, label, retrieval input, model result, metric, or empirical conclusion was created.",
            "A failed query remains recorded and is not retried automatically by this program.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "raw_unique_navigation_lead_count": len(rows), "failure_count": len(failures)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
