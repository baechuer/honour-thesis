#!/usr/bin/env python3
"""Finalize PAF feasibility dispositions after direct agreement or sealed adjudication."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PACKET_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets/reconciliation/paf"
PAF_CODES = {
    "PAF_PASS", "PAF_PASS_DECLARED_TECHNICAL_CUE", "PAF_FAIL_REQUIRED_SOURCE_UNIQUE_CUE",
    "PAF_FAIL_NO_NONIDENTITY_CONTRAST", "PAF_FAIL_NO_NATURAL_TASK_FRAME",
    "PAF_DEFER_INSUFFICIENT_SOURCE_EVIDENCE",
}
PASS_CODES = {"PAF_PASS", "PAF_PASS_DECLARED_TECHNICAL_CUE"}
CUE_RISKS = {
    "SOURCE_TITLE_OR_NAME", "REPOSITORY_OR_PROVIDER", "PATH_OR_URL",
    "FILE_OR_COMMAND_IDENTIFIER", "LITERAL_SOURCE_HEADING_OR_UNIQUE_PHRASE",
    "PROPRIETARY_ARTIFACT", "NONE_IDENTIFIED",
}
MEMBER_TOKENS = {"S-1", "S-2", "S-3"}


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


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def certificates_by_member(row: Any, family_token: str) -> dict[str, dict[str, Any]]:
    if not isinstance(row, dict) or set(row) != {"family_token", "member_certificates"} or not isinstance(row["member_certificates"], list):
        raise SystemExit(f"Coordinator PAF return family schema is not exact: {family_token}")
    result: dict[str, dict[str, Any]] = {}
    for certificate in row["member_certificates"]:
        required = {"member_token", "neutral_task_frame", "functional_decision_boundary", "nonidentity_expression", "source_evidence_anchors", "cue_risk_inventory", "result_code"}
        if not isinstance(certificate, dict) or set(certificate) != required or certificate.get("member_token") in result or certificate.get("member_token") not in MEMBER_TOKENS or certificate.get("result_code") not in PAF_CODES:
            raise SystemExit(f"Invalid coordinator PAF certificate: {family_token}")
        frame = certificate.get("neutral_task_frame")
        anchors, risks = certificate.get("source_evidence_anchors"), certificate.get("cue_risk_inventory")
        if not isinstance(frame, dict) or set(frame) != {"goal", "input_or_state", "deliverable"} or not all(nonempty_string(frame[key]) for key in frame) or not nonempty_string(certificate.get("functional_decision_boundary")) or not nonempty_string(certificate.get("nonidentity_expression")) or not isinstance(anchors, list) or not anchors or not all(nonempty_string(value) for value in anchors) or not isinstance(risks, list) or not risks or len(risks) != len(set(risks)) or not set(risks) <= CUE_RISKS:
            raise SystemExit(f"Invalid coordinator PAF feasibility fields: {family_token}")
        result[str(certificate["member_token"])] = certificate
    if set(result) != MEMBER_TOKENS:
        raise SystemExit(f"Coordinator PAF return must contain exactly three opaque members: {family_token}")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finalize source-native PAF family dispositions without authoring prompts.")
    parser.add_argument("--packet-dir", type=Path, default=PACKET_DIR)
    parser.add_argument("--expected-families", type=int, default=4)
    parser.add_argument("--batch-label", default="B001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    packet_dir = args.packet_dir.resolve()
    reconciliation_dir = packet_dir / "reconciliation"
    direct_path = reconciliation_dir / "direct_agreements.jsonl"
    disagreement_path = reconciliation_dir / "disagreement_index.jsonl"
    coordinator_packet_path = reconciliation_dir / "coordinator_packet.jsonl"
    coordinator_return_path = reconciliation_dir / "coordinator_return.jsonl"
    bindings_path = packet_dir / "internal_paf_source_provenance_bindings.jsonl"
    required = [direct_path, disagreement_path, coordinator_packet_path, coordinator_return_path, bindings_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    output_dir = reconciliation_dir / "final_dispositions"
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    direct_rows, disagreement_rows, coordinator_packets, coordinator_returns = read_jsonl(direct_path), read_jsonl(disagreement_path), read_jsonl(coordinator_packet_path), read_jsonl(coordinator_return_path)
    direct = {str(row.get("family_token")): row for row in direct_rows}
    packets = {str(row.get("family_token")): row for row in coordinator_packets}
    returns = {str(row.get("family_token")): row for row in coordinator_returns}
    disagreements = {str(row.get("family_token")): row for row in disagreement_rows}
    if len(direct_rows) != len(direct) or len(disagreement_rows) != len(disagreements) or len(coordinator_packets) != len(packets) or len(coordinator_returns) != len(returns) or set(packets) != set(returns) or set(packets) != set(disagreements) or set(direct) & set(packets) or len(direct) + len(packets) != args.expected_families:
        raise SystemExit(f"PAF direct/coordinator records must be an exact {args.expected_families}-family partition")
    if any(not isinstance(row.get("member_tokens_with_result_code_disagreement"), list) or not row["member_tokens_with_result_code_disagreement"] or not set(row["member_tokens_with_result_code_disagreement"]) <= MEMBER_TOKENS for row in disagreements.values()):
        raise SystemExit("Sealed coordinator PAF packet is not bound to an A/B result-code disagreement")
    bindings_by_family: dict[str, list[dict[str, Any]]] = {}
    for binding in read_jsonl(bindings_path):
        bindings_by_family.setdefault(str(binding.get("family_token")), []).append(binding)
    if set(bindings_by_family) != set(direct) | set(packets) or any({str(row.get("member_token")) for row in rows} != MEMBER_TOKENS for rows in bindings_by_family.values()):
        raise SystemExit("PAF source/provenance bindings do not exactly cover final PAF family/member tokens")

    final_rows: list[dict[str, Any]] = []
    for family_token, row in direct.items():
        a = {str(value.get("member_token")): value for value in row.get("reviewer_a_certificates", [])}
        b = {str(value.get("member_token")): value for value in row.get("reviewer_b_certificates", [])}
        if set(a) != MEMBER_TOKENS or set(b) != MEMBER_TOKENS or any(a[token].get("result_code") != b[token].get("result_code") for token in MEMBER_TOKENS):
            raise SystemExit(f"Direct PAF row does not preserve exact A/B result-code agreement: {family_token}")
        final_certificates = [{"member_token": token, "final_result_code": a[token]["result_code"], "decision_route": "DIRECT_A_B_RESULT_CODE_AGREEMENT", "feasibility_certificates": {"reviewer_a": a[token], "reviewer_b": b[token]}} for token in sorted(MEMBER_TOKENS)]
        route = "DIRECT_A_B_RESULT_CODE_AGREEMENT"

        final_rows.append({"family_token": family_token, "final_member_dispositions": final_certificates, "decision_route": route, "source_provenance_binding": sorted(bindings_by_family[family_token], key=lambda value: value["member_token"])})
    for family_token, row in returns.items():
        coordinator = certificates_by_member(row, family_token)
        final_certificates = [{"member_token": token, "final_result_code": coordinator[token]["result_code"], "decision_route": "SEALED_INDEPENDENT_RESULT_CODE_ADJUDICATION", "feasibility_certificates": {"coordinator": coordinator[token]}} for token in sorted(MEMBER_TOKENS)]
        final_rows.append({"family_token": family_token, "final_member_dispositions": final_certificates, "decision_route": "SEALED_INDEPENDENT_RESULT_CODE_ADJUDICATION", "source_provenance_binding": sorted(bindings_by_family[family_token], key=lambda value: value["member_token"])})
    for row in final_rows:
        codes = [member["final_result_code"] for member in row["final_member_dispositions"]]
        row["family_paf_disposition"] = "PAF_ELIGIBLE_FOR_PROMPT_AUTHORING" if all(code in PASS_CODES for code in codes) else "PAF_NOT_ELIGIBLE_FOR_PROMPT_AUTHORING"
        row["technical_cue_stratum"] = "HAS_DECLARED_TECHNICAL_CUE" if "PAF_PASS_DECLARED_TECHNICAL_CUE" in codes else "NO_DECLARED_TECHNICAL_CUE_IN_FINAL_CODES"
        row["claim_boundary"] = "PAF is a source-grounded prompt-feasibility certificate, not an actual prompt or a cue-safety, source/cluster admission, acceptable-set, selector, or metric claim."
    final_rows.sort(key=lambda row: row["family_token"])
    output_dir.mkdir(parents=True)
    dispositions_path = output_dir / "family_paf_dispositions.jsonl"
    write_jsonl(dispositions_path, final_rows)
    codes = Counter(member["final_result_code"] for row in final_rows for member in row["final_member_dispositions"])
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_FINAL_PAF_FEASIBILITY_DISPOSITIONS_NO_PROMPT_OR_ADMISSION",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "counts": {"families": len(final_rows), "paf_eligible_families": sum(row["family_paf_disposition"] == "PAF_ELIGIBLE_FOR_PROMPT_AUTHORING" for row in final_rows), "technical_cue_stratum_families": sum(row["technical_cue_stratum"] == "HAS_DECLARED_TECHNICAL_CUE" for row in final_rows), "final_member_codes": dict(sorted(codes.items()))},
        "outputs": {"family_paf_dispositions.jsonl": sha256_file(dispositions_path)},
        "claim_boundary": "A PAF-pass family is only eligible for the next prompt-authoring gate. It is not cue safe and is not admitted to a benchmark or result set.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
