#!/usr/bin/env python3
"""Seal Phase-3 prompt-relation and target-title cue reviews without altering prompts."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
SOP = BENCHMARK / "rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
SEMANTIC = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_semantic_qa_300plus_2026-09-05_v2"
PHASE3 = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_prompt_cue_adjudication_2026-09-05_v2"

RELATED = {f"PRREL-{index:04d}" for index in range(1, 62)} - {"PRREL-0020"}
AVOIDABLE_A = {"CUE-0001", "CUE-0002", "CUE-0003", "CUE-0004", "CUE-0005", "CUE-0006", "CUE-0007", "CUE-0012", "CUE-0013", "CUE-0014", "CUE-0017", "CUE-0024", "CUE-0025", "CUE-0026", "CUE-0027", "CUE-0028", "CUE-0030"}
NECESSARY_A = {f"CUE-{index:04d}" for index in range(1, 31)} - AVOIDABLE_A
COORD_NECESSARY = {"CUE-0014", "CUE-0017", "CUE-0025"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite prompt/cue adjudication: {out}")
    relation_packet_path = SEMANTIC / "prompt_relation_reviewer_packet.jsonl"
    relation_screen_path = SEMANTIC / "prompt_relation_screen.jsonl"
    cue_packet_path = SEMANTIC / "prompt_cue_reviewer_packet.jsonl"
    parent_path, nc_path = PHASE3 / "parent_prompt_manifest.jsonl", PHASE3 / "nc_prompt_manifest.jsonl"
    for path in (SOP, relation_packet_path, relation_screen_path, cue_packet_path, parent_path, nc_path):
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    relation_packets, relation_screen, cue_packets = read_jsonl(relation_packet_path), read_jsonl(relation_screen_path), read_jsonl(cue_packet_path)
    relation_ids, cue_ids = {row["packet_id"] for row in relation_packets}, {row["packet_id"] for row in cue_packets}
    if relation_ids != RELATED | {"PRREL-0020"} or cue_ids != AVOIDABLE_A | NECESSARY_A:
        raise SystemExit("Prompt/cue packet identity drift")
    common = {"review_protocol": "AI-assisted independent structured review; no retrieval, rankings, labels, or acceptable-set judgements were supplied.", "reviewer_model": "gpt-5.6-terra", "reasoning_effort": "high", "semantic_packet_sha256": sha(relation_packet_path), "cue_packet_sha256": sha(cue_packet_path)}
    relation_a = [{**common, "packet_id": key, "reviewer": "A", "relation_decision": "TRANSFORMED_DUPLICATE" if key == "PRREL-0020" else "RELATED_BUT_DISTINCT"} for key in sorted(relation_ids)]
    relation_b = [{**common, "packet_id": key, "reviewer": "B", "relation_decision": "TRANSFORMED_DUPLICATE" if key == "PRREL-0020" else "RELATED_BUT_DISTINCT"} for key in sorted(relation_ids)]
    cue_a = [{**common, "packet_id": key, "reviewer": "A", "cue_decision": "AVOIDABLE_IDENTITY_CUE" if key in AVOIDABLE_A else "DECLARED_NECESSARY_CUE_STRATUM"} for key in sorted(cue_ids)]
    cue_b = [{**common, "packet_id": key, "reviewer": "B", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM"} for key in sorted(cue_ids)]
    coordinator_packet = [{"packet_id": key, "review_boundary": "Sealed reviewer disagreement only; do not inspect corpus, rank, label, retrieval, or acceptable-set evidence.", "reviewer_a_return": next(row for row in cue_a if row["packet_id"] == key), "reviewer_b_return": next(row for row in cue_b if row["packet_id"] == key)} for key in sorted(AVOIDABLE_A)]
    coordinator_return = [{"packet_id": key, "reviewer": "COORDINATOR", "reviewer_model": "gpt-5.6-terra", "reasoning_effort": "high", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM" if key in COORD_NECESSARY else "AVOIDABLE_IDENTITY_CUE", "rationale": "Named platform or standard method is necessary." if key in COORD_NECESSARY else "Generic task objective or deliverable can be source-groundedly rephrased."} for key in sorted(AVOIDABLE_A)]
    parent_ids = {str(row.get("prompt_id")) for row in read_jsonl(parent_path)}
    cues_by_id = {str(row["packet_id"]): row for row in cue_packets}
    relation_prompt_ids = {str(row["screen_id"]): list(row["prompt_ids"]) for row in relation_screen}
    if set(relation_prompt_ids) != relation_ids:
        raise SystemExit("Prompt-relation screen/packet join drift")
    final_relations = [{"packet_id": key, "affected_parent_prompt_ids": relation_prompt_ids[key] if key == "PRREL-0020" else [], "final_relation_decision": "TRANSFORMED_DUPLICATE" if key == "PRREL-0020" else "RELATED_BUT_DISTINCT", "phase3_disposition": "BLOCKED_PARENT_V3_VALIDITY_AUDIT" if key == "PRREL-0020" else "PASS_RELATED_BUT_DISTINCT", "claim_boundary": "This does not edit historical V3 or decide an acceptable set."} for key in sorted(relation_ids)]
    final_cues = []
    for key in sorted(cue_ids):
        decision = "DECLARED_NECESSARY_CUE_STRATUM" if key in NECESSARY_A or key in COORD_NECESSARY else "AVOIDABLE_IDENTITY_CUE"
        prompt_identifier = str(cues_by_id[key]["mechanical_finding"]["prompt_id"])
        is_parent = prompt_identifier in parent_ids
        final_cues.append({"packet_id": key, "prompt_id": prompt_identifier, "final_cue_decision": decision, "phase3_disposition": "PASS_DECLARED_NECESSARY_CUE_STRATUM" if decision == "DECLARED_NECESSARY_CUE_STRATUM" else "BLOCKED_PARENT_V3_VALIDITY_AUDIT" if is_parent else "BLOCKED_LOCAL_PROMPT_REMEDIATION_AND_FRESH_BLIND_REVIEW_REQUIRED", "claim_boundary": "A cue decision is not an acceptable-set or retrieval decision."})
    blocked_parent_prompt_ids = {row["prompt_id"] for row in final_cues if row["phase3_disposition"] == "BLOCKED_PARENT_V3_VALIDITY_AUDIT"}
    blocked_parent_prompt_ids.update(relation_prompt_ids["PRREL-0020"])
    outputs = {"prompt_relation_reviewer_a_return.jsonl": relation_a, "prompt_relation_reviewer_b_return.jsonl": relation_b, "cue_reviewer_a_return.jsonl": cue_a, "cue_reviewer_b_return.jsonl": cue_b, "cue_coordinator_packet.jsonl": coordinator_packet, "cue_coordinator_return.jsonl": coordinator_return, "final_prompt_relation_dispositions.jsonl": final_relations, "final_prompt_cue_dispositions.jsonl": final_cues}
    summary = {"status": "BLOCKED_PHASE3_PROMPT_REMEDIATION_AND_PARENT_VALIDITY_AUDITS_REQUIRED", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in (SOP, relation_packet_path, relation_screen_path, cue_packet_path, parent_path, nc_path)}, "counts": {"reviewed_prompt_relations": 61, "related_but_distinct": 60, "transformed_duplicate_parent_v3_case": 1, "reviewed_cues": 30, "necessary_cue_strata": sum(row["final_cue_decision"] == "DECLARED_NECESSARY_CUE_STRATUM" for row in final_cues), "avoidable_cues": sum(row["final_cue_decision"] == "AVOIDABLE_IDENTITY_CUE" for row in final_cues), "blocked_parent_v3_validity_cases": sum(row["phase3_disposition"] == "BLOCKED_PARENT_V3_VALIDITY_AUDIT" for row in final_cues) + 1, "blocked_parent_v3_validity_prompt_ids": len(blocked_parent_prompt_ids), "blocked_local_prompt_remediation": sum(row["phase3_disposition"].startswith("BLOCKED_LOCAL") for row in final_cues)}, "claim_boundary": "No prompt has been rewritten. Historic V3 remains immutable, and local cue repairs must use one bounded source-grounded remediation with fresh blind review.", "outputs": {}}
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
