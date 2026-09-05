#!/usr/bin/env python3
"""Audit source binding and literal excerpts in an RQ1b V3 D1 triage review."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DECISIONS = {"READY_FOR_C1", "LIKELY_NONPARALLEL", "NO_PLAUSIBLE_THIRD", "NEEDS_PARENT_REVIEW"}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--amendment",
        type=Path,
        action="append",
        required=True,
        help="Frozen amendment manifest. Repeat for a cross-wave review.",
    )
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    review = json.loads(args.review.read_text(encoding="utf-8"))
    errors: list[str] = []
    sources: dict[str, dict] = {}
    for amendment in args.amendment:
        for row in read_jsonl(amendment):
            source_id = row.get("amendment_source_id")
            if not isinstance(source_id, str) or not source_id:
                errors.append(f"invalid_source_id:{amendment}")
                continue
            if source_id in sources:
                errors.append(f"duplicate_source_id_across_amendments:{source_id}")
                continue
            sources[source_id] = row
    checked_members = 0
    checked_literals = 0
    review_scope = review.get("review_scope")
    if not isinstance(review_scope, dict):
        errors.append("invalid_review_scope_not_object")
        reviewed_ids: set[str] = set()
    else:
        raw_reviewed_ids = review_scope.get("reviewed_source_ids", [])
        if not isinstance(raw_reviewed_ids, list) or not all(isinstance(source_id, str) for source_id in raw_reviewed_ids):
            errors.append("invalid_reviewed_source_ids")
            reviewed_ids = set()
        else:
            reviewed_ids = set(raw_reviewed_ids)
    for composition in review.get("candidate_compositions", []):
        decision = composition.get("structural_decision")
        if decision not in DECISIONS:
            errors.append(f"invalid_decision:{composition.get('composition_id')}")
        members = composition.get("members", [])
        if not members:
            errors.append(f"missing_members:{composition.get('composition_id')}")
            continue
        source_texts: list[str] = []
        for member in members:
            source_id = member.get("source_id")
            source = sources.get(source_id)
            if source is None:
                errors.append(f"unknown_source:{source_id}")
                continue
            if source_id not in reviewed_ids:
                errors.append(f"member_not_in_review_scope:{source_id}")
            canonical = source["canonical"]
            path = Path(canonical["local_raw_path"])
            if not path.is_file() or sha256(path) != canonical["source_sha256"]:
                errors.append(f"source_binding_mismatch:{source_id}")
                continue
            if member.get("local_raw_path") != canonical["local_raw_path"]:
                errors.append(f"path_mismatch:{source_id}")
            if member.get("artifact_path") != canonical["artifact_path"]:
                errors.append(f"artifact_path_mismatch:{source_id}")
            if member.get("source_sha256") != canonical["source_sha256"]:
                errors.append(f"hash_mismatch:{source_id}")
            text = path.read_text(encoding="utf-8", errors="replace")
            source_texts.append(text)
            for literal in member.get("literal_evidence", []):
                checked_literals += 1
                if not isinstance(literal, str) or not literal or literal not in text:
                    errors.append(f"invalid_member_literal:{source_id}:{literal!r}")
            checked_members += 1
        joined = "\n".join(source_texts)
        for literal in composition.get("literal_envelope_evidence", []):
            checked_literals += 1
            if not isinstance(literal, str) or not literal or literal not in joined:
                errors.append(f"invalid_envelope_literal:{composition.get('composition_id')}:{literal!r}")

    output = {
        "status": "PASS" if not errors else "FAIL",
        "amendments": [str(path) for path in args.amendment],
        "review": str(args.review),
        "composition_count": len(review.get("candidate_compositions", [])),
        "checked_member_count": checked_members,
        "checked_literal_count": checked_literals,
        "errors": errors,
        "claim_boundary": "This audit verifies only the frozen source ID, canonical artifact path, local-byte path/hash binding, and that quoted excerpts are literal substrings. It does not decide shared envelopes, peer roles, C1 eligibility, prompts, labels, selectors, retrieval, or results.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
