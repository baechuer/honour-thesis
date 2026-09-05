#!/usr/bin/env python3
"""Author and packetise RQ2-native technical wave 001 prompts.

Prompts are naturalistic task vignettes keyed to necessary operational state,
not candidate titles.  Private target rows and target-blinded review packets are
kept separate.  This script creates no gold label or admission.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
LEADS = BASE / "candidates/rq2_native_discovery_wave_001_technical_2026-08-31.jsonl"
AUTHORS = BASE / "prompts/rq2_native_technical_wave_001_authoring_private_2026-08-31.jsonl"
PACKETS = BASE / "review/rq2_native_technical_wave_001_target_blinded_packets_2026-08-31.jsonl"
SUMMARY = BASE / "review/rq2_native_technical_wave_001_authoring_packet_summary_2026-08-31.json"


PROMPTS = {
    "public-skillme-rate-limit-handler": "A partner API now returns 429 responses during our evening sync and includes a retry delay. Redesign the caller so queued work respects the quota, recovers without a synchronized retry spike, and exposes when the backlog cannot clear in time.",
    "public-skillme-circuit-breaker-builder": "When the address-verification service slows down, request threads wait until they exhaust the worker pool and the whole checkout API becomes unavailable. Add fail-fast isolation and a cautious recovery probe so the rest of checkout can degrade safely.",
    "public-skillme-connection-pool-tuner": "PostgreSQL allows 100 application connections, yet under peak traffic workers spend 700 ms waiting to check one out while many connections sit idle across replicas. Diagnose the pool settings and propose a measured configuration with overload behaviour.",

    "public-skillme-index-advisor": "A tenant dashboard query scans 40 million orders to filter by tenant and status and return the newest 50 rows. Using its execution plan and workload frequencies, recommend the smallest useful index change and how to prove the write-cost trade-off is acceptable.",
    "public-skillme-query-rewriter": "The available indexes are already used, but a report still executes one correlated lookup per account and becomes slower on later pages because it skips a growing offset. Rewrite the query shape and compare plans and results before and after.",
    "public-skillme-partition-planner": "An events table has reached two terabytes, only 90 days must remain online, and monthly deletes now block maintenance and leave vacuum behind. Design a safe partition layout, retention operation, migration sequence, and rollback checks.",

    "public-skillme-coverage-gap-finder": "Before changing the payment state machine, use the branch report and recent defect history to identify the few unexecuted paths most likely to hide a serious regression. Return a prioritized test backlog with the evidence for each choice.",
    "public-skillme-mutation-test-runner": "This billing module reports 92% line coverage, but weak assertions have allowed two calculation regressions through. Introduce controlled code changes to find which tests would still pass, then prioritise the surviving cases without destabilising the suite.",
    "public-skillme-characterization-test-writer": "A decade-old invoice calculator has no trustworthy tests and must be refactored without changing customer-visible totals. Capture its current observable behaviour across representative and awkward inputs before anyone decides which behaviours are actually correct.",

    "public-skillme-mock-stub-designer": "Unit tests for a renewal service currently call a payment SDK, the system clock and a remote entitlement endpoint. Replace those boundaries with deterministic test substitutes that can express success, timeout and retry cases without duplicating business logic.",
    "public-skillme-test-data-builder": "Tests across the order domain hand-build inconsistent customer, subscription and invoice objects. Create reusable factories that produce valid defaults, allow explicit overrides, and make boundary cases readable while respecting domain invariants.",
    "public-skillme-test-placeholder-data": "A frontend prototype needs a remotely reachable set of fake products, customers and CRUD responses plus stable placeholder images for a stakeholder demo. Set up the disposable demonstration data contract without connecting production systems.",

    "public-skillme-web-performance": "On the checkout page, the largest element appears after 4.1 seconds, the layout jumps when pricing loads, and the first interaction sometimes stalls. Build a browser-based diagnosis that identifies the dominant causes and verifies improvements under repeatable conditions.",
    "public-skillme-load-testing": "Before launch, determine whether an order API can sustain 600 concurrent users while keeping p95 below 400 ms. Design a gradual traffic experiment that exposes capacity, tail latency, errors and the first saturated resource without overwhelming production.",
    "public-skillme-mobile-perf-profiler": "A native mobile app starts slowly, drops frames while scrolling a long feed, and grows its heap after repeated navigation. Collect comparable real-device traces, isolate the dominant causes, and define before-and-after acceptance checks.",

    "public-skillme-api-design": "A public API needs a new invoices resource for listing, retrieving and cancelling invoices. Define the request and response contract, pagination, error semantics, idempotency and examples so an external consumer can implement against it before the server is built.",
    "public-skillme-api-versioning-strategist": "Hundreds of integrations use our current customer response, but a replacement model removes two fields and changes an identifier. Plan how both contracts will coexist, how consumers learn and migrate, and what evidence permits a final sunset.",
    "public-skillme-api-client-generator": "We have an approved machine-readable HTTP contract and need a typed TypeScript client for three product teams. Generate the model and operation surface while centralising authentication, transport errors and retries so updates remain reproducible from the contract.",

    "public-skillme-database-schema": "Design relational persistence for organisations, subscriptions, invoices and payments, including ownership, uniqueness and lifecycle constraints. Provide the tables, keys and a migration sequence that can be introduced without corrupting existing customer records.",
    "public-skillme-graphql-schema": "A customer dashboard must query organisations, projects and paginated activity through one graph endpoint. Define the types and operations, then prevent per-row resolver calls and unbounded expensive queries while keeping errors predictable for clients.",
    "public-skillme-feature-store-design": "A churn model uses account activity aggregates in training and must serve the same features online within 30 ms. Design point-in-time-correct historical joins, online materialisation, freshness checks and a way to detect training-serving skew.",

    "public-skillme-llm-evaluation": "A document-grounded support assistant is being changed to a new prompt and retriever. Build a regression harness from representative questions, objective checks and calibrated qualitative judging so CI can show which capabilities improved or broke.",
    "public-skillme-model-evaluation-report": "A supervised fraud classifier is ready for a release decision. Compare it with the current baseline using business costs, class imbalance, customer and geography slices, threshold behaviour and calibration, then state whether and how it should ship.",
    "public-skillme-data-drift-monitor": "A credit-risk model has been live for six months and recent applicants differ from its training population. Define production checks for input and prediction shift, alert thresholds, investigation context and evidence that should trigger retraining rather than noise.",

    "public-skillme-framework-upgrader": "Move a production web service from one major framework release to the next without a flag day. Use the migration guidance and available codemods to stage changes behind passing CI, identify incompatible plugins, and retain a rollback point after each step.",
    "public-skillme-language-version-migrator": "A Python service must move from 3.10 to 3.13 while continuing to serve traffic. Inventory semantic and dependency breaks, apply source changes in reviewable batches, and verify behaviour under both runtimes before removing the old one.",
    "public-skillme-migration-safety-checker": "A live table with 800 million rows needs a required `account_region` field populated from existing data. Review the proposed DDL for lock and rewrite risk and replace it with a staged rollout that old and new application versions can safely share and reverse.",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    leads = [
        row for row in read_jsonl(LEADS)
        if str(row["screen_disposition"]).startswith("PROMOTE_TO_RQ2_PROMPT_AUTHORING")
    ]
    if len(leads) != 9:
        raise SystemExit(f"Expected nine promoted technical clusters, found {len(leads)}")
    candidates = [candidate for lead in leads for candidate in lead["candidates"]]
    if len(candidates) != 27 or set(PROMPTS) != {str(row["skill_id"]) for row in candidates}:
        raise SystemExit("Prompt map must cover exactly 27 promoted candidates")

    author_rows: list[dict[str, Any]] = []
    packet_rows: list[dict[str, Any]] = []
    prompt_index = 0
    for lead_index, lead in enumerate(leads):
        roster: list[dict[str, str]] = []
        for candidate in lead["candidates"]:
            source_path = ROOT.parent / str(candidate["source_path"])
            if not source_path.is_file() or sha256_file(source_path) != str(candidate["source_sha256"]):
                raise SystemExit(f"Source replay failed: {source_path}")
            roster.append({
                "source_path": str(candidate["source_path"]),
                "source_sha256": str(candidate["source_sha256"]),
            })
        for candidate_index, candidate in enumerate(lead["candidates"]):
            prompt_index += 1
            prompt_id = f"NC-NATIVE-TECH-W001-{prompt_index:03d}"
            prompt = PROMPTS[str(candidate["skill_id"])]
            author_rows.append({
                "prompt_id": prompt_id,
                "cluster_lead_id": lead["cluster_lead_id"],
                "author_intended_candidate_source_sha256": candidate["source_sha256"],
                "prompt": prompt,
                "authoring_basis": "NATURAL_TASK_WITH_NECESSARY_OPERATIONAL_STATE_NOT_SKILL_TITLE",
                "initial_cue_audit": (
                    "No candidate title, repository, provider, package, source path, or explicit sibling exclusion is named. "
                    "Discriminating facts are necessary resource, failure, lifecycle, consumer, or artefact-state conditions "
                    "and still require independent source-echo review."
                ),
                "status": "AUTHORING_DRAFT_NOT_A_GOLD_LABEL_OR_ADMITTED_RQ2_CASE",
            })
            rotation = (lead_index + candidate_index + prompt_index) % len(roster)
            rotated = roster[rotation:] + roster[:rotation]
            packet_rows.append({
                "packet_id": f"NC-TARGET-BLIND-{prompt_id}",
                "prompt_id": prompt_id,
                "cluster_lead_id": lead["cluster_lead_id"],
                "prompt": prompt,
                "candidates": [
                    {"alias": chr(ord("A") + alias_index), **row}
                    for alias_index, row in enumerate(rotated)
                ],
                "reviewer_instruction": (
                    "Read each preserved source independently. The author target is withheld. Classify every candidate as "
                    "fully_adequate, partially_adequate, inadequate, or unclear; identify necessary-versus-gratuitous "
                    "cueing, source/body echo, hierarchy, subsumption, workflow composition, and multi-acceptable risk. "
                    "Do not infer or request the intended target and do not open private authoring data or prior labels/results."
                ),
                "status": "TARGET_BLINDED_REVIEW_INPUT_NOT_A_LABEL_OR_RESULT",
            })

    write_jsonl(AUTHORS, author_rows)
    write_jsonl(PACKETS, packet_rows)
    summary = {
        "status": "PASS_RQ2_NATIVE_TECHNICAL_WAVE_001_AUTHORING_PACKETISATION_NOT_A_LABEL_OR_ADMISSION",
        "promoted_cluster_count": len(leads),
        "private_prompt_count": len(author_rows),
        "target_blinded_packet_count": len(packet_rows),
        "candidate_judgment_slot_count": sum(len(row["candidates"]) for row in packet_rows),
        "input_sha256": {str(LEADS.relative_to(ROOT)): sha256_file(LEADS)},
        "artifacts": {
            str(AUTHORS.relative_to(ROOT)): sha256_file(AUTHORS),
            str(PACKETS.relative_to(ROOT)): sha256_file(PACKETS),
        },
        "claim_boundary": [
            "The prompts are private authoring drafts and target-blinded review inputs, not labels or admissions.",
            "Candidate order is rotated and the author-intended source is absent from review packets.",
            "Every source hash was replayed, but adequacy, cue safety, cluster completeness, provenance admission, and final gold remain unresolved."
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
