#!/usr/bin/env python3
"""Persist independent C3 Wave 002 blind-review returns without adjudicating them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def records(reviewer: str, composition: str, entries: list[tuple[str, str, str, list[str], str]]) -> list[dict[str, object]]:
    return [
        {
            "reviewer": reviewer,
            "anonymous_composition_id": composition,
            "blind_packet_id": packet_id,
            "residual_cue_risk": risk,
            "disposition": disposition,
            "exact_cue_phrases": phrases,
            "rationale": rationale,
            "review_scope": "C3 residual-cue review only; not a label, adequacy decision, selector input, metric, or result.",
        }
        for packet_id, risk, disposition, phrases, rationale in entries
    ]


RETURNS = [
    *records("Helmholtz", "001", [
        ("001-P01", "low", "ALLOW_AS_OPERATIONAL", [], "Foreground-background pairings, hexadecimal values, thresholds, and a contrast report are necessary operational constraints without a copied title, command, package, template, or distinctive source clause."),
        ("001-P02", "low", "ALLOW_AS_OPERATIONAL", [], "The palette, text-background combinations, and pair report describe the requested work generically and contain no accidental source-identifying wording."),
        ("001-P03", "low", "ALLOW_AS_OPERATIONAL", [], "Reviewing image text alternatives and returning severity-ranked fixes is operationally necessary and does not expose a source-specific identifier."),
        ("001-P04", "low", "ALLOW_AS_OPERATIONAL", [], "The assistive-technology framing and prioritised image-description fixes are generic task details, not copied or repository-specific cues."),
        ("001-P05", "high", "REWRITE_CUE_ONLY", ["create separate files by language or locale and purpose", "translation-only subtitle text, same-language captions that include material sounds, subtitles for narrative information otherwise unavailable, a spoken-description script for visual action, and a transcript"], "This unusually specific multi-deliverable taxonomy and its language-or-locale grouping form a distinctive source-derived clause rather than only the minimum operational request."),
        ("001-P06", "high", "REWRITE_CUE_ONLY", ["issue distinct files for each locale and audience need", "translated dialogue, captions that retain meaningful sounds, subtitle material carrying otherwise missed story information, narration for visual events, and a full transcript"], "Despite paraphrasing, the detailed parallel package of locale-specific accessibility deliverables remains a distinctive residual source cue."),
    ]),
    *records("Helmholtz", "002", [
        ("002-P01", "low", "ALLOW_AS_OPERATIONAL", [], "A complete page inventory, consistent page-level assessment, spreadsheet, and short summary are ordinary operational specifications for a site-wide review."),
        ("002-P02", "low", "ALLOW_AS_OPERATIONAL", [], "The request uses generic wording for website scope, page enumeration, tabular assessment, and overview reporting, with no source-identifying phrase."),
        ("002-P03", "medium", "REWRITE_CUE_ONLY", ["Cite representative examples for each finding and produce a complete reusable style guide, noting lower confidence wherever the corpus is too small"], "The combined evidence-citation, reusable-guide, and small-corpus confidence clause is unusually close to a distinctive source workflow and can be generalised."),
        ("002-P04", "low", "ALLOW_AS_OPERATIONAL", [], "Tone, terminology, structure, corpus examples, and evidence limitations are general analytical requirements and are not a copied heading, named file, or distinctive source clause."),
        ("002-P05", "medium", "REWRITE_CUE_ONLY", ["Mark each item as acceptable, needing revision, or needing replacement", "a location-level tally, a terminology-conflict glossary, and a concise reusable style reference"], "The particular three-way decision scheme plus tally, glossary, and reusable-reference bundle is a distinctive source-derived output structure beyond the minimum task specification."),
        ("002-P06", "medium", "REWRITE_CUE_ONLY", ["Categorise each as fit to keep, needing editing, or requiring new copy", "counts of issues by surface; a glossary resolving inconsistent terms; and a brief editorial reference for future interface copy"], "The paraphrased but specific classification-and-deliverables bundle remains a residual cue and should be simplified while retaining the underlying operational intent."),
    ]),
    *records("Dalton the 2nd", "004", [
        ("004-P01", "medium", "REWRITE_CUE_ONLY", ["cash collected", "amounts that appear uncollectible", "rather than recurring subscription revenue"], "The combined collection-status and subscription-revenue contrast closely tracks distinctive source wording; the operational request can be retained with less source-specific phrasing."),
        ("004-P02", "low", "ALLOW_AS_OPERATIONAL", [], "The wording is paraphrased and describes necessary reporting constraints without a title, command, package, template, or copied distinctive clause."),
        ("004-P03", "low", "ALLOW_AS_OPERATIONAL", [], "The terms describe necessary audit inputs and requested exception categories; no source-specific heading, command, package, or distinctive copied clause appears."),
        ("004-P04", "low", "ALLOW_AS_OPERATIONAL", [], "This is an operational paraphrase of requested controls and exception types, without identifiable repository-specific wording."),
        ("004-P05", "low", "ALLOW_AS_OPERATIONAL", [], "The request uses ordinary invoice-matching and reconciliation terminology needed to specify the work, without copied source identifiers."),
        ("004-P06", "low", "ALLOW_AS_OPERATIONAL", [], "The wording is generic operational language for an item-level supporting-record comparison and does not reproduce a source-specific identifier."),
    ]),
    *records("Dalton the 2nd", "005", [
        ("005-P01", "high", "REWRITE_CUE_ONLY", ["one-way commercial confidentiality agreement", "clause by clause", "issue log", "preferred redlines", "fallback positions", "do not treat it as a mutual agreement"], "The scope gate and deliverable bundle closely reproduce distinctive source language and structure; preserve the operational intent but rewrite the source-identifying phrasing."),
        ("005-P02", "low", "ALLOW_AS_OPERATIONAL", [], "Although it retains necessary unilateral-scope constraints, it paraphrases the requested work and contains no title, command, template name, or copied distinctive clause."),
        ("005-P03", "high", "REWRITE_CUE_ONLY", ["investor rights agreement", "client's actual role", "term-by-term risk matrix", "related side letters"], "The agreement title and the combined role-specific matrix and side-letter-conflict phrasing are source-identifying rather than merely generic operational detail."),
        ("005-P04", "low", "ALLOW_AS_OPERATIONAL", [], "The request uses generalized document and review language; side letters and cross-document inconsistencies are necessary operational details, not copied identifiers here."),
        ("005-P05", "high", "REWRITE_CUE_ONLY", ["credit agreement", "represented party", "issues table", "ask which party is represented before reviewing"], "The title and the specific represented-party intake and table-output combination closely follow distinctive source wording and should be rewritten."),
        ("005-P06", "low", "ALLOW_AS_OPERATIONAL", [], "This is a generalized paraphrase of a party-perspective contract review workflow, without a source title or copied distinctive phrase."),
    ]),
    *records("Galileo", "007", [
        ("007-P01", "low", "ALLOW_AS_OPERATIONAL", [], "The request uses generic implementation requirements for a multi-user transactional data system; its details are operational constraints rather than copied source-specific wording."),
        ("007-P02", "low", "ALLOW_AS_OPERATIONAL", [], "The wording is a general paraphrase of transactional data-design requirements and contains no title, heading, named package, command, template, or distinctive copied clause."),
        ("007-P03", "low", "ALLOW_AS_OPERATIONAL", [], "Reporting, history retention, and descriptive-versus-measure records are necessary domain specifications and are expressed without a source-identifying name or distinctive phrase."),
        ("007-P04", "low", "ALLOW_AS_OPERATIONAL", [], "The request states ordinary analytics-design constraints in paraphrased language, with no copied heading, repository-specific term, or named artifact."),
        ("007-P05", "low", "ALLOW_AS_OPERATIONAL", [], "Entity-and-relationship extraction plus a machine-usable graph and readable diagram are necessary request details, not source-identifying wording."),
        ("007-P06", "low", "ALLOW_AS_OPERATIONAL", [], "The wording is generic and paraphrased; it contains no source title, specific format name, command, package, template, or distinctive clause."),
    ]),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing_to_overwrite:{args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in RETURNS),
        encoding="utf-8",
    )
    print(json.dumps({"records": len(RETURNS), "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
