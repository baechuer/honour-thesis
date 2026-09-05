#!/usr/bin/env python3
"""Build the v1.1 B1R source-text-transfer approval packet without transfer.

The strict-gold v1.1 overlay changes which prompts are scored, not the frozen
2,433-skill source corpus. Its I3C extraction therefore reuses the parent
version's exact 57 hash-bound inputs and output destinations while recording
the v1.1 local strict-contract seal as the downstream consumer boundary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_rq2b_i3c_transfer_packet import verify as verify_parent_i3c_packet
from rq2b_common import (
    b1r_chunk_inventory,
    b1r_scope_for_extraction,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_json,
    write_json_new,
)
from rq2b_v11_contract import RELATIVE_ROOT, VERSION_ID, verify as verify_v11_contract
from build_rq2b_v11_implementation_seal import SEAL_NAME, verify as verify_v11_seal


PARENT_VERSION = "rq2b-full-library-v1-2026-08-02"
PARENT_ROOT = f"skill_benchmark/rq2b_full_library/{PARENT_VERSION}"
PACKET_NAME = "b1r_v11_authorisation_packet.json"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"v1.1 B1R artifact is not an object: {path}")
    return value


def source_scope(extraction: dict[str, Any]) -> dict[str, Any]:
    """Re-express the shared parent corpus scope under the v1.1 scoring overlay."""
    parent = b1r_scope_for_extraction(extraction)
    return {
        "stage": "B1R",
        "version_id": VERSION_ID,
        "source_corpus_parent_version": PARENT_VERSION,
        "destination": parent["destination"],
        "purpose": "I3C extraction for the shared frozen 2,433-skill corpus; v1.1 will score only its strict 381-prompt overlay after QA",
        "texts": parent["texts"],
        "source_utf8_bytes": parent["source_utf8_bytes"],
        "local_qwen_proxy_tokens": parent["local_qwen_proxy_tokens"],
        "chunks": parent["chunks"],
        "maximum_replacement_assignments": parent["maximum_replacement_assignments"],
        "maximum_total_assignment_attempts": parent["maximum_total_assignment_attempts"],
        "maximum_assigned_source_rows": parent["maximum_assigned_source_rows"],
        "maximum_assigned_source_utf8_bytes": parent["maximum_assigned_source_utf8_bytes"],
        "maximum_assigned_qwen_proxy_tokens": parent["maximum_assigned_qwen_proxy_tokens"],
        "maximum_active_workers": parent["maximum_active_workers"],
        "worker_reasoning": parent["worker_reasoning"],
        "flush_every_completed_rows": parent["flush_every_completed_rows"],
        "authorises": parent["authorises"],
        "does_not_authorise": parent["does_not_authorise"],
    }


def build(root: Path) -> dict[str, Any]:
    root = root.resolve()
    v11 = root / RELATIVE_ROOT
    verify_v11_contract(root)
    strict_seal = verify_v11_seal(root)
    extraction = verify_parent_i3c_packet(root)
    require(extraction.get("state") == "built_not_transmitted", "Parent I3C packet is not awaiting transfer")
    require(extraction.get("external_texts_transmitted") == 0, "Parent I3C packet records prior transfer")
    require(extraction.get("worker_count") == 0, "Parent I3C packet records prior workers")
    require(extraction.get("counts", {}).get("input_rows") == 2433, "Parent I3C packet source count drift")
    require(extraction.get("counts", {}).get("chunks") == 57, "Parent I3C packet chunk count drift")

    materialization = read_json(v11 / "materialization_report.json")
    require(materialization.get("parent_version") == PARENT_VERSION, "v1.1 parent version drift")
    require(materialization.get("evaluation_scope") == "strict_gold_only", "v1.1 is not strict-only")
    packet_path = v11 / PACKET_NAME
    require(not packet_path.exists(), f"Refusing to overwrite v1.1 B1R packet: {packet_path}")

    scope = source_scope(extraction)
    chunks = b1r_chunk_inventory(extraction)
    packet = {
        "schema_version": "rq2b-v11-b1r-authorisation-packet-v1",
        "version_id": VERSION_ID,
        "state": "awaiting_explicit_v11_b1r_source_transfer_approval",
        "network_calls": 0,
        "external_texts_transmitted": 0,
        "workers_started": 0,
        "scope": scope,
        "scope_sha256": sha256_json(scope),
        "v11_strict_contract_seal": {
            "path": relative(v11 / SEAL_NAME, root),
            "sha256": sha256_file(v11 / SEAL_NAME),
            "state": strict_seal["state"],
        },
        "parent_i3c_source_packet": {
            "parent_version": PARENT_VERSION,
            "manifest_path": f"{PARENT_ROOT}/i3c_extraction/manifest.json",
            "manifest_sha256": sha256_file(root / PARENT_ROOT / "i3c_extraction" / "manifest.json"),
            "shared_corpus_skills": extraction["counts"]["input_rows"],
            "shared_corpus_chunks": extraction["counts"]["chunks"],
        },
        "v11_scoring_boundary": {
            "strict_gold_only": True,
            "scored_prompts": 381,
            "controlled_scored_prompts": 243,
            "public_gold_scored_prompts": 138,
            "stress_prompts_not_in_accuracy": 12,
            "i3c_outputs_are_not_a_retrieval_result": True,
        },
        "extraction_prompt": extraction["extraction_prompt"],
        "chunks": chunks,
        "execution_requirements": {
            "use_only_assigned_input_artifact_text": True,
            "read_frozen_extraction_prompt": True,
            "one_json_object_per_input_row": True,
            "flush_every_completed_rows": 10,
            "validate_jsonl_row_identity_and_exact_evidence": True,
            "record_hash_bound_worker_event_per_explicit_assignment": True,
            "close_completed_or_failed_workers": True,
            "no_duplicate_active_assignments": True,
            "stop_on_hash_or_identity_failure": True,
            "no_automatic_retries": True,
            "replacement_assignments_must_be_explicit_and_event_logged": True,
            "maximum_active_workers": 6,
        },
        "worker_event_ledger": {
            "path": f"{PARENT_ROOT}/i3c_extraction/worker_events.jsonl",
            "schema_version": "rq2b-i3c-worker-event-v1",
            "record_failed_replacements": True,
            "count_repeated_assignments_in_transfer_and_time_costs": True,
        },
        "approval_receipt_contract": {
            "path": f"{RELATIVE_ROOT}/b1r_v11_approval_receipt.json",
            "schema_version": "rq2b-v11-b1r-approval-receipt-v1",
            "state": "explicitly_approved_for_v11_b1r_once",
            "must_bind_packet_and_scope_hashes": True,
        },
        "next_action": "obtain explicit user approval of this exact packet and scope hash before assigning any source-text chunk",
    }
    write_json_new(packet_path, packet)
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    root = args.root.resolve()
    packet = build(root)
    packet_path = root / RELATIVE_ROOT / PACKET_NAME
    print(
        json.dumps(
            {
                "state": packet["state"],
                "packet_sha256": sha256_file(packet_path),
                "scope_sha256": packet["scope_sha256"],
                "counts": {
                    "source_skill_texts": packet["scope"]["texts"],
                    "chunks": packet["scope"]["chunks"],
                    "source_utf8_bytes": packet["scope"]["source_utf8_bytes"],
                    "local_proxy_tokens": packet["scope"]["local_qwen_proxy_tokens"],
                    "maximum_active_workers": packet["scope"]["maximum_active_workers"],
                    "maximum_total_assignment_attempts": packet["scope"]["maximum_total_assignment_attempts"],
                    "maximum_assigned_source_rows": packet["scope"]["maximum_assigned_source_rows"],
                },
                "external_texts_transmitted": packet["external_texts_transmitted"],
                "workers_started": packet["workers_started"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
