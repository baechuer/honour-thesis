#!/usr/bin/env python3
"""Build the exact B1R Codex-worker text-transfer approval packet without transfer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import (
    VERSION_ID,
    B1R_RECEIPT_RELATIVE_PATH,
    b1r_chunk_inventory,
    b1r_scope_for_extraction,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_json,
    verify_b1s_implementation_seal,
    version_root,
    write_json_new,
)
from build_rq2b_i3c_transfer_packet import verify as verify_i3c_packet


def build(root: Path) -> dict[str, Any]:
    seal = verify_b1s_implementation_seal(root)
    frozen_root = version_root(root)
    extraction_manifest_path = frozen_root / "i3c_extraction" / "manifest.json"
    extraction = verify_i3c_packet(root)
    require(extraction.get("state") == "built_not_transmitted", "I3C packet is not awaiting transfer")
    require(extraction.get("external_texts_transmitted") == 0, "I3C packet records prior transfer")
    require(extraction.get("worker_count") == 0, "I3C packet records prior workers")
    output_path = frozen_root / "b1r_authorisation_packet.json"
    require(not output_path.exists(), f"Refusing to overwrite B1R approval packet: {output_path}")

    chunks = b1r_chunk_inventory(extraction)
    scope = b1r_scope_for_extraction(extraction)
    packet = {
        "schema_version": "rq2b-b1r-authorisation-packet-v1",
        "version_id": VERSION_ID,
        "state": "awaiting_explicit_b1r_source_transfer_approval",
        "network_calls": 0,
        "external_texts_transmitted": 0,
        "workers_started": 0,
        "scope": scope,
        "scope_sha256": sha256_json(scope),
        "implementation_seal": {
            "path": relative(frozen_root / "b1s_implementation_seal.json", root),
            "sha256": sha256_file(frozen_root / "b1s_implementation_seal.json"),
            "state": seal["state"],
        },
        "i3c_extraction_manifest": {
            "path": relative(extraction_manifest_path, root),
            "sha256": sha256_file(extraction_manifest_path),
        },
        "extraction_prompt": extraction["extraction_prompt"],
        "chunks": chunks,
        "execution_requirements": {
            "use_only_assigned_input_artifact_text": True,
            "read_frozen_extraction_prompt": True,
            "one_json_object_per_input_row": True,
            "validate_jsonl_row_identity_and_exact_evidence": True,
            "record_hash_bound_worker_event_per_explicit_assignment": True,
            "close_completed_or_failed_workers": True,
            "no_duplicate_active_assignments": True,
            "stop_on_hash_or_identity_failure": True,
            "no_automatic_retries": True,
            "replacement_assignments_must_be_explicit_and_event_logged": True,
        },
        "worker_event_ledger": {
            "path": relative(frozen_root / "i3c_extraction" / "worker_events.jsonl", root),
            "schema_version": "rq2b-i3c-worker-event-v1",
            "record_failed_replacements": True,
            "count_repeated_assignments_in_transfer_and_time_costs": True,
        },
        "next_action": "obtain explicit user approval of this packet and scope hash before spawning any worker",
        "approval_receipt_contract": {
            "path": B1R_RECEIPT_RELATIVE_PATH,
            "schema_version": "rq2b-b1r-approval-receipt-v1",
            "state": "explicitly_approved_for_b1r_once",
            "must_bind_packet_and_scope_hashes": True,
        },
    }
    write_json_new(output_path, packet)
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    root = args.root.resolve()
    result = build(root)
    packet_path = version_root(root) / "b1r_authorisation_packet.json"
    print(
        json.dumps(
            {
                "state": result["state"],
                "scope_sha256": result["scope_sha256"],
                "packet_sha256": sha256_file(packet_path),
                "counts": {
                    "texts": result["scope"]["texts"],
                    "chunks": result["scope"]["chunks"],
                    "source_utf8_bytes": result["scope"]["source_utf8_bytes"],
                    "local_qwen_proxy_tokens": result["scope"]["local_qwen_proxy_tokens"],
                    "maximum_replacement_assignments": result["scope"]["maximum_replacement_assignments"],
                    "maximum_total_assignment_attempts": result["scope"]["maximum_total_assignment_attempts"],
                    "maximum_assigned_source_rows": result["scope"]["maximum_assigned_source_rows"],
                    "maximum_assigned_source_utf8_bytes": result["scope"]["maximum_assigned_source_utf8_bytes"],
                    "maximum_assigned_qwen_proxy_tokens": result["scope"]["maximum_assigned_qwen_proxy_tokens"],
                },
                "external_texts_transmitted": result["external_texts_transmitted"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
