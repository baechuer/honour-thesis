#!/usr/bin/env python3
"""Materialise proposal-scoped Round 31 C3 cue-review packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--c1", type=Path, required=True)
    parser.add_argument("--packet-manifest", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    prompts = read_jsonl(args.prompts)
    c1 = [row for row in read_jsonl(args.c1) if row.get("c1_status") == "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT"]
    packets: dict[str, dict[str, str]] = {}
    for row in read_jsonl(args.packet_manifest):
        proposal_id = str(row.get("proposal_id", ""))
        skill_id = str(row.get("skill_id", ""))
        if proposal_id and skill_id:
            packets.setdefault(proposal_id, {})[skill_id] = str(row.get("packet_original_path", ""))

    args.output_directory.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    failures: list[str] = []
    for index, record in enumerate(sorted(c1, key=lambda row: str(row["proposal_id"])), 1):
        proposal_id = str(record["proposal_id"])
        candidate_ids = [str(value) for value in record["candidate_skill_ids"]]
        selected = [row for row in prompts if str(row.get("proposal_id")) == proposal_id]
        expected = {(skill_id, variant) for skill_id in candidate_ids for variant in ("direct", "paraphrase")}
        observed = {(str(row.get("intended_candidate_skill_id")), str(row.get("variant"))) for row in selected}
        if expected != observed:
            failures.append(f"prompt_coverage:{proposal_id}")
        paths = packets.get(proposal_id, {})
        if set(paths) != set(candidate_ids) or any(not Path(paths[skill_id]).is_file() for skill_id in candidate_ids):
            failures.append(f"packet_alignment:{proposal_id}")
        payload = {
            "c3_packet_status": "C3_MANUAL_CUE_REVIEW_PACKET_NOT_A_LABEL_OR_RESULT",
            "proposal_id": proposal_id,
            "candidate_originals": [
                {"skill_id": skill_id, "packet_original_path": paths.get(skill_id)}
                for skill_id in candidate_ids
            ],
            "prompt_drafts": selected,
            "exclusions": [
                "This packet is only for model-assisted manual cue review, not human review.",
                "No adequacy judgement, gold label, acceptable set, retrieval input, metric, or result exists.",
            ],
        }
        output = args.output_directory / f"c3_round31_group_{index:02d}_manual_review_packet_2026-08-28.json"
        output.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        outputs.append(str(output))

    summary = {
        "status": "C3_ROUND31_MANUAL_PACKETS_READY_NOT_A_LABEL_OR_RESULT" if not failures else "C3_ROUND31_MANUAL_PACKETS_INCOMPLETE_NOT_A_LABEL_OR_RESULT",
        "packet_count": len(outputs),
        "outputs": outputs,
        "failures": failures,
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "packet_count": len(outputs), "failures": failures}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
