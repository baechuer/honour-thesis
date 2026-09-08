#!/usr/bin/env python3
"""Validate sealed coordinator returns for the V7 gate-reissue disagreement queue."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_sealed_coordinator_2026_09_08_v1"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-gate-reissue-sealed-coordinator-2026-09-08-v1" / "gate_reissue_coordinator"


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def normalised_text(value: str) -> str:
    return " ".join(value.replace("#", " ").casefold().split())


def valid_anchor(anchor: Any, source: str) -> bool:
    if not isinstance(anchor, str) or ";" in anchor:
        return False
    normal = normalised_text(anchor)
    return 4 <= len(normal) <= 160 and normal in normalised_text(source)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def load_expected(dispatch: Path) -> tuple[dict[str, dict[str, Any]], set[str], set[str]]:
    schema = json.loads((dispatch / "coordinator_return_schema.json").read_text(encoding="utf-8"))
    required, decisions = set(schema["required_fields"]), set(schema["decisions"])
    rows = load_jsonl(dispatch / "coordinator_reviewer_manifest.jsonl")
    packets = load_jsonl(dispatch / "coordinator_sealed_packets.jsonl")
    expected = {row["coordinator_dispatch_id"]: row for row in packets}
    packet_fields = {
        "coordinator_dispatch_id", "blind_packet_id", "candidate_token", "prompt", "prompt_render_sha256",
        "reviewer_a_return_sha256", "reviewer_b_return_sha256", "reviewer_A_assessment", "reviewer_B_assessment",
        "fresh_source_visible_skill", "fresh_source_render_sha256", "frozen_adequacy_rubric", "coordinator_instruction",
        "coordinator_input_packet_sha256",
    }
    if len(expected) != 9 or len(rows) != 9 or len({row["coordinator_dispatch_id"] for row in rows}) != 9:
        raise ValueError("coordinator dispatch cardinality drift")
    for row in rows:
        packet = expected.get(row.get("coordinator_dispatch_id"))
        if packet is None or row.get("packet_sha256") != canonical_sha(packet):
            raise ValueError("coordinator reviewer-manifest packet hash drift")
    for packet in expected.values():
        if set(packet) != packet_fields:
            raise ValueError("coordinator sealed packet schema drift")
        without_input_hash = {key: value for key, value in packet.items() if key != "coordinator_input_packet_sha256"}
        if packet["coordinator_input_packet_sha256"] != canonical_sha(without_input_hash):
            raise ValueError("coordinator input hash drift")
        if packet["prompt_render_sha256"] != canonical_sha({"prompt": packet["prompt"]}):
            raise ValueError("coordinator prompt render hash drift")
        if packet["fresh_source_render_sha256"] != canonical_sha({"candidate_token": packet["candidate_token"], "source_full_skill": packet["fresh_source_visible_skill"]}):
            raise ValueError("coordinator source render hash drift")
    return expected, required, decisions


def validate_return(returned: Any, packet: dict[str, Any], required: set[str], decisions: set[str]) -> str | None:
    if not isinstance(returned, dict) or set(returned) != required:
        return "return schema drift"
    for key in (
        "blind_packet_id", "candidate_token", "reviewer_a_return_sha256", "reviewer_b_return_sha256",
        "prompt_render_sha256", "fresh_source_render_sha256", "coordinator_input_packet_sha256",
    ):
        if returned[key] != packet[key]:
            return f"binding drift: {key}"
    if returned["coordinator_decision"] not in decisions:
        return "unsupported coordinator decision"
    if not isinstance(returned["rationale"], str) or not returned["rationale"].strip():
        return "empty rationale"
    if not valid_anchor(returned["source_anchor"], packet["fresh_source_visible_skill"]):
        return "source-anchor drift"
    if returned["coordinator_output_sha256"] != canonical_sha({key: value for key, value in returned.items() if key != "coordinator_output_sha256"}):
        return "coordinator output-hash drift"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dispatch", type=Path, default=DISPATCH)
    parser.add_argument("--return-root", type=Path, default=RETURN_ROOT)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    expected, required, decisions = load_expected(args.dispatch.resolve())
    root = args.return_root.resolve()
    valid: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    invalid: dict[str, str] = {}
    for dispatch_id, packet in expected.items():
        path = root / f"{dispatch_id}.json"
        if not path.is_file():
            missing.append(dispatch_id)
            continue
        try:
            returned = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            invalid[dispatch_id] = f"unreadable JSON: {exc}"
            continue
        problem = validate_return(returned, packet, required, decisions)
        if problem:
            invalid[dispatch_id] = problem
        else:
            valid[dispatch_id] = returned
    unexpected = sorted(str(path) for path in root.glob("*.json") if path.stem not in expected) if root.is_dir() else []
    rationale_locations: dict[str, list[str]] = defaultdict(list)
    for dispatch_id, returned in valid.items():
        rationale_locations[returned["rationale"]].append(dispatch_id)
    duplicate_rationales = {text: ids for text, ids in rationale_locations.items() if len(ids) > 1}
    closure_blockers = sorted(dispatch_id for dispatch_id, returned in valid.items() if returned["coordinator_decision"] in {"CONFIRMED_UNCLEAR", "REOPEN_PACKET"})
    status = (
        "PASS_V7_GATE_REISSUE_COORDINATOR_RETURNS_COMPLETE"
        if not missing and not invalid and not unexpected and not duplicate_rationales
        else "PASS_V7_GATE_REISSUE_COORDINATOR_RETURNS_PARTIAL"
        if args.allow_incomplete and not invalid and not unexpected and not duplicate_rationales
        else "FAIL_V7_GATE_REISSUE_COORDINATOR_RETURN_VALIDATION"
    )
    print(json.dumps({
        "status": status,
        "dispatch": str(args.dispatch.resolve()),
        "expected_returns": len(expected),
        "valid_returns": len(valid),
        "missing_returns": sorted(missing),
        "invalid_returns": invalid,
        "unexpected_return_paths": unexpected,
        "duplicate_rationales": duplicate_rationales,
        "closure_blockers": closure_blockers,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    if status.startswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
