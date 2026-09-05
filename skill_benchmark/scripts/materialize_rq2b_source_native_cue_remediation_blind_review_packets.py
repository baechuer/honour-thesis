#!/usr/bin/env python3
"""Validate cue-remediation drafts and create re-blinded adequacy packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
DEFAULT_PACKET_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"
DEFAULT_AUTHORING_DIR = DEFAULT_PACKET_DIR / "reconciliation/prompt_authoring"

INTEGRITY_CODES = {"CUE_SAFE", "CUE_RISK", "SOURCE_UNSUPPORTED_OR_MALFORMED"}
CANDIDATE_CODES = {
    "MOST_SUITABLE",
    "FULLY_ACCEPTABLE",
    "PARTIALLY_ADEQUATE",
    "INADEQUATE",
    "UNCLEAR_FROM_SOURCE",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise re-blinded packets for one-time source-native cue remediation.")
    parser.add_argument("--authoring-dir", type=Path, default=DEFAULT_AUTHORING_DIR)
    parser.add_argument("--batch-label", default="BATCH_001")
    parser.add_argument("--expected-remediation-prompts", type=int, default=2)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.batch_label.strip():
        raise SystemExit("--batch-label must be non-empty")
    if args.expected_remediation_prompts < 1:
        raise SystemExit("--expected-remediation-prompts must be positive")
    authoring_dir = args.authoring_dir.resolve()
    adequacy_dir = authoring_dir / "target_blind_adequacy_packets"
    original_review_packet = adequacy_dir / "reviewer_a_packet.jsonl"
    original_key = adequacy_dir / "internal_reconciliation_key.jsonl"
    remediation_dir = authoring_dir / "cue_remediation"
    author_packet = remediation_dir / "author_packet.jsonl"
    author_return = remediation_dir / "author_return.jsonl"
    output_dir = remediation_dir / "target_blind_adequacy_packets"
    required = [original_review_packet, original_key, author_packet, author_return]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")

    original_packets = {str(row["prompt_token"]): row for row in read_jsonl(original_review_packet)}
    original_keys = {str(row["prompt_token"]): row for row in read_jsonl(original_key)}
    remediation_packets = {str(row["original_prompt_token"]): row for row in read_jsonl(author_packet)}
    returns = read_jsonl(author_return)
    if len(remediation_packets) != args.expected_remediation_prompts or len(returns) != args.expected_remediation_prompts:
        raise SystemExit(f"Expected exactly {args.expected_remediation_prompts} one-time cue-remediation packets and returns")

    return_by_old: dict[str, dict[str, Any]] = {}
    for row in returns:
        old_token = row.get("original_prompt_token")
        if not nonempty(old_token) or str(old_token) not in remediation_packets or str(old_token) in return_by_old:
            raise SystemExit("Invalid or duplicate cue-remediation return token")
        packet = remediation_packets[str(old_token)]
        for key in ("family_token", "target_member_token", "target_source_sha256"):
            if row.get(key) != packet.get(key):
                raise SystemExit(f"Remediation return binding mismatch: {old_token}/{key}")
        if row.get("remediation_round") != 1 or not nonempty(row.get("revised_prompt")) or not nonempty(row.get("cue_audit")):
            raise SystemExit(f"Invalid remediation prompt/audit: {old_token}")
        requirements = row.get("source_supported_distinguishing_requirements")
        if not isinstance(requirements, list) or not requirements or not all(nonempty(item) for item in requirements):
            raise SystemExit(f"Invalid remediation requirements: {old_token}")
        return_by_old[str(old_token)] = row
    if set(return_by_old) != set(remediation_packets):
        raise SystemExit("Remediation return set does not reconstruct author packet")

    reviewer_rows: list[dict[str, Any]] = []
    reconciliation_key: list[dict[str, Any]] = []
    for old_token, row in sorted(return_by_old.items()):
        original_packet = original_packets.get(old_token)
        original_key = original_keys.get(old_token)
        if not isinstance(original_packet, dict) or not isinstance(original_key, dict):
            raise SystemExit(f"Missing prior blind packet/key: {old_token}")
        revised_prompt = str(row["revised_prompt"])
        prompt_token = "PR-" + hashlib.sha256(f"{old_token}|{revised_prompt}".encode("utf-8")).hexdigest()[:16]
        old_candidate_to_key = {str(item["candidate_token"]): item for item in original_key["candidates"]}
        candidates_with_key = []
        for candidate in original_packet["candidate_sources"]:
            old_candidate = str(candidate["candidate_token"])
            key_item = old_candidate_to_key.get(old_candidate)
            if not isinstance(key_item, dict):
                raise SystemExit(f"Original candidate key missing: {old_token}/{old_candidate}")
            candidates_with_key.append((candidate, key_item))
        candidates_with_key.sort(key=lambda pair: hashlib.sha256(f"{prompt_token}|{pair[1]['canonical_source_sha256']}".encode("utf-8")).hexdigest())
        candidates = []
        key_candidates = []
        for index, (candidate, key_item) in enumerate(candidates_with_key, start=1):
            candidate_token = f"C-{index}"
            candidates.append({"candidate_token": candidate_token, "complete_original_skill": candidate["complete_original_skill"]})
            key_candidates.append({"candidate_token": candidate_token, "member_token": key_item["member_token"], "canonical_source_sha256": key_item["canonical_source_sha256"]})
        reviewer_rows.append({
            "record_type": "source_native_target_blind_cue_remediation_adequacy",
            "prompt_token": prompt_token,
            "natural_user_task_prompt": revised_prompt,
            "candidate_sources": candidates,
            "review_instructions": [
                "You do not know the author’s intended target or the earlier prompt. Assess every candidate only from the supplied complete original source.",
                "Mark prompt integrity CUE_SAFE, CUE_RISK, or SOURCE_UNSUPPORTED_OR_MALFORMED. Cues include source identity, repository/provider/path/hash, copied distinctive wording, or a hidden implementation fingerprint.",
                "For each candidate select MOST_SUITABLE, FULLY_ACCEPTABLE, PARTIALLY_ADEQUATE, INADEQUATE, or UNCLEAR_FROM_SOURCE and give brief source-grounded evidence.",
                "This is the sole re-review after a cue-risk rewrite. It is local prompt-to-family adequacy only; do not infer strict uniqueness, whole-library completeness, retrieval performance or admission.",
            ],
            "required_return": {"prompt_integrity": sorted(INTEGRITY_CODES), "candidate_decision": sorted(CANDIDATE_CODES), "candidate_tokens": [candidate["candidate_token"] for candidate in candidates]},
        })
        reconciliation_key.append({
            "prompt_token": prompt_token,
            "replaces_prompt_token": old_token,
            "remediation_round": 1,
            "family_token": row["family_token"],
            "intended_target_member_token": row["target_member_token"],
            "intended_target_source_sha256": row["target_source_sha256"],
            "author_cue_audit": row["cue_audit"],
            "author_source_supported_distinguishing_requirements": row["source_supported_distinguishing_requirements"],
            "candidates": key_candidates,
        })

    output_dir.mkdir(parents=True)
    reviewer_a = output_dir / "reviewer_a_packet.jsonl"
    reviewer_b = output_dir / "reviewer_b_packet.jsonl"
    key_path = output_dir / "internal_reconciliation_key.jsonl"
    template = output_dir / "review_return_template.json"
    write_jsonl(reviewer_a, reviewer_rows)
    write_jsonl(reviewer_b, reviewer_rows)
    write_jsonl(key_path, reconciliation_key)
    write_json(template, {"prompt_token": "PR-...", "prompt_integrity": "CUE_SAFE", "prompt_integrity_evidence": "...", "candidate_assessments": [{"candidate_token": "C-1", "decision": "MOST_SUITABLE", "evidence": ["..."]}], "prompt_adequacy_summary": "..."})
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_CUE_REMEDIATION_REBLINDED_PACKETS_NO_REVIEW_YET",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "counts": {"revised_prompts": len(reviewer_rows), "per_reviewer_candidate_assessments": len(reviewer_rows) * 3, "maximum_rewrites_per_prompt": 1},
        "outputs": {"reviewer_a_packet.jsonl": sha256_file(reviewer_a), "reviewer_b_packet.jsonl": sha256_file(reviewer_b), "internal_reconciliation_key.jsonl": sha256_file(key_path), "review_return_template.json": sha256_file(template)},
        "claim_boundary": "Re-blinded packets only; the initial cue-risk prompts remain unadmitted until this one permitted re-review is reconciled.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
