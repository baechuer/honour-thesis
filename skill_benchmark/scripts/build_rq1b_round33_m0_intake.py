#!/usr/bin/env python3
"""Run frozen M0 canonicalisation and prior-root filtering for Round 33.

Round 33 consumes navigation-only public repository leads. It neither pins a
commit nor reads skill bodies, and it cannot produce candidates, prompts,
labels, retrieval inputs, metrics, or empirical results.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from build_rq1b_round22_m0_intake import main as intake_round22_shape


def option(argv: list[str], name: str) -> Path:
    try:
        return Path(argv[argv.index(name) + 1])
    except (ValueError, IndexError) as error:
        raise SystemExit(f"{name} is required") from error


def rewrite_rows(path: Path) -> None:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    revised = []
    for row in rows:
        if "round22_source_candidate_id" in row:
            identifier = str(row.pop("round22_source_candidate_id"))
            row["round33_source_candidate_id"] = identifier.replace("R22-M0-", "R33-M0-", 1)
        revised.append(row)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in revised),
        encoding="utf-8",
    )


def main() -> int:
    argv = sys.argv[1:]
    canonical = option(argv, "--canonical-output")
    new_roots = option(argv, "--new-root-output")
    summary_path = option(argv, "--summary")
    exit_code = intake_round22_shape()
    rewrite_rows(canonical)
    rewrite_rows(new_roots)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["status"] = "M0_ROUND33_INTAKE_DERIVED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT"
    summary["round"] = "RQ1b cross-source Round 33"
    summary["round22_intake_mechanics_reused_only"] = True
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "raw_discovery_lead_count": summary.get("raw_discovery_lead_count"),
        "canonical_public_source_count": summary.get("canonical_public_source_count"),
        "new_root_intake_count": summary.get("new_root_intake_count"),
        "exact_prior_root_exclusion_count": summary.get("exact_prior_root_exclusion_count"),
    }, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
