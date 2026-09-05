#!/usr/bin/env python3
"""Create one permitted cue-remediation authoring packet for a source-native batch."""

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


def require_nonempty_string(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"Missing non-empty {key}: {row.get('original_prompt_token')}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise one-time source-native cue-remediation authoring packets.")
    parser.add_argument("--authoring-dir", type=Path, default=DEFAULT_AUTHORING_DIR)
    parser.add_argument("--batch-label", default="BATCH_001")
    parser.add_argument("--expected-cue-risk-prompts", type=int, default=2)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.batch_label.strip():
        raise SystemExit("--batch-label must be non-empty")
    if args.expected_cue_risk_prompts < 1:
        raise SystemExit("--expected-cue-risk-prompts must be positive")
    authoring_dir = args.authoring_dir.resolve()
    author_packet = authoring_dir / "author_packet.jsonl"
    author_return = authoring_dir / "author_return.jsonl"
    adequacy_dir = authoring_dir / "target_blind_adequacy_packets"
    review_packet = adequacy_dir / "reviewer_a_packet.jsonl"
    internal_key = adequacy_dir / "internal_reconciliation_key.jsonl"
    final_prompts = adequacy_dir / "reconciliation/final_prompt_dispositions/reconciled_prompt_dispositions.jsonl"
    remediation_dir = authoring_dir / "cue_remediation"
    review_dir = remediation_dir / "target_blind_adequacy_packets"
    required = [author_packet, author_return, review_packet, internal_key, final_prompts]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if remediation_dir.exists() or review_dir.exists():
        raise SystemExit("Cue-remediation output directory already exists")

    final_rows = read_jsonl(final_prompts)
    cue_rows = [row for row in final_rows if row.get("final_prompt_disposition") == "REMEDIATE_CUE_RISK"]
    if len(cue_rows) != args.expected_cue_risk_prompts or any(row.get("prompt_integrity") != "CUE_RISK" for row in cue_rows):
        raise SystemExit(f"Expected exactly {args.expected_cue_risk_prompts} CUE_RISK prompt dispositions for the one permitted rewrite")
    cue_by_token = {str(row["prompt_token"]): row for row in cue_rows}

    author_families = {str(row["family_token"]): row for row in read_jsonl(author_packet)}
    author_drafts = {(str(row["family_token"]), str(row["target_member_token"])): row for row in read_jsonl(author_return)}
    original_packet_by_token = {str(row["prompt_token"]): row for row in read_jsonl(review_packet)}
    key_by_token = {str(row["prompt_token"]): row for row in read_jsonl(internal_key)}
    if set(cue_by_token) - set(original_packet_by_token) or set(cue_by_token) - set(key_by_token):
        raise SystemExit("Cue-risk prompts not fully bound to original blind packet/key")

    author_packets: list[dict[str, Any]] = []
    for old_token, final in sorted(cue_by_token.items()):
        family_token = str(final["family_token"])
        member_token = str(final["intended_target_member_token"])
        original = author_drafts.get((family_token, member_token))
        family = author_families.get(family_token)
        if not isinstance(original, dict) or not isinstance(family, dict):
            raise SystemExit(f"Missing source-authoring material for cue remediation: {old_token}")
        author_packets.append({
            "record_type": "source_native_one_time_cue_remediation_authoring",
            "original_prompt_token": old_token,
            "remediation_round": 1,
            "family_token": family_token,
            "target_member_token": member_token,
            "target_source_sha256": original["target_source_sha256"],
            "original_prompt": original["prompt"],
            "complete_original_sources": family["members"],
            "instructions": [
                "The prior draft was marked CUE_RISK. This is the one permitted rewrite; no further cue rewrite will be allowed.",
                "Retain a natural task that the assigned target can support from its complete original source. Do not add capabilities.",
                "Remove source identity signals: no title/name, repository/provider, path, hash, file/command name, copied distinctive phrase, or hidden implementation fingerprint.",
                "Write only ordinary task-defining inputs, expected output and source-supported material constraints. Do not see or infer the target-blind candidate judgments.",
                "This is prompt remediation only; do not assess candidates, change source membership, claim strict uniqueness, or make any final-library decision.",
            ],
        })

    remediation_dir.mkdir(parents=True)
    author_packet_path = remediation_dir / "author_packet.jsonl"
    author_template_path = remediation_dir / "author_return_template.json"
    write_jsonl(author_packet_path, author_packets)
    write_json(author_template_path, {
        "original_prompt_token": "P-...",
        "remediation_round": 1,
        "family_token": "F-...",
        "target_member_token": "S-1",
        "target_source_sha256": "...",
        "revised_prompt": "...",
        "source_supported_distinguishing_requirements": ["..."],
        "cue_audit": "...",
    })
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_ONE_TIME_CUE_REMEDIATION_AUTHOR_PACKET_NO_REWRITE_YET",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "counts": {"cue_risk_prompts": len(author_packets), "maximum_rewrites_per_prompt": 1},
        "outputs": {"author_packet.jsonl": sha256_file(author_packet_path), "author_return_template.json": sha256_file(author_template_path)},
        "claim_boundary": "Authoring packet only; no cue remediation, adequacy outcome, prompt/family admission or whole-library result has been produced.",
    }
    write_json(remediation_dir / "author_packet_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
