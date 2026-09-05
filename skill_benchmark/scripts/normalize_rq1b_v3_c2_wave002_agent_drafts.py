#!/usr/bin/env python3
"""Make schema-only normalisations to persisted RQ1b V3 C2 Wave 002 drafts.

No prompt text, target, constraints, source evidence, or disposition may change.
The only permitted changes are the worker's descriptive paraphrase token and a
unique packet-ID suffix for the two variants.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


RAW_PARAPHRASE = "intent-preserving paraphrase"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()

    raw = read_jsonl(args.input)
    output: list[dict[str, Any]] = []
    changes: list[dict[str, str]] = []
    failures: list[str] = []
    for index, record in enumerate(raw, start=1):
        result = dict(record)
        raw_variant = str(result.get("variant", ""))
        if raw_variant == RAW_PARAPHRASE:
            variant = "paraphrase"
        elif raw_variant == "direct":
            variant = "direct"
        else:
            failures.append(f"row:{index}:unexpected_variant:{raw_variant}")
            continue
        raw_packet_id = str(result.get("c2_packet_id", ""))
        if not raw_packet_id:
            failures.append(f"row:{index}:blank_packet_id")
            continue
        result["variant"] = variant
        result["c2_packet_id"] = f"{raw_packet_id.lower()}-{variant}"
        result["schema_normalisation"] = {
            "normaliser": Path(__file__).name,
            "raw_variant": raw_variant,
            "normalised_variant": variant,
            "raw_c2_packet_id": raw_packet_id,
            "normalised_c2_packet_id": result["c2_packet_id"],
            "unchanged_fields": [
                "prompt_text", "sealed_target_source_id", "c1_review_id",
                "intended_operational_constraints", "construction_rationale",
                "avoided_source_cues", "c2_disposition",
            ],
        }
        changes.append({
            "row": str(index), "raw_variant": raw_variant,
            "normalised_variant": variant, "raw_packet_id": raw_packet_id,
            "normalised_packet_id": result["c2_packet_id"],
        })
        output.append(result)

    output.sort(key=lambda row: (
        str(row["c1_review_id"]), str(row["sealed_target_source_id"]), str(row["variant"]),
    ))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in output),
        encoding="utf-8",
    )
    audit = {
        "status": "C2_SCHEMA_NORMALISATION_PASS_NOT_A_LABEL_OR_RESULT" if not failures else "C2_SCHEMA_NORMALISATION_FAIL_NOT_A_LABEL_OR_RESULT",
        "input_sha256": sha256(args.input),
        "input_rows": len(raw),
        "output_rows": len(output),
        "changes": changes,
        "failures": failures,
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "No prompt semantic, source evidence, cue-safety, adequacy, label, retrieval, model, metric, or result decision was made.",
        ],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: audit[key] for key in audit if key != "changes"}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
