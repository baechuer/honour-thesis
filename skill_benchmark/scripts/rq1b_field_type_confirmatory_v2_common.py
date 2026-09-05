"""Shared local helpers for composition-keyed RQ1b v2 protocol tooling."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path


FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)
MATERIALISED_CARD_STATUSES = {
    "MATERIALISED_FROM_LITERAL_VALID_CARD",
    "MATERIALISED_FROM_LITERAL_SAFE_SURFACE_CUE_REPAIR",
    "MATERIALISED_FROM_FROZEN_CANONICAL_CARD",
}

DISPLAY_NAMES = {
    "use_condition": "Use condition",
    "input_precondition": "Input / precondition",
    "output_artifact": "Output artifact",
    "workflow_procedure": "Workflow / procedure",
    "success_verification": "Success / verification",
    "boundary_not_for": "Boundary / not for",
    "dependency_resource": "Dependency / resource",
}


def load_json(path: Path):
    return json.loads(path.read_text())


def load_object(path: Path) -> dict:
    value = load_json(path)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def load_list(path: Path) -> list:
    value = load_json(path)
    if not isinstance(value, list):
        raise ValueError(f"JSON array required: {path}")
    return value


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_digest(value: object) -> str:
    """Match the frozen v2 ledger's sorted default-json hash definition."""
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def opaque_packet_id(namespace: str, private_id: str, canonical_card_sha256: str) -> str:
    digest = hashlib.sha256(
        f"rq1b-field-type-v2:{namespace}:{private_id}:{canonical_card_sha256}".encode()
    ).hexdigest()[:20]
    return f"{namespace.upper()}-{digest}"


def validate_card(cards: dict, context: str) -> None:
    if not isinstance(cards, dict) or not cards:
        raise ValueError(f"cards missing: {context}")
    for label, card in cards.items():
        if not isinstance(label, str) or not isinstance(card, dict) or set(card) != set(FIELDS):
            raise ValueError(f"card schema invalid: {context}:{label}")
        for field in FIELDS:
            cell = card[field]
            if not isinstance(cell, dict) or set(cell) != {"status", "quotes"}:
                raise ValueError(f"cell schema invalid: {context}:{label}:{field}")
            if cell["status"] not in {"EVIDENCE", "NOT_STATED"}:
                raise ValueError(f"cell status invalid: {context}:{label}:{field}")
            if not isinstance(cell["quotes"], list) or any(
                not isinstance(quote, str) or not quote for quote in cell["quotes"]
            ):
                raise ValueError(f"cell quotes invalid: {context}:{label}:{field}")
            if cell["status"] == "EVIDENCE" and not cell["quotes"]:
                raise ValueError(f"evidence missing quote: {context}:{label}:{field}")
            if cell["status"] == "NOT_STATED" and cell["quotes"]:
                raise ValueError(f"not-stated has quotes: {context}:{label}:{field}")


def card_surface_cue_violations(cards: dict) -> list[str]:
    """Return only source-locating cues prohibited in blinded card excerpts.

    Product/domain names remain valid operational content. This deliberately
    targets surface artifacts that identify a source skill or repository rather
    than the operation: URLs, markdown link targets, local artifact links, and
    copied markdown heading blocks.
    """
    violations = []
    for label, card in cards.items():
        for field, cell in card.items():
            for quote_index, quote in enumerate(cell["quotes"]):
                location = f"{label}:{field}:{quote_index}"
                if re.search(r"(?:https?://|ftp://|www\.)", quote, flags=re.IGNORECASE):
                    violations.append(f"url:{location}")
                if re.search(r"\[[^\]\n]+\]\([^\)\n]+\)", quote):
                    violations.append(f"markdown_link_target:{location}")
                if re.search(r"(?:^|\n)\s*(?:#{1,6}|[-*+]\s+#{1,6})\s+\S", quote):
                    violations.append(f"markdown_heading_block:{location}")
                if re.search(r"(?:^|[\s`])(?:SKILL|README)\.md(?:$|[\s`?/#)])", quote, flags=re.IGNORECASE):
                    violations.append(f"skill_or_readme_artifact:{location}")
    return violations


