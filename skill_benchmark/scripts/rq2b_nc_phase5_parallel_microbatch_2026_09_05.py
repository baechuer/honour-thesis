#!/usr/bin/env python3
"""Freeze and verify controller-only Phase-5 parallel V7 microbatches.

Phase 5 is a dispatch materialiser, not a review or reconciliation tool.  It
reads only the frozen V7/V2 controller inputs and the canonical V7 reviewer
render paths.  In particular, it never reads reviewer or coordinator returns.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
V7_PROTOCOL = BENCHMARK / "scripts/rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
V7_EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
V2_AUDIT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"
V2_LEDGER = V2_AUDIT / "prompt_k6_allocation_ledger.jsonl"
V7_BATCH_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-v7-strict-unified-target-blind-batches-2026-09-05"
DEFAULT_OUT = NC_ROOT / "manifests/rq2b_nc_phase5_parallel_microbatch_2026_09_05_v1"
DEFAULT_GROUP_REPAIR_OUT = DEFAULT_OUT / "group_delivery_repair_M0002_v1"
DEFAULT_POST_INCIDENT_GROUP_DELIVERY_OUT = DEFAULT_OUT / "single_group_delivery_post_m0002_v1"

GROUP_COUNT = 1226
MAX_GROUPS = 4
MAX_BYTES = 320 * 1024
ROLES = ("A", "B")
V7_STATUS = "PASS_PHASE4_V7_STRICT_UNIFIED_BLIND_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS"
PHASE5_STATUS = "PASS_PHASE5_PARALLEL_MICROBATCH_ALLOCATION_FROZEN_PENDING_DISPATCH"
GROUP_DELIVERY_SCHEMA = "rq2b_nc_phase5_single_group_delivery_repair_v1"
POST_INCIDENT_GROUP_DELIVERY_SCHEMA = "rq2b_nc_phase5_post_incident_single_group_ab_delivery_v1"
GROUP_DELIVERY_TARGET_MICROBATCH = "RQ2B-P5-MB-0002"
OVERSIZE_SINGLETON_EXCEPTION = (
    "Amendment §3.3: an individually >320KiB exact V7 group is authorised only as an oversize singleton."
)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_sha(value: Any) -> str:
    return sha_bytes(canonical_bytes(value))


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(WORKSPACE))


def load_v7_protocol() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_phase5_v7_protocol", V7_PROTOCOL)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load frozen V7 protocol")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if module.EXECUTION != V7_EXECUTION or module.AUDIT != V2_AUDIT or module.BATCH_ROOT != V7_BATCH_ROOT:
        raise ValueError("V7 protocol binding drift")
    return module


def required_input_hashes() -> dict[str, str]:
    return {
        relative(V7_PROTOCOL): sha(V7_PROTOCOL),
        relative(V7_EXECUTION / "summary.json"): sha(V7_EXECUTION / "summary.json"),
        relative(V7_EXECUTION / "unified_prompt_group_batch_manifest.jsonl"): sha(V7_EXECUTION / "unified_prompt_group_batch_manifest.jsonl"),
        relative(V2_LEDGER): sha(V2_LEDGER),
    }


def verify_frozen_inputs(protocol: Any) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]], str]:
    for path in (V7_PROTOCOL, V7_EXECUTION / "summary.json", V7_EXECUTION / "unified_prompt_group_batch_manifest.jsonl", V2_LEDGER):
        if not path.is_file():
            raise ValueError(f"Missing Phase-5 frozen input: {path}")
    protocol.verify_execution()
    summary = read_json(V7_EXECUTION / "summary.json")
    if summary.get("status") != V7_STATUS:
        raise ValueError("V7 execution status drift")
    manifests = read_jsonl(V7_EXECUTION / "unified_prompt_group_batch_manifest.jsonl")
    if len(manifests) != GROUP_COUNT:
        raise ValueError("V7 group count drift")
    by_batch = {row.get("batch_id"): row for row in manifests}
    by_prompt = {row.get("prompt_sha256"): row for row in manifests}
    if len(by_batch) != GROUP_COUNT or len(by_prompt) != GROUP_COUNT:
        raise ValueError("V7 batch or prompt uniqueness drift")
    expected_ids = [f"RQ2B-P4-V7-U{ordinal:04d}" for ordinal in range(1, GROUP_COUNT + 1)]
    if sorted(by_batch) != expected_ids:
        raise ValueError("V7 canonical batch-id sequence drift")
    ledgers = read_jsonl(V2_LEDGER)
    by_ledger_prompt = {row.get("prompt_sha256"): row for row in ledgers}
    if len(by_ledger_prompt) != GROUP_COUNT or set(by_ledger_prompt) != set(by_prompt):
        raise ValueError("V2 ledger / V7 prompt join drift")
    _, main_by_id, tail_by_id = protocol.verify_audit()
    tails_by_prompt: dict[str, list[dict[str, Any]]] = {}
    for row in tail_by_id.values():
        tails_by_prompt.setdefault(row["prompt_sha256"], []).append(row)
    return manifests, main_by_id, tails_by_prompt, protocol.reviewer_instruction_and_schema()[0]


def expected_v7_render(
    protocol: Any,
    manifest: dict[str, Any],
    main_by_id: dict[str, dict[str, Any]],
    tails_by_prompt: dict[str, list[dict[str, Any]]],
    instruction: str,
    reviewer: str,
) -> dict[str, Any]:
    """Rebuild the exact V7 render without touching return directories."""
    if reviewer not in ROLES:
        raise ValueError(f"Unknown reviewer role: {reviewer}")
    main_spec = manifest.get("sealed_main_packet", {})
    main = main_by_id.get(main_spec.get("packet_id"))
    if main is None or canonical_sha(main) != main_spec.get("packet_sha256") or len(main.get("candidates", [])) != 6:
        raise ValueError("V7 main-packet content binding drift")
    tails = sorted(tails_by_prompt.get(manifest["prompt_sha256"], []), key=lambda row: row["packet_id"])
    expected_tail_specs = manifest.get("sealed_tail_packets")
    if not isinstance(expected_tail_specs, list) or len(tails) != 2 or len(expected_tail_specs) != 2:
        raise ValueError("V7 tail-packet cardinality drift")
    tail_by_id = {row["packet_id"]: row for row in tails}
    ordered_tails: list[dict[str, Any]] = []
    for spec in expected_tail_specs:
        tail = tail_by_id.get(spec.get("packet_id"))
        if tail is None or canonical_sha(tail) != spec.get("packet_sha256") or len(tail.get("candidates", [])) != 1:
            raise ValueError("V7 tail-packet content binding drift")
        ordered_tails.append(tail)
    candidates = [{"candidate_token": item["candidate_token"], "source_full_skill": item["source_full_skill"]} for item in main["candidates"]]
    candidates.extend(
        {"candidate_token": item["candidate_token"], "source_full_skill": item["source_full_skill"]}
        for tail in ordered_tails
        for item in tail["candidates"]
    )
    candidates.sort(key=lambda item: item["candidate_token"])
    tokens = [item["candidate_token"] for item in candidates]
    if len(tokens) != 8 or len(set(tokens)) != 8 or canonical_sha(tokens) != manifest.get("unified_candidate_tokens_sha256"):
        raise ValueError("V7 unified candidate binding drift")
    packet = {
        "blind_packet_id": manifest["blind_packet_id"],
        "prompt": main["prompt"],
        "candidates": candidates,
        "review_instruction": instruction,
    }
    output = {
        "schema_version": "rq2b_nc_phase4_v7_strict_unified_blind_render",
        "batch_id": manifest["batch_id"],
        "reviewer_blind_id": reviewer,
        "batch_input_sha256": canonical_sha(packet),
        "reviewer_instruction_sha256": manifest["reviewer_instruction_sha256"],
        "blindness_notice": "This file contains no target, main/tail role, rank, lane, proposal channel, source path/provenance/licence, peer return, retrieval/reranking/provider outcome or metric. Review only this file and the frozen V7 schema.",
        "packet": packet,
    }
    if set(output) != protocol.RENDER_TOP_LEVEL or protocol.keys_deep(output) & protocol.FORBIDDEN_KEYS:
        raise ValueError("V7 expected render allowlist or blindness drift")
    return output


def ledger_source_set(ledger: dict[str, Any]) -> list[str]:
    source_sha = [row.get("canonical_source_sha256") for row in ledger.get("main_allocation", [])]
    source_sha.extend(row.get("canonical_source_sha256") for row in ledger.get("tail_allocation", []))
    if len(source_sha) != 8 or any(not isinstance(value, str) or len(value) != 64 for value in source_sha) or len(set(source_sha)) != 8:
        raise ValueError(f"V2 ledger source-set drift for {ledger.get('prompt_sha256')}")
    return sorted(source_sha)


@dataclass(frozen=True)
class Group:
    batch_id: str
    prompt_sha256: str
    family_key: tuple[str, str]
    source_sha256_set: tuple[str, ...]
    status: str
    renders: dict[str, dict[str, Any]]
    render_bytes: dict[str, int]
    render_sha256: dict[str, str]
    artifact_paths: dict[str, str]


def classify_group(batch_id: str, renders: dict[str, dict[str, Any]]) -> tuple[str, dict[str, str]]:
    paths = {role: V7_BATCH_ROOT / f"reviewer_{role}" / f"{batch_id}.json" for role in ROLES}
    exists = {role: path.is_file() for role, path in paths.items()}
    if all(exists.values()):
        # A present canonical artifact must be the exact frozen V7 render.
        for role, path in paths.items():
            if path.read_bytes() != pretty_bytes(renders[role]):
                raise ValueError(f"V7 canonical render content drift: {relative(path)}")
        status = "COMPLETED_CANONICAL_V7_RENDER_EXISTS"
    elif any(exists.values()):
        status = "INFLIGHT_PARTIAL_CANONICAL_V7_RENDER_EXISTS"
    else:
        status = "UNSTARTED_NO_CANONICAL_V7_RENDER_EXISTS"
    return status, {role: relative(path) for role, path in paths.items()}


def reconstruct_groups() -> list[Group]:
    protocol = load_v7_protocol()
    manifests, main_by_id, _tails_by_prompt, instruction = verify_frozen_inputs(protocol)
    ledgers = {row["prompt_sha256"]: row for row in read_jsonl(V2_LEDGER)}
    groups: list[Group] = []
    for manifest in sorted(manifests, key=lambda row: row["batch_id"]):
        ledger = ledgers[manifest["prompt_sha256"]]
        lane = ledger.get("lane_id")
        reporting_group = ledger.get("reporting_group")
        if not isinstance(lane, str) or not isinstance(reporting_group, str) or not lane or not reporting_group:
            raise ValueError("V2 ledger family key drift")
        renders = {
            role: expected_v7_render(protocol, manifest, main_by_id, _tails_by_prompt, instruction, role)
            for role in ROLES
        }
        status, paths = classify_group(manifest["batch_id"], renders)
        group = Group(
            batch_id=manifest["batch_id"],
            prompt_sha256=manifest["prompt_sha256"],
            family_key=(lane, reporting_group),
            source_sha256_set=tuple(ledger_source_set(ledger)),
            status=status,
            renders=renders,
            render_bytes={role: len(pretty_bytes(renders[role])) for role in ROLES},
            render_sha256={role: sha_bytes(pretty_bytes(renders[role])) for role in ROLES},
            artifact_paths=paths,
        )
        groups.append(group)
    if len(groups) != GROUP_COUNT or len({group.batch_id for group in groups}) != GROUP_COUNT:
        raise ValueError("Phase-5 reconstructed group cardinality drift")
    return groups


def controller_group_row(group: Group) -> dict[str, Any]:
    return {
        "batch_id": group.batch_id,
        "canonical_v7_artifact_paths": group.artifact_paths,
        "canonical_v7_render_bytes": group.render_bytes,
        "canonical_v7_render_sha256": group.render_sha256,
        "family_key": {"lane_id": group.family_key[0], "reporting_group": group.family_key[1]},
        "prompt_sha256": group.prompt_sha256,
        "source_sha256_set": list(group.source_sha256_set),
        "transition_status": group.status,
    }


def allocate(unstarted: list[Group]) -> list[list[Group]]:
    """Lexical first-fit allocation; all constraints are checked before append."""
    buckets: list[list[Group]] = []
    for group in sorted(unstarted, key=lambda item: item.batch_id):
        # §3.3 permits an individually oversized exact V7 render only in its
        # own bucket.  The byte test below keeps all following groups out.
        for bucket in buckets:
            bucket_sources = {source for item in bucket for source in item.source_sha256_set}
            bucket_families = {item.family_key for item in bucket}
            if len(bucket) >= MAX_GROUPS or group.family_key in bucket_families or bucket_sources & set(group.source_sha256_set):
                continue
            if any(sum(item.render_bytes[role] for item in bucket) + group.render_bytes[role] > MAX_BYTES for role in ROLES):
                continue
            bucket.append(group)
            break
        else:
            buckets.append([group])
    allocated_ids = [group.batch_id for bucket in buckets for group in bucket]
    expected_ids = [group.batch_id for group in sorted(unstarted, key=lambda item: item.batch_id)]
    if len(allocated_ids) != len(set(allocated_ids)) or set(allocated_ids) != set(expected_ids):
        raise ValueError("Phase-5 greedy membership drift")
    return buckets


def microbatch_rows(buckets: list[list[Group]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ordinal, bucket in enumerate(buckets, start=1):
        source_sets = [set(group.source_sha256_set) for group in bucket]
        family_keys = [group.family_key for group in bucket]
        if len(bucket) > MAX_GROUPS or len(set(family_keys)) != len(family_keys):
            raise ValueError("Phase-5 microbatch cardinality or family conflict")
        for left in range(len(source_sets)):
            for right in range(left + 1, len(source_sets)):
                if source_sets[left] & source_sets[right]:
                    raise ValueError("Phase-5 microbatch source conflict")
        totals = {role: sum(group.render_bytes[role] for group in bucket) for role in ROLES}
        oversize_singleton = len(bucket) == 1 and any(bucket[0].render_bytes[role] > MAX_BYTES for role in ROLES)
        if any(total > MAX_BYTES for total in totals.values()) and not oversize_singleton:
            raise ValueError("Phase-5 microbatch byte ceiling conflict")
        rows.append({
            "amendment_exception": OVERSIZE_SINGLETON_EXCEPTION if oversize_singleton else None,
            "allocation_rule": "lexical_batch_id_first_fit; maximum four groups; no shared lane_id/reporting_group family; no shared canonical source SHA-256; each reviewer envelope at most 320KiB of exact V7 renders",
            "batch_ids": [group.batch_id for group in bucket],
            "controller_family_keys": [{"lane_id": group.family_key[0], "reporting_group": group.family_key[1]} for group in bucket],
            "controller_source_sha256_sets": [list(group.source_sha256_set) for group in bucket],
            "expected_render_bytes": totals,
            "group_count": len(bucket),
            "microbatch_id": f"RQ2B-P5-MB-{ordinal:04d}",
            "oversize_singleton": oversize_singleton,
        })
    return rows


def reviewer_envelopes(buckets: list[list[Group]], role: str) -> list[dict[str, Any]]:
    # Reviewer-facing records have exactly these three fields.  The nested
    # render is byte-for-byte the V7 JSON render, not a Phase-5 reinterpretation.
    return [
        {"microbatch_id": f"RQ2B-P5-MB-{ordinal:04d}", "reviewer_role": role, "v7_render": group.renders[role]}
        for ordinal, bucket in enumerate(buckets, start=1)
        for group in bucket
    ]


def output_payload(groups: list[Group]) -> tuple[dict[str, bytes], dict[str, Any]]:
    counts = {status: sum(group.status == status for group in groups) for status in (
        "COMPLETED_CANONICAL_V7_RENDER_EXISTS",
        "INFLIGHT_PARTIAL_CANONICAL_V7_RENDER_EXISTS",
        "UNSTARTED_NO_CANONICAL_V7_RENDER_EXISTS",
    )}
    if counts["INFLIGHT_PARTIAL_CANONICAL_V7_RENDER_EXISTS"]:
        raise ValueError("Refusing Phase-5 freeze: in-flight partial V7 canonical render(s) exist")
    unstarted = [group for group in groups if group.status == "UNSTARTED_NO_CANONICAL_V7_RENDER_EXISTS"]
    buckets = allocate(unstarted)
    microbatches = microbatch_rows(buckets)
    oversize_records = [record for record in microbatches if record["oversize_singleton"]]
    envelopes = {role: reviewer_envelopes(buckets, role) for role in ROLES}
    files = {
        "controller_group_transition_list.jsonl": jsonl_bytes([controller_group_row(group) for group in groups]),
        "controller_unstarted_microbatch_records.jsonl": jsonl_bytes(microbatches),
        "sealed_reviewer_A_envelope.jsonl": jsonl_bytes(envelopes["A"]),
        "sealed_reviewer_B_envelope.jsonl": jsonl_bytes(envelopes["B"]),
    }
    envelope_hashes = {
        name: {"bytes": len(files[name]), "sha256": sha_bytes(files[name])}
        for name in ("sealed_reviewer_A_envelope.jsonl", "sealed_reviewer_B_envelope.jsonl")
    }
    files["sealed_reviewer_envelope_hashes.json"] = pretty_bytes(envelope_hashes)
    transition = {
        "status": PHASE5_STATUS,
        "claim_boundary": "Phase 5 freezes only controller allocation and reviewer-facing copies of exact V7 renders. It does not read, validate, infer, reconcile, or record any reviewer or coordinator semantic decision.",
        "classification_rule": "completed means both canonical V7 reviewer render artifacts exist; inflight means exactly one exists; unstarted means neither exists. Any inflight group aborts freezing.",
        "counts": {
            "completed": counts["COMPLETED_CANONICAL_V7_RENDER_EXISTS"],
            "inflight": counts["INFLIGHT_PARTIAL_CANONICAL_V7_RENDER_EXISTS"],
            "microbatches": len(microbatches),
            "oversize_singleton_count": len(oversize_records),
            "oversize_singleton_batch_ids": [record["batch_ids"][0] for record in oversize_records],
            "unstarted": counts["UNSTARTED_NO_CANONICAL_V7_RENDER_EXISTS"],
            "v7_groups": len(groups),
        },
        "limits": {"max_groups_per_microbatch": MAX_GROUPS, "max_exact_v7_render_bytes_per_reviewer_microbatch": MAX_BYTES},
        "frozen_inputs": required_input_hashes(),
        "implementation": {"path": relative(Path(__file__)), "sha256": sha(Path(__file__)), "python": sys.version},
        "outputs": {name: sha_bytes(value) for name, value in files.items()},
    }
    files["transition_summary.json"] = pretty_bytes(transition)
    return files, transition


def write_payload(out: Path, files: dict[str, bytes]) -> None:
    out.mkdir(parents=True)
    for name, value in files.items():
        (out / name).write_bytes(value)


def delivery_path(out: Path, microbatch_id: str, reviewer: str) -> Path:
    if reviewer not in ROLES:
        raise ValueError(f"Unknown reviewer role: {reviewer}")
    if not microbatch_id.startswith("RQ2B-P5-MB-"):
        raise ValueError("Invalid Phase-5 microbatch id")
    return out.resolve() / "delivery" / microbatch_id / f"reviewer_{reviewer}"


def load_sealed_microbatch_envelope(out: Path, microbatch_id: str, reviewer: str) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Read only allocation/envelope records; never inspect a reviewer return."""
    out = out.resolve()
    summary_path = out / "transition_summary.json"
    hashes_path = out / "sealed_reviewer_envelope_hashes.json"
    records_path = out / "controller_unstarted_microbatch_records.jsonl"
    envelope_path = out / f"sealed_reviewer_{reviewer}_envelope.jsonl"
    for path in (summary_path, hashes_path, records_path, envelope_path):
        if not path.is_file():
            raise ValueError(f"Missing frozen Phase-5 allocation artifact: {path}")
    summary = read_json(summary_path)
    if summary.get("status") != PHASE5_STATUS:
        raise ValueError("Phase-5 allocation status drift")
    outputs = summary.get("outputs", {})
    if outputs.get(hashes_path.name) != sha(hashes_path) or outputs.get(records_path.name) != sha(records_path):
        raise ValueError("Phase-5 allocation output-hash drift")
    hashes = read_json(hashes_path)
    hash_record = hashes.get(envelope_path.name)
    if not isinstance(hash_record, dict) or hash_record.get("sha256") != sha(envelope_path) or hash_record.get("bytes") != envelope_path.stat().st_size:
        raise ValueError("Phase-5 sealed reviewer-envelope hash or byte drift")
    record_rows = [row for row in read_jsonl(records_path) if row.get("microbatch_id") == microbatch_id]
    if len(record_rows) != 1:
        raise ValueError("Unknown or ambiguous frozen Phase-5 microbatch")
    envelope_rows = [row for row in read_jsonl(envelope_path) if row.get("microbatch_id") == microbatch_id]
    if len(envelope_rows) != record_rows[0].get("group_count"):
        raise ValueError("Phase-5 microbatch envelope membership drift")
    if any(set(row) != {"reviewer_role", "microbatch_id", "v7_render"} or row["reviewer_role"] != reviewer for row in envelope_rows):
        raise ValueError("Phase-5 reviewer-envelope field drift")
    expected_batch_ids = record_rows[0].get("batch_ids")
    actual_batch_ids = [row["v7_render"].get("batch_id") for row in envelope_rows]
    if actual_batch_ids != expected_batch_ids:
        raise ValueError("Phase-5 microbatch V7-render membership drift")
    return envelope_rows, record_rows[0], hash_record


