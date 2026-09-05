#!/usr/bin/env python3
"""Collect W22 public GitHub repository metadata for RQ1b V3 discovery only."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


QUERIES = {
    "finance_and_accounting": "skills finance accounting in:readme",
    "legal_and_compliance": "skills legal compliance in:readme",
    "health_and_science": "skills healthcare medical science in:readme",
    "research_and_analysis": "skills research analysis in:readme",
    "data_and_database": "skills data database analytics in:readme",
    "design_and_content": "skills design content marketing in:readme",
    "operations_and_projects": "skills operations project management in:readme",
    "multi_skill_repositories": '"SKILL.md" "skills" in:readme',
}


def search(query: str, per_page: int) -> tuple[list[dict[str, object]], str | None]:
    url = "https://api.github.com/search/repositories?" + urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": per_page}
    )
    request = Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "rq1b-v3-w22-discovery"},
    )
    try:
        with urlopen(request, timeout=30) as response:  # nosec B310: fixed public API endpoint
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return [], f"HTTP_{error.code}"
    except URLError as error:
        return [], f"URL_ERROR_{error.reason}"
    except TimeoutError:
        return [], "TIMEOUT"
    items = body.get("items")
    return ([item for item in items if isinstance(item, dict)], None) if isinstance(items, list) else ([], "MISSING_ITEMS")


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
        items, failure = search(query, args.per_query)
        if failure:
            failures.append({"lane": lane, "query": query, "failure": failure})
            continue
        for rank, item in enumerate(items, start=1):
            url = item.get("html_url")
            full_name = item.get("full_name")
            if not isinstance(url, str) or not isinstance(full_name, str) or not url.startswith("https://github.com/"):
                continue
            root = url.rstrip("/")
            if root in seen:
                continue
            seen.add(root)
            topics = item.get("topics") if isinstance(item.get("topics"), list) else []
            rows.append(
                {
                    "discovery_id": f"RQ1B-V3-W22-M0-{lane.upper()}-{rank:03d}",
                    "canonical_public_source_url": root,
                    "domains": [lane.replace("_", "-"), *[str(topic) for topic in topics[:8]]],
                    "source_family_hints": ["GitHub repository-search navigation lead"],
                    "navigation_hints": [f"GitHub repository search query: {query}", f"repository full_name: {full_name}"],
                    "caveats": ["M0 navigation lead only; no repository tree or source body was inspected"],
                    "licence_status_observations": ["NOT_OBSERVED_AT_M0"],
                    "m0_status": "M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "RQ1B_V3_W22_M0_COMPLETE_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
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
    print(json.dumps({"status": summary["status"], "lead_count": len(rows), "failure_count": len(failures)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
