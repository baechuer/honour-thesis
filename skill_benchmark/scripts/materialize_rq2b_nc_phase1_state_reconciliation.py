#!/usr/bin/env python3
"""Materialise a bounded, non-overwriting RQ2b-NC Phase-1 state snapshot.

The snapshot joins only the named post-Phase-0 terminal local-gate artifacts to
their root full-source reconciliation keys.  It deliberately does not make a
whole-library source union, acceptable-set decision, or final-library claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW = NC / "review"
MANIFESTS = NC / "manifests"
PHASE0 = REVIEW / "rq2b_nc_phase0_state_reconciliation_2026-09-05_v2"
PHASE0_SUMMARY = PHASE0 / "summary.json"
PHASE0_FAMILIES = PHASE0 / "phase0_family_state.jsonl"
PHASE0_SOURCES = PHASE0 / "phase0_source_native_inspection_union.jsonl"
CHECKPOINT = MANIFESTS / "curation_closed_checkpoint_2026-08-31/summary.json"

# This is intentionally an explicit, closed input list.  Do not replace it
# with glob discovery: later batches must not silently enter this snapshot.
POST_PHASE0_SPECS = (
    ("B013", "source_native_dense_lexical_union_b013_2026-09-04"),
    ("B014", "source_native_dense_lexical_union_b014_2026-09-04"),
    ("B015", "source_native_dense_lexical_union_b015_2026-09-04"),
    ("B052", "source_native_marketing_advertising_seo_social_community_web_analytics_journalism_publishing_localisation_communications_b052_2026-09-05"),
    ("B054", "source_native_remaining_pool_disjoint_lexical_b054_2026-09-05"),
    ("B055", "source_native_remaining_pool_disjoint_lexical_b055_2026-09-05"),
    ("B056", "source_native_remaining_pool_disjoint_lexical_b056_2026-09-05"),
    ("B057", "source_native_remaining_pool_disjoint_lexical_b057_2026-09-05"),
    ("B058", "source_native_remaining_pool_disjoint_lexical_b058_2026-09-05"),
    ("B059", "source_native_remaining_pool_disjoint_lexical_b059_2026-09-05"),
    ("B060", "source_native_low_cue_workflow_b060_2026-09-05"),
    ("B061", "source_native_low_cue_workflow_b061_2026-09-05"),
    ("B062", "source_native_low_cue_workflow_b062_2026-09-05"),
    ("B063", "source_native_low_cue_workflow_b063_2026-09-05"),
    ("B064", "source_native_low_cue_workflow_b064_2026-09-05"),
)
B065_PARENT = REVIEW / "source_native_low_cue_workflow_b065_2026-09-05"
B065_ROOT = B065_PARENT / "batch_065_full_source_review_packets"
B065_KEY = B065_ROOT / "internal_reconciliation_key.jsonl"
B065_QUEUE = B065_PARENT / "b065_source_native_semantic_family_queue.jsonl"
B065_DISCOVERY_MANIFEST = B065_PARENT / "historical_source_exclusion_manifest.json"
B065_TERMINAL_FAMILIES = B065_ROOT / "reconciliation/prompt_authoring/cue_remediation/remediation_cap_closure/terminal_family_dispositions.jsonl"
B065_TERMINAL_PROMPTS = B065_ROOT / "reconciliation/prompt_authoring/cue_remediation/remediation_cap_closure/terminal_prompt_dispositions.jsonl"
ELIGIBLE = "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
PASS_PROMPT = "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
CLAIM_BOUNDARY = (
    "Current local state only. This establishes neither a whole-library "
    "acceptable-set outcome nor a global source-unique/final-library count."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSON input: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Canonical JSON object required: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSONL input: {path}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise SystemExit(f"Canonical JSONL object rows required: {path}")
    return rows


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8", newline="\n")


def require_text(row: dict[str, Any], key: str, context: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"Missing non-empty {key} in {context}: {row}")
    return value


def batch_paths(batch: str, parent_name: str) -> tuple[Path, Path, Path | None]:
    parent = REVIEW / parent_name
    root = parent / f"batch_{batch[1:]}_full_source_review_packets"
    gate = root / "reconciliation/prompt_authoring/target_blind_adequacy_packets/reconciliation/final_prompt_dispositions/family_gate_dispositions.jsonl"
    key = root / "internal_reconciliation_key.jsonl"
    discovery = parent / "historical_source_exclusion_manifest.json" if batch >= "B054" else None
    return gate, key, discovery


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise the bounded RQ2b-NC Phase-1 structural state.")
    parser.add_argument("--output-dir", type=Path, default=REVIEW / "rq2b_nc_phase1_state_reconciliation_2026-09-05_v3")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = args.output_dir.resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite an existing Phase-1 snapshot: {out}")

    bound_inputs: dict[str, str] = {}
    for path in (PHASE0_SUMMARY, PHASE0_FAMILIES, PHASE0_SOURCES, CHECKPOINT):
        if not path.is_file():
            raise SystemExit(f"Missing Phase-1 anchor: {path}")
        bound_inputs[relative(path)] = sha256(path)

    checkpoint = read_json(CHECKPOINT)
    phase0_summary = read_json(PHASE0_SUMMARY)
    phase0_families = read_jsonl(PHASE0_FAMILIES)
    phase0_source_rows = read_jsonl(PHASE0_SOURCES)
    checkpoint_counts = checkpoint.get("counts", {})
    phase0_counts = phase0_summary.get("counts", {})
    if (checkpoint_counts.get("curation_eligible_clusters"), checkpoint_counts.get("curation_eligible_nc_prompts")) != (54, 125):
        raise SystemExit("Frozen curation checkpoint drift: expected 54 clusters and 125 prompts")
    if phase0_counts.get("source_native_local_gate_eligible_families") != 167:
        raise SystemExit("Phase-0 drift: expected 167 locally eligible families")
    if sum(row.get("phase0_state") == "LOCAL_GATE_ELIGIBLE" for row in phase0_families) != 167:
        raise SystemExit("Phase-0 family-state drift: expected 167 locally eligible family rows")
    if len(phase0_source_rows) != 3922:
        raise SystemExit("Phase-0 source inspection union drift: expected 3922 exact source hashes")
    phase0_hashes = {require_text(row, "canonical_source_sha256", str(PHASE0_SOURCES)) for row in phase0_source_rows}
    if len(phase0_hashes) != 3922 or any(len(value) != 64 for value in phase0_hashes):
        raise SystemExit("Phase-0 source inspection union has malformed or duplicate hashes")
    phase0_local_eligible_hashes = {
        require_text(row, "canonical_source_sha256", str(PHASE0_SOURCES))
        for row in phase0_source_rows
        if row.get("locally_eligible_source") is True
    }
    if len(phase0_local_eligible_hashes) != 501:
        raise SystemExit("Phase-0 locally eligible source set drift: expected 501 exact hashes")

    family_output: list[dict[str, Any]] = []
    structural_rows: list[dict[str, Any]] = [
        {
            "record_type": "named_stratum_state",
            "stratum": "frozen_curation_checkpoint",
            "unit_count": 54,
            "prompt_count": 125,
            "state": "FROZEN_CURATION_ELIGIBLE_NOT_FINAL_GOLD",
            "source_native_temporal_boundary": "PRE_PHASE0_FROZEN_CHECKPOINT",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "record_type": "named_stratum_state",
            "stratum": "phase0_local_gate_baseline",
            "unit_count": 167,
            "prompt_count": 501,
            "state": "LOCAL_GATE_ELIGIBLE_UNADMITTED",
            "source_native_temporal_boundary": "PHASE0_CANONICAL_SNAPSHOT",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    post_hashes: dict[str, set[str]] = {}
    terminal_eligible_hashes: set[str] = set()
    discovery_checks: dict[str, dict[str, Any]] = {}
    total_eligible = total_passed_prompts = 0

    for batch, parent_name in POST_PHASE0_SPECS:
        gate_path, key_path, discovery_path = batch_paths(batch, parent_name)
        for path in (gate_path, key_path):
            if not path.is_file():
                raise SystemExit(f"Missing fixed {batch} input: {path}")
            bound_inputs[relative(path)] = sha256(path)
        gate_rows = read_jsonl(gate_path)
        key_rows = read_jsonl(key_path)
        gate_by_family = {require_text(row, "family_token", str(gate_path)): row for row in gate_rows}
        if len(gate_by_family) != len(gate_rows):
            raise SystemExit(f"{batch} terminal family gate has duplicate family_token values")
        key_by_family: dict[str, list[dict[str, Any]]] = {}
        for row in key_rows:
            family = require_text(row, "family_token", str(key_path))
            source_hash = require_text(row, "canonical_source_sha256", str(key_path))
            source_paths = row.get("source_paths")
            if len(source_hash) != 64 or not isinstance(source_paths, list) or len(source_paths) != 1 or not isinstance(source_paths[0], str):
                raise SystemExit(f"{batch} root reconciliation key has malformed source binding: {row}")
            source_path = WORKSPACE / source_paths[0]
            if not source_path.is_file() or sha256(source_path) != source_hash:
                raise SystemExit(f"{batch} root reconciliation key path/hash binding failed: {source_path}")
            if row.get("source_byte_replay") != "PASS_SHA256_MATCH":
                raise SystemExit(f"{batch} root reconciliation key lacks PASS_SHA256_MATCH: {row}")
            key_by_family.setdefault(family, []).append(row)
        if not set(gate_by_family).issubset(key_by_family) or any(len(rows) != 3 for rows in key_by_family.values()):
            raise SystemExit(f"{batch} terminal family gate is not a subset of exactly three-source root-key families")
        hashes = {require_text(row, "canonical_source_sha256", str(key_path)) for row in key_rows}
        if len(key_rows) != 75 or len(hashes) != 75:
            raise SystemExit(f"{batch} root reconciliation key must be exactly 25 source-disjoint triads")
        post_hashes[batch] = hashes

        eligible_rows = [row for row in gate_rows if row.get("family_disposition") == ELIGIBLE]
        passed = sum(int(row.get("prompt_disposition_counts", {}).get(PASS_PROMPT, 0)) for row in eligible_rows)
        total_eligible += len(eligible_rows)
        total_passed_prompts += passed
        state_counts = Counter(require_text(row, "family_disposition", str(gate_path)) for row in gate_rows)
        structural_rows.append({
            "record_type": "named_stratum_state",
            "stratum": f"post_phase0_terminal_{batch.lower()}",
            "unit_count": len(gate_rows),
            "eligible_family_count": len(eligible_rows),
            "passed_prompt_count": passed,
            "family_disposition_counts": dict(sorted(state_counts.items())),
            "state": "TERMINAL_LOCAL_GATE_JOINED_TO_ROOT_FULL_SOURCE_KEY",
            "source_native_temporal_boundary": "POST_PHASE0_TERMINAL_LOCAL_GATE",
            "claim_boundary": CLAIM_BOUNDARY,
        })
        for family, gate_row in sorted(gate_by_family.items()):
            eligible = gate_row.get("family_disposition") == ELIGIBLE
            sources: list[str] | None = None
            if eligible:
                sources = sorted(require_text(row, "canonical_source_sha256", str(key_path)) for row in key_by_family[family])
                if len(sources) != 3 or len(set(sources)) != 3:
                    raise SystemExit(f"{batch} eligible {family} lacks three distinct joined source hashes")
                terminal_eligible_hashes.update(sources)
            family_output.append({
                "record_type": "post_phase0_terminal_local_eligibility",
                "batch": batch,
                "family_token": family,
                "terminal_local_family_disposition": require_text(gate_row, "family_disposition", str(gate_path)),
                "passed_prompt_count": int(gate_row.get("prompt_disposition_counts", {}).get(PASS_PROMPT, 0)),
                "joined_canonical_source_sha256": sources,
                "source_native_temporal_boundary": "POST_PHASE0_TERMINAL_LOCAL_GATE",
                "claim_boundary": CLAIM_BOUNDARY,
            })
        if discovery_path is not None:
            if not discovery_path.is_file():
                raise SystemExit(f"{batch} cannot claim source disjointness without its discovery manifest")
            bound_inputs[relative(discovery_path)] = sha256(discovery_path)
            manifest = read_json(discovery_path)
            if manifest.get("phase0_source_union") != relative(PHASE0_SOURCES) or manifest.get("phase0_source_union_sha256") != sha256(PHASE0_SOURCES):
                raise SystemExit(f"{batch} discovery manifest is not bound to the canonical Phase-0 source union")
            if batch == "B054":
                manifest_establishes_disjointness = (
                    manifest.get("B054_unique_source_hashes") == 75
                    and manifest.get("intersection_B054_vs_B001_B053") == 0
                )
            else:
                manifest_establishes_disjointness = (
                    manifest.get("selected_batch_unique_source_hashes") == 75
                    and manifest.get("intersection_selected_batch_vs_all_bound_prior_sources") == 0
                )
            if not manifest_establishes_disjointness:
                raise SystemExit(f"{batch} discovery manifest does not establish its claimed source-disjoint selection")
            discovery_checks[batch] = {"manifest": relative(discovery_path), "manifest_sha256": sha256(discovery_path), "verified": True}

    # B065 is a terminal remediation-cap closure, not the provisional initial
    # gate. Its five terminal family rows cover only the source-final subset.
    for path in (B065_KEY, B065_QUEUE, B065_DISCOVERY_MANIFEST, B065_TERMINAL_FAMILIES, B065_TERMINAL_PROMPTS):
        if not path.is_file():
            raise SystemExit(f"Missing fixed B065 terminal-cap input: {path}")
        bound_inputs[relative(path)] = sha256(path)
    b065_queue_rows = read_jsonl(B065_QUEUE)
    if len(b065_queue_rows) != 18:
        raise SystemExit("B065 discovery queue must contain exactly 18 triads")
    b065_queue_hashes: set[str] = set()
    b065_queue_families: set[str] = set()
    for row in b065_queue_rows:
        family_id = require_text(row, "family_id", str(B065_QUEUE))
        hashes = row.get("member_source_sha256")
        if family_id in b065_queue_families or not isinstance(hashes, list) or len(hashes) != 3:
            raise SystemExit("B065 discovery queue is not 18 distinct three-source families")
        b065_queue_families.add(family_id)
        for source_hash in hashes:
            if not isinstance(source_hash, str) or len(source_hash) != 64:
                raise SystemExit("B065 discovery queue has malformed source hashes")
            b065_queue_hashes.add(source_hash)
    if len(b065_queue_hashes) != 54:
        raise SystemExit("B065 discovery queue must contain 54 exact source hashes")
    b065_key_by_family: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(B065_KEY):
        family = require_text(row, "family_token", str(B065_KEY))
        source_hash = require_text(row, "canonical_source_sha256", str(B065_KEY))
        source_paths = row.get("source_paths")
        if len(source_hash) != 64 or not isinstance(source_paths, list) or len(source_paths) != 1 or not isinstance(source_paths[0], str):
            raise SystemExit(f"B065 root reconciliation key has malformed source binding: {row}")
        source_path = WORKSPACE / source_paths[0]
        if not source_path.is_file() or sha256(source_path) != source_hash or row.get("source_byte_replay") != "PASS_SHA256_MATCH":
            raise SystemExit(f"B065 root reconciliation key path/hash binding failed: {source_path}")
        b065_key_by_family.setdefault(family, []).append(row)
    b065_key_hashes = {require_text(row, "canonical_source_sha256", str(B065_KEY)) for rows in b065_key_by_family.values() for row in rows}
    if len(b065_key_by_family) != 18 or any(len(rows) != 3 for rows in b065_key_by_family.values()) or b065_key_hashes != b065_queue_hashes:
        raise SystemExit("B065 root key does not exactly bind the 18-triad discovery queue")
    prior_discovery_hashes = phase0_hashes | set().union(*post_hashes.values())
    b065_discovery_overlap = sorted(b065_queue_hashes & prior_discovery_hashes)
    b065_manifest = read_json(B065_DISCOVERY_MANIFEST)
    if (
        b065_manifest.get("selected_batch_unique_source_hashes") != 54
        or b065_manifest.get("total_prior_source_exclusion_unique_source_hashes") != len(prior_discovery_hashes)
        or b065_manifest.get("intersection_selected_batch_vs_all_bound_prior_sources") != 0
        or b065_discovery_overlap
    ):
        raise SystemExit("B065 discovery source queue is not exactly disjoint from bound prior sources")
    b065_family_rows = read_jsonl(B065_TERMINAL_FAMILIES)
    b065_prompt_rows = read_jsonl(B065_TERMINAL_PROMPTS)
    b065_family_by_token = {require_text(row, "family_token", str(B065_TERMINAL_FAMILIES)): row for row in b065_family_rows}
    if len(b065_family_by_token) != 5 or len(b065_prompt_rows) != 15 or not set(b065_family_by_token).issubset(b065_key_by_family):
        raise SystemExit("B065 terminal remediation-cap closure coverage drift")
    b065_prompt_by_family = Counter(require_text(row, "family_token", str(B065_TERMINAL_PROMPTS)) for row in b065_prompt_rows)
    if set(b065_prompt_by_family) != set(b065_family_by_token) or any(count != 3 for count in b065_prompt_by_family.values()):
        raise SystemExit("B065 terminal prompt dispositions do not bind three prompts per terminal family")
    b065_terminal_prompt_tokens: set[str] = set()
    for row in b065_prompt_rows:
        family = require_text(row, "family_token", str(B065_TERMINAL_PROMPTS))
        prompt_token = require_text(row, "terminal_prompt_token", str(B065_TERMINAL_PROMPTS))
        intended_source = require_text(row, "intended_target_source_sha256", str(B065_TERMINAL_PROMPTS))
        family_sources = {require_text(key_row, "canonical_source_sha256", str(B065_KEY)) for key_row in b065_key_by_family[family]}
        if prompt_token in b065_terminal_prompt_tokens or intended_source not in family_sources:
            raise SystemExit("B065 terminal prompt disposition is not uniquely bound to its root-key family source")
        b065_terminal_prompt_tokens.add(prompt_token)
    b065_terminal_prompt_passes = sum(row.get("terminal_prompt_disposition") == PASS_PROMPT for row in b065_prompt_rows)
    if b065_terminal_prompt_passes != 8:
        raise SystemExit("B065 terminal remediation-cap closure drift: expected eight prompt pass dispositions")
    b065_eligible_rows = [
        row for row in b065_family_rows
        if row.get("terminal_family_disposition") == ELIGIBLE and row.get("all_three_members_pass") is True
    ]
    if len(b065_eligible_rows) != 1 or b065_eligible_rows[0].get("terminal_prompt_disposition_counts", {}).get(PASS_PROMPT) != 3:
        raise SystemExit("B065 cap closure must have exactly one all-three terminally eligible family")
    b065_eligible_hashes = {
        require_text(row, "canonical_source_sha256", str(B065_KEY))
        for row in b065_key_by_family[require_text(b065_eligible_rows[0], "family_token", str(B065_TERMINAL_FAMILIES))]
    }
    if len(b065_eligible_hashes) != 3:
        raise SystemExit("B065 terminally eligible family must bind three distinct sources")
    existing_local_eligible_hashes = phase0_local_eligible_hashes | terminal_eligible_hashes
    b065_local_overlap = sorted(b065_eligible_hashes & existing_local_eligible_hashes)
    if b065_local_overlap:
        raise SystemExit("B065 terminally eligible sources overlap an existing local-eligible source set")
    post_hashes["B065"] = b065_key_hashes
    terminal_eligible_hashes.update(b065_eligible_hashes)
    total_eligible += 1
    total_passed_prompts += 3
    b065_state_counts = Counter(require_text(row, "terminal_family_disposition", str(B065_TERMINAL_FAMILIES)) for row in b065_family_rows)
    structural_rows.append({
        "record_type": "named_stratum_state",
        "stratum": "post_phase0_terminal_b065_remediation_cap_closure",
        "unit_count": len(b065_family_rows),
        "eligible_family_count": 1,
        "passed_prompt_count_in_eligible_family": 3,
        "terminal_prompt_pass_disposition_count_all_terminal_families": b065_terminal_prompt_passes,
        "family_disposition_counts": dict(sorted(b065_state_counts.items())),
        "state": "TERMINAL_REMEDIATION_CAP_CLOSURE_JOINED_TO_ROOT_FULL_SOURCE_KEY",
        "source_native_temporal_boundary": "POST_PHASE0_B065_TERMINAL_REMEDIATION_CAP_CLOSURE",
        "claim_boundary": CLAIM_BOUNDARY,
    })
    for family, row in sorted(b065_family_by_token.items()):
        eligible = row.get("terminal_family_disposition") == ELIGIBLE
        sources = sorted(require_text(key_row, "canonical_source_sha256", str(B065_KEY)) for key_row in b065_key_by_family[family]) if eligible else None
        family_output.append({
            "record_type": "post_phase0_terminal_local_eligibility",
            "batch": "B065",
            "family_token": family,
            "terminal_local_family_disposition": require_text(row, "terminal_family_disposition", str(B065_TERMINAL_FAMILIES)),
            "passed_prompt_count": int(row.get("terminal_prompt_disposition_counts", {}).get(PASS_PROMPT, 0)),
            "joined_canonical_source_sha256": sources,
            "source_native_temporal_boundary": "POST_PHASE0_B065_TERMINAL_REMEDIATION_CAP_CLOSURE",
            "claim_boundary": CLAIM_BOUNDARY,
        })
    if (total_eligible, total_passed_prompts) != (61, 183):
        raise SystemExit("Post-Phase-0 replay drift: expected 61 eligible families and 183 passed prompts in eligible families")
    if any(
        row["terminal_local_family_disposition"] == ELIGIBLE
        and (not isinstance(row["joined_canonical_source_sha256"], list) or len(row["joined_canonical_source_sha256"]) != 3)
        for row in family_output
    ):
        raise SystemExit("Every locally eligible post-Phase-0 family must have three joined source hashes")
    if len(terminal_eligible_hashes) != 183:
        raise SystemExit("Post-Phase-0 locally eligible source set drift: expected 183 exact hashes")
    structural_rows.append({
        "record_type": "named_stratum_aggregate",
        "stratum": "structural_progress_only",
        "frozen_checkpoint_clusters": 54,
        "phase0_local_eligible_families": 167,
        "post_phase0_terminal_local_eligible_families": 61,
        "structural_progress_count": 282,
        "remaining_to_300": 18,
        "state": "STRATUM_COUNT_AGGREGATE_NOT_SOURCE_UNION_OR_FINAL_LIBRARY_COUNT",
        "source_native_temporal_boundary": "CROSS_STRATUM_COUNTS_ONLY",
        "claim_boundary": CLAIM_BOUNDARY,
    })

    phase0_overlaps = {
        batch: {"post_batch_exact_hash_count": len(hashes), "overlap_exact_hash_count": len(hashes & phase0_hashes)}
        for batch, hashes in sorted(post_hashes.items())
    }
    pairwise = []
    for left, right in combinations(sorted(post_hashes), 2):
        overlap = sorted(post_hashes[left] & post_hashes[right])
        pairwise.append({"left_batch": left, "right_batch": right, "overlap_exact_hash_count": len(overlap), "overlap_exact_hashes": overlap})
    local_eligible_overlap = sorted(phase0_local_eligible_hashes & terminal_eligible_hashes)
    local_eligible_source_check: dict[str, Any] = {
        "phase0_source_native_local_gate_eligible_exact_source_count": len(phase0_local_eligible_hashes),
        "post_phase0_terminal_local_gate_eligible_exact_source_count": len(terminal_eligible_hashes),
        "exact_overlap_source_hash_count": len(local_eligible_overlap),
        "exact_overlap_source_hashes": local_eligible_overlap,
        "claim_boundary": "Source-native local-gate source sets only; excludes frozen checkpoint and parent strata and is not a final-library count.",
    }
    if not local_eligible_overlap:
        local_eligible_source_check["combined_source_native_local_gate_eligible_exact_source_count"] = 501 + 183
    report = {
        "status": "PASS_EXACT_PAIRWISE_OVERLAP_CHECKS_WITH_GLOBAL_UNION_EXPLICITLY_UNRESOLVED",
        "phase0_inspection_union": {"path": relative(PHASE0_SOURCES), "sha256": sha256(PHASE0_SOURCES), "exact_hash_count": len(phase0_hashes)},
        "post_batch_vs_phase0_exact_hash_overlap": phase0_overlaps,
        "phase0_local_eligible_source_vs_post_terminal_local_eligible_source": local_eligible_source_check,
        "post_batch_pairwise_exact_hash_overlap": pairwise,
        "b054_b064_discovery_manifest_checks": discovery_checks,
        "b065_discovery_source_queue_disjointness_vs_prior": {
            "queue": relative(B065_QUEUE),
            "queue_sha256": sha256(B065_QUEUE),
            "queue_exact_source_hash_count": len(b065_queue_hashes),
            "prior_exact_source_hash_count": len(prior_discovery_hashes),
            "exact_overlap_source_hash_count": len(b065_discovery_overlap),
            "manifest": relative(B065_DISCOVERY_MANIFEST),
            "manifest_sha256": sha256(B065_DISCOVERY_MANIFEST),
            "verified": True,
        },
        "b065_terminal_local_eligible_source_vs_existing_local_eligible_sources": {
            "b065_exact_source_hash_count": len(b065_eligible_hashes),
            "existing_local_eligible_exact_source_hash_count": len(existing_local_eligible_hashes),
            "exact_overlap_source_hash_count": len(b065_local_overlap),
            "combined_source_native_local_gate_eligible_exact_source_count": len(existing_local_eligible_hashes | b065_eligible_hashes),
            "claim_boundary": "Source-native local-gate source sets only; not a final-library count.",
        },
        "global_source_unique_union": {
            "status": "UNRESOLVED_NOT_COMPUTED",
            "reason": "The named strata overlap temporally and procedurally; pairwise hash checks do not authorise a global source-unique union or final-library count.",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }

    out.mkdir(parents=True)
    write_jsonl(out / "phase1_structural_state.jsonl", structural_rows)
    write_jsonl(out / "post_phase0_terminal_local_eligibility.jsonl", family_output)
    write_json(out / "phase1_source_overlap_report.json", report)
    markdown = "\n".join([
        "# RQ2b NC Phase-1 State Reconciliation — 2026-09-05",
        "",
        "This is a current-state, structural reconciliation only. It contains no prompts or reviewer content.",
        "",
        "- Frozen curation checkpoint: 54 clusters and 125 prompts.",
        "- Phase-0 baseline: 167 locally eligible source-native families.",
        "- Named post-Phase-0 terminal additions: 61 locally eligible families and 183 passed prompts within eligible families; every eligible family is joined to three root-key source hashes.",
        "- B065 remediation-cap closure has eight terminal prompt pass dispositions across its five terminal families, but only its one all-three family contributes three passed prompts and one eligible family to the local-eligible aggregate.",
        "- The Phase-0 501 locally eligible source hashes and the 183 terminally eligible post-Phase-0 source hashes are checked separately; a zero overlap permits the labelled 684 source-native local-gate aggregate only.",
        "- Structural progress is 282 and remaining-to-300 is 18. These are stratum-count aggregates, not source-unique union or final-library counts.",
        "- Exact post-batch overlaps and Phase-0 overlaps are in `phase1_source_overlap_report.json`. B054–B064 source-disjoint selection claims are retained only after their bound discovery manifests validate.",
        "",
        "## Boundary",
        "",
        "No whole-library acceptable-set audit, global source-unique union, final library admission, retrieval result, metric, or thesis-result claim is established.",
        "",
    ])
    (out / "PHASE1_STATE_RECONCILIATION_2026-09-05.md").write_text(markdown, encoding="utf-8", newline="\n")
    outputs = {name: sha256(out / name) for name in (
        "phase1_structural_state.jsonl",
        "post_phase0_terminal_local_eligibility.jsonl",
        "phase1_source_overlap_report.json",
        "PHASE1_STATE_RECONCILIATION_2026-09-05.md",
    )}
    summary = {
        "status": "PASS_RQ2B_NC_PHASE1_STRUCTURAL_STATE_RECONCILIATION_WITH_GLOBAL_UNION_UNRESOLVED",
        "counts": {
            "frozen_checkpoint_clusters": 54,
            "frozen_checkpoint_prompts": 125,
            "phase0_local_eligible_families": 167,
            "post_phase0_terminal_local_eligible_families": 61,
            "post_phase0_terminal_passed_prompts_in_eligible_families": 183,
            "b065_terminal_prompt_pass_dispositions_all_terminal_families": 8,
            "phase0_source_native_local_gate_eligible_exact_sources": 501,
            "post_phase0_terminal_local_gate_eligible_exact_sources": 183,
            "structural_progress_count": 282,
            "remaining_to_300": 18,
        },
        "bound_inputs": dict(sorted(bound_inputs.items())),
        "outputs": outputs,
        "global_source_unique_union": report["global_source_unique_union"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(out / "summary.json", summary)
    print(json.dumps({"output_dir": str(out), "status": summary["status"], "counts": summary["counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
