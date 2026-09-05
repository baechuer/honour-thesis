#!/usr/bin/env python3
"""Materialise the current Master RQ2B-NC Phase-3 closure proof.

This is deliberately a *closure proof*, not an experiment or an audit-input
freeze.  It binds the current 3,813-source union, the changed-scope reviews,
and the explicitly limited historical inheritance decision.  Any drift in a
required input, count, reviewer outcome, or cue screen is a fail-closed block.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NC = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
M = NC / "manifests"
SOP = NC / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"

P0 = M / "rq2b_nc_master_phase0_reconciliation_2026-09-06_v1"
P1 = M / "rq2b_nc_master_phase1_reconciliation_2026-09-06_v1"
PRE = M / "rq2b_nc_master_phase3_preflight_2026-09-06_v1"
UNION_REVIEW = M / "rq2b_nc_master_phase3_source_union_review_2026-09-06_v2"
DELTA = M / "rq2b_nc_master_phase3_union_delta_proof_2026-09-06_v1"
SCOPE = M / "rq2b_nc_master_phase3_semantic_scope_2026-09-06_v1"
GAP = M / "rq2b_nc_master_phase3_gap_audit_2026-09-06_v1"
PACKETS = M / "rq2b_nc_master_phase3_changed_scope_qa_packets_2026-09-06_v1"
INTEGRITY = M / "rq2b_nc_master_phase3_return_integrity_2026-09-06_v2"
RECON = M / "rq2b_nc_master_phase3_changed_scope_qa_reconciliation_2026-09-06_v6"
HISTORICAL = M / "rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2/candidate_source_union.jsonl"

EXPECTED_PACKET_SHA = {
    "source_relation": "afe0a7ad34471fe61f61415432c8d3432be0c91eef45702659740ca020367fa2",
    "prompt_relation": "039c2bb7f7b77c006f4bf4c0570562453142f0cc0831770671053aca454fd963",
    "prompt_cue": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def check(checks: list[dict], blockers: list[dict], name: str, ok: bool, **detail: object) -> None:
    row = {"check": name, "status": "PASS" if ok else "BLOCK", **detail}
    checks.append(row)
    if not ok:
        blockers.append(row)


def find_audit(audits: list[dict], kind: str) -> dict | None:
    return next((audit for audit in audits if audit.get("kind") == kind), None)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        raise SystemExit(f"Refusing to overwrite append-only output: {output}")

    required = [
        SOP,
        P0 / "summary.json",
        P1 / "summary.json", P1 / "source_union.jsonl", P1 / "family_state_ledger.jsonl",
        PRE / "summary.json", PRE / "candidate_source_union.jsonl", PRE / "terminal_source_union.jsonl", PRE / "union_change_log.json",
        UNION_REVIEW / "report.json", DELTA / "report.json", SCOPE / "report.json", GAP / "report.json",
        PACKETS / "manifest.json", PACKETS / "source_relation_reviewer_packet.jsonl",
        PACKETS / "prompt_relation_reviewer_packet.jsonl", PACKETS / "prompt_cue_screen.jsonl",
        PACKETS / "prompt_cue_reviewer_packet.jsonl", INTEGRITY / "report.json",
        RECON / "summary.json", RECON / "final_record_status.jsonl", RECON / "sealed_disagreement_packets.jsonl",
        HISTORICAL,
    ]
    checks: list[dict] = []
    blockers: list[dict] = []
    input_hashes: dict[str, str] = {}
    for path in required:
        exists = path.is_file()
        check(checks, blockers, "required_input", exists, path=relative(path))
        if exists:
            input_hashes[relative(path)] = digest(path)
    if blockers:
        return write(output, checks, blockers, input_hashes, {}, {})

    phase0 = load_json(P0 / "summary.json")
    phase1 = load_json(P1 / "summary.json")
    preflight = load_json(PRE / "summary.json")
    union_review = load_json(UNION_REVIEW / "report.json")
    delta = load_json(DELTA / "report.json")
    semantic_scope = load_json(SCOPE / "report.json")
    gap = load_json(GAP / "report.json")
    packet_manifest = load_json(PACKETS / "manifest.json")
    integrity = load_json(INTEGRITY / "report.json")
    reconciliation = load_json(RECON / "summary.json")
    p1_sources = load_jsonl(P1 / "source_union.jsonl")
    terminal_sources = load_jsonl(PRE / "terminal_source_union.jsonl")
    current_union = load_jsonl(PRE / "candidate_source_union.jsonl")
    historical_union = load_jsonl(HISTORICAL)
    change_log = load_json(PRE / "union_change_log.json")
    source_packets = load_jsonl(PACKETS / "source_relation_reviewer_packet.jsonl")
    prompt_packets = load_jsonl(PACKETS / "prompt_relation_reviewer_packet.jsonl")
    cue_screen = load_jsonl(PACKETS / "prompt_cue_screen.jsonl")
    cue_packets = load_jsonl(PACKETS / "prompt_cue_reviewer_packet.jsonl")
    final_records = load_jsonl(RECON / "final_record_status.jsonl")
    sealed = load_jsonl(RECON / "sealed_disagreement_packets.jsonl")

    check(checks, blockers, "phase0_canonical_status",
          phase0.get("status") == "PASS_RQ2B_NC_PHASE0_CANONICAL_STATE_RECONCILIATION_NO_EXPERIMENT",
          observed=phase0.get("status"))
    check(checks, blockers, "phase1_canonical_status",
          phase1.get("status") == "PASS_RQ2B_NC_MASTER_PHASE1_RECONCILIATION_NO_EXPERIMENT",
          observed=phase1.get("status"), structural_count=phase1.get("structural_count"))
    check(checks, blockers, "phase1_no_experiment_gate",
          phase1.get("gates", {}).get("no_retrieval_or_embedding") is True,
          observed=phase1.get("gates", {}).get("no_retrieval_or_embedding"))
    check(checks, blockers, "preflight_expected_prior_status",
          preflight.get("status") == "BLOCKED_MASTER_PHASE3_PREFLIGHT",
          observed=preflight.get("status"))
    check(checks, blockers, "source_union_review_status",
          union_review.get("status") == "PASS_SOURCE_UNION_PREFLIGHT", observed=union_review.get("status"))
    check(checks, blockers, "source_union_review_no_retrieval",
          union_review.get("scope", {}).get("retrieval_outcomes_used") is False,
          observed=union_review.get("scope", {}).get("retrieval_outcomes_used"))

    p1_hashes = [row.get("canonical_source_sha256") for row in p1_sources]
    terminal_hashes = [row.get("canonical_source_sha256") for row in terminal_sources]
    union_hashes = [row.get("canonical_source_sha256") for row in current_union]
    historical_hashes = [row.get("canonical_source_sha256") for row in historical_union]
    p1_families = defaultdict(list)
    for row in p1_sources:
        p1_families[(row.get("batch"), row.get("family_token"))].append(row)
    b052 = [row for row in p1_sources if row.get("batch") == "B052"]
    added_rows = [row for row in p1_sources if row.get("batch") in {"B013", "B015"} and row.get("canonical_source_sha256") not in set(historical_hashes)]
    added_by_batch = Counter(row.get("batch") for row in added_rows)
    removed = set(change_log.get("removed_b052_hashes", []))
    additions = set(change_log.get("added_master_phase1_hashes", []))
    expected_rebuilt = (set(historical_hashes) - removed) | additions

    check(checks, blockers, "terminal_source_union_identity",
          len(p1_sources) == 147 and p1_hashes == terminal_hashes,
          phase1_rows=len(p1_sources), terminal_rows=len(terminal_sources), exact_order_equal=p1_hashes == terminal_hashes)
    check(checks, blockers, "terminal_triads",
          len(p1_families) == 49 and all(len(rows) == 3 and len({r.get("canonical_source_sha256") for r in rows}) == 3 for rows in p1_families.values()),
          families=len(p1_families), bad_families=[f"{key[0]}:{key[1]}" for key, rows in p1_families.items() if len(rows) != 3 or len({r.get('canonical_source_sha256') for r in rows}) != 3])
    check(checks, blockers, "terminal_exact_hashes",
          len(set(p1_hashes)) == 147 and all(isinstance(value, str) and len(value) == 64 for value in p1_hashes),
          unique_hashes=len(set(p1_hashes)))
    check(checks, blockers, "fresh_b052_three_member_closure",
          len(b052) == 9 and len({row.get("family_token") for row in b052}) == 3,
          b052_rows=len(b052), b052_families=len({row.get("family_token") for row in b052}))
    check(checks, blockers, "delta_counts_and_batches",
          len(historical_union) == 3810 and len(removed) == 6 and len(additions) == 9
          and len(current_union) == 3813 and additions == {row.get("canonical_source_sha256") for row in added_rows}
          and added_by_batch == Counter({"B013": 3, "B015": 6}),
          historical=len(historical_union), removed=len(removed), additions=len(additions), rebuilt=len(current_union), added_by_batch=dict(sorted(added_by_batch.items())))
    check(checks, blockers, "changed_scope_three_current_families",
          len({(row.get("batch"), row.get("family_token")) for row in added_rows}) == 3
          and all(len([row for row in added_rows if (row.get("batch"), row.get("family_token")) == family]) == 3
                  for family in {(row.get("batch"), row.get("family_token")) for row in added_rows}),
          changed_families=sorted(f"{batch}:{family}" for batch, family in {(row.get("batch"), row.get("family_token")) for row in added_rows}))
    check(checks, blockers, "delta_exact_union_replay",
          set(union_hashes) == expected_rebuilt and len(set(union_hashes)) == 3813,
          expected_unique=len(expected_rebuilt), observed_unique=len(set(union_hashes)), exact_set_equal=set(union_hashes) == expected_rebuilt)
    check(checks, blockers, "delta_proof_status_and_arithmetic",
          delta.get("status") == "PASS" and delta.get("counts", {}).get("arithmetic_check") == "3810 - 6 + 9 = 3813"
          and delta.get("counts", {}).get("added_by_batch") == {"B013": 3, "B015": 6},
          observed_status=delta.get("status"), arithmetic=delta.get("counts", {}).get("arithmetic_check"))

    check(checks, blockers, "changed_scope_basis",
          semantic_scope.get("status") == "FRESH_PHASE3_SEMANTIC_CUE_REVIEW_REQUIRED_FOR_DELTA"
          and semantic_scope.get("delta", {}).get("added_B013_source_records") == 3
          and semantic_scope.get("delta", {}).get("added_B015_source_records") == 6
          and semantic_scope.get("inheritance_audit", {}).get("new_prompt_text_needs_fresh_review") == 3,
          observed_status=semantic_scope.get("status"), delta=semantic_scope.get("delta"))
    check(checks, blockers, "historical_inheritance_limited_to_unchanged_scope",
          gap.get("freeze_status") == "BLOCKED_PENDING_FRESH_PHASE3_PREFLIGHT"
          and any(item.get("artifact_class") == "SOP_and_protocol_definitions" for item in gap.get("safe_hash_inheritance", []))
          and any(item.get("artifact_class") == "semantic_QA_and_final_phase3_admission" for item in gap.get("must_regenerate", [])),
          freeze_status=gap.get("freeze_status"), safe_classes=[x.get("artifact_class") for x in gap.get("safe_hash_inheritance", [])], must_regenerate=[x.get("artifact_class") for x in gap.get("must_regenerate", [])])

    check(checks, blockers, "changed_scope_packet_construction",
          packet_manifest.get("status") == "PASS_PACKET_CONSTRUCTION_ONLY_NO_SEMANTIC_APPROVAL"
          and packet_manifest.get("counts", {}).get("candidate_union") == 3813
          and packet_manifest.get("counts", {}).get("fresh_sources") == 9
          and packet_manifest.get("counts", {}).get("source_relation_packets") == 45
          and packet_manifest.get("counts", {}).get("prompt_relation_packets") == 45
          and packet_manifest.get("counts", {}).get("prompt_cue_screen") == 9
          and packet_manifest.get("counts", {}).get("prompt_cue_packets") == 0,
          observed_counts=packet_manifest.get("counts"))
    packet_files = {
        "source_relation": PACKETS / "source_relation_reviewer_packet.jsonl",
        "prompt_relation": PACKETS / "prompt_relation_reviewer_packet.jsonl",
        "prompt_cue": PACKETS / "prompt_cue_reviewer_packet.jsonl",
    }
    check(checks, blockers, "changed_scope_packet_hashes",
          all(digest(path) == EXPECTED_PACKET_SHA[kind] for kind, path in packet_files.items()),
          observed={kind: digest(path) for kind, path in packet_files.items()}, expected=EXPECTED_PACKET_SHA)
    check(checks, blockers, "changed_scope_packet_counts",
          len(source_packets) == len({row.get("packet_id") for row in source_packets}) == 45
          and len(prompt_packets) == len({row.get("packet_id") for row in prompt_packets}) == 45
          and len(cue_screen) == len({row.get("packet_id") for row in cue_screen}) == 9 and len(cue_packets) == 0,
          source_relation=len(source_packets), prompt_relation=len(prompt_packets), cue_screen=len(cue_screen), cue_packets=len(cue_packets))
    check(checks, blockers, "cue_screen_no_mechanical_identity_signal",
          all(row.get("mechanical_disposition") == "PASS_NO_MECHANICAL_CUE_SIGNAL" for row in cue_screen),
          dispositions=sorted({row.get("mechanical_disposition") for row in cue_screen}))

    source_audit = find_audit(integrity.get("audits", []), "source_relation")
    prompt_audit = find_audit(integrity.get("audits", []), "prompt_relation")
    cue_audit = find_audit(integrity.get("audits", []), "prompt_cue")
    def exact_ab(audit: dict | None, expected_sha: str, expected_rows: int) -> bool:
        if not audit or audit.get("expected") != expected_rows or audit.get("packet_sha256") != expected_sha:
            return False
        reviewers = audit.get("reviewers", {})
        return all(
            reviewers.get(label, {}).get("rows") == expected_rows
            and reviewers.get(label, {}).get("unique_ids") == expected_rows
            and reviewers.get(label, {}).get("duplicate_ids") == 0
            and reviewers.get(label, {}).get("missing_ids") == []
            and reviewers.get(label, {}).get("extra_ids") == []
            and reviewers.get(label, {}).get("bad_records") == []
            and reviewers.get(label, {}).get("all_sha_match") is True
            for label in ("A", "B")
        )
    check(checks, blockers, "return_integrity_status", integrity.get("status") == "PASS_RETURN_INTEGRITY", observed=integrity.get("status"))
    check(checks, blockers, "source_relation_two_reviewer_exact_agreement_integrity",
          exact_ab(source_audit, EXPECTED_PACKET_SHA["source_relation"], 45), observed=source_audit)
    check(checks, blockers, "prompt_relation_two_reviewer_exact_agreement_integrity",
          exact_ab(prompt_audit, EXPECTED_PACKET_SHA["prompt_relation"], 45), observed=prompt_audit)
    check(checks, blockers, "cue_zero_packet_legitimacy",
          cue_audit is not None and cue_audit.get("screen_rows") == 9 and cue_audit.get("screen_unique_ids") == 9
          and cue_audit.get("screen_all_no_signal") is True and cue_audit.get("packet_rows") == 0
          and cue_audit.get("packet_sha256") == EXPECTED_PACKET_SHA["prompt_cue"], observed=cue_audit)

    decisions = Counter(record.get("decision") for record in final_records)
    statuses = Counter(record.get("status") for record in final_records)
    check(checks, blockers, "changed_scope_v6_pass_and_no_coordinator",
          reconciliation.get("status") == "PASS_CHANGED_SCOPE_RECONCILIATION"
          and reconciliation.get("counts", {}).get("source_relation_packets") == 45
          and reconciliation.get("counts", {}).get("prompt_relation_packets") == 45
          and reconciliation.get("counts", {}).get("prompt_cue_packets") == 0
          and reconciliation.get("counts", {}).get("A_returns") == 90
          and reconciliation.get("counts", {}).get("B_returns") == 90
          and reconciliation.get("counts", {}).get("coordinator_returns") == 0
          and reconciliation.get("counts", {}).get("sealed_disagreements") == 0
          and reconciliation.get("retrieval_or_embedding_executed") is False
          and reconciliation.get("historical_decisions_inherited") is False
          and reconciliation.get("validation_errors") == [] and len(sealed) == 0,
          observed_status=reconciliation.get("status"), counts=reconciliation.get("counts"), retrieval_or_embedding_executed=reconciliation.get("retrieval_or_embedding_executed"), historical_decisions_inherited=reconciliation.get("historical_decisions_inherited"), validation_errors=reconciliation.get("validation_errors"))
    check(checks, blockers, "changed_scope_v6_terminal_agreement_decisions",
          len(final_records) == 90 and statuses == Counter({"RETAINED_AGREEMENT": 90})
          and decisions == Counter({"RELATED_BUT_DISTINCT": 90}),
          records=len(final_records), statuses=dict(statuses), decisions=dict(decisions))

    counts = {
        "historical_union": len(historical_union),
        "current_union": len(current_union),
        "union_removed_b052": len(removed),
        "union_added_B013_B015": len(additions),
        "terminal_source_rows": len(p1_sources),
        "terminal_families": len(p1_families),
        "source_relation_packets": len(source_packets),
        "prompt_relation_packets": len(prompt_packets),
        "prompt_cue_screen_rows": len(cue_screen),
        "prompt_cue_packets": len(cue_packets),
        "final_changed_scope_records": len(final_records),
    }
    inheritance = {
        "historical_scope": "Only unchanged historical records may retain immutable SOP/protocol and parent-V3 identity/result-reference bindings.",
        "changed_scope": "The three B013/B015 changed families are supplied by current v6 source/prompt relation proof; B052 removals supply no admission.",
        "forbidden_inference": "No historical Phase-3 admission, audit-input freeze, acceptable-set label, retrieval outcome, or metric is inherited.",
    }
    return write(output, checks, blockers, input_hashes, counts, inheritance)


def write(output: Path, checks: list[dict], blockers: list[dict], input_hashes: dict[str, str], counts: dict, inheritance: dict) -> int:
    output.mkdir(parents=True, exist_ok=False)
    status = "PASS_RQ2B_NC_MASTER_PHASE3_CLOSURE_NO_EXPERIMENT" if not blockers else "BLOCKED_RQ2B_NC_MASTER_PHASE3_CLOSURE"
    summary = {
        "status": status,
        "claim_boundary": "Phase-3 closure proof only. No audit-input freeze, K=6 execution, final-library update, acceptable-set assertion, retrieval, embedding, provider call, result, metric, or formal-experiment readiness is established.",
        "counts": counts,
        "input_sha256": dict(sorted(input_hashes.items())),
        "checks": checks,
        "blockers": blockers,
        "historical_inheritance_boundary": inheritance,
        "next_phase": "A separately authorised fresh Phase-4 audit-input method freeze/preflight remains required; this artifact does not perform it.",
    }
    (output / "phase3_closure_checks.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in checks), encoding="utf-8"
    )
    (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(output), "status": status, "blockers": len(blockers), "counts": counts}, sort_keys=True))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
