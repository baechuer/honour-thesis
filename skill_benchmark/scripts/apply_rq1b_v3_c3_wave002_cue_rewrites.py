#!/usr/bin/env python3
"""Apply the principal-approved C3 Wave 002 cue-only rewrites.

Every rewrite is tied to a blind C3 review finding.  The sealed target, input
class, requested operation, and deliverable class are retained.  This script
does not adjudicate adequacy or create a label/result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REWRITES_BY_BLIND_PACKET = {
    "001-P05": "Given a video, determine the languages and accessibility needs, then create the appropriate separate captions, subtitles, spoken-description material, and transcript for the required locales.",
    "001-P06": "Prepare the accessibility text deliverables required for this video after determining its languages and significant visual and audio content. Provide the needed captions, subtitles, spoken-description material, and transcript for the relevant locales.",
    "002-P03": "Analyse the supplied organisational content for recurring editorial choices. Support the assessment with examples and provide a practical style guide, noting conclusions limited by sparse material.",
    "002-P05": "Review the supplied product-interface text in context. Identify issues, recommend revisions where appropriate, preserve legally controlled wording, and summarise patterns that should guide future interface copy.",
    "002-P06": "Assess the supplied in-product messages in their user context. Identify wording that should change, keep legally controlled language unchanged, and summarise recurring issues and editorial guidance for later copy work.",
    "004-P01": "For the requested period, summarise customer billing records by invoices issued, payments received, and balances unlikely to be recovered. Base the revenue view on realised payments rather than recurring estimates.",
    "005-P01": "Assess the terms of a commercial confidentiality contract that binds only one side. Record material risks and proposed negotiation changes appropriate to that arrangement.",
    "005-P03": "Review a business ownership agreement and associated supplementary agreements from the client's position. Identify material term risks, cross-document inconsistencies, and changes required before approval.",
    "005-P05": "Review the supplied financing contract from the client's stated side. If that side is unclear, obtain it first; list material issues, their impacts, and proposed revisions.",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2-ledger", type=Path, required=True)
    parser.add_argument("--sealed-mapping", type=Path, required=True)
    parser.add_argument("--c3-reviews", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.audit.exists():
        raise SystemExit("refusing_to_overwrite_c3r1")
    mapping = json.loads(args.sealed_mapping.read_text(encoding="utf-8"))
    blind_to_c2 = {row["blind_packet_id"]: row["c2_packet_id"] for row in mapping}
    reviews = {row["blind_packet_id"]: row for row in read_jsonl(args.c3_reviews)}
    c2_rows = read_jsonl(args.c2_ledger)
    rewrite_by_c2 = {}
    failures: list[str] = []
    for blind_id, replacement in REWRITES_BY_BLIND_PACKET.items():
        if blind_id not in blind_to_c2 or blind_id not in reviews:
            failures.append(f"missing_blind_lineage:{blind_id}")
            continue
        if reviews[blind_id]["disposition"] != "REWRITE_CUE_ONLY":
            failures.append(f"rewrite_without_c3_review:{blind_id}")
            continue
        rewrite_by_c2[blind_to_c2[blind_id]] = (blind_id, replacement, reviews[blind_id])
    if failures:
        raise SystemExit(";".join(failures))

    changed: list[dict[str, Any]] = []
    rewritten: list[dict[str, Any]] = []
    for row in c2_rows:
        clone = dict(row)
        packet_id = str(clone["c2_packet_id"])
        if packet_id in rewrite_by_c2:
            blind_id, replacement, review = rewrite_by_c2[packet_id]
            prior = str(clone["prompt_text"])
            clone["prompt_text"] = replacement
            clone["c3_cue_revision"] = {
                "revision": "r1",
                "blind_packet_id": blind_id,
                "reason": "C3 requested a cue-only rewrite; preserves the same intended operation and deliverable class while removing source-shaped wording.",
                "prior_prompt_text": prior,
                "c3_exact_cue_phrases": review["exact_cue_phrases"],
                "changed_fields": ["prompt_text", "c3_cue_revision"],
                "sealed_target_changed": False,
                "operational_intent_changed": False,
            }
            changed.append({"blind_packet_id": blind_id, "c2_packet_id": packet_id})
        rewritten.append(clone)
    expected = set(rewrite_by_c2)
    observed = {row["c2_packet_id"] for row in changed}
    if observed != expected:
        raise SystemExit("rewrite_coverage_mismatch")
    rewritten.sort(key=lambda row: str(row["c2_packet_id"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rewritten),
        encoding="utf-8",
    )
    audit = {
        "status": "C3_CUE_ONLY_REWRITE_APPLIED_NOT_A_LABEL_OR_RESULT",
        "input_c2_ledger_sha256": sha256(args.c2_ledger),
        "sealed_mapping_sha256": sha256(args.sealed_mapping),
        "c3_reviews_sha256": sha256(args.c3_reviews),
        "output_sha256": sha256(args.output),
        "row_count": len(rewritten),
        "changed_packet_count": len(changed),
        "changed_packets": changed,
        "network_calls": 0,
        "texts_transmitted": 0,
        "exclusions": [
            "No final C3 cue decision, C4 adequacy judgment, label, selector input, model call, metric, or result was created.",
        ],
    }
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
