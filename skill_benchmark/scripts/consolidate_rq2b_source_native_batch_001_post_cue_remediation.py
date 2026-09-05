#!/usr/bin/env python3
"""Consolidate a batch's initial and one-time cue-remediation prompt records."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
DEFAULT_AUTHORING_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets/reconciliation/prompt_authoring"

PASS = "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Consolidate initial and one-time source-native cue-remediation prompt records.")
    parser.add_argument("--authoring-dir", type=Path, default=DEFAULT_AUTHORING_DIR)
    parser.add_argument("--batch-label", default="BATCH_001")
    parser.add_argument("--expected-initial-prompts", type=int, default=12)
    parser.add_argument("--expected-remediations", type=int, default=2)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.batch_label.strip():
        raise SystemExit("--batch-label must be non-empty")
    if args.expected_initial_prompts < 1 or args.expected_remediations < 1:
        raise SystemExit("Expected prompt and remediation counts must be positive")
    authoring_dir = args.authoring_dir.resolve()
    initial_final = authoring_dir / "target_blind_adequacy_packets/reconciliation/final_prompt_dispositions/reconciled_prompt_dispositions.jsonl"
    remediation_dir = authoring_dir / "cue_remediation/target_blind_adequacy_packets"
    remediation_final = remediation_dir / "reconciliation/final_prompt_dispositions/reconciled_prompt_dispositions.jsonl"
    remediation_key = remediation_dir / "internal_reconciliation_key.jsonl"
    output_dir = (args.output_dir.resolve() if args.output_dir else authoring_dir / f"{args.batch_label.lower()}_post_cue_remediation_consolidation")
    required = [initial_final, remediation_final, remediation_key]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    initial_rows = read_jsonl(initial_final)
    remediation_rows = read_jsonl(remediation_final)
    remediation_keys = read_jsonl(remediation_key)
    initial_by_token = {str(row["prompt_token"]): row for row in initial_rows}
    remediation_by_token = {str(row["prompt_token"]): row for row in remediation_rows}
    key_by_new_token = {str(row["prompt_token"]): row for row in remediation_keys}
    if len(initial_rows) != len(initial_by_token) or len(initial_rows) != args.expected_initial_prompts:
        raise SystemExit(f"Expected exactly {args.expected_initial_prompts} initial prompt records")
    if len(remediation_rows) != len(remediation_by_token) or len(remediation_rows) != args.expected_remediations:
        raise SystemExit(f"Expected exactly {args.expected_remediations} cue-remediation prompt records")
    if set(remediation_by_token) != set(key_by_new_token) or len(key_by_new_token) != args.expected_remediations:
        raise SystemExit("Cue-remediation final/key token mismatch")
    replacements: dict[str, tuple[str, dict[str, Any]]] = {}
    for new_token, key in key_by_new_token.items():
        old_token = str(key.get("replaces_prompt_token"))
        if old_token not in initial_by_token or old_token in replacements:
            raise SystemExit(f"Invalid or duplicate cue-remediation replacement: {old_token}")
        old = initial_by_token[old_token]
        new = remediation_by_token[new_token]
        if old.get("final_prompt_disposition") != "REMEDIATE_CUE_RISK" or old.get("prompt_integrity") != "CUE_RISK":
            raise SystemExit(f"Replacement does not bind an initial cue-risk prompt: {old_token}")
        if old.get("family_token") != key.get("family_token") or old.get("intended_target_member_token") != key.get("intended_target_member_token"):
            raise SystemExit(f"Replacement family/member binding mismatch: {old_token}")
        replacements[old_token] = (new_token, new)
    if len(replacements) != args.expected_remediations:
        raise SystemExit(f"Expected exactly {args.expected_remediations} replacements")

    active_rows: list[dict[str, Any]] = []
    superseded_rows: list[dict[str, Any]] = []
    for old_token, old in sorted(initial_by_token.items()):
        if old_token in replacements:
            new_token, new = replacements[old_token]
            active_rows.append({
                "active_prompt_token": new_token,
                "supersedes_prompt_token": old_token,
                "family_token": new["family_token"],
                "intended_target_member_token": new["intended_target_member_token"],
                "active_prompt_disposition": new["final_prompt_disposition"],
                "active_prompt_integrity": new["prompt_integrity"],
                "active_target_blind_decision": new["intended_target_blind_decision"],
                "review_route": new["review_route"],
                "remediation_round": 1,
                "claim_boundary": "One cue rewrite and a re-blinded local adequacy review only; this record is not a whole-library acceptable set or final-library admission.",
            })
            superseded_rows.append({
                "superseded_prompt_token": old_token,
                "superseded_disposition": old["final_prompt_disposition"],
                "replacement_prompt_token": new_token,
                "replacement_disposition": new["final_prompt_disposition"],
                "reason": "ONE_TIME_CUE_REMEDIATION",
            })
        else:
            active_rows.append({
                "active_prompt_token": old_token,
                "supersedes_prompt_token": None,
                "family_token": old["family_token"],
                "intended_target_member_token": old["intended_target_member_token"],
                "active_prompt_disposition": old["final_prompt_disposition"],
                "active_prompt_integrity": old["prompt_integrity"],
                "active_target_blind_decision": old["intended_target_blind_decision"],
                "review_route": old["review_route"],
                "remediation_round": 0,
                "claim_boundary": "Local three-source adequacy only; this record is not a whole-library acceptable set or final-library admission.",
            })
    active_rows.sort(key=lambda row: (str(row["family_token"]), str(row["intended_target_member_token"])))
    if len(active_rows) != args.expected_initial_prompts or len({row["active_prompt_token"] for row in active_rows}) != args.expected_initial_prompts:
        raise SystemExit("Active prompt ledger does not reconstruct the expected unique prompt records")

    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in active_rows:
        by_family[str(row["family_token"])].append(row)
    family_rows: list[dict[str, Any]] = []
    for family_token, rows in sorted(by_family.items()):
        members = {str(row["intended_target_member_token"]) for row in rows}
        all_pass = len(rows) == 3 and members == {"S-1", "S-2", "S-3"} and all(row["active_prompt_disposition"] == PASS for row in rows)
        family_rows.append({
            "family_token": family_token,
            "active_prompt_count": len(rows),
            "active_member_tokens": sorted(members),
            "family_disposition": "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT" if all_pass else "RETAIN_AS_UNADMITTED_REVIEW_RECORD",
            "active_prompt_disposition_counts": dict(sorted(Counter(row["active_prompt_disposition"] for row in rows).items())),
            "claim_boundary": "Eligibility only; the later whole-library audit and final freeze remain required before any library admission.",
        })
    output_dir.mkdir(parents=True)
    active_path = output_dir / "active_prompt_dispositions.jsonl"
    family_path = output_dir / "family_gate_dispositions.jsonl"
    superseded_path = output_dir / "superseded_cue_risk_records.jsonl"
    write_jsonl(active_path, active_rows)
    write_jsonl(family_path, family_rows)
    write_jsonl(superseded_path, superseded_rows)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_POST_CUE_REMEDIATION_CONSOLIDATED_NO_FINAL_LIBRARY_ADMISSION",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "counts": {
            "active_prompts": len(active_rows),
            "families": len(family_rows),
            "one_time_cue_replacements": len(superseded_rows),
            "active_prompt_dispositions": dict(sorted(Counter(row["active_prompt_disposition"] for row in active_rows).items())),
            "family_dispositions": dict(sorted(Counter(row["family_disposition"] for row in family_rows).items())),
        },
        "outputs": {"active_prompt_dispositions.jsonl": sha256_file(active_path), "family_gate_dispositions.jsonl": sha256_file(family_path), "superseded_cue_risk_records.jsonl": sha256_file(superseded_path)},
        "claim_boundary": "The active prompt ledger records at most one cue rewrite per affected prompt. This is not a whole-library acceptable-set result, cluster/source/prompt final-library admission, selector outcome or metric.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
