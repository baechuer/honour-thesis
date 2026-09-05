#!/usr/bin/env python3
"""Deterministically split Round 38 blinded C4 packets into two reviewer slices."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True) + "\n" for row in rows), encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--slice", type=Path, action="append", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    if len(args.slice) != 2:
        raise SystemExit("requires_exactly_two_slices")
    packets = sorted(read_jsonl(args.input), key=lambda row: str(row.get("review_packet_id", "")))
    packet_ids = [str(row.get("review_packet_id", "")) for row in packets]
    if not packet_ids or len(packet_ids) != len(set(packet_ids)) or len(packets) % 2:
        raise SystemExit("invalid_packet_set")
    size = len(packets) // 2
    outputs = []
    for index, path in enumerate(args.slice):
        rows = packets[index * size:(index + 1) * size]
        write_jsonl(path, rows)
        outputs.append({"slice_index": index + 1, "path": str(path), "sha256": sha256(path), "packet_ids": [str(row["review_packet_id"]) for row in rows]})
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({
        "status": "C4_BLIND_PACKET_SLICES_MATERIALISED_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "packet_count": len(packets),
        "slices": outputs,
        "exclusions": ["No candidate identity, repository, intended label, adequacy judgment, retrieval input, model result, metric, or frozen cluster was created."],
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "packet_slices_written", "packet_count": len(packets), "slice_count": len(outputs), "slice_size": size}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
