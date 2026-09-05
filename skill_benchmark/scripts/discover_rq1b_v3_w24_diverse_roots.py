#!/usr/bin/env python3
"""Collect diverse public GitHub metadata leads for RQ1b V3 Wave 024 only."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


QUERIES = {
    "legal_governance": '"SKILL.md" legal compliance skills in:readme',
    "finance_business": '"SKILL.md" finance accounting business skills in:readme',
    "health_science": '"SKILL.md" healthcare science skills in:readme',
    "research_education": '"SKILL.md" research education skills in:readme',
    "data_database": '"SKILL.md" data database analytics skills in:readme',
    "infrastructure": '"SKILL.md" devops infrastructure skills in:readme',
    "security": '"SKILL.md" security skills agent in:readme',
    "design_content": '"SKILL.md" design content skills in:readme',
    "marketing_product": '"SKILL.md" marketing product skills in:readme',
    "writing_communications": '"SKILL.md" writing communication skills in:readme',
    "operations_projects": '"SKILL.md" operations project skills in:readme',
    "multi_skill_general": '"SKILL.md" "skills/" agent in:readme',
}


def search(query: str, per_page: int) -> tuple[list[dict[str, object]], str | None]:
    url = "https://api.github.com/search/repositories?" + urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": per_page}
    )
    request = Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "rq1b-v3-w24-diverse-discovery"},
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
    parser.add_argument("--per-query", type=int, default=30)
    args = parser.parse_args()
    if not 1 <= args.per_query <= 100:
        raise SystemExit("per_query_must_be_between_1_and_100")

    leads: list[dict[str, object]] = []
    failures: list[dict[str, str]] = []
    seen: set[str] = set()
    for lane, query in QUERIES.items():
        items, failure = search(query, args.per_query)
        if failure:
            failures.append({"lane": lane, "query": query, "failure": failure})
            continue
        for rank, item in enumerate(items, start=1):
            url, full_name = item.get("html_url"), item.get("full_name")
            if not isinstance(url, str) or not isinstance(full_name, str) or not url.startswith("https://github.com/"):
                continue
            canonical_url = url.rstrip("/")
            if canonical_url in seen:
                continue
            seen.add(canonical_url)
            topics = item.get("topics") if isinstance(item.get("topics"), list) else []
            leads.append(
                {
                    "discovery_id": f"RQ1B-V3-W24-M0-{lane.upper()}-{rank:03d}",
                    "canonical_public_source_url": canonical_url,
                    "domains": [lane.replace("_", "-"), *[str(topic) for topic in topics[:8]]],
                    "source_family_hints": ["GitHub repository-search navigation lead"],
                    "navigation_hints": [f"GitHub repository search query: {query}", f"repository full_name: {full_name}"],
                    "caveats": ["M0 metadata lead only; no repository tree or source body was inspected"],
                    "licence_status_observations": ["NOT_OBSERVED_AT_M0"],
                    "m0_status": "RQ1B_V3_W24_M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in leads), encoding="utf-8")
    summary = {
        "status": "RQ1B_V3_W24_M0_COMPLETE_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "observed_on": date.today().isoformat(),
        "query_count": len(QUERIES),
        "per_query_limit": args.per_query,
        "raw_unique_navigation_lead_count": len(leads),
        "failures": failures,
        "exclusions": [
            "Only public repository-search metadata was requested.",
            "No repository tree or raw skill source body was fetched, read, executed, or treated as candidate evidence.",
            "No source is admitted and no composition, prompt, label, retrieval input, model result, metric, or empirical conclusion was created.",
            "Each failed query is retained and this program never retries it automatically.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "lead_count": len(leads), "failure_count": len(failures)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
