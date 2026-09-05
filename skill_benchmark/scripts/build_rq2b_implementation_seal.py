#!/usr/bin/env python3
"""Bind the reviewed zero-network RQ2b implementation before any science run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_rq2b_i3c_transfer_packet import verify as verify_i3c_packet
from build_rq2b_representations import verify as verify_representations
from rq2b_common import (
    B0F_A1_AMENDMENT_RELATIVE_PATH,
    B0F_A1_AMENDMENT_SHA256,
    B0F_A1_RECEIPT_RELATIVE_PATH,
    VERSION_ID,
    RQ2B_IMPLEMENTATION_SCRIPT_PATHS,
    read_json,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_b0f_a1_amendment,
    verify_b1s_implementation_seal,
    verify_frozen_manifest,
    version_root,
    write_json_new,
)


SCRIPT_PATHS = RQ2B_IMPLEMENTATION_SCRIPT_PATHS


def bound_file(root: Path, path: Path) -> dict[str, Any]:
    require(path.is_file(), f"B1S artifact missing: {path}")
    return {
        "path": relative(path, root),
        "sha256": sha256_file(path),
        "utf8_bytes": path.stat().st_size,
    }


def approved_amendment_from_verification(
    verification: dict[str, Any],
) -> dict[str, Any]:
    """Unwrap the approved amendment bundle returned by the shared verifier."""
    require(
        set(verification) == {"amendment", "receipt"},
        "Approved B0F-A1 verification bundle mismatch",
    )
    amendment = verification["amendment"]
    require(isinstance(amendment, dict), "Approved B0F-A1 amendment is invalid")
    require(
        amendment.get("amendment_id")
        == "rq2b-b0f-a1-skillrouter-embedding-replication-v1",
        "Approved B0F-A1 amendment identity mismatch",
    )
    return amendment


def build(root: Path) -> dict[str, Any]:
    frozen = verify_frozen_manifest(root)
    amendment = approved_amendment_from_verification(
        verify_b0f_a1_amendment(root, require_approval=True)
    )
    representations = verify_representations(root)
    packet = verify_i3c_packet(root)
    frozen_root = version_root(root)
    seal_path = frozen_root / "b1s_implementation_seal.json"
    require(not seal_path.exists(), f"Refusing to overwrite B1S seal: {seal_path}")

    exact_bytes_path = frozen_root / "exact_source_byte_integrity.json"
    chunking_smoke_path = frozen_root / "smoke" / "chunking_smoke.json"
    pipeline_smoke_path = frozen_root / "smoke" / "local_pipeline_tests_v17.json"
    review_path = frozen_root / "reviews" / "b1s_independent_review.json"
    exact_bytes = read_json(exact_bytes_path)
    chunking = read_json(chunking_smoke_path)
    pipeline = read_json(pipeline_smoke_path)
    review = read_json(review_path)

    require(exact_bytes.get("state") == "provenance_metadata_correction_no_scientific_effect", "Exact-byte audit state mismatch")
    require(chunking.get("state") == "zero_network_no_score_smoke", "Chunking smoke did not pass")
    require(pipeline.get("state") == "pass_zero_network_no_scientific_result", "Local pipeline smoke did not pass")
    require(pipeline.get("schema_version") == "rq2b-local-pipeline-tests-v17", "Local pipeline smoke version mismatch")
    require(
        pipeline.get("prospective_amendment", {}).get("amendment_id")
        == amendment["amendment_id"],
        "Local pipeline smoke is not bound to the SkillRouter-embedding amendment",
    )
    require(review.get("verdict") == "PASS", "Independent B1S review did not pass")
    require(review.get("eligible_as_final_approval") is True, "Independent B1S review is not eligible as final approval")
    require(review.get("network_calls") == 0, "Independent B1S review used network")
    require(review.get("scientific_runs") == 0, "Independent B1S review ran scientific scoring")
    require(review.get("edits_made") is False, "Independent B1S review was not read-only")
    require(review.get("prohibited_artifacts_read") is False, "Independent B1S review read prohibited artifacts")
    finding_counts = review.get("finding_counts")
    require(
        isinstance(finding_counts, dict)
        and set(finding_counts) == {"P0", "P1", "P2"}
        and all(
            isinstance(finding_counts[key], int)
            and not isinstance(finding_counts[key], bool)
            and finding_counts[key] >= 0
            for key in ("P0", "P1", "P2")
        ),
        "Independent B1S review finding counts are invalid",
    )
    require(
        finding_counts["P0"] == finding_counts["P1"] == 0,
        "Independent B1S review cannot pass with P0 or P1 findings",
    )

    output_files = [
        root / chunk["expected_output_path"]
        for chunk in packet["chunks"]
        if (root / chunk["expected_output_path"]).exists()
    ]
    boundaries = {
        "i3c_worker_outputs": len(output_files),
        "i3c_merged_exists": (frozen_root / "i3c_merged").exists(),
        "i3c_manual_qa_exists": (frozen_root / "i3c_manual_qa").exists(),
        "qwen_payload_exists": (frozen_root / "qwen_payload").exists(),
        "skillrouter_embedding_payload_exists": (
            frozen_root / "skillrouter_embedding_payload"
        ).exists(),
        "skillrouter_payload_exists": (frozen_root / "skillrouter_payload").exists(),
        "scientific_runs_root_exists": (frozen_root / "runs").exists(),
    }
    require(boundaries["i3c_worker_outputs"] == 0, "Unexpected I3C worker output before B1R")
    require(boundaries["i3c_merged_exists"] is False, "Unexpected merged I3C before B1R")
    require(boundaries["i3c_manual_qa_exists"] is False, "Unexpected I3C manual-QA packet before B1R")
    require(boundaries["qwen_payload_exists"] is False, "Unexpected Qwen payload before B1E")
    require(
        boundaries["skillrouter_embedding_payload_exists"] is False,
        "Unexpected SkillRouter embedding payload before B1E",
    )
    require(boundaries["skillrouter_payload_exists"] is False, "Unexpected SkillRouter payload before B2P")
    require(boundaries["scientific_runs_root_exists"] is False, "Unexpected scientific run root before B1S")

    scripts: dict[str, dict[str, Any]] = {}
    for path_text in SCRIPT_PATHS:
        path = root / path_text
        compile(path.read_text(encoding="utf-8"), path_text, "exec")
        scripts[path.stem] = bound_file(root, path)
    require(
        pipeline.get("implementation_script_hashes")
        == {artifact["path"]: artifact["sha256"] for artifact in scripts.values()},
        "Local pipeline smoke is not bound to the current implementation scripts",
    )

    artifact_paths = {
        "frozen_manifest": frozen_root / "manifest.json",
        "protocol_snapshot": frozen_root / "protocol_snapshot.md",
        "approval_receipt": frozen_root / "b0f_approval_receipt.json",
        "skillrouter_embedding_amendment": root / B0F_A1_AMENDMENT_RELATIVE_PATH,
        "skillrouter_embedding_amendment_approval_receipt": root / B0F_A1_RECEIPT_RELATIVE_PATH,
        "representation_manifest": frozen_root / "representations" / "manifest.json",
        "representation_provenance_refresh": frozen_root / "representation_provenance_refresh.json",
        "exact_source_byte_integrity": exact_bytes_path,
        "i3c_packet_manifest": frozen_root / "i3c_extraction" / "manifest.json",
        "i3c_identity_manifest": frozen_root / "i3c_extraction" / "identity_manifest.jsonl",
        "chunking_smoke": chunking_smoke_path,
        "local_pipeline_smoke_v17": pipeline_smoke_path,
        "independent_review_pass1": frozen_root / "reviews" / "b1s_independent_review_pass1.json",
        "independent_review_pass2_ineligible": frozen_root / "reviews" / "b1s_independent_review_pass2_ineligible.json",
        "independent_review_pass3_failed": frozen_root / "reviews" / "b1s_independent_review_pass3_failed.json",
        "independent_review_pass4_failed": frozen_root / "reviews" / "b1s_independent_review_pass4_failed.json",
        "independent_review_pass5_failed": frozen_root / "reviews" / "b1s_independent_review_pass5_failed.json",
        "independent_review_pass6_failed": frozen_root / "reviews" / "b1s_independent_review_pass6_failed.json",
        "independent_review_pass7_failed": frozen_root / "reviews" / "b1s_independent_review_pass7_failed.json",
        "independent_review_pass8_failed": frozen_root / "reviews" / "b1s_independent_review_pass8_failed.json",
        "independent_review_pass9_failed": frozen_root / "reviews" / "b1s_independent_review_pass9_failed.json",
        "independent_review_pass10_failed": frozen_root / "reviews" / "b1s_independent_review_pass10_failed.json",
        "independent_review_pass11_ineligible_usage_limit": frozen_root / "reviews" / "b1s_independent_review_pass11_ineligible_usage_limit.json",
        "independent_review_pass12_superseded_seal_builder_bug": frozen_root / "reviews" / "b1s_independent_review_pass12_superseded_seal_builder_bug.json",
        "independent_review_scope": frozen_root / "reviews" / "b1s_final_review_scope.md",
        "independent_review": review_path,
    }
    for chunk in packet["chunks"]:
        artifact_paths[f"i3c_input_chunk_{int(chunk['chunk_index']):04d}"] = root / chunk["input_path"]
    seal = {
        "schema_version": "rq2b-b1s-implementation-seal-v1",
        "version_id": VERSION_ID,
        "state": "implementation_sealed_no_scientific_execution",
        "approved_scope_sha256": frozen["approved_scope_sha256"],
        "b0f_a1_amendment_sha256": B0F_A1_AMENDMENT_SHA256,
        "network_calls": 0,
        "scientific_selector_runs": 0,
        "external_texts_transmitted": 0,
        "thesis_results_written": False,
        "counts": {
            "skills": frozen["counts"]["skills"],
            "prompts": frozen["counts"]["prompts"],
            "i1_i2_rows": representations["summary"]["skills"],
            "i3c_input_rows": packet["counts"]["input_rows"],
            "i3c_chunks": packet["counts"]["chunks"],
            "implementation_scripts": len(scripts),
        },
        "production_boundaries": boundaries,
        "independent_review": {
            "verdict": review["verdict"],
            "eligible_as_final_approval": review["eligible_as_final_approval"],
            "network_calls": review["network_calls"],
            "scientific_runs": review["scientific_runs"],
            "edits_made": review["edits_made"],
            "prohibited_artifacts_read": review["prohibited_artifacts_read"],
            "finding_counts": review["finding_counts"],
        },
        "bound_artifacts": {
            name: bound_file(root, path) for name, path in artifact_paths.items()
        },
        "implementation_scripts": scripts,
        "next_gate": {
            "stage": "B1R",
            "requires_explicit_user_approval": True,
            "authorised_now": False,
            "external_source_text_transfer": False,
        },
    }
    write_json_new(seal_path, seal)
    return verify_b1s_implementation_seal(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    result = verify_b1s_implementation_seal(root) if args.verify_only else build(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
