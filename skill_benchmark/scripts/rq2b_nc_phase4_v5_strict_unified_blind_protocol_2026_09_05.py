#!/usr/bin/env python3
"""Materialise, render, validate, and reconcile the strict Phase-4 V7 blind audit.

V7 supersedes V6 before any V6 outcome enters the candidate library.  It keeps
the sealed V2 K=6+two-tail source allocation, but reviewers receive one uniform
eight-candidate source-native packet.  This script deliberately validates all
content bindings again at every boundary rather than trusting asserted hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
SOP = NC_ROOT / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
AUDIT = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"
EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
BATCH_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-v7-strict-unified-target-blind-batches-2026-09-05"
RETURN_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
COORD_RETURN_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-v7-strict-unified-coordinator-returns-2026-09-05"
RECON_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-v7-strict-unified-reconciliation-2026-09-05"

ALLOWED_ADEQUACY = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"}
RETURN_TOP_LEVEL = {
    "reviewer_blind_id",
    "batch_id",
    "blind_packet_id",
    "batch_input_sha256",
    "reviewer_instruction_sha256",
    "assessments",
    "reviewer_output_sha256",
}
ASSESSMENT_FIELDS = {
    "candidate_token",
    "adequacy",
    "source_anchor",
    "rationale",
    "missing_material_requirement_or_null",
}
COORDINATOR_RETURN_FIELDS = {
    "blind_packet_id",
    "candidate_token",
    "reviewer_a_return_sha256",
    "reviewer_b_return_sha256",
    "fresh_source_render_sha256",
    "coordinator_decision",
    "source_anchor",
    "rationale",
    "coordinator_output_sha256",
}
COORDINATOR_DECISIONS = {
    "CONFIRMED_FULLY_ACCEPTABLE",
    "CONFIRMED_PARTIALLY_ADEQUATE",
    "CONFIRMED_INADEQUATE",
    "CONFIRMED_UNCLEAR",
    "REOPEN_PACKET",
}
RENDER_TOP_LEVEL = {
    "schema_version",
    "batch_id",
    "reviewer_blind_id",
    "batch_input_sha256",
    "reviewer_instruction_sha256",
    "blindness_notice",
    "packet",
}
PACKET_FIELDS = {"blind_packet_id", "prompt", "candidates", "review_instruction"}
CANDIDATE_FIELDS = {"candidate_token", "source_full_skill"}
FORBIDDEN_KEYS = {
    "packet_kind", "tail_kind", "lane_id", "reporting_stratum", "reporting_group",
    "allocation_slot", "selection_channel", "rank_position", "channel_score",
    "canonical_source_sha256", "source_path", "target", "historical_gold",
    "local_roster", "prompt_sha256", "provenance", "license",
}
EXPECTED_V2_OUTPUTS = {
    "candidate_proposal_config.json",
    "main_blind_review_packets.jsonl",
    "opaque_token_join.jsonl",
    "prompt_k6_allocation_ledger.jsonl",
    "source_visible_review_pairs.jsonl",
    "tail_blind_review_packets.jsonl",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def canonical_without(value: dict[str, Any], key: str) -> str:
    copy = dict(value)
    copy.pop(key, None)
    return canonical_sha(copy)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def blind_packet_id(prompt_sha: str) -> str:
    digest = hashlib.sha256(f"rq2b-nc-phase4-v7-strict-unified\0{prompt_sha}".encode("utf-8")).hexdigest()
    return "P-" + digest[:18].upper()


def keys_deep(value: Any) -> set[str]:
    if isinstance(value, dict):
        result = set(value)
        for item in value.values():
            result |= keys_deep(item)
        return result
    if isinstance(value, list):
        result: set[str] = set()
        for item in value:
            result |= keys_deep(item)
        return result
    return set()


def verify_audit() -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    required = {
        "audit_summary": AUDIT / "summary.json",
        "main_packets": AUDIT / "main_blind_review_packets.jsonl",
        "tail_packets": AUDIT / "tail_blind_review_packets.jsonl",
        "allocation_ledger_sealed": AUDIT / "prompt_k6_allocation_ledger.jsonl",
        "opaque_token_join_sealed": AUDIT / "opaque_token_join.jsonl",
        "controlling_sop": SOP,
    }
    for name, path in required.items():
        if not path.is_file():
            raise ValueError(f"Missing V5 bound input {name}: {path}")
    summary = read_json(required["audit_summary"])
    if summary.get("status") != "PASS_PHASE4_K6_OUTCOME_BLIND_AUDIT_INPUT_MATERIALISED_PENDING_BLIND_REVIEWS":
        raise ValueError("V2 audit-input status drift")
    if set(summary.get("outputs", {})) != EXPECTED_V2_OUTPUTS:
        raise ValueError("V2 sealed audit-output keyset drift")
    for name, expected in summary["outputs"].items():
        path = AUDIT / name
        if not path.is_file() or sha(path) != expected:
            raise ValueError(f"V2 sealed audit hash drift: {name}")
    main = {row["packet_id"]: row for row in read_jsonl(required["main_packets"])}
    tail = {row["packet_id"]: row for row in read_jsonl(required["tail_packets"])}
    return summary, main, tail


def reviewer_instruction_and_schema() -> tuple[str, dict[str, str], dict[str, Any], dict[str, Any]]:
    instruction = (
        "Read the prompt and every complete source-visible candidate. Independently assess each candidate "
        "as FULLY_ACCEPTABLE, PARTIALLY_ADEQUATE, INADEQUATE or UNCLEAR under the frozen rubric. "
        "For source_anchor, provide exactly one literal section heading or short quoted phrase that appears "
        "in the source-visible skill; do not combine multiple anchors. Candidate-token order has no target, "
        "rank, route, main-pool or tail meaning. Do not select MOST_SUITABLE."
    )
    rubric = {
        "FULLY_ACCEPTABLE": "Independently satisfies every material input, transformation, constraint and requested output without an unrecorded component or material unsupported assumption.",
        "PARTIALLY_ADEQUATE": "Meaningful neighbouring route that misses a material requirement, output, constraint, executable step or dependency.",
        "INADEQUATE": "Not a plausible route for the central task/input/output boundary.",
        "UNCLEAR": "Source-visible material is insufficient or internally ambiguous; this blocks closure and is not a weak negative.",
    }
    return_schema = {
        "schema_version": "rq2b_nc_phase4_v7_strict_unified_blind_batch_return",
        "status": "FROZEN_BEFORE_REVIEW",
        "allowed_top_level": sorted(RETURN_TOP_LEVEL),
        "required_top_level": sorted(RETURN_TOP_LEVEL),
        "allowed_assessment_fields": sorted(ASSESSMENT_FIELDS),
        "assessment_required": sorted(ASSESSMENT_FIELDS),
        "reviewer_blind_id_values": ["A", "B"],
        "adequacy_values": sorted(ALLOWED_ADEQUACY),
        "rubric": rubric,
        "reviewer_instruction": instruction,
        "blindness_prohibitions": [
            "Read only the assigned rendered packet and this frozen schema.",
            "Do not inspect allocation, token join, target/local/historical reference, source path/provenance/licence, peer return, rank/lane/channel/main/tail metadata, retrieval/reranking/provider output or metric.",
            "Do not communicate with the other reviewer before submitting the sealed return.",
        ],
        "return_validation": [
            "Exactly eight assessments, one for each unified-packet token.",
            "Top-level and assessment objects have exactly the allowed fields; extra fields are rejected.",
            "source_anchor is one literal source-visible heading or short phrase and is mechanically located in the rendered source.",
            "FULLY_ACCEPTABLE requires a null missing_material_requirement_or_null; every other adequacy requires a non-empty string.",
            "reviewer_output_sha256 is SHA-256 of canonical JSON excluding that field (UTF-8, sorted keys, comma/colon separators).",
        ],
    }
    coordinator_schema = {
        "schema_version": "rq2b_nc_phase4_v7_strict_unified_blind_coordinator",
        "trigger": "A/B adequacy disagreement, either UNCLEAR, invalid return or missing return. Literal source anchors are independently mechanically located during return validation; different valid locators alone are logged but are not a decision conflict.",
        "input_rule": "Receive only the two validated returns and one fresh source-visible candidate. Do not inspect targets, main/tail assignment, rank, source path, provenance, historical/local reference or retrieval outcome.",
        "allowed_top_level": sorted(COORDINATOR_RETURN_FIELDS),
        "required_fields": sorted(COORDINATOR_RETURN_FIELDS),
        "decisions": sorted(COORDINATOR_DECISIONS),
        "validation": ["Output has exactly the allowed fields and binds the fresh source render plus SHA-256s of both already-validated independent returns.", "source_anchor is exactly one bounded literal source-visible heading or short phrase and is mechanically located.", "coordinator_output_sha256 is SHA-256 of canonical JSON excluding that field (UTF-8, sorted keys, comma/colon separators).", "Validated coordinator outputs are applied only by the finalise command; REOPEN_PACKET and CONFIRMED_UNCLEAR prevent library-level closure."],
    }
    return instruction, rubric, return_schema, coordinator_schema


def freeze(out: Path) -> None:
    if out.exists():
        raise ValueError(f"Refusing to overwrite V7 execution freeze: {out}")
    audit_summary, main_by_id, tail_by_id = verify_audit()
    main_by_prompt: dict[str, dict[str, Any]] = {}
    for row in main_by_id.values():
        prompt_sha = row["prompt_sha256"]
        if prompt_sha in main_by_prompt:
            raise ValueError("Duplicated V2 main prompt group")
        main_by_prompt[prompt_sha] = row
    tails_by_prompt: dict[str, list[dict[str, Any]]] = {}
    for row in tail_by_id.values():
        tails_by_prompt.setdefault(row["prompt_sha256"], []).append(row)
    if len(main_by_id) != 1226 or len(main_by_prompt) != 1226 or len(tail_by_id) != 2452 or set(tails_by_prompt) != set(main_by_prompt):
            raise ValueError("V7 sealed prompt cardinality drift")
    instruction, rubric, return_schema, coordinator_schema = reviewer_instruction_and_schema()
    instruction_sha = canonical_sha({"reviewer_instruction": instruction, "rubric": rubric})
    batches: list[dict[str, Any]] = []
    for ordinal, prompt_sha in enumerate(sorted(main_by_prompt), start=1):
        main = main_by_prompt[prompt_sha]
        tails = sorted(tails_by_prompt[prompt_sha], key=lambda row: row["packet_id"])
        if len(main["candidates"]) != 6 or len(tails) != 2 or any(len(row["candidates"]) != 1 for row in tails):
            raise ValueError("V7 K=6+two-tail cardinality drift")
        tokens = [candidate["candidate_token"] for candidate in main["candidates"]]
        tokens.extend(candidate["candidate_token"] for row in tails for candidate in row["candidates"])
        if len(tokens) != 8 or len(set(tokens)) != 8:
            raise ValueError("V7 unified token uniqueness drift")
        batches.append({
            "batch_id": f"RQ2B-P4-V7-U{ordinal:04d}",
            "blind_packet_id": blind_packet_id(prompt_sha),
            "prompt_group_unit": "one prompt with six sealed main candidates plus two sealed tails; all roles hidden from reviewers",
            "prompt_sha256": prompt_sha,
            "sealed_main_packet": {"packet_id": main["packet_id"], "packet_sha256": canonical_sha(main), "candidate_count": 6},
            "sealed_tail_packets": [{"packet_id": row["packet_id"], "packet_sha256": canonical_sha(row), "candidate_count": 1} for row in tails],
            "unified_candidate_tokens_sha256": canonical_sha(sorted(tokens)),
            "reviewer_instruction_sha256": instruction_sha,
            "batch_status": "PENDING_TWO_INDEPENDENT_TARGET_BLIND_RETURNS",
        })
    counts = {"prompt_groups": len(batches), "reviewer_visible_candidates_per_prompt_group": 8, "sealed_main_candidates_per_prompt_group": 6, "sealed_tail_candidates_per_prompt_group": 2, "required_independent_assessments": len(batches) * 8 * 2}
    if counts != {"prompt_groups": 1226, "reviewer_visible_candidates_per_prompt_group": 8, "sealed_main_candidates_per_prompt_group": 6, "sealed_tail_candidates_per_prompt_group": 2, "required_independent_assessments": 19616}:
        raise ValueError("V7 workload drift")
    out.mkdir(parents=True)
    write_jsonl(out / "unified_prompt_group_batch_manifest.jsonl", batches)
    write_json(out / "unified_independent_reviewer_return_schema.json", return_schema)
    write_json(out / "unified_sealed_coordinator_return_schema.json", coordinator_schema)
    bound_inputs = {str(SOP.relative_to(WORKSPACE)): sha(SOP), str((AUDIT / "summary.json").relative_to(WORKSPACE)): sha(AUDIT / "summary.json")}
    for name in audit_summary["outputs"]:
        bound_inputs[str((AUDIT / name).relative_to(WORKSPACE))] = sha(AUDIT / name)
    summary = {
        "status": "PASS_PHASE4_V7_STRICT_UNIFIED_BLIND_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS",
        "claim_boundary": "This V7 repair freezes source-native review delivery and schemas only. It contains no reviewer outcome, token-join use, reconciliation, acceptable-set label, retrieval result or final benchmark disposition.",
        "repair_reason": "V4, V5 and V6 were stopped before any outcome entered the library after static QA found insufficient exact-schema, content-binding, frozen-bound-input or coordinator-return enforcement. V7 rejects extra fields, reconstructs every packet at validation, re-hashes every freeze-bound input, validates both independent and coordinator returns, and finalises only validated reconciliation decisions.",
        "bound_inputs": bound_inputs,
        "implementation": {"path": str(Path(__file__).relative_to(WORKSPACE)), "sha256": sha(Path(__file__).resolve()), "python": sys.version},
        "counts": counts,
        "reviewer_instruction_sha256": instruction_sha,
        "outputs": {},
    }
    for path in (out / "unified_prompt_group_batch_manifest.jsonl", out / "unified_independent_reviewer_return_schema.json", out / "unified_sealed_coordinator_return_schema.json"):
        summary["outputs"][path.name] = sha(path)
    write_json(out / "summary.json", summary)
    print(json.dumps({"counts": counts, "output_dir": str(out), "status": summary["status"]}, sort_keys=True))


def verify_execution() -> dict[str, Any]:
    summary_path = EXECUTION / "summary.json"
    if not summary_path.is_file():
        raise ValueError("Missing V7 execution freeze")
    summary = read_json(summary_path)
    if summary.get("status") != "PASS_PHASE4_V7_STRICT_UNIFIED_BLIND_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS":
        raise ValueError("V7 execution status drift")
    impl = summary.get("implementation", {})
    if impl.get("path") != str(Path(__file__).relative_to(WORKSPACE)) or impl.get("sha256") != sha(Path(__file__).resolve()):
        raise ValueError("V7 implementation hash drift")
    for name, expected in summary.get("outputs", {}).items():
        path = EXECUTION / name
        if not path.is_file() or sha(path) != expected:
            raise ValueError(f"V7 execution output hash drift: {name}")
    bound_inputs = summary.get("bound_inputs")
    expected_bound_paths = {
        str(SOP.relative_to(WORKSPACE)),
        str((AUDIT / "summary.json").relative_to(WORKSPACE)),
        *(str((AUDIT / name).relative_to(WORKSPACE)) for name in EXPECTED_V2_OUTPUTS),
    }
    if not isinstance(bound_inputs, dict) or set(bound_inputs) != expected_bound_paths:
        raise ValueError("V7 frozen bound-input ledger is missing")
    for relative_path, expected in bound_inputs.items():
        path = (WORKSPACE / relative_path).resolve()
        if not path.is_relative_to(WORKSPACE) or not path.is_file() or sha(path) != expected:
            raise ValueError(f"V7 frozen bound-input hash drift: {relative_path}")
    verify_audit()
    return summary


def find_manifest(batch_id: str) -> dict[str, Any]:
    rows = [row for row in read_jsonl(EXECUTION / "unified_prompt_group_batch_manifest.jsonl") if row["batch_id"] == batch_id]
    if len(rows) != 1:
        raise ValueError(f"Unknown or ambiguous V7 batch: {batch_id}")
    return rows[0]


def expected_packet(batch_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    verify_execution()
    manifest = find_manifest(batch_id)
    _, main_by_id, tail_by_id = verify_audit()
    main_spec = manifest["sealed_main_packet"]
    main = main_by_id.get(main_spec["packet_id"])
    if main is None or canonical_sha(main) != main_spec["packet_sha256"] or len(main["candidates"]) != main_spec["candidate_count"] or main_spec["candidate_count"] != 6:
        raise ValueError("V7 sealed-main content binding drift")
    tails: list[dict[str, Any]] = []
    for spec in manifest["sealed_tail_packets"]:
        tail = tail_by_id.get(spec["packet_id"])
        if tail is None or canonical_sha(tail) != spec["packet_sha256"] or len(tail["candidates"]) != spec["candidate_count"] or spec["candidate_count"] != 1:
            raise ValueError("V7 sealed-tail content binding drift")
        tails.append(tail)
    raw_candidates = list(main["candidates"]) + [candidate for tail in tails for candidate in tail["candidates"]]
    candidates = [{"candidate_token": candidate["candidate_token"], "source_full_skill": candidate["source_full_skill"]} for candidate in raw_candidates]
    candidates.sort(key=lambda candidate: candidate["candidate_token"])
    tokens = [candidate["candidate_token"] for candidate in candidates]
    if len(candidates) != 8 or len(set(tokens)) != 8 or canonical_sha(tokens) != manifest["unified_candidate_tokens_sha256"]:
        raise ValueError("V7 unified candidate content binding drift")
    instruction, _, _, _ = reviewer_instruction_and_schema()
    packet = {"blind_packet_id": manifest["blind_packet_id"], "prompt": main["prompt"], "candidates": candidates, "review_instruction": instruction}
    if set(packet) != PACKET_FIELDS or any(set(candidate) != CANDIDATE_FIELDS for candidate in candidates) or keys_deep(packet) & FORBIDDEN_KEYS:
        raise ValueError("V7 reviewer-render allowlist or blindness drift")
    return manifest, packet


def render(batch_id: str, reviewer: str, output_dir: Path) -> None:
    manifest, packet = expected_packet(batch_id)
    output = {
        "schema_version": "rq2b_nc_phase4_v7_strict_unified_blind_render",
        "batch_id": batch_id,
        "reviewer_blind_id": reviewer,
        "batch_input_sha256": canonical_sha(packet),
        "reviewer_instruction_sha256": manifest["reviewer_instruction_sha256"],
        "blindness_notice": "This file contains no target, main/tail role, rank, lane, proposal channel, source path/provenance/licence, peer return, retrieval/reranking/provider outcome or metric. Review only this file and the frozen V7 schema.",
        "packet": packet,
    }
    if set(output) != RENDER_TOP_LEVEL or keys_deep(output) & FORBIDDEN_KEYS:
        raise ValueError("V7 reviewer-render leakage")
    path = output_dir.resolve() / f"reviewer_{reviewer}" / f"{batch_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError(f"Refusing to overwrite V7 reviewer batch: {path}")
    write_json(path, output)
    print(json.dumps({"batch_id": batch_id, "output": str(path), "reviewer": reviewer, "sha256": sha(path), "status": "PASS_V7_CONTENT_BOUND_UNIFIED_BLIND_BATCH"}, sort_keys=True))


def normalised_text(value: str) -> str:
    return " ".join(value.replace("#", " ").casefold().split())


def valid_anchor(anchor: str, source: str) -> bool:
    normal = normalised_text(anchor)
    return 4 <= len(normal) <= 160 and ";" not in anchor and normal in normalised_text(source)


def load_validated_return(batch_id: str, reviewer: str, return_path: Path | None = None) -> tuple[dict[str, Any], dict[str, Any], Path]:
    manifest, packet = expected_packet(batch_id)
    batch_path = BATCH_ROOT / f"reviewer_{reviewer}" / f"{batch_id}.json"
    if not batch_path.is_file():
        raise ValueError(f"Missing V7 frozen reviewer rendering: {batch_path}")
    batch = read_json(batch_path)
    expected_batch = {
        "schema_version": "rq2b_nc_phase4_v7_strict_unified_blind_render",
        "batch_id": batch_id,
        "reviewer_blind_id": reviewer,
        "batch_input_sha256": canonical_sha(packet),
        "reviewer_instruction_sha256": manifest["reviewer_instruction_sha256"],
        "blindness_notice": "This file contains no target, main/tail role, rank, lane, proposal channel, source path/provenance/licence, peer return, retrieval/reranking/provider outcome or metric. Review only this file and the frozen V7 schema.",
        "packet": packet,
    }
    if batch != expected_batch or set(batch) != RENDER_TOP_LEVEL or keys_deep(batch) & FORBIDDEN_KEYS:
        raise ValueError("V7 frozen reviewer-render content binding or blindness drift")
    actual_path = return_path or (RETURN_ROOT / f"reviewer_{reviewer}" / f"{batch_id}.json")
    if not actual_path.is_file():
        raise ValueError(f"Missing V7 reviewer return: {actual_path}")
    returned = read_json(actual_path)
    if set(returned) != RETURN_TOP_LEVEL:
        raise ValueError("V7 return has missing or forbidden top-level fields")
    if returned["reviewer_blind_id"] != reviewer or returned["batch_id"] != batch_id or returned["blind_packet_id"] != packet["blind_packet_id"] or returned["batch_input_sha256"] != canonical_sha(packet) or returned["reviewer_instruction_sha256"] != manifest["reviewer_instruction_sha256"] or returned["reviewer_output_sha256"] != canonical_without(returned, "reviewer_output_sha256"):
        raise ValueError("V7 return identity or cryptographic binding drift")
    assessments = returned["assessments"]
    source_by_token = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in packet["candidates"]}
    if not isinstance(assessments, list) or len(assessments) != 8 or {item.get("candidate_token") for item in assessments if isinstance(item, dict)} != set(source_by_token):
        raise ValueError("V7 return candidate partition drift")
    for assessment in assessments:
        if not isinstance(assessment, dict) or set(assessment) != ASSESSMENT_FIELDS:
            raise ValueError("V7 assessment has missing or forbidden fields")
        decision = assessment["adequacy"]
        anchor = assessment["source_anchor"]
        rationale = assessment["rationale"]
        missing = assessment["missing_material_requirement_or_null"]
        if decision not in ALLOWED_ADEQUACY or not isinstance(anchor, str) or not valid_anchor(anchor, source_by_token[assessment["candidate_token"]]) or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("V7 assessment adequacy, source-anchor or rationale drift")
        if (decision == "FULLY_ACCEPTABLE" and missing is not None) or (decision != "FULLY_ACCEPTABLE" and (not isinstance(missing, str) or not missing.strip())):
            raise ValueError("V7 missing-material requirement drift")
    return manifest, returned, actual_path


def validate(batch_id: str, reviewer: str, return_path: Path | None = None) -> None:
    _, returned, actual_path = load_validated_return(batch_id, reviewer, return_path)
    print(json.dumps({"assessments": len(returned["assessments"]), "batch_id": batch_id, "return_sha256": sha(actual_path), "reviewer": reviewer, "status": "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION"}, sort_keys=True))


def coordinator_context(batch_id: str, candidate_token: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Rebuild the only permitted coordinator context from independently validated returns."""
    manifest, return_a, path_a = load_validated_return(batch_id, "A")
    _, return_b, path_b = load_validated_return(batch_id, "B")
    _, packet = expected_packet(batch_id)
    by_a = {item["candidate_token"]: item for item in return_a["assessments"]}
    by_b = {item["candidate_token"]: item for item in return_b["assessments"]}
    source_by_token = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in packet["candidates"]}
    if candidate_token not in source_by_token:
        raise ValueError("Unknown V7 coordinator candidate token")
    decision_a, decision_b = by_a[candidate_token]["adequacy"], by_b[candidate_token]["adequacy"]
    if decision_a == decision_b and decision_a != "UNCLEAR":
        raise ValueError("Coordinator is not eligible for an exact non-UNCLEAR agreement")
    source = source_by_token[candidate_token]
    bindings = {
        "blind_packet_id": manifest["blind_packet_id"],
        "candidate_token": candidate_token,
        "reviewer_a_return_sha256": sha(path_a),
        "reviewer_b_return_sha256": sha(path_b),
        "fresh_source_render_sha256": canonical_sha({"candidate_token": candidate_token, "source_full_skill": source}),
    }
    packet_for_coordinator = {
        **bindings,
        "reviewer_A_assessment": by_a[candidate_token],
        "reviewer_B_assessment": by_b[candidate_token],
        "fresh_source_visible_skill": source,
        "coordinator_instruction": "Resolve only this A/B adequacy disagreement or UNCLEAR trigger under the frozen rubric. Do not inspect targets, main/tail role, allocation, rank, source path/provenance, historical/local reference, retrieval outcome or metric. Return only the strict coordinator schema.",
    }
    return bindings, packet_for_coordinator, {"reviewer_A": by_a[candidate_token], "reviewer_B": by_b[candidate_token]}


