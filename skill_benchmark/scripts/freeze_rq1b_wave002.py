#!/usr/bin/env python3
"""Freeze the independently curated Wave 002 RQ1b natural-original set.

This is a local-only evidence join.  It refuses to write a manifest unless the
final P0 register, P1 literal-overlap audit, current P2 blind decisions, P3
original-only decisions, source bytes, and Wave 001 disjointness all agree.
It deliberately implements no masking, selector, embedding, retrieval, or
external-model call.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
REGISTER = ROOT / "prompts" / "wave_002_p0_authoring_prompt_register.md"
P1_AUDIT = ROOT / "review" / "wave_002_p1_literal_prompt_overlap_audit.json"
P2_MAIN_MANIFEST = ROOT / "review" / "wave_002" / "blind_review_response_manifest.json"
P2_MAIN_PACKETS = ROOT / "review" / "wave_002" / "packet_manifest.json"
P2_MAIN_CONSENSUS = ROOT / "review" / "wave_002" / "p2_acceptable_set_consensus.json"
P2_R1_MANIFEST = ROOT / "review" / "wave_002_r1" / "blind_review_response_manifest.json"
P2_R1_PACKETS = ROOT / "review" / "wave_002_r1" / "packet_manifest.json"
P2_R1_CONSENSUS = ROOT / "review" / "wave_002_r1" / "p2_acceptable_set_consensus.json"
P3_MAP = ROOT / "review" / "wave_002" / "P3_SOURCE_EVIDENCE_AND_RESIDUAL_MAP.md"
WAVE_ONE = ROOT / "manifest" / "wave_001_frozen_manifest.jsonl"
OUTPUT = ROOT / "manifest" / "wave_002_frozen_manifest.jsonl"
CERTIFICATE = ROOT / "manifest" / "wave_002_freeze_certificate.json"
REVISED_NUMBERS = {3, 11, 14}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def staged_inventory() -> dict[str, dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    manifests = sorted(ROOT.glob("staged_sources/*/source_expansion_manifest.jsonl"))
    if not manifests:
        raise ValueError("no staged Wave 002 source manifests found")
    for manifest in manifests:
        for row in load_jsonl(manifest):
            source_path = manifest.parent / "skills" / row["skill_id"] / "source" / "SKILL.original.md"
            previous = inventory.get(row["skill_id"])
            if previous and previous["source_sha256"] != row["source_sha256"]:
                raise ValueError(f"conflicting source SHA for {row['skill_id']}")
            inventory[row["skill_id"]] = {**row, "source_path": source_path}
    return inventory


def parse_register() -> dict[int, dict[str, str]]:
    text = REGISTER.read_text()
    sections = re.split(r"^## W2-(\d{3}): .*?$", text, flags=re.MULTILINE)
    records: dict[int, dict[str, str]] = {}
    for index in range(1, len(sections), 2):
        number = int(sections[index])
        body = sections[index + 1]
        primary = re.search(r"^- `authoring_primary_candidate`:\s*(?:\n\s*)?`([^`]+)`", body, re.MULTILINE)
        field = re.search(r"^- `tentative_primary_field`:\s*`([^`]+)`", body, re.MULTILINE)
        direct = re.search(r"^- Direct:\s*(.*?)(?=^- Paraphrase:)", body, re.MULTILINE | re.DOTALL)
        paraphrase = re.search(
            r"^- Paraphrase:\s*(.*?)(?=^## |^## Required Next Audit|\Z)", body, re.MULTILINE | re.DOTALL
        )
        if not primary or not field or not direct or not paraphrase:
            raise ValueError(f"unparseable W2-{number:03d} prompt block")
        records[number] = {
            "authoring_primary_candidate": primary.group(1),
            "primary_field": field.group(1),
            "direct_prompt": " ".join(direct.group(1).split()),
            "paraphrase_prompt": " ".join(paraphrase.group(1).split()),
        }
    if sorted(records) != list(range(1, 18)):
        raise ValueError("register must contain exactly W2-001 through W2-017")
    return records


def card_for(number: int) -> Path:
    cards = sorted(ROOT.glob(f"clusters/RQ1B-W2-DRAFT-{number:03d}-*/cluster_card.md"))
    if len(cards) != 1:
        raise ValueError(f"expected one card for W2-{number:03d}, found {len(cards)}")
    return cards[0]


def candidates_from_card(number: int) -> list[str]:
    text = card_for(number).read_text()
    match = re.search(r"- Candidate skills:\s*(.*?)(?=\n- Preserved originals)", text, re.DOTALL)
    if not match:
        raise ValueError(f"W2-{number:03d} missing candidate block")
    candidates = re.findall(r"`([^`]+)`", match.group(1))
    if len(candidates) != 2 or len(set(candidates)) != 2:
        raise ValueError(f"W2-{number:03d} must have two distinct candidates")
    return candidates


def current_p2_decision(
    number: int,
    response_manifest: dict[str, Any],
    packet_manifest: dict[str, Any],
    consensus: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    """Return current singleton candidate and concise evidence for a prompt pair."""
    suffix = f"C{number:03d}"
    packet = next((row for row in packet_manifest["packets"] if row["packet_id"].endswith(suffix)), None)
    if packet is None:
        raise ValueError(f"P2 packet missing for W2-{number:03d}")
    packet_id = packet["packet_id"]
    responses = response_manifest["reviewer_responses"]
    reviewed = [entry["responses"].get(packet_id) for entry in responses if packet_id in entry["responses"]]
    if len(reviewed) != 2:
        raise ValueError(f"{packet_id} does not have exactly two blind reviews")
    acceptable_sets = [record["acceptable_set"] for record in reviewed]
    if acceptable_sets[0] != acceptable_sets[1] or len(acceptable_sets[0]) != 1:
        raise ValueError(f"{packet_id} lacks agreed singleton acceptable set")
    artifact = acceptable_sets[0][0]
    if artifact not in {"A", "B"}:
        raise ValueError(f"{packet_id} has invalid accepted artifact {artifact}")
    candidate = packet["blind_candidate_order"][ord(artifact) - ord("A")]
    consensus_rows = [row for row in consensus["consensus"] if row["packet_id"] == packet_id]
    if len(consensus_rows) != 2 or any(
        not row["acceptable_set_agreement"]
        or row["adjudication_required"]
        or row["adjudicated_acceptable_set"] != [artifact]
        for row in consensus_rows
    ):
        raise ValueError(f"{packet_id} consensus record does not support both prompts")
    return candidate, {
        "status": "AGREED_SINGLETON",
        "review_method": response_manifest["review_method"],
        "response_manifest": str(P2_R1_MANIFEST if number in REVISED_NUMBERS else P2_MAIN_MANIFEST),
        "consensus": str(P2_R1_CONSENSUS if number in REVISED_NUMBERS else P2_MAIN_CONSENSUS),
        "revision": "R1" if number in REVISED_NUMBERS else "initial",
        "accepted_blind_artifact": artifact,
    }


def update_card_freeze_row(card: Path) -> None:
    text = card.read_text()
    old = "| Frozen final manifest | `NOT STARTED` | |"
    new = (
        "| Frozen final manifest | `P4 FROZEN ORIGINAL_ONLY` | "
        "`manifest/wave_002_frozen_manifest.jsonl`; no selector or masked comparison authorised. |"
    )
    if old in text:
        card.write_text(text.replace(old, new, 1))
    elif new not in text:
        raise ValueError(f"{card}: unexpected P4 row")


def main() -> None:
    register = parse_register()
    audit = load_json(P1_AUDIT)
    main_responses = load_json(P2_MAIN_MANIFEST)
    main_packets = load_json(P2_MAIN_PACKETS)
    main_consensus = load_json(P2_MAIN_CONSENSUS)
    r1_responses = load_json(P2_R1_MANIFEST)
    r1_packets = load_json(P2_R1_PACKETS)
    r1_consensus = load_json(P2_R1_CONSENSUS)
    source_map = P3_MAP.read_text()
    inventory = staged_inventory()
    wave_one_candidates = {
        candidate for row in load_jsonl(WAVE_ONE) for candidate in row["candidate_skill_ids"]
    }
    errors: list[str] = []

    if audit.get("cluster_count") != 17 or audit.get("prompt_count") != 34:
        errors.append("P1 audit does not cover 17 clusters / 34 prompts")
    for key in ("candidate_name_hit_count", "title_or_short_line_hit_count", "multi_token_phrase_hit_count"):
        if audit.get(key) != 0:
            errors.append(f"P1 audit {key} is nonzero")
    audited = {record["draft_number"]: record for record in audit.get("records", [])}
    if sorted(audited) != list(range(1, 18)):
        errors.append("P1 audit does not contain every W2 draft")
    if "P3 COMPLETE / 17 ORIGINAL_ONLY" not in source_map:
        errors.append("P3 source map is not a complete all-original-only decision")

    candidate_uses: Counter[str] = Counter()
    frozen_rows: list[dict[str, Any]] = []
    for number in range(1, 18):
        card = card_for(number)
        card_text = card.read_text()
        cluster_id = f"RQ1B-W2-DRAFT-{number:03d}"
        candidates = candidates_from_card(number)
        prompt = register[number]
        if "| Task-like prompt feasibility | `P1 PASS`" not in card_text:
            errors.append(f"{cluster_id}: P1 is not recorded as pass")
        expected_p2 = "`P2 AGREED SINGLETON (R1)`" if number in REVISED_NUMBERS else "`P2 AGREED SINGLETON`"
        if expected_p2 not in card_text:
            errors.append(f"{cluster_id}: current P2 disposition is missing")
        if "| Field-masking eligibility | `P3 ORIGINAL_ONLY`" not in card_text:
            errors.append(f"{cluster_id}: P3 original-only disposition is missing")
        if f"| C{number:03d} |" not in source_map:
            errors.append(f"{cluster_id}: missing P3 source-map row")
        if prompt["authoring_primary_candidate"] not in candidates:
            errors.append(f"{cluster_id}: authoring primary is not a candidate")

        audit_record = audited.get(number, {})
        by_name = {entry["prompt_name"]: entry for entry in audit_record.get("prompt_audit", [])}
        for prompt_name, text_key in (("direct", "direct_prompt"), ("paraphrase", "paraphrase_prompt")):
            audit_prompt = by_name.get(prompt_name, {})
            if audit_prompt.get("prompt") != prompt[text_key]:
                errors.append(f"{cluster_id}: P1 audit does not match final {prompt_name} prompt")
            if any(audit_prompt.get(key) for key in (
                "candidate_name_hits", "title_or_short_line_hits", "multi_token_phrase_hits"
            )):
                errors.append(f"{cluster_id}: final {prompt_name} has a P1 literal overlap")

        if number in REVISED_NUMBERS:
            accepted, evidence = current_p2_decision(number, r1_responses, r1_packets, r1_consensus)
        else:
            accepted, evidence = current_p2_decision(number, main_responses, main_packets, main_consensus)
        if accepted != prompt["authoring_primary_candidate"]:
            errors.append(f"{cluster_id}: P2 singleton disagrees with authoring primary")

        source_hashes: dict[str, str] = {}
        for candidate in candidates:
            candidate_uses[candidate] += 1
            source = inventory.get(candidate)
            if source is None:
                errors.append(f"{cluster_id}: candidate absent from staged inventory: {candidate}")
                continue
            source_path = source["source_path"]
            if not source_path.exists():
                errors.append(f"{cluster_id}: source does not exist: {source_path}")
                continue
            actual = sha256(source_path)
            if actual != source["source_sha256"]:
                errors.append(f"{cluster_id}: source hash mismatch: {candidate}")
            source_hashes[candidate] = actual

        frozen_rows.append({
            "cluster_id": cluster_id,
            "packet_id": f"wave_002-C{number:03d}" if number not in REVISED_NUMBERS else f"wave_002_r1-C{number:03d}",
            "draft_id": f"RQ1b Wave 002 Draft {number:03d}",
            "wave_id": "W2",
            "status": "VALID_CLUSTER_ORIGINAL_ONLY",
            "primary_field": prompt["primary_field"],
            "candidate_skill_ids": candidates,
            "acceptable_skill_ids": [accepted],
            "frozen_singleton_primary": accepted,
            "direct_prompt": prompt["direct_prompt"],
            "paraphrase_prompt": prompt["paraphrase_prompt"],
            "source_hashes": source_hashes,
            "acceptable_set_evidence": evidence,
            "masking_eligibility": "ORIGINAL_ONLY",
            "source_evidence_map": str(P3_MAP),
            "literal_overlap_audit": str(P1_AUDIT),
            "execution_scope": "NATURAL_ORIGINAL_ONLY_NO_RETRIEVAL_OR_EXTERNAL_TEXT_TRANSFER",
        })

    reused = sorted(candidate for candidate, count in candidate_uses.items() if count > 1)
    if reused:
        errors.append(f"candidate reuse within Wave 002: {', '.join(reused)}")
    cross_wave = sorted(set(candidate_uses) & wave_one_candidates)
    if cross_wave:
        errors.append(f"candidate overlap with Wave 001: {', '.join(cross_wave)}")
    if errors:
        raise SystemExit("freeze refused:\n- " + "\n- ".join(errors))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(canonical_json(row) + "\n" for row in frozen_rows))
    for number in range(1, 18):
        update_card_freeze_row(card_for(number))

    certificate = {
        "status": "RQ1B_WAVE_002_FROZEN_NOT_EXECUTED",
        "purpose": "Natural-original acceptable-set preparation only. This freeze permits neither retrieval nor a causal target-field mask comparison.",
        "wave_id": "W2",
        "cluster_count": len(frozen_rows),
        "prompt_count": 2 * len(frozen_rows),
        "unique_candidate_count": len(candidate_uses),
        "field_counts": dict(sorted(Counter(row["primary_field"] for row in frozen_rows).items())),
        "status_counts": dict(sorted(Counter(row["status"] for row in frozen_rows).items())),
        "candidate_reuse_within_wave_count": len(reused),
        "candidate_overlap_with_wave_001_count": len(cross_wave),
        "p1_final_literal_overlap_counts": {
            key: audit[key] for key in (
                "candidate_name_hit_count", "title_or_short_line_hit_count", "multi_token_phrase_hit_count"
            )
        },
        "p2_current_decisions": {
            "final_prompt_count": 34,
            "agreed_singleton_prompt_count": 34,
            "adjudication_required_count": 0,
            "initial_packet_count_retained": 14,
            "r1_packet_count_replacing_initial_prompts": 3,
            "model_assisted_curation_only": True,
        },
        "p3_masking_eligibility": "17 ORIGINAL_ONLY; no causal single-field inference is authorised.",
        "input_hashes": {
            str(path): sha256(path)
            for path in (
                REGISTER, P1_AUDIT, P2_MAIN_MANIFEST, P2_MAIN_PACKETS, P2_MAIN_CONSENSUS,
                P2_R1_MANIFEST, P2_R1_PACKETS, P2_R1_CONSENSUS, P3_MAP, WAVE_ONE,
            )
        },
        "frozen_manifest": str(OUTPUT),
        "frozen_manifest_sha256": sha256(OUTPUT),
        "execution_boundary": "No selector, embedding, retrieval, API call, or external text transfer has occurred.",
    }
    CERTIFICATE.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(certificate, indent=2))


if __name__ == "__main__":
    main()