def canonical_v7_path(role: str, batch_id: str) -> Path:
    return V7_BATCH_ROOT / f"reviewer_{role}" / f"{batch_id}.json"


def paired_microbatch_envelopes(out: Path, microbatch_id: str) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    by_role: dict[str, list[dict[str, Any]]] = {}
    record: dict[str, Any] | None = None
    for role in ROLES:
        rows, role_record, _ = load_sealed_microbatch_envelope(out, microbatch_id, role)
        if record is None:
            record = role_record
        elif role_record != record:
            raise ValueError("Phase-5 A/B microbatch-record binding drift")
        by_role[role] = rows
    if record is None:
        raise ValueError("Missing Phase-5 microbatch record")
    return by_role, record


def materialise_or_verify_canonical_v7_renders(out: Path, microbatch_id: str) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Create only absent V7 renders; existing canonical files must match exactly."""
    by_role, record = paired_microbatch_envelopes(out, microbatch_id)
    for role, rows in by_role.items():
        for row in rows:
            batch_id = row["v7_render"]["batch_id"]
            path = canonical_v7_path(role, batch_id)
            expected = pretty_bytes(row["v7_render"])
            if path.exists():
                if not path.is_file() or path.read_bytes() != expected:
                    raise ValueError(f"Canonical V7 render exists but does not match: {relative(path)}")
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            # The path was checked immediately above: this never overwrites.
            path.write_bytes(expected)
    return by_role, record


def verify_canonical_v7_renders(out: Path, microbatch_id: str) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    by_role, record = paired_microbatch_envelopes(out, microbatch_id)
    for role, rows in by_role.items():
        for row in rows:
            batch_id = row["v7_render"]["batch_id"]
            path = canonical_v7_path(role, batch_id)
            if not path.is_file() or path.read_bytes() != pretty_bytes(row["v7_render"]):
                raise ValueError(f"Canonical V7 render missing or byte-drifted: {relative(path)}")
    return by_role, record


def extract(out: Path, microbatch_id: str, reviewer: str) -> None:
    # Materialise both roles first so the frozen V7 validator has its required
    # canonical paths regardless of which single-role transport is requested.
    materialise_or_verify_canonical_v7_renders(out, microbatch_id)
    envelope_rows, record, source_hash = load_sealed_microbatch_envelope(out, microbatch_id, reviewer)
    destination = delivery_path(out, microbatch_id, reviewer)
    if destination.exists():
        raise ValueError(f"Refusing to overwrite extracted Phase-5 delivery: {destination}")
    envelope_path = destination / "reviewer_envelope.json"
    envelope_bytes = pretty_bytes(envelope_rows)
    sidecar = {
        "bound_sealed_envelope": {
            "bytes": source_hash["bytes"],
            "path": relative(out.resolve() / f"sealed_reviewer_{reviewer}_envelope.jsonl"),
            "sha256": source_hash["sha256"],
        },
        "exact_v7_batch_ids": record["batch_ids"],
        "microbatch_id": microbatch_id,
        "reviewer_envelope": {"bytes": len(envelope_bytes), "path": envelope_path.name, "sha256": sha_bytes(envelope_bytes)},
        "reviewer_role": reviewer,
        "status": "PASS_PHASE5_SINGLE_MICROBATCH_REVIEWER_ENVELOPE_EXTRACTED",
    }
    destination.mkdir(parents=True)
    envelope_path.write_bytes(envelope_bytes)
    (destination / "delivery_hashes.json").write_bytes(pretty_bytes(sidecar))
    print(json.dumps({"bytes": len(envelope_bytes), "microbatch_id": microbatch_id, "output": str(destination), "reviewer": reviewer, "sha256": sha_bytes(envelope_bytes), "status": sidecar["status"]}, sort_keys=True))


def verify_delivery(out: Path, microbatch_id: str, reviewer: str) -> None:
    verify_canonical_v7_renders(out, microbatch_id)
    envelope_rows, record, source_hash = load_sealed_microbatch_envelope(out, microbatch_id, reviewer)
    destination = delivery_path(out, microbatch_id, reviewer)
    envelope_path = destination / "reviewer_envelope.json"
    sidecar_path = destination / "delivery_hashes.json"
    if not destination.is_dir() or {path.name for path in destination.iterdir() if path.is_file()} != {envelope_path.name, sidecar_path.name}:
        raise ValueError("Phase-5 extracted delivery membership drift")
    expected_envelope = pretty_bytes(envelope_rows)
    if not envelope_path.is_file() or envelope_path.read_bytes() != expected_envelope:
        raise ValueError("Phase-5 extracted reviewer-envelope byte drift")
    expected_sidecar = {
        "bound_sealed_envelope": {
            "bytes": source_hash["bytes"],
            "path": relative(out.resolve() / f"sealed_reviewer_{reviewer}_envelope.jsonl"),
            "sha256": source_hash["sha256"],
        },
        "exact_v7_batch_ids": record["batch_ids"],
        "microbatch_id": microbatch_id,
        "reviewer_envelope": {"bytes": len(expected_envelope), "path": envelope_path.name, "sha256": sha_bytes(expected_envelope)},
        "reviewer_role": reviewer,
        "status": "PASS_PHASE5_SINGLE_MICROBATCH_REVIEWER_ENVELOPE_EXTRACTED",
    }
    if not sidecar_path.is_file() or read_json(sidecar_path) != expected_sidecar:
        raise ValueError("Phase-5 extracted delivery sidecar drift")
    print(json.dumps({"bytes": len(expected_envelope), "microbatch_id": microbatch_id, "output": str(destination), "reviewer": reviewer, "status": "PASS_PHASE5_SINGLE_MICROBATCH_REVIEWER_ENVELOPE_VERIFIED"}, sort_keys=True))


def group_delivery_path(repair_out: Path, microbatch_id: str, batch_id: str, reviewer: str) -> Path:
    if reviewer not in ROLES:
        raise ValueError(f"Unknown reviewer role: {reviewer}")
    return repair_out.resolve() / "delivery" / microbatch_id / batch_id / f"reviewer_{reviewer}"


def group_delivery_controller_path(repair_out: Path) -> Path:
    return repair_out.resolve() / "controller_group_delivery_manifest.jsonl"


def require_group_delivery_target(microbatch_id: str) -> None:
    if microbatch_id != GROUP_DELIVERY_TARGET_MICROBATCH:
        raise ValueError(
            "This operational repair is deliberately limited to frozen microbatch "
            f"{GROUP_DELIVERY_TARGET_MICROBATCH}"
        )


def group_delivery_contract(microbatch_id: str, reviewer: str, render: dict[str, Any]) -> dict[str, Any]:
    """The only reviewer-facing companion to one exact V7 render.

    It contains just the selected group's return anchors and tokens.  It does
    not carry the other groups in the parent microbatch, allocation metadata,
    or any review outcome.
    """
    tokens = [candidate["candidate_token"] for candidate in render["packet"]["candidates"]]
    return {
        "batch_id": render["batch_id"],
        "output_contract": {
            "assessment_candidate_tokens": tokens,
            "batch_input_sha256": render["batch_input_sha256"],
            "reviewer_blind_id": reviewer,
            "reviewer_instruction_sha256": render["reviewer_instruction_sha256"],
            "return_top_level_fields": ["assessments", "batch_id", "batch_input_sha256", "reviewer_blind_id", "reviewer_instruction_sha256"],
        },
        "parent_microbatch_id": microbatch_id,
        "reviewer_role": reviewer,
        "schema_version": GROUP_DELIVERY_SCHEMA,
        "status": "SINGLE_GROUP_OUTPUT_ONLY",
    }


def group_delivery_rows(
    out: Path,
    repair_out: Path,
    microbatch_id: str,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Bind every A/B single-group delivery to the already frozen allocation."""
    require_group_delivery_target(microbatch_id)
    by_role, record = verify_canonical_v7_renders(out, microbatch_id)
    allocation_path = out.resolve() / "controller_unstarted_microbatch_records.jsonl"
    rows: list[dict[str, Any]] = []
    for role in ROLES:
        for envelope in by_role[role]:
            render = envelope["v7_render"]
            batch_id = render["batch_id"]
            render_bytes = pretty_bytes(render)
            contract_bytes = pretty_bytes(group_delivery_contract(microbatch_id, role, render))
            destination = group_delivery_path(repair_out, microbatch_id, batch_id, role)
            rows.append({
                "batch_id": batch_id,
                "canonical_v7_render": {
                    "bytes": len(render_bytes),
                    "path": relative(canonical_v7_path(role, batch_id)),
                    "sha256": sha_bytes(render_bytes),
                },
                "candidate_token_count": len(render["packet"]["candidates"]),
                "candidate_tokens_sha256": canonical_sha([candidate["candidate_token"] for candidate in render["packet"]["candidates"]]),
                "delivery_path": relative(destination),
                "parent_microbatch_allocation": {
                    "microbatch_id": microbatch_id,
                    "record_path": relative(allocation_path),
                    "record_sha256": canonical_sha(record),
                },
                "v7_batch_input_sha256": render["batch_input_sha256"],
                "reviewer_role": role,
                "schema_version": GROUP_DELIVERY_SCHEMA,
                "single_group_output_contract": {
                    "bytes": len(contract_bytes),
                    "filename": "single_group_output_contract.json",
                    "sha256": sha_bytes(contract_bytes),
                },
                "v7_render_filename": "v7_render.json",
            })
    if len(rows) != len(record["batch_ids"]) * len(ROLES):
        raise ValueError("Group-delivery controller cardinality drift")
    return rows, by_role, record


