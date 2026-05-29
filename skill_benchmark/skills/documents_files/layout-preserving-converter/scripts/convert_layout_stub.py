#!/usr/bin/env python3
"""Lightweight document-to-markdown layout normalizer.

This is not a full document converter. It is a small helper for preserving
headings, labels, and simple table-like rows in a stable text format.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^\s*([A-Z][A-Za-z0-9 /&-]{2,}|Section[: ]+.+)\s*$")
LABEL_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 /_-]{1,40})\s*:\s*(.+?)\s*$")
TABLE_SPLIT_RE = re.compile(r"\s{2,}|\t+")


def normalize_lines(text: str) -> list[str]:
    lines = [line.rstrip() for line in text.splitlines()]
    out: list[str] = []
    pending_table: list[list[str]] = []

    def flush_table() -> None:
        nonlocal pending_table
        if not pending_table:
            return
        width = max(len(row) for row in pending_table)
        padded = [row + [""] * (width - len(row)) for row in pending_table]
        header = "| " + " | ".join(padded[0]) + " |"
        rule = "| " + " | ".join(["---"] * width) + " |"
        out.append(header)
        out.append(rule)
        for row in padded[1:]:
            out.append("| " + " | ".join(row) + " |")
        pending_table = []

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_table()
            if out and out[-1] != "":
                out.append("")
            continue

        if HEADING_RE.match(line):
            flush_table()
            if out and out[-1] != "":
                out.append("")
            out.append(f"## {line}")
            continue

        label_match = LABEL_RE.match(line)
        if label_match:
            flush_table()
            out.append(f"- {label_match.group(1)}: {label_match.group(2)}")
            continue

        columns = [part.strip() for part in TABLE_SPLIT_RE.split(line) if part.strip()]
        if len(columns) >= 3:
            pending_table.append(columns)
            continue

        flush_table()
        if line.startswith(("-", "*")):
            out.append(f"- {line[1:].strip()}")
        else:
            out.append(line)

    flush_table()
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Preserve simple document layout cues in markdown.")
    parser.add_argument("input", nargs="?", help="Input file. Reads stdin if omitted.")
    parser.add_argument("-o", "--output", help="Optional output file. Prints to stdout if omitted.")
    args = parser.parse_args()

    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    result = "\n".join(normalize_lines(text)).strip() + "\n"

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
