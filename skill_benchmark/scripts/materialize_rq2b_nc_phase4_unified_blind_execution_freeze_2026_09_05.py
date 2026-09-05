#!/usr/bin/env python3
"""Freeze a repaired Phase-4 delivery where main/tail roles are reviewer-hidden."""
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
AUDIT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"
OUT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v4-unified-8candidate-blind-delivery"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical_row_sha(row: dict[str, Any]) -> str:
    return text_sha(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def blind_packet_id(prompt_sha: str) -> str:
    return "P-" + hashlib.sha256(f"rq2b-nc-phase4-unified-blind-v1\0{prompt_sha}".encode("utf-8")).hexdigest()[:18].upper()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite unified blind execution freeze: {out}")
    paths = {"controlling_sop": SOP, "audit_summary": AUDIT / "summary.json", "main_packets": AUDIT / "main_blind_review_packets.jsonl", "tail_packets": AUDIT / "tail_blind_review_packets.jsonl", "allocation_ledger_sealed": AUDIT / "prompt_k6_allocation_ledger.jsonl", "opaque_token_join_sealed": AUDIT / "opaque_token_join.jsonl"}
    for path in paths.values():
        if not path.is_file():
            raise SystemExit(f"Missing V4 freeze input: {path}")
    audit_summary = json.loads(paths["audit_summary"].read_text(encoding="utf-8"))
    if audit_summary.get("status") != "PASS_PHASE4_K6_OUTCOME_BLIND_AUDIT_INPUT_MATERIALISED_PENDING_BLIND_REVIEWS":
        raise SystemExit("Audit input status drift")
    for name, expected in audit_summary.get("outputs", {}).items():
        path = AUDIT / name
        if not path.is_file() or sha(path) != expected:
            raise SystemExit(f"Sealed audit-output hash drift: {name}")
    main = read_jsonl(paths["main_packets"])
    tails = read_jsonl(paths["tail_packets"])
    main_by_prompt = {row["prompt_sha256"]: row for row in main}
    tails_by_prompt: dict[str, list[dict[str, Any]]] = {}
    for row in tails:
        tails_by_prompt.setdefault(row["prompt_sha256"], []).append(row)
    if len(main) != len(main_by_prompt) != 1226 or len(tails) != 2452 or set(tails_by_prompt) != set(main_by_prompt):
        raise SystemExit("Frozen main/tail prompt partition drift")
    if any(len(row["candidates"]) != 6 for row in main) or any(len(rows) != 2 or any(len(row["candidates"]) != 1 for row in rows) for rows in tails_by_prompt.values()):
        raise SystemExit("Frozen K=6/tail cardinality drift")
    reviewer_instruction = "Read the prompt and every complete source-visible candidate in this packet. Independently judge each candidate as FULLY_ACCEPTABLE, PARTIALLY_ADEQUATE, INADEQUATE or UNCLEAR under the frozen adequacy rubric. Quote or precisely locate source-visible support and any material limitation. Candidate token order has no target, rank, route, main-pool or tail meaning. Do not select MOST_SUITABLE."
    rubric = {"FULLY_ACCEPTABLE": "Independently satisfies every material input, transformation, constraint and requested output without an unrecorded component or material unsupported assumption.", "PARTIALLY_ADEQUATE": "Meaningful neighbouring route that misses a material requirement, output, constraint, executable step or dependency.", "INADEQUATE": "Not a plausible route for the central task/input/output boundary.", "UNCLEAR": "Source-visible material is insufficient or internally ambiguous; this blocks closure and is not a weak negative."}
    instruction_sha = text_sha(reviewer_instruction + "\n" + json.dumps(rubric, sort_keys=True))
    batches: list[dict[str, Any]] = []
    for ordinal, (prompt_sha, main_row) in enumerate(sorted(main_by_prompt.items()), start=1):
        tail_rows = sorted(tails_by_prompt[prompt_sha], key=lambda row: row["packet_id"])
        sources = [candidate["candidate_token"] for candidate in main_row["candidates"]] + [candidate["candidate_token"] for row in tail_rows for candidate in row["candidates"]]
        if len(sources) != 8 or len(set(sources)) != 8:
            raise SystemExit("Unified blind candidate token uniqueness drift")
        batches.append({"batch_id": f"RQ2B-P4-U{ordinal:04d}", "blind_packet_id": blind_packet_id(prompt_sha), "prompt_group_unit": "one prompt with six sealed main candidates plus two sealed tails; roles are hidden from reviewers", "prompt_sha256": prompt_sha, "sealed_main_packet": {"packet_id": main_row["packet_id"], "packet_sha256": canonical_row_sha(main_row), "candidate_count": 6}, "sealed_tail_packets": [{"packet_id": row["packet_id"], "packet_sha256": canonical_row_sha(row), "candidate_count": 1} for row in tail_rows], "unified_candidate_tokens_sha256": text_sha("\n".join(sorted(sources))), "reviewer_A": "INDEPENDENT_TARGET_BLIND", "reviewer_B": "INDEPENDENT_TARGET_BLIND", "reviewer_instruction_sha256": instruction_sha, "batch_status": "PENDING_TWO_INDEPENDENT_TARGET_BLIND_RETURNS"})
    reviewer_schema = {"schema_version": "rq2b_nc_phase4_unified_blind_batch_return_v1", "status": "FROZEN_BEFORE_REVIEW", "required_top_level": ["reviewer_blind_id", "batch_id", "blind_packet_id", "batch_input_sha256", "reviewer_instruction_sha256", "assessments", "reviewer_output_sha256"], "reviewer_blind_id_values": ["A", "B"], "assessment_required": ["candidate_token", "adequacy", "source_anchor", "rationale", "missing_material_requirement_or_null"], "adequacy_values": list(rubric), "rubric": rubric, "reviewer_instruction": reviewer_instruction, "blindness_prohibitions": ["Read only the assigned rendered packet and this schema.", "Do not inspect an allocation ledger, token join, target/local/historical reference, source path/provenance/licence, peer return, rank/lane/channel/main/tail metadata, retrieval/reranking/provider output or metric.", "Do not communicate with the other reviewer before the sealed return is submitted."], "return_validation": ["Exactly eight assessments, one for each token in the unified packet.", "No return field identifies main/tail membership, rank, lane, source path or target.", "reviewer_output_sha256 is SHA-256 of canonical JSON excluding that field (UTF-8, sorted keys, comma/colon separators)."]}
    coordinator_schema = {"schema_version": "rq2b_nc_phase4_unified_blind_coordinator_v1", "trigger": "A/B disagreement, either UNCLEAR, invalid/missing return or source-anchor conflict.", "input_rule": "Receive only the sealed independent returns and fresh unified source rendering; no main/tail assignment, target, historical/local reference, rank/lane or retrieval outcome.", "required_fields": ["blind_packet_id", "candidate_token", "reviewer_a_return_sha256", "reviewer_b_return_sha256", "fresh_source_render_sha256", "coordinator_decision", "source_anchor", "rationale", "coordinator_output_sha256"], "decisions": ["CONFIRMED_FULLY_ACCEPTABLE", "CONFIRMED_PARTIALLY_ADEQUATE", "CONFIRMED_INADEQUATE", "CONFIRMED_UNCLEAR", "REOPEN_PACKET"]}
    counts = {"prompt_groups": len(batches), "reviewer_visible_candidates_per_prompt_group": 8, "sealed_main_candidates_per_prompt_group": 6, "sealed_tail_candidates_per_prompt_group": 2, "required_independent_assessments": len(batches) * 8 * 2}
    if counts != {"prompt_groups": 1226, "reviewer_visible_candidates_per_prompt_group": 8, "sealed_main_candidates_per_prompt_group": 6, "sealed_tail_candidates_per_prompt_group": 2, "required_independent_assessments": 19616}:
        raise SystemExit("Unified review workload drift")
    summary = {"status": "PASS_PHASE4_UNIFIED_BLIND_REVIEW_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS", "claim_boundary": "This freezes a corrected review delivery and schemas only. It contains no adequacy return, token join use, reconciliation, acceptable-set label, retrieval result or final benchmark disposition.", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in paths.values()}, "implementation": {"path": str(Path(__file__).relative_to(WORKSPACE)), "sha256": sha(Path(__file__).resolve()), "python": sys.version}, "counts": counts, "reviewer_instruction_sha256": instruction_sha, "outputs": {}, "repair_reason": "V3 delivery exposed packet_kind and differed from its candidate-order declaration. V4 presents all eight already-sealed candidates as one uniform opaque-token-ordered packet, while preserving the sealed K=6/tail allocation only outside reviewer view."}
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
        path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    write_jsonl(out / "unified_prompt_group_batch_manifest.jsonl", batches)
    (out / "unified_independent_reviewer_return_schema.json").write_text(json.dumps(reviewer_schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "unified_sealed_coordinator_return_schema.json").write_text(json.dumps(coordinator_schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for path in (out / "unified_prompt_group_batch_manifest.jsonl", out / "unified_independent_reviewer_return_schema.json", out / "unified_sealed_coordinator_return_schema.json"):
        summary["outputs"][path.name] = sha(path)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"counts": counts, "output_dir": str(out), "status": summary["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
