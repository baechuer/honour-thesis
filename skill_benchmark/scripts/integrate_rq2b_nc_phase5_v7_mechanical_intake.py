#!/usr/bin/env python3
"""Mechanically integrate the two frozen V7 machine-review inputs.

This is deliberately an intake and routing program, not a reconciliation
program.  It binds an active raw return *by Git object path and SHA*, replays
the frozen V7 validator, and creates only target-blind routing queues.  It
never opens the opaque target join, does not create an acceptable set, and does
not emit a coordinator conclusion.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import runpy
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
PROTOCOL = WORKSPACE / "skill_benchmark" / "scripts" / "rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
HANDOFF = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2_fresh_v20"
V7_EXECUTION = "skill_benchmark/rq2b_naturalistic_confusability/manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
RETURN_ROOT = "skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
B_SELECTION = "skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B-NC-phase5-v7-machine-b-full-raw-collection-validation-2026-09-08-v3/return_selection_replay.jsonl"
# The source commit preserves an invalid B-lane return for each of these groups
# and explicitly records that no replacement may be selected before a frozen-
# SOP disposition.  A passing file at the canonical path is therefore retained
# but deliberately not promoted to active evidence by this integration.
A_BINDING_GATE_INVALID_SUFFIX = {
    "RQ2B-P4-V7-U0979": "1558815b1a78e372",
    "RQ2B-P4-V7-U1078": "04f4510e00c66923",
}


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def git_blob(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=WORKSPACE)


def git_blob_or_none(revision: str, path: str) -> bytes | None:
    probe = subprocess.run(["git", "cat-file", "-e", f"{revision}:{path}"], cwd=WORKSPACE, capture_output=True)
    return git_blob(revision, path) if probe.returncode == 0 else None


def git_blobs(revision: str, paths: list[str]) -> dict[str, bytes | None]:
    """Read a bounded set of Git blobs in one batch, preserving missing paths."""
    unique = list(dict.fromkeys(paths))
    refs = [f"{revision}:{path}" for path in unique]
    # `subprocess.run(input=...)` drains stdout while feeding stdin; a manual
    # write-then-read pipe deadlocks when a large return set fills both pipes.
    process = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=WORKSPACE,
        input=("\n".join(refs) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        raise ValueError(f"git cat-file batch failed: {process.stderr.decode('utf-8')}")
    stream = io.BytesIO(process.stdout)
    result: dict[str, bytes | None] = {}
    for path in unique:
        header = stream.readline().decode("utf-8").rstrip("\n")
        pieces = header.split()
        if len(pieces) == 2 and pieces[1] == "missing":
            result[path] = None
            continue
        if len(pieces) != 3 or pieces[1] != "blob":
            raise ValueError(f"unexpected git cat-file header for {path}: {header!r}")
        size = int(pieces[2])
        body = stream.read(size)
        if len(body) != size or stream.read(1) != b"\n":
            raise ValueError(f"truncated git blob for {path}")
        result[path] = body
    return result


def git_commit(revision: str) -> str:
    return subprocess.check_output(["git", "rev-parse", revision], cwd=WORKSPACE, text=True).strip()


def jsonl_from_blob(revision: str, path: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in git_blob(revision, path).decode("utf-8").splitlines() if line]


def assessment_vector_hash(returned: dict[str, Any]) -> tuple[str, bool]:
    """A non-semantic equality check: exact token-to-adequacy vector + UNCLEAR flag."""
    vector = sorted((item["candidate_token"], item["adequacy"]) for item in returned["assessments"])
    encoded = json.dumps(vector, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return sha_bytes(encoded), any(item["adequacy"] == "UNCLEAR" for item in returned["assessments"])


def make_ledger_row(
    *, group: dict[str, Any], lane: str, owner: str, source_commit: str | None,
    source_path: str | None, source_sha256: str | None, selection_basis: str,
    validation: str, vector_sha256: str | None, contains_unclear: bool | None,
    validation_error: str | None = None,
) -> dict[str, Any]:
    # Deliberately no target, gold, retrieval result, reconciliation decision,
    # source skill body, or adequacy outcome is emitted.
    return {
        "schema_version": "rq2b_nc_phase5_v7_mechanical_integration_intake_v1",
        "batch_id": group["batch_id"],
        "blind_packet_id": group["blind_packet_id"],
        "owner_machine": owner,
        "reviewer_lane": lane,
        "source_commit": source_commit,
        "source_return_path": source_path,
        "source_return_sha256": source_sha256,
        "selection_basis": selection_basis,
        "active_return_selected": validation == "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION",
        "validation": validation,
        "validation_error": validation_error,
        "assessment_vector_sha256": vector_sha256,
        "contains_unclear": contains_unclear,
        "packet_input_sha256": group["packet_input_sha256"],
        "protocol_instruction_sha256": group["protocol_instruction_sha256"],
        "assignment_version": group["assignment_version"],
    }


def validate_active_return(
    *, batch_id: str, lane: str, raw: bytes, manifest: dict[str, Any], packet: dict[str, Any], packet_input_sha256: str, protocol_globals: dict[str, Any],
) -> tuple[str, str | None, bool | None, str | None]:
    """Apply the frozen return-validation contract against cached verified packets.

    The frozen protocol repeatedly loads a source-visible reviewer-rendering
    file for each lane.  This intake has already rebuilt and allowlist-checked
    the exact packet from the frozen manifest, so this direct implementation
    avoids materialising or copying that source-visible cache while preserving
    the same return-schema, binding, anchor, and missing-material checks.
    """
    try:
        returned = json.loads(raw.decode("utf-8"))
        if set(returned) != protocol_globals["RETURN_TOP_LEVEL"]:
            raise ValueError("V7 return has missing or forbidden top-level fields")
        if (
            returned["reviewer_blind_id"] != lane
            or returned["batch_id"] != batch_id
            or returned["blind_packet_id"] != packet["blind_packet_id"]
            or returned["batch_input_sha256"] != packet_input_sha256
            or returned["reviewer_instruction_sha256"] != manifest["reviewer_instruction_sha256"]
            or returned["reviewer_output_sha256"] != protocol_globals["canonical_without"](returned, "reviewer_output_sha256")
        ):
            raise ValueError("V7 return identity or cryptographic binding drift")
        assessments = returned["assessments"]
        source_by_token = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in packet["candidates"]}
        if not isinstance(assessments, list) or len(assessments) != 8 or {item.get("candidate_token") for item in assessments if isinstance(item, dict)} != set(source_by_token):
            raise ValueError("V7 return candidate partition drift")
        for assessment in assessments:
            if not isinstance(assessment, dict) or set(assessment) != protocol_globals["ASSESSMENT_FIELDS"]:
                raise ValueError("V7 assessment has missing or forbidden fields")
            decision = assessment["adequacy"]
            anchor = assessment["source_anchor"]
            rationale = assessment["rationale"]
            missing = assessment["missing_material_requirement_or_null"]
            if decision not in protocol_globals["ALLOWED_ADEQUACY"] or not isinstance(anchor, str) or not protocol_globals["valid_anchor"](anchor, source_by_token[assessment["candidate_token"]]) or not isinstance(rationale, str) or not rationale.strip():
                raise ValueError("V7 assessment adequacy, source-anchor or rationale drift")
            if (decision == "FULLY_ACCEPTABLE" and missing is not None) or (decision != "FULLY_ACCEPTABLE" and (not isinstance(missing, str) or not missing.strip())):
                raise ValueError("V7 missing-material requirement drift")
        vector_sha256, contains_unclear = assessment_vector_hash(returned)
        return "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION", vector_sha256, contains_unclear, None
    except Exception as exc:  # validator diagnostics are evidence, not a repair.
        return "INVALID_RETAINED", None, None, f"{type(exc).__name__}: {exc}"


def assert_packet_integrity(group: dict[str, Any], sealed: dict[str, Any], packet: dict[str, Any], protocol_globals: dict[str, Any]) -> None:
    if group["blind_packet_id"] != sealed["blind_packet_id"] or packet["blind_packet_id"] != sealed["blind_packet_id"]:
        raise ValueError(f"{group['batch_id']}: blind packet identity drift")
    if group["packet_input_sha256"] != protocol_globals["canonical_sha"](packet):
        raise ValueError(f"{group['batch_id']}: packet-input hash drift")
    if sealed["sealed_main_packet"].get("candidate_count") != 6 or len(sealed["sealed_tail_packets"]) != 2:
        raise ValueError(f"{group['batch_id']}: K=6 / two-tail shape drift")
    if group["sealed_main_packet_sha256"] != sealed["sealed_main_packet"].get("packet_sha256"):
        raise ValueError(f"{group['batch_id']}: main packet hash drift")
    if group["sealed_tail_packet_sha256s"] != [item.get("packet_sha256") for item in sealed["sealed_tail_packets"]]:
        raise ValueError(f"{group['batch_id']}: tail packet hash drift")
    if len(packet["candidates"]) != 8 or protocol_globals["keys_deep"](packet) & protocol_globals["FORBIDDEN_KEYS"]:
        raise ValueError(f"{group['batch_id']}: reviewer packet blindness drift")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-machine-a", default="71fb10e")
    parser.add_argument("--source-machine-b", default="ab7ea5a")
    parser.add_argument(
        "--validator-render-cache",
        default="skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B-NC-phase4-v7-strict-unified-target-blind-batches-2026-09-05",
        help="target-blind V7 reviewer render cache used only by the frozen validator",
    )
    parser.add_argument(
        "--materialise-validator-render-cache",
        action="store_true",
        help="create missing target-blind validator render files in --validator-render-cache",
    )
    parser.add_argument(
        "--output",
        default="skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1",
    )
    args = parser.parse_args()
    source_a, source_b = git_commit(args.source_machine_a), git_commit(args.source_machine_b)
    out = (WORKSPACE / args.output).resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite existing intake package: {out}")
    out.mkdir(parents=True)

    a_manifest_path = f"{HANDOFF}/machine_a_manifest.jsonl"
    b_manifest_path = f"{HANDOFF}/machine_b_manifest.jsonl"
    a_manifest_raw, b_manifest_raw = git_blob(source_a, a_manifest_path), git_blob(source_b, b_manifest_path)
    a_groups = [json.loads(line) for line in a_manifest_raw.decode("utf-8").splitlines() if line]
    b_groups = [json.loads(line) for line in b_manifest_raw.decode("utf-8").splitlines() if line]
    a_by_id, b_by_id = ({row["batch_id"]: row for row in groups} for groups in (a_groups, b_groups))
    if len(a_by_id) != len(a_groups) or len(b_by_id) != len(b_groups):
        raise ValueError("duplicate prompt group in machine manifest")
    if set(a_by_id) & set(b_by_id):
        raise ValueError("machine manifests overlap")
    scope = set(a_by_id) | set(b_by_id)
    if len(a_groups) != 533 or len(b_groups) != 533 or len(scope) != 1066:
        raise ValueError("unexpected current V7 machine scope; refusing integration")

    v7_manifest_path = f"{V7_EXECUTION}/unified_prompt_group_batch_manifest.jsonl"
    v7_a, v7_b = git_blob(source_a, v7_manifest_path), git_blob(source_b, v7_manifest_path)
    if v7_a != v7_b:
        raise ValueError("machine source commits disagree on V7 unified manifest")

    # Batch-read every possible raw return before validation.  This is a
    # mechanical transport optimisation only; byte hashes are still checked
    # individually and no blob is copied into the output package.
    a_return_paths = [f"{RETURN_ROOT}/reviewer_{lane}/{bid}.json" for bid in a_by_id for lane in ("A", "B")]
    b_selection = jsonl_from_blob(source_b, B_SELECTION)
    selected_b: dict[tuple[str, str], dict[str, Any]] = {}
    for row in b_selection:
        key = (row["batch_id"], row["lane"])
        if row["batch_id"] not in b_by_id or row["lane"] not in {"A", "B"} or key in selected_b:
            raise ValueError("Machine-B selection ledger is malformed or outside machine scope")
        selected_b[key] = row
    expected_b_ledger_rows = {(bid, lane) for bid in b_by_id for lane in ("A", "B")}
    if set(selected_b) != expected_b_ledger_rows:
        raise ValueError("Machine-B selection ledger does not cover exactly the machine scope")
    a_raw_by_path = git_blobs(source_a, a_return_paths)
    b_raw_by_path = git_blobs(source_b, [row["return_path"] for row in selected_b.values()])

    protocol_ns = runpy.run_path(str(PROTOCOL))
    g = protocol_ns["load_validated_return"].__globals__
    execution_replay = g["verify_execution"]()
    audit_replay = g["verify_audit"]()
    # The frozen implementation deliberately reloads its complete manifest on
    # every packet call.  Cache only those already hash-verified structures for
    # this read-only replay; the packet-level hash assertions below still run
    # for every member of the 1,066-group scope.
    verified_manifest_rows = g["read_jsonl"](g["EXECUTION"] / "unified_prompt_group_batch_manifest.jsonl")
    verified_manifest_by_id = {row["batch_id"]: row for row in verified_manifest_rows}
    if len(verified_manifest_rows) != 1226 or len(verified_manifest_by_id) != 1226:
        raise ValueError("frozen V7 unified manifest count/identity drift")
    g["find_manifest"] = lambda batch_id: verified_manifest_by_id[batch_id]
    # Render validator-only packet copies in an automatic temporary directory.
    # This replay cache is never part of the integration artifact.
    with tempfile.TemporaryDirectory(prefix="rq2b-v7-mechanical-intake-") as temp:
        temp_dir = Path(temp)
        render_cache = (WORKSPACE / args.validator_render_cache).resolve()
        if args.materialise_validator_render_cache:
            render_cache.mkdir(parents=True, exist_ok=True)
        g["BATCH_ROOT"] = render_cache
        g["verify_execution"] = lambda: execution_replay
        g["verify_audit"] = lambda: audit_replay
        _audit_summary, main_by_id, tail_by_id = audit_replay
        instruction, _rubric, _return_schema, _coordinator_schema = g["reviewer_instruction_and_schema"]()
        packet_by_id: dict[str, tuple[dict[str, Any], dict[str, Any], str]] = {}
        for bid in sorted(scope):
            # `verify_execution` and `verify_audit` above have already replayed
            # all source packet content and hashes.  Assemble each selected
            # reviewer-visible packet from those verified maps once, rather
            # than rehashing the entire source packet separately for each lane.
            sealed = verified_manifest_by_id[bid]
            main = main_by_id[sealed["sealed_main_packet"]["packet_id"]]
            tails = [tail_by_id[item["packet_id"]] for item in sealed["sealed_tail_packets"]]
            candidates = list(main["candidates"]) + [candidate for tail in tails for candidate in tail["candidates"]]
            packet = {
                "blind_packet_id": sealed["blind_packet_id"],
                "prompt": main["prompt"],
                "candidates": sorted(({"candidate_token": item["candidate_token"], "source_full_skill": item["source_full_skill"]} for item in candidates), key=lambda item: item["candidate_token"]),
                "review_instruction": instruction,
            }
            group = a_by_id.get(bid, b_by_id.get(bid))
            assert_packet_integrity(group, sealed, packet, g)
            packet_by_id[bid] = (sealed, packet, g["canonical_sha"](packet))
            for lane in ("A", "B"):
                renderer_path = render_cache / f"reviewer_{lane}" / f"{bid}.json"
                if not renderer_path.is_file():
                    if not args.materialise_validator_render_cache:
                        raise ValueError(f"missing validator render cache: {renderer_path}; rerun with --materialise-validator-render-cache and an ephemeral cache path")
                    # The frozen renderer prints a status line per packet;
                    # suppress that ephemeral diagnostic stream so the intake
                    # report is the only durable replay record.
                    with contextlib.redirect_stdout(io.StringIO()):
                        protocol_ns["render"](bid, lane, render_cache)

        ledger: list[dict[str, Any]] = []
        group_rows: dict[str, list[dict[str, Any]]] = {}
        invalid_preservation: list[dict[str, Any]] = []
        unselected_validator_passing: list[dict[str, Any]] = []

        # Machine A always points to the original A-machine source commit.  A
        # missing or invalid raw return remains a ledger row, never a rewrite.
        for bid, group in sorted(a_by_id.items()):
            rows = []
            for lane in ("A", "B"):
                path = f"{RETURN_ROOT}/reviewer_{lane}/{bid}.json"
                raw = a_raw_by_path[path]
                if lane == "B" and bid in A_BINDING_GATE_INVALID_SUFFIX:
                    if raw is None:
                        raise ValueError(f"{bid}/B: frozen binding gate lacks canonical-path evidence")
                    frozen_manifest, packet, packet_input_sha256 = packet_by_id[bid]
                    current_validation, _vector, _unclear, current_error = validate_active_return(batch_id=bid, lane=lane, raw=raw, manifest=frozen_manifest, packet=packet, packet_input_sha256=packet_input_sha256, protocol_globals=g)
                    if current_validation != "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION":
                        raise ValueError(f"{bid}/B: expected unselected validator-passing path no longer passes: {current_error}")
                    invalid_path = f"{RETURN_ROOT}/reviewer_B/superseded_invalid/{bid}_{A_BINDING_GATE_INVALID_SUFFIX[bid]}.json"
                    invalid_raw = git_blob(source_a, invalid_path)
                    invalid_validation, _vector, _unclear, invalid_error = validate_active_return(batch_id=bid, lane=lane, raw=invalid_raw, manifest=frozen_manifest, packet=packet, packet_input_sha256=packet_input_sha256, protocol_globals=g)
                    if invalid_validation != "INVALID_RETAINED":
                        raise ValueError(f"{bid}/B: expected preserved binding-drift return does not fail validator")
                    row = make_ledger_row(group=group, lane=lane, owner="machine_a", source_commit=source_a, source_path=invalid_path, source_sha256=sha_bytes(invalid_raw), selection_basis="frozen_binding_gate_unresolved_no_active_B_selection", validation="NO_APPROVED_ACTIVE_RETURN", vector_sha256=None, contains_unclear=None, validation_error=invalid_error)
                    invalid_preservation.append({"batch_id": bid, "owner_machine": "machine_a", "reviewer_lane": lane, "source_commit": source_a, "source_return_path": invalid_path, "source_return_sha256": sha_bytes(invalid_raw), "validation": "INVALID_RETAINED", "validation_error": invalid_error})
                    unselected_validator_passing.append({"batch_id": bid, "owner_machine": "machine_a", "reviewer_lane": lane, "source_commit": source_a, "return_path": path, "return_sha256": sha_bytes(raw), "reason_not_selected": "frozen_binding_gate_requires_SOP_disposition_before_traceable_reissue_or_active_selection"})
                elif raw is None:
                    row = make_ledger_row(group=group, lane=lane, owner="machine_a", source_commit=source_a, source_path=None, source_sha256=None, selection_basis="no_source_return_present", validation="MISSING_RETAINED", vector_sha256=None, contains_unclear=None, validation_error="no raw return at frozen source commit")
                    invalid_preservation.append({"batch_id": bid, "owner_machine": "machine_a", "reviewer_lane": lane, "source_commit": source_a, "source_return_path": None, "source_return_sha256": None, "validation": "MISSING_RETAINED", "validation_error": row["validation_error"]})
                else:
                    frozen_manifest, packet, packet_input_sha256 = packet_by_id[bid]
                    validation, vector, unclear, error = validate_active_return(batch_id=bid, lane=lane, raw=raw, manifest=frozen_manifest, packet=packet, packet_input_sha256=packet_input_sha256, protocol_globals=g)
                    row = make_ledger_row(group=group, lane=lane, owner="machine_a", source_commit=source_a, source_path=path, source_sha256=sha_bytes(raw), selection_basis="canonical_original", validation=validation, vector_sha256=vector, contains_unclear=unclear, validation_error=error)
                    if validation != "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION":
                        invalid_preservation.append({"batch_id": bid, "owner_machine": "machine_a", "reviewer_lane": lane, "source_commit": source_a, "source_return_path": path, "source_return_sha256": sha_bytes(raw), "validation": validation, "validation_error": error})
                ledger.append(row); rows.append(row)
            group_rows[bid] = rows

        # Machine B is selected only through its validated selection ledger;
        # this follows reissues by pointer and keeps original invalid raw files
        # untouched in their source commit.
        for bid, group in sorted(b_by_id.items()):
            rows = []
            for lane in ("A", "B"):
                selected = selected_b.get((bid, lane))
                if selected is None:
                    path = f"{RETURN_ROOT}/reviewer_{lane}/{bid}.json"
                    raw = git_blob_or_none(source_b, path)
                    row = make_ledger_row(group=group, lane=lane, owner="machine_b", source_commit=source_b, source_path=path if raw is not None else None, source_sha256=sha_bytes(raw) if raw is not None else None, selection_basis="no_valid_selected_return_retained_raw" if raw is not None else "no_source_return_present", validation="MISSING_RETAINED" if raw is None else "INVALID_RETAINED", vector_sha256=None, contains_unclear=None, validation_error="Machine-B selection ledger intentionally contains no active lane for this started-incomplete group")
                    if raw is not None:
                        invalid_preservation.append({"batch_id": bid, "owner_machine": "machine_b", "reviewer_lane": lane, "source_commit": source_b, "source_return_path": path, "source_return_sha256": sha_bytes(raw), "validation": "INVALID_RETAINED", "validation_error": row["validation_error"]})
                else:
                    raw = b_raw_by_path[selected["return_path"]]
                    if raw is None:
                        raise ValueError(f"{bid}/{lane}: selection-ledger path is absent at Machine-B source commit")
                    if sha_bytes(raw) != selected["return_sha256"]:
                        raise ValueError(f"{bid}/{lane}: selection-ledger return SHA drift")
                    frozen_manifest, packet, packet_input_sha256 = packet_by_id[bid]
                    validation, vector, unclear, error = validate_active_return(batch_id=bid, lane=lane, raw=raw, manifest=frozen_manifest, packet=packet, packet_input_sha256=packet_input_sha256, protocol_globals=g)
                    if selected["validation"] == "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION":
                        if validation != "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION":
                            raise ValueError(f"{bid}/{lane}: selected Machine-B active return fails fresh validation: {error}")
                        row = make_ledger_row(group=group, lane=lane, owner="machine_b", source_commit=source_b, source_path=selected["return_path"], source_sha256=selected["return_sha256"], selection_basis=selected["return_source"], validation=validation, vector_sha256=vector, contains_unclear=unclear, validation_error=None)
                    else:
                        if validation == "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION":
                            raise ValueError(f"{bid}/{lane}: Machine-B invalid-retained selection unexpectedly passes fresh validation")
                        row = make_ledger_row(group=group, lane=lane, owner="machine_b", source_commit=source_b, source_path=selected["return_path"], source_sha256=selected["return_sha256"], selection_basis=f"{selected['return_source']}_invalid_retained", validation="INVALID_RETAINED", vector_sha256=None, contains_unclear=None, validation_error=error)
                        invalid_preservation.append({"batch_id": bid, "owner_machine": "machine_b", "reviewer_lane": lane, "source_commit": source_b, "source_return_path": selected["return_path"], "source_return_sha256": selected["return_sha256"], "validation": "INVALID_RETAINED", "validation_error": error})
                ledger.append(row); rows.append(row)
            group_rows[bid] = rows

    # Docket is intentionally group-level and target-blind.  The four extra
    # entries are mechanically evidenced by this replay, not semantic fixes.
    explicit_gate_reasons = {
        "RQ2B-P4-V7-U0323": "historical_REOPEN_PACKET_method_gate_requires_user_decision",
        "RQ2B-P4-V7-U0527": "both_lanes_source_anchor_or_rationale_drift",
        "RQ2B-P4-V7-U0979": "machine_a_reviewer_B_identity_or_cryptographic_binding_drift",
        "RQ2B-P4-V7-U1078": "machine_a_reviewer_B_identity_or_cryptographic_binding_drift",
        "RQ2B-P4-V7-U1068": "machine_a_reviewer_B_raw_return_missing",
        "RQ2B-P4-V7-U1157": "machine_a_both_raw_returns_missing",
    }
    direct, coordinator, docket = [], [], []
    for bid in sorted(scope):
        rows = group_rows[bid]
        all_valid = all(row["validation"] == "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION" for row in rows)
        route = None
        if bid in explicit_gate_reasons:
            route = "GATE_DOCKET"
            docket.append({"batch_id": bid, "blind_packet_id": rows[0]["blind_packet_id"], "owner_machine": rows[0]["owner_machine"], "gate_reason": explicit_gate_reasons[bid], "active_return_lane_count": sum(row["active_return_selected"] for row in rows)})
        elif not all_valid:
            route = "STARTED_INCOMPLETE"
            docket.append({"batch_id": bid, "blind_packet_id": rows[0]["blind_packet_id"], "owner_machine": rows[0]["owner_machine"], "gate_reason": "missing_or_invalid_raw_return_requires_user_approved_reissue_or_defer", "active_return_lane_count": sum(row["active_return_selected"] for row in rows)})
        else:
            same_vector = rows[0]["assessment_vector_sha256"] == rows[1]["assessment_vector_sha256"]
            has_unclear = bool(rows[0]["contains_unclear"] or rows[1]["contains_unclear"])
            queue_row = {"batch_id": bid, "blind_packet_id": rows[0]["blind_packet_id"], "owner_machine": rows[0]["owner_machine"], "packet_input_sha256": rows[0]["packet_input_sha256"], "reviewer_A_return_sha256": next(row["source_return_sha256"] for row in rows if row["reviewer_lane"] == "A"), "reviewer_B_return_sha256": next(row["source_return_sha256"] for row in rows if row["reviewer_lane"] == "B")}
            if same_vector and not has_unclear:
                route = "DIRECT_RECONCILIATION_ELIGIBLE"
                direct.append(queue_row)
            else:
                route = "SEALED_COORDINATOR_ELIGIBLE"
                queue_row["trigger"] = "UNCLEAR" if has_unclear else "candidate_level_disagreement"
                coordinator.append(queue_row)
        for row in rows:
            row["group_route"] = route

    ledger.sort(key=lambda row: (row["owner_machine"], row["batch_id"], row["reviewer_lane"]))
    direct.sort(key=lambda row: row["batch_id"])
    coordinator.sort(key=lambda row: row["batch_id"])
    docket.sort(key=lambda row: row["batch_id"])
    invalid_preservation.sort(key=lambda row: (row["owner_machine"], row["batch_id"], row["reviewer_lane"]))
    unselected_validator_passing.sort(key=lambda row: (row["owner_machine"], row["batch_id"], row["reviewer_lane"]))

    write_jsonl(out / "integration_intake_ledger.jsonl", ledger)
    write_jsonl(out / "direct_reconciliation_queue.jsonl", direct)
    write_jsonl(out / "sealed_coordinator_queue.jsonl", coordinator)
    write_jsonl(out / "gate_docket.jsonl", docket)
    write_jsonl(out / "retained_invalid_or_missing_returns.jsonl", invalid_preservation)
    write_jsonl(out / "unselected_validator_passing_returns.jsonl", unselected_validator_passing)
    counts = Counter(row["validation"] for row in ledger)
    routes = Counter(row["group_route"] for row in ledger if row["reviewer_lane"] == "A")
    report = {
        "schema_version": "rq2b_nc_phase5_v7_mechanical_integration_report_v1",
        "claim_boundary": "Mechanical intake, validator replay, and target-blind routing only. No coordinator conclusion, opaque target join, acceptable set, library update, retrieval, metric, or thesis result is created.",
        "frozen_inputs": {
            "machine_a_source_commit": source_a,
            "machine_b_source_commit": source_b,
            "machine_a_manifest_path": a_manifest_path,
            "machine_a_manifest_sha256": sha_bytes(a_manifest_raw),
            "machine_b_manifest_path": b_manifest_path,
            "machine_b_manifest_sha256": sha_bytes(b_manifest_raw),
            "v7_unified_manifest_path": v7_manifest_path,
            "v7_unified_manifest_sha256": sha_bytes(v7_a),
            "frozen_protocol_path": str(PROTOCOL.relative_to(WORKSPACE)),
            "frozen_protocol_sha256": sha_path(PROTOCOL),
            "machine_b_selection_ledger_path": B_SELECTION,
            "machine_b_selection_ledger_sha256": sha_bytes(git_blob(source_b, B_SELECTION)),
        },
        "scope_checks": {"machine_a_groups": len(a_groups), "machine_b_groups": len(b_groups), "combined_pending_groups": len(scope), "machine_scope_disjoint": True, "machine_scope_coverage_complete": True, "v7_unified_manifest_identical_across_source_commits": True},
        "mechanical_replay": {
            # Keep only replay commitments/digests.  The frozen validator's
            # full replay object includes source material and is intentionally
            # not copied into this target-blind integration package.
            "execution_replay_status": execution_replay.get("status"),
            "execution_replay_canonical_sha256": g["canonical_sha"](execution_replay),
            "audit_replay_passed": True,
            "audit_replay_item_count": len(audit_replay),
            "audit_replay_canonical_sha256": g["canonical_sha"](audit_replay),
            "packet_hash_k6_two_tail_blindness_replay": "PASS",
            "return_validation_counts": dict(sorted(counts.items())),
            "active_return_count": sum(row["active_return_selected"] for row in ledger),
            "retained_invalid_or_missing_return_count": len(invalid_preservation),
            "unselected_validator_passing_return_count": len(unselected_validator_passing),
            "machine_b_ready_for_reconciliation_groups": sum(1 for bid in b_by_id if all(row["active_return_selected"] for row in group_rows[bid])),
            "machine_b_finalised_groups_created": 0,
        },
        "routing": {"direct_reconciliation_eligible_groups": len(direct), "sealed_coordinator_eligible_groups": len(coordinator), "gate_docket_groups": len(docket), "group_route_counts": dict(sorted(routes.items()))},
        "prohibitions_honoured": ["no raw return copied or overwritten", "no target join", "no coordinator conclusion", "no acceptable set", "no library update", "no K=8 amendment"],
    }
    write_json(out / "mechanical_integration_report.json", report)
    write_json(out / "integrity_report.json", report)
    report_markdown = (
        "# V7 mechanical integration report\n\n"
        "This package records mechanical evidence only. `READY_FOR_RECONCILIATION` means two active returns passed the frozen validator; it is not finalisation. The routing queues must not be executed before the gate docket is decided.\n\n"
        f"- Scope: {len(scope)} groups; Machine A {len(a_groups)}, Machine B {len(b_groups)}; no overlap.\n"
        f"- Active validator-passing returns: {sum(row['active_return_selected'] for row in ledger)}.\n"
        f"- Direct-reconciliation eligible: {len(direct)}; sealed-coordinator eligible: {len(coordinator)}; decision docket: {len(docket)}.\n"
        f"- Machine B has {report['mechanical_replay']['machine_b_ready_for_reconciliation_groups']} READY_FOR_RECONCILIATION groups and zero newly finalised groups.\n\n"
        "See `gate_memo.md` before any semantic step.\n"
    )
    (out / "mechanical_integration_report.md").write_text(report_markdown, encoding="utf-8")
    (out / "integrity_report.md").write_text(report_markdown, encoding="utf-8")
    (out / "gate_memo.md").write_text(
        "# Gate memo — no semantic resolution performed\n\n"
        "This memo is target-blind. It records why specified groups are withheld from reconciliation; it does not decide adequacy, open a target join, or modify K=6.\n\n"
        "## Required user decisions\n\n"
        "- `RQ2B-P4-V7-U0323`: historical V7 material records `REOPEN_PACKET`. Decide whether this is a purely local packet/anchor defect that permits a fresh independent A+B reissue on the same frozen packet, or a substantive coverage/construct concern requiring explicit defer/exclude or a prospective amendment. No automatic K=8 change is permitted.\n"
        "- `RQ2B-P4-V7-U0527`: both raw lanes fail the frozen source-anchor/rationale validator. Preserve both originals. Preferred path: after the U0323 method decision, issue a fresh independent A+B review on the unchanged frozen packet; alternative: explicit defer/exclude. Do not invent anchors, rationales, or adequacy.\n\n"
        "## Additional mechanical docket entries discovered in Machine A evidence\n\n"
        "- `RQ2B-P4-V7-U0979` and `RQ2B-P4-V7-U1078`: reviewer-B identity/cryptographic binding drift. A valid lane alone is insufficient; retain the raw record and choose a traceable fresh B-lane (or fresh A+B) reissue, or defer/exclude.\n"
        "- `RQ2B-P4-V7-U1068`: reviewer-B raw return is absent at the frozen Machine-A source commit.\n"
        "- `RQ2B-P4-V7-U1157`: neither raw return is present at the frozen Machine-A source commit.\n\n"
        "The last four are not semantic repairs and are listed because the mechanical replay cannot make them disappear.\n",
        encoding="utf-8",
    )
    (out / "README.md").write_text(
        "# RQ2b-NC V7 mechanical integration intake\n\n"
        "This is a frozen pointer-and-hash intake package for the two supplied machine commits. It is not a merged raw-return tree and does not alter canonical raw returns. The intake ledger selects at most one validator-passing active return per lane; all reissues are selected by source path and SHA.\n\n"
        "## Exact replay\n\n"
        "```sh\n"
        "python3 skill_benchmark/scripts/integrate_rq2b_nc_phase5_v7_mechanical_intake.py \\\n"
        "  --source-machine-a 71fb10eb297f4a9c5ae8d8bb4bec8dc8b955a0d8 \\\n"
        "  --source-machine-b ab7ea5a5a72d22c2e06fcdbcad2d2a0d70b0cbee \\\n"
        "  --validator-render-cache /private/tmp/rq2b-v7-mechanical-replay-cache \\\n"
        "  --materialise-validator-render-cache \\\n"
        "  --output /private/tmp/rq2b-v7-mechanical-integration-replay\n"
        "```\n\n"
        "The command materialises source-visible but target-blind validator renders only in `/private/tmp`; they are replay cache, not intake evidence, and must not be committed. It must run in a clone containing both source commits and the frozen V7 protocol.\n\n"
        "## Stop boundary\n\n"
        "Do not execute either routing queue until the gate docket has explicit approval. In particular, `READY_FOR_RECONCILIATION` is not `FINALISED`. This package contains no target identity, gold label, retrieval outcome, acceptable set, or library update.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS_V7_MECHANICAL_INTAKE", "output": str(out), "direct": len(direct), "coordinator": len(coordinator), "docket": len(docket)}, sort_keys=True))


if __name__ == "__main__":
    main()
