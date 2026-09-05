#!/usr/bin/env python3
"""Validate one source-only RQ1b V3 D1 draft against frozen source overlays."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED_EVIDENCE = ("trigger", "operation", "output")
FORBIDDEN_KEYS = {
    "prompt", "gold", "label", "winner", "acceptable_set", "selector", "metric", "representation",
}
BOUNDARY = (
    "D1 materialisation validates source binding and literal evidence only. It does not establish "
    "semantic validity, a prompt, a gold label, field recoverability, or retrieval."
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def has_forbidden_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(key.lower() in FORBIDDEN_KEYS or has_forbidden_key(child) for key, child in value.items())
    if isinstance(value, list):
        return any(has_forbidden_key(child) for child in value)
    return False


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--old-source-frame", type=Path, required=True)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest_path = args.output_dir / "d1_draft_manifest.jsonl"
    audit_path = args.output_dir / "D1_DIRECTED_DRAFT_MATERIALISATION_AUDIT.json"
    if manifest_path.exists() or audit_path.exists():
        raise ValueError("refusing to overwrite an existing D1 materialisation")

    source_index: dict[str, dict] = {}
    for row in read_jsonl(args.old_source_frame / "canonical_sources.jsonl"):
        canonical = row["canonical"]
        source_index[row["source_id"]] = {
            "source_id": row["source_id"], "sha256": row["sha256"], "title": row.get("title", ""),
            "origin_key": canonical["origin_key"], "absolute_path": canonical["absolute_path"],
            "relative_path": canonical["relative_path"],
        }
    for row in read_jsonl(args.amendment):
        canonical = row["canonical"]
        source_index[row["amendment_source_id"]] = {
            "source_id": row["amendment_source_id"], "sha256": canonical["source_sha256"], "title": "",
            "origin_key": canonical["repository_ref"], "absolute_path": str(Path(canonical["local_raw_path"]).resolve()),
            "relative_path": canonical["local_raw_path"],
        }

    drafts = read_jsonl(args.input_jsonl)
    errors: list[str] = []
    rendered: list[dict] = []
    seen_sources: set[str] = set()
    for row_number, draft in enumerate(drafts, start=1):
        prefix = f"row {row_number}"
        if has_forbidden_key(draft):
            errors.append(f"{prefix}: forbidden scientific key")
            continue
        members = draft.get("members")
        if not isinstance(members, list) or len(members) not in {3, 4}:
            errors.append(f"{prefix}: requires exactly three or four members")
            continue
        row_members: list[dict] = []
        row_ids: set[str] = set()
        for member in members:
            source_id = member.get("source_id")
            source = source_index.get(source_id)
            if source is None:
                errors.append(f"{prefix}: unknown source {source_id}")
                continue
            if source_id in row_ids:
                errors.append(f"{prefix}: duplicate source {source_id}")
                continue
            row_ids.add(source_id)
            source_path = Path(source["absolute_path"])
            if not source_path.is_file() or sha256_file(source_path) != source["sha256"]:
                errors.append(f"{prefix}: hash mismatch {source_id}")
                continue
            evidence = member.get("evidence")
            if not isinstance(evidence, dict):
                errors.append(f"{prefix}: missing evidence {source_id}")
                continue
            source_text = source_path.read_text(encoding="utf-8")
            for key in REQUIRED_EVIDENCE:
                value = evidence.get(key)
                if not isinstance(value, str) or not value.strip() or value not in source_text:
                    errors.append(f"{prefix}: nonliteral {key} evidence {source_id}")
            boundary = evidence.get("constraint")
            if boundary is not None and (not isinstance(boundary, str) or not boundary.strip() or boundary not in source_text):
                errors.append(f"{prefix}: nonliteral constraint evidence {source_id}")
            row_members.append({
                **source, "title": member.get("title", source["title"]), "evidence": evidence,
                "peer_route_reason": member.get("peer_route_reason", ""), "concern": member.get("concern", ""),
            })
        if len(row_members) == len(members):
            overlap = seen_sources.intersection(row_ids)
            if overlap:
                errors.append(f"{prefix}: source reuse across this wave {sorted(overlap)}")
            seen_sources.update(row_ids)
            rendered.append({
                "d1_draft_id": draft.get("d1_draft_id"), "discovery_lane": draft.get("discovery_lane"),
                "shared_envelope": draft.get("shared_envelope"), "members": row_members,
                "composition_concerns": draft.get("composition_concerns", []), "claim_boundary": BOUNDARY,
            })

    args.output_dir.mkdir(parents=True, exist_ok=True)
    audit = {
        "status": "PASS" if not errors else "FAIL", "records": len(rendered), "errors": errors,
        "network_calls": 0, "texts_transmitted": 0, "claim_boundary": BOUNDARY,
        "input_sha256": sha256_file(args.input_jsonl),
    }
    if errors:
        audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise SystemExit("D1 materialisation failed; manifest not written")
    manifest_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rendered), encoding="utf-8")
    audit["output_sha256"] = sha256_file(manifest_path)
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(audit_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
