#!/usr/bin/env python3
"""Materialise blinded C4 adequacy-review cards for cross-source RQ1b drafts.

Reviewer packets contain a prompt and anonymous candidate cards only. The
separate key retains candidate identities for later consensus processing. This
is local curation scaffolding, not a label, retrieval input, model call,
metric, or frozen benchmark cluster.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


IDENTITY_SECTION_TITLES = {
    "related skills",
    "related skill",
    "see also",
    "references",
    "links",
    "further reading",
}


def scrub_source(text: str) -> str:
    """Remove source/provenance cues while retaining capability evidence."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                lines = lines[index + 1:]
                break
    title: str | None = None
    retained: list[str] = []
    skip_identity_section = False
    for line in lines:
        heading = re.match(r"^\s*#+\s+(.+?)\s*#*\s*$", line)
        if heading:
            heading_text = heading.group(1).strip()
            if title is None:
                title = heading_text
                continue
            skip_identity_section = heading_text.casefold() in IDENTITY_SECTION_TITLES
            if skip_identity_section:
                continue
        if skip_identity_section:
            continue
        line = re.sub(r"<!--.*?-->", "", line)
        # Some skills describe an HTML comment marker literally, often without
        # closing it on the same line. Preserve the instruction but remove the
        # comment-shaped token from reviewer cards.
        line = line.replace("<!--", "[REDACTED_COMMENT_MARKER]").replace("-->", "")
        line = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
        line = re.sub(r"https?://\S+", "[REDACTED_URL]", line)
        if line.strip():
            retained.append(line)
    cleaned = "\n".join(retained).strip()
    if title:
        cleaned = re.sub(re.escape(title), "[REDACTED_SKILL_TITLE]", cleaned, flags=re.IGNORECASE)
    return cleaned + "\n"


