#!/usr/bin/env python3
"""Freeze Phase-4 target-blind review schemas and one-prompt work batches."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
SOP = NC_ROOT / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
AUDIT_INPUT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"
OUT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v3_review-execution-batch-return-repair"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def canonical_row_sha(row: dict[str, Any]) -> str:
    return text_sha(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite review-execution freeze: {out}")

    paths = {
        "controlling_sop": SOP,
        "audit_input_summary": AUDIT_INPUT / "summary.json",
        "main_packets": AUDIT_INPUT / "main_blind_review_packets.jsonl",
        "tail_packets": AUDIT_INPUT / "tail_blind_review_packets.jsonl",
        "opaque_token_join_sealed": AUDIT_INPUT / "opaque_token_join.jsonl",
        "allocation_ledger_sealed": AUDIT_INPUT / "prompt_k6_allocation_ledger.jsonl",
    }
    for path in paths.values():
        if not path.is_file():
            raise SystemExit(f"Missing review-execution input: {path}")
    audit_summary = json.loads(paths["audit_input_summary"].read_text(encoding="utf-8"))
    if audit_summary.get("status") != "PASS_PHASE4_K6_OUTCOME_BLIND_AUDIT_INPUT_MATERIALISED_PENDING_BLIND_REVIEWS":
        raise SystemExit("Audit input status drift")
    main_packets = read_jsonl(paths["main_packets"])
    tail_packets = read_jsonl(paths["tail_packets"])
    main_by_prompt = {row["prompt_sha256"]: row for row in main_packets}
    tails_by_prompt: dict[str, list[dict[str, Any]]] = {}
    for row in tail_packets:
        tails_by_prompt.setdefault(row["prompt_sha256"], []).append(row)
    if len(main_packets) != len(main_by_prompt) != 1226 or len(tail_packets) != 2452 or set(tails_by_prompt) != set(main_by_prompt) or any(len(rows) != 2 for rows in tails_by_prompt.values()):
        raise SystemExit("Blind-packet population or prompt-group partition drift")
    if any(len(row.get("candidates", [])) != 6 for row in main_packets) or any(len(row.get("candidates", [])) != 1 for row in tail_packets):
        raise SystemExit("Reviewer-visible K=6/tail packet cardinality drift")
    if any([item["candidate_token"] for item in row["candidates"]] != sorted(item["candidate_token"] for item in row["candidates"]) for row in main_packets):
        raise SystemExit("Reviewer-visible candidate order is not opaque-token order")

    reviewer_schema = {
        "schema_version": "rq2b_nc_phase4_independent_target_blind_return_v1",
        "status": "FROZEN_BEFORE_REVIEW",
        "required_top_level": ["reviewer_blind_id", "batch_id", "batch_input_sha256", "reviewer_instruction_sha256", "packet_returns", "reviewer_output_sha256"],
        "reviewer_blind_id_values": ["A", "B"],
        "packet_return_required": ["packet_id", "packet_sha256", "assessments"],
        "assessment_required": ["candidate_token", "adequacy", "source_anchor", "rationale", "missing_material_requirement_or_null"],
        "adequacy_values": ["FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"],
        "rubric": {
            "FULLY_ACCEPTABLE": "The complete source-visible skill can independently satisfy every material input, transformation, constraint and requested output without an unrecorded component or material unsupported assumption.",
            "PARTIALLY_ADEQUATE": "The skill is a meaningful neighbouring route but misses a material task requirement, output, constraint, executable step or dependency.",
            "INADEQUATE": "The skill is not a plausible route for the prompt's central task/input/output boundary.",
            "UNCLEAR": "The source-visible material is insufficient or internally ambiguous; this is a blocker, never a weak negative."
        },
        "blindness_prohibitions": ["Do not inspect any allocation ledger, token join, source path/provenance ledger, historical parent reference, NC local roster, target mapping, prior review, retrieval/reranking result, provider output or metric.", "Do not infer an intended answer from candidate-token order; token order is deliberately opaque.", "Do not communicate with the other reviewer or coordinator about a packet before submitting a sealed return."],
        "reviewer_instruction": "Read the prompt and every complete source-visible candidate in the assigned packet. Return one adequacy judgement per token, quoting or precisely locating source-visible support and any material limit. Do not choose MOST_SUITABLE: it is a post-adjudication case relation, not an independent adequacy label.",
        "return_validation": ["Exactly three packet_returns are required for the frozen one-prompt group: one K6 main packet and its two tail packets.", "Each packet candidate occurs exactly once.", "No token outside the assigned packet occurs.", "No unsupported decision or missing source anchor is accepted.", "reviewer_output_sha256 is SHA-256 of the canonical return JSON with that field omitted (UTF-8, keys sorted, separators comma/colon).", "The return is immutable after its output SHA-256 is recorded."],
        "canonical_return_shape": {"reviewer_blind_id": "A|B", "batch_id": "RQ2B-P4-Gxxxx", "batch_input_sha256": "sha256", "reviewer_instruction_sha256": "sha256", "packet_returns": [{"packet_id": "opaque packet ID", "packet_sha256": "sha256", "assessments": [{"candidate_token": "opaque token", "adequacy": "FULLY_ACCEPTABLE|PARTIALLY_ADEQUATE|INADEQUATE|UNCLEAR", "source_anchor": "quote or precise source-visible location", "rationale": "source-grounded explanation", "missing_material_requirement_or_null": "text or null"}]}], "reviewer_output_sha256": "sha256 excluding this field"}
    }
    coordinator_schema = {
        "schema_version": "rq2b_nc_phase4_sealed_disagreement_coordinator_v1",
        "status": "FROZEN_BEFORE_REVIEW",
        "trigger": "Any A/B adequacy disagreement, missing/invalid return, UNCLEAR judgement, or source-anchor conflict.",
        "input_rule": "Coordinator receives only the sealed A/B returns, packet rendering and validity fields needed to resolve the disagreement; no target, local roster, historical gold, rank, lane or retrieval outcome.",
        "required_fields": ["packet_id", "candidate_token", "reviewer_a_return_sha256", "reviewer_b_return_sha256", "fresh_source_render_sha256", "coordinator_decision", "source_anchor", "rationale", "coordinator_output_sha256"],
        "coordinator_decisions": ["CONFIRMED_FULLY_ACCEPTABLE", "CONFIRMED_PARTIALLY_ADEQUATE", "CONFIRMED_INADEQUATE", "CONFIRMED_UNCLEAR", "REOPEN_PACKET"],
        "fail_closed": "CONFIRMED_UNCLEAR or REOPEN_PACKET blocks the affected prompt from final freeze."
    }
    instruction_sha = text_sha(reviewer_schema["reviewer_instruction"] + "\n" + json.dumps(reviewer_schema["rubric"], sort_keys=True))
    batches: list[dict[str, Any]] = []
    for ordinal, (prompt_sha, main) in enumerate(sorted(main_by_prompt.items()), start=1):
        tails = sorted(tails_by_prompt[prompt_sha], key=lambda row: row["packet_id"])
        batches.append({
            "batch_id": f"RQ2B-P4-G{ordinal:04d}",
            "prompt_group_unit": "one_prompt_id_with_its_k6_main_and_two_predeclared_tails",
            "main_packet": {"packet_id": main["packet_id"], "packet_sha256": canonical_row_sha(main)},
            "tail_packets": [{"packet_id": row["packet_id"], "packet_sha256": canonical_row_sha(row)} for row in tails],
            "reviewer_A": {"reviewer_blind_id": "A", "assignment": "INDEPENDENT_TARGET_BLIND"},
            "reviewer_B": {"reviewer_blind_id": "B", "assignment": "INDEPENDENT_TARGET_BLIND"},
            "reviewer_instruction_sha256": instruction_sha,
            "batch_status": "PENDING_TWO_INDEPENDENT_TARGET_BLIND_RETURNS"
        })
    counts = {"prompt_groups": len(batches), "main_packets": len(main_packets), "tail_packets": len(tail_packets), "candidate_assessments_per_reviewer": 7356 + 2452, "required_independent_candidate_assessments": 2 * (7356 + 2452), "batch_size_prompt_groups": 1}
    if counts != {"prompt_groups": 1226, "main_packets": 1226, "tail_packets": 2452, "candidate_assessments_per_reviewer": 9808, "required_independent_candidate_assessments": 19616, "batch_size_prompt_groups": 1}:
        raise SystemExit("Review workload count drift")
    summary = {
        "status": "PASS_PHASE4_REVIEW_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_TARGET_BLIND_RETURNS",
        "claim_boundary": "This freezes reviewer instructions, schemas and batch assignments only. It creates no adequacy return, acceptable-set label, reconciliation, retrieval outcome or final benchmark disposition.",
        "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in paths.values()},
        "implementation": {"path": str(Path(__file__).relative_to(WORKSPACE)), "sha256": sha(Path(__file__).resolve()), "python": sys.version},
        "counts": counts,
        "reviewer_instruction_sha256": instruction_sha,
        "outputs": {},
        "separation": {"reviewers_receive": ["assigned blind packet rendering", "frozen reviewer instruction and return schema"], "reviewers_do_not_receive": ["opaque_token_join", "allocation_ledger", "source path/provenance ledger", "targets", "historical/local labels", "peer returns", "rank/lane/channel", "retrieval/reranking/provider outcomes or metrics"], "coordinator_receives_only_after": "both returns are sealed and a discrepancy/UNCLEAR/validity trigger is present"}
    }
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    write_jsonl(out / "prompt_group_batch_manifest.jsonl", batches)
    (out / "independent_reviewer_return_schema.json").write_text(json.dumps(reviewer_schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "sealed_coordinator_return_schema.json").write_text(json.dumps(coordinator_schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for path in (out / "prompt_group_batch_manifest.jsonl", out / "independent_reviewer_return_schema.json", out / "sealed_coordinator_return_schema.json"):
        summary["outputs"][path.name] = sha(path)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"counts": counts, "output_dir": str(out), "status": summary["status"]}, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
