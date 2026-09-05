#!/usr/bin/env python3
"""Mechanically seal complete target-blind reviewer working slices."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--parts", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-prompts", type=int, required=True)
    parser.add_argument("--mode", choices=("target-blind", "prompt-authoring", "full-source"), default="target-blind")
    args = parser.parse_args()

    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite formal return: {args.output}")
    packet_rows = read_jsonl(args.packet)
    if args.mode == "target-blind":
        expected = [(str(row.get("prompt_token")),) for row in packet_rows]
    elif args.mode == "full-source":
        expected = [(str(row.get("family_token")),) for row in packet_rows]
    else:
        expected = [
            (str(row.get("family_token")), str(member.get("member_token")), str(member.get("canonical_source_sha256")))
            for row in packet_rows for member in row.get("members", [])
        ]
    if len(expected) != args.expected_prompts or len(set(expected)) != len(expected) or any("None" in token for token in expected):
        raise SystemExit("Packet does not contain the expected unique bindings")
    rows = [row for part in args.parts for row in read_jsonl(part)]
    if args.mode == "target-blind":
        observed = [(str(row.get("prompt_token")),) for row in rows]
    elif args.mode == "full-source":
        observed = [(str(row.get("family_token")),) for row in rows]
    else:
        observed = [
            (str(row.get("family_token")), str(row.get("target_member_token")), str(row.get("target_source_sha256")))
            for row in rows
        ]
    if len(rows) != args.expected_prompts or len(set(observed)) != len(observed) or set(observed) != set(expected):
        raise SystemExit("Working slices do not exactly reconstruct the blinded packet")
    if args.mode == "target-blind":
        by_token = {(str(row["prompt_token"]),): row for row in rows}
    elif args.mode == "full-source":
        by_token = {(str(row["family_token"]),): row for row in rows}
    else:
        by_token = {
            (str(row["family_token"]), str(row["target_member_token"]), str(row["target_source_sha256"])): row
            for row in rows
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for token in expected:
            handle.write(json.dumps(by_token[token], ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS_TARGET_BLIND_WORKING_PARTS_SEALED", "prompts": len(rows), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
