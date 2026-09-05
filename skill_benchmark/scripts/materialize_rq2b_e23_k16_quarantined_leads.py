#!/usr/bin/env python3
"""Extract quarantined source-reading leads from rejected E23 K=16 tails.

The output is deliberately not a cluster, prompt, candidate admission,
acceptable-set, selector, or metric artifact.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NC_ROOT = ROOT / "rq2b_naturalistic_confusability"
CALIBRATION_DIR = NC_ROOT / "manifests/background_corpus_k_calibration_2026-09-03"
PAIR_REGISTER = CALIBRATION_DIR / "calibration_pair_register_internal.jsonl"
REVIEW_DIR = NC_ROOT / "review/background_corpus_k_calibration_reviews_2026-09-03"
DECISION = REVIEW_DIR / "k_selection/k_selection_decision.json"
RECONCILED = REVIEW_DIR / "k_selection/reconciled_calibration_outcomes.jsonl"
OUTPUT = REVIEW_DIR / "quarantined_k16_post_k_positive_leads.jsonl"
SUMMARY = REVIEW_DIR / "quarantined_k16_post_k_positive_leads_summary.json"
POSITIVE = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    required = [PAIR_REGISTER, DECISION, RECONCILED]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    if decision.get("status") != "K_SELECTION_HOLD" or decision.get("selected_k") is not None:
        raise SystemExit("Lead extraction is defined only for the E23 K_SELECTION_HOLD result")
    pairs = {str(row["calibration_pair_id"]): row for row in read_jsonl(PAIR_REGISTER)}
    reconciled = read_jsonl(RECONCILED)
    leads = []
    for result in reconciled:
        if result["selected_at_k"]["16"] or result["reconciled_outcome"] not in POSITIVE:
            continue
        pair = pairs.get(str(result["calibration_pair_id"]))
        if pair is None:
            raise SystemExit("Reconciled pair absent from internal register")
        leads.append({
            "record_type": "e23_calibration_post_k16_positive_quarantined_lead",
            "calibration_pair_id": result["calibration_pair_id"],
            "lane_id": result["lane_id"],
            "prompt_id": result["prompt_id"],
            "canonical_source_sha256": result["canonical_source_sha256"],
            "source_paths": pair["source_paths"],
            "final_intake_role": pair["final_intake_role"],
            "reconciled_outcome": result["reconciled_outcome"],
            "tail": result["tail"],
            "discovery_reasons": pair["discovery_reasons"],
            "quarantine_status": "SOURCE_READING_LEAD_ONLY_PENDING_SEPARATE_METHOD_DECISION",
            "claim_boundary": (
                "This record is not a semantic-confusability cluster, source admission, benchmark prompt, "
                "acceptable-set member, final test case, representation, selector output, or metric result."
            ),
        })
    leads.sort(key=lambda row: (row["lane_id"], row["prompt_id"], row["canonical_source_sha256"]))
    if len(leads) != 43 or len({row["calibration_pair_id"] for row in leads}) != 43:
        raise SystemExit("E23 rejected K=16 lead count is not the expected 43 unique pairs")
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in leads:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "status": "PASS_E23_K16_POST_K_POSITIVE_QUARANTINED_LEAD_EXTRACTION_NOT_A_CLUSTER_OR_ADMISSION",
        "bound_inputs": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "counts": {
            "prompt_source_leads": len(leads),
            "unique_source_hashes": len({row["canonical_source_sha256"] for row in leads}),
            "unique_prompts": len({row["prompt_id"] for row in leads}),
            "by_lane": dict(sorted(Counter(row["lane_id"] for row in leads).items())),
            "by_outcome": dict(sorted(Counter(row["reconciled_outcome"] for row in leads).items())),
            "by_final_intake_role": dict(sorted(Counter(row["final_intake_role"] for row in leads).items())),
            "all_are_predeclared_tails": all(row["tail"] for row in leads),
        },
        "output": {"path": str(OUTPUT.relative_to(ROOT)), "sha256": sha256_file(OUTPUT)},
        "claim_boundary": [
            "The E23 K selection remains K_SELECTION_HOLD.",
            "A lead must undergo separate source-grounded cluster, cue-safe prompt, and target-blinded local adequacy procedures before any benchmark use.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
