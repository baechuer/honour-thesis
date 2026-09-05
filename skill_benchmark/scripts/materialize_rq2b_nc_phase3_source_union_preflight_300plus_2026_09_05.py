#!/usr/bin/env python3
"""Materialise the post-300 RQ2b-NC source-canonical union preflight.

This is a fail-closed Phase-3 preflight only.  It replays exact source bytes,
local provenance, terminal local-gate records, and source-visible reviewer
packet prompt text.  It neither freezes an audit input nor creates a K=6
proposal, acceptable-set label, final benchmark, retrieval result, or metric.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
REVIEW = NC / "review"
MANIFESTS = NC / "manifests"
PHASE0 = REVIEW / "rq2b_nc_phase0_state_reconciliation_2026-09-05_v3_replay"
V3 = REVIEW / "rq2b_nc_phase1_state_reconciliation_2026-09-05_v3_replay"
V4 = REVIEW / "rq2b_nc_phase1_state_reconciliation_2026-09-05_v4_replay"
BASE_CANDIDATES = MANIFESTS / "current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
CHECKPOINT_CLUSTERS = MANIFESTS / "curation_closed_checkpoint_2026-08-31/curation_eligible_clusters.jsonl"
CHECKPOINT_PROMPTS = MANIFESTS / "curation_closed_checkpoint_2026-08-31/curation_eligible_prompts.jsonl"
PARENT_PROMPTS = WORKSPACE / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
SOP = REVIEW / "RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
B071_SPEC = REVIEW / "source_native_local_bge_continuation_b071_2026-09-05/batch_071_full_source_review_packets/reconciliation/prompt_authoring/cue_remediation/partial_remediation_composite_closure/B071_PHASE1_V4_TERMINAL_SPEC.json"
ELIGIBLE = "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
PROMPT_PASS = "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"


@dataclass(frozen=True)
class TerminalSpec:
    batch: str
    parent_name: str
    mode: str

    @property
    def root(self) -> Path:
        return REVIEW / self.parent_name / f"batch_{self.batch[1:]}_full_source_review_packets"


V3_SPECS = (
    TerminalSpec("B013", "source_native_dense_lexical_union_b013_2026-09-04", "normal"),
    TerminalSpec("B014", "source_native_dense_lexical_union_b014_2026-09-04", "normal"),
    TerminalSpec("B015", "source_native_dense_lexical_union_b015_2026-09-04", "normal"),
    TerminalSpec("B052", "source_native_marketing_advertising_seo_social_community_web_analytics_journalism_publishing_localisation_communications_b052_2026-09-05", "normal"),
    TerminalSpec("B054", "source_native_remaining_pool_disjoint_lexical_b054_2026-09-05", "normal"),
    TerminalSpec("B055", "source_native_remaining_pool_disjoint_lexical_b055_2026-09-05", "normal"),
    TerminalSpec("B056", "source_native_remaining_pool_disjoint_lexical_b056_2026-09-05", "normal"),
    TerminalSpec("B057", "source_native_remaining_pool_disjoint_lexical_b057_2026-09-05", "normal"),
    TerminalSpec("B058", "source_native_remaining_pool_disjoint_lexical_b058_2026-09-05", "normal"),
    TerminalSpec("B059", "source_native_remaining_pool_disjoint_lexical_b059_2026-09-05", "normal"),
    TerminalSpec("B060", "source_native_low_cue_workflow_b060_2026-09-05", "normal"),
    TerminalSpec("B061", "source_native_low_cue_workflow_b061_2026-09-05", "normal"),
    TerminalSpec("B062", "source_native_low_cue_workflow_b062_2026-09-05", "normal"),
    TerminalSpec("B063", "source_native_low_cue_workflow_b063_2026-09-05", "normal"),
    TerminalSpec("B064", "source_native_low_cue_workflow_b064_2026-09-05", "normal"),
    TerminalSpec("B065", "source_native_low_cue_workflow_b065_2026-09-05", "cap"),
)
V4_SPECS = (
    TerminalSpec("B066", "source_native_technical_workflow_b066_2026-09-05", "cap"),
    TerminalSpec("B067", "source_native_local_bge_continuation_b067_2026-09-05", "normal_paf"),
    TerminalSpec("B068", "source_native_local_bge_continuation_b068_2026-09-05", "cap_paf"),
    TerminalSpec("B069", "source_native_local_bge_continuation_b069_2026-09-05", "cap_paf"),
    TerminalSpec("B070", "source_native_local_bge_continuation_b070_2026-09-05", "normal_paf"),
    TerminalSpec("B071", "source_native_local_bge_continuation_b071_2026-09-05", "composite_paf"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSON input: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing canonical JSONL input: {path}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise SystemExit(f"Expected JSON object rows: {path}")
    return rows


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8", newline="\n")


def require_text(row: dict[str, Any], field: str, context: str) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"Missing {field} in {context}: {row}")
    return value


def bind(bound: dict[str, str], path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"Missing required bound input: {path}")
    bound[rel(path)] = sha256(path)


def packet_texts(path: Path, tokens: set[str]) -> dict[str, str]:
    """Read only token/text pairs from a source-visible reviewer packet."""
    found: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            token = row.get("prompt_token")
            if token in tokens:
                text = row.get("natural_user_task_prompt")
                if not isinstance(text, str) or not text.strip() or token in found:
                    raise SystemExit(f"Malformed or duplicate prompt-token binding in {path}: {token}")
                found[token] = text
    if set(found) != tokens:
        raise SystemExit(f"Reviewer packet does not bind every terminal prompt token: {path}")
    return found


def base_source_paths(row: dict[str, Any]) -> list[str]:
    paths: set[str] = set()
    if isinstance(row.get("source_path"), str):
        paths.add(row["source_path"])
    binding = row.get("provenance_binding")
    if isinstance(binding, dict) and isinstance(binding.get("source_path"), str):
        paths.add(binding["source_path"])
    for key in ("v3_identity_records", "rq1_records"):
        values = row.get(key)
        if isinstance(values, list):
            for value in values:
                if isinstance(value, dict) and isinstance(value.get("source_path"), str):
                    paths.add(value["source_path"])
    if not paths:
        raise SystemExit(f"Base candidate lacks a local source replay path: {row.get('canonical_source_sha256')}")
    return sorted(paths)


def replay_source_paths(source_hash: str, paths: list[str], context: str) -> None:
    if len(source_hash) != 64:
        raise SystemExit(f"Malformed source SHA-256 in {context}: {source_hash}")
    for stored in paths:
        candidates = [WORKSPACE / stored]
        if not stored.startswith("skill_benchmark/"):
            candidates.append(WORKSPACE / "skill_benchmark" / stored)
        valid = [path for path in candidates if path.is_file() and sha256(path) == source_hash]
        if not valid:
            raise SystemExit(f"Source byte replay failed in {context}: {stored}")


def root_key(root: Path, family: str, bound: dict[str, str]) -> list[dict[str, Any]]:
    path = root / "internal_reconciliation_key.jsonl"
    bind(bound, path)
    rows = [row for row in read_jsonl(path) if row.get("family_token") == family]
    if len(rows) != 3:
        raise SystemExit(f"{root.name}/{family} must bind exactly three root-key source rows")
    hashes = [require_text(row, "canonical_source_sha256", str(path)) for row in rows]
    if len(set(hashes)) != 3:
        raise SystemExit(f"{root.name}/{family} root key does not contain three distinct sources")
    for row in rows:
        if row.get("source_byte_replay") != "PASS_SHA256_MATCH":
            raise SystemExit(f"Root key lacks PASS_SHA256_MATCH: {row}")
    return sorted(rows, key=lambda row: str(row["member_token"]))


def provenance_rows(root: Path, family: str, paf: bool, bound: dict[str, str]) -> list[dict[str, Any]]:
    path = (
        root / "reconciliation/paf/internal_paf_source_provenance_bindings.jsonl"
        if paf else root / "reconciliation/pass_provenance_preflight/pass_family_source_provenance_preflight.jsonl"
    )
    bind(bound, path)
    rows = [row for row in read_jsonl(path) if row.get("family_token") == family]
    if len(rows) != 3:
        raise SystemExit(f"{root.name}/{family} must bind exactly three provenance rows")
    hashes = {require_text(row, "canonical_source_sha256", str(path)) for row in rows}
    if len(hashes) != 3:
        raise SystemExit(f"{root.name}/{family} provenance has duplicate source hashes")
    if paf:
        if any(row.get("final_source_decision") != "PASS_TO_PROMPT_AUTHORING" or row.get("family_provenance_preflight_status") != "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE" for row in rows):
            raise SystemExit(f"{root.name}/{family} PAF binding is not eligible")
    else:
        for row in rows:
            paths = row.get("source_paths")
            if not isinstance(paths, list) or not paths or not all(isinstance(value, str) for value in paths):
                raise SystemExit(f"{root.name}/{family} source provenance lacks replayable source paths")
            if not str(row.get("provenance_preflight_status", "")).startswith("PASS_") or row.get("source_byte_replay") != "PASS_SHA256_MATCH":
                raise SystemExit(f"{root.name}/{family} source provenance replay is not a pass")
            replay_source_paths(str(row["canonical_source_sha256"]), paths, f"source provenance {root.name}/{family}")
    return sorted(rows, key=lambda row: str(row["member_token"]))


def source_rows(root: Path, family: str, provenance: list[dict[str, Any]], paf: bool, bound: dict[str, str]) -> list[dict[str, Any]]:
    """Bind a source identity ledger without inventing a missing historical one.

    Later source-native batches retain a root reconciliation key.  The Phase-0
    batches instead make their source identity/provenance binding in the
    pass-provenance preflight, so that record is the only valid fallback.  It
    is source-byte replayed above and contains one member/hash/path row per
    accepted source.  PAF records do not carry paths and therefore may never
    use the fallback.
    """
    key = root / "internal_reconciliation_key.jsonl"
    evidence = [
        root / "reviewer_a_packet.jsonl",
        root / "reviewer_b_packet.jsonl",
        root / "reviewer_b_return.jsonl",
        root / "reconciliation/final_dispositions/reconciled_family_dispositions.jsonl",
    ]
    reviewer_a = root / "reviewer_a_return.jsonl"
    reviewer_a_plural = root / "reviewer_a_returns.jsonl"
    if reviewer_a.is_file():
        evidence.append(reviewer_a)
    elif reviewer_a_plural.is_file():
        evidence.append(reviewer_a_plural)
    else:
        raise SystemExit(f"Missing source Reviewer-A return for historical provenance fallback: {root}")
    for path in evidence:
        bind(bound, path)
    final_rows = [
        row for row in read_jsonl(root / "reconciliation/final_dispositions/reconciled_family_dispositions.jsonl")
        if row.get("family_token") == family
    ]
    if len(final_rows) != 1:
        raise SystemExit(f"Expected exactly one source final-disposition row for {root.name}/{family}")
    evidence_records = final_rows[0].get("evidence_records")
    route = str(final_rows[0].get("decision_route", ""))
    direct_pass = (
        isinstance(evidence_records, dict)
        and isinstance(evidence_records.get("reviewer_a"), dict)
        and isinstance(evidence_records.get("reviewer_b"), dict)
        and evidence_records["reviewer_a"].get("decision") == "PASS_TO_PROMPT_AUTHORING"
        and evidence_records["reviewer_b"].get("decision") == "PASS_TO_PROMPT_AUTHORING"
    )
    coordinator_pass = (
        isinstance(evidence_records, dict)
        and isinstance(evidence_records.get("coordinator"), dict)
        and evidence_records["coordinator"].get("decision") == "PASS_TO_PROMPT_AUTHORING"
    )
    if "DISAGREEMENT" in route or "COORDINATOR" in route:
        coordinator_return: Path | None = None
        for path in (
            root / "reconciliation/coordinator_packet.jsonl",
            root / "reconciliation/coordinator_return.jsonl",
        ):
            bind(bound, path)
            if path.name == "coordinator_return.jsonl":
                coordinator_return = path
        coordinator_rows = [row for row in read_jsonl(coordinator_return) if row.get("family_token") == family] if coordinator_return else []
        coordinator_pass = coordinator_pass or (
            len(coordinator_rows) == 1 and coordinator_rows[0].get("decision") == "PASS_TO_PROMPT_AUTHORING"
        )
    if final_rows[0].get("final_decision") != "PASS_TO_PROMPT_AUTHORING" or not (direct_pass or coordinator_pass):
        raise SystemExit(f"Selected source family lacks a sealed two-reviewer pass record: {root.name}/{family}")
    if key.is_file():
        return root_key(root, family, bound)
    if paf:
        raise SystemExit(f"PAF source provenance may not substitute for a missing root key: {root.name}/{family}")
    return [
        {
            "canonical_source_sha256": row["canonical_source_sha256"],
            "member_token": row["member_token"],
            "source_paths": row["source_paths"],
            "source_byte_replay": row["source_byte_replay"],
        }
        for row in provenance
    ]


def paths_for_mode(root: Path, mode: str) -> tuple[Path, Path]:
    authoring = root / "reconciliation/prompt_authoring"
    if mode in {"normal", "normal_paf"}:
        leaf = authoring / "target_blind_adequacy_packets/reconciliation/final_prompt_dispositions"
        return leaf / "family_gate_dispositions.jsonl", leaf / "reconciled_prompt_dispositions.jsonl"
    if mode == "cue_reblind":
        leaf = authoring / "cue_remediation/target_blind_adequacy_packets/reconciliation/final_prompt_dispositions"
        return leaf / "family_gate_dispositions.jsonl", leaf / "reconciled_prompt_dispositions.jsonl"
    if mode == "cap" or mode == "cap_paf":
        leaf = authoring / "cue_remediation/remediation_cap_closure"
        return leaf / "terminal_family_dispositions.jsonl", leaf / "terminal_prompt_dispositions.jsonl"
    if mode == "composite_paf":
        leaf = authoring / "cue_remediation/partial_remediation_composite_closure"
        return leaf / "composite_terminal_family_dispositions.jsonl", leaf / "composite_terminal_prompt_dispositions.jsonl"
    if mode == "post_cue":
        matches = sorted(path for path in authoring.glob("batch_*_post_cue_remediation_consolidation") if (path / "family_gate_dispositions.jsonl").is_file() and (path / "active_prompt_dispositions.jsonl").is_file())
        if len(matches) != 1:
            raise SystemExit(f"Expected exactly one active post-cue consolidation under {authoring}: {matches}")
        return matches[0] / "family_gate_dispositions.jsonl", matches[0] / "active_prompt_dispositions.jsonl"
    raise SystemExit(f"Unsupported terminal mode: {mode}")


def target_key_and_packet(root: Path, use_cue: bool, bound: dict[str, str]) -> tuple[Path, Path]:
    base = root / "reconciliation/prompt_authoring"
    leaf = base / ("cue_remediation/target_blind_adequacy_packets" if use_cue else "target_blind_adequacy_packets")
    key = leaf / "internal_reconciliation_key.jsonl"
    packet = leaf / "reviewer_a_packet.jsonl"
    bind(bound, key)
    bind(bound, packet)
    return key, packet


def terminal_prompt_records(root: Path, family: str, mode: str, bound: dict[str, str]) -> list[dict[str, Any]]:
    family_path, prompt_path = paths_for_mode(root, mode)
    bind(bound, family_path)
    bind(bound, prompt_path)
    family_rows = [row for row in read_jsonl(family_path) if row.get("family_token") == family]
    if len(family_rows) != 1:
        raise SystemExit(f"Expected one terminal family row for {root.name}/{family}")
    family_row = family_rows[0]
    if mode in {"cap", "cap_paf", "composite_paf"}:
        eligible = family_row.get("terminal_family_disposition") == ELIGIBLE and family_row.get("all_three_members_pass") is True
    else:
        eligible = family_row.get("family_disposition") == ELIGIBLE
    if not eligible:
        raise SystemExit(f"State ledger selected a non-eligible terminal family: {root.name}/{family}")
    rows = [row for row in read_jsonl(prompt_path) if row.get("family_token") == family]
    if len(rows) != 3:
        raise SystemExit(f"{root.name}/{family} must have exactly three terminal prompt rows")
    prepared: list[dict[str, Any]] = []
    for row in rows:
        if mode == "post_cue":
            disposition, integrity, token = row.get("active_prompt_disposition"), row.get("active_prompt_integrity"), row.get("active_prompt_token")
            use_cue = int(row.get("remediation_round", 0)) == 1
            member = require_text(row, "intended_target_member_token", str(prompt_path))
            direct_hash = None
        elif mode in {"normal", "normal_paf", "cue_reblind"}:
            disposition, integrity, token = row.get("final_prompt_disposition"), row.get("prompt_integrity"), row.get("prompt_token")
            use_cue = mode == "cue_reblind"
            member = require_text(row, "intended_target_member_token", str(prompt_path))
            direct_hash = None
        else:
            disposition, integrity, token = row.get("terminal_prompt_disposition"), "CUE_SAFE", row.get("terminal_prompt_token")
            use_cue = mode != "composite_paf" or row.get("terminal_route") == "ONE_TIME_CUE_REMEDIATION_REPLACEMENT"
            member = require_text(row, "intended_target_member_token", str(prompt_path))
            direct_hash = require_text(row, "intended_target_source_sha256", str(prompt_path))
        if disposition != PROMPT_PASS or integrity != "CUE_SAFE" or not isinstance(token, str) or not token:
            raise SystemExit(f"Terminal prompt does not pass cue-safe local gate: {root.name}/{family}/{token}")
        prepared.append({"prompt_token": token, "member_token": member, "direct_source_hash": direct_hash, "use_cue": use_cue})
    if len({row["prompt_token"] for row in prepared}) != 3 or len({row["member_token"] for row in prepared}) != 3:
        raise SystemExit(f"{root.name}/{family} terminal prompts must target three distinct members")
    return prepared


def resolve_prompt_source(root: Path, item: dict[str, Any], family: str, bound: dict[str, str]) -> tuple[str, str]:
    if item["direct_source_hash"] is not None:
        _key, packet = target_key_and_packet(root, bool(item["use_cue"]), bound)
        return str(item["direct_source_hash"]), packet_texts(packet, {str(item["prompt_token"])}).popitem()[1]
    key_path, packet = target_key_and_packet(root, bool(item["use_cue"]), bound)
    matches = [row for row in read_jsonl(key_path) if row.get("family_token") == family and row.get("prompt_token") == item["prompt_token"]]
    if len(matches) != 1:
        raise SystemExit(f"Prompt token lacks an unambiguous target join: {key_path}/{item['prompt_token']}")
    row = matches[0]
    if row.get("intended_target_member_token") != item["member_token"]:
        raise SystemExit(f"Prompt member-token join drift for {item['prompt_token']}")
    source_hash = require_text(row, "intended_target_source_sha256", str(key_path))
    return source_hash, packet_texts(packet, {str(item["prompt_token"])}).popitem()[1]


def phase0_records(bound: dict[str, str]) -> list[tuple[str, str, Path, str, str]]:
    batch_path = PHASE0 / "phase0_batch_state.jsonl"
    family_path = PHASE0 / "phase0_family_state.jsonl"
    for path in (batch_path, family_path):
        bind(bound, path)
    batches = {row["batch"]: row for row in read_jsonl(batch_path)}
    records: list[tuple[str, str, Path, str, str]] = []
    for row in read_jsonl(family_path):
        if row.get("phase0_state") != "LOCAL_GATE_ELIGIBLE":
            continue
        batch = require_text(row, "batch", str(family_path))
        batch_row = batches.get(batch)
        if batch_row is None or not isinstance(batch_row.get("canonical_source_final"), str):
            raise SystemExit(f"Phase-0 eligible family has no batch root binding: {batch}")
        final_path = WORKSPACE / str(batch_row["canonical_source_final"])
        root = final_path.parents[2]
        kind = batch_row.get("canonical_local_gate_kind")
        mode = {
            "INITIAL_TARGET_BLIND_FINALIZER": "normal",
            "POST_CUE_REMEDIATION_CONSOLIDATION": "post_cue",
            "ONE_TIME_REMEDIATION_REBLIND_FINALIZER": "cue_reblind",
        }.get(kind)
        if mode is None:
            raise SystemExit(f"Unsupported Phase-0 local-gate kind for eligible family: {batch}/{kind}")
        records.append(("PHASE0", batch, root, require_text(row, "family_token", str(family_path)), mode))
    if len(records) != 167:
        raise SystemExit(f"Phase-0 current replay drift: expected 167 eligible families, got {len(records)}")
    return records


def terminal_records(path: Path, specs: tuple[TerminalSpec, ...], stratum: str, expected: int, bound: dict[str, str]) -> list[tuple[str, str, Path, str, str]]:
    bind(bound, path)
    spec_by_batch = {spec.batch: spec for spec in specs}
    records: list[tuple[str, str, Path, str, str]] = []
    for row in read_jsonl(path):
        eligible = row.get("locally_eligible_all_three") is True or (
            row.get("terminal_local_family_disposition") == ELIGIBLE
            and isinstance(row.get("joined_canonical_source_sha256"), list)
            and len(row["joined_canonical_source_sha256"]) == 3
        )
        if not eligible:
            continue
        batch = require_text(row, "batch", str(path))
        spec = spec_by_batch.get(batch)
        if spec is None:
            raise SystemExit(f"Terminal state contains unbound batch {batch}")
        records.append((stratum, batch, spec.root, require_text(row, "family_token", str(path)), spec.mode))
    if len(records) != expected:
        raise SystemExit(f"{stratum} terminal replay drift: expected {expected}, got {len(records)}")
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialise the RQ2b-NC 300+ Phase-3 source-union preflight.")
    parser.add_argument("--output-dir", type=Path, default=MANIFESTS / "rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2")
    parser.add_argument("--validate-only", action="store_true", help="Replay all source/prompt bindings without creating an output package.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite existing Phase-3 preflight: {out}")

    bound: dict[str, str] = {}
    for path in (SOP, BASE_CANDIDATES, CHECKPOINT_CLUSTERS, CHECKPOINT_PROMPTS, PARENT_PROMPTS, B071_SPEC):
        bind(bound, path)
    for directory in (PHASE0, V3, V4):
        bind(bound, directory / "summary.json")

    base_rows = read_jsonl(BASE_CANDIDATES)
    base_by_hash: dict[str, dict[str, Any]] = {}
    for row in base_rows:
        source_hash = require_text(row, "canonical_source_sha256", str(BASE_CANDIDATES))
        if source_hash in base_by_hash:
            raise SystemExit("Base candidate union has duplicate canonical source SHA-256")
        paths = base_source_paths(row)
        replay_source_paths(source_hash, paths, f"base candidate {source_hash}")
        base_by_hash[source_hash] = row
    if len(base_by_hash) != 3094:
        raise SystemExit(f"Base candidate-union drift: expected 3094 sources, got {len(base_by_hash)}")

    checkpoint_clusters = read_jsonl(CHECKPOINT_CLUSTERS)
    checkpoint_prompts = read_jsonl(CHECKPOINT_PROMPTS)
    parent_prompts = read_jsonl(PARENT_PROMPTS)
    if (len(checkpoint_clusters), len(checkpoint_prompts), len(parent_prompts)) != (54, 125, 381):
        raise SystemExit("Checkpoint or parent prompt anchor count drift")
    checkpoint_hashes = {source for row in checkpoint_clusters for source in row.get("candidate_source_sha256", [])}
    if not checkpoint_hashes or not checkpoint_hashes.issubset(base_by_hash):
        raise SystemExit("Checkpoint sources are not a subset of the historical base candidate union")

    family_records = phase0_records(bound)
    family_records += terminal_records(V3 / "post_phase0_terminal_local_eligibility.jsonl", V3_SPECS, "PHASE1_V3", 61, bound)
    family_records += terminal_records(V4 / "post_phase1_terminal_local_state.jsonl", V4_SPECS, "PHASE1_V4", 22, bound)
    if len(family_records) != 250 or len({(batch, family) for _, batch, _, family, _ in family_records}) != 250:
        raise SystemExit("Expected 250 source-native eligible families after the 54-cluster checkpoint")

    candidate_records: dict[str, dict[str, Any]] = {
        source_hash: {
            "canonical_source_sha256": source_hash,
            "historical_base_candidate": row,
            "local_nc_origin_records": [],
        }
        for source_hash, row in base_by_hash.items()
    }
    provenance_output: list[dict[str, Any]] = []
    local_clusters: list[dict[str, Any]] = []
    local_prompts: list[dict[str, Any]] = []

    for stratum, batch, root, family, mode in sorted(family_records, key=lambda item: (item[0], item[1], item[3])):
        provenance = provenance_rows(root, family, mode.endswith("_paf"), bound)
        sources = source_rows(root, family, provenance, mode.endswith("_paf"), bound)
        source_hashes = {str(row["canonical_source_sha256"]) for row in sources}
        if source_hashes != {str(row["canonical_source_sha256"]) for row in provenance}:
            raise SystemExit(f"Root-key/provenance source mismatch for {batch}/{family}")
        if mode.endswith("_paf"):
            for source_row in sources:
                paths = source_row.get("source_paths")
                if not isinstance(paths, list) or not paths or not all(isinstance(value, str) for value in paths):
                    raise SystemExit(f"PAF root key lacks replayable source paths for {batch}/{family}")
                replay_source_paths(str(source_row["canonical_source_sha256"]), paths, f"PAF root key {batch}/{family}")
        prompts = terminal_prompt_records(root, family, mode, bound)
        cluster_id = f"RQ2B-NC-SOURCE-NATIVE-{batch}-{family}"
        local_clusters.append({
            "audit_cluster_id": cluster_id,
            "cluster_origin": "SOURCE_NATIVE_LOCAL_GATE_ELIGIBLE_UNADMITTED",
            "phase_stratum": stratum,
            "discovery_batch": batch,
            "family_token": family,
            "candidate_source_sha256": sorted(source_hashes),
            "claim_boundary": "Phase-3 preflight only; no final cluster admission or whole-library label is established.",
        })
        by_member = {str(row["member_token"]): row for row in sources}
        for source_row, provenance_row in zip(sources, provenance):
            source_hash = str(source_row["canonical_source_sha256"])
            origin = {
                "phase_stratum": stratum,
                "discovery_batch": batch,
                "family_token": family,
                "member_token": source_row["member_token"],
                "source_paths": source_row["source_paths"],
                "provenance_record": provenance_row,
            }
            candidate_records.setdefault(source_hash, {"canonical_source_sha256": source_hash, "historical_base_candidate": None, "local_nc_origin_records": []})["local_nc_origin_records"].append(origin)
            provenance_output.append({"canonical_source_sha256": source_hash, **origin})
        for item in prompts:
            source_hash, prompt_text = resolve_prompt_source(root, item, family, bound)
            if source_hash not in source_hashes or source_hash != str(by_member[item["member_token"]]["canonical_source_sha256"]):
                raise SystemExit(f"Prompt target source is not the root-key member for {batch}/{family}/{item['prompt_token']}")
            local_prompts.append({
                "audit_prompt_id": f"RQ2B-NC-SOURCE-NATIVE-{batch}-{item['prompt_token']}",
                "prompt": prompt_text,
                "prompt_text_sha256": hashlib.sha256(prompt_text.encode("utf-8")).hexdigest(),
                "audit_cluster_id": cluster_id,
                "phase_stratum": stratum,
                "discovery_batch": batch,
                "family_token": family,
                "local_prompt_token": item["prompt_token"],
                "intended_target_source_sha256": source_hash,
                "claim_boundary": "Phase-3 preflight only; no whole-library acceptable-set label exists.",
            })

    if (len(local_clusters), len(local_prompts), len(provenance_output)) != (250, 750, 750):
        raise SystemExit("Local NC preflight cardinality drift: every eligible family requires 3 sources and 3 prompts")
    if len({row["audit_cluster_id"] for row in local_clusters}) != 250:
        raise SystemExit("Duplicate local audit cluster identifier")
    if len({row["audit_prompt_id"] for row in local_prompts}) != 750:
        raise SystemExit("Duplicate local audit prompt identifier")

    nc_clusters = [{"cluster_origin": "FROZEN_CURATION_CHECKPOINT", **row} for row in checkpoint_clusters] + local_clusters
    nc_prompts = [
        {"prompt_origin": "FROZEN_CURATION_CHECKPOINT", "prompt_text_sha256": hashlib.sha256(require_text(row, "prompt", str(CHECKPOINT_PROMPTS)).encode("utf-8")).hexdigest(), **row}
        for row in checkpoint_prompts
    ] + local_prompts
    all_prompts = [
        {"prompt_origin": "FROZEN_PARENT_V3", "prompt_text_sha256": require_text(row, "prompt_sha256", str(PARENT_PROMPTS)), **row}
        for row in parent_prompts
    ] + nc_prompts
    duplicate_prompt_groups: dict[str, list[str]] = defaultdict(list)
    for row in all_prompts:
        duplicate_prompt_groups[str(row["prompt_text_sha256"])].append(str(row.get("audit_prompt_id", row.get("prompt_id"))))
    exact_prompt_duplicates = [
        {"prompt_text_sha256": digest, "prompt_ids": sorted(ids)}
        for digest, ids in sorted(duplicate_prompt_groups.items()) if len(ids) > 1
    ]
    local_by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in provenance_output:
        local_by_hash[str(row["canonical_source_sha256"])].append(row)
    base_overlap = [
        {"canonical_source_sha256": source_hash, "historical_base_present": True, "local_occurrences": sorted(rows, key=lambda row: (row["discovery_batch"], row["family_token"], row["member_token"]))}
        for source_hash, rows in sorted(local_by_hash.items()) if source_hash in base_by_hash
    ]
    checkpoint_by_hash: dict[str, list[str]] = defaultdict(list)
    for row in checkpoint_clusters:
        for source_hash in row.get("candidate_source_sha256", []):
            checkpoint_by_hash[str(source_hash)].append(str(row["cluster_id"]))
    checkpoint_overlap = [
        {
            "canonical_source_sha256": source_hash,
            "checkpoint_cluster_ids": sorted(checkpoint_by_hash[source_hash]),
            "local_occurrences": sorted(rows, key=lambda row: (row["discovery_batch"], row["family_token"], row["member_token"])),
            "preflight_disposition": "BLOCKED_PENDING_CROSS_CLUSTER_RELATION_OR_EXCLUSION_DECISION",
        }
        for source_hash, rows in sorted(local_by_hash.items()) if source_hash in checkpoint_by_hash
    ]
    expected_candidate_count = len(set(base_by_hash) | set(local_by_hash))
    if expected_candidate_count != len(candidate_records):
        raise SystemExit("Source-canonical candidate union cardinality drift")
    if expected_candidate_count != 3810:
        raise SystemExit(f"Expected 3810 exact source-canonical candidates after local deduplication, got {expected_candidate_count}")

    summary = {
        "status": "BLOCKED_PHASE3_LOCAL_CROSS_CLUSTER_SOURCE_REUSE_REQUIRES_REVIEW" if checkpoint_overlap else "PASS_PHASE3_STRUCTURAL_SOURCE_UNION_PREFLIGHT_SEMANTIC_QA_PENDING",
        "claim_boundary": "This Phase-3 preflight creates no audit-input freeze, K=6 proposal, acceptable-set label, final benchmark, retrieval result, metric, or thesis-result update.",
        "counts": {
            "historical_base_source_canonical_candidates": len(base_by_hash),
            "local_gate_eligible_source_native_families": len(local_clusters),
            "local_gate_eligible_source_native_prompts": len(local_prompts),
            "checkpoint_clusters": len(checkpoint_clusters),
            "checkpoint_nc_prompts": len(checkpoint_prompts),
            "total_nc_clusters_preflight": len(nc_clusters),
            "total_nc_prompts_preflight": len(nc_prompts),
            "frozen_parent_prompts": len(parent_prompts),
            "total_prompt_groups_preflight": len(all_prompts),
            "source_canonical_candidates_exact_hash_unique": expected_candidate_count,
            "local_source_hashes_already_in_historical_base": len(base_overlap),
            "checkpoint_local_cross_cluster_source_reuses": len(checkpoint_overlap),
            "exact_duplicate_prompt_text_groups": len(exact_prompt_duplicates),
        },
        "required_next_phase3_checks": [
            "Resolve or explicitly exclude every cross-cluster source reuse without silently merging cluster meanings.",
            "Run semantic near-copy, lineage/quarantine, source-description-overlay, parent-NC split, and identity-cue QA.",
            "Do not freeze Phase-4 audit input while any systemic defect remains.",
        ],
        "bound_inputs": dict(sorted(bound.items())),
    }
    if args.validate_only:
        print(json.dumps({"status": summary["status"], "counts": summary["counts"]}, sort_keys=True))
        return 0

    out.mkdir(parents=True)
    outputs: dict[str, Any] = {
        "candidate_source_union.jsonl": [candidate_records[key] for key in sorted(candidate_records)],
        "nc_cluster_manifest.jsonl": sorted(nc_clusters, key=lambda row: str(row.get("audit_cluster_id", row.get("cluster_id")))),
        "nc_prompt_manifest.jsonl": sorted(nc_prompts, key=lambda row: str(row.get("audit_prompt_id", row.get("prompt_id")))),
        "parent_prompt_manifest.jsonl": sorted(parent_prompts, key=lambda row: str(row["prompt_id"])),
        "local_source_provenance_ledger.jsonl": sorted(provenance_output, key=lambda row: (row["discovery_batch"], row["family_token"], row["member_token"])),
        "historical_base_local_source_overlap.jsonl": base_overlap,
        "checkpoint_local_cross_cluster_source_reuse.jsonl": checkpoint_overlap,
        "exact_duplicate_prompt_text_groups.jsonl": exact_prompt_duplicates,
    }
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
    summary["outputs"] = {name: sha256(out / name) for name in outputs}
    write_json(out / "summary.json", summary)
    print(json.dumps({"output_dir": str(out), "status": summary["status"], "counts": summary["counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
