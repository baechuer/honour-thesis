#!/usr/bin/env python3
"""Materialise unblinded full-source prompt-authoring packets for eligible families."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"


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
    parser = argparse.ArgumentParser(description="Materialise unblinded full-source prompt-authoring packets for provenance-eligible families.")
    parser.add_argument("--review-dir", type=Path, default=REVIEW_DIR)
    parser.add_argument("--paf-dir", type=Path, help="Final PAF disposition directory; when supplied, author only PAF-eligible families exactly bound to final source/provenance eligibility.")
    parser.add_argument("--expected-families", type=int, default=4)
    parser.add_argument("--batch-label", default="B001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    review_dir = args.review_dir.resolve()
    final_path = review_dir / "reconciliation/final_dispositions/reconciled_family_dispositions.jsonl"
    key_path = review_dir / "internal_reconciliation_key.jsonl"
    provenance_path = review_dir / "reconciliation/pass_provenance_preflight/pass_family_provenance_dispositions.jsonl"
    packet_path_input = review_dir / "reviewer_a_packet.jsonl"
    output_dir = review_dir / "reconciliation/prompt_authoring"
    required = [final_path, key_path, provenance_path, packet_path_input]
    paf_path: Path | None = None
    if args.paf_dir is not None:
        paf_path = args.paf_dir.resolve() / "family_paf_dispositions.jsonl"
        required.append(paf_path)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    eligible_tokens = {str(row["family_token"]) for row in read_jsonl(final_path) if row.get("final_decision") == "PASS_TO_PROMPT_AUTHORING"}
    provenance = {str(row["family_token"]): row for row in read_jsonl(provenance_path)}
    eligible_tokens = {token for token in eligible_tokens if provenance.get(token, {}).get("family_provenance_preflight_status") == "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE"}
    paf_by_family: dict[str, dict[str, Any]] = {}
    paf_final_sha256: str | None = None
    paf_authoring_aids: dict[str, list[dict[str, str]]] = {}
    if paf_path is not None:
        paf_rows = read_jsonl(paf_path)
        paf_by_family = {str(row.get("family_token")): row for row in paf_rows}
        if len(paf_rows) != len(paf_by_family) or set(paf_by_family) != eligible_tokens:
            raise SystemExit("PAF final output must exactly cover the final source/provenance-eligible family-token set")
        for family_token, paf_row in paf_by_family.items():
            bindings = paf_row.get("source_provenance_binding")
            if not isinstance(bindings, list) or len(bindings) != 3:
                raise SystemExit(f"PAF source/provenance binding incomplete: {family_token}")
            expected_hashes: dict[str, str] = {}
            for key_row in read_jsonl(key_path):
                if str(key_row.get("family_token")) == family_token:
                    expected_hashes[str(key_row.get("member_token"))] = str(key_row.get("canonical_source_sha256"))
            actual_hashes = {str(row.get("member_token")): str(row.get("canonical_source_sha256")) for row in bindings}
            if set(actual_hashes) != {"S-1", "S-2", "S-3"} or actual_hashes != expected_hashes or any(row.get("final_source_decision") != "PASS_TO_PROMPT_AUTHORING" or row.get("family_provenance_preflight_status") != "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE" for row in bindings):
                raise SystemExit(f"PAF binding does not exactly match final source/provenance eligibility: {family_token}")
            final_members = paf_row.get("final_member_dispositions")
            if not isinstance(final_members, list) or len(final_members) != 3:
                raise SystemExit(f"PAF final member dispositions incomplete: {family_token}")
            aids: list[dict[str, str]] = []
            for member in final_members:
                certificates = member.get("feasibility_certificates") if isinstance(member, dict) else None
                if not isinstance(certificates, dict) or not certificates:
                    raise SystemExit(f"PAF final feasibility certificate absent: {family_token}")
                certificate = next(iter(certificates.values()))
                if not isinstance(certificate, dict):
                    raise SystemExit(f"PAF final feasibility certificate malformed: {family_token}")
                member_token = str(member.get("member_token"))
                if member_token not in {"S-1", "S-2", "S-3"} or not all(isinstance(certificate.get(field), str) and certificate[field].strip() for field in ("functional_decision_boundary", "nonidentity_expression")):
                    raise SystemExit(f"PAF authoring aid fields malformed: {family_token}/{member_token}")
                aids.append({
                    "member_token": member_token,
                    "final_result_code": str(member.get("final_result_code")),
                    "functional_decision_boundary": certificate["functional_decision_boundary"],
                    "nonidentity_expression": certificate["nonidentity_expression"],
                })
            if {aid["member_token"] for aid in aids} != {"S-1", "S-2", "S-3"}:
                raise SystemExit(f"PAF authoring aids do not cover every member: {family_token}")
            paf_authoring_aids[family_token] = sorted(aids, key=lambda aid: aid["member_token"])
        eligible_tokens = {token for token, row in paf_by_family.items() if row.get("family_paf_disposition") == "PAF_ELIGIBLE_FOR_PROMPT_AUTHORING"}
        paf_final_sha256 = sha256_file(paf_path)
    if len(eligible_tokens) != args.expected_families:
        raise SystemExit(f"Expected exactly {args.expected_families} provenance-eligible source families")
    key_by_family: dict[str, dict[str, str]] = {}
    for row in read_jsonl(key_path):
        token = str(row["family_token"])
        if token in eligible_tokens:
            key_by_family.setdefault(token, {})[str(row["member_token"])] = str(row["canonical_source_sha256"])
    packets = {str(row["family_token"]): row for row in read_jsonl(packet_path_input)}
    authoring_rows: list[dict[str, Any]] = []
    for family_token in sorted(eligible_tokens):
        packet = packets.get(family_token)
        members = packet.get("members") if isinstance(packet, dict) else None
        if not isinstance(members, list) or len(members) != 3 or set(key_by_family.get(family_token, {})) != {"S-1", "S-2", "S-3"}:
            raise SystemExit(f"Eligible family packet/key incomplete: {family_token}")
        authoring_rows.append({
            "record_type": "source_native_prompt_authoring_family",
            "family_token": family_token,
            "members": [{
                "member_token": member["member_token"],
                "canonical_source_sha256": key_by_family[family_token][member["member_token"]],
                "complete_original_skill": member["complete_original_skill"],
            } for member in members],
            "required_output": {
                "one_prompt_per_member": True,
                "prompt_fields": ["family_token", "target_member_token", "target_source_sha256", "prompt", "source_supported_distinguishing_requirements", "cue_audit"],
                "cue_audit": "State why no source title/name/repository/provider/path/unique worked-example phrase is leaked. Use only ordinary task-defining constraints supported by the target source.",
            },
            "instructions": [
                "Write exactly three natural user-task prompts: one intended for each member.",
                "Use the complete original skills as evidence; do not add unsupported capabilities.",
                "Do not copy or mention source title, provider, repository, path, hash, file name, command unique to that skill, or distinctive source wording.",
                "Give a concrete input, intended output and material constraint sufficient for later target-blind adequacy review.",
                "A prompt is a draft only. Do not claim strict uniqueness, acceptable-set completeness, cluster admission or benchmark result.",
            ],
            **({
                "paf_final_outputs_binding": {"path": relative(paf_path), "sha256": paf_final_sha256},
                "paf_nonidentity_authoring_aid": {
                    "instruction": "These are source-grounded feasibility constraints, not an actual prompt and not a cue-safety claim. Preserve the functional decision boundary and nonidentity expression; do not copy identity-bearing source text or treat declared technical cues as safe.",
                    "final_member_constraints": paf_authoring_aids[family_token],
                    "technical_cue_stratum": paf_by_family[family_token]["technical_cue_stratum"],
                },
            } if paf_path is not None else {}),
        })
    output_dir.mkdir(parents=True)
    author_packet_path = output_dir / "author_packet.jsonl"
    template_path = output_dir / "author_return_template.json"
    write_jsonl(author_packet_path, authoring_rows)
    template = {"family_token": "F-...", "target_member_token": "S-1", "target_source_sha256": "...", "prompt": "...", "source_supported_distinguishing_requirements": ["..."], "cue_audit": "..."}
    if paf_path is not None:
        template["paf_nonidentity_authoring_aid_used"] = "State how the final PAF functional boundary/nonidentity expression was respected without copying identity-bearing source wording."
    write_json(template_path, template)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_PROMPT_AUTHORING_PACKETS_NO_PROMPT_DRAFT_YET",
        "bound_inputs": {relative(final_path): sha256_file(final_path), relative(key_path): sha256_file(key_path), relative(provenance_path): sha256_file(provenance_path), relative(packet_path_input): sha256_file(packet_path_input), **({relative(paf_path): paf_final_sha256} if paf_path is not None else {})},
        "counts": {"families": len(authoring_rows), "expected_prompt_drafts": len(authoring_rows) * 3},
        "outputs": {"author_packet.jsonl": sha256_file(author_packet_path), "author_return_template.json": sha256_file(template_path)},
        "claim_boundary": "Packets only; prompts must still be written and target-blind reviewed before any NC admission decision." if paf_path is None else "Packets only; PAF pass is feasibility eligibility only, not cue safety or admission. Prompts must still be written and target-blind reviewed before any NC admission decision.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
