#!/usr/bin/env python3
"""Select a deterministic, path-only Wave 038 M2 roster without source reads."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def path_bucket(path: str) -> str:
    parts = path.split("/")
    return "/".join(parts[:2]) if len(parts) > 1 else parts[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", type=Path, required=True)
    parser.add_argument("--cap-per-root", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.cap_per_root <= 0:
        raise SystemExit("invalid_cap")
    rows = [json.loads(line) for line in args.paths.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows or any(row.get("status") != "RQ1B_V3_W38_M1_PATH_ONLY_NOT_A_SOURCE_OR_RESULT" for row in rows):
        raise SystemExit("invalid_m1_path_rows")
    by_root: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_root[row["root"]].append(row)
    selected = []
    by_root_counts = {}
    for root in sorted(by_root):
        buckets: dict[str, list[dict]] = defaultdict(list)
        for row in sorted(by_root[root], key=lambda item: item["repository_path"]):
            buckets[path_bucket(row["repository_path"])].append(row)
        chosen = []
        while len(chosen) < args.cap_per_root and buckets:
            made_progress = False
            for bucket in sorted(list(buckets)):
                if len(chosen) == args.cap_per_root:
                    break
                options = buckets[bucket]
                chosen.append(options.pop(0))
                made_progress = True
                if not options:
                    del buckets[bucket]
            if not made_progress:
                break
        by_root_counts[root] = {"available_path_count": len(by_root[root]), "selected_path_count": len(chosen)}
        selected.extend(chosen)
    roster = []
    for index, row in enumerate(sorted(selected, key=lambda item: (item["root"], item["repository_path"])), start=1):
        roster.append({
            "capture_id": f"RQ1B-V3-W38-M2-{index:04d}",
            "root": row["root"],
            "domain": row["domain"],
            "discovery_id": row["discovery_id"],
            "commit_sha": row["commit_sha"],
            "repository_path": row["repository_path"],
            "m2_status": "RQ1B_V3_W38_M2_PATH_ROSTER_NOT_A_SOURCE_OR_RESULT",
            "claim_boundary": "This is a selected repository path only. No source body has been fetched, parsed, embedded, scored or used to form a cluster.",
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in roster), encoding="utf-8")
    report = {
        "status": "RQ1B_V3_W38_M2_PATH_ROSTER_COMPLETE_NOT_A_SOURCE_OR_RESULT",
        "m1_path_count": len(rows),
        "selected_path_count": len(roster),
        "root_count": len(by_root),
        "cap_per_root": args.cap_per_root,
        "selection_rule": "Round-robin across sorted first-two-segment path buckets, then sorted within bucket; path strings only.",
        "by_root": by_root_counts,
        "network_calls": 0,
        "source_body_reads": 0,
        "source_body_transfers": 0,
        "claim_boundary": "M2 is deterministic path-only selection, not source admission, triage, cluster construction, prompt construction, label, selector input, metric or result.",
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("m1_path_count", "selected_path_count", "root_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
