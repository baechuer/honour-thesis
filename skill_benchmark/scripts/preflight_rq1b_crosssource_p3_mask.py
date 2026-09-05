#!/usr/bin/env python3
"""Fail-closed P3 preflight for one P1/P2 union; never writes a masked copy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def occurrences(text: str, quote: str) -> list[tuple[int, int]]:
    positions: list[tuple[int, int]] = []
    start = 0
    while True:
        index = text.find(quote, start)
        if index < 0:
            return positions
        positions.append((index, index + len(quote)))
        start = index + 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p1-root", type=Path, required=True)
    parser.add_argument("--family-id", required=True)
    parser.add_argument("--union", type=Path, required=True)
    args = parser.parse_args()

    family_dir = args.p1_root / args.family_id
    packet = json.loads((family_dir / "p1_evidence_mapping_packet.json").read_text())
    union = json.loads(args.union.read_text())
    candidate_text = {
        item["label"]: (family_dir / item["text_path"]).read_text()
        for item in packet["candidates"]
    }

    failures: list[str] = []
    proposed: dict[str, list[dict]] = {label: [] for label in candidate_text}
    for record in union.get("records", []):
        classification = record.get("classification")
        if classification == "inseparable_structural_cue" or classification == "UNRESOLVED":
            failures.append(f"unsafe_union_classification:{classification}")
            continue
        if classification != "differential_target_field":
            continue
        label, quote, replacement = record.get("candidate"), record.get("quote"), record.get("replacement")
        if label not in candidate_text or not isinstance(quote, str) or not quote:
            failures.append("malformed_differential_record")
            continue
        if not isinstance(replacement, str):
            failures.append(f"missing_replacement:{label}")
            continue
        hits = occurrences(candidate_text[label], quote)
        if len(hits) != 1:
            failures.append(f"nonunique_or_missing_span:{label}:{len(hits)}")
            continue
        start, end = hits[0]
        proposed[label].append({"start": start, "end": end, "quote": quote, "replacement": replacement})

    for label, spans in proposed.items():
        ordered = sorted(spans, key=lambda item: (item["start"], item["end"], item["replacement"]))
        for left, right in zip(ordered, ordered[1:]):
            if right["start"] < left["end"]:
                failures.append(f"overlapping_target_spans:{label}")

    payload = {
        "status": (
            "P3_MASK_CONSTRUCTION_PREFLIGHT_PASS_NOT_A_MASK_OR_RESULT"
            if not failures
            else "P3_MASK_CONSTRUCTION_PREFLIGHT_FAIL_ORIGINAL_ONLY"
        ),
        "family_id": args.family_id,
        "union": str(args.union),
        "candidate_span_counts": {label: len(spans) for label, spans in proposed.items()},
        "failures": sorted(set(failures)),
        "exclusions": [
            "No source was changed.",
            "No masked copy was written.",
            "No selector, embedding, retrieval, API call, metric, or result exists.",
        ],
    }
    output = args.p1_root / "audits" / f"{args.family_id}_p3_preflight.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "status": payload["status"], "failure_count": len(payload["failures"])}, sort_keys=True))


if __name__ == "__main__":
    main()
