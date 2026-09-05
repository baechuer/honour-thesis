#!/usr/bin/env python3
"""Fail-closed Master Phase-4 audit-input-freeze controller.

This controller is deliberately a preparation gate, not a selector or an
experiment runner.  It will write a *blocked prerequisite report* when a
fresh, explicit Master Phase-3 closure is absent or is not in the declared
PASS state.  In that state it neither writes an audit-input package nor reads
source bodies, prompts, labels, retrieval output, embeddings, provider output,
or historical acceptable-set outcomes.

Once a future Phase-3 closure exists, this controller rebinds the proposed
freeze dependencies and writes only a readiness record unless a separately
implemented, hash-bound proposal/packet materialiser is supplied.  This avoids
misrepresenting a dependency inventory as a frozen audit input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
NC = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
MANIFESTS = NC / "manifests"
SOP = NC / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
READINESS = MANIFESTS / "rq2b_nc_master_phase4_freeze_readiness_2026-09-06_v1/report.md"
PREFLIGHT = MANIFESTS / "rq2b_nc_master_phase3_preflight_2026-09-06_v1"
DEFAULT_CLOSURE = MANIFESTS / "rq2b_nc_master_phase3_closure_2026-09-06_v1/summary.json"
DEFAULT_OUT = MANIFESTS / "rq2b_nc_master_phase4_freeze_staging_2026-09-06_v1"
EXPECTED_PHASE3_STATUS = "PASS_RQ2B_NC_MASTER_PHASE3_CLOSURE_NO_EXPERIMENT"
COMPOSITE_MANIFEST = MANIFESTS / "rq2b_nc_master_phase4_current_nc_prompt_composite_2026-09-06_v1/manifest.json"
COMPOSITE_AUDIT = MANIFESTS / "rq2b_nc_master_phase4_current_nc_prompt_composite_audit_2026-09-06_v3/report.json"
EXPECTED_COMPOSITE_STATUS = "PASS_CURRENT_NC_PROMPT_COMPOSITE_BINDING_NO_FREEZE_NO_EXPERIMENT"
EXPECTED_COMPOSITE_AUDIT_STATUS = "PASS_CURRENT_NC_PROMPT_COMPOSITE_MECHANICAL_AUDIT_NO_FREEZE_NO_EXPERIMENT"

# These keys are deliberately requirements on the *future explicit closure*,
# rather than inferred from historical v3/v7 packages.  The old package is a
# protocol reference only, never a current count, token map, or result.
REQUIRED_CLOSURE_INPUTS = (
    "candidate_source_union_3813",
    "parent_prompt_manifest_381",
    "nc_triad_manifest_49",
    "nc_prompt_manifest",
    "source_provenance_manifest",
    "candidate_proposal_implementation",
    "candidate_proposal_contract",
    "review_packet_schema",
    "analysis_contract",
)
PARENT_381 = ROOT / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
HISTORICAL_NC_PROMPTS = MANIFESTS / "rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2/nc_prompt_manifest.jsonl"
PROPOSAL_IMPLEMENTATION = ROOT / "skill_benchmark/scripts/materialize_rq2b_nc_phase4_option1_k6_audit_input_2026_09_05.py"
PROPOSAL_CONTRACT = NC / "review/WHOLE_LIBRARY_POOLED_DISCOVERY_PROTOCOL_2026-08-31.json"
PACKET_SCHEMA_REFERENCE = MANIFESTS / "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery/summary.json"
ANALYSIS_CONTRACT_REFERENCE = NC / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
MISSING_PROMPT_BINDING = MANIFESTS / "rq2b_nc_master_phase4_missing_nc_prompt_binding_2026-09-06_v1"
MISSING_PROMPT_BINDING_MANIFEST = MISSING_PROMPT_BINDING / "manifest.json"
MISSING_PROMPT_BINDING_ROWS = MISSING_PROMPT_BINDING / "prompt_binding_rows.jsonl"
EXPECTED_MISSING_PROMPT_BINDING_STATUS = "PASS_CURRENT_NC_PROMPT_BINDING_COMPLETE"
COMPOSITE_ROWS = COMPOSITE_MANIFEST.parent / "composite_prompt_binding_rows.jsonl"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def input_record(path: Path) -> dict[str, Any]:
    record: dict[str, Any] = {"path": rel(path), "exists": path.is_file()}
    if path.is_file():
        record["sha256"] = digest(path)
    return record


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing:{rel(path)}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def validate_missing_prompt_binding(triads: dict[tuple[str, str], set[str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Accept a supplemental nine-prompt binding only if it is complete.

    Partial PASS rows are never promoted into a Phase-4 NC prompt manifest:
    every affected triad needs all three fresh current bindings, cue-safe
    authoring and target-blind local approval before the historical 46 groups
    can be unioned with it.
    """
    defects: list[dict[str, Any]] = []
    if not MISSING_PROMPT_BINDING_MANIFEST.is_file() or not MISSING_PROMPT_BINDING_ROWS.is_file():
        return [{"check": "missing_nc_prompt_binding", "reason": "binding_package_absent"}], []
    try:
        manifest = json.loads(MISSING_PROMPT_BINDING_MANIFEST.read_text(encoding="utf-8"))
        rows = read_jsonl(MISSING_PROMPT_BINDING_ROWS)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [{"check": "missing_nc_prompt_binding", "reason": f"unreadable:{error.__class__.__name__}"}], []
    if manifest.get("status") != EXPECTED_MISSING_PROMPT_BINDING_STATUS:
        defects.append({"check": "missing_nc_prompt_binding_status", "reason": f"expected:{EXPECTED_MISSING_PROMPT_BINDING_STATUS};observed:{manifest.get('status')!r}"})
    covered: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row.get("batch"), row.get("family_token"))
        if key not in triads:
            defects.append({"check": "missing_nc_prompt_binding_row", "reason": "unknown_terminal_family"})
            continue
        visible = row.get("source_visible_candidate_set")
        target = row.get("target_canonical_source_sha256")
        final = row.get("final_local_disposition")
        valid_visible = isinstance(visible, list) and {
            item.get("canonical_source_sha256") for item in visible if isinstance(item, dict)
        } == triads[key] and all(
            isinstance(item, dict)
            and item.get("source_byte_replay") == "PASS_SHA256_MATCH"
            and str(item.get("provenance_preflight_status", "")).startswith("PASS_")
            and item.get("source_path_sha256") == item.get("canonical_source_sha256")
            for item in visible
        )
        valid_prompt = isinstance(row.get("author_prompt"), str) and isinstance(row.get("author_prompt_sha256"), str) and digest_text(row["author_prompt"]) == row["author_prompt_sha256"]
        valid_local = isinstance(final, dict) and final.get("prompt_integrity") == "CUE_SAFE" and final.get("intended_target_blind_decision") == "MOST_SUITABLE"
        valid_phase3 = isinstance(row.get("phase3_linkage"), dict) and row["phase3_linkage"].get("prompt_cue_screen") is not None
        if not (target in triads[key] and valid_visible and valid_prompt and valid_local and valid_phase3 and row.get("binding_status") == "PASS_CURRENT_NC_PROMPT_BINDING"):
            defects.append({"check": "missing_nc_prompt_binding_row", "reason": "incomplete_fresh_authoring_cue_target_blind_or_provenance_binding"})
        covered[key].append(row)
    needed = {key for key, sources in triads.items() if len(sources) == 3 and key not in {
        ("B013", "F-59796e6dce627ba4"), ("B015", "F-1f956c52aa7f0c9d"), ("B015", "F-98199f9119042f1a")
    }}
    # The supplemental binder must cover exactly the documented three gaps,
    # with a unique prompt and target for each member.
    supplemental_keys = set(covered)
    expected_keys = set(triads) - needed
    if supplemental_keys != expected_keys:
        defects.append({"check": "missing_nc_prompt_binding_coverage", "reason": "supplemental_family_set_drift"})
    for key in expected_keys:
        group = covered.get(key, [])
        if len(group) != 3 or len({row.get("canonical_prompt_id") for row in group}) != 3 or {row.get("target_canonical_source_sha256") for row in group} != triads[key]:
            defects.append({"check": "missing_nc_prompt_binding_coverage", "reason": f"incomplete_triad:{key[0]}/{key[1]}"})
    return defects, rows


