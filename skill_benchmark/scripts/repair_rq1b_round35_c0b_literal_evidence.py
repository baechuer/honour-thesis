#!/usr/bin/env python3
"""Apply four declared citation-only repairs to the Round 35 C0B ledger.

The independent C0B reviewers supplied four otherwise valid multiline source
quotes with their line breaks encoded as literal ``\\n``.  The C0B validator
requires byte-for-byte substrings.  This guard therefore changes only the
listed evidence slots to shorter exact single-line substrings.  It preserves
every proposal id, status, candidate list, rationale, and rejection risk, and
fails closed if the supplied ledger does not match the declared locations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PATCHES = {
    (
        "R35-C0A-PRODUCT_COLLABORATION-04",
        "r35m1-Rohit-ATS-Airlock-skills-access-review",
        1,
    ): "Report what",
    (
        "R35-C0A-PRODUCT_COLLABORATION-06",
        "r35m1-CloudLandBeta-PowerRustCOBOL-agents-skills-clarify",
        0,
    ): "Optional **phase 1.5** of the spec-driven workflow (see `specs/README.md`): run",
    (
        "R35-C0A-PRODUCT_COLLABORATION-06",
        "r35m1-ashmoonori-afk-birkin-skills-planning-neurosis",
        0,
    ): "Replace a vague idea with a crystal-clear specification by asking ONE targeted",
    (
        "R35-C0A-PRODUCT_COLLABORATION-07",
        "r35m1-ashmoonori-afk-birkin-skills-quality-model-compare",
        0,
    ): "Run the **same prompt through two models** and read the answers **blind**",
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    applied: list[dict[str, object]] = []
    pending = set(PATCHES)
    for row in rows:
        proposal_id = str(row.get("proposal_id", ""))
        evidence_rows = row.get("candidate_evidence")
        if not isinstance(evidence_rows, list):
            raise SystemExit(f"candidate_evidence_missing:{proposal_id}")
        for evidence in evidence_rows:
            if not isinstance(evidence, dict):
                raise SystemExit(f"candidate_evidence_shape:{proposal_id}")
            skill_id = str(evidence.get("skill_id", ""))
            substrings = evidence.get("evidence_substrings")
            if not isinstance(substrings, list):
                raise SystemExit(f"evidence_substrings_missing:{proposal_id}:{skill_id}")
            for index in range(len(substrings)):
                key = (proposal_id, skill_id, index)
                if key not in PATCHES:
                    continue
                old = substrings[index]
                replacement = PATCHES[key]
                if not isinstance(old, str) or old == replacement:
                    raise SystemExit(f"unexpected_evidence_at_repair_location:{key}")
                substrings[index] = replacement
                applied.append({
                    "proposal_id": proposal_id,
                    "skill_id": skill_id,
                    "evidence_index": index,
                    "old_evidence": old,
                    "replacement_exact_substring": replacement,
                })
                pending.remove(key)
    if pending:
        raise SystemExit(f"repair_locations_missing:{sorted(pending)}")
    if len(applied) != len(PATCHES):
        raise SystemExit(f"repair_count:{len(applied)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    args.repair_log.parent.mkdir(parents=True, exist_ok=True)
    args.repair_log.write_text(json.dumps({
        "status": "C0B_ROUND35_LITERAL_EVIDENCE_REPAIRED_PENDING_INDEPENDENT_VALIDATION_NOT_A_CLUSTER_OR_RESULT",
        "input_ledger": str(args.input),
        "input_sha256": sha256(args.input),
        "output_ledger": str(args.output),
        "output_sha256": sha256(args.output),
        "repair_count": len(applied),
        "repairs": applied,
        "invariant": "Only the four declared evidence strings changed; no status, candidate membership, rationale, risk, prompt, label, acceptable set, retrieval input, model call, metric, or result changed.",
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "repair_written", "repair_count": len(applied)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
