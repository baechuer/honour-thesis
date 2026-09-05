#!/usr/bin/env python3
"""Zero-network regression tests for the frozen RQ2b local implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from audit_rq2b_exact_source_bytes import compute as compute_exact_bytes
from analyze_rq2b_results import self_test as analysis_self_test
from build_rq2b_implementation_seal import approved_amendment_from_verification
from build_rq2b_cost_ledger import self_test as cost_ledger_self_test
from build_rq2b_i3c_qa_packet import self_test as i3c_qa_packet_self_test
from build_rq2b_i3c_execution_ledger import self_test as i3c_execution_ledger_self_test
from build_rq2b_i3c_transfer_packet import chunks_by_limits, verify as verify_i3c_packet
from build_rq2b_qwen_payload import self_test as qwen_payload_self_test
from build_rq2b_skillrouter_embedding_payload import (
    self_test as skillrouter_embedding_payload_self_test,
)
from build_rq2b_representations import verify as verify_representations
from build_rq2b_skillrouter_payload import self_test as skillrouter_payload_self_test
from finalize_rq2b_i3c_qa import self_test as i3c_qa_decision_self_test
from merge_rq2b_i3c import canonical_extraction, self_test as merge_self_test
from rq2b_chunking import exact_text_chunks
from rq2b_common import (
    B1R_MAXIMUM_ACTIVE_WORKERS,
    FIELD_SPECS,
    RQ2B_IMPLEMENTATION_SCRIPT_PATHS,
    b1r_chunk_inventory,
    b1r_scope_for_extraction,
    read_json,
    repo_root,
    require,
    selector_evidence_spans,
    serialize_i3_flat,
    serialize_i3c,
    sha256_text,
    sha256_file,
    verify_frozen_manifest,
    verify_b0f_a1_amendment,
    verify_i3c_retrieval_ready,
    version_root,
    write_json_new,
)
from rq2b_statistics import self_test as statistics_self_test
from run_rq2b_bm25 import self_test as bm25_self_test
from run_rq2b_qwen import self_test as qwen_self_test
from run_rq2b_skillrouter_embedding import self_test as skillrouter_embedding_self_test
from run_rq2b_skillrouter import self_test as skillrouter_self_test
from verify_rq2b_warm_state import self_test as warm_state_self_test


class CharacterTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [ord(character) for character in text]

    def __call__(self, text: str, **_: Any) -> dict[str, Any]:
        return {
            "input_ids": self.encode(text),
            "offset_mapping": [(index, index + 1) for index in range(len(text))],
        }


def expect_value_error(callable_value: Callable[[], Any], contains: str) -> None:
    try:
        callable_value()
    except ValueError as exc:
        require(contains in str(exc), f"Unexpected negative-test error: {exc}")
    else:
        raise AssertionError(f"Expected ValueError containing {contains!r}")


def evidence_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    source = "name line\nDescription line\n# Steps\nFirst action.\nSecond action.\n"
    input_row = {
        "source_row_index": 0,
        "skill_id": "synthetic",
        "name": "name line",
        "description": "Description line",
        "family": "synthetic",
        "source": "synthetic/SKILL.md",
        "source_sha256": sha256_text(source),
        "text": source,
    }
    fields = {field: [] for field, _ in FIELD_SPECS}
    fields["workflow_steps"] = [
        {
            "id": "step_2",
            "text": "second",
            "evidence": "Second action.",
            "evidence_status": "explicit",
            "confidence": 0.9,
            "selector_usefulness": "high",
        },
        {
            "id": "step_1",
            "text": "first",
            "evidence": "First action.",
            "evidence_status": "explicit",
            "confidence": 0.9,
            "selector_usefulness": "high",
        },
    ]
    fields["success_criteria"] = [
        {
            "id": "success_1",
            "text": "duplicate",
            "evidence": "First action.",
            "evidence_status": "implicit",
            "confidence": 0.6,
            "selector_usefulness": "medium",
        }
    ]
    output_row = {
        "schema_version": "I3C_SUBAGENT_EXTRACTION_V2",
        "parser": "codex_subagent",
        "family": input_row["family"],
        "skill": None,
        "skill_id": input_row["skill_id"],
        "name": input_row["name"],
        "description": input_row["description"],
        "source": input_row["source"],
        "fields": fields,
        "absent_fields": sorted(field for field, _ in FIELD_SPECS if not fields[field]),
        "field_warnings": {},
        "qa_warnings": [],
    }
    return input_row, output_row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--verify-record", action="store_true")
    args = parser.parse_args()
    root = repo_root()
    frozen = verify_frozen_manifest(root)
    amendment = verify_b0f_a1_amendment(root)
    approved_amendment = approved_amendment_from_verification(
        verify_b0f_a1_amendment(root, require_approval=True)
    )
    representations = verify_representations(root)
    packet = verify_i3c_packet(root)
    exact_bytes = compute_exact_bytes(root)
    require(frozen["counts"]["skills"] == 2433, "Frozen skill count regression")
    require(representations["summary"]["i2_exact_source_rows"] == 2433, "I2 exact-source regression")
    require(packet["counts"]["input_rows"] == 2433, "I3C packet row regression")
    require(packet["external_texts_transmitted"] == 0, "I3C packet transfer regression")
    require(exact_bytes["affected_rows"] == 1 and exact_bytes["total_byte_delta"] == 107, "Exact-byte correction regression")
    expect_value_error(
        lambda: verify_i3c_retrieval_ready(root),
        "I3C execution ledger is missing",
    )

    input_row, output_row = evidence_fixture()
    canonical, retained, omitted = canonical_extraction(input_row, output_row)
    require([row["item_id"] for row in retained] == ["step_1", "step_2"], "Evidence source-order regression")
    require(len(omitted) == 1, "Evidence global-dedupe regression")
    i3c = serialize_i3c(input_row["name"], input_row["description"], retained)
    flat = serialize_i3_flat(input_row["name"], input_row["description"], retained)
    require("Workflow / procedure:" in i3c, "Fielded label regression")
    require("Workflow / procedure:" not in flat, "Flat label leakage regression")
    bad_output = json.loads(json.dumps(output_row))
    bad_output["fields"]["workflow_steps"][0]["evidence"] = "Invented evidence."
    expect_value_error(
        lambda: canonical_extraction(input_row, bad_output),
        "Non-substring I3C evidence",
    )
    bad_fields = json.loads(json.dumps(output_row))
    bad_fields["fields"]["extra_field"] = []
    expect_value_error(
        lambda: canonical_extraction(input_row, bad_fields),
        "field-key set mismatch",
    )
    leaked_output = json.loads(json.dumps(output_row))
    leaked_output["gold_skill"] = "synthetic"
    expect_value_error(
        lambda: canonical_extraction(input_row, leaked_output),
        "top-level key mismatch",
    )
    malformed_warning = json.loads(json.dumps(output_row))
    malformed_warning["qa_warnings"] = [
        {
            "code": "generic_fragment_skipped",
            "field": "workflow_steps",
            "message": "Synthetic warning.",
            "evidence": "# Steps",
            "nested": {"anything": "not allowed"},
        }
    ]
    expect_value_error(
        lambda: canonical_extraction(input_row, malformed_warning),
        "warning key mismatch",
    )
    malformed_field_warning = json.loads(json.dumps(output_row))
    malformed_field_warning["field_warnings"] = {"unknown_field": []}
    expect_value_error(
        lambda: canonical_extraction(input_row, malformed_field_warning),
        "field_warnings field-key mismatch",
    )
    spans, _ = selector_evidence_spans(
        output_row,
        source_text=input_row["text"],
        name=input_row["name"],
        description=input_row["description"],
    )
    require(len(spans) == 2, "Selector span regression")

    tokenizer = CharacterTokenizer()
    chunk_text = "paragraph one\n\nparagraph two is longer\n\nparagraph three"
    chunks = exact_text_chunks(tokenizer, chunk_text, maximum_tokens=22, overlap_tokens=4)
    require(len(chunks) > 1, "Synthetic chunking did not exercise overlap")
    require(chunks[0].start_char == 0 and chunks[-1].end_char == len(chunk_text), "Synthetic chunk coverage regression")
    synthetic_rows = [{"skill_id": f"s{index}"} for index in range(5)]
    token_counts = {row["skill_id"]: 20 for row in synthetic_rows}
    packet_chunks = chunks_by_limits(synthetic_rows, token_counts)
    require(sum(len(chunk) for chunk in packet_chunks) == 5, "Packet chunk identity loss")

    report = {
        "schema_version": "rq2b-local-pipeline-tests-v17",
        "state": "pass_zero_network_no_scientific_result",
        "network_calls": 0,
        "frozen_version": frozen["version_id"],
        "representations": representations["summary"],
        "i3c_packet_chunks": packet["counts"]["chunks"],
        "i3c_packet_exact_proxy_tokens": packet["counts"]["total_qwen_proxy_tokens"],
        "retrieval_ready_without_execution_ledger_rejected": True,
        "exact_byte_correction": {
            "affected_rows": exact_bytes["affected_rows"],
            "byte_delta": exact_bytes["total_byte_delta"],
        },
        "merge_self_test": merge_self_test(),
        "bm25_self_test": bm25_self_test(),
        "qwen_self_test": qwen_self_test(),
        "qwen_payload_self_test": qwen_payload_self_test(),
        "skillrouter_embedding_self_test": skillrouter_embedding_self_test(),
        "skillrouter_embedding_payload_self_test": skillrouter_embedding_payload_self_test(),
        "skillrouter_self_test": skillrouter_self_test(),
        "skillrouter_payload_self_test": skillrouter_payload_self_test(),
        "statistics_self_test": statistics_self_test(),
        "analysis_self_test": analysis_self_test(),
        "cost_ledger_self_test": cost_ledger_self_test(),
        "i3c_qa_packet_self_test": i3c_qa_packet_self_test(),
        "i3c_execution_ledger_self_test": i3c_execution_ledger_self_test(),
        "i3c_qa_decision_self_test": i3c_qa_decision_self_test(),
        "warm_state_self_test": warm_state_self_test(),
        "b1r_contract_self_test": {
            "maximum_active_workers": B1R_MAXIMUM_ACTIVE_WORKERS,
            "scope_hash_deterministic": b1r_scope_for_extraction(packet)
            == b1r_scope_for_extraction(packet),
            "chunk_inventory_matches": b1r_chunk_inventory(packet)
            == [
                {
                    "chunk_index": row["chunk_index"],
                    "input_path": row["input_path"],
                    "input_sha256": row["input_sha256"],
                    "expected_output_path": row["expected_output_path"],
                    "row_count": row["row_count"],
                    "qwen_proxy_tokens": row["qwen_proxy_tokens"],
                    "utf8_bytes": row["utf8_bytes"],
                }
                for row in packet["chunks"]
            ],
        },
        "implementation_script_hashes": {
            path_text: sha256_file(root / path_text)
            for path_text in RQ2B_IMPLEMENTATION_SCRIPT_PATHS
        },
        "production_boundaries": {
            "i3c_worker_output_files": sum(
                (root / chunk["expected_output_path"]).exists()
                for chunk in packet["chunks"]
            ),
            "qwen_payload_exists": (version_root(root) / "qwen_payload").exists(),
            "skillrouter_embedding_payload_exists": (
                version_root(root) / "skillrouter_embedding_payload"
            ).exists(),
            "i3c_merged_exists": (version_root(root) / "i3c_merged").exists(),
        },
        "prospective_amendment": {
            "amendment_id": amendment["amendment_id"],
            "authorization_state": amendment["authorization_state"],
            "primary_hypotheses_unchanged": amendment["reporting_contract"]["primary_hypotheses_unchanged"],
        },
        "implementation_seal_bundle_self_test": {
            "approved_amendment_id": approved_amendment["amendment_id"],
            "approval_receipt_verified": True,
        },
    }
    require(report["production_boundaries"]["i3c_worker_output_files"] == 0, "Unexpected I3C worker outputs exist")
    require(report["production_boundaries"]["qwen_payload_exists"] is False, "Unexpected Qwen payload exists")
    require(
        report["production_boundaries"]["skillrouter_embedding_payload_exists"] is False,
        "Unexpected SkillRouter embedding payload exists",
    )
    require(report["production_boundaries"]["i3c_merged_exists"] is False, "Unexpected merged I3C exists")
    require(
        report["b1r_contract_self_test"]["maximum_active_workers"] == 6
        and report["b1r_contract_self_test"]["scope_hash_deterministic"]
        and report["b1r_contract_self_test"]["chunk_inventory_matches"],
        "B1R shared-contract self-test failed",
    )
    record_path = version_root(root) / "smoke" / "local_pipeline_tests_v17.json"
    if args.record:
        write_json_new(record_path, report)
    if args.verify_record:
        require(record_path.exists(), f"Local pipeline test record missing: {record_path}")
        require(read_json(record_path) == report, "Local pipeline test record drift")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