def validate_current_composite_binding(triads: dict[tuple[str, str], set[str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate the fresh nine-row changed-family replacement.

    The superseded missing-binder package is historical evidence only.  This
    validator consumes the current composite manifest/audit and replays every
    member source path, prompt digest, phase-3 linkage, and local target-blind
    disposition before allowing the three changed triads to join the 46
    inherited triads.
    """
    defects: list[dict[str, Any]] = []
    if not COMPOSITE_ROWS.is_file():
        return [{"check": "current_nc_prompt_composite_rows", "reason": "absent"}], []
    try:
        rows = read_jsonl(COMPOSITE_ROWS)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [{"check": "current_nc_prompt_composite_rows", "reason": f"unreadable:{error.__class__.__name__}"}], []
    expected = {
        ("B013", "F-59796e6dce627ba4"),
        ("B015", "F-1f956c52aa7f0c9d"),
        ("B015", "F-98199f9119042f1a"),
    }
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row.get("batch"), row.get("family_token"))
        grouped[key].append(row)
        visible = row.get("source_visible_candidate_set")
        if not isinstance(visible, list) or {x.get("canonical_source_sha256") for x in visible if isinstance(x, dict)} != triads.get(key, set()):
            defects.append({"check": "current_nc_prompt_composite_row", "reason": f"triad_visible_set:{key}"})
        for item in visible if isinstance(visible, list) else []:
            if not isinstance(item, dict) or item.get("source_byte_replay") != "PASS_SHA256_MATCH" or not str(item.get("provenance_preflight_status", "")).startswith("PASS_"):
                defects.append({"check": "current_nc_prompt_composite_row", "reason": f"source_replay_or_provenance:{key}"})
            elif not replay_source_path_digest(item.get("canonical_source_sha256"), item.get("source_path")):
                defects.append({"check": "current_nc_prompt_composite_row", "reason": f"source_byte_replay:{key}"})
        prompt = row.get("author_prompt")
        if not isinstance(prompt, str) or digest_text(prompt) != row.get("author_prompt_sha256"):
            defects.append({"check": "current_nc_prompt_composite_row", "reason": f"prompt_digest:{key}"})
        final = row.get("final_local_disposition")
        linkage = row.get("phase3_linkage")
        valid_target_blind = isinstance(final, dict) and (final.get("intended_target_blind_decision") == "MOST_SUITABLE" or final.get("review_route") == "REMEDIATION_A_B_COORDINATOR_FINALIZED")
        if row.get("binding_status") != "PASS_CURRENT_NC_PROMPT_BINDING" or row.get("composite_binding_status") != "PASS_CURRENT_NC_PROMPT_COMPOSITE" or not isinstance(final, dict) or final.get("prompt_integrity") != "CUE_SAFE" or not valid_target_blind or not isinstance(linkage, dict) or linkage.get("prompt_cue_screen") is None:
            defects.append({"check": "current_nc_prompt_composite_row", "reason": f"fresh_evidence_or_phase3_linkage:{key}"})
    if set(grouped) != expected or len(rows) != 9 or any(len(grouped.get(k, [])) != 3 for k in expected):
        defects.append({"check": "current_nc_prompt_composite_coverage", "reason": "expected_three_triads_nine_rows"})
    for key in expected:
        group = grouped.get(key, [])
        targets = {r.get("author_target_source_sha256", r.get("target_source_sha256")) for r in group}
        if targets != triads.get(key, set()) or len({r.get("canonical_prompt_id") for r in group}) != 3:
            defects.append({"check": "current_nc_prompt_composite_coverage", "reason": f"target_or_prompt_identity:{key}"})
    return defects, rows


def replay_source_path_digest(source: Any, stored_path: Any) -> bool:
    if not isinstance(source, str) or not isinstance(stored_path, str):
        return False
    candidates = [ROOT / stored_path, ROOT / "skill_benchmark" / stored_path]
    existing = [p for p in candidates if p.is_file()]
    return bool(existing) and all(digest(p) == source for p in existing)


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def provenance_paths(row: dict[str, Any]) -> list[str]:
    """Return declared, hash-bound source paths without repository searching."""
    paths: set[str] = set()
    historical = row.get("historical_base_candidate")
    if isinstance(historical, dict):
        binding = historical.get("provenance_binding")
        if isinstance(binding, dict) and isinstance(binding.get("source_path"), str):
            paths.add(binding["source_path"])
        for name in ("rq1_records", "rq1_exact_reuse_records", "v3_identity_records"):
            for item in historical.get(name, []):
                if isinstance(item, dict) and isinstance(item.get("source_path"), str):
                    paths.add(item["source_path"])
    for origin in row.get("local_nc_origin_records", []):
        if not isinstance(origin, dict):
            continue
        for path in origin.get("source_paths", []):
            if isinstance(path, str):
                paths.add(path)
        record = origin.get("provenance_record")
        if isinstance(record, dict):
            for path in record.get("source_paths", []):
                if isinstance(path, str):
                    paths.add(path)
    return sorted(paths)


def replay_source_provenance(source: str, row: dict[str, Any]) -> bool:
    paths = provenance_paths(row)
    if not paths:
        return False
    for stored in paths:
        candidate_paths = [ROOT / stored, ROOT / "skill_benchmark" / stored]
        existing = [path for path in candidate_paths if path.is_file()]
        if not existing or any(digest(path) != source for path in existing):
            return False
    return True


def parse_closure_inputs(summary: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Parse explicit closure bindings, while allowing a Phase-3-only closure.

    If a closure declares a Phase-4 input, every declaration must have an
    exact path and digest and is replayed before use.  A null/absent field is
    permitted because the current Phase-3 closure predates Phase-4 binding.
    """
    declared = summary.get("phase4_freeze_inputs")
    issues: list[dict[str, str]] = []
    if declared is None:
        return {}, []
    if not isinstance(declared, dict):
        return {}, [{"check": "phase4_freeze_inputs", "reason": "not_object"}]
    for key, value in declared.items():
        value = declared.get(key)
        if not isinstance(value, dict):
            issues.append({"check": key, "reason": "missing_or_not_object"})
            continue
        stored_path = value.get("path")
        stored_sha = value.get("sha256")
        if not isinstance(stored_path, str) or not stored_path:
            issues.append({"check": key, "reason": "missing_path"})
        if not isinstance(stored_sha, str) or len(stored_sha) != 64:
            issues.append({"check": key, "reason": "missing_sha256"})
    return declared, issues


def declared_path(value: dict[str, Any]) -> Path:
    stored = value["path"]
    path = Path(stored)
    return path if path.is_absolute() else ROOT / path


def replay_closure_declarations(declared: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    """Replay every closure-declared path/hash without searching or guessing."""
    rebound: dict[str, dict[str, Any]] = {}
    defects: list[dict[str, str]] = []
    for key, value in sorted(declared.items()):
        if not isinstance(value, dict) or not isinstance(value.get("path"), str) or not isinstance(value.get("sha256"), str):
            # parse_closure_inputs already reports malformed values; retain an
            # explicit fail-closed replay record in case it is called alone.
            defects.append({"check": key, "reason": "malformed_declaration"})
            continue
        path = declared_path(value)
        rebound[key] = input_record(path)
        if not path.is_file():
            defects.append({"check": key, "reason": "declared_path_absent"})
        elif digest(path) != value["sha256"]:
            defects.append({"check": key, "reason": "declared_sha256_drift"})
    return rebound, defects


def closure_state(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if not path.is_file():
        return None, [{"check": "master_phase3_closure", "reason": "absent"}]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return None, [{"check": "master_phase3_closure", "reason": f"unreadable:{error.__class__.__name__}"}]
    if payload.get("status") != EXPECTED_PHASE3_STATUS:
        return payload, [{"check": "master_phase3_closure_status", "reason": f"expected:{EXPECTED_PHASE3_STATUS};observed:{payload.get('status')!r}"}]
    _, issues = parse_closure_inputs(payload)
    return payload, issues


def blocked_report(closure: Path, defects: list[dict[str, str]]) -> dict[str, Any]:
    """A dependency-only report.  No future-freeze content is materialised."""
    return {
        "status": "BLOCKED_PREREQUISITE_PHASE3",
        "claim_boundary": (
            "Dependency preflight only. This is not an audit-input freeze, acceptable-set audit, "
            "retrieval run, embedding/provider call, selector outcome, metric, or thesis result."
        ),
        "freeze_not_materialised": True,
        "phase3_closure_required_status": EXPECTED_PHASE3_STATUS,
        "phase3_closure": input_record(closure),
        "blocking_defects": defects,
        "bound_preparation_references": {
            "controlling_sop": input_record(SOP),
            "phase4_readiness_plan": input_record(READINESS),
            "current_phase3_structural_preflight_summary": input_record(PREFLIGHT / "summary.json"),
            "current_candidate_source_union_3813": input_record(PREFLIGHT / "candidate_source_union.jsonl"),
            "current_terminal_nc_triad_sources_49": input_record(PREFLIGHT / "terminal_source_union.jsonl"),
            "parent_381_prompt_identity_manifest": input_record(PARENT_381),
        },
        "required_future_closure_input_keys": list(REQUIRED_CLOSURE_INPUTS),
        "required_freeze_contract": {
            "proposal_boundary": "outcome-blind, deterministic, hash-bound; no retrieval/provider/embedding outcomes",
            "k_rule": "exactly six opaque main-pool candidates per applicable prompt and at most two deterministic eligible tails per prompt group",
            "review_boundary": "source-visible reviewer packets and exact independent/coordinator return schemas; no labels before the freeze",
            "analysis_boundary": "freeze hypotheses, estimands, endpoints, strata, metrics, failure analysis, cost accounting, margins, rerank budget and bootstrap/statistical plan before outcomes",
        },
        "implementation": {
            "path": rel(Path(__file__).resolve()),
            "sha256": digest(Path(__file__).resolve()),
            "python": sys.version,
            "platform": platform.platform(),
        },
    }


def write_report(out: Path, report: dict[str, Any]) -> None:
    out.mkdir(parents=True)
    (out / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def phase4_input_validation(closure_payload: dict[str, Any], closure_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """Bind current input identities and identify absent current NC prompts.

    Historical prompt records can supply a current prompt only when their
    batch/family/target maps exactly to a current terminal triad.  Missing
    records are reported, never authored or inferred here.
    """
    required = {
        "controlling_sop": SOP,
        "phase3_closure": closure_path,
        "current_union_3813": PREFLIGHT / "candidate_source_union.jsonl",
        "current_terminal_nc_sources": PREFLIGHT / "terminal_source_union.jsonl",
        "parent_381_prompt_manifest": PARENT_381,
        "historical_nc_prompt_reference_only": HISTORICAL_NC_PROMPTS,
        "current_nc_prompt_composite_rows": COMPOSITE_ROWS,
        "candidate_proposal_implementation_reference_only": PROPOSAL_IMPLEMENTATION,
        "candidate_proposal_contract_reference_only": PROPOSAL_CONTRACT,
        "review_packet_schema_reference_only": PACKET_SCHEMA_REFERENCE,
        "analysis_contract_reference_only": ANALYSIS_CONTRACT_REFERENCE,
        "current_nc_prompt_composite_manifest": COMPOSITE_MANIFEST,
        "current_nc_prompt_composite_audit_v3": COMPOSITE_AUDIT,
    }
    bindings = {name: input_record(path) for name, path in required.items()}
    defects: list[dict[str, Any]] = [
        {"check": "required_input_exists", "input": name, "reason": "absent"}
        for name, record in bindings.items() if not record["exists"]
    ]
    if defects:
        return bindings, defects, []

    # The current composite and its fresh mechanical audit are an explicit
    # Phase-4 prerequisite.  Historical/blocked audits must never satisfy it.
    try:
        composite = json.loads(COMPOSITE_MANIFEST.read_text(encoding="utf-8"))
        composite_audit = json.loads(COMPOSITE_AUDIT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        defects.append({"check": "current_nc_prompt_composite_audit_v3", "reason": f"unreadable:{error.__class__.__name__}"})
        return bindings, defects, []
    if composite.get("status") != EXPECTED_COMPOSITE_STATUS:
        defects.append({"check": "current_nc_prompt_composite_manifest", "reason": f"unexpected_status:{composite.get('status')!r}"})
    if composite_audit.get("status") != EXPECTED_COMPOSITE_AUDIT_STATUS:
        defects.append({"check": "current_nc_prompt_composite_audit_v3", "reason": f"unexpected_status:{composite_audit.get('status')!r}"})
    declared_manifest_sha = composite_audit.get("inputs", {}).get("composite_manifest_sha256")
    observed_manifest_sha = digest(COMPOSITE_MANIFEST)
    if declared_manifest_sha != observed_manifest_sha:
        defects.append({"check": "current_nc_prompt_composite_audit_v3", "reason": "composite_manifest_sha256_mismatch", "expected": declared_manifest_sha, "observed": observed_manifest_sha})
    bindings["current_nc_prompt_composite_audit_v3_binding"] = {"path": rel(COMPOSITE_AUDIT), "sha256": digest(COMPOSITE_AUDIT), "status": composite_audit.get("status")}
    bindings["current_nc_prompt_composite_manifest_binding"] = {"path": rel(COMPOSITE_MANIFEST), "sha256": observed_manifest_sha, "status": composite.get("status")}
    if defects:
        return bindings, defects, []

    # Do not ignore a declaration simply because a controller also has a
    # conventional path.  Every declared binding is replayed and, for names
    # shared with this controller, must resolve to the same bytes.
    declared, declared_schema_defects = parse_closure_inputs(closure_payload)
    declared_rebound, declared_replay_defects = replay_closure_declarations(declared)
    bindings["phase3_declared_inputs"] = declared_rebound
    defects.extend(declared_schema_defects)
    defects.extend(declared_replay_defects)
    aliases = {
        "candidate_source_union_3813": "current_union_3813",
        "parent_prompt_manifest_381": "parent_381_prompt_manifest",
        "nc_triad_manifest_49": "current_terminal_nc_sources",
        "candidate_proposal_implementation": "candidate_proposal_implementation_reference_only",
        "candidate_proposal_contract": "candidate_proposal_contract_reference_only",
        "review_packet_schema": "review_packet_schema_reference_only",
        "analysis_contract": "analysis_contract_reference_only",
    }
    for declared_name, conventional_name in aliases.items():
        if declared_name not in declared:
            continue
        expected = bindings[conventional_name].get("sha256")
        observed = declared_rebound.get(declared_name, {}).get("sha256")
        if expected != observed:
            defects.append({"check": declared_name, "reason": f"declared_binding_does_not_match_current_{conventional_name}"})
    if defects:
        return bindings, defects, []

    union = read_jsonl(PREFLIGHT / "candidate_source_union.jsonl")
    terminal = read_jsonl(PREFLIGHT / "terminal_source_union.jsonl")
    parent = read_jsonl(PARENT_381)
    historical_prompts = read_jsonl(HISTORICAL_NC_PROMPTS)
    union_hashes = {row.get("canonical_source_sha256") for row in union}
    union_by_hash = {row.get("canonical_source_sha256"): row for row in union}
    if len(union) != 3813 or len(union_hashes) != 3813:
        defects.append({"check": "current_union_3813", "reason": "cardinality_or_duplicate_drift", "rows": len(union), "unique": len(union_hashes)})
    if len(parent) != 381 or len({row.get("prompt_id") for row in parent}) != 381:
        defects.append({"check": "parent_381_prompt_manifest", "reason": "cardinality_or_identity_drift", "rows": len(parent), "unique_prompt_ids": len({row.get("prompt_id") for row in parent})})

    triads: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in terminal:
        batch, family, source = row.get("batch"), row.get("family_token"), row.get("canonical_source_sha256")
        if not all(isinstance(value, str) and value for value in (batch, family, source)):
            defects.append({"check": "terminal_nc_source_schema", "reason": "missing_batch_family_or_source"})
            continue
        triads[(batch, family)].add(source)
    composite_defects, composite_rows = validate_current_composite_binding(triads)
    defects.extend(composite_defects)
    bindings["current_nc_prompt_composite_rows"] = {"path": rel(COMPOSITE_ROWS), "sha256": digest(COMPOSITE_ROWS), "rows": len(composite_rows)}
    bad_triads = sorted(f"{batch}/{family}" for (batch, family), sources in triads.items() if len(sources) != 3 or not sources <= union_hashes)
    if len(terminal) != 147 or len(triads) != 49 or bad_triads:
        defects.append({"check": "current_nc_49_triads", "reason": "cardinality_or_source_provenance_drift", "source_rows": len(terminal), "families": len(triads), "bad_families": bad_triads})
    provenance_failures = sorted(source for source in set().union(*triads.values()) if not isinstance(union_by_hash.get(source), dict) or not replay_source_provenance(source, union_by_hash[source]))
    if provenance_failures:
        defects.append({"check": "current_nc_49_triads", "reason": "source_byte_or_declared_provenance_replay_failure", "sources": provenance_failures})

    prompts_by_family: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in historical_prompts:
        key = (row.get("discovery_batch"), row.get("family_token"))
        target = row.get("intended_target_source_sha256")
        if key in triads and target in triads[key]:
            prompts_by_family[key].append(row)
    historical_current_prompt_rows = 0
    missing_prompt_families: list[dict[str, Any]] = []
    for key, sources in sorted(triads.items()):
        rows = prompts_by_family.get(key, [])
        prompt_ids = {row.get("audit_prompt_id") for row in rows}
        targets = {row.get("intended_target_source_sha256") for row in rows}
        if len(rows) != 3 or len(prompt_ids) != 3 or targets != sources:
            missing_prompt_families.append({
                "batch": key[0], "family_token": key[1],
                "expected_current_triads": sorted(sources),
                "historical_reference_prompt_rows_matching_current_targets": len(rows),
                "historical_reference_prompt_ids": sorted(value for value in prompt_ids if isinstance(value, str)),
                "reason": "No complete current three-prompt manifest is hash-bound to this terminal triad; do not infer or author prompts during Phase-4 freezing.",
            })
        else:
            malformed = [
                row for row in rows
                if not isinstance(row.get("prompt"), str)
                or digest_text(row["prompt"]) != row.get("prompt_text_sha256")
                or row.get("intended_target_source_sha256") not in sources
            ]
            if malformed:
                defects.append({"check": "historical_current_nc_prompt_reference", "reason": f"prompt_text_or_target_binding_drift:{key[0]}/{key[1]}"})
            else:
                historical_current_prompt_rows += len(rows)
    bindings["validated_historical_current_nc_prompt_rows"] = {"rows": historical_current_prompt_rows, "expected": 138}
    if historical_current_prompt_rows != 138:
        defects.append({"check": "historical_current_nc_prompt_reference", "reason": "expected_46_complete_triads_or_138_prompt_rows"})
    if missing_prompt_families:
        defects.append({"check": "current_nc_prompt_manifest_49", "reason": "incomplete_current_prompt_coverage", "families_missing_complete_prompts": len(missing_prompt_families), "expected_families": 49})
        binding_defects, binding_rows = validate_current_composite_binding(triads)
        # A PASS supplemental binding makes the three gaps eligible to be
        # unioned only after its own exact checks; the subsequent 147-row
        # freeze materialiser must still revalidate the combined manifest.
        if not binding_defects:
            missing_prompt_families = []
            defects = [defect for defect in defects if defect.get("check") != "current_nc_prompt_manifest_49"]
            bindings["current_nc_prompt_composite_rows_validated"] = {"rows": len(binding_rows), "sha256": digest(COMPOSITE_ROWS)}
        else:
            defects.extend(binding_defects)
    return bindings, defects, missing_prompt_families


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase3-closure", type=Path, default=DEFAULT_CLOSURE,
                        help="Fresh Master Phase-3 closure summary; historical closure is never accepted.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT,
                        help="New append-only staging directory for this invocation.")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    closure = args.phase3_closure.resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite append-only Phase-4 staging output: {out}")

    payload, defects = closure_state(closure)
    # This deliberately handles the current expected state.  It does not
    # partially create a freeze just because a closure file appears.
    if defects:
        report = blocked_report(closure, defects)
        write_report(out, report)
        print(json.dumps({"output_dir": str(out), "status": report["status"], "blockers": len(defects)}, sort_keys=True))
        return 0

    bindings, validation_defects, missing_prompts = phase4_input_validation(payload, closure)
    if validation_defects:
        report = {
            "status": "BLOCKED_PHASE4_CURRENT_INPUT_BINDING",
            "claim_boundary": "Phase-4 input-binding attempt only. No audit-input freeze, candidate proposal, opaque token, tail, reviewer packet, acceptable-set label, retrieval, embedding, provider output, metric or result was materialised.",
            "freeze_not_materialised": True,
            "phase3_closure": input_record(closure),
            "input_bindings": bindings,
            "hard_blockers": validation_defects,
            "counts": {"current_union_sources": 3813, "current_nc_terminal_source_rows": 147, "current_nc_terminal_triads": 49, "parent_prompts": 381, "nc_families_missing_complete_prompt_manifest": len(missing_prompts)},
            "no_selector_execution": True,
            "implementation": {"path": rel(Path(__file__).resolve()), "sha256": digest(Path(__file__).resolve()), "python": sys.version},
        }
        write_report(out, report)
        write_jsonl(out / "blocked_nc_prompt_families.jsonl", missing_prompts)
        print(json.dumps({"output_dir": str(out), "status": report["status"], "blockers": len(validation_defects)}, sort_keys=True))
        return 0

    # This branch is intentionally unreachable until the repository has a
    # complete current 49-family prompt manifest.  It is not permitted to
    # substitute historical prompts or execute the proposal implementation.
    report = {
        "status": "READY_FOR_SEPARATE_PHASE4_PACKET_FREEZE_NOT_EXECUTED",
        "claim_boundary": "All input identities bound, but no candidate proposal or packet construction was run by this controller.",
        "freeze_not_materialised": True,
        "phase3_closure": input_record(closure), "input_bindings": bindings,
        "implementation": {"path": rel(Path(__file__).resolve()), "sha256": digest(Path(__file__).resolve())},
    }
    write_report(out, report)
    print(json.dumps({"output_dir": str(out), "status": report["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