def load_validated_coordinator_return(batch_id: str, candidate_token: str, return_path: Path | None = None) -> tuple[dict[str, Any], Path]:
    bindings, _, _ = coordinator_context(batch_id, candidate_token)
    actual_path = return_path or (COORD_RETURN_ROOT / batch_id / f"{candidate_token}.json")
    if not actual_path.is_file():
        raise ValueError(f"Missing V7 coordinator return: {actual_path}")
    returned = read_json(actual_path)
    if set(returned) != COORDINATOR_RETURN_FIELDS:
        raise ValueError("V7 coordinator return has missing or forbidden fields")
    for key, expected in bindings.items():
        if returned[key] != expected:
            raise ValueError(f"V7 coordinator return binding drift: {key}")
    if returned["coordinator_decision"] not in COORDINATOR_DECISIONS or not isinstance(returned["rationale"], str) or not returned["rationale"].strip():
        raise ValueError("V7 coordinator decision or rationale drift")
    _, coordinator_packet, _ = coordinator_context(batch_id, candidate_token)
    if not isinstance(returned["source_anchor"], str) or not valid_anchor(returned["source_anchor"], coordinator_packet["fresh_source_visible_skill"]):
        raise ValueError("V7 coordinator source-anchor drift")
    if returned["coordinator_output_sha256"] != canonical_without(returned, "coordinator_output_sha256"):
        raise ValueError("V7 coordinator output-hash drift")
    return returned, actual_path


