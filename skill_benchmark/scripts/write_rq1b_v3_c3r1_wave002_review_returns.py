#!/usr/bin/env python3
"""Persist the fresh, packet-level C3r1 returns for cue-rewritten packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROWS = [
    {
        "reviewer": "Bohr the 2nd", "blind_packet_id": "004-P01", "residual_cue_risk": "low", "disposition": "ALLOW_AS_OPERATIONAL", "exact_cue_phrases": [],
        "rationale": "The request states operational reporting constraints in generic terms. It contains no source title, system name, command, template label, or repository-specific wording.",
    },
    {
        "reviewer": "Bohr the 2nd", "blind_packet_id": "005-P01", "residual_cue_risk": "low", "disposition": "ALLOW_AS_OPERATIONAL", "exact_cue_phrases": [],
        "rationale": "The one-sided commercial confidentiality scope is necessary operational detail. The wording does not retain a distinctive heading, authoring metadata, or source-specific phrase.",
    },
    {
        "reviewer": "Bohr the 2nd", "blind_packet_id": "005-P03", "residual_cue_risk": "low", "disposition": "ALLOW_AS_OPERATIONAL", "exact_cue_phrases": [],
        "rationale": "The agreement type, associated documents, client position, and cross-document review are generic operational constraints. No source-identifying terminology or copied template language remains.",
    },
    {
        "reviewer": "Bohr the 2nd", "blind_packet_id": "005-P05", "residual_cue_risk": "low", "disposition": "ALLOW_AS_OPERATIONAL", "exact_cue_phrases": [],
        "rationale": "Requesting the client's side before a financing-contract review is necessary framing for the task. The wording is generic and contains no title, package name, command, or distinctive source identifier.",
    },
    {
        "reviewer": "Archimedes the 2nd", "blind_packet_id": "001-P05", "residual_cue_risk": "high", "disposition": "REJECT_UNSAFE_CUE", "exact_cue_phrases": ["determine the languages and accessibility needs", "separate captions, subtitles, spoken-description material, and transcript", "required locales"],
        "rationale": "The unusually specific bundle of deliverables and sequencing creates a highly distinctive operational signature rather than a neutral request description.",
    },
    {
        "reviewer": "Archimedes the 2nd", "blind_packet_id": "001-P06", "residual_cue_risk": "high", "disposition": "REJECT_UNSAFE_CUE", "exact_cue_phrases": ["determining its languages and significant visual and audio content", "captions, subtitles, spoken-description material, and transcript", "relevant locales"],
        "rationale": "The paraphrase retains the same distinctive multi-deliverable accessibility bundle and content-analysis framing, leaving strong residual cues.",
    },
    {
        "reviewer": "Archimedes the 2nd", "blind_packet_id": "002-P03", "residual_cue_risk": "medium", "disposition": "REWRITE_CUE_ONLY", "exact_cue_phrases": ["recurring editorial choices", "practical style guide", "conclusions limited by sparse material"],
        "rationale": "The request is broadly operational, but its combination of editorial-pattern analysis, style-guide output, and sparse-material qualification is more diagnostic than necessary.",
    },
    {
        "reviewer": "Archimedes the 2nd", "blind_packet_id": "002-P05", "residual_cue_risk": "high", "disposition": "REJECT_UNSAFE_CUE", "exact_cue_phrases": ["product-interface text in context", "preserve legally controlled wording", "future interface copy"],
        "rationale": "The interface-copy context combined with an explicit constraint on legally controlled language forms a narrow, recognizable operational cue pattern.",
    },
    {
        "reviewer": "Archimedes the 2nd", "blind_packet_id": "002-P06", "residual_cue_risk": "high", "disposition": "REJECT_UNSAFE_CUE", "exact_cue_phrases": ["in-product messages in their user context", "keep legally controlled language unchanged", "editorial guidance for later copy work"],
        "rationale": "The prompt retains a specific combination of in-product copy review, legally controlled text, and downstream editorial guidance that creates strong residual cues.",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing_to_overwrite:{args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for row in ROWS:
        row["review_scope"] = "C3r1 residual-cue review only; not a label, adequacy decision, selector input, metric, or result."
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in ROWS),
        encoding="utf-8",
    )
    print(json.dumps({"records": len(ROWS), "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
