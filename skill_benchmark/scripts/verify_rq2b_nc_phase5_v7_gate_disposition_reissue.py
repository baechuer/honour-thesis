#!/usr/bin/env python3
"""Validate user-approved V7 gate reissue returns before reconciliation."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
DISPATCH = NC / "manifests" / "rq2b_nc_phase5_v7_gate_disposition_reissue_2026_09_08_v1"
RETURN_ROOT = NC / "review" / "RQ2B-NC-phase5-v7-gate-disposition-reissue-2026-09-08-v1"


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalised_text(value: str) -> str:
    return " ".join(value.replace("#", " ").casefold().split())


def valid_anchor(anchor: Any, source: str) -> bool:
    if not isinstance(anchor, str) or ";" in anchor:
        return False
    normal = normalised_text(anchor)
    return 4 <= len(normal) <= 160 and normal in normalised_text(source)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def load_expected(dispatch: Path) -> tuple[dict[tuple[str, str], dict[str, Any]], set[str], set[str], set[str]]:
    schema = json.loads((dispatch / "reviewer_return_schema.json").read_text(encoding="utf-8"))
    allowed_top = set(schema["allowed_top_level"])
    assessment_fields = set(schema["allowed_assessment_fields"])
    adequacy_values = set(schema["adequacy_values"])
    expected: dict[tuple[str, str], dict[str, Any]] = {}
    packet_fields = {"blind_packet_id", "prompt", "candidates", "review_instruction"}
    for lane in ("A", "B"):
        rows = load_jsonl(dispatch / f"reviewer_{lane}_reissue_manifest.jsonl")
        for row in rows:
            key = (lane, row.get("batch_id"))
            packet = row.get("sealed_target_blind_packet")
            if not isinstance(key[1], str) or key in expected or not isinstance(packet, dict):
                raise ValueError("reviewer reissue manifest identity drift")
            if set(packet) != packet_fields or packet.get("blind_packet_id") != row.get("blind_packet_id"):
                raise ValueError(f"packet identity/schema drift: {key}")
            candidates = packet.get("candidates")
            if not isinstance(candidates, list) or len(candidates) != 8:
                raise ValueError(f"packet candidate cardinality drift: {key}")
            tokens = [candidate.get("candidate_token") for candidate in candidates if isinstance(candidate, dict)]
            if len(tokens) != 8 or tokens != sorted(tokens) or len(set(tokens)) != 8:
                raise ValueError(f"packet candidate-token drift: {key}")
            if any(set(candidate) != {"candidate_token", "source_full_skill"} for candidate in candidates):
                raise ValueError(f"packet candidate schema drift: {key}")
            if row.get("packet_input_sha256") != canonical_sha(packet):
                raise ValueError(f"packet input-hash drift: {key}")
            expected[key] = row
    if set(expected) != {
        ("A", "RQ2B-P4-V7-U1157"),
        ("B", "RQ2B-P4-V7-U0527"),
        ("B", "RQ2B-P4-V7-U0979"),
        ("B", "RQ2B-P4-V7-U1068"),
        ("B", "RQ2B-P4-V7-U1078"),
        ("B", "RQ2B-P4-V7-U1157"),
    }:
        raise ValueError("user-approved reissue lane scope drift")
    return expected, allowed_top, assessment_fields, adequacy_values


def validate_return(returned: Any, lane: str, row: dict[str, Any], allowed_top: set[str], assessment_fields: set[str], adequacy_values: set[str]) -> str | None:
    if not isinstance(returned, dict) or set(returned) != allowed_top:
        return "top-level schema drift"
    if returned["reviewer_blind_id"] != lane or returned["batch_id"] != row["batch_id"] or returned["blind_packet_id"] != row["blind_packet_id"]:
        return "return identity drift"
    if returned["batch_input_sha256"] != row["packet_input_sha256"] or returned["reviewer_instruction_sha256"] != row["protocol_instruction_sha256"]:
        return "return hash-binding drift"
    if returned["reviewer_output_sha256"] != canonical_sha({key: value for key, value in returned.items() if key != "reviewer_output_sha256"}):
        return "reviewer output-hash drift"
    packet = row["sealed_target_blind_packet"]
    expected_sources = {candidate["candidate_token"]: candidate["source_full_skill"] for candidate in packet["candidates"]}
    assessments = returned.get("assessments")
    if not isinstance(assessments, list) or len(assessments) != 8:
        return "assessment cardinality drift"
    if {assessment.get("candidate_token") for assessment in assessments if isinstance(assessment, dict)} != set(expected_sources):
        return "assessment candidate partition drift"
    for assessment in assessments:
        if not isinstance(assessment, dict) or set(assessment) != assessment_fields:
            return "assessment schema drift"
        adequacy = assessment.get("adequacy")
        missing = assessment.get("missing_material_requirement_or_null")
        if adequacy not in adequacy_values:
            return "unsupported adequacy"
        if adequacy == "FULLY_ACCEPTABLE" and missing is not None:
            return "fully acceptable assessment has non-null missing requirement"
        if adequacy != "FULLY_ACCEPTABLE" and (not isinstance(missing, str) or not missing.strip()):
            return "non-fully assessment lacks material missing requirement"
        if not isinstance(assessment.get("rationale"), str) or not assessment["rationale"].strip():
            return "empty rationale"
        if not valid_anchor(assessment.get("source_anchor"), expected_sources[assessment["candidate_token"]]):
            return "source-anchor drift"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dispatch", type=Path, default=DISPATCH)
    parser.add_argument("--return-root", type=Path, default=RETURN_ROOT)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    expected, allowed_top, assessment_fields, adequacy_values = load_expected(args.dispatch.resolve())
    root = args.return_root.resolve()
    valid: dict[tuple[str, str], dict[str, Any]] = {}
    missing: list[str] = []
    invalid: dict[str, str] = {}
    for (lane, batch_id), row in sorted(expected.items()):
        path = root / f"reviewer_{lane}" / f"{batch_id}.json"
        if not path.is_file():
            missing.append(f"{lane}:{batch_id}")
            continue
        try:
            returned = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            invalid[f"{lane}:{batch_id}"] = f"unreadable JSON: {exc}"
            continue
        problem = validate_return(returned, lane, row, allowed_top, assessment_fields, adequacy_values)
        if problem:
            invalid[f"{lane}:{batch_id}"] = problem
        else:
            valid[(lane, batch_id)] = returned
    unexpected = []
    if root.is_dir():
        for path in root.glob("reviewer_*/*.json"):
            lane = path.parent.name.removeprefix("reviewer_")
            if (lane, path.stem) not in expected:
                unexpected.append(str(path))
    rationale_locations: dict[str, list[str]] = defaultdict(list)
    for (lane, batch_id), returned in valid.items():
        for assessment in returned["assessments"]:
            rationale_locations[assessment["rationale"]].append(f"{lane}:{batch_id}:{assessment['candidate_token']}")
    duplicate_rationales = {text: locations for text, locations in rationale_locations.items() if len(locations) > 1}
    status = (
        "PASS_V7_GATE_REISSUE_RETURNS_COMPLETE"
        if not missing and not invalid and not unexpected and not duplicate_rationales
        else "PASS_V7_GATE_REISSUE_RETURNS_PARTIAL"
        if args.allow_incomplete and not invalid and not unexpected and not duplicate_rationales
        else "FAIL_V7_GATE_REISSUE_RETURN_VALIDATION"
    )
    print(json.dumps({
        "status": status,
        "dispatch": str(args.dispatch.resolve()),
        "expected_returns": len(expected),
        "valid_returns": len(valid),
        "missing_returns": missing,
        "invalid_returns": invalid,
        "unexpected_return_paths": unexpected,
        "duplicate_rationales": duplicate_rationales,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    if status.startswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
