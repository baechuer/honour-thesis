#!/usr/bin/env python3
"""Validate structural provenance of a versioned RQ1b V3 public intake draft.

This validates only self-reported source-lead shape and duplicate identifiers.
It neither downloads artifacts nor decides source quality, C1 eligibility,
cluster membership, a prompt, a label, or a retrieval result.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


DEFAULT_STATUS = "RQ1B_V3_D1_W9_PUBLIC_SOURCE_INTAKE_DRAFT_NOT_A_CLUSTER"
REQUIRED = {
    "status",
    "lane",
    "origin_url",
    "repository_ref",
    "artifact_path",
    "raw_artifact_url",
    "artifact_heading_or_name",
    "public_artifact_evidence",
    "possible_peer_route_family",
    "visible_license_note",
}
PROHIBITED = {"prompt", "target", "gold", "winner", "selector", "embedding", "metric", "result"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", type=Path, action="append", required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--expected-status", default=DEFAULT_STATUS)
    parser.add_argument("--report-status-prefix", default="RQ1B_V3_D1_W9")
    return parser.parse_args()


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    rows: list[tuple[Path, int, dict[str, Any]]] = []
    raw_urls: dict[str, tuple[Path, int]] = {}
    artifacts: dict[tuple[str, str], tuple[Path, int]] = {}
    lane_counts: Counter[str] = Counter()
    origin_hosts: set[str] = set()
    for path in args.draft:
        if not path.is_file():
            failures.append(f"missing_draft_file:{path}")
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                failures.append(f"invalid_json:{path}:{number}:{error.msg}")
                continue
            if not isinstance(row, dict):
                failures.append(f"row_not_object:{path}:{number}")
                continue
            rows.append((path, number, row))
            missing = sorted(REQUIRED - set(row))
            extra_prohibited = sorted(key for key in row if any(token in key.casefold() for token in PROHIBITED))
            if missing:
                failures.append(f"missing_fields:{path}:{number}:{','.join(missing)}")
            if extra_prohibited:
                failures.append(f"prohibited_field:{path}:{number}:{','.join(extra_prohibited)}")
            if row.get("status") != args.expected_status:
                failures.append(f"bad_status:{path}:{number}")
            values = {key: str(row.get(key, "")).strip() for key in REQUIRED - {"visible_license_note"}}
            if any(not value for value in values.values()):
                failures.append(f"empty_required_value:{path}:{number}")
            origin_url, raw_url = str(row.get("origin_url", "")), str(row.get("raw_artifact_url", ""))
            if not valid_url(origin_url) or not valid_url(raw_url):
                failures.append(f"invalid_url:{path}:{number}")
            if raw_url in raw_urls:
                failures.append(f"duplicate_raw_url:{path}:{number}:first={raw_urls[raw_url][0]}:{raw_urls[raw_url][1]}")
            else:
                raw_urls[raw_url] = (path, number)
            artifact_key = (str(row.get("repository_ref", "")), str(row.get("artifact_path", "")))
            if artifact_key in artifacts:
                failures.append(f"duplicate_repository_artifact:{path}:{number}:first={artifacts[artifact_key][0]}:{artifacts[artifact_key][1]}")
            else:
                artifacts[artifact_key] = (path, number)
            lane_counts[str(row.get("lane", ""))] += 1
            origin_hosts.add(urlparse(origin_url).netloc)

    report = {
        "status": f"{args.report_status_prefix}_INTAKE_STRUCTURAL_AUDIT_{'PASS' if not failures else 'FAIL'}_NOT_A_CLUSTER",
        "draft_record_count": len(rows),
        "lane_counts": dict(sorted(lane_counts.items())),
        "distinct_origin_hosts": sorted(origin_hosts),
        "distinct_origin_host_count": len(origin_hosts),
        "failures": sorted(set(failures)),
        "boundary": "Structural public-source intake audit only. It does not verify downloaded bytes, source quality, C1 eligibility, cluster membership, prompt, label, selector, metric, or result.",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
