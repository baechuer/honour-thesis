#!/usr/bin/env python3
"""Audit literal source cues in cross-source RQ1b C2 prompt drafts, locally.

This checks only candidate-name, title/short-line, and exact three/four-token
overlap against the exact original sources. It creates no label, adequacy
judgment, retrieval input, model call, metric, or benchmark result.
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


def normalise(value: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", value.lower()) if token not in STOPWORDS]


def ngrams(tokens: list[str], size: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[index:index + size]) for index in range(len(tokens) - size + 1)}


def source_titles(lines: list[str], skill_id: str) -> set[tuple[str, ...]]:
    titles = {tuple(normalise(skill_id.replace("-", " ")))}
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            tokens = tuple(normalise(stripped.lstrip("#").strip()))
            if tokens:
                titles.add(tokens)
            break
        if stripped.lower().startswith("name:"):
            tokens = tuple(normalise(stripped.split(":", 1)[1]))
            if tokens:
                titles.add(tokens)
    return titles


def is_natural_language_short_line(line: str, tokens: list[str]) -> bool:
    """Exclude markup and code fragments from the short-line cue rule.

    Candidate names and exact three/four-token phrase overlap are audited
    separately. This predicate limits the short-line check to compact prose so
    YAML keys, code fences, shell fragments, and Markdown structure cannot
    create automatic pseudo-cues merely because a technical prompt contains a
    common token such as ``test`` or ``sql``.
    """

    stripped = line.strip()
    if not 3 <= len(tokens) <= 8:
        return False
    if stripped.startswith(("#", "```", "- ", "* ", "+ ", "|")):
        return False
    if re.match(r"^[A-Za-z0-9_.-]+\s*:", stripped):
        return False
    if any(character in stripped for character in ("{", "}", "[", "]", "<", ">", "=", ";")):
        return False
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--queue", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queue_by_id: dict[str, dict[str, Any]] = {}
    for path in args.queue:
        for row in read_jsonl(path):
            proposal_id = str(row.get("proposal_id", ""))
            if proposal_id in queue_by_id:
                raise SystemExit(f"duplicate_queue_proposal:{proposal_id}")
            queue_by_id[proposal_id] = row

    records: list[dict[str, Any]] = []
    failures: list[str] = []
    for prompt_row in read_jsonl(args.prompts):
        proposal_id = str(prompt_row.get("proposal_id", ""))
        proposal = queue_by_id.get(proposal_id)
        if proposal is None:
            failures.append(f"missing_queue_proposal:{proposal_id}")
            continue
        prompt = str(prompt_row.get("prompt", ""))
        prompt_tokens = normalise(prompt)
        prompt_token_set = set(prompt_tokens)
        prompt_phrases = ngrams(prompt_tokens, 3) | ngrams(prompt_tokens, 4)
        candidate_name_hits: list[dict[str, Any]] = []
        short_line_hits: list[dict[str, Any]] = []
        phrase_hits: list[dict[str, Any]] = []

        for candidate in proposal.get("candidates", []):
            skill_id = str(candidate.get("skill_id", ""))
            path = Path(str(candidate.get("local_original_path", "")))
            if not path.is_file():
                failures.append(f"missing_source:{proposal_id}:{skill_id}")
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            for name_tokens in source_titles(lines, skill_id):
                if name_tokens and set(name_tokens).issubset(prompt_token_set):
                    candidate_name_hits.append({"skill_id": skill_id, "candidate_name_tokens": " ".join(name_tokens)})
            for line_number, line in enumerate(lines, start=1):
                line_tokens = normalise(line)
                if not line_tokens:
                    continue
                if is_natural_language_short_line(line, line_tokens) and set(line_tokens).issubset(prompt_token_set):
                    short_line_hits.append({"skill_id": skill_id, "line": line_number, "source_text": line})
                source_phrases = ngrams(line_tokens, 3) | ngrams(line_tokens, 4)
                for phrase in sorted(prompt_phrases & source_phrases):
                    phrase_hits.append({"skill_id": skill_id, "line": line_number, "phrase": " ".join(phrase)})

        cue_status = "C3_LITERAL_CUE_PASS_NOT_A_LABEL_OR_RESULT"
        if candidate_name_hits or short_line_hits or phrase_hits:
            cue_status = "C3_LITERAL_CUE_REVIEW_REQUIRED_NOT_A_LABEL_OR_RESULT"
        records.append({
            "c3_status": cue_status,
            "proposal_id": proposal_id,
            "intended_candidate_skill_id": prompt_row.get("intended_candidate_skill_id"),
            "variant": prompt_row.get("variant"),
            "prompt": prompt,
            "candidate_name_hits": candidate_name_hits,
            "title_or_short_line_hits": short_line_hits,
            "multi_token_phrase_hits": phrase_hits,
            "exclusions": [
                "Literal cue audit is not a semantic-leakage proof.",
                "No gold label, adequacy judgment, retrieval input, model call, metric, or frozen benchmark cluster was created.",
            ],
        })

    summary = {
        "status": "C3_LITERAL_CUE_AUDIT_COMPLETE_NOT_A_LABEL_OR_RESULT" if not failures else "C3_LITERAL_CUE_AUDIT_INCOMPLETE_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(records),
        "literal_pass_count": sum(row["c3_status"] == "C3_LITERAL_CUE_PASS_NOT_A_LABEL_OR_RESULT" for row in records),
        "review_required_count": sum(row["c3_status"] == "C3_LITERAL_CUE_REVIEW_REQUIRED_NOT_A_LABEL_OR_RESULT" for row in records),
        "failures": failures,
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "prompt_count", "literal_pass_count", "review_required_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
