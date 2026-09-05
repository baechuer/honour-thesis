#!/usr/bin/env python3
"""Compare RQ1b V3 C4B consensus with the separately sealed C5 target key.

Run this only after a structurally valid C4B consensus audit.  The output is a
pre-C6 target-consistency record: it can identify a candidate strict-gold
packet, but cannot freeze a cluster, produce selector input, or report a
retrieval result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


C4B_STRICT = "RQ1B_V3_C4B_STRICT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"json_not_object:{path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    result = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"jsonl_row_not_object:{path}:{number}")
            result.append(value)
    return result


def case_id(packet_id: str) -> str:
    prefix, separator, suffix = packet_id.rpartition("-R")
    if not separator or suffix not in {"1", "2"}:
        raise ValueError(f"invalid_reviewer_packet_id:{packet_id}")
    return prefix


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c4b-consensus", type=Path, required=True)
    parser.add_argument("--sealed-target-key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    consensus = read_json(args.c4b_consensus)
    if consensus.get("status") != "RQ1B_V3_C4B_CONSENSUS_AUDIT_PASS_NOT_A_LABEL_OR_RESULT":
        raise SystemExit("c4b_consensus_not_pass")

    target_by_case: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(args.sealed_target_key):
        target_by_case.setdefault(case_id(str(row.get("review_packet_id", ""))), []).append(row)

    failures: list[str] = []
    reconciled: list[dict[str, Any]] = []
    for row in consensus.get("consensus", []):
        base = str(row.get("case_id", ""))
        key_rows = target_by_case.get(base, [])
        if len(key_rows) != 2:
            failures.append(f"target_pair_coverage:{base}")
            continue
        comparable = [
            (key_row.get("c4a_packet_id"), key_row.get("composition_id"), key_row.get("c2_packet_id"), key_row.get("sealed_target_source_id"), key_row.get("residual_cue_risk"))
            for key_row in key_rows
        ]
        if comparable[0] != comparable[1]:
            failures.append(f"target_pair_mismatch:{base}")
            continue
        _, composition_id, c2_packet_id, sealed_target, cue_risk = comparable[0]
        selected_cards = row.get("canonical_selected_cards", [])
        selected_card = selected_cards[0] if len(selected_cards) == 2 and selected_cards[0] == selected_cards[1] else None
        source_by_card = {
            str(item.get("canonical_card_label")): str(item.get("source_id"))
            for item in key_rows[0].get("canonical_card_to_source", [])
        }
        if row.get("disposition") == C4B_STRICT:
            selected_source = source_by_card.get(str(selected_card))
            if not selected_source:
                failures.append(f"selected_card_not_in_target_mapping:{base}")
                continue
            disposition = (
                "RQ1B_V3_C5_TARGET_CONSISTENT_STRICT_GOLD_CANDIDATE_NOT_FROZEN"
                if selected_source == sealed_target
                else "RQ1B_V3_C5_TARGET_MISMATCH_NOT_A_GOLD_LABEL"
            )
        else:
            selected_source = None
            disposition = "RQ1B_V3_C5_NO_STRICT_C4B_SINGLETON_NOT_A_GOLD_LABEL"
        reconciled.append({
            "case_id": base,
            "composition_id": composition_id,
            "c2_packet_id": c2_packet_id,
            "residual_cue_risk": cue_risk,
            "c4b_disposition": row.get("disposition"),
            "canonical_selected_card": selected_card,
            "selected_source_id": selected_source,
            "sealed_target_source_id": sealed_target,
            "disposition": disposition,
        })

    output = {
        "status": "RQ1B_V3_C5_TARGET_RECONCILIATION_PASS_NOT_FROZEN" if not failures else "RQ1B_V3_C5_TARGET_RECONCILIATION_FAIL_NOT_FROZEN",
        "case_count": len(reconciled),
        "target_consistent_strict_gold_candidate_count": sum(row["disposition"] == "RQ1B_V3_C5_TARGET_CONSISTENT_STRICT_GOLD_CANDIDATE_NOT_FROZEN" for row in reconciled),
        "target_mismatch_count": sum(row["disposition"] == "RQ1B_V3_C5_TARGET_MISMATCH_NOT_A_GOLD_LABEL" for row in reconciled),
        "no_strict_singleton_count": sum(row["disposition"] == "RQ1B_V3_C5_NO_STRICT_C4B_SINGLETON_NOT_A_GOLD_LABEL" for row in reconciled),
        "reconciliation": reconciled,
        "failures": sorted(set(failures)),
        "boundary": "C5 compares C4B consensus with a sealed construction target. Even a target-consistent row is only a strict-gold candidate until C6 lineage validation and freeze.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("status", "case_count", "target_consistent_strict_gold_candidate_count", "target_mismatch_count", "no_strict_singleton_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
