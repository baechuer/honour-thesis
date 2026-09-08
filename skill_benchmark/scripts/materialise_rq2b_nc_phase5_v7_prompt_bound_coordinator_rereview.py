#!/usr/bin/env python3
"""Materialise a prospective, prompt-bound V7 coordinator re-review package.

The historical V7/V2 coordinator returns remain immutable.  This amendment
re-reviews every coordinator-eligible disagreement with the same frozen source
and A/B returns, plus the original target-blind prompt and frozen adequacy
rubric.  It contains no target join, gold label, rank, main/tail role, retrieval
outcome, acceptable set, or library update.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
PROTOCOL = WORKSPACE / "skill_benchmark" / "scripts" / "rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
INTEGRATION = NC / "manifests" / "rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_2026_09_08_v1"


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def git_blobs(revision: str, paths: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(paths))
    process = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=WORKSPACE,
        input=("\n".join(f"{revision}:{path}" for path in unique) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        raise ValueError(process.stderr.decode("utf-8"))
    result: dict[str, bytes] = {}
    cursor = 0
    for path in unique:
        end = process.stdout.index(b"\n", cursor)
        header = process.stdout[cursor:end].decode("utf-8").split()
        cursor = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise ValueError(f"missing/unexpected source blob for {revision}:{path}: {header}")
        size = int(header[2])
        result[path] = process.stdout[cursor:cursor + size]
        cursor += size
        if process.stdout[cursor:cursor + 1] != b"\n":
            raise ValueError(f"truncated source blob for {revision}:{path}")
        cursor += 1
    return result


def coordinator_packet_id(batch_id: str, candidate_token: str) -> str:
    return "PCR-" + hashlib.sha256(f"{batch_id}\0{candidate_token}".encode("utf-8")).hexdigest()[:20].upper()


def group_sort_key(batch_id: str) -> str:
    return hashlib.sha256(batch_id.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen re-review package: {output}")

    ledger = load_jsonl(INTEGRATION / "integration_intake_ledger.jsonl")
    selected = [row for row in ledger if row["group_route"] == "SEALED_COORDINATOR_ELIGIBLE"]
    by_group: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in selected:
        if not row["active_return_selected"]:
            raise ValueError(f"coordinator queue contains inactive return: {row['batch_id']}")
        by_group[row["batch_id"]][row["reviewer_lane"]] = row
    if len(by_group) != 832 or any(set(lanes) != {"A", "B"} for lanes in by_group.values()):
        raise ValueError("integration queue does not contain exactly 832 complete A/B coordinator groups")

    blobs_by_commit: dict[str, dict[str, bytes]] = {}
    for commit in sorted({row["source_commit"] for row in selected}):
        paths = [row["source_return_path"] for row in selected if row["source_commit"] == commit]
        blobs_by_commit[commit] = git_blobs(commit, paths)

    protocol = runpy.run_path(str(PROTOCOL))
    g = protocol["expected_packet"].__globals__
    execution = g["verify_execution"]()
    audit = g["verify_audit"]()
    manifest_rows = g["read_jsonl"](g["EXECUTION"] / "unified_prompt_group_batch_manifest.jsonl")
    manifest_by_id = {row["batch_id"]: row for row in manifest_rows}
    if len(manifest_by_id) != 1226:
        raise ValueError("V7 frozen manifest identity/count drift")
    _audit_summary, main_by_id, tail_by_id = audit
    _instruction, rubric, _review_schema, _historical_coordinator_schema = g["reviewer_instruction_and_schema"]()

    amendment_id = "RQ2B-NC-V7-PROMPT-BOUND-COORDINATOR-REREVIEW-2026-09-08-V1"
    coordinator_instruction = (
        "Prospective re-review: resolve only this A/B adequacy disagreement under the supplied frozen adequacy rubric. "
        "Use the supplied target-blind prompt, one complete source-visible candidate, and two sealed assessments. "
        "Do not inspect or infer target identity, gold label, main/tail role, allocation, rank, source path/provenance, "
        "historical/local reference, retrieval outcome, metric, acceptable-set status, or another coordinator's work. "
        "Return only the strict prompt-bound coordinator schema."
    )
    return_fields = {
        "blind_packet_id", "candidate_token", "reviewer_a_return_sha256", "reviewer_b_return_sha256",
        "prompt_render_sha256", "fresh_source_render_sha256", "coordinator_input_packet_sha256",
        "coordinator_decision", "source_anchor", "rationale", "coordinator_output_sha256",
    }
    return_schema = {
        "schema_version": "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_return_v1",
        "prospective_amendment_id": amendment_id,
        "trigger": "Re-review every prior A/B adequacy disagreement using the original target-blind prompt, frozen rubric, validated A/B assessments, and one fresh source-visible candidate.",
        "input_rule": "Read only the assigned prompt-bound packet and this schema. Do not inspect target identity, gold, main/tail role, rank, provenance, historical/local reference, retrieval, outcome, metric, or any other reviewer/coordinator material.",
        "allowed_top_level": sorted(return_fields),
        "required_fields": sorted(return_fields),
        "decisions": ["CONFIRMED_FULLY_ACCEPTABLE", "CONFIRMED_PARTIALLY_ADEQUATE", "CONFIRMED_INADEQUATE", "CONFIRMED_UNCLEAR", "REOPEN_PACKET"],
        "validation": [
            "Output has exactly the allowed fields and copies every supplied hash binding verbatim.",
            "source_anchor is exactly one bounded literal heading or short phrase mechanically located in fresh_source_visible_skill.",
            "coordinator_output_sha256 is SHA-256 of canonical JSON excluding that field (UTF-8, sorted keys, comma/colon separators).",
            "CONFIRMED_UNCLEAR and REOPEN_PACKET block closure; no target join or library update is authorised by this package.",
        ],
    }

    packets_by_group: dict[str, list[dict[str, Any]]] = {}
    admin_rows: list[dict[str, Any]] = []
    for batch_id in sorted(by_group, key=group_sort_key):
        pair = by_group[batch_id]
        returns: dict[str, dict[str, Any]] = {}
        for lane, row in pair.items():
            raw = blobs_by_commit[row["source_commit"]][row["source_return_path"]]
            if sha_bytes(raw) != row["source_return_sha256"]:
                raise ValueError(f"{batch_id}/{lane}: source return hash drift")
            returns[lane] = json.loads(raw)
        manifest = manifest_by_id[batch_id]
        main = main_by_id[manifest["sealed_main_packet"]["packet_id"]]
        tails = [tail_by_id[item["packet_id"]] for item in manifest["sealed_tail_packets"]]
        candidates = list(main["candidates"]) + [candidate for tail in tails for candidate in tail["candidates"]]
        source_by_token = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in candidates}
        assessments_a = {item["candidate_token"]: item for item in returns["A"]["assessments"]}
        assessments_b = {item["candidate_token"]: item for item in returns["B"]["assessments"]}
        if set(assessments_a) != set(source_by_token) or set(assessments_b) != set(source_by_token) or len(source_by_token) != 8:
            raise ValueError(f"{batch_id}: candidate partition drift")
        rows: list[dict[str, Any]] = []
        for token in sorted(source_by_token):
            if assessments_a[token]["adequacy"] == assessments_b[token]["adequacy"] and assessments_a[token]["adequacy"] != "UNCLEAR":
                continue
            source = source_by_token[token]
            input_packet = {
                "prospective_amendment_id": amendment_id,
                "coordinator_dispatch_id": coordinator_packet_id(batch_id, token),
                "blind_packet_id": manifest["blind_packet_id"],
                "candidate_token": token,
                "prompt": main["prompt"],
                "prompt_render_sha256": canonical_sha({"prompt": main["prompt"]}),
                "reviewer_a_return_sha256": pair["A"]["source_return_sha256"],
                "reviewer_b_return_sha256": pair["B"]["source_return_sha256"],
                "reviewer_A_assessment": assessments_a[token],
                "reviewer_B_assessment": assessments_b[token],
                "fresh_source_visible_skill": source,
                "fresh_source_render_sha256": canonical_sha({"candidate_token": token, "source_full_skill": source}),
                "frozen_adequacy_rubric": rubric,
                "coordinator_instruction": coordinator_instruction,
            }
            packet = {**input_packet, "coordinator_input_packet_sha256": canonical_sha(input_packet)}
            if g["keys_deep"](packet) & g["FORBIDDEN_KEYS"]:
                raise ValueError(f"{batch_id}/{token}: prompt-bound coordinator packet blindness drift")
            rows.append(packet)
            admin_rows.append({
                "coordinator_dispatch_id": packet["coordinator_dispatch_id"],
                "batch_id": batch_id,
                "blind_packet_id": manifest["blind_packet_id"],
                "candidate_token": token,
                "packet_sha256": canonical_sha(packet),
            })
        if not rows:
            raise ValueError(f"{batch_id}: disagreement group has no candidate-level trigger")
        packets_by_group[batch_id] = rows
    if len(admin_rows) != 2291:
        raise ValueError(f"expected 2291 candidate-level disagreements, got {len(admin_rows)}")

    assignments: dict[str, list[str]] = {"coordinator_1": [], "coordinator_2": [], "coordinator_3": []}
    loads = {owner: 0 for owner in assignments}
    for batch_id in sorted(packets_by_group, key=group_sort_key):
        owner = min(assignments, key=lambda name: (loads[name], len(assignments[name]), name))
        assignments[owner].append(batch_id)
        loads[owner] += len(packets_by_group[batch_id])

    output.mkdir(parents=True)
    write_json(output / "coordinator_return_schema.json", return_schema)
    admin_by_id = {row["coordinator_dispatch_id"]: row for row in admin_rows}
    for owner, groups in assignments.items():
        packets = [packet for batch_id in groups for packet in packets_by_group[batch_id]]
        reviewer_manifest = [{
            "coordinator_dispatch_id": packet["coordinator_dispatch_id"],
            "blind_packet_id": packet["blind_packet_id"],
            "candidate_token": packet["candidate_token"],
            "packet_sha256": canonical_sha(packet),
        } for packet in packets]
        write_jsonl(output / f"{owner}_reviewer_manifest.jsonl", reviewer_manifest)
        write_jsonl(output / f"{owner}_sealed_packets.jsonl", packets)
        for packet in packets:
            admin_by_id[packet["coordinator_dispatch_id"]]["owner_coordinator"] = owner
    admin_rows.sort(key=lambda row: row["coordinator_dispatch_id"])
    write_jsonl(output / "sealed_admin_assignment_ledger.jsonl", admin_rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_dispatch_v1",
        "status": "PASS_PROSPECTIVE_PROMPT_BOUND_COORDINATOR_REREVIEW_DISPATCH_PENDING_RETURNS",
        "claim_boundary": "Target-blind prospective re-review input only; no coordinator decision, target join, group finalisation, acceptable-set label, retrieval result, metric, or library update.",
        "prospective_amendment_id": amendment_id,
        "bound_inputs": {
            "integration_ledger": str(INTEGRATION.relative_to(WORKSPACE) / "integration_intake_ledger.jsonl"),
            "integration_ledger_sha256": sha_path(INTEGRATION / "integration_intake_ledger.jsonl"),
            "frozen_v7_protocol": str(PROTOCOL.relative_to(WORKSPACE)),
            "frozen_v7_protocol_sha256": sha_path(PROTOCOL),
            "execution_replay_status": execution["status"],
            "execution_replay_sha256": canonical_sha(execution),
        },
        "counts": {
            "rereview_prompt_groups": len(packets_by_group),
            "rereview_candidate_packets": len(admin_rows),
            "coordinator_1_groups": len(assignments["coordinator_1"]), "coordinator_1_packets": loads["coordinator_1"],
            "coordinator_2_groups": len(assignments["coordinator_2"]), "coordinator_2_packets": loads["coordinator_2"],
            "coordinator_3_groups": len(assignments["coordinator_3"]), "coordinator_3_packets": loads["coordinator_3"],
            "historical_gate_docket_groups_not_in_rereview_scope": 6,
        },
        "integrity": {
            "all_selected_return_hashes_replayed": True,
            "all_packets_include_target_blind_original_prompt": True,
            "all_packets_include_frozen_adequacy_rubric": True,
            "all_packets_bind_prompt_source_and_full_input_hash": True,
            "whole_groups_kept_with_one_coordinator": True,
            "assignment_disjoint": True,
            "assignment_covers_every_rereview_group_once": True,
        },
        "historical_evidence_boundary": {
            "preserved_without_overwrite": "rq2b_nc_phase5_v7_sealed_coordinator_dispatch_2026_09_08_v2 and its returns",
            "reason_for_prospective_rereview": "Historical V2 collection contained REOPEN_PACKET outcomes; V1 supplies the target-blind prompt and explicit rubric, then requires new hash-bound returns for every prior disagreement rather than selectively rerunning only reopens.",
        },
        "prohibitions_honoured": ["no target join", "no K change", "no decision substitution", "no acceptable-set or library update"],
    }
    write_json(output / "integrity_report.json", report)
    (output / "integrity_report.md").write_text(
        "# Prompt-bound coordinator re-review dispatch integrity report\n\n"
        f"- Re-review prompt groups: {len(packets_by_group)}\n"
        f"- Candidate-level re-review packets: {len(admin_rows)}\n"
        f"- Coordinator 1: {len(assignments['coordinator_1'])} groups / {loads['coordinator_1']} packets\n"
        f"- Coordinator 2: {len(assignments['coordinator_2'])} groups / {loads['coordinator_2']} packets\n"
        f"- Coordinator 3: {len(assignments['coordinator_3'])} groups / {loads['coordinator_3']} packets\n\n"
        "All historical V2 returns remain immutable. This is a target-blind prospective re-review of every prior disagreement, not a selective re-review of only reopened packets. The six historical gate-docket groups are excluded and remain separately traceable.\n",
        encoding="utf-8",
    )
    (output / "PROSPECTIVE_AMENDMENT.md").write_text(
        "# Prospective amendment: prompt-bound coordinator re-review\n\n"
        "## Why this amendment exists\n\n"
        "Historical V2 coordinator packets provided two sealed A/B assessments and one source-visible candidate. V2 evidence remains preserved, but `REOPEN_PACKET` outcomes demonstrated that this input did not always support a unique adequacy resolution. This amendment does not overwrite or reinterpret V2.\n\n"
        "## What changes\n\n"
        "Every re-review packet adds the original V7 target-blind prompt and the frozen adequacy rubric. The return schema binds the prompt render, fresh source render, both selected independent-return hashes, and a hash of the complete coordinator input packet.\n\n"
        "## Scope and safeguards\n\n"
        "All 832 prior disagreement groups and all 2,291 candidate-level disagreement packets are re-reviewed, so the amendment does not cherry-pick historical reopens. Each group stays whole and is assigned to exactly one coordinator. Coordinators receive no target identity, gold label, source path/provenance, rank, main/tail role, retrieval outcome, metric, acceptable-set status, admin ledger, or peer coordinator material. The six historical gate-docket groups remain outside this scope.\n\n"
        "## What this does not authorise\n\n"
        "This package does not authorise a target join, group finalisation, acceptable-set creation, library change, K change, retrieval run, metric, or thesis result update. Those require later gates under the master SOP.\n",
        encoding="utf-8",
    )
    (output / "README.md").write_text(
        "# RQ2b-NC V7 prompt-bound coordinator re-review\n\n"
        "Each coordinator reads only its own `*_sealed_packets.jsonl`, own reviewer manifest, and `coordinator_return_schema.json`. It must not inspect the admin ledger, historical V2 packets/returns, target join, rank, main/tail role, provenance, retrieval outcome, acceptable-set artifact, or another coordinator's files.\n\n"
        "For every manifest row, create exactly one strict-schema return named by `coordinator_dispatch_id` in the coordinator-specific return directory. Copy all supplied hash bindings verbatim. Use one literal source anchor from the supplied skill. `REOPEN_PACKET` or `CONFIRMED_UNCLEAR` is required when the sealed packet does not support a defensible resolution.\n\n"
        "This is prospective target-blind review input only. It does not finalise any group or update the library.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(output), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
