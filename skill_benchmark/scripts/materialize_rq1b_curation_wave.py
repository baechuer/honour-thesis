#!/usr/bin/env python3
"""Materialise auditable local packets for an RQ1b curation wave.

This tool does not score skills, call models, select labels, or make a
cluster valid. It creates two views of a reviewed candidate list:

* an authoring packet with provenance and source texts for evidence mapping;
* a blinded review packet containing only the task prompt and candidate texts.

The separation prevents the reviewer from seeing a declared field, source
family, intended candidate, or any retrieval output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
INVENTORY_PATH = ROOT / "manifest" / "source_inventory.jsonl"
DRAFT_AUDIT_PATH = ROOT / "manifest" / "draft_pool_audit.json"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_inventory() -> dict[str, dict[str, Any]]:
    return {row["skill_id"]: row for row in load_jsonl(INVENTORY_PATH)}


def load_drafts() -> dict[int, dict[str, Any]]:
    audit = json.loads(DRAFT_AUDIT_PATH.read_text())
    drafts: dict[int, dict[str, Any]] = {}
    for card in audit["cards"]:
        try:
            number = int(card["id"].split()[-1])
        except (AttributeError, TypeError, ValueError) as error:
            raise ValueError(f"unparseable draft identity: {card.get('id')!r}") from error
        drafts[number] = card
    return drafts


def enrich_record(record: dict[str, Any], drafts: dict[int, dict[str, Any]]) -> dict[str, Any]:
    """Expand a concise, source-screened selection record from the audit."""
    if "draft_number" not in record:
        return record
    try:
        number = int(record["draft_number"])
    except (TypeError, ValueError) as error:
        raise ValueError(f"invalid draft_number: {record.get('draft_number')!r}") from error
    draft = drafts.get(number)
    if draft is None:
        raise ValueError(f"unknown draft_number: {number}")
    status = draft.get("status", "")
    if "SOURCE SCREENING PASSED" not in status:
        raise ValueError(f"draft {number:03d} is not source-screened: {status}")
    expanded = dict(record)
    expanded.pop("draft_number")
    expanded.update({
        "cluster_id": f"RQ1B-W001-{number:03d}",
        "draft_id": draft["id"],
        "primary_field": draft["primary_field"],
        "candidate_skill_ids": draft["candidates"],
    })
    return expanded


def validate_record(record: dict[str, Any], inventory: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    required = {
        "cluster_id",
        "draft_id",
        "primary_field",
        "candidate_skill_ids",
        "source_evidence_status",
        "direct_prompt",
        "paraphrase_prompt",
        "authoring_primary_candidate",
        "masking_eligibility",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append(f"missing keys: {', '.join(missing)}")
        return errors

    candidates = record["candidate_skill_ids"]
    if not isinstance(candidates, list) or not 2 <= len(candidates) <= 4:
        errors.append("candidate_skill_ids must contain two to four skills")
    if len(set(candidates)) != len(candidates):
        errors.append("candidate_skill_ids contains a duplicate")
    if record["authoring_primary_candidate"] not in candidates:
        errors.append("authoring_primary_candidate must be a candidate")
    for prompt_key in ("direct_prompt", "paraphrase_prompt"):
        prompt = record[prompt_key]
        if not isinstance(prompt, str) or len(prompt.split()) < 8:
            errors.append(f"{prompt_key} must be a task-like prompt of at least eight words")
    for candidate in candidates:
        source = inventory.get(candidate)
        if source is None:
            errors.append(f"unknown candidate in inventory: {candidate}")
            continue
        source_path = Path(source["source_path"])
        if not source_path.exists():
            errors.append(f"missing source file: {source_path}")
        elif sha256(source_path) != source["source_sha256"]:
            errors.append(f"source hash changed: {candidate}")
    return errors


def render_source(record: dict[str, Any], inventory: dict[str, dict[str, Any]]) -> str:
    chunks = []
    for candidate in record["candidate_skill_ids"]:
        source = inventory[candidate]
        path = Path(source["source_path"])
        chunks.append(
            "\n".join(
                [
                    f"## Candidate: {candidate}",
                    f"Source path: `{path}`",
                    f"SHA-256: `{source['source_sha256']}`",
                    "",
                    path.read_text().rstrip(),
                ]
            )
        )
    return "\n\n---\n\n".join(chunks)


def write_packets(selection: dict[str, Any], selection_path: Path) -> None:
    inventory = load_inventory()
    drafts = load_drafts()
    records = [enrich_record(record, drafts) for record in selection.get("records", [])]
    if not isinstance(records, list) or not records:
        raise ValueError("selection must contain a non-empty records array")

    all_errors: list[str] = []
    usage: dict[str, list[str]] = {}
    for record in records:
        record_errors = validate_record(record, inventory)
        all_errors.extend(f"{record.get('cluster_id', '<missing>')}: {error}" for error in record_errors)
        for candidate in record.get("candidate_skill_ids", []):
            usage.setdefault(candidate, []).append(record.get("cluster_id", "<missing>"))
    reused = {candidate: ids for candidate, ids in usage.items() if len(ids) > 1}
    if reused:
        all_errors.extend(
            f"candidate reused across wave: {candidate} -> {', '.join(ids)}"
            for candidate, ids in sorted(reused.items())
        )
    if all_errors:
        raise ValueError("\n".join(all_errors))

    wave_id = selection.get("wave_id", selection_path.stem)
    output_dir = ROOT / "review" / wave_id
    authoring_dir = output_dir / "authoring_packets"
    blind_dir = output_dir / "blind_packets"
    authoring_dir.mkdir(parents=True, exist_ok=True)
    blind_dir.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    for index, record in enumerate(records, start=1):
        packet_id = f"{wave_id}-C{index:03d}"
        metadata = {
            "packet_id": packet_id,
            "cluster_id": record["cluster_id"],
            "draft_id": record["draft_id"],
            "primary_field": record["primary_field"],
            "candidate_skill_ids": record["candidate_skill_ids"],
            "source_evidence_status": record["source_evidence_status"],
            "masking_eligibility": record["masking_eligibility"],
            "authoring_primary_candidate": record["authoring_primary_candidate"],
            "source_hashes": {
                candidate: inventory[candidate]["source_sha256"]
                for candidate in record["candidate_skill_ids"]
            },
        }
        authoring = "\n".join(
            [
                f"# {packet_id} Authoring Packet",
                "",
                "Status: `CURATION ONLY / NOT A VALID CLUSTER / NO RETRIEVAL`",
                "",
                "## Private Curation Metadata",
                "",
                "```json",
                json.dumps(metadata, indent=2),
                "```",
                "",
                "## Proposed Task Prompts",
                "",
                f"- Direct: {record['direct_prompt']}",
                f"- Independently phrased: {record['paraphrase_prompt']}",
                "",
                "## Original Sources",
                "",
                render_source(record, inventory),
                "",
            ]
        )
        blind = "\n".join(
            [
                f"# {packet_id} Blinded Acceptability Packet",
                "",
                "Status: `REVIEW MATERIAL / NO DECLARED FIELD OR INTENDED LABEL`",
                "",
                "## Task A",
                "",
                record["direct_prompt"],
                "",
                "## Task B",
                "",
                record["paraphrase_prompt"],
                "",
                "## Candidate Artifacts",
                "",
                render_source(record, inventory),
                "",
                "## Reviewer Response",
                "",
                "For each task and candidate, assign exactly one: `acceptable`, "
                "`plausible_but_insufficient`, or `not_acceptable`. Explain any "
                "material ambiguity in one sentence. Do not infer a declared target field.",
                "",
            ]
        )
        (authoring_dir / f"{packet_id}.md").write_text(authoring)
        (blind_dir / f"{packet_id}.md").write_text(blind)
        manifest_rows.append(metadata)

    summary = {
        "status": "CURATION_PACKETS_MATERIALISED_NOT_REVIEWED_NOT_VALID",
        "wave_id": wave_id,
        "selection_path": str(selection_path),
        "cluster_count": len(records),
        "candidate_skill_count": len(usage),
        "candidate_reuse_count": len(reused),
        "external_calls": 0,
        "retrieval_runs": 0,
        "packets": manifest_rows,
    }
    (output_dir / "packet_manifest.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({
        "wave_id": wave_id,
        "cluster_count": len(records),
        "candidate_skill_count": len(usage),
        "candidate_reuse_count": len(reused),
        "output_dir": str(output_dir),
    }, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("selection", type=Path)
    args = parser.parse_args()
    write_packets(json.loads(args.selection.read_text()), args.selection)


if __name__ == "__main__":
    main()
