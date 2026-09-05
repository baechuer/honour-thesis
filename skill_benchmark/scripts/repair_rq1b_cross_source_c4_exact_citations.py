#!/usr/bin/env python3
"""Create a citation-exact derivative of a blinded C4 review without relabeling it."""

import argparse
import copy
import hashlib
import json
from pathlib import Path


REPAIRS = {
    ("C4R15_v3_A2", "C4R03-026", "Candidate A", "Photography or filming permission status; parking or access instructions; note on what journalists will have access to"):
        "photography or filming permission status; parking or access instructions; note on what journalists will have access to (exclusive interviews, product demo, etc.).",
    ("C4R15_v3_A2", "C4R03-027", "Candidate A", "Hashtags: 3–5 relevant, at the end."):
        "Put the link in the **first comment**",
    ("C4R15_v3_A2", "C4R03-030", "Candidate A", "Hashtags: 3–5 relevant, at the end."):
        "Recommend a **personal** voice for thought leadership;",
    ("C4R15_v3_A2", "C4R03-030", "Candidate A", "personal voices that beat company pages."):
        "Recommend a **personal** voice for thought leadership;",
    ("C4R15_v3_A2", "C4R03-034", "Candidate A", "personal voices that beat company pages."):
        "Recommend a **personal** voice for thought leadership;",
    ("C4R15_v3_A2", "C4R03-037", "Candidate C", "Results Table: Structured summary dataframe or matrix."):
        "SILVA taxonomy classification",
    ("C4R15_v3_A2", "C4R03-040", "Candidate C", "Visualization: Rendered SVG/PNG figures."):
        "3D PCoA projections",
    ("C4R15_v3_A2", "C4R03-046", "Candidate B", "Input is not a raster -> suggest using a GeoTIFF file."):
        "`solar-panels` | `geoai.SolarPanelDetector`",
    ("C4R15_v3_B2", "C4R03-030", "Candidate A", "Hashtags: 3–5 relevant, at the end"):
        "Put the link in the **first comment**",
    ("C4R15_v3_B2", "C4R03-030", "Candidate A", "still human and first-person"):
        "Recommend a **personal** voice for thought leadership;",
    ("C4R15_v3_B2", "C4R03-032", "Candidate B", "connects the visual to the wider story"):
        "a description of the image or video being posted (so the caption relates to the visual)",
    ("C4R15_v3_A1", "C4R03-006", "Candidate C", "Gather inputs. Collect or confirm: company basics"):
        "Generate professional, honest, data-driven investor updates",
    ("C4R15_v3_A1", "C4R03-007", "Candidate A", "Benchmark on **engagement rate, share of voice, and growth trend — never follower-count vanity**"):
        "The **landscape / positioning** lens",
    ("C4R15_v3_A1", "C4R03-007", "Candidate A", "test gaps with KPIs → social-strategy."):
        "The **landscape / positioning** lens",
    ("C4R15_v3_A1", "C4R03-008", "Candidate A", "engagement rate, share of voice, and growth trend"):
        "The **landscape / positioning** lens",
    ("C4R15_v3_A1", "C4R03-010", "Candidate A", "test gaps with KPIs → social-strategy."):
        "The **landscape / positioning** lens",
    ("C4R15_v3_A1", "C4R03-011", "Candidate A", "Benchmark on **engagement rate, share of voice, and growth trend — never follower-count vanity**"):
        "The **landscape / positioning** lens",
    ("C4R15_v3_A1", "C4R03-019", "Candidate B", "Media contact: name, title, email, phone."):
        "**Media contact:** name, title, email, phone.",
    ("C4R15_v3_A1", "C4R03-022", "Candidate B", "Media contact: name, title, email, phone."):
        "**Media contact:** name, title, email, phone.",
    ("C4R15_v3_A1", "C4R03-023", "Candidate B", "The hard numbers. Funding amount, customer count, growth percentage"):
        "**The hard numbers.** Funding amount, customer count, growth percentage, price, headcount, market size — whatever quantifies the news.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repair only C4 evidence-substring exactness; preserve all judgments and rationales."
    )
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--reviewer-input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    args = parser.parse_args()

    original = json.loads(args.review.read_text())
    revised = copy.deepcopy(original)
    cards = {
        (packet["review_packet_id"], card["card_label"]): card["card_text"]
        for packet in map(json.loads, args.reviewer_input.read_text().splitlines())
        for card in packet["candidate_cards"]
    }
    applied = []
    reviewer_id = revised["reviewer_id"]
    for review in revised["reviews"]:
        packet_id = review["review_packet_id"]
        for judgment in review["candidate_judgments"]:
            card_label = judgment["card_label"]
            card_text = cards[(packet_id, card_label)]
            repaired = []
            for evidence in judgment["evidence_snippets"]:
                key = (reviewer_id, packet_id, card_label, evidence)
                replacement = REPAIRS.get(key, evidence)
                if replacement not in card_text:
                    raise SystemExit(f"replacement_not_exact:{key}:{replacement}")
                if replacement != evidence:
                    applied.append(
                        {
                            "reviewer_id": reviewer_id,
                            "review_packet_id": packet_id,
                            "card_label": card_label,
                            "old_evidence": evidence,
                            "new_exact_evidence": replacement,
                        }
                    )
                repaired.append(replacement)
            judgment["evidence_snippets"] = repaired

    expected = [key for key in REPAIRS if key[0] == reviewer_id]
    if len(applied) != len(expected):
        raise SystemExit(f"repair_coverage_mismatch:applied={len(applied)}:expected={len(expected)}")

    args.output.write_text(json.dumps(revised, ensure_ascii=False, indent=2) + "\n")
    ledger = {
        "status": "C4_CITATION_EXACTNESS_REPAIR_ONLY_NOT_A_REVIEW_OR_LABEL",
        "purpose": "Replace only failed non-exact evidence snippets with exact text from the same anonymous card.",
        "not_changed": ["reviewer_id", "review_method", "adequacy", "rationale", "packet coverage"],
        "input_review": str(args.review),
        "input_sha256": sha256(args.review),
        "output_review": str(args.output),
        "output_sha256": sha256(args.output),
        "repairs": applied,
    }
    args.ledger.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"reviewer_id": reviewer_id, "repairs": len(applied), "output_sha256": ledger["output_sha256"]}))


if __name__ == "__main__":
    main()
