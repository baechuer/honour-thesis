#!/usr/bin/env python3
"""Materialise blinded full-original-skill packets for one discovery batch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
CORPUS = NC_ROOT / "manifests/source_native_description_corpus_2026-09-04/source_native_description_corpus.jsonl"
BOOTSTRAP_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04"
BATCH = BOOTSTRAP_DIR / "batch_001_full_source_review_queue_internal.jsonl"
OUTPUT_DIR = BOOTSTRAP_DIR / "batch_001_full_source_review_packets"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def token(prefix: str, value: str) -> str:
    return prefix + hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise blinded full-original-source review packets for a discovery batch.")
    parser.add_argument("--batch", type=Path, default=BATCH)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--batch-label", default="B001")
    parser.add_argument("--expected-families", type=int, default=25)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    batch_path = args.batch.resolve()
    output_dir = args.output_dir.resolve()
    required = [PROTOCOL, CORPUS, batch_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    corpus_by_hash = {str(row["canonical_source_sha256"]): row for row in read_jsonl(CORPUS)}
    batch_rows = read_jsonl(batch_path)
    if len(batch_rows) != args.expected_families:
        raise SystemExit(f"{args.batch_label} must contain exactly {args.expected_families} families")
    if any(len(row.get("member_source_sha256", [])) != 3 for row in batch_rows):
        raise SystemExit("Every batch family must have exactly three members")

    reviewer_packets: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []
    for family in batch_rows:
        family_id = str(family["family_id"])
        family_token = token("F-", family_id)
        members: list[dict[str, Any]] = []
        source_hashes = [str(value) for value in family["member_source_sha256"]]
        ordered_hashes = sorted(source_hashes, key=lambda value: hashlib.sha256(f"member:{family_id}:{value}".encode("utf-8")).hexdigest())
        for member_index, source_hash in enumerate(ordered_hashes, start=1):
            row = corpus_by_hash.get(source_hash)
            if row is None:
                raise SystemExit(f"Batch source absent from native corpus: {source_hash}")
            source_paths = [WORKSPACE / str(path) for path in row["source_paths"]]
            source_bytes = []
            for path in source_paths:
                if not path.is_file() or sha256_file(path) != source_hash:
                    raise SystemExit(f"Full-source byte replay failed: {path}")
                source_bytes.append(path.read_bytes())
            if len(set(source_bytes)) != 1:
                raise SystemExit(f"Aliased paths differ for source: {source_hash}")
            source_text = source_bytes[0].decode("utf-8", errors="replace")
            member_token = f"S-{member_index}"
            members.append({
                "member_token": member_token,
                "complete_original_skill": source_text,
                "source_byte_sha256": source_hash,
                "review_instruction": "Read the complete original skill. Cite literal excerpts or line locations; do not infer missing capability from topic familiarity.",
            })
            reconciliation_rows.append({
                "family_token": family_token,
                "family_id": family_id,
                "member_token": member_token,
                "canonical_source_sha256": source_hash,
                "source_paths": [relative(path) for path in source_paths],
                "source_byte_replay": "PASS_SHA256_MATCH",
                "bootstrap_batch_rank": family["batch_rank"],
                "bootstrap_discovery_route": family["discovery_route"],
            })
        reviewer_packets.append({
            "record_type": "source_native_full_source_family_review",
            "family_token": family_token,
            "members": members,
            "rubric": {
                "pass": "Three independent first-route skills share a bounded objective/input/output envelope and have source-supported operational contrast for natural prompts.",
                "reject_codes": ["REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION", "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK", "REJECT_NO_BOUNDED_ENVELOPE", "REJECT_NO_MEMBER_LEVEL_PROMPTABILITY"],
                "defer_codes": ["DEFER_PROVENANCE_OR_LICENSE", "DEFER_INSUFFICIENT_SOURCE_EVIDENCE"],
                "rule": "Do not use rank, source path, origin, population role, previous results or another reviewer's judgement. The original source is authoritative.",
            },
            "return_schema": {"decision": "PASS_TO_PROMPT_AUTHORING | rejection/defer code", "common_envelope_evidence": ["literal source evidence"], "member_contrast_evidence": {"S-1": ["literal evidence"], "S-2": ["literal evidence"], "S-3": ["literal evidence"]}, "rationale": "short source-grounded explanation"},
        })
    output_dir.mkdir(parents=True)
    for reviewer in ("a", "b"):
        write_jsonl(output_dir / f"reviewer_{reviewer}_packet.jsonl", reviewer_packets)
    reconciliation_path = output_dir / "internal_reconciliation_key.jsonl"
    write_jsonl(reconciliation_path, reconciliation_rows)
    template = {
        "record_type": "source_native_full_source_family_review_return",
        "family_token": "F-...",
        "decision": "PASS_TO_PROMPT_AUTHORING | rejection/defer code",
        "common_envelope_evidence": [],
        "member_contrast_evidence": {"S-1": [], "S-2": [], "S-3": []},
        "rationale": "",
    }
    write_json(output_dir / "review_return_template.json", template)
    summary = {
        "status": f"PASS_{args.batch_label}_FULL_ORIGINAL_SOURCE_PACKETS_MATERIALISED_UNREVIEWED",
        "protocol": relative(PROTOCOL),
        "bound_inputs": {relative(CORPUS): sha256_file(CORPUS), relative(batch_path): sha256_file(batch_path)},
        "counts": {"families": len(reviewer_packets), "sources": len(reconciliation_rows), "reviewers": 2},
        "outputs": {"reviewer_a_packet.jsonl": sha256_file(output_dir / "reviewer_a_packet.jsonl"), "reviewer_b_packet.jsonl": sha256_file(output_dir / "reviewer_b_packet.jsonl"), "internal_reconciliation_key.jsonl": sha256_file(reconciliation_path), "review_return_template.json": sha256_file(output_dir / "review_return_template.json")},
        "claim_boundary": "Packets bind complete original skills for independent review; no reviewer outcome, cluster, prompt, label, admission, selector or metric exists yet.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
