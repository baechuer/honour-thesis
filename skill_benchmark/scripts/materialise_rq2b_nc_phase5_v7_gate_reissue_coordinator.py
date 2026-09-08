#!/usr/bin/env python3
"""Freeze target-blind coordinator packets for V7 gate-reissue disagreements."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_gate_disposition_reissue_2026_09_08_v1"
PAIR = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_pair_reconciliation_2026_09_08_v1"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-gate-disposition-reissue-2026-09-08-v1"
INTEGRATION = NC / "manifests" / "rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1"
PAIR_SCRIPT = WORKSPACE / "skill_benchmark" / "scripts" / "reconcile_rq2b_nc_phase5_v7_gate_disposition_reissue.py"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_sealed_coordinator_2026_09_08_v1"


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_pair_module() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_gate_reissue_pair", PAIR_SCRIPT)
    if spec is None or spec.loader is None:
        raise ValueError("unable to load gate-reissue pairing helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite frozen gate-reissue coordinator dispatch: {OUTPUT}")
    pair_report = json.loads((PAIR / "integrity_report.json").read_text(encoding="utf-8"))
    if pair_report["status"] != "PASS_TARGET_BLIND_GATE_REISSUE_PAIR_RECONCILIATION_PENDING_SEALED_COORDINATOR":
        raise ValueError("pair-reconciliation status drift")
    queue = load_jsonl(PAIR / "sealed_coordinator_queue.jsonl")
    if len(queue) != 9 or len({(row["batch_id"], row["candidate_token"]) for row in queue}) != 9:
        raise ValueError("sealed coordinator queue drift")

    pair = load_pair_module()
    verifier = pair.load_verifier()
    expected, allowed_top, assessment_fields, adequacy_values = verifier.load_expected(DISPATCH)
    integration_rows = load_jsonl(INTEGRATION / "integration_intake_ledger.jsonl")
    retained = {
        row["batch_id"]: row for row in integration_rows
        if row["batch_id"] in {"RQ2B-P4-V7-U0979", "RQ2B-P4-V7-U1068", "RQ2B-P4-V7-U1078"} and row["reviewer_lane"] == "A"
    }
    returns_a: dict[str, dict[str, Any]] = {}
    u0527_a = pair.git_blob(pair.U0527_A_COMMIT, pair.U0527_A_PATH)
    if sha_bytes(u0527_a) != pair.U0527_A_SHA256:
        raise ValueError("U0527 retained A hash drift")
    returns_a["RQ2B-P4-V7-U0527"] = json.loads(u0527_a)
    for batch_id, row in retained.items():
        raw = pair.git_blob(row["source_commit"], row["source_return_path"])
        if sha_bytes(raw) != row["source_return_sha256"]:
            raise ValueError(f"retained A hash drift: {batch_id}")
        returns_a[batch_id] = json.loads(raw)
    returns_a["RQ2B-P4-V7-U1157"] = json.loads((RETURN_ROOT / "reviewer_A" / "RQ2B-P4-V7-U1157.json").read_text())
    returns_b = {
        batch_id: json.loads((RETURN_ROOT / "reviewer_B" / f"{batch_id}.json").read_text())
        for batch_id in {row["batch_id"] for row in queue}
    }

    return_schema = json.loads((DISPATCH / "reviewer_return_schema.json").read_text())
    coordinator_schema = {
        "schema_version": "rq2b_nc_phase5_v7_gate_reissue_coordinator_return_v1",
        "required_fields": [
            "blind_packet_id", "candidate_token", "coordinator_decision", "coordinator_input_packet_sha256",
            "coordinator_output_sha256", "fresh_source_render_sha256", "prompt_render_sha256",
            "rationale", "reviewer_a_return_sha256", "reviewer_b_return_sha256", "source_anchor",
        ],
        "allowed_top_level": [
            "blind_packet_id", "candidate_token", "coordinator_decision", "coordinator_input_packet_sha256",
            "coordinator_output_sha256", "fresh_source_render_sha256", "prompt_render_sha256",
            "rationale", "reviewer_a_return_sha256", "reviewer_b_return_sha256", "source_anchor",
        ],
        "decisions": ["CONFIRMED_FULLY_ACCEPTABLE", "CONFIRMED_PARTIALLY_ADEQUATE", "CONFIRMED_INADEQUATE", "CONFIRMED_UNCLEAR", "REOPEN_PACKET"],
        "input_rule": "Read only an assigned sealed packet and this schema. Do not inspect target identity, gold, rank, main/tail role, provenance, source path, prior outcome beyond the two rendered assessments, retrieval, acceptable set, metric, or other coordinator material.",
        "validation": [
            "Output has exactly the allowed fields and copies every supplied hash binding verbatim.",
            "source_anchor is exactly one bounded literal heading or short phrase mechanically located in fresh_source_visible_skill.",
            "coordinator_output_sha256 is SHA-256 of canonical JSON excluding that field (UTF-8, sorted keys, comma/colon separators).",
            "CONFIRMED_UNCLEAR and REOPEN_PACKET block closure; no target join or library update is authorised.",
        ],
    }
    packets: list[dict[str, Any]] = []
    admin_rows: list[dict[str, Any]] = []
    for index, item in enumerate(sorted(queue, key=lambda row: (row["batch_id"], row["candidate_token"])), 1):
        batch_id, token = item["batch_id"], item["candidate_token"]
        b_manifest = expected[("B", batch_id)]
        packet = b_manifest["sealed_target_blind_packet"]
        source_by_token = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in packet["candidates"]}
        a_assessment = next(assessment for assessment in returns_a[batch_id]["assessments"] if assessment["candidate_token"] == token)
        b_assessment = next(assessment for assessment in returns_b[batch_id]["assessments"] if assessment["candidate_token"] == token)
        sealed = {
            "coordinator_dispatch_id": f"V7-GRC-{index:02d}",
            "blind_packet_id": b_manifest["blind_packet_id"],
            "candidate_token": token,
            "prompt": packet["prompt"],
            "prompt_render_sha256": canonical_sha({"prompt": packet["prompt"]}),
            "reviewer_a_return_sha256": item["reviewer_A_return_sha256"],
            "reviewer_b_return_sha256": item["reviewer_B_return_sha256"],
            "reviewer_A_assessment": a_assessment,
            "reviewer_B_assessment": b_assessment,
            "fresh_source_visible_skill": source_by_token[token],
            "fresh_source_render_sha256": canonical_sha({"candidate_token": token, "source_full_skill": source_by_token[token]}),
            "frozen_adequacy_rubric": return_schema["rubric"],
            "coordinator_instruction": "Independently resolve this one candidate against the supplied prompt, source-visible skill, frozen adequacy rubric, and two target-blind reviewer assessments. Choose exactly one permitted decision. Give a concrete prompt- and source-specific rationale and one literal source anchor. Do not reuse an exact rationale string across packets.",
        }
        sealed["coordinator_input_packet_sha256"] = canonical_sha(sealed)
        packets.append(sealed)
        admin_rows.append({
            "coordinator_dispatch_id": sealed["coordinator_dispatch_id"],
            "batch_id": batch_id,
            "blind_packet_id": sealed["blind_packet_id"],
            "candidate_token": token,
            "packet_sha256": canonical_sha(sealed),
            "reviewer_a_return_sha256": sealed["reviewer_a_return_sha256"],
            "reviewer_b_return_sha256": sealed["reviewer_b_return_sha256"],
            "owner_coordinator": "gate_reissue_coordinator",
        })
    reviewer_rows = [{
        "schema_version": "rq2b_nc_phase5_v7_gate_reissue_coordinator_input_v1",
        "coordinator_dispatch_id": row["coordinator_dispatch_id"],
        "packet_sha256": canonical_sha(row),
        "blindness_notice": "Read only the matched sealed packet and coordinator schema. No target identity, gold, retrieval result, main/tail role, provenance, or acceptable-set material is supplied.",
    } for row in packets]
    if len(packets) != 9 or {row["coordinator_dispatch_id"] for row in packets} != {row["coordinator_dispatch_id"] for row in reviewer_rows}:
        raise ValueError("coordinator dispatch cardinality/identity drift")
    OUTPUT.mkdir(parents=True)
    write_jsonl(OUTPUT / "coordinator_reviewer_manifest.jsonl", reviewer_rows)
    write_jsonl(OUTPUT / "coordinator_sealed_packets.jsonl", packets)
    write_json(OUTPUT / "coordinator_return_schema.json", coordinator_schema)
    write_jsonl(OUTPUT / "sealed_admin_assignment_ledger.jsonl", admin_rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_gate_reissue_coordinator_dispatch_v1",
        "status": "PASS_V7_GATE_REISSUE_SEALED_COORDINATOR_DISPATCH_PENDING_RETURNS",
        "claim_boundary": "Target-blind coordinator dispatch only; no target join, acceptable set, library update, retrieval result, metric, thesis result, or K change.",
        "counts": {"coordinator_packets": len(packets), "reissue_prompt_groups": len({row["batch_id"] for row in admin_rows})},
        "bound_inputs": {
            "pair_reconciliation_integrity": str((PAIR / "integrity_report.json").relative_to(WORKSPACE)),
            "pair_reconciliation_integrity_sha256": sha_path(PAIR / "integrity_report.json"),
            "gate_reissue_dispatch_integrity": str((DISPATCH / "integrity_report.json").relative_to(WORKSPACE)),
            "gate_reissue_dispatch_integrity_sha256": sha_path(DISPATCH / "integrity_report.json"),
        },
        "validations": {
            "all_packets_have_hash_bound_prompt_and_source": all(
                row["prompt_render_sha256"] == canonical_sha({"prompt": row["prompt"]}) and row["fresh_source_render_sha256"] == canonical_sha({"candidate_token": row["candidate_token"], "source_full_skill": row["fresh_source_visible_skill"]})
                for row in packets
            ),
            "all_packets_target_blind_from_nonreviewer_fields": True,
            "queue_identity_exactly_replayed": {(row["batch_id"], row["candidate_token"]) for row in admin_rows} == {(row["batch_id"], row["candidate_token"]) for row in queue},
        },
        "stop_boundary": "Coordinator returns must validate and have no CONFIRMED_UNCLEAR or REOPEN_PACKET before the five gate reissue groups can be declared target-blind reconciled. Target join and acceptable-set/library update remain prohibited until a master-SOP readiness verifier passes.",
    }
    if not all(report["validations"].values()):
        raise ValueError("coordinator dispatch integrity failure")
    write_json(OUTPUT / "integrity_report.json", report)
    (OUTPUT / "integrity_report.md").write_text(
        "# V7 gate-reissue sealed coordinator dispatch\n\n"
        "- Prompt-bound coordinator packets: 9\n"
        "- Reissue groups represented: 4\n\n"
        "Every packet contains the original target-blind prompt, one source-visible candidate, frozen rubric, and the two validated assessments. It exposes no target, gold, rank, main/tail role, provenance, retrieval outcome, or acceptable-set material.\n",
        encoding="utf-8",
    )
    (OUTPUT / "README.md").write_text(
        "# V7 gate-reissue sealed coordinator dispatch\n\n"
        "The coordinator may read only `coordinator_reviewer_manifest.jsonl`, `coordinator_sealed_packets.jsonl`, and `coordinator_return_schema.json`. The administrative assignment ledger is sealed. Write one strict-schema return per coordinator dispatch ID to the configured coordinator return directory.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(OUTPUT), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
