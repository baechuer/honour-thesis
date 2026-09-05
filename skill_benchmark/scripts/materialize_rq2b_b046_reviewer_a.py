#!/usr/bin/env python3
"""Materialise the sole full-source Reviewer A packet and return for B046."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_commerce_ecommerce_retail_sales_travel_hospitality_real_estate_logistics_procurement_b046_2026-09-04"
INPUT = ROOT / "b046_source_native_three_skill_full_original_packets.jsonl"
LEDGER = ROOT / "source_native_reciprocal_family_ledger.jsonl"
PACKET_DIR = ROOT / "batch_046_full_source_review_packets"
PACKET = PACKET_DIR / "reviewer_a_packet.jsonl"
RETURN = PACKET_DIR / "reviewer_a_return.jsonl"

# (decision, one literal complete-source phrase per member, rationale).  The
# phrases are replayed against the immutable full sources before any return is
# written, so no title, path, discovery rank, or prior outcome enters review.
DECISIONS: dict[int, tuple[str, tuple[str, str, str], str]] = {
    1: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Packages community management operations outputs", "Packages property management operations outputs", "Packages product management operations outputs"), "The three complete sources share the same reusable-artifact packaging method, sections, file naming, dependencies, and delivery notes; only the domain token changes, which does not establish distinct first routes."),
    2: ("REJECT_COMPONENT_OR_COMPOSITION", ("end-to-end management of Google Shopping campaigns", "Optimize Google Shopping product feeds", "Audits e-commerce product feed exports"), "Campaign/feed management, feed optimisation, and diagnostic audit are linked operational stages for Shopping work. The complete sources do not define three alternative first routes to one same bounded input/output task."),
    3: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Uses persistent markdown files for general planning", "Set a tracking document as the source of truth", "Create and manage todo tracking documents"), "All three sources establish a persistent work-tracking document for multi-step tasks, decisions, and progress. Their complete instructions provide the same planning/tracking route rather than materially distinct roles."),
    4: ("REJECT_TOPIC_ONLY", ("Writes MLS and portal listing copy", "Writes the single on-site PDP master copy", "Writes an Amazon product title"), "The sources respectively create property MLS copy, an on-site product-detail page, and an Amazon listing. Listing text is a shared topic, but the user object, platform constraints, and output family differ."),
    5: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Performance measurement, attribution modeling", "UTM parameter strategy, campaign tracking", "Guides selection and honest application of a marketing attribution model"), "Each complete source centres on marketing attribution and ROI/performance interpretation. UTM setup and model-selection detail are variations within the same attribution route, not three independently preferable first routes."),
    6: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Packages platform engineering operations outputs", "Packages repository and engineering workflow outputs", "Packages site reliability engineering operations outputs"), "All members use the same operation-output packaging structure and differ only in a labelled engineering domain. The full sources do not establish operationally distinct first routes."),
    7: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Score and qualify leads based on criteria and fit", "Score and prioritize leads based on firmographic fit", "Score and qualify sales leads based on criteria and fit"), "Every member scores/qualifies sales leads and returns a priority ranking. Different named scoring frameworks or signal wording do not make three material routes."),
    8: ("REJECT_COMPONENT_OR_COMPOSITION", ("Generates UTM-tagged URLs for campaign tracking", "Generate UTM-tagged URLs for campaign tracking", "Generate QR codes with URLs and UTM tracking"), "The first two are the same UTM-link generation route; QR-code creation adds a delivery representation using those links. This is duplicate-plus-component coverage rather than a three-route family."),
    9: ("REJECT_COMPONENT_OR_COMPOSITION", ("Integrate PayPal payment processing", "Build headless e-commerce backends with Medusa.js", "Build e-commerce stores with WooCommerce"), "PayPal integration is one payment component, whereas Medusa and WooCommerce are competing full storefront platforms. The source set mixes a subcomponent with end-to-end implementations rather than equivalent routes."),
    10: ("REJECT_TOPIC_ONLY", ("Process multiple documents in bulk", "Executing Plans takes a written plan", "Batch Processing enables parallel AI task execution"), "Bulk document operations, executing a written plan, and parallel AI task execution have different input objects and outputs. Parallel/batch execution is only a shared broad mechanism."),
    11: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("optimize signup, registration, account creation", "increase conversions on any marketing page", "optimize signup, registration, account creation"), "Two complete sources are materially the same signup-flow optimisation route, while the page CRO source is a broader container. The set is not three independent, balanced alternatives."),
    12: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Product-led growth and customer-base growth", "Build product-led growth engines", "Build self-serve acquisition and expansion motions"), "All members prescribe product-led/self-serve acquisition, activation, and expansion work. Their framework variations do not establish distinct first-route skills for one bounded task."),
    13: ("REJECT_TOPIC_ONLY", ("Pull the branch's latest CI test failures", "Check the buildup of un-archived OpenSpec changes", "Report status across all in-flight delivery pipelines"), "CI-failure synchronisation, archiving accumulated changes, and reporting delivery state operate on different lifecycle objects and outputs. Delivery workflow is only a topic relationship."),
    14: ("REJECT_COMPONENT_OR_COMPOSITION", ("Divides a lead list into useful commercial segments", "Assesses the quality, composition, and usefulness of a lead list", "Normalizes and improves the consistency of prospect-list data"), "Cleaning a lead export, analysing its quality, and segmenting it are sequential or composable lead-list operations, not alternatives for one shared input/output envelope."),
    15: ("REJECT_TOPIC_ONLY", ("Automate Linear issue tracking", "Automate ClickUp workspace management", "Automate expense tracking"), "Linear workflow automation, ClickUp workspace automation, and expense reimbursement automation have distinct task objects and expected outputs; automation is only a broad common topic."),
    16: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Packages manufacturing operations outputs", "Packages retail operations outputs", "Packages robotics operations outputs"), "All three complete sources package operations outputs using the same sections, filenames, dependency handling, and delivery notes, with only a domain label substituted."),
    17: ("REJECT_TOPIC_ONLY", ("optimize signup, registration, account creation", "optimize any form that is NOT signup/registration", "optimize any form that is NOT signup/registration"), "Signup-flow optimisation and non-signup form optimisation have explicitly different input objects; the latter two are duplicates. There is no three-way common bounded envelope."),
    18: ("REJECT_TOPIC_ONLY", ("tracking expenses with headers and initial entries", "Append a deal status update", "Duplicate a Google Sheets template tab"), "Expense-sheet setup, sales-deal logging, and copying a monthly template have different user objectives and outputs. Google Sheets is shared tooling only."),
    19: ("REJECT_TOPIC_ONLY", ("Creates and manages tracking plans", "Creates, reads, and manages roadmap files", "Manages newsroom editorial workflows"), "Schema-constrained event tracking, roadmap-file phase tracking, and newsroom assignment workflows concern different concrete task objects. Tracking is not a sufficient common envelope."),
    20: ("REJECT_COMPONENT_OR_COMPOSITION", ("Review affiliate campaign results and improve strategy", "Generate affiliate performance reports", "Manage and compare multiple affiliate programs as a portfolio"), "Campaign retrospective, KPI reporting, and portfolio management are related but distinct analytical/management stages. The full sources do not present them as three alternative first routes."),
    21: ("REJECT_TOPIC_ONLY", ("optimize signup, registration, account creation", "increase conversions on any marketing page", "optimize any form that is NOT signup/registration"), "Signup conversion, page conversion, and non-signup form conversion operate on explicitly different user objects. Conversion-rate optimisation is a broad topic rather than a shared concrete task."),
    22: ("REJECT_GENERIC_SPECIALIST", ("decide WHO IN YOUR ICP TO HIT NOW", "Designs the outbound GTM motion", "which existing accounts to work now"), "The first and third sources rank accounts for immediate action, while the middle source designs the broader outbound motion and cadence. The broad strategy source is not a peer route to the concrete prioritisation task."),
    23: ("REJECT_GENERIC_SPECIALIST", ("founder needs demo scripts, discovery call frameworks", "Builds competitive positioning notes", "Writes demo scripts for sales"), "The founder sales-script source is a broad container covering demos, discovery, objections, RFPs, and competitive work; the other two are specialised subroutes, so the family is generic-specialist rather than balanced alternatives."),
    24: ("REJECT_TOPIC_ONLY", ("Weekly revenue / sales forecasting", "Spreadsheet operations for small businesses", "Builds annual operating budgets"), "Weekly forecasting, general spreadsheet operations, and annual budgeting have different time horizons, inputs, and output families. Small-business operations does not make a bounded common task."),
    25: ("REJECT_TOPIC_ONLY", ("increase conversions on any marketing page", "optimize any form that is NOT signup/registration", "optimize signup, registration, account creation"), "Page, non-signup form, and signup-flow conversion work each have expressly different input objects and boundaries in the complete sources. CRO alone is only a shared topic."),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def line_anchor(source: str, phrase: str) -> str:
    for line_number, line in enumerate(source.splitlines(), 1):
        if phrase in line:
            return f"L{line_number}: {line.strip()}"
    raise SystemExit(f"literal evidence phrase not found: {phrase!r}")


def main() -> int:
    if PACKET_DIR.exists():
        raise SystemExit(f"refusing to overwrite B046 Reviewer A material: {PACKET_DIR}")
    rows, ledger = read_jsonl(INPUT), read_jsonl(LEDGER)
    if len(rows) != len(ledger) != 25 or set(DECISIONS) != set(range(1, 26)):
        raise SystemExit("B046 reviewer input cardinality/decision map mismatch")
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != "2fd09e2bed0f46c5ddd4c580a454143ab26506a8b3efbfedf9ce13d8348c8e15":
        raise SystemExit("immutable B046 full-original packet hash mismatch")
    if hashlib.sha256(LEDGER.read_bytes()).hexdigest() != "a8f24eeddc6294af1e27abdbaec770e85858e3cbc3f74825c3bcfc63a65e67dd":
        raise SystemExit("immutable B046 family-ledger hash mismatch")
    packets: list[dict[str, Any]] = []
    returns: list[dict[str, Any]] = []
    for row in rows:
        rank = int(row["batch_rank"])
        if row["family_id"] != ledger[rank - 1]["family_id"]:
            raise SystemExit(f"ledger family mismatch at B046 rank {rank}")
        members, sources = [], []
        for position, member in enumerate(row["members"], 1):
            originals = member["preserved_complete_original_sources"]
            if not originals:
                raise SystemExit(f"missing complete source at B046 rank {rank}, member {position}")
            source = originals[0]["preserved_original_skill_utf8"]
            expected_hash = str(member["canonical_source_sha256"])
            if any(hashlib.sha256(item["preserved_original_skill_utf8"].encode("utf-8")).hexdigest() != expected_hash for item in originals):
                raise SystemExit(f"complete-source hash mismatch at B046 rank {rank}, member {position}")
            sources.append(source)
            members.append({"member_token": f"S-{position}", "source_byte_sha256": expected_hash, "complete_original_skill": source, "review_instruction": "Read the complete original skill. Cite literal excerpts or line locations; do not infer missing capability from topic familiarity."})
        family_token = "F-" + str(row["family_id"]).removeprefix("SN-LEX-")
        packets.append({"record_type": "source_native_full_source_reviewer_a_packet", "family_token": family_token, "members": members, "rubric": {"pass": "Three independent first-route skills share a bounded objective/input/output envelope, present plausible natural confusion, and have source-supported distinct roles or tools.", "reject_codes": ["REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION", "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK", "REJECT_NO_BOUNDED_ENVELOPE"], "rule": "The complete original source is authoritative. Do not use discovery rank, source path, origin, prior outcomes, or another reviewer's judgement."}})
        decision, phrases, rationale = DECISIONS[rank]
        evidence = {f"S-{position}": [line_anchor(source, phrase)] for position, (source, phrase) in enumerate(zip(sources, phrases), 1)}
        returns.append({"record_type": "source_native_full_source_reviewer_a_return", "family_token": family_token, "decision": decision, "common_envelope_evidence": [item for values in evidence.values() for item in values], "member_contrast_evidence": evidence, "rationale": rationale, "review_boundary": "Reviewer A full-source family assessment only; no provenance, prompt, adequacy, admission, selector, retrieval-result, or metric decision."})
    if len({member["source_byte_sha256"] for packet in packets for member in packet["members"]}) != 75:
        raise SystemExit("B046 Reviewer A packet source cardinality mismatch")
    PACKET_DIR.mkdir(parents=True)
    write_jsonl(PACKET, packets)
    write_jsonl(RETURN, returns)
    print(json.dumps({"packet_sha256": hashlib.sha256(PACKET.read_bytes()).hexdigest(), "return_sha256": hashlib.sha256(RETURN.read_bytes()).hexdigest(), "families": len(returns), "source_hashes": 75, "decision_counts": {decision: sum(row["decision"] == decision for row in returns) for decision in sorted({row["decision"] for row in returns})}}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
