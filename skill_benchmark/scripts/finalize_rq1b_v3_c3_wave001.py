#!/usr/bin/env python3
"""Freeze RQ1b V3 Wave 001 C3 cue dispositions after mechanical recheck."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-c3-wave001-finaliser-v1"
BOUNDARY = (
    "C3 records cue control and residual cue risk only. It is not a cue-safety proof, "
    "strict gold label, C4 adequacy decision, selector input, metric, or routing result."
)
RISK_BY_TARGET = {
    ("RQ1B-V3-D1-C1-W1-001", "RQ1B-V3-SRC-019877"): (
        "high",
        "PDF-to-Markdown is a genuine mutually exclusive input/output constraint. The residual risk is operational, not accidental source leakage.",
    ),
    ("RQ1B-V3-D1-C1-W1-001", "RQ1B-V3-SRC-025411"): (
        "high",
        "DOCX-to-Markdown is a genuine mutually exclusive input/output constraint. The residual risk is operational, not accidental source leakage.",
    ),
    ("RQ1B-V3-D1-C1-W1-001", "RQ1B-V3-SRC-027887"): (
        "high",
        "XLSX-to-Markdown is a genuine mutually exclusive input/output constraint. The residual risk is operational, not accidental source leakage.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-001", "RQ1B-V3-SRC-026295"): (
        "medium",
        "The confidentiality-agreement domain and review topics are genuine constraints with moderate route-identification risk.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-001", "RQ1B-V3-SRC-003741"): (
        "high",
        "Represented side, outsourcing context, one-table-only output and graded legal risk form a strongly identifying but genuine workflow/output bundle.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-001", "RQ1B-V3-SRC-026070"): (
        "high",
        "Transaction document set and function-level post-closing service comparison are strongly identifying but genuine operational constraints.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-002", "RQ1B-V3-SRC-000006"): (
        "medium",
        "Python, labelled tabular input, static exploratory figure and image export are genuine constraints with medium route-identification risk.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-002", "RQ1B-V3-SRC-010026"): (
        "high",
        "The R/publication-vector-PDF/faceted-comparison/font-portability bundle is a strongly identifying but genuine constraint bundle.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-002", "RQ1B-V3-SRC-012750"): (
        "high",
        "Interactive browser behaviour, point inspection, navigation and image export are strongly identifying but genuine interface/output constraints.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-003", "RQ1B-V3-SRC-019213"): (
        "high",
        "Native editable PPTX output and presenter notes are strongly identifying but genuine deliverable constraints.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-003", "RQ1B-V3-SRC-019694"): (
        "high",
        "Blank hosted-presentation creation and return of the created object are strongly identifying but genuine interface constraints.",
    ),
    ("RQ1B-V3-D1-C1-W4R1-003", "RQ1B-V3-SRC-011582"): (
        "high",
        "Browser HTML output and adaptation of a supplied project starter are strongly identifying but genuine artifact/workspace constraints.",
    ),
}
ALLOWED_TITLE_HIT_PACKETS = {"RQ1B-V3-D1-C1-W1-001-C2-019877-direct"}
ALLOWED_SHORT_NAME_HIT_PACKETS = {
    "RQ1B-V3-D1-C1-W4R1-003-019213-direct",
    "RQ1B-V3-D1-C1-W4R1-003-019213-paraphrase",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-ledger", type=Path, required=True)
    parser.add_argument("--mechanical-inventory", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.ledger.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_final_c3")

    c2_rows = read_jsonl(args.c2_ledger)
    inventory = json.loads(args.mechanical_inventory.read_text(encoding="utf-8"))
    inventory_by_packet = {str(row["c2_packet_id"]): row for row in inventory["records"]}
    c2_ids = {str(row["c2_packet_id"]) for row in c2_rows}
    if set(inventory_by_packet) != c2_ids:
        raise SystemExit("mechanical_inventory_coverage_mismatch")
    if inventory.get("failures"):
        raise SystemExit("mechanical_inventory_has_failures")

    final_rows: list[dict[str, Any]] = []
    for c2 in c2_rows:
        packet_id = str(c2["c2_packet_id"])
        inventory_record = inventory_by_packet[packet_id]
        key = (str(c2["c1_review_id"]), str(c2["sealed_target_source_id"]))
        if key not in RISK_BY_TARGET:
            raise SystemExit(f"missing_risk_mapping:{key[0]}:{key[1]}")
        if c2.get("c2_disposition") != "C2_DRAFT_FOR_C3":
            raise SystemExit(f"unexpected_c2_disposition:{packet_id}")
        if inventory_record["source_phrase_hits"]:
            raise SystemExit(f"unresolved_source_phrase_hit:{packet_id}")
        if inventory_record["title_phrase_hits"] and packet_id not in ALLOWED_TITLE_HIT_PACKETS:
            raise SystemExit(f"unapproved_title_phrase_hit:{packet_id}")
        if inventory_record["short_source_name_token_hits"] and packet_id not in ALLOWED_SHORT_NAME_HIT_PACKETS:
            raise SystemExit(f"unapproved_short_name_hit:{packet_id}")
        risk, rationale = RISK_BY_TARGET[key]
        final_rows.append({
            "c2_packet_id": packet_id,
            "c1_review_id": c2["c1_review_id"],
            "sealed_target_source_id": c2["sealed_target_source_id"],
            "variant": c2["variant"],
            "c3_disposition": "C3_ALLOW_C4_WITH_RISK_ANNOTATION",
            "residual_cue_risk": risk,
            "manual_rationale": rationale,
            "mechanical_title_phrase_hits": inventory_record["title_phrase_hits"],
            "mechanical_short_name_token_hits": inventory_record["short_source_name_token_hits"],
            "mechanical_source_phrase_hits": inventory_record["source_phrase_hits"],
            "cue_only_revision_applied": bool(c2.get("c3_cue_revision")),
            "review_mode": "independent source-aware C3 cue review plus principal integration; no C4 adequacy judgment",
            "claim_boundary": BOUNDARY,
        })

    final_rows.sort(key=lambda row: row["c2_packet_id"])
    args.ledger.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in final_rows),
        encoding="utf-8",
    )
    risk_counts = Counter(row["residual_cue_risk"] for row in final_rows)
    audit = {
        "status": "C3_FINAL_CUE_GATE_PASS_NOT_A_LABEL_OR_RESULT",
        "version": VERSION,
        "packet_count": len(final_rows),
        "allow_c4_count": sum(row["c3_disposition"] == "C3_ALLOW_C4_WITH_RISK_ANNOTATION" for row in final_rows),
        "risk_counts": dict(sorted(risk_counts.items())),
        "cue_only_revision_count": sum(row["cue_only_revision_applied"] for row in final_rows),
        "c2_ledger_sha256": sha256_file(args.c2_ledger),
        "mechanical_inventory_sha256": sha256_file(args.mechanical_inventory),
        "final_ledger_sha256": sha256_file(args.ledger),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
        "exclusions": [
            "C4 adequacy review, gold labels, selector input, model/API calls, metrics and retrieval results remain unperformed.",
        ],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