def render_card(card: dict) -> str:
    lines: list[str] = []
    for field in FIELDS:
        cell = card[field]
        lines.append(f"{DISPLAY_NAMES[field]}:")
        lines.extend(cell["quotes"] if cell["status"] == "EVIDENCE" else ["NOT_STATED"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def rendered_packet_field_sections(rendered: str) -> dict[str, str]:
    """Return only source-derived field content, excluding generated headings."""
    if not isinstance(rendered, str):
        raise ValueError("rendered field card must be a string")
    sections = {}
    positions = []
    for field in FIELDS:
        marker = f"{DISPLAY_NAMES[field]}:"
        position = rendered.find(marker)
        if position < 0:
            raise ValueError(f"rendered field heading missing: {field}")
        positions.append((field, position, len(marker)))
    if [position for _, position, _ in positions] != sorted(position for _, position, _ in positions):
        raise ValueError("rendered field headings out of order")
    for index, (field, position, marker_length) in enumerate(positions):
        start = position + marker_length
        end = positions[index + 1][1] if index + 1 < len(positions) else len(rendered)
        sections[field] = rendered[start:end]
    return sections


def usable_exact_packet_evidence(quote: object, sections: dict[str, str]) -> bool:
    """Reject generated formatting and require nonempty source-card content."""
    if not isinstance(quote, str) or not quote or not quote.strip() or quote.strip() == "NOT_STATED":
        return False
    return any(
        content.strip() != "NOT_STATED" and quote in content
        for content in sections.values()
    )


def canonical_entries(root: Path) -> dict[str, dict]:
    ledger = load_object(root / "canonicalisation_ledger.json")
    entries = ledger.get("compositions")
    if not isinstance(entries, list):
        raise ValueError("composition ledger missing compositions list")
    by_id = {}
    for entry in entries:
        composition_id = entry.get("composition_id") if isinstance(entry, dict) else None
        if not isinstance(composition_id, str) or composition_id in by_id:
            raise ValueError("invalid or duplicate composition ledger entry")
        by_id[composition_id] = entry
    return by_id


def materialised_composition_ids(root: Path) -> set[str]:
    return {
        composition_id
        for composition_id, entry in canonical_entries(root).items()
        if entry.get("status") in MATERIALISED_CARD_STATUSES
    }


def composition_rows(root: Path) -> dict[str, dict]:
    rows = load_list(root / "composition_manifest_private.json")
    by_id = {}
    for row in rows:
        composition_id = row.get("composition_id") if isinstance(row, dict) else None
        if not isinstance(composition_id, str) or composition_id in by_id:
            raise ValueError("invalid or duplicate private composition row")
        candidates = row.get("private_candidates")
        if not isinstance(candidates, list) or len(candidates) not in {3, 4}:
            raise ValueError(f"candidate count invalid: {composition_id}")
        labels = [candidate.get("label") for candidate in candidates if isinstance(candidate, dict)]
        if len(labels) != len(candidates) or len(set(labels)) != len(labels):
            raise ValueError(f"candidate labels invalid: {composition_id}")
        by_id[composition_id] = row
    return by_id


def routing_family_rows(root: Path) -> dict[str, dict]:
    rows = load_list(root / "routing_family_manifest_private.json")
    by_id = {}
    for row in rows:
        family_id = row.get("routing_family_id") if isinstance(row, dict) else None
        if not isinstance(family_id, str) or family_id in by_id:
            raise ValueError("invalid or duplicate private routing-family row")
        prompts = row.get("prompt_lineage")
        if not isinstance(prompts, list):
            raise ValueError(f"prompt lineage missing: {family_id}")
        variants = {item.get("prompt_variant") for item in prompts if isinstance(item, dict)}
        if variants != {"direct", "paraphrase"} or len(prompts) != 2:
            raise ValueError(f"direct/paraphrase pair invalid: {family_id}")
        if any(not isinstance(item.get("prompt"), str) or not item["prompt"].strip() for item in prompts):
            raise ValueError(f"prompt text missing: {family_id}")
        by_id[family_id] = row
    return by_id


def canonical_cards(root: Path, composition_id: str) -> dict:
    path = root / "canonical_cards" / f"{composition_id}.json"
    payload = load_object(path)
    if payload.get("composition_id") != composition_id:
        raise ValueError(f"canonical composition_id mismatch: {composition_id}")
    if payload.get("status") != "RQ1B_FIELD_TYPE_ABLATION_V2_CANONICAL_SOURCE_CARD_NOT_A_RESULT":
        raise ValueError(f"canonical status mismatch: {composition_id}")
    if tuple(payload.get("field_order", [])) != FIELDS:
        raise ValueError(f"canonical field order mismatch: {composition_id}")
    entry = canonical_entries(root).get(composition_id)
    if entry is None or entry.get("status") not in MATERIALISED_CARD_STATUSES:
        raise ValueError(f"canonical entry unavailable: {composition_id}")
    if entry.get("canonical_card_sha256") != canonical_json_digest(payload):
        raise ValueError(f"canonical hash mismatch: {composition_id}")
    cards = payload.get("cards")
    validate_card(cards, composition_id)
    return cards


def label_for_skill(composition: dict, skill_id: str) -> str:
    labels = {
        candidate.get("skill_id"): candidate.get("label")
        for candidate in composition["private_candidates"]
    }
    label = labels.get(skill_id)
    if not isinstance(label, str):
        raise ValueError("strict gold absent from private composition")
    return label


def cell_signature(cell: dict) -> str:
    return json.dumps({"status": cell["status"], "quotes": cell["quotes"]}, sort_keys=True)