def assert_blind_card(text: str, candidate: dict[str, Any]) -> None:
    """Fail closed if a packet still reveals stored source provenance."""
    source_path = str(candidate.get("source_repository_path", ""))
    # A bare SKILL.md is a generic artifact name, not source identity. Paths
    # with directories can identify a source layout and remain prohibited.
    path_marker = source_path if "/" in source_path else ""
    prohibited = [
        str(candidate.get("repository_url", "")),
        path_marker,
        str(candidate.get("skill_id", "")),
    ]
    for value in prohibited:
        if value and value.casefold() in text.casefold():
            raise ValueError(f"unredacted_source_marker:{value}")
    if re.search(r"https?://|<!--|github\\.com", text, flags=re.IGNORECASE):
        raise ValueError("unredacted_url_or_comment")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--queue", type=Path, action="append", required=True)
    parser.add_argument(
        "--source-pool",
        type=Path,
        help="Optional frozen source pool used to resolve candidate_skill_ids in an ID-only C0/C1 queue.",
    )
    parser.add_argument("--reviewer-input", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--seed", default="rq1b-cross-source-c4-r02")
    parser.add_argument("--packet-prefix", default="C4R02")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_by_id: dict[str, dict[str, Any]] = {}
    if args.source_pool:
        source_by_id = {
            str(row.get("skill_id", "")): row
            for row in read_jsonl(args.source_pool)
            if str(row.get("skill_id", ""))
        }
    queue_by_id: dict[str, dict[str, Any]] = {}
    for path in args.queue:
        for row in read_jsonl(path):
            proposal_id = str(row.get("proposal_id", ""))
            if proposal_id in queue_by_id:
                raise SystemExit(f"duplicate_queue_proposal:{proposal_id}")
            if not row.get("candidates") and row.get("candidate_skill_ids"):
                ids = [str(value) for value in row["candidate_skill_ids"]]
                missing = [skill_id for skill_id in ids if skill_id not in source_by_id]
                if missing:
                    raise SystemExit(f"missing_source_pool_candidates:{proposal_id}:{','.join(missing)}")
                row = {**row, "candidates": [source_by_id[skill_id] for skill_id in ids]}
            queue_by_id[proposal_id] = row

    prompts_by_proposal: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(args.prompts):
        prompts_by_proposal[str(row["proposal_id"])].append(row)

    packets: list[dict[str, Any]] = []
    keys: list[dict[str, Any]] = []
    labels = ["Candidate A", "Candidate B", "Candidate C", "Candidate D"]
    failures: list[str] = []

    for cluster_index, proposal_id in enumerate(sorted(prompts_by_proposal), start=1):
        proposal = queue_by_id.get(proposal_id)
        if proposal is None:
            failures.append(f"missing_queue_proposal:{proposal_id}")
            continue
        candidates = proposal.get("candidates", [])
        if not 3 <= len(candidates) <= 4:
            failures.append(f"candidate_count:{proposal_id}:{len(candidates)}")
            continue
        ordered = list(candidates)
        seed_int = int(hashlib.sha256(f"{args.seed}:{proposal_id}".encode()).hexdigest(), 16)
        random.Random(seed_int).shuffle(ordered)
        cards: list[dict[str, str]] = []
        label_key: list[dict[str, str]] = []
        for index, candidate in enumerate(ordered):
            source = Path(str(candidate.get("local_original_path", "")))
            if not source.is_file():
                failures.append(f"missing_source:{proposal_id}:{candidate.get('skill_id')}")
                continue
            card_label = labels[index]
            card_text = scrub_source(source.read_text(encoding="utf-8"))
            assert_blind_card(card_text, candidate)
            cards.append({"card_label": card_label, "card_text": card_text})
            label_key.append({"card_label": card_label, "skill_id": str(candidate.get("skill_id")), "source_sha256": str(candidate.get("source_sha256"))})
        if len(cards) != len(candidates):
            continue
        for prompt_index, prompt_row in enumerate(sorted(prompts_by_proposal[proposal_id], key=lambda row: (str(row.get("variant")), str(row.get("intended_candidate_skill_id"))))):
            packets.append({
                "c4_status": "C4_BLIND_PACKET_MATERIALISED_NOT_A_LABEL_OR_RESULT",
                "review_packet_id": f"{args.packet_prefix}-{len(packets) + 1:03d}",
                "proposal_ref": f"cluster-{cluster_index:03d}",
                "prompt_ref": f"prompt-{prompt_index + 1:02d}",
                "prompt": str(prompt_row["prompt"]),
                "candidate_cards": cards,
                "review_instructions": "For each anonymous candidate, mark fully_adequate, partially_adequate, or not_adequate for this prompt and cite short evidence from the card. Do not infer a hidden gold label.",
                "exclusions": ["No candidate identity, repository, intended label, retrieval result, or metric is present in this reviewer input."],
            })
            keys.append({
                "review_packet_id": packets[-1]["review_packet_id"],
                "proposal_id": proposal_id,
                "prompt_variant": prompt_row.get("variant"),
                "intended_candidate_skill_id_sealed": prompt_row.get("intended_candidate_skill_id"),
                "card_key": label_key,
                "status": "C4_KEY_SEALED_NOT_A_LABEL_OR_RESULT",
            })

    args.reviewer_input.parent.mkdir(parents=True, exist_ok=True)
    args.key.parent.mkdir(parents=True, exist_ok=True)
    args.reviewer_input.write_text("".join(json.dumps(row, ensure_ascii=True) + "\n" for row in packets), encoding="utf-8")
    args.key.write_text("".join(json.dumps(row, ensure_ascii=True) + "\n" for row in keys), encoding="utf-8")
    print(json.dumps({"packet_count": len(packets), "key_count": len(keys), "failures": failures, "status": "C4_PACKET_PASS_NOT_A_LABEL_OR_RESULT" if not failures else "C4_PACKET_INCOMPLETE_NOT_A_LABEL_OR_RESULT"}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
