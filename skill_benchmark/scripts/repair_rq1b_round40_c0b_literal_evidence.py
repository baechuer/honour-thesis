#!/usr/bin/env python3
"""Apply two citation-only repairs to the Round 40 C0B ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPAIRS = {
    (
        "R40-C0A-cloud_data_engineering-02",
        "r40m1-Lightbridge-KS-agent-stuff-plugins-coding-skills-data-architecture",
        0,
    ): (
        "One Markdown doc with Mermaid diagrams.",
        "One Markdown doc\n  with Mermaid diagrams.",
    ),
    (
        "R40-C0A-cloud_data_engineering-05",
        "r40m1-amaniagent-skills-memory-layered-agent-memory",
        1,
    ): (
        "Split the memory into **two repositories that mirror the same folder shape**",
        "Split the memory into **two repositories that mirror\nthe same folder shape**",
    ),
    (
        "R40-C0A-web_commerce_automation-05",
        "r40m1-juicer-io-skills-topic-scout-skills-topic-scout",
        1,
    ): (
        "The output is a ranked, evidence-linked shortlist to validate against search demand and existing coverage — not a publish list.",
        "The\noutput is a ranked, evidence-linked shortlist to validate against search\ndemand and existing coverage — not a publish list.",
    ),
    (
        "R40-C0A-web_commerce_automation-06",
        "r40m1-juicer-io-skills-mention-scout-skills-mention-scout",
        0,
    ): (
        "Find the conversations your brand should be part of — and how to show up well.",
        "Find the conversations your brand should be part of — and how to show up\nwell.",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()

    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    before = {
        str(row["proposal_id"]): {
            "status": row.get("c0b_status"),
            "candidate_skill_ids": row.get("candidate_skill_ids"),
            "route_out_or_containment_risks": row.get("route_out_or_containment_risks"),
            "source_review_rationale": row.get("source_review_rationale"),
        }
        for row in rows
    }
    matched: list[dict[str, object]] = []
    for row in rows:
        for evidence in row.get("candidate_evidence", []):
            substrings = evidence.get("evidence_substrings")
            if not isinstance(substrings, list):
                continue
            for index, value in enumerate(substrings):
                key = (str(row.get("proposal_id")), str(evidence.get("skill_id")), index)
                repair = REPAIRS.get(key)
                if repair is None:
                    continue
                old, replacement = repair
                if value != old:
                    raise SystemExit(f"unexpected_target_evidence:{key}")
                substrings[index] = replacement
                matched.append({
                    "proposal_id": key[0],
                    "skill_id": key[1],
                    "evidence_index": index,
                    "old_evidence": old,
                    "replacement_exact_substring": replacement,
                })
    if len(matched) != len(REPAIRS):
        raise SystemExit(f"expected_repairs:{len(REPAIRS)}:actual:{len(matched)}")
    after = {
        str(row["proposal_id"]): {
            "status": row.get("c0b_status"),
            "candidate_skill_ids": row.get("candidate_skill_ids"),
            "route_out_or_containment_risks": row.get("route_out_or_containment_risks"),
            "source_review_rationale": row.get("source_review_rationale"),
        }
        for row in rows
    }
    if before != after:
        raise SystemExit("non_citation_fields_changed")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    args.repair_log.write_text(json.dumps({
        "status": "C0B_ROUND40_LITERAL_EVIDENCE_REPAIRED_PENDING_INDEPENDENT_VALIDATION_NOT_A_CLUSTER_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "repairs": matched,
        "invariant": "Only declared evidence strings changed; no status, candidate membership, source-review rationale, risk, prompt, label, acceptable set, retrieval input, model call, metric, or result changed.",
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "repair_written", "repair_count": len(matched)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
