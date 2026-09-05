#!/usr/bin/env python3
"""Validate and materialise RQ1b V3 D1 Wave 007 source-only drafts.

The materialiser provides mechanical provenance and literal-span validation. It
does not decide peer-route quality, prompt suitability, a gold label, field
recoverability, or any retrieval outcome.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-d1-wave007-materialiser-v2"
REQUIRED_EVIDENCE = ("trigger", "operation", "output")
ALLOWED_LANES = {"D1-7A", "D1-7B", "D1-7C", "D1-7D", "D1-7E"}
FORBIDDEN_KEYS = {
    "prompt", "gold", "label", "winner", "acceptable_set", "selector",
    "metric", "representation",
}
BOUNDARY = (
    "D1 materialisation validates source binding, prior-screen non-reuse and literal evidence only. "
    "It does not establish semantic validity, a prompt, a gold label, field recoverability or retrieval."
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def has_forbidden_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(key.lower() in FORBIDDEN_KEYS or has_forbidden_key(child) for key, child in value.items())
    if isinstance(value, list):
        return any(has_forbidden_key(child) for child in value)
    return False


def prior_source_ids(paths: list[Path]) -> set[str]:
    used: set[str] = set()
    for path in paths:
        for row in read_jsonl(path):
            used.update(member["source_id"] for member in row["members"])
    return used


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-frame", type=Path, required=True)
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prior-d1-manifest", type=Path, action="append", default=[])
    args = parser.parse_args()

    output_manifest = args.output_dir / "d1_draft_manifest.jsonl"
    audit_path = args.output_dir / "D1_WAVE_007_MATERIALISATION_AUDIT.json"
    if output_manifest.exists() or audit_path.exists():
        raise SystemExit("refusing_to_overwrite_d1_wave007_materialisation")
    if any(not path.is_file() for path in args.prior_d1_manifest):
        raise SystemExit("missing_prior_d1_manifest")

    canonical_path = args.source_frame / "canonical_sources.jsonl"
    frame_manifest_path = args.source_frame / "source_frame_manifest.json"
    canonical = {row["source_id"]: row for row in read_jsonl(canonical_path)}
    prior_ids = prior_source_ids(args.prior_d1_manifest)
    drafts = read_jsonl(args.input_jsonl)
    errors: list[str] = []
    rendered: list[dict[str, Any]] = []
    seen_draft_ids: set[str] = set()
    current_ids: set[str] = set()

    for index, draft in enumerate(drafts, start=1):
        prefix = f"row {index}"
        if has_forbidden_key(draft):
            errors.append(f"{prefix}:forbidden_scientific_field_present")
            continue
        draft_id = draft.get("d1_draft_id")
        lane = draft.get("discovery_lane")
        members = draft.get("members")
        envelope = draft.get("shared_envelope")
        if not isinstance(draft_id, str) or not draft_id or draft_id in seen_draft_ids:
            errors.append(f"{prefix}:missing_or_duplicate_draft_id")
            continue
        seen_draft_ids.add(draft_id)
        if lane not in ALLOWED_LANES or not isinstance(envelope, str) or not envelope.strip():
            errors.append(f"{draft_id}:invalid_lane_or_envelope")
            continue
        if not isinstance(members, list) or len(members) not in {3, 4}:
            errors.append(f"{draft_id}:member_count_must_be_three_or_four")
            continue
        member_ids = [member.get("source_id") for member in members if isinstance(member, dict)]
        if len(member_ids) != len(members) or len(set(member_ids)) != len(member_ids):
            errors.append(f"{draft_id}:missing_or_duplicate_member_id")
            continue
        overlap = sorted(set(member_ids) & (prior_ids | current_ids))
        if overlap:
            errors.append(f"{draft_id}:prior_or_current_source_reuse:{','.join(overlap)}")
            continue

        rendered_members: list[dict[str, Any]] = []
        for member in members:
            source_id = member["source_id"]
            source = canonical.get(source_id)
            if source is None:
                errors.append(f"{draft_id}:unknown_source:{source_id}")
                continue
            metadata = source["canonical"]
            source_path = Path(metadata["absolute_path"])
            if not source_path.is_file() or sha256_file(source_path) != source["sha256"]:
                errors.append(f"{draft_id}:source_hash_drift:{source_id}")
                continue
            evidence = member.get("evidence")
            if not isinstance(evidence, dict):
                errors.append(f"{draft_id}:missing_evidence:{source_id}")
                continue
            source_text = source_path.read_text(encoding="utf-8")
            for field in REQUIRED_EVIDENCE:
                excerpt = evidence.get(field)
                if not isinstance(excerpt, str) or not excerpt.strip() or excerpt not in source_text:
                    errors.append(f"{draft_id}:nonliteral_{field}:{source_id}")
            constraint = evidence.get("constraint")
            if constraint is not None and (
                not isinstance(constraint, str) or not constraint.strip() or constraint not in source_text
            ):
                errors.append(f"{draft_id}:nonliteral_constraint:{source_id}")
            if not isinstance(member.get("peer_route_reason"), str) or not member["peer_route_reason"].strip():
                errors.append(f"{draft_id}:missing_peer_route_reason:{source_id}")
            rendered_members.append({
                "source_id": source_id,
                "sha256": source["sha256"],
                "origin_key": metadata["origin_key"],
                "relative_path": metadata["relative_path"],
                "absolute_path": metadata["absolute_path"],
                "title": member.get("title", ""),
                "evidence": evidence,
                "peer_route_reason": member["peer_route_reason"],
                "concern": member.get("concern", ""),
            })
        if len(rendered_members) == len(members):
            rendered.append({
                "d1_draft_id": draft_id,
                "discovery_lane": lane,
                "shared_envelope": envelope,
                "members": rendered_members,
                "composition_concerns": draft.get("composition_concerns", []),
                "claim_boundary": BOUNDARY,
            })
            current_ids.update(member_ids)

    # A failed draft must never be counted as mechanically accepted merely
    # because its source identities and some of its spans were valid.
    invalid_draft_ids = {
        error.split(":", 1)[0]
        for error in errors
        if error.startswith("RQ1B-V3-D1-W7-")
    }
    if invalid_draft_ids:
        rendered = [row for row in rendered if row["d1_draft_id"] not in invalid_draft_ids]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    base_audit = {
        "version": VERSION,
        "input_records": len(drafts),
        "prior_manifest_sha256": {str(path): sha256_file(path) for path in args.prior_d1_manifest},
        "source_frame_manifest_sha256": sha256_file(frame_manifest_path),
        "input_sha256": sha256_file(args.input_jsonl),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    if errors:
        audit_path.write_text(json.dumps({
            **base_audit,
            "status": "FAIL",
            "accepted_records": len(rendered),
            "errors": errors,
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise SystemExit("D1 Wave 007 materialisation failed; no manifest was written")

    output_manifest.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rendered),
        encoding="utf-8",
    )
    audit_path.write_text(json.dumps({
        **base_audit,
        "status": "PASS",
        "records": len(rendered),
        "source_reuse_count": 0,
        "member_count_distribution": dict(sorted(Counter(len(row["members"]) for row in rendered).items())),
        "origin_count_distribution": dict(sorted(Counter(len({member["origin_key"] for member in row["members"]}) for row in rendered).items())),
        "output_sha256": sha256_file(output_manifest),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(audit_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
