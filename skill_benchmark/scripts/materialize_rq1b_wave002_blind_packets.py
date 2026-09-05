#!/usr/bin/env python3
"""Materialise local-only, blinded Wave 002 RQ1b review packets.

Packets contain only two task prompts and unmodified original candidate
artifacts. Authoring metadata is retained separately for later curation, never
inside a blinded packet. This program does not call a model or a selector, and
does not validate a cluster.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
REGISTER = ROOT / "prompts" / "wave_002_p0_authoring_prompt_register.md"
WAVE_ONE_MANIFEST = ROOT / "manifest" / "wave_001_frozen_manifest.jsonl"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_staged_inventory() -> dict[str, dict[str, object]]:
    inventory: dict[str, dict[str, object]] = {}
    manifests = sorted(ROOT.glob("staged_sources/*/source_expansion_manifest.jsonl"))
    if not manifests:
        raise ValueError("no staged-source manifests found")
    for manifest in manifests:
        for line in manifest.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            source_path = manifest.parent / "skills" / row["skill_id"] / "source" / "SKILL.original.md"
            previous = inventory.get(row["skill_id"])
            if previous is not None and previous["source_sha256"] != row["source_sha256"]:
                raise ValueError(f"conflicting staged sources for {row['skill_id']}")
            inventory[row["skill_id"]] = {**row, "local_source_path": source_path}
    return inventory


def parse_prompt_register() -> dict[int, dict[str, str]]:
    text = REGISTER.read_text()
    sections = re.split(r"^## W2-(\d{3}): .*?$", text, flags=re.MULTILINE)
    prompts: dict[int, dict[str, str]] = {}
    for index in range(1, len(sections), 2):
        number = int(sections[index])
        body = sections[index + 1]
        primary = re.search(
            r"^- `authoring_primary_candidate`:\s*(?:\n\s*)?`([^`]+)`",
            body,
            re.MULTILINE,
        )
        field = re.search(r"^- `tentative_primary_field`:\s*`([^`]+)`", body, re.MULTILINE)
        direct = re.search(r"^- Direct:\s*(.*?)(?=^- Paraphrase:)", body, re.MULTILINE | re.DOTALL)
        paraphrase = re.search(
            r"^- Paraphrase:\s*(.*?)(?=^## |^## Required Next Audit|\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        )
        if not primary or not field or not direct or not paraphrase:
            raise ValueError(f"unparseable prompt block W2-{number:03d}")
        prompts[number] = {
            "authoring_primary_candidate": primary.group(1),
            "primary_field": field.group(1),
            "direct_prompt": " ".join(direct.group(1).split()),
            "paraphrase_prompt": " ".join(paraphrase.group(1).split()),
        }
    return prompts


def card_for(number: int) -> Path:
    cards = sorted(ROOT.glob(f"clusters/RQ1B-W2-DRAFT-{number:03d}-*/cluster_card.md"))
    if len(cards) != 1:
        raise ValueError(f"expected one card for W2-{number:03d}, found {len(cards)}")
    return cards[0]


def candidates_for(number: int) -> list[str]:
    text = card_for(number).read_text()
    if "| Task-like prompt feasibility | `P1 PASS`" not in text:
        raise ValueError(f"W2-{number:03d} has not passed P1")
    candidate_block = re.search(r"- Candidate skills:\s*(.*?)(?=\n- Preserved originals)", text, re.DOTALL)
    if not candidate_block:
        raise ValueError(f"missing candidates in W2-{number:03d}")
    candidates = re.findall(r"`([^`]+)`", candidate_block.group(1))
    if len(candidates) != 2 or len(set(candidates)) != 2:
        raise ValueError(f"W2-{number:03d} must have exactly two distinct candidates")
    return candidates


def wave_one_candidates() -> set[str]:
    candidates: set[str] = set()
    for line in WAVE_ONE_MANIFEST.read_text().splitlines():
        if line.strip():
            candidates.update(json.loads(line)["candidate_skill_ids"])
    return candidates


def render_artifact(label: str, candidate: str, source: dict[str, object]) -> str:
    source_path = Path(str(source["local_source_path"]))
    if not source_path.exists():
        raise ValueError(f"missing source: {source_path}")
    if sha256(source_path) != source["source_sha256"]:
        raise ValueError(f"source hash changed: {candidate}")
    return "\n".join(
        [
            f"## Artifact {label}",
            "",
            source_path.read_text().rstrip(),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-wave", default="wave_002")
    parser.add_argument("--draft-numbers", nargs="+", type=int, default=list(range(1, 18)))
    args = parser.parse_args()
    selected_numbers = sorted(set(args.draft_numbers))
    if not selected_numbers or any(number < 1 or number > 17 for number in selected_numbers):
        raise ValueError("draft numbers must be in the inclusive range 1..17")

    inventory = load_staged_inventory()
    prompts = parse_prompt_register()
    if sorted(prompts) != list(range(1, 18)):
        raise ValueError("expected exactly W2-001 through W2-017 prompt blocks")

    output = ROOT / "review" / args.review_wave
    authoring_dir = output / "authoring_packets"
    blind_dir = output / "blind_packets"
    authoring_dir.mkdir(parents=True, exist_ok=True)
    blind_dir.mkdir(parents=True, exist_ok=True)

    wave_one = wave_one_candidates()
    wave_two_usage: dict[str, list[str]] = {}
    packets = []
    for number in selected_numbers:
        metadata = prompts[number]
        candidates = candidates_for(number)
        if metadata["authoring_primary_candidate"] not in candidates:
            raise ValueError(f"authoring primary is not a W2-{number:03d} candidate")
        unknown = sorted(set(candidates) - set(inventory))
        if unknown:
            raise ValueError(f"unknown W2-{number:03d} candidates: {unknown}")
        overlap = sorted(set(candidates) & wave_one)
        if overlap:
            raise ValueError(f"Wave 001 candidate reuse in W2-{number:03d}: {overlap}")
        for candidate in candidates:
            wave_two_usage.setdefault(candidate, []).append(f"RQ1B-W2-DRAFT-{number:03d}")

        packet_id = f"{args.review_wave}-C{number:03d}"
        source_hashes = {candidate: inventory[candidate]["source_sha256"] for candidate in candidates}
        private = {
            "packet_id": packet_id,
            "wave_id": "W2",
            "cluster_id": f"RQ1B-W2-DRAFT-{number:03d}",
            "candidate_skill_ids": candidates,
            "primary_field": metadata["primary_field"],
            "authoring_primary_candidate": metadata["authoring_primary_candidate"],
            "source_evidence_status": "SOURCE_BACKED_DRAFT_P1_PASS",
            "masking_eligibility": "PENDING_RESIDUAL_CUE_AUDIT",
            "source_hashes": source_hashes,
        }
        authoring = "\n".join(
            [
                f"# {packet_id} Authoring Packet",
                "",
                "Status: `CURATION ONLY / P2 NOT REVIEWED / NOT A VALID CLUSTER / NO RETRIEVAL`",
                "",
                "## Private Curation Metadata",
                "",
                "```json",
                json.dumps(private, indent=2),
                "```",
                "",
                "## Proposed Task Prompts",
                "",
                f"- Direct: {metadata['direct_prompt']}",
                f"- Independently phrased: {metadata['paraphrase_prompt']}",
                "",
            ]
        )
        blind_candidates = sorted(candidates)
        blind = "\n".join(
            [
                f"# {packet_id} Blinded Acceptability Packet",
                "",
                "Status: `REVIEW MATERIAL / NO DECLARED FIELD OR INTENDED LABEL`",
                "",
                "## Task A",
                "",
                metadata["direct_prompt"],
                "",
                "## Task B",
                "",
                metadata["paraphrase_prompt"],
                "",
                "## Candidate Artifacts",
                "",
                "\n\n---\n\n".join(
                    render_artifact(chr(ord("A") + position), candidate, inventory[candidate])
                    for position, candidate in enumerate(blind_candidates)
                ),
                "",
                "## Reviewer Response",
                "",
                "For each task and artifact, assign exactly one: `acceptable`, "
                "`plausible_but_insufficient`, or `not_acceptable`. State why "
                "each acceptable artifact satisfies all material conditions, or "
                "why another artifact fails. Do not infer a declared target, "
                "field, provenance, or retrieval result.",
                "",
            ]
        )
        (authoring_dir / f"{packet_id}.md").write_text(authoring)
        (blind_dir / f"{packet_id}.md").write_text(blind)
        packets.append({
            **private,
            "blind_candidate_order": blind_candidates,
            "direct_prompt": metadata["direct_prompt"],
            "paraphrase_prompt": metadata["paraphrase_prompt"],
        })

    reused = {candidate: clusters for candidate, clusters in wave_two_usage.items() if len(clusters) > 1}
    if reused:
        raise ValueError(f"Wave 002 candidate reuse: {reused}")
    summary = {
        "status": "P2_BLIND_PACKETS_MATERIALISED_NOT_REVIEWED_NOT_VALID",
        "wave_id": "W2",
        "review_wave": args.review_wave,
        "cluster_count": len(packets),
        "prompt_count": 2 * len(packets),
        "candidate_skill_count": len(wave_two_usage),
        "candidate_reuse_count": len(reused),
        "candidate_overlap_with_wave_001_count": 0,
        "external_calls": 0,
        "retrieval_runs": 0,
        "packets": packets,
    }
    (output / "packet_manifest.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: summary[key] for key in summary if key.endswith("count")}, indent=2))
    print(f"output={output}")


if __name__ == "__main__":
    main()
