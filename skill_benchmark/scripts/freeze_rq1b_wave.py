#!/usr/bin/env python3
"""Freeze a fully curated RQ1b natural-original wave without scoring it.

This validator joins local source hashes, the authoring prompt packet, the
literal-overlap audit, model-assisted blind acceptable-set outcome, and the
source/residual decision. It deliberately has no selector, embedding, model,
network, or masking implementation. A frozen ``ORIGINAL_ONLY`` entry is valid
for natural-original selection only, never for a causal mask delta.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/rq1b_naturalistic_public_replication")
INVENTORY_PATH = ROOT / "manifest" / "source_inventory.jsonl"
AUDIT_PATH = ROOT / "manifest" / "draft_pool_audit.json"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def resolve_selection(selection: dict[str, Any]) -> list[dict[str, Any]]:
    audit = json.loads(AUDIT_PATH.read_text())
    drafts = {int(card["id"].split()[-1]): card for card in audit["cards"]}
    rows: list[dict[str, Any]] = []
    for raw in selection["records"]:
        number = int(raw["draft_number"])
        draft = drafts[number]
        rows.append({
            "draft_number": number,
            "cluster_id": f"RQ1B-W001-{number:03d}",
            "draft_id": draft["id"],
            "primary_field": draft["primary_field"],
            "candidate_skill_ids": draft["candidates"],
            "direct_prompt": raw["direct_prompt"],
            "paraphrase_prompt": raw["paraphrase_prompt"],
            "authoring_primary_candidate": raw["authoring_primary_candidate"],
        })
    return rows


def normalise_candidates(value: str) -> set[str]:
    """Read one candidate-status cell from a recovered Markdown response."""
    value = value.strip().replace("`", "").replace("<br>", ",")
    if value in {"", "None", "-", "--", "---", "—"}:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def load_blind_rows(response_manifest_path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """Load raw response tables retained from the six blinded local reviewers."""
    response_manifest = json.loads(response_manifest_path.read_text())
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for record in response_manifest["reviewers"]:
        reviewer = record["reviewer"]
        response_path = Path(record["recovered_response_path"])
        if not response_path.exists() or file_hash(response_path) != record["recovered_response_sha256"]:
            raise ValueError(f"blind response integrity failed for {reviewer}")
        for line in response_path.read_text().splitlines():
            if not line.startswith("| C"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 6:
                continue
            packet_short, task_cell, accepted, plausible, not_accepted, note = cells
            packet_match = re.fullmatch(r"C(\d{3})", packet_short)
            if packet_match is None:
                continue
            task = "A" if task_cell.lower().endswith("a") else "B" if task_cell.lower().endswith("b") else None
            if task is None:
                raise ValueError(f"{reviewer} has unparseable task cell {task_cell!r}")
            key = (reviewer, f"wave_001-C{packet_match.group(1)}-{task}")
            if key in rows:
                raise ValueError(f"duplicate blind response row: {key}")
            rows[key] = {
                "acceptable": normalise_candidates(accepted),
                "plausible_but_insufficient": normalise_candidates(plausible),
                "not_acceptable": normalise_candidates(not_accepted),
                "note": note,
            }
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--packet-manifest", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--overlap-audit", type=Path, required=True)
    parser.add_argument("--source-map", type=Path, required=True)
    parser.add_argument("--blind-response-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    args = parser.parse_args()

    selection = json.loads(args.selection.read_text())
    packet_manifest = json.loads(args.packet_manifest.read_text())
    decisions = json.loads(args.decisions.read_text())
    overlap = json.loads(args.overlap_audit.read_text())
    source_map = args.source_map.read_text()
    blind_rows = load_blind_rows(args.blind_response_manifest)
    inventory = {row["skill_id"]: row for row in load_jsonl(INVENTORY_PATH)}
    selected = resolve_selection(selection)
    packets = {row["packet_id"]: row for row in packet_manifest["packets"]}
    decision_by_packet = {row["packet_id"]: row for row in decisions["records"]}
    expected_packet_ids = [f"wave_001-C{index:03d}" for index in range(1, len(selected) + 1)]

    errors: list[str] = []
    if len(selected) < 50:
        errors.append(f"requires at least 50 clusters, found {len(selected)}")
    if len(expected_packet_ids) != len(set(expected_packet_ids)):
        errors.append("duplicate generated packet ids")
    if set(packets) != set(expected_packet_ids):
        errors.append("packet manifest does not exactly cover selection")
    if set(decision_by_packet) != set(expected_packet_ids):
        errors.append("decision ledger does not exactly cover selection")
    if overlap.get("cluster_count") != len(selected):
        errors.append("overlap audit cluster count differs from selection")
    if overlap.get("candidate_name_hit_count") != 0:
        errors.append("candidate name occurs in at least one prompt")
    if overlap.get("multi_token_phrase_hit_count") != 0:
        errors.append("three- or four-token source phrase occurs in at least one prompt")

    candidate_uses: Counter[str] = Counter()
    frozen_rows: list[dict[str, Any]] = []
    for index, row in enumerate(selected, start=1):
        packet_id = f"wave_001-C{index:03d}"
        packet = packets.get(packet_id, {})
        decision = decision_by_packet.get(packet_id, {})
        if packet.get("cluster_id") != row["cluster_id"]:
            errors.append(f"{packet_id}: cluster identity mismatch")
        if packet.get("candidate_skill_ids") != row["candidate_skill_ids"]:
            errors.append(f"{packet_id}: candidate identity mismatch")
        if packet.get("authoring_primary_candidate") != row["authoring_primary_candidate"]:
            errors.append(f"{packet_id}: authoring primary mismatch")
        if decision.get("acceptable_set_status") != "AGREED_SINGLETON":
            errors.append(f"{packet_id}: no agreed singleton acceptable set")
        if decision.get("masking_eligibility") not in {"ORIGINAL_ONLY", "MASK_ELIGIBLE"}:
            errors.append(f"{packet_id}: invalid masking decision")
        if f"| C{index:03d} |" not in source_map:
            errors.append(f"{packet_id}: missing exact source-map row")

        reviewer_pair = ("A1", "B1") if index <= 21 else ("A2", "B2") if index <= 42 else ("A3", "B3")
        for task in ("A", "B"):
            reviewed = [blind_rows.get((reviewer, f"{packet_id}-{task}")) for reviewer in reviewer_pair]
            if any(item is None for item in reviewed):
                errors.append(f"{packet_id}: missing {task} response from reviewer pair {reviewer_pair}")
                continue
            first, second = reviewed
            if not first["note"] or not second["note"]:
                errors.append(f"{packet_id}: missing reviewer note for task {task}")
            if first["acceptable"] != second["acceptable"]:
                errors.append(f"{packet_id}: reviewers disagree on acceptable set for task {task}")
            if first["acceptable"] != {row["authoring_primary_candidate"]}:
                errors.append(f"{packet_id}: task {task} does not support singleton authoring primary")
            for item in reviewed:
                partition = item["acceptable"] | item["plausible_but_insufficient"] | item["not_acceptable"]
                if partition != set(row["candidate_skill_ids"]):
                    errors.append(f"{packet_id}: task {task} reviewer labels do not partition candidates")
                if (item["acceptable"] & item["plausible_but_insufficient"]
                        or item["acceptable"] & item["not_acceptable"]
                        or item["plausible_but_insufficient"] & item["not_acceptable"]):
                    errors.append(f"{packet_id}: task {task} reviewer labels overlap")

        source_hashes: dict[str, str] = {}
        for candidate in row["candidate_skill_ids"]:
            candidate_uses[candidate] += 1
            source = inventory.get(candidate)
            if source is None:
                errors.append(f"{packet_id}: unknown candidate {candidate}")
                continue
            source_path = Path(source["source_path"])
            if not source_path.exists():
                errors.append(f"{packet_id}: source missing {source_path}")
                continue
            actual = file_hash(source_path)
            if actual != source["source_sha256"]:
                errors.append(f"{packet_id}: source hash mismatch for {candidate}")
            if packet.get("source_hashes", {}).get(candidate) != actual:
                errors.append(f"{packet_id}: packet source hash mismatch for {candidate}")
            source_hashes[candidate] = actual

        mask = decision.get("masking_eligibility")
        frozen_rows.append({
            "cluster_id": row["cluster_id"],
            "packet_id": packet_id,
            "draft_id": row["draft_id"],
            "status": "VALID_CLUSTER_MASK_ELIGIBLE" if mask == "MASK_ELIGIBLE" else "VALID_CLUSTER_ORIGINAL_ONLY",
            "primary_field": row["primary_field"],
            "candidate_skill_ids": row["candidate_skill_ids"],
            "acceptable_skill_ids": [row["authoring_primary_candidate"]],
            "frozen_singleton_primary": row["authoring_primary_candidate"],
            "direct_prompt": row["direct_prompt"],
            "paraphrase_prompt": row["paraphrase_prompt"],
            "source_hashes": source_hashes,
            "acceptable_set_evidence": {
                "status": "AGREED_SINGLETON",
                "review_method": decisions["review_method"],
            "review_summary": decisions["review_summary"],
            "raw_response_manifest": str(args.blind_response_manifest),
            },
            "masking_eligibility": mask,
            "source_evidence_map": decisions["source_evidence_map"],
            "literal_overlap_audit": decisions["prompt_overlap_audit"],
            "execution_scope": "NATURAL_ORIGINAL_ONLY_NO_RETRIEVAL_OR_EXTERNAL_TEXT_TRANSFER",
        })

    reused = sorted(candidate for candidate, count in candidate_uses.items() if count > 1)
    if reused:
        errors.append(f"candidate reused across frozen clusters: {', '.join(reused)}")
    if errors:
        raise SystemExit("freeze refused:\n- " + "\n- ".join(errors))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(canonical_json(row) + "\n" for row in frozen_rows))
    field_counts = Counter(row["primary_field"] for row in frozen_rows)
    status_counts = Counter(row["status"] for row in frozen_rows)
    certificate = {
        "status": "RQ1B_WAVE_001_FROZEN_NOT_EXECUTED",
        "purpose": "Natural-original RQ1b selection preparation only; no causal masked comparison is authorised by this freeze.",
        "cluster_count": len(frozen_rows),
        "unique_candidate_count": len(candidate_uses),
        "field_counts": dict(sorted(field_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "literal_overlap_summary": {
            "candidate_name_hit_count": overlap["candidate_name_hit_count"],
            "multi_token_phrase_hit_count": overlap["multi_token_phrase_hit_count"],
            "title_or_short_line_hit_count": overlap["title_or_short_line_hit_count"],
            "manual_disposition": "short generic-heading or operational-term hits are retained as audit evidence; no candidate name or multi-token source phrase is copied",
        },
        "input_hashes": {
            "selection": file_hash(args.selection),
            "packet_manifest": file_hash(args.packet_manifest),
            "decisions": file_hash(args.decisions),
            "overlap_audit": file_hash(args.overlap_audit),
            "source_evidence_map": file_hash(args.source_map),
            "blind_response_manifest": file_hash(args.blind_response_manifest),
        },
        "frozen_manifest": str(args.output),
        "frozen_manifest_sha256": file_hash(args.output),
        "execution_boundary": "No retrieval, embeddings, external API calls, or text transmission have occurred.",
    }
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(certificate, indent=2))


if __name__ == "__main__":
    main()
