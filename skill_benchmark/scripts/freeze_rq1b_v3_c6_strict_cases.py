#!/usr/bin/env python3
"""Freeze lineage-validated RQ1b V3 C6 strict prompt cases with cue strata.

The C6 output intentionally reports prompt cases and parent-composition
coverage separately.  A parent triad is not counted as fully covered unless
all of its C3-allowed target/variant packets survived C4B and C5.  This is
curation provenance only, never a selector run or a field-effect result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


C5_PASS = "RQ1B_V3_C5_TARGET_RECONCILIATION_PASS_NOT_FROZEN"
C5_CONSISTENT = "RQ1B_V3_C5_TARGET_CONSISTENT_STRICT_GOLD_CANDIDATE_NOT_FROZEN"
C5_NO_SINGLETON = "RQ1B_V3_C5_NO_STRICT_C4B_SINGLETON_NOT_A_GOLD_LABEL"
C3_ALLOW = "C3_ALLOW_C4_WITH_RISK_ANNOTATION"
C4B_PASS = "RQ1B_V3_C4B_CONSENSUS_AUDIT_PASS_NOT_A_LABEL_OR_RESULT"
BLINDNESS_PASS = "RQ1B_V3_C4B_BLINDNESS_AUDIT_PASS_NOT_A_RESULT"
C4A_ACCEPT = "RQ1B_V3_C4A_CONFORMANCE_ACCEPT_CANONICAL_CARD_NOT_A_RESULT"
C4A_AUDIT_PASS = "RQ1B_V3_C4A_CANONICAL_CARD_AUDIT_PASS"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"jsonl_row_not_object:{path}:{number}")
            rows.append(value)
    return rows


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index_unique(rows: list[dict[str, Any]], field: str, source: str) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = str(row.get(field, ""))
        if not value or value in output:
            raise ValueError(f"duplicate_or_missing_{field}:{source}:{value}")
        output[value] = row
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lineage-manifest", type=Path, action="append", required=True)
    parser.add_argument("--canonical-proposal", type=Path, action="append", required=True)
    parser.add_argument("--canonical-audit", type=Path, action="append", required=True)
    parser.add_argument("--c3-ledger", type=Path, action="append", required=True)
    parser.add_argument("--prompt-ledger", type=Path, action="append", required=True)
    parser.add_argument("--blindness-audit", type=Path, required=True)
    parser.add_argument("--c4b-consensus", type=Path, required=True)
    parser.add_argument("--c5-reconciliation", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    blindness = read_json(args.blindness_audit)
    c4b = read_json(args.c4b_consensus)
    c5 = read_json(args.c5_reconciliation)
    if blindness.get("status") != BLINDNESS_PASS:
        raise SystemExit("blindness_audit_not_pass")
    if c4b.get("status") != C4B_PASS:
        raise SystemExit("c4b_consensus_not_pass")
    if c5.get("status") != C5_PASS:
        raise SystemExit("c5_reconciliation_not_pass")

    lineage_by_packet: dict[str, dict[str, Any]] = {}
    for path in args.lineage_manifest:
        rows = read_json(path)
        if not isinstance(rows, list):
            raise SystemExit(f"lineage_not_list:{path}")
        for row in rows:
            packet_id = str(row.get("packet_id", ""))
            if not packet_id or packet_id in lineage_by_packet:
                raise SystemExit(f"duplicate_or_missing_lineage_packet:{packet_id}")
            lineage_by_packet[packet_id] = row

    canonical_by_packet: dict[str, tuple[dict[str, Any], dict[str, Any], Path, Path]] = {}
    if len(args.canonical_proposal) != len(args.canonical_audit):
        raise SystemExit("canonical_input_count_mismatch")
    for proposal_path, audit_path in zip(args.canonical_proposal, args.canonical_audit):
        proposal, audit = read_json(proposal_path), read_json(audit_path)
        packet_id = str(proposal.get("packet_id", ""))
        if proposal.get("status") != C4A_ACCEPT or audit.get("status") != C4A_AUDIT_PASS or audit.get("packet_id") != packet_id:
            raise SystemExit(f"canonical_not_valid:{packet_id}")
        canonical_by_packet[packet_id] = (proposal, audit, proposal_path, audit_path)

    c3_by_packet: dict[str, dict[str, Any]] = {}
    c3_digest_to_path: dict[str, Path] = {}
    for path in args.c3_ledger:
        c3_digest_to_path[digest(path)] = path
        for packet_id, row in index_unique(read_jsonl(path), "c2_packet_id", str(path)).items():
            if packet_id in c3_by_packet:
                raise SystemExit(f"duplicate_c3_packet:{packet_id}")
            c3_by_packet[packet_id] = row
    prompt_by_packet: dict[str, dict[str, Any]] = {}
    for path in args.prompt_ledger:
        for packet_id, row in index_unique(read_jsonl(path), "c2_packet_id", str(path)).items():
            if packet_id in prompt_by_packet:
                raise SystemExit(f"duplicate_prompt_packet:{packet_id}")
            prompt_by_packet[packet_id] = row

    c4b_by_case = index_unique(c4b.get("consensus", []), "case_id", "c4b_consensus")
    failures: list[str] = []
    frozen: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    frozen_by_composition: dict[str, set[str]] = defaultdict(set)

    for row in c5.get("reconciliation", []):
        case = str(row.get("case_id", ""))
        composition_id = str(row.get("composition_id", ""))
        c2_packet_id = str(row.get("c2_packet_id", ""))
        packet_id = f"C4A-{composition_id}"
        lineage = lineage_by_packet.get(packet_id)
        canonical = canonical_by_packet.get(packet_id)
        if lineage is None or canonical is None:
            failures.append(f"missing_lineage_or_canonical:{case}:{packet_id}")
            continue
        c3_row, prompt_row, c4b_row = c3_by_packet.get(c2_packet_id), prompt_by_packet.get(c2_packet_id), c4b_by_case.get(case)
        if c3_row is None or prompt_row is None or c4b_row is None:
            failures.append(f"missing_c3_prompt_or_c4b:{case}")
            continue
        if c3_row.get("c3_disposition") != C3_ALLOW or not str(prompt_row.get("prompt_text", "")):
            failures.append(f"c3_or_prompt_not_valid:{case}")
            continue
        if c2_packet_id not in {str(value) for value in lineage.get("c2_packets", [])}:
            failures.append(f"c2_not_bound_to_lineage:{case}")
            continue
        if str(row.get("residual_cue_risk")) != str(c3_row.get("residual_cue_risk")):
            failures.append(f"cue_risk_mismatch:{case}")
            continue
        expected_c3_digest = str(lineage.get("c3_packet_ledger_sha256", ""))
        if expected_c3_digest not in c3_digest_to_path:
            failures.append(f"c3_ledger_hash_not_bound:{case}")
            continue
        c1_path = Path(str(lineage.get("c1_ledger_path", "")))
        if not c1_path.is_file() or digest(c1_path) != str(lineage.get("c1_ledger_sha256", "")):
            failures.append(f"c1_ledger_hash_not_bound:{case}")
            continue
        candidate_hashes = []
        for candidate in lineage.get("candidates", []):
            original = Path(str(candidate.get("original_path", "")))
            expected_hash = str(candidate.get("source_sha256", ""))
            if not original.is_file() or digest(original) != expected_hash:
                failures.append(f"candidate_source_hash_not_bound:{case}:{candidate.get('label')}")
            candidate_hashes.append({"source_id": candidate.get("source_id"), "source_sha256": expected_hash})
        if any(item.startswith(f"candidate_source_hash_not_bound:{case}:") for item in failures):
            continue
        if row.get("disposition") == C5_CONSISTENT:
            if c4b_row.get("disposition") != "RQ1B_V3_C4B_STRICT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT":
                failures.append(f"c5_c4b_disposition_mismatch:{case}")
                continue
            proposal, audit, proposal_path, audit_path = canonical
            frozen.append({
                "status": "RQ1B_V3_C6_FROZEN_STRICT_CASE_WITH_CUE_STRATUM_NOT_A_RETRIEVAL_RESULT",
                "case_id": case,
                "composition_id": composition_id,
                "c2_packet_id": c2_packet_id,
                "prompt_variant": prompt_row.get("variant"),
                "prompt_sha256": hashlib.sha256(str(prompt_row.get("prompt_text", "")).encode("utf-8")).hexdigest(),
                "strict_gold_source_id": row.get("sealed_target_source_id"),
                "selected_canonical_card": row.get("canonical_selected_card"),
                "residual_cue_risk": row.get("residual_cue_risk"),
                "candidate_source_hashes": candidate_hashes,
                "c1_ledger_sha256": lineage.get("c1_ledger_sha256"),
                "c3_ledger_sha256": expected_c3_digest,
                "canonical_card_sha256": digest(proposal_path),
                "canonical_card_audit_sha256": digest(audit_path),
                "c4b_consensus_sha256": digest(args.c4b_consensus),
                "c5_reconciliation_sha256": digest(args.c5_reconciliation),
                "boundary": "Frozen strict curation case only. Cue risk remains a reporting stratum; this is not a selector, field-effect, or routing result.",
            })
            frozen_by_composition[composition_id].add(c2_packet_id)
        elif row.get("disposition") == C5_NO_SINGLETON:
            exclusions.append({
                "case_id": case,
                "composition_id": composition_id,
                "c2_packet_id": c2_packet_id,
                "residual_cue_risk": row.get("residual_cue_risk"),
                "reason": "no_strict_c4b_singleton",
                "status": "RQ1B_V3_C6_EXCLUDED_NOT_A_STRICT_CASE",
            })
        else:
            exclusions.append({
                "case_id": case,
                "composition_id": composition_id,
                "c2_packet_id": c2_packet_id,
                "residual_cue_risk": row.get("residual_cue_risk"),
                "reason": str(row.get("disposition")),
                "status": "RQ1B_V3_C6_EXCLUDED_NOT_A_STRICT_CASE",
            })

    coverage: list[dict[str, Any]] = []
    for packet_id, lineage in sorted(lineage_by_packet.items()):
        composition_id = str(lineage.get("composition_id", ""))
        if packet_id not in canonical_by_packet:
            continue
        expected = {str(value) for value in lineage.get("c2_packets", [])}
        observed = frozen_by_composition.get(composition_id, set())
        coverage.append({
            "composition_id": composition_id,
            "c4a_packet_id": packet_id,
            "expected_c3_allowed_case_count": len(expected),
            "frozen_strict_case_count": len(observed),
            "all_target_variant_cases_strict": observed == expected,
            "status": "RQ1B_V3_C6_PARENT_COMPOSITION_COVERAGE_NOT_A_RETRIEVAL_RESULT",
        })

    output_root = args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "c6_frozen_strict_cases.jsonl").write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in frozen), encoding="utf-8")
    (output_root / "c6_exclusions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in exclusions), encoding="utf-8")
    (output_root / "c6_parent_composition_coverage.jsonl").write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in coverage), encoding="utf-8")
    report = {
        "status": "RQ1B_V3_C6_FREEZE_PASS_NOT_A_RETRIEVAL_RESULT" if not failures else "RQ1B_V3_C6_FREEZE_FAIL_NOT_A_RETRIEVAL_RESULT",
        "frozen_strict_case_count": len(frozen),
        "excluded_case_count": len(exclusions),
        "parent_compositions_with_any_frozen_case": sum(row["frozen_strict_case_count"] > 0 for row in coverage),
        "parent_compositions_complete_all_target_variant_cases": sum(row["all_target_variant_cases_strict"] for row in coverage),
        "frozen_case_cue_risk_counts": dict(sorted(Counter(str(row["residual_cue_risk"]) for row in frozen).items())),
        "failures": sorted(set(failures)),
        "boundary": "C6 freezes strict source-card curation with explicit cue strata. It does not establish ecological validity, field causality, retrieval performance, or a thesis result.",
    }
    (output_root / "c6_freeze_report.json").write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
