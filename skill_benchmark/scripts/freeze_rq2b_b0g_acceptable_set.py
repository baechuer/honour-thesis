#!/usr/bin/env python3
"""Build and finalize the local RQ2b B0G acceptable-set freeze.

The controller consumes only revalidated blinded-review artefacts. It never
calls a provider, runs a selector, or reads a retrieval result. Proposal
creation is deliberately distinct from finalization: an independent,
metadata-only review must bind the proposal before it can become the frozen
acceptable set.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import build_rq2b_b0g_batched_review as initial
import run_rq2b_b0g_adjudication as adjudication


VERSION = "rq2b-b0g-final-freeze-v1"
OUTPUT_NAME = "final_freeze_v2_2026-08-09"
SCORING_STRATA = {"controlled", "public_gold"}
INDEPENDENT_REVIEW_SCOPE = [
    "controller_logic",
    "proposal_manifest",
    "outcomes_hash_and_schema",
    "strict_status_hash_and_schema",
    "freeze_report_stop_rules",
    "added_alternative_pattern",
]
OUTCOME_FIELDS = {
    "prompt_id",
    "prompt_sha256",
    "stratum",
    "candidate_skill_id",
    "candidate_source_sha256",
    "a_label",
    "b_label",
    "c_label",
    "final_label",
    "decision_path",
}
ACCEPTABLE_FIELDS = {
    "prompt_id",
    "prompt_sha256",
    "stratum",
    "candidate_skill_id",
    "candidate_source_sha256",
    "acceptance_basis",
    "reviewed_skill_id",
}
STRICT_STATUS_FIELDS = {
    "prompt_id",
    "prompt_sha256",
    "stratum",
    "strict_gold_skill_id",
    "strict_gold_reviewed",
    "strict_gold_final_label",
    "strict_gold_accepted_after_duplicate_closure",
}
PROPOSAL_MANIFEST_FIELDS = {
    "schema_version",
    "state",
    "initial_plan_sha256",
    "initial_validation_inventory_sha256",
    "adjudication_plan_sha256",
    "adjudication_validation_inventory_sha256",
    "source_manifest_sha256",
    "prompt_manifest_sha256",
    "candidate_pool_sha256",
    "controller_sha256",
    "scored_prompts",
    "reviewed_units",
    "direct_fully_acceptable",
    "acceptable_after_duplicate_closure",
    "added_direct_fully_acceptable",
    "added_acceptable_after_duplicate_closure",
    "added_alternatives_sha256",
    "strict_gold_rejections",
    "prompts_without_fully_acceptable",
    "proposal_path",
    "proposal_sha256",
    "outcomes_path",
    "outcomes_sha256",
    "strict_status_path",
    "strict_status_sha256",
    "report_path",
    "report_sha256",
    "network_calls",
    "provider_calls",
    "raw_text_in_outputs",
}
REPORT_FIELDS = {
    "schema_version",
    "state",
    "proposal_sha256",
    "decision_rule",
    "stop_rules",
    "review_required",
    "counts",
    "strict_versus_acceptable",
    "added_alternatives",
    "unresolved_cases",
    "reviewer_agreement",
    "per_stratum_rates",
    "network_calls",
    "provider_calls",
    "retrieval_or_selector_runs",
}
INDEPENDENT_REVIEW_FIELDS = {
    "schema_version",
    "state",
    "proposal_manifest_sha256",
    "proposal_sha256",
    "outcomes_sha256",
    "strict_status_sha256",
    "report_sha256",
    "review_scope",
    "reviewer_id",
    "reviewer_method",
    "controller_sha256",
    "hard_stop_rules_checked",
    "added_alternatives_sha256",
    "added_alternatives_count",
    "added_alternative_pattern_assessment",
    "rationale",
    "observations",
    "findings",
    "recommendation",
    "network_calls",
    "provider_calls",
    "raw_text_reviewed",
}
FINAL_MANIFEST_FIELDS = {
    "schema_version",
    "state",
    "proposal_manifest_sha256",
    "independent_review_sha256",
    "final_acceptable_set_path",
    "final_acceptable_set_sha256",
    "network_calls",
    "provider_calls",
    "retrieval_or_selector_runs",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def controller_sha256() -> dict[str, str]:
    directory = Path(__file__).resolve().parent
    controller_paths = {
        "build_rq2b_b0g_batched_review.py": directory / "build_rq2b_b0g_batched_review.py",
        "run_rq2b_b0g_adjudication.py": directory / "run_rq2b_b0g_adjudication.py",
        "freeze_rq2b_b0g_acceptable_set.py": Path(__file__).resolve(),
    }
    return {name: sha256_file(path) for name, path in controller_paths.items()}


def read_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"Missing JSON input: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def write_json_new(path: Path, value: Any) -> None:
    require(not path.exists(), f"Refusing to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    require(not path.exists(), f"Refusing to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def output_root(root: Path) -> Path:
    return initial.review_root(root) / OUTPUT_NAME


def paths(root: Path) -> dict[str, Path]:
    base = output_root(root)
    return {
        "proposal": base / "proposed_acceptable_set.jsonl",
        "outcomes": base / "reviewed_unit_outcomes.jsonl",
        "strict": base / "strict_gold_status.jsonl",
        "report": base / "freeze_report.json",
        "manifest": base / "proposal_manifest.json",
        "review": base / "independent_freeze_review.json",
        "final": base / "final_acceptable_set.jsonl",
        "final_manifest": base / "final_freeze_manifest.json",
    }


def validated_c_labels(root: Path) -> tuple[dict[str, str], str, str]:
    plan, manifest = adjudication.load_adjudication_plan(root)
    result = adjudication.summary(root)
    require(result["state"] == "adjudication_complete_pending_acceptable_set", "Adjudication is not complete")
    records = adjudication.validated_adjudication_records(root, plan, manifest)
    require(len(records) == result["batches_total"], "Adjudication validation coverage mismatch")
    by_token: dict[str, str] = {}
    for record in records:
        validated_path = root / str(record["validated_adjudications_path"])
        for row in initial.read_jsonl(validated_path):
            require(set(row) == {"review_token", "label", "decision_sha256"}, "C validated row schema mismatch")
            token = row["review_token"]
            require(token not in by_token, "Duplicate C review token")
            require(row["label"] in initial.LABELS, "Invalid C label")
            by_token[token] = row["label"]
    expected = {row["adjudication_token"] for row in plan}
    require(set(by_token) == expected, "C label token coverage mismatch")
    inventory = [
        {
            "batch_id": record["batch_id"],
            "packet_sha256": record["packet_sha256"],
            "decision_sha256": record["decision_sha256"],
            "validated_adjudications_sha256": record["validated_adjudications_sha256"],
        }
        for record in records
    ]
    return by_token, manifest["plan_sha256"], canonical_sha256(sorted(inventory, key=lambda row: row["batch_id"]))


def proposal_data(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    initial_plan, initial_labels, initial_inventory_sha = adjudication.validated_initial_labels(root)
    initial_manifest = initial.load_plan(root)[1]
    c_labels, c_plan_sha, c_inventory_sha = validated_c_labels(root)
    c_plan, _ = adjudication.load_adjudication_plan(root)
    units = initial.unit_lookup(root)
    source_paths = initial.input_paths(root)
    sources = {row["skill_id"]: row for row in initial.read_jsonl(source_paths["source_manifest"])}
    prompts = {row["prompt_id"]: row for row in initial.read_jsonl(source_paths["prompt_manifest"])}
    candidates = initial.read_jsonl(source_paths["candidate_pool"])

    by_unit: dict[str, dict[str, str]] = defaultdict(dict)
    for assignment in initial_plan:
        by_unit[assignment["unit_token"]][assignment["reviewer_role"]] = initial_labels[assignment["assignment_token"]]
    require(set(by_unit) == set(units), "Initial reviewed-unit coverage mismatch")
    require(all(set(labels) == set(initial.ROLES) for labels in by_unit.values()), "Initial A/B label coverage mismatch")

    c_by_unit = {row["unit_token"]: c_labels[row["adjudication_token"]] for row in c_plan}
    require(len(c_by_unit) == len(c_plan), "Duplicate C unit")
    candidate_pairs = {(row["prompt_id"], row["candidate_skill_id"]) for row in candidates}
    require(len(candidate_pairs) == len(units), "Candidate-pool unit mismatch")
    scored_prompt_ids = sorted(
        prompt_id for prompt_id, prompt in prompts.items() if prompt["stratum"] in SCORING_STRATA
    )
    reviewed_prompt_ids = {unit["_prompt_id"] for unit in units.values()}
    require(len(scored_prompt_ids) == 389, "Expected exactly 389 scored prompts")
    require(reviewed_prompt_ids == set(scored_prompt_ids), "Candidate pool does not cover the exact scored-prompt identity set")

    outcomes: list[dict[str, Any]] = []
    direct_accepts: set[tuple[str, str]] = set()
    for unit_token, unit in units.items():
        prompt_id = unit["_prompt_id"]
        skill_id = unit["_skill_id"]
        a_label = by_unit[unit_token]["A"]
        b_label = by_unit[unit_token]["B"]
        c_label = c_by_unit.get(unit_token)
        if c_label is not None:
            final_label = c_label
            path = "c_adjudication"
        elif a_label == b_label:
            final_label = a_label
            path = "a_b_agreement"
        else:
            require(
                not ({a_label, b_label} & adjudication.ELIGIBILITY_LABELS),
                "Potentially acceptable A/B disagreement omitted from C plan",
            )
            final_label = "not_fully_acceptable_disagreement"
            path = "a_b_nonpotential_disagreement"
        prompt = prompts[prompt_id]
        source = sources[skill_id]
        outcome = {
            "prompt_id": prompt_id,
            "prompt_sha256": prompt["prompt_sha256"],
            "stratum": prompt["stratum"],
            "candidate_skill_id": skill_id,
            "candidate_source_sha256": source["source_sha256"],
            "a_label": a_label,
            "b_label": b_label,
            "c_label": c_label,
            "final_label": final_label,
            "decision_path": path,
        }
        require(set(outcome) == OUTCOME_FIELDS, "Outcome schema mismatch")
        outcomes.append(outcome)
        if final_label == "fully_acceptable":
            direct_accepts.add((prompt_id, skill_id))

    outcomes.sort(key=lambda row: (row["prompt_id"], row["candidate_skill_id"]))
    accepted_hashes_by_prompt: dict[str, set[str]] = defaultdict(set)
    for prompt_id, skill_id in direct_accepts:
        accepted_hashes_by_prompt[prompt_id].add(sources[skill_id]["source_sha256"])
    proposed: list[dict[str, Any]] = []
    for prompt_id in scored_prompt_ids:
        prompt = prompts[prompt_id]
        for skill_id, source in sorted(sources.items()):
            source_hash = source["source_sha256"]
            if source_hash not in accepted_hashes_by_prompt[prompt_id]:
                continue
            basis = "reviewed_fully_acceptable" if (prompt_id, skill_id) in direct_accepts else "exact_i2_duplicate_closure"
            reviewed_skill_ids = sorted(
                accepted_skill_id
                for accepted_prompt_id, accepted_skill_id in direct_accepts
                if accepted_prompt_id == prompt_id and sources[accepted_skill_id]["source_sha256"] == source_hash
            )
            require(reviewed_skill_ids, "Duplicate closure missing reviewed source")
            row = {
                "prompt_id": prompt_id,
                "prompt_sha256": prompt["prompt_sha256"],
                "stratum": prompt["stratum"],
                "candidate_skill_id": skill_id,
                "candidate_source_sha256": source_hash,
                "acceptance_basis": basis,
                "reviewed_skill_id": reviewed_skill_ids[0],
            }
            require(set(row) == ACCEPTABLE_FIELDS, "Acceptable-set row schema mismatch")
            proposed.append(row)
    proposed.sort(key=lambda row: (row["prompt_id"], row["candidate_skill_id"]))

    proposed_pairs = {(row["prompt_id"], row["candidate_skill_id"]) for row in proposed}
    proposed_by_pair = {(row["prompt_id"], row["candidate_skill_id"]): row for row in proposed}
    preaudit_path = initial.version_root(root) / "b0g_m_v3_2026-08-08" / "initial_acceptable_set.jsonl"
    preaudit_pairs = {
        (row["prompt_id"], row["candidate_skill_id"])
        for row in initial.read_jsonl(preaudit_path)
        if row.get("included_in_pre_audit_acceptable_set") is True
    }
    strict_status: list[dict[str, Any]] = []
    strict_rejections: list[dict[str, Any]] = []
    empty_prompts: list[str] = []
    outcome_by_pair = {(row["prompt_id"], row["candidate_skill_id"]): row for row in outcomes}
    for prompt_id in scored_prompt_ids:
        prompt = prompts[prompt_id]
        strict_id = prompt["gold_skill"]
        outcome = outcome_by_pair.get((prompt_id, strict_id))
        reviewed = outcome is not None
        final_label = outcome["final_label"] if outcome else None
        accepted = (prompt_id, strict_id) in proposed_pairs
        row = {
            "prompt_id": prompt_id,
            "prompt_sha256": prompt["prompt_sha256"],
            "stratum": prompt["stratum"],
            "strict_gold_skill_id": strict_id,
            "strict_gold_reviewed": reviewed,
            "strict_gold_final_label": final_label,
            "strict_gold_accepted_after_duplicate_closure": accepted,
        }
        require(set(row) == STRICT_STATUS_FIELDS, "Strict-status schema mismatch")
        strict_status.append(row)
        if not reviewed or final_label != "fully_acceptable":
            strict_rejections.append(row)
        if not any(candidate_prompt_id == prompt_id for candidate_prompt_id, _ in proposed_pairs):
            empty_prompts.append(prompt_id)
    strict_status.sort(key=lambda row: row["prompt_id"])
    added_direct = sorted(direct_accepts - preaudit_pairs)
    added_proposed = sorted(proposed_pairs - preaudit_pairs)
    added_alternatives = [
        {
            "prompt_id": prompt_id,
            "candidate_skill_id": skill_id,
            "stratum": proposed_by_pair[(prompt_id, skill_id)]["stratum"],
            "acceptance_basis": proposed_by_pair[(prompt_id, skill_id)]["acceptance_basis"],
            "reviewed_skill_id": proposed_by_pair[(prompt_id, skill_id)]["reviewed_skill_id"],
        }
        for prompt_id, skill_id in added_proposed
    ]
    unresolved_cases = [
        {
            "prompt_id": row["prompt_id"],
            "candidate_skill_id": row["candidate_skill_id"],
            "stratum": row["stratum"],
            "decision_path": row["decision_path"],
            "final_label": row["final_label"],
        }
        for row in outcomes
        if row["final_label"] == "uncertain"
    ]
    pair_counts = Counter(f"{row['a_label']}|{row['b_label']}" for row in outcomes)
    stratum_rates: dict[str, dict[str, Any]] = {}
    agreement_by_stratum: dict[str, dict[str, Any]] = {}
    strict_by_stratum: dict[str, dict[str, Any]] = {}
    for stratum in sorted(SCORING_STRATA):
        stratum_outcomes = [row for row in outcomes if row["stratum"] == stratum]
        stratum_strict = [row for row in strict_status if row["stratum"] == stratum]
        total = len(stratum_outcomes)
        require(total > 0, f"No reviewed units for scored stratum: {stratum}")
        exact_agreement = sum(row["a_label"] == row["b_label"] for row in stratum_outcomes)
        c_count = sum(row["decision_path"] == "c_adjudication" for row in stratum_outcomes)
        direct_full = sum(row["final_label"] == "fully_acceptable" for row in stratum_outcomes)
        unresolved = sum(row["final_label"] == "uncertain" for row in stratum_outcomes)
        stratum_rates[stratum] = {
            "reviewed_units": total,
            "direct_fully_acceptable": direct_full,
            "direct_fully_acceptable_rate": direct_full / total,
            "unresolved_cases": unresolved,
            "unresolved_case_rate": unresolved / total,
        }
        agreement_by_stratum[stratum] = {
            "reviewed_units": total,
            "exact_a_b_agreements": exact_agreement,
            "exact_a_b_agreement_rate": exact_agreement / total,
            "c_adjudications": c_count,
            "c_adjudication_rate": c_count / total,
        }
        strict_by_stratum[stratum] = {
            "strict_gold_rows": len(stratum_strict),
            "final_label_counts": dict(sorted(Counter(str(row["strict_gold_final_label"]) for row in stratum_strict).items())),
            "rejected_or_unreviewed": sum(
                not row["strict_gold_reviewed"] or row["strict_gold_final_label"] != "fully_acceptable"
                for row in stratum_strict
            ),
        }
    counts = {
        "scored_prompts": len(scored_prompt_ids),
        "reviewed_units": len(outcomes),
        "direct_fully_acceptable": len(direct_accepts),
        "acceptable_after_duplicate_closure": len(proposed),
        "added_direct_fully_acceptable": len(added_direct),
        "added_acceptable_after_duplicate_closure": len(added_proposed),
        "strict_gold_rejections": len(strict_rejections),
        "prompts_without_fully_acceptable": len(empty_prompts),
    }
    bindings = {
        "initial_plan_sha256": initial_manifest["plan_sha256"],
        "initial_validation_inventory_sha256": initial_inventory_sha,
        "adjudication_plan_sha256": c_plan_sha,
        "adjudication_validation_inventory_sha256": c_inventory_sha,
        "source_manifest_sha256": sha256_file(source_paths["source_manifest"]),
        "prompt_manifest_sha256": sha256_file(source_paths["prompt_manifest"]),
        "candidate_pool_sha256": sha256_file(source_paths["candidate_pool"]),
        "controller_sha256": controller_sha256(),
        "counts": counts,
        "strict_rejections": strict_rejections,
        "empty_prompts": empty_prompts,
        "added_direct": added_direct,
        "added_candidates": added_alternatives,
        "added_alternatives_sha256": canonical_sha256(added_alternatives),
        "audit_details": {
            "strict_versus_acceptable": {
                "strict_gold_status_by_stratum": strict_by_stratum,
                "strict_gold_rejections": strict_rejections,
            },
            "added_alternatives": added_alternatives,
            "unresolved_cases": unresolved_cases,
            "reviewer_agreement": {
                "a_b_ordered_label_pair_counts": dict(sorted(pair_counts.items())),
                "by_stratum": agreement_by_stratum,
            },
            "per_stratum_rates": stratum_rates,
        },
    }
    return outcomes, proposed, strict_status, bindings


def hard_stop_rules(outcomes: list[dict[str, Any]], bindings: dict[str, Any]) -> dict[str, bool]:
    return {
        "all_review_units_resolved": len(outcomes) == 7_710 and all(row["final_label"] for row in outcomes),
        "exact_scored_prompt_identity_covered": bindings["counts"]["scored_prompts"] == 389,
        "strict_gold_not_rejected": not bindings["strict_rejections"],
        "each_scored_prompt_has_fully_acceptable": not bindings["empty_prompts"],
    }


def proposal_state(hard_stops: dict[str, bool]) -> str:
    return "pending_independent_review" if all(hard_stops.values()) else "blocked_stop_rules"


def report_data(state: str, proposal_sha: str, hard_stops: dict[str, bool], bindings: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": VERSION,
        "state": state,
        "proposal_sha256": proposal_sha,
        "decision_rule": "A/B agreement decides when no C record exists; C decides every eligible potential-acceptability disagreement; only final fully_acceptable candidates enter the set, followed by exact-I2 source-hash duplicate closure.",
        "stop_rules": hard_stops,
        "review_required": {
            "independent_metadata_review": True,
            "added_acceptable_candidates_require_pattern_review": bool(bindings["added_candidates"]),
            "added_acceptable_candidate_count": len(bindings["added_candidates"]),
            "added_acceptable_candidates_sha256": bindings["added_alternatives_sha256"],
            "automatic_unanticipated_pattern_disposition": "not_decided",
        },
        "counts": bindings["counts"],
        "strict_versus_acceptable": bindings["audit_details"]["strict_versus_acceptable"],
        "added_alternatives": bindings["audit_details"]["added_alternatives"],
        "unresolved_cases": bindings["audit_details"]["unresolved_cases"],
        "reviewer_agreement": bindings["audit_details"]["reviewer_agreement"],
        "per_stratum_rates": bindings["audit_details"]["per_stratum_rates"],
        "network_calls": 0,
        "provider_calls": 0,
        "retrieval_or_selector_runs": 0,
    }


def build_proposal(root: Path) -> dict[str, Any]:
    output = paths(root)
    require(not any(path.exists() for key, path in output.items() if key not in {"review", "final", "final_manifest"}), "Freeze proposal already exists")
    outcomes, proposed, strict_status, bindings = proposal_data(root)
    hard_stops = hard_stop_rules(outcomes, bindings)
    state = proposal_state(hard_stops)
    write_jsonl_new(output["outcomes"], outcomes)
    write_jsonl_new(output["proposal"], proposed)
    write_jsonl_new(output["strict"], strict_status)
    report = report_data(state, sha256_file(output["proposal"]), hard_stops, bindings)
    write_json_new(output["report"], report)
    manifest = {
        "schema_version": VERSION,
        "state": state,
        **{key: bindings[key] for key in PROPOSAL_MANIFEST_FIELDS if key in bindings},
        "scored_prompts": bindings["counts"]["scored_prompts"],
        "reviewed_units": bindings["counts"]["reviewed_units"],
        "direct_fully_acceptable": bindings["counts"]["direct_fully_acceptable"],
        "acceptable_after_duplicate_closure": bindings["counts"]["acceptable_after_duplicate_closure"],
        "added_direct_fully_acceptable": bindings["counts"]["added_direct_fully_acceptable"],
        "added_acceptable_after_duplicate_closure": bindings["counts"]["added_acceptable_after_duplicate_closure"],
        "added_alternatives_sha256": bindings["added_alternatives_sha256"],
        "strict_gold_rejections": bindings["counts"]["strict_gold_rejections"],
        "prompts_without_fully_acceptable": bindings["counts"]["prompts_without_fully_acceptable"],
        "proposal_path": str(output["proposal"].relative_to(root)),
        "proposal_sha256": sha256_file(output["proposal"]),
        "outcomes_path": str(output["outcomes"].relative_to(root)),
        "outcomes_sha256": sha256_file(output["outcomes"]),
        "strict_status_path": str(output["strict"].relative_to(root)),
        "strict_status_sha256": sha256_file(output["strict"]),
        "report_path": str(output["report"].relative_to(root)),
        "report_sha256": sha256_file(output["report"]),
        "network_calls": 0,
        "provider_calls": 0,
        "raw_text_in_outputs": False,
    }
    require(set(manifest) == PROPOSAL_MANIFEST_FIELDS, "Proposal-manifest schema mismatch")
    write_json_new(output["manifest"], manifest)
    return manifest


def load_proposal(root: Path) -> tuple[dict[str, Any], dict[str, Path], dict[str, bool]]:
    output = paths(root)
    manifest = read_json(output["manifest"])
    require(set(manifest) == PROPOSAL_MANIFEST_FIELDS, "Proposal-manifest schema mismatch")
    require(manifest["schema_version"] == VERSION, "Proposal-manifest version mismatch")
    require(manifest["state"] in {"pending_independent_review", "blocked_stop_rules"}, "Proposal-manifest state mismatch")
    require(
        manifest["network_calls"] == manifest["provider_calls"] == 0 and manifest["raw_text_in_outputs"] is False,
        "Proposal-manifest boundary mismatch",
    )
    for name in ("proposal", "outcomes", "strict", "report"):
        require(output[name].is_file(), f"Missing proposal output: {name}")
    require(manifest["proposal_path"] == str(output["proposal"].relative_to(root)), "Proposal path mismatch")
    require(manifest["outcomes_path"] == str(output["outcomes"].relative_to(root)), "Outcomes path mismatch")
    require(manifest["strict_status_path"] == str(output["strict"].relative_to(root)), "Strict path mismatch")
    require(manifest["report_path"] == str(output["report"].relative_to(root)), "Report path mismatch")
    require(manifest["proposal_sha256"] == sha256_file(output["proposal"]), "Proposal hash mismatch")
    require(manifest["outcomes_sha256"] == sha256_file(output["outcomes"]), "Outcomes hash mismatch")
    require(manifest["strict_status_sha256"] == sha256_file(output["strict"]), "Strict hash mismatch")
    require(manifest["report_sha256"] == sha256_file(output["report"]), "Report hash mismatch")
    expected_outcomes, expected_proposal, expected_strict, expected_bindings = proposal_data(root)
    require(initial.read_jsonl(output["outcomes"]) == expected_outcomes, "Outcomes do not match revalidated review inputs")
    require(initial.read_jsonl(output["proposal"]) == expected_proposal, "Proposal does not match revalidated review inputs")
    require(initial.read_jsonl(output["strict"]) == expected_strict, "Strict-status file does not match revalidated review inputs")
    for key in (
        "initial_plan_sha256",
        "initial_validation_inventory_sha256",
        "adjudication_plan_sha256",
        "adjudication_validation_inventory_sha256",
        "source_manifest_sha256",
        "prompt_manifest_sha256",
        "candidate_pool_sha256",
        "controller_sha256",
    ):
        require(manifest[key] == expected_bindings[key], f"Proposal input binding drift: {key}")
    require(manifest["scored_prompts"] == expected_bindings["counts"]["scored_prompts"], "Proposal count drift")
    require(manifest["reviewed_units"] == expected_bindings["counts"]["reviewed_units"], "Proposal count drift")
    require(manifest["direct_fully_acceptable"] == expected_bindings["counts"]["direct_fully_acceptable"], "Proposal count drift")
    require(manifest["acceptable_after_duplicate_closure"] == expected_bindings["counts"]["acceptable_after_duplicate_closure"], "Proposal count drift")
    require(manifest["added_direct_fully_acceptable"] == expected_bindings["counts"]["added_direct_fully_acceptable"], "Proposal count drift")
    require(manifest["added_acceptable_after_duplicate_closure"] == expected_bindings["counts"]["added_acceptable_after_duplicate_closure"], "Proposal count drift")
    require(manifest["added_alternatives_sha256"] == expected_bindings["added_alternatives_sha256"], "Added-alternatives binding drift")
    require(manifest["strict_gold_rejections"] == expected_bindings["counts"]["strict_gold_rejections"], "Proposal count drift")
    require(manifest["prompts_without_fully_acceptable"] == expected_bindings["counts"]["prompts_without_fully_acceptable"], "Proposal count drift")
    expected_hard_stops = hard_stop_rules(expected_outcomes, expected_bindings)
    expected_state = proposal_state(expected_hard_stops)
    require(manifest["state"] == expected_state, "Proposal state does not match recomputed stop rules")
    report = read_json(output["report"])
    require(set(report) == REPORT_FIELDS, "Freeze-report schema mismatch")
    require(
        report == report_data(expected_state, manifest["proposal_sha256"], expected_hard_stops, expected_bindings),
        "Freeze report does not match recomputed audit state",
    )
    return manifest, output, expected_hard_stops


def validate_independent_review(
    manifest: dict[str, Any], output: dict[str, Path], recomputed_hard_stops: dict[str, bool]
) -> dict[str, Any]:
    review = read_json(output["review"])
    require(set(review) == INDEPENDENT_REVIEW_FIELDS, "Independent-review schema mismatch")
    require(review["schema_version"] == "rq2b-b0g-freeze-independent-review-v1", "Independent-review version mismatch")
    require(review["state"] in {"pass", "blocked"}, "Independent-review state mismatch")
    require(review["proposal_manifest_sha256"] == sha256_file(output["manifest"]), "Independent-review manifest binding mismatch")
    require(review["proposal_sha256"] == manifest["proposal_sha256"], "Independent-review proposal binding mismatch")
    require(review["outcomes_sha256"] == manifest["outcomes_sha256"], "Independent-review outcomes binding mismatch")
    require(review["strict_status_sha256"] == manifest["strict_status_sha256"], "Independent-review strict binding mismatch")
    require(review["report_sha256"] == manifest["report_sha256"], "Independent-review report binding mismatch")
    require(review["review_scope"] == INDEPENDENT_REVIEW_SCOPE, "Independent-review scope mismatch")
    require(isinstance(review["reviewer_id"], str) and review["reviewer_id"].strip(), "Independent-review provenance missing")
    require(review["reviewer_method"] == "independent_read_only_metadata_review", "Independent-review method mismatch")
    require(review["controller_sha256"] == manifest["controller_sha256"], "Independent-review controller binding mismatch")
    require(review["hard_stop_rules_checked"] == recomputed_hard_stops, "Independent review did not bind recomputed stop rules")
    report = read_json(output["report"])
    has_added_alternatives = report["review_required"]["added_acceptable_candidates_require_pattern_review"]
    expected_pass_assessment = (
        "no_unanticipated_pattern"
        if has_added_alternatives
        else "not_applicable"
    )
    require(review["added_alternatives_sha256"] == manifest["added_alternatives_sha256"], "Independent-review added-delta binding mismatch")
    require(review["added_alternatives_count"] == manifest["added_acceptable_after_duplicate_closure"], "Independent-review added-delta count mismatch")
    require(isinstance(review["rationale"], str) and len(review["rationale"].strip()) >= 40, "Independent-review rationale missing")
    require(
        isinstance(review["observations"], list)
        and review["observations"]
        and all(isinstance(item, str) and item.strip() for item in review["observations"]),
        "Independent-review observations missing",
    )
    require(review["network_calls"] == review["provider_calls"] == 0 and review["raw_text_reviewed"] is False, "Independent-review boundary mismatch")
    if review["state"] == "pass":
        require(all(recomputed_hard_stops.values()), "Hard stop rule blocks a passing review")
        require(review["added_alternative_pattern_assessment"] == expected_pass_assessment, "Added-alternative pattern blocks finalization")
        require(review["findings"] == [], "Independent review retains actionable findings")
        require(review["recommendation"] == "finalize", "Independent review does not recommend finalization")
    else:
        require(not all(recomputed_hard_stops.values()), "Blocked review lacks a hard-stop condition")
        require(review["added_alternative_pattern_assessment"] == "not_assessed_due_to_hard_stop_rules", "Blocked-review pattern assessment mismatch")
        require(isinstance(review["findings"], list) and review["findings"] and all(isinstance(item, str) and item.strip() for item in review["findings"]), "Blocked review lacks findings")
        require(review["recommendation"] == "do_not_finalize", "Blocked review recommendation mismatch")
    return review


def verify_independent_review(root: Path) -> dict[str, Any]:
    manifest, _, hard_stops = load_proposal(root)
    review = validate_independent_review(manifest, paths(root), hard_stops)
    return {
        "schema_version": VERSION,
        "state": "independent_review_pass" if review["state"] == "pass" else "independent_review_confirms_block",
        "proposal_manifest_sha256": sha256_file(paths(root)["manifest"]),
        "independent_review_sha256": sha256_file(paths(root)["review"]),
        "hard_stop_rules": hard_stops,
        "network_calls": 0,
        "provider_calls": 0,
        "retrieval_or_selector_runs": 0,
    }


def finalize(root: Path) -> dict[str, Any]:
    manifest, output, recomputed_hard_stops = load_proposal(root)
    require(manifest["state"] == "pending_independent_review", "Hard stop rule blocks finalization")
    require(all(recomputed_hard_stops.values()), "Recomputed hard stop rule blocks finalization")
    review = validate_independent_review(manifest, output, recomputed_hard_stops)
    require(review["state"] == "pass", "Independent review does not permit finalization")
    require(not output["final"].exists() and not output["final_manifest"].exists(), "Final acceptable set already exists")
    proposal_rows = initial.read_jsonl(output["proposal"])
    require(all(set(row) == ACCEPTABLE_FIELDS for row in proposal_rows), "Final proposal row schema mismatch")
    write_jsonl_new(output["final"], proposal_rows)
    final_manifest = {
        "schema_version": VERSION,
        "state": "frozen_acceptable_set_no_retrieval_authorized",
        "proposal_manifest_sha256": sha256_file(output["manifest"]),
        "independent_review_sha256": sha256_file(output["review"]),
        "final_acceptable_set_path": str(output["final"].relative_to(root)),
        "final_acceptable_set_sha256": sha256_file(output["final"]),
        "network_calls": 0,
        "provider_calls": 0,
        "retrieval_or_selector_runs": 0,
    }
    require(set(final_manifest) == FINAL_MANIFEST_FIELDS, "Final-manifest schema mismatch")
    write_json_new(output["final_manifest"], final_manifest)
    return final_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--build-proposal", action="store_true")
    actions.add_argument("--verify-independent-review", action="store_true")
    actions.add_argument("--finalize", action="store_true")
    parser.add_argument("--root", type=Path, default=initial.repo_root())
    args = parser.parse_args()
    root = args.root.resolve()
    if args.build_proposal:
        result = build_proposal(root)
    elif args.verify_independent_review:
        result = verify_independent_review(root)
    else:
        result = finalize(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
