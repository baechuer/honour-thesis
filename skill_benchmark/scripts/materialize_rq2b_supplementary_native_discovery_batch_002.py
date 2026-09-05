#!/usr/bin/env python3
"""Materialise the provenance-first second RQ2 supplementary reading batch.

This is a bounded list of source-visible *contrast-family hypotheses*.  It is
not a cluster, candidate admission, prompt, label, representation, selector,
or result.  Each lead was selected only from the local provenance-first
navigation subset and is source-disjoint from Batch 001.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
PREFILTER = BASE / (
    "manifests/rq2b_native_discovery_provenance_first_prefilter_2026-09-03/"
    "rq2_native_source_navigation_provenance_first_excluding_current_and_b001.jsonl"
)
CURRENT_UNION = BASE / (
    "manifests/current_pre_freeze_consolidated_2026-08-31/"
    "canonical_candidate_union_current_pre_freeze.jsonl"
)
BATCH_001 = BASE / "candidates/rq2_native_supplementary_discovery_batch_001_2026-09-03.jsonl"
PROTOCOL = BASE / "review/USER_AUTHORIZED_SUPPLEMENTARY_RQ2_NATIVE_DISCOVERY_PROTOCOL_2026-09-03.md"
OUTPUT = BASE / "candidates/rq2_native_supplementary_discovery_batch_002_2026-09-03.jsonl"
SUMMARY = BASE / "candidates/rq2_native_supplementary_discovery_batch_002_2026-09-03_summary.json"


# These are deliberately diverse operational hypotheses, not pre-judged
# clusters.  Their first full-source gate rejects any family which turns out to
# be a parent/component, prerequisite/downstream sequence, generic/specialist
# relation, near-duplicate, provider cue, or keyword-only connection.
FAMILIES: list[dict[str, Any]] = [
    {"family_id": "SUPP-NATIVE-B002-01", "envelope_hypothesis": "prepare sensitive user-provided information for a controlled external sharing or storage context", "contrast_hypothesis": "dataset de-identification versus file-metadata removal versus cryptographic protection", "source_ids": ["RQ1B-V3-SRC-002420", "RQ1B-V3-SRC-000176", "RQ1B-V3-SRC-001105"]},
    {"family_id": "SUPP-NATIVE-B002-02", "envelope_hypothesis": "establish whether a product will remain usable and trustworthy across language variants", "contrast_hypothesis": "pseudo-localisation stress test versus text-expansion layout repair versus translation quality review", "source_ids": ["RQ1B-V3-SRC-012675", "RQ1B-V3-SRC-002024", "RQ1B-V3-SRC-009420"]},
    {"family_id": "SUPP-NATIVE-B002-03", "envelope_hypothesis": "improve whether a user can complete a critical interface interaction without assistive-technology exclusion", "contrast_hypothesis": "form semantics and errors versus keyboard operation versus non-text alternative treatment", "source_ids": ["RQ1B-V3-SRC-011992", "RQ1B-V3-SRC-010739", "RQ1B-V3-SRC-001274"]},
    {"family_id": "SUPP-NATIVE-B002-04", "envelope_hypothesis": "repair a confusing customer-facing screen before it creates user error or abandonment", "contrast_hypothesis": "empty/error-state design versus heuristic usability review versus visual-hierarchy repair", "source_ids": ["RQ1B-V3-SRC-000082", "RQ1B-V3-SRC-012016", "RQ1B-V3-SRC-002929"]},
    {"family_id": "SUPP-NATIVE-B002-05", "envelope_hypothesis": "obtain credible evidence that an external system integration behaves safely under realistic conditions", "contrast_hypothesis": "HTTP-boundary test versus provider sandbox/fixture test versus dependency double", "source_ids": ["RQ1B-V3-SRC-001820", "RQ1B-V3-SRC-009043", "RQ1B-V3-SRC-002204"]},
    {"family_id": "SUPP-NATIVE-B002-06", "envelope_hypothesis": "choose an evidence-generating test approach for a risky behaviour change with unknown defect modes", "contrast_hypothesis": "invariant/property exploration versus chartered exploratory testing versus regression protection", "source_ids": ["RQ1B-V3-SRC-011794", "RQ1B-V3-SRC-001614", "RQ1B-V3-SRC-001095"]},
    {"family_id": "SUPP-NATIVE-B002-07", "envelope_hypothesis": "make an existing automated test suite understandable and dependable for future change", "contrast_hypothesis": "diagnosable assertions versus execution-slice taxonomy versus maintenance refactor", "source_ids": ["RQ1B-V3-SRC-010500", "RQ1B-V3-SRC-009705", "RQ1B-V3-SRC-009024"]},
    {"family_id": "SUPP-NATIVE-B002-08", "envelope_hypothesis": "turn operational or project knowledge into documentation that a new reader can use safely", "contrast_hypothesis": "stress-ready runbook versus project front-door README versus docs-as-code operating model", "source_ids": ["RQ1B-V3-SRC-001662", "RQ1B-V3-SRC-002210", "RQ1B-V3-SRC-010827"]},
    {"family_id": "SUPP-NATIVE-B002-09", "envelope_hypothesis": "isolate the cause of an intermittent production defect using a defensible evidence strategy", "contrast_hypothesis": "search-space bisection versus concurrency/race diagnosis versus production telemetry", "source_ids": ["RQ1B-V3-SRC-002109", "RQ1B-V3-SRC-002088", "RQ1B-V3-SRC-010967"]},
    {"family_id": "SUPP-NATIVE-B002-10", "envelope_hypothesis": "make a defensible safety decision while bringing a change into production", "contrast_hypothesis": "readiness review versus canary evidence gate versus rollback decision", "source_ids": ["RQ1B-V3-SRC-011373", "RQ1B-V3-SRC-000544", "RQ1B-V3-SRC-012298"]},
    {"family_id": "SUPP-NATIVE-B002-11", "envelope_hypothesis": "prevent a service from failing as demand grows or a dependency becomes constrained", "contrast_hypothesis": "capacity forecast versus scalability design versus connection-pool saturation control", "source_ids": ["RQ1B-V3-SRC-003008", "RQ1B-V3-SRC-002808", "RQ1B-V3-SRC-012960"]},
    {"family_id": "SUPP-NATIVE-B002-12", "envelope_hypothesis": "establish trustworthy data quality before an operational or analytical decision", "contrast_hypothesis": "input validation rule versus framework-level data-quality suite versus declarative quality checks", "source_ids": ["RQ1B-V3-SRC-002244", "RQ1B-V3-SRC-010188", "RQ1B-V3-SRC-010798"]},
    {"family_id": "SUPP-NATIVE-B002-13", "envelope_hypothesis": "design a product data practice that respects a person's privacy rights and bounded purpose", "contrast_hypothesis": "consent lifecycle versus access-request fulfilment versus collection minimisation", "source_ids": ["RQ1B-V3-SRC-010374", "RQ1B-V3-SRC-002314", "RQ1B-V3-SRC-011879"]},
    {"family_id": "SUPP-NATIVE-B002-14", "envelope_hypothesis": "assess a proposed software change for credible security exposure before users are harmed", "contrast_hypothesis": "attack-surface threat model versus failure-mode analysis versus exploited-vulnerability review", "source_ids": ["RQ1B-V3-SRC-010338", "RQ1B-V3-SRC-010558", "RQ1B-V3-SRC-010110"]},
    {"family_id": "SUPP-NATIVE-B002-15", "envelope_hypothesis": "establish a security gate for source-controlled software before deployment", "contrast_hypothesis": "static-analysis integration versus build supply-chain protection versus repository-access review", "source_ids": ["RQ1B-V3-SRC-010881", "RQ1B-V3-SRC-001527", "RQ1B-V3-SRC-000909"]},
    {"family_id": "SUPP-NATIVE-B002-16", "envelope_hypothesis": "make an AI-produced answer safe for downstream use and easy to check", "contrast_hypothesis": "prompt construction versus schema-constrained output versus evidence-to-claim grounding", "source_ids": ["RQ1B-V3-SRC-009874", "RQ1B-V3-SRC-009387", "RQ1B-V3-SRC-001772"]},
    {"family_id": "SUPP-NATIVE-B002-17", "envelope_hypothesis": "make a document-grounded AI system remain useful as its knowledge base evolves", "contrast_hypothesis": "semantic chunk boundary design versus production vector-index operations versus end-to-end RAG architecture", "source_ids": ["RQ1B-V3-SRC-002683", "RQ1B-V3-SRC-001422", "RQ1B-V3-SRC-010531"]},
    {"family_id": "SUPP-NATIVE-B002-18", "envelope_hypothesis": "repair how users find and return to the right place in a product", "contrast_hypothesis": "information architecture versus mobile navigation state versus URL/deep-link routing", "source_ids": ["RQ1B-V3-SRC-002474", "RQ1B-V3-SRC-010980", "RQ1B-V3-SRC-003220"]},
    {"family_id": "SUPP-NATIVE-B002-19", "envelope_hypothesis": "turn analysis into a visual artifact that lets a decision-maker see the important evidence", "contrast_hypothesis": "decision narrative versus shared live dashboard versus focused chart annotation", "source_ids": ["RQ1B-V3-SRC-002408", "RQ1B-V3-SRC-002714", "RQ1B-V3-SRC-002847"]},
    {"family_id": "SUPP-NATIVE-B002-20", "envelope_hypothesis": "reduce recurring customer-support burden by making product problems measurable and self-resolvable", "contrast_hypothesis": "support-outcome analytics versus self-serve knowledge-base design versus actionable user-facing error handling", "source_ids": ["RQ1B-V3-SRC-012007", "RQ1B-V3-SRC-009326", "RQ1B-V3-SRC-010328"]},
    {"family_id": "SUPP-NATIVE-B002-21", "envelope_hypothesis": "ensure a business event is propagated reliably after a durable state change", "contrast_hypothesis": "transactional outbox pattern versus explicit delivery guarantee reasoning versus event-system architecture", "source_ids": ["RQ1B-V3-SRC-003019", "RQ1B-V3-SRC-010856", "RQ1B-V3-SRC-003589"]},
    {"family_id": "SUPP-NATIVE-B002-22", "envelope_hypothesis": "produce an editable architecture or process diagram that another technical contributor can maintain", "contrast_hypothesis": "draw.io XML artifact versus native Visio reconstruction versus text-based Mermaid diagram", "source_ids": ["RQ1B-V3-SRC-000323", "RQ1B-V3-SRC-000303", "RQ1B-V3-SRC-002609"]},
    {"family_id": "SUPP-NATIVE-B002-23", "envelope_hypothesis": "communicate analysed operational evidence visually to a stakeholder audience", "contrast_hypothesis": "presentation/dashboard delivery versus report-layout design versus web infographic", "source_ids": ["RQ1B-V3-SRC-000017", "RQ1B-V3-SRC-000157", "RQ1B-V3-SRC-002586"]},
    {"family_id": "SUPP-NATIVE-B002-24", "envelope_hypothesis": "give a software change an independent, evidence-based quality assessment before it is accepted", "contrast_hypothesis": "scoped code review versus general quality review versus agent-mediated review", "source_ids": ["RQ1B-V3-SRC-000162", "RQ1B-V3-SRC-002838", "RQ1B-V3-SRC-002187"]},
    {"family_id": "SUPP-NATIVE-B002-25", "envelope_hypothesis": "turn a completed research paper into an audience-appropriate scholarly communication deliverable", "contrast_hypothesis": "venue-specific paper revision versus timed presentation versus research poster", "source_ids": ["RQ1B-V3-SRC-000089", "RQ1B-V3-SRC-000342", "RQ1B-V3-SRC-002779"]},
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
    required = [PREFILTER, CURRENT_UNION, BATCH_001, PROTOCOL]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required inputs: {missing}")
    prefilter_rows = read_jsonl(PREFILTER)
    by_id = {
        str(row["source_id"]): row for row in prefilter_rows
        if row.get("record_type") == "provenance_first_source_reading_lead"
    }
    if len(by_id) != 20356:
        raise SystemExit("The provenance-first navigation subset is not the expected 20,356-lead checkpoint")
    current_hashes = {str(row["canonical_source_sha256"]) for row in read_jsonl(CURRENT_UNION)}
    b001_hashes = {
        str(candidate["source_sha256"])
        for row in read_jsonl(BATCH_001) if row.get("record_type") == "contrast_family_lead"
        for candidate in row["candidates"]
    }
    family_ids = [str(family["family_id"]) for family in FAMILIES]
    selected_ids = [source_id for family in FAMILIES for source_id in family["source_ids"]]
    if len(FAMILIES) != 25 or len(set(family_ids)) != 25:
        raise SystemExit("Batch 002 must contain exactly 25 uniquely identified contrast-family leads")
    if len(selected_ids) != 75 or len(set(selected_ids)) != 75:
        raise SystemExit("Batch 002 must contain 75 source-ID-unique appearances")
    selected_hashes: set[str] = set()
    origins: Counter[str] = Counter()
    rows: list[dict[str, Any]] = [{
        "record_type": "batch_scope",
        "batch_id": "RQ2-NATIVE-SUPPLEMENTARY-B002-2026-09-03",
        "method": "provenance-first, source-visible contrast-family navigation only",
        "input_provenance_first_lead_count": len(by_id),
        "selected_family_count": len(FAMILIES),
        "selected_source_appearance_count": len(selected_ids),
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "explicit_exclusions": [
            "admission", "prompt authoring", "gold/acceptable labels", "representation", "selector/reranker", "metrics", "thesis results",
        ],
        "claim_boundary": "Each family is a full-source reading hypothesis, never an admitted semantic cluster or RQ2 candidate.",
    }]
    for family in FAMILIES:
        candidates: list[dict[str, Any]] = []
        for source_id in family["source_ids"]:
            source = by_id.get(source_id)
            if source is None:
                raise SystemExit(f"Source is absent from the provenance-first navigation subset: {source_id}")
            source_hash = str(source["source_sha256"])
            if source_hash in current_hashes or source_hash in b001_hashes:
                raise SystemExit(f"Source is not disjoint from current union or Batch 001: {source_id}")
            source_path = Path(str(source["source_path"]))
            if not source_path.is_file() or sha256_file(source_path) != source_hash:
                raise SystemExit(f"Source-byte replay failed: {source_id}")
            if source_hash in selected_hashes:
                raise SystemExit(f"Batch 002 duplicated a source hash: {source_id}")
            selected_hashes.add(source_hash)
            origins[str(source["origin_key"])] += 1
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
                "local_provenance": source.get("local_provenance"),
                "source_byte_replay": "PASS_SHA256_MATCH",
                "status": "SOURCE_READING_LEAD_NOT_AN_ADMITTED_CANDIDATE",
            })
        rows.append({
            "record_type": "contrast_family_lead",
            "batch_id": "RQ2-NATIVE-SUPPLEMENTARY-B002-2026-09-03",
            **family,
            "candidates": candidates,
            "required_next_gate": (
                "Read all preserved sources; reject any hierarchy, composition-only dependency, generic/specialist relation, near-duplicate, "
                "or keyword-only connection before prompt work.  A surviving family then still requires cue-safe authoring and target-blind adequacy review."
            ),
            "status": "SOURCE_VISIBLE_HYPOTHESIS_PENDING_FULL_SOURCE_SCREEN",
        })
    if len(selected_hashes) != 75:
        raise SystemExit("Batch 002 must have exactly 75 unique replayed source hashes")
    write_jsonl(OUTPUT, rows)
    summary = {
        "status": "PASS_SUPPLEMENTARY_RQ2_NATIVE_BATCH_002_SOURCE_READING_QUEUE_NOT_A_CLUSTER_OR_RESULT",
        "selected_family_count": len(FAMILIES),
        "selected_source_appearance_count": len(selected_ids),
        "selected_source_hash_count": len(selected_hashes),
        "origin_count": len(origins),
        "origin_appearance_counts": dict(sorted(origins.items())),
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifacts": {str(OUTPUT.relative_to(ROOT)): sha256_file(OUTPUT)},
        "claim_boundary": [
            "Every selected source already passed the exact same local provenance precondition applied to Batch 001.",
            "A contrast family remains a source-reading hypothesis until full-source semantic screening passes.",
            "No candidate-library union, prompt, label, K=6 queue, representation, selector, metric, or thesis result changes here.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
