#!/usr/bin/env python3
"""Render one sealed, target-blind Phase-4 prompt-group batch for reviewer A or B."""
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
EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v3_review-execution-batch-return-repair"
OUT = NC_ROOT / "review/RQ2B-NC-phase4-target-blind-batches-2026-09-05_v2_batch-return-repair"
ORDER_SALT = "rq2b-nc-phase4-reviewer-visible-order-v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical_row_sha(row: dict[str, Any]) -> str:
    return text_sha(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def reviewer_order(reviewer: str, packet_id: str, candidate: dict[str, Any]) -> str:
    return hashlib.sha256(f"{ORDER_SALT}\0{reviewer}\0{packet_id}\0{candidate['candidate_token']}".encode("utf-8")).hexdigest()


def render_packet(packet: dict[str, Any], reviewer: str, expected_sha: str) -> dict[str, Any]:
    if canonical_row_sha(packet) != expected_sha:
        raise SystemExit(f"Packet hash drift: {packet['packet_id']}")
    candidates = [dict(candidate) for candidate in packet["candidates"]]
    candidates.sort(key=lambda candidate: reviewer_order(reviewer, packet["packet_id"], candidate))
    return {
        "packet_id": packet["packet_id"],
        "packet_sha256": expected_sha,
        "packet_kind": packet["packet_kind"],
        "prompt": packet["prompt"],
        "prompt_sha256": packet["prompt_sha256"],
        "candidates": candidates,
        "review_instruction": packet["review_instruction"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--reviewer", choices=("A", "B"), required=True)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if not (EXECUTION / "summary.json").is_file():
        raise SystemExit("Missing review-execution freeze")
    summary = json.loads((EXECUTION / "summary.json").read_text(encoding="utf-8"))
    if summary.get("status") != "PASS_PHASE4_REVIEW_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_TARGET_BLIND_RETURNS":
        raise SystemExit("Review-execution freeze status drift")
    batch_rows = read_jsonl(EXECUTION / "prompt_group_batch_manifest.jsonl")
    batch = next((row for row in batch_rows if row["batch_id"] == args.batch_id), None)
    if batch is None:
        raise SystemExit(f"Unknown frozen batch ID: {args.batch_id}")
    main_by_id = {row["packet_id"]: row for row in read_jsonl(AUDIT / "main_blind_review_packets.jsonl")}
    tail_by_id = {row["packet_id"]: row for row in read_jsonl(AUDIT / "tail_blind_review_packets.jsonl")}
    main_spec = batch["main_packet"]
    if main_spec["packet_id"] not in main_by_id:
        raise SystemExit("Frozen main packet is absent")
    rendered = [render_packet(main_by_id[main_spec["packet_id"]], args.reviewer, main_spec["packet_sha256"])]
    for tail_spec in batch["tail_packets"]:
        if tail_spec["packet_id"] not in tail_by_id:
            raise SystemExit("Frozen tail packet is absent")
        rendered.append(render_packet(tail_by_id[tail_spec["packet_id"]], args.reviewer, tail_spec["packet_sha256"]))
    if len(rendered) != 3 or len(rendered[0]["candidates"]) != 6 or any(len(packet["candidates"]) != 1 for packet in rendered[1:]):
        raise SystemExit("Rendered prompt group does not contain K=6 plus exactly two tails")
    output = {
        "batch_id": args.batch_id,
        "reviewer_blind_id": args.reviewer,
        "batch_input_sha256": text_sha(json.dumps(rendered, ensure_ascii=False, sort_keys=True, separators=(",", ":"))),
        "blindness_notice": "This rendering intentionally excludes target identity, local roster, historical gold, lane, rank, proposal channel, source path/provenance/licence, peer returns and every retrieval/reranking/provider/metric outcome. Review only this file and the frozen return schema.",
        "packets": rendered,
    }
    if args.validate_only:
        print(json.dumps({"batch_id": args.batch_id, "candidate_assessments": sum(len(packet["candidates"]) for packet in rendered), "reviewer": args.reviewer, "status": "PASS_RENDERED_TARGET_BLIND_BATCH"}, sort_keys=True))
        return 0
    out = args.output_dir.resolve() / f"reviewer_{args.reviewer}"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{args.batch_id}.json"
    if path.exists():
        raise SystemExit(f"Refusing to overwrite reviewer batch: {path}")
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"batch_id": args.batch_id, "output": str(path), "reviewer": args.reviewer, "sha256": sha(path), "status": "PASS_RENDERED_TARGET_BLIND_BATCH"}, sort_keys=True))


if __name__ == "__main__":
    main()
