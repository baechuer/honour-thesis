#!/usr/bin/env python3
"""Write the independent, source-replayed Reviewer B return for B046."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_commerce_ecommerce_retail_sales_travel_hospitality_real_estate_logistics_procurement_b046_2026-09-04"
PACKET = ROOT / "batch_046_full_source_review_packets/reviewer_b_packet.jsonl"
RETURN = ROOT / "batch_046_full_source_review_packets/reviewer_b_return.jsonl"


# decision, literal phrase for each source, source-grounded family rationale.
REVIEWS: dict[int, tuple[str, tuple[str, str, str], str]] = {
    1: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Packages community management operations outputs", "Packages property management operations outputs", "Packages product management operations outputs"), "All three package a known set of materials into the same outline, file/section organisation, and delivery checklist; the domain-labelled context is not a distinct first-route operation."),
    2: ("REJECT_COMPONENT_OR_COMPOSITION", ("end-to-end management of Google Shopping campaigns", "Optimize Google Shopping product feeds", "Audits e-commerce product feed exports"), "The full sources place feed optimisation and feed QA within the broader Shopping-campaign operating surface; the audit/improvement steps are composable rather than three alternative first routes."),
    3: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Uses persistent markdown files for general planning", "Set a tracking document as the source of truth", "Create and manage todo tracking documents"), "Each source establishes a persistent task record for planning, decisions, and progress. The wording and document conventions do not create materially distinct routes."),
    4: ("REJECT_TOPIC_ONLY", ("Writes MLS and portal listing copy", "Writes the single on-site PDP master copy", "Writes an Amazon product title"), "The sources have different user objects and constrained deliverables: property portal remarks, a storefront PDP, and Amazon title/bullets/backend terms. 'Listing copy' alone is only a topic overlap."),
    5: ("REJECT_GENERIC_SPECIALIST", ("Performance measurement, attribution modeling", "UTM parameter strategy, campaign tracking", "Guides selection and honest application of a marketing attribution model"), "The general analytics source spans tracking, reporting, and attribution; the UTM workflow and model-selection memo are narrower parts of that surface, not balanced peer first routes."),
    6: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Packages platform engineering operations outputs", "Packages repository and engineering workflow outputs", "Packages site reliability engineering operations outputs"), "All sources use the same reusable-artifact packaging procedure and output, with only the operations context substituted."),
    7: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Score and qualify leads based on criteria and fit", "Score and prioritize leads based on firmographic fit", "Score and qualify sales leads"), "Every source scores sales leads against fit/signals and produces prioritisation. Framework labels and signal detail are not separate first routes."),
    8: ("REJECT_COMPONENT_OR_COMPOSITION", ("Generates UTM-tagged URLs for campaign tracking", "Generate UTM-tagged URLs for campaign tracking", "Generate QR codes with URLs and UTM tracking"), "S-1 and S-2 describe the same UTM-link task; S-3 adds QR rendering around a URL with UTM tracking. This is duplicate-plus-composition coverage."),
    9: ("REJECT_COMPONENT_OR_COMPOSITION", ("Integrate PayPal payment processing", "Build headless e-commerce backends", "Build e-commerce stores with WooCommerce"), "PayPal integration is a payment component, while the other sources build complete commerce platforms. They do not have equivalent input/output envelopes."),
    10: ("REJECT_TOPIC_ONLY", ("Process multiple documents in bulk", "Executing Plans takes a written plan", "Batch Processing enables parallel AI task execution"), "Bulk file transformation, executing a written plan, and parallel AI work operate on different input objects and output contracts; batch execution is only a broad mechanism."),
    11: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("optimize signup, registration, account creation", "increase conversions on any marketing page", "optimize signup, registration, account creation"), "S-1 and S-3 are the same signup-flow optimisation route, while S-2 is a broader page-CRO container. The family lacks three independent peers."),
    12: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Product-led growth and customer-base growth", "Build product-led growth engines", "Build self-serve acquisition and expansion motions"), "All three sources cover the same product-led acquisition, activation, retention, and expansion surface; framework naming does not establish distinct first routes."),
    13: ("REJECT_TOPIC_ONLY", ("Pull the branch's latest CI test failures", "Check the buildup of un-archived OpenSpec changes", "Report status across all in-flight delivery pipelines"), "CI-failure synchronisation, archival of accumulated changes, and portfolio status reporting have distinct workflow objects and output actions. Delivery workflow is only a topic relation."),
    14: ("REJECT_COMPONENT_OR_COMPOSITION", ("Divides a lead list into useful commercial segments", "Assesses the quality, composition, and usefulness", "Normalizes and improves the consistency"), "Cleaning, quality analysis, and commercial segmentation are sequential/composable transformations of a lead list, not alternative routes to one bounded task."),
    15: ("REJECT_TOPIC_ONLY", ("Automate Linear issue tracking", "Automate ClickUp workspace management", "Automate expense tracking"), "The automation targets and expected artefacts are respectively engineering issues, workspace tasks, and reimbursements. Automation is the only common topic."),
    16: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Packages manufacturing operations outputs", "Packages retail operations outputs", "Packages robotics operations outputs"), "Each source applies the same packaging procedure and output structure to a different named domain; no source-supported operational contrast is present."),
    17: ("REJECT_TOPIC_ONLY", ("optimize signup, registration, account creation", "optimize any form that is NOT signup/registration", "optimize any form that is NOT signup/registration"), "The sources explicitly split signup flows from non-signup forms, and S-2/S-3 duplicate the latter route. There is no three-way bounded common envelope."),
    18: ("REJECT_TOPIC_ONLY", ("Set up a Google Sheets spreadsheet for tracking expenses", "Append a deal status update", "Duplicate a Google Sheets template tab"), "Expense-sheet creation, a deal-log append, and monthly-template duplication are distinct spreadsheet tasks with different inputs and outputs."),
    19: ("REJECT_TOPIC_ONLY", ("Creates and manages tracking plans", "Creates, reads, and manages roadmap files", "Manages newsroom editorial workflows"), "Event-schema governance, roadmap phase tracking, and newsroom coordination concern different task objects and deliverables. Tracking is only a broad label."),
    20: ("REJECT_COMPONENT_OR_COMPOSITION", ("Review affiliate campaign results and improve strategy", "Generate affiliate performance reports", "Manage and compare multiple affiliate programs"), "Campaign retrospective, KPI reporting, and portfolio management are connected analytical/management stages rather than substitutable first routes."),
    21: ("REJECT_TOPIC_ONLY", ("optimize signup, registration, account creation", "increase conversions on any marketing page", "optimize any form that is NOT signup/registration"), "Signup, page, and non-signup-form CRO have source-stated distinct user objects and boundaries. Conversion optimisation alone does not supply a shared concrete envelope."),
    22: ("REJECT_GENERIC_SPECIALIST", ("decide WHO IN YOUR ICP TO HIT NOW", "Designs the outbound GTM motion", "which existing accounts to work now"), "The two account-prioritisation sources are concrete current-account workflows, whereas the motion source defines the broader outbound strategy, signal stack, and cadence. It is not a peer route."),
    23: ("REJECT_GENERIC_SPECIALIST", ("founder needs demo scripts, discovery call frameworks", "Builds competitive positioning notes", "Writes demo scripts for sales"), "The founder sales-script source is a broad pre-sales container that encompasses demos and competitive work, while the other sources are narrow specialised deliverables."),
    24: ("REJECT_TOPIC_ONLY", ("Weekly revenue / sales forecasting", "Spreadsheet operations for small businesses", "Builds annual operating budgets"), "Weekly forecasting, generic spreadsheet operation, and annual budgeting use different time horizons, inputs, and output artefacts. Small-business operations is only a topic overlap."),
    25: ("REJECT_TOPIC_ONLY", ("increase conversions on any marketing page", "optimize any form that is NOT signup/registration", "optimize signup, registration, account creation"), "Page, non-signup form, and signup-flow CRO are explicitly separated by input object in their sources, so the set has no shared bounded first-route envelope."),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def line_anchor(source: str, phrase: str) -> str:
    for number, line in enumerate(source.splitlines(), 1):
        if phrase in line:
            return f"L{number}: {line.strip()}"
    raise SystemExit(f"literal evidence not found: {phrase!r}")


def main() -> int:
    if RETURN.exists():
        raise SystemExit("refusing to overwrite existing B046 Reviewer B return")
    rows = read_jsonl(PACKET)
    if len(rows) != 25 or set(REVIEWS) != set(range(1, 26)):
        raise SystemExit("packet/review cardinality mismatch")
    returns: list[dict[str, Any]] = []
    for rank, packet in enumerate(rows, 1):
        if packet["record_type"] != "source_native_full_source_reviewer_b_packet" or len(packet["members"]) != 3:
            raise SystemExit(f"malformed packet at rank {rank}")
        decision, phrases, rationale = REVIEWS[rank]
        evidence: dict[str, list[str]] = {}
        for member, phrase in zip(packet["members"], phrases):
            source = member["complete_original_skill"]
            expected_hash = member["source_byte_sha256"]
            if hashlib.sha256(source.encode("utf-8")).hexdigest() != expected_hash:
                raise SystemExit(f"source hash mismatch at rank {rank}, {member['member_token']}")
            evidence[member["member_token"]] = [line_anchor(source, phrase)]
        returns.append({
            "record_type": "source_native_full_source_reviewer_b_return",
            "family_token": packet["family_token"],
            "decision": decision,
            "common_envelope_evidence": [entry for entries in evidence.values() for entry in entries],
            "member_contrast_evidence": evidence,
            "rationale": rationale,
            "review_boundary": "Reviewer B full-source family assessment only; no provenance, prompt, adequacy, admission, selector, retrieval-result, or metric decision.",
        })
    RETURN.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in returns), encoding="utf-8")
    counts = {decision: sum(row["decision"] == decision for row in returns) for decision in sorted({row["decision"] for row in returns})}
    print(json.dumps({"return_sha256": hashlib.sha256(RETURN.read_bytes()).hexdigest(), "families": len(returns), "sources_replayed": 75, "decision_counts": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
