#!/usr/bin/env python3
"""Materialise a bounded Phase-1 structural state with B066--B070 terminals.

This is a conservative controller: it binds fixed terminal artifacts, root
source keys, discovery queues/manifests, byte replays, and PAF provenance
bindings.  Its only aggregate is a named structural stratum count.  It does
not compute a whole-library, source-unique, retrieval, metric, or final-library
result.  B071 is deliberately absent until supplied as an explicit terminal
specification with ``--b071-terminal-spec``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW = NC / "review"
PHASE0 = REVIEW / "rq2b_nc_phase0_state_reconciliation_2026-09-05_v2"
PHASE0_SUMMARY = PHASE0 / "summary.json"
PHASE0_FAMILIES = PHASE0 / "phase0_family_state.jsonl"
PHASE0_SOURCES = PHASE0 / "phase0_source_native_inspection_union.jsonl"
CHECKPOINT = NC / "manifests/curation_closed_checkpoint_2026-08-31/summary.json"
V3 = REVIEW / "rq2b_nc_phase1_state_reconciliation_2026-09-05_v3"
V3_SUMMARY = V3 / "summary.json"
V3_STRUCTURAL = V3 / "phase1_structural_state.jsonl"

ELIGIBLE = "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
PASS_PROMPT = "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
PROVENANCE_PASS = "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE"
SOURCE_PASS = "PASS_TO_PROMPT_AUTHORING"
CLAIM_BOUNDARY = (
    "Structural named-stratum state only. This establishes neither a "
    "whole-library acceptable-set outcome, a global source-unique union, "
    "a final-library count, a retrieval result, nor a metric."
)


@dataclass(frozen=True)
class TerminalSpec:
    """Closed terminal input contract; B071 must be provided explicitly later."""

    batch: str
    parent_name: str
    queue_name: str
    terminal_kind: str
    expected_terminal_families: int
    expected_eligible_families: int
    expected_passed_prompts_in_eligible_families: int


# Explicitly closed input list.  Do not replace with discovery/globbing: B071
# is not included unless a caller supplies a separately reviewed JSON spec.
FIXED_TERMINAL_SPECS = (
    TerminalSpec("B066", "source_native_technical_workflow_b066_2026-09-05", "b066_source_native_semantic_family_queue.jsonl", "remediation_cap_terminal_closure", 5, 0, 0),
    TerminalSpec("B067", "source_native_local_bge_continuation_b067_2026-09-05", "b067_source_native_local_bge_family_queue.jsonl", "normal_final_target_gate", 8, 8, 24),
    TerminalSpec("B068", "source_native_local_bge_continuation_b068_2026-09-05", "b068_source_native_local_bge_family_queue.jsonl", "remediation_cap_terminal_closure", 2, 2, 6),
    TerminalSpec("B069", "source_native_local_bge_continuation_b069_2026-09-05", "b069_source_native_local_bge_family_queue.jsonl", "remediation_cap_terminal_closure", 4, 2, 6),
    TerminalSpec("B070", "source_native_local_bge_continuation_b070_2026-09-05", "b070_source_native_local_bge_family_queue.jsonl", "normal_final_target_gate", 9, 7, 21),
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


def bind_input(bound_inputs: dict[str, str], path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"Missing fixed terminal input: {path}")
    bound_inputs[relative(path)] = sha256(path)


def parse_explicit_b071_spec(path: Path) -> TerminalSpec:
    """Load a future B071 only if its terminal contract is supplied verbatim."""

    value = read_json(path)
    required = {
        "batch", "parent_name", "queue_name", "terminal_kind", "expected_terminal_families",
        "expected_eligible_families", "expected_passed_prompts_in_eligible_families",
    }
    if set(value) != required or value.get("batch") != "B071":
        raise SystemExit("B071 terminal spec must contain exactly the explicit B071 terminal contract fields")
    if value["terminal_kind"] not in {
        "normal_final_target_gate",
        "remediation_cap_terminal_closure",
        "partial_remediation_composite_closure",
    }:
        raise SystemExit("B071 terminal spec has an unsupported terminal_kind")
    if any(not isinstance(value[key], str) or not value[key] for key in ("parent_name", "queue_name")):
        raise SystemExit("B071 terminal spec parent_name and queue_name must be non-empty")
    counts = ("expected_terminal_families", "expected_eligible_families", "expected_passed_prompts_in_eligible_families")
    if any(not isinstance(value[key], int) or value[key] < 0 for key in counts):
        raise SystemExit("B071 terminal spec expected counts must be non-negative integers")
    return TerminalSpec(**value)


def terminal_paths(spec: TerminalSpec) -> dict[str, Path]:
    """Return only canonical terminal and evidence paths for one fixed batch."""

    parent = REVIEW / spec.parent_name
    root = parent / f"batch_{spec.batch[1:]}_full_source_review_packets"
    paths = {
        "queue": parent / spec.queue_name,
        "discovery_manifest": parent / "historical_source_exclusion_manifest.json",
        "source_replay": parent / "source_provenance_byte_replay_ledger.jsonl",
        "root_key": root / "internal_reconciliation_key.jsonl",
        "provenance_dispositions": root / "reconciliation/pass_provenance_preflight/pass_family_provenance_dispositions.jsonl",
        "paf_bindings": root / "reconciliation/paf/internal_paf_source_provenance_bindings.jsonl",
    }
    if spec.terminal_kind == "normal_final_target_gate":
        paths["terminal_families"] = root / "reconciliation/prompt_authoring/target_blind_adequacy_packets/reconciliation/final_prompt_dispositions/family_gate_dispositions.jsonl"
    elif spec.terminal_kind == "remediation_cap_terminal_closure":
        cap = root / "reconciliation/prompt_authoring/cue_remediation/remediation_cap_closure"
        paths["terminal_families"] = cap / "terminal_family_dispositions.jsonl"
        paths["terminal_prompts"] = cap / "terminal_prompt_dispositions.jsonl"
    else:
        composite = root / "reconciliation/prompt_authoring/cue_remediation/partial_remediation_composite_closure"
        paths["terminal_families"] = composite / "composite_terminal_family_dispositions.jsonl"
        paths["terminal_prompts"] = composite / "composite_terminal_prompt_dispositions.jsonl"
        paths["terminal_summary"] = composite / "summary.json"
    if any(path is None for path in paths.values()):
        raise SystemExit(f"{spec.batch} requires exactly one top-level discovery queue")
    return {name: path for name, path in paths.items() if path is not None}


def validate_root_key(spec: TerminalSpec, path: Path) -> dict[str, set[str]]:
    """Check 25 source-disjoint root triads and source byte identity."""

    key_rows = read_jsonl(path)
    by_family: dict[str, set[str]] = {}
    for row in key_rows:
        family = require_text(row, "family_token", str(path))
        source_hash = require_text(row, "canonical_source_sha256", str(path))
        source_paths = row.get("source_paths")
        if len(source_hash) != 64 or not isinstance(source_paths, list) or len(source_paths) != 1 or not isinstance(source_paths[0], str):
            raise SystemExit(f"{spec.batch} root reconciliation key has malformed source binding: {row}")
        source_path = WORKSPACE / source_paths[0]
        if not source_path.is_file() or sha256(source_path) != source_hash or row.get("source_byte_replay") != "PASS_SHA256_MATCH":
            raise SystemExit(f"{spec.batch} root reconciliation key path/hash binding failed: {source_path}")
        by_family.setdefault(family, set()).add(source_hash)
    all_hashes = set().union(*by_family.values()) if by_family else set()
    if len(key_rows) != 75 or len(by_family) != 25 or any(len(hashes) != 3 for hashes in by_family.values()) or len(all_hashes) != 75:
        raise SystemExit(f"{spec.batch} root reconciliation key must be exactly 25 source-disjoint triads")
    return by_family


def validate_discovery_and_replay(spec: TerminalSpec, paths: dict[str, Path], root_by_family: dict[str, set[str]]) -> None:
    """Bind the discovery queue/manifest and source replay ledger to root keys."""

    queue_rows = read_jsonl(paths["queue"])
    queue_by_family: dict[str, set[str]] = {}
    for row in queue_rows:
        family = require_text(row, "family_id", str(paths["queue"]))
        hashes = row.get("member_source_sha256")
        if not isinstance(hashes, list) or len(hashes) != 3 or any(not isinstance(value, str) or len(value) != 64 for value in hashes):
            raise SystemExit(f"{spec.batch} discovery queue lacks an exact source-hash triad")
        queue_by_family[family] = set(hashes)
    queue_hashes = set().union(*queue_by_family.values()) if queue_by_family else set()
    root_hashes = set().union(*root_by_family.values())
    if len(queue_rows) != 25 or len(queue_by_family) != 25 or len(queue_hashes) != 75 or queue_hashes != root_hashes:
        raise SystemExit(f"{spec.batch} discovery queue does not exactly bind the 25 root-key triads")

    manifest = read_json(paths["discovery_manifest"])
    phase0_path = relative(PHASE0_SOURCES)
    phase0_sha256 = sha256(PHASE0_SOURCES)
    if manifest.get("selected_batch_unique_source_hashes") != 75:
        raise SystemExit(f"{spec.batch} discovery manifest does not bind 75 selected source hashes")
    if spec.batch == "B066":
        zero_overlap = manifest.get("intersection_selected_batch_vs_all_bound_prior_sources") == 0
        phase0_bound = (
            manifest.get("phase0_source_union") == phase0_path
            and manifest.get("phase0_source_union_sha256") == phase0_sha256
        )
    else:
        zero_overlap = manifest.get("intersection_selected_vs_all_excluded_sources") == 0
        phase0 = manifest.get("phase0_v2")
        phase0_bound = (
            isinstance(phase0, dict)
            and phase0.get("inspection_union") == phase0_path
            and phase0.get("inspection_union_sha256") == phase0_sha256
        )
    if not zero_overlap or not phase0_bound:
        raise SystemExit(f"{spec.batch} discovery manifest lacks its zero-overlap Phase-0-bound evidence")

    replay_rows = read_jsonl(paths["source_replay"])
    replay_hashes: set[str] = set()
    for row in replay_rows:
        source_hash = require_text(row, "canonical_source_sha256", str(paths["source_replay"]))
        if row.get("source_byte_replay_status") != "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256":
            raise SystemExit(f"{spec.batch} source replay ledger lacks byte-replay pass status")
        replay_hashes.add(source_hash)
    if len(replay_rows) != 75 or len(replay_hashes) != 75 or replay_hashes != root_hashes:
        raise SystemExit(f"{spec.batch} source replay ledger does not exactly bind root-key sources")


def validate_provenance(spec: TerminalSpec, paths: dict[str, Path], root_by_family: dict[str, set[str]], terminal_families: set[str]) -> None:
    """Require terminal family provenance and PAF source bindings before counting."""

    dispositions = {
        require_text(row, "family_token", str(paths["provenance_dispositions"])): row
        for row in read_jsonl(paths["provenance_dispositions"])
    }
    paf_by_family: dict[str, set[str]] = {}
    for row in read_jsonl(paths["paf_bindings"]):
        family = require_text(row, "family_token", str(paths["paf_bindings"]))
        source_hash = require_text(row, "canonical_source_sha256", str(paths["paf_bindings"]))
        if row.get("family_provenance_preflight_status") != PROVENANCE_PASS or row.get("final_source_decision") != SOURCE_PASS:
            raise SystemExit(f"{spec.batch} PAF provenance binding is not prompt-authoring eligible")
        paf_by_family.setdefault(family, set()).add(source_hash)
    for family in terminal_families:
        if family not in root_by_family or dispositions.get(family, {}).get("family_provenance_preflight_status") != PROVENANCE_PASS:
            raise SystemExit(f"{spec.batch} terminal family lacks eligible provenance disposition: {family}")
        if paf_by_family.get(family) != root_by_family[family]:
            raise SystemExit(f"{spec.batch} terminal family PAF sources do not exactly bind its root key: {family}")


def terminal_family_rows(spec: TerminalSpec, paths: dict[str, Path], root_by_family: dict[str, set[str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Load canonical terminal rows and select only all-three local families."""

    if spec.terminal_kind == "partial_remediation_composite_closure":
        composite_summary = read_json(paths["terminal_summary"])
        outputs = composite_summary.get("outputs")
        if (
            not isinstance(outputs, dict)
            or outputs.get("composite_terminal_family_dispositions.jsonl") != sha256(paths["terminal_families"])
            or outputs.get("composite_terminal_prompt_dispositions.jsonl") != sha256(paths["terminal_prompts"])
            or "NO_SECOND_REWRITE" not in str(composite_summary.get("status", ""))
        ):
            raise SystemExit(f"{spec.batch} composite terminal summary does not bind its closed terminal outputs")
    rows = read_jsonl(paths["terminal_families"])
    key = "family_disposition" if spec.terminal_kind == "normal_final_target_gate" else "terminal_family_disposition"
    by_family = {require_text(row, "family_token", str(paths["terminal_families"])): row for row in rows}
    if len(by_family) != len(rows) or not set(by_family).issubset(root_by_family):
        raise SystemExit(f"{spec.batch} terminal family artifact has duplicate or unbound family tokens")
    if spec.terminal_kind in {"remediation_cap_terminal_closure", "partial_remediation_composite_closure"}:
        prompt_rows = read_jsonl(paths["terminal_prompts"])
        prompt_counts = Counter(require_text(row, "family_token", str(paths["terminal_prompts"])) for row in prompt_rows)
        if set(prompt_counts) != set(by_family):
            raise SystemExit(f"{spec.batch} remediation terminal prompts do not cover terminal families exactly")
        tokens: set[str] = set()
        for row in prompt_rows:
            family = require_text(row, "family_token", str(paths["terminal_prompts"]))
            token = require_text(row, "terminal_prompt_token", str(paths["terminal_prompts"]))
            intended = require_text(row, "intended_target_source_sha256", str(paths["terminal_prompts"]))
            if token in tokens or intended not in root_by_family[family]:
                raise SystemExit(f"{spec.batch} remediation terminal prompt is not uniquely source-bound")
            tokens.add(token)
        if any(prompt_counts[family] != row.get("terminal_prompt_count") for family, row in by_family.items()):
            raise SystemExit(f"{spec.batch} remediation terminal prompt count does not match family closure")
        eligible = [
            row for row in rows
            if row.get(key) == ELIGIBLE and row.get("all_three_members_pass") is True
        ]
        if any(row.get(key) == ELIGIBLE and row.get("all_three_members_pass") is not True for row in rows):
            raise SystemExit(f"{spec.batch} cap closure cannot count a non-all-three terminal family")
    else:
        eligible = [row for row in rows if row.get(key) == ELIGIBLE]
    for row in eligible:
        if root_by_family[require_text(row, "family_token", str(paths["terminal_families"]))] is None:
            raise SystemExit(f"{spec.batch} locally eligible terminal family lacks a root-key source triad")
        if row.get("terminal_prompt_disposition_counts" if spec.terminal_kind != "normal_final_target_gate" else "prompt_disposition_counts", {}).get(PASS_PROMPT) != 3:
            raise SystemExit(f"{spec.batch} locally eligible terminal family must have exactly three pass prompts")
    return rows, eligible


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise the bounded RQ2b-NC Phase-1 v4 structural state.")
    parser.add_argument("--output-dir", type=Path, default=REVIEW / "rq2b_nc_phase1_state_reconciliation_2026-09-05_v4")
    parser.add_argument("--b071-terminal-spec", type=Path, help="Explicit reviewed B071 terminal contract JSON; absent by default.")
    parser.add_argument("--validate-only", action="store_true", help="Replay all bindings without creating a v4 snapshot.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite an existing Phase-1 v4 snapshot: {out}")

    specs = list(FIXED_TERMINAL_SPECS)
    if args.b071_terminal_spec is not None:
        specs.append(parse_explicit_b071_spec(args.b071_terminal_spec.resolve()))

    bound_inputs: dict[str, str] = {}
    if args.b071_terminal_spec is not None:
        bind_input(bound_inputs, args.b071_terminal_spec.resolve())
    for path in (CHECKPOINT, PHASE0_SUMMARY, PHASE0_FAMILIES, PHASE0_SOURCES, V3_SUMMARY, V3_STRUCTURAL):
        bind_input(bound_inputs, path)
    checkpoint = read_json(CHECKPOINT)
    phase0_summary = read_json(PHASE0_SUMMARY)
    v3_summary = read_json(V3_SUMMARY)
    if checkpoint.get("counts", {}).get("curation_eligible_clusters") != 54:
        raise SystemExit("Frozen curation checkpoint drift: expected 54 clusters")
    if phase0_summary.get("counts", {}).get("source_native_local_gate_eligible_families") != 167:
        raise SystemExit("Phase-0 drift: expected 167 locally eligible families")
    if sum(row.get("phase0_state") == "LOCAL_GATE_ELIGIBLE" for row in read_jsonl(PHASE0_FAMILIES)) != 167:
        raise SystemExit("Phase-0 family-state drift: expected 167 locally eligible rows")
    v3_counts = v3_summary.get("counts", {})
    if (v3_counts.get("post_phase0_terminal_local_eligible_families"), v3_counts.get("structural_progress_count")) != (61, 282):
        raise SystemExit("Phase-1 v3 anchor drift: expected 61 post-Phase-0 families and structural count 282")

    structural_rows: list[dict[str, Any]] = [
        {"record_type": "named_stratum_state", "stratum": "frozen_curation_checkpoint", "unit_count": 54, "state": "FROZEN_CURATION_ELIGIBLE_NOT_FINAL_GOLD", "claim_boundary": CLAIM_BOUNDARY},
        {"record_type": "named_stratum_state", "stratum": "phase0_local_gate_baseline", "unit_count": 167, "state": "LOCAL_GATE_ELIGIBLE_UNADMITTED", "claim_boundary": CLAIM_BOUNDARY},
        {"record_type": "named_stratum_state", "stratum": "phase1_v3_closed_terminal_anchor", "unit_count": 61, "state": "PREVIOUSLY_MATERIALISED_LOCAL_GATE_ELIGIBLE_UNADMITTED", "claim_boundary": CLAIM_BOUNDARY},
    ]
    family_output: list[dict[str, Any]] = []
    fixed_eligible = fixed_passed_prompts = 0
    b071_eligible = b071_passed_prompts = 0
    for spec in specs:
        paths = terminal_paths(spec)
        for path in paths.values():
            bind_input(bound_inputs, path)
        root_by_family = validate_root_key(spec, paths["root_key"])
        validate_discovery_and_replay(spec, paths, root_by_family)
        rows, eligible = terminal_family_rows(spec, paths, root_by_family)
        terminal_families = {require_text(row, "family_token", str(paths["terminal_families"])) for row in rows}
        validate_provenance(spec, paths, root_by_family, terminal_families)
        pass_key = "prompt_disposition_counts" if spec.terminal_kind == "normal_final_target_gate" else "terminal_prompt_disposition_counts"
        passed = sum(int(row.get(pass_key, {}).get(PASS_PROMPT, 0)) for row in eligible)
        if (len(rows), len(eligible), passed) != (spec.expected_terminal_families, spec.expected_eligible_families, spec.expected_passed_prompts_in_eligible_families):
            raise SystemExit(f"{spec.batch} explicit terminal replay drift")
        if spec.batch == "B071":
            b071_eligible += len(eligible)
            b071_passed_prompts += passed
        else:
            fixed_eligible += len(eligible)
            fixed_passed_prompts += passed
        disposition_key = "family_disposition" if spec.terminal_kind == "normal_final_target_gate" else "terminal_family_disposition"
        structural_rows.append({
            "record_type": "named_stratum_state",
            "stratum": f"post_phase1_{spec.batch.lower()}_{spec.terminal_kind}",
            "terminal_kind": spec.terminal_kind,
            "terminal_family_count": len(rows),
            "locally_eligible_family_count": len(eligible),
            "passed_prompt_count_in_locally_eligible_families": passed,
            "terminal_family_disposition_counts": dict(sorted(Counter(require_text(row, disposition_key, str(paths["terminal_families"])) for row in rows).items())),
            "state": "TERMINAL_LOCAL_STATE_JOINED_TO_ROOT_KEY_WITH_DISCOVERY_AND_PROVENANCE_EVIDENCE",
            "claim_boundary": CLAIM_BOUNDARY,
        })
        for row in rows:
            family = require_text(row, "family_token", str(paths["terminal_families"]))
            is_eligible = row in eligible
            family_output.append({
                "record_type": "post_phase1_terminal_local_state",
                "batch": spec.batch,
                "terminal_kind": spec.terminal_kind,
                "family_token": family,
                "terminal_local_family_disposition": require_text(row, disposition_key, str(paths["terminal_families"])),
                "locally_eligible_all_three": is_eligible,
                "joined_canonical_source_sha256": sorted(root_by_family[family]) if is_eligible else None,
                "claim_boundary": CLAIM_BOUNDARY,
            })

    if (fixed_eligible, fixed_passed_prompts) != (19, 57):
        raise SystemExit("B066--B070 terminal replay drift: expected 19 locally eligible families and 57 pass prompts")
    additional_eligible = fixed_eligible + b071_eligible
    additional_passed_prompts = fixed_passed_prompts + b071_passed_prompts
    structural_progress = 54 + 167 + 61 + additional_eligible
    structural_rows.append({
        "record_type": "named_stratum_aggregate",
        "stratum": "structural_progress_only",
        "frozen_checkpoint_clusters": 54,
        "phase0_local_eligible_families": 167,
        "phase1_v3_closed_terminal_local_eligible_families": 61,
        "b066_b070_terminal_local_eligible_families": fixed_eligible,
        "explicit_b071_terminal_local_eligible_families": b071_eligible,
        "structural_progress_count": structural_progress,
        "state": "STRATUM_COUNT_AGGREGATE_NOT_SOURCE_UNION_OR_FINAL_LIBRARY_COUNT",
        "claim_boundary": CLAIM_BOUNDARY,
    })

    if args.validate_only:
        print(json.dumps({
            "status": "PASS_RQ2B_NC_PHASE1_V4_BINDING_REPLAY_NO_SNAPSHOT",
            "structural_progress_count": structural_progress,
            "b066_b070_terminal_local_eligible_families": fixed_eligible,
            "explicit_b071_terminal_local_eligible_families": b071_eligible,
        }, sort_keys=True))
        return 0

    out.mkdir(parents=True)
    write_jsonl(out / "phase1_v4_structural_state.jsonl", structural_rows)
    write_jsonl(out / "post_phase1_terminal_local_state.jsonl", family_output)
    summary = {
        "status": "PASS_RQ2B_NC_PHASE1_V4_STRUCTURAL_STATE_WITH_GLOBAL_UNION_NOT_COMPUTED",
        "counts": {
            "frozen_checkpoint_clusters": 54,
            "phase0_local_eligible_families": 167,
            "phase1_v3_closed_terminal_local_eligible_families": 61,
            "b066_b070_terminal_local_eligible_families": fixed_eligible,
            "b066_b070_passed_prompts_in_locally_eligible_families": fixed_passed_prompts,
            "explicit_b071_terminal_local_eligible_families": b071_eligible,
            "explicit_b071_passed_prompts_in_locally_eligible_families": b071_passed_prompts,
            "all_explicit_additional_terminal_local_eligible_families": additional_eligible,
            "all_explicit_additional_passed_prompts_in_locally_eligible_families": additional_passed_prompts,
            "structural_progress_count": structural_progress,
        },
        "bound_inputs": dict(sorted(bound_inputs.items())),
        "b071": "NOT_INCLUDED_UNTIL_AN_EXPLICIT_TERMINAL_SPEC_IS_SUPPLIED" if args.b071_terminal_spec is None else "EXPLICIT_TERMINAL_SPEC_INCLUDED",
        "global_source_unique_union": {"status": "NOT_COMPUTED", "reason": "This controller materialises structural strata only."},
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(out / "summary.json", summary)
    print(json.dumps({"output_dir": str(out), "status": summary["status"], "counts": summary["counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
