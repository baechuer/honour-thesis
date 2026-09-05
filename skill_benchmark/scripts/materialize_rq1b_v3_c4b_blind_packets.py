#!/usr/bin/env python3
"""Materialise source-deidentified RQ1b V3 C4B adequacy-review packets.

This program is deliberately a curation boundary, not a selector.  It combines
only C4A canonical cards whose literal/provenance audit passed with C3-allowed
prompt records.  Two reviewer-specific files receive distinct deterministic
candidate-label permutations; the separately stored key contains the sealed
lineage required only by later C5/C6 reconciliation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any


FIELD_ORDER = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)
CARD_STATUSES = {"EVIDENCE", "NOT_STATED"}
C4A_ACCEPT = "RQ1B_V3_C4A_CONFORMANCE_ACCEPT_CANONICAL_CARD_NOT_A_RESULT"
C4A_AUDIT_PASS = "RQ1B_V3_C4A_CANONICAL_CARD_AUDIT_PASS"
C3_ALLOW = "C3_ALLOW_C4_WITH_RISK_ANNOTATION"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"jsonl_row_not_object:{path}:{line_number}")
        rows.append(value)
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lineage-manifest", type=Path, action="append", required=True)
    parser.add_argument("--canonical-proposal", type=Path, action="append", required=True)
    parser.add_argument("--canonical-audit", type=Path, action="append", required=True)
    parser.add_argument("--c3-ledger", type=Path, action="append", required=True)
    parser.add_argument("--prompt-ledger", type=Path, action="append", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--seed", default="rq1b-v3-c4b-v1")
    return parser.parse_args()


def index_unique(rows: list[dict[str, Any]], field: str, source: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = str(row.get(field, ""))
        if not value:
            raise ValueError(f"missing_{field}:{source}")
        if value in indexed:
            raise ValueError(f"duplicate_{field}:{source}:{value}")
        indexed[value] = row
    return indexed


def validate_card(card: dict[str, Any], packet_id: str) -> None:
    if set(card) != set(FIELD_ORDER):
        raise ValueError(f"card_field_coverage:{packet_id}")
    for field in FIELD_ORDER:
        value = card[field]
        if not isinstance(value, dict):
            raise ValueError(f"card_field_not_object:{packet_id}:{field}")
        status = str(value.get("status", ""))
        quotes = value.get("quotes")
        if status not in CARD_STATUSES or not isinstance(quotes, list):
            raise ValueError(f"card_field_schema:{packet_id}:{field}")
        if status == "NOT_STATED" and quotes:
            raise ValueError(f"not_stated_has_quotes:{packet_id}:{field}")
        if status == "EVIDENCE" and (not quotes or not all(isinstance(quote, str) and quote for quote in quotes)):
            raise ValueError(f"evidence_quotes_invalid:{packet_id}:{field}")


def reviewer_labels(seed: str, case_index: int, candidate_labels: list[str], reviewer_index: int) -> list[str]:
    ordered = list(candidate_labels)
    material = f"{seed}:{case_index}:{reviewer_index}".encode("utf-8")
    random.Random(int(hashlib.sha256(material).hexdigest(), 16)).shuffle(ordered)
    if reviewer_index == 2 and ordered == reviewer_labels(seed, case_index, candidate_labels, 1):
        ordered = ordered[1:] + ordered[:1]
    return ordered


def main() -> int:
    args = parse_args()
    if len(args.canonical_proposal) != len(args.canonical_audit):
        raise SystemExit("canonical_proposal_audit_count_mismatch")

    lineage_by_packet: dict[str, dict[str, Any]] = {}
    lineage_paths: dict[str, Path] = {}
    for manifest_path in args.lineage_manifest:
        rows = read_json(manifest_path)
        if not isinstance(rows, list):
            raise SystemExit(f"lineage_manifest_not_list:{manifest_path}")
        for row in rows:
            packet_id = str(row.get("packet_id", ""))
            if not packet_id or packet_id in lineage_by_packet:
                raise SystemExit(f"duplicate_or_missing_lineage_packet:{manifest_path}:{packet_id}")
            lineage_by_packet[packet_id] = row
            lineage_paths[packet_id] = manifest_path

    canonical_by_packet: dict[str, tuple[dict[str, Any], Path, Path]] = {}
    for proposal_path, audit_path in zip(args.canonical_proposal, args.canonical_audit):
        proposal = read_json(proposal_path)
        audit = read_json(audit_path)
        packet_id = str(proposal.get("packet_id", ""))
        if not packet_id or packet_id in canonical_by_packet:
            raise SystemExit(f"duplicate_or_missing_canonical_packet:{proposal_path}:{packet_id}")
        if proposal.get("status") != C4A_ACCEPT:
            raise SystemExit(f"canonical_not_accepted:{packet_id}")
        if audit.get("status") != C4A_AUDIT_PASS or audit.get("packet_id") != packet_id:
            raise SystemExit(f"canonical_audit_not_pass:{packet_id}")
        cards = proposal.get("cards")
        if not isinstance(cards, dict) or set(cards) not in ({"Candidate A", "Candidate B", "Candidate C"}, {"Candidate A", "Candidate B", "Candidate C", "Candidate D"}):
            raise SystemExit(f"canonical_card_coverage:{packet_id}")
        for card in cards.values():
            validate_card(card, packet_id)
        canonical_by_packet[packet_id] = (proposal, proposal_path, audit_path)

    c3_by_packet: dict[str, dict[str, Any]] = {}
    for ledger_path in args.c3_ledger:
        for packet_id, row in index_unique(read_jsonl(ledger_path), "c2_packet_id", str(ledger_path)).items():
            if packet_id in c3_by_packet:
                raise SystemExit(f"duplicate_c3_packet:{packet_id}")
            c3_by_packet[packet_id] = row

    prompt_by_packet: dict[str, dict[str, Any]] = {}
    for ledger_path in args.prompt_ledger:
        for packet_id, row in index_unique(read_jsonl(ledger_path), "c2_packet_id", str(ledger_path)).items():
            if packet_id in prompt_by_packet:
                raise SystemExit(f"duplicate_prompt_packet:{packet_id}")
            prompt_by_packet[packet_id] = row

    reviewer_rows = {1: [], 2: []}
    # C4B consensus may use the anonymous C4A-card mapping, but not the
    # construction target.  Keep C5 target information in a separate file.
    unpermutation_key: list[dict[str, Any]] = []
    sealed_target_key: list[dict[str, Any]] = []
    included_packet_ids: list[str] = []
    case_index = 0
    failures: list[str] = []

    for packet_id in sorted(canonical_by_packet):
        lineage = lineage_by_packet.get(packet_id)
        if lineage is None:
            failures.append(f"missing_lineage:{packet_id}")
            continue
        proposal, proposal_path, audit_path = canonical_by_packet[packet_id]
        cards = proposal["cards"]
        candidates = lineage.get("candidates")
        c2_packet_ids = lineage.get("c2_packets")
        if not isinstance(candidates, list) or not isinstance(c2_packet_ids, list):
            failures.append(f"lineage_schema:{packet_id}")
            continue
        candidate_by_label = index_unique(candidates, "label", packet_id)
        if set(candidate_by_label) != set(cards):
            failures.append(f"lineage_card_label_mismatch:{packet_id}")
            continue

        for c2_packet_id in sorted(str(value) for value in c2_packet_ids):
            c3_row = c3_by_packet.get(c2_packet_id)
            prompt_row = prompt_by_packet.get(c2_packet_id)
            if c3_row is None or prompt_row is None:
                failures.append(f"missing_c3_or_prompt:{packet_id}:{c2_packet_id}")
                continue
            if c3_row.get("c3_disposition") != C3_ALLOW:
                failures.append(f"c3_not_allowed:{packet_id}:{c2_packet_id}")
                continue
            prompt_text = str(prompt_row.get("prompt_text", ""))
            sealed_target = str(prompt_row.get("sealed_target_source_id", c3_row.get("sealed_target_source_id", "")))
            source_ids = {str(candidate.get("source_id", "")) for candidate in candidates}
            if not prompt_text or sealed_target not in source_ids:
                failures.append(f"prompt_or_target_not_bound:{packet_id}:{c2_packet_id}")
                continue
            case_index += 1
            candidate_labels = list(cards)
            permutations = {index: reviewer_labels(args.seed, case_index, candidate_labels, index) for index in (1, 2)}
            for reviewer_index, order in permutations.items():
                reviewer_packet_id = f"C4B-{case_index:04d}-R{reviewer_index}"
                reviewer_rows[reviewer_index].append({
                    "status": "RQ1B_V3_C4B_KEY_BLIND_ADEQUACY_PACKET_NOT_A_LABEL_OR_RESULT",
                    "review_packet_id": reviewer_packet_id,
                    "prompt_text": prompt_text,
                    "candidate_cards": [
                        {"card_label": f"Candidate {chr(65 + index)}", "card": cards[original_label]}
                        for index, original_label in enumerate(order)
                    ],
                    "allowed_response_labels": [
                        "ONE_FULLY_ADEQUATE",
                        "MULTIPLE_ADEQUATE",
                        "NONE_ADEQUATE",
                        "UNCERTAIN",
                    ],
                    "review_instructions": (
                        "Assess adequacy using only this prompt and these anonymous cards. "
                        "Return ONE_FULLY_ADEQUATE only if exactly one card fully supports the request without a stated boundary conflict; "
                        "otherwise return MULTIPLE_ADEQUATE, NONE_ADEQUATE, or UNCERTAIN. "
                        "For any selected card, cite exact excerpts from the card. Do not infer source identity or a hidden target."
                    ),
                    "exclusions": [
                        "No source title, URL, repository, source identifier, candidate identity, sealed target, selector output, embedding, metric, or other review is present."
                    ],
                })
                unpermutation_key.append({
                    "review_packet_id": reviewer_packet_id,
                    "c4a_packet_id": packet_id,
                    "composition_id": lineage.get("composition_id"),
                    "card_key": [
                        {
                            "review_card_label": f"Candidate {chr(65 + index)}",
                            "canonical_card_label": original_label,
                        }
                        for index, original_label in enumerate(order)
                    ],
                    "canonical_proposal_sha256": sha256(proposal_path),
                    "canonical_audit_sha256": sha256(audit_path),
                    "status": "RQ1B_V3_C4B_UNPERMUTATION_MAPPING_NOT_A_LABEL_OR_RESULT",
                })
                sealed_target_key.append({
                    "review_packet_id": reviewer_packet_id,
                    "c4a_packet_id": packet_id,
                    "composition_id": lineage.get("composition_id"),
                    "c2_packet_id": c2_packet_id,
                    "prompt_variant": prompt_row.get("variant"),
                    "sealed_target_source_id": sealed_target,
                    "residual_cue_risk": c3_row.get("residual_cue_risk"),
                    "canonical_card_to_source": [
                        {
                            "canonical_card_label": original_label,
                            "source_id": candidate_by_label[original_label].get("source_id"),
                            "source_sha256": candidate_by_label[original_label].get("source_sha256"),
                        }
                        for original_label in order
                    ],
                    "lineage_manifest_path": str(lineage_paths[packet_id]),
                    "status": "RQ1B_V3_C5_SEALED_TARGET_MAPPING_NOT_A_LABEL_OR_RESULT",
                })
            included_packet_ids.append(packet_id)

    output_root = args.output_root
    reviewer_dir = output_root / "reviewer_packets"
    key_dir = output_root / "private_key"
    reviewer_dir.mkdir(parents=True, exist_ok=True)
    key_dir.mkdir(parents=True, exist_ok=True)
    for reviewer_index in (1, 2):
        (reviewer_dir / f"reviewer_{reviewer_index}.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in reviewer_rows[reviewer_index]),
            encoding="utf-8",
        )
    (key_dir / "c4b_unpermutation_key.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in unpermutation_key),
        encoding="utf-8",
    )
    (key_dir / "c5_sealed_target_key.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in sealed_target_key),
        encoding="utf-8",
    )
    report = {
        "status": "RQ1B_V3_C4B_MATERIALISATION_PASS_NOT_A_LABEL_OR_RESULT" if not failures else "RQ1B_V3_C4B_MATERIALISATION_INCOMPLETE_NOT_A_LABEL_OR_RESULT",
        "canonical_packet_count": len(canonical_by_packet),
        "included_c4a_packet_count": len(set(included_packet_ids)),
        "review_packets_per_reviewer": len(reviewer_rows[1]),
        "unpermutation_key_rows": len(unpermutation_key),
        "sealed_target_key_rows": len(sealed_target_key),
        "failures": failures,
        "boundary": "This materialises blind adequacy inputs only. It does not create a C4B judgment, gold label, retrieval input, metric, selector result, or frozen cluster.",
    }
    (output_root / "materialisation_report.json").write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
