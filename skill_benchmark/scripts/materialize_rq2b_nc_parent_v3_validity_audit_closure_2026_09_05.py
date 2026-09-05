#!/usr/bin/env python3
"""Seal the immutable-parent V3 validity audit after independent blind review."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
SOP = BENCHMARK / "rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
INPUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_parent_v3_validity_audit_2026-09-05"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_parent_v3_validity_audit_closure_2026-09-05"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


# These are the verbatim independent decisions returned against the two sealed
# packets. They are evidence, not a new review or a reconstruction from V3.
REVIEWER_A = [
    {"case_id": "PV3-REL-001", "cue_decision": "", "relation_decision": "TRANSFORMED_DUPLICATE_OR_SPLIT_LEAK", "rationale": "Both prompts request the same large-library skill-routing policy and enumerate the same stages: candidate generation/budget, representation, reranking, and fallback. The two-stage wording is a minor paraphrase, not an independent operational task.", "source_anchors": ["S-1: Guide, Routing notes, Workflow", "S-2: Use when, Workflow"]},
    {"case_id": "PV3-CUE-001", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "", "rationale": "The source-like phrase 'webhook automation workflow' is avoidable: the remaining endpoint, signature-verification, retry, event-processing, monitoring, and downstream-action requirements already define the task.", "source_anchors": ["S-1: Webhook Endpoint Setup", "S-1: Event Processing", "S-1: Error Handling", "S-1: Monitoring"]},
    {"case_id": "PV3-CUE-002", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "", "rationale": "The source-like 'employee expense tracker/register' wording is not needed to preserve the task because receipts, categorization, approval/reimbursement status, summaries, and dashboard maintenance specify it independently.", "source_anchors": ["S-1: Receipt Processing Pipeline", "S-1: Approval Workflow", "S-1: Analytics Dashboard", "S-1: Reimbursement Processing"]},
    {"case_id": "PV3-CUE-003", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "", "rationale": "The source-like 'SaaS metrics' phrase can be removed without losing the intended work: MRR, ARR, churn, expansion, cohorts, CAC payback, LTV, and the subscription export fully constrain it.", "source_anchors": ["S-1: Overview", "S-1: Churn Metrics", "S-1: Cohort Analysis", "S-1: Investor Reporting Template"]},
    {"case_id": "PV3-CUE-004", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "", "rationale": "The source-like 'modern web best practices' label is unnecessary because the stated security, compatibility, markup, dependency, and production-readiness criteria define the review scope.", "source_anchors": ["S-1: Security", "S-1: Deprecated APIs", "S-1: Code quality", "S-1: Audit checklist"]},
    {"case_id": "PV3-CUE-005", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "", "rationale": "The source-like 'API and interface design guidance' wording is removable: the requested exported SDK/public interface, contracts, compatibility, and deprecation rules retain the operational boundary.", "source_anchors": ["S-1: Overview", "S-1: Contract First", "S-1: Input/Output Separation", "S-1: Verification"]},
    {"case_id": "PV3-CUE-006", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "", "rationale": "The source-like 'developer-facing API documentation' wording is unnecessary because reference pages, quickstarts, authentication, parameters, errors, webhook/SDK examples, migration notes, and fixed-contract boundary already specify the task.", "source_anchors": ["S-1: When to use this skill", "S-1: Step 1: Classify the API-doc job", "S-1: Step 5: Apply API-doc rules", "S-1: When not to use this skill"]},
    {"case_id": "PV3-CUE-007", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "", "rationale": "The source-like 'operational security monitoring workflow' phrase can be removed without loss because alerts, threat detection, incident response, and compliance reporting establish the operational scope.", "source_anchors": ["S-1: Security Monitoring Stack", "S-1: Detection Rules", "S-1: Incident Response", "S-1: Compliance Monitoring"]},
]

REVIEWER_B = [
    {"case_id": "PV3-REL-001", "cue_decision": "NOT_A_CUE", "relation_decision": "TRANSFORMED_DUPLICATE_OR_SPLIT_LEAK", "rationale": "Q-1 and Q-2 request the same routing-policy artifact for the same 2000-skill setting, with the same candidate-generation, representation, reranking, and fallback work; Q-2 only recasts the stages and drops Q-1's cost wording.", "source_anchors": ["S-1: routing-policy guide says to define first-stage retrieval, representation, reranking and fallback", "S-2: workflow specifies candidate generation, representation fields, reranking and fallback"]},
    {"case_id": "PV3-CUE-001", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM", "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS", "rationale": "The potentially source-like wording names a necessary operational distinction: a running webhook system rather than a static API plan. The remaining requirements independently specify endpoints, signature verification, retries, event processing, monitoring, and actions; no distinctive product/title string is needed to interpret them.", "source_anchors": ["S-1: Webhook Endpoint Setup and Signature Verification", "S-1: Event Processing, Error Handling, Monitoring"]},
    {"case_id": "PV3-CUE-002", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM", "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS", "rationale": "Employee expense tracking/register describes the requested persistent artifact, while the prompt supplies the necessary operational scope (receipts, categorization, reimbursement, approvals, monthly summaries and dashboard updates). It is not an unnecessary identity label.", "source_anchors": ["S-1: Receipt Processing Pipeline", "S-1: expense-workflow coverage of categorization, policy/approvals and reimbursement"]},
    {"case_id": "PV3-CUE-003", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM", "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS", "rationale": "SaaS metrics is necessary task vocabulary, and the enumerated MRR, ARR, churn, expansion, cohorts, CAC payback and LTV make the intended analytical output independently concrete. The DCF/stock-report exclusion defines the boundary rather than naming an identity.", "source_anchors": ["S-1: Overview lists revenue metrics, churn/retention, unit economics and cohort analysis", "S-1: Churn Metrics section"]},
    {"case_id": "PV3-CUE-004", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS", "rationale": "The opening label 'modern web best practices' is redundant: the following secure defaults, compatibility, maintainable markup, dependency use and production-readiness requirements already define the requested review. The broad label closely mirrors the source framing and could be omitted without loss of task meaning.", "source_anchors": ["S-1: describes modern web-development standards based on best-practices audits", "S-1: Security section and browser/code-quality coverage"]},
    {"case_id": "PV3-CUE-005", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM", "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS", "rationale": "API/interface language is required to identify the output as a public SDK interface rather than backend architecture or a REST-only contract. The module boundaries, stable methods, type contracts, returns, compatibility and deprecation requirements provide substantive task specification.", "source_anchors": ["S-1: applies to module boundaries and public interfaces", "S-1: core principle of stable, documented interfaces"]},
    {"case_id": "PV3-CUE-006", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM", "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS", "rationale": "Developer-facing API documentation is the requested deliverable category, not surplus identity wording. The prompt independently states the required pages/examples and fixes the contract as pre-existing, excluding redesign and contract validation.", "source_anchors": ["S-1: documentation-cluster scope includes reference docs, quickstarts, SDK/webhook guides and migration updates", "S-1: focus on publishing/refreshing integrator-facing documentation"]},
    {"case_id": "PV3-CUE-007", "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM", "relation_decision": "INDEPENDENT_OPERATIONAL_TASKS", "rationale": "Operational security monitoring distinguishes a live detection-and-response workflow from the expressly excluded static threat-model/ownership tasks. Alerts, detection, incident response and compliance reporting are functional requirements rather than a title-like identifier.", "source_anchors": ["S-1: Security Monitoring Stack", "S-1: Detection Rules, Incident Response and Compliance Monitoring"]},
]

COORDINATOR = [
    {"case_id": "PV3-CUE-001", "final_decision": "AVOIDABLE_IDENTITY_CUE", "rationale": "Deleting ‘webhook automation workflow’ leaves endpoint setup, signature verification, retries, event processing, monitoring, and downstream action. These constraints sufficiently specify the intended operational boundary."},
    {"case_id": "PV3-CUE-002", "final_decision": "AVOIDABLE_IDENTITY_CUE", "rationale": "Deleting ‘employee expense tracker/register’ leaves receipts, categorisation, approvals, reimbursement status, summaries, and a dashboard. The remaining constraints sufficiently specify the intended system."},
    {"case_id": "PV3-CUE-003", "final_decision": "AVOIDABLE_IDENTITY_CUE", "rationale": "Deleting ‘SaaS metrics’ leaves MRR, ARR, churn, expansion, cohorts, CAC payback, LTV, and subscription exports. Together these materially specify SaaS analytics rather than generic reporting."},
    {"case_id": "PV3-CUE-005", "final_decision": "AVOIDABLE_IDENTITY_CUE", "rationale": "Deleting ‘API and interface design guidance’ leaves exported SDK/public-interface requirements, contracts, compatibility, and deprecation rules. These constraints sufficiently preserve the intended task boundary."},
    {"case_id": "PV3-CUE-006", "final_decision": "AVOIDABLE_IDENTITY_CUE", "rationale": "Deleting ‘developer-facing API documentation’ leaves reference pages, quickstarts, authentication, parameters, errors, webhook/SDK examples, migration notes, and fixed-contract boundaries. The remaining requirements sufficiently specify the work."},
    {"case_id": "PV3-CUE-007", "final_decision": "AVOIDABLE_IDENTITY_CUE", "rationale": "Deleting ‘operational security monitoring workflow’ leaves monitoring stack, alerts, threat detection, incident response, compliance reporting, and detection rules. These constraints sufficiently specify security monitoring operations."},
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite immutable audit closure: {out}")
    required = (SOP, INPUT / "summary.json", INPUT / "reviewer_a_packet.jsonl", INPUT / "reviewer_b_packet.jsonl", INPUT / "internal_historical_join.jsonl")
    for path in required:
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    packet_cases = [json.loads(line)["case_id"] for line in (INPUT / "reviewer_a_packet.jsonl").read_text(encoding="utf-8").splitlines() if line]
    expected_cases = ["PV3-REL-001", *[f"PV3-CUE-{n:03d}" for n in range(1, 8)]]
    if packet_cases != expected_cases:
        raise SystemExit("Parent audit packet case roster or order drift")
    if [row["case_id"] for row in REVIEWER_A] != expected_cases or [row["case_id"] for row in REVIEWER_B] != expected_cases:
        raise SystemExit("Sealed reviewer evidence roster drift")
    if [row["case_id"] for row in COORDINATOR] != ["PV3-CUE-001", "PV3-CUE-002", "PV3-CUE-003", "PV3-CUE-005", "PV3-CUE-006", "PV3-CUE-007"]:
        raise SystemExit("Sealed coordinator evidence roster drift")
    joins = [json.loads(line) for line in (INPUT / "internal_historical_join.jsonl").read_text(encoding="utf-8").splitlines() if line]
    joins_by_case = {row["case_id"]: row for row in joins}
    if set(joins_by_case) != set(expected_cases):
        raise SystemExit("Historical join roster drift")
    a_by_case = {row["case_id"]: row for row in REVIEWER_A}
    b_by_case = {row["case_id"]: row for row in REVIEWER_B}
    coordinator_by_case = {row["case_id"]: row for row in COORDINATOR}
    final_rows: list[dict[str, Any]] = []
    for case_id in expected_cases:
        join = joins_by_case[case_id]
        if case_id == "PV3-REL-001":
            if a_by_case[case_id]["relation_decision"] != "TRANSFORMED_DUPLICATE_OR_SPLIT_LEAK" or b_by_case[case_id]["relation_decision"] != "TRANSFORMED_DUPLICATE_OR_SPLIT_LEAK":
                raise SystemExit("Relation reviewers no longer agree on transformed duplicate")
            final_rows.append({
                "case_id": case_id,
                "case_type": "PROMPT_RELATION",
                "parent_prompt_ids": join["parent_prompt_ids"],
                "historical_gold_skill_ids": join["historical_gold_skill_ids"],
                "final_decision": "EXCLUDE_PARENT_V3_VALIDITY_TRANSFORMED_DUPLICATE",
                "review_path": "A_B_AGREEMENT",
                "no_v3_rewrite": True,
                "later_acceptable_set_decision": False,
                "rationale": "Both independent blinded reviewers classified this as a transformed duplicate or split leak. Both historical endpoints are excluded without selecting one by historical performance.",
            })
            continue
        a_decision = a_by_case[case_id]["cue_decision"]
        b_decision = b_by_case[case_id]["cue_decision"]
        if a_decision == b_decision == "AVOIDABLE_IDENTITY_CUE":
            decision, path, rationale = "EXCLUDE_PARENT_V3_VALIDITY_AVOIDABLE_CUE", "A_B_AGREEMENT", "Both independent blinded reviewers found an avoidable source-like identity cue. The immutable historical prompt is excluded; it is not rewritten."
        elif case_id in coordinator_by_case and coordinator_by_case[case_id]["final_decision"] == "AVOIDABLE_IDENTITY_CUE":
            decision, path, rationale = "EXCLUDE_PARENT_V3_VALIDITY_AVOIDABLE_CUE", "A_B_DISAGREEMENT_SEALED_COORDINATOR", coordinator_by_case[case_id]["rationale"]
        elif case_id in coordinator_by_case and coordinator_by_case[case_id]["final_decision"] == "NECESSARY_CUE_STRATUM":
            decision, path, rationale = "PASS_PARENT_V3_VALIDITY_NECESSARY_CUE_STRATUM", "A_B_DISAGREEMENT_SEALED_COORDINATOR", coordinator_by_case[case_id]["rationale"]
        else:
            decision, path, rationale = "BLOCKED_PARENT_V3_VALIDITY_UNCLEAR", "A_B_DISAGREEMENT_UNRESOLVED", "The blind reviewers disagreed and the sealed coordinator did not supply a permitted resolution."
        final_rows.append({
            "case_id": case_id,
            "case_type": "TARGET_TITLE_CUE",
            "parent_prompt_ids": join["parent_prompt_ids"],
            "historical_gold_skill_ids": join["historical_gold_skill_ids"],
            "final_decision": decision,
            "review_path": path,
            "no_v3_rewrite": True,
            "later_acceptable_set_decision": False,
            "rationale": rationale,
        })
    counts = {
        "audit_cases": len(final_rows),
        "affected_parent_prompt_ids": sum(len(row["parent_prompt_ids"]) for row in final_rows),
        "excluded_parent_prompt_ids": sum(len(row["parent_prompt_ids"]) for row in final_rows if row["final_decision"].startswith("EXCLUDE")),
        "pass_parent_prompt_ids": sum(len(row["parent_prompt_ids"]) for row in final_rows if row["final_decision"].startswith("PASS")),
        "blocked_parent_prompt_ids": sum(len(row["parent_prompt_ids"]) for row in final_rows if row["final_decision"].startswith("BLOCKED")),
        "agreement_cases": sum(row["review_path"] == "A_B_AGREEMENT" for row in final_rows),
        "coordinator_resolved_cases": sum(row["review_path"] == "A_B_DISAGREEMENT_SEALED_COORDINATOR" for row in final_rows),
    }
    if counts != {"audit_cases": 8, "affected_parent_prompt_ids": 9, "excluded_parent_prompt_ids": 9, "pass_parent_prompt_ids": 0, "blocked_parent_prompt_ids": 0, "agreement_cases": 2, "coordinator_resolved_cases": 6}:
        raise SystemExit(f"Unexpected immutable-parent validity closure counts: {counts}")
    summary = {
        "status": "PASSED_PARENT_V3_VALIDITY_AUDIT_ALL_AFFECTED_PROMPTS_EXCLUDED_NO_V3_REWRITE",
        "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in required},
        "counts": counts,
        "claim_boundary": "This closure excludes nine affected historical V3 prompts from the future parent validity pool. It does not alter V3, reopen prompt construction, decide a K=6 acceptable set, or produce a retrieval metric.",
        "outputs": {},
    }
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {
        "reviewer_a_verbatim_decisions.jsonl": REVIEWER_A,
        "reviewer_b_verbatim_decisions.jsonl": REVIEWER_B,
        "sealed_coordinator_decisions.jsonl": COORDINATOR,
        "final_parent_v3_validity_dispositions.jsonl": final_rows,
    }
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": counts, "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
