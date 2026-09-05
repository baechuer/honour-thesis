#!/usr/bin/env python3
"""Audit literal source leakage in RQ1b task prompts, locally only.

The audit reports exact title/headings and multi-token phrase overlap between a
prompt and its candidate originals. It is a curation check, not a semantic
leakage proof and not a selector experiment.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
INVENTORY = ROOT / "manifest" / "source_inventory.jsonl"
STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "in", "into",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "with", "your",
}


def normalise(value: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", value.lower()) if token not in STOPWORDS]


def ngrams(tokens: list[str], size: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[index:index + size]) for index in range(len(tokens) - size + 1)}


def source_lines(source_path: Path) -> list[str]:
    return source_path.read_text().splitlines()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("selection", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    inventory = {
        row["skill_id"]: row
        for row in (json.loads(line) for line in INVENTORY.read_text().splitlines() if line.strip())
    }
    selection = json.loads(args.selection.read_text())
    audit = json.loads((ROOT / "manifest" / "draft_pool_audit.json").read_text())
    drafts = {int(card["id"].split()[-1]): card for card in audit["cards"]}
    records: list[dict[str, Any]] = []

    for record in selection["records"]:
        draft = drafts[int(record["draft_number"])]
        candidate_sources = {
            candidate: source_lines(Path(inventory[candidate]["source_path"]))
            for candidate in draft["candidates"]
        }
        prompt_rows = []
        for prompt_name in ("direct_prompt", "paraphrase_prompt"):
            prompt = record[prompt_name]
            prompt_tokens = normalise(prompt)
            prompt_phrases = ngrams(prompt_tokens, 3) | ngrams(prompt_tokens, 4)
            prompt_token_set = set(prompt_tokens)
            candidate_name_hits = []
            title_hits = []
            phrase_hits = []
            for candidate, lines in candidate_sources.items():
                candidate_name_tokens = normalise(inventory[candidate]["frontmatter_name"] or "")
                if candidate_name_tokens and set(candidate_name_tokens).issubset(prompt_token_set):
                    candidate_name_hits.append({
                        "candidate": candidate,
                        "candidate_name": inventory[candidate]["frontmatter_name"],
                    })
                for line_number, line in enumerate(lines, start=1):
                    line_tokens = normalise(line)
                    if not line_tokens:
                        continue
                    if len(line_tokens) <= 8 and set(line_tokens).issubset(set(prompt_tokens)):
                        title_hits.append({
                            "candidate": candidate,
                            "line": line_number,
                            "source_text": line,
                        })
                    source_phrases = ngrams(line_tokens, 3) | ngrams(line_tokens, 4)
                    for phrase in sorted(prompt_phrases & source_phrases):
                        phrase_hits.append({
                            "candidate": candidate,
                            "line": line_number,
                            "phrase": " ".join(phrase),
                        })
            prompt_rows.append({
                "prompt_name": prompt_name,
                "prompt": prompt,
                "candidate_name_hits": candidate_name_hits,
                "title_or_short_line_hits": title_hits,
                "multi_token_phrase_hits": phrase_hits,
            })
        records.append({
            "draft_number": record["draft_number"],
            "cluster_id": f"RQ1B-W001-{int(record['draft_number']):03d}",
            "candidate_skill_ids": draft["candidates"],
            "prompt_audit": prompt_rows,
        })

    summary = {
        "audit_type": "RQ1B_LITERAL_PROMPT_OVERLAP_ONLY",
        "status": "LOCAL_CURATION_CHECK_NOT_A_SEMANTIC_LEAKAGE_OR_ROUTING_RESULT",
        "selection": str(args.selection),
        "cluster_count": len(records),
        "title_or_short_line_hit_count": sum(
            len(row["title_or_short_line_hits"])
            for record in records for row in record["prompt_audit"]
        ),
        "candidate_name_hit_count": sum(
            len(row["candidate_name_hits"])
            for record in records for row in record["prompt_audit"]
        ),
        "multi_token_phrase_hit_count": sum(
            len(row["multi_token_phrase_hits"])
            for record in records for row in record["prompt_audit"]
        ),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({
        "cluster_count": summary["cluster_count"],
        "title_or_short_line_hit_count": summary["title_or_short_line_hit_count"],
        "multi_token_phrase_hit_count": summary["multi_token_phrase_hit_count"],
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
