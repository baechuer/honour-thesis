#!/usr/bin/env python3
"""Validate that the amended RQ2b prefreeze protocol is internally aligned."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "skill_benchmark" / "outputs" / "rq2b" / "preflight"
PROTOCOL = ROOT / "thesis_notes" / "current" / (
    "RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md"
)
SPEC = ROOT / "thesis_notes" / "current" / (
    "RQ2 Comprehensive Methodology Specification - 2026-07-26.md"
)
TRACKERS = [
    ROOT / "thesis_notes" / "current" / "RQ2 Current Status and Implementation Tracker - 2026-07-26.md",
    ROOT / "thesis_notes" / "current" / "Thesis Progress Tracker.md",
    ROOT / "thesis_notes" / "current" / "Experiment Methodology Tracker.md",
    ROOT / "thesis_notes" / "current" / "Thesis Experiment Roadmap.md",
]
OUTPUT_JSON = PREFLIGHT / "protocol_validation.json"
OUTPUT_MD = PREFLIGHT / "protocol_validation.md"


def require(condition: bool, label: str, errors: list[str]) -> None:
    if not condition:
        errors.append(label)


def main() -> None:
    audit = json.loads((PREFLIGHT / "audit.json").read_text(encoding="utf-8"))
    token = json.loads((PREFLIGHT / "token_limit_audit.json").read_text(encoding="utf-8"))
    precision = json.loads((PREFLIGHT / "precision_audit.json").read_text(encoding="utf-8"))
    protocol = PROTOCOL.read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")
    rereview = (PREFLIGHT / "independent_protocol_rereview.md").read_text(encoding="utf-8")
    tracker_texts = [path.read_text(encoding="utf-8") for path in TRACKERS]
    errors: list[str] = []

    require(audit["pass_preflight"] is True, "source/prompt preflight did not pass", errors)
    require(audit["network_calls"] == 0, "preflight network_calls is not zero", errors)
    require(audit["source_summary"]["skill_count"] == 2433, "skill count is not 2433", errors)
    require(audit["prompt_summary"]["controlled_count"] == 245, "controlled count is not 245", errors)
    require(audit["prompt_summary"]["public_gold_count"] == 144, "public count is not 144", errors)
    require(audit["prompt_summary"]["stress_count"] == 12, "stress count is not 12", errors)
    require(len(audit["legacy_freeze_drift"]["drifted"]) == 47, "legacy drift count is not 47", errors)
    require(len(audit["exact_duplicate_sources"]) == 2, "exact duplicate group count is not 2", errors)

    qwen = token["qwen"]
    reranker = token["skillrouter"]
    require(token["network_calls"] == 0, "token audit network_calls is not zero", errors)
    require(qwen["provider_documented_per_text_limit"] == 8192, "Qwen ceiling is not 8192", errors)
    require(qwen["proposed_chunk_tokens"] == 7500, "Qwen chunk is not 7500", errors)
    require(qwen["proposed_overlap_tokens"] == 256, "Qwen overlap is not 256", errors)
    require(qwen["sources_requiring_proposed_chunking"] == 3, "Qwen chunked-source count is not 3", errors)
    require(reranker["maximum_pair_tokens"] == 2048, "SkillRouter pair limit is not 2048", errors)
    require(reranker["overlap_tokens"] == 128, "SkillRouter overlap is not 128", errors)
    require(reranker["minimum_document_window_budget"] == 1699, "SkillRouter minimum budget is not 1699", errors)
    require(
        reranker["prompt_contract_sha256"]
        == "face140f238119fc19ba12de90131d1031ada388f08f73e641d0dffd6a00817e",
        "SkillRouter prompt hash mismatch",
        errors,
    )

    require(precision["network_calls"] == 0, "precision audit network_calls is not zero", errors)
    require(precision["noninferiority_margin"] == 0.03, "precision margin is not 0.03", errors)
    require(precision["grouping_field"] == "prompt_inventory.group", "precision grouping field is stale", errors)
    require(precision["strata"]["controlled"]["group_count"] == 25, "controlled group count is not 25", errors)
    require(precision["strata"]["public_gold"]["group_count"] == 62, "public group count is not 62", errors)

    for hypothesis in ("P1-C", "P1-P", "P2-C", "P2-P", "P3-C", "P3-P", "P4-C", "P4-P"):
        require(hypothesis in protocol, f"missing atomic hypothesis {hypothesis}", errors)
    for phrase in (
        "Qwen max-chunk multi-vector retrieval pipeline",
        "only the evidence quote is selector-visible",
        "grouped paired sign-flip randomization",
        "seed `2026080201`",
        "seed `2026080202`",
        "conditional acceptable Hit@1",
        "re.sub(r\"\\s+\", \" \", evidence.strip())",
        "exact hashed `group` field in `prompt_inventory.jsonl`",
        "Separate explicit I3C text-transfer approval required",
        "end-to-end Hit@1 = Recall@K x conditional Hit@1",
        "No acceptable skill may be added after rankings are inspected",
    ):
        require(phrase in protocol, f"protocol missing: {phrase}", errors)
    require("Final verdict: **PASS**" in rereview, "independent final focused PASS missing", errors)

    require("no category/tag or benchmark metadata" in spec, "spec I1 definition is stale", errors)
    require("Do **not** reuse `benchmark-v0.4-2026-06-16`" in spec, "spec version rule is stale", errors)
    for path, text in zip(TRACKERS, tracker_texts):
        require(
            "PREFREEZE REVIEW COMPLETE / AWAITING USER APPROVAL" in text,
            f"tracker status stale: {path.name}",
            errors,
        )

    report = {
        "schema_version": "rq2b-prefreeze-protocol-validation-v1",
        "state": "prefreeze_validation_not_approval_not_result",
        "network_calls": 0,
        "pass_validation": not errors,
        "errors": errors,
        "check_families": 6,
    }
    OUTPUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# RQ2b Prefreeze Protocol Validation",
        "",
        "This is local consistency validation, not user approval and not a scientific result.",
        "",
        f"- Status: {'PASS' if not errors else 'FAIL'}",
        f"- Check families: {report['check_families']}",
        "- Network calls: 0",
    ]
    if errors:
        lines.extend(["", "## Errors", "", *[f"- {error}" for error in errors]])
    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
