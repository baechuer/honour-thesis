#!/usr/bin/env python3
"""Materialise blinded Prompt Abstractability / Anti-Cue Feasibility packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"
PAF_SUPPLEMENT = NC_ROOT / "review/RQ2B_NC_PAF_PROSPECTIVE_SUPPLEMENT_2026-09-05.md"
PAF_CODES = [
    "PAF_PASS",
    "PAF_PASS_DECLARED_TECHNICAL_CUE",
    "PAF_FAIL_REQUIRED_SOURCE_UNIQUE_CUE",
    "PAF_FAIL_NO_NONIDENTITY_CONTRAST",
    "PAF_FAIL_NO_NATURAL_TASK_FRAME",
    "PAF_DEFER_INSUFFICIENT_SOURCE_EVIDENCE",
]
CUE_RISKS = [
    "SOURCE_TITLE_OR_NAME", "REPOSITORY_OR_PROVIDER", "PATH_OR_URL",
    "FILE_OR_COMMAND_IDENTIFIER", "LITERAL_SOURCE_HEADING_OR_UNIQUE_PHRASE",
    "PROPRIETARY_ARTIFACT", "NONE_IDENTIFIED",
]


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def unique_by_token(rows: list[dict[str, Any]], field: str, label: str) -> dict[str, dict[str, Any]]:
    result = {str(row.get(field)): row for row in rows}
    if len(rows) != len(result) or "None" in result:
        raise SystemExit(f"{label} must have unique nonempty {field} values")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise blinded source-native PAF feasibility packets after source/provenance eligibility.")
    parser.add_argument("--review-dir", type=Path, default=REVIEW_DIR)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--expected-families", type=int, default=4)
    parser.add_argument("--batch-label", default="B001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    review_dir = args.review_dir.resolve()
    output_dir = (args.output_dir or review_dir / "reconciliation/paf").resolve()
    final_path = review_dir / "reconciliation/final_dispositions/reconciled_family_dispositions.jsonl"
    provenance_path = review_dir / "reconciliation/pass_provenance_preflight/pass_family_provenance_dispositions.jsonl"
    key_path = review_dir / "internal_reconciliation_key.jsonl"
    packet_path = review_dir / "reviewer_a_packet.jsonl"
    required = [PAF_SUPPLEMENT, final_path, provenance_path, key_path, packet_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")

    final = unique_by_token(read_jsonl(final_path), "family_token", "Final source dispositions")
    provenance = unique_by_token(read_jsonl(provenance_path), "family_token", "Provenance dispositions")
    eligible = {
        token for token, row in final.items()
        if row.get("final_decision") == "PASS_TO_PROMPT_AUTHORING"
        and provenance.get(token, {}).get("family_provenance_preflight_status") == "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE"
    }
    if len(eligible) != args.expected_families:
        raise SystemExit(f"Expected exactly {args.expected_families} final source/provenance-eligible families")
    packets = unique_by_token(read_jsonl(packet_path), "family_token", "Full-source reviewer packet")
    key_rows = read_jsonl(key_path)
    key_by_family: dict[str, dict[str, dict[str, Any]]] = {}
    for row in key_rows:
        token, member = str(row.get("family_token")), str(row.get("member_token"))
        if token in eligible:
            key_by_family.setdefault(token, {})[member] = row

    reviewer_rows: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    for family_token in sorted(eligible):
        packet = packets.get(family_token, {})
        members = packet.get("members")
        keys = key_by_family.get(family_token, {})
        if not isinstance(members, list) or len(members) != 3 or set(keys) != {"S-1", "S-2", "S-3"}:
            raise SystemExit(f"Eligible family packet/key incomplete: {family_token}")
        opaque_members = []
        for member in members:
            member_token = str(member.get("member_token"))
            source_text = member.get("complete_original_skill")
            source_hash = str(member.get("source_byte_sha256"))
            if member_token not in keys or not isinstance(source_text, str) or not source_text or source_hash != str(keys[member_token].get("canonical_source_sha256")):
                raise SystemExit(f"Complete-source binding failed for {family_token}/{member_token}")
            opaque_members.append({"member_token": member_token, "complete_original_skill": source_text})
            bindings.append({
                "family_token": family_token, "member_token": member_token,
                "canonical_source_sha256": source_hash,
                "final_source_decision": final[family_token]["final_decision"],
                "family_provenance_preflight_status": provenance[family_token]["family_provenance_preflight_status"],
            })
        reviewer_rows.append({
            "record_type": "source_native_paf_family_feasibility_review",
            "family_token": family_token,
            "members": opaque_members,
            "instruction": "Assess each complete original source independently. Return a feasibility certificate, never an actual user prompt. Use only opaque family/member tokens; do not use or infer title, provider, repository, path, hash, rank, prior review, or other identity metadata.",
            "rule": "PASS means a neutral natural task frame and nonidentity contrast can be evidenced from this source. PAF_PASS_DECLARED_TECHNICAL_CUE records a technical-cue stratum, not cue safety. A family advances only when every member finally has one of those two pass codes.",
            "return_schema": {
                "family_token": "F-...",
                "member_certificates": [{
                    "member_token": "S-1",
                    "neutral_task_frame": {"goal": "", "input_or_state": "", "deliverable": ""},
                    "functional_decision_boundary": "",
                    "nonidentity_expression": "",
                    "source_evidence_anchors": ["literal source evidence or line location"],
                    "cue_risk_inventory": CUE_RISKS,
                    "result_code": " | ".join(PAF_CODES),
                }],
            },
        })
    output_dir.mkdir(parents=True)
    for reviewer in ("a", "b"):
        write_jsonl(output_dir / f"reviewer_{reviewer}_packet.jsonl", reviewer_rows)
    write_jsonl(output_dir / "internal_paf_source_provenance_bindings.jsonl", bindings)
    write_json(output_dir / "review_return_template.json", reviewer_rows[0]["return_schema"])
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_PAF_PACKETS_MATERIALISED_UNREVIEWED",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "counts": {"families": len(reviewer_rows), "members": len(bindings), "reviewers": 2},
        "outputs": {name: sha256_file(output_dir / name) for name in ["reviewer_a_packet.jsonl", "reviewer_b_packet.jsonl", "internal_paf_source_provenance_bindings.jsonl", "review_return_template.json"]},
        "claim_boundary": "PAF packets are feasibility certificates only. They contain no prompt draft and create no source, cluster, prompt, acceptable-set, admission, selector, metric, or cue-safety claim.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
