#!/usr/bin/env python3
"""Turn a locally preserved public Google skills index into source-intake leads.

This is catalog parsing only. It does not fetch individual SKILL.md files,
evaluate their content, construct a cluster, or create any experiment input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


STATUS = "RQ1B_V3_D1_W11_PUBLIC_SOURCE_INTAKE_DRAFT_NOT_A_CLUSTER"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=500)
    return parser.parse_args()


def inferred_path(entrypoint: str) -> str:
    marker = "/skills/"
    parsed = urlparse(entrypoint)
    if marker in parsed.path:
        return parsed.path.split(marker, 1)[1]
    return parsed.path.lstrip("/")


def main() -> int:
    args = parse_args()
    catalog_payload = json.loads(args.catalog.read_text(encoding="utf-8"))
    catalog = catalog_payload.get("skills") if isinstance(catalog_payload, dict) else catalog_payload
    if not isinstance(catalog, list):
        raise SystemExit("catalog_is_not_a_list")
    leads: list[dict] = []
    seen_urls: set[str] = set()
    for record in catalog:
        if not isinstance(record, dict):
            continue
        entrypoint = record.get("entrypoint")
        name = record.get("name")
        description = record.get("description")
        if not isinstance(entrypoint, str) or not entrypoint.endswith("/SKILL.md"):
            continue
        if entrypoint in seen_urls or not isinstance(name, str) or not isinstance(description, str):
            continue
        seen_urls.add(entrypoint)
        leads.append(
            {
                "artifact_heading_or_name": name,
                "artifact_path": inferred_path(entrypoint),
                "lane": "google_public_skill_catalog",
                "origin_url": "https://github.com/google/skills",
                "possible_peer_route_family": "catalog-derived public skill; source-only triage pending",
                "public_artifact_evidence": description[:800],
                "raw_artifact_url": entrypoint,
                "repository_ref": "google/skills@main",
                "status": STATUS,
                "visible_license_note": "not assessed at intake",
            }
        )
        if len(leads) >= args.limit:
            break
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for lead in leads:
            handle.write(json.dumps(lead, ensure_ascii=True, sort_keys=True) + "\n")
    print(json.dumps({"catalog_records": len(catalog), "lead_count": len(leads), "status": "RQ1B_V3_D1_W11_CATALOG_PARSE_PASS_NOT_A_CLUSTER"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
