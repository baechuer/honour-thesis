#!/usr/bin/env python3
"""Materialise the SOP Phase-0 state from canonical RQ2b-NC ledgers.

This controller is deliberately read-mostly and non-overwriting.  It makes a
new state snapshot; it does not amend V3, historical preflights, reviewer
returns, or any semantic decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW = NC / "review"
MANIFESTS = NC / "manifests"
SOP = REVIEW / "RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
CHECKPOINT_DIR = MANIFESTS / "curation_closed_checkpoint_2026-08-31"
CHECKPOINT_SUMMARY = CHECKPOINT_DIR / "summary.json"
CHECKPOINT_CLUSTERS = CHECKPOINT_DIR / "curation_eligible_clusters.jsonl"
CHECKPOINT_PROMPTS = CHECKPOINT_DIR / "curation_eligible_prompts.jsonl"

# B013--B015 entered the Phase-0 snapshot before their target-blind local
# gates existed. Their later terminal dispositions are explicitly allocated to
# the Phase-1 controller. Re-reading their new gates here would double-count
# the same families across the two temporal strata.
PHASE1_TEMPORAL_HANDOFF_BATCHES = {"B013", "B014", "B015"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSONL input: {path}")
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSON input: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def label(number: int) -> str:
    return f"B{number:03d}"


def batch_root(number: int) -> Path:
    matches = sorted(REVIEW.glob(f"*/batch_{number:03d}_full_source_review_packets"))
    if len(matches) != 1:
        raise SystemExit(f"{label(number)} has {len(matches)} canonical batch roots, expected exactly one: {matches}")
    return matches[0]


def batch_parent(number: int) -> Path:
    if number == 53:
        matches = sorted(REVIEW.glob("source_native_*_b053_2026-09-05"))
        if len(matches) != 1:
            raise SystemExit(f"B053 parent is ambiguous: {matches}")
        return matches[0]
    return batch_root(number).parent


def discovery_ledger(number: int) -> Path:
    """Pick the single root-level source-family ledger for one discovery batch."""
    parent = batch_parent(number)
    expected = [
        f"batch_{number:03d}_full_source_review_queue_internal.jsonl",
        f"b{number:03d}_source_native_semantic_family_queue.jsonl",
        "source_native_reciprocal_family_ledger.jsonl",
        "source_native_discovery_ledger.jsonl",
    ]
    for name in expected:
        candidate = parent / name
        if candidate.is_file():
            rows = read_jsonl(candidate)
            selected = [
                row for row in rows
                if str(row.get("batch_id", "")).endswith(label(number))
                and isinstance(row.get("member_source_sha256"), list)
            ]
            if len(selected) == 25 and all(len(row["member_source_sha256"]) == 3 for row in selected):
                return candidate
    raise SystemExit(f"No canonical 25-by-3 discovery ledger for {label(number)} under {parent}")


def canonical_source_final(root: Path) -> Path:
    path = root / "reconciliation/final_dispositions/reconciled_family_dispositions.jsonl"
    if not path.is_file():
        raise SystemExit(f"Missing canonical full-source final disposition: {path}")
    return path


def provenance_dispositions(root: Path) -> Path | None:
    path = root / "reconciliation/pass_provenance_preflight/pass_family_provenance_dispositions.jsonl"
    return path if path.is_file() else None


def active_local_gate(root: Path) -> tuple[Path, Path, str] | None:
    """Select the deepest valid local family/prompt gate without overwriting history."""
    authoring = root / "reconciliation/prompt_authoring"
    consolidations = sorted(authoring.glob("batch_*_post_cue_remediation_consolidation"))
    valid = [
        directory for directory in consolidations
        if (directory / "family_gate_dispositions.jsonl").is_file()
        and (directory / "active_prompt_dispositions.jsonl").is_file()
    ]
    if len(valid) > 1:
        raise SystemExit(f"Ambiguous post-cue consolidations under {authoring}: {valid}")
    if valid:
        return (
            valid[0] / "family_gate_dispositions.jsonl",
            valid[0] / "active_prompt_dispositions.jsonl",
            "POST_CUE_REMEDIATION_CONSOLIDATION",
        )
    remediation = authoring / "cue_remediation/target_blind_adequacy_packets/reconciliation/final_prompt_dispositions"
    if (remediation / "family_gate_dispositions.jsonl").is_file() and (remediation / "reconciled_prompt_dispositions.jsonl").is_file():
        return (
            remediation / "family_gate_dispositions.jsonl",
            remediation / "reconciled_prompt_dispositions.jsonl",
            "ONE_TIME_REMEDIATION_REBLIND_FINALIZER",
        )
    initial = authoring / "target_blind_adequacy_packets/reconciliation/final_prompt_dispositions"
    if (initial / "family_gate_dispositions.jsonl").is_file() and (initial / "reconciled_prompt_dispositions.jsonl").is_file():
        return (
            initial / "family_gate_dispositions.jsonl",
            initial / "reconciled_prompt_dispositions.jsonl",
            "INITIAL_TARGET_BLIND_FINALIZER",
        )
    return None


def require_token(row: dict[str, Any], key: str, context: str) -> str:
    value = str(row.get(key, ""))
    if not value:
        raise SystemExit(f"Missing {key} in {context}: {row}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise a non-overwriting RQ2b-NC Phase-0 state snapshot.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REVIEW / "rq2b_nc_phase0_state_reconciliation_2026-09-05",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = args.output_dir.resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite an existing Phase-0 snapshot: {out}")
    for path in (SOP, CHECKPOINT_SUMMARY, CHECKPOINT_CLUSTERS, CHECKPOINT_PROMPTS):
        if not path.is_file():
            raise SystemExit(f"Missing Phase-0 anchor: {path}")

    bound_inputs: dict[str, str] = {}
    for path in (SOP, CHECKPOINT_SUMMARY, CHECKPOINT_CLUSTERS, CHECKPOINT_PROMPTS):
        bound_inputs[relative(path)] = sha256(path)
    checkpoint = read_json(CHECKPOINT_SUMMARY)
    checkpoint_clusters = read_jsonl(CHECKPOINT_CLUSTERS)
    checkpoint_prompts = read_jsonl(CHECKPOINT_PROMPTS)
    if (len(checkpoint_clusters), len(checkpoint_prompts)) != (54, 125):
        raise SystemExit("Frozen checkpoint drift: expected 54 clusters and 125 prompts")

    discovery_by_batch: dict[str, list[dict[str, Any]]] = {}
    discovery_path_by_batch: dict[str, Path] = {}
    source_occurrences: dict[str, list[dict[str, str]]] = defaultdict(list)
    for number in range(1, 54):
        batch = label(number)
        path = discovery_ledger(number)
        rows = [
            row for row in read_jsonl(path)
            if str(row.get("batch_id", "")).endswith(batch)
            and isinstance(row.get("member_source_sha256"), list)
        ]
        if len(rows) != 25 or any(len(row["member_source_sha256"]) != 3 for row in rows):
            raise SystemExit(f"{batch} discovery ledger is not exactly 25 three-source families: {path}")
        ids = [require_token(row, "family_id", batch) for row in rows]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"Duplicate family_id in {batch} discovery ledger")
        discovery_by_batch[batch] = rows
        discovery_path_by_batch[batch] = path
        bound_inputs[relative(path)] = sha256(path)
        for row in rows:
            family_id = str(row["family_id"])
            for source_hash in row["member_source_sha256"]:
                source_hash = str(source_hash)
                if len(source_hash) != 64:
                    raise SystemExit(f"Malformed source hash in {batch}: {source_hash}")
                source_occurrences[source_hash].append({"batch": batch, "family_id": family_id})

    family_rows: list[dict[str, Any]] = []
    batch_rows: list[dict[str, Any]] = []
    eligible_source_hashes: set[str] = set()
    eligible_prompts = 0
    for number in range(1, 52):
        batch = label(number)
        root = batch_root(number)
        source_path = canonical_source_final(root)
        bound_inputs[relative(source_path)] = sha256(source_path)
        source_rows = read_jsonl(source_path)
        if len(source_rows) != 25:
            raise SystemExit(f"{batch} source-final record must contain 25 families")
        provenance_path = provenance_dispositions(root)
        provenance_by_family: dict[str, dict[str, Any]] = {}
        if provenance_path is not None:
            bound_inputs[relative(provenance_path)] = sha256(provenance_path)
            provenance_by_family = {
                require_token(row, "family_token", str(provenance_path)): row
                for row in read_jsonl(provenance_path)
            }
        active = None if batch in PHASE1_TEMPORAL_HANDOFF_BATCHES else active_local_gate(root)
        gate_by_family: dict[str, dict[str, Any]] = {}
        prompt_rows: list[dict[str, Any]] = []
        gate_kind = (
            "EXPLICIT_PHASE1_TEMPORAL_HANDOFF"
            if batch in PHASE1_TEMPORAL_HANDOFF_BATCHES
            else "NO_LOCAL_GATE_OUTPUT"
        )
        if active is not None:
            family_path, prompt_path, gate_kind = active
            bound_inputs[relative(family_path)] = sha256(family_path)
            bound_inputs[relative(prompt_path)] = sha256(prompt_path)
            gate_by_family = {
                require_token(row, "family_token", str(family_path)): row
                for row in read_jsonl(family_path)
            }
            prompt_rows = read_jsonl(prompt_path)
        state_counts: Counter[str] = Counter()
        for source_row in source_rows:
            family = require_token(source_row, "family_token", str(source_path))
            decision = require_token(source_row, "final_decision", str(source_path))
            if decision.startswith("DEFER_"):
                state = "DEFERRED_SOURCE_NATIVE_FAMILY_GATE"
                provenance_state = "NOT_APPLICABLE_SOURCE_DEFER"
                gate_state = "NOT_RUN_SOURCE_DEFER"
            elif decision != "PASS_TO_PROMPT_AUTHORING":
                state = "EXCLUDED_SOURCE_NATIVE_FAMILY_GATE"
                provenance_state = "NOT_APPLICABLE_SOURCE_REJECT"
                gate_state = "NOT_APPLICABLE_SOURCE_REJECT"
            else:
                provenance = provenance_by_family.get(family)
                if provenance is None:
                    state = "IN_FLIGHT_PROVENANCE_GATE_REQUIRED"
                    provenance_state = "MISSING"
                    gate_state = "NOT_RUN"
                else:
                    provenance_state = require_token(provenance, "family_provenance_preflight_status", str(provenance_path))
                    if provenance_state != "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE":
                        state = "DEFERRED_PROVENANCE_OR_LICENSE"
                        gate_state = "NOT_RUN"
                    else:
                        gate = gate_by_family.get(family)
                        if gate is None:
                            state = "IN_FLIGHT_TARGET_BLIND_REVIEW_REQUIRED"
                            gate_state = "MISSING"
                        else:
                            gate_state = require_token(gate, "family_disposition", "local family gate")
                            if gate_state == "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT":
                                state = "LOCAL_GATE_ELIGIBLE"
                                relevant_prompts = [row for row in prompt_rows if str(row.get("family_token", "")) == family]
                                if len(relevant_prompts) != 3:
                                    raise SystemExit(f"{batch} eligible {family} does not bind exactly three active prompt rows")
                                eligible_prompts += 3
                            elif gate_state == "RETAIN_AS_UNADMITTED_REVIEW_RECORD":
                                state = "UNADMITTED_LOCAL_GATE"
                            else:
                                raise SystemExit(f"Unexpected local family disposition in {batch}: {gate_state}")
            state_counts[state] += 1
            family_rows.append({
                "record_type": "source_native_family_phase0_state",
                "batch": batch,
                "family_token": family,
                "source_final_decision": decision,
                "provenance_state": provenance_state,
                "local_gate_selection": gate_kind,
                "local_gate_state": gate_state,
                "phase0_state": state,
                "claim_boundary": "Phase-0 state only; no whole-library acceptable-set or final-library admission is established.",
            })
        batch_rows.append({
            "record_type": "source_native_batch_phase0_state",
            "batch": batch,
            "family_count": len(source_rows),
            "state_counts": dict(sorted(state_counts.items())),
            "canonical_discovery_ledger": relative(discovery_path_by_batch[batch]),
            "canonical_source_final": relative(source_path),
            "canonical_provenance": relative(provenance_path) if provenance_path else None,
            "canonical_local_gate_kind": gate_kind,
            "phase0_batch_state": "CLOSED_LOCAL_GATE" if not any(key.startswith("IN_FLIGHT") for key in state_counts) else "IN_FLIGHT_WITH_EXPLICIT_NEXT_GATE",
        })

        if active is not None:
            eligible_tokens = {
                row["family_token"] for row in gate_by_family.values()
                if row.get("family_disposition") == "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
            }
            if eligible_tokens:
                provenance_sources = root / "reconciliation/pass_provenance_preflight/pass_family_source_provenance_preflight.jsonl"
                if not provenance_sources.is_file():
                    raise SystemExit(f"{batch} eligible family lacks source provenance ledger")
                bound_inputs[relative(provenance_sources)] = sha256(provenance_sources)
                for row in read_jsonl(provenance_sources):
                    if str(row.get("family_token", "")) in eligible_tokens:
                        source_hash = str(row.get("canonical_source_sha256", ""))
                        if len(source_hash) != 64:
                            raise SystemExit(f"Malformed eligible source hash in {batch}")
                        eligible_source_hashes.add(source_hash)

    b052 = label(52)
    b052_root = batch_root(52)
    b052_a_plural = b052_root / "reviewer_a_returns.jsonl"
    b052_b = b052_root / "reviewer_b_return.jsonl"
    b052_packet = b052_root / "reviewer_a_packet.jsonl"
    for path in (b052_a_plural, b052_b, b052_packet):
        if not path.is_file():
            raise SystemExit(f"B052 expected A/B source-review input is missing: {path}")
        bound_inputs[relative(path)] = sha256(path)
    if len(read_jsonl(b052_a_plural)) != 25 or len(read_jsonl(b052_b)) != 25 or len(read_jsonl(b052_packet)) != 25:
        raise SystemExit("B052 A/B source-review coverage is not 25 records")
    for row in discovery_by_batch[b052]:
        family_rows.append({
            "record_type": "source_native_family_phase0_state",
            "batch": b052,
            "family_token": str(row["family_id"]),
            "source_final_decision": "NOT_YET_RECONCILED",
            "provenance_state": "NOT_RUN",
            "local_gate_selection": "NOT_RUN",
            "local_gate_state": "NOT_RUN",
            "phase0_state": "IN_FLIGHT_SOURCE_AB_RECONCILIATION_REQUIRED",
            "claim_boundary": "Phase-0 state only; no semantic or admission decision is implied by an un-reconciled A/B review.",
        })
    batch_rows.append({
        "record_type": "source_native_batch_phase0_state",
        "batch": b052,
        "family_count": 25,
        "state_counts": {"IN_FLIGHT_SOURCE_AB_RECONCILIATION_REQUIRED": 25},
        "canonical_discovery_ledger": relative(discovery_path_by_batch[b052]),
        "canonical_source_final": None,
        "canonical_provenance": None,
        "canonical_local_gate_kind": "NOT_RUN",
        "phase0_batch_state": "IN_FLIGHT_WITH_EXPLICIT_NEXT_GATE",
        "compatibility_requirement": "Create only a relative reviewer_a_return.jsonl -> reviewer_a_returns.jsonl symlink before canonical reconciliation; preserve both return bytes.",
    })

    b053 = label(53)
    b053_rows = discovery_by_batch[b053]
    b053_source_to_families: dict[str, set[str]] = defaultdict(set)
    for row in b053_rows:
        for source_hash in row["member_source_sha256"]:
            b053_source_to_families[str(source_hash)].add(str(row["family_id"]))
    b053_conflicts = {source: sorted(families) for source, families in b053_source_to_families.items() if len(families) > 1}
    b053_quarantine: list[dict[str, Any]] = []
    residual: list[str] = []
    for row in b053_rows:
        family = str(row["family_id"])
        conflicting = sorted({source for source in row["member_source_sha256"] if source in b053_conflicts})
        if conflicting:
            state = "QUARANTINED_SOP_SOURCE_DISJOINTNESS_VIOLATION"
            b053_quarantine.append({
                "record_type": "source_disjointness_quarantine",
                "batch": b053,
                "family_id": family,
                "disposition": state,
                "supersedes_disposition_for_admission": "DEFER_UNREVIEWED_FULL_SOURCE_REQUIRED",
                "gate": "SOP_PHASE_1_SOURCE_NATIVE_AND_SOURCE_DISJOINT",
                "blocker": "WITHIN_B053_REUSED_CANONICAL_SOURCE_SHA256",
                "conflicting_source_sha256": conflicting,
                "conflicting_family_ids": sorted({other for source in conflicting for other in b053_conflicts[source] if other != family}),
                "review_admission_status": "INELIGIBLE_NO_REVIEW_NO_PROMPT_NO_ADMISSION",
                "artifact_preservation": "ORIGINAL_QUEUE_REPLAY_DEFER_AND_SUMMARY_RETAINED_UNMODIFIED",
                "reopen_condition": "NEW_SOURCE_DISJOINT_DISCOVERY_SELECTION_ONLY",
            })
        else:
            state = "DEFERRED_UNREVIEWED_FULL_SOURCE_REQUIRED"
            residual.append(family)
        family_rows.append({
            "record_type": "source_native_family_phase0_state",
            "batch": b053,
            "family_token": family,
            "source_final_decision": "NOT_RUN",
            "provenance_state": "NOT_RUN",
            "local_gate_selection": "NOT_RUN",
            "local_gate_state": "NOT_RUN",
            "phase0_state": state,
            "claim_boundary": "Phase-0 state only; preserved discovery material is not a source-native family admission.",
        })
    if (len(b053_quarantine), len(residual)) != (23, 2):
        raise SystemExit(f"Unexpected B053 source-disjointness partition: {len(b053_quarantine)} quarantined, {len(residual)} residual")
    b052_hashes = {source for row in discovery_by_batch[b052] for source in row["member_source_sha256"]}
    b053_hashes = {source for row in b053_rows for source in row["member_source_sha256"]}
    if b052_hashes & b053_hashes:
        raise SystemExit("B053 residual discovery is not source-disjoint from B052")
    b053_quarantine.append({
        "record_type": "batch_disposition",
        "batch": b053,
        "disposition": "PARTIALLY_QUARANTINED_SOURCE_DISJOINTNESS_GATE_FAILURE",
        "quarantined_family_count": len(b053_quarantine),
        "residual_family_ids": sorted(residual),
        "residual_status": "DEFERRED_UNREVIEWED_FULL_SOURCE_REQUIRED",
        "supersedes_batch_status_for_admission": "PASS_B053_DISCOVERY_QUEUE_ONLY_UNREVIEWED",
        "artifact_preservation": "ORIGINAL_QUEUE_REPLAY_DEFER_AND_SUMMARY_RETAINED_UNMODIFIED",
    })
    batch_rows.append({
        "record_type": "source_native_batch_phase0_state",
        "batch": b053,
        "family_count": 25,
        "state_counts": {
            "DEFERRED_UNREVIEWED_FULL_SOURCE_REQUIRED": len(residual),
            "QUARANTINED_SOP_SOURCE_DISJOINTNESS_VIOLATION": len(b053_quarantine) - 1,
        },
        "canonical_discovery_ledger": relative(discovery_path_by_batch[b053]),
        "canonical_source_final": None,
        "canonical_provenance": None,
        "canonical_local_gate_kind": "NOT_RUN",
        "phase0_batch_state": "CLOSED_WITH_EXPLICIT_DEFER_OR_QUARANTINE",
    })

    if len(family_rows) != 53 * 25:
        raise SystemExit(f"Unexpected Phase-0 family coverage: {len(family_rows)}")
    state_counts = Counter(str(row["phase0_state"]) for row in family_rows)
    native_eligible = state_counts["LOCAL_GATE_ELIGIBLE"]
    if (native_eligible, eligible_prompts, len(eligible_source_hashes)) != (167, 501, 501):
        raise SystemExit(
            "Phase-0 local-gate replay drift: "
            f"families={native_eligible}, prompts={eligible_prompts}, sources={len(eligible_source_hashes)}"
        )

    source_rows = []
    for source_hash, occurrences in sorted(source_occurrences.items()):
        by_batch = Counter(item["batch"] for item in occurrences)
        source_rows.append({
            "record_type": "source_native_inspection_union",
            "canonical_source_sha256": source_hash,
            "inspection_occurrence_count": len(occurrences),
            "inspection_batches": sorted(by_batch),
            "occurrences_by_batch": dict(sorted(by_batch.items())),
            "locally_eligible_source": source_hash in eligible_source_hashes,
            "source_reuse_status": "UNIQUE_INSPECTION_SOURCE" if len(occurrences) == 1 else "REUSED_INSPECTION_SOURCE_RETAINED_NONADMISSION_EVIDENCE",
        })
    if (sum(len(row["member_source_sha256"]) for rows in discovery_by_batch.values() for row in rows), len(source_rows)) != (3975, 3922):
        raise SystemExit("Phase-0 source-union replay drift")

    out.mkdir(parents=True)
    outputs = {
        "phase0_batch_state.jsonl": sorted(batch_rows, key=lambda row: row["batch"]),
        "phase0_family_state.jsonl": sorted(family_rows, key=lambda row: (row["batch"], row["family_token"])),
        "phase0_source_native_inspection_union.jsonl": source_rows,
        "phase0_b053_source_disjointness_quarantine.jsonl": b053_quarantine,
    }
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
    summary = {
        "status": "PASS_RQ2B_NC_PHASE0_CANONICAL_STATE_RECONCILIATION_NO_EXPERIMENT",
        "sop": relative(SOP),
        "status_interpretation": "Every inspected batch has an explicit eligible, unadmitted, deferred, excluded, quarantined or in-flight disposition. In-flight is a declared next local gate, not an ambiguity or admission.",
        "counts": {
            "frozen_checkpoint_clusters": 54,
            "frozen_checkpoint_prompts": 125,
            "source_native_discovery_families": len(family_rows),
            "source_native_inspection_occurrences": 3975,
            "source_native_inspection_exact_hash_unique": len(source_rows),
            "source_native_local_gate_eligible_families": native_eligible,
            "source_native_local_gate_eligible_prompts": eligible_prompts,
            "source_native_local_gate_eligible_exact_sources": len(eligible_source_hashes),
            "structural_cluster_progress_including_frozen_checkpoint": 54 + native_eligible,
            "clusters_remaining_to_300_including_frozen_checkpoint": 300 - (54 + native_eligible),
            "family_state_counts": dict(sorted(state_counts.items())),
        },
        "special_controls": {
            "b050_b049_cross_batch_source_reuse": "RETAINED_AS_INSPECTION_PROVENANCE_ONLY; B050 duplicate triad is not locally eligible.",
            "b052": "A/B returns are complete; a relative singular-name symlink is the only allowed compatibility bridge before source reconciliation.",
            "b053": "23 families quarantined for within-batch source reuse; 2 source-disjoint residual families are deferred unreviewed; all original discovery artifacts remain untouched.",
            "b054": "No canonical B054 discovery artifact exists at this snapshot and it is not a started batch.",
        },
        "bound_inputs": dict(sorted(bound_inputs.items())),
        "outputs": {name: sha256(out / name) for name in outputs},
        "claim_boundary": "Phase-0 reconstruction only. No K=6 proposal, acceptable-set label, final library admission, embedding, reranking, provider call, retrieval result, metric or thesis-result update is produced.",
    }
    write_json(out / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
