#!/usr/bin/env python3
"""Map legacy RQ1b cross-source C6 primary records into the V3 source frame.

This is a local provenance audit only. It does not merge protocols, construct
V3 cards, create prompts or labels, or produce retrieval evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


BOUNDARY = (
    "This audit maps immutable legacy C6 source hashes into the V3 source frame. "
    "It does not merge the legacy and V3 protocols, validate V3 card preservation, "
    "create a V3 strict cluster, or establish human annotation, retrieval, or a field effect."
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-manifest-dir", type=Path, required=True)
    parser.add_argument("--v3-source-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists():
        raise SystemExit(f"refusing_to_overwrite:{args.output}")
    source_rows = read_jsonl(args.v3_source_manifest)
    source_by_sha = {row["sha256"]: row["source_id"] for row in source_rows}
    c6_paths = sorted(args.legacy_manifest_dir.glob("c6*.jsonl"))
    if not c6_paths:
        raise SystemExit("no_c6_jsonl_files")

    packet_rows: list[dict[str, Any]] = []
    input_hashes: dict[str, str] = {}
    for path in c6_paths:
        input_hashes[path.name] = sha256_file(path)
        for line_number, row in enumerate(read_jsonl(path), start=1):
            if not str(row.get("c6_status", "")).startswith("C6_FROZEN_PRIMARY"):
                continue
            candidate_hashes = row.get("candidate_source_sha256")
            if not isinstance(candidate_hashes, list) or len(candidate_hashes) not in (3, 4):
                raise SystemExit(f"invalid_candidate_hashes:{path.name}:{line_number}")
            packet_rows.append({
                "file": path.name,
                "line": line_number,
                "review_packet_id": row.get("review_packet_id"),
                "proposal_id": row.get("proposal_id"),
                "prompt_variant": row.get("prompt_variant"),
                "candidate_source_sha256": candidate_hashes,
            })

    composition_map: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for packet in packet_rows:
        composition_map.setdefault(tuple(sorted(packet["candidate_source_sha256"])), []).append(packet)
    compositions: list[dict[str, Any]] = []
    unmapped_compositions = 0
    for index, (hashes, packets) in enumerate(sorted(composition_map.items()), start=1):
        mapped_ids = [source_by_sha.get(value) for value in hashes]
        mapped = all(mapped_ids)
        unmapped_compositions += int(not mapped)
        compositions.append({
            "legacy_composition_index": index,
            "candidate_source_sha256": list(hashes),
            "v3_source_ids": mapped_ids,
            "candidate_count": len(hashes),
            "fully_mapped_to_v3_source_frame": mapped,
            "legacy_packet_count": len(packets),
            "legacy_proposal_ids": sorted({item["proposal_id"] for item in packets}),
            "legacy_variants": dict(sorted(Counter(item["prompt_variant"] for item in packets).items())),
        })

    distinct_review_ids = {item["review_packet_id"] for item in packet_rows}
    result = {
        "status": "RQ1B_LEGACY_C6_TO_V3_SOURCE_FRAME_MAPPING_PASS_NOT_MERGED" if not unmapped_compositions else "RQ1B_LEGACY_C6_TO_V3_SOURCE_FRAME_MAPPING_INCOMPLETE_NOT_MERGED",
        "legacy_c6_files_scanned": len(c6_paths),
        "legacy_primary_packet_rows": len(packet_rows),
        "distinct_legacy_review_packet_ids": len(distinct_review_ids),
        "legacy_candidate_compositions": len(compositions),
        "composition_cardinality": dict(sorted(Counter(item["candidate_count"] for item in compositions).items())),
        "fully_mapped_compositions": len(compositions) - unmapped_compositions,
        "unmapped_compositions": unmapped_compositions,
        "v3_source_frame_records": len(source_rows),
        "legacy_c6_file_sha256": input_hashes,
        "v3_source_manifest_sha256": sha256_file(args.v3_source_manifest),
        "compositions": compositions,
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
        "protocol_boundary": [
            "The legacy campaign's C3/C4 records are model-assisted rather than human annotation.",
            "Hash mapping proves only byte-level source inclusion in the V3 source frame.",
            "A mapped legacy composition cannot be counted as V3 C4A/C4B/C5/C6 without an explicit future compatibility amendment and the required V3 gates.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "legacy_primary_packet_rows", "distinct_legacy_review_packet_ids", "legacy_candidate_compositions", "fully_mapped_compositions", "unmapped_compositions")}, sort_keys=True))
    return 0 if not unmapped_compositions else 1


if __name__ == "__main__":
    raise SystemExit(main())
