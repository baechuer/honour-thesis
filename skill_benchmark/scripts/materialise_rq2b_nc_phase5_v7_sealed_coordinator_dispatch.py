#!/usr/bin/env python3
"""Materialise the target-blind Phase-5 V7 sealed-coordinator dispatch.

This script consumes only the mechanically validated active-return pointers in
the V7 integration ledger.  It emits coordinator packets for existing A/B
adequacy disagreements.  It neither resolves a disagreement nor opens a target
join, acceptable set, tail role, retrieval result, or library update.
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
# V1 is a preserved, immutable historical dispatch.  V2 binds the two selected
# input-return hashes directly into every reviewer-visible packet, as required
# by the frozen coordinator schema.
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_sealed_coordinator_dispatch_2026_09_08_v2"


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


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
        size = int(header[2]); result[path] = process.stdout[cursor:cursor + size]
        cursor += size
        if process.stdout[cursor:cursor + 1] != b"\n":
            raise ValueError(f"truncated source blob for {revision}:{path}")
        cursor += 1
    return result


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def coordinator_packet_id(batch_id: str, candidate_token: str) -> str:
    return "SC-" + hashlib.sha256(f"{batch_id}\0{candidate_token}".encode("utf-8")).hexdigest()[:20].upper()


def group_sort_key(batch_id: str) -> str:
    return hashlib.sha256(batch_id.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise SystemExit(f"refusing to overwrite frozen dispatch package: {out}")

    ledger = load_jsonl(INTEGRATION / "integration_intake_ledger.jsonl")
    selected = [row for row in ledger if row["group_route"] == "SEALED_COORDINATOR_ELIGIBLE"]
    by_group: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in selected:
        if not row["active_return_selected"]:
            raise ValueError(f"coordinator queue contains inactive return: {row['batch_id']}")
        by_group[row["batch_id"]][row["reviewer_lane"]] = row
    if len(by_group) != 832 or any(set(lanes) != {"A", "B"} for lanes in by_group.values()):
        raise ValueError("integration queue does not contain exactly 832 complete active A/B groups")

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
    if len(manifest_rows) != 1226 or len(manifest_by_id) != 1226:
        raise ValueError("V7 frozen manifest count/identity drift")
    _audit_summary, main_by_id, tail_by_id = audit
    _instruction, _rubric, _review_schema, coordinator_schema = g["reviewer_instruction_and_schema"]()
    coordinator_instruction = (
        "Resolve only this A/B adequacy disagreement under the frozen rubric. "
        "Do not inspect targets, main/tail role, allocation, rank, source path/provenance, "
        "historical/local reference, retrieval outcome or metric. Return only the strict coordinator schema."
    )

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
        a = {item["candidate_token"]: item for item in returns["A"]["assessments"]}
        b = {item["candidate_token"]: item for item in returns["B"]["assessments"]}
        if set(a) != set(source_by_token) or set(b) != set(source_by_token) or len(source_by_token) != 8:
            raise ValueError(f"{batch_id}: candidate partition drift")
        rows: list[dict[str, Any]] = []
        for token in sorted(source_by_token):
            if a[token]["adequacy"] == b[token]["adequacy"] and a[token]["adequacy"] != "UNCLEAR":
                continue
            source = source_by_token[token]
            packet = {
                "coordinator_dispatch_id": coordinator_packet_id(batch_id, token),
                "blind_packet_id": manifest["blind_packet_id"],
                "candidate_token": token,
                "reviewer_a_return_sha256": pair["A"]["source_return_sha256"],
                "reviewer_b_return_sha256": pair["B"]["source_return_sha256"],
                "reviewer_A_assessment": a[token],
                "reviewer_B_assessment": b[token],
                "fresh_source_visible_skill": source,
                "fresh_source_render_sha256": canonical_sha({"candidate_token": token, "source_full_skill": source}),
                "coordinator_instruction": coordinator_instruction,
            }
            # Any failure here is an information-leakage or contract defect;
            # do not dispatch partial work.
            if g["keys_deep"](packet) & g["FORBIDDEN_KEYS"]:
                raise ValueError(f"{batch_id}/{token}: coordinator packet blindness drift")
            rows.append(packet)
            admin_rows.append({
                "coordinator_dispatch_id": packet["coordinator_dispatch_id"], "batch_id": batch_id,
                "blind_packet_id": manifest["blind_packet_id"], "candidate_token": token,
                "packet_sha256": canonical_sha(packet), "reviewer_A_return_sha256": pair["A"]["source_return_sha256"],
                "reviewer_B_return_sha256": pair["B"]["source_return_sha256"],
            })
        if not rows:
            raise ValueError(f"{batch_id}: coordinator-eligible group has no disagreement")
        packets_by_group[batch_id] = rows
    if len(admin_rows) != 2291:
        raise ValueError(f"expected 2291 candidate-level disagreements, got {len(admin_rows)}")

    # Keep a whole group with one coordinator. SHA ordering is deterministic;
    # greedy assignment by candidate load avoids a misleading equal-group but
    # unequal-workload split.
    assignments: dict[str, list[str]] = {"coordinator_1": [], "coordinator_2": [], "coordinator_3": []}
    loads = {name: 0 for name in assignments}
    for batch_id in sorted(packets_by_group, key=group_sort_key):
        owner = min(assignments, key=lambda name: (loads[name], len(assignments[name]), name))
        assignments[owner].append(batch_id)
        loads[owner] += len(packets_by_group[batch_id])

    out.mkdir(parents=True)
    write_json(out / "coordinator_return_schema.json", coordinator_schema)
    admin_by_id = {row["coordinator_dispatch_id"]: row for row in admin_rows}
    for owner, groups in assignments.items():
        packets = [packet for batch_id in groups for packet in packets_by_group[batch_id]]
        reviewer_manifest = [{
            "coordinator_dispatch_id": packet["coordinator_dispatch_id"],
            "blind_packet_id": packet["blind_packet_id"], "candidate_token": packet["candidate_token"],
            "packet_sha256": canonical_sha(packet),
        } for packet in packets]
        write_jsonl(out / f"{owner}_reviewer_manifest.jsonl", reviewer_manifest)
        write_jsonl(out / f"{owner}_sealed_packets.jsonl", packets)
        for packet in packets:
            admin_by_id[packet["coordinator_dispatch_id"]]["owner_coordinator"] = owner
    admin_rows.sort(key=lambda row: row["coordinator_dispatch_id"])
    write_jsonl(out / "sealed_admin_assignment_ledger.jsonl", admin_rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_sealed_coordinator_dispatch_v2",
        "claim_boundary": "Target-blind coordinator input dispatch only; no coordinator decisions, reconciliation finalisation, target join, acceptable set, retrieval, metric, or library update.",
        "bound_inputs": {
            "integration_ledger": str(INTEGRATION.relative_to(WORKSPACE) / "integration_intake_ledger.jsonl"),
            "integration_ledger_sha256": sha_path(INTEGRATION / "integration_intake_ledger.jsonl"),
            "frozen_protocol": str(PROTOCOL.relative_to(WORKSPACE)),
            "frozen_protocol_sha256": sha_path(PROTOCOL),
            "execution_replay_status": execution["status"],
            "execution_replay_sha256": canonical_sha(execution),
        },
        "counts": {
            "eligible_prompt_groups": len(packets_by_group), "candidate_level_coordinator_packets": len(admin_rows),
            "coordinator_1_groups": len(assignments["coordinator_1"]), "coordinator_1_packets": loads["coordinator_1"],
            "coordinator_2_groups": len(assignments["coordinator_2"]), "coordinator_2_packets": loads["coordinator_2"],
            "coordinator_3_groups": len(assignments["coordinator_3"]), "coordinator_3_packets": loads["coordinator_3"],
            "excluded_gate_docket_groups": 6,
        },
        "integrity": {"all_input_return_hashes_replayed": True, "all_packets_target_blind": True, "whole_groups_kept_with_one_coordinator": True, "assignment_disjoint": True, "assignment_covers_every_eligible_group_once": True},
        "v1_supersession": {
            "supersedes": "rq2b_nc_phase5_v7_sealed_coordinator_dispatch_2026_09_08_v1",
            "reason": "V1 packets omitted reviewer_a_return_sha256 and reviewer_b_return_sha256, which are required immutable bindings in the frozen coordinator return schema. V1 is retained unchanged and must not be used for returns.",
            "all_v2_packets_include_required_input_return_hash_bindings": True,
        },
        "prohibitions_honoured": ["no target join", "no K change", "no reconciliation decision", "no acceptable-set or library update"],
    }
    write_json(out / "integrity_report.json", report)
    (out / "integrity_report.md").write_text(
        "# Sealed coordinator dispatch integrity report (V2)\n\n"
        f"- Eligible prompt groups: {len(packets_by_group)}\n"
        f"- Candidate-level packets: {len(admin_rows)}\n"
        f"- Coordinator 1: {len(assignments['coordinator_1'])} groups / {loads['coordinator_1']} packets\n"
        f"- Coordinator 2: {len(assignments['coordinator_2'])} groups / {loads['coordinator_2']} packets\n"
        f"- Coordinator 3: {len(assignments['coordinator_3'])} groups / {loads['coordinator_3']} packets\n\n"
        "The six gate-docket groups are not dispatched. No return or decision is materialised here.\n\n"
        "V2 supersedes V1 for coordinator review only: V1 omitted the two reviewer-return SHA bindings required by the frozen coordinator schema. V1 remains preserved unchanged; its packets must not be used to create returns.\n", encoding="utf-8")
    (out / "README.md").write_text(
        "# RQ2b-NC V7 sealed coordinator dispatch (V2)\n\n"
        "Each coordinator receives only its `*_sealed_packets.jsonl`, its reviewer manifest, and `coordinator_return_schema.json`. It must not inspect the admin ledger, any target join, main/tail role, rank, provenance, historical label, retrieval outcome, or another coordinator's packet file.\n\n"
        "For every packet, write one strict-schema return to a coordinator-specific return directory, naming the file by `coordinator_dispatch_id`. The return itself contains only the frozen coordinator schema fields; the dispatch ID is transport metadata and must not be inserted into the return JSON. Copy `reviewer_a_return_sha256`, `reviewer_b_return_sha256`, and `fresh_source_render_sha256` verbatim from the supplied packet.\n\n"
        "V2 is the only active coordinator dispatch. The preserved V1 package omitted the two required input-return SHA bindings and therefore must not be used to create coordinator returns.\n\n"
        "These inputs are target-blind. They are not decisions, finalised groups, acceptable sets, or experimental results.\n", encoding="utf-8")
    (out / "U0323_method_gate_note.md").write_text(
        "# U0323 method gate\n\n"
        "`U0323` is excluded from the V2 coordinator dispatch. Its existing sealed coordinator rationale records materially incompatible requested workflows, not a malformed anchor, schema, or packet hash. Therefore a same-packet A+B reissue would not repair a mechanical defect. The original evidence remains preserved; any next action requires an explicit prospective method amendment or an explicit defer/exclude decision. This note contains no target identity or reconciliation decision.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS_V7_SEALED_COORDINATOR_DISPATCH_MATERIALISED", "output": str(out), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
