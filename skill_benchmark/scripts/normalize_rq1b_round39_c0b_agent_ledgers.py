#!/usr/bin/env python3
"""Apply schema-only C0B ledger normalisation for Round 39."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from normalize_rq1b_round34_c0b_agent_ledgers import main as normalize_round34_shape


def summary_path(argv: list[str]) -> Path:
    try:
        return Path(argv[argv.index("--summary") + 1])
    except (ValueError, IndexError) as error:
        raise SystemExit("--summary is required") from error


def main() -> int:
    path = summary_path(sys.argv[1:])
    exit_code = normalize_round34_shape()
    summary = json.loads(path.read_text(encoding="utf-8"))
    summary["status"] = "C0B_ROUND39_AGENT_LEDGER_SCHEMA_NORMALISED_PENDING_LITERAL_VALIDATION_NOT_A_CLUSTER_OR_RESULT"
    summary["round"] = "RQ1b cross-source Round 39"
    summary["round34_normalisation_mechanics_reused_only"] = True
    path.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "output_row_count", "rows_with_mechanical_key_normalisation")}, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
