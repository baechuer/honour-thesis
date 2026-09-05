#!/usr/bin/env python3
"""Pin Round 25 public Git roots before any tree census or body acquisition.

Exactly one public ``git ls-remote URL HEAD`` attempt is made per fresh M0
root. The per-root checkpoint is durable; failures remain non-admissions and
are never retried automatically by this program.
"""

from __future__ import annotations

import argparse

import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def origin(url: str) -> str:
    parsed = urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise ValueError(f"not_canonical_github_root:{url}")
    return f"{parts[0]}/{parts[1]}"


def probe(url: str) -> tuple[str, str | None, str | None]:
    completed = subprocess.run(["git", "ls-remote", url, "HEAD"], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        return "UNREACHABLE", None, (completed.stderr.strip() or f"exit_{completed.returncode}")[:500]
    parts = completed.stdout.strip().split()
    if len(parts) != 2 or parts[1] != "HEAD" or len(parts[0]) != 40:
        return "UNREACHABLE", None, "missing_or_invalid_HEAD"
    return "REACHABLE", parts[0], None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--probe-output", type=Path, required=True)
    parser.add_argument("--plan-output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    m0_rows = read_jsonl(args.m0)
    args.probe_output.parent.mkdir(parents=True, exist_ok=True)
    existing = read_jsonl(args.probe_output) if args.probe_output.exists() else []
    existing_by_id = {str(row.get("round25_source_candidate_id")): row for row in existing}
    expected_ids = {str(row["round25_source_candidate_id"]) for row in m0_rows}
    if len(existing_by_id) != len(existing) or not set(existing_by_id).issubset(expected_ids):
        raise SystemExit("invalid_existing_probe_checkpoint")

    probe_rows: list[dict[str, object]] = []
    admitted: list[dict[str, object]] = []
    def persist() -> None:
        args.probe_output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in probe_rows), encoding="utf-8")
    for number, row in enumerate(m0_rows, start=1):
        identifier = str(row["round25_source_candidate_id"])
        url = str(row["canonical_public_source_url"])
        recovered = existing_by_id.get(identifier)
        if recovered is None:
            status, commit, error = probe(url)
            record = {
                "round25_source_candidate_id": identifier,
                "public_url": url,
                "probe_status": status,
                "pinned_commit": commit,
                "error": error,
                "m1_probe_status": "M1_HEAD_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT" if status == "REACHABLE" else "M1_HEAD_PROBE_FAILED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
            }
        else:
            record = recovered
            status, commit = str(record["probe_status"]), record.get("pinned_commit")
        probe_rows.append(record)
        persist()
        if status == "REACHABLE":
            admitted.append({
                "round25_source_candidate_id": identifier,
                "origin": origin(url),
                "repository_url": url,
                "pinned_commit": commit,
                "domains": row["domains"],
                "originating_discovery_ids": row["originating_discovery_ids"],
                "navigation_hints": row["navigation_hints"],
                "licence_status_observations": row["licence_status_observations"],
                "caveats": row["caveats"],
                "m1_intake_status": "M1_PINNED_PUBLIC_SOURCE_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT",
            })
        if not args.quiet and (number % 5 == 0 or number == len(m0_rows)):
            print(json.dumps({"M1_HEAD_PROBE_PROGRESS": f"{number}/{len(m0_rows)}", "probe_status": status}, sort_keys=True), flush=True)
    plan = {
        "status": "M1_ROUND25_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT",
        "round": "RQ1b cross-source Round 25",
        "m0_input": str(args.m0),
        "head_probe": str(args.probe_output),
        "source_count": len(admitted),
        "sources": admitted,
        "explicit_exclusions": [
            "No repository body was cloned or acquired by the HEAD probe.",
            "No source content was executed, and no composition, prompt, label, retrieval input, model result, metric, or empirical conclusion was created.",
            "A failed HEAD probe is a recorded non-admission and receives no automatic retry.",
        ],
    }
    args.plan_output.write_text(json.dumps(plan, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": "M1_ROUND25_HEAD_PROBE_COMPLETE_NOT_A_SOURCE_BODY_ADMISSION_OR_RESULT",
        "m0_input_count": len(m0_rows),
        "reachable_pinned_count": len(admitted),
        "unreachable_count": len(m0_rows) - len(admitted),
        "probe_output": str(args.probe_output),
        "plan_output": str(args.plan_output),
        "failures": [row for row in probe_rows if row["probe_status"] != "REACHABLE"],
        "exclusions": plan["explicit_exclusions"],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "m0_input_count", "reachable_pinned_count", "unreachable_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
