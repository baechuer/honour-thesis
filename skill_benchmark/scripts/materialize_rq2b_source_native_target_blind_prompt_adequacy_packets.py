#!/usr/bin/env python3
"""Validate authored prompts and materialise source-to-source blind adequacy packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PACKET_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"
AUTHORING_DIR = PACKET_DIR / "reconciliation/prompt_authoring"

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


def require_nonempty_string(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"Missing non-empty {key}: {row.get('family_token')}")
    return value


def stable_candidate_order(family_token: str, prompt_token: str, members: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        members,
        key=lambda member: hashlib.sha256(
            f"{family_token}|{prompt_token}|{member['canonical_source_sha256']}".encode("utf-8")
        ).hexdigest(),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate authored prompts and materialise target-blind adequacy packets.")
    parser.add_argument("--authoring-dir", type=Path, default=AUTHORING_DIR)
    parser.add_argument("--expected-families", type=int, default=4)
    parser.add_argument("--batch-label", default="B001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    authoring_dir = args.authoring_dir.resolve()
    author_packet = authoring_dir / "author_packet.jsonl"
    author_return = authoring_dir / "author_return.jsonl"
    output_dir = authoring_dir / "target_blind_adequacy_packets"
    required = [author_packet, author_return]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")

    families = {str(row["family_token"]): row for row in read_jsonl(author_packet)}
    if len(families) != args.expected_families:
        raise SystemExit(f"Expected exactly {args.expected_families} authoring-family packet records")
    expected: dict[tuple[str, str], str] = {}
    for family_token, family in families.items():
        members = family.get("members")
        if not isinstance(members, list) or len(members) != 3:
            raise SystemExit(f"Invalid author packet family: {family_token}")
        for member in members:
            expected[(family_token, str(member["member_token"]))] = str(member["canonical_source_sha256"])
    if len(expected) != args.expected_families * 3:
        raise SystemExit(f"Author packet does not bind exactly {args.expected_families * 3} targets")

    authored_rows = read_jsonl(author_return)
    seen: set[tuple[str, str]] = set()
    validated: list[dict[str, Any]] = []
    for row in authored_rows:
        family_token = require_nonempty_string(row, "family_token")
        member_token = require_nonempty_string(row, "target_member_token")
        target_sha = require_nonempty_string(row, "target_source_sha256")
        prompt = require_nonempty_string(row, "prompt")
        cue_audit = require_nonempty_string(row, "cue_audit")
        requirements = row.get("source_supported_distinguishing_requirements")
        key = (family_token, member_token)
        if key not in expected or expected[key] != target_sha or key in seen:
            raise SystemExit(f"Invalid or duplicate authored target: {key}")
        if not isinstance(requirements, list) or not requirements or not all(isinstance(item, str) and item.strip() for item in requirements):
            raise SystemExit(f"Invalid distinguishing requirements: {key}")
        seen.add(key)
        prompt_token = "P-" + hashlib.sha256(
            f"{family_token}|{member_token}|{target_sha}|{prompt}".encode("utf-8")
        ).hexdigest()[:16]
        validated.append({
            "family_token": family_token,
            "target_member_token": member_token,
            "target_source_sha256": target_sha,
            "prompt": prompt,
            "cue_audit": cue_audit,
            "source_supported_distinguishing_requirements": requirements,
            "prompt_token": prompt_token,
        })
    if len(authored_rows) != args.expected_families * 3 or seen != set(expected):
        raise SystemExit(f"Author return must reconstruct exactly {args.expected_families * 3} bound targets")

    reviewer_packets: list[dict[str, Any]] = []
    reconciliation_key: list[dict[str, Any]] = []
    for draft in sorted(validated, key=lambda row: row["prompt_token"]):
        family = families[draft["family_token"]]
        ordered_members = stable_candidate_order(draft["family_token"], draft["prompt_token"], family["members"])
        candidates = []
        key_candidates = []
        for index, member in enumerate(ordered_members, start=1):
            candidate_token = f"C-{index}"
            candidates.append({
                "candidate_token": candidate_token,
                "complete_original_skill": member["complete_original_skill"],
            })
            key_candidates.append({
                "candidate_token": candidate_token,
                "member_token": member["member_token"],
                "canonical_source_sha256": member["canonical_source_sha256"],
            })
        reviewer_packets.append({
            "record_type": "source_native_target_blind_prompt_adequacy",
            "prompt_token": draft["prompt_token"],
            "natural_user_task_prompt": draft["prompt"],
            "candidate_sources": candidates,
            "review_instructions": [
                "You do not know which source the author intended. Assess every candidate independently from the supplied complete original source.",
                "First mark prompt integrity CUE_SAFE, CUE_RISK, or SOURCE_UNSUPPORTED_OR_MALFORMED. A cue names or leaks source identity, a repository/provider/path/hash, copied distinctive source wording, or a hidden implementation fingerprint.",
                "For every candidate choose exactly one: MOST_SUITABLE, FULLY_ACCEPTABLE, PARTIALLY_ADEQUATE, INADEQUATE, or UNCLEAR_FROM_SOURCE.",
                "MOST_SUITABLE means the source is the strongest direct first route for the concrete task. FULLY_ACCEPTABLE means an independently adequate alternative. PARTIALLY_ADEQUATE means it materially helps but misses an essential constraint. INADEQUATE means it cannot deliver the essential task. UNCLEAR_FROM_SOURCE means the supplied source does not support a confident conclusion.",
                "Use brief source-grounded evidence. Do not use the source title/name as evidence and do not infer missing capability from absence alone.",
                "This is a local prompt-to-family adequacy review only: do not claim strict uniqueness, whole-library acceptable-set completeness, retrieval performance, cluster admission, or benchmark outcome.",
            ],
            "required_return": {
                "prompt_integrity": sorted(INTEGRITY_CODES),
                "candidate_decision": sorted(CANDIDATE_CODES),
                "candidate_tokens": [candidate["candidate_token"] for candidate in candidates],
            },
        })
        reconciliation_key.append({
            "prompt_token": draft["prompt_token"],
            "family_token": draft["family_token"],
            "intended_target_member_token": draft["target_member_token"],
            "intended_target_source_sha256": draft["target_source_sha256"],
            "author_cue_audit": draft["cue_audit"],
            "author_source_supported_distinguishing_requirements": draft["source_supported_distinguishing_requirements"],
            "candidates": key_candidates,
        })

    output_dir.mkdir(parents=True)
    reviewer_a_packet = output_dir / "reviewer_a_packet.jsonl"
    reviewer_b_packet = output_dir / "reviewer_b_packet.jsonl"
    reconciliation_key_path = output_dir / "internal_reconciliation_key.jsonl"
    template_path = output_dir / "review_return_template.json"
    write_jsonl(reviewer_a_packet, reviewer_packets)
    write_jsonl(reviewer_b_packet, reviewer_packets)
    write_jsonl(reconciliation_key_path, reconciliation_key)
    write_json(template_path, {
        "prompt_token": "P-...",
        "prompt_integrity": "CUE_SAFE",
        "prompt_integrity_evidence": "...",
        "candidate_assessments": [{"candidate_token": "C-1", "decision": "MOST_SUITABLE", "evidence": ["..."]}],
        "prompt_adequacy_summary": "...",
    })
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_TARGET_BLIND_ADEQUACY_PACKETS_NO_ADEQUACY_REVIEW_YET",
        "bound_inputs": {relative(author_packet): sha256_file(author_packet), relative(author_return): sha256_file(author_return)},
        "counts": {"families": len(families), "prompts": len(reviewer_packets), "per_prompt_candidates": 3, "per_reviewer_candidate_assessments": len(reviewer_packets) * 3},
        "outputs": {
            "reviewer_a_packet.jsonl": sha256_file(reviewer_a_packet),
            "reviewer_b_packet.jsonl": sha256_file(reviewer_b_packet),
            "internal_reconciliation_key.jsonl": sha256_file(reconciliation_key_path),
            "review_return_template.json": sha256_file(template_path),
        },
        "claim_boundary": "Packets only; no target, candidate or family is adequate/admitted until independent target-blind review and reconciliation complete.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
