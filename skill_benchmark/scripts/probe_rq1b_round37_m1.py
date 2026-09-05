#!/usr/bin/env python3
"""Pin each Round 37 M0 root once without reading trees or source bodies."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


M0_STATUS = "M0_CANONICAL_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def origin(url: str) -> str:
    parsed = urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise ValueError(f"not_canonical_github_root:{url}")
    return f"{parts[0]}/{parts[1]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--probe-output", type=Path, required=True)
    parser.add_argument("--plan-output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--replace-uniform-dns-failures", action="store_true")
    parser.add_argument("--transport-failure-audit", type=Path)
    args = parser.parse_args()

    m0 = read_jsonl(args.m0)
    if any(row.get("m0_status") != M0_STATUS for row in m0):
        raise SystemExit("invalid_m0_status")
    expected = {str(row.get("round37_source_candidate_id", "")) for row in m0}
    if "" in expected or len(expected) != len(m0):
        raise SystemExit("invalid_or_duplicate_round37_source_id")
    existing = read_jsonl(args.probe_output) if args.probe_output.exists() else []
    previous = {str(row.get("round37_source_candidate_id", "")): row for row in existing}
    if len(previous) != len(existing) or not set(previous).issubset(expected):
        raise SystemExit("invalid_existing_probe_checkpoint")
    if args.replace_uniform_dns_failures:
        if args.transport_failure_audit is None:
            raise SystemExit("transport_failure_audit_required")
        uniform_dns = (
            len(previous) == len(m0)
            and all(
                row.get("probe_status") == "UNREACHABLE"
                and "Could not resolve host: github.com" in str(row.get("error", ""))
                for row in previous.values()
            )
        )
        if not uniform_dns:
            raise SystemExit("replacement_requires_uniform_pre_resolution_dns_failure")
        args.transport_failure_audit.parent.mkdir(parents=True, exist_ok=True)
        args.transport_failure_audit.write_text(json.dumps({
            "status": "M1_ROUND37_SANDBOX_DNS_TRANSPORT_FAILURE_SUPERSEDED_BEFORE_NETWORK_PROBE",
            "failure_count": len(previous),
            "reason": "all sandbox attempts failed before GitHub hostname resolution; none are repository reachability findings",
            "prior_probe_output": str(args.probe_output),
            "excluded_claims": ["No repository-specific non-admission is inferred from this uniform sandbox transport failure."],
        }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        previous = {}
        args.probe_output.unlink()

    records: list[dict[str, Any]] = []
    pinned: list[dict[str, Any]] = []
    for position, m0_row in enumerate(m0, start=1):
        identifier = str(m0_row["round37_source_candidate_id"])
        url = str(m0_row["canonical_public_source_url"])
        record = previous.get(identifier)
        if record is None:
            completed = subprocess.run(["git", "ls-remote", url, "HEAD"], text=True, capture_output=True, check=False)
            parts = completed.stdout.strip().split()
            reachable = completed.returncode == 0 and len(parts) == 2 and parts[1] == "HEAD" and len(parts[0]) == 40
            record = {
                "round37_source_candidate_id": identifier,
                "public_url": url,
                "probe_status": "REACHABLE" if reachable else "UNREACHABLE",
                "pinned_commit": parts[0] if reachable else None,
                "error": None if reachable else (completed.stderr.strip() or f"missing_or_invalid_HEAD_or_exit_{completed.returncode}")[:500],
                "m1_probe_status": "M1_HEAD_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT" if reachable else "M1_HEAD_PROBE_FAILED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
            }
        records.append(record)
        write_jsonl(args.probe_output, records)
        if record["probe_status"] == "REACHABLE":
            pinned.append({
                "plan_position": position,
                "round37_source_candidate_id": identifier,
                "origin": origin(url),
                "repository_url": url,
                "pinned_commit": record["pinned_commit"],
                "domains": m0_row["domains"],
                "originating_discovery_ids": m0_row["originating_discovery_ids"],
                "sample_path_hints": m0_row["sample_path_hints"],
                "m1_intake_status": "M1_PINNED_PUBLIC_SOURCE_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT",
            })
        if identifier not in previous and (position % 5 == 0 or position == len(m0)):
            print(json.dumps({"M1_HEAD_PROBE_PROGRESS": f"{position}/{len(m0)}", "source_id": identifier, "status": record["probe_status"]}, sort_keys=True), flush=True)

    plan = {
        "status": "M1_ROUND37_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT",
        "m0_input": str(args.m0),
        "source_count": len(pinned),
        "sources": pinned,
        "exclusions": [
            "The HEAD probe does not fetch a repository tree or source body.",
            "A failed HEAD probe is a durable non-admission with no automatic retry.",
            "No source content was executed and no candidate composition, prompt, label, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.plan_output.parent.mkdir(parents=True, exist_ok=True)
    args.plan_output.write_text(json.dumps(plan, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": "M1_ROUND37_HEAD_PROBE_COMPLETE_NOT_A_SOURCE_BODY_ADMISSION_OR_RESULT",
        "m0_input_count": len(m0),
        "reachable_pinned_count": len(pinned),
        "unreachable_count": len(m0) - len(pinned),
        "failures": [row for row in records if row["probe_status"] != "REACHABLE"],
        "exclusions": plan["exclusions"],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "m0_input_count", "reachable_pinned_count", "unreachable_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
