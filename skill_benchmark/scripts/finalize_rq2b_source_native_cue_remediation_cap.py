#!/usr/bin/env python3
"""Close the one permitted source-native cue-remediation round without admission."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
DEFAULT_AUTHORING_DIR = NC_ROOT / (
    "review/source_native_lexical_bootstrap_2026-09-04/"
    "batch_001_full_source_review_packets/reconciliation/prompt_authoring"
)

PASS = "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
REMEDIATION_TERMINALS = {
    "REMEDIATE_CUE_RISK": "TERMINAL_AFTER_ONE_REMEDIATION_CUE_RISK",
    "REMEDIATE_INTENDED_TARGET_NOT_MOST_SUITABLE": (
        "TERMINAL_AFTER_ONE_REMEDIATION_INTENDED_TARGET_NOT_MOST_SUITABLE"
    ),
}
FAMILY_ELIGIBLE = "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
FAMILY_UNADMITTED = "RETAIN_AS_UNADMITTED_REVIEW_RECORD"
CLAIM_BOUNDARY = (
    "This one-time cue-remediation cap closure creates no final-library admission. "
    "Only PASS records remain eligible for a later whole-library acceptable-set audit; "
    "no second rewrite is permitted."
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise SystemExit(f"Non-object JSONL record in {path}")
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, value: str) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_sha256(row: dict[str, Any]) -> str:
    encoded = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError:
        return str(path)


def require_text(row: dict[str, Any], key: str, context: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"Missing non-empty {key}: {context}")
    return value


def index_unique(rows: list[dict[str, Any]], key: str, context: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = require_text(row, key, context)
        if value in indexed:
            raise SystemExit(f"Duplicate {key} {value}: {context}")
        indexed[value] = row
    return indexed


def counter_as_dict(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def target_identity(row: dict[str, Any], context: str) -> tuple[str, str, str]:
    return (
        require_text(row, "family_token", context),
        require_text(row, "intended_target_member_token", context),
        require_text(row, "intended_target_source_sha256", context),
    )


def assert_same(value: Any, expected: Any, context: str) -> None:
    if value != expected:
        raise SystemExit(f"Binding mismatch for {context}: {value!r} != {expected!r}")


def validate_target_in_candidates(key: dict[str, Any], context: str) -> None:
    family, member, source_sha = target_identity(key, context)
    candidates = key.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 3:
        raise SystemExit(f"Expected exactly three candidates: {context}")
    target_count = 0
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise SystemExit(f"Invalid candidate record: {context}")
        candidate_member = require_text(candidate, "member_token", context)
        candidate_sha = require_text(candidate, "canonical_source_sha256", context)
        require_text(candidate, "candidate_token", context)
        if candidate_member == member and candidate_sha == source_sha:
            target_count += 1
    if target_count != 1:
        raise SystemExit(f"Target source/member must occur exactly once among candidates: {context}")
    if not family:
        raise SystemExit(f"Missing family binding: {context}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Terminalize a source-native one-time cue-remediation round; no second rewrite or admission."
    )
    parser.add_argument("--authoring-dir", type=Path, default=DEFAULT_AUTHORING_DIR)
    parser.add_argument("--batch-label", default="BATCH_001")
    parser.add_argument("--expected-prompts", type=int, default=2)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.batch_label.strip():
        raise SystemExit("--batch-label must be non-empty")
    if args.expected_prompts < 1:
        raise SystemExit("--expected-prompts must be positive")

    authoring_dir = args.authoring_dir.resolve()
    original_dir = authoring_dir / "target_blind_adequacy_packets"
    remediation_dir = authoring_dir / "cue_remediation"
    revised_dir = remediation_dir / "target_blind_adequacy_packets"
    original_final = original_dir / "reconciliation/final_prompt_dispositions/reconciled_prompt_dispositions.jsonl"
    original_key = original_dir / "internal_reconciliation_key.jsonl"
    author_packet = remediation_dir / "author_packet.jsonl"
    author_return = remediation_dir / "author_return.jsonl"
    revised_final = revised_dir / "reconciliation/final_prompt_dispositions/reconciled_prompt_dispositions.jsonl"
    revised_key = revised_dir / "internal_reconciliation_key.jsonl"
    revised_family_gate = revised_dir / "reconciliation/final_prompt_dispositions/family_gate_dispositions.jsonl"
    output_dir = remediation_dir / "remediation_cap_closure"
    required = [
        original_final,
        original_key,
        author_packet,
        author_return,
        revised_final,
        revised_key,
        revised_family_gate,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists and will not be overwritten: {output_dir}")

    original_by_token = index_unique(read_jsonl(original_final), "prompt_token", "original final dispositions")
    original_key_by_token = index_unique(read_jsonl(original_key), "prompt_token", "original reconciliation key")
    author_packet_by_old = index_unique(read_jsonl(author_packet), "original_prompt_token", "remediation author packet")
    author_return_by_old = index_unique(read_jsonl(author_return), "original_prompt_token", "remediation author return")
    revised_by_token = index_unique(read_jsonl(revised_final), "prompt_token", "revised final dispositions")
    revised_key_by_token = index_unique(read_jsonl(revised_key), "prompt_token", "revised reconciliation key")
    family_gate_by_token = index_unique(read_jsonl(revised_family_gate), "family_token", "revised family gate")

    original_cue_risk = {
        token: row
        for token, row in original_by_token.items()
        if row.get("final_prompt_disposition") == "REMEDIATE_CUE_RISK"
    }
    if len(original_cue_risk) != args.expected_prompts:
        raise SystemExit(
            f"Expected exactly {args.expected_prompts} original cue-risk prompts; found {len(original_cue_risk)}"
        )
    if set(author_packet_by_old) != set(original_cue_risk):
        raise SystemExit("Author packet must contain exactly the original cue-risk prompt tokens")
    if set(author_return_by_old) != set(original_cue_risk):
        raise SystemExit("Author return must contain exactly the original cue-risk prompt tokens")
    if set(original_key_by_token) != set(original_by_token):
        raise SystemExit("Original final disposition/key token mismatch")

    replacements: dict[str, str] = {}
    terminal_rows: list[dict[str, Any]] = []
    for old_token in sorted(original_cue_risk):
        original = original_cue_risk[old_token]
        original_key_row = original_key_by_token[old_token]
        packet = author_packet_by_old[old_token]
        returned = author_return_by_old[old_token]
        context = f"original prompt {old_token}"
        if original.get("prompt_integrity") != "CUE_RISK":
            raise SystemExit(f"Original cue remediation does not bind CUE_RISK integrity: {context}")
        original_identity = target_identity(original_key_row, context)
        assert_same(original.get("family_token"), original_identity[0], f"{context}/original family")
        assert_same(original.get("intended_target_member_token"), original_identity[1], f"{context}/original member")
        validate_target_in_candidates(original_key_row, context)
        for label, row in (("author packet", packet), ("author return", returned)):
            if row.get("remediation_round") != 1:
                raise SystemExit(f"Expected remediation round 1: {context}/{label}")
            packet_identity = (
                require_text(row, "family_token", f"{context}/{label}"),
                require_text(row, "target_member_token", f"{context}/{label}"),
                require_text(row, "target_source_sha256", f"{context}/{label}"),
            )
            assert_same(packet_identity, original_identity, f"{context}/{label} identity")
        require_text(returned, "revised_prompt", f"{context}/author return")
        require_text(returned, "cue_audit", f"{context}/author return")

        matched_keys = [
            (new_token, key)
            for new_token, key in revised_key_by_token.items()
            if key.get("replaces_prompt_token") == old_token
        ]
        if len(matched_keys) != 1:
            raise SystemExit(f"Expected exactly one revised token replacing {old_token}")
        new_token, key = matched_keys[0]
        if key.get("remediation_round") != 1:
            raise SystemExit(f"Expected remediation round 1 in revised key: {old_token}")
        assert_same(target_identity(key, f"revised prompt {new_token}"), original_identity, f"{context}/revised identity")
        validate_target_in_candidates(key, f"revised prompt {new_token}")
        if new_token not in revised_by_token:
            raise SystemExit(f"Missing revised final disposition: {new_token}")
        revised = revised_by_token[new_token]
        assert_same(revised.get("family_token"), original_identity[0], f"revised prompt {new_token}/family")
        assert_same(revised.get("intended_target_member_token"), original_identity[1], f"revised prompt {new_token}/member")
        revised_disposition = require_text(revised, "final_prompt_disposition", f"revised prompt {new_token}")
        if revised_disposition == PASS:
            terminal_disposition = PASS
            eligible = True
        elif revised_disposition in REMEDIATION_TERMINALS:
            terminal_disposition = REMEDIATION_TERMINALS[revised_disposition]
            eligible = False
        else:
            raise SystemExit(f"Unexpected revised disposition cannot be terminalized: {new_token}/{revised_disposition}")
        if new_token in replacements.values():
            raise SystemExit(f"Revised token replaces more than one original prompt: {new_token}")
        replacements[old_token] = new_token
        terminal_rows.append({
            "terminal_prompt_token": new_token,
            "replaces_prompt_token": old_token,
            "remediation_round": 1,
            "family_token": original_identity[0],
            "intended_target_member_token": original_identity[1],
            "intended_target_source_sha256": original_identity[2],
            "original_final_record_sha256": record_sha256(original),
            "original_final_prompt_disposition": original["final_prompt_disposition"],
            "original_prompt_integrity": original["prompt_integrity"],
            "original_intended_target_blind_decision": original.get("intended_target_blind_decision"),
            "revised_final_record_sha256": record_sha256(revised),
            "revised_final_prompt_disposition": revised_disposition,
            "revised_prompt_integrity": revised.get("prompt_integrity"),
            "revised_intended_target_blind_decision": revised.get("intended_target_blind_decision"),
            "revised_review_route": revised.get("review_route"),
            "terminal_prompt_disposition": terminal_disposition,
            "eligible_for_whole_library_acceptable_set_audit": eligible,
            "claim_boundary": CLAIM_BOUNDARY,
        })

    if len(replacements) != args.expected_prompts:
        raise SystemExit("Replacement mapping does not reconstruct the expected prompt count")
    if set(revised_key_by_token) != set(revised_by_token):
        raise SystemExit("Revised final disposition/key token mismatch")
    if set(revised_by_token) != set(replacements.values()):
        raise SystemExit("Revised final prompts must be exactly the one-to-one replacement tokens")

    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in terminal_rows:
        by_family[str(row["family_token"])].append(row)
    if set(family_gate_by_token) != set(by_family):
        raise SystemExit("Revised family gate must contain exactly the terminalized families")
    family_rows: list[dict[str, Any]] = []
    for family_token, rows in sorted(by_family.items()):
        gate = family_gate_by_token[family_token]
        revised_rows = [revised_by_token[str(row["terminal_prompt_token"])] for row in rows]
        members = sorted(str(row["intended_target_member_token"]) for row in rows)
        revised_counts = counter_as_dict([str(row["final_prompt_disposition"]) for row in revised_rows])
        assert_same(gate.get("prompt_count"), len(rows), f"family {family_token}/prompt_count")
        assert_same(gate.get("prompt_disposition_counts"), revised_counts, f"family {family_token}/prompt dispositions")
        all_three_pass = (
            len(rows) == 3
            and members == ["S-1", "S-2", "S-3"]
            and all(row["terminal_prompt_disposition"] == PASS for row in rows)
        )
        terminal_family_disposition = FAMILY_ELIGIBLE if all_three_pass else FAMILY_UNADMITTED
        assert_same(gate.get("family_disposition"), terminal_family_disposition, f"family {family_token}/gate")
        family_rows.append({
            "family_token": family_token,
            "revised_family_gate_record_sha256": record_sha256(gate),
            "revised_family_gate_disposition": gate["family_disposition"],
            "terminal_family_disposition": terminal_family_disposition,
            "terminal_prompt_count": len(rows),
            "terminal_member_tokens": members,
            "terminal_prompt_disposition_counts": counter_as_dict(
                [str(row["terminal_prompt_disposition"]) for row in rows]
            ),
            "all_three_members_pass": all_three_pass,
            "claim_boundary": CLAIM_BOUNDARY,
        })

    terminal_rows.sort(key=lambda row: (str(row["family_token"]), str(row["intended_target_member_token"])))
    output_dir.mkdir(parents=True)
    terminal_prompt_path = output_dir / "terminal_prompt_dispositions.jsonl"
    terminal_family_path = output_dir / "terminal_family_dispositions.jsonl"
    write_jsonl(terminal_prompt_path, terminal_rows)
    write_jsonl(terminal_family_path, family_rows)
    batch_md = "\n".join([
        f"# {args.batch_label} one-time cue-remediation cap closure",
        "",
        "This directory terminalizes the single permitted cue-remediation round.",
        "It creates **no final library admission** and permits **NO second rewrite**.",
        "",
        f"- Terminal revised prompts: {len(terminal_rows)}",
        f"- Passes eligible only for a later whole-library acceptable-set audit: {sum(row['eligible_for_whole_library_acceptable_set_audit'] for row in terminal_rows)}",
        f"- Terminalized after one remediation: {sum(not row['eligible_for_whole_library_acceptable_set_audit'] for row in terminal_rows)}",
        f"- Family records: {len(family_rows)}",
        f"- Families eligible only for that later audit: {sum(row['terminal_family_disposition'] == FAMILY_ELIGIBLE for row in family_rows)}",
        "",
        "Original and revised final outcomes are retained in the terminal prompt ledger, alongside canonical record hashes. Input file hashes are bound in `summary.json`.",
        "",
    ])
    batch_md_path = output_dir / "BATCH.md"
    write_text(batch_md_path, batch_md)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_ONE_TIME_CUE_REMEDIATION_CAP_CLOSED_NO_FINAL_LIBRARY_ADMISSION_NO_SECOND_REWRITE",
        "claim_boundary": CLAIM_BOUNDARY,
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "counts": {
            "original_cue_risk_prompts": len(original_cue_risk),
            "one_to_one_revised_prompts": len(terminal_rows),
            "terminal_prompt_dispositions": counter_as_dict([str(row["terminal_prompt_disposition"]) for row in terminal_rows]),
            "eligible_for_whole_library_acceptable_set_audit": sum(
                row["eligible_for_whole_library_acceptable_set_audit"] for row in terminal_rows
            ),
            "terminal_after_one_remediation": sum(
                not row["eligible_for_whole_library_acceptable_set_audit"] for row in terminal_rows
            ),
            "families": len(family_rows),
            "terminal_family_dispositions": counter_as_dict(
                [str(row["terminal_family_disposition"]) for row in family_rows]
            ),
        },
        "outputs": {
            "terminal_prompt_dispositions.jsonl": sha256_file(terminal_prompt_path),
            "terminal_family_dispositions.jsonl": sha256_file(terminal_family_path),
            "BATCH.md": sha256_file(batch_md_path),
        },
    }
    summary_path = output_dir / "summary.json"
    write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
