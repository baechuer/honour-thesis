#!/usr/bin/env python3
"""Materialise two source-grounded description overlays and blind-review packets."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
PROPOSAL = BASE / "review/description_remediation_proposals_terra_2026-08-31.json"
PROMPTS = BASE / "manifests/current_pre_freeze_consolidated_2026-08-31/admitted_prompt_manifest_current_pre_freeze.jsonl"
OUTPUT = BASE / "manifests/description_remediation_wave_001_pre_freeze_2026-08-31"
EXPECTED_PROMPTS = {
    "RQ2B-NC-RQ1-REAUTH-B002-R1-021-01",
    "RQ2B-NC-RQ1-REAUTH-B002-R1-021-02",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    proposals = list(proposal["proposals"])
    if len(proposals) != 2:
        raise SystemExit("Expected exactly two description proposals")

    overlay_rows: list[dict[str, Any]] = []
    by_hash: dict[str, dict[str, Any]] = {}
    for item in proposals:
        source_path = ROOT.parent / str(item["preserved_source_path"])
        source_hash = str(item["source_sha256"])
        if not source_path.is_file() or sha256_file(source_path) != source_hash:
            raise SystemExit(f"Source replay failed: {source_path}")
        source_text = source_path.read_text(encoding="utf-8")
        old_description = str(item["proposed_target"]["old_description"])
        if old_description != ">" or 'description: ">"' not in source_text:
            raise SystemExit(f"Expected literal placeholder description: {source_path}")
        new_description = str(item["proposed_target"]["new_description"]).strip()
        if not new_description or any(prompt_id in new_description for prompt_id in EXPECTED_PROMPTS):
            raise SystemExit(f"Invalid proposed description: {source_hash}")
        row = {
            "candidate_skill_id": item["candidate_skill_id"],
            "canonical_source_sha256": source_hash,
            "preserved_source_path": item["preserved_source_path"],
            "preserved_source_description": old_description,
            "final_library_description_overlay": new_description,
            "source_evidence": item["exact_source_evidence"],
            "leakage_audit": item["leakage_audit"],
            "overlay_scope": "FUTURE_RQ2B_NC_FINAL_REPRESENTATIONS_ONLY_DO_NOT_MUTATE_HISTORICAL_V3_OR_SOURCE_BYTES",
            "status": "SOURCE_GROUNDED_OVERLAY_PENDING_FRESH_TARGET_BLINDED_REVIEW",
        }
        overlay_rows.append(row)
        by_hash[source_hash] = row

    prompt_rows = [row for row in read_jsonl(PROMPTS) if str(row["prompt_id"]) in EXPECTED_PROMPTS]
    if len(prompt_rows) != 2 or {str(row["prompt_id"]) for row in prompt_rows} != EXPECTED_PROMPTS:
        raise SystemExit("Expected exact two-prompt remediation roster")
    packets: list[dict[str, Any]] = []
    for prompt in sorted(prompt_rows, key=lambda row: str(row["prompt_id"])):
        roster = [str(value) for value in prompt["candidate_source_sha256"]]
        if set(roster) != set(by_hash):
            raise SystemExit(f"Prompt overlay roster mismatch: {prompt['prompt_id']}")
        candidates = []
        for alias, source_hash in zip(["A", "B"], sorted(roster)):
            overlay = by_hash[source_hash]
            candidates.append({
                "alias": alias,
                "canonical_source_sha256": source_hash,
                "preserved_source_path": overlay["preserved_source_path"],
                "description_overlay": overlay["final_library_description_overlay"],
            })
        packets.append({
            "packet_id": f"RQ2B-NC-DESCRIPTION-REMEDIATION-{prompt['prompt_id']}",
            "prompt_id": prompt["prompt_id"],
            "cluster_id": prompt["cluster_id"],
            "prompt": prompt["prompt"],
            "candidates": candidates,
            "reviewer_instruction": (
                "The prior intended target and local reconciliation are withheld. Read both full preserved sources and "
                "their source-grounded description overlays. Classify each candidate as MOST_SUITABLE, FULLY_ACCEPTABLE, "
                "PARTIALLY_ADEQUATE, INADEQUATE, or UNCLEAR; identify description leakage, unsupported capability, input/output "
                "mismatch, and required composition. Do not consult selector output, metrics, prior labels, or results."
            ),
            "status": "TARGET_BLINDED_DESCRIPTION_REMEDIATION_REVIEW_INPUT_NOT_FINAL_GOLD",
        })

    OUTPUT.mkdir(parents=True, exist_ok=True)
    overlay_path = OUTPUT / "description_overlay.jsonl"
    packet_path = OUTPUT / "target_blinded_review_packets.jsonl"
    write_jsonl(overlay_path, sorted(overlay_rows, key=lambda row: row["candidate_skill_id"]))
    write_jsonl(packet_path, packets)
    summary = {
        "status": "PASS_DESCRIPTION_OVERLAY_MATERIALISATION_PENDING_BLIND_REVIEW_NOT_FINAL_REPRESENTATION",
        "overlay_source_count": len(overlay_rows),
        "review_prompt_count": len(packets),
        "input_sha256": {
            str(PROPOSAL.relative_to(ROOT)): sha256_file(PROPOSAL),
            str(PROMPTS.relative_to(ROOT)): sha256_file(PROMPTS),
        },
        "artifact_sha256": {
            overlay_path.name: sha256_file(overlay_path),
            packet_path.name: sha256_file(packet_path),
        },
        "claim_boundary": [
            "Historical V3 source bytes, prompts, representations, labels and results are unchanged.",
            "These overlays are eligible only for the future final-library representation build after fresh blind review.",
            "No final gold, acceptable set, selector output, metric or experiment is produced.",
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
