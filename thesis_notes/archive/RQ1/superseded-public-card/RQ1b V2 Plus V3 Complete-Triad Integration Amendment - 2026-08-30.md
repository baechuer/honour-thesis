# RQ1b V2 Plus V3 Complete-Triad Integration Amendment

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `LOCAL COMPATIBILITY AND MATERIALISATION COMPLETE / NO SELECTOR RUN / NO EXTERNAL TRANSFER`

Date: 2026-08-30

## Purpose

This amendment cleans the reproducible direct V3 C6 inventory and admits only
the subset that has the exact evaluation shape of the RQ1b V2 field-type
experiment. It creates a prospective harmonised corpus without mutating V2 or
retrospectively calling V3 curation a selector result.

## Admission Rule

A V3 parent enters only when it has exactly three candidates, all three
target skills have one direct and one paraphrase C6 strict case, its seven
source-grounded fields follow the V2 order, and C6 binds exact C4A-card,
C4A-audit, C4B-consensus, C5 target-map and prompt-hash evidence for every
case. Its two blinded C4B reviewers must agree on the strict singleton for all
six cases. Cue risk remains a reporting stratum.

The four admitted triads are `RQ1B-V3-D1-W4-001`,
`RQ1B-V3-W29-D1-UI-DOMAIN-001`,
`RQ1B-V3-W32-D1-PRIOR-ART-SURVEY-001`, and
`RQ1B-V3-W33-D1-PATHWAY-INPUT-001`.

`RQ1B-V3-D1-W4-002` and `RQ1B-V3-D1-W4-003` each have four rather than six
frozen strict cases. They remain quarantined. No prompts, labels or cards are
invented to make an asymmetric composition look complete.

## Materialised Artifacts

`skill_benchmark/scripts/build_rq1b_v2_v3_complete_triad_extension.py` creates
the immutable local extension:

`skill_benchmark/rq1b_final_public_corpus_v1/v2_v3_complete_triad_extension_2026-08-30/`

It writes V2-shaped canonical-card and all-candidate one-field-mask artifacts
for the four imported triads, a private routing-family manifest, a compatibility
audit, a partial-triad quarantine ledger and a combined future-matrix manifest.
It copies no original source bodies and does not create embeddings, retrieval
scores, metrics, API calls or thesis results.

## Prospective Matrix And Reporting Boundary

| Component | Candidate compositions | Strict routing families | Prompts |
| --- | ---: | ---: | ---: |
| Completed native V2 | 48 | 87 | 174 |
| Imported complete V3 triads | 4 | 12 | 24 |
| Prospective V2+V3 matrix | 52 | 99 | 198 |

With `FULL` plus seven masks, a later run has 1,584 rows per retriever
(`198 prompts x 8 conditions`). Existing V2 scores stay frozen. A later run
must report native V2, imported V3 and the harmonised estimate separately;
only an identical frozen condition renderer permits that combined estimate.
A Qwen run still requires a fresh, exact-payload external-transfer approval.
