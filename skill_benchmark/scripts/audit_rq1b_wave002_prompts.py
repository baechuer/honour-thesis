#!/usr/bin/env python3
"""Audit literal source leakage in Wave 002 authoring prompts, locally only.

The audit reads the actual Wave 002 prompt register and draft cards. It reports
candidate-name, heading, and 3/4-token source-phrase overlap. It is curation
QA, not semantic-fidelity evidence or a selector experiment.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
REGISTER = ROOT / "prompts" / "wave_002_p0_authoring_prompt_register.md"
OUTPUT = ROOT / "review" / "wave_002_p1_literal_prompt_overlap_audit.json"
STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "in", "into",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "with", "your",
}


def normalise(value: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", value.lower()) if token not in STOPWORDS]


def ngrams(tokens: list[str], size: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[index:index + size]) for index in range(len(tokens) - size + 1)}


def read_inventory() -> dict[str, dict[str, object]]:
    inventory: dict[str, dict[str, object]] = {}
    manifests = sorted(ROOT.glob("staged_sources/*/source_expansion_manifest.jsonl"))
    if not manifests:
        raise ValueError("No Wave 002 staged-source manifests found")
    for manifest in manifests:
        for line in manifest.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            skill_id = row["skill_id"]
            previous = inventory.get(skill_id)
            if previous and previous != row:
                raise ValueError(f"Conflicting staged-source inventory rows for {skill_id}")
            inventory[skill_id] = row
    return inventory


def read_prompt_sections() -> dict[int, dict[str, str]]:
    text = REGISTER.read_text()
    sections = re.split(r"^## W2-(\d{3}): .*?$", text, flags=re.MULTILINE)
    prompts: dict[int, dict[str, str]] = {}
    for index in range(1, len(sections), 2):
        number = int(sections[index])
        body = sections[index + 1]
        direct = re.search(r"^- Direct:\s*(.*?)(?=^- Paraphrase:)", body, re.MULTILINE | re.DOTALL)
        paraphrase = re.search(
            r"^- Paraphrase:\s*(.*?)(?=^## |^## Required Next Audit|\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        )
        if not direct or not paraphrase:
            raise ValueError(f"Missing direct or paraphrase prompt for W2-{number:03d}")
        prompts[number] = {
            "direct": " ".join(direct.group(1).split()),
            "paraphrase": " ".join(paraphrase.group(1).split()),
        }
    return prompts


def read_candidates(number: int) -> list[str]:
    matches = sorted(ROOT.glob(f"clusters/RQ1B-W2-DRAFT-{number:03d}-*/cluster_card.md"))
    if len(matches) != 1:
        raise ValueError(f"Expected one card for W2-{number:03d}, found {len(matches)}")
    text = matches[0].read_text()
    candidate_block = re.search(
        r"- Candidate skills:\s*(.*?)(?=\n- Preserved originals)",
        text,
        re.DOTALL,
    )
    if not candidate_block:
        raise ValueError(f"Missing candidate block in {matches[0]}")
    candidates = re.findall(r"`([^`]+)`", candidate_block.group(1))
    if len(candidates) != 2:
        raise ValueError(f"Expected two candidates for W2-{number:03d}, found {len(candidates)}")
    return candidates


def audit_prompt(prompt: str, candidates: list[str], inventory: dict[str, dict[str, object]]) -> dict[str, object]:
    prompt_tokens = normalise(prompt)
    prompt_token_set = set(prompt_tokens)
    prompt_phrases = ngrams(prompt_tokens, 3) | ngrams(prompt_tokens, 4)
    candidate_name_hits: list[dict[str, object]] = []
    title_hits: list[dict[str, object]] = []
    phrase_hits: list[dict[str, object]] = []

    for candidate in candidates:
        source = inventory[candidate]
        candidate_name = str(source["frontmatter_name"] or "")
        name_tokens = normalise(candidate_name)
        if name_tokens and set(name_tokens).issubset(prompt_token_set):
            candidate_name_hits.append({"candidate": candidate, "candidate_name": candidate_name})

        source_candidates = list(ROOT.glob(
            f"staged_sources/*/skills/{candidate}/source/SKILL.original.md"
        ))
        if len(source_candidates) != 1:
            raise ValueError(f"Expected one preserved original for {candidate}, found {len(source_candidates)}")
        for line_number, line in enumerate(source_candidates[0].read_text().splitlines(), start=1):
            line_tokens = normalise(line)
            if not line_tokens:
                continue
            if 2 <= len(line_tokens) <= 8 and set(line_tokens).issubset(prompt_token_set):
                title_hits.append({"candidate": candidate, "line": line_number, "source_text": line})
            source_phrases = ngrams(line_tokens, 3) | ngrams(line_tokens, 4)
            for phrase in sorted(prompt_phrases & source_phrases):
                phrase_hits.append({"candidate": candidate, "line": line_number, "phrase": " ".join(phrase)})

    return {
        "prompt": prompt,
        "candidate_name_hits": candidate_name_hits,
        "title_or_short_line_hits": title_hits,
        "multi_token_phrase_hits": phrase_hits,
    }


def main() -> None:
    inventory = read_inventory()
    prompts = read_prompt_sections()
    records = []
    for number in sorted(prompts):
        candidates = read_candidates(number)
        records.append(
            {
                "wave_id": "W2",
                "draft_number": number,
                "cluster_id": f"RQ1B-W2-DRAFT-{number:03d}",
                "candidate_skill_ids": candidates,
                "prompt_audit": [
                    {"prompt_name": name, **audit_prompt(prompt, candidates, inventory)}
                    for name, prompt in prompts[number].items()
                ],
            }
        )

    summary = {
        "audit_type": "RQ1B_WAVE002_LITERAL_PROMPT_OVERLAP_ONLY",
        "status": "LOCAL_CURATION_CHECK_NOT_A_SEMANTIC_LEAKAGE_OR_ROUTING_RESULT",
        "cluster_count": len(records),
        "prompt_count": 2 * len(records),
        "candidate_name_hit_count": sum(
            len(row["candidate_name_hits"])
            for record in records for row in record["prompt_audit"]
        ),
        "title_or_short_line_hit_count": sum(
            len(row["title_or_short_line_hits"])
            for record in records for row in record["prompt_audit"]
        ),
        "multi_token_phrase_hit_count": sum(
            len(row["multi_token_phrase_hits"])
            for record in records for row in record["prompt_audit"]
        ),
        "records": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: summary[key] for key in summary if key.endswith("count")}, indent=2))
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
