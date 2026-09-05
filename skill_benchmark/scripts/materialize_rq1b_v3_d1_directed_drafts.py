#!/usr/bin/env python3
"""Validate and materialise source-only RQ1b V3 D1 discovery drafts."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-d1-directed-materialiser-v1"
REQUIRED_EVIDENCE = ("trigger", "operation", "output")
FORBIDDEN_KEYS = {"prompt", "gold", "label", "winner", "acceptable_set", "selector", "metric", "representation"}
BOUNDARY = (
    "D1 materialisation validates source binding and literal evidence only. It does not "
    "establish semantic validity, a prompt, a gold label, field recoverability, or retrieval."
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_canonical_sources(path: Path) -> dict[str, dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return {row["source_id"]: row for row in rows}


def has_forbidden_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(key.lower() in FORBIDDEN_KEYS or has_forbidden_key(child) for key, child in value.items())
    if isinstance(value, list):
        return any(has_forbidden_key(child) for child in value)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-frame", type=Path, required=True)
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    output_manifest = args.output_dir / "d1_draft_manifest.jsonl"
    audit_path = args.output_dir / "D1_DIRECTED_DRAFT_MATERIALISATION_AUDIT.json"
    if output_manifest.exists() or audit_path.exists():
        raise ValueError("refusing to overwrite a D1 materialisation")
    canonical_path = args.source_frame / "canonical_sources.jsonl"
    source_manifest_path = args.source_frame / "source_frame_manifest.json"
    canonical = load_canonical_sources(canonical_path)
    drafts = [json.loads(line) for line in args.input_jsonl.read_text().splitlines() if line.strip()]
    errors: list[str] = []
    rendered: list[dict] = []
    seen_draft_ids: set[str] = set()
    all_source_ids: list[str] = []

    for index, draft in enumerate(drafts, start=1):
        prefix = f"row {index}"
        if has_forbidden_key(draft):
            errors.append(f"{prefix}: forbidden scientific field present")
            continue
        draft_id = draft.get("d1_draft_id")
        lane = draft.get("discovery_lane")
        envelope = draft.get("shared_envelope")
        members = draft.get("members")
        if not isinstance(draft_id, str) or not draft_id or draft_id in seen_draft_ids:
            errors.append(f"{prefix}: missing or duplicate d1_draft_id")
            continue
        seen_draft_ids.add(draft_id)
        if lane not in {"D1-A", "D1-B"} or not isinstance(envelope, str) or not envelope.strip():
            errors.append(f"{draft_id}: missing discovery lane or shared envelope")
            continue
        if not isinstance(members, list) or len(members) not in {3, 4}:
            errors.append(f"{draft_id}: member count must be three or four")
            continue
        member_ids = [member.get("source_id") for member in members if isinstance(member, dict)]
        if len(member_ids) != len(members) or len(set(member_ids)) != len(member_ids):
            errors.append(f"{draft_id}: missing or duplicated source IDs")
            continue

        rendered_members = []
        for member in members:
            source = canonical.get(member["source_id"])
            if source is None:
                errors.append(f"{draft_id}: unknown source {member['source_id']}")
                continue
            metadata = source["canonical"]
            source_path = Path(metadata["absolute_path"])
            if not source_path.is_file() or sha256_file(source_path) != source["sha256"]:
                errors.append(f"{draft_id}: source hash drift {member['source_id']}")
                continue
            evidence = member.get("evidence")
            if not isinstance(evidence, dict):
                errors.append(f"{draft_id}: missing evidence for {member['source_id']}")
                continue
            source_text = source_path.read_text(encoding="utf-8")
            for field in REQUIRED_EVIDENCE:
                excerpt = evidence.get(field)
                if not isinstance(excerpt, str) or not excerpt.strip() or excerpt not in source_text:
                    errors.append(f"{draft_id}: nonliteral {field} evidence for {member['source_id']}")
            constraint = evidence.get("constraint")
            if constraint is not None and (not isinstance(constraint, str) or not constraint.strip() or constraint not in source_text):
                errors.append(f"{draft_id}: nonliteral constraint evidence for {member['source_id']}")
            if not isinstance(member.get("peer_route_reason"), str) or not member["peer_route_reason"].strip():
                errors.append(f"{draft_id}: missing peer_route_reason for {member['source_id']}")
            rendered_members.append({
                "source_id": member["source_id"],
                "sha256": source["sha256"],
                "origin_key": metadata["origin_key"],
                "relative_path": metadata["relative_path"],
                "absolute_path": metadata["absolute_path"],
                "title": member.get("title", ""),
                "evidence": evidence,
                "peer_route_reason": member.get("peer_route_reason", ""),
                "concern": member.get("concern", ""),
            })
        if len(rendered_members) == len(members):
            all_source_ids.extend(member_ids)
            rendered.append({
                "d1_draft_id": draft_id,
                "discovery_lane": lane,
                "shared_envelope": envelope,
                "members": rendered_members,
                "composition_concerns": draft.get("composition_concerns", []),
                "claim_boundary": BOUNDARY,
            })

    args.output_dir.mkdir(parents=True, exist_ok=True)
    if errors:
        audit_path.write_text(json.dumps({
            "status": "FAIL", "version": VERSION, "input_records": len(drafts), "accepted_records": len(rendered),
            "errors": errors, "network_calls": 0, "texts_transmitted": 0, "claim_boundary": BOUNDARY,
        }, indent=2, sort_keys=True) + "\n")
        raise SystemExit("D1 materialisation failed; no manifest was written")
    output_manifest.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rendered))
    origins_per_draft = [len({member["origin_key"] for member in row["members"]}) for row in rendered]
    audit_path.write_text(json.dumps({
        "status": "PASS", "version": VERSION, "records": len(rendered),
        "member_count_distribution": dict(sorted(Counter(len(row["members"]) for row in rendered).items())),
        "source_reuse_count": len(all_source_ids) - len(set(all_source_ids)),
        "origin_count_distribution": dict(sorted(Counter(origins_per_draft).items())),
        "input_sha256": sha256_file(args.input_jsonl),
        "output_sha256": sha256_file(output_manifest),
        "source_frame_manifest_sha256": sha256_file(source_manifest_path),
        "network_calls": 0, "texts_transmitted": 0, "claim_boundary": BOUNDARY,
    }, indent=2, sort_keys=True) + "\n")
    print(audit_path.read_text())


if __name__ == "__main__":
    main()