def validate_coordinator(batch_id: str, candidate_token: str, return_path: Path | None = None) -> None:
    returned, actual_path = load_validated_coordinator_return(batch_id, candidate_token, return_path)
    print(json.dumps({"batch_id": batch_id, "candidate_token": candidate_token, "coordinator_return_sha256": sha(actual_path), "decision": returned["coordinator_decision"], "status": "PASS_V7_STRICT_COORDINATOR_RETURN_VALIDATION"}, sort_keys=True))


def reconcile(batch_id: str, output_dir: Path) -> None:
    target = output_dir.resolve() / batch_id
    if target.exists():
        raise ValueError(f"Refusing to overwrite V7 reconciliation: {target}")
    manifest, return_a, path_a = load_validated_return(batch_id, "A")
    _, return_b, path_b = load_validated_return(batch_id, "B")
    _, packet = expected_packet(batch_id)
    by_a = {item["candidate_token"]: item for item in return_a["assessments"]}
    by_b = {item["candidate_token"]: item for item in return_b["assessments"]}
    source_by_token = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in packet["candidates"]}
    ledger, coordinator_packets = [], []
    for token in sorted(by_a):
        decision_a, decision_b = by_a[token]["adequacy"], by_b[token]["adequacy"]
        needs_coordinator = decision_a != decision_b or "UNCLEAR" in {decision_a, decision_b}
        disposition = "COORDINATOR_REQUIRED" if needs_coordinator else "EXACT_AGREEMENT_RETAINED"
        ledger.append({"candidate_token": token, "reviewer_A_adequacy": decision_a, "reviewer_B_adequacy": decision_b, "reviewer_A_source_anchor": by_a[token]["source_anchor"], "reviewer_B_source_anchor": by_b[token]["source_anchor"], "reconciliation_disposition": disposition})
        if needs_coordinator:
            coordinator_packets.append({"blind_packet_id": manifest["blind_packet_id"], "candidate_token": token, "reviewer_A_assessment": by_a[token], "reviewer_B_assessment": by_b[token], "fresh_source_visible_skill": source_by_token[token], "fresh_source_render_sha256": canonical_sha({"candidate_token": token, "source_full_skill": source_by_token[token]}), "coordinator_instruction": "Resolve only the A/B adequacy disagreement or UNCLEAR trigger under the frozen rubric. Do not inspect targets, main/tail role, allocation, rank, path, provenance, historical/local reference, retrieval outcome or metric."})
    target.mkdir(parents=True)
    write_json(target / "reconciliation_ledger.json", {"batch_id": batch_id, "blind_packet_id": manifest["blind_packet_id"], "reviewer_A_return_sha256": sha(path_a), "reviewer_B_return_sha256": sha(path_b), "candidate_reconciliations": ledger, "status": "PENDING_SEALED_COORDINATOR_FOR_DISAGREEMENTS_OR_UNCLEAR" if coordinator_packets else "PASS_EXACT_INDEPENDENT_AGREEMENT_PENDING_LIBRARY_LEVEL_CLOSURE"})
    write_jsonl(target / "sealed_coordinator_packets.jsonl", coordinator_packets)
    result = {"batch_id": batch_id, "exact_agreements": sum(row["reconciliation_disposition"] == "EXACT_AGREEMENT_RETAINED" for row in ledger), "coordinator_packets": len(coordinator_packets), "status": "PASS_V7_RECONCILIATION_MATERIALISED_PENDING_COORDINATOR" if coordinator_packets else "PASS_V7_EXACT_AGREEMENT_PENDING_LIBRARY_LEVEL_CLOSURE"}
    write_json(target / "summary.json", result)
    print(json.dumps(result, sort_keys=True))