def prepare_group_delivery_controller(
    out: Path,
    repair_out: Path,
    microbatch_id: str,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    rows, by_role, record = group_delivery_rows(out, repair_out, microbatch_id)
    controller_path = group_delivery_controller_path(repair_out)
    expected = jsonl_bytes(rows)
    if controller_path.exists():
        if not controller_path.is_file() or controller_path.read_bytes() != expected:
            raise ValueError("Refusing group-delivery controller manifest drift or overwrite")
    else:
        repair_out.resolve().mkdir(parents=True, exist_ok=True)
        controller_path.write_bytes(expected)
    return rows, by_role, record


def group_delivery_leak_check(
    delivery: Path,
    render: dict[str, Any],
    contract: dict[str, Any],
    peer_renders: list[dict[str, Any]],
) -> None:
    """Reject any peer prompt, V7 batch id, or candidate token in one delivery."""
    render_path = delivery / "v7_render.json"
    contract_path = delivery / "single_group_output_contract.json"
    if {path.name for path in delivery.iterdir() if path.is_file()} != {render_path.name, contract_path.name}:
        raise ValueError("Group-delivery file membership drift")
    if render_path.read_bytes() != pretty_bytes(render) or contract_path.read_bytes() != pretty_bytes(contract):
        raise ValueError("Group-delivery byte binding drift")
    payload = render_path.read_bytes() + b"\n" + contract_path.read_bytes()
    own_batch_id = render["batch_id"]
    own_tokens = {candidate["candidate_token"] for candidate in render["packet"]["candidates"]}
    if not isinstance(render["packet"].get("prompt"), str) or set(render) != load_v7_protocol().RENDER_TOP_LEVEL:
        raise ValueError("Group-delivery V7 render shape drift")
    for peer in peer_renders:
        if peer["batch_id"] == own_batch_id:
            continue
        if peer["batch_id"].encode("utf-8") in payload:
            raise ValueError("Group-delivery peer batch-id leakage")
        peer_prompt = peer["packet"]["prompt"].encode("utf-8")
        if peer_prompt != render["packet"]["prompt"].encode("utf-8") and peer_prompt in payload:
            raise ValueError("Group-delivery peer prompt leakage")
        for candidate in peer["packet"]["candidates"]:
            token = candidate["candidate_token"]
            if token not in own_tokens and token.encode("utf-8") in payload:
                raise ValueError("Group-delivery peer candidate-token leakage")


def extract_group_delivery(out: Path, repair_out: Path, microbatch_id: str, batch_id: str, reviewer: str) -> None:
    rows, by_role, record = prepare_group_delivery_controller(out, repair_out, microbatch_id)
    if batch_id not in record["batch_ids"]:
        raise ValueError("Batch is not a member of the frozen target microbatch")
    render = next(row["v7_render"] for row in by_role[reviewer] if row["v7_render"]["batch_id"] == batch_id)
    destination = group_delivery_path(repair_out, microbatch_id, batch_id, reviewer)
    if destination.exists():
        raise ValueError(f"Refusing to overwrite extracted single-group delivery: {destination}")
    contract = group_delivery_contract(microbatch_id, reviewer, render)
    destination.mkdir(parents=True)
    (destination / "v7_render.json").write_bytes(pretty_bytes(render))
    (destination / "single_group_output_contract.json").write_bytes(pretty_bytes(contract))
    peer_renders = [row["v7_render"] for row in by_role[reviewer]]
    group_delivery_leak_check(destination, render, contract, peer_renders)
    controller_row = next(row for row in rows if row["batch_id"] == batch_id and row["reviewer_role"] == reviewer)
    print(json.dumps({"batch_id": batch_id, "controller_row_sha256": canonical_sha(controller_row), "microbatch_id": microbatch_id, "output": str(destination), "reviewer": reviewer, "status": "PASS_PHASE5_SINGLE_GROUP_DELIVERY_EXTRACTED"}, sort_keys=True))


def verify_group_delivery(out: Path, repair_out: Path, microbatch_id: str, batch_id: str, reviewer: str) -> dict[str, Any]:
    rows, by_role, record = prepare_group_delivery_controller(out, repair_out, microbatch_id)
    if batch_id not in record["batch_ids"]:
        raise ValueError("Batch is not a member of the frozen target microbatch")
    render = next(row["v7_render"] for row in by_role[reviewer] if row["v7_render"]["batch_id"] == batch_id)
    contract = group_delivery_contract(microbatch_id, reviewer, render)
    destination = group_delivery_path(repair_out, microbatch_id, batch_id, reviewer)
    if not destination.is_dir():
        raise ValueError("Missing single-group delivery")
    group_delivery_leak_check(destination, render, contract, [row["v7_render"] for row in by_role[reviewer]])
    controller_row = next(row for row in rows if row["batch_id"] == batch_id and row["reviewer_role"] == reviewer)
    result = {
        "batch_id": batch_id,
        "controller_row_sha256": canonical_sha(controller_row),
        "delivery_v7_render_sha256": sha_bytes(pretty_bytes(render)),
        "microbatch_id": microbatch_id,
        "no_leak_check": "PASS_NO_PEER_PROMPT_BATCH_ID_OR_CANDIDATE_TOKEN",
        "reviewer_role": reviewer,
        "status": "PASS_PHASE5_SINGLE_GROUP_DELIVERY_VERIFIED",
    }
    print(json.dumps(result, sort_keys=True))
    return result


def structural_group_delivery_repair(out: Path, repair_out: Path, microbatch_id: str) -> None:
    """Write a no-outcomes structural report after every target delivery verifies."""
    require_group_delivery_target(microbatch_id)
    report_path = repair_out.resolve() / "phase5_group_delivery_repair_report.json"
    if report_path.exists():
        raise ValueError(f"Refusing to overwrite immutable group-delivery repair report: {report_path}")
    rows, _by_role, record = prepare_group_delivery_controller(out, repair_out, microbatch_id)
    checks: list[dict[str, Any]] = []
    for batch_id in record["batch_ids"]:
        for reviewer in ROLES:
            checks.append(verify_group_delivery(out, repair_out, microbatch_id, batch_id, reviewer))
    report = {
        "claim_boundary": "This is an operational transport repair only. It verifies exact V7 render bytes, single-group output contracts, frozen allocation binding, hashes and peer-leak exclusion. It does not dispatch a review or read, infer, validate, reconcile or record any semantic reviewer outcome.",
        "controller_manifest": {
            "path": relative(group_delivery_controller_path(repair_out)),
            "rows": len(rows),
            "sha256": sha(group_delivery_controller_path(repair_out)),
        },
        "frozen_phase5_allocation": {
            "microbatch_id": microbatch_id,
            "record_sha256": canonical_sha(record),
            "transition_summary_sha256": sha(out.resolve() / "transition_summary.json"),
        },
        "checks": checks,
        "status": "PASS_PHASE5_GROUP_DELIVERY_REPAIR_M0002_STRUCTURAL_ONLY",
    }
    report_path.write_bytes(pretty_bytes(report))
    print(json.dumps({"checks": len(checks), "output": str(report_path), "status": report["status"]}, sort_keys=True))


def post_incident_group_delivery_controller_path(delivery_out: Path, microbatch_id: str) -> Path:
    """Keep post-incident controller manifests disjoint from the M0002 repair."""
    return delivery_out.resolve() / "controller" / microbatch_id / "controller_group_delivery_manifest.jsonl"


def post_incident_group_delivery_contract(microbatch_id: str, reviewer: str, render: dict[str, Any]) -> dict[str, Any]:
    """Return the same narrow contract with an explicit prospective-control identity."""
    contract = group_delivery_contract(microbatch_id, reviewer, render)
    contract["schema_version"] = POST_INCIDENT_GROUP_DELIVERY_SCHEMA
    contract["status"] = "POST_INCIDENT_SINGLE_GROUP_OUTPUT_ONLY"
    return contract


def post_incident_group_delivery_rows(
    out: Path,
    delivery_out: Path,
    microbatch_id: str,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Bind all roles/groups in any frozen microbatch without accessing returns."""
    by_role, record = verify_canonical_v7_renders(out, microbatch_id)
    allocation_path = out.resolve() / "controller_unstarted_microbatch_records.jsonl"
    rows: list[dict[str, Any]] = []
    for role in ROLES:
        for envelope in by_role[role]:
            render = envelope["v7_render"]
            batch_id = render["batch_id"]
            render_bytes = pretty_bytes(render)
            contract_bytes = pretty_bytes(post_incident_group_delivery_contract(microbatch_id, role, render))
            destination = group_delivery_path(delivery_out, microbatch_id, batch_id, role)
            rows.append({
                "batch_id": batch_id,
                "canonical_v7_render": {
                    "bytes": len(render_bytes),
                    "path": relative(canonical_v7_path(role, batch_id)),
                    "sha256": sha_bytes(render_bytes),
                },
                "candidate_token_count": len(render["packet"]["candidates"]),
                "candidate_tokens_sha256": canonical_sha([candidate["candidate_token"] for candidate in render["packet"]["candidates"]]),
                "delivery_path": relative(destination),
                "parent_microbatch_allocation": {
                    "microbatch_id": microbatch_id,
                    "record_path": relative(allocation_path),
                    "record_sha256": canonical_sha(record),
                },
                "v7_batch_input_sha256": render["batch_input_sha256"],
                "reviewer_role": role,
                "schema_version": POST_INCIDENT_GROUP_DELIVERY_SCHEMA,
                "single_group_output_contract": {
                    "bytes": len(contract_bytes),
                    "filename": "single_group_output_contract.json",
                    "sha256": sha_bytes(contract_bytes),
                },
                "v7_render_filename": "v7_render.json",
            })
    if len(rows) != len(record["batch_ids"]) * len(ROLES):
        raise ValueError("Post-incident group-delivery controller cardinality drift")
    return rows, by_role, record


def prepare_post_incident_group_delivery_controller(
    out: Path,
    delivery_out: Path,
    microbatch_id: str,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    rows, by_role, record = post_incident_group_delivery_rows(out, delivery_out, microbatch_id)
    controller_path = post_incident_group_delivery_controller_path(delivery_out, microbatch_id)
    expected = jsonl_bytes(rows)
    if controller_path.exists():
        if not controller_path.is_file() or controller_path.read_bytes() != expected:
            raise ValueError("Refusing post-incident group-delivery controller manifest drift or overwrite")
    else:
        controller_path.parent.mkdir(parents=True, exist_ok=True)
        controller_path.write_bytes(expected)
    return rows, by_role, record


def verify_post_incident_group_delivery_controller(
    out: Path,
    delivery_out: Path,
    microbatch_id: str,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    rows, by_role, record = post_incident_group_delivery_rows(out, delivery_out, microbatch_id)
    controller_path = post_incident_group_delivery_controller_path(delivery_out, microbatch_id)
    if not controller_path.is_file() or controller_path.read_bytes() != jsonl_bytes(rows):
        raise ValueError("Missing or byte-drifted post-incident group-delivery controller manifest")
    return rows, by_role, record


def post_incident_group_delivery_checks(
    out: Path,
    delivery_out: Path,
    microbatch_id: str,
    batch_id: str,
) -> list[dict[str, Any]]:
    rows, by_role, record = verify_post_incident_group_delivery_controller(out, delivery_out, microbatch_id)
    if batch_id not in record["batch_ids"]:
        raise ValueError("Batch is not a member of the frozen post-incident microbatch")
    checks: list[dict[str, Any]] = []
    for reviewer in ROLES:
        render = next(row["v7_render"] for row in by_role[reviewer] if row["v7_render"]["batch_id"] == batch_id)
        contract = post_incident_group_delivery_contract(microbatch_id, reviewer, render)
        destination = group_delivery_path(delivery_out, microbatch_id, batch_id, reviewer)
        if not destination.is_dir():
            raise ValueError("Missing post-incident single-group delivery")
        group_delivery_leak_check(destination, render, contract, [row["v7_render"] for row in by_role[reviewer]])
        controller_row = next(row for row in rows if row["batch_id"] == batch_id and row["reviewer_role"] == reviewer)
        checks.append({
            "batch_id": batch_id,
            "controller_row_sha256": canonical_sha(controller_row),
            "delivery_v7_render_sha256": sha_bytes(pretty_bytes(render)),
            "microbatch_id": microbatch_id,
            "no_leak_check": "PASS_NO_PEER_PROMPT_BATCH_ID_OR_CANDIDATE_TOKEN",
            "reviewer_role": reviewer,
            "status": "PASS_PHASE5_POST_INCIDENT_SINGLE_GROUP_AB_DELIVERY_VERIFIED",
        })
    return checks


def materialise_post_incident_group_delivery(
    out: Path,
    delivery_out: Path,
    microbatch_id: str,
    batch_id: str,
) -> None:
    """Materialise both A/B isolated deliveries atomically at the group boundary."""
    materialise_or_verify_canonical_v7_renders(out, microbatch_id)
    rows, by_role, record = prepare_post_incident_group_delivery_controller(out, delivery_out, microbatch_id)
    if batch_id not in record["batch_ids"]:
        raise ValueError("Batch is not a member of the frozen post-incident microbatch")
    destinations = {role: group_delivery_path(delivery_out, microbatch_id, batch_id, role) for role in ROLES}
    if any(destination.exists() for destination in destinations.values()):
        raise ValueError("Refusing to overwrite an extracted post-incident single-group A/B delivery")
    for reviewer, destination in destinations.items():
        render = next(row["v7_render"] for row in by_role[reviewer] if row["v7_render"]["batch_id"] == batch_id)
        contract = post_incident_group_delivery_contract(microbatch_id, reviewer, render)
        destination.mkdir(parents=True)
        (destination / "v7_render.json").write_bytes(pretty_bytes(render))
        (destination / "single_group_output_contract.json").write_bytes(pretty_bytes(contract))
        group_delivery_leak_check(destination, render, contract, [row["v7_render"] for row in by_role[reviewer]])
    checks = post_incident_group_delivery_checks(out, delivery_out, microbatch_id, batch_id)
    print(json.dumps({"batch_id": batch_id, "checks": len(checks), "microbatch_id": microbatch_id, "output": str(delivery_out.resolve()), "status": "PASS_PHASE5_POST_INCIDENT_SINGLE_GROUP_AB_DELIVERY_MATERIALISED"}, sort_keys=True))


def verify_post_incident_group_delivery(
    out: Path,
    delivery_out: Path,
    microbatch_id: str,
    batch_id: str,
) -> None:
    checks = post_incident_group_delivery_checks(out, delivery_out, microbatch_id, batch_id)
    print(json.dumps({"batch_id": batch_id, "checks": checks, "microbatch_id": microbatch_id, "status": "PASS_PHASE5_POST_INCIDENT_SINGLE_GROUP_AB_DELIVERY_VERIFIED"}, sort_keys=True))


def preflight_post_incident_microbatch_delivery(out: Path, delivery_out: Path, microbatch_id: str) -> None:
    """Freeze a structural-only, no-outcomes preflight before isolated review starts."""
    rows, _by_role, record = verify_post_incident_group_delivery_controller(out, delivery_out, microbatch_id)
    report_path = delivery_out.resolve() / "preflight" / microbatch_id / "phase5_post_incident_single_group_preflight.json"
    if report_path.exists():
        raise ValueError(f"Refusing to overwrite immutable post-incident preflight: {report_path}")
    checks: list[dict[str, Any]] = []
    for batch_id in record["batch_ids"]:
        checks.extend(post_incident_group_delivery_checks(out, delivery_out, microbatch_id, batch_id))
    report = {
        "claim_boundary": "Structural transport preflight only. It verifies frozen allocation membership, exact V7 render bytes, isolated A/B single-group contracts, controller binding and sibling-leak exclusion. It does not read reviewer/coordinator returns, infer adequacy, create an acceptable set, open a token join, or report a retrieval result.",
        "controller_manifest": {
            "path": relative(post_incident_group_delivery_controller_path(delivery_out, microbatch_id)),
            "rows": len(rows),
            "sha256": sha(post_incident_group_delivery_controller_path(delivery_out, microbatch_id)),
        },
        "frozen_phase5_allocation": {
            "microbatch_id": microbatch_id,
            "record_sha256": canonical_sha(record),
            "transition_summary_sha256": sha(out.resolve() / "transition_summary.json"),
        },
        "checks": checks,
        "schema_version": POST_INCIDENT_GROUP_DELIVERY_SCHEMA,
        "status": "PASS_PHASE5_POST_INCIDENT_SINGLE_GROUP_MICROBATCH_PREFLIGHT",
    }
    report_path.parent.mkdir(parents=True)
    report_path.write_bytes(pretty_bytes(report))
    print(json.dumps({"checks": len(checks), "microbatch_id": microbatch_id, "output": str(report_path), "status": report["status"]}, sort_keys=True))


def verify_frozen_allocation_hashes(out: Path) -> dict[str, Any]:
    summary_path = out.resolve() / "transition_summary.json"
    if not summary_path.is_file():
        raise ValueError("Missing Phase-5 transition summary")
    summary = read_json(summary_path)
    if summary.get("status") != PHASE5_STATUS or not isinstance(summary.get("outputs"), dict):
        raise ValueError("Phase-5 allocation summary drift")
    expected = {
        "controller_group_transition_list.jsonl",
        "controller_unstarted_microbatch_records.jsonl",
        "sealed_reviewer_A_envelope.jsonl",
        "sealed_reviewer_B_envelope.jsonl",
        "sealed_reviewer_envelope_hashes.json",
    }
    if set(summary["outputs"]) != expected:
        raise ValueError("Phase-5 frozen allocation output membership drift")
    for name, expected_sha in summary["outputs"].items():
        path = out / name
        if not path.is_file() or sha(path) != expected_sha:
            raise ValueError(f"Phase-5 frozen allocation output hash drift: {name}")
    return summary


def label_opaque_return_checks(protocol: Any, batch_id: str, reviewer: str, render: dict[str, Any]) -> dict[str, str]:
    """Validate return shape and anchors without accessing adequacy-label values."""
    return_path = protocol.RETURN_ROOT / f"reviewer_{reviewer}" / f"{batch_id}.json"
    if not return_path.is_file():
        return {"batch_id": batch_id, "reviewer": reviewer, "status": "RETURN_NOT_PRESENT"}
    value = read_json(return_path)
    if set(value) != protocol.RETURN_TOP_LEVEL or value.get("reviewer_blind_id") != reviewer or value.get("batch_id") != batch_id:
        raise ValueError("V7 label-opaque return top-level schema drift")
    if value.get("batch_input_sha256") != render["batch_input_sha256"] or value.get("reviewer_instruction_sha256") != render["reviewer_instruction_sha256"]:
        raise ValueError("V7 label-opaque return render binding drift")
    expected_sources = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in render["packet"]["candidates"]}
    assessments = value.get("assessments")
    if not isinstance(assessments, list) or len(assessments) != len(expected_sources):
        raise ValueError("V7 label-opaque return assessment cardinality drift")
    seen: set[str] = set()
    for assessment in assessments:
        # Deliberately inspect keys, token identity and source anchor only.  No
        # adequacy value is accessed, copied, validated or reported here.
        if not isinstance(assessment, dict) or set(assessment) != protocol.ASSESSMENT_FIELDS:
            raise ValueError("V7 label-opaque return assessment schema drift")
        token = assessment.get("candidate_token")
        anchor = assessment.get("source_anchor")
        if token not in expected_sources or token in seen or not isinstance(anchor, str) or not protocol.valid_anchor(anchor, expected_sources[token]):
            raise ValueError("V7 label-opaque return candidate or source-anchor drift")
        seen.add(token)
    if seen != set(expected_sources):
        raise ValueError("V7 label-opaque return token membership drift")
    return {"batch_id": batch_id, "reviewer": reviewer, "status": "RETURN_LABEL_OPAQUE_SCHEMA_AND_SOURCE_ANCHOR_PASS"}


def structural_qa(out: Path, report_dir: Path, validate_returns: bool) -> None:
    """Report structural checks for the first three frozen microbatches only."""
    out = out.resolve()
    summary = verify_frozen_allocation_hashes(out)
    verify(out)
    protocol = load_v7_protocol()
    protocol.verify_execution()
    microbatch_ids = [f"RQ2B-P5-MB-{ordinal:04d}" for ordinal in range(1, 4)]
    report_rows: list[dict[str, Any]] = []
    label_opaque_rows: list[dict[str, str]] = []
    for microbatch_id in microbatch_ids:
        by_role, record = verify_canonical_v7_renders(out, microbatch_id)
        if len(record["batch_ids"]) != record["group_count"] or len(record["batch_ids"]) > MAX_GROUPS:
            raise ValueError("Phase-5 structural allocation cardinality drift")
        for role in ROLES:
            verify_delivery(out, microbatch_id, role)
            for row in by_role[role]:
                render = row["v7_render"]
                if set(render) != protocol.RENDER_TOP_LEVEL or protocol.keys_deep(render) & protocol.FORBIDDEN_KEYS:
                    raise ValueError("Phase-5 structural reviewer identity or leakage drift")
                batch_id = render.get("batch_id")
                if row["reviewer_role"] != role or batch_id not in record["batch_ids"] or render.get("reviewer_blind_id") != role:
                    raise ValueError("Phase-5 structural reviewer identity drift")
                report_rows.append({
                    "batch_id": batch_id,
                    "canonical_v7_render_bytes": len(pretty_bytes(render)),
                    "canonical_v7_render_sha256": sha_bytes(pretty_bytes(render)),
                    "microbatch_id": microbatch_id,
                    "reviewer_role": role,
                    "status": "PASS_ALLOCATION_CANONICAL_BINDING_TRANSPORT_IDENTITY_NO_LEAKAGE",
                })
                if validate_returns:
                    label_opaque_rows.append(label_opaque_return_checks(protocol, batch_id, role, render))
    report = {
        "allocation_summary_sha256": sha(out / "transition_summary.json"),
        "claim_boundary": "Structural QA checks allocation, canonical V7 render binding, delivery transport bytes/hashes, reviewer identity and forbidden-key leakage. Optional return checking is label-opaque: it checks only schema shape, render binding, token identity and source anchors, never adequacy-label values.",
        "microbatch_ids": microbatch_ids,
        "return_validation_mode": "NOT_REQUESTED" if not validate_returns else "LABEL_OPAQUE_SCHEMA_AND_SOURCE_ANCHOR_ONLY",
        "rows": report_rows,
        "return_rows": label_opaque_rows,
        "status": "PASS_PHASE5_STRUCTURAL_QA_M0001_M0003",
    }
    destination = report_dir.resolve()
    if destination.exists():
        raise ValueError(f"Refusing to overwrite immutable Phase-5 structural QA report: {destination}")
    destination.mkdir(parents=True)
    report_path = destination / "phase5_structural_qa_M0001_M0003.json"
    report_path.write_bytes(pretty_bytes(report))
    print(json.dumps({"output": str(report_path), "rows": len(report_rows), "status": report["status"]}, sort_keys=True))


def freeze(out: Path) -> None:
    out = out.resolve()
    if out.exists():
        raise ValueError(f"Refusing to overwrite immutable Phase-5 allocation: {out}")
    files, transition = output_payload(reconstruct_groups())
    write_payload(out, files)
    print(json.dumps({"counts": transition["counts"], "output_dir": str(out), "status": transition["status"]}, sort_keys=True))


def verify(out: Path) -> None:
    out = out.resolve()
    if not out.is_dir():
        raise ValueError(f"Missing Phase-5 allocation directory: {out}")
    summary = verify_frozen_allocation_hashes(out)
    required_names = set(summary["outputs"]) | {"transition_summary.json"}
    actual_names = {path.name for path in out.iterdir() if path.is_file()}
    if actual_names != required_names:
        raise ValueError("Phase-5 output membership drift")
    implementation = summary.get("implementation")
    if not isinstance(implementation, dict) or implementation.get("path") != relative(Path(__file__)) or not isinstance(implementation.get("sha256"), str) or len(implementation["sha256"]) != 64:
        raise ValueError("Phase-5 frozen materialiser identity drift")
    frozen_inputs = summary.get("frozen_inputs")
    expected_input_names = set(required_input_hashes())
    if not isinstance(frozen_inputs, dict) or set(frozen_inputs) != expected_input_names:
        raise ValueError("Phase-5 frozen-input membership drift")
    for path_text, expected_sha in frozen_inputs.items():
        path = (WORKSPACE / path_text).resolve()
        if path == Path(__file__).resolve():
            # The allocation retains the identity of the materialiser that
            # created it; delivery-only code may be safely appended later.
            continue
        if not path.is_file() or sha(path) != expected_sha:
            raise ValueError(f"Phase-5 frozen-input hash drift: {path_text}")
    group_rows = read_jsonl(out / "controller_group_transition_list.jsonl")
    if len(group_rows) != GROUP_COUNT or len({row.get("batch_id") for row in group_rows}) != GROUP_COUNT:
        raise ValueError("Phase-5 group-list membership drift")
    unstarted_ids = {row["batch_id"] for row in group_rows if row.get("transition_status") == "UNSTARTED_NO_CANONICAL_V7_RENDER_EXISTS"}
    records = read_jsonl(out / "controller_unstarted_microbatch_records.jsonl")
    if len({row.get("microbatch_id") for row in records}) != len(records):
        raise ValueError("Phase-5 microbatch-id uniqueness drift")
    allocated_ids: list[str] = []
    for record in records:
        over_limit = any(value > MAX_BYTES for value in record["expected_render_bytes"].values())
        expected_exception = OVERSIZE_SINGLETON_EXCEPTION if record["oversize_singleton"] else None
        if record["group_count"] > MAX_GROUPS:
            raise ValueError("Phase-5 microbatch limit drift")
        if over_limit and not (record["oversize_singleton"] and record["group_count"] == 1):
            raise ValueError("Phase-5 non-singleton byte ceiling conflict")
        if record["oversize_singleton"] != over_limit or record["amendment_exception"] != expected_exception:
            raise ValueError("Phase-5 oversize-singleton amendment drift")
        families = [(value["lane_id"], value["reporting_group"]) for value in record["controller_family_keys"]]
        if len(families) != len(set(families)):
            raise ValueError("Phase-5 family conflict")
        source_sets = [set(values) for values in record["controller_source_sha256_sets"]]
        if any(source_sets[left] & source_sets[right] for left in range(len(source_sets)) for right in range(left + 1, len(source_sets))):
            raise ValueError("Phase-5 source conflict")
        if len(record["batch_ids"]) != record["group_count"]:
            raise ValueError("Phase-5 microbatch batch-id cardinality drift")
        allocated_ids.extend(record["batch_ids"])
    if len(allocated_ids) != len(set(allocated_ids)) or set(allocated_ids) != unstarted_ids:
        raise ValueError("Phase-5 allocation membership drift")
    for role in ROLES:
        envelope_rows = read_jsonl(out / f"sealed_reviewer_{role}_envelope.jsonl")
        by_microbatch: dict[str, list[str]] = {}
        for envelope in envelope_rows:
            if set(envelope) != {"reviewer_role", "microbatch_id", "v7_render"} or envelope["reviewer_role"] != role:
                raise ValueError("Phase-5 reviewer-facing envelope field drift")
            by_microbatch.setdefault(envelope["microbatch_id"], []).append(envelope["v7_render"].get("batch_id"))
        if {batch_id for batch_ids in by_microbatch.values() for batch_id in batch_ids} != unstarted_ids:
            raise ValueError("Phase-5 reviewer-envelope membership drift")
        for record in records:
            if by_microbatch.get(record["microbatch_id"]) != record["batch_ids"]:
                raise ValueError("Phase-5 reviewer-envelope microbatch ordering drift")
    counts = summary.get("counts", {})
    if counts.get("v7_groups") != GROUP_COUNT or counts.get("unstarted") != len(unstarted_ids) or counts.get("microbatches") != len(records):
        raise ValueError("Phase-5 transition count drift")
    print(json.dumps({"counts": counts, "output_dir": str(out), "status": "PASS_PHASE5_PARALLEL_MICROBATCH_ALLOCATION_VERIFIED"}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("freeze", "verify"):
        subparsers.add_parser(command).add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    for command in ("extract", "verify-delivery"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
        subparser.add_argument("--microbatch-id", required=True)
        subparser.add_argument("--reviewer", choices=ROLES, required=True)
    for command in ("extract-group-delivery", "verify-group-delivery"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
        subparser.add_argument("--repair-dir", type=Path, default=DEFAULT_GROUP_REPAIR_OUT)
        subparser.add_argument("--microbatch-id", required=True)
        subparser.add_argument("--batch-id", required=True)
        subparser.add_argument("--reviewer", choices=ROLES, required=True)
    for command in ("materialise-group-delivery-ab", "verify-group-delivery-ab"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
        subparser.add_argument("--delivery-dir", type=Path, default=DEFAULT_POST_INCIDENT_GROUP_DELIVERY_OUT)
        subparser.add_argument("--microbatch-id", required=True)
        subparser.add_argument("--batch-id", required=True)
    post_incident_preflight = subparsers.add_parser("preflight-group-delivery-ab")
    post_incident_preflight.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    post_incident_preflight.add_argument("--delivery-dir", type=Path, default=DEFAULT_POST_INCIDENT_GROUP_DELIVERY_OUT)
    post_incident_preflight.add_argument("--microbatch-id", required=True)
    repair_qa = subparsers.add_parser("structural-group-delivery-repair")
    repair_qa.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    repair_qa.add_argument("--repair-dir", type=Path, default=DEFAULT_GROUP_REPAIR_OUT)
    repair_qa.add_argument("--microbatch-id", default=GROUP_DELIVERY_TARGET_MICROBATCH)
    qa = subparsers.add_parser("structural-qa")
    qa.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    qa.add_argument("--report-dir", type=Path, default=DEFAULT_OUT / "structural_qa_M0001_M0003_v2")
    qa.add_argument("--validate-returns", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "freeze":
            freeze(args.output_dir)
        elif args.command == "verify":
            verify(args.output_dir)
        elif args.command == "extract":
            extract(args.output_dir, args.microbatch_id, args.reviewer)
        elif args.command == "structural-qa":
            structural_qa(args.output_dir, args.report_dir, args.validate_returns)
        elif args.command == "extract-group-delivery":
            extract_group_delivery(args.output_dir, args.repair_dir, args.microbatch_id, args.batch_id, args.reviewer)
        elif args.command == "verify-group-delivery":
            verify_group_delivery(args.output_dir, args.repair_dir, args.microbatch_id, args.batch_id, args.reviewer)
        elif args.command == "structural-group-delivery-repair":
            structural_group_delivery_repair(args.output_dir, args.repair_dir, args.microbatch_id)
        elif args.command == "materialise-group-delivery-ab":
            materialise_post_incident_group_delivery(args.output_dir, args.delivery_dir, args.microbatch_id, args.batch_id)
        elif args.command == "verify-group-delivery-ab":
            verify_post_incident_group_delivery(args.output_dir, args.delivery_dir, args.microbatch_id, args.batch_id)
        elif args.command == "preflight-group-delivery-ab":
            preflight_post_incident_microbatch_delivery(args.output_dir, args.delivery_dir, args.microbatch_id)
        else:
            verify_delivery(args.output_dir, args.microbatch_id, args.reviewer)
    except ValueError as exc:
        raise SystemExit(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
