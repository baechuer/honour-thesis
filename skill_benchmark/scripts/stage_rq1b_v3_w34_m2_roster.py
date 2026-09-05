#!/usr/bin/env python3
"""Build a deterministic per-root body-capture roster from Wave 034 M1 paths.

No network access occurs here.  The roster is a bounded, path-only staging
artifact; it is not a source frame, candidate composition, or experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.parse
from collections import Counter
from pathlib import Path
from typing import Any


ROOT_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m1-summary", type=Path, required=True)
    parser.add_argument("--path-rows", type=Path, required=True)
    parser.add_argument("--per-root", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("path_row_not_object")
            rows.append(value)
    return rows


def main() -> int:
    args = parse_args()
    summary = json.loads(args.m1_summary.read_text(encoding="utf-8"))
    successful = {
        str(row["root"]): str(row["commit_sha"])
        for row in summary.get("root_rows", [])
        if isinstance(row, dict) and row.get("status") == "M1_PIN_AND_TREE_PASS"
    }
    if not successful:
        raise SystemExit("no_successful_m1_roots")
    grouped: dict[str, list[dict[str, Any]]] = {root: [] for root in successful}
    for row in read_jsonl(args.path_rows):
        root = str(row.get("root", ""))
        if root not in grouped:
            continue
        if row.get("commit_sha") != successful[root]:
            raise SystemExit(f"commit_mismatch:{root}")
        grouped[root].append(row)
    roster: list[dict[str, Any]] = []
    for root in sorted(grouped):
        match = ROOT_RE.fullmatch(root)
        if not match:
            raise SystemExit(f"invalid_root:{root}")
        owner, repo = match.groups()
        ranked = sorted(
            grouped[root],
            key=lambda row: hashlib.sha256(f"rq1b-v3-w34-m2:{root}:{row['repository_path']}".encode("utf-8")).hexdigest(),
        )
        for row in ranked[: args.per_root]:
            path = str(row["repository_path"])
            commit = successful[root]
            roster.append(
                {
                    "status": "RQ1B_V3_W34_M2_BODY_CAPTURE_ROSTER_NOT_A_SOURCE_OR_RESULT",
                    "root": root,
                    "domain": row.get("domain"),
                    "commit_sha": commit,
                    "repository_path": path,
                    "raw_url": f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{urllib.parse.quote(path, safe='/')}",
                    "selection_rule": f"deterministic_sha256_rank_top_{args.per_root}_per_successful_root",
                }
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in roster), encoding="utf-8")
    payload = {
        "status": "RQ1B_V3_W34_M2_ROSTER_PASS_NOT_A_SOURCE_OR_RESULT",
        "successful_root_count": len(successful),
        "per_root_cap": args.per_root,
        "roster_row_count": len(roster),
        "domain_counts": dict(sorted(Counter(str(row.get("domain")) for row in roster).items())),
        "network_calls": 0,
        "body_capture_count": 0,
        "boundary": "A deterministic path roster only; no source body, cluster, prompt, gold, selector, metric or result exists.",
    }
    args.summary.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
