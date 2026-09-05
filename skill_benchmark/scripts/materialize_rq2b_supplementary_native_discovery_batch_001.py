#!/usr/bin/env python3
"""Materialise the first bounded supplementary RQ2-native source-reading queue.

This is deliberately a source-visible navigation artifact.  It never admits a
candidate, cluster, prompt, label, representation, selector input, or metric.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
NAVIGATION = BASE / (
    "manifests/rq2b_native_discovery_universe_live_reconciled_2026-08-31/"
    "rq2_native_source_navigation.jsonl"
)
CURRENT_UNION = BASE / (
    "manifests/current_pre_freeze_consolidated_2026-08-31/"
    "canonical_candidate_union_current_pre_freeze.jsonl"
)
PROTOCOL = BASE / "review/USER_AUTHORIZED_SUPPLEMENTARY_RQ2_NATIVE_DISCOVERY_PROTOCOL_2026-09-03.md"
OUTPUT = BASE / "candidates/rq2_native_supplementary_discovery_batch_001_2026-09-03.jsonl"
SUMMARY = BASE / "candidates/rq2_native_supplementary_discovery_batch_001_2026-09-03_summary.json"


# Every row is a source-visible *hypothesis*, deliberately not an assertion that
# the sources form a valid cluster.  The subsequent full-source screen must
# reject hierarchy, composition, duplicate, provenance, licence, and cue risks.
FAMILIES: list[dict[str, Any]] = [
    {
        "family_id": "SUPP-NATIVE-B001-01",
        "envelope_hypothesis": "scope a security assessment of software change or code",
        "contrast_hypothesis": "whole-codebase audit versus architecture-aware review versus change-scoped scan",
        "source_ids": ["RQ1B-V3-SRC-000003", "RQ1B-V3-SRC-000018", "RQ1B-V3-SRC-000199"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-02",
        "envelope_hypothesis": "select an automated application-security scan for a defined software risk surface",
        "contrast_hypothesis": "custom static rule scan versus multi-language SAST versus dependency/supply-chain scan",
        "source_ids": ["RQ1B-V3-SRC-000338", "RQ1B-V3-SRC-000395", "RQ1B-V3-SRC-000412"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-03",
        "envelope_hypothesis": "identify an exposure route before a software release",
        "contrast_hypothesis": "hard-coded credential scan versus public-client leak audit versus AI-agent configuration audit",
        "source_ids": ["RQ1B-V3-SRC-000250", "RQ1B-V3-SRC-000287", "RQ1B-V3-SRC-000152"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-04",
        "envelope_hypothesis": "respond to a production alert with evidence and safe escalation",
        "contrast_hypothesis": "alert diagnosis versus broad incident response versus agent-led on-call triage",
        "source_ids": ["RQ1B-V3-SRC-000504", "RQ1B-V3-SRC-000510", "RQ1B-V3-SRC-000573"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-05",
        "envelope_hypothesis": "preserve operational context around a production incident",
        "contrast_hypothesis": "service recovery versus runbook authoring versus shift handoff",
        "source_ids": ["RQ1B-V3-W21-SRC-0045", "RQ1B-V3-SRC-000190", "RQ1B-V3-SRC-000445"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-06",
        "envelope_hypothesis": "find weaknesses in an existing automated test suite",
        "contrast_hypothesis": "mutation survival versus missing-line coverage versus test-driven-development review",
        "source_ids": ["RQ1B-V3-SRC-001089", "RQ1B-V3-SRC-000047", "RQ1B-V3-SRC-001487"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-07",
        "envelope_hypothesis": "plan or check broad software-test assurance",
        "contrast_hypothesis": "test-plan design versus generic test implementation versus regression-sweep review",
        "source_ids": ["RQ1B-V3-SRC-000074", "RQ1B-V3-SRC-000450", "RQ1B-V3-SRC-001254"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-08",
        "envelope_hypothesis": "establish confidence in data-pipeline correctness",
        "contrast_hypothesis": "expectation-based data tests versus cross-source reconciliation versus DataOps quality gates",
        "source_ids": ["RQ1B-V3-SRC-000742", "RQ1B-V3-SRC-000126", "RQ1B-V3-SRC-000866"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-09",
        "envelope_hypothesis": "define a reliable data-engineering workflow under quality constraints",
        "contrast_hypothesis": "freshness/SLA ownership versus language-agnostic correctness reasoning versus end-to-end pipeline delivery",
        "source_ids": ["RQ1B-V3-SRC-000192", "RQ1B-V3-SRC-000991", "RQ1B-V3-SRC-001430"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-10",
        "envelope_hypothesis": "change a production database without unacceptable downtime or rollback risk",
        "contrast_hypothesis": "Postgres-specific online migration versus general staged migration planning versus ORM/schema migration patterns",
        "source_ids": ["RQ1B-V3-SRC-000877", "RQ1B-V3-SRC-000268", "RQ1B-V3-SRC-000095"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-11",
        "envelope_hypothesis": "define or evolve an API contract for external consumers",
        "contrast_hypothesis": "design-first specification versus gateway contract governance versus REST/GraphQL versioning",
        "source_ids": ["RQ1B-V3-SRC-000038", "RQ1B-V3-SRC-000682", "RQ1B-V3-SRC-000689"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-12",
        "envelope_hypothesis": "make a breaking API change safely",
        "contrast_hypothesis": "schema-diff changelog versus code/API migration versus external API integration work",
        "source_ids": ["RQ1B-V3-SRC-000059", "RQ1B-V3-SRC-000254", "RQ1B-V3-SRC-000361"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-13",
        "envelope_hypothesis": "recover structured content from complex or scanned PDFs",
        "contrast_hypothesis": "layout-aware PDF parser versus PDF-to-Markdown conversion versus OCR document parsing",
        "source_ids": ["RQ1B-V3-W13-SRC-0014", "RQ1B-V3-SRC-001350", "RQ1B-V3-SRC-001934"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-14",
        "envelope_hypothesis": "transform a document artifact into a required output format",
        "contrast_hypothesis": "Pandoc format conversion versus document-processing API versus PDF-specific tool choice",
        "source_ids": ["RQ1B-V3-W13-SRC-0019", "RQ1B-V3-SRC-000177", "RQ1B-V3-SRC-001722"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-15",
        "envelope_hypothesis": "find and synthesise academic literature for a bounded research question",
        "contrast_hypothesis": "domain literature review versus scholarly search/metrics versus structured research summarisation",
        "source_ids": ["RQ1B-V3-W25-SRC-0006", "RQ1B-V3-SRC-000430", "RQ1B-V3-W9-SRC-0013"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-16",
        "envelope_hypothesis": "research an external question and deliver a sourced synthesis",
        "contrast_hypothesis": "multi-mode research investigation versus general research analysis versus web research synthesis",
        "source_ids": ["RQ1B-V3-SRC-000063", "RQ1B-V3-SRC-000080", "RQ1B-V3-SRC-000581"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-17",
        "envelope_hypothesis": "evaluate an LLM or agent system with operational feedback",
        "contrast_hypothesis": "general agent-evaluation design versus Arize evaluator workflow versus LangSmith online evaluation",
        "source_ids": ["RQ1B-V3-SRC-000084", "RQ1B-V3-SRC-000106", "RQ1B-V3-SRC-000554"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-18",
        "envelope_hypothesis": "assess compliance risk before release or audit",
        "contrast_hypothesis": "evidence-oriented checklist versus broad compliance scan versus software-licence compliance audit",
        "source_ids": ["RQ1B-V3-SRC-000163", "RQ1B-V3-SRC-000292", "RQ1B-V3-SRC-000133"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-19",
        "envelope_hypothesis": "improve accessibility of a user-facing application",
        "contrast_hypothesis": "web WCAG review versus Android-specific accessibility review versus responsive accessibility design",
        "source_ids": ["RQ1B-V3-SRC-000257", "RQ1B-V3-W9-SRC-0043", "RQ1B-V3-SRC-001426"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-20",
        "envelope_hypothesis": "review a digital interface against user-experience requirements",
        "contrast_hypothesis": "brief-and-codebase design critique versus phased UI/UX review versus cross-platform UX audit",
        "source_ids": ["RQ1B-V3-SRC-000077", "RQ1B-V3-SRC-000115", "RQ1B-V3-W26-SRC-0146"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-21",
        "envelope_hypothesis": "diagnose and verify a web application's performance problem",
        "contrast_hypothesis": "cross-stack performance optimisation versus automated web-vitals gate versus framework-specific performance audit",
        "source_ids": ["RQ1B-V3-W9-SRC-0025", "RQ1B-V3-SRC-000285", "RQ1B-V3-SRC-000114"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-22",
        "envelope_hypothesis": "improve organic search performance of an existing site",
        "contrast_hypothesis": "content-portfolio audit versus on-page audit versus phased SEO roadmap",
        "source_ids": ["RQ1B-V3-SRC-000021", "RQ1B-V3-SRC-000808", "RQ1B-V3-SRC-000759"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-23",
        "envelope_hypothesis": "analyse a market or competitor landscape for a product decision",
        "contrast_hypothesis": "product research synthesis versus market-research planning versus tool-mediated competitive intelligence",
        "source_ids": ["RQ1B-V3-SRC-000248", "RQ1B-V3-SRC-000375", "RQ1B-V3-SRC-000870"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-24",
        "envelope_hypothesis": "assess and remediate a cloud-production operational problem",
        "contrast_hypothesis": "general AWS diagnosis versus ECS operational review versus cloud-server management",
        "source_ids": ["RQ1B-V3-SRC-000105", "RQ1B-V3-SRC-000396", "RQ1B-V3-SRC-000020"],
    },
    {
        "family_id": "SUPP-NATIVE-B001-25",
        "envelope_hypothesis": "diagnose a slow relational-database query or workload",
        "contrast_hypothesis": "SQL query optimisation versus execution-plan/index strategy versus PostgreSQL operations diagnosis",
        "source_ids": ["RQ1B-V3-SRC-001072", "RQ1B-V3-SRC-001418", "RQ1B-V3-W31-SRC-0094"],
    },
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    required = [NAVIGATION, CURRENT_UNION, PROTOCOL]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required inputs: {missing}")

    navigation_rows = read_jsonl(NAVIGATION)
    navigation_by_id = {str(row["source_id"]): row for row in navigation_rows}
    if len(navigation_by_id) != len(navigation_rows):
        raise SystemExit("Navigation manifest contains duplicate source IDs")
    current_hashes = {str(row["canonical_source_sha256"]) for row in read_jsonl(CURRENT_UNION)}
    if len(current_hashes) != 3094:
        raise SystemExit("Current candidate union is not the expected 3,094-source checkpoint")

    family_ids = [str(row["family_id"]) for row in FAMILIES]
    selected_ids = [source_id for family in FAMILIES for source_id in family["source_ids"]]
    if len(FAMILIES) != 25 or len(set(family_ids)) != 25:
        raise SystemExit("Exactly 25 unique source-reading family leads are required")
    if len(selected_ids) != 75 or len(set(selected_ids)) != 75:
        raise SystemExit("Each three-member source lead must be source-disjoint in Batch 001")

    output_rows: list[dict[str, Any]] = [{
        "record_type": "batch_scope",
        "batch_id": "RQ2-NATIVE-SUPPLEMENTARY-B001-2026-09-03",
        "method": "source-visible contrast-family navigation only",
        "input_navigation_source_count": len(navigation_rows),
        "current_candidate_union_count": len(current_hashes),
        "selected_family_count": len(FAMILIES),
        "selected_source_appearance_count": len(selected_ids),
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "explicit_exclusions": [
            "admission", "prompt authoring", "gold/acceptable labels", "selector/reranker output",
            "embeddings", "metrics", "representation extraction", "thesis results",
        ],
        "claim_boundary": "A family is a full-source reading hypothesis, not a semantic cluster or candidate-library admission.",
    }]
    origin_counts: Counter[str] = Counter()
    root_counts: Counter[str] = Counter()
    source_hashes: set[str] = set()
    for family in FAMILIES:
        candidates: list[dict[str, Any]] = []
        for source_id in family["source_ids"]:
            if source_id not in navigation_by_id:
                raise SystemExit(f"Selected source is absent from the bound navigation frame: {source_id}")
            source = navigation_by_id[source_id]
            source_hash = str(source["source_sha256"])
            if source_hash in current_hashes:
                raise SystemExit(f"Selected source is already in the current candidate union: {source_id}")
            source_path = Path(str(source["source_path"]))
            if not source_path.is_file() or sha256_file(source_path) != source_hash:
                raise SystemExit(f"Source-byte replay failed: {source_id}")
            source_hashes.add(source_hash)
            origin_counts[str(source["origin_key"])] += 1
            root_counts[str(source["source_root"])] += 1
            candidates.append({
                "source_id": source_id,
                "source_sha256": source_hash,
                "source_path": str(source_path),
                "source_name": source.get("source_name"),
                "source_description": source.get("source_description"),
                "heading_preview": source.get("heading_preview"),
                "origin_key": source.get("origin_key"),
                "source_root": source.get("source_root"),
                "repository_ref": source.get("repository_ref"),
                "licence_disposition_at_navigation": source.get("licence_disposition"),
                "source_byte_replay": "PASS_SHA256_MATCH",
                "status": "SOURCE_READING_LEAD_NOT_AN_ADMITTED_CANDIDATE",
            })
        output_rows.append({
            "record_type": "contrast_family_lead",
            "batch_id": "RQ2-NATIVE-SUPPLEMENTARY-B001-2026-09-03",
            **family,
            "candidates": candidates,
            "required_next_gate": (
                "Read all preserved sources; establish a bounded common envelope and pairwise operational contrast; "
                "then pass provenance/licence, cue-safe authoring and target-blinded adequacy gates before any admission."
            ),
            "status": "SOURCE_VISIBLE_HYPOTHESIS_PENDING_FULL_SOURCE_SCREEN",
        })

    if len(source_hashes) != 75:
        raise SystemExit("The batch must contain 75 source-hash-unique candidates")
    write_jsonl(OUTPUT, output_rows)
    summary = {
        "status": "PASS_SUPPLEMENTARY_RQ2_NATIVE_BATCH_001_SOURCE_READING_QUEUE_NOT_A_CLUSTER_OR_RESULT",
        "selected_family_count": len(FAMILIES),
        "selected_source_appearance_count": len(selected_ids),
        "selected_source_hash_count": len(source_hashes),
        "origin_count": len(origin_counts),
        "source_root_counts": dict(sorted(root_counts.items())),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {str(OUTPUT.relative_to(ROOT)): sha256_file(OUTPUT)},
        "claim_boundary": [
            "All 75 candidates are outside the current 3,094-source candidate union and pass local source-byte replay.",
            "The 25 contrast families are navigation hypotheses only; no family is a valid cluster until full-source screening passes.",
            "Missing or insufficient provenance/licence, hierarchy, composition, near-duplication, cue leakage, or failed blind adequacy review blocks admission.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
