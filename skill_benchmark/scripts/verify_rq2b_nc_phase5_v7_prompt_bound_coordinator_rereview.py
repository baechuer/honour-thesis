#!/usr/bin/env python3
"""Validate prompt-bound coordinator re-review returns against their frozen dispatch."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_2026_09_08_v1"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-prompt-bound-coordinator-rereview-2026-09-08-v1"


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


def load_expected(dispatch: Path) -> tuple[set[str], set[str], dict[str, tuple[str, dict[str, Any]]]]:
    schema = json.loads((dispatch / "coordinator_return_schema.json").read_text(encoding="utf-8"))
    required, decisions = set(schema["required_fields"]), set(schema["decisions"])
    expected: dict[str, tuple[str, dict[str, Any]]] = {}
    packet_fields = {
        "prospective_amendment_id", "coordinator_dispatch_id", "blind_packet_id", "candidate_token",
        "prompt", "prompt_render_sha256", "reviewer_a_return_sha256", "reviewer_b_return_sha256",
        "reviewer_A_assessment", "reviewer_B_assessment", "fresh_source_visible_skill",
        "fresh_source_render_sha256", "frozen_adequacy_rubric", "coordinator_instruction",
        "coordinator_input_packet_sha256",
    }
    for owner in ("coordinator_1", "coordinator_2", "coordinator_3"):
        manifest = load_jsonl(dispatch / f"{owner}_reviewer_manifest.jsonl")
        packets = load_jsonl(dispatch / f"{owner}_sealed_packets.jsonl")
        by_id = {packet["coordinator_dispatch_id"]: packet for packet in packets}
        if len(by_id) != len(packets) or len(manifest) != len(packets):
            raise ValueError(f"{owner}: reviewer dispatch cardinality drift")
        for row in manifest:
            packet = by_id.get(row.get("coordinator_dispatch_id"))
            if packet is None or row.get("packet_sha256") != canonical_sha(packet):
                raise ValueError(f"{owner}: reviewer manifest packet-hash drift")
            if set(packet) != packet_fields:
                raise ValueError(f"{owner}: prompt-bound packet schema drift")
            packet_without_input_hash = {key: value for key, value in packet.items() if key != "coordinator_input_packet_sha256"}
            if packet["coordinator_input_packet_sha256"] != canonical_sha(packet_without_input_hash):
                raise ValueError(f"{owner}: packet-input hash drift")
            if packet["prompt_render_sha256"] != canonical_sha({"prompt": packet["prompt"]}):
                raise ValueError(f"{owner}: prompt-render hash drift")
            if packet["fresh_source_render_sha256"] != canonical_sha({
                "candidate_token": packet["candidate_token"], "source_full_skill": packet["fresh_source_visible_skill"],
            }):
                raise ValueError(f"{owner}: fresh-source hash drift")
            dispatch_id = packet["coordinator_dispatch_id"]
            if dispatch_id in expected:
                raise ValueError("cross-coordinator overlap")
            expected[dispatch_id] = (owner, packet)
    if len(expected) != 2291:
        raise ValueError(f"expected 2291 re-review packets, got {len(expected)}")
    return required, decisions, expected


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
    if returned["coordinator_output_sha256"] != canonical_sha({
        key: value for key, value in returned.items() if key != "coordinator_output_sha256"
    }):
        return "coordinator-output hash drift"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dispatch", type=Path, default=DISPATCH)
    parser.add_argument("--return-root", type=Path, default=RETURN_ROOT)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    required, decisions, expected = load_expected(args.dispatch.resolve())
    return_root = args.return_root.resolve()
    valid: list[str] = []
    missing: list[str] = []
    invalid: dict[str, str] = {}
    unexpected: list[str] = []
    for dispatch_id, (owner, packet) in expected.items():
        path = return_root / owner / f"{dispatch_id}.json"
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
            valid.append(dispatch_id)
    if return_root.is_dir():
        for path in return_root.glob("coordinator_*/*.json"):
            if path.stem not in expected or path.parent.name != expected[path.stem][0]:
                unexpected.append(str(path))
    status = (
        "PASS_V7_PROMPT_BOUND_COORDINATOR_REREVIEW_RETURNS_COMPLETE"
        if not missing and not invalid and not unexpected
        else "PASS_V7_PROMPT_BOUND_COORDINATOR_REREVIEW_RETURNS_PARTIAL"
        if args.allow_incomplete and not invalid and not unexpected
        else "FAIL_V7_PROMPT_BOUND_COORDINATOR_REREVIEW_RETURN_VALIDATION"
    )
    print(json.dumps({
        "status": status,
        "dispatch": str(args.dispatch.resolve()),
        "expected_packets": len(expected),
        "valid_returns": len(valid),
        "missing_returns": len(missing),
        "invalid_returns": invalid,
        "unexpected_return_paths": unexpected,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    if status.startswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
