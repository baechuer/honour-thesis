#!/usr/bin/env python3
"""Mechanically inventory literal source cues in RQ1b V3 C2 prompt drafts.

The output is an inventory for manual C3 review, not a cue-safety proof, label,
adequacy decision, retrieval input, model call, metric, or benchmark result.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "in", "into",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "with", "your",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def tokens(value: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", value.lower()) if token not in STOPWORDS]


def ngrams(values: list[str], size: int) -> set[tuple[str, ...]]:
    return {tuple(values[index:index + size]) for index in range(len(values) - size + 1)}


def source_name_phrases(text: str) -> set[tuple[str, ...]]:
    phrases: set[tuple[str, ...]] = set()
    for line in text.splitlines()[:30]:
        stripped = line.strip()
        if stripped.lower().startswith("name:"):
            phrase = tuple(tokens(stripped.split(":", 1)[1]))
            if phrase:
                phrases.add(phrase)
        if stripped.startswith("#"):
            phrase = tuple(tokens(stripped.lstrip("#").strip()))
            if phrase:
                phrases.add(phrase)
            break
    return phrases


def short_prose_lines(text: str) -> list[tuple[int, str, list[str]]]:
    result: list[tuple[int, str, list[str]]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        line_tokens = tokens(stripped)
        if not 3 <= len(line_tokens) <= 12:
            continue
        if stripped.startswith(("#", "```", "- ", "* ", "+ ", "|")):
            continue
        if re.match(r"^[A-Za-z0-9_.-]+\s*:", stripped):
            continue
        if any(character in stripped for character in ("{", "}", "[", "]", "<", ">", "=", ";")):
            continue
        result.append((line_number, line, line_tokens))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-ledger", type=Path, required=True)
    parser.add_argument("--c1-roster", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sources_by_c1: dict[str, dict[str, dict[str, str]]] = {}
    failures: list[str] = []
    for roster_path in args.c1_roster:
        for record in read_jsonl(roster_path):
            c1_id = str(record.get("c1_review_id", ""))
            if c1_id in sources_by_c1:
                failures.append(f"duplicate_c1_roster:{c1_id}")
                continue
            sources_by_c1[c1_id] = {
                str(member["source_id"]): {
                    "path": str(member["absolute_path"]),
                    "title": str(member["title"]),
                }
                for member in record["members"]
            }

    records: list[dict[str, Any]] = []
    for c2 in read_jsonl(args.c2_ledger):
        c1_id = str(c2.get("c1_review_id", ""))
        target_id = str(c2.get("sealed_target_source_id", ""))
        prompt = str(c2.get("prompt_text", ""))
        member_sources = sources_by_c1.get(c1_id)
        if member_sources is None:
            failures.append(f"missing_c1_roster:{c1_id}")
            continue
        if target_id not in member_sources:
            failures.append(f"missing_target_source:{c1_id}:{target_id}")
            continue

        prompt_tokens = tokens(prompt)
        prompt_set = set(prompt_tokens)
        prompt_ngrams = ngrams(prompt_tokens, 3) | ngrams(prompt_tokens, 4)
        title_phrase_hits: list[dict[str, str]] = []
        short_name_token_hits: list[dict[str, str]] = []
        source_phrase_hits: list[dict[str, Any]] = []
        missing_sources: list[str] = []

        for source_id, member in member_sources.items():
            source_path = Path(member["path"])
            if not source_path.is_file():
                missing_sources.append(source_id)
                continue
            source_text = source_path.read_text(encoding="utf-8")
            for phrase in source_name_phrases(source_text):
                if len(phrase) >= 2 and set(phrase).issubset(prompt_set):
                    title_phrase_hits.append({"source_id": source_id, "phrase": " ".join(phrase)})
                elif len(phrase) == 1 and phrase[0] in prompt_set:
                    short_name_token_hits.append({"source_id": source_id, "token": phrase[0]})
            for line_number, line, line_tokens in short_prose_lines(source_text):
                for phrase in sorted(prompt_ngrams & (ngrams(line_tokens, 3) | ngrams(line_tokens, 4))):
                    source_phrase_hits.append({
                        "source_id": source_id,
                        "line": line_number,
                        "phrase": " ".join(phrase),
                        "source_text": line,
                    })

        status = "C3_MECHANICAL_REVIEW_REQUIRED_NOT_A_LABEL_OR_RESULT"
        records.append({
            "c2_packet_id": c2.get("c2_packet_id"),
            "c1_review_id": c1_id,
            "sealed_target_source_id": target_id,
            "variant": c2.get("variant"),
            "prompt_text": prompt,
            "title_phrase_hits": title_phrase_hits,
            "short_source_name_token_hits": short_name_token_hits,
            "source_phrase_hits": source_phrase_hits,
            "missing_sources": missing_sources,
            "mechanical_c3_status": status,
            "boundary": "A literal overlap may be a genuine operational constraint. Manual C3 must distinguish it from an accidental source identifier.",
        })

    summary = {
        "status": "C3_MECHANICAL_CUE_INVENTORY_COMPLETE_NOT_A_LABEL_OR_RESULT" if not failures else "C3_MECHANICAL_CUE_INVENTORY_INCOMPLETE_NOT_A_LABEL_OR_RESULT",
        "packet_count": len(records),
        "title_phrase_hit_packets": sum(bool(row["title_phrase_hits"]) for row in records),
        "short_name_token_hit_packets": sum(bool(row["short_source_name_token_hits"]) for row in records),
        "source_phrase_hit_packets": sum(bool(row["source_phrase_hits"]) for row in records),
        "missing_source_packets": sum(bool(row["missing_sources"]) for row in records),
        "failures": failures,
        "records": records,
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "No cue-safety proof, C4 adequacy decision, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in summary if key != "records"}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