def finalise(batch_id: str, output_dir: Path) -> None:
    """Apply only independently validated outcomes or a validated coordinator decision."""
    target = output_dir.resolve() / batch_id
    if not target.is_dir() or not (target / "reconciliation_ledger.json").is_file():
        raise ValueError("V7 reconciliation ledger must exist before finalisation")
    final_path = target / "final_disposition.json"
    if final_path.exists():
        raise ValueError(f"Refusing to overwrite V7 final disposition: {final_path}")
    manifest, return_a, _ = load_validated_return(batch_id, "A")
    _, return_b, _ = load_validated_return(batch_id, "B")
    by_a = {item["candidate_token"]: item for item in return_a["assessments"]}
    by_b = {item["candidate_token"]: item for item in return_b["assessments"]}
    decision_map = {
        "CONFIRMED_FULLY_ACCEPTABLE": "FULLY_ACCEPTABLE",
        "CONFIRMED_PARTIALLY_ADEQUATE": "PARTIALLY_ADEQUATE",
        "CONFIRMED_INADEQUATE": "INADEQUATE",
        "CONFIRMED_UNCLEAR": "UNCLEAR",
        "REOPEN_PACKET": "REOPEN_PACKET",
    }
    dispositions: list[dict[str, Any]] = []
    blocked = False
    for token in sorted(by_a):
        a, b = by_a[token]["adequacy"], by_b[token]["adequacy"]
        if a == b and a != "UNCLEAR":
            dispositions.append({"candidate_token": token, "final_adequacy": a, "decision_route": "EXACT_INDEPENDENT_AGREEMENT"})
            continue
        coordinator, coordinator_path = load_validated_coordinator_return(batch_id, token)
        final = decision_map[coordinator["coordinator_decision"]]
        dispositions.append({"candidate_token": token, "final_adequacy": final, "decision_route": "VALIDATED_COORDINATOR", "coordinator_return_sha256": sha(coordinator_path)})
        if final in {"UNCLEAR", "REOPEN_PACKET"}:
            blocked = True
    payload = {
        "batch_id": batch_id,
        "blind_packet_id": manifest["blind_packet_id"],
        "candidate_dispositions": dispositions,
        "status": "METHOD_GATE_OPEN_REOPEN_OR_UNCLEAR" if blocked else "PASS_V7_VALIDATED_BATCH_DISPOSITIONS_PENDING_LIBRARY_LEVEL_CLOSURE",
        "claim_boundary": "This is a target-blind source-adequacy disposition only. It does not open the token join, designate a main/tail member, create an acceptable set, determine MOST_SUITABLE, or report any retrieval result.",
    }
    write_json(final_path, payload)
    print(json.dumps({"batch_id": batch_id, "blocked": blocked, "dispositions": len(dispositions), "status": payload["status"]}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    freeze_parser = sub.add_parser("freeze")
    freeze_parser.add_argument("--output-dir", type=Path, default=EXECUTION)
    render_parser = sub.add_parser("render")
    render_parser.add_argument("--batch-id", required=True)
    render_parser.add_argument("--reviewer", choices=("A", "B"), required=True)
    render_parser.add_argument("--output-dir", type=Path, default=BATCH_ROOT)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--batch-id", required=True)
    validate_parser.add_argument("--reviewer", choices=("A", "B"), required=True)
    validate_parser.add_argument("--return-file", type=Path)
    coordinator_parser = sub.add_parser("validate-coordinator")
    coordinator_parser.add_argument("--batch-id", required=True)
    coordinator_parser.add_argument("--candidate-token", required=True)
    coordinator_parser.add_argument("--return-file", type=Path)
    reconcile_parser = sub.add_parser("reconcile")
    reconcile_parser.add_argument("--batch-id", required=True)
    reconcile_parser.add_argument("--output-dir", type=Path, default=RECON_ROOT)
    finalise_parser = sub.add_parser("finalise")
    finalise_parser.add_argument("--batch-id", required=True)
    finalise_parser.add_argument("--output-dir", type=Path, default=RECON_ROOT)
    args = parser.parse_args()
    try:
        if args.command == "freeze":
            freeze(args.output_dir)
        elif args.command == "render":
            render(args.batch_id, args.reviewer, args.output_dir)
        elif args.command == "validate":
            validate(args.batch_id, args.reviewer, args.return_file)
        elif args.command == "validate-coordinator":
            validate_coordinator(args.batch_id, args.candidate_token, args.return_file)
        elif args.command == "reconcile":
            reconcile(args.batch_id, args.output_dir)
        else:
            finalise(args.batch_id, args.output_dir)
    except ValueError as exc:
        raise SystemExit(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
