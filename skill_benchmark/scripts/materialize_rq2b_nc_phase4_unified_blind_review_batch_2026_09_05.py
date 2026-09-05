#!/usr/bin/env python3
"""Render one hash-verified uniform eight-candidate packet for reviewer A or B."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
AUDIT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"
EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v4-unified-8candidate-blind-delivery"
OUT = NC_ROOT / "review/RQ2B-NC-phase4-unified-target-blind-batches-2026-09-05"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical_row_sha(row: dict[str, Any]) -> str:
    return text_sha(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--reviewer", choices=("A", "B"), required=True)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    execution_summary = json.loads((EXECUTION / "summary.json").read_text(encoding="utf-8"))
    if execution_summary.get("status") != "PASS_PHASE4_UNIFIED_BLIND_REVIEW_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS":
        raise SystemExit("Unified execution status drift")
    for name, expected in execution_summary.get("outputs", {}).items():
        path = EXECUTION / name
        if not path.is_file() or sha(path) != expected:
            raise SystemExit(f"Unified execution output hash drift: {name}")
    audit_summary = json.loads((AUDIT / "summary.json").read_text(encoding="utf-8"))
    for name, expected in audit_summary.get("outputs", {}).items():
        path = AUDIT / name
        if not path.is_file() or sha(path) != expected:
            raise SystemExit(f"Sealed audit output hash drift: {name}")
    manifest = next((row for row in read_jsonl(EXECUTION / "unified_prompt_group_batch_manifest.jsonl") if row["batch_id"] == args.batch_id), None)
    if manifest is None:
        raise SystemExit(f"Unknown frozen unified batch: {args.batch_id}")
    main_by_id = {row["packet_id"]: row for row in read_jsonl(AUDIT / "main_blind_review_packets.jsonl")}
    tail_by_id = {row["packet_id"]: row for row in read_jsonl(AUDIT / "tail_blind_review_packets.jsonl")}
    main_spec = manifest["sealed_main_packet"]
    main = main_by_id.get(main_spec["packet_id"])
    if main is None or canonical_row_sha(main) != main_spec["packet_sha256"] or len(main["candidates"]) != main_spec["candidate_count"] != 6:
        raise SystemExit("Sealed main packet mismatch")
    tails: list[dict[str, Any]] = []
    for spec in manifest["sealed_tail_packets"]:
        tail = tail_by_id.get(spec["packet_id"])
        if tail is None or canonical_row_sha(tail) != spec["packet_sha256"] or len(tail["candidates"]) != spec["candidate_count"] != 1:
            raise SystemExit("Sealed tail packet mismatch")
        tails.append(tail)
    candidates = list(main["candidates"]) + [candidate for tail in tails for candidate in tail["candidates"]]
    candidates.sort(key=lambda candidate: candidate["candidate_token"])
    if len(candidates) != 8 or len({candidate["candidate_token"] for candidate in candidates}) != 8 or text_sha("\n".join(candidate["candidate_token"] for candidate in candidates)) != manifest["unified_candidate_tokens_sha256"]:
        raise SystemExit("Unified candidate-token set drift")
    schema = json.loads((EXECUTION / "unified_independent_reviewer_return_schema.json").read_text(encoding="utf-8"))
    blind_packet = {"blind_packet_id": manifest["blind_packet_id"], "prompt": main["prompt"], "prompt_sha256": main["prompt_sha256"], "candidates": candidates, "review_instruction": schema["reviewer_instruction"]}
    output = {"batch_id": args.batch_id, "reviewer_blind_id": args.reviewer, "batch_input_sha256": canonical_row_sha(blind_packet), "reviewer_instruction_sha256": manifest["reviewer_instruction_sha256"], "blindness_notice": "This file deliberately contains no main/tail role, target, local roster, historical reference, rank, lane, proposal channel, source path/provenance/licence, peer return, retrieval/reranking/provider outcome or metric. Review only this file and the frozen unified return schema.", "packet": blind_packet}
    if args.validate_only:
        print(json.dumps({"batch_id": args.batch_id, "candidate_assessments": len(candidates), "reviewer": args.reviewer, "status": "PASS_HASH_VERIFIED_UNIFIED_BLIND_BATCH"}, sort_keys=True))
        return 0
    out = args.output_dir.resolve() / f"reviewer_{args.reviewer}"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{args.batch_id}.json"
    if path.exists():
        raise SystemExit(f"Refusing to overwrite unified reviewer batch: {path}")
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"batch_id": args.batch_id, "output": str(path), "reviewer": args.reviewer, "sha256": sha(path), "status": "PASS_HASH_VERIFIED_UNIFIED_BLIND_BATCH"}, sort_keys=True))


if __name__ == "__main__":
    main()
