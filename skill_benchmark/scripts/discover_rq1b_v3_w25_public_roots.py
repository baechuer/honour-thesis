#!/usr/bin/env python3
"""Collect public GitHub navigation leads for RQ1b V3 Wave 025.

This program retrieves repository-search metadata only. It does not fetch a
repository tree or source body, execute code, create a candidate composition,
or infer a skill label. Each query is attempted once and failures are retained.
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
    "software_quality": '"SKILL.md" testing debugging code review skills in:readme',
    "data_analysis": '"SKILL.md" data analytics visualisation skills in:readme',
    "research_science": '"SKILL.md" research science laboratory skills in:readme',
    "legal_contracts": '"SKILL.md" legal contract compliance skills in:readme',
    "finance_controls": '"SKILL.md" finance accounting audit skills in:readme',
    "healthcare": '"SKILL.md" clinical healthcare medical skills in:readme',
    "product_design": '"SKILL.md" product design UX skills in:readme',
    "content_media": '"SKILL.md" writing content media skills in:readme',
    "marketing_sales": '"SKILL.md" marketing sales customer skills in:readme',
    "cloud_operations": '"SKILL.md" cloud devops infrastructure skills in:readme',
    "security": '"SKILL.md" security incident vulnerability skills in:readme',
    "education": '"SKILL.md" education teaching learning skills in:readme',
    "business_operations": '"SKILL.md" operations procurement project skills in:readme',
    "multi_domain": '"SKILL.md" "skills/" agent in:readme',
}


def search(query: str, per_query: int) -> tuple[list[dict[str, object]], str | None]:
    endpoint = "https://api.github.com/search/repositories?" + urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": per_query}
    )
    request = Request(
        endpoint,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "rq1b-v3-w25-navigation"},
    )
    try:
        with urlopen(request, timeout=30) as response:  # nosec B310: fixed public GitHub endpoint
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
    parser.add_argument("--query-config", type=Path)
    parser.add_argument("--status-prefix", default="RQ1B_V3_W25")
    parser.add_argument("--per-query", type=int, default=30)
    args = parser.parse_args()
    if not 1 <= args.per_query <= 100:
        raise SystemExit("per_query_must_be_between_1_and_100")
    if args.output.exists() or args.summary.exists():
        raise SystemExit("refusing_to_overwrite_existing_w25_m0_output")

    queries = QUERIES
    if args.query_config is not None:
        loaded = json.loads(args.query_config.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in loaded.items()):
            raise SystemExit("query_config_must_be_a_string_to_string_object")
        queries = loaded
    rows: list[dict[str, object]] = []
    failures: list[dict[str, str]] = []
    seen: set[str] = set()
    for lane, query in queries.items():
        items, failure = search(query, args.per_query)
        if failure:
            failures.append({"lane": lane, "query": query, "failure": failure})
            continue
        for rank, item in enumerate(items, start=1):
            url = item.get("html_url")
            full_name = item.get("full_name")
            if not isinstance(url, str) or not isinstance(full_name, str) or not url.startswith("https://github.com/"):
                continue
            canonical_url = url.rstrip("/")
            if canonical_url in seen:
                continue
            seen.add(canonical_url)
            topics = item.get("topics") if isinstance(item.get("topics"), list) else []
            rows.append(
                {
                    "discovery_id": f"{args.status_prefix.replace('_', '-')}-M0-{lane.upper()}-{rank:03d}",
                    "canonical_public_source_url": canonical_url,
                    "repository_full_name": full_name,
                    "domains": [lane.replace("_", "-"), *[str(topic) for topic in topics[:8]]],
                    "source_family_hints": ["GitHub repository-search navigation lead"],
                    "navigation_hints": [f"GitHub repository search query: {query}", f"repository full_name: {full_name}"],
                    "caveats": ["M0 metadata lead only; no repository tree or source body was inspected"],
                    "licence_status_observations": ["NOT_OBSERVED_AT_M0"],
                    "m0_status": f"{args.status_prefix}_M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": f"{args.status_prefix}_M0_COMPLETE_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "observed_on": date.today().isoformat(),
        "query_count": len(queries),
        "per_query_limit": args.per_query,
        "raw_unique_navigation_lead_count": len(rows),
        "failures": failures,
        "boundary": [
            "Only public repository-search metadata was requested.",
            "No repository tree or raw skill source body was fetched, read, executed, or admitted.",
            "No composition, prompt, label, retrieval input, model result, metric, or empirical conclusion was created.",
            "Each failed query is retained and this program never retries it automatically.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "lead_count": len(rows), "failure_count": len(failures)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
