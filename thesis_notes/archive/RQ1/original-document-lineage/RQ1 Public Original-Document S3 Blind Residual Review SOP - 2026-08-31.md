# RQ1 Public Original-Document S3 Blind Residual Review SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-31
Status: `S3 COMPLETE / LOCAL PROMPT-GOLD-BLIND LEAKAGE GATE / NO SELECTOR EXECUTION`

## Purpose

S3 tests whether a technically faithful S2 mask still explicitly states a
candidate-specific value of the field that was meant to be removed. It is the
semantic leakage gate between source-level deletion and any later strict-family
or selector work.

This is not a judgement about whether the remaining document is a good skill,
whether a prompt matches a candidate, or whether a field affects routing.

## Review Unit and Blinding

The unit is one materialised single-field composition-condition. A reviewer
receives only anonymous masked candidate documents, the target field category
and a fixed response schema. It does not receive original documents, source
maps, source links, prompts, gold labels, family membership, candidate
provenance, cards, scores or results.

Each candidate-field response is one of:

- `CLEAR`: no explicit candidate-specific target-field value remains;
- `RESIDUAL_FOUND`: an explicit remaining target value is present and is cited
  by masked-document line range and quote; or
- `UNCERTAIN`: the reviewer cannot determine that outcome from masked text.

At a composition-field level, every candidate must be `CLEAR` for S3 pass.
Any residual or uncertainty excludes the condition. This is deliberately
fail-closed.

## Scope and Group Derivation

S3 reviews only the seven single-field conditions that passed S2, not the
three group documents separately. A group is eligible only when:

1. its S2 group mask passed technical audit; and
2. every candidate in every component single-field condition passed S3.

This is valid because S2 group text is exactly the recorded union of its
component single-field deletions; a separate group review would duplicate the
same residual question without adding an independent source transformation.

## Mechanical Acceptance

Canonical review submissions must exactly cover their assigned condition,
candidates and target field. `RESIDUAL_FOUND` requires a valid masked-document
line range and non-empty quote; `CLEAR` and `UNCERTAIN` cite no residual line.
The coordinator verifies packet hash, output coverage and review-line bounds
before aggregation.

## S3 Closure

All 183 materialised single-field composition conditions were reviewed in 61
anonymous batches. Each canonical submission passed packet, item, candidate,
target-field and residual-line validation before aggregation. The first six
reviewer submissions were discarded before canonicalisation because an early
packet interface omitted the item-local target-field category. Reissued packets
contained that category; no output from the discarded wave entered the ledger.

| Field | Clear | Residual found | Uncertain |
| --- | ---: | ---: | ---: |
| Use condition | 2 | 19 | 0 |
| Input/precondition | 2 | 17 | 0 |
| Output artifact | 3 | 21 | 1 |
| Workflow/procedure | 0 | 22 | 0 |
| Success/verification | 11 | 21 | 0 |
| Boundary/not-for | 15 | 22 | 0 |
| Dependency/resource | 0 | 27 | 0 |

Only 33 of 183 single-field composition conditions clear the fail-closed
residual gate. None of the three pre-specified groups clears: every group has
at least one component single-field condition with residual information,
uncertainty, no source map, or the recorded S2 edit conflict.

## Closure Boundary

This ends the current full-original removal branch before strict-family
linkage and before any BM25, Qwen, API, hosted, metric or thesis-result stage.
A small survivor-only selector comparison would not answer the intended
seven-field and three-group public RQ1 comparison, so it is not created. The
result is that this non-broadening source-level deletion intervention does not
yield the planned complete-case denominator in these public documents. It is
not evidence that any field lacks routing value, and it does not alter the
separate controlled or derivative-card RQ1 evidence.
