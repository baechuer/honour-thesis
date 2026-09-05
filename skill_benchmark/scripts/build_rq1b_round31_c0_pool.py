#!/usr/bin/env python3
"""Materialise the Round 31 C0 source-only pool from M2 navigation records.

This is a provenance-preserving status bridge. It neither reads full source
bodies nor makes a semantic relation, candidate composition, prompt, label,
or empirical result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


M2_PASS = "M2A_PASS_LOCAL_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m2", type=Path, required=True)
    parser.add_argument("--m2-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    m2_summary = json.loads(args.m2_summary.read_text(encoding="utf-8"))
    if m2_summary.get("status") != M2_PASS:
        raise SystemExit(f"unexpected_m2_status:{m2_summary.get('status')}")
    source_rows = read_jsonl(args.m2)
    ids = [str(row.get("skill_id")) for row in source_rows]
    if len(ids) != len(set(ids)) or len(source_rows) != int(m2_summary.get("inventory_record_count", -1)):
        raise SystemExit("invalid_m2_inventory_contract")

    pool = [{
        **row,
        "c0_pool_status": "SOURCE_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT",
        "source_inventory": str(args.m2),
    } for row in source_rows]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in pool), encoding="utf-8")
    summary = {
        "status": "C0_ROUND31_SOURCE_POOL_READY_NOT_A_CLUSTER_OR_RESULT",
        "m2_input": str(args.m2),
        "source_record_count": len(pool),
        "origin_count": len({str(row["origin"]) for row in pool}),
        "integrity_failures": [],
        "exclusions": [
            "The source pool contains source-navigation metadata only.",
            "No full-source semantic review, candidate composition, prompt, label, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "source_record_count": len(pool), "origin_count": summary["origin_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
