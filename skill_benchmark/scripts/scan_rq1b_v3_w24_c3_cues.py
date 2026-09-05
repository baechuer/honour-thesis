#!/usr/bin/env python3
"""Produce a mechanical C3 cue scan for one RQ1b V3 C2 prompt record."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STOPWORDS = {"analyzing", "analysis", "structure", "structures", "skill", "skills", "the", "and", "for", "with", "from"}


def title_terms(title: str) -> list[str]:
    return sorted({token.lower() for token in re.findall(r"[A-Za-z][A-Za-z-]{3,}", title) if token.lower() not in STOPWORDS})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-record", type=Path, required=True)
    parser.add_argument("--c1-review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    c2 = json.loads(args.c2_record.read_text(encoding="utf-8"))
    c1 = json.loads(args.c1_review.read_text(encoding="utf-8"))
    members = c1.get("packet_members") or c1.get("member_cards")
    packets = c2.get("draft_packets")
    if not isinstance(members, list) or not isinstance(packets, list):
        raise SystemExit("invalid_c1_or_c2_record")
    title_by_source = {
        str(member.get("provisional_source_id") or member.get("source_id")): str(member.get("title", ""))
        for member in members
    }
    scans = []
    for packet in packets:
        prompt = packet.get("prompt_text")
        source_id = str(packet.get("sealed_target_source_id", ""))
        if not isinstance(prompt, str) or source_id not in title_by_source:
            raise SystemExit("invalid_packet")
        normalized = prompt.lower()
        title = title_by_source[source_id]
        matched_terms = [term for term in title_terms(title) if re.search(rf"\b{re.escape(term)}\b", normalized)]
        full_title_match = title.lower() in normalized
        scans.append(
            {
                "packet_id": packet.get("packet_id"),
                "variant": packet.get("variant"),
                "sealed_target_source_id": source_id,
                "source_title": title,
                "full_title_match": full_title_match,
                "matched_title_terms": matched_terms,
                "status": "C3_MECHANICAL_SCAN_REQUIRES_MANUAL_RESIDUAL_RISK_REVIEW",
            }
        )
    report = {
        "record_type": "RQ1B_V3_C3_MECHANICAL_CUE_SCAN",
        "c2_record": str(args.c2_record),
        "c1_review": str(args.c1_review),
        "packet_count": len(scans),
        "scans": scans,
        "boundary": [
            "This scan detects full-title and selected title-term overlaps only; it does not decide whether a term is a necessary operational fact or an unsafe identifier.",
            "It makes no C3 pass/reject, gold-label, adequacy, selector, metric or retrieval claim.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "RQ1B_V3_C3_MECHANICAL_SCAN_COMPLETE_NOT_A_RESULT", "packet_count": len(scans)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
